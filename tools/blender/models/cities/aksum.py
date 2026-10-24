"""Aksum landmark miniatures: the carved granite stelae (the Great Stele standing and fallen, King Ezana's Stele,
the Rome Stele), the stelae fields, the mansions of Dungur and Ta'akha Maryam, the royal tombs, the Mai Shum
reservoir, the church of Mary of Zion in three forms, the Ezana stone and the coronation thrones.

Conventions as in FORMAT.md: metres, origin at the ground centre, +X east, +Y north, +Z up, main face toward -Y.

Aksumite walls are drawn with their two signatures: bays that step in and out along the wall, and timber
courses every metre or so whose square ends ("monkey heads") stick out of the stone. The stelae carry the same
architecture carved in granite: storeys of beam ends and lattice windows over a false door, a rounded head.
Small parts are collected per colour in a Parts buffer and made into one mesh each.
"""
import math
from chronokit import Model, box, cylinder, dome, join, shade, mesh_from
from worldkit import *

STELE_C = "#8F8B84"          # the grey nepheline syenite of the stelae
STELE_DK = "#6E6A64"
ROUGH_C = "#9C978C"
STONE, STONE_LT, STONE_DK = "#A99D86", "#BDB29B", "#8E836E"
DRESSED = "#B7AD98"          # dressed granite of podiums and steps
WOOD, WOOD_DK = "#5C4430", "#45321F"
EARTH, EARTH_DK, GRASS = "#B5A27A", "#9E8C66", "#8E9A62"
ROCK, ROCK_DK = "#8A8274", "#736C60"
WATER_C = "#5F878C"
BRONZE_C, GOLD_C = "#8C6E3E", "#C9A24A"
WHITE_C, PLAST = "#EAE4D6", "#D9CFBA"
THATCH_C, JUNIPER = "#A88E58", "#5E7148"
ROBE = "#E8E2D2"
BOX_FACES = [(3, 2, 1, 0), (4, 5, 6, 7), (0, 1, 5, 4), (1, 2, 6, 5), (2, 3, 7, 6), (3, 0, 4, 7)]
FACES = {"S": (0, -1), "N": (0, 1), "E": (1, 0), "W": (-1, 0)}


def rnd(seed):
    """A small deterministic generator, so the miniatures are the same every bake."""
    s = [seed * 2654435761 % 4294967296 or 1]

    def r(a=0.0, b=1.0):
        s[0] = (1103515245 * s[0] + 12345) % 2147483648
        return a + (b - a) * s[0] / 2147483648
    return r


# ---------------------------------------------------------------- a buffer of small parts, one mesh per colour

class Parts:
    def __init__(self, name):
        self.name = name
        self.g = {}
        self.xf = None          # optional vertex transform (used to lay fallen stelae down)

    def poly(self, color, verts, faces):
        if self.xf:
            verts = [self.xf(v) for v in verts]
        vs, fs = self.g.setdefault(color, ([], []))
        b = len(vs)
        vs.extend(verts)
        fs.extend(tuple(b + i for i in f) for f in faces)

    def hexa(self, color, v8):
        self.poly(color, v8, BOX_FACES)

    def cube(self, color, cx, cy, z0, w, d, h):
        if w <= 0 or d <= 0 or h <= 0:
            return
        v = []
        for z in (z0, z0 + h):
            v += [(cx - w / 2, cy - d / 2, z), (cx + w / 2, cy - d / 2, z), (cx + w / 2, cy + d / 2, z), (cx - w / 2, cy + d / 2, z)]
        self.poly(color, v, BOX_FACES)

    def rcube(self, color, cx, cy, z0, w, d, h, ang):
        """A box turned by ang radians about its own vertical axis."""
        c, s = math.cos(ang), math.sin(ang)
        v = []
        for z in (z0, z0 + h):
            for px, py in ((-w / 2, -d / 2), (w / 2, -d / 2), (w / 2, d / 2), (-w / 2, d / 2)):
                v.append((cx + px * c - py * s, cy + px * s + py * c, z))
        self.poly(color, v, BOX_FACES)

    def frustum(self, color, cx, cy, z0, w0, d0, w1, d1, h):
        v = [(cx - w0 / 2, cy - d0 / 2, z0), (cx + w0 / 2, cy - d0 / 2, z0), (cx + w0 / 2, cy + d0 / 2, z0), (cx - w0 / 2, cy + d0 / 2, z0),
             (cx - w1 / 2, cy - d1 / 2, z0 + h), (cx + w1 / 2, cy - d1 / 2, z0 + h), (cx + w1 / 2, cy + d1 / 2, z0 + h), (cx - w1 / 2, cy + d1 / 2, z0 + h)]
        self.poly(color, v, BOX_FACES)

    def cone(self, color, x, y, z0, r0, r1, h, n=8, start=0.0):
        v = [(x + r0 * math.cos(start + math.tau * i / n), y + r0 * math.sin(start + math.tau * i / n), z0) for i in range(n)]
        if r1 > 1e-4:
            v += [(x + r1 * math.cos(start + math.tau * i / n), y + r1 * math.sin(start + math.tau * i / n), z0 + h) for i in range(n)]
            f = [tuple(range(n))[::-1], tuple(range(n, 2 * n))] + [(i, (i + 1) % n, n + (i + 1) % n, n + i) for i in range(n)]
        else:
            v.append((x, y, z0 + h))
            f = [tuple(range(n))[::-1]] + [(i, (i + 1) % n, n) for i in range(n)]
        self.poly(color, v, f)

    def disc(self, color, x, y, z, r, depth, face="S", n=8):
        """A short cylinder sticking out of a wall face (a round beam end, a boss, a plate)."""
        nx, ny = FACES[face]
        tx, ty = abs(ny), abs(nx)
        v = []
        for k in (0, 1):
            off = depth * k
            for i in range(n):
                a = math.tau * i / n
                u, w = r * math.cos(a), r * math.sin(a)
                v.append((x + tx * u + nx * off, y + ty * u + ny * off, z + w))
        f = [tuple(range(n)), tuple(range(2 * n - 1, n - 1, -1))] + [(i, (i + 1) % n, n + (i + 1) % n, n + i) for i in range(n)]
        self.poly(color, v, f)

    def dome(self, color, x, y, z0, r, squash=1.0, n=10, rings=4):
        v, f = [], []
        for k in range(rings):
            phi = (math.pi / 2) * k / rings
            v += [(x + r * math.cos(phi) * math.cos(math.tau * i / n), y + r * math.cos(phi) * math.sin(math.tau * i / n), z0 + r * math.sin(phi) * squash) for i in range(n)]
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
                verts.append(tuple(p[i] + a * u[i] + b * v[i] for i in range(3)))
        self.poly(color, verts, BOX_FACES)

    def build(self):
        objs = [mesh_from(f"{self.name}_{i}", vs, fs, (0, 0, 0), color) for i, (color, (vs, fs)) in enumerate(self.g.items()) if fs]
        return join(objs, self.name)


def fbox(P, color, x, y, z0, along, out, h, face, off=0.0):
    """A box on a wall face: `along` the face, `out` across it, its centre `off` metres out from (x, y)."""
    nx, ny = FACES[face]
    if nx == 0:
        P.cube(color, x, y + ny * off, z0, along, out, h)
    else:
        P.cube(color, x + nx * off, y, z0, out, along, h)


def face_line(cx, cy, w, d, face):
    nx, ny = FACES[face]
    if nx == 0:
        return (cx, cy + ny * d / 2), w, (nx, ny), (1, 0)
    return (cx + nx * w / 2, cy), d, (nx, ny), (0, 1)


# ---------------------------------------------------------------- Aksumite masonry: stepped bays, timber courses, monkey heads

def podium(P, cx, cy, w, d, h, tiers=3, color=DRESSED, step=0.7, batter=0.15):
    """A stepped podium of dressed stone: each tier set back from the one below, its sides slightly battered."""
    th = h / tiers
    for k in range(tiers):
        w0, d0 = w - 2 * step * k, d - 2 * step * k
        P.frustum(shade(color, -0.04 * (k % 2)), cx, cy, th * k, w0, d0, w0 - batter, d0 - batter, th)
    return w - 2 * step * (tiers - 1) - batter, d - 2 * step * (tiers - 1) - batter


def stairs(P, cx, cy, w, z_top, run, face="S", color=DRESSED, n=None, z0=0.0):
    """A flight of steps rising toward (cx, cy) from the given side; (cx, cy) is the top edge."""
    n = n or max(3, int((z_top - z0) / 0.3))
    nx, ny = FACES[face]
    rise = (z_top - z0) / n
    for i in range(n):
        dist = run * (n - i - 0.5) / n
        x, y = cx + nx * dist, cy + ny * dist
        depth = run / n * (1.0 + 0.0)
        fbox(P, shade(color, -0.03 * (i % 2)), x, y, z0, w, depth + run * i / n * 0, rise * (i + 1), face)


