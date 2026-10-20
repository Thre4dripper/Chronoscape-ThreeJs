"""Nara / Heijō-kyō landmark miniatures.

The hall, gate, corridor and roof helpers are copied from the Kyoto module (kyoto.py) and
extended with gilt ridge-end fins (shibi); the pagodas, octagonal halls, log storehouse
and curved gable are Nara's own."""
import math
from chronokit import Model, box, cylinder, dome, join, shade, mesh_from
from worldkit import *

VERM = "#B8452E"          # vermilion (ni-nuri) of state halls and Nara temples
WHITE = "#EEE7D8"         # plastered wall panels
BARK = "#6E4B3A"          # cypress-bark (hiwada) roofs
TILE = TILE_GREY
GLAZE = "#3F8A62"         # green lattice windows and glazed details
STONE = "#BDB5A6"
GRAVEL = "#E2DACA"
EARTH = "#C4B28D"
CLAY = "#CDBB98"          # earth walls (tsuiji)
MOSS = "#8E9B6A"
GRASS = "#9AA56E"
WOOD = "#6A5442"          # unpainted, weathered timber
DARKW = "#3A2E26"
PINE = "#557048"
CEDAR = "#4A6440"
WILLOW = "#93A660"
FIELD = "#A9A877"
EDO_COL = "#7A4A36"       # the dark red-brown columns of the 1709 hall


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


def jpagoda(name, w, storeys, total_h, wall=WOOD, roof=TILE, trim=None, spire_frac=0.24, taper=0.91, over=0.6):
    """A Japanese pagoda: short storeys under very wide, upturned eaves, bracket bands, balconies, a tall bronze finial (sōrin)."""
    trim = trim or shade(wall, -0.15)
    base = w * 0.18
    parts = [box(name + "_base", w * 1.5, w * 1.5, base, (0, 0, 0), STONE)]
    sh = (total_h * (1 - spire_frac) - base) / storeys
    z, ww = base, w
    for i in range(storeys):
        bh = sh * 0.56
        if i:
            parts.append(box(f"{name}_bal{i}", ww * 1.18, ww * 1.18, 0.35, (0, 0, z), trim))
        parts.append(box(f"{name}_s{i}", ww, ww, bh, (0, 0, z), wall))
        parts.append(box(f"{name}_dr{i}", ww * 0.3, ww * 1.01, bh * 0.6, (0, 0, z + bh * 0.1), DARKW))
        parts.append(box(f"{name}_dr2{i}", ww * 1.01, ww * 0.3, bh * 0.6, (0, 0, z + bh * 0.1), DARKW))
        parts.append(box(f"{name}_br{i}", ww * 1.25, ww * 1.25, sh * 0.1, (0, 0, z + bh), trim))
        parts.append(eaved_roof(f"{name}_r{i}", ww * 1.25, ww * 1.25, sh * 0.32, (0, 0, z + bh + sh * 0.1), roof, over=ww * over, curve=0.3))
        z += sh
        ww *= taper
    sp = total_h - z
    parts.append(box(name + "_roban", ww * 0.5, ww * 0.5, sp * 0.08, (0, 0, z - sh * 0.08), roof))
    parts.append(cylinder(name + "_spire", max(0.15, w * 0.03), sp * 0.95, (0, 0, z), BRONZE, verts=8))
    for k in range(9):
        parts.append(cylinder(f"{name}_ring{k}", max(0.5, w * 0.1) * (1 - k * 0.04), 0.22, (0, 0, z + sp * (0.12 + k * 0.065)), BRONZE, verts=10))
    parts.append(box(name + "_suien", max(0.8, w * 0.14), 0.15, sp * 0.1, (0, 0, z + sp * 0.75), BRONZE))
    parts.append(dome(name + "_jewel", max(0.3, w * 0.04), (0, 0, z + sp * 0.95), GILT, segments=10, rings=6))
    return join(parts, name)



# ---------------------------------------------------------------- Nara's own parts

def npagoda(name, w, storeys, total_h, mokoshi=False, roof=TILE, col=VERM, wall=WHITE, spire_frac=0.26, taper=0.9, over=0.46):
    """A Nara pagoda: white-walled storeys with vermilion posts and bracket bands under very wide eaves,
    a tall bronze finial; mokoshi=True adds a skirt roof to every storey (Yakushi-ji)."""
    trim = shade(col, -0.1)
    base = max(1.2, w * 0.14)
    parts = [box(name + "_base", w * 1.55, w * 1.55, base, (0, 0, 0), STONE)]
    sh = (total_h * (1 - spire_frac) - base) / storeys
    z, ww = base, w
    for i in range(storeys):
        bh = sh * (0.62 if mokoshi else 0.6)
        if i:
            parts.append(box(f"{name}_bal{i}", ww * 1.16, ww * 1.16, 0.4, (0, 0, z), trim))
        parts.append(box(f"{name}_s{i}", ww, ww, bh, (0, 0, z), wall))
        for sx in (-1, 1):
            for sy in (-1, 1):
                parts.append(box(f"{name}_p{i}{sx}{sy}", ww * 0.09, ww * 0.09, bh, (sx * ww * 0.455, sy * ww * 0.455, z), col))
        parts.append(box(f"{name}_dr{i}", ww * 0.3, ww * 1.01, bh * 0.55, (0, 0, z + bh * 0.08), DARKW))
        parts.append(box(f"{name}_dr2{i}", ww * 1.01, ww * 0.3, bh * 0.55, (0, 0, z + bh * 0.08), DARKW))
        if mokoshi:
            mw = ww * 1.3
            parts.append(box(f"{name}_mw{i}", mw, mw, bh * 0.42, (0, 0, z), wall))
            parts.append(box(f"{name}_ml{i}", mw * 1.01, mw * 0.3, bh * 0.22, (0, 0, z + bh * 0.12), GLAZE))
            parts.append(box(f"{name}_ml2{i}", mw * 0.3, mw * 1.01, bh * 0.22, (0, 0, z + bh * 0.12), GLAZE))
            parts.append(eaved_roof(f"{name}_mr{i}", mw, mw, sh * 0.16, (0, 0, z + bh * 0.42), roof, over=ww * 0.28, curve=0.2))
        parts.append(box(f"{name}_br{i}", ww * 1.22, ww * 1.22, sh * 0.1, (0, 0, z + bh), trim))
        parts.append(eaved_roof(f"{name}_r{i}", ww * 1.22, ww * 1.22, sh * 0.3, (0, 0, z + bh + sh * 0.1), roof, over=ww * over, curve=0.3))
        z += sh
        ww *= taper
    sp = total_h - z
    parts.append(box(name + "_roban", ww * 0.5, ww * 0.5, sp * 0.06, (0, 0, z - sh * 0.06), roof))
    parts.append(cylinder(name + "_spire", max(0.15, w * 0.03), sp * 0.95, (0, 0, z), BRONZE, verts=8))
    for k in range(9):
        parts.append(cylinder(f"{name}_ring{k}", max(0.5, w * 0.1) * (1 - k * 0.04), 0.25, (0, 0, z + sp * (0.12 + k * 0.065)), BRONZE, verts=10))
    parts.append(box(name + "_suien", max(0.8, w * 0.14), 0.15, sp * 0.1, (0, 0, z + sp * 0.76), BRONZE))
    parts.append(dome(name + "_jewel", max(0.3, w * 0.045), (0, 0, z + sp * 0.95), GILT, segments=10, rings=6))
    return join(parts, name)


