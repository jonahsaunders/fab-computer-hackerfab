"""Build the FAB Computer wired mechanical assembly from three KiCad STEP exports."""
from dataclasses import dataclass
from math import acos, cos, hypot, pi, sin, tan
from pathlib import Path
import argparse
import re
import subprocess

from OCP.BRepBuilderAPI import (
    BRepBuilderAPI_MakeEdge, BRepBuilderAPI_MakeFace, BRepBuilderAPI_MakeWire,
)
from OCP.BRepPrimAPI import BRepPrimAPI_MakeCone, BRepPrimAPI_MakeRevol, BRepPrimAPI_MakeSphere
from OCP.IFSelect import IFSelect_RetDone
from OCP.Interface import Interface_Static
from OCP.Quantity import Quantity_Color, Quantity_TOC_RGB
from OCP.STEPCAFControl import STEPCAFControl_Reader, STEPCAFControl_Writer
from OCP.STEPControl import STEPControl_AsIs
from OCP.TCollection import TCollection_ExtendedString
from OCP.TDataStd import TDataStd_Name
from OCP.TDF import TDF_Label, TDF_LabelSequence
from OCP.TDocStd import TDocStd_Document
from OCP.TopLoc import TopLoc_Location
from OCP.gp import gp_Ax1, gp_Ax2, gp_Circ, gp_Dir, gp_Pnt, gp_Trsf, gp_Vec
from OCP.XCAFDoc import XCAFDoc_ColorGen, XCAFDoc_DocumentTool

import build_enclosure as case


REPO = Path(__file__).resolve().parents[2]
MODULE = "daughterboards/micromanipulator/hardware"
PCBS = {
    "host": ("hardware/backplane/HackerfabBackplane.kicad_pcb", "46x184mm", "Host backplane"),
    "motion": (f"{MODULE}/daughterboard/FabNanoDaughterboard.kicad_pcb", "60.63x55.08mm", "Motion card in J1"),
    "encoder": (f"{MODULE}/encoder-backplane/EncoderBackplane.kicad_pcb", "60x55.08mm", "Encoder card in J3"),
}

CASE = "Printed enclosure"
FIXINGS = "Mechanical fasteners and cable ties"
TOOLS = "Tool harness at motion card"
ENCODERS = "Three encoder harnesses"
SERVICE = "DC and USB connections"
IVORY = (231, 225, 206)
BLACK = (35, 42, 49)
METAL = (175, 187, 196)
DARK_METAL = (122, 140, 151)
INSERT_METAL = (182, 188, 188)
TOOL = (143, 82, 53)
ENC = (59, 112, 135)
SLEEVE = (43, 51, 59)


@dataclass
class Part:
    group: str
    name: str
    solid: object
    rgb: tuple


def part(group, name, solid, rgb):
    if solid.IsNull():
        raise RuntimeError(f"Empty model for {name}")
    return Part(group, name, solid, rgb)


def add(a, b):
    return tuple(x + y for x, y in zip(a, b))


def sub(a, b):
    return tuple(x - y for x, y in zip(a, b))


def times(vector, scale):
    return tuple(x * scale for x in vector)


def distance(a, b):
    return hypot(*sub(a, b))


def unit(vector):
    return times(vector, 1 / hypot(*vector))


def dot(a, b):
    return sum(x*y for x, y in zip(a, b))


def cross(a, b):
    return (a[1]*b[2]-a[2]*b[1], a[2]*b[0]-a[0]*b[2], a[0]*b[1]-a[1]*b[0])


