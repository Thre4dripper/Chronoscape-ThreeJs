"""Great Zimbabwe landmark miniatures: the Great Enclosure with its parallel passage and Conical Tower, the Hill Complex
among the boulders of the kopje with the soapstone birds, the Valley, Ridge and Eastern Ruins, the Ancient Ascent,
the cattle kraal, an elite daga household, the iron-smelters' ground, the trade ground, commoners' homesteads and
the fields with their granaries.

Conventions as in FORMAT.md: metres, origin at the ground centre, +X east, +Y north, +Z up.

The drystone walls are built course by course (bands of alternating granite tones) by stone_wall(): the outer face
lies on the given line at ground level, the wall's body lies to its left, both faces batter inward as they rise, and
open ends are rounded like the entrances at Great Zimbabwe. Small parts are gathered per colour in a Parts buffer
and made into one mesh each.
"""
import math
from chronokit import Model, join, mesh_from, shade
from worldkit import *

GR1, GR2, GR3 = "#B2A999", "#A1988A", "#BDB4A5"          # dressed granite courses
GR_DK = "#6E675E"                                          # chevron band, shadowed courses
STONE = (GR1, GR2, GR1, GR3, GR2, GR1)
ROCK, ROCK_DK, ROCK_LT = "#857F74", "#6F6A60", "#979085"   # natural granite of the kopjes
SOAP = "#7E8470"                                           # soapstone (greenish schist)
DAGA, DAGA_LT, DAGA_DK = "#A8774E", "#BA8A5E", "#8A5E3C"
THATCH_C, THATCH_DK = "#B39A5E", "#9C8550"
EARTH, EARTH_DK, SWEPT = "#B09872", "#98805E", "#C4A77E"
GRASS, GRASS_DK = "#8E9A5C", "#76824A"
LEAF, LEAF_DK, TRUNK = "#62804A", "#4F6A3C", "#6A5038"
POLE, THORN = "#7A5E40", "#6B6A40"
HORN = "#DCD2BA"
CATTLE = ["#5A3E2C", "#C9B79A", "#8A5A3A", "#3E3530", "#B07A50", "#E2D8C4"]
IVORY = "#EDE3CC"
CLOTH_B, CLOTH_W, CLOTH_R = "#3F5E8C", "#E9E2D2", "#A8443A"
BEADS = ["#2F6FA8", "#D8B23A", "#2E8A6A", "#B8442E"]
COPPER, GOLD_C = "#B06A3A", "#D4AE55"
CLAY, FURNACE = "#9C5E3C", "#A0603E"
SLAG, CHAR, ORE = "#3E3A36", "#2A2622", "#8A4A32"
LEATHER = "#7A5236"
MAT = "#B39960"
STALK, SORGHUM, MILLET, BEAN = "#7C8A48", "#A8562E", "#8F7348", "#5E8A44"
BOX_FACES = [(3, 2, 1, 0), (4, 5, 6, 7), (0, 1, 5, 4), (1, 2, 6, 5), (2, 3, 7, 6), (3, 0, 4, 7)]


# ---------------------------------------------------------------- a buffer of small parts, one mesh per colour

class Parts:
    def __init__(self, name):
        self.name = name
        self.g = {}

    def poly(self, color, verts, faces):
        vs, fs = self.g.setdefault(color, ([], []))
        b = len(vs)
        vs.extend(verts)
        fs.extend(tuple(b + i for i in f) for f in faces)

    def cube(self, color, cx, cy, z0, w, d, h):
        if w <= 0 or d <= 0 or h <= 0:
            return
        v = []
        for z in (z0, z0 + h):
            v += [(cx - w / 2, cy - d / 2, z), (cx + w / 2, cy - d / 2, z), (cx + w / 2, cy + d / 2, z), (cx - w / 2, cy + d / 2, z)]
        self.poly(color, v, BOX_FACES)

    def frustum(self, color, cx, cy, z0, w0, d0, w1, d1, h):
        v = [(cx - w0 / 2, cy - d0 / 2, z0), (cx + w0 / 2, cy - d0 / 2, z0), (cx + w0 / 2, cy + d0 / 2, z0), (cx - w0 / 2, cy + d0 / 2, z0),
             (cx - w1 / 2, cy - d1 / 2, z0 + h), (cx + w1 / 2, cy - d1 / 2, z0 + h), (cx + w1 / 2, cy + d1 / 2, z0 + h), (cx - w1 / 2, cy + d1 / 2, z0 + h)]
        self.poly(color, v, BOX_FACES)

    def cone(self, color, x, y, z0, r0, r1, h, n=6, start=0.0):
        v = [(x + r0 * math.cos(start + math.tau * i / n), y + r0 * math.sin(start + math.tau * i / n), z0) for i in range(n)]
        if r1 > 1e-4:
            v += [(x + r1 * math.cos(start + math.tau * i / n), y + r1 * math.sin(start + math.tau * i / n), z0 + h) for i in range(n)]
            f = [tuple(range(n))[::-1], tuple(range(n, 2 * n))] + [(i, (i + 1) % n, n + (i + 1) % n, n + i) for i in range(n)]
        else:
            v.append((x, y, z0 + h))
            f = [tuple(range(n))[::-1]] + [(i, (i + 1) % n, n) for i in range(n)]
        self.poly(color, v, f)

    def dome(self, color, x, y, z0, r, squash=1.0, n=10, rings=4, ry=None):
        ry = ry or r
        v, f = [], []
        for k in range(rings):
            phi = (math.pi / 2) * k / rings
            v += [(x + r * math.cos(phi) * math.cos(math.tau * i / n), y + ry * math.cos(phi) * math.sin(math.tau * i / n), z0 + r * math.sin(phi) * squash) for i in range(n)]
        v.append((x, y, z0 + r * squash))
        top = len(v) - 1
        f.append(tuple(range(n))[::-1])
        for k in range(rings - 1):
            a, b = k * n, (k + 1) * n
            f += [(a + i, a + (i + 1) % n, b + (i + 1) % n, b + i) for i in range(n)]
        a = (rings - 1) * n
        f += [(a + i, a + (i + 1) % n, top) for i in range(n)]
        self.poly(color, v, f)

    def beam(self, color, p0, p1, tw, th=None):
        th = th or tw
        d = [p1[i] - p0[i] for i in range(3)]
        L = math.sqrt(sum(c * c for c in d)) or 1e-6
        d = [c / L for c in d]
        up = (0, 0, 1) if abs(d[2]) < 0.95 else (1, 0, 0)
        u = (d[1] * up[2] - d[2] * up[1], d[2] * up[0] - d[0] * up[2], d[0] * up[1] - d[1] * up[0])
        ul = math.sqrt(sum(c * c for c in u)) or 1e-6
        u = [c / ul * tw / 2 for c in u]
        v = (u[1] * d[2] - u[2] * d[1], u[2] * d[0] - u[0] * d[2], u[0] * d[1] - u[1] * d[0])
        vl = math.sqrt(sum(c * c for c in v)) or 1e-6
        v = [c / vl * th / 2 for c in v]
        verts = []
        for p in (p0, p1):
            for a, b in ((-1, -1), (1, -1), (1, 1), (-1, 1)):
                q = [p[i] + a * u[i] + b * v[i] for i in range(3)]
                q[2] = max(0.0, q[2])
                verts.append(tuple(q))
        self.poly(color, verts, BOX_FACES)

    def build(self):
        objs = [mesh_from(f"{self.name}_{i}", vs, fs, (0, 0, 0), color) for i, (color, (vs, fs)) in enumerate(self.g.items()) if fs]
        return join(objs, self.name)


def rnd(seed):
    """A tiny deterministic random sequence in [0, 1)."""
    k = seed
    while True:
        k = (k * 1103515245 + 12345) % 2147483648
        yield (k >> 8) / 8388608.0


def obox(P, color, cx, cy, z0, w, d, h, ang=0.0):
    """A box turned by ang (radians, counter-clockwise) about its own centre."""
    c, s = math.cos(ang), math.sin(ang)
    pts = [(-w / 2, -d / 2), (w / 2, -d / 2), (w / 2, d / 2), (-w / 2, d / 2)]
    v = [(cx + px * c - py * s, cy + px * s + py * c, z) for z in (z0, z0 + h) for px, py in pts]
    P.poly(color, v, BOX_FACES)


def slab(P, color, pts, z0, h):
    """A closed outline [(x, y), ...] extruded from z0 up by h."""
    n = len(pts)
    v = [(x, y, z0) for x, y in pts] + [(x, y, z0 + h) for x, y in pts]
    f = [tuple(range(n))[::-1], tuple(range(n, 2 * n))] + [(i, (i + 1) % n, n + (i + 1) % n, n + i) for i in range(n)]
    P.poly(color, v, f)


def ell(cx, cy, rx, ry, n=32, wob=None, p=2.0, a0=0.0):
    out = []
    for i in range(n):
        t = a0 + math.tau * i / n
        c, s = math.cos(t), math.sin(t)
        k = 1 + (wob(t) if wob else 0.0)
        if p != 2.0:
            c = math.copysign(abs(c) ** (2 / p), c)
            s = math.copysign(abs(s) ** (2 / p), s)
        out.append((cx + rx * k * c, cy + ry * k * s))
    return out


def slant_cyl(P, color, c0, r0, z0, c1, r1, z1, n=10):
    v = [(c0[0] + r0 * math.cos(math.tau * i / n), c0[1] + r0 * math.sin(math.tau * i / n), z0) for i in range(n)]
    v += [(c1[0] + r1 * math.cos(math.tau * i / n), c1[1] + r1 * math.sin(math.tau * i / n), z1) for i in range(n)]
    f = [tuple(range(n))[::-1], tuple(range(n, 2 * n))] + [(i, (i + 1) % n, n + (i + 1) % n, n + i) for i in range(n)]
    P.poly(color, v, f)


# ---------------------------------------------------------------- drystone walls

def _norm(x, y):
    l = math.hypot(x, y) or 1e-9
    return x / l, y / l