def octagon_hall(name, r, h, roof_h, plat=1.2, col=VERM, wall=WHITE, roof=TILE):
    """An octagonal hall (endō): octagonal stone platform, white walls with red posts, a pointed octagonal roof with a jewel."""
    def octo(rr):
        return [(rr * math.cos(math.pi / 8 + k * math.pi / 4), rr * math.sin(math.pi / 8 + k * math.pi / 4)) for k in range(8)]
    parts = [prism(name + "_pl", octo(r * 1.35), plat, (0, 0, 0), STONE)]
    parts.append(stair(name + "_st", r * 0.6, plat, 2.4, 4, (0, -r * 1.3, 0), "S", STONE))
    parts.append(prism(name + "_w", octo(r), h, (0, 0, plat), wall))
    for k, (px, py) in enumerate(octo(r)):
        parts.append(box(f"{name}_p{k}", 0.6, 0.6, h, (px, py, plat), col))
    parts.append(prism(name + "_dr", octo(r * 0.55), h * 0.6, (0, -r * 0.5, plat), DARKW))
    parts.append(prism(name + "_bm", octo(r * 1.04), h * 0.1, (0, 0, plat + h * 0.9), col))
    rf = cylinder(name + "_rf", r * 1.75, roof_h, (0, 0, plat + h), roof, verts=8, r_top=r * 0.12)
    rf = rot(rf, 22.5)
    parts.append(rf)
    parts.append(cylinder(name + "_ped", r * 0.16, roof_h * 0.12, (0, 0, plat + h + roof_h), BRONZE, verts=8))
    parts.append(dome(name + "_jw", r * 0.14, (0, 0, plat + h + roof_h * 1.16), GILT, segments=10, rings=6))
    return join(parts, name)


def karahafu(name, w, d, h, loc=(0, 0, 0), color=TILE, n=16):
    """A cusped, curved gable (karahafu): a roof surface whose ridge rises in a bell curve, extruded front-back (d along Y)."""
    x, y, z = loc
    prof = []
    for i in range(n + 1):
        t = -1 + 2 * i / n
        bell = math.exp(-(t * 1.7) ** 2)
        lift = 0.12 * max(0.0, abs(t) - 0.75) / 0.25
        prof.append((t * w / 2, h * bell + h * lift))
    verts = []
    for (px, pz) in prof:
        verts += [(px, -d / 2, pz), (px, d / 2, pz), (px, -d / 2, pz - 0.7), (px, d / 2, pz - 0.7)]
    faces = []
    for i in range(n):
        a, b = 4 * i, 4 * (i + 1)
        faces += [(a, b, b + 1, a + 1), (a + 2, a + 3, b + 3, b + 2), (a, a + 2, b + 2, b), (a + 1, b + 1, b + 3, a + 3)]
    faces += [(0, 1, 3, 2), (4 * n, 4 * n + 2, 4 * n + 3, 4 * n + 1)]
    roofo = mesh_from(name + "_r", verts, faces, (x, y, z), color)
    gable = mesh_from(name + "_g", [(px, -d / 2 + 0.3, pz - 0.7) for px, pz in prof] + [(w / 2, -d / 2 + 0.3, 0), (-w / 2, -d / 2 + 0.3, 0)],
                      [tuple(range(n + 3))], (x, y, z), shade(WOOD, 0.15))
    return join([roofo, gable], name)


def stone_lantern(name, loc, s=1.0, color=STONE):
    x, y, z = loc
    parts = [box(name + "_b", 0.9 * s, 0.9 * s, 0.3 * s, (x, y, z), color),
             cylinder(name + "_p", 0.18 * s, 1.0 * s, (x, y, z + 0.3 * s), color, verts=6),
             box(name + "_f", 0.6 * s, 0.6 * s, 0.5 * s, (x, y, z + 1.3 * s), "#EDE3C8"),
             cylinder(name + "_c", 0.6 * s, 0.35 * s, (x, y, z + 1.8 * s), color, verts=6, r_top=0.1 * s)]
    return join(parts, name)


def lantern_row(name, a, b, n, s=1.0):
    (ax, ay), (bx, by) = a, b
    return join([stone_lantern(f"{name}{i}", (ax + (bx - ax) * i / max(1, n - 1), ay + (by - ay) * i / max(1, n - 1), 0), s) for i in range(n)], name)


def log_store(name, L, W, H, lift, loc=(0, 0, 0), roof=TILE, n_pillars=10, rooms=True):
    """An azekura storehouse on pillars: log-coursed end rooms, a boarded middle room, a low hipped roof. Long axis X, doors on -Y."""
    x, y, z = loc
    parts = []
    for i in range(n_pillars):
        for j in range(4):
            px = -L / 2 + 0.6 + (L - 1.2) * i / (n_pillars - 1)
            py = -W / 2 + 0.6 + (W - 1.2) * j / 3
            parts.append(cylinder(f"{name}_pi{i}{j}", 0.35, lift, (x + px, y + py, z), WOOD, verts=8))
    parts.append(box(name + "_fl", L + 0.4, W + 0.4, 0.5, (x, y, z + lift), shade(WOOD, -0.1)))
    zb = z + lift + 0.5
    room = L / 3 if rooms else L
    nb = max(6, int(H / 0.5))
    for k, cx in enumerate((-room, 0, room) if rooms else (0,)):
        if rooms and k == 1:
            parts.append(box(f"{name}_mid", room, W, H, (x + cx, y, zb), shade(WOOD, 0.08)))
            continue
        for b in range(nb):
            inset = 0.0 if b % 2 == 0 else 0.18
            parts.append(box(f"{name}_lg{k}_{b}", room - inset, W - inset, H / nb, (x + cx, y, zb + b * H / nb), shade(WOOD, 0.05 if b % 2 else -0.05)))
        parts.append(box(f"{name}_door{k}", room * 0.22, 0.2, H * 0.55, (x + cx, y - W / 2 - 0.05, zb + H * 0.1), DARKW))
    body = join(parts, name + "_body")
    rf = hip(name + "_rf", L, W, max(2.0, W * 0.5), (x, y, zb + H), roof, over=max(1.2, W * 0.2))
    return body, rf


def machiya_rows(name, x0, y0, x1, y1, lot=6.0, depth=11.0, h=5.5, roof=TILE, gap=6.0, wall=CLAY):
    """Rows of narrow town houses facing streets that run along X, back to back in pairs."""
    parts = []
    y = y0
    r = 0
    while y + 2 * depth <= y1 + 0.01:
        for side, yy in ((0, y + depth / 2), (1, y + depth * 1.5)):
            x = x0
            k = 0
            while x + lot <= x1 + 0.01:
                hh = h * (0.85 + 0.3 * (((k * 7 + r * 3 + side) % 5) / 5))
                parts.append(box(f"{name}_h{r}{side}{k}", lot - 0.4, depth - 0.6, hh, (x + lot / 2, yy, 0), shade(wall, 0.06 * ((k + r) % 3 - 1))))
                parts.append(seg_prism(f"{name}_r{r}{side}{k}", (x + 0.0, yy), (x + lot, yy), hh, depth + 0.6, 2.2, shade(roof, 0.05 * ((k + side) % 3 - 1))))
                if side == 0:
                    parts.append(box(f"{name}_f{r}{k}", lot * 0.7, 0.2, hh * 0.5, (x + lot / 2, yy - depth / 2 + 0.2, 0), DARKW))
                x += lot
                k += 1
        y += 2 * depth + gap
        r += 1
    return join(parts, name)


