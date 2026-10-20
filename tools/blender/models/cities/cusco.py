"""Cusco / Qusqu landmark miniatures: Inca kancha and temples of fitted stone under steep ichu thatch,
the zigzag terraces of Sacsayhuamán, and the Spanish baroque churches raised on Inca walls.
Builders face south (-Y); the landmark rotation turns them on the map.

Most geometry goes through Acc, an accumulator that collects boxes and prisms per colour and makes
one mesh per colour, so walls can carry thousands of individually shaped stones cheaply."""
import math
import random
from chronokit import Model, box, cylinder, dome, join, shade, mesh_from
from worldkit import *

# ---------------------------------------------------------------- palette
AND = "#7A786D"          # grey andesite of the temples and palaces
DIOR = "#6A7263"         # green diorite of Hatun Rumiyoc
LIME = "#ADA593"         # grey limestone of Sacsayhuamán
FIELD = "#978A72"        # fieldstone set in clay
CLAYW = "#B49C78"        # clay-plastered walls
RED_PL = "#9C4F3B"       # red plaster
ICHU = "#B59B5C"         # ichu-grass thatch
SAND = "#D8C79E"
PAVE = "#C9BEA4"
EARTH = "#A58F68"
GRASS = "#8C9A64"
MAIZE = "#7E9550"
GOLD = GILT
CANT = "#8F7266"         # reddish andesite of the colonial churches
CANT_L = "#A88E80"
WHITE = "#ECE5D4"
TILE = "#A65A3E"
WOOD = "#5E4332"
DOMEC = "#CFC2A8"
WATERC = "#5F878C"
CLOTH = "#E9DFC8"

BOX_F = [(3, 2, 1, 0), (4, 5, 6, 7), (0, 1, 5, 4), (1, 2, 6, 5), (2, 3, 7, 6), (3, 0, 4, 7)]


def tones(c, k=0.07):
    return [c, shade(c, k), shade(c, -k)]


# ---------------------------------------------------------------- accumulator

class Acc:
    """Collects geometry per colour under a stack of 2D placements; build() makes one joined object."""

    def __init__(self, name):
        self.name = name
        self.g = {}
        self.T = [(0.0, 0.0, 0.0)]

    def push(self, x=0.0, y=0.0, deg=0.0):
        ox, oy, oa = self.T[-1]
        c, s = math.cos(oa), math.sin(oa)
        self.T.append((ox + x * c - y * s, oy + x * s + y * c, oa + math.radians(deg)))

    def pop(self):
        self.T.pop()

    def add(self, color, verts, faces):
        ox, oy, oa = self.T[-1]
        c, s = math.cos(oa), math.sin(oa)
        vs, fs = self.g.setdefault(color, ([], []))
        o = len(vs)
        vs.extend((ox + x * c - y * s, oy + x * s + y * c, z) for x, y, z in verts)
        fs.extend(tuple(i + o for i in f) for f in faces)

    def box(self, color, x, y, z, w, d, h, ang=0.0, tw=None, td=None):
        tw = w if tw is None else tw
        td = d if td is None else td
        c, s = math.cos(ang), math.sin(ang)
        loc = [(-w / 2, -d / 2, 0), (w / 2, -d / 2, 0), (w / 2, d / 2, 0), (-w / 2, d / 2, 0),
               (-tw / 2, -td / 2, h), (tw / 2, -td / 2, h), (tw / 2, td / 2, h), (-tw / 2, td / 2, h)]
        self.add(color, [(x + px * c - py * s, y + px * s + py * c, z + pz) for px, py, pz in loc], BOX_F)

    def seg(self, color, a, b, z, t, h, tt=None, ext=0.0):
        """A wall-like (optionally battered) box from a to b."""
        (ax, ay), (bx, by) = a, b
        L = math.hypot(bx - ax, by - ay)
        ang = math.atan2(by - ay, bx - ax)
        self.box(color, (ax + bx) / 2, (ay + by) / 2, z, L + ext, t, h, ang, L + ext, t if tt is None else tt)

    def prism(self, color, pts, z, h, top=None):
        n = len(pts)
        top = top or pts
        verts = [(x, y, z) for x, y in pts] + [(x, y, z + h) for x, y in top]
        faces = [tuple(range(n))[::-1], tuple(range(n, 2 * n))] + [(i, (i + 1) % n, n + (i + 1) % n, n + i) for i in range(n)]
        self.add(color, verts, faces)

    def lathe(self, color, x, y, z, prof, n=16):
        verts, faces = [], []
        prof = [(max(r, 0.01), zz) for r, zz in prof]
        for r, zz in prof:
            for i in range(n):
                a = math.tau * i / n
                verts.append((x + r * math.cos(a), y + r * math.sin(a), z + zz))
        m = len(prof)
        for k in range(m - 1):
            for i in range(n):
                j = (i + 1) % n
                faces.append((k * n + i, k * n + j, (k + 1) * n + j, (k + 1) * n + i))
        faces.append(tuple(range(n))[::-1])
        faces.append(tuple(range((m - 1) * n, m * n)))
        self.add(color, verts, faces)

    def cyl(self, color, x, y, z, r, h, n=16, rt=None):
        self.lathe(color, x, y, z, [(r, 0), (r if rt is None else rt, h)], n)

    def ring(self, color, x, y, z, r0, r1, h, n=32):
        verts, faces = [], []
        for zz in (0, h):
            for r in (r1, r0):
                for i in range(n):
                    a = math.tau * i / n
                    verts.append((x + r * math.cos(a), y + r * math.sin(a), z + zz))
        for i in range(n):
            j = (i + 1) % n
            O0, I0, O1, I1 = 0, n, 2 * n, 3 * n
            faces += [(O0 + i, O0 + j, O1 + j, O1 + i), (I0 + j, I0 + i, I1 + i, I1 + j), (O1 + i, O1 + j, I1 + j, I1 + i), (O0 + j, O0 + i, I0 + i, I0 + j)]
        self.add(color, verts, faces)

    def roof(self, color, x, y, z, L, W, h, axis="x", over=0.5, hip=0.0, eave=0.35, ridge=True):
        """Thatch or tile roof: an eave slab and a gable (hip=0) or hipped (hip = ridge inset) solid; ridge along axis."""
        a, b = L / 2 + over, W / 2 + over
        hp = min(hip, a - 0.2)
        loc = [(-a, -b, 0), (a, -b, 0), (a, b, 0), (-a, b, 0), (-a + hp, 0, h), (a - hp, 0, h)]
        faces = [(3, 2, 1, 0), (0, 1, 5, 4), (2, 3, 4, 5), (1, 2, 5), (3, 0, 4)]
        if axis == "x":
            vs = [(x + u, y + v, z + eave + w) for u, v, w in loc]
            self.box(shade(color, -0.12), x, y, z, 2 * a, 2 * b, eave)
        else:
            vs = [(x + v, y + u, z + eave + w) for u, v, w in loc]
            self.box(shade(color, -0.12), x, y, z, 2 * b, 2 * a, eave)
        self.add(color, vs, faces)
        if ridge:
            rl = 2 * (a - hp) + 0.4
            if axis == "x":
                self.box(shade(color, -0.22), x, y, z + eave + h - 0.25, rl, 0.55, 0.45)
            else:
                self.box(shade(color, -0.22), x, y, z + eave + h - 0.25, 0.55, rl, 0.45)

    def gable_end(self, color, x, y, z, W, h, axis="x", t=0.7):
        """A triangular stone gable wall across a building whose ridge runs along axis, centred at (x, y)."""
        if axis == "x":
            vs = [(x - t / 2, y - W / 2, z), (x - t / 2, y + W / 2, z), (x - t / 2, y, z + h), (x + t / 2, y - W / 2, z), (x + t / 2, y + W / 2, z), (x + t / 2, y, z + h)]
        else:
            vs = [(x - W / 2, y - t / 2, z), (x + W / 2, y - t / 2, z), (x, y - t / 2, z + h), (x - W / 2, y + t / 2, z), (x + W / 2, y + t / 2, z), (x, y + t / 2, z + h)]
        self.add(color, vs, [(0, 1, 2), (5, 4, 3), (0, 3, 4, 1), (1, 4, 5, 2), (2, 5, 3, 0)])

    def panel(self, color, pts, x, y, z, face="S", depth=0.3):
        """A flat prism from an outline [(s, z), ...] on a wall facing S/N/E/W, centred on the wall plane at (x, y)."""
        n = len(pts)
        d = depth / 2
        if face in ("S", "N"):
            vs = [(x + s, y - d, z + zz) for s, zz in pts] + [(x + s, y + d, z + zz) for s, zz in pts]
        else:
            vs = [(x - d, y + s, z + zz) for s, zz in pts] + [(x + d, y + s, z + zz) for s, zz in pts]
        faces = [tuple(range(n)), tuple(range(2 * n - 1, n - 1, -1))] + [(i, (i + 1) % n, n + (i + 1) % n, n + i) for i in range(n)]
        self.add(color, vs, faces)

    def trap(self, color, x, y, z, w0, w1, h, face="S", depth=0.3):
        self.panel(color, [(-w0 / 2, 0), (w0 / 2, 0), (w1 / 2, h), (-w1 / 2, h)], x, y, z, face, depth)

    def arch(self, color, x, y, z, w, h, face="S", depth=0.3, seg=8):
        r = w / 2
        rect = max(0.0, h - r)
        pts = [(-r, 0), (r, 0)] + [(r * math.cos(math.pi * i / seg), rect + r * math.sin(math.pi * i / seg)) for i in range(seg + 1)] + [(-r, 0)]
        pts = pts[:-1]
        self.panel(color, pts, x, y, z, face, depth)

    def build(self):
        objs = [mesh_from(f"{self.name}_{i}", vs, fs, (0, 0, 0), c) for i, (c, (vs, fs)) in enumerate(self.g.items()) if fs]
        return join(objs, self.name) if objs else None


# ---------------------------------------------------------------- Inca masonry

def stone_face(acc, a, b, z0, h, off, colors, rnd, course=0.8, block=1.5, jit=0.3, cham=0.2, slope=0.0, proud=(0.05, 0.14), batter=0.0, skip=(), side=1, pillow=0.25):
    """Cover the face of a wall running a->b with individually cut stones. side=1 is the right-hand side of a->b.
    off: distance of the face from the wall's centre line at z0; batter: inward lean per metre of height.
    skip: [(t0, t1, ztop)] spans along the wall (from a) left bare for doors.
    slope > 0 tilts the top joints for polygonal masonry; cham chamfers the corners."""
    (ax, ay), (bx, by) = a, b
    L = math.hypot(bx - ax, by - ay)
    if L < 0.3:
        return
    tx, ty = (bx - ax) / L, (by - ay) / L
    nx, ny = side * ty, -side * tx

    def P(t, z, o):
        d = off - batter * (z - z0) + o
        return (ax + tx * t + nx * d, ay + ty * t + ny * d, z)

    z, row = z0, 0
    top = z0 + h
    while z < top - 0.08:
        ch = course * (1 + rnd.uniform(-jit, jit))
        if z + ch > top - course * 0.45:
            ch = top - z
        t = 0.0
        first = True
        while t < L - 0.05:
            if first and row % 2:
                bw = block * rnd.uniform(0.35, 0.75)
            else:
                bw = block * (1 + rnd.uniform(-jit, jit))
            first = False
            if t + bw > L - block * 0.35:
                bw = L - t
            t0, t1 = t, t + bw
            t = t1
            tc = (t0 + t1) / 2
            if any(s0 < tc < s1 and z < zt for s0, s1, zt in skip):
                continue
            g = 0.06
            za, zb = z + g, z + ch - g
            zl = zb - rnd.uniform(0, slope) * ch
            zr = zb - rnd.uniform(0, slope) * ch
            if slope:
                za += rnd.uniform(0, slope * 0.4) * ch
            c = cham * min(bw, ch)
            pts = []
            for (pt, pz, dt, dz) in ((t0 + g, za, 1, 1), (t1 - g, za, -1, 1), (t1 - g, zr, -1, -1), (t0 + g, zl, 1, -1)):
                cc = c * rnd.uniform(0.3, 1.0) if rnd.random() < 0.8 else 0.0
                if cc > 0.02:
                    if dz > 0:   # bottom corners: go along the bottom edge first, then up
                        pts += ([(pt, pz + cc), (pt + dt * cc, pz)] if dt < 0 else [(pt, pz + cc), (pt + dt * cc, pz)])
                    else:
                        pts += [(pt, pz - cc), (pt + dt * cc, pz)]
                else:
                    pts.append((pt, pz))
            # order the outline counter-clockwise around its centre (in t, z)
            cx = sum(p[0] for p in pts) / len(pts)
            cz = sum(p[1] for p in pts) / len(pts)
            pts.sort(key=lambda p: math.atan2(p[1] - cz, p[0] - cx))
            pr = rnd.uniform(*proud)
            k = pillow
            back = [P(pt, pz, -0.03) for pt, pz in pts]
            front = [P(cx + (pt - cx) * (1 - k * pr / max(0.3, min(bw, ch)) * 2), cz + (pz - cz) * (1 - k * pr / max(0.3, min(bw, ch)) * 2), pr) for pt, pz in pts]
            n = len(pts)
            faces = [tuple(range(n))[::-1], tuple(range(n, 2 * n))] + [(i, (i + 1) % n, n + (i + 1) % n, n + i) for i in range(n)]
            acc.add(rnd.choice(colors), back + front, faces)
        z += ch
        row += 1


