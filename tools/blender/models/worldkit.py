"""
World architecture kit: parts for building the miniatures of every city outside
Rome (Islamic, Mughal and Indian, Chinese and Japanese, Gothic and Byzantine,
Egyptian and Mesopotamian, Mesoamerican and Andean, African). Same conventions
as chronokit: metres, origin at the ground centre, +X east, +Y north, +Z up,
flat clay colours. Openings are dark inset panels rather than boolean holes:
they read the same at miniature scale and stay light to bake.

Every function returns one joined object; compose them into a chronokit.Model.
"""
import math
import bpy, bmesh
from mathutils import Vector
from chronokit import box, cylinder, dome, join, shade, mesh_from, hip_roof, gable_roof, _finish

# palette by material, shared by every city
RED_SANDSTONE, BUFF_SANDSTONE, MARBLE, PLASTER, MUDBRICK, BRICK = "#A8553F", "#C9A06A", "#EEE8DC", "#E6DCC8", "#B48A62", "#B5714F"
LIMESTONE, GRANITE, BASALT, TUFA, ADOBE, WHITEWASH = "#D8CBB0", "#9C9690", "#5E5A56", "#C9B48A", "#C29B70", "#F0EBE0"
TILE_GREY, TILE_GREEN, TILE_GOLD, TILE_RED, SLATE, LEAD = "#5E5F62", "#5F8A5A", "#C9A24A", "#A65238", "#5C6068", "#7D8590"
TIMBER, TIMBER_RED, LACQUER, THATCH, GILT, BRONZE = "#8C6A4A", "#9A3A2C", "#B23A2A", "#B39A5E", "#D4AE55", "#7E6E4E"
GLAZE_BLUE, GLAZE_TURQ, DARK, WATER, GREEN, STUCCO = "#3E5C9A", "#3F9A9A", "#2E241C", "#5F878C", "#7D9A6C", "#E8DCC2"


def lathe(name, profile, loc=(0, 0, 0), color=MARBLE, verts=24, cap_top=True, cap_bottom=True):
    """Solid of revolution about Z from [(radius, z), ...] going upward."""
    bm = bmesh.new()
    rings = []
    for r, z in profile:
        ring = []
        for i in range(verts):
            a = math.tau * i / verts
            ring.append(bm.verts.new((loc[0] + r * math.cos(a), loc[1] + r * math.sin(a), loc[2] + z)))
        rings.append(ring)
    for a, b in zip(rings, rings[1:]):
        for i in range(verts):
            j = (i + 1) % verts
            bm.faces.new((a[i], a[j], b[j], b[i]))
    if cap_bottom and profile[0][0] > 1e-4:
        bm.faces.new(list(reversed(rings[0])))
    if cap_top and profile[-1][0] > 1e-4:
        bm.faces.new(rings[-1])
    bmesh.ops.remove_doubles(bm, verts=bm.verts, dist=1e-5)
    bmesh.ops.recalc_face_normals(bm, faces=bm.faces)
    me = bpy.data.meshes.new(name)
    bm.to_mesh(me)
    bm.free()
    o = bpy.data.objects.new(name, me)
    bpy.context.collection.objects.link(o)
    return _finish(o, name, color)


def prism(name, pts, h, loc=(0, 0, 0), color=LIMESTONE):
    """Extrude a closed 2D outline [(x, y), ...] (counter-clockwise) up by h."""
    n = len(pts)
    verts = [(x, y, 0) for x, y in pts] + [(x, y, h) for x, y in pts]
    faces = [tuple(range(n))[::-1], tuple(range(n, 2 * n))] + [(i, (i + 1) % n, n + (i + 1) % n, n + i) for i in range(n)]
    return mesh_from(name, verts, faces, loc, color)


def frustum(name, w0, d0, w1, d1, h, loc=(0, 0, 0), color=LIMESTONE):
    """A box with a smaller top: battered walls, pylons, pyramid tiers, platforms."""
    verts = [(-w0 / 2, -d0 / 2, 0), (w0 / 2, -d0 / 2, 0), (w0 / 2, d0 / 2, 0), (-w0 / 2, d0 / 2, 0),
             (-w1 / 2, -d1 / 2, h), (w1 / 2, -d1 / 2, h), (w1 / 2, d1 / 2, h), (-w1 / 2, d1 / 2, h)]
    faces = [(3, 2, 1, 0), (4, 5, 6, 7), (0, 1, 5, 4), (1, 2, 6, 5), (2, 3, 7, 6), (3, 0, 4, 7)]
    return mesh_from(name, verts, faces, loc, color)


