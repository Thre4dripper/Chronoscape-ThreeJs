"""Kaifeng (Bianzhou, Dongjing of the Song, Ming and Qing Kaifeng) landmark miniatures.

The hall, gate, gallery, roof, terrace, bracket, lou, wall and corbel helpers are copied from the Chang'an module (changan.py,
itself from nara.py and kyoto.py); the glazed octagonal pagoda, the woven-arch timber bridge, the restaurant with its caimen
and the rest are Kaifeng's own."""
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
MRED = "#A8402C"          # Ming column red
MGREEN = "#3F7A58"        # Ming green-glazed tile


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


def half_disc(name, r, length, loc, color, n=10):
    """A half-disc standing in the XZ plane, length thick along Y (the rounded top of a stele)."""
    x, y, z = loc
    pts = [(r * math.cos(math.pi * i / n), r * math.sin(math.pi * i / n)) for i in range(n + 1)]
    k = len(pts)
    verts = [(px, -length / 2, pz) for px, pz in pts] + [(px, length / 2, pz) for px, pz in pts]
    faces = [tuple(range(k)), tuple(range(2 * k - 1, k - 1, -1))] + [(i, i + 1, k + i + 1, k + i) for i in range(k - 1)] + [(k - 1, 0, k, 2 * k - 1)]
    return mesh_from(name, verts, faces, (x, y, z), color)


def stele_tortoise(name, loc=(0, 0, 0), h=2.8, w=1.0, color="#8A8680", deg=0.0):
    """A Tang stele on a tortoise (bixi): squat shell, head, upright slab, rounded dragon-carved top."""
    x, y, z = loc
    parts = [dome(name + "_shell", w * 0.9, (0, 0, 0.0), color, squash=0.5, segments=12, rings=6),
             box(name + "_head", w * 0.45, w * 0.6, w * 0.4, (0, -w * 1.0, 0.0), color),
             box(name + "_slab", w, w * 0.32, h, (0, 0, w * 0.35), color),
             half_disc(name + "_top", w * 0.5, w * 0.36, (0, 0, w * 0.35 + h), color)]
    o = join(parts, name)
    if deg:
        o = rot(o, deg)
    return move(o, x, y, z)


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


# ---------------------------------------------------------------- brick pagodas

def sawtooth(name, w, z, h, s, color):
    """A course of bricks laid corner-out (the 'water-chestnut teeth' of Tang cornices) round a w x w square."""
    parts = []
    n = max(4, int(w / (s * 1.7)))
    for side in range(4):
        for i in range(n):
            t = -w / 2 + w * (i + 0.5) / n
            x, y = [(t, -w / 2), (w / 2, t), (t, w / 2), (-w / 2, t)][side]
            parts.append(box(f"{name}_{side}_{i}", s, s, h, (x, y, z), color, rot_z=math.pi / 4))
    return join(parts, name)


def corbel(name, w, w_next, z, out_n=3, in_n=3, step=0.14, ch=0.15, color=PBRICK, saw=True):
    """A stepped brick cornice: courses corbelled out from w, then stepped back in to w_next. Returns (object, z on top)."""
    parts = []
    ww, zz = w, z
    for i in range(out_n):
        ww += 2 * step
        parts.append(box(f"{name}_o{i}", ww, ww, ch, (0, 0, zz), shade(color, 0.05 if i % 2 else -0.02)))
        if saw and i == 1:
            parts.append(sawtooth(f"{name}_saw", ww, zz, ch, ch * 1.6, shade(color, -0.12)))
        zz += ch
    top = ww
    for i in range(in_n):
        ww = top + (w_next - top) * (i + 1) / in_n
        parts.append(box(f"{name}_i{i}", ww, ww, ch, (0, 0, zz), shade(color, 0.02 if i % 2 else -0.04)))
        zz += ch
    return join(parts, name), zz




def ramp(name, x0, x1, y0, y1, z0, z1, color=BRICKF):
    """A ramp of width x0..x1 rising along Y from (y0, z0) to (y1, z1), a solid wedge down to z = 0."""
    verts = [(x0, y0, z0), (x1, y0, z0), (x1, y1, z1), (x0, y1, z1), (x0, y0, 0), (x1, y0, 0), (x1, y1, 0), (x0, y1, 0)]
    faces = [(0, 1, 2, 3), (4, 5, 1, 0), (5, 6, 2, 1), (6, 7, 3, 2), (7, 4, 0, 3), (7, 6, 5, 4)]
    return mesh_from(name, verts, faces, (0, 0, 0), color)


def ramp_rails(name, x0, x1, y0, y1, z0, z1, color=STONE, n=10):
    parts = []
    for x in (x0 + 0.2, x1 - 0.2):
        for i in range(n):
            t0, t1 = i / n, (i + 1) / n
            ya, yb = y0 + (y1 - y0) * t0, y0 + (y1 - y0) * t1
            za, zb = z0 + (z1 - z0) * t0, z0 + (z1 - z0) * t1
            parts.append(box(f"{name}_p{x:.0f}_{i}", 0.35, 0.35, 1.2, (x, ya, za), color))
            L = math.hypot(yb - ya, zb - za)
            ang = math.atan2(zb - za, yb - ya)
            rail = box(f"{name}_r{x:.0f}_{i}", 0.25, L, 0.2, (0, 0, 0), color)
            rail.rotation_euler[0] = ang
            bpy.context.view_layer.objects.active = rail
            bpy.ops.object.select_all(action="DESELECT")
            rail.select_set(True)
            bpy.ops.object.transform_apply(rotation=True)
            parts.append(move(rail, x, (ya + yb) / 2, (za + zb) / 2 + 1.0))
    return join(parts, name)


def crenel_line(name, a, b, z, color=MBRICK, size=1.0, gap=1.2, t=0.8):
    (ax, ay), (bx, by) = a, b
    L = math.hypot(bx - ax, by - ay)
    ang = math.atan2(by - ay, bx - ax)
    n = max(1, int(L / (size + gap)))
    parts = [box(f"{name}_p", L, t, 0.9, ((ax + bx) / 2, (ay + by) / 2, z), color, rot_z=ang)]
    for i in range(n):
        u = (i + 0.5) / n
        parts.append(box(f"{name}_{i}", size, t, 1.1, (ax + (bx - ax) * u, ay + (by - ay) * u, z + 0.9), color, rot_z=ang))
    return join(parts, name)


def paifang(name, w, h, color=MRED, roof=MGREEN):
    """A memorial archway of three bays: four posts, beams, a small hipped roof over each bay, the middle one highest."""
    parts = []
    xs = [-w / 2, -w / 6, w / 6, w / 2]
    for i, x in enumerate(xs):
        parts.append(box(f"{name}_post{i}", 0.7, 0.7, h * (1.0 if i in (1, 2) else 0.8), (x, 0, 0), color))
        parts.append(box(f"{name}_foot{i}", 1.6, 1.6, 0.8, (x, 0, 0), STONE))
    for k, (x0, x1, hh) in enumerate(((-w / 2, -w / 6, h * 0.8), (-w / 6, w / 6, h), (w / 6, w / 2, h * 0.8))):
        cx, L = (x0 + x1) / 2, x1 - x0
        parts.append(box(f"{name}_beam{k}", L + 0.8, 0.8, 1.2, (cx, 0, hh - 1.8), color))
        parts.append(box(f"{name}_board{k}", L * 0.6, 0.3, 1.0, (cx, -0.1, hh - 3.0), GLAZE_TEAL))
        parts.append(eaved_roof(f"{name}_roof{k}", L + 0.6, 1.6, 1.4, (cx, 0, hh - 0.6), roof, over=0.9, curve=0.3))
    return join(parts, name)


def octagon_pavilion(name, r, h1, h2, roof=MGREEN, col=MRED, wall=WHITE):
    """The Shengxin tower: an octagonal pavilion of two storeys with two octagonal eaves and a pointed roof."""
    def octo(rr):
        return [(rr * math.cos(math.pi / 8 + k * math.pi / 4), rr * math.sin(math.pi / 8 + k * math.pi / 4)) for k in range(8)]
    parts = [prism(name + "_pl", octo(r * 1.4), 1.0, (0, 0, 0), STONE)]
    parts.append(prism(name + "_w1", octo(r), h1, (0, 0, 1.0), wall))
    for k, (px, py) in enumerate(octo(r)):
        parts.append(box(f"{name}_c{k}", 0.5, 0.5, h1, (px, py, 1.0), col))
    parts.append(rot(cylinder(name + "_e1", r * 1.6, h1 * 0.35, (0, 0, 1.0 + h1), roof, verts=8, r_top=r * 0.8), 22.5))
    z2 = 1.0 + h1 + h1 * 0.25
    parts.append(prism(name + "_w2", octo(r * 0.75), h2, (0, 0, z2), wall))
    for k, (px, py) in enumerate(octo(r * 0.75)):
        parts.append(box(f"{name}_u{k}", 0.45, 0.45, h2, (px, py, z2), col))
    parts.append(rot(cylinder(name + "_e2", r * 1.35, r * 1.2, (0, 0, z2 + h2), roof, verts=8, r_top=r * 0.08), 22.5))
    parts.append(dome(name + "_jw", r * 0.14, (0, 0, z2 + h2 + r * 1.25), GILT, segments=10, rings=6))
    return join(parts, name)





# ---------------------------------------------------------------- Kaifeng parts
from mathutils import Vector

IRON = "#6E4C35"          # the Iron Pagoda's rust-brown glaze
IRON_L = "#86623F"
IRON_D = "#4B3527"
FBRICK = "#A99779"        # the Fan pagoda's buff-grey brick
FTILE = "#BCAA88"         # its Buddha tiles
PRED = "#A63C2C"          # red-plastered palace walls
SGLAZE = "#3E7F5E"        # Song green glaze
YGLAZE = "#C9A23A"        # Qing yellow glaze
QRED = "#A8402C"
LACQ_BLACK = "#2C2622"
BLOSSOM = "#E2A6AE"
BLOSSOM_W = "#EDE3D8"
LOTUS = "#5E8C52"
ROCK = "#9C9A92"
ROCK_D = "#7E7C76"
SILT = "#C9B98E"
CANVAS = "#D8CCB0"
FLAG_COLORS = ["#B8382C", "#D9A93A", "#3F7A58", "#3E5C9A", "#E8DCC0"]


def ngon(r, n, start=0.0):
    return [(r * math.cos(start + math.tau * k / n), r * math.sin(start + math.tau * k / n)) for k in range(n)]


def beam3d(name, p0, p1, w, h, color):
    """A square-section beam from p0 to p1 (3D points): w wide across, h deep."""
    a, b = Vector(p0), Vector(p1)
    d = (b - a).normalized()
    s = d.cross(Vector((0, 0, 1)))
    if s.length < 1e-6:
        s = Vector((1, 0, 0))
    s.normalize()
    u = s.cross(d).normalized()
    verts = [tuple(p + s * (sx * w / 2) + u * (sz * h / 2)) for p in (a, b) for sx, sz in ((-1, -1), (1, -1), (1, 1), (-1, 1))]
    faces = [(0, 1, 2, 3), (7, 6, 5, 4), (0, 4, 5, 1), (1, 5, 6, 2), (2, 6, 7, 3), (3, 7, 4, 0)]
    return mesh_from(name, verts, faces, (0, 0, 0), color)


def log3d(name, p0, p1, r, color, n=8):
    """A round log from p0 to p1."""
    a, b = Vector(p0), Vector(p1)
    d = (b - a).normalized()
    s = d.cross(Vector((0, 0, 1)))
    if s.length < 1e-6:
        s = Vector((1, 0, 0))
    s.normalize()
    u = s.cross(d).normalized()
    verts = [tuple(p + (s * math.cos(math.tau * k / n) + u * math.sin(math.tau * k / n)) * r) for p in (a, b) for k in range(n)]
    faces = [(i, (i + 1) % n, n + (i + 1) % n, n + i) for i in range(n)] + [tuple(range(n))[::-1], tuple(range(n, 2 * n))]
    return mesh_from(name, verts, faces, (0, 0, 0), color)


def face_box(name, r, a, w, d, h, z, color):
    """A box standing on a polygon face at distance r in direction a (radians), its width along the face."""
    return box(name, w, d, h, (r * math.cos(a), r * math.sin(a), z), color, rot_z=a + math.pi / 2)


def pavilion(name, w, h, roof=TILE, col=VERM, sides=4, plat=0.6, roof_h=None):
    """A small open pavilion (ting) on posts: square with a hipped roof, or polygonal with a pointed roof."""
    parts = []
    if sides == 4:
        parts.append(box(name + "_pl", w + 1.2, w + 1.2, plat, (0, 0, 0), STONE))
        for sx in (-1, 1):
            for sy in (-1, 1):
                parts.append(box(f"{name}_p{sx}{sy}", 0.35, 0.35, h, (sx * w / 2, sy * w / 2, plat), col))
        parts.append(box(name + "_bm", w + 0.4, w + 0.4, 0.4, (0, 0, plat + h - 0.4), col))
        parts.append(eaved_roof(name + "_r", w, w, roof_h or w * 0.55, (0, 0, plat + h), roof, over=w * 0.3, curve=0.3, hip=True))
    else:
        parts.append(prism(name + "_pl", ngon(w * 0.65, sides), plat, (0, 0, 0), STONE))
        for k, (px, py) in enumerate(ngon(w / 2, sides)):
            parts.append(box(f"{name}_p{k}", 0.3, 0.3, h, (px, py, plat), col))
        parts.append(prism(name + "_bm", ngon(w / 2 + 0.2, sides), 0.35, (0, 0, plat + h - 0.35), col))
        rh = roof_h or w * 0.75
        parts.append(lathe(name + "_r", [(w / 2 + w * 0.35, 0), (w / 2 + w * 0.35, 0.15), (w * 0.25, rh * 0.6), (0.05, rh)], (0, 0, plat + h), roof, verts=sides))
        parts.append(dome(name + "_jw", max(0.2, w * 0.06), (0, 0, plat + h + rh), GILT, segments=8, rings=5))
    return join(parts, name)


def parasol(name, r, h, color=CANVAS):
    """A vendor's big parasol on a pole, as on the scroll's bridge."""
    return join([cylinder(name + "_pole", 0.06, h, (0, 0, 0), WOOD, verts=6),
                 lathe(name + "_c", [(r, 0), (r * 0.5, r * 0.25), (0.05, r * 0.42)], (0, 0, h - r * 0.3), color, verts=10)], name)


