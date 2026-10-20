"""Cairo landmark miniatures: Fustat and Babylon, Ibn Tulun, Fatimid al-Qahira, the Mamluk Citadel and Ottoman Bulaq.

Conventions as in FORMAT.md: metres, origin at the ground centre, +X east, +Y north, qibla / main front toward -Y
unless a builder says otherwise; the landmark rotation turns it on the map.
"""
import math
from chronokit import Model, box, cylinder, dome, join, shade, gable_roof, hip_roof, mesh_from
from worldkit import *

STONE, STONE_LT, STONE_DK = "#D7C29C", "#E6D9BD", "#BBA27A"
TULUN, TULUN_LT = "#C6A982", "#DCCAA8"
FATIMID, BRICK_PL = "#D3BE98", "#CDB48C"
ABLAQ_RED, MARBLE_W = "#A4604A", "#EEE7D8"
GREEN_TILE, LEAD_GREY, WOOD, MASH = "#3F7F62", "#A19E95", "#7A5A3C", "#5A4130"
SAND, PAVE, ROCK = "#D8C7A1", "#E4D7BC", "#C2AE88"
PALM, ORCHARD, FIELD = "#6E8A55", "#7E9563", "#B9B07A"
HOUSES = ["#DCCBA8", "#D2BC96", "#E3D6BC", "#C9B089", "#D8C6A6"]
FACE_ROT = {"S": 0, "N": 180, "E": 90, "W": -90}


# ---------------------------------------------------------------- helpers

def spin(o, deg):
    """Rotate about the world origin (bake the location first so the pivot is (0, 0))."""
    return rot(move(o), deg)


def place(o, x=0, y=0, deg=0):
    o = move(o)
    if deg:
        o = rot(o, deg)
    return move(o, x, y, 0)


def oct_pts(r, start=math.pi / 8):
    return [(r * math.cos(start + i * math.pi / 4), r * math.sin(start + i * math.pi / 4)) for i in range(8)]


def oct_prism(name, r, h, loc=(0, 0, 0), color=STONE):
    return prism(name, oct_pts(r), h, loc, color)


def ngon_pts(r, n, start=0.0):
    return [(r * math.cos(start + math.tau * i / n), r * math.sin(start + math.tau * i / n)) for i in range(n)]


def face_panels(name, r, n, w, h, z, loc=(0, 0, 0), color=DARK, pointed=True, every=1, start=0.0, depth=0.25):
    """Arched recesses on the faces of a regular n-gon of circumradius r whose vertices start at angle `start`."""
    x0, y0, _ = loc
    ap = r * math.cos(math.pi / n)
    out = []
    for j in range(0, n, every):
        phi = start + math.pi / n + j * math.tau / n
        p = arch_panel(f"{name}{j}", w, h, (0, 0, 0), "S", color, pointed, depth)
        p = rot(p, math.degrees(phi) + 90)
        out.append(move(p, x0 + (ap + 0.03) * math.cos(phi), y0 + (ap + 0.03) * math.sin(phi), z))
    return join(out, name)


def ground(name, w, d, color=SAND, h=0.3, loc=(0, 0, 0)):
    return box(name, w, d, h, loc, color)


def crest(name, w, d, z, loc=(0, 0), color=STONE, size=0.8):
    """Mamluk stepped cresting round the top of a w x d block."""
    return move(merlons(name, w, d, z, size, size * 0.6, color, "stepped"), loc[0], loc[1], 0)


def bands(name, w, d, z0, z1, loc=(0, 0), color=ABLAQ_RED, every=1.5, band=0.55, grow=0.12):
    """Horizontal courses of a second colour on a block (ablaq stone, brick banding)."""
    out = []
    z, k = z0, 0
    while z + band <= z1:
        out.append(box(f"{name}{k}", w + grow, d + grow, band, (loc[0], loc[1], z), color))
        z += every
        k += 1
    return join(out, name)


def windows(name, length, n, z, h, loc, face="S", fill=0.35, pointed=True, rows=1, dz=0.0):
    x, y = loc[0], loc[1]
    out = [arcade(f"{name}_{r}", length, h, n, (x, y, z + r * dz), face, DARK, pointed, fill, 0.25) for r in range(rows)]
    return join(out, name)


def mashrabiyas(name, length, n, z, h, loc, face="S", color=MASH):
    """A row of projecting turned-wood oriels on a wall face."""
    x, y = loc[0], loc[1]
    bay = length / n
    out = []
    for i in range(n):
        u = -length / 2 + bay * (i + 0.5)
        o = join([box(f"{name}{i}a", bay * 0.6, 0.9, h, (0, -0.45, 0), color),
                  box(f"{name}{i}b", bay * 0.62, 1.1, h * 0.08, (0, -0.55, h), shade(color, -0.25)),
                  box(f"{name}{i}c", bay * 0.48, 0.95, h * 0.6, (0, -0.48, h * 0.25), shade(color, -0.35))], f"{name}{i}")
        o = rot(o, FACE_ROT[face])
        dx, dy = {"S": (u, 0), "N": (u, 0), "E": (0, u), "W": (0, u)}[face]
        out.append(move(o, x + dx, y + dy, z))
    return join(out, name)


def ramp_strip(name, inner, outer, ztop, zbot, color):
    """A sloping band between two point lists (a stair or ramp winding round a tower)."""
    n = len(inner)
    verts, faces = [], []
    for i in range(n):
        verts += [(inner[i][0], inner[i][1], ztop[i]), (outer[i][0], outer[i][1], ztop[i]), (outer[i][0], outer[i][1], zbot[i]), (inner[i][0], inner[i][1], zbot[i])]
    for i in range(n - 1):
        a, b = 4 * i, 4 * (i + 1)
        faces += [(a, a + 1, b + 1, b), (a + 1, a + 2, b + 2, b + 1), (a + 2, a + 3, b + 3, b + 2), (a + 3, a, b, b + 3)]
    faces += [(0, 1, 2, 3), (4 * (n - 1) + 3, 4 * (n - 1) + 2, 4 * (n - 1) + 1, 4 * (n - 1))]
    return mesh_from(name, verts, faces, (0, 0, 0), color)


def sq_pt(f, half):
    """Point at fraction f round a square of half-side `half`, starting at the south-west corner, going east."""
    f4 = (f % 1.0) * 4
    side = min(3, int(f4))
    u = f4 - side
    c = [(-half, -half), (half, -half), (half, half), (-half, half), (-half, -half)]
    (ax, ay), (bx, by) = c[side], c[side + 1]
    return (ax + (bx - ax) * u, ay + (by - ay) * u)


def pointed_profile(r, k=1.4, bulb=0.0, n=12):
    """A pointed (two-centred) dome profile [(radius, z)] of base radius r; k > 1 makes it taller."""
    R = k * r
    phimax = math.acos(1 - r / R)
    out = []
    for i in range(n + 1):
        t = i / n
        ph = phimax * t
        x = r - R * (1 - math.cos(ph))
        z = R * math.sin(ph)
        x *= 1 + bulb * math.sin(math.pi * min(1.0, t * 1.4))
        out.append((max(0.0, x) if i < n else 0.0, z))
    return out


def finial(name, r, loc, color=BRONZE):
    x, y, z = loc
    parts = [lathe(name + "_b", [(r * 0.10, 0), (r * 0.14, r * 0.1), (r * 0.05, r * 0.22), (r * 0.11, r * 0.34), (r * 0.03, r * 0.48), (0.0, r * 0.62)], (x, y, z), color, verts=10)]
    parts.append(box(name + "_cr", r * 0.04, r * 0.04, r * 0.18, (x, y, z + r * 0.6), color))
    return join(parts, name)


