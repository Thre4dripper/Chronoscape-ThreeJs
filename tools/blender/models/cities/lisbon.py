"""Lisbon landmark miniatures: the castle hill in four states, the Romanesque Sé, the Roman theatre, the Moorish and
Fernandine gates, the Manueline riverfront (Paço da Ribeira, Casa da Índia, the Ribeira das Naus with a carrack on the
slipway), the Rossio's hospital and Estaus palace, the Carmo and São Roque, the Misericórdia portal, the Casa dos Bicos,
the Chafariz d'El-Rei, the Ópera do Tejo, São Vicente de Fora and Pombal's Praça do Comércio.

Conventions as in FORMAT.md: metres, origin at the ground centre, +X east, +Y north, +Z up, the main front toward -Y;
the landmark rotation turns it on the map. Repetitive parts are accumulated in a Buf (one mesh per colour).
"""
import math
import bpy
from chronokit import Model, box, cylinder, dome, join, shade, gable_roof, hip_roof, mesh_from, ellipse_ring
from worldkit import *

# ---------------------------------------------------------------- palette
LIOZ = "#E9E2D2"         # Lisbon's pale lioz limestone
LIOZ_D = "#D2C8B2"
STONE = "#CDBF9F"        # rubble masonry, plastered and weathered
STONE_D = "#AFA184"
CASTLE = "#BDAE8C"
CASTLE_D = "#A29372"
EARTH = "#B89A70"        # rammed earth
TILE = "#B4643F"
TILE_D = "#94512F"
TILE_L = "#C77B54"
LIME = "#F1ECE0"         # whitewash
OCHRE = "#E2C27E"        # Pombaline yellow ochre
POMBAL = "#E8D8B4"
AZUL = "#3F68A0"         # azulejo blue
AZUL_L = "#8DA9C9"
TEAL = "#4C8C88"
GROUND = "#C9B48E"
PAVE = "#D9CCAE"
SAND = "#D8C79F"
YARD = "#BFA67C"
GRASS = "#8E9C68"
LEAF = "#5C7F4B"
PINE = "#4A6A44"
TRUNK = "#76583C"
WOOD = "#7A5A3A"
WOOD_D = "#5A422C"
HULL = "#6B4A30"
SAIL = "#EFE6D0"
RED = "#A8342A"
GOLD = "#D2AE52"
BRONZE_D = "#5E5440"
LEADC = "#7F8891"
GLASS = "#3B4A66"
HOUSES = ["#EFE6D2", "#E9D2B4", "#F2EDE2", "#E3C9A0", "#DDE0D8", "#EAD9BE", "#D9C7E0"]
FACE_ROT = {"S": 0, "N": 180, "E": 90, "W": -90}


# ---------------------------------------------------------------- mesh accumulator
class Buf:
    """Collects many simple solids into one mesh (one colour)."""

    def __init__(self):
        self.v, self.f = [], []

    def hexa(self, c):
        b = len(self.v)
        self.v += [tuple(p) for p in c]
        self.f += [(b, b + 3, b + 2, b + 1), (b + 4, b + 5, b + 6, b + 7), (b, b + 1, b + 5, b + 4), (b + 1, b + 2, b + 6, b + 5),
                   (b + 2, b + 3, b + 7, b + 6), (b + 3, b, b + 4, b + 7)]

    def box(self, cx, cy, z, w, d, h, ang=0.0):
        ca, sa = math.cos(ang), math.sin(ang)
        pts = [(-w / 2, -d / 2), (w / 2, -d / 2), (w / 2, d / 2), (-w / 2, d / 2)]
        pts = [(cx + x * ca - y * sa, cy + x * sa + y * ca) for x, y in pts]
        self.hexa([(x, y, z) for x, y in pts] + [(x, y, z + h) for x, y in pts])

    def box2(self, x0, y0, x1, y1, z0, z1):
        self.box((x0 + x1) / 2, (y0 + y1) / 2, z0, abs(x1 - x0), abs(y1 - y0), z1 - z0)

    def frustum(self, cx, cy, z, w0, d0, w1, d1, h):
        self.hexa([(cx - w0 / 2, cy - d0 / 2, z), (cx + w0 / 2, cy - d0 / 2, z), (cx + w0 / 2, cy + d0 / 2, z), (cx - w0 / 2, cy + d0 / 2, z),
                   (cx - w1 / 2, cy - d1 / 2, z + h), (cx + w1 / 2, cy - d1 / 2, z + h), (cx + w1 / 2, cy + d1 / 2, z + h), (cx - w1 / 2, cy + d1 / 2, z + h)])

    def prism(self, pts, z0, z1):
        b = len(self.v)
        n = len(pts)
        self.v += [(x, y, z0) for x, y in pts] + [(x, y, z1) for x, y in pts]
        self.f.append(tuple(range(b, b + n))[::-1])
        self.f.append(tuple(range(b + n, b + 2 * n)))
        for i in range(n):
            j = (i + 1) % n
            self.f.append((b + i, b + j, b + n + j, b + n + i))

    def lathe(self, prof, cx, cy, z0, n=8, start=0.0):
        """Solid of revolution from [(r, z), ...]; r = 0 at either end closes to a point."""
        rings = []
        for r, z in prof:
            if r <= 1e-6:
                rings.append([len(self.v)])
                self.v.append((cx, cy, z0 + z))
            else:
                ring = []
                for i in range(n):
                    a = start + math.tau * i / n
                    ring.append(len(self.v))
                    self.v.append((cx + r * math.cos(a), cy + r * math.sin(a), z0 + z))
                rings.append(ring)
        for A, B in zip(rings, rings[1:]):
            if len(A) == 1 and len(B) == 1:
                continue
            for i in range(n):
                j = (i + 1) % n
                if len(A) == 1:
                    self.f.append((A[0], B[i], B[j]))
                elif len(B) == 1:
                    self.f.append((A[i], A[j], B[0]))
                else:
                    self.f.append((A[i], A[j], B[j], B[i]))
        if len(rings[0]) > 1:
            self.f.append(tuple(rings[0])[::-1])
        if len(rings[-1]) > 1:
            self.f.append(tuple(rings[-1]))

    def beam(self, p0, p1, side, w, t):
        """A box from p0 to p1: width w along `side`, thickness t along the third direction."""
        d = [p1[i] - p0[i] for i in range(3)]
        sl = math.sqrt(sum(c * c for c in side)) or 1.0
        e1 = [c / sl * w / 2 for c in side]
        n = [d[1] * side[2] - d[2] * side[1], d[2] * side[0] - d[0] * side[2], d[0] * side[1] - d[1] * side[0]]
        nl = math.sqrt(sum(c * c for c in n)) or 1.0
        e2 = [c / nl * t / 2 for c in n]
        c = []
        for p in (p0, p1):
            for s1, s2 in ((-1, -1), (1, -1), (1, 1), (-1, 1)):
                c.append(tuple(p[i] + s1 * e1[i] + s2 * e2[i] for i in range(3)))
        self.hexa(c)

    def gable_y(self, cx, y0, y1, w, z, h, over=0.3):
        """A gable roof with its ridge along Y."""
        W = w / 2 + over
        b = len(self.v)
        self.v += [(cx - W, y0, z), (cx + W, y0, z), (cx, y0, z + h), (cx - W, y1, z), (cx + W, y1, z), (cx, y1, z + h)]
        self.f += [(b, b + 1, b + 2), (b + 5, b + 4, b + 3), (b, b + 3, b + 4, b + 1), (b + 1, b + 4, b + 5, b + 2), (b + 2, b + 5, b + 3, b)]

    def gable_x(self, cy, x0, x1, d, z, h, over=0.3):
        D = d / 2 + over
        b = len(self.v)
        self.v += [(x0, cy - D, z), (x0, cy + D, z), (x0, cy, z + h), (x1, cy - D, z), (x1, cy + D, z), (x1, cy, z + h)]
        self.f += [(b, b + 1, b + 2), (b + 5, b + 4, b + 3), (b, b + 3, b + 4, b + 1), (b + 1, b + 4, b + 5, b + 2), (b + 2, b + 5, b + 3, b)]

    def hip(self, cx, cy, w, d, z, h, over=0.4):
        """A hipped roof over a w x d rectangle, the ridge along the longer side."""
        W, D = w / 2 + over, d / 2 + over
        b = len(self.v)
        if w >= d:
            r = max(0.0, W - D)
            self.v += [(cx - W, cy - D, z), (cx + W, cy - D, z), (cx + W, cy + D, z), (cx - W, cy + D, z), (cx - r, cy, z + h), (cx + r, cy, z + h)]
            self.f += [(b + 3, b + 2, b + 1, b), (b, b + 1, b + 5, b + 4), (b + 1, b + 2, b + 5), (b + 2, b + 3, b + 4, b + 5), (b + 3, b, b + 4)]
        else:
            r = max(0.0, D - W)
            self.v += [(cx - W, cy - D, z), (cx + W, cy - D, z), (cx + W, cy + D, z), (cx - W, cy + D, z), (cx, cy - r, z + h), (cx, cy + r, z + h)]
            self.f += [(b + 3, b + 2, b + 1, b), (b, b + 1, b + 4), (b + 1, b + 2, b + 5, b + 4), (b + 2, b + 3, b + 5), (b + 3, b, b + 4, b + 5)]

    def lean(self, x0, y0, x1, y1, z_lo, z_hi, high_side):
        """A mono-pitch roof slab over a rectangle, high along one side (N, S, E or W)."""
        def zz(x, y):
            return {"N": z_lo + (z_hi - z_lo) * (y - y0) / (y1 - y0), "S": z_hi - (z_hi - z_lo) * (y - y0) / (y1 - y0),
                    "E": z_lo + (z_hi - z_lo) * (x - x0) / (x1 - x0), "W": z_hi - (z_hi - z_lo) * (x - x0) / (x1 - x0)}[high_side]
        pts = [(x0, y0), (x1, y0), (x1, y1), (x0, y1)]
        self.hexa([(x, y, zz(x, y) - 0.25) for x, y in pts] + [(x, y, zz(x, y)) for x, y in pts])

    def slab(self, uv, face, c_along, c_normal, z0, t):
        """Extrude an outline [(u, v)] (u along the wall, v up) through thickness t on a wall face.
        face S/N: the wall plane is y = c_normal, u along X; face E/W: x = c_normal, u along Y."""
        n = len(uv)
        b = len(self.v)
        for s in (-t / 2, t / 2):
            for u, v in uv:
                if face in "SN":
                    self.v.append((c_along + u, c_normal + s, z0 + v))
                else:
                    self.v.append((c_normal + s, c_along + u, z0 + v))
        self.f.append(tuple(range(b, b + n)))
        self.f.append(tuple(range(b + 2 * n - 1, b + n - 1, -1)))
        for i in range(n):
            j = (i + 1) % n
            self.f.append((b + i, b + n + i, b + n + j, b + j))

    def merge(self, other, deg=0.0, dx=0.0, dy=0.0, dz=0.0):
        a = math.radians(deg)
        ca, sa = math.cos(a), math.sin(a)
        b = len(self.v)
        self.v += [(x * ca - y * sa + dx, x * sa + y * ca + dy, z + dz) for x, y, z in other.v]
        self.f += [tuple(i + b for i in f) for f in other.f]

    def mesh(self, name, color):
        if not self.f:
            return None
        return mesh_from(name, self.v, self.f, (0, 0, 0), color)


class Bufs(dict):
    """A Buf per colour."""

    def __missing__(self, color):
        self[color] = Buf()
        return self[color]

    def objects(self, name):
        return [b.mesh(f"{name}_{i}", c) for i, (c, b) in enumerate(self.items()) if b.f]

    def join(self, name):
        objs = [o for o in self.objects(name) if o is not None]
        return join(objs, name) if objs else None

    def merge(self, other, deg=0.0, dx=0.0, dy=0.0, dz=0.0):
        for c, b in other.items():
            self[c].merge(b, deg, dx, dy, dz)


# ---------------------------------------------------------------- small helpers
def place(o, ang=0.0, x=0.0, y=0.0, z=0.0):
    """Rotate an object built at the origin (degrees counter-clockwise from above), then move it."""
    if ang:
        o = rot(o, ang)
    if x or y or z:
        o = move(o, x, y, z)
    return o