def fitted_wall(acc, pts, z, h, t, color, rnd, faces=(1,), batter=0.04, course=0.8, block=1.5, jit=0.3, cham=0.2, slope=0.0, proud=(0.05, 0.14),
                closed=False, skips=None, joint=None, core=True):
    """A battered wall along a polyline with cut stones on the chosen sides (1 = right of travel, -1 = left)."""
    pts = list(pts) + ([pts[0]] if closed else [])
    cols = tones(color)
    for i in range(1, len(pts)):
        a, b = pts[i - 1], pts[i]
        if core:
            acc.seg(joint or shade(color, -0.38), a, b, z, t, h, t - 2 * batter * h, ext=t * 0.9)
        for s in faces:
            stone_face(acc, a, b, z, h, t / 2, cols, rnd, course, block, jit, cham, slope, proud, batter, (skips or {}).get(i, ()), side=s)


def inca_house(acc, x, y, z, L, W, h, axis="x", door_side=1, doors=2, stone=AND, roof=ICHU, rh=None, hip=0.0, niches=0, rnd=None, faced=False,
               jamb=None, door_w=1.2, gable=True, gold=None):
    """A one-room Inca building: battered walls, trapezoidal doors on one long side, stone gables, steep thatch."""
    b = 0.05
    rh = rh or W * 0.62
    if axis == "x":
        acc.box(stone, x, y, z, L, W, h, 0, L - 2 * b * h, W - 2 * b * h)
    else:
        acc.box(stone, x, y, z, W, L, h, 0, W - 2 * b * h, L - 2 * b * h)
    face = {("x", 1): "N", ("x", -1): "S", ("y", 1): "E", ("y", -1): "W"}[(axis, door_side)]
    dh = min(2.4, h * 0.62)
    spots = [(-L / 2 + L * (i + 0.5) / doors) for i in range(doors)]
    nspots = [(-L / 2 + L * (i + 1) / (doors + 1)) for i in range(doors)] if niches else []
    off = W / 2 - b * dh / 2 + 0.03
    for s in spots:
        px, py = (x + s, y + door_side * off) if axis == "x" else (x + door_side * off, y + s)
        if jamb:
            acc.trap(jamb, px, py, z, door_w * 1.45, door_w * 1.15, dh * 1.12, face, 0.42)
        acc.trap(DARK, px, py, z, door_w, door_w * 0.78, dh, face, 0.5)
    for s in nspots:
        for side in ((door_side, -door_side) if niches > 1 else (door_side,)):
            px, py = (x + s, y + side * off) if axis == "x" else (x + side * off, y + s)
            f = {("x", 1): "N", ("x", -1): "S", ("y", 1): "E", ("y", -1): "W"}[(axis, side)]
            acc.trap(shade(stone, -0.45), px, py, z + 1.0, 0.7, 0.55, 1.0, f, 0.4)
    if faced and rnd:
        if axis == "x":
            a, bb = (x - L / 2, y + door_side * W / 2), (x + L / 2, y + door_side * W / 2)
            sd = -door_side
        else:
            a, bb = (x + door_side * W / 2, y - L / 2), (x + door_side * W / 2, y + L / 2)
            sd = door_side
        sk = [(s + L / 2 - door_w, s + L / 2 + door_w, z + dh + 0.3) for s in spots]
        stone_face(acc, a, bb, z, h, 0.0, tones(stone), rnd, course=0.75, block=1.6, jit=0.25, cham=0.15, proud=(0.04, 0.1), batter=b, skip=sk, side=sd)
    if gold:
        if axis == "x":
            acc.box(gold, x, y, z + h * 0.8, L - 2 * b * h * 0.8 + 0.25, W - 2 * b * h * 0.8 + 0.25, 0.35)
        else:
            acc.box(gold, x, y, z + h * 0.8, W - 2 * b * h * 0.8 + 0.25, L - 2 * b * h * 0.8 + 0.25, 0.35)
    tw, tl = W - 2 * b * h, L - 2 * b * h
    if gable and not hip:
        for s in (-1, 1):
            if axis == "x":
                acc.gable_end(stone, x + s * (tl / 2 - 0.35), y, z + h, tw, rh * 0.92, "x")
            else:
                acc.gable_end(stone, x, y + s * (tl / 2 - 0.35), z + h, tw, rh * 0.92, "y")
    return (tl, tw, rh)


def inca_roof(acc, x, y, z, L, W, h, axis="x", rh=None, hip=0.0, roof=ICHU):
    b = 0.05
    rh = rh or W * 0.62
    tl, tw = L - 2 * b * h, W - 2 * b * h
    acc.roof(roof, x, y, z + h, tl, tw, rh, axis, over=0.55 if not hip else 0.7, hip=hip)
    if not hip:   # roof-tie pegs projecting from the gables
        for s in (-1, 1):
            for k in (0.3, 0.6):
                if axis == "x":
                    acc.box(shade(AND, -0.1), x + s * (tl / 2 + 0.1), y, z + h + rh * k, 0.5, 0.25, 0.25)
                else:
                    acc.box(shade(AND, -0.1), x, y + s * (tl / 2 + 0.1), z + h + rh * k, 0.25, 0.5, 0.25)


def kancha_c(A1, A2, cx, cy, W, D, rnd, stone=AND, wall_h=4.0, t=1.0, gate="S", gate_at=0.0, sides="NSEW", hw=6.0, hh=3.6, z=0.0,
             face_out=True, fine=True, court=SAND, frac=0.8, doors=2, jamb=None, roof=ICHU, block=1.4, course=0.75, slope=0.0, wall_color=None, inner=None):
    """A walled compound with one gate and a one-room house along each listed inner side, doors toward the court."""
    x0, x1, y0, y1 = cx - W / 2, cx + W / 2, cy - D / 2, cy + D / 2
    A1.box(court, cx, cy, z, W - 0.2, D - 0.2, 0.12)
    ring = [(x0, y0), (x1, y0), (x1, y1), (x0, y1)]
    # gate position along its side (from the side's start, counter-clockwise order S: x0->x1, E: y0->y1, N: x1->x0, W: y1->y0)
    sidx = {"S": 1, "E": 2, "N": 3, "W": 4}
    Ls = {"S": W, "E": D, "N": W, "W": D}
    skips = {}
    if gate:
        gt = Ls[gate] / 2 + gate_at
        skips[sidx[gate]] = [(gt - 1.8, gt + 1.8, z + 3.4)]
    fitted_wall(A1, ring, z, wall_h, t, wall_color or stone, rnd, faces=(1,) if face_out else (), closed=True, skips=skips,
                block=block, course=course, slope=slope, cham=0.25 if slope else 0.18, joint=shade(wall_color or stone, -0.3 if face_out else 0.0))
    if gate:
        gt = Ls[gate] / 2 + gate_at
        gx, gy, f = {"S": (x0 + gt, y0 - t / 2, "S"), "N": (x1 - gt, y1 + t / 2, "N"), "E": (x1 + t / 2, y0 + gt, "E"), "W": (x0 - t / 2, y1 - gt, "W")}[gate]
        A1.trap(jamb or shade(stone, -0.25), gx, gy, z, 3.0, 2.3, 3.4, f, 0.6)
        A1.trap(DARK, gx, gy, z, 2.1, 1.6, 3.0, f, 0.7)
    # houses
    inset = t / 2 + 0.6
    nsy = ("S" in sides) + ("N" in sides)
    for sd in sides:
        if sd in "SN":
            L = (W - 2 * inset) * frac
            yy = (y0 + inset + hw / 2) if sd == "S" else (y1 - inset - hw / 2)
            ds = 1 if sd == "S" else -1
            inca_house(A1, cx, yy, z, L, hw, hh, "x", ds, doors, stone if fine else CLAYW, rnd=rnd, jamb=jamb)
            inca_roof(A2, cx, yy, z, L, hw, hh, "x", roof=roof)
        else:
            avail = D - 2 * inset - (2 * hw + 2.0 if nsy else 0)
            L = avail * (frac if nsy else frac)
            xx = (x1 - inset - hw / 2) if sd == "E" else (x0 + inset + hw / 2)
            ds = -1 if sd == "E" else 1
            inca_house(A1, xx, cy, z, L, hw, hh, "y", ds, max(1, doors - 1), stone if fine else CLAYW, rnd=rnd, jamb=jamb)
            inca_roof(A2, xx, cy, z, L, hw, hh, "y", roof=roof)
    if inner:
        A1.box(inner, cx, cy, z, W - 2 * (inset + hw) - 1, D - 2 * (inset + hw) - 1, 0.18)


def great_hall(A1, A2, x, y, z, L, W, h, rnd, stone=AND, doors=6, door_side=-1, rh=None, faced=True, roof=ICHU, jamb=None):
    """A kallanka: a long hall with many doorways onto a plaza and a tall hipped thatched roof."""
    rh = rh or W * 0.7
    inca_house(A1, x, y, z, L, W, h, "x", door_side, doors, stone, rnd=rnd, faced=faced, gable=False, door_w=1.6, jamb=jamb)
    inca_roof(A2, x, y, z, L, W, h, "x", rh=rh, hip=W * 0.7, roof=roof)


def round_tower(A1, A2, x, y, z, r, h, rnd, stone=AND, roof=ICHU, rh=None, door="S"):
    A1.cyl(stone, x, y, z, r, h, 24, r * 0.95)
    for i in range(int(h / 0.8)):
        if i % 2:
            A1.ring(shade(stone, -0.12), x, y, z + i * 0.8, r - 0.1, r * (1 - 0.05 * i * 0.8 / h) + 0.04, 0.08, 24)
    dx, dy = {"S": (0, -r), "N": (0, r), "E": (r, 0), "W": (-r, 0)}[door]
    A1.trap(DARK, x + dx, y + dy, z, 1.3, 1.0, 2.4, door, 0.8)
    A2.lathe(shade(roof, -0.12), x, y, z + h, [(r * 1.08, 0), (r * 1.08, 0.4)], 24)
    A2.lathe(roof, x, y, z + h + 0.4, [(r * 1.08, 0), (r * 0.55, (rh or r * 1.6) * 0.6), (0.15, rh or r * 1.6)], 24)


def figure(acc, x, y, z, color, s=1.0):
    acc.cyl(color, x, y, z, 0.28 * s, 1.1 * s, 6, 0.2 * s)
    acc.cyl(shade(color, -0.1), x, y, z + 1.1 * s, 0.17 * s, 0.35 * s, 6, 0.12 * s)


def llama(acc, x, y, z, color, deg=0.0, s=1.0):
    acc.push(x, y, deg)
    acc.box(color, 0, 0, z + 0.75 * s, 1.1 * s, 0.42 * s, 0.5 * s)
    acc.box(color, 0.5 * s, 0, z + 1.1 * s, 0.22 * s, 0.22 * s, 0.75 * s)
    acc.box(color, 0.62 * s, 0, z + 1.75 * s, 0.32 * s, 0.18 * s, 0.18 * s)
    for lx in (-0.42, 0.42):
        for ly in (-0.14, 0.14):
            acc.box(color, lx * s, ly * s, z, 0.12 * s, 0.12 * s, 0.78 * s)
    acc.pop()


def cone_tree(acc, x, y, z, r, color="#6E8456"):
    acc.cyl(TIMBER, x, y, z, r * 0.12, r * 0.8, 6)
    acc.lathe(color, x, y, z + r * 0.6, [(r, 0), (r * 0.7, r * 1.1), (0.05, r * 2.0)], 8)


def maize_rows(acc, x0, x1, y0, y1, z, step=2.2, color=MAIZE, hgt=1.4):
    yy = y0
    while yy <= y1:
        xx = x0
        while xx <= x1:
            acc.box(color, xx, yy, z, 0.35, 0.35, hgt, 0, 0.12, 0.12)
            xx += step
        yy += step * 0.9


# ---------------------------------------------------------------- Spanish baroque

def balustrade(acc, a, b, z, color, h=0.9, step=0.7):
    (ax, ay), (bx, by) = a, b
    L = math.hypot(bx - ax, by - ay)
    ang = math.atan2(by - ay, bx - ax)
    acc.box(color, (ax + bx) / 2, (ay + by) / 2, z + h - 0.18, L, 0.42, 0.18, ang)
    n = max(2, int(L / step))
    for i in range(n + 1):
        t = i / n
        acc.box(color, ax + (bx - ax) * t, ay + (by - ay) * t, z, 0.22, 0.22, h - 0.18, ang, 0.14, 0.14)