def court(m, name, cx, cy, W, D, hall, gate=None, sb=1, sr=2, kairo_w=6.0, kairo_roof=TILE, col=VERM):
    """A cloistered temple court: a roofed corridor round W x D, the main hall (dict for H) inside, a gate (dict for G) on the south side."""
    m.add(sb, gallery(f"{name}_kairo", rect_pts(W, D, cx, cy), w=kairo_w, h=3.8, col=col, roof=kairo_roof, closed=True, wall=WHITE), "halls")
    hw = dict(hall)
    hn = hw.pop("w"), hw.pop("d"), hw.pop("h")
    hy = hw.pop("y", cy + D * 0.12)
    H(m, f"{name}_hall", *hn, cx, hy, sb=sb, sr=sr, **hw)
    if gate:
        g = dict(gate)
        gn = g.pop("w"), g.pop("d"), g.pop("h1"), g.pop("h2")
        G(m, f"{name}_gate", *gn, cx, cy - D / 2, sb=sb, sr=sr, **g)


def trees(m, name, pts, r=4.5, color=PINE, stage=2):
    m.add(stage, grove(name, [(x, y, 0) for x, y in pts], r, color))


# ---------------------------------------------------------------- the palace

def daigokuden(early=True):
    """The First Daigokuden-in: the hall on its terrace, the cloistered court, the south gate, the seven banner poles."""
    m = Model("daigokuden" if early else "daigokuden-752")
    W, D = 180, 260
    m.add(0, box("ground", W, D, 0.3, (0, 0, 0), GRAVEL), "grounds")
    m.add(0, box("terrace", W - 14, 100, 2.4, (0, 70, 0.3), shade(GRAVEL, -0.06)))
    m.add(0, box("terrace_face", W - 14, 1.0, 2.9, (0, 20, 0.3), STONE))
    for x in (-36, 0, 36):
        m.add(0, stair(f"tst{x}", 9, 2.4, 6, 5, (x, 17, 0.3), "S", STONE))
    m.add(1, gallery("kairo", rect_pts(W - 6, D - 6), w=6, h=4.2, closed=True, wall=WHITE), "halls")
    m.add(1, gallery("crossk", [(-W / 2 + 3, 20), (-40, 20)], w=5, h=3.6), "halls")
    m.add(1, gallery("crossk2", [(40, 20), (W / 2 - 3, 20)], w=5, h=3.6), "halls")
    G(m, "minamimon", 22, 9, 6.5, 4.5, 0, -D / 2 + 3, roof_h=5.5, bays=5, shibi=GILT)
    for s in (-1, 1):
        for i, y in enumerate((-25, -85)):
            H(m, f"chodo{s}{i}", 40, 12, 5.5, s * 58, y, deg=-90 * s, plat=0.8, roof="irimoya", roof_h=6.5, bays=9)
    if early:
        m.add(0, box("podium", 54, 30, 1.6, (0, 82, 2.7), STONE))
        m.add(0, stair("podium_st", 14, 1.6, 4, 4, (0, 65, 2.7), "S", STONE))
        H(m, "daigokuden", 44, 20, 9.5, 0, 82, z=4.3, plat=0, roof="irimoya", roof_h=12.5, bays=9, shibi=GILT, over=6.5)
        poles = []
        for i in range(7):
            x = -24 + i * 8
            poles.append(cylinder(f"pole{i}", 0.3, 12, (x, -10, 0.3), VERM if i != 3 else GILT, verts=6))
            poles.append(box(f"flag{i}", 1.6, 0.15, 4.5, (x + 0.9, -10, 6.5), ("#3E5C9A", "#B8452E", "#EEE7D8", "#D4AE55", "#2E241C", "#B8452E", "#3F8A62")[i]))
        m.add(2, join(poles, "banners"), "roofs")
    else:
        m.add(0, box("podium", 54, 30, 1.6, (0, 82, 2.7), shade(STONE, -0.08)))
        stones = [cylinder(f"fs{i}{j}", 0.9, 0.5, (-20 + i * 5, 82 - 7.5 + j * 5, 4.3), STONE, verts=8) for i in range(9) for j in range(4)]
        m.add(1, join(stones, "found_stones"), "halls")
        heaps = [box(f"timber{i}", 14, 1.2, 1.2, (-15 + i * 10, 55, 2.7 + (i % 2) * 1.2), WOOD) for i in range(4)]
        m.add(1, join(heaps, "timber"))
        H(m, "kari", 20, 10, 4.0, -45, 82, z=2.7, plat=0.4, roof="gable", roof_h=3.5, bays=5, col=WOOD, roof_color=BARK)
        m.add(2, grove("weeds", [(-60, -60, 0), (55, -90, 0), (60, 60, 2.7), (-65, 110, 2.7)], 2.2, GRASS))
    trees(m, "trees", [(-80, -120), (80, -120), (-80, 118), (80, 118)], 3.5)
    return m


def chodo_in():
    """The east zone after 745: the Second Daigokuden on its podium and the court of the assembly halls below."""
    m = Model("chodo-in")
    W, D = 180, 300
    m.add(0, box("ground", W, D, 0.3, (0, 0, 0), GRAVEL), "grounds")
    # the Daigokuden court, north
    m.add(1, gallery("kairo_n", rect_pts(W - 6, 84, 0, 105), w=6, h=4.0, closed=True, wall=WHITE), "halls")
    m.add(0, box("podium", 50, 26, 2.2, (0, 112, 0.3), STONE))
    m.add(0, stair("podium_st", 12, 2.2, 5, 5, (0, 96.5, 0.3), "S", STONE))
    H(m, "daigokuden2", 40, 18, 9.0, 0, 112, z=2.5, plat=0, roof="hip", roof_h=11, bays=9, shibi=GILT, over=6)
    G(m, "daigokuden_mon", 18, 8, 5.5, 4.0, 0, 63, roof_h=5, bays=5)
    # the Chōdō-in, south
    m.add(1, gallery("kairo_s", rect_pts(W - 6, 206, 0, -44), w=6, h=4.0, closed=True, wall=WHITE), "halls")
    for s in (-1, 1):
        for i, y in enumerate((35, -5, -55, -105)):
            H(m, f"chodo{s}{i}", 34, 11, 5.0, s * 56, y, deg=-90 * s, plat=0.8, roof="irimoya", roof_h=6, bays=8)
    G(m, "chodomon", 20, 9, 6.0, 4.5, 0, -147, roof_h=5.5, bays=5, shibi=GILT)
    return m


