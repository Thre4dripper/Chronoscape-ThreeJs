"""Kyoto / Heian-kyō landmark miniatures."""
import math
from chronokit import Model, box, cylinder, dome, join, shade, mesh_from
from worldkit import *

VERM = "#B8452E"          # vermilion (ni-nuri) of state halls and shrines
WHITE = "#EEE7D8"         # plastered wall panels
BARK = "#6E4B3A"          # cypress-bark (hiwada) roofs
TILE = TILE_GREY
GLAZE = "#3F8A62"         # green-glazed ridge and eave tiles
STONE = "#BDB5A6"
GRAVEL = "#E2DACA"
EARTH = "#C4B28D"
CLAY = "#CDBB98"          # earth walls (tsuiji)
MOSS = "#8E9B6A"
WOOD = "#6A5442"          # unpainted, weathered timber
DARKW = "#3A2E26"
PINE = "#557048"
SAKURA = "#E2B4BE"
FIELD = "#A9A877"


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

def irimoya(name, w, d, h, loc=(0, 0, 0), color=TILE, over=None, curve=0.16, ridge=None, gable=None):
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
            parts.append(box(f"{name}_sb{s}", rt * 1.4, rt * 1.0, rt * 3.0, (x + s * (rl / 2 + rt * 0.3), y, z + h - rt * 0.4), shibi))
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
        rparts.append(irimoya(name + "_ir", w, d, rh, (0, 0, zt), roof_color, over=over, ridge=ridge))
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
        rparts.append(irimoya(name + "_tr", uw, ud, rh, (0, 0, zu + 0.4 + h2), roof, over=ud * 0.55, ridge=ridge))
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


# ---------------------------------------------------------------- the Greater Palace

def chodo_in():
    """The northern half of the State Halls: Daigokuden on its podium, the Dragon-Tail Terrace and its towers, assembly halls."""
    m = Model("chodo-in")
    W, D = 170, 220
    m.add(0, box("ground", W, D, 0.3, (0, 0, 0), GRAVEL), "grounds")
    m.add(0, box("terrace", W - 12, 70, 1.6, (0, 70, 0.3), shade(GRAVEL, -0.05)))
    m.add(0, box("terrace_edge", W - 12, 1.2, 2.2, (0, 35, 0.3), STONE))
    m.add(0, stair("rstair_w", 8, 1.8, 6, 5, (-30, 32, 0), "S", STONE))
    m.add(0, stair("rstair_e", 8, 1.8, 6, 5, (30, 32, 0), "S", STONE))
    m.add(1, gallery("kairo", rect_pts(W - 6, D - 6), w=6, h=4.2, closed=True, wall=WHITE), "halls")
    # the Daigokuden: eleven bays on a stone podium, hipped roof with green-glazed trim and ridge fins
    m.add(0, box("podium", 62, 30, 3.0, (0, 72, 1.9), STONE))
    m.add(0, stair("podium_st", 14, 3.0, 6, 6, (0, 54, 1.9), "S", STONE))
    H(m, "daigokuden", 52, 21, 11.0, 0, 72, z=4.9, plat=0, roof="hip", roof_h=15, bays=11, trim=GLAZE, ridge=GLAZE, shibi=GILT, over=6.5)
    # Sōryūrō and Byakkorō on the terrace ends: two-storey towers with hip-and-gable roofs
    for s, nm in ((1, "soryuro"), (-1, "byakkoro")):
        G(m, nm, 14, 10, 6.0, 5.0, s * 64, 40, z=1.9, roof_h=7, bays=3, top="irimoya", ridge=GLAZE)
    # the assembly halls (chōdō) facing the court from east and west
    for s in (-1, 1):
        for i, y in enumerate((-5, -45, -85)):
            H(m, f"chodo{s}{i}", 34, 11, 5.5, s * 52, y, deg=-90 * s, plat=0.8, roof="hip", roof_h=6, bays=7, trim=GLAZE)
    G(m, "kaishomon", 24, 10, 6.5, 4.5, 0, -101, roof_h=6, bays=5)
    return m


def shinden_hall(name, w, d, h, roof=BARK, floor=1.6, col=VERM, wall=WHITE):
    return hall_parts(name, w, d, h, roof="irimoya", roof_color=roof, col=col, wall=wall, plat=0, floor=floor, roof_h=min(w, d) * 0.6, doors=True)


def SH(m, name, w, d, h, x=0.0, y=0.0, deg=0.0, **kw):
    body, roof = shinden_hall(name, w, d, h, **kw)
    m.add(1, put(body, x, y, deg), "halls")
    m.add(2, put(roof, x, y, deg), "roofs")


def dairi():
    """The emperor's residence: Shishinden and its gravel court, Seiryōden, the rear pavilions, all linked by corridors."""
    m = Model("dairi")
    W, D = 220, 300
    m.add(0, box("ground", W, D, 0.3, (0, 0, 0), EARTH), "grounds")
    m.add(0, wall_line("outer", rect_pts(W - 2, D - 2), 3.4, 1.6, closed=True))
    m.add(0, box("court", 90, 58, 0.35, (0, -42, 0.05), GRAVEL))
    m.add(1, gallery("kairo", rect_pts(110, 110, 0, -30), w=5, h=3.4, roof=BARK, closed=True), "halls")
    SH(m, "shishinden", 34, 22, 6.5, 0, 0)
    m.add(1, stair("shishinden_st", 10, 2.0, 4, 6, (0, -14, 0), "S", WOOD))
    m.add(1, tree("sakon_cherry", 3.2, (14, -22, 0), SAKURA))
    m.add(1, tree("ukon_tachibana", 2.8, (-14, -22, 0), "#4E7A3C"))
    m.add(1, put(small_gate("kenreimon", 12, 7, 6.0), 0, -D / 2 + 1))
    m.add(1, put(small_gate("jomeimon2", 10, 6, 5.5), 0, -85))
    SH(m, "seiryoden", 30, 14, 5.5, 50, 10, deg=90)
    SH(m, "jijuden", 26, 14, 5.5, 0, 50)
    SH(m, "joneiden", 26, 14, 5.5, 0, 88)
    for i, (x, y) in enumerate(((-62, 45), (62, 45), (-62, 85), (62, 85), (-55, 125), (55, 125), (0, 125))):
        SH(m, f"pav{i}", 22, 13, 5.0, x, y)
    m.add(1, gallery("watadono", [(0, 11), (0, 43)], w=4, h=3.0, roof=BARK))
    m.add(1, gallery("wd2", [(0, 57), (0, 81)], w=4, h=3.0, roof=BARK))
    m.add(1, gallery("wd3", [(-51, 45), (-13, 45)], w=4, h=3.0, roof=BARK))
    m.add(1, gallery("wd4", [(13, 45), (51, 45)], w=4, h=3.0, roof=BARK))
    m.add(1, gallery("wd5", [(-51, 85), (-13, 85)], w=4, h=3.0, roof=BARK))
    m.add(1, gallery("wd6", [(13, 85), (51, 85)], w=4, h=3.0, roof=BARK))
    m.add(1, gallery("wd7", [(0, 95), (0, 118)], w=4, h=3.0, roof=BARK))
    m.add(1, grove("trees", [(-90, -110, 0), (90, -110, 0), (-95, 0, 0), (95, -40, 0), (-90, 130, 0), (92, 120, 0), (-30, 140, 0)], 4.0))
    return m


