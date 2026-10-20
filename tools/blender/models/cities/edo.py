"""Edo / Tokyo landmark miniatures: Edo Castle in four states, the timber bridges, the great temples and
shrines, and the shops, theatres and quarters of the shogun's city (1457-1872).

Conventions as worldkit: metres, origin at the ground centre, +X east, +Y north, +Z up, main front to the
south (-Y). Helpers below build at the origin and are put in place with place()/grp().
"""
import math
import bpy
from mathutils import Vector
from chronokit import Model, box, cylinder, dome, join, shade, gable_roof, hip_roof, mesh_from, _finish
from worldkit import *

# ---------------------------------------------------------------- palette
WHITE_PL = "#EEEAE0"      # lime plaster
TIMBER_D = "#4A3A2C"      # dark weathered timber
TIMBER_L = "#8C6A4A"      # bridge planking
VERM = "#B4432F"          # vermilion lacquer
ROOF_T = "#5B5D61"        # grey roof tile
ROOF_LEAD = "#8A9096"     # lead / pale tile of the first keep
COPPER = "#5E8C76"        # weathered copper
BOARD = "#6E5D4B"         # shingle / board roofs
STONE = "#A19B92"         # granite ishigaki
STONE_D = "#8A847B"
EARTH = "#A38D6B"
GRASS = "#8F9D6D"
GRAVEL = "#D2C6AC"
WATER_C = "#5F878C"
INDIGO = "#2F3E5C"
BRICK_R = "#A85A42"
PINE_C = "#4E6A47"
LEAF_C = "#6F8A5C"
CHERRY = "#E4BCC2"
IZU = "#C9C6BC"
SLATE_R = "#555A62"
BLACK_W = "#2E2A27"
MUD = "#C2AE8A"           # earth-walled houses
NAMAKO = "#5D6166"


# ---------------------------------------------------------------- placement

def _sel(o):
    bpy.ops.object.select_all(action="DESELECT")
    o.select_set(True)
    bpy.context.view_layer.objects.active = o


def place(o, x=0, y=0, z=0, a=0):
    """Bake o's transform, then turn it a degrees (counter-clockwise from above) about the world origin and move it."""
    if o is None:
        return None
    _sel(o)
    bpy.ops.object.transform_apply(location=True, rotation=True, scale=True)
    if a:
        o.rotation_euler = (0, 0, math.radians(a))
        bpy.ops.object.transform_apply(rotation=True)
    if x or y or z:
        o.location = (x, y, z)
        bpy.ops.object.transform_apply(location=True)
    return o


def grp(parts, name, x=0, y=0, z=0, a=0):
    return place(join(parts, name), x, y, z, a)


def beam(name, p0, p1, r, color, verts=6):
    """A round post or pole between two points."""
    v = Vector(p1) - Vector(p0)
    bpy.ops.mesh.primitive_cylinder_add(vertices=verts, radius=r, depth=v.length, location=(Vector(p0) + Vector(p1)) / 2)
    o = bpy.context.active_object
    o.rotation_mode = "QUATERNION"
    o.rotation_quaternion = v.normalized().to_track_quat("Z", "Y")
    bpy.ops.object.transform_apply(rotation=True)
    return _finish(o, name, color)


def bar(name, p0, p1, w, h, color):
    """A square-section timber between two points (w wide, h deep)."""
    a, b = Vector(p0), Vector(p1)
    u = (b - a).normalized()
    side = u.cross(Vector((0, 0, 1)))
    side = side.normalized() if side.length > 1e-6 else Vector((0, 1, 0))
    up = side.cross(u).normalized()
    verts = []
    for p in (a, b):
        for sw, sh in ((-1, -1), (1, -1), (1, 1), (-1, 1)):
            verts.append(tuple(p + side * (sw * w / 2) + up * (sh * h / 2)))
    faces = [(0, 1, 2, 3), (7, 6, 5, 4), (0, 4, 5, 1), (1, 5, 6, 2), (2, 6, 7, 3), (3, 7, 4, 0)]
    return mesh_from(name, verts, faces, (0, 0, 0), color)


def seg(name, p0, p1, t, h, color, z=0.0):
    """A straight wall slab along p0 -> p1 (plan points)."""
    (ax, ay), (bx, by) = p0, p1
    L = math.hypot(bx - ax, by - ay)
    return box(name, L, t, h, ((ax + bx) / 2, (ay + by) / 2, z), color, rot_z=math.atan2(by - ay, bx - ax))


# ---------------------------------------------------------------- roofs

def irimoya(name, w, d, h, loc=(0, 0, 0), color=ROOF_T, over=None, gable=None, ridge=True):
    """Hip-and-gable roof (irimoya) with concave slopes; ridge along the longer side."""
    if d > w:
        o = irimoya(name, d, w, h, (0, 0, 0), color, over, gable, ridge)
        return place(o, loc[0], loc[1], loc[2], 90)
    over = over if over is not None else min(w, d) * 0.2
    W, D = w + 2 * over, d + 2 * over
    dk = D * 0.2
    g = max(W / 2 - (D / 2 - dk), W * 0.12)
    hk = h * (1 - 2 * dk / D)
    t = 0.45
    xm, ym, zm = W / 2 - t * (W / 2 - g), D / 2 - t * (D / 2 - dk), hk * 0.3
    verts = [(-W / 2, -D / 2, 0), (W / 2, -D / 2, 0), (W / 2, D / 2, 0), (-W / 2, D / 2, 0),
             (-xm, -ym, zm), (xm, -ym, zm), (xm, ym, zm), (-xm, ym, zm),
             (-g, -dk, hk), (g, -dk, hk), (g, dk, hk), (-g, dk, hk),
             (-g, 0, h), (g, 0, h)]
    faces = [(3, 2, 1, 0), (0, 1, 5, 4), (1, 2, 6, 5), (2, 3, 7, 6), (3, 0, 4, 7),
             (4, 5, 9, 8), (5, 6, 10, 9), (6, 7, 11, 10), (7, 4, 8, 11),
             (8, 9, 13, 12), (10, 11, 12, 13), (9, 10, 13), (11, 8, 12)]
    parts = [mesh_from(name + "_r", verts, faces, (0, 0, 0), color)]
    if gable:
        for s in (-1, 1):
            tv = [(s * (g + 0.06), -dk * 0.8, hk + 0.15), (s * (g + 0.06), dk * 0.8, hk + 0.15), (s * (g + 0.06), 0, h - 0.4)]
            tv += [(x - s * 0.05, y, z) for x, y, z in tv]
            parts.append(mesh_from(f"{name}_gb{s}", tv, [(0, 1, 2), (5, 4, 3), (0, 3, 4, 1), (1, 4, 5, 2), (2, 5, 3, 0)], (0, 0, 0), gable))
    if ridge:
        rh = max(0.4, h * 0.06)
        parts.append(box(name + "_ridge", 2 * g + rh, rh * 1.2, rh, (0, 0, h - rh * 0.5), shade(color, -0.3)))
        for s in (-1, 1):
            parts.append(box(f"{name}_oni{s}", rh * 1.3, rh * 1.4, rh * 1.6, (s * (g + rh * 0.3), 0, h - rh * 0.5), shade(color, -0.3)))
    return grp(parts, name, *loc)


def kirizuma(name, w, d, h, loc=(0, 0, 0), color=ROOF_T, over=0.6, ridge=True):
    """Plain gable roof with the ridge along X (eaves to the front and back)."""
    W, D = w + 2 * over, d + 2 * over
    verts = [(-W / 2, -D / 2, 0), (W / 2, -D / 2, 0), (W / 2, D / 2, 0), (-W / 2, D / 2, 0), (-W / 2, 0, h), (W / 2, 0, h)]
    faces = [(3, 2, 1, 0), (0, 1, 5, 4), (2, 3, 4, 5), (1, 2, 5), (3, 0, 4)]
    parts = [mesh_from(name + "_r", verts, faces, (0, 0, 0), color)]
    if ridge and d > 3:
        rh = max(0.25, d * 0.03)
        parts.append(box(name + "_ridge", W, rh * 1.2, rh, (0, 0, h - rh * 0.5), shade(color, -0.3)))
    return grp(parts, name, *loc)


def hafu(name, w, h, dep, loc=(0, 0, 0), a=0, roof=ROOF_T, face=WHITE_PL):
    """A chidori-hafu: a little triangular gable dormer facing south (-Y), its back running into the roof."""
    parts = [gable_roof(name + "_r", w, dep, h, (0, dep / 2, 0), roof, overhang=0.25)]
    tv = [(-w / 2 + 0.3, -0.05, 0.2), (w / 2 - 0.3, -0.05, 0.2), (0, -0.05, h - 0.35)]
    tv += [(x, y + 0.3, z) for x, y, z in tv]
    parts.append(mesh_from(name + "_f", tv, [(0, 1, 2), (5, 4, 3), (0, 3, 4, 1), (1, 4, 5, 2), (2, 5, 3, 0)], (0, 0, 0), face))
    return grp(parts, name, loc[0], loc[1], loc[2], a)


def hip_x(name, w, d, h, loc=(0, 0, 0), color=SLATE_R, ridge=0.5, overhang=0.6):
    """A Western hipped roof with its ridge along X."""
    o = hip_roof(name, d, w, h, (0, 0, 0), color, ridge=ridge, overhang=overhang)
    return place(o, loc[0], loc[1], loc[2], 90)


# ---------------------------------------------------------------- buildings

def jhall(name, w, d, h, loc=(0, 0, 0), wall=WHITE_PL, roof=ROOF_T, roof_h=None, base=0.6, base_color=STONE, kind="irimoya",
          trim=TIMBER_D, door=True, posts=None, over=None, gable=None, a=0):
    """A Japanese hall: a stone footing, plastered or lacquered walls with a dark tie-beam band, a heavy roof."""
    parts = []
    if base:
        parts.append(box(name + "_base", w + 2, d + 2, base, (0, 0, 0), base_color))
    parts.append(box(name + "_wall", w, d, h, (0, 0, base), wall))
    parts.append(box(name + "_band", w + 0.15, d + 0.15, min(0.7, h * 0.12), (0, 0, base + h * 0.82), trim))
    if door:
        parts.append(box(name + "_door", min(w * 0.3, 6), 0.3, h * 0.62, (0, -d / 2 - 0.05, base), DARK))
    if posts:
        n = max(2, int(w / 3.6))
        for i in range(n + 1):
            for s in (-1, 1):
                parts.append(cylinder(f"{name}_p{i}{s}", 0.28, h, (-w / 2 - 1 + (w + 2) * i / n, s * (d / 2 + 1), base), posts, verts=6))
        parts.append(box(name + "_ver", w + 2.6, d + 2.6, 0.3, (0, 0, base), shade(TIMBER_L, -0.1)))
    rh = roof_h or min(w, d) * 0.45
    if kind == "irimoya":
        parts.append(irimoya(name + "_roof", w, d, rh, (0, 0, base + h), roof, over=over, gable=gable))
    elif kind == "hip":
        parts.append(eaved_roof(name + "_roof", w, d, rh, (0, 0, base + h), roof, over=over if over is not None else min(w, d) * 0.15, curve=0.12))
    else:
        parts.append(kirizuma(name + "_roof", w, d, rh, (0, 0, base + h), roof, over=over if over is not None else 0.8))
    return grp(parts, name, loc[0], loc[1], loc[2], a)