def pinnacle(acc, x, y, z, s, color):
    acc.box(color, x, y, z, s, s, s * 1.2)
    acc.lathe(color, x, y, z + s * 1.2, [(s * 0.35, 0), (s * 0.45, s * 0.4), (s * 0.12, s * 1.0), (0.02, s * 1.5)], 8)


def cross(acc, x, y, z, s, color=BRONZE):
    acc.box(color, x, y, z, 0.15 * s, 0.15 * s, 1.6 * s)
    acc.box(color, x, y, z + 1.0 * s, 0.8 * s, 0.15 * s, 0.15 * s)


def bell_tower(acc, x, y, z, w, h, color, trim, rnd=None, belfry=True, cupola=True, ashlar=True, storeys=2, cupola_color=None):
    """A square Spanish tower: a plain shaft with bands, one or two belfry storeys with arched openings, corner pinnacles, a cupola and lantern."""
    acc.box(color, x, y, z, w, w, h)
    for k in range(1, 4):
        acc.box(trim, x, y, z + h * k / 4 - 0.25, w + 0.3, w + 0.3, 0.3)
    if ashlar and rnd:
        for f, (a, b) in (("S", ((x - w / 2, y - w / 2), (x + w / 2, y - w / 2))), ("E", ((x + w / 2, y - w / 2), (x + w / 2, y + w / 2))),
                          ("N", ((x + w / 2, y + w / 2), (x - w / 2, y + w / 2))), ("W", ((x - w / 2, y + w / 2), (x - w / 2, y - w / 2)))):
            stone_face(acc, a, b, z, h * 0.5, 0.0, tones(color, 0.05), rnd, course=0.9, block=1.9, jit=0.12, cham=0.04, proud=(0.03, 0.06))
    acc.box(trim, x, y, z + h, w + 0.8, w + 0.8, 0.5)
    zz = z + h + 0.5
    bw = w * 0.86
    for s in range(storeys if belfry else 0):
        bh = w * (0.95 if s == 0 else 0.75)
        acc.box(color, x, y, zz, bw, bw, bh)
        for f, (dx, dy) in (("S", (0, -bw / 2)), ("N", (0, bw / 2)), ("E", (bw / 2, 0)), ("W", (-bw / 2, 0))):
            nb = 2 if s == 0 else 1
            for k in range(nb):
                o = (k - (nb - 1) / 2) * bw * 0.42
                px, py = (x + dx + (o if f in "SN" else 0), y + dy + (o if f in "EW" else 0))
                acc.arch(DARK, px, py, zz + bh * 0.2, bw * (0.3 if nb == 2 else 0.42), bh * 0.62, f, 0.4)
            # pilasters
            for k in (-1, 1):
                px, py = (x + dx + (k * bw * 0.47 if f in "SN" else 0), y + dy + (k * bw * 0.47 if f in "EW" else 0))
                acc.box(trim, px, py, zz, 0.45, 0.45, bh)
        acc.box(trim, x, y, zz + bh, bw + 0.6, bw + 0.6, 0.4)
        for sx in (-1, 1):
            for sy in (-1, 1):
                pinnacle(acc, x + sx * bw / 2, y + sy * bw / 2, zz + bh + 0.4, w * 0.13, trim)
        zz += bh + 0.4
        bw *= 0.78
    if cupola:
        r = bw * 0.5
        acc.cyl(color, x, y, zz, r, r * 0.4, 16)
        acc.lathe(cupola_color or DOMEC, x, y, zz + r * 0.4, [(r, 0)] + [(r * math.cos(a), r * math.sin(a) * 0.95) for a in [math.pi / 2 * i / 6 for i in range(1, 7)]], 16)
        acc.cyl(trim, x, y, zz + r * 1.3, r * 0.25, r * 0.5, 8)
        acc.lathe(trim, x, y, zz + r * 1.8, [(r * 0.3, 0), (0.05, r * 0.35)], 8)
        cross(acc, x, y, zz + r * 2.1, w * 0.12)
    return zz


def church_dome(acc, x, y, z, r, color, trim, dome_color=DOMEC, drum=0.7, windows=8):
    acc.cyl(color, x, y, z, r * 1.05, r * drum, 20)
    for i in range(windows):
        a = math.tau * (i + 0.5) / windows
        acc.box(DARK, x + math.cos(a) * r * 1.03, y + math.sin(a) * r * 1.03, z + r * drum * 0.25, 0.35, r * 0.28, r * drum * 0.5, a)
        acc.box(trim, x + math.cos(a + math.pi / windows) * r * 1.07, y + math.sin(a + math.pi / windows) * r * 1.07, z, 0.5, 0.5, r * drum, a)
    acc.cyl(trim, x, y, z + r * drum, r * 1.12, 0.45, 20)
    zz = z + r * drum + 0.45
    acc.lathe(dome_color, x, y, zz, [(r, 0)] + [(r * math.cos(a), r * math.sin(a) * 1.05) for a in [math.pi / 2 * i / 8 for i in range(1, 9)]], 20)
    for i in range(8):
        a = math.tau * i / 8
        acc.box(trim, x + math.cos(a) * r * 0.72, y + math.sin(a) * r * 0.72, zz, 0.35, 0.35, r * 0.72, a)
    zt = zz + r * 1.0
    acc.cyl(trim, x, y, zt, r * 0.22, r * 0.45, 8)
    acc.lathe(dome_color, x, y, zt + r * 0.45, [(r * 0.26, 0), (r * 0.16, r * 0.2), (0.03, r * 0.33)], 8)
    cross(acc, x, y, zt + r * 0.75, r * 0.18)


def retable(acc, x, y, z, w, h, color, tiers=3, door_w=None, rnd=None):
    """A carved stone retable-facade on a wall facing -Y at y: tiers of paired columns, niches, cornices, a crowning pediment."""
    th = h / tiers
    door_w = door_w or w * 0.3
    for k in range(tiers):
        zz = z + k * th
        ww = w * (1 - 0.12 * k)
        acc.box(color, x, y - 0.4, zz, ww, 0.8, th)
        for s in (-1, 1):
            for c in (0.32, 0.44):
                acc.cyl(shade(color, 0.08), x + s * ww * c, y - 0.95, zz + 0.3, 0.32, th - 0.9, 10)
                acc.box(shade(color, 0.08), x + s * ww * c, y - 0.95, zz, 0.8, 0.8, 0.3)
                acc.box(shade(color, 0.08), x + s * ww * c, y - 0.95, zz + th - 0.6, 0.85, 0.85, 0.6)
            if k < tiers - 1 or tiers == 1:
                acc.arch(DARK, x + s * ww * 0.38, y - 0.85, zz + th * 0.22, ww * 0.07, th * 0.5, "S", 0.3)
        acc.box(shade(color, 0.12), x, y - 0.6, zz + th - 0.35, ww + 0.8, 1.4, 0.35)
        if k == 0:
            acc.arch(DARK, x, y - 0.9, zz, door_w, th * 0.85, "S", 0.4)
        elif k == tiers - 1:
            acc.arch(DARK, x, y - 0.9, zz + th * 0.15, ww * 0.18, th * 0.6, "S", 0.3)
        else:
            acc.arch(DARK, x, y - 0.9, zz + th * 0.2, ww * 0.12, th * 0.55, "S", 0.3)
    # broken-curve pediment
    zt = z + h
    ww = w * (1 - 0.12 * (tiers - 1))
    pts = [(ww / 2 * math.cos(math.pi * i / 10), ww / 4 * math.sin(math.pi * i / 10)) for i in range(11)]
    acc.panel(shade(color, 0.05), [(-ww / 2, 0)] + list(reversed(pts))[1:-1] + [(ww / 2, 0)], x, y - 0.4, zt, "S", 0.8)
    cross(acc, x, y - 0.4, zt + ww / 4, 1.6)


def church(acc, L, W, H, rnd, color=CANT, trim=CANT_L, roof=TILE, towers=2, tw=7.0, th=None, dome_r=0.0, dome_at=0.62, front_h=None,
           aisles=0.0, portals=1, buttress=True, retable_w=None, belfry_storeys=2, ashlar=True, balus=True, apse=False, cupola_color=None, z=0.0):
    """A Spanish church, facade at y = -L/2 (south), altar at +Y; origin at the middle of the plan."""
    y0 = -L / 2
    th = th or H * 1.7
    front_h = front_h or H * 1.25
    nave_w = W - 2 * aisles
    acc.box(color, 0, 0, z, nave_w, L, H)
    if aisles:
        for s in (-1, 1):
            acc.box(color, s * (nave_w / 2 + aisles / 2), 0.0, z, aisles, L - (tw if towers else 0) * 0.0, H * 0.78)
            acc.roof(roof, s * (nave_w / 2 + aisles / 2), 0.0, z + H * 0.78, L - 1, aisles, aisles * 0.3, "y", over=0.3, eave=0.25, ridge=False)
    # buttresses and windows along the sides
    nb = max(3, int(L / 8))
    for i in range(nb):
        yy = y0 + (tw if towers else 2) + 3 + (L - (tw if towers else 2) - 6) * i / (nb - 1)
        for s in (-1, 1):
            if buttress:
                acc.box(shade(color, -0.05), s * (W / 2 + 0.7), yy, z, 1.4, 2.0, H * (0.78 if aisles else 0.95), 0, 0.7, 1.6)
            if i < nb - 1:
                wy = yy + (L - (tw if towers else 2) - 6) / (nb - 1) / 2
                acc.arch(DARK, s * (W / 2 + 0.03), wy, z + (H * 0.78 if aisles else H) * 0.5, 1.4, 2.8, "E" if s > 0 else "W", 0.25)
                if aisles:
                    acc.arch(DARK, s * (nave_w / 2 + 0.03), wy, z + H * 0.82, 1.2, 2.0, "E" if s > 0 else "W", 0.25)
    acc.box(trim, 0, 0, z + H, nave_w + 0.8, L + 0.2, 0.6)
    acc.roof(roof, 0, 0.6, z + H + 0.6, L - 0.6, nave_w, nave_w * 0.33, "y", over=0.35, eave=0.25)
    if balus:
        for s in (-1, 1):
            balustrade(acc, (s * (W / 2 + 0.1), y0 + 2), (s * (W / 2 + 0.1), L / 2 - 2), z + (H * 0.78 if aisles else H) + 0.0, trim, 0.8, 1.0)
    if apse:
        r = nave_w / 2
        pts = [(r * math.cos(-math.pi / 2 + math.pi * i / 8 - math.pi / 2), 0) for i in range(0)]
        acc.prism(color, [(r * math.cos(a), L / 2 + r * math.sin(a)) for a in [math.pi * i / 8 for i in range(9)]][::-1] + [], z, H)
        acc.prism(roof, [(r * math.cos(a), L / 2 + r * math.sin(a)) for a in [math.pi * i / 8 for i in range(9)]][::-1], z + H, 0.6,
                  [(0.6 * r * math.cos(a), L / 2 + 0.6 * r * math.sin(a)) for a in [math.pi * i / 8 for i in range(9)]][::-1])
    # front: a frontispiece wall rising over the roof, ashlar, with the retable portal
    fw = W if towers else W + 1
    acc.box(color, 0, y0 + 1.0, z, fw - (2 * tw if towers == 2 else 0) + 1.0, 2.0, front_h)
    acc.box(trim, 0, y0 + 1.0, z + front_h, fw - (2 * tw if towers == 2 else 0) + 1.6, 2.4, 0.5)
    if ashlar:
        a, b = (-(fw / 2 - (tw if towers == 2 else 0)), y0), ((fw / 2 - (tw if towers == 2 else 0)), y0)
        stone_face(acc, a, b, z, front_h, 0.0, tones(color, 0.05), rnd, course=0.9, block=2.0, jit=0.12, cham=0.04, proud=(0.03, 0.06),
                   skip=[((fw / 2 - (tw if towers == 2 else 0)) - (retable_w or W * 0.4) / 2 - 0.5, (fw / 2 - (tw if towers == 2 else 0)) + (retable_w or W * 0.4) / 2 + 0.5, z + front_h + 5)])
    rw = retable_w or W * 0.4
    retable(acc, 0, y0, z, rw, front_h * 0.92, shade(color, 0.12), 3)
    if portals > 1:
        for s in (-1, 1):
            acc.arch(DARK, s * W * 0.3 * (0.7 if towers == 2 else 1.0), y0 - 0.1, z, 2.4, 5.0, "S", 0.5)
            acc.box(trim, s * W * 0.3 * (0.7 if towers == 2 else 1.0), y0 - 0.2, z + 5.4, 3.6, 0.6, 0.5)
    # towers
    if towers:
        spots = [(-1,), (1,)] if towers == 2 else [(-1,)]
        for (s,) in spots:
            tx = s * (W / 2 - tw / 2 + (0.0 if towers == 2 else 0.8))
            bell_tower(acc, tx, y0 + tw / 2 - 0.5, z, tw, th * 0.62, color, trim, rnd, storeys=belfry_storeys, cupola_color=cupola_color)
    if dome_r:
        dy = y0 + L * dome_at
        base = nave_w * 0.33 + 1.6
        acc.cyl(color, 0, dy, z + H, dome_r * 1.3, base, 8)
        acc.cyl(trim, 0, dy, z + H + base, dome_r * 1.38, 0.4, 8)
        church_dome(acc, 0, dy, z + H + base + 0.4, dome_r, color, trim)


