"""Khanbaliq / Dadu / Beijing landmark miniatures.

The hall, gate, roof, wall and corridor helpers are copied from the Chang'an module (changan.py, itself from nara.py
and kyoto.py); the yellow-roofed palace halls, marble terraces, corner towers, the Meridian Gate, Tibetan dagobas,
gers, barges and the Ming gate are Khanbaliq's own."""
import math
import bpy
from chronokit import Model, box, cylinder, dome, join, shade, mesh_from
from worldkit import *

VERM = "#B04A32"          # red ochre on columns and brackets
WHITE = "#EDE5D3"         # whitewashed walls
TILE = "#5C5D60"          # grey tile
BARK = "#6E4B3A"
GLAZE = "#3F8A62"         # green glaze
GLAZE_TEAL = "#3C7F7A"
STONE = "#B9B1A2"
GRAVEL = "#DDD3BE"
EARTH = "#C4AE86"         # rammed loess
BRICKF = "#A49A8A"        # grey brick facing
MBRICK = "#8E8A84"        # Ming grey brick
CLAY = "#CDB994"          # courtyard walls
GRASS = "#9AA56E"
FIELD = "#B4AE78"
WOOD = "#6A5442"
DARKW = "#3A2E26"
PINE = "#557048"
WILLOW = "#93A660"
LOCUST = "#6F8A50"
CYPRESS = "#4E6646"
WATERC = "#5F878C"
CHIWEI = "#4F5754"
MRED = "#A8402C"          # Ming and Qing column red
MGREEN = "#3F7A58"        # green-glazed tile
YELLOW = "#D9A33A"        # imperial yellow glazed tile
YELLOW_D = "#B5832C"
PRED = "#9C3A2C"          # red-plastered palace walls
PRED_D = "#86322A"
JADE = "#EEEAE0"          # white marble (hanbaiyu)
JADE_D = "#D8D2C4"
BLUE_T = "#3E6795"        # blue glazed tile
PURPLE_T = "#6E4A6E"
BLACK_T = "#3B3C3E"       # black glazed tile
LATTICE = "#7E2E24"       # red lattice doors and windows
FELT = "#EDE6D6"
STUPA_W = "#F1EEE6"


# ---------------------------------------------------------------- helpers copied from changan.py
def shibi_fin(name, rt, loc, s, color=GILT):
    """A ridge-end ornament (shibi): an upright fin curling inward, s = -1 west end, +1 east end."""
    x, y, z = loc
    a = box(name + "_a", rt * 1.2, rt * 0.9, rt * 2.2, (x, y, z), color)
    b = box(name + "_b", rt * 1.0, rt * 0.8, rt * 1.4, (x - s * rt * 0.7, y, z + rt * 1.4), color)
    return join([a, b], name)


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


def tree_row(m, name, a, b, n, r=3.0, color=LOCUST, stage=2, z=0.0):
    (ax, ay), (bx, by) = a, b
    pts = [(ax + (bx - ax) * i / max(1, n - 1), ay + (by - ay) * i / max(1, n - 1), z) for i in range(n)]
    m.add(stage, grove(name, pts, r, color), "trees")


def trees(m, name, pts, r=4.5, color=PINE, stage=2):
    m.add(stage, grove(name, [(x, y, 0) for x, y in pts], r, color), "trees")


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


def ramp(name, x0, x1, y0, y1, z0, z1, color=BRICKF):
    """A ramp of width x0..x1 rising along Y from (y0, z0) to (y1, z1), a solid wedge down to z = 0."""
    verts = [(x0, y0, z0), (x1, y0, z0), (x1, y1, z1), (x0, y1, z1), (x0, y0, 0), (x1, y0, 0), (x1, y1, 0), (x0, y1, 0)]
    faces = [(0, 1, 2, 3), (4, 5, 1, 0), (5, 6, 2, 1), (6, 7, 3, 2), (7, 4, 0, 3), (7, 6, 5, 4)]
    return mesh_from(name, verts, faces, (0, 0, 0), color)


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



# ---------------------------------------------------------------- Khanbaliq parts
TEAL = "#3D6B68"          # blue-green painted brackets and beams (hexi caihua)


HILL_PROFILE = [(1.0, 0.0), (0.86, 0.22), (0.68, 0.5), (0.48, 0.74), (0.28, 0.9), (0.1, 0.99), (0.0, 1.0)]


def mound_z(q):
    """Height fraction of a mound at normalised radius q (0 at the top, 1 at the foot)."""
    if q >= 1.0:
        return 0.0
    for (r0, z0), (r1, z1) in zip(HILL_PROFILE, HILL_PROFILE[1:]):
        if r1 <= q <= r0:
            return z0 + (z1 - z0) * (r0 - q) / (r0 - r1)
    return 1.0


def mound(name, rx, ry, h, loc=(0, 0, 0), color=GRASS, segments=24, rings=10):
    """An elliptical hill rx by ry, h high, with slopes that steepen toward the top."""
    o = lathe(name, [(r, z) for r, z in HILL_PROFILE], (0, 0, 0), color, verts=segments)
    for v in o.data.vertices:
        v.co.x, v.co.y, v.co.z = v.co.x * rx, v.co.y * ry, v.co.z * h
    return move(o, *loc)


def ya_block(name, w, h, loc=(0, 0, 0), color=STUPA_W, k=0.74):
    """A square block with recessed corners (the 'ya'-shaped plan of Tibetan stupa podiums)."""
    x, y, z = loc
    return join([box(name + "_a", w, w * k, h, (x, y, z), color), box(name + "_b", w * k, w, h, (x, y, z), color)], name)


def xumizuo(name, w, d, h, loc=(0, 0, 0), color=JADE):
    """A Sumeru pedestal: plinth, recessed waist, projecting cap."""
    x, y, z = loc
    i = min(0.6, h * 0.15)
    return join([box(name + "_pl", w, d, h * 0.3, (x, y, z), color),
                 box(name + "_ws", w - 2 * i, d - 2 * i, h * 0.4, (x, y, z + h * 0.3), shade(color, -0.07)),
                 box(name + "_cp", w + 0.2, d + 0.2, h * 0.3, (x, y, z + h * 0.7), color)], name)


def marble_terrace(name, w, d, h, loc=(0, 0, 0), color=JADE, post_every=4.5, rail=True):
    """A white marble terrace with a balustrade round its edge."""
    x, y, z = loc
    parts = [xumizuo(name + "_x", w, d, h, loc, color)]
    if rail:
        parts.append(balustrade(name + "_bal", rect_pts(w - 0.5, d - 0.5, x, y), 1.1, color, post_every, True, z + h))
    return join(parts, name)


def imperial_stair(name, w, h, run, x, y, z=0.0, deg=0.0, color=JADE, n=6):
    """Steps climbing h over run toward +Y from (x, y), with a sloping carved slab (the 'imperial way') up the middle."""
    parts = [box(f"{name}_s{i}", w, run * (n - i) / n, h / n, (0, -run * (n - i) / n / 2, i * h / n), color) for i in range(n)]
    rw = w * 0.3
    parts.append(ramp(name + "_slab", -rw / 2, rw / 2, -run, 0, 0.12, h + 0.06, shade(color, -0.1)))
    return put(join(parts, name), x, y, deg, z)


def imperial_hall(m, name, w, d, h, x=0.0, y=0.0, z=0.0, deg=0.0, roof="hip", double=True, roof_color=YELLOW, trim=None,
                  bays=None, col=MRED, wall=LATTICE, roof_h=None, plat=0.0, plat_color=JADE, sb=1, sr=2, ridge=None, bk=True,
                  chiwen=True, over=None, bk_mult=1, lattice=False, beasts=0):
    """A Ming-Qing hall: red columns and lattice, blue-green brackets, a hipped (hip), hip-and-gable (xieshan) or
    pyramidal (pyramid) roof, single or double-eaved. Returns the height of the ridge."""
    n = bays or max(3, round(w / 5.5))
    body = hall_body(name, w, d, h, plat=plat, col=col, wall=wall, bays=n, plat_color=plat_color, stairs=False)
    m.add(sb, put(body, x, y, deg, z), "halls")
    zt = plat + h
    bh = max(0.5, h * 0.08)
    m.add(sb, put(box(name + "_band", w + 0.4, d + 0.4, bh, (0, 0, zt - bh), TEAL), x, y, deg, z))
    if bk:
        bs = max(0.45, min(w, d) * 0.026)
        nd = max(2, round(d / 5.5))
        m.add(sb, put(brackets(name + "_bk", w + 0.4, d + 0.4, zt - 0.1, n * bk_mult, nd * bk_mult, bs, TEAL), x, y, deg, z))
        zt += bs * 1.3
    if lattice:
        lp = []
        bw = w / n
        for i in range(n):
            cx = -w / 2 + bw * (i + 0.5)
            for f in (-1, 1):
                for k in range(7):
                    lp.append(box(f"{name}_lv{i}{f}{k}", 0.16, 0.2, h * 0.62, (cx - bw * 0.3 + k * bw * 0.1, f * (d / 2 - 0.15), plat + h * 0.18), GILT))
                for k in range(3):
                    lp.append(box(f"{name}_lh{i}{f}{k}", bw * 0.66, 0.2, 0.16, (cx, f * (d / 2 - 0.15), plat + h * (0.25 + k * 0.2)), GILT))
        m.add(sb, put(join(lp, name + "_lattice"), x, y, deg, z))
    rc = ridge or shade(roof_color, -0.2)
    cw = shade(roof_color, -0.12) if chiwen else None
    rparts = []
    def beast_row(tag, W, D, z0, zc, inner, nb):
        """Little glazed beasts in a row up each corner ridge, from the eave corner toward the ridge."""
        out = []
        for sx in (-1, 1):
            for sy in (-1, 1):
                a = (sx * W / 2, sy * D / 2, z0)
                b = (sx * inner[0], sy * inner[1], zc)
                for k in range(nb):
                    t = 0.06 + 0.07 * k
                    out.append(box(f"{name}_{tag}b{sx}{sy}{k}", 0.55, 0.55, 0.75, (a[0] + (b[0] - a[0]) * t, a[1] + (b[1] - a[1]) * t, a[2] + (b[2] - a[2]) * t), shade(roof_color, -0.25)))
        return out

    if double:
        le_h = max(1.4, min(w, d) * 0.13)
        o = over if over is not None else max(1.8, min(w, d) * 0.2)
        rparts.append(eaved_roof(name + "_le", w + 0.6, d + 0.6, le_h, (0, 0, zt), roof_color, over=o, curve=0.2))
        if beasts:
            W, D = w + 0.6 + 2 * o, d + 0.6 + 2 * o
            rparts += beast_row("l", W, D, zt + le_h * 0.2 + 0.2, zt + le_h * 0.12 + 0.2, (W * 0.42, D * 0.42), beasts)
        uw, ud = w * 0.9, d * 0.82
        dz = zt + le_h * 0.35
        dh = le_h + 0.6
        rparts.append(box(name + "_drum", uw, ud, dh, (0, 0, dz), wall))
        rparts.append(box(name + "_dband", uw + 0.3, ud + 0.3, 0.5, (0, 0, dz + dh - 0.5), TEAL))
        zt2 = dz + dh
    else:
        uw, ud, zt2 = w, d, zt
    rh = roof_h or (ud * 0.6 if roof == "hip" else ud * 0.66 if roof == "xieshan" else max(uw, ud) * 0.62)
    if beasts and roof in ("hip", "xieshan"):
        o2 = min(uw, ud) * (0.22 if roof == "hip" else 0.24)
        W, D = uw + 2 * o2, ud + 2 * o2
        if roof == "hip":
            rparts += beast_row("u", W, D, zt2 + rh * 0.18 + 0.2, zt2 + rh + 0.2, (max(0.0, (W - D) * 0.5) / 2, 0.0), beasts)
        else:
            rparts += beast_row("u", W, D, zt2 + rh * 0.16 + 0.2, zt2 + rh * 0.42 + 0.2, (max(W - D * 0.6, W * 0.35) / 2, D * 0.21), beasts)
    if roof == "hip":
        rparts.append(hip(name + "_up", uw, ud, rh, (0, 0, zt2), roof_color, over=min(uw, ud) * 0.22, ridge=rc, trim=trim, shibi=cw))
    elif roof == "xieshan":
        rparts.append(irimoya(name + "_up", uw, ud, rh, (0, 0, zt2), roof_color, over=min(uw, ud) * 0.24, ridge=rc, gable=PRED, shibi=cw))
    else:
        rparts.append(eaved_roof(name + "_up", uw, ud, rh, (0, 0, zt2), roof_color, over=min(uw, ud) * 0.25, curve=0.2))
        rparts.append(dome(name + "_ball", max(0.45, uw * 0.05), (0, 0, zt2 + rh - 0.25), GILT, squash=1.3, segments=10, rings=6))
    m.add(sr, put(join(rparts, name + "_roofs"), x, y, deg, z), "roofs")
    return z + zt2 + rh


