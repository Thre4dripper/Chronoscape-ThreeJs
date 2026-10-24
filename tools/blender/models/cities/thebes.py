"""Thebes (Waset) landmark miniatures: Karnak and its precincts, the processional way, Luxor temple, and the temples,
tombs and villages of the west bank.

Conventions as in FORMAT.md: metres, origin at the ground centre, +X east, +Y north, the main front toward -Y;
the landmark rotation turns it on the map.
"""
import math
import random
import bpy
from mathutils import Matrix
from chronokit import Model, box, cylinder, join, shade, mesh_from, ring_extrude
from worldkit import *

SAND, SAND_DK, PAVE = "#D9C49A", "#CBB48A", "#E2D3B4"
SANDSTONE, SANDSTONE_LT, SANDSTONE_DK = "#CDB389", "#DCC6A0", "#B79B72"
LIME = "#E4D9C2"
MUD, MUD_LT, MUD_DK = "#AE8D6A", "#C3A57F", "#977756"
GRANITE_R, GRANITE_B, QUARTZITE, QUARTZ_RED = "#9A5B49", "#4E4A48", "#B5876A", "#A2584A"
PAINT_BLUE, PAINT_RED, PAINT_YEL = "#4A6790", "#A4503B", "#D1A957"
GOLD = "#D4AE55"
PALM, FIELD, NILE = "#6E8A55", "#A9AE72", "#5E8A86"
ROCK, ROCK_DK, ROCK_LT = "#C4A47A", "#A98A62", "#D6BE94"
PENNANT = "#B8433A"
HOUSE_COLS = ["#C9AE88", "#D4BE9A", "#BFA27C", "#DCC9A8", "#C6A780"]
FACE_ROT = {"S": 0, "N": 180, "E": 90, "W": -90}


# ---------------------------------------------------------------- generic helpers

def link_mesh(name, me):
    o = bpy.data.objects.new(name, me)
    bpy.context.collection.objects.link(o)
    return o


def clone(o, name, x=0.0, y=0.0, z=0.0, deg=0.0, tilt_x=0.0, tilt_y=0.0, scale=1.0):
    """A transformed copy of a prototype object (its mesh copied, so materials come along)."""
    me = o.data.copy()
    M = (Matrix.Translation((x, y, z)) @ Matrix.Rotation(math.radians(deg), 4, "Z") @ Matrix.Rotation(math.radians(tilt_y), 4, "Y")
         @ Matrix.Rotation(math.radians(tilt_x), 4, "X") @ Matrix.Scale(scale, 4) @ o.matrix_world)
    me.transform(M)
    return link_mesh(name, me)


def drop(o):
    if o is not None:
        bpy.data.objects.remove(o, do_unlink=True)


def scatter(proto, name, spots):
    """Clones of a prototype at [(x, y, deg), ...] (or (x, y, deg, z)), joined; the prototype is removed."""
    out = []
    for i, s in enumerate(spots):
        x, y, deg = s[0], s[1], s[2]
        z = s[3] if len(s) > 3 else 0.0
        out.append(clone(proto, f"{name}{i}", x, y, z, deg))
    drop(proto)
    return join(out, name)


def place(o, x=0.0, y=0.0, deg=0.0, z=0.0):
    o = move(o)
    if deg:
        o = rot(o, deg)
    return move(o, x, y, z)


def pivot(o, deg, px, py):
    """Turn a part by deg (counter-clockwise) about the point (px, py)."""
    o = move(o, -px, -py, 0)
    o = rot(o, deg)
    return move(o, px, py, 0)


def ground(name, w, d, color=SAND, h=0.3, loc=(0, 0, 0)):
    return box(name, w, d, h, loc, color)


def quad(name, pts, color):
    """A single coloured face (a painted panel or a pool surface); pts counter-clockwise seen from its front."""
    return mesh_from(name, pts, [tuple(range(len(pts)))], (0, 0, 0), color)


def wedge(name, w, length, h, loc=(0, 0, 0), color=SANDSTONE, face="S"):
    """A ramp rising from z=0 at its front (-Y before rotation) to h at its back."""
    v = [(-w / 2, -length / 2, 0), (w / 2, -length / 2, 0), (w / 2, length / 2, 0), (-w / 2, length / 2, 0), (-w / 2, length / 2, h), (w / 2, length / 2, h)]
    f = [(3, 2, 1, 0), (0, 1, 5, 4), (1, 2, 5), (3, 0, 4), (2, 3, 4, 5)]
    o = mesh_from(name, v, f, (0, 0, 0), color)
    o = rot(o, FACE_ROT[face])
    return move(o, *loc)


def vault_row(name, n, w, length, wall_h, loc=(0, 0, 0), color=MUD, along="y", gap=0.8):
    """n parallel barrel-vaulted brick magazines side by side: each a box with a half-cylinder roof."""
    x0, y0, z0 = loc
    parts = []
    seg = 8
    for i in range(n):
        off = (i - (n - 1) / 2) * (w + gap)
        cx, cy = (x0 + off, y0) if along == "y" else (x0, y0 + off)
        bw, bd = (w, length) if along == "y" else (length, w)
        parts.append(box(f"{name}w{i}", bw, bd, wall_h, (cx, cy, z0), color))
        verts, faces = [], []
        for k in range(seg + 1):
            a = math.pi * k / seg
            u, zz = -w / 2 * math.cos(a), w / 2 * math.sin(a) * 0.9
            for e in (-length / 2, length / 2):
                verts.append((cx + u, cy + e, z0 + wall_h + zz) if along == "y" else (cx + e, cy + u, z0 + wall_h + zz))
        for k in range(seg):
            a, b = 2 * k, 2 * (k + 1)
            faces.append((a, b, b + 1, a + 1))
        faces.append(tuple(range(0, 2 * seg + 2, 2)))
        faces.append(tuple(range(2 * seg + 1, 0, -2)))
        parts.append(mesh_from(f"{name}v{i}", verts, faces, (0, 0, 0), shade(color, 0.05)))
    return join(parts, name)


def brick_wall(name, pts, h, t, color=MUD, batter=0.3, crenels=False, closed=False):
    """A battered mud-brick wall along a polyline (optionally closed), with corner blocks and optional rounded crenellations."""
    if closed:
        pts = list(pts) + [pts[0]]
    parts = []
    for i in range(1, len(pts)):
        (ax, ay), (bx, by) = pts[i - 1], pts[i]
        L = math.hypot(bx - ax, by - ay)
        a = math.degrees(math.atan2(by - ay, bx - ax))
        seg = frustum(f"{name}s{i}", L + t * 0.2, t * (1 + batter), L + t * 0.2, t, h, (0, 0, 0), color)
        parts.append(place(seg, (ax + bx) / 2, (ay + by) / 2, a))
        if crenels:
            n = max(1, int(L / 2.6))
            for k in range(n):
                u = -L / 2 + (k + 0.5) * L / n
                c = cylinder(f"{name}c{i}_{k}", t * 0.32, 1.1, (0, 0, 0), shade(color, -0.04), verts=6)
                parts.append(place(c, (ax + bx) / 2 + math.cos(math.radians(a)) * u, (ay + by) / 2 + math.sin(math.radians(a)) * u, 0, h))
    return join(parts, name)


def sacred_lake(name, w, d, loc=(0, 0, 0), stone=SANDSTONE_DK, steps_n=4):
    """A rectangular stone-lined pool with stairs at the corners."""
    x, y, z = loc
    r = 2.5
    parts = [box(name + "_n", w + 2 * r, r, 1.0, (x, y + d / 2 + r / 2, z), stone), box(name + "_s", w + 2 * r, r, 1.0, (x, y - d / 2 - r / 2, z), stone),
             box(name + "_e", r, d, 1.0, (x + w / 2 + r / 2, y, z), stone), box(name + "_w", r, d, 1.0, (x - w / 2 - r / 2, y, z), stone),
             box(name + "_water", w, d, 0.55, (x, y, z), NILE)]
    for sx, sy in ((-1, -1), (1, -1), (1, 1), (-1, 1)):
        for k in range(steps_n):
            parts.append(box(f"{name}_st{sx}{sy}{k}", 6 - k, 3, 0.9 - k * 0.12, (x + sx * (w / 2 - 3 + k * 0.4), y + sy * (d / 2 - 1.5 - k * 2.2), z), stone))
    return join(parts, name)


def palms(name, spots, r=2.2, z=0.3):
    return join([tree(f"{name}{i}", r * (0.85 + 0.3 * ((i * 37) % 7) / 7), (x, y, z), PALM, TIMBER, "palm") for i, (x, y) in enumerate(spots)], name)


def palm_ring(name, x0, x1, y0, y1, n, seed=1, r=2.2):
    rnd = random.Random(seed)
    return palms(name, [(rnd.uniform(x0, x1), rnd.uniform(y0, y1)) for _ in range(n)], r)


def e_house(name, w, d, h, loc, color, door="S", extras=True, roofless=False, simple=False):
    """An Egyptian mud-brick house: whitewashed walls, a flat roof with a low parapet, a roof shelter and a dark doorway."""
    x, y, z = loc
    if roofless:
        t = 0.6
        parts = [box(name + "n", w, t, h, (x, y + d / 2 - t / 2, z), color), box(name + "s", w, t, h * 0.7, (x, y - d / 2 + t / 2, z), color),
                 box(name + "e", t, d, h * 0.85, (x + w / 2 - t / 2, y, z), color), box(name + "w", t, d, h * 0.55, (x - w / 2 + t / 2, y, z), color),
                 box(name + "f", w - 1, d - 1, 0.25, (x, y, z), shade(SAND, -0.05))]
        return join(parts, name)
    dx, dy = {"S": (0, -d / 2), "N": (0, d / 2), "E": (w / 2, 0), "W": (-w / 2, 0)}[door]
    dw = min(w, d) * 0.22
    if simple:
        parts = [box(name + "b", w, d, h, (x, y, z), color), box(name + "r", w - 0.8, d - 0.8, 0.12, (x, y, z + h - 0.06), shade(color, -0.18)),
                 box(name + "d", dw if door in "SN" else 0.3, 0.3 if door in "SN" else dw, min(2.0, h * 0.6), (x + dx, y + dy, z), DARK)]
        if extras:
            parts.append(box(name + "sh", w * 0.3, d * 0.3, 1.5, (x + w * 0.2, y + d * 0.2, z + h), shade(color, 0.05)))
        return join(parts, name)
    parts = [box(name + "b", w, d, h, (x, y, z), color), box(name + "r", w - 0.7, d - 0.7, 0.18, (x, y, z + h), shade(color, -0.16)),
             box(name + "p1", w, 0.35, 0.5, (x, y - d / 2 + 0.175, z + h), color)]
    parts.append(box(name + "p2", w, 0.35, 0.5, (x, y + d / 2 - 0.175, z + h), color))
    parts.append(box(name + "p3", 0.35, d, 0.5, (x - w / 2 + 0.175, y, z + h), color))
    parts.append(box(name + "p4", 0.35, d, 0.5, (x + w / 2 - 0.175, y, z + h), color))
    parts.append(box(name + "d", dw if door in "SN" else 0.3, 0.3 if door in "SN" else dw, min(2.0, h * 0.6), (x + dx, y + dy, z), DARK))
    if extras:
        parts.append(box(name + "sh", w * 0.35, d * 0.35, 1.6, (x + w * 0.22, y + d * 0.22, z + h), shade(color, 0.04)))
        parts.append(cylinder(name + "si", min(w, d) * 0.12, 1.4, (x - w * 0.25, y - d * 0.2, z + h), shade(color, -0.08), verts=8))
    return join(parts, name)


def house_field(name, x0, x1, y0, y1, seed=3, size=(6, 12), h=(4, 7), lane=2.5, fill=0.85, z=0.3, avoid=(), color_set=HOUSE_COLS, roofless=False, simple=True):
    """Blocks of houses on a jittered grid with lanes; avoid = [(xa, xb, ya, yb), ...] rectangles left clear."""
    rnd = random.Random(seed)
    out = []
    y = y0
    i = 0
    while y < y1 - size[0]:
        row_d = rnd.uniform(*size)
        x = x0
        while x < x1 - size[0]:
            w = rnd.uniform(*size)
            if x + w > x1:
                break
            cx, cy = x + w / 2, y + row_d / 2
            clear = all(not (xa - 1 < cx < xb + 1 and ya - 1 < cy < yb + 1) for xa, xb, ya, yb in avoid)
            if clear and rnd.random() < fill:
                out.append(e_house(f"{name}{i}", w - 0.6, row_d - 0.6, rnd.uniform(*h), (cx, cy, z), color_set[i % len(color_set)],
                                   rnd.choice("SN"), rnd.random() < 0.3, roofless, simple))
                i += 1
            x += w + (lane if rnd.random() < 0.3 else 0.4)
        y += row_d + lane
    return join(out, name) if out else None


# ---------------------------------------------------------------- statues, sphinxes, columns, obelisks

def sphinx_proto(name, s=1.0, kind="human", color=SANDSTONE, base=True):
    """A sphinx lying on a plinth, facing -Y; s=1 is about 5 m long."""
    p = []
    z = 0.9 * s if base else 0.0
    if base:
        p.append(box(name + "b", 1.7 * s, 5.4 * s, 0.9 * s, (0, 0, 0), shade(color, -0.08)))
    p.append(box(name + "body", 1.3 * s, 3.0 * s, 1.0 * s, (0, 0.6 * s, z), color))
    p.append(box(name + "hq", 1.42 * s, 1.3 * s, 1.35 * s, (0, 1.45 * s, z), color))
    p.append(box(name + "paw", 1.2 * s, 1.7 * s, 0.42 * s, (0, -1.65 * s, z), color))
    p.append(box(name + "ch", 1.15 * s, 0.9 * s, 1.6 * s, (0, -0.75 * s, z), color))
    if kind == "ram":
        p.append(box(name + "hd", 0.7 * s, 1.35 * s, 0.75 * s, (0, -1.05 * s, z + 1.4 * s), color))
        p.append(box(name + "hn", 1.55 * s, 0.5 * s, 0.42 * s, (0, -0.6 * s, z + 1.6 * s), shade(color, -0.12)))
    elif kind == "jackal":
        p.append(box(name + "hd", 0.6 * s, 1.2 * s, 0.6 * s, (0, -1.0 * s, z + 1.45 * s), shade(color, -0.25)))
        p.append(box(name + "ea", 0.5 * s, 0.2 * s, 0.6 * s, (0, -0.55 * s, z + 2.0 * s), shade(color, -0.25)))
    else:
        p.append(frustum(name + "nm", 1.45 * s, 1.0 * s, 0.85 * s, 0.7 * s, 1.0 * s, (0, -0.55 * s, z + 1.5 * s), color))
        p.append(box(name + "fc", 0.62 * s, 0.4 * s, 0.82 * s, (0, -1.15 * s, z + 1.58 * s), shade(color, 0.06)))
    return join(p, name)


