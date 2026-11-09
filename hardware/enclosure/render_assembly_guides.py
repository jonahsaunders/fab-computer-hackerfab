"""Render six assembly steps per enclosure from the case and board CAD."""
from dataclasses import dataclass
from pathlib import Path
import argparse

import numpy as np
from PIL import Image, ImageDraw, ImageFont

import build_enclosure as printed
import build_wired_assembly as wired
import laser_cut as laser
from render_enclosure import cutaway, mesh, render


TOP = (1.03, 0.72, 1.52)
FRONT = (-1.05, -0.80, 1.13)
ZERO = (0, 0, 0)
BOARD_GROUPS = [record[2] for record in wired.PCBS.values()]


@dataclass
class Step:
    title: str
    detail: str
    items: list
    arrows: list
    camera: tuple = TOP


def show(items, offset=ZERO):
    return [(p, offset) for p in items]


def lift(items, z):
    return show(items, (0, 0, z))


def down(points, height):
    return [(wired.add(p, (0, 0, height)), p) for p in points]


def printed_steps(model):
    case = [p for p in model if p.group == wired.CASE]
    base = [p for p in case if p.name == "01-base"]
    lid = [p for p in case if p.name == "02-lid"]
    gates = [p for p in case if "gate" in p.name]
    keepers = [p for p in case if "keeper" in p.name]
    fittings = [p for p in model if p.group == wired.FIXINGS]
    inserts = [p for p in fittings if "insert" in p.name]
    screws = [p for p in fittings if p.name.startswith("PCB mount") and "insert" not in p.name]
    cap_screws = [p for p in fittings if "keeper" in p.name and p.name.endswith("screw")]
    lid_screws = [p for p in fittings if p.name.startswith("Lid mount") and p.name.endswith("screw")]
    host = [p for p in model if p.group == BOARD_GROUPS[0]]
    cards = [p for p in model if p.group in BOARD_GROUPS[1:]]
    gland = [p for p in model if p.name.startswith(("PMS12", "J4 terminal", "24 V jacketed"))]
    board_step = base + inserts + gland
    pcb_points = [(x, y, 14.6) for x, y in (printed.H1_H4[0], printed.H1_H4[-1])]
    card_points = [(77, printed.MOTION_Y, printed.MOTION_Z), (76, printed.ENCODER_Y, printed.ENCODER_Z)]
    raised_inserts = []
    for item in inserts:
        raised_inserts += show([item], (12, 0, 0) if "gate" in item.name else (0, 0, 12))
    gate_inserts = [
        ((printed.WIDTH+11, y, printed.GATE_SCREW_Z), (printed.WIDTH-printed.GATE_RECESS, y, printed.GATE_SCREW_Z))
        for y in (gate.y-printed.GATE_SCREW_SPAN/2 for gate in printed.GATES)
    ]
    return [
        Step("Print the kit", "One base, one lid, two cable gates, and four keepers.",
             show(base)+show(lid, (158, -16, -106))+show(gates, (28,0,0))+lift(keepers, 19), []),
        Step("Fit the 16 inserts", "Four each at the base, lid, keepers, and gates.",
             show(base)+raised_inserts, down([(19, 9.2, 13), (158.8, 178.8, 108)], 11)+gate_inserts,
             (1.02, 0.61, 1.95)),
        Step("Mount the backplane", "Fit the DC gland first. Seat the PCB on its four standoffs.",
             show(board_step)+lift(host+screws, 22), down(pcb_points, 21), (1.02, 0.61, 1.95)),
        Step("Seat and secure the cards", "Motion goes in J1. Encoder goes in J3. Fit the four keepers last.",
             show(board_step+host+screws)+lift(cards, 12)+lift(keepers+cap_screws, 27), down(card_points, 11)),
        Step("Connect and secure the leads", "Thread the ties, plug in the leads, and drop both sleeves into the gates.",
             show(cutaway(model, routing=True)), [], TOP),
        Step("Close the lid", "Check both cable openings, then install the four lid screws.",
             show([p for p in model if p not in lid+lid_screws])+lift(lid, 20)+lift(lid_screws, 30),
             down([(7.2,7.2,112), (158.8,7.2,112)], 17), FRONT),
    ]