def plain_hall(name, w, d, h, roof=TILE, wall=CLAY, ridge_dir="x", rh=None):
    """A small hall as a block under a gabled roof: side buildings, storerooms, houses. Returns one object."""
    rh = rh or min(w, d) * 0.38
    parts = [box(name + "_b", w, d, h, (0, 0, 0), wall)]
    if ridge_dir == "x":
        parts.append(seg_prism(name + "_r", (-w / 2 - 0.6, 0), (w / 2 + 0.6, 0), h, d + 1.6, rh, roof))
    else:
        parts.append(seg_prism(name + "_r", (0, -d / 2 - 0.6), (0, d / 2 + 0.6), h, w + 1.6, rh, roof))
    return join(parts, name)


def block_hall(name, w, d, h, roof=YELLOW, wall=PRED, rh=None):
    """A hall reduced to a red block under a hipped glazed roof: the side palaces of the Forbidden City."""
    rh = rh or min(w, d) * 0.5
    return join([box(name + "_b", w, d, h, (0, 0, 0), wall), eaved_roof(name + "_r", w, d, rh, (0, 0, h), roof, over=min(w, d) * 0.16, curve=0.16)], name)


def red_wall(name, pts, h=6.0, t=1.6, color=PRED, cap=YELLOW, closed=False):
    """A red-plastered palace wall with a glazed tile coping."""
    return wall_line(name, pts, h, t, color, cap, closed)


def corner_tower(name, s=12.0, roof=YELLOW, col=MRED, wall=LATTICE):
    """A corner tower of the Forbidden City type: a cross-shaped pavilion of a square core and four porches, a skirt of eaves,
    hip-and-gable roofs over the porches and two crossed hip-and-gable roofs on top, with a gilt finial."""
    h = s * 0.5
    parts = [box(name + "_base", s * 1.6, s * 1.6, 0.6, (0, 0, 0), JADE)]
    parts.append(box(name + "_core", s, s, h, (0, 0, 0.6), wall))
    for k in range(4):
        a = math.pi / 2 * k
        cx, cy = math.cos(a) * s * 0.62, math.sin(a) * s * 0.62
        pw, pd = (s * 0.3, s * 0.62) if k % 2 == 0 else (s * 0.62, s * 0.3)
        parts.append(box(f"{name}_po{k}", pw, pd, h * 0.82, (cx, cy, 0.6), wall))
        for sgn in (-1, 1):
            if k % 2 == 0:
                parts.append(box(f"{name}_pc{k}{sgn}", 0.5, 0.5, h * 0.82, (cx + math.cos(a) * s * 0.14, cy + sgn * s * 0.3, 0.6), col))
            else:
                parts.append(box(f"{name}_pc{k}{sgn}", 0.5, 0.5, h * 0.82, (cx + sgn * s * 0.3, cy + math.sin(a) * s * 0.14, 0.6), col))
    z1 = 0.6 + h * 0.82
    parts.append(eaved_roof(name + "_skirt", s * 1.55, s * 1.55, s * 0.22, (0, 0, z1), roof, over=s * 0.14, curve=0.3))
    for k in range(4):
        a = math.pi / 2 * k
        cx, cy = math.cos(a) * s * 0.66, math.sin(a) * s * 0.66
        r = irimoya(f"{name}_pr{k}", s * 0.66, s * 0.36, s * 0.34, (0, 0, 0), roof, over=s * 0.1, gable=PRED)
        if k % 2 == 0:
            r = rot(r, 90)
        parts.append(move(r, cx, cy, z1 + s * 0.1))
    z2 = 0.6 + h + s * 0.08
    parts.append(box(name + "_drum", s * 0.8, s * 0.8, s * 0.22, (0, 0, z2 - s * 0.08), wall))
    t1 = irimoya(name + "_t1", s * 1.0, s * 0.62, s * 0.55, (0, 0, 0), roof, over=s * 0.14, gable=PRED)
    t2 = rot(irimoya(name + "_t2", s * 1.0, s * 0.62, s * 0.55, (0, 0, 0), roof, over=s * 0.14, gable=PRED), 90)
    parts += [move(t1, 0, 0, z2 + s * 0.12), move(t2, 0, 0, z2 + s * 0.12)]
    parts.append(dome(name + "_fin", s * 0.07, (0, 0, z2 + s * 0.12 + s * 0.53), GILT, squash=1.4, segments=10, rings=6))
    return join(parts, name)


def tib_stupa(name, H, color=STUPA_W, tiers=2, eye=False, canopy=BRONZE, top=GILT, podium=None):
    """A Tibetan-style stupa (dagoba) H high: ya-shaped podium tiers, lotus base, bell-shaped body,
    ya-shaped neck, a tapering spire of thirteen rings, a canopy hung with bells and a gilt top."""
    parts = []
    z = 0.0
    pw = podium or H * 0.6
    ph = H * 0.17
    for t in range(tiers):
        w = pw * (1 - 0.13 * t)
        h = ph / tiers
        parts.append(ya_block(f"{name}_pod{t}", w, h * 0.86, (0, 0, z), color))
        parts.append(ya_block(f"{name}_cor{t}", w + 0.5, h * 0.14, (0, 0, z + h * 0.86), shade(color, -0.06)))
        z += h
    R = H * 0.17
    parts.append(lathe(name + "_lotus", [(R * 1.32, 0), (R * 1.36, H * 0.012), (R * 1.22, H * 0.03), (R * 1.08, H * 0.045)], (0, 0, z), shade(color, -0.04), verts=28))
    z += H * 0.045
    body = [(R * 0.94, 0), (R * 1.0, H * 0.05), (R * 1.04, H * 0.11), (R * 1.0, H * 0.16), (R * 0.86, H * 0.2), (R * 0.6, H * 0.235), (R * 0.42, H * 0.25)]
    parts.append(lathe(name + "_body", body, (0, 0, z), color, verts=32))
    if eye:
        parts.append(arch_panel(name + "_eye", R * 0.5, R * 0.75, (0, -R * 1.02, z + H * 0.05), "S", "#A8302A", pointed=False, depth=R * 0.2))
        parts.append(box(name + "_eyeg", R * 0.18, R * 0.12, R * 0.22, (0, -R * 1.1, z + H * 0.1), GILT))
    z += H * 0.25
    parts.append(ya_block(name + "_neck", R * 0.95, H * 0.035, (0, 0, z), color))
    z += H * 0.035
    sp = H * 0.24
    parts.append(cylinder(name + "_spire", R * 0.52, sp, (0, 0, z), color, verts=20, r_top=R * 0.26))
    for k in range(13):
        rr = R * (0.53 - 0.27 * (k + 0.5) / 13)
        parts.append(cylinder(f"{name}_ring{k}", rr + 0.12, sp / 13 * 0.25, (0, 0, z + sp * (k + 0.6) / 13), shade(color, -0.1), verts=20))
    z += sp
    parts.append(cylinder(name + "_canopy", R * 0.78, H * 0.012, (0, 0, z), canopy, verts=24, r_top=R * 0.7))
    parts.append(cylinder(name + "_canopy2", R * 0.7, H * 0.025, (0, 0, z + H * 0.012), canopy, verts=24, r_top=R * 0.25))
    for k in range(12):
        a = math.tau * k / 12
        parts.append(box(f"{name}_bell{k}", 0.25, 0.25, 0.7, (math.cos(a) * R * 0.74, math.sin(a) * R * 0.74, z - 0.7), canopy))
    z += H * 0.035
    parts.append(lathe(name + "_top", [(R * 0.16, 0), (R * 0.2, H * 0.012), (R * 0.16, H * 0.03), (R * 0.08, H * 0.045), (R * 0.1, H * 0.055), (0, H * 0.075)], (0, 0, z), top, verts=14))
    return join(parts, name)


def ger(name, r, loc=(0, 0, 0), color=FELT, deg=0.0):
    """A Mongol felt tent: a lattice wall cylinder, a domed roof with a smoke ring, a painted door facing south."""
    x, y, z = loc
    h = r * 0.6
    parts = [cylinder(name + "_w", r, h, (0, 0, 0), color, verts=14),
             cylinder(name + "_r", r * 1.03, r * 0.42, (0, 0, h), shade(color, -0.04), verts=14, r_top=r * 0.18),
             cylinder(name + "_ring", r * 0.2, r * 0.06, (0, 0, h + r * 0.42), WOOD, verts=10),
             box(name + "_band", r * 2.06, 0.15, 0.25, (0, 0, h * 0.55), "#8A3A2E"),
             box(name + "_door", r * 0.45, 0.3, h * 0.85, (0, -r + 0.05, 0), "#B04A32")]
    o = join(parts, name)
    if deg:
        o = rot(o, deg)
    return move(o, x, y, z)


def barge(name, L, W, loc=(0, 0, 0), deg=0.0, cargo=True):
    """A canal barge: a long hull pointed at both ends, a mat-roofed cabin at the stern, a mast, sacks of grain."""
    x, y, z = loc
    e = L * 0.15
    pts = [(-L / 2, 0), (-L / 2 + e, -W / 2), (L / 2 - e, -W / 2), (L / 2, 0), (L / 2 - e, W / 2), (-L / 2 + e, W / 2)]
    parts = [prism(name + "_hull", pts, 1.3, (0, 0, 0), WOOD),
             box(name + "_deck", L - 2 * e, W * 0.86, 0.12, (0, 0, 1.3), shade(WOOD, 0.15)),
             box(name + "_cab", L * 0.22, W * 0.8, 1.5, (-L * 0.3, 0, 1.3), shade(WOOD, 0.08)),
             seg_prism(name + "_mat", (-L * 0.42, 0), (-L * 0.18, 0), 2.8, W * 0.95, 0.9, "#8C7650"),
             cylinder(name + "_mast", 0.14, L * 0.45, (L * 0.05, 0, 1.3), DARKW, verts=6)]
    if cargo:
        for i in range(4):
            for j in (-1, 1):
                parts.append(box(f"{name}_sk{i}{j}", 1.2, W * 0.36, 0.7, (L * 0.12 + i * 1.4 - 1.5, j * W * 0.2, 1.42), "#D8C9A0"))
    o = join(parts, name)
    if deg:
        o = rot(o, deg)
    return move(o, x, y, z)


def taihu_rocks(name, pts, s=2.0, color="#9C978C"):
    """Clusters of eroded garden rocks: tilted boxes at the given (x, y, z) points."""
    parts = []
    for i, (x, y, z) in enumerate(pts):
        k = 0.7 + 0.5 * ((i * 37) % 11) / 11
        parts.append(box(f"{name}{i}", s * k, s * 0.8 * k, s * 1.3 * k, (x, y, z - 0.3), shade(color, 0.05 * ((i % 3) - 1)), rot_z=i * 0.9))
    return join(parts, name)


def round_pavilion(name, r, h1, h2, roof=BLUE_T, col=MRED, wall=LATTICE, trim=None):
    """A round double-eaved pavilion on a stone base with a gilt finial."""
    parts = [cylinder(name + "_pl", r * 1.45, 1.0, (0, 0, 0), JADE, verts=20)]
    parts.append(cylinder(name + "_w1", r, h1, (0, 0, 1.0), wall, verts=16))
    for k in range(8):
        a = math.tau * k / 8
        parts.append(box(f"{name}_c{k}", 0.45, 0.45, h1, (r * math.cos(a), r * math.sin(a), 1.0), col))
    parts.append(cylinder(name + "_e1", r * 1.65, h1 * 0.32, (0, 0, 1.0 + h1), roof, verts=20, r_top=r * 0.8))
    if trim:
        parts.append(cylinder(name + "_t1", r * 1.67, 0.3, (0, 0, 1.0 + h1), trim, verts=20))
    z2 = 1.0 + h1 + h1 * 0.22
    parts.append(cylinder(name + "_w2", r * 0.74, h2, (0, 0, z2), wall, verts=16))
    parts.append(cylinder(name + "_e2", r * 1.35, r * 1.15, (0, 0, z2 + h2), roof, verts=20, r_top=r * 0.08))
    if trim:
        parts.append(cylinder(name + "_t2", r * 1.37, 0.3, (0, 0, z2 + h2), trim, verts=20))
    parts.append(dome(name + "_jw", r * 0.15, (0, 0, z2 + h2 + r * 1.2), GILT, squash=1.4, segments=10, rings=6))
    return join(parts, name)