def seated_proto(name, H, color=QUARTZITE, crown="double", base=True, queen=False):
    """A seated king on a block throne, facing -Y; H is the total height with the base."""
    H = H / 0.95
    p = []
    bh = 0.12 * H if base else 0.0
    if base:
        p.append(box(name + "b", 0.52 * H, 0.74 * H, bh, (0, 0.05 * H, 0), shade(color, -0.1)))
    z = bh
    p.append(box(name + "th", 0.44 * H, 0.42 * H, 0.29 * H, (0, 0.15 * H, z), shade(color, -0.04)))
    p.append(box(name + "bk", 0.44 * H, 0.09 * H, 0.5 * H, (0, 0.32 * H, z), shade(color, -0.04)))
    p.append(box(name + "sh", 0.30 * H, 0.13 * H, 0.26 * H, (0, -0.13 * H, z), color))
    p.append(box(name + "ft", 0.32 * H, 0.2 * H, 0.035 * H, (0, -0.16 * H, z), color))
    p.append(box(name + "lp", 0.32 * H, 0.34 * H, 0.07 * H, (0, -0.05 * H, z + 0.24 * H), color))
    p.append(frustum(name + "to", 0.23 * H, 0.15 * H, 0.31 * H, 0.15 * H, 0.27 * H, (0, 0.13 * H, z + 0.31 * H), color))
    for sx in (-1, 1):
        p.append(box(f"{name}fa{sx}", 0.065 * H, 0.22 * H, 0.06 * H, (sx * 0.12 * H, -0.03 * H, z + 0.31 * H), color))
        p.append(box(f"{name}ua{sx}", 0.065 * H, 0.07 * H, 0.21 * H, (sx * 0.155 * H, 0.1 * H, z + 0.34 * H), color))
        if queen:
            p.append(box(f"{name}q{sx}", 0.08 * H, 0.08 * H, 0.3 * H, (sx * 0.2 * H, -0.2 * H, z), shade(color, 0.05)))
    p.append(frustum(name + "nm", 0.24 * H, 0.17 * H, 0.15 * H, 0.12 * H, 0.14 * H, (0, 0.13 * H, z + 0.57 * H), color))
    p.append(box(name + "fc", 0.12 * H, 0.06 * H, 0.11 * H, (0, 0.04 * H, z + 0.6 * H), shade(color, 0.07)))
    if crown == "double":
        p.append(cylinder(name + "cr", 0.065 * H, 0.13 * H, (0, 0.13 * H, z + 0.7 * H), shade(color, 0.05), verts=8, r_top=0.035 * H))
    return join(p, name)


def standing_proto(name, H, color=GRANITE_R, crown="double", base=True):
    """A standing king, left foot forward, with a back pillar, facing -Y."""
    p = []
    bh = 0.08 * H if base else 0.0
    if base:
        p.append(box(name + "b", 0.3 * H, 0.42 * H, bh, (0, 0, 0), shade(color, -0.1)))
    z = bh
    p.append(box(name + "bp", 0.16 * H, 0.07 * H, 0.82 * H, (0, 0.1 * H, z), shade(color, -0.05)))
    p.append(box(name + "l1", 0.07 * H, 0.08 * H, 0.42 * H, (-0.05 * H, -0.09 * H, z), color))
    p.append(box(name + "l2", 0.07 * H, 0.08 * H, 0.42 * H, (0.05 * H, 0.04 * H, z), color))
    p.append(frustum(name + "kt", 0.2 * H, 0.14 * H, 0.18 * H, 0.12 * H, 0.12 * H, (0, 0.0, z + 0.4 * H), shade(color, 0.08)))
    p.append(frustum(name + "to", 0.15 * H, 0.1 * H, 0.22 * H, 0.11 * H, 0.2 * H, (0, 0.0, z + 0.52 * H), color))
    for sx in (-1, 1):
        p.append(box(f"{name}a{sx}", 0.05 * H, 0.06 * H, 0.3 * H, (sx * 0.13 * H, 0.0, z + 0.42 * H), color))
    p.append(frustum(name + "nm", 0.17 * H, 0.12 * H, 0.1 * H, 0.09 * H, 0.1 * H, (0, 0.0, z + 0.72 * H), color))
    if crown == "double":
        p.append(cylinder(name + "cr", 0.045 * H, 0.1 * H, (0, 0.0, z + 0.82 * H), shade(color, 0.05), verts=8, r_top=0.025 * H))
    return join(p, name)


def osiride_proto(name, h, w=2.2, color=SANDSTONE, figure=SANDSTONE_LT):
    """A square pillar with a mummiform figure of the king against its front (-Y)."""
    p = [box(name + "p", w, w, h, (0, 0, 0), color),
         box(name + "f", w * 0.62, 0.7, h * 0.72, (0, -w / 2 - 0.35, 0), figure),
         box(name + "hd", w * 0.42, 0.6, h * 0.1, (0, -w / 2 - 0.3, h * 0.72), figure),
         cylinder(name + "cr", w * 0.16, h * 0.12, (0, -w / 2 - 0.3, h * 0.82), figure, verts=8, r_top=w * 0.08)]
    return join(p, name)


def column_proto(name, r, h, kind="open", color=SANDSTONE, band=PAINT_BLUE):
    """A papyrus column on a round base: 'open' (bell capital, for the tall central aisles) or 'bud' (closed capital)."""
    p = [cylinder(name + "b", r * 1.35, h * 0.035, (0, 0, 0), shade(color, -0.06), verts=10)]
    sh = h * (0.8 if kind == "open" else 0.84)
    p.append(cylinder(name + "s", r, sh, (0, 0, h * 0.035), color, verts=10, r_top=r * 0.88))
    if band:
        p.append(cylinder(name + "bd", r * 0.9, h * 0.025, (0, 0, h * 0.035 + sh - h * 0.06), band, verts=10))
    z = h * 0.035 + sh
    if kind == "open":
        p.append(cylinder(name + "c", r * 0.88, h * 0.13, (0, 0, z), shade(color, 0.05), verts=10, r_top=r * 1.75))
        z += h * 0.13
    else:
        p.append(cylinder(name + "c1", r * 0.88, h * 0.05, (0, 0, z), shade(color, 0.05), verts=10, r_top=r * 1.1))
        p.append(cylinder(name + "c2", r * 1.1, h * 0.07, (0, 0, z + h * 0.05), shade(color, 0.05), verts=10, r_top=r * 0.75))
        z += h * 0.12
    a = r * (2.1 if kind == "open" else 1.6)
    p.append(box(name + "ab", a, a, h * 0.035, (0, 0, z), shade(color, 0.08)))
    return join(p, name)


def obelisk_t(name, h, loc=(0, 0, 0), color=GRANITE_R, tip=GOLD, base=True):
    """An obelisk on a pedestal with a gilded pyramidion."""
    x, y, z = loc
    b = h * 0.095
    p = []
    zb = z
    if base:
        p.append(box(name + "pd", b * 1.7, b * 1.7, b * 0.7, (x, y, z), shade(color, -0.12)))
        zb = z + b * 0.7
    sh = h * 0.9
    p.append(frustum(name + "s", b, b, b * 0.68, b * 0.68, sh, (x, y, zb), color))
    p.append(frustum(name + "t", b * 0.68, b * 0.68, 0.02, 0.02, h - sh, (x, y, zb + sh), tip))
    return join(p, name)


def batter_panel(name, cx, half_w, z0, z1, d0, d1, h, color, offset=0.12):
    """A flat panel on the battered front (-Y) face of a tower whose depth tapers from d0 at z=0 to d1 at z=h."""
    yy = lambda z: -(d0 / 2 - (d0 - d1) / 2 * z / h) - offset
    pts = [(cx - half_w, yy(z0), z0), (cx + half_w, yy(z0), z0), (cx + half_w, yy(z1), z1), (cx - half_w, yy(z1), z1)]
    return quad(name, pts, color)


def e_pylon(name, w, h, d, loc=(0, 0, 0), color=SANDSTONE, face="S", gate=None, flags=2, relief=True, unfinished=None, back_relief=False):
    """An Egyptian pylon: two battered towers with torus and cavetto cornice, a taller-than-wide gateway, flagstaffs
    with pennants in front, and painted relief panels on the towers' faces. unfinished = (left, right) height fractions."""
    x, y, z = loc
    gw = gate or w * 0.13
    tw = (w - gw) / 2
    p = []
    for s in (-1, 1):
        cx = s * (gw / 2 + tw / 2)
        frac = 1.0 if not unfinished else unfinished[0 if s < 0 else 1]
        th = h * frac
        p.append(frustum(f"{name}t{s}", tw, d, tw - (tw * 0.14) * frac, d - d * 0.26 * frac, th, (cx, 0, 0), color))
        t1w, t1d = tw * 0.86, d * 0.74
        if not unfinished:
            p.append(box(f"{name}tr{s}", t1w + 0.4, t1d + 0.4, h * 0.022, (cx, 0, th), shade(color, -0.07)))
            p.append(frustum(f"{name}cv{s}", t1w + 0.4, t1d + 0.4, t1w + h * 0.07, t1d + h * 0.07, h * 0.06, (cx, 0, th + h * 0.022), shade(color, 0.06)))
            if relief:
                p.append(batter_panel(f"{name}rl{s}", cx, tw * 0.3, h * 0.12, h * 0.72, d, t1d, h, shade(color, -0.13)))
                p.append(batter_panel(f"{name}rb{s}", cx, tw * 0.34, h * 0.76, h * 0.8, d, t1d, h, PAINT_BLUE, 0.16))
                p.append(batter_panel(f"{name}rr{s}", cx, tw * 0.34, h * 0.08, h * 0.1, d, t1d, h, PAINT_RED, 0.16))
                if back_relief:
                    q = batter_panel(f"{name}bl{s}", 0, tw * 0.3, h * 0.12, h * 0.72, d, t1d, h, shade(color, -0.13))
                    q = rot(q, 180)
                    p.append(move(q, cx, 0, 0))
        for k in range(flags):
            fx = cx - s * (tw * 0.18 + k * tw * 0.22)
            if not unfinished:
                p.append(cylinder(f"{name}fs{s}{k}", 0.42, h * 1.18, (fx, -d / 2 - 0.55, 0), TIMBER, verts=6))
                p.append(box(f"{name}pn{s}{k}", 0.12, 1.4, 4.2, (fx, -d / 2 - 1.3, h * 1.18 - 4.4), PENNANT if k % 2 == 0 else PAINT_BLUE))
    gh = h * 0.66
    p.append(box(name + "g", gw + 1.2, d * 0.84, gh, (0, 0, 0), shade(color, 0.03)))
    p.append(frustum(name + "gc", gw + 1.2, d * 0.84, gw + 1.2 + h * 0.05, d * 0.84 + h * 0.05, h * 0.045, (0, 0, gh), shade(color, 0.07)))
    p.append(box(name + "dr", gw * 0.6, d * 0.88, gh * 0.72, (0, 0, 0), DARK))
    p.append(box(name + "ws", gw * 0.9, 0.2, h * 0.03, (0, -d * 0.42 - 0.1, gh * 0.8), PAINT_YEL))
    o = join(p, name)
    o = rot(o, FACE_ROT[face])
    return move(o, x, y, z)


def roofed_block(name, w, d, h, loc=(0, 0, 0), color=SANDSTONE, cornice=True, door=None, raised=None):
    """A flat-roofed stone temple block with a cavetto cornice; raised = (w, d, extra_h) central raised roof."""
    x, y, z = loc
    p = [box(name + "b", w, d, h, (x, y, z), color)]
    if cornice:
        p.append(frustum(name + "c", w, d, w + 1.2, d + 1.2, 0.9, (x, y, z + h), shade(color, 0.06)))
    if raised:
        rw, rd, rh = raised
        p.append(box(name + "rs", rw, rd, rh, (x, y, z + h), color))
        p.append(frustum(name + "rc", rw, rd, rw + 0.8, rd + 0.8, 0.6, (x, y, z + h + rh), shade(color, 0.06)))
    if door:
        dx, dy = {"S": (0, -d / 2), "N": (0, d / 2), "E": (w / 2, 0), "W": (-w / 2, 0)}[door]
        dw = min(w, d) * 0.18
        p.append(box(name + "d", dw if door in "SN" else 0.4, 0.4 if door in "SN" else dw, h * 0.6, (x + dx, y + dy, z), DARK))
    return join(p, name)


def peristyle_cols(proto, name, x0, x1, y0, y1, nx, ny, rows=1, gap=4.0, sides="NSEW", z=0.0):
    """Columns round a court: nx along the N and S sides, ny along E and W (corners shared), `rows` deep inward."""
    spots = []
    for r in range(rows):
        a0, a1, b0, b1 = x0 + r * gap, x1 - r * gap, y0 + r * gap, y1 - r * gap
        for i in range(nx):
            xx = a0 + (a1 - a0) * i / max(1, nx - 1)
            if "S" in sides:
                spots.append((xx, b0, 0, z))
            if "N" in sides:
                spots.append((xx, b1, 0, z))
        for j in range(1, ny - 1):
            yy = b0 + (b1 - b0) * j / max(1, ny - 1)
            if "W" in sides:
                spots.append((a0, yy, 0, z))
            if "E" in sides:
                spots.append((a1, yy, 0, z))
    return scatter(proto, name, spots)


def court_walls(name, x0, x1, y0, y1, h, t=2.0, color=SANDSTONE, gaps=()):
    """Walls round a rectangle; gaps = sides ('N', 'S', 'E', 'W') left open (where pylons stand)."""
    p = []
    if "S" not in gaps:
        p.append(box(name + "s", x1 - x0, t, h, ((x0 + x1) / 2, y0, 0), color))
    if "N" not in gaps:
        p.append(box(name + "n", x1 - x0, t, h, ((x0 + x1) / 2, y1, 0), color))
    if "W" not in gaps:
        p.append(box(name + "w", t, y1 - y0, h, (x0, (y0 + y1) / 2, 0), color))
    if "E" not in gaps:
        p.append(box(name + "e", t, y1 - y0, h, (x1, (y0 + y1) / 2, 0), color))
    return join(p, name)


def nile_boat(name, L, loc=(0, 0, 0), deg=0.0, sail=True, hull=TIMBER, cloth="#EEE6D2", cabin=True, sacred=False):
    """An Egyptian river boat along X: a hull curving up at both ends, a cabin, steering oars and a tall square sail."""
    W = L * 0.22
    n = 9
    verts, faces = [], []
    for i in range(n):
        u = -1 + 2 * i / (n - 1)
        hw = max(0.04, W / 2 * (1 - u * u) ** 0.7)
        zb = L * 0.06 * u * u
        zt = L * 0.07 + L * 0.1 * u ** 4
        xx = u * L / 2
        verts += [(xx, -hw, zt), (xx, hw, zt), (xx, hw * 0.6, zb), (xx, -hw * 0.6, zb)]
    for i in range(n - 1):
        a, b = 4 * i, 4 * (i + 1)
        faces += [(a, b, b + 1, a + 1), (a + 1, b + 1, b + 2, a + 2), (a + 2, b + 2, b + 3, a + 3), (a + 3, b + 3, b, a)]
    faces += [(0, 1, 2, 3), (4 * (n - 1) + 3, 4 * (n - 1) + 2, 4 * (n - 1) + 1, 4 * (n - 1))]
    col = GOLD if sacred else hull
    parts = [mesh_from(name + "h", verts, faces, (0, 0, 0), col)]
    if sacred:
        for s in (-1, 1):
            parts.append(box(f"{name}rm{s}", L * 0.05, W * 0.3, L * 0.06, (s * L * 0.47, 0, L * 0.15), GOLD))
        parts.append(box(name + "nb", L * 0.18, W * 0.5, L * 0.08, (0, 0, L * 0.07), GOLD))
        parts.append(box(name + "nv", L * 0.14, W * 0.42, L * 0.05, (0, 0, L * 0.15), "#EEE6D2"))
    elif cabin:
        parts.append(box(name + "cb", L * 0.22, W * 0.55, L * 0.07, (-L * 0.12, 0, L * 0.07), shade(hull, 0.18)))
    for s in (-1, 1):
        parts.append(box(f"{name}oar{s}", L * 0.25, 0.15, 0.15, (-L * 0.38, s * W * 0.35, L * 0.07), TIMBER))
    if sail and not sacred:
        parts.append(cylinder(name + "m", L * 0.012, L * 0.5, (L * 0.05, 0, L * 0.07), TIMBER, verts=6))
        parts.append(box(name + "s", 0.12, W * 1.9, L * 0.32, (L * 0.05, 0, L * 0.22), cloth))
        parts.append(box(name + "y", 0.2, W * 2.0, 0.2, (L * 0.05, 0, L * 0.54), TIMBER))
    o = join(parts, name)
    return place(o, loc[0], loc[1], deg, loc[2] if len(loc) > 2 else 0.0)