def vnormals(pts, closed):
    """Right-hand unit normals at each vertex (outward for a counter-clockwise loop), mitred at the corners."""
    n = len(pts)
    out = []
    for i in range(n):
        segs = []
        if closed or i > 0:
            a = pts[i - 1]
            segs.append((pts[i][0] - a[0], pts[i][1] - a[1]))
        if closed or i < n - 1:
            c = pts[(i + 1) % n]
            segs.append((c[0] - pts[i][0], c[1] - pts[i][1]))
        ns = [_norm(dy, -dx) for dx, dy in segs]
        mx, my = _norm(sum(q[0] for q in ns), sum(q[1] for q in ns))
        s = 1.0
        if len(ns) == 2:
            s = 1.0 / max(0.5, mx * ns[0][0] + my * ns[0][1])
        out.append((mx * s, my * s))
    return out


def _per(v, n):
    return list(v) if isinstance(v, (list, tuple)) else [v] * n


def stone_wall(P, pts, h, tb, tt=None, closed=False, z0=0.0, courses=8, tones=STONE, lean=0.8, rounded=True):
    """A battered drystone wall laid in courses. The outer face stands on pts at its foot; the body lies to the
    left of the direction of travel. h, tb (base thickness), tt (top thickness) and z0 may be lists (one per point).
    Returns a function at(i, f) -> (outer (x, y), inner (x, y), z) at height fraction f of point i."""
    n = len(pts)
    H, TB, Z = _per(h, n), _per(tb, n), _per(z0, n)
    TT = _per(tt, n) if tt is not None else [t * 0.55 for t in TB]
    N = vnormals(pts, closed)

    def at(i, f):
        px, py = pts[i]
        nx, ny = N[i]
        do = (TB[i] - TT[i]) * lean * f
        di = TB[i] - (TB[i] - TT[i]) * (1 - lean) * f
        return (px - nx * do, py - ny * do), (px - nx * di, py - ny * di), Z[i] + H[i] * f

    segs = range(n) if closed else range(n - 1)
    for k in range(courses):
        f0, f1 = k / courses, (k + 1) / courses
        col = tones[k % len(tones)]
        verts = []
        for i in range(n):
            o0, i0, za = at(i, f0)
            o1, i1, zb = at(i, f1)
            verts += [(o0[0], o0[1], za), (i0[0], i0[1], za), (o1[0], o1[1], zb), (i1[0], i1[1], zb)]
        faces = []
        for i in segs:
            j = (i + 1) % n
            a, b = 4 * i, 4 * j
            faces += [(a, b, b + 2, a + 2), (b + 1, a + 1, a + 3, b + 3), (a + 2, b + 2, b + 3, a + 3), (a + 1, b + 1, b, a)]
        if not closed:
            L = 4 * (n - 1)
            faces += [(0, 2, 3, 1), (L, L + 1, L + 3, L + 2)]
        P.poly(col, verts, faces)
        if rounded and not closed:
            for e in (0, n - 1):
                o0, i0, za = at(e, f0)
                o1, i1, zb = at(e, f1)
                c0 = ((o0[0] + i0[0]) / 2, (o0[1] + i0[1]) / 2)
                c1 = ((o1[0] + i1[0]) / 2, (o1[1] + i1[1]) / 2)
                slant_cyl(P, col, c0, math.dist(o0, i0) / 2, za, c1, math.dist(o1, i1) / 2, zb, 10)
    return at


def arc_pts(cx, cy, rx, ry, d0, d1, seg=2.2, wob=None):
    """Points along an ellipse from d0 to d1 degrees (counter-clockwise), about seg metres apart."""
    L = abs(math.radians(d1 - d0)) * (rx + ry) / 2
    n = max(3, int(L / seg) + 1)
    out = []
    for i in range(n):
        t = math.radians(d0 + (d1 - d0) * i / (n - 1))
        k = 1 + (wob(t) if wob else 0.0)
        out.append((cx + rx * k * math.cos(t), cy + ry * k * math.sin(t)))
    return out


def enclosure(P, cx, cy, rx, ry, h, tb, tt=None, gaps=(), z0=0.0, courses=7, tones=STONE, wob=None, seg=2.2):
    """An elliptical drystone enclosure; gaps = [(deg0, deg1), ...] are entrances (allow for the rounded ends)."""
    if not gaps:
        pts = arc_pts(cx, cy, rx, ry, 0, 360, seg, wob)[:-1]
        stone_wall(P, pts, h, tb, tt, True, z0, courses, tones)
        return
    gs = sorted(gaps)
    for i, (a0, a1) in enumerate(gs):
        b0, b1 = a1, gs[(i + 1) % len(gs)][0] + (360 if i == len(gs) - 1 else 0)
        pts = arc_pts(cx, cy, rx, ry, b0, b1, seg, wob)
        ts = [math.radians(b0 + (b1 - b0) * k / (len(pts) - 1)) for k in range(len(pts))]
        ev = lambda v: [v(t) for t in ts] if callable(v) else v
        stone_wall(P, pts, ev(h), ev(tb), ev(tt), False, z0, courses, tones)


def chevron(P, pts_fn, d0, d1, top, band=0.9, zig=0.85, rows=2, out=0.1, color=GR_DK):
    """A chevron (zigzag) band on a wall face. pts_fn(theta_deg, z) -> (x, y) on the outer face at height z;
    top(theta_deg) is the height of the band's top."""
    L = abs(math.radians(d1 - d0)) * 40
    n = max(4, int(L / zig))
    for r in range(rows):
        prev = None
        for i in range(n + 1):
            t = d0 + (d1 - d0) * i / n
            zt = top(t) - r * band * 0.62
            z = zt if i % 2 == 0 else zt - band
            x, y = pts_fn(t, z, out)
            if prev:
                P.beam(color, prev, (x, y, z), 0.24, 0.24)
            prev = (x, y, z)


# ---------------------------------------------------------------- houses, granaries, rocks, plants, animals

def hut(P, x, y, r, z0=0.0, wh=None, rh=None, wall=DAGA, roof=THATCH_C, door=-math.pi / 2, plat=0.0, plat_col=GR2, n=12):
    """A round daga house under a conical thatch roof, optionally on a raised platform."""
    wh = wh or max(1.9, r * 0.72)
    rh = rh or r * 1.1
    if plat:
        P.cone(plat_col, x, y, z0, r + 1.25, r + 1.05, plat, 14)
        z0 += plat
    P.cone(wall, x, y, z0, r, r * 0.98, wh, n)
    P.cone(roof, x, y, z0 + wh - 0.2, r * 1.3, r * 0.5, rh * 0.55, n)
    P.cone(roof, x, y, z0 + wh - 0.2 + rh * 0.55, r * 0.5, 0, rh * 0.45, n)
    P.cone(THATCH_DK, x, y, z0 + wh - 0.25, r * 1.32, r * 1.3, 0.12, n)
    dx, dy = math.cos(door), math.sin(door)
    obox(P, DARK, x + dx * r, y + dy * r, z0, 0.3, 0.85, min(1.55, wh * 0.78), door)
    P.cone(DAGA_DK, x + dx * (r + 0.35), y + dy * (r + 0.35), z0, 0.55, 0.5, 0.12, 6)


def mound(P, x, y, r, z0=0.0):
    """A collapsed daga house: a low mound of burnt daga under grass."""
    P.dome(DAGA_DK, x, y, z0, r, 0.25, 10, 3)
    P.dome(GRASS_DK, x + r * 0.2, y - r * 0.1, z0 + r * 0.12, r * 0.5, 0.3, 8, 2)


def granary(P, x, y, r=0.9, legs=0.9, z0=0.0):
    for a in (0.6, 2.2, 3.8, 5.4):
        P.cone(ROCK_DK if a < 3 else POLE, x + math.cos(a) * r * 0.6, y + math.sin(a) * r * 0.6, z0, 0.14, 0.12, legs, 5)
    P.cone(POLE, x, y, z0 + legs, r * 1.1, r * 1.1, 0.12, 10)
    P.cone(DAGA_LT, x, y, z0 + legs + 0.12, r, r * 1.05, r * 1.2, 10)
    P.cone(THATCH_C, x, y, z0 + legs + 0.12 + r * 1.2, r * 1.35, 0, r * 1.1, 10)


def boulder(P, x, y, rx, ry, rz, z0=0.0, seed=1, color=ROCK, n=9, rings=5, rot=0.0):
    """A rounded granite corestone: a lumpy, leaning ovoid, undercut at its foot and flattened on top."""
    r = rnd(seed * 7 + 3)
    phi0 = math.radians(-24)
    s0 = math.sin(phi0)
    lx, ly = (next(r) - 0.5) * 0.5 * rx, (next(r) - 0.5) * 0.5 * ry
    flat = 0.75 + next(r) * 0.2
    v = []
    for k in range(rings):
        phi = phi0 + (math.radians(78) - phi0) * k / (rings - 1)
        u = k / (rings - 1)
        for i in range(n):
            a = math.tau * i / n + rot
            q = 1 + 0.26 * (next(r) - 0.5)
            zz = rz * (math.sin(phi) - s0) / (1 - s0)
            v.append((x + lx * u * u + rx * q * math.cos(phi) * math.cos(a), y + ly * u * u + ry * q * math.cos(phi) * math.sin(a), z0 + zz * (flat if k == rings - 1 else 1.0)))
    v.append((x + lx, y + ly, z0 + rz * flat))
    top = len(v) - 1
    f = [tuple(range(n))[::-1]]
    for k in range(rings - 1):
        a, b = k * n, (k + 1) * n
        f += [(a + i, a + (i + 1) % n, b + (i + 1) % n, b + i) for i in range(n)]
    a = (rings - 1) * n
    f += [(a + i, a + (i + 1) % n, top) for i in range(n)]
    P.poly(color, v, f)


def bush(P, x, y, r, z0=0.0, color=LEAF):
    P.dome(color, x, y, z0, r, 0.75, 8, 3)


