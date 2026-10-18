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


# ---------------------------------------------------------------- fortifications (every tradition)

def wall_run(name, pts, h, t, loc=(0, 0, 0), color=RED_SANDSTONE, towers=True, tower_r=None, tower_every=40.0, merlon="box", tower_shape="round", batter=0.0):
    """A wall along a polyline [(x, y), ...] with towers at the corners and every tower_every metres."""
    x0, y0, z0 = loc
    parts = []
    tr = tower_r or t * 1.4
    for i in range(1, len(pts)):
        (ax, ay), (bx, by) = pts[i - 1], pts[i]
        L = math.hypot(bx - ax, by - ay)
        a = math.atan2(by - ay, bx - ax)
        cx, cy = (ax + bx) / 2 + x0, (ay + by) / 2 + y0
        if batter:
            seg = frustum(f"{name}_s{i}", L, t * (1 + batter), L, t, h, (0, 0, 0), color)
            seg = rot(seg, math.degrees(a))
            parts.append(move(seg, cx, cy, z0))
        else:
            parts.append(box(f"{name}_s{i}", L, t, h, (cx, cy, z0), color, rot_z=a))
        n = max(1, int(L / 2.2))
        for k in range(n):
            u = -L / 2 + (k + 0.5) * L / n
            mx, my = cx + math.cos(a) * u, cy + math.sin(a) * u
            if merlon == "round":
                parts.append(cylinder(f"{name}_m{i}_{k}", 0.55, 1.0, (mx, my, z0 + h), color, verts=6))
            elif merlon:
                parts.append(box(f"{name}_m{i}_{k}", 1.1, t * 0.9, 1.2, (mx, my, z0 + h), color, rot_z=a))
        if towers:
            tpts = [(ax, ay)] + [(ax + (bx - ax) * j / max(1, round(L / tower_every)), ay + (by - ay) * j / max(1, round(L / tower_every))) for j in range(1, max(1, round(L / tower_every)))]
            for j, (tx, ty) in enumerate(tpts):
                if tower_shape == "round":
                    parts.append(cylinder(f"{name}_t{i}_{j}", tr, h * 1.18, (tx + x0, ty + y0, z0), shade(color, -0.04), verts=12, r_top=tr * (0.9 if batter else 1.0)))
                else:
                    parts.append(box(f"{name}_t{i}_{j}", tr * 2, tr * 2, h * 1.2, (tx + x0, ty + y0, z0), shade(color, -0.04), rot_z=a))
    if towers:
        tx, ty = pts[-1]
        if tower_shape == "round":
            parts.append(cylinder(f"{name}_tend", tr, h * 1.18, (tx + x0, ty + y0, z0), shade(color, -0.04), verts=12))
        else:
            parts.append(box(f"{name}_tend", tr * 2, tr * 2, h * 1.2, (tx + x0, ty + y0, z0), shade(color, -0.04)))
    return join(parts, name)