def suzakumon():
    m = Model("suzakumon")
    m.add(0, box("ground", 40, 20, 0.3, (0, 0, 0), GRAVEL), "grounds")
    m.add(0, wall_line("wall_w", [(-20, 1.5), (-14.5, 1.5)], 5.0, 2.4))
    m.add(0, wall_line("wall_e", [(14.5, 1.5), (20, 1.5)], 5.0, 2.4))
    G(m, "gate", 25, 10, 7.5, 5.5, roof_h=7.0, bays=5, top="irimoya", shibi=GILT)
    return m


def suzaku_oji():
    """A stretch of the avenue: gravel road, ditches, willows, the earth walls of the wards and a ward gate on each side."""
    m = Model("suzaku-oji")
    W, D = 96, 200
    m.add(0, box("ground", W, D, 0.3, (0, 0, 0), EARTH), "grounds")
    m.add(0, box("road", 66, D, 0.12, (0, 0, 0.3), GRAVEL))
    for s in (-1, 1):
        m.add(0, box(f"ditch{s}", 2.4, D, 0.15, (s * 34.5, 0, 0.3), WATER))
        m.add(0, box(f"verge{s}", 9, D, 0.1, (s * 40.5, 0, 0.3), GRASS))
        m.add(1, wall_line(f"ward_wall{s}a", [(s * 46, -D / 2), (s * 46, -8)], 3.6, 1.6), "walls")
        m.add(1, wall_line(f"ward_wall{s}b", [(s * 46, 8), (s * 46, D / 2)], 3.6, 1.6))
        m.add(1, put(small_gate(f"bomon{s}", 8, 4, 4.8, VERM, TILE, "irimoya"), s * 46, 0, 90))
        m.add(2, grove(f"willows{s}", [(s * 37.5, -D / 2 + 8 + i * 14, 0.3) for i in range(14) if abs(-D / 2 + 8 + i * 14) > 9], 2.6, WILLOW), "trees")
    return m


def rajomon():
    m = Model("rajomon")
    m.add(0, box("ground", 40, 16, 0.3, (0, 0, 0), GRAVEL), "grounds")
    m.add(0, wall_line("wall_w", [(-20, 0.5), (-18, 0.5)], 5.0, 2.4))
    m.add(0, wall_line("wall_e", [(18, 0.5), (20, 0.5)], 5.0, 2.4))
    G(m, "gate", 35, 10, 8.0, 6.0, roof_h=7.5, bays=7, top="irimoya", shibi=GILT)
    return m


# ---------------------------------------------------------------- Tōdai-ji

def daibutsuden(edo=False):
    """The Hall of the Great Buddha in its cloister: eleven bays (752) or seven with a cusped front gable (1709)."""
    m = Model("daibutsuden-1709" if edo else "daibutsuden")
    W, D = 200, 200
    m.add(0, box("ground", W, D, 0.3, (0, 0, 0), GRAVEL), "grounds")
    m.add(1, gallery("kairo", rect_pts(W - 8, D - 8), w=7, h=4.6, closed=True, wall=WHITE, col=EDO_COL if edo else VERM), "halls")
    G(m, "chumon", 30 if not edo else 26, 12, 7.5, 6.0, 0, -D / 2 + 4, roof_h=7.5, bays=5, shibi=None if edo else GILT, col=EDO_COL if edo else VERM)
    m.add(0, box("path", 10, 70, 0.1, (0, -55, 0.3), STONE))
    lantern = [cylinder("lt_base", 1.2, 1.2, (0, -40, 0.3), STONE, verts=8), cylinder("lt_post", 0.35, 1.8, (0, -40, 1.5), BRONZE, verts=8),
               cylinder("lt_fire", 0.9, 1.4, (0, -40, 3.3), BRONZE, verts=8), cylinder("lt_cap", 1.3, 0.8, (0, -40, 4.7), BRONZE, verts=8, r_top=0.2)]
    m.add(1, join(lantern, "octagonal_lantern"))
    if not edo:
        m.add(0, box("platform", 94, 58, 2.0, (0, 30, 0.3), STONE))
        m.add(0, stair("pst", 24, 2.0, 5, 5, (0, -1.5, 0.3), "S", STONE))
        H(m, "hall", 86, 50, 28.0, 0, 30, z=2.3, plat=0, roof="hip", roof_h=17.0, bays=11, mokoshi=True, shibi=GILT, over=9.0)
    else:
        m.add(0, box("platform", 64, 57, 2.0, (0, 30, 0.3), STONE))
        m.add(0, stair("pst", 18, 2.0, 5, 5, (0, -1.0, 0.3), "S", STONE))
        H(m, "hall", 57, 50, 26.0, 0, 30, z=2.3, plat=0, roof="irimoya", roof_h=21.0, bays=7, mokoshi=True, shibi=GILT, over=9.0, col=EDO_COL)
        mk_z = 2.3 + 26.0 * 0.42 + 3.0
        m.add(2, karahafu("karahafu", 20, 9, 5.5, (0, 30 - 25 - 7.5, mk_z), TILE), "roofs")
        m.add(1, box("kangen_mado", 9, 0.4, 4.0, (0, 30 - 25 - 0.3, mk_z + 2.0), DARKW))
    trees(m, "trees", [(-60, -80), (60, -80), (-85, 40), (85, 40), (-80, 85), (80, 85)], 4.0)
    return m


def todaiji_pagoda():
    m = Model("todaiji-pagoda")
    W = 90
    m.add(0, box("ground", W, W, 0.3, (0, 0, 0), GRAVEL), "grounds")
    m.add(0, box("platform", 24, 24, 1.6, (0, 0, 0.3), STONE))
    m.add(1, gallery("kairo", rect_pts(W - 6, W - 6), w=5, h=3.6, closed=True, wall=WHITE), "halls")
    for i, (x, y, d) in enumerate(((0, -W / 2 + 3, 0), (0, W / 2 - 3, 180), (-W / 2 + 3, 0, -90), (W / 2 - 3, 0, 90))):
        m.add(1, put(small_gate(f"gate{i}", 9, 6, 5.0, VERM, TILE, "irimoya"), x, y, d))
    m.add(2, put(npagoda("pagoda", 12.0, 7, 84.0), 0, 0, 0, 1.9), "pagoda")
    return m