def pipe(points, radius, trim=12.0):
    """Exact cylinders and circular bends keep the STEP small and editable."""
    solids = []
    current = points[0]

    def straight(end):
        delta = sub(end, current)
        length = hypot(*delta)
        if length > 0.0001:
            solids.append(case.cylinder(*current, radius, length, delta))

    for before, corner, after in zip(points, points[1:], points[2:]):
        in_dir = unit(sub(corner, before))
        out_dir = unit(sub(after, corner))
        turn = acos(max(-1.0, min(1.0, dot(in_dir, out_dir))))
        if turn < 0.00001:
            continue
        length = min(trim, 0.44 * distance(corner, before), 0.44 * distance(after, corner))
        begin = sub(corner, times(in_dir, length))
        end = add(corner, times(out_dir, length))
        normal = unit(cross(in_dir, out_dir))
        bend_radius = length / tan(turn / 2)
        if bend_radius <= radius:
            raise RuntimeError(f"Route bend at {corner} needs radius above {radius:.2f} mm")
        center = add(begin, times(cross(normal, in_dir), bend_radius))
        straight(begin)
        circle = gp_Circ(gp_Ax2(gp_Pnt(*begin), gp_Dir(*in_dir)), radius)
        wire = BRepBuilderAPI_MakeWire(BRepBuilderAPI_MakeEdge(circle).Edge()).Wire()
        section = BRepBuilderAPI_MakeFace(wire).Face()
        solids.append(BRepPrimAPI_MakeRevol(section, gp_Ax1(gp_Pnt(*center), gp_Dir(*normal)), turn, True).Shape())
        current = end
    straight(points[-1])
    return case.fuse(solids[0], *solids[1:])


def hex_prism(radius, height):
    return case.prism([(radius * cos(pi / 6 + i * pi / 3),
                        radius * sin(pi / 6 + i * pi / 3), 0) for i in range(6)], (0, 0, height))


def axis_x(shape, x, y, z):
    return move(turn(shape, (0, 1, 0), pi / 2), x, y, z)


def move(shape, x, y, z):
    transform = gp_Trsf()
    transform.SetTranslation(gp_Vec(x, y, z))
    return shape.Moved(TopLoc_Location(transform))


def turn(shape, axis, angle):
    transform = gp_Trsf()
    transform.SetRotation(gp_Ax1(gp_Pnt(0, 0, 0), gp_Dir(*axis)), angle)
    return shape.Moved(TopLoc_Location(transform))


def metal_fasteners():
    def button_screw(length):
        shaft = case.cylinder(0, 0, -length, 1.47, length + 0.025)
        # A spherical crown clipped at the underside gives the ISO button-head envelope.
        sphere = BRepPrimAPI_MakeSphere(gp_Pnt(0, 0, -1.63), 3.28).Shape()
        crown = case.cut(sphere, case.box(-4, -4, -6, 8, 8, 6))
        hex_socket = case.translate(hex_prism(2.0 / (3**0.5), 1.10), 0, 0, 0.60)
        return case.cut(case.fuse(shaft, crown), hex_socket)

    def insert():
        body = case.cylinder(0, 0, -3.4, 2.03, 3.4)
        for z in (-3.05, -1.85, -0.65):
            flange = BRepPrimAPI_MakeCone(gp_Ax2(gp_Pnt(0, 0, z), gp_Dir(0, 0, 1)),
                                          2.13, 2.03, 0.42).Shape()
            body = case.fuse(body, flange)
        return case.cut(body, case.cylinder(0, 0, -3.45, 1.30, 3.55))

    result = []
    m3x6, m3x8, m3_insert = button_screw(6), button_screw(8), insert()
    washer = case.cut(case.cylinder(0, 0, 0, 3.5, 0.50), case.cylinder(0, 0, -0.05, 1.60, 0.60))

    def vertical(name, x, y, bearing, insert_top, screw):
        return [
            part(FIXINGS, name + " screw", move(screw, x, y, bearing), METAL),
            part(FIXINGS, name + " heat-set insert", move(m3_insert, x, y, insert_top), INSERT_METAL),
        ]

    for i, (x, y) in enumerate(case.H1_H4, 1):
        seat = case.BOARD_BOTTOM + case.BOARD_THICKNESS
        result += vertical(f"PCB mount {i}", x, y, seat + 0.50, case.BOARD_BOTTOM, m3x6)
        result.append(part(FIXINGS, f"PCB mount {i} nylon washer", move(washer, x, y, seat), IVORY))
    for i, (x, y) in enumerate(case.LID_SCREWS, 1):
        seat = case.BODY_HEIGHT + case.LID_THICKNESS - 1.25
        result += vertical(f"Lid mount {i}", x, y, seat, case.BODY_HEIGHT, m3x8)
    for keeper in case.KEEPERS:
        result += vertical(keeper.name[3:], keeper.anchor_x, keeper.anchor_y, keeper.deck_z + 4,
                           keeper.deck_z, m3x8)
    for gate in case.GATES:
        for side, y in enumerate((gate.y - case.GATE_SCREW_SPAN / 2, gate.y + case.GATE_SCREW_SPAN / 2), 1):
            result += [
                part(FIXINGS, f"{gate.name[3:]} screw {side}", axis_x(m3x8, case.WIDTH, y, case.GATE_SCREW_Z), METAL),
                part(FIXINGS, f"{gate.name[3:]} insert {side}",
                     axis_x(m3_insert, case.WIDTH - case.GATE_RECESS, y, case.GATE_SCREW_Z), INSERT_METAL),
            ]
    return result