def gatehouse(name, w, d, h, loc=(0, 0, 0), face="S", color=RED_SANDSTONE, trim=MARBLE, style="mughal"):
    """A city or fort gate: a block with a tall arched passage, flanking towers and a crown (style: mughal | gothic | sinic | roman)."""
    x, y, z = loc
    parts = [box(name + "_b", w, d, h, (0, 0, 0), color)]
    parts.append(arch_panel(name + "_arch", w * 0.32, h * 0.62, (0, -d / 2 - 0.05, 0), "S", DARK, style in ("mughal", "gothic")))
    parts.append(arch_panel(name + "_archb", w * 0.32, h * 0.62, (0, d / 2 + 0.05, 0), "N", DARK, style in ("mughal", "gothic")))
    if style == "sinic":
        parts.append(box(name + "_hall", w * 0.8, d * 0.75, h * 0.45, (0, 0, h), TIMBER_RED))
        parts.append(eaved_roof(name + "_r1", w * 0.8, d * 0.75, h * 0.3, (0, 0, h * 1.45), TILE_GREY, double=True))
    elif style == "gothic":
        for s in (-1, 1):
            parts.append(cylinder(f"{name}_tw{s}", w * 0.2, h * 1.35, (s * w * 0.45, -d * 0.2, 0), color, verts=12))
            parts.append(cylinder(f"{name}_tc{s}", w * 0.22, h * 0.45, (s * w * 0.45, -d * 0.2, h * 1.35), SLATE, verts=12, r_top=0))
        parts.append(merlons(name + "_mer", w, d, h, 0.9, 0.8, color))
    else:
        for s in (-1, 1):
            parts.append(cylinder(f"{name}_tw{s}", w * 0.17, h * 1.12, (s * w * 0.5, -d * 0.15, 0), shade(color, -0.04), verts=12))
            if style == "mughal":
                parts.append(chhatri(f"{name}_ct{s}", w * 0.13, w * 0.36, (s * w * 0.5, -d * 0.15, h * 1.12), trim))
        parts.append(merlons(name + "_mer", w * 0.7, d, h, 0.9, 0.7, color, "round" if style == "mughal" else "box"))
        if style == "mughal":
            for i in range(-2, 3):
                parts.append(chhatri(f"{name}_cs{i}", w * 0.04, w * 0.11, (i * w * 0.12, -d / 2 + 0.6, h), trim))
    o = join(parts, name)
    o = rot(o, {"S": 0, "N": 180, "E": 90, "W": -90}[face])
    return move(o, x, y, z)


# ---------------------------------------------------------------- China, Korea and Japan

def eaved_roof(name, w, d, h, loc=(0, 0, 0), color=TILE_GREY, over=None, curve=0.18, double=False, hip=True):
    """An East Asian hipped roof with wide eaves whose corners turn up; double = a second eave below."""
    x, y, z = loc
    over = over if over is not None else min(w, d) * 0.18
    W, D = w + 2 * over, d + 2 * over
    ridge = max(0.0, (W - D) * 0.5) if hip else W * 0.5
    lift = h * curve
    verts = [(-W / 2, -D / 2, lift), (W / 2, -D / 2, lift), (W / 2, D / 2, lift), (-W / 2, D / 2, lift),
             (-W * 0.42, -D * 0.42, h * 0.12), (W * 0.42, -D * 0.42, h * 0.12), (W * 0.42, D * 0.42, h * 0.12), (-W * 0.42, D * 0.42, h * 0.12),
             (-ridge / 2, 0, h), (ridge / 2, 0, h)]
    faces = [(0, 1, 5, 4), (1, 2, 6, 5), (2, 3, 7, 6), (3, 0, 4, 7), (4, 5, 9, 8), (6, 7, 8, 9), (5, 6, 9), (7, 4, 8), (3, 2, 1, 0)]
    parts = [mesh_from(name + "_r", verts, faces, (x, y, z), color)]
    parts.append(box(name + "_ridge", max(ridge, 0.5) + 0.6, 0.6, 0.5, (x, y, z + h - 0.2), shade(color, -0.25)))
    for s in (-1, 1):
        if ridge > 0.5:
            parts.append(box(f"{name}_ch{s}", 0.6, 0.9, 1.0, (x + s * (ridge / 2 + 0.2), y, z + h - 0.2), shade(color, -0.25)))
    if double:
        parts.append(eaved_roof(name + "_low", w * 1.18, d * 1.25, h * 0.35, (x, y, z - h * 0.42), color, over * 0.9, curve, False, True))
    return join(parts, name)