def colonial_range(A1, A2, a, b, depth, h, rnd, wall=WHITE, roof=TILE, inca=AND, inca_h=0.0, arcade_side=0, storeys=2, balcony_side=0, arcade_storeys=9):
    """A colonial building range along a->b: Inca courses at the foot, whitewashed upper walls, tile roof, arcades or balconies."""
    (ax, ay), (bx, by) = a, b
    L = math.hypot(bx - ax, by - ay)
    ang = math.atan2(by - ay, bx - ax)
    cx, cy = (ax + bx) / 2, (ay + by) / 2
    A1.push(cx, cy, math.degrees(ang))
    A2.push(cx, cy, math.degrees(ang))
    if inca_h:
        A1.box(inca, 0, 0, 0, L, depth, inca_h)
        for sd in (1, -1):
            stone_face(A1, (-L / 2, sd * depth / 2), (L / 2, sd * depth / 2), 0, inca_h, 0.0, tones(inca), rnd, course=0.7, block=1.3, jit=0.3, cham=0.2,
                       proud=(0.04, 0.1), side=(1 if sd < 0 else -1))
    A1.box(wall, 0, 0, inca_h, L, depth, h - inca_h)
    A1.box(shade(wall, -0.1), 0, 0, h - 0.3, L + 0.2, depth + 0.2, 0.3)
    n = max(2, int(L / 3.5))
    for k in range(storeys):
        zz = (h / storeys) * k
        for i in range(n):
            s = -L / 2 + L * (i + 0.5) / n
            for sd in (1, -1):
                if sd == arcade_side and k < arcade_storeys:
                    A1.arch(DARK, s, sd * (depth / 2 + 0.02), zz + 0.2, L / n * 0.62, h / storeys * 0.8, "N" if sd > 0 else "S", 0.3)
                elif zz + 1.0 >= inca_h:
                    A1.box(DARK, s, sd * (depth / 2 + 0.02), zz + h / storeys * 0.3, 1.0, 0.3, h / storeys * 0.45)
        if balcony_side and k == storeys - 1:
            for i in range(0, n, 2):
                s = -L / 2 + L * (i + 0.5) / n
                A1.box(WOOD, s, balcony_side * (depth / 2 + 0.7), zz + 0.3, 3.0, 1.4, 0.25)
                A1.box(WOOD, s, balcony_side * (depth / 2 + 0.7), zz + 0.55, 3.0, 1.4, 1.4, 0, 3.0, 1.4)
                A1.box(shade(WOOD, -0.25), s, balcony_side * (depth / 2 + 1.42), zz + 0.7, 2.6, 0.1, 1.0)
                A2.box(TILE, s, balcony_side * (depth / 2 + 0.75), zz + 1.95, 3.4, 1.6, 0.25)
    A1.pop()
    A2.roof(roof, 0, 0, h, L, depth, depth * 0.3, "x", over=0.5, eave=0.2, ridge=False)
    A2.pop()


# ---------------------------------------------------------------- the temple of the sun

ARC_R, ARC_C = 30.0, (-24.0, 12.0)


def _arc_pts(n=10):
    a0 = math.asin(18 / ARC_R)
    return [(ARC_C[0] + ARC_R * math.sin(-a0 + 2 * a0 * i / n), ARC_C[1] - ARC_R * math.cos(-a0 + 2 * a0 * i / n)) for i in range(n + 1)]


def cori_base(A0, A1, A2, rnd, gold=True, colonial=False):
    """Ground, the platform of the compound and the garden terraces falling toward the Saphy (south)."""
    P = 3.0
    A0.box(EARTH, 0, 0, 0, 90, 110, 0.3)
    A0.box(shade(AND, 0.15), 0, 17, 0.3, 86, 74, P - 0.3)                       # platform y -20..54
    A0.box(EARTH, 0, -26, 0.3, 86, 12, 1.7)                                      # tier A y -32..-20, top 2.0
    A0.box(EARTH, 0, -38, 0.3, 86, 12, 0.8)                                      # tier B y -44..-32, top 1.1
    cols = tones(AND)
    sk = [(43 + 21, 43 + 27, 9)]
    stone_face(A0, (-43, -20), (43, -20), 2.0, 1.0, 0.0, cols, rnd, 0.5, 1.4, 0.25, 0.15, 0, (0.04, 0.1), skip=sk)
    stone_face(A0, (-43, -32), (43, -32), 1.1, 0.9, 0.0, cols, rnd, 0.45, 1.4, 0.25, 0.15, 0, (0.04, 0.1), skip=sk)
    stone_face(A0, (-43, -44), (43, -44), 0.3, 0.8, 0.0, cols, rnd, 0.4, 1.4, 0.25, 0.15, 0, (0.04, 0.1), skip=sk)
    for a, b in (((43, -20), (43, 54)), ((43, 54), (-43, 54)), ((-43, 54), (-43, -20))):
        stone_face(A0, a, b, 0.3, P - 0.3, 0.0, cols, rnd, 1.1, 2.6, 0.25, 0.15, 0, (0.04, 0.1))
    # stair down the garden
    for k in range(12):
        A0.box(shade(AND, 0.1), 24, -20 - 2.0 + (24 - 2 * k) * 0.0 - k * 2.0 + 2.0, 0.3, 5, 2.0, max(0.1, P - 0.3 - k * 0.24))
    # garden beds
    A0.box(GRASS, -8, -26, 2.0, 62, 9, 0.15)
    A0.box(GRASS, -8, -38, 1.1, 62, 9, 0.15)
    A0.box(GRASS, 0, -49.5, 0.3, 84, 9, 0.15)
    if gold:
        maize_rows(A2, -36, 18, -29.5, -22.5, 2.15, 2.4, GOLD, 1.7)
        for i, (lx, ly) in enumerate([(-34, -36), (-26, -40), (-18, -35.5), (-10, -39), (-2, -36), (8, -40), (14, -35.5)]):
            llama(A2, lx, ly, 1.25, GOLD, 30 * i)
        for fx, fy in ((-30, -38), (0, -40.5), (16, -38.5)):
            figure(A2, fx, fy, 1.25, shade(GOLD, -0.1), 1.2)
        maize_rows(A2, -38, 38, -53, -46, 0.45, 3.0, shade(GOLD, -0.15) if not colonial else MAIZE, 1.3)
    else:
        maize_rows(A1, -36, 18, -29.5, -22.5, 2.15, 3.0, MAIZE, 1.3)
        maize_rows(A1, -38, 38, -53, -46, 0.45, 3.0, MAIZE, 1.3)
        for i in range(8):
            cone_tree(A1, -34 + i * 8.5, -38 + (i % 2) * 2, 1.25, 2.2)
    return P


def cori_enclosure(A1, A2, rnd, P, h=5.5, gold=True, inca_h=None):
    """The outer walls with the curved wall at the south-west, a double-jamb gate on the street (north) side, and the gold band."""
    t, bat = 1.4, 0.04
    hh = inca_h or h
    straight = [(-6, -12), (42, -12), (42, 52), (-42, 52), (-42, -12)]
    skips = {3: [(42 - 3.0, 42 + 3.0, P + 4.0)], 1: [(26 - 1.6, 26 + 1.6, P + 3.0)]}
    fitted_wall(A1, straight, P, hh, t, AND, rnd, faces=(1,), batter=bat, course=0.85, block=1.9, jit=0.25, cham=0.16, skips=skips)
    arc = _arc_pts(10)
    fitted_wall(A1, arc, P, hh + (1.0 if not inca_h else 0.0), t + 0.2, shade(AND, 0.05), rnd, faces=(1,), batter=bat * 0.7, course=0.7, block=1.6, jit=0.12, cham=0.08)
    A1.trap(shade(AND, -0.3), 0, 52 + t / 2, P, 3.2, 2.5, 4.0, "N", 0.6)
    A1.trap(DARK, 0, 52 + t / 2, P, 2.2, 1.7, 3.5, "N", 0.75)
    A1.trap(DARK, 26, -12 - t / 2, P, 1.5, 1.15, 2.8, "S", 0.7)
    if gold:
        zb = P + h * 0.78
        tt = t - 2 * bat * h * 0.78 + 0.32
        for i in range(1, len(straight)):
            A2.seg(GOLD, straight[i - 1], straight[i], zb, tt, 0.8, ext=tt)
        for i in range(1, len(arc)):
            A2.seg(GOLD, arc[i - 1], arc[i], zb + 0.6, tt + 0.2, 0.8, ext=0.4)
        A2.box(GOLD, 0, 52, P, 3.6, t + 0.5, 0.4)


def coricancha():
    rnd = random.Random(7)
    m = Model("coricancha")
    A0, A1, A2 = Acc("cori0"), Acc("cori1"), Acc("cori2")
    P = cori_base(A0, A1, A2, rnd, gold=True)
    A1.box(PAVE, 0, 20, P, 82, 62, 0.12)
    cori_enclosure(A1, A2, rnd, P)
    # the shrines round the court
    blds = [  # x, y, L, W, axis, door side, doors, gold
        (33, 20, 52, 12, "y", -1, 4, True),          # the sun
        (-25, 43, 22, 9, "x", -1, 2, False),          # moon
        (6, 43, 30, 9, "x", -1, 3, False),            # stars
        (-19, 0, 22, 9, "x", 1, 2, False),            # thunder
        (6, 0, 26, 9, "x", 1, 2, False),              # rainbow
        (-36, 22, 22, 8, "y", 1, 2, False),           # priests
    ]
    for x, y, L, W, ax, ds, nd, g in blds:
        h = 5.0 if g else 4.4
        inca_house(A1, x, y, P, L, W, h, ax, ds, nd, AND, rnd=rnd, faced=True, jamb=GOLD if g else shade(AND, -0.25), niches=2, gold=GOLD if g else None)
        inca_roof(A2, x, y, P, L, W, h, ax, rh=W * 0.7)
    # the octagonal font in the court
    A1.lathe(shade(AND, 0.1), -4, 21, P, [(2.2, 0), (2.2, 0.7), (1.9, 0.9)], 8)
    A1.cyl(WATERC, -4, 21, P + 0.9, 1.7, 0.05, 8)
    A2.box(GOLD, -4, 21, P + 0.95, 0.5, 0.5, 0.5)
    m.add(0, A0.build(), "platform")
    m.add(1, A1.build(), "walls")
    m.add(2, A2.build(), "roofs")
    return m


def inticancha():
    """The early Inticancha: a small fieldstone enclosure with three thatched shrine-houses, fields round about."""
    rnd = random.Random(11)
    m = Model("inticancha")
    A0, A1, A2 = Acc("int0"), Acc("int1"), Acc("int2")
    A0.box(EARTH, 0, 0, 0, 90, 110, 0.3)
    A0.box(shade(EARTH, -0.08), 0, 17, 0.3, 50, 44, 1.2)
    stone_face(A0, (-25, -5), (25, -5), 0.3, 1.2, 0.0, tones(FIELD), rnd, 0.45, 0.8, 0.45, 0.35, 0.2, (0.04, 0.12))
    kancha_c(A1, A2, 0, 17, 38, 30, rnd, FIELD, wall_h=2.4, t=0.9, gate="N", sides="NEW", hw=5.0, hh=2.6, z=1.5, block=0.8, course=0.45, slope=0.25,
             fine=False, court=EARTH, frac=0.7, doors=1)
    A1.cyl(shade(FIELD, 0.1), -6, 13, 1.5, 0.9, 1.6, 8, 0.7)             # a standing stone (huaca) in the yard
    # fields: terraces of maize and potatoes falling toward the stream
    for k, (y0, y1, zt) in enumerate(((-12, -24, 0.9), (-24, -38, 0.6), (-38, -54, 0.3))):
        A0.box(shade(EARTH, -0.04 * k), 0, (y0 + y1) / 2, 0.3, 88, abs(y1 - y0), zt - 0.3 + 0.01)
        stone_face(A0, (-44, y0), (44, y0), zt, 0.3, 0.0, tones(FIELD), rnd, 0.3, 0.7, 0.4, 0.3, 0.2, (0.04, 0.1))
        maize_rows(A1, -40, 40, y1 + 1.5, y0 - 1.5, zt, 2.8 if k != 1 else 2.0, MAIZE if k != 1 else "#6E8650", 1.3 if k != 1 else 0.5)
    for i, (hx, hy) in enumerate(((-34, 44), (32, 46), (36, 30))):
        A1.cyl(FIELD, hx, hy, 0.3, 2.6, 2.0, 12)
        A2.lathe(ICHU, hx, hy, 2.3, [(3.2, 0), (0.15, 3.4)], 12)
    m.add(0, A0.build(), "ground")
    m.add(1, A1.build(), "walls")
    m.add(2, A2.build(), "roofs")
    return m