def rot(o, deg):
    """Turn a part about the vertical axis through the world origin (where every part is built)."""
    bpy.ops.object.select_all(action="DESELECT")
    o.select_set(True)
    bpy.context.view_layer.objects.active = o
    bpy.ops.object.transform_apply(location=True, rotation=True, scale=True)
    o.rotation_euler[2] += math.radians(deg)
    bpy.ops.object.transform_apply(rotation=True)
    return o


def move(o, x=0, y=0, z=0):
    o.location = (o.location[0] + x, o.location[1] + y, o.location[2] + z)
    bpy.ops.object.select_all(action="DESELECT")
    o.select_set(True)
    bpy.context.view_layer.objects.active = o
    bpy.ops.object.transform_apply(location=True)
    return o


# ---------------------------------------------------------------- openings and trim

def arch_panel(name, w, h, loc, face="S", color=DARK, pointed=True, depth=0.3):
    """A dark arched recess on a wall face (a door, an arcade bay, a window). loc = centre of its base on the wall."""
    x, y, z = loc
    rect_h = h - w / 2 * (1.1 if pointed else 1.0)
    parts = [box(name + "_r", w, depth, rect_h, (0, 0, 0), color)]
    if pointed:
        tip = h - rect_h
        pts = [(-w / 2, 0), (w / 2, 0), (w * 0.22, tip * 0.75), (0, tip), (-w * 0.22, tip * 0.75)]
    else:
        pts = [(w / 2 * math.cos(math.pi * i / 8), w / 2 * math.sin(math.pi * i / 8)) for i in range(9)]
    verts = [(px, -depth / 2, pz + rect_h) for px, pz in pts] + [(px, depth / 2, pz + rect_h) for px, pz in pts]
    n = len(pts)
    faces = [tuple(range(n)), tuple(range(2 * n - 1, n - 1, -1))] + [(i, (i + 1) % n, n + (i + 1) % n, n + i) for i in range(n)]
    parts.append(mesh_from(name + "_t", verts, faces, (0, 0, 0), color))
    o = join(parts, name)
    o = rot(o, {"S": 0, "N": 180, "E": 90, "W": -90}[face])
    return move(o, x, y, z)


def arcade(name, length, h, n, loc, face="S", color=DARK, pointed=True, fill=0.7, depth=0.3):
    """A row of n arched recesses along a wall face, centred on loc."""
    x, y, z = loc
    bay = length / n
    along = (1, 0) if face in ("S", "N") else (0, 1)
    out = [arch_panel(f"{name}{i}", bay * fill, h, (x + along[0] * (-length / 2 + bay * (i + 0.5)), y + along[1] * (-length / 2 + bay * (i + 0.5)), z), face, color, pointed, depth) for i in range(n)]
    return join(out, name)


def merlons(name, w, d, z, size=0.8, gap=1.0, color=RED_SANDSTONE, shape="box"):
    """Battlements round the top of a w x d rectangle. shape: box | round | stepped."""
    out = []
    step = size + gap
    for side, (length, fixed, horiz) in enumerate([(w, -d / 2, True), (w, d / 2, True), (d, -w / 2, False), (d, w / 2, False)]):
        n = max(1, int(length / step))
        for i in range(n):
            t = -length / 2 + (i + 0.5) * length / n
            x, y = (t, fixed) if horiz else (fixed, t)
            if shape == "round":
                out.append(cylinder(f"{name}{side}_{i}", size / 2, size * 1.1, (x, y, z), color, verts=8))
                out.append(dome(f"{name}{side}_{i}d", size / 2, (x, y, z + size * 1.1), color, segments=8, rings=4))
            elif shape == "stepped":
                out.append(box(f"{name}{side}_{i}", size, size, size * 0.6, (x, y, z), color))
                out.append(box(f"{name}{side}_{i}b", size * 0.55, size * 0.55, size * 0.5, (x, y, z + size * 0.6), color))
            else:
                out.append(box(f"{name}{side}_{i}", size, size * 0.7, size * 1.1, (x, y, z), color))
    return join(out, name)