def monkey_wall(P, cx, cy, w, d, h, z0=0.0, color=STONE, faces="NSEW", bay=3.4, proud=0.35, course=1.05,
                head=0.2, head_every=0.75, windows=None, win_w=0.9, win_h=1.1, door=None, door_w=1.6, door_h=2.4, cornice=True):
    """An Aksumite block: rubble walls in alternating projecting and recessed bays, tied by timber courses whose
    square ends stick out ('monkey heads'); dark windows framed in timber; a timber cornice at the roof."""
    P.cube(color, cx, cy, z0, w, d, h)
    if cornice:
        P.cube(WOOD, cx, cy, z0 + h - 0.05, w + 0.3, d + 0.3, 0.22)
        P.cube(shade(color, 0.04), cx, cy, z0 + h + 0.17, w + 0.1, d + 0.1, 0.3)
    for face in faces:
        (mx, my), L, (nx, ny), (tx, ty) = face_line(cx, cy, w, d, face)
        n = max(1, round(L / bay))
        if n % 2 == 0:
            n += 1
        seg = L / n
        for i in range(n):
            u = -L / 2 + seg * (i + 0.5)
            px, py = mx + tx * u, my + ty * u
            out = proud if i % 2 == 0 else 0.0
            if out:
                fbox(P, shade(color, 0.03), px, py, z0, seg, out, h - 0.05, face, out / 2)
            # timber courses with their beam ends
            z = z0 + course
            while z < z0 + h - 0.45:
                fbox(P, WOOD, px, py, z, seg + (0.02 if out else -0.02), 0.06, 0.14, face, out + 0.03)
                m = max(1, int(seg / head_every))
                for k in range(m):
                    uu = -seg / 2 + seg * (k + 0.5) / m
                    fbox(P, WOOD_DK, px + tx * uu, py + ty * uu, z - 0.03, head, 0.2, head, face, out + 0.1)
                z += course
            # windows on the recessed bays, door in the middle bay of the door face
            if face == door and i == n // 2:
                framed_opening(P, px, py, z0, door_w, door_h, face, out, sill=False)
            elif windows and not out:
                for wz in windows:
                    if wz + win_h < h - 0.3:
                        framed_opening(P, px, py, z0 + wz, win_w, win_h, face, out)


def framed_opening(P, x, y, z, w, h, face, off=0.0, frame=0.16, sill=True):
    """A dark opening in a timber frame whose cross-pieces end in monkey heads at the corners."""
    fbox(P, DARK, x, y, z, w, 0.08, h, face, off + 0.02)
    nx, ny = FACES[face]
    tx, ty = abs(ny), abs(nx)
    zb = z - frame if sill else z
    for s in (-1, 1):
        fbox(P, WOOD, x + tx * s * (w / 2 + frame / 2), y + ty * s * (w / 2 + frame / 2), zb, frame, 0.12, h + frame + (z - zb), face, off + 0.06)
    for zz in ((z - frame, z + h) if sill else (z + h,)):
        fbox(P, WOOD, x, y, zz, w + 2 * frame, 0.12, frame, face, off + 0.06)
        for s in (-1, 1):
            fbox(P, WOOD_DK, x + tx * s * (w / 2 + frame * 1.2), y + ty * s * (w / 2 + frame * 1.2), zz - 0.02, 0.2, 0.22, 0.2, face, off + 0.12)


# ---------------------------------------------------------------- the carved stele

def stele(P, H, W, D, storeys, place, color=STELE_C, taper=0.86, cuts=(), sides=True, back=True, door_frac=0.17, plate=True):
    """An Aksumite stele in local coordinates (base centre at the origin, front toward -Y). `place(z)` returns the
    vertex transform for a part at height z (identity-plus-offset when standing, a laying-down move when fallen).

    Front and back are carved as a tower of `storeys` storeys: each a row of round beam ends over a timber band,
    then lattice windows; at the bottom a false door with its lock; at the top a rounded head that once held a
    metal plate. The faces carry a shallow central recess between raised edge strips."""
    Wt, Dt = W * taper, D * taper
    rh = Wt / 2
    Hs = H - rh
    wz = lambda z: W + (Wt - W) * z / Hs
    dz = lambda z: D + (Dt - D) * z / Hs
    zs = sorted(set([0.0, Hs] + [c for c in cuts if 0 < c < Hs]))
    for a, b in zip(zs, zs[1:]):
        P.xf = place((a + b) / 2)
        P.frustum(color, 0, 0, a, wz(a), dz(a), wz(b), dz(b), b - a)
        # raised edge strips on front and back (the frame round the recessed centre)
        for fy in (-1, 1):
            if fy == 1 and not back:
                continue
            for sx in (-1, 1):
                e0, e1 = W * 0.09, Wt * 0.09
                xa0, xb0 = sx * (wz(a) / 2 - e0), sx * wz(a) / 2
                xa1, xb1 = sx * (wz(b) / 2 - e1), sx * wz(b) / 2
                ya, yb = fy * dz(a) / 2, fy * dz(b) / 2
                t = 0.05 * fy
                v = [(min(xa0, xb0), ya, a), (max(xa0, xb0), ya, a), (max(xa0, xb0), ya + t, a), (min(xa0, xb0), ya + t, a),
                     (min(xa1, xb1), yb, b), (max(xa1, xb1), yb, b), (max(xa1, xb1), yb + t, b), (min(xa1, xb1), yb + t, b)]
                P.hexa(shade(color, 0.05), v)
    # the rounded head: a half disc, and the plate that was fixed to it
    P.xf = place(Hs + rh / 2)
    n = 14
    pts = [(rh * math.cos(math.pi * i / n), Hs + rh * math.sin(math.pi * i / n)) for i in range(n + 1)]
    v = [(x, -Dt / 2, z) for x, z in pts] + [(x, Dt / 2, z) for x, z in pts]
    m = n + 1
    f = [tuple(range(m)), tuple(range(2 * m - 1, m - 1, -1))] + [(i, i + 1, m + i + 1, m + i) for i in range(n)] + [(m - 1, 0, m, 2 * m - 1)]
    P.poly(color, v, f)
    if plate:
        P.disc(BRONZE_C, 0, -Dt / 2 + 0.01, Hs + rh * 0.42, rh * 0.42, 0.06, "S", 14)
        P.disc(shade(BRONZE_C, -0.2), 0, -Dt / 2 - 0.04, Hs + rh * 0.42, rh * 0.18, 0.04, "S", 10)
    # storeys
    base_h = H * door_frac
    top_m = rh * 0.25
    sh = (Hs - base_h - top_m) / storeys
    for faceo in ("S", "N", "E", "W"):
        if faceo == "N" and not back:
            continue
        if faceo in "EW" and not sides:
            continue
        nx, ny = FACES[faceo]
        for k in range(storeys + 1):
            z = base_h + k * sh
            P.xf = place(z + sh / 2)
            w, d = wz(z), dz(z)
            span = w if nx == 0 else d
            fx, fy = (nx * w / 2, ny * d / 2)
            # timber band and the row of round beam ends
            fbox(P, shade(color, -0.12), fx, fy, z, span * 0.98, 0.07, sh * 0.13, faceo, 0.035)
            nh = max(3, int(span / 0.3))
            for i in range(nh):
                u = -span / 2 + span * (i + 0.5) / nh
                px, py = fx + abs(ny) * u, fy + abs(nx) * u
                P.disc(shade(color, 0.06), px, py, z + sh * 0.065, sh * 0.06, 0.12, faceo, 8)
            if k == storeys:
                break
            # windows: four across on the broad faces, two on the narrow ones
            nw = 4 if nx == 0 else 2
            ww = span / (nw * 1.9)
            wh = sh * 0.5
            wz0 = z + sh * 0.3
            for i in range(nw):
                u = -span / 2 + span * (i + 0.5) / nw
                if nw == 4:
                    u *= 0.92
                px, py = fx + abs(ny) * u, fy + abs(nx) * u
                fbox(P, STELE_DK, px, py, wz0, ww, 0.04, wh, faceo, 0.0)
                fbox(P, shade(color, 0.04), px, py, wz0 - 0.06, ww + 0.14, 0.05, 0.08, faceo, 0.03)
                fbox(P, shade(color, 0.04), px, py, wz0 + wh, ww + 0.14, 0.05, 0.08, faceo, 0.03)
                fbox(P, shade(color, 0.0), px, py, wz0, ww * 0.16, 0.06, wh, faceo, 0.03)
                fbox(P, shade(color, 0.0), px, py, wz0 + wh * 0.45, ww, 0.06, wh * 0.1, faceo, 0.03)
    # the false door at the foot of the front (and the back on the great stelae)
    for faceo in (("S", "N") if back else ("S",)):
        nx, ny = FACES[faceo]
        P.xf = place(base_h / 2)
        dw, dh = W * 0.34, base_h * 0.72
        fy = ny * D / 2
        fbox(P, shade(color, -0.2), 0, fy, base_h * 0.12, dw, 0.05, dh, faceo, 0.0)
        for s in (-1, 1):
            fbox(P, shade(color, 0.07), s * (dw / 2 + 0.07), fy, base_h * 0.12 - 0.1, 0.14, 0.08, dh + 0.2, faceo, 0.04)
        fbox(P, shade(color, 0.07), 0, fy, base_h * 0.12 + dh, dw + 0.42, 0.08, 0.14, faceo, 0.04)
        fbox(P, shade(color, 0.07), 0, fy, base_h * 0.12 - 0.14, dw + 0.42, 0.08, 0.14, faceo, 0.04)
        for s in (-1, 1):
            for zz in (base_h * 0.12 - 0.14, base_h * 0.12 + dh):
                P.disc(shade(color, 0.07), s * (dw / 2 + 0.28), fy, zz + 0.07, 0.07, 0.1, faceo, 8)
        P.disc(BRONZE_C, dw * 0.25, fy, base_h * 0.12 + dh * 0.5, 0.07, 0.08, faceo, 8)
        P.disc(shade(color, -0.25), dw * 0.25, fy, base_h * 0.12 + dh * 0.35, 0.05, 0.06, faceo, 6)
    P.xf = None