def suzakumon():
    m = Model("suzakumon")
    m.add(0, box("ground", 40, 18, 0.3, (0, 0, 0), GRAVEL), "grounds")
    m.add(0, wall_line("wall", [(-20, 2), (-17, 2)], 4.5, 2.0))
    m.add(0, wall_line("wall2", [(17, 2), (20, 2)], 4.5, 2.0))
    G(m, "gate", 34, 13, 8.0, 6.0, roof_h=8.5, bays=7, top="hip", trim=GLAZE, ridge=GLAZE, shibi=GILT)
    return m


def rashomon():
    m = Model("rashomon")
    m.add(0, box("ground", 36, 12, 0.3, (0, 0, 0), GRAVEL), "grounds")
    G(m, "gate", 32, 8.5, 8.0, 6.0, roof_h=7.5, bays=7, top="irimoya", ridge=GLAZE)
    return m


def rashomon_ruin():
    """The fallen gate: its podium, foundation stones, a few leaning posts and heaps of tiles in the grass."""
    m = Model("rashomon-ruin")
    m.add(0, box("ground", 36, 12, 0.3, (0, 0, 0), MOSS), "grounds")
    m.add(0, box("podium", 33, 10, 0.9, (0, 0, 0.2), shade(STONE, -0.1)))
    stones = []
    for i in range(8):
        for j, y in enumerate((-3.6, 0, 3.6)):
            if (i * 3 + j) % 4 == 1:
                continue
            stones.append(cylinder(f"st{i}{j}", 0.75, 0.5, (-14 + i * 4, y, 1.1), STONE, verts=8))
    m.add(1, join(stones, "stones"), "ruin")
    posts = [box("post0", 0.8, 0.8, 7.0, (-10, -3.6, 1.1), shade(VERM, -0.35)), box("post1", 0.8, 0.8, 4.5, (6, 3.6, 1.1), shade(VERM, -0.35))]
    lean = box("post2", 0.8, 0.8, 8.0, (0, 0, 0), shade(VERM, -0.4))
    lean.rotation_euler = (0.0, 0.9, 0.3)
    posts.append(put(rot(lean, 0), 2, -1.5, 0, 1.3))
    beam = box("beam", 12, 0.7, 0.7, (0, 0, 0), shade(VERM, -0.45))
    beam.rotation_euler = (0.0, 0.18, 0.15)
    posts.append(put(rot(beam, 0), -6, 1.0, 0, 2.2))
    m.add(1, join(posts, "posts"))
    heaps = [dome(f"heap{i}", 2.2 + (i % 3) * 0.6, (x, y, 1.0), shade(TILE, 0.15), squash=0.4, segments=10, rings=5) for i, (x, y) in enumerate(((-13, 2), (-4, -2.5), (9, 1.5), (14, -2)))]
    m.add(2, join(heaps, "tiles"), "ruin")
    m.add(2, grove("weeds", [(-16, -4.5, 0), (16, 4, 0), (4, 4.5, 0)], 1.4, "#7E8C55"))
    return m


# ---------------------------------------------------------------- the south temples

def east_west_temple(mirror=1, pagoda_on=True, early=False):
    """Tō-ji (mirror=1, pagoda south-east) or Sai-ji (mirror=-1): the Kondō and the five-storey pagoda."""
    m = Model("toji")
    W, D = 140, 120
    m.add(0, box("ground", W, D, 0.3, (0, 0, 0), GRAVEL), "grounds")
    m.add(0, wall_line("wall_s", [(-W / 2 + 1, -D / 2 + 1), (W / 2 - 1, -D / 2 + 1)], 3.2, 1.4))
    m.add(0, wall_line("wall_e", [(mirror * (W / 2 - 1), -D / 2 + 1), (mirror * (W / 2 - 1), D / 2 - 1)], 3.2, 1.4))
    H(m, "kondo", 34, 20, 9.0, -mirror * 45, 22, plat=1.6, roof="irimoya", roof_h=12, bays=7, mokoshi=True, over=4.5)
    m.add(1, gallery("kairo", [(-mirror * 45 - 30, 0), (-mirror * 45 - 30, -30), (-mirror * 45 + 30, -30), (-mirror * 45 + 30, 0)], w=5, h=3.6))
    G(m, "chumon", 18, 9, 6.0, 4.5, -mirror * 45, -36, roof_h=5.5, bays=3)
    if pagoda_on:
        m.add(0, box("pagoda_base", 16, 16, 1.4, (mirror * 42, -24, 0.2), STONE))
        m.add(2, put(jpagoda("pagoda", 9.5, 5, 54.0, WOOD, TILE), mirror * 42, -24, 0, 1.6), "pagoda")
    elif early:
        m.add(0, box("pagoda_base", 16, 16, 1.4, (mirror * 42, -24, 0.2), STONE))
        stones = [cylinder(f"fs{i}{j}", 0.7, 0.5, (mirror * 42 + (i - 1.5) * 3.2, -24 + (j - 1.5) * 3.2, 1.6), STONE, verts=8) for i in range(4) for j in range(4) if i in (0, 3) or j in (0, 3)]
        m.add(1, join(stones, "found_stones"))
        m.add(1, box("heart_pillar", 0.9, 0.9, 30, (mirror * 42, -24, 1.6), WOOD))
    m.add(1, grove("trees", [(mirror * 10, 45, 0), (mirror * 60, 45, 0), (-mirror * 62, -50, 0), (mirror * 15, -50, 0)], 4.5))
    return m