def romon(name, w, d, h1, h2, loc=(0, 0, 0), color=VERM, roof=ROOF_T, a=0, side=WHITE_PL):
    """A two-storey temple gate (sanmon / niomon): a post-framed lower storey with closed side bays, a pent roof,
    a railed upper storey and a big hip-and-gable roof."""
    parts = []
    parts.append(box(name + "_base", w + 1.5, d + 1.5, 0.6, (0, 0, 0), STONE))
    n = 4 if w > 14 else 3
    for i in range(n + 1):
        for s in (-1, 1):
            parts.append(cylinder(f"{name}_p{i}{s}", 0.45, h1, (-w / 2 + w * i / n, s * d / 2 * 0.85, 0.6), color, verts=8))
    bay = w / n
    for s in (-1, 1):
        parts.append(box(f"{name}_side{s}", bay * 0.92, d * 0.8, h1 * 0.85, (s * (w / 2 - bay / 2), 0, 0.6), color))
        parts.append(box(f"{name}_lat{s}", bay * 0.6, 0.2, h1 * 0.5, (s * (w / 2 - bay / 2), -d * 0.4 - 0.1, 1.8), shade(color, -0.45)))
    parts.append(box(name + "_tie", w + 0.4, d * 0.9, 0.8, (0, 0, h1 - 0.2), color))
    parts.append(eaved_roof(name + "_r1", w, d, w * 0.11, (0, 0, h1 + 0.4), roof, over=d * 0.32, curve=0.15))
    z2 = h1 + 0.4 + w * 0.06
    parts.append(box(name + "_bal", w * 0.92, d * 0.86, 0.9, (0, 0, z2), shade(color, -0.15)))
    parts.append(box(name + "_up", w * 0.84, d * 0.72, h2, (0, 0, z2), color))
    parts.append(box(name + "_upw", w * 0.5, 0.2, h2 * 0.5, (0, -d * 0.36 - 0.1, z2 + h2 * 0.25), shade(color, -0.45)))
    parts.append(irimoya(name + "_r2", w * 0.84, d * 0.72, d * 0.95, (0, 0, z2 + h2), roof, over=d * 0.3))
    return grp(parts, name, loc[0], loc[1], loc[2], a)


def yakuimon(name, w, d, h, loc=(0, 0, 0), color=VERM, roof=ROOF_T, a=0, door=DARK):
    """A single-storey roofed gate on four posts (yakui-mon / munamon) with a gable roof."""
    parts = []
    for s in (-1, 1):
        parts.append(box(f"{name}_mp{s}", 0.9, 0.9, h, (s * w * 0.38, -d * 0.15, 0), color))
        parts.append(box(f"{name}_bp{s}", 0.6, 0.6, h * 0.85, (s * w * 0.38, d * 0.35, 0), color))
    parts.append(box(name + "_lintel", w * 0.95, 1.0, 0.8, (0, -d * 0.15, h - 0.8), color))
    parts.append(box(name + "_doors", w * 0.7, 0.3, h * 0.82, (0, -d * 0.1, 0), door))
    parts.append(kirizuma(name + "_roof", w, d, d * 0.42, (0, 0, h), roof, over=1.0))
    return grp(parts, name, loc[0], loc[1], loc[2], a)


def gongen(name, w, d, loc=(0, 0, 0), wall=VERM, roof=COPPER, base=1.0, a=0):
    """A gongen-zukuri shrine: wide worship hall in front, a linking chamber, the sanctuary behind."""
    parts = [box(name + "_base", w + 4, d + 4, base, (0, 0, 0), STONE)]
    hd = d * 0.38
    parts.append(box(name + "_hai", w, hd, 6, (0, -d / 2 + hd / 2, base), wall))
    parts.append(box(name + "_haib", w + 0.2, hd + 0.2, 0.6, (0, -d / 2 + hd / 2, base + 5), BLACK_W))
    parts.append(box(name + "_haid", w * 0.5, 0.3, 4, (0, -d / 2 - 0.05, base), DARK))
    parts.append(irimoya(name + "_hair", w, hd, hd * 0.75, (0, -d / 2 + hd / 2, base + 6), roof, gable=GILT))
    parts.append(hafu(name + "_haf", w * 0.36, hd * 0.32, hd * 0.6, (0, -d / 2 - hd * 0.2, base + 6.2), roof=roof, face=GILT))
    parts.append(box(name + "_ishi", w * 0.38, d * 0.26, 5, (0, -d * 0.02, base), wall))
    parts.append(gable_roof(name + "_ishir", w * 0.38, d * 0.26, 3.2, (0, -d * 0.02, base + 5), roof, overhang=0.8))
    bd = d * 0.38
    parts.append(box(name + "_hon", w * 0.72, bd, 7, (0, d / 2 - bd / 2, base), wall))
    parts.append(box(name + "_honb", w * 0.72 + 0.2, bd + 0.2, 0.6, (0, d / 2 - bd / 2, base + 6), BLACK_W))
    parts.append(irimoya(name + "_honr", w * 0.72, bd, bd * 0.8, (0, d / 2 - bd / 2, base + 7), roof, gable=GILT))
    return grp(parts, name, loc[0], loc[1], loc[2], a)


def kura(name, w, d, h, loc=(0, 0, 0), a=0, wall=WHITE_PL, roof=ROOF_T, ridge_y=False):
    """A fireproof storehouse: thick white plaster, a dark namako base, a heavy tile roof, one dark door."""
    parts = [box(name + "_w", w, d, h, (0, 0, 0), wall),
             box(name + "_b", w + 0.2, d + 0.2, h * 0.28, (0, 0, 0), NAMAKO),
             box(name + "_door", min(2.2, w * 0.3), 0.3, h * 0.45, (0, -d / 2 - 0.05, 0), BLACK_W)]
    rh = min(w, d) * 0.32
    if ridge_y:
        parts.append(gable_roof(name + "_r", w, d, rh, (0, 0, h), roof, overhang=0.5))
    else:
        parts.append(kirizuma(name + "_r", w, d, rh, (0, 0, h), roof, over=0.5))
    return grp(parts, name, loc[0], loc[1], loc[2], a)


def shop_row(name, n, unit, d, loc=(0, 0, 0), a=0, h1=3.4, h2=2.4, wall=MUD, roof=ROOF_T, front=TIMBER_D, noren=None,
             storeys=2, lattice=None, seed=0):
    """A street front of n machiya: shop floor with a dark lattice or open front, a pent eave, a low upper floor,
    a gable roof with its eaves to the street. lattice = colour of a harimise (display lattice)."""
    parts = []
    for i in range(n):
        x = -n * unit / 2 + (i + 0.5) * unit
        k = ((i * 7 + seed * 3) % 5) / 10.0
        hh1 = h1 + k * 0.4
        parts.append(box(f"{name}_g{i}", unit - 0.25, d, hh1, (x, 0, 0), wall))
        parts.append(box(f"{name}_f{i}", unit * 0.82, 0.25, hh1 * 0.72, (x, -d / 2 - 0.05, 0.15), lattice or front))
        parts.append(box(f"{name}_e{i}", unit, 1.5, 0.3, (x, -d / 2 - 0.55, hh1 - 0.3), roof))
        if noren:
            parts.append(box(f"{name}_n{i}", unit * 0.5, 0.15, 1.0, (x, -d / 2 - 0.25, hh1 - 1.4), noren))
        top = hh1
        if storeys == 2:
            parts.append(box(f"{name}_u{i}", unit - 0.25, d * 0.82, h2, (x, d * 0.09, hh1), wall))
            parts.append(box(f"{name}_uw{i}", unit * 0.7, 0.2, h2 * 0.45, (x, -d * 0.32, hh1 + h2 * 0.3), lattice or front))
            top = hh1 + h2
            rd = d * 0.82
            ry = d * 0.09
        else:
            rd, ry = d, 0
        parts.append(kirizuma(f"{name}_r{i}", unit - 0.2, rd, rd * 0.32, (x, ry, top), shade(roof, ((i * 2 + seed) % 3 - 1) * 0.08), over=0.5, ridge=False))
    return grp(parts, name, loc[0], loc[1], loc[2], a)


def nagaya(name, length, d, loc=(0, 0, 0), a=0, h=3.0, doors=None, wall=MUD, roof=BOARD):
    """A back-alley tenement row: one long single-storey block under a single board roof, one door per household."""
    n = doors or max(2, int(length / 2.7))
    parts = [box(name + "_w", length, d, h, (0, 0, 0), wall)]
    for i in range(n):
        x = -length / 2 + (i + 0.5) * length / n
        parts.append(box(f"{name}_d{i}", length / n * 0.45, 0.2, h * 0.7, (x, -d / 2 - 0.05, 0), TIMBER_D))
        parts.append(box(f"{name}_s{i}", length / n * 0.3, 0.2, 0.9, (x + length / n * 0.3, -d / 2 - 0.05, 1.3), shade(MUD, 0.3)))
    parts.append(kirizuma(name + "_r", length, d, d * 0.3, (0, 0, h), roof, over=0.5))
    return grp(parts, name, loc[0], loc[1], loc[2], a)


def dobei(name, p0, p1, h=2.4, t=0.8, color=WHITE_PL, cap=ROOF_T, z=0.0):
    """A plastered earthen wall with a tile cap."""
    return join([seg(name + "_w", p0, p1, t, h, color, z), seg(name + "_c", p0, p1, t + 0.8, 0.45, cap, z + h)], name)


def fence(name, p0, p1, h=2.4, color=TIMBER_D, z=0.0, every=6.0):
    """A board fence or palisade with posts."""
    (ax, ay), (bx, by) = p0, p1
    L = math.hypot(bx - ax, by - ay)
    parts = [seg(name + "_b", p0, p1, 0.35, h, color, z)]
    n = max(1, int(L / every))
    for i in range(n + 1):
        t = i / n
        parts.append(cylinder(f"{name}_p{i}", 0.3, h + 0.6, (ax + (bx - ax) * t, ay + (by - ay) * t, z), shade(color, -0.2), verts=5))
    return join(parts, name)


def pine(name, s=1.0, loc=(0, 0, 0), color=PINE_C, seed=0):
    """A Japanese black pine: a leaning trunk and flat cloud-pruned tiers."""
    x, y, z = loc
    lean = 0.6 * s * (1 if seed % 2 else -1)
    parts = [beam(name + "_t", (x, y, z + 0.35 * s), (x + lean, y, z + 6.2 * s), 0.3 * s, TIMBER_D, verts=5)]
    tiers = [(lean, 0, 6.0, 2.6), (1.4 * (1 if seed % 3 else -1), 0.7, 4.3, 1.9), (-1.2, -0.9 * (1 if seed % 2 else -1), 5.1, 1.7)]
    for i, (dx, dy, zz, r) in enumerate(tiers):
        parts.append(cylinder(f"{name}_c{i}", r * s, 0.9 * s, (x + dx * s, y + dy * s, z + zz * s), color, verts=7, r_top=r * s * 0.55))
    return join(parts, name)


def leafy(name, r, loc, color=LEAF_C):
    return tree(name, r, loc, color)


def lantern(name, loc, s=1.0, color=STONE):
    """A stone toro."""
    x, y, z = loc
    return join([cylinder(name + "_b", 0.35 * s, 1.2 * s, (x, y, z), color, verts=6),
                 box(name + "_l", 0.8 * s, 0.8 * s, 0.6 * s, (x, y, z + 1.2 * s), shade(color, 0.15)),
                 cylinder(name + "_c", 0.75 * s, 0.4 * s, (x, y, z + 1.8 * s), color, verts=6, r_top=0.1 * s)], name)


def boat(name, L, W, loc=(0, 0, 0), a=0, color=TIMBER_L, cargo=None, roofed=False):
    pts = [(-L / 2, -W / 2), (L * 0.32, -W / 2), (L / 2, 0), (L * 0.32, W / 2), (-L / 2, W / 2)]
    parts = [prism(name + "_h", pts, 0.7, (0, 0, 0), color)]
    if cargo:
        parts.append(box(name + "_cg", L * 0.45, W * 0.7, 0.7, (-L * 0.05, 0, 0.7), cargo))
    if roofed:
        parts.append(box(name + "_cab", L * 0.45, W * 0.85, 1.4, (-L * 0.05, 0, 0.7), shade(color, 0.2)))
        parts.append(kirizuma(name + "_cr", L * 0.5, W * 0.9, 0.6, (-L * 0.05, 0, 2.1), BOARD, over=0.2, ridge=False))
    return grp(parts, name, loc[0], loc[1], loc[2], a)


# ---------------------------------------------------------------- castle parts

def ishigaki(name, w, d, h, loc=(0, 0, 0), color=STONE, batter=0.35, top=None):
    """A battered dry-stone platform (w x d at the top), optional top surface colour."""
    b = h * batter
    parts = [frustum(name + "_s", w + 2 * b, d + 2 * b, w, d, h, (0, 0, 0), color)]
    if top:
        parts.append(box(name + "_top", w - 0.2, d - 0.2, 0.15, (0, 0, h), top))
    return grp(parts, name, *loc)


def ishigaki_run(name, p0, p1, h, t, z=0.0, color=STONE, batter=0.3):
    (ax, ay), (bx, by) = p0, p1
    L = math.hypot(bx - ax, by - ay)
    o = frustum(name, L, t + 2 * h * batter, L, t, h, (0, 0, 0), color)
    return place(o, (ax + bx) / 2, (ay + by) / 2, z, math.degrees(math.atan2(by - ay, bx - ax)))