def stele_platform(P, cx, cy, W, D, scale=1.0, color=DRESSED, altar=True):
    """The stepped base the stele stands in, with the base plate in front carved with offering hollows."""
    w, d = W * 3.0 * scale, D * 4.2 * scale
    P.cube(shade(color, -0.06), cx, cy, 0, w, d, 0.35)
    P.cube(color, cx, cy + d * 0.08, 0.35, w * 0.72, d * 0.66, 0.35)
    P.cube(shade(color, 0.03), cx, cy + d * 0.12, 0.7, W * 1.5, D * 1.9, 0.3)
    if altar:
        ay = cy - d * 0.34
        P.cube(shade(color, 0.05), cx, ay, 0.35, w * 0.58, d * 0.2, 0.42)
        for i in range(4):
            x = cx - w * 0.21 + w * 0.14 * i
            P.cone(DARK, x, ay, 0.775, 0.22 * scale, 0.16 * scale, 0.02, 10)
    return 1.0


def standing(x, y, z):
    return lambda zz: (lambda v: (v[0] + x, v[1] + y, v[2] + z))


def fallen(x0, y0, D, cuts, Hs, jitter, seed=3, lie="N"):
    """A transform for a stele fallen on its back (front up), its foot near (x0, y0), its pieces strung out
    northward (or eastward) with gaps and small twists."""
    r = rnd(seed)
    pieces = []
    bounds = [0.0] + list(cuts) + [10 ** 6]
    for k in range(len(bounds) - 1):
        pieces.append((bounds[k], bounds[k + 1], k * jitter[0], r(-1, 1) * jitter[1], r(-1, 1) * jitter[2]))

    def place(zc):
        for a, b, gap, yaw, side in pieces:
            if a <= zc < b:
                break
        mid = (a + min(b, Hs)) / 2 + gap
        c, s = math.cos(yaw), math.sin(yaw)

        def xf(v):
            x, y, z = v
            # lay down: height becomes distance north, the front face turns up
            X, Y, Z = x, z + gap, -y + D * 0.5
            # twist the piece about its own middle
            X, Y = side + (X * c - (Y - mid) * s), mid + (X * s + (Y - mid) * c)
            if lie == "E":
                X, Y = Y, -X
            return (X + x0, Y + y0, max(0.0, Z))
        return xf
    return place


# ---------------------------------------------------------------- the three great stelae

def great_stele(variant="standing"):
    """Stele 1, the Great Stele: 33 m, thirteen storeys, carved on all four faces; drawn standing or as it lies, broken."""
    return _great(33.0, 3.84, 2.35, None if variant == "standing" else "fallen")


def _great(H, W, D, mode):
    m = Model("great-stele")
    g, s = Parts("gs_ground"), Parts("gs_stele")
    g.cube(EARTH, 0, 0, 0, 14, 44, 0.12)
    by = -16.0
    stele_platform(g, 0, by, W, D, 1.0)
    rh = W * 0.86 / 2
    Hs = H - rh
    if mode is None:
        stele(s, H, W, D, 13, standing(0, by + D * 0.25, 1.0))
    else:
        stump = 1.6
        cuts = [stump, 6.2, 12.5, 18.4, 24.0, 28.6]
        lay = fallen(0.0, by + D * 0.25 + 1.5, D, [c - stump for c in cuts[1:]], Hs - stump, (0.75, 0.1, 0.55), seed=5)
        st = standing(0, by + D * 0.25, 1.0)

        def place(z):
            if z < stump:
                return st(z)
            f = lay(z - stump)
            return lambda v: f((v[0], v[1], v[2] - stump))
        stele(s, H, W, D, 13, place, cuts=cuts)
        r = rnd(11)
        for k in range(22):
            g.rcube(shade(STELE_C, -0.08), r(-3.4, 3.4), by + 3 + r(0, 33), 0.12, r(0.25, 0.8), r(0.2, 0.6), r(0.15, 0.4), r(0, 3))
    m.add(0, g.build(), "platform")
    m.add(1, s.build(), "stele")
    return m


def ezana_stele():
    """Stele 3, 'King Ezana's Stele': about 21 m, the last great stele, still standing."""
    m = Model("ezana-stele")
    g, s = Parts("es_ground"), Parts("es_stele")
    W, D = 2.65, 1.18
    g.cube(EARTH, 0, 0, 0, 10, 8, 0.12)
    stele_platform(g, 0, 0.3, W, D, 1.0)
    stele(s, 20.6, W, D, 9, standing(0, 0.3 + D * 0.25, 1.0))
    m.add(0, g.build(), "platform")
    m.add(1, s.build(), "stele")
    return m


def rome_stele(variant="standing"):
    """Stele 2, the 'Rome Stele': about 24 m; drawn standing, or fallen in pieces as the Italians found it in 1937."""
    m = Model("rome-stele")
    g, s = Parts("rs_ground"), Parts("rs_stele")
    W, D = 2.32, 1.3
    H = 24.0
    bx = -11.6
    g.cube(EARTH, 0, 0, 0, 30, 10, 0.12)
    # the platform turned so its altar faces south while the stele stands at the west end
    stele_platform(g, bx, 0, W, D, 0.95)
    rh = W * 0.86 / 2
    Hs = H - rh
    if variant == "standing":
        stele(s, H, W, D, 10, standing(bx, D * 0.25, 1.0))
    else:
        stump = 1.4
        cuts = [stump, 7.0, 13.2, 18.6]
        lay = fallen(0, 0, D, [c - stump for c in cuts[1:]], Hs - stump, (0.6, 0.06, 0.25), seed=9, lie="E")
        st = standing(bx, D * 0.25, 1.0)

        def place(z):
            if z < stump:
                return st(z)
            f = lay(z - stump)
            # the lying pieces start just east of the stump
            return lambda v: (lambda p: (p[0] + bx + 1.6, p[1], p[2]))(f((v[0], v[1], v[2] - stump)))
        stele(s, H, W, D, 10, place, cuts=cuts)
    m.add(0, g.build(), "platform")
    m.add(1, s.build(), "stele")
    return m




# ---------------------------------------------------------------- lesser stelae, rubble, small things

def rough_stele(P, x, y, h, w, d, r, lean=(0.0, 0.0), color=ROUGH_C):
    """An undressed granite slab set up over a grave: irregular sides, a rough point or rounded top."""
    j = lambda s: r(-s, s)
    b = [(x - w / 2 + j(0.08 * w), y - d / 2 + j(0.1 * d), 0), (x + w / 2 + j(0.08 * w), y - d / 2 + j(0.1 * d), 0),
         (x + w / 2 + j(0.08 * w), y + d / 2 + j(0.1 * d), 0), (x - w / 2 + j(0.08 * w), y + d / 2 + j(0.1 * d), 0)]
    th = h * r(0.78, 0.9)
    tw, td = w * r(0.6, 0.85), d * r(0.7, 0.9)
    tx, ty = x + lean[0] * th, y + lean[1] * th
    t = [(tx - tw / 2, ty - td / 2, th), (tx + tw / 2, ty - td / 2, th), (tx + tw / 2, ty + td / 2, th), (tx - tw / 2, ty + td / 2, th)]
    P.hexa(color, b + t)
    apex = (tx + lean[0] * (h - th) + j(tw * 0.25), ty + lean[1] * (h - th), h)
    P.poly(color, t + [apex], [(0, 1, 4), (1, 2, 4), (2, 3, 4), (3, 0, 4)])


def half_head(P, x, y, z, rad, depth, color, n=10):
    """The rounded head of a dressed stele: a half disc standing on the shaft."""
    pts = [(rad * math.cos(math.pi * i / n), rad * math.sin(math.pi * i / n)) for i in range(n + 1)]
    v = [(x + px, y - depth / 2, z + pz) for px, pz in pts] + [(x + px, y + depth / 2, z + pz) for px, pz in pts]
    m = n + 1
    f = [tuple(range(m)), tuple(range(2 * m - 1, m - 1, -1))] + [(i, i + 1, m + i + 1, m + i) for i in range(n)] + [(m - 1, 0, m, 2 * m - 1)]
    P.poly(color, v, f)