def tree(P, x, y, h, r, z0=0.0, color=LEAF, lean=0.0):
    """A msasa or fig: a short trunk and a broad flattish crown."""
    P.beam(TRUNK, (x, y, z0), (x + lean, y, z0 + h * 0.62), max(0.25, r * 0.12))
    P.dome(color, x + lean, y, z0 + h * 0.5, r, 0.55, 10, 3)
    P.dome(shade(color, -0.08), x + lean + r * 0.35, y + r * 0.2, z0 + h * 0.62, r * 0.6, 0.6, 8, 3)


def cow(P, x, y, deg, col, s=1.0, horns=True, hump=True):
    """A long-horned sanga cow, standing."""
    c, sn = math.cos(math.radians(deg)), math.sin(math.radians(deg))

    def T(px, py, pz):
        return (x + (px * c - py * sn) * s, y + (px * sn + py * c) * s, pz * s)

    P.beam(col, T(-0.75, 0, 1.0), T(0.65, 0, 1.02), 0.55 * s, 0.6 * s)
    if hump:
        P.beam(col, T(0.3, 0, 1.3), T(0.55, 0, 1.38), 0.28 * s, 0.22 * s)
    P.beam(col, T(0.6, 0, 1.15), T(1.05, 0, 0.92), 0.26 * s, 0.3 * s)
    if horns:
        for side in (-1, 1):
            P.beam(HORN, T(0.85, side * 0.1, 1.2), T(0.75, side * 0.5, 1.45), 0.07 * s)
            P.beam(HORN, T(0.75, side * 0.5, 1.45), T(0.8, side * 0.45, 1.8), 0.06 * s)
    for lx in (-0.6, 0.5):
        for ly in (-0.17, 0.17):
            P.beam(col, T(lx, ly, 0.8), T(lx, ly, 0.0), 0.13 * s)
    P.beam(col, T(-0.78, 0, 1.15), T(-0.9, 0, 0.55), 0.05 * s)


def bird_column(P, x, y, z0, face=-math.pi / 2, S=1.6, ring=True):
    """A Zimbabwe bird: a soapstone eagle with folded wings on top of a carved soapstone column (S: drawn larger than life)."""
    P.cone(SOAP, x, y, z0, 0.17 * S, 0.14 * S, 1.0 * S, 8)
    if ring:
        for k in range(3):
            P.cone(shade(SOAP, -0.15), x, y, z0 + (0.25 + 0.25 * k) * S, 0.165 * S, 0.165 * S, 0.05 * S, 8)
    zt = z0 + 1.0 * S
    P.cone(SOAP, x, y, zt, 0.16 * S, 0.15 * S, 0.06 * S, 8)
    dx, dy = math.cos(face), math.sin(face)

    def F(a, z):
        return (x + dx * a * S, y + dy * a * S, z)

    P.beam(SOAP, F(-0.02, zt + 0.06 * S), F(0.02, zt + 0.16 * S), 0.12 * S, 0.06 * S)
    P.beam(SOAP, F(-0.2, zt + 0.14 * S), F(0.06, zt + 0.36 * S), 0.13 * S, 0.17 * S)
    P.beam(SOAP, F(0.06, zt + 0.34 * S), F(0.1, zt + 0.48 * S), 0.08 * S, 0.08 * S)
    P.beam(SOAP, F(0.1, zt + 0.47 * S), F(0.18, zt + 0.43 * S), 0.05 * S, 0.04 * S)


def monolith(P, x, y, z0, h, w=0.35, color=GR2):
    P.cone(color, x, y, z0, w, w * 0.7, h, 4, math.pi / 4)


def free_spots(cands, r, obstacles, taken, gap=1.0):
    """Keep candidate (x, y) points at least r+gap clear of circular obstacles [(x, y, R)] and of each other."""
    out = []
    for (x, y) in cands:
        if any(math.hypot(x - ox, y - oy) < r + R + gap for ox, oy, R in obstacles + taken):
            continue
        taken.append((x, y, r))
        out.append((x, y))
    return out


# ---------------------------------------------------------------- the Great Enclosure

GE_RX, GE_RY = 44.5, 34.0


def ge_wob(t):
    return 0.035 * math.sin(2 * t + 0.7) + 0.02 * math.cos(3 * t + 0.3)


def ge_k(t):
    return ((1 + math.cos(t + 0.15)) / 2) ** 2


def ge_h(t):
    return 6.0 + 5.0 * ge_k(t)


def ge_tb(t):
    return 3.0 + 2.2 * ge_k(t)


def ge_pt(deg, frac=1.0):
    t = math.radians(deg)
    k = 1 + ge_wob(t)
    return (GE_RX * k * frac * math.cos(t), GE_RY * k * frac * math.sin(t))


def ge_face(deg, z, out=0.0, z0=0.2):
    """A point on the outer face of the Great Enclosure's outer wall at height z (out = metres proud of the face)."""
    t = math.radians(deg)
    p0, p1 = ge_pt(deg - 0.5), ge_pt(deg + 0.5)
    nx, ny = _norm(p1[1] - p0[1], -(p1[0] - p0[0]))
    px, py = ge_pt(deg)
    tb = ge_tb(t)
    f = max(0.0, min(1.0, (z - z0) / ge_h(t)))
    d = (tb - tb * 0.5) * 0.8 * f - out
    return px - nx * d, py - ny * d


def great_enclosure(variant="1350"):
    late = variant == "1500"
    m = Model("great-enclosure")
    g = Parts("ge_ground")
    slab(g, EARTH, ell(0, 0, 49.5, 39.5, 48, ge_wob), 0, 0.2)
    slab(g, SWEPT, ell(-6, 0, 30, 22, 36), 0.2, 0.04)

    walls = Parts("ge_outer")
    gaps = [(98.5, 107.5), (143.5, 151.5), (189.5, 197.5)]
    tt = lambda t: ge_tb(t) * 0.5
    enclosure(walls, 0, 0, GE_RX, GE_RY, ge_h, ge_tb, tt, gaps=gaps, z0=0.2, courses=16, wob=ge_wob, seg=1.7)
    # the chevron band along the top of the highest (eastern) stretch, over the parallel passage
    chevron(walls, ge_face, -42, 66, lambda d: 0.2 + ge_h(math.radians(d)) - 0.9, band=0.85, zig=0.8, rows=2)
    # a dark course below it, as a shadow line
    for d in range(-42, 66, 3):
        a, b = ge_face(d, 0.2 + ge_h(math.radians(d)) - 2.75, 0.05), ge_face(d + 3, 0.2 + ge_h(math.radians(d + 3)) - 2.75, 0.05)
        walls.beam(GR_DK, (a[0], a[1], 0.2 + ge_h(math.radians(d)) - 2.75), (b[0], b[1], 0.2 + ge_h(math.radians(d + 3)) - 2.75), 0.12, 0.18)
    # small monoliths standing on the wall top above the chevron (several were recorded on this stretch)
    for d in range(-20, 41, 12):
        t = math.radians(d)
        px, py = ge_pt(d)
        p0, p1 = ge_pt(d - 0.5), ge_pt(d + 0.5)
        nx, ny = _norm(p1[1] - p0[1], -(p1[0] - p0[0]))
        tb = ge_tb(t)
        dd = (tb - tb * 0.5) * 0.8 + tb * 0.25
        monolith(walls, px - nx * dd, py - ny * dd, 0.2 + ge_h(t), 1.8 if d % 24 else 2.4, 0.4, GR3)
    # steps up into the north entrance
    t = math.radians(103)
    px, py = ge_pt(103)
    nx, ny = _norm(ge_pt(103.5)[1] - ge_pt(102.5)[1], -(ge_pt(103.5)[0] - ge_pt(102.5)[0]))
    ang = math.atan2(ny, nx) + math.pi / 2
    for k in range(3):
        d = 1.2 - k * 1.1
        obox(walls, GR3 if k % 2 else GR1, px + nx * d, py + ny * d, 0.2, 3.2 - k * 0.3, 1.1, 0.22 * (3 - k), ang)

    inner = Parts("ge_inner")
    # the parallel passage: a second wall about a metre inside the outer wall on the east, from the north entrance to the tower
    d0, d1 = -34, 96
    ths = [d0 + (d1 - d0) * i / 60 for i in range(61)]
    outer = [ge_pt(d) for d in ths]
    N = vnormals(outer, False)
    ppts = [(outer[i][0] - N[i][0] * (ge_tb(math.radians(ths[i])) + 1.05), outer[i][1] - N[i][1] * (ge_tb(math.radians(ths[i])) + 1.05)) for i in range(len(ths))]
    stone_wall(inner, ppts, [7.2 + 2.2 * ge_k(math.radians(d)) for d in ths], 2.3, 1.3, False, 0.2, 12)
    # the tower court: a curving screen wall closing it from the interior
    stone_wall(inner, [ge_pt(d, 0.53) for d in range(-84, -16, 3)], 4.2, 1.7, 1.0, False, 0.2, 7)
    # the older inner enclosures with their daga houses
    enclosure(inner, -14, 6, 11, 9, 4.0, 1.8, 1.0, gaps=[(38, 56), (246, 264)], z0=0.2, courses=7)
    enclosure(inner, 8, 12, 8, 7, 3.4, 1.5, 0.9, gaps=[(196, 218)], z0=0.2, courses=6)
    enclosure(inner, -30, -10, 7, 6, 3.0, 1.4, 0.8, gaps=[(-6, 18)], z0=0.2, courses=5)
    # the Conical Tower (9 m high, 5.5 m across at the base) and its small twin
    tx, ty = ge_pt(-40, 0.72)
    nc = 15
    for k in range(nc):
        f0, f1 = k / nc, (k + 1) / nc
        r0, r1 = 2.75 - 1.55 * f0 ** 1.25, 2.75 - 1.55 * f1 ** 1.25
        inner.cone(STONE[k % len(STONE)], tx, ty, 0.2 + 9.1 * f0, r0, r1, 9.1 / nc, 20)
    inner.cone(GR_DK, tx, ty, 9.3, 1.24, 1.16, 0.18, 20)
    sx, sy = ge_pt(-56, 0.68)
    for k in range(5):
        inner.cone(STONE[k % len(STONE)], sx, sy, 0.2 + 0.6 * k, 1.15 - 0.1 * k, 1.05 - 0.1 * k, 0.6, 14)
    # a stepped platform beside the tower
    px, py = ge_pt(-12, 0.6)
    inner.cone(GR2, px, py, 0.2, 3.3, 3.1, 0.6, 16)
    inner.cone(GR1, px, py, 0.8, 2.6, 2.45, 0.5, 16)

    houses = Parts("ge_houses")
    spots = [(-17, 7, 3.2, 0.8, 0.3), (-9, 3.5, 2.6, 0.6, 1.2), (8, 12, 3.0, 0.7, -1.9), (-30, -10, 2.6, 0.5, 0.0), (-4, -15, 3.0, 0.8, 1.6),
             (14, -4, 2.8, 0.6, 2.8), (-28, 14, 2.6, 0.5, -0.6), (-34, 5, 2.4, 0.4, 0.2), (-17, -21, 2.6, 0.5, 1.4), (0, 22, 2.6, 0.5, -1.6), (22, 4, 2.6, 0.5, 3.0)]
    keep = {0, 2, 4} if late else set(range(len(spots)))
    for i, (x, y, r, pl, door) in enumerate(spots):
        if i in keep:
            hut(houses, x, y, r, 0.2, plat=pl, door=door, plat_col=GR2 if pl > 0.55 else DAGA_DK)
        else:
            mound(houses, x, y, r + 0.6, 0.2)
    if not late:
        for (x, y) in ((-21, -3), (3, 0), (-12, -8)):
            houses.cone(CLAY, x, y, 0.24, 0.35, 0.25, 0.55, 8)
    m.add(0, g.build(), "ground")
    m.add(1, walls.build(), "outer-wall")
    m.add(2, inner.build(), "inner-walls")
    m.add(3, houses.build(), "houses")
    if late:
        green = Parts("ge_green")
        r = rnd(41)
        for (x, y, h, rr) in ((-24, -2, 7, 4.2), (6, 20, 6, 3.5), (30, -18, 6.5, 3.6), (-40, -18, 5, 3.0), (18, -26, 5.5, 3.2), (-6, -26, 4.5, 2.6)):
            tree(green, x, y, h, rr, 0.2, LEAF if h > 5.5 else LEAF_DK)
        for i in range(38):
            a = next(r) * math.tau
            fr = 0.25 + next(r) * 0.6
            x, y = GE_RX * fr * math.cos(a) * 0.85, GE_RY * fr * math.sin(a) * 0.85
            bush(green, x, y, 0.9 + next(r) * 1.1, 0.2, GRASS if i % 3 else LEAF_DK)
        for i in range(26):
            a = next(r) * math.tau
            x, y = ge_pt(math.degrees(a), 1.06)
            bush(green, x, y, 1.0 + next(r) * 1.4, 0.0, GRASS_DK if i % 2 else LEAF_DK)
        for d in (20, 140, 230, 300):
            t = math.radians(d)
            px, py = ge_pt(d, 0.96)
            bush(green, px, py, 1.1, 0.2 + ge_h(t), GRASS)
        m.add(4, green.build(), "overgrowth")
    return m