def tie(gate, cable_z, radius):
    x = 155.0
    y = gate.y
    bottom = gate.tie_top - 3.65

    def arch(r, side, lower, end):
        shoulder = gate.tie_top + 0.55
        return [(end, y-side, lower), (end, y+side, lower), (end, y+side, shoulder)] + [
            (end, y + r*cos(i*pi/18), cable_z + r*sin(i*pi/18)) for i in range(19)
        ] + [(end, y-side, shoulder)]

    outer = case.prism(arch(radius + 1.35, 8.18, bottom - 0.48, x), (2.5, 0, 0))
    inner = case.prism(arch(radius + 0.47, 7.30, bottom + 0.48, x - 0.05), (2.6, 0, 0))
    band = case.cut(outer, inner)
    head = case.box(x-0.5, y+radius+0.15, cable_z-1.5, 3.5, 2.35, 3.0)
    return part(FIXINGS, gate.name[3:] + " cable tie", case.fuse(band, head), BLACK)


def use_step_exports(folder, kicad):
    folder.mkdir(parents=True, exist_ok=True)
    for name, (relative, origin, _) in PCBS.items():
        output = folder / f"pcb-{name}.step"
        if output.is_file():
            continue
        run = subprocess.run([kicad, "pcb", "export", "step", "--subst-models", "--force",
                              "--user-origin", origin, "--output", str(output), str(REPO / relative)],
                             capture_output=True, text=True)
        if not output.is_file() or output.stat().st_size < 10000:
            raise RuntimeError(run.stdout + run.stderr)


def pcb_shapes(path):
    doc = TDocStd_Document(TCollection_ExtendedString("PCB model"))
    reader = STEPCAFControl_Reader()
    if reader.ReadFile(str(path)) != IFSelect_RetDone or not reader.Transfer(doc):
        raise RuntimeError(f"Could not read {path}")
    tool = XCAFDoc_DocumentTool.ShapeTool_s(doc.Main())
    roots = TDF_LabelSequence()
    tool.GetFreeShapes(roots)
    children = TDF_LabelSequence()
    tool.GetComponents_s(roots.Value(1), children, False)

    def name(label):
        attr = TDataStd_Name()
        return attr.Get().ToExtString() if label.FindAttribute(TDataStd_Name.GetID_s(), attr) else ""

    for i in range(1, children.Length() + 1):
        child = children.Value(i)
        target = TDF_Label()
        if tool.GetReferredShape_s(child, target):
            yield name(child), name(target), tool.GetShape_s(child)


def fit_board(board, solid):
    if board == "host":
        return move(solid, *case.HOST)
    row_y = case.MOTION_Y if board == "motion" else case.ENCODER_Y
    return move(turn(solid, (1, 0, 0), -pi / 2), case.CARD_A1_X, row_y - 1.6, case.CARD_A1_Z)


