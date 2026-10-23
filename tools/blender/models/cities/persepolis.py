"""Persepolis landmark miniatures: the Takht with its double stair and towered parapet, the Apadana and the
Hall of a Hundred Columns with their double-bull columns, the Gate of All Nations with its bulls, the palaces of
Darius and Xerxes with their dark stone door frames, the treasury and barracks, the rock-cut royal tombs and a
pavilion palace in a paradise garden, intact, under construction and as burned ruins.

Conventions as worldkit: metres, origin at the ground centre of the footprint, +X east, +Y north, +Z up, main
front to the south (-Y); the landmark's rotation turns it on the map. Buildings on the terrace stand on a block
of the terrace TERR_H high so that they read as sitting on the Takht. Helpers build pieces at the origin;
bake() applies transforms so every object's origin is the world origin, turn() rotates about it.
"""
import math, random
import bpy
from chronokit import Model, box, cylinder, join, shade, mesh_from
from worldkit import lathe, frustum, tree
from archkit import copy_at, cyl_x

# ---------------------------------------------------------------- palette
STONE = "#B7AE9E"     # grey Persepolis limestone
STONE_D = "#9F9687"
STONE_L = "#CBC3B3"   # paving
COL = "#C9C1B0"       # column limestone
BULL = "#B2A894"
DSTONE = "#4D4844"    # polished dark stone of door and window frames
REL = "#ABA292"       # relief ground
FIG = "#8D8474"       # relief figures
BLUE = "#4F6A8E"
RED = "#A64B3B"
GILT = "#CFA64E"
MUD = "#C6A47C"       # mud-brick walls, plastered
MUD_D = "#AE8D66"
ROOF = "#A88B66"      # flat earth roofs
CEDAR = "#7A563A"
GLAZE = "#4E6E96"
CHAR = "#3D3530"
ASH = "#6C635A"
SOOT = "#7E766B"
EARTH = "#B89D77"
EARTH_D = "#A3885F"
ROCK = "#998F7F"
ROCK_L = "#B3A996"
WATERC = "#5F878C"
LEAF = "#6F8A5C"
CYPRESS = "#56704A"
TIMBER = "#8C6A4A"
WOODCOL = "#9C4E3A"   # plastered and painted wooden columns of the treasury
DARK = "#2E241C"
SAND = "#D2BE98"
TERR_H = 12.0


# ================================================================ basic helpers

def _sel(o):
    bpy.ops.object.select_all(action="DESELECT")
    o.select_set(True)
    bpy.context.view_layer.objects.active = o


def bake(o):
    if o is None:
        return None
    _sel(o)
    bpy.ops.object.transform_apply(location=True, rotation=True, scale=True)
    return o


def turn(o, deg, x=0.0, y=0.0, z=0.0):
    """Rotate about the world Z axis (degrees, counter-clockwise from above), then move."""
    bake(o)
    o.rotation_euler = (0.0, 0.0, math.radians(deg))
    o.location = (x, y, z)
    return bake(o)


def J(parts, name):
    parts = [p for p in parts if p is not None]
    if not parts:
        return None
    return bake(join(parts, name))


def copies(proto, locs, name, rots=None):
    """Copies of a piece built at the origin, at each (x, y, z) with an optional Z rotation (radians)."""
    bake(proto)
    objs = [copy_at(proto, loc, rots[i] if rots else 0.0, name=f"{name}{i}") for i, loc in enumerate(locs)]
    bpy.data.objects.remove(proto, do_unlink=True)
    return J(objs, name)


def B(name, x0, x1, y0, y1, z0, z1, color):
    """Box from extents."""
    return box(name, x1 - x0, y1 - y0, z1 - z0, ((x0 + x1) / 2, (y0 + y1) / 2, z0), color)


def slab(name, w, d, h=TERR_H, color=STONE, joints=True):
    """A block of the terrace under a building: masonry face with course lines and a paved top."""
    parts = [box(name, w, d, h, (0, 0, 0), color), box(name + "_pv", w - 0.3, d - 0.3, 0.12, (0, 0, h), STONE_L)]
    for k, z in enumerate((h * 0.36, h * 0.7)):
        parts.append(box(f"{name}_c{k}", w + 0.14, d + 0.14, 0.2, (0, 0, z), STONE_D))
    if joints:
        for side in (-1, 1):
            n = max(2, int(w / 6))
            for i in range(n):
                x = -w / 2 + (i + 0.5) * w / n
                parts.append(box(f"{name}_jx{side}{i}", 0.14, 0.1, h * 0.36, (x, side * (d / 2 + 0.03), h * (0.0 if i % 2 else 0.36)), STONE_D))
            n = max(2, int(d / 6))
            for i in range(n):
                y = -d / 2 + (i + 0.5) * d / n
                parts.append(box(f"{name}_jy{side}{i}", 0.1, 0.14, h * 0.36, (side * (w / 2 + 0.03), y, h * (0.0 if i % 2 else 0.36)), STONE_D))
    return J(parts, name)


def mound(name, x0, x1, y0, y1, h, color=EARTH, z=0.0):
    """A slumped wall or heap: a low frustum."""
    w, d = x1 - x0, y1 - y0
    return frustum(name, w + h * 0.8, d + h * 0.8, max(0.3, w * 0.55), max(0.3, d * 0.55), h, ((x0 + x1) / 2, (y0 + y1) / 2, z), color)


# ================================================================ crenellations, reliefs, doors

def merlon_run(name, a, b, z0, z1=None, size=1.5, t=0.55, color=MUD, gap=0.8):
    """Persepolitan stepped merlons along a segment (z rising from z0 to z1 for stair parapets)."""
    z1 = z0 if z1 is None else z1
    (ax, ay), (bx, by) = a, b
    L = math.hypot(bx - ax, by - ay)
    ang = math.atan2(by - ay, bx - ax)
    n = max(1, int(L / (size + gap)))
    parts = []
    for i in range(n):
        u = (i + 0.5) / n
        x, y, z = ax + (bx - ax) * u, ay + (by - ay) * u, z0 + (z1 - z0) * u
        parts.append(box(f"{name}{i}a", size, t, size * 0.45, (x, y, z), color, rot_z=ang))
        parts.append(box(f"{name}{i}b", size * 0.5, t, size * 0.45, (x, y, z + size * 0.45), color, rot_z=ang))
    return J(parts, name)


def merlon_rect(name, x0, x1, y0, y1, z, size=1.5, color=MUD, sides="SNWE", t=0.55):
    parts = []
    if "S" in sides:
        parts.append(merlon_run(name + "s", (x0, y0 + t / 2), (x1, y0 + t / 2), z, size=size, color=color, t=t))
    if "N" in sides:
        parts.append(merlon_run(name + "n", (x0, y1 - t / 2), (x1, y1 - t / 2), z, size=size, color=color, t=t))
    if "W" in sides:
        parts.append(merlon_run(name + "w", (x0 + t / 2, y0 + 1.5), (x0 + t / 2, y1 - 1.5), z, size=size, color=color, t=t))
    if "E" in sides:
        parts.append(merlon_run(name + "e", (x1 - t / 2, y0 + 1.5), (x1 - t / 2, y1 - 1.5), z, size=size, color=color, t=t))
    return J(parts, name)


def relief_band(name, x0, x1, yf, z, h, every=1.15, color=REL, fig=FIG, paint=True):
    """A register of relief on a wall facing -Y at y = yf: a ground band with a procession of raised figures."""
    parts = [box(name, x1 - x0, 0.16, h, ((x0 + x1) / 2, yf - 0.08, z), color)]
    n = max(1, int((x1 - x0) / every))
    for i in range(n):
        x = x0 + (i + 0.5) * (x1 - x0) / n
        c = (BLUE if i % 7 == 3 else RED if i % 7 == 5 else fig) if paint else fig
        parts.append(box(f"{name}f{i}", 0.38, 0.13, h * 0.76, (x, yf - 0.2, z + h * 0.1), c))
    return J(parts, name)


def door_frame(name, w, h, depth, color=DSTONE, jamb=0.8, z0=0.0, panel=True, cornice=True):
    """A Persepolitan stone door or window frame facing -Y: jambs, lintel and an Egyptian cavetto cornice."""
    W = w + 2 * jamb
    parts = [box(name + "_j1", jamb, depth, h, (-(w + jamb) / 2, 0, z0), color),
             box(name + "_j2", jamb, depth, h, ((w + jamb) / 2, 0, z0), color),
             box(name + "_l", W, depth, 0.7, (0, 0, z0 + h), color)]
    if cornice:
        parts.append(frustum(name + "_cv", W, depth, W * 1.14, depth * 1.35, 0.7, (0, 0, z0 + h + 0.7), color))
        parts.append(box(name + "_ct", W * 1.16, depth * 1.38, 0.22, (0, 0, z0 + h + 1.4), color))
    if panel:
        parts.append(box(name + "_p", w, depth * 0.96, h, (0, 0, z0), DARK))
    return J(parts, name)


def frame_at(name, w, h, depth, x, y, z, face="S", **kw):
    o = door_frame(name, w, h, depth, **kw)
    return turn(o, {"S": 0, "N": 180, "E": 90, "W": -90}[face], x, y, z)


# ================================================================ columns

def star_shaft(name, r0, r1, h, flutes=16, color=COL, z0=0.0, depth=0.1):
    """A fluted shaft: the section alternates arris and flute."""
    n = flutes * 2
    verts, faces = [], []
    for z, r in ((0.0, r0), (h, r1)):
        for i in range(n):
            a = math.tau * i / n
            rr = r if i % 2 == 0 else r * (1 - depth)
            verts.append((rr * math.cos(a), rr * math.sin(a), z0 + z))
    for i in range(n):
        j = (i + 1) % n
        faces.append((i, j, n + j, n + i))
    faces.append(tuple(range(n))[::-1])
    faces.append(tuple(range(n, 2 * n)))
    return mesh_from(name, verts, faces, (0, 0, 0), color)


def bull_pair(name, s, z, color=BULL, simple=False):
    """Two bull foreparts back to back along X (the Persepolitan double-bull protome)."""
    parts = []
    for sx in (-1, 1):
        parts.append(box(f"{name}b{sx}", 2.0 * s, 1.4 * s, 1.35 * s, (sx * 1.1 * s, 0, z + 0.55 * s), color))
        parts.append(box(f"{name}h{sx}", 0.95 * s, 0.85 * s, 1.0 * s, (sx * 2.45 * s, 0, z + 1.2 * s), color))
        if not simple:
            parts.append(box(f"{name}l{sx}", 0.9 * s, 1.25 * s, 0.6 * s, (sx * 1.75 * s, 0, z), color))
            parts.append(box(f"{name}m{sx}", 0.5 * s, 0.6 * s, 0.5 * s, (sx * 3.05 * s, 0, z + 1.2 * s), color))
            parts.append(box(f"{name}k{sx}", 0.22 * s, 1.5 * s, 0.22 * s, (sx * 2.4 * s, 0, z + 2.2 * s), shade(color, -0.1)))
    return J(parts, name)


def persian_column(name, h, r=0.8, color=COL, bull=BULL, detail=2, flutes=16, bulls=True):
    """A Persepolitan column: square plinth, bell base, fluted shaft, palm capital, volute block, double bulls.
    detail 2 = hero, 1 = plain bell base and simple capital. h is the height to the top of the bulls' backs."""
    s = r / 0.8
    parts = [box(name + "_pl", 2.6 * s, 2.6 * s, 0.3 * s, (0, 0, 0), shade(color, -0.05))]
    if detail >= 2:
        base_h = 1.7 * s
        parts.append(lathe(name + "_bs", [(1.2 * s, 0.3 * s), (1.15 * s, 0.5 * s), (0.95 * s, 1.05 * s), (0.82 * s, 1.4 * s), (0.95 * s, 1.5 * s), (0.82 * s, 1.7 * s)], color=color, verts=12))
        cap_h = (5.6 if bulls else 3.4) * s
    else:
        base_h = 1.1 * s
        parts.append(cylinder(name + "_bs", 1.05 * s, 0.8 * s, (0, 0, 0.3 * s), color, verts=8, r_top=0.8 * s))
        cap_h = (3.8 if bulls else 1.6) * s
    shaft_h = max(1.0, h - base_h - cap_h)
    parts.append(star_shaft(name + "_sh", r, r * 0.9, shaft_h, flutes if detail >= 2 else 10, color, base_h))
    z = base_h + shaft_h
    if detail >= 2:
        parts.append(lathe(name + "_pm", [(0.72 * s, 0), (0.9 * s, 0.35 * s), (1.2 * s, 1.1 * s), (1.25 * s, 1.4 * s), (0.75 * s, 1.5 * s)], (0, 0, z), color, verts=12))
        parts.append(box(name + "_vb", 1.3 * s, 1.3 * s, 1.9 * s, (0, 0, z + 1.5 * s), color))
        for k, zz in enumerate((z + 1.5 * s, z + 3.2 * s)):
            parts.append(box(f"{name}_vr{k}", 1.55 * s, 1.55 * s, 0.22 * s, (0, 0, zz), shade(color, -0.08)))
        zb = z + 3.4 * s
    else:
        parts.append(frustum(name + "_pm", 1.3 * s, 1.3 * s, 1.9 * s, 1.9 * s, 1.0 * s, (0, 0, z), color))
        parts.append(box(name + "_vb", 1.3 * s, 1.3 * s, 0.6 * s, (0, 0, z + 1.0 * s), color))
        zb = z + 1.6 * s
    if bulls:
        parts.append(bull_pair(name + "_bl", s, zb, bull, simple=detail < 2))
    return J(parts, name)


