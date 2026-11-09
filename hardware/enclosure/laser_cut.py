"""Generate the flat-panel FAB Computer case, 1:1 DXF/SVG cuts, and STEP."""
from dataclasses import dataclass, field
from math import cos, pi, sin
from pathlib import Path
import argparse

from OCP.TopLoc import TopLoc_Location

import build_enclosure as printed
import build_wired_assembly as wired

LEFT, RIGHT, DEPTH, DECK = -2.0, 166.0, 186.0, 108.0
WIDTH = RIGHT - LEFT
SCREW = 3.5
X, Y, Z = (1, 0, 0), (0, 1, 0), (0, 0, 1)
NX, NY, NZ = (-1, 0, 0), (0, -1, 0), (0, 0, -1)
PANEL = "Laser-cut panels"
BLOCKS = "12 mm M3 blocks and board standoffs"
SCREWS = "Panel and board fasteners"
PADS = "Feet"


@dataclass(frozen=True)
class Circle:
    x: float
    y: float
    diameter: float


def rect(w, h):
    return [(0, 0), (w, 0), (w, h), (0, h)]


def arc(cx, cy, r, start, stop, segments=18):
    return [(cx+r*cos(start+(stop-start)*i/segments), cy+r*sin(start+(stop-start)*i/segments))
            for i in range(segments+1)]


def slot(x, y, length, height):
    r = height / 2
    half = length / 2 - r
    return arc(x+half, y, r, -pi/2, pi/2) + arc(x-half, y, r, pi/2, 3*pi/2)


@dataclass
class Plate:
    name: str
    width: float
    height: float
    origin: tuple
    u: tuple = X
    v: tuple = Y
    normal: tuple = Z
    outline: list = field(default_factory=list)
    holes: list = field(default_factory=list)

    def __post_init__(self):
        self.outline = self.outline or rect(self.width, self.height)

    def bore(self, xyz, diameter=SCREW):
        d = wired.sub(xyz, self.origin)
        self.holes.append(Circle(wired.dot(d, self.u), wired.dot(d, self.v), diameter))

    def point(self, u, v, n=0):
        return wired.add(self.origin, wired.add(wired.times(self.u, u),
                         wired.add(wired.times(self.v, v), wired.times(self.normal, n))))

    def solid(self, thick):
        solid = printed.prism([self.point(*p) for p in self.outline], wired.times(self.normal, thick))
        cutters = []
        for shape in self.holes:
            if isinstance(shape, Circle):
                cutters.append(printed.cylinder(*self.point(shape.x, shape.y, -0.05),
                               shape.diameter/2, thick+0.1, self.normal))
            else:
                cutters.append(printed.prism([self.point(*p, -0.05) for p in shape],
                               wired.times(self.normal, thick+0.1)))
        return printed.cut(solid, *cutters)


@dataclass(frozen=True)
class Bolt:
    name: str
    xyz: tuple
    out: tuple
    length: int = 6


@dataclass(frozen=True)
class Block:
    name: str
    center: tuple


