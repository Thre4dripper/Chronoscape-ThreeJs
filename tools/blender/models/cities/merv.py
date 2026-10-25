"""Merv landmark miniatures: Erk Kala, the walls of Gyaur Kala and Sultan Kala, Sanjar's mausoleum, the Shahriyar Ark,
the corrugated koshks (Kyz Kala), the ice houses and the Timurid town.

Conventions as in FORMAT.md: metres, origin at the ground centre, +X east, +Y north, main front toward -Y unless a
builder says otherwise; the landmark rotation turns it on the map. Geometry is gathered per colour in a Batch (as in
the Samarkand module) so that thousands of towers, merlons, corrugations and brick panels stay cheap.
"""
import math
from chronokit import Model, box, cylinder, dome, join, shade, mesh_from
from worldkit import *

# ---------------------------------------------------------------- palette
MUD, MUD_LT, MUD_DK = "#C3A278", "#D2B68C", "#A88B63"      # mud brick and pakhsa
ERODED = "#BFA47E"
BRICK_S, BRICK_SL, BRICK_SD = "#C49A6C", "#D6B386", "#A47E56"   # Seljuk fired brick
TURQ, TURQ_LT, COBALT, TWHITE = "#2C9FAF", "#5CBEC6", "#23428F", "#EEEADF"
DEEP = "#1F2F5C"
GROUND, PAVE, PAVE_DK = "#D8C49C", "#D6C3A0", "#BFA982"
LEAF, LEAF_DK = "#6F8C55", "#5D7A48"
WOOD, WOOD_DK = "#8A6744", "#6A4E33"
WATER_C = "#5F8E94"
STRAW = "#C9B26E"
DOOR = DARK


# ---------------------------------------------------------------- mesh batch (after samarkand.py)

class Batch:
    """Collects geometry per colour and builds one joined object."""

    def __init__(self, name):
        self.name = name
        self.g = {}

    def add(self, c, verts, faces):
        V, F = self.g.setdefault(c, ([], []))
        o = len(V)
        V.extend(verts)
        F.extend(tuple(i + o for i in f) for f in faces)

    def box(self, c, x, y, z, w, d, h, rz=0.0):
        cs, sn = math.cos(rz), math.sin(rz)
        pts = [(-w / 2, -d / 2), (w / 2, -d / 2), (w / 2, d / 2), (-w / 2, d / 2)]
        V = [(x + px * cs - py * sn, y + px * sn + py * cs, zz) for zz in (z, z + h) for px, py in pts]
        self.add(c, V, [(3, 2, 1, 0), (4, 5, 6, 7), (0, 1, 5, 4), (1, 2, 6, 5), (2, 3, 7, 6), (3, 0, 4, 7)])

    def prism(self, c, pts, z, h, x=0.0, y=0.0, top_scale=1.0):
        n = len(pts)
        V = [(x + px, y + py, z) for px, py in pts] + [(x + px * top_scale, y + py * top_scale, z + h) for px, py in pts]
        F = [tuple(range(n))[::-1], tuple(range(n, 2 * n))] + [(i, (i + 1) % n, n + (i + 1) % n, n + i) for i in range(n)]
        self.add(c, V, F)

    def frustum(self, c, x, y, z, w0, d0, w1, d1, h):
        V = [(x - w0 / 2, y - d0 / 2, z), (x + w0 / 2, y - d0 / 2, z), (x + w0 / 2, y + d0 / 2, z), (x - w0 / 2, y + d0 / 2, z),
             (x - w1 / 2, y - d1 / 2, z + h), (x + w1 / 2, y - d1 / 2, z + h), (x + w1 / 2, y + d1 / 2, z + h), (x - w1 / 2, y + d1 / 2, z + h)]
        self.add(c, V, [(3, 2, 1, 0), (4, 5, 6, 7), (0, 1, 5, 4), (1, 2, 6, 5), (2, 3, 7, 6), (3, 0, 4, 7)])

    def seg(self, c, ax, ay, bx, by, z, w0, w1, h, ext=0.0, lean=0.0):
        """A battered wall (or ridge) along a segment: base width w0, top width w1; lean shifts the top inward (+normal)."""
        L = math.hypot(bx - ax, by - ay) or 1e-6
        ux, uy = (bx - ax) / L, (by - ay) / L
        nx, ny = -uy, ux
        a0 = (ax - ux * ext, ay - uy * ext)
        b0 = (bx + ux * ext, by + uy * ext)
        V = []
        for zz, w, sh in ((z, w0, 0.0), (z + h, w1, lean)):
            for (px, py), s in ((a0, -1), (b0, -1), (b0, 1), (a0, 1)):
                V.append((px + nx * (s * w / 2 + sh), py + ny * (s * w / 2 + sh), zz))
        self.add(c, V, [(3, 2, 1, 0), (4, 5, 6, 7), (0, 1, 5, 4), (1, 2, 6, 5), (2, 3, 7, 6), (3, 0, 4, 7)])

    def ramp(self, c, x, y0, y1, w, z, h):
        """A wedge rising from y0 (ground) to y1 (height h), w wide (y1 > y0)."""
        V = [(x - w / 2, y0, z), (x + w / 2, y0, z), (x + w / 2, y1, z), (x - w / 2, y1, z), (x - w / 2, y1, z + h), (x + w / 2, y1, z + h)]
        self.add(c, V, [(3, 2, 1, 0), (0, 1, 5, 4), (1, 2, 5), (3, 0, 4), (2, 3, 4, 5)])

    def panel(self, c, outline, O, ang, depth=0.25, off=0.0):
        """Extrude a flat outline [(u, v)] on a wall plane through O whose outward normal is at angle ang (radians)."""
        nx, ny = math.cos(ang), math.sin(ang)
        ux, uy = -ny, nx
        ox, oy, oz = O
        n = len(outline)
        V = []
        for k in (off, off + depth):
            for u, v in outline:
                V.append((ox + u * ux + nx * k, oy + u * uy + ny * k, oz + v))
        F = [tuple(range(n))[::-1], tuple(range(n, 2 * n))] + [(i, (i + 1) % n, n + (i + 1) % n, n + i) for i in range(n)]
        self.add(c, V, F)

    def rect(self, c, O, ang, u0, u1, v0, v1, depth=0.2, off=0.0):
        self.panel(c, [(u0, v0), (u1, v0), (u1, v1), (u0, v1)], O, ang, depth, off)

    def lathe(self, c, prof, x, y, z, n=24, mod=None, cap_top=True, cap_bottom=True, start=0.0, arc=math.tau):
        closed = abs(arc - math.tau) < 1e-6
        m = n if closed else n + 1
        V, F = [], []
        for k, (r, zz) in enumerate(prof):
            for i in range(m):
                a = start + arc * i / n
                f = mod(a, k / max(1, len(prof) - 1)) if mod else 1.0
                V.append((x + r * f * math.cos(a), y + r * f * math.sin(a), z + zz))
        for k in range(len(prof) - 1):
            for i in range(n):
                j = (i + 1) % m
                F.append((k * m + i, k * m + j, (k + 1) * m + j, (k + 1) * m + i))
        if closed:
            if cap_bottom and prof[0][0] > 1e-4:
                F.append(tuple(range(m))[::-1])
            if cap_top and prof[-1][0] > 1e-4:
                L = len(prof) - 1
                F.append(tuple(L * m + i for i in range(m)))
        elif cap_top and prof[-1][0] > 1e-4:
            L = len(prof) - 1
            # close the half-round top with its chord
            F.append(tuple(L * m + i for i in range(m)))
        self.add(c, V, F)

    def build(self):
        objs = [mesh_from(f"{self.name}_{i}", V, F, (0, 0, 0), c) for i, (c, (V, F)) in enumerate(self.g.items()) if F]
        return join(objs, self.name)


# ---------------------------------------------------------------- transforms and outlines

def _bake(o):
    L = o.location.copy()
    if L.length > 0:
        for v in o.data.vertices:
            v.co += L
        o.location = (0, 0, 0)
    return o


def rz(o, deg):
    """Rotate an object's mesh counter-clockwise about the vertical axis through the origin."""
    _bake(o)
    a = math.radians(deg)
    c, s = math.cos(a), math.sin(a)
    for v in o.data.vertices:
        x, y = v.co.x, v.co.y
        v.co.x, v.co.y = x * c - y * s, x * s + y * c
    o.data.update()
    return o


def mv(o, x=0.0, y=0.0, z=0.0):
    _bake(o)
    for v in o.data.vertices:
        v.co.x += x
        v.co.y += y
        v.co.z += z
    o.data.update()
    return o


def put(o, x=0.0, y=0.0, z=0.0, deg=0.0):
    if deg:
        rz(o, deg)
    return mv(o, x, y, z)


FACING = {"S": 0, "E": 90, "N": 180, "W": -90}
SOUTH, EAST, NORTH, WEST = -math.pi / 2, 0.0, math.pi / 2, math.pi


def ngon(r, n, start=None):
    s = math.pi / n if start is None else start
    return [(r * math.cos(s + k * math.tau / n), r * math.sin(s + k * math.tau / n)) for k in range(n)]


def arch_outline(w, h, R=0.66, n=3):
    """A pointed (two-centred) arch of span w and total height h, as a convex outline."""
    Rr = R * w
    phimax = math.acos((Rr - w / 2) / Rr)
    rise = Rr * math.sin(phimax)
    hr = max(0.0, h - rise)
    right = [(w / 2 - Rr + Rr * math.cos(phimax * i / n), hr + Rr * math.sin(phimax * i / n)) for i in range(n + 1)]
    right[-1] = (0.0, right[-1][1])
    left = [(-x, y) for x, y in reversed(right[:-1])]
    return [(-w / 2, 0.0)] + right + left


def diamond(s):
    return [(0, -s / 2), (s / 2, 0), (0, s / 2), (-s / 2, 0)]


def rnd(i, k=1):
    """A cheap deterministic pseudo-random number in [0, 1)."""
    return ((i * 7919 + k * 104729) % 1000) / 1000.0


# ---------------------------------------------------------------- ornament

def lozenge_field(B, O, ang, u0, u1, v0, v1, step, colors, off=0.0, size=0.62, depth=0.12):
    """Patterned brickwork (hazarbaf) or glazed lozenges in staggered rows."""
    rows = max(1, int((v1 - v0) / step))
    cols = max(1, int((u1 - u0) / step))
    for j in range(rows):
        for i in range(cols):
            u = u0 + (i + 0.5 + (0.5 if j % 2 else 0)) * (u1 - u0) / cols
            if u > u1 - step * 0.3:
                continue
            v = v0 + (j + 0.5) * (v1 - v0) / rows
            B.panel(colors[(i + j) % len(colors)], [(u + x, v + y) for x, y in diamond(step * size)], O, ang, depth, off)


def kufic_band(B, O, ang, u0, u1, v0, v1, ground=BRICK_SD, letter=BRICK_SL, off=0.0, pitch=None):
    """An inscription frieze: a band with upright strokes and a base line."""
    B.rect(ground, O, ang, u0, u1, v0, v1, 0.16, off)
    h = v1 - v0
    pitch = pitch or h * 0.55
    n = max(2, int((u1 - u0) / pitch))
    for i in range(n):
        u = u0 + (i + 0.5) * (u1 - u0) / n
        tall = 0.78 if i % 3 != 1 else 0.45
        B.rect(letter, O, ang, u - pitch * 0.13, u + pitch * 0.13, v0 + h * 0.16, v0 + h * tall, 0.08, off + 0.16)
    B.rect(letter, O, ang, u0 + pitch * 0.2, u1 - pitch * 0.2, v0 + h * 0.12, v0 + h * 0.22, 0.08, off + 0.16)