def column_base(name, r=0.8, color=COL, detail=1):
    s = r / 0.8
    parts = [box(name + "_pl", 2.6 * s, 2.6 * s, 0.3 * s, (0, 0, 0), shade(color, -0.05))]
    if detail >= 2:
        parts.append(lathe(name + "_bs", [(1.2 * s, 0.3 * s), (1.15 * s, 0.5 * s), (0.95 * s, 1.05 * s), (0.82 * s, 1.4 * s), (0.95 * s, 1.5 * s), (0.82 * s, 1.7 * s)], color=color, verts=10))
    else:
        parts.append(cylinder(name + "_bs", 1.05 * s, 0.7 * s, (0, 0, 0.3 * s), color, verts=8, r_top=0.82 * s))
    return J(parts, name)


def drum(name, r, L, x, y, z, ang=0.0, color=COL):
    """A fallen column drum lying on its side."""
    o = cyl_x(name, r, L, (0, 0, r), color, verts=10)
    return turn(o, math.degrees(ang), x, y, z)


def col_grid(xs, ys):
    return [(x, y) for x in xs for y in ys]


# ================================================================ stairs

def parapet_slope(name, x0, x1, zb, zt, y, t=0.6, extra=1.1, color=STONE):
    """A side wall of a stair flight, rising with the steps (a trapezoid in XZ)."""
    v = [(x0, y - t / 2, 0), (x1, y - t / 2, 0), (x1, y - t / 2, zt + extra), (x0, y - t / 2, zb + extra),
         (x0, y + t / 2, 0), (x1, y + t / 2, 0), (x1, y + t / 2, zt + extra), (x0, y + t / 2, zb + extra)]
    f = [(0, 1, 2, 3), (4, 7, 6, 5), (0, 4, 5, 1), (1, 5, 6, 2), (2, 6, 7, 3), (3, 7, 4, 0)]
    return mesh_from(name, v, f, (0, 0, 0), color)


def flight(name, x0, x1, zb, zt, ya, yb, n, color=STONE, parapet_y=None, merl=True, extra=1.1, para_color=None, nosing=False):
    """Steps along X from x0 (bottom, height zb) to x1 (top, height zt), between ya and yb, solid to the ground."""
    parts = []
    dx = (x1 - x0) / n
    rise = (zt - zb) / n
    for i in range(n):
        xa = x0 + dx * i
        parts.append(box(f"{name}{i}", abs(dx), yb - ya, zb + rise * (i + 1), (xa + dx / 2, (ya + yb) / 2, 0), color))
        if nosing:
            parts.append(box(f"{name}{i}n", 0.06, yb - ya - 0.2, 0.05, (xa + 0.03 * (1 if dx > 0 else -1), (ya + yb) / 2, zb + rise * (i + 1)), shade(color, -0.12)))
    if parapet_y is not None:
        pc = para_color or shade(color, -0.04)
        parts.append(parapet_slope(name + "_pp", x0, x1, zb, zt, parapet_y, color=pc, extra=extra))
        if merl:
            parts.append(merlon_run(name + "_pm", (x0, parapet_y), (x1, parapet_y), zb + extra, zt + extra, size=1.0, t=0.5, color=pc, gap=0.5))
    return J(parts, name)


def stair_reliefs(name, x0, x1, zb, zt, yf, base=0.3, reg=0.75, gap=0.15, paint=True):
    """Relief registers on the side wall of a flight facing -Y (bottom at x0, top at x1), each running as far
    down the slope as the parapet is tall enough to hold it."""
    parts = []
    z, k = base, 0
    while z + reg < zt + 0.6:
        need = z + reg + 0.2 - 1.1
        if need >= zt:
            break
        xs = x0 if need <= zb else x0 + (x1 - x0) * (need - zb) / (zt - zb)
        a, b = sorted((xs, x1))
        if b - a > 1.5:
            parts.append(relief_band(f"{name}{k}", a + 0.3, b - 0.3, yf, z, reg, paint=paint))
        z += reg + gap
        k += 1
    return J(parts, name)


# ================================================================ figures

def lamassu(name, human=True, s=1.0, color=STONE):
    """A blocky winged bull (human-headed lamassu if human) on a plinth, facing -Y, at the origin."""
    p = [box(name + "_pl", 2.0 * s, 5.6 * s, 0.5 * s, (0, 0.3 * s, 0), shade(color, -0.06)),
         box(name + "_bd", 1.7 * s, 4.0 * s, 2.0 * s, (0, 0.6 * s, 2.3 * s), color),
         box(name + "_ch", 1.6 * s, 1.2 * s, 2.8 * s, (0, -1.7 * s, 1.9 * s), color)]
    for k, (lx, ly) in enumerate(((-0.55, -1.8), (0.55, -1.8), (-0.55, 2.0), (0.55, 2.0))):
        p.append(box(f"{name}_lg{k}", 0.5 * s, 0.7 * s, 1.9 * s, (lx * s, ly * s, 0.5 * s), color))
    if human:
        p.append(box(name + "_hd", 1.1 * s, 1.1 * s, 1.3 * s, (0, -2.0 * s, 4.7 * s), color))
        p.append(box(name + "_br", 0.95 * s, 0.6 * s, 1.3 * s, (0, -2.45 * s, 3.9 * s), shade(color, -0.12)))
        p.append(cylinder(name + "_cr", 0.62 * s, 1.1 * s, (0, -2.0 * s, 6.0 * s), shade(color, -0.04), verts=10))
        p.append(box(name + "_hr", 1.4 * s, 0.25 * s, 0.25 * s, (0, -2.0 * s, 6.1 * s), shade(color, -0.12)))
    else:
        p.append(box(name + "_hd", 1.0 * s, 1.6 * s, 1.15 * s, (0, -2.4 * s, 4.4 * s), color))
        p.append(box(name + "_hr", 2.0 * s, 0.28 * s, 0.28 * s, (0, -2.0 * s, 5.55 * s), shade(color, -0.12)))
    for sx in (-1, 1):
        x = sx * 0.95 * s
        v = [(x - 0.1 * s, -1.3 * s, 3.4 * s), (x - 0.1 * s, 2.4 * s, 4.6 * s), (x - 0.1 * s, 2.6 * s, 3.5 * s), (x - 0.1 * s, -0.8 * s, 2.6 * s)]
        v += [(vx + 0.2 * s, vy, vz) for vx, vy, vz in v]
        p.append(mesh_from(f"{name}_w{sx}", v, [(0, 1, 2, 3), (7, 6, 5, 4), (0, 4, 5, 1), (1, 5, 6, 2), (2, 6, 7, 3), (3, 7, 4, 0)], (0, 0, 0), shade(color, -0.07)))
    return J(p, name)


def crane(name, x, y, z, h, ang=0.0):
    """A timber A-frame derrick with a hanging rope."""
    p = [box(name + "_a", 0.35, 0.35, h, (-1.8, 0, 0), TIMBER), box(name + "_b", 0.35, 0.35, h, (1.8, 0, 0), TIMBER),
         box(name + "_c", 4.6, 0.4, 0.4, (0, 0, h), TIMBER), box(name + "_r", 0.08, 0.08, h * 0.5, (0, 0, h * 0.5), DARK),
         box(name + "_s", 0.3, 4.0, 0.3, (0, 0, h * 0.3), TIMBER)]
    return turn(J(p, name), ang, x, y, z)


def scaffold(name, x, y, z, w, h):
    p = []
    for sx in (-1, 1):
        for sy in (-1, 1):
            p.append(box(f"{name}p{sx}{sy}", 0.25, 0.25, h, (sx * w / 2, sy * w / 2, 0), TIMBER))
    for k in range(1, int(h / 4) + 1):
        p.append(box(f"{name}d{k}", w + 0.5, 1.0, 0.2, (0, -w / 2, k * 4), TIMBER))
        p.append(box(f"{name}e{k}", 1.0, w + 0.5, 0.2, (w / 2, 0, k * 4), TIMBER))
    return turn(J(p, name), 0, x, y, z)


# ================================================================ the Takht and the great stair

