"""Parametric FAB Computer enclosure, in millimetres.

Install cadquery-ocp in Python 3.12 or run in an OCP-enabled environment.
Run this file with an output directory to build the STEP and print-oriented STLs.
Datum: front-left outside corner of the base. +Y points toward host slot J3.
"""
from dataclasses import dataclass
from math import hypot, pi
from pathlib import Path
import argparse

from OCP.Bnd import Bnd_Box
from OCP.BRepAlgoAPI import BRepAlgoAPI_Cut, BRepAlgoAPI_Fuse
from OCP.BRepBndLib import BRepBndLib
from OCP.BRepBuilderAPI import BRepBuilderAPI_MakeFace, BRepBuilderAPI_MakePolygon, BRepBuilderAPI_Transform
from OCP.BRepCheck import BRepCheck_Analyzer
from OCP.BRepFilletAPI import BRepFilletAPI_MakeFillet
from OCP.BRepGProp import BRepGProp
from OCP.BRepMesh import BRepMesh_IncrementalMesh
from OCP.BRepPrimAPI import BRepPrimAPI_MakeBox, BRepPrimAPI_MakeCone, BRepPrimAPI_MakeCylinder, BRepPrimAPI_MakePrism
from OCP.GProp import GProp_GProps
from OCP.gp import gp_Ax1, gp_Ax2, gp_Dir, gp_Pnt, gp_Trsf, gp_Vec
from OCP.IFSelect import IFSelect_RetDone
from OCP.Quantity import Quantity_Color, Quantity_TOC_RGB
from OCP.STEPCAFControl import STEPCAFControl_Writer
from OCP.STEPControl import STEPControl_AsIs
from OCP.StlAPI import StlAPI_Writer
from OCP.TCollection import TCollection_ExtendedString
from OCP.TDataStd import TDataStd_Name
from OCP.TDocStd import TDocStd_Document
from OCP.TopAbs import TopAbs_EDGE, TopAbs_SOLID
from OCP.TopExp import TopExp_Explorer
from OCP.TopLoc import TopLoc_Location
from OCP.TopTools import TopTools_ListOfShape
from OCP.TopoDS import TopoDS
from OCP.XCAFDoc import XCAFDoc_ColorGen, XCAFDoc_DocumentTool

# Case shell and fit.
WIDTH, DEPTH = 166.0, 186.0
BODY_HEIGHT, LID_THICKNESS = 108.0, 4.0
WALL, FLOOR, OUTER_RADIUS = 3.2, 3.6, 4.5
BOARD_BOTTOM = 13.0
BOARD_THICKNESS = 1.6
INSERT_DIA, INSERT_DEPTH = 4.1, 6.3
SCREW_CLEARANCE = 3.4
CARD_GROOVE = 2.65
CARD_TOP_GAP = 0.65
DC_GLAND_DIA = 12.5
EPS = 0.05

# Backplane location, taken from the matching KiCad Edge.Cuts and H1-H4.
# Board envelope 111.5 x 154.0. The H1-H4 bolt pattern is 103.5 x 146.0.
HOST = (15.0, 5.2, BOARD_BOTTOM)
H1_H4 = [(HOST[0] + x, HOST[1] + y) for x in (4.0, 107.5) for y in (4.0, 150.0)]
LID_SCREWS = [(x, y) for x in (7.2, WIDTH - 7.2) for y in (7.2, DEPTH - 7.2)]

# KiCad user origin is the row A pin 1 of each daughtercard. The repository
# places the fitted card at (0, -2.01, 17.74) relative to the host A1 datum.
CARD_A1_X = HOST[0] + 16.5
CARD_A1_Z = BOARD_BOTTOM + BOARD_THICKNESS + 17.74
MOTION_Y = HOST[1] + 79.0 - 2.01
ENCODER_Y = HOST[1] + 131.0 - 2.01
MOTION_Z = CARD_A1_Z + 54.92
ENCODER_Z = CARD_A1_Z + 20.92

HOST_USB_X, HOST_USB_Z = HOST[0] + 69.6, BOARD_BOTTOM + 3.15
MOTION_USB_Y, MOTION_USB_Z = MOTION_Y + 1.2, CARD_A1_Z + 20.92
DC_GLAND_Y, DC_GLAND_Z = 46.5, 23.4

GATE_WINDOW = 34.0
GATE_FLANGE = 47.0
GATE_RECESS = 2.8
GATE_BOTTOM = 82.0
GATE_SCREW_Z, GATE_SCREW_SPAN = 90.0, 40.6