def cornice(name, w, d, z, h=0.6, over=0.5, color=LIMESTONE):
    return box(name, w + over * 2, d + over * 2, h, (0, 0, z), color)


def stair(name, w, rise, run, n, loc, face="S", color=LIMESTONE):
    """Steps climbing from the ground at loc toward the building (away from face)."""
    x, y, z = loc
    # stacked treads, each shorter than the one below, all flush with the building side (+Y before rotation)
    parts = [box(f"{name}{i}", w, run * (n - i) / n, rise / n, (0, run / 2 - run * (n - i) / n / 2, z + rise * i / n), color) for i in range(n)]
    o = join(parts, name)
    o = rot(o, {"S": 0, "N": 180, "E": 90, "W": -90}[face])
    return move(o, x, y, 0)


# ---------------------------------------------------------------- Islamic, Persian, Mughal and Indian

def onion_dome(name, r, loc=(0, 0, 0), color=MARBLE, bulb=1.18, height=1.55, drum=0.5, finial=True, finial_color=GILT):
    """A bulbous dome on a drum, with a lotus collar and a finial. r = drum radius; height in units of r."""
    x, y, z = loc
    R, H = r, r * height
    prof = [(R, 0), (R, drum * r), (R * 1.04, drum * r), (R * bulb, drum * r + H * 0.28), (R * bulb * 0.98, drum * r + H * 0.45), (R * 0.82, drum * r + H * 0.66),
            (R * 0.45, drum * r + H * 0.84), (R * 0.16, drum * r + H * 0.95), (0.0, drum * r + H)]
    parts = [lathe(name + "_b", prof, (x, y, z), color, verts=28)]
    if finial:
        top = z + drum * r + H
        parts.append(lathe(name + "_f", [(r * 0.12, 0), (r * 0.16, r * 0.08), (r * 0.05, r * 0.2), (r * 0.1, r * 0.3), (r * 0.03, r * 0.42), (0.0, r * 0.62)], (x, y, top - r * 0.02), finial_color, verts=10))
    return join(parts, name)


def shallow_dome(name, r, loc=(0, 0, 0), color=MARBLE, rise=0.55, drum=0.0, finial=False):
    x, y, z = loc
    prof = [(r, 0)] + ([(r, drum)] if drum else []) + [(r * math.cos(a), drum + r * rise * math.sin(a)) for a in [math.pi / 2 * i / 7 for i in range(1, 8)]]
    prof[-1] = (0.0, prof[-1][1])
    parts = [lathe(name + "_d", prof, (x, y, z), color, verts=28)]
    if finial:
        parts.append(cylinder(name + "_f", r * 0.05, r * 0.35, (x, y, z + drum + r * rise), GILT, verts=8))
    return join(parts, name)


def ribbed_dome(name, r, loc=(0, 0, 0), color=GLAZE_TURQ, height=1.5, ribs=16, drum=0.6, drum_color=GLAZE_BLUE):
    """Timurid melon dome: a tall drum and a fluted bulb."""
    x, y, z = loc
    parts = [cylinder(name + "_drum", r * 0.92, r * drum, (x, y, z), drum_color, verts=ribs * 2)]
    bulb = onion_dome(name + "_bulb", r * 0.92, (x, y, z + r * drum), color, bulb=1.12, height=height, drum=0.0, finial=True)
    me = bulb.data
    for v in me.vertices:
        dx, dy = v.co.x - x, v.co.y - y
        rr = math.hypot(dx, dy)
        if rr > 1e-3:
            a = math.atan2(dy, dx)
            k = 1 + 0.06 * math.cos(a * ribs)
            v.co.x, v.co.y = x + dx * k, y + dy * k
    parts.append(bulb)
    return join(parts, name)


