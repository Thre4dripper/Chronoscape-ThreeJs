"""Dunhuang / Shazhou landmark miniatures.

The hall, roof, gate and wall helpers are copied from the Chang'an module (changan.py); the layered
rammed-earth walls, beacon tower, cave cliff with its galleries and the Great Buddha façade are Dunhuang's own."""
import math
import bpy
from chronokit import Model, box, cylinder, dome, join, shade, mesh_from
from worldkit import *

VERM = "#B04A32"          # Tang red ochre on columns and brackets
WHITE = "#EDE5D3"         # whitewashed walls
TILE = "#5C5D60"          # grey tile
BARK = "#6E4B3A"
GLAZE = "#3F8A62"         # green glaze (Tang ridges, Ming roofs)
GLAZE_TEAL = "#3C7F7A"
STONE = "#B9B1A2"
GRAVEL = "#DDD3BE"
EARTH = "#C4AE86"         # rammed loess
EARTH_D = "#B09A72"
BRICKF = "#A49A8A"        # grey brick facing (Tang palace terraces)
PBRICK = "#B7A68A"        # the buff-grey brick of the pagodas
PBRICK_D = "#9C8C72"
MBRICK = "#8E8A84"        # Ming grey brick
CLAY = "#CDB994"          # ward and courtyard walls
GRASS = "#9AA56E"
FIELD = "#B4AE78"
WOOD = "#6A5442"
DARKW = "#3A2E26"
PINE = "#557048"
WILLOW = "#93A660"
LOCUST = "#6F8A50"
WATERC = "#5F878C"


def shibi_fin(name, rt, loc, s, color=GILT):
    """A ridge-end ornament (shibi): an upright fin curling inward, s = -1 west end, +1 east end."""
    x, y, z = loc
    a = box(name + "_a", rt * 1.2, rt * 0.9, rt * 2.2, (x, y, z), color)
    b = box(name + "_b", rt * 1.0, rt * 0.8, rt * 1.4, (x - s * rt * 0.7, y, z + rt * 1.4), color)
    return join([a, b], name)


# ---------------------------------------------------------------- placement and small parts

def put(o, x=0.0, y=0.0, deg=0.0, z=0.0):
    """Turn an object about the world origin (deg counter-clockwise; 90 turns a south front to face east) and move it."""
    o = move(o)
    if deg:
        o = rot(o, deg)
    return move(o, x, y, z)


def seg_prism(name, a, b, z, width, rh, color):
    """A gabled roof (or ridge-shaped mound) running from a to b, base at z."""
    (ax, ay), (bx, by) = a, b
    L = math.hypot(bx - ax, by - ay)
    t = math.atan2(by - ay, bx - ax)
    ca, sa = math.cos(t), math.sin(t)
    cx, cy = (ax + bx) / 2, (ay + by) / 2
    loc = [(-L / 2, -width / 2, 0), (L / 2, -width / 2, 0), (L / 2, width / 2, 0), (-L / 2, width / 2, 0), (-L / 2, 0, rh), (L / 2, 0, rh)]
    verts = [(cx + px * ca - py * sa, cy + px * sa + py * ca, z + pz) for px, py, pz in loc]
    faces = [(3, 2, 1, 0), (0, 1, 5, 4), (2, 3, 4, 5), (1, 2, 5), (3, 0, 4)]
    return mesh_from(name, verts, faces, (0, 0, 0), color)


def blob(name, rx, ry, h, loc=(0, 0, 0), color=WATER, seed=0.0, n=28):
    """An irregular rounded outline (pond, island) extruded by h."""
    pts = []
    for i in range(n):
        a = math.tau * i / n
        k = 1 + 0.12 * math.sin(3 * a + seed) + 0.07 * math.cos(5 * a + seed * 2)
        pts.append((rx * k * math.cos(a), ry * k * math.sin(a)))
    return prism(name, pts, h, loc, color)


def grove(name, pts, r=4.0, color=PINE):
    return join([tree(f"{name}{i}", r * (0.85 + 0.3 * ((i * 37) % 7) / 7), (x, y, z), color) for i, (x, y, z) in enumerate(pts)], name)


def wall_line(name, pts, h=3.0, t=1.3, color=CLAY, cap=TILE, closed=False):
    """Earth wall (tsuiji) along a polyline with a small tiled cap."""
    if closed:
        pts = list(pts) + [pts[0]]
    parts = []
    for i in range(1, len(pts)):
        (ax, ay), (bx, by) = pts[i - 1], pts[i]
        L = math.hypot(bx - ax, by - ay)
        a = math.atan2(by - ay, bx - ax)
        cx, cy = (ax + bx) / 2, (ay + by) / 2
        parts.append(box(f"{name}_w{i}", L + t, t, h, (cx, cy, 0), color, rot_z=a))
        parts.append(seg_prism(f"{name}_c{i}", (ax - math.cos(a) * t / 2, ay - math.sin(a) * t / 2), (bx + math.cos(a) * t / 2, by + math.sin(a) * t / 2), h, t + 1.0, 0.7, cap))
    return join(parts, name)


def rect_pts(w, d, x=0.0, y=0.0):
    return [(x - w / 2, y - d / 2), (x + w / 2, y - d / 2), (x + w / 2, y + d / 2), (x - w / 2, y + d / 2)]


def gallery(name, pts, w=5.0, h=3.2, col=VERM, roof=TILE, floor=0.5, wall=None, closed=False, post_every=4.5):
    """A roofed corridor (kairō, watadono) on posts along a polyline."""
    if closed:
        pts = list(pts) + [pts[0]]
    parts = []
    for i in range(1, len(pts)):
        (ax, ay), (bx, by) = pts[i - 1], pts[i]
        L = math.hypot(bx - ax, by - ay)
        a = math.atan2(by - ay, bx - ax)
        ca, sa = math.cos(a), math.sin(a)
        cx, cy = (ax + bx) / 2, (ay + by) / 2
        parts.append(box(f"{name}_f{i}", L + w, w, floor, (cx, cy, 0), STONE, rot_z=a))
        if wall:
            parts.append(box(f"{name}_wl{i}", L, 0.6, h, (cx, cy, floor), wall, rot_z=a))
        n = max(1, round(L / post_every))
        for k in range(n + 1):
            t = -L / 2 + L * k / n
            for s in (-1, 1):
                off = s * (w / 2 - 0.3)
                parts.append(box(f"{name}_p{i}_{k}{s}", 0.42, 0.42, h, (cx + ca * t - sa * off, cy + sa * t + ca * off, floor), col))
        parts.append(box(f"{name}_b{i}", L + w, w, 0.35, (cx, cy, floor + h - 0.35), col, rot_z=a))
        ext = w / 2 + 0.6
        parts.append(seg_prism(f"{name}_r{i}", (ax - ca * ext, ay - sa * ext), (bx + ca * ext, by + sa * ext), floor + h, w + 1.8, w * 0.38, roof))
    return join(parts, name)


# ---------------------------------------------------------------- roofs

def irimoya(name, w, d, h, loc=(0, 0, 0), color=TILE, over=None, curve=0.16, ridge=None, gable=None, shibi=None):
    """Hip-and-gable roof (irimoya), ridge along X: a hipped skirt, a steeper gabled top, eave corners turned up."""
    x, y, z = loc
    over = min(w, d) * 0.24 if over is None else over
    W, D = w + 2 * over, d + 2 * over
    lift, sag = h * curve, h * 0.02
    zm = h * 0.42
    Wm = max(W - D * 0.6, W * 0.35)
    Dm = D * 0.42
    E = [(-W / 2, -D / 2, lift), (0, -D / 2, sag), (W / 2, -D / 2, lift), (W / 2, 0, sag), (W / 2, D / 2, lift), (0, D / 2, sag), (-W / 2, D / 2, lift), (-W / 2, 0, sag)]
    M = [(-Wm / 2, -Dm / 2, zm), (Wm / 2, -Dm / 2, zm), (Wm / 2, Dm / 2, zm), (-Wm / 2, Dm / 2, zm)]
    R = [(-Wm / 2, 0, h), (Wm / 2, 0, h)]
    faces = [(0, 1, 8), (1, 9, 8), (1, 2, 9), (2, 3, 9), (3, 10, 9), (3, 4, 10), (4, 5, 10), (5, 11, 10), (5, 6, 11), (6, 7, 11), (7, 8, 11), (7, 0, 8),
             (8, 9, 13, 12), (10, 11, 12, 13), (11, 8, 12), (9, 10, 13), (7, 6, 5, 4, 3, 2, 1, 0)]
    parts = [mesh_from(name + "_r", E + M + R, faces, (x, y, z), color)]
    rc = ridge or shade(color, -0.2)
    rt = max(0.4, D * 0.035)
    parts.append(box(name + "_rg", Wm + rt, rt, rt, (x, y, z + h - rt * 0.4), rc))
    for s in (-1, 1):
        parts.append(box(f"{name}_on{s}", rt * 0.9, rt * 1.1, rt * 1.5, (x + s * (Wm / 2 + rt * 0.1), y, z + h - rt * 0.4), rc))
        gx = x + s * (Wm / 2 + 0.06)
        gverts = [(gx, y - Dm / 2 * 0.92, z + zm + 0.1), (gx, y + Dm / 2 * 0.92, z + zm + 0.1), (gx, y, z + h - 0.3)]
        parts.append(mesh_from(f"{name}_gb{s}", gverts, [(0, 1, 2)], (0, 0, 0), gable or shade(WOOD, 0.1)))
        if shibi:
            parts.append(shibi_fin(f"{name}_sb{s}", rt, (x + s * (Wm / 2 + rt * 0.2), y, z + h - rt * 0.4), s, shibi))
    return join(parts, name)


def hip(name, w, d, h, loc=(0, 0, 0), color=TILE, over=None, ridge=None, trim=None, shibi=None):
    """Hipped roof (yosemune) on worldkit's eaved roof, with a heavier ridge, optional coloured eave trim and ridge-end fins."""
    x, y, z = loc
    over = min(w, d) * 0.22 if over is None else over
    parts = [eaved_roof(name + "_r", w, d, h, loc, color, over=over, curve=0.16)]
    W, D = w + 2 * over, d + 2 * over
    rl = max(0.0, (W - D) * 0.5)
    rt = max(0.5, D * 0.035)
    rc = ridge or shade(color, -0.2)
    parts.append(box(name + "_rg", rl + rt * 2, rt, rt * 1.2, (x, y, z + h - rt * 0.4), rc))
    if shibi:
        for s in (-1, 1):
            parts.append(shibi_fin(f"{name}_sb{s}", rt, (x + s * (rl / 2 + rt * 0.3), y, z + h - rt * 0.4), s, shibi))
    if trim:
        lz = z + h * 0.16 - 0.25
        for s in (-1, 1):
            parts.append(box(f"{name}_tx{s}", W, 0.7, 0.5, (x, y + s * (D / 2 - 0.3), lz), trim))
            parts.append(box(f"{name}_ty{s}", 0.7, D, 0.5, (x + s * (W / 2 - 0.3), y, lz), trim))
    return join(parts, name)


# ---------------------------------------------------------------- halls and gates