def kufic_ring(B, x, y, z, h, r, n, ground=COBALT, letter=TWHITE, sides=32):
    B.lathe(ground, [(r * 1.02, 0), (r * 1.02, h)], x, y, z, sides)
    for i in range(n):
        a = math.tau * (i + 0.5) / n
        tall = 0.85 if i % 4 != 2 else 0.5
        w = math.tau * r / n * 0.32
        B.panel(letter, [(-w / 2, h * 0.12), (w / 2, h * 0.12), (w / 2, h * tall), (-w / 2, h * tall)], (x + r * 1.02 * math.cos(a), y + r * 1.02 * math.sin(a), z), a, 0.12)


def pointed_dome(B, r, x, y, z, color, height=1.15, n=48, rings=12, finial=None, bulge=1.0):
    """A slightly pointed Persian dome: profile of two arcs meeting at the apex."""
    prof = []
    for k in range(rings + 1):
        t = k / rings
        a = t * math.pi / 2
        rr = r * math.cos(a) * (1 + (bulge - 1) * math.sin(a * 2))
        zz = r * height * math.sin(a) ** 0.9
        prof.append((rr, zz))
    # sharpen the crown
    prof[-2] = (prof[-2][0] * 0.8, prof[-2][1])
    prof[-1] = (0.0, r * height * 1.04)
    B.lathe(color, prof, x, y, z, n)
    if finial:
        B.lathe(finial, [(r * 0.05, 0), (r * 0.07, r * 0.06), (r * 0.02, r * 0.16), (r * 0.05, r * 0.22), (0.0, r * 0.36)], x, y, z + r * height * 1.02, 8)
    return z + r * height * 1.04


def melon_dome(B, r, x, y, z, ribs=24, height=1.5, color=TURQ, amp=0.06, rings=12, finial=GILT):
    H = r * height
    base = [(1.0, 0.0), (1.06, 0.10), (1.12, 0.24), (1.11, 0.36), (1.06, 0.48), (0.86, 0.60), (0.72, 0.72), (0.55, 0.82), (0.36, 0.91), (0.17, 0.97), (0.0, 1.0)]
    prof = []
    for k in range(rings + 1):
        t = k / rings * (len(base) - 1)
        i = min(int(t), len(base) - 2)
        f = t - i
        prof.append((r * (base[i][0] * (1 - f) + base[i + 1][0] * f), H * (base[i][1] * (1 - f) + base[i + 1][1] * f)))
    prof[-1] = (0.0, H)
    mod = lambda a, t: 1.0 + amp * (2 * abs(math.cos(ribs * a / 2)) - 1.2) * (1 - t * 0.6)
    B.lathe(color, prof, x, y, z, ribs * 4, mod)
    if finial:
        B.lathe(finial, [(r * 0.06, 0), (r * 0.09, r * 0.06), (r * 0.03, r * 0.16), (r * 0.07, r * 0.24), (0.0, r * 0.45)], x, y, z + H - r * 0.02, 8)
    return z + H


def tree_b(B, x, y, z, r, kind="round", color=LEAF):
    B.box(WOOD_DK, x, y, z, r * 0.25, r * 0.25, r * 1.3)
    if kind == "poplar":
        B.lathe(color, [(r * 0.15, 0), (r * 0.5, r * 0.8), (r * 0.42, r * 2.6), (0.0, r * 3.8)], x, y, z + r * 0.8, 6)
    else:
        B.lathe(color, [(r * 0.2, 0), (r * 0.95, r * 0.45), (r * 0.9, r * 1.2), (r * 0.45, r * 1.7), (0.0, r * 1.85)], x, y, z + r * 0.9, 7)


def flat_houses(B, specs, z=0.3, color=MUD, door_ang=SOUTH):
    """Plain flat-roofed houses: (x, y, w, d, h)."""
    for i, (x, y, w, d, h) in enumerate(specs):
        c = [color, shade(color, 0.08), shade(color, -0.07)][i % 3]
        B.box(c, x, y, z, w, d, h)
        B.box(shade(c, -0.12), x, y, z + h, w + 0.3, d + 0.3, 0.35)
        oy = y - d / 2 if door_ang == SOUTH else y + d / 2
        B.rect(DOOR, (x, oy, z), door_ang, -0.6, 0.6, 0, 2.0, 0.1)


def house_grid(B, x0, y0, x1, y1, seed=0, cell=11.0, hmin=3.0, hmax=5.5, color=MUD, z=0.3):
    """Courtyard houses packed in a rectangle: each an L or U of rooms round a small yard."""
    nx, ny = max(1, int((x1 - x0) / cell)), max(1, int((y1 - y0) / cell))
    cw, cd = (x1 - x0) / nx, (y1 - y0) / ny
    for i in range(nx):
        for j in range(ny):
            k = seed + i * 31 + j * 17
            cx, cy = x0 + (i + 0.5) * cw, y0 + (j + 0.5) * cd
            h = hmin + (hmax - hmin) * rnd(k)
            c = [color, shade(color, 0.07), shade(color, -0.06)][k % 3]
            w, d = cw * 0.9, cd * 0.9
            t = min(w, d) * 0.32
            B.box(c, cx, cy - d / 2 + t / 2, z, w, t, h)
            B.box(c, cx - w / 2 + t / 2, cy + t / 2, z, t, d - t, h * 0.9)
            if k % 2:
                B.box(c, cx + w / 2 - t / 2, cy + t / 2, z, t, d - t, h * 0.85)
            else:
                B.box(c, cx + t / 2, cy + d / 2 - t / 2, z, w - t, t, h * 0.8)
            B.rect(DOOR, (cx, cy - d / 2, z), SOUTH, -0.5, 0.5, 0, 1.9, 0.08)


# ---------------------------------------------------------------- Merv parts

def corrugate(B, c, ax, ay, bx, by, ang, z, h, r, spacing, taper=0.86, n=8):
    """The koshk wall: a row of tall half-round ribs of mud brick along a wall face (outward normal ang)."""
    L = math.hypot(bx - ax, by - ay)
    k = max(1, int(L / spacing))
    for i in range(k):
        t = (i + 0.5) / k
        cx, cy = ax + (bx - ax) * t, ay + (by - ay) * t
        B.lathe(c, [(r, 0), (r * 0.97, h * 0.5), (r * taper, h)], cx, cy, z, n, start=ang - math.pi / 2, arc=math.pi)


def corrugated_block(B, w, d, z, h, r, spacing, body=MUD, rib=MUD_LT, parapet=True, n=12):
    """A rectangular body whose four faces are covered with half-round ribs."""
    B.box(body, 0, 0, z, w, d, h)
    corrugate(B, rib, -w / 2, -d / 2, w / 2, -d / 2, SOUTH, z, h, r, spacing, n=n)
    corrugate(B, rib, -w / 2, d / 2, w / 2, d / 2, NORTH, z, h, r, spacing, n=n)
    corrugate(B, rib, -w / 2, -d / 2, -w / 2, d / 2, WEST, z, h, r, spacing, n=n)
    corrugate(B, rib, w / 2, -d / 2, w / 2, d / 2, EAST, z, h, r, spacing, n=n)
    if parapet:
        B.box(shade(body, -0.06), 0, 0, z + h, w + r * 1.6, d + r * 1.6, 0.9)


def ring_pts(r, n, start=0.0):
    return [(r * math.cos(start + math.tau * i / n), r * math.sin(start + math.tau * i / n)) for i in range(n)]


def mud_wall(B, pts, h, t, color=MUD, closed=True, z=0.0, batter=0.35, merlon=True, towers=None, tower_r=4.0, tower_h=None,
             every=20.0, slits=True, out_sign=1, skip=()):
    """A battered mud-brick wall along points, with closely set half-round towers on the outer side and loopholes.
    out_sign = +1 puts the towers on the right-hand side of the direction of travel (outside of a clockwise ring)."""
    n = len(pts)
    segs = range(n) if closed else range(n - 1)
    for i in segs:
        if i in skip:
            continue
        (ax, ay), (bx, by) = pts[i], pts[(i + 1) % n]
        L = math.hypot(bx - ax, by - ay)
        ux, uy = (bx - ax) / L, (by - ay) / L
        nx, ny = uy * out_sign, -ux * out_sign          # outward normal
        B.seg(color, ax, ay, bx, by, z, t * (1 + batter), t, h, ext=t * 0.3)
        a_out = math.atan2(ny, nx)
        if merlon:
            k = max(1, int(L / 2.6))
            for j in range(k):
                u = (j + 0.5) / k
                mx, my = ax + (bx - ax) * u + nx * t * 0.3, ay + (by - ay) * u + ny * t * 0.3
                B.box(color, mx, my, z + h, 1.2, t * 0.35, 1.3, math.atan2(uy, ux))
        if slits:
            k = max(1, int(L / 5.0))
            for j in range(k):
                u = (j + 0.5) / k
                O = (ax + (bx - ax) * u + nx * t / 2, ay + (by - ay) * u + ny * t / 2, z + h * 0.62)
                B.rect(DARK, O, a_out, -0.18, 0.18, 0, 1.4, 0.08)
        if towers:
            m = max(1, round(L / every))
            th = tower_h or h * 1.15
            for j in range(m):
                u = j / m
                tx, ty = ax + (bx - ax) * u + nx * t * 0.75, ay + (by - ay) * u + ny * t * 0.75
                if towers == "round":
                    B.lathe(shade(color, -0.05), [(tower_r * 1.12, 0), (tower_r, th)], tx, ty, z, 12)
                    for q in range(8):
                        a = math.tau * q / 8
                        B.box(shade(color, -0.05), tx + tower_r * 0.85 * math.cos(a), ty + tower_r * 0.85 * math.sin(a), z + th, 0.9, 0.9, 1.0, a)
                else:
                    B.seg(shade(color, -0.05), tx - ux * tower_r, ty - uy * tower_r, tx + ux * tower_r, ty + uy * tower_r, z, tower_r * 2.3, tower_r * 2, th)


def gate_towers(B, x, y, r, h, gap, color=MUD, z=0.0, arch_w=None, face=SOUTH, depth=16.0):
    """A gate: two massive round towers either side of a vaulted passage block, facing -Y."""
    for s in (-1, 1):
        B.lathe(shade(color, -0.04), [(r * 1.15, 0), (r * 1.02, h * 0.85), (r, h)], x + s * (gap / 2 + r * 0.7), y, z, 16)
        k = 12
        for j in range(k):
            a = math.tau * j / k
            B.box(color, x + s * (gap / 2 + r * 0.7) + r * 0.92 * math.cos(a), y + r * 0.92 * math.sin(a), z + h, 1.1, 1.1, 1.2, a)
    B.box(color, x, y + depth * 0.25, z, gap + r, depth, h * 0.85)
    aw = arch_w or gap * 0.7
    B.panel(DARK, arch_outline(aw, h * 0.6), (x, y + depth * 0.25 - depth / 2, z), face, 0.3, -0.05)
    B.panel(DARK, arch_outline(aw, h * 0.6), (x, y + depth * 0.25 + depth / 2, z), NORTH, 0.3, -0.05)