def nandaimon(edo=True):
    m = Model("nandaimon" if edo else "nandaimon-752")
    m.add(0, box("ground", 36, 16, 0.3, (0, 0, 0), GRAVEL), "grounds")
    if not edo:
        G(m, "gate", 29, 11, 9.0, 7.0, roof_h=8.0, bays=5, top="irimoya", shibi=GILT)
        return m
    # Chōgen's gate: one-piece round pillars, stacked bracket arms, a pent roof and an open upper frame under a hip-and-gable roof
    w, d = 29.0, 10.8
    m.add(0, box("base", w + 3, d + 3, 1.0, (0, 0, 0.3), STONE))
    z0 = 1.3
    cols = []
    for i in range(6):
        for j in range(3):
            cols.append(cylinder(f"col{i}{j}", 0.55, 19.5, (-w / 2 + i * w / 5, -d / 2 + j * d / 2, z0), WOOD, verts=10))
    for k, zz in enumerate((5.5, 11.0, 16.5)):
        cols.append(box(f"nuki{k}", w + 1.0, 0.5, 0.6, (0, -d / 2, z0 + zz), shade(WOOD, -0.1)))
        cols.append(box(f"nukib{k}", w + 1.0, 0.5, 0.6, (0, d / 2, z0 + zz), shade(WOOD, -0.1)))
    for s in (-1, 1):
        cols.append(box(f"nio{s}", 3.6, 3.0, 8.4, (s * w * 0.4, d * 0.05, z0), "#5A4030"))
        cols.append(box(f"nio_screen{s}", w / 5 * 0.9, 0.3, 8.0, (s * w * 0.4, -d / 2 + 0.3, z0 + 0.2), shade(DARKW, 0.1)))
    m.add(1, join(cols, "frame"), "halls")
    brk = []
    for t in range(6):
        e = 0.5 + t * 0.5
        brk.append(box(f"brl{t}", w + 2 * e, d + 2 * e, 0.42, (0, 0, z0 + 8.6 + t * 0.55), shade(WOOD, -0.18 + 0.04 * (t % 2))))
        brk.append(box(f"bru{t}", w * 0.86 + 2 * e, d + 2 * e, 0.42, (0, 0, z0 + 17.0 + t * 0.5), shade(WOOD, -0.18 + 0.04 * (t % 2))))
    m.add(1, join(brk, "brackets"))
    m.add(2, eaved_roof("lower_roof", w + 6, d + 6, 3.0, (0, 0, z0 + 11.9), TILE, over=3.2, curve=0.22), "roofs")
    m.add(2, irimoya("upper_roof", w * 0.86 + 6, d + 6, 7.0, (0, 0, z0 + 20.0), TILE, over=3.0))
    return m


def shosoin():
    m = Model("shosoin")
    m.add(0, box("ground", 60, 30, 0.3, (0, 0, 0), GRAVEL), "grounds")
    m.add(0, wall_line("fence", rect_pts(57, 27), 1.6, 0.6, WOOD, TILE, closed=True))
    body, rf = log_store("store", 33, 9.4, 5.6, 2.7, (0, 0, 0.3), TILE, n_pillars=10)
    m.add(1, body, "storehouse")
    m.add(2, rf, "roof")
    trees(m, "trees", [(-25, 10), (24, -9), (25, 10)], 3.0, CEDAR)
    return m


def hokkedo(edo=True):
    m = Model("hokkedo" if edo else "hokkedo-752")
    m.add(0, box("ground", 36, 36, 0.3, (0, 0, 0), MOSS), "grounds")
    m.add(0, box("terrace", 30, 32, 0.9, (0, 0, 0.3), STONE))
    if edo:
        H(m, "shodo", 22, 13, 5.5, 0, 6.5, z=1.2, plat=0, roof="hip", roof_h=7.0, bays=5, over=3.0, doors=False)
        H(m, "raido", 22, 13, 5.5, 0, -6.5, z=1.2, plat=0, roof="irimoya", roof_h=7.0, bays=5, over=3.0)
    else:
        H(m, "shodo", 22, 13, 5.5, 0, 8, z=1.2, plat=0, roof="hip", roof_h=7.0, bays=5, over=3.0, doors=False)
        H(m, "raido", 18, 7, 4.2, 0, -10, z=1.2, plat=0, roof="gable", roof_h=3.5, bays=5, over=1.5)
    trees(m, "trees", [(-15, 15), (15, 16), (-16, -14)], 3.0, CEDAR)
    return m


def nigatsudo():
    """The Hall of the Second Month on its slope: the hall on the hillside, a deep stage on a lattice of pillars, a covered stair."""
    m = Model("nigatsudo")
    W, D = 50, 40
    m.add(0, box("ground", W, D, 0.3, (0, 0, 0), MOSS), "grounds")
    top = 9.0
    m.add(0, prism("hill", [(-25, 20), (25, 20), (25, 2), (-25, 2)], top, (0, 0, 0.3), shade(MOSS, -0.08)))
    m.add(0, mesh_from("slope", [(-25, 2, top + 0.3), (25, 2, top + 0.3), (25, -4, 0.3), (-25, -4, 0.3), (-25, 2, 0.3), (25, 2, 0.3)],
                       [(0, 3, 2, 1), (3, 4, 5, 2), (0, 4, 3), (1, 2, 5), (4, 0, 1, 5)], (0, 0, 0), shade(MOSS, -0.18)))
    lat = []
    sx0, sx1, sy0, sy1 = -16.0, 16.0, -13.0, 2.0
    xs = [sx0 + i * 4 for i in range(9)]
    ys = [sy0 + j * 3.75 for j in range(5)]
    def gz(y):
        return max(0.3, min(top + 0.3, 0.3 + top * (y + 4) / 6))
    for x in xs:
        for y in ys:
            g = gz(y)
            if top + 0.3 - g > 0.2:
                lat.append(box(f"pil{x:.0f}_{y:.0f}", 0.7, 0.7, top + 0.3 - g, (x, y, g), WOOD))
    for k, zb in enumerate((3.0, 6.0)):
        for y in ys:
            if gz(y) < zb:
                lat.append(box(f"nx{k}_{y:.0f}", sx1 - sx0 + 1, 0.4, 0.45, (0, y, zb), shade(WOOD, -0.1)))
    lat.append(box("deck", sx1 - sx0 + 2, sy1 - sy0 + 2, 0.6, (0, (sy0 + sy1) / 2, top + 0.3), "#9C8263"))
    lat.append(box("rail", sx1 - sx0 + 2, 0.3, 1.0, (0, sy0 - 1, top + 0.9), WOOD))
    m.add(1, join(lat, "stage"), "halls")
    H(m, "hall", 30, 16, 5.5, 0, 10, z=top + 0.3, plat=0, floor=0.6, roof="irimoya", roof_h=8.5, bays=7, col=WOOD, wall="#DCCFB6", over=3.5)
    m.add(1, gallery("stair", [(-21, -18), (-21, 6)], w=3.2, h=2.8, col=WOOD, roof=TILE, floor=0.4), "halls")
    m.add(2, grove("forest", [(-20, 16, top), (20, 17, top), (22, -14, 0), (-10, -17, 0), (12, -18, 0)], 3.4, CEDAR))
    return m


# ---------------------------------------------------------------- Kōfuku-ji and the Gekyō

