"""Chang'an / Xi'an landmark miniatures.

The hall, gate, corridor and roof helpers are copied from the Nara module (nara.py, itself from kyoto.py);
the rammed-earth terraces, brick pagodas, Tang gate platforms and the Ming towers are Chang'an's own."""
import math
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


def gg_storey(name, w, h, z, bays, color=PBRICK, door_w=None):
    """A storey of the Greater Wild Goose Pagoda: battered brick walls cut into bays by shallow pilasters, an architrave, an arched door on each face."""
    parts = [frustum(name + "_w", w, w, w * 0.985, w * 0.985, h, (0, 0, z), color)]
    pw, pd = max(0.35, w * 0.02), 0.32
    for i in range(bays + 1):
        t = -w / 2 + w * i / bays
        t = max(-w / 2 + pw / 2, min(w / 2 - pw / 2, t))
        pc = shade(color, 0.07)
        parts.append(box(f"{name}_ps{i}", pw, pd, h * 0.86, (t, -w / 2 + 0.05, z), pc))
        parts.append(box(f"{name}_pn{i}", pw, pd, h * 0.86, (t, w / 2 - 0.05, z), pc))
        parts.append(box(f"{name}_pw{i}", pd, pw, h * 0.86, (-w / 2 + 0.05, t, z), pc))
        parts.append(box(f"{name}_pe{i}", pd, pw, h * 0.86, (w / 2 - 0.05, t, z), pc))
    parts.append(box(name + "_lan", w + 0.5, w + 0.5, h * 0.07, (0, 0, z + h * 0.86), shade(color, 0.05)))
    parts.append(box(name + "_pu", w + 0.2, w + 0.2, h * 0.07, (0, 0, z + h * 0.93), shade(color, -0.05)))
    dw = door_w or w / bays * 0.75
    dh = min(h * 0.7, dw * 2.0)
    for face, (fx, fy) in (("S", (0, -w / 2)), ("N", (0, w / 2)), ("E", (w / 2, 0)), ("W", (-w / 2, 0))):
        parts.append(arch_panel(f"{name}_a{face}", dw, dh, (fx, fy, z + 0.05), face, DARK, pointed=False, depth=0.7))
    return join(parts, name)


def greater_goose_tower(name, storeys=7, color=PBRICK, early=False):
    """The pagoda itself on its brick platform. Returns (platform, tower)."""
    if early:
        widths = [26.0, 23.5, 21.0, 18.5, 16.0]
        heights = [10.0, 7.6, 7.0, 6.5, 6.0]
        bays = [9, 7, 7, 5, 5]
    else:
        widths = [25.0, 23.2, 21.5, 19.8, 18.1, 16.4, 14.8]
        heights = [8.6, 6.4, 6.1, 5.8, 5.5, 5.3, 5.1]
        bays = [9, 9, 7, 7, 5, 5, 5]
    plat_h = 4.2
    plat = [terrace(name + "_plat", 44, 46, plat_h, (0, 0, 0), STONE, shade(color, -0.06), batter=0.03, rail=False)]
    plat.append(stair(name + "_sts", 10, plat_h, 9, 9, (0, -23 - 4.5, 0), "S", shade(color, -0.04)))
    plat.append(stair(name + "_stn", 10, plat_h, 9, 9, (0, 23 + 4.5, 0), "N", shade(color, -0.04)))
    parts = []
    z = plat_h
    for i in range(storeys):
        w, h = widths[i], heights[i]
        parts.append(gg_storey(f"{name}_s{i}", w, h, z, bays[i], color, door_w=2.6 if i else 3.2))
        z += h
        w_next = widths[i + 1] if i + 1 < storeys else w * 0.82
        c, z = corbel(f"{name}_c{i}", w, w_next, z, 4, 4, 0.16, 0.2, color, saw=True)
        parts.append(c)
    wt = widths[-1] * 0.82
    # the steles of the imperial prefaces in niches either side of the south door
    for s in (-1, 1):
        parts.append(box(f"{name}_niche{s}", 2.4, 0.4, 4.2, (s * 6.2, -widths[0] / 2 - 0.1, plat_h + 0.6), DARK))
        parts.append(box(f"{name}_stele{s}", 1.5, 0.3, 3.4, (s * 6.2, -widths[0] / 2 - 0.25, plat_h + 0.8), "#9A968E"))
    if early:
        # an Indian-looking crown: a drum, a hemispherical dome, a railing box and a mast of discs
        parts.append(frustum(name + "_cap", wt, wt, wt * 0.7, wt * 0.7, 1.4, (0, 0, z), color))
        parts.append(cylinder(name + "_drum", wt * 0.32, 1.6, (0, 0, z + 1.4), color, verts=20))
        parts.append(dome(name + "_dome", wt * 0.32, (0, 0, z + 3.0), shade(color, 0.08), squash=0.9, segments=20, rings=10))
        parts.append(box(name + "_harm", 1.8, 1.8, 1.0, (0, 0, z + 3.0 + wt * 0.29), color))
        for k in range(5):
            parts.append(cylinder(f"{name}_disc{k}", 1.6 - k * 0.22, 0.25, (0, 0, z + 4.2 + wt * 0.29 + k * 0.75), BRONZE, verts=12))
        parts.append(cylinder(name + "_mast", 0.12, 4.5, (0, 0, z + 4.0 + wt * 0.29), BRONZE, verts=6))
    else:
        parts.append(frustum(name + "_cap", wt, wt, wt * 0.45, wt * 0.45, 2.2, (0, 0, z), color))
        parts.append(frustum(name + "_cap2", wt * 0.45, wt * 0.45, wt * 0.18, wt * 0.18, 1.6, (0, 0, z + 2.2), shade(color, 0.05)))
        parts.append(dome(name + "_bao", 1.1, (0, 0, z + 3.7), shade(color, 0.1), squash=1.5, segments=14, rings=8))
        parts.append(cylinder(name + "_spike", 0.18, 2.4, (0, 0, z + 5.2), BRONZE, verts=6))
    return join(plat, name + "_platform"), join(parts, name + "_tower")


def greater_goose(variant="750"):
    m = Model({"750": "greater-goose", "652": "greater-goose-652", "1400": "greater-goose-1400"}[variant])
    W, D = 200, 240
    ming = variant == "1400"
    col = shade(PBRICK, -0.08) if ming else PBRICK
    m.add(0, box("ground", W, D, 0.3, (0, 0, 0), FIELD if ming else GRAVEL), "grounds")
    plat, tower = greater_goose_tower("pagoda", 5 if variant == "652" else 7, col, early=variant == "652")
    m.add(0, move(plat, 0, 10, 0.3), "platform")
    m.add(1, move(tower, 0, 10, 0.3), "pagoda")
    if not ming:
        m.add(0, box("court", 168, 200, 0.06, (0, 0, 0.3), shade(GRAVEL, -0.05)))
        m.add(0, gallery("kairo", rect_pts(170, 206, 0, 0), w=6, h=3.6, closed=True, wall=WHITE), "court")
        body, roof = gate_parts("gate", 22, 9, 6.0, 4.5, roof_h=5.5, bays=5, top="hip", trim=GLAZE, shibi=CHIWEI)
        m.add(1, move(body, 0, -103, 0.3), "court")
        m.add(2, move(roof, 0, -103, 0.3), "roofs")
        tang_hall(m, "fodian", 34, 18, 7.5, 0, 72, z=0.3, bays=7, plat=1.6, roof_h=8.0)
        for s in (-1, 1):
            tang_hall(m, f"side{s}", 30, 11, 5.0, s * 66, -30, deg=-90 * s, z=0.3, bays=7, plat=0.8, roof="irimoya", roof_h=5.0)
            lou(m, f"lou{s}", 10, 9, 4.2, 3.6, s * 52, -76, z=0.3, plat=0.8, roof="hip", trim=GLAZE)
        m.add(1, box("path", 8, 60, 0.08, (0, -70, 0.36), STONE))
        trees(m, "pines", [(-60, -92), (60, -92), (-78, 30), (78, 30), (-75, 88), (75, 88), (-30, 90), (30, 90)], 4.2)
        beds = [box(f"peony{i}", 6, 3, 0.7, (x, y, 0.3), ("#C8607A", "#E8D8D0", "#A83A4A")[i % 3]) for i, (x, y) in enumerate(((-36, 50), (36, 50), (-36, 40), (36, 40)))]
        m.add(2, join(beds, "peonies"))
        trees(m, "outside", [(-92, -110), (92, -110), (-92, 110), (92, 110)], 4.0, LOCUST)
    else:
        m.add(0, walled("wall", 120, 150, 3.0, 1.4, (("S", 0, 10),), CLAY, TILE, 0, 5), "court")
        m.add(1, move(small_gate("gate", 9, 5, 4.4, MRED, TILE, "irimoya"), 0, -70, 0.3), "court")
        tang_hall(m, "hall", 22, 12, 5.5, 0, 58, z=0.3, bays=5, plat=1.0, roof="irimoya", roof_h=5.5, shibi=None, trim=None, col=MRED, bk=False)
        strips = []
        for i in range(10):
            x = -95 + i * 19
            if abs(x) < 70:
                for y0, y1 in ((-118, -80), (88, 118)):
                    strips.append(box(f"f{i}{y0}", 17, y1 - y0, 0.12, (x + 9, (y0 + y1) / 2, 0.3), shade(FIELD, 0.06 * (i % 3 - 1))))
            else:
                strips.append(box(f"f{i}", 17, 236, 0.12, (x + 9, 0, 0.3), shade(FIELD, 0.06 * (i % 3 - 1))))
        m.add(0, join(strips, "fields"))
        m.add(1, yard_houses("farm", 80, -95, 22, 18, 3.6, CLAY, TILE))
        trees(m, "trees", [(-70, -60), (-75, 70), (70, 75), (-40, 90), (45, -60)], 4.0, LOCUST)
    return m