def stall(name, w=3.0, d=2.0, h=2.4, cloth=CANVAS, goods="#B08A5A"):
    """A street stall: a table of goods under an awning on four poles."""
    parts = [box(name + "_t", w, d * 0.7, 0.9, (0, -d * 0.1, 0), WOOD), box(name + "_g", w * 0.85, d * 0.5, 0.3, (0, -d * 0.1, 0.9), goods)]
    for sx in (-1, 1):
        for sy in (-1, 1):
            parts.append(box(f"{name}_p{sx}{sy}", 0.1, 0.1, h, (sx * w / 2, sy * d / 2, 0), WOOD))
    parts.append(beam3d(name + "_aw", (-w / 2 - 0.2, -d / 2 - 0.4, h - 0.3), (w / 2 + 0.2, -d / 2 - 0.4, h - 0.3), 0.1, 0.1, WOOD))
    verts = [(-w / 2 - 0.2, -d / 2 - 0.5, h - 0.35), (w / 2 + 0.2, -d / 2 - 0.5, h - 0.35), (w / 2 + 0.2, d / 2 + 0.2, h + 0.3), (-w / 2 - 0.2, d / 2 + 0.2, h + 0.3)]
    parts.append(mesh_from(name + "_cl", verts, [(0, 1, 2, 3)], (0, 0, 0), cloth))
    return join(parts, name)


def boat(name, L, W, cabin=0.45, mast=None, roof=BARK, hull=WOOD, cover="#9C8A6A"):
    """A Song canal boat along X: a flaring hull with raised ends, a deck house with a curved roof, an optional mast
    given as (base x, tilt in degrees from vertical, length)."""
    parts = [frustum(name + "_hull", L * 0.8, W * 0.62, L, W, 1.3, (0, 0, 0), hull)]
    for s in (-1, 1):
        parts.append(frustum(f"{name}_end{s}", W * 0.4, W * 0.9, W * 0.2, W * 0.95, 0.8, (s * (L / 2 - W * 0.2), 0, 1.0), shade(hull, -0.08)))
    parts.append(box(name + "_rail", L * 0.92, W * 1.02, 0.25, (0, 0, 1.3), shade(hull, 0.1)))
    if cabin:
        cl = L * cabin
        parts.append(box(name + "_cab", cl, W * 0.82, 1.9, (L * 0.08, 0, 1.3), cover))
        parts.append(seg_prism(name + "_cr", (L * 0.08 - cl / 2 - 0.3, 0), (L * 0.08 + cl / 2 + 0.3, 0), 3.2, W * 0.95, 0.7, roof))
        for i in range(int(cl / 1.4)):
            parts.append(box(f"{name}_win{i}", 0.6, W * 0.84, 0.5, (L * 0.08 - cl / 2 + 0.9 + i * 1.4, 0, 2.2), DARKW))
    parts.append(beam3d(name + "_oar", (-L / 2 + 0.5, 0, 1.6), (-L / 2 - 3.5, 0, 0.2), 0.2, 0.25, WOOD))
    if mast:
        mx, tilt, ml = mast
        t = math.radians(tilt)
        top = (mx + math.sin(t) * ml, 0, 1.3 + math.cos(t) * ml)
        parts.append(log3d(name + "_mast", (mx, 0, 1.3), top, 0.16, WOOD, 6))
        parts.append(beam3d(name + "_stay", top, (L / 2 - 0.5, 0, 1.6), 0.05, 0.05, DARKW))
        parts.append(beam3d(name + "_stay2", top, (mx - 2.0, W * 0.4, 1.5), 0.05, 0.05, DARKW))
    return join(parts, name)


def caimen(name, w=7.0, h=11.0):
    """A 'coloured tower gate' (caimen) of lashed poles before a great tavern: a tall frame, a pointed top, banners and streamers."""
    parts = []
    d = 2.0
    pole = "#9A7A52"
    for sx in (-1, 1):
        for sy in (-1, 1):
            parts.append(log3d(f"{name}_p{sx}{sy}", (sx * w / 2, sy * d / 2, 0), (sx * w * 0.38, sy * d * 0.4, h), 0.13, pole, 6))
    for k, z in enumerate((h * 0.42, h * 0.66, h * 0.86)):
        ww = w * (1 - 0.12 * (k + 1) / 1.5)
        for sy in (-1, 1):
            parts.append(log3d(f"{name}_hx{k}{sy}", (-ww / 2 - 0.4, sy * d * 0.45, z), (ww / 2 + 0.4, sy * d * 0.45, z), 0.09, pole, 6))
        for sx in (-1, 1):
            parts.append(log3d(f"{name}_hy{k}{sx}", (sx * ww / 2, -d * 0.6, z), (sx * ww / 2, d * 0.6, z), 0.08, pole, 6))
    for sx in (-1, 1):
        parts.append(log3d(f"{name}_dg{sx}", (sx * w / 2, -d / 2, 0.3), (-sx * w * 0.32, -d / 2, h * 0.42), 0.08, pole, 6))
        parts.append(log3d(f"{name}_tp{sx}", (sx * w * 0.38, 0, h), (0, 0, h * 1.25), 0.1, pole, 6))
    parts.append(box(name + "_flag", 0.2, 0.2, h * 0.3, (0, 0, h * 1.2), FLAG_COLORS[0]))
    # streamers and banners in five colours hanging from the cross poles
    for k, z in enumerate((h * 0.42, h * 0.66, h * 0.86)):
        n = 7 - 2 * k
        for i in range(n):
            x = -w * 0.38 + w * 0.76 * i / max(1, n - 1)
            parts.append(box(f"{name}_st{k}_{i}", 0.45, 0.06, 1.6 - 0.3 * k, (x, -d * 0.5, z - 1.6 + 0.3 * k), FLAG_COLORS[(i + k) % 5]))
    parts.append(box(name + "_board", w * 0.5, 0.15, 1.1, (0, -d * 0.55, h * 0.48), "#2E3A5A"))
    parts.append(box(name + "_lantern", 0.7, 0.7, 0.9, (0, -d * 0.5, h * 0.28), "#C8402C"))
    return join(parts, name)


def wine_flag(name, h=9.0, color="#E8E0CC", border="#3E5C9A"):
    """A tavern's tall flag pole with a long cloth banner."""
    return join([cylinder(name + "_pole", 0.1, h, (0, 0, 0), WOOD, verts=6),
                 box(name + "_cloth", 0.08, 1.2, 3.2, (0, 0.7, h - 3.6), color),
                 box(name + "_b1", 0.1, 1.3, 0.25, (0, 0.7, h - 0.6), border),
                 box(name + "_b2", 0.1, 1.3, 0.25, (0, 0.7, h - 3.6), border)], name)


FIG_COLORS = ["#3E5C7A", "#8C3A2C", "#D8CCB0", "#5A6A4A", "#7A5A8A", "#B08A50", "#2E3A4A", "#E8E0D0"]


def figure(name, color="#3E5C7A", h=1.7):
    """A small standing figure: a robe, a head, a hat."""
    return join([cylinder(name + "_b", 0.24, h * 0.74, (0, 0, 0), color, verts=6, r_top=0.15),
                 cylinder(name + "_h", 0.12, h * 0.16, (0, 0, h * 0.74), "#D9B48A", verts=6),
                 cylinder(name + "_c", 0.2, h * 0.1, (0, 0, h * 0.9), "#2E2620", verts=6, r_top=0.05)], name)


def storeyed(m, name, w, d, hs, x=0.0, y=0.0, deg=0.0, z=0.0, roof_color=TILE, col=VERM, wall=WHITE, plat=1.0, bays=None,
             roof="irimoya", trim=None, shibi=None, ridge=None, shrink=0.94, sb=1, sr=2):
    """A building of several storeys: each with balcony, railing and a pent eave, a big roof on top. Returns the floor levels."""
    n = bays or max(3, round(w / 4.0))
    floors = []
    zz = plat
    ww, dd = w, d
    roofs = []
    for k, h in enumerate(hs):
        floors.append(zz)
        body = hall_body(f"{name}_s{k}", ww, dd, h, plat=plat if k == 0 else 0, col=col, wall=wall, bays=n, doors=(k == 0), stairs=False)
        m.add(sb, put(body, x, y, deg, z + (0 if k == 0 else zz)), "halls")
        top = zz + h
        if k < len(hs) - 1:
            ph = max(1.0, h * 0.28)
            roofs.append(eaved_roof(f"{name}_pent{k}", ww + 0.4, dd + 0.4, ph, (0, 0, top), roof_color, over=max(1.0, min(ww, dd) * 0.12), curve=0.26))
            nw, nd = ww * shrink, dd * shrink
            zb = top + ph * 0.55
            bal = [box(f"{name}_bal{k}", nw + 2.0, nd + 2.0, 0.35, (0, 0, zb), shade(col, -0.1)),
                   balustrade(f"{name}_rl{k}", rect_pts(nw + 1.8, nd + 1.8), 1.0, col, 2.2, True, zb + 0.35)]
            m.add(sb, put(join(bal, f"{name}_balc{k}"), x, y, deg, z))
            zz = zb + 0.35
            ww, dd = nw, nd
        else:
            zz = top
    rh = min(ww, dd) * 0.55
    if roof == "irimoya":
        roofs.append(irimoya(name + "_top", ww, dd, rh, (0, 0, zz), roof_color, over=min(ww, dd) * 0.22, ridge=ridge, shibi=shibi))
    else:
        roofs.append(hip(name + "_top", ww, dd, rh, (0, 0, zz), roof_color, over=min(ww, dd) * 0.22, ridge=ridge, trim=trim, shibi=shibi))
    m.add(sr, put(join(roofs, name + "_roofs"), x, y, deg, z), "roofs")
    return floors, zz + rh


# ---------------------------------------------------------------- the Iron Pagoda

def iron_storey(name, R, h, z, k):
    """One storey of the Iron Pagoda: an octagonal glazed shaft, corner columns, doors and Buddha niches on alternate faces,
    bracket sets, a thin tiled eave with upturned corners and bells, and a balcony course."""
    parts = [prism(name + "_w", ngon(R, 8), h, (0, 0, z), IRON if k % 2 == 0 else shade(IRON, 0.05))]
    for i, (px, py) in enumerate(ngon(R * 1.004, 8)):
        parts.append(cylinder(f"{name}_c{i}", 0.17, h, (px, py, z), IRON_D, verts=6))
    ap = R * math.cos(math.pi / 8)
    side = 2 * R * math.sin(math.pi / 8)
    for f in range(8):
        a = math.pi / 8 + f * math.pi / 4
        if (f + k) % 2 == 0:
            parts.append(face_box(f"{name}_dr{f}", ap + 0.05, a, side * 0.3, 0.3, h * 0.5, z + h * 0.1, DARK))
            parts.append(face_box(f"{name}_da{f}", ap + 0.05, a, side * 0.18, 0.3, h * 0.08, z + h * 0.6, DARK))
            parts.append(face_box(f"{name}_df{f}", ap + 0.02, a, side * 0.46, 0.2, h * 0.7, z + h * 0.04, IRON_L))
        else:
            parts.append(face_box(f"{name}_tp{f}", ap + 0.02, a, side * 0.62, 0.2, h * 0.56, z + h * 0.14, IRON_L))
            parts.append(face_box(f"{name}_ni{f}", ap + 0.08, a, side * 0.3, 0.25, h * 0.3, z + h * 0.26, IRON_D))
            parts.append(face_box(f"{name}_bu{f}", ap + 0.12, a, side * 0.14, 0.2, h * 0.18, z + h * 0.28, "#B08A50"))
        tx, ty = -math.sin(a), math.cos(a)
        for t in (-0.27, 0.0, 0.27):
            bx, by = (ap + 0.25) * math.cos(a) + tx * t * side, (ap + 0.25) * math.sin(a) + ty * t * side
            parts.append(box(f"{name}_bk{f}{t}", 0.32, 0.55, 0.32, (bx, by, z + h - 0.42), IRON_D, rot_z=a + math.pi / 2))
    E = R + 0.85 + 0.05 * R
    parts.append(lathe(name + "_eave", [(R * 0.99, 0.0), (E, 0.08), (E, 0.24), (R * 0.95, 0.72)], (0, 0, z + h), IRON_D, verts=8))
    for i, (px, py) in enumerate(ngon(E - 0.1, 8)):
        a = math.tau * i / 8
        parts.append(beam3d(f"{name}_up{i}", (px * 0.93, py * 0.93, z + h + 0.2), (px * 1.06, py * 1.06, z + h + 0.62), 0.28, 0.22, IRON_D))
        parts.append(cylinder(f"{name}_bell{i}", 0.13, 0.32, (px * 0.98, py * 0.98, z + h - 0.3), BRONZE, verts=6))
    parts.append(prism(name + "_pz", ngon(R * 0.97, 8), 0.24, (0, 0, z + h + 0.72), shade(IRON_L, 0.06)))
    return join(parts, name)


def iron_pagoda():
    m = Model("iron-pagoda")
    W = 90
    m.add(0, box("ground", W, W, 0.3, (0, 0, 0), GRAVEL), "court")
    m.add(0, walled("wall", W - 4, W - 4, 3.2, 1.4, (("S", 0, 10),), CLAY, TILE), "court")
    m.add(1, move(small_gate("gate", 9, 5, 4.4, VERM, TILE, "irimoya"), 0, -W / 2 + 4, 0.3), "court")
    m.add(0, box("path", 5, 34, 0.08, (0, -27, 0.3), STONE))
    # the octagonal stone base
    py = -4.0
    base = [prism("plinth0", ngon(8.2, 8), 0.6, (0, 0, 0.3), STONE), prism("plinth1", ngon(7.0, 8), 0.5, (0, 0, 0.9), shade(STONE, 0.06)),
            prism("plinth2", ngon(6.0, 8), 0.3, (0, 0, 1.4), shade(STONE, -0.05))]
    base.append(balustrade("plinth_rail", ngon(7.8, 8), 0.8, STONE, 2.0, True, 0.9))
    m.add(0, move(join(base, "base"), 0, py), "base")
    m.add(0, stair("base_st", 3.4, 1.1, 2.4, 4, (0, py - 8.6, 0.3), "S", STONE))
    # thirteen storeys
    storeys = []
    z = 1.7
    n = 13
    for k in range(n):
        R = 5.0 - 1.7 * (k / (n - 1)) ** 1.1
        h = 5.2 if k == 0 else 2.95 - 0.05 * k
        storeys.append(iron_storey(f"st{k}", R, h, z, k))
        z += h + 0.96
    R = 5.0 - 1.7
    E = R + 1.0
    crown = [lathe("roof", [(E, 0), (E, 0.15), (R * 0.55, 1.6), (0.4, 2.6), (0.0, 2.75)], (0, 0, z - 0.2), IRON_D, verts=8),
             lathe("gourd", [(0.55, 0), (0.85, 0.45), (0.5, 1.0), (0.3, 1.2), (0.62, 1.7), (0.35, 2.3), (0.15, 2.6), (0.05, 3.3)], (0, 0, z + 2.3), BRONZE, verts=12),
             cylinder("spike", 0.07, 1.6, (0, 0, z + 5.4), GILT, verts=6)]
    for i, (px, py2) in enumerate(ngon(R * 0.6, 8)):
        crown.append(beam3d(f"chain{i}", (0, 0, z + 5.0), (px, py2, z + 0.9), 0.06, 0.06, DARKW))
    m.add(1, move(join(storeys[:5], "lower"), 0, py), "pagoda")
    m.add(2, move(join(storeys[5:], "upper"), 0, py), "pagoda")
    m.add(2, move(join(crown, "crown"), 0, py), "crown")
    # the temple court: a hall behind, a bell pavilion, steles and trees
    tang_hall(m, "hall", 24, 12, 6.0, 0, 30, z=0.3, bays=5, plat=1.0, roof="irimoya", roof_h=5.4, shibi=CHIWEI, trim=None)
    m.add(1, put(pavilion("bell", 6, 4.2, TILE, VERM), -28, -24, 0, 0.3))
    m.add(1, put(pavilion("stele_p", 5, 3.6, TILE, VERM), 28, -24, 0, 0.3))
    m.add(1, stele_tortoise("stele", (28, -24, 0.9), 2.2, 0.9))
    trees(m, "pines", [(-32, 10), (32, 10), (-34, -38), (34, -38), (-20, 36), (20, 36), (-36, 30), (36, 30)], 3.8)
    return m