# ---------------------------------------------------------------- the Hill Complex

HZ = 3.6   # height of the rock summit the walls stand on

HILL_BOULDERS = [   # x, y, rx, ry, height, base offset (a boulder perched on another)
    (-128, 18, 10, 8, 12, 0), (-120, -26, 8, 7, 10, 0), (-75, 34, 9, 7, 13, 0), (-58, -44, 9, 7, 11, 0), (-60, 42, 10, 8, 12, 0),
    (-35, 8, 12, 9, 17, 0), (-30, 5, 7, 6, 9, 13), (-20, 28, 8, 7, 13, 0), (-12, -26, 10, 8, 15, 0), (8, -12, 13, 10, 20, 0), (14, -16, 7, 6, 9, 15),
    (22, -32, 9, 8, 12, 0), (30, 30, 9, 7, 12, 0), (40, 2, 8, 7, 15, 0), (47, 21, 5, 4, 7, 0),
    (62, 28, 11, 8, 19, 0), (60, -30, 10, 8, 17, 0), (84, 42, 9, 7, 15, 0), (108, 32, 12, 9, 22, 0), (102, 37, 7, 6, 9, 16), (122, 4, 8, 10, 18, 0),
    (112, -30, 11, 9, 20, 0), (118, -25, 6, 5, 8, 15), (86, -40, 8, 6, 13, 0),
    (-48, -20, 3.5, 3, 4, 0), (12, 46, 4, 3, 4.5, 0), (48, -44, 4, 3, 4, 0), (-104, -36, 4, 3, 4, 0), (130, -12, 4, 4, 5, 0), (-140, 0, 5, 4, 5, 0), (-6, 44, 3, 3, 3.5, 0),
]


def loft(P, color, rings):
    """Stacked outlines [(pts, z), ...] (same point count) joined into one closed solid."""
    n = len(rings[0][0])
    v, f = [], []
    for pts, z in rings:
        v += [(x, y, z) for x, y in pts]
    f.append(tuple(range(n))[::-1])
    for k in range(len(rings) - 1):
        a, b = k * n, (k + 1) * n
        f += [(a + i, a + (i + 1) % n, b + (i + 1) % n, b + i) for i in range(n)]
    L = (len(rings) - 1) * n
    f.append(tuple(range(L, L + n)))
    P.poly(color, v, f)


def hill_base(P):
    wob = lambda t: 0.05 * math.sin(3 * t + 0.4) + 0.03 * math.cos(5 * t + 1.0)
    rings = [(ell(0, 0, 134 * k, 54 * k, 64, wob, p=2.5), z) for k, z in ((1.0, 0.0), (0.985, 1.4), (0.962, 2.8), (0.945, HZ))]
    loft(P, ROCK_DK, rings[:3])
    loft(P, ROCK, rings[2:])
    for i, (x, y, rx, ry, rz, zo) in enumerate(HILL_BOULDERS):
        z0 = (0.0 if abs(x) > 128 or abs(y) > 44 else HZ - rz * 0.12) + zo
        boulder(P, x, y, rx, ry, rz, z0, i + 1, (ROCK, ROCK_LT, ROCK_DK)[i % 3], 11 if rx > 6 else 8, 6, i * 0.7)


def hill_walls(P, early=False):
    """The summit walls. Returns obstacle circles for placing houses."""
    k = 0.45 if early else 1.0
    obs = [(x, y, max(rx, ry) * 0.9) for x, y, rx, ry, rz, zo in HILL_BOULDERS]
    # Western Enclosure: the largest, its wall following the cliff on the west and south
    if early:
        stone_wall(P, arc_pts(-90, -2, 32, 30, 150, 300, 2.4), 2.8, 2.0, 1.3, False, HZ, 5)
    else:
        hfun = lambda d: 7.5 + 2.0 * max(0.0, -math.sin(math.radians(d)))
        for (a0, a1) in ((55, 124), (142, 226), (246, 305)):
            pts = arc_pts(-90, -2, 32, 30, a0, a1, 2.0)
            ds = [a0 + (a1 - a0) * i / (len(pts) - 1) for i in range(len(pts))]
            stone_wall(P, pts, [hfun(d) for d in ds], 5.0, 2.6, False, HZ, 14)
        stone_wall(P, [(-104, 10), (-92, 14), (-80, 11)], 3.0, 1.5, 0.9, False, HZ, 5)
    obs += [(-90, -2, 0)]
    # rim walls along the cliff edges, linking the boulders
    sh = 5.0 * k
    stone_wall(P, [(-50, -36), (-40, -40), (-25, -38), (-10, -40), (8, -41), (20, -40)], sh, 2.4 * (0.8 if early else 1), 1.3, False, HZ, 8 if not early else 4)
    if not early:
        stone_wall(P, [(48, 38), (30, 42), (14, 41), (0, 36), (-18, 40), (-35, 40), (-50, 36)], 4.2, 2.2, 1.2, False, HZ, 8)
        # a narrow passage between two parallel walls
        stone_wall(P, [(-30, -12), (-18, -9), (-6, -4.5)], 3.2, 1.4, 0.8, False, HZ, 6)
        stone_wall(P, [(-31, -14.8), (-19, -11.8), (-7, -7.3)], 3.2, 1.4, 0.8, False, HZ, 6)
        # 'the Recess': a small enclosure in the middle of the summit
        enclosure(P, 5, 20, 9, 8, 3.6, 1.6, 0.9, gaps=[(246, 270)], z0=HZ, courses=7)
        # the Eastern Enclosure: walls between the boulders
        for wpts in ([(63, -21), (60, -11), (60, -4.5)], [(60, 4.5), (60, 12), (63, 19)], [(72, 34), (78, 39)], [(93, 40), (98, 36)],
                     [(116, 24), (119, 14)], [(121, -8), (118, -20)], [(101, -34), (94, -38)], [(78, -40), (70, -36)]):
            stone_wall(P, wpts, 5.5, 2.4, 1.2, False, HZ, 10)
        # the balcony enclosure: a walled terrace against the boulders above the Eastern Enclosure
        slab(P, ROCK, ell(76, 30, 7, 5.5, 14), HZ, 4.0)
        stone_wall(P, arc_pts(76, 30, 7, 5.5, 190, 350, 1.6), 1.8, 0.9, 0.6, False, HZ + 4.0, 4)
    else:
        stone_wall(P, [(63, -21), (60, -11), (60, -4.5)], 1.8, 1.3, 0.8, False, HZ, 4)
        stone_wall(P, [(101, -34), (94, -38)], 1.6, 1.2, 0.8, False, HZ, 3)
    obs += [(5, 20, 9.5), (92, 0, 12), (76, 30, 7), (-18, -10, 4), (-28, -13, 3), (-8, -6, 3)]
    return obs


def hill_ascent_stubs(P):
    # top of the Ancient Ascent at the south-west entrance, and the Terrace Ascent on the north
    for k in range(8):
        P.cube(GR1 if k % 2 else GR3, -108, -30 - k * 1.25, 0, 2.4, 1.25, HZ - k * 0.45)
    for k in range(7):
        P.cube(GR1 if k % 2 else GR3, 2, 50 + k * 1.3, 0, 2.2, 1.3, HZ - k * 0.5)