def santo_domingo():
    """Santo Domingo on the Coricancha: the Dominican church with its apse on the curved wall, the cloister round the Inca chambers."""
    rnd = random.Random(13)
    m = Model("santo-domingo")
    A0, A1, A2, A3 = Acc("sd0"), Acc("sd1"), Acc("sd2"), Acc("sd3")
    P = cori_base(A0, A1, A2, rnd, gold=False, colonial=True)
    A1.box(PAVE, 0, 20, P, 82, 62, 0.12)
    cori_enclosure(A1, A2, rnd, P, h=5.5, gold=False, inca_h=3.6)
    # church: apse on the curved wall, facade on the street (north), tower at its west corner
    A2.push(-24, 19, 180)
    church(A2, 60, 16, 14, rnd, color=WHITE, trim=CANT_L, towers=0, front_h=17, retable_w=8, apse=True, ashlar=False, balus=False, z=P)
    A2.pop()
    A3.push(-35.5, 47, 0)
    bell_tower(A3, 0, 0, P, 7.5, 18, CANT, CANT_L, rnd, storeys=2)
    A3.pop()
    # the cloister, two storeys of arcades, round the Inca chambers
    cx0, cx1, cy0, cy1 = -12, 38, -6, 46
    for a, b, sd in (((cx0, cy0 + 3.5), (cx1, cy0 + 3.5), 1), ((cx1 - 3.5, cy0 + 7), (cx1 - 3.5, cy1 - 7), 1), ((cx1, cy1 - 3.5), (cx0, cy1 - 3.5), 1), ((cx0 + 3.5, cy1 - 7), (cx0 + 3.5, cy0 + 7), 1)):
        colonial_range(A1, A2, a, b, 7, 9, rnd, wall=WHITE, inca_h=0, arcade_side=sd, storeys=2)
    for (x, y, L, W, ax, ds) in ((13, 27, 16, 8, "x", -1), (13, 10, 16, 8, "x", 1)):
        inca_house(A1, x, y, P, L, W, 4.4, ax, ds, 2, AND, rnd=rnd, faced=True, niches=2)
        inca_roof(A2, x, y, P, L, W, 4.4, ax, rh=W * 0.45, roof=TILE)
    A1.lathe(shade(AND, 0.1), 13, 18.5, P, [(1.8, 0), (1.8, 0.7), (1.5, 0.9)], 8)
    m.add(0, A0.build(), "platform")
    m.add(1, A1.build(), "inca walls")
    m.add(2, A2.build(), "church")
    m.add(3, A3.build(), "tower")
    return m


# ---------------------------------------------------------------- Sacsayhuamán

def zigzag(yb, amp, x0, x1, period=24.0):
    pts = []
    n = int(round((x1 - x0) / period))
    for i in range(n + 1):
        x = x0 + (x1 - x0) * i / n
        pts.append((x, yb))
        if i < n:
            pts.append((x + (x1 - x0) / n / 2, yb - amp))
    return pts