# ---------------------------------------------------------------- the Fan pagoda

def fan_storey(name, r, h, z, tiles=True, doors=("S", "N")):
    """A storey of the Fan pagoda: a hexagonal brick shaft faced with rows of square Buddha tiles, arched doors on two faces."""
    parts = [prism(name + "_w", ngon(r, 6), h, (0, 0, z), FBRICK)]
    ap = r * math.cos(math.pi / 6)
    door_faces = {"S": 4, "N": 1}
    dfs = [door_faces[d] for d in doors]
    for f in range(6):
        a = math.pi / 6 + f * math.pi / 3
        tx, ty = -math.sin(a), math.cos(a)
        if f in dfs:
            parts.append(face_box(f"{name}_d{f}", ap + 0.05, a, 2.2, 0.5, min(4.2, h * 0.6), z + 0.2, DARK))
            parts.append(face_box(f"{name}_da{f}", ap + 0.05, a, 1.3, 0.5, 0.6, z + 0.2 + min(4.2, h * 0.6), DARK))
        if not tiles:
            continue
        nc = max(3, int(r * 0.85 / 1.25))
        nr = max(2, int((h - 0.8) / 1.25))
        for i in range(nc):
            u = (i - (nc - 1) / 2) * 1.2
            for j in range(nr):
                zz = z + 0.5 + j * 1.2
                if f in dfs and abs(u) < 1.8 and zz < z + min(4.2, h * 0.6) + 0.9:
                    continue
                parts.append(box(f"{name}_t{f}_{i}_{j}", 0.95, 0.16, 0.95, ((ap + 0.03) * math.cos(a) + tx * u, (ap + 0.03) * math.sin(a) + ty * u, zz), FTILE if (i + j) % 3 else shade(FTILE, -0.08), rot_z=a + math.pi / 2))
    return join(parts, name)


def fan_eave(name, r, r_next, z, color=FBRICK):
    """A corbelled brick eave on a hexagon: courses stepping out, then back in to the next storey."""
    prof = [(r, 0), (r + 0.3, 0), (r + 0.3, 0.22), (r + 0.6, 0.22), (r + 0.6, 0.44), (r + 0.9, 0.44), (r + 0.9, 0.66), (r + 0.55, 0.9), (r_next, 1.1)]
    return lathe(name, prof, (0, 0, z), shade(color, -0.06), verts=6)


def fan_pagoda(variant="song"):
    m = Model({"song": "fan-pagoda", "ming": "fan-pagoda-ming", "qing": "fan-pagoda-qing"}[variant])
    W, D = 100, 110
    m.add(0, box("ground", W, D, 0.3, (0, 0, 0), FIELD if variant == "qing" else GRAVEL), "terrace")
    # the Fan terrace: a low mound faced in brick, with a stair up its south side
    th = 2.4
    m.add(0, frustum("terrace", 80, 92, 76, 88, th, (0, 2, 0.3), shade(EARTH, 0.02)), "terrace")
    m.add(0, box("terrace_top", 75, 87, 0.05, (0, 2, th + 0.3), GRAVEL if variant != "qing" else shade(FIELD, 0.05)))
    m.add(0, stair("terrace_st", 8, th, 5, 8, (0, -44 - 2.5, 0.3), "S", STONE))
    zb = th + 0.35
    py = -10.0
    m.add(0, move(prism("base", ngon(12.6, 6), 1.2, (0, 0, zb), STONE), 0, py))
    if variant == "song":
        radii = [11.0, 10.0, 9.2, 8.4, 7.6, 6.9, 6.2, 5.5, 4.9]
        heights = [8.4, 6.6, 6.0, 5.4, 5.0, 4.6, 4.3, 4.0, 3.8]
    else:
        radii, heights = [11.0, 10.0, 9.2], [8.4, 6.6, 6.0]
    z = zb + 1.2
    low, high = [], []
    for k, (r, h) in enumerate(zip(radii, heights)):
        dest = low if k < 3 else high
        dest.append(fan_storey(f"s{k}", r, h, z, tiles=k < 3 or variant == "song", doors=("S", "N") if k % 2 == 0 else ("S",)))
        z += h
        rn = radii[k + 1] if k + 1 < len(radii) else r * (0.82 if variant == "song" else 0.99)
        dest.append(fan_eave(f"e{k}", r, rn, z))
        z += 1.1
    m.add(1, move(join(low, "lower"), 0, py), "pagoda")
    top = []
    if variant == "song":
        rt = radii[-1] * 0.82
        top.append(lathe("roof", [(rt + 0.6, 0), (rt * 0.6, 1.8), (0.6, 3.6), (0, 3.8)], (0, 0, z), shade(FBRICK, -0.1), verts=6))
        top.append(lathe("finial", [(0.9, 0), (1.1, 0.6), (0.6, 1.2), (0.8, 1.8), (0.3, 2.6), (0.08, 4.2)], (0, 0, z + 3.6), BRONZE, verts=10))
        m.add(2, move(join(high + top, "upper"), 0, py), "crown")
    else:
        rt = radii[-1] * 0.99
        top.append(prism("flat", ngon(rt, 6), 0.4, (0, 0, z), shade(FBRICK, 0.04)))
        for k, (px, py2) in enumerate(ngon(rt - 0.4, 6)):
            nx, ny = ngon(rt - 0.4, 6)[(k + 1) % 6]
            top.append(beam3d(f"par{k}", (px, py2, z + 0.9), (nx, ny, z + 0.9), 0.5, 1.0, shade(FBRICK, -0.04)))
        top.append(tree("shrub0", 1.0, (3.0, 2.0, z + 0.4), "#7C8E58"))
        top.append(tree("shrub1", 0.8, (-4.0, -1.0, z + 0.4), "#7C8E58"))
        if variant == "qing":
            # the small seven-tiered spire of the Qing set on the flat top
            zz, rr = z + 0.4, 2.2
            for k in range(7):
                hh = 0.95 - 0.05 * k
                top.append(prism(f"mini{k}", ngon(rr, 6), hh, (0, 0, zz), FBRICK))
                top.append(lathe(f"minie{k}", [(rr, 0), (rr + 0.35, 0.12), (rr + 0.35, 0.25), (rr * 0.88, 0.4)], (0, 0, zz + hh), shade(FBRICK, -0.08), verts=6))
                zz += hh + 0.4
                rr *= 0.88
            top.append(lathe("mini_top", [(rr + 0.2, 0), (0.25, 0.9), (0.06, 1.8)], (0, 0, zz), BRONZE, verts=8))
        m.add(2, move(join(top, "top"), 0, py), "top")
    # the temple on the terrace
    if variant == "song":
        tang_hall(m, "hall", 26, 14, 6.5, 0, 28, z=zb, bays=5, plat=1.0, roof="hip", roof_h=6.0, shibi=CHIWEI, trim=GLAZE)
        for s in (-1, 1):
            tang_hall(m, f"side{s}", 18, 8, 4.4, s * 28, 14, deg=-90 * s, z=zb, bays=4, plat=0.6, roof="irimoya", roof_h=3.8, bk=False, shibi=None, trim=None)
        m.add(1, put(pavilion("bell", 6, 4.0), 26, -30, 0, zb))
        body, roof = gate_parts("gate", 12, 6, 4.4, 3.4, roof_h=3.8, bays=3, top="hip", trim=GLAZE, shibi=CHIWEI)
        m.add(1, put(body, 0, -40, 0, zb), "halls")
        m.add(2, put(roof, 0, -40, 0, zb))
        trees(m, "pines", [(-30, -30), (-34, 30), (34, 34), (-22, 40), (22, 40)], 3.6)
    elif variant == "ming":
        tang_hall(m, "hall", 20, 12, 5.5, 0, 28, z=zb, bays=5, plat=0.8, roof="irimoya", roof_h=5.0, shibi=None, trim=None, col=MRED, bk=False)
        m.add(1, put(small_gate("gate", 8, 4, 4.0, MRED, TILE, "irimoya"), 0, -40, 0, zb))
        trees(m, "trees", [(-30, -30), (-34, 30), (34, 34), (30, -28)], 3.6, LOCUST)
    else:
        tang_hall(m, "hall", 14, 9, 4.6, 0, 30, z=zb, bays=3, plat=0.6, roof="gable", roof_h=3.6, shibi=None, trim=None, col=MRED, bk=False)
        strips = [box(f"fx{s}", 8, 108, 0.12, (s * 45.5, 0, 0.3), shade(FIELD, 0.06 * s)) for s in (-1, 1)]
        strips += [box(f"fy{s}", 82, 5, 0.12, (0, s * 51.5 + 1.5, 0.3), shade(FIELD, -0.05)) for s in (-1, 1)]
        m.add(0, join(strips, "fields"))
        trees(m, "jujube", [(-30, -30), (-34, 30), (34, 34), (30, -28), (-44, 0), (44, -10)], 3.2, LOCUST)
    return m


# ---------------------------------------------------------------- Xiangguo temple

def xiangguo_temple():
    """The Song temple after Meng Yuanlao and the usual reconstruction: gate, bell and drum towers over the market court,
    the middle gate, the main hall on its terrace inside galleries, the Zisheng pavilion and the rear halls."""
    m = Model("xiangguo-temple")
    W, D = 180, 240
    m.add(0, box("ground", W, D, 0.3, (0, 0, 0), GRAVEL), "grounds")
    m.add(0, walled("wall", W - 4, D - 4, 3.8, 1.6, (("S", 0, 26), ("N", 0, 10)), CLAY, TILE), "walls")
    body, roof = gate_parts("shanmen", 28, 11, 6.2, 4.6, roof_h=6.0, bays=5, top="hip", trim=GLAZE, shibi=CHIWEI)
    m.add(1, put(body, 0, -D / 2 + 8, 0, 0.3), "halls")
    m.add(2, put(roof, 0, -D / 2 + 8, 0, 0.3), "roofs")
    # the market court: stalls in rows, the bell tower (east) and drum tower (west)
    lou(m, "bell", 13, 13, 6.0, 5.0, 48, -78, z=0.3, plat=1.4, roof="hip", roof_h=6.0, trim=GLAZE, shibi=CHIWEI)
    lou(m, "drum", 13, 13, 6.0, 5.0, -48, -78, z=0.3, plat=1.4, roof="hip", roof_h=6.0, trim=GLAZE, shibi=CHIWEI)
    stalls = []
    k = 0
    for row, y in enumerate((-100, -88, -62)):
        for i in range(-3, 4):
            x = i * 9.5 + (4.0 if row % 2 else 0)
            if abs(x) < 6 or abs(x) > 34:
                continue
            o = stall(f"stall{k}", 4.0, 2.6, 2.6, CANVAS if k % 3 else "#C9B28A", ["#B08A5A", "#8C5A3A", "#6E8A5A", "#C9A24A"][k % 4])
            stalls.append(put(o, x, y, 0, 0.3))
            k += 1
    m.add(2, join(stalls, "stalls"), "market")
    for s in (-1, 1):
        m.add(0, gallery(f"mkt_gal{s}", [(s * 82, -112), (s * 82, -52)], w=5, h=3.2, wall=WHITE))
    # the middle gate and the main court with its galleries
    body, roof = gate_parts("zhongmen", 20, 9, 5.2, 4.0, roof_h=5.0, bays=5, top="hip", trim=GLAZE, shibi=CHIWEI)
    m.add(1, put(body, 0, -50, 0, 0.3), "halls")
    m.add(2, put(roof, 0, -50, 0, 0.3), "roofs")
    m.add(0, gallery("kairo_w", [(-12, -50), (-72, -50), (-72, 46), (-14, 46)], w=6, h=3.6, wall=WHITE))
    m.add(0, gallery("kairo_e", [(12, -50), (72, -50), (72, 46), (14, 46)], w=6, h=3.6, wall=WHITE))
    m.add(0, box("court", 120, 90, 0.06, (0, -2, 0.3), shade(GRAVEL, -0.05)))
    m.add(0, box("path", 8, 60, 0.1, (0, -60, 0.3), STONE))
    # the main hall on a terrace, double eaves
    m.add(0, terrace("dx_t", 58, 34, 2.0, (0, 6, 0.3), STONE, shade(STONE, -0.1), batter=0.02, rail=True, rail_color=WHITE), "terraces")
    m.add(0, stair("dx_st", 14, 2.0, 5, 6, (0, 6 - 17 - 2.5, 0.3), "S", STONE))
    tang_hall(m, "daxiong", 46, 24, 9.0, 0, 6, z=2.3, bays=9, roof="hip", roof_h=10.0, plat=0.3, mokoshi=True, shibi=CHIWEI, trim=GLAZE, stairs=False)
    # side halls in the court
    for s in (-1, 1):
        tang_hall(m, f"side{s}", 22, 11, 5.0, s * 50, 0, deg=-90 * s, z=0.3, bays=5, plat=0.8, roof="irimoya", roof_h=5.0, bk=False, shibi=None, trim=None)
    # the Zisheng pavilion behind
    lou(m, "zisheng", 26, 18, 8.0, 7.0, 0, 70, z=0.3, plat=1.6, roof="hip", roof_h=9.0, trim=GLAZE, shibi=CHIWEI, double_top=True)
    # rear halls and monks' quarters
    tang_hall(m, "rear", 50, 13, 6.0, 0, 104, z=0.3, bays=10, plat=1.0, roof="irimoya", roof_h=6.0, bk=False, shibi=None, trim=None)
    for s in (-1, 1):
        for i in range(3):
            tang_hall(m, f"seng{s}{i}", 34, 9, 4.0, s * 81, -10 + i * 40, deg=-90 * s, z=0.3, bays=7, plat=0.5, roof="gable", roof_h=3.4, bk=False, shibi=None, trim=None)
    trees(m, "pines", [(-40, 30), (40, 30), (-40, -30), (40, -30), (-50, 70), (50, 70), (-30, 90), (30, 90), (-60, -100), (60, -100)], 4.0)
    return m