def arch_uv(w, h, kind="round", n=8):
    """Outline (u, v) of an arched opening w wide and h high, base at v = 0. kind: round | pointed | flat."""
    if kind == "flat":
        return [(-w / 2, 0), (w / 2, 0), (w / 2, h), (-w / 2, h)]
    if kind == "pointed":
        rect = max(0.0, h - w * 0.8)
        pts = [(-w / 2, 0), (w / 2, 0), (w / 2, rect)]
        for i in range(1, n // 2 + 1):
            a = math.pi / 2 * i / (n // 2)
            pts.append((w / 2 - w * (1 - math.cos(a)) * 0.5, rect + (h - rect) * math.sin(a)))
        pts[-1] = (0, h)
        for i in range(n // 2 - 1, 0, -1):
            u, v = pts[3 + i - 1]
            pts.append((-u, v))
        pts.append((-w / 2, rect))
        return pts
    rect = max(0.0, h - w / 2)
    pts = [(-w / 2, 0), (w / 2, 0)]
    for i in range(n + 1):
        a = math.pi * i / n
        pts.append((w / 2 * math.cos(a), rect + w / 2 * math.sin(a)))
    return pts


def opening(B, face, along, normal, z, w, h, kind="round", color=DARK, t=0.3):
    """A dark arched recess on a wall face, centred at `along`; `normal` is the wall's outer plane coordinate."""
    off = {"S": -0.05, "N": 0.05, "E": 0.05, "W": -0.05}[face]
    B[color].slab(arch_uv(w, h, kind), face, along, normal + off, z, t)


def openings(B, face, a0, a1, normal, z, w, h, n, kind="round", color=DARK, t=0.3, skip=()):
    for i in range(n):
        if i in skip:
            continue
        u = a0 + (a1 - a0) * (i + 0.5) / n
        opening(B, face, u, normal, z, w, h, kind, color, t)


def win_rows(B, x0, y0, x1, y1, z_list, h, spacing, w=1.2, faces="SNEW", kind="flat", color=DARK, skip_mid=0.0, frame=None):
    """Rows of windows on the faces of a rectangular block, one row per z in z_list."""
    for f in faces:
        if f in "SN":
            L, a0, nrm = x1 - x0, x0, (y0 if f == "S" else y1)
        else:
            L, a0, nrm = y1 - y0, y0, (x1 if f == "E" else x0)
        n = max(1, int(L / spacing))
        for z in z_list:
            for i in range(n):
                u = a0 + L * (i + 0.5) / n
                if skip_mid and abs(u - (a0 + L / 2)) < skip_mid:
                    continue
                if frame:
                    opening(B, f, u, nrm, z - 0.25, w + 0.6, h + 0.5, kind, frame, 0.14)
                opening(B, f, u, nrm, z, w, h, kind, color, 0.2)


def box_merlons(Bb, x0, y0, x1, y1, z, size=1.0, gap=0.9, sides="SNEW", t=0.8):
    step = size + gap
    for side in sides:
        if side in "SN":
            y = y0 + t / 2 if side == "S" else y1 - t / 2
            n = max(1, int((x1 - x0) / step))
            for i in range(n):
                Bb.box(x0 + (i + 0.5) * (x1 - x0) / n, y, z, size, t, size * 1.1)
        else:
            x = x0 + t / 2 if side == "W" else x1 - t / 2
            n = max(1, int((y1 - y0) / step))
            for i in range(n):
                Bb.box(x, y0 + (i + 0.5) * (y1 - y0) / n, z, t, size, size * 1.1)


def capped_merlons(Bb, x0, y0, x1, y1, z, size=0.9, gap=0.8, sides="SNEW", t=0.7):
    """Andalusi merlons with pyramidal caps (as on the castle and the Sé)."""
    step = size + gap
    for side in sides:
        horiz = side in "SN"
        L = (x1 - x0) if horiz else (y1 - y0)
        n = max(1, int(L / step))
        for i in range(n):
            u = (x0 if horiz else y0) + (i + 0.5) * L / n
            x, y = (u, (y0 + t / 2 if side == "S" else y1 - t / 2)) if horiz else ((x0 + t / 2 if side == "W" else x1 - t / 2), u)
            Bb.box(x, y, z, size if horiz else t, t if horiz else size, size * 0.9)
            Bb.lathe([(size * 0.5, 0), (0, size * 0.55)], x, y, z + size * 0.9, 4, math.pi / 4)


def wall_line(B, pts, h, t, color, z=0.0, merl=True, cap=False, msize=0.9):
    """A plain wall along a polyline in one Buf colour, with merlons."""
    for (ax, ay), (bx, by) in zip(pts, pts[1:]):
        L = math.hypot(bx - ax, by - ay)
        a = math.atan2(by - ay, bx - ax)
        B[color].box((ax + bx) / 2, (ay + by) / 2, z, L + t * 0.5, t, h, a)
        if merl:
            n = max(1, int(L / (msize * 2.0)))
            for k in range(n):
                u = -L / 2 + (k + 0.5) * L / n
                mx, my = (ax + bx) / 2 + math.cos(a) * u, (ay + by) / 2 + math.sin(a) * u
                B[color].box(mx, my, z + h, msize, t * 0.8, msize * 1.1, a)
                if cap:
                    B[color].lathe([(msize * 0.5, 0), (0, msize * 0.55)], mx, my, z + h + msize * 1.1, 4, a + math.pi / 4)


def sq_tower(B, x, y, w, h, color, top="merlons", roof=TILE, z=0.0, d=None):
    d = d or w
    B[color].box(x, y, z, w, d, h)
    B[shade(color, -0.08)].box(x, y, z + h - 0.6, w + 0.5, d + 0.5, 0.6)
    if top == "merlons":
        box_merlons(B[color], x - w / 2, y - d / 2, x + w / 2, y + d / 2, z + h, 0.9, 0.8, "SNEW", 0.6)
    elif top == "capped":
        capped_merlons(B[color], x - w / 2, y - d / 2, x + w / 2, y + d / 2, z + h, 0.9, 0.8, "SNEW", 0.6)
    elif top == "pyramid":
        B[roof].lathe([(max(w, d) * 0.74, 0), (0, max(w, d) * 0.55)], x, y, z + h, 4, math.pi / 4)
    elif top == "hip":
        B[roof].hip(x, y, w, d, z + h, min(w, d) * 0.4, 0.4)


def tree_into(B, x, y, z, r, kind="round", leaf=LEAF):
    if kind == "pine":
        B[TRUNK].lathe([(r * 0.12, 0), (r * 0.08, r * 2.6)], x, y, z, 5)
        B[PINE].lathe([(r * 0.3, 0), (r * 1.1, r * 0.35), (r * 0.9, r * 0.75), (0, r * 0.95)], x, y, z + r * 2.3, 7)
    elif kind == "cypress":
        B[PINE].lathe([(r * 0.45, 0), (r * 0.62, r * 1.2), (r * 0.5, r * 2.8), (0, r * 4.2)], x, y, z + r * 0.2, 6)
    else:
        B[TRUNK].box(x, y, z, r * 0.24, r * 0.24, r * 0.9)
        B[leaf].lathe([(r * 0.55, 0), (r * 0.95, r * 0.35), (r, r * 0.85), (r * 0.7, r * 1.4), (0, r * 1.7)], x, y, z + r * 0.75, 7)


def house(B, x, y, w, d, h, color, roof="tile", z=0.0, door="S", windows=True):
    B[color].box(x, y, z, w, d, h)
    if roof == "tile":
        if w >= d:
            B[TILE].hip(x, y, w, d, z + h, d * 0.32, 0.3)
        else:
            B[TILE].hip(x, y, w, d, z + h, w * 0.32, 0.3)
    elif roof == "flat":
        B[shade(color, -0.08)].box(x, y, z + h, w, d, 0.4)
        B[shade(color, 0.05)].box(x, y, z + h, w - 0.8, d - 0.8, 0.45)
    if door:
        nrm = {"S": y - d / 2, "N": y + d / 2, "E": x + w / 2, "W": x - w / 2}[door]
        al = x if door in "SN" else y
        opening(B, door, al, nrm, z, min(w, d) * 0.16 + 0.6, min(2.4, h * 0.45), "flat", DARK, 0.2)
    if windows and h > 5.5:
        L = w if door in "SN" else d
        n = max(1, int(L / 3.2))
        for k in range(1, int((h - 1.5) / 3.0)):
            for i in range(n):
                u = (x if door in "SN" else y) - L / 2 + L * (i + 0.5) / n
                nrm = {"S": y - d / 2, "N": y + d / 2, "E": x + w / 2, "W": x - w / 2}[door]
                opening(B, door, u, nrm, z + k * 3.0, 0.8, 1.4, "flat", DARK, 0.15)


def rope_column(B, x, y, z, r, h, color=LIOZ, band=None, turns=3.0, seg=20, plane=None):
    """A Manueline twisted-rope column: a shaft wound with a raised spiral band, a capital and a base."""
    band = band or shade(color, -0.12)
    B[color].lathe([(r * 1.35, 0), (r * 1.35, r * 0.6), (r, r * 0.9), (r, h - r * 0.9), (r * 1.4, h - r * 0.5), (r * 1.4, h)], x, y, z, 8)
    for strand in (0.0, math.pi):
        pts = []
        for i in range(seg + 1):
            t = i / seg
            a = strand + turns * math.tau * t
            pts.append((x + r * 1.05 * math.cos(a), y + r * 1.05 * math.sin(a), z + r * 0.9 + (h - r * 1.8) * t))
        for p0, p1 in zip(pts, pts[1:]):
            mx, my = (p0[0] + p1[0]) / 2 - x, (p0[1] + p1[1]) / 2 - y
            B[band].beam(p0, p1, (mx, my, 0), r * 0.42, r * 0.4)


def pinnacle(B, x, y, z, w, h, color=LIOZ):
    B[color].box(x, y, z, w, w, h * 0.45)
    B[color].lathe([(w * 0.7, 0), (0, h * 0.55)], x, y, z + h * 0.45, 4, math.pi / 4)


def armillary(B, x, y, z, r, color=GOLD, plane="S"):
    """Manuel I's emblem: an armillary sphere (a ring with a band), shown flat on a wall."""
    n = 12
    for k in range(n):
        a0, a1 = math.tau * k / n, math.tau * (k + 1) / n
        p0 = (x + r * math.cos(a0), y, z + r * math.sin(a0)) if plane in "SN" else (x, y + r * math.cos(a0), z + r * math.sin(a0))
        p1 = (x + r * math.cos(a1), y, z + r * math.sin(a1)) if plane in "SN" else (x, y + r * math.cos(a1), z + r * math.sin(a1))
        B[color].beam(p0, p1, (0, 1, 0) if plane in "SN" else (1, 0, 0), r * 0.25, r * 0.18)
    if plane in "SN":
        B[color].beam((x - r, y, z - r * 0.35), (x + r, y, z + r * 0.35), (0, 1, 0), r * 0.25, r * 0.22)
    else:
        B[color].beam((x, y - r, z - r * 0.35), (x, y + r, z + r * 0.35), (1, 0, 0), r * 0.25, r * 0.22)


def christ_cross(B, x, y, z, s, face="S"):
    """The cross of the Order of Christ (red with a white inner cross), on a wall face or a sail."""
    t = 0.15
    if face in "SN":
        B[RED].box(x, y, z - s / 2, s * 0.32, t, s)
        B[RED].box(x, y, z - s * 0.16, s, t, s * 0.32)
        B[LIME].box(x, y - (t * 0.6 if face == "S" else -t * 0.6), z - s * 0.4, s * 0.1, t, s * 0.8)
        B[LIME].box(x, y - (t * 0.6 if face == "S" else -t * 0.6), z - s * 0.05, s * 0.8, t, s * 0.1)
    else:
        B[RED].box(x, y, z - s / 2, t, s * 0.32, s)
        B[RED].box(x, y, z - s * 0.16, t, s, s * 0.32)


def manueline_portal(B, face, along, normal, z, w, h, color=LIOZ, door_kind="round"):
    """A Manueline portal: a dark arched door framed by twisted-rope colonnettes, a carved canopy with pinnacles,
    a niche with a figure and the armillary sphere above."""
    s = {"S": -1, "N": 1, "E": 1, "W": -1}[face]
    out = normal + s * 0.5

    def P(u, n):          # (along, outward) -> (x, y)
        return (along + u, normal + s * n) if face in "SN" else (normal + s * n, along + u)

    # frame slab
    x, y = P(0, 0.25)
    if face in "SN":
        B[color].box(x, y, z, w, 0.5, h)
    else:
        B[color].box(x, y, z, 0.5, w, h)
    opening(B, face, along, out, z, w * 0.46, h * 0.5, door_kind, DARK, 0.25)
    # colonnettes either side of the door and at the frame's edges
    for u in (-w * 0.3, w * 0.3, -w * 0.47, w * 0.47):
        cx, cy = P(u, 0.75)
        rope_column(B, cx, cy, z, w * 0.035, h * (0.62 if abs(u) < w * 0.4 else 0.8), color, turns=4, seg=16)
    # the canopy band and the tympanum niche
    cx, cy = P(0, 0.7)
    if face in "SN":
        B[shade(color, -0.06)].box(cx, cy, z + h * 0.62, w * 0.75, 0.5, h * 0.06)
        B[shade(color, -0.15)].box(cx, cy + s * 0.05, z + h * 0.7, w * 0.22, 0.5, h * 0.18)
    else:
        B[shade(color, -0.06)].box(cx, cy, z + h * 0.62, 0.5, w * 0.75, h * 0.06)
        B[shade(color, -0.15)].box(cx + s * 0.05, cy, z + h * 0.7, 0.5, w * 0.22, h * 0.18)
    fx, fy = P(0, 1.0)
    B[LIME].lathe([(w * 0.04, 0), (w * 0.035, h * 0.13), (w * 0.025, h * 0.15), (0, h * 0.17)], fx, fy, z + h * 0.7, 6)
    ax, ay = P(0, 0.75)
    armillary(B, ax, ay, z + h * 0.94, w * 0.08, GOLD, face)
    for u in (-w * 0.47, -w * 0.3, w * 0.3, w * 0.47):
        px, py = P(u, 0.75)
        pinnacle(B, px, py, z + (h * 0.8 if abs(u) > w * 0.4 else h * 0.62), w * 0.06, h * 0.25, color)


# ---------------------------------------------------------------- ships
def hull_into(B, L, beam, depth, color=HULL, sheer=1.6, stern_h=4.0, bow_h=2.5, stations=18, x=0.0, y=0.0, z=0.0, ang=0.0, frame=False):
    """A carvel hull lofted along X (bow at +X), full-bodied, with sheer rising to a high stern and a lower bow.
    frame=True leaves the upper strakes off to show ribs (a ship on the slipway)."""
    sub = Buf()
    secs = []
    for i in range(stations + 1):
        t = -1 + 2 * i / stations                      # -1 stern .. +1 bow
        hw = beam / 2 * (1 - abs(t) ** 2.6) ** 0.55 if t < 0 else beam / 2 * (1 - t ** 1.8) ** 0.6
        hw = max(hw, 0.15)
        top = depth + sheer * t * t + (stern_h * max(0, -t - 0.55) / 0.45 if t < -0.55 else 0) + (bow_h * max(0, t - 0.65) / 0.35 if t > 0.65 else 0)
        bot = depth * 0.12 * abs(t) ** 3
        xx = t * L / 2
        secs.append([(xx, 0, bot), (xx, hw * 0.55, bot + depth * 0.12), (xx, hw * 0.95, depth * 0.55), (xx, hw, top),
                     (xx, -hw, top), (xx, -hw * 0.95, depth * 0.55), (xx, -hw * 0.55, bot + depth * 0.12)])
    n = 7
    for s in secs:
        sub.v += s
    for i in range(stations):
        a, b = i * n, (i + 1) * n
        for k in range(n):
            if k == 3:
                continue                                # the open deck
            k2 = (k + 1) % n
            if frame and k in (2, 4) and 0 < i < stations - 1:
                continue
            sub.f.append((a + k, b + k, b + k2, a + k2))
    e = stations * n
    sub.f.append(tuple(range(n)))
    sub.f.append(tuple(range(e + n - 1, e - 1, -1)))
    # deck
    for i in range(stations):
        a, b = i * n, (i + 1) * n
        sub.f.append((a + 4, b + 4, b + 3, a + 3)) if not frame else None
    if frame:
        for i in range(1, stations):
            xx, _, _ = secs[i][0]
            hw = secs[i][3][1]
            top = secs[i][3][2]
            for s in (-1, 1):
                sub.beam((xx, s * hw * 0.95, depth * 0.55), (xx, s * hw, top), (1, 0, 0), 0.35, 0.3)
    B[color].merge(sub, ang, x, y, z)


def carrack_into(B, L, x=0.0, y=0.0, z=0.0, ang=0.0, rig="full", flag=True, frame=False, frigate=False):
    """A nau (carrack) of the India run: deep hull, tall aftercastle, overhanging forecastle, three or four masts.
    rig: full | bare (masts only) | none."""
    beam = L * 0.3
    depth = L * 0.17
    S = Bufs()
    if frigate:
        beam = L * 0.27
        hull_into(S, L, beam, depth, "#5A4636", sheer=L * 0.015, stern_h=L * 0.035, bow_h=L * 0.015, x=0, y=0, z=0, frame=frame)
        S["#C9A24A"].box(0, beam * 0.49, depth * 0.62, L * 0.8, 0.14, L * 0.02)
        S["#C9A24A"].box(0, -beam * 0.49, depth * 0.62, L * 0.8, 0.14, L * 0.02)
        for j in range(12):
            for sgn in (-1, 1):
                S[DARK].box(-L * 0.36 + j * L * 0.064, sgn * beam * 0.5, depth * 0.66, 0.6, 0.12, 0.6)
        S[shade(HULL, 0.12)].box(-L * 0.38, 0, depth + L * 0.02, L * 0.16, beam * 0.8, L * 0.03)
        S[WOOD_D].beam((L * 0.45, 0, depth + L * 0.03), (L * 0.66, 0, depth + L * 0.1), (0, 1, 0), 0.4, 0.4)
    else:
        hull_into(S, L, beam, depth, HULL, sheer=L * 0.03, stern_h=L * 0.08, bow_h=L * 0.05, x=0, y=0, z=0, frame=frame)
    if not frame and not frigate:
        # aftercastle (two decks) and forecastle (triangular, overhanging the bow)
        S[shade(HULL, 0.12)].box(-L * 0.36, 0, depth + L * 0.04, L * 0.2, beam * 0.78, L * 0.05)
        S[shade(HULL, 0.2)].box(-L * 0.41, 0, depth + L * 0.09, L * 0.1, beam * 0.64, L * 0.04)
        S[shade(HULL, 0.12)].prism([(L * 0.3, -beam * 0.36), (L * 0.53, 0), (L * 0.3, beam * 0.36)], depth + L * 0.03, depth + L * 0.08)
        S[RED].box(-L * 0.36, 0, depth + L * 0.09 - 0.05, L * 0.2 + 0.1, beam * 0.79, 0.25)
        # wales
        for k in (0.45, 0.75):
            S[WOOD_D].box(0, beam * 0.49, depth * k, L * 0.8, 0.15, 0.3)
            S[WOOD_D].box(0, -beam * 0.49, depth * k, L * 0.8, 0.15, 0.3)
        # gunports
        for j in range(6):
            for sgn in (-1, 1):
                S[DARK].box(-L * 0.25 + j * L * 0.09, sgn * beam * 0.5, depth * 0.62, 0.7, 0.12, 0.7)
        # bowsprit
        S[WOOD_D].beam((L * 0.45, 0, depth + L * 0.06), (L * 0.68, 0, depth + L * 0.16), (0, 1, 0), 0.4, 0.4)
    if rig != "none":
        masts = [(L * 0.22, L * 0.62, 0.95), (-L * 0.02, L * 0.85, 1.25), (-L * 0.26, L * 0.5, 0.0)]
        if L > 30:
            masts.append((-L * 0.4, L * 0.38, 0.0))
        for k, (mx, mh, sail) in enumerate(masts):
            S[WOOD_D].lathe([(0.35, 0), (0.22, mh)], mx, 0, depth, 6)
            if rig == "full":
                if sail:
                    sw = beam * sail
                    for j, (zf, hf) in enumerate(((0.3, 0.42), (0.75, 0.2))):
                        ww = sw * (1.0 if j == 0 else 0.6)
                        S[WOOD_D].box(mx + 0.4, 0, depth + mh * (zf + hf) + 0.2, 0.3, ww * 1.1, 0.3)
                        S[SAIL].box(mx + 0.45, 0, depth + mh * zf, 0.2, ww, mh * hf)
                        if j == 0 and flag:
                            christ_cross(S, mx + 0.6, 0, depth + mh * (zf + hf * 0.62), ww * 0.45, "E")
                else:
                    # lateen yard and sail on the mizzen and bonaventure
                    p0 = (mx + L * 0.12, 0, depth + mh * 0.25)
                    p1 = (mx - L * 0.14, 0, depth + mh * 1.0)
                    S[WOOD_D].beam(p0, p1, (0, 1, 0), 0.3, 0.3)
                    b = len(S[SAIL].v)
                    S[SAIL].v += [(p0[0] - 0.3, -0.1, p0[2] + 0.2), (p1[0] - 0.3, -0.1, p1[2] - 0.4), (mx - 0.2, -0.1, depth + mh * 0.18),
                                  (p0[0] - 0.3, 0.1, p0[2] + 0.2), (p1[0] - 0.3, 0.1, p1[2] - 0.4), (mx - 0.2, 0.1, depth + mh * 0.18)]
                    S[SAIL].f += [(b, b + 1, b + 2), (b + 5, b + 4, b + 3), (b, b + 3, b + 4, b + 1), (b + 1, b + 4, b + 5, b + 2), (b + 2, b + 5, b + 3, b)]
            if k == 1:
                S[WOOD_D].lathe([(0.9, 0), (1.1, 1.2), (0, 1.3)], mx, 0, depth + mh * 0.82, 6)    # main top
            if rig == "bare" and sail:
                for zf, ww in ((0.72, beam * sail * 1.05), (0.95, beam * sail * 0.6)):
                    S[WOOD_D].box(mx + 0.4, 0, depth + mh * zf, 0.3, ww, 0.3)
            for sgn in (-1, 1):
                for j in range(3):
                    xo = mx - L * 0.035 + j * L * 0.035
                    S["#4A3A2A"].beam((xo, sgn * beam * 0.48, depth + 0.3), (mx, sgn * 0.3, depth + mh * 0.8), (1, 0, 0), 0.08, 0.08)
        if flag:
            S[LIME].box(-L * 0.42, 0, depth + L * 0.13, 0.1, 0.1, L * 0.12)
            S[RED].box(-L * 0.42, 0.9, depth + L * 0.13 + L * 0.085, 0.08, 1.8, 1.2)
    B.merge(S, ang, x, y, z)


def caravel_into(B, L, x=0.0, y=0.0, z=0.0, ang=0.0, rig="lateen", frame=False):
    """A caravel: a slim, low hull with a small aftercastle and two or three lateen-rigged masts."""
    beam = L * 0.27
    depth = L * 0.14
    S = Bufs()
    hull_into(S, L, beam, depth, shade(HULL, 0.08), sheer=L * 0.025, stern_h=L * 0.05, bow_h=L * 0.02, stations=10, frame=frame)
    if not frame:
        S[shade(HULL, 0.2)].box(-L * 0.38, 0, depth + L * 0.03, L * 0.18, beam * 0.75, L * 0.04)
    if rig != "none":
        for mx, mh in ((L * 0.18, L * 0.75), (-L * 0.08, L * 0.62), (-L * 0.3, L * 0.45)):
            S[WOOD_D].lathe([(0.25, 0), (0.15, mh)], mx, 0, depth, 6)
            if rig == "lateen":
                p0 = (mx + L * 0.2, 0, depth + mh * 0.2)
                p1 = (mx - L * 0.22, 0, depth + mh * 1.05)
                S[WOOD_D].beam(p0, p1, (0, 1, 0), 0.22, 0.22)
                b = len(S[SAIL].v)
                S[SAIL].v += [(p0[0] - 0.2, -0.08, p0[2] + 0.2), (p1[0] - 0.2, -0.08, p1[2] - 0.3), (mx - L * 0.02, -0.08, depth + 1.0),
                              (p0[0] - 0.2, 0.08, p0[2] + 0.2), (p1[0] - 0.2, 0.08, p1[2] - 0.3), (mx - L * 0.02, 0.08, depth + 1.0)]
                S[SAIL].f += [(b, b + 1, b + 2), (b + 5, b + 4, b + 3), (b, b + 3, b + 4, b + 1), (b + 1, b + 4, b + 5, b + 2), (b + 2, b + 5, b + 3, b)]
                christ_cross(S, mx - L * 0.03, -0.12, depth + mh * 0.62, L * 0.12, "S")
    B.merge(S, ang, x, y, z)



# ================================================================ the castle hill
CASTLE_RING = [(-108, -52), (-70, -66), (-20, -71), (35, -70), (82, -58), (108, -32), (112, 18), (92, 58), (40, 70), (-15, 72), (-70, 64), (-104, 38), (-112, -10), (-108, -52)]
KEEP = (-14, 64, -32, 36)            # castelejo: x0, x1, y0, y1 offset into the east part (x from 36 to 100)


def _hilltop(B, color=GROUND):
    """The hilltop as a low battered platform with a scarp, rock outcrops on the edge."""
    B[shade(color, -0.12)].frustum(0, 0, 0, 228, 148, 216, 138, 1.6)
    B[color].prism([(x * 0.93, y * 0.93) for x, y in CASTLE_RING[:-1]], 1.6, 2.6)
    for x, y, r in ((-112, -40, 5), (-60, -70, 4), (100, -50, 6), (110, 40, 5), (-90, 60, 4), (30, 72, 4)):
        B[shade(color, -0.2)].lathe([(r, 0), (r * 0.7, 2.2), (0, 3.0)], x, y, 0, 6)


def _castelejo(B, color, top="merlons", z=2.6):
    """The inner castle at the east end: curtain walls with square towers, the keep, a court."""
    x0, x1, y0, y1 = 36.0, 100.0, -34.0, 38.0
    wall_line(B, [(x0, y0), (x1, y0), (x1, y1), (x0, y1), (x0, y0)], 12.0, 3.0, color, z, True, top == "capped", 1.0)
    B[shade(color, 0.08)].box2(x0 + 1.5, y0 + 1.5, x1 - 1.5, y1 - 1.5, z, z + 0.4)
    towers = [(x0, y0), (x1, y0), (x1, y1), (x0, y1), ((x0 + x1) / 2, y0), ((x0 + x1) / 2, y1), (x0, 2), (x1, 2), (x1, (y1 + 2) / 2 + 2), (x0 + 16, y0)]
    for i, (tx, ty) in enumerate(towers):
        sq_tower(B, tx, ty, 7.0, 16.0, shade(color, -0.04), top, z=z)
    # keep (Torre de Menagem) and the Torre de Ulisses
    sq_tower(B, x1 - 8, y1 - 9, 11.0, 23.0, shade(color, -0.07), top, z=z)
    sq_tower(B, x0 + 9, y1 - 6, 9.0, 20.0, shade(color, -0.05), top, z=z)
    opening(B, "W", 10.0, x0 - 1.5, z, 3.2, 6.5, "round")
    for tx, ty in ((x1 - 8, y1 - 9), (x0 + 9, y1 - 6)):
        for zz in (8, 14):
            opening(B, "S", tx, ty - 4.6, z + zz, 0.9, 1.8, "round")


def _palace_1550(B, z=2.6, roofs=True):
    """The Paço da Alcáçova: ranges round a court, a chapel, a loggia on the south over the river."""
    walls = "#E6DAC0"
    rngs = [(-92, -50, -20, -34, 12), (-92, -34, -78, 30, 10), (-78, 16, -20, 30, 10), (-20, -50, -6, 30, 12)]
    for x0, y0, x1, y1, h in rngs:
        B[walls].box2(x0, y0, x1, y1, z, z + h)
        if roofs:
            B[TILE].hip((x0 + x1) / 2, (y0 + y1) / 2, x1 - x0, y1 - y0, z + h, min(x1 - x0, y1 - y0) * 0.34, 0.4)
        else:
            B[shade(walls, -0.25)].box2(x0 + 0.8, y0 + 0.8, x1 - 0.8, y1 - 0.8, z + h - 0.1, z + h + 0.05)
    win_rows(B, -92, -50, -20, -34, [z + 2.0, z + 7.0], 2.4, 5.0, 1.5, "S", "round")
    openings(B, "S", -88, -24, -50, z + 0.2, 4.0, 4.4, 9, "round")
    win_rows(B, -20, -50, -6, 30, [z + 6.0], 2.2, 5.5, 1.3, "E", "round")
    # chapel of São Miguel with a small bell-cote, and a tower at the south-west corner
    B[LIME].box2(-60, 34, -36, 46, z, z + 11)
    if roofs:
        B[TILE].gable_x(40, -60, -36, 12, z + 11, 3.8)
    B[LIME].box(-36, 40, z, 1.0, 4.0, 15.0)
    sq_tower(B, -96, -52, 10.0, 20.0, "#DCCDAE", "pyramid" if roofs else "merlons", TILE, z)
    for x, y in ((-60, -6), (-40, 0), (-70, 10), (-48, 12)):
        tree_into(B, x, y, z, 2.6, "round", "#4F7A45")
    B[GRASS].box2(-76, -32, -22, 14, z, z + 0.15)


def court_houses(B, x0, y0, x1, y1, z, seed=0, cell=12.0, lane=2.2, h=(4.6, 6.4), colors=HOUSES[:5]):
    """A packed quarter of flat-roofed courtyard houses: four ranges round a small open patio, lanes between."""
    k = seed
    y = y0
    while y + cell <= y1 + 0.01:
        x = x0
        while x + cell <= x1 + 0.01:
            c = colors[k % len(colors)]
            hh = h[0] + (k * 37 % 7) / 6.0 * (h[1] - h[0])
            w = cell - (k * 13 % 3) * 0.8
            d = cell - (k * 7 % 3) * 0.8
            pw, pd = w * 0.36, d * 0.36
            cx, cy = x + w / 2, y + d / 2
            B[c].box2(x, y, x + w, cy - pd / 2, z, z + hh)
            B[c].box2(x, cy + pd / 2, x + w, y + d, z, z + hh)
            B[c].box2(x, cy - pd / 2, cx - pw / 2, cy + pd / 2, z, z + hh)
            B[c].box2(cx + pw / 2, cy - pd / 2, x + w, cy + pd / 2, z, z + hh)
            B[shade(c, -0.1)].box2(x - 0.15, y - 0.15, x + w + 0.15, y + d + 0.15, z + hh, z + hh + 0.35)
            B[shade(c, -0.3)].box2(cx - pw / 2, cy - pd / 2, cx + pw / 2, cy + pd / 2, z, z + 0.2)
            opening(B, "S", cx - w * 0.25, y, z, 0.9, 2.0, "flat")
            if k % 4 == 0:
                B[TILE].lean(x, cy + pd / 2, x + w, y + d, z + hh, z + hh + 1.4, "S")
            x += w + lane
            k += 1
        y += cell + lane


def _houses_patch(B, rects, seed=0, roof="tile", h=(5.0, 8.0), z=2.6, colors=HOUSES):
    k = seed
    for x0, y0, x1, y1 in rects:
        x = x0
        while x < x1 - 4:
            w = 5.0 + (k * 37 % 5)
            y = y0
            while y < y1 - 4:
                d = 6.0 + (k * 53 % 4)
                hh = h[0] + (k * 29 % 7) / 6.0 * (h[1] - h[0])
                house(B, x + w / 2, y + d / 2, w - 0.6, d - 0.6, hh, colors[k % len(colors)], roof, z, "S", False)
                y += d + 1.2
                k += 1
            x += w + 1.4


def castelo(variant="1550"):
    m = Model("castelo-" + variant)
    B0, B1, B2 = Bufs(), Bufs(), Bufs()
    _hilltop(B0, "#C4AE86" if variant != "roman" else "#B9A47C")
    col = {"moorish": EARTH, "roman": STONE}.get(variant, CASTLE)
    if variant == "roman":
        # the old hill-fort's dry-stone enclosure, terraces of houses, a small temple on the summit
        ring = [(x * 0.82, y * 0.82) for x, y in CASTLE_RING]
        wall_line(B1, ring, 3.5, 2.2, STONE_D, 2.6, False)
        for k, r in enumerate((0.6, 0.38)):
            B1[shade(GROUND, -0.06 * k)].prism([(x * r, y * r) for x, y in CASTLE_RING[:-1]], 2.6, 3.4 + 0.8 * k)
        _houses_patch(B1, [(-80, -48, -20, -10), (-80, 10, -30, 44), (30, -46, 76, -12), (40, 14, 80, 46)], 3, "tile", (3.5, 5.0), 2.6)
        tb = Bufs()
        tb[LIOZ].box(0, 0, 0, 12.0, 20.0, 1.8)
        for cx in (-4.2, -1.4, 1.4, 4.2):
            tb[LIOZ].lathe([(0.5, 0), (0.42, 6.0)], cx, -8.5, 1.8, 8)
        tb[LIOZ].box(0, 2.0, 1.8, 10.0, 13.0, 6.0)
        tb[LIOZ].box(0, 0, 7.8, 11.0, 19.0, 0.9)
        tb[TILE].gable_y(0, -9.6, 9.6, 11.0, 8.7, 2.6, 0.3)
        tb[LIOZ].box(0, -12.5, 0, 9.0, 5.0, 0.9)
        B2.merge(tb, 0, 0, 0, 3.4 + 0.8)
        for x, y in ((-30, 30), (60, 40), (-60, -30), (20, -50)):
            tree_into(B2, x, y, 2.6, 3.0, "round", "#6E8A55")
    else:
        top = "capped" if variant == "moorish" else "merlons"
        # the alcáçova curtain, square towers every ~30 m
        wall_line(B1, CASTLE_RING, 9.0, 2.6, col, 0.0, True, variant == "moorish", 0.9)
        for (ax, ay), (bx, by) in zip(CASTLE_RING, CASTLE_RING[1:]):
            L = math.hypot(bx - ax, by - ay)
            n = max(1, round(L / 32))
            for j in range(n):
                tx, ty = ax + (bx - ax) * j / n, ay + (by - ay) * j / n
                sq_tower(B1, tx, ty, 6.0, 12.5, shade(col, -0.05), top)
                for f in "SNEW":
                    al = tx if f in "SN" else ty
                    nrm = {"S": ty - 3.0, "N": ty + 3.0, "E": tx + 3.0, "W": tx - 3.0}[f]
                    opening(B1, f, al, nrm, 7.0, 0.35, 1.6, "flat", DARK, 0.2)
        # the gate (Porta de São Jorge) on the west side, the barbican
        opening(B1, "W", -20.0, -110.5, 0.0, 3.6, 6.5, "pointed" if variant == "moorish" else "round")
        _castelejo(B2, col, top)
        if variant == "moorish":
            # the quarter of courtyard houses (Praça Nova) and the citadel mosque with its minaret
            court_houses(B1, -96, -50, -24, 22, 2.6, seed=1)
            court_houses(B1, -60, 24, -20, 46, 2.6, seed=7)
            court_houses(B1, -16, -62, 30, -14, 2.6, seed=3)
            court_houses(B1, -14, 12, 28, 60, 2.6, seed=5)
            mq = Bufs()
            mq[LIME].box2(-6, 20, 22, 44, 2.6, 9.0)
            for k in range(4):
                mq[TILE].gable_y(-2.5 + k * 7, 20, 44, 7.0, 9.0, 2.2, 0.1)
            mq[LIME].box(-3, 50, 2.6, 5.0, 5.0, 17.0)
            mq[shade(LIME, -0.1)].box(-3, 50, 19.6, 5.6, 5.6, 0.5)
            mq[LIME].box(-3, 50, 20.1, 3.4, 3.4, 3.0)
            mq[TILE_D].lathe([(2.3, 0), (0, 1.8)], -3, 50, 23.1, 4, math.pi / 4)
            opening(mq, "S", 8.0, 20.0, 2.6, 2.6, 4.2, "pointed")
            B2.merge(mq, 0, -70, 0, 0)
            for x, y in ((-10, -30), (-14, 6)):
                tree_into(B2, x, y, 2.6, 2.4, "round", "#4F7A45")
        else:
            _palace_1550(B2, 2.6, roofs=(variant != "1800"))
            _houses_patch(B1, [(-2, -60, 30, -40), (-4, 44, 30, 66), (-80, 38, -63, 50), (-2, -34, 28, -8)], 2, "tile", (6.0, 9.0), 2.6)
            # the parish church of Santa Cruz do Castelo among the houses
            B2[LIME].box2(2, 6, 26, 16, 2.6, 12.0)
            B2[TILE].gable_x(11, 2, 26, 10, 12.0, 3.2)
            B2[LIME].box(0, 13, 2.6, 4.0, 4.0, 17.0)
            B2[TILE].lathe([(3.0, 0), (0, 2.6)], 0, 13, 19.6, 4, math.pi / 4)
            layered_portal(B2, "S", 14, 6, 2.6, 2.6, 4.2, 2, LIOZ, "round")
            for f in "SW":
                opening(B2, f, 0 if f == "S" else 13, 11.0 if f == "S" else -2.0, 14.0, 1.2, 2.0, "round")
            if variant == "1800":
                # barracks sheds against the north wall
                B2[STONE].box2(-90, 44, -64, 58, 2.6, 8.6)
                B2[TILE].gable_x(51, -90, -64, 14, 8.6, 3.0)
            for x, y in ((-100, -20), (20, -55), (24, 55), (-8, -60), (10, 60)):
                tree_into(B2, x, y, 2.6, 3.4, "pine")
    m.add(0, B0.join("cs_ground"), "hill")
    m.add(1, B1.join("cs_walls"), "walls")
    m.add(2, B2.join("cs_keep"), "castle")
    return m



def disc_uv(r, n=16):
    return [(r * math.cos(math.tau * k / n), r + r * math.sin(math.tau * k / n)) for k in range(n)]


def rose(B, face, along, normal, z, r, frame=LIOZ):
    """A rose window: a stone ring and a dark glazed disc with a cross of tracery."""
    off = {"S": -1, "N": 1, "E": 1, "W": -1}[face]
    B[frame].slab(disc_uv(r * 1.18), face, along, normal + off * 0.12, z - r * 0.18, 0.3)
    B[GLASS].slab(disc_uv(r), face, along, normal + off * 0.3, z, 0.15)
    B[frame].slab([(-r, r - 0.12), (r, r - 0.12), (r, r + 0.12), (-r, r + 0.12)], face, along, normal + off * 0.4, z, 0.1)
    B[frame].slab([(-0.12, 0), (0.12, 0), (0.12, 2 * r), (-0.12, 2 * r)], face, along, normal + off * 0.4, z, 0.1)


def layered_portal(B, face, along, normal, z, w, h, n=4, color=LIOZ, kind="round"):
    """A deep Romanesque or Gothic portal: n receding archivolts, each a step narrower, a dark door at the back."""
    s = {"S": -1, "N": 1, "E": 1, "W": -1}[face]
    for k in range(n):
        ww, hh = w * (1 - 0.13 * k), h * (1 - 0.09 * k)
        B[shade(color, -0.04 * k)].slab(arch_uv(ww, hh, kind), face, along, normal + s * (0.6 - 0.25 * k), z, 0.3)
    B[DARK].slab(arch_uv(w * (1 - 0.13 * n), h * (1 - 0.09 * n), kind), face, along, normal + s * (0.62 - 0.25 * n), z, 0.3)


def gothic_buttresses(B, x0, x1, y, h, n, color, side=-1, depth=1.6, w=1.1):
    for k in range(n + 1):
        x = x0 + (x1 - x0) * k / n
        B[color].frustum(x, y + side * depth / 2, 0, w, depth, w, depth * 0.4, h)


# ================================================================ the Sé
def se(variant="1550"):
    m = Model("se-" + variant)
    B0, B1, B2 = Bufs(), Bufs(), Bufs()
    B0[PAVE].box(0, 0, 0, 40, 90, 0.3)
    col = "#D9CDB2"
    z = 0.3
    # nave and aisles
    B1[col].box2(-7, -40, 7, 12, z, 21)
    B1[TILE].gable_y(0, -40.5, 12, 14, 21, 4.8, 0.4)
    for sgn in (-1, 1):
        x0, x1 = sorted((sgn * 7, sgn * 13))
        B1[col].box2(x0, -34, x1, 12, z, 13)
        B1[TILE].lean(x0, -34, x1, 12, 12.8, 15.5, "E" if sgn < 0 else "W")
        for k in range(6):
            y = -30 + k * 7.5
            B1[shade(col, -0.06)].box(sgn * 13.8, y, z, 1.6, 1.4, 11.5)
            opening(B1, "E" if sgn > 0 else "W", y + 3.7, sgn * 13, 7.0, 0.9, 2.4, "round")
            opening(B1, "E" if sgn > 0 else "W", y + 3.7, sgn * 7, 15.5, 0.9, 2.8, "round")
    # transept
    B1[col].box2(-19, 12, 19, 22, z, 19)
    B1[TILE].gable_x(17, -19.4, 19.4, 10, 19, 4.0, 0.4)
    for sgn in (-1, 1):
        rose(B1, "E" if sgn > 0 else "W", 17, sgn * 19, 11.0, 1.6, LIOZ)
    if variant == "1550":
        # the Gothic chancel and ambulatory with radiating chapels
        B1[col].box2(-7, 22, 7, 32, z, 21)
        B1[TILE].gable_y(0, 22, 32, 14, 21, 4.8, 0.4)
        apse = [(7 * math.cos(a), 32 + 7 * math.sin(a)) for a in [i * math.pi / 6 for i in range(7)]]
        B1[col].prism(apse, z, 21)
        B1[TILE].lathe([(7.4, 0), (0, 4.2)], 0, 32, 21, 12, 0)
        amb = [(13 * math.cos(a), 30 + 13 * math.sin(a)) for a in [i * math.pi / 8 for i in range(9)]]
        B1[col].prism(amb, z, 12)
        B1[TILE].lathe([(13.3, 0), (8.0, 2.5)], 0, 30, 12, 16, 0)
        for k in range(5):
            a = math.pi * (k + 0.5) / 5
            cx, cy = 13.2 * math.cos(a), 30 + 13.2 * math.sin(a)
            B1[col].lathe([(3.2, 0), (3.2, 9.5)], cx, cy, z, 6)
            B1[TILE].lathe([(3.5, 0), (0, 2.4)], cx, cy, 9.5 + z, 6)
            ux, uy = math.cos(a), math.sin(a)
            B1[shade(col, -0.08)].beam((cx + ux * 3.4, cy + uy * 3.4, z), (cx + ux * 3.4, cy + uy * 3.4, 8.5), (-uy, ux, 0), 0.8, 1.0)
        # the lantern over the crossing
        sq_tower(B2, 0, 17, 11.0, 29.0, col, "merlons")
        for f, (dx, dy) in (("S", (0, -5.5)), ("N", (0, 5.5)), ("E", (5.5, 0)), ("W", (-5.5, 0))):
            opening(B2, f, (dx if f in "SN" else 17 + dy), (17 + dy if f in "SN" else dx), 22.0, 1.4, 4.0, "pointed")
    else:
        # the Baroque east end built after 1755
        B1[LIME].box2(-9, 22, 9, 42, z, 22)
        B1[TILE].hip(0, 32, 18, 20, 22, 4.2, 0.5)
        win_rows(B1, -9, 22, 9, 42, [12.0], 3.4, 6.0, 1.6, "EW", "round")
        B1[col].box(0, 17, 19, 10.0, 10.0, 3.0)
        B1[TILE].hip(0, 17, 10, 10, 22, 2.6, 0.3)
    # the west front: two towers, a crenellated screen, the portal and the rose
    for sgn in (-1, 1):
        x = sgn * 14.5
        B2[col].box(x, -39, z, 11, 10, 29.5)
        for zz in (8.0, 16.0):
            opening(B2, "S", x, -44, zz, 1.0, 2.6, "round")
        for u in (-2.0, 2.0):
            opening(B2, "S", x + u, -44, 23.0, 1.6, 4.0, "round")
            opening(B2, "E" if sgn > 0 else "W", -39 + u, x + sgn * 5.5, 23.0, 1.6, 4.0, "round")
        B2[shade(col, -0.08)].box(x, -39, 29.2, 11.6, 10.6, 0.6)
        if variant == "1550":
            box_merlons(B2[col], x - 5.5, -44, x + 5.5, -34, 29.8, 1.1, 0.9, "SNEW", 0.7)
        else:
            B2[col].box(x, -39, 29.8, 8.0, 8.0, 4.0)
            for f in "SNEW":
                opening(B2, f, x if f in "SN" else -39, (-43 if f == "S" else -35) if f in "SN" else (x + (4 if f == "E" else -4)), 30.3, 2.0, 3.0, "round")
            B2[TILE].lathe([(6.0, 0), (0, 3.5)], x, -39, 33.8, 4, math.pi / 4)
    B2[col].box2(-9, -44, 9, -40, z, 24)
    box_merlons(B2[col], -9, -44, 9, -40, 24, 1.1, 0.9, "S", 0.7)
    layered_portal(B2, "S", 0, -44, z, 8.0, 10.5, 4, LIOZ, "round")
    rose(B2, "S", 0, -44, 14.5, 3.0, LIOZ)
    m.add(0, B0.join("se_g"), "ground")
    m.add(1, B1.join("se_nave"), "nave")
    m.add(2, B2.join("se_front"), "towers")
    return m


def se_mosque():
    """The main mosque of al-Ushbuna as it is usually imagined: a hall of parallel aisles, a court with galleries, a square minaret."""
    m = Model("se-mosque")
    B0, B1, B2 = Bufs(), Bufs(), Bufs()
    B0[PAVE].box(0, 0, 0, 40, 90, 0.3)
    z = 0.3
    # prayer hall: 5 aisles under parallel gable roofs, the qibla wall at the north (+Y) end
    B1[LIME].box2(-18, 0, 18, 42, z, 8.5)
    for k in range(5):
        B1[TILE].gable_y(-14.4 + k * 7.2, 0, 42, 7.2, 8.5, 2.2, 0.05)
    B1[LIME].box(0, 43.2, z, 5.0, 2.4, 7.0)
    B1[TILE_D].lathe([(2.6, 0), (0, 1.8)], 0, 43.2, 7.3, 8)
    openings(B1, "S", -16, 16, 0, z, 4.6, 6.2, 5, "pointed")
    # court with galleries on three sides, a fountain and orange trees
    B1[SAND].box2(-18, -40, 18, 0, z, z + 0.15)
    for sgn in (-1, 1):
        x0, x1 = sorted((sgn * 18, sgn * 12.5))
        B1[LIME].box2(x0, -40, x1, -1, z, 6.0)
        B1[TILE].lean(x0, -40, x1, -1, 6.0, 7.4, "E" if sgn > 0 else "W")
        B1[LIME].box2(sgn * 18 - 0.3, -40, sgn * 18 + 0.3, -1, 6.0, 7.6)
        openings(B1, "E" if sgn < 0 else "W", -40, -1, sgn * 12.5, z, 3.0, 4.2, 9, "pointed")
    B1[LIME].box2(-18, -44, 18, -40, z, 6.5)
    capped_merlons(B1[LIME], -18, -44, 18, -40, 6.5, 0.7, 0.6, "S", 0.5)
    capped_merlons(B1[LIME], -18.3, -40, -17.7, -1, 7.6, 0.7, 0.6, "W", 0.5)
    capped_merlons(B1[LIME], 17.7, -40, 18.3, -1, 7.6, 0.7, 0.6, "E", 0.5)
    opening(B1, "S", 0, -44, z, 3.4, 5.0, "pointed")
    B1[WATER].lathe([(2.2, 0), (2.2, 0.6)], 0, -20, z, 8)
    for x, y in ((-7, -30), (7, -30), (-7, -10), (7, -10)):
        tree_into(B1, x, y, z, 2.0, "round", "#3F6B3A")
    # minaret in the south-west corner of the court
    B2[LIME].box(-14, -40, z, 5.5, 5.5, 18.0)
    for zz in (6.0, 11.0):
        opening(B2, "S", -14, -42.75, zz, 0.8, 1.8, "pointed")
    B2[shade(LIME, -0.08)].box(-14, -40, 18.3, 6.3, 6.3, 0.6)
    capped_merlons(B2[LIME], -17.1, -43.1, -10.9, -36.9, 18.9, 0.7, 0.6, "SNEW", 0.5)
    B2[LIME].box(-14, -40, 18.9, 3.2, 3.2, 3.6)
    B2[TILE_D].lathe([(2.2, 0), (0, 1.8)], -14, -40, 22.5, 4, math.pi / 4)
    B2[GOLD].lathe([(0, 0), (0.3, 0.3), (0, 0.6)], -14, -40, 24.3, 6)
    m.add(0, B0.join("sm_g"), "ground")
    m.add(1, B1.join("sm_hall"), "hall")
    m.add(2, B2.join("sm_min"), "minaret")
    return m


# ================================================================ Olisipo
def roman_theatre():
    m = Model("roman-theatre")
    B0, B1, B2 = Bufs(), Bufs(), Bufs()
    yc = -10.0
    B0[GROUND].box(0, 0, 0, 70, 50, 0.3)
    # the hillside the cavea is dug into
    B0[shade(GROUND, -0.1)].prism([(-35, yc), (35, yc), (35, 25), (-35, 25)], 0.3, 1.2)
    tiers = [(7.5, 16.0, 4.5), (16.0, 25.0, 9.5), (25.0, 32.5, 14.0)]
    z0 = 0.3
    objs = []
    for i, (r0, r1, h) in enumerate(tiers):
        nrow = int((r1 - r0) / 1.6)
        for j in range(nrow):
            ra = r0 + (r1 - r0) * j / nrow
            hh = z0 + (h - z0) * (j + 1) / nrow
            objs.append(ellipse_ring(f"th_c{i}_{j}", r1, r1, ra / r1, hh, (0, yc, 0.3), LIOZ if j % 2 else "#DDD3BC", n=32, arc=math.pi, start=0.0))
        z0 = h + 0.5
    m.add(0, join(objs, "th_cavea"), "cavea")
    for k in range(1, 6):
        a = math.pi * k / 6
        for (r0, r1, h), zs in zip(tiers, (0.3, 5.0, 10.0)):
            p0 = (r0 * math.cos(a), yc + r0 * math.sin(a), zs + 0.6)
            p1 = (r1 * math.cos(a), yc + r1 * math.sin(a), h + 0.35)
            B1[STONE_D].beam(p0, p1, (-math.sin(a), math.cos(a), 0), 0.9, 0.1)
    # outer wall on top of the cavea
    for k in range(16):
        a0, a1 = math.pi * k / 16, math.pi * (k + 1) / 16
        p0 = (32.8 * math.cos(a0), yc + 32.8 * math.sin(a0), 14.3)
        p1 = (32.8 * math.cos(a1), yc + 32.8 * math.sin(a1), 14.3)
        B1[STONE].beam(p0, p1, (0, 0, 1), 2.4, 0.8)
    # orchestra, stage (pulpitum) and the scaenae frons
    B1["#E8E1D2"].lathe([(7.5, 0), (7.5, 0.25)], 0, yc, 0.3, 24)
    B1[LIOZ].box(0, yc - 2.8, 0.3, 46.0, 5.6, 1.5)
    for k in range(-5, 6):
        B1[STONE_D].box(k * 4.0, yc - 0.05, 0.3, 1.2, 0.3, 1.4)
    B1[STONE].box(0, yc - 9.0, 0.3, 50.0, 4.0, 13.5)
    for sgn in (-1, 1):
        B1[STONE].box(sgn * 29.0, yc - 6.5, 0.3, 8.0, 9.0, 11.5)
        B1[TILE].hip(sgn * 29.0, yc - 6.5, 8.0, 9.0, 11.8, 2.2, 0.3)
    for lvl, z in enumerate((1.8, 7.6)):
        for k in range(-6, 7):
            B2["#EEE8DC"].lathe([(0.32, 0), (0.27, 5.4)], k * 3.6, yc - 6.6, z, 8)
        B2[LIOZ].box(0, yc - 6.7, z + 5.4, 46.0, 1.0, 0.6)
    for k in (-1, 0, 1):
        opening(B2, "N", k * 12.0, yc - 7.0, 1.8, 3.6 if k == 0 else 2.6, 5.5 if k == 0 else 4.4, "round")
    B2[TILE].gable_x(yc - 9.0, -25.0, 25.0, 4.0, 13.8, 1.6)
    openings(B1, "S", -24, 24, yc - 11.0, 0.3, 2.6, 5.0, 8, "round")
    openings(B1, "S", -24, 24, yc - 11.0, 7.0, 1.6, 3.2, 8, "round")
    m.add(1, B1.join("th_stage"), "stage")
    m.add(2, B2.join("th_frons"), "scaenae frons")
    m.add(0, B0.join("th_g"), "cavea")
    return m


# ================================================================ gates
def _gate(name, L, wall_h, tower_w, tower_h, gap, color, top="merlons", kind="round", houses_side=None, roofs=False):
    B1, B2 = Bufs(), Bufs()
    B1[GROUND].box(0, 0, 0, L, 16, 0.25)
    wall_line(B1, [(-L / 2, 0), (-gap / 2 - tower_w / 2, 0)], wall_h, 3.0, color, 0.25, True, top == "capped", 0.9)
    wall_line(B1, [(gap / 2 + tower_w / 2, 0), (L / 2, 0)], wall_h, 3.0, color, 0.25, True, top == "capped", 0.9)
    B1[color].box(0, 0, 0.25, gap + 0.4, 4.0, wall_h + 2.0)
    box_merlons(B1[color], -gap / 2, -2, gap / 2, 2, wall_h + 2.25, 0.9, 0.8, "SN", 0.6)
    opening(B1, "S", 0, -2.0, 0.25, gap * 0.62, wall_h * 0.68, kind)
    opening(B1, "N", 0, 2.0, 0.25, gap * 0.62, wall_h * 0.68, kind)
    for sgn in (-1, 1):
        x = sgn * (gap / 2 + tower_w / 2)
        sq_tower(B2, x, -0.8, tower_w, tower_h, shade(color, -0.04), top if not roofs else "pyramid", TILE, 0.25, tower_w + 1.2)
        for zz in (tower_h * 0.45, tower_h * 0.75):
            opening(B2, "S", x, -0.8 - (tower_w + 1.2) / 2, zz, 0.6, 1.4, "round")
    if houses_side:
        k = 0
        x = -L / 2 + 1
        while x < L / 2 - 5:
            if abs(x) < gap / 2 + tower_w + 3:
                x += 4
                continue
            w = 5 + k % 3
            house(B2, x + w / 2, 5.0, w - 0.5, 6.0, 6.5 + (k % 3), HOUSES[k % 6], "tile", 0.25, "N", False)
            x += w + 0.4
            k += 1
    return B1, B2


def porta_do_sol():
    m = Model("porta-do-sol")
    B1, B2 = _gate("pds", 50, 8.5, 7.0, 13.0, 4.5, CASTLE, "capped", "pointed", houses_side=True)
    m.add(1, B1.join("pds_wall"), "wall")
    m.add(2, B2.join("pds_towers"), "towers")
    return m


def porta_santo_antao():
    m = Model("porta-santo-antao")
    B1, B2 = _gate("psa", 36, 9.5, 6.5, 15.0, 5.0, STONE, "merlons", "round", houses_side=True)
    christ_cross(B2, 0, -2.2, 10.0, 1.2, "S")
    m.add(1, B1.join("psa_wall"), "wall")
    m.add(2, B2.join("psa_towers"), "towers")
    return m



# ================================================================ the Ribeira
def range_block(B, x0, y0, x1, y1, z, h, color, roof="hip", storeys=3, win_faces="SNEW", spacing=4.0, kind="round", arcade_face=None, arcade_kind="round", roof_color=TILE):
    """A palace or warehouse range: walls, a cornice, rows of windows, an optional ground-floor arcade, a hipped roof."""
    B[color].box2(x0, y0, x1, y1, z, z + h)
    B[shade(color, -0.1)].box2(x0 - 0.3, y0 - 0.3, x1 + 0.3, y1 + 0.3, z + h - 0.6, z + h)
    if roof == "hip":
        B[roof_color].hip((x0 + x1) / 2, (y0 + y1) / 2, x1 - x0, y1 - y0, z + h, min(x1 - x0, y1 - y0) * 0.32, 0.5)
    elif roof == "flat":
        B[shade(color, -0.2)].box2(x0 + 0.5, y0 + 0.5, x1 - 0.5, y1 - 0.5, z + h - 0.05, z + h + 0.05)
    fl = h / storeys
    zs = [z + fl * k + fl * 0.3 for k in range(1 if arcade_face else 0, storeys)]
    faces = "".join(f for f in win_faces if f != arcade_face)
    if zs:
        win_rows(B, x0, y0, x1, y1, zs, fl * 0.45, spacing, min(1.4, spacing * 0.35), win_faces, kind, frame=LIOZ)
    if arcade_face:
        f = arcade_face
        L = (x1 - x0) if f in "SN" else (y1 - y0)
        n = max(1, int(L / 4.5))
        a0, a1 = (x0, x1) if f in "SN" else (y0, y1)
        nrm = {"S": y0, "N": y1, "E": x1, "W": x0}[f]
        openings(B, f, a0, a1, nrm, z, L / n * 0.68, fl * 0.85, n, arcade_kind)


def _chimneys(B, x0, y0, x1, y1, z, n, color, seed=0):
    for k in range(n):
        t = (k + 0.5) / n
        x = x0 + (x1 - x0) * t
        y = y0 + (y1 - y0) * (0.3 + 0.4 * ((k + seed) % 2))
        B[color].box(x, y, z, 1.0, 1.0, 2.6)
        B[shade(color, -0.15)].box(x, y, z + 2.6, 1.4, 1.4, 0.4)


def _loggia(B, x0, x1, y, z, h, n, col=LIOZ, face="S"):
    """An open gallery: a dark recess behind a row of columns carrying arches."""
    s = -1 if face == "S" else 1
    B["#3A3128"].box2(x0, y - s * 0.2, x1, y - s * 2.6, z, z + h)
    for k in range(n + 1):
        x = x0 + (x1 - x0) * k / n
        B[col].lathe([(0.45, 0), (0.38, h * 0.72), (0.6, h * 0.76)], x, y + s * 0.4, z, 8)
    for k in range(n):
        xc = x0 + (x1 - x0) * (k + 0.5) / n
        bw = (x1 - x0) / n
        B[col].slab([(-bw / 2, h * 0.72), (bw / 2, h * 0.72), (bw / 2, h), (-bw / 2, h)], face, xc, y + s * 0.4, z, 0.8)
        B["#3A3128"].slab(arch_uv(bw * 0.78, h * 0.16, "round"), face, xc, y + s * 0.85, z + h * 0.72, 0.1)
    B[col].box2(x0 - 0.5, y + s * 0.0, x1 + 0.5, y + s * 0.9, z + h, z + h + 0.6)


def paco_ribeira(variant="1550"):
    m = Model("paco-ribeira-" + variant)
    B0, B1, B2 = Bufs(), Bufs(), Bufs()
    B0[PAVE].box(0, 0, 0, 110, 150, 0.3)
    B0[LIOZ_D].box2(-55, -75, 55, -71, 0, 0.9)                      # the river quay
    for x in (-40, 10):
        for k in range(5):
            B0[LIOZ_D].box2(x, -75 + k * 0.6, x + 8, -74.4 + k * 0.6, 0, 0.9 - k * 0.18)
    z = 0.3
    W = "#EDE3CC" if variant == "1550" else "#E9DCC0"
    hE = 17.0 if variant == "1550" else 20.0
    # east range on the Terreiro, with an arcaded loggia on the ground floor
    range_block(B1, 32, -56, 52, 60, z, hE, W, "hip", 3, "ENW", 3.0, "round", arcade_face="E")
    for k in range(9):
        B1[LIOZ].box(52.2, -54 + k * 14, z, 0.5, 1.0, hE - 0.6)
    _chimneys(B1, 36, -50, 48, 56, z + hE + 2.0, 7, W, 0)
    # river wing with an open gallery (varanda) on the upper floor
    range_block(B1, -52, -71, 32, -56, z, 14.0, W, "hip", 2, "N", 3.0, "round")
    openings(B1, "S", -50, 30, -71, z + 0.4, 2.2, 4.0, 20, "round")
    _loggia(B1, -50, 30, -71, z + 7.0, 6.0, 16, LIOZ, "S")
    _chimneys(B1, -48, -66, 28, -61, z + 14.0 + 1.8, 6, W, 1)
    # west and north ranges round the garden court
    range_block(B1, -52, -56, -38, 40 if variant == "1550" else 38, z, 12.0, W, "hip", 2, "WE", 3.2, "round")
    if variant == "1550":
        range_block(B1, -52, 40, 32, 60, z, 14.0, W, "hip", 2, "NS", 3.2, "round")
        _chimneys(B1, -48, 44, 28, 56, z + 14.0 + 1.8, 6, W, 0)
    B1[GRASS].box2(-38, -56, 32, 40, z, z + 0.12)
    # a parterre of box hedges round a fountain
    for gx in (-26, 14):
        for gy in (-40, 16):
            B1["#4C6E40"].box2(gx - 9, gy - 9, gx + 9, gy - 8.2, z, z + 0.9)
            B1["#4C6E40"].box2(gx - 9, gy + 8.2, gx + 9, gy + 9, z, z + 0.9)
            B1["#4C6E40"].box2(gx - 9, gy - 9, gx - 8.2, gy + 9, z, z + 0.9)
            B1["#4C6E40"].box2(gx + 8.2, gy - 9, gx + 9, gy + 9, z, z + 0.9)
            tree_into(B1, gx, gy, z, 2.6, "round", "#4E7A47")
    B1[LIOZ].lathe([(4.0, 0), (4.0, 0.7)], -6, -12, z, 12)
    B1[WATER].lathe([(3.4, 0), (3.4, 0.75)], -6, -12, z, 12)
    B1[LIOZ].lathe([(0.6, 0), (0.4, 2.2), (1.4, 2.4), (0, 3.0)], -6, -12, z, 8)
    for x in (-30, -15, 4, 22):
        tree_into(B1, x, -24, z, 1.6, "cypress")
    # Manueline windows and armillary spheres on the Terreiro front
    for k, y in enumerate((-40.0, -12.0, 16.0, 44.0)):
        armillary(B1, 52.6, y, z + hE - 3.0, 1.0, GOLD, "E")
    if variant == "1550":
        sq_tower(B2, 44, -64, 14.0, 24.0, "#E5D9BE", "pyramid", TILE, z)
        for f, a, nrm in (("S", 44, -71.05), ("E", -64, 51.05)):
            opening(B2, f, a, nrm, z + 15.0, 4.0, 5.0, "round", "#3A3128")
            opening(B2, f, a, nrm, z + 9.0, 1.6, 3.0, "round")
        armillary(B2, 44, -71.4, z + 21.0, 1.4, GOLD, "S")
        sq_tower(B2, 44, 56, 10.0, 21.0, "#E5D9BE", "pyramid", TILE, z)
        # the royal chapel on the north range
        B2[LIME].box2(-30, 46, -4, 58, z, 17.0)
        B2[TILE].gable_x(52, -30, -4, 12, 17.0, 4.0)
        layered_portal(B2, "N", -17, 58, z, 4.0, 6.0, 3, LIOZ, "round")
        B2[LIME].box(-30.6, 52, z, 1.2, 4.0, 21.0)
        opening(B2, "W", 52, -31.2, 17.0, 1.6, 2.8, "round")
    else:
        # Filippo Terzi's Torreão on the river: four storeys and a lead dome with a lantern
        T = "#EDE6D6"
        B2[T].box2(28, -75, 55, -48, z, 31.0)
        B2[shade(T, -0.1)].box2(27.5, -75.5, 55.5, -47.5, 30.4, 31.0)
        for zz in (2.0, 9.0, 16.0, 23.0):
            openings(B2, "S", 28, 55, -75, z + zz, 2.0, 3.6, 5, "flat" if zz > 2 else "round")
            openings(B2, "E", -75, -48, 55, z + zz, 2.0, 3.6, 5, "flat" if zz > 2 else "round")
            openings(B2, "W", -75, -48, 28, z + zz, 2.0, 3.6, 5, "flat" if zz > 2 else "round")
        for xx in (28.5, 41.5, 54.5):
            B2[LIOZ].box(xx, -75.2, z, 1.4, 0.8, 30.5)
        for yy in (-74.5, -61.5, -48.5):
            B2[LIOZ].box(55.2, yy, z, 0.8, 1.4, 30.5)
        for k in range(12):
            B2[LIOZ].box(28.6 + k * 2.3, -74.7, 31.0, 0.5, 0.5, 1.1)
            B2[LIOZ].box(54.7, -74.4 + k * 2.3, 31.0, 0.5, 0.5, 1.1)
        B2[LIOZ].box2(30, -73, 53, -50, 31.0, 33.5)
        B2[LEADC].lathe([(12.5, 0), (11.5, 3.0), (8.5, 7.0), (4.0, 9.5), (2.0, 10.0)], 41.5, -61.5, 33.5, 4, math.pi / 4)
        B2[LIOZ].lathe([(2.0, 0), (2.0, 3.2), (2.4, 3.4), (0, 5.4)], 41.5, -61.5, 43.5, 8)
        B2[GOLD].box(41.5, -61.5, 48.9, 0.25, 0.25, 2.0)
        # the Patriarchal church along the north side, its front with twin towers to the west
        P = "#F0EADC"
        range_block(B1, 6, 40, 32, 60, z, 16.0, W, "hip", 3, "NS", 3.2, "round")
        B2[P].box2(-46, 40, 6, 60, z, 25.0)
        B2[TILE].gable_x(50, -46, 6, 20, 25.0, 6.0, 0.4)
        win_rows(B2, -46, 40, 6, 60, [z + 15.0], 4.0, 6.5, 1.8, "NS", "round")
        for sgn in (-1, 1):
            sq_tower(B2, -49, 50 + sgn * 7.5, 6.0, 32.0, P, "pyramid", LEADC, z)
            opening(B2, "W", 50 + sgn * 7.5, -52.05, z + 24.0, 2.0, 3.6, "round")
        B2[P].box2(-52, 44, -46, 56, z, 23.0)
        B2[LIOZ].prism([(-52.4, 43.6), (-52.4, 56.4), (-52.0, 56.4), (-52.0, 43.6)], 23.0, 23.6)
        layered_portal(B2, "W", 50, -52, z, 4.6, 8.0, 3, LIOZ, "round")
        rose(B2, "W", 50, -52, 13.0, 1.8, LIOZ)
        sq_tower(B2, 44, 56, 10.0, 23.0, "#E5D9BE", "pyramid", TILE, z)
    m.add(0, B0.join("pr_g"), "ground")
    m.add(1, B1.join("pr_ranges"), "palace")
    m.add(2, B2.join("pr_towers"), "towers" if variant == "1550" else "torreão")
    return m


def casa_da_india():
    m = Model("casa-da-india")
    B0, B1, B2 = Bufs(), Bufs(), Bufs()
    B0[PAVE].box(0, 0, 0, 60, 34, 0.3)
    B0[LIOZ_D].box2(-30, -17, 30, -11, 0, 0.8)
    z = 0.3
    C = "#E4D7BA"
    range_block(B1, -28, -10, 28, 15, z, 13.0, C, "hip", 2, "EWN", 4.0, "round", arcade_face="S")
    B1[C].box2(-6, -11.5, 6, -10, z, 13.6)
    B1[TILE].gable_y(0, -11.5, -2, 12, 13.0, 3.5, 0.3)
    manueline_portal(B1, "S", 0, -11.5, z, 6.0, 8.0, LIOZ)
    win_rows(B1, -28, -10, 28, 15, [z + 8.0], 2.6, 4.0, 1.4, "S", "round")
    armillary(B1, -14, -10.4, z + 11.0, 0.9, GOLD, "S")
    armillary(B1, 14, -10.4, z + 11.0, 0.9, GOLD, "S")
    # on the quay: a timber crane, bales, sacks of pepper, barrels and a lighter alongside
    B2[WOOD].box(20, -14.5, 0.8, 0.8, 0.8, 9.0)
    B2[WOOD].beam((20, -14.5, 9.0), (24, -18.5, 10.5), (1, -1, 0), 0.5, 0.5)
    B2[WOOD].beam((20, -14.5, 6.0), (23, -17.5, 10.2), (1, -1, 0), 0.3, 0.3)
    B2["#4A4036"].box(24, -18.5, 7.0, 0.1, 0.1, 3.4)
    for k in range(9):
        x, y = -24 + (k % 3) * 2.2 + (k // 3) * 9, -13.2 - (k % 2) * 1.6
        B2["#B89B6C" if k % 2 else "#A88A5A"].box(x, y, 0.8, 1.6, 1.2, 0.9 + (k % 3) * 0.3)
    for k in range(6):
        B2["#C8B48A"].lathe([(0.45, 0), (0.55, 0.5), (0.4, 1.1), (0, 1.2)], -4 + k * 1.3, -14.6, 0.8, 6)
    for k in range(4):
        B2[WOOD].lathe([(0.45, 0), (0.55, 0.5), (0.45, 1.0)], 6 + k * 1.2, -13.0, 0.8, 8)
    m.add(0, B0.join("ci_g"), "quay")
    m.add(1, B1.join("ci_house"), "warehouse")
    m.add(2, B2.join("ci_quay"), "cargo")
    return m


def _slipway(B, x, y0, y1, w, z0, z1):
    """An inclined timber slipway from y0 (low, at the water) to y1 (high)."""
    L = y1 - y0
    B[WOOD_D].hexa([(x - w / 2, y0, 0), (x + w / 2, y0, 0), (x + w / 2, y1, 0), (x - w / 2, y1, 0),
                    (x - w / 2, y0, z0), (x + w / 2, y0, z0), (x + w / 2, y1, z1), (x - w / 2, y1, z1)])
    n = int(L / 2.5)
    for k in range(n + 1):
        yy = y0 + L * k / n
        zz = z0 + (z1 - z0) * k / n
        B[WOOD].box(x, yy, zz, w + 0.6, 0.5, 0.25)


def ribeira_das_naus(variant="1550"):
    m = Model("ribeira-das-naus-" + variant)
    B0, B1, B2 = Bufs(), Bufs(), Bufs()
    B0[SAND].box(0, 0, 0, 130, 70, 0.3)
    B0[YARD].box2(-65, 8, 65, 35, 0.3, 0.4)
    # slipways running down to the water at -Y
    for x in (-30, 22):
        _slipway(B0, x, -35, 8, 13.0, 0.4, 2.6)
    if variant == "1550":
        # a nau in frame and nearly planked, a caravel in ribs
        S = Bufs()
        carrack_into(S, 36.0, 0, 0, 0, 0, rig="bare", flag=False)
        B1.merge(S, 90, -30, -12, 2.0)
        for yy in (-24, -14, -4):
            for sgn in (-1, 1):
                B1[WOOD].beam((-30 + sgn * 6.5, yy, 0.5), (-30 + sgn * 4.4, yy, 6.0), (0, 1, 0), 0.35, 0.35)
        C = Bufs()
        caravel_into(C, 22.0, 0, 0, 0, 0, rig="none", frame=True)
        B1.merge(C, 90, 22, -12, 1.8)
        # sheds, stores and the timber yard
        for x0, x1 in ((-62, -40), (-14, 8)):
            for k in range(6):
                B1[STONE].box(x0 + 1 + (x1 - x0 - 2) * k / 5, 26, 0.4, 1.2, 1.2, 7.0)
            B1[STONE].box2(x0, 30.5, x1, 34.5, 0.4, 7.4)
            B1[TILE].gable_x(28, x0 - 0.5, x1 + 0.5, 13, 7.4, 3.6, 0.4)
        range_block(B1, 36, 18, 62, 34, 0.4, 9.0, "#DCCBA8", "hip", 2, "S", 4.0, "flat")
        for k in range(7):
            B2[WOOD].box(-55 + k * 0.9, 10, 0.4, 0.8, 12.0, 0.8 + (k % 3) * 0.5)
        for k in range(4):
            B2[WOOD_D].beam((-2 + k * 1.2, 2, 0.8), (-2 + k * 1.2, 24, 0.8), (1, 0, 0), 0.7, 0.7)
        for k in range(5):
            B2["#B6A07A"].lathe([(1.1, 0), (1.1, 0.8)], 42 + k * 2.6, 10, 0.4, 10)
        # sheerlegs for stepping masts
        B2[WOOD_D].beam((-6, -30, 0.4), (-2, -30, 16.0), (0, 1, 0), 0.5, 0.5)
        B2[WOOD_D].beam((2, -30, 0.4), (-2, -30, 16.0), (0, 1, 0), 0.5, 0.5)
        B2[WOOD_D].beam((-2, -24, 0.4), (-2, -30, 16.0), (1, 0, 0), 0.4, 0.4)
        for x, y in ((-62, 0), (60, -2)):
            tree_into(B2, x, y, 0.4, 2.8, "pine")
    else:
        # the Arsenal Real da Marinha behind the slipways, a frigate on the stocks
        S = Bufs()
        carrack_into(S, 40.0, 0, 0, 0, 0, rig="bare", flag=False, frigate=True)
        B1.merge(S, 90, -30, -12, 2.0)
        range_block(B1, -62, 14, 62, 34, 0.4, 14.0, POMBAL, "hip", 3, "SEW", 4.2, "flat", arcade_face=None)
        B1[POMBAL].box2(-8, 12.5, 8, 14, 0.4, 16.0)
        b = len(B1[POMBAL].v)
        B1[LIOZ].prism([(-9, 12.4), (9, 12.4), (9, 13.2), (-9, 13.2)], 16.0, 16.6)
        opening(B1, "S", 0, 12.5, 0.4, 4.0, 5.5, "round")
        for k in range(6):
            B2[WOOD].box(36 + k * 0.9, 0, 0.4, 0.8, 12.0, 0.8 + (k % 3) * 0.5)
        C = Bufs()
        caravel_into(C, 24.0, 0, 0, 0, 0, rig="none", frame=True)
        B2.merge(C, 90, 22, -12, 1.8)
    m.add(0, B0.join("rn_g"), "slipways")
    m.add(1, B1.join("rn_ships"), "ships")
    m.add(2, B2.join("rn_yard"), "yard")
    return m



# ================================================================ Pombaline Lisbon
def pombal_range(B, x0, y0, x1, y1, z, h, arcade_face=None, color=POMBAL, storeys=4, spacing=3.6, inner_faces="", dormers=True):
    """A Pombaline block: ground-floor arcade (or shopfronts), three storeys of framed windows with first-floor
    balconies, a cornice and a tiled roof with dormers."""
    B[color].box2(x0, y0, x1, y1, z, z + h)
    B[LIOZ].box2(x0 - 0.3, y0 - 0.3, x1 + 0.3, y1 + 0.3, z + h - 0.7, z + h)
    B[LIOZ].box2(x0 - 0.1, y0 - 0.1, x1 + 0.1, y1 + 0.1, z, z + 0.9)
    B[TILE].hip((x0 + x1) / 2, (y0 + y1) / 2, x1 - x0, y1 - y0, z + h, min(x1 - x0, y1 - y0) * 0.38, 0.4)
    fl = h / storeys
    faces = (arcade_face or "") + inner_faces
    for f in faces:
        L = (x1 - x0) if f in "SN" else (y1 - y0)
        a0 = x0 if f in "SN" else y0
        nrm = {"S": y0, "N": y1, "E": x1, "W": x0}[f]
        n = max(1, int(L / spacing))
        for i in range(n):
            u = a0 + L * (i + 0.5) / n
            if f == arcade_face:
                opening(B, f, u, nrm, z, spacing * 0.62, fl * 0.92, "round", "#3A3128", 0.3)
            else:
                opening(B, f, u, nrm, z, spacing * 0.4, fl * 0.7, "flat", DARK, 0.2)
            for k in range(1, storeys):
                opening(B, f, u, nrm, z + fl * k + fl * 0.22, spacing * 0.34, fl * 0.58, "flat", LIOZ, 0.25)
                opening(B, f, u, nrm, z + fl * k + fl * 0.25, spacing * 0.26, fl * 0.52, "flat", DARK, 0.3)
            # first-floor balcony slab
            off = {"S": -0.6, "N": 0.6, "E": 0.6, "W": -0.6}[f]
            if f in "SN":
                B[LIOZ].box(u, nrm + off, z + fl, spacing * 0.5, 1.0, 0.25)
            else:
                B[LIOZ].box(nrm + off, u, z + fl, 1.0, spacing * 0.5, 0.25)
            if dormers and i % 2 == 0:
                dz = z + h + 0.2
                inset = 1.6
                if f in "SN":
                    yy = nrm + (inset if f == "S" else -inset)
                    B[color].box(u, yy, dz, 1.6, 1.4, 1.8)
                    B[TILE].gable_y(u, yy - 0.7, yy + 0.7, 1.6, dz + 1.8, 0.8, 0.15)
                else:
                    xx = nrm + (-inset if f == "E" else inset)
                    B[color].box(xx, u, dz, 1.4, 1.6, 1.8)
                    B[TILE].gable_x(u, xx - 0.7, xx + 0.7, 1.6, dz + 1.8, 0.8, 0.15)


def _statue_jose(B, x, y, z, s=1.0):
    """Machado de Castro's equestrian José I on its pedestal, with the two groups at its sides (simplified)."""
    BR = "#56654F"
    B[LIOZ].box(x, y, z, 14 * s, 18 * s, 1.0 * s)
    B[LIOZ].box(x, y, z + 1.0 * s, 11 * s, 15 * s, 1.0 * s)
    B[LIOZ_D].box(x, y, z + 2.0 * s, 6.5 * s, 10 * s, 6.0 * s)
    B[LIOZ].box(x, y, z + 8.0 * s, 7.4 * s, 11 * s, 0.8 * s)
    for sgn in (-1, 1):
        B[LIOZ_D].box(x + sgn * 4.6 * s, y, z + 2.0 * s, 2.2 * s, 6 * s, 2.0 * s)
        B[BR].lathe([(0.9 * s, 0), (0.7 * s, 2.6 * s), (0, 3.2 * s)], x + sgn * 4.6 * s, y + 1.2 * s, z + 4.0 * s, 6)
        B[BR].box(x + sgn * 4.6 * s, y - 1.2 * s, z + 4.0 * s, 1.4 * s, 1.6 * s, 1.6 * s)
    BR_MEDAL = GOLD
    B[BR_MEDAL].lathe([(0.9 * s, 0), (0.9 * s, 0.15 * s)], x, y - 5.05 * s, z + 5.0 * s, 10)
    zb = z + 8.8 * s
    # horse (facing south, -Y): body, neck, head, legs (the near foreleg raised), tail
    B[BR].lathe([(0.9 * s, 0), (1.15 * s, 1.0 * s), (1.15 * s, 3.4 * s), (0.85 * s, 4.4 * s)], x, y + 2.2 * s, zb + 3.0 * s, 8, 0)
    hb = Buf()
    hb.lathe([(0.95 * s, 0), (1.2 * s, 1.2 * s), (1.15 * s, 3.4 * s), (0.8 * s, 4.6 * s)], 0, 0, 0, 8)
    # lay the body along Y
    hb.v = [(vx, -vz, vy) for vx, vy, vz in hb.v]
    B[BR].merge(hb, 0, x, y + 2.3 * s, zb + 3.2 * s)
    B[BR].beam((x, y - 1.8 * s, zb + 3.6 * s), (x, y - 3.0 * s, zb + 6.0 * s), (1, 0, 0), 0.9 * s, 1.0 * s)
    B[BR].beam((x, y - 3.0 * s, zb + 6.0 * s), (x, y - 4.4 * s, zb + 5.4 * s), (1, 0, 0), 0.6 * s, 0.8 * s)
    for lx, ly, lz0, lz1, dy in ((-0.5, 1.6, 2.6, 0.0, 0.0), (0.5, 1.6, 2.6, 0.0, 0.0), (-0.5, -1.4, 2.8, 0.0, 0.0), (0.5, -1.4, 3.2, 1.6, -1.2)):
        B[BR].beam((x + lx * s, y + ly * s, zb + lz0 * s + 0.6 * s), (x + lx * s, y + (ly + dy) * s, zb + lz1 * s), (1, 0, 0), 0.4 * s, 0.4 * s)
    B[BR].beam((x, y + 2.4 * s, zb + 3.8 * s), (x, y + 3.4 * s, zb + 1.6 * s), (1, 0, 0), 0.5 * s, 0.4 * s)
    # rider with cloak and plumed helmet
    B[BR].box(x, y - 0.2 * s, zb + 4.3 * s, 1.0 * s, 1.0 * s, 1.9 * s)
    B[BR].box(x, y + 0.2 * s, zb + 4.0 * s, 1.8 * s, 0.6 * s, 1.6 * s)
    B[BR].lathe([(0.35 * s, 0), (0.42 * s, 0.4 * s), (0, 0.8 * s)], x, y - 0.2 * s, zb + 6.2 * s, 6)
    B[BR].lathe([(0.2 * s, 0), (0.35 * s, 0.4 * s), (0, 0.9 * s)], x, y - 0.1 * s, zb + 6.9 * s, 5)
    B[BR].beam((x + 0.6 * s, y - 0.4 * s, zb + 5.2 * s), (x + 0.6 * s, y - 2.0 * s, zb + 5.8 * s), (0, 0, 1), 0.2 * s, 0.2 * s)


def praca_comercio():
    m = Model("praca-comercio")
    B0, B1, B2 = Bufs(), Bufs(), Bufs()
    W, D = 215.0, 200.0
    B0[PAVE].box(0, 0, 0, W, D, 0.3)
    # paving pattern of the square
    for k in range(-4, 5):
        B0["#CFC2A2"].box(k * 18, -6, 0.3, 0.6, 156, 0.06)
        B0["#CFC2A2"].box(0, -6 + k * 18, 0.3, 170, 0.6, 0.06)
    z = 0.3
    h = 16.0
    # east and west wings (arcades face the square), the north range with the opening of the Rua Augusta
    pombal_range(B1, 87.5, -78, 107.5, 100, z, h, "W", inner_faces="E")
    pombal_range(B1, -107.5, -78, -87.5, 100, z, h, "E", inner_faces="W")
    pombal_range(B1, -87.5, 80, -8, 100, z, h, "S", inner_faces="N")
    pombal_range(B1, 8, 80, 87.5, 100, z, h, "S", inner_faces="N")
    # the opening of the Rua Augusta (the arch is later): a plain gap with the street paving
    B0["#CFC2A2"].box(0, 90, 0.3, 16, 20, 0.08)
    # the riverside towers at the ends of the wings, echoing Terzi's Torreão
    for sgn in (-1, 1):
        x0, x1 = sorted((sgn * 85.5, sgn * 107.5))
        B2[POMBAL].box2(x0, -100, x1, -78, z, 22.0)
        B2[LIOZ].box2(x0 - 0.3, -100.3, x1 + 0.3, -77.7, 21.3, 22.0)
        for f in "SEW":
            L0, L1 = (x0, x1) if f == "S" else (-100, -78)
            nrm = {"S": -100, "E": x1, "W": x0}[f]
            openings(B2, f, L0, L1, nrm, z, 3.4, 6.0, 4, "round", "#3A3128")
            for zz in (7.0, 11.5, 16.0):
                openings(B2, f, L0, L1, nrm, z + zz, 1.5, 3.0, 4, "flat")
        for xx in (x0 + 0.4, x1 - 0.4):
            B2[LIOZ].box(xx, -100.3, z, 0.9, 0.7, 21.5)
        B2[LIOZ].box2(x0 + 1, -99, x1 - 1, -79, 22.0, 24.0)
        B2[TILE].lathe([(14.5, 0), (12.0, 2.0), (6.0, 6.0), (0, 7.5)], (x0 + x1) / 2, -89, 24.0, 4, math.pi / 4)
        for k in range(10):
            B2[LIOZ].box(x0 + 1 + k * 2.2, -100.0, 22.0, 0.5, 0.5, 1.0)
    # Cais das Colunas: steps down to the river between two columns
    for k in range(5):
        B0[LIOZ].box2(-14, -100 + k * 0.9, 14, -99.1 + k * 0.9, 0, 0.3 - k * 0.05)
    for sgn in (-1, 1):
        B2[LIOZ].box(sgn * 9, -96.5, z, 2.0, 2.0, 1.2)
        B2[LIOZ].lathe([(0.65, 0), (0.55, 8.5), (1.0, 8.8), (1.0, 9.4)], sgn * 9, -96.5, z + 1.2, 10)
        B2[LIOZ].lathe([(0.9, 0), (0, 1.0)], sgn * 9, -96.5, z + 10.6, 6)
    B0[LIOZ].box2(-107.5, -100, 107.5, -98.5, 0, 0.9)
    # the statue in the middle of the square
    _statue_jose(B2, 0, -8, z, 0.95)
    for x in (-60, 60):
        for y in (-60, 40):
            B2[BRONZE_D].box(x, y, z, 0.3, 0.3, 4.0)
            B2["#E9D9A0"].lathe([(0.4, 0), (0.5, 0.6), (0, 0.8)], x, y, z + 4.0, 6)
    m.add(0, B0.join("pc_g"), "square")
    m.add(1, B1.join("pc_wings"), "arcades")
    m.add(2, B2.join("pc_towers"), "towers and statue")
    return m



# ================================================================ the Rossio
def hospital():
    """Hospital Real de Todos os Santos: the church facing the Rossio (-Y) up a broad stair, an arcaded front,
    cross-shaped wards round four cloisters."""
    m = Model("hospital-todos-os-santos")
    B0, B1, B2 = Bufs(), Bufs(), Bufs()
    B0[PAVE].box(0, 0, 0, 100, 110, 0.3)
    z = 0.3
    C = "#EDE4D0"
    # outer ranges
    range_block(B1, -48, -44, 48, -36, z, 10.0, C, "hip", 2, "N", 3.4, "round", arcade_face="S")
    range_block(B1, -48, -36, -40, 52, z, 10.0, C, "hip", 2, "WE", 3.6, "round")
    range_block(B1, 40, -36, 48, 52, z, 10.0, C, "hip", 2, "WE", 3.6, "round")
    range_block(B1, -40, 44, 40, 52, z, 10.0, C, "hip", 2, "NS", 3.6, "round")
    # the cross of the wards
    range_block(B1, -40, 2, -6, 14, z, 12.0, C, "hip", 2, "NS", 3.4, "round")
    range_block(B1, 6, 2, 40, 14, z, 12.0, C, "hip", 2, "NS", 3.4, "round")
    range_block(B1, -6, -8, 6, 44, z, 13.0, C, "hip", 2, "EW", 3.4, "round")
    B1[shade(C, -0.05)].box(0, 8, z, 14, 14, 16.0)
    B1[TILE].lathe([(10.0, 0), (0, 5.0)], 0, 8, 16.3, 4, math.pi / 4)
    # cloisters: grass, a well, galleries
    for cx, cy in ((-23, -17), (23, -17), (-23, 29), (23, 29)):
        B1[GRASS].box(cx, cy, z, 30, 22 if cy < 0 else 26, 0.12)
        B1[LIOZ].lathe([(1.0, 0), (1.0, 1.0)], cx, cy, z, 8)
        tree_into(B1, cx + 6, cy + 4, z, 2.2, "round", "#4E7A47")
    # the church at the head, its Manueline portal at the top of a stair onto the Rossio
    B2[LIME].box2(-8, -50, 8, -8, z, 17.0)
    B2[TILE].gable_y(0, -50.3, -8, 16, 17.0, 5.0, 0.4)
    for sgn in (-1, 1):
        for k in range(4):
            B2[LIOZ].frustum(sgn * 8.6, -46 + k * 10, z, 1.2, 1.4, 1.0, 0.6, 15.0)
            opening(B2, "E" if sgn > 0 else "W", -41 + k * 10, sgn * 8, 9.0, 1.4, 4.4, "round")
    B2[LIME].box(0, -46, z, 16, 0.1, 0.1)
    manueline_portal(B2, "S", 0, -50, z + 2.0, 8.0, 12.0, LIOZ)
    for k in range(5):
        B2[LIOZ].box2(-9 + k * 0.6, -55 + k * 1.0, 9 - k * 0.6, -50, z, z + 0.4 * (k + 1))
    B2[LIOZ].box2(-12, -50.4, 12, -50, z + 15.5, z + 16.7)
    for x in (-12, 12):
        pinnacle(B2, x, -50.2, z + 16.7, 0.8, 3.5, LIOZ)
    B2[LIME].box(9.5, -46, z, 4.0, 4.0, 22.0)
    B2[TILE].lathe([(3.0, 0), (0, 3.5)], 9.5, -46, z + 22.0, 4, math.pi / 4)
    opening(B2, "S", 9.5, -48.0, z + 17.0, 1.4, 2.8, "round")
    m.add(0, B0.join("hp_g"), "ground")
    m.add(1, B1.join("hp_wards"), "wards")
    m.add(2, B2.join("hp_church"), "church")
    return m


def estaus():
    m = Model("estaus")
    B0, B1, B2 = Bufs(), Bufs(), Bufs()
    B0[PAVE].box(0, 0, 0, 75, 35, 0.3)
    z = 0.3
    C = "#E8DCC4"
    range_block(B1, -30, -16, 32, -3, z, 13.0, C, "hip", 2, "SN", 3.4, "round")
    B1[LIOZ].box2(-6, -17, 6, -16, z, z + 11.0)
    layered_portal(B1, "S", 0, -17, z, 4.0, 6.0, 3, LIOZ, "round")
    christ_cross(B1, 0, -17.6, z + 10.2, 1.8, "S")
    # prison ranges round the court behind
    range_block(B1, -30, -3, -22, 16, z, 9.0, STONE, "hip", 2, "W", 3.0, "flat")
    range_block(B1, 24, -3, 32, 16, z, 9.0, STONE, "hip", 2, "E", 3.0, "flat")
    range_block(B1, -22, 9, 24, 16, z, 9.0, STONE, "hip", 2, "N", 3.0, "flat")
    B1[SAND].box2(-22, -3, 24, 9, z, z + 0.1)
    tree_into(B1, 0, 3, z, 2.4, "round")
    sq_tower(B2, -34.0, -9.5, 9.0, 21.0, C, "pyramid", TILE, z)
    for zz in (6.0, 12.0, 16.5):
        opening(B2, "S", -34.0, -14.0, z + zz, 1.2, 2.2, "round")
        opening(B2, "W", -9.5, -38.5, z + zz, 1.2, 2.2, "round")
    m.add(0, B0.join("es_g"), "ground")
    m.add(1, B1.join("es_palace"), "palace")
    m.add(2, B2.join("es_tower"), "tower")
    return m


# ================================================================ Gothic and Mannerist churches
def _pointed_ring(B, color, xa, xb, y, z_spring, rise, w, t, along="x", n=8):
    """A free-standing pointed arch rib between (xa, z_spring) and (xb, z_spring), along X at y (or along Y at x=y)."""
    span = xb - xa
    pts = []
    for i in range(n + 1):
        u = i / n
        if u <= 0.5:
            a = math.pi / 2 * (u / 0.5)
            px = xa + span * 0.5 * (1 - math.cos(a)) * 1.0
            pz = z_spring + rise * math.sin(a)
        else:
            a = math.pi / 2 * ((1 - u) / 0.5)
            px = xb - span * 0.5 * (1 - math.cos(a))
            pz = z_spring + rise * math.sin(a)
        pts.append((px, pz))
    for (x0, z0), (x1, z1) in zip(pts, pts[1:]):
        if along == "x":
            B[color].beam((x0, y, z0), (x1, y, z1), (0, 1, 0), t, w)
        else:
            B[color].beam((y, x0, z0), (y, x1, z1), (1, 0, 0), t, w)


def carmo(variant="1550"):
    m = Model("carmo-" + variant)
    B0, B1, B2 = Bufs(), Bufs(), Bufs()
    B0[PAVE].box(0, 0, 0, 28, 66, 0.3)
    z = 0.3
    C = "#DCCFB4"
    ruin = variant == "ruin"
    # aisle walls with buttresses
    for sgn in (-1, 1):
        x0, x1 = sorted((sgn * 11, sgn * 10.2))
        B1[C].box2(x0, -30, x1, 20, z, 14.0)
        for k in range(6):
            y = -29 + k * 9.6
            B1[shade(C, -0.07)].frustum(sgn * 12.2, y, z, 2.2, 1.4, 1.0, 1.0, 14.5)
            pinnacle(B1, sgn * 12.0, y, 14.5, 0.9, 3.2, shade(C, -0.07))
            if k < 5:
                opening(B1, "E" if sgn > 0 else "W", y + 4.8, sgn * 11, 5.0, 1.6, 6.5, "pointed", GLASS if not ruin else DARK)
    if not ruin:
        B1[C].box2(-5, -30, 5, 20, z, 23.0)
        B1[TILE].gable_y(0, -30.4, 20, 10, 23.0, 4.0, 0.4)
        for sgn in (-1, 1):
            x0, x1 = sorted((sgn * 5, sgn * 11))
            B1[TILE].lean(x0, -30, x1, 20, 14.0, 17.0, "E" if sgn < 0 else "W")
            for k in range(5):
                opening(B1, "E" if sgn > 0 else "W", -24 + k * 9.6, sgn * 5, 16.5, 1.2, 4.5, "pointed", GLASS)
    else:
        # the open nave: piers with transverse pointed arches, longitudinal arcades, no roof
        B1[GRASS].box2(-10.2, -30, 10.2, 20, z, z + 0.1)
        for k in range(6):
            y = -29 + k * 9.6
            for sgn in (-1, 1):
                B1[C].box(sgn * 5, y, z, 1.6, 1.6, 12.0)
            _pointed_ring(B1, C, -5, 5, y, 12.0 + z, 8.5, 1.4, 1.1, "x", 10)
            if k < 5:
                for sgn in (-1, 1):
                    _pointed_ring(B1, C, y, y + 9.6, sgn * 5, 12.0 + z, 5.5, 1.2, 1.0, "y", 8)
    # apse (still vaulted after 1755) and the side chapels
    apse = [(5.5 * math.cos(a), 20 + 5.5 * math.sin(a)) for a in [i * math.pi / 5 for i in range(6)]]
    B2[C].prism(apse, z, 21.0)
    B2[TILE].lathe([(5.9, 0), (0, 3.6)], 0, 20, 21.0, 10, 0)
    for sgn in (-1, 1):
        sa = [(sgn * 7.6 + 2.6 * math.cos(a), 20 + 2.6 * math.sin(a)) for a in [i * math.pi / 5 for i in range(6)]]
        B2[C].prism(sa, z, 14.0)
        B2[TILE].lathe([(2.9, 0), (0, 2.2)], sgn * 7.6, 20, 14.0, 10, 0)
    for k in range(1, 5):
        a = math.pi * k / 5
        opening(B2, "N", 5.5 * math.cos(a), 20 + 5.5 * math.sin(a) * 0 + 5.4, 7.0, 1.0, 7.0, "pointed", GLASS) if False else None
    # west front with portal and rose
    B2[C].box2(-11, -32, 11, -30, z, 15.0)
    if not ruin:
        B2[C].prism([(-5, -32), (5, -32), (5, -30), (-5, -30)], 15.0, 23.0)
        b = len(B2[C].v)
        B2[C].v += [(-5, -32, 23.0), (5, -32, 23.0), (0, -32, 27.0), (-5, -30, 23.0), (5, -30, 23.0), (0, -30, 27.0)]
        B2[C].f += [(b, b + 1, b + 2), (b + 5, b + 4, b + 3), (b, b + 3, b + 4, b + 1), (b + 1, b + 4, b + 5, b + 2), (b + 2, b + 5, b + 3, b)]
        rose(B2, "S", 0, -32, 16.5, 2.4, LIOZ)
    else:
        B2[C].box2(-5, -32, 5, -30, 15.0, 19.0)
    layered_portal(B2, "S", 0, -32, z, 6.0, 10.0, 4, LIOZ, "pointed")
    for sgn in (-1, 1):
        B2[shade(C, -0.07)].frustum(sgn * 5.5, -33, z, 1.4, 2.0, 1.0, 1.0, 16.0 if not ruin else 15.0)
    m.add(0, B0.join("cm_g"), "ground")
    m.add(1, B1.join("cm_nave"), "nave" if not ruin else "ruined nave")
    m.add(2, B2.join("cm_front"), "front and apse")
    return m


def sao_roque(variant="church"):
    m = Model("sao-roque-" + variant)
    B0, B1, B2 = Bufs(), Bufs(), Bufs()
    B0[PAVE].box(0, 0, 0, 30, 62, 0.3)
    z = 0.3
    if variant == "ermida":
        # the small plague chapel of 1506 with a porch and a bell-cote, in its walled yard
        B1[LIME].box2(-4.5, -6, 4.5, 10, z, 7.0)
        B1[TILE].gable_y(0, -6.3, 10, 9, 7.0, 2.8, 0.3)
        B1[LIME].box2(-3.5, 10, 3.5, 15, z, 6.0)
        B1[TILE].gable_y(0, 10, 15.3, 7, 6.0, 2.3, 0.3)
        B1[LIME].box2(-4.5, -11, 4.5, -6, z, 0.4)
        for x in (-4, 4):
            B1[LIOZ].box(x, -10.5, z, 0.6, 0.6, 4.0)
        B1[TILE].lean(-4.8, -11, 4.8, -6, 4.2, 5.6, "N")
        opening(B1, "S", 0, -6, z, 1.8, 3.0, "round")
        B2[LIME].prism([(-1.6, -6.2), (1.6, -6.2), (1.6, -5.4), (-1.6, -5.4)], 9.8, 12.0)
        opening(B2, "S", 0, -6.2, 10.0, 1.0, 1.6, "round")
        wall_line(B1, [(-12, -20), (12, -20), (12, 24), (-12, 24), (-12, -20)], 2.2, 0.6, LIME, z, False)
        for x, y in ((-8, 0), (8, 6), (-7, 18), (7, -14)):
            tree_into(B2, x, y, z, 2.2, "round")
        tree_into(B2, 9, 20, z, 1.4, "cypress")
    else:
        C = "#ECE6D8"
        B1[C].box2(-12, -31, 12, 22, z, 19.0)
        B1[TILE].gable_y(0, -31.3, 22, 24, 19.0, 5.5, 0.4)
        for sgn in (-1, 1):
            x0, x1 = sorted((sgn * 12, sgn * 14.6))
            B1[C].box2(x0, -26, x1, 18, z, 10.0)
            B1[TILE].lean(x0, -26, x1, 18, 10.0, 12.0, "W" if sgn > 0 else "E")
            for k in range(5):
                opening(B1, "E" if sgn > 0 else "W", -22 + k * 9.5, sgn * 12, 12.75, 2.2, 3.7, "flat", LIOZ, 0.14)
                opening(B1, "E" if sgn > 0 else "W", -22 + k * 9.5, sgn * 12, 13.0, 1.6, 3.2, "flat", GLASS)
                opening(B1, "E" if sgn > 0 else "W", -22 + k * 9.5, sgn * 14.6, 3.0, 1.2, 2.4, "flat", GLASS)
            for k in range(6):
                B1[LIOZ].box(sgn * 12.2, -26.5 + k * 9.5, 10.0, 0.5, 1.0, 9.0)
                B1[LIOZ].box(sgn * 14.8, -26.5 + k * 8.8, z, 0.5, 0.9, 9.7)
            B1[LIOZ].box2(sgn * 12 - 0.35, -31, sgn * 12 + 0.35, 22, 18.3, 19.0)
        B1[C].box2(-7, 22, 7, 31, z, 16.0)
        B1[TILE].hip(0, 26.5, 14, 9, 16.0, 3.0, 0.3)
        # the plain Mannerist front: pilasters, a portal with pediment, three windows, a low pediment
        for x in (-11.6, -4.0, 4.0, 11.6):
            B2[LIOZ].box(x, -31.3, z, 1.2, 0.6, 18.7)
        B2[LIOZ].box2(-12.3, -31.6, 12.3, -31, 9.0, 9.8)
        B2[LIOZ].box2(-12.3, -31.6, 12.3, -31, 18.4, 19.2)
        opening(B2, "S", 0, -31.6, z, 3.0, 5.6, "flat")
        B2[LIOZ].prism([(-2.6, -32.0), (2.6, -32.0), (0, -32.0)], 0, 0) if False else None
        B2[LIOZ].box2(-2.4, -32.0, 2.4, -31.4, z + 5.6, z + 6.2)
        for x in (-7.8, 0, 7.8):
            opening(B2, "S", x, -31.6, 11.5, 1.8, 4.6, "flat", GLASS)
        for x in (-7.8, 7.8):
            opening(B2, "S", x, -31.6, z, 1.8, 4.0, "flat")
        b = len(B2[LIOZ].v)
        B2[LIOZ].v += [(-12.3, -31.8, 19.2), (12.3, -31.8, 19.2), (0, -31.8, 24.5), (-12.3, -30.8, 19.2), (12.3, -30.8, 19.2), (0, -30.8, 24.5)]
        B2[LIOZ].f += [(b, b + 1, b + 2), (b + 5, b + 4, b + 3), (b, b + 3, b + 4, b + 1), (b + 1, b + 4, b + 5, b + 2), (b + 2, b + 5, b + 3, b)]
        B2[C].box(10.5, 25.5, z, 5.0, 5.0, 24.0)
        for f in "SNEW":
            opening(B2, f, 10.5 if f in "SN" else 25.5, {"S": 23.0, "N": 28.0, "E": 13.0, "W": 8.0}[f], 19.0, 1.4, 3.0, "round")
        B2[TILE].lathe([(3.8, 0), (0, 3.0)], 10.5, 25.5, 24.3, 4, math.pi / 4)
    m.add(0, B0.join("sr_g"), "ground")
    m.add(1, B1.join("sr_nave"), "nave")
    m.add(2, B2.join("sr_front"), "front")
    return m


def misericordia(variant="1550"):
    m = Model("misericordia-" + variant)
    B0, B1, B2 = Bufs(), Bufs(), Bufs()
    B0[PAVE].box(0, 0, 0, 40, 24, 0.3)
    z = 0.3
    if variant == "1550":
        C = "#EEE6D6"
        B1[C].box2(-20, -7, 12, 7, z, 15.0)
        B1[TILE].gable_x(0, -20.3, 12, 14, 15.0, 4.5, 0.4)
        B1[C].box2(12, -5, 19.5, 5, z, 13.0)
        B1[TILE].gable_x(0, 12, 19.8, 10, 13.0, 3.5, 0.3)
        for x in (-16, 7):
            opening(B1, "S", x, -7, 9.0, 1.4, 3.6, "round", GLASS)
        for k in range(5):
            B1[LIOZ].frustum(-19.5 + k * 7.8, -7.6, z, 1.0, 1.2, 0.8, 0.6, 13.5)
            pinnacle(B1, -19.5 + k * 7.8, -7.6, z + 13.5, 0.8, 3.0, LIOZ)
        B1[LIOZ].box2(-20.3, -7.4, 12.3, -7, 14.2, 15.0)
        manueline_portal(B2, "S", -4.0, -7.0, z, 9.0, 13.0, LIOZ)
        B2[C].box(-21.0, 0, z, 2.0, 5.0, 19.0)
        opening(B2, "W", 0, -22.0, 15.0, 1.8, 2.8, "round")
    else:
        # the Conceição Velha: a plainer, taller church rebuilt behind the surviving south wall and portal
        C = "#E9DFC9"
        B1[C].box2(-20, -7, 14, 7, z, 17.0)
        B1[TILE].hip(-3, 0, 34, 14, 17.0, 4.2, 0.4)
        B1[C].box2(14, -5, 19.5, 5, z, 14.0)
        B1[TILE].hip(16.8, 0, 5.5, 10, 14.0, 2.6, 0.3)
        for x in (-16, -10, 3, 9):
            opening(B1, "S", x, -7, 12.0, 1.4, 2.6, "flat", GLASS)
        B1[LIOZ].box2(-20.3, -7.4, 14.3, -7, 16.3, 17.0)
        manueline_portal(B2, "S", -4.0, -7.0, z, 9.0, 13.0, LIOZ)
        B2[C].box(-18, 4, z, 4.0, 4.0, 21.0)
        for f in "SW":
            opening(B2, f, -18 if f == "S" else 4, -20.0 if f == "W" else 2.0, 17.5, 1.4, 2.4, "round")
        B2[TILE].lathe([(3.0, 0), (0, 2.6)], -18, 4, 21.3, 4, math.pi / 4)
    m.add(0, B0.join("mi_g"), "ground")
    m.add(1, B1.join("mi_nave"), "church")
    m.add(2, B2.join("mi_portal"), "portal")
    return m


def casa_dos_bicos(variant="1550"):
    m = Model("casa-dos-bicos-" + variant)
    B0, B1, B2 = Bufs(), Bufs(), Bufs()
    B0[PAVE].box(0, 0, 0, 25, 14, 0.3)
    z = 0.3
    h = 16.0 if variant == "1550" else 8.2
    C = "#E6DECB"
    B1[C].box2(-12, -6, 12, 6, z, z + h)
    B1[TILE].hip(0, 0, 24, 12, z + h, 3.6, 0.5)
    # the diamond points
    rows = int(h / 0.9)
    for r in range(rows):
        for c in range(26):
            x = -11.5 + c * 0.92
            zz = z + 0.6 + r * 0.9
            if (r < 3 and c in (5, 6, 7, 18, 19)) or (r >= 6 and r < 9 and c in (3, 4, 11, 12, 13, 21, 22)) or (r >= 12 and r < 15 and c in (6, 7, 16, 17)):
                continue
            B1[LIOZ].lathe([(0.48, 0), (0, 0.32)], 0, 0, 0, 4, math.pi / 4)
            sub = B1[LIOZ]
            n0 = len(sub.v) - 5
            for j in range(n0, len(sub.v)):
                vx, vy, vz = sub.v[j]
                sub.v[j] = (x + vx, -6.0 - vz, zz + vy + 0.4)
    # doors below, Manueline windows above (irregular, as on the house)
    for x in (-5.5, 6.5):
        opening(B2, "S", x, -6.3, z, 1.8, 2.8, "round")
    opening(B2, "S", 0.5, -6.3, z, 1.2, 2.2, "flat")
    for x in (-7.5, 0.5, 8.5):
        opening(B2, "S", x, -6.3, z + 6.0, 1.5, 2.4, "round")
    if variant == "1550":
        for x in (-5.0, 5.0):
            opening(B2, "S", x, -6.3, z + 11.2, 2.2, 2.4, "round")
            B2[LIOZ].box(x, -6.6, z + 10.9, 2.8, 0.6, 0.3)
    win_rows(B2, -12, -6, 12, 6, [z + 2.5, z + 6.5] + ([z + 10.5] if variant == "1550" else []), 2.0, 4.0, 1.2, "NEW", "flat")
    m.add(0, B0.join("cb_g"), "ground")
    m.add(1, B1.join("cb_house"), "house")
    m.add(2, B2.join("cb_win"), "windows")
    return m


def chafariz():
    m = Model("chafariz-del-rei")
    B0, B1, B2 = Bufs(), Bufs(), Bufs()
    B0[LIOZ_D].box(0, 0, 0, 30, 10, 0.3)
    z = 0.3
    C = "#DCD0B5"
    B1[C].box2(-14, 0.5, 14, 4, z, 6.0)
    B1[C].box2(-14.5, 0.3, 14.5, 4.2, 6.0, 6.5)
    box_merlons(B1[C], -14, 0.5, 14, 4, 6.5, 0.8, 0.7, "SNEW", 0.5)
    openings(B1, "S", -13, 13, 0.5, z + 0.8, 3.0, 4.2, 6, "round", "#4A5458")
    for k in range(6):
        x = -13 + 26 * (k + 0.5) / 6
        B1[BRONZE_D].beam((x, 0.4, z + 2.2), (x, -0.6, z + 2.0), (1, 0, 0), 0.25, 0.25)
        B1[LIOZ].box(x, 0.45, z + 4.4, 0.8, 0.2, 0.8)
    # the trough with water
    B1[LIOZ].box2(-14, -2.2, 14, 0.5, z, z + 0.9)
    B1[WATER].box2(-13.6, -1.8, 13.6, 0.3, z, z + 0.92)
    # steps at the ends and the royal arms in the middle
    for sgn in (-1, 1):
        for k in range(4):
            B2[C].box(sgn * (14.8 + k * 0.0), 2.25, z, 1.4, 3.5, 1.2 + k * 1.3) if k == 0 else None
    # the royal arms: a shield with the five blue escutcheons (quinas)
    B2[C].box(0, 0.3, 6.5, 3.0, 0.6, 2.6)
    B2[LIME].box(0, -0.05, 6.9, 1.8, 0.2, 1.9)
    for dx, dz in ((0, 0.75), (-0.5, 0.75), (0.5, 0.75), (0, 1.25), (0, 0.25)):
        B2[AZUL].box(dx, -0.2, 6.9 + dz + 0.05, 0.32, 0.12, 0.4)
    B2[RED].box(0, -0.12, 8.8, 2.0, 0.1, 0.2)
    for x in (-12, 12):
        B2["#7A6A50"].lathe([(0.45, 0), (0.55, 0.6), (0.4, 1.1)], x, -3.5, z, 8)
    m.add(0, B0.join("cf_g"), "ground")
    m.add(1, B1.join("cf_wall"), "fountain")
    m.add(2, B2.join("cf_top"), "arms")
    return m


def opera_do_tejo():
    m = Model("opera-do-tejo")
    B0, B1, B2 = Bufs(), Bufs(), Bufs()
    B0[PAVE].box(0, 0, 0, 42, 72, 0.3)
    z = 0.3
    C = "#EFE6D3"
    B1[C].box2(-20, -35, 20, 6, z, 21.0)
    B1[TILE].hip(0, -14.5, 40, 41, 21.0, 6.0, 0.5)
    win_rows(B1, -20, -35, 20, 6, [z + 7.0, z + 13.0], 3.0, 3.4, 1.6, "EW", "round", frame=LIOZ)
    for sgn in (-1, 1):
        for k in range(8):
            B1[LIOZ].box(sgn * 20.2, -33.5 + k * 5.6, z, 0.5, 1.0, 20.5)
    # the front: pilasters, three doors, two rows of windows, a balustrade and a crowning pediment
    for k in range(7):
        B1[LIOZ].box(-18 + k * 6, -35.3, z, 1.4, 0.7, 20.5)
    for x in (-6, 0, 6):
        opening(B1, "S", x, -35.6, z, 3.0, 5.6, "round", "#3A3128")
    for x in (-15, -9, -3, 3, 9, 15):
        opening(B1, "S", x, -35.6, z + 8.0, 2.2, 4.4, "round", GLASS)
        opening(B1, "S", x, -35.6, z + 14.0, 1.8, 3.0, "flat", GLASS)
    B1[LIOZ].box2(-20.4, -35.8, 20.4, -34.6, 20.4, 21.2)
    for k in range(18):
        B1[LIOZ].box(-19.2 + k * 2.26, -35.3, 21.2, 0.4, 0.4, 1.0)
    B1[LIOZ].box2(-20.4, -35.8, 20.4, -34.6, 22.2, 22.6)
    b = len(B2[LIOZ].v)
    B2[LIOZ].v += [(-8, -35.8, 22.6), (8, -35.8, 22.6), (0, -35.8, 26.0), (-8, -34.6, 22.6), (8, -34.6, 22.6), (0, -34.6, 26.0)]
    B2[LIOZ].f += [(b, b + 1, b + 2), (b + 5, b + 4, b + 3), (b, b + 3, b + 4, b + 1), (b + 1, b + 4, b + 5, b + 2), (b + 2, b + 5, b + 3, b)]
    for x in (-8, 0, 8):
        B2[LIOZ].lathe([(0.45, 0), (0.4, 1.8), (0, 2.2)], x, -35.2, 26.0 if x == 0 else 22.6, 6)
    # the fly tower over the deep stage
    B2[C].box2(-16, 4, 16, 34, z, 29.0)
    B2[TILE].gable_x(19, -16.4, 16.4, 30, 29.0, 6.5, 0.4)
    win_rows(B2, -16, 4, 16, 34, [z + 22.0], 2.6, 5.0, 1.4, "EWN", "round")
    m.add(0, B0.join("op_g"), "ground")
    m.add(1, B1.join("op_house"), "auditorium")
    m.add(2, B2.join("op_fly"), "stage house")
    return m


def sao_vicente(variant="1750"):
    m = Model("sao-vicente-" + variant)
    B0, B1, B2 = Bufs(), Bufs(), Bufs()
    B0[PAVE].box(0, 0, 0, 60, 90, 0.3)
    z = 0.3
    if variant == "old":
        C = "#DCD0B6"
        B1[C].box2(-7, -32, 7, 22, z, 15.0)
        B1[TILE].gable_y(0, -32.3, 22, 14, 15.0, 4.2, 0.4)
        for sgn in (-1, 1):
            x0, x1 = sorted((sgn * 7, sgn * 12))
            B1[C].box2(x0, -26, x1, 18, z, 9.0)
            B1[TILE].lean(x0, -26, x1, 18, 9.0, 11.5, "E" if sgn < 0 else "W")
        apse = [(6 * math.cos(a), 22 + 6 * math.sin(a)) for a in [i * math.pi / 6 for i in range(7)]]
        B1[C].prism(apse, z, 13.0)
        B1[TILE].lathe([(6.3, 0), (0, 3.2)], 0, 22, 13.0, 12, 0)
        layered_portal(B1, "S", 0, -32, z, 5.0, 7.0, 3, LIOZ, "round")
        sq_tower(B2, -10, -28, 7.0, 22.0, C, "pyramid", TILE, z)
        # the Augustinian cloister and the canons' ranges
        for (x0, y0, x1, y1) in ((14, -30, 28, -24), (14, 14, 28, 20), (14, -24, 18, 14), (24, -24, 28, 14)):
            B1[LIME].box2(x0, y0, x1, y1, z, 8.0)
            B1[TILE].hip((x0 + x1) / 2, (y0 + y1) / 2, x1 - x0, y1 - y0, 8.0, 2.2, 0.3)
        B1[GRASS].box2(18, -24, 24, 14, z, z + 0.1)
        for x, y in ((-20, -20), (-22, 10), (-18, 30), (20, 32)):
            tree_into(B2, x, y, z, 3.0, "round")
    else:
        C = "#F0EBDF"
        # nave, side chapels, transept, chancel
        B1[C].box2(-11, -36, 11, 10, z, 25.0)
        B1[LEADC if False else TILE].gable_y(0, -36, 10, 22, 25.0, 6.0, 0.4)
        for sgn in (-1, 1):
            x0, x1 = sorted((sgn * 11, sgn * 17))
            B1[C].box2(x0, -34, x1, 10, z, 15.0)
            B1[TILE].lean(x0, -34, x1, 10, 15.0, 17.5, "E" if sgn < 0 else "W")
            for k in range(4):
                opening(B1, "E" if sgn > 0 else "W", -28 + k * 10, sgn * 11, 18.0, 2.2, 4.0, "round", GLASS)
        B1[C].box2(-25, 10, 25, 24, z, 25.0)
        B1[TILE].gable_x(17, -25.4, 25.4, 14, 25.0, 5.0, 0.4)
        B1[C].box2(-9, 24, 9, 43, z, 22.0)
        B1[TILE].gable_y(0, 24, 43.3, 18, 22.0, 5.0, 0.4)
        # cloister ranges to the east
        for (x0, y0, x1, y1) in ((17, -34, 30, -28), (17, 2, 30, 8), (26, -28, 30, 2)):
            B1[C].box2(x0, y0, x1, y1, z, 12.0)
            B1[TILE].hip((x0 + x1) / 2, (y0 + y1) / 2, x1 - x0, y1 - y0, 12.0, 2.0, 0.3)
        B1[GRASS].box2(17, -28, 26, 2, z, z + 0.1)
        openings(B1, "W", -28, 2, 26, z, 2.2, 3.6, 8, "round", "#3A3128")
        win_rows(B1, -25, 10, 25, 24, [z + 16.0], 4.0, 4.5, 1.8, "EW", "round", GLASS, frame=LIOZ)
        win_rows(B1, -9, 24, 9, 43, [z + 14.0], 4.0, 4.5, 1.8, "EWN", "round", GLASS, frame=LIOZ)
        for sgn in (-1, 1):
            for k in range(5):
                B1[LIOZ].box(sgn * 17.2, -33 + k * 10.5, z, 0.5, 1.1, 14.6)
                B1[LIOZ].box(sgn * 11.2, -33 + k * 10.5, 15.0, 0.5, 1.1, 9.8)
        # crossing: the dome (lost in 1755) or a low hipped roof after
        if variant == "1750":
            B2[C].lathe([(7.5, 0), (7.5, 6.0)], 0, 17, 25.0, 16)
            for k in range(8):
                a = math.tau * (k + 0.5) / 8
                B2[GLASS].box(7.55 * math.cos(a), 17 + 7.55 * math.sin(a), 26.5, 1.0, 1.0, 3.0, a)
            B2[LEADC].lathe([(7.8, 0), (7.2, 3.0), (5.4, 6.0), (2.6, 8.0), (1.2, 8.4)], 0, 17, 31.0, 16)
            B2[C].lathe([(1.4, 0), (1.4, 2.6), (0, 4.2)], 0, 17, 39.4, 8)
        else:
            B2[C].box(0, 17, 25.0, 15, 14, 3.0)
            B2[TILE].hip(0, 17, 15, 14, 28.0, 3.0, 0.3)
        # the white front: two towers, three arched doors, niches, a central pediment
        B2[C].box2(-25, -45, 25, -36, z, 27.0)
        for k in range(6):
            B2[LIOZ].box(-22.5 + k * 9, -45.3, z, 1.6, 0.7, 26.5)
        for x in (-7.5, 0, 7.5):
            opening(B2, "S", x, -45.6, z, 3.2 if x == 0 else 2.8, 7.0 if x == 0 else 6.2, "round", "#3A3128")
            opening(B2, "S", x, -45.6, 13.0, 1.6, 3.4, "round", LIOZ_D)
            opening(B2, "S", x, -45.6, 19.0, 2.0, 4.0, "round", GLASS)
        B2[LIOZ].box2(-25.3, -45.6, 25.3, -44.8, 11.0, 11.8)
        B2[LIOZ].box2(-25.3, -45.6, 25.3, -44.8, 26.4, 27.2)
        b = len(B2[LIOZ].v)
        B2[LIOZ].v += [(-12, -45.4, 27.2), (12, -45.4, 27.2), (0, -45.4, 31.5), (-12, -44.0, 27.2), (12, -44.0, 27.2), (0, -44.0, 31.5)]
        B2[LIOZ].f += [(b, b + 1, b + 2), (b + 5, b + 4, b + 3), (b, b + 3, b + 4, b + 1), (b + 1, b + 4, b + 5, b + 2), (b + 2, b + 5, b + 3, b)]
        for sgn in (-1, 1):
            x = sgn * 20.5
            B2[C].box(x, -40.5, 27.0, 9.0, 9.0, 9.0)
            for f in "SNEW":
                al = x if f in "SN" else -40.5
                nrm = {"S": -45.0, "N": -36.0, "E": x + 4.5, "W": x - 4.5}[f]
                opening(B2, f, al, nrm, 28.5, 2.6, 5.0, "round")
            B2[LIOZ].box(x, -40.5, 36.0, 9.6, 9.6, 0.7)
            B2[C].lathe([(3.4, 0), (3.4, 2.0)], x, -40.5, 36.7, 8)
            B2[LEADC].lathe([(3.6, 0), (2.8, 1.8), (1.2, 3.0), (0, 3.4)], x, -40.5, 38.7, 8)
            B2[GOLD].box(x, -40.5, 42.1, 0.2, 0.2, 1.4)
    m.add(0, B0.join("sv_g"), "ground")
    m.add(1, B1.join("sv_church"), "church")
    m.add(2, B2.join("sv_front"), "front" if variant != "1750" else "front and dome")
    return m

BUILDERS = {
    "lisbon/castelo": lambda: castelo("1550"),
    "lisbon/castelo-roman": lambda: castelo("roman"),
    "lisbon/castelo-moorish": lambda: castelo("moorish"),
    "lisbon/castelo-1800": lambda: castelo("1800"),
    "lisbon/se": lambda: se("1550"),
    "lisbon/se-1800": lambda: se("1800"),
    "lisbon/se-mosque": se_mosque,
    "lisbon/roman-theatre": roman_theatre,
    "lisbon/porta-do-sol": porta_do_sol,
    "lisbon/porta-santo-antao": porta_santo_antao,
    "lisbon/paco-ribeira": lambda: paco_ribeira("1550"),
    "lisbon/paco-ribeira-1750": lambda: paco_ribeira("1750"),
    "lisbon/casa-da-india": casa_da_india,
    "lisbon/ribeira-das-naus": lambda: ribeira_das_naus("1550"),
    "lisbon/ribeira-das-naus-1800": lambda: ribeira_das_naus("1800"),
    "lisbon/praca-comercio": praca_comercio,
    "lisbon/hospital-todos-os-santos": hospital,
    "lisbon/estaus": estaus,
    "lisbon/carmo": lambda: carmo("1550"),
    "lisbon/carmo-ruin": lambda: carmo("ruin"),
    "lisbon/sao-roque": lambda: sao_roque("church"),
    "lisbon/sao-roque-ermida": lambda: sao_roque("ermida"),
    "lisbon/misericordia": lambda: misericordia("1550"),
    "lisbon/conceicao-velha": lambda: misericordia("1800"),
    "lisbon/casa-dos-bicos": lambda: casa_dos_bicos("1550"),
    "lisbon/casa-dos-bicos-1800": lambda: casa_dos_bicos("1800"),
    "lisbon/chafariz-del-rei": chafariz,
    "lisbon/opera-do-tejo": opera_do_tejo,
    "lisbon/sao-vicente": lambda: sao_vicente("1750"),
    "lisbon/sao-vicente-old": lambda: sao_vicente("old"),
    "lisbon/sao-vicente-1800": lambda: sao_vicente("1800"),
}