def east_asian_hall(name, w, d, h, loc=(0, 0, 0), wall=TIMBER_RED, roof=TILE_GREY, platform=1.2, plat_color=LIMESTONE, double=False, columns=True, roof_h=None, face="S"):
    """A timber hall on a stone platform: red columns, plastered or latticed walls, a heavy eaved roof."""
    x, y, z = loc
    parts = [box(name + "_plat", w + 4, d + 4, platform, (x, y, z), plat_color)]
    parts.append(stair(name + "_st", w * 0.3, platform, platform * 2, 4, (x, y - d / 2 - 2, z), "S", plat_color))
    zb = z + platform
    parts.append(box(name + "_walls", w * 0.94, d * 0.86, h, (x, y, zb), shade(wall, 0.25) if columns else wall))
    if columns:
        n = max(3, int(w / 3.5))
        for i in range(n + 1):
            for sy in (-1, 1):
                parts.append(cylinder(f"{name}_c{i}{sy}", 0.32, h, (x - w / 2 + w * i / n, y + sy * d / 2, zb), wall, verts=8))
        parts.append(box(name + "_lattice", w * 0.7, 0.3, h * 0.6, (x, y - d * 0.43 - 0.1, zb + h * 0.1), shade(wall, -0.25)))
    parts.append(box(name + "_beam", w + 0.6, d + 0.6, 0.6, (x, y, zb + h - 0.3), wall))
    parts.append(eaved_roof(name + "_roof", w, d, roof_h or min(w, d) * 0.42, (x, y, zb + h + 0.3), roof, double=double))
    o = join(parts, name)
    if face != "S":
        o = rot(o, {"N": 180, "E": 90, "W": -90}[face])
    return o


def pagoda(name, w, storeys, loc=(0, 0, 0), wall=PLASTER, roof=TILE_GREY, storey_h=None, sides=4, taper=0.86, spire=True, masonry=False):
    """A multi-storey pagoda: diminishing storeys, an eave at each, a bronze spire with rings (sorin)."""
    x, y, z = loc
    sh = storey_h or w * 0.42
    parts = [box(name + "_base", w * 1.3, w * 1.3, w * 0.12, (x, y, z), LIMESTONE)]
    zz = z + w * 0.12
    ww = w
    for i in range(storeys):
        if sides == 4:
            parts.append(box(f"{name}_s{i}", ww, ww, sh, (x, y, zz), wall))
        else:
            pts = [((ww / 2) * math.cos(math.pi / sides + k * math.tau / sides), (ww / 2) * math.sin(math.pi / sides + k * math.tau / sides)) for k in range(sides)]
            parts.append(prism(f"{name}_s{i}", pts, sh, (x, y, zz), wall))
        if masonry:
            parts.append(box(f"{name}_e{i}", ww * 1.18, ww * 1.18, sh * 0.12, (x, y, zz + sh), roof))
            parts.append(box(f"{name}_e{i}b", ww * 1.06, ww * 1.06, sh * 0.08, (x, y, zz + sh - sh * 0.08), shade(roof, 0.1)))
        else:
            parts.append(eaved_roof(f"{name}_r{i}", ww, ww, ww * 0.18, (x, y, zz + sh), roof, over=ww * 0.32, curve=0.3))
        zz += sh + (ww * 0.12 if not masonry else sh * 0.12)
        ww *= taper
    if spire:
        parts.append(cylinder(name + "_spire", ww * 0.08, w * 1.1, (x, y, zz - ww * 0.05), BRONZE, verts=8))
        for k in range(7):
            parts.append(cylinder(f"{name}_ring{k}", ww * 0.18, 0.18, (x, y, zz + w * 0.12 + k * w * 0.1), BRONZE, verts=10))
        parts.append(dome(name + "_jewel", ww * 0.12, (x, y, zz + w * 1.1), GILT, segments=10, rings=6))
    return join(parts, name)


def torii(name, w, h, loc=(0, 0, 0), color=LACQUER, face="S"):
    x, y, z = loc
    parts = [cylinder(f"{name}_p{s}", w * 0.06, h, (x + s * w * 0.4, y, z), color, verts=10) for s in (-1, 1)]
    parts.append(box(name + "_kasagi", w * 1.25, w * 0.1, w * 0.1, (x, y, z + h), DARK))
    parts.append(box(name + "_shimaki", w * 1.12, w * 0.09, w * 0.08, (x, y, z + h - w * 0.08), color))
    parts.append(box(name + "_nuki", w * 1.0, w * 0.06, w * 0.07, (x, y, z + h * 0.78), color))
    o = join(parts, name)
    return rot(o, {"S": 0, "N": 0, "E": 90, "W": 90}[face])