def rock_mass(name, x0, x1, y0, y1, hmin, hmax, seed=5, n=6, color=ROCK):
    """A jagged rock outcrop or cliff built from stacked, offset frustums."""
    rnd = random.Random(seed)
    p = []
    for i in range(n):
        w = (x1 - x0) * rnd.uniform(0.45, 0.8)
        d = (y1 - y0) * rnd.uniform(0.45, 0.8)
        cx = rnd.uniform(x0 + w / 2, x1 - w / 2)
        cy = rnd.uniform(y0 + d / 2, y1 - d / 2)
        h = rnd.uniform(hmin, hmax)
        c = color if i % 2 == 0 else shade(color, -0.07)
        p.append(frustum(f"{name}{i}", w, d, w * rnd.uniform(0.35, 0.6), d * rnd.uniform(0.35, 0.6), h, (cx, cy, 0), c))
    p.append(frustum(name + "base", x1 - x0, y1 - y0, (x1 - x0) * 0.8, (y1 - y0) * 0.8, hmin * 0.6, ((x0 + x1) / 2, (y0 + y1) / 2, 0), shade(color, -0.04)))
    return join(p, name)


def boulders(name, x0, x1, y0, y1, n, seed=7, rmax=2.0, color=ROCK, z=0.0):
    rnd = random.Random(seed)
    out = []
    for i in range(n):
        r = rnd.uniform(0.5, rmax)
        out.append(cylinder(f"{name}{i}", r, r * rnd.uniform(0.6, 1.2), (rnd.uniform(x0, x1), rnd.uniform(y0, y1), z), shade(color, rnd.uniform(-0.08, 0.04)), verts=7, r_top=r * 0.5))
    return join(out, name)


def kiosk(name, w, d, h, loc=(0, 0, 0), color=SANDSTONE, nx=4, ny=4, podium=1.4, roof=True, pillars=True, naos=True, ramps=True):
    """A barque shrine: a peripteral chapel of square pillars on a podium with ramps, cavetto-crowned."""
    x, y, z = loc
    p = [box(name + "pd", w, d, podium, (x, y, z), shade(color, -0.05)),
         frustum(name + "pc", w, d, w + 0.5, d + 0.5, 0.3, (x, y, z + podium - 0.3), shade(color, 0.05))]
    zz = z + podium
    if pillars:
        for i in range(nx):
            for j in range(ny):
                if 0 < i < nx - 1 and 0 < j < ny - 1:
                    continue
                px = x - w / 2 + 0.8 + (w - 1.6) * i / (nx - 1)
                py = y - d / 2 + 0.8 + (d - 1.6) * j / (ny - 1)
                p.append(box(f"{name}pi{i}{j}", 0.9, 0.9, h, (px, py, zz), color))
    if naos:
        p.append(box(name + "na", w * 0.45, d * 0.55, h, (x, y, zz), shade(color, 0.03)))
        p.append(box(name + "nd", w * 0.2, d * 0.56, h * 0.7, (x, y, zz), DARK))
    if roof:
        p.append(box(name + "rf", w - 0.2, d - 0.2, 0.6, (x, y, zz + h), color))
        p.append(frustum(name + "rc", w - 0.2, d - 0.2, w + 0.6, d + 0.6, 0.6, (x, y, zz + h + 0.6), shade(color, 0.06)))
    if ramps:
        p.append(wedge(name + "r1", w * 0.35, 5, podium, (x, y - d / 2 - 2.5, z), shade(color, -0.05), "S"))
        p.append(wedge(name + "r2", w * 0.35, 5, podium, (x, y + d / 2 + 2.5, z), shade(color, -0.05), "N"))
    return join(p, name)


def barque_on_stand(name, L, loc=(0, 0, 0)):
    """The god's portable barque with its veiled shrine, on a stand."""
    x, y, z = loc
    p = [box(name + "st", L * 0.25, L * 0.45, L * 0.18, (x, y, z), shade(SANDSTONE, -0.1))]
    o = nile_boat(name + "b", L, (0, 0, 0), 90, sail=False, sacred=True)
    o = move(o, x, y, z + L * 0.18)
    p.append(o)
    return join(p, name)


# ---------------------------------------------------------------- Karnak

AX = -50.0          # x of Karnak's main (east-west) axis in the model; the model's +X is real south


def _hypostyle(m, name, y0, y1, hw, cut=True):
    """The Great Hypostyle Hall: 12 open-papyrus columns in the nave, 122 bud columns in the aisles, a clerestory;
    the roof of part of the north wing is left off to show the columns."""
    d = y1 - y0
    cy = (y0 + y1) / 2
    nave = column_proto(name + "pn", 1.75, 21.0, "open", SANDSTONE)
    spots = []
    for sx in (-1, 1):
        for j in range(6):
            spots.append((AX + sx * 5.2, y0 + d * (j + 0.5) / 6, 0))
    m.add(2, scatter(nave, name + "_nave", spots), "hypostyle")
    aisle = column_proto(name + "pa", 1.35, 14.5, "bud", SANDSTONE)
    spots = []
    for sx in (-1, 1):
        for i in range(7):
            xx = AX + sx * (10.5 + (hw - 13.0) * i / 6)
            for j in range(9):
                if i == 0 and j in (0, 8):
                    continue
                spots.append((xx, y0 + d * (j + 0.5) / 9, 0))
    m.add(2, scatter(aisle, name + "_aisles", spots))
    p = []
    zr = 14.5
    for sx in (-1, 1):
        p.append(box(f"{name}_sw{sx}", 2.2, d, zr + 1.2, (AX + sx * (hw + 1.1), cy, 0), SANDSTONE_DK))
        p.append(box(f"{name}_ar{sx}", 2.8, d, 1.2, (AX + sx * 5.2, cy, 21.0 - 1.2), SANDSTONE))
    # aisle roofs (north wing partly cut away)
    for sx in (-1, 1):
        w = hw - 8.0
        xm = AX + sx * (8.0 + w / 2)
        if cut and sx < 0:
            p.append(box(f"{name}_ra{sx}", w * 0.4, d + 1, 1.0, (AX + sx * (8.0 + w * 0.2), cy, zr), shade(SANDSTONE, 0.05)))
            p.append(box(f"{name}_rb{sx}", w * 0.6, d * 0.3, 1.0, (AX + sx * (8.0 + w * 0.7), y1 - d * 0.15, zr), shade(SANDSTONE, 0.05)))
        else:
            p.append(box(f"{name}_ra{sx}", w, d + 1, 1.0, (xm, cy, zr), shade(SANDSTONE, 0.05)))
    # clerestory: stone grilles between the aisle roof and the nave roof
    zc = 21.0
    for sx in (-1, 1):
        p.append(box(f"{name}_cl{sx}", 1.4, d, zc - zr - 1.0, (AX + sx * 8.0, cy, zr + 1.0), SANDSTONE))
        for j in range(8):
            p.append(box(f"{name}_gr{sx}{j}", 1.5, d / 8 * 0.55, (zc - zr - 1.0) * 0.6, (AX + sx * 8.0, y0 + d * (j + 0.5) / 8, zr + 1.8), DARK))
    p.append(box(name + "_rn", 17.5, d + 1, 1.1, (AX, cy, zc), shade(SANDSTONE, 0.07)))
    p.append(box(name + "_rnb", 17.5, 0.6, 0.6, (AX, y0 - 0.2, zc + 1.1), PAINT_BLUE))
    m.add(2, join(p, name + "_roof"))


def _karnak_inner(m, v):
    """The inner temple from the third pylon east: obelisk courts, inner pylons, sanctuary, MK court, Akh-menu."""
    p = []
    if v in ("1250", "late"):
        m.add(1, e_pylon("k_p3", 96, 26, 11, (AX, -61, 0), SANDSTONE, back_relief=False), "pylons")
    if v in ("1470", "1250", "late"):
        m.add(1, e_pylon("k_p4", 72, 22, 7, (AX, -41.5, 0), SANDSTONE, flags=2))
        m.add(1, e_pylon("k_p5", 58, 17, 5, (AX, -24.5, 0), SANDSTONE, flags=1, relief=False))
        # Wadjet hall walls and roofed side aisles round Hatshepsut's obelisks
        p.append(court_walls("k_wadj", AX - 33, AX + 33, -38, -27, 10, 1.6, SANDSTONE_DK, gaps=("N", "S")))
        wc = column_proto("k_wcol", 0.9, 9.0, "bud", SANDSTONE, band=None)
        spots = [(AX + sx * dx, yy, 0) for sx in (-1, 1) for dx in (14, 20, 26) for yy in (-35, -30)]
        p.append(scatter(wc, "k_wcols", spots))
        # inner walls along the axis east of the 5th pylon to the sanctuary
        p.append(court_walls("k_inner", AX - 30, AX + 30, -22, 6, 8, 1.6, SANDSTONE_DK, gaps=("S",)))
        p.append(roofed_block("k_maat_n", 18, 24, 7, (AX - 19, -8, 0), SANDSTONE_LT))
        p.append(roofed_block("k_maat_s", 18, 24, 7, (AX + 19, -8, 0), SANDSTONE_LT))
    if v in ("1250", "late"):
        m.add(1, e_pylon("k_p6", 46, 12, 4, (AX, -18, 0), SANDSTONE, flags=0, relief=False))
        # Thutmose III's granite barque sanctuary
        p.append(box("k_sanct", 8, 18, 7.5, (AX, -6, 0), GRANITE_R))
        p.append(frustum("k_sanctc", 8, 18, 8.8, 18.8, 0.7, (AX, -6, 7.5), shade(GRANITE_R, 0.08)))
        p.append(box("k_sanctd", 3, 18.2, 4.5, (AX, -6, 0), DARK))
    if v == "1470":
        # the Red Chapel: red quartzite on a black granite plinth
        p.append(box("k_redb", 7.5, 19, 1.0, (AX, -7, 0), GRANITE_B))
        p.append(box("k_red", 6.5, 18, 5.4, (AX, -7, 1.0), QUARTZ_RED))
        p.append(frustum("k_redc", 6.5, 18, 7.4, 18.9, 0.6, (AX, -7, 6.4), shade(QUARTZ_RED, 0.1)))
        p.append(box("k_redd", 2.4, 18.2, 3.6, (AX, -7, 1.0), DARK))
    # Middle Kingdom court and temple (the core of every period)
    if v == "1950":
        mk = [box("k_mkplat", 46, 44, 1.2, (AX, 30, 0), LIME),
              roofed_block("k_mk", 36, 30, 7.5, (AX, 34, 1.2), LIME, door="S", raised=(14, 24, 2.0))]
        pil = box("k_mkpil", 1.6, 1.6, 6.0, (0, 0, 0), LIME)
        mk.append(scatter(pil, "k_mkpils", [(AX - 15 + 30 * i / 9, 15.5, 0, 1.2) for i in range(10)]))
        mk.append(box("k_mkporch", 33, 4, 0.6, (AX, 16.5, 7.2), shade(LIME, 0.05)))
        os_ = osiride_proto("k_mkos", 6.0, 1.6, LIME, "#EFE6D4")
        mk.append(scatter(os_, "k_mkoss", [(AX - 13.5 + 27 * i / 3, 14.2, 0, 1.2) for i in range(4)]))
        m.add(1, join(mk, "k_mktemple"), "temple")
    else:
        p.append(box("k_mkcourt", 52, 42, 0.8, (AX, 28, 0), shade(PAVE, -0.04)))
        p.append(court_walls("k_mkw", AX - 26, AX + 26, 7, 50, 6, 1.4, SANDSTONE_DK, gaps=("S",)))
    if v in ("1250", "late"):
        # Akh-menu, Thutmose III's festival hall (across the axis), with its raised central nave
        p.append(roofed_block("k_akh", 100, 44, 9, (AX, 77, 0), SANDSTONE_LT, raised=(64, 14, 4.0)))
        p.append(box("k_akhd", 5, 44.4, 6, (AX + 40, 77, 0), DARK))
        # the eastern temple and Thutmose III's single great obelisk (the Lateran obelisk)
        p.append(roofed_block("k_east", 30, 16, 7, (AX, 118, 0), SANDSTONE, door="N"))
        m.add(3, obelisk_t("k_lateran", 32, (AX, 132, 0)), "obelisks")
    m.add(1, join(p, "k_inner"))


def _karnak_south(m, v):
    """The southern processional axis: courts and the 7th-10th pylons toward Mut."""
    YS = -50.0
    p = []
    if v in ("1250", "late"):
        m.add(1, e_pylon("k_p7", 62, 22, 8, (20, YS, 0), SANDSTONE, face="E"))
        m.add(1, e_pylon("k_p9", 56, 21, 9, (152, YS, 0), SANDSTONE, face="E"))
        m.add(1, e_pylon("k_p10", 66, 28, 12, (228, YS, 0), SANDSTONE, face="E"))
        for xa, xb in ((0, 16), (24, 81), (89, 147), (157, 222)):
            p.append(box(f"k_sw{xa}a", xb - xa, 1.6, 8, ((xa + xb) / 2, YS - 26, 0), SANDSTONE_DK))
            p.append(box(f"k_sw{xa}b", xb - xa, 1.6, 8, ((xa + xb) / 2, YS + 26, 0), SANDSTONE_DK))
        # Amenhotep II's jubilee pavilion east of the 9th-10th court
        p.append(kiosk("k_amii", 26, 18, 6, (190, YS + 52, 0), SANDSTONE, 6, 4, 1.0))
        # standing colossi in the 7th pylon court
        st = standing_proto("k_c7", 9.0, GRANITE_R)
        m.add(3, scatter(st, "k_c7s", [(30, YS - 20, 90), (30, YS + 20, 90)]))
    if v in ("1470", "1250", "late"):
        m.add(1, e_pylon("k_p8", 56, 22, 10, (85, YS, 0), SANDSTONE_LT, face="E"))
    if v == "1470":
        p.append(box("k_road8", 150, 12, 0.35, (160, YS, 0), PAVE))
    if p:
        m.add(1, join(p, "k_south"))


def _karnak_obelisks(m, v):
    out = []
    if v in ("1470", "1250", "late"):
        for sx in (-1, 1):
            out.append(obelisk_t(f"k_ob_t1{sx}", 21.2, (AX + sx * 9, -50, 0)))
            out.append(obelisk_t(f"k_ob_h{sx}", 29.5, (AX + sx * 6.5, -32.5, 0)))
    if out:
        m.add(3, join(out, "k_obelisks"), "obelisks")


def _karnak_lake(m):
    m.add(0, sacred_lake("k_lake", 77, 120, (82, 52, 0)), "lake")


def _karnak_houses(m, regions, seed=7, z=0.3, fill=0.85):
    out = []
    for i, (x0, x1, y0, y1) in enumerate(regions):
        out.append(house_field(f"k_h{i}_", x0, x1, y0, y1, seed + i, (6, 11), (4, 7.5), 2.5, fill, z))
    out = [o for o in out if o is not None]
    if out:
        m.add(3, join(out, "k_houses"), "town")