def hall_parts(name, w, d, h, roof="irimoya", roof_h=None, roof_color=TILE, col=VERM, wall=WHITE, plat=1.0, plat_color=STONE,
               bays=None, over=None, mokoshi=False, floor=0.0, doors=True, ridge=None, trim=None, shibi=None, stairs=True):
    """A timber hall: platform (or raised floor), columns, wall panels, dark doors; returns (body, roof)."""
    parts = []
    z = 0.0
    if plat:
        parts.append(box(name + "_pl", w + 3, d + 3, plat, (0, 0, 0), plat_color))
        if stairs and plat > 0.5:
            parts.append(box(name + "_st", min(w * 0.3, 12), 3.0, plat * 0.55, (0, -d / 2 - 3.0, 0), plat_color))
        z = plat
    if floor:
        parts.append(box(name + "_us", w * 0.9, d * 0.9, floor, (0, 0, z), DARKW))
        parts.append(box(name + "_ve", w + 2.4, d + 2.4, 0.35, (0, 0, z + floor - 0.35), WOOD))
        z += floor
    parts.append(box(name + "_w", w - 0.5, d - 0.5, h, (0, 0, z), wall))
    n = bays or max(3, round(w / 4.2))
    m_ = max(2, round(d / 4.2))
    cs = max(0.45, min(w, d) * 0.035)
    for i in range(n + 1):
        cx = -w / 2 + w * i / n
        for sy in (-1, 1):
            parts.append(box(f"{name}_c{i}{sy}", cs, cs, h, (cx, sy * (d / 2 - cs / 2), z), col))
    for j in range(1, m_):
        cy = -d / 2 + d * j / m_
        for sx in (-1, 1):
            parts.append(box(f"{name}_k{j}{sx}", cs, cs, h, (sx * (w / 2 - cs / 2), cy, z), col))
    parts.append(box(name + "_hb", w + 0.3, d + 0.3, max(0.4, h * 0.09), (0, 0, z + h - max(0.4, h * 0.09)), col))
    parts.append(box(name + "_tb", w + 0.3, d + 0.3, max(0.25, h * 0.05), (0, 0, z + h * 0.45), col))
    if doors:
        bw = w / n
        for i in range(n):
            if i == 0 or i == n - 1:
                continue
            cx = -w / 2 + bw * (i + 0.5)
            parts.append(box(f"{name}_d{i}", bw * 0.72, 0.25, h * 0.42, (cx, -d / 2 - 0.05, z), DARKW))
    body = join(parts, name + "_body")
    rh = roof_h or min(w, d) * 0.55
    zt = z + h
    rparts = []
    if mokoshi:
        rparts.append(eaved_roof(name + "_mk", w + 0.6, d + 0.6, max(1.2, h * 0.16), (0, 0, z + h * 0.42), roof_color, over=max(2.0, min(w, d) * 0.14), curve=0.12))
    if roof == "irimoya":
        rparts.append(irimoya(name + "_ir", w, d, rh, (0, 0, zt), roof_color, over=over, ridge=ridge, shibi=shibi))
    elif roof == "gable":
        rparts.append(seg_prism(name + "_ga", (-w / 2 - 1.2, 0), (w / 2 + 1.2, 0), zt, d + (over if over is not None else 2.4) * 2, rh, roof_color))
    else:
        rparts.append(hip(name + "_hp", w, d, rh, (0, 0, zt), roof_color, over=over, ridge=ridge, trim=trim, shibi=shibi))
    return body, join(rparts, name + "_roof")


def H(m, name, w, d, h, x=0.0, y=0.0, deg=0.0, z=0.0, sb=1, sr=2, **kw):
    body, roof = hall_parts(name, w, d, h, **kw)
    m.add(sb, put(body, x, y, deg, z), "halls")
    m.add(sr, put(roof, x, y, deg, z), "roofs")


def gate_parts(name, w, d, h1, h2, col=VERM, wall=WHITE, roof=TILE, base=1.0, roof_h=None, bays=5, top="irimoya", ridge=None, trim=None, shibi=None):
    """A two-storey gate (nijūmon / rōmon): open lower storey, pent eave, balconied upper storey, big top roof. Returns (body, roof)."""
    parts = [box(name + "_bs", w + 2.5, d + 2.5, base, (0, 0, 0), STONE)]
    z = base
    bw = w / bays
    cs = max(0.6, w * 0.026)
    for i in range(bays + 1):
        x = -w / 2 + i * bw
        for y in (-d / 2 + cs / 2, 0.0, d / 2 - cs / 2):
            parts.append(box(f"{name}_c{i}_{y:.0f}", cs, cs, h1, (x, y, z), col))
    for s in (-1, 1):
        parts.append(box(f"{name}_sw{s}", bw * 0.94, d * 0.94, h1 * 0.82, (s * (w / 2 - bw / 2), 0, z), wall))
    parts.append(box(name + "_dk", w - 2 * bw, d * 0.5, h1 * 0.86, (0, 0, z), DARK))
    parts.append(box(name + "_bm", w + 0.4, d + 0.4, h1 * 0.12, (0, 0, z + h1 * 0.88), col))
    zu = z + h1 + h1 * 0.3
    parts.append(box(name + "_bc", w * 0.9, d * 0.8, 0.5, (0, 0, zu - 0.1), col))
    for s in (-1, 1):
        parts.append(box(f"{name}_rx{s}", w * 0.9, 0.25, 0.9, (0, s * d * 0.39, zu + 0.4), col))
        parts.append(box(f"{name}_ry{s}", 0.25, d * 0.8, 0.9, (s * w * 0.44, 0, zu + 0.4), col))
    uw, ud = w * 0.84, d * 0.66
    parts.append(box(name + "_uw", uw, ud, h2, (0, 0, zu + 0.4), wall))
    for i in range(bays + 1):
        x = -uw / 2 + i * uw / bays
        for s in (-1, 1):
            parts.append(box(f"{name}_uc{i}{s}", cs * 0.8, cs * 0.8, h2, (x, s * (ud / 2 - cs * 0.4), zu + 0.4), col))
    for i in range(1, bays - 1):
        x = -uw / 2 + (i + 0.5) * uw / bays
        parts.append(box(f"{name}_ud{i}", uw / bays * 0.6, 0.2, h2 * 0.6, (x, -ud / 2 - 0.05, zu + 0.6), DARKW))
    parts.append(box(name + "_ub", uw + 0.3, ud + 0.3, h2 * 0.1, (0, 0, zu + 0.4 + h2 * 0.9), col))
    body = join(parts, name + "_body")
    rparts = [eaved_roof(name + "_le", w, d, h1 * 0.32, (0, 0, z + h1), roof, over=d * 0.32, curve=0.22)]
    rh = roof_h or d * 0.9
    if top == "irimoya":
        rparts.append(irimoya(name + "_tr", uw, ud, rh, (0, 0, zu + 0.4 + h2), roof, over=ud * 0.55, ridge=ridge, shibi=shibi))
    else:
        rparts.append(hip(name + "_tr", uw, ud, rh, (0, 0, zu + 0.4 + h2), roof, over=ud * 0.55, ridge=ridge, trim=trim, shibi=shibi))
    return body, join(rparts, name + "_roof")


def G(m, name, w, d, h1, h2, x=0.0, y=0.0, deg=0.0, z=0.0, sb=1, sr=2, **kw):
    body, roof = gate_parts(name, w, d, h1, h2, **kw)
    m.add(sb, put(body, x, y, deg, z), "halls")
    m.add(sr, put(roof, x, y, deg, z), "roofs")


def small_gate(name, w, d, h, col=VERM, roof=BARK, kind="gable"):
    """A one-storey gate on four or six posts with a gabled or hip-and-gable roof."""
    parts = []
    for sx in (-1, 0, 1):
        for sy in (-1, 1):
            parts.append(box(f"{name}_p{sx}{sy}", 0.6, 0.6, h, (sx * (w / 2 - 0.3), sy * (d / 2 - 0.3), 0), col))
    parts.append(box(name + "_b", w + 0.4, d + 0.4, 0.5, (0, 0, h - 0.5), col))
    if kind == "gable":
        parts.append(seg_prism(name + "_r", (0, -d / 2 - 1.5), (0, d / 2 + 1.5), h, w + 2.5, w * 0.4, roof))
    else:
        parts.append(irimoya(name + "_r", w, d, w * 0.5, (0, 0, h), roof, over=1.5))
    return join(parts, name)



# ---------------------------------------------------------------- Chang'an parts
import bpy

CHIWEI = "#4F5754"        # dark ceramic ridge-end fins of Tang halls


def _drop(o):
    bpy.data.objects.remove(o, do_unlink=True)


def hall_body(name, w, d, h, **kw):
    """hall_parts without its roof."""
    body, roof = hall_parts(name, w, d, h, roof="gable", roof_h=1.0, **kw)
    _drop(roof)
    return body


def balustrade(name, pts, h=1.0, color=STONE, post_every=3.5, closed=True, z=0.0):
    """A railing along a polyline: a top rail and posts."""
    if closed:
        pts = list(pts) + [pts[0]]
    parts = []
    for i in range(1, len(pts)):
        (ax, ay), (bx, by) = pts[i - 1], pts[i]
        L = math.hypot(bx - ax, by - ay)
        a = math.atan2(by - ay, bx - ax)
        parts.append(box(f"{name}_r{i}", L, 0.22, 0.18, ((ax + bx) / 2, (ay + by) / 2, z + h - 0.18), color, rot_z=a))
        parts.append(box(f"{name}_m{i}", L, 0.14, 0.12, ((ax + bx) / 2, (ay + by) / 2, z + h * 0.45), color, rot_z=a))
        n = max(1, round(L / post_every))
        for k in range(n):
            t = k / n
            parts.append(box(f"{name}_p{i}_{k}", 0.3, 0.3, h + 0.15, (ax + (bx - ax) * t, ay + (by - ay) * t, z), color))
    return join(parts, name)


def terrace(name, w, d, h, loc=(0, 0, 0), top=EARTH, face=BRICKF, batter=0.06, rail=False, rail_color=STONE):
    """A rammed-earth platform faced in brick: a battered block, a plinth course, a coping course and the beaten top."""
    x, y, z = loc
    b = h * batter
    parts = [frustum(name + "_core", w + 2 * b, d + 2 * b, w, d, h, (x, y, z), face)]
    parts.append(box(name + "_plinth", w + 2 * b + 0.4, d + 2 * b + 0.4, min(0.6, h * 0.1), (x, y, z), shade(face, -0.1)))
    ct = min(0.45, h * 0.08)
    parts.append(box(name + "_cope", w + 0.5, d + 0.5, ct, (x, y, z + h - ct), shade(face, 0.12)))
    parts.append(box(name + "_top", w - 0.3, d - 0.3, 0.05, (x, y, z + h), top))
    if rail:
        parts.append(balustrade(name + "_bal", [(x - w / 2 + 0.3, y - d / 2 + 0.3), (x + w / 2 - 0.3, y - d / 2 + 0.3), (x + w / 2 - 0.3, y + d / 2 - 0.3), (x - w / 2 + 0.3, y + d / 2 - 0.3)], 1.0, rail_color, 3.5, True, z + h))
    return join(parts, name)


def brackets(name, w, d, z, nw, nd, s=0.7, color=VERM):
    """Bracket sets (dougong) at the column heads round a w x d hall: block, arm thrust outward, block."""
    parts = []
    pos = []
    for i in range(nw + 1):
        x = -w / 2 + w * i / nw
        pos += [(x, -d / 2, 0, -1), (x, d / 2, 0, 1)]
    for j in range(1, nd):
        yy = -d / 2 + d * j / nd
        pos += [(-w / 2, yy, -1, 0), (w / 2, yy, 1, 0)]
    for k, (x, y, ox, oy) in enumerate(pos):
        parts.append(box(f"{name}_b{k}", s, s, s * 0.55, (x, y, z), color))
        if ox:
            parts.append(box(f"{name}_a{k}", s * 2.6, s * 0.5, s * 0.45, (x + ox * s * 0.9, y, z + s * 0.55), shade(color, -0.08)))
        else:
            parts.append(box(f"{name}_a{k}", s * 0.5, s * 2.6, s * 0.45, (x, y + oy * s * 0.9, z + s * 0.55), shade(color, -0.08)))
        parts.append(box(f"{name}_t{k}", s * 1.6, s * 1.6, s * 0.4, (x + ox * s * 1.4, y + oy * s * 1.4, z + s), color))
    return join(parts, name)


def tang_hall(m, name, w, d, h, x=0.0, y=0.0, deg=0.0, z=0.0, bays=None, roof="hip", roof_h=None, plat=1.0, over=None,
              shibi=CHIWEI, trim=GLAZE, ridge=None, col=VERM, wall=WHITE, mokoshi=False, bk=True, sb=1, sr=2, roof_color=TILE, plat_color=STONE, stairs=True):
    """A Tang hall: red columns, white walls, bracket sets, a low hipped (or hip-and-gable) roof with green-glazed trim and dark ridge-end fins."""
    n = bays or max(3, round(w / 5.0))
    body, rf = hall_parts(name, w, d, h, roof=roof, roof_h=roof_h or d * 0.42, roof_color=roof_color, col=col, wall=wall, plat=plat, bays=n,
                          over=over if over is not None else min(w, d) * 0.3, mokoshi=mokoshi, ridge=ridge or shade(roof_color, -0.25), trim=trim, shibi=shibi,
                          plat_color=plat_color, stairs=stairs)
    m.add(sb, put(body, x, y, deg, z), "halls")
    if bk:
        nd = max(2, round(d / 5.0))
        m.add(sb, put(brackets(name + "_bk", w + 0.4, d + 0.4, plat + h - max(0.4, h * 0.09) - 0.1, n, nd, max(0.45, min(w, d) * 0.028), shade(col, -0.05)), x, y, deg, z))
    m.add(sr, put(rf, x, y, deg, z), "roofs")