def dressed_stele(P, x, y, h, w, d, color=STELE_C, door=True, bands=0):
    """A dressed but mostly plain stele: tapering shaft, rounded head, perhaps a carved door and a few beam bands."""
    rad = w * 0.44
    P.frustum(color, x, y, 0, w, d, w * 0.88, d * 0.88, h - rad)
    half_head(P, x, y, h - rad, rad, d * 0.88, color)
    if door:
        fbox(P, shade(color, -0.22), x, y - d / 2, 0.4, w * 0.36, 0.05, h * 0.1, "S", 0.0)
        fbox(P, shade(color, 0.07), x, y - d / 2, 0.4 + h * 0.1, w * 0.5, 0.08, 0.14, "S", 0.03)
    for k in range(bands):
        z = h * (0.22 + 0.6 * k / max(1, bands))
        ww = w + (w * 0.88 - w) * z / (h - rad)
        fbox(P, shade(color, -0.1), x, y - d / 2 + 0.03 * z / h, z, ww, 0.06, 0.18, "S", 0.0)


def stone_base(P, x, y, w, d, h, color=DRESSED):
    P.cube(shade(color, -0.05), x, y, 0, w, d, h * 0.5)
    P.cube(color, x, y, h * 0.5, w * 0.8, d * 0.8, h * 0.5)


def rubble(P, cx, cy, w, d, n, r, color=STONE, z0=0.0, size=(0.3, 0.9)):
    for k in range(n):
        s = r(*size)
        P.rcube(shade(color, r(-0.08, 0.05)), cx + r(-w / 2, w / 2), cy + r(-d / 2, d / 2), z0, s, s * r(0.6, 1.0), s * r(0.4, 0.8), r(0, 3))


def tree(P, x, y, h, r_, color=JUNIPER, z0=0.0):
    P.cone(WOOD, x, y, z0, 0.18, 0.12, h * 0.4, 6)
    P.cone(color, x, y, z0 + h * 0.3, r_, r_ * 0.25, h * 0.55, 8)
    P.dome(shade(color, 0.05), x, y, z0 + h * 0.75, r_ * 0.45, 1.0, 8, 3)


def round_hut(P, x, y, r_, wall_h=2.0, color=STONE, thatch=THATCH_C, door="S"):
    P.cone(color, x, y, 0, r_, r_, wall_h, 12)
    P.cone(thatch, x, y, wall_h - 0.1, r_ * 1.2, 0.08, r_ * 1.25, 12)
    P.cone(WOOD_DK, x, y, wall_h + r_ * 1.15 - 0.1, 0.08, 0.02, 0.5, 4)
    nx, ny = FACES[door]
    fbox(P, DARK, x + nx * r_, y + ny * r_, 0, 0.8, 0.12, 1.6, door, 0.0)


def flat_house(P, x, y, w, d, h, color=STONE, door="S"):
    P.cube(color, x, y, 0, w, d, h)
    P.cube(shade(color, -0.07), x, y, h, w + 0.25, d + 0.25, 0.2)
    nx, ny = FACES[door]
    fbox(P, DARK, x + nx * w / 2, y + ny * d / 2, 0, 0.8, 0.1, 1.5, door, 0.03)


def ruin_block(P, cx, cy, w, d, hmax, r, z0=0.0, t=0.9, color=STONE, rooms=0):
    """The broken stumps of an Aksumite block: wall bases of uneven height, gaps, fallen stones."""
    for face in "NSEW":
        (mx, my), L, (nx, ny), (tx, ty) = face_line(cx, cy, w - t, d - t, face)
        n = max(1, int(L / 2.6))
        for i in range(n):
            if r() < 0.18:
                continue
            u = -L / 2 + L * (i + 0.5) / n
            hh = hmax * r(0.25, 1.0)
            fbox(P, shade(color, r(-0.06, 0.03)), mx + tx * u, my + ty * u, z0, L / n + 0.05, t, hh, face, 0.0)
    for k in range(rooms):
        if r() < 0.5:
            x = cx + r(-w / 3, w / 3)
            P.cube(shade(color, -0.04), x, cy, z0, t * 0.8, d - t, hmax * r(0.2, 0.6))
        else:
            y = cy + r(-d / 3, d / 3)
            P.cube(shade(color, -0.04), cx, y, z0, w - t, t * 0.8, hmax * r(0.2, 0.6))
    rubble(P, cx, cy, w + 1, d + 1, int((w + d) / 3), r, color, z0)


# ---------------------------------------------------------------- the stelae fields

def northern_stelae(variant="full"):
    """The eastern part of the royal stelae field: the terrace, three dressed stelae of 15-18 m and dozens of
    rough ones; in the early variant only rough stones and cairns."""
    m = Model("northern-stelae")
    g, t, s = Parts("ns_ground"), Parts("ns_terrace"), Parts("ns_stelae")
    r = rnd(21)
    g.cube(EARTH, 0, 0, 0, 64, 70, 0.12)
    early = variant == "early"
    if not early:
        # the terrace and its retaining wall of dressed blocks along the south, steps up in the middle
        t.cube(DRESSED, 0, 2, 0.12, 60, 44, 1.2)
        for i in range(24):
            fbox(t, shade(DRESSED, -0.06 * (i % 2)), -28.75 + i * 2.5, -20, 0.12, 2.4, 0.3, 1.25, "S", 0.15)
        stairs(t, 0, -20, 8, 1.32, 2.4, "S", DRESSED, 4)
        for x, y, h, w, d, n in ((-14, 6, 18.2, 1.9, 1.0, 6), (17, 4, 15.3, 1.6, 0.9, 5)):
            stone_base(t, x, y, w * 2.6, d * 3.2, 0.5)
            stele(s, h, w, d, n, standing(x, y, 1.82), sides=False)
        # stele 5, fallen and broken, front up
        lay = fallen(4.0, 3.0, 0.9, [5.5, 10.4], 15.0, (0.7, 0.08, 0.3), seed=17)

        def on_terrace(z):
            f = lay(z)
            return lambda v: (lambda q: (q[0], q[1], q[2] + 1.32))(f(v))
        stele(s, 15.8, 1.7, 0.9, 5, on_terrace, cuts=[5.5, 10.4], sides=False)
        z_ok = 1.32
        n, area = 34, (56, 38)
    else:
        z_ok = 0.12
        n, area = 46, (54, 56)
        for k in range(6):
            x, y = r(-22, 22), r(-22, 22)
            s.cone(STONE, x, y, 0.12, r(1.2, 2.0), 0.3, r(0.6, 1.1), 9)
    for k in range(n):
        x, y = r(-area[0] / 2, area[0] / 2), r(-area[1] / 2, area[1] / 2) + (2 if not early else 0)
        if not early and ((abs(x + 14) < 3 and abs(y - 6) < 3) or (abs(x - 4) < 3 and 1 < y < 22) or (abs(x - 17) < 3 and abs(y - 4) < 3)):
            continue
        h = r(1.2, 4.5) if early else r(1.5, 7.5)
        if r() < 0.22:
            s.rcube(ROUGH_C, x, y, z_ok, r(0.5, 0.9), h, r(0.35, 0.6), r(0, 3))
        else:
            p = Parts("tmp")
            rough_stele(p, 0, 0, h, r(0.5, 1.0) * (1 + h / 10), r(0.35, 0.6), r, (r(-0.06, 0.06), r(-0.06, 0.06)))
            for col, (vs, fs) in p.g.items():
                s.poly(col, [(vx + x, vy + y, vz + z_ok) for vx, vy, vz in vs], fs)
    m.add(0, g.build(), "ground")
    m.add(1, t.build() if t.g else None, "terrace")
    m.add(2, s.build(), "stelae")
    return m


def gudit_stelae():
    """The stelae field west of the town: hundreds of small undressed stelae over 3rd-4th-century graves, many fallen."""
    m = Model("gudit-stelae")
    g, s = Parts("gd_ground"), Parts("gd_stelae")
    r = rnd(33)
    g.cube(EARTH, 0, 0, 0, 90, 50, 0.12)
    g.cube(GRASS, -10, 4, 0.12, 60, 34, 0.04)
    # grave platforms and slab-covered shafts
    for k in range(9):
        x, y = r(-38, 38), r(-18, 18)
        g.cube(shade(STONE, r(-0.05, 0.05)), x, y, 0.12, r(3, 6), r(2.5, 5), r(0.3, 0.6))
    for k in range(150):
        x, y = r(-42, 42), r(-21, 21)
        h = r(1.0, 4.2) if r() < 0.9 else r(5, 7.5)
        if r() < 0.35:
            s.rcube(shade(ROUGH_C, r(-0.05, 0.05)), x, y, 0.12, r(0.4, 0.8), h, r(0.3, 0.5), r(0, 3))
            continue
        p = Parts("tmp")
        if h > 5:
            dressed_stele(p, 0, 0, h, r(0.8, 1.1), r(0.45, 0.6), shade(STELE_C, 0.04), door=False)
        else:
            rough_stele(p, 0, 0, h, r(0.4, 0.9), r(0.3, 0.5), r, (r(-0.08, 0.08), r(-0.08, 0.08)))
        for col, (vs, fs) in p.g.items():
            s.poly(col, [(vx + x, vy + y, vz + 0.12) for vx, vy, vz in vs], fs)
    m.add(0, g.build(), "ground")
    m.add(1, s.build(), "stelae")
    return m