def sacsayhuaman(phase="1530"):
    rnd = random.Random(17)
    m = Model("sacsayhuaman-" + phase)
    A0, A1, A2, A3 = Acc("sx0"), Acc("sx1"), Acc("sx2"), Acc("sx3")
    A0.box(GRASS, 0, 0, 0, 380, 240, 0.3)
    A0.box(shade(SAND, -0.05), 0, -100, 0.3, 360, 36, 0.08)                         # the esplanade, Chuquipampa
    walls = [  # base line, amplitude, x-extent, height, block, course, base z
        (-74, 10, 168, 7.0, 3.2, 2.3, 0.3),
        (-62, 9, 156, 5.5, 2.3, 1.7, 7.3),
        (-51, 8, 144, 4.5, 1.6, 1.2, 12.8),
    ]
    back = 20
    top = 17.3
    built = {"1530": (1.0, 1.0, 1.0), "1470": (0.6, 0.0, 0.0), "ruin": (1.0, 0.75, 0.45)}[phase]
    for k, (yb, amp, xe, h, blk, crs, zb) in enumerate(walls):
        line = zigzag(yb, amp, -xe, xe)
        poly = line + [(xe, back), (-xe, back)]
        fill = EARTH if (phase == "1470" and k > 0) else shade(GRASS, -0.05 * k)
        if built[k] > 0:
            A0.prism(fill, poly, zb, h)
        else:   # still a raw earth slope
            A0.prism(fill, poly, zb, h, [(x, y + 7) for x, y in line] + [(xe, back), (-xe, back)])
        if built[k] <= 0:
            continue
        zs = zb
        hs = h * (built[k] if phase == "1470" else 1.0)
        for i in range(1, len(line)):
            a, b = line[i - 1], line[i]
            if phase == "1470" and a[0] > 40:
                continue
            gate = (i == len(line) // 2)
            if phase == "ruin" and k > 0 and rnd.random() > built[k]:
                hs_i = hs * rnd.uniform(0.25, 0.6)
            else:
                hs_i = hs
            L = math.hypot(b[0] - a[0], b[1] - a[1])
            sk = [(L / 2 - 2.0, L / 2 + 2.0, zs + 4.0)] if gate else []
            stone_face(A1, a, b, zs, hs_i, 0.0, tones(LIME, 0.08), rnd, course=crs, block=blk, jit=0.45, cham=0.3, slope=0.32, proud=(0.12, 0.35), skip=sk)
            if gate:
                mx, my = (a[0] + b[0]) / 2, (a[1] + b[1]) / 2
                ang = math.degrees(math.atan2(b[1] - a[1], b[0] - a[0]))
                A1.push(mx, my, ang)
                A1.trap(shade(LIME, -0.3), 0, -0.1, zs, 4.0, 3.0, 3.8, "S", 0.6)
                A1.trap(DARK, 0, -0.15, zs, 3.0, 2.2, 3.4, "S", 0.7)
                A1.pop()
                for j in range(6):
                    A1.box(shade(LIME, 0.1), mx, my + 1.5 + j * 1.2, zs + j * h / 6, 3.0, 1.2, h / 6)
            if phase == "1530":     # parapet on top, set back
                A2.seg(shade(LIME, 0.06), (a[0], a[1] + 1.2), (b[0], b[1] + 1.2), zb + h, 1.0, 1.0, ext=1.0)
    # the hill behind, as five contour layers rounding off toward the city
    lh = (top - 0.3) / 5
    for j in range(5):
        rx, ry = 178 - 12 * j, 94 - 7 * j
        pts = [(x, 22 + y) for x, y in blob_pts(rx, ry, 300 + j, 40, 0.05)]
        tp = [(x * 0.96, 22 + y * 0.95) for x, y in blob_pts(rx, ry, 300 + j, 40, 0.05)]
        A0.prism(shade(GRASS, -0.06 + 0.03 * j), pts, 0.3 + j * lh, lh, tp)
    if phase != "ruin":
        A0.lathe(PAVE, 0, 20, top, [(34, 0), (34, 0.1)], 32)
        A0.box(PAVE, 0, 45, top, 120, 18, 0.1)
    if phase == "1470":
        # ramps of earth and stones on their way
        for x in (-90, -30, 30):
            A1.box(EARTH, x, -95, 0.3, 8, 22, 4.5, 0, 6, 0.6)
        for i in range(14):
            x = rnd.uniform(-170, 170)
            A1.box(rnd.choice(tones(LIME)), x, rnd.uniform(-115, -88), 0.3, rnd.uniform(2, 4), rnd.uniform(1.5, 3), rnd.uniform(1.2, 2.6), rnd.uniform(0, 3))
        for i in range(8):     # workers' huts
            hx, hy = rnd.uniform(-100, 100), rnd.uniform(45, 70)
            A1.cyl(FIELD, hx, hy, top, 2.4, 1.8, 10)
            A2.lathe(ICHU, hx, hy, top + 1.8, [(3.0, 0), (0.12, 3.2)], 10)
        A1.ring(LIME, 0, 20, top, 11, 12.2, 1.4, 40)
        A1.ring(LIME, 0, 20, top, 7, 8.2, 1.0, 32)
        m.add(0, A0.build(), "hill")
        m.add(1, A1.build(), "walls")
        m.add(2, A2.build(), "camp")
        return m
    if phase == "ruin":
        A1.ring(LIME, 0, 20, top, 11, 12.2, 0.9, 40)
        A1.ring(LIME, 0, 20, top, 7, 8.2, 0.7, 32)
        A1.ring(LIME, 0, 20, top, 3.6, 4.8, 0.5, 24)
        for sx in (-52, 52):
            for a, b in (((-11, -7), (11, -7)), ((11, -7), (11, 7)), ((11, 7), (-11, 7)), ((-11, 7), (-11, -7))):
                A1.seg(LIME, (sx + a[0], 30 + a[1]), (sx + b[0], 30 + b[1]), top, 1.2, rnd.uniform(0.6, 1.6), ext=1.2)
        for i in range(25):
            x = rnd.uniform(-170, 170)
            A1.box(rnd.choice(tones(LIME)), x, rnd.uniform(-90, -80), 0.3, rnd.uniform(1, 2.5), rnd.uniform(1, 2), rnd.uniform(0.8, 1.6), rnd.uniform(0, 3))
        m.add(0, A0.build(), "hill")
        m.add(1, A1.build(), "walls")
        return m
    # Muyuqmarka: three concentric round walls, a tall roofed core
    mx, my = 0, 20
    A3.ring(LIME, mx, my, top, 11, 12.2, 3.5, 48)
    A3.ring(shade(LIME, 0.05), mx, my, top, 7, 8.2, 8.0, 40)
    round_tower(A3, A3, mx, my, top, 4.8, 14.0, rnd, LIME, ICHU, rh=9.0, door="S")
    for r0, r1, z1 in ((8.2, 11.0, 3.5), (4.8, 7.0, 8.0)):
        A3.ring(shade(ICHU, -0.05), mx, my, top + z1, r0 - 0.2, r1 + 0.4, 0.5, 40)
    A3.trap(DARK, mx, my - 12.2, top, 1.6, 1.2, 2.4, "S", 1.0)
    A3.trap(DARK, mx, my - 8.2, top, 1.4, 1.1, 2.4, "S", 1.0)
    # Sallaqmarka and Paucarmarka: rectangular towers
    for sx in (-52, 52):
        inca_house(A3, sx, 30, top, 22, 14, 13.0, "x", -1, 3, LIME, rnd=rnd, faced=True, niches=2, gable=False, door_w=1.4)
        A3.box(DARK, sx, 30 - 7 + 0.4, top + 8.5, 1.0, 0.3, 1.4)
        A3.roof(ICHU, sx, 30, top + 13.0, 20.7, 12.7, 8.0, "x", over=0.8, hip=6.5)
    # storerooms and halls behind, the water tank and channels
    for x, y in ((-96, 52), (-72, 62), (72, 62), (96, 52), (-30, 66), (30, 66)):
        inca_house(A2, x, y, top, 18, 7, 3.6, "x", -1, 3, LIME, rnd=rnd)
        inca_roof(A2, x, y, top, 18, 7, 3.6, "x")
    A2.box(shade(LIME, -0.1), 0, 62, top, 16, 9, 0.6)
    A2.box(WATERC, 0, 62, top + 0.1, 14, 7, 0.55)
    A2.box(WATERC, 0, 44, top, 0.6, 18, 0.2)
    m.add(0, A0.build(), "terraces")
    m.add(1, A1.build(), "zigzag walls")
    m.add(2, A2.build(), "parapets and halls")
    m.add(3, A3.build(), "towers")
    return m


# ---------------------------------------------------------------- the plaza

def haukaypata():
    rnd = random.Random(19)
    m = Model("haukaypata")
    A0, A1, A2 = Acc("hk0"), Acc("hk1"), Acc("hk2")
    A0.box(SAND, 0, 0, 0, 180, 124, 0.3)
    for a, b in (((-90, -62), (90, -62)), ((90, -62), (90, 62)), ((90, 62), (-90, 62)), ((-90, 62), (-90, -62))):
        A0.seg(shade(AND, 0.1), a, b, 0.3, 1.0, 0.4, ext=1.0)
    # the ushnu: three stepped tiers of fitted stone, a stair, a seat and a libation basin
    ux, uy = 6, -16
    z = 0.3
    for k, (w, hgt) in enumerate(((24, 1.8), (17, 1.6), (10.5, 1.4))):
        A1.box(shade(AND, 0.05 * k), ux, uy, z, w, w, hgt, 0, w - 0.3, w - 0.3)
        c = [(ux - w / 2, uy - w / 2), (ux + w / 2, uy - w / 2), (ux + w / 2, uy + w / 2), (ux - w / 2, uy + w / 2)]
        for i in range(4):
            sk = [(w / 2 - 1.6, w / 2 + 1.6, z + hgt + 1)] if i == 0 else []
            stone_face(A1, c[i], c[(i + 1) % 4], z, hgt, 0.0, tones(AND), rnd, 0.5, 1.0, 0.25, 0.18, 0, (0.04, 0.1), 0.1, sk)
        z += hgt
    n = 10
    for j in range(n):
        ys, ye = uy - 12 - (n - j) * 0.9, uy - 5.25
        A1.box(shade(AND, 0.12), ux, (ys + ye) / 2, 0.3, 3.4, ye - ys, 4.8 * (j + 1) / n)
    A2.box(GOLD, ux + 1.2, uy + 1.0, z, 1.6, 1.2, 0.6)
    A2.box(GOLD, ux + 1.2, uy + 1.55, z + 0.6, 1.6, 0.25, 0.9)
    A2.cyl(DARK, ux - 1.6, uy - 0.8, z, 0.9, 0.12, 12)
    A2.box(DARK, ux - 1.6, uy - 3.0, z - 0.02, 0.35, 4.4, 0.1)
    A1.box(shade(AND, -0.2), ux - 6, uy - 28, 0.3, 0.6, 32, 0.08)                     # drain toward the Saphy
    # stone benches along the edges, poles with feather standards, standing huaca stones
    for i in range(10):
        A1.box(shade(AND, 0.08), -80 + i * 17.5, 58, 0.3, 9, 1.2, 0.6)
        A1.box(shade(AND, 0.08), -80 + i * 17.5, -58, 0.3, 9, 1.2, 0.6)
    for i, (px, py) in enumerate(((-40, 20), (-10, 30), (30, 25), (60, 0), (-60, -10), (40, -35), (-30, -40))):
        A2.cyl(TIMBER, px, py, 0.3, 0.12, 7, 6)
        A2.box(["#A33A2A", "#D2A63C", "#3E6A8A"][i % 3], px + 0.6, py, 5.2, 1.2, 0.1, 1.8)
    for px, py in ((-70, 40), (70, -40), (-20, 50)):
        A1.cyl(shade(AND, 0.1), px, py, 0.3, 0.7, 1.8, 7, 0.5)
    # a crowd for the feast: lords and attendants, litters of the dead kings
    for i in range(40):
        figure(A2, rnd.uniform(-70, 70), rnd.uniform(-50, 50), 0.3, rnd.choice(["#A33A2A", "#D7C7A0", "#3E5A7A", "#7A5A3C", "#C9A24A"]))
    for i in range(6):
        lx, ly = -50 + i * 14, 40
        A2.box(TIMBER, lx, ly, 0.9, 3.4, 1.2, 0.2)
        A2.box(["#C9A24A", "#A33A2A"][i % 2], lx, ly, 1.1, 1.3, 1.0, 1.4)
        figure(A2, lx - 2, ly, 0.3, "#7A5A3C")
        figure(A2, lx + 2, ly, 0.3, "#7A5A3C")
    m.add(0, A0.build(), "plaza")
    m.add(1, A1.build(), "ushnu")
    m.add(2, A2.build(), "feast")
    return m


def plaza_1650():
    """The Spanish Plaza de Armas: arcaded houses (portales) over the Inca plaza's edges, a fountain, market stalls."""
    rnd = random.Random(23)
    m = Model("plaza-1650")
    A0, A1, A2 = Acc("pz0"), Acc("pz1"), Acc("pz2")
    A0.box("#CDBB98", 0, 0, 0, 180, 124, 0.3)
    A0.box(shade(PAVE, -0.05), 10, 8, 0.3, 140, 100, 0.06)
    for i in range(-6, 8):
        A0.box(shade(PAVE, -0.15), 10 + i * 10, 8, 0.36, 0.4, 100, 0.03)
    # portales: two-storey arcaded houses on the north-west (-X) and south-west (-Y) sides
    colonial_range(A1, A2, (-84, -40), (-84, 60), 10, 9, rnd, wall=WHITE, inca=AND, inca_h=0, arcade_side=-1, storeys=2, balcony_side=-1, arcade_storeys=1)
    colonial_range(A1, A2, (-78, -55), (88, -55), 10, 9, rnd, wall=WHITE, inca=AND, inca_h=0, arcade_side=1, storeys=2, balcony_side=1, arcade_storeys=1)
    # the fountain
    A1.lathe(shade(CANT, 0.2), 10, 8, 0.3, [(4.5, 0), (4.5, 0.9), (4.0, 0.9)], 16)
    A1.cyl(WATERC, 10, 8, 0.9, 4.0, 0.25, 16)
    A1.lathe(shade(CANT, 0.2), 10, 8, 1.15, [(0.6, 0), (0.45, 2.0), (1.6, 2.4), (1.6, 2.7), (0.3, 2.9), (0.2, 4.0)], 12)
    # picota and a cross
    A1.cyl(shade(CANT, 0.1), 45, 30, 0.3, 0.4, 5, 8)
    cross(A1, -20, 40, 0.3, 2.0, shade(CANT, 0.1))
    # market stalls under cloth awnings, and people
    for i in range(6):
        for j in range(4):
            sx, sy = -40 + i * 8, -30 + j * 7
            A2.box(TIMBER, sx, sy, 0.3, 0.12, 0.12, 2.0)
            A2.roof(CLOTH, sx, sy, 2.3, 3.0, 2.6, 0.7, "x", over=0.2, eave=0.08, ridge=False)
            A2.box(rnd.choice(["#C9A24A", "#A33A2A", "#7E9550", "#D7C7A0"]), sx, sy, 0.3, 2.4, 1.6, 0.6)
    for i in range(30):
        figure(A2, rnd.uniform(-60, 75), rnd.uniform(-40, 50), 0.3, rnd.choice(["#2E2A2A", "#A33A2A", "#D7C7A0", "#3E5A7A", "#7A5A3C"]))
    m.add(0, A0.build(), "plaza")
    m.add(1, A1.build(), "portales")
    m.add(2, A2.build(), "market")
    return m


# ---------------------------------------------------------------- palaces

def kiswarkancha():
    rnd = random.Random(29)
    m = Model("kiswarkancha")
    A0, A1, A2 = Acc("kw0"), Acc("kw1"), Acc("kw2")
    A0.box(EARTH, 0, 0, 0, 100, 85, 0.3)
    # outer wall of fitted stone round the whole block
    fitted_wall(A1, [(-49, -27), (-49, 41), (49, 41), (49, -20)], 0.3, 4.5, 1.2, AND, rnd, faces=(-1,), course=0.8, block=1.8)
    # the great hall opening onto the plaza
    great_hall(A1, A2, -8, -34.5, 0.3, 66, 13, 6.0, rnd, AND, doors=7, door_side=-1, jamb=shade(AND, -0.25))
    # two courts of rooms behind
    kancha_c(A1, A2, -24, 12, 44, 46, rnd, AND, wall_h=3.8, t=0.9, gate="S", sides="NEW", hw=6, hh=3.6, z=0.3, face_out=False)
    kancha_c(A1, A2, 24, 12, 44, 46, rnd, AND, wall_h=3.8, t=0.9, gate="S", sides="NEW", hw=6, hh=3.6, z=0.3, face_out=False)
    # Suntur Wasi, the round tower at the plaza corner
    round_tower(A1, A2, 40, -26, 0.3, 6.0, 8.0, rnd, AND, ICHU, rh=12.0, door="S")
    m.add(0, A0.build(), "ground")
    m.add(1, A1.build(), "walls")
    m.add(2, A2.build(), "roofs")
    return m


def kasana():
    rnd = random.Random(31)
    m = Model("kasana")
    A0, A1, A2 = Acc("ks0"), Acc("ks1"), Acc("ks2")
    A0.box(EARTH, 0, 0, 0, 100, 90, 0.3)
    fitted_wall(A1, [(-49, -24), (-49, 44), (49, 44), (49, -24)], 0.3, 4.6, 1.2, AND, rnd, faces=(-1,), course=0.8, block=1.8)
    great_hall(A1, A2, 0, -33, 0.3, 90, 18, 7.0, rnd, AND, doors=9, door_side=-1, rh=13.0, jamb=shade(AND, -0.25))
    kancha_c(A1, A2, -23, 15, 46, 52, rnd, AND, wall_h=3.8, t=0.9, gate="S", sides="NSW", hw=6, hh=3.6, z=0.3, face_out=False)
    kancha_c(A1, A2, 23, 15, 46, 52, rnd, AND, wall_h=3.8, t=0.9, gate="S", sides="NSE", hw=6, hh=3.6, z=0.3, face_out=False)
    for i in range(8):
        figure(A1, -40 + i * 11, -44.2, 0.3, "#A33A2A" if i % 2 else "#D7C7A0")
    m.add(0, A0.build(), "ground")
    m.add(1, A1.build(), "walls")
    m.add(2, A2.build(), "roofs")
    return m


def serpent(acc, x, y, z, length, face="S", color=shade(AND, 0.2)):
    n = 8
    for i in range(n):
        s = -length / 2 + length * (i + 0.5) / n
        dz = 0.35 * math.sin(i * 1.3)
        acc.box(color, x + s, y - 0.1, z + dz, length / n * 1.1, 0.3, 0.35)
    acc.box(color, x + length / 2 + 0.2, y - 0.1, z + 0.1, 0.6, 0.35, 0.5)


def amarukancha():
    rnd = random.Random(37)
    m = Model("amarukancha")
    A0, A1, A2 = Acc("am0"), Acc("am1"), Acc("am2")
    A0.box(EARTH, 0, 0, 0, 72, 90, 0.3)
    ring = [(-35, -44), (35, -44), (35, 44), (-35, 44)]
    fitted_wall(A1, ring, 0.3, 4.6, 1.2, AND, rnd, closed=True, course=0.8, block=1.8, skips={1: [(35 - 2.5, 35 + 2.5, 5)]})
    A1.trap(shade(AND, -0.3), 0, -44.6, 0.3, 3.4, 2.6, 4.0, "S", 0.6)
    A1.trap(DARK, 0, -44.7, 0.3, 2.3, 1.8, 3.5, "S", 0.7)
    for s in (-1, 1):
        A1.push(s * 5.5, -44.75, 0)
        serpent(A1, 0, 0, 2.2, 4.0)
        A1.pop()
    great_hall(A1, A2, 0, -28, 0.3, 58, 14, 6.5, rnd, AND, doors=6, door_side=-1, rh=10.5, jamb=shade(AND, -0.25))
    kancha_c(A1, A2, -16, 16, 32, 50, rnd, AND, wall_h=3.8, t=0.9, gate="S", sides="NEW", hw=6, hh=3.6, z=0.3, face_out=False)
    kancha_c(A1, A2, 16, 16, 32, 50, rnd, AND, wall_h=3.8, t=0.9, gate="S", sides="NEW", hw=6, hh=3.6, z=0.3, face_out=False)
    m.add(0, A0.build(), "ground")
    m.add(1, A1.build(), "walls")
    m.add(2, A2.build(), "roofs")
    return m


def aqllawasi():
    rnd = random.Random(41)
    m = Model("aqllawasi")
    A0, A1, A2 = Acc("aq0"), Acc("aq1"), Acc("aq2")
    A0.box(EARTH, 0, 0, 0, 90, 76, 0.3)
    ring = [(-44, -37), (44, -37), (44, 37), (-44, 37)]
    fitted_wall(A1, ring, 0.3, 6.5, 1.4, AND, rnd, closed=True, course=0.75, block=1.6, skips={1: [(44 - 2.5, 44 + 2.5, 5)]})
    A1.trap(shade(AND, -0.3), 0, -37.7, 0.3, 3.4, 2.6, 4.2, "S", 0.6)
    A1.trap(DARK, 0, -37.8, 0.3, 2.3, 1.8, 3.7, "S", 0.7)
    # long halls of looms and brewing rooms round two courts
    for cx in (-21, 21):
        kancha_c(A1, A2, cx, 0, 38, 66, rnd, AND, wall_h=3.6, t=0.8, gate="S" if cx < 0 else "W", sides="NSEW", hw=7, hh=3.8, z=0.3, face_out=False, frac=0.85)
    for i in range(6):
        figure(A1, -30 + i * 4, -6 + (i % 2) * 3, 0.42, "#D7C7A0")
    for i in range(8):
        A1.cyl("#B4704E", 15 + (i % 4) * 2.4, -6 + (i // 4) * 2.4, 0.42, 0.6, 1.0, 8, 0.25)
    m.add(0, A0.build(), "ground")
    m.add(1, A1.build(), "walls")
    m.add(2, A2.build(), "roofs")
    return m


def santa_catalina():
    rnd = random.Random(43)
    m = Model("santa-catalina")
    A0, A1, A2 = Acc("sc0"), Acc("sc1"), Acc("sc2")
    A0.box(EARTH, 0, 0, 0, 90, 76, 0.3)
    # the Inca enclosure walls carry the convent's whitewashed upper walls
    ring = [(-44, -37), (44, -37), (44, 37), (-44, 37)]
    fitted_wall(A1, ring, 0.3, 4.2, 1.4, AND, rnd, closed=True, course=0.75, block=1.6)
    for i in range(4):
        a, b = ring[i], ring[(i + 1) % 4]
        A1.seg(WHITE, a, b, 4.5, 1.1, 3.5, ext=1.1)
    # the church along the street, bell gable at its west end
    A1.push(-6, -28, 0)
    A1.box(WHITE, 0, 0, 0.3, 56, 12, 14)
    A1.box(CANT_L, 0, 0, 14.3, 56.8, 12.6, 0.5)
    for i in range(6):
        A1.arch(DARK, -24 + i * 9.6, -6.05, 7.5, 1.4, 3.0, "S", 0.25)
    retable(A1, -8, -6, 0.3, 8, 11, CANT_L, 2)
    A1.box(WHITE, -26.5, 0, 14.3, 3, 8, 6)
    for k in (-1.6, 1.6):
        A1.arch(DARK, -26.5 - 1.6, k, 16.0, 1.2, 2.4, "W", 0.4)
    cross(A1, -26.5, 0, 20.3, 1.2)
    A1.pop()
    A2.roof(TILE, -6, -28, 14.8, 56, 12, 4.0, "x", over=0.4, eave=0.25)
    # cloister ranges
    for a, b in (((-30, -12), (30, -12)), ((30, -12), (30, 31)), ((30, 31), (-30, 31)), ((-30, 31), (-30, -12))):
        colonial_range(A1, A2, a, b, 7, 8, rnd, wall=WHITE, arcade_side=1, storeys=2)
    for i in range(6):
        cone_tree(A1, -20 + i * 8, 9 + (i % 2) * 4, 0.3, 1.8)
    A1.lathe(shade(CANT, 0.2), 0, 10, 0.3, [(1.8, 0), (1.8, 0.7), (1.5, 0.7)], 12)
    m.add(0, A0.build(), "ground")
    m.add(1, A1.build(), "walls")
    m.add(2, A2.build(), "roofs")
    return m


def hatunkancha():
    rnd = random.Random(47)
    m = Model("hatunkancha")
    A0, A1, A2 = Acc("hc0"), Acc("hc1"), Acc("hc2")
    A0.box(EARTH, 0, 0, 0, 90, 80, 0.3)
    ring = [(-44, -39), (44, -39), (44, 39), (-44, 39)]
    fitted_wall(A1, ring, 0.3, 5.0, 1.3, AND, rnd, closed=True, course=0.8, block=1.7, skips={1: [(44 - 2.5, 44 + 2.5, 5)]})
    A1.trap(shade(AND, -0.3), 0, -39.7, 0.3, 3.4, 2.6, 4.2, "S", 0.6)
    A1.trap(DARK, 0, -39.8, 0.3, 2.3, 1.8, 3.7, "S", 0.7)
    A1.box(PAVE, 0, 0, 0.3, 4, 76, 0.1)
    A1.box(PAVE, 0, 0, 0.3, 86, 4, 0.1)
    for cx in (-22, 22):
        for cy in (-19.5, 19.5):
            kancha_c(A1, A2, cx, cy, 38, 33, rnd, AND, wall_h=3.4, t=0.8, gate="S" if cy > 0 else "N", sides="NS" if cx < 0 else "NSE", hw=6, hh=3.4, z=0.3, face_out=False, doors=2)
    m.add(0, A0.build(), "ground")
    m.add(1, A1.build(), "walls")
    m.add(2, A2.build(), "roofs")
    return m


def pucamarca():
    rnd = random.Random(53)
    m = Model("pucamarca")
    A0, A1, A2 = Acc("pk0"), Acc("pk1"), Acc("pk2")
    A0.box(EARTH, 0, 0, 0, 70, 56, 0.3)
    kancha_c(A1, A2, 0, -2, 68, 52, rnd, AND, wall_h=4.4, t=1.2, gate="S", sides="SEW", hw=7, hh=3.8, z=0.3, face_out=True, inner=RED_PL)
    # the shrine raised at the back of the court
    A1.box(shade(AND, 0.06), 0, 14, 0.3, 26, 12, 1.6)
    stone_face(A1, (-13, 8), (13, 8), 0.3, 1.6, 0.0, tones(AND), rnd, 0.55, 1.2, 0.2, 0.15, 0, (0.04, 0.1))
    for j in range(5):
        A1.box(shade(AND, 0.1), 0, 8 - 2.5 + j * 0.5, 0.3, 3.0, 0.5 * (5 - j) + 0.0, 0.32 * (j + 1))
    inca_house(A1, 0, 15, 1.9, 20, 8, 4.2, "x", -1, 1, RED_PL, rnd=rnd, door_w=1.5, jamb=shade(AND, -0.2), niches=2)
    inca_roof(A2, 0, 15, 1.9, 20, 8, 4.2, "x", rh=6.0)
    m.add(0, A0.build(), "ground")
    m.add(1, A1.build(), "walls")
    m.add(2, A2.build(), "roofs")
    return m


def kusicancha():
    rnd = random.Random(59)
    m = Model("kusicancha")
    A0, A1, A2 = Acc("ku0"), Acc("ku1"), Acc("ku2")
    A0.box(EARTH, 0, 0, 0, 70, 60, 0.3)
    for i, cx in enumerate((-23, 0, 23)):
        kancha_c(A1, A2, cx, 0, 20, 56, rnd, AND, wall_h=3.6, t=0.8, gate="S" if i != 1 else "N", sides="NSEW", hw=5, hh=3.2, z=0.3, face_out=True, frac=0.85, doors=1,
                 block=1.2, course=0.6)
    m.add(0, A0.build(), "ground")
    m.add(1, A1.build(), "walls")
    m.add(2, A2.build(), "roofs")
    return m


def hatun_rumiyoc(colonial=False):
    rnd = random.Random(61)
    m = Model("hatun-rumiyoc" + ("-1650" if colonial else ""))
    A0, A1, A2 = Acc("hr0"), Acc("hr1"), Acc("hr2")
    A0.box(EARTH, 0, 0, 0, 70, 70, 0.3)
    # the street wall of polygonal diorite with the twelve-angled stone
    t, h = 1.6, 4.2 if not colonial else 4.0
    A1.seg(shade(DIOR, -0.4), (-34, -34), (34, -34), 0.3, t, h, t - 0.4, ext=t)
    stone_face(A1, (-34, -34), (34, -34), 0.3, h, t / 2, tones(DIOR, 0.08), rnd, course=1.05, block=1.6, jit=0.4, cham=0.3, slope=0.35, proud=(0.08, 0.2), batter=0.05,
               skip=[(34 - 1.8, 34 + 1.8, 4.0), (34 + 9 - 0.9, 34 + 9 + 0.9, 3.0)])
    # the twelve-angled stone
    pts = [(math.cos(math.tau * i / 12 + 0.2) * (0.95 + 0.25 * (i % 2)) * 0.95, math.sin(math.tau * i / 12 + 0.2) * (0.85 + 0.2 * ((i + 1) % 2)) * 0.8) for i in range(12)]
    A1.panel(shade(DIOR, 0.12), [(9 + px, 2.0 + pz) for px, pz in pts], 0, -34 - t / 2 + 0.05 * 2.0, 0.3, "S", 0.7)
    A1.trap(shade(DIOR, -0.25), 0, -34 - t / 2 + 0.1, 0.3, 3.0, 2.3, 3.6, "S", 0.6)
    A1.trap(DARK, 0, -34 - t / 2 + 0.05, 0.3, 2.1, 1.6, 3.1, "S", 0.7)
    for a, b in (((34, -34), (34, 34)), ((34, 34), (-34, 34)), ((-34, 34), (-34, -34))):
        fitted_wall(A1, [a, b], 0.3, 3.8, 1.1, AND, rnd, course=0.75, block=1.5)
    if not colonial:
        for (x, y, L, W, ax, ds) in ((0, -26, 50, 7, "x", 1), (0, 26, 50, 7, "x", -1), (-26, 0, 30, 7, "y", 1), (26, 0, 30, 7, "y", -1)):
            inca_house(A1, x, y, 0.3, L, W, 3.8, ax, ds, 3, AND, rnd=rnd, faced=True)
            inca_roof(A2, x, y, 0.3, L, W, 3.8, ax)
        A1.box(SAND, 0, 0, 0.3, 40, 40, 0.1)
    else:
        # the colonial mansion on the Inca walls: an upper storey with a long balcony over the street, ranges round a patio
        A1.seg(WHITE, (-34, -34), (34, -34), h + 0.3, t - 0.3, 4.2, ext=t)
        for i in range(10):
            A1.box(DARK, -30 + i * 6.6, -34 - (t - 0.3) / 2 - 0.02, h + 1.4, 1.2, 0.2, 2.1)
        A1.box(WOOD, -8, -34 - 1.1, h + 1.0, 30, 0.9, 0.3)
        A1.box(WOOD, -8, -34 - 1.1, h + 1.3, 30, 0.9, 1.4)
        for i in range(10):
            A1.box(shade(WOOD, -0.25), -21.5 + i * 3, -34 - 1.57, h + 1.5, 2.2, 0.1, 1.0)
        A2.box(TILE, -8, -34 - 1.0, h + 3.2, 31, 1.2, 0.3)
        for a, b in (((-26, -26), (26, -26)), ((29, -26), (29, 26)), ((29, 29), (-29, 29)), ((-29, 26), (-29, -26))):
            colonial_range(A1, A2, a, b, 8, 8.5, rnd, wall=WHITE, arcade_side=1, storeys=2)
        A1.lathe(shade(CANT, 0.2), 0, 0, 0.3, [(1.6, 0), (1.6, 0.7), (1.3, 0.7)], 12)
    m.add(0, A0.build(), "ground")
    m.add(1, A1.build(), "walls")
    m.add(2, A2.build(), "roofs")
    return m


# ---------------------------------------------------------------- shrines and storehouses

def blob_pts(rx, ry, seed, n=22, k=0.18):
    r = random.Random(seed)
    ph = [r.uniform(0, 6) for _ in range(3)]
    return [(rx * (1 + k * math.sin(3 * a + ph[0]) + k * 0.6 * math.cos(5 * a + ph[1])) * math.cos(a),
             ry * (1 + k * math.sin(2 * a + ph[2]) + k * 0.5 * math.cos(4 * a + ph[0])) * math.sin(a)) for a in [math.tau * i / n for i in range(n)]]


def qenqo():
    rnd = random.Random(67)
    m = Model("qenqo")
    A0, A1, A2 = Acc("qq0"), Acc("qq1"), Acc("qq2")
    A0.box(GRASS, 0, 0, 0, 60, 50, 0.3)
    ROCK = "#B9AF9A"
    # the outcrop: stacked irregular masses
    for k, (rx, ry, h, ox, oy) in enumerate(((22, 14, 3.0, 0, 8), (18, 11, 2.6, -1, 9), (13, 8, 2.2, 1, 10), (8, 5, 1.6, 0, 10))):
        pts = [(x + ox, y + oy) for x, y in blob_pts(rx, ry, 70 + k)]
        top = [(ox + x * 0.93, oy + y * 0.93) for x, y in blob_pts(rx, ry, 70 + k)]
        A0.prism(shade(ROCK, -0.04 * k), pts, 0.3 + sum(t[2] for t in ((22, 14, 3.0), (18, 11, 2.6), (13, 8, 2.2), (8, 5, 1.6))[:k]), h, top)
    ztop = 0.3 + 3.0 + 2.6 + 2.2 + 1.6
    # zigzag libation channel down the top
    zz = [(-4, 13), (-1.5, 11.5), (-3.5, 10), (-1, 8.5), (-3, 7), (-0.5, 5.5)]
    for i in range(1, len(zz)):
        A1.seg(DARK, zz[i - 1], zz[i], ztop - 0.05, 0.3, 0.12, ext=0.3)
    # carved steps and seats, the cave mouth
    for j in range(5):
        A1.box(shade(ROCK, 0.08), 12 + j * 0.0, 2 + j * 1.0, 0.3, 4, 1.0, 1.2 * (j + 1))
    A1.trap(DARK, -8, -6.8, 0.3, 3.0, 2.4, 2.2, "S", 1.6)
    A1.box(shade(ROCK, 0.1), -6, -3, 0.3, 2.4, 1.2, 1.0)
    # the semicircle of niched walls round the standing stone
    for i in range(14):
        a0 = math.pi + math.pi * i / 14
        a1 = math.pi + math.pi * (i + 1) / 14
        p0 = (14 * math.cos(a0), -6 + 14 * math.sin(a0))
        p1 = (14 * math.cos(a1), -6 + 14 * math.sin(a1))
        fitted_wall(A1, [p1, p0], 0.3, 2.4, 1.1, AND, rnd, faces=(1, -1), course=0.6, block=1.2, proud=(0.03, 0.08))
        am = (a0 + a1) / 2
        A1.box(shade(AND, -0.45), 13.3 * math.cos(am), -6 + 13.3 * math.sin(am), 1.0, 0.8, 0.4, 1.0, am + math.pi / 2)
    A2.box(shade(ROCK, -0.05), 0, -9, 0.3, 2.4, 2.4, 1.0)
    A2.box(ROCK, 0, -9, 1.3, 1.8, 1.4, 5.0, 0.1, 1.2, 1.0)
    for i in range(5):
        figure(A2, rnd.uniform(-10, 10), rnd.uniform(-16, -12), 0.3, rnd.choice(["#A33A2A", "#D7C7A0", "#7A5A3C"]))
    m.add(0, A0.build(), "rock")
    m.add(1, A1.build(), "walls")
    m.add(2, A2.build(), "stone")
    return m


def qollqampata():
    rnd = random.Random(71)
    m = Model("qollqampata")
    A0, A1, A2 = Acc("qp0"), Acc("qp1"), Acc("qp2")
    A0.box(EARTH, 0, 0, 0, 100, 70, 0.3)
    z = 0.3
    tiers = [(-32.2, -20, 2.4), (-20, -5, 2.4), (-5, 12, 2.4), (12, 35, 2.4)]
    for k, (y0, y1, h) in enumerate(tiers):
        A0.box(shade(EARTH, -0.04 * k), 0, (y0 + 35) / 2, z, 98, 35 - y0, h)
        stone_face(A0, (-49, y0), (49, y0), z, h, 0.0, tones(FIELD), rnd, 0.6, 1.1, 0.35, 0.25, 0.15, (0.04, 0.12), skip=[(49 - 2.5, 49 + 2.5, z + h + 1)])
        for j in range(6):
            A0.box(shade(FIELD, 0.12), 0, y0 - (6 - j) * 0.45 + 0.225, z, 3.4, 0.45, h * (j + 1) / 6)
        z += h
        if k < 2:
            maize_rows(A1, -46, 46, y0 + 2, y1 - 2, z, 2.6, MAIZE, 1.3)
    # rows of storehouses on the upper tiers: round on one, rectangular on the other
    zr = 0.3 + 2.4 * 3
    for i in range(10):
        x = -42 + i * 9.3
        if abs(x) < 4:
            continue
        A1.cyl(FIELD, x, 3.5, zr, 2.4, 3.0, 12)
        A1.trap(DARK, x, 3.5 - 2.4, zr + 1.0, 0.7, 0.55, 0.8, "S", 0.4)
        A2.lathe(ICHU, x, 3.5, zr + 3.0, [(2.9, 0), (0.12, 3.3)], 12)
    zr2 = zr + 2.4
    for i in range(6):
        x = -40 + i * 16
        if abs(x) < 4:
            x += 6
        inca_house(A1, x, 24, zr2, 11, 5, 3.0, "x", -1, 1, FIELD, rnd=rnd, door_w=0.8)
        inca_roof(A2, x, 24, zr2, 11, 5, 3.0, "x")
    for i in range(4):
        figure(A1, -10 + i * 6, -1, zr, "#D7C7A0" if i % 2 else "#7A5A3C")
    m.add(0, A0.build(), "terraces")
    m.add(1, A1.build(), "storehouses")
    m.add(2, A2.build(), "roofs")
    return m


# ---------------------------------------------------------------- churches of the Spanish city

def cathedral():
    rnd = random.Random(73)
    m = Model("cathedral")
    A0, A1, A2, A3 = Acc("ct0"), Acc("ct1"), Acc("ct2"), Acc("ct3")
    A0.box(EARTH, 0, 0, 0, 100, 85, 0.3)
    # the raised atrium with steps down to the plaza
    A0.box(shade(CANT, 0.2), 0, -34.25, 0.3, 74, 8.5, 1.4)
    for j in range(3):
        A0.box(shade(CANT, 0.25), 0, -39.0 - j, 0.3, 74 - 2 * j, 1.0, 1.4 * (3 - j) / 4)
    # main church: three naves, two squat towers, ashlar front with three portals
    A1.push(0, 6, 0)
    church(A1, 70, 46, 17, rnd, color=CANT, trim=CANT_L, roof=TILE, towers=2, tw=10, th=30, aisles=13, portals=3, retable_w=15, belfry_storeys=1, front_h=22, z=0.3,
           cupola_color=CANT_L)
    A1.pop()
    # El Triunfo on the south-east, with its small dome; a lower chapel on the north-west
    A2.push(36, 2, 0)
    church(A2, 60, 18, 12, rnd, color=CANT, trim=CANT_L, towers=0, front_h=14, retable_w=7, dome_r=5.0, dome_at=0.5, ashlar=True, balus=False, z=0.3)
    A2.pop()
    A2.push(-35, 4, 0)
    church(A2, 54, 16, 10, rnd, color=shade(CANT, 0.05), trim=CANT_L, towers=0, front_h=11, retable_w=6, ashlar=False, balus=False, z=0.3)
    A2.pop()
    # pinnacles on the front and atrium cross
    for x in (-15, -8, 8, 15):
        pinnacle(A3, x, -28.0, 22.8, 0.9, CANT_L)
    cross(A3, -26, -35, 1.7, 2.4, CANT_L)
    for i in range(10):
        figure(A3, rnd.uniform(-30, 30), rnd.uniform(-37, -31), 1.7, rnd.choice(["#2E2A2A", "#A33A2A", "#D7C7A0", "#3E5A7A"]))
    m.add(0, A0.build(), "atrium")
    m.add(1, A1.build(), "cathedral")
    m.add(2, A2.build(), "chapels")
    m.add(3, A3.build(), "pinnacles")
    return m


def la_compania():
    rnd = random.Random(79)
    m = Model("la-compania")
    A0, A1, A2 = Acc("lc0"), Acc("lc1"), Acc("lc2")
    A0.box(EARTH, 0, 0, 0, 44, 75, 0.3)
    A0.box(shade(CANT, 0.2), 0, -34, 0.3, 40, 6, 0.9)
    A1.push(-2, 2, 0)
    church(A1, 66, 24, 18, rnd, color=CANT, trim=CANT_L, roof=TILE, towers=2, tw=7.5, th=46, dome_r=6.5, dome_at=0.7, portals=1, retable_w=11.5, belfry_storeys=2,
           front_h=27, z=0.3, cupola_color=CANT_L, balus=True)
    A1.pop()
    # the chapel of Lourdes beside it
    A2.push(17, 6, 0)
    church(A2, 40, 9, 10, rnd, color=shade(CANT, 0.05), trim=CANT_L, towers=0, front_h=12, retable_w=5, ashlar=False, balus=False, z=0.3)
    A2.pop()
    m.add(0, A0.build(), "ground")
    m.add(1, A1.build(), "church")
    m.add(2, A2.build(), "chapel")
    return m


def san_francisco():
    rnd = random.Random(83)
    m = Model("san-francisco")
    A0, A1, A2 = Acc("sf0"), Acc("sf1"), Acc("sf2")
    A0.box(EARTH, 0, 0, 0, 70, 80, 0.3)
    A1.push(-18, 0, 0)
    church(A1, 72, 20, 15, rnd, color=CANT, trim=CANT_L, towers=1, tw=9, th=40, portals=1, retable_w=8, belfry_storeys=1, front_h=19, z=0.3, balus=False)
    A1.pop()
    for a, b in (((-3.5, -26), (30.5, -26)), ((30.5, -26), (30.5, 26)), ((30.5, 26), (-3.5, 26)), ((-3.5, 26), (-3.5, -26))):
        colonial_range(A1, A2, a, b, 8, 9, rnd, wall=WHITE, arcade_side=1, storeys=2)
    for i in range(4):
        cone_tree(A1, 6 + i * 6, -2 + (i % 2) * 6, 0.3, 2.0)
    A1.lathe(shade(CANT, 0.2), 13, 0, 0.3, [(1.6, 0), (1.6, 0.7), (1.3, 0.7)], 12)
    m.add(0, A0.build(), "ground")
    m.add(1, A1.build(), "church")
    m.add(2, A2.build(), "roofs")
    return m


def san_blas():
    rnd = random.Random(89)
    m = Model("san-blas")
    A0, A1, A2 = Acc("sb0"), Acc("sb1"), Acc("sb2")
    A0.box(EARTH, 0, 0, 0, 24, 44, 0.3)
    A0.box(PAVE, 0, -17, 0.3, 22, 9, 0.2)
    for a, b in (((-11, -21.5), (-3, -21.5)), ((3, -21.5), (11, -21.5))):
        A0.seg(WHITE, a, b, 0.3, 0.6, 1.0, ext=0.6)
    cross(A0, 0, -18, 0.5, 1.2, shade(CANT, 0.2))
    # adobe nave on a stone plinth, tile roof, a bell gable over the door
    A1.box(FIELD, 0, 4, 0.3, 11, 30, 1.4)
    for a, b in (((-5.5, -11), (5.5, -11)), ((5.5, -11), (5.5, 19)), ((5.5, 19), (-5.5, 19)), ((-5.5, 19), (-5.5, -11))):
        stone_face(A1, a, b, 0.3, 1.4, 0.0, tones(FIELD), rnd, 0.45, 0.8, 0.35, 0.25, 0.2, (0.03, 0.08))
    for a, b in (((-11, -21.5), (-11, -12.5)), ((11, -12.5), (11, -21.5))):
        A0.seg(WHITE, a, b, 0.3, 0.6, 1.0, ext=0.6)
    cone_tree(A0, -7.5, -15, 0.5, 2.2)
    cone_tree(A0, 8.5, -15, 0.5, 2.0)
    A1.box(WHITE, 0, 4, 1.7, 10.6, 29.6, 6.6)
    A1.arch(DARK, 0, -11.05, 0.3, 2.4, 4.2, "S", 0.4)
    A1.box(CANT_L, 0, -11.2, 4.7, 3.6, 0.4, 0.4)
    for i in range(4):
        for s in (-1, 1):
            A1.box(DARK, s * 5.32, -6 + i * 6, 5.0, 0.3, 0.9, 1.5)
    A2.roof(TILE, 0, 4, 8.3, 30, 10.6, 3.2, "y", over=0.5, eave=0.2)
    A2.box(WHITE, 0, -10.6, 8.3, 6.0, 1.0, 4.4)
    A2.gable_end(WHITE, 0, -10.6, 12.7, 6.0, 1.6, "y", 1.0)
    for s in (-1.3, 1.3):
        A2.arch(DARK, s, -11.15, 10.0, 1.1, 2.2, "S", 0.3)
    cross(A2, 0, -10.6, 14.3, 0.9)
    A1.box(WHITE, 7.8, 10, 0.3, 5, 9, 4.0)
    A2.roof(TILE, 7.8, 10, 4.3, 9, 5, 1.6, "y", over=0.3, eave=0.15)
    m.add(0, A0.build(), "atrium")
    m.add(1, A1.build(), "nave")
    m.add(2, A2.build(), "roof")
    return m


BUILDERS = {
    "cusco/coricancha": coricancha,
    "cusco/inticancha": inticancha,
    "cusco/santo-domingo": santo_domingo,
    "cusco/sacsayhuaman": lambda: sacsayhuaman("1530"),
    "cusco/sacsayhuaman-1470": lambda: sacsayhuaman("1470"),
    "cusco/sacsayhuaman-ruin": lambda: sacsayhuaman("ruin"),
    "cusco/haukaypata": haukaypata,
    "cusco/plaza-1650": plaza_1650,
    "cusco/kiswarkancha": kiswarkancha,
    "cusco/cathedral": cathedral,
    "cusco/kasana": kasana,
    "cusco/amarukancha": amarukancha,
    "cusco/la-compania": la_compania,
    "cusco/aqllawasi": aqllawasi,
    "cusco/santa-catalina": santa_catalina,
    "cusco/hatunkancha": hatunkancha,
    "cusco/pucamarca": pucamarca,
    "cusco/kusicancha": kusicancha,
    "cusco/hatun-rumiyoc": hatun_rumiyoc,
    "cusco/hatun-rumiyoc-1650": lambda: hatun_rumiyoc(True),
    "cusco/qenqo": qenqo,
    "cusco/qollqampata": qollqampata,
    "cusco/san-francisco": san_francisco,
    "cusco/san-blas": san_blas,
}