def lou(m, name, w, d, h1, h2, x=0.0, y=0.0, deg=0.0, z=0.0, plat=1.0, roof="irimoya", roof_h=None, roof_color=TILE, col=VERM, wall=WHITE,
        trim=None, shibi=None, ridge=None, bays=None, double_top=False, sb=1, sr=2, plat_color=STONE):
    """A two-storey tower hall: lower storey with a pent eave, a balcony, an upper storey and its roof."""
    n = bays or max(3, round(w / 4.5))
    b1 = hall_body(name + "_l", w, d, h1, plat=plat, col=col, wall=wall, bays=n, plat_color=plat_color, stairs=plat > 0.5)
    z1 = plat + h1
    ph = max(1.2, h1 * 0.32)
    pent = eaved_roof(name + "_pent", w + 0.4, d + 0.4, ph, (0, 0, z1), roof_color, over=max(1.2, min(w, d) * 0.13), curve=0.26)
    uw, ud = w * 0.84, d * 0.8
    zu = z1 + ph * 0.6
    bal = [box(name + "_bal", uw + 2.2, ud + 2.2, 0.4, (0, 0, zu), shade(col, -0.1))]
    bal.append(balustrade(name + "_rail", rect_pts(uw + 2.0, ud + 2.0), 1.0, col, 2.5, True, zu + 0.4))
    b2 = hall_body(name + "_u", uw, ud, h2, plat=0, col=col, wall=wall, bays=n, doors=False)
    parts_r = [pent]
    rh = roof_h or min(uw, ud) * 0.55
    zt = zu + 0.4 + h2
    if double_top:
        parts_r.append(eaved_roof(name + "_dt", uw + 0.4, ud + 0.4, rh * 0.32, (0, 0, zt), roof_color, over=min(uw, ud) * 0.16, curve=0.26))
        b2u = box(name + "_drum", uw * 0.86, ud * 0.86, rh * 0.3, (0, 0, zt + rh * 0.1), shade(col, -0.15))
        parts_r.append(b2u)
        zt += rh * 0.38
    if roof == "irimoya":
        parts_r.append(irimoya(name + "_top", uw * (0.86 if double_top else 1), ud * (0.86 if double_top else 1), rh, (0, 0, zt), roof_color, over=min(uw, ud) * 0.2, ridge=ridge, shibi=shibi))
    else:
        parts_r.append(hip(name + "_top", uw * (0.86 if double_top else 1), ud * (0.86 if double_top else 1), rh, (0, 0, zt), roof_color, over=min(uw, ud) * 0.2, ridge=ridge, trim=trim, shibi=shibi))
    m.add(sb, put(b1, x, y, deg, z), "halls")
    m.add(sb, put(join(bal, name + "_balc"), x, y, deg, z))
    m.add(sb, put(b2, x, y, deg, z + zu + 0.4))
    m.add(sr, put(join(parts_r, name + "_roofs"), x, y, deg, z), "roofs")
    return zt + rh


def walled(name, W, D, h=3.2, t=1.4, gaps=(("S", 0.0, 10.0),), color=CLAY, cap=TILE, x=0.0, y=0.0):
    """A rectangular earth wall with openings: gaps = [(side, offset along side, width)]."""
    sides = dict(S=((-W / 2, -D / 2), (W / 2, -D / 2)), N=((-W / 2, D / 2), (W / 2, D / 2)), W=((-W / 2, -D / 2), (-W / 2, D / 2)), E=((W / 2, -D / 2), (W / 2, D / 2)))
    parts = []
    for s, ((ax, ay), (bx, by)) in sides.items():
        L = math.hypot(bx - ax, by - ay)
        cuts = sorted((off + L / 2 - gw / 2, off + L / 2 + gw / 2) for side, off, gw in gaps if side == s)
        t0 = 0.0
        for k, (c0, c1) in enumerate(cuts + [(L, L)]):
            if c0 - t0 > 0.5:
                p = (ax + (bx - ax) * t0 / L + x, ay + (by - ay) * t0 / L + y)
                q = (ax + (bx - ax) * c0 / L + x, ay + (by - ay) * c0 / L + y)
                parts.append(wall_line(f"{name}_{s}{k}", [p, q], h, t, color, cap))
            t0 = c1
    return join(parts, name)


def gate_platform(name, w, d, h, passages, pw, face=BRICKF, top=EARTH, ph=None, crenel=True):
    """A Tang city gate's base: a battered, brick-faced earth block with flat-topped (trapezoidal) passages on both faces."""
    parts = [terrace(name + "_blk", w, d, h, (0, 0, 0), top, face, batter=0.05)]
    ph = ph or h * 0.66
    b = h * 0.05
    gap = max(2.5, (w * 0.7 - passages * pw) / max(1, passages - 1))
    total = passages * pw + (passages - 1) * gap
    for i in range(passages):
        cx = -total / 2 + pw / 2 + i * (pw + gap)
        for s in (-1, 1):
            yy = s * (d / 2 + b * 0.5 - 0.05)
            parts.append(box(f"{name}_p{i}{s}", pw, b + 0.5, ph * 0.78, (cx, yy, 0), DARK))
            parts.append(frustum(f"{name}_pt{i}{s}", pw, b + 0.5, pw * 0.55, b + 0.5, ph * 0.22, (cx, yy, ph * 0.78), DARK))
        parts.append(box(f"{name}_road{i}", pw * 0.9, d + 2 * b + 1.0, 0.06, (cx, 0, 0), shade(EARTH, -0.12)))
    if crenel:
        parts.append(merlons(name + "_mer", w - 1.0, d - 1.0, h, size=0.9, gap=1.2, color=shade(face, 0.04)))
    return join(parts, name)


def tang_gate(m, name, w, d, h, passages, pw, hall_w, hall_d, hall_h, bays, x=0.0, y=0.0, deg=0.0, roof_h=None, wall_len=0.0, wall_h=None,
              ramps=False, sb=0, sh=1, sr=2):
    """A Tang gate: platform with passages, a hall on top, stubs of wall to either side and optional ramps up the inner face."""
    m.add(sb, put(gate_platform(name + "_plat", w, d, h, passages, pw), x, y, deg), "gates")
    wh = wall_h or h * 0.92
    if wall_len > w / 2:
        for s in (-1, 1):
            seg = terrace(f"{name}_wall{s}", wall_len - w / 2, d * 0.62, wh, (s * (w / 2 + (wall_len - w / 2) / 2), 0, 0), EARTH, shade(BRICKF, 0.04), batter=0.08)
            m.add(sb, put(seg, x, y, deg))
            mer = merlons(f"{name}_wm{s}", wall_len - w / 2 - 1.0, d * 0.62 - 1.0, wh, 0.8, 1.2, shade(BRICKF, 0.06))
            m.add(sb, put(move(mer, s * (w / 2 + (wall_len - w / 2) / 2)), x, y, deg))
            if ramps:
                L = min(wall_len - w / 2 - 4, wh * 3.2)
                x0 = s * (w / 2 + 2)
                x1 = x0 + s * L
                yy = d * 0.31 + 3.5
                verts = [(x0, yy - 3, wh), (x0, yy + 3, wh), (x1, yy + 3, 0), (x1, yy - 3, 0), (x0, yy - 3, 0), (x0, yy + 3, 0)]
                faces = [(0, 1, 2, 3), (4, 5, 1, 0), (3, 4, 0), (5, 2, 1), (3, 2, 5, 4)]
                m.add(sb, put(mesh_from(f"{name}_ramp{s}", verts, faces, (0, 0, 0), shade(BRICKF, 0.02)), x, y, deg))
    tang_hall(m, name + "_hall", hall_w, hall_d, hall_h, x, y, deg, z=h, bays=bays, roof="hip", roof_h=roof_h, plat=0.8, sb=sh, sr=sr, stairs=False)


def tree_row(m, name, a, b, n, r=3.0, color=LOCUST, stage=2, z=0.0):
    (ax, ay), (bx, by) = a, b
    pts = [(ax + (bx - ax) * i / max(1, n - 1), ay + (by - ay) * i / max(1, n - 1), z) for i in range(n)]
    m.add(stage, grove(name, pts, r, color), "trees")


def trees(m, name, pts, r=4.5, color=PINE, stage=2):
    m.add(stage, grove(name, [(x, y, 0) for x, y in pts], r, color), "trees")


def tpagoda(name, w, storeys, total_h, roof=TILE, col=VERM, wall=WHITE, spire_frac=0.22, taper=0.9, over=0.42):
    """A Tang timber pagoda: square storeys of white walls and red posts under wide grey eaves, a bronze finial."""
    trim = shade(col, -0.1)
    base = max(1.2, w * 0.14)
    parts = [box(name + "_base", w * 1.5, w * 1.5, base, (0, 0, 0), STONE)]
    sh = (total_h * (1 - spire_frac) - base) / storeys
    z, ww = base, w
    for i in range(storeys):
        bh = sh * 0.6
        if i:
            parts.append(box(f"{name}_bal{i}", ww * 1.16, ww * 1.16, 0.4, (0, 0, z), trim))
        parts.append(box(f"{name}_s{i}", ww, ww, bh, (0, 0, z), wall))
        for sx in (-1, 1):
            for sy in (-1, 1):
                parts.append(box(f"{name}_p{i}{sx}{sy}", ww * 0.09, ww * 0.09, bh, (sx * ww * 0.455, sy * ww * 0.455, z), col))
        parts.append(box(f"{name}_dr{i}", ww * 0.3, ww * 1.01, bh * 0.55, (0, 0, z + bh * 0.08), DARKW))
        parts.append(box(f"{name}_dr2{i}", ww * 1.01, ww * 0.3, bh * 0.55, (0, 0, z + bh * 0.08), DARKW))
        parts.append(box(f"{name}_br{i}", ww * 1.22, ww * 1.22, sh * 0.1, (0, 0, z + bh), trim))
        parts.append(eaved_roof(f"{name}_r{i}", ww * 1.22, ww * 1.22, sh * 0.3, (0, 0, z + bh + sh * 0.1), roof, over=ww * over, curve=0.28))
        z += sh
        ww *= taper
    sp = total_h - z
    parts.append(cylinder(name + "_spire", max(0.15, w * 0.03), sp * 0.95, (0, 0, z - sh * 0.1), BRONZE, verts=8))
    for k in range(7):
        parts.append(cylinder(f"{name}_ring{k}", max(0.5, w * 0.1) * (1 - k * 0.05), 0.25, (0, 0, z + sp * (0.12 + k * 0.08)), BRONZE, verts=10))
    parts.append(dome(name + "_jewel", max(0.3, w * 0.045), (0, 0, z + sp * 0.92), GILT, segments=10, rings=6))
    return join(parts, name)


def shop_row(name, x0, x1, y, depth, h, unit=18.0, face=-1, roof=TILE, wall=CLAY, awning="#8C6A4A", doors=True, posts=True):
    """Shops in a row along X between x0 and x1, fronts toward face (-1 south, +1 north): units under gabled roofs, an awning along the front."""
    parts = []
    n = max(1, round((x1 - x0) / unit))
    u = (x1 - x0) / n
    for i in range(n):
        cx = x0 + u * (i + 0.5)
        hh = h * (0.9 + 0.2 * ((i * 7) % 5) / 5)
        parts.append(box(f"{name}_u{i}", u - 0.8, depth, hh, (cx, y, 0), shade(wall, 0.04 * ((i % 3) - 1))))
        parts.append(seg_prism(f"{name}_r{i}", (cx - u / 2 + 0.2, y), (cx + u / 2 - 0.2, y), hh, depth + 1.2, depth * 0.32, shade(roof, 0.05 * ((i % 2) - 0.5))))
        if doors:
            parts.append(box(f"{name}_d{i}", u * 0.6, 0.2, hh * 0.6, (cx, y + face * (depth / 2 + 0.05), 0), DARKW))
    parts.append(box(name + "_aw", x1 - x0, 2.4, 0.25, ((x0 + x1) / 2, y + face * (depth / 2 + 1.2), h * 0.62), awning))
    if posts:
        for i in range(n + 1):
            parts.append(box(f"{name}_ap{i}", 0.25, 0.25, h * 0.62, (x0 + u * i, y + face * (depth / 2 + 2.2), 0), WOOD))
    return join(parts, name)


def yard_houses(name, cx, cy, w, d, h=4.0, wall=CLAY, roof=TILE, seed=0):
    """A courtyard compound: four ranges round a yard."""
    t = min(w, d) * 0.28
    parts = []
    for k, (px, py, pw, pd, ax) in enumerate(((cx, cy + d / 2 - t / 2, w, t, "x"), (cx, cy - d / 2 + t / 2, w, t, "x"),
                                               (cx - w / 2 + t / 2, cy, t, d - 2 * t, "y"), (cx + w / 2 - t / 2, cy, t, d - 2 * t, "y"))):
        hh = h * (1.0 if k == 0 else 0.85)
        parts.append(box(f"{name}_b{k}", pw, pd, hh, (px, py, 0), shade(wall, 0.03 * ((k + seed) % 3 - 1))))
        if ax == "x":
            parts.append(seg_prism(f"{name}_r{k}", (px - pw / 2 - 0.4, py), (px + pw / 2 + 0.4, py), hh, pd + 1.0, pd * 0.35, roof))
        else:
            parts.append(seg_prism(f"{name}_r{k}", (px, py - pd / 2 - 0.4), (px, py + pd / 2 + 0.4), hh, pw + 1.0, pw * 0.35, roof))
    return join(parts, name)