def motion_envelopes():
    """Convert the board's six box-based VRML models to exact STEP solids."""
    path = REPO / PCBS["motion"][0]
    raw = path.read_text(encoding="utf-8")
    for block in re.split(r"(?m)(?=^\t\(footprint )", raw)[1:]:
        model = re.search(r'\(model "\$\{KIPRJMOD\}/([^"]+\.wrl)"', block)
        if not model:
            continue
        x, y, *angle = map(float, re.search(r"\n\t\t\(at ([^)]*)\)", block)[1].split())
        ref = re.search(r'\(property "Reference" "([^"]+)"', block)[1]
        source = (path.parent / model[1]).read_text(encoding="utf-8")
        boxes = re.findall(r"translation ([^{}]+?) children .*?diffuseColor ([^{}]+?) \}.*?Box \{ size ([^{}]+?) \}", source)
        if not boxes:
            raise RuntimeError(f"Missing box geometry for {ref}")
        for i, (location, rgb, size) in enumerate(boxes, 1):
            xyz = [float(v) * 2.54 for v in location.split()]
            dims = [float(v) * 2.54 for v in size.split()]
            solid = case.box(*(a-b/2 for a, b in zip(xyz, dims)), *dims)
            if angle:
                solid = case.rotate(solid, (0, 0, 1), angle[0]*pi/180)
            solid = case.translate(solid, x-60.63, 55.08-y, 1.6012)
            yield part(PCBS["motion"][2], f"{ref} model segment {i}", fit_board("motion", solid),
                       tuple(round(float(v)*255) for v in rgb.split()))


def pcb_parts(folder):
    result = []
    positions = {}
    pcb_colors = {"host": (31, 103, 88), "motion": (30, 121, 101), "encoder": (36, 137, 113)}
    for board, (_, _, group) in PCBS.items():
        for ref, title, shape in pcb_shapes(folder / f"pcb-{board}.step"):
            solid = fit_board(board, shape)
            if "_PCB" in title:
                ref, rgb = "PCB", pcb_colors[board]
            elif "KF128" in title:
                rgb = (81, 151, 104)
            elif "USB" in title:
                rgb = METAL
            elif ref.startswith("J"):
                rgb = IVORY if any(s in title for s in ("JST", "DIN", "SH1.0", "WingTAT")) else BLACK
            elif ref.startswith("C") and "CP" in title:
                rgb = METAL
            elif ref.startswith("C"):
                rgb = (150, 132, 103)
            elif ref.startswith("R"):
                rgb = (69, 75, 77)
            else:
                rgb = BLACK
            result.append(part(group, ref + " " + title, solid, rgb))
            positions[board, ref] = case.bounds(solid)
    return result + list(motion_envelopes()), positions


def plug_shape(center_x, mate_y, center_z, count, along, pitch, ph):
    width = 3.8 + (count - 1) * pitch if ph else count * pitch + 0.35
    height = 4.45 if ph else 2.65
    protrusion = 4.15 if ph else 5.5
    xdim, zdim = (width, height) if along == "x" else (height, width)
    body = case.box(center_x - xdim / 2, mate_y, center_z - zdim / 2, xdim, protrusion, zdim)
    # Captive crimp openings and the shallow molded grip ledge are visible from above.
    holes = []
    pins = []
    for i in range(count):
        offset = pitch * (i - (count - 1) / 2)
        px, pz = (center_x + offset, center_z) if along == "x" else (center_x, center_z + offset)
        pins.append((px, mate_y + protrusion - 0.04, pz))
        holes.append(case.cylinder(px, mate_y + protrusion + 0.04, pz, 0.61, 0.62, (0, -1, 0)))
    if ph:
        ledge = case.box(center_x - xdim / 2 + 0.35, mate_y + 1.2, center_z + zdim / 2 - 0.05,
                         xdim - 0.7, 2.1, 0.34)
        body = case.fuse(body, ledge)
    return case.cut(body, *holes), pins


