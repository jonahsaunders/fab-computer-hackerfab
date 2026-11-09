"""Render the wired STEP source geometry without a GUI (NumPy and Pillow)."""
from pathlib import Path
import argparse

import numpy as np
from PIL import Image, ImageDraw, ImageFont
from OCP.BRep import BRep_Tool
from OCP.BRepMesh import BRepMesh_IncrementalMesh
from OCP.TopAbs import TopAbs_FACE, TopAbs_REVERSED
from OCP.TopLoc import TopLoc_Location
from OCP.TopoDS import TopoDS

import build_enclosure as case
import build_wired_assembly as assembly


def mesh(item):
    solid = item.solid
    BRepMesh_IncrementalMesh(solid, 0.10, False, 0.20, True)
    cast_face = getattr(TopoDS, "Face_s", None) or TopoDS.Face
    batches = []
    for face in map(cast_face, case.shapes_of_type(solid, TopAbs_FACE)):
        loc = TopLoc_Location()
        tri = BRep_Tool.Triangulation_s(face, loc)
        if tri is None:
            continue
        transform = loc.Transformation()
        xyz = np.asarray([tri.Node(i).Transformed(transform).Coord() for i in range(1, tri.NbNodes()+1)])
        faces = np.asarray([tri.Triangle(i).Get() for i in range(1, tri.NbTriangles()+1)]) - 1
        if face.Orientation() == TopAbs_REVERSED:
            faces = faces[:, [0, 2, 1]]
        batches.append(xyz[faces])
    triangles = np.concatenate(batches)
    return triangles, np.tile(item.rgb, (len(triangles), 1))


def unit(v):
    return v / np.linalg.norm(v)


def view_frame(camera):
    eye = unit(np.asarray(camera))
    right = unit(np.cross([0., 0., 1.], eye))
    up = np.cross(eye, right)
    return np.array([right, -up, eye]).T


def framing(xyz, width, height, border):
    low, high = xyz[:, :, :2].min(axis=(0, 1)), xyz[:, :, :2].max(axis=(0, 1))
    scale = min((width - 2*border)/(high[0]-low[0]), (height - 2*border)/(high[1]-low[1]))
    offset = np.array([width, height])/2 - (low+high)*scale/2
    return scale, offset


def raster(triangles, normals, width, height, frame, scale, offset, shadow=False):
    visible = normals @ frame[:, 2] > 1e-6
    projected = triangles[visible] @ frame
    projected[:, :, :2] = projected[:, :, :2] * scale + offset
    depth = np.full((height, width), -np.inf, dtype=np.float32)
    surface = np.full((height, width), -1, dtype=np.int32) if not shadow else None
    indices = np.flatnonzero(visible)
    low = np.maximum(np.floor(projected[:, :, :2].min(axis=1)).astype(int), 0)
    high = np.minimum(np.ceil(projected[:, :, :2].max(axis=1)).astype(int), [width-1, height-1])
    for index, p, (left, top), (right, bottom) in zip(indices, projected, low, high):
        (ax, ay, az), (bx, by, bz), (cx, cy, cz) = p
        area = (by-cy)*(ax-cx)+(cx-bx)*(ay-cy)
        if abs(area) < 0.0001 or left > right or top > bottom:
            continue
        dx = np.arange(left, right+1)[None, :] + (0.5-cx)
        dy = np.arange(top, bottom+1)[:, None] + (0.5-cy)
        u = ((by-cy)*dx+(cx-bx)*dy)/area
        v = ((cy-ay)*dx+(ax-cx)*dy)/area
        w = 1-u-v
        depth_view = depth[top:bottom+1, left:right+1]
        z = u*az+v*bz+w*cz
        mask = (u >= -1e-5) & (v >= -1e-5) & (w >= -1e-5) & (z > depth_view)
        if np.any(mask):
            depth_view[mask] = z[mask]
            if surface is not None:
                surface[top:bottom+1, left:right+1][mask] = index
    return depth, surface