def hill_complex(variant="1350"):
    early, late = variant == "1100", variant == "1500"
    m = Model("hill-complex")
    rock = Parts("hc_rock")
    hill_base(rock)
    walls = Parts("hc_walls")
    obs = hill_walls(walls, early)
    hill_ascent_stubs(walls)
    top = Parts("hc_top")
    if not early:
        # turrets and monoliths along the top of the Western Enclosure's wall
        for i, d in enumerate(range(150, 300, 9)):
            t = math.radians(d)
            if 122 < d < 144 or 224 < d < 248:
                continue
            x, y = -90 + 32 * math.cos(t) * 0.93, -2 + 30 * math.sin(t) * 0.93
            zt = HZ + 7.5 + 2.0 * max(0.0, -math.sin(t))
            if i % 2:
                top.cone(GR3, x, y, zt, 0.9, 0.75, 1.5, 10)
            else:
                monolith(top, x, y, zt, 2.8, 0.32, GR2)
        # the Eastern Enclosure's platform with the soapstone birds on their columns, and tall monoliths behind
        stone_wall(top, ell(92, 0, 11, 4.2, 28), 1.3, 1.3, 1.0, True, HZ, 3, lean=0.4)
        slab(top, GR1, ell(92, 0, 10.0, 3.2, 28), HZ, 1.25)
        for i in range(6):
            bird_column(top, 83.5 + i * 3.4, -1.0, HZ + 1.25, -math.pi / 2 + (0.3 if i % 2 else -0.3), S=2.0)
        for i, x in enumerate((84, 89, 95, 100)):
            monolith(top, x, 2.0, HZ + 1.25, 4.2 + (i % 2) * 1.0, 0.45, GR3)
    # daga houses on the summit
    houses = Parts("hc_houses")
    r = rnd(5 if early else 9)
    cands = []
    for i in range(400):
        x, y = -120 + next(r) * 240, -40 + next(r) * 80
        if ((x / 124) ** 2.6 if x > 0 else (-x / 124) ** 2.6) + (abs(y) / 44) ** 2.6 < 1:
            cands.append((x, y))
    taken = []
    rr = 2.6 if early else 2.9
    fixed = [] if early else [(-108, -12), (-100, 17), (-82, -18), (-76, 15), (-96, 2), (100, 18), (104, -16), (78, -20), (-45, -22), (-40, 25), (30, -15), (22, 12)]
    spots = free_spots(fixed + cands, rr, obs, taken, 1.6)
    n = {"1100": 34, "1350": 24, "1500": 6}[variant]
    for i, (x, y) in enumerate(spots[:n]):
        hut(houses, x, y, rr - (0.4 if i % 3 == 0 else 0), HZ, plat=0.0 if early else (0.5 if i % 2 else 0.0), plat_col=DAGA_DK, door=next(r) * math.tau)
    if late:
        for (x, y) in spots[n:n + 10]:
            mound(houses, x, y, rr + 0.5, HZ)
    m.add(0, rock.build(), "kopje")
    m.add(1, walls.build(), "walls")
    if not early:
        m.add(2, top.build(), "birds-and-turrets")
    m.add(3, houses.build(), "houses")
    if late or early:
        green = Parts("hc_green")
        r = rnd(77)
        for i in range(46 if late else 14):
            x, y = -125 + next(r) * 250, -46 + next(r) * 92
            if ((abs(x) / 126) ** 2.6 + (abs(y) / 47) ** 2.6) > 1:
                continue
            if late and i % 6 == 0:
                tree(green, x, y, 6 + next(r) * 3, 3 + next(r) * 1.5, HZ, LEAF)
            else:
                bush(green, x, y, 0.9 + next(r) * 1.3, HZ, GRASS if i % 2 else LEAF_DK)
        m.add(4, green.build(), "trees")
    return m


# ---------------------------------------------------------------- the smaller stone enclosures

def valley_ruins(variant="1350"):
    late = variant == "1500"
    m = Model("valley-ruins")
    g = Parts("vr_ground")
    slab(g, EARTH, [(-70, -25), (70, -25), (70, 25), (-70, 25)], 0, 0.2)
    walls = Parts("vr_walls")
    encl = [(-46, 0, 18, 14, 5.0, 2.6, [(74, 98), (296, 318)]), (-10, 4, 13, 11, 4.2, 2.2, [(250, 272)]),
            (24, -2, 15, 12, 4.8, 2.4, [(146, 168), (14, 36)]), (55, 6, 11, 10, 3.8, 2.0, [(196, 220)])]
    for (cx, cy, rx, ry, h, tb, gaps) in encl:
        enclosure(walls, cx, cy, rx, ry, h, tb, tb * 0.55, gaps=gaps, z0=0.2, courses=8, wob=lambda t: 0.04 * math.sin(3 * t + cx))
    stone_wall(walls, [(-30, -14), (-25, -13.5), (-20, -11.5)], 2.0, 1.2, 0.8, False, 0.2, 4)
    stone_wall(walls, [(38, -9), (42, -7), (46, -3.5)], 2.0, 1.2, 0.8, False, 0.2, 4)
    stone_wall(walls, [(-66, 14), (-61, 18), (-56, 19)], 1.8, 1.1, 0.7, False, 0.2, 4)
    houses = Parts("vr_houses")
    plat = [(-53, 2, 2.8, -0.5), (-40, -3, 2.8, 1.0), (-45, 7, 2.6, 0.2), (-10, 4, 3.2, -1.8), (18, -3, 2.8, 2.6), (29, 0, 2.8, 0.4), (55, 6, 2.8, -2.4)]
    ground = [(-25, 16, 2.4), (5, -18, 2.6), (40, 16, 2.4), (-64, -17, 2.4), (64, -18, 2.4)]
    keepp = {0, 4} if late else set(range(len(plat)))
    keepg = {1} if late else set(range(len(ground)))
    for i, (x, y, r, d) in enumerate(plat):
        if i in keepp:
            hut(houses, x, y, r, 0.2, plat=0.7, door=d)
        else:
            mound(houses, x, y, r + 0.5, 0.2)
    for i, (x, y, r) in enumerate(ground):
        if i in keepg:
            hut(houses, x, y, r, 0.2, door=-math.pi / 2)
            granary(houses, x + 4.2, y - 1.5, 0.8, 0.8, 0.2)
        elif late:
            mound(houses, x, y, r + 0.4, 0.2)
    m.add(0, g.build(), "ground")
    m.add(1, walls.build(), "walls")
    m.add(2, houses.build(), "houses")
    green = Parts("vr_green")
    r = rnd(13 if late else 31)
    for (x, y) in ((-63, 4), (-28, -2), (8, 20), (40, -20), (66, 18)):
        tree(green, x, y, 6.5, 3.4, 0.2, LEAF)
    for i in range(40 if late else 10):
        x, y = -68 + next(r) * 136, -23 + next(r) * 46
        bush(green, x, y, 0.7 + next(r) * (1.4 if late else 0.6), 0.2, GRASS if i % 2 else LEAF_DK)
    m.add(3, green.build(), "trees")
    return m


def ridge_ruins():
    m = Model("ridge-ruins")
    g = Parts("rr_ground")
    slab(g, EARTH, [(-35, -25), (35, -25), (35, 25), (-35, 25)], 0, 0.2)
    slab(g, ROCK_DK, ell(0, 0, 31, 19, 32, lambda t: 0.06 * math.sin(3 * t)), 0.2, 0.6)
    slab(g, ROCK, ell(0, 0, 28, 16.5, 32, lambda t: 0.06 * math.sin(3 * t)), 0.8, 0.5)
    for i, (x, y, rx, ry, rz) in enumerate([(-24, 9, 5, 4, 4.5), (22, 11, 4, 3.5, 3.5), (-20, -12, 3.5, 3, 3), (27, -9, 4, 3, 3.5), (8, 15, 3, 2.5, 2.5)]):
        boulder(g, x, y, rx, ry, rz, 1.1, i + 40, (ROCK, ROCK_LT)[i % 2])
    walls = Parts("rr_walls")
    enclosure(walls, -4, 2, 14, 10, 3.8, 2.0, 1.1, gaps=[(254, 282)], z0=1.3, courses=7, wob=lambda t: 0.05 * math.sin(2 * t + 1))
    stone_wall(walls, arc_pts(16, -1, 7, 6, -70, 120, 1.8), 3.0, 1.6, 0.9, False, 1.3, 6)
    houses = Parts("rr_houses")
    hut(houses, -9, 3, 2.6, 1.3, plat=0.5, plat_col=DAGA_DK, door=-1.2)
    hut(houses, 1, 1, 2.6, 1.3, plat=0.5, plat_col=DAGA_DK, door=-1.8)
    hut(houses, 17, -1, 2.4, 1.3, door=0.2)
    hut(houses, -26, -17, 2.4, 0.2, door=0.6)
    hut(houses, 25, 18, 2.4, 0.2, door=-2.0)
    granary(houses, -20, -20, 0.8, 0.8, 0.2)
    for (x, y) in ((-30, 18), (30, -19)):
        tree(houses, x, y, 6, 3.2, 0.2)
    m.add(0, g.build(), "ridge")
    m.add(1, walls.build(), "walls")
    m.add(2, houses.build(), "houses")
    return m