def toji_kodo():
    m = Model("toji-kodo")
    m.add(0, box("ground", 44, 26, 0.3, (0, 0, 0), GRAVEL), "grounds")
    H(m, "kodo", 34, 17, 7.5, 0, 0.5, plat=1.2, roof="hip", roof_h=10, bays=9, over=3.5)
    return m


def shinsen_en(small=False):
    m = Model("shinsen-en-small" if small else "shinsen-en")
    W, D = 200, 240
    m.add(0, box("ground", W, D, 0.3, (0, 0, 0), MOSS if not small else FIELD), "grounds")
    if not small:
        m.add(0, wall_line("wall", rect_pts(W - 2, D - 2), 3.2, 1.4, closed=True))
        m.add(0, blob("pond", 72, 64, 0.35, (0, -30, 0.05), WATER, 0.7))
        m.add(0, blob("island", 14, 10, 1.2, (10, -38, 0), MOSS, 2.1))
        m.add(1, grove("island_pines", [(8, -38, 1.2), (14, -36, 1.2)], 3.0))
        H(m, "kenrinkaku", 30, 15, 6.0, 0, 62, plat=1.4, roof="irimoya", roof_h=8, bays=7, ridge=GLAZE)
        for s in (-1, 1):
            m.add(1, gallery(f"rou{s}", [(s * 18, 62), (s * 50, 62), (s * 50, 0), (s * 50, -18)], w=4.5, h=3.2))
            H(m, f"tsuridono{s}", 12, 9, 3.8, s * 50, -26, plat=0, floor=1.2, roof="irimoya", roof_h=4.5, bays=3, col=VERM)
        m.add(1, gallery("bridge", [(-8, 28), (4, -27)], w=3, h=1.0, roof=WOOD))
        m.add(1, grove("trees", [(-85, 100, 0), (-60, 105, 0), (60, 105, 0), (85, 95, 0), (-88, -100, 0), (88, -105, 0), (-80, 20, 0), (82, 30, 0), (-40, -105, 0), (40, -108, 0)], 5.0))
    else:
        m.add(0, blob("pond", 38, 30, 0.35, (0, -55, 0.05), WATER, 1.3))
        m.add(0, blob("island", 8, 6, 1.0, (4, -58, 0), MOSS, 0.4))
        m.add(1, put(small_gate("torii_gate", 6, 3, 4.5, VERM, TILE), 0, -15))
        H(m, "shrine", 8, 6, 3.2, 4, -58, z=1.0, plat=0, roof="gable", roof_h=2.5, bays=2)
        m.add(1, gallery("bridge", [(-30, -58), (-2, -58)], w=2.5, h=1.0, col=VERM, roof=VERM))
        m.add(0, wall_line("fence", rect_pts(110, 80, 0, -55), 2.2, 0.8, closed=True))
        rows = [box(f"paddy{i}", 70, 20, 0.15, (x, y, 0.3), shade(FIELD, 0.12 * (i % 2))) for i, (x, y) in enumerate(((-55, 40), (45, 40), (-55, 75), (45, 75), (-55, 108), (45, 108)))]
        m.add(0, join(rows, "paddies"))
        for i, (x, y) in enumerate(((-30, 20), (30, 15), (70, -10), (-75, -20))):
            H(m, f"farm{i}", 9, 6, 2.6, x, y, plat=0.3, roof="irimoya", roof_color=THATCH, roof_h=4, col=WOOD, wall=CLAY, doors=False, stairs=False)
        m.add(1, grove("trees", [(-50, -30, 0), (52, -40, 0), (-20, -95, 0), (30, -98, 0), (80, 60, 0)], 4.5))
    return m


# ---------------------------------------------------------------- Higashiyama

