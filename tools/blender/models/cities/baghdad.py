"""Baghdad landmark miniatures: al-Mansur's Round City and its palace and mosque, the Abbasid palaces and bridges,
the late-caliphal east city (Mustansiriya, gates, Dar al-Khilafa, the muqarnas tomb of Zumurrud Khatun) and Ottoman Baghdad.

Conventions as in FORMAT.md: metres, origin at the ground centre, +X east, +Y north, main front toward -Y unless a builder
says otherwise; the landmark rotation turns it on the map.
"""
import math
import random
from chronokit import Model, box, cylinder, dome, join, shade, gable_roof, hip_roof, mesh_from, ring_extrude
from worldkit import *

BRICK_Y, BRICK_L, BRICK_D = "#CDAA7C", "#DCC29A", "#B08A60"      # yellow Baghdad fired brick
MUD, MUD_L = "#C4A982", "#D3BC96"                                  # sun-dried brick and clay plaster
PLAST = "#E4D8C0"
GREEN_DOME, GREEN_DK = "#4E8A62", "#3E6E50"
TURQ, BLUE_T, GOLDEN = "#3F9A9A", "#3E62A0", "#C9A24A"
SAND, PAVE, ROAD, DUST = "#D8C7A1", "#E3D5B8", "#CDB894", "#BFA982"
PALM, ORCH, FIELD = "#6E8A55", "#7E9563", "#B9B07A"
WOOD, WOOD_D, CLOTH = "#7A5A3C", "#5E4430", "#EDE4CF"
HOUSES = ["#D9C29A", "#CDB48A", "#E2D0AE", "#C8AA80", "#D4BC94"]
FACE_ROT = {"S": 0, "N": 180, "E": 90, "W": -90}


# ---------------------------------------------------------------- helpers (several copied from cairo.py)

def place(o, x=0, y=0, deg=0):
    o = move(o)
    if deg:
        o = rot(o, deg)
    return move(o, x, y, 0)


def ngon_pts(r, n, start=0.0):
    return [(r * math.cos(start + math.tau * i / n), r * math.sin(start + math.tau * i / n)) for i in range(n)]


def oct_prism(name, r, h, loc=(0, 0, 0), color=BRICK_Y):
    return prism(name, ngon_pts(r, 8, math.pi / 8), h, loc, color)


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


def boxes(name, specs, color):
    """Many boxes in one mesh (fast): specs = [(cx, cy, w, d, h[, z[, angle_rad]]), ...]."""
    verts, faces = [], []
    for s in specs:
        cx, cy, w, d, h = s[:5]
        z = s[5] if len(s) > 5 else 0.0
        a = s[6] if len(s) > 6 else 0.0
        ca, sa = math.cos(a), math.sin(a)
        b = len(verts)
        for zz in (z, z + h):
            for sx, sy in ((-1, -1), (1, -1), (1, 1), (-1, 1)):
                x, y = sx * w / 2, sy * d / 2
                verts.append((cx + x * ca - y * sa, cy + x * sa + y * ca, zz))
        faces += [(b + 3, b + 2, b + 1, b), (b + 4, b + 5, b + 6, b + 7), (b, b + 1, b + 5, b + 4), (b + 1, b + 2, b + 6, b + 5), (b + 2, b + 3, b + 7, b + 6), (b + 3, b, b + 4, b + 7)]
    if not specs:
        return None
    return mesh_from(name, verts, faces, (0, 0, 0), color)


def annulus(name, r0, r1, h, a0=0.0, a1=math.tau, n=None, z=0.0, color=BRICK_Y):
    """A ring (or an arc of one) of inner radius r0 and outer radius r1, extruded up by h."""
    full = abs((a1 - a0) - math.tau) < 1e-6
    n = n or max(6, int(abs(a1 - a0) * r1 / 24))
    k = n if full else n + 1
    outer = [(r1 * math.cos(a0 + (a1 - a0) * i / n), r1 * math.sin(a0 + (a1 - a0) * i / n)) for i in range(k)]
    inner = [(r0 * math.cos(a0 + (a1 - a0) * i / n), r0 * math.sin(a0 + (a1 - a0) * i / n)) for i in range(k)]
    return ring_extrude(name, outer, inner, h, (0, 0, z), color, closed=full)


def arcs_between(gaps, half):
    """The angular spans [(a0, a1), ...] of a circle left between gaps centred at the angles in `gaps` (half-width `half`)."""
    g = sorted(a % math.tau for a in gaps)
    return [(g[i] + half, (g[(i + 1) % len(g)] + (math.tau if i == len(g) - 1 else 0)) - half) for i in range(len(g))]


def bands(name, w, d, z0, z1, loc=(0, 0), color=BRICK_D, every=1.5, band=0.55, grow=0.12):
    """Horizontal courses of a second colour round the four faces of a block or an enclosure (perimeter strips only)."""
    out = []
    z = z0
    t = max(0.3, grow)
    cx, cy = loc[0], loc[1]
    while z + band <= z1:
        out += [(cx, cy - d / 2, w + grow, t, band, z), (cx, cy + d / 2, w + grow, t, band, z),
                (cx - w / 2, cy, t, d + grow, band, z), (cx + w / 2, cy, t, d + grow, band, z)]
        z += every
    return boxes(name, out, color)


def windows(name, length, n, z, h, loc, face="S", fill=0.35, pointed=True):
    return arcade(name, length, h, n, (loc[0], loc[1], z), face, DARK, pointed, fill, 0.25)


def diamonds(name, length, n, z, s, loc, face="S", color=BRICK_D, depth=0.25):
    """A row of lozenges of carved brick on a wall face (patterned Abbasid brickwork)."""
    verts, faces = [], []
    for i in range(n):
        x = -length / 2 + (i + 0.5) * length / n
        b = len(verts)
        for y in (-depth / 2, depth / 2):
            verts += [(x - s, y, s), (x, y, 2 * s), (x + s, y, s), (x, y, 0)]
        faces += [(b, b + 1, b + 2, b + 3), (b + 7, b + 6, b + 5, b + 4), (b, b + 4, b + 5, b + 1), (b + 1, b + 5, b + 6, b + 2), (b + 2, b + 6, b + 7, b + 3), (b + 3, b + 7, b + 4, b)]
    o = mesh_from(name, verts, faces, (0, 0, 0), color)
    o = rot(o, FACE_ROT[face])
    return move(o, loc[0], loc[1], z)


def on_faces(w, d, cx=0.0, cy=0.0, off=0.05):
    """(length, x, y, face) for the four outer faces of a w x d block."""
    return [(w, cx, cy - d / 2 - off, "S"), (w, cx, cy + d / 2 + off, "N"), (d, cx + w / 2 + off, cy, "E"), (d, cx - w / 2 - off, cy, "W")]


def blind_arcade_faces(name, w, d, z, h, bay, cx=0.0, cy=0.0, fill=0.66, frames=None):
    """Blind pointed arches (dark recesses) round all four faces of a block; frames = colour of a rectangular frame per bay."""
    out = []
    for i, (L, x, y, f) in enumerate(on_faces(w, d, cx, cy)):
        n = max(1, int(L / bay))
        out.append(arcade(f"{name}{i}", L * 0.94, h, n, (x, y, z), f, DARK, True, fill, 0.3))
        if frames:
            step = L * 0.94 / n
            specs = []
            for k in range(n):
                u = -L * 0.94 / 2 + step * (k + 0.5)
                bx, by = (x + u, y) if f in ("S", "N") else (x, y + u)
                bw, bd = (step * 0.86, 0.22) if f in ("S", "N") else (0.22, step * 0.86)
                specs.append((bx, by, bw, bd, h * 1.12, z - h * 0.04))
            out.append(boxes(f"{name}{i}f", specs, frames))
    return join(out, name)


def lozenge_faces(name, w, d, z, s, cx=0.0, cy=0.0, color=BRICK_D, step=None):
    step = step or s * 3.0
    return join([diamonds(f"{name}{i}", L * 0.94, max(2, int(L * 0.94 / step)), z, s, (x, y), f, color) for i, (L, x, y, f) in enumerate(on_faces(w, d, cx, cy, 0.08))], name)


def crest(name, w, d, z, loc=(0, 0), color=BRICK_Y, size=0.8, shape="stepped"):
    return move(merlons(name, w, d, z, size, size * 0.7, color, shape), loc[0], loc[1], 0)


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