def tamon(name, p0, p1, z, t=7.0, h=4.2, wall=WHITE_PL, roof=ROOF_T):
    """A tamon-yagura: a long white single-storey defensive building along the top of a stone wall."""
    (ax, ay), (bx, by) = p0, p1
    L = math.hypot(bx - ax, by - ay)
    parts = [box(name + "_w", L, t, h, (0, 0, 0), wall),
             box(name + "_win", L * 0.96, t + 0.12, 0.6, (0, 0, h * 0.45), DARK),
             box(name + "_base", L, t + 0.1, 0.8, (0, 0, 0), NAMAKO),
             kirizuma(name + "_r", L, t, t * 0.38, (0, 0, h), roof, over=0.7)]
    return grp(parts, name, (ax + bx) / 2, (ay + by) / 2, z, math.degrees(math.atan2(by - ay, bx - ax)))


def yagura(name, w, d, storeys=3, loc=(0, 0, 0), a=0, base_h=0.0, wall=WHITE_PL, roof=ROOF_T, stone=STONE):
    """A castle turret: stacked white storeys, a dark window band each, eaves at each, a hip-and-gable top, chidori gables."""
    parts = []
    z = 0.0
    if base_h:
        parts.append(frustum(name + "_st", w * 1.25 + base_h * 0.6, d * 1.25 + base_h * 0.6, w * 1.2, d * 1.2, base_h, (0, 0, 0), stone))
        z = base_h
    ww, dd = w, d
    for i in range(storeys):
        sh = 4.6 if i == 0 else 3.9
        last = i == storeys - 1
        parts.append(box(f"{name}_s{i}", ww, dd, sh, (0, 0, z), wall))
        parts.append(box(f"{name}_w{i}", ww + 0.12, dd + 0.12, 0.7, (0, 0, z + sh * 0.42), DARK))
        if last:
            parts.append(irimoya(f"{name}_r{i}", ww, dd, min(ww, dd) * 0.5, (0, 0, z + sh), roof, over=min(ww, dd) * 0.16, gable=WHITE_PL))
        else:
            rh = min(ww, dd) * 0.2
            parts.append(eaved_roof(f"{name}_r{i}", ww, dd, rh, (0, 0, z + sh), roof, over=min(ww, dd) * 0.16, curve=0.25))
            if i % 2 == 0:
                parts.append(hafu(f"{name}_h{i}", ww * 0.42, rh * 1.6, dd * 0.3, (0, -dd / 2 - min(ww, dd) * 0.05, z + sh + 0.1), roof=roof))
        z += sh + min(ww, dd) * 0.08
        ww *= 0.8
        dd *= 0.8
    return grp(parts, name, loc[0], loc[1], loc[2], a)


def tenshu(name, w, d, loc=(0, 0, 0), storeys=5, wall=WHITE_PL, roof=ROOF_LEAD):
    """The great keep: five diminishing storeys, eaves and chidori gables on each, a top hip-and-gable roof with
    gilt shachihoko at the ridge ends."""
    parts = []
    z = 0.0
    ww, dd = w, d
    hs = [7.2, 6.4, 5.8, 5.4, 5.2, 5.0, 5.0][:storeys]
    for i, sh in enumerate(hs):
        last = i == storeys - 1
        parts.append(box(f"{name}_s{i}", ww, dd, sh, (0, 0, z), wall))
        for k in range(2):
            parts.append(box(f"{name}_w{i}{k}", ww + 0.14, dd + 0.14, 0.9, (0, 0, z + sh * (0.3 + 0.35 * k)), DARK))
        parts.append(box(f"{name}_b{i}", ww + 0.1, dd + 0.1, 0.6, (0, 0, z), BLACK_W))
        if last:
            rh = min(ww, dd) * 0.55
            parts.append(irimoya(f"{name}_r{i}", ww, dd, rh, (0, 0, z + sh), roof, over=min(ww, dd) * 0.2, gable=WHITE_PL))
            o_ = min(ww, dd) * 0.2
            gx = max((max(ww, dd) + 2 * o_) / 2 - 0.3 * (min(ww, dd) + 2 * o_), (max(ww, dd) + 2 * o_) * 0.12)
            for s in (-1, 1):
                parts.append(box(f"{name}_shachi{s}", 0.9, 0.9, 2.6, (s * gx, 0, z + sh + rh - 0.3), GILT))
        else:
            rh = min(ww, dd) * 0.17
            parts.append(eaved_roof(f"{name}_r{i}", ww, dd, rh, (0, 0, z + sh), roof, over=min(ww, dd) * 0.13, curve=0.3))
            if i in (0, 2):
                for f in (0, 180):
                    off = dd / 2 + min(ww, dd) * 0.04
                    hf = hafu(f"{name}_h{i}{f}", ww * 0.36, rh * 1.9, dd * 0.28, (0, -off, z + sh), roof=roof)
                    parts.append(place(hf, 0, 0, 0, f))
            if i in (1, 3):
                for f in (90, -90):
                    off = ww / 2 + min(ww, dd) * 0.04
                    hf = hafu(f"{name}_h{i}{f}", dd * 0.36, rh * 1.9, ww * 0.28, (0, -off, z + sh), roof=roof)
                    parts.append(place(hf, 0, 0, 0, f))
        z += sh + min(ww, dd) * 0.07
        ww *= 0.84
        dd *= 0.84
    return grp(parts, name, *loc)


def koraimon(name, w, h, loc=(0, 0, 0), a=0, color=BLACK_W, roof=ROOF_T):
    """A korai-mon: the outer gate of a masugata, two heavy posts, a small roof over the beam, dark doors."""
    parts = []
    for s in (-1, 1):
        parts.append(box(f"{name}_p{s}", 1.0, 1.0, h, (s * w / 2, 0, 0), color))
        parts.append(box(f"{name}_bp{s}", 0.6, 0.6, h * 0.7, (s * w / 2, 2.4, 0), color))
        parts.append(kirizuma(f"{name}_sr{s}", 1.6, 2.6, 0.7, (s * w / 2, 1.6, h * 0.7), roof, over=0.3, ridge=False))
    parts.append(box(name + "_beam", w + 2.2, 0.9, 0.9, (0, 0, h - 0.9), color))
    parts.append(box(name + "_doors", w - 1, 0.4, h - 1.2, (0, 0.2, 0), shade(color, 0.12)))
    parts.append(kirizuma(name + "_r", w + 3, 2.6, 1.3, (0, 0, h), roof, over=0.4))
    return grp(parts, name, loc[0], loc[1], loc[2], a)


def masugata(name, s=40.0, loc=(0, 0, 0), a=0, wall_h=6.0, stone=STONE, roof=ROOF_T, inner="W"):
    """A masugata gate: a square stone-walled court entered through a korai-mon on its outer (south) side,
    left through a watari-yagura (a gatehouse bridging the wall) on the inner side, at right angles."""
    parts = [box(name + "_court", s, s, 0.3, (0, 0, 0), GRAVEL)]
    t = 7.0
    hs = s / 2
    gap = 7.0
    # outer wall (south) split by the korai-mon
    for k in (-1, 1):
        parts.append(ishigaki_run(f"{name}_s{k}", (k * gap / 2, -hs), (k * hs, -hs), wall_h * 0.6, 3.0, 0, stone))
        parts.append(dobei(f"{name}_sd{k}", (k * gap / 2, -hs), (k * hs, -hs), 2.0, 0.9, z=wall_h * 0.6))
    parts.append(koraimon(name + "_kor", gap - 1, 6.5, (0, -hs, 0)))
    sx = -1 if inner == "W" else 1
    # far side wall (north) and the other side
    parts.append(ishigaki_run(name + "_n", (-hs, hs), (hs, hs), wall_h, t, 0, stone))
    parts.append(tamon(name + "_nt", (-hs, hs), (hs, hs), wall_h, t * 0.9, 3.8, roof=roof))
    parts.append(ishigaki_run(name + "_o", (-sx * hs, -hs), (-sx * hs, hs), wall_h, t, 0, stone))
    parts.append(dobei(name + "_od", (-sx * hs, -hs), (-sx * hs, hs), 2.0, 0.9, z=wall_h))
    # inner side: watari-yagura over an opening
    for k in (-1, 1):
        parts.append(ishigaki_run(f"{name}_i{k}", (sx * hs, k * gap / 2), (sx * hs, k * hs), wall_h, t, 0, stone))
    parts.append(box(name + "_idoor", 1.0, gap, wall_h * 0.85, (sx * hs, 0, 0), BLACK_W))
    wy = [box(name + "_wy", t + 1, s + 2, 4.6, (0, 0, 0), WHITE_PL),
          box(name + "_wyw", t + 1.12, s * 0.9, 0.7, (0, 0, 2.0), DARK),
          box(name + "_wyb", t + 1.1, s + 2.1, 0.7, (0, 0, 0), NAMAKO),
          place(kirizuma(name + "_wyr", s + 2, t + 1, (t + 1) * 0.4, (0, 0, 0), roof, over=0.9), 0, 0, 4.6, 90)]
    parts.append(grp(wy, name + "_watari", sx * hs, 0, wall_h))
    return grp(parts, name, loc[0], loc[1], loc[2], a)


# ---------------------------------------------------------------- Edo Castle