def kit(t):
    if not 2.8 <= t <= 3.25:
        raise ValueError("Use measured stock between 2.8 and 3.25 mm.")
    dz = t-3
    floor = Plate("01-floor", WIDTH, DEPTH, (LEFT, 0, 0))
    lid = Plate("02-vented-lid", WIDTH, DEPTH, (LEFT, 0, DECK))
    left = Plate("03-left-service-wall", DEPTH, DECK-t, (LEFT, 0, t), Y, Z, X)
    right = Plate("04-right-harness-wall", DEPTH, DECK-t, (RIGHT-t, 0, t), Y, Z, X)
    end_x = LEFT+t+0.15
    end_w = WIDTH-2*t-0.30
    front = Plate("05-front-wall", end_w, DECK-t, (end_x, 0, t), X, Z, Y)
    back = Plate("06-back-wall", end_w, DECK-t, (end_x, DEPTH-t, t), X, Z, Y)
    plates = [floor, lid, left, right, front, back]
    cubes, bolts = [], []
    left_x, right_x = LEFT+t+6, RIGHT-t-6

    def attach(name, plate, point, outward, length=6):
        plate.bore(point)
        bolts.append(Bolt(name, point, outward, length))

    for x, side, side_x, out_x in ((left_x, left, LEFT, NX), (right_x, right, RIGHT, X)):
        for y, end, end_y, out_y in ((t+6, front, 0, NY), (DEPTH-t-6, back, DEPTH, Y)):
            for label, z, horizontal, face, out_z in (
                ("floor", t+6, floor, 0, NZ), ("lid", DECK-6, lid, DECK+t, Z),
            ):
                cubes.append(Block(label, (x, y, z)))
                attach(label, side, (side_x, y, z), out_x)
                attach(label, end, (x, end_y, z), out_y)
                attach(label, horizontal, (x, y, face), out_z)

    for x, y in printed.H1_H4:
        attach("backplane", floor, (x, y, 0), NZ)
        bolts.append(Bolt("backplane", (x, y, 14.6+dz), Z))

    for y in (28, 34, 40, 46, 78, 84, 90, 96, 134, 140, 146, 152):
        for x in (42.5, 82.5, 122.5):
            lid.holes.append(slot(x-LEFT, y, 30, 3.2))
    for panel in (front, back):
        for x in (20, 26, 49, 55, 61, 67, 104, 110, 116, 122, 128, 134, 140, 146):
            panel.holes.append([(x-end_x-b, 14.8-t+a) for a, b in slot(0, 0, 12, 3)])
    front.holes.append(slot(printed.HOST_USB_X-end_x, printed.HOST_USB_Z+dz-t, 17, 9.8))
    left.holes.append(slot(printed.MOTION_USB_Y, printed.MOTION_USB_Z+dz-t, 32, 23))
    left.holes.append(Circle(printed.DC_GLAND_Y, printed.DC_GLAND_Z+dz-t, 12.5))

    # An open-top window behind each external overlay passes pre-crimped plugs.
    opening_low = 82-t
    outline = [(0, 0), (DEPTH, 0), (DEPTH, DECK-t)]
    for gate in reversed(printed.GATES):
        a, b = gate.y-17, gate.y+17
        outline += [(b, DECK-t), (b, opening_low), (a, opening_low), (a, DECK-t)]
    right.outline = outline + [(0, DECK-t)]

    gates, shelves = [], []
    for label, gate in zip(("tool", "encoder"), printed.GATES):
        z0, w = 74.0+dz, 50.4
        h = DECK-z0-0.2
        radius = gate.bundle/2
        notch_z = gate.notch_bottom+dz-z0
        contour = [(0, 0), (w, 0), (w, h), (w/2+radius, h)]
        contour += arc(w/2, notch_z+radius, radius, 0, -pi)
        contour += [(w/2-radius, h), (0, h)]
        overlay = Plate(f"07-{label}-gate" if label == "tool" else "08-encoder-gate",
                        w, h, (RIGHT, gate.y-w/2, z0), Y, Z, X, contour)
        shelf_top = gate.tie_top+dz
        shelf = Plate(f"11-{label}-tie-shelf" if label == "tool" else "12-encoder-tie-shelf",
                      11.4, 52.4, (RIGHT-t-11.4, gate.y-26.2, shelf_top-t))
        for y in (gate.y-20.5, gate.y+20.5):
            center_z = shelf_top-t-6
            cubes.append(Block(f"{label} shelf", (right_x, y, center_z)))
            right.bore((RIGHT, y, center_z))
            attach(f"{label} gate", overlay, (RIGHT+t, y, center_z), X, 10)
            attach(f"{label} shelf", shelf, (right_x, y, shelf_top), Z)
        # The tie passes up through both slots and closes around the bundle.
        for y in (26.2-(radius+1.0), 26.2+(radius+1.0)):
            shelf.holes.append(slot(6.0, y, 4.3, 2.4))
        gates.append(overlay)
        shelves.append(shelf)

    keepers = []
    for name, face, height, bolt_y in (
        ("09-motion-keeper", printed.MOTION_Y, printed.MOTION_Z, 60.5),
        ("10-encoder-keeper", printed.ENCODER_Y, printed.ENCODER_Z, 121.0),
    ):
        bar_z = height+dz+0.80
        lo_y = bolt_y-5.7
        bar_y = face-0.8-4.2
        bar_w = WIDTH-2*t-0.70
        bar_h = bar_y+8.4-lo_y
        delta = bar_y-lo_y
        contour = [(0, 0), (17, 0), (30, delta), (bar_w-30, delta), (bar_w-17, 0),
                   (bar_w, 0), (bar_w, bar_h), (0, bar_h)]
        if name == "09-motion-keeper":
            # The right ear turns forward before it enters the tie shelf footprint.
            contour = [(0, 0), (17, 0), (30, delta), (bar_w-27, delta), (bar_w-12, 0),
                       (bar_w, 0), (bar_w, 10.7), (bar_w-12, 10.7), (bar_w-19, bar_h), (0, bar_h)]
        keeper = Plate(name, bar_w, bar_h, (LEFT+t+0.35, lo_y, bar_z), outline=contour)
        for x, panel, wall, out in ((left_x, left, LEFT, NX), (right_x, right, RIGHT, X)):
            cubes.append(Block(name, (x, bolt_y, bar_z-6)))
            attach(name, panel, (wall, bolt_y, bar_z-6), out)
            attach(name, keeper, (x, bolt_y, bar_z+t), Z)
        keepers.append(keeper)
    return plates + gates + keepers + shelves, cubes, bolts