def takht(variant="460"):
    """A stretch of the terrace's west face with the double stair. Builder: face along X, plain to -Y,
    north end of the terrace at x = -66 (rotation 90 turns the face to the west)."""
    m = Model("takht")
    H, yf, X0, X1 = TERR_H, -4.0, -66.0, 68.0
    cx, cy, w, d = (X0 + X1) / 2, (yf + 20) / 2, X1 - X0, 20 - yf
    p = [B("t_core", X0, X1, yf, 20, 0, H, STONE), B("t_pave", X0 + 0.2, X1, yf + 0.2, 20, H, H + 0.12, STONE_L)]
    # masonry: courses of big blocks with staggered joints on the west face and the north end
    NC = 8
    for k in range(1, NC):
        z = H * k / NC
        for a0, b0 in ((X0, -31.5), (31.5, X1)):
            p.append(B(f"t_cf{k}{a0}", a0 - 0.05, b0, yf - 0.1, yf, z - 0.07, z + 0.07, STONE_D))
        p.append(B(f"t_cn{k}", X0 - 0.1, X0, yf, 20, z - 0.07, z + 0.07, STONE_D))
    rj = random.Random(4)
    for k in range(NC):
        za, zb_ = H * k / NC, H * (k + 1) / NC
        x = X0 + rj.uniform(0.5, 2.5)
        while x < X1 - 1:
            if not -31.5 < x < 31.5:
                p.append(B(f"t_j{k}_{x:.0f}", x, x + 0.12, yf - 0.1, yf, za, zb_, STONE_D))
            x += rj.uniform(1.8, 3.4)
        y = yf + rj.uniform(0.5, 2.5)
        while y < 20 - 1:
            p.append(B(f"t_jn{k}_{y:.0f}", X0 - 0.1, X0, y, y + 0.12, za, zb_, STONE_D))
            y += rj.uniform(1.8, 3.4)
    p.append(B("t_plinth", X0 - 0.3, X1, yf - 0.3, yf, 0, 0.6, STONE_D))
    for k in range(1, 5):
        y = yf + 24.0 * k / 5
        p.append(B(f"t_pvx{k}", X0 + 0.5, X1, y - 0.06, y + 0.06, H + 0.12, H + 0.16, STONE_D))
    x = X0 + 4.0
    while x < X1:
        p.append(B(f"t_pvy{x:.0f}", x - 0.06, x + 0.06, yf + 0.3, 20, H + 0.12, H + 0.16, STONE_D))
        x += 4.0
    m.add(0, J(p, "terrace"), "terrace")

    # the double stair: lower flights climb outward from the centre to landings, upper flights return inward
    s = []
    n = 60
    built_upper = variant != "500"
    for sx in (-1, 1):
        s.append(flight(f"lo{sx}", sx * 3.0, sx * 24.5, 0.0, 6.0, -20.0, -12.4, n, STONE, parapet_y=-19.7, merl=variant == "460", nosing=True))
        s.append(B(f"land{sx}", min(sx * 24.5, sx * 31.5), max(sx * 24.5, sx * 31.5), -20.0, yf, 0, 6.0, STONE))
        s.append(B(f"land_p{sx}", min(sx * 24.5, sx * 31.5), max(sx * 24.5, sx * 31.5), -20.0, -19.4, 6.0, 7.1, shade(STONE, -0.04)))
        s.append(B(f"land_e{sx}", min(sx * 31.5, sx * 30.9), max(sx * 31.5, sx * 30.9), -20.0, yf, 6.0, 7.1, shade(STONE, -0.04)))
        if built_upper:
            s.append(flight(f"up{sx}", sx * 24.5, sx * 3.0, 6.0, H, -12.0, yf, n, STONE, parapet_y=-12.2, merl=variant == "460", nosing=True))
        else:
            s.append(flight(f"up{sx}", sx * 24.5, sx * 17.0, 6.0, 8.0, -12.0, yf, 10, STONE, parapet_y=-12.2, merl=False))
        if variant == "460":
            s.append(merlon_run(f"land_m{sx}", (sx * 24.8, -19.7), (sx * 31.2, -19.7), 7.1, size=1.0, t=0.5, color=shade(STONE, -0.04), gap=0.5))
    s.append(B("top", -3.0, 3.0, -12.0, yf, 0, H, STONE))
    for k in range(1, 8):
        z = H * k / 8
        s.append(B(f"top_c{k}", -3.0, 3.0, -12.1, -12.0, z - 0.06, z + 0.06, STONE_D))
        if z < 6.0:
            for sx in (-1, 1):
                xa, xb = sorted((sx * 31.5, sx * 31.6))
                s.append(B(f"land_c{k}{sx}", xa, xb, -20.0, yf, z - 0.06, z + 0.06, STONE_D))
                xa, xb = sorted((sx * 24.5, sx * 31.5))
                s.append(B(f"land_f{k}{sx}", xa, xb, -20.1, -20.0, z - 0.06, z + 0.06, STONE_D))
    for sx in (-1, 1):
        s.append(B(f"top_p{sx}", min(sx * 3.0, sx * 4.2), max(sx * 3.0, sx * 4.2), -12.4, -10.6, H, H + 2.2, shade(STONE, -0.04)))
        s.append(merlon_run(f"top_m{sx}", (sx * 3.6, -11.5), (sx * 3.6, -11.5 + 0.01), H + 2.2, size=1.0, t=1.6, color=shade(STONE, -0.04)))
    s.append(B("top_f", -3.1, 3.1, -12.1, -11.9, H * 0.62, H * 0.62 + 0.22, STONE_D))
    m.add(0, J(s, "stair"), "terrace")

    # parapet, towers and the fortification turning east at the north end
    q = []
    if variant == "460":
        for a, b in ((X0 + 4, -9.0), (9.0, X1)):
            q.append(B(f"pw{a}", a, b, yf, yf + 2.2, H, H + 4.5, MUD))
            q.append(merlon_run(f"pwm{a}", (a, yf + 0.4), (b, yf + 0.4), H + 4.5, size=1.1, color=MUD, gap=0.6))
            q.append(B(f"pwg{a}", a, b, yf - 0.05, yf + 2.25, H + 3.4, H + 3.9, GLAZE))
        for tx in (X0 + 4.0, -40.0, -6.0, 6.0, 38.0, X1 - 4):
            q.append(B(f"tw{tx}", tx - 3.5, tx + 3.5, yf, yf + 6.0, H, H + 9.0, shade(MUD, -0.04)))
            q.append(B(f"twc{tx}", tx - 3.7, tx + 3.7, yf - 0.2, yf + 6.2, H + 8.4, H + 9.0, MUD_D))
            q.append(B(f"twg{tx}", tx - 3.55, tx + 3.55, yf - 0.05, yf + 6.05, H + 7.2, H + 7.7, GLAZE))
            q.append(merlon_rect(f"twm{tx}", tx - 3.5, tx + 3.5, yf, yf + 6.0, H + 9.0, size=1.1, color=shade(MUD, -0.04)))
            for dx in (-1.6, 1.6):
                q.append(frame_at(f"twd{tx}{dx}", 0.9, 1.8, 0.5, tx + dx, yf, H + 4.6, "S"))
        q.append(B("nw", X0, X0 + 3.0, yf + 6, 20, H, H + 7.5, MUD))
        q.append(merlon_run("nwm", (X0 + 0.4, yf + 6), (X0 + 0.4, 20), H + 7.5, size=1.4, color=MUD))
        q.append(B("nt", X0, X0 + 8.0, yf, yf + 8.0, H, H + 12.0, shade(MUD, -0.06)))
        q.append(merlon_rect("ntm", X0, X0 + 8.0, yf, yf + 8.0, H + 12.0, size=1.3, color=shade(MUD, -0.06)))
        q.append(B("nt2", X0, X0 + 7.0, 13.0, 20.0, H, H + 10.5, shade(MUD, -0.04)))
        q.append(merlon_rect("nt2m", X0, X0 + 7.0, 13.0, 20.0, H + 10.5, size=1.2, color=shade(MUD, -0.04)))
        m.add(1, J(q, "parapet"), "fortification")
    elif variant == "500":
        # the face is up but the parapet is only begun; the upper flights are a ramp of earth with scaffolding
        q.append(B("pw_a", X0 + 4, -30.0, yf, yf + 2.2, H, H + 2.0, MUD))
        q.append(B("nt", X0, X0 + 8.0, yf, yf + 8.0, H, H + 5.0, shade(MUD, -0.06)))
        for sx in (-1, 1):
            v = [(sx * 17.0, -12.0, 0), (sx * 3.0, -12.0, 0), (sx * 3.0, -12.0, H), (sx * 17.0, -12.0, 8.0),
                 (sx * 17.0, yf, 0), (sx * 3.0, yf, 0), (sx * 3.0, yf, H), (sx * 17.0, yf, 8.0)]
            q.append(mesh_from(f"ramp{sx}", v, [(0, 1, 2, 3), (7, 6, 5, 4), (0, 4, 5, 1), (1, 5, 6, 2), (2, 6, 7, 3), (3, 7, 4, 0)], (0, 0, 0), EARTH))
            for k in range(4):
                xx = sx * (5.0 + k * 3.4)
                q.append(box(f"sc{sx}{k}", 0.25, 0.25, 10.5, (xx, -12.6, 0), TIMBER))
            q.append(box(f"scb{sx}", 13.0, 0.9, 0.2, (sx * 10.0, -12.8, 6.5), TIMBER))
            q.append(box(f"scb2{sx}", 13.0, 0.9, 0.2, (sx * 10.0, -12.8, 9.5), TIMBER))
        for k, (bx_, by_) in enumerate(((-44, -16), (-40, -17), (-46, -12.5), (40, -15), (45, -13), (50, -17))):
            q.append(box(f"blk{k}", 2.6, 1.6, 1.2, (bx_, by_, 0), STONE_L, rot_z=0.3 * k))
            if k % 2 == 0:
                q.append(box(f"blk{k}b", 2.2, 1.4, 1.0, (bx_, by_, 1.2), STONE_L, rot_z=0.3 * k + 0.2))
        q.append(box("sledge", 4.0, 2.0, 0.3, (-36, -16, 0), TIMBER))
        q.append(box("sledge_b", 3.0, 1.7, 1.4, (-36, -16, 0.3), STONE_L))
        q.append(crane("cr", 30.0, -8.0, H, 8.0, 0))
        m.add(1, J(q, "works"), "fortification")
    else:
        # ruin: the mud-brick parapet and towers melted into mounds, earth washed against the foot of the stair
        for k, (a, b) in enumerate(((X0 + 4, -36), (-34, -9), (9, 30), (32, X1 - 1))):
            q.append(mound(f"pm{k}", a, b, yf + 0.2, yf + 2.2, 1.4 + 0.5 * (k % 2), EARTH, H))
        for tx in (X0 + 4.0, -40.0, 38.0):
            q.append(mound(f"tm{tx}", tx - 3, tx + 3, yf + 0.5, yf + 5.5, 3.0, EARTH_D, H))
        q.append(mound("nm", X0 + 0.3, X0 + 6.0, yf + 0.5, 19.5, 4.0, EARTH_D, H))
        q.append(B("silt", -34.0, 34.0, -20.0, -17.5, 0, 0.8, EARTH))
        q.append(frustum("silt_c", 8.0, 7.0, 5.0, 3.0, 1.2, (0, -16.0, 0), EARTH))
        for k, (bx_, by_) in enumerate(((-45, -15), (22, -18), (48, -14))):
            q.append(box(f"fallen{k}", 1.8, 1.2, 0.9, (bx_, by_, 0), STONE_D, rot_z=0.5 * k))
        m.add(1, J(q, "ruin"), "fortification")
    return m


# ================================================================ Apadana

AP_C = 6.0                         # centre of the building (x and y) inside the 124 m footprint
AP_XS = [-19.0, -9.0, 1.0, 11.0, 21.0, 31.0]
AP_PLAT = 3.0


def apadana_stair(name, paint=True, carved=1.0):
    """One of the Apadana's relief stairs, built facing -Y with its back at y = 0: two flights rising to a
    central landing and long relief wings with stepped merlons. carved: share of the wing reliefs finished."""
    p = []
    for sx in (-1, 1):
        p.append(flight(f"{name}f{sx}", sx * 16.0, sx * 4.0, 0.0, AP_PLAT, -12.0, -6.0, 14, STONE, parapet_y=-11.7, extra=1.2))
        p.append(stair_reliefs(f"{name}fr{sx}", sx * 16.0, sx * 4.0, 0.0, AP_PLAT, -12.0, paint=paint))
        p.append(B(f"{name}bk{sx}", min(sx * 4, sx * 16), max(sx * 4, sx * 16), -6.0, 0, 0, AP_PLAT, STONE))
        # wings
        x0, x1 = (sx * 16.0, sx * 46.0) if sx > 0 else (sx * 46.0, sx * 16.0)
        p.append(B(f"{name}w{sx}", x0, x1, -4.0, 0, 0, AP_PLAT + 1.2, STONE))
        p.append(merlon_run(f"{name}wm{sx}", (x0, -3.7), (x1, -3.7), AP_PLAT + 1.2, size=1.1, t=0.5, color=shade(STONE, -0.04), gap=0.5))
        span = (x1 - x0) * carved
        if span > 2:
            xa, xb = (x0, x0 + span) if sx < 0 else (x1 - span, x1)
            for k in range(3):
                p.append(relief_band(f"{name}wr{sx}{k}", xa + 0.6, xb - 0.6, -4.0, 0.35 + k * 1.3, 1.1, paint=paint))
        # end panels with the lion attacking a bull
        p.append(B(f"{name}lb{sx}", sx * 16.0 - 0.6, sx * 16.0 + 0.6, -12.2, -11.9, 0.5, 1.7, FIG))
    p.append(B(f"{name}ld", -4.0, 4.0, -12.0, 0, 0, AP_PLAT, STONE))
    p.append(B(f"{name}lp", -4.0, 4.0, -12.0, -11.4, AP_PLAT, AP_PLAT + 1.2, shade(STONE, -0.04)))
    p.append(merlon_run(f"{name}lm", (-4.0, -11.7), (4.0, -11.7), AP_PLAT + 1.2, size=1.1, t=0.5, color=shade(STONE, -0.04), gap=0.5))
    p.append(relief_band(f"{name}lr", -3.5, 3.5, -12.0, 0.4, 2.2, every=1.4, paint=paint))
    return J(p, name)