def edo_castle(v="1800"):
    if v == "1460":
        return dokan_castle()
    m = Model("edo-castle" + ("" if v == "1800" else "-" + v))
    burned = v == "1872"
    # ground, moats and the stone platforms of the baileys
    m.add(0, box("ground", 800, 700, 0.4, (0, 0, 0), GRASS), "ishigaki")
    for nm, (x, y, w, d) in dict(hakucho=(101, 25, 18, 300), hasuike=(-150, -292, 450, 22), ninomaru=(271, 0, 18, 470),
                                  ).items():
        m.add(0, box("moat_" + nm, w, d, 0.5, (x, y, 0), WATER_C))
    top = GRASS if burned else GRAVEL
    m.add(0, ishigaki("honmaru", 440, 560, 10, (-150, 40, 0), STONE, top=top))
    m.add(0, ishigaki("tenshudai", 45, 41, 14, (-120, 250, 10), STONE_D, batter=0.18, top=GRAVEL))
    m.add(0, ishigaki("ninomaru", 140, 480, 5, (187, 10, 0), STONE, top=GRASS if burned else GRAVEL))
    m.add(0, box("sannomaru", 112, 660, 1.0, (340, 0, 0.3), GRAVEL))
    # stage 1: walls, gates and turrets
    zt = 10.0
    W0, W1, S0, S1 = -366.4, 66.4, -236.4, 316.4      # tamon line, set in from the honmaru's edge
    runs = [((W0 + 12, S0), (W1 - 34, S0)), ((W1, S0 + 40), (W1, 90)), ((W1, 140), (W1, S1 - 14)),
            ((W1 - 14, S1), (-98, S1)), ((-142, S1), (W0 + 14, S1)), ((W0, S1 - 14), (W0, 120)), ((W0, 60), (W0, S0 + 14))]
    for i, (p0, p1) in enumerate(runs):
        if v == "1610" and i in (1, 5):
            m.add(1, dobei(f"hon_dobei{i}", p0, p1, 2.4, 1.0, z=zt))
        else:
            m.add(1, tamon(f"hon_tamon{i}", p0, p1, zt), "walls")
    m.add(1, yagura("fujimi", 18, 15, 3, (W1 - 18, S0 + 18, zt)))
    for i, (x, y) in enumerate([(W0 + 12, S1 - 12), (W0 + 12, S0 + 12), (W1 - 10, S1 - 10)]):
        m.add(1, yagura(f"hon_yagura{i}", 13, 11, 2, (x, y, zt)))
    for i, (x, y) in enumerate([(W1, 115), (W0, 90)]):
        m.add(1, yakuimon(f"hon_gate{i}", 9, 6, 5.5, (x, y, zt), BLACK_W, a=90))
    # ninomaru
    zn = 5.0
    nx0, nx1, ny0, ny1 = 117, 257, -230, 250
    m.add(1, dobei("ni_dobei_e", (nx1, ny0 + 12), (nx1, ny1 - 12), z=zn))
    m.add(1, dobei("ni_dobei_n", (nx0 + 10, ny1), (nx1 - 12, ny1), z=zn))
    m.add(1, dobei("ni_dobei_s", (nx0 + 10, ny0), (nx1 - 12, ny0), z=zn))
    ny = [(nx1 - 8, ny1 - 8), (nx1 - 8, ny0 + 8)] + ([] if v == "1610" else [(nx0 + 8, ny0 + 8), (nx1 - 8, 10)])
    for i, (x, y) in enumerate(ny):
        m.add(1, yagura(f"ni_yagura{i}", 11, 9, 2, (x, y, zn)))
    # sannomaru: the east wall on the Ote moat and the masugata gates
    m.add(1, masugata("otemon", 44, (372, -40, 0), a=90, inner="E"))
    if v != "1610":
        m.add(1, masugata("hirakawamon", 40, (330, 322, 0), a=180, inner="E"))
    m.add(1, masugata("kikyomon", 36, (340, -322, 0), a=0, inner="W"))
    for i, (p0, p1) in enumerate([((396, -300), (396, -64)), ((396, -16), (396, 300))]):
        m.add(1, ishigaki_run(f"san_wall{i}", p0, p1, 4.0, 4.0))
        m.add(1, dobei(f"san_dobei{i}", p0, p1, 2.2, 0.9, z=4.0))
    # stage 2: palaces, offices, gardens
    if not burned:
        halls = [(-200, -175, 60, 40), (-140, -170, 60, 30), (-260, -165, 60, 36), (-180, -128, 40, 50), (-110, -120, 40, 40), (-240, -112, 50, 40),
                 (-190, -72, 70, 40), (-120, -62, 40, 50), (-262, -62, 44, 40), (-62, -82, 44, 30), (-200, 8, 80, 40), (-122, 20, 60, 36),
                 (-282, 20, 40, 50), (-200, 58, 50, 40), (-130, 80, 50, 40), (-272, 92, 50, 40), (-200, 118, 60, 36), (-62, 62, 40, 60),
                 (-282, 160, 40, 40), (-200, 168, 44, 40), (-30, -150, 40, 30), (-300, 230, 40, 30), (-30, 240, 40, 30)]
        for i, (x, y, w, d) in enumerate(halls):
            m.add(2, jhall(f"palace{i}", w, d, 5.0, (x, y, zt), "#E8E2D2", ROOF_T, roof_h=min(w, d) * 0.36, base=0.8, base_color=STONE_D,
                           gable=WHITE_PL if i % 3 == 0 else None, door=False), "palaces")
        for i, (p0, p1) in enumerate([((-62, -67), (-62, 32)), ((-82, 62), (-105, 80)), ((-50, -135), (-62, -97)), ((-282, 185), (-300, 215))]):
            m.add(2, seg(f"corr{i}", p0, p1, 5, 3.6, "#E8E2D2", zt), "palaces")
        for i, (x, y, w, d) in enumerate([(185, 70, 60, 40), (175, -50, 50, 34), (215, 160, 40, 28)]):
            m.add(2, jhall(f"nipalace{i}", w, d, 4.6, (x, y, zn), "#E8E2D2", ROOF_T, roof_h=min(w, d) * 0.36, base=0.6, door=False), "palaces")
    m.add(2, box("ni_pond", 40, 26, 0.3, (200, -150, zn), WATER_C), "palaces")
    for i, (x, y, w, d) in enumerate([(335, 70, 12, 56), (325, -130, 40, 12), (335, 180, 12, 40)]):
        m.add(2, jhall(f"bansho{i}", w, d, 3.6, (x, y, 1.3), "#E2D8C4", ROOF_T, roof_h=min(w, d) * 0.4, base=0, kind="kirizuma" if w > d else "irimoya", door=False))
    rnd = [(-350, 290), (-340, -200), (40, 280), (-20, -210), (-120, -210), (-330, 10), (150, -200), (230, -110), (140, 120), (240, 220),
           (150, 230), (320, 260), (360, 120), (310, -230), (370, -170), (300, 20), (-260, 290), (60, -100), (-60, 290), (175, -170)]
    for i, (x, y) in enumerate(rnd):
        z = zt if x < 75 else (zn if x < 262 else 1.3)
        m.add(2, pine(f"pine{i}", 1.9, (x, y, z), seed=i))
    if v == "1610":
        m.add(3, tenshu("keep", 40, 36, (-120, 250, 24)), "keep")
    return m


def dokan_castle():
    m = Model("edo-castle-1460")
    m.add(0, box("ground", 800, 700, 0.4, (0, 0, 0), GRASS), "earthworks")
    bank = "#8F8A5E"
    encl = [("nejiro", -190, 60, 230, 260, 9.0), ("nakajiro", 45, 20, 190, 300, 6.0), ("sotojiro", 255, 0, 150, 420, 3.0)]
    for nm, x, y, w, d, h in encl:
        m.add(0, frustum(nm, w + 2 * h * 0.9, d + 2 * h * 0.9, w, d, h, (x, y, 0), bank))
        m.add(0, box(nm + "_top", w - 1, d - 1, 0.12, (x, y, h), "#9AA674"))
    m.add(0, box("drymoat1", 10, 320, 0.5, (-61, 40, 0), "#6D5A44"))
    m.add(0, box("drymoat2", 16, 360, 0.5, (162, 10, 0), "#6D5A44"))
    for i, (x, y) in enumerate([(-61, -130), (162, -175)]):
        m.add(0, box(f"causeway{i}", 22, 10, 0.6, (x, y, 0), EARTH))
    for nm, x, y, w, d, h in encl:
        x0, x1, y0, y1 = x - w / 2 + 2, x + w / 2 - 2, y - d / 2 + 2, y + d / 2 - 2
        pts = [(x0, y0), (x1, y0), (x1, y1), (x0, y1), (x0, y0)]
        m.add(1, fence(f"{nm}_pal0a", (x0, y0), (x - 5, y0), 2.6, "#5A4634", h, 8.0), "palisades")
        m.add(1, fence(f"{nm}_pal0b", (x + 5, y0), (x1, y0), 2.6, "#5A4634", h, 8.0))
        for i in range(1, 4):
            m.add(1, fence(f"{nm}_pal{i}", pts[i], pts[i + 1], 2.6, "#5A4634", h, 8.0))
        m.add(1, yakuimon(nm + "_gate", 7, 4, 4.4, (x, y0, h), "#5A4634", BOARD))
    halls = [(-215, 40, 42, 22, 9.0, THATCH), (-140, 110, 28, 14, 9.0, THATCH), (-150, -20, 24, 12, 9.0, BOARD), (-250, -30, 20, 12, 9.0, BOARD),
             (-180, 90, 18, 10, 9.0, BOARD), (40, 60, 32, 14, 6.0, BOARD), (20, -40, 26, 12, 6.0, BOARD), (90, 100, 20, 10, 6.0, THATCH),
             (100, -90, 30, 10, 6.0, BOARD), (-10, 120, 18, 10, 6.0, THATCH), (250, 80, 16, 8, 3.0, THATCH), (240, -60, 14, 8, 3.0, THATCH),
             (265, 160, 16, 8, 3.0, BOARD), (230, -150, 24, 8, 3.0, THATCH), (280, 0, 12, 8, 3.0, THATCH), (230, 20, 12, 8, 3.0, BOARD)]
    for i, (x, y, w, d, z, r) in enumerate(halls):
        m.add(2, jhall(f"hall{i}", w, d, 3.4, (x, y, z), "#A88E6C", r, roof_h=d * 0.65, base=0.4, base_color=EARTH, door=True), "halls")
    tw = [box("tw_s0", 9, 9, 4.2, (0, 0, 0), "#A88E6C"), eaved_roof("tw_r0", 9, 9, 2.2, (0, 0, 4.2), THATCH, over=1.6, curve=0.1),
          box("tw_s1", 6.5, 6.5, 3.4, (0, 0, 5.4), "#A88E6C"), irimoya("tw_r1", 6.5, 6.5, 4.5, (0, 0, 8.8), THATCH, over=1.4)]
    m.add(2, grp(tw, "seishoken", -265, 150, 9))
    import random
    rng = random.Random(1457)
    k = 0
    for cx, cy, n, sp in [(-300, 250, 9, 50), (-340, -180, 7, 40), (-100, -260, 6, 45), (60, 260, 7, 50), (200, 290, 5, 40), (350, 250, 4, 30),
                          (360, -250, 5, 35), (130, -260, 5, 40), (-330, 60, 4, 25), (-250, 120, 3, 25), (60, -110, 3, 25)]:
        for j in range(n):
            x, y = cx + rng.uniform(-sp, sp), cy + rng.uniform(-sp * 0.6, sp * 0.6)
            x, y = max(-392, min(392, x)), max(-342, min(342, y))
            z = 0.0
            for nm, ex, ey, w, d, h in encl:
                if abs(x - ex) < w / 2 - 6 and abs(y - ey) < d / 2 - 6:
                    z = h
                elif abs(x - ex) < w / 2 + h and abs(y - ey) < d / 2 + h:
                    z = -1
            if z < 0:
                continue
            m.add(2, leafy(f"tree{k}", rng.uniform(4.5, 6.5), (x, y, z)) if k % 3 else pine(f"pine{k}", 2.0, (x, y, z), seed=k))
            k += 1
    for i, (x, y) in enumerate([(-370, -300), (-350, -320), (-320, -300), (-300, -325), (-270, -305)]):
        m.add(2, jhall(f"village{i}", 10, 6, 2.6, (x, y, 0), MUD, THATCH, roof_h=4, base=0, kind="kirizuma"))
    return m


# ---------------------------------------------------------------- bridges