def xiangguo_qing():
    """The Qing temple as rebuilt in 1766: gate, bell and drum towers, Tianwang hall, the double-eaved main hall,
    the octagonal glazed Luohan hall round its central pavilion, and the sutra library."""
    m = Model("xiangguo-temple-qing")
    W, D = 180, 240
    m.add(0, box("ground", W, D, 0.3, (0, 0, 0), GRAVEL), "grounds")
    m.add(0, walled("wall", W - 30, D - 20, 4.0, 1.4, (("S", 0, 20), ("N", 0, 8)), shade(MBRICK, 0.2), MGREEN), "walls")
    # the gate: a hall-like gate with three arched doors
    gp = [box("gate_w", 30, 10, 7.0, (0, 0, 0.6), shade(QRED, 0.05)), box("gate_pl", 33, 13, 0.6, (0, 0, 0), STONE)]
    for i in (-1, 0, 1):
        gp.append(arch_panel(f"gate_d{i}", 3.2, 4.6, (i * 9, -5.05, 0.6), "S", DARK, pointed=False, depth=0.4))
    m.add(1, move(join(gp, "gate"), 0, -D / 2 + 16), "halls")
    m.add(2, irimoya("gate_r", 30, 10, 5.2, (0, -D / 2 + 16, 7.6), MGREEN, over=2.4, ridge=YGLAZE), "roofs")
    for s, nm in ((1, "bell"), (-1, "drum")):
        lou(m, nm, 11, 11, 6.0, 5.0, s * 40, -72, z=0.3, plat=1.6, roof="irimoya", roof_h=5.6, roof_color=MGREEN, col=QRED, double_top=True, ridge=YGLAZE)
    tang_hall(m, "tianwang", 28, 14, 6.0, 0, -50, z=0.3, bays=5, roof="irimoya", roof_h=6.4, plat=1.0, col=QRED, roof_color=MGREEN, shibi=YGLAZE, trim=None, bk=True)
    m.add(0, terrace("dx_t", 50, 32, 2.0, (0, -4, 0.3), STONE, shade(STONE, -0.1), batter=0.02, rail=True, rail_color=WHITE), "terraces")
    m.add(0, stair("dx_st", 12, 2.0, 5, 6, (0, -4 - 16 - 2.5, 0.3), "S", STONE))
    tang_hall(m, "daxiong", 38, 22, 9.0, 0, -4, z=2.3, bays=7, roof="irimoya", roof_h=10.0, plat=0.3, mokoshi=True, col=QRED, roof_color=YGLAZE, shibi=MGREEN, trim=None, stairs=False)
    # the octagonal Luohan hall: a ring of rooms round a court, a tall octagonal pavilion in the middle
    oz = 0.3
    cy = 46
    ring = [prism("oct_pl", ngon(25, 8, math.pi / 8), 1.0, (0, 0, 0), STONE)]
    outer, inner = ngon(23, 8, math.pi / 8), ngon(15, 8, math.pi / 8)
    for k in range(8):
        a0, a1 = outer[k], outer[(k + 1) % 8]
        b0, b1 = inner[k], inner[(k + 1) % 8]
        ring.append(mesh_from(f"oct_w{k}", [(a0[0], a0[1], 1.0), (a1[0], a1[1], 1.0), (b1[0], b1[1], 1.0), (b0[0], b0[1], 1.0),
                                            (a0[0], a0[1], 7.0), (a1[0], a1[1], 7.0), (b1[0], b1[1], 7.0), (b0[0], b0[1], 7.0)],
                              [(3, 2, 1, 0), (4, 5, 6, 7), (0, 1, 5, 4), (1, 2, 6, 5), (2, 3, 7, 6), (3, 0, 4, 7)], (0, 0, 0), WHITE))
        mx, my = (a0[0] + a1[0]) / 2, (a0[1] + a1[1]) / 2
        a = math.atan2(my, mx)
        for t in (-0.3, 0.0, 0.3):
            ring.append(box(f"oct_d{k}{t}", 1.8, 0.4, 3.2, (mx * 1.01 - math.sin(a) * t * 17, my * 1.01 + math.cos(a) * t * 17, 1.0), DARK, rot_z=a + math.pi / 2))
    for k, (px, py) in enumerate(ngon(23.2, 8, math.pi / 8)):
        ring.append(box(f"oct_c{k}", 0.6, 0.6, 6.0, (px, py, 1.0), QRED))
    m.add(1, move(join(ring, "luohan_ring"), 0, cy, oz), "halls")
    rr = [rot(lathe("oct_roof_o", [(26.5, 0), (26.5, 0.2), (19.0, 3.4)], (0, 0, 7.0), MGREEN, verts=8, cap_top=False, cap_bottom=False), 22.5),
          rot(lathe("oct_roof_i", [(11.8, 0), (11.8, 0.2), (19.0, 3.4)], (0, 0, 7.0), MGREEN, verts=8, cap_top=False, cap_bottom=False), 22.5),
          rot(lathe("oct_ridge", [(19.3, 3.2), (19.3, 3.7), (18.7, 3.7), (18.7, 3.2)], (0, 0, 7.0), YGLAZE, verts=8, cap_top=False, cap_bottom=False), 22.5)]
    m.add(2, move(join(rr, "luohan_roof"), 0, cy, oz), "roofs")
    cp = octagon_pavilion("center", 7.0, 8.0, 6.0, roof=YGLAZE, col=QRED, wall=WHITE)
    m.add(2, move(cp, 0, cy, oz))
    lou(m, "cangjing", 30, 14, 6.0, 5.0, 0, 90, z=0.3, plat=1.0, roof="irimoya", roof_h=6.0, roof_color=MGREEN, col=QRED, ridge=YGLAZE)
    for s in (-1, 1):
        tang_hall(m, f"side{s}", 26, 10, 4.6, s * 52, -10, deg=-90 * s, z=0.3, bays=6, plat=0.6, roof="irimoya", roof_h=4.4, bk=False, shibi=None, trim=None, col=QRED, roof_color=TILE)
    trees(m, "ginkgo", [(-30, -30), (30, -30), (-55, 40), (55, 40), (-40, 80), (40, 80), (-60, -95), (60, -95)], 4.2, "#8A9A4C")
    return m


# ---------------------------------------------------------------- the Song palace

def red_wall(name, pts, h=9.0, t=3.0, color=PRED, cap=SGLAZE):
    """A red-plastered palace wall with a glazed tile coping."""
    return wall_line(name, pts, h, t, color, cap)


def que_pair(m, name, x, y, sb=1, sr=2):
    """A que tower at the end of the Xuande gate's wing: a red platform with a double-eaved pavilion."""
    m.add(0, terrace(f"{name}_b", 18, 18, 10.0, (x, y, 0.3), EARTH, PRED, batter=0.03), "gate")
    m.add(0, move(merlons(f"{name}_m", 17, 17, 10.0, 0.7, 1.3, shade(PRED, -0.05)), x, y, 0.3))
    lou(m, f"{name}_t", 11, 11, 4.4, 3.6, x, y, z=10.3, plat=0.4, roof="hip", roof_h=4.6, roof_color=SGLAZE, trim=None, shibi=CHIWEI, sb=sb, sr=sr, double_top=False)


def song_palace():
    """The Xuande gate with its five passages, double-eaved tower and U-shaped wings ending in que towers;
    behind it the Daqing gate, the cloistered court and the Daqing hall with its side halls."""
    m = Model("song-palace")
    W, D = 320, 340
    m.add(0, box("ground", W, D, 0.3, (0, 0, 0), shade(STONE, 0.08)), "court")
    gy = -130.0
    # palace walls: the south wall either side of the gate, the side walls, a cross wall behind the hall
    m.add(0, red_wall("wall_sw", [(-151, gy), (-62, gy)]), "walls")
    m.add(0, red_wall("wall_se", [(62, gy), (151, gy)]))
    m.add(0, red_wall("wall_w", [(-151, gy), (-151, 168)]))
    m.add(0, red_wall("wall_e", [(151, gy), (151, 168)]))
    for s in (-1, 1):
        m.add(1, move(terrace(f"corner{s}", 14, 14, 10.0, (0, 0, 0.3), EARTH, PRED, batter=0.03), s * 151, gy))
        lou(m, f"jiaolou{s}", 9, 9, 3.6, 3.0, s * 151, gy, z=10.3, plat=0.3, roof="irimoya", roof_h=4.0, roof_color=SGLAZE, shibi=CHIWEI)
    # the Xuande gate: a red platform with five passages and a double-eaved hall of eleven bays
    gplat = [terrace("xd_plat", 84, 28, 11.0, (0, 0, 0.3), EARTH, PRED, batter=0.03)]
    pw, gap = 5.6, 4.2
    for i in range(5):
        cx = (i - 2) * (pw + gap)
        for s in (-1, 1):
            gplat.append(box(f"xd_p{i}{s}", pw, 0.8, 6.0, (cx, s * 14.05, 0.3), DARK))
            gplat.append(frustum(f"xd_pt{i}{s}", pw, 0.8, pw * 0.55, 0.8, 1.8, (cx, s * 14.05, 6.3), DARK))
        # gilt studs on the doors, Huizong's 'golden nails'
        for r in range(3):
            for c in range(3):
                gplat.append(box(f"xd_n{i}{r}{c}", 0.35, 0.3, 0.35, (cx - 1.4 + c * 1.4, -14.5, 1.4 + r * 1.4), GILT))
    gplat.append(merlons("xd_mer", 83, 27, 11.3, 0.7, 1.3, shade(PRED, -0.05)))
    m.add(0, move(join(gplat, "xuande_platform"), 0, gy), "gate")
    tang_hall(m, "xuande", 58, 17, 8.5, 0, gy, z=11.3, bays=11, roof="hip", roof_h=8.5, plat=0.5, mokoshi=True, shibi=CHIWEI, trim=None,
              roof_color=SGLAZE, ridge=shade(SGLAZE, -0.3), stairs=False, sb=1, sr=2)
    # the wings: side towers (duolou) on the platform ends, then walls running south to the que towers
    for s in (-1, 1):
        m.add(0, terrace(f"wing_x{s}", 22, 18, 10.0, (s * 53, gy, 0.3), EARTH, PRED, batter=0.03))
        tang_hall(m, f"duolou{s}", 14, 10, 4.6, s * 53, gy, z=10.3, bays=3, roof="hip", roof_h=4.6, plat=0.4, roof_color=SGLAZE, shibi=CHIWEI, trim=None, stairs=False)
        m.add(0, terrace(f"wing_y{s}", 10, 20, 9.0, (s * 58, gy - 18, 0.3), EARTH, PRED, batter=0.03))
        m.add(1, put(gallery(f"wing_g{s}", [(0, 8), (0, -8)], w=5, h=3.0, col=VERM, roof=SGLAZE, floor=0.3), s * 58, gy - 18, 0, 9.3))
        que_pair(m, f"que{s}", s * 58, gy - 30)
    m.add(0, box("square", 100, 24, 0.08, (0, gy - 28, 0.3), shade(STONE, -0.06)))
    # the court between the Xuande and Daqing gates: offices along the sides
    for s in (-1, 1):
        for i in range(3):
            tang_hall(m, f"office{s}{i}", 26, 10, 4.6, s * 127, -100 + i * 32, deg=-90 * s, z=0.3, bays=6, plat=0.6, roof="gable", roof_h=3.6, bk=False, shibi=None, trim=None)
    # the Daqing gate and the cloister
    dq_gy = -62.0
    body, roof = gate_parts("daqingmen", 36, 12, 7.0, 5.0, roof_h=6.5, bays=7, top="hip", trim=SGLAZE, shibi=CHIWEI)
    m.add(1, put(body, 0, dq_gy, 0, 0.3), "halls")
    m.add(2, put(roof, 0, dq_gy, 0, 0.3), "roofs")
    m.add(0, gallery("cloister_w", [(-19, dq_gy), (-104, dq_gy), (-104, 150), (-20, 150)], w=7, h=4.2, wall=WHITE, roof=TILE))
    m.add(0, gallery("cloister_e", [(19, dq_gy), (104, dq_gy), (104, 150), (20, 150)], w=7, h=4.2, wall=WHITE, roof=TILE))
    for s in (-1, 1):
        lou(m, f"cl_lou{s}", 12, 10, 4.6, 3.6, s * 104, 40, z=0.3, plat=0.8, roof="hip", roof_h=4.6, trim=SGLAZE, shibi=CHIWEI)
    m.add(0, box("dq_court", 200, 205, 0.06, (0, 44, 0.3), shade(STONE, -0.03)))
    m.add(0, box("dq_path", 10, 70, 0.1, (0, -24, 0.36), WHITE))
    # the Daqing hall on its terrace, with side halls
    hy = 52.0
    m.add(0, terrace("dq_t", 130, 52, 3.2, (0, hy, 0.3), STONE, shade(STONE, -0.12), batter=0.02, rail=True, rail_color=WHITE), "terraces")
    for x in (-24, 0, 24):
        m.add(0, stair(f"dq_st{x}", 10, 3.2, 6, 7, (x, hy - 26 - 3.0, 0.3), "S", STONE))
    tang_hall(m, "daqing", 66, 30, 11.0, 0, hy, z=3.5, bays=9, roof="hip", roof_h=12.0, plat=0.4, mokoshi=True, shibi=CHIWEI, trim=SGLAZE, stairs=False)
    for s in (-1, 1):
        tang_hall(m, f"xie{s}", 22, 18, 7.5, s * 50, hy, z=3.5, bays=5, roof="irimoya", roof_h=7.0, plat=0.4, shibi=CHIWEI, trim=None, stairs=False)
    tang_hall(m, "rear", 44, 16, 7.0, 0, 128, z=0.3, bays=7, roof="hip", roof_h=7.0, plat=1.4, shibi=CHIWEI, trim=SGLAZE)
    # bronze vessels and the incense burners in the court
    for s in (-1, 1):
        m.add(1, cylinder(f"ding{s}", 1.2, 2.0, (s * 20, 8, 0.3), BRONZE, verts=10))
    trees(m, "trees", [(-130, 120), (130, 120), (-130, 60), (130, 60), (-138, 0), (138, 0)], 4.4)
    return m


# ---------------------------------------------------------------- the Imperial Way