def kiyomizu(early=False):
    """Kiyomizu-dera: the main hall half on the hill, half on a stage carried by a lattice of pillars over the slope."""
    m = Model("kiyomizu-800" if early else "kiyomizu")
    W, D = 180, 200
    m.add(0, box("ground", W, D, 0.3, (0, 0, 0), MOSS), "grounds")
    top = 14.0
    # the hillside: a plateau to the north, a steep slope falling south, a lower spur for the gate and pagoda to the west
    plateau = [(-90, 100), (90, 100), (90, 14), (-10, 14), (-30, 22), (-90, 22)]
    m.add(0, prism("plateau", plateau, top, (0, 0, 0.3), shade(MOSS, -0.08)))
    sv = [(-10, 14, top), (90, 14, top), (90, -2, 0.3), (-10, -2, 0.3)]
    m.add(0, mesh_from("slope", sv + [(-10, 14, 0.3), (90, 14, 0.3)], [(0, 1, 2, 3), (3, 2, 5, 4), (0, 3, 4), (1, 5, 2), (4, 5, 1, 0)], (0, 0, 0), shade(MOSS, -0.18)))
    m.add(0, prism("spur_slope", [(-90, 22), (-30, 22), (-10, 14), (-10, 6), (-90, 6)], top * 0.55, (0, 0, 0.3), shade(MOSS, -0.12)))
    hx, hy = 40.0, 31.0
    if early:
        H(m, "hondo", 24, 18, 6.0, hx, hy, z=top + 0.3, plat=0, floor=1.0, roof="irimoya", roof_color=BARK, roof_h=9, bays=5, col=WOOD)
        posts = []
        for i in range(5):
            for j in range(2):
                x, y = hx - 10 + i * 5, 12 + j * 3
                hz = top * (y + 2) / 16
                posts.append(box(f"post{i}{j}", 0.8, 0.8, top + 1.3 - hz, (x, y, hz), WOOD))
        posts.append(box("deck", 24, 6, 0.6, (hx, 15, top + 0.7), WOOD))
        m.add(1, join(posts, "posts"), "halls")
        m.add(2, grove("forest", [(-70, 60, top), (-40, 80, top), (0, 70, top), (75, 80, top), (80, 40, top), (-60, -40, 0), (-20, -60, 0), (30, -60, 0), (70, -40, 0), (-75, 0, 0), (-50, 40, top)], 6.0))
        return m
    # the stage (butai) and the pillar lattice (kakezukuri)
    sx0, sx1, sy0, sy1 = hx - 16, hx + 16, -6.0, 19.0
    lattice = []
    xs = [sx0 + i * 4 for i in range(9)]
    ys = [sy0 + j * (sy1 - sy0) / 4 for j in range(5)]
    def ground_z(y):
        return max(0.3, min(top, 0.3 + (top - 0.3) * (y + 2) / 16))
    for x in xs:
        for y in ys:
            gz = ground_z(y)
            lattice.append(box(f"pil{x:.0f}_{y:.0f}", 0.9, 0.9, top + 0.9 - gz, (x, y, gz), WOOD))
    for k, zb in enumerate((3.2, 6.6, 10.0)):
        for y in ys:
            if ground_z(y) < zb:
                lattice.append(box(f"nx{k}_{y:.0f}", sx1 - sx0 + 1.2, 0.45, 0.55, ((sx0 + sx1) / 2, y, zb), shade(WOOD, -0.1)))
        for x in xs:
            yy = [y for y in ys if ground_z(y) < zb]
            if len(yy) > 1:
                lattice.append(box(f"ny{k}_{x:.0f}", 0.45, max(yy) - min(yy) + 1.2, 0.55, (x, (max(yy) + min(yy)) / 2, zb), shade(WOOD, -0.1)))
    lattice.append(box("deck", sx1 - sx0 + 2, sy1 - sy0 + 2, 0.7, ((sx0 + sx1) / 2, (sy0 + sy1) / 2, top + 0.9), "#9C8263"))
    lattice.append(box("rail_s", sx1 - sx0 + 2, 0.3, 1.1, ((sx0 + sx1) / 2, sy0 - 1, top + 1.6), WOOD))
    for s in (-1, 1):
        lattice.append(box(f"rail{s}", 0.3, sy1 - sy0 + 2, 1.1, ((sx0 + sx1) / 2 + s * ((sx1 - sx0) / 2 + 1), (sy0 + sy1) / 2, top + 1.6), WOOD))
    m.add(1, join(lattice, "stage"), "halls")
    # the Hondō: front wings toward the stage, a great cypress-bark roof
    H(m, "hondo", 36, 28, 7.5, hx, hy + 2, z=top + 0.3, plat=0, floor=1.3, roof="irimoya", roof_color=BARK, roof_h=13, bays=9, col=WOOD, wall="#DCCFB6", over=4.0)
    for s in (-1, 1):
        H(m, f"wing{s}", 8, 10, 6.0, hx + s * 22, hy - 14, z=top + 0.3, plat=0, floor=1.3, roof="irimoya", roof_color=BARK, roof_h=5.5, bays=2, col=WOOD, wall="#DCCFB6")
    # Niōmon, west gate and three-storey pagoda on the western spur, all vermilion
    G(m, "niomon", 16, 8, 5.5, 4.5, -72, 40, deg=-90, z=top + 0.3, roof=BARK, roof_h=5, bays=3, base=0.5)
    m.add(2, put(jpagoda("sanjunoto", 5.0, 3, 31.0, VERM, BARK, trim=WHITE), -42, 50, 0, top + 0.3), "roofs")
    G(m, "saimon", 10, 6, 4.5, 3.5, -50, 24, z=top + 0.3, roof=BARK, roof_h=4, bays=3, base=0.4)
    H(m, "okunoin", 16, 12, 4.5, 78, 40, z=top + 0.3, plat=0, floor=1.0, roof="irimoya", roof_color=BARK, roof_h=6, bays=4, col=WOOD)
    m.add(2, grove("forest", [(-70, 80, top), (-30, 85, top), (10, 80, top), (75, 85, top), (82, 62, top), (-60, -50, 0), (-25, -70, 0), (20, -75, 0), (60, -55, 0), (-80, -10, 0), (5, -25, 0), (80, -20, 0), (-30, 66, top)], 6.0))
    m.add(2, grove("maples", [(-15, -10, 0), (75, 2, 0), (-5, 0, 0)], 4.0, "#B0613A"))
    return m


def yasaka_shrine():
    m = Model("yasaka-shrine")
    W, D = 150, 150
    m.add(0, box("ground", W, D, 0.3, (0, 0, 0), GRAVEL), "grounds")
    m.add(0, wall_line("fence", rect_pts(W - 4, D - 4), 2.0, 0.8, VERM, TILE, closed=True))
    # Gion-zukuri main hall: sanctuary and worship hall under one great roof
    H(m, "honden", 34, 30, 6.0, 0, 15, plat=0, floor=1.4, roof="irimoya", roof_color=BARK, roof_h=13, bays=7, over=5.0)
    H(m, "maidono", 16, 12, 4.0, 0, -22, plat=0.8, roof="irimoya", roof_color=BARK, roof_h=5.5, bays=4, wall=VERM, doors=False)
    lanterns = [box(f"lant{i}{s}", 0.8, 0.8, 0.9, (s * 8.5 + (i - 1.5) * 4 * 0, -22 + (i - 1.5) * 3.4, 4.5), "#F0E4C8") for i in range(4) for s in (-1, 1)]
    m.add(2, join(lanterns, "lanterns"))
    # the vermilion west gate (Nishi Rōmon) facing down Shijō, and the south gate with a stone torii
    G(m, "nishi_romon", 12, 7, 5.0, 4.0, -W / 2 + 6, -5, deg=-90, roof=TILE, roof_h=4.5, bays=3, base=0.5)
    m.add(1, put(torii("torii", 10, 8, (0, 0, 0), STONE), 0, -64))
    m.add(1, put(small_gate("minamimon", 10, 6, 6, VERM, TILE), 0, -D / 2 + 2))
    for i, (x, y) in enumerate(((40, 30), (45, -30), (-35, 50))):
        H(m, f"massha{i}", 8, 6, 3.0, x, y, plat=0.4, roof="gable", roof_color=BARK, roof_h=2.6, bays=2, wall=VERM)
    m.add(2, grove("trees", [(-55, 55, 0), (-20, 62, 0), (25, 60, 0), (60, 55, 0), (62, 10, 0), (60, -55, 0), (-60, -55, 0), (-30, -45, 0)], 5.0))
    return m


def yasaka_pagoda():
    m = Model("yasaka-pagoda")
    m.add(0, box("ground", 30, 30, 0.3, (0, 0, 0), GRAVEL), "grounds")
    m.add(0, wall_line("fence", rect_pts(28, 28), 2.0, 0.8, CLAY, TILE, closed=True))
    m.add(1, box("base", 9, 9, 1.0, (0, 0, 0.3), STONE), "pagoda")
    m.add(2, put(jpagoda("pagoda", 6.4, 5, 45.0, WOOD, TILE), 0, 0, 0, 1.3), "pagoda")
    return m