def chhatri(name, r, h, loc=(0, 0, 0), color=MARBLE, dome_color=None, pillars=6, base=0.0):
    """An open domed kiosk on pillars, with a chhajja (eave) and a little onion dome."""
    x, y, z = loc
    parts = []
    if base:
        parts.append(cylinder(name + "_base", r * 1.1, base, (x, y, z), color, verts=pillars * 2))
        z += base
    for i in range(pillars):
        a = math.tau * i / pillars
        parts.append(cylinder(f"{name}_p{i}", r * 0.09, h * 0.55, (x + r * 0.8 * math.cos(a), y + r * 0.8 * math.sin(a), z), color, verts=6))
    parts.append(cylinder(name + "_eave", r * 1.25, h * 0.06, (x, y, z + h * 0.55), color, verts=pillars * 2, r_top=r * 0.95))
    parts.append(onion_dome(name + "_d", r * 0.85, (x, y, z + h * 0.61), dome_color or color, height=1.3, drum=0.15))
    return join(parts, name)


def minaret(name, r, h, loc=(0, 0, 0), color=RED_SANDSTONE, band_color=MARBLE, balconies=3, cap="chhatri", sides=16, taper=0.75):
    """A tapering tower with corbelled balconies and a crowning kiosk (cap: chhatri | cone | lantern | dome)."""
    x, y, z = loc
    parts = [cylinder(name + "_shaft", r, h, (x, y, z), color, verts=sides, r_top=r * taper)]
    for i in range(1, balconies + 1):
        t = h * i / (balconies + 0.6)
        rr = r * (1 - (1 - taper) * t / h)
        parts.append(cylinder(f"{name}_bal{i}", rr * 1.45, r * 0.22, (x, y, z + t), band_color, verts=sides))
        parts.append(cylinder(f"{name}_cor{i}", rr * 1.02, r * 0.3, (x, y, z + t - r * 0.3), band_color, verts=sides, r_top=rr * 1.45))
    top = z + h
    rt = r * taper
    if cap == "chhatri":
        parts.append(chhatri(name + "_ch", rt * 1.25, rt * 3.2, (x, y, top), band_color))
    elif cap == "cone":
        parts.append(cylinder(name + "_cone", rt * 1.1, rt * 4.5, (x, y, top), LEAD, verts=sides, r_top=0.0))
    elif cap == "lantern":
        parts.append(cylinder(name + "_lan", rt * 0.8, rt * 2.2, (x, y, top), band_color, verts=8))
        parts.append(dome(name + "_lantd", rt * 0.85, (x, y, top + rt * 2.2), color, segments=12, rings=6))
    else:
        parts.append(onion_dome(name + "_cap", rt, (x, y, top), band_color, height=1.4, drum=0.2))
    return join(parts, name)


def iwan(name, w, h, depth, loc=(0, 0, 0), face="S", color=BUFF_SANDSTONE, frame=MARBLE, panel=DARK):
    """A pishtaq: a tall rectangular frame around a deep pointed-arch recess, the gateway of mosques, madrasas and tombs."""
    x, y, z = loc
    parts = [box(name + "_frame", w, depth, h, (0, 0, 0), color)]
    parts.append(box(name + "_band", w * 0.92, depth + 0.2, h * 0.04, (0, 0, h * 0.93), frame))
    for s in (-1, 1):
        parts.append(box(f"{name}_edge{s}", w * 0.04, depth + 0.2, h * 0.95, (s * w * 0.44, 0, 0), frame))
        parts.append(cylinder(f"{name}_gul{s}", w * 0.045, h * 0.25, (s * w * 0.48, -depth / 2, h), frame, verts=8, r_top=w * 0.02))
    o = join(parts, name)
    arch = arch_panel(name + "_arch", w * 0.62, h * 0.78, (0, -depth / 2 - 0.05, 0), "S", panel, True, 0.4)
    o = join([o, arch], name)
    o = rot(o, {"S": 0, "N": 180, "E": 90, "W": -90}[face])
    return move(o, x, y, z)


def jali_wall(name, length, h, loc, face="S", color=MARBLE, n=6):
    """A low screen wall with lattice panels (drawn as shallow dark rectangles)."""
    x, y, z = loc
    parts = [box(name + "_w", length, 0.4, h, (0, 0, 0), color)]
    bay = length / n
    for i in range(n):
        parts.append(box(f"{name}_j{i}", bay * 0.6, 0.45, h * 0.6, (-length / 2 + bay * (i + 0.5), 0, h * 0.2), shade(color, -0.3)))
    o = join(parts, name)
    o = rot(o, {"S": 0, "N": 180, "E": 90, "W": -90}[face])
    return move(o, x, y, z)