def square_pavilion(name, w, h, eaves=1, roof=YELLOW, col=MRED, wall=LATTICE, base=1.0, trim=None):
    """A square pavilion with one to three pyramidal eaves and a gilt finial."""
    parts = [box(name + "_pl", w * 1.45, w * 1.45, base, (0, 0, 0), JADE)]
    parts.append(box(name + "_w", w * 0.8, w * 0.8, h, (0, 0, base), wall))
    for sx in (-1, 1):
        for sy in (-1, 1):
            parts.append(box(f"{name}_c{sx}{sy}", 0.5, 0.5, h, (sx * w * 0.42, sy * w * 0.42, base), col))
    z = base + h
    ww = w
    for k in range(eaves):
        last = k == eaves - 1
        rh = ww * (0.62 if last else 0.22)
        parts.append(box(f"{name}_bd{k}", ww * 0.92, ww * 0.92, 0.5, (0, 0, z - 0.5), TEAL))
        parts.append(eaved_roof(f"{name}_e{k}", ww, ww, rh, (0, 0, z), roof, over=ww * 0.26, curve=0.24))
        if trim:
            parts.append(box(f"{name}_tr{k}", ww * 1.5, ww * 1.5, 0.3, (0, 0, z + rh * 0.1), trim))
        if not last:
            ww *= 0.78
            parts.append(box(f"{name}_dr{k}", ww * 0.8, ww * 0.8, ww * 0.36, (0, 0, z + rh * 0.4), wall))
            z += rh * 0.4 + ww * 0.36
        else:
            z += rh
    parts.append(dome(name + "_jw", max(0.35, w * 0.06), (0, 0, z - 0.3), GILT, squash=1.4, segments=10, rings=6))
    return join(parts, name)


def scatter_trees(m, name, pts, r=4.0, color=PINE, stage=2):
    m.add(stage, grove(name, pts, r, color), "trees")


def golden_water(name, x0, x1, y0, sag, width=6.0, n=10, color=WATERC, bank=JADE):
    """A bow-shaped stream bending south between x0 and x1 (the Golden Water stream), with marble banks."""
    parts = []
    for i in range(n):
        xa, xb = x0 + (x1 - x0) * i / n, x0 + (x1 - x0) * (i + 1) / n
        ya = y0 - sag * (1 - ((2 * (xa - x0) / (x1 - x0)) - 1) ** 2)
        yb = y0 - sag * (1 - ((2 * (xb - x0) / (x1 - x0)) - 1) ** 2)
        L = math.hypot(xb - xa, yb - ya) + 0.3
        a = math.atan2(yb - ya, xb - xa)
        cx, cy = (xa + xb) / 2, (ya + yb) / 2
        parts.append(box(f"{name}_w{i}", L, width, 0.35, (cx, cy, 0), color, rot_z=a))
        for sgn in (-1, 1):
            parts.append(box(f"{name}_b{i}{sgn}", L, 0.6, 0.9, (cx - math.sin(a) * sgn * (width / 2 + 0.3), cy + math.cos(a) * sgn * (width / 2 + 0.3), 0), bank, rot_z=a))
    return join(parts, name)


def marble_bridges(name, xs, y, length=12.0, w=4.5, h=1.4, color=JADE):
    parts = []
    for i, x in enumerate(xs):
        parts.append(box(f"{name}_d{i}", w, length, h, (x, y, 0), color))
        for sgn in (-1, 1):
            parts.append(box(f"{name}_r{i}{sgn}", 0.35, length, 0.9, (x + sgn * (w / 2 - 0.2), y, h), color))
    return join(parts, name)


def huabiao(name, h=9.6, loc=(0, 0, 0), color=JADE):
    """A carved marble column with a cloud board and a crouching beast on top."""
    x, y, z = loc
    parts = [box(name + "_b", 2.2, 2.2, 0.8, (x, y, z), color), cylinder(name + "_c", 0.5, h, (x, y, z + 0.8), color, verts=8),
             box(name + "_cloud", 2.4, 0.35, 0.8, (x, y, z + h * 0.78), color), cylinder(name + "_cap", 0.8, 0.5, (x, y, z + h + 0.8), color, verts=10),
             dome(name + "_beast", 0.45, (x, y, z + h + 1.3), color, squash=1.4, segments=8, rings=5)]
    return join(parts, name)


def stone_lion(name, loc=(0, 0, 0), color="#9E978A"):
    x, y, z = loc
    return join([box(name + "_b", 1.8, 2.6, 1.4, (x, y, z), JADE), box(name + "_body", 1.2, 1.8, 1.4, (x, y, z + 1.4), color),
                 dome(name + "_h", 0.6, (x, y - 0.5, z + 2.6), color, squash=1.1, segments=8, rings=5)], name)


def gate_tower_on_wall(m, name, w, d, wall_h, x=0.0, y=0.0, deg=0.0, roof=YELLOW, sb=1, sr=2, double=True, roof_kind="hip"):
    """A palace gate: a red block in the wall line with an arched passage, a hall on top."""
    blk = [box(name + "_blk", w + 6, d + 4, wall_h, (0, 0, 0), PRED), box(name + "_pl", w + 6.4, d + 4.4, 0.8, (0, 0, 0), JADE)]
    for f, fy in (("S", -(d + 4) / 2 - 0.05), ("N", (d + 4) / 2 + 0.05)):
        blk.append(arch_panel(f"{name}_a{f}", min(5.0, w * 0.18), wall_h * 0.6, (0, fy, 0), f, DARK, pointed=False, depth=0.5))
    m.add(0, put(join(blk, name + "_platform"), x, y, deg), "walls")
    return imperial_hall(m, name + "_hall", w, d, w * 0.15 + 2.5, x, y, z=wall_h, deg=deg, roof=roof_kind, double=double, roof_color=roof, sb=sb, sr=sr, bk=False)


def pailou5(name, w, h, col=MRED, roof=YELLOW, board=TEAL):
    """A five-opening timber gateway with roofs at three levels, the middle highest."""
    parts = []
    xs = [-w / 2 + w * i / 5 for i in range(6)]
    hs = [0.72, 0.86, 1.0, 0.86, 0.72]
    for i, x in enumerate(xs):
        ph = h * max(hs[max(0, i - 1)], hs[min(4, i)])
        parts.append(box(f"{name}_post{i}", 1.0, 1.0, ph, (x, 0, 0), col))
        parts.append(box(f"{name}_foot{i}", 2.2, 2.6, 1.2, (x, 0, 0), JADE))
    for k in range(5):
        x0, x1 = xs[k], xs[k + 1]
        cx, L = (x0 + x1) / 2, x1 - x0
        hh = h * hs[k]
        parts.append(box(f"{name}_door{k}", L - 1.2, 0.5, hh * 0.45, (cx, 0, 0), "#7A2A22"))
        parts.append(box(f"{name}_beam{k}", L + 1.0, 1.0, 1.2, (cx, 0, hh - 3.2), col))
        parts.append(box(f"{name}_board{k}", L * 0.7, 0.5, 1.6, (cx, -0.1, hh - 2.0), board))
        parts.append(box(f"{name}_bk{k}", L + 0.6, 1.6, 0.7, (cx, 0, hh - 0.4), TEAL))
        parts.append(eaved_roof(f"{name}_roof{k}", L + 0.8, 2.6, 2.2, (cx, 0, hh + 0.3), roof, over=1.4, curve=0.3))
    return join(parts, name)


# ---------------------------------------------------------------- towers, gates, bridge, harbour

def drum_tower():
    m = Model("drum-tower")
    W, D, BH = 56.0, 34.0, 13.0
    m.add(0, box("plinth", W + 1.0, D + 1.0, 1.2, (0, 0, 0), JADE_D), "base")
    m.add(0, frustum("base", W, D, W - 0.8, D - 0.8, BH, (0, 0, 0), PRED))
    m.add(0, box("cope", W + 0.4, D + 0.4, 0.6, (0, 0, BH - 0.6), MBRICK))
    for i, x in enumerate((-14, 0, 14)):
        m.add(0, arch_panel(f"ts{i}", 6.0, 8.5, (x, -D / 2, 0.0), "S", DARK, pointed=False, depth=0.9))
        m.add(0, arch_panel(f"tn{i}", 6.0, 8.5, (x, D / 2, 0.0), "N", DARK, pointed=False, depth=0.9))
    m.add(0, balustrade("rail", rect_pts(W - 1.2, D - 1.2), 1.1, MBRICK, 3.5, True, BH))
    lou(m, "tower", 44, 22, 7.5, 6.0, 0, 0, z=BH, plat=0.8, roof="irimoya", roof_h=8.5, roof_color=TILE, col=MRED, double_top=True,
        ridge=shade(TILE, -0.3), bays=5, plat_color=MBRICK, shibi=MGREEN)
    m.add(2, join([box(f"trim{s}", 50, 0.7, 0.4, (0, s * 12.6, BH + 0.8 + 7.5 + 0.2), MGREEN) for s in (-1, 1)], "trim"), "roofs")
    m.add(1, cylinder("drum", 2.4, 1.6, (0, -6, BH + 0.8), "#8A3A2A", verts=16))
    return m


def bell_tower(variant="qing"):
    m = Model("bell-tower" if variant == "qing" else "bell-tower-1450")
    B = 31.0
    if variant == "qing":
        BH = 15.0
        m.add(0, box("plinth", B + 1, B + 1, 1.2, (0, 0, 0), JADE_D), "base")
        m.add(0, frustum("base", B, B, B - 0.8, B - 0.8, BH, (0, 0, 0), MBRICK))
        m.add(0, box("cope", B + 0.4, B + 0.4, 0.7, (0, 0, BH - 0.7), JADE_D))
        for f, (fx, fy) in (("S", (0, -B / 2)), ("N", (0, B / 2)), ("E", (B / 2, 0)), ("W", (-B / 2, 0))):
            m.add(0, arch_panel(f"t{f}", 6.0, 8.0, (fx, fy, 0.0), f, DARK, pointed=False, depth=0.9))
        m.add(0, balustrade("rail", rect_pts(B - 1.2, B - 1.2), 1.1, JADE, 3.0, True, BH))
        U, UH = 21.0, 13.0
        up = [box("upper", U, U, UH, (0, 0, BH), MBRICK)]
        for sx in (-1, 1):
            for sy in (-1, 1):
                up.append(box(f"pil{sx}{sy}", 1.2, 1.2, UH, (sx * (U / 2 - 0.4), sy * (U / 2 - 0.4), BH), JADE_D))
        up.append(box("band", U + 0.6, U + 0.6, 0.8, (0, 0, BH + UH - 0.8), JADE_D))
        for f, (fx, fy) in (("S", (0, -U / 2)), ("N", (0, U / 2)), ("E", (U / 2, 0)), ("W", (-U / 2, 0))):
            up.append(arch_panel(f"u{f}", 5.0, 8.5, (fx, fy, BH + 1.0), f, DARK, pointed=False, depth=0.6))
        m.add(1, join(up, "upper"), "tower")
        z = BH + UH
        r = [eaved_roof("le", U + 0.4, U + 0.4, 2.6, (0, 0, z), BLACK_T, over=2.8, curve=0.24),
             box("le_trim", U + 6.2, U + 6.2, 0.35, (0, 0, z + 0.4), MGREEN),
             box("drum", 17.5, 17.5, 3.0, (0, 0, z + 0.9), MBRICK),
             irimoya("top", 17.5, 17.5, 10.5, (0, 0, z + 3.9), BLACK_T, over=3.4, ridge=MGREEN, gable=MBRICK, shibi=MGREEN)]
        m.add(2, join(r, "roofs"), "roofs")
    else:
        BH = 10.0
        m.add(0, frustum("base", B, B, B - 0.8, B - 0.8, BH, (0, 0, 0), PRED), "base")
        m.add(0, box("plinth", B + 1, B + 1, 1.0, (0, 0, 0), JADE_D))
        for f, (fx, fy) in (("S", (0, -B / 2)), ("N", (0, B / 2)), ("E", (B / 2, 0)), ("W", (-B / 2, 0))):
            m.add(0, arch_panel(f"t{f}", 6.0, 7.0, (fx, fy, 0.0), f, DARK, pointed=False, depth=0.9))
        m.add(0, balustrade("rail", rect_pts(B - 1.2, B - 1.2), 1.1, MBRICK, 3.0, True, BH))
        lou(m, "tower", 22, 22, 7.5, 6.5, 0, 0, z=BH, plat=0.8, roof="irimoya", roof_h=9.0, roof_color=TILE, col=MRED, double_top=True,
            ridge=MGREEN, bays=5, plat_color=MBRICK, shibi=MGREEN)
    return m