def apadana(variant="460"):
    m = Model("apadana")
    z0 = TERR_H + AP_PLAT
    c = AP_C
    base = [slab("ap_slab", 124, 124), B("ap_plat", -50, 62, -50, 62, TERR_H, z0, STONE),
            B("ap_plat_c", -50.15, 62.15, -50.15, 62.15, z0 - 0.5, z0 - 0.25, STONE_D), B("ap_floor", -48, 60, -48, 60, z0, z0 + 0.06, STONE_L)]
    carved = 0.45 if variant == "500" else 1.0
    st = apadana_stair("ap_ns", paint=variant in ("460", "500"), carved=carved if variant != "500" else 0.0)
    base.append(turn(st, 0, c, -50.0, TERR_H))
    st = apadana_stair("ap_es", paint=variant in ("460", "500"), carved=carved)
    base.append(turn(st, -90, -50.0, c, TERR_H))
    m.add(0, J(base, "platform"), "platform")

    hall = col_grid([x + c - 6 for x in AP_XS], [y + c - 6 for y in AP_XS])
    port_s = col_grid([x + c - 6 for x in AP_XS], [-43.5, -33.5])
    port_w = col_grid([-43.5, -33.5], [y + c - 6 for y in AP_XS])
    port_e = col_grid([45.5, 55.5], [y + c - 6 for y in AP_XS])
    porticoes = port_s + port_w + port_e
    CH = 19.5
    rnd = random.Random(7)

    if variant == "460":
        cols = copies(persian_column("ap_col", CH, 0.8, detail=2), [(x, y, z0) for x, y in porticoes], "ap_cols")
        w = [B("ap_hall", -29, 41, -29, 41, z0, z0 + CH + 0.6, MUD),
             B("ap_store", -29, 41, 41, 60, z0, z0 + 13.0, MUD_D)]
        for k, (x, y) in enumerate(((-38.5, -38.5), (50.5, -38.5), (-38.5, 50.5), (50.5, 50.5))):
            w.append(B(f"ap_tw{k}", x - 9.5, x + 9.5, y - 9.5, y + 9.5, z0, z0 + 28.0, shade(MUD, -0.03)))
            w.append(B(f"ap_twg{k}", x - 9.6, x + 9.6, y - 9.6, y + 9.6, z0 + 23.0, z0 + 24.2, GLAZE))
            w.append(B(f"ap_twg2{k}", x - 9.62, x + 9.62, y - 9.62, y + 9.62, z0 + 23.4, z0 + 23.8, GILT))
            w.append(B(f"ap_twc{k}", x - 9.9, x + 9.9, y - 9.9, y + 9.9, z0 + 27.2, z0 + 28.0, MUD_D))
            w.append(merlon_rect(f"ap_twm{k}", x - 9.5, x + 9.5, y - 9.5, y + 9.5, z0 + 28.0, size=1.6, color=shade(MUD, -0.03)))
            for face, (fx, fy) in (("S", (x, y - 9.5)), ("N", (x, y + 9.5)), ("W", (x - 9.5, y)), ("E", (x + 9.5, y))):
                if (face == "S" and y > 0) or (face == "N" and y < 0) or (face == "W" and x > 0) or (face == "E" and x < 0):
                    continue
                w.append(frame_at(f"ap_tww{k}{face}", 2.0, 3.2, 1.2, fx, fy, z0 + 16.0, face))
                w.append(frame_at(f"ap_twv{k}{face}", 2.0, 3.2, 1.2, fx, fy, z0 + 7.0, face))
        for face, (fx, fy) in (("S", (c, -29.0)), ("W", (-29.0, c)), ("E", (41.0, c))):
            w.append(frame_at(f"ap_door{face}", 4.0, 9.0, 1.6, fx, fy, z0, face))
            for off in (-16.0, 16.0):
                ox, oy = (fx + off, fy) if face == "S" else (fx, fy + off)
                w.append(frame_at(f"ap_win{face}{off}", 2.4, 4.2, 1.4, ox, oy, z0 + 3.0, face))
        w.append(frame_at("ap_doorN", 3.0, 6.5, 1.4, c, 60.0, z0, "N"))
        m.add(1, J([cols] + w, "hall"), "columns")
        zr = z0 + CH
        r = [B("ap_roofA", -48.5, 60.5, -29, 41, zr, zr + 1.6, ROOF), B("ap_roofB", -29, 41, -48.5, -29, zr, zr + 1.6, ROOF),
             B("ap_beamS", -29, 41, -48.6, -47.6, zr - 1.2, zr, CEDAR), B("ap_beamW", -48.6, -47.6, -29, 41, zr - 1.2, zr, CEDAR),
             B("ap_beamE", 59.6, 60.6, -29, 41, zr - 1.2, zr, CEDAR),
             B("ap_cornS", -29, 41, -48.9, -48.3, zr + 1.0, zr + 1.6, BLUE), B("ap_cornW", -48.9, -48.3, -29, 41, zr + 1.0, zr + 1.6, BLUE),
             B("ap_cornE", 60.3, 60.9, -29, 41, zr + 1.0, zr + 1.6, BLUE)]
        r.append(merlon_run("ap_rmS", (-28.5, -48.2), (40.5, -48.2), zr + 1.6, size=1.6))
        r.append(merlon_run("ap_rmW", (-48.2, -28.5), (-48.2, 40.5), zr + 1.6, size=1.6))
        r.append(merlon_run("ap_rmE", (60.2, -28.5), (60.2, 40.5), zr + 1.6, size=1.6))
        r.append(merlon_rect("ap_rmSt", -29, 41, 41, 60, z0 + 13.0, size=1.4, color=MUD_D, sides="N"))
        m.add(2, J(r, "roof"), "roof")
    elif variant == "500":
        done = port_s + [p for p in hall if p[1] < -5]
        rising = [p for p in hall if p[1] >= -5]
        cols = copies(persian_column("ap_col", CH, 0.8, detail=2), [(x, y, z0) for x, y in done], "ap_cols")
        parts = [cols]
        partial = []
        for k, (x, y) in enumerate(rising):
            hh = rnd.choice([0, 0, 3.5, 6.0, 9.0, 12.0])
            parts.append(turn(column_base(f"ap_b{k}", 0.8, detail=2), 0, x, y, z0))
            if hh:
                parts.append(star_shaft(f"ap_ps{k}", 0.8, 0.78, hh, 16, COL, z0 + 1.7))
                parts[-1] = turn(parts[-1], 0, x, y, 0)
        for k, (x, y) in enumerate(port_w):
            parts.append(turn(column_base(f"ap_bw{k}", 0.8, detail=2), 0, x, y, z0))
        for k, (x, y) in enumerate(port_e):
            parts.append(turn(column_base(f"ap_be{k}", 0.8, detail=1), 0, x, y, z0))
        parts.append(B("ap_ftS", -29, 41, -29, -24, z0, z0 + 1.6, MUD))
        parts.append(B("ap_ftW", -29, -24, -24, 41, z0, z0 + 1.6, MUD))
        parts.append(B("ap_ftE", 36, 41, -24, 41, z0, z0 + 1.0, MUD))
        for k, (x, y) in enumerate(((-38.5, -38.5), (50.5, -38.5))):
            parts.append(B(f"ap_tw{k}", x - 9.5, x + 9.5, y - 9.5, y + 9.5, z0, z0 + 7.0 + 3 * k, shade(MUD, -0.03)))
        parts.append(crane("ap_cr1", 11.0, 16.0, z0, 22.0, 0))
        parts.append(crane("ap_cr2", 21.0, 26.0, z0, 22.0, 90))
        parts.append(crane("ap_cr3", -38.5, 21.0, z0, 18.0, 90))
        parts.append(scaffold("ap_sc1", 1.0, 26.0, z0, 3.4, 16.0))
        parts.append(scaffold("ap_sc2", 31.0, 6.0, z0, 3.4, 12.0))
        for k in range(7):
            parts.append(drum(f"ap_dr{k}", 0.8, 1.8, -15 + 7 * k, 50.0 + (k % 2) * 4, z0, 0.4 * k))
        parts.append(B("ap_capblk", 0, 5.0, 46.0, 48.6, z0, z0 + 2.4, STONE_L))
        parts.append(B("ap_capblk2", 9.0, 13.5, 47.0, 49.4, z0, z0 + 2.0, STONE_L))
        m.add(1, J(parts, "building"), "columns")
    elif variant == "burned":
        allc = porticoes + hall
        fallen = set(rnd.sample(range(len(allc)), 10))
        stand = [p for i, p in enumerate(allc) if i not in fallen]
        cols = copies(persian_column("ap_col", CH, 0.8, color=shade(COL, -0.18), bull=shade(BULL, -0.25), detail=2), [(x, y, z0) for x, y in stand], "ap_cols")
        parts = [cols, B("ap_ash", -28, 40, -28, 40, z0, z0 + 0.3, ASH)]
        for k, i in enumerate(sorted(fallen)):
            x, y = allc[i]
            parts.append(turn(column_base(f"ap_fb{k}", 0.8, color=shade(COL, -0.18), detail=2), 0, x, y, z0))
            a = rnd.uniform(0, math.pi)
            for j in range(3):
                parts.append(drum(f"ap_fd{k}{j}", 0.8, 2.2, x + math.cos(a) * (3 + j * 2.6), y + math.sin(a) * (3 + j * 2.6), z0, a, shade(COL, -0.2)))
        for k, (x0, x1, y0, y1, h) in enumerate(((-29, 41, -29, -24, 6), (-29, -24, -24, 41, 8), (36, 41, -24, 41, 5), (-29, 41, 36, 41, 7))):
            parts.append(mound(f"ap_wm{k}", x0, x1, y0, y1, h, shade(MUD, -0.12), z0))
            parts.append(B(f"ap_wmc{k}", x0 + 1, x1 - 1, y0 + 1, y1 - 1, z0 + h - 0.6, z0 + h - 0.1, CHAR))
        for k, (x, y) in enumerate(((-38.5, -38.5), (50.5, -38.5), (-38.5, 50.5), (50.5, 50.5))):
            parts.append(frustum(f"ap_twr{k}", 19, 19, 13, 13, 11.0 + 2 * k, (x, y, z0), shade(MUD, -0.12)))
            parts.append(B(f"ap_twc{k}", x - 6, x + 6, y - 6, y + 6, z0 + 10.6 + 2 * k, z0 + 11.2 + 2 * k, CHAR))
        parts.append(mound("ap_store", -27, 39, 43, 58, 5.0, shade(MUD, -0.12), z0))
        for k in range(8):
            a = rnd.uniform(0, math.pi)
            parts.append(box(f"ap_beam{k}", 9.0, 0.7, 0.7, (rnd.uniform(-20, 32), rnd.uniform(-20, 32), z0 + 0.3), CHAR, rot_z=a))
        m.add(1, J(parts, "ruin"), "columns")
    else:  # ruin
        allc = porticoes + hall
        keep = [0, 1, 6, 8, 12, 14, 19, 23, 36 + 7, 36 + 14, 36 + 15, 36 + 21, 36 + 28]
        stand = [allc[i] for i in keep]
        parts = []
        for k, (x, y) in enumerate(stand):
            o = persian_column(f"ap_rc{k}", CH if k % 4 else CH - 3.0, 0.8, color=shade(COL, -0.08), detail=2, bulls=(k % 3 == 0))
            parts.append(turn(o, 0, x, y, z0))
        rest = [p for i, p in enumerate(allc) if i not in keep]
        parts.append(copies(column_base("ap_base", 0.8, color=shade(COL, -0.08), detail=1), [(x, y, z0) for x, y in rest], "ap_bases"))
        for k in range(14):
            x, y = rnd.choice(rest)
            a = rnd.uniform(0, math.pi)
            parts.append(drum(f"ap_rd{k}", 0.8, 2.2, x + 2.5 * math.cos(a), y + 2.5 * math.sin(a), z0, a, shade(COL, -0.1)))
        for k, (x0, x1, y0, y1, h) in enumerate(((-29, 41, -29, -24, 2.5), (-29, -24, -24, 41, 3.0), (36, 41, -24, 41, 2.0), (-29, 41, 36, 41, 3.0), (-27, 39, 43, 58, 3.0))):
            parts.append(mound(f"ap_rm{k}", x0, x1, y0, y1, h, EARTH, z0))
        for k, (x, y) in enumerate(((-38.5, -38.5), (50.5, -38.5), (-38.5, 50.5), (50.5, 50.5))):
            parts.append(mound(f"ap_rt{k}", x - 8, x + 8, y - 8, y + 8, 4.5, EARTH_D, z0))
        # the stairs lie buried under washed-down brick and earth (which is why their reliefs survive)
        parts.append(frustum("ap_bur1", 96, 14, 90, 6, 3.6, (c, -55.5, TERR_H), EARTH))
        parts.append(frustum("ap_bur2", 14, 96, 6, 90, 3.6, (-55.5, c, TERR_H), EARTH))
        m.add(1, J(parts, "ruin"), "columns")
    return m


# ================================================================ Gate of All Nations