def kofukuji(stage="752"):
    """Kōfuku-ji: the Central Golden Hall in its cloister, the Eastern and Western Golden Halls, the five-storey pagoda, the octagonal halls."""
    m = Model({"720": "kofukuji-720", "752": "kofukuji", "900": "kofukuji-900"}[stage])
    W, D = 300, 220
    m.add(0, box("ground", W, D, 0.3, (0, 0, 0), GRAVEL), "grounds")
    m.add(0, wall_line("wall_s", [(-W / 2 + 2, -D / 2 + 2), (W / 2 - 2, -D / 2 + 2)], 3.2, 1.4))
    court(m, "chu", -9, 5, 110, 100, dict(w=34, d=20, h=9.5, y=25, plat=1.4, roof="hip", roof_h=11, bays=7, mokoshi=True, shibi=GILT, over=5.0),
          dict(w=18, d=9, h1=6.0, h2=4.5, roof_h=5.5, bays=3))
    H(m, "kodo", 38, 16, 7.0, -9, 85, plat=1.2, roof="irimoya", roof_h=9, bays=9)
    G(m, "nandaimon", 20, 9, 6.0, 4.5, -9, -D / 2 + 7, roof_h=5.5, bays=5)
    late = stage in ("752", "900")
    if late:
        H(m, "tokondo", 25, 14, 8.0, 82, 10, deg=-90, plat=1.6, roof="hip", roof_h=9, bays=7, shibi=GILT)
        H(m, "saikondo", 25, 14, 8.0, -98, 10, deg=90, plat=1.6, roof="hip", roof_h=9, bays=7)
        m.add(2, put(npagoda("pagoda", 8.7, 5, 50.0), 108, -55), "pagoda")
        m.add(1, put(octagon_hall("hokuendo", 7.5, 6.0, 7.5), -128, 62), "halls")
    if stage == "900":
        m.add(1, put(octagon_hall("nanendo", 7.5, 6.0, 7.5), -118, -75), "halls")
    if stage == "720":
        m.add(0, box("hokuendo_site", 22, 22, 0.8, (-128, 62, 0.3), EARTH))
    trees(m, "trees", [(-140, -100), (140, -100), (140, 95), (-140, 100), (60, 90), (60, -95), (-60, -95), (125, 40)], 4.5)
    return m


def sarusawa():
    m = Model("sarusawa")
    m.add(0, box("ground", 110, 80, 0.3, (0, 0, 0), GRASS), "grounds")
    m.add(0, blob("bank", 51, 36, 0.4, (0, -2, 0.0), STONE, 0.9))
    m.add(0, blob("pond", 48, 33, 0.5, (0, -2, 0.05), WATER, 0.9))
    m.add(1, grove("willows", [(-50, 10, 0), (-42, -30, 0), (-10, -38, 0), (25, -37, 0), (50, -14, 0), (48, 20, 0), (20, 34, 0)], 3.2, WILLOW), "trees")
    H(m, "uneme", 5, 4, 2.6, -44, 30, deg=180, plat=0.4, roof="gable", roof_h=2.0, bays=2, wall=VERM, roof_color=BARK)
    m.add(1, put(torii("torii", 4, 4, (0, 0, 0), VERM), -44, 23.5))
    m.add(1, stair("steps52", 6, 3.5, 6, 8, (-30, 35, 0.3), "S", STONE))
    m.add(2, lantern_row("lanterns", (-20, 36), (30, 36), 6, 0.9))
    return m


def gangoji(edo=False):
    m = Model("gangoji-1700" if edo else "gangoji")
    W, D = 200, 200
    m.add(0, box("ground", W, D, 0.3, (0, 0, 0), GRAVEL if not edo else EARTH), "grounds")
    m.add(0, box("pagoda_court", 54, 54, 0.4, (55, -40, 0.3), shade(GRAVEL, -0.05)))
    m.add(0, wall_line("pagoda_wall", rect_pts(54, 54, 55, -40), 2.8, 1.2, closed=True))
    m.add(2, put(npagoda("pagoda", 8.5, 5, 50.0), 55, -40, 0, 0.7), "pagoda")
    if not edo:
        court(m, "kon", -35, -10, 100, 110, dict(w=30, d=18, h=8.5, y=8, plat=1.4, roof="irimoya", roof_h=10, bays=7, shibi=GILT, over=4.5),
              dict(w=16, d=8, h1=5.5, h2=4.0, roof_h=5, bays=3))
        H(m, "kodo", 34, 15, 7.0, -35, 70, plat=1.2, roof="irimoya", roof_h=8.5, bays=9)
        for i, y in enumerate((40, 70)):
            H(m, f"sobo{i}", 70, 10, 4.0, 55, y, plat=0.5, roof="gable", roof_h=4.0, bays=14, doors=False)
        trees(m, "trees", [(-90, -90), (90, -90), (-90, 90), (90, 92), (0, -90)], 4.5)
    else:
        H(m, "gokurakubo", 14, 14, 5.0, 40, 55, plat=0.8, roof="irimoya", roof_h=7, bays=4, col=WOOD, wall="#DCCFB6")
        H(m, "zenshitsu", 26, 10, 3.8, 40, 78, plat=0.6, roof="gable", roof_h=4.5, bays=8, col=WOOD, wall="#DCCFB6", doors=False)
        m.add(1, machiya_rows("town_w", -98, -98, -10, 98, lot=6.5, depth=11), "town")
        m.add(1, machiya_rows("town_s", 0, -98, 98, -72, lot=6.5, depth=11))
        m.add(1, machiya_rows("town_e", 88, -10, 98, 30, lot=5.0, depth=9))
        trees(m, "trees", [(15, 25), (70, 30), (20, 90), (80, 95)], 4.0)
    return m


def kasuga_taisha():
    """Kasuga: vermilion corridor and south gate, the four small sanctuaries behind their fence, worship halls, lanterns."""
    m = Model("kasuga-taisha")
    W, D = 130, 110
    m.add(0, box("ground", W, D, 0.3, (0, 0, 0), MOSS), "grounds")
    m.add(0, box("court", 76, 58, 0.25, (0, 12, 0.3), GRAVEL))
    m.add(1, gallery("kairo", rect_pts(76, 58, 0, 12), w=4.5, h=3.4, closed=True, wall=WHITE, roof=TILE), "halls")
    G(m, "nanmon", 12, 7, 5.0, 3.6, 0, -17, roof_h=4.5, bays=3, base=0.6)
    H(m, "heiden", 20, 7, 3.6, 0, 4, plat=0.6, roof="irimoya", roof_h=4.0, bays=5, doors=False, wall=VERM)
    m.add(1, wall_line("mizugaki", rect_pts(34, 12, 0, 30), 1.6, 0.5, VERM, BARK, closed=True))
    for i in range(4):
        x = -12 + i * 8
        H(m, f"honden{i}", 4.2, 5.4, 2.6, x, 30, plat=0, floor=1.0, roof="gable", roof_h=2.4, bays=1, wall=VERM, roof_color=BARK, over=1.2, doors=True)
        m.add(2, seg_prism(f"hisashi{i}", (x, 26.6), (x, 25.0), 3.0, 4.6, 1.0, BARK))
    G(m, "chumon", 12, 6, 4.5, 3.4, 0, 18, roof_h=4.0, bays=3, base=0.4)
    for s in (-1, 1):
        m.add(2, lantern_row(f"lant_app{s}", (s * 5, -54), (s * 5, -24), 8, 1.0), "lanterns")
        m.add(2, lantern_row(f"lant_side{s}", (s * 44, -14), (s * 44, 36), 6, 0.9))
    bronze = [box(f"bl{i}{s}", 0.6, 0.6, 0.8, (s * 38.0, -14 + i * 4.0, 2.4), GILT) for i in range(14) for s in (-1, 1)]
    m.add(2, join(bronze, "hanging_lanterns"))
    m.add(2, grove("cedars", [(-58, 45, 0), (-40, 50, 0), (0, 50, 0), (40, 50, 0), (58, 44, 0), (60, 0, 0), (-60, 0, 0), (58, -40, 0), (-58, -40, 0), (-30, -45, 0), (30, -45, 0)], 5.0, CEDAR))
    return m