def sanjusangendo():
    """A 120 m hall of 35 bays, facing south in the builder (east on the map), with a central porch."""
    m = Model("sanjusangendo")
    m.add(0, box("ground", 125, 24, 0.3, (0, 0, 0), GRAVEL), "grounds")
    H(m, "hall", 118, 17, 6.0, 0, 1, plat=0.9, roof="irimoya", roof_h=9.0, bays=35, over=3.0)
    m.add(1, box("veranda", 120, 2.2, 0.5, (0, -8.8, 0.9), WOOD))
    porch = [box(f"porch_p{s}", 0.6, 0.6, 5.5, (s * 5, -10.5, 0.9), VERM) for s in (-1, 1)]
    porch.append(seg_prism("porch_roof", (0, -12.5), (0, -6.0), 6.2, 13.5, 3.2, TILE))
    m.add(2, join(porch, "porch"), "roofs")
    return m


# ---------------------------------------------------------------- Fujiwara and Muromachi palaces

def shinden_mansion(name, W, D, kaisho=False, flowers=False, roof=BARK):
    """A shinden-zukuri compound: main hall, side halls on corridors, corridors running south to pond pavilions, a pond with an island."""
    m = Model(name)
    m.add(0, box("ground", W, D, 0.3, (0, 0, 0), EARTH), "grounds")
    m.add(0, wall_line("tsuiji", rect_pts(W - 2, D - 2), 3.0, 1.4, closed=True))
    py = -D * 0.25
    m.add(0, box("garden_sand", W * 0.7, D * 0.12, 0.35, (0, D * 0.02, 0.05), GRAVEL))
    m.add(0, blob("pond", W * 0.36, D * 0.15, 0.35, (0, py, 0.05), WATER, 1.1))
    m.add(0, blob("island", W * 0.08, D * 0.03, 1.0, (W * 0.05, py - 2, 0), MOSS, 0.3))
    sy = D * 0.12
    SH(m, "shinden", W * 0.22, 14, 5.2, 0, sy)
    ex = W * 0.3
    for s, nm in ((1, "higashi_tai"), (-1, "nishi_tai")):
        SH(m, nm, 16, 11, 4.6, s * ex, sy + 16, deg=-90 * s)
        m.add(1, gallery(f"watadono{s}", [(s * W * 0.11, sy + 2), (s * (ex - 6), sy + 2), (s * (ex - 6), sy + 10)], w=3.6, h=2.8, roof=roof))
        m.add(1, gallery(f"chumonro{s}", [(s * (ex + 2), sy + 8), (s * (ex + 2), py + 6)], w=3.6, h=2.8, roof=roof))
        SH(m, f"pavilion{s}", 9, 7, 3.4, s * (ex + 2), py, floor=1.2)
    SH(m, "kita_tai", W * 0.2, 12, 4.8, 0, sy + 38)
    m.add(1, gallery("wd_north", [(0, sy + 7), (0, sy + 32)], w=3.6, h=2.8, roof=roof))
    m.add(1, gallery("pond_bridge", [(-W * 0.02, py + D * 0.15), (W * 0.04, py + 2)], w=2.6, h=0.9, col=VERM, roof=VERM))
    for s in (-1, 1):
        m.add(1, put(small_gate(f"mon{s}", 8, 5, 4.5, WOOD, roof), s * (W / 2 - 1), sy + 6, 90))
    for i, (x, y) in enumerate(((-W * 0.3, D * 0.42), (W * 0.3, D * 0.42), (0, D * 0.44))):
        H(m, f"zoshi{i}", 18, 8, 3.2, x, y, plat=0.3, roof="gable", roof_color=roof, roof_h=3.0, col=WOOD, wall=CLAY, doors=False, stairs=False)
    if kaisho:
        SH(m, "kaisho", 18, 13, 4.6, -W * 0.25, D * 0.3 - 6, col=WOOD, wall="#E6DAC0")
    tc = SAKURA if flowers else PINE
    trees = [(-W * 0.38, py - D * 0.15, 0), (W * 0.38, py - D * 0.17, 0), (-W * 0.2, py - D * 0.2, 0), (W * 0.15, py - D * 0.21, 0), (-W * 0.42, py + 20, 0), (W * 0.42, py + 22, 0)]
    m.add(2, grove("trees", trees, 3.8, tc))
    if flowers:
        m.add(2, grove("trees2", [(-W * 0.4, D * 0.05, 0), (W * 0.4, D * 0.02, 0), (0, py - D * 0.2, 0)], 3.4, "#C9A2C8"))
    return m


def tsuchimikado_dono():
    return shinden_mansion("tsuchimikado-dono", 120, 220)


def hana_no_gosho():
    return shinden_mansion("hana-no-gosho", 110, 220, kaisho=True, flowers=True)


def gosho():
    """The Edo palace: Kenreimon, the Shishinden court in its corridor, Seiryōden, Kogosho and the residential halls."""
    m = Model("gosho")
    W, D = 250, 450
    m.add(0, box("ground", W, D, 0.3, (0, 0, 0), EARTH), "grounds")
    m.add(0, wall_line("wall", rect_pts(W - 2, D - 2), 4.0, 1.6, "#E9DFC9", TILE, closed=True))
    cy = -110
    m.add(0, box("court", 100, 70, 0.35, (0, cy - 10, 0.05), GRAVEL))
    m.add(1, gallery("kairo", rect_pts(120, 110, 0, cy), w=5, h=3.4, roof=BARK, closed=True), "halls")
    SH(m, "shishinden", 33, 23, 7.0, 0, cy + 30)
    m.add(1, tree("sakon_cherry", 3.2, (16, cy + 10, 0), SAKURA))
    m.add(1, tree("ukon_tachibana", 2.8, (-16, cy + 10, 0), "#4E7A3C"))
    m.add(1, put(small_gate("jomeimon", 12, 6, 6), 0, cy - 55))
    m.add(1, put(small_gate("kenreimon", 14, 7, 6.5, WOOD, BARK), 0, -D / 2 + 1))
    SH(m, "seiryoden", 30, 14, 5.8, 75, cy + 35, deg=90)
    SH(m, "kogosho", 26, 14, 5.2, 70, cy + 95)
    SH(m, "gogakumonsho", 24, 13, 5.0, 70, cy + 130)
    m.add(0, blob("oike", 34, 22, 0.35, (95, cy + 165, 0.05), WATER, 0.4))
    SH(m, "otsune", 44, 22, 6.0, -10, cy + 185)
    SH(m, "kogo", 36, 18, 5.0, -50, cy + 250)
    SH(m, "nyogo", 30, 16, 4.8, 40, cy + 265)
    for i, (x, y) in enumerate(((-75, cy + 120), (-75, cy + 160), (60, cy + 320), (-40, cy + 320))):
        SH(m, f"hall{i}", 24, 12, 4.6, x, y)
    m.add(1, gallery("link1", [(0, cy + 42), (0, cy + 174)], w=4, h=3.0, roof=BARK))
    m.add(1, gallery("link2", [(0, cy + 196), (0, cy + 300), (-50, cy + 300), (-50, cy + 259)], w=4, h=3.0, roof=BARK))
    m.add(1, gallery("link3", [(0, cy + 95), (57, cy + 95)], w=4, h=3.0, roof=BARK))
    m.add(2, grove("trees", [(-100, -200, 0), (100, -200, 0), (-105, 0, 0), (110, 40, 0), (-100, 180, 0), (100, 200, 0), (115, 120, 0), (80, 60, 0)], 5.0))
    return m