def karnak(variant="1250"):
    v = variant
    m = Model("karnak")
    m.add(0, ground("k_g", 500, 580, SAND), "ground")
    if v == "1950":
        m.add(0, brick_wall("k_mkenc", [(AX - 62, -52), (AX + 62, -52), (AX + 62, 100), (AX - 62, 100)], 6, 4, MUD, closed=True), "walls")
        m.add(1, e_pylon("k_mkgate", 30, 9, 6, (AX, -52, 0), MUD_LT, flags=1, relief=False))
        _karnak_inner(m, v)
        # the White Chapel on the processional way in front of the temple
        wc = kiosk("k_white", 6.8, 6.8, 4.2, (AX, -22, 0), "#F0EADC", 4, 4, 1.2, naos=False)
        m.add(2, wc, "chapel")
        m.add(2, barque_on_stand("k_wbarque", 4.5, (AX, -22, 1.2)))
        m.add(1, box("k_way", 10, 230, 0.35, (AX, -170, 0), PAVE))
        _karnak_houses(m, [(-200, -125, -230, -80), (30, 160, -230, -100), (-200, -125, -20, 140), (30, 170, -20, 120), (-110, 10, 115, 165)], seed=11, fill=0.75)
        m.add(3, palm_ring("k_palms", -110, -62, -280, -70, 10, 4))
        m.add(3, palm_ring("k_palms2", -38, 15, -280, -70, 10, 5))
        m.add(0, join([box("k_f1", 90, 110, 0.4, (195, 230, 0), FIELD), box("k_f2", 35, 120, 0.4, (-222, -220, 0), FIELD), box("k_f3", 60, 90, 0.4, (210, -200, 0), FIELD)], "k_fields"))
        return m
    if v == "1470":
        m.add(0, brick_wall("k_tienc", [(AX - 80, -48), (AX + 80, -48), (AX + 80, 110), (AX - 80, 110)], 8, 5, MUD, closed=True), "walls")
        m.add(0, box("k_way", 14, 240, 0.35, (AX, -170, 0), PAVE))
        _karnak_inner(m, v)
        _karnak_south(m, v)
        _karnak_obelisks(m, v)
        m.add(2, barque_on_stand("k_rbarque", 4.5, (AX, -19, 0)), "chapel")
        _karnak_houses(m, [(-200, -95, -250, -80), (15, 170, -250, -110), (-210, -140, -20, 200), (40, 170, 20, 120), (-120, 120, 135, 220)], seed=21, fill=0.75)
        m.add(3, palm_ring("k_palms", -38, 0, -280, -60, 12, 5))
        m.add(3, palm_ring("k_palms2", -100, -62, -280, -60, 12, 6))
        return m
    late = v == "late"
    # enclosure walls
    if late:
        enc = [(AX - 56, -225), (-244, -225), (-244, 284), (244, 284), (244, -225), (AX + 56, -225)]
        m.add(0, brick_wall("k_nect", enc, 21, 12, MUD, batter=0.25), "walls")
        m.add(1, e_pylon("k_egate", 20, 19, 13, (AX, 284, 0), SANDSTONE_LT, face="N", gate=8, flags=0, relief=False))
        m.add(1, e_pylon("k_ngate", 18, 17, 13, (-244, -20, 0), SANDSTONE_LT, face="W", gate=7, flags=0, relief=False))
        m.add(1, e_pylon("k_eugate", 20, 19, 13, (244, -150, 0), SANDSTONE_LT, face="E", gate=8, flags=0, relief=False))
    else:
        enc = [(AX - 49, -126), (-190, -126), (-190, 205), (236, 205), (236, -126), (AX + 49, -126)]
        m.add(0, brick_wall("k_nkenc", enc, 12, 7, MUD, batter=0.25), "walls")
    _karnak_lake(m)
    # the front: dromos of rams (1250) or the first court with Taharqa's kiosk (late)
    ram = sphinx_proto("k_ram", 1.0, "ram", SANDSTONE)
    if late:
        m.add(1, e_pylon("k_p1", 113, 31.6, 15, (AX, -225, 0), SANDSTONE, unfinished=(0.7, 1.0)), "pylons")
        # the mud-brick construction ramp left behind the south tower
        m.add(1, wedge("k_ramp", 14, 34, 22, (AX + 20, -200.5, 0), MUD_LT, "N"))
        m.add(1, court_walls("k_c1", AX - 51, AX + 51, -217, -133, 9, 2.0, SANDSTONE_DK, gaps=("N", "S")))
        bub = column_proto("k_bub", 1.0, 11, "bud", SANDSTONE, band=None)
        sp = [(AX + sx * 45, -210 + 70 * j / 17, 0) for sx in (-1, 1) for j in range(18)]
        sp = [q for q in sp if not (q[0] > AX and -191 < q[1] < -159)]
        m.add(2, scatter(bub, "k_bubcols", sp), "court")
        m.add(2, box("k_bubroof", 8, 76, 0.8, (AX - 45, -175, 11.3), SANDSTONE))
        m.add(2, box("k_bubroof2", 8, 22, 0.8, (AX + 45, -202, 11.3), SANDSTONE))
        tk = column_proto("k_tah", 1.6, 21, "open", SANDSTONE_LT)
        m.add(2, scatter(tk, "k_taharqa", [(AX + sx * 7, -205 + 50 * j / 4, 0) for sx in (-1, 1) for j in range(5)]))
        m.add(2, box("k_tahscreen", 10, 46, 4, (AX, -180, 0), SANDSTONE_LT))
        # Seti II's triple shrine (north) and Ramesses III's barque temple (south side)
        m.add(1, roofed_block("k_seti2", 14, 22, 8, (AX - 24, -196, 0), SANDSTONE_LT, door="E"))
        m.add(1, e_pylon("k_r3p", 28, 13, 5, (AX + 28, -175, 0), SANDSTONE, face="W", flags=0, relief=True))
        m.add(1, roofed_block("k_r3", 29, 26, 9, (AX + 45.25, -175, 0), SANDSTONE))
        m.add(3, scatter(ram, "k_crams", [(AX - 39, -208 + 66 * j / 11, 90) for j in range(12)]), "sphinxes")
        r2 = sphinx_proto("k_ram2", 1.0, "ram", SANDSTONE)
        m.add(3, scatter(r2, "k_drams", [(AX + sx * 9, -282 + 5.5 * j, 90 * -sx) for sx in (-1, 1) for j in range(9)]))
        # the Khonsu temple in the south-west corner, facing the Euergetes gate
        m.add(1, e_pylon("k_khp", 34, 18, 8, (214, -150, 0), SANDSTONE, face="E", flags=2))
        m.add(1, court_walls("k_khc", 182, 210, -166, -134, 8, 1.6, SANDSTONE_DK, gaps=("E",)))
        m.add(1, roofed_block("k_khb", 34, 30, 9, (164, -150, 0), SANDSTONE, raised=(14, 10, 2.5)))
        kc = column_proto("k_khcol", 0.9, 8, "bud", SANDSTONE, band=None)
        m.add(2, scatter(kc, "k_khcols", [(186 + 20 * i / 4, -150 + sy * 12, 0) for sy in (-1, 1) for i in range(5)]))
        m.add(2, box("k_khav", 30, 9, 0.35, (229, -150, 0), PAVE))
    else:
        m.add(3, scatter(ram, "k_rams", [(AX + sx * 11, -282 + 5.6 * j, 90 * -sx) for sx in (-1, 1) for j in range(26)]), "sphinxes")
        m.add(0, box("k_dromos", 16, 156, 0.35, (AX, -208, 0), PAVE))
    m.add(1, e_pylon("k_p2", 98, 30, 15, (AX, -126, 0), SANDSTONE), "pylons")
    st = standing_proto("k_rc2", 15, GRANITE_R)
    m.add(3, scatter(st, "k_c2s", [(AX - 14, -136, 0), (AX + 14, -136, 0)]), "statues")
    _hypostyle(m, "k_hh", -118.5, -66.5, 51.5)
    _karnak_inner(m, v)
    _karnak_south(m, v)
    _karnak_obelisks(m, v)
    # the temple of Ptah in the north
    m.add(1, e_pylon("k_ptp", 18, 9, 4, (-168, 22, 0), SANDSTONE, flags=0, relief=False))
    m.add(1, roofed_block("k_pt", 16, 22, 7, (-168, 38, 0), SANDSTONE))
    # priests' houses and the town
    if late:
        regions = [(140, 236, 150, 276), (-236, -140, 170, 276), (150, 236, -215, -180)]
    else:
        regions = [(140, 230, 130, 198), (-185, -120, 130, 198), (-110, 60, 222, 285), (80, 245, -285, -200), (-240, -200, -280, -150)]
    _karnak_houses(m, regions, seed=31 if late else 41, fill=0.7)
    m.add(3, palm_ring("k_palms", -98, -66, -280, -140, 12, 8) if not late else palm_ring("k_palms", -236, -140, 150, 276, 6, 8))
    return m


def karnak_quay():
    m = Model("karnak-quay")
    m.add(0, ground("q_g", 140, 160, SAND_DK), "ground")
    m.add(0, box("q_water", 92, 64, 0.5, (0, -48, 0), NILE))
    m.add(0, box("q_canal", 44, 20, 0.5, (0, -72, 0), NILE))
    p = [box("q_ww", 4, 66, 3.0, (-48, -47, 0), SANDSTONE_DK), box("q_we", 4, 66, 3.0, (48, -47, 0), SANDSTONE_DK),
         box("q_wn", 100, 4, 3.0, (0, -14, 0), SANDSTONE_DK),
         box("q_cw1", 26, 4, 3.0, (-35, -80, 0), SANDSTONE_DK), box("q_cw2", 26, 4, 3.0, (35, -80, 0), SANDSTONE_DK)]
    m.add(1, join(p, "q_walls"), "quay")
    # the tribune: a T-shaped landing stage with two ramps into the water
    t = [box("q_tri", 30, 16, 3.6, (0, -10, 0), SANDSTONE), box("q_tri2", 12, 10, 3.6, (0, -22, 0), SANDSTONE),
         wedge("q_rw", 6, 14, 3.6, (-12, -26, 0), SANDSTONE_LT, "S"), wedge("q_re", 6, 14, 3.6, (12, -26, 0), SANDSTONE_LT, "S"),
         box("q_flood", 30.2, 0.3, 1.2, (0, -18.1, 1.6), shade(SANDSTONE, -0.15))]
    m.add(1, join(t, "q_tribune"))
    m.add(2, join([obelisk_t("q_ob1", 7, (-9, -5, 3.6), SANDSTONE_LT), obelisk_t("q_ob2", 7, (9, -5, 3.6), SANDSTONE_LT)], "q_obelisks"), "monuments")
    m.add(0, box("q_way", 16, 70, 0.4, (0, 45, 0), PAVE))
    ram = sphinx_proto("q_ram", 1.0, "ram", SANDSTONE)
    m.add(2, scatter(ram, "q_rams", [(sx * 10, 14 + 5.6 * j, 90 * -sx) for sx in (-1, 1) for j in range(12)]))
    # storehouses on the quay
    m.add(2, vault_row("q_store_w", 4, 5, 26, 3.5, (-50, 30, 0), MUD), "stores")
    m.add(2, vault_row("q_store_e", 4, 5, 26, 3.5, (50, 30, 0), MUD))
    m.add(2, join([e_house("q_off", 14, 10, 5, (-48, 62, 0.3), HOUSE_COLS[1]), e_house("q_off2", 12, 10, 4.5, (48, 64, 0.3), HOUSE_COLS[3])], "q_offices"))
    boats = [nile_boat("q_userhat", 34, (-18, -46, 0.5), 90, sail=False, sacred=True),
             nile_boat("q_b1", 20, (24, -56, 0.5), 80), nile_boat("q_b2", 16, (32, -34, 0.5), 95, sail=False),
             nile_boat("q_b3", 18, (-36, -62, 0.5), 85)]
    m.add(3, join(boats, "q_boats"), "boats")
    m.add(3, palms("q_palms", [(-62, -20), (-60, 0), (62, -18), (60, 4), (-62, 70), (62, 74), (-30, 76), (30, 76)]))
    return m


# ---------------------------------------------------------------- Mut and Montu

def mut_precinct():
    m = Model("mut-precinct")
    m.add(0, ground("mu_g", 260, 330, SAND), "ground")
    m.add(0, brick_wall("mu_enc", [(-32, -160), (-125, -160), (-125, 160), (125, 160), (125, -160), (-8, -160)], 9, 6, MUD), "walls")
    # the Isheru: a crescent lake round the back of the temple
    cx, cy = -20.0, -20.0
    outer = [(cx + 66 * math.cos(math.pi * i / 24 - math.pi * 0.08), cy + 70 * math.sin(math.pi * i / 24 - math.pi * 0.08)) for i in range(25)]
    outer = [(cx + 66, cy - 60)] + [(cx + 66 * math.cos(-math.pi * 0.08 + (math.pi * 1.16) * i / 24), cy + 70 * math.sin(-math.pi * 0.08 + (math.pi * 1.16) * i / 24)) for i in range(25)] + [(cx - 66, cy - 60)]
    inner = [(cx + 42, cy - 60)] + [(cx + 42 * math.cos(-math.pi * 0.08 + (math.pi * 1.16) * i / 24), cy + 48 * math.sin(-math.pi * 0.08 + (math.pi * 1.16) * i / 24)) for i in range(25)] + [(cx - 42, cy - 60)]
    m.add(0, ring_extrude("mu_lake", outer, inner, 0.55, (0, 0, 0), NILE, closed=False), "lake")
    m.add(0, ring_extrude("mu_rim", [(cx + (x - cx) * 1.06, cy + (y - cy) * 1.05) for x, y in outer], outer, 0.9, (0, 0, 0), SANDSTONE_DK, closed=False))
    m.add(0, ring_extrude("mu_rim2", inner, [(cx + (x - cx) * 0.93, cy + (y - cy) * 0.92) for x, y in inner], 0.9, (0, 0, 0), SANDSTONE_DK, closed=False))
    # the temple of Mut
    m.add(1, e_pylon("mu_p1", 54, 18, 9, (cx, -100, 0), SANDSTONE), "temple")
    m.add(1, court_walls("mu_c1", cx - 24, cx + 24, -95, -62, 7, 1.6, SANDSTONE_DK, gaps=("S", "N")))
    m.add(1, e_pylon("mu_p2", 44, 14, 7, (cx, -58, 0), SANDSTONE, flags=0))
    m.add(1, roofed_block("mu_hall", 34, 50, 9, (cx, -28, 0), SANDSTONE, raised=(14, 30, 2.5)))
    cc = column_proto("mu_col", 0.85, 7.5, "bud", SANDSTONE, band=None)
    m.add(2, scatter(cc, "mu_cols", [(cx + sx * 16, -90 + 26 * j / 4, 0) for sx in (-1, 1) for j in range(5)]), "courts")
    # rows of Sekhmet statues
    sk = seated_proto("mu_sek", 2.2, GRANITE_B, crown=None, base=True)
    sp = [(cx + sx * (21 - k * 2.6), -92 + 3.2 * j, 0) for sx in (-1, 1) for k in range(2) for j in range(10)]
    sp += [(cx - 60 + 4 * i, -128, 0) for i in range(12)] + [(cx + 16 + 4 * i, -128, 0) for i in range(12)]
    m.add(3, scatter(sk, "mu_sekhmet", sp), "statues")
    # the temple of Khonsupakhered (east) and a temple of Ramesses III (west of the lake)
    m.add(1, e_pylon("mu_kp", 26, 11, 5, (72, -60, 0), SANDSTONE_LT, flags=0))
    m.add(1, roofed_block("mu_k", 22, 36, 7, (72, -34, 0), SANDSTONE_LT))
    m.add(1, e_pylon("mu_rp", 24, 11, 5, (-104, 0, 0), SANDSTONE, flags=0, relief=False))
    m.add(1, roofed_block("mu_r", 18, 30, 7, (-104, 24, 0), SANDSTONE))
    # gate and avenue
    m.add(1, e_pylon("mu_gate", 22, 14, 8, (cx, -160, 0), SANDSTONE_LT, flags=0, gate=8))
    m.add(0, box("mu_way", 12, 50, 0.35, (cx, -135, 0), PAVE))
    ram = sphinx_proto("mu_ram", 1.0, "ram", SANDSTONE)
    m.add(3, scatter(ram, "mu_rams", [(cx + sx * 9, -152 + 5.6 * j, 90 * -sx) for sx in (-1, 1) for j in range(4)]))
    m.add(3, house_field("mu_h", 30, 118, 70, 150, 51, (6, 10), (4, 6.5), 2.5, 0.85), "houses")
    m.add(3, house_field("mu_h2", -118, -50, 70, 150, 52, (6, 10), (4, 6.5), 2.5, 0.8))
    m.add(3, palm_ring("mu_palms", 40, 115, -150, -90, 12, 9))
    return m