def laser_steps(shell, electronics):
    panels = [p for p in shell if p.group == laser.PANEL]
    floor, lid, *walls = panels[:6]
    gates = panels[6:8]
    keepers = panels[8:10]
    shelves = panels[10:12]
    fittings = [p for p in shell if p.group in {laser.BLOCKS, laser.SCREWS, laser.PADS}]
    board = [p for p in electronics if p.group == BOARD_GROUPS[0]]
    cards = [p for p in electronics if p.group in BOARD_GROUPS[1:]]
    gland = [p for p in electronics if p.name.startswith(("PMS12", "J4 terminal", "24 V jacketed"))]
    floor_parts = [p for p in fittings if p.group == laser.PADS or
                   p.name.startswith(("floor block", "10 mm backplane standoff"))]
    corner_parts = [p for p in fittings if p.name.startswith(("floor block", "lid block", "10 mm backplane standoff"))]
    bounds = {p.name: printed.bounds(p.solid) for p in fittings if p.group == laser.SCREWS}
    floor_fasteners = [p for p in fittings if p.group == laser.SCREWS and bounds[p.name][2] < 0]
    wall_fasteners = [p for p in fittings if p.group == laser.SCREWS and p.name.startswith(("floor", "lid"))
                      and bounds[p.name][2] >= 0 and bounds[p.name][5] <= laser.DECK]
    keep_blocks = [p for p in fittings if p.group == laser.BLOCKS and "keeper" in p.name]
    keep_fasteners = [p for p in fittings if p.group == laser.SCREWS and "keeper" in p.name]
    wall_keep = [p for p in keep_fasteners if bounds[p.name][0] < laser.LEFT or bounds[p.name][3] > laser.RIGHT]
    bar_keep = [p for p in keep_fasteners if p not in wall_keep]
    pcb_screws = [p for p in fittings if p.group == laser.SCREWS and p.name.startswith("backplane")
                  and bounds[p.name][2] > 8]
    normal_case = [floor, *walls, *corner_parts, *wall_fasteners]
    installed = [p for p in shell if p != lid and not (p.group == laser.SCREWS and p.name.startswith("lid")
                 and printed.bounds(p.solid)[5] > laser.DECK+0.1)]
    cut = printed.cut(walls[1].solid, printed.box(162, 2, 34, 7, 182, 47.8))
    installed = [wired.part(p.group, p.name, cut, p.rgb) if p == walls[1] else p for p in installed]
    lid_screws = [p for p in shell if p.group == laser.SCREWS and p.name.startswith("lid")
                  and printed.bounds(p.solid)[5] > laser.DECK+0.1]
    exploded_walls = []
    for panel, shift in zip(walls, ((-16,0,0), (16,0,0), (0,-16,0), (0,16,0)), strict=True):
        exploded_walls += show([panel], shift)
    return [
        Step("Start at the floor", "Fit four blocks and four 10 mm standoffs. Add the feet underneath.",
             show([floor]+floor_fasteners)+show([p for p in floor_parts if p.group == laser.PADS])+
             lift([p for p in floor_parts if p.group == laser.BLOCKS], 14),
             down([(7,9,12), (122.5,155.2,13)], 12), TOP),
        Step("Build the four walls", "Use the lower and upper corner blocks. Keep the top open.",
             show([floor]+corner_parts)+exploded_walls,
             [((184,54,57), (166,54,57)), ((89,-18,48), (89,0,48))], TOP),
        Step("Fit the gland and host", "Feed the DC lead before lowering the host onto its four standoffs.",
             show(normal_case+gland)+lift(board+pcb_screws, 21),
             down([(19,9.2,14.6),(122.5,155.2,14.6)], 20), (-1.02,-0.61,1.95)),
        Step("Add the two cards and bars", "Seat J1 and J3 before fastening their two removable keeper bars.",
             show(normal_case+gland+board+pcb_screws+keep_blocks+wall_keep)+lift(cards, 11)+lift(keepers, 25)+lift(bar_keep, 29),
             down([(77,printed.MOTION_Y,88.1),(77,printed.ENCODER_Y,54.1)], 11)),
        Step("Mount the gates and route", "Bolt each gate through the wall to its shelf blocks. Tie both bundles.",
             show(installed+electronics), [], TOP),
        Step("Fasten the lid", "Check the USB plugs and sleeved bundles, then install four lid screws.",
             show([p for p in shell if p not in [lid,*lid_screws]]+electronics)+lift([lid],20)+lift(lid_screws,30),
             down([(7,9,111),(157,9,111)], 18), FRONT),
    ]