def gate_all_nations(variant="460"):
    """Builder: the stair (west) door to -Y with bulls, the human-headed lamassu on the +Y door,
    the door toward the Apadana on +X (rotation 90 turns -Y to the west)."""
    m = Model("gate-all-nations")
    z0 = TERR_H
    m.add(0, J([slab("g_slab", 26, 30), B("g_floor", -12.5, 12.5, -12.5, 12.5, z0, z0 + 0.1, STONE_L)], "base"), "terrace")
    WH, T = 17.0, 3.0
    jambs = []
    for sx in (-1, 1):
        lo, hi = min(sx * 2.4, sx * 4.4), max(sx * 2.4, sx * 4.4)
        jambs.append(B(f"g_jf{sx}", lo, hi, -9.6, -7.5, z0, z0 + 12.0, STONE))
        jambs.append(B(f"g_jfu{sx}", lo, hi, -13.0, -9.6, z0 + 6.7, z0 + 12.0, STONE))
        jambs.append(B(f"g_jb{sx}", lo, hi, 7.5, 9.6, z0, z0 + 12.0, STONE))
        jambs.append(B(f"g_jbu{sx}", lo, hi, 9.6, 13.0, z0 + 6.7, z0 + 12.0, STONE))
        b = lamassu(f"g_bull{sx}", human=False, s=1.0)
        jambs.append(turn(b, 0, sx * 3.4, -11.8, z0 + 0.0))
        h = lamassu(f"g_lam{sx}", human=True, s=1.0)
        jambs.append(turn(h, 180, sx * 3.4, 11.8, z0))
        jambs.append(B(f"g_ins{sx}", sx * 3.4 - 0.85, sx * 3.4 + 0.85, -13.15, -13.0, z0 + 8.2, z0 + 11.2, STONE_L))
    for yy in ((-1, 1) if variant == "460" else ()):
        jambs.append(B(f"g_lt{yy}", -4.6, 4.6, min(yy * 13.0, yy * 7.5), max(yy * 13.0, yy * 7.5), z0 + 12.0, z0 + 13.0, STONE))
        jambs.append(frustum(f"g_cv{yy}", 9.2, 5.5, 10.4, 6.6, 1.0, (0, yy * 10.25, z0 + 13.0), STONE))
    if variant == "460":
        w = [B("g_wS1", -12.5, -4.2, -12.5, -12.5 + T, z0, z0 + WH, MUD), B("g_wS2", 4.2, 12.5, -12.5, -12.5 + T, z0, z0 + WH, MUD),
             B("g_wN1", -12.5, -4.2, 12.5 - T, 12.5, z0, z0 + WH, MUD), B("g_wN2", 4.2, 12.5, 12.5 - T, 12.5, z0, z0 + WH, MUD),
             B("g_wW", -12.5, -12.5 + T, -9.5, 9.5, z0, z0 + WH, MUD), B("g_wE1", 12.5 - T, 12.5, -9.5, -2.2, z0, z0 + WH, MUD),
             B("g_wE2", 12.5 - T, 12.5, 2.2, 9.5, z0, z0 + WH, MUD), B("g_wS3", -4.2, 4.2, -12.5, -9.5, z0 + 13.0, z0 + WH, MUD),
             B("g_wN3", -4.2, 4.2, 9.5, 12.5, z0 + 13.0, z0 + WH, MUD), B("g_wE3", 12.5 - T, 12.5, -2.2, 2.2, z0 + 11.0, z0 + WH, MUD)]
        w.append(frame_at("g_dE", 4.0, 9.0, 3.6, 11.0, 0, z0, "E"))
        for k, (f, x, y) in enumerate((("W", -12.5, -6.0), ("W", -12.5, 6.0), ("S", -8.4, -12.5), ("S", 8.4, -12.5), ("N", -8.4, 12.5), ("N", 8.4, 12.5), ("E", 12.5, -6.5), ("E", 12.5, 6.5))):
            w.append(frame_at(f"g_n{k}", 1.6, 3.4, 0.8, x, y, z0 + 8.0, f))
        w.append(copies(persian_column("g_col", 16.5, 0.65, detail=1), [(x, y, z0) for x in (-4.6, 4.6) for y in (-4.6, 4.6)], "g_cols"))
        m.add(1, J(jambs + w, "gate"), "gate")
        r = [B("g_roof", -12.8, 12.8, -12.8, 12.8, z0 + WH, z0 + WH + 1.2, ROOF), B("g_glz", -12.85, 12.85, -12.85, 12.85, z0 + WH - 1.6, z0 + WH - 0.8, GLAZE),
             merlon_rect("g_rm", -12.8, 12.8, -12.8, 12.8, z0 + WH + 1.2, size=1.5)]
        m.add(2, J(r, "roof"), "roof")
    else:
        w = [mound("g_mS", -12.5, -4.4, -12.5, -9.5, 2.4, EARTH, z0), mound("g_mS2", 4.4, 12.5, -12.5, -9.5, 1.8, EARTH, z0),
             mound("g_mN", -12.5, -4.4, 9.5, 12.5, 2.0, EARTH, z0), mound("g_mN2", 4.4, 12.5, 9.5, 12.5, 2.6, EARTH, z0),
             mound("g_mW", -12.5, -9.5, -9.5, 9.5, 2.2, EARTH, z0), mound("g_mE", 9.5, 12.5, -9.5, 9.5, 1.6, EARTH, z0)]
        w.append(turn(persian_column("g_c1", 16.5, 0.65, detail=2, bulls=False), 0, -4.6, -4.6, z0))
        w.append(turn(persian_column("g_c2", 16.5, 0.65, detail=2, bulls=False), 0, -4.6, 4.6, z0))
        w.append(turn(column_base("g_b3", 0.65), 0, 4.6, -4.6, z0))
        w.append(turn(column_base("g_b4", 0.65), 0, 4.6, 4.6, z0))
        w.append(drum("g_d1", 0.65, 2.0, 6.5, -2.0, z0, 0.6))
        w.append(drum("g_d2", 0.65, 2.0, 3.0, 1.5, z0, 1.9))
        w.append(box("g_cap", 3.5, 1.3, 1.3, (7.0, 6.5, z0), BULL, rot_z=0.4))
        m.add(1, J(jambs + w, "gate"), "gate")
    return m


# ================================================================ Hall of a Hundred Columns

def hundred_columns(variant="460"):
    """Builder: the north porch to -Y (rotation 180)."""
    m = Model("hundred-columns")
    z0 = TERR_H
    m.add(0, J([slab("h_slab", 72, 92), B("h_floor", -36, 36, -46, 46, z0, z0 + 0.1, STONE_L),
                B("h_step", -30, 30, -46.0, -44.2, z0, z0 + 0.5, STONE)], "base"), "terrace")
    CH = 14.0
    hall_pts = col_grid([-29.25 + 6.5 * i for i in range(10)], [-19.25 + 6.5 * j for j in range(10)])
    porch = col_grid([-26.25 + 7.5 * i for i in range(8)], [-40.5, -32.0])
    doors = [("S", -13.0, -26.0), ("S", 13.0, -26.0), ("N", -13.0, 46.0), ("N", 13.0, 46.0),
             ("W", -36.0, 0.0), ("W", -36.0, 26.0), ("E", 36.0, 0.0), ("E", 36.0, 26.0)]
    wins = [("S", -26.0, -26.0), ("S", 0.0, -26.0), ("S", 26.0, -26.0), ("N", -26.0, 46.0), ("N", 0.0, 46.0), ("N", 26.0, 46.0),
            ("W", -36.0, -13.0), ("W", -36.0, 13.0), ("W", -36.0, 38.0), ("E", 36.0, -13.0), ("E", 36.0, 13.0), ("E", 36.0, 38.0)]
    if variant == "460":
        # about 460 BCE: Artaxerxes I's builders are roofing the hall; the north half is covered, over the south
        # half the cedar beams are still being laid on the forest of columns
        parts = [copies(persian_column("h_pc", CH, 0.65, detail=2), [(x, y, z0) for x, y in porch], "h_porch"),
                 copies(persian_column("h_hc", CH, 0.65, detail=1), [(x, y, z0) for x, y in hall_pts], "h_hall"),
                 B("h_wS", -36, 36, -26, -22.5, z0, z0 + CH + 0.4, MUD), B("h_wN", -36, 36, 42.5, 46, z0, z0 + CH + 0.4, MUD),
                 B("h_wW", -36, -32.5, -22.5, 42.5, z0, z0 + CH + 0.4, MUD), B("h_wE", 32.5, 36, -22.5, 42.5, z0, z0 + CH + 0.4, MUD)]
        for sx in (-1, 1):
            parts.append(B(f"h_anta{sx}", min(sx * 31.5, sx * 36), max(sx * 31.5, sx * 36), -44.0, -26, z0, z0 + CH + 0.4, MUD))
            lam = lamassu(f"h_bull{sx}", human=False, s=1.35)
            parts.append(turn(lam, 0, sx * 33.75, -42.0, z0))
        for k, (f, x, y) in enumerate(doors):
            parts.append(frame_at(f"h_d{k}", 3.4, 8.0, 4.2, x + {"W": 1.75, "E": -1.75}.get(f, 0), y + {"S": 1.75, "N": -1.75}.get(f, 0), z0, f))
        for k, (f, x, y) in enumerate(wins):
            parts.append(frame_at(f"h_w{k}", 2.0, 3.6, 3.9, x + {"W": 1.75, "E": -1.75}.get(f, 0), y + {"S": 1.75, "N": -1.75}.get(f, 0), z0 + 2.5, f))
        m.add(1, J(parts, "hall"), "columns")
        zr = z0 + CH
        r = [B("h_roof", -36.4, 36.4, 10.0, 46.4, zr, zr + 1.4, ROOF), B("h_proof", -36.4, 36.4, -46.4, -22.5, zr, zr + 1.4, ROOF),
             B("h_beam", -36, 36, -46.6, -45.6, zr - 1.1, zr, CEDAR),
             B("h_glz", -36.5, 36.5, 10.0, 46.5, zr + 0.5, zr + 1.0, BLUE), B("h_glzp", -36.5, 36.5, -46.5, -22.5, zr + 0.5, zr + 1.0, BLUE),
             B("h_edge", -32.5, 32.5, 9.4, 10.0, zr - 0.6, zr + 1.4, CEDAR),
             merlon_rect("h_rm", -36.4, 36.4, 10.0, 46.4, zr + 1.4, size=1.5, sides="NWE"),
             merlon_rect("h_rmp", -36.4, 36.4, -46.4, -22.5, zr + 1.4, size=1.5, sides="SWE")]
        for j in range(5):
            y = -19.25 + 6.5 * j
            r.append(B(f"h_bm{j}", -32.5, 32.5, y - 0.45, y + 0.45, zr - 0.2, zr + 0.7, CEDAR))
        for i in range(0, 10, 2):
            x = -29.25 + 6.5 * i
            r.append(B(f"h_jst{i}", x - 0.3, x + 0.3, -1.0 - 6.5 * (i % 4 == 0), 10.0, zr + 0.7, zr + 1.2, CEDAR))
        r.append(crane("h_cr", -3.0, -6.0, zr + 0.7, 7.0, 0))
        r.append(box("h_beamload", 7.0, 0.7, 0.7, (-3.0, -6.0, zr + 3.5), CEDAR))
        m.add(2, J(r, "roof"), "roof")
    else:
        parts = [copies(column_base("h_base", 0.65, color=shade(COL, -0.1)), [(x, y, z0) for x, y in hall_pts + porch], "h_bases"),
                 B("h_ash", -32, 32, -22, 42, z0, z0 + 0.25, ASH)]
        for k, (f, x, y) in enumerate(doors):
            parts.append(frame_at(f"h_d{k}", 3.4, 8.0, 2.2, x, y, z0, f, panel=False, color=shade(DSTONE, 0.15)))
        for k, (f, x, y) in enumerate(wins[::2]):
            parts.append(frame_at(f"h_w{k}", 2.0, 3.6, 1.8, x, y, z0 + 2.5, f, panel=False, color=shade(DSTONE, 0.15)))
        rnd = random.Random(3)
        for k, (x, y) in enumerate(rnd.sample(hall_pts, 6)):
            parts.append(turn(star_shaft(f"h_st{k}", 0.65, 0.63, rnd.uniform(1.5, 4.5), 10, shade(COL, -0.1), 1.1), 0, x, y, z0))
        for k in range(16):
            x, y = rnd.choice(hall_pts)
            a = rnd.uniform(0, math.pi)
            parts.append(drum(f"h_dr{k}x", 0.65, 1.8, x + 2.6 * math.cos(a), y + 2.6 * math.sin(a), z0, a, shade(COL, -0.12)))
        for k, (x0, x1, y0, y1) in enumerate(((-36, 36, -26, -23), (-36, 36, 43, 46), (-36, -33, -23, 43), (33, 36, -23, 43))):
            parts.append(mound(f"h_m{k}", x0, x1, y0, y1, 2.2, EARTH, z0))
        parts.append(turn(J([box("h_bf", 1.8, 2.5, 2.4, (0, 0, 0.5), STONE), box("h_bh", 1.2, 1.4, 1.4, (0, -1.6, 2.6), STONE),
                             box("h_bp", 2.2, 3.4, 0.5, (0, 0, 0), STONE)], "h_bullfrag"), 0, -33.75, -42.0, z0))
        m.add(1, J(parts, "ruin"), "columns")
    return m