def yuan_towers():
    m = Model("yuan-towers")
    m.add(0, box("ground", 60, 220, 0.25, (0, 0, 0), shade(EARTH, 0.05)), "base")
    m.add(0, box("street", 12, 200, 0.06, (0, 0, 0.25), shade(EARTH, -0.12)))
    # the Qizheng tower (drums and water-clock) to the south, the bell tower to the north
    m.add(0, terrace("dbase", 44, 30, 9.0, (0, -78, 0), EARTH, BRICKF, batter=0.05), "base")
    m.add(0, arch_panel("dtun_s", 6, 6.5, (0, -93.3, 0), "S", DARK, pointed=False, depth=0.8))
    m.add(0, arch_panel("dtun_n", 6, 6.5, (0, -62.7, 0), "N", DARK, pointed=False, depth=0.8))
    m.add(0, move(merlons("dmer", 43, 29, 9.0, 0.8, 1.4, shade(BRICKF, 0.05)), 0, -78))
    lou(m, "drum", 32, 18, 7.0, 5.5, 0, -78, z=9.0, plat=0.6, roof="hip", roof_h=7.5, roof_color=TILE, col=VERM, ridge=shade(TILE, -0.3), shibi=CHIWEI, bays=5)
    m.add(0, terrace("bbase", 26, 26, 8.0, (0, 80, 0), EARTH, BRICKF, batter=0.05))
    m.add(0, arch_panel("btun_s", 5, 6, (0, 66.6, 0), "S", DARK, pointed=False, depth=0.8))
    m.add(0, move(merlons("bmer", 25, 25, 8.0, 0.8, 1.4, shade(BRICKF, 0.05)), 0, 80))
    lou(m, "bell", 17, 17, 6.5, 5.5, 0, 80, z=8.0, plat=0.6, roof="irimoya", roof_h=7.5, roof_color=TILE, col=VERM, ridge=shade(TILE, -0.3), shibi=CHIWEI, bays=3)
    # market stalls along the street between them
    m.add(1, put(shop_row("stw", -45, 45, 16, 6, 4.0, unit=10, face=-1), 0, 0, 90), "market")
    m.add(1, put(shop_row("ste", -45, 45, -16, 6, 4.0, unit=10, face=1), 0, 0, 90))
    trees(m, "trees", [(-22, -40), (22, 40), (-22, 55), (22, -50)], 3.5, LOCUST)
    return m


def ming_gate():
    """A Ming Inner City gate: the wall with its gate tower, the barbican and the arrow tower (built facing -Y, outward)."""
    m = Model("ming-gate")
    W, wall_h, yw = 110.0, 11.0, 32.0
    m.add(0, box("ground", W, 100, 0.3, (0, 0, 0), shade(EARTH, 0.04)), "walls")
    m.add(0, frustum("wall", W, 18, W, 14, wall_h, (0, yw, 0.3), MBRICK))
    m.add(0, crenel_line("cren", (-W / 2, yw - 6.6), (W / 2, yw - 6.6), wall_h + 0.3))
    m.add(0, box("parapet_n", W, 0.7, 1.0, (0, yw + 6.7, wall_h + 0.3), MBRICK))
    m.add(0, box("walk", W, 13, 0.08, (0, yw, wall_h + 0.3), shade(MBRICK, 0.12)))
    m.add(1, arch_panel("pass_s", 6.0, 8.0, (0, yw - 9.0, 0.3), "S", DARK, pointed=False, depth=0.8), "gates")
    m.add(1, arch_panel("pass_n", 6.0, 8.0, (0, yw + 9.0, 0.3), "N", DARK, pointed=False, depth=0.8))
    for s in (-1, 1):
        verts = [(s * 20, yw + 9, wall_h + 0.3), (s * 20, yw + 15, wall_h + 0.3), (s * 52, yw + 15, 0.3), (s * 52, yw + 9, 0.3), (s * 20, yw + 9, 0.3), (s * 20, yw + 15, 0.3)]
        m.add(0, mesh_from(f"mdao{s}", verts, [(0, 1, 2, 3), (4, 5, 1, 0), (3, 4, 0), (5, 2, 1), (3, 2, 5, 4)], (0, 0, 0), shade(MBRICK, 0.05)))
    # the barbican
    for s in (-1, 1):
        m.add(0, frustum(f"bw{s}", 10, 66, 8, 66, wall_h, (s * 39, -10, 0.3), MBRICK))
        m.add(0, crenel_line(f"bc{s}", (s * 43.4, -43), (s * 43.4, 22), wall_h + 0.3))
    m.add(0, frustum("bw_s", 88, 10, 88, 8, wall_h, (0, -44, 0.3), MBRICK))
    m.add(1, arch_panel("bgate", 5.5, 7.0, (44.1, -5, 0.3), "E", DARK, pointed=False, depth=0.8))
    m.add(1, put(plain_hall("temple", 10, 7, 4.0, TILE, MRED), -20, -20, 0, 0.3))
    jl = [box("jianlou", 50, 13, 9.0, (0, -44, wall_h + 0.3), shade(MBRICK, 0.06))]
    for r in range(4):
        for i in range(12):
            jl.append(box(f"win{r}_{i}", 1.1, 0.4, 1.1, (-22.6 + i * 4.1, -50.6, wall_h + 1.4 + r * 2.0), DARK))
        for i in range(2):
            for s in (-1, 1):
                jl.append(box(f"wins{r}_{i}{s}", 0.4, 1.1, 1.1, (s * 25.1, -46.5 + i * 5, wall_h + 1.4 + r * 2.0), DARK))
    m.add(1, join(jl, "arrow_tower"))
    m.add(2, irimoya("jl_r", 50, 13, 6.5, (0, -44, wall_h + 9.3), TILE, over=2.3, ridge=MGREEN, gable=MBRICK), "roofs")
    m.add(2, eaved_roof("jl_pent", 52, 15, 1.4, (0, -44, wall_h + 7.7), TILE, over=1.5, curve=0.15))
    lou(m, "zhenglou", 34, 13, 6.5, 5.5, 0, yw, z=wall_h + 0.3, plat=0.6, roof="irimoya", roof_h=8.0, roof_color=TILE, col=MRED,
        double_top=True, ridge=MGREEN, shibi=MGREEN)
    return m


def dianmen():
    m = Model("dianmen")
    m.add(0, box("ground", 60, 22, 0.2, (0, 0, 0), GRAVEL), "walls")
    m.add(0, xumizuo("base", 40, 15, 1.4, (0, 0, 0.2)))
    m.add(0, red_wall("wall_w", [(-30, 0), (-20.5, 0)], 6.5, 2.2))
    m.add(0, red_wall("wall_e", [(20.5, 0), (30, 0)], 6.5, 2.2))
    m.add(0, imperial_stair("st_s", 10, 1.4, 3.0, 0, -7.5, 0.2))
    m.add(0, imperial_stair("st_n", 10, 1.4, 3.0, 0, 7.5, 0.2, 180))
    imperial_hall(m, "gate", 36, 12, 7.0, 0, 0, z=1.6, roof="xieshan", double=False, bays=7, roof_h=6.5)
    for i, x in enumerate((-8, 0, 8)):
        for f in (-1, 1):
            m.add(1, box(f"door{i}{f}", 4.0, 0.3, 5.0, (x, f * 5.85, 1.6), "#7A2A22"))
    return m


def wanning_bridge():
    m = Model("wanning-bridge")
    m.add(0, box("water", 30, 12, 0.3, (0, 0, 0), WATERC), "banks")
    for s in (-1, 1):
        m.add(0, box(f"bank{s}", 30, 13, 2.0, (0, s * 13.5, 0), shade(EARTH, 0.05)))
        m.add(0, box(f"quay{s}", 30, 1.2, 2.2, (0, s * 6.6, 0), STONE))
    m.add(1, box("span", 10, 14, 2.6, (0, 0, 0.3), STONE), "bridge")
    for f, x in (("E", 5.05), ("W", -5.05)):
        m.add(1, arch_panel(f"arch{f}", 5.0, 2.6, (x, 0, 0.3), f, DARK, pointed=False, depth=0.4))
    for s in (-1, 1):
        m.add(1, ramp(f"ramp{s}", -5, 5, s * 20, s * 7, 2.0, 2.9, STONE))
    m.add(1, box("deck", 9, 26, 0.12, (0, 0, 2.9), shade(STONE, 0.1)))
    for sx in (-1, 1):
        m.add(1, balustrade(f"rail{sx}", [(sx * 4.6, -9), (sx * 4.6, 9)], 1.0, JADE_D, 2.2, False, 2.9))
    for sx in (-1, 1):
        for sy in (-1, 1):
            m.add(2, join([box(f"bst{sx}{sy}", 1.4, 2.0, 0.7, (sx * 8.5, sy * 7.2, 2.0), "#8E887C"),
                           dome(f"bsh{sx}{sy}", 0.6, (sx * 8.5, sy * 6.8, 2.7), "#8E887C", squash=1.2, segments=8, rings=5)], f"beast{sx}{sy}"), "beasts")
    return m


def jishuitan_harbour():
    m = Model("jishuitan-harbour")
    m.add(0, box("water", 90, 120, 0.25, (-35, 0, 0), WATERC), "quays")
    m.add(0, box("quay", 70, 120, 1.6, (45, 0, 0), STONE))
    m.add(0, box("quay_top", 69, 119, 0.05, (45, 0, 1.6), shade(GRAVEL, -0.05)))
    for y in (-35, 15):
        m.add(0, stair("steps", 10, 1.6, 4.0, 5, (10, y, 0), "W", STONE))
    for i in range(10):
        m.add(0, cylinder(f"bol{i}", 0.4, 0.8, (11.5, -54 + i * 12, 1.6), DARKW, verts=6))
    def hall_y(name, x, y, w, L, h, roof=TILE, wall=CLAY):
        return join([box(name + "_b", w, L, h, (x, y, 1.6), wall), seg_prism(name + "_r", (x, y - L / 2 - 0.6), (x, y + L / 2 + 0.6), 1.6 + h, w + 1.6, w * 0.38, roof)], name)
    m.add(1, hall_y("ware_a", 34, 30, 13, 46, 5.0), "warehouses")
    m.add(1, hall_y("ware_b", 62, 30, 13, 46, 5.5))
    m.add(1, join([box("gran_b", 40, 20, 6.0, (52, -32, 1.6), CLAY), eaved_roof("gran_r", 40, 20, 6.5, (52, -32, 7.6), TILE, over=2.0, curve=0.12)], "granary"))
    # a timber crane and stacked sacks on the quay
    cr = [box("cr_p1", 0.6, 0.6, 9, (15, -4, 1.6), WOOD), box("cr_p2", 0.6, 0.6, 9, (15, 4, 1.6), WOOD), box("cr_b", 0.6, 9, 0.6, (15, 0, 10.6), WOOD),
          box("cr_arm", 12, 0.5, 0.5, (11, 0, 10.0), WOOD), box("cr_rope", 0.15, 0.15, 6, (6, 0, 4.0), DARKW)]
    m.add(1, join(cr, "crane"))
    sacks = [box(f"sk{i}{j}{k}", 1.3, 0.9, 0.6, (20 + i * 1.5, -14 + j * 1.0, 1.6 + k * 0.6), "#D8C9A0") for i in range(4) for j in range(3) for k in range(2)]
    m.add(1, join(sacks, "sacks"))
    for i, (x, y) in enumerate(((3, -42), (3, -16), (3, 10), (3, 36), (-10, -30), (-10, 22), (-24, -6), (-40, 30), (-52, -36))):
        m.add(2, barge(f"barge{i}", 20 if i < 6 else 16, 4.8, (x, y, 0.15), 90 + (0 if i < 6 else 12 * (i % 3 - 1))), "barges")
    trees(m, "willows", [(75, -55), (75, 55), (40, 56), (25, -56)], 3.5, WILLOW)
    return m