def lesser_goose():
    m = Model("lesser-goose")
    W = 110
    m.add(0, box("ground", W, W, 0.3, (0, 0, 0), GRAVEL), "grounds")
    m.add(0, walled("wall", W - 4, W - 4, 3.2, 1.4, (("S", 0, 9), ("N", 0, 6)), CLAY, TILE), "court")
    m.add(0, terrace("plat", 20, 20, 2.0, (0, 0, 0.3), STONE, shade(PBRICK, -0.05), batter=0.03))
    m.add(0, stair("st", 5, 2.0, 4, 6, (0, -12, 0.3), "S", shade(PBRICK, -0.05)))
    m.add(0, stair("stn", 5, 2.0, 4, 6, (0, 12, 0.3), "N", shade(PBRICK, -0.05)))
    parts = []
    z = 2.3
    w1, h1 = 11.4, 9.0
    parts.append(frustum("s0", w1, w1, w1 * 0.99, w1 * 0.99, h1, (0, 0, z), PBRICK))
    for face, (fx, fy) in (("S", (0, -w1 / 2)), ("N", (0, w1 / 2))):
        parts.append(arch_panel(f"door{face}", 1.9, 3.6, (fx, fy, z + 0.1), face, DARK, pointed=False, depth=0.7))
        parts.append(box(f"lintel{face}", 3.0, 0.5, 0.35, (fx, fy, z + 3.8), shade(PBRICK, 0.1)))
    z += h1
    n = 15
    ws = []
    for i in range(1, n):
        t = i / (n - 1)
        ws.append(w1 * (1.02 + 0.05 * math.sin(math.pi * t * 1.1) - 0.52 * t ** 1.9))
    prev = w1 * 0.99
    for i, w in enumerate(ws):
        c, z = corbel(f"c{i}", prev, w, z, 4, 2, 0.13, 0.15, PBRICK, saw=True)
        parts.append(c)
        bh = 1.62 - 0.05 * i
        parts.append(frustum(f"s{i + 1}", w, w, w * 0.99, w * 0.99, bh, (0, 0, z), shade(PBRICK, 0.02 * ((i % 2) - 0.5))))
        for face, (fx, fy) in (("S", (0, -w / 2)), ("N", (0, w / 2))):
            parts.append(arch_panel(f"win{i}{face}", 0.75, min(1.25, bh * 0.75), (fx, fy, z + 0.15), face, DARK, pointed=False, depth=0.5))
        z += bh
        prev = w * 0.99
    c, z = corbel("ctop", prev, prev * 0.7, z, 4, 3, 0.12, 0.15, PBRICK, saw=True)
    parts.append(c)
    parts.append(frustum("cap", prev * 0.7, prev * 0.7, prev * 0.3, prev * 0.3, 1.2, (0, 0, z), PBRICK))
    parts.append(cylinder("lotus", 0.9, 0.5, (0, 0, z + 1.2), shade(PBRICK, 0.08), verts=12, r_top=1.2))
    parts.append(dome("bao", 0.8, (0, 0, z + 1.7), shade(PBRICK, 0.1), squash=1.4, segments=12, rings=8))
    parts.append(cylinder("spike", 0.12, 1.6, (0, 0, z + 2.6), BRONZE, verts=6))
    m.add(1, join(parts, "pagoda"), "pagoda")
    # the court: a gate, a small hall to the north, the bell pavilion, trees
    body, roof = gate_parts("gate", 12, 6, 4.5, 3.4, roof_h=3.8, bays=3, top="hip", trim=GLAZE, shibi=CHIWEI)
    m.add(1, move(body, 0, -W / 2 + 2, 0.3), "court")
    m.add(2, move(roof, 0, -W / 2 + 2, 0.3), "roofs")
    tang_hall(m, "hall", 20, 11, 5.0, 0, 38, z=0.3, bays=5, plat=1.0, roof="irimoya", roof_h=4.6)
    lou(m, "bell", 7, 7, 3.6, 3.0, 34, -30, z=0.3, plat=0.6, roof="hip", trim=GLAZE)
    trees(m, "trees", [(-34, -34), (-38, 10), (-30, 34), (36, 10), (22, -42), (-20, -44), (40, 40)], 3.6, LOCUST)
    return m


# ---------------------------------------------------------------- the palaces and gates

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


def que_tower(m, name, x, y, s, sb=1, sr=2):
    """A triple-stepped que: a main tower on a high brick bastion, two lower towers stepping outward (s = +1 east, -1 west)."""
    tiers = [(0.0, 34, 30, 15.0, 19, 15, 6.0, 5.0), (s * 26, 18, 22, 12.0, 12, 10, 4.6, 0), (s * 40, 12, 15, 9.0, 8.5, 8, 3.8, 0)]
    for i, (dx, tw, td, th, hw, hd, h1, h2) in enumerate(tiers):
        m.add(0, terrace(f"{name}_b{i}", tw, td, th, (x + dx, y, 0), EARTH, BRICKF, batter=0.05), "terraces")
        m.add(0, move(merlons(f"{name}_m{i}", tw - 1.0, td - 1.0, th, 0.8, 1.4, shade(BRICKF, 0.05)), x + dx, y))
        if h2:
            lou(m, f"{name}_t{i}", hw, hd, h1, h2, x + dx, y, z=th, plat=0.5, roof="hip", trim=GLAZE, shibi=CHIWEI, sb=sb, sr=sr)
        else:
            tang_hall(m, f"{name}_t{i}", hw, hd, h1, x + dx, y, z=th, bays=3, plat=0.5, roof="hip", roof_h=hd * 0.5, sb=sb, sr=sr, stairs=False)