# ---------------------------------------------------------------- Zen and Pure Land temples

def shokokuji(with_pagoda=True):
    m = Model("shokokuji" if with_pagoda else "shokokuji-1750")
    W, D = 220, 260
    m.add(0, box("ground", W, D, 0.3, (0, 0, 0), GRAVEL), "grounds")
    m.add(0, wall_line("wall", rect_pts(W - 2, D - 2), 3.2, 1.4, closed=True))
    ax = -25
    m.add(0, blob("lotus_pond", 22, 9, 0.35, (ax, -95, 0.05), WATER, 0.2))
    G(m, "sanmon", 26, 12, 8.0, 6.5, ax, -70, col=WOOD, roof=TILE, roof_h=8.5, bays=5)
    if with_pagoda:
        H(m, "butsuden", 30, 26, 9.0, ax, -15, plat=1.2, roof="irimoya", roof_h=12, mokoshi=True, bays=5, col=WOOD, wall="#D9CCB2")
    H(m, "hatto", 32, 26, 9.5, ax, 45, plat=1.2, roof="irimoya", roof_h=12.5, mokoshi=True, bays=5, col=WOOD, wall="#D9CCB2")
    H(m, "hojo", 40, 24, 5.0, ax, 100, plat=0.6, roof="irimoya", roof_color=BARK, roof_h=7, bays=8, col=WOOD, wall="#E2D6BC")
    m.add(1, gallery("kairo", [(ax - 24, -70), (ax - 24, 45), (ax - 18, 45)], w=4, h=3.2, col=WOOD))
    m.add(1, gallery("kairo2", [(ax + 24, -70), (ax + 24, 45), (ax + 18, 45)], w=4, h=3.2, col=WOOD))
    if with_pagoda:
        m.add(0, box("pagoda_base", 28, 28, 1.8, (70, -40, 0.2), STONE))
        m.add(2, put(jpagoda("daito", 15.0, 7, 107.0, VERM, TILE, trim=WHITE, taper=0.93, over=0.5), 70, -40, 0, 2.0), "pagoda")
    for i, (x, y) in enumerate(((70, 60), (70, 100), (-90, 60), (-90, 100), (-90, -30))):
        H(m, f"tatchu{i}", 18, 12, 3.6, x, y, plat=0.4, roof="irimoya", roof_h=5, bays=4, col=WOOD, wall=CLAY)
    m.add(2, grove("pines", [(-95, -110, 0), (90, -110, 0), (35, -100, 0), (-80, -75, 0), (95, 10, 0), (20, 120, 0)], 5.0))
    return m


def kenninji():
    m = Model("kenninji")
    W, D = 100, 240
    m.add(0, box("ground", W, D, 0.3, (0, 0, 0), GRAVEL), "grounds")
    m.add(0, wall_line("wall", rect_pts(W - 2, D - 2), 3.0, 1.3, closed=True))
    m.add(1, put(small_gate("chokushimon", 10, 6, 6, WOOD, TILE), 0, -D / 2 + 2), "halls")
    G(m, "sanmon", 20, 10, 6.5, 5.0, 0, -75, col=WOOD, roof=TILE, roof_h=7, bays=5)
    H(m, "butsuden", 24, 20, 7.0, 0, -25, plat=1.0, roof="irimoya", roof_h=10, mokoshi=True, bays=5, col=WOOD, wall="#D9CCB2")
    H(m, "hatto", 28, 22, 7.5, 0, 22, plat=1.0, roof="irimoya", roof_h=11, mokoshi=True, bays=5, col=WOOD, wall="#D9CCB2")
    H(m, "hojo", 36, 22, 4.5, 0, 75, plat=0.6, roof="irimoya", roof_color=BARK, roof_h=7, bays=8, col=WOOD, wall="#E2D6BC")
    for i, (x, y) in enumerate(((-34, -60), (34, -60), (-34, 0), (34, 0), (-34, 60), (34, 60), (-30, 105), (30, 105))):
        m.add(0, wall_line(f"tw{i}", rect_pts(24, 30, x, y), 2.2, 0.8, CLAY, TILE, closed=True))
        H(m, f"tatchu{i}", 14, 9, 3.2, x, y + 3, plat=0.3, roof="irimoya", roof_h=4.5, bays=4, col=WOOD, wall=CLAY, doors=False)
    m.add(2, grove("pines", [(0, -100, 0), (-12, -50, 0), (12, -50, 0), (-40, -105, 0), (40, -105, 0)], 3.8))
    return m