# ================================================================ Dunhuang

RAM = "#D9BF8E"           # rammed loess, fresh
RAM_D = "#BBA176"         # the shadowed line between courses
RAM_OLD = "#C2AC86"       # weathered
SAND = "#DCC79E"
GROUND = "#CBBD9A"
CLIFF = "#C4A87F"         # Mogao conglomerate
CLIFF_D = "#A88C68"
POPLAR = "#7C9455"
ELM = "#6E8A4E"
REED = "#AAA96C"
TAMARISK = "#9C8A6A"
FELT = "#D9CDB4"
CAMEL = "#B08A5C"
MUD = "#BFA47C"
PLANK = "#8A6C4E"
FLAME = "#D9822B"


# ---------------------------------------------------------------- small parts

def poplar(name, x, y, h=12.0, r=1.5, color=POPLAR, z=0.0):
    """A Lombardy-like oasis poplar: a thin trunk and a tall narrow crown."""
    return join([cylinder(name + "_t", 0.22, h * 0.3, (x, y, z), BARK, verts=5),
                 cylinder(name + "_c", r, h * 0.82, (x, y, z + h * 0.18), color, verts=7, r_top=r * 0.12)], name)


def elm(name, x, y, r=3.0, z=0.0):
    return tree(name, r, (x, y, z), ELM)


def shrub(name, x, y, r=1.2, color=TAMARISK, z=0.0):
    return dome(name, r, (x, y, z), color, squash=0.7, segments=7, rings=3)


def seg(name, a, b, h, tb, tt, color, z=0.0, ext=0.0):
    """A battered rammed-earth wall from a to b: base thickness tb, top tt, ends extended by ext."""
    (ax, ay), (bx, by) = a, b
    L = math.hypot(bx - ax, by - ay) + 2 * ext
    o = frustum(name, L, tb, L, tt, h, (0, 0, 0), color)
    o = rot(o, math.degrees(math.atan2(by - ay, bx - ax)))
    return move(o, (ax + bx) / 2, (ay + by) / 2, z)


def courses(name, a, b, h, tb, tt, step=1.4, color=RAM_D, z=0.0, ext=0.0, top=None):
    """The horizontal lines of rammed-earth courses: thin bands round a battered wall every step metres."""
    (ax, ay), (bx, by) = a, b
    L = math.hypot(bx - ax, by - ay) + 2 * ext
    ang = math.atan2(by - ay, bx - ax)
    out = []
    zz = step
    while zz < (top or h) - 0.4:
        t = tb - (tb - tt) * zz / h
        out.append(box(f"{name}{int(zz * 10)}", L, t + 0.16, 0.16, ((ax + bx) / 2, (ay + by) / 2, z + zz), color, rot_z=ang))
        zz += step
    return join(out, name) if out else None


def crenels(name, a, b, h, tt, side, color=RAM, every=2.2):
    """Merlons along the outer edge of a wall top; side = +1 right of a->b, -1 left."""
    (ax, ay), (bx, by) = a, b
    L = math.hypot(bx - ax, by - ay)
    ang = math.atan2(by - ay, bx - ax)
    ux, uy = (bx - ax) / L, (by - ay) / L
    nx, ny = uy * side, -ux * side
    off = tt / 2 - 0.4
    n = max(1, int(L / every))
    out = []
    for i in range(n):
        u = (i + 0.5) * L / n
        out.append(box(f"{name}{i}", 1.3, 0.8, 1.4, (ax + ux * u + nx * off, ay + uy * u + ny * off, h), color, rot_z=ang))
    out.append(box(name + "_lip", L, 0.8, 0.5, ((ax + bx) / 2 + nx * off, (ay + by) / 2 + ny * off, h), color, rot_z=ang))
    return join(out, name)


def earth_wall(m, name, pts, h, tb, tt, color=RAM, stage=0, crenel=True, step=1.4):
    """Rammed-earth wall along a polyline whose outside is on the right of the direction of travel."""
    for i in range(1, len(pts)):
        a, b = pts[i - 1], pts[i]
        m.add(stage, seg(f"{name}{i}", a, b, h, tb, tt, color, ext=tt / 2), "walls")
        c = courses(f"{name}{i}c", a, b, h, tb, tt, step, shade(color, -0.12), ext=tt / 2 - 0.1)
        if c:
            m.add(stage, c)
        if crenel:
            m.add(stage, crenels(f"{name}{i}m", a, b, h, tt, 1, color))
            m.add(stage, crenels(f"{name}{i}n", a, b, h, tt, -1, color, every=9.0))


def bastion(name, x, y, w, out, h, normal=(0, -1), color=RAM, step=1.4, top_tower=False):
    """A projecting 'horse-face' bastion: battered earth block with courses, centred on its wall-face midpoint (x, y)."""
    parts = [frustum(name + "_b", w, out * 2, w - 1.4, out * 2 - 1.4, h, (0, -out / 2, 0), color)]
    zz = step
    while zz < h - 0.4:
        k = 1.4 * zz / h
        parts.append(box(f"{name}_c{int(zz * 10)}", w - k + 0.16, out * 2 - k + 0.16, 0.16, (0, -out / 2, zz), shade(color, -0.12)))
        zz += step
    n = max(2, int(w / 2.6))
    for i in range(n):
        parts.append(box(f"{name}_m{i}", 1.2, 0.8, 1.4, (-w / 2 + 0.7 + (w - 1.4) * (i + 0.5) / n, -out * 1.5 + 0.7 + 0.4, h), color))
    o = join(parts, name)
    o = rot(o, math.degrees(math.atan2(normal[0], -normal[1])))
    return move(o, x, y, 0)


def passage(name, w, h, depth, loc, color=DARK):
    """A flat-topped (trapezoidal) gate passage, Tang fashion: a dark panel with sloping shoulders."""
    x, y, z = loc
    return join([box(name + "_r", w, depth, h * 0.74, (x, y, z), color),
                 frustum(name + "_t", w, depth, w * 0.5, depth, h * 0.26, (x, y, z + h * 0.74), color)], name)


def earth_gate(m, name, x, y, w, d, h, pw, ph, stage=0, color=RAM):
    """A rammed-earth gate block with one passage through it (N-S), coursed, crenellated."""
    m.add(stage, frustum(name, w + 1.2, d + 1.2, w, d, h, (x, y, 0), color), "gates")
    zz = 1.4
    parts = []
    while zz < h - 0.4:
        k = 1.2 * (1 - zz / h)
        parts.append(box(f"{name}_c{int(zz * 10)}", w + k + 0.16, d + k + 0.16, 0.16, (x, y, zz), shade(color, -0.12)))
        zz += 1.4
    parts.append(passage(name + "_ps", pw, ph, d + 1.6, (x, y, 0)))
    parts.append(box(name + "_rd", pw * 0.9, d + 6, 0.08, (x, y, 0), shade(GROUND, -0.1)))
    m.add(stage, join(parts, name + "_det"))


def ramp_up(name, x0, x1, y0, y1, z0, z1, color=RAM):
    """A solid ramp of width y0..y1 rising along X from (x0, z0) to (x1, z1)."""
    verts = [(x0, y0, 0), (x0, y1, 0), (x1, y1, 0), (x1, y0, 0), (x0, y0, z0), (x0, y1, z0), (x1, y1, z1), (x1, y0, z1)]
    faces = [(0, 3, 2, 1), (4, 5, 6, 7), (0, 1, 5, 4), (2, 3, 7, 6), (1, 2, 6, 5), (3, 0, 4, 7)]
    return mesh_from(name, verts, faces, (0, 0, 0), color)


def flat_yard(name, cx, cy, w, d, h=3.4, color=MUD, door=-1):
    """A courtyard house of earth: four flat-roofed ranges with a parapet lip round an open yard, a dark gate."""
    t = min(w, d) * 0.3
    parts = []
    for k, (px, py, pw, pd) in enumerate(((cx, cy + d / 2 - t / 2, w, t), (cx, cy - d / 2 + t / 2, w, t),
                                           (cx - w / 2 + t / 2, cy, t, d - 2 * t), (cx + w / 2 - t / 2, cy, t, d - 2 * t))):
        hh = h * (1.0 if k == 0 else 0.85)
        c = shade(color, 0.04 * ((k * 3 + int(cx)) % 3 - 1))
        parts.append(box(f"{name}_b{k}", pw, pd, hh, (px, py, 0), c))
        parts.append(box(f"{name}_p{k}", pw + 0.2, pd + 0.2, 0.3, (px, py, hh), shade(c, -0.06)))
    parts.append(box(name + "_g", 1.6, 0.25, 2.2, (cx, cy + door * (d / 2 + 0.05), 0), DARKW))
    parts.append(box(name + "_y", w - 2 * t, d - 2 * t, 0.06, (cx, cy, 0), shade(GROUND, -0.06)))
    return join(parts, name)


def hut(name, x, y, w, d, h=3.0, color=MUD, deg=0.0):
    o = join([box(name + "_b", w, d, h, (0, 0, 0), color), box(name + "_r", w + 0.4, d + 0.4, 0.35, (0, 0, h), shade(color, -0.1)),
              box(name + "_d", 1.0, 0.2, 1.9, (0, -d / 2 - 0.05, 0), DARKW)], name)
    if deg:
        o = rot(o, deg)
    return move(o, x, y, 0)


def yurt(name, x, y, r=2.6):
    return join([cylinder(name + "_w", r, 1.6, (x, y, 0), FELT, verts=12),
                 dome(name + "_r", r * 1.02, (x, y, 1.6), shade(FELT, -0.06), squash=0.45, segments=12, rings=4),
                 box(name + "_d", 0.9, 0.3, 1.3, (x, y - r, 0), "#8C4A32")], name)


def camel(name, x, y, deg=0.0, color=CAMEL, loaded=False):
    parts = [box(name + "_b", 2.0, 0.8, 0.85, (0, 0, 1.25), color)]
    for s in (-0.45, 0.45):
        parts.append(dome(f"{name}_h{s}", 0.36, (s, 0, 2.05), shade(color, -0.05), segments=6, rings=3))
    for sx in (-0.75, 0.75):
        for sy in (-0.25, 0.25):
            parts.append(box(f"{name}_l{sx}{sy}", 0.18, 0.18, 1.25, (sx, sy, 0), shade(color, -0.1)))
    parts.append(box(name + "_n", 0.3, 0.3, 1.0, (1.15, 0, 1.6), color))
    parts.append(box(name + "_hd", 0.6, 0.28, 0.3, (1.35, 0, 2.5), color))
    if loaded:
        for s in (-1, 1):
            parts.append(box(f"{name}_pk{s}", 0.9, 0.5, 0.7, (0, s * 0.62, 1.4), "#C9B48A"))
    o = join(parts, name)
    if deg:
        o = rot(o, deg)
    return move(o, x, y, 0)


def ground(name, w, d, color=GROUND):
    return box(name, w, d, 0.3, (0, 0, 0), color)


def drift(name, x, y, w, d, h, color=SAND):
    """A sand drift heaped against a wall: a low frustum."""
    return frustum(name, w, d, w * 0.5, d * 0.2, h, (x, y, 0), color)


# ---------------------------------------------------------------- the town walls (hero)

GATE_X, WALL_Y, CORNER = 170.0, -38.0, (-195.0, -38.0)