@dataclass(frozen=True)
class Gate:
    name: str
    y: float
    bundle: float
    notch_bottom: float
    tie_top: float


GATES = [
    Gate("03-tools-gate", 94.0, 17.0, 90.0, 90.8),
    Gate("04-encoder-gate", 148.0, 13.0, 93.0, 93.7),
]


@dataclass(frozen=True)
class Keeper:
    name: str
    face_y: float
    top_z: float
    card_edge: float
    anchor_x: float
    anchor_y: float
    inward: int

    @property
    def deck_z(self):
        return self.top_z + CARD_TOP_GAP


KEEPERS = [
    Keeper("05-motion-keeper-left", MOTION_Y, MOTION_Z, CARD_A1_X - 10.63, 8.75, 103.0, 1),
    Keeper("06-motion-keeper-right", MOTION_Y, MOTION_Z, CARD_A1_X + 89.37, 133.3, 69.0, -1),
    Keeper("07-encoder-keeper-left", ENCODER_Y, ENCODER_Z, CARD_A1_X - 10.0, 8.75, 145.0, 1),
    Keeper("08-encoder-keeper-right", ENCODER_Y, ENCODER_Z, CARD_A1_X + 90.0, 133.3, 123.0, -1),
]


def box(x, y, z, dx, dy, dz):
    return BRepPrimAPI_MakeBox(gp_Pnt(x, y, z), dx, dy, dz).Shape()


def cylinder(x, y, z, radius, length, direction=(0, 0, 1)):
    return BRepPrimAPI_MakeCylinder(
        gp_Ax2(gp_Pnt(x, y, z), gp_Dir(*direction)), radius, length
    ).Shape()


def prism(points, vector):
    profile = BRepBuilderAPI_MakePolygon()
    for point in points:
        profile.Add(gp_Pnt(*point))
    profile.Close()
    return BRepPrimAPI_MakePrism(BRepBuilderAPI_MakeFace(profile.Wire()).Face(), gp_Vec(*vector)).Shape()


def bounds(shape):
    extent = Bnd_Box()
    BRepBndLib.AddOptimal_s(shape, extent, False, False)
    return extent.Get()


def volume(shape):
    props = GProp_GProps()
    BRepGProp.VolumeProperties_s(shape, props)
    return props.Mass()


def shapes_of_type(shape, kind):
    explorer = TopExp_Explorer(shape, kind)
    while explorer.More():
        yield explorer.Current()
        explorer.Next()


def boolean(operator, base, tools):
    if not tools:
        return base
    args = TopTools_ListOfShape()
    args.Append(base)
    operands = TopTools_ListOfShape()
    for tool in tools:
        operands.Append(tool)
    operation = operator()
    operation.SetArguments(args)
    operation.SetTools(operands)
    operation.SetNonDestructive(True)
    operation.SetFuzzyValue(1e-6)
    operation.Build()
    if not operation.IsDone():
        raise RuntimeError(f"Boolean failed ({operator.__name__})")
    return operation.Shape()


def fuse(base, *tools):
    return boolean(BRepAlgoAPI_Fuse, base, tools)


def cut(base, *tools):
    return boolean(BRepAlgoAPI_Cut, base, tools)


def rounded_box(x, y, z, dx, dy, dz, radius):
    body = box(x, y, z, dx, dy, dz)
    fillet = BRepFilletAPI_MakeFillet(body)
    for edge in shapes_of_type(body, TopAbs_EDGE):
        a, b, c, d, e, f = bounds(edge)
        if d - a < 1e-6 and e - b < 1e-6 and f - c > 1:
            cast_edge = getattr(TopoDS, "Edge_s", None) or TopoDS.Edge
            fillet.Add(radius, cast_edge(edge))
    fillet.Build()
    if not fillet.IsDone():
        raise RuntimeError("Could not round the enclosure corners")
    return fillet.Shape()


def insert_cutters(x, y, z, axis=(0, 0, -1)):
    start = tuple(coord - EPS * normal for coord, normal in zip((x, y, z), axis))
    bore = cylinder(*start, INSERT_DIA / 2, INSERT_DEPTH + EPS, axis)
    lead = BRepPrimAPI_MakeCone(
        gp_Ax2(gp_Pnt(*start), gp_Dir(*axis)), INSERT_DIA / 2 + 0.34,
        INSERT_DIA / 2, 0.7 + EPS
    ).Shape()
    return bore, lead