def courtyard_ring(name, w, d, wall_h, depth, loc=(0, 0, 0), color=RED_SANDSTONE, arcade_color=DARK, inner_arcade=True, bays=None):
    """Four ranges of rooms round an open court (mosque courts, caravanserais, madrasas, palaces)."""
    x, y, z = loc
    parts = [box(name + "_s", w, depth, wall_h, (x, y - d / 2 + depth / 2, z), color), box(name + "_n", w, depth, wall_h, (x, y + d / 2 - depth / 2, z), color),
             box(name + "_w", depth, d - 2 * depth, wall_h, (x - w / 2 + depth / 2, y, z), color), box(name + "_e", depth, d - 2 * depth, wall_h, (x + w / 2 - depth / 2, y, z), color)]
    if inner_arcade:
        nb = bays or max(3, int(w / (wall_h * 0.9)))
        nd = max(3, int(d / (wall_h * 0.9)))
        ah = wall_h * 0.72
        parts.append(arcade(name + "_as", w - 2 * depth, ah, nb, (x, y - d / 2 + depth + 0.05, z), "N", arcade_color))
        parts.append(arcade(name + "_an", w - 2 * depth, ah, nb, (x, y + d / 2 - depth - 0.05, z), "S", arcade_color))
        parts.append(arcade(name + "_aw", d - 2 * depth, ah, nd, (x - w / 2 + depth + 0.05, y, z), "E", arcade_color))
        parts.append(arcade(name + "_ae", d - 2 * depth, ah, nd, (x + w / 2 - depth - 0.05, y, z), "W", arcade_color))
    return join(parts, name)