def carved_dome(name, r, loc=(0, 0, 0), color=STONE, k=1.4, bulb=0.0, ribs=0, amp=0.035, base_w=None, base_h=0.0, drum_h=None, drum_color=None, windows_n=8, top=True):
    """A Cairene stone dome: square base with stepped shoulders, a drum with windows, a pointed dome (ribbed or carved)."""
    x, y, z = loc
    parts = []
    if base_w:
        parts.append(box(name + "_sq", base_w, base_w, base_h * 0.6, (x, y, z), drum_color or color))
        parts.append(oct_prism(name + "_tr", base_w / 2 / math.cos(math.pi / 8) * 0.96, base_h * 0.4, (x, y, z + base_h * 0.6), drum_color or color))
        z += base_h
    dh = r * 0.45 if drum_h is None else drum_h
    if dh > 0:
        parts.append(cylinder(name + "_drum", r * 1.04, dh, (x, y, z), drum_color or color, verts=16))
        if windows_n:
            parts.append(face_panels(name + "_dw", r * 1.04, 16, r * 0.22, dh * 0.7, z + dh * 0.12, (x, y, 0), DARK, True, 16 // windows_n))
        z += dh
    verts = max(32, ribs * 2) if ribs else 32
    prof = pointed_profile(r, k, bulb)
    d = lathe(name + "_d", prof, (x, y, z), color, verts=verts)
    if ribs:
        for v in d.data.vertices:
            dx, dy = v.co.x - x, v.co.y - y
            rr = math.hypot(dx, dy)
            if rr > 1e-3 and v.co.z > z + 0.05:
                kk = 1 + amp * math.cos(math.atan2(dy, dx) * ribs)
                v.co.x, v.co.y = x + dx * kk, y + dy * kk
    parts.append(d)
    if top:
        parts.append(finial(name + "_f", r * 0.45, (x, y, z + prof[-1][1] - r * 0.03)))
    return join(parts, name)


def mamluk_minaret(name, w, h, loc=(0, 0, 0), color=STONE, trim=STONE_LT, top="bulb", base=True, bulb_color=None, shaft="oct"):
    """A Mamluk minaret: square base, muqarnas balcony, octagonal (or round) middle, a pavilion of columns and a bulb.
    top: bulb | mabkhara | faience (a green-tiled garlic bulb)."""
    x, y, z = loc
    parts = []
    if base:
        hb = h * 0.38
        parts.append(box(name + "_b", w, w, hb, (x, y, z), color))
        for f, (dx, dy) in (("S", (0, -w / 2)), ("N", (0, w / 2)), ("E", (w / 2, 0)), ("W", (-w / 2, 0))):
            parts.append(arch_panel(f"{name}_n{f}", w * 0.3, hb * 0.26, (x + dx * 1.02, y + dy * 1.02, z + hb * 0.58), f, DARK, True, 0.2))
        z += hb
        parts.append(frustum(name + "_m1", w * 0.98, w * 0.98, w * 1.3, w * 1.3, w * 0.35, (x, y, z), trim))
        parts.append(box(name + "_p1", w * 1.3, w * 1.3, w * 0.2, (x, y, z + w * 0.35), color))
        z += w * 0.35
    ho = h * (0.27 if base else 0.5)
    r8 = w * 0.47
    if shaft == "round":
        parts.append(cylinder(name + "_o", r8, ho, (x, y, z), color, verts=16))
        parts.append(face_panels(name + "_on", r8, 8, r8 * 0.45, ho * 0.3, z + ho * 0.45, (x, y, 0), DARK, True, 2, -math.pi / 8))
    else:
        parts.append(oct_prism(name + "_o", r8, ho, (x, y, z), color))
        parts.append(face_panels(name + "_on", r8, 8, r8 * 0.45, ho * 0.3, z + ho * 0.45, (x, y, 0), DARK, True, 2, math.pi / 8))
    z += ho
    parts.append(cylinder(name + "_m2", r8, w * 0.3, (x, y, z), trim, verts=8, r_top=r8 * 1.32))
    parts.append(cylinder(name + "_p2", r8 * 1.32, w * 0.18, (x, y, z + w * 0.3), color, verts=8))
    z += w * 0.3
    if top == "mabkhara":
        rk = r8 * 0.72
        parts.append(oct_prism(name + "_k", rk, h * 0.08, (x, y, z), color))
        parts.append(face_panels(name + "_ka", rk, 8, rk * 0.5, h * 0.06, z + 0.1, (x, y, 0), DARK, True, 1, math.pi / 8))
        parts.append(carved_dome(name + "_kd", rk, (x, y, z + h * 0.08), color, k=1.6, ribs=12, amp=0.06, drum_h=0, top=True))
    elif top == "faience":
        rs = w * 0.36
        parts.append(cylinder(name + "_r", rs, h * 0.11, (x, y, z), color, verts=16))
        parts.append(cylinder(name + "_rb", rs * 1.05, w * 0.12, (x, y, z + h * 0.11), trim, verts=16))
        parts.append(onion_dome(name + "_bulb", rs * 1.05, (x, y, z + h * 0.11 + w * 0.12), bulb_color or GREEN_TILE, bulb=1.28, height=1.5, drum=0.15, finial=True, finial_color=BRONZE))
    else:
        rs = w * 0.3
        hr = h * 0.12
        parts.append(cylinder(name + "_r", rs, hr, (x, y, z), color, verts=16))
        parts.append(cylinder(name + "_m3", rs, w * 0.2, (x, y, z + hr), trim, verts=16, r_top=rs * 1.3))
        z += hr + w * 0.2
        hp = h * 0.065
        for i in range(8):
            a = math.tau * i / 8
            parts.append(cylinder(f"{name}_c{i}", w * 0.035, hp, (x + rs * 0.85 * math.cos(a), y + rs * 0.85 * math.sin(a), z), trim, verts=6))
        parts.append(cylinder(name + "_cap", rs * 1.05, w * 0.1, (x, y, z + hp), color, verts=16))
        parts.append(onion_dome(name + "_bulb", rs * 0.95, (x, y, z + hp + w * 0.1), bulb_color or color, bulb=1.22, height=1.75, drum=0.05, finial=True, finial_color=BRONZE))
    return join(parts, name)


def ghuri_minaret(name, w, h, loc=(0, 0, 0), color=STONE, trim=STONE_LT):
    """Al-Ghuri's minaret at al-Azhar: a square shaft ending in two rectangular lanterns, each with its own bulb."""
    x, y, z = loc
    parts = [box(name + "_b", w, w, h * 0.55, (x, y, z), color)]
    for f, (dx, dy) in (("S", (0, -w / 2)), ("N", (0, w / 2)), ("E", (w / 2, 0)), ("W", (-w / 2, 0))):
        parts.append(arch_panel(f"{name}_n{f}", w * 0.3, h * 0.12, (x + dx * 1.02, y + dy * 1.02, z + h * 0.3), f, DARK, True, 0.2))
    z += h * 0.55
    parts.append(frustum(name + "_m1", w, w, w * 1.3, w * 1.3, w * 0.3, (x, y, z), trim))
    z += w * 0.3
    w2 = w * 0.86
    parts.append(box(name + "_s2", w2, w2, h * 0.17, (x, y, z), color))
    parts.append(windows(name + "_w2", w2, 2, z + h * 0.04, h * 0.08, (x, y - w2 / 2 - 0.05), "S", 0.5))
    z += h * 0.17
    parts.append(frustum(name + "_m2", w2, w2, w2 * 1.25, w2 * 1.25, w * 0.25, (x, y, z), trim))
    z += w * 0.25
    for s in (-1, 1):
        cx = x + s * w2 * 0.27
        parts.append(box(f"{name}_h{s}", w2 * 0.42, w2 * 0.8, h * 0.1, (cx, y, z), color))
        parts.append(arch_panel(f"{name}_ha{s}", w2 * 0.22, h * 0.07, (cx, y - w2 * 0.4 - 0.05, z + h * 0.01), "S", DARK, True, 0.2))
        parts.append(onion_dome(f"{name}_hb{s}", w2 * 0.2, (cx, y, z + h * 0.1), color, bulb=1.2, height=1.7, drum=0.1, finial=True, finial_color=BRONZE))
    return join(parts, name)


def spiral_minaret(name, loc=(0, 0, 0), color=TULUN, side=13.5, h1=21.0, r2=4.8, h2=10.0):
    """Ibn Tulun's minaret: a square tower with a stair winding round its outside, a cylinder with a helical ramp,
    an open octagonal kiosk and a ribbed 'incense-burner' helmet."""
    x, y, z = loc
    parts = [box(name + "_sq", side, side, h1, (x, y, z), color)]
    parts.append(windows(name + "_sqw", side * 0.6, 2, z + h1 * 0.55, 3.0, (x, y - side / 2 - 0.05), "S", 0.4))
    half, wd = side / 2, 2.0
    n = 48
    fr = [i / n for i in range(n + 1)]
    inner = [(x + sq_pt(f, half)[0], y + sq_pt(f, half)[1]) for f in fr]
    outer = [(x + sq_pt(f, half + wd)[0], y + sq_pt(f, half + wd)[1]) for f in fr]
    para = [(x + sq_pt(f, half + wd - 0.35)[0], y + sq_pt(f, half + wd - 0.35)[1]) for f in fr]
    zt = [z + h1 * f for f in fr]
    parts.append(ramp_strip(name + "_st", inner, outer, zt, [max(z, t - 1.2) for t in zt], shade(color, -0.22)))
    parts.append(ramp_strip(name + "_pa", para, outer, [t + 1.1 for t in zt], [max(z, t - 0.2) for t in zt], shade(color, 0.12)))
    z += h1
    parts.append(box(name + "_plat", side + 0.6, side + 0.6, 0.6, (x, y, z), shade(color, 0.08)))
    parts.append(cylinder(name + "_cy", r2, h2, (x, y, z), color, verts=24))
    m = 40
    ang = [math.tau * i / m - math.pi / 2 for i in range(m + 1)]
    inner2 = [(x + r2 * math.cos(a), y + r2 * math.sin(a)) for a in ang]
    outer2 = [(x + (r2 + 1.6) * math.cos(a), y + (r2 + 1.6) * math.sin(a)) for a in ang]
    zt2 = [z + h2 * i / m for i in range(m + 1)]
    parts.append(ramp_strip(name + "_ra", inner2, outer2, zt2, [t - 1.0 for t in zt2], shade(color, -0.22)))
    para2 = [(x + (r2 + 1.3) * math.cos(a), y + (r2 + 1.3) * math.sin(a)) for a in ang]
    parts.append(ramp_strip(name + "_rp", para2, outer2, [t + 1.0 for t in zt2], [t - 0.2 for t in zt2], shade(color, 0.12)))
    z += h2
    rk = 3.0
    parts.append(oct_prism(name + "_k", rk, 4.4, (x, y, z), color))
    parts.append(face_panels(name + "_ka", rk, 8, rk * 0.5, 3.4, z + 0.3, (x, y, 0), DARK, True, 1, math.pi / 8))
    parts.append(carved_dome(name + "_hd", rk, (x, y, z + 4.4), color, k=1.7, ribs=16, amp=0.07, drum_h=0.6, windows_n=0))
    return join(parts, name)


def court_mosque(name, w, d, h, hall_d, side_d, back_d, color, loc=(0, 0, 0), bays=None, roof=None, crest_color=None, ext_windows=True):
    """A Cairene courtyard mosque: outer walls with cresting, a deep prayer hall on the qibla (south) side, arcades round the court.
    Returns (shell, interior) so they can rise in separate stages."""
    x0, y0, z0 = loc
    t = 1.6
    shell = [box(name + "_ws", w, t, h, (x0, y0 - d / 2 + t / 2, z0), color), box(name + "_wn", w, t, h, (x0, y0 + d / 2 - t / 2, z0), color),
             box(name + "_ww", t, d - 2 * t, h, (x0 - w / 2 + t / 2, y0, z0), color), box(name + "_we", t, d - 2 * t, h, (x0 + w / 2 - t / 2, y0, z0), color)]
    shell.append(crest(name + "_cr", w, d, z0 + h, (x0, y0), crest_color or color, 0.8))
    if ext_windows:
        nw, nd = max(3, int(w / 7)), max(3, int(d / 7))
        shell.append(windows(name + "_xs", w * 0.9, nw, z0 + h * 0.5, h * 0.3, (x0, y0 - d / 2 - 0.02), "S"))
        shell.append(windows(name + "_xn", w * 0.9, nw, z0 + h * 0.5, h * 0.3, (x0, y0 + d / 2 + 0.02), "N"))
        shell.append(windows(name + "_xw", d * 0.9, nd, z0 + h * 0.5, h * 0.3, (x0 - w / 2 - 0.02, y0), "W"))
        shell.append(windows(name + "_xe", d * 0.9, nd, z0 + h * 0.5, h * 0.3, (x0 + w / 2 + 0.02, y0), "E"))
    rh = h - 1.2
    rc = roof or shade(color, 0.12)
    yA = y0 - d / 2 + t + hall_d
    yB = y0 + d / 2 - t - back_d
    cw = w - 2 * t - 2 * side_d
    inner = [box(name + "_hall", w - 2 * t, hall_d, rh, (x0, y0 - d / 2 + t + hall_d / 2, z0), rc),
             box(name + "_back", w - 2 * t, back_d, rh, (x0, y0 + d / 2 - t - back_d / 2, z0), rc)]
    for s in (-1, 1):
        inner.append(box(f"{name}_side{s}", side_d, yB - yA, rh, (x0 + s * (w / 2 - t - side_d / 2), (yA + yB) / 2, z0), rc))
    inner.append(box(name + "_pave", cw, yB - yA, 0.15, (x0, (yA + yB) / 2, z0), PAVE))
    nb = bays or max(4, int(cw / 5))
    nd = max(3, int((yB - yA) / 5))
    ah = rh * 0.78
    inner.append(arcade(name + "_ah", cw, ah, nb, (x0, yA + 0.05, z0), "N", DARK, True, 0.72))
    inner.append(arcade(name + "_ab", cw, ah, nb, (x0, yB - 0.05, z0), "S", DARK, True, 0.72))
    inner.append(arcade(name + "_aw", yB - yA, ah, nd, (x0 - cw / 2 + 0.05, (yA + yB) / 2, z0), "E", DARK, True, 0.72))
    inner.append(arcade(name + "_ae", yB - yA, ah, nd, (x0 + cw / 2 - 0.05, (yA + yB) / 2, z0), "W", DARK, True, 0.72))
    return join(shell, name + "_shell"), join(inner, name + "_inner")


def fortress_gate(name, w, d, h, loc=(0, 0, 0), face="S", color=STONE, towers="square", tower_w=None, belvedere=False, trim=STONE_LT):
    """A gate block with a tall arched passage between two towers (square or half-round)."""
    x, y, z = loc
    tw = tower_w or w * 0.36
    parts = [box(name + "_c", w - tw, d * 0.8, h * 0.85, (0, d * 0.1, 0), color)]
    parts.append(arch_panel(name + "_a", (w - 2 * tw) * 0.75 + 1.0, h * 0.62, (0, -d * 0.3 - 0.05, 0), "S", DARK, True, 0.4))
    parts.append(arch_panel(name + "_ab", (w - 2 * tw) * 0.75 + 1.0, h * 0.62, (0, d / 2 + 0.05, 0), "N", DARK, True, 0.4))
    for s in (-1, 1):
        cx = s * (w / 2 - tw / 2)
        if towers == "round":
            parts.append(box(f"{name}_tb{s}", tw, d * 0.6, h, (cx, d * 0.2, 0), color))
            parts.append(cylinder(f"{name}_tr{s}", tw / 2, h, (cx, -d / 2 + tw / 2, 0), color, verts=20))
            parts.append(arch_panel(f"{name}_tn{s}", tw * 0.22, h * 0.18, (cx, -d / 2 - 0.05, h * 0.62), "S", DARK, True, 0.2))
        else:
            parts.append(box(f"{name}_t{s}", tw, d, h, (cx, 0, 0), color))
            parts.append(arch_panel(f"{name}_tn{s}", tw * 0.22, h * 0.18, (cx, -d / 2 - 0.05, h * 0.62), "S", DARK, True, 0.2))
        parts.append(box(f"{name}_tp{s}", tw + 0.4, (d if towers != "round" else d * 0.6) + 0.4, 0.5, (cx, 0 if towers != "round" else d * 0.2, h), trim))
    parts.append(box(name + "_band", w - 2 * tw + 0.2, 0.3, 0.7, (0, -d * 0.3 - 0.15, h * 0.72), trim))
    if belvedere:
        bw = w * 0.5
        parts.append(box(name + "_bv", bw, d * 0.6, h * 0.35, (0, d * 0.1, h * 0.85), color))
        parts.append(arcade(name + "_bva", bw * 0.9, h * 0.25, 4, (0, d * 0.1 - d * 0.3 - 0.05, h * 0.87), "S", DARK, True, 0.7))
        parts.append(carved_dome(name + "_bvd", bw * 0.22, (0, d * 0.1, h * 1.2), FATIMID, k=1.5, ribs=12, drum_h=0, windows_n=0))
    o = join(parts, name)
    o = rot(move(o), FACE_ROT[face])
    return move(o, x, y, z)


def boat(name, length, loc=(0, 0, 0), deg=0, sail=True, hull=WOOD, cloth="#EDE4CF"):
    """A Nile boat: a pointed hull, a raked mast and a big lateen sail."""
    L, W = length, length * 0.24
    pts = [(-L / 2, 0), (-L * 0.3, -W / 2), (L * 0.3, -W / 2), (L / 2, 0), (L * 0.3, W / 2), (-L * 0.3, W / 2)]
    parts = [prism(name + "_h", pts, L * 0.1, (0, 0, 0), hull), box(name + "_d", L * 0.6, W * 0.7, L * 0.02, (0, 0, L * 0.1), shade(hull, 0.25))]
    if sail:
        parts.append(cylinder(name + "_m", L * 0.02, L * 0.55, (L * 0.12, 0, L * 0.1), WOOD, verts=6))
        verts = [(L * 0.12, 0.05, L * 0.22), (-L * 0.42, 0.05, L * 0.18), (L * 0.5, 0.05, L * 0.95)]
        parts.append(mesh_from(name + "_s", verts + [(v[0], -0.05, v[2]) for v in verts], [(0, 1, 2), (5, 4, 3), (0, 3, 4, 1), (1, 4, 5, 2), (2, 5, 3, 0)], (0, 0, 0), cloth))
    else:
        parts.append(box(name + "_cab", L * 0.25, W * 0.6, L * 0.12, (-L * 0.15, 0, L * 0.1), shade(hull, 0.15)))
    o = join(parts, name)
    return place(o, loc[0], loc[1], deg)


def palms(name, spots, r=2.0, z=0.3):
    return join([tree(f"{name}{i}", r, (x, y, z), PALM, TIMBER, "palm") for i, (x, y) in enumerate(spots)], name)


def houses(name, specs, z=0.3, mash=True):
    """Plain flat-roofed houses: specs = [(x, y, w, d, h), ...]; tall ones get a row of mashrabiyas."""
    out = []
    for i, (x, y, w, d, h) in enumerate(specs):
        c = HOUSES[i % len(HOUSES)]
        out.append(flat_house(f"{name}{i}", w, d, h, (x, y, z), c, True, "S"))
        if mash and h >= 8 and w >= 6:
            out.append(mashrabiyas(f"{name}m{i}", w * 0.8, max(1, int(w / 4)), z + h * 0.55, h * 0.25, (x, y - d / 2 - 0.02), "S"))
    return join(out, name)


# ---------------------------------------------------------------- Fustat and Babylon

def amr_mosque(variant="827"):
    m = Model("amr-mosque")
    m.add(0, ground("amr_g", 120, 112, SAND), "ground")
    if variant == "700":
        shell, inner = court_mosque("amr", 74, 62, 8, 22, 8, 8, "#CDB792", (0, -8, 0), roof="#C8B08A")
        m.add(0, shell, "walls")
        m.add(1, inner, "halls")
        towers = [box(f"amr_t{i}", 4, 4, 13, (sx * 35, -8 + sy * 29, 0), "#C4AC86") for i, (sx, sy) in enumerate([(-1, -1), (1, -1), (1, 1), (-1, 1)])]
        towers += [box(f"amr_tp{i}", 4.6, 4.6, 0.6, (sx * 35, -8 + sy * 29, 13), "#B89F78") for i, (sx, sy) in enumerate([(-1, -1), (1, -1), (1, 1), (-1, 1)])]
        m.add(2, join(towers, "amr_towers"), "towers")
        m.add(2, palms("amr_palm", [(-50, 40), (-44, 46), (48, 42), (52, 30), (-52, -44), (50, -46), (0, 44), (12, 48)], 2.2))
        m.add(2, houses("amr_h", [(-46, 38, 10, 8, 6), (46, 40, 9, 9, 7), (-50, -46, 8, 8, 5)], mash=False))
        return m
    shell, inner = court_mosque("amr", 118, 110, 11, 42, 16, 12, "#DDCFB2", (0, 0, 0))
    m.add(0, shell, "walls")
    m.add(1, inner, "halls")
    yc = (-55 + 1.6 + 42 + 55 - 1.6 - 12) / 2
    parts = [box("amr_fb", 8, 8, 4.5, (0, yc, 0.15), "#E6DBC2"), face_panels("amr_fa", 8 / 2 / math.cos(math.pi / 4), 4, 3.6, 3.6, 0.15, (0, yc, 0), DARK, True, 1, math.pi / 4)]
    parts.append(carved_dome("amr_fd", 4.0, (0, yc, 4.65), "#E6DBC2", k=1.2, drum_h=0.6, windows_n=0))
    for i, (sx, sy) in enumerate([(-1, -1), (1, -1), (1, 1), (-1, 1)]):
        parts.append(box(f"amr_t{i}", 4.4, 4.4, 15, (sx * 57, sy * 53, 0), "#D3C3A2"))
        parts.append(carved_dome(f"amr_tc{i}", 1.8, (sx * 57, sy * 53, 15), "#D3C3A2", k=1.5, drum_h=0.4, windows_n=0))
    parts.append(arch_panel("amr_door", 5, 7.5, (0, 55.05, 0), "N", DARK, True, 0.4))
    m.add(2, join(parts, "amr_top"), "fountain")
    return m


def babylon():
    m = Model("babylon")
    m.add(0, ground("bab_g", 180, 260, SAND), "ground")
    wall_c, brick = "#D9C9A8", "#A86B4E"
    pts = [(-88, -128), (88, -128), (88, 128), (-88, 128), (-88, -128)]
    walls = [wall_run("bab_w", pts, 13, 3.4, color=wall_c, towers=True, tower_r=5.5, tower_every=34, merlon="box")]
    for i in range(4):
        (ax, ay), (bx, by) = pts[i], pts[i + 1]
        L = math.hypot(bx - ax, by - ay)
        for k, zb in enumerate((2.5, 5.5, 8.5, 11.5)):
            walls.append(box(f"bab_band{i}_{k}", L if ay == by else 3.8, 3.8 if ay == by else L, 0.6, ((ax + bx) / 2, (ay + by) / 2, zb), brick))
    m.add(1, join(walls, "bab_walls"), "walls")
    towers = []
    for i, ty in enumerate((12, -38)):
        towers.append(cylinder(f"bab_rt{i}", 12, 16, (-86, ty, 0), wall_c, verts=28))
        towers += [cylinder(f"bab_rtb{i}_{k}", 12.25, 0.6, (-86, ty, zb), brick, verts=28) for k, zb in enumerate((3, 6.5, 10, 13.5))]
        towers.append(face_panels(f"bab_rtw{i}", 12, 12, 1.4, 2.4, 11, (-86, ty, 0), DARK, False, 2))
    towers.append(cylinder("bab_church_d", 5, 3, (-86, 12, 16), STONE_LT, verts=20))
    towers.append(carved_dome("bab_george", 4.6, (-86, 12, 19), STONE_LT, k=1.1, drum_h=0.5, windows_n=0))
    towers.append(arch_panel("bab_irongate", 6, 9, (-88.4, -13, 0), "W", DARK, False, 0.5))
    # the south gatehouse carrying the Hanging Church
    towers.append(box("bab_sg", 34, 24, 14, (-48, -121, 0), wall_c))
    towers.append(bands("bab_sgb", 34, 24, 3, 14, (-48, -121), brick, 3.0, 0.6))
    m.add(2, join(towers, "bab_towers"), "towers")
    white = "#F0E9DA"
    ch = [box("hang_base", 26, 30, 1.0, (-48, -119, 14), STONE_LT), box("hang_body", 22, 26, 8.5, (-48, -119, 15), white)]
    for k, dx in enumerate((-7.2, 0, 7.2)):
        ch.append(gable_roof(f"hang_r{k}", 6.8, 26, 3.0, (-48 + dx, -119, 23.5), "#8E6A4A", 0.3))
    ch.append(windows("hang_w", 26, 5, 17, 3.6, (-48 - 11.05, -119), "W"))
    ch.append(windows("hang_we", 26, 5, 17, 3.6, (-48 + 11.05, -119), "E"))
    ch.append(arch_panel("hang_door", 3.5, 5.5, (-48, -106.05, 15), "N", DARK, True, 0.3))
    ch.append(stair("hang_st", 5, 14, 18, 14, (-48, -97, 0), "N", wall_c))
    for s2 in (-1, 1):
        ch.append(box(f"hang_bell{s2}", 4.2, 4.2, 13, (-48 + s2 * 8.5, -105, 15), white))
        ch.append(arch_panel(f"hang_bella{s2}", 2.0, 3.4, (-48 + s2 * 8.5, -102.85, 23.5), "N", DARK, True, 0.2))
        ch.append(cylinder(f"hang_bellc{s2}", 2.6, 3.0, (-48 + s2 * 8.5, -105, 28), "#8E6A4A", verts=8, r_top=0))
        ch.append(box(f"hang_cross{s2}", 0.3, 0.3, 1.6, (-48 + s2 * 8.5, -105, 31), BRONZE))
    # Abu Serga, St Barbara and the houses of Qasr al-Sham'
    for k, (cx, cy, w, d, h) in enumerate([(14, -30, 15, 28, 8), (46, -62, 13, 24, 7.5), (-20, 64, 12, 20, 7)]):
        ch.append(box(f"ch{k}", w, d, h, (cx, cy, 0.3), "#E4D9C2"))
        ch.append(gable_roof(f"ch{k}r", w, d, w * 0.25, (cx, cy, h + 0.3), "#9A7A58", 0.3))
        ch.append(box(f"ch{k}a", w * 0.55, 4, h * 0.75, (cx, cy + d / 2 + 2, 0.3), "#E4D9C2"))
    ch.append(houses("bab_h", [(-55, 30, 14, 12, 8), (-40, 70, 12, 14, 9), (40, 40, 16, 12, 10), (55, 95, 14, 14, 8), (10, 100, 18, 12, 9), (-50, -40, 12, 16, 7),
                                (50, 5, 12, 12, 8), (-15, -85, 14, 10, 7), (30, -105, 12, 10, 6), (-60, 100, 12, 12, 7), (65, -20, 10, 14, 7), (-25, 20, 10, 10, 6),
                                (-60, 0, 14, 12, 9), (-20, -50, 12, 14, 8), (70, 60, 12, 16, 9), (25, 75, 14, 10, 8), (-40, 105, 14, 10, 8), (70, -110, 12, 10, 7),
                                (-10, 40, 12, 12, 9), (40, -10, 10, 12, 7), (-65, -80, 12, 14, 8), (0, -110, 12, 10, 7), (65, 115, 12, 8, 7), (-30, -15, 10, 10, 7)]))
    ch.append(palms("bab_palm", [(0, 10), (-30, -60), (30, 70), (60, -100), (-70, 60)], 2.2))
    m.add(3, join(ch, "bab_churches"), "churches")
    return m


def nilometer():
    m = Model("nilometer")
    m.add(0, box("nil_quay", 18, 18, 0.8, (0, 0, 0), STONE_DK), "quay")
    m.add(0, stair("nil_steps", 6, 0.8, 3, 4, (-9, 0, 0), "W", STONE_DK))
    body = [box("nil_body", 9, 9, 6.5, (0, 0, 0.8), STONE_LT), cornice("nil_corn", 9, 9, 7.3, 0.5, 0.35, STONE)]
    for f, (dx, dy) in (("S", (0, -4.5)), ("N", (0, 4.5)), ("E", (4.5, 0)), ("W", (-4.5, 0))):
        body.append(arch_panel(f"nil_w{f}", 2.4, 4.2, (dx * 1.01, dy * 1.01, 0.8), f, DARK, True, 0.3))
    body.append(box("nil_rail", 15, 15, 0.9, (0, 0, 0.8), STONE))
    body.append(box("nil_rail_in", 13.6, 13.6, 1.0, (0, 0, 0.8), STONE_DK))
    m.add(1, join(body, "nil_house"), "well-house")
    m.add(2, cylinder("nil_roof", 5.6, 4.6, (0, 0, 7.8), "#B3A58A", verts=16, r_top=0.0), "roof")
    m.add(2, finial("nil_fin", 1.6, (0, 0, 12.2)))
    return m


# ---------------------------------------------------------------- Tulunid

def ibn_tulun():
    m = Model("ibn-tulun")
    m.add(0, ground("tul_g", 162, 162, "#D6C49E"), "ground")
    zw = [wall_run("tul_ziy", [(61, -81), (81, -81), (81, 81), (-81, 81), (-81, -81), (-61, -81)], 9, 1.6, color=TULUN, towers=False, merlon="box")]
    for f, loc in (("W", (-81.05, 0)), ("E", (81.05, 0)), ("N", (0, 81.05))):
        zw.append(windows(f"tul_zd{f}", 120, 5, 0.3, 5.5, loc, f, 0.25))
    m.add(0, join(zw, "tul_ziyadas"))
    shell, inner = court_mosque("tul", 122, 140, 13, 37, 15, 11, TULUN, (0, -11, 0), bays=13, roof=TULUN_LT)
    m.add(1, shell, "mosque")
    m.add(1, inner)
    yc = 2.0
    f = [box("tul_fb", 13, 13, 7, (0, yc, 0.15), TULUN_LT)]
    for side in ("S", "N", "E", "W"):
        dx, dy = {"S": (0, -6.55), "N": (0, 6.55), "E": (6.55, 0), "W": (-6.55, 0)}[side]
        f.append(arcade(f"tul_fa{side}", 11, 5.2, 3, (dx, yc + dy, 0.15), side, DARK, True, 0.7))
    f.append(cornice("tul_fc", 13, 13, 7.15, 0.4, 0.3, TULUN))
    f.append(carved_dome("tul_fd", 5.4, (0, yc, 7.5), TULUN_LT, k=1.25, base_w=12.4, base_h=2.4, drum_h=1.2, windows_n=8))
    m.add(2, join(f, "tul_fountain"), "fountain")
    m.add(2, carved_dome("tul_mihd", 4.2, (0, -77, 11.8), TULUN_LT, k=1.35, base_w=9, base_h=2.0, drum_h=0.8, windows_n=8))
    m.add(3, spiral_minaret("tul_min", (0, 71, 0), TULUN), "minaret")
    br = [box("tul_br", 3.2, 6.2, 11.5, (0, 61.6, 0), TULUN), arch_panel("tul_bra", 2.6, 7, (-1.65, 61.6, 0), "W", DARK, False, 0.4),
          arch_panel("tul_brb", 2.6, 7, (1.65, 61.6, 0), "E", DARK, False, 0.4)]
    m.add(3, join(br, "tul_bridge"))
    return m


def tulunid_palace():
    m = Model("tulunid-palace")
    m.add(0, ground("tp_g", 380, 260, "#D2BF98"), "ground")
    m.add(0, box("tp_maydan", 196, 236, 0.45, (88, 0, 0), "#CBB68C"))
    w = [wall_run("tp_wall", [(-188, -128), (-12, -128), (-12, 128), (-188, 128), (-188, -128)], 9, 2.4, color=BRICK_PL, tower_r=3.6, tower_every=36),
         wall_run("tp_mw", [(-12, -120), (186, -120), (186, 120), (-12, 120)], 3, 1.2, color=BRICK_PL, towers=False, merlon=None)]
    w.append(fortress_gate("tp_gate", 26, 14, 13, (-100, -128, 0), "S", BRICK_PL, "square"))
    m.add(1, join(w, "tp_walls"), "walls")
    b = [courtyard_ring("tp_c1", 64, 56, 8, 9, (-140, -70, 0.3), BRICK_PL), courtyard_ring("tp_c2", 56, 50, 8, 8, (-60, -75, 0.3), BRICK_PL),
         charbagh("tp_garden", 70, 80, (-140, 55, 0.3), path_color=BRICK_PL), courtyard_ring("tp_c3", 50, 60, 9, 9, (-55, 60, 0.3), BRICK_PL)]
    b.append(box("tp_hall", 40, 30, 14, (-95, -10, 0.3), "#D9C3A0"))
    b.append(arcade("tp_hall_a", 34, 9, 5, (-95, -25.05, 0.3), "S", DARK, True, 0.7))
    b.append(houses("tp_h", [(-170, 0, 18, 30, 9), (-30, 0, 20, 30, 10), (-170, 110, 20, 12, 7), (-30, -115, 22, 10, 7)], mash=False))
    m.add(2, join(b, "tp_halls"), "palace")
    t = [carved_dome("tp_golden", 9.5, (-95, -10, 14.3), GILT, k=1.25, drum_h=2.0, drum_color="#D9C3A0")]
    pv = [box("tp_pav", 18, 12, 8, (-2, 0, 0.3), "#D9C3A0"), arcade("tp_pava", 16, 6, 4, (7.05, 0, 3), "E", DARK, True, 0.7),
          carved_dome("tp_pavd", 4.5, (-2, 0, 8.3), "#D9C3A0", k=1.3, drum_h=0.6, windows_n=0)]
    t.append(join(pv, "tp_pavilion"))
    t.append(join([cylinder(f"tp_post{i}", 0.5, 3, (x, 0, 0.45), WOOD, verts=6) for i, x in enumerate((20, 170))], "tp_posts"))
    t.append(palms("tp_palm", [(-180, -110), (-20, 110), (60, 112), (120, 112), (180, 112), (60, -112), (120, -112), (180, -112), (-170, 120), (-60, 118)], 2.6))
    m.add(3, join(t, "tp_domes"), "domes")
    return m


# ---------------------------------------------------------------- Fatimid al-Qahira

def al_azhar(variant="1350"):
    m = Model("al-azhar")
    m.add(0, ground("az_g", 100, 95, SAND), "ground")
    col = "#DED1B4"
    shell, inner = court_mosque("az", 86, 76, 11, 28, 9, 9, col, (0, -9.5, 0), bays=11)
    m.add(0, shell, "walls")
    m.add(1, inner, "arcades")
    yh = -47.5 + 1.6 + 14
    top = [box("az_transept", 9, 28, 13.5, (0, yh, 0), shade(col, 0.1)), crest("az_tcr", 9, 28, 13.5, (0, yh), col, 0.6),
           iwan("az_tiwan", 9, 13.5, 1.2, (0, yh + 14 + 0.6, 0), "N", col, STONE_LT)]
    top.append(carved_dome("az_mihd", 4.0, (0, -42, 13.5), col, k=1.55, ribs=14, amp=0.06, drum_h=1.0, windows_n=8))
    top.append(carved_dome("az_hafd", 3.6, (0, yh + 9, 13.5), col, k=1.55, ribs=14, amp=0.06, drum_h=1.0, windows_n=8))
    for s in (-1, 1):
        top.append(carved_dome(f"az_cd{s}", 3.0, (s * 36, -42, 9.8), col, k=1.5, ribs=12, amp=0.06, drum_h=0.6, windows_n=0))
    m.add(2, join(top, "az_domes"), "domes")
    yf = 28.5
    if variant == "972":
        p = [box("az_portal", 11, 4, 13, (0, yf + 2, 0), col), arch_panel("az_pa", 4, 8.5, (0, yf + 4.05, 0), "N", DARK, True, 0.4),
             box("az_fm", 4.2, 4.2, 6, (0, yf + 2, 13), col), oct_prism("az_fmo", 2.2, 3.5, (0, yf + 2, 19), col),
             carved_dome("az_fmd", 2.0, (0, yf + 2, 22.5), col, k=1.5, ribs=10, drum_h=0, windows_n=0)]
        m.add(3, join(p, "az_fatimid_minaret"), "minaret")
        m.add(3, palms("az_palm", [(-40, 40), (-25, 42), (30, 41), (42, 38)], 2.0))
        return m
    mad = []
    for k, (cx, dome_r) in enumerate(((-28, 4.5), (28, 5.0))):
        mad.append(box(f"az_mad{k}", 30, 17, 12, (cx, yf + 9, 0), STONE))
        mad.append(crest(f"az_madcr{k}", 30, 17, 12, (cx, yf + 9), STONE, 0.6))
        mad.append(windows(f"az_madw{k}", 26, 4, 3.5, 5.5, (cx, yf + 17.55), "N", 0.4))
        mad.append(carved_dome(f"az_madd{k}", dome_r, (cx + (8 if k else -8), yf + 9, 12), STONE, k=1.4, ribs=24 if k else 0, amp=0.03, base_w=dome_r * 2.2, base_h=2.0, drum_h=1.2))
    mad.append(box("az_gate", 14, 10, 15, (0, yf + 12, 0), STONE))
    mad.append(iwan("az_gatei", 9, 15, 1.2, (0, yf + 17.6, 0), "N", STONE, STONE_LT))
    mad.append(bands("az_gateb", 14, 10, 1.0, 14, (0, yf + 12), ABLAQ_RED, 1.8, 0.5))
    m.add(2, join(mad, "az_madrasas"))
    mins = [mamluk_minaret("az_aqbugha", 4.6, 40, (14, yf + 14, 0), STONE, STONE_LT, "bulb")]
    if variant == "1600":
        mins.append(mamluk_minaret("az_qaitbay", 4.8, 46, (-9, yf + 15, 0), STONE, STONE_LT, "bulb"))
        mins.append(ghuri_minaret("az_ghuri", 6.0, 52, (-38, -2, 0), STONE, STONE_LT))
    m.add(3, join(mins, "az_minarets"), "minarets")
    return m


def eastern_palace():
    m = Model("eastern-palace")
    m.add(0, ground("ep_g", 260, 360, "#D6C49F"), "ground")
    pts = [(-126, -176), (126, -176), (126, 176), (-126, 176), (-126, -176)]
    w = [wall_run("ep_wall", pts, 14, 3, color=FATIMID, tower_r=4.0, tower_every=48, merlon="box", tower_shape="square")]
    w.append(fortress_gate("ep_golden", 34, 16, 17, (-126, 0, 0), "W", FATIMID, "square", belvedere=True))
    w.append(fortress_gate("ep_gn", 22, 12, 15, (-40, 176, 0), "N", FATIMID, "square"))
    w.append(fortress_gate("ep_ge", 22, 12, 15, (126, 40, 0), "E", FATIMID, "square"))
    w.append(fortress_gate("ep_gs", 22, 12, 15, (-30, -176, 0), "S", FATIMID, "square"))
    w.append(fortress_gate("ep_gw2", 22, 12, 15, (-126, 120, 0), "W", FATIMID, "square"))
    m.add(1, join(w, "ep_walls"), "walls")
    c = [courtyard_ring("ep_c1", 80, 64, 10, 11, (50, 70, 0.3), FATIMID), courtyard_ring("ep_c2", 76, 60, 10, 11, (50, -60, 0.3), FATIMID),
         courtyard_ring("ep_c3", 64, 54, 9, 9, (-60, -125, 0.3), FATIMID), charbagh("ep_garden", 70, 74, (-55, 85, 0.3), path_color=FATIMID)]
    c.append(box("ep_hall", 52, 38, 17, (-50, -30, 0.3), "#DCC9A6"))
    c.append(arcade("ep_halla", 46, 11, 7, (-50 + 26.05, -30, 0.3), "E", DARK, True, 0.7))
    c.append(crest("ep_hallc", 52, 38, 17.3, (-50, -30), FATIMID, 0.7))
    c.append(houses("ep_h", [(60, 145, 40, 20, 12), (-10, 150, 30, 16, 10), (-95, 150, 26, 18, 9), (95, 0, 22, 30, 11), (5, 10, 22, 26, 12), (100, -130, 30, 26, 9),
                              (10, -110, 26, 20, 10), (-100, -60, 22, 26, 9), (-100, 30, 18, 24, 8), (40, 5, 26, 20, 9)], mash=False))
    m.add(2, join(c, "ep_courts"), "courts")
    d = [carved_dome("ep_throne", 10, (-50, -30, 17.3), FATIMID, k=1.5, ribs=20, amp=0.04, drum_h=2.5, windows_n=8)]
    d.append(box("ep_tomb", 18, 18, 11, (75, -150, 0.3), "#DCC9A6"))
    d.append(carved_dome("ep_tombd", 7.5, (75, -150, 11.3), FATIMID, k=1.5, ribs=16, amp=0.05, drum_h=1.2))
    for k, (bx, by, bz) in enumerate(((50, 97, 10.3), (83, -60, 10.3), (60, 145, 12.9))):
        d.append(box(f"ep_bv{k}", 10, 10, 6, (bx, by, bz), FATIMID))
        d.append(arcade(f"ep_bva{k}", 9, 4.5, 3, (bx, by - 5.05, bz), "S", DARK, True, 0.7))
        d.append(carved_dome(f"ep_bvd{k}", 3.6, (bx, by, bz + 6), FATIMID, k=1.5, ribs=12, drum_h=0, windows_n=0))
    d.append(palms("ep_palm", [(-110, 60), (-110, 110), (100, 120), (110, 160), (-110, -150), (110, -100)], 2.6))
    m.add(3, join(d, "ep_domes"), "domes")
    return m


def western_palace():
    m = Model("western-palace")
    m.add(0, ground("wp_g", 150, 200, "#D6C49F"), "ground")
    w = [wall_run("wp_wall", [(-73, -98), (73, -98), (73, 98), (-73, 98), (-73, -98)], 12, 2.6, color=FATIMID, tower_r=3.6, tower_every=45, tower_shape="square")]
    w.append(fortress_gate("wp_gate", 30, 14, 15, (73, 0, 0), "E", FATIMID, "square", belvedere=True))
    m.add(1, join(w, "wp_walls"), "walls")
    c = [courtyard_ring("wp_c1", 70, 60, 9, 10, (10, 50, 0.3), FATIMID), courtyard_ring("wp_c2", 60, 50, 9, 9, (15, -55, 0.3), FATIMID),
         charbagh("wp_garden", 46, 70, (-42, -30, 0.3), path_color=FATIMID)]
    c.append(box("wp_hall", 36, 28, 14, (25, 0, 0.3), "#DCC9A6"))
    c.append(houses("wp_h", [(-45, 60, 26, 20, 9), (-45, 85, 30, 12, 8), (50, -88, 30, 10, 8)], mash=False))
    m.add(2, join(c, "wp_courts"), "courts")
    d = [carved_dome("wp_dome", 7.5, (25, 0, 14.3), FATIMID, k=1.5, ribs=16, amp=0.05, drum_h=1.5)]
    lg = [box("wp_loggia", 12, 40, 19, (-66, -30, 0), FATIMID), arcade("wp_logga", 36, 5.5, 6, (-72.05, -30, 12.6), "W", DARK, True, 0.75)]
    d.append(join(lg, "wp_belvedere"))
    d.append(palms("wp_palm", [(-60, -70), (-25, -70), (-60, 10), (-25, 12)], 2.4))
    m.add(3, join(d, "wp_domes"), "domes")
    return m


def _zuwayla_body(name, col):
    parts = [box(name + "_c", 12, 18, 16, (0, 4, 0), col)]
    parts.append(arch_panel(name + "_a", 4.8, 11, (0, -5.05, 0), "S", DARK, True, 0.5))
    parts.append(arch_panel(name + "_ab", 4.8, 11, (0, 13.05, 0), "N", DARK, True, 0.5))
    parts.append(box(name + "_lint", 6.4, 0.4, 0.8, (0, -5.2, 11.5), STONE_LT))
    for s in (-1, 1):
        cx = s * 9.0
        parts.append(box(f"{name}_tb{s}", 11, 14, 20, (cx, 6, 0), col))
        parts.append(cylinder(f"{name}_tr{s}", 5.5, 20, (cx, -6.5, 0), col, verts=24))
        parts.append(cylinder(f"{name}_tp{s}", 5.8, 0.6, (cx, -6.5, 20), STONE_LT, verts=24))
        parts.append(box(f"{name}_tbp{s}", 11.4, 14.4, 0.6, (cx, 6, 20), STONE_LT))
        for k, a in enumerate((-50, -90, -130)):
            ar = math.radians(a)
            p = arch_panel(f"{name}_tn{s}{k}", 1.6, 3.4, (0, 0, 0), "S", DARK, True, 0.25)
            p = rot(p, a + 90)
            parts.append(move(p, cx + 5.55 * math.cos(ar), -6.5 + 5.55 * math.sin(ar), 13.5))
        parts.append(box(f"{name}_tw{s}", 1.0, 0.3, 1.8, (cx, -12.05, 6), DARK))
    return join(parts, name)


def bab_zuwayla(variant="1092"):
    m = Model("bab-zuwayla")
    m.add(0, ground("bz_g", 30, 26, SAND, 0.2), "ground")
    m.add(0, join([box("bz_wl", 2.0, 5, 12, (-14.5, 6, 0), STONE), box("bz_wr", 2.0, 5, 12, (14.5, 6, 0), STONE)], "bz_wall"))
    m.add(1, _zuwayla_body("bz", STONE), "gate")
    if variant == "1600":
        mins = [mamluk_minaret(f"bz_min{s}", 3.6, 30, (s * 9.0, 2, 20.6), STONE, STONE_LT, "bulb", base=False) for s in (-1, 1)]
        m.add(2, join(mins, "bz_minarets"), "minarets")
    else:
        par = [box(f"bz_par{s}", 10.6, 13.6, 1.2, (s * 9.0, 6, 20.6), STONE) for s in (-1, 1)]
        par += [crest(f"bz_cr{s}", 10.6, 13.6, 21.8, (s * 9.0, 6), STONE, 0.7) for s in (-1, 1)]
        par.append(crest("bz_crc", 12, 18, 16, (0, 4), STONE, 0.7))
        m.add(2, join(par, "bz_parapets"), "parapets")
    return m


def bab_al_futuh():
    m = Model("bab-al-futuh")
    m.add(0, ground("bf_g", 28, 24, SAND, 0.2), "ground")
    m.add(0, join([box("bf_wl", 3, 5, 12, (-13, 7, 0), STONE), box("bf_wr", 3, 5, 12, (13, 7, 0), STONE)], "bf_wall"))
    parts = [box("bf_c", 9, 16, 15, (0, 4, 0), STONE), arch_panel("bf_a", 4.2, 10, (0, -4.05, 0), "S", DARK, False, 0.5),
             arch_panel("bf_ab", 4.2, 10, (0, 12.05, 0), "N", DARK, False, 0.5)]
    for s in (-1, 1):
        cx = s * 8.5
        parts.append(box(f"bf_tb{s}", 10, 12, 18, (cx, 6, 0), STONE))
        parts.append(cylinder(f"bf_tr{s}", 5.6, 18, (cx, -4.5, 0), STONE, verts=28))
        parts.append(cylinder(f"bf_tp{s}", 5.9, 0.6, (cx, -4.5, 18), STONE_LT, verts=28))
        parts.append(box(f"bf_tbp{s}", 10.4, 12.4, 0.6, (cx, 6, 18), STONE_LT))
        for k, a in enumerate((-60, -90, -120)):
            ar = math.radians(a)
            parts.append(move(rot(box(f"bf_sl{s}{k}", 0.5, 0.25, 2.2, (0, 0, 0), DARK), a + 90), cx + 5.62 * math.cos(ar), -4.5 + 5.62 * math.sin(ar), 11))
    for k in range(5):
        parts.append(box(f"bf_vs{k}", 0.5, 0.3, 0.5, (-2.4 + k * 1.2, -4.2, 10.4 + 0.3 * math.sin(math.pi * k / 4)), STONE_LT))
    m.add(1, join(parts, "bf_gate"), "gate")
    par = [box(f"bf_par{s}", 9.6, 11.6, 1.1, (s * 8.5, 6, 18.6), STONE) for s in (-1, 1)]
    par += [crest(f"bf_cr{s}", 9.6, 11.6, 19.7, (s * 8.5, 6), STONE, 0.7) for s in (-1, 1)] + [crest("bf_crc", 9, 16, 15, (0, 4), STONE, 0.7)]
    m.add(2, join(par, "bf_parapets"), "parapets")
    return m


def _shield(name, r, loc, face="S"):
    o = cylinder(name, r, 0.35, (0, 0, 0), STONE_LT, verts=12)
    o = move(o)
    o.rotation_euler[0] = math.pi / 2
    import bpy
    bpy.ops.object.select_all(action="DESELECT")
    o.select_set(True)
    bpy.context.view_layer.objects.active = o
    bpy.ops.object.transform_apply(rotation=True)
    o = rot(o, FACE_ROT[face])
    return move(o, *loc)


def bab_al_nasr():
    m = Model("bab-al-nasr")
    m.add(0, ground("bn_g", 28, 24, SAND, 0.2), "ground")
    m.add(0, join([box("bn_wl", 3, 5, 12, (-13, 7, 0), STONE), box("bn_wr", 3, 5, 12, (13, 7, 0), STONE)], "bn_wall"))
    parts = [box("bn_c", 9, 16, 15, (0, 4, 0), STONE), arch_panel("bn_a", 4.2, 10, (0, -4.05, 0), "S", DARK, False, 0.5),
             arch_panel("bn_ab", 4.2, 10, (0, 12.05, 0), "N", DARK, False, 0.5), box("bn_insc", 8.4, 0.3, 0.9, (0, -4.2, 11.2), DARK)]
    for s in (-1, 1):
        cx = s * 8.5
        parts.append(box(f"bn_t{s}", 10, 20, 19, (cx, 1.5, 0), STONE))
        parts.append(box(f"bn_tp{s}", 10.4, 20.4, 0.6, (cx, 1.5, 19), STONE_LT))
        for k, dx in enumerate((-2.5, 2.5)):
            parts.append(_shield(f"bn_sh{s}{k}", 1.3, (cx + dx, -8.7, 8.5), "S"))
            parts.append(box(f"bn_sw{s}{k}", 0.35, 0.3, 3.6, (cx + dx, -8.6, 3.6), STONE_LT))
        parts.append(arch_panel(f"bn_tn{s}", 1.6, 3.2, (cx, -8.55, 13.5), "S", DARK, True, 0.25))
    m.add(1, join(parts, "bn_gate"), "gate")
    par = [box(f"bn_par{s}", 9.6, 19.6, 1.1, (s * 8.5, 1.5, 19.6), STONE) for s in (-1, 1)]
    par += [crest(f"bn_cr{s}", 9.6, 19.6, 20.7, (s * 8.5, 1.5), STONE, 0.7) for s in (-1, 1)] + [crest("bn_crc", 9, 16, 15, (0, 4), STONE, 0.7)]
    m.add(2, join(par, "bn_parapets"), "parapets")
    return m


def al_hakim():
    m = Model("al-hakim")
    m.add(0, ground("hk_g", 110, 100, SAND), "ground")
    col = "#D9C9A8"
    shell, inner = court_mosque("hk", 96, 92, 12, 30, 12, 12, col, (0, -3, 0), bays=12)
    m.add(0, shell, "walls")
    m.add(1, inner, "arcades")
    yh = -49 + 1.6 + 15
    top = [box("hk_tr", 10, 30, 14.5, (0, yh, 0), shade(col, 0.1)), crest("hk_trc", 10, 30, 14.5, (0, yh), col, 0.6)]
    for k, x in enumerate((-40, 0, 40)):
        top.append(carved_dome(f"hk_d{k}", 4.5 if x == 0 else 3.8, (x, -43, 14.5 if x == 0 else 10.8), col, k=1.5, ribs=0, drum_h=1.2, windows_n=8))
    portal = [box("hk_portal", 16, 8, 15, (0, 46, 0), STONE), iwan("hk_pi", 9, 14, 1.0, (0, 50.1, 0), "N", STONE, STONE_LT)]
    top.append(join(portal, "hk_portal"))
    m.add(2, join(top, "hk_domes"), "portal and domes")
    mins = []
    for s in (-1, 1):
        x = s * 44
        mins.append(frustum(f"hk_sal{s}", 15, 15, 12, 12, 18, (x, 42, 0), STONE))
        mins.append(move(cornice(f"hk_salc{s}", 12, 12, 18, 0.5, 0.3, STONE_LT), x, 42, 0))
        if s < 0:
            mins.append(cylinder("hk_m1", 3.2, 12, (x, 42, 18.5), STONE, verts=20))
        else:
            mins.append(oct_prism("hk_m2", 3.4, 12, (x, 42, 18.5), STONE))
        mins.append(mamluk_minaret(f"hk_top{s}", 5.2, 14, (x, 42, 30.5), STONE, STONE_LT, "mabkhara", base=False))
    m.add(3, join(mins, "hk_minarets"), "minarets")
    return m


def _fan(name, r, n=9, loc=(0, 0, 0), color=STONE_LT):
    """A fluted shell hood (a half-disc of radiating flutes) on a south-facing wall."""
    x, y, z = loc
    verts, faces = [(x, y - 0.6, z)], []
    for i in range(n * 2 + 1):
        a = math.pi * i / (n * 2)
        off = 0.6 if i % 2 == 0 else 0.25
        verts.append((x + r * math.cos(a), y - off, z + r * math.sin(a)))
    for i in range(1, n * 2 + 1):
        faces.append((0, i, i + 1))
    back = len(verts)
    verts += [(x + r * math.cos(math.pi * i / (n * 2)), y, z + r * math.sin(math.pi * i / (n * 2))) for i in range(n * 2 + 1)]
    for i in range(n * 2):
        faces.append((i + 1, back + i, back + i + 1, i + 2))
    return mesh_from(name, verts, faces, (0, 0, 0), color)


def al_aqmar():
    m = Model("al-aqmar")
    m.add(0, ground("aq_g", 30, 35, SAND, 0.2), "ground")
    shell, inner = court_mosque("aq", 26, 28, 9, 10, 4.5, 4.5, "#D7C7A6", (0, 2.5, 0), bays=4, ext_windows=False)
    m.add(1, shell, "walls")
    m.add(1, inner)
    f = [box("aq_front", 30, 2.4, 10.5, (0, -12.8, 0), STONE_LT), crest("aq_frc", 30, 2.4, 10.5, (0, -12.8), STONE_LT, 0.55)]
    f.append(arch_panel("aq_door", 3.0, 5.5, (0, -14.05, 0), "S", DARK, True, 0.4))
    f.append(_fan("aq_hood", 2.6, 9, (0, -14.0, 5.6), STONE))
    f.append(box("aq_frame", 8.4, 0.4, 0.5, (0, -14.2, 8.6), STONE))
    for s in (-1, 1):
        f.append(arch_panel(f"aq_n{s}", 1.8, 4.0, (s * 7.5, -14.05, 1.2), "S", DARK, True, 0.3))
        f.append(_fan(f"aq_nh{s}", 1.2, 7, (s * 7.5, -14.0, 5.6), STONE))
        f.append(box(f"aq_mq{s}", 2.4, 0.5, 1.2, (s * 7.5, -14.2, 7.6), STONE))
    f.append(box("aq_band", 28, 0.4, 0.6, (0, -14.2, 9.4), STONE))
    m.add(2, join(f, "aq_facade"), "facade")
    m.add(3, mamluk_minaret("aq_min", 3.0, 21, (-12.5, -10.5, 0), "#D7C7A6", STONE_LT, "bulb"), "minaret")
    return m


# ---------------------------------------------------------------- Ayyubid and Mamluk

def _nasir_mosque(name):
    shell, inner = court_mosque(name, 62, 56, 12, 22, 8, 8, STONE, (0, 0, 0), bays=8)
    parts = [shell, inner]
    parts.append(carved_dome(name + "_maq", 8.5, (0, -16, 10.8), GREEN_TILE, k=1.3, base_w=19, base_h=2.6, drum_h=2.2, drum_color=STONE))
    parts.append(mamluk_minaret(name + "_mne", 5.0, 40, (29, 26, 0), STONE, STONE_LT, "faience", shaft="round"))
    parts.append(mamluk_minaret(name + "_mnw", 5.0, 36, (-29, 26, 0), STONE, STONE_LT, "faience"))
    parts.append(iwan(name + "_portal", 8, 14, 1.0, (-12, 28.1, 0), "N", STONE, STONE_LT))
    return join(parts, name)


def citadel(variant="1350"):
    m = Model("citadel")
    A, B = (-20, -178), (-10, 160)
    north = [A, (140, -195), (255, -70), (240, 110), (120, 195), B]
    south = [B, (-150, 130), (-255, 40), (-245, -90), (-150, -185), A]
    outline = [(-150, -185), A, (140, -195), (255, -70), (240, 110), (120, 195), B, (-150, 130), (-255, 40), (-245, -90)]
    m.add(0, prism("cit_rock", outline, 2.5, (0, 0, 0), ROCK), "rock")
    wc = "#D2BD95"
    w = [wall_run("cit_wn", north, 14, 5, color=wc, tower_r=7.0, tower_every=50, merlon="box"),
         wall_run("cit_ws", south, 14, 5, color=wc, tower_r=7.0, tower_every=50, merlon="box"),
         wall_run("cit_wp", [A, B], 10, 3.5, color=wc, tower_r=5.0, tower_every=80, merlon="box")]
    m.add(1, join([move(o, 0, 0, 2.5) for o in w], "cit_walls"), "walls")
    t = []
    for k, (x, y) in enumerate(((255, -70), (240, 110), (120, 195), (140, -195))):
        t.append(box(f"cit_sq{k}", 20, 20, 22, (x, y, 2.5), shade(wc, -0.05)))
        t.append(crest(f"cit_sqc{k}", 20, 20, 24.5, (x, y), wc, 0.9))
        t.append(windows(f"cit_sqw{k}", 16, 3, 13, 4, (x, y - 10.05), "S", 0.3))
    t.append(fortress_gate("cit_mudarraj", 30, 16, 17, (55, 178, 2.5), "N", wc, "round"))
    t.append(fortress_gate("cit_jabal", 24, 14, 15, (248, 20, 2.5), "E", wc, "square"))
    t.append(fortress_gate("cit_qulla", 24, 14, 14, (-15, -9, 2.5), "W", wc, "square"))
    m.add(2, join(t, "cit_towers"), "towers and gates")
    b = []
    # the royal (southern) enclosure: the Striped Palace on the cliff, the Great Iwan, palace courts
    b.append(box("cit_ablaq", 70, 30, 22, (-205, -40, 2.5), STONE))
    b.append(bands("cit_ablaqb", 70, 30, 4.0, 22, (-205, -40), ABLAQ_RED, 1.4, 0.6, 0.15))
    b.append(windows("cit_ablaqw", 62, 7, 10, 7, (-205 - 35.1, -40), "W", 0.45))
    b.append(windows("cit_ablaqw2", 28, 3, 10, 7, (-205, -40 - 15.1), "S", 0.45))
    b.append(box("cit_iwan", 44, 34, 20, (-125, 78, 2.5), STONE))
    b.append(iwan("cit_iwanf", 22, 20, 1.2, (-125, 78 - 17.6, 2.5), "S", STONE, STONE_LT))
    b.append(courtyard_ring("cit_harem", 60, 50, 11, 10, (-185, 35, 2.5), STONE))
    b.append(courtyard_ring("cit_pal2", 50, 40, 10, 9, (-110, -120, 2.5), STONE))
    b.append(houses("cit_sh", [(-60, 110, 30, 14, 9), (-200, -120, 24, 20, 9), (-55, -150, 26, 14, 8), (-150, -10, 20, 18, 10), (-170, -85, 22, 16, 11),
                               (-90, 115, 22, 14, 10), (-235, 0, 14, 18, 9), (-30, 70, 18, 26, 9), (-35, -60, 16, 30, 10), (-140, -150, 20, 14, 8)], z=2.5))
    b.append(cylinder("cit_well", 4.5, 4, (-45, -110, 2.5), STONE_LT, verts=16))
    # the military (northern) enclosure: barracks round a parade ground
    b.append(houses("cit_nh", [(60, -160, 70, 14, 8), (190, -100, 14, 70, 8), (200, 60, 14, 80, 8), (120, 160, 60, 14, 8), (40, 120, 40, 16, 9),
                               (90, -60, 30, 24, 10), (150, 20, 26, 30, 9), (20, -100, 24, 20, 8), (60, 40, 30, 16, 9), (110, 110, 24, 18, 9),
                               (210, -20, 14, 40, 8), (20, 20, 20, 30, 10), (130, -120, 26, 16, 8)], z=2.5, mash=False))
    m.add(3, join(b, "cit_palaces"), "palaces")
    d = [carved_dome("cit_iwand", 13, (-125, 78, 22.5), GREEN_TILE, k=1.25, drum_h=3.0, drum_color=STONE)]
    d.append(carved_dome("cit_ablaqd", 7, (-215, -40, 24.5), GREEN_TILE, k=1.3, drum_h=1.5, drum_color=STONE))
    d.append(place(_nasir_mosque("cit_nasir"), -85, 10, 15))
    d[-1] = move(d[-1], 0, 0, 2.5)
    if variant == "1600":
        sp = [box("cit_sul", 20, 20, 10, (0, 0, 0), STONE_LT), shallow_dome("cit_suld", 8.5, (0, 0, 10), GREEN_TILE, rise=0.75, drum=2.0, finial=True),
              box("cit_sulp", 20, 8, 7, (0, -14, 0), STONE_LT), arcade("cit_sulpa", 18, 5, 5, (0, -18.05, 0), "S", DARK, True, 0.7)]
        sp += [shallow_dome(f"cit_sulpd{k}", 2.6, (x, -14, 7), GREEN_TILE, rise=0.8) for k, x in enumerate((-6, 0, 6))]
        sp.append(minaret("cit_sulm", 1.5, 30, (11.5, 8, 0), STONE_LT, STONE_LT, 1, "cone", 16, 0.85))
        o = join(sp, "cit_suleyman")
        d.append(move(place(o, 120, 70, -10), 0, 0, 2.5))
    m.add(4, join(d, "cit_domes"), "mosques and domes")
    return m


def qalawun():
    m = Model("qalawun")
    m.add(0, ground("ql_g", 100, 90, SAND), "ground")
    s = []
    # the maristan behind, round courts with iwans
    s.append(courtyard_ring("ql_mar", 54, 58, 9, 9, (-22, -8, 0.3), BRICK_PL))
    s.append(box("ql_marpool", 14, 6, 0.6, (-22, -8, 0.3), WATER))
    for f, loc in (("N", (-22, -8 - 29 + 9.05)), ("S", (-22, -8 + 29 - 9.05))):
        s.append(arch_panel(f"ql_mariw{f}", 10, 8, (loc[0], loc[1], 0.3), f, DARK, True, 0.4))
    s.append(houses("ql_mh", [(-35, 33, 30, 14, 8), (-8, 34, 16, 12, 9), (-40, -40, 20, 8, 7)], mash=False))
    m.add(1, join(s, "ql_hospital"), "hospital")
    f = []
    f.append(courtyard_ring("ql_mad", 36, 36, 18, 9, (32, -27, 0.3), STONE))
    f.append(box("ql_corr", 52, 6, 11, (24, -6, 0.3), STONE))
    f.append(box("ql_maus", 28, 30, 22, (36, 12, 0.3), STONE))
    f.append(box("ql_nasir", 25, 16, 18, (37.5, 36, 0.3), STONE))
    f.append(windows("ql_w1", 34, 6, 6, 7, (50.05, -27), "E", 0.4, rows=2, dz=8))
    f.append(windows("ql_w2", 28, 4, 6, 9, (50.05, 12), "E", 0.4, rows=2, dz=10))
    f.append(windows("ql_w3", 15, 3, 6, 7, (50.05, 36), "E", 0.4))
    f.append(iwan("ql_portal", 7, 15, 1.0, (50.6, -6, 0.3), "E", STONE, MARBLE_W))
    f.append(arch_panel("ql_gothic", 3.4, 11, (50.15, 38, 0.3), "E", DARK, True, 0.5))
    f.append(box("ql_gothicf", 0.6, 6, 13, (50.3, 38, 0.3), MARBLE_W))
    f.append(crest("ql_c1", 36, 36, 18.3, (32, -27), STONE, 0.7))
    f.append(crest("ql_c2", 28, 30, 22.3, (36, 12), STONE, 0.7))
    f.append(crest("ql_c3", 25, 16, 18.3, (37.5, 36), STONE, 0.6))
    m.add(2, join(f, "ql_facade"), "madrasa and mausoleum")
    t = [carved_dome("ql_dome", 10.5, (36, 12, 22.3), STONE, k=1.35, drum_h=4.0, windows_n=8)]
    t.append(mamluk_minaret("ql_min", 7.5, 56, (48, 27.5, 0.3), STONE, STONE_LT, "bulb"))
    t.append(mamluk_minaret("ql_nmin", 4.4, 42, (45, 42, 0.3), STONE_LT, STONE_LT, "mabkhara"))
    m.add(3, join(t, "ql_dome_minarets"), "dome and minarets")
    return m


def sultan_hasan():
    m = Model("sultan-hasan")
    m.add(0, ground("sh_g", 68, 150, SAND), "ground")
    H = 36
    ring = [box("sh_s", 68, 36, H, (0, -32, 0), STONE), box("sh_n", 68, 37, H, (0, 36.5, 0), STONE),
            box("sh_w", 17, 32, H, (-25.5, 2, 0), STONE), box("sh_e", 17, 32, H, (25.5, 2, 0), STONE),
            box("sh_pave", 34, 32, 0.2, (0, 2, 0), PAVE)]
    ring.append(arch_panel("sh_qiwan", 20, 28, (0, -13.85, 0.2), "N", DARK, True, 0.6))
    ring.append(arch_panel("sh_niwan", 14, 22, (0, 17.85, 0.2), "S", DARK, True, 0.6))
    ring.append(arch_panel("sh_wiwan", 14, 22, (-16.85, 2, 0.2), "E", DARK, True, 0.6))
    ring.append(arch_panel("sh_eiwan", 14, 22, (16.85, 2, 0.2), "W", DARK, True, 0.6))
    m.add(1, join(ring, "sh_block"), "walls")
    f = []
    for face, xs, length, nb in (("W", -34.05, 104, 9), ("E", 34.05, 104, 9)):
        bay = length / nb
        for i in range(nb):
            yy = -50 + bay * (i + 0.5)
            f.append(box(f"sh_rec{face}{i}", 0.3, bay * 0.55, 27, (xs, yy, 4), STONE_DK))
            for r in range(6):
                f.append(arch_panel(f"sh_win{face}{i}{r}", bay * 0.22, 2.0, (xs + (-0.12 if face == "W" else 0.12), yy, 5.5 + r * 4.2), face, DARK, False, 0.2))
    f.append(join([box("sh_cs", 71.5, 3.5, 2.4, (0, -50.0, H - 2.4), STONE_LT), box("sh_cn", 71.5, 3.5, 2.4, (0, 55.0, H - 2.4), STONE_LT),
                   box("sh_cw", 3.5, 105, 2.4, (-34.0, 2.5, H - 2.4), STONE_LT), box("sh_ce", 3.5, 105, 2.4, (34.0, 2.5, H - 2.4), STONE_LT)], "sh_corn"))
    f.append(crest("sh_crest", 71, 108, H, (0, 2.5), STONE, 1.1))
    # the entrance block and the great portal at the north-east corner
    f.append(box("sh_ent", 54, 20, 30, (3, 65, 0), STONE))
    f.append(crest("sh_entc", 54, 20, 30, (3, 65), STONE, 1.0))
    f.append(iwan("sh_portal", 14, 34, 7, (20, 72.0, 0), "N", STONE, STONE_LT))
    f.append(windows("sh_entw", 40, 5, 8, 4, (-5, 75.05), "N", 0.3, rows=3, dz=7))
    # the mausoleum behind the qibla iwan
    f.append(box("sh_maus", 30, 25, 31, (0, -62.5, 0), STONE))
    f.append(windows("sh_mausw", 26, 3, 7, 7, (0, -75.05), "S", 0.35, rows=2, dz=11))
    f.append(windows("sh_mausw2", 22, 3, 7, 7, (-15.05, -62.5), "W", 0.35, rows=2, dz=11))
    f.append(windows("sh_mausw3", 22, 3, 7, 7, (15.05, -62.5), "E", 0.35, rows=2, dz=11))
    f.append(crest("sh_mausc", 30, 25, 31, (0, -62.5), STONE, 0.9))
    m.add(2, join(f, "sh_facades"), "facades and mausoleum")
    t = [carved_dome("sh_dome", 12.0, (0, -62.5, 31), LEAD_GREY, k=1.45, bulb=0.12, base_w=26, base_h=3.5, drum_h=3.0, drum_color=STONE)]
    t.append(mamluk_minaret("sh_min_s", 7.2, 81, (-19, -51, 0), STONE, STONE_LT, "bulb"))
    t.append(mamluk_minaret("sh_min_n", 6.4, 70, (19, -51, 0), STONE, STONE_LT, "bulb"))
    fo = [cylinder(f"sh_fc{i}", 0.35, 6, (4 * math.cos(math.tau * i / 8), 2 + 4 * math.sin(math.tau * i / 8), 0.2), MARBLE_W, verts=6) for i in range(8)]
    fo.append(cylinder("sh_fring", 4.6, 0.8, (0, 2, 6.2), WOOD, verts=16))
    fo.append(onion_dome("sh_fdome", 4.4, (0, 2, 7.0), WOOD, bulb=1.15, height=1.3, drum=0.1, finial=True, finial_color=BRONZE))
    fo.append(cylinder("sh_fbasin", 2.4, 1.0, (0, 2, 0.2), MARBLE_W, verts=8))
    t.append(join(fo, "sh_fountain"))
    m.add(3, join(t, "sh_dome_minarets"), "dome and minarets")
    return m


def khan_el_khalili():
    m = Model("khan-el-khalili")
    m.add(0, ground("kk_g", 100, 70, PAVE), "ground")
    b = [courtyard_ring("kk_c1", 44, 44, 11, 8, (-25, 6, 0.3), STONE), courtyard_ring("kk_c2", 44, 44, 11, 8, (25, 6, 0.3), STONE)]
    b.append(box("kk_shops", 100, 8, 5.5, (0, -30, 0.3), "#D8C7A6"))
    b.append(arcade("kk_shopa", 96, 3.6, 16, (0, -34.05, 0.3), "S", DARK, False, 0.6))
    b.append(arcade("kk_shopb", 96, 3.6, 16, (0, -25.95, 0.3), "N", DARK, False, 0.6))
    for k, cx in enumerate((-25, 25)):
        b.append(windows(f"kk_w{k}", 40, 8, 6.5, 2.6, (cx, 28.05), "N", 0.3))
        b.append(arcade(f"kk_sh{k}", 40, 4, 8, (cx, -16.05, 0.3), "S", DARK, False, 0.6))
        b.append(bands(f"kk_ab{k}", 44, 44, 0.8, 5.5, (cx, 6), "#C9AE86", 1.4, 0.4, 0.1))
    m.add(1, join(b, "kk_khans"), "khans")
    t = [box("kk_gate", 7, 10, 15, (-50, 6, 0.3), STONE), iwan("kk_gatei", 7, 15, 1.0, (-53.4, 6, 0.3), "W", STONE, STONE_LT),
         bands("kk_gateb", 7, 10, 1.0, 14, (-50, 6), ABLAQ_RED, 1.6, 0.5)]
    for k, cx in enumerate((-25, 25)):
        t.append(mashrabiyas(f"kk_m{k}", 38, 7, 6.5, 3.4, (cx, -16.02), "S"))
        t.append(mashrabiyas(f"kk_mn{k}", 38, 7, 6.5, 3.4, (cx, 28.02), "N"))
        for j, (dx, dy) in enumerate(((-15, 20), (12, -8))):
            t.append(box(f"kk_malqaf{k}{j}", 2.4, 1.4, 2.6, (cx + dx, 6 + dy, 11.3), "#CDB48E"))
    t.append(join([box(f"kk_bale{i}", 1.6, 1.2, 1.0, (-25 + (i % 4) * 3 - 4.5, 6 + (i // 4) * 2.5 - 2, 0.3), "#B89C70") for i in range(8)], "kk_bales"))
    m.add(2, join(t, "kk_gate_and_oriels"), "gate and oriels")
    return m


def aqueduct_intake():
    m = Model("aqueduct-intake")
    m.add(0, ground("aqd_g", 90, 45, SAND, 0.2), "ground")
    hx = -24
    tw = [prism("aqd_hex", ngon_pts(20.5, 6), 22, (hx, 0, 0), STONE)]
    tw.append(face_panels("aqd_hexa", 20.5, 6, 9, 15, 0.2, (hx, 0, 0), DARK, True, 1, 0.0))
    tw.append(prism("aqd_hexc", ngon_pts(21.2, 6), 0.8, (hx, 0, 22), STONE_LT))
    m.add(1, join(tw, "aqd_tower"), "tower")
    a = [box("aqd_run", 46, 4.4, 19, (21, 0, 0), STONE), box("aqd_chan", 46, 2.0, 0.8, (21, 0, 19), shade(STONE, -0.15))]
    a.append(arcade("aqd_as", 44, 13, 8, (21, -2.25, 0), "S", DARK, True, 0.62))
    a.append(arcade("aqd_an", 44, 13, 8, (21, 2.25, 0), "N", DARK, True, 0.62))
    ramp = [(-46, 18.3, 22.8), (6, 18.3, 0.2)]
    rv = [(-46, 18.2, 22), (6, 18.2, 0.2), (6, 22.2, 0.2), (-46, 22.2, 22), (-46, 18.2, 0), (6, 18.2, 0), (6, 22.2, 0), (-46, 22.2, 0)]
    a.append(mesh_from("aqd_ramp", rv, [(0, 1, 2, 3), (4, 7, 6, 5), (0, 4, 5, 1), (1, 5, 6, 2), (2, 6, 7, 3), (3, 7, 4, 0)], (0, 0, 0), shade(STONE, -0.05)))
    m.add(2, join(a, "aqd_aqueduct"), "aqueduct")
    w = []
    for k, (dx, dy) in enumerate(((-7, -6), (7, -6), (0, 7))):
        w.append(box(f"aqd_shed{k}", 6, 5, 3.0, (hx + dx, dy, 22.8), WOOD))
        w.append(gable_roof(f"aqd_shedr{k}", 6, 5, 1.4, (hx + dx, dy, 25.8), "#9A7A58", 0.3))
    w.append(join([box(f"aqd_ox{i}", 1.8, 0.8, 1.1, (hx - 12 + i * 3.2, 12, 22.8), "#8A6F55") for i in range(3)], "aqd_oxen"))
    m.add(3, join(w, "aqd_wheels"), "water-wheels")
    return m


# ---------------------------------------------------------------- late Mamluk and Ottoman

def al_muayyad():
    m = Model("al-muayyad")
    m.add(0, ground("mu_g", 80, 95, SAND), "ground")
    shell, inner = court_mosque("mu", 78, 92, 14, 30, 10, 10, STONE, (0, -1, 0), bays=9)
    m.add(0, shell, "walls")
    m.add(1, inner, "arcades")
    t = []
    for k, x in enumerate((-29, 29)):
        t.append(box(f"mu_mb{k}", 17, 17, 18, (x, -36, 0), STONE))
        t.append(crest(f"mu_mbc{k}", 17, 17, 18, (x, -36), STONE, 0.7))
        t.append(carved_dome(f"mu_md{k}", 7.2, (x, -36, 18), STONE, k=1.45, ribs=28, amp=0.03, base_w=16, base_h=2.4, drum_h=2.4))
    t.append(box("mu_portal", 6, 12, 20, (38, 30, 0), STONE))
    t.append(iwan("mu_pi", 10, 20, 1.2, (41.1, 30, 0), "E", STONE, STONE_LT))
    t.append(bands("mu_pb", 6, 12, 1.0, 19, (38, 30), ABLAQ_RED, 1.6, 0.5))
    m.add(2, join(t, "mu_domes"), "domes and portal")
    return m


def wikala_al_ghuri():
    m = Model("wikala-al-ghuri")
    m.add(0, ground("wk_g", 35, 45, PAVE, 0.2), "ground")
    b = [courtyard_ring("wk_low", 35, 45, 8, 9.5, (0, 0, 0.2), STONE), bands("wk_ab", 35, 45, 0.8, 7.5, (0, 0), "#C2A47A", 1.5, 0.45, 0.1)]
    b.append(arcade("wk_shops", 30, 4, 6, (0, -22.55, 0.2), "S", DARK, False, 0.6))
    m.add(1, join(b, "wk_ground"), "storerooms")
    u = [courtyard_ring("wk_up", 35, 45, 14, 9.5, (0, 0, 8.2), "#E1D3B5", DARK, False)]
    for f, loc, L in (("S", (0, -22.55), 35), ("N", (0, 22.55), 35), ("E", (17.55, 0), 45), ("W", (-17.55, 0), 45)):
        u.append(windows(f"wk_w{f}", L * 0.85, int(L / 4), 9.5, 2.0, loc, f, 0.4, False, rows=3, dz=4.4))
    u.append(mashrabiyas("wk_mc", 14, 4, 12, 3, (0, -13.25 + 0.0), "N"))
    u.append(mashrabiyas("wk_mc2", 14, 4, 12, 3, (0, 13.25), "S"))
    u.append(crest("wk_cr", 35, 45, 22.2, (0, 0), "#E1D3B5", 0.6))
    m.add(2, join(u, "wk_upper"), "apartments")
    p = [box("wk_portal", 9, 3, 13, (0, -21.5, 0.2), STONE), iwan("wk_pi", 6.5, 12.5, 0.8, (0, -23.2, 0.2), "S", STONE, STONE_LT),
         bands("wk_pb", 9, 3, 1.0, 12, (0, -21.5), ABLAQ_RED, 1.5, 0.45)]
    p += [box(f"wk_malqaf{k}", 2.6, 1.6, 2.6, (x, y, 22.2), "#CDB48E") for k, (x, y) in enumerate(((-10, 15), (10, -15)))]
    m.add(3, join(p, "wk_portal"), "portal")
    return m


def bulaq():
    m = Model("bulaq")
    m.add(0, ground("bq_g", 140, 220, SAND), "ground")
    m.add(0, box("bq_water", 20, 220, 0.35, (-60, 0, 0), WATER))
    q = [box("bq_quay", 5, 220, 1.8, (-47.5, 0, 0), STONE_DK)]
    for k, y in enumerate((-80, -20, 40, 95)):
        q.append(stair(f"bq_st{k}", 8, 1.8, 4, 5, (-50, y, 0), "W", STONE_DK))
    m.add(1, join(q, "bq_quay"), "quay")
    b = []
    for k, (x, y, w, d) in enumerate(((-20, 72, 40, 36), (-20, 22, 38, 34), (-22, -28, 36, 34), (30, 80, 34, 34), (34, 26, 32, 34))):
        b.append(courtyard_ring(f"bq_wk{k}", w, d, 10, 7, (x, y, 0.3), STONE if k % 2 else "#D9C9A8"))
        b.append(mashrabiyas(f"bq_wm{k}", w * 0.8, int(w / 6), 6, 3, (x, y - d / 2 - 0.02, 0.3), "S"))
    b.append(houses("bq_h", [(-25, -70, 18, 14, 9), (-28, -100, 14, 14, 10), (50, -20, 16, 18, 11), (20, -20, 14, 14, 8), (55, 100, 14, 16, 9), (58, 50, 12, 14, 8), (-30, 102, 16, 10, 8)]))
    for k, (x, y) in enumerate(((5, 100), (5, 50))):
        b.append(join([cylinder(f"bq_gr{k}{i}", 3.2, 5.5, (x + (i - 1) * 7, y, 0.3), "#D3BE98", verts=12) for i in range(3)] +
                      [dome(f"bq_grd{k}{i}", 3.2, (x + (i - 1) * 7, y, 5.8), "#D3BE98", 1.0, 12, 6) for i in range(3)], f"bq_granary{k}"))
    m.add(2, join(b, "bq_wikalas"), "wikalas")
    s = [box("bq_sinan", 22, 22, 11, (0, 0, 0), STONE_LT), shallow_dome("bq_sinand", 10.5, (0, 0, 11), LEAD_GREY, rise=0.62, drum=2.2, finial=True)]
    for side, (dx, dy, ww, dd) in (("S", (0, -14.5, 30, 7)), ("E", (14.5, 0, 7, 22)), ("W", (-14.5, 0, 7, 22))):
        s.append(box(f"bq_por{side}", ww, dd, 7, (dx, dy, 0), STONE_LT))
        n = 5 if side == "S" else 4
        s.append(arcade(f"bq_pora{side}", (ww if side == "S" else dd) * 0.92, 5.2, n, (dx + {"S": 0, "E": 3.55, "W": -3.55}[side], dy + (-3.55 if side == "S" else 0), 0), side, DARK, True, 0.7))
        for i in range(n):
            u = -(ww if side == "S" else dd) / 2 + (ww if side == "S" else dd) * (i + 0.5) / n
            s.append(shallow_dome(f"bq_pord{side}{i}", 2.4, (dx + (u if side == "S" else 0), dy + (0 if side == "S" else u), 7), LEAD_GREY, rise=0.7))
    s.append(minaret("bq_sinm", 1.5, 28, (13, 13, 0), STONE_LT, STONE_LT, 1, "cone", 16, 0.85))
    s.append(wall_run("bq_sinw", [(-24, -24), (24, -24), (24, 24), (-24, 24), (-24, -24)], 2.4, 0.8, color=STONE_LT, towers=False, merlon=None))
    m.add(3, place(join(s, "bq_sinan_mosque"), 30, -72, 0), "mosque")
    bt = [boat("bq_b0", 18, (-60, -90), 92), boat("bq_b1", 22, (-61, -45), 88), boat("bq_b2", 16, (-58, 5), 95, sail=False), boat("bq_b3", 20, (-62, 50), 90),
          boat("bq_b4", 15, (-57, 85), 85, sail=False), boat("bq_b5", 19, (-63, 105), 91)]
    m.add(3, join([move(b, 0, 0, 0.35) for b in bt], "bq_boats"))
    m.add(3, join([box(f"bq_sack{i}", 2.0, 1.4, 1.2, (-40 + (i % 3) * 2.6, -60 + (i // 3) * 30, 0.3), "#BFA57A") for i in range(15)], "bq_sacks"))
    return m


def qaitbay():
    m = Model("qaitbay")
    m.add(0, ground("qb_g", 60, 50, SAND), "ground")
    b = [box("qb_hall", 38, 32, 14, (-8, 2, 0.3), STONE), bands("qb_hb", 38, 32, 1.0, 13, (-8, 2), ABLAQ_RED, 2.2, 0.5, 0.1),
         crest("qb_hc", 38, 32, 14.3, (-8, 2), STONE, 0.7), windows("qb_hw", 32, 5, 6, 5.5, (-8, 18.05), "N", 0.35)]
    b.append(box("qb_lantern", 7, 7, 2.2, (-8, 4, 14.3), "#A08360"))
    b.append(hip_roof("qb_lanternr", 7, 7, 1.6, (-8, 4, 16.5), "#A08360", 0.3, 0.2))
    b.append(box("qb_sabil", 13, 12, 13, (-23.5, -18, 0.3), STONE))
    b.append(arcade("qb_kuttab", 12, 4, 3, (-23.5, -24.05, 8.5), "S", DARK, True, 0.75))
    b.append(windows("qb_sabw", 10, 2, 2, 4, (-23.5, -24.05), "S", 0.5, False))
    b.append(wall_run("qb_encl", [(-30, -25), (30, -25), (30, 25), (-30, 25), (-30, -25)], 3.0, 0.9, color=STONE, towers=False, merlon=None))
    m.add(1, join(b, "qb_mosque"), "mosque")
    t = [box("qb_maus", 20, 20, 16, (19, -10, 0.3), STONE), crest("qb_mc", 20, 20, 16.3, (19, -10), STONE, 0.7), windows("qb_mw", 16, 3, 7, 6, (19, -20.05), "S", 0.35)]
    t.append(carved_dome("qb_dome", 8.2, (19, -10, 16.3), "#D2BE98", k=1.45, ribs=36, amp=0.028, base_w=18, base_h=3.0, drum_h=3.2, drum_color=STONE))
    t.append(iwan("qb_portal", 7, 15, 1.0, (-14, 18.6, 0.3), "N", STONE, STONE_LT))
    t.append(mamluk_minaret("qb_min", 4.8, 42, (-2, 18, 0.3), STONE, STONE_LT, "bulb"))
    m.add(2, join(t, "qb_dome_minaret"), "dome and minaret")
    return m


BUILDERS = {
    "cairo/amr-mosque": amr_mosque,
    "cairo/amr-mosque-700": lambda: amr_mosque("700"),
    "cairo/babylon": babylon,
    "cairo/nilometer": nilometer,
    "cairo/ibn-tulun": ibn_tulun,
    "cairo/tulunid-palace": tulunid_palace,
    "cairo/al-azhar-972": lambda: al_azhar("972"),
    "cairo/al-azhar-1350": lambda: al_azhar("1350"),
    "cairo/al-azhar-1600": lambda: al_azhar("1600"),
    "cairo/eastern-palace": eastern_palace,
    "cairo/western-palace": western_palace,
    "cairo/bab-zuwayla": bab_zuwayla,
    "cairo/bab-zuwayla-1600": lambda: bab_zuwayla("1600"),
    "cairo/bab-al-futuh": bab_al_futuh,
    "cairo/bab-al-nasr": bab_al_nasr,
    "cairo/al-hakim": al_hakim,
    "cairo/al-aqmar": al_aqmar,
    "cairo/citadel": citadel,
    "cairo/citadel-1600": lambda: citadel("1600"),
    "cairo/qalawun": qalawun,
    "cairo/sultan-hasan": sultan_hasan,
    "cairo/khan-el-khalili": khan_el_khalili,
    "cairo/aqueduct-intake": aqueduct_intake,
    "cairo/al-muayyad": al_muayyad,
    "cairo/wikala-al-ghuri": wikala_al_ghuri,
    "cairo/bulaq": bulaq,
    "cairo/qaitbay": qaitbay,
}