def paths(plate):
    yield from plate.holes
    yield plate.outline


def svg(file, layout, w, h):
    items = []
    for plate, dx, dy in layout:
        for shape in paths(plate):
            if isinstance(shape, Circle):
                items.append(f'<circle cx="{dx+shape.x:.4f}" cy="{h-dy-shape.y:.4f}" r="{shape.diameter/2:.4f}"/>')
            else:
                points = " ".join(f"{dx+x:.4f},{h-dy-y:.4f}" for x, y in shape)
                items.append(f'<polygon points="{points}"/>')
    file.write_text(
        f'<svg xmlns="http://www.w3.org/2000/svg" width="{w}mm" height="{h}mm" viewBox="0 0 {w} {h}">\n'
        '<g id="CUT" fill="none" stroke="#ff0000" stroke-width="0.05">\n'
        + "\n".join(items) + "\n</g>\n</svg>\n", encoding="utf-8")


def dxf(file, layout):
    pairs = [(0, "SECTION"), (2, "HEADER"), (9, "$ACADVER"), (1, "AC1015"),
             (9, "$INSUNITS"), (70, 4), (0, "ENDSEC"), (0, "SECTION"), (2, "TABLES"),
             (0, "TABLE"), (2, "LAYER"), (70, 1), (0, "LAYER"), (100, "AcDbSymbolTableRecord"),
             (100, "AcDbLayerTableRecord"), (2, "CUT"), (70, 0), (62, 1), (6, "CONTINUOUS"),
             (0, "ENDTAB"), (0, "ENDSEC"), (0, "SECTION"), (2, "ENTITIES")]
    for plate, dx, dy in layout:
        for shape in paths(plate):
            if isinstance(shape, Circle):
                pairs += [(0, "CIRCLE"), (100, "AcDbEntity"), (8, "CUT"), (100, "AcDbCircle"),
                          (10, f"{dx+shape.x:.4f}"), (20, f"{dy+shape.y:.4f}"), (30, 0),
                          (40, f"{shape.diameter/2:.4f}")]
            else:
                pairs += [(0, "LWPOLYLINE"), (100, "AcDbEntity"), (8, "CUT"),
                          (100, "AcDbPolyline"), (90, len(shape)), (70, 1)]
                for x, y in shape:
                    pairs += [(10, f"{dx+x:.4f}"), (20, f"{dy+y:.4f}")]
    pairs += [(0, "ENDSEC"), (0, "EOF")]
    file.write_text("".join(f"{key}\n{value}\n" for key, value in pairs), encoding="ascii")


def cut_files(folder, plates):
    folder.mkdir(parents=True, exist_ok=True)
    coupon = Plate("13-fit-coupon", 62, 27, (0, 0, 0), holes=[
        Circle(8, 8, 3.5), Circle(19, 8, 3.5), Circle(36, 11, 12.5),
        Circle(52, 8, 3.5), slot(17, 20, 16, 3.2),
    ])
    all_parts = plates + [coupon]
    positions = [(8, 8), (184, 8), (363, 8), (363, 121), (8, 204), (180, 204),
                 (363, 239), (423, 239), (8, 320), (180, 320), (363, 281), (387, 281), (426, 287)]
    layout = [(p, *xy) for p, xy in zip(all_parts, positions, strict=True)]
    assert all(x+p.width < 600 and y+p.height < 400 for p, x, y in layout)
    for i, (p, x, y) in enumerate(layout):
        for q, qx, qy in layout[:i]:
            assert x+p.width+3 <= qx or qx+q.width+3 <= x or y+p.height+3 <= qy or qy+q.height+3 <= y
    svg(folder / "sheet-600x400.svg", layout, 600, 400)
    dxf(folder / "sheet-600x400.dxf", layout)
    individual = folder / "individual"
    individual.mkdir(exist_ok=True)
    for p in all_parts:
        svg(individual / f"{p.name}.svg", [(p, 3, 3)], p.width+6, p.height+6)
        dxf(individual / f"{p.name}.dxf", [(p, 3, 3)])


def face_up(shape, direction):
    turns = {X: (Y, pi/2), NX: (Y, -pi/2), Y: (X, -pi/2), NY: (X, pi/2), NZ: (X, pi)}
    return wired.turn(shape, *turns[direction]) if direction in turns else shape