def mosque(name, w, d, loc=(0, 0, 0), color=RED_SANDSTONE, trim=MARBLE, dome_color=MARBLE, domes=3, minarets=2, minaret_h=None, hall_depth=None,
           court=True, plinth=0.0, style="mughal", qibla="W"):
    """
    A congregational mosque: a prayer hall on the qibla side with domes over it and an iwan in the middle,
    an arcaded court with a pool, gateways, and minarets. style: mughal | persian | ottoman | sultanate | maghrebi.
    Built facing qibla = "W" (India, Central Asia) and rotated for other sides.
    """
    parts = []
    z = plinth
    if plinth:
        parts.append(box(name + "_plinth", w + 6, d + 6, plinth, (0, 0, 0), color))
        for face, (px, py) in (("S", (0, -d / 2 - 3)), ("N", (0, d / 2 + 3)), ("E", (w / 2 + 3, 0))):
            parts.append(stair(f"{name}_st{face}", min(w, d) * 0.22, plinth, plinth * 2.2, max(4, int(plinth * 2)), (px, py, 0), face, color))
    hd = hall_depth or d * 0.28
    hall_h = max(8.0, min(w, d) * 0.14)
    # prayer hall along the west (qibla) side; the court opens east of it
    hx = -w / 2 + hd / 2
    parts.append(box(name + "_hall", hd, d * 0.9 if court else d, hall_h, (hx, 0, z), color))
    parts.append(move(cornice(name + "_hallc", hd, d * 0.9 if court else d, z + hall_h, 0.5, 0.4, trim), hx, 0, 0))
    parts.append(arcade(name + "_hallarc", d * 0.86, hall_h * 0.62, 11, (hx + hd / 2 + 0.05, 0, z), "E", DARK))
    iw_w, iw_h = min(d * 0.32, hall_h * 2.0), hall_h * 1.55
    parts.append(iwan(name + "_iwan", iw_w, iw_h, 3.0, (hx + hd / 2 + 1.0, 0, z), "E", color if style != "persian" else GLAZE_BLUE, trim))
    # domes over the hall
    rd = min(hd * 0.42, d * 0.12)
    for i in range(domes):
        t = 0 if domes == 1 else (i - (domes - 1) / 2) / ((domes - 1) / 2)
        r = rd * (1.0 if abs(t) < 0.01 else 0.72)
        py = t * d * 0.27
        if style == "persian":
            parts.append(ribbed_dome(f"{name}_dome{i}", r, (hx - hd * 0.1, py, z + hall_h), GLAZE_TURQ, height=1.45))
        elif style == "ottoman":
            parts.append(shallow_dome(f"{name}_dome{i}", r * 1.2, (hx - hd * 0.1, py, z + hall_h), LEAD, rise=0.6, drum=r * 0.35, finial=True))
        elif style == "maghrebi":
            parts.append(hip_roof(f"{name}_roof{i}", hd * 0.9, d * 0.28, hd * 0.18, (hx, py, z + hall_h), TILE_GREEN, ridge=0.5, overhang=0.3))
        else:
            parts.append(onion_dome(f"{name}_dome{i}", r, (hx - hd * 0.1, py, z + hall_h), dome_color, height=1.55 if style == "mughal" else 1.25, drum=0.5))
    if court:
        cw, cd = w - hd, d
        parts.append(courtyard_ring(name + "_court", cw, cd, hall_h * 0.6, max(4.0, cd * 0.07), (hx + hd / 2 + cw / 2, 0, z), color, DARK))
        parts.append(box(name + "_pave", cw - 2, cd - 2, 0.2, (hx + hd / 2 + cw / 2, 0, z), shade(color, 0.35)))
        parts.append(box(name + "_pool", min(cw, cd) * 0.16, min(cw, cd) * 0.16, 0.35, (hx + hd / 2 + cw / 2, 0, z), WATER))
        # gateways on the other three sides
        gx = w / 2
        parts.append(iwan(name + "_gateE", min(cd * 0.2, 16), hall_h * 1.2, 6, (gx, 0, z), "E", color, trim))
        if style == "mughal":
            for s, f in ((-1, "S"), (1, "N")):
                parts.append(iwan(f"{name}_gate{f}", min(cw * 0.16, 14), hall_h * 1.05, 6, (hx + hd / 2 + cw / 2, s * cd / 2, z), f, color, trim))
    mh = minaret_h or hall_h * 3.6
    mr = max(1.2, mh * 0.05)
    spots = [(-w / 2 + hd + 0.3, -d / 2 * 0.95), (-w / 2 + hd + 0.3, d / 2 * 0.95)] if minarets == 2 else [(-w / 2 + hd + 0.3, s * d / 2 * 0.95) for s in (-1, 1)] + [(w / 2, s * d / 2) for s in (-1, 1)]
    if minarets == 1:
        spots = [(w / 2 - mr * 2, d / 2 - mr * 2)]
    for i, (mx, my) in enumerate(spots[:minarets]):
        cap = {"mughal": "chhatri", "ottoman": "cone", "persian": "lantern", "maghrebi": "lantern", "sultanate": "dome"}[style]
        sides = 4 if style == "maghrebi" else 16
        parts.append(minaret(f"{name}_min{i}", mr, mh, (mx, my, z), color if style != "persian" else BUFF_SANDSTONE, trim, 3 if style == "mughal" else 2, cap, sides, 0.82 if style == "maghrebi" else 0.75))
    o = join(parts, name)
    return rot(o, {"W": 0, "S": 90, "E": 180, "N": -90}[qibla])