def eastern_ruins():
    m = Model("eastern-ruins")
    g = Parts("er_ground")
    slab(g, EARTH, [(-40, -27.5), (40, -27.5), (40, 27.5), (-40, 27.5)], 0, 0.2)
    walls = Parts("er_walls")
    levels = [(-10.0, 1.8), (6.0, 3.6)]
    for (yf, z) in levels:
        front = [(x, yf + 2.5 * math.sin(x / 9.0 + yf)) for x in range(-38, 39, 4)]
        slab(g, ROCK_DK if z > 2 else EARTH_DK, front + [(38, 27.5), (-38, 27.5)], 0.2, z - 0.2)
        stone_wall(walls, list(reversed(front)), z - 0.1, 1.2, 0.9, False, 0.2, max(3, int(z * 2)), lean=0.6, rounded=False)
    for i, (x, y, rx, ry, rz) in enumerate([(-25, 20, 8, 6, 8), (15, 22, 9, 7, 9), (32, 10, 6, 6, 7), (-34, 2, 4, 3.5, 3.5), (36, -20, 4, 3, 3)]):
        boulder(g, x, y, rx, ry, rz, 3.4 if y > 8 else 1.6 if y > -8 else 0.2, i + 60, (ROCK, ROCK_LT)[i % 2])
    stone_wall(walls, [(-18, 21), (-12, 15), (-3, 12.5), (4, 13.5), (8, 16)], 3.2, 1.6, 0.9, False, 3.6, 6)
    stone_wall(walls, [(-31, 9), (-35, 14)], 2.4, 1.3, 0.8, False, 3.6, 4)
    houses = Parts("er_houses")
    hut(houses, -5, 21, 2.8, 3.6, door=-1.6)
    hut(houses, 26, 18, 2.4, 3.6, door=-2.2)
    hut(houses, -20, -2, 2.6, 1.8, door=-1.4)
    hut(houses, 8, -3, 2.6, 1.8, door=-1.7)
    hut(houses, 27, -3, 2.4, 1.8, door=-1.2)
    hut(houses, -24, -19, 2.4, 0.2, door=0.4)
    hut(houses, 18, -19, 2.4, 0.2, door=2.6)
    granary(houses, -4, -18, 0.8, 0.8, 0.2)
    for (x, y) in ((-36, -24), (0, 25), (36, 25)):
        tree(houses, x, y, 6, 3.0, 0.2 if y < 0 else 3.6)
    m.add(0, g.build(), "slope")
    m.add(1, walls.build(), "terrace-walls")
    m.add(2, houses.build(), "houses")
    return m


def hill_ascent():
    m = Model("hill-ascent")
    prof = [(-55, 0.3), (-40, 1.6), (-25, 3.6), (-8, 6.4), (8, 9.0), (25, 12.0), (40, 15.0), (55, 17.0)]

    def zs(y):
        for (y0, z0), (y1, z1) in zip(prof, prof[1:]):
            if y0 <= y <= y1:
                return z0 + (z1 - z0) * (y - y0) / (y1 - y0)
        return prof[-1][1] if y > 0 else prof[0][1]

    g = Parts("ha_slope")
    # the rock slope: a wedge rising to the north, a little uneven across
    v, f = [], []
    n = len(prof)
    for (y, z) in prof:
        v += [(-15, y, 0), (15, y, 0), (15, y, z + 0.3 + 0.3 * math.sin(y / 7)), (-15, y, z + 0.3 - 0.3 * math.sin(y / 9))]
    for i in range(n - 1):
        a, b = 4 * i, 4 * (i + 1)
        f += [(a + 3, a + 2, b + 2, b + 3), (a, b, b + 1, a + 1), (a, a + 3, b + 3, b), (a + 1, b + 1, b + 2, a + 2)]
    L = 4 * (n - 1)
    f += [(0, 1, 2, 3), (L + 3, L + 2, L + 1, L)]
    g.poly(ROCK, v, f)
    for i, (x, y, rx, ry, rz) in enumerate([(-10, -44, 5, 4.5, 6), (10, -32, 6, 5, 8), (-11, -16, 5.5, 5, 8), (-6.5, -27, 2.5, 2.5, 3.5), (10, 2, 6, 6, 10), (7.5, 18, 2.5, 3, 4),
                                            (-10, 20, 6, 5, 10), (11, 34, 5, 5, 8), (-10, 44, 6, 5, 9), (12, 50, 3.5, 3, 5), (-13, -54, 2.5, 2, 2.5), (13, -50, 2, 2, 2)]):
        boulder(g, x, y, rx, ry, rz, max(0.0, zs(y) - 0.8), i + 80, (ROCK_LT, ROCK, ROCK_DK)[i % 3])
    steps = Parts("ha_steps")
    walls = Parts("ha_walls")
    # lower flight on the west, a landing, upper flight on the east
    for (x0, y0, y1) in ((-3.0, -54, -6), (3.0, -2, 53)):
        y = y0
        k = 0
        while y < y1:
            steps.cube(GR3 if k % 2 else GR2, x0, y + 0.8, 0, 2.6, 1.6, zs(y + 0.8) + 0.7)
            y += 1.6
            k += 1
        for side in (-1, 1):
            ys = [y0 + (y1 - y0) * i / 14 for i in range(15)]
            pts = [(x0 + side * 1.4, yy) for yy in ys]
            if side > 0:
                pts = list(reversed(pts))
                ys = list(reversed(ys))
            stone_wall(walls, pts, 2.2, 1.2, 0.8, False, [zs(yy) + 0.3 for yy in ys], 5, lean=0.6, rounded=True)
    steps.cube(GR1, 0, -4, 0, 9.4, 4.4, zs(-4) + 0.7)
    # the narrow gateway at the top
    stone_wall(walls, [(-14, 53), (-7, 52.5), (1.5, 53)], 3.0, 1.6, 1.0, False, zs(53), 6)
    stone_wall(walls, [(4.5, 53), (9, 52.5), (14, 53)], 3.0, 1.6, 1.0, False, zs(53), 6)
    m.add(0, g.build(), "slope")
    m.add(1, steps.build(), "steps")
    m.add(2, walls.build(), "walls")
    return m


# ---------------------------------------------------------------- cattle, houses, crafts and fields

def royal_kraal():
    m = Model("royal-kraal")
    g = Parts("rk_ground")
    slab(g, GRASS, ell(0, 0, 45, 35, 40), 0, 0.15)
    slab(g, EARTH_DK, ell(0, 0, 30, 22, 40), 0.15, 0.08)
    fence = Parts("rk_fence")
    r = rnd(3)
    n = 150
    for i in range(n):
        t = math.tau * i / n
        if abs(math.atan2(math.sin(t), math.cos(t))) < 0.06:
            continue
        x, y = 31 * math.cos(t), 23 * math.sin(t)
        fence.cone(POLE, x, y, 0.15, 0.12, 0.1, 1.9 + next(r) * 0.4, 5)
        if i % 2 == 0:
            fence.cone(THORN, 33 * math.cos(t), 25 * math.sin(t), 0.15, 1.1, 0.4, 1.1, 6)
    for z in (0.6, 1.1, 1.6):
        fence.beam(POLE, (31, -1.6, z), (31, 1.6, z), 0.12)
    for (x0, y0, rx, ry) in ((-30, 28, 5, 4),):
        for i in range(24):
            t = math.tau * i / 24
            fence.cone(POLE, x0 + rx * math.cos(t), y0 + ry * math.sin(t), 0.15, 0.1, 0.08, 1.4, 5)
    houses = Parts("rk_huts")
    hut(houses, 34, 26, 2.6, 0.15, door=-2.4)
    hut(houses, 40, 16, 2.2, 0.15, door=3.0)
    hut(houses, -38, -24, 2.4, 0.15, door=0.6)
    granary(houses, -40, -15, 0.8, 0.8, 0.15)
    for (x, y) in ((-40, 10), (20, -31), (-8, 31)):
        tree(houses, x, y, 7, 3.6, 0.15)
    herd = Parts("rk_herd")
    k = 0
    for i in range(7):
        for j in range(4):
            x = -24 + i * 7.6 + (next(r) - 0.5) * 3
            y = -14 + j * 8.5 + (next(r) - 0.5) * 3
            if (x / 27) ** 2 + (y / 19) ** 2 > 1 or next(r) < 0.18:
                continue
            cow(herd, x, y, next(r) * 360, CATTLE[k % len(CATTLE)])
            k += 1
    for (x, y, d) in ((-26, 28, 20), (-32, 27, 200), (36, -3, 0), (40, 4, 160), (-24, -30, 30)):
        cow(herd, x, y, d, CATTLE[k % len(CATTLE)], 0.7 if x < -20 and y > 20 else 1.0)
        k += 1
    m.add(0, g.build(), "ground")
    m.add(1, fence.build(), "fence")
    m.add(2, houses.build(), "huts")
    m.add(3, herd.build(), "cattle")
    return m


def daga_wall(P, pts, h=1.6, t=0.6, z0=0.2):
    stone_wall(P, pts, h, t, t * 0.8, False, z0, 3, (DAGA, DAGA_LT, DAGA), lean=0.5)


def elite_houses():
    m = Model("elite-houses")
    g = Parts("eh_ground")
    slab(g, EARTH, [(-30, -25), (30, -25), (30, 25), (-30, 25)], 0, 0.2)
    slab(g, SWEPT, ell(0, -2, 22, 14, 32), 0.2, 0.04)
    plat = Parts("eh_platforms")
    stone_wall(plat, ell(-12, 9, 11.5, 9, 30), 1.2, 1.2, 1.0, True, 0.2, 3, lean=0.4)
    slab(plat, DAGA_LT, ell(-12, 9, 10.6, 8.1, 30), 0.2, 1.15)
    stone_wall(plat, ell(14, 12, 7.5, 6.5, 24), 0.9, 1.0, 0.8, True, 0.2, 2, lean=0.4)
    slab(plat, DAGA_LT, ell(14, 12, 6.6, 5.6, 24), 0.2, 0.85)
    for k in range(3):
        plat.cube(GR1 if k % 2 else GR3, -12, -1.2 - k * 0.7, 0.2, 2.4, 0.7, 1.15 - k * 0.38)
    houses = Parts("eh_houses")
    hut(houses, -16, 10, 4.0, 1.35, wh=2.8, door=-1.4, wall=DAGA_LT)
    hut(houses, -5, 8, 3.2, 1.35, wh=2.6, door=-1.9, wall=DAGA_LT)
    hut(houses, 14, 12, 3.6, 1.05, wh=2.7, door=-1.7, wall=DAGA_LT)
    hut(houses, 10, -11, 3.0, 0.24, door=2.2)
    hut(houses, -15, -13, 3.2, 0.24, door=1.2)
    granary(houses, 22, -3, 0.9, 1.0, 0.24)
    granary(houses, 24, -9, 0.8, 1.0, 0.24)
    daga_wall(houses, [(-26, 4), (-25, -4), (-20, -10)])
    daga_wall(houses, [(-11, -15), (-2, -17.5), (7, -14)])
    daga_wall(houses, [(18, 6), (21, 1.5)])
    daga_wall(houses, [(-0.5, 12), (6.5, 14)])
    for (x, y) in ((2, -4), (3, -3), (-2, -6)):
        houses.cone(CLAY, x, y, 0.24, 0.35, 0.25, 0.5, 8)
    houses.cone(ROCK_DK, 0, -2, 0.24, 0.8, 0.7, 0.15, 8)
    for (x, y) in ((-26, -20), (25, 20), (26, -20)):
        tree(houses, x, y, 6.5, 3.4, 0.2)
    r = rnd(71)
    for k in range(12):
        x, y = -29 + next(r) * 58, (-24 + next(r) * 4) if k % 2 else (21 + next(r) * 3)
        bush(houses, x, y, 0.6 + next(r) * 0.6, 0.2, GRASS_DK if k % 3 else LEAF_DK)
    m.add(0, g.build(), "ground")
    m.add(1, plat.build(), "platforms")
    m.add(2, houses.build(), "houses")
    return m