def imperial_way():
    """A stretch of the Yujie in its 1112 form: the emperor's lane between red-lacquered fences, brick-lined channels with lotus
    and blossoming trees, black-lacquered fences, and covered walks for the people on both sides."""
    m = Model("imperial-way")
    W, D = 110, 560
    m.add(0, box("ground", W, D, 0.3, (0, 0, 0), shade(EARTH, 0.06)), "avenue")
    m.add(0, box("lane", 18, D, 0.08, (0, 0, 0.3), shade(STONE, 0.04)))
    for s in (-1, 1):
        m.add(0, box(f"ch_edge{s}", 6.2, D, 0.5, (s * 16, 0, 0.3), BRICKF))
        m.add(0, box(f"ch_water{s}", 4.6, D, 0.08, (s * 16, 0, 0.8), WATERC))
        pads = [cylinder(f"lotus{s}_{i}", 0.7 + 0.3 * (i % 3) / 2, 0.06, (s * 16 + ((i * 37) % 5 - 2) * 0.5, -D / 2 + 3 + i * 4.3, 0.88), LOTUS, verts=8) for i in range(int((D - 6) / 4.3))]
        m.add(2, join(pads, f"lotus{s}"), "planting")
        m.add(0, box(f"walk{s}", 22, D, 0.06, (s * 41, 0, 0.3), shade(EARTH, -0.04)))
    # fences: red lacquer either side of the imperial lane, black lacquer outside the channels
    fences = []
    for s in (-1, 1):
        for x, col, tag in ((s * 9.8, LACQUER, "red"), (s * 21.5, LACQ_BLACK, "black")):
            n = int(D / 3.0)
            for i in range(n + 1):
                y = -D / 2 + i * D / n
                fences.append(box(f"f{tag}{s}_{i}", 0.22, 0.22, 1.3, (x, y, 0.3), col))
            fences.append(box(f"fr{tag}{s}", 0.18, D, 0.16, (x, 0, 1.45), col))
            fences.append(box(f"fm{tag}{s}", 0.14, D, 0.12, (x, 0, 0.8), col))
            # the cross-legged 'chazi' trestles along the fence, every 9 m
            for i in range(int(D / 9)):
                y = -D / 2 + 4.5 + i * 9
                fences.append(beam3d(f"fx{tag}{s}_{i}a", (x, y - 1.2, 0.3), (x, y + 1.2, 1.4), 0.12, 0.12, col))
                fences.append(beam3d(f"fx{tag}{s}_{i}b", (x, y + 1.2, 0.3), (x, y - 1.2, 1.4), 0.12, 0.12, col))
    m.add(1, join(fences, "fences"), "fences")
    # the covered walks (yulang)
    for s in (-1, 1):
        m.add(1, gallery(f"yulang{s}", [(s * 47, -D / 2 + 4), (s * 47, D / 2 - 4)], w=8, h=3.6, col=VERM, roof=TILE, floor=0.4, post_every=5.0), "walks")
    # peach, plum, pear and apricot along the channels
    tr = []
    for s in (-1, 1):
        for side, x in enumerate((s * 12.6, s * 19.4)):
            for i in range(int(D / 16)):
                y = -D / 2 + 6 + i * 16 + side * 8
                tr.append(tree(f"t{s}{side}_{i}", 2.6, (x, y, 0.3), (BLOSSOM, BLOSSOM_W, "#7E9A5C")[(i + side) % 3], TIMBER))
    m.add(2, join(tr, "blossom"), "planting")
    # a few people's stalls and carriages at the walks, and the emperor's lane left empty
    for i, y in enumerate((-200, -80, 60, 180)):
        m.add(2, put(stall(f"st{i}", 3.6, 2.4, 2.4), (-1) ** i * 33, y, 90 * (-1) ** i, 0.3))
    return m


# ---------------------------------------------------------------- the Rainbow Bridge

def rainbow_bridge():
    """The pierless 'woven arch' over the Bian after the scroll and Tang Huancheng: two interlocking systems of logs (one of three
    segments, one of four), cross beams at the nodes, a humped plank deck with railings, stalls and parasols, tall marker poles
    at the ends, and a grain boat beneath lowering its mast."""
    m = Model("rainbow-bridge")
    W, D = 44, 56
    R = 13.0              # half the clear span (bank to bank)
    m.add(0, box("water", W, 2 * R, 0.12, (0, 0, 0), WATERC), "banks")
    for s in (-1, 1):
        m.add(0, box(f"bank{s}", W, D / 2 - R, 0.9, (0, s * (R + (D / 2 - R) / 2), 0), shade(EARTH, 0.03)))
        # timber-piled revetments along both banks
        piles = [cylinder(f"pile{s}_{i}", 0.16, 1.15, (-W / 2 + 0.4 + i * 0.5, s * (R - 0.15), 0.0), WOOD, verts=8) for i in range(int((W - 0.8) / 0.5))]
        piles.append(box(f"wale{s}", W, 0.25, 0.25, (0, s * (R - 0.1), 0.85), WOOD))
        m.add(0, join(piles, f"piles{s}"))
        # stone abutments that take the arch thrust
        m.add(0, box(f"abut{s}", 10.5, 3.0, 1.6, (0, s * (R + 1.2), 0.0), STONE))
    # the two arch systems, alternating across the width
    A = [(-R, 0.9), (-7.5, 4.6), (7.5, 4.6), (R, 0.9)]
    B = [(-R + 0.5, 0.7), (-9.5, 3.1), (0.0, 5.55), (9.5, 3.1), (R - 0.5, 0.7)]
    logs = []
    nrow = 13
    BW = 8.4
    for i in range(nrow):
        x = -BW / 2 - 0.2 + i * (BW + 0.4) / (nrow - 1)
        pts = A if i % 2 == 0 else B
        for k in range(len(pts) - 1):
            (y0, z0), (y1, z1) = pts[k], pts[k + 1]
            logs.append(log3d(f"log{i}_{k}", (x, y0, z0), (x, y1, z1), 0.23, shade(TIMBER, -0.08 if i % 2 else 0.02), 10))
    # cross beams at every node, lashed with rope
    for (y, z) in A[1:-1] + B[1:-1]:
        logs.append(log3d(f"cross{y}", (-BW / 2 - 0.3, y, z + 0.05), (BW / 2 + 0.3, y, z + 0.05), 0.22, shade(TIMBER, -0.1)))
        for i in range(0, nrow, 2):
            x = -BW / 2 - 0.2 + i * (BW + 0.4) / (nrow - 1)
            logs.append(cylinder(f"rope{y}_{i}", 0.26, 0.4, (x, y, z - 0.15), "#B39A6A", verts=6))
    # struts from the arch up to the deck near the ends
    for s in (-1, 1):
        for x in (-BW / 2 + 0.4, BW / 2 - 0.4):
            logs.append(log3d(f"strut{s}{x}", (x, s * 11.0, 1.8), (x, s * 11.0, 3.2), 0.14, TIMBER))
    m.add(1, join(logs, "arch"), "arch")

    def deck_z(y):
        a = abs(y)
        return 6.3 - 0.0219 * a * a if a <= R else max(0.9, 2.6 - (a - R) * (1.7 / 8.0))

    deck, rails = [], []
    ys = [-21.0 + i * 1.0 for i in range(43)]
    for k in range(len(ys) - 1):
        y0, y1 = ys[k], ys[k + 1]
        deck.append(beam3d(f"deck{k}", (0, y0, deck_z(y0) - 0.2), (0, y1, deck_z(y1) - 0.2), BW - 0.2, 0.4, shade(TIMBER, 0.08)))
        for h_ in (0.0, 0.5):
            yh = y0 + h_
            deck.append(box(f"plank{k}_{h_}", BW - 0.1, 0.1, 0.06, (0, yh, deck_z(yh)), shade(TIMBER, -0.12)))
        for s in (-1, 1):
            rails.append(beam3d(f"rail{k}{s}", (s * (BW / 2 + 0.2), y0, deck_z(y0) + 1.05), (s * (BW / 2 + 0.2), y1, deck_z(y1) + 1.05), 0.16, 0.16, "#8A6844"))
            rails.append(beam3d(f"railm{k}{s}", (s * (BW / 2 + 0.2), y0, deck_z(y0) + 0.55), (s * (BW / 2 + 0.2), y1, deck_z(y1) + 0.55), 0.1, 0.1, "#8A6844"))
            rails.append(box(f"post{k}{s}", 0.22 if k % 2 == 0 else 0.12, 0.22 if k % 2 == 0 else 0.12, 1.2, (s * (BW / 2 + 0.2), y0, deck_z(y0) - 0.05), "#7A5A3A"))
            yh = y0 + 0.5
            rails.append(box(f"bal{k}{s}", 0.1, 0.1, 1.0, (s * (BW / 2 + 0.2), yh, deck_z(yh) - 0.05), "#7A5A3A"))
    m.add(1, join(deck, "deck"), "deck")
    m.add(2, join(rails, "rails"), "deck")
    # stalls and parasols on the hump, sheds and willows on the banks
    props = []
    for k, (x, y) in enumerate(((-3.3, -9), (3.3, -6), (-3.3, -3), (3.3, 2), (-3.3, 6), (3.3, 9), (-3.3, 11), (3.3, -11))):
        props.append(put(parasol(f"umb{k}", 1.6, 3.0, (CANVAS, "#C9B28A", "#B9A27E")[k % 3]), x, y, 0, deck_z(y)))
        props.append(box(f"goods{k}", 1.4, 1.0, 0.7, (x * 0.85, y + 0.6, deck_z(y)), ("#A0784A", "#8C6A4A", "#B89A5A")[k % 3]))
    for s in (-1, 1):
        for x in (-W / 2 + 5, W / 2 - 5):
            sh = [box(f"shed{s}{x}", 7, 4.5, 3.0, (x, s * 22.5, 0.9), CLAY), seg_prism(f"shedr{s}{x}", (x - 4, s * 22.5), (x + 4, s * 22.5), 3.9, 6.0, 1.5, TILE),
                  box(f"shedaw{s}{x}", 7, 2.0, 0.15, (x, s * 22.5 - s * 3.2, 2.4), CANVAS)]
            props.append(join(sh, f"shed{s}{x}"))
        # the tall marker poles (huabiao) with cross pieces and a bird on top, as on the scroll
        for x in (-BW / 2 - 1.0, BW / 2 + 1.0):
            props.append(cylinder(f"hb{s}{x}", 0.15, 10.0, (x, s * 16.5, 0.9), "#7A5A3A", verts=6))
            props.append(box(f"hbx{s}{x}", 1.8, 0.15, 0.15, (x, s * 16.5, 9.4), "#7A5A3A"))
            props.append(box(f"hbb{s}{x}", 0.3, 0.6, 0.3, (x, s * 16.5, 10.9), "#E8E0D0"))
        for x in (-W / 2 + 2.8, W / 2 - 2.8):
            props.append(tree(f"willow{s}{x}", 2.4, (x, s * 16.0, 0.9), WILLOW))
        for x in (-11.0, 11.0):
            props.append(put(stall(f"bstall{s}{x}", 3.0, 2.2, 2.4, CANVAS, "#A0784A"), x, s * 18.5, 0 if s > 0 else 180, 0.9))
            props.append(put(parasol(f"bumb{s}{x}", 1.5, 2.8), x + 3.0 * (1 if x > 0 else -1), s * 19.0, 0, 0.9))
    m.add(2, join(props, "props"), "life")
    # the grain boat shooting the bridge, its mast half lowered
    bt = boat("boat", 18.0, 4.6, cabin=0.5, mast=(-1.5, 55, 9.0))
    m.add(2, put(bt, 7.0, -1.0, 0, 0.0), "boat")
    for i in range(3):
        m.add(2, beam3d(f"pole{i}", (2 + i * 4, 1.8, 2.4), (1 + i * 4, 4.2, 0.05), 0.12, 0.12, WOOD))
    # the crowd: people leaning over the rails, crossing, crew on the boat, porters on the banks
    crowd = []
    k = 0
    for y in [-17 + i * 1.6 for i in range(22)]:
        for x in (-2.4, 0.4, 2.8) if abs(y) < 12 else (-1.2, 1.6):
            if (k * 7) % 5 == 0:
                k += 1
                continue
            xx = x + ((k * 13) % 7 - 3) * 0.15
            crowd.append(put(figure(f"p{k}", FIG_COLORS[k % len(FIG_COLORS)]), xx, y, 0, deck_z(y)))
            k += 1
    for s in (-1, 1):
        for i in range(16):
            x = -19 + i * 2.5 + (i % 3) * 0.6
            crowd.append(put(figure(f"b{s}{i}", FIG_COLORS[(i + 3) % len(FIG_COLORS)]), x, s * (15.5 + (i % 4) * 2.4), 0, 0.9))
    for i, (x, y) in enumerate(((2, 1.6), (6, -1.8), (10, 1.5), (14, -1.2), (-0.8, 0.0))):
        crowd.append(put(figure(f"crew{i}", "#5A6A7A"), 7.0 + x - 7.0, -1.0 + y, 0, 1.3))
    m.add(2, join(crowd, "crowd"), "life")
    return m


# ---------------------------------------------------------------- the Fan Tower

def fan_tower():
    """Three linked three-storey halls round a court, joined by covered flying bridges at the upper floors, the caimen of lashed
    poles at the street gate, a wine flag and lanterns."""
    m = Model("fan-tower")
    W, D = 80, 64
    m.add(0, box("ground", W, D, 0.3, (0, 0, 0), shade(EARTH, 0.05)), "court")
    m.add(0, box("court", 30, 26, 0.06, (0, -6, 0.3), STONE))
    hs = [4.6, 3.8, 3.4]
    floors_c, top_c = storeyed(m, "main", 30, 16, hs, 0, 16, 0, 0.3, roof_color=TILE, col=VERM, wall=WHITE, plat=1.0, bays=7, roof="irimoya", shibi=CHIWEI)
    for s in (-1, 1):
        storeyed(m, f"wing{s}", 22, 14, hs, s * 27, -8, -90 * s, 0.3, roof_color=TILE, col=VERM, wall=WHITE, plat=1.0, bays=5, roof="irimoya", shibi=CHIWEI)
    # flying bridges at the second and third floors between the halls
    fb = []
    for s in (-1, 1):
        for k in (1, 2):
            zf = 0.3 + floors_c[k]
            a = (s * 15.0, 9.0)
            b = (s * 20.0, 2.0)
            fb.append(box(f"fb_floor{s}{k}", 3.2, 9.0, 0.35, ((a[0] + b[0]) / 2, (a[1] + b[1]) / 2, zf), WOOD, rot_z=math.atan2(b[1] - a[1], b[0] - a[0]) + math.pi / 2))
            fb.append(move(gallery(f"fb_gal{s}{k}", [a, b], w=3.0, h=2.4, col=VERM, roof=TILE, floor=0.1), 0, 0, zf))
    m.add(2, join(fb, "flying_bridges"), "bridges")
    # the street front: a gate building, the caimen and the wine flag
    m.add(1, put(small_gate("gate", 9, 4, 4.0, VERM, TILE, "irimoya"), 0, -24, 0, 0.3), "front")
    m.add(2, put(caimen("caimen", 8.0, 12.0), 0, -29.3, 0, 0.3), "caimen")
    m.add(2, put(wine_flag("flag", 12.0), 9, -29, 0, 0.3))
    lanterns = []
    for s in (-1, 1):
        for i in range(5):
            lanterns.append(box(f"lan{s}{i}", 0.6, 0.6, 0.8, (s * 15.5, 10 + i * 3.0 - 6, 0.3 + floors_c[1] - 1.2), "#C8402C"))
    for i in range(7):
        lanterns.append(box(f"lanf{i}", 0.6, 0.6, 0.8, (-12 + i * 4, 7.6, 0.3 + floors_c[2] - 1.2), "#D9A93A"))
    m.add(2, join(lanterns, "lanterns"))
    # kitchens and stores at the back, a wall round the lot
    m.add(0, walled("wall", W - 2, D - 2, 2.8, 0.9, (("S", 0, 10),), CLAY, TILE), "court")
    for x in (-28, 28):
        m.add(1, put(yard_houses(f"kitchen{x}", 0, 0, 14, 10, 3.6, CLAY, TILE), x, 22))
    return m


# ---------------------------------------------------------------- the Genyue garden