def montu_precinct():
    m = Model("montu-precinct")
    m.add(0, ground("mo_g", 160, 170, SAND), "ground")
    m.add(0, brick_wall("mo_enc", [(-8, -80), (-75, -80), (-75, 80), (75, 80), (75, -80), (8, -80)], 8, 5, MUD), "walls")
    g = [box("mo_g1", 16, 10, 17, (0, -80, 0), SANDSTONE_LT), frustum("mo_g2", 16, 10, 17.4, 11.4, 1.2, (0, -80, 17), shade(SANDSTONE_LT, 0.06)),
         box("mo_g3", 5, 10.4, 10, (0, -80, 0), DARK), box("mo_g4", 16.2, 10.2, 0.6, (0, -80, 13), PAINT_BLUE)]
    m.add(1, join(g, "mo_gate"), "gate")
    m.add(0, box("mo_way", 10, 40, 0.35, (0, -58, 0), PAVE))
    sph = sphinx_proto("mo_sph", 0.9, "human", SANDSTONE)
    m.add(3, scatter(sph, "mo_sphs", [(sx * 8, -72 + 6 * j, 90 * -sx) for sx in (-1, 1) for j in range(5)]), "sphinxes")
    pc = column_proto("mo_pc", 1.0, 10, "bud", SANDSTONE)
    m.add(2, scatter(pc, "mo_portico", [(-15 + 30 * i / 5, yy, 0) for i in range(6) for yy in (-40, -34)]), "portico")
    m.add(2, box("mo_porroof", 34, 10, 0.8, (0, -37, 10.3), SANDSTONE))
    m.add(1, e_pylon("mo_p", 44, 16, 7, (0, -27, 0), SANDSTONE), "temple")
    m.add(1, roofed_block("mo_t", 34, 52, 9, (0, 6, 0), SANDSTONE, raised=(12, 28, 2.4)))
    m.add(1, roofed_block("mo_maat", 14, 20, 6, (-52, -10, 0), SANDSTONE_LT, door="E"))
    m.add(0, sacred_lake("mo_lake", 26, 36, (48, 44, 0), steps_n=3), "lake")
    m.add(3, house_field("mo_h", -70, -30, 30, 74, 61, (5, 9), (3.5, 6), 2.2, 0.8), "houses")
    m.add(3, palms("mo_palms", [(30, -60), (40, -66), (55, -58), (-40, -66), (-58, -56), (62, 10), (66, 20)]))
    return m


def town_of_thebes():
    m = Model("town-of-thebes")
    m.add(0, ground("t_g", 260, 220, SAND), "ground")
    m.add(0, frustum("t_mound", 250, 210, 226, 186, 3.0, (0, 0, 0.3), shade(SAND, -0.08)), "mound")
    z = 3.3
    p = []
    lanes = [(-120, 120, -4, 4), (-6, 6, -100, 100), (-120, 120, 52, 58), (-120, 120, -62, -56), (56, 62, -100, 100), (-66, -60, -100, 100)]
    hs = house_field("t_h", -112, 112, -92, 92, 71, (6, 11), (4.5, 8.5), 2.2, 0.92, z, avoid=lanes + [(20, 50, 15, 45), (-50, -20, -45, -15), (-8, 8, 62, 78)])
    m.add(1, hs, "houses")
    # granary courts with domed silos and a little shrine
    g = []
    for k, (gx, gy) in enumerate(((35, 30), (-35, -30))):
        g.append(box(f"t_gc{k}", 28, 28, 2.4, (gx, gy, z), MUD_LT))
        g.append(box(f"t_gci{k}", 25, 25, 0.2, (gx, gy, z + 2.4), shade(MUD_LT, -0.12)))
        for i in range(3):
            for j in range(3):
                g.append(cylinder(f"t_si{k}{i}{j}", 3.0, 4.0, (gx - 8 + 8 * i, gy - 8 + 8 * j, z), MUD, verts=12))
                g.append(cylinder(f"t_sd{k}{i}{j}", 3.0, 2.2, (gx - 8 + 8 * i, gy - 8 + 8 * j, z + 4.0), MUD, verts=12, r_top=0.6))
    m.add(2, join(g, "t_granaries"), "granaries")
    m.add(2, kiosk("t_shrine", 8, 10, 3.5, (0, 70, z), LIME, 3, 4, 0.6), "shrine")
    m.add(3, palm_ring("t_palms", -125, 125, 95, 108, 10, 12))
    m.add(3, palm_ring("t_palms2", -125, 125, -108, -95, 10, 13))
    return m


# ---------------------------------------------------------------- the processional way

def avenue_of_sphinxes(variant="sphinx"):
    m = Model("avenue-of-sphinxes")
    m.add(0, ground("av_g", 32, 300, SAND), "ground")
    if variant == "way":
        m.add(0, frustum("av_bank", 16, 300, 13, 300, 0.8, (0, 0, 0.3), MUD_LT), "road")
        m.add(1, join([box("av_pw", 0.7, 300, 1.2, (-7.2, 0, 0.3), MUD), box("av_pe", 0.7, 300, 1.2, (7.2, 0, 0.3), MUD)], "av_parapets"), "walls")
        m.add(2, palms("av_palms", [(sx * 11.5, -145 + 13 * j) for sx in (-1, 1) for j in range(23)], 2.0), "trees")
        sh = kiosk("av_shr", 5, 6, 2.5, (12.5, 40, 0.3), LIME, 3, 3, 0.5)
        m.add(2, sh)
        return m
    m.add(0, box("av_pave", 9, 300, 0.6, (0, 0, 0.3), PAVE), "road")
    m.add(0, join([box("av_edge_w", 0.8, 300, 0.75, (-4.9, 0, 0.3), SANDSTONE_DK), box("av_edge_e", 0.8, 300, 0.75, (4.9, 0, 0.3), SANDSTONE_DK)], "av_edges"))
    sph = sphinx_proto("av_sph", 1.0, "human", SANDSTONE)
    sp = [(sx * 8.2, -147 + 4.9 * j, 90 * -sx, 0.3) for sx in (-1, 1) for j in range(61)]
    m.add(1, scatter(sph, "av_sphinxes", sp), "sphinxes")
    m.add(2, join([box("av_ww", 0.9, 300, 1.4, (-13, 0, 0.3), MUD_LT), box("av_we", 0.9, 300, 1.4, (13, 0, 0.3), MUD_LT)], "av_walls"), "walls")
    m.add(2, join([tree(f"av_t{i}", 1.4, (sx * 11.3, -140 + 14 * j, 0.3), "#7C9460", TIMBER, "round") for i, (sx, j) in enumerate([(sx, j) for sx in (-1, 1) for j in range(21)])], "av_trees"))
    return m


def opet_shrine():
    m = Model("opet-shrine")
    m.add(0, ground("op_g", 24, 34, SAND), "ground")
    m.add(0, box("op_way", 6, 34, 0.35, (0, 0, 0), PAVE))
    p = [box("op_pd", 12, 18, 1.8, (0, 0, 0.3), shade(SANDSTONE_LT, -0.05)),
         frustum("op_pc", 12, 18, 12.5, 18.5, 0.3, (0, 0, 1.8), shade(SANDSTONE_LT, 0.05)),
         wedge("op_r1", 4.2, 5, 1.8, (0, -11.5, 0.3), shade(SANDSTONE_LT, -0.05), "S"),
         wedge("op_r2", 4.2, 5, 1.8, (0, 11.5, 0.3), shade(SANDSTONE_LT, -0.05), "N")]
    m.add(1, join(p, "op_podium"), "podium")
    # square pillars with Hathor-style capitals and painted bands, an architrave and cavetto roof
    pil = join([box("op_pp", 0.9, 0.9, 4.0, (0, 0, 0), SANDSTONE_LT), box("op_pb", 0.95, 0.95, 0.25, (0, 0, 3.0), PAINT_BLUE),
                box("op_ph", 1.05, 1.05, 0.7, (0, 0, 3.3), shade(SANDSTONE_LT, 0.08)), box("op_pf", 0.6, 1.15, 0.5, (0, 0, 3.4), PAINT_YEL),
                box("op_pk", 1.2, 1.2, 0.6, (0, 0, 4.0), shade(SANDSTONE_LT, 0.06))], "op_pil")
    sp = []
    for i in range(4):
        for j in range(5):
            if 0 < i < 3 and 0 < j < 4:
                continue
            sp.append((-5.2 + 10.4 * i / 3, -8.2 + 16.4 * j / 4, 0, 2.1))
    m.add(2, scatter(pil, "op_pils", sp), "pillars")
    rf = [box("op_rf", 11.8, 17.8, 0.6, (0, 0, 6.7), SANDSTONE_LT), frustum("op_rc", 11.8, 17.8, 12.8, 18.8, 0.6, (0, 0, 7.3), shade(SANDSTONE_LT, 0.06)),
          box("op_bandf", 11.9, 17.9, 0.2, (0, 0, 6.5), PAINT_RED)]
    m.add(2, join(rf, "op_roof"))
    m.add(2, barque_on_stand("op_barque", 5.0, (0, 0, 2.1)), "barque")
    stands = [join([cylinder(f"op_os{i}", 0.35, 1.0, (x, y, 0.3), SANDSTONE_DK, verts=8), cylinder(f"op_ot{i}", 0.6, 0.15, (x, y, 1.3), GOLD, verts=8)], f"op_offer{i}")
              for i, (x, y) in enumerate([(-2.5, -15.5), (2.5, -15.5), (-2.5, 15.5), (2.5, 15.5)])]
    m.add(3, join(stands, "op_offerings"), "offerings")
    sph = sphinx_proto("op_sph", 0.6, "ram", SANDSTONE)
    m.add(3, scatter(sph, "op_rams", [(sx * 4.2, yy, 90 * -sx) for sx in (-1, 1) for yy in (-15.5, -12.5, 12.5, 15.5)]))
    st = seated_proto("op_st", 2.6, GRANITE_R)
    m.add(3, scatter(st, "op_statues", [(-7.5, -14, 0), (7.5, -14, 0), (-7.5, 14, 180), (7.5, 14, 180)]))
    m.add(3, palms("op_palms", [(-10, -8), (10, -8), (-10, 8), (10, 8), (-10, 0), (10, 0), (-10.5, -3.5), (10.5, 3.5)], 1.6), "trees")
    return m


# ---------------------------------------------------------------- Luxor

def _luxor_front(m, roman=False):
    """Ramesses II's pylon, obelisks, colossi and court, turned slightly toward Karnak."""
    parts = []
    parts.append(e_pylon("lx_p1", 65, 24, 14, (0, -118, 0), SANDSTONE))
    parts.append(court_walls("lx_c1", -28.5, 28.5, -111, -60, 9, 2.0, SANDSTONE_DK, gaps=("S", "N")))
    col = column_proto("lx_cc", 0.95, 9.5, "bud", SANDSTONE)
    parts.append(peristyle_cols(col, "lx_c1cols", -24, 24, -106, -66, 11, 9, rows=2, gap=4.0))
    parts.append(box("lx_c1rf_w", 9, 44, 0.8, (-24, -86, 9.8), SANDSTONE))
    parts.append(box("lx_c1rf_e", 9, 44, 0.8, (24, -86, 9.8), SANDSTONE))
    parts.append(kiosk("lx_triple", 12, 10, 5, (-10, -95, 0), SANDSTONE_LT, 4, 3, 0.8, ramps=False))
    stc = standing_proto("lx_cst", 7.5, GRANITE_R)
    parts.append(scatter(stc, "lx_c1stat", [(-16 + 8 * i, -68.5, 0) for i in range(5)]))
    o = join(parts, "lx_front")
    o = pivot(o, -6, 0, -60)
    m.add(1, o, "pylon")
    fr = []
    s = seated_proto("lx_seat", 15.5, GRANITE_B)
    fr.append(scatter(s, "lx_seated", [(-9.5, -132, 0), (9.5, -132, 0)]))
    st = standing_proto("lx_stand", 11, GRANITE_R)
    fr.append(scatter(st, "lx_standing", [(-21, -128, 0), (-28, -128, 0), (21, -128, 0), (28, -128, 0)]))
    fr.append(obelisk_t("lx_obw", 22.8, (13.5, -140.5, 0)))
    fr.append(obelisk_t("lx_obe", 25.0, (-13.5, -140.5, 0)))
    o = join(fr, "lx_colossi")
    o = pivot(o, -6, 0, -60)
    m.add(3, o, "colossi")


def _luxor_core(m):
    """Amenhotep III's colonnade, sun court, hypostyle and sanctuaries."""
    big = column_proto("lx_big", 1.6, 19.0, "open", SANDSTONE)
    m.add(2, scatter(big, "lx_colonnade", [(sx * 5.2, -56 + 48 * j / 6, 0) for sx in (-1, 1) for j in range(7)]), "colonnade")
    m.add(2, join([box("lx_arch_w", 2.6, 52, 1.6, (-5.2, -32, 19.0), SANDSTONE), box("lx_arch_e", 2.6, 52, 1.6, (5.2, -32, 19.0), SANDSTONE)], "lx_architraves"))
    m.add(1, join([box("lx_cw_w", 2.2, 52, 13, (-12, -34, 0), SANDSTONE_DK), box("lx_cw_e", 2.2, 52, 13, (12, -34, 0), SANDSTONE_DK),
                   quad("lx_opet_w", [(-10.85, -58, 2), (-10.85, -10, 2), (-10.85, -10, 11), (-10.85, -58, 11)], shade(SANDSTONE_DK, -0.12)),
                   quad("lx_opet_e", [(10.85, -10, 2), (10.85, -58, 2), (10.85, -58, 11), (10.85, -10, 11)], shade(SANDSTONE_DK, -0.12))], "lx_colwalls"))
    sw = [court_walls("lx_sun", -27, 27, -8, 48, 11, 2.0, SANDSTONE_DK, gaps=("N", "S")),
          box("lx_sun_sw", 15, 2.0, 11, (-19.5, -8, 0), SANDSTONE_DK), box("lx_sun_se", 15, 2.0, 11, (19.5, -8, 0), SANDSTONE_DK)]
    m.add(1, join(sw, "lx_sunwalls"), "temple")
    cc = column_proto("lx_sc", 1.05, 10.5, "bud", SANDSTONE)
    m.add(2, peristyle_cols(cc, "lx_suncols", -23, 23, -4, 46, 12, 12, rows=2, gap=4.2, sides="SEW"))
    m.add(2, join([box("lx_srf_w", 10, 52, 0.8, (-22, 20, 10.8), SANDSTONE), box("lx_srf_e", 10, 52, 0.8, (22, 20, 10.8), SANDSTONE),
                   box("lx_srf_s", 54, 10, 0.8, (0, 0.5, 10.8), SANDSTONE)], "lx_sunroof"))
    m.add(1, roofed_block("lx_hyp", 54, 18, 13, (0, 57, 0), SANDSTONE, raised=(18, 18, 2.2)))
    m.add(1, roofed_block("lx_inner", 42, 74, 10, (0, 103, 0), SANDSTONE, raised=(14, 30, 2.0)))
    m.add(1, box("lx_hypdoor", 6, 0.5, 8, (0, 47.8, 0), DARK))