def smelting_area():
    m = Model("smelting-area")
    g = Parts("sm_ground")
    slab(g, EARTH, [(-25, -20), (25, -20), (25, 20), (-25, 20)], 0, 0.2)
    slab(g, EARTH_DK, ell(-4, 4, 14, 8, 24), 0.2, 0.04)
    works = Parts("sm_works")
    for i, (x, y) in enumerate(((-12, 6), (-4, 9), (4, 6))):
        works.dome(DAGA_DK, x, y, 0.2, 1.8, 0.25, 12, 3)
        slant_cyl(works, FURNACE, (x, y), 1.0, 0.4, (x, y), 0.55, 2.3, 12)
        works.cone(CHAR, x, y, 2.3, 0.45, 0.45, 0.03, 12)
        for a in (-1.9, -1.2, 0.0) if i != 1 else (-1.6, -0.4, 1.0):
            works.beam(CLAY, (x + math.cos(a) * 0.7, y + math.sin(a) * 0.7, 0.55), (x + math.cos(a) * 1.7, y + math.sin(a) * 1.7, 0.75), 0.18)
        a = -1.5
        for s in (-0.5, 0.5):
            works.dome(LEATHER, x + math.cos(a) * 2.6 + s * 0.5, y + math.sin(a) * 2.6, 0.2, 0.5, 0.8, 8, 3)
    # the forge under its shelter
    for (px, py) in ((9, -9), (15, -9), (9, -3), (15, -3)):
        works.cone(POLE, px, py, 0.2, 0.12, 0.1, 2.4, 5)
    works.cone(THATCH_C, 12, -6, 2.5, 4.6, 0, 2.4, 12)
    works.cone(DAGA_DK, 12, -6, 0.2, 0.9, 0.8, 0.5, 8)
    works.cube(ROCK_DK, 13.6, -5.2, 0.2, 0.7, 0.5, 0.6)
    for k in range(5):
        works.beam(ROCK_LT, (9.5 + k * 0.5, -10.4, 0.25), (9.8 + k * 0.5, -10.4, 0.9), 0.1, 0.35)
    # charcoal, slag, ore and firewood
    for (x, y, r) in ((-18, -10, 2.2), (-12, -14, 1.8)):
        works.cone(CHAR, x, y, 0.2, r, 0.2, r * 0.9, 10)
    works.dome(SLAG, 17, 11, 0.2, 4.2, 0.35, 12, 3)
    works.cone(ORE, -20, 7, 0.2, 2.0, 0.3, 1.2, 10)
    for k in range(6):
        works.beam(TRUNK, (-6 + k * 0.1, -13 + k * 0.45, 0.35), (2 + k * 0.1, -13 + k * 0.45, 0.35 + (k % 2) * 0.2), 0.28)
    for (x, y) in ((-21, 16), (21, -16), (8, -17)):
        tree(works, x, y, 6, 3.2, 0.2)
    hut(works, 20, 2, 2.4, 0.2, door=3.0)
    hut(works, -18, 15, 2.2, 0.2, door=-0.8, wall=DAGA_DK)
    # a small bowl furnace and crucibles for copper, ore baskets, tuyere pipes drying, slag scatter
    works.dome(DAGA_DK, 2, -6, 0.2, 1.3, 0.4, 10, 3)
    works.cone(CHAR, 2, -6, 0.6, 0.7, 0.5, 0.1, 10)
    for k in range(4):
        works.cone(CLAY, 0.0 + k * 0.6, -8.2, 0.2, 0.18, 0.14, 0.3, 8)
        works.cone(MAT, -16 + k * 1.1, 2 + (k % 2) * 0.6, 0.2, 0.45, 0.55, 0.5, 8)
        works.cone(ORE, -16 + k * 1.1, 2 + (k % 2) * 0.6, 0.7, 0.45, 0.1, 0.25, 8)
    for k in range(7):
        works.beam(CLAY, (-9 + k * 0.45, -3.5, 0.3), (-9 + k * 0.45, -2.2, 0.3), 0.2)
    r = rnd(57)
    for k in range(14):
        works.dome(SLAG, 13 + next(r) * 9, 6 + next(r) * 10, 0.2, 0.5 + next(r) * 0.6, 0.4, 7, 2)
    for k in range(5):
        works.cone(CHAR, -20 + k * 2.6, -14 - (k % 2) * 2.5, 0.2, 1.0 + (k % 3) * 0.3, 0.15, 1.0, 9)
    for k in range(4):
        works.beam(TRUNK, (6 + k * 0.4, 14, 0.35 + k * 0.05), (12, 14 + k * 0.4, 0.35), 0.26)
    # a low windbreak of poles and grass behind the furnaces
    for k in range(18):
        works.cone(POLE, -15 + k * 1.1, 12.5 + 0.6 * math.sin(k * 0.5), 0.2, 0.08, 0.06, 1.8, 5)
    works.cube(THATCH_DK, -5.6, 12.5, 0.5, 19.5, 0.35, 1.2)
    for k in range(24):
        bush(works, -24 + next(r) * 48, -19 + next(r) * 38 if k % 2 else 17 + next(r) * 2, 0.6 + next(r) * 0.6, 0.2, GRASS_DK)
    m.add(0, g.build(), "ground")
    m.add(1, works.build(), "furnaces")
    return m