def crag(name, r0, h, loc=(0, 0, 0), seed=0.0, color=ROCK, n=9, lean=0.15):
    """A craggy rock mass: an irregular base outline rising to a smaller, offset, uneven top."""
    x, y, z = loc
    base, mid, top = [], [], []
    for i in range(n):
        a = math.tau * i / n
        k = 1 + 0.22 * math.sin(3 * a + seed) + 0.12 * math.cos(5 * a + seed * 1.7)
        base.append((x + r0 * k * math.cos(a), y + r0 * k * math.sin(a), z))
        mid.append((x + r0 * 0.68 * k * math.cos(a + 0.2) + lean * r0, y + r0 * 0.6 * k * math.sin(a + 0.2), z + h * (0.5 + 0.1 * math.sin(a * 2 + seed))))
        top.append((x + r0 * 0.3 * k * math.cos(a - 0.3) + lean * r0 * 1.5, y + r0 * 0.28 * k * math.sin(a - 0.3), z + h * (0.86 + 0.14 * math.sin(a * 3 + seed))))
    verts = base + mid + top + [(x + lean * r0 * 1.6, y, z + h * 1.02)]
    faces = [tuple(range(n))[::-1]]
    for ring in (0, 1):
        o = ring * n
        faces += [(o + i, o + (i + 1) % n, o + n + (i + 1) % n, o + n + i) for i in range(n)]
    faces += [(2 * n + i, 2 * n + (i + 1) % n, 3 * n) for i in range(n)]
    return mesh_from(name, verts, faces, (0, 0, 0), color)


def genyue():
    """Huizong's garden as an interpretation: the Wansui peak of piled Lake Tai rocks with pavilions on its ridges, lesser hills,
    a lake with a hall and gallery, standing rocks, groves of pine, plum and bamboo."""
    m = Model("genyue")
    W, D = 360, 300
    m.add(0, box("ground", W, D, 0.3, (0, 0, 0), GRASS), "ground")
    m.add(0, walled("wall", W - 4, D - 4, 3.6, 1.4, (("S", 0, 12), ("W", 0, 8)), PRED, SGLAZE), "ground")
    m.add(0, blob("lake", 60, 36, 0.25, (60, -60, 0.3), WATERC, 0.7), "water")
    m.add(0, blob("pond", 26, 18, 0.25, (-130, -60, 0.3), WATERC, 1.9))
    # winding stream from the hill to the lake
    pts = [(-40, 10), (-10, -20), (20, -40), (50, -60)]
    for i in range(len(pts) - 1):
        (ax, ay), (bx, by) = pts[i], pts[i + 1]
        m.add(0, box(f"stream{i}", math.hypot(bx - ax, by - ay) + 4, 5, 0.22, ((ax + bx) / 2, (ay + by) / 2, 0.3), WATERC, rot_z=math.atan2(by - ay, bx - ax)))
    # the main peak and its ridges
    hills = [crag("peak", 46, 28, (-60, 50, 0.3), 0.3, ROCK, 11, 0.1), crag("peak_e", 30, 18, (-15, 70, 0.3), 1.4, ROCK_D, 9),
             crag("peak_w", 32, 16, (-110, 40, 0.3), 2.2, ROCK_D, 9), crag("ridge_n", 26, 14, (-60, 100, 0.3), 3.1, ROCK, 9),
             crag("hill_s", 22, 10, (-70, -10, 0.3), 4.0, ROCK_D, 8), crag("wanshou", 24, 15, (100, 70, 0.3), 5.3, ROCK, 9),
             crag("hill_se", 16, 8, (140, 20, 0.3), 6.1, ROCK_D, 8)]
    m.add(0, join(hills, "hills"), "hills")
    # standing Taihu rocks
    rocks = [crag(f"stone{i}", 1.6 + (i % 3) * 0.6, 4.0 + (i % 4) * 1.6, (x, y, 0.3), i * 0.9, ROCK, 7, 0.25)
             for i, (x, y) in enumerate(((20, -10), (35, -25), (5, -55), (-25, -50), (120, -30), (150, -60), (60, 20), (-140, -40), (-150, 100), (30, 110), (160, 110), (-20, -110)))]
    m.add(1, join(rocks, "rocks"), "rocks")
    # pavilions on the heights and by the water
    m.add(1, put(pavilion("summit", 7, 4.0, SGLAZE, VERM, sides=8), -52.6, 50, 0, 27.4), "pavilions")
    m.add(1, put(pavilion("east_ting", 5, 3.4, TILE, VERM), -7.8, 70, 0, 17.2))
    m.add(1, put(pavilion("west_ting", 5, 3.4, TILE, VERM), -102.3, 40, 0, 15.1))
    m.add(1, put(pavilion("wanshou_ting", 6, 3.6, SGLAZE, VERM, sides=6), 105.8, 70, 0, 14.1))
    m.add(1, put(pavilion("lake_ting", 6, 3.4, TILE, VERM, sides=8), 50, -60, 0, 0.3))
    lou(m, "jiangxiao", 22, 14, 5.0, 4.0, 148, -100, z=0.3, plat=1.2, roof="irimoya", roof_h=5.0, roof_color=SGLAZE, shibi=CHIWEI)
    m.add(1, gallery("lake_gal", [(134, -112), (80, -124), (20, -122), (-14, -104)], w=4, h=3.0, roof=TILE, floor=0.4))
    tang_hall(m, "hall", 30, 14, 6.0, -120, -110, z=0.3, bays=7, roof="irimoya", roof_h=6.0, plat=1.2, roof_color=SGLAZE, shibi=CHIWEI, trim=None)
    # groves: pines on the hill, plum and apricot by the water, bamboo on the north
    pines = [(-90, 70), (-40, 85), (-75, 25), (-30, 40), (-95, 15), (-55, 120), (80, 95), (120, 55), (-130, 70)]
    trees(m, "pines", pines, 5.0, PINE)
    plums = [(x, y) for x in range(20, 170, 22) for y in (-20, 5) if abs(x - 60) > 12]
    trees(m, "plums", plums, 3.0, BLOSSOM)
    bamboo = [(x, 125 + (x % 3) * 4) for x in range(-170, 170, 9) if abs(x) > 8]
    m.add(2, grove("bamboo", [(x, y, 0.3) for x, y in bamboo], 2.2, "#7FA05A"))
    deer = [box(f"deer{i}", 1.3, 0.5, 0.9, (x, y, 0.8), "#A07850") for i, (x, y) in enumerate(((-150, -10), (-140, -2), (160, -100)))]
    m.add(2, join(deer, "deer"), "life")
    return m


# ---------------------------------------------------------------- the Zhou bridge

def zhouqiao(variant="song"):
    """The Zhou bridge over the Bian: under the Song a low flat bridge of stone columns and beams with stone railings, the river
    walls carved with sea horses and waves, night-market stalls; in the Ming a stone arch."""
    m = Model("zhouqiao" if variant == "song" else "zhouqiao-ming")
    W, D = 50, 64
    R = 13.0
    m.add(0, box("water", W, 2 * R, 0.15, (0, 0, 0), WATERC if variant == "song" else shade(WATERC, 0.1)), "banks")
    bw = 22.0 if variant == "song" else 14.0
    for s in (-1, 1):
        m.add(0, box(f"bank{s}", W, D / 2 - R, 2.4, (0, s * (R + (D / 2 - R) / 2), 0), shade(EARTH, 0.04)))
        # the stone river walls with their carved panels
        wall = [box(f"rw{s}", W, 0.8, 2.4, (0, s * (R + 0.2), 0), STONE)]
        for i in range(8):
            x = -W / 2 + 3 + i * 6.2
            if abs(x) < bw / 2 + 1:
                continue
            wall.append(box(f"relief{s}{i}", 4.6, 0.25, 1.4, (x, s * (R - 0.25), 0.5), shade(STONE, 0.12)))
            wall.append(box(f"relief_h{s}{i}", 1.6, 0.3, 0.7, (x - 0.8, s * (R - 0.35), 0.9), shade(STONE, -0.12)))
            wall.append(box(f"relief_w{s}{i}", 3.4, 0.3, 0.3, (x + 0.4, s * (R - 0.35), 0.65), shade(STONE, -0.08)))
        m.add(0, join(wall, f"riverwall{s}"))
    if variant == "song":
        # stone columns in rows, stone beams, a flat slab deck and stone railings
        cols = []
        for yy in (-6.5, 0.0, 6.5):
            for i in range(7):
                x = -bw / 2 + 1 + i * (bw - 2) / 6
                cols.append(box(f"col{yy}_{i}", 0.9, 0.9, 2.2, (x, yy, 0.1), shade(STONE, -0.04)))
            cols.append(box(f"cap{yy}", bw, 1.3, 0.4, (0, yy, 2.0), STONE))
        m.add(1, join(cols, "columns"), "bridge")
        deck = [box("deck", bw, 2 * R + 1.6, 0.4, (0, 0, 2.4), shade(STONE, 0.06))]
        for s in (-1, 1):
            n = 14
            for i in range(n + 1):
                deck.append(box(f"bal{s}{i}", 0.35, 0.35, 1.1, (s * (bw / 2 - 0.3), -R - 0.8 + i * (2 * R + 1.6) / n, 2.8), WHITE))
            deck.append(box(f"balr{s}", 0.3, 2 * R + 1.6, 0.25, (s * (bw / 2 - 0.3), 0, 3.75), WHITE))
        m.add(1, join(deck, "deck"), "bridge")
        # the night market: stalls along the deck edges and the banks, lanterns on poles
        props = []
        k = 0
        for y in (-9, -3, 3, 9):
            for s in (-1, 1):
                props.append(put(stall(f"st{k}", 2.8, 2.0, 2.3, (CANVAS, "#C9B28A")[k % 2], ("#B08A5A", "#C8603A", "#D9A93A")[k % 3]), s * (bw / 2 - 2.6), y, -90 * s, 2.8))
                k += 1
        for s in (-1, 1):
            for x in (-20, -14, 14, 20):
                props.append(put(stall(f"bst{s}{x}", 3.0, 2.2, 2.4), x, s * 22, 0 if s > 0 else 180, 2.4))
            for x in (-bw / 2 - 2, bw / 2 + 2):
                props.append(cylinder(f"lp{s}{x}", 0.08, 5.0, (x, s * 15, 2.4), WOOD, verts=6))
                props.append(box(f"lt{s}{x}", 0.7, 0.7, 0.9, (x, s * 15, 6.6), "#C8402C"))
        m.add(2, join(props, "night_market"), "market")
        for s in (-1, 1):
            for x0, x1 in ((-W / 2 + 1, -bw / 2 - 4), (bw / 2 + 4, W / 2 - 1)):
                m.add(1, put(shop_row(f"shops{s}{x0}", x0, x1, 0, 6, 4.4, 4.5, -1, TILE, CLAY), 0, s * 28.5, 0 if s > 0 else 180, 2.4), "shops")
        crowd = [put(figure(f"p{i}", FIG_COLORS[i % len(FIG_COLORS)]), -bw / 2 + 3 + (i * 37) % int(bw - 6), -R + 1 + (i * 53) % int(2 * R - 2), 0, 2.8) for i in range(30)]
        m.add(2, join(crowd, "crowd"), "market")
    else:
        # a single stone arch, humped deck and railings
        arch = []
        n = 16
        for i in range(n):
            a0, a1 = math.pi * i / n, math.pi * (i + 1) / n
            y0, z0 = -R * math.cos(a0), 2.4 + 3.2 * math.sin(a0)
            y1, z1 = -R * math.cos(a1), 2.4 + 3.2 * math.sin(a1)
            arch.append(beam3d(f"ring{i}", (0, y0, z0 + 0.5), (0, y1, z1 + 0.5), bw, 1.0, STONE))
        for s in (-1, 1):
            arch.append(box(f"spandrel{s}", bw, R * 0.9, 3.6, (0, s * R * 0.6, 2.4), shade(STONE, 0.04)))
        m.add(1, join(arch, "arch"), "bridge")
        deck = []
        for s in (-1, 1):
            for i in range(10):
                y = -R + i * 2.6
                z = 2.4 + 3.2 * math.sin(math.pi * (i + 0.5) / 10) + 1.5
                deck.append(box(f"bal{s}{i}", 0.4, 0.4, 1.0, (s * (bw / 2 - 0.3), y + 1.3, z), WHITE))
        m.add(2, join(deck, "rails"), "rails")
        for s in (-1, 1):
            for x0, x1 in ((-W / 2 + 1, -bw / 2 - 3), (bw / 2 + 3, W / 2 - 1)):
                m.add(2, put(shop_row(f"shops{s}{x0}", x0, x1, 0, 7, 4.6, 5.0, -1, TILE, shade(MBRICK, 0.25)), 0, s * 27, 0 if s > 0 else 180, 2.4), "houses")
            m.add(1, stair(f"steps{s}", 6, 2.4, 3, 6, (bw / 2 + 4, s * (R + 2.5), 0.0), "S" if s < 0 else "N", STONE))
            for x in (-22, -16, 16, 22):
                m.add(2, tree(f"willow{s}{x}", 2.4, (x, s * 16.5, 2.4), WILLOW))
            for x in (-bw / 2 - 1.5, bw / 2 + 1.5):
                m.add(2, cylinder(f"lp{s}{x}", 0.1, 4.0, (x, s * 14.5, 2.4), STONE, verts=8))
                m.add(2, box(f"lt{s}{x}", 0.8, 0.8, 0.9, (x, s * 14.5, 6.4), "#D8CCB0"))
        m.add(2, put(boat("boat0", 9.0, 2.6, cabin=0.4), -16, -4, 0, 0.0))
        m.add(2, put(boat("boat1", 8.0, 2.4, cabin=0.35), 17, 5, 180, 0.0))
        crowd = [put(figure(f"p{i}", FIG_COLORS[i % len(FIG_COLORS)]), -4 + (i * 37) % 8, -10 + (i * 53) % 20, 0, 2.4 + 3.2 * math.sin(math.pi * ((-10 + (i * 53) % 20) + R) / (2 * R)) + 1.0) for i in range(12)]
        crowd += [put(figure(f"q{i}", FIG_COLORS[(i + 2) % len(FIG_COLORS)]), -22 + (i * 29) % 44, (1 if i % 2 else -1) * (15 + (i * 7) % 7), 0, 2.4) for i in range(30)]
        m.add(2, join(crowd, "crowd"), "houses")
    return m


# ---------------------------------------------------------------- the synagogue