def nine_dragon_wall():
    m = Model("nine-dragon-wall")
    m.add(0, xumizuo("base", 26.4, 2.4, 1.0, (0, 0, 0)), "base")
    m.add(0, box("waves", 25.6, 1.5, 0.8, (0, 0, 1.0), "#2F6E8C"))
    m.add(1, box("body", 25.4, 1.3, 3.8, (0, 0, 1.8), "#3E8C86"), "dragons")
    cols = [YELLOW, "#E8E2D0", PURPLE_T, BLUE_T, YELLOW, "#C8742E", BLUE_T, PURPLE_T, "#E8E2D0"]
    for f in (-1, 1):
        for i in range(9):
            cx = -11.2 + i * 2.8
            parts = []
            for k in range(7):
                t = k / 6
                px = cx - 1.0 + 2.0 * t
                pz = 2.3 + 2.6 * t + 0.6 * math.sin(t * math.tau * 1.3 + i)
                parts.append(box(f"dr{f}{i}_{k}", 0.6, 0.18, 0.55, (px, f * 0.72, pz), cols[i], rot_z=0))
            parts.append(dome(f"pearl{f}{i}", 0.22, (cx + 0.9, f * 0.76, 2.6), "#E9D9A0", segments=8, rings=4))
            m.add(1, join(parts, f"dragon{f}{i}"))
    m.add(2, box("cornice", 25.8, 1.8, 0.45, (0, 0, 5.6), MGREEN), "roof")
    m.add(2, hip("roof", 25.6, 1.6, 1.4, (0, 0, 6.05), YELLOW, over=0.5, ridge=YELLOW_D, shibi=YELLOW_D))
    return m


# ---------------------------------------------------------------- Tiananmen

def tiananmen(variant="qing"):
    m = Model("tiananmen" if variant == "qing" else "chengtianmen-1450")
    m.add(0, box("ground", 160, 60, 0.2, (0, 0, 0), GRAVEL), "walls")
    m.add(0, golden_water("river", -80, 80, -19, 2.5, 6.0, 20))
    xs = (0, -13, 13, -26, 26)
    m.add(0, marble_bridges("bridges", xs, -21, 12, 4.5, 1.2))
    if variant == "qing":
        PW, PD, PH = 118.0, 40.0, 13.0
        m.add(0, box("plinth", PW + 1.6, PD + 1.6, 1.0, (0, 8, 0.2), JADE))
        m.add(0, frustum("platform", PW, PD, PW - 1.6, PD - 1.6, PH, (0, 8, 0.2), PRED))
        m.add(0, box("cope", PW - 1.0, PD - 1.0, 0.6, (0, 8, PH - 0.4), YELLOW_D))
        for i, x in enumerate(xs):
            w = 5.2 if i == 0 else 4.4 if i < 3 else 3.8
            h = 8.8 if i == 0 else 7.6 if i < 3 else 6.4
            m.add(0, arch_panel(f"ps{i}", w, h, (x, -12.05, 0.2), "S", DARK, pointed=False, depth=0.6))
            m.add(0, arch_panel(f"pn{i}", w, h, (x, 28.05, 0.2), "N", DARK, pointed=False, depth=0.6))
        m.add(0, balustrade("rail", rect_pts(PW - 2.4, PD - 2.4, 0, 8), 1.1, JADE, 1.0, True, PH + 0.2))
        m.add(0, xumizuo("hall_base", 63, 30, 1.0, (0, 8, PH + 0.2)))
        imperial_hall(m, "tower", 57, 24, 9.5, 0, 8, z=PH + 1.2, roof="xieshan", double=True, bays=9, roof_h=10.0, bk_mult=4, lattice=True, beasts=9)
        lamps = [box(f"lamp{i}", 0.9, 0.9, 1.4, (-24 + i * 6, -4.4, PH + 6.6), "#C8402E") for i in range(9)]
        m.add(1, join(lamps, "lanterns"))
        for s in (-1, 1):
            m.add(0, red_wall(f"icwall{s}", [(s * 59, 8), (s * 80, 8)], 9.0, 3.0))
            m.add(1, huabiao(f"huabiao{s}", 9.6, (s * 30, -27, 0.2)), "monuments")
            m.add(1, huabiao(f"huabiao_n{s}", 9.6, (s * 30, 29, 0.2)))
            m.add(1, stone_lion(f"lion{s}", (s * 9, -14, 0.2)))
    else:
        for s in (-1, 1):
            m.add(0, red_wall(f"icwall{s}", [(s * 80, 8), (s * 24, 8)], 8.0, 3.0))
            m.add(0, box(f"pier{s}", 4, 5, 9.0, (s * 22, 8, 0.2), PRED))
        m.add(1, put(pailou5("gateway", 40, 16), 0, 8, 0, 0.2), "gateway")
        m.add(0, box("pave", 44, 14, 0.15, (0, 8, 0.2), JADE_D))
    tp = [(-78 + i * 3.5, 26 + (i % 2) * 2) for i in range(16)] + [(78 - i * 3.5, 26 + (i % 2) * 2) for i in range(16)] + [(-78 + i * 7, 25) for i in range(0)] + [(78 - i * 7, 25) for i in range(6)] + [(-78 + i * 6, -10) for i in range(4)] + [(78 - i * 6, -10) for i in range(4)]
    trees(m, "trees", tp, 3.0, PINE)
    if variant == "qing":
        for i, x in enumerate(xs):
            posts = [box(f"bp{i}_{k}{sg}", 0.4, 0.4, 1.3, (x + sg * 2.05, -27 + k * 2.0, 1.4), JADE) for k in range(7) for sg in (-1, 1)]
            m.add(1, join(posts, f"bridge_posts{i}"))
    return m


# ---------------------------------------------------------------- the Round City

def tuancheng(variant="qing"):
    m = Model("tuancheng" if variant == "qing" else "tuancheng-yuan")
    if variant == "qing":
        R, H = 40.0, 4.6
        m.add(0, cylinder("terrace", R, H, (0, 0, 0), MBRICK, verts=36), "terrace")
        m.add(0, cylinder("top", R - 0.6, 0.06, (0, 0, H), shade(GRAVEL, -0.05), verts=36))
        mer = []
        for k in range(48):
            a = math.tau * k / 48
            mer.append(box(f"mer{k}", 1.2, 0.6, 1.0, (math.cos(a) * (R - 0.4), math.sin(a) * (R - 0.4), H), MBRICK, rot_z=a + math.pi / 2))
        m.add(0, join(mer, "crenels"))
        for f, x in (("E", R), ("W", -R)):
            m.add(0, arch_panel(f"gate{f}", 3.6, 3.6, (x, 0, 0), f, DARK, pointed=False, depth=0.6))
        m.add(1, put(corner_tower("chengguang", 20.0, YELLOW), 0, 4, 0, H), "halls")
        m.add(1, put(square_pavilion("jarpav", 7, 3.5, 1, BLUE_T), 0, -22, 0, H))
        m.add(1, cylinder("jar", 1.0, 0.8, (0, -22, H + 1.0), "#2F4F3E", verts=12))
        scatter_trees(m, "pines", [(-24, 20, H), (24, 20, H), (-26, -14, H), (26, -14, H)], 4.5, PINE)
    else:
        m.add(0, cylinder("water", 45, 0.25, (0, 0, 0), WATERC, verts=36), "islet")
        m.add(0, blob("islet", 30, 29, 1.4, (0, 0, 0), shade(GRASS, 0.05), 1.3))
        m.add(0, cylinder("terr", 17, 1.2, (0, 0, 1.4), JADE, verts=28))
        z = 2.6
        body = [cylinder("hall", 9.5, 6.5, (0, 0, z), LATTICE, verts=22)]
        for k in range(11):
            a = math.tau * k / 11
            body.append(box(f"col{k}", 0.6, 0.6, 6.5, (math.cos(a) * 10.2, math.sin(a) * 10.2, z), MRED))
        m.add(1, join(body, "yitian"), "hall")
        rf = [cylinder("eave1", 14.5, 2.4, (0, 0, z + 6.5), TILE, verts=22, r_top=9.0), box("dr", 0.1, 0.1, 0.1, (0, 0, z + 8.9), TILE),
              cylinder("drum", 8.0, 2.4, (0, 0, z + 8.4), LATTICE, verts=22), cylinder("eave2", 11.5, 6.0, (0, 0, z + 10.8), TILE, verts=22, r_top=0.6),
              dome("ball", 0.9, (0, 0, z + 16.6), GILT, squash=1.4, segments=10, rings=6)]
        m.add(2, join(rf, "roofs"), "roofs")
        m.add(1, box("stonebridge", 6, 16, 1.4, (8, 37, 0), STONE))
        m.add(1, box("woodbridge", 16, 5, 1.2, (-37, -4, 0), WOOD))
        trees(m, "trees", [(-18, 18), (18, -18), (20, 16)], 3.5, PINE)
    return m


# ---------------------------------------------------------------- Jingshan

def jingshan(variant="qing"):
    m = Model("jingshan" if variant == "qing" else "jingshan-1450")
    m.add(0, box("ground", 420, 260, 0.2, (0, 0, 0), GRASS), "hill")
    hills = [(0, 0, 120, 105, 45.0), (-82, 0, 85, 80, 33.0), (82, 0, 85, 80, 33.0), (-150, 4, 62, 62, 22.0), (150, 4, 62, 62, 22.0)]
    for i, (x, y, rx, ry, h) in enumerate(hills):
        m.add(0, mound(f"peak{i}", rx, ry, h, (x, y, 0.2), shade(GRASS, -0.06 * (i % 2)), 24, 10))

    def zat(px, py):
        return max([h * mound_z(math.hypot((px - x) / rx, (py - y) / ry)) for x, y, rx, ry, h in hills])

    pts = []
    for i in range(70):
        a = i * 2.39996
        rr = 30 + (i * 53) % 150
        px, py = math.cos(a) * rr * 1.25, math.sin(a) * rr * 0.62
        if abs(px) < 200 and abs(py) < 120:
            zz = zat(px, py)
            if variant == "qing" and any(abs(px - x) < 14 and abs(py - y) < 14 for x, y, _, _, _ in hills):
                continue
            pts.append((px, py, max(0.2, zz - 0.6)))
    m.add(2, grove("pines", pts[:30], 4.5, PINE), "trees")
    m.add(2, grove("cypress", pts[30:], 4.0, CYPRESS))
    if variant == "qing":
        for i, (x, y, rx, ry, h) in enumerate(hills):
            m.add(1, box(f"pad{i}", 16 if i == 0 else 12, 16 if i == 0 else 12, 3.0, (x, y, h - 2.6), JADE_D), "pavilions")
        m.add(1, put(square_pavilion("wanchun", 13, 6.0, 3, YELLOW, base=1.2), 0, 0, 0, 45.4))
        for s in (-1, 1):
            m.add(1, put(octagon_pavilion(f"oct{s}", 5.0, 4.5, 3.0, roof=MGREEN, col=MRED, wall=LATTICE), s * 82, 0, 0, 33.4))
            m.add(1, put(round_pavilion(f"rnd{s}", 4.0, 4.0, 2.8, roof=BLUE_T, trim=PURPLE_T), s * 150, 4, 0, 22.4))
        m.add(1, put(imperial_hall_simple("shouhuang", 30, 12, 5.5), 0, 118, 0, 0.2))
    return m


def imperial_hall_simple(name, w, d, h, roof=YELLOW):
    """A small hall as one object: red body, lattice front, hip-and-gable glazed roof."""
    return join([box(name + "_pl", w + 3, d + 3, 0.8, (0, 0, 0), JADE), box(name + "_b", w, d, h, (0, 0, 0.8), PRED),
                 box(name + "_lat", w * 0.8, 0.3, h * 0.7, (0, -d / 2 - 0.1, 0.8), LATTICE), box(name + "_band", w + 0.4, d + 0.4, 0.5, (0, 0, 0.8 + h - 0.5), TEAL),
                 irimoya(name + "_r", w, d, d * 0.62, (0, 0, 0.8 + h), roof, over=d * 0.26, gable=PRED)], name)


# ---------------------------------------------------------------- temples

def temple_gate(m, name, x, y, w=18, d=8, roof=TILE, deg=0.0, sb=1, sr=2):
    imperial_hall(m, name, w, d, 4.8, x, y, deg=deg, roof="xieshan", double=False, roof_color=roof, bays=3, bk=False, plat=0.8,
                  plat_color=STONE, chiwen=False, sb=sb, sr=sr)


def miaoying():
    m = Model("miaoying")
    m.add(0, box("ground", 90, 150, 0.25, (0, 0, 0), GRAVEL), "walls")
    m.add(0, red_wall("wall", rect_pts(86, 146), 4.0, 1.4, PRED, TILE, closed=True))
    m.add(0, red_wall("stupa_wall", [(-42, 2), (42, 2)], 3.6, 1.2, PRED, TILE))
    for sx in (-1, 1):
        m.add(1, put(plain_hall(f"cornerroom{sx}", 7, 7, 4.0, TILE, PRED), sx * 36, 66, 0, 0.25))
    temple_gate(m, "shanmen", 0, -68)
    imperial_hall(m, "tianwang", 22, 10, 5.0, 0, -45, roof="xieshan", double=False, roof_color=TILE, bk=False, plat=0.8, chiwen=False)
    imperial_hall(m, "yizhi", 22, 11, 5.0, 0, -24, roof="xieshan", double=False, roof_color=TILE, bk=False, plat=0.8, chiwen=False)
    imperial_hall(m, "qifo", 26, 13, 6.0, 0, -6, roof="xieshan", double=False, roof_color=TILE, bk=True, plat=1.0)
    for sx in (-1, 1):
        m.add(1, put(plain_hall(f"wing{sx}", 7, 40, 4.0, TILE, CLAY, "y"), sx * 34, -35, 0, 0.25))
    m.add(1, put(tib_stupa("stupa", 50.9, STUPA_W, tiers=2, canopy=BRONZE, podium=31.0), 0, 38, 0, 0.25), "stupa")
    trees(m, "trees", [(-25, -58), (25, -58), (-26, 20), (26, 20)], 3.5, LOCUST)
    return m