# ================================================================ palaces (Tachara, Hadish, Tripylon)

def palace_stair(name, half, rise, depth, yfront, paint=True, n=10):
    """Two flights facing each other on the front (-Y) of a raised palace, with relief on their faces."""
    p = []
    for sx in (-1, 1):
        p.append(flight(f"{name}f{sx}", sx * half, sx * 2.0, 0.0, rise, yfront, yfront + depth, n, STONE, parapet_y=yfront + 0.3, extra=1.0))
        p.append(stair_reliefs(f"{name}r{sx}", sx * half, sx * 2.0, 0.0, rise, yfront, reg=0.65, paint=paint))
    p.append(B(f"{name}c", -2.0, 2.0, yfront, yfront + depth, 0, rise, STONE))
    p.append(relief_band(f"{name}cr", -1.7, 1.7, yfront, 0.3, max(0.8, rise - 0.6), every=1.0, paint=paint))
    return J(p, name)


def palace(name, W, D, plat, front, port, hall, col_h, wall_h, stair_half, variant="intact", windows_side=3, front_wins=2,
           hall_cols=None, port_cols=None, col_r=0.55, ash=False):
    """A Persepolitan palace on the terrace: a raised platform with a relief stair on the front (-Y), a columned
    portico and a hall of mud brick framed by dark stone doors and windows; or its ruin, where only the stone
    frames and the column bases stand. port / hall = (x0, x1, y0, y1)."""
    m = Model(name)
    z0 = TERR_H
    zp = z0 + plat
    base = [slab(name + "_slab", W, D), B(name + "_plat", -W / 2, W / 2, front, D / 2, z0, zp, STONE),
            B(name + "_pc", -W / 2 - 0.1, W / 2 + 0.1, front - 0.1, D / 2 + 0.1, zp - 0.4, zp - 0.2, STONE_D),
            B(name + "_fl", -W / 2 + 0.5, W / 2 - 0.5, front + 0.5, D / 2 - 0.5, zp, zp + 0.06, STONE_L)]
    base.append(turn(palace_stair(name + "_st", stair_half, plat, front + D / 2, 0.0, paint=variant == "intact"), 0, 0, -D / 2, z0))
    m.add(0, J(base, "platform"), "platform")
    hx0, hx1, hy0, hy1 = hall
    px0, px1, py0, py1 = port
    # frames: front door + windows, side windows, back windows
    fr = [("S", 0.0, hy0, "door")]
    for k in range(front_wins):
        off = (hx1 - hx0) / 2 * (k + 1) / (front_wins + 1)
        fr += [("S", -off, hy0, "win"), ("S", off, hy0, "win")]
    for k in range(windows_side):
        y = hy0 + (hy1 - hy0) * (k + 0.5) / windows_side
        fr += [("W", hx0, y, "win"), ("E", hx1, y, "win")]
    fr += [("N", (hx1 - hx0) * -0.22, hy1, "win"), ("N", (hx1 - hx0) * 0.22, hy1, "win")]
    if variant == "intact":
        p = [B(name + "_hall", hx0, hx1, hy0, hy1, zp, zp + wall_h, MUD)]
        if port_cols:
            p.append(copies(persian_column(name + "_col", col_h, col_r, detail=2), [(x, y, zp) for x, y in port_cols], name + "_cols"))
        for k, (f, x, y, kind) in enumerate(fr):
            if kind == "door":
                p.append(frame_at(f"{name}_d{k}", 2.4, 6.0, 1.6, x, y, zp, f))
            else:
                p.append(frame_at(f"{name}_w{k}", 1.5, 3.0, 1.5, x, y, zp + 1.4, f))
        m.add(1, J(p, "hall"), "walls")
        r = [B(name + "_roof", hx0 - 0.3, hx1 + 0.3, hy0, hy1 + 0.3, zp + wall_h, zp + wall_h + 1.0, ROOF),
             merlon_rect(name + "_rm", hx0 - 0.3, hx1 + 0.3, hy0, hy1 + 0.3, zp + wall_h + 1.0, size=1.3, sides="NWE" if port_cols else "SNWE"),
             B(name + "_glz", hx0 - 0.35, hx1 + 0.35, hy0 - 0.05, hy1 + 0.35, zp + wall_h - 1.2, zp + wall_h - 0.5, GLAZE)]
        if port_cols:
            zr = zp + col_h
            r += [B(name + "_proof", px0, px1, py0, hy0, zr, zr + 1.0, ROOF), B(name + "_pbeam", px0, px1, py0 - 0.1, py0 + 0.8, zr - 0.9, zr, CEDAR),
                  merlon_run(name + "_prm", (px0, py0 + 0.3), (px1, py0 + 0.3), zr + 1.0, size=1.3)]
            if zr + 1.0 < zp + wall_h:
                r.append(B(name + "_pwall", hx0, hx1, hy0, hy0 + 1.0, zr + 1.0, zp + wall_h + 1.0, MUD))
                r.append(merlon_run(name + "_prm2", (hx0, hy0 + 0.3), (hx1, hy0 + 0.3), zp + wall_h + 1.0, size=1.3))
        m.add(2, J(r, "roof"), "roof")
    else:
        p = []
        if ash:
            p.append(B(name + "_ash", hx0 + 1, hx1 - 1, hy0 + 1, hy1 - 1, zp, zp + 0.3, ASH))
        pts = (hall_cols or []) + (port_cols or [])
        if pts:
            p.append(copies(column_base(name + "_base", col_r, color=shade(COL, -0.08)), [(x, y, zp) for x, y in pts], name + "_bases"))
        for k, (f, x, y, kind) in enumerate(fr):
            if kind == "door":
                p.append(frame_at(f"{name}_d{k}", 2.4, 6.0, 1.6, x, y, zp, f, panel=False))
            else:
                p.append(frame_at(f"{name}_w{k}", 1.5, 3.0, 1.5, x, y, zp + 1.4, f, panel=False))
                p.append(B(f"{name}_ws{k}", -0.8, 0.8, -0.75, 0.75, zp, zp + 1.4, DSTONE))
                p[-1] = turn(p[-1], 0, x, y, 0)
        segs = [(hx0, hx1, hy0, hy0 + 1.5), (hx0, hx1, hy1 - 1.5, hy1), (hx0, hx0 + 1.5, hy0, hy1), (hx1 - 1.5, hx1, hy0, hy1)]
        for k, (a, b, c, d) in enumerate(segs):
            p.append(mound(f"{name}_m{k}", a, b, c, d, 1.2, EARTH, zp))
        rnd = random.Random(len(name))
        for k in range(5):
            if pts:
                x, y = rnd.choice(pts)
                a = rnd.uniform(0, math.pi)
                p.append(drum(f"{name}_dr{k}", col_r, 1.6, x + 1.8 * math.cos(a), y + 1.8 * math.sin(a), zp, a, shade(COL, -0.1)))
        m.add(1, J(p, "ruin"), "walls")
    return m


def tachara(variant="intact"):
    hall_cols = col_grid([-7.5, 0.0, 7.5], [0.0, 6.0, 12.0, 18.0])
    port = col_grid([-9.0, -3.0, 3.0, 9.0], [-13.0, -8.5])
    return palace("tachara", 32, 44, 2.6, -16.0, (-13, 13, -15.5, -6.0), (-15, 15, -6.0, 21.5), 9.5, 11.0, 13.0, variant,
                  windows_side=3, front_wins=2, hall_cols=hall_cols, port_cols=port, col_r=0.5)


def hadish(variant="intact"):
    hall_cols = col_grid([-15 + 6 * i for i in range(6)], [-5 + 6 * j for j in range(6)])
    port = col_grid([-15 + 6 * i for i in range(6)], [-18.0, -12.5])
    return palace("hadish", 42, 58, 4.0, -22.0, (-19, 19, -21.0, -9.0), (-20, 20, -9.0, 28.0), 11.0, 13.0, 18.0, variant,
                  windows_side=4, front_wins=2, hall_cols=hall_cols, port_cols=port, col_r=0.55, ash=True)


def tripylon(variant="intact"):
    hall_cols = col_grid([-4.5, 4.5], [0.5, 8.5])
    m = palace("tripylon", 26, 26, 2.0, -7.0, (-9, 9, -6.5, -6.0), (-10, 10, -6.0, 12.5), 0.0, 12.0, 11.0, variant,
               windows_side=1, front_wins=0, hall_cols=hall_cols, port_cols=None, col_r=0.5)
    z = TERR_H + 2.0
    side = [frame_at("tri_dW", 2.2, 6.0, 1.6, -10.0, 3.0, z, "W", panel=variant == "intact"), frame_at("tri_dE", 2.2, 6.0, 1.6, 10.0, 3.0, z, "E", panel=variant == "intact")]
    m.add(1, J(side, "side_doors"))
    return m


# ================================================================ harem, treasury, garrison

def harem(variant="intact"):
    """Builder: the main hall with its porch to -Y (rotation 180); suites along +X and +Y."""
    m = Model("harem")
    z0 = TERR_H
    m.add(0, J([slab("hr_slab", 56, 90), B("hr_floor", -28, 28, -45, 45, z0, z0 + 0.08, STONE_L)], "base"), "terrace")
    port = col_grid([-21.0, -14.5, -8.0, -1.5], [-42.0, -38.5])
    hall_cols = col_grid([-20, -13, -6, 1], [-31, -24, -17])
    units = []
    for j in range(9):
        y0 = -44 + j * 9.8
        units.append((13.0, 27.0, y0, y0 + 9.0, 6.0 + (j % 2) * 0.8, "W"))
    for i, (x0, x1) in enumerate(((-26, -13), (-10, 4))):
        for j in range(4):
            y0 = -4 + j * 12.0
            units.append((x0, x1, y0, y0 + 11.0, 6.4 - (j % 2) * 0.6, "S"))
    if variant == "intact":
        p = [copies(persian_column("hr_col", 9.0, 0.45, detail=2), [(x, y, z0) for x, y in port], "hr_cols"),
             B("hr_hall", -26, 4, -36, -8, z0, z0 + 11.0, MUD)]
        p.append(frame_at("hr_d", 2.2, 5.5, 1.5, -11.0, -36.0, z0, "S"))
        for k, x in enumerate((-21.0, -1.0)):
            p.append(frame_at(f"hr_w{k}", 1.4, 2.8, 1.4, x, -36.0, z0 + 1.4, "S"))
        for k, (x0, x1, y0, y1, h, f) in enumerate(units):
            p.append(B(f"hr_u{k}", x0, x1, y0, y1, z0, z0 + h, MUD if k % 2 else shade(MUD, -0.05)))
            if f == "W":
                p.append(B(f"hr_c{k}", 7.0, x0, y0 + 1.0, y1 - 1.0, z0, z0 + 0.12, SAND))
                p.append(frame_at(f"hr_ud{k}", 1.3, 3.2, 1.0, x0, (y0 + y1) / 2, z0, "W"))
            else:
                p.append(frame_at(f"hr_ud{k}", 1.3, 3.2, 1.0, (x0 + x1) / 2, y0, z0, "S"))
        p.append(B("hr_wall", 27.0, 28.0, -45, 45, z0, z0 + 7.5, MUD_D))
        m.add(1, J(p, "rooms"), "walls")
        r = [B("hr_roof", -26.3, 4.3, -36, -7.7, z0 + 11.0, z0 + 11.8, ROOF), B("hr_proof", -24.0, 1.0, -44.0, -36.0, z0 + 9.0, z0 + 9.8, ROOF),
             B("hr_pbeam", -24.0, 1.0, -44.1, -43.3, z0 + 8.2, z0 + 9.0, CEDAR), merlon_rect("hr_rm", -26.3, 4.3, -36, -7.7, z0 + 11.8, size=1.2),
             merlon_run("hr_prm", (-24.0, -43.7), (1.0, -43.7), z0 + 9.8, size=1.2)]
        for k, (x0, x1, y0, y1, h, f) in enumerate(units):
            r.append(B(f"hr_ur{k}", x0 - 0.1, x1 + 0.1, y0 - 0.1, y1 + 0.1, z0 + h, z0 + h + 0.4, ROOF))
        m.add(2, J(r, "roof"), "roof")
    else:
        p = [copies(column_base("hr_base", 0.45, color=shade(COL, -0.08)), [(x, y, z0) for x, y in port + hall_cols], "hr_bases"),
             frame_at("hr_d", 2.2, 5.5, 1.5, -11.0, -36.0, z0, "S", panel=False)]
        for k, x in enumerate((-21.0, -1.0)):
            p.append(frame_at(f"hr_w{k}", 1.4, 2.8, 1.4, x, -36.0, z0 + 1.4, "S", panel=False))
        for k, (a, b, c, d) in enumerate(((-26, 4, -36, -34.5), (-26, -24.5, -36, -8), (2.5, 4, -36, -8), (-26, 4, -9.5, -8))):
            p.append(mound(f"hr_hm{k}", a, b, c, d, 1.4, EARTH, z0))
        for k, (x0, x1, y0, y1, h, f) in enumerate(units):
            p.append(mound(f"hr_um{k}", x0 + 0.5, x1 - 0.5, y0 + 0.5, y1 - 0.5, 1.6 + (k % 3) * 0.4, EARTH if k % 2 else EARTH_D, z0))
        m.add(1, J(p, "ruin"), "walls")
    return m