def shazhou_gate(variant="tang"):
    """The south-west corner of the town and the south gate. Footprint 420 x 130: wall face at y = -38, corner at x = -195."""
    m = Model("shazhou-gate")
    han, ruin = variant == "han", variant == "ruin"
    m.add(0, ground("sg_ground", 420, 130), "ground")
    H, TB, TT = (8.0, 7.0, 4.0) if han else (10.0, 9.0, 5.0)
    gw = 30.0 if han else 34.0
    cx, cy = CORNER
    west = [(cx, 62.0), (cx, cy)]
    south1 = [(cx, cy), (GATE_X - gw / 2, cy)]
    south2 = [(GATE_X + gw / 2, cy), (210.0, cy)]
    if not ruin:
        earth_wall(m, "sg_w", west, H, TB, TT)
        earth_wall(m, "sg_s", south1, H, TB, TT)
        earth_wall(m, "sg_e", south2, H, TB, TT)
    else:
        # slumped ridges with breaches; heights wander
        chunks = [((cx, 62), (cx, 30), 6.5), ((cx, 22), (cx, -10), 8.0), ((cx, -14), (cx, cy), 5.5),
                  ((cx, cy), (-150, cy), 7.5), ((-140, cy), (-80, cy), 5.0), ((-68, cy), (10, cy), 8.5), ((22, cy), (90, cy), 4.5),
                  ((100, cy), (GATE_X - gw / 2 - 2, cy), 6.0), ((GATE_X + gw / 2 + 4, cy), (210, cy), 5.5)]
        for i, (a, b, hh) in enumerate(chunks):
            m.add(0, seg(f"sg_r{i}", a, b, hh, 9.5, 2.5, RAM_OLD), "walls")
            m.add(0, courses(f"sg_rc{i}", a, b, hh, 9.5, 2.5, 1.4, shade(RAM_OLD, -0.12)))
            mx, my = (a[0] + b[0]) / 2, (a[1] + b[1]) / 2
            vertical = abs(a[0] - b[0]) < 1
            L = math.hypot(b[0] - a[0], b[1] - a[1])
            m.add(0, drift(f"sg_dr{i}", mx + (-6 if vertical else 0), my + (0 if vertical else -6), 6 if vertical else L * 0.8, L * 0.8 if vertical else 6, 2.2))
    # bastions on the outer faces
    if not han:
        for i, bx in enumerate((-140.0, -90.0, -40.0, 10.0, 60.0, 110.0)):
            if ruin and i % 2:
                continue
            m.add(0, bastion(f"sg_bs{i}", bx, cy - TB / 2 + 0.6, 12.0, 8.0, H - (2.5 if ruin else 0), (0, -1), RAM_OLD if ruin else RAM))
        for i, by in enumerate((10.0, 50.0)):
            m.add(0, bastion(f"sg_bw{i}", cx - TB / 2 + 0.6, by, 12.0, 8.0, H - (3 if ruin else 0), (-1, 0), RAM_OLD if ruin else RAM))
    # the corner: a broad square bastion carrying a corner tower
    ch = H + (1.5 if not ruin else -1.0)
    cs = 16.0 if han else 22.0
    ccx, ccy = cx - 3.0, cy - 3.0
    col = RAM_OLD if ruin else RAM
    m.add(0, frustum("sg_corner", cs + 1.4, cs + 1.4, cs, cs, ch, (ccx, ccy, 0), col), "walls")
    m.add(0, join([box(f"sg_cc{k}", cs + 1.4 * (1 - k * 1.4 / ch) + 0.16, cs + 1.4 * (1 - k * 1.4 / ch) + 0.16, 0.16, (ccx, ccy, k * 1.4), shade(col, -0.12))
                   for k in range(1, int(ch / 1.4))], "sg_ccourses"))
    if not ruin:
        m.add(0, move(merlons("sg_cmer", cs - 0.8, cs - 0.8, ch, 1.2, 1.4, col), ccx, ccy, 0))
        if han:
            # a plain timber lookout on posts
            for sx in (-1, 1):
                for sy in (-1, 1):
                    m.add(1, box(f"sg_lp{sx}{sy}", 0.5, 0.5, 4.5, (ccx + sx * 3, ccy + sy * 3, ch), WOOD), "towers")
            m.add(1, box("sg_lfl", 7.4, 7.4, 0.4, (ccx, ccy, ch + 2.2), WOOD))
            m.add(2, hip("sg_lroof", 6.6, 6.6, 2.4, (ccx, ccy, ch + 4.5), TILE, over=1.2), "roofs")
        else:
            lou(m, "sg_jiaolou", 11.0, 11.0, 4.2, 3.6, ccx, ccy, 0.0, ch, plat=0.4, roof="hip", sb=1, sr=2, bays=3)
    # the gate
    gd = TB + 7.0
    gh = H + 0.5
    if ruin:
        m.add(0, frustum("sg_gate", gw + 3, gd + 3, gw - 6, gd - 5, gh - 3.0, (GATE_X, cy, 0), RAM_OLD), "gates")
        m.add(0, passage("sg_gps", 6.5, 5.0, gd + 4, (GATE_X, cy, 0)))
        m.add(0, drift("sg_gdr", GATE_X - 9, cy - gd / 2 - 3, 12, 6, 2.4))
        for i in range(3):
            m.add(1, cylinder(f"sg_stump{i}", 0.35, 1.2 + i * 0.5, (GATE_X - 6 + i * 6, cy + 2, gh - 3.0), DARKW, verts=6), "timbers")
    else:
        earth_gate(m, "sg_gate", GATE_X, cy, gw, gd, gh, 6.0 if han else 7.0, 6.0 if han else 7.5, 0, RAM)
        m.add(0, move(merlons("sg_gmer", gw - 1.0, gd - 1.0, gh, 1.2, 1.4, RAM), GATE_X, cy, 0))
        if han:
            body, roof = hall_parts("sg_gt", 16.0, 8.0, 4.0, roof="hip", roof_h=3.2, plat=0.4, bays=3, col=WOOD, wall=shade(RAM, 0.1), over=2.0, stairs=False)
            m.add(1, put(body, GATE_X, cy, 0.0, gh), "towers")
            m.add(2, put(roof, GATE_X, cy, 0.0, gh), "roofs")
        else:
            lou(m, "sg_gt", 20.0, 11.0, 4.8, 4.0, GATE_X, cy, 0.0, gh, plat=0.4, roof="hip", sb=1, sr=2, bays=5)
            # barbican in front, opening to the east
            bbs = [[(GATE_X + 22, -43.0), (GATE_X + 22, -46.0)], [(GATE_X + 22, -53.0), (GATE_X + 22, -59.0), (GATE_X - 22, -59.0), (GATE_X - 22, -43.0)]]
            for j, bb in enumerate(bbs):
                for i in range(1, len(bb)):
                    m.add(1, seg(f"sg_bb{j}{i}", bb[i - 1], bb[i], 7.5, 5.0, 3.0, RAM, ext=1.5 if i > 1 or j == 0 else 0.0))
                    m.add(1, courses(f"sg_bbc{j}{i}", bb[i - 1], bb[i], 7.5, 5.0, 3.0, 1.4, RAM_D, ext=1.4 if i > 1 or j == 0 else 0.0))
                    m.add(1, crenels(f"sg_bbm{j}{i}", bb[i - 1], bb[i], 7.5, 3.0, -1, RAM))
        # ramp up the inside of the wall beside the gate
        m.add(0, ramp_up("sg_ramp", GATE_X - gw / 2 - 40, GATE_X - gw / 2 - 2, cy + TB / 2 - 0.5, cy + TB / 2 + 4.5, 0.0, H, shade(RAM, 0.03)))
    # inside the corner: houses, lanes and poplars (none left in the ruin)
    if not ruin:
        yards = [(-168, 4, 22, 18), (-168, 48, 22, 22), (-140, 16, 24, 22), (-140, 48, 24, 22), (-110, 10, 26, 20), (-110, 44, 26, 26),
                 (-80, 16, 24, 24), (-80, 50, 22, 18), (-50, 8, 26, 18), (-50, 42, 28, 26), (-18, 18, 24, 26), (-18, 52, 24, 16),
                 (12, 8, 24, 18), (12, 42, 26, 26), (44, 18, 26, 26), (44, 52, 24, 16), (76, 8, 26, 18), (76, 42, 26, 26),
                 (108, 16, 24, 24), (108, 50, 24, 18), (136, 10, 20, 18), (136, 44, 20, 24)] if not han else [(-150, 22, 30, 26), (-100, 30, 32, 28), (-40, 20, 30, 24), (40, 30, 28, 26), (100, 22, 30, 24)]
        for i, (x, y, w, d) in enumerate(yards):
            m.add(1, flat_yard(f"sg_y{i}", x, y, w, d, 3.4 + (i % 3) * 0.3), "houses")
        m.add(1, box("sg_street", 12, 90, 0.08, (GATE_X, cy + 50, 0), shade(GROUND, -0.1)))
        for i in range(22):
            x = -182 + i * 15.5
            m.add(2, poplar(f"sg_pp{i}", x, 28 + (i % 2) * 2.5, 11 + (i % 3), 1.4), "trees")
        for i, (x, y) in enumerate(((192, -2), (200, 30), (196, 58), (182, 60))):
            m.add(2, poplar(f"sg_pq{i}", x, y, 12, 1.4))
        m.add(1, box("sg_lane", 360, 5, 0.06, (-10, 28, 0), shade(GROUND, -0.1)))
        if not han:
            m.add(1, flat_yard("sg_guard", GATE_X - 30, -20, 16, 12, 3.6, MUD, -1))
    for i, (x, y) in enumerate(((-120, -58), (-60, -60), (0, -57), (60, -60), (110, -58), (205, -58))):
        m.add(2, (shrub if ruin else poplar)(f"sg_op{i}", x, y), "trees")
    if variant == "tang":
        for i in range(4):
            m.add(2, camel(f"sg_cm{i}", GATE_X - 30 - i * 4.5, -52.0, 0.0, loaded=True))
    return m


# ---------------------------------------------------------------- the yamen

def yamen(variant="tang"):
    """The governor's compound: gate hall, main hall, rear hall, side ranges in a rammed-earth enclosure. Footprint 130 x 150."""
    m = Model("yamen")
    han = variant == "han"
    m.add(0, ground("ym_g", 130, 150), "ground")
    W, D = 124.0, 144.0
    wall_h = 5.5 if han else 4.5
    m.add(0, walled("ym_wall", W, D, wall_h, 2.2, (("S", 0.0, 12.0),), RAM, shade(RAM, -0.15) if han else TILE), "walls")
    m.add(0, box("ym_axis", 8, D - 6, 0.1, (0, 0, 0), shade(GROUND, -0.12)))
    # gate hall
    tang_hall(m, "ym_gate", 22, 10, 4.5, 0, -D / 2 + 6, bays=5, roof="hip", plat=0.8, sb=1, sr=2, trim=None if han else GLAZE, bk=not han,
              shibi=None if han else CHIWEI, wall=shade(RAM, 0.12) if han else WHITE, col=WOOD if han else VERM)
    # inner gate wall dividing the courts
    m.add(0, walled("ym_inner", W - 14, 70, 3.2, 1.2, (("S", 0.0, 10.0), ("N", 0.0, 8.0)), CLAY, TILE, 0, 22), "walls")
    tang_hall(m, "ym_main", 32, 17, 6.0, 0, 18, bays=7, roof="hip", plat=1.6, sb=1, sr=2, trim=None if han else GLAZE, bk=not han,
              shibi=None if han else CHIWEI, wall=shade(RAM, 0.12) if han else WHITE, col=WOOD if han else VERM)
    tang_hall(m, "ym_rear", 26, 13, 4.8, 0, 50, bays=5, roof="hip", plat=1.0, sb=1, sr=2, trim=None, bk=False,
              wall=shade(RAM, 0.12) if han else WHITE, col=WOOD if han else VERM)
    for s in (-1, 1):
        for k, yy in enumerate((-30, 18)):
            body, roof = hall_parts(f"ym_side{s}{k}", 9, 34 if k else 26, 3.6, roof="gable", roof_h=2.6, plat=0.6, bays=2, col=WOOD, wall=shade(RAM, 0.14), over=1.4, doors=False, stairs=False)
            m.add(1, put(body, s * 44, yy, 0.0), "halls")
            m.add(2, put(roof, s * 44, yy, 0.0), "roofs")
    if han:
        # a Han watchtower of several storeys, like the pottery tower models from Han tombs
        tx, ty = 46, 58
        z = 0.0
        for i, (w, h) in enumerate(((9, 4.5), (7.5, 4.0), (6, 3.5))):
            m.add(1, box(f"ym_tw{i}", w, w, h, (tx, ty, z), shade(RAM, 0.1)), "tower")
            m.add(1, box(f"ym_twb{i}", w + 1.6, w + 1.6, 0.4, (tx, ty, z + h), WOOD))
            m.add(2, hip(f"ym_twr{i}", w, w, 1.6, (tx, ty, z + h + 0.4), TILE, over=1.4))
            z += h + 1.6
        for i, (x, y) in enumerate(((-45, -55), (45, -55), (-50, 52), (-30, 62))):
            m.add(2, elm(f"ym_t{i}", x, y, 3.2), "trees")
    else:
        # a drum tower over the gate court and the archive
        lou(m, "ym_drum", 10, 10, 4.0, 3.4, -46, 58, 0.0, 0.0, plat=1.2, roof="hip", bays=3, sb=1, sr=2)
        for i, (x, y) in enumerate(((-20, -40), (20, -40), (-20, -8), (20, -8), (-40, 40), (40, 40), (48, 62), (-30, 64))):
            m.add(2, (elm if i < 4 else poplar)(f"ym_t{i}", x, y), "trees")
    if variant == "guiyi":
        for s in (-1, 1):
            m.add(2, box(f"ym_flag{s}", 0.3, 0.3, 10, (s * 8, -D / 2 - 1, 0), WOOD))
            m.add(2, box(f"ym_flagc{s}", 2.4, 0.1, 1.6, (s * 8 + 1.2, -D / 2 - 1, 8), "#A8402C"))
    return m