def hanyuan_hall():
    """The Hanyuan Hall on its three terraces at the edge of the Longshou plateau, the flanking Xiangluan and Qifeng towers
    joined to it by raised galleries, and the three long ramps of the Dragon-Tail Way."""
    m = Model("hanyuan-hall")
    W, D = 320, 300
    m.add(0, box("ground", W, D, 0.3, (0, 0, 0), GRAVEL), "terraces")
    m.add(0, box("plateau", W, 110, 4.0, (0, 95, 0), EARTH))
    m.add(0, box("plateau_face", W, 1.2, 4.2, (0, 40, 0), shade(BRICKF, 0.02)))
    m.add(0, terrace("t1", 170, 90, 5.0, (0, 95, 4.0), EARTH, BRICKF, batter=0.04, rail=True))
    m.add(0, terrace("t2", 112, 64, 4.0, (0, 97, 9.0), EARTH, BRICKF, batter=0.04, rail=True))
    m.add(0, terrace("t3", 86, 48, 2.5, (0, 99, 13.0), shade(STONE, 0.05), shade(STONE, -0.05), batter=0.02, rail=True, rail_color=WHITE))
    for xs in (-24, 24):
        m.add(0, stair(f"st2{xs}", 9, 4.0, 7, 8, (xs, 65 - 3.5, 9.0), "S", STONE))
        m.add(0, stair(f"st3{xs}", 7, 2.5, 4, 5, (xs, 75 - 2.0, 13.0), "S", STONE))
    # the Dragon-Tail Way: three ramps in two flights, two landings and a causeway onto the first terrace
    m.add(0, terrace("landing1", 70, 14, 4.0, (0, -55, 0.3), EARTH, BRICKF, batter=0.03))
    m.add(0, terrace("landing2", 70, 14, 9.0, (0, -1, 0.3), EARTH, BRICKF, batter=0.03))
    m.add(0, terrace("causeway", 64, 44, 9.0, (0, 28, 0.3), EARTH, BRICKF, batter=0.03))
    for k, xc in enumerate((-22, 0, 22)):
        m.add(0, ramp(f"rampA{k}", xc - 4.5, xc + 4.5, -112, -62, 0.3, 4.3, shade(BRICKF, 0.06)))
        m.add(0, ramp(f"rampB{k}", xc - 4.5, xc + 4.5, -48, -8, 4.3, 9.3, shade(BRICKF, 0.06)))
        m.add(1, ramp_rails(f"railA{k}", xc - 4.5, xc + 4.5, -112, -62, 0.3, 4.3, WHITE, 8), "rails")
        m.add(1, ramp_rails(f"railB{k}", xc - 4.5, xc + 4.5, -48, -8, 4.3, 9.3, WHITE, 7))
    m.add(1, balustrade("rail_l2", rect_pts(69, 13, 0, -1), 1.0, WHITE, 3.0, True, 9.3))
    m.add(1, balustrade("rail_cw", [(-31.5, 6), (-31.5, 50)], 1.0, WHITE, 3.0, False, 9.3))
    m.add(1, balustrade("rail_cw2", [(31.5, 6), (31.5, 50)], 1.0, WHITE, 3.0, False, 9.3))
    # the hall: eleven bays with its surrounding gallery, a hipped roof with green trim and dark fins
    tang_hall(m, "hanyuan", 74, 34, 11.0, 0, 99, z=15.5, bays=11, roof="hip", roof_h=13.5, plat=0.6, over=7.5, sb=1, sr=2, stairs=False)
    m.add(1, box("inner_wall", 60, 20, 10.5, (0, 99, 16.1), shade(WHITE, -0.04)))
    # the towers on their bastions and the galleries that join them to the hall terrace
    for s in (-1, 1):
        que_tower(m, f"que{s}", s * 112, 20, s)
        m.add(0, terrace(f"wing{s}a", 60, 9, 13.0, (s * 86, 97, 0), EARTH, BRICKF, batter=0.03))
        m.add(0, terrace(f"wing{s}b", 9, 50, 13.0, (s * 112, 61, 0), EARTH, BRICKF, batter=0.03))
        g = gallery(f"feilang{s}", [(s * 56, 97), (s * 112, 97), (s * 112, 34)], w=6, h=3.6, col=VERM, roof=TILE, wall=WHITE)
        m.add(1, move(g, 0, 0, 13.0), "halls")
    # the court below: banners and guard posts along the approach
    poles = []
    cols = ("#B8452E", "#3E5C9A", "#D4AE55", "#EEE7D8", "#3F8A62")
    for i, y in enumerate(range(-140, -60, 16)):
        for s in (-1, 1):
            x = s * 42
            poles.append(cylinder(f"pole{i}{s}", 0.25, 10, (x, y, 0.3), VERM, verts=6))
            poles.append(box(f"flag{i}{s}", 0.15, 1.8, 4.0, (x, y + 1.0, 5.8), cols[(i + (s > 0)) % 5]))
    m.add(2, join(poles, "banners"), "banners")
    m.add(0, box("road", 70, 40, 0.06, (0, -130, 0.3), shade(GRAVEL, -0.08)))
    for s in (-1, 1):
        tang_hall(m, f"chaotang{s}", 56, 14, 6.5, s * 92, -95, deg=-90 * s, z=0.3, bays=11, plat=1.2, roof="irimoya", roof_h=6.0)
        lou(m, f"belldrum{s}", 11, 11, 5.0, 4.0, s * 92, -30, z=0.3, plat=1.2, roof="hip", trim=GLAZE, shibi=CHIWEI)
        m.add(1, move(gallery(f"court_gal{s}", [(s * 150, -148), (s * 150, 38)], w=5, h=3.4, wall=WHITE), 0, 0, 0.3))
    # the complaint drum and the red lung-stone before the west and east court halls
    m.add(1, join([cylinder("drum", 1.4, 1.6, (-72, -120, 1.6), "#9A3A2A", verts=12), box("drum_stand", 2.6, 1.0, 1.6, (-72, -120, 0.3), WOOD),
                   box("lung_stone", 2.2, 1.4, 1.6, (72, -120, 0.3), "#A8503A")], "petition"))
    trees(m, "trees", [(-150, -130), (150, -130), (-150, 135), (150, 135), (-80, 140), (80, 140)], 4.2, PINE)
    return m


def hanyuan_ruin():
    m = Model("hanyuan-hall-ruin")
    W, D = 320, 300
    m.add(0, box("ground", W, D, 0.3, (0, 0, 0), FIELD), "fields")
    strips = []
    for i in range(16):
        x = -W / 2 + 10 + i * 20
        strips.append(box(f"s{i}", 18, 120, 0.15, (x, -85, 0.3), shade(FIELD, 0.07 * ((i % 3) - 1))))
    m.add(0, join(strips, "strips"))
    m.add(0, frustum("plateau", W, 112, W - 10, 100, 3.5, (0, 95, 0.3), shade(EARTH, -0.02)), "mounds")
    m.add(0, frustum("mound1", 150, 82, 120, 60, 6.5, (0, 97, 3.8), EARTH))
    m.add(0, frustum("mound2", 92, 50, 70, 36, 5.0, (0, 99, 10.3), shade(EARTH, 0.05)))
    m.add(0, frustum("tail", 54, 120, 30, 110, 4.5, (0, -20, 0.3), shade(EARTH, 0.03)))
    for s in (-1, 1):
        m.add(0, frustum(f"que{s}", 40, 28, 22, 16, 10.0, (s * 116, 20, 0.3), shade(EARTH, -0.04)))
        m.add(0, frustum(f"wing{s}", 50, 8, 44, 4, 5.0, (s * 86, 97, 3.8), shade(EARTH, -0.04)))
    stones = [cylinder(f"fs{i}{j}", 0.9, 0.5, (-30 + i * 6, 99 - 9 + j * 6, 15.3), STONE, verts=8) for i in range(11) for j in range(4) if (i + j) % 3]
    m.add(1, join(stones, "column_bases"), "ruins")
    m.add(1, move(yard_houses("farm1", 0, 0, 24, 20, 3.4, CLAY, TILE), -110, -100, 0.3), "village")
    m.add(1, move(yard_houses("farm2", 0, 0, 20, 18, 3.2, CLAY, TILE, 1), 120, -110, 0.3))
    m.add(1, box("cave", 3, 0.5, 2.2, (40, 57, 4.0), DARK))
    trees(m, "trees", [(-130, -70), (-95, -125), (135, -85), (100, 140), (-140, 140), (60, 150)], 4.0, LOCUST)
    return m


def chengtianmen():
    m = Model("chengtianmen")
    m.add(0, box("ground", 140, 44, 0.3, (0, 0, 0), GRAVEL), "gates")
    tang_gate(m, "ct", 80, 30, 11.0, 3, 7.0, 56, 18, 8.0, 9, wall_len=70, roof_h=8.0)
    for s in (-1, 1):
        lou(m, f"que{s}", 13, 11, 4.5, 3.6, s * 59, 0, z=10.1, plat=0.4, roof="hip", trim=GLAZE, shibi=CHIWEI)
        g = gallery(f"gal{s}", [(s * 28, 0), (s * 52, 0)], w=4.5, h=3.2, col=VERM, roof=TILE)
        m.add(1, move(g, 0, 0, 11.0))
    return m


def zhuquemen():
    m = Model("zhuquemen")
    m.add(0, box("ground", 90, 34, 0.3, (0, 0, 0), GRAVEL), "gates")
    tang_gate(m, "zq", 56, 22, 9.0, 3, 6.0, 36, 13, 6.5, 5, wall_len=45, roof_h=6.0)
    return m


def danfengmen():
    m = Model("danfengmen")
    m.add(0, box("ground", 180, 60, 0.3, (0, 0, 0), GRAVEL), "gates")
    tang_gate(m, "df", 75, 33, 10.0, 5, 8.5, 60, 18, 8.0, 11, wall_len=90, roof_h=8.5, ramps=True)
    return m