def pdome(name, r, loc=(0, 0, 0), color=BRICK_Y, k=1.35, drum_h=None, drum_color=None, windows_n=8, ribs=0, amp=0.04, top=True, bulb=0.0):
    """A pointed brick or tiled dome on a drum with windows."""
    x, y, z = loc
    parts = []
    dh = r * 0.4 if drum_h is None else drum_h
    if dh > 0:
        parts.append(cylinder(name + "_drum", r * 1.04, dh, (x, y, z), drum_color or color, verts=24))
        if windows_n:
            parts.append(face_panels(name + "_dw", r * 1.04, 16, r * 0.2, dh * 0.62, z + dh * 0.16, (x, y, 0), DARK, True, max(1, 16 // windows_n)))
        z += dh
    prof = pointed_profile(r, k, bulb)
    d = lathe(name + "_d", prof, (x, y, z), color, verts=max(28, ribs * 2) if ribs else 28)
    if ribs:
        for v in d.data.vertices:
            dx, dy = v.co.x - x, v.co.y - y
            if math.hypot(dx, dy) > 1e-3 and v.co.z > z + 0.05:
                kk = 1 + amp * math.cos(math.atan2(dy, dx) * ribs)
                v.co.x, v.co.y = x + dx * kk, y + dy * kk
    parts.append(d)
    if top:
        parts.append(finial(name + "_f", r * 0.4, (x, y, z + prof[-1][1] - r * 0.03)))
    return join(parts, name)


def muqarnas_cone(name, r, h, tiers, loc=(0, 0, 0), color=BRICK_Y, cell=1.2, top=True):
    """The Iraqi 'sugar-loaf' muqarnas dome: tiers of small niches stepping inward to a point."""
    x, y, z0 = loc
    parts = []
    th = h / (tiers + 0.6)
    for k in range(tiers):
        t = k / tiers
        rk = r * (1 - t) ** 0.8
        n = max(8, int(round(math.tau * rk / cell / 4)) * 4)
        z = z0 + k * th
        parts.append(prism(f"{name}_t{k}", ngon_pts(rk, n, math.pi / n), th * 0.82, (x, y, z), color))
        rn = r * (1 - (k + 1) / tiers) ** 0.8 if k < tiers - 1 else rk * 0.35
        parts.append(cylinder(f"{name}_c{k}", rk * 1.02, th * 0.18, (x, y, z + th * 0.82), shade(color, 0.08), verts=n, r_top=rn * 1.04 if rn > 0 else 0.05))
        parts.append(face_panels(f"{name}_n{k}", rk, n, math.tau * rk / n * 0.62, th * 0.66, z + th * 0.06, (x, y, 0), shade(color, -0.42), True, 1, math.pi / n, 0.18))
    ztop = z0 + tiers * th
    parts.append(cylinder(name + "_tip", r * 0.12, th * 0.6, (x, y, ztop), color, verts=8, r_top=0.02))
    if top:
        parts.append(finial(name + "_fin", r * 0.35, (x, y, ztop + th * 0.5)))
    return join(parts, name)


def portal(name, w, h, depth, loc, face="S", color=BRICK_Y, trim=BRICK_L, hood=True, inscription=True):
    """A projecting pishtaq portal: piers and lintel round a recessed arch, a muqarnas hood stepping out from the back wall,
    an inscription frame and carved lozenges."""
    x, y, z = loc
    rw = w * 0.56
    pw = (w - rw) / 2
    yb = depth * 0.12                       # front face of the recess's back wall
    parts = [box(name + "_back", rw, depth / 2 - yb, h * 0.86, (0, (yb + depth / 2) / 2, 0), shade(color, -0.12))]
    for s in (-1, 1):
        parts.append(box(f"{name}_pier{s}", pw, depth, h, (s * (rw / 2 + pw / 2), 0, 0), color))
    parts.append(box(name + "_lint", rw, depth, h * 0.14, (0, 0, h * 0.86), color))
    parts.append(arch_panel(name + "_door", rw * 0.52, h * 0.42, (0, yb - 0.15, 0), "S", DARK, True, 0.3))
    parts.append(arch_panel(name + "_arch", rw * 0.98, h * 0.86, (0, -depth / 2 - 0.05, 0), "S", shade(color, -0.32), True, 0.1))
    if hood:
        tiers, rd = 5, depth / 2 + yb
        z0, th = h * 0.5, h * 0.36 / 5
        for k in range(tiers):
            dk = rd * (k + 1) / tiers * 0.9
            parts.append(box(f"{name}_hr{k}", rw * 0.98, dk, th, (0, yb - dk / 2, z0 + k * th), shade(trim, 0.05 * (k % 2))))
            parts.append(arcade(f"{name}_ha{k}", rw * 0.94, th * 0.84, max(2, int(rw / 0.9)), (0, yb - dk - 0.02, z0 + k * th + th * 0.08), "S", shade(trim, -0.45), True, 0.7, 0.12))
    if inscription:
        parts.append(box(name + "_ins", w * 0.94, 0.3, h * 0.05, (0, -depth / 2 - 0.12, h * 0.9), shade(color, -0.4)))
        for s in (-1, 1):
            parts.append(box(f"{name}_insv{s}", w * 0.04, 0.3, h * 0.86, (s * (rw / 2 + w * 0.04), -depth / 2 - 0.12, 0.0), shade(color, -0.4)))
            lz = diamonds(f"{name}_lz{s}", 0.01, 1, 0, w * 0.05, (0, 0), "S", trim)
            parts.append(move(lz, s * (rw / 2 + pw * 0.6), -depth / 2 - 0.15, h * 0.62))
            parts.append(arch_panel(f"{name}_sn{s}", pw * 0.5, h * 0.3, (s * (rw / 2 + pw * 0.6), -depth / 2 - 0.05, h * 0.12), "S", DARK, True, 0.25))
    parts.append(box(name + "_cap", w + 0.4, depth + 0.4, 0.5, (0, 0, h), trim))
    o = join(parts, name)
    o = rot(o, FACE_ROT[face])
    return move(o, x, y, z)


def palms(name, spots, r=2.2, z=0.3):
    return join([tree(f"{name}{i}", r, (x, y, z), PALM, TIMBER, "palm") for i, (x, y) in enumerate(spots)], name)


def trees(name, spots, r=2.6, z=0.3, color=ORCH):
    return join([tree(f"{name}{i}", r, (x, y, z), color) for i, (x, y) in enumerate(spots)], name)


def houses(name, specs, z=0.3):
    """Plain flat-roofed courtyard houses: specs = [(x, y, w, d, h), ...]; a dark court on the roof of the larger ones."""
    walls, courts, pars = [], [], []
    for i, (x, y, w, d, h) in enumerate(specs):
        walls.append((x, y, w, d, h, z))
        pars.append((x, y, w + 0.2, d + 0.2, 0.5, z + h))
        if w >= 8 and d >= 8:
            courts.append((x, y, w * 0.4, d * 0.4, 0.1, z + h + 0.02))
    out = [boxes(name + "_w", walls, HOUSES[0]), boxes(name + "_p", pars, shade(HOUSES[1], -0.05))]
    if courts:
        out.append(boxes(name + "_c", courts, shade(HOUSES[3], -0.45)))
    return join(out, name)


def boat(name, length, loc=(0, 0, 0), deg=0, sail=True, hull=WOOD, cloth=CLOTH):
    """A Tigris boat: a pointed hull, a mast and a lateen sail."""
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


def abbasid_wall(name, pts, h, t, color=BRICK_Y, tower_r=None, every=24.0, merlon="round"):
    """An early Abbasid enclosure wall: plain brick with closely spaced half-round buttress towers (as at Ukhaidir and Samarra)."""
    return wall_run(name, pts, h, t, color=color, towers=True, tower_r=tower_r or t * 1.5, tower_every=every, merlon=merlon)


def court_mosque(name, w, d, h, hall_d, side_d, back_d, color, loc=(0, 0, 0), roof=None, piers=True):
    """An early Abbasid courtyard mosque: thick outer walls, a deep flat-roofed prayer hall on the qibla (south) side,
    arcades round the court. Returns (shell, interior)."""
    x0, y0, z0 = loc
    t = 2.0
    shell = [box(name + "_ws", w, t, h, (x0, y0 - d / 2 + t / 2, z0), color), box(name + "_wn", w, t, h, (x0, y0 + d / 2 - t / 2, z0), color),
             box(name + "_ww", t, d - 2 * t, h, (x0 - w / 2 + t / 2, y0, z0), color), box(name + "_we", t, d - 2 * t, h, (x0 + w / 2 - t / 2, y0, z0), color)]
    shell.append(crest(name + "_cr", w, d, z0 + h, (x0, y0), color, 0.8, "stepped"))
    rh = h - 1.4
    rc = roof or shade(color, 0.12)
    yA = y0 - d / 2 + t + hall_d
    yB = y0 + d / 2 - t - back_d
    cw = w - 2 * t - 2 * side_d
    inner = [box(name + "_hall", w - 2 * t, hall_d, rh, (x0, y0 - d / 2 + t + hall_d / 2, z0), rc),
             box(name + "_back", w - 2 * t, back_d, rh, (x0, y0 + d / 2 - t - back_d / 2, z0), rc)]
    for s in (-1, 1):
        inner.append(box(f"{name}_side{s}", side_d, yB - yA, rh, (x0 + s * (w / 2 - t - side_d / 2), (yA + yB) / 2, z0), rc))
    # aisle lines on the hall roof (the flat timber roof over rows of piers)
    na = max(3, int(hall_d / 5))
    inner.append(boxes(name + "_aisles", [(x0, y0 - d / 2 + t + (k + 0.5) * hall_d / na, w - 2 * t - 1, 0.5, 0.35, z0 + rh) for k in range(na)], shade(rc, -0.12)))
    inner.append(box(name + "_pave", cw, yB - yA, 0.15, (x0, (yA + yB) / 2, z0), PAVE))
    nb = max(4, int(cw / 4.5))
    nd = max(3, int((yB - yA) / 4.5))
    ah = rh * 0.78
    inner.append(arcade(name + "_ah", cw, ah, nb, (x0, yA + 0.05, z0), "N", DARK, True, 0.7))
    inner.append(arcade(name + "_ab", cw, ah, nb, (x0, yB - 0.05, z0), "S", DARK, True, 0.7))
    inner.append(arcade(name + "_aw", yB - yA, ah, nd, (x0 - cw / 2 + 0.05, (yA + yB) / 2, z0), "E", DARK, True, 0.7))
    inner.append(arcade(name + "_ae", yB - yA, ah, nd, (x0 + cw / 2 - 0.05, (yA + yB) / 2, z0), "W", DARK, True, 0.7))
    return join(shell, name + "_shell"), join(inner, name + "_inner")


def round_minaret(name, r, h, loc=(0, 0, 0), color=BRICK_Y, trim=BRICK_L, base=True, top="cap", tile=None):
    """An Iraqi brick minaret: octagonal base, tapering round shaft with brick bands, a muqarnas balcony and a small cap."""
    x, y, z = loc
    parts = []
    if base:
        parts.append(oct_prism(name + "_b", r * 1.35, h * 0.16, (x, y, z), color))
        z += h * 0.16
    hs = h * 0.66
    parts.append(cylinder(name + "_s", r, hs, (x, y, z), color, verts=16, r_top=r * 0.8))
    for k in range(1, 5):
        zz = z + hs * k / 5
        rr = r * (1 - 0.2 * k / 5) + 0.06
        parts.append(cylinder(f"{name}_bd{k}", rr, 0.5, (x, y, zz), tile or trim, verts=16))
    z += hs
    rt = r * 0.8
    parts.append(cylinder(name + "_cor", rt, r * 0.7, (x, y, z), trim, verts=16, r_top=rt * 1.45))
    parts.append(cylinder(name + "_bal", rt * 1.45, 0.4, (x, y, z + r * 0.7), color, verts=16))
    z += r * 0.7 + 0.4
    if top == "cone":
        parts.append(cylinder(name + "_up", rt * 0.7, h * 0.1, (x, y, z), color, verts=16))
        parts.append(cylinder(name + "_cone", rt * 0.78, h * 0.12, (x, y, z + h * 0.1), LEAD, verts=16, r_top=0.0))
    else:
        parts.append(cylinder(name + "_up", rt * 0.62, h * 0.08, (x, y, z), tile or color, verts=16))
        parts.append(pdome(name + "_cap", rt * 0.66, (x, y, z + h * 0.08), tile or color, k=1.3, drum_h=0, top=True))
    return join(parts, name)


def ottoman_dome(name, r, loc, color=LEAD, drum_color=PLAST, drum=0.45):
    x, y, z = loc
    parts = [cylinder(name + "_dr", r * 1.03, r * drum, (x, y, z), drum_color, verts=24),
             face_panels(name + "_dw", r * 1.03, 16, r * 0.17, r * drum * 0.6, z + r * drum * 0.18, (x, y, 0), DARK, True, 1)]
    parts.append(shallow_dome(name + "_d", r, (x, y, z + r * drum), color, rise=0.78, finial=True))
    return join(parts, name)


# ---------------------------------------------------------------- the Round City

GATE_ANG = {"khurasan": 45, "sham": 135, "kufa": 225, "basra": 315}
R_MOAT, R_OUT, R_MAIN0, R_MAIN1, R_RES0, R_RES1, R_IN = (1172, 1198), (1158, 1165), 1078, 1100, 836, 1068, (826, 832)


def gate_complex(tag, dome_color=GREEN_DOME):
    """One gate of the Round City built along +X (outward): moat bridge, outer gate, main gate with the domed audience hall,
    and the arcaded passage (taq) through the residential ring to the inner gate. Returns (walls_part, passage_part, dome_part)."""
    w = []
    w.append(box(f"{tag}_br", R_MOAT[1] - R_MOAT[0] + 6, 9, 1.0, ((R_MOAT[0] + R_MOAT[1]) / 2, 0, 0.3), BRICK_D))
    w.append(box(f"{tag}_og", 14, 26, 11, (R_OUT[0] + 3.5, 0, 0), BRICK_Y))
    w.append(arch_panel(f"{tag}_oga", 5, 7.5, (R_OUT[0] + 10.6, 0, 0), "E", DARK, True, 0.4))
    for s in (-1, 1):
        w.append(cylinder(f"{tag}_ogt{s}", 6, 13, (R_OUT[0] + 6, s * 14, 0), BRICK_Y, verts=14))
    # walled lane across the intervallum (the bent entrance)
    for s in (-1, 1):
        w.append(box(f"{tag}_lw{s}", R_OUT[0] - R_MAIN1, 1.4, 6, ((R_OUT[0] + R_MAIN1) / 2, s * 12, 0), BRICK_Y))
    # main gate block
    gx = (R_MAIN0 + R_MAIN1) / 2
    w.append(box(f"{tag}_mg", 44, 54, 22, (gx, 0, 0), BRICK_Y))
    w.append(bands(f"{tag}_mgb", 44, 54, 3, 21, (gx, 0), BRICK_D, 3.0, 0.5))
    w.append(arch_panel(f"{tag}_mga", 9, 14, (gx + 22.1, 0, 0), "E", DARK, True, 0.5))
    w.append(arch_panel(f"{tag}_mgi", 9, 14, (gx - 22.1, 0, 0), "W", DARK, True, 0.5))
    for s in (-1, 1):
        w.append(cylinder(f"{tag}_mgt{s}", 10, 26, (gx + 18, s * 27, 0), BRICK_Y, verts=16))
        w.append(crest(f"{tag}_mgtc{s}", 13, 13, 26, (gx + 18, s * 27), BRICK_Y, 1.0, "box"))
    w.append(crest(f"{tag}_mgc", 44, 54, 22, (gx, 0), BRICK_Y, 1.2, "box"))
    # arcaded passage through the residential ring
    L = R_RES1 - R_RES0 + 12
    px = (R_RES0 + R_RES1) / 2 - 2
    p = [box(f"{tag}_ps", L, 18, 9, (px, 0, 0.3), BRICK_L)]
    p.append(frustum(f"{tag}_pr", L, 18, L, 7, 2.2, (px, 0, 9.3), shade(BRICK_L, -0.06)))
    for s, f in ((-1, "S"), (1, "N")):
        p.append(arcade(f"{tag}_pa{s}", L * 0.96, 6.5, 22, (px, s * 9.05, 0.3), f, DARK, True, 0.64))
    p.append(box(f"{tag}_ig", 16, 30, 12, (R_IN[0] - 4, 0, 0), BRICK_Y))
    p.append(arch_panel(f"{tag}_iga", 6, 9, (R_IN[0] - 12.1, 0, 0), "W", DARK, True, 0.4))
    p.append(crest(f"{tag}_igc", 16, 30, 12, (R_IN[0] - 4, 0), BRICK_Y, 1.0, "box"))
    # the audience hall above the gate with its dome and a weather-vane figure
    d = [box(f"{tag}_hall", 28, 28, 9, (gx, 0, 22), PLAST), arcade(f"{tag}_hw", 26, 6, 3, (gx + 14.05, 0, 23), "E", DARK, True, 0.6),
         arcade(f"{tag}_hw2", 26, 6, 3, (gx - 14.05, 0, 23), "W", DARK, True, 0.6)]
    d.append(pdome(f"{tag}_dome", 12, (gx, 0, 31), dome_color, k=1.3, drum_h=2.5, drum_color=PLAST, windows_n=8))
    d.append(cylinder(f"{tag}_vane", 0.3, 4, (gx, 0, 49.5), BRONZE, verts=6))
    d.append(box(f"{tag}_vanef", 2.8, 0.6, 1.8, (gx, 0, 52.5), BRONZE))
    return join(w, f"{tag}_walls"), join(p, f"{tag}_passage"), join(d, f"{tag}_domes")


def residential_ring(name, rng, gaps, half=0.032, sectors=15, rows=2):
    """The ring of officers' fiefs between the main and inner walls: blocks between radial lanes (sikak), with courtyard houses."""
    walls, courts, paths = [], [], []
    rr = [(R_RES0 + 6, (R_RES0 + R_RES1) / 2 - 6), ((R_RES0 + R_RES1) / 2 + 6, R_RES1 - 10)]
    for a0, a1 in arcs_between(gaps, half):
        for k in range(sectors):
            s0 = a0 + (a1 - a0) * k / sectors
            s1 = a0 + (a1 - a0) * (k + 1) / sectors
            for (r0, r1) in rr[:rows]:
                nr, nt = 3, 2
                for i in range(nr):
                    ra = r0 + (r1 - r0) * i / nr
                    rb = r0 + (r1 - r0) * (i + 1) / nr
                    rm = (ra + rb) / 2
                    lane = 4.0 / rm
                    for j in range(nt):
                        ta = s0 + lane + (s1 - s0 - 2 * lane) * j / nt
                        tb = s0 + lane + (s1 - s0 - 2 * lane) * (j + 1) / nt
                        tm = (ta + tb) / 2
                        dr, dt = (rb - ra) - 3.0, (tb - ta) * rm - 3.0
                        h = rng.uniform(6.0, 9.5)
                        walls.append((rm * math.cos(tm), rm * math.sin(tm), dr, dt, h, 0.35, tm))
                        courts.append((rm * math.cos(tm), rm * math.sin(tm), dr * 0.42, dt * 0.42, 0.1, 0.35 + h + 0.02, tm))
    cols = {}
    for k, wsp in enumerate(walls):
        cols.setdefault(k % 3, []).append(wsp)
    out = [boxes(f"{name}_h{c}", lst, HOUSES[c]) for c, lst in cols.items()]
    out.append(boxes(name + "_c", courts, "#6E5A44"))
    return join(out, name)


def round_city(variant="770"):
    m = Model("round-city")
    rng = random.Random(762)
    gaps = [math.radians(a) for a in GATE_ANG.values()]
    m.add(0, cylinder("rc_ground", 1200, 0.3, (0, 0, 0), SAND, verts=128), "ground")
    if variant == "1200":
        return round_city_ruins(m, rng, gaps)
    m.add(0, annulus("rc_moat", R_MOAT[0], R_MOAT[1], 0.42, n=160, color=WATER))
    m.add(0, annulus("rc_ringroad", R_RES0 - 2, R_RES1 + 6, 0.33, n=160, color=ROAD))
    m.add(0, cylinder("rc_plaza", R_IN[0], 0.32, (0, 0, 0), PAVE, verts=128))
    # walls: outer, main (with towers) and inner, interrupted at the four gates
    walls = []
    for i, (a0, a1) in enumerate(arcs_between(gaps, 0.016)):
        walls.append(annulus(f"rc_out{i}", R_OUT[0], R_OUT[1], 8.5, a0, a1, color=BRICK_Y))
    for i, (a0, a1) in enumerate(arcs_between(gaps, 0.022)):
        walls.append(annulus(f"rc_main{i}", R_MAIN0, R_MAIN1, 18, a0, a1, color=BRICK_Y))
        walls.append(annulus(f"rc_mainp{i}", R_MAIN1 - 3, R_MAIN1, 1.6, a0, a1, z=18, color=shade(BRICK_Y, -0.06)))
        walls.append(annulus(f"rc_mainb{i}", R_MAIN1 - 0.1, R_MAIN1 + 0.25, 0.6, a0, a1, z=9, color=BRICK_D))
        twr = []
        n = 28
        for k in range(1, n + 1):
            a = a0 + (a1 - a0) * k / (n + 1)
            twr.append(cylinder(f"rc_tw{i}_{k}", 7, 21, ((R_MAIN1 + 1) * math.cos(a), (R_MAIN1 + 1) * math.sin(a), 0), shade(BRICK_Y, -0.04), verts=12))
        walls.append(join(twr, f"rc_towers{i}"))
    for i, (a0, a1) in enumerate(arcs_between(gaps, 0.012)):
        walls.append(annulus(f"rc_in{i}", R_IN[0], R_IN[1], 7, a0, a1, color=BRICK_Y))
    m.add(1, join(walls, "rc_walls"), "walls")
    # gates
    gw, gp, gd = [], [], []
    for tag, ang in GATE_ANG.items():
        a, b, c = gate_complex("rc_" + tag)
        gw.append(rot(a, ang))
        gp.append(rot(b, ang))
        gd.append(rot(c, ang))
    m.add(1, join(gw, "rc_gates"))
    # the ring of fiefs, the passages, the offices round the plaza and the avenues
    res = [residential_ring("rc_res", rng, gaps)]
    res += gp
    offices = []
    for a0, a1 in arcs_between(gaps, 0.06):
        n = 7
        for k in range(n):
            t = a0 + (a1 - a0) * (k + 0.5) / n
            offices.append((790 * math.cos(t), 790 * math.sin(t), 44, (a1 - a0) / n * 790 * 0.6, 8.0, 0.32, t))
    res.append(boxes("rc_offices", offices, PLAST))
    res.append(boxes("rc_officec", [(x, y, w * 0.45, d * 0.5, 0.1, 8.34, t) for (x, y, w, d, h, z, t) in offices], "#6E5A44"))
    av = []
    for tag, ang in GATE_ANG.items():
        a = math.radians(ang)
        r_end = 235 if tag == "basra" else 120
        L = R_IN[0] - r_end
        rm = (R_IN[0] + r_end) / 2
        av.append((rm * math.cos(a), rm * math.sin(a), L, 16, 0.12, 0.32, a))
    res.append(boxes("rc_avenues", av, ROAD))
    m.add(2, join(res, "rc_quarters"), "quarters")
    if variant == "770":
        # market stalls still crowding the plaza ends of the passages before 773
        st = []
        for tag, ang in GATE_ANG.items():
            a = math.radians(ang)
            for k in range(10):
                r = R_IN[0] - 30 - (k // 2) * 9
                off = (k % 2 * 2 - 1) * 16
                st.append((r * math.cos(a) - off * math.sin(a), r * math.sin(a) + off * math.cos(a), 6, 5, 3.0, 0.32, a))
        m.add(2, boxes("rc_stalls", st, "#C8B08A"))
    m.add(3, join(gd, "rc_gate_domes"), "gate domes")
    return m


def round_city_ruins(m, rng, gaps):
    """Madinat al-Mansur about 1200: the walls fallen to mounds and stumps, a quarter round the mosque, gardens on the rest."""
    m.add(0, annulus("rcr_moat", R_MOAT[0], R_MOAT[1], 0.36, n=160, color="#9C9A72"))
    m.add(0, cylinder("rcr_in", R_RES1, 0.33, (0, 0, 0), "#D2C29C", verts=128))
    mounds, stumps = [], []
    for i in range(70):
        a = rng.uniform(0, math.tau)
        L = rng.uniform(30, 110) / R_MAIN1
        if rng.random() < 0.55:
            stumps.append(annulus(f"rcr_w{i}", R_MAIN0 + 3, R_MAIN1 - 3, rng.uniform(4.0, 12.0), a, a + L, n=4, color=BRICK_D))
        else:
            r = (R_MAIN0 + R_MAIN1) / 2
            mounds.append((r * math.cos(a + L / 2), r * math.sin(a + L / 2), L * r, 34, rng.uniform(2.5, 6.0), 0.3, a + L / 2 + math.pi / 2))
    for i in range(30):
        a = rng.uniform(0, math.tau)
        L = rng.uniform(20, 70) / R_OUT[1]
        stumps.append(annulus(f"rcr_o{i}", R_OUT[0], R_OUT[1], rng.uniform(1.0, 4.0), a, a + L, n=3, color=shade(BRICK_Y, -0.1)))
    m.add(1, join(stumps + [boxes("rcr_mounds", mounds, DUST)], "rcr_walls"), "ruined walls")
    # mounds of the old houses and the remains of the Khurasan gate
    hm = []
    for i in range(160):
        a = rng.uniform(0, math.tau)
        r = rng.uniform(R_RES0, R_RES1)
        hm.append((r * math.cos(a), r * math.sin(a), rng.uniform(25, 70), rng.uniform(25, 60), rng.uniform(0.8, 3.0), 0.3, a))
    g = math.radians(GATE_ANG["khurasan"])
    gx = (R_MAIN0 + R_MAIN1) / 2
    gate = place(join([box("rcr_g", 36, 40, 14, (0, 0, 0), BRICK_Y), arch_panel("rcr_ga", 8, 10, (18.1, 0, 0), "E", DARK, True, 0.5),
                       shallow_dome("rcr_gd", 9, (0, 0, 14), shade(BRICK_Y, -0.1), rise=0.4)], "rcr_gate"), gx * math.cos(g), gx * math.sin(g), GATE_ANG["khurasan"])
    m.add(1, join([boxes("rcr_hm", hm, DUST), gate], "rcr_mounds2"))
    # the old palace walls, broken (its Green Dome fell in 941)
    pw = []
    for k in range(4):
        for j in range(5):
            if rng.random() < 0.7:
                u = -80 + j * 40
                h = rng.uniform(3, 9)
                x, y = [(u, -98), (u, 98), (98, u), (-98, u)][k]
                pw.append((x, y, 30 if k < 2 else 4, 4 if k < 2 else 30, h, 0.3))
    pal = boxes("rcr_palace", pw, shade(BRICK_Y, -0.04))
    m.add(2, rot(pal, 45), "quarter")
    # the quarter round al-Mansur's mosque (the mosque itself is its own landmark, south-east of the centre)
    hs = []
    a_m = math.radians(315)
    for i in range(140):
        a = a_m + rng.uniform(-0.6, 0.6)
        r = rng.uniform(260, 700)
        hs.append((r * math.cos(a), r * math.sin(a), rng.uniform(8, 15), rng.uniform(8, 14), rng.uniform(5, 8)))
    for i in range(60):
        a = math.radians(GATE_ANG["basra"]) + rng.uniform(-0.05, 0.05)
        r = rng.uniform(720, 1150)
        hs.append((r * math.cos(a), r * math.sin(a), rng.uniform(8, 14), rng.uniform(8, 12), rng.uniform(5, 7)))
    m.add(2, houses("rcr_houses", hs, 0.33))
    pl = []
    for i in range(140):
        a = rng.uniform(0, math.tau)
        r = rng.uniform(250, 1050)
        if abs(((a - a_m + math.pi) % math.tau) - math.pi) < 0.7 and r < 720:
            continue
        pl.append((r * math.cos(a), r * math.sin(a)))
    m.add(3, palms("rcr_palm", pl, 6.0, 0.33), "gardens")
    return m


# ---------------------------------------------------------------- the palace and the mosque

def golden_gate_palace():
    m = Model("golden-gate-palace")
    m.add(0, ground("gg_g", 200, 200, PAVE), "ground")
    # outer wall with half-round buttresses and the Golden Gate on the front
    pts = [(-99, -99), (99, -99), (99, 99), (-99, 99), (-99, -99)]
    w = [abbasid_wall("gg_wall", pts, 12, 3.0, BRICK_Y, 3.2, 16)]
    w.append(bands("gg_wb", 198, 198, 3, 11.5, (0, 0), BRICK_D, 4.0, 0.45, 0.25))
    w.append(portal("gg_gate", 30, 22, 6, (0, -100, 0), "S", BRICK_Y, BRICK_L, hood=True))
    w.append(box("gg_golden", 6.5, 0.6, 9, (0, -103.6, 0), GILT))
    m.add(0, join(w, "gg_walls"), "walls")
    # ranges of rooms round the walls, and wings cutting the inside into four courts
    r = [courtyard_ring("gg_ring", 190, 190, 10, 16, (0, 0, 0.3), BRICK_L, DARK)]
    r.append(box("gg_wx", 158, 12, 10, (0, 47, 0.3), BRICK_L))
    r.append(arcade("gg_wxa", 150, 7, 22, (0, 47 - 6.05, 0.3), "S", DARK, True, 0.7))
    r.append(arcade("gg_wxb", 150, 7, 22, (0, 47 + 6.05, 0.3), "N", DARK, True, 0.7))
    r.append(crest("gg_ringc", 190, 190, 10.3, (0, 0), BRICK_L, 0.8, "stepped"))
    # gardens and pools in the four courts
    g = []
    for k, (cx, cy, lw, ld) in enumerate(((-45, 66, 60, 20), (45, 66, 60, 20), (-56, -12, 34, 40), (56, -12, 34, 40))):
        g.append(box(f"gg_lawn{k}", lw, ld, 0.35, (cx, cy, 0.3), GREEN))
        g.append(box(f"gg_pool{k}", lw * 0.25, ld * 0.25, 0.45, (cx, cy, 0.3), WATER))
        g.append(trees(f"gg_tr{k}", [(cx - lw * 0.33, cy), (cx + lw * 0.33, cy), (cx, cy - ld * 0.33), (cx, cy + ld * 0.33)], 2.2, 0.3))
    g.append(box("gg_fore", 40, 50, 0.15, (0, -52, 0.3), PAVE))
    r.append(join(g, "gg_gardens"))
    m.add(1, join([x for x in r if x], "gg_ranges"), "courts")
    # the central block: forecourt iwan, square audience hall, upper chamber, the Green Dome and its horseman
    c = [box("gg_core", 46, 46, 18, (0, 0, 0.3), BRICK_L), bands("gg_coreb", 46, 46, 3, 18, (0, 0), BRICK_D, 3.5, 0.45, 0.2),
         crest("gg_corec", 46, 46, 18.3, (0, 0), BRICK_L, 0.8, "stepped")]
    c.append(iwan("gg_iwan", 16, 17, 3.0, (0, -24.5, 0.3), "S", BRICK_Y, BRICK_L))
    for f in ("E", "W", "N"):
        dx, dy = {"E": (23.05, 0), "W": (-23.05, 0), "N": (0, 23.05)}[f]
        c.append(arch_panel(f"gg_cd{f}", 6, 10, (dx, dy, 0.3), f, DARK, True, 0.4))
    c.append(windows("gg_cw", 40, 6, 11, 4.0, (0, -23.05), "S", 0.32))
    c.append(box("gg_upper", 24, 24, 9, (0, 2, 18.3), PLAST))
    c.append(blind_arcade_faces("gg_upa", 24, 24, 19.5, 6, 6, 0, 2, 0.6))
    c.append(cylinder("gg_drum", 11.2, 5, (0, 2, 27.3), PLAST, verts=32))
    c.append(face_panels("gg_drw", 11.2, 16, 1.8, 3.4, 28.0, (0, 2, 0), DARK, True, 1))
    m.add(2, join(c, "gg_audience"), "audience hall")
    d = [lathe("gg_green", pointed_profile(11, 1.25, 0.03, 14), (0, 2, 32.3), GREEN_DOME, verts=40)]
    top = 32.3 + pointed_profile(11, 1.25)[-1][1]
    d.append(cylinder("gg_ped", 0.8, 1.2, (0, 2, top - 0.3), BRONZE, verts=8))
    d.append(box("gg_horse", 3.2, 1.0, 1.3, (0, 2, top + 0.9), BRONZE))
    for sx in (-1, 1):
        d.append(box(f"gg_leg{sx}", 0.35, 0.9, 1.0, (sx * 1.2, 2, top), BRONZE))
    d.append(box("gg_neck", 0.6, 0.8, 1.2, (1.6, 2, top + 1.8), BRONZE))
    d.append(cylinder("gg_rider", 0.4, 1.5, (-0.2, 2, top + 2.2), BRONZE, verts=8))
    d.append(box("gg_lance", 4.0, 0.15, 0.15, (0.8, 2, top + 3.3), BRONZE, rot_z=0.0))
    m.add(3, join(d, "gg_green_dome"), "Green Dome")
    return m


def mansur_mosque(variant="809"):
    m = Model("mansur-mosque")
    col = MUD if variant == "763" else BRICK_Y
    m.add(0, ground("mm_g", 100, 100, PAVE), "ground")
    shell, inner = court_mosque("mm", 94, 90, 10, 32, 10, 10, col, (0, -4, 0), roof=MUD_L if variant == "763" else BRICK_L)
    m.add(0, shell, "walls")
    m.add(1, inner, "halls")
    t = []
    if variant != "763":
        # half-round buttresses on the outer walls, as on Abbasid mosques at Samarra
        tw = []
        for k in range(7):
            u = -39 + k * 13
            for (x, y) in ((u, -49.4), (u, 41.4)):
                tw.append(cylinder(f"mm_bt{len(tw)}", 1.8, 11, (x, y, 0), shade(col, -0.05), verts=10))
            v = -45 + k * 13
            for x in (-47.4, 47.4):
                tw.append(cylinder(f"mm_bt{len(tw)}", 1.8, 11, (x, v, 0), shade(col, -0.05), verts=10))
        t.append(join(tw, "mm_buttresses"))
        t.append(bands("mm_b", 94, 90, 2.5, 9.5, (0, -4), BRICK_D, 3.5, 0.4, 0.2))
        t.append(round_minaret("mm_min", 2.6, 30, (0, 45.2, 0), BRICK_Y, BRICK_L, True, "cap"))
        t.append(box("mm_mihp", 8, 2.5, 11.5, (0, -50.6, 0), col))
        t.append(box("mm_fount", 6, 6, 3.0, (0, 6, 0.15), BRICK_L))
        t.append(pdome("mm_fountd", 3.0, (0, 6, 3.15), BRICK_L, k=1.2, drum_h=0, top=False))
    else:
        # the first mosque: mud brick and a flat roof on wooden columns, some single tree trunks
        cols = [cylinder(f"mm_col{i}", 0.45, 6.5, (-30 + i * 6, -19.2, 0.15), WOOD, verts=8) for i in range(11)]
        t.append(join(cols, "mm_cols"))
        t.append(box("mm_fount", 5, 5, 0.5, (0, 6, 0.15), WATER))
        t.append(palms("mm_palm", [(-20, 14), (20, 19), (0, 24)], 2.2, 0.15))
    for s in (-1, 1):
        t.append(arch_panel(f"mm_door{s}", 4.5, 7, (s * 47.1, 16, 0), "E" if s > 0 else "W", DARK, True, 0.4))
    m.add(2, join(t, "mm_tower"), "minaret")
    return m


# ---------------------------------------------------------------- palaces by the river

def khuld_palace():
    """Front (-Y) is the river side: quay, water gate and the audience hall facing the Tigris."""
    m = Model("khuld-palace")
    m.add(0, ground("kh_g", 300, 220, "#CDBE98"), "ground")
    m.add(0, box("kh_quay", 300, 16, 1.6, (0, -102, 0), BRICK_D))
    m.add(0, stair("kh_steps", 30, 1.6, 6, 6, (0, -110, 0), "S", BRICK_D))
    pts = [(-146, -92), (146, -92), (146, 106), (-146, 106), (-146, -92)]
    w = [abbasid_wall("kh_wall", pts, 9, 2.4, BRICK_Y, 2.8, 20)]
    w.append(portal("kh_watergate", 22, 16, 5, (0, -93, 0), "S", BRICK_Y, BRICK_L))
    w.append(portal("kh_landgate", 18, 14, 5, (-70, 107, 0), "N", BRICK_Y, BRICK_L, hood=False))
    m.add(1, join(w, "kh_walls"), "walls")
    b = [box("kh_hall", 54, 40, 14, (0, -50, 0.3), BRICK_L), bands("kh_hb", 54, 40, 3, 14, (0, -50), BRICK_D, 3.5, 0.45)]
    b.append(iwan("kh_iwan", 16, 16, 3, (0, -71.5, 0.3), "S", BRICK_Y, BRICK_L))
    b.append(arcade("kh_hallarc", 50, 8, 6, (0, -70.1, 0.3), "S", DARK, True, 0.55))
    b.append(crest("kh_hc", 54, 40, 14.3, (0, -50), BRICK_L, 0.8, "stepped"))
    b.append(courtyard_ring("kh_c1", 90, 70, 9, 11, (-90, 30, 0.3), BRICK_L))
    b.append(courtyard_ring("kh_c2", 80, 64, 9, 10, (95, 25, 0.3), BRICK_L))
    b.append(courtyard_ring("kh_c3", 70, 50, 8, 9, (0, 70, 0.3), BRICK_L))
    b.append(box("kh_c3pave", 50, 30, 0.1, (0, 70, 0.3), PAVE))
    b.append(houses("kh_serv", [(-125, -70, 30, 18, 7), (125, -70, 30, 18, 7), (-125, 85, 26, 30, 7), (125, 85, 26, 30, 7)]))
    m.add(2, join(b, "kh_halls"), "halls")
    g = [charbagh("kh_garden", 120, 70, (0, -2, 0.3), path_color=BRICK_L, trees=True)]
    g.append(palms("kh_palm", [(-140, -80), (-110, -82), (-80, -80), (80, -80), (110, -82), (140, -80), (-60, -10), (60, -10), (-62, 15), (62, 15)], 2.6))
    g.append(pdome("kh_dome", 12, (0, -50, 14.3), GREEN_DOME, k=1.3, drum_h=3, drum_color=PLAST))
    for s in (-1, 1):
        g.append(pdome(f"kh_pav{s}", 4.5, (s * 120, -85, 7.3), PLAST, k=1.2, drum_h=0.5))
        g.append(box(f"kh_pavb{s}", 12, 10, 7, (s * 120, -85, 0.3), BRICK_L))
        g.append(arcade(f"kh_pava{s}", 11, 5, 3, (s * 120, -90.05, 0.3), "S", DARK, True, 0.7))
    m.add(3, join(g, "kh_dome_gardens"), "dome and gardens")
    m.add(3, join([boat("kh_boat1", 16, (-60, -104), 0, sail=False), boat("kh_boat2", 14, (40, -105), 180, sail=False)], "kh_boats"))
    return m


def rusafa(variant="800"):
    m = Model("rusafa")
    m.add(0, ground("ru_g", 300, 220, "#D2C29C"), "ground")
    shell, inner = court_mosque("ru_m", 110, 100, 10, 34, 10, 10, BRICK_Y, (-85, 0, 0))
    m.add(0, shell, "mosque")
    m.add(1, inner)
    m.add(1, round_minaret("ru_min", 2.8, 30, (-85, 53, 0), BRICK_Y, BRICK_L))
    if variant == "1200":
        tombs = []
        for i, (x, y) in enumerate([(20, -40), (45, -55), (70, -35), (25, 10), (60, 20), (95, -10), (110, 45), (40, 60), (80, 75), (120, -70)]):
            tombs.append(box(f"ru_t{i}", 9, 9, 6, (x, y, 0.3), BRICK_L))
            tombs.append(pdome(f"ru_td{i}", 3.6, (x, y, 6.3), BRICK_L if i % 3 else TURQ, k=1.4, drum_h=0.6, windows_n=0))
        graves = [(rng_x, rng_y, 2.0, 1.0, 0.6, 0.3) for rng_x, rng_y in [(10 + 9 * (i % 12), -90 + 14 * (i // 12)) for i in range(84)]]
        tombs.append(boxes("ru_graves", graves, "#D9CFB8"))
        m.add(2, join(tombs, "ru_cemetery"), "tombs of the caliphs")
        m.add(3, palms("ru_palm", [(-140, 80), (-140, -80), (140, 90), (-30, 90), (-30, -95), (140, 20), (0, 80)], 2.6), "palms")
        return m
    pts = [(-20, -100), (140, -100), (140, 100), (-20, 100), (-20, -100)]
    m.add(1, abbasid_wall("ru_wall", pts, 9, 2.2, BRICK_Y, 2.6, 22), "palace walls")
    p = [box("ru_hall", 40, 34, 13, (60, -30, 0.3), BRICK_L), iwan("ru_iwan", 14, 15, 3, (60, -48, 0.3), "S", BRICK_Y, BRICK_L),
         crest("ru_hc", 40, 34, 13.3, (60, -30), BRICK_L, 0.8)]
    p.append(courtyard_ring("ru_c1", 60, 50, 8, 9, (40, 55, 0.3), BRICK_L))
    p.append(courtyard_ring("ru_c2", 50, 60, 8, 9, (110, 40, 0.3), BRICK_L))
    p.append(charbagh("ru_garden", 70, 44, (55, -73, 0.3), path_color=BRICK_L))
    p.append(houses("ru_barracks", [(-130, 85, 30, 16, 6), (-130, -85, 30, 16, 6), (-128, 40, 26, 40, 6), (-128, -40, 26, 40, 6)]))
    m.add(2, join(p, "ru_palace"), "palace")
    m.add(3, pdome("ru_dome", 9, (60, -30, 13.3), GREEN_DOME, k=1.3, drum_h=2.0, drum_color=PLAST), "dome")
    m.add(3, palms("ru_palm", [(-140, 0), (0, 100), (135, -90), (-20, -105), (100, -90)], 2.6))
    return m


def bridge_of_boats():
    """Spans along X; the river runs along Y. Boats in a line, a planked deck, chains to brick abutments with toll houses."""
    m = Model("bridge-of-boats")
    m.add(0, box("bb_water", 270, 30, 0.12, (0, 0, 0), WATER), "river")
    ab = []
    for s in (-1, 1):
        cx = s * 172
        ab.append(box(f"bb_bank{s}", 76, 30, 0.6, (cx, 0, 0), SAND))
        ab.append(box(f"bb_pier{s}", 30, 16, 3.0, (s * 145, 0, 0), BRICK_D))
        ab.append(stair(f"bb_ramp{s}", 9, 3.0, 12, 6, (s * 166, 0, 0), "E" if s > 0 else "W", BRICK_D))
        ab.append(flat_house(f"bb_toll{s}", 9, 8, 5, (s * 158, 12, 3.0), BRICK_L, True, "S"))
        ab.append(flat_house(f"bb_guard{s}", 7, 7, 4.5, (s * 158, -12, 3.0), BRICK_L, True, "N"))
        for k in (-1, 1):
            ab.append(cylinder(f"bb_post{s}{k}", 0.6, 5, (s * 132, k * 6.5, 3.0), WOOD_D, verts=8))
    m.add(0, join(ab, "bb_abutments"), "abutments")
    hulls = []
    n = 46
    for i in range(n):
        x = -126 + i * 252 / (n - 1)
        L, W = 17.0, 4.4
        pts = [(0, -L / 2), (W / 2, -L * 0.32), (W / 2, L * 0.32), (0, L / 2), (-W / 2, L * 0.32), (-W / 2, -L * 0.32)]
        hulls.append(prism(f"bb_h{i}", [(px + x, py) for px, py in pts], 1.5, (0, 0, 0), WOOD if i % 2 else shade(WOOD, 0.12)))
    m.add(1, join(hulls, "bb_boats"), "boats")
    deck = [box("bb_deck", 256, 7, 0.5, (0, 0, 1.5), "#9C7A52")]
    deck.append(boxes("bb_planks", [(-126 + k * 4.2, 0, 0.5, 7.2, 0.12, 2.0) for k in range(61)], shade("#9C7A52", -0.15)))
    rails = []
    for s in (-1, 1):
        rails.append((0, s * 3.4, 256, 0.25, 0.25, 3.0))
        for k in range(33):
            rails.append((-126 + k * 7.875, s * 3.4, 0.25, 0.25, 1.2, 2.0))
    deck.append(boxes("bb_rail", rails, WOOD_D))
    chains = [(s * 136, k * 6.5, 14, 0.25, 0.25, 2.6) for s in (-1, 1) for k in (-1, 1)]
    deck.append(boxes("bb_chains", chains, "#5A5650"))
    m.add(2, join(deck, "bb_deck_all"), "deck")
    m.add(3, join([boat("bb_b1", 15, (-60, 14), 90), boat("bb_b2", 13, (70, -13), -90, sail=False)], "bb_traffic"), "boats")
    return m


# ---------------------------------------------------------------- learning

def bayt_al_hikma():
    m = Model("bayt-al-hikma")
    m.add(0, ground("bh_g", 90, 70, "#D6C7A2"), "ground")
    m.add(0, abbasid_wall("bh_wall", [(-44, -34), (44, -34), (44, 34), (-44, 34), (-44, -34)], 6, 1.4, BRICK_Y, 1.6, 14), "walls")
    r = [courtyard_ring("bh_ring", 62, 44, 9, 9, (-8, 4, 0.3), BRICK_L), box("bh_pave", 44, 26, 0.1, (-8, 4, 0.3), PAVE),
         box("bh_pool", 8, 5, 0.4, (-8, 4, 0.3), WATER), crest("bh_crest", 62, 44, 9.3, (-8, 4), BRICK_L, 0.6)]
    r.append(windows("bh_win", 56, 8, 4.5, 2.6, (-8, 26.05), "N", 0.3))
    r.append(windows("bh_wins", 56, 8, 4.5, 2.6, (-8, -18.05), "S", 0.3))
    r.append(portal("bh_gate", 12, 11, 3, (-8, -19, 0.3), "S", BRICK_Y, BRICK_L))
    m.add(1, join(r, "bh_courts"), "book rooms")
    h = [box("bh_hall", 18, 18, 11, (31, 4, 0.3), BRICK_L), iwan("bh_iwan", 9, 10, 2, (21.5, 4, 0.3), "W", BRICK_Y, BRICK_L)]
    h.append(pdome("bh_dome", 7.5, (31, 4, 11.3), BRICK_L, k=1.3, drum_h=1.6))
    h.append(trees("bh_tr", [(-8, -28), (20, -27), (36, -26), (30, 28), (38, 26)], 2.2))
    h.append(palms("bh_palm", [(-38, -28), (-38, 28)], 2.0))
    m.add(2, join(h, "bh_hall_dome"), "reading hall")
    return m


def shammasiyya_observatory():
    m = Model("shammasiyya-observatory")
    m.add(0, ground("ob_g", 60, 50, "#D3C39C"), "ground")
    m.add(0, wall_run("ob_encl", [(-29, -24), (29, -24), (29, 24), (-29, 24), (-29, -24)], 2.4, 0.8, color=BRICK_L, towers=False, merlon=None))
    m.add(0, box("ob_plat", 34, 30, 1.2, (4, -2, 0.3), BRICK_D), "platform")
    # the meridian wall (north-south) carrying a graduated arc
    mw = [box("ob_mwall", 2.2, 24, 11, (-4, -2, 1.5), BRICK_Y), bands("ob_mwb", 2.2, 24, 2.5, 11, (-4, -2), BRICK_D, 3.0, 0.35)]
    arc = []
    R = 9.5
    for k in range(25):
        a = math.radians(5 + k * 80 / 24)
        arc.append((-2.8, -2 - 11 + R * math.cos(a) * 1.0 + 1.5, 0.3, 0.9, 0.5, 1.5 + R * math.sin(a)))
    mw.append(boxes("ob_arc", [(x, y, w, d, h, z) for (x, y, w, d, h, z) in arc], BRONZE))
    mw.append(box("ob_stair", 3, 6, 1.0, (-1, 8, 1.5), BRICK_D))
    m.add(1, join(mw, "ob_meridian"), "meridian wall")
    ins = [cylinder("ob_gnomon", 0.7, 12, (14, -8, 1.5), BRICK_L, verts=12), cylinder("ob_gtop", 1.0, 0.6, (14, -8, 13.5), BRONZE, verts=12)]
    ins.append(box("ob_line", 0.4, 16, 0.1, (14, 2, 1.5), BRONZE))
    # an armillary sphere: rings on a stand
    sx, sy, sz = 12, 7, 1.5
    ins.append(cylinder("ob_stand", 0.4, 2.6, (sx, sy, sz), BRONZE, verts=8))
    for k, ang in enumerate((0, 60, 120)):
        ringo = annulus(f"ob_ring{k}", 2.2, 2.5, 0.25, n=24, color=BRONZE)
        ringo = rot(ringo, 0)
        ringo.rotation_euler[0] = math.radians(90)
        ringo.rotation_euler[2] = math.radians(ang)
        ins.append(move(ringo, sx, sy, sz + 4.8))
    ins.append(annulus("ob_eq", 2.3, 2.55, 0.25, n=24, z=sz + 4.7, color=BRONZE))
    ins[-1] = move(ins[-1], sx, sy, 0)
    m.add(2, join(ins, "ob_instruments"), "instruments")
    hs = [box("ob_house", 12, 10, 6, (-20, 14, 0.3), BRICK_L), pdome("ob_hd", 4.4, (-20, 14, 6.3), BRICK_L, k=1.25, drum_h=0.8, windows_n=4),
          arch_panel("ob_hdoor", 2, 3.5, (-20, 8.95, 0.3), "S", DARK, True, 0.3), flat_house("ob_store", 10, 7, 4.5, (-20, -15, 0.3), BRICK_L, True, "N")]
    hs.append(trees("ob_tr", [(24, 18), (-26, 2), (24, -20)], 2.0))
    m.add(3, join(hs, "ob_house_all"), "house")
    return m


# ---------------------------------------------------------------- Karkh

def karkh_market():
    m = Model("karkh-market")
    m.add(0, ground("km_g", 260, 180, "#D2C29E"), "ground")
    m.add(0, box("km_canal", 260, 12, 0.35, (0, -84, 0), WATER))
    m.add(0, box("km_quay", 260, 6, 1.0, (0, -75, 0), BRICK_D))
    shops, vault, doors = [], [], []
    rows = [-40, 8, 56]
    for j, y in enumerate(rows):
        L = 190 if j != 1 else 150
        x0 = -20 if j == 1 else -25
        for s in (-1, 1):
            shops.append((x0, y + s * 8.5, L, 9, 5.5, 0.3))
            doors.append(arcade(f"km_d{j}{s}", L * 0.97, 3.2, int(L / 4.2), (x0, y + s * 4.0 - s * 0.05, 0.3), "N" if s < 0 else "S", DARK, False, 0.62, 0.2))
        v = frustum(f"km_v{j}", L, 8, L, 2.2, 2.6, (x0, y, 5.8), shade(BRICK_L, -0.05))
        vault.append(v)
        vault.append(boxes(f"km_vl{j}", [(x0 - L / 2 + k * L / 10, y, 1.2, 2.4, 0.8, 8.4) for k in range(1, 10)], BRICK_L))
    m.add(1, join([boxes("km_shops", shops, BRICK_L)] + doors, "km_shoprows"), "market streets")
    m.add(2, join(vault, "km_vaults"), "vaults")
    k = [courtyard_ring("km_khan", 50, 46, 9, 8, (98, 30, 0.3), BRICK_Y), portal("km_khang", 12, 11, 3, (98, 7.5, 0.3), "S", BRICK_Y, BRICK_L, hood=False),
         box("km_khanp", 34, 30, 0.1, (98, 30, 0.3), PAVE)]
    k.append(box("km_mosque", 26, 22, 8, (-110, -40, 0.3), BRICK_L))
    k.append(pdome("km_md", 5.5, (-110, -40, 8.3), BRICK_L, k=1.3, drum_h=1.0))
    k.append(round_minaret("km_min", 1.6, 20, (-121, -27, 0.3), BRICK_Y, BRICK_L))
    k.append(houses("km_store", [(-100 + i * 26, -63, 22, 12, 6) for i in range(8)]))
    k.append(houses("km_h", [(-105, 30, 14, 12, 7), (-108, 70, 16, 12, 8), (60, 80, 14, 12, 7), (115, 76, 16, 14, 8), (-60, 82, 18, 10, 7), (0, 82, 14, 10, 7),
                             (110, -20, 16, 14, 7), (60, -20, 14, 12, 6)]))
    k.append(join([boat("km_boat1", 12, (-60, -84), 0, sail=False), boat("km_boat2", 13, (30, -84), 180), boat("km_boat3", 11, (90, -84), 0, sail=False)], "km_boats"))
    m.add(3, join(k, "km_khan_mosque"), "khan and mosque")
    return m


# ---------------------------------------------------------------- the shrine of the Kazimayn

def kazimayn(variant="1650"):
    m = Model("kazimayn")
    m.add(0, ground("kz_g", 140, 120, "#D8CAA6"), "ground")
    if variant == "800":
        enc = [wall_run("kz_encl", [(-60, -50), (60, -50), (60, 50), (-60, 50), (-60, -50)], 2.6, 0.9, color=MUD, towers=False, merlon=None)]
        g = [(x, y, 2.2, 1.0, 0.6, 0.3) for x, y in [(-50 + (i % 14) * 7.5, -40 + (i // 14) * 10) for i in range(84)] if abs(x) > 16 or abs(y) > 14]
        enc.append(boxes("kz_graves", g, "#D9CFB8"))
        m.add(0, join(enc, "kz_cemetery"), "cemetery")
        t = [box("kz_tomb", 14, 12, 5, (0, 0, 0.3), MUD_L), arch_panel("kz_td", 2.2, 3.2, (0, -6.05, 0.3), "S", DARK, False, 0.3),
             wall_run("kz_tw", [(-11, -10), (11, -10), (11, 10), (-11, 10), (-11, -10)], 2.2, 0.6, color=MUD_L, towers=False, merlon=None)]
        m.add(1, join(t, "kz_grave"), "grave")
        m.add(2, palms("kz_palm", [(-30, 20), (30, 22), (-25, -25), (35, -20), (0, 35), (-45, 40), (45, 40)], 2.4), "palms")
        return m
    ring_c = BRICK_L if variant == "1200" else "#E2D6BE"
    m.add(0, courtyard_ring("kz_ring", 138, 118, 9, 9, (0, 0, 0.3), ring_c, DARK), "court")
    m.add(0, crest("kz_rc", 138, 118, 9.3, (0, 0), ring_c, 0.7, "stepped"))
    gates = []
    for f, (x, y) in (("S", (0, -59)), ("N", (0, 59)), ("E", (69, 0)), ("W", (-69, 0))):
        gates.append(portal(f"kz_gate{f}", 14, 14, 4, (x, y, 0.3), f, ring_c if variant == "1200" else BLUE_T, BRICK_L, hood=variant != "1200"))
    m.add(1, join(gates, "kz_gates"), "gates")
    m.add(1, box("kz_pave", 120, 100, 0.12, (0, 0, 0.3), PAVE))
    body_c = BRICK_Y
    s = [box("kz_shrine", 44, 32, 14, (0, 4, 0.3), body_c), crest("kz_sc", 44, 32, 14.3, (0, 4), body_c, 0.7)]
    s.append(blind_arcade_faces("kz_sba", 44, 32, 2.5, 8, 5.5, 0, 4, 0.62))
    if variant == "1200":
        s.append(portal("kz_sp", 14, 16, 3, (0, -12.5, 0.3), "S", BRICK_Y, BRICK_L))
        m.add(2, join(s, "kz_shrine_body"), "shrine")
        d = [pdome(f"kz_d{k}", 7.5, (x, 4, 14.3), BRICK_L, k=1.4, drum_h=2.2) for k, x in enumerate((-11, 11))]
        d.append(round_minaret("kz_min", 1.8, 26, (24, -14, 0.3), BRICK_Y, BRICK_L))
        m.add(3, join(d, "kz_domes"), "domes")
        return m
    # the 17th-century shrine: tiled iwan front, twin domes and four minarets
    s.append(portal("kz_sp", 18, 20, 4, (0, -13, 0.3), "S", BLUE_T, GOLDEN))
    s.append(box("kz_porch", 40, 6, 9, (0, -15, 0.3), "#E6DCC6"))
    s.append(arcade("kz_porcha", 38, 7, 7, (0, -18.05, 0.3), "S", DARK, True, 0.7))
    m.add(2, join(s, "kz_shrine_body"), "shrine")
    d = []
    for k, x in enumerate((-10.5, 10.5)):
        d.append(cylinder(f"kz_dr{k}", 8, 5, (x, 6, 14.3), BLUE_T, verts=32))
        d.append(face_panels(f"kz_drw{k}", 8, 16, 1.2, 3.2, 15.0, (x, 6, 0), DARK, True, 2))
        d.append(onion_dome(f"kz_d{k}", 7.6, (x, 6, 19.3), TURQ, bulb=1.1, height=1.35, drum=0.1, finial=True, finial_color=GILT))
    for k, (x, y) in enumerate(((-21, -15), (21, -15), (-21, 19), (21, 19))):
        d.append(minaret(f"kz_m{k}", 1.7, 32, (x, y, 0.3), BLUE_T, GOLDEN, 2, "lantern", 16, 0.85))
    m.add(3, join(d, "kz_domes"), "domes and minarets")
    return m


# ---------------------------------------------------------------- the late caliphate

def mustansiriya():
    """Long axis along X. The street portal is on +Y (north-east after rotation); -Y is the river side."""
    m = Model("mustansiriya")
    W, D, H = 98, 42, 13.5
    t, rd = 1.6, 8.0
    m.add(0, ground("ms_g", 104, 46, PAVE), "ground")
    cw, cd = W - 2 * (t + rd), D - 2 * (t + rd)
    sh = [box("ms_shell_s", W, t, H, (0, -D / 2 + t / 2, 0.3), BRICK_Y), box("ms_shell_n", W, t, H, (0, D / 2 - t / 2, 0.3), BRICK_Y),
          box("ms_shell_w", t, D - 2 * t, H, (-W / 2 + t / 2, 0, 0.3), BRICK_Y), box("ms_shell_e", t, D - 2 * t, H, (W / 2 - t / 2, 0, 0.3), BRICK_Y)]
    sh.append(box("ms_rooms_s", W - 2 * t, rd, H - 1.2, (0, -D / 2 + t + rd / 2, 0.3), BRICK_L))
    sh.append(box("ms_rooms_n", W - 2 * t, rd, H - 1.2, (0, D / 2 - t - rd / 2, 0.3), BRICK_L))
    sh.append(box("ms_rooms_w", rd, cd, H - 1.2, (-W / 2 + t + rd / 2, 0, 0.3), BRICK_L))
    sh.append(box("ms_rooms_e", rd, cd, H - 1.2, (W / 2 - t - rd / 2, 0, 0.3), BRICK_L))
    sh.append(box("ms_court", cw, cd, 0.12, (0, 0, 0.3), "#E8DCC4"))
    sh.append(box("ms_pool", 10, 3, 0.3, (0, 0, 0.3), WATER))
    m.add(0, join(sh, "ms_shell"), "walls")
    # exterior: two tiers of blind arches in frames, patterned lozenge bands, an inscription frieze and a stepped parapet
    ext = [blind_arcade_faces("ms_x1", W, D, 1.2, 5.0, 4.4, 0, 0, 0.6, BRICK_L), blind_arcade_faces("ms_x2", W, D, 7.6, 4.2, 4.4, 0, 0, 0.55, BRICK_L)]
    ext.append(bands("ms_xb", W, D, 6.4, 7.2, (0, 0), BRICK_D, 9, 0.6, 0.4))
    ext.append(lozenge_faces("ms_lz", W, D, 12.0, 0.45, 0, 0, BRICK_D, 1.6))
    ext.append(bands("ms_frieze", W, D, 11.6, 13.4, (0, 0), shade(BRICK_Y, -0.08), 3, 0.25, 0.3))
    ext.append(crest("ms_parapet", W, D, H + 0.3, (0, 0), BRICK_Y, 0.7, "stepped"))
    m.add(1, join(ext, "ms_facades"), "facades")
    # court: two storeys of pointed arcades in rectangular frames on all four sides
    ct = []
    for tier, (z, h) in enumerate(((0.3, 5.4), (6.6, 4.8))):
        for (L, x, y, f) in ((cw, 0, -cd / 2 - 0.02, "N"), (cw, 0, cd / 2 + 0.02, "S"), (cd, -cw / 2 - 0.02, 0, "E"), (cd, cw / 2 + 0.02, 0, "W")):
            n = max(3, int(L / 4.3))
            ct.append(arcade(f"ms_ca{tier}{f}", L * 0.96, h, n, (x, y, z), f, DARK, True, 0.62, 0.35))
            step = L * 0.96 / n
            fr = []
            for k in range(n):
                u = -L * 0.96 / 2 + step * (k + 0.5)
                bx, by = (x + u, y) if f in ("S", "N") else (x, y + u)
                bw, bd = (step * 0.84, 0.18) if f in ("S", "N") else (0.18, step * 0.84)
                fr.append((bx, by, bw, bd, h * 1.1, z - 0.15))
            ct.append(boxes(f"ms_cf{tier}{f}", fr, shade(BRICK_L, 0.08)))
        ct.append(boxes(f"ms_cband{tier}", [(0, -cd / 2 + 0.1, cw, 0.4, 0.5, 6.0), (0, cd / 2 - 0.1, cw, 0.4, 0.5, 6.0),
                                            (-cw / 2 + 0.1, 0, 0.4, cd, 0.5, 6.0), (cw / 2 - 0.1, 0, 0.4, cd, 0.5, 6.0)], BRICK_D))
    # iwans: river side (south) and the west end face the court; the prayer hall is the east end
    ct.append(iwan("ms_iwan_s", 11, 16.5, 2.2, (0, -cd / 2 + 1.0, 0.3), "N", BRICK_Y, BRICK_L))
    ct.append(iwan("ms_iwan_w", 10, 15.5, 2.0, (-cw / 2 + 1.0, 0, 0.3), "E", BRICK_Y, BRICK_L))
    ct.append(iwan("ms_iwan_e", 12, 17.0, 2.4, (cw / 2 - 1.1, 0, 0.3), "W", BRICK_Y, BRICK_L))
    ct.append(crest("ms_cpar", cw + 1.0, cd + 1.0, H - 0.9, (0, 0), BRICK_L, 0.55, "stepped"))
    ct.append(arch_panel("ms_entry", 5, 9, (0, cd / 2 + 0.3, 0.3), "S", DARK, True, 0.5))
    m.add(2, join(ct, "ms_court_arcades"), "court")
    # the street portal with its muqarnas hood and inscription; the prayer hall's mihrab projection on the east end
    tp = [portal("ms_portal", 16, 17.5, 3.4, (0, D / 2 + 1.2, 0.3), "N", BRICK_Y, BRICK_L)]
    tp.append(box("ms_mihb", 4.5, 10, 12, (W / 2 + 2.2, 0, 0.3), BRICK_Y))
    tp.append(blind_arcade_faces("ms_mihba", 4.5, 10, 2.0, 7, 3.5, W / 2 + 2.2, 0, 0.6))
    tp.append(pdome("ms_mihd", 2.4, (W / 2 + 2.2, 0, 12.3), BRICK_L, k=1.5, drum_h=0.8, windows_n=4, ribs=12, amp=0.05))
    for s in (-1, 1):
        tp.append(box(f"ms_cornertower{s}", 4.5, 4.5, H + 2.5, (s * (W / 2 - 2.2), D / 2 - 2.2, 0.3), BRICK_Y))
        tp.append(box(f"ms_cornertowerr{s}", 4.5, 4.5, H + 2.5, (s * (W / 2 - 2.2), -D / 2 + 2.2, 0.3), BRICK_Y))
    m.add(3, join(tp, "ms_portal_all"), "portal")
    return m


def talisman_gate():
    """Front (-Y) faces out of the city across the moat."""
    m = Model("talisman-gate")
    m.add(0, ground("tg_g", 44, 36, SAND), "ground")
    m.add(0, box("tg_moat", 44, 9, 0.35, (0, -12, 0), "#7E9A88"))
    m.add(0, box("tg_bridge", 7, 11, 1.4, (0, -12, 0), BRICK_D))
    w = [box("tg_wall", 44, 5, 13, (0, 7, 0.3), BRICK_Y), crest("tg_wc", 44, 5, 13.3, (0, 7), BRICK_Y, 0.8, "round")]
    w.append(bands("tg_wb", 44, 5, 2, 12.5, (0, 7), BRICK_D, 3.0, 0.35, 0.2))
    m.add(1, join(w, "tg_walls"), "wall")
    tw = [cylinder("tg_tower", 10, 19, (0, -1, 0.3), BRICK_Y, verts=40)]
    for k, z in enumerate((3.5, 7.0, 10.5)):
        tw.append(cylinder(f"tg_tb{k}", 10.08, 0.4, (0, -1, z), BRICK_D, verts=40))
    tw.append(cylinder("tg_ins", 10.12, 1.4, (0, -1, 14.6), shade(BRICK_Y, -0.38), verts=40))
    tw.append(cylinder("tg_ins2", 10.16, 0.25, (0, -1, 16.2), BRICK_L, verts=40))
    tw.append(cylinder("tg_cap", 10.4, 0.6, (0, -1, 19.3), BRICK_L, verts=40))
    mer = []
    for k in range(28):
        a = math.tau * k / 28
        mer.append(cylinder(f"tg_m{k}", 0.6, 1.3, (9.8 * math.cos(a), -1 + 9.8 * math.sin(a), 19.9), BRICK_Y, verts=6))
    tw.append(join(mer, "tg_merlons"))
    tw.append(arch_panel("tg_arch", 4.2, 7.5, (0, -11.1, 0.3), "S", DARK, True, 0.6))
    tw.append(box("tg_archf", 6.8, 0.6, 9.4, (0, -10.6, 0.3), BRICK_L))
    m.add(2, join(tw, "tg_tower_all"), "tower")
    # the relief over the arch: a seated figure holding the tongues of two dragons, and the inscription panel
    r = [box("tg_panel", 8.4, 0.5, 3.0, (0, -11.0, 10.2), BRICK_L), cylinder("tg_fig", 0.5, 1.4, (0, -11.35, 10.7), shade(BRICK_L, -0.3), verts=8),
         dome("tg_head", 0.38, (0, -11.35, 12.4), shade(BRICK_L, -0.3), segments=8, rings=5)]
    for s in (-1, 1):
        body = []
        for k in range(9):
            u = 0.7 + k * 0.42
            body.append((s * u, -11.4, 0.42, 0.3, 0.32, 11.6 - 1.1 * math.sin(k / 8 * math.pi) + 0.15 * k))
        r.append(boxes(f"tg_drag{s}", body, shade(BRICK_L, -0.3)))
        r.append(box(f"tg_wing{s}", 0.9, 0.25, 0.7, (s * 2.4, -11.4, 12.2), shade(BRICK_L, -0.3)))
    m.add(3, join(r, "tg_relief"), "relief")
    return m


def wastani_gate():
    """Front (-Y) faces out; the round tower stands beyond the moat, joined to the wall by a bridge."""
    m = Model("wastani-gate")
    m.add(0, ground("wg_g", 50, 44, SAND), "ground")
    m.add(0, box("wg_moat", 50, 10, 0.35, (0, 3, 0), "#8E9E80"))
    w = [box("wg_wall", 50, 5, 11, (0, 13, 0.3), BRICK_Y), crest("wg_wc", 50, 5, 11.3, (0, 13), BRICK_Y, 0.8, "round"),
         box("wg_wgate", 12, 7, 12.5, (0, 13, 0.3), BRICK_Y), arch_panel("wg_wga", 3.4, 6.5, (0, 9.4, 0.3), "S", DARK, True, 0.4)]
    br = [box("wg_bridge", 5, 12, 5.5, (0, 3, 0.3), BRICK_D), box("wg_parapet_l", 0.5, 12, 1.0, (-2.3, 3, 5.8), BRICK_D), box("wg_parapet_r", 0.5, 12, 1.0, (2.3, 3, 5.8), BRICK_D)]
    for s in (-1, 1):
        br.append(arch_panel(f"wg_ba{s}", 2.4, 3.6, (s * 2.55, 3, 0.3), "E" if s > 0 else "W", DARK, True, 0.2))
    m.add(1, join(w + br, "wg_walls"), "wall and bridge")
    t = [cylinder("wg_tower", 9.5, 15, (0, -9, 0.3), BRICK_Y, verts=40)]
    for k, z in enumerate((3.0, 6.5)):
        t.append(cylinder(f"wg_tb{k}", 9.58, 0.35, (0, -9, z), BRICK_D, verts=40))
    t.append(cylinder("wg_band", 9.62, 1.6, (0, -9, 9.6), BRICK_L, verts=40))
    lz = []
    for k in range(32):
        a = math.tau * k / 32
        lz.append((9.7 * math.cos(a), -9 + 9.7 * math.sin(a), 0.6, 0.6, 0.6, 10.1, a + math.pi / 4))
    t.append(boxes("wg_lz", lz, BRICK_D))
    t.append(cylinder("wg_cap", 9.9, 0.6, (0, -9, 15.3), BRICK_L, verts=40))
    mer = [cylinder(f"wg_m{k}", 0.6, 1.2, (9.3 * math.cos(math.tau * k / 26), -9 + 9.3 * math.sin(math.tau * k / 26), 15.9), BRICK_Y, verts=6) for k in range(26)]
    t.append(join(mer, "wg_merlons"))
    t.append(arch_panel("wg_arch", 3.6, 6.5, (0, -18.6, 0.3), "S", DARK, True, 0.5))
    t.append(face_panels("wg_slits", 9.5, 16, 0.5, 1.8, 11.8, (0, -9, 0), DARK, False, 2))
    m.add(2, join(t, "wg_tower_all"), "tower")
    m.add(3, shallow_dome("wg_dome", 6.5, (0, -9, 15.9), shade(BRICK_L, -0.05), rise=0.45), "roof")
    return m


def dar_al_khilafa(variant="1200"):
    """Front (-Y) is the river: quay, water gates and the Taj palace; the city gates are on +Y."""
    m = Model("dar-al-khilafa")
    m.add(0, ground("dk_g", 450, 300, "#D2C39E"), "ground")
    m.add(0, box("dk_quay", 450, 14, 1.5, (0, -143, 0), BRICK_D))
    if variant == "830":
        pts = [(-215, -134), (215, -134), (215, 140), (-215, 140), (-215, -134)]
        m.add(1, abbasid_wall("dk_wall", pts, 7, 2.0, BRICK_Y, 2.4, 26), "walls")
        p = [box("dk_hall", 50, 36, 13, (-40, -95, 0.3), BRICK_L), iwan("dk_iwan", 15, 15, 3, (-40, -114, 0.3), "S", BRICK_Y, BRICK_L),
             crest("dk_hc", 50, 36, 13.3, (-40, -95), BRICK_L, 0.8),
             courtyard_ring("dk_c1", 80, 60, 8, 10, (-40, -40, 0.3), BRICK_L), courtyard_ring("dk_c2", 60, 50, 8, 9, (60, -90, 0.3), BRICK_L)]
        p.append(stair("dk_steps", 20, 1.5, 6, 5, (-40, -150, 0), "S", BRICK_D))
        p.append(houses("dk_serv", [(150, 110, 30, 20, 6), (110, 115, 26, 16, 6), (-170, 110, 30, 18, 6), (-180, 60, 22, 30, 6)]))
        m.add(2, join(p, "dk_palace"), "palace")
        g = [charbagh("dk_garden", 140, 110, (90, 30, 0.3), path_color=BRICK_L), pdome("dk_dome", 11, (-40, -95, 13.3), GREEN_DOME, k=1.3, drum_h=2.5, drum_color=PLAST)]
        rng = random.Random(819)
        g.append(palms("dk_palm", [(rng.uniform(-200, 200), rng.uniform(40, 125)) for _ in range(26)] + [(rng.uniform(-200, 200), -125) for _ in range(8)], 2.8))
        m.add(3, join(g, "dk_gardens"), "dome and gardens")
        m.add(3, join([boat("dk_b1", 16, (-90, -146), 0, sail=False), boat("dk_b2", 14, (40, -146), 180)], "dk_boats"))
        return m
    pts = [(-220, -134), (220, -134), (220, 146), (-220, 146), (-220, -134)]
    w = [abbasid_wall("dk_wall", pts, 11, 2.6, BRICK_Y, 3.2, 22)]
    for k, x in enumerate((-110, 60)):
        w.append(portal(f"dk_cgate{k}", 22, 18, 6, (x, 148, 0), "N", BRICK_Y, BRICK_L))
    w.append(portal("dk_wgate", 20, 15, 5, (110, -135, 0), "S", BRICK_Y, BRICK_L, hood=False))
    w.append(stair("dk_steps", 22, 1.5, 6, 5, (0, -150, 0), "S", BRICK_D))
    m.add(1, join(w, "dk_walls"), "walls")
    # the Taj on the river, courts of the palaces, gardens and the menagerie
    p = [box("dk_taj", 72, 46, 16, (0, -100, 0.3), BRICK_L), bands("dk_tajb", 72, 46, 3, 16, (0, -100), BRICK_D, 3.5, 0.45)]
    p.append(iwan("dk_tajiw", 18, 18, 3, (0, -124.5, 0.3), "S", BRICK_Y, BRICK_L))
    p.append(arcade("dk_taja", 68, 9, 9, (0, -123.1, 0.3), "S", DARK, True, 0.55))
    p.append(crest("dk_tajc", 72, 46, 16.3, (0, -100), BRICK_L, 0.8))
    for s in (-1, 1):
        p.append(box(f"dk_wing{s}", 50, 16, 10, (s * 64, -114, 0.3), BRICK_L))
        p.append(arcade(f"dk_winga{s}", 46, 7, 9, (s * 64, -122.05, 0.3), "S", DARK, True, 0.7))
    p.append(courtyard_ring("dk_c1", 90, 70, 10, 11, (-120, -60, 0.3), BRICK_L))
    p.append(courtyard_ring("dk_c2", 80, 70, 10, 11, (120, -60, 0.3), BRICK_L))
    p.append(courtyard_ring("dk_c3", 70, 60, 9, 10, (0, -20, 0.3), BRICK_L))
    p.append(houses("dk_serv", [(160, 110, 40, 20, 7), (110, 115, 40, 14, 7), (190, 60, 24, 40, 7), (160, 10, 30, 22, 7), (-40, 120, 40, 16, 7), (20, 120, 30, 16, 7)]))
    # the Caliph's mosque by the north-west gate
    shell, inner = court_mosque("dk_m", 84, 70, 10, 26, 9, 9, BRICK_Y, (-165, 95, 0))
    p += [shell, inner]
    m.add(2, join([x for x in p if x], "dk_palaces"), "palaces")
    g = [charbagh("dk_garden1", 110, 80, (-85, 40, 0.3), path_color=BRICK_L), charbagh("dk_garden2", 90, 70, (100, 50, 0.3), path_color=BRICK_L)]
    # menagerie: a walled park with trees and pens
    g.append(wall_run("dk_menw", [(150, -20), (210, -20), (210, 30), (150, 30), (150, -20)], 3.0, 0.8, color=BRICK_L, towers=False, merlon=None))
    g.append(trees("dk_ment", [(160, -10), (175, 15), (195, -5), (200, 22), (165, 22)], 2.6))
    g.append(boxes("dk_pens", [(160 + k * 10, 25, 6, 4, 2.5, 0.3) for k in range(5)], BRICK_D))
    g.append(pdome("dk_tajd", 15, (0, -100, 16.3), GREEN_DOME, k=1.3, drum_h=3.5, drum_color=PLAST))
    for s in (-1, 1):
        g.append(box(f"dk_gal{s}", 100, 8, 7, (s * 160, -126, 0.3), BRICK_L))
        g.append(arcade(f"dk_gala{s}", 96, 5, 16, (s * 160, -130.05, 0.3), "S", DARK, True, 0.7))
    g.append(box("dk_firdaws", 22, 22, 9, (100, 50, 0.3), PLAST))
    for f, (dx, dy) in (("S", (0, -11.05)), ("N", (0, 11.05)), ("E", (11.05, 0)), ("W", (-11.05, 0))):
        g.append(arcade(f"dk_fa{f}", 20, 6, 3, (100 + dx, 50 + dy, 0.3), f, DARK, True, 0.7))
    g.append(pdome("dk_firdawsd", 8, (100, 50, 9.3), TURQ, k=1.3, drum_h=1.5, drum_color=PLAST))
    g.append(box("dk_pool", 50, 12, 0.5, (-85, -12, 0.3), WATER))
    rng = random.Random(1180)
    g.append(trees("dk_tr", [(rng.uniform(-110, -20), rng.uniform(88, 135)) for _ in range(12)] + [(rng.uniform(20, 140), rng.uniform(95, 135)) for _ in range(8)], 3.0))
    g.append(palms("dk_palmr", [(-200 + k * 25, -137) for k in range(17) if abs(-200 + k * 25) > 50], 2.6))
    g.append(round_minaret("dk_min", 3.6, 42, (-212, 137, 0), BRICK_Y, BRICK_L, True, "cap"))
    g.append(join([boat("dk_b1", 16, (-90, -146), 0, sail=False), boat("dk_b2", 15, (60, -146), 180, sail=False)], "dk_boats"))
    m.add(3, join(g, "dk_domes_gardens"), "domes and gardens")
    return m


def zumurrud_khatun():
    m = Model("zumurrud-khatun")
    m.add(0, ground("zk_g", 20, 20, "#D8CAA6"), "ground")
    m.add(0, wall_run("zk_court", [(-9.5, -9.5), (-2, -9.5)], 2.2, 0.5, color=BRICK_L, towers=False, merlon=None))
    m.add(0, wall_run("zk_court2", [(2, -9.5), (9.5, -9.5), (9.5, 9.5), (-9.5, 9.5), (-9.5, -9.5)], 2.2, 0.5, color=BRICK_L, towers=False, merlon=None))
    r = 4.6
    b = [oct_prism("zk_oct", r, 6.5, (0, 0, 0.3), BRICK_Y)]
    b.append(face_panels("zk_octn", r, 8, 2.2, 4.4, 0.8, (0, 0, 0), shade(BRICK_Y, -0.3), True, 1, math.pi / 8))
    b.append(arch_panel("zk_door", 1.4, 2.6, (0, -r * math.cos(math.pi / 8) - 0.2, 0.3), "S", DARK, True, 0.3))
    b.append(prism("zk_band", ngon_pts(r + 0.1, 8, math.pi / 8), 0.5, (0, 0, 6.3), BRICK_L))
    m.add(1, join(b, "zk_chamber"), "chamber")
    m.add(2, muqarnas_cone("zk_cone", 4.3, 12.5, 9, (0, 0, 6.8), BRICK_Y, 1.05), "muqarnas dome")
    m.add(3, join([box(f"zk_grave{i}", 1.8, 0.8, 0.5, (x, y, 0.3), "#E2D8C0") for i, (x, y) in enumerate([(-7, 6), (-7, 3.5), (6.8, 6.5), (7, -6), (-6.5, -6)])], "zk_graves"), "graves")
    return m


def gilani_mosque(variant="1650"):
    m = Model("gilani-mosque")
    m.add(0, ground("gl_g", 110, 90, "#D8CAA6"), "ground")
    if variant == "1200":
        m.add(0, courtyard_ring("gl_ring", 60, 50, 8, 8, (-15, 0, 0.3), BRICK_L), "madrasa")
        m.add(0, box("gl_pave", 44, 34, 0.1, (-15, 0, 0.3), PAVE))
        m.add(1, portal("gl_gate", 10, 10, 3, (-15, -25.5, 0.3), "S", BRICK_Y, BRICK_L, hood=False), "gate")
        t = [box("gl_tomb", 14, 14, 9, (26, 0, 0.3), BRICK_Y), bands("gl_tb", 14, 14, 2, 8.5, (26, 0), BRICK_D, 2.5, 0.35)]
        t.append(pdome("gl_td", 6, (26, 0, 9.3), BRICK_L, k=1.4, drum_h=1.5, windows_n=8))
        t.append(round_minaret("gl_min", 1.5, 20, (-42, 22, 0.3), BRICK_Y, BRICK_L))
        m.add(2, join(t, "gl_tomb_all"), "tomb")
        m.add(3, houses("gl_h", [(-45, -35, 16, 12, 6), (40, 35, 18, 14, 7), (45, -35, 16, 14, 6), (-48, 35, 14, 12, 6), (5, 38, 16, 10, 6)]), "houses")
        return m
    m.add(0, courtyard_ring("gl_ring", 108, 88, 8, 8, (0, 0, 0.3), "#E4D8C0"), "court")
    m.add(0, box("gl_pave", 92, 72, 0.1, (0, 0, 0.3), PAVE))
    g = [portal("gl_gate", 14, 13, 4, (0, -45, 0.3), "S", BLUE_T, GOLDEN), portal("gl_gateE", 12, 11, 3, (55, 10, 0.3), "E", BLUE_T, GOLDEN, hood=False)]
    m.add(1, join(g, "gl_gates"), "gates")
    t = [box("gl_tomb", 28, 28, 15, (0, 10, 0.3), "#E6DCC6"), blind_arcade_faces("gl_tba", 28, 28, 2.5, 9, 5.5, 0, 10, 0.6)]
    t.append(box("gl_hall", 60, 16, 10, (0, 30, 0.3), "#E6DCC6"))
    t.append(arcade("gl_halla", 56, 7, 10, (0, 21.95, 0.3), "S", DARK, True, 0.7))
    t.append(box("gl_portico", 40, 7, 8, (0, -7.5, 0.3), "#E6DCC6"))
    t.append(arcade("gl_porta", 38, 6, 7, (0, -11.05, 0.3), "S", DARK, True, 0.7))
    m.add(2, join(t, "gl_buildings"), "tomb and prayer hall")
    d = [ottoman_dome("gl_dome", 12.5, (0, 10, 15.3), "#E8E2D2", BLUE_T, 0.5)]
    for k, x in enumerate((-20, 20)):
        d.append(ottoman_dome(f"gl_hd{k}", 5, (x, 30, 10.3), "#E8E2D2", "#E6DCC6", 0.2))
    d.append(round_minaret("gl_min", 1.8, 34, (40, -30, 0.3), "#E6DCC6", GOLDEN, True, "cap", TURQ))
    m.add(3, join(d, "gl_domes"), "domes and minaret")
    return m


def khan_mirjan():
    """A covered khan: the central hall roofed by transverse pointed arches carrying vaults, with clerestory openings."""
    m = Model("khan-mirjan")
    W, D, H = 46, 32, 11.5
    m.add(0, ground("kmj_g", 46, 32, PAVE), "ground")
    b = [box("kmj_block", W, D, H, (0, 0, 0.3), BRICK_Y), bands("kmj_b", W, D, 2.5, 11, (0, 0), BRICK_D, 3.0, 0.35, 0.2)]
    b.append(blind_arcade_faces("kmj_ba", W, D, 1.2, 4.2, 4.0, 0, 0, 0.55))
    b.append(windows("kmj_w2", W * 0.9, 10, 6.6, 2.4, (0, -D / 2 - 0.05), "S", 0.3))
    b.append(crest("kmj_c", W, D, H + 0.3, (0, 0), BRICK_Y, 0.6, "stepped"))
    m.add(1, join(b, "kmj_walls"), "walls")
    # the central hall's roof: a pointed barrel vault along X with transverse arches showing as ribs
    hw, hl, zb = 12.0, 34.0, H + 0.3
    prof = pointed_profile(hw / 2, 1.25, 0.0, 10)
    verts, faces = [], []
    pts = [(-r, z) for r, z in prof] + [(r, z) for r, z in reversed(prof[:-1])]
    for x0 in (-hl / 2, hl / 2):
        for y, z in pts:
            verts.append((x0, y, zb + z * 0.9))
    n = len(pts)
    for i in range(n - 1):
        faces.append((i, i + 1, n + i + 1, n + i))
    faces.append(tuple(range(n))[::-1])
    faces.append(tuple(range(n, 2 * n)))
    v = mesh_from("kmj_vault", verts, faces, (0, 0, 0), BRICK_L)
    ribs = []
    for k in range(9):
        x = -hl / 2 + k * hl / 8
        rv = [(x - 0.5, y, zb + z * 0.9 + (0.45 if 0 < j < n - 1 else 0)) for j, (y, z) in enumerate(pts)] + [(x + 0.5, y, zb + z * 0.9 + (0.45 if 0 < j < n - 1 else 0)) for j, (y, z) in enumerate(pts)]
        rf = [(i, i + 1, n + i + 1, n + i) for i in range(n - 1)] + [tuple(range(n))[::-1], tuple(range(n, 2 * n))]
        ribs.append(mesh_from(f"kmj_rib{k}", rv, rf, (0, 0, 0), BRICK_Y))
    clere = [box("kmj_cl", hl + 2, hw + 2, 1.6, (0, 0, zb - 0.2), BRICK_Y)]
    clere.append(windows("kmj_clw", hl, 8, zb + 0.1, 1.2, (0, -hw / 2 - 1.05), "S", 0.45, False))
    clere.append(windows("kmj_clwn", hl, 8, zb + 0.1, 1.2, (0, hw / 2 + 1.05), "N", 0.45, False))
    m.add(2, join([v] + ribs + clere, "kmj_roof"), "vaulted hall")
    m.add(3, portal("kmj_portal", 11, 14, 2.4, (0, -D / 2 - 1.0, 0.3), "S", BRICK_Y, BRICK_L), "portal")
    return m


def ottoman_citadel():
    """Front (-Y) faces the river; the main gate opens to the city on +Y."""
    m = Model("ottoman-citadel")
    m.add(0, ground("oc_g", 280, 220, "#D0C19C"), "ground")
    pts = [(-134, -104), (134, -104), (134, 104), (-134, 104), (-134, -104)]
    w = [wall_run("oc_wall", pts, 12, 3.2, color=BRICK_Y, towers=True, tower_r=6.5, tower_every=44, merlon="box", batter=0.3)]
    w.append(gatehouse("oc_gate", 30, 18, 15, (40, 104, 0), "N", BRICK_Y, BRICK_L, "roman"))
    w.append(gatehouse("oc_rgate", 22, 14, 12, (-60, -104, 0), "S", BRICK_Y, BRICK_L, "roman"))
    m.add(1, join(w, "oc_walls"), "walls")
    b = [box("oc_parade", 120, 80, 0.12, (20, 20, 0.3), "#CDBB92")]
    b.append(houses("oc_barracks", [(-95, 60, 60, 16, 8), (-95, 20, 60, 16, 8), (-95, -20, 60, 16, 8), (90, -70, 70, 16, 8), (20, -75, 50, 14, 7),
                                    (100, 75, 40, 16, 7), (110, 30, 24, 30, 9)]))
    for k, (x, y) in enumerate(((-95, 60), (-95, 20), (-95, -20))):
        b.append(gable_roof(f"oc_br{k}", 60, 16, 3, (x, y, 8.8), "#8E7A5E", 0.4))
    b.append(box("oc_armoury", 36, 24, 10, (-40, -70, 0.3), BRICK_L))
    b.append(windows("oc_armw", 32, 6, 4, 3, (-40, -82.05), "S", 0.3))
    b.append(boxes("oc_guns", [(-120 + k * 30, -96, 3.5, 1.0, 1.0, 12.3) for k in range(9)], "#4A4844"))
    m.add(2, join(b, "oc_barracks_all"), "barracks")
    mq = [box("oc_mq", 26, 26, 11, (40, -25, 0.3), PLAST), box("oc_mqp", 26, 8, 7, (40, -42, 0.3), PLAST),
          arcade("oc_mqpa", 24, 5.5, 5, (40, -46.05, 0.3), "S", DARK, True, 0.7)]
    mq.append(ottoman_dome("oc_dome", 11, (40, -25, 11.3), LEAD, PLAST, 0.35))
    mq.append(minaret("oc_min", 1.6, 34, (57, -14, 0.3), PLAST, PLAST, 2, "cone", 12, 0.85))
    mq.append(cylinder("oc_flag", 0.2, 14, (-20, 60, 0.3), WOOD_D, verts=6))
    mq.append(box("oc_flagc", 4.5, 0.15, 3, (-17.7, 60, 11.3), "#A8332A"))
    m.add(3, join(mq, "oc_mosque"), "mosque")
    return m


BUILDERS = {
    "baghdad/round-city": lambda: round_city("800"),
    "baghdad/round-city-1200": lambda: round_city("1200"),
    "baghdad/golden-gate-palace": golden_gate_palace,
    "baghdad/mansur-mosque": mansur_mosque,
    "baghdad/mansur-mosque-770": lambda: mansur_mosque("763"),
    "baghdad/khuld-palace": khuld_palace,
    "baghdad/rusafa": rusafa,
    "baghdad/rusafa-1200": lambda: rusafa("1200"),
    "baghdad/bridge-of-boats": bridge_of_boats,
    "baghdad/bayt-al-hikma": bayt_al_hikma,
    "baghdad/shammasiyya-observatory": shammasiyya_observatory,
    "baghdad/karkh-market": karkh_market,
    "baghdad/kazimayn": kazimayn,
    "baghdad/kazimayn-800": lambda: kazimayn("800"),
    "baghdad/kazimayn-1200": lambda: kazimayn("1200"),
    "baghdad/mustansiriya": mustansiriya,
    "baghdad/talisman-gate": talisman_gate,
    "baghdad/wastani-gate": wastani_gate,
    "baghdad/dar-al-khilafa": dar_al_khilafa,
    "baghdad/dar-al-khilafa-830": lambda: dar_al_khilafa("830"),
    "baghdad/zumurrud-khatun": zumurrud_khatun,
    "baghdad/gilani-mosque": gilani_mosque,
    "baghdad/gilani-1200": lambda: gilani_mosque("1200"),
    "baghdad/khan-mirjan": khan_mirjan,
    "baghdad/ottoman-citadel": ottoman_citadel,
}