# ---------------------------------------------------------------- monasteries

def monastery(kind="kaiyuan"):
    """A walled monastery 100 x 130: gate, pagoda or library, main hall, rear hall, cloisters."""
    m = Model(kind)
    m.add(0, ground("ms_g", 100, 130), "ground")
    W, D = 96.0, 126.0
    m.add(0, walled("ms_wall", W, D, 3.6, 1.6, (("S", 0.0, 10.0),), CLAY, TILE), "walls")
    m.add(0, box("ms_path", 6, D - 8, 0.1, (0, 0, 0), shade(GROUND, -0.12)))
    G(m, "ms_gate", 16, 8, 4.0, 3.2, 0, -D / 2 + 5, sb=1, sr=2, top="hip", ridge=CHIWEI)
    if kind == "wei":
        # the early plan: a tall timber pagoda in the middle of a cloistered court, the Buddha hall behind
        m.add(0, gallery("ms_clo", rect_pts(70, 64, 0, -10), 4.0, 3.0, VERM, TILE, 0.4, WHITE, closed=True), "cloister")
        m.add(1, move(tpagoda("ms_pag", 11.0, 5, 34.0), 0, -10, 0), "pagoda")
        tang_hall(m, "ms_hall", 26, 15, 6.0, 0, 40, bays=5, roof="irimoya", plat=1.4, sb=1, sr=2, trim=None, shibi=CHIWEI)
        for i, (x, y) in enumerate(((-38, 48), (38, 48), (-38, 20), (38, 20), (-30, -52), (30, -52))):
            m.add(2, poplar(f"ms_t{i}", x, y), "trees")
        return m
    m.add(0, gallery("ms_clo", [(-36, -D / 2 + 10), (-36, 30), (36, 30), (36, -D / 2 + 10)], 4.0, 3.0, VERM, TILE, 0.4, WHITE), "cloister")
    tang_hall(m, "ms_hall", 28, 16, 6.5, 0, 14, bays=5, roof="hip", plat=1.6, sb=1, sr=2, trim=GLAZE, shibi=CHIWEI)
    if kind == "kaiyuan":
        p = tpagoda("ms_pag", 9.0, 5, 30.0)
        m.add(1, move(p, 0, -22, 0), "pagoda")
        tang_hall(m, "ms_lect", 26, 13, 5.0, 0, 48, bays=5, roof="irimoya", plat=1.0, sb=1, sr=2, trim=None, shibi=CHIWEI)
        for s in (-1, 1):
            body, roof = hall_parts(f"ms_dorm{s}", 8, 30, 3.4, roof="gable", roof_h=2.4, plat=0.5, bays=2, col=WOOD, wall=CLAY, over=1.2, doors=False, stairs=False)
            m.add(1, put(body, s * 40, 46, 0.0), "halls")
            m.add(2, put(roof, s * 40, 46, 0.0), "roofs")
    else:
        # Longxing: a two-storey sutra library behind the Buddha hall, a bell tower and a sutra tower in the front court
        lou(m, "ms_lib", 22, 12, 4.6, 4.0, 0, 46, 0.0, 0.0, plat=1.2, roof="irimoya", bays=5, sb=1, sr=2, shibi=CHIWEI)
        lou(m, "ms_bell", 8, 8, 3.6, 3.0, -20, -26, 0.0, 0.0, plat=0.8, roof="hip", bays=3, sb=1, sr=2)
        lou(m, "ms_sutra", 8, 8, 3.6, 3.0, 20, -26, 0.0, 0.0, plat=0.8, roof="hip", bays=3, sb=1, sr=2)
        for s in (-1, 1):
            m.add(1, flat_yard(f"ms_cells{s}", s * 40, 46, 14, 30, 3.2, CLAY), "halls")
        m.add(1, stupa("ms_stupa", 2.4, (0, -8, 0), PLASTER, rail=False, gateways=0), "stupa")
    for i, (x, y) in enumerate(((-26, -46), (26, -46), (-42, -10), (42, -10), (-24, 62), (24, 62))):
        m.add(2, poplar(f"ms_t{i}", x, y), "trees")
    return m


# ---------------------------------------------------------------- east bank