def taiji_palace():
    m = Model("taiji-palace")
    W, D = 360, 440
    m.add(0, box("ground", W, D, 0.3, (0, 0, 0), GRAVEL), "grounds")
    # the front court with its cloister and the Taiji gate
    m.add(0, gallery("kairo", rect_pts(340, 300, 0, -54), w=6, h=4.0, closed=True, wall=WHITE), "court")
    m.add(0, terrace("gate_t", 64, 20, 2.0, (0, -204, 0.3)))
    tang_hall(m, "taijimen", 48, 14, 7.0, 0, -204, z=2.3, bays=7, plat=0.4, roof_h=6.0, stairs=False)
    m.add(1, box("gate_open", 14, 15, 5.5, (0, -204, 2.7), DARK))
    # the throne hall on its two-tier terrace with paired stairs
    m.add(0, terrace("t1", 136, 70, 3.4, (0, 12, 0.3), EARTH, BRICKF, rail=True))
    m.add(0, terrace("t2", 106, 50, 2.4, (0, 14, 3.7), EARTH, BRICKF, rail=True, rail_color=WHITE))
    for xs in (-22, 22):
        m.add(0, stair(f"st1{xs}", 9, 3.4, 7, 7, (xs, 12 - 35 - 3.5, 0.3), "S", STONE))
        m.add(0, stair(f"st2{xs}", 8, 2.4, 5, 6, (xs, 14 - 25 - 2.5, 3.7), "S", STONE))
    tang_hall(m, "taiji", 82, 36, 12.5, 0, 14, z=6.1, bays=13, roof="hip", roof_h=15.0, plat=0.6, over=8.0, stairs=False)
    m.add(0, box("dao", 12, 180, 0.08, (0, -114, 0.3), STONE))
    marks = []
    for i in range(12):
        for s in (-1, 1):
            marks.append(box(f"rank{i}{s}", 0.8, 0.5, 1.2, (s * 14, -190 + i * 13, 0.3), "#A9A397"))
    for s in (-1, 1):
        for y in (-60, -120):
            marks.append(cylinder(f"censer{s}{y}", 1.4, 1.8, (s * 30, y, 0.3), BRONZE, verts=10))
            marks.append(cylinder(f"censer_t{s}{y}", 1.0, 1.2, (s * 30, y, 2.1), BRONZE, verts=10, r_top=0.3))
    m.add(1, join(marks, "rank_markers"), "court")
    tree_row(m, "locusts_w", (-150, -180), (-150, 60), 10, 4.0, LOCUST)
    tree_row(m, "locusts_e", (150, -180), (150, 60), 10, 4.0, LOCUST)
    for s in (-1, 1):
        tang_hall(m, f"side{s}", 56, 14, 6.0, s * 130, -80, deg=-90 * s, z=0.3, bays=11, plat=1.0, roof="irimoya", roof_h=6.0)
        lou(m, f"lou{s}", 16, 13, 6.0, 5.0, s * 70, -150, z=0.3, plat=1.2, roof="hip", trim=GLAZE, shibi=CHIWEI)
        body, roof = gate_parts(f"sidegate{s}", 18, 8, 5.5, 4.0, roof_h=5.0, bays=5, top="hip", trim=GLAZE, shibi=CHIWEI)
        m.add(1, put(body, s * 170, -40, -90 * s, 0.3))
        m.add(2, put(roof, s * 170, -40, -90 * s, 0.3))
    # the inner court and the Liangyi Hall behind
    m.add(0, gallery("kairo2", rect_pts(240, 120, 0, 156), w=5, h=3.6, closed=True, wall=WHITE))
    body, roof = gate_parts("zhumingmen", 22, 9, 6.0, 4.5, roof_h=5.5, bays=5, top="hip", trim=GLAZE, shibi=CHIWEI)
    m.add(1, move(body, 0, 96, 0.3), "court")
    m.add(2, move(roof, 0, 96, 0.3), "roofs")
    m.add(0, terrace("t3", 70, 36, 2.0, (0, 170, 0.3), EARTH, BRICKF, rail=True))
    tang_hall(m, "liangyi", 50, 24, 9.0, 0, 170, z=2.3, bays=9, roof="hip", roof_h=10.0, plat=0.4, stairs=False)
    for s in (-1, 1):
        tang_hall(m, f"inner{s}", 30, 12, 5.0, s * 85, 160, deg=-90 * s, z=0.3, bays=7, plat=0.8, roof="irimoya", roof_h=5.0)
    trees(m, "trees", [(-160, -200), (160, -200), (-165, 60), (165, 60), (-160, 205), (160, 205), (-140, 120), (140, 120)], 4.5, PINE)
    return m


# ---------------------------------------------------------------- markets and Xingqing

def market(west=False):
    """A walled market of two wards: four lanes in a '#' making nine blocks, shops facing the lanes, the market office in the middle."""
    m = Model("west-market" if west else "east-market")
    W, D = 920, 900
    m.add(0, box("ground", W, D, 0.3, (0, 0, 0), EARTH), "grounds")
    lanes = [box(f"lx{i}", 30, D - 20, 0.06, (x, 0, 0.3), shade(EARTH, -0.1)) for i, x in enumerate((-150, 150))]
    lanes += [box(f"ly{i}", W - 20, 30, 0.06, (0, y, 0.3), shade(EARTH, -0.1)) for i, y in enumerate((-150, 150))]
    lanes += [box(f"ring{i}", W - 20, 12, 0.05, (0, s * (D / 2 - 18), 0.3), shade(EARTH, -0.06)) for i, s in enumerate((-1, 1))]
    lanes += [box(f"ringv{i}", 12, D - 20, 0.05, (s * (W / 2 - 18), 0, 0.3), shade(EARTH, -0.06)) for i, s in enumerate((-1, 1))]
    m.add(0, join(lanes, "lanes"))
    gaps = [(side, off, 16) for side in ("S", "N") for off in (-150, 150)] + [(side, off, 16) for side in ("E", "W") for off in (-150, 150)]
    m.add(0, walled("wall", W - 6, D - 6, 4.0, 2.0, gaps, CLAY, TILE), "walls")
    for i, (x, y, deg) in enumerate([(-150, -D / 2 + 3, 0), (150, -D / 2 + 3, 0), (-150, D / 2 - 3, 180), (150, D / 2 - 3, 180),
                                     (W / 2 - 3, -150, 90), (W / 2 - 3, 150, 90), (-W / 2 + 3, -150, -90), (-W / 2 + 3, 150, -90)]):
        m.add(1, put(small_gate(f"gate{i}", 14, 6, 5.0, VERM, TILE, "irimoya"), x, y, deg), "shops")
    awn = ["#8C6A4A", "#7A5A42", "#9A7A56"] if not west else ["#A0503A", "#3E5C7A", "#B08A4A", "#6A7A4A"]
    k = 0
    for bx0, bx1 in ((-440, -167), (-133, 133), (167, 440)):
        for by0, by1 in ((-430, -167), (-133, 133), (167, 430)):
            centre = bx0 == -133 and by0 == -133
            cx, cy = (bx0 + bx1) / 2, (by0 + by1) / 2
            rows = []
            rows.append(shop_row(f"rs{k}", bx0 + 10, bx1 - 10, by0 + 5, 9, 4.2, 17, -1, TILE, CLAY, awn[k % len(awn)]))
            rows.append(shop_row(f"rn{k}", bx0 + 10, bx1 - 10, by1 - 5, 9, 4.2, 17, 1, TILE, CLAY, awn[(k + 1) % len(awn)]))
            side = shop_row(f"rw{k}", by0 + 16, by1 - 16, 0, 9, 4.0, 17, -1, TILE, CLAY, awn[(k + 2) % len(awn)])
            rows.append(put(side, bx0 + 5, 0, -90))
            side = shop_row(f"re{k}", by0 + 16, by1 - 16, 0, 9, 4.0, 17, -1, TILE, CLAY, awn[k % len(awn)])
            rows.append(put(side, bx1 - 5, 0, 90))
            if not centre:
                pond_block = west and bx0 == 167 and by0 == -430
                y = by0 + 34
                j = 0
                while y + 21 < by1 - 24:
                    if not (pond_block and y < cy + 30):
                        for f, yy in ((-1, y), (1, y + 10)):
                            rows.append(shop_row(f"in{k}_{j}{f}", bx0 + 26, bx1 - 26, yy, 9, 4.4 + 0.6 * ((j + k) % 3), 24, f, TILE, CLAY,
                                                 awn[(j + k + (f > 0)) % len(awn)], doors=False, posts=False))
                    y += 31
                    j += 1
            m.add(1, move(join(rows, f"block{k}"), 0, 0, 0.3))
            k += 1
    # the market office, its drum tower and the standard weights hall in the central block
    m.add(0, box("plaza", 200, 200, 0.05, (0, 0, 0.3), shade(GRAVEL, -0.04)))
    tang_hall(m, "office", 34, 16, 5.5, 0, 30, z=0.3, bays=7, plat=1.0, roof="irimoya", roof_h=5.5, bk=False)
    tang_hall(m, "pingzhun", 26, 12, 5.0, -50, -20, deg=-90, z=0.3, bays=5, plat=0.8, roof="irimoya", roof_h=4.8, bk=False)
    lou(m, "drum", 9, 9, 4.0, 3.4, 40, -35, z=0.3, plat=0.8, roof="hip", trim=GLAZE)
    m.add(1, cylinder("well", 1.8, 0.9, (0, -40, 0.3), STONE, verts=12))
    trees(m, "trees", [(-60, 70), (60, 70), (-70, -70), (70, 75), (0, -75)], 4.0, LOCUST)
    tree_row(m, "lane_trees", (-140, -400), (-140, 400), 14, 3.2, WILLOW)
    tree_row(m, "lane_trees2", (140, -400), (140, 400), 14, 3.2, WILLOW)
    if west:
        # the timber pond fed by the canal of 742, with stacks of logs, in the south-east block
        m.add(0, blob("pond", 70, 45, 0.25, (300, -300, 0.3), WATERC, 1.2), "grounds")
        logs = []
        for i in range(6):
            for j in range(3):
                logs.append(cylinder(f"log{i}{j}", 0.5, 14, (0, 0, 0), WOOD, verts=8))
                lg = logs[-1]
                lg.rotation_euler[1] = math.pi / 2
                bpy.context.view_layer.objects.active = lg
                bpy.ops.object.select_all(action="DESELECT")
                lg.select_set(True)
                bpy.ops.object.transform_apply(rotation=True)
                move(lg, 230 + i * 3, -230 - j * 4, 0.8 + (i % 2) * 0.8)
        m.add(1, join(logs, "logs"))
        m.add(1, box("landing", 16, 30, 0.6, (360, -300, 0.3), WOOD))
    return m