def synagogue():
    """After Jean Domenge's drawings of 1722: built with its gate on -Y (turned to face east on the map) and the main hall
    and the chamber of the scrolls at +Y (the west end, toward Jerusalem)."""
    m = Model("synagogue")
    W, D = 40, 110
    m.add(0, box("ground", W, D, 0.3, (0, 0, 0), GRAVEL), "courts")
    m.add(0, walled("wall", W - 2, D - 2, 3.4, 0.9, (("S", 0, 6),), shade(WHITE, -0.06), TILE), "courts")
    m.add(0, box("path", 3.2, 90, 0.08, (0, -8, 0.3), STONE))
    m.add(1, put(small_gate("gate", 8, 4, 4.2, MRED, TILE, "irimoya"), 0, -D / 2 + 3.6, 0, 0.3), "gates")
    m.add(1, put(paifang("arch1", 12, 7.0, MRED, TILE), 0, -40, 0, 0.3))
    for y in (-28, -2):
        m.add(0, wall_line(f"cross{y}a", [(-18.5, y), (-4.5, y)], 3.0, 0.8, shade(WHITE, -0.06), TILE))
        m.add(0, wall_line(f"cross{y}b", [(4.5, y), (18.5, y)], 3.0, 0.8, shade(WHITE, -0.06), TILE))
        m.add(1, put(small_gate(f"cgate{y}", 8, 3.6, 4.0, MRED, TILE, "irimoya"), 0, y, 0, 0.3))
    # stele pavilions of 1489, 1512 and 1663 in the middle court, and a great archway
    for s in (-1, 1):
        m.add(1, put(pavilion(f"stp{s}", 4.6, 3.4, TILE, MRED), s * 11, -15, 0, 0.3), "pavilions")
        m.add(1, box(f"stele{s}", 1.0, 0.35, 2.4, (s * 11, -15, 0.9), "#8E8A84"))
    m.add(1, put(paifang("arch2", 14, 7.8, MRED, TILE), 0, 6, 0, 0.3))
    # side halls: the hall of the patriarchs and the hall for washing
    for s in (-1, 1):
        tang_hall(m, f"side{s}", 14, 7, 4.0, s * 14, 16, deg=-90 * s, z=0.3, bays=4, plat=0.5, roof="gable", roof_h=3.0, bk=False, shibi=None, trim=None, col=MRED)
    # the main hall with its porch, and the chamber of the Torah scrolls behind
    m.add(0, terrace("hall_t", 26, 30, 1.2, (0, 31, 0.3), STONE, shade(STONE, -0.1), batter=0.02, rail=True, rail_color=WHITE), "hall")
    m.add(0, stair("hall_st", 8, 1.2, 3, 4, (0, 31 - 15 - 1.5, 0.3), "S", STONE))
    tang_hall(m, "porch", 20, 5, 4.6, 0, 20, z=1.5, bays=5, plat=0.1, roof="gable", roof_h=2.4, bk=False, shibi=None, trim=None, col=MRED, wall=shade(MRED, 0.5), stairs=False)
    tang_hall(m, "hall", 21, 17, 6.4, 0, 32, z=1.5, bays=5, plat=0.2, roof="irimoya", roof_h=6.4, bk=True, shibi=TILE, trim=None, col=MRED, stairs=False)
    tang_hall(m, "bema", 12, 7, 5.2, 0, 45, z=1.5, bays=3, plat=0.2, roof="hip", roof_h=4.0, bk=False, shibi=None, trim=None, col=MRED, stairs=False)
    trees(m, "trees", [(-14, -46), (14, -46), (-14, -34), (14, -34), (-15, 48), (15, 48)], 2.8, LOCUST)
    return m


# ---------------------------------------------------------------- the south gate

def south_gate(variant="song"):
    m = Model("south-gate" if variant == "song" else "south-gate-ming")
    W, D = 130, 110
    m.add(0, box("ground", W, D, 0.3, (0, 0, 0), shade(EARTH, 0.05)), "walls")
    if variant == "song":
        m.add(0, box("moat", W, 12, 0.08, (0, -34, 0.3), WATERC))
        m.add(0, box("bridge", 9, 15, 1.2, (0, -34, 0.3), WOOD))
        m.add(0, box("road", 12, D, 0.06, (0, 0, 0.3), shade(EARTH, -0.12)))
        tang_gate(m, "zhuque", 40, 20, 10.0, 3, 5.0, 30, 12, 6.0, 7, 0, 6, 0, roof_h=6.5, wall_len=64, wall_h=9.0, ramps=True)
        for x0, x1 in ((-62, -10), (10, 62)):
            m.add(1, put(shop_row(f"shops{x0}", x0, x1, 0, 7, 4.2, 6.5, -1, TILE, CLAY), 0, 34, 0, 0.3), "town")
            m.add(1, put(shop_row(f"shops_s{x0}", x0, x1, 0, 6, 3.8, 6.5, 1, TILE, CLAY), 0, -48, 0, 0.3))
        trees(m, "willows", [(-55, -26), (-40, -26), (-25, -26), (25, -26), (40, -26), (55, -26)], 3.0, WILLOW)
        crowd = [put(figure(f"p{i}", FIG_COLORS[i % len(FIG_COLORS)]), -2 + (i * 37) % 5, -54 + (i * 23) % 26 if i % 2 else 22 + (i * 23) % 30, 0, 0.3) for i in range(18)]
        m.add(2, join(crowd, "crowd"), "town")
    else:
        wh = 12.0
        m.add(0, box("moat", W, 10, 0.08, (0, -47, 0.3), WATERC))
        m.add(0, box("bridge", 9, 14, 1.2, (0, -47, 0.3), STONE))
        m.add(0, box("road", 10, 30, 0.06, (0, 40, 0.3), shade(EARTH, -0.12)))
        m.add(0, frustum("wall", W, 16, W, 12, wh, (0, 4, 0.3), MBRICK), "walls")
        m.add(0, crenel_line("cren_s", (-W / 2, -3.7), (W / 2, -3.7), wh + 0.3))
        m.add(0, box("parapet_n", W, 0.7, 1.0, (0, 9.7, wh + 0.3), MBRICK))
        m.add(0, box("walk", W, 11, 0.08, (0, 4, wh + 0.3), shade(MBRICK, 0.12)))
        m.add(1, arch_panel("passage_s", 6.0, 8.0, (0, -4.1, 0.3), "S", DARK, pointed=False, depth=0.8), "gates")
        m.add(1, arch_panel("passage_n", 6.0, 8.0, (0, 12.1, 0.3), "N", DARK, pointed=False, depth=0.8))
        for s in (-1, 1):
            verts = [(s * 20, 13, wh + 0.3), (s * 20, 19, wh + 0.3), (s * 56, 19, 0.3), (s * 56, 13, 0.3), (s * 20, 13, 0.3), (s * 20, 19, 0.3)]
            m.add(0, mesh_from(f"mdao{s}", verts, [(0, 1, 2, 3), (4, 5, 1, 0), (3, 4, 0), (5, 2, 1), (3, 2, 5, 4)], (0, 0, 0), shade(MBRICK, 0.05)))
        # the barbican (wengcheng) and its outer gate
        bh = 10.0
        for s in (-1, 1):
            m.add(0, frustum(f"bwall{s}", 10, 34, 8, 34, bh, (s * 27, -21, 0.3), MBRICK))
            m.add(0, crenel_line(f"bcren{s}", (s * 31.5, -38), (s * 31.5, -4), bh + 0.3))
        m.add(0, frustum("bwall_s", 64, 9, 64, 7, bh, (0, -38, 0.3), MBRICK))
        m.add(0, crenel_line("bcren_south", (-32, -42.2), (32, -42.2), bh + 0.3))
        m.add(1, arch_panel("bgate_s", 5.0, 6.6, (0, -42.6, 0.3), "S", DARK, pointed=False, depth=0.8))
        m.add(1, arch_panel("bgate_n", 5.0, 6.6, (0, -33.4, 0.3), "N", DARK, pointed=False, depth=0.8))
        jl = [box("jianlou", 22, 8, 5.0, (0, -38, bh + 0.3), shade(MBRICK, 0.06))]
        for r in range(2):
            for i in range(6):
                jl.append(box(f"win{r}_{i}", 1.0, 0.4, 1.0, (-8.75 + i * 3.5, -42.1, bh + 1.2 + r * 2.0), DARK))
        m.add(1, join(jl, "arrow_tower"))
        m.add(2, irimoya("jianlou_r", 22, 8, 4.2, (0, -38, bh + 5.3), TILE, over=1.6, ridge=shade(TILE, -0.25)), "roofs")
        lou(m, "zhenglou", 30, 12, 6.0, 5.0, 0, 4, z=wh + 0.3, plat=0.6, roof="irimoya", roof_h=7.0, roof_color=TILE, col=MRED, double_top=True, ridge=shade(TILE, -0.3))
        for x0, x1 in ((-62, -12), (12, 62)):
            m.add(1, put(shop_row(f"shops{x0}", x0, x1, 0, 7, 4.2, 7.0, -1, TILE, shade(MBRICK, 0.25)), 0, 36, 0, 0.3), "town")
        trees(m, "willows", [(-55, -40), (-42, -40), (42, -40), (55, -40)], 3.0, WILLOW)
    return m


# ---------------------------------------------------------------- the Prince of Zhou's palace

def zhou_palace():
    """A Ming princely palace as an interpretation (after the Ming rules and the Prince of Qin's palace in Xi'an): screen wall,
    moat and inner wall, the Duanli gate, three halls on an I-shaped terrace, side halls, the residence and gardens."""
    m = Model("zhou-palace")
    W, D = 300, 380
    m.add(0, box("ground", W, D, 0.3, (0, 0, 0), GRAVEL), "walls")
    m.add(0, walled("screen", W - 4, D - 4, 5.0, 1.8, (("S", 0, 16), ("N", 0, 10)), PRED, MGREEN), "walls")
    IW, ID = 190, 290
    oy = 10
    for s in (-1, 1):
        m.add(0, box(f"moat_x{s}", IW + 30, 8, 0.12, (0, oy + s * (ID / 2 + 9), 0.3), WATERC))
        m.add(0, box(f"moat_y{s}", 8, ID + 18, 0.12, (s * (IW / 2 + 11), oy, 0.3), WATERC))
    m.add(0, box("bridge", 14, 12, 1.0, (0, oy - ID / 2 - 9, 0.3), STONE))
    m.add(0, walled("inner", IW, ID, 8.0, 3.0, (("S", 0, 18), ("N", 0, 10)), PRED, MGREEN, 0, oy), "walls")
    for sx in (-1, 1):
        for sy in (-1, 1):
            lou(m, f"corner{sx}{sy}", 8, 8, 3.4, 2.8, sx * (IW / 2), oy + sy * (ID / 2), z=8.0, plat=0.3, roof="irimoya", roof_h=3.6, roof_color=MGREEN, col=MRED)
    body, roof = gate_parts("duanli", 36, 12, 7.0, 5.0, roof_h=6.5, bays=5, top="irimoya", col=MRED, wall=shade(MRED, 0.35), roof=MGREEN)
    m.add(1, put(body, 0, oy - ID / 2, 0, 0.3), "halls")
    m.add(2, put(roof, 0, oy - ID / 2, 0, 0.3), "roofs")
    body, roof = gate_parts("outer_gate", 26, 10, 6.0, 4.5, roof_h=5.5, bays=5, top="irimoya", col=MRED, wall=shade(MRED, 0.35), roof=MGREEN)
    m.add(1, put(body, 0, -D / 2 + 9, 0, 0.3))
    m.add(2, put(roof, 0, -D / 2 + 9, 0, 0.3))
    m.add(0, box("approach", 10, 40, 0.08, (0, -D / 2 + 26, 0.3), STONE))
    # the three halls on an I-shaped terrace
    m.add(0, terrace("gong_t", 90, 150, 2.6, (0, oy - 20, 0.3), STONE, shade(STONE, -0.06), batter=0.02, rail=True, rail_color=WHITE), "terraces")
    m.add(0, stair("gst", 14, 2.6, 6, 6, (0, oy - 95 - 3, 0.3), "S", STONE))
    tang_hall(m, "chengyun", 50, 24, 9.0, 0, oy - 70, z=2.9, bays=9, roof="hip", roof_h=10.0, plat=0.4, mokoshi=True, shibi=YGLAZE, trim=None, col=MRED, roof_color=MGREEN, stairs=False, bk=True)
    tang_hall(m, "yuandian", 24, 20, 7.0, 0, oy - 22, z=2.9, bays=5, roof="hip", roof_h=7.0, plat=0.4, shibi=YGLAZE, trim=None, col=MRED, roof_color=MGREEN, stairs=False, bk=False)
    tang_hall(m, "cundian", 44, 22, 8.0, 0, oy + 28, z=2.9, bays=9, roof="irimoya", roof_h=8.5, plat=0.4, shibi=YGLAZE, trim=None, col=MRED, roof_color=MGREEN, stairs=False, bk=True)
    for s in (-1, 1):
        for i in range(3):
            tang_hall(m, f"wu{s}{i}", 40, 10, 5.0, s * 74, oy - 100 + i * 60, deg=-90 * s, z=0.3, bays=8, plat=0.6, roof="irimoya", roof_h=4.5, bk=False, shibi=None, trim=None, col=MRED)
    for i in range(2):
        tang_hall(m, f"gong{i}", 60, 16, 6.0, 0, oy + 80 + i * 36, z=0.3, bays=11, plat=0.8, roof="irimoya", roof_h=6.0, bk=False, shibi=None, trim=None, col=MRED, roof_color=MGREEN)
    # gardens and offices in the outer precinct
    m.add(0, blob("pond", 16, 14, 0.25, (-128, 150, 0.3), WATERC, 0.4), "grounds")
    m.add(1, put(pavilion("pond_ting", 5, 3.2, MGREEN, MRED, sides=6), -128, 172, 0, 0.3))
    for i, (x, y) in enumerate(((128, 150), (128, -140), (-128, -140), (128, 10), (-128, 10))):
        m.add(1, yard_houses(f"office{i}", x, y, 36, 40, 4.5, CLAY, TILE, i))
    trees(m, "trees", [(-125, 90), (-100, 170), (-140, 60), (130, 90), (-125, -80), (130, -80), (-60, -175), (60, -175), (60, 165), (-60, 165)], 4.6, PINE)
    return m


# ---------------------------------------------------------------- the Dragon Pavilion