def cable_branch(group, reference, bounds, count, along, pitch, ph, route, rgb, pin_colors):
    left, _, low, right, mate, high = bounds
    x, z = (left + right) / 2, (low + high) / 2
    # Pin-header dimensions include the mating pins. Place the envelope at the pin tips.
    body, pins = plug_shape(x, mate + 0.015, z, count, along, pitch, ph)
    name = f"{reference} JST PHR-{count} housing" if ph else f"{reference} {pitch} mm mating housing envelope"
    out = [part(group, name, body, IVORY if ph else BLACK)]
    start_y = pins[0][1]
    merge_y = start_y + 6.6
    for i, (px, py, pz) in enumerate(pins):
        if count == 2:
            lateral, stagger = (i-0.5)*0.96, 0.0
        else:
            lateral = (i//2 - ((count+1)//2 - 1)/2) * 0.96
            stagger = (i%2-0.5)*0.96
        end_x, end_z = (x+lateral, z+stagger) if along == "x" else (x+stagger, z+lateral)
        wire = pipe([(px, py, pz), (px, py+1.5, pz), (end_x, merge_y-1.2, end_z),
                     (end_x, merge_y+0.35, end_z)], 0.45, 2.8)
        out.append(part(group, f"{reference} lead {i+1}", wire, pin_colors[i % len(pin_colors)]))
    first = (x, merge_y, z)
    trunk = pipe([first, *route(x, merge_y, z)], 0.68 + 0.145*count, 9.5)
    out.append(part(group, f"{reference} branch", trunk, rgb))
    return out


def jacket(group, label, points, radius):
    # The sleeve is an envelope of the split braid. The cable core is a separate solid.
    outer = pipe(points, radius, 14.0)
    inner = pipe(points, radius-0.64, 14.0)
    sleeve = case.cut(outer, inner)
    return [part(group, label + " split sleeve", sleeve, SLEEVE),
            part(group, label + " conductors", pipe(points, radius-0.69, 14.0), BLACK)]


def tool_harness(positions):
    color = [(105, 151, 168), (195, 188, 157), (187, 106, 67), (77, 86, 97)]
    # Higher branches follow staggered lanes above the spare J2 slot.
    top = [
        ("J13", 3, 120.5, 4.7, 99.3), ("J5", 4, 117.6, 3.3, 102.0),
        ("J4", 4, 114.7, 0.9, 103.0), ("J3", 4, 111.8, -1.7, 102.7),
        ("J19", 4, 109.0, -3.75, 100.95), ("J16", 2, 106.0, -4.9, 99.0),
        ("J17", 2, 103.2, -4.6, 96.9),
    ]
    out = []
    for ref, count, lane, dy, tz in top:
        def route(x, y, z):
            return [(x, max(lane-4.2, y+0.8), z+4.1), (x+4.5, lane, 95.1),
                    (139.4, lane, 96.0), (150.0, 94+dy, tz), (154.8, 94+dy, tz)]
        out += cable_branch(TOOLS, ref, positions["motion", ref], count, "x",
                            1.27 if ref == "J19" else 2.0, ref != "J19", route, TOOL, color)

    side = [
        ("J15", 5, 104.4, 127.9, 3.05, 96.9),
        ("J12", 6, 108.0, 131.8, 0.0, 97.2),
        ("J14", 4, 111.6, 135.5, -3.0, 94.9),
    ]
    for ref, count, lane, bend_x, dy, tz in side:
        def route(x, y, z):
            return [(x+4.5, max(lane-2.5, y+1), z+3), (bend_x, lane, z+9),
                    (143.0, lane, 88.8), (150.0, 94+dy, tz), (154.8, 94+dy, tz)]
        out += cable_branch(TOOLS, ref, positions["motion", ref], count, "z",
                            2.54 if ref == "J12" else 2.0, ref != "J12", route, TOOL, color)
    points = [(151.0, 94.0, 98.5), (182.0, 94.0, 98.5), (202.0, 89.0, 92.0),
              (222.0, 80.0, 83.0)]
    out += jacket(TOOLS, "1/2 inch tool", points, 6.99)
    out.append(tie(case.GATES[0], 98.5, 6.99))
    return out


def encoder_harness(positions):
    out = []
    palette = [(66, 145, 150), (172, 184, 189), (78, 113, 157), (187, 127, 76), (104, 126, 109), (71, 81, 95)]
    for ref, lane, dy, dz in (("J1", 169.5, 2.15, 1.2), ("J2", 163.5, 0.0, -1.95), ("J3", 158.0, -2.15, 1.0)):
        def route(x, y, z):
            return [(x, lane-2.4, z+2.1), (x+4.8, lane, z+6.0),
                    (111.5, lane, z+7.3), (126.5, lane, 67.5), (140, lane-3.2, 89.5),
                    (150.2, 148+dy, 99.5+dz), (154.4, 148+dy, 99.5+dz)]
        out += cable_branch(ENCODERS, ref, positions["encoder", ref], 6, "x", 2.0, True, route, ENC, palette)
    points = [(151.0, 148.0, 99.5), (182.0, 148.0, 99.5), (203.0, 152.0, 93.5),
              (222.0, 159.0, 83.0)]
    out += jacket(ENCODERS, "3/8 inch encoder", points, 5.40)
    out.append(tie(case.GATES[1], 99.5, 5.40))
    return out


def usb_plug(length):
    # Local +Z points into the receptacle. The long molded boot is sized to the
    # checked access envelope of the case, with a USB-C tongue envelope.
    plug = case.rounded_box(-6.15, -3.65, -length, 12.3, 7.3, length, 1.45)
    tongue = case.rounded_box(-4.16, -1.18, -0.02, 8.32, 2.36, 6.25, 0.94)
    ribs = [case.cylinder(0, 0, -length-i*1.3, 2.9-i*0.18, 0.65) for i in range(1, 5)]
    neck = BRepPrimAPI_MakeCone(gp_Ax2(gp_Pnt(0, 0, -length-6.2), gp_Dir(0, 0, 1)), 2.0, 3.2, 6.4).Shape()
    return case.fuse(plug, neck, *ribs), tongue


def service_leads():
    out = []
    # Host plug faces +Y. Motion plug faces +X and is rotated 90 degrees in the panel.
    boot, tongue = usb_plug(18.0)
    for name, solid, rgb in (("boot", boot, BLACK), ("tongue", tongue, METAL)):
        solid = case.rotate(solid, (1, 0, 0), -pi/2)
        out.append(part(SERVICE, "Host USB-C " + name, case.translate(solid, case.HOST_USB_X, 5.18, case.HOST_USB_Z), rgb))
    out.append(part(SERVICE, "Host USB-C lead", pipe([
        (case.HOST_USB_X, -18.6, case.HOST_USB_Z), (case.HOST_USB_X, -40, case.HOST_USB_Z),
        (case.HOST_USB_X-8, -59, 13.3), (case.HOST_USB_X-26, -77, 11.2)
    ], 1.9, 12), BLACK))

    boot, tongue = usb_plug(24.5)
    for name, solid, rgb in (("boot", boot, BLACK), ("tongue", tongue, METAL)):
        out.append(part(SERVICE, "Motion USB-C " + name, axis_x(solid, 20.47, case.MOTION_USB_Y, case.MOTION_USB_Z), rgb))
    out.append(part(SERVICE, "Motion USB-C lead", pipe([
        (-9.9, case.MOTION_USB_Y, case.MOTION_USB_Z), (-28, case.MOTION_USB_Y, case.MOTION_USB_Z),
        (-49, case.MOTION_USB_Y+8.0, 47), (-67, case.MOTION_USB_Y+19, 36)
    ], 1.9, 14), BLACK))

    y, z = case.DC_GLAND_Y, case.DC_GLAND_Z
    stem = case.cylinder(0, 0, -0.05, 5.99, 8.05)
    body = case.translate(hex_prism(8.5, 6.2), 0, 0, -6.15)
    cap = case.translate(hex_prism(8.0, 7.0), 0, 0, -14.8)
    collar = case.cylinder(0, 0, -10.0, 7.4, 4.6)
    shell = case.cut(case.fuse(stem, body, collar, cap), case.cylinder(0, 0, -15.0, 2.61, 23.3))
    gasket = case.cut(case.cylinder(0, 0, -0.58, 7.05, 0.58), case.cylinder(0, 0, -0.7, 5.98, 0.85))
    nut = case.cut(hex_prism(8.68, 3.6), case.cylinder(0, 0, -0.05, 5.96, 3.7))
    out += [
        part(SERVICE, "PMS12 BK080 gland body and cap", axis_x(shell, -0.58, y, z), (61, 67, 74)),
        part(SERVICE, "PMS12 BK080 panel gasket", axis_x(gasket, 0.0, y, z), BLACK),
        part(SERVICE, "PMS12 BK080 locknut", axis_x(nut, case.WALL, y, z), (72, 81, 89)),
        part(SERVICE, "24 V jacketed lead", pipe([(8.45, y, z), (-29, y, z), (-49, y-7.5, 20),
                                                 (-69, y-19.5, 14.6)], 2.60, 14), BLACK),
    ]
    for target_y, color in ((61.24, (175, 70, 52)), (56.16, (46, 53, 62))):
        out.append(part(SERVICE, f"J4 terminal lead at {target_y:.2f}", pipe([
            (8.25, y+(1.03 if target_y > 60 else -1.03), z), (10.1, y+3.8, z),
            (11.5, target_y-3.8, z-1.6), (11.5, target_y, z-2.4),
            (15.71, target_y, z-2.4)
        ], 0.78, 4.0), color))
    return out


def build_scene(board_folder):
    palette = {"01-base": (54, 68, 82), "02-lid": (66, 82, 98),
               "03-tools-gate": (192, 117, 61), "04-encoder-gate": (62, 137, 158)}
    printed = [part(CASE, name, shape, palette.get(name, (86, 107, 126)))
               for name, shape in case.build_parts().items()]
    boards, positions = pcb_parts(board_folder)
    return printed + metal_fasteners() + boards + tool_harness(positions) + encoder_harness(positions) + service_leads()


def write_step(path, parts):
    ext = TCollection_ExtendedString
    doc = TDocStd_Document(ext("FAB Computer wired enclosure"))
    tool = XCAFDoc_DocumentTool.ShapeTool_s(doc.Main())
    colors = XCAFDoc_DocumentTool.ColorTool_s(doc.Main())
    root = tool.NewShape()
    groups = {}
    masters = {}
    TDataStd_Name.Set_s(root, ext("FAB Computer wired enclosure"))
    for item in parts:
        if item.group not in groups:
            group = tool.NewShape()
            TDataStd_Name.Set_s(group, ext(item.group))
            tool.AddComponent(root, group, TopLoc_Location())
            groups[item.group] = group
        origin_solid = item.solid.Located(TopLoc_Location())
        key = (origin_solid, item.rgb)
        if key not in masters:
            label = tool.AddShape(origin_solid, False)
            TDataStd_Name.Set_s(label, ext(item.name))
            rgb = tuple(value / 255.0 for value in item.rgb)
            colors.SetColor(label, Quantity_Color(*rgb, Quantity_TOC_RGB), XCAFDoc_ColorGen)
            masters[key] = label
        instance = tool.AddComponent(groups[item.group], masters[key], item.solid.Location())
        TDataStd_Name.Set_s(instance, ext(item.name))
    tool.UpdateAssemblies()
    writer = STEPCAFControl_Writer()
    Interface_Static.SetIVal_s("write.surfacecurve.mode", 0)
    writer.SetNameMode(True)
    writer.SetColorMode(True)
    if not writer.Transfer(doc, STEPControl_AsIs) or writer.Write(str(path)) != IFSelect_RetDone:
        raise RuntimeError("Wired STEP assembly export failed")


def main():
    parser = argparse.ArgumentParser(description=__doc__)
    parser.add_argument("output", type=Path)
    parser.add_argument("--pcb-steps", type=Path, required=True)
    parser.add_argument("--kicad-cli", default="kicad-cli")
    args = parser.parse_args()
    args.output.mkdir(parents=True, exist_ok=True)
    use_step_exports(args.pcb_steps, args.kicad_cli)
    scene = build_scene(args.pcb_steps)
    print(f"Writing {len(scene)} named CAD shapes")
    write_step(args.output / "FAB-Computer-Wired.step", scene)


if __name__ == "__main__":
    main()