def guangji(early=False):
    m = Model("guangji-early" if early else "guangji")
    m.add(0, box("ground", 110, 230, 0.25, (0, 0, 0), GRAVEL if not early else shade(FIELD, 0.05)), "walls")
    if early:
        m.add(0, wall_line("wall", rect_pts(56, 84, 0, 10), 3.0, 1.2, CLAY, TILE, closed=True))
        m.add(1, put(small_gate("gate", 7, 4, 3.6, VERM, TILE), 0, -32, 0, 0.25), "halls")
        tang_hall(m, "hall", 18, 11, 4.5, 0, 22, z=0.25, bays=5, roof="hip", roof_h=4.5, plat=0.8, shibi=None, trim=None, bk=False)
        tang_hall(m, "side", 12, 7, 3.4, 0, -6, z=0.25, bays=3, roof="gable", roof_h=2.8, plat=0.5, shibi=None, trim=None, bk=False)
        trees(m, "trees", [(-18, 0), (18, 0), (-20, 40), (20, 44), (-40, -70), (35, -80), (-38, 90), (40, 95)], 4.0, LOCUST)
        for i, y in enumerate((-95, -70, 75, 100)):
            m.add(0, box(f"plot{i}", 90, 18, 0.12, (0, y, 0.25), shade(GRASS, 0.04 * (i % 2))))
        return m
    m.add(0, red_wall("wall", rect_pts(106, 226), 4.2, 1.4, PRED, TILE, closed=True))
    temple_gate(m, "shanmen", 0, -108, 20, 9)
    for sx in (-1, 1):
        lou(m, f"bt{sx}", 9, 9, 4.5, 3.5, sx * 30, -88, z=0.25, plat=0.8, roof="irimoya", roof_h=4.5, roof_color=TILE, col=MRED)
    imperial_hall(m, "tianwang", 26, 11, 5.5, 0, -62, z=0.25, roof="xieshan", double=False, roof_color=TILE, bk=False, plat=0.8, chiwen=False)
    m.add(0, marble_terrace("dx_t", 40, 26, 1.6, (0, -12, 0.25)))
    imperial_hall(m, "daxiong", 32, 18, 7.0, 0, -12, z=1.85, roof="xieshan", double=False, roof_color=TILE, bays=5)
    imperial_hall(m, "yuantong", 26, 13, 6.0, 0, 38, z=0.25, roof="xieshan", double=False, roof_color=TILE, bk=False, plat=1.0)
    lou(m, "duobao", 30, 13, 5.5, 4.5, 0, 82, z=0.25, plat=1.0, roof="irimoya", roof_h=6.0, roof_color=TILE, col=MRED)
    for sx in (-1, 1):
        m.add(1, put(plain_hall(f"wing{sx}", 8, 140, 4.2, TILE, CLAY, "y"), sx * 44, -10, 0, 0.25))
    m.add(0, put(marble_terrace("jietai", 14, 14, 2.4, (0, 0, 0)), -30, 40, 0, 0.25))
    trees(m, "trees", [(-20, -82), (20, -82), (-22, 12), (22, 12), (-20, 60), (20, 60)], 3.8, PINE)
    return m


def confucius_guozijian():
    m = Model("confucius-guozijian")
    m.add(0, box("ground", 280, 300, 0.25, (0, 0, 0), GRAVEL), "walls")
    # the Temple of Confucius on the east
    TX = 72
    m.add(0, red_wall("t_wall", rect_pts(124, 292, TX, 0), 4.5, 1.5, PRED, YELLOW, closed=True))
    temple_gate(m, "xianshi", TX, -142, 22, 9, MGREEN)
    stl = []
    for r in range(4):
        for i in range(14):
            stl.append(box(f"stele{r}_{i}", 1.4, 0.4, 3.0, (TX - 52 + i * 8, -118 + r * 12, 0.25), "#7C7A74"))
    m.add(1, join(stl, "steles"), "steles")
    m.add(0, xumizuo("dcm_b", 30, 13, 1.2, (TX, -48, 0.25)))
    imperial_hall(m, "dachengmen", 26, 10, 5.5, TX, -48, z=1.45, roof="xieshan", double=False, roof_color=MGREEN, bk=False)
    for i, (px, py) in enumerate(((TX - 34, -22), (TX + 34, -22), (TX - 34, 2), (TX + 34, 2))):
        m.add(1, put(square_pavilion(f"stpav{i}", 8, 4.5, 2, YELLOW), px, py, 0, 0.25))
    m.add(0, marble_terrace("dc_t", 46, 30, 2.0, (TX, 52, 0.25)))
    imperial_hall(m, "dacheng", 36, 20, 8.0, TX, 54, z=2.25, roof="hip", double=True, roof_color=MGREEN, trim=YELLOW, bays=7)
    for sx in (-1, 1):
        m.add(1, put(plain_hall(f"t_wing{sx}", 8, 90, 4.5, MGREEN, PRED, "y"), TX + sx * 52, 30, 0, 0.25))
    imperial_hall(m, "chongsheng", 28, 12, 6.0, TX, 120, z=0.25, roof="xieshan", double=False, roof_color=MGREEN, bk=False, plat=1.0)
    trees(m, "t_cyp", [(TX - 40, -80), (TX + 40, -80), (TX - 20, 20), (TX + 20, 20), (TX - 45, 90), (TX + 45, 90), (TX - 18, -70), (TX + 18, -70)], 4.0, CYPRESS)
    # the Imperial Academy on the west
    GX = -70
    m.add(0, red_wall("g_wall", rect_pts(126, 292, GX, 0), 4.0, 1.4, PRED, TILE, closed=True))
    temple_gate(m, "jixian", GX, -142, 20, 8)
    temple_gate(m, "taixue", GX, -80, 22, 9, MGREEN)
    m.add(0, marble_terrace("yl_t", 40, 24, 1.4, (GX, 10, 0.25)))
    imperial_hall(m, "yilun", 34, 17, 7.0, GX, 10, z=1.65, roof="xieshan", double=False, roof_color=TILE, bays=7)
    for sx in (-1, 1):
        m.add(1, put(plain_hall(f"liutang{sx}", 9, 130, 4.5, TILE, CLAY, "y"), GX + sx * 50, 0, 0, 0.25))
    imperial_hall(m, "jingyi", 22, 10, 5.0, GX, 100, z=0.25, roof="xieshan", double=False, roof_color=TILE, bk=False, plat=0.8)
    trees(m, "g_trees", [(GX - 25, -40), (GX + 25, -40), (GX - 25, 60), (GX + 25, 60), (GX - 30, 125), (GX + 30, 125)], 4.2, LOCUST)
    return m


def yonghegong():
    m = Model("yonghegong")
    m.add(0, box("ground", 120, 440, 0.25, (0, 0, 0), GRAVEL), "walls")
    m.add(1, put(paifang("pf_s", 22, 11, MRED, YELLOW), 0, -205, 0, 0.25), "gates")
    for sx in (-1, 1):
        m.add(1, put(paifang(f"pf{sx}", 18, 10, MRED, YELLOW), sx * 48, -180, 90, 0.25))
    m.add(0, box("avenue", 10, 80, 0.08, (0, -150, 0.25), JADE_D))
    tree_row(m, "row_w", (-10, -188), (-10, -112), 9, 3.2, LOCUST)
    tree_row(m, "row_e", (10, -188), (10, -112), 9, 3.2, LOCUST)
    m.add(0, red_wall("wall", rect_pts(116, 318, 0, 55), 5.0, 1.6, PRED, YELLOW, closed=True))
    temple_gate(m, "zhaotai", 0, -100, 20, 9, YELLOW)
    for sx in (-1, 1):
        lou(m, f"bt{sx}", 9, 9, 4.5, 3.5, sx * 38, -78, z=0.25, plat=0.8, roof="irimoya", roof_h=4.5, roof_color=YELLOW, col=MRED)
        m.add(1, put(octagon_pavilion(f"stele{sx}", 3.6, 3.5, 2.5, roof=YELLOW), sx * 22, -62, 0, 0.25))
    imperial_hall(m, "yonghemen", 32, 14, 6.5, 0, -40, z=0.25, roof="xieshan", double=False, bays=5, plat=1.0)
    imperial_hall(m, "yonghedian", 32, 18, 7.5, 0, 6, z=0.25, roof="xieshan", double=False, bays=7, plat=1.4)
    imperial_hall(m, "yongyou", 28, 14, 6.5, 0, 46, z=0.25, roof="xieshan", double=False, bays=5, plat=1.2)
    top = imperial_hall(m, "falun", 34, 22, 8.0, 0, 96, z=0.25, roof="xieshan", double=False, bays=7, plat=1.6)
    for i, (px, py) in enumerate(((0, 96), (-11, 90), (11, 90), (-11, 102), (11, 102))):
        m.add(2, join([box(f"lt{i}", 3.0, 3.0, 2.2, (px, py, top - 2.5 if i else top - 1.5), PRED),
                       eaved_roof(f"ltr{i}", 3.0, 3.0, 1.6, (px, py, (top - 0.3) if i else (top + 0.7)), YELLOW, over=0.8, curve=0.2),
                       dome(f"ltg{i}", 0.5, (px, py, (top + 1.2) if i else (top + 2.2)), GILT, squash=2.0, segments=8, rings=5)], f"lamatop{i}"))
    # the Wanfu pavilion and its flanking pavilions with flying bridges
    m.add(0, marble_terrace("wf_t", 40, 30, 1.4, (0, 165, 0.25)))
    z = 1.65
    for k, (w, d, h) in enumerate(((30, 22, 8.0), (27, 19, 6.5), (24, 17, 5.5))):
        imperial_hall(m, f"wanfu{k}", w, d, h, 0, 165, z=z, roof="xieshan" if k == 2 else "hip", double=False, bays=5, bk=k == 0,
                      roof_h=(6.0 if k == 2 else 2.0), over=(None if k == 2 else w * 0.12), chiwen=k == 2)
        z += h + (2.6 if k < 2 else 0)
    for sx in (-1, 1):
        lou(m, f"side{sx}", 13, 13, 6.0, 5.0, sx * 31, 165, z=0.25, plat=1.0, roof="irimoya", roof_h=5.5, roof_color=YELLOW, col=MRED)
        m.add(1, box(f"fly{sx}", 9, 3, 1.0, (sx * 19.5, 165, 9.5), MRED))
        m.add(2, seg_prism(f"flyr{sx}", (sx * 15, 165), (sx * 24, 165), 12.5, 4.2, 1.2, YELLOW))
    for sx in (-1, 1):
        m.add(1, put(plain_hall(f"wing{sx}", 7, 150, 4.2, YELLOW, PRED, "y"), sx * 49, 40, 0, 0.25))
    trees(m, "pines", [(-30, -20), (30, -20), (-25, 70), (25, 70), (-30, 130), (30, 130)], 3.8, PINE)
    return m


# ---------------------------------------------------------------- Qionghua island