# ---------------------------------------------------------------- the temples of the grid

def yakushiji(stage="752"):
    m = Model({"720": "yakushiji-720", "752": "yakushiji", "1700": "yakushiji-1700"}[stage])
    W, D = 190, 180
    m.add(0, box("ground", W, D, 0.3, (0, 0, 0), GRAVEL if stage != "1700" else EARTH), "grounds")
    for x in (-38, 38):
        m.add(0, box(f"pbase{x}", 15, 15, 1.3, (x, -28, 0.3), STONE))
    if stage == "1700":
        m.add(2, put(npagoda("east_pagoda", 7.0, 3, 34.0, mokoshi=True), 38, -28, 0, 1.6), "pagoda")
        H(m, "kari_kondo", 22, 13, 5.5, 0, 22, plat=1.0, roof="irimoya", roof_h=7, bays=5, col=WOOD, wall="#DCCFB6")
        H(m, "toindo", 20, 13, 5.5, 72, 55, deg=-90, plat=1.0, roof="irimoya", roof_h=7, bays=5)
        H(m, "kodo", 30, 14, 6.0, 0, 70, plat=1.0, roof="irimoya", roof_h=7.5, bays=7, col=WOOD, wall="#DCCFB6")
        m.add(0, wall_line("wall", [(-94, -88), (94, -88)], 2.6, 1.2))
        m.add(1, put(small_gate("nandaimon", 10, 6, 5.0, VERM, TILE, "irimoya"), 0, -86))
        trees(m, "trees", [(-38, -28), (-70, 30), (-80, -60), (70, -65), (-40, 70)], 4.5)
        return m
    m.add(1, gallery("kairo", rect_pts(150, 120, 0, -8), w=6, h=3.8, closed=True, wall=WHITE), "halls")
    G(m, "chumon", 20, 9, 6.0, 4.5, 0, -68, roof_h=5.5, bays=5)
    if stage == "720":
        H(m, "kondo", 28, 17, 8.0, 0, 18, plat=1.6, roof="irimoya", roof_h=10, bays=7, mokoshi=True, shibi=GILT)
        scaff = [box(f"sc{i}{j}", 0.3, 0.3, 14, (-16 + i * 4.0, 18 + j * 21 - 10.5, 0.3), WOOD) for i in range(9) for j in range(2)]
        m.add(1, join(scaff, "scaffold"))
        for x in (-38, 38):
            m.add(1, box(f"shinbashira{x}", 0.9, 0.9, 24, (x, -28, 1.6), WOOD))
            m.add(1, join([cylinder(f"fs{x}{i}{j}", 0.6, 0.4, (x - 4.5 + i * 3, -28 - 4.5 + j * 3, 1.6), STONE, verts=8) for i in range(4) for j in range(4) if i in (0, 3) or j in (0, 3)], f"stones{x}"))
    else:
        H(m, "kondo", 28, 17, 8.0, 0, 18, plat=1.6, roof="irimoya", roof_h=10, bays=7, mokoshi=True, shibi=GILT)
        for x, nm in ((-38, "west_pagoda"), (38, "east_pagoda")):
            m.add(2, put(npagoda(nm, 7.0, 3, 34.0, mokoshi=True), x, -28, 0, 1.6), "pagoda")
    H(m, "kodo", 40, 16, 7.0, 0, 62, plat=1.2, roof="irimoya", roof_h=8.5, bays=9)
    trees(m, "trees", [(-85, -80), (85, -80), (-85, 75), (85, 75)], 4.0)
    return m


def daianji(edo=False):
    m = Model("daianji-1700" if edo else "daianji")
    W, D = 180, 200
    m.add(0, box("ground", W, D, 0.3, (0, 0, 0), GRAVEL if not edo else GRASS), "grounds")
    if not edo:
        court(m, "kon", 0, -10, 130, 120, dict(w=34, d=19, h=9.0, y=10, plat=1.5, roof="hip", roof_h=10.5, bays=7, shibi=GILT, over=5.0),
              dict(w=20, d=9, h1=6.0, h2=4.5, roof_h=5.5, bays=5))
        H(m, "kodo", 40, 16, 7.0, 0, 72, plat=1.2, roof="irimoya", roof_h=8.5, bays=9)
        for s in (-1, 1):
            H(m, f"sobo{s}", 60, 9, 4.0, s * 78, 30, deg=90, plat=0.5, roof="gable", roof_h=4.0, bays=12, doors=False)
        trees(m, "trees", [(-80, -90), (80, -90), (-60, 92), (60, 92)], 4.0)
    else:
        H(m, "hondo", 16, 12, 4.5, 0, 10, plat=0.8, roof="irimoya", roof_h=6, bays=4, col=WOOD, wall="#DCCFB6")
        H(m, "kuri", 14, 9, 3.6, 25, 30, plat=0.4, roof="gable", roof_h=4, bays=4, col=WOOD, wall=CLAY, roof_color=THATCH, doors=False)
        m.add(0, wall_line("wall", rect_pts(70, 60, 5, 15), 2.2, 1.0, closed=True))
        m.add(1, put(small_gate("gate", 6, 4, 3.8, WOOD, TILE), 5, -15))
        for i, (x, y) in enumerate(((-40, -70), (40, -70))):
            m.add(0, dome(f"pagoda_mound{i}", 10, (x, y, 0.3), shade(GRASS, -0.1), squash=0.25, segments=14, rings=6))
        rows = [box(f"field{i}", 80, 22, 0.15, (x, y, 0.3), shade(FIELD, 0.1 * (i % 2))) for i, (x, y) in enumerate(((-45, 72), (45, 72), (-50, -30), (55, -30)))]
        m.add(0, join(rows, "fields"))
        trees(m, "trees", [(-20, 35), (30, -5), (-70, 20), (70, 10), (0, 90)], 4.5)
    return m