def caravan_market():
    """A walled caravan inn and market yard, 90 x 70: rooms round a court, stables, a shop row outside, camels."""
    m = Model("caravan-market")
    m.add(0, ground("cm_g", 90, 70), "ground")
    W, D = 64.0, 48.0
    oy = 6.0
    m.add(0, walled("cm_wall", W, D, 4.8, 2.0, (("S", 0.0, 7.0),), RAM, shade(RAM, -0.15), 0, oy), "walls")
    # ranges of rooms inside the walls, flat roofed
    for k, (x, y, w, d) in enumerate(((0, oy + D / 2 - 6, W - 4, 8), (-W / 2 + 6, oy + 2, 8, D - 20), (W / 2 - 6, oy + 2, 8, D - 20))):
        m.add(1, box(f"cm_r{k}", w, d, 3.6, (x, y, 0), MUD), "rooms")
        m.add(1, box(f"cm_rp{k}", w + 0.3, d + 0.3, 0.3, (x, y, 3.6), shade(MUD, -0.08)))
    m.add(1, arcade("cm_arc", W - 8, 2.6, 9, (0, oy + D / 2 - 10.05, 0), "S", DARK, False, 0.6))
    # gate tower
    m.add(1, box("cm_gt", 12, 6, 6.5, (0, oy - D / 2, 0), RAM), "gate")
    m.add(1, passage("cm_gps", 4.0, 4.4, 6.6, (0, oy - D / 2, 0)))
    m.add(2, hip("cm_gtr", 10, 5, 2.6, (0, oy - D / 2, 6.5), TILE, over=1.2), "roofs")
    # stable sheds: posts and a reed roof along the east side of the court
    for i in range(5):
        m.add(1, box(f"cm_sp{i}", 0.35, 0.35, 2.8, (W / 2 - 13, oy - 10 + i * 5, 0), WOOD))
    m.add(2, box("cm_shed", 4.5, 22, 0.35, (W / 2 - 11, oy, 2.8), REED))
    # well, bales, camels in the yard
    m.add(1, cylinder("cm_well", 1.0, 0.8, (-6, oy, 0), STONE, verts=10))
    for i in range(6):
        m.add(1, box(f"cm_bale{i}", 1.6, 1.0, 0.9, (-14 + (i % 3) * 2.0, oy - 10 + (i // 3) * 1.4, (i % 2) * 0.0), "#C9B48A"))
    for i, (x, y, a) in enumerate(((4, oy - 6, 20), (8, oy + 2, -30), (-2, oy + 8, 80), (12, oy - 12, 0))):
        m.add(1, camel(f"cm_c{i}", x, y, a, loaded=i % 2 == 0))
    # shop row outside the gate, facing the road on the south
    m.add(1, shop_row("cm_shops", -42, -10, -26, 6, 3.4, 8.0, -1, REED, MUD, "#8C6A4A"), "shops")
    m.add(1, shop_row("cm_shops2", 10, 42, -26, 6, 3.4, 8.0, -1, REED, MUD, "#8C6A4A"))
    for i, (x, y) in enumerate(((-40, 28), (40, 28), (-42, -8), (42, -8))):
        m.add(2, poplar(f"cm_t{i}", x, y), "trees")
    for i in range(3):
        m.add(2, camel(f"cm_rc{i}", -20 + i * 5.0, -33, 0.0, loaded=True))
    return m


def xian_shrine():
    """The Sogdian fire-god shrine, 50 x 50: a walled court, a flat-roofed hall with a portico and painted niches, a fire altar."""
    m = Model("xian-shrine")
    m.add(0, ground("xs_g", 50, 50), "ground")
    m.add(0, walled("xs_wall", 46, 46, 3.0, 1.2, (("S", 0.0, 4.0),), MUD, shade(MUD, -0.12)), "walls")
    m.add(1, box("xs_plat", 22, 16, 1.0, (0, 8, 0), shade(MUD, -0.05)), "hall")
    m.add(1, box("xs_hall", 18, 12, 5.5, (0, 10, 1.0), PLASTER))
    m.add(1, box("xs_roof", 18.6, 12.6, 0.5, (0, 10, 6.5), shade(MUD, -0.1)))
    for i in range(5):
        m.add(1, cylinder(f"xs_col{i}", 0.35, 4.5, (-8 + i * 4, 2.4, 1.0), WOOD, verts=8))
    m.add(1, box("xs_por", 19, 4, 0.5, (0, 2.6, 5.5), shade(MUD, -0.1)))
    for i in range(4):
        m.add(1, box(f"xs_niche{i}", 2.2, 0.2, 3.0, (-6 + i * 4, 3.95, 1.8), "#8E4A36" if i % 2 else "#4E6A82"))
    m.add(2, box("xs_alt", 2.4, 2.4, 1.2, (0, -8, 0), STONE), "altar")
    m.add(2, box("xs_alt2", 1.6, 1.6, 0.4, (0, -8, 1.2), STONE))
    m.add(2, cylinder("xs_fire", 0.7, 0.9, (0, -8, 1.6), FLAME, verts=8, r_top=0.05))
    for i, (x, y) in enumerate(((-17, -16), (17, -16), (-18, 18), (18, 18))):
        m.add(2, poplar(f"xs_t{i}", x, y, 10), "trees")
    return m


def dang_bridge():
    """A timber trestle bridge, 95 m along X: poplar-log deck on bents, stone-filled timber cribs against the floods."""
    m = Model("dang-bridge")
    L, Wd, z = 92.0, 6.0, 3.4
    for s in (-1, 1):
        m.add(0, box(f"db_bank{s}", 8, 14, 0.3, (s * (L / 2 - 1), 0, 0), shade(GROUND, -0.04)), "abutments")
    for s in (-1, 1):
        m.add(0, frustum(f"db_ab{s}", 6, 9, 5, 8, z, (s * (L / 2 - 2), 0, 0), RAM))
    n = 8
    for i in range(1, n):
        x = -L / 2 + L * i / n
        if i % 2 == 0:
            m.add(0, box(f"db_crib{i}", 4.0, 7.4, 1.8, (x, 0, 0), STONE))
            for k in range(3):
                m.add(0, box(f"db_cl{i}{k}", 4.4, 0.3, 0.3, (x, -3.7 + k * 3.7, 0.3 + k * 0.5), WOOD))
        for sy in (-2.4, -0.8, 0.8, 2.4):
            m.add(1, cylinder(f"db_p{i}{sy}", 0.25, z, (x, sy, 0), WOOD, verts=6), "trestles")
        m.add(1, box(f"db_cap{i}", 0.5, 6.8, 0.4, (x, 0, z - 0.4), WOOD))
        m.add(1, box(f"db_br{i}", 0.2, 6.0, 0.25, (x, 0, z * 0.45), WOOD))
    m.add(2, box("db_deck", L, Wd, 0.45, (0, 0, z), PLANK), "deck")
    for k in range(int(L / 1.2)):
        m.add(2, box(f"db_log{k}", 0.55, Wd + 0.4, 0.2, (-L / 2 + 0.6 + k * 1.2, 0, z + 0.45), shade(PLANK, 0.06 * (k % 2))))
    for s in (-1, 1):
        m.add(2, box(f"db_rail{s}", L, 0.18, 0.18, (0, s * (Wd / 2 - 0.1), z + 1.4), WOOD))
        for k in range(12):
            m.add(2, box(f"db_rp{s}{k}", 0.2, 0.2, 1.4, (-L / 2 + 2 + k * (L - 4) / 11, s * (Wd / 2 - 0.1), z + 0.45), WOOD))
    m.add(2, move(camel("db_camel", -10, 0.8, 0.0, loaded=True), 0, 0, z + 0.65))
    return m


def canal_head():
    """Where a canal leaves the river, 50 x 30: a brushwood-and-stone weir, earth abutments and a timber sluice gate (doumen)."""
    m = Model("canal-head")
    m.add(0, ground("ch_g", 50, 30), "ground")
    # the canal channel running west from the river bank (+X side is the river)
    m.add(0, box("ch_canal", 46, 6, 0.4, (-2, 0, 0), WATER), "channel")
    for s in (-1, 1):
        m.add(0, frustum(f"ch_bank{s}", 46, 4, 46, 1.6, 1.4, (-2, s * 5, 0), RAM))
    m.add(0, box("ch_river", 4, 30, 0.35, (23, 0, 0), WATER))
    # weir: a wedge of brushwood bundles and stones angled into the river
    for i in range(7):
        m.add(1, box(f"ch_weir{i}", 3.0, 1.6, 1.2, (20 + i * 0.4, -3 - i * 1.6, 0), "#8E7A58" if i % 2 else STONE, rot_z=0.3), "weir")
    for i in range(6):
        m.add(1, cylinder(f"ch_stake{i}", 0.15, 2.0, (21.8 + i * 0.35, -2.5 - i * 1.8, 0), WOOD, verts=5))
    # sluice: two earth abutments, two posts, a beam, gate planks, a windlass
    for s in (-1, 1):
        m.add(1, box(f"ch_abut{s}", 4, 3, 2.8, (0, s * 4.6, 0), RAM), "sluice")
        m.add(1, box(f"ch_post{s}", 0.5, 0.5, 4.2, (0, s * 3.1, 0), WOOD))
    m.add(1, box("ch_beam", 0.6, 7.4, 0.5, (0, 0, 4.2), WOOD))
    for k in range(4):
        m.add(1, box(f"ch_plank{k}", 0.25, 6.0, 0.4, (0.1, 0, 0.6 + k * 0.42), PLANK))
    wd = cylinder("ch_wind", 0.3, 6.0, (0, 0, 1.9), WOOD, verts=6)
    wd.rotation_euler[0] = math.pi / 2
    m.add(1, wd)
    m.add(1, box("ch_foot", 1.4, 8, 0.2, (-1.2, 0, 2.8), PLANK))
    # a guard's hut, poplars, reeds
    m.add(2, hut("ch_hut", -16, 10, 6, 4.5, 2.8), "hut")
    for i, (x, y) in enumerate(((-22, -10), (-8, -11), (8, 11), (-4, 12))):
        m.add(2, poplar(f"ch_t{i}", x, y, 11), "trees")
    for i in range(4):
        m.add(2, shrub(f"ch_reed{i}", 16 + (i % 2) * 2, 8 + i * 1.6, 0.9, REED))
    return m


# ---------------------------------------------------------------- Han frontier

def beacon(ruin=False):
    """A Han beacon (feng sui), 16 x 16: a battered tower of rammed earth with reed layers, a lookout, quarters and fuel stacks."""
    m = Model("beacon")
    m.add(0, ground("bc_g", 16, 16), "ground")
    h = 6.0 if ruin else 9.0
    col = RAM_OLD if ruin else RAM
    tx, ty = 1.5, 1.5
    m.add(0, frustum("bc_tower", 7.6, 7.6, 5.4 if not ruin else 4.2, 5.4 if not ruin else 3.6, h, (tx, ty, 0), col), "tower")
    zz = 0.9
    while zz < h - 0.3:
        k = (7.6 - (5.4 if not ruin else 4.0)) * zz / h
        m.add(0, box(f"bc_reed{int(zz * 10)}", 7.6 - k + 0.14, 7.6 - k + 0.14, 0.12, (tx, ty, zz), REED if not ruin else shade(REED, -0.15)))
        zz += 0.9
    if ruin:
        m.add(0, box("bc_top", 2.6, 2.0, 1.0, (tx + 0.6, ty, h), col))
        m.add(1, drift("bc_dr", tx, ty - 4.6, 8, 3, 1.4), "debris")
        m.add(1, drift("bc_dr2", tx - 4.4, ty, 3, 7, 1.0))
        for i, (a, b) in enumerate((((-7, -7), (-7, 0)), ((-7, -7), (-1, -7)))):
            m.add(1, seg(f"bc_wr{i}", a, b, 0.9, 1.2, 0.4, col))
        m.add(2, shrub("bc_shrub", 5, -5, 1.0), "scrub")
        return m
    # parapet and lookout hut on top, ladder notches, signal pole with basket
    m.add(1, move(merlons("bc_mer", 5.0, 5.0, h, 0.6, 0.9, col), tx, ty, 0), "lookout")
    m.add(1, box("bc_hut", 2.4, 2.4, 1.8, (tx + 0.8, ty + 0.8, h), shade(col, 0.05)))
    m.add(1, box("bc_hutr", 2.9, 2.9, 0.25, (tx + 0.8, ty + 0.8, h + 1.8), REED))
    m.add(1, cylinder("bc_pole", 0.12, 7.0, (tx - 1.6, ty - 1.6, h), WOOD, verts=5))
    m.add(1, box("bc_arm", 3.2, 0.12, 0.12, (tx - 1.6, ty - 1.6, h + 6.0), WOOD, rot_z=0.5))
    m.add(1, cylinder("bc_basket", 0.5, 0.7, (tx - 0.2, ty - 0.8, h + 5.2), "#7A5E3E", verts=6))
    # foot-holes up the north face instead of a ladder
    for k in range(6):
        m.add(1, box(f"bc_hole{k}", 0.5, 0.2, 0.35, (tx, ty + 3.8 - 1.1 * (k + 0.5) / 6.5 - 0.02, 0.8 + k * 1.3), DARK))
    # quarters at the foot: a walled yard on the south-west
    for i, (a, b) in enumerate((((-7.5, -7.5), (-7.5, 1.0)), ((-7.5, -7.5), (-2.5, -7.5)), ((-2.5, -7.5), (-2.5, -3.0)))):
        m.add(1, seg(f"bc_yw{i}", a, b, 2.0, 0.9, 0.6, col, ext=0.3), "quarters")
    m.add(1, box("bc_room", 4.0, 3.0, 2.3, (-5.2, -1.0, 0), shade(col, 0.04)))
    m.add(1, box("bc_roomr", 4.4, 3.4, 0.25, (-5.2, -1.0, 2.3), REED))
    # fuel stacks (brushwood piles) for the fires
    for i, (x, y) in enumerate(((5.5, -5.5), (6.8, -2.5), (3.0, -6.8), (-1, 6.5), (-4, 6.5))):
        m.add(2, cylinder(f"bc_fuel{i}", 1.0, 1.6, (x, y, 0), "#8E7A58", verts=6, r_top=0.15), "fuel")
    return m


def han_fort():
    """A square Han fort after the 'Small Square Fort' near the Yumen Pass, 40 x 40: 26 m square, walls ~9.5 m, a single gate."""
    m = Model("han-fort")
    m.add(0, ground("hf_g", 40, 40), "ground")
    S, h = 26.0, 9.5
    pts = [(-S / 2, S / 2), (S / 2, S / 2), (S / 2, -S / 2), (-S / 2, -S / 2), (-S / 2, S / 2)]   # clockwise: outside on the right
    for i in range(1, len(pts)):
        a, b = pts[i - 1], pts[i]
        m.add(0, seg(f"hf_w{i}", a, b, h, 4.6, 3.2, RAM, ext=2.3), "walls")
        m.add(0, courses(f"hf_c{i}", a, b, h, 4.6, 3.2, 1.0, RAM_D, ext=2.2))
        m.add(1, crenels(f"hf_m{i}", a, b, h, 3.2, 1, RAM), "parapet")
    m.add(0, move(rot(passage("hf_gate", 2.6, 3.4, 5.6, (0, 0, 0)), 90), -S / 2, 4.0, 0))
    m.add(1, box("hf_hut", 7, 5, 2.6, (4, 4, 0), shade(RAM, 0.06)), "inside")
    m.add(2, box("hf_hutr", 7.5, 5.5, 0.3, (4, 4, 2.6), REED))
    # outside: a corral, fuel stacks, a cart track
    for i, (a, b) in enumerate((((-18, -18), (-6, -18)), ((-18, -18), (-18, -15)), ((-6, -18), (-6, -15)))):
        m.add(1, seg(f"hf_pen{i}", a, b, 1.2, 0.6, 0.4, "#8E7A58"), "corral")
    for i, (x, y) in enumerate(((16, -16), (17, -12), (16, 16))):
        m.add(2, cylinder(f"hf_fuel{i}", 1.1, 1.8, (x, y, 0), "#8E7A58", verts=6, r_top=0.15), "fuel")
    m.add(0, box("hf_track", 10, 3, 0.08, (-S / 2 - 5, 4.0, 0), shade(GROUND, -0.12)))
    for i, (x, y) in enumerate(((17, 4), (-17, 16))):
        m.add(2, poplar(f"hf_t{i}", x, y, 10), "trees")
    return m


# ---------------------------------------------------------------- the spring and the village

def spring_shrine():
    """A modest shrine on the south shore of the Crescent Moon Spring, 80 x 40: an earth terrace, a hall, a two-storey pavilion, reeds and poplars."""
    m = Model("spring-shrine")
    m.add(0, ground("ss_g", 80, 40, SAND), "ground")
    m.add(0, frustum("ss_terr", 52, 22, 50, 20, 1.2, (0, -4, 0), RAM), "terrace")
    m.add(0, walled("ss_wall", 54, 24, 2.4, 0.9, (("N", 0.0, 6.0),), MUD, shade(MUD, -0.12), 0, -4))
    tang_hall(m, "ss_hall", 14, 8, 4.2, -10, -7, deg=180.0, z=1.2, bays=3, roof="irimoya", plat=0.6, sb=1, sr=2, trim=None, shibi=None)
    lou(m, "ss_pav", 9, 8, 3.6, 3.0, 13, -6, 180.0, 1.2, plat=0.4, roof="hip", bays=3, sb=1, sr=2)
    # reeds and the shore toward the water on the north edge
    for i in range(12):
        m.add(2, shrub(f"ss_reed{i}", -34 + i * 6.2, 16 + (i % 3) * 1.2, 1.3, REED), "reeds")
    for i, (x, y) in enumerate(((-34, -14), (-30, 8), (32, 8), (34, -14), (-2, 10), (24, -18))):
        m.add(2, poplar(f"ss_t{i}", x, y, 12), "trees")
    for i, (x, y) in enumerate(((-38, -18), (38, -17))):
        m.add(0, frustum(f"ss_dune{i}", 6, 6, 1, 1, 3.0, (x, y, 0), SAND))
    return m


def ming_village():
    """A hamlet in the ruins, 80 x 60: a broken stretch of the old wall, mud huts, a sheep pen, felt tents, poplars."""
    m = Model("ming-village")
    m.add(0, ground("mv_g", 80, 60), "ground")
    for i, (a, b, hh) in enumerate((((-40, 24), (-12, 24), 5.5), ((-4, 24), (22, 24), 3.8), ((28, 24), (40, 24), 6.0))):
        m.add(0, seg(f"mv_w{i}", a, b, hh, 7.0, 2.0, RAM_OLD), "old wall")
        m.add(0, courses(f"mv_wc{i}", a, b, hh, 7.0, 2.0, 1.4, shade(RAM_OLD, -0.12)))
    for i, (x, y, w, d, a) in enumerate(((-28, 14, 9, 6, 0), (-14, 14, 7, 6, 0), (12, 13, 10, 6, 0), (26, 4, 6, 8, 90), (-30, -6, 8, 6, 15))):
        m.add(1, hut(f"mv_h{i}", x, y, w, d, 2.8 + (i % 2) * 0.4, MUD, a), "huts")
    # sheep pen of brushwood
    pen = [(-6, -20), (14, -20), (14, -6), (-6, -6), (-6, -20)]
    for i in range(1, len(pen)):
        if i == 4:
            continue
        m.add(1, seg(f"mv_pen{i}", pen[i - 1], pen[i], 1.2, 0.7, 0.5, "#8E7A58"), "pen")
    for i in range(9):
        m.add(1, box(f"mv_sheep{i}", 0.9, 0.5, 0.6, (-3 + (i % 3) * 4.5, -17 + (i // 3) * 4, 0.3), "#E6DECB"))
    m.add(1, yurt("mv_y1", 26, -16, 3.0), "tents")
    m.add(1, yurt("mv_y2", 32, -6, 2.6))
    m.add(1, yurt("mv_y3", -24, -22, 2.8))
    m.add(2, cylinder("mv_hay", 2.0, 2.4, (-36, 4, 0), THATCH, verts=8, r_top=0.4), "stacks")
    for i, (x, y) in enumerate(((-36, -16), (-18, 4), (2, 6), (36, 14), (18, -26))):
        m.add(2, poplar(f"mv_t{i}", x, y, 11), "trees")
    for i, (x, y) in enumerate(((-10, 20), (24, 20), (38, -24))):
        m.add(2, shrub(f"mv_s{i}", x, y), "scrub")
    m.add(0, drift("mv_dr", 4, 20, 12, 5, 1.8))
    return m


# ---------------------------------------------------------------- the Mogao cliff (hero)

CLIFF_Y = 4.0                  # front face of the cliff (south face in the builder)
TIERS = (2.5, 11.0, 19.5, 28.0)


def cliff_front(x):
    """The cliff face wanders a little in and out along its length."""
    return CLIFF_Y + 1.6 * math.sin(x / 23.0) + 0.9 * math.sin(x / 7.3 + 1.0)


def face_y(x, z):
    """The y of the battered cliff face at height z."""
    return cliff_front(x) - 0.8 + 0.8 * min(1.0, z / (cliff_h(x) - 1.5))


def cliff_h(x):
    return 36.0 + 2.0 * math.sin(x / 41.0) + 1.0 * math.sin(x / 13.0)


def great_facade(m, name, x, storeys, w, sh, d=7.0, ruin=False):
    """A timber façade of several storeys against the cliff over a colossal Buddha: storeys of red posts and white walls,
    each with its eave, a hipped roof on top; ruin = only the lower storeys and bare posts."""
    yf = cliff_front(x)
    z = 0.0
    m.add(0, box(name + "_plat", w + 4, d + 4, 0.8, (x, yf - d / 2 + 0.5, 0), STONE), "facades")
    z = 0.8
    ww = w
    for i in range(storeys):
        yy = yf - d / 2 + 0.6
        m.add(1, box(f"{name}_s{i}", ww, d, sh, (x, yy, z), WHITE if not ruin else shade(WHITE, -0.12)), "facades")
        for k in range(5):
            m.add(1, box(f"{name}_c{i}{k}", 0.6, 0.6, sh, (x - ww / 2 + 0.3 + (ww - 0.6) * k / 4, yy - d / 2 + 0.25, z), VERM))
        m.add(1, box(f"{name}_win{i}", ww * 0.5, 0.2, sh * 0.45, (x, yy - d / 2 - 0.05, z + sh * 0.3), DARKW))
        m.add(1, box(f"{name}_bal{i}", ww + 1.6, d + 1.2, 0.35, (x, yy - 0.6, z), shade(VERM, -0.1)))
        last = i == storeys - 1
        if last and not ruin:
            m.add(2, hip(f"{name}_r{i}", ww, d, d * 0.75, (x, yy, z + sh), TILE, over=2.4, ridge=CHIWEI, trim=GLAZE), "roofs")
        elif not ruin or i < storeys - 1:
            m.add(2, eaved_roof(f"{name}_e{i}", ww + 0.4, d + 0.4, 1.4, (x, yy - 0.4, z + sh - 0.2), TILE, over=2.2, curve=0.3), "roofs")
        z += sh
        ww *= 0.97
    if ruin:
        for k in range(4):
            m.add(1, box(f"{name}_bare{k}", 0.5, 0.5, sh * 1.4, (x - w / 2 + 2 + k * (w - 4) / 3, yf - d + 0.8, z), shade(VERM, -0.3)))


def mogao(variant="800"):
    """The Mogao cliff compressed to 420 x 110 m, its face to the south: cave mouths in tiers, plank galleries, timber porches,
    the façades of the North (Cave 96) and South (Cave 130) Great Buddhas, the Daquan stream and its poplars."""
    m = Model("mogao")
    early, late, ming = variant == "500", variant == "950", variant == "1500"
    m.add(0, ground("mg_g", 420, 110, shade(GROUND, -0.02)), "cliff")
    # the cliff: one continuous mesh with a wandering, slightly battered face, a rounded lip and the dune slope behind
    xs = [-210 + 420 * i / 70 for i in range(71)]
    rows = []
    for x in xs:
        yf = cliff_front(x)
        hh = cliff_h(x)
        rows.append([(x, yf - 0.8, 0.0), (x, yf, hh - 1.5), (x, yf + 2.5, hh), (x, yf + 14, hh + 3.0 + 1.5 * math.sin(x / 31.0)),
                     (x, 55.0, hh + 7.0 + 3.0 * math.sin(x / 17.0 + 2)), (x, 55.0, 0.0)])
    verts = [v for r in rows for v in r]
    k = 6
    faces = []
    for i in range(len(rows) - 1):
        for j in range(k - 1):
            a, b = i * k + j, (i + 1) * k + j
            faces.append((a, b, b + 1, a + 1))
        faces.append((i * k + k - 1, (i + 1) * k + k - 1, (i + 1) * k, i * k))
    faces.append(tuple(range(k - 1, -1, -1)))
    last = (len(rows) - 1) * k
    faces.append(tuple(range(last, last + k)))
    m.add(0, mesh_from("mg_cliff", verts, faces, (0, 0, 0), CLIFF))
    # the sand slope on top, lighter than the conglomerate face
    sv = [(x, cliff_front(x) + 2.6, cliff_h(x) + 0.05) for x in xs] + [(x, 54.8, cliff_h(x) + 7.05 + 3.0 * math.sin(x / 17.0 + 2)) for x in xs]
    n = len(xs)
    sfaces = [(i, i + 1, n + i + 1, n + i) for i in range(n - 1)]
    m.add(0, mesh_from("mg_sandtop", sv, sfaces, (0, 0, 0), SAND))
    for i in range(n - 1):
        x0, x1 = xs[i], xs[i + 1]
        verts = [(x0, cliff_front(x0) - 0.8, 0), (x1, cliff_front(x1) - 0.8, 0), (x1, cliff_front(x1) - 0.5, 2.4), (x0, cliff_front(x0) - 0.5, 2.4),
                 (x0, cliff_front(x0) - 5.0, 0), (x1, cliff_front(x1) - 5.0, 0)]
        m.add(0, mesh_from(f"mg_talus{i}", verts, [(4, 5, 2, 3), (0, 4, 3), (5, 1, 2)], (0, 0, 0), shade(CLIFF, 0.12)))
    # strata lines on the face
    for i in range(0, n - 1, 2):
        x0, x1 = xs[i], xs[min(i + 2, n - 1)]
        xc = (x0 + x1) / 2
        for kk, zz in enumerate((8.5, 17.0, 25.5)):
            m.add(0, box(f"mg_str{i}{kk}", x1 - x0 + 0.3, 0.3, 0.3, (xc, cliff_front(xc) - 0.75 + 0.8 * zz / cliff_h(xc), zz), CLIFF_D))
    # which caves are cut: the Wei caves in the middle of the cliff only, the Tang and later ones all along
    span = (-70, 70) if early else (-200, 200)
    tiers = TIERS[1:3] if early else TIERS
    caves = []
    k = 0
    for t, zt in enumerate(tiers):
        x = span[0] + 3 + (t * 2.7) % 5
        while x < span[1] - 3:
            k += 1
            w = 2.4 + (k * 7 % 5) * 0.35
            hc = 3.0 + (k * 3 % 4) * 0.4
            skip = (abs(x - 40) < 14) or (abs(x + 70) < 9 and not early)    # the Great Buddha façades
            if not skip:
                caves.append((x, zt, w, hc))
            x += 5.5 + (k * 11 % 7) * 0.9
    for i, (x, zt, w, hc) in enumerate(caves):
        yf = face_y(x, zt + 2.0)
        m.add(1, box(f"mg_cave{i}", w, 0.5, hc, (x, yf - 0.15, zt + 0.6), DARK), "caves")
    # plank galleries along each tier, with posts and ladders between tiers (rotted away by the Ming)
    if not ming:
        for t, zt in enumerate(tiers):
            if t == 0 and not early:
                continue
            xs = span[0]
            while xs < span[1]:
                xe = min(span[1], xs + 30)
                xc = (xs + xe) / 2
                if not (abs(xc - 40) < 14 or (abs(xc + 70) < 9 and not early)):
                    yf = face_y(xc, zt)
                    m.add(1, box(f"mg_gal{t}_{int(xs)}", xe - xs, 1.8, 0.3, (xc, yf - 0.9, zt + 0.25), PLANK), "galleries")
                    m.add(1, box(f"mg_galr{t}_{int(xs)}", xe - xs, 0.15, 0.15, (xc, yf - 1.75, zt + 1.3), WOOD))
                    for p in range(4):
                        m.add(1, box(f"mg_gp{t}_{int(xs)}{p}", 0.18, 0.18, 1.1, (xs + 2 + p * (xe - xs - 4) / 3, yf - 1.75, zt + 0.25), WOOD))
                xs = xe + 1.5
            if t:
                for j in range(3 if early else 6):
                    lx = span[0] + 20 + j * (span[1] - span[0] - 40) / max(1, (2 if early else 5))
                    if abs(lx - 40) < 16 or abs(lx + 70) < 11:
                        lx += 22
                    yf = face_y(lx, zt)
                    z0 = tiers[t - 1] + 0.25
                    st = box(f"mg_lad{t}{j}", 1.0, 0.5, math.hypot(zt - z0, 5.0), (0, 0, 0), WOOD)
                    st.rotation_euler[1] = math.atan2(5.0, zt - z0)
                    m.add(1, move(st, lx, yf - 1.2, z0))
    # timber porches (kuyan) over the more important caves
    porch_n = 6 if early else (18 if not late else 26)
    if ming:
        porch_n = 4
    big = [c for c in caves if c[2] > 3.3]
    for i, (x, zt, w, hc) in enumerate(big[:porch_n * 3:3]):
        yf = face_y(x, zt + 2.0)
        pw = w + 3.0
        for s in (-1, 1):
            m.add(1, box(f"mg_pp{i}{s}", 0.35, 0.35, hc + 0.6, (x + s * pw / 2, yf - 2.0, zt + 0.5), VERM))
        m.add(2, eaved_roof(f"mg_por{i}", pw, 2.6, 1.3, (x, yf - 1.1, zt + hc + 1.1), TILE if not late else shade(TILE, 0.05), over=0.9, curve=0.3), "roofs")
    # the Great Buddha façades
    if not early:
        if ming:
            great_facade(m, "mg_n", 40.0, 2, 22.0, 8.5, ruin=True)
            great_facade(m, "mg_s", -70.0, 1, 14.0, 9.0, ruin=True)
        else:
            great_facade(m, "mg_n", 40.0, 5 if late else 4, 22.0, 8.0 if late else 9.2)
            great_facade(m, "mg_s", -70.0, 3, 14.0, 8.4)
    # the valley floor: the Daquan stream, poplars and elms, stupas, the monks' houses
    m.add(0, box("mg_stream", 420, 7, 0.35, (0, -46, 0), WATER), "valley")
    nt = 14 if ming else 34
    for i in range(nt):
        x = -200 + i * 400 / (nt - 1) + (i % 3) * 2.0
        y = -34 + (i % 2) * 6
        if abs(x - 40) < 14:
            continue
        m.add(2, (poplar(f"mg_t{i}", x, y, 13 + (i % 3)) if i % 3 else elm(f"mg_t{i}", x, y, 3.4)), "trees")
    if not ming:
        for i, x in enumerate((-150, -20, 120)):
            m.add(1, flat_yard(f"mg_house{i}", x, -18, 22, 14, 3.4, MUD, -1), "houses")
        for i, x in enumerate((-180, -110, 90, 170)):
            m.add(1, stupa(f"mg_stupa{i}", 2.0, (x, -22, 0), PLASTER, rail=False, gateways=0), "stupas")
        if late or variant == "800":
            tang_hall(m, "mg_temple", 16, 9, 4.4, 160.0, -14.0, bays=3, roof="hip", plat=0.8, sb=1, sr=2, trim=None)
    else:
        for i, x in enumerate((-180, 60, 150)):
            m.add(1, drift(f"mg_sand{i}", x, cliff_front(x) - 4, 40, 8, 3.5), "sand")
        m.add(1, hut("mg_hermit", 100, -18, 7, 5, 2.8), "houses")
    if late:
        # pilgrims and lamps on the festival night: a line of small figures is beyond this scale; a banner pole instead
        for i, x in enumerate((-30, 110)):
            m.add(2, box(f"mg_pole{i}", 0.3, 0.3, 12, (x, -12, 0), WOOD))
            m.add(2, box(f"mg_ban{i}", 0.1, 1.4, 4.5, (x + 0.2, -12.8, 6.5), "#A8402C"))
    return m


BUILDERS = {
    "dunhuang/shazhou-gate": lambda: shazhou_gate("tang"),
    "dunhuang/shazhou-gate-han": lambda: shazhou_gate("han"),
    "dunhuang/shazhou-gate-ruin": lambda: shazhou_gate("ruin"),
    "dunhuang/yamen": lambda: yamen("guiyi"),
    "dunhuang/yamen-han": lambda: yamen("han"),
    "dunhuang/kaiyuan-si": lambda: monastery("kaiyuan"),
    "dunhuang/longxing-si": lambda: monastery("longxing"),
    "dunhuang/wei-monastery": lambda: monastery("wei"),
    "dunhuang/caravan-market": caravan_market,
    "dunhuang/xian-shrine": xian_shrine,
    "dunhuang/dang-bridge": dang_bridge,
    "dunhuang/canal-head": canal_head,
    "dunhuang/beacon": lambda: beacon(False),
    "dunhuang/beacon-ruin": lambda: beacon(True),
    "dunhuang/han-fort": han_fort,
    "dunhuang/spring-shrine": spring_shrine,
    "dunhuang/ming-village": ming_village,
    "dunhuang/mogao": lambda: mogao("800"),
    "dunhuang/mogao-500": lambda: mogao("500"),
    "dunhuang/mogao-950": lambda: mogao("950"),
    "dunhuang/mogao-1500": lambda: mogao("1500"),
}