# ---------------------------------------------------------------- the mansions: Dungur and Ta'akha Maryam

def pavilion(P, cx, cy, w, d, h, pod_h, tower=5.0, tower_h=None, stair_face="S", color=STONE, windows=(1.3, 4.4)):
    """The central block of an Aksumite mansion: a stepped podium, a two-storey block with monkey-head walls,
    four corner towers and a broad stair to the door."""
    tower_h = tower_h or h + 2.6
    pw, pd = w + 6, d + 6
    for k in range(3):
        P.frustum(shade(DRESSED, -0.04 * (k % 2)), cx, cy, pod_h / 3 * k, pw - 1.4 * k, pd - 1.4 * k, pw - 1.4 * k - 0.25, pd - 1.4 * k - 0.25, pod_h / 3)
    monkey_wall(P, cx, cy, w, d, h, pod_h, color, windows=windows, door=stair_face, bay=3.0, head_every=0.95)
    for sx in (-1, 1):
        for sy in (-1, 1):
            monkey_wall(P, cx + sx * (w / 2 - tower / 2 + 0.6), cy + sy * (d / 2 - tower / 2 + 0.6), tower, tower, tower_h, pod_h,
                        shade(color, 0.03), bay=2.4, windows=(h + 0.6,), win_w=0.7, win_h=0.9, head_every=0.95)
    nx, ny = FACES[stair_face]
    stairs(P, cx + nx * (pw / 2), cy + ny * (pd / 2), 5.0, pod_h, pod_h * 1.6, stair_face, DRESSED)


def mansion(name, W, D, plan, mode="full", seed=40):
    """A mansion on the Dungur / Ta'akha Maryam model: ranges of rooms round courtyards, a central pavilion.
    `plan` = dict(ranges=[(cx, cy, w, d, h)], pav=(cx, cy, w, d, h, pod_h), base=h, stair=(x, w))."""
    m = Model(name)
    g, a, b = Parts(name + "_ground"), Parts(name + "_ranges"), Parts(name + "_pavilion")
    r = rnd(seed)
    base = plan["base"]
    g.cube(EARTH, 0, 0, 0, W, D, 0.12)
    # the platform the whole mansion stands on, paved courts on top
    g.frustum(DRESSED, 0, 0, 0.12, W - 2, D - 2, W - 2.6, D - 2.6, base - 0.12)
    g.cube(shade(DRESSED, 0.06), 0, 0, base, W - 3.2, D - 3.2, 0.05)
    sx, sw = plan["stair"]
    if mode == "full":
        # the double staircase up to the entrance in the south range
        for s in (-1, 1):
            stairs(g, sx + s * (sw / 2 + 1.2), -(D - 2) / 2, sw / 2, base, 1.0, "S", DRESSED, 4)
        for (cx, cy, w, d, h) in plan["ranges"]:
            dk = plan["deco"]
            monkey_wall(a, cx, cy, w, d, h, base + 0.05, STONE, faces="NSEW", bay=dk[0], windows=(1.6,), course=dk[1], head_every=dk[2],
                        door="S" if cy - d / 2 < -D / 2 + 4 else None)
        pc = plan["pav"]
        pavilion(b, pc[0], pc[1], pc[2], pc[3], pc[4], base + pc[5])
    else:
        rubble(g, 0, 0, W - 6, D - 6, int(W * D / 60), r, STONE, base)
        for (cx, cy, w, d, h) in plan["ranges"]:
            ruin_block(a, cx, cy, w, d, 1.6, r, base, rooms=2)
        pc = plan["pav"]
        pw, pd = pc[2] + 6, pc[3] + 6
        for k in range(3):
            b.frustum(shade(DRESSED, -0.04 * (k % 2)), pc[0], pc[1], base + pc[5] / 3 * k, pw - 1.4 * k, pd - 1.4 * k, pw - 1.4 * k - 0.25, pd - 1.4 * k - 0.25, pc[5] / 3)
        ruin_block(b, pc[0], pc[1], pc[2], pc[3], 2.2, r, base + pc[5], rooms=3)
        stairs(b, pc[0], pc[1] - pd / 2, 5.0, base + pc[5], pc[5] * 1.6, "S", shade(DRESSED, -0.05), z0=base)
        # earth heaped over the ruin: low mounds with grass
        for k in range(8):
            g.dome(shade(EARTH, r(-0.06, 0.02)), r(-W / 2 + 6, W / 2 - 6), r(-D / 2 + 6, D / 2 - 6), base - 0.3, r(3, 7), 0.25, 10, 3)
        for k in range(5):
            tree(g, r(-W / 2 + 4, W / 2 - 4), r(-D / 2 + 4, D / 2 - 4), r(3.5, 6), r(1.3, 2.2), shade(JUNIPER, r(-0.05, 0.08)), base)
    m.add(0, g.build(), "platform")
    m.add(1, a.build(), "ranges")
    m.add(2, b.build(), "pavilion")
    return m


DUNGUR = dict(base=1.2, stair=(0, 8), deco=(3.6, 1.2, 1.3),
              ranges=[(0, -24.5, 52, 6, 4.4), (0, 24.5, 52, 6, 4.4), (-23.5, 0, 6, 43, 4.4), (23.5, 0, 6, 43, 4.4),
                      (-13.5, 12.0, 14, 5, 3.8), (13.5, 12.0, 14, 5, 3.8)],
              pav=(0, -2.0, 16, 15, 7.2, 2.4))

TAAKHA = dict(base=1.0, stair=(0, 10), deco=(5.0, 1.4, 2.4),
              ranges=[(0, -36.5, 112, 6, 4.2), (0, 36.5, 112, 6, 4.2), (-54, 0, 6, 67, 4.2), (54, 0, 6, 67, 4.2),
                      (-30, 0, 6, 67, 4.0), (30, 0, 6, 67, 4.0), (-42, 10, 18, 5, 3.6), (42, -10, 18, 5, 3.6),
                      (0, 22, 30, 5, 3.8)],
              pav=(0, -4.0, 22, 18, 7.6, 2.6))


def dungur(variant="full"):
    return mansion("dungur", 60, 58, DUNGUR, variant, 41)


def taakha_maryam(variant="full"):
    return mansion("taakha-maryam", 120, 80, TAAKHA, variant, 52)


# ---------------------------------------------------------------- tombs

def tomb_block(P, cx, cy, w, d, h, slot_w, slot_len, color=DRESSED, door="dark"):
    """A raised tomb platform of dressed granite cut by an open stairwell from the south, going down to the
    ground-level entrance of the chambers below."""
    y0, y1 = cy - d / 2, cy + d / 2
    xs0, xs1 = cx - slot_w / 2, cx + slot_w / 2
    ye = y0 + slot_len
    P.cube(color, (cx - w / 2 + xs0) / 2, cy, 0.12, xs0 - (cx - w / 2), d, h)
    P.cube(color, (xs1 + cx + w / 2) / 2, cy, 0.12, cx + w / 2 - xs1, d, h)
    P.cube(color, cx, (ye + y1) / 2, 0.12, slot_w, y1 - ye, h)
    # coursing lines of the big ashlar blocks
    nc = max(2, int(h / 0.55))
    ch = h / nc
    for k in range(nc):
        z = 0.12 + k * ch
        if k:
            P.cube(shade(color, -0.12), cx, cy, z, w + 0.04, d + 0.04, 0.05)
        # vertical joints of the big blocks, staggered course by course
        for face in "NSEW":
            (mx, my), L, (nx, ny), (tx, ty) = face_line(cx, cy, w, d, face)
            bl = 1.6
            nb = int(L / bl)
            for i in range(nb):
                u = -L / 2 + bl * (i + 0.5 * (k % 2)) + 0.4
                if -L / 2 < u < L / 2 and not (face == "S" and abs(u) < slot_w / 2 + 0.2):
                    fbox(P, shade(color, -0.12), mx + tx * u, my + ty * u, z + 0.03, 0.05, 0.04, ch - 0.06, face, 0.01)
    n = max(4, int(h / 0.25))
    run = slot_len * 0.85
    for i in range(n):
        y = y0 + run * (i + 0.5) / n
        P.cube(shade(color, -0.04 * (i % 2)), cx, y, 0.12, slot_w, run / n, h * (1 - (i + 1) / n) + 0.02)
    P.cube(shade(color, -0.1), cx, ye - slot_len * 0.075, 0.12, slot_w, slot_len * 0.15, 0.02)
    # the entrance at the foot of the stair
    if door == "dark":
        fbox(P, DARK, cx, ye, 0.12, slot_w * 0.55, 0.1, min(h, 1.9), "S", 0.02)
        fbox(P, shade(color, 0.08), cx, ye, 0.12 + min(h, 1.9), slot_w * 0.8, 0.3, 0.35, "S", 0.1)