def honganji(goeido_north=True, goeido=(62, 48), name="higashi-honganji"):
    """Two great halls side by side behind gates on the street: built facing south, turned to face east on the map (+X is north)."""
    m = Model(name)
    W, D = 240, 200
    m.add(0, box("ground", W, D, 0.3, (0, 0, 0), GRAVEL), "grounds")
    m.add(0, wall_line("wall", rect_pts(W - 2, D - 2), 3.6, 1.5, "#E8DFCB", TILE, closed=True))
    gs = 1 if goeido_north else -1
    gw, gd = goeido
    gx, ax = gs * 52, -gs * 62
    H(m, "goeido", gw, gd, 13.0, gx, 5, plat=2.2, roof="irimoya", roof_h=24, bays=11, col=WOOD, wall="#D9CCB2", over=6.5, mokoshi=False)
    H(m, "amidado", 38, 32, 9.0, ax, 10, plat=1.6, roof="irimoya", roof_h=15, bays=7, col=WOOD, wall="#D9CCB2", over=4.5)
    m.add(1, gallery("link", [(gx - gs * (gw / 2 + 2), 15), (ax + gs * 22, 15)], w=5, h=4.0, col=WOOD))
    G(m, "goeidomon", 30, 14, 9.0, 7.0, gx, -D / 2 + 10, col=WOOD, roof=TILE, roof_h=9, bays=5)
    m.add(1, put(small_gate("amidadomon", 14, 8, 8, WOOD, TILE, "irimoya"), ax, -D / 2 + 6))
    for i, (x, y) in enumerate(((gs * 60, 70), (-gs * 40, 72), (-gs * 95, 70), (0, 80))):
        H(m, f"shoin{i}", 28, 14, 3.8, x, y, plat=0.4, roof="irimoya", roof_color=BARK, roof_h=4.5, bays=6, col=WOOD, wall="#E6DCC4", doors=False)
    m.add(2, grove("ginkgo", [(gx - 30, -55, 0), (gx + 30, -55, 0), (ax, -50, 0), (-W / 2 + 12, -80, 0), (W / 2 - 12, -80, 0)], 6.0, "#7F9A4E"))
    return m


def hokoji_daibutsuden():
    """The Great Buddha hall on its stone terrace: built facing south, turned to face west on the map."""
    m = Model("hokoji-daibutsuden")
    m.add(0, box("terrace", 90, 60, 3.0, (0, 0, 0), STONE), "grounds")
    m.add(0, stair("st", 16, 3.0, 6, 6, (0, -30, 0), "S", STONE))
    H(m, "hall", 76, 46, 15.0, 0, 3, z=3.0, plat=0.6, roof="irimoya", roof_h=24, bays=11, col=WOOD, wall="#D9CCB2", mokoshi=True, over=5.0)
    return m


# ---------------------------------------------------------------- Edo works