def ruin_wall(B, pts, h, t, color=ERODED, closed=True, z=0.0, towers=0.0, every=20.0, seed=0, out_sign=1, skip=()):
    """A slumped mud-brick wall: a rounded ridge with gaps and the stumps of towers as cones."""
    n = len(pts)
    segs = range(n) if closed else range(n - 1)
    for i in segs:
        if i in skip:
            continue
        (ax, ay), (bx, by) = pts[i], pts[(i + 1) % n]
        L = math.hypot(bx - ax, by - ay)
        k = max(1, int(L / 6.0))
        ux, uy = (bx - ax) / L, (by - ay) / L
        nx, ny = uy * out_sign, -ux * out_sign
        for j in range(k):
            if rnd(seed + i * 13 + j, 3) < 0.08:
                continue              # a breach
            u0, u1 = j / k, (j + 1) / k
            hh = h * (0.6 + 0.4 * rnd(seed + i * 7 + j))
            B.seg(color, ax + (bx - ax) * u0, ay + (by - ay) * u0, ax + (bx - ax) * u1, ay + (by - ay) * u1, z, t * 2.2, t * 0.5, hh, ext=0.6)
        if towers:
            m = max(1, round(L / every))
            for j in range(m):
                u = j / m
                tx, ty = ax + (bx - ax) * u + nx * t * 0.6, ay + (by - ay) * u + ny * t * 0.6
                hh = h * (0.8 + 0.5 * rnd(seed + i * 5 + j, 2))
                B.lathe(shade(color, -0.04), [(towers * 1.5, 0), (towers * 1.2, hh * 0.35), (towers * 0.8, hh * 0.7), (towers * 0.3, hh)], tx, ty, z, 12)


def rubble_field(B, x0, y0, x1, y1, n, seed=0, z=0.3, color=ERODED):
    """Low mounds of melted mud brick and heaps of broken fired brick where houses stood."""
    for i in range(n):
        x = x0 + (x1 - x0) * rnd(seed + i, 1)
        y = y0 + (y1 - y0) * rnd(seed + i, 2)
        w = 4 + 8 * rnd(seed + i, 3)
        d = 3 + 7 * rnd(seed + i, 4)
        if i % 4 == 0:
            B.lathe(BRICK_SD, [(w * 0.3, 0), (w * 0.15, 0.6), (0.0, 0.9)], x, y, z, 7)
        else:
            B.frustum(color if i % 3 else MUD_DK, x, y, z, w, d, w * 0.5, d * 0.5, 0.6 + 1.6 * rnd(seed + i, 5))


def gravestones(B, x0, y0, x1, y1, n, seed=0, z=0.3):
    """A Muslim cemetery: small mud-brick and fired-brick tombs aligned north-south."""
    for i in range(n):
        x = x0 + (x1 - x0) * rnd(seed + i, 6)
        y = y0 + (y1 - y0) * rnd(seed + i, 7)
        c = [MUD_LT, BRICK_SL, MUD][i % 3]
        B.box(c, x, y, z, 1.1, 2.2, 0.45)
        B.seg(c, x, y - 0.9, x, y + 0.9, z + 0.45, 0.8, 0.15, 0.4)


# ---------------------------------------------------------------- the Mausoleum of Sultan Sanjar