def luxor_temple(variant="1250"):
    m = Model("luxor-temple")
    m.add(0, ground("lx_g", 120, 290, SAND), "ground")
    if variant == "1470":
        m.add(0, brick_wall("lx_enc", [(-40, -60), (40, -60), (40, 140), (-40, 140)], 7, 4, MUD, closed=True), "walls")
        m.add(1, e_pylon("lx_tp", 40, 13, 7, (0, -10, 0), SANDSTONE, flags=2), "temple")
        m.add(1, court_walls("lx_tc", -16, 16, -6, 30, 7, 1.6, SANDSTONE_DK, gaps=("S",)))
        pc = column_proto("lx_tcol", 0.8, 7, "bud", SANDSTONE, band=None)
        m.add(2, peristyle_cols(pc, "lx_tcols", -12, 12, -2, 26, 6, 6, sides="EW"))
        m.add(1, roofed_block("lx_tt", 30, 60, 8, (0, 64, 0), SANDSTONE, raised=(10, 24, 1.8)))
        m.add(2, kiosk("lx_hbs", 16, 12, 5, (0, -100, 0), SANDSTONE_LT, 4, 3, 0.8, naos=False), "chapel")
        m.add(2, barque_on_stand("lx_hbarque", 5.0, (0, -100, 0.8)))
        m.add(0, box("lx_way", 12, 80, 0.35, (0, -100, 0), PAVE))
        m.add(3, house_field("lx_h", -58, -22, -140, 140, 81, (6, 10), (4, 6.5), 2.2, 0.85), "houses")
        m.add(3, house_field("lx_h2", 44, 58, -140, 140, 82, (6, 10), (4, 6), 2.2, 0.7))
        m.add(3, palm_ring("lx_palms", 22, 42, -140, -70, 10, 3))
        return m
    _luxor_front(m)
    _luxor_core(m)
    if variant == "roman":
        pts = [(-12, -140), (-55, -140), (-55, 140), (55, 140), (55, -140), (12, -140)]
        m.add(0, brick_wall("lx_camp", pts, 9, 3.5, "#C2A786", batter=0.1), "walls")
        tw = []
        for i, (x, y) in enumerate([(-55, -140), (55, -140), (55, 140), (-55, 140)] + [(sx * 55, -140 + 280 * j / 6) for sx in (-1, 1) for j in range(1, 6)] + [(sx * 14, -140) for sx in (-1, 1)]):
            tw.append(cylinder(f"lx_tw{i}", 4.2, 11, (x, y, 0), "#B89C7A", verts=12))
        m.add(1, join(tw, "lx_towers"))
        tc = column_proto("lx_tet", 0.7, 9, "bud", "#E6DCC8", band=None)
        m.add(2, scatter(tc, "lx_tetra", [(40, -110, 0), (52, -110, 0), (40, -98, 0), (52, -98, 0)]), "camp")
        bar = [vault_row("lx_bar_w", 3, 6, 60, 3.5, (-44, 40, 0), "#C9AE88"), vault_row("lx_bar_e", 3, 6, 60, 3.5, (44, 40, 0), "#C9AE88"),
               house_field("lx_rh", -54, -34, -60, 10, 91, (6, 9), (4, 6), 2.0, 0.85), house_field("lx_rh2", 34, 54, -80, 10, 92, (6, 9), (4, 6), 2.0, 0.85)]
        m.add(3, join([b for b in bar if b is not None], "lx_barracks"), "barracks")
        return m
    m.add(3, house_field("lx_h", -58, -36, -60, 140, 83, (6, 10), (4, 7), 2.2, 0.85), "houses")
    m.add(3, palm_ring("lx_palms", 36, 56, -60, 140, 14, 4))
    return m


# ---------------------------------------------------------------- Deir el-Bahari