def page(path, title, subtitle, steps, regular, bold, cache):
    img = Image.new("RGB", (2400, 2825), "#edf2f2")
    draw = ImageDraw.Draw(img)

    def font(size, semibold=False):
        return ImageFont.truetype(str(bold if semibold else regular), size)

    ink, muted = "#162b38", "#4b6270"
    draw.rectangle((75,69,139,81), fill="#bb784b")
    draw.text((158,44), "FAB COMPUTER  /  ASSEMBLY", font=font(43, True), fill=muted)
    draw.text((70,105), title, font=font(87, True), fill=ink)
    draw.text((76,211), subtitle, font=font(44), fill=muted)
    for i, step in enumerate(steps):
        print(path.stem, i+1, step.title, flush=True)
        x, y = 64 + (i%2)*1147, 302 + (i//2)*816
        draw.rounded_rectangle((x, y, x+1125, y+794), radius=28, fill="#f9fbfb", outline="#d5e0e1", width=3)
        draw.rounded_rectangle((x+28,y+25,x+108,y+101), radius=15, fill="#285566")
        draw.text((x+68,y+63), str(i+1), fill="#ffffff", font=font(49, True), anchor="mm")
        draw.text((x+133,y+35), step.title, fill=ink, font=font(50, True))
        objects = []
        for part, shift in step.items:
            key = (part.name, hash(part.solid))
            if key not in cache:
                cache[key] = mesh(part)
            xyz, color = cache[key]
            objects.append((xyz+np.asarray(shift), color) if shift != ZERO else (xyz, color))
        pic, locate = render(objects, (1053, 590), step.camera)
        dx, dy = x+36, y+111
        img.paste(pic, (dx, dy))
        for a, b in step.arrows:
            a = np.array(locate(a))+(dx,dy)
            b = np.array(locate(b))+(dx,dy)
            if np.linalg.norm(b-a) < 12:
                continue
            direction = (b-a)/np.linalg.norm(b-a)
            cross = np.array([-direction[1], direction[0]])
            arrow_end = b-direction*4
            draw.line((tuple(a), tuple(arrow_end)), fill="#bf7846", width=6)
            draw.polygon([tuple(arrow_end), tuple(arrow_end-direction*18+cross*10),
                          tuple(arrow_end-direction*18-cross*10)], fill="#bf7846")
        label_font = font(33)
        lines = [""]
        for word in step.detail.split():
            candidate = f"{lines[-1]} {word}".strip()
            if draw.textlength(candidate, font=label_font) > 1059:
                lines.append(word)
            else:
                lines[-1] = candidate
        draw.multiline_text((x+33,y+706), "\n".join(lines), fill=muted, font=label_font, spacing=4)
    img.save(path, quality=94, method=6)


def main():
    parser = argparse.ArgumentParser(description=__doc__)
    parser.add_argument("output", type=Path)
    parser.add_argument("--pcb-steps", type=Path, required=True)
    parser.add_argument("--font", type=Path, required=True)
    parser.add_argument("--bold-font", type=Path, required=True)
    parser.add_argument("--version", choices=("both", "printed", "laser-cut"), default="both")
    args = parser.parse_args()
    model = wired.build_scene(args.pcb_steps)
    cache = {}
    args.output.mkdir(parents=True, exist_ok=True)
    if args.version != "laser-cut":
        page(args.output / "assemble-printed.webp", "Assemble the printed case",
             "PETG shell  ·  Heat-set inserts  ·  Four removable card keepers",
             printed_steps(model), args.font, args.bold_font, cache)
    if args.version != "printed":
        t = 3.0
        shell = laser.models(t, *laser.kit(t))
        page(args.output / "assemble-laser-cut.webp", "Assemble the laser-cut case",
             "3 mm acrylic  ·  M3 corner blocks  ·  Two removable keeper bars",
             laser_steps(shell, laser.electronics(t, model)), args.font, args.bold_font, cache)


if __name__ == "__main__":
    main()