def port_profile(center, z, width, below, above, roof_width):
    """A printable 45 degree roof over the plug clearance rectangle."""
    left, right = center - width / 2, center + width / 2
    shoulder = z + above
    peak = shoulder + (width - roof_width) / 2
    return [(left, z - below), (right, z - below), (right, shoulder),
            (center + roof_width / 2, peak), (center - roof_width / 2, peak), (left, shoulder)]


def right_wall_ramp(y, z, width, reach):
    inner = WIDTH - WALL
    return prism([(inner + EPS, y, z - reach - EPS), (inner + EPS, y, z + EPS),
                  (inner - reach, y, z + EPS), (inner - reach, y, z)],
                 (0, width, 0))


def gate_tie_support(gate):
    """A 45 degree heel puts the tie just below the horizontal bundle."""
    x = WIDTH - WALL
    y = gate.y - 7.0
    top = gate.tie_top
    return prism([(x + EPS, y, 72.0), (x + EPS, y, GATE_BOTTOM - 0.3),
                  (x - 0.85, y, GATE_BOTTOM - 0.3), (x - 0.85, y, top),
                  (x - 11.0, y, top), (x - 11.0, y, 83.1)],
                 (0, 14.0, 0))


def make_base():
    outer = rounded_box(0, 0, 0, WIDTH, DEPTH, BODY_HEIGHT, OUTER_RADIUS)
    inner = rounded_box(WALL, WALL, FLOOR, WIDTH - 2 * WALL, DEPTH - 2 * WALL,
                        BODY_HEIGHT - FLOOR + EPS, 1.5)
    shell = cut(outer, inner)
    supports = [
        cylinder(x, y, FLOOR - EPS, 4.4, BOARD_BOTTOM - FLOOR + EPS)
        for x, y in H1_H4
    ]
    supports += [
        cylinder(x, y, FLOOR - EPS, 4.7, BODY_HEIGHT - FLOOR + EPS)
        for x, y in LID_SCREWS
    ]
    openings = []
    for x, y in H1_H4:
        openings.extend(insert_cutters(x, y, BOARD_BOTTOM))
    for x, y in LID_SCREWS:
        openings.extend(insert_cutters(x, y, BODY_HEIGHT))

    for k in KEEPERS:
        supports.append(box(k.anchor_x - 5.85, k.anchor_y - 7.3, FLOOR - EPS,
                            11.7, 14.6, k.deck_z - FLOOR + EPS))
        # The small locating pin prevents the keeper from turning with the screw.
        supports.append(cylinder(k.anchor_x, k.anchor_y + 4.6, k.deck_z - EPS, 1.0, 1.55))
        openings.extend(insert_cutters(k.anchor_x, k.anchor_y, k.deck_z))

    for gate in GATES:
        lower = GATE_BOTTOM - 0.2
        openings.append(box(WIDTH - WALL - 0.2, gate.y - GATE_WINDOW / 2, GATE_BOTTOM,
                            WALL + 0.4, GATE_WINDOW, BODY_HEIGHT - GATE_BOTTOM + EPS))
        openings.append(box(WIDTH - GATE_RECESS, gate.y - GATE_FLANGE / 2, lower,
                            GATE_RECESS + EPS, GATE_FLANGE, BODY_HEIGHT - lower + EPS))
        for y in (gate.y - GATE_SCREW_SPAN / 2, gate.y + GATE_SCREW_SPAN / 2):
            # Backing lug gives the side-facing insert a full 6.3 mm of engagement.
            supports.append(box(WIDTH - 11.2, y - 3.05, 78.0, 8.05, 6.1, 22.0))
            supports.append(right_wall_ramp(y - 3.05, 78.0, 6.1, 8.0))
            openings.extend(insert_cutters(WIDTH - GATE_RECESS, y, GATE_SCREW_Z, (-1, 0, 0)))
        supports.append(gate_tie_support(gate))
        openings.append(box(WIDTH - WALL - 8.8, gate.y - 7.1, gate.tie_top - 5.0,
                            4.3, 14.2, 3.15))

    for wall_y in (-EPS, DEPTH - WALL - EPS):
        for x in (20, 26, 49, 55, 61, 67, 104, 110, 116, 122, 128, 134, 140, 146):
            openings.append(box(x - 1.5, wall_y, 8.8, 3.0, WALL + 2 * EPS, 12.0))

    front_usb = port_profile(HOST_USB_X, HOST_USB_Z, 17.0, 5.0, 4.8, 6.0)
    openings.append(prism([(x, -EPS, z) for x, z in front_usb], (0, WALL + 2 * EPS, 0)))
    motion_usb = port_profile(MOTION_USB_Y, MOTION_USB_Z, 29.0, 10.5, 6.0, 8.0)
    openings.append(prism([(-EPS, y, z) for y, z in motion_usb], (WALL + 2 * EPS, 0, 0)))
    openings.append(cylinder(-EPS, DC_GLAND_Y, DC_GLAND_Z, DC_GLAND_DIA / 2, WALL + 2 * EPS, (1, 0, 0)))
    return cut(fuse(shell, *supports), *openings)