def treasury(variant="intact"):
    m = Model("treasury")
    z0 = TERR_H
    m.add(0, J([slab("tr_slab", 76, 130), B("tr_floor", -38, 38, -65, 65, z0, z0 + 0.08, STONE_L)], "base"), "terrace")
    WH = 8.0
    courts = [(-30.0, 0.0, 32.0, 56.0), (6.0, 32.0, -56.0, -32.0), (-30.0, -6.0, -20.0, 0.0)]
    halls = [(-34.0, 34.0, 4.0, 28.0, 8, 4), (-34.0, 2.0, -62.0, -24.0, 6, 6), (4.0, 34.0, 32.0, 62.0, 5, 5)]
    rnd = random.Random(11)
    if variant == "intact":
        p = [B("tr_outerS", -38, 38, -65, -62, z0, z0 + WH, MUD), B("tr_outerN", -38, 38, 62, 65, z0, z0 + WH, MUD),
             B("tr_outerW", -38, -35, -62, 62, z0, z0 + WH, MUD), B("tr_outerE", 35, 38, -62, 62, z0, z0 + WH, MUD)]
        p.append(frame_at("tr_door", 2.6, 5.0, 3.4, -36.5, -10.0, z0, "W"))
        p.append(frame_at("tr_door2", 2.6, 5.0, 3.4, 0.0, 63.5, z0, "N"))
        roof = []
        # roofed blocks everywhere except the courts: a coarse grid of 8 m cells
        for i in range(9):
            for j in range(16):
                x0, y0 = -35 + i * 7.8, -62 + j * 7.75
                cxx, cyy = x0 + 3.9, y0 + 3.875
                if any(a <= cxx <= b and c <= cyy <= d for a, b, c, d in courts):
                    continue
                roof.append(B(f"tr_r{i}_{j}", x0, x0 + 7.8, y0, y0 + 7.75, z0 + WH - 0.8, z0 + WH, ROOF if (i + j) % 3 else shade(ROOF, -0.05)))
        for k, (a, b, c, d) in enumerate(courts):
            p.append(B(f"tr_cf{k}", a, b, c, d, z0, z0 + 0.12, SAND))
            cols = [(a + 2.0, y) for y in [c + 2.5 + 3.5 * t for t in range(int((d - c - 3) / 3.5))]] + [(x, d - 2.0) for x in [a + 5.0 + 3.5 * t for t in range(int((b - a - 6) / 3.5))]]
            p.append(copies(cylinder(f"tr_wc{k}", 0.3, WH - 0.8, (0, 0, 0), WOODCOL, verts=8), [(x, y, z0) for x, y in cols], f"tr_wcs{k}"))
            roof.append(B(f"tr_cw{k}", a, a + 4.0, c, d - 4.0, z0 + WH - 0.8, z0 + WH, ROOF))
            roof.append(B(f"tr_cn{k}", a, b, d - 4.0, d, z0 + WH - 0.8, z0 + WH, ROOF))
            for f, x, y in (("E", b, (c + d) / 2), ("S", (a + b) / 2, c)):
                p.append(frame_at(f"tr_cd{k}{f}", 1.8, 4.0, 1.2, x, y, z0, f, color=MUD_D, cornice=False))
        for k, (a, b, c, d) in enumerate(((-38.2, 38.2, -65.2, -63.8), (-38.2, 38.2, 63.8, 65.2), (-38.2, -36.8, -63.8, 63.8), (36.8, 38.2, -63.8, 63.8))):
            p.append(B(f"tr_par{k}", a, b, c, d, z0 + WH, z0 + WH + 0.9, MUD_D))
        m.add(1, J(p, "walls"), "walls")
        m.add(2, J(roof, "roofs"), "roof")
    else:
        p = []
        for k, (a, b, c, d) in enumerate(((-38, 38, -65, -62), (-38, 38, 62, 65), (-38, -35, -62, 62), (35, 38, -62, 62))):
            p.append(mound(f"tr_om{k}", a, b, c, d, 2.4, EARTH_D, z0))
        bases = []
        for k, (a, b, c, d, nx, ny) in enumerate(halls):
            bases += col_grid([a + (b - a) * (i + 0.5) / nx for i in range(nx)], [c + (d - c) * (j + 0.5) / ny for j in range(ny)])
            for q, (u0, u1, v0, v1) in enumerate(((a, b, c - 1.0, c), (a, b, d, d + 1.0), (a - 1.0, a, c, d))):
                p.append(mound(f"tr_hm{k}{q}", u0, u1, v0, v1, 1.3, EARTH, z0))
            p.append(B(f"tr_ash{k}", a + 0.5, b - 0.5, c + 0.5, d - 0.5, z0, z0 + 0.15, ASH))
        p.append(copies(cylinder("tr_base", 0.75, 0.5, (0, 0, 0), STONE, verts=8), [(x, y, z0) for x, y in bases], "tr_bases"))
        for k in range(14):
            x, y = rnd.uniform(-34, 34), rnd.uniform(-60, 60)
            p.append(mound(f"tr_heap{k}", x - 2, x + 2, y - 2, y + 2, 1.0, EARTH, z0))
        m.add(1, J(p, "ruin"), "walls")
    return m


def garrison(variant="intact"):
    m = Model("garrison")
    z0 = TERR_H
    m.add(0, J([slab("ga_slab", 40, 120), B("ga_floor", -20, 20, -60, 60, z0, z0 + 0.08, STONE_L)], "base"), "terrace")
    ranges = [(-19.0, -10.0), (-6.0, 4.0)]
    towers = [-52.0, -26.0, 0.0, 26.0, 52.0]
    if variant == "intact":
        p = []
        for i, (x0, x1) in enumerate(ranges):
            for j in range(10):
                y0 = -58 + j * 11.8
                p.append(B(f"ga_r{i}{j}", x0, x1, y0, y0 + 11.2, z0, z0 + 6.0 + (j % 2) * 0.5, MUD if (i + j) % 2 else shade(MUD, -0.05)))
                p.append(B(f"ga_d{i}{j}", x1, x1 + 0.1, y0 + 4.8, y0 + 6.4, z0, z0 + 2.6, DARK))
        p.append(B("ga_court", -10, -6, -58, 58, z0, z0 + 0.12, SAND))
        p.append(B("ga_court2", 4, 13, -58, 58, z0, z0 + 0.12, SAND))
        p.append(B("ga_wall", 13.0, 17.0, -60, 60, z0, z0 + 9.0, MUD_D))
        p.append(merlon_run("ga_wm", (16.6, -60), (16.6, 60), z0 + 9.0, size=1.4, color=MUD_D))
        for k, y in enumerate(towers):
            p.append(B(f"ga_t{k}", 12.5, 20.0, y - 3.75, y + 3.75, z0, z0 + 12.5, shade(MUD_D, -0.05)))
            p.append(merlon_rect(f"ga_tm{k}", 12.5, 20.0, y - 3.75, y + 3.75, z0 + 12.5, size=1.2, color=shade(MUD_D, -0.05)))
        m.add(1, J(p, "barracks"), "walls")
        r = []
        for i, (x0, x1) in enumerate(ranges):
            r.append(B(f"ga_roof{i}", x0 - 0.2, x1 + 0.2, -58.2, 58.2, z0 + 6.5, z0 + 6.9, ROOF))
            r.append(merlon_run(f"ga_rm{i}", (x1, -58), (x1, 58), z0 + 6.9, size=1.0, color=MUD))
        m.add(2, J(r, "roofs"), "roof")
    else:
        p = []
        for i, (x0, x1) in enumerate(ranges):
            for j in range(5):
                y0 = -58 + j * 23.6
                p.append(mound(f"ga_m{i}{j}", x0 + 0.5, x1 - 0.5, y0 + 1, y0 + 22, 2.0 + (j % 2) * 0.6, EARTH if j % 2 else EARTH_D, z0))
        p.append(mound("ga_wm", 13.5, 16.5, -59, 59, 3.0, EARTH_D, z0))
        for k, y in enumerate(towers):
            p.append(mound(f"ga_tm{k}", 13.5, 19.0, y - 3, y + 3, 4.0, EARTH_D, z0))
        m.add(1, J(p, "ruin"), "walls")
    return m


# ================================================================ the unfinished gate

def unfinished_gate():
    m = Model("unfinished-gate")
    z0 = TERR_H
    m.add(0, J([slab("u_slab", 30, 30), B("u_floor", -15, 15, -15, 15, z0, z0 + 0.08, STONE_L)], "base"), "terrace")
    p = []
    for k, (a, b, c, d) in enumerate(((-12, -4, -12, -10), (4, 12, -12, -10), (-12, -4, 10, 12), (4, 12, 10, 12), (-12, -10, -10, 10), (10, 12, -10, 10))):
        p.append(B(f"u_ft{k}", a, b, c, d, z0, z0 + 1.0 + 0.4 * (k % 2), MUD))
    for k, (x, y) in enumerate(((-4.6, -4.6), (4.6, -4.6), (-4.6, 4.6), (4.6, 4.6))):
        p.append(turn(column_base(f"u_b{k}", 0.65, detail=2), 0, x, y, z0))
        hh = (0, 2.4, 5.2, 0)[k]
        if hh:
            p.append(turn(cylinder(f"u_s{k}", 0.68, hh, (0, 0, 1.4), STONE_L, verts=12), 0, x, y, z0))
    for sx in (-1, 1):
        p.append(B(f"u_j{sx}", min(sx * 2.4, sx * 4.4), max(sx * 2.4, sx * 4.4), -13.5, -9.0, z0, z0 + 5.0, STONE_L))
        p.append(B(f"u_jb{sx}", min(sx * 2.4, sx * 4.4), max(sx * 2.4, sx * 4.4), 9.0, 12.5, z0, z0 + 3.0, STONE_L))
        # roughed-out bull blocks: the masons had blocked out the body and head
        p.append(box(f"u_bull{sx}", 2.2, 5.0, 3.8, (sx * 3.4, -11.0, z0), STONE_L))
        p.append(box(f"u_bullh{sx}", 1.4, 1.8, 1.6, (sx * 3.4, -13.2, z0 + 3.8), STONE_L))
    for k, (x, y, a) in enumerate(((8.0, -5.0, 0.3), (9.5, 2.0, 1.4), (-8.5, 4.0, 0.9), (-2.0, 7.0, 0.1), (6.0, 7.5, 2.0))):
        p.append(drum(f"u_dr{k}", 0.68, 1.8, x, y, z0, a, STONE_L))
    for k, (x, y) in enumerate(((-9.0, -6.0), (0.0, -6.5), (11.0, -13.0))):
        p.append(box(f"u_blk{k}", 2.6, 1.6, 1.3, (x, y, z0), STONE_L, rot_z=0.4 * k))
    p.append(crane("u_cr", 0.0, 0.0, z0, 12.0, 0))
    m.add(1, J(p, "works"), "walls")
    return m


# ================================================================ royal tomb