def kaleb_tombs():
    """The two tombs on the ridge north-east of the town traditionally of Kaleb and his son Gebre Meskel:
    a terrace with two raised blocks of fine granite masonry, each opened by a stair down to its chambers."""
    m = Model("kaleb-tombs")
    g, a, b = Parts("kt_ground"), Parts("kt_tombs"), Parts("kt_top")
    r = rnd(61)
    g.cube(EARTH, 0, 0, 0, 50, 36, 0.12)
    g.cube(STONE, 0, 1, 0.12, 46, 30, 0.5)
    for k in range(5):
        g.cube(shade(STONE, -0.05), -18.4 + k * 9.2, -14.2, 0.12, 8.8, 0.6, 0.7)
    # Kaleb (west) and Gebre Meskel (east)
    a.xf = lambda v: (v[0], v[1], v[2] + 0.5)
    tomb_block(a, -11, 1, 16, 18, 1.6, 2.4, 9)
    tomb_block(a, 11, 2, 15, 20, 1.6, 2.4, 8)
    a.xf = None
    # remains above Gebre Meskel's tomb: column bases and wall stubs of a lost superstructure
    for i in range(3):
        for j in range(2):
            b.cube(DRESSED, 6.5 + i * 4.5, 6 + j * 5, 2.22, 0.9, 0.9, 0.5)
            b.cone(shade(DRESSED, 0.04), 6.5 + i * 4.5, 6 + j * 5, 2.72, 0.32, 0.3, r(0.3, 1.6), 8)
    b.cube(STONE, 11, 12.2, 2.22, 14, 0.8, 0.9)
    rubble(b, 0, -10, 40, 6, 24, r, STONE, 0.12)
    for k in range(4):
        tree(b, r(-22, 22), r(10, 16), r(3, 5), r(1.2, 2), shade(JUNIPER, r(-0.04, 0.06)))
    m.add(0, g.build(), "terrace")
    m.add(1, a.build(), "tombs")
    m.add(2, b.build(), "remains")
    return m


def tomb_false_door():
    """The Tomb of the False Door: a stairwell going down past a granite slab carved as a door with its frame,
    beam ends and lock, into the chamber of a probably 4th-century royal tomb. The superstructure is lost."""
    m = Model("tomb-false-door")
    g, a, b = Parts("fd_ground"), Parts("fd_tomb"), Parts("fd_door")
    r = rnd(71)
    g.cube(EARTH, 0, 0, 0, 24, 20, 0.12)
    tomb_block(a, 0, 1, 16, 14, 1.6, 4.6, 9, DRESSED, door="none")
    # the false door slab facing up the stair: a monolith carved like a wooden door in its frame, with beam ends
    y = 1 - 7 + 9
    b.cube(STELE_C, 0, y + 0.3, 0.12, 4.2, 0.6, 3.4)
    b.cube(shade(STELE_C, 0.04), 0, y + 0.3, 3.52, 4.5, 0.8, 0.25)
    framed_opening(b, 0, y, 0.7, 1.5, 2.1, "S", 0.0, 0.2)
    b.cube(shade(STELE_C, -0.2), 0, y - 0.06, 0.7, 1.5, 0.06, 2.1)
    for zz in (0.5, 3.1):
        fbox(b, shade(STELE_C, -0.1), 0, y, zz, 4.2, 0.1, 0.16, "S", 0.05)
        for i in range(9):
            b.disc(shade(STELE_C, 0.06), -1.9 + i * 0.475, y - 0.05, zz + 0.08, 0.08, 0.12, "S", 8)
    b.disc(BRONZE_C, 0.4, y - 0.1, 1.7, 0.1, 0.1, "S", 8)
    rubble(b, 0, -7.5, 20, 3, 12, r, DRESSED, 0.12)
    m.add(0, g.build(), "ground")
    m.add(1, a.build(), "tomb")
    m.add(2, b.build(), "false door")
    return m


# ---------------------------------------------------------------- Mai Shum

def mai_shum():
    """The Mai Shum reservoir: a basin cut in the rock at the foot of Mai Qoqo, held by a wall on the south,
    with flights of steps down to the water on the south and west."""
    m = Model("mai-shum")
    g, a, b = Parts("ms_ground"), Parts("ms_rock"), Parts("ms_steps")
    r = rnd(81)
    g.cube(EARTH, 0, 0, 0, 56, 40, 0.12)
    bw, bd = 40, 26
    g.cube(WATER_C, 0, 1, 0.12, bw, bd, 0.45)
    rim = 1.7
    # rock all round the basin, higher on the hill side (north and east)
    for face in "NSEW":
        (mx, my), L, (nx, ny), (tx, ty) = face_line(0, 1, bw, bd, face)
        n = int(L / 2.2)
        for i in range(n + 1):
            u = -L / 2 + L * i / n
            hh = rim * (1.5 if face in "NE" else 1.0) * r(0.8, 1.1)
            depth = r(3, 5)
            fbox(a, shade(ROCK, r(-0.06, 0.05)), mx + tx * u, my + ty * u, 0.12, 2.6, depth, hh, face, depth / 2)
    # the dam wall on the south, of laid stone
    a.cube(STONE, 0, 1 - bd / 2 - 1.2, 0.12, bw * 0.7, 1.6, rim + 0.2)
    for k in range(int(bw * 0.7 / 1.4)):
        fbox(a, shade(STONE, -0.08 * (k % 2)), -bw * 0.35 + 0.7 + k * 1.4, 1 - bd / 2 - 2.0, 0.12 + (k % 3) * 0.55, 1.3, 0.1, 0.5, "S", 0.0)
    # steps down to the water: on the dam (south) and the west side
    for i in range(6):
        b.cube(shade(DRESSED, -0.04 * (i % 2)), 0, 1 - bd / 2 + 0.6 * i + 0.3, 0.12, 10, 0.6, rim + 0.2 - (i + 1) * (rim - 0.3) / 6)
        b.cube(shade(DRESSED, -0.04 * (i % 2)), -bw / 2 + 0.55 * i + 0.3, 6, 0.12, 0.55, 5, rim - (i + 1) * (rim - 0.3) / 6)
    # women's water jars on the steps, a stone trough
    for k in range(5):
        b.cone("#9C5E3C", -3 + k * 1.4, 1 - bd / 2 - 0.6, rim + 0.32, 0.22, 0.12, 0.5, 8)
    b.cube(STONE, 8, -bd / 2 - 3.5, 0.12, 3.4, 1.0, 0.6)
    b.cube(WATER_C, 8, -bd / 2 - 3.5, 0.72, 3.0, 0.7, 0.02)
    for x, y in ((-25.5, 17.5), (25.5, 16.5), (-25, -17.5), (24, -15)):
        tree(b, x, y, r(4, 6), r(1.5, 2.2), shade(JUNIPER, r(-0.04, 0.06)))
    for k in range(60):
        ang = r(0, math.tau)
        x, y = 23.5 * math.cos(ang), 1 + 16.5 * math.sin(ang)
        a.rcube(shade(ROCK, r(-0.08, 0.04)), x, y, 0.12, r(0.6, 1.6), r(0.5, 1.2), r(0.4, 1.4), r(0, 3))
    m.add(0, g.build(), "basin")
    m.add(1, a.build(), "rock")
    m.add(2, b.build(), "steps")
    return m


# ---------------------------------------------------------------- the church of Mary of Zion

def battlements(P, cx, cy, w, d, z, color, size=0.7, gap=0.7):
    for face in "NSEW":
        (mx, my), L, (nx, ny), (tx, ty) = face_line(cx, cy, w, d, face)
        n = int(L / (size + gap))
        for i in range(n):
            u = -L / 2 + (size + gap) * (i + 0.5) + (L - n * (size + gap)) / 2
            fbox(P, color, mx + tx * u, my + ty * u, z, size, size * 0.7, size * 1.1, face, -size * 0.35)


def enclosure(P, w, d, h, t, color, gate_w=5.0, merlon=False, towers=0.0, gate_h=None):
    """A rectangular precinct wall with a gate in the south side."""
    for face in "NEW":
        (mx, my), L, _, _ = face_line(0, 0, w - t, d - t, face)
        fbox(P, color, mx, my, 0.12, L + t, t, h, face, 0.0)
    for s in (-1, 1):
        L = (w - gate_w) / 2
        P.cube(color, s * (gate_w / 2 + L / 2), -d / 2 + t / 2, 0.12, L, t, h)
    if merlon:
        battlements(P, 0, 0, w, d, 0.12 + h, shade(color, 0.03), 0.6, 0.6)
    gh = gate_h or h + 2.0
    for s in (-1, 1):
        P.cube(shade(color, 0.04), s * (gate_w / 2 + 1.0), -d / 2 + t / 2, 0.12, 2.0, t + 1.2, gh)
    P.cube(shade(color, 0.04), 0, -d / 2 + t / 2, 0.12 + gh - 1.2, gate_w + 4, t + 1.2, 1.2)
    fbox(P, DARK, 0, -d / 2, 0.12, gate_w - 0.6, 0.2, gh - 1.4, "S", 0.0)
    if towers:
        for sx in (-1, 1):
            for sy in (-1, 1):
                P.cone(shade(color, 0.03), sx * (w / 2 - t / 2), sy * (d / 2 - t / 2), 0.12, towers, towers, h + 1.8, 14)
                P.dome(shade(color, 0.06), sx * (w / 2 - t / 2), sy * (d / 2 - t / 2), 0.12 + h + 1.8, towers, 0.9, 14, 4)