def nijo_castle():
    """Moats, battered stone walls with white plaster on top, corner turrets, the Ninomaru palace and the Honmaru with its keep."""
    m = Model("nijo-castle")
    W, D = 500, 400
    m.add(0, box("ground", W, D, 0.3, (0, 0, 0), EARTH), "grounds")
    moat = [box("moat_s", W, 16, 0.35, (0, -D / 2 + 8, 0.05), WATER), box("moat_n", W, 16, 0.35, (0, D / 2 - 8, 0.05), WATER),
            box("moat_w", 16, D, 0.35, (-W / 2 + 8, 0, 0.05), WATER), box("moat_e", 16, D, 0.35, (W / 2 - 8, 0, 0.05), WATER)]
    m.add(0, join(moat, "moat"))
    ow, od = W - 36, D - 36
    m.add(0, wall_run("stone", rect_pts(ow, od) + [(-ow / 2, -od / 2)], 6.5, 5.0, (0, 0, 0.3), GRANITE, towers=False, merlon=None, batter=0.5))
    m.add(1, wall_line("dobei", rect_pts(ow, od), 2.2, 1.0, WHITEWASH, TILE, closed=True), "walls")
    for i, (x, y) in enumerate(((-ow / 2, -od / 2), (ow / 2, -od / 2), (ow / 2, od / 2), (-ow / 2, od / 2))):
        tur = [box(f"yag{i}a", 16, 14, 6.0, (0, 0, 0), WHITEWASH), box(f"yag{i}w", 16.2, 14.2, 0.8, (0, 0, 3.4), DARK),
               eaved_roof(f"yag{i}r1", 16, 14, 2.4, (0, 0, 6.0), TILE, over=2.0, curve=0.2),
               box(f"yag{i}b", 11, 9, 4.0, (0, 0, 7.0), WHITEWASH), irimoya(f"yag{i}r2", 11, 9, 5.0, (0, 0, 11.0), TILE, over=2.2)]
        m.add(2, put(join(tur, f"yagura{i}"), x, y, 0, 6.8), "roofs")
    # Higashi Ōtemon: the east main gate, a gatehouse bridging the wall, with an earth bridge over the moat
    m.add(0, box("east_bridge", 18, 14, 0.9, (W / 2 - 8, 70, 0.3), EARTH))
    gate = [box("otemon_b", 14, 32, 7.0, (0, 0, 0), WHITEWASH), box("otemon_dk", 14.4, 10, 5.0, (0, 0, 0), DARK), box("otemon_band", 14.2, 32.2, 0.8, (0, 0, 4.4), DARK),
            irimoya("otemon_r", 32, 14, 6.0, (0, 0, 7.0), TILE, over=2.5)]
    g = join(gate[:3], "otemon")
    r = gate[3]
    r = rot(move(r), 90)
    m.add(1, put(g, ow / 2, 70, 0, 0.3))
    m.add(2, put(r, ow / 2, 70, 0, 0.3))
    # the Ninomaru palace, its halls stepped back diagonally ('flying geese')
    for i, (x, y, w, d) in enumerate(((150, -40, 34, 26), (125, -12, 26, 22), (98, 18, 36, 28), (70, 48, 28, 22), (44, 74, 28, 22), (18, 98, 24, 20))):
        H(m, f"ninomaru{i}", w, d, 6.5, x, y, plat=0.6, roof="irimoya", roof_h=10, bays=max(4, w // 5), col=WOOD, wall="#EDE6D6", over=3.0)
    m.add(1, put(small_gate("karamon", 9, 5, 6.5, "#6A4A32", BARK, "irimoya"), 172, -78))
    m.add(0, blob("ninomaru_pond", 28, 22, 0.35, (40, 20, 0.05), WATER, 2.0))
    # the Honmaru: an inner moat and wall, a palace and the five-storey keep at its south-west corner
    hx, hy, hw, hd = -125, 0, 190, 180
    imoat = [box("imoat_s", hw + 30, 14, 0.35, (hx, hy - hd / 2 - 7, 0.05), WATER), box("imoat_n", hw + 30, 14, 0.35, (hx, hy + hd / 2 + 7, 0.05), WATER),
             box("imoat_w", 14, hd, 0.35, (hx - hw / 2 - 7, hy, 0.05), WATER), box("imoat_e", 14, hd, 0.35, (hx + hw / 2 + 7, hy, 0.05), WATER)]
    m.add(0, join(imoat, "inner_moat"))
    m.add(0, wall_run("istone", rect_pts(hw, hd, hx, hy) + [(hx - hw / 2, hy - hd / 2)], 7.5, 5.0, (0, 0, 0.3), GRANITE, towers=False, merlon=None, batter=0.5))
    m.add(0, box("honmaru_fill", hw - 4, hd - 4, 7.8, (hx, hy, 0), shade(EARTH, -0.05)))
    m.add(0, box("ibridge", 12, 16, 1.0, (hx + hw / 2 + 7, 20, 0.3), EARTH))
    for i, (x, y) in enumerate(((hx + 30, hy + 20), (hx - 10, hy + 45), (hx + 40, hy - 30))):
        H(m, f"honmaru_palace{i}", 34, 22, 6.0, x, y, z=7.8, plat=0.4, roof="irimoya", roof_h=9, bays=7, col=WOOD, wall="#EDE6D6")
    m.add(2, put(castle_keep("tenshu", 22, 18, 5, (0, 0, 0), base_h=9.0), hx - hw / 2 + 18, hy - hd / 2 + 16, 0, 7.8), "keep")
    m.add(2, grove("pines", [(-30, -150, 0), (30, -160, 0), (200, 140, 0), (-30, 150, 0), (120, 150, 0), (210, -150, 0), (-220, 160, 0)], 6.0))
    return m


def kamo_bridge(name, L, w, piers=12):
    """A timber deck on paired stone pillars with a railing capped by bronze finials (giboshi); bridge runs along X."""
    m = Model(name)
    dz = 4.2
    pil = []
    for i in range(piers + 1):
        x = -L / 2 + 6 + (L - 12) * i / piers
        for s in (-1, 1):
            pil.append(cylinder(f"pil{i}{s}", 0.75, dz, (x, s * (w / 2 - 1.0), 0), GRANITE, verts=8))
        pil.append(box(f"cap{i}", 1.4, w + 0.6, 0.6, (x, 0, dz - 0.6), WOOD))
    m.add(0, join(pil, "piers"), "piers")
    m.add(1, box("deck", L, w, 0.6, (0, 0, dz), "#9C8263"), "deck")
    m.add(1, box("abut_w", 8, w + 3, dz + 0.3, (-L / 2 + 2, 0, 0), STONE))
    m.add(1, box("abut_e", 8, w + 3, dz + 0.3, (L / 2 - 2, 0, 0), STONE))
    rail = []
    for s in (-1, 1):
        rail.append(box(f"rail{s}", L - 4, 0.25, 0.25, (0, s * (w / 2 - 0.2), dz + 1.4), WOOD))
        rail.append(box(f"rail_lo{s}", L - 4, 0.2, 0.2, (0, s * (w / 2 - 0.2), dz + 0.8), WOOD))
        for k in range(17):
            x = -L / 2 + 2 + (L - 4) * k / 16
            rail.append(box(f"rp{s}{k}", 0.35, 0.35, 1.6, (x, s * (w / 2 - 0.2), dz + 0.6), WOOD))
            if k % 4 == 0:
                rail.append(onion_dome(f"gb{s}{k}", 0.28, (x, s * (w / 2 - 0.2), dz + 2.2), "#5E7E6A", bulb=1.3, height=1.4, drum=0.2, finial=False))
    m.add(2, join(rail, "railing"), "railing")
    return m


def chion_in_sanmon():
    m = Model("chion-in-sanmon")
    m.add(0, box("ground", 55, 25, 0.3, (0, 0, 0), GRAVEL), "grounds")
    G(m, "sanmon", 46, 18, 9.0, 7.0, 0, 0, col=WOOD, wall="#DCCFB6", roof=TILE, roof_h=8.0, bays=5, base=1.2)
    for s in (-1, 1):
        stairs = [box(f"yamaro{s}", 5, 9, 9.5, (s * 25.5, 2, 0.3), "#DCCFB6"), seg_prism(f"yamaro_r{s}", (s * 25.5, -3), (s * 25.5, 7), 9.8, 7, 2.6, TILE)]
        m.add(1, join(stairs, f"yamaro{s}"))
    m.add(0, wall_line("walls", [(-27, -6), (-27, 11)], 3.0, 1.2, CLAY, TILE))
    m.add(0, wall_line("walls2", [(27, -6), (27, 11)], 3.0, 1.2, CLAY, TILE))
    return m


BUILDERS = {
    "kyoto/chodo-in": chodo_in,
    "kyoto/dairi": dairi,
    "kyoto/suzakumon": suzakumon,
    "kyoto/rashomon": rashomon,
    "kyoto/rashomon-ruin": rashomon_ruin,
    "kyoto/toji": lambda: east_west_temple(1, True),
    "kyoto/toji-800": lambda: east_west_temple(1, False, early=True),
    "kyoto/toji-kodo": toji_kodo,
    "kyoto/saiji": lambda: east_west_temple(-1, True),
    "kyoto/shinsen-en": shinsen_en,
    "kyoto/shinsen-en-small": lambda: shinsen_en(True),
    "kyoto/kiyomizu": kiyomizu,
    "kyoto/kiyomizu-800": lambda: kiyomizu(True),
    "kyoto/yasaka-shrine": yasaka_shrine,
    "kyoto/yasaka-pagoda": yasaka_pagoda,
    "kyoto/sanjusangendo": sanjusangendo,
    "kyoto/tsuchimikado-dono": tsuchimikado_dono,
    "kyoto/hana-no-gosho": hana_no_gosho,
    "kyoto/shokokuji": shokokuji,
    "kyoto/shokokuji-1750": lambda: shokokuji(False),
    "kyoto/kenninji": kenninji,
    "kyoto/nijo-castle": nijo_castle,
    "kyoto/higashi-honganji": lambda: honganji(True, (62, 48), "higashi-honganji"),
    "kyoto/nishi-honganji": lambda: honganji(False, (58, 44), "nishi-honganji"),
    "kyoto/gosho": gosho,
    "kyoto/sanjo-bridge": lambda: kamo_bridge("sanjo-bridge", 100, 8, 12),
    "kyoto/gojo-bridge": lambda: kamo_bridge("gojo-bridge", 100, 7, 10),
    "kyoto/chion-in-sanmon": chion_in_sanmon,
    "kyoto/hokoji-daibutsuden": hokoji_daibutsuden,
}