def royal_tomb():
    """A cliff of Kuh-e Rahmat with the cross-shaped tomb façade cut into it, facing -Y (rotation 90 = west)."""
    m = Model("royal-tomb")
    rock = [B("rt_cliff", -22, 22, -6.0, 15.0, 0, 30.0, ROCK),
            frustum("rt_back", 44, 21, 26, 8, 12.0, (0, 4.5, 30.0), shade(ROCK, -0.04)),
            B("rt_cut", -12.5, 12.5, -7.0, -6.0, 0.8, 31.5, ROCK_L),
            frustum("rt_cheekW", 10, 12, 5, 7, 33.0, (-17.5, -6.0, 0), ROCK),
            frustum("rt_cheekE", 10, 12, 5, 7, 33.0, (17.5, -6.0, 0), ROCK),
            frustum("rt_lintel", 25, 6, 22, 4, 4.0, (0, -7.0, 31.5), ROCK),
            frustum("rt_talus", 44, 9, 38, 4, 2.0, (0, -10.5, 0), shade(ROCK, 0.08))]
    rr = random.Random(9)
    for k in range(12):
        x, y, sz = rr.uniform(-21, 21), rr.uniform(-14, 12), rr.uniform(2.0, 5.0)
        if y < -6:
            continue
        rock.append(frustum(f"rt_boulder{k}", sz * 1.6, sz * 1.4, sz * 0.6, sz * 0.5, sz, (x, y, 30.0 + rr.uniform(0, 3)), shade(ROCK, rr.uniform(-0.08, 0.06))))
    m.add(0, J(rock, "rock"), "rock")
    yf = -7.0
    CR = shade(ROCK_L, -0.16)
    p = [B("rt_low", -5.5, 5.5, yf - 0.2, yf, 2.0, 9.5, CR),
         B("rt_mid", -10.0, 10.0, yf - 0.2, yf, 9.5, 18.0, CR),
         B("rt_up", -5.5, 5.5, yf - 0.2, yf, 18.0, 28.5, CR)]
    for k, x in enumerate((-7.4, -2.8, 2.8, 7.4)):
        p.append(cylinder(f"rt_c{k}", 0.45, 5.6, (x, yf - 0.35, 9.6), ROCK_L, verts=12))
        p.append(B(f"rt_cb{k}", x - 0.6, x + 0.6, yf - 0.8, yf - 0.2, 9.5, 9.8, ROCK_L))
        p.append(turn(bull_pair(f"rt_b{k}", 0.38, 0.0, ROCK_L, simple=True), 0, x, yf - 0.45, 15.2))
    for k, z in enumerate((16.0, 16.45, 16.9)):
        p.append(B(f"rt_ar{k}", -9.6 + k * 0.1, 9.6 - k * 0.1, yf - 0.75 - 0.1 * k, yf - 0.2, z, z + 0.42, ROCK_L))
    for i in range(26):
        x = -9.3 + i * 0.73
        p.append(B(f"rt_dt{i}", x, x + 0.4, yf - 0.95, yf - 0.2, 17.35, 17.75, ROCK_L))
    p.append(frame_at("rt_door", 1.8, 3.6, 0.7, 0, yf - 0.3, 9.6, "S", color=ROCK_L))
    # upper register: two tiers of throne-bearers lift the dais; the king before the fire altar, Ahuramazda above
    for t, z in enumerate((18.6, 20.1)):
        p.append(B(f"rt_tier{t}", -4.8, 4.8, yf - 0.5, yf - 0.2, z + 1.15, z + 1.45, ROCK_L))
        for i in range(12):
            x = -4.3 + i * 0.78
            p.append(B(f"rt_tb{t}{i}", x - 0.17, x + 0.17, yf - 0.5, yf - 0.2, z, z + 1.15, ROCK_L))
    p.append(B("rt_dais", -5.0, 5.0, yf - 0.6, yf - 0.2, 21.6, 22.1, ROCK_L))
    for k in range(3):
        p.append(B(f"rt_ped{k}", -3.8 + k * 0.3, -1.8 - k * 0.3, yf - 0.6, yf - 0.2, 22.1 + k * 0.3, 22.4 + k * 0.3, ROCK_L))
    p.append(B("rt_king", -3.1, -2.4, yf - 0.7, yf - 0.2, 23.0, 25.4, ROCK_L))
    p.append(B("rt_bow", -2.4, -2.2, yf - 0.7, yf - 0.2, 23.6, 25.0, ROCK_L))
    p.append(B("rt_altar", 1.2, 2.4, yf - 0.6, yf - 0.2, 22.1, 23.7, ROCK_L))
    for k in range(3):
        p.append(B(f"rt_alt{k}", 1.0 - k * 0.1, 2.6 + k * 0.1, yf - 0.62, yf - 0.2, 23.7 + k * 0.25, 23.95 + k * 0.25, ROCK_L))
    p.append(B("rt_fire", 1.5, 2.1, yf - 0.62, yf - 0.2, 24.45, 25.1, RED))
    disc = cylinder("rt_disc", 0.6, 0.3, (0, 0, 0), ROCK_L, verts=12)
    disc.rotation_euler[0] = math.pi / 2
    p.append(turn(disc, 0, 0, yf - 0.3, 26.3))
    for sx in (-1, 1):
        p.append(B(f"rt_wing{sx}", min(sx * 0.6, sx * 3.0), max(sx * 0.6, sx * 3.0), yf - 0.55, yf - 0.2, 26.0, 26.6, ROCK_L))
    p.append(B("rt_figure", -0.25, 0.25, yf - 0.6, yf - 0.2, 26.6, 27.8, ROCK_L))
    m.add(1, J(p, "facade"), "facade")
    return m


# ================================================================ pavilion palace in a paradise

def plain_palace(variant="intact"):
    m = Model("plain-palace")
    intact = variant == "intact"
    g = [B("pp_ground", -50, 50, -50, 50, 0, 0.1, "#9FA878" if intact else EARTH)]
    walls = [(-50, -4, -50, -48.8), (4, 50, -50, -48.8), (-50, 50, 48.8, 50), (-50, -48.8, -48.8, 48.8), (48.8, 50, -48.8, 48.8)]
    for k, (a, b, c, d) in enumerate(walls):
        if intact:
            g.append(B(f"pp_w{k}", a, b, c, d, 0, 3.0, MUD))
            g.append(B(f"pp_wc{k}", a - 0.1, b + 0.1, c - 0.1, d + 0.1, 3.0, 3.3, MUD_D))
        else:
            g.append(mound(f"pp_w{k}", a, b, c, d, 1.0, EARTH_D))
    # stone channels: a rectangle with a central axis, basins at the corners
    ch = [(-30, 30, -41, -40), (-30, 30, 9, 10), (-30.5, -29.5, -41, 10), (29.5, 30.5, -41, 10), (-0.5, 0.5, -41, 10)]
    for k, (a, b, c, d) in enumerate(ch):
        g.append(B(f"pp_ch{k}", a - 0.4, b + 0.4, c - 0.4, d + 0.4, 0.1, 0.35, STONE))
        if intact:
            g.append(B(f"pp_wt{k}", a, b, c, d, 0.1, 0.38, WATERC))
    for k, (x, y) in enumerate(((-30, -40.5), (30, -40.5), (-30, 9.5), (30, 9.5), (0, -15.0))):
        g.append(B(f"pp_bs{k}", x - 1.6, x + 1.6, y - 1.6, y + 1.6, 0.1, 0.45, STONE))
        if intact:
            g.append(B(f"pp_bw{k}", x - 1.2, x + 1.2, y - 1.2, y + 1.2, 0.1, 0.5, WATERC))
    m.add(0, J(g, "garden"), "garden")
    t = []
    rnd = random.Random(5)
    spots = [(x, y) for x in (-24, -16, -8, 8, 16, 24) for y in (-34, -24, -14, -4, 4)]
    spots += [(x, y) for x in (-42, 42) for y in (-40, -28, -16, -4, 8, 20, 32, 42)]
    for k, (x, y) in enumerate(spots):
        if intact:
            kind = "cypress" if (x in (-42, 42) or (k % 5 == 0)) else "round"
            t.append(tree(f"pp_t{k}", 2.0 if kind == "round" else 1.6, (x, y, 0.1), LEAF if kind == "round" else CYPRESS, kind=kind))
        elif k % 4 == 0:
            t.append(cylinder(f"pp_st{k}", 0.35, 0.8, (x, y, 0.1), TIMBER, verts=6))
    m.add(1, J(t, "trees"), "trees")
    # the pavilion at the head of the garden, a gatehouse at the foot
    p = [B("pp_plat", -21, 21, 14, 42, 0, 1.2, STONE)]
    porch_s = [(x, 17.5) for x in (-15, -9, -3, 3, 9, 15)]
    porch_n = [(x, 38.5) for x in (-15, -9, -3, 3, 9, 15)]
    hall = col_grid([-5.0, 0.0, 5.0], [25.0, 31.0])
    if intact:
        p.append(copies(persian_column("pp_col", 9.0, 0.45, detail=2), [(x, y, 1.2) for x, y in porch_s + porch_n], "pp_cols"))
        p.append(B("pp_hall", -10, 10, 21, 35, 1.2, 10.2, MUD))
        p.append(frame_at("pp_d", 2.2, 5.0, 1.4, 0, 21, 1.2, "S"))
        p.append(frame_at("pp_dn", 2.2, 5.0, 1.4, 0, 35, 1.2, "N"))
        for sx in (-1, 1):
            p.append(frame_at(f"pp_w{sx}", 1.4, 2.6, 1.2, sx * 10, 28, 2.4, "E" if sx > 0 else "W"))
            p.append(B(f"pp_side{sx}", min(sx * 10, sx * 18), max(sx * 10, sx * 18), 21, 35, 1.2, 6.2, shade(MUD, -0.04)))
        p.append(B("pp_gate", -5, 5, -50.5, -44.5, 0, 6.0, MUD))
        p.append(frame_at("pp_gd", 2.4, 4.0, 1.4, 0, -50.5, 0, "S"))
        m.add(2, J(p, "pavilion"), "pavilion")
        r = [B("pp_roof", -18.5, 18.5, 15.5, 40.5, 10.2, 11.0, ROOF), B("pp_beam", -18.5, 18.5, 15.4, 16.2, 9.4, 10.2, CEDAR),
             B("pp_beamn", -18.5, 18.5, 39.8, 40.6, 9.4, 10.2, CEDAR), merlon_rect("pp_rm", -18.5, 18.5, 15.5, 40.5, 11.0, size=1.2),
             B("pp_sroof", -18.2, 18.2, 20.8, 35.2, 6.2, 6.6, ROOF)]
        r.append(merlon_rect("pp_gm", -5, 5, -50.5, -44.5, 6.0, size=1.0))
        m.add(3, J(r, "roof"), "roof")
    else:
        p.append(copies(column_base("pp_base", 0.45, color=shade(COL, -0.08)), [(x, y, 1.2) for x, y in porch_s + porch_n + hall], "pp_bases"))
        p.append(frame_at("pp_d", 2.2, 5.0, 1.4, 0, 21, 1.2, "S", panel=False))
        p.append(mound("pp_hm", -10, 10, 21, 35, 1.4, EARTH, 1.2))
        p.append(mound("pp_gm", -5, 5, -50.5, -44.5, 1.6, EARTH_D))
        m.add(2, J(p, "ruin"), "pavilion")
    return m


BUILDERS = {
    "persepolis/takht": lambda: takht("460"),
    "persepolis/takht-500": lambda: takht("500"),
    "persepolis/takht-ruin": lambda: takht("ruin"),
    "persepolis/apadana": lambda: apadana("460"),
    "persepolis/apadana-500": lambda: apadana("500"),
    "persepolis/apadana-burned": lambda: apadana("burned"),
    "persepolis/apadana-ruin": lambda: apadana("ruin"),
    "persepolis/gate-all-nations": lambda: gate_all_nations("460"),
    "persepolis/gate-all-nations-ruin": lambda: gate_all_nations("ruin"),
    "persepolis/hundred-columns": lambda: hundred_columns("460"),
    "persepolis/hundred-columns-ruin": lambda: hundred_columns("ruin"),
    "persepolis/unfinished-gate": unfinished_gate,
    "persepolis/tachara": lambda: tachara("intact"),
    "persepolis/tachara-ruin": lambda: tachara("ruin"),
    "persepolis/tripylon": lambda: tripylon("intact"),
    "persepolis/tripylon-ruin": lambda: tripylon("ruin"),
    "persepolis/hadish": lambda: hadish("intact"),
    "persepolis/hadish-ruin": lambda: hadish("ruin"),
    "persepolis/harem": lambda: harem("intact"),
    "persepolis/harem-ruin": lambda: harem("ruin"),
    "persepolis/treasury": lambda: treasury("intact"),
    "persepolis/treasury-ruin": lambda: treasury("ruin"),
    "persepolis/garrison": lambda: garrison("intact"),
    "persepolis/garrison-ruin": lambda: garrison("ruin"),
    "persepolis/royal-tomb": royal_tomb,
    "persepolis/plain-palace": lambda: plain_palace("intact"),
    "persepolis/plain-palace-ruin": lambda: plain_palace("ruin"),
}