def jbridge(name, L, W, rise, spans, z0=1.0, thick=0.7, deck=TIMBER_L, giboshi=BRONZE):
    """A Japanese timber bridge along X: an arched plank deck on rows of piles, railings with giboshi caps."""
    N = 20
    zs = lambda s: z0 + rise * (1 - (2 * s / L) ** 2)
    ss = [-L / 2 + L * i / N for i in range(N + 1)]
    verts = []
    for s in ss:
        z = zs(s)
        verts += [(s, -W / 2, z), (s, W / 2, z), (s, W / 2, z - thick), (s, -W / 2, z - thick)]
    faces = []
    for i in range(N):
        a, b = 4 * i, 4 * (i + 1)
        faces += [(a, b, b + 1, a + 1), (a + 2, b + 2, b + 3, a + 3), (a + 1, b + 1, b + 2, a + 2), (a + 3, b + 3, b, a)]
    faces += [(0, 1, 2, 3), (4 * N + 3, 4 * N + 2, 4 * N + 1, 4 * N)]
    parts = [mesh_from(name + "_deck", verts, faces, (0, 0, 0), deck)]
    rail = shade(deck, -0.2)
    for sy in (-1, 1):
        y = sy * (W / 2 - 0.15)
        for i in range(N):
            p0, p1 = (ss[i], y, zs(ss[i]) + 1.1), (ss[i + 1], y, zs(ss[i + 1]) + 1.1)
            parts.append(bar(f"{name}_rail{sy}_{i}", p0, p1, 0.25, 0.25, rail))
            p0b, p1b = (ss[i], y, zs(ss[i]) + 0.5), (ss[i + 1], y, zs(ss[i + 1]) + 0.5)
            parts.append(bar(f"{name}_mrail{sy}_{i}", p0b, p1b, 0.15, 0.15, rail))
        for i in range(0, N + 1, 2):
            s = ss[i]
            parts.append(box(f"{name}_post{sy}_{i}", 0.3, 0.3, 1.3, (s, y, zs(s)), rail))
        for s in (ss[0], ss[N // 2], ss[N]):
            parts.append(cylinder(f"{name}_gb{sy}{s:.0f}", 0.24, 0.4, (s, y, zs(s) + 1.3), giboshi, verts=8))
            parts.append(dome(f"{name}_gbd{sy}{s:.0f}", 0.24, (s, y, zs(s) + 1.7), giboshi, squash=1.6, segments=8, rings=4))
    for k in range(1, spans):
        s = -L / 2 + L * k / spans
        zb = zs(s) - thick
        for j in range(4):
            y = -W / 2 + 0.6 + (W - 1.2) * j / 3
            parts.append(cylinder(f"{name}_pile{k}_{j}", 0.28, zb, (s, y, 0), TIMBER_D, verts=6))
        parts.append(box(f"{name}_cap{k}", 0.6, W + 0.4, 0.5, (s, 0, zb - 0.5), TIMBER_D))
        parts.append(box(f"{name}_nuki{k}", 0.3, W, 0.3, (s, 0, zb * 0.45), TIMBER_D))
    return join(parts, name)


def nihonbashi():
    m = Model("nihonbashi")
    for s in (-1, 1):
        m.add(0, box(f"abut{s}", 11, 2.6, 1.0, (0, s * 25.7, 0), STONE), "abutments")
    br = jbridge("bridge", 51, 8, 3.0, 5)
    m.add(1, place(br, 0, 0, 0, 90), "bridge")
    for s in (-1, 1):
        m.add(2, box(f"kosatsu{s}", 3, 0.4, 2.2, (s * 3.5, s * 26.5, 1.0), WHITE_PL), "notices")
    return m


def ryogoku_bridge():
    m = Model("ryogoku-bridge")
    for s in (-1, 1):
        m.add(0, box(f"abut{s}", 3.0, 9, 1.0, (s * 86.5, 0, 0), STONE), "abutments")
    m.add(1, jbridge("bridge", 171, 7, 4.0, 17), "bridge")
    return m


# ---------------------------------------------------------------- temples and shrines

def kaminarimon(name, loc=(0, 0, 0), a=0):
    parts = [box(name + "_base", 13, 8, 0.4, (0, 0, 0), STONE)]
    for s in (-1, 1):
        parts.append(box(f"{name}_side{s}", 3.6, 5.4, 6.2, (s * 4.6, 0, 0.4), VERM))
        parts.append(box(f"{name}_lat{s}", 2.6, 0.2, 3.6, (s * 4.6, -2.8, 1.6), shade(VERM, -0.45)))
        for k in (-1, 1):
            parts.append(cylinder(f"{name}_p{s}{k}", 0.4, 7.0, (s * 2.7, k * 2.6, 0.4), VERM, verts=8))
    parts.append(box(name + "_tie", 12, 6, 0.8, (0, 0, 6.8), VERM))
    parts.append(cylinder(name + "_lantern", 1.6, 3.6, (0, 0, 2.8), "#9C2E22", verts=12))
    parts.append(box(name + "_lantb", 3.4, 3.4, 0.4, (0, 0, 2.6), BLACK_W))
    parts.append(irimoya(name + "_roof", 12, 6, 4.4, (0, 0, 7.6), ROOF_T, over=2.0))
    return grp(parts, name, loc[0], loc[1], loc[2], a)


def sensoji(v="1800"):
    m = Model("sensoji" + ("" if v == "1800" else "-" + v))
    m.add(0, box("precinct", 160, 420, 0.3, (0, 0, 0), GRAVEL), "precinct")
    if v == "1460":
        m.add(0, box("path", 5, 300, 0.4, (0, -40, 0), EARTH))
        m.add(1, yakuimon("gate", 8, 4, 4.4, (0, -150, 0), "#7A5A3E", BOARD), "gate")
        m.add(2, jhall("hall", 22, 18, 5.5, (0, 110, 0), "#9A6A4A", THATCH, roof_h=11, base=1.0, base_color=EARTH, posts="#7A5A3E"), "hall")
        m.add(2, jhall("hall2", 10, 8, 3.5, (40, 60, 0), "#9A6A4A", BOARD, roof_h=4, base=0.5))
        for i, (x, y) in enumerate([(-50, -170), (-60, -120), (55, -180), (60, -100), (-55, 20), (50, -10)]):
            m.add(2, jhall(f"hut{i}", 9, 6, 2.6, (x, y, 0), MUD, THATCH, roof_h=4.0, base=0, kind="kirizuma"))
        for i, (x, y) in enumerate([(-40, 150), (45, 160), (-60, 80), (65, 130), (-30, -60), (30, -200), (-65, -10)]):
            m.add(2, leafy(f"tree{i}", 4.5, (x, y, 0)) if i % 2 else pine(f"pine{i}", 1.3, (x, y, 0), seed=i))
        return m
    m.add(0, box("path", 7, 330, 0.45, (0, -40, 0), STONE))
    m.add(0, box("court", 70, 60, 0.45, (0, 100, 0), shade(GRAVEL, 0.1)))
    if v == "1872":
        m.add(1, box("kaminari_footing", 13, 8, 0.6, (0, -200, 0), STONE_D), "gates")
    else:
        m.add(1, kaminarimon("kaminarimon", (0, -200, 0)), "gates")
    for s in (-1, 1):
        for j in range(2):
            m.add(1, shop_row(f"nakamise{s}{j}", 11, 6.0, 5, (s * 12.5, -132 + j * 74, 0), a=-90 * s, storeys=1, h1=3.2,
                              wall="#D8C8A6", noren=VERM if j else INDIGO, seed=j + s))
    m.add(1, romon("hozomon", 22, 9, 9.0, 7.0, (0, -22, 0)), "gates")
    m.add(2, pagoda("pagoda", 8, 5, (46, 22, 0), wall=VERM, roof=ROOF_T, storey_h=3.6), "pagoda")
    hall = [box("hall_base", 40, 38, 1.8, (0, 0, 0), STONE),
            box("hall_ver", 38, 36, 0.4, (0, 0, 1.8), shade(TIMBER_L, -0.1)),
            box("hall_wall", 32, 30, 8.5, (0, 0, 1.8), VERM),
            box("hall_band", 32.3, 30.3, 0.8, (0, 0, 8.6), BLACK_W),
            box("hall_door", 14, 0.3, 6, (0, -15.1, 2.2), "#3A2A20"),
            eaved_roof("hall_mokoshi", 33, 31, 3.0, (0, 0, 10.3), ROOF_T, over=3.4, curve=0.12),
            box("hall_upper", 27, 25, 3.0, (0, 0, 11.0), VERM),
            irimoya("hall_roof", 27, 25, 15.5, (0, 0, 14.0), ROOF_T, over=4.5, gable=GILT)]
    for i in range(9):
        for s in (-1, 1):
            hall.append(cylinder(f"hall_col{i}{s}", 0.4, 8.5, (-17 + 34 * i / 8, s * 16.6, 1.8), VERM, verts=6))
    m.add(2, grp(hall, "hondo", 0, 142, 0), "main hall")
    m.add(2, gongen("sanja", 16, 18, (50, 150, 0), VERM, ROOF_T, base=0.6))
    m.add(2, jhall("awashima", 12, 10, 4, (-50, 60, 0), VERM, ROOF_T, roof_h=5, base=0.8))
    m.add(2, jhall("belltower", 6, 6, 4, (-48, -70, 0), VERM, ROOF_T, roof_h=3.5, base=1.5, door=False))
    for i, (x, y) in enumerate([(-30, -10), (30, -10), (-24, 40), (24, 40), (-24, 80), (24, 80)]):
        m.add(2, lantern(f"toro{i}", (x, y, 0.3), 1.2))
    for s in (-1, 1):
        for j, y in enumerate((-180, -146, -112, -78)):
            x = s * (42 if j % 2 else 58)
            m.add(2, jhall(f"shiin{s}{j}", 14, 10, 3.6, (x, y, 0), "#D9CDB4", ROOF_T, roof_h=4.5, base=0.4, door=False), "subtemples")
            m.add(2, dobei(f"shiinw{s}{j}", (x - 10, y - 9), (x + 10, y - 9), 2.0, 0.6))
    trees = [(-60, 120), (-62, 175), (40, 190), (-30, 190), (65, 100), (-65, 20), (65, -40), (-62, -40), (20, 195), (-40, 120), (64, 60),
             (-70, -200), (70, -195), (-45, 165), (68, 180), (0, 195), (-68, 95), (30, 75), (-35, 25), (70, 10)]
    for i, (x, y) in enumerate(trees):
        m.add(2, pine(f"pine{i}", 1.9, (x, y, 0), seed=i) if i % 3 else leafy(f"tree{i}", 5.0, (x, y, 0)))
    return m


def kaneiji(v="1800"):
    m = Model("kaneiji" + ("" if v == "1800" else "-" + v))
    m.add(0, box("ground", 300, 160, 0.3, (0, 0, 0), GRASS), "ground")
    m.add(0, box("path", 8, 70, 0.4, (50, -45, 0), GRAVEL))
    m.add(0, box("court", 70, 64, 0.4, (50, 8, 0), GRAVEL))
    m.add(0, box("pagoda_court", 26, 26, 0.4, (-120, 25, 0), GRAVEL))
    if v == "1872":
        m.add(1, box("chudo_platform", 51, 46, 2.2, (50, 10, 0), STONE_D), "ruins")
        import random
        rng = random.Random(7)
        for i in range(26):
            x, y = 50 + rng.uniform(-22, 22), 10 + rng.uniform(-20, 20)
            m.add(1, box(f"debris{i}", rng.uniform(1.5, 5), rng.uniform(0.6, 2), rng.uniform(0.4, 1.4), (x, y, 2.2), "#3A3330", rot_z=rng.uniform(0, 3)))
        for i, (x, y) in enumerate([(32, -6), (68, -6), (32, 26), (68, 26), (50, -6)]):
            m.add(1, cylinder(f"stump{i}", 0.5, rng.uniform(1.5, 4.0), (x, y, 2.2), "#2E2826", verts=6))
    else:
        hall = [box("base", 52, 47, 2.4, (0, 0, 0), STONE),
                box("wall", 45, 40, 9.0, (0, 0, 2.4), VERM),
                box("band", 45.3, 40.3, 0.9, (0, 0, 10.0), BLACK_W),
                box("door", 18, 0.3, 6.5, (0, -20.1, 2.4), "#3A2A20"),
                eaved_roof("mokoshi", 46, 41, 3.6, (0, 0, 11.4), ROOF_T, over=4.0, curve=0.14),
                box("upper", 38, 33, 4.0, (0, 0, 12.4), VERM),
                irimoya("roof", 38, 33, 16, (0, 0, 16.4), ROOF_T, over=5.0, gable=GILT)]
        for i in range(11):
            for s in (-1, 1):
                hall.append(cylinder(f"col{i}{s}", 0.45, 9.0, (-24 + 48 * i / 10, s * 22, 2.4), VERM, verts=6))
        hall.append(stair("st", 14, 2.4, 4, 5, (0, -25.5, 0), "N", STONE))
        m.add(1, grp(hall, "chudo", 50, 10, 0), "Konpon Chudo")
        m.add(1, romon("monjuro", 16, 8, 6.5, 5.0, (50, -65, 0)))
    m.add(2, pagoda("pagoda", 9, 5, (-120, 25, 0), wall=VERM, roof=ROOF_T, storey_h=3.8), "pagoda")
    trees = [(-140, -50), (-100, -60), (-60, -40), (-30, 50), (-80, 60), (-140, 65), (110, 60), (120, -40), (100, -65), (-10, -55), (130, 10), (-40, 0)]
    for i, (x, y) in enumerate(trees):
        m.add(2, leafy(f"cherry{i}", 4.2, (x, y, 0), CHERRY) if i % 2 else pine(f"pine{i}", 1.5, (x, y, 0), seed=i))
    return m


def zojoji():
    m = Model("zojoji")
    m.add(0, box("precinct", 160, 240, 0.3, (0, 0, 0), GRAVEL), "precinct")
    m.add(0, box("path", 8, 130, 0.4, (0, -45, 0), STONE))
    m.add(1, romon("sanmon", 29, 17, 9.0, 6.0, (0, -95, 0)), "Sanmon")
    hall = [box("base", 56, 46, 2.6, (0, 0, 0), STONE), box("wall", 50, 40, 10, (0, 0, 2.6), "#A2402E"),
            box("band", 50.3, 40.3, 0.9, (0, 0, 11.6), BLACK_W), box("door", 20, 0.3, 7, (0, -20.1, 2.6), "#3A2A20"),
            irimoya("roof", 50, 40, 18, (0, 0, 12.6), ROOF_T, over=5.0, gable=GILT), stair("st", 16, 2.6, 4, 5, (0, -25, 0), "N", STONE)]
    m.add(2, grp(hall, "daiden", 0, 70, 0), "Daiden")
    m.add(2, pagoda("pagoda", 8, 5, (55, -10, 0), wall=VERM, roof=ROOF_T, storey_h=3.6))
    m.add(2, jhall("kyozo", 10, 10, 4.5, (-50, 10, 0), VERM, ROOF_T, roof_h=5, base=1.0))
    m.add(2, jhall("shoro", 7, 7, 4.5, (-50, -50, 0), VERM, ROOF_T, roof_h=4, base=1.8, door=False))
    for i, (x, y) in enumerate([(-65, -105), (65, -105), (-65, 100), (65, 105), (-30, 115), (30, 115), (65, 40), (-65, 60), (-25, -60), (25, -60), (65, -60), (-68, -10)]):
        m.add(2, pine(f"pine{i}", 1.5, (x, y, 0), seed=i))
    return m


def kanda_myojin():
    m = Model("kanda-myojin")
    m.add(0, box("precinct", 90, 90, 0.3, (0, 0, 0), GRAVEL), "precinct")
    m.add(0, box("path", 6, 40, 0.4, (0, -25, 0), STONE))
    m.add(1, place(torii("torii", 9, 8, (0, 0, 0), color=VERM), 0, -40, 0.3), "torii")
    m.add(1, romon("zuishinmon", 14, 7, 5.0, 4.0, (0, -27, 0), VERM, COPPER))
    m.add(2, gongen("shaden", 38, 42, (0, 18, 0), VERM, COPPER, base=1.2), "shrine")
    for i, (x, y) in enumerate([(-38, -38), (38, -38), (-38, 30), (38, 30), (-30, -10), (32, -8)]):
        m.add(2, leafy(f"tree{i}", 3.6, (x, y, 0)) if i % 2 else pine(f"pine{i}", 1.2, (x, y, 0), seed=i))
    return m


def yushima_seido():
    m = Model("yushima-seido")
    m.add(0, box("ground", 80, 70, 0.3, (0, 0, 0), GRAVEL), "precinct")
    pts = [(-37, -32), (37, -32), (37, 33), (-37, 33), (-37, -32)]
    for i in range(4):
        if i == 0:
            m.add(1, dobei("wall0a", (-37, -32), (-5, -32), 3.0, 1.0, BLACK_W, ROOF_T), "walls")
            m.add(1, dobei("wall0b", (5, -32), (37, -32), 3.0, 1.0, BLACK_W, ROOF_T))
        else:
            m.add(1, dobei(f"wall{i}", pts[i], pts[i + 1], 3.0, 1.0, BLACK_W, ROOF_T))
    m.add(1, yakuimon("nyutokumon", 8, 5, 5.0, (0, -32, 0), BLACK_W, "#3B3D40"))
    m.add(1, yakuimon("kyomon", 9, 5, 5.5, (0, -8, 0), BLACK_W, "#3B3D40"))
    ts = east_asian_hall("taiseiden", 26, 16, 6.5, (0, 0, 0), wall=BLACK_W, roof="#3B3D40", platform=1.6, plat_color=STONE, double=False)
    m.add(2, place(ts, 0, 14, 0), "Taiseiden")
    for s in (-1, 1):
        m.add(2, jhall(f"kairo{s}", 6, 30, 3.5, (s * 26, 12, 0), BLACK_W, "#3B3D40", roof_h=2.6, base=0.5, kind="kirizuma", door=False))
    for i, (x, y) in enumerate([(-28, -22), (28, -22), (-14, -20), (14, -20)]):
        m.add(2, leafy(f"tree{i}", 2.8, (x, y, 0), "#5E7A50"))
    return m


def ekoin():
    m = Model("ekoin")
    m.add(0, box("ground", 100, 90, 0.3, (0, 0, 0), GRAVEL), "precinct")
    m.add(0, box("path", 6, 40, 0.4, (0, -25, 0), STONE))
    m.add(1, yakuimon("gate", 9, 5, 5.0, (0, -42, 0), TIMBER_D, ROOF_T), "gate")
    for i, (p0, p1) in enumerate([((-48, -42), (-6, -42)), ((6, -42), (48, -42)), ((48, -42), (48, 42)), ((48, 42), (-48, 42)), ((-48, 42), (-48, -42))]):
        m.add(1, dobei(f"wall{i}", p0, p1, 2.4, 0.8, WHITE_PL, ROOF_T))
    m.add(2, jhall("hondo", 28, 22, 6.5, (0, 20, 0), "#8A5A3A", ROOF_T, roof_h=12, base=1.2, posts=TIMBER_D), "halls")
    m.add(2, frustum("muenzuka", 16, 12, 6, 4, 3, (-28, -8, 0), "#8F8A6A"))
    for i in range(7):
        m.add(2, box(f"stone{i}", 0.8, 0.6, 1.8 + (i % 3) * 0.5, (-34 + i * 2, -18, 0.3), STONE))
    m.add(2, box("tahoto", 2.5, 2.5, 3.5, (-28, -8, 3), STONE_D))
    m.add(2, cylinder("dohyo", 3.6, 0.7, (28, -14, 0.3), "#B89A6A", verts=16))
    for sx in (-1, 1):
        for sy in (-1, 1):
            m.add(2, cylinder(f"post{sx}{sy}", 0.18, 5.0, (28 + sx * 3.6, -14 + sy * 3.6, 0.3), TIMBER_D, verts=6))
    m.add(2, irimoya("dohyo_roof", 8, 8, 2.6, (28, -14, 5.3), BOARD, over=0.6))
    for i, (x, y) in enumerate([(-40, 30), (40, 30), (40, -30), (-42, -32)]):
        m.add(2, pine(f"pine{i}", 1.1, (x, y, 0), seed=i))
    return m


def tomioka_hachiman():
    m = Model("tomioka-hachiman")
    m.add(0, box("precinct", 100, 90, 0.3, (0, 0, 0), GRAVEL), "precinct")
    m.add(0, box("path", 7, 40, 0.4, (0, -25, 0), STONE))
    t = torii("torii", 11, 9, (0, 0, 0), color=VERM)
    m.add(1, place(t, 0, -40, 0.3), "torii")
    m.add(1, romon("gate", 14, 7, 5.0, 4.0, (0, -26, 0), VERM, ROOF_T))
    m.add(2, gongen("shaden", 44, 42, (0, 18, 0), VERM, COPPER, base=1.2), "shrine")
    m.add(2, box("yokozuna_stone", 1.2, 4.0, 4.5, (36, -22, 0.3), STONE_D))
    m.add(2, cylinder("dohyo", 3.2, 0.5, (36, -10, 0.3), "#B89A6A", verts=16))
    for i, (x, y) in enumerate([(-42, -38), (42, -38), (-42, 32), (42, 32), (-36, -10), (-30, 40)]):
        m.add(2, pine(f"pine{i}", 1.3, (x, y, 0), seed=i))
    return m


def hie_shrine():
    m = Model("hie-shrine")
    m.add(0, box("ground", 90, 100, 0.3, (0, 0, 0), GRASS), "hill")
    m.add(0, frustum("hill", 86, 70, 70, 55, 7.0, (0, 14, 0), "#87926A"))
    m.add(0, box("hilltop", 69, 54, 0.15, (0, 14, 7.0), GRAVEL))
    n = 10
    for i in range(n):
        y0 = -34 + i * 2.05
        m.add(0, box(f"step{i}", 8, -13.5 - y0, 7.0 * (i + 1) / n, (0, (y0 - 13.5) / 2, 0), STONE))
    sanno = [cylinder("p1", 0.55, 8.5, (-3.8, 0, 0), VERM, verts=10), cylinder("p2", 0.55, 8.5, (3.8, 0, 0), VERM, verts=10),
             box("kasagi", 12, 1.0, 0.9, (0, 0, 8.5), DARK), box("nuki", 10, 0.7, 0.7, (0, 0, 6.8), VERM),
             mesh_from("gassho", [(-3.4, -0.3, 9.4), (3.4, -0.3, 9.4), (0, -0.3, 12.2), (-3.4, 0.3, 9.4), (3.4, 0.3, 9.4), (0, 0.3, 12.2)],
                       [(0, 1, 2), (5, 4, 3), (0, 3, 4, 1), (1, 4, 5, 2), (2, 5, 3, 0)], (0, 0, 0), DARK)]
    m.add(1, grp(sanno, "sanno_torii", 0, -44, 0.3), "Sanno torii")
    m.add(1, romon("shinmon", 12, 6, 4.6, 3.6, (0, -8, 7.0), VERM, ROOF_T))
    m.add(2, gongen("shaden", 36, 32, (0, 23, 7.0), VERM, ROOF_T, base=1.0), "shrine")
    for i, (x, y, z) in enumerate([(-38, -12, 0.3), (38, -12, 0.3), (-28, 34, 7), (28, 34, 7), (-38, 10, 2), (38, 10, 2), (-20, -32, 0.3), (20, -32, 0.3)]):
        m.add(2, leafy(f"tree{i}", 3.8, (x, y, z), "#5E7A50") if i % 2 else pine(f"pine{i}", 1.2, (x, y, z), seed=i))
    return m


def benten_do():
    m = Model("benten-do")
    m.add(0, cylinder("island", 19.5, 0.8, (0, 0, 0), "#9AA06E", verts=14), "island")
    m.add(0, box("causeway", 4, 8, 0.7, (0, -16, 0), EARTH))
    m.add(0, cylinder("base", 7.5, 1.2, (0, 2, 0.8), STONE, verts=8))
    m.add(1, cylinder("hall", 5.6, 4.6, (0, 2, 2.0), VERM, verts=8), "hall")
    m.add(1, cylinder("band", 5.7, 0.5, (0, 2, 5.6), BLACK_W, verts=8))
    m.add(1, box("door", 3, 0.3, 3, (0, 2 - 5.3, 2.0), DARK))
    m.add(2, cylinder("roof", 8.4, 4.4, (0, 2, 6.6), ROOF_T, verts=8, r_top=0.4), "roof")
    m.add(2, cylinder("hoju", 0.5, 1.4, (0, 2, 11.0), BRONZE, verts=8))
    m.add(2, dome("hoju_d", 0.6, (0, 2, 12.3), GILT, squash=1.4, segments=8, rings=4))
    m.add(2, lantern("toro", (-4, -10, 0.8), 1.1))
    m.add(2, pine("pine0", 1.1, (10, 8, 0.8), seed=1))
    m.add(2, pine("pine1", 0.9, (-11, 6, 0.8), seed=2))
    m.add(2, leafy("tree0", 3.0, (8, -9, 0.8), "#6F8A5C"))
    return m


# ---------------------------------------------------------------- commerce, entertainment and works

def fish_market():
    m = Model("fish-market")
    m.add(0, box("quay", 170, 6, 1.2, (0, -14, 0), STONE), "quay")
    m.add(0, box("yard", 170, 28, 0.6, (0, 3, 0), "#B8A888"))
    for i in range(8):
        x = -74 + i * 21
        shed = []
        for sx in (-1, 1):
            for sy in (-1, 1):
                shed.append(box(f"p{sx}{sy}", 0.4, 0.4, 3.0, (sx * 8.5, sy * 4.5, 0), TIMBER_D))
        shed.append(kirizuma("r", 18.5, 10, 2.0, (0, 0, 3.0), BOARD, over=0.6))
        shed.append(box("stall", 16, 2.4, 0.9, (0, -3, 0), TIMBER_L))
        m.add(1, grp(shed, f"shed{i}", x, -2, 0.6), "sheds")
        m.add(1, shop_row(f"tonya{i}", 3, 6.4, 7, (x, 11.5, 0.6), storeys=2 if i % 2 else 1, wall="#CFC0A0", noren=INDIGO if i % 3 else None, seed=i))
    for i in range(16):
        x = -80 + i * 10.5 + (i % 3)
        m.add(2, cylinder(f"tub{i}", 0.7, 0.7, (x, -9.5 + (i % 2) * 1.6, 1.2), TIMBER_L, verts=8), "goods")
        m.add(2, box(f"crate{i}", 1.2, 0.9, 0.5, (x + 3, -6.5, 0.6), shade(TIMBER_L, 0.15)))
    for i, x in enumerate([-60, -25, 15, 50, 75]):
        m.add(2, boat(f"boat{i}", 9, 2.2, (x, -18.5, 0), a=0 if i % 2 else 180, cargo="#7D8C94" if i % 2 else None))
    return m


def echigoya():
    m = Model("echigoya")
    m.add(0, box("ground", 70, 60, 0.3, (0, 0, 0), GRAVEL), "ground")
    shop = [box("g", 66, 26, 4.8, (0, 0, 0), BLACK_W), box("gfront", 64, 0.3, 3.4, (0, -13.1, 0.2), "#3A3028"),
            box("eave", 67, 2.2, 0.35, (0, -14.0, 4.5), ROOF_T),
            box("u", 66, 22, 3.8, (0, 2, 4.8), BLACK_W),
            box("uwin", 50, 0.3, 1.2, (0, -9.1, 6.0), "#6A5E52"),
            kirizuma("roof", 66, 22, 6.0, (0, 2, 8.6), ROOF_T, over=1.4)]
    for s in (-1, 1):
        shop.append(box(f"udatsu{s}", 1.2, 24, 6.4, (s * 33.6, 2, 4.8), WHITE_PL))
    for i in range(9):
        x = -28 + i * 7
        shop.append(box(f"noren{i}", 5.6, 0.18, 2.2, (x, -13.6, 2.0), INDIGO))
        shop.append(box(f"mon{i}", 1.2, 0.2, 1.0, (x, -13.75, 2.6), WHITE_PL))
    shop.append(box("kanban", 14, 0.5, 2.2, (0, -9.0, 9.6), "#2A2420"))
    shop.append(box("kanban_t", 12, 0.6, 1.4, (0, -9.0, 10.0), GILT))
    m.add(1, grp(shop, "shop", 0, -15, 0.3), "shop")
    for i, x in enumerate([-24, -6, 12, 28]):
        m.add(2, kura(f"kura{i}", 11 if i < 3 else 9, 9, 7.5, (x, 22, 0.3), ridge_y=True), "storehouses")
    m.add(2, jhall("oku", 30, 10, 3.8, (-6, 8, 0.3), "#D9CDB4", ROOF_T, roof_h=3, base=0, kind="kirizuma", door=False))
    return m


def nakamura_za():
    m = Model("nakamura-za")
    m.add(0, box("ground", 26, 42, 0.2, (0, 0, 0), GRAVEL), "ground")
    m.add(1, box("hall", 24, 38, 10, (0, 0.5, 0), "#7A6650"), "theatre")
    m.add(1, box("hall_band", 24.2, 38.2, 0.8, (0, 0.5, 6.0), DARK))
    m.add(1, kirizuma("roof", 24, 38, 6.5, (0, 0.5, 10), ROOF_T, over=0.8))
    m.add(1, box("kido", 3, 0.3, 2.2, (0, -18.6, 0.2), DARK))
    m.add(1, box("eave", 25, 2.0, 0.3, (0, -19.3, 4.2), BOARD))
    cols = ["#C9A24A", "#B23A2A", "#3E5C9A", "#E8DCC2", "#5F8A5A", "#B23A2A"]
    for i in range(6):
        m.add(2, box(f"kanban{i}", 3.4, 0.3, 2.6, (-9.5 + i * 3.8, -18.8, 4.7), cols[i]), "billboards")
    for i in range(10):
        m.add(2, cylinder(f"lantern{i}", 0.35, 0.8, (-10.8 + i * 2.4, -19.6, 3.1), "#E8D2A8" if i % 2 else VERM, verts=8))
    yg = [box("y", 6.5, 4.5, 3.6, (0, 0, 0), "#4E3A6A"), box("y_mon", 2.2, 0.2, 2.2, (0, -2.3, 0.7), WHITE_PL),
          kirizuma("y_r", 6.5, 4.5, 1.2, (0, 0, 3.6), BOARD, over=0.3, ridge=False)]
    for i in range(5):
        yg.append(cylinder(f"bonten{i}", 0.08, 3.2, (-2.4 + i * 1.2, 0, 4.4), TIMBER_D, verts=4))
        yg.append(box(f"bontenh{i}", 0.5, 0.5, 0.8, (-2.4 + i * 1.2, 0, 7.4), WHITE_PL))
    m.add(3, grp(yg, "yagura", 0, -16.5, 10.0), "drum tower")
    return m


def yoshiwara():
    m = Model("yoshiwara")
    m.add(0, box("ground", 216, 316, 0.3, (0, 0, 0), "#C8B898"), "ground")
    for nm, (x, y, w, d) in dict(s=(0, -158.5, 220, 3), n=(0, 158.5, 220, 3), w=(-108.5, 0, 3, 320), e=(108.5, 0, 3, 320)).items():
        m.add(0, box("dobu_" + nm, w, d, 0.35, (x, y, 0), "#3E4A48"))
    m.add(0, box("nakanocho", 14, 300, 0.4, (0, 0, 0), GRAVEL))
    pts = [(-105, -155), (105, -155), (105, 155), (-105, 155), (-105, -155)]
    for i in range(4):
        if i == 0:
            m.add(1, fence("fence_sa", (-105, -155), (-6, -155), 2.6, "#4A3A30"), "fence")
            m.add(1, fence("fence_sb", (6, -155), (105, -155), 2.6, "#4A3A30"))
        else:
            m.add(1, fence(f"fence{i}", pts[i], pts[i + 1], 2.6, "#4A3A30"))
    omon = [box("p1", 1.0, 1.0, 6.5, (-3.5, 0, 0), BLACK_W), box("p2", 1.0, 1.0, 6.5, (3.5, 0, 0), BLACK_W),
            box("beam", 9.5, 1.0, 0.9, (0, 0, 5.6), BLACK_W), kirizuma("r", 10, 3.4, 1.6, (0, 0, 6.5), "#3E3A38", over=0.4)]
    m.add(1, grp(omon, "omon", 0, -155, 0), "fence")
    # the quarter: cross streets at y = -80, 0, +80; houses face the streets
    bands = [(-150, -86), (-74, -6), (6, 74), (86, 150)]
    for side in (-1, 1):
        for b, (y0, y1) in enumerate(bands):
            L = y1 - y0
            n = int(L / 8.5)
            # teahouses along Naka-no-cho
            m.add(2, shop_row(f"chaya{side}{b}", n, L / n, 9, (side * 12.5, (y0 + y1) / 2, 0), a=-90 * side, h1=3.6, h2=2.6,
                              wall="#D9CBAE", noren="#9C3A2E" if b % 2 else INDIGO, seed=b), "houses")
            # brothels along the cross streets, with red lattices
            for k, yy in enumerate((y0 + 8, y1 - 8)):
                if (b == 0 and k == 0) or (b == 3 and k == 1):
                    continue
                face = 0 if k == 0 else 180
                xs = side * 60
                mm = shop_row(f"mise{side}{b}{k}", 9, 9.5, 12, (0, 0, 0), h1=3.8, h2=3.0, wall="#D6C6A6", lattice="#8E3A2A", seed=b + k)
                m.add(2, place(mm, xs, yy, 0, face))
            # a back row of larger houses in the middle of the block
            m.add(2, shop_row(f"oya{side}{b}", 4, 15.0, 16 if L > 70 else 13, (side * 61, (y0 + y1) / 2, 0), h1=4.0, h2=3.2,
                              wall="#CDBD9C", lattice="#8E3A2A", seed=b + 2))
        for i in range(-6, 7):
            m.add(3, leafy(f"cherry{side}{i}", 1.8, (side * 3.5, i * 22 + 4, 0.4), CHERRY), "cherries")
    return m


def kaga_akamon():
    m = Model("kaga-akamon")
    m.add(0, box("ground", 110, 24, 0.3, (0, 0, 0), GRAVEL), "ground")
    for s in (-1, 1):
        x = s * 32
        ny = [box("lo", 44, 9, 2.6, (0, 0, 0), NAMAKO), box("up", 44, 9, 4.2, (0, 0, 2.6), WHITE_PL)]
        for i in range(6):
            ny.append(box(f"win{i}", 2.2, 0.3, 1.2, (-18 + i * 7.2, -4.6, 4.0), BLACK_W))
        for i in range(10):
            ny.append(box(f"gx{i}", 0.12, 0.2, 2.4, (-21 + i * 4.6, -4.55, 0.1), WHITE_PL))
        ny.append(kirizuma("r", 44, 9, 3.0, (0, 0, 6.8), ROOF_T, over=0.8))
        m.add(1, grp(ny, f"nagaya{s}", x, 4, 0.3), "nagaya")
        bs = [box("b", 4.5, 4.5, 3.2, (0, 0, 0), WHITE_PL), box("bw", 2.2, 0.3, 1.0, (0, -2.3, 1.4), BLACK_W),
              eaved_roof("br", 4.5, 4.5, 2.0, (0, 0, 3.2), ROOF_T, over=0.9)]
        m.add(1, grp(bs, f"bansho{s}", s * 9.0, -8, 0.3))
    gate = [box("mp1", 1.1, 1.1, 7.0, (-3.6, -1.0, 0), VERM), box("mp2", 1.1, 1.1, 7.0, (3.6, -1.0, 0), VERM),
            box("bp1", 0.8, 0.8, 6.2, (-3.6, 3.0, 0), VERM), box("bp2", 0.8, 0.8, 6.2, (3.6, 3.0, 0), VERM),
            box("lintel", 9.6, 1.2, 1.0, (0, -1.0, 6.2), VERM), box("doors", 6.4, 0.4, 5.6, (0, -0.6, 0), "#8E3226"),
            box("frieze", 9.2, 5.0, 1.0, (0, 1.0, 7.0), VERM),
            irimoya("roof", 11, 7.5, 3.6, (0, 1.0, 8.0), ROOF_T, over=1.3, gable=GILT)]
    m.add(2, grp(gate, "akamon", 0, 0, 0.3), "Akamon")
    return m


def tsukiji_honganji():
    m = Model("tsukiji-honganji")
    m.add(0, box("precinct", 110, 90, 0.3, (0, 0, 0), GRAVEL), "precinct")
    m.add(0, box("path", 8, 30, 0.4, (0, -30, 0), STONE))
    hall = [box("base", 64, 54, 2.0, (0, 0, 0), STONE), box("wall", 58, 48, 11, (0, 0, 2.0), "#7A5A40"),
            box("band", 58.3, 48.3, 1.0, (0, 0, 11.6), BLACK_W), box("door", 30, 0.3, 7, (0, -24.1, 2.0), "#2E2620"),
            irimoya("roof", 58, 48, 22, (0, 0, 13.0), ROOF_T, over=6.0, gable=GILT), stair("st", 20, 2.0, 4, 4, (0, -29, 0), "N", STONE)]
    for i in range(13):
        hall.append(cylinder(f"col{i}", 0.45, 11, (-29 + 58 * i / 12, -26, 2.0), "#6A4A34", verts=6))
    m.add(1, grp(hall, "hondo", 0, 12, 0), "main hall")
    m.add(2, yakuimon("gate", 10, 6, 6.0, (0, -40, 0), "#6A4A34", ROOF_T), "gate and subtemples")
    for s in (-1, 1):
        m.add(2, jhall(f"sub{s}", 13, 10, 4.0, (s * 42, -28, 0), "#B8A07C", ROOF_T, roof_h=5, base=0.5))
        m.add(2, jhall(f"sub2{s}", 10, 9, 3.6, (s * 46, 30, 0), "#B8A07C", ROOF_T, roof_h=4.5, base=0.5))
        m.add(2, pine(f"pine{s}", 1.2, (s * 30, -38, 0), seed=s + 2))
    return m


def hinomi_yagura():
    m = Model("hinomi-yagura")
    m.add(0, box("pad", 8, 8, 0.25, (0, 0, 0), STONE), "legs")
    H = 8.6
    for sx in (-1, 1):
        for sy in (-1, 1):
            m.add(0, beam(f"leg{sx}{sy}", (sx * 3.4, sy * 3.4, 0.2), (sx * 1.6, sy * 1.6, H), 0.17, TIMBER_D))
    for k, z in enumerate((2.6, 5.4)):
        t = z / H
        r = 3.4 - 1.8 * t
        for i, (a, b) in enumerate([((-r, -r), (r, -r)), ((r, -r), (r, r)), ((r, r), (-r, r)), ((-r, r), (-r, -r))]):
            m.add(1, bar(f"tie{k}{i}", (a[0], a[1], z), (b[0], b[1], z), 0.14, 0.14, TIMBER_D), "bracing")
    for i, (a, b) in enumerate([((-3.4, -3.4, 0.3), (2.5, -2.5, 2.6)), ((3.4, 3.4, 0.3), (-2.5, 2.5, 2.6)), ((-3.4, 3.4, 0.3), (-2.5, -2.5, 2.6))]):
        m.add(1, bar(f"brace{i}", a, b, 0.1, 0.1, TIMBER_D))
    for s in (-0.4, 0.4):
        m.add(1, bar(f"ladder{s}", (s, -3.6, 0.2), (s, -1.75, H), 0.08, 0.08, TIMBER_L))
    for i in range(12):
        t = (i + 0.5) / 12
        m.add(1, bar(f"rung{i}", (-0.4, -3.6 + 1.85 * t, 0.2 + (H - 0.2) * t), (0.4, -3.6 + 1.85 * t, 0.2 + (H - 0.2) * t), 0.05, 0.05, TIMBER_L))
    m.add(2, box("floor", 4.0, 4.0, 0.3, (0, 0, H), TIMBER_L), "lookout")
    for sx in (-1, 1):
        for sy in (-1, 1):
            m.add(2, box(f"rp{sx}{sy}", 0.14, 0.14, 2.2, (sx * 1.85, sy * 1.85, H + 0.3), TIMBER_D))
    for i, (a, b) in enumerate([((-1.9, -1.9), (1.9, -1.9)), ((1.9, -1.9), (1.9, 1.9)), ((1.9, 1.9), (-1.9, 1.9)), ((-1.9, 1.9), (-1.9, -1.9))]):
        m.add(2, bar(f"rail{i}", (a[0], a[1], H + 1.1), (b[0], b[1], H + 1.1), 0.1, 0.1, TIMBER_D))
    m.add(2, eaved_roof("roof", 3.8, 3.8, 1.3, (0, 0, H + 2.5), BOARD, over=0.5, curve=0.15))
    m.add(2, cylinder("hansho", 0.35, 0.7, (0, 0, H + 1.6), BRONZE, verts=10))
    return m


def shimbashi_station():
    m = Model("shimbashi-station")
    m.add(0, box("ground", 110, 70, 0.3, (0, 0, 0), "#B9AD95"), "ground")
    m.add(0, box("forecourt", 80, 10, 0.35, (0, -30, 0), GRAVEL))
    blocks = [(0, 28, 20, 11.5), (-42, 18, 22, 10.5), (42, 18, 22, 10.5), (-23.5, 19, 14, 8.0), (23.5, 19, 14, 8.0)]
    for i, (x, w, d, h) in enumerate(blocks):
        y = -18
        parts = [box("b", w, d, h, (0, 0, 0), IZU), box("plinth", w + 0.3, d + 0.3, 1.0, (0, 0, 0), shade(IZU, -0.15)),
                 box("course", w + 0.3, d + 0.3, 0.4, (0, 0, h * 0.5), shade(IZU, -0.1)),
                 box("cornice", w + 0.8, d + 0.8, 0.5, (0, 0, h - 0.5), shade(IZU, 0.15))]
        nw = max(2, int(w / 3.6))
        parts.append(arcade("w1", w * 0.86, h * 0.34, nw, (0, -d / 2 - 0.05, 1.2), "S", DARK, pointed=False, fill=0.5))
        parts.append(arcade("w2", w * 0.86, h * 0.3, nw, (0, -d / 2 - 0.05, h * 0.55), "S", DARK, pointed=False, fill=0.45))
        if i == 0:
            parts.append(arch_panel("door", 5, 4.6, (0, -d / 2 - 0.08, 0.6), "S", "#3A2E26", pointed=False))
        parts.append(hip_x("r", w, d, min(w, d) * 0.3, (0, 0, h), SLATE_R, ridge=0.45, overhang=0.6))
        m.add(1, grp(parts, f"block{i}", x, y, 0.3), "station")
    m.add(1, box("platform", 104, 8, 1.0, (0, 2, 0.3), STONE), "station")
    for i in range(14):
        m.add(2, cylinder(f"cpost{i}", 0.18, 4.2, (-48 + i * 7.4, 4.5, 1.3), TIMBER_D, verts=6), "platform")
    m.add(2, kirizuma("canopy", 100, 8, 1.2, (0, 2.5, 5.5), "#6A6058", over=0.4, ridge=False))
    for i, y in enumerate((13, 24)):
        m.add(2, box(f"ballast{i}", 110, 3.6, 0.4, (0, y, 0.3), "#7C7266"))
        for s in (-0.75, 0.75):
            m.add(2, box(f"rail{i}{s}", 110, 0.15, 0.2, (0, y + s, 0.7), "#3A3A3C"))
    loco = [beam("boiler", (-5, 0, 2.1), (1.5, 0, 2.1), 0.85, "#2E3A30", verts=12), box("cab", 2.2, 2.4, 2.6, (2.6, 0, 1.0), "#2E3A30"),
            box("cabr", 2.6, 2.6, 0.2, (2.6, 0, 3.6), "#1E1E1E"), box("frame", 9, 2.0, 0.5, (-1.2, 0, 0.9), "#1E1E1E"),
            cylinder("chimney", 0.35, 1.6, (-4.2, 0, 2.8), "#1E1E1E", verts=8), dome("steamdome", 0.55, (-1.4, 0, 2.9), BRONZE, segments=8, rings=4),
            box("tender", 3.4, 2.2, 1.8, (5.6, 0, 0.9), "#2E3A30")]
    for k in range(3):
        for s in (-1, 1):
            loco.append(beam(f"wheel{k}{s}", (-3.8 + k * 2.2, s * 0.85, 0.9), (-3.8 + k * 2.2, s * 1.05, 0.9), 0.75, "#1E1E1E", verts=10))
    m.add(3, grp(loco, "loco", -30, 24, 0.6), "train")
    for k in range(3):
        car = [box("body", 8.0, 2.4, 2.1, (0, 0, 1.0), "#6A2E26"), box("frame", 8.2, 2.0, 0.4, (0, 0, 0.6), "#1E1E1E"),
               box("roofc", 8.2, 2.6, 0.3, (0, 0, 3.1), "#4A4440"), box("win", 7.0, 2.45, 0.6, (0, 0, 2.0), "#E8DCC2")]
        m.add(3, grp(car, f"car{k}", -16 + k * 9.0, 24, 0.6))
    return m


def ginza_brick():
    m = Model("ginza-brick")
    m.add(0, box("street", 27, 240, 0.3, (0, 0, 0), "#D8CDB5"), "street")
    for s in (-1, 1):
        m.add(0, box(f"pave{s}", 3.6, 240, 0.4, (s * 15.3, 0, 0), "#B07A60"))
        m.add(0, box(f"lot{s}", 12.9, 240, 0.3, (s * 23.55, 0, 0), "#C2B294"))
    blocks = [(-120, -46), (-36, 54), (64, 120)]
    for s in (-1, 1):
        for b, (y0, y1) in enumerate(blocks):
            L = y1 - y0
            yc = (y0 + y1) / 2
            unfinished = b == 2 and s == 1
            stucco = (b + (s > 0)) % 2 == 1
            wall = WHITE_PL if stucco else BRICK_R
            parts = [box("g", 12, L, 4.4, (0, 0, 0), wall), box("u", 12, L, 4.2, (0, 0, 4.4), wall),
                     box("band", 12.3, L, 0.4, (0, 0, 4.2), shade(wall, 0.2) if not stucco else "#CFC6B6")]
            nb = int(L / 3.2)
            for i in range(nb):
                yy = -L / 2 + (i + 0.5) * L / nb
                parts.append(box(f"win{i}", 0.3, 1.4, 2.0, (-6.1, yy, 5.3), DARK))
                parts.append(box(f"door{i}", 0.3, 1.8, 2.8, (-6.1, yy, 0.2), "#3A2E26"))
            parts.append(box("veranda", 3.0, L, 0.35, (-7.5, 0, 4.2), "#E8E2D6"))
            parts.append(box("verrail", 0.15, L, 0.9, (-8.9, 0, 4.55), "#E8E2D6"))
            for i in range(nb + 1):
                yy = -L / 2 + i * L / nb
                parts.append(cylinder(f"col{i}", 0.16, 4.2, (-8.8, yy, 0), WHITE_PL, verts=6))
            if unfinished:
                for i in range(int(L / 4) + 1):
                    yy = -L / 2 + i * 4
                    parts.append(beam(f"scaf{i}", (-6.6, yy, 0), (-6.6, yy, 10.5), 0.08, "#9A8060", verts=4))
                    parts.append(beam(f"scafb{i}", (6.6, yy, 0), (6.6, yy, 10.5), 0.08, "#9A8060", verts=4))
                for z in (3.0, 6.0, 9.0):
                    parts.append(bar(f"ledger{z}", (-6.6, -L / 2, z), (-6.6, L / 2, z), 0.1, 0.1, "#9A8060"))
                parts.append(box("rafters", 12, L, 0.25, (0, 0, 8.6), TIMBER_L))
            else:
                parts.append(hip_roof("roof", 12, L, 3.2, (0, 0, 8.6), ROOF_T, ridge=0.85, overhang=0.5))
            o = grp(parts, f"block{s}{b}", 0, 0, 0)
            if s < 0:
                o = place(o, 0, 0, 0, 180)
            m.add(1, place(o, s * 23.55, yc, 0.3), "brick blocks")
        for i in range(19):
            y = -114 + i * 12.6
            if i % 4 == 3:
                m.add(2, cylinder(f"lamp{s}{i}", 0.1, 3.6, (s * 12.8, y, 0.4), "#2E2A27", verts=6), "trees and lamps")
                m.add(2, box(f"lampb{s}{i}", 0.6, 0.6, 0.7, (s * 12.8, y, 4.0), "#E8D8A8"))
            else:
                kind = (CHERRY, PINE_C, "#86A060")[i % 3]
                m.add(2, leafy(f"tree{s}{i}", 1.5, (s * 12.8, y, 0.4), kind) if kind != PINE_C else pine(f"pine{s}{i}", 0.7, (s * 12.8, y, 0.4), seed=i))
    return m


def asakusa_okura():
    m = Model("asakusa-okura")
    m.add(0, box("ground", 70, 300, 0.6, (-15, 0, 0), "#C2B294"), "ground")
    ys = [-131 + k * 37.4 for k in range(8)]
    for k, y in enumerate(ys):
        m.add(0, box(f"dock{k}", 30, 9, 0.2, (35, y, 0), WATER_C))
    edges = [-150] + [v for y in ys for v in (y - 4.5, y + 4.5)] + [150]
    for i in range(0, len(edges), 2):
        y0, y1 = edges[i], edges[i + 1]
        if y1 - y0 > 0.5:
            m.add(0, box(f"quay{i}", 30, y1 - y0, 1.0, (35, (y0 + y1) / 2, 0), STONE))
    for c, x in enumerate((-38, -16, 6)):
        for k in range(9):
            y = -132 + k * 33
            m.add(1, kura(f"kura{c}{k}", 14, 27, 6.0, (x, y, 0.6), a=0, ridge_y=True), "storehouses")
    for i, y in enumerate(ys[::2]):
        m.add(2, boat(f"boat{i}", 11, 3.0, (36, y, 0.1), a=180, cargo="#D9CBA0"), "boats")
    for i, (x, y) in enumerate([(20, -145), (20, 145), (-48, -148), (-48, 148)]):
        m.add(2, pine(f"pine{i}", 1.0, (x, y, 0.6), seed=i))
    return m


BUILDERS = {
    "edo/edo-castle": lambda: edo_castle("1800"),
    "edo/edo-castle-1460": lambda: edo_castle("1460"),
    "edo/edo-castle-1610": lambda: edo_castle("1610"),
    "edo/edo-castle-1872": lambda: edo_castle("1872"),
    "edo/nihonbashi": nihonbashi,
    "edo/ryogoku-bridge": ryogoku_bridge,
    "edo/sensoji": lambda: sensoji("1800"),
    "edo/sensoji-1460": lambda: sensoji("1460"),
    "edo/sensoji-1872": lambda: sensoji("1872"),
    "edo/kaneiji": lambda: kaneiji("1800"),
    "edo/kaneiji-1872": lambda: kaneiji("1872"),
    "edo/zojoji": zojoji,
    "edo/kanda-myojin": kanda_myojin,
    "edo/yushima-seido": yushima_seido,
    "edo/ekoin": ekoin,
    "edo/fish-market": fish_market,
    "edo/echigoya": echigoya,
    "edo/nakamura-za": nakamura_za,
    "edo/yoshiwara": yoshiwara,
    "edo/kaga-akamon": kaga_akamon,
    "edo/tsukiji-honganji": tsukiji_honganji,
    "edo/hie-shrine": hie_shrine,
    "edo/hinomi-yagura": hinomi_yagura,
    "edo/shimbashi-station": shimbashi_station,
    "edo/ginza-brick": ginza_brick,
    "edo/benten-do": benten_do,
    "edo/tomioka-hachiman": tomioka_hachiman,
    "edo/asakusa-okura": asakusa_okura,
}