def castle_keep(name, w, d, storeys, loc=(0, 0, 0), base_h=None, wall=WHITEWASH, roof=TILE_GREY, stone=GRANITE):
    """A Japanese tenshu on a battered stone base: stacked storeys, each with eaves and gables."""
    x, y, z = loc
    bh = base_h or w * 0.5
    parts = [frustum(name + "_base", w * 1.35, d * 1.35, w * 1.05, d * 1.05, bh, (x, y, z), stone)]
    zz, ww, dd = z + bh, w, d
    for i in range(storeys):
        sh = 4.2 if i else 5.0
        parts.append(box(f"{name}_s{i}", ww, dd, sh, (x, y, zz), wall))
        parts.append(box(f"{name}_w{i}", ww * 1.01, dd * 1.01, 0.6, (x, y, zz + sh * 0.55), DARK))
        last = i == storeys - 1
        parts.append(eaved_roof(f"{name}_r{i}", ww, dd, (ww * 0.35 if last else ww * 0.16), (x, y, zz + sh), roof, over=ww * 0.12, curve=0.25, hip=not last or True))
        if not last and i % 2 == 0:
            parts.append(gable_roof(f"{name}_g{i}", ww * 0.4, dd * 0.3, ww * 0.15, (x, y - dd / 2, zz + sh), roof, overhang=0.3))
        zz += sh + ww * 0.1
        ww *= 0.8
        dd *= 0.8
    return join(parts, name)


# ---------------------------------------------------------------- Gothic, Romanesque and Byzantine Europe