def _mentuhotep(m, stage=1):
    X = -70.0
    p = [box("mh_plat", 62, 56, 5.0, (X, -10, 0), LIME), wedge("mh_ramp", 10, 30, 5.0, (X, -53, 0), shade(LIME, -0.04), "S")]
    pil = join([box("mh_pil", 1.5, 1.5, 5.0, (0, 0, 0), LIME), box("mh_pilk", 1.8, 1.8, 0.3, (0, 0, 4.7), shade(LIME, 0.05))], "mh_pilp")
    p.append(scatter(pil, "mh_pils", [(X - 29 + 58 * i / 19, yy, 0) for i in range(20) for yy in (-39.5, -42.5) if abs(-29 + 58 * i / 19) > 6]))
    p.append(box("mh_porr", 60, 6, 0.7, (X, -41, 5.0), LIME))
    amb = box("mh_ap", 1.2, 1.2, 4.5, (0, 0, 0), LIME)
    sp = [(X - 26 + 52 * i / 11, yy, 5.0) for i in range(12) for yy in (-34, 14)] + [(xx, -34 + 48 * j / 8, 5.0) for xx in (X - 26, X + 26) for j in range(1, 8)]
    sp += [(X - 22 + 44 * i / 9, yy, 5.0) for i in range(10) for yy in (-30, 10)] + [(xx, -30 + 40 * j / 7, 5.0) for xx in (X - 22, X + 22) for j in range(1, 7)]
    p.append(scatter(amb, "mh_amb", sp))
    p.append(box("mh_ambr", 56, 52, 0.7, (X, -10, 9.5), LIME))
    p.append(box("mh_core", 24, 24, 9, (X, -10, 10.2), shade(LIME, -0.04)))
    p.append(frustum("mh_corec", 24, 24, 25, 25, 0.8, (X, -10, 19.2), shade(LIME, 0.04)))
    p.append(box("mh_rear", 40, 46, 6.0, (X, 44, 0), LIME))
    p.append(box("mh_reard", 6, 1, 4, (X, 20.6, 0), DARK))
    m.add(stage, join(p, "mh_temple"), "mentuhotep")
    trees = [tree(f"mh_tr{i}", 2.4, (X - 25 + 10 * (i % 6), -110 + 12 * (i // 6), 0.3), "#6E8A55", TIMBER, "round") for i in range(18) if (i % 6) not in (2, 3)]
    trees += [box(f"mh_pit{i}", 4, 4, 0.35, (X - 25 + 10 * (i % 6), -110 + 12 * (i // 6), 0), shade(MUD, -0.1)) for i in range(18) if (i % 6) not in (2, 3)]
    m.add(3, join(trees, "mh_grove"), "garden")
    osr = osiride_proto("mh_os", 4.5, 1.2, LIME, "#EFE6D4")
    m.add(3, scatter(osr, "mh_causeway_statues", [(X + sx * 8, -136 + 8 * j, 90 * -sx) for sx in (-1, 1) for j in range(4)]))


def _cliff(m):
    m.add(0, rock_mass("db_cliff", -120, 120, 70, 140, 34, 58, seed=3, n=9), "cliff")
    m.add(0, rock_mass("db_cliff2", -120, -104, -20, 120, 14, 30, seed=4, n=3))
    m.add(0, rock_mass("db_cliff3", 104, 120, 0, 120, 16, 34, seed=6, n=3))


def deir_el_bahari(variant="1470"):
    m = Model("deir-el-bahari")
    m.add(0, ground("db_g", 240, 280, SAND), "ground")
    _cliff(m)
    _mentuhotep(m)
    m.add(0, box("db_mcause", 12, 40, 0.35, (-70, -120, 0), PAVE))
    m.add(0, boulders("db_scree", -118, 118, 60, 72, 40, 61, 2.4, ROCK))
    if variant == "1950":
        doors = [box(f"db_mkt{i}", 2.2, 0.6, 3.0, (-100 + 22 * i, 69.6, 0), DARK) for i in range(10)]
        m.add(2, join(doors, "db_mktombs"), "tombs")
        return m
    X = 40.0
    m.add(0, box("db_cause", 14, 16, 0.4, (X, -132, 0), PAVE))
    m.add(0, box("db_court", 10, 40, 0.35, (X, -104, 0), PAVE))
    g = [box(f"db_pool{s}", 10, 6, 0.4, (X + s * 22, -112, 0.3), NILE) for s in (-1, 1)]
    g += [tree(f"db_inc{i}", 1.5, (X - 40 + 10 * (i % 9), -92 - 9 * (i // 9), 0.3), "#7E9460", TIMBER, "round") for i in range(18) if (i % 9) != 4]
    m.add(3, join(g, "db_garden"), "garden")
    t = [box("db_t1", 124, 62, 7.0, (X, -24, 0), LIME), box("db_t2", 84, 56, 7.0, (X, 34, 7.0), LIME),
         wedge("db_r1", 10, 30, 7.0, (X, -69, 0), shade(LIME, -0.05), "S"), wedge("db_r2", 9, 26, 7.0, (X, -2, 7.0), shade(LIME, -0.05), "S")]
    m.add(1, join(t, "db_terraces"), "terraces")
    pil = box("db_pil", 1.4, 1.4, 6.0, (0, 0, 0), "#EFE7D6")
    sp = []
    for sx in (-1, 1):
        for i in range(11):
            xx = X + sx * (8 + 36 * i / 10)
            sp += [(xx, -61, 0), (xx, -57.5, 0), (xx, 0, 7.0), (xx, 3.5, 7.0)]
    m.add(2, scatter(pil, "db_pils", sp), "colonnades")
    m.add(2, join([box(f"db_por{k}{s}", 38, 6, 0.8, (X + s * 26, yy, zz), "#EFE7D6") for k, (yy, zz) in enumerate(((-59.3, 6.0), (1.7, 13.0))) for s in (-1, 1)], "db_porticoes"))
    m.add(1, roofed_block("db_hathor", 12, 20, 6, (X - 54, -14, 7.0), "#EFE7D6", door="S"))
    m.add(1, roofed_block("db_anubis", 12, 18, 6, (X + 54, -14, 7.0), "#EFE7D6", door="S"))
    osr = osiride_proto("db_os", 6.5, 1.6, "#EFE7D6", "#F3ECDD")
    m.add(2, scatter(osr, "db_osirides", [(X - 34 + 68 * i / 23, 9.0, 0, 14.0) for i in range(24) if abs(-34 + 68 * i / 23) > 3]))
    m.add(1, join([box("db_cwall_w", 30, 1.6, 7, (X - 21, 13, 14.0), "#EFE7D6"), box("db_cwall_e", 30, 1.6, 7, (X + 21, 13, 14.0), "#EFE7D6"),
                   box("db_gate", 6, 1.8, 7.5, (X, 13, 14.0), GRANITE_R)], "db_upperwall"))
    pc = column_proto("db_pc", 0.6, 6, "bud", "#EFE7D6", band=None)
    m.add(2, peristyle_cols(pc, "db_peri", X - 26, X + 26, 20, 56, 10, 6, sides="NSEW", z=14.0))
    m.add(2, box("db_sanct", 6, 2, 6, (X, 69.5, 14.0), DARK))
    st = osiride_proto("db_colos", 8, 2.0, "#EFE7D6", "#F3ECDD")
    m.add(3, scatter(st, "db_queenstat", [(X - 6, -64, 0), (X + 6, -64, 0)]), "statues")
    sph = sphinx_proto("db_sph", 0.9, "human", SANDSTONE_LT)
    m.add(3, scatter(sph, "db_sphinxes", [(X + sx * 9, -135 + 6 * j, 90 * -sx) for sx in (-1, 1) for j in range(4)]))
    return m


# ---------------------------------------------------------------- Valley of the Kings, nobles' tombs

def valley_of_the_kings():
    m = Model("valley-of-the-kings")
    m.add(0, ground("vk_g", 120, 200, ROCK_LT), "ground")
    m.add(0, box("vk_floor", 30, 200, 0.4, (0, 0, 0), "#DCC7A0"))
    m.add(0, box("vk_path", 3, 196, 0.5, (0, 0, 0), shade(PAVE, 0.03)))
    m.add(1, rock_mass("vk_w1", -60, -18, -100, -20, 18, 34, seed=11, n=12), "rocks")
    m.add(1, rock_mass("vk_w2", -60, -22, -10, 100, 22, 40, seed=12, n=12))
    m.add(1, rock_mass("vk_e1", 18, 60, -100, -5, 16, 30, seed=13, n=12))
    m.add(1, rock_mass("vk_e2", 22, 60, 5, 100, 20, 36, seed=14, n=12))
    m.add(1, rock_mass("vk_w0", -60, -30, -20, -8, 10, 18, seed=15, n=4))
    m.add(1, rock_mass("vk_e0", 30, 60, -8, 6, 10, 16, seed=16, n=4))
    tombs = []
    spots = [(-18.5, -70, "E"), (-21, -35, "E"), (-21.5, 10, "E"), (-22, 50, "E"), (-21, 85, "E"),
             (18.5, -80, "W"), (18, -45, "W"), (22, -2, "W"), (22.5, 35, "W"), (22, 70, "W")]
    for i, (x, y, f) in enumerate(spots):
        s = 1 if f == "E" else -1
        tombs.append(box(f"vk_cut{i}", 6, 5, 4.5, (x + s * 1.0, y, 0), shade(ROCK, -0.12)))
        tombs.append(box(f"vk_lint{i}", 0.6, 4.0, 0.6, (x + s * 4.05, y, 3.4), ROCK_LT))
        tombs.append(box(f"vk_door{i}", 0.4, 2.6, 3.4, (x + s * 3.9, y, 0), DARK))
        tombs.append(box(f"vk_stair{i}", 4.0, 2.6, 0.45, (x + s * 6.0, y, 0), shade(ROCK_LT, -0.3)))
        for k in range(3):
            tombs.append(cylinder(f"vk_spoil{i}{k}", 3.2 - k * 0.7, 2.0 - k * 0.4, (x + s * (9.5 + k * 2.5), y + 5 - k * 3, 0), "#E6D8BC", verts=10, r_top=0.4))
        tombs.append(box(f"vk_bask{i}", 0.8, 0.8, 0.6, (x + s * 7.5, y - 2.2, 0.4), TIMBER))
    m.add(2, join(tombs, "vk_tombs"), "tombs")
    m.add(1, boulders("vk_bw", -17, -12, -98, 98, 55, 41, 1.6, ROCK))
    m.add(1, boulders("vk_be", 12, 17, -98, 98, 55, 42, 1.6, ROCK))
    huts = []
    for i, (x, y) in enumerate([(-5, -92), (-1, -92), (3, -92), (8, -88), (-8, -86), (-4, -84), (4, -83)]):
        huts += [box(f"vk_hut{i}", 3, 3, 1.8, (x, y, 0.4), "#CDB792"), box(f"vk_hr{i}", 3.2, 3.2, 0.2, (x, y, 2.2), shade("#CDB792", -0.12))]
    huts += [box("vk_post", 4, 4, 3.2, (6, -96, 0.4), MUD_LT), box("vk_postr", 4.4, 4.4, 0.4, (6, -96, 3.6), shade(MUD_LT, -0.1))]
    huts += [cylinder(f"vk_jar{i}", 0.4, 0.9, (-10 + 1.0 * i, -90, 0.4), "#B07A55", verts=8) for i in range(5)]
    m.add(3, join(huts, "vk_huts"), "huts")
    return m


def nobles_tombs():
    m = Model("nobles-tombs")
    m.add(0, ground("nt_g", 200, 120, ROCK_LT), "ground")
    tiers = [(96, 0.0), (68, 6.0), (40, 12.0)]
    hill = [frustum(f"nt_tier{k}", 200 - 8 * k, d, 196 - 8 * k, d - 2.0, 6.0, (0, 60 - d / 2 + 1.0, z), shade(ROCK, -0.03 * k)) for k, (d, z) in enumerate(tiers)]
    m.add(0, join(hill, "nt_hill"), "hill")
    m.add(0, rock_mass("nt_top", -90, 90, 36, 60, 22, 30, seed=21, n=9))
    m.add(0, join([box("nt_path1", 4, 30, 0.3, (-60, -44, 0), PAVE), box("nt_path2", 4, 30, 0.3, (30, -44, 0), PAVE)], "nt_paths"))
    rnd = random.Random(5)
    t, pyr = [], []
    for k, (d, z) in enumerate(tiers):
        yface = 60 - d
        n = 14 - k
        for i in range(n):
            x = -88 + 176 * (i + 0.5) / n + rnd.uniform(-3, 3)
            t.append(box(f"nt_court{k}{i}", 9, 6, 0.25, (x, yface - 3.2, z), shade(SAND, -0.1)))
            t.append(box(f"nt_cwa{k}{i}", 0.6, 6, 1.4, (x - 4.5, yface - 3.2, z), MUD_LT))
            t.append(box(f"nt_cwb{k}{i}", 0.6, 6, 1.4, (x + 4.5, yface - 3.2, z), MUD_LT))
            t.append(box(f"nt_fac{k}{i}", 7, 0.3, 4.5, (x, yface - 0.1, z), shade(ROCK_LT, 0.04)))
            t.append(box(f"nt_door{k}{i}", 1.8, 0.4, 2.8, (x, yface - 0.3, z), DARK))
            t.append(box(f"nt_cone{k}{i}", 6.0, 0.3, 0.5, (x, yface - 0.3, z + 3.6), "#B0644A"))
            if rnd.random() < 0.6:
                pyr.append(frustum(f"nt_pyr{k}{i}", 4.2, 4.2, 0.2, 0.2, 5.0, (x, yface + 3.5, z + 6.0), MUD_LT))
                pyr.append(box(f"nt_pyrn{k}{i}", 1.0, 0.3, 1.2, (x, yface + 1.35, z + 6.6), DARK))
    for i in range(9):
        x = -88 + 176 * (i + 0.5) / 9
        t.append(box(f"nt_lc{i}", 10, 8, 1.4, (x, -50, 0), MUD_LT))
        t.append(box(f"nt_ld{i}", 1.6, 0.4, 1.2, (x, -54.1, 0), DARK))
        pyr.append(frustum(f"nt_lp{i}", 4.6, 4.6, 0.2, 0.2, 5.4, (x, -48, 1.4), MUD_LT))
    m.add(1, join(t, "nt_tombs"), "tombs")
    m.add(2, join(pyr, "nt_pyramids"), "pyramids")
    m.add(3, palms("nt_palms", [(-95, -56), (-80, -58), (95, -56), (82, -57), (0, -57)], 1.8), "trees")
    return m


# ---------------------------------------------------------------- the Ramesseum

def _fallen_colossus(name, loc):
    """The toppled seated colossus: the throne and legs in place, the torso and head lying broken beside them."""
    x, y, z = loc
    stump = [box(name + "b", 10, 14, 2.4, (x, y, 0), shade(GRANITE_R, -0.1)), box(name + "th", 8.5, 8, 5.0, (x, y + 2.5, 2.4), shade(GRANITE_R, -0.04)),
             box(name + "sh", 6, 2.6, 4.0, (x, y - 2.6, 2.4), GRANITE_R)]
    torso = seated_proto(name + "t", 19.0, GRANITE_R, crown=None, base=False)
    lying = clone(torso, name + "ly", x - 13, y - 4, 7.4, 25, tilt_x=-90)
    drop(torso)
    blocks = [box(f"{name}rb{i}", 2.5 + i % 2, 2 + (i % 3), 1.5 + (i % 2), (x - 6 + 3.5 * i, y - 14 - (i % 3) * 2, 0), shade(GRANITE_R, -0.05 * (i % 3)), rot_z=0.4 * i) for i in range(5)]
    return join(stump + [lying] + blocks, name)


def ramesseum(variant="1250"):
    ruin = variant == "ruin"
    m = Model("ramesseum")
    m.add(0, ground("rm_g", 180, 280, SAND), "ground")
    m.add(0, brick_wall("rm_enc", [(-10, -110), (-88, -110), (-88, 138), (88, 138), (88, -110), (10, -110)], 7 if ruin else 9, 4, MUD if not ruin else MUD_LT), "walls")
    vh = 1.7 if ruin else 4.0
    mags = [vault_row("rm_mn", 6, 5, 38, vh, (68, 30, 0), MUD), vault_row("rm_mb", 10, 5, 24, vh, (0, 116, 0), MUD),
            vault_row("rm_ms", 4, 5, 34, vh, (-70, 60, 0), MUD), vault_row("rm_mn2", 8, 5, 30, vh, (62, 98, 0), MUD, along="x")]
    m.add(0, join(mags, "rm_magazines"), "magazines")
    if ruin:
        m.add(1, e_pylon("rm_p1", 67, 24, 14, (0, -98, 0), SANDSTONE, unfinished=(0.45, 0.7)), "pylons")
        m.add(1, join([cylinder(f"rm_rub{i}", 7 + i, 3 + i % 3, (-30 + 15 * i, -84 + 4 * (i % 2), 0), SANDSTONE_DK, verts=10, r_top=2) for i in range(5)], "rm_rubble"))
        m.add(1, e_pylon("rm_p2", 58, 20, 10, (0, -37, 0), SANDSTONE, unfinished=(0.35, 0.25)))
    else:
        m.add(1, e_pylon("rm_p1", 67, 24, 14, (0, -98, 0), SANDSTONE, back_relief=True), "pylons")
        m.add(1, e_pylon("rm_p2", 58, 20, 10, (0, -37, 0), SANDSTONE))
    m.add(1, court_walls("rm_c1", -30, 30, -91, -42, 8, 2.0, SANDSTONE_DK, gaps=("S", "N")))
    pal = [box("rm_pal", 26, 40, 6 if not ruin else 2.5, (-46, -66, 0), MUD_LT), box("rm_win", 0.4, 4, 3, (-32.8, -66, 3.5 if not ruin else 0), DARK)]
    if not ruin:
        pal.append(box("rm_palr", 22, 34, 0.2, (-46, -66, 6), shade(MUD_LT, -0.15)))
    m.add(1, join(pal, "rm_palace"))
    col = column_proto("rm_c1c", 0.9, 9, "bud", SANDSTONE)
    m.add(2, scatter(col, "rm_c1cols", [(xx, -86 + 38 * j / 7, 0) for xx in (20, 25) for j in range(8) if not (ruin and j % 3 == 1)]), "courts")
    if ruin:
        m.add(3, _fallen_colossus("rm_colossus", (-12, -54, 0)), "colossus")
    else:
        m.add(3, scatter(seated_proto("rm_col", 19.0, GRANITE_R, queen=True), "rm_colossus", [(-12, -52, 0)]), "colossus")
    osr = osiride_proto("rm_os", 8.0, 2.0, SANDSTONE, SANDSTONE_LT)
    sp = [(-22 + 44 * i / 7, -26, 180) for i in range(8)] + [(-22 + 44 * i / 7, 8, 0) for i in range(8)]
    if ruin:
        sp = [s for i, s in enumerate(sp) if i % 3 != 1]
    m.add(2, scatter(osr, "rm_osirides", sp))
    m.add(1, court_walls("rm_c2", -28, 28, -32, 10, 7 if not ruin else 4, 1.6, SANDSTONE_DK, gaps=("S", "N")))
    s2 = seated_proto("rm_c2s", 8, GRANITE_B)
    m.add(3, scatter(s2, "rm_younger_memnon", [(-7, -2, 0), (7, -2, 0)] if not ruin else [(7, -2, 0)]))
    nave = column_proto("rm_nv", 1.2, 13.5, "open", SANDSTONE)
    aisle = column_proto("rm_ai", 0.95, 10.5, "bud", SANDSTONE)
    ns = [(sx * 4.2, 14 + 30 * j / 5, 0) for sx in (-1, 1) for j in range(6)]
    as_ = [(sx * (10 + 5.5 * i), 14 + 30 * j / 5, 0) for sx in (-1, 1) for i in range(3) for j in range(6)]
    if ruin:
        ns = [s for i, s in enumerate(ns) if i % 4 != 3]
        as_ = [s for i, s in enumerate(as_) if s[0] < 0 and i % 3 != 2]
    m.add(2, scatter(nave, "rm_nave", ns), "hypostyle")
    m.add(2, scatter(aisle, "rm_aisles", as_))
    walls = [box(f"rm_hw{sx}", 2, 34, 11.4 if not ruin else 5, (sx * 27, 29, 0), SANDSTONE_DK) for sx in (-1, 1)]
    if not ruin:
        walls += [box("rm_hr_w", 20, 34, 0.9, (-16.5, 29, 10.5), SANDSTONE), box("rm_hr_e", 20, 34, 0.9, (16.5, 29, 10.5), SANDSTONE),
                  box("rm_hr_n", 14, 34, 0.9, (0, 29, 13.5), shade(SANDSTONE, 0.06))]
        walls += [box(f"rm_hcl{sx}", 1.2, 34, 2.1, (sx * 6.8, 29, 11.4), SANDSTONE) for sx in (-1, 1)]
        walls += [box(f"rm_hgr{sx}{j}", 1.3, 2.4, 1.2, (sx * 6.8, 15 + 28 * j / 5, 11.8), DARK) for sx in (-1, 1) for j in range(6)]
    else:
        walls += [box("rm_hr_frag", 14, 12, 0.9, (0, 40, 13.5), shade(SANDSTONE, 0.06)), box("rm_hr_frag2", 20, 10, 0.9, (-16.5, 40, 10.5), SANDSTONE)]
    m.add(2, join(walls, "rm_hyproof"))
    m.add(1, roofed_block("rm_inner", 40, 36, 8.5 if not ruin else 5, (0, 66, 0), SANDSTONE, cornice=not ruin), "temple")
    m.add(1, roofed_block("rm_tuya", 18, 34, 6 if not ruin else 3, (40, 20, 0), SANDSTONE_LT, cornice=not ruin))
    more = [vault_row("rm_mw", 5, 5, 30, vh, (-72, -20, 0), MUD), vault_row("rm_mne", 6, 5, 34, vh, (62, -60, 0), MUD),
            vault_row("rm_msw", 6, 5, 26, vh, (-50, 115, 0), MUD, along="x")]
    m.add(0, join(more, "rm_magazines2"))
    pp = column_proto("rm_pp", 0.8, 7.5, "bud", SANDSTONE, band=None)
    sp = [(-25, -86 + 38 * j / 7, 0) for j in range(8)] + [(sx * 23, -29 + 34 * j / 6, 0) for sx in (-1, 1) for j in range(1, 6)]
    if ruin:
        sp = [q for i, q in enumerate(sp) if i % 2 == 0]
    m.add(2, scatter(pp, "rm_porticoes", sp))
    if not ruin:
        m.add(2, join([box("rm_c1rf_n", 10, 42, 0.8, (22.5, -67, 9.3), SANDSTONE), box("rm_c1rf_s", 5, 42, 0.8, (-25, -67, 7.7), SANDSTONE)], "rm_c1roofs"))
        m.add(1, join([wedge("rm_ramp2", 8, 6, 1.5, (0, 9.5, 0), shade(SANDSTONE, -0.06), "S"), box("rm_hypplat", 54, 34, 0.6, (0, 29, 0), shade(PAVE, -0.04))], "rm_ramps"))
    m.add(3, house_field("rm_school", -84, -60, -104, -50, 131, (5, 8), (3.5, 5), 2.0, 0.85, roofless=ruin), "houses")
    if not ruin:
        stp = standing_proto("rm_hst", 6.5, GRANITE_B)
        m.add(3, scatter(stp, "rm_hypstat", [(-9, 10.5, 0), (9, 10.5, 0)]))
        m.add(3, house_field("rm_front", 36, 84, -104, -82, 132, (5, 8), (3.5, 5), 2.0, 0.85))
    m.add(3, palms("rm_palms", [(-70, -100), (-60, -104), (70, -100), (78, -92), (-80, 120), (80, 128), (40, -104), (52, -100), (-40, 130)]), "trees")
    return m


# ---------------------------------------------------------------- Seti I at Qurna

def seti_qurna():
    m = Model("seti-qurna")
    m.add(0, ground("sq_g", 120, 160, SAND), "ground")
    m.add(0, brick_wall("sq_enc", [(-8, -78), (-58, -78), (-58, 78), (58, 78), (58, -78), (8, -78)], 7, 3.5, MUD), "walls")
    m.add(1, e_pylon("sq_p1", 58, 15, 9, (0, -70, 0), MUD_LT, flags=2, relief=False), "pylons")
    m.add(1, e_pylon("sq_p2", 52, 13, 8, (0, -24, 0), MUD_LT, flags=0, relief=False))
    m.add(1, court_walls("sq_c", -27, 27, -65, -28, 5, 1.6, MUD, gaps=("S", "N")))
    m.add(0, box("sq_way", 8, 120, 0.35, (0, -18, 0), PAVE))
    sph = sphinx_proto("sq_sph", 0.9, "human", SANDSTONE)
    m.add(3, scatter(sph, "sq_sphinxes", [(sx * 7, -60 + 6 * j, 90 * -sx) for sx in (-1, 1) for j in range(5)]), "sphinxes")
    pc = column_proto("sq_pc", 0.85, 8.5, "bud", SANDSTONE)
    m.add(2, scatter(pc, "sq_portico", [(-22.5 + 45 * i / 9, yy, 0) for i in range(10) for yy in (12,)]), "temple")
    m.add(2, box("sq_porr", 50, 6, 0.8, (0, 14, 9.3), SANDSTONE))
    m.add(2, box("sq_porb", 50.2, 6.2, 0.3, (0, 14, 9.0), PAINT_BLUE))
    m.add(1, roofed_block("sq_t", 50, 54, 9, (0, 44, 0), SANDSTONE, raised=(14, 30, 2.2)))
    m.add(1, box("sq_door", 4, 0.5, 6, (0, 16.8, 0), DARK))
    m.add(1, join([box(f"sq_dd{i}", 2.4, 0.5, 4.5, (-18 + 9 * i, 16.8, 0), DARK) for i in range(5) if i != 2], "sq_doors"))
    m.add(1, roofed_block("sq_pal", 18, 30, 5, (-40, -46, 0), MUD_LT))
    pcp = column_proto("sq_palc", 0.5, 4.5, "bud", "#D8C3A0", band=None)
    m.add(2, scatter(pcp, "sq_palcols", [(-29.5, -58 + 6 * j, 0) for j in range(5)]))
    m.add(0, vault_row("sq_mag", 5, 5, 34, 3.5, (40, 40, 0), MUD), "magazines")
    m.add(0, vault_row("sq_mag2", 4, 5, 22, 3.5, (40, -50, 0), MUD))
    m.add(3, house_field("sq_h", -54, -32, 0, 72, 121, (5, 8), (3.5, 5), 2.0, 0.85), "houses")
    m.add(3, palms("sq_palms", [(-50, -74), (50, -72), (-40, 70), (-50, 60), (48, -10), (50, 0), (20, -74), (-20, -74)]), "trees")
    return m


# ---------------------------------------------------------------- the Colossi of Memnon and Kom el-Hettan

def colossi_of_memnon(variant="1250"):
    m = Model("colossi-of-memnon")
    m.add(0, ground("cm_g", 120, 400, SAND), "ground")
    if variant == "1250":
        m.add(0, brick_wall("cm_enc", [(-50, -172), (-58, -172), (-58, 198), (58, 198), (58, -172), (50, -172)], 7, 4, MUD), "walls")
        m.add(1, e_pylon("cm_p1", 100, 19, 12, (0, -172, 0), MUD_LT, flags=2), "pylons")
        m.add(1, e_pylon("cm_p2", 84, 20, 11, (0, -90, 0), MUD_LT, flags=2, relief=False))
        m.add(1, e_pylon("cm_p3", 86, 23, 12, (0, 18, 0), SANDSTONE, flags=2))
        m.add(0, box("cm_way", 12, 180, 0.35, (0, -76, 0), PAVE))
        jk = sphinx_proto("cm_jk", 1.0, "jackal", "#D2C2A2")
        m.add(3, scatter(jk, "cm_jackals", [(sx * 9, -158 + 6.4 * j, 90 * -sx) for sx in (-1, 1) for j in range(10)] + [(sx * 9, -78 + 6.6 * j, 90 * -sx) for sx in (-1, 1) for j in range(13)]), "statues")
        pc = column_proto("cm_pc", 1.2, 13, "bud", SANDSTONE)
        m.add(2, peristyle_cols(pc, "cm_court", -40, 40, 30, 130, 12, 14, rows=3, gap=4.5, sides="EW"), "court")
        m.add(1, court_walls("cm_cw", -46, 46, 25, 135, 9, 2.0, SANDSTONE_DK, gaps=("S",)))
        st = standing_proto("cm_st", 8, QUARTZITE)
        m.add(3, scatter(st, "cm_courtstat", [(sx * 25, 36 + 92 * j / 7, 90 * -sx) for sx in (-1, 1) for j in range(8)]))
        m.add(1, roofed_block("cm_hyp", 70, 40, 12, (0, 157, 0), SANDSTONE, raised=(22, 40, 3.0)), "temple")
        m.add(1, roofed_block("cm_sanct", 46, 20, 9, (0, 187, 0), SANDSTONE))
        st2 = [obelisk_t("cm_stela_n", 8, (-34, 28, 0), QUARTZITE, QUARTZITE), obelisk_t("cm_stela_s", 8, (34, 28, 0), QUARTZITE, QUARTZITE)]
        m.add(3, join(st2, "cm_stelae"))
    else:
        rnd = random.Random(9)
        m.add(0, box("cm_field", 100, 120, 0.4, (0, 60, 0), FIELD))
        rub = []
        for i in range(16):
            x = rnd.uniform(-48, 48)
            y = rnd.uniform(-160, 190)
            w = rnd.uniform(6, 18)
            rub.append(frustum(f"cm_rub{i}", w, w * 0.8, w * 0.4, w * 0.3, rnd.uniform(1.0, 3.0), (x, y, 0), shade(MUD_LT, -0.05 * (i % 3))))
        m.add(1, join(rub, "cm_rubble"), "ruins")
        stumps = column_proto("cm_stump", 1.2, 2.6, "bud", SANDSTONE, band=None)
        m.add(2, scatter(stumps, "cm_stumps", [(rnd.uniform(-40, 40), rnd.uniform(30, 130), 0) for _ in range(14)]), "stumps")
        st = standing_proto("cm_fst", 8, QUARTZITE, base=False)
        fallen = [clone(st, f"cm_fall{i}", rnd.uniform(-35, 35), rnd.uniform(40, 120), 1.2, rnd.uniform(0, 360), tilt_x=-90) for i in range(4)]
        drop(st)
        m.add(2, join(fallen, "cm_fallen"))
        m.add(3, palm_ring("cm_palms", -55, 55, -150, 190, 18, 21), "fields")
    for k, sx in enumerate((-1, 1)):
        c = seated_proto(f"cm_col{k}", 20.0, QUARTZITE, crown="double", queen=True)
        c = move(c, sx * 8.5, -188, 0)
        m.add(3 if variant == "1250" else 1, c, "colossi")
    if variant == "roman":
        rep = [box(f"cm_rep{i}", 6.9, 5.0, 1.05, (8.5, -185.3, 9.8 + i * 1.15), SANDSTONE_LT if i % 2 else SANDSTONE) for i in range(5)]
        rep.append(box("cm_crack", 7.2, 5.6, 0.25, (8.5, -185.3, 9.6), DARK))
        m.add(2, join(rep, "cm_repair"), "repair")
    return m


# ---------------------------------------------------------------- Medinet Habu

def _migdol(name, loc, w=30, d=16, h=22):
    x, y, z = loc
    p = []
    for s in (-1, 1):
        p.append(frustum(f"{name}t{s}", w * 0.38, d, w * 0.36, d * 0.92, h, (x + s * w * 0.31, y, 0), SANDSTONE))
        p.append(move(merlons(f"{name}m{s}", w * 0.36, d * 0.92, h, 1.0, 1.2, SANDSTONE, "round"), x + s * w * 0.31, y, 0))
        for r in range(3):
            p.append(box(f"{name}w{s}{r}", 1.4, 0.3, 2.0, (x + s * w * 0.31, y - d / 2 + 0.2 + r * 0.25, 8 + r * 4.5), DARK))
    p.append(box(name + "br", w * 0.3, d * 0.8, h * 0.72, (x, y, 0), SANDSTONE_LT))
    p.append(box(name + "pa", w * 0.14, d * 0.84, h * 0.4, (x, y, 0), DARK))
    p.append(box(name + "win", w * 0.16, 0.3, 2.4, (x, y - d * 0.4, h * 0.5), DARK))
    return join(p, name)


def medinet_habu(variant="600"):
    m = Model("medinet-habu")
    m.add(0, ground("mb_g", 210, 320, SAND), "ground")
    m.add(0, brick_wall("mb_enc", [(-16, -140), (-100, -140), (-100, 150), (100, 150), (100, -140), (16, -140)], 18, 9, MUD, batter=0.2, crenels=True), "walls")
    m.add(0, brick_wall("mb_low", [(-15, -157), (-104, -157), (-104, 157), (104, 157), (104, -157), (15, -157)], 4, 1.6, SANDSTONE_DK, batter=0.1, crenels=True))
    m.add(1, _migdol("mb_gate", (0, -149, 0)), "gates")
    m.add(1, _migdol("mb_wgate", (0, 150, 0), 24, 14, 18))
    X = 10.0
    m.add(1, e_pylon("mb_p1", 68, 24, 12, (X, -80, 0), SANDSTONE), "temple")
    m.add(1, court_walls("mb_c1", X - 32, X + 32, -74, -30, 9, 2.0, SANDSTONE_DK, gaps=("S", "N")))
    osr = osiride_proto("mb_os", 8.5, 2.2, SANDSTONE, SANDSTONE_LT)
    m.add(2, scatter(osr, "mb_c1os", [(X + 26, -70 + 36 * j / 6, -90) for j in range(7)]), "courts")
    pc = column_proto("mb_pc", 1.0, 9, "open", SANDSTONE)
    m.add(2, scatter(pc, "mb_c1cols", [(X - 26, -70 + 36 * j / 6, 0) for j in range(7)]))
    m.add(1, e_pylon("mb_p2", 60, 21, 10, (X, -25, 0), SANDSTONE))
    m.add(1, court_walls("mb_c2", X - 30, X + 30, -20, 20, 9, 2.0, SANDSTONE_DK, gaps=("S", "N")))
    m.add(2, scatter(osiride_proto("mb_os2", 8.0, 2.0, SANDSTONE, SANDSTONE_LT), "mb_c2os",
                     [(X - 24 + 48 * i / 7, -16, 180) for i in range(8)] + [(X - 24 + 48 * i / 7, 16, 0) for i in range(8)]))
    m.add(1, roofed_block("mb_hyp", 56, 26, 11, (X, 34, 0), SANDSTONE, raised=(16, 26, 2.4)))
    m.add(1, roofed_block("mb_inner", 50, 56, 9, (X, 75, 0), SANDSTONE))
    m.add(1, roofed_block("mb_pal", 30, 40, 7, (X - 50, -52, 0), MUD_LT, cornice=False))
    m.add(1, box("mb_window", 0.4, 6, 3.5, (X - 34.8, -52, 3.5), DARK))
    m.add(1, e_pylon("mb_tp", 26, 11, 5, (62, -120, 0), SANDSTONE_LT, flags=0))
    m.add(1, roofed_block("mb_t", 18, 30, 7, (62, -97, 0), SANDSTONE_LT, raised=(8, 22, 1.6)))
    chap = []
    for i in range(4):
        cx = -70 + 13 * i
        chap.append(e_pylon(f"mb_gw{i}", 11, 7, 3, (cx, -132, 0), SANDSTONE_LT, flags=0, relief=False))
        chap.append(roofed_block(f"mb_gwc{i}", 9, 12, 6, (cx, -122, 0), SANDSTONE_LT))
    m.add(2, join(chap, "mb_godswives"), "chapels")
    m.add(0, box("mb_lake", 14, 18, 0.5, (70, -40, 0), NILE))
    if variant == "djeme":
        hs = [house_field("mb_dj1", -92, -40, -134, -80, 101, (6, 10), (5, 9), 2.2, 0.92, avoid=[(-76, -25, -140, -112)]),
              house_field("mb_dj2", 46, 92, -70, 142, 102, (6, 10), (5, 9), 2.2, 0.92, avoid=[(60, 80, -50, -30)]),
              house_field("mb_dj3", -92, -30, -20, 142, 103, (6, 10), (5, 9), 2.2, 0.92),
              house_field("mb_dj4", -26, 46, 104, 142, 104, (6, 10), (5, 9), 2.2, 0.92)]
        m.add(3, join([h for h in hs if h is not None], "mb_djeme"), "town")
    else:
        m.add(3, house_field("mb_pr", -92, -36, 40, 142, 106, (6, 10), (4, 6), 2.4, 0.7), "houses")
        m.add(3, palms("mb_palms", [(80, 80), (84, 100), (76, 120), (-84, 0), (-80, 14)]))
    return m


# ---------------------------------------------------------------- Deir el-Medina

def deir_el_medina(variant="1250"):
    ruin = variant in ("ruin", "hathor")
    m = Model("deir-el-medina")
    m.add(0, ground("dm_g", 80, 170, ROCK_LT), "ground")
    m.add(0, frustum("dm_slope", 12, 170, 6, 166, 6, (-34, 0, 0), ROCK), "slope")
    m.add(0, box("dm_street", 3.0, 128, 0.35, (0, -10, 0), PAVE))
    wall_h = 3.6 if not ruin else 1.6
    m.add(1, brick_wall("dm_wall", [(-2, -76), (-25, -76), (-25, 56), (25, 56), (25, -76), (2, -76)], wall_h, 1.2, "#E4D8C0" if not ruin else MUD_LT, batter=0.1), "walls")
    houses = []
    n = 23
    for i in range(n):
        y = -73 + 126 * (i + 0.5) / n
        for sx in (-1, 1):
            c = HOUSE_COLS[(i + (sx > 0)) % len(HOUSE_COLS)] if ruin else ["#EDE5D3", "#E6DCC6", "#F1EAD9"][(i + (sx > 0)) % 3]
            houses.append(e_house(f"dm_h{i}{sx}", 20.5, 5.0, 3.6 if not ruin else 1.8, (sx * 12.6, y, 0.3), c, "E" if sx < 0 else "W", extras=not ruin and i % 2 == 0, roofless=ruin))
    m.add(2, join(houses, "dm_houses"), "houses")
    pyr, chap = [], []
    for j in range(9):
        y = -78 + 150 * j / 8
        h = 5.0 if not ruin else 3.0
        chap.append(box(f"dm_tc{j}", 6, 6, 2.2, (-33.5, y, 6), "#E6DCC6"))
        chap.append(box(f"dm_td{j}", 0.3, 1.4, 1.8, (-30.4, y, 6), DARK))
        pyr.append(frustum(f"dm_tp{j}", 4.4, 4.4, 0.3, 0.3, h, (-34, y, 8.2), MUD_LT if ruin else "#EDE5D3"))
        pyr.append(box(f"dm_tpy{j}", 0.8, 0.8, 0.6, (-34, y, 8.2 + h), "#E8D9B0"))
    m.add(3, join(pyr + chap, "dm_tombs"), "tombs")
    m.add(0, boulders("dm_bould", -40, -29, -84, 84, 30, 51, 1.4, ROCK))
    if ruin:
        m.add(1, boulders("dm_sand", -22, 22, -72, 52, 26, 52, 2.2, "#D8C49C"))
    if not ruin:
        m.add(3, join([roofed_block(f"dm_sh{k}", 7, 9, 4, (33, -40 + 30 * k, 0.3), "#EDE5D3", door="W") for k in range(3)], "dm_chapels"))
    if variant == "hathor":
        m.add(1, brick_wall("dm_tenc", [(-20, 58), (20, 58), (20, 84), (-20, 84)], 5, 1.6, MUD, closed=True), "temple")
        m.add(1, e_pylon("dm_tpy", 14, 8, 3, (0, 62, 0), SANDSTONE_LT, flags=0))
        m.add(1, roofed_block("dm_temple", 10, 16, 7, (0, 73, 0), SANDSTONE_LT, raised=(6, 8, 1.2)))
    elif not ruin:
        m.add(3, palms("dm_palm", [(30, 60), (34, 70), (-10, 66)], 1.8))
    return m


# ---------------------------------------------------------------- Malkata

def malkata():
    m = Model("malkata")
    m.add(0, ground("ml_g", 240, 300, SAND), "ground")
    rnd = random.Random(17)

    def palace(name, x0, x1, y0, y1, h, rooms, cols, color=MUD_LT):
        p = [court_walls(name + "w", x0, x1, y0, y1, h, 1.4, color)]
        w, d = x1 - x0, y1 - y0
        hx, hy = (x0 + x1) / 2, (y0 + y1) / 2
        p.append(box(name + "fl", w * 0.5, d * 0.45, 0.2, (hx, hy, 0.3), PAINT_BLUE))
        p.append(box(name + "fl2", w * 0.46, d * 0.08, 0.22, (hx, hy - d * 0.12, 0.3), PAINT_YEL))
        cp = cylinder(name + "cp", 0.45, h - 0.4, (0, 0, 0), "#9A7A54", verts=8)
        sp = [(hx - w * 0.2 + w * 0.4 * i / (cols - 1), hy - d * 0.18 + d * 0.36 * j / 2, 0) for i in range(cols) for j in range(3)]
        p.append(scatter(cp, name + "cols", sp))
        p.append(box(name + "rf", w * 0.25, d * 0.45, 0.4, (hx + w * 0.12, hy, h - 0.4), shade(color, -0.1)))
        for k in range(rooms):
            rx = x0 + 3 + (w - 6) * (k + 0.5) / rooms
            p.append(e_house(f"{name}r{k}", (w - 6) / rooms - 1.2, d * 0.18, h * rnd.uniform(0.6, 1.0), (rx, y1 - d * 0.12, 0.3), color, "S", False, roofless=rnd.random() < 0.4))
            p.append(e_house(f"{name}q{k}", (w - 6) / rooms - 1.2, d * 0.18, h * rnd.uniform(0.6, 1.0), (rx, y0 + d * 0.12, 0.3), color, "N", False, roofless=rnd.random() < 0.4))
        return join(p, name)

    m.add(1, palace("ml_king", -70, 20, -40, 80, 6.5, 6, 6), "palaces")
    m.add(1, palace("ml_queen", -70, -5, -120, -55, 5.5, 4, 4))
    m.add(1, palace("ml_north", -100, -45, 92, 136, 5.0, 4, 3))
    m.add(1, palace("ml_fest", 40, 100, -20, 60, 6.0, 4, 5, MUD))
    m.add(1, e_pylon("ml_tp", 34, 11, 6, (55, 96, 0), MUD_LT, flags=0, relief=False))
    m.add(1, roofed_block("ml_temple", 30, 34, 6.5, (55, 120, 0), MUD_LT, cornice=False, raised=(10, 20, 1.5)))
    m.add(2, house_field("ml_village", -104, -78, -136, 80, 111, (5, 9), (3, 5), 2.0, 0.85), "houses")
    m.add(2, house_field("ml_village2", 10, 100, -136, -40, 112, (5, 9), (3, 5), 2.0, 0.7))
    m.add(0, brick_wall("ml_enc", [(-108, -142), (108, -142), (108, 142), (-108, 142)], 4.0, 2.0, MUD_LT, closed=True), "walls")
    m.add(0, box("ml_harbour", 8, 300, 0.5, (116, 0, 0), NILE))
    m.add(3, join([nile_boat("ml_barge", 18, (116, -60, 0.5), 90, sail=False, sacred=True)], "ml_boats"), "harbour")
    return m


BUILDERS = {
    "thebes/karnak": karnak,
    "thebes/karnak-1950": lambda: karnak("1950"),
    "thebes/karnak-1470": lambda: karnak("1470"),
    "thebes/karnak-late": lambda: karnak("late"),
    "thebes/karnak-quay": karnak_quay,
    "thebes/mut-precinct": mut_precinct,
    "thebes/montu-precinct": montu_precinct,
    "thebes/town-of-thebes": town_of_thebes,
    "thebes/avenue-of-sphinxes": avenue_of_sphinxes,
    "thebes/processional-way": lambda: avenue_of_sphinxes("way"),
    "thebes/opet-shrine": opet_shrine,
    "thebes/luxor-temple": luxor_temple,
    "thebes/luxor-1470": lambda: luxor_temple("1470"),
    "thebes/luxor-roman": lambda: luxor_temple("roman"),
    "thebes/deir-el-bahari": deir_el_bahari,
    "thebes/deir-el-bahari-1950": lambda: deir_el_bahari("1950"),
    "thebes/valley-of-the-kings": valley_of_the_kings,
    "thebes/nobles-tombs": nobles_tombs,
    "thebes/ramesseum": ramesseum,
    "thebes/ramesseum-ruin": lambda: ramesseum("ruin"),
    "thebes/seti-qurna": seti_qurna,
    "thebes/colossi-of-memnon": colossi_of_memnon,
    "thebes/memnon-ruin": lambda: colossi_of_memnon("ruin"),
    "thebes/memnon-roman": lambda: colossi_of_memnon("roman"),
    "thebes/medinet-habu": medinet_habu,
    "thebes/medinet-habu-djeme": lambda: medinet_habu("djeme"),
    "thebes/deir-el-medina": deir_el_medina,
    "thebes/deir-el-medina-ruin": lambda: deir_el_medina("ruin"),
    "thebes/deir-el-medina-hathor": lambda: deir_el_medina("hathor"),
    "thebes/malkata": malkata,
}