def tomb(name, w, h, loc=(0, 0, 0), color=MARBLE, trim=None, plinth=0.0, dome_r=None, chhatris=4, minarets=0, octagonal=False, onion=True):
    """A square (or octagonal) domed tomb with iwans on four sides, corner chhatris, optional plinth and minarets."""
    x, y, z = loc
    trim = trim or shade(color, -0.12)
    parts = []
    if plinth:
        pw = w * (2.0 if minarets else 1.5)
        parts.append(box(name + "_plinth", pw, pw, plinth, (x, y, z), color))
        parts.append(arcade(name + "_plarc", pw * 0.9, plinth * 0.75, 9, (x, y - pw / 2 - 0.05, z), "S", DARK, False))
        z += plinth
    if octagonal:
        pts = [((w / 2) * math.cos(math.pi / 8 + i * math.pi / 4), (w / 2) * math.sin(math.pi / 8 + i * math.pi / 4)) for i in range(8)]
        parts.append(prism(name + "_body", pts, h, (x, y, z), color))
    else:
        parts.append(box(name + "_body", w, w, h, (x, y, z), color))
        cut = w * 0.12
        for sx in (-1, 1):
            for sy in (-1, 1):
                parts.append(box(f"{name}_ch{sx}{sy}", cut, cut, h, (x + sx * (w / 2 - cut / 2), y + sy * (w / 2 - cut / 2), z), shade(color, -0.05)))
    for f, (dx, dy) in (("S", (0, -w / 2)), ("N", (0, w / 2)), ("E", (w / 2, 0)), ("W", (-w / 2, 0))):
        parts.append(iwan(f"{name}_iw{f}", w * 0.45, h * 0.95, 1.0, (x + dx, y + dy, z), f, color, trim))
    parts.append(cornice(name + "_corn", w, w, z + h, 0.5, 0.3, trim))
    r = dome_r or w * 0.33
    if onion:
        parts.append(onion_dome(name + "_dome", r, (x, y, z + h + 0.5), color, height=1.6, drum=0.7))
    else:
        parts.append(shallow_dome(name + "_dome", r, (x, y, z + h + 0.5), color, rise=0.9, drum=r * 0.4, finial=True))
    if chhatris:
        for sx in (-1, 1):
            for sy in (-1, 1):
                parts.append(chhatri(f"{name}_ct{sx}{sy}", w * 0.08, w * 0.22, (x + sx * w * 0.32, y + sy * w * 0.32, z + h + 0.5), color))
    if minarets:
        pw = w * 2.0
        for sx in (-1, 1):
            for sy in (-1, 1):
                parts.append(minaret(f"{name}_m{sx}{sy}", w * 0.045, h * 2.4, (x + sx * pw / 2 * 0.92, y + sy * pw / 2 * 0.92, z), color, trim, 3, "chhatri"))
    return join(parts, name)


def charbagh(name, w, d, loc=(0, 0, 0), path_color=RED_SANDSTONE, lawn=GREEN, water=WATER, trees=True):
    """A four-part garden: walks and water channels crossing at a central pool, trees in the beds."""
    x, y, z = loc
    parts = [box(name + "_lawn", w, d, 0.3, (x, y, z), lawn)]
    parts.append(box(name + "_walkx", w, d * 0.06, 0.45, (x, y, z), path_color))
    parts.append(box(name + "_walky", w * 0.06, d, 0.45, (x, y, z), path_color))
    parts.append(box(name + "_chx", w * 0.96, d * 0.02, 0.5, (x, y, z), water))
    parts.append(box(name + "_chy", w * 0.02, d * 0.96, 0.5, (x, y, z), water))
    parts.append(box(name + "_pool", w * 0.1, d * 0.1, 0.55, (x, y, z), water))
    if trees:
        for i in range(4):
            for j in range(4):
                tx = x + (i - 1.5) * w * 0.22 + (w * 0.05 if i >= 2 else -w * 0.05)
                ty = y + (j - 1.5) * d * 0.22 + (d * 0.05 if j >= 2 else -d * 0.05)
                parts.append(tree(f"{name}_t{i}{j}", min(w, d) * 0.035, (tx, ty, z + 0.3)))
    return join(parts, name)


def tree(name, r, loc=(0, 0, 0), color="#6F8A5C", trunk=TIMBER, kind="round"):
    x, y, z = loc
    parts = [cylinder(name + "_tr", r * 0.15, r * 1.2, (x, y, z), trunk, verts=6)]
    if kind == "palm":
        for i in range(6):
            a = math.tau * i / 6
            f = box(f"{name}_fr{i}", r * 1.4, r * 0.25, r * 0.08, (x + math.cos(a) * r * 0.6, y + math.sin(a) * r * 0.6, z + r * 2.4), color, rot_z=a)
            parts.append(f)
        parts[0] = cylinder(name + "_tr", r * 0.12, r * 2.4, (x, y, z), trunk, verts=6)
    elif kind == "cypress":
        parts.append(cylinder(name + "_c", r * 0.55, r * 3.2, (x, y, z + r * 0.4), color, verts=8, r_top=0.05))
    else:
        bpy.ops.mesh.primitive_ico_sphere_add(subdivisions=1, radius=r, location=(x, y, z + r * 1.6))
        parts.append(_finish(bpy.context.active_object, name + "_c", color))
    return join(parts, name)