def render(objects, size, camera, key=(-0.50, -0.70, 1.4)):
    """Orthographic render with a filtered shadow map and contact shadows."""
    triangles = np.concatenate([obj[0] for obj in objects])
    colors = np.concatenate([obj[1] for obj in objects])
    normal = np.cross(triangles[:, 1]-triangles[:, 0], triangles[:, 2]-triangles[:, 0])
    normal /= np.maximum(np.linalg.norm(normal, axis=1, keepdims=True), 1e-14)
    width, height = size
    view = view_frame(camera)
    scale, offset = framing(triangles @ view, width, height, height*0.085)
    depth, surfaces = raster(triangles, normal, width, height, view, scale, offset)

    light = view_frame(key)
    ssize = min(1550, max(620, width//2))
    ls, lo = framing(triangles @ light, ssize, ssize, ssize*0.06)
    shadowmap, _ = raster(triangles, normal, ssize, ssize, light, ls, lo, True)
    view_to_light = view.T @ light
    canvas = np.empty((height, width, 3), dtype=np.uint8)
    light_angle = np.clip(normal @ light[:, 2], 0, 1)
    reflection = unit(light[:, 2] + view[:, 2])
    gloss = np.clip(normal @ reflection, 0, 1)**17
    face_angle = np.clip(normal @ view[:, 2], 0, 1)
    ambient = 0.65 + 0.19*np.clip(normal[:, 2], 0, 1) + 0.085*face_angle

    for start in range(0, height, 128):
        stop = min(start+128, height)
        x = (np.arange(width)[None, :]+0.5-offset[0])/scale
        y = (np.arange(start, stop)[:, None]+0.5-offset[1])/scale
        zfloor = (-0.16 - x*view[2, 0] - y*view[2, 1])/view[2, 2]
        face = surfaces[start:stop]
        hit = face >= 0
        z = np.where(hit, depth[start:stop], zfloor)
        lx = (x*view_to_light[0, 0]+y*view_to_light[1, 0]+z*view_to_light[2, 0])*ls+lo[0]
        ly = (x*view_to_light[0, 1]+y*view_to_light[1, 1]+z*view_to_light[2, 1])*ls+lo[1]
        lz = x*view_to_light[0, 2]+y*view_to_light[1, 2]+z*view_to_light[2, 2]
        ux, uy = lx.astype(int), ly.astype(int)
        covered = np.zeros_like(z)
        for ox, oy in ((0, 0), (2, 4), (-2, -4), (4, -2), (-4, 2), (6, 0), (-6, 0)):
            qx, qy = ux+ox, uy+oy
            valid = (qx >= 0) & (qx < ssize) & (qy >= 0) & (qy < ssize)
            covered += valid & (shadowmap[qy.clip(0, ssize-1), qx.clip(0, ssize-1)] > lz+0.44)
        shade = covered/7
        f = face[hit]
        intensity = ambient[f] + 0.29*light_angle[f]*(1-0.78*shade[hit])
        rgb = colors[f]*intensity[:, None] + (gloss[f]*(1-0.65*shade[hit])*19)[:, None]
        canvas[start:stop] = np.clip(np.array([249, 251, 251]) - shade[:, :, None]*np.array([15, 18, 18]), 0, 255).astype(np.uint8)
        canvas[start:stop][hit] = np.clip(rgb, 0, 255).astype(np.uint8)

    def locate(xyz):
        q = np.asarray(xyz) @ view
        return tuple(q[:2]*scale+offset)

    return Image.fromarray(canvas), locate


def cutaway(parts, routing=False):
    out = []
    for item in parts:
        if item.name == "02-lid" or (item.group == assembly.FIXINGS and item.name.startswith("Lid mount") and item.name.endswith(" screw")):
            continue
        if item.name == "01-base":
            cutters = [case.box(145, 2, 38, 24, 182, 43.8)]
            if routing:
                cutters.append(case.box(-1, 179.7, 39, 168, 8, 70))
            solid = case.cut(item.solid, *cutters)
        elif item.name in {"Host USB-C lead", "Motion USB-C lead", "24 V jacketed lead"}:
            solid = case.cut(item.solid, case.box(-90, -95, -1, 68, 310, 115),
                             case.box(-100, -95, -1, 335, 72, 115))
        else:
            solid = item.solid
        out.append(assembly.part(item.group, item.name, solid, item.rgb))
    return out


def main():
    parser = argparse.ArgumentParser(description=__doc__)
    parser.add_argument("output", type=Path)
    parser.add_argument("--pcb-steps", type=Path, required=True)
    parser.add_argument("--font", type=Path, required=True, help="Path to a regular sans serif TrueType font")
    parser.add_argument("--bold-font", type=Path, required=True, help="Path to a semibold TrueType font")
    parser.add_argument("--proof", action="store_true", help="Render at 45 percent size")
    args = parser.parse_args()
    args.output.mkdir(parents=True, exist_ok=True)
    parts = assembly.build_scene(args.pcb_steps)
    factor = 0.45 if args.proof else 1.0
    cached = {}

    def px(value):
        return round(value*factor)

    def xy(x, y):
        return px(x), px(y)

    def font(size, bold=False):
        return ImageFont.truetype(str(args.bold_font if bold else args.font), px(size))

    def get_models(visible):
        for item in visible:
            key = (item.group, item.name, hash(item.solid))
            if key not in cached:
                cached[key] = mesh(item)
            yield cached[key]

    paper, ink, muted = "#edf2f2", "#182b38", "#4c6370"
    hero = Image.new("RGB", xy(3840, 2160), paper)
    draw = ImageDraw.Draw(hero)

    def text(x, y, value, size, bold=False, fill=ink):
        draw.text(xy(x, y), value, fill=fill, font=font(size, bold))

    def panel(x, y, w, h):
        draw.rounded_rectangle((*xy(x, y), *xy(x+w, y+h)), radius=px(34),
                               fill="#f9fbfb", outline="#d6e2e2", width=max(1, px(3)))

    draw.rectangle((*xy(122, 85), *xy(191, 97)), fill="#bb784b")
    text(219, 58, "FAB COMPUTER   /   ENCLOSURE", 44, True, muted)
    text(116, 132, "Wired enclosure", 110, True)
    text(123, 265, "166 × 186 × 112 mm  ·  Motion in J1  ·  Encoders in J3", 48, False, muted)

    panel(108, 365, 2290, 1635)
    text(168, 409, "Cable routing cutaway", 56, True)
    print("Rendering open assembly", flush=True)
    opened, _ = render(list(get_models(cutaway(parts))), xy(2170, 1415), (1.03, 0.89, 1.67))
    hero.paste(opened, xy(168, 490))
    for x, label, color in ((171, "TOOL BUNDLE", "#bf753d"), (770, "ENCODER BUNDLE", "#3e899e")):
        draw.rounded_rectangle((*xy(x, 1923), *xy(x+26, 1949)), radius=px(6), fill=color)
        text(x+43, 1907, label, 40, True, muted)

    panel(2440, 365, 1292, 1635)
    text(2500, 409, "Service connections", 56, True)
    print("Rendering service side", flush=True)
    closed_parts = [p for p in parts if p.group in {assembly.CASE, assembly.SERVICE, assembly.FIXINGS}
                    and "cable tie" not in p.name and "terminal lead" not in p.name]
    closed, locate = render(list(get_models(closed_parts)), xy(1172, 1145), (-1.08, -0.86, 0.92))
    hero.paste(closed, xy(2500, 576))
    for i, (label, xyz, (dx, dy)) in enumerate([
        ("24 V DC", (-14, case.DC_GLAND_Y, case.DC_GLAND_Z), (-92, 56)),
        ("Motion USB-C", (-5, case.MOTION_USB_Y, case.MOTION_USB_Z), (-96, -69)),
        ("Host USB-C", (case.HOST_USB_X, -8.0, case.HOST_USB_Z), (83, -65)),
    ], 1):
        anchor_x, anchor_y = locate(xyz)
        anchor_x, anchor_y = px(2500)+anchor_x, px(576)+anchor_y
        x, y = anchor_x+px(dx), anchor_y+px(dy)
        r = px(32)
        draw.line((anchor_x, anchor_y, x, y), fill="#92a8b2", width=max(1, px(5)))
        dot = px(7)
        draw.ellipse((anchor_x-dot, anchor_y-dot, anchor_x+dot, anchor_y+dot), fill="#e6edef")
        draw.ellipse((x-r, y-r, x+r, y+r), fill="#f7fafa", outline="#526874", width=max(1, px(3)))
        draw.text((x, y), str(i), fill=ink, font=font(35, True), anchor="mm")
        text(2498+(i-1)*394, 1820, f"{i}  {label}", 40, True, muted)
    text(120, 2035, "CAD assembly with cable and mating-housing envelopes", 38, False, muted)
    hero.save(args.output / "wired-case.webp", quality=94, method=6)

    print("Rendering close-up", flush=True)
    closeup, _ = render(list(get_models(cutaway(parts, routing=True))), xy(3060, 2070), (0.61, 0.73, 2.06))
    routing = Image.new("RGB", xy(3200, 2410), paper)
    routing.paste(closeup, xy(70, 218))
    close_draw = ImageDraw.Draw(routing)
    close_draw.text(xy(92, 57), "Installed harnesses", fill=ink, font=font(95, True))
    close_draw.text(xy(96, 2321), "JST housings and wire fanouts are visible above the boards. The side wall is sectioned.", fill=muted, font=font(39))
    routing.save(args.output / "wired-routing.webp", quality=94, method=6)


if __name__ == "__main__":
    main()