def toshodaiji():
    m = Model("toshodaiji")
    W, D = 150, 150
    m.add(0, box("ground", W, D, 0.3, (0, 0, 0), GRAVEL), "grounds")
    m.add(0, wall_line("wall", [(-74, -73), (74, -73)], 3.0, 1.3))
    m.add(1, put(small_gate("nandaimon", 14, 7, 6.0, VERM, TILE, "irimoya"), 0, -72))
    # the Kondō: seven bays, the front bay left open as a portico of eight columns
    m.add(0, box("kondo_plat", 33, 20, 1.3, (0, 0, 0.3), STONE))
    m.add(0, stair("kondo_st", 10, 1.3, 3, 4, (0, -11.5, 0.3), "S", STONE))
    body, roof = hall_parts("kondo", 28, 11.5, 8.5, roof="hip", roof_h=10.5, bays=7, plat=0, shibi=GILT, over=4.5)
    m.add(1, put(body, 0, 1.5, 0, 1.6), "halls")
    porch = [cylinder(f"pc{i}", 0.4, 8.5, (-14 + i * 4, -6.5, 1.6), VERM, verts=10) for i in range(8)]
    porch.append(box("porch_beam", 29, 3.6, 0.6, (0, -5.2, 1.6 + 7.9), VERM))
    m.add(1, join(porch, "porch"))
    m.add(2, put(hip("kondo_roof", 28, 14.6, 10.5, (0, 0, 0), TILE, over=4.5, shibi=GILT), 0, -0.3, 0, 1.6 + 8.5), "roofs")
    H(m, "kodo", 34, 13.5, 7.0, 0, 40, plat=1.0, roof="irimoya", roof_h=8.5, bays=9)
    for i, x in enumerate((48, 60)):
        b, r = log_store(f"store{i}", 6, 5, 3.6, 1.6, (x, 10, 0.3), TILE, n_pillars=3, rooms=False)
        m.add(1, b)
        m.add(2, r)
    G(m, "koro", 10, 6, 4.0, 3.5, 50, 40, deg=-90, roof_h=3.5, bays=3, base=0.5)
    trees(m, "pines", [(-60, -55), (-40, -60), (40, -60), (60, -50), (-60, 20), (-62, 60), (60, 70), (-25, 68), (25, 70)], 4.0)
    return m


def saidaiji():
    m = Model("saidaiji")
    W, D = 180, 130
    m.add(0, box("ground", W, D, 0.3, (0, 0, 0), GRAVEL), "grounds")
    m.add(0, wall_line("wall", [(-88, -63), (88, -63)], 2.8, 1.2))
    m.add(1, put(small_gate("gate", 12, 6, 5.5, VERM, TILE, "irimoya"), 0, -62))
    H(m, "hondo", 26, 18, 6.5, 0, 25, plat=1.2, roof="irimoya", roof_h=9, bays=7, col=WOOD, wall="#DCCFB6")
    H(m, "shiodo", 16, 12, 5.0, -38, 20, plat=1.0, roof="irimoya", roof_h=6.5, bays=5)
    H(m, "aizendo", 12, 10, 4.0, 40, 30, plat=0.8, roof="irimoya", roof_h=5, bays=3, col=WOOD, wall="#DCCFB6")
    G(m, "shoro", 7, 6, 3.5, 3.0, 40, -5, roof_h=3.2, bays=1, base=0.5)
    m.add(0, box("pagoda_platform", 20, 20, 1.6, (-55, -30, 0.3), STONE))
    stones = [cylinder(f"fs{i}{j}", 0.7, 0.4, (-55 - 6 + i * 4, -36 + j * 4, 1.9), STONE, verts=8) for i in range(4) for j in range(4)]
    m.add(1, join(stones, "found_stones"))
    trees(m, "trees", [(-80, 50), (-60, 55), (70, 55), (80, 0), (-80, -10), (65, -45), (-20, -45)], 4.0)
    return m


def market():
    """The East Market: an earth-walled ward block, gates, rows of stalls, the market office and drum, a canal landing."""
    m = Model("market")
    W, D = 220, 220
    m.add(0, box("ground", W, D, 0.3, (0, 0, 0), EARTH), "grounds")
    m.add(0, box("canal", 8, D, 0.4, (-W / 2 + 6, 0, 0.0), WATER))
    m.add(0, box("landing", 10, 30, 0.6, (-W / 2 + 15, 0, 0.3), WOOD))
    m.add(0, wall_line("wall_n", [(-98, 104), (-8, 104)], 3.2, 1.4))
    m.add(0, wall_line("wall_n2", [(8, 104), (106, 104)], 3.2, 1.4))
    m.add(0, wall_line("wall_s", [(-98, -104), (-8, -104)], 3.2, 1.4))
    m.add(0, wall_line("wall_s2", [(8, -104), (106, -104)], 3.2, 1.4))
    m.add(0, wall_line("wall_e", [(106, -104), (106, -8)], 3.2, 1.4))
    m.add(0, wall_line("wall_e2", [(106, 8), (106, 104)], 3.2, 1.4))
    m.add(0, wall_line("wall_w", [(-98, -104), (-98, -20)], 3.2, 1.4))
    m.add(0, wall_line("wall_w2", [(-98, 20), (-98, 104)], 3.2, 1.4))
    for i, (x, y, d) in enumerate(((0, -104, 0), (0, 104, 180), (106, 0, 90), (-98, 0, -90))):
        m.add(1, put(small_gate(f"gate{i}", 9, 5, 4.6, VERM, TILE, "irimoya"), x, y, d), "stalls")
    stalls = []
    k = 0
    for qx in (-50, 55):
        for qy in (-55, 52):
            for r in range(5):
                y = qy - 36 + r * 18
                stalls.append(box(f"st{k}", 64, 5, 2.4, (qx, y, 0.3), shade(WOOD, 0.15 + 0.05 * (r % 2))))
                stalls.append(seg_prism(f"sr{k}", (qx - 33, y), (qx + 33, y), 2.7, 7.0, 1.6, shade(BARK, 0.05 * (r % 3))))
                k += 1
    m.add(1, join(stalls, "stall_rows"))
    H(m, "ichi_tsukasa", 18, 10, 4.5, 0, 0, plat=0.6, roof="irimoya", roof_h=5.5, bays=5, roof_color=TILE)
    G(m, "drum_tower", 6, 6, 3.5, 3.0, 18, 14, roof_h=3, bays=1, base=0.4)
    trees(m, "willows", [(-20, -20), (20, -22), (-20, 22), (-85, 60), (-85, -60)], 3.2, WILLOW)
    return m


BUILDERS = {
    "nara/daigokuden": lambda: daigokuden(True),
    "nara/daigokuden-752": lambda: daigokuden(False),
    "nara/chodo-in": chodo_in,
    "nara/suzakumon": suzakumon,
    "nara/suzaku-oji": suzaku_oji,
    "nara/rajomon": rajomon,
    "nara/daibutsuden": lambda: daibutsuden(False),
    "nara/daibutsuden-1709": lambda: daibutsuden(True),
    "nara/todaiji-pagoda": todaiji_pagoda,
    "nara/nandaimon": lambda: nandaimon(True),
    "nara/nandaimon-752": lambda: nandaimon(False),
    "nara/shosoin": shosoin,
    "nara/hokkedo": lambda: hokkedo(True),
    "nara/hokkedo-752": lambda: hokkedo(False),
    "nara/nigatsudo": nigatsudo,
    "nara/kofukuji-720": lambda: kofukuji("720"),
    "nara/kofukuji": lambda: kofukuji("752"),
    "nara/kofukuji-900": lambda: kofukuji("900"),
    "nara/sarusawa": sarusawa,
    "nara/gangoji": lambda: gangoji(False),
    "nara/gangoji-1700": lambda: gangoji(True),
    "nara/kasuga-taisha": kasuga_taisha,
    "nara/yakushiji-720": lambda: yakushiji("720"),
    "nara/yakushiji": lambda: yakushiji("752"),
    "nara/yakushiji-1700": lambda: yakushiji("1700"),
    "nara/daianji": lambda: daianji(False),
    "nara/daianji-1700": lambda: daianji(True),
    "nara/toshodaiji": toshodaiji,
    "nara/saidaiji": saidaiji,
    "nara/market": market,
}