def models(t, plates, cubes, bolts):
    palette = {"01-floor": (60, 76, 90), "02-vented-lid": (100, 121, 137),
               "07-tool-gate": (192, 117, 61), "08-encoder-gate": (62, 137, 158)}
    result = [wired.part(PANEL, p.name, p.solid(t), palette.get(p.name, (57, 74, 91)))
              for p in plates]
    cube = printed.cut(printed.box(-6, -6, -6, 12, 12, 12),
                       *(printed.cylinder(*(wired.times(a, -6.05)), 1.53, 12.1, a) for a in (X, Y, Z)))
    for i, item in enumerate(cubes, 1):
        result.append(wired.part(BLOCKS, f"{item.name} block {i}", wired.move(cube, *item.center), wired.METAL))
    template = wired.metal_fasteners()
    screw6 = next(p.solid for p in template if p.name.endswith("mount 1 screw")).Located(TopLoc_Location())
    screw10 = printed.fuse(screw6, printed.cylinder(0, 0, -10, 1.47, 4.05))
    washer = next(p.solid for p in template if "washer" in p.name).Located(TopLoc_Location())
    for i, bolt in enumerate(bolts, 1):
        screw = screw6 if bolt.length == 6 else screw10
        result += [
            wired.part(SCREWS, f"{bolt.name} M3 x {bolt.length} screw {i}", wired.move(face_up(screw, bolt.out),
                       *wired.add(bolt.xyz, wired.times(bolt.out, 0.5))), wired.METAL),
            wired.part(SCREWS, f"{bolt.name} washer {i}", wired.move(face_up(washer, bolt.out), *bolt.xyz), wired.IVORY),
        ]
    stand = printed.cut(wired.hex_prism(5/(3**0.5), 10), printed.cylinder(0, 0, -0.05, 1.53, 10.1))
    for x, y in printed.H1_H4:
        result.append(wired.part(BLOCKS, "10 mm backplane standoff", wired.move(stand, x, y, t), wired.METAL))
    for x in (LEFT+18, RIGHT-18):
        for y in (21, DEPTH-21):
            result.append(wired.part(PADS, "Adhesive foot", printed.cylinder(x, y, -3.5, 6.35, 3.5), wired.BLACK))
    return result


def laser_ties(t):
    dz = t-3.0
    ties = []
    for gate, r in zip(printed.GATES, (6.99, 5.40)):
        c = gate.y
        z = gate.notch_bottom+gate.bundle/2+dz
        deck = gate.tie_top+dz
        bottom = deck-t-1.15
        foot = gate.bundle/2+1.0
        x = RIGHT-t-5.4

        def band_shape(offset, ax):
            leg = foot+offset
            return [(ax, c-leg, bottom-offset), (ax, c+leg, bottom-offset), (ax, c+leg, deck+0.5)] + [
                (ax, y, zz) for y, zz in arc(c, z, r+0.54+offset, 0, pi)
            ] + [(ax, c-leg, deck+0.5)]

        band = printed.cut(printed.prism(band_shape(0.43, x-1.25), (2.5, 0, 0)),
                           printed.prism(band_shape(-0.43, x-1.30), (2.6, 0, 0)))
        head = printed.box(x-1.75, c+foot-0.6, bottom-2.0, 3.5, 2.4, 2.8)
        ties.append(wired.part(wired.FIXINGS, gate.name[3:]+" shelf cable tie",
                               printed.fuse(band, head), wired.BLACK))
    return ties


def electronics(t, installed):
    result = []
    for item in installed:
        if item.group in {wired.CASE, wired.FIXINGS}:
            continue
        dx = LEFT if item.name.startswith("PMS12 BK080") else 0.0
        if item.name == "PMS12 BK080 locknut":
            dx += t - printed.WALL
        result.append(wired.part(item.group, item.name, wired.move(item.solid, dx, 0, t-3), item.rgb))
    return result + laser_ties(t)


def main():
    parser = argparse.ArgumentParser(description=__doc__)
    parser.add_argument("output", type=Path)
    parser.add_argument("--thickness", type=float, default=3.0, help="Measured uniform sheet thickness in mm")
    parser.add_argument("--pcb-steps", type=Path, help="Include the wired boards from the three cached KiCad STEP exports")
    parser.add_argument("--kicad-cli", default="kicad-cli")
    args = parser.parse_args()
    plates, cubes, bolts = kit(args.thickness)
    cut_files(args.output / "cut", plates)
    scene = models(args.thickness, plates, cubes, bolts)
    if args.pcb_steps:
        wired.use_step_exports(args.pcb_steps, args.kicad_cli)
        scene += electronics(args.thickness, wired.build_scene(args.pcb_steps))
    wired.write_step(args.output / "FAB-Computer-Laser-Cut.step", scene)
    print(f"{len(plates)} panels, {len(cubes)} threaded blocks, {len(bolts)} screws and washers")


if __name__ == "__main__":
    main()