def make_lid():
    lid = rounded_box(0, 0, BODY_HEIGHT, WIDTH, DEPTH, LID_THICKNESS, OUTER_RADIUS)
    tab_z = BODY_HEIGHT - 2.0
    tabs = [
        box(42, WALL + 0.4, tab_z, 30, 1.9, 2.05),
        box(94, DEPTH - WALL - 2.3, tab_z, 30, 1.9, 2.05),
        box(WALL + 0.4, 32, tab_z, 1.9, 23, 2.05),
        box(WALL + 0.4, 121, tab_z, 1.9, 19, 2.05),
        box(WIDTH - WALL - 2.3, 32, tab_z, 1.9, 23, 2.05),
    ]
    openings = []
    for x, y in LID_SCREWS:
        openings.append(cylinder(x, y, BODY_HEIGHT - EPS, SCREW_CLEARANCE / 2, LID_THICKNESS + 2 * EPS))
        openings.append(cylinder(x, y, BODY_HEIGHT + LID_THICKNESS - 1.25, 3.35, 1.25 + EPS))
    for y in (28, 34, 40, 46, 78, 84, 90, 96, 134, 140, 146, 152):
        for x in (42.5, 82.5, 122.5):
            r, half = 1.6, 13.4
            z, h = BODY_HEIGHT - EPS, LID_THICKNESS + 2 * EPS
            openings.append(fuse(box(x - half, y - r, z, 2 * half, 2 * r, h),
                                 cylinder(x - half, y, z, r, h),
                                 cylinder(x + half, y, z, r, h)))
    return cut(fuse(lid, *tabs), *openings)


def make_gate(gate):
    low, high = GATE_BOTTOM + 0.27, BODY_HEIGHT - 0.20
    flange = box(WIDTH - GATE_RECESS, gate.y - GATE_FLANGE / 2 + 0.26, low,
                 GATE_RECESS, GATE_FLANGE - 0.52, high - low)
    plug = box(WIDTH - WALL, gate.y - GATE_WINDOW / 2 + 0.29, low,
               WALL, GATE_WINDOW - 0.58, high - low)
    center_z = gate.notch_bottom + gate.bundle / 2
    notch = [
        cylinder(WIDTH - WALL - EPS, gate.y, center_z, gate.bundle / 2, WALL + 2 * EPS, (1, 0, 0)),
        box(WIDTH - WALL - EPS, gate.y - gate.bundle / 2, center_z,
            WALL + 2 * EPS, gate.bundle, BODY_HEIGHT - center_z + EPS),
    ]
    for y in (gate.y - GATE_SCREW_SPAN / 2, gate.y + GATE_SCREW_SPAN / 2):
        notch.append(cylinder(WIDTH - GATE_RECESS - EPS, y, GATE_SCREW_Z,
                              SCREW_CLEARANCE / 2, GATE_RECESS + 2 * EPS, (1, 0, 0)))
    return cut(fuse(flange, plug), *notch)


def make_keeper(k):
    ax, ay, z = k.anchor_x, k.anchor_y, k.deck_z
    center_y = k.face_y - BOARD_THICKNESS / 2
    tx = k.card_edge + k.inward * 2.7
    dx, dy = tx - ax, center_y - ay
    reach = hypot(dx, dy)
    across_x, across_y = -dy / reach * 4.8, dx / reach * 4.8
    arm = prism([(ax + across_x, ay + across_y, z), (ax - across_x, ay - across_y, z),
                 (tx - across_x, center_y - across_y, z), (tx + across_x, center_y + across_y, z)],
                (0, 0, 4.0))
    x_min = min(k.card_edge - k.inward * 1.15, k.card_edge + k.inward * 4.15)
    cap = box(x_min, center_y - 4.0, z, 5.3, 8.0, 4.0)
    jaw_z = k.top_z - 2.5
    jaws = [
        box(x_min, y, jaw_z, 5.3, 1.65, z - jaw_z + EPS)
        for y in (center_y - CARD_GROOVE / 2 - 1.65, center_y + CARD_GROOVE / 2)
    ]
    keeper = fuse(cylinder(ax, ay, z, 6.45, 4.0), arm, cap, *jaws)
    clearances = [
        cylinder(ax, ay, z - EPS, SCREW_CLEARANCE / 2, 4.0 + 2 * EPS),
        cylinder(ax, ay + 4.6, z - EPS, 1.25, 1.9),
    ]
    if k.inward > 0:
        clearances.append(box(-1, ay - 15, jaw_z - EPS, WALL + 1.4, 30, 9))
    return cut(keeper, *clearances)