def stupa(name, r, loc=(0, 0, 0), color=PLASTER, drum=0.25, rail=True, gateways=4, harmika=True, umbrellas=3, base_color=None):
    """A Buddhist stupa: a hemispherical anda on a drum, harmika and stacked umbrellas, a railing with toranas."""
    x, y, z = loc
    parts = [cylinder(name + "_drum", r * 1.08, r * drum, (x, y, z), base_color or shade(color, -0.08), verts=32)]
    parts.append(shallow_dome(name + "_anda", r, (x, y, z + r * drum), color, rise=0.92))
    top = z + r * drum + r * 0.92
    if harmika:
        parts.append(box(name + "_harmika", r * 0.3, r * 0.3, r * 0.16, (x, y, top - r * 0.02), shade(color, -0.1)))
        top += r * 0.14
    for i in range(umbrellas):
        parts.append(cylinder(f"{name}_mast{i}", r * 0.03, r * 0.16, (x, y, top + i * r * 0.16), TIMBER, verts=6))
        parts.append(cylinder(f"{name}_umb{i}", r * (0.2 - i * 0.04), r * 0.03, (x, y, top + (i + 1) * r * 0.16 - r * 0.03), shade(color, -0.15), verts=12))
    if rail:
        parts.append(lathe(name + "_rail", [(r * 1.42, 0), (r * 1.42, r * 0.22), (r * 1.38, r * 0.22), (r * 1.38, 0)], (x, y, z), BUFF_SANDSTONE, verts=40, cap_top=False, cap_bottom=False))
        parts.append(cylinder(name + "_path", r * 1.38, 0.15, (x, y, z), shade(color, -0.2), verts=40))
        for i in range(gateways):
            a = math.pi / 2 * i
            gx, gy = x + r * 1.42 * math.cos(a), y + r * 1.42 * math.sin(a)
            g = [box(f"{name}_tp{i}{s}", r * 0.05, r * 0.05, r * 0.42, (gx + s * r * 0.12 * -math.sin(a), gy + s * r * 0.12 * math.cos(a), z), BUFF_SANDSTONE) for s in (-1, 1)]
            for k in range(3):
                g.append(box(f"{name}_tb{i}{k}", r * 0.38, r * 0.04, r * 0.035, (gx, gy, z + r * (0.28 + k * 0.07)), BUFF_SANDSTONE, rot_z=a + math.pi / 2))
            parts.append(join(g, f"{name}_torana{i}"))
    return join(parts, name)


def shikhara_temple(name, w, h, loc=(0, 0, 0), color=BUFF_SANDSTONE, mandapa=True, face="E"):
    """A Hindu temple: curvilinear tower (shikhara) with an amalaka over the sanctum, a pillared hall in front."""
    x, y, z = loc
    parts = [box(name + "_plinth", w * 2.4, w * 1.3, w * 0.25, (x - w * 0.5, y, z), shade(color, -0.1))]
    base = z + w * 0.25
    prof = [(w * 0.62, 0), (w * 0.6, h * 0.25), (w * 0.52, h * 0.55), (w * 0.38, h * 0.8), (w * 0.24, h * 0.93), (w * 0.0, h * 0.95)]
    sh = lathe(name + "_shikhara", prof, (x, y, base), color, verts=16)
    for v in sh.data.vertices:  # square it off with recessed offsets
        dx, dy = v.co.x - x, v.co.y - y
        a = math.atan2(dy, dx)
        k = 1 / max(abs(math.cos(a)), abs(math.sin(a)))
        v.co.x, v.co.y = x + dx * min(k, 1.3), y + dy * min(k, 1.3)
    parts.append(sh)
    parts.append(lathe(name + "_amalaka", [(w * 0.05, 0), (w * 0.28, w * 0.06), (w * 0.3, w * 0.12), (w * 0.05, w * 0.2), (0, w * 0.45)], (x, y, base + h * 0.93), color, verts=20))
    if mandapa:
        mx = x - w * 1.0
        parts.append(box(name + "_mandapa", w * 1.0, w * 0.9, h * 0.25, (mx, y, base), color))
        parts.append(frustum(name + "_mroof", w * 1.05, w * 0.95, w * 0.3, w * 0.3, h * 0.2, (mx, y, base + h * 0.25), color))
        parts.append(arch_panel(name + "_door", w * 0.3, h * 0.2, (mx - w * 0.5 - 0.05, y, base), "W", DARK, False))
    o = join(parts, name)
    return rot(o, {"W": 0, "S": 90, "E": 180, "N": -90}[face]) if face != "W" else o