def qionghua(variant="yuan"):
    m = Model("qionghua" if variant == "yuan" else "qionghua-qing")
    m.add(0, box("lake", 290, 280, 0.2, (0, 0, 0), WATERC), "island")
    m.add(0, blob("island", 136, 128, 1.2, (0, 0, 0.0), shade(GRASS, 0.04), 0.4))
    prof = [(108, 0), (100, 4), (86, 10), (68, 17), (50, 23), (32, 28), (17, 31), (0, 32.5)]
    hill = lathe("hill", prof, (0, 8, 1.2), GRASS, verts=24)
    for v in hill.data.vertices:
        a = math.atan2(v.co.y - 8, v.co.x)
        k = 1 + 0.07 * math.sin(3 * a + 1.1) + 0.04 * math.cos(5 * a)
        v.co.x, v.co.y = v.co.x * k, 8 + (v.co.y - 8) * k
    m.add(0, hill)

    def hz(rr):
        for (r0, z0), (r1, z1) in zip(prof, prof[1:]):
            if r1 <= rr <= r0:
                return 1.2 + z0 + (z1 - z0) * (r0 - rr) / (r0 - r1)
        return 1.2 if rr > prof[0][0] else 33.7

    shore = []
    for k in range(56):
        a = math.tau * k / 56
        f = 0.965 * (1 + 0.12 * math.sin(3 * a + 0.4) + 0.07 * math.cos(5 * a + 0.8))     # follows the island's outline (blob, seed 0.4)
        shore.append((136 * f * math.cos(a), 128 * f * math.sin(a)))
    m.add(1, balustrade("shore", shore, 1.0, JADE_D, 2.6, True, 1.2), "rocks")
    rocks, tpts = [], []
    for i in range(230):
        a = i * 2.39996
        rr = 22 + (i * 41) % 98
        px, py = math.cos(a) * rr, 8 + math.sin(a) * rr
        if abs(px) < 16 and py < 0:
            continue
        (rocks if i % 3 == 0 else tpts).append((px, py, hz(rr)))
    m.add(1, taihu_rocks("rocks", rocks, 3.0), "rocks")
    m.add(2, grove("pines", tpts, 4.5, PINE), "trees")
    # a stair up the south slope
    for i in range(10):
        r0 = 100 - i * 8.5
        m.add(1, box(f"step{i}", 7, 9, hz(r0) + 0.3, (0, 8 - r0 + 4, 0.8), STONE))
        m.add(1, box(f"stepr{i}", 0.4, 9, hz(r0) + 1.2, (3.6, 8 - r0 + 4, 0.8), JADE_D))
        m.add(1, box(f"stepl{i}", 0.4, 9, hz(r0) + 1.2, (-3.6, 8 - r0 + 4, 0.8), JADE_D))
    # the south gate hall on the shore and the bridge stub
    imperial_hall(m, "shore_gate", 22, 9, 5.0, 0, -112, z=1.2, roof="xieshan", double=False, roof_color=MGREEN if variant == "yuan" else YELLOW, bk=False, plat=0.8, chiwen=False)
    m.add(1, box("bridge", 7, 18, 1.4, (12, -133, 0), JADE))
    if variant == "yuan":
        top = 33.7
        m.add(1, box("summit", 50, 32, 2.2, (0, 8, top - 1.6), JADE_D))
        imperial_hall(m, "guanghan", 38, 20, 7.0, 0, 8, z=top + 0.6, roof="xieshan", double=True, roof_color=MGREEN, ridge=YELLOW_D, bays=7)
        for sx in (-1, 1):
            r = 44
            m.add(1, box(f"pad{sx}", 12, 12, hz(r) + 0.5, (sx * r * 0.75, 8 - r * 0.6, 0.8), JADE_D))
            m.add(1, put(square_pavilion(f"pav{sx}", 7, 3.5, 1, MGREEN), sx * r * 0.75, 8 - r * 0.6, 0, hz(r) + 1.3))
    else:
        top = 33.7
        m.add(1, box("summit", 34, 34, 2.2, (0, 8, top - 1.6), STONE))
        m.add(2, put(tib_stupa("dagoba", 35.9, STUPA_W, tiers=1, eye=True, canopy=GILT, podium=20.0), 0, 8, 0, top + 0.6), "dagoba")
        for k, (yy, w, d, h) in enumerate(((-60, 26, 12, 5.5), (-38, 18, 10, 4.5), (-22, 14, 8, 4.0))):
            rr = abs(yy - 8)
            zb = hz(rr + d / 2)
            m.add(1, box(f"tpad{k}", w + 6, d + 6, zb + 0.4, (0, yy, 0.8), STONE))
            imperial_hall(m, f"yongan{k}", w, d, h, 0, yy, z=zb + 1.2, roof="xieshan", double=False, roof_color=YELLOW, bk=False, plat=0.6, chiwen=k == 0)
    return m


# ---------------------------------------------------------------- the Forbidden City

def palace_walls(m, name, xw, ys, yn, h, color=PRED, top=TILE, cren_gap=3.6, gates=()):
    """A rectangular palace wall x in [-xw, xw], y in [ys, yn], with a walkway, crenels on the outer edge and gaps for gate blocks."""
    t = 9.0
    sides = [((-xw, ys), (xw, ys)), ((xw, ys), (xw, yn)), ((xw, yn), (-xw, yn)), ((-xw, yn), (-xw, ys))]
    parts = []
    for k, ((ax, ay), (bx, by)) in enumerate(sides):
        L = math.hypot(bx - ax, by - ay)
        a = math.atan2(by - ay, bx - ax)
        cuts = sorted((g[1] - g[2] / 2, g[1] + g[2] / 2) for g in gates if g[0] == k)
        t0 = 0.0
        for j, (c0, c1) in enumerate(cuts + [(L, L)]):
            if c0 - t0 > 1.0:
                u0, u1 = t0, c0
                cx, cy = ax + math.cos(a) * (u0 + u1) / 2, ay + math.sin(a) * (u0 + u1) / 2
                seg = u1 - u0
                parts.append(box(f"{name}_s{k}_{j}", seg + (t if j == 0 else 0), t, h, (cx, cy, 0), color, rot_z=a))
                parts.append(box(f"{name}_w{k}_{j}", seg, t - 1.0, 0.1, (cx, cy, h), top, rot_z=a))
                nx, ny = math.sin(a), -math.cos(a)            # outward normal for a counter-clockwise ring
                n = max(1, int(seg / (1.4 + cren_gap)))
                for i in range(n):
                    u = u0 + (i + 0.5) * seg / n
                    px, py = ax + math.cos(a) * u + nx * (t / 2 - 0.4), ay + math.sin(a) * u + ny * (t / 2 - 0.4)
                    parts.append(box(f"{name}_m{k}_{j}_{i}", 1.4, 0.8, 1.3, (px, py, h), color, rot_z=a))
            t0 = c1
    m.add(0, join(parts, name), "walls")


def wumen(m, x, y):
    """The Meridian Gate: a U-shaped red platform opening south, the nine-bay hall in the middle and four square
    pavilions on the wings joined by galleries (the 'Five Phoenix Towers')."""
    H = 12.0
    blk = [box("wm_c", 126, 32, H, (x, y, 0), PRED), box("wm_cp", 127, 33, 1.0, (x, y, 0), JADE_D), box("wm_cc", 127, 33, 0.6, (x, y, H - 0.6), YELLOW_D)]
    for s in (-1, 1):
        blk += [box(f"wm_w{s}", 24, 62, H, (x + s * 51, y - 47, 0), PRED), box(f"wm_wp{s}", 25, 63, 1.0, (x + s * 51, y - 47, 0), JADE_D),
                box(f"wm_wc{s}", 25, 63, 0.6, (x + s * 51, y - 47, H - 0.6), YELLOW_D)]
    for i, (px, w, h) in enumerate(((0, 6.0, 9.0), (-14, 5.0, 8.0), (14, 5.0, 8.0))):
        blk.append(arch_panel(f"wm_ps{i}", w, h, (x + px, y - 16.05, 0), "S", DARK, pointed=False, depth=0.6))
        blk.append(arch_panel(f"wm_pn{i}", w, h, (x + px, y + 16.05, 0), "N", DARK, pointed=False, depth=0.6))
    m.add(0, join(blk, "wumen_platform"), "walls")
    m.add(0, balustrade("wm_rail", rect_pts(124, 30, x, y), 1.0, PRED, 4.0, True, H))
    imperial_hall(m, "wm_hall", 60, 25, 9.0, x, y + 1, z=H, roof="hip", double=True, bays=9, roof_h=10.0)
    for s in (-1, 1):
        m.add(1, put(gallery(f"wm_gal{s}", [(0, -8), (0, -66)], w=8, h=4.2, col=MRED, roof=YELLOW, wall=LATTICE), x + s * 51, y, 0, H), "halls")
        for k, yy in enumerate((y - 6, y - 72)):
            imperial_hall(m, f"wm_pav{s}{k}", 15, 15, 5.5, x + s * 51, yy, z=H, roof="pyramid", double=True, bays=3, bk=False)


def forbidden_city(variant="qing"):
    m = Model("forbidden-city" if variant == "qing" else "forbidden-city-1450")
    XW, YS, YN = 372.0, -400.0, 476.0
    m.add(0, box("court", 2 * XW, YN - YS, 0.3, (0, (YS + YN) / 2, 0), shade(GRAVEL, -0.04)), "walls")
    m.add(0, box("wm_square", 78, 78, 0.3, (0, YS - 39, 0), shade(GRAVEL, -0.04)))
    palace_walls(m, "walls", XW, YS, YN, 10.0, gates=[(0, XW, 130), (2, XW, 50), (1, 70, 30), (3, YN - YS - 70, 30)])
    wumen(m, 0, YS)
    gate_tower_on_wall(m, "shenwu", 40, 14, 10.0, 0, YN, roof=YELLOW)
    for s in (-1, 1):
        gate_tower_on_wall(m, f"donghua{s}", 26, 12, 10.0, s * XW, YS + 70, deg=90, roof=YELLOW)
    for sx in (-1, 1):
        for yy in (YS, YN):
            m.add(2, put(corner_tower(f"jiaolou{sx}{int(yy)}", 13.0), sx * (XW - 4), yy + (4 if yy < 0 else -4), 0, 10.0), "roofs")
    # the Golden Water stream and the Gate of Supreme Harmony
    m.add(0, golden_water("jinshui", -60, 60, -320, 12, 7.0, 10))
    m.add(0, marble_bridges("jsbridges", (0, -12, 12, -24, 24), -332, 14, 5.0, 1.2))
    m.add(0, xumizuo("thm_base", 66, 30, 3.0, (0, -290, 0.3)))
    m.add(0, imperial_stair("thm_st", 18, 3.0, 6.0, 0, -305, 0.3))
    imperial_hall(m, "taihemen", 52, 20, 8.5, 0, -290, z=3.3, roof="xieshan", double=True, bays=9)
    # galleries round the great court
    for sx in (-1, 1):
        m.add(1, put(plain_hall(f"court_gal{sx}", 9, 230, 5.0, YELLOW, PRED, "y"), sx * 118, -180, 0, 0.3), "halls")
        imperial_hall(m, f"tiren{sx}", 26, 14, 6.0, sx * 112, -180, z=0.3, roof="xieshan", double=True, bays=5, bk=False, plat=1.2)
    m.add(1, put(plain_hall("court_gal_s1", 74, 9, 5.0, YELLOW, PRED), -82, -280, 0, 0.3))
    m.add(1, put(plain_hall("court_gal_s2", 74, 9, 5.0, YELLOW, PRED), 82, -280, 0, 0.3))
    # the three-tiered terrace and the three great halls
    big = variant != "qing"
    for k in range(3):
        m.add(0, marble_terrace(f"sandai{k}", 136 - 12 * k, 232 - 12 * k, 2.7, (0, -60, 0.3 + 2.7 * k), JADE, 5.0))
    for k in range(3):
        m.add(0, imperial_stair(f"sd_st{k}", 16, 2.7, 6.0, 0, -176 + 6 * k, 0.3 + 2.7 * k))
    zt = 0.3 + 8.1
    imperial_hall(m, "taihedian", 70 if big else 64, 40 if big else 37, 12.5, 0, -128, z=zt, roof="hip", double=True, bays=11, roof_h=12.0, beasts=10)
    imperial_hall(m, "zhonghedian", 24, 24, 7.0, 0, -70, z=zt, roof="pyramid", double=False, bays=5, roof_h=10.0)
    imperial_hall(m, "baohedian", 49, 24, 9.0, 0, -22, z=zt, roof="xieshan", double=True, bays=9)
    for sx in (-1, 1):
        m.add(1, put(xumizuo(f"bronze_b{sx}", 3, 3, 1.0, (0, 0, 0), JADE), sx * 30, -150, 0, zt))
        m.add(1, cylinder(f"vat{sx}", 1.2, 1.4, (sx * 30, -150, zt + 1.0), BRONZE, verts=10))
    # the inner court
    imperial_hall(m, "qianqingmen", 32, 13, 6.5, 0, 82, z=1.8, roof="xieshan", double=False, bays=5, plat=0.0)
    m.add(0, xumizuo("qqm_b", 38, 18, 1.5, (0, 82, 0.3)))
    m.add(0, red_wall("inner_wall", [(-16.5, 82), (-62, 82), (-62, 300), (62, 300), (62, 82), (16.5, 82)], 7.0, 2.0))
    m.add(0, marble_terrace("inner_t", 74, 190, 2.4, (0, 196, 0.3), JADE, 6.0))
    zi = 2.7
    imperial_hall(m, "qianqing", 50, 24, 10.0, 0, 144, z=zi, roof="hip", double=True, bays=9)
    imperial_hall(m, "jiaotai", 15, 15, 5.5, 0, 196, z=zi, roof="pyramid", double=False, bays=3, bk=False, roof_h=7.0)
    imperial_hall(m, "kunning", 44, 20, 9.0, 0, 246, z=zi, roof="hip", double=True, bays=9)
    # the six eastern and six western palaces, and the outer ranges, as blocks
    for sx in (-1, 1):
        for i in range(2):
            for j in range(3):
                cx, cy = sx * (100 + i * 52), 120 + j * 62
                m.add(0, put(red_wall(f"pal_w{sx}{i}{j}", rect_pts(46, 56), 5.5, 1.2, PRED, YELLOW, closed=True), cx, cy, 0, 0.3))
                m.add(1, put(block_hall(f"pal_f{sx}{i}{j}", 26, 11, 5.0), cx, cy - 10, 0, 0.3))
                m.add(1, put(block_hall(f"pal_r{sx}{i}{j}", 26, 10, 4.5), cx, cy + 14, 0, 0.3))
        for i in range(5):
            for j in range(4):
                cx, cy = sx * (238 + i * 26), 40 + j * 90
                if i == 4 and j == 0:
                    continue
                m.add(1, put(block_hall(f"east_r{sx}{i}{j}", 18, 40 if j % 2 else 30, 5.0, YELLOW if (i + j) % 3 else TILE), cx, cy, 0, 0.3))
        # Wenhua (east) and Wuying (west) halls with their courts
        m.add(0, put(red_wall(f"wh_w{sx}", rect_pts(110, 150), 5.5, 1.4, PRED, YELLOW, closed=True), sx * 230, -230, 0, 0.3))
        imperial_hall(m, f"wenhua{sx}", 40, 18, 7.0, sx * 230, -230, z=0.3, roof="xieshan", double=False, bays=7, plat=1.4)
        m.add(1, put(block_hall(f"wh_back{sx}", 30, 12, 5.5), sx * 230, -180, 0, 0.3))
        for j in range(3):
            m.add(1, put(block_hall(f"south_r{sx}{j}", 60, 14, 5.0, TILE), sx * 260, -350 + j * 32 if j < 2 else -120, 0, 0.3))
    # the imperial garden at the north end
    m.add(0, red_wall("garden_wall", rect_pts(140, 120, 0, 385), 5.0, 1.4, PRED, YELLOW, closed=True))
    imperial_hall(m, "qinan", 30, 16, 6.0, 0, 390, z=0.3, roof="hip", double=False, bays=5, plat=1.2)
    for sx in (-1, 1):
        m.add(1, put(square_pavilion(f"gpav{sx}", 10, 4.5, 2, YELLOW), sx * 45, 360, 0, 0.3))
    trees(m, "garden_trees", [(-55, 410), (55, 410), (-30, 345), (30, 345), (-60, 350), (60, 350), (-20, 425), (20, 425)], 4.0, CYPRESS)
    return m