def trade_ground():
    m = Model("trade-ground")
    g = Parts("tg_ground")
    slab(g, EARTH, [(-35, -25), (35, -25), (35, 25), (-35, 25)], 0, 0.2)
    slab(g, SWEPT, ell(0, 0, 30, 20, 32), 0.2, 0.04)
    sh = Parts("tg_shelters")
    for (cx, cy, w, d) in ((6, 8, 9, 5.5), (-4, -11, 8, 5)):
        for sx in (-1, 0, 1):
            for sy in (-1, 1):
                sh.cone(POLE, cx + sx * (w / 2 - 0.4), cy + sy * (d / 2 - 0.4), 0.24, 0.12, 0.1, 2.4, 5)
        sh.frustum(THATCH_C, cx, cy, 2.4, w + 1.0, d + 1.0, w * 0.6, d * 0.4, 1.0)
    hut(sh, 26, -10, 3.4, 0.24, plat=0.6, door=2.6)
    tree(sh, -22, 12, 9, 6.5, 0.24, LEAF)
    goods = Parts("tg_goods")
    r = rnd(19)
    # mats with goods
    for (x, y, w, d) in ((4, 8, 6, 3.5), (-4, -11, 5.5, 3.2), (-14, -4, 4, 3), (14, -2, 4.5, 3), (-16, 14, 4, 2.8), (2, -1, 3.6, 2.6)):
        goods.cube(MAT, x, y, 0.24, w, d, 0.05)
    # ivory: pairs of curved tusks
    for (x, y, a) in ((-15, -4, 0.2), (-14.5, -3, 0.25), (-13.5, -5, 0.1), (13, 18, 1.4), (15, 18, 1.5)):
        c, s = math.cos(a), math.sin(a)
        p = [(x + c * (-1.4) , y + s * (-1.4), 0.35), (x, y, 0.5), (x + c * 1.4 - s * 0.4, y + s * 1.4 + c * 0.4, 0.75)]
        goods.beam(IVORY, p[0], p[1], 0.22)
        goods.beam(IVORY, p[1], p[2], 0.17)
    # cloth bales, bead strings, pots, copper ingots
    for k in range(6):
        goods.cube((CLOTH_B, CLOTH_W, CLOTH_R)[k % 3], 2.5 + (k % 3) * 1.2, 7.5 + (k // 3) * 1.1, 0.29, 1.0, 0.9, 0.5)
    for k in range(8):
        goods.cube(BEADS[k % 4], -5.8 + k * 0.5, -11, 0.29, 0.14, 2.2, 0.08)
    for k in range(6):
        goods.cone(CLAY if k % 2 else "#4A4038", 13 + (k % 3) * 0.9, -3 + (k // 3) * 1.0, 0.29, 0.35, 0.25, 0.55, 8)
    for k in range(4):
        goods.cube(COPPER, -16 + k * 0.7, 14, 0.29, 0.25, 1.0, 0.08)
        goods.cube(COPPER, -16 + k * 0.7, 14, 0.29, 0.7, 0.25, 0.08)
    goods.cone(GOLD_C, 1.5, -1.0, 0.29, 0.12, 0.1, 0.12, 6)
    goods.cone(GREEN, 2.5, -1.2, 0.29, 0.3, 0.42, 0.35, 10)
    goods.cone("#5E8F7A", 1.8, -0.2, 0.29, 0.25, 0.35, 0.18, 10)
    for k in range(4):
        cow(goods, 22 + (k % 2) * 4, 12 + (k // 2) * 4, 30 + k * 70, CATTLE[k])
    for k in range(5):
        cow(goods, -28 + (k % 3) * 2.2, -18 + (k // 3) * 1.8, 20 + k * 60, CATTLE[(k + 2) % 6], 0.5, hump=False)
    # more mats: salt, iron hoes, baskets of grain, pots, soapstone bowls, cloth
    for (x, y, w, d) in ((-22, -6, 4, 3), (-8, 14, 4.5, 3), (18, 6, 4, 3), (-24, -14, 3.5, 2.6), (10, -18, 4.5, 3)):
        goods.cube(MAT, x, y, 0.24, w, d, 0.05)
    for k in range(5):
        goods.beam("#4A4A4C", (-23.5 + k * 0.7, -7, 0.32), (-23.5 + k * 0.7, -5.2, 0.32), 0.25, 0.08)
    for k in range(6):
        goods.cone(MAT, -9.6 + (k % 3) * 1.4, 13.4 + (k // 3) * 1.3, 0.29, 0.5, 0.6, 0.5, 8)
        goods.cone("#C9A86A", -9.6 + (k % 3) * 1.4, 13.4 + (k // 3) * 1.3, 0.79, 0.55, 0.1, 0.25, 8)
    for k in range(5):
        goods.cone(SOAP, 16.6 + (k % 3) * 1.1, 5.4 + (k // 3) * 1.1, 0.29, 0.3, 0.42, 0.3, 10)
    for k in range(6):
        goods.cube((CLOTH_R, CLOTH_B, CLOTH_W)[k % 3], 8.5 + (k % 3) * 1.2, -18.5 + (k // 3) * 1.1, 0.29, 1.0, 0.9, 0.45 + (k % 2) * 0.2)
    for k in range(5):
        goods.cube("#E8E4DC", -25 + (k % 3) * 0.9, -14.5 + (k // 3) * 0.9, 0.29, 0.7, 0.7, 0.4)
    for k in range(4):
        goods.cube(LEATHER, 22 - k * 0.9, -14, 0.24, 0.8, 1.6, 0.25 + 0.05 * k)
    tree(goods, 28, 18, 6, 3.4, 0.24, LEAF_DK)
    tree(goods, -30, 20, 6.5, 3.2, 0.24, LEAF)
    rr = rnd(29)
    for k in range(24):
        bush(goods, -34 + next(rr) * 68, (-24 + next(rr) * 5) if k % 2 else (20 + next(rr) * 4), 0.6 + next(rr) * 0.6, 0.2, GRASS_DK)
    m.add(0, g.build(), "ground")
    m.add(1, sh.build(), "shelters")
    m.add(2, goods.build(), "goods")
    return m


def homestead(P, cx, cy, seed, huts=3, pen=True, rot=0.0):
    r = rnd(seed)
    slab(P, SWEPT, ell(cx, cy, 7.5, 6.5, 20), 0.2, 0.04)
    for i in range(huts):
        a = rot + math.tau * i / huts + 0.4
        x, y = cx + math.cos(a) * 7.0, cy + math.sin(a) * 6.0
        hut(P, x, y, 2.2 + next(r) * 0.6, 0.2, wall=DAGA if i % 2 else DAGA_DK, door=a + math.pi)
    a = rot + math.tau * (huts - 0.5) / huts + 0.4
    granary(P, cx + math.cos(a) * 7.5, cy + math.sin(a) * 6.5, 0.8, 0.9, 0.2)
    P.cube(ROCK_DK, cx + 1.0, cy - 1.0, 0.2, 1.2, 0.7, 0.3)
    P.cone(CLAY, cx - 1.2, cy + 0.5, 0.24, 0.35, 0.25, 0.5, 8)
    if pen:
        a = rot + math.pi * 1.25
        px, py = cx + math.cos(a) * 12, cy + math.sin(a) * 10
        for i in range(16):
            t = math.tau * i / 16
            if i == 0:
                continue
            P.cone(POLE, px + 3.0 * math.cos(t), py + 3.0 * math.sin(t), 0.2, 0.09, 0.07, 1.2, 5)
        for k in range(3):
            cow(P, px + (k - 1) * 1.4, py + (k % 2) * 0.8, 40 + k * 90, CATTLE[(seed + k) % len(CATTLE)], 0.45, horns=True, hump=False)


def commoners_village():
    m = Model("commoners-village")
    g = Parts("cv_ground")
    slab(g, GRASS, [(-45, -35), (45, -35), (45, 35), (-45, 35)], 0, 0.2)
    houses = Parts("cv_homesteads")
    homestead(houses, -24, 12, 3, 4, True, 0.3)
    homestead(houses, 16, 18, 7, 3, True, 1.9)
    homestead(houses, -4, -16, 11, 4, False, 0.9)
    homestead(houses, 28, -14, 17, 3, True, 3.6)
    green = Parts("cv_green")
    for (x, y, h, r) in ((-40, -28, 6, 3.4), (0, 4, 7, 3.8), (40, 30, 6, 3.2), (-40, 30, 5.5, 3.0), (40, 2, 6, 3.0)):
        tree(green, x, y, h, r, 0.2)
    rr = rnd(23)
    for i in range(14):
        bush(green, -44 + next(rr) * 88, -34 + next(rr) * 68, 0.6 + next(rr) * 0.7, 0.2, GRASS_DK if i % 2 else LEAF_DK)
    m.add(0, g.build(), "ground")
    m.add(1, houses.build(), "homesteads")
    m.add(2, green.build(), "trees")
    return m


def field(P, x0, x1, y0, y1, rows, head, stalk_h=1.8, crop=True):
    for k in range(rows):
        y = y0 + (y1 - y0) * (k + 0.5) / rows
        P.cube(EARTH_DK, (x0 + x1) / 2, y, 0.2, x1 - x0, 1.1, 0.25)
        if crop:
            P.cube(STALK, (x0 + x1) / 2, y, 0.45, x1 - x0 - 0.6, 0.5, stalk_h)
            P.cube(head, (x0 + x1) / 2, y, 0.45 + stalk_h, x1 - x0 - 0.6, 0.6, 0.35)


def fields_granaries():
    m = Model("fields-granaries")
    g = Parts("fg_ground")
    slab(g, GRASS, [(-65, -40), (65, -40), (65, 40), (-65, 40)], 0, 0.2)
    slab(g, EARTH, [(-62, -38), (-12, -38), (-12, 38), (-62, 38)], 0.2, 0.03)
    slab(g, EARTH, [(12, -38), (62, -38), (62, 38), (12, 38)], 0.2, 0.03)
    crops = Parts("fg_crops")
    field(crops, -60, -14, 6, 36, 12, SORGHUM, 2.0)
    field(crops, 14, 60, 8, 36, 12, MILLET, 1.1)
    field(crops, -60, -14, -36, -6, 11, SORGHUM, 0.0, crop=False)
    field(crops, 14, 60, -36, -8, 11, BEAN, 0.5)
    stores = Parts("fg_stores")
    for (x, y) in ((-3, 2), (5, -4), (-5, -10), (4, 10)):
        granary(stores, x, y, 1.0, 1.0, 0.2)
    # the watchers' platform against birds
    for (px, py) in ((-2.5, 20.5), (0.5, 20.5), (-2.5, 23.5), (0.5, 23.5)):
        stores.cone(POLE, px, py, 0.2, 0.13, 0.11, 3.0, 5)
    stores.cube(POLE, -1, 22, 3.0, 4.0, 4.0, 0.25)
    stores.cone(THATCH_C, -1, 22, 4.6, 2.9, 0, 1.4, 8)
    for (px, py) in ((-2.6, 20.6), (0.6, 23.4)):
        stores.beam(POLE, (px, py, 3.25), (px, py, 4.7), 0.1)
    # a threshing floor on a granite outcrop, with grain heaps; a shelter
    stores.dome(ROCK_LT, 2, -24, 0.0, 6.0, 0.12, 14, 3)
    stores.cone(SORGHUM, 0.5, -23, 0.7, 1.0, 0.1, 0.6, 10)
    stores.cone("#C9A86A", 3.5, -25, 0.7, 0.8, 0.1, 0.45, 10)
    hut(stores, 6, -33, 2.4, 0.2, door=2.0)
    for (x, y) in ((-63, 0), (63, 0), (0, 37), (-30, 39), (35, -39), (-38, -39)):
        tree(stores, x, y, 6, 3.0, 0.2)
    r = rnd(83)
    for k in range(22):
        x, y = (-63.5 + next(r) * 127, 39 - next(r) * 1.5) if k % 2 else (-63.5 + next(r) * 127, -39 + next(r) * 1.5)
        bush(stores, x, y, 0.6 + next(r) * 0.6, 0.2, GRASS_DK if k % 3 else LEAF_DK)
    m.add(0, g.build(), "ground")
    m.add(1, crops.build(), "fields")
    m.add(2, stores.build(), "granaries")
    return m


BUILDERS = {
    "great-zimbabwe/great-enclosure": great_enclosure,
    "great-zimbabwe/great-enclosure-1500": lambda: great_enclosure("1500"),
    "great-zimbabwe/hill-complex": hill_complex,
    "great-zimbabwe/hill-complex-1100": lambda: hill_complex("1100"),
    "great-zimbabwe/hill-complex-1500": lambda: hill_complex("1500"),
    "great-zimbabwe/valley-ruins": valley_ruins,
    "great-zimbabwe/valley-ruins-1500": lambda: valley_ruins("1500"),
    "great-zimbabwe/ridge-ruins": ridge_ruins,
    "great-zimbabwe/eastern-ruins": eastern_ruins,
    "great-zimbabwe/hill-ascent": hill_ascent,
    "great-zimbabwe/royal-kraal": royal_kraal,
    "great-zimbabwe/elite-houses": elite_houses,
    "great-zimbabwe/smelting-area": smelting_area,
    "great-zimbabwe/trade-ground": trade_ground,
    "great-zimbabwe/commoners-village": commoners_village,
    "great-zimbabwe/fields-granaries": fields_granaries,
}