def xingqing_palace():
    """A portion of the Xingqing Palace: the Dragon Pond and the Chenxiang Pavilion, the two towers by the south-west wall, the main halls behind."""
    m = Model("xingqing-palace")
    W, D = 620, 560
    m.add(0, box("ground", W, D, 0.3, (0, 0, 0), shade(GRASS, 0.05)), "grounds")
    m.add(0, walled("wall", W - 8, D - 8, 5.0, 2.2, (("N", 0, 14), ("S", 120, 14), ("W", -60, 12)), CLAY, TILE), "walls")
    m.add(0, blob("pond", 175, 100, 0.25, (40, -55, 0.3), WATERC, 0.7, 36), "pond")
    m.add(0, blob("shore", 182, 107, 0.2, (40, -55, 0.3), shade(GRAVEL, -0.05), 0.7, 36))
    # the Chenxiang Pavilion on its terrace above the peony beds, north-east of the pond
    m.add(0, terrace("cx_t", 34, 34, 3.0, (175, 85, 0.3), STONE, shade(STONE, -0.08), batter=0.03, rail=True, rail_color=WHITE))
    m.add(0, stair("cx_st", 8, 3.0, 5, 6, (175, 85 - 17 - 2.5, 0.3), "S", STONE))
    lou(m, "chenxiang", 15, 15, 4.5, 3.8, 175, 85, z=3.3, plat=0.4, roof="hip", roof_h=6.5, col="#8A4A30", trim=GLAZE, shibi=CHIWEI)
    pc = ("#C8607A", "#E8D8D0", "#A83A4A", "#D88AA0")
    for c in range(4):
        pts = [(140 + (i % 9) * 8.5 + (c % 2) * 4, (52 if i < 9 else 120) + (c // 2) * 4, 0.3) for i in range(18) if i % 4 == c]
        m.add(2, grove(f"peony{c}", pts, 1.8, pc[c]), "gardens")
    # the Huae Xianghui and Qinzheng Wuben towers by the south-west walls
    m.add(0, terrace("hx_t", 46, 30, 6.0, (-240, -232, 0.3), EARTH, BRICKF))
    lou(m, "huae", 34, 18, 6.0, 5.0, -240, -232, z=6.3, plat=0.4, roof="irimoya", roof_h=8.0, trim=GLAZE, shibi=CHIWEI, double_top=True)
    m.add(0, terrace("qz_t", 30, 44, 6.0, (-288, -150, 0.3), EARTH, BRICKF))
    lou(m, "qinzheng", 26, 16, 5.5, 4.5, -288, -150, deg=-90, z=6.3, plat=0.4, roof="irimoya", roof_h=7.0, trim=GLAZE, shibi=CHIWEI)
    # the main halls in the north: the Xingqing Hall in its court, and the Nanxun Hall
    m.add(0, gallery("court", rect_pts(220, 120, -40, 195), w=5, h=3.6, closed=True, wall=WHITE), "halls")
    m.add(0, terrace("xq_t", 66, 30, 2.0, (-40, 215, 0.3), EARTH, BRICKF, rail=True))
    tang_hall(m, "xingqing", 48, 22, 8.5, -40, 215, z=2.3, bays=9, roof="hip", roof_h=9.0, plat=0.4, stairs=False)
    body, roof = gate_parts("xq_gate", 18, 8, 5.5, 4.0, roof_h=5.0, bays=5, top="hip", trim=GLAZE, shibi=CHIWEI)
    m.add(1, move(body, -40, 135, 0.3))
    m.add(2, move(roof, -40, 135, 0.3))
    tang_hall(m, "nanxun", 34, 16, 7.0, 170, 205, z=0.3, bays=7, roof="irimoya", roof_h=7.0, plat=1.4)
    tang_hall(m, "longtang", 26, 12, 6.0, -120, 20, z=0.3, bays=5, roof="irimoya", roof_h=5.5, plat=1.2)
    # a dragon boat on the pond
    boat = [box("hull", 18, 4.5, 1.4, (40, -70, 0.4), "#9A3A2A"), box("cabin", 7, 3.4, 2.4, (40, -70, 1.8), "#C9A24A"),
            eaved_roof("cabin_r", 7, 3.4, 1.4, (40, -70, 4.2), GLAZE, over=1.0), box("head", 2.0, 1.2, 2.6, (49.5, -70, 0.6), GILT)]
    m.add(2, join(boat, "boat"))
    willows = [(40 + 192 * math.cos(a), -55 + 114 * math.sin(a)) for a in [i * math.tau / 24 for i in range(24)]]
    trees(m, "willows", [p for p in willows if not (130 < p[0] < 210 and p[1] > 20) and not (-140 < p[0] < -100 and 0 < p[1] < 40)], 6.5, WILLOW)
    trees(m, "pines", [(-200, 100), (-250, 40), (250, -180), (260, 150), (-150, -230), (100, 250), (-260, 110), (240, -60), (-60, -200), (150, -200)], 6.0, PINE)
    # the Changqing and Hualu halls to the east, residential courts to the north-west, covered ways and paths
    tang_hall(m, "changqing", 38, 16, 7.0, 240, 40, z=0.3, bays=7, roof="irimoya", roof_h=7.0, plat=1.4)
    tang_hall(m, "hualu", 30, 14, 6.0, 245, -110, deg=90, z=0.3, bays=7, roof="irimoya", roof_h=6.0, plat=1.2)
    for i, (x, y) in enumerate(((-250, 230), (-200, 230), (-250, 175), (-200, 175), (60, 235), (110, 235))):
        m.add(1, yard_houses(f"res{i}", x, y, 42, 40, 5.0, shade(WHITE, -0.1), TILE, i), "halls")
    m.add(1, move(gallery("way1", [(175, 103), (175, 186)], w=4.5, h=3.2), 0, 0, 0.3))
    m.add(1, move(gallery("way2", [(-40, 135 - 4), (-40, 60), (-100, 30)], w=4.5, h=3.2), 0, 0, 0.3))
    paths = [box("p1", 8, 100, 0.06, (120, -215, 0.3), shade(GRAVEL, -0.05)), box("p2", 240, 7, 0.06, (0, 95, 0.3), shade(GRAVEL, -0.05)),
             box("p3", 7, 90, 0.06, (-40, 90 - 45, 0.3), shade(GRAVEL, -0.05))]
    m.add(0, join(paths, "paths"))
    return m


# ---------------------------------------------------------------- temples, abbey, academy, church

def temple_gate(m, name, x, y, w=20, d=9, deg=0, sb=1, sr=2):
    body, roof = gate_parts(name, w, d, 5.5, 4.2, roof_h=5.0, bays=5, top="hip", trim=GLAZE, shibi=CHIWEI)
    m.add(sb, put(body, x, y, deg, 0.3), "halls")
    m.add(sr, put(roof, x, y, deg, 0.3), "roofs")


def daxingshan_si():
    m = Model("daxingshan-si")
    W = 300
    m.add(0, box("ground", W, W, 0.3, (0, 0, 0), GRAVEL), "grounds")
    m.add(0, walled("wall", W - 6, W - 6, 3.6, 1.6, (("S", 0, 22), ("N", 0, 8)), CLAY, TILE), "walls")
    temple_gate(m, "nandamen", 0, -W / 2 + 3, 24, 10)
    m.add(0, gallery("kairo", rect_pts(170, 150, 0, -10), w=6, h=3.8, closed=True, wall=WHITE), "walls")
    temple_gate(m, "zhongmen", 0, -85, 18, 8)
    m.add(1, put(tpagoda("pagoda", 11.0, 5, 52.0), 0, -40, 0, 0.3), "pagoda")
    m.add(0, terrace("fd_t", 48, 28, 1.8, (0, 30, 0.3), EARTH, BRICKF, rail=True))
    tang_hall(m, "fodian", 38, 20, 8.5, 0, 30, z=2.1, bays=7, roof="hip", roof_h=9.0, plat=0.4, stairs=False)
    tang_hall(m, "jiangtang", 44, 18, 7.0, 0, 100, z=0.3, bays=9, roof="irimoya", roof_h=7.5, plat=1.2)
    for s in (-1, 1):
        lou(m, f"lou{s}", 10, 9, 4.2, 3.6, s * 45, -60, z=0.3, plat=0.8, roof="hip", trim=GLAZE, shibi=CHIWEI)
        for i in range(4):
            tang_hall(m, f"sengfang{s}{i}", 50, 10, 4.2, s * 122, -100 + i * 66, deg=-90 * s, z=0.3, bays=10, plat=0.5, roof="gable", roof_h=3.8, bk=False, shibi=None, trim=None)
        tang_hall(m, f"back{s}", 40, 10, 4.2, s * 60, 132, z=0.3, bays=8, plat=0.5, roof="gable", roof_h=3.6, bk=False, shibi=None, trim=None)
    trees(m, "trees", [(-80, -120), (80, -120), (-90, 70), (90, 70), (-30, 132), (30, 132), (-100, 0), (100, 0)], 4.5, PINE)
    return m


def xuandu_guan():
    m = Model("xuandu-guan")
    W = 240
    m.add(0, box("ground", W, W, 0.3, (0, 0, 0), GRAVEL), "grounds")
    m.add(0, walled("wall", W - 6, W - 6, 3.6, 1.6, (("S", 0, 18),), CLAY, TILE), "walls")
    temple_gate(m, "gate", 0, -W / 2 + 3, 20, 9)
    # a three-tiered altar for the great Taoist rites, with stairs on four sides
    for i, (w, h) in enumerate(((44, 1.6), (34, 1.6), (24, 1.6))):
        m.add(0, terrace(f"altar{i}", w, w, h, (0, -40, 0.3 + i * 1.6), shade(EARTH, 0.04 * i), shade(STONE, -0.05 + 0.04 * i), batter=0.0, rail=True, rail_color=WHITE), "altar")
    for face, (dx, dy) in (("S", (0, -1)), ("N", (0, 1)), ("E", (1, 0)), ("W", (-1, 0))):
        m.add(0, stair(f"ast{face}", 5, 4.8, 10, 10, (dx * 27, -40 + dy * 27, 0.3), face, STONE))
    m.add(1, cylinder("censer", 1.5, 2.2, (0, -40, 5.1), BRONZE, verts=10), "altar")
    m.add(0, terrace("hall_t", 50, 28, 1.8, (0, 55, 0.3), EARTH, BRICKF, rail=True))
    tang_hall(m, "sanqing", 38, 20, 8.0, 0, 55, z=2.1, bays=7, roof="hip", roof_h=8.5, plat=0.4, stairs=False)
    for s in (-1, 1):
        lou(m, f"jinglou{s}", 14, 12, 5.0, 4.2, s * 66, 0, z=0.3, plat=1.0, roof="hip", trim=GLAZE, shibi=CHIWEI)
        tang_hall(m, f"side{s}", 40, 10, 4.5, s * 95, 60, deg=-90 * s, z=0.3, bays=8, plat=0.6, roof="irimoya", roof_h=4.5, bk=False)
    tang_hall(m, "back", 50, 12, 5.0, 0, 100, z=0.3, bays=10, plat=0.6, roof="irimoya", roof_h=5.0, bk=False)
    trees(m, "cypress", [(-40, -90), (40, -90), (-60, -40), (60, -40), (-90, -80), (90, -80), (-40, 100 - 25), (45, 75)], 3.6, "#4E6A44")
    return m


def ximing_si():
    m = Model("ximing-si")
    W, D = 220, 260
    m.add(0, box("ground", W, D, 0.3, (0, 0, 0), GRAVEL), "grounds")
    m.add(0, walled("wall", W - 6, D - 6, 3.6, 1.6, (("S", 0, 20),), CLAY, TILE), "walls")
    temple_gate(m, "gate", 0, -D / 2 + 3, 22, 9)
    m.add(0, gallery("kairo", rect_pts(130, 130, 0, -5), w=6, h=3.8, closed=True, wall=WHITE), "walls")
    temple_gate(m, "zhongmen", 0, -70, 18, 8)
    m.add(0, terrace("fd_t", 44, 26, 1.6, (0, 5, 0.3), EARTH, BRICKF, rail=True))
    tang_hall(m, "fodian", 34, 18, 8.0, 0, 5, z=1.9, bays=7, roof="hip", roof_h=8.5, plat=0.4, stairs=False)
    lou(m, "jingzang", 26, 14, 5.0, 4.5, 0, 90, z=0.3, plat=1.2, roof="irimoya", roof_h=6.0, shibi=CHIWEI)
    m.add(1, put(tpagoda("pagoda", 8.0, 5, 38.0), -75, -85, 0, 0.3), "halls")
    for s in (-1, 1):
        tang_hall(m, f"side{s}", 36, 10, 4.5, s * 88, 20, deg=-90 * s, z=0.3, bays=7, plat=0.6, roof="irimoya", roof_h=4.5, bk=False)
        tang_hall(m, f"back{s}", 34, 10, 4.2, s * 60, 112, z=0.3, bays=7, plat=0.5, roof="gable", roof_h=3.6, bk=False, shibi=None, trim=None)
    tang_hall(m, "east_court", 30, 12, 5.0, 75, -85, z=0.3, bays=6, plat=0.8, roof="irimoya", roof_h=5.0, bk=False)
    trees(m, "trees", [(-90, -110), (90, -110), (-60, 60), (60, 60), (-95, 90), (95, 90)], 4.2, PINE)
    return m


def guozijian():
    m = Model("guozijian")
    W, D = 260, 220
    m.add(0, box("ground", W, D, 0.3, (0, 0, 0), GRAVEL), "grounds")
    m.add(0, walled("wall", W - 6, D - 6, 3.4, 1.5, (("S", -60, 14), ("S", 60, 12)), CLAY, TILE), "walls")
    # the Temple of Confucius on the west: a gate, a cloistered court, the hall of the sage
    m.add(0, gallery("kairo", rect_pts(100, 120, -60, -10), w=5, h=3.6, closed=True, wall=WHITE))
    temple_gate(m, "gate", -60, -D / 2 + 3, 18, 8)
    m.add(0, terrace("dc_t", 36, 22, 1.6, (-60, 10, 0.3), EARTH, BRICKF, rail=True))
    tang_hall(m, "wenxuan", 28, 15, 7.0, -60, 10, z=1.9, bays=7, roof="hip", roof_h=7.0, plat=0.4, stairs=False)
    # the lecture hall, dormitories and library on the east
    tang_hall(m, "lecture", 40, 16, 6.5, 60, 0, z=0.3, bays=9, roof="irimoya", roof_h=6.5, plat=1.2)
    for i in range(4):
        tang_hall(m, f"dorm{i}", 70, 9, 3.8, 60, -80 + i * 20 if i < 2 else 40 + (i - 2) * 20, z=0.3, bays=12, plat=0.4, roof="gable", roof_h=3.2, bk=False, shibi=None, trim=None)
    lou(m, "library", 22, 12, 4.8, 4.0, -60, 85, z=0.3, plat=1.0, roof="irimoya", roof_h=5.5, shibi=CHIWEI)
    temple_gate(m, "gate2", 60, -D / 2 + 3, 14, 7)
    trees(m, "trees", [(-110, -90), (-10, -90), (-110, 70), (-10, 70), (110, 90), (110, -90), (10, 90)], 4.0, LOCUST)
    return m


def daqin_monastery(ruin=False):
    m = Model("daqin-880" if ruin else "daqin-monastery")
    W, D = 110, 130
    m.add(0, box("ground", W, D, 0.3, (0, 0, 0), GRAVEL if not ruin else shade(GRASS, 0.05)), "grounds")
    m.add(0, walled("wall", W - 4, D - 4, 3.0, 1.2, (("S", 0, 7),), CLAY, TILE), "walls")
    m.add(1, put(small_gate("gate", 8, 4.5, 4.4, VERM if not ruin else WOOD, TILE, "irimoya"), 0, -D / 2 + 2, 0, 0.3), "halls")
    if not ruin:
        tang_hall(m, "church", 24, 13, 6.0, 0, 28, z=0.3, bays=5, roof="hip", roof_h=6.2, plat=1.2)
        cross = [box("cross_v", 0.35, 0.35, 2.6, (0, 28, 0.3 + 1.2 + 6.0 + 6.2 - 0.3), GILT), box("cross_h", 1.6, 0.35, 0.35, (0, 28, 0.3 + 1.2 + 6.0 + 6.2 + 1.3), GILT)]
        m.add(2, join(cross, "cross"))
        for s in (-1, 1):
            tang_hall(m, f"side{s}", 22, 9, 4.2, s * 36, -5, deg=-90 * s, z=0.3, bays=5, plat=0.6, roof="irimoya", roof_h=4.0, bk=False)
        tang_hall(m, "quarters", 40, 9, 4.0, 0, 55, z=0.3, bays=8, plat=0.5, roof="gable", roof_h=3.4, bk=False, shibi=None, trim=None)
        trees(m, "trees", [(-35, -45), (35, -45), (-40, 45), (40, 45)], 3.4, PINE)
    else:
        # the church closed and stripped: walls and columns, the roof fallen in, weeds in the court; the stele still stands
        body = hall_body("church", 24, 13, 6.0, plat=1.2, col=shade(VERM, -0.2), wall=shade(WHITE, -0.12), bays=5)
        m.add(1, move(body, 0, 28, 0.3), "halls")
        m.add(2, seg_prism("roof_half", (-14, 28 - 3.5), (14, 28 - 3.5), 0.3 + 1.2 + 6.0, 7.5, 2.6, shade(TILE, 0.05)), "roofs")
        rubble = [box(f"tiles{i}", 3 + i % 3, 2 + i % 2, 0.6, (-10 + i * 4.5, 36 + (i % 3) * 1.5, 1.5), shade(TILE, 0.08)) for i in range(6)]
        m.add(2, join(rubble, "rubble"))
        for s in (-1, 1):
            b = hall_body(f"side{s}", 22, 9, 4.2, plat=0.6, col=shade(VERM, -0.2), wall=shade(WHITE, -0.12), bays=5)
            m.add(1, put(b, s * 36, -5, -90 * s, 0.3))
            if s > 0:
                m.add(2, put(irimoya("side_roof", 22, 9, 4.0, (0, 0, 0.6 + 4.2), shade(TILE, 0.05), over=2.0), s * 36, -5, -90 * s, 0.3))
        m.add(2, grove("weeds", [(-20, -20, 0.3), (18, -30, 0.3), (-30, 15, 0.3), (25, 50, 0.3), (-15, 55, 0.3), (40, -50, 0.3)], 1.8, GRASS), "weeds")
        trees(m, "trees", [(-35, -45), (40, 45)], 3.6, PINE)
    if ruin:
        # the stele of 781 on its tortoise in the front court
        m.add(1, box("stele_plat", 5, 5, 0.3, (0, -18, 0.3), STONE), "stele")
        m.add(1, stele_tortoise("stele", (0, -18, 0.6), 2.8, 1.0, "#8F8A82"))
    else:
        m.add(1, cylinder("censer", 1.0, 1.6, (0, -18, 0.3), BRONZE, verts=10), "halls")
    return m


# ---------------------------------------------------------------- Ming Xi'an

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


def ming_south_gate():
    m = Model("ming-south-gate")
    W, D = 130, 140
    m.add(0, box("ground", W, D, 0.3, (0, 0, 0), shade(EARTH, 0.04)), "walls")
    m.add(0, box("moat", W, 12, 0.2, (0, -54, 0.3), WATERC))
    m.add(0, box("bridge", 9, 16, 1.2, (52, -54, 0.3), STONE))
    m.add(0, box("road_e", 10, 50, 0.06, (52, -22, 0.3), shade(EARTH, -0.1)))
    m.add(0, box("road_e2", 10, 10, 0.06, (49, -5, 0.3), shade(EARTH, -0.1)))
    m.add(0, box("road_n", 12, 26, 0.06, (0, 57, 0.3), shade(EARTH, -0.1)))
    # the main wall, 12 m high and 18 m thick at the base, battered, faced in grey brick
    wall_h = 12.0
    m.add(0, frustum("wall", W, 18, W, 14, wall_h, (0, 35, 0.3), MBRICK), "walls")
    m.add(0, crenel_line("cren_s", (-W / 2, 28.3), (W / 2, 28.3), wall_h + 0.3))
    m.add(0, box("parapet_n", W, 0.7, 1.0, (0, 41.7, wall_h + 0.3), MBRICK))
    m.add(0, box("walk", W, 13, 0.08, (0, 35, wall_h + 0.3), shade(MBRICK, 0.12)))
    m.add(1, arch_panel("passage_s", 6.0, 8.0, (0, 26.1, 0.3), "S", DARK, pointed=False, depth=0.8), "gates")
    m.add(1, arch_panel("passage_n", 6.0, 8.0, (0, 43.9, 0.3), "N", DARK, pointed=False, depth=0.8))
    for s in (-1, 1):
        verts = [(s * 22, 47, wall_h + 0.3), (s * 22, 53, wall_h + 0.3), (s * 60, 53, 0.3), (s * 60, 47, 0.3), (s * 22, 47, 0.3), (s * 22, 53, 0.3)]
        m.add(0, mesh_from(f"mdao{s}", verts, [(0, 1, 2, 3), (4, 5, 1, 0), (3, 4, 0), (5, 2, 1), (3, 2, 5, 4)], (0, 0, 0), shade(MBRICK, 0.05)))
    # the barbican and its arrow tower
    for s in (-1, 1):
        m.add(0, frustum(f"bwall{s}", 12, 60, 9, 60, wall_h, (s * 39, -3, 0.3), MBRICK))
        m.add(0, crenel_line(f"bcren{s}", (s * 44.6, -33), (s * 44.6, 26), wall_h + 0.3))
    m.add(0, frustum("bwall_s", 90, 12, 90, 9, wall_h, (0, -29, 0.3), MBRICK))
    m.add(1, arch_panel("bgate", 5.5, 7.0, (45.1, -5, 0.3), "E", DARK, pointed=False, depth=0.8))
    jl = [box("jianlou", 54, 15, 9.0, (0, -29, wall_h + 0.3), shade(MBRICK, 0.06))]
    for r in range(4):
        for i in range(12):
            jl.append(box(f"win{r}_{i}", 1.1, 0.4, 1.1, (-24.75 + i * 4.5, -36.6, wall_h + 1.4 + r * 2.0), DARK))
        for i in range(3):
            for s in (-1, 1):
                jl.append(box(f"wins{r}_{i}{s}", 0.4, 1.1, 1.1, (s * 27.1, -33 + i * 4, wall_h + 1.4 + r * 2.0), DARK))
    m.add(1, join(jl, "arrow_tower"))
    m.add(2, irimoya("jianlou_r", 54, 15, 7.0, (0, -29, wall_h + 9.3), TILE, over=2.5, ridge=shade(TILE, -0.25)), "roofs")
    m.add(2, eaved_roof("jianlou_pent", 56, 17, 1.5, (0, -29, wall_h + 7.6), TILE, over=1.6, curve=0.15))
    # the gate tower on the wall: two storeys, three eaves
    lou(m, "zhenglou", 38, 15, 7.0, 6.0, 0, 35, z=wall_h + 0.3, plat=0.6, roof="irimoya", roof_h=8.5, roof_color=TILE, col=MRED, double_top=True, ridge=shade(TILE, -0.3))
    return m


def bell_tower():
    m = Model("bell-tower")
    B = 35.5
    m.add(0, frustum("base", B, B, B - 0.6, B - 0.6, 8.6, (0, 0, 0), MBRICK), "base")
    m.add(0, box("plinth", B + 0.6, B + 0.6, 1.0, (0, 0, 0), STONE))
    for face, (fx, fy) in (("S", (0, -B / 2)), ("N", (0, B / 2)), ("E", (B / 2, 0)), ("W", (-B / 2, 0))):
        m.add(0, arch_panel(f"tunnel{face}", 6.0, 6.2, (fx, fy, 0.0), face, DARK, pointed=False, depth=0.9))
    m.add(0, crenel_line("cren_s", (-B / 2 + 0.6, -B / 2 + 0.6), (B / 2 - 0.6, -B / 2 + 0.6), 8.6, MBRICK, 0.9, 1.0, 0.6))
    m.add(0, crenel_line("cren_n", (-B / 2 + 0.6, B / 2 - 0.6), (B / 2 - 0.6, B / 2 - 0.6), 8.6, MBRICK, 0.9, 1.0, 0.6))
    m.add(0, crenel_line("cren_e", (B / 2 - 0.6, -B / 2 + 0.6), (B / 2 - 0.6, B / 2 - 0.6), 8.6, MBRICK, 0.9, 1.0, 0.6))
    m.add(0, crenel_line("cren_w", (-B / 2 + 0.6, -B / 2 + 0.6), (-B / 2 + 0.6, B / 2 - 0.6), 8.6, MBRICK, 0.9, 1.0, 0.6))
    top = lou(m, "tower", 21, 21, 7.0, 6.0, 0, 0, z=8.6, plat=0.9, roof="hip", roof_h=8.5, roof_color=MGREEN, col=MRED, double_top=True,
              ridge=shade(MGREEN, -0.25), bays=5, plat_color=STONE)
    m.add(2, cylinder("finial_base", 0.9, 0.8, (0, 0, top - 0.5), GILT, verts=10), "roofs")
    m.add(2, dome("finial", 0.8, (0, 0, top + 0.3), GILT, squash=1.6, segments=12, rings=8))
    m.add(2, cylinder("finial_spike", 0.15, 1.6, (0, 0, top + 1.4), GILT, verts=6))
    return m


def drum_tower():
    m = Model("drum-tower")
    W, D = 52.6, 38.0
    m.add(0, frustum("base", W, D, W - 0.6, D - 0.6, 7.7, (0, 0, 0), MBRICK), "base")
    m.add(0, box("plinth", W + 0.6, D + 0.6, 1.0, (0, 0, 0), STONE))
    m.add(0, arch_panel("tunnel_s", 6.0, 6.0, (0, -D / 2, 0.0), "S", DARK, pointed=False, depth=0.9))
    m.add(0, arch_panel("tunnel_n", 6.0, 6.0, (0, D / 2, 0.0), "N", DARK, pointed=False, depth=0.9))
    for nm, a, b in (("s", (-W / 2 + 0.6, -D / 2 + 0.6), (W / 2 - 0.6, -D / 2 + 0.6)), ("n", (-W / 2 + 0.6, D / 2 - 0.6), (W / 2 - 0.6, D / 2 - 0.6)),
                     ("e", (W / 2 - 0.6, -D / 2 + 0.6), (W / 2 - 0.6, D / 2 - 0.6)), ("w", (-W / 2 + 0.6, -D / 2 + 0.6), (-W / 2 + 0.6, D / 2 - 0.6))):
        m.add(0, crenel_line("cren_" + nm, a, b, 7.7, MBRICK, 0.9, 1.0, 0.6))
    lou(m, "tower", 38, 22, 7.0, 5.5, 0, 0, z=7.7, plat=0.9, roof="irimoya", roof_h=8.0, roof_color=TILE, col=MRED, double_top=True,
        ridge=shade(TILE, -0.3), bays=7, plat_color=STONE, shibi=MGREEN)
    trim = [box(f"trim{s}", 44, 0.6, 0.4, (0, s * 12.8, 7.7 + 0.9 + 7.0 + 0.2), MGREEN) for s in (-1, 1)]
    m.add(2, join(trim, "trim"), "roofs")
    return m


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


def great_mosque():
    """Built with its entrance on -Y (east once turned) and the prayer hall at +Y (the west end, facing Mecca)."""
    m = Model("great-mosque")
    W, D = 50, 250
    m.add(0, box("ground", W, D, 0.3, (0, 0, 0), GRAVEL), "grounds")
    m.add(0, walled("wall", W - 2, D - 2, 3.6, 1.0, (("S", 0, 6),), shade(MBRICK, 0.15), MGREEN), "walls")
    for i, y in enumerate((-70, -20, 40)):
        m.add(0, wall_line(f"cross{i}a", [(-24, y), (-6, y)], 3.4, 0.9, shade(MBRICK, 0.15), MGREEN))
        m.add(0, wall_line(f"cross{i}b", [(6, y), (24, y)], 3.4, 0.9, shade(MBRICK, 0.15), MGREEN))
        m.add(1, put(small_gate(f"cgate{i}", 10, 4.0, 4.6, MRED, MGREEN, "irimoya"), 0, y), "courts")
    # first court: the wooden archway; second: the stone archway and stele pavilions
    m.add(1, move(paifang("wood_arch", 14, 9.0), 0, -100, 0.3))
    m.add(1, move(paifang("stone_arch", 12, 7.0, "#B9B2A4", "#8E8A84"), 0, -48, 0.3))
    for s in (-1, 1):
        tang_hall(m, f"stelepav{s}", 5, 5, 3.2, s * 13, -40, z=0.3, bays=1, plat=0.5, roof="hip", roof_h=2.6, bk=False, shibi=None, trim=None, col=MRED, roof_color=MGREEN)
        tang_hall(m, f"side3{s}", 22, 7, 3.8, s * 19, 10, deg=-90 * s, z=0.3, bays=5, plat=0.5, roof="irimoya", roof_h=3.4, bk=False, shibi=None, trim=None, col=MRED, roof_color=TILE)
        tang_hall(m, f"side4{s}", 18, 7, 3.8, s * 19, 62, deg=-90 * s, z=0.3, bays=4, plat=0.5, roof="irimoya", roof_h=3.4, bk=False, shibi=None, trim=None, col=MRED, roof_color=TILE)
    # third court: the octagonal Shengxin tower, from which the call to prayer was given
    m.add(1, move(octagon_pavilion("shengxin", 4.2, 5.0, 4.0), 0, 10, 0.3), "courts")
    # fourth court: the Phoenix pavilion, the moon terrace and the prayer hall
    m.add(1, move(octagon_pavilion("phoenix", 3.2, 4.0, 3.0), 0, 58, 0.3))
    for s in (-1, 1):
        tang_hall(m, f"wing{s}", 7, 5, 3.4, s * 7.5, 58, z=0.3, bays=2, plat=1.0, roof="irimoya", roof_h=2.8, bk=False, shibi=None, trim=None, col=MRED, roof_color=MGREEN)
    m.add(0, terrace("moon", 34, 14, 1.4, (0, 82, 0.3), STONE, shade(STONE, -0.06), batter=0.0, rail=True, rail_color=WHITE), "prayer")
    m.add(0, terrace("hall_t", 36, 36, 1.4, (0, 106, 0.3), STONE, shade(STONE, -0.06), batter=0.0))
    tang_hall(m, "prayer_hall", 32, 32, 7.0, 0, 106, z=1.7, bays=7, plat=0.3, roof="irimoya", roof_h=9.0, over=3.5, bk=True, shibi=MGREEN, trim=None, col=MRED, roof_color=GLAZE_TEAL, stairs=False)
    trees(m, "trees", [(-16, -110), (16, -110), (-16, -80), (16, -82), (-14, -8), (14, 28), (-14, 30), (16, -6)], 2.8, "#5E7A4C")
    return m


def qin_palace():
    m = Model("qin-palace")
    W, D = 500, 600
    m.add(0, box("ground", W, D, 0.3, (0, 0, 0), GRAVEL), "grounds")
    m.add(0, walled("outer", W - 8, D - 8, 7.0, 3.0, (("S", 0, 14), ("N", 0, 10), ("E", 0, 10), ("W", 0, 10)), shade(EARTH, -0.02), TILE), "walls")
    # the inner city: a moat and a brick wall round the palace proper
    IW, ID = 300, 380
    moat = [box("moat_s", IW + 40, 12, 0.2, (0, -ID / 2 - 14, 0.3), WATERC), box("moat_n", IW + 40, 12, 0.2, (0, ID / 2 + 14, 0.3), WATERC),
            box("moat_w", 12, ID + 16, 0.2, (-IW / 2 - 14, 0, 0.3), WATERC), box("moat_e", 12, ID + 16, 0.2, (IW / 2 + 14, 0, 0.3), WATERC)]
    m.add(0, join(moat, "moat"))
    m.add(0, box("bridge", 12, 16, 1.0, (0, -ID / 2 - 14, 0.3), STONE))
    m.add(0, walled("inner", IW, ID, 8.0, 3.0, (("S", 0, 16), ("N", 0, 10)), MBRICK, MGREEN), "walls")
    body, roof = gate_parts("duanli", 34, 12, 7.0, 5.0, roof_h=6.5, bays=5, top="irimoya", col=MRED, wall=shade(MRED, 0.35))
    m.add(1, move(body, 0, -ID / 2, 0.3), "halls")
    m.add(2, move(roof, 0, -ID / 2, 0.3), "roofs")
    body, roof = gate_parts("outer_gate", 26, 10, 6.0, 4.5, roof_h=5.5, bays=5, top="irimoya", col=MRED, wall=shade(MRED, 0.35))
    m.add(1, move(body, 0, -D / 2 + 4, 0.3))
    m.add(2, move(roof, 0, -D / 2 + 4, 0.3))
    # three halls on an I-shaped terrace, the residence behind
    m.add(0, terrace("gong_t", 90, 160, 2.6, (0, -10, 0.3), STONE, shade(STONE, -0.06), batter=0.02, rail=True, rail_color=WHITE), "terraces")
    tang_hall(m, "chengyun", 50, 24, 9.0, 0, -60, z=2.9, bays=9, roof="hip", roof_h=10.0, plat=0.4, shibi=MGREEN, trim=None, col=MRED, roof_color=MGREEN, stairs=False, bk=True)
    tang_hall(m, "yuandian", 26, 20, 7.0, 0, -10, z=2.9, bays=5, roof="hip", roof_h=7.0, plat=0.4, shibi=MGREEN, trim=None, col=MRED, roof_color=MGREEN, stairs=False, bk=False)
    tang_hall(m, "cundian", 44, 22, 8.0, 0, 42, z=2.9, bays=9, roof="irimoya", roof_h=8.5, plat=0.4, shibi=MGREEN, trim=None, col=MRED, roof_color=MGREEN, stairs=False, bk=True)
    m.add(0, stair("gst", 14, 2.6, 6, 6, (0, -90 - 3, 0.3), "S", STONE))
    for s in (-1, 1):
        for i in range(3):
            tang_hall(m, f"wu{s}{i}", 40, 10, 5.0, s * 112, -120 + i * 70, deg=-90 * s, z=0.3, bays=8, plat=0.6, roof="irimoya", roof_h=4.5, bk=False, shibi=None, trim=None, col=MRED)
    for i in range(2):
        tang_hall(m, f"gong{i}", 60, 16, 6.0, 0, 110 + i * 40, z=0.3, bays=11, plat=0.8, roof="irimoya", roof_h=6.0, bk=False, shibi=None, trim=None, col=MRED, roof_color=MGREEN)
    # gardens and offices in the outer precinct
    m.add(0, blob("pond", 40, 26, 0.25, (-190, 230, 0.3), WATERC, 0.4), "grounds")
    for i, (x, y) in enumerate(((180, 200), (180, -200), (-180, -200), (190, 20))):
        m.add(1, yard_houses(f"office{i}", x, y, 50, 40, 4.5, CLAY, TILE, i))
    trees(m, "trees", [(-200, 160), (-150, 250), (-220, 100), (200, 260), (-200, -100), (210, -110), (-100, -260), (100, -260)], 5.0, PINE)
    return m


BUILDERS = {
    "changan/taiji-palace": taiji_palace,
    "changan/chengtianmen": chengtianmen,
    "changan/zhuquemen": zhuquemen,
    "changan/danfengmen": danfengmen,
    "changan/hanyuan-hall": hanyuan_hall,
    "changan/hanyuan-hall-ruin": hanyuan_ruin,
    "changan/east-market": lambda: market(False),
    "changan/west-market": lambda: market(True),
    "changan/xingqing-palace": xingqing_palace,
    "changan/greater-goose": lambda: greater_goose("750"),
    "changan/greater-goose-652": lambda: greater_goose("652"),
    "changan/greater-goose-1400": lambda: greater_goose("1400"),
    "changan/lesser-goose": lesser_goose,
    "changan/daxingshan-si": daxingshan_si,
    "changan/xuandu-guan": xuandu_guan,
    "changan/ximing-si": ximing_si,
    "changan/daqin-monastery": lambda: daqin_monastery(False),
    "changan/daqin-880": lambda: daqin_monastery(True),
    "changan/guozijian": guozijian,
    "changan/ming-south-gate": ming_south_gate,
    "changan/bell-tower": bell_tower,
    "changan/drum-tower": drum_tower,
    "changan/great-mosque": great_mosque,
    "changan/qin-palace": qin_palace,
}