def gothic_church(name, length, width, nave_h, loc=(0, 0, 0), color=LIMESTONE, roof=SLATE, towers=2, spire=False, transept=True, apse=True, rose=True, face="W",
                  flying=True, tower_h=None):
    """A cathedral facing west: twin-towered front, nave and aisles with buttresses, transept, round apse, a crossing flèche."""
    parts = []
    aisle_w, aisle_h = width * 0.22, nave_h * 0.5
    nave_w = width - 2 * aisle_w
    L = length
    parts.append(box(name + "_nave", L, nave_w, nave_h, (0, 0, 0), color))
    parts.append(gable_roof(name + "_naveroof", nave_w, L, nave_w * 0.75, (0, 0, nave_h), roof, overhang=0.4))
    # gable_roof ridge runs along Y; rotate it to run along X
    parts[-1] = rot(parts[-1], 90)
    for s in (-1, 1):
        parts.append(box(f"{name}_aisle{s}", L, aisle_w, aisle_h, (0, s * (nave_w / 2 + aisle_w / 2), 0), color))
        parts.append(box(f"{name}_aisleroof{s}", L, aisle_w * 1.05, 0.8, (0, s * (nave_w / 2 + aisle_w / 2), aisle_h), roof))
        n = max(4, int(L / 7))
        for i in range(n):
            bx = -L / 2 + L * (i + 0.5) / n
            parts.append(box(f"{name}_but{s}{i}", 1.4, 2.2, aisle_h * 1.2, (bx, s * (width / 2 + 0.6), 0), shade(color, -0.06)))
            parts.append(cylinder(f"{name}_pin{s}{i}", 0.5, 3.0, (bx, s * (width / 2 + 0.6), aisle_h * 1.2), shade(color, -0.06), verts=4, r_top=0))
            parts.append(arch_panel(f"{name}_win{s}{i}", L / n * 0.4, nave_h * 0.35, (bx, s * (nave_w / 2 + 0.05), aisle_h + 1.2), "S" if s < 0 else "N", "#4A5568", True, 0.25))
            if flying:
                fb = frustum(f"{name}_fly{s}{i}", 0.6, aisle_w + 1.2, 0.6, 0.6, 0.8, (0, 0, 0), shade(color, -0.04))
                parts.append(move(fb, bx, s * (nave_w / 2 + aisle_w / 2 + 0.3), aisle_h + nave_h * 0.2))
    if transept:
        tw = width * 1.55
        parts.append(box(name + "_transept", nave_w * 1.1, tw, nave_h, (L * 0.12, 0, 0), color))
        parts.append(gable_roof(name + "_troof", nave_w * 1.1, tw, nave_w * 0.75, (L * 0.12, 0, nave_h), roof, overhang=0.4))
        for s in (-1, 1):
            parts.append(cylinder(f"{name}_trose{s}", nave_w * 0.3, 0.4, (L * 0.12, s * tw / 2, nave_h * 0.55), "#4A5568", verts=20))
            parts[-1].rotation_euler[0] = math.pi / 2
        parts.append(cylinder(name + "_fleche", 1.2, nave_h * 0.9, (L * 0.12, 0, nave_h + nave_w * 0.7), LEAD, verts=8, r_top=0))
    if apse:
        prof_r = nave_w / 2
        a = cylinder(name + "_apse", prof_r, nave_h, (L / 2, 0, 0), color, verts=16)
        parts.append(a)
        parts.append(cylinder(name + "_apseroof", prof_r * 1.05, nave_w * 0.6, (L / 2, 0, nave_h), roof, verts=16, r_top=0.2))
        parts.append(cylinder(name + "_amb", prof_r + aisle_w, aisle_h, (L / 2, 0, 0), color, verts=16))
    th = tower_h or nave_h * 1.6
    front = -L / 2
    if towers == 2:
        for s in (-1, 1):
            parts.append(box(f"{name}_tower{s}", width * 0.34, width * 0.34, th, (front + width * 0.15, s * (width / 2 - width * 0.17), 0), color))
            parts.append(merlons(f"{name}_tm{s}", width * 0.34, width * 0.34, th, 0.6, 0.6, color))
            parts[-1] = move(parts[-1], front + width * 0.15, s * (width / 2 - width * 0.17), 0)
            for k in range(2):
                parts.append(arch_panel(f"{name}_tw{s}{k}", width * 0.06, th * 0.2, (front - 0.05, s * (width / 2 - width * 0.17) + (k - 0.5) * width * 0.12, th * 0.62), "W", DARK, True, 0.3))
            if spire:
                parts.append(cylinder(f"{name}_sp{s}", width * 0.19, th * 0.9, (front + width * 0.15, s * (width / 2 - width * 0.17), th), color, verts=8, r_top=0))
        parts.append(box(name + "_front", 2.0, width * 0.36, nave_h * 1.05, (front, 0, 0), color))
    elif towers == 1:
        parts.append(box(name + "_tower", width * 0.4, width * 0.4, th, (front, 0, 0), color))
        if spire:
            parts.append(cylinder(name + "_sp", width * 0.26, th * 0.9, (front, 0, th), roof if spire == "slate" else color, verts=8, r_top=0))
    for k, s in enumerate((-1, 0, 1)):
        parts.append(arch_panel(f"{name}_portal{k}", width * (0.14 if s else 0.18), nave_h * (0.36 if s else 0.45), (front - 1.0, s * width * 0.3, 0), "W", DARK, True, 0.6))
    if rose:
        r = cylinder(name + "_rose", nave_w * 0.32, 0.5, (front - 1.05, 0, nave_h * 0.68), "#4A5568", verts=24)
        r.rotation_euler[1] = math.pi / 2
        parts.append(r)
    o = join(parts, name)
    return rot(o, {"W": 0, "S": 90, "E": 180, "N": -90}[face])


def campanile(name, w, h, loc=(0, 0, 0), color=BRICK, cap="spire", cap_color=None, belfry=DARK):
    x, y, z = loc
    parts = [box(name + "_shaft", w, w, h, (x, y, z), color)]
    for f, (dx, dy) in (("S", (0, -w / 2)), ("N", (0, w / 2)), ("E", (w / 2, 0)), ("W", (-w / 2, 0))):
        parts.append(arcade(f"{name}_bel{f}", w * 0.8, h * 0.12, 2, (x + dx * 1.02, y + dy * 1.02, z + h * 0.8), f, belfry, False))
    parts.append(cornice(name + "_c", w, w, z + h, 0.5, 0.3, shade(color, 0.15)))
    parts[-1] = move(parts[-1], x, y, 0)
    if cap == "spire":
        parts.append(cylinder(name + "_sp", w * 0.62, h * 0.35, (x, y, z + h + 0.5), cap_color or shade(color, -0.1), verts=4, r_top=0))
        parts[-1].rotation_euler[2] = math.pi / 4
    elif cap == "pyramid":
        parts.append(cylinder(name + "_py", w * 0.72, w * 0.6, (x, y, z + h + 0.5), cap_color or TILE_RED, verts=4, r_top=0))
        parts[-1].rotation_euler[2] = math.pi / 4
    elif cap == "merlons":
        parts.append(merlons(name + "_m", w, w, z + h + 0.5, 0.7, 0.6, color))
        parts[-1] = move(parts[-1], x, y, 0)
    return join(parts, name)