def translate(shape, dx, dy, dz):
    transform = gp_Trsf()
    transform.SetTranslation(gp_Vec(dx, dy, dz))
    return BRepBuilderAPI_Transform(shape, transform, True).Shape()


def rotate(shape, axis, angle):
    transform = gp_Trsf()
    transform.SetRotation(gp_Ax1(gp_Pnt(0, 0, 0), gp_Dir(*axis)), angle)
    return BRepBuilderAPI_Transform(shape, transform, True).Shape()


def build_parts():
    return {
        "01-base": make_base(),
        "02-lid": make_lid(),
        **{gate.name: make_gate(gate) for gate in GATES},
        **{keeper.name: make_keeper(keeper) for keeper in KEEPERS},
    }


COLORS = {
    "01-base": (0.23, 0.27, 0.31),
    "02-lid": (0.35, 0.40, 0.45),
    "03-tools-gate": (0.78, 0.45, 0.18),
    "04-encoder-gate": (0.26, 0.54, 0.65),
}


def write_assembly(path, parts):
    doc = TDocStd_Document(TCollection_ExtendedString("FAB Computer Enclosure"))
    tool = XCAFDoc_DocumentTool.ShapeTool_s(doc.Main())
    colors = XCAFDoc_DocumentTool.ColorTool_s(doc.Main())
    assembly = tool.NewShape()
    TDataStd_Name.Set_s(assembly, TCollection_ExtendedString("FAB Computer Enclosure"))
    for name, shape in parts.items():
        label = tool.AddShape(shape, False)
        TDataStd_Name.Set_s(label, TCollection_ExtendedString(name))
        rgb = COLORS.get(name, (0.29, 0.32, 0.35))
        colors.SetColor(label, Quantity_Color(*rgb, Quantity_TOC_RGB), XCAFDoc_ColorGen)
        tool.AddComponent(assembly, label, TopLoc_Location())
    tool.UpdateAssemblies()
    writer = STEPCAFControl_Writer()
    writer.SetNameMode(True)
    writer.SetColorMode(True)
    if not writer.Transfer(doc, STEPControl_AsIs) or writer.Write(str(path)) != IFSelect_RetDone:
        raise RuntimeError("STEP assembly export failed")


def print_oriented(name, shape):
    if name in {"03-tools-gate", "04-encoder-gate"}:
        shape = rotate(shape, (0, 1, 0), pi / 2)
    elif name != "01-base":
        shape = rotate(shape, (1, 0, 0), pi)
    x, y, z, *_ = bounds(shape)
    return translate(shape, -x, -y, -z)


def main():
    parser = argparse.ArgumentParser(description=__doc__)
    parser.add_argument("output", type=Path)
    args = parser.parse_args()
    folder = args.output
    (folder / "STL").mkdir(parents=True, exist_ok=True)
    parts = build_parts()
    for name, shape in parts.items():
        if not BRepCheck_Analyzer(shape).IsValid() or len(list(shapes_of_type(shape, TopAbs_SOLID))) != 1:
            raise RuntimeError(f"{name} should be one valid solid")
        printable = print_oriented(name, shape)
        BRepMesh_IncrementalMesh(printable, 0.055, False, 0.12, True)
        stl = StlAPI_Writer()
        stl.ASCIIMode = False
        if not stl.Write(printable, str(folder / "STL" / f"{name}.stl")):
            raise RuntimeError(f"STL export failed for {name}")
        print(f"{name:<25} {volume(shape) / 1000:6.1f} cm^3  {tuple(round(n, 2) for n in bounds(printable)[3:])}")
    write_assembly(folder / "FAB-Computer-Enclosure.step", parts)


if __name__ == "__main__":
    main()