def dragon_pavilion():
    """The present form: a brick platform some 13 m high at the north end of the causeway, a long stair with the carved dragon
    slope up its middle, a double-eaved hall roofed in yellow glaze, side halls at the foot."""
    m = Model("dragon-pavilion")
    W, D = 120, 150
    m.add(0, box("ground", W, D, 0.3, (0, 0, 0), shade(STONE, 0.1)), "platform")
    for s in (-1, 1):
        m.add(0, box(f"lake{s}", 46, 26, 0.1, (s * 37, -62, 0.3), WATERC))
    m.add(0, box("causeway", 10, 60, 0.08, (0, -45, 0.3), STONE))
    py, pd, ph = 30.0, 40.0, 13.0
    m.add(0, terrace("plat", 50, pd, ph, (0, py, 0.3), STONE, "#9A9690", batter=0.04, rail=True, rail_color=WHITE), "platform")
    face = py - pd / 2
    run = 24.0
    for s in (-1, 1):
        m.add(0, stair(f"st{s}", 5.0, ph, run, 30, (s * 4.6, face - run / 2, 0.3), "S", STONE))
        m.add(0, ramp_rails(f"rail{s}", s * 7.3, s * 7.3 + s * 0.3, face - run, face, 0.3, ph + 0.3, WHITE, 10))
    m.add(0, ramp("dragon", -2.1, 2.1, face - run, face, 0.3, ph + 0.3, "#DCD4C4"))
    scales = [box(f"scale{i}", 3.0, 0.5, 0.25, (0, face - run + 1 + i * 1.9, 0.3 + (ph) * (1 + i * 1.9) / run + 0.1), "#C9BFA8") for i in range(12)]
    m.add(1, join(scales, "dragon_relief"))
    tang_hall(m, "longting", 28, 18, 7.0, 0, py + 2, z=ph + 0.3, bays=7, roof="irimoya", roof_h=8.0, plat=0.6, mokoshi=True, col=QRED, roof_color=YGLAZE, shibi=MGREEN, trim=None, stairs=False)
    for s in (-1, 1):
        tang_hall(m, f"side{s}", 22, 10, 5.0, s * 42, 10, deg=-90 * s, z=0.3, bays=5, plat=0.8, roof="irimoya", roof_h=4.8, bk=False, shibi=None, trim=None, col=QRED, roof_color=MGREEN)
        m.add(1, put(pavilion(f"ting{s}", 6, 3.8, YGLAZE, QRED, sides=8), s * 40, -24, 0, 0.3))
        m.add(1, box(f"lion{s}", 1.2, 2.0, 2.2, (s * 9, face - run - 3, 0.3), "#B9B1A2"))
    m.add(1, put(paifang("gate", 16, 8.0, QRED, YGLAZE), 0, -66, 0, 0.3), "gate")
    m.add(1, cylinder("burner", 1.0, 2.2, (0, -28, 0.3), BRONZE, verts=10))
    trees(m, "cypress", [(-20, -30), (20, -30), (-30, 60), (30, 60), (-50, 55), (50, 55), (-52, -10), (52, -10)], 3.4, PINE)
    return m


# ---------------------------------------------------------------- the Yanqing temple

def yanqing_temple():
    """The Jade Emperor pavilion of the Yuan: a two-stage square brick tower with arched doors and a corbelled cornice, crowned by
    an octagonal pavilion under a tent-like roof; the gate, side halls and main hall of the walled court."""
    m = Model("yanqing-temple")
    W, D = 70, 120
    m.add(0, box("ground", W, D, 0.3, (0, 0, 0), GRAVEL), "court")
    m.add(0, walled("wall", W - 4, D - 4, 3.4, 1.2, (("S", 0, 8),), shade(MBRICK, 0.25), TILE), "court")
    m.add(1, put(small_gate("gate", 9, 4.5, 4.4, MRED, TILE, "irimoya"), 0, -D / 2 + 4, 0, 0.3), "halls")
    m.add(0, box("path", 4, 90, 0.08, (0, -10, 0.3), STONE))
    yb = "#B4A88E"
    py = -14
    tw = [box("y_plinth", 15, 15, 0.8, (0, 0, 0.3), STONE), frustum("y_low", 13, 13, 12.6, 12.6, 6.0, (0, 0, 1.1), yb)]
    for face in ("S", "N", "E", "W"):
        fx, fy = {"S": (0, -6.4), "N": (0, 6.4), "E": (6.4, 0), "W": (-6.4, 0)}[face]
        tw.append(arch_panel(f"y_door{face}", 2.2, 3.6, (fx, fy, 1.1), face, DARK, pointed=False, depth=0.5))
    c, ztop = corbel("y_cor", 12.6, 10.0, 7.1, 4, 4, 0.2, 0.2, yb, saw=True)
    tw.append(c)
    tw.append(box("y_mid", 10.0, 10.0, 2.4, (0, 0, ztop), shade(yb, 0.04)))
    tw.append(merlons("y_par", 9.8, 9.8, ztop + 2.4, 0.5, 0.7, shade(yb, -0.04)))
    z2 = ztop + 2.4
    tw.append(prism("y_oct", ngon(3.6, 8, math.pi / 8), 3.0, (0, 0, z2), WHITE))
    for k, (px, py2) in enumerate(ngon(3.65, 8, math.pi / 8)):
        tw.append(box(f"y_col{k}", 0.35, 0.35, 3.0, (px, py2, z2), MRED))
    for k in range(8):
        a = math.pi / 4 + k * math.pi / 4
        tw.append(face_box(f"y_win{k}", 3.35, a, 1.0, 0.25, 1.6, z2 + 0.6, DARKW))
    m.add(1, move(join(tw, "yuhuang_tower"), 0, py), "pavilion")
    rf = [rot(lathe("y_eave", [(5.4, 0), (5.4, 0.2), (3.0, 1.2), (1.6, 3.4), (0.2, 4.4), (0.0, 4.5)], (0, 0, z2 + 3.0), MGREEN, verts=8), 22.5),
          lathe("y_fin", [(0.4, 0), (0.6, 0.4), (0.3, 0.9), (0.45, 1.3), (0.06, 2.2)], (0, 0, z2 + 7.4), GILT, verts=10)]
    m.add(2, move(join(rf, "yuhuang_roof"), 0, py), "roofs")
    for s in (-1, 1):
        tang_hall(m, f"side{s}", 18, 8, 4.4, s * 24, 4, deg=-90 * s, z=0.3, bays=4, plat=0.6, roof="gable", roof_h=3.4, bk=False, shibi=None, trim=None, col=MRED)
    tang_hall(m, "sanqing", 24, 13, 6.0, 0, 36, z=0.3, bays=5, plat=1.2, roof="irimoya", roof_h=6.0, bk=True, shibi=TILE, trim=None, col=MRED)
    m.add(1, stele_tortoise("stele", (-14, -36, 0.3), 2.6, 0.9))
    m.add(1, cylinder("burner", 0.8, 1.6, (0, -32, 0.3), BRONZE, verts=10))
    trees(m, "trees", [(-24, -40), (24, -40), (-24, 48), (24, 48), (22, -22)], 3.2, PINE)
    return m


# ---------------------------------------------------------------- the grain wharves

def bian_wharves():
    """A stone-faced quay on the Bian inside the east outer city: grain boats moored and unloading, porters with sacks, a timber
    hoist, round and long granaries, warehouse sheds and willows."""
    m = Model("bian-wharves")
    W, D = 220, 70
    zl = 1.4
    m.add(0, box("water", W, 14, 0.1, (0, -28, 0), WATERC), "quay")
    m.add(0, box("land", W, 56, zl, (0, 7, 0), shade(EARTH, 0.04)))
    m.add(0, box("quay_wall", W, 1.2, zl + 0.1, (0, -20.6, 0), STONE))
    m.add(0, box("quay_top", W, 9, 0.06, (0, -15.5, zl), shade(STONE, 0.05)))
    for x in range(-100, 101, 25):
        m.add(0, stair(f"steps{x}", 4, zl, 3, 5, (x, -22.1, 0.0), "S", STONE))
    for i, x in enumerate((-70, 0, 70)):
        H(m, f"granary{i}", 46, 15, 5.0, x, 21, z=zl, sb=1, sr=2, roof="gable", roof_h=5.5, roof_color=TILE, col=WOOD, wall=CLAY, plat=1.0, doors=True)
    for i, x in enumerate((-100, -40, 40, 100)):
        m.add(1, cylinder(f"cang{i}", 4.0, 5.0, (x, -2, zl), CLAY, verts=14), "granaries")
        m.add(2, cylinder(f"cang_r{i}", 4.8, 2.6, (x, -2, zl + 5.0), THATCH, verts=14, r_top=0.3), "roofs")
    m.add(1, put(gallery("shed", [(-24, 0), (24, 0)], w=9, h=3.6, col=WOOD, roof=TILE, floor=0.2, post_every=4.0), 0, -4, 0, zl), "sheds")
    sacks = []
    for i in range(36):
        x = -20 + (i % 9) * 4.6
        y = -6 + (i // 9) * 1.2
        sacks.append(box(f"sack{i}", 1.1, 0.8, 0.55, (x, y, zl + 0.2 + (i // 18) * 0.55), "#C9B48A" if i % 3 else "#B8A276"))
    m.add(2, join(sacks, "sacks"), "goods")
    # a timber hoist on the quay
    for x in (-60, 60):
        hp = [beam3d(f"hleg{x}a", (x - 2, -14, zl), (x, -16, zl + 9), 0.35, 0.35, WOOD), beam3d(f"hleg{x}b", (x + 2, -14, zl), (x, -16, zl + 9), 0.35, 0.35, WOOD),
              beam3d(f"hboom{x}", (x, -16, zl + 9), (x, -25, zl + 7), 0.25, 0.25, WOOD), beam3d(f"hrope{x}", (x, -25, zl + 7), (x, -25, zl + 2.5), 0.05, 0.05, DARKW),
              box(f"hload{x}", 1.4, 1.0, 0.8, (x, -25, zl + 1.7), "#C9B48A")]
        m.add(2, join(hp, f"hoist{x}"), "goods")
    # the boats, gangplanks and porters
    for i, (x, mast) in enumerate(((-80, None), (-30, (2.0, 0, 9.0)), (20, None), (75, (1.0, 0, 10.0)))):
        m.add(2, put(boat(f"boat{i}", 18.0, 4.6, cabin=0.42, mast=mast), x, -28, 0, 0.0), "boats")
        m.add(2, beam3d(f"plank{i}", (x - 4, -25.8, 1.4), (x - 4, -20.0, zl + 0.05), 0.9, 0.12, WOOD))
    crowd = []
    for i in range(26):
        x = -95 + i * 7.4
        y = -12 - (i % 3) * 2.5
        crowd.append(put(figure(f"porter{i}", ("#5A6A7A", "#8C6A4A", "#D8CCB0")[i % 3]), x, y, 0, zl))
        crowd.append(box(f"psack{i}", 0.7, 0.5, 0.4, (x, y, zl + 1.4), "#C9B48A"))
    m.add(2, join(crowd, "porters"), "life")
    trees(m, "willows", [(x, -10) for x in (-104, -50, -15, 45, 104)] + [(x, 31) for x in (-104, -35, 35, 104)], 3.2, WILLOW)
    return m


# ---------------------------------------------------------------- the East Water Gate

def east_water_gate():
    """The outer wall runs north-south (along Y) at x = 0 and the Bian flows east (+X) through the gate: towers on both banks,
    a covered gallery across the canal with an iron grille half lowered, and walled walkways out along both banks."""
    m = Model("east-water-gate")
    W, D = 90, 80
    RW = 14.0
    m.add(0, box("water", W, 2 * RW, 0.12, (0, 0, 0), WATERC), "walls")
    for s in (-1, 1):
        m.add(0, box(f"bank{s}", W, D / 2 - RW, 1.0, (0, s * (RW + (D / 2 - RW) / 2), 0), shade(EARTH, 0.04)))
        # the wall stubs north and south of the gate
        m.add(0, terrace(f"wall{s}", 16, D / 2 - RW - 7.5, 10.0, (0, s * (RW + 6 + (D / 2 - RW - 7.5) / 2), 1.0), EARTH, shade(EARTH, -0.12), batter=0.08))
        m.add(0, move(merlons(f"wmer{s}", 15, D / 2 - RW - 8.5, 11.0, 0.8, 1.3, shade(EARTH, -0.1)), 0, s * (RW + 6 + (D / 2 - RW - 7.5) / 2)))
        # the gate towers on the banks
        m.add(0, terrace(f"tower{s}", 22, 12, 12.0, (0, s * (RW + 4), 0.0), EARTH, BRICKF, batter=0.05), "towers")
        m.add(0, move(merlons(f"tmer{s}", 21, 11, 12.0, 0.8, 1.3, shade(BRICKF, 0.05)), 0, s * (RW + 4)))
        lou(m, f"lou{s}", 14, 8, 4.0, 3.2, 0, s * (RW + 4), z=12.0, plat=0.4, roof="hip", roof_h=4.4, trim=None, shibi=CHIWEI)
        # the walled walkways (guaizi cheng) out along the banks
        m.add(0, terrace(f"guaizi{s}", 34, 5, 6.0, (28, s * (RW + 3.5), 1.0), EARTH, shade(EARTH, -0.12), batter=0.06), "walls")
        m.add(0, crenel_line(f"gcren{s}", (11, s * (RW + 1.3)), (43.5, s * (RW + 1.3)), 7.0, shade(EARTH, -0.12), 0.7, 1.1, 0.6))
    # the gallery across the canal and the grille
    gal = gallery("gallery", [(0, -RW - 1), (0, RW + 1)], w=7, h=3.2, col=VERM, roof=TILE, floor=0.5)
    m.add(1, move(gal, 0, 0, 11.5), "gallery")
    frame = [box("g_beam", 8.0, 2 * RW + 2, 1.0, (0, 0, 10.6), WOOD)]
    for i in range(15):
        y = -RW + 1 + i * (2 * RW - 2) / 14
        frame.append(box(f"bar{i}", 0.3, 0.3, 6.6, (3.2, y, 4.0), DARKW))
    for z in (4.2, 7.0, 10.2):
        frame.append(box(f"bar_h{z}", 0.3, 2 * RW - 1.5, 0.3, (3.2, 0, z), DARKW))
    m.add(1, join(frame, "grille"))
    # a boat being hauled in, trackers on the inner bank
    m.add(2, put(boat("boat", 16.0, 4.4, cabin=0.45, mast=(1.0, 0, 9.0)), -26, -3, 0, 0.0), "life")
    crowd = [put(figure(f"tracker{i}", ("#5A6A7A", "#8C6A4A")[i % 2]), -40 + i * 2.2, RW + 2.5, 0, 1.0) for i in range(6)]
    crowd += [beam3d("towrope", (-20, -3, 3.0), (-28, RW + 2.5, 2.0), 0.06, 0.06, DARKW)]
    m.add(2, join(crowd, "trackers"))
    trees(m, "willows", [(-30, 30), (-40, -30), (40, 32), (40, -32), (-15, -32)], 3.2, WILLOW)
    return m


BUILDERS = {
    "kaifeng/iron-pagoda": iron_pagoda,
    "kaifeng/fan-pagoda": lambda: fan_pagoda("song"),
    "kaifeng/fan-pagoda-ming": lambda: fan_pagoda("ming"),
    "kaifeng/fan-pagoda-qing": lambda: fan_pagoda("qing"),
    "kaifeng/xiangguo-temple": xiangguo_temple,
    "kaifeng/xiangguo-temple-qing": xiangguo_qing,
    "kaifeng/song-palace": song_palace,
    "kaifeng/imperial-way": imperial_way,
    "kaifeng/rainbow-bridge": rainbow_bridge,
    "kaifeng/fan-tower": fan_tower,
    "kaifeng/genyue": genyue,
    "kaifeng/zhouqiao": lambda: zhouqiao("song"),
    "kaifeng/zhouqiao-ming": lambda: zhouqiao("ming"),
    "kaifeng/synagogue": synagogue,
    "kaifeng/south-gate": lambda: south_gate("song"),
    "kaifeng/south-gate-ming": lambda: south_gate("ming"),
    "kaifeng/zhou-palace": zhou_palace,
    "kaifeng/dragon-pavilion": dragon_pavilion,
    "kaifeng/yanqing-temple": yanqing_temple,
    "kaifeng/bian-wharves": bian_wharves,
    "kaifeng/east-water-gate": east_water_gate,
}