# ---------------------------------------------------------------- Kublai's palace

def yuan_palace():
    m = Model("yuan-palace")
    XW, YS, YN = 362.0, -430.0, 470.0
    m.add(0, box("court", 2 * XW, YN - YS, 0.3, (0, (YS + YN) / 2, 0), shade(GRAVEL, -0.02)), "walls")
    m.add(0, box("front", 70, 47, 0.3, (0, YS - 23.5, 0), shade(GRAVEL, -0.02)))
    YW = "#C9AE96"
    palace_walls(m, "walls", XW, YS, YN, 10.0, color=YW, gates=[(0, XW, 90), (2, XW, 40), (1, 230, 26), (3, YN - YS - 230, 26)])
    # the Chongtian gate: a twelve-bay gate on a platform with two flanking towers on short wings
    blk = [box("ct_c", 90, 24, 10.0, (0, YS, 0), YW)]
    for s in (-1, 1):
        blk.append(box(f"ct_w{s}", 18, 46, 10.0, (s * 36, YS - 24, 0), YW))
    for i, px in enumerate((0, -13, 13)):
        blk.append(arch_panel(f"ct_p{i}", 5.0, 7.5, (px, YS - 12.05, 0), "S", DARK, pointed=False, depth=0.6))
    m.add(0, join(blk, "chongtian"))
    imperial_hall(m, "ct_hall", 56, 18, 7.5, 0, YS, z=10.0, roof="hip", double=False, roof_color=MGREEN, ridge=YELLOW_D, bays=11, bk=False)
    for s in (-1, 1):
        imperial_hall(m, f"ct_que{s}", 14, 14, 5.0, s * 36, YS - 38, z=10.0, roof="pyramid", double=True, roof_color=YELLOW, bk=False, bays=3)
    gate_tower_on_wall(m, "houzai", 34, 12, 10.0, 0, YN, roof=MGREEN, double=False, roof_kind="xieshan")
    for s in (-1, 1):
        gate_tower_on_wall(m, f"donghua{s}", 22, 10, 10.0, s * XW, YS + 230, deg=90, roof=MGREEN, double=False, roof_kind="xieshan")
    for sx in (-1, 1):
        for yy in (YS, YN):
            m.add(2, put(corner_tower(f"jiao{sx}{int(yy)}", 12.0, MGREEN), sx * (XW - 4), yy + (4 if yy < 0 else -4), 0, 10.0), "roofs")
    # the Daming court
    m.add(1, gallery("dm_cloister", rect_pts(220, 270, 0, -250), w=7, h=4.5, col=VERM, roof=MGREEN, wall=WHITE, closed=True, post_every=6.0), "halls")
    for sx in (-1, 1):
        for yy in (-385, -115):
            imperial_hall(m, f"dm_corner{sx}{yy}", 14, 14, 5.0, sx * 110, yy, z=0.3, roof="pyramid", double=False, roof_color=YELLOW, bk=False, bays=3)
    imperial_hall(m, "damingmen", 40, 14, 7.0, 0, -385, z=0.3, roof="xieshan", double=True, roof_color=YELLOW, trim=MGREEN, bays=7, plat=1.2)
    m.add(0, marble_terrace("dm_t1", 96, 160, 2.2, (0, -235, 0.3), JADE, 5.0))
    m.add(0, marble_terrace("dm_t2", 84, 70, 2.0, (0, -268, 2.5), JADE, 5.0))
    m.add(0, imperial_stair("dm_st", 16, 2.2, 6.0, 0, -315, 0.3))
    m.add(0, box("steppe_grass", 30, 18, 0.15, (0, -330, 0.3), "#8FA35E"))
    imperial_hall(m, "daming", 63, 38, 12.0, 0, -268, z=4.5, roof="hip", double=True, roof_color=YELLOW, trim=MGREEN, bays=11, roof_h=11.0)
    imperial_hall(m, "dm_corridor", 14, 44, 6.5, 0, -227, z=2.5, roof="xieshan", double=False, roof_color=YELLOW, bk=False, bays=3, deg=90, roof_h=5.0)
    imperial_hall(m, "dm_rear", 45, 22, 9.0, 0, -190, z=2.5, roof="xieshan", double=True, roof_color=YELLOW, trim=MGREEN, bays=9)
    for sx in (-1, 1):
        imperial_hall(m, f"dm_side{sx}", 18, 12, 6.0, sx * 64, -260, z=0.3, roof="xieshan", double=False, roof_color=MGREEN, bk=False, plat=1.0)
    # the Yanchun court behind
    m.add(1, gallery("yc_cloister", rect_pts(190, 220, 0, 45), w=7, h=4.5, col=VERM, roof=MGREEN, wall=WHITE, closed=True, post_every=6.0))
    imperial_hall(m, "yanchunmen", 34, 12, 6.0, 0, -65, z=0.3, roof="xieshan", double=False, roof_color=MGREEN, bays=7, plat=1.0)
    m.add(0, marble_terrace("yc_t", 70, 120, 2.0, (0, 50, 0.3), JADE, 5.0))
    lou(m, "yanchun", 50, 28, 8.0, 7.0, 0, 20, z=2.3, plat=0.6, roof="irimoya", roof_h=10.0, roof_color=MGREEN, col=MRED, wall=LATTICE, double_top=True, ridge=YELLOW_D, bays=9)
    imperial_hall(m, "yc_corridor", 12, 30, 6.0, 0, 52, z=2.3, roof="xieshan", double=False, roof_color=MGREEN, bk=False, bays=3, deg=90, roof_h=4.5)
    imperial_hall(m, "yc_rear", 40, 20, 8.0, 0, 82, z=2.3, roof="xieshan", double=True, roof_color=MGREEN, bays=7)
    # side courts, kitchens, stores; felt tents and horse lines in the north-west yard
    for sx in (-1, 1):
        for j in range(2, 5):
            m.add(1, put(block_hall(f"side{sx}{j}", 40, 14, 5.0, MGREEN if j % 2 else TILE, WHITE), sx * 230, -330 + j * 70 if j != 3 else -120, 0, 0.3))
        for j in range(4):
            m.add(1, put(block_hall(f"rear{sx}{j}", 30, 12, 4.5, TILE, WHITE), sx * 180, 220 + j * 50, 0, 0.3))
    for i, (gx, gy, gr) in enumerate(((-300, 280, 6.0), (-278, 300, 5.0), (-300, 320, 5.0), (-262, 268, 4.5), (-320, 250, 4.5), (-250, 330, 5.5))):
        m.add(1, ger(f"ger{i}", gr, (gx, gy, 0.3)))
    m.add(1, cylinder("banner_pole", 0.3, 14, (-285, 300, 0.3), DARKW, verts=6))
    m.add(1, box("banner", 0.2, 3.0, 2.0, (-285, 301.6, 11.5), "#E8E2D0"))
    m.add(0, box("park", 2 * XW - 12, 300, 0.12, (0, 310, 0.3), shade(GRASS, 0.04)))
    m.add(0, blob("pond", 40, 26, 0.2, (150, 330, 0.4), WATERC, 0.8))
    tp = [(-80, 300), (80, 300), (-60, 380), (60, 380), (0, 420), (-120, 400), (120, 400), (-150, 200), (150, 200)]
    tp += [(-330 + i * 37, 445 - (i % 3) * 22) for i in range(18)] + [(200 + (i % 4) * 30, 250 + (i // 4) * 30) for i in range(12)]
    tp += [(-200 + (i % 3) * 26, 380 + (i // 3) * 22) for i in range(6)]
    trees(m, "trees", tp, 5.0, PINE)
    for sx in (-1, 1):
        for i in range(3):
            for j in range(4):
                m.add(1, put(block_hall(f"office{sx}{i}{j}", 34, 12, 4.5, TILE if (i + j) % 2 else MGREEN, WHITE), sx * (160 + i * 60), -400 + j * 45, 0, 0.3))
        m.add(0, put(red_wall(f"court_w{sx}", rect_pts(150, 190), 4.0, 1.2, YW, MGREEN, closed=True), sx * 220, -310, 0, 0.3))
    return m


BUILDERS = {
    "khanbaliq/yuan-palace": yuan_palace,
    "khanbaliq/qionghua": lambda: qionghua("yuan"),
    "khanbaliq/qionghua-qing": lambda: qionghua("qing"),
    "khanbaliq/tuancheng": lambda: tuancheng("qing"),
    "khanbaliq/tuancheng-yuan": lambda: tuancheng("yuan"),
    "khanbaliq/forbidden-city": lambda: forbidden_city("qing"),
    "khanbaliq/forbidden-city-1450": lambda: forbidden_city("1450"),
    "khanbaliq/tiananmen": lambda: tiananmen("qing"),
    "khanbaliq/chengtianmen-1450": lambda: tiananmen("1450"),
    "khanbaliq/jingshan": lambda: jingshan("qing"),
    "khanbaliq/jingshan-1450": lambda: jingshan("1450"),
    "khanbaliq/drum-tower": drum_tower,
    "khanbaliq/bell-tower": lambda: bell_tower("qing"),
    "khanbaliq/bell-tower-1450": lambda: bell_tower("1450"),
    "khanbaliq/yuan-towers": yuan_towers,
    "khanbaliq/jishuitan-harbour": jishuitan_harbour,
    "khanbaliq/wanning-bridge": wanning_bridge,
    "khanbaliq/confucius-guozijian": confucius_guozijian,
    "khanbaliq/yonghegong": yonghegong,
    "khanbaliq/nine-dragon-wall": nine_dragon_wall,
    "khanbaliq/dianmen": dianmen,
    "khanbaliq/ming-gate": ming_gate,
    "khanbaliq/guangji": lambda: guangji(False),
    "khanbaliq/guangji-early": lambda: guangji(True),
    "khanbaliq/miaoying": miaoying,
}