def church_podium(P, w, d, h, cy=0.0):
    podium(P, 0, cy, w, d, h, tiers=2, color=DRESSED, step=1.2)
    P.cube(shade(DRESSED, 0.05), 0, cy, h - 0.02, w - 2.4 - 0.15, d - 2.4 - 0.15, 0.04)
    stairs(P, 0, cy - d / 2, w * 0.45, h, h * 2.0, "S", DRESSED)


def mary_of_zion(variant="1665"):
    """Mary of Zion, built long-side north-south here (entrance -Y); the landmark rotation turns the entrance west.
    1665: Fasilides' battlemented church on the old Aksumite podium, inside a battlemented precinct.
    aksumite: the first basilica on its podium, monkey-head walls. 1500: the great five-aisled church Alvares saw."""
    m = Model("mary-of-zion")
    g, a, b, c = Parts("mz_ground"), Parts("mz_walls"), Parts("mz_church"), Parts("mz_roofs")
    r = rnd(91)
    W, D = 90, 100
    g.cube(EARTH, 0, 0, 0, W, D, 0.12)
    g.cube(shade(DRESSED, -0.08), 0, -4, 0.12, 50, 70, 0.04)
    ph = 2.6
    church_podium(g, 40, 58, ph, cy=2)
    if variant == "1665":
        enclosure(a, 86, 96, 4.2, 1.2, STONE, 6.0, merlon=True, towers=2.4)
        # the church: a rectangular stone block with battlements, round corner turrets with domes, an arcaded porch
        cw, cd, ch = 18, 30, 9.5
        cy = 4
        b.cube(STONE_DK, 0, cy, ph, cw, cd, ch)
        b.cube(shade(STONE_DK, 0.05), 0, cy, ph + ch, cw + 0.4, cd + 0.4, 0.4)
        battlements(b, 0, cy, cw + 0.4, cd + 0.4, ph + ch + 0.4, shade(STONE_DK, 0.05), 0.7, 0.7)
        for sx in (-1, 1):
            for sy in (-1, 1):
                b.cone(shade(STONE_DK, 0.04), sx * cw / 2, cy + sy * cd / 2, ph, 1.6, 1.5, ch + 2.4, 14)
                c.dome(shade(STONE_DK, 0.1), sx * cw / 2, cy + sy * cd / 2, ph + ch + 2.4, 1.5, 1.0, 14, 5)
            # arched windows down the long sides
            for k in range(5):
                y = cy - cd / 2 + 4 + k * (cd - 8) / 4
                face = "E" if sx > 0 else "W"
                for zz in (ph + 2.0, ph + 6.0):
                    fbox(b, DARK, sx * cw / 2, y, zz, 1.0, 0.1, 1.6, face, 0.03)
                    b.disc(DARK, sx * (cw / 2 + 0.01), y, zz + 1.6, 0.5, 0.1, face, 8)
        # porch on the entrance front
        b.cube(shade(STONE_DK, 0.03), 0, cy - cd / 2 - 2.0, ph, 12, 4, 5.2)
        for k in range(3):
            fbox(b, DARK, -4 + k * 4, cy - cd / 2 - 4, ph, 2.2, 0.1, 3.0, "S", 0.03)
            b.disc(DARK, -4 + k * 4, cy - cd / 2 - 4.03, ph + 3.0, 1.1, 0.1, "S", 10)
        battlements(b, 0, cy - cd / 2 - 2.0, 12, 4, ph + 5.2, shade(STONE_DK, 0.05), 0.6, 0.6)
        # a raised lantern over the sanctuary at the far end
        c.cube(shade(STONE_DK, 0.06), 0, cy + cd / 2 - 6, ph + ch, 6, 6, 2.2)
        c.dome(shade(STONE_DK, 0.1), 0, cy + cd / 2 - 6, ph + ch + 2.2, 3.0, 0.8, 14, 5)
        c.cone(GOLD_C, 0, cy + cd / 2 - 6, ph + ch + 4.6, 0.12, 0.08, 1.4, 6)
        c.cube(GOLD_C, 0, cy + cd / 2 - 6, ph + ch + 5.5, 1.0, 0.12, 0.12)
        # clergy houses along the precinct wall and juniper trees in the churchyard
        for k in range(6):
            flat_house(a, -38 + 2.4, -30 + k * 11, 4.2, 7, 3.0, STONE, "E")
            flat_house(a, 38 - 2.4, -30 + k * 11, 4.2, 7, 3.0, STONE, "W")
        for k in range(14):
            x = r(-40, 40)
            y = r(-44, 44)
            if abs(x) < 23 and abs(y - 2) < 33:
                continue
            tree(c, x, y, r(5, 8), r(1.6, 2.6), shade(JUNIPER, r(-0.05, 0.06)))
    elif variant == "aksumite":
        # a low precinct wall, the basilica in monkey-head masonry: tall nave, lower aisles, a porch
        enclosure(a, 86, 96, 2.6, 1.0, STONE, 6.0, gate_h=4.0)
        cy = 3
        monkey_wall(b, 0, cy, 26, 46, 6.0, ph, STONE, bay=3.4, windows=(2.6,), door="S")
        monkey_wall(c, 0, cy, 10, 44, 4.2, ph + 6.3, STONE_LT, bay=3.0, windows=(1.4,), faces="EW")
        monkey_wall(b, 0, cy - 23 - 3, 12, 6, 4.4, ph, STONE, bay=3.0, door="S", faces="SEW")
        for k in range(8):
            y = -38 + k * 10.5
            flat_house(a, -36.5, y, r(5, 7), r(5, 8), r(2.8, 3.6), STONE, "E")
            flat_house(a, 36.5, y, r(5, 7), r(5, 8), r(2.8, 3.6), STONE, "W")
        for x, y in ((-26, 34), (26, 36), (-27, -36), (27, -38), (0, 40)):
            tree(a, x, y, r(5, 7), r(1.6, 2.2), shade(JUNIPER, r(-0.04, 0.06)))
    else:
        # c. 1500: the high open-roofed circuit round the church, the great enclosure like a town wall,
        # the two rectors' mansions and the houses of canons and monks
        enclosure(a, 86, 96, 4.6, 1.4, STONE, 6.0, merlon=False, gate_h=7.0)
        a.xf = lambda v: (v[0], v[1] + 2, v[2] + ph - 0.12)
        enclosure(a, 38, 56, 4.0, 0.8, STONE_LT, 4.0, gate_h=5.4)
        a.xf = None
        cy = 4
        b.cube(PLAST, 0, cy, ph, 30, 44, 6.2)
        b.cube(shade(PLAST, 0.04), 0, cy, ph + 6.2, 18, 42, 3.4)
        b.cube(shade(PLAST, 0.06), 0, cy, ph + 9.6, 8, 40, 2.4)
        for s in (-1, 1):
            for k in range(8):
                y = cy - 18 + k * 5
                fbox(b, DARK, s * 15, y, ph + 2.2, 0.9, 0.1, 1.8, "E" if s > 0 else "W", 0.03)
                b.disc(DARK, s * 15.01, y, ph + 4.0, 0.45, 0.1, "E" if s > 0 else "W", 8)
                fbox(b, DARK, s * 9, y, ph + 7.4, 0.8, 0.1, 1.3, "E" if s > 0 else "W", 0.03)
        fbox(b, DARK, 0, cy - 22, ph, 3.0, 0.1, 4.0, "S", 0.03)
        b.disc(DARK, 0, cy - 22.03, ph + 4.0, 1.5, 0.1, "S", 10)
        c.cone(GOLD_C, 0, cy + 16, ph + 12.0, 0.12, 0.08, 1.4, 6)
        c.cube(GOLD_C, 0, cy + 16, ph + 12.9, 1.0, 0.12, 0.12)
        for s in (-1, 1):
            monkey_wall(c, s * 31, -30, 12, 10, 5.0, 0.12, STONE, bay=3.0, windows=(2.6,), door="S")
        for k in range(16):
            x = r(-40, 40)
            y = r(-44, 44)
            if abs(x) < 23 and abs(y - 2) < 31:
                continue
            if abs(x) > 24 and y < -24:
                continue
            round_hut(c, x, y, r(2.0, 2.8), 2.0, STONE, THATCH_C, "S" if y > 0 else "N")
        for k in range(8):
            x, y = r(-40, 40), r(-44, 44)
            if abs(x) < 23 and abs(y - 2) < 31:
                continue
            tree(c, x, y, r(5, 8), r(1.6, 2.4), shade(JUNIPER, r(-0.05, 0.06)))
    m.add(0, g.build(), "podium")
    m.add(1, a.build(), "precinct")
    m.add(2, b.build(), "church")
    m.add(3, c.build(), "roofs")
    return m


# ---------------------------------------------------------------- inscriptions and thrones