def domed_basilica(name, w, d, loc=(0, 0, 0), color=PLASTER, dome_color=LEAD, main_r=None, semi=True, buttress=True, minarets=0):
    """A Byzantine domed church (Hagia Sophia type): a square core, a great dome on a ring of windows, semi-domes east and west."""
    x, y, z = loc
    h = min(w, d) * 0.42
    r = main_r or min(w, d) * 0.3
    parts = [box(name + "_core", w, d, h, (x, y, z), color)]
    parts.append(cylinder(name + "_drum", r * 1.02, r * 0.18, (x, y, z + h), color, verts=40))
    parts.append(arcade(name + "_drumwin", r * 1.6, r * 0.14, 8, (x, y - r * 1.02, z + h + 0.1), "S", DARK, False))
    parts.append(shallow_dome(name + "_dome", r, (x, y, z + h + r * 0.18), dome_color, rise=0.55, finial=True))
    if semi:
        for s in (-1, 1):
            sd = shallow_dome(f"{name}_semi{s}", r * 0.95, (0, 0, 0), dome_color, rise=0.5)
            for v in sd.data.vertices:
                if v.co.x * s < 0:
                    v.co.x = 0
            parts.append(move(sd, x + s * r * 0.95, y, z + h * 0.88))
    if buttress:
        for sx in (-1, 1):
            for sy in (-1, 1):
                parts.append(box(f"{name}_bt{sx}{sy}", w * 0.16, d * 0.16, h * 1.2, (x + sx * w * 0.36, y + sy * d * 0.42, z), shade(color, -0.06)))
    parts.append(box(name + "_narthex", w * 0.12, d * 0.9, h * 0.6, (x - w / 2 - w * 0.06, y, z), color))
    for i in range(minarets):
        sx, sy = [(-1, -1), (1, -1), (1, 1), (-1, 1)][i]
        parts.append(minaret(f"{name}_min{i}", 1.6, h * 1.9, (x + sx * w * 0.55, y + sy * d * 0.55, z), WHITEWASH, WHITEWASH, 2, "cone"))
    return join(parts, name)


def palazzo(name, w, d, h, loc=(0, 0, 0), color=STUCCO, roof=TILE_RED, storeys=3, rustic=None, court=True, loggia=False, tower=False):
    """An Italian palace: rusticated ground floor, rows of arched windows, a deep cornice, a courtyard."""
    x, y, z = loc
    parts = []
    if court:
        parts.append(courtyard_ring(name + "_ring", w, d, h, min(w, d) * 0.3, (x, y, z), color, DARK, True))
    else:
        parts.append(box(name + "_b", w, d, h, (x, y, z), color))
    parts.append(box(name + "_rust", w + 0.3, d + 0.3, h / storeys, (x, y, z), rustic or shade(color, -0.15)))
    for s in range(1, storeys):
        for f, dy in (("S", -d / 2), ("N", d / 2)):
            parts.append(arcade(f"{name}_w{s}{f}", w * 0.9, h / storeys * 0.55, max(3, int(w / 4)), (x, y + dy * 1.01, z + h / storeys * s + 0.6), f, DARK, False, 0.4))
    parts.append(cornice(name + "_corn", w, d, z + h, 0.9, 0.9, shade(color, 0.12)))
    parts[-1] = move(parts[-1], x, y, 0)
    parts.append(hip_roof(name + "_roof", w, d, min(w, d) * 0.15, (x, y, z + h + 0.9), roof, ridge=0.5, overhang=0.6))
    if tower:
        parts.append(campanile(name + "_tower", w * 0.16, h * 1.9, (x, y - d * 0.3, z), color, "merlons"))
    return join(parts, name)