def sanjar_mausoleum():
    m = Model("sanjar-mausoleum")
    G = Batch("san_ground")
    G.box(GROUND, 0, 0, 0, 40, 40, 0.3)
    G.box(PAVE, 0, 0, 0.3, 36, 36, 0.3)
    G.box(BRICK_SD, 0, 0, 0.6, 31, 31, 0.9)
    for s in (-1, 1):
        for k in range(3):
            tree_b(G, s * 17.5, -17 + k * 17, 0.3, 1.1, "poplar")
    m.add(0, G.build(), "platform")

    W = 27.0
    z0 = 1.5
    H1 = 15.5       # the cube
    B = Batch("san_cube")
    B.box(BRICK_S, 0, 0, z0, W, W, H1)
    faces = ((SOUTH, (0, -W / 2)), (NORTH, (0, W / 2)), (EAST, (W / 2, 0)), (WEST, (-W / 2, 0)))
    for k, (ang, (cx, cy)) in enumerate(faces):
        O = (cx, cy, z0)
        # framing pilasters at the corners and a deep central niche (the entrance on the south and north)
        for s in (-1, 1):
            B.rect(BRICK_SL, O, ang, s * W * 0.5 - 1.2 * s - 0.6, s * W * 0.5 - 1.2 * s + 0.6, 0, H1, 0.25)
        B.rect(BRICK_SL, O, ang, -W * 0.25, W * 0.25, 0.0, H1 * 0.86, 0.22)
        B.panel(BRICK_SD, arch_outline(W * 0.4, H1 * 0.8), O, ang, 0.3, 0.0)
        B.panel(DARK if k < 2 else BRICK_SD, arch_outline(W * 0.17, H1 * 0.42), O, ang, 0.22, 0.3)
        if k >= 2:
            B.panel(DARK, arch_outline(W * 0.08, H1 * 0.14), (cx, cy, z0 + H1 * 0.5), ang, 0.1, 0.52)
        # patterned brick in the spandrels and side panels (hazarbaf)
        for s in (-1, 1):
            lozenge_field(B, O, ang, s * W * 0.31 - 2.2, s * W * 0.31 + 2.2, H1 * 0.12, H1 * 0.8, 0.72, (BRICK_SD, BRICK_SL), 0.25, 0.55, 0.1)
        kufic_band(B, O, ang, -W * 0.47, W * 0.47, H1 * 0.88, H1 * 0.97, BRICK_SD, BRICK_SL, 0.0, 1.3)
    B.box(BRICK_SL, 0, 0, z0 + H1, W + 0.8, W + 0.8, 0.6)
    m.add(1, B.build(), "cube")

    # the open gallery round the upper storey
    zg = z0 + H1 + 0.6
    Hg = 6.0
    Gl = Batch("san_gallery")
    Gl.box(BRICK_S, 0, 0, zg, W * 0.78, W * 0.78, Hg)     # the drum wall behind the gallery
    n = 7
    for ang, (cx, cy) in faces:
        ux, uy = -math.sin(ang), math.cos(ang)
        bay = (W - 1.0) / n
        for i in range(n + 1):
            u = -W / 2 + 0.5 + i * bay
            Gl.box(BRICK_S, cx + ux * u - math.cos(ang) * 0.6, cy + uy * u - math.sin(ang) * 0.6, zg, 1.2, 1.2, Hg)
        for i in range(n):
            u = -W / 2 + 0.5 + (i + 0.5) * bay
            O = (cx + ux * u, cy + uy * u, zg)
            Gl.panel(BRICK_SL, arch_outline(bay * 0.86, Hg * 0.88), O, ang, 0.15, -0.6)
            Gl.panel(DARK, arch_outline(bay * 0.66, Hg * 0.78), O, ang, 0.2, -0.45)
        Gl.rect(BRICK_SD, (cx, cy, zg + Hg - 0.9), ang, -W / 2, W / 2, 0, 0.9, 0.3, -0.6)
    Gl.box(BRICK_SL, 0, 0, zg + Hg, W + 0.4, W + 0.4, 0.7)
    for i in range(int(W * 4 / 1.6)):
        t = i * 1.6
        side, u = int(t // W), t % W - W / 2
        x, y = [(u, -W / 2), (W / 2, u), (-u, W / 2), (-W / 2, -u)][side % 4]
        Gl.box(BRICK_S, x, y, zg + Hg + 0.7, 0.7, 0.7, 0.8)
    m.add(2, Gl.build(), "gallery")

    # octagonal zone, drum and the double dome
    D = Batch("san_dome")
    zt = zg + Hg + 0.7
    D.prism(BRICK_S, ngon(11.4, 16), zt, 2.0)
    D.lathe(BRICK_SL, [(11.6, 0), (11.6, 0.5)], 0, 0, zt + 2.0, 32)
    zd = zt + 2.5
    D.lathe(BRICK_S, [(9.9, 0), (9.9, 2.4)], 0, 0, zd, 48)
    for i in range(16):
        a = math.tau * (i + 0.5) / 16
        D.panel(DARK, arch_outline(0.9, 1.7), (9.9 * math.cos(a), 9.9 * math.sin(a), zd + 0.35), a, 0.12, -0.02)
    kufic_ring(D, 0, 0, zd + 2.4, 1.3, 9.75, 28, COBALT, TWHITE, 48)
    # the outer shell: sits proud of the inner dome on a short collar, glazed turquoise
    D.lathe(TURQ_LT, [(9.95, 0), (9.95, 0.5)], 0, 0, zd + 3.7, 48)
    pointed_dome(D, 9.6, 0, 0, zd + 4.2, TURQ, height=1.12, n=96, rings=20, finial=GILT)
    m.add(3, D.build(), "dome")
    return m


# ---------------------------------------------------------------- the Friday mosque of Sultan Kala

def brick_portal(B, x, y, z, w, h, depth, ang=SOUTH, body=BRICK_S, frame=BRICK_SL, field=BRICK_SD, tile=None):
    """A pishtaq on a face through (x, y) with outward normal ang: frame, patterned fields, deep arch and door."""
    ux, uy = -math.sin(ang), math.cos(ang)
    nx, ny = math.cos(ang), math.sin(ang)
    B.seg(body, x - ux * w / 2 - nx * depth / 2, y - uy * w / 2 - ny * depth / 2, x + ux * w / 2 - nx * depth / 2, y + uy * w / 2 - ny * depth / 2, z, depth, depth, h)
    O = (x, y, z)
    for s in (-1, 1):
        B.rect(frame, O, ang, s * w * 0.47 - w * 0.03, s * w * 0.47 + w * 0.03, 0, h * 0.97, 0.22)
    B.rect(frame, O, ang, -w * 0.5, w * 0.5, h * 0.94, h, 0.22)
    if tile:
        kufic_band(B, O, ang, -w * 0.42, w * 0.42, h * 0.84, h * 0.93, tile[1], TWHITE, 0.0)
    else:
        kufic_band(B, O, ang, -w * 0.42, w * 0.42, h * 0.84, h * 0.93, field, frame, 0.0)
    for s in (-1, 1):
        u0, u1 = sorted((s * w * 0.33, s * w * 0.42))
        lozenge_field(B, O, ang, u0, u1, h * 0.05, h * 0.8, max(0.8, (u1 - u0) / 1.6), tile or (field, frame), 0.0, 0.6, 0.1)
    B.panel(frame, arch_outline(w * 0.62, h * 0.8), O, ang, 0.22)
    B.panel(tile[1] if tile else DARK, arch_outline(w * 0.54, h * 0.74), O, ang, 0.3)
    B.panel(DARK, arch_outline(w * 0.2, h * 0.32), O, ang, 0.1, 0.3)


def seljuk_minaret(B, x, y, r, h, z=0.0, color=BRICK_S, band=BRICK_SL):
    """A tapering round brick minaret on an octagonal base, with patterned bands and a balcony."""
    B.prism(BRICK_SD, ngon(r * 1.35, 8), z, r * 2.2, x, y)
    B.lathe(color, [(r, 0), (r * 0.72, h)], x, y, z + r * 2.2, 16)
    for f in (0.3, 0.55, 0.78):
        rr = r * (1 - 0.28 * f)
        B.lathe(band, [(rr * 1.04, 0), (rr * 1.04, r * 0.6)], x, y, z + r * 2.2 + h * f, 16)
    rt = r * 0.72
    B.lathe(band, [(rt, 0), (rt * 1.5, r * 0.7), (rt * 1.5, r * 1.0)], x, y, z + r * 2.2 + h, 16)
    B.lathe(color, [(rt * 0.7, 0), (rt * 0.7, r * 1.4), (0.0, r * 2.4)], x, y, z + r * 2.2 + h + r * 1.0, 12)


def friday_mosque():
    """Qibla to the west: dome chamber on the west, entrance on the east (built at the origin, facing -Y as usual for the map)."""
    m = Model("friday-mosque")
    W, D = 110.0, 90.0
    G = Batch("fm_ground")
    G.box(GROUND, 0, 0, 0, W, D, 0.3)
    m.add(0, G.build(), "ground")
    B = Batch("fm_body")
    H = 8.0
    dep = 11.0
    cx0, cx1 = -W / 2 + 4, W / 2 - 4
    cy0, cy1 = -D / 2 + 4, D / 2 - 4
    # four ranges of arcades round the court
    B.box(BRICK_S, 0, cy0 + dep / 2, 0.3, cx1 - cx0, dep, H)
    B.box(BRICK_S, 0, cy1 - dep / 2, 0.3, cx1 - cx0, dep, H)
    B.box(BRICK_S, cx0 + dep / 2 + 8, 0, 0.3, dep + 16, cy1 - cy0 - 2 * dep, H)       # deeper prayer hall on the qibla side
    B.box(BRICK_S, cx1 - dep / 2, 0, 0.3, dep, cy1 - cy0 - 2 * dep, H)
    for (x, y, w, d) in ((0, cy0 + dep / 2, cx1 - cx0, dep), (0, cy1 - dep / 2, cx1 - cx0, dep), (cx0 + dep / 2 + 8, 0, dep + 16, cy1 - cy0 - 2 * dep), (cx1 - dep / 2, 0, dep, cy1 - cy0 - 2 * dep)):
        B.box(BRICK_SL, x, y, 0.3 + H, w + 0.3, d + 0.3, 0.5)
        # little domes over each bay of the halls
        n = max(2, int(max(w, d) / 9))
        for i in range(n):
            t = -0.5 + (i + 0.5) / n
            bx, by = (x + t * w, y) if w > d else (x, y + t * d)
            B.lathe(BRICK_SL, [(2.6, 0), (2.2, 1.2), (1.2, 2.0), (0.0, 2.3)], bx, by, 0.8 + H, 8)
    ix0, ix1 = cx0 + dep + 16, cx1 - dep
    iy0, iy1 = cy0 + dep, cy1 - dep
    B.box(PAVE, (ix0 + ix1) / 2, 0, 0.3, ix1 - ix0, iy1 - iy0, 0.15)
    B.box(WATER_C, (ix0 + ix1) / 2, 0, 0.3, 5, 5, 0.4)
    # inner court facades: arcades of pointed arches
    for ang, (x, y), L in ((NORTH, ((ix0 + ix1) / 2, iy0), ix1 - ix0), (SOUTH, ((ix0 + ix1) / 2, iy1), ix1 - ix0), (WEST, (ix1, 0), iy1 - iy0), (EAST, (ix0, 0), iy1 - iy0)):
        n = int(L / 4.5)
        ux, uy = -math.sin(ang), math.cos(ang)
        for i in range(n):
            u = -L / 2 + (i + 0.5) * L / n
            B.panel(DARK, arch_outline(L / n * 0.66, H * 0.72), (x + ux * u, y + uy * u, 0.3), ang, 0.2)
    # outer walls: blind niches
    for ang, (x, y), L in ((SOUTH, (0, -D / 2 + 4), W - 8), (NORTH, (0, D / 2 - 4), W - 8)):
        n = int(L / 6)
        for i in range(n):
            u = -L / 2 + (i + 0.5) * L / n
            B.panel(BRICK_SD, arch_outline(L / n * 0.6, H * 0.7), (u, y, 0.3), ang, 0.15)
    # the dome chamber on the qibla (west) side
    dcx = cx0 + 13
    B.box(BRICK_S, dcx, 0, 0.3, 24, 24, 15)
    B.box(BRICK_SL, dcx, 0, 15.3, 24.6, 24.6, 0.6)
    B.prism(BRICK_S, ngon(11.6, 8), 15.9, 2.6, dcx, 0)
    for i in range(8):
        a = math.tau * i / 8
        B.panel(DARK, arch_outline(2.4, 2.0), (dcx + 11.6 * math.cos(math.pi / 8) * math.cos(a), 11.6 * math.cos(math.pi / 8) * math.sin(a), 16.2), a, 0.08)
    pointed_dome(B, 10.4, dcx, 0, 18.5, BRICK_SL, height=1.05, n=40, rings=10)
    m.add(1, B.build(), "halls")
    P = Batch("fm_portals")
    brick_portal(P, ix0 + 0.1, 0, 0.3, 16, 17, 4, EAST)              # qibla iwan before the dome
    brick_portal(P, (ix0 + ix1) / 2, iy0 - 0.1, 0.3, 11, 12, 3, NORTH)
    brick_portal(P, (ix0 + ix1) / 2, iy1 + 0.1, 0.3, 11, 12, 3, SOUTH)
    brick_portal(P, ix1 - 0.1, 0, 0.3, 11, 12, 3, WEST)
    brick_portal(P, cx1 + 0.1, 0, 0.3, 14, 14, 4, EAST)              # the entrance on the east
    seljuk_minaret(P, cx1 - 3, cy1 - 3, 2.2, 32, 0.3)
    for i in range(6):
        tree_b(P, cx1 + 2.0, -40 + i * 6 if i < 3 else 22 + (i - 3) * 6, 0.3, 1.0, "poplar")
    m.add(2, P.build(), "portals and minaret")
    return m


# ---------------------------------------------------------------- Shahriyar Ark

ARK_PTS = [(-172, -182), (172, -182), (176, 182), (-176, 182)]


def kepter_khana(B, x, y, z=0.3):
    """The 'dovecote': a building whose walls are lined with rows of small niches (dovecote, library or strong-room)."""
    w, d, h = 30.0, 26.0, 9.0
    B.box(MUD, x, y, z, w, d, h)
    B.box(shade(MUD, -0.06), x, y, z + h - 0.2, w + 0.6, d + 0.6, 0.6)
    for ang, (cx, cy), L in ((SOUTH, (x, y - d / 2), w), (NORTH, (x, y + d / 2), w), (EAST, (x + w / 2, y), d), (WEST, (x - w / 2, y), d)):
        for i in range(int(L / 2.2)):
            u = -L / 2 + 1.1 + i * 2.2
            B.panel(MUD_LT, [(u - 0.5, 0), (u + 0.5, 0), (u + 0.5, h * 0.9), (u - 0.5, h * 0.9)], (cx, cy, z), ang, 0.6)
    # the inner rows of niches seen over the roofless top
    B.box(DARK, x, y, z + h - 0.5, w * 0.6, d * 0.55, 0.6)


def ark_keep(B, x, y, z=0.3, ruin=False):
    """The pavilion-keep in the manner of a koshk: corrugated walls on a sloping plinth (reconstruction)."""
    w, d = 34.0, 30.0
    B.frustum(MUD_DK, x, y, z, w + 10, d + 10, w + 2, d + 2, 5.0)
    if ruin:
        sub = Batch("tmp")
        corrugated_block(sub, w, d, 0, 7.0, 1.1, 2.3, MUD, ERODED, parapet=False)
        for c, (V, F) in sub.g.items():
            B.add(c, [(vx + x, vy + y, vz + z + 5.0) for vx, vy, vz in V], F)
        B.frustum(ERODED, x, y, z + 12.0, w - 4, d - 4, w * 0.4, d * 0.4, 3.0)
        return
    sub = Batch("tmp")
    corrugated_block(sub, w, d, 0, 16.0, 1.1, 2.3, MUD, MUD_LT)
    for c, (V, F) in sub.g.items():
        B.add(c, [(vx + x, vy + y, vz + z + 5.0) for vx, vy, vz in V], F)
    B.box(DARK, x, y, z + 21.6, w * 0.32, d * 0.3, 0.4)
    B.box(MUD_LT, x - w * 0.25, y + d * 0.2, z + 21.9, 8, 8, 3.2)
    for s in (-1, 1):
        B.panel(DARK, arch_outline(1.4, 2.6), (x + s * 6, y - d / 2 - 1.2, z + 14), SOUTH, 0.1)
    # ramp up the plinth to the door
    B.seg(MUD_DK, x, y - d / 2 - 22, x, y - d / 2 - 4, z, 4.0, 4.0, 0.6)
    B.frustum(MUD_DK, x, y - d / 2 - 6, z, 4.5, 6, 4.5, 4, 5.0)
    B.panel(DARK, arch_outline(2.2, 3.4), (x, y - d / 2 - 1.2, z + 5), SOUTH, 0.12)


def ark_palace(B, x, y, z=0.3):
    """A palace of four iwans round a court."""
    w, d, h, dep = 70.0, 60.0, 8.0, 10.0
    B.box(BRICK_S, x, y - d / 2 + dep / 2, z, w, dep, h)
    B.box(BRICK_S, x, y + d / 2 - dep / 2, z, w, dep, h)
    B.box(BRICK_S, x - w / 2 + dep / 2, y, z, dep, d - 2 * dep, h)
    B.box(BRICK_S, x + w / 2 - dep / 2, y, z, dep, d - 2 * dep, h)
    for (cx, cy, ww, dd) in ((x, y - d / 2 + dep / 2, w, dep), (x, y + d / 2 - dep / 2, w, dep), (x - w / 2 + dep / 2, y, dep, d), (x + w / 2 - dep / 2, y, dep, d)):
        B.box(BRICK_SL, cx, cy, z + h, ww + 0.3, dd + 0.3, 0.5)
    B.box(PAVE, x, y, z, w - 2 * dep, d - 2 * dep, 0.15)
    B.box(WATER_C, x, y, z, 10, 6, 0.4)
    for ang, (cx, cy), L in ((NORTH, (x, y - d / 2 + dep), w - 2 * dep), (SOUTH, (x, y + d / 2 - dep), w - 2 * dep), (EAST, (x - w / 2 + dep, y), d - 2 * dep), (WEST, (x + w / 2 - dep, y), d - 2 * dep)):
        brick_portal(B, cx, cy, z, 12, 12, 2.5, ang)
        n = int(L / 5)
        ux, uy = -math.sin(ang), math.cos(ang)
        for i in range(n):
            u = -L / 2 + (i + 0.5) * L / n
            if abs(u) < 7:
                continue
            B.panel(DARK, arch_outline(2.6, h * 0.7), (cx + ux * u, cy + uy * u, z), ang, 0.15)
    # the audience hall behind the north iwan, domed
    B.box(BRICK_S, x, y + d / 2 - dep / 2, z, 16, 16, 11)
    pointed_dome(B, 7.4, x, y + d / 2 - dep / 2, z + 11, BRICK_SL, height=1.0, n=28, rings=8)
    brick_portal(B, x, y - d / 2, z, 14, 13, 3, SOUTH)


def shahriyar_ark(ruin=False):
    m = Model("shahriyar-ark" + ("-ruin" if ruin else ""))
    G = Batch("ark_ground")
    G.box(GROUND, 0, 0, 0, 360, 380, 0.3)
    m.add(0, G.build(), "ground")
    pts = [(-164, -176), (164, -176), (166, 176), (-166, 176)]
    if ruin:
        R = Batch("ark_ruin")
        ruin_wall(R, pts, 9.0, 6.0, ERODED, True, 0.3, towers=3.2, every=22.0, seed=11, out_sign=1)
        # the palace and buildings as mounds, the keep a corrugated stump
        R.frustum(ERODED, -20, 40, 0.3, 74, 64, 56, 46, 3.0)
        for (x, y, w, d) in ((-20, 40, 12, 60), (-20, 40, 70, 10), (40, -60, 30, 26), (100, 60, 40, 24), (-110, -40, 50, 30)):
            R.frustum(MUD_DK, x, y, 3.0 if (x, y) == (-20, 40) else 0.3, w, d, w * 0.6, d * 0.6, 2.2)
        ark_keep(R, -110, 110, 0.3, ruin=True)
        rubble_field(R, 60, 20, 150, 150, 40, seed=5)
        rubble_field(R, -150, -150, -50, -60, 30, seed=9)
        for i in range(10):
            R.frustum(ERODED, -140 + rnd(i) * 280, -150 + rnd(i, 5) * 160, 0.3, 14, 10, 6, 4, 1.4)
        for i in range(8):
            tree_b(R, -150 + i * 40, -140 + (i % 3) * 30, 0.3, 1.4, color="#8C9A5E")
        # a rebuilt gate as a gap between cones
        R.lathe(ERODED, [(12, 0), (6, 8), (2, 12)], -16, -180, 0.3, 12)
        R.lathe(ERODED, [(12, 0), (6, 8), (2, 12)], 16, -180, 0.3, 12)
        m.add(1, R.build(), "ruins")
        return m
    Wb = Batch("ark_walls")
    # glacis and the battered wall with closely set half-round towers
    for i in range(4):
        (ax, ay), (bx, by) = pts[i], pts[(i + 1) % 4]
        L = math.hypot(bx - ax, by - ay)
        ux, uy = (bx - ax) / L, (by - ay) / L
        nx, ny = -uy, ux
        Wb.seg(MUD_DK, ax - nx * 6, ay - ny * 6, bx - nx * 6, by - ny * 6, 0.3, 10, 2, 3.0, ext=6)
    mud_wall(Wb, pts, 12.0, 6.0, MUD, True, 0.3, 0.3, True, "round", 4.2, 14.0, 20.0, True, out_sign=1, skip=())
    gate_towers(Wb, 0, -176, 8.0, 15.0, 8.0, MUD, 0.3)
    Wb.seg(PAVE_DK, 0, -190, 0, -150, 0.3, 6, 6, 0.1)
    m.add(1, Wb.build(), "walls")
    P = Batch("ark_inner")
    ark_palace(P, -20, 40)
    kepter_khana(P, 40, -60)
    house_grid(P, 70, 20, 160, 160, seed=3, cell=13, color=MUD)
    house_grid(P, -160, -160, -60, -60, seed=7, cell=13, color=MUD)
    house_grid(P, 80, -160, 160, -90, seed=5, cell=13, color=MUD)
    # barracks and stables along the west wall
    for k in range(5):
        P.box(MUD_LT, -150, -40 + k * 18, 0.3, 12, 14, 4.5)
    # a small mosque of the citadel
    P.box(BRICK_S, 100, -40, 0.3, 20, 16, 7)
    pointed_dome(P, 6.0, 96, -40, 7.3, BRICK_SL, 1.0, 24, 8)
    seljuk_minaret(P, 108, -34, 1.2, 16, 0.3)
    for i in range(14):
        tree_b(P, -50 + (i % 7) * 10, 90 + (i // 7) * 10, 0.3, 1.6, "round" if i % 2 else "poplar")
    P.seg(PAVE_DK, 0, -150, -20, 10, 0.3, 6, 6, 0.1)
    # the sultan's garden: avenues of poplars and fruit trees round a pool
    P.box(LEAF_DK, -105, 10, 0.3, 64, 70, 0.2)
    P.box(WATER_C, -105, 10, 0.3, 10, 14, 0.45)
    for i in range(6):
        for j in range(6):
            if 2 <= i <= 3 and 2 <= j <= 3:
                continue
            tree_b(P, -132 + i * 10.8, -18 + j * 11.2, 0.5, 1.6 if (i + j) % 2 else 1.3, "poplar" if i in (0, 5) else "round")
    house_grid(P, -60, 92, 40, 160, seed=12, cell=13, color=MUD)
    house_grid(P, 20, -160, 70, -100, seed=17, cell=13, color=MUD)
    m.add(2, P.build(), "palace")
    K = Batch("ark_keep")
    ark_keep(K, -110, 110)
    m.add(3, K.build(), "keep")
    return m


# ---------------------------------------------------------------- the walls of Sultan Kala (south gate)

def sultan_kala_walls(ruin=False):
    """A 300 m stretch of the south wall; outside (the ditch) toward -Y, the town toward +Y."""
    m = Model("sultan-kala-walls" + ("-ruin" if ruin else ""))
    G = Batch("skw_ground")
    G.box(GROUND, 0, 0, 0, 300, 90, 0.3)
    xL, xR = -144.0, 144.0
    wy = -6.0
    if ruin:
        G.box(shade(GROUND, -0.08), 0, -36, 0.3, 300, 8, 0.1)
        m.add(0, G.build(), "ground")
        R = Batch("skw_ruin")
        ruin_wall(R, [(xL, wy), (-14, wy)], 12.0, 7.0, ERODED, False, 0.3, towers=4.0, every=16.0, seed=2, out_sign=1)
        ruin_wall(R, [(14, wy), (xR, wy)], 12.0, 7.0, ERODED, False, 0.3, towers=4.0, every=16.0, seed=9, out_sign=1)
        ruin_wall(R, [(xL, -26), (xR, -26)], 3.0, 2.5, ERODED, False, 0.3, seed=4)
        for s in (-1, 1):
            R.lathe(ERODED, [(11, 0), (7, 9), (2.5, 15)], s * 16, wy - 2, 0.3, 12)
        for i in range(10):
            R.frustum(MUD_DK, -120 + i * 26, 22 + (i % 3) * 10, 0.3, 14, 10, 7, 5, 1.2 + (i % 2))
        for i in range(6):
            tree_b(R, -130 + i * 50, 38, 0.3, 1.2, color="#8C9A5E")
        R.seg(PAVE_DK, 0, -45, 0, 45, 0.3, 5, 5, 0.08)
        rubble_field(R, -140, 8, -12, 44, 40, seed=31)
        rubble_field(R, 12, 8, 140, 44, 40, seed=57)
        m.add(1, R.build(), "ruins")
        return m
    # ditch with water, the bridge
    G.box(WATER_C, 0, -38, 0.0, 300, 9, 0.35)
    G.box(PAVE_DK, 0, -38, 0.0, 9, 12, 0.6)
    G.seg(PAVE_DK, 0, -45, 0, -30, 0.3, 7, 7, 0.1)
    G.seg(PAVE_DK, 0, -6, 0, 45, 0.3, 8, 8, 0.1)
    m.add(0, G.build(), "ground and ditch")
    W = Batch("skw_walls")
    # outer (fore) wall with small towers
    mud_wall(W, [(xL, -28), (-10, -28)], 4.5, 2.4, MUD, False, 0.3, 0.2, True, "round", 1.8, 5.5, 15.0, True, out_sign=1)
    mud_wall(W, [(10, -28), (xR, -28)], 4.5, 2.4, MUD, False, 0.3, 0.2, True, "round", 1.8, 5.5, 15.0, True, out_sign=1)
    # the glacis slope before the main wall
    W.seg(MUD_DK, xL, wy - 9, -14, wy - 9, 0.3, 10, 2, 4.0)
    W.seg(MUD_DK, 14, wy - 9, xR, wy - 9, 0.3, 10, 2, 4.0)
    # main wall: battered, with an inner gallery of loopholes and half-round towers about every 15 m
    mud_wall(W, [(xL, wy), (-14, wy)], 15.0, 7.0, MUD, False, 0.3, 0.45, True, "round", 4.6, 17.0, 15.0, True, out_sign=1)
    mud_wall(W, [(14, wy), (xR, wy)], 15.0, 7.0, MUD, False, 0.3, 0.45, True, "round", 4.6, 17.0, 15.0, True, out_sign=1)
    for x in (-128, -98, -68, -38, 38, 68, 98, 128):
        W.rect(DARK, (x, wy - 5.2, 9.0), SOUTH, -5, 5, 0, 1.0, 0.1)
    # the inner face: a gallery of vaulted casemates opening toward the town
    for x in range(-142, 143, 4):
        if abs(x) < 18 or 28 < abs(x) < 56:
            continue
        W.panel(DARK, arch_outline(2.4, 4.2), (x, wy + 3.5, 0.3), NORTH, 0.15)
    # the rampart walk and stair on the town side
    for s in (-1, 1):
        W.seg(MUD_DK, s * 30, wy + 6, s * 54, wy + 6, 0.3, 3, 3, 0.1)
        for k in range(10):
            W.box(MUD_DK, s * (30 + k * 2.4), wy + 5.5, 0.3, 2.4, 3, 1.5 * (k + 1))
    m.add(1, W.build(), "walls")
    Gt = Batch("skw_gate")
    gate_towers(Gt, 0, wy, 9.0, 19.0, 10.0, MUD, 0.3, 7.0, depth=18.0)
    # barbican: a small walled court in front of the gate
    mud_wall(Gt, [(-14, wy - 10), (-14, -24), (14, -24), (14, wy - 10)], 7.0, 2.6, MUD, False, 0.3, 0.2, True, "round", 2.2, 8.0, 14.0, True, out_sign=1)
    Gt.panel(DARK, arch_outline(4.5, 5.0), (0, -24 - 1.3, 0.3), SOUTH, 0.2)
    Gt.box(BRICK_SL, 0, wy - 9.6, 14.6, 12, 1.0, 1.4)
    m.add(2, Gt.build(), "gate")
    T = Batch("skw_town")
    for x0 in (-138, 18):
        house_grid(T, x0, 10, x0 + 120, 44, seed=int(x0) + 200, cell=9, color=MUD)
    for i in range(6):
        tree_b(T, -10 + (i % 2) * 20, 12 + i * 5, 0.3, 1.1, "poplar")
    m.add(3, T.build(), "town")
    return m


# ---------------------------------------------------------------- the walls of Gyaur Kala (south gate)

def gyaur_kala_walls(ruin=False):
    m = Model("gyaur-kala-walls" + ("-ruin" if ruin else ""))
    G = Batch("gkw_ground")
    G.box(GROUND, 0, 0, 0, 240, 70, 0.3)
    wy = -8.0
    if ruin:
        m.add(0, G.build(), "ground")
        R = Batch("gkw_ruin")
        ruin_wall(R, [(-114, wy), (-12, wy)], 16.0, 9.0, ERODED, False, 0.3, towers=4.5, every=24.0, seed=21, out_sign=1)
        ruin_wall(R, [(12, wy), (114, wy)], 16.0, 9.0, ERODED, False, 0.3, towers=4.5, every=24.0, seed=27, out_sign=1)
        for s in (-1, 1):
            R.lathe(ERODED, [(12, 0), (7, 11), (2.5, 18)], s * 15, wy - 2, 0.3, 12)
        for i in range(8):
            R.frustum(ERODED, -100 + i * 28, 20 + (i % 2) * 8, 0.3, 12, 9, 5, 4, 1.0)
        R.seg(PAVE_DK, 0, -35, 0, 35, 0.3, 4, 4, 0.08)
        rubble_field(R, -110, 6, -10, 33, 60, seed=13)
        rubble_field(R, 10, 6, 110, 33, 60, seed=77)
        for i in range(8):
            tree_b(R, -100 + i * 28, -28, 0.3, 1.2, color="#8C9A5E")
        m.add(1, R.build(), "ruins")
        return m
    G.seg(PAVE_DK, 0, -35, 0, 35, 0.3, 8, 8, 0.1)
    m.add(0, G.build(), "ground")
    W = Batch("gkw_walls")
    # a broad rampart with a wall on top; rectangular towers about every 24 m and a gallery of arrow-slits
    for a, b in (((-114, wy), (-13, wy)), ((13, wy), (114, wy))):
        W.seg(MUD_DK, a[0], wy, b[0], wy, 0.3, 22, 14, 6.0)
    mud_wall(W, [(-114, wy), (-13, wy)], 13.0, 7.0, MUD, False, 6.3, 0.25, True, "square", 4.0, 15.0, 24.0, True, out_sign=1)
    mud_wall(W, [(13, wy), (114, wy)], 13.0, 7.0, MUD, False, 6.3, 0.25, True, "square", 4.0, 15.0, 24.0, True, out_sign=1)
    for x in range(-110, 112, 6):
        if abs(x) < 16:
            continue
        W.panel(DARK, arch_outline(0.8, 2.2, 0.55), (x, wy - 4.4, 13.0), SOUTH, 0.1)
    m.add(1, W.build(), "walls")
    Gt = Batch("gkw_gate")
    for s in (-1, 1):
        Gt.frustum(MUD, s * 12, wy - 2, 0.3, 14, 20, 12, 17, 22.0)
        Gt.frustum(MUD_LT, s * 12, wy - 2, 22.3, 12.5, 17.5, 12.5, 17.5, 1.2)
        for k in range(4):
            Gt.box(MUD, s * 12 - 4.5 + k * 3, wy - 10.5, 23.5, 1.4, 1.0, 1.4)
        for k in range(3):
            Gt.panel(DARK, arch_outline(0.7, 2.0, 0.55), (s * 12, wy - 12.0, 8 + k * 4.5), SOUTH, 0.1)
    Gt.box(MUD, 0, wy, 0.3, 12, 18, 16)
    Gt.panel(DARK, arch_outline(6.5, 9.0, 0.5), (0, wy - 9.05, 0.3), SOUTH, 0.3)
    Gt.panel(DARK, arch_outline(6.5, 9.0, 0.5), (0, wy + 9.05, 0.3), NORTH, 0.3)
    for k in range(5):
        Gt.box(MUD, -4.8 + k * 2.4, wy - 8, 16.3, 1.3, 1.0, 1.3)
    m.add(2, Gt.build(), "gate")
    T = Batch("gkw_town")
    house_grid(T, -110, 8, -10, 33, seed=40, cell=11, color=MUD)
    house_grid(T, 10, 8, 110, 33, seed=50, cell=11, color=MUD)
    m.add(3, T.build(), "houses")
    return m


# ---------------------------------------------------------------- Beni Makhan mosque

def beni_makhan():
    m = Model("beni-makhan")
    G = Batch("bm_ground")
    G.box(GROUND, 0, 0, 0, 70, 60, 0.3)
    m.add(0, G.build(), "ground")
    B = Batch("bm_body")
    # enclosure
    for (x, y, w, d) in ((-6, -22, 52, 1.6), (-6, 22, 52, 1.6), (19.2, 0, 1.6, 44)):
        B.box(MUD, x, y, 0.3, w, d, 6)
    B.box(PAVE, 3, 0, 0.3, 30, 42, 0.12)
    # prayer hall of piers on the west (qibla) side under a flat roof
    B.box(MUD, -24, 0, 0.3, 16, 46, 1.0)
    for i in range(4):
        for j in range(9):
            B.lathe(MUD_LT, [(0.75, 0), (0.62, 4.2), (0.95, 4.6), (0.95, 5.0)], -30 + i * 4, -18 + j * 4.5, 1.3, 8)
    B.box(MUD, -24, 0, 6.3, 17, 46.5, 1.2)
    B.box(MUD, -32.3, 0, 0.3, 1.4, 46, 7.5)
    B.box(MUD_DK, -24, 0, 7.5, 17.4, 46.8, 0.5)
    # side arcades
    for s in (-1, 1):
        B.box(MUD, 3, s * 19, 0.3, 30, 4.5, 5.0)
        for i in range(7):
            B.panel(DARK, arch_outline(2.6, 3.6), (-10 + i * 4.3, s * 16.7, 0.3), NORTH if s < 0 else SOUTH, 0.12)
    for i in range(9):
        B.panel(DARK, arch_outline(2.6, 4.0), (-15.9, -18 + i * 4.5, 0.3), EAST, 0.1)
    # gate on the east and square minaret at the north-east corner
    B.box(MUD_LT, 19.2, 0, 0.3, 4, 9, 8)
    B.panel(DARK, arch_outline(3.6, 5.5), (21.3, 0, 0.3), EAST, 0.2)
    B.frustum(MUD_LT, 16, 18, 0.3, 4.6, 4.6, 3.6, 3.6, 17)
    B.box(MUD, 16, 18, 17.3, 4.4, 4.4, 1.0)
    B.frustum(MUD_LT, 16, 18, 18.3, 3.2, 3.2, 1.4, 1.4, 3.0)
    m.add(1, B.build(), "mosque")
    C = Batch("bm_cistern")
    # the domed cistern (sardoba) south-east of the mosque
    C.lathe(MUD_LT, [(7.5, 0), (7.5, 1.5), (6.4, 4.5), (4.0, 6.8), (0.0, 7.8)], 28, -20, 0.3, 24)
    C.panel(DARK, arch_outline(1.6, 2.4), (28, -27.6, 0.3), SOUTH, 0.12)
    C.lathe(MUD, [(1.0, 0), (1.0, 1.8), (0.0, 2.6)], 28, -20, 7.9, 8)
    flat_houses(C, [(28, 10, 9, 8, 4), (28, 22, 10, 7, 4.5), (-24, 26, 14, 5, 3.5)])
    for i in range(3):
        tree_b(C, 8 + i * 6, -26, 0.3, 1.0)
    house_grid(C, -34, 23.6, 22, 29.6, seed=90, cell=5.6, hmin=3.0, hmax=4.5)
    house_grid(C, -34, -29.6, 18, -23.6, seed=95, cell=7, hmin=3.0, hmax=4.5)
    m.add(2, C.build(), "cistern")
    return m


# ---------------------------------------------------------------- the Buddhist stupa and monastery

def stupa_monastery():
    m = Model("stupa")
    G = Batch("st_ground")
    G.box(GROUND, 0, 0, 0, 90, 90, 0.3)
    G.box(PAVE_DK, -20, 4, 0.3, 40, 40, 0.15)
    m.add(0, G.build(), "ground")
    E = Batch("st_enclosure")
    for (x, y, w, d) in ((0, -43.5, 87, 2), (0, 43.5, 87, 2), (-43.5, 0, 2, 87), (43.5, 0, 2, 87)):
        E.box(MUD, x, y, 0.3, w, d, 4.5)
    E.box(MUD_LT, -20, -43.5, 0.3, 7, 4, 6.5)
    E.panel(DARK, arch_outline(2.8, 4.0), (-20, -45.6, 0.3), SOUTH, 0.15)
    # monastery (vihara): cells round a court on the east
    mx, my, mw, md, dep = 22.0, 0.0, 38.0, 46.0, 7.0
    for (x, y, w, d) in ((mx, my - md / 2 + dep / 2, mw, dep), (mx, my + md / 2 - dep / 2, mw, dep), (mx - mw / 2 + dep / 2, my, dep, md - 2 * dep), (mx + mw / 2 - dep / 2, my, dep, md - 2 * dep)):
        E.box(MUD, x, y, 0.3, w, d, 5.5)
        E.box(MUD_DK, x, y, 5.8, w + 0.3, d + 0.3, 0.4)
    for ang, (x, y), L in ((NORTH, (mx, my - md / 2 + dep), mw - 2 * dep), (SOUTH, (mx, my + md / 2 - dep), mw - 2 * dep), (EAST, (mx - mw / 2 + dep, my), md - 2 * dep), (WEST, (mx + mw / 2 - dep, my), md - 2 * dep)):
        n = int(L / 3.2)
        ux, uy = -math.sin(ang), math.cos(ang)
        for i in range(n):
            u = -L / 2 + (i + 0.5) * L / n
            E.panel(DARK, [(-0.6, 0), (0.6, 0), (0.6, 2.0), (-0.6, 2.0)], (x + ux * u, y + uy * u, 0.3), ang, 0.1)
    E.box(PAVE, mx, my, 0.3, mw - 2 * dep, md - 2 * dep, 0.12)
    # sanctuary with the great Buddha (a hall on the north side of the stupa court)
    E.box(MUD_LT, -20, 34, 0.3, 22, 10, 7.5)
    E.box(MUD_DK, -20, 34, 7.8, 22.4, 10.4, 0.5)
    E.panel(DARK, arch_outline(4.0, 5.2), (-20, 28.95, 0.3), SOUTH, 0.12)
    for i in range(4):
        tree_b(E, -38 + i * 4, -36, 0.3, 1.3)
    m.add(1, E.build(), "monastery")
    S = Batch("st_stupa")
    x, y = -20.0, 4.0
    S.box(MUD, x, y, 0.45, 24, 24, 3.2)
    S.box(MUD_LT, x, y, 3.65, 25, 25, 0.4)
    S.box(MUD, x, y, 4.05, 18.5, 18.5, 3.0)
    S.box(MUD_LT, x, y, 7.05, 19.3, 19.3, 0.4)
    for ang, (cx, cy) in ((SOUTH, (x, y - 12)), (NORTH, (x, y + 12)), (EAST, (x + 12, y)), (WEST, (x - 12, y))):
        for i in range(7):
            S.panel(MUD_DK, [(-1.2 + (i - 3) * 3.2, 0.6), (1.2 + (i - 3) * 3.2, 0.6), (1.2 + (i - 3) * 3.2, 2.7), (-1.2 + (i - 3) * 3.2, 2.7)], (cx, cy, 0.45), ang, 0.1)
    # stair up the south side
    for k in range(8):
        S.box(MUD_DK, x, y - 12 - 3.5 + k * 0.45, 0.45, 4.0, 4.0 - k * 0.45, 0.4 * (k + 1))
    S.lathe(MUD_LT, [(7.8, 0), (7.8, 1.8)], x, y, 7.45, 32)
    S.lathe("#E2D6BE", [(7.6, 0), (7.4, 2.4), (6.6, 5.0), (5.0, 7.0), (2.8, 8.2), (0.0, 8.6)], x, y, 9.25, 64)
    S.box(MUD_LT, x, y, 17.6, 3.0, 3.0, 1.6)
    S.box(MUD_DK, x, y, 19.2, 3.6, 3.6, 0.4)
    S.box(WOOD_DK, x, y, 19.6, 0.35, 0.35, 5.0)
    for k in range(4):
        S.lathe(BRONZE, [(1.9 - k * 0.38, 0), (1.9 - k * 0.38, 0.22)], x, y, 20.2 + k * 1.1, 12)
    # small votive stupas round the court
    for i in range(14):
        a = math.tau * (i + 0.5) / 14
        vx, vy = x + 17.5 * math.cos(a), y + 17.5 * math.sin(a)
        if vy < y - 14 and abs(vx - x) < 4:
            continue
        S.box(MUD, vx, vy, 0.45, 2.4, 2.4, 1.2)
        S.lathe("#E2D6BE", [(1.0, 0), (0.95, 0.5), (0.6, 1.1), (0.0, 1.4)], vx, vy, 1.65, 24)
        S.box(WOOD_DK, vx, vy, 3.0, 0.15, 0.15, 0.9)
    m.add(2, S.build(), "stupa")
    return m


# ---------------------------------------------------------------- Erk Kala

def erk_kala(ruin=False):
    m = Model("erk-kala" + ("-ruin" if ruin else ""))
    G = Batch("erk_mound")
    G.box(GROUND, 0, 0, 0, 520, 520, 0.3)
    if ruin:
        bump = lambda a, t: 1.0 + 0.025 * math.sin(a * 23) * t + 0.015 * math.sin(a * 7)
        G.lathe(ERODED, [(258, 0), (246, 10), (236, 19), (226, 21), (214, 16), (206, 11), (0, 11)], 0, 0, 0.3, 96, bump)
        # the breach where the old gate was
        G.frustum(GROUND, 0, -232, 0.3, 26, 30, 20, 24, 12.0)
        m.add(0, G.build(), "rampart")
        R = Batch("erk_ruin")
        for i in range(24):
            a = math.tau * i / 24
            R.lathe(ERODED, [(9, 0), (5, 4), (1.5, 6)], 232 * math.cos(a), 232 * math.sin(a), 19.0, 8)
        for i in range(14):
            R.frustum(MUD_DK, -150 + rnd(i) * 300, -140 + rnd(i, 3) * 280, 11.3, 26, 20, 12, 9, 1.5 + rnd(i, 7) * 2)
        for i in range(12):
            tree_b(R, -120 + rnd(i, 9) * 240, -120 + rnd(i, 4) * 240, 11.3, 1.5, color="#8C9A5E")
        rubble_field(R, -150, -150, 150, 150, 90, seed=101, z=11.3)
        m.add(1, R.build(), "ruins")
        return m
    # the rampart and the raised interior
    G.lathe(MUD_DK, [(258, 0), (245, 9), (234, 16), (220, 16), (212, 11), (0, 11)], 0, 0, 0.3, 96)
    # a ramp up to the south gate
    G.ramp(MUD_DK, 0, -259, -230, 14, 0.3, 16.0)
    m.add(0, G.build(), "rampart")
    W = Batch("erk_walls")
    n = 64
    pts = ring_pts(227, n, -math.pi / 2 + math.tau / n / 2)
    mud_wall(W, pts, 10.0, 6.0, MUD, True, 16.3, 0.3, True, "round", 4.4, 12.5, 24.0, True, out_sign=1, skip=(n - 1,))
    gate_towers(W, 0, -227, 7.0, 15.0, 7.0, MUD, 16.3, 5.0, depth=12.0)
    m.add(1, W.build(), "walls")
    P = Batch("erk_inner")
    z = 11.3
    # the governor's columned hall (reconstruction), granaries and houses
    P.box(MUD_LT, 0, 60, z, 50, 40, 1.4)
    P.box(MUD, 0, 66, z + 1.4, 40, 28, 9.0)
    P.box(MUD_DK, 0, 66, z + 10.4, 41, 29, 0.8)
    for i in range(8):
        P.lathe(WOOD, [(0.45, 0), (0.38, 6.0), (0.8, 6.4), (0.8, 6.8)], -17.5 + i * 5, 47, z + 1.4, 8)
    P.box(MUD_DK, 0, 47, z + 8.2, 40, 4, 0.7)
    P.box(MUD, 0, 48, z + 8.9, 40, 6, 0.4)
    for k in range(6):
        P.box(MUD_LT, -110 + k * 18, 100, z, 13, 36, 6.0)
        P.lathe(MUD_LT, [(6.5, 0), (5.0, 2.2), (0.0, 3.4)], -110 + k * 18, 100, z + 6.0, 8)
    house_grid(P, -160, -150, -30, -20, seed=1, cell=14, color=MUD, z=z)
    house_grid(P, 30, -150, 160, -20, seed=8, cell=14, color=MUD, z=z)
    house_grid(P, 60, 10, 170, 110, seed=4, cell=14, color=MUD, z=z)
    house_grid(P, -175, -10, -60, 70, seed=6, cell=14, color=MUD, z=z)
    P.seg(PAVE_DK, 0, -220, 0, 40, z, 9, 9, 0.12)
    m.add(2, P.build(), "citadel")
    return m


# ---------------------------------------------------------------- the Kyz Kalas

def kyz_kala(big=True):
    m = Model("great-kyz-kala" if big else "small-kyz-kala")
    W, D = (42.0, 37.0) if big else (19.0, 17.0)
    FW, FD = (52.0, 58.0) if big else (30.0, 28.0)
    ph, bh = (4.0, 9.0) if big else (2.5, 7.0)
    G = Batch("kk_ground")
    G.box(GROUND, 0, 0, 0, FW, FD, 0.3)
    # the sloping plinth
    G.frustum(MUD_DK, 0, 0, 0.3, W + (8 if big else 5), D + (8 if big else 5), W + 1.0, D + 1.0, ph)
    for i in range(6 if big else 3):
        tree_b(G, -FW / 2 + 3 + i * (FW - 6) / max(1, (5 if big else 2)), -FD / 2 + 2.5, 0.3, 1.1 if big else 0.9, "poplar")
    m.add(0, G.build(), "plinth")
    B = Batch("kk_body")
    r, sp = (1.15, 2.3) if big else (0.85, 1.7)
    corrugated_block(B, W, D, ph + 0.3, bh, r, sp, MUD, MUD_LT, n=12 if big else 16)
    if not big:
        for i in range(12):
            tree_b(B, -13 + (i % 6) * 5.2, 9.5 + (i // 6) * 3.5, 0.3, 0.9)
    z = ph + 0.3 + bh
    # roof with the opening of the court and stubs of the upper rooms
    B.box(DARK, 0, 0, z + 0.3, W * 0.28, D * 0.3, 0.7)
    if big:
        for s in (-1, 1):
            B.box(MUD, s * (W * 0.32), 0, z + 0.9, W * 0.18, D * 0.7, 2.2)
            B.box(MUD, 0, s * D * 0.3, z + 0.9, W * 0.4, D * 0.16, 1.8)
    # windows high in the walls
    for ang, (cx, cy), L in ((SOUTH, (0, -D / 2 - r), W), (NORTH, (0, D / 2 + r), W), (EAST, (W / 2 + r, 0), D), (WEST, (-W / 2 - r, 0), D)):
        for i in range(3 if big else 1):
            u = (i - (1 if big else 0)) * L * 0.3 if big else 0.0
            ux, uy = -math.sin(ang), math.cos(ang)
            B.panel(DARK, [(-0.35, 0), (0.35, 0), (0.35, 1.8), (-0.35, 1.8)], (cx + ux * u, cy + uy * u, z - 3.2), ang, 0.1, 0.05)
    # the ramp to the door in the south side
    rl = 10.0 if big else 5.0
    B.seg(MUD_DK, 0, -D / 2 - rl, 0, -D / 2 - 1, 0.3, 3.5 if big else 2.4, 3.0 if big else 2.0, 0.4)
    for k in range(6):
        B.box(MUD_DK, 0, -D / 2 - rl + rl * (k + 0.5) / 6, 0.3, 3.4 if big else 2.2, rl / 6, ph * (k + 1) / 6)
    B.panel(DARK, arch_outline(2.0 if big else 1.3, 3.2 if big else 2.2), (0, -D / 2 - r - 0.1, ph + 0.3), SOUTH, 0.3)
    m.add(1, B.build(), "corrugated walls")
    return m


# ---------------------------------------------------------------- Muhammad ibn Zayd

def muhammad_ibn_zayd():
    m = Model("muhammad-ibn-zayd")
    G = Batch("miz_ground")
    G.box(GROUND, 0, 0, 0, 24, 30, 0.3)
    for (x, y, w, d) in ((0, -14.6, 24, 0.8), (0, 14.6, 24, 0.8), (-11.6, 0, 0.8, 30), (11.6, 0, 0.8, 30)):
        G.box(MUD, x, y, 0.3, w, d, 1.6)
    gravestones(G, -10, -13, -5.5, 12, 14, seed=21)
    gravestones(G, 5.5, -13, 10, -6, 6, seed=29)
    gravestones(G, 5.5, 11, 10, 13, 3, seed=35)
    tree_b(G, 8.5, -11, 0.3, 1.2, "poplar")
    tree_b(G, -8.5, 11, 0.3, 1.2)
    m.add(0, G.build(), "court")
    B = Batch("miz_body")
    cy = 4.0
    B.box(BRICK_S, 0, cy, 0.3, 13, 13, 8.5)
    for ang, (cx, cyy) in ((NORTH, (0, cy + 6.5)), (EAST, (6.5, cy)), (WEST, (-6.5, cy))):
        B.panel(BRICK_SD, arch_outline(6.0, 6.8), (cx, cyy, 0.3), ang, 0.18)
        lozenge_field(B, (cx, cyy, 0.3), ang, -2.6, 2.6, 0.6, 5.6, 0.75, (BRICK_SL, BRICK_SD), 0.18, 0.55, 0.08)
        kufic_band(B, (cx, cyy, 0.3), ang, -6.3, 6.3, 7.2, 8.2, BRICK_SD, BRICK_SL, 0.0, 0.8)
    # entrance hall and portal on the south
    B.box(BRICK_S, 0, cy - 9.5, 0.3, 9, 6, 7.0)
    brick_portal(B, 0, cy - 12.5, 0.3, 9.4, 9.0, 1.6, SOUTH)
    kufic_band(B, (0, cy - 6.5, 0.3), SOUTH, -6.3, -4.6, 7.2, 8.2, BRICK_SD, BRICK_SL, 0.0, 0.8)
    kufic_band(B, (0, cy - 6.5, 0.3), SOUTH, 4.6, 6.3, 7.2, 8.2, BRICK_SD, BRICK_SL, 0.0, 0.8)
    B.box(BRICK_SL, 0, cy, 8.8, 13.4, 13.4, 0.5)
    B.prism(BRICK_S, ngon(6.4, 8), 9.3, 1.6, 0, cy)
    for i in range(8):
        a = math.tau * i / 8
        B.panel(DARK, arch_outline(0.9, 1.1), (6.4 * math.cos(math.pi / 8) * math.cos(a), cy + 6.4 * math.cos(math.pi / 8) * math.sin(a), 9.5), a, 0.06)
    pointed_dome(B, 5.6, 0, cy, 10.9, BRICK_SL, height=1.0, n=36, rings=10, finial=BRONZE)
    m.add(1, B.build(), "mausoleum")
    return m


# ---------------------------------------------------------------- the ice house

def yakhdan():
    m = Model("yakhdan")
    G = Batch("yk_ground")
    G.box(GROUND, 0, 0, 0, 60, 44, 0.3)
    # freezing pools north of the shade wall, a channel from the canal
    for k in range(3):
        G.box(PAVE_DK, -16 + k * 16, -10, 0.3, 14.5, 9, 0.25)
        G.box("#9FC0C4", -16 + k * 16, -10, 0.55, 13.5, 8, 0.1)
    G.box(WATER_C, 0, -4.5, 0.3, 52, 1.0, 0.35)
    G.box(WATER_C, 27.5, 4, 0.3, 1.0, 18, 0.35)
    m.add(0, G.build(), "pools")
    W = Batch("yk_wall")
    W.seg(MUD, -28, -17, 28, -17, 0.3, 2.6, 1.4, 9.0)
    for i in range(11):
        W.box(MUD_DK, -25 + i * 5, -18.4, 0.3, 1.8, 1.4, 7.5)
    W.box(MUD, -29, -12, 0.3, 1.2, 10, 5.0)
    W.box(MUD, 29, -12, 0.3, 1.2, 10, 5.0)
    m.add(1, W.build(), "shade wall")
    D = Batch("yk_dome")
    x, y = 0.0, 9.0
    D.lathe(MUD, [(11.5, 0), (11.2, 2.8)], x, y, 0.3, 36)
    prof = []
    steps = 9
    for k in range(steps):
        r0 = 10.6 * (1 - k / steps) ** 1.15
        r1 = 10.6 * (1 - (k + 1) / steps) ** 1.15
        z0 = 2.8 + k * 1.55
        prof += [(r0, z0), (r0 * 0.985, z0 + 1.2), (r1 + 0.25, z0 + 1.35)]
    prof.append((0.0, 2.8 + steps * 1.55 + 0.4))
    D.lathe(MUD_LT, prof, x, y, 0.3, 64)
    D.lathe(MUD_DK, [(0.6, 0), (0.5, 1.2), (0.0, 1.6)], x, y, 2.8 + steps * 1.55 + 0.6, 8)
    # entrance passage on the south and straw stacks
    D.box(MUD, x, y - 12, 0.3, 4.0, 4.0, 3.6)
    D.panel(DARK, arch_outline(1.8, 2.8), (x, y - 14.05, 0.3), SOUTH, 0.12)
    for i in range(4):
        D.lathe(STRAW, [(1.6, 0), (1.5, 1.4), (0.0, 2.4)], -22 + i * 3.6, 16, 0.3, 8)
    tree_b(D, 22, 16, 0.3, 1.3, "poplar")
    tree_b(D, 25, 12, 0.3, 1.1)
    m.add(2, D.build(), "dome")
    return m


# ---------------------------------------------------------------- the Askhab mausolea

def tim_portal(B, x, y, z, w, h, depth, ang=SOUTH):
    """A Timurid iwan: brick body with turquoise and cobalt tile frames, banna'i fields and a deep blue arch."""
    brick_portal(B, x, y, z, w, h, depth, ang, BRICK_SL, TURQ, COBALT, tile=(TURQ, COBALT))
    ux, uy = -math.sin(ang), math.cos(ang)
    nx, ny = math.cos(ang), math.sin(ang)
    for s in (-1, 1):
        gx, gy = x + ux * s * w / 2 - nx * 0.6, y + uy * s * w / 2 - ny * 0.6
        B.lathe(TURQ, [(0.7, 0), (0.62, h * 1.04)], gx, gy, z, 10)
        for k in range(1, 5):
            B.lathe(COBALT, [(0.74, h * k / 5), (0.74, h * k / 5 + 0.5)], gx, gy, z, 10)
        B.lathe(TWHITE, [(0.85, h * 1.04), (0.0, h * 1.04 + 1.6)], gx, gy, z, 10)


def askhab():
    m = Model("askhab")
    G = Batch("ask_ground")
    G.box(GROUND, 0, 0, 0, 60, 44, 0.3)
    G.box(PAVE, 0, -2, 0.3, 54, 34, 0.8)
    for k in range(5):
        G.box(PAVE_DK, 0, -19 - 0.6 + k * 0.2, 0.3, 14, 1.2, 0.16 * (k + 1))
    for i in range(6):
        tree_b(G, -27 + (i % 2) * 54, -16 + (i // 2) * 12, 0.3, 1.4, "poplar")
    m.add(0, G.build(), "terrace")
    B = Batch("ask_iwans")
    for s in (-1, 1):
        x = s * 13
        tim_portal(B, x, 6, 1.1, 18, 17, 7, SOUTH)
        # the tomb in the open before the iwan: stepped base and a long sarcophagus
        B.box(MUD_LT, x, -6, 1.1, 6.0, 9.0, 0.6)
        B.box(PAVE_DK, x, -6, 1.7, 4.4, 7.4, 0.6)
        B.box(TWHITE, x, -6, 2.3, 1.8, 5.2, 1.0)
        B.seg(TWHITE, x, -8.5, x, -3.5, 3.3, 1.8, 0.2, 0.7)
        for k in range(4):
            B.box(WOOD_DK, x + (k % 2 * 2 - 1) * 2.6, -6 + (k // 2 * 2 - 1) * 4.2, 1.7, 0.2, 0.2, 2.6)
    # the small pilgrims' mosque at the back
    B.box(BRICK_SL, 0, 15, 1.1, 10, 8, 6)
    pointed_dome(B, 3.6, 0, 15, 7.1, TURQ, height=1.1, n=32, rings=10, finial=GILT)
    m.add(1, B.build(), "iwans")
    C = Batch("ask_cemetery")
    gravestones(C, -26, -17, -18, 10, 28, seed=3, z=1.1)
    gravestones(C, 18, -17, 26, 10, 28, seed=8, z=1.1)
    gravestones(C, -6, -16, 6, -10, 8, seed=14, z=1.1)
    m.add(2, C.build(), "graves")
    return m


# ---------------------------------------------------------------- Abdullah Khan Kala

def abdullah_khan_kala():
    """A stretch of the Timurid wall with its north gate; built facing -Y (the landmark is turned 180 degrees)."""
    m = Model("abdullah-khan-kala")
    G = Batch("akk_ground")
    G.box(GROUND, 0, 0, 0, 200, 60, 0.3)
    G.box(WATER_C, 0, -22, 0.0, 200, 6, 0.35)
    G.box(PAVE_DK, 0, -22, 0.0, 8, 8, 0.6)
    G.seg(PAVE_DK, 0, -30, 0, 30, 0.3, 7, 7, 0.1)
    m.add(0, G.build(), "ground")
    W = Batch("akk_walls")
    wy = -6.0
    mud_wall(W, [(-94, wy), (-12, wy)], 10.0, 5.5, MUD_LT, False, 0.3, 0.4, True, "round", 4.0, 12.0, 30.0, True, out_sign=1)
    mud_wall(W, [(12, wy), (94, wy)], 10.0, 5.5, MUD_LT, False, 0.3, 0.4, True, "round", 4.0, 12.0, 30.0, True, out_sign=1)
    m.add(1, W.build(), "walls")
    Gt = Batch("akk_gate")
    for s in (-1, 1):
        Gt.lathe(MUD_LT, [(6.4, 0), (5.8, 14.0)], s * 11, wy - 1, 0.3, 16)
        Gt.lathe(BRICK_SL, [(6.0, 14.0), (6.0, 15.2)], s * 11, wy - 1, 0.3, 16)
        for k in range(10):
            a = math.tau * k / 10
            Gt.box(MUD_LT, s * 11 + 5.4 * math.cos(a), wy - 1 + 5.4 * math.sin(a), 15.5, 1.1, 1.1, 1.2, a)
    Gt.box(BRICK_SL, 0, wy, 0.3, 12, 14, 13)
    tim_portal(Gt, 0, wy - 7.05, 0.3, 11, 13.5, 1.0, SOUTH)
    m.add(2, Gt.build(), "gate")
    T = Batch("akk_town")
    house_grid(T, -95, 6, -12, 28, seed=60, cell=11, color=MUD)
    house_grid(T, 12, 6, 95, 28, seed=70, cell=11, color=MUD)
    for i in range(8):
        tree_b(T, -90 + i * 25 if i < 4 else 15 + (i - 4) * 25, -28, 0.3, 1.2, "poplar")
    m.add(3, T.build(), "houses")
    return m


# ---------------------------------------------------------------- the Majan weir

def majan_dam():
    m = Model("majan-dam")
    G = Batch("md_ground")
    G.box(GROUND, 0, 0, 0, 70, 40, 0.3)
    # the canal running north (along Y), wider above the weir where water is held back
    G.box(WATER_C, 0, 10, 0.05, 18, 20, 0.35)
    G.box(WATER_C, 0, -10, 0.05, 12, 20, 0.3)
    for s in (-1, 1):
        G.seg(MUD_DK, s * 10, -20, s * 10, 20, 0.3, 3.5, 1.5, 1.6)
    m.add(0, G.build(), "canal")
    B = Batch("md_weir")
    B.box(BRICK_S, 0, 0, 0.0, 26, 4.0, 3.6)
    B.box(BRICK_SL, 0, 0, 3.6, 26.4, 4.4, 0.4)
    for i in range(4):
        x = -7.5 + i * 5
        B.rect(DARK, (x, -2.0, 0.0), SOUTH, -1.4, 1.4, 0.1, 2.4, 0.1)
        B.box(WOOD_DK, x - 1.6, -0.2, 4.0, 0.35, 0.35, 2.4)
        B.box(WOOD_DK, x + 1.6, -0.2, 4.0, 0.35, 0.35, 2.4)
        B.box(WOOD, x, -0.2, 6.2, 3.6, 0.4, 0.4)
        B.box(WOOD, x, -0.2, 2.0 + (i % 2) * 1.2, 2.8, 0.25, 1.4)
        B.box("#8FB4B8", x, -2.6, 0.35, 2.4, 1.2, 0.35)
    # gatekeeper's hut, brushwood stores and a gauge post
    flat_houses(B, [(22, 8, 7, 6, 3.2), (-22, -10, 6, 5, 2.8)])
    for i in range(5):
        B.box(STRAW, -24 + (i % 3) * 3.2, 8 + (i // 3) * 3, 0.3, 2.6, 1.6, 1.2)
    B.box(WOOD_DK, 6, 4, 0.0, 0.3, 0.3, 4.5)
    for k in range(4):
        B.box(TWHITE, 6, 3.84, 0.6 + k * 1.0, 0.36, 0.05, 0.12)
    for i in range(4):
        tree_b(B, 26 - (i % 2) * 6, -14 + (i // 2) * 6, 0.3, 1.3, "poplar")
    F = Batch("md_fields")
    for s in (-1, 1):
        for k in range(9):
            F.box("#8FA05E" if k % 2 else "#A99A66", s * 22, -18 + 1.5 + k * 1.6, 0.3, 14, 0.9, 0.25)
        for k in range(36):
            F.lathe("#D8B848" if k % 3 else "#9DB05A", [(0.45, 0), (0.45, 0.35), (0.0, 0.6)], s * 22 - 6 + (k % 6) * 2.4, -17 + (k // 6) * 2.6, 0.55, 8)
    for k in range(10):
        F.box(BRICK_SD, -10.6 if k % 2 else 10.6, -18 + (k // 2) * 8, 0.3, 1.2, 3.5, 1.9)
        tree_b(F, -13.5 if k % 2 else 13.5, -16 + (k // 2) * 8, 0.3, 1.0, "poplar" if k % 3 else "round")
    m.add(2, F.build(), "fields")
    m.add(1, B.build(), "weir")
    return m


BUILDERS = {
    "merv/sanjar-mausoleum": sanjar_mausoleum,
    "merv/friday-mosque": friday_mosque,
    "merv/shahriyar-ark": lambda: shahriyar_ark(False),
    "merv/shahriyar-ark-ruin": lambda: shahriyar_ark(True),
    "merv/sultan-kala-walls": lambda: sultan_kala_walls(False),
    "merv/sultan-kala-walls-ruin": lambda: sultan_kala_walls(True),
    "merv/gyaur-kala-walls": lambda: gyaur_kala_walls(False),
    "merv/gyaur-kala-walls-ruin": lambda: gyaur_kala_walls(True),
    "merv/beni-makhan": beni_makhan,
    "merv/stupa": stupa_monastery,
    "merv/erk-kala": lambda: erk_kala(False),
    "merv/erk-kala-ruin": lambda: erk_kala(True),
    "merv/great-kyz-kala": lambda: kyz_kala(True),
    "merv/small-kyz-kala": lambda: kyz_kala(False),
    "merv/muhammad-ibn-zayd": muhammad_ibn_zayd,
    "merv/yakhdan": yakhdan,
    "merv/askhab": askhab,
    "merv/abdullah-khan-kala": abdullah_khan_kala,
    "merv/majan-dam": majan_dam,
}