def inscribed_slab(P, x, y, w, h, t, color=STELE_C, face="S", lines=10, z0=0.0):
    nx, ny = FACES[face]
    if nx == 0:
        P.cube(color, x, y, z0, w, t, h)
    else:
        P.cube(color, x, y, z0, t, w, h)
    for f in ((face, "N" if face == "S" else "S") if nx == 0 else (face, "W" if face == "E" else "E")):
        fx, fy = FACES[f]
        for k in range(lines):
            z = z0 + h * 0.12 + k * h * 0.76 / lines
            fbox(P, shade(color, -0.28), x + fx * t / 2, y + fy * t / 2, z, w * 0.82, 0.03, h * 0.025, f, 0.0)


def ezana_stone():
    """The Ezana Stone: a granite slab recording King Ezana's wars and his new faith in Ge'ez, Sabaic and Greek."""
    m = Model("ezana-stone")
    g, a = Parts("ez_ground"), Parts("ez_stone")
    r = rnd(101)
    g.cube(EARTH, 0, 0, 0, 6, 5, 0.12)
    g.cube(DRESSED, 0, 0, 0.12, 3.2, 1.8, 0.3)
    inscribed_slab(a, 0, 0, 1.9, 2.3, 0.4, STELE_C, "S", 26, 0.42)
    half_head(a, 0, 0, 2.72, 0.95, 0.4, STELE_C, 10)
    for k in range(22):
        ang = math.tau * k / 22
        a.rcube(shade(STONE, r(-0.06, 0.04)), 2.5 * math.cos(ang), 2.0 * math.sin(ang), 0.12, r(0.35, 0.55), r(0.3, 0.45), r(0.25, 0.45), ang)
    m.add(0, g.build(), "base")
    m.add(1, a.build(), "stone")
    return m


def throne(P, x, y, s=1.0, broken=False, slab=False, r=None):
    P.cube(shade(DRESSED, -0.05), x, y, 0.12, 2.6 * s, 2.6 * s, 0.45 * s)
    P.cube(shade(DRESSED, -0.1), x, y, 0.12 + 0.3 * s, 2.7 * s, 2.7 * s, 0.08 * s)
    P.cube(DRESSED, x, y, 0.12 + 0.45 * s, 2.0 * s, 2.0 * s, 0.35 * s)
    P.cube(shade(DRESSED, 0.05), x, y, 0.12 + 0.72 * s, 2.1 * s, 2.1 * s, 0.08 * s)
    for i in range(3):
        P.cube(shade(DRESSED, -0.04 * (i % 2)), x, y - 1.3 * s - 0.25 - 0.5 * i, 0.12, 1.4 * s, 0.5, 0.45 * s * (3 - i) / 3)
    z = 0.12 + 0.8 * s
    # the four holes for the legs of the lost metal-clad seat
    for sx in (-1, 1):
        for sy in (-1, 1):
            P.cube(DARK, x + sx * 0.6 * s, y + sy * 0.6 * s, z, 0.25 * s, 0.25 * s, 0.02)
    if not broken:
        P.cube(STELE_C, x, y + 0.1 * s, z, 1.3 * s, 1.1 * s, 0.55 * s)
        P.cube(STELE_C, x, y + 0.6 * s, z, 1.3 * s, 0.25 * s, 1.5 * s)
        for sx in (-1, 1):
            P.cube(STELE_C, x + sx * 0.6 * s, y + 0.05 * s, z + 0.55 * s, 0.18 * s, 1.0 * s, 0.4 * s)
    if slab:
        inscribed_slab(P, x, y + 1.6 * s, 1.6 * s, 2.2 * s, 0.3 * s, STELE_C, "S", 9, 0.12)


def coronation_thrones(variant="aksumite"):
    """Granite throne bases in a row: the Aksumite kings' victory thrones, later used as the seats of the
    coronation, with the king's stone in the middle."""
    m = Model("coronation-thrones")
    g, a = Parts("ct_ground"), Parts("ct_thrones")
    r = rnd(111)
    g.cube(EARTH, 0, 0, 0, 40, 10, 0.12)
    g.cube(shade(DRESSED, -0.06), 0, 0, 0.12, 38, 6, 0.05)
    for i in range(19):
        for j in range(3):
            g.cube(shade(DRESSED, -0.03 * ((i + j) % 3) - 0.04), -18 + i * 2.0, -2 + j * 2.0, 0.17, 1.92, 1.92, 0.04)
    xs = [-16, -11.5, -7, 0, 7, 11.5, 16]
    for k, x in enumerate(xs):
        if x == 0:
            throne(a, x, 0.3, 1.35, broken=False, slab=True)
        else:
            throne(a, x, 0.4, 1.0, broken=(k in (0, 5)), slab=(k in (2, 4)))
    for k in range(6):
        a.rcube(shade(DRESSED, r(-0.06, 0.04)), r(-19, 19), r(-4.5, -3.2), 0.12, r(0.3, 0.7), r(0.3, 0.6), r(0.2, 0.4), r(0, 3))
    m.add(0, g.build(), "ground")
    m.add(1, a.build(), "thrones")
    return m


# ---------------------------------------------------------------- Beta Giyorgis

def beta_giyorgis():
    """The hilltop settlement on Beta Giyorgis: stone houses on terraces, cattle pens and the elite cemetery
    with its rough stelae."""
    m = Model("beta-giyorgis")
    g, a, b = Parts("bg_ground"), Parts("bg_houses"), Parts("bg_stelae")
    r = rnd(121)
    g.cube(EARTH, 0, 0, 0, 90, 70, 0.12)
    g.cube(GRASS, 0, 0, 0.12, 86, 66, 0.04)
    # terrace walls running across the slope
    for k, y in enumerate((-24, -10, 6)):
        g.cube(STONE, -6, y, 0.12, 70 - k * 6, 1.0, 1.0)
    for i in range(5):
        for j in range(4):
            if r() < 0.2:
                continue
            x, y = -36 + i * 12 + r(-1.5, 1.5), -29 + j * 13.5 + r(-1, 1)
            w, d = r(4.5, 7), r(4, 6)
            col = shade(STONE, r(-0.06, 0.04))
            flat_house(a, x, y + 1.5, w, d, r(2.4, 3.2), col, "S")
            # a walled yard in front, a granary, a grinding stone
            for side in (-1, 1):
                a.cube(STONE_DK, x + side * (w / 2 + 0.6), y - 2.0, 0.12, 0.5, 4.2, 1.0)
            a.cube(STONE_DK, x - w / 4 - 0.6, y - 4.0, 0.12, w / 2, 0.5, 1.0)
            a.cone(THATCH_C, x + w / 2 - 0.6, y - 2.6, 0.12, 0.8, 0.8, 1.2, 10)
            a.cone(THATCH_C, x + w / 2 - 0.6, y - 2.6, 1.32, 1.0, 0.05, 0.9, 10)
    for k in range(4):
        x, y = r(-36, 18), r(-28, 18)
        rr = r(3, 5)
        for i in range(14):
            ang = math.tau * i / 14
            a.rcube(STONE_DK, x + rr * math.cos(ang), y + rr * math.sin(ang), 0.12, 1.4, 0.6, 0.9, ang + math.pi / 2)
    # the cemetery on the north-east of the hilltop
    for k in range(40):
        x, y = r(26, 43), r(-14, 32)
        p = Parts("tmp")
        rough_stele(p, 0, 0, r(1.2, 4.0), r(0.4, 0.8), r(0.3, 0.5), r, (r(-0.06, 0.06), r(-0.06, 0.06)))
        for col, (vs, fs) in p.g.items():
            b.poly(col, [(vx + x, vy + y, vz + 0.16) for vx, vy, vz in vs], fs)
    for k in range(6):
        b.cone(STONE, r(26, 42), r(-10, 30), 0.12, r(1.2, 1.8), 0.3, r(0.5, 0.9), 9)
    m.add(0, g.build(), "terraces")
    m.add(1, a.build(), "houses")
    m.add(2, b.build(), "stelae")
    return m


BUILDERS = {
    "aksum/great-stele": lambda: great_stele("standing"),
    "aksum/great-stele-fallen": lambda: great_stele("fallen"),
    "aksum/ezana-stele": ezana_stele,
    "aksum/rome-stele": lambda: rome_stele("standing"),
    "aksum/rome-stele-fallen": lambda: rome_stele("fallen"),
    "aksum/northern-stelae": lambda: northern_stelae("full"),
    "aksum/northern-stelae-early": lambda: northern_stelae("early"),
    "aksum/gudit-stelae": gudit_stelae,
    "aksum/dungur": lambda: dungur("full"),
    "aksum/dungur-ruin": lambda: dungur("ruin"),
    "aksum/taakha-maryam": lambda: taakha_maryam("full"),
    "aksum/taakha-maryam-ruin": lambda: taakha_maryam("ruin"),
    "aksum/kaleb-tombs": kaleb_tombs,
    "aksum/tomb-false-door": tomb_false_door,
    "aksum/mai-shum": mai_shum,
    "aksum/mary-of-zion": lambda: mary_of_zion("1665"),
    "aksum/mary-of-zion-aksumite": lambda: mary_of_zion("aksumite"),
    "aksum/mary-of-zion-1500": lambda: mary_of_zion("1500"),
    "aksum/ezana-stone": ezana_stone,
    "aksum/coronation-thrones": coronation_thrones,
    "aksum/beta-giyorgis": beta_giyorgis,
}
