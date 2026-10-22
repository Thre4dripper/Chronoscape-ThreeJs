"""Córdoba landmark miniatures: Roman Corduba (forum, temple, theatre, mausoleum, bridge), the Umayyad Great Mosque in four
states, the Alcázars, the river mills and gates, and the Castilian city of synagogue and Fernandine churches.

Conventions as in FORMAT.md: metres, origin at the ground centre, +X east, +Y north, +Z up, the main front (the mosque's
qibla) toward -Y; the landmark rotation turns it on the map. Repetitive parts (arcades, merlons, roofs, trees) are
accumulated in a Buf (one mesh per colour) instead of thousands of separate objects.
"""
import math
import bpy
from chronokit import Model, box, cylinder, dome, join, shade, gable_roof, hip_roof, mesh_from, ellipse_ring, columns, mini_temple
from worldkit import *

# ---------------------------------------------------------------- palette
STONE = "#D6BE93"        # Córdoba calcarenite, golden
STONE_L = "#E6D6B4"
STONE_D = "#BCA37A"
HALL = "#CDB68C"
VR = "#A9452F"           # red brick voussoirs
VW = "#EFE5CF"           # cream stone voussoirs
TILE = "#B4683F"         # roof tile
TILE_D = "#9A5636"
GROUND = "#CDB88E"
PAVE = "#DCCBA6"
LIME = "#EEE6D4"         # whitewash
LEAF = "#58804A"
ORANGE_LEAF = "#3F6B3A"
PALM_C = "#6E8A55"
CYPRESS = "#46633F"
TRUNK = "#7A5C3E"
GOLD = "#D2AE52"
SILVER = "#D8D8D0"
GLASS = "#3D4C70"
WOOD = "#7A5A3C"
WATER_C = "#5F878C"
MARBLES = ["#EEE8DC", "#8F837B", "#A6705E", "#C9C2B4", "#6F7C78"]
HOUSES = ["#EDE4D0", "#E2D4B6", "#F2ECDF", "#D9C6A2", "#E8DCC4"]
FACE_ROT = {"S": 0, "N": 180, "E": 90, "W": -90}


# ---------------------------------------------------------------- mesh accumulator
class Buf:
    """Collects many simple solids into one mesh (one colour)."""

    def __init__(self):
        self.v, self.f = [], []

    def hexa(self, c):
        """Eight corners: a bottom quad then the matching top quad."""
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
        L = math.sqrt(sum(c * c for c in d)) or 1.0
        sl = math.sqrt(sum(c * c for c in side)) or 1.0
        e1 = [c / sl * w / 2 for c in side]
        n = [d[1] * side[2] - d[2] * side[1], d[2] * side[0] - d[0] * side[2], d[0] * side[1] - d[1] * side[0]]
        nl = math.sqrt(sum(c * c for c in n)) or 1.0
        e2 = [c / nl * t / 2 for c in n]
        c = []
        for p in (p0, p1):
            for s1, s2 in ((-1, -1), (1, -1), (1, 1), (-1, 1)):
                c.append(tuple(p[i] + s1 * e1[i] + s2 * e2[i] for i in range(3)))
        self.hexa([c[0], c[1], c[2], c[3], c[4], c[5], c[6], c[7]])

    def gable_y(self, cx, y0, y1, w, z, h, over=0.15):
        """A gable roof with its ridge along Y."""
        W = w / 2 + over
        b = len(self.v)
        self.v += [(cx - W, y0, z), (cx + W, y0, z), (cx, y0, z + h), (cx - W, y1, z), (cx + W, y1, z), (cx, y1, z + h)]
        self.f += [(b, b + 1, b + 2), (b + 5, b + 4, b + 3), (b, b + 3, b + 4, b + 1), (b + 1, b + 4, b + 5, b + 2), (b + 2, b + 5, b + 3, b)]

    def gable_x(self, cy, x0, x1, d, z, h, over=0.15):
        D = d / 2 + over
        b = len(self.v)
        self.v += [(x0, cy - D, z), (x0, cy + D, z), (x0, cy, z + h), (x1, cy - D, z), (x1, cy + D, z), (x1, cy, z + h)]
        self.f += [(b, b + 1, b + 2), (b + 5, b + 4, b + 3), (b, b + 3, b + 4, b + 1), (b + 1, b + 4, b + 5, b + 2), (b + 2, b + 5, b + 3, b)]

    def tri_y(self, cx, y, w, z, h, t):
        """A gable triangle (wall) standing across X at y."""
        b = len(self.v)
        self.v += [(cx - w / 2, y - t / 2, z), (cx + w / 2, y - t / 2, z), (cx, y - t / 2, z + h), (cx - w / 2, y + t / 2, z), (cx + w / 2, y + t / 2, z), (cx, y + t / 2, z + h)]
        self.f += [(b, b + 1, b + 2), (b + 5, b + 4, b + 3), (b, b + 3, b + 4, b + 1), (b + 1, b + 4, b + 5, b + 2), (b + 2, b + 5, b + 3, b)]

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


# ---------------------------------------------------------------- small helpers
def place(o, ang=0.0, x=0.0, y=0.0, z=0.0):
    o = move(o)
    if ang:
        o = rot(o, ang)
    return move(o, x, y, z)


def voussoirs(B, plane, c_along, c_across, zc, r0, r1, a0, a1, n, t, colors=(VR, VW)):
    """An arch ring of n alternating voussoirs in a vertical plane. plane 'x': spans along X at y = c_across;
    plane 'y': spans along Y at x = c_across. Angles in degrees, 0 = toward +along, 90 = up."""
    for k in range(n):
        A = math.radians(a0 + (a1 - a0) * k / n)
        Bn = math.radians(a0 + (a1 - a0) * (k + 1) / n)
        pts = []
        for s in (-1, 1):
            for r, a in ((r0, A), (r1, A), (r1, Bn), (r0, Bn)):
                u, z = c_along + r * math.cos(a), zc + r * math.sin(a)
                if plane == "x":
                    pts.append((u, c_across + s * t / 2, z))
                else:
                    pts.append((c_across + s * t / 2, u, z))
        B[colors[k % len(colors)]].hexa(pts)


def stepped_merlons(Bb, x0, y0, x1, y1, z, size=0.9, gap=0.8, sides="SNEW", t=0.8):
    """Córdoba's stepped (Andalusi) merlons along the sides of a rectangle."""
    step = size + gap
    for side in sides:
        if side in "SN":
            y = y0 + t / 2 if side == "S" else y1 - t / 2
            L = x1 - x0
            n = max(1, int(L / step))
            for i in range(n):
                x = x0 + (i + 0.5) * L / n
                Bb.box(x, y, z, size, t, size * 0.7)
                Bb.box(x, y, z + size * 0.7, size * 0.5, t, size * 0.5)
        else:
            x = x0 + t / 2 if side == "W" else x1 - t / 2
            L = y1 - y0
            n = max(1, int(L / step))
            for i in range(n):
                y = y0 + (i + 0.5) * L / n
                Bb.box(x, y, z, t, size, size * 0.7)
                Bb.box(x, y, z + size * 0.7, t, size * 0.5, size * 0.5)


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


def tree_into(B, x, y, z, r, kind="round", leaf=LEAF):
    if kind == "palm":
        h = r * 3.6
        B[TRUNK].lathe([(r * 0.14, 0), (r * 0.1, h)], x, y, z, 6)
        for i in range(7):
            a = math.tau * i / 7 + 0.3
            tip = (x + math.cos(a) * r * 1.5, y + math.sin(a) * r * 1.5, z + h - r * 0.55)
            B[PALM_C].beam((x, y, z + h + 0.1), tip, (-math.sin(a), math.cos(a), 0), r * 0.42, r * 0.08)
    elif kind == "cypress":
        B[CYPRESS].lathe([(r * 0.45, 0), (r * 0.62, r * 1.2), (r * 0.5, r * 2.8), (0, r * 4.2)], x, y, z + r * 0.2, 6)
    else:
        B[TRUNK].box(x, y, z, r * 0.24, r * 0.24, r * 0.9)
        B[leaf].lathe([(r * 0.55, 0), (r * 0.95, r * 0.35), (r, r * 0.85), (r * 0.7, r * 1.4), (0, r * 1.7)], x, y, z + r * 0.75, 7)


def house_into(B, x, y, w, d, h, z=0.3, color=None, roof=None, i=0):
    c = color or HOUSES[i % len(HOUSES)]
    B[c].box(x, y, z, w, d, h)
    if roof == "tile":
        if w >= d:
            B[TILE].gable_x(y, x - w / 2, x + w / 2, d, z + h, d * 0.3)
        else:
            B[TILE].gable_y(x, y - d / 2, y + d / 2, w, z + h, w * 0.3)
    else:
        B[shade(c, -0.08)].box(x, y, z + h, w, d, 0.5)
        B[shade(c, 0.05)].box(x, y, z + h, w - 1.0, d - 1.0, 0.55)
        B[DARK].box(x, y - d / 2 - 0.02, z, min(w, d) * 0.18, 0.1, h * 0.45)


def portal(name, w, h, loc, face="S", frame=STONE_L, ring=True, pointed=False):
    """A Córdoban portal: a framed (alfiz) panel with a dark horseshoe door and a ring of red-and-white voussoirs."""
    x, y, z = loc
    B = Bufs()
    B[frame].box(0, -0.25, 0, w, 0.5, h)
    B[shade(frame, -0.1)].box(0, -0.52, h * 0.92, w * 1.04, 0.1, h * 0.08)
    dw = w * 0.48
    o = arch_panel(name + "_d", dw, h * 0.62, (0, -0.55, 0), "S", DARK, pointed, 0.2)
    if ring:
        rc = h * 0.62 - dw / 2
        voussoirs(B, "x", 0, -0.6, rc, dw / 2 + 0.02, dw / 2 + w * 0.13, -18, 198, 13, 0.16)
    obj = join([B.join(name + "_f"), o], name)
    return place(obj, FACE_ROT[face], x, y, z)


def oct_pts(r, start=math.pi / 8):
    return [(r * math.cos(start + i * math.pi / 4), r * math.sin(start + i * math.pi / 4)) for i in range(8)]


# ================================================================ the Great Mosque
XW, XP, XE = -65.0, 10.0, 65.0      # west wall, pre-Almanzor east wall, Almanzor's east wall
YN = 31.0                            # the hall's north facade on the court
H = 10.0                             # hall wall height
T = 1.4                              # wall thickness
BAY = 3.0                            # column spacing along the aisles


def _cutaway(B, x_lines, cy0, cy1):
    """The forest of columns: arcade lines along Y at each x, with double arches of red brick and white stone."""
    nb = int(round((cy1 - cy0) / BAY))
    B[PAVE].box2(x_lines[0], cy0, x_lines[-1], cy1, 0.3, 0.42)
    k = 0
    for x in x_lines:
        for i in range(nb + 1):
            y = cy0 + i * BAY
            B[MARBLES[k % len(MARBLES)]].lathe([(0.26, 0.42), (0.22, 3.3)], x, y, 0, 8, math.pi / 8)
            B[STONE_L].box(x, y, 3.3, 0.62, 0.62, 0.4)
            B[STONE].box(x, y, 3.7, 0.62, 0.9, 0.35)
            B[STONE].box(x, y, 4.05, 0.6, 0.7, 2.65)
            k += 1
        for i in range(nb):
            yc = cy0 + (i + 0.5) * BAY
            voussoirs(B, "y", yc, x, 4.35, 1.15, 1.55, -22, 202, 11, 0.6)
            voussoirs(B, "y", yc, x, 6.8, 1.12, 1.52, 0, 180, 9, 0.6)
        B[STONE].box(x, (cy0 + cy1) / 2, 8.3, 0.6, cy1 - cy0 + 0.6, H - 8.3)


def _hall(B, x0, x1, y0, y1, n_aisles, cut, roof_color=TILE, north_open=True):
    """Prayer hall: outer walls, an inner mass, one gable roof per aisle, a cut-away block of arcades."""
    aw = (x1 - x0) / n_aisles
    k0, k1, cy0, cy1 = cut
    cx0, cx1 = x0 + k0 * aw, x0 + k1 * aw
    # outer walls
    B[STONE].box2(x0, y0, x0 + T, y1, 0.3, H)
    B[STONE].box2(x1 - T, y0, x1, y1, 0.3, H)
    B[STONE].box2(x0, y0, x1, y0 + T, 0.3, H)
    B[STONE].box2(x0, y1 - T, x1, y1, 0.3, H)
    # inner mass around the cut
    g = 0.3
    B[HALL].box2(x0 + T, y0 + T, cx0 - g, y1 - T, 0.3, H - 0.1)
    B[HALL].box2(cx1 + g, y0 + T, x1 - T, y1 - T, 0.3, H - 0.1)
    B[HALL].box2(cx0 - g, y0 + T, cx1 + g, cy0 - g, 0.3, H - 0.1)
    B[HALL].box2(cx0 - g, cy1 + g, cx1 + g, y1 - T, 0.3, H - 0.1)
    _cutaway(B, [cx0 + j * aw for j in range(k1 - k0 + 1)], cy0, cy1)
    # roofs: one gable per aisle, split over the cut
    rh = aw * 0.36
    for i in range(n_aisles):
        cx = x0 + (i + 0.5) * aw
        if k0 <= i < k1:
            B[roof_color].gable_y(cx, y0, cy0 - g, aw, H, rh)
            B[roof_color].gable_y(cx, cy1 + g, y1, aw, H, rh)
            B[STONE].tri_y(cx, cy0 - g - 0.2, aw, H, rh, 0.4)
            B[STONE].tri_y(cx, cy1 + g + 0.2, aw, H, rh, 0.4)
        else:
            B[roof_color].gable_y(cx, y0, y1, aw, H, rh)
        B[STONE].tri_y(cx, y0 + 0.2, aw, H, rh, 0.4)
        B[STONE].tri_y(cx, y1 - 0.2, aw, H, rh, 0.4)
    # buttresses: west and east every two bays, south at every aisle line
    for x, s in ((x0, -1), (x1, 1)):
        n = int((y1 - y0) / (2 * BAY))
        for j in range(n + 1):
            y = y0 + 1.2 + j * (y1 - y0 - 2.4) / n
            B[STONE_D].box(x + s * 0.8, y, 0.3, 1.6, 1.5, H + 0.4)
            B[STONE_D].box(x + s * 0.8, y, H + 0.4, 1.0, 1.0, 0.8)
    for i in range(n_aisles + 1):
        x = x0 + 1.0 + i * (x1 - x0 - 2.0) / n_aisles
        B[STONE_D].box(x, y0 - 0.8, 0.3, 1.5, 1.6, H + 0.4)
        B[STONE_D].box(x, y0 - 0.8, H + 0.4, 1.0, 1.0, 0.8)
    stepped_merlons(B[STONE], x0, y0, x1, y1, H, 0.9, 0.9, "SEW")
    # the court facade: an arch per aisle, red and white
    for i in range(n_aisles):
        cx = x0 + (i + 0.5) * aw
        dw = aw * 0.6
        B[DARK].box(cx, y1 + 0.1, 0.3, dw, 0.3, 6.2 - dw / 2 - 0.3)
        voussoirs(B, "x", cx, y1 + 0.15, 6.2 - dw / 2, 0.0001 + dw / 2 * 0.98, dw / 2 + 0.7, -22, 202, 13, 0.35)
        voussoirs(B, "x", cx, y1 + 0.1, 6.2 - dw / 2, 0.001, dw / 2 * 0.98, 0, 180, 6, 0.3, (DARK,))
    # frieze of alternating red and white blocks under the eaves on the court side
    for i in range(int((x1 - x0) / 1.2)):
        B[VR if i % 2 else VW].box(x0 + 0.6 + i * 1.2, y1 + 0.2, H - 1.4, 1.1, 0.3, 0.7)
    return aw


def _court(B, x0, x1, y0, y1, galleries, trees, wall_h=8.5, fountains=2):
    B[PAVE].box2(x0 + T, y0, x1 - T, y1 - T, 0.3, 0.45)
    B[STONE].box2(x0, y0, x0 + T, y1, 0.3, wall_h)
    B[STONE].box2(x1 - T, y0, x1, y1, 0.3, wall_h)
    B[STONE].box2(x0, y1 - T, x1, y1, 0.3, wall_h)
    stepped_merlons(B[STONE], x0, y0, x1, y1, wall_h, 0.9, 0.9, "NEW")
    for x, s in ((x0, -1), (x1, 1)):
        n = max(2, int((y1 - y0) / 9))
        for j in range(n + 1):
            y = y0 + 1.5 + j * (y1 - y0 - 3) / n
            B[STONE_D].box(x + s * 0.8, y, 0.3, 1.6, 1.5, wall_h + 0.3)
    n = max(2, int((x1 - x0) / 9))
    for j in range(n + 1):
        B[STONE_D].box(x0 + 1.5 + j * (x1 - x0 - 3) / n, y1 + 0.8, 0.3, 1.5, 1.6, wall_h + 0.3)
    gd = 6.0 if galleries else 0.0
    if galleries:
        gh = 6.4
        B[HALL].box2(x0 + T, y0 + 0.5, x0 + T + gd, y1 - T, 0.3, gh)
        B[HALL].box2(x1 - T - gd, y0 + 0.5, x1 - T, y1 - T, 0.3, gh)
        B[HALL].box2(x0 + T + gd, y1 - T - gd, x1 - T - gd, y1 - T, 0.3, gh)
        B[TILE].gable_y(x0 + T + gd / 2, y0 + 0.5, y1 - T, gd, gh, 1.4)
        B[TILE].gable_y(x1 - T - gd / 2, y0 + 0.5, y1 - T, gd, gh, 1.4)
        B[TILE].gable_x(y1 - T - gd / 2, x0 + T + gd, x1 - T - gd, gd, gh, 1.4)
        for xs, f in ((x0 + T + gd + 0.05, "E"), (x1 - T - gd - 0.05, "W")):
            L = y1 - T - y0 - 0.5
            nb = int(L / 4.0)
            for j in range(nb):
                y = y0 + 0.5 + (j + 0.5) * L / nb
                B[DARK].box(xs, y, 0.3, 0.2, 2.2, 3.2)
                voussoirs(B, "y", y, xs + (0.12 if f == "E" else -0.12), 3.5, 1.1, 1.45, -15, 195, 9, 0.25)
        L = x1 - x0 - 2 * T - 2 * gd
        nb = int(L / 4.0)
        for j in range(nb):
            x = x0 + T + gd + (j + 0.5) * L / nb
            B[DARK].box(x, y1 - T - gd - 0.05, 0.3, 2.2, 0.2, 3.2)
            voussoirs(B, "x", x, y1 - T - gd - 0.12, 3.5, 1.1, 1.45, -15, 195, 9, 0.25)
    # trees in rows, as the court's trees are lined up with the aisles of the hall
    kind, rows_dx = trees
    ix0, ix1 = x0 + T + gd + 3.0, x1 - T - gd - 3.0
    x = ix0
    col = 0
    while x <= ix1 + 0.01:
        y = y0 + 6.0
        row = 0
        while y <= y1 - T - gd - 4.0:
            k = kind
            if kind == "mixed":
                k = "palm" if (col + row) % 3 == 0 else "round"
            elif kind == "orange":
                k = "cypress" if (col * 7 + row) % 11 == 0 else ("palm" if (col + row) % 9 == 4 else "round")
            if not (abs(x - (x0 + x1) / 2) < 3 and abs(y - (y0 + y1) / 2) < 6):
                tree_into(B, x, y, 0.45, 1.6 if k == "round" else 1.9, k, ORANGE_LEAF if kind == "orange" else LEAF)
            if kind in ("orange", "mixed"):
                B[WATER_C].box(x + rows_dx / 2, y, 0.45, 0.35, 5.4, 0.08)
            y += 6.0
            row += 1
        x += rows_dx
        col += 1
    cxm = (x0 + x1) / 2
    for j in range(fountains):
        fx = cxm + (j - (fountains - 1) / 2) * (x1 - x0) * 0.32
        B[WATER_C].prism([(fx + px, (y0 + y1) / 2 + py) for px, py in oct_pts(2.0)], 1.0, 1.05)
        B[STONE_L].prism([(fx + px, (y0 + y1) / 2 + py) for px, py in oct_pts(2.4)], 0.45, 1.0)


def _minaret_793(B, x, y):
    s, h = 5.6, 19.0
    B[STONE].box(x, y, 0.3, s, s, h)
    stepped_merlons(B[STONE], x - s / 2, y - s / 2, x + s / 2, y + s / 2, h + 0.3, 0.7, 0.5, "SNEW", 0.6)
    for f, (dx, dy) in (("S", (0, -s / 2)), ("N", (0, s / 2)), ("E", (s / 2, 0)), ("W", (-s / 2, 0))):
        B[DARK].box(x + dx * 1.01, y + dy * 1.01, 12.0, 0.9 if f in "SN" else 0.12, 0.12 if f in "SN" else 0.9, 2.2)
    B[STONE_L].box(x, y, h + 0.3, 2.6, 2.6, 3.2)
    B[STONE_L].lathe([(1.5, 0), (1.3, 0.6), (0.6, 1.4), (0, 1.8)], x, y, h + 3.5, 8)


def _minaret_951(B, x, y, top="pommels"):
    """Abd al-Rahman III's minaret: a square stone shaft with twin-arched windows, stepped merlons and a crowning kiosk."""
    s, h = 8.6, 33.0
    B[STONE].box(x, y, 0.3, s, s, h)
    B[STONE_D].box(x, y, h - 0.3, s + 0.5, s + 0.5, 0.6)
    stepped_merlons(B[STONE], x - s / 2, y - s / 2, x + s / 2, y + s / 2, h + 0.3, 0.8, 0.6, "SNEW", 0.7)
    for zz in (11.0, 19.0, 26.0):
        for f in "SNEW":
            for k in (-1, 1):
                ox = k * 1.0
                if f in "SN":
                    px, py = x + ox, y + (s / 2 + 0.02) * (1 if f == "N" else -1)
                    B[STONE_L].box(px, py, zz - 0.4, 2.0 if k < 0 else 2.0, 0.12, 3.8)
                    B[DARK].box(px, py + (0.04 if f == "N" else -0.04), zz, 0.8, 0.14, 2.6)
                    voussoirs(B, "x", px, py + (0.08 if f == "N" else -0.08), zz + 2.6, 0.42, 0.75, -20, 200, 7, 0.1)
                else:
                    px, py = x + (s / 2 + 0.02) * (1 if f == "E" else -1), y + ox
                    B[STONE_L].box(px, py, zz - 0.4, 0.12, 2.0, 3.8)
                    B[DARK].box(px + (0.04 if f == "E" else -0.04), py, zz, 0.14, 0.8, 2.6)
                    voussoirs(B, "y", py, px + (0.08 if f == "E" else -0.08), zz + 2.6, 0.42, 0.75, -20, 200, 7, 0.1)
    k = 4.4
    B[STONE_L].box(x, y, h + 0.3, k, k, 6.5)
    for f, (dx, dy) in (("S", (0, -k / 2)), ("N", (0, k / 2)), ("E", (k / 2, 0)), ("W", (-k / 2, 0))):
        B[DARK].box(x + dx * 1.02, y + dy * 1.02, h + 1.6, 1.4 if f in "SN" else 0.12, 0.12 if f in "SN" else 1.4, 3.4)
    B[STONE_D].box(x, y, h + 6.8, k + 0.6, k + 0.6, 0.5)
    B[STONE_L].lathe([(2.3, 0), (2.1, 0.9), (1.4, 2.0), (0.5, 2.7), (0, 2.9)], x, y, h + 7.3, 10)
    tz = h + 10.2
    if top == "pommels":
        B[BRONZE].box(x, y, tz, 0.18, 0.18, 4.2)
        for i, (r, z, c) in enumerate(((0.75, 0.6, GOLD), (0.62, 1.9, SILVER), (0.5, 3.0, GOLD))):
            B[c].lathe([(0, -r), (r * 0.7, -r * 0.7), (r, 0), (r * 0.7, r * 0.7), (0, r)], x, y, tz + z, 8)
    else:
        B[BRONZE].box(x, y, tz, 0.22, 0.22, 3.2)
        B[BRONZE].box(x, y, tz + 2.0, 1.6, 0.22, 0.22)


def _bell_tower(B, x, y):
    """Hernán Ruiz III's casing of the minaret (from 1593): a rusticated shaft, a belfry and a clock stage."""
    s = 12.0
    B[STONE_L].box(x, y, 0.3, s, s, 35.0)
    for z in range(4, 34, 4):
        B[STONE].box(x, y, z, s + 0.2, s + 0.2, 0.35)
    for zz in (9.0, 18.0, 27.0):
        for f, (dx, dy) in (("S", (0, -s / 2)), ("N", (0, s / 2)), ("E", (s / 2, 0)), ("W", (-s / 2, 0))):
            B[DARK].box(x + dx * 1.01, y + dy * 1.01, zz, 1.4 if f in "SN" else 0.15, 0.15 if f in "SN" else 1.4, 2.6)
    B[STONE].box(x, y, 35.0, s + 1.0, s + 1.0, 0.8)
    b = 9.4
    B[STONE_L].box(x, y, 35.8, b, b, 8.0)
    for f, (dx, dy) in (("S", (0, -b / 2)), ("N", (0, b / 2)), ("E", (b / 2, 0)), ("W", (-b / 2, 0))):
        for k in (-1, 1):
            if f in "SN":
                B[DARK].box(x + k * 2.2, y + dy * 1.01, 37.0, 2.4, 0.15, 3.6)
                B[DARK].lathe([(1.2, 0), (0.85, 0.85), (0, 1.2)], x + k * 2.2, y + dy * 1.01, 40.6, 6)
            else:
                B[DARK].box(x + dx * 1.01, y + k * 2.2, 37.0, 0.15, 2.4, 3.6)
                B[DARK].lathe([(1.2, 0), (0.85, 0.85), (0, 1.2)], x + dx * 1.01, y + k * 2.2, 40.6, 6)
    B[STONE].box(x, y, 43.8, b + 0.8, b + 0.8, 0.6)
    for sx in (-1, 1):
        for sy in (-1, 1):
            B[STONE_L].lathe([(0.45, 0), (0.3, 1.2), (0, 2.4)], x + sx * b / 2, y + sy * b / 2, 44.4, 6)
    c = 6.4
    B[STONE_L].box(x, y, 44.4, c, c, 5.2)
    B[DARK].box(x, y - c / 2 - 0.05, 46.2, 1.6, 0.12, 1.6)
    B[STONE].box(x, y, 49.6, c + 0.5, c + 0.5, 0.5)
    B[STONE_L].lathe([(2.6, 0), (2.4, 1.2), (1.6, 2.6), (0.6, 3.4), (0, 3.6)], x, y, 50.1, 12)
    B[BRONZE].box(x, y, 53.6, 0.3, 0.3, 2.6)


def _cathedral(B, cx, cy):
    """The Renaissance cathedral (1523–1607) rising from the middle of the hall: a Latin cross with a crossing dome."""
    L, W, h = 70.0, 15.0, 27.0
    TL = 46.0
    B[STONE_L].box2(cx - L / 2, cy - W / 2, cx + L / 2, cy + W / 2, 0.3, h)
    B[STONE_L].box2(cx - W / 2, cy - TL / 2, cx + W / 2, cy + TL / 2, 0.3, h)
    B[TILE].gable_x(cy, cx - L / 2, cx + L / 2, W, h, 6.0, 0.4)
    B[TILE].gable_y(cx, cy - TL / 2, cy + TL / 2, W, h, 6.0, 0.4)
    for s in (-1, 1):
        B[STONE_L].tri_y(cx, cy + s * TL / 2, W, h, 6.0, 0.6)
    # end gables of the long arm
    for s in (-1, 1):
        b = len(B[STONE_L].v)
        x = cx + s * L / 2
        B[STONE_L].v += [(x, cy - W / 2, h), (x, cy + W / 2, h), (x, cy, h + 6.0), (x + s * 0.6, cy - W / 2, h), (x + s * 0.6, cy + W / 2, h), (x + s * 0.6, cy, h + 6.0)]
        B[STONE_L].f += [(b, b + 1, b + 2), (b + 5, b + 4, b + 3), (b, b + 3, b + 4, b + 1), (b + 1, b + 4, b + 5, b + 2), (b + 2, b + 5, b + 3, b)]
    # buttresses with pinnacles and tall round-headed windows
    for i in range(9):
        x = cx - L / 2 + 2 + i * (L - 4) / 8
        if abs(x - cx) < W / 2 + 1:
            continue
        for s in (-1, 1):
            B[STONE].box(x, cy + s * (W / 2 + 0.8), 0.3, 1.4, 1.6, h - 1.0)
            B[STONE].lathe([(0.55, 0), (0, 2.6)], x, cy + s * (W / 2 + 0.8), h - 0.7, 4, math.pi / 4)
    for j in range(7):
        y = cy - TL / 2 + 2 + j * (TL - 4) / 6
        if abs(y - cy) < W / 2 + 1:
            continue
        for s in (-1, 1):
            B[STONE].box(cx + s * (W / 2 + 0.8), y, 0.3, 1.6, 1.4, h - 1.0)
            B[STONE].lathe([(0.55, 0), (0, 2.6)], cx + s * (W / 2 + 0.8), y, h - 0.7, 4, math.pi / 4)
    for i in range(8):
        x = cx - L / 2 + 5 + i * (L - 10) / 7
        if abs(x - cx) < W / 2 + 2:
            continue
        for s in (-1, 1):
            B[GLASS].box(x, cy + s * (W / 2 + 0.03), 13.0, 2.2, 0.12, 8.0)
            B[GLASS].lathe([(1.1, 0), (0.78, 0.78), (0, 1.1)], x, cy + s * (W / 2 + 0.03), 21.0, 6)
    for s in (-1, 1):
        voussoirs(B, "x", cx, cy + s * (TL / 2 + 0.12), 18.0, 0.001, 2.6, 0, 360, 12, 0.2, (GLASS,))
        B[DARK].box(cx, cy + s * (TL / 2 + 0.05), 0.3, 4.0, 0.2, 7.0)
    # crossing: an octagonal drum and an oval dome with a lantern
    B[STONE_L].prism([(cx + px, cy + py) for px, py in oct_pts(7.8)], h, h + 4.5)
    for i in range(8):
        a = i * math.pi / 4
        B[GLASS].box(cx + 7.3 * math.cos(a), cy + 7.3 * math.sin(a), h + 1.0, 0.4, 1.8, 2.6, a)
    prof = [(7.4, 0), (7.1, 2.2), (6.1, 4.4), (4.4, 6.2), (2.2, 7.4), (1.2, 7.7)]
    B[TILE_D].lathe(prof, cx, cy, h + 4.5, 16)
    B[STONE_L].lathe([(1.3, 0), (1.3, 2.0), (1.5, 2.1), (0.2, 3.4), (0, 4.0)], cx, cy, h + 12.2, 8)
    for i in range(16):
        a = math.tau * i / 16
        B[STONE_L].box(cx + 8.2 * math.cos(a), cy + 8.2 * math.sin(a), h, 0.5, 0.5, 4.8)
    # Gothic pinnacles at the corners of the crossing (the cathedral mixes Gothic and Renaissance)
    for sx in (-1, 1):
        for sy in (-1, 1):
            B[STONE].lathe([(0.8, 0), (0.8, 3.0), (0, 6.5)], cx + sx * W / 2, cy + sy * W / 2, h, 4, math.pi / 4)


def _houses_fill(B, rects, seed=0):
    """Low patio houses filling parts of the footprint the mosque did not yet cover."""
    i = seed
    for x0, y0, x1, y1 in rects:
        y = y0 + 1.0
        while y < y1 - 5:
            x = x0 + 1.0
            dd = 7.0 + (i * 3) % 5
            while x < x1 - 5:
                ww = 7.0 + (i * 5) % 6
                ww = min(ww, x1 - x - 1.0)
                hh = 3.2 + (i % 3) * 0.8
                dh = min(dd, y1 - y - 1)
                if i % 3 == 2:
                    B[GREEN].box(x + ww / 2, y + dh / 2, 0.3, ww, dh, 0.12)
                    tree_into(B, x + ww / 2, y + dh / 2, 0.42, 1.5, "palm" if i % 2 else "round")
                else:
                    house_into(B, x + ww / 2, y + dh / 2, ww, dh, hh, 0.3, None, "tile" if i % 4 == 0 else None, i)
                x += ww + 3.5
                i += 1
            y += dd + 4.0


def mezquita(variant="950"):
    m = Model("mezquita-" + variant)
    full = variant in ("1300", "1600")
    x1 = XE if full else XP
    y0 = {"786": -6.0, "950": -31.0}.get(variant, -86.5)
    ycn = 62.0 if variant == "786" else 89.0
    n_ai = 19 if full else 11
    cut = {"786": (1, 5, -1.0, 23.0), "950": (1, 5, -25.0, -1.0)}.get(variant, (1, 5, -76.0, -52.0))
    m.add(0, box("mz_ground", 130, 178, 0.3, (0, 0, 0), GROUND), "ground")
    B0, B1, B2 = Bufs(), Bufs(), Bufs()
    # stage 1: the hall and the court
    _hall(B1, XW, x1, y0, YN, n_ai, cut)
    trees = {"786": ("palm", 13.6), "950": ("mixed", 6.82)}.get(variant, ("orange", 6.82))
    _court(B1, XW, x1, YN, ycn, variant != "786", trees, fountains=1 if variant == "786" else (2 if variant == "950" else 3))
    # portals on the long facades
    objs = []
    for j, y in enumerate(range(int(y0 + 9), int(YN - 4), 15)):
        objs.append(portal(f"mz_pw{j}", 5.6, 8.6, (XW - 0.02, y, 0.3), "W"))
    step = 11 if full else 15
    for j, y in enumerate(range(int(y0 + 9), int(YN - 4), step)):
        objs.append(portal(f"mz_pe{j}", 5.6, 8.6, (x1 + 0.02, y, 0.3), "E"))
    objs.append(portal("mz_pn", 5.0, 8.0, (-27.5 + 12, ycn + 0.02, 0.3), "N"))
    m.add(1, join(objs, "mz_portals"), "portals")
    # the qibla wall and its mihrab, pushed out of the south wall
    ax = XW + 5.5 * (XP - XW) / 11          # the axis of the pre-Almanzor mosque
    B1[STONE_D].box(ax, y0 - 1.6, 0.3, 4.6, 3.2, 7.0)
    B1[STONE_D].lathe([(2.3, 0), (2.0, 0.9), (1.0, 1.9), (0, 2.2)], ax, y0 - 1.6, 7.3, 8)
    # outside: houses where the mosque has not yet reached
    if variant == "786":
        _houses_fill(B0, [(13.0, -86.0, 63.0, 86.0), (-63.0, -86.0, 10.0, -10.0), (-63.0, 66.0, 10.0, 87.0)])
    elif variant == "950":
        _houses_fill(B0, [(13.0, -86.0, 63.0, 86.0), (-63.0, -86.0, 10.0, -35.0)], 3)
    m.add(0, B0.join("mz_houses"), "ground")
    # stage 2: minaret, domes, the cathedral
    mx, my = ax, ycn - 4.3
    if variant == "786":
        _minaret_793(B2, ax, ycn - 2.8)
    elif variant == "950":
        _minaret_951(B2, mx, my)
    elif variant == "1300":
        _minaret_951(B2, mx, my, top="cross")
    else:
        _bell_tower(B2, mx, my)
    if full:
        # al-Hakam II's maqsura domes over the mihrab bays and the lantern of the Villaviciosa bay
        for dx, dy, r in ((0, -83.0, 3.2), (-6.8, -83.0, 2.6), (6.8, -83.0, 2.6), (0, -31.0, 3.4)):
            B2[STONE_L].prism([(ax + dx + px, dy + py) for px, py in oct_pts(r + 0.4)], H, H + 3.6)
            B2[TILE_D].lathe([(r, 0), (r * 0.9, r * 0.5), (r * 0.55, r * 0.9), (0, r * 1.05)], ax + dx, dy, H + 3.6, 8)
    if variant == "1600":
        _cathedral(B2, -3.0, -20.0)
    m.add(1, B1.join("mz_hall"), "hall")
    m.add(2, B2.join("mz_tower"), "tower" if variant != "1600" else "cathedral")
    return m


# ================================================================ the river
def roman_bridge():
    m = Model("roman-bridge")
    L, W, dz = 262.0, 9.0, 8.5
    n = 16
    B0, B1 = Bufs(), Bufs()
    B0[STONE_D].box(0, -L / 2 + 6, 0, W + 6, 12, 2.0)
    B0[STONE_D].box(0, L / 2 - 6, 0, W + 6, 12, 2.0)
    B1[STONE].box(0, 0, 0, W, L, dz)
    span = (L - 16) / n
    for i in range(n):
        y = -L / 2 + 8 + span * (i + 0.5)
        aw = span * 0.66
        pointed = i in (3, 4, 9, 13)
        for s in (-1, 1):
            o = arch_panel(f"rb_a{s}{i}", aw, dz * 0.8, (s * (W / 2 + 0.05), y, 0), "E" if s > 0 else "W", "#3C4648", pointed, 0.3)
            m.add(1, o)
            voussoirs(B1, "y", y, s * (W / 2 + 0.1), dz * 0.8 - aw / 2 * (1.1 if pointed else 1.0), aw / 2, aw / 2 + 0.9, 0, 180, 9, 0.25, (STONE_D, STONE))
    for i in range(1, n):
        y = -L / 2 + 8 + span * i
        # upstream (east, +X) cutwaters, downstream (west) square buttresses
        B1[STONE_D].prism([(W / 2, y - 2.0), (W / 2 + 4.0, y), (W / 2, y + 2.0)], 0, dz * 0.62)
        B1[STONE_D].box(-W / 2 - 1.4, y, 0, 2.8, 3.6, dz * 0.62)
    # pyramidal caps on the cutwaters
    for i in range(1, n):
        y = -L / 2 + 8 + span * i
        b = len(B1[STONE].v)
        z0 = dz * 0.62
        B1[STONE].v += [(W / 2, y - 2.0, z0), (W / 2 + 4.0, y, z0), (W / 2, y + 2.0, z0), (W / 2, y, z0 + 2.2)]
        B1[STONE].f += [(b, b + 2, b + 1), (b, b + 1, b + 3), (b + 1, b + 2, b + 3), (b + 2, b, b + 3)]
    for s in (-1, 1):
        B1[STONE_L].box(s * (W / 2 - 0.35), 0, dz, 0.7, L, 1.1)
    B1[PAVE].box(0, 0, dz, W - 1.4, L, 0.12)
    m.add(0, B0.join("rb_ends"), "abutments")
    m.add(1, B1.join("rb_body"), "arches")
    # a few mule carts' worth of traffic markers: low stone benches (guard posts) at the ends
    B2 = Bufs()
    for s in (-1, 1):
        B2[STONE_L].box(-W / 2 + 1.0, s * (L / 2 - 4), dz, 0.8, 0.8, 2.0)
        B2[STONE_L].box(W / 2 - 1.0, s * (L / 2 - 4), dz, 0.8, 0.8, 2.0)
    m.add(2, B2.join("rb_posts"), "parapets")
    return m


def puerta_del_puente(variant="medieval"):
    m = Model("puerta-del-puente-" + variant)
    m.add(0, box("pp_g", 30, 14, 0.3, (0, 0, 0), GROUND), "ground")
    B0, B1 = Bufs(), Bufs()
    # wall stubs to the edges of the footprint
    B0[STONE].box2(-15, -1.5, -7, 1.5, 0.3, 9.0)
    B0[STONE].box2(7, -1.5, 15, 1.5, 0.3, 9.0)
    if variant == "1600":
        B1[STONE_L].box(0, 0, 0.3, 14.0, 5.0, 12.5)
        objs = [arch_panel("pp_a", 5.0, 9.0, (0, -2.55, 0.3), "S", DARK, False, 0.3), arch_panel("pp_b", 5.0, 9.0, (0, 2.55, 0.3), "N", DARK, False, 0.3)]
        for s in (-1, 1):
            for k in (3.6, 5.6):
                for f in (-1, 1):
                    B1[STONE_L].lathe([(0.5, 0), (0.5, 0.6), (0.42, 0.7), (0.38, 8.4), (0.55, 8.6), (0.55, 9.0)], s * k, f * 2.8, 0.3, 10)
        B1[STONE].box(0, 0, 9.3, 15.0, 6.6, 1.0)          # entablature
        B1[STONE_L].box(0, 0, 10.3, 15.2, 6.8, 0.5)
        for i in range(12):
            B1[STONE_D].box(-6.6 + i * 1.2, -3.42, 9.45, 0.5, 0.1, 0.7)
        B1[STONE_L].box(0, 0, 10.8, 11.0, 5.0, 1.7)       # attic
        B1[STONE_D].box(0, -2.55, 11.0, 2.4, 0.2, 1.4)     # the city's arms
        B1[STONE].box(0, 0, 12.5, 11.4, 5.4, 0.4)
        for s in (-1, 1):
            B1[STONE_L].lathe([(0.5, 0), (0.45, 0.8), (0, 1.8)], s * 5.0, -2.2, 12.9, 8)
            B1[STONE_L].lathe([(0.5, 0), (0.45, 0.8), (0, 1.8)], s * 5.0, 2.2, 12.9, 8)
        m.add(1, join(objs + [B1.join("pp_arch")], "pp_arch"), "arch")
    else:
        col = STONE if variant == "medieval" else "#D3C3A1"
        B1[col].box(0, 0, 0.3, 8.0, 10.0, 11.0)
        pointed = variant == "medieval"
        objs = [arch_panel("pp_a", 3.8, 6.8, (0, -5.05, 0.3), "S", DARK, pointed, 0.3), arch_panel("pp_b", 3.8, 6.8, (0, 5.05, 0.3), "N", DARK, pointed, 0.3)]
        if variant == "medieval":
            voussoirs(B1, "x", 0, -5.1, 6.8 - 1.9 * 1.1, 1.95, 2.6, -15, 195, 11, 0.15)
        for s in (-1, 1):
            B1[col].box(s * 5.5, 0, 0.3, 4.4, 8.0, 14.0)
            if variant == "medieval":
                stepped_merlons(B1[col], s * 5.5 - 2.2, -4.0, s * 5.5 + 2.2, 4.0, 14.3, 0.7, 0.5, "SNEW", 0.6)
                B1[DARK].box(s * 5.5, -4.03, 9.0, 0.6, 0.1, 1.6)
            else:
                B1[shade(col, -0.06)].box(s * 5.5, 0, 14.3, 4.8, 8.4, 0.5)
        if variant == "medieval":
            stepped_merlons(B1[col], -3.3, -5.0, 3.3, 5.0, 11.3, 0.7, 0.5, "SN", 0.6)
        else:
            B1[shade(col, -0.06)].box(0, 0, 11.3, 8.4, 10.4, 0.5)
            B1[TILE].gable_x(0, -3.3, 3.3, 9.0, 11.8, 1.6)
        m.add(1, join(objs + [B1.join("pp_gate")], "pp_gate"), "gate")
    stepped_merlons(B0[STONE], -15, -1.5, -7, 1.5, 9.3, 0.7, 0.6, "SN", 0.6)
    stepped_merlons(B0[STONE], 7, -1.5, 15, 1.5, 9.3, 0.7, 0.6, "SN", 0.6)
    m.add(0, B0.join("pp_walls"), "ground")
    return m


def calahorra():
    """Henry II's Calahorra (1369): two rectangular towers joined by a round one, a passage through for the road."""
    m = Model("calahorra")
    m.add(0, box("ca_g", 34, 30, 0.3, (0, 0, 0), GROUND), "ground")
    B1, B2 = Bufs(), Bufs()
    col = "#D2B98E"
    for s in (-1, 1):
        B1[col].box(s * 10.5, 2.0, 0.3, 11.0, 13.0, 19.0)
        stepped_merlons(B2[col], s * 10.5 - 5.5, -4.5, s * 10.5 + 5.5, 8.5, 19.3, 0.8, 0.7, "SNEW", 0.7)
        for zz in (7.0, 13.0):
            B1[DARK].box(s * 10.5, -4.55, zz, 0.9, 0.12, 1.8)
            B1[DARK].box(s * 16.05, 2.0, zz, 0.12, 0.9, 1.8)
    # the central body: a block whose south face is a half-round tower
    B1[col].box(0, 3.0, 0.3, 10.0, 18.0, 16.5)
    B1[col].lathe([(5.0, 0), (5.0, 17.3)], 0, -6.0, 0.3, 20)
    B1[shade(col, -0.05)].lathe([(5.4, 0), (5.4, 0.6)], 0, -6.0, 17.6, 20)
    for i in range(14):
        a = math.tau * i / 14
        B2[col].box(5.0 * math.cos(a), -6.0 + 5.0 * math.sin(a), 18.2, 0.8, 0.8, 1.2, a)
    stepped_merlons(B2[col], -5.0, -6.0, 5.0, 12.0, 16.8, 0.8, 0.7, "NEW", 0.7)
    objs = [arch_panel("ca_pass_s", 3.6, 6.5, (0, -11.05, 0.3), "S", DARK, True, 0.3), arch_panel("ca_pass_n", 3.6, 6.5, (0, 12.05, 0.3), "N", DARK, True, 0.3)]
    B1[STONE_L].box(0, -11.1, 8.0, 2.0, 0.15, 1.2)
    m.add(1, join(objs + [B1.join("ca_body")], "ca_body"), "towers")
    m.add(2, B2.join("ca_top"), "battlements")
    return m


def albolafia(wheel=True):
    m = Model("albolafia" + ("" if wheel else "-1600"))
    B0, B1, B2 = Bufs(), Bufs(), Bufs()
    # the weir (azuda) running out into the river and the mill house on it
    B0[STONE_D].box(0, -6.5, 0, 30.0, 3.0, 1.2)
    B0[STONE_D].box(-6.0, 1.0, 0, 16.0, 14.0, 1.4)
    B1[STONE].box(-7.0, -1.0, 1.4, 11.0, 8.0, 5.2)
    B1[TILE].gable_x(-1.0, -12.5, -1.5, 8.0, 6.6, 2.2)
    for k in (-2, 0, 2):
        B1[DARK].box(-7.0 + k * 2.2, -5.05, 1.4, 1.2, 0.12, 1.8)        # mill races
    B1[DARK].box(-7.0, 3.05, 1.4, 1.2, 0.12, 2.4)
    # the aqueduct on arches toward the Alcázar
    for i in range(4):
        y = 1.0 + i * 2.6
        B1[STONE].box(5.0, y, 1.4, 1.4, 1.0, 8.4 - 1.4)
    B1[STONE].box(5.0, 5.0, 8.4, 1.6, 10.0, 1.0)
    B1[WATER_C].box(5.0, 5.0, 9.4, 0.8, 10.0, 0.06)
    if wheel:
        R, cx, cy, cz = 5.6, 5.0, -2.6, 6.0
        side = (1, 0, 0)
        for i in range(16):
            a = math.tau * i / 16
            b = math.tau * (i + 1) / 16
            p0 = (cx, cy + R * math.cos(a), cz + R * math.sin(a))
            p1 = (cx, cy + R * math.cos(b), cz + R * math.sin(b))
            for dx in (-0.55, 0.55):
                B2[WOOD].beam((p0[0] + dx, p0[1], p0[2]), (p1[0] + dx, p1[1], p1[2]), side, 0.18, 0.35)
            B2[shade(WOOD, -0.25)].box(cx, cy + R * math.cos(a), cz + R * math.sin(a) - 0.25, 1.4, 0.5, 0.5)
            if i % 2 == 0:
                for dx in (-0.55, 0.55):
                    B2[WOOD].beam((cx + dx, cy, cz), (cx + dx, cy + R * math.cos(a), cz + R * math.sin(a)), side, 0.14, 0.2)
        B2[WOOD].beam((cx - 1.6, cy, cz), (cx + 1.6, cy, cz), (0, 1, 0), 0.45, 0.45)
        B2[STONE].box(cx - 1.4, cy, 0, 0.8, 1.2, cz)
        B2[STONE].box(cx + 1.4, cy, 0, 0.8, 1.2, cz)
        B2[WATER_C].box(cx, cy + R - 0.6, cz + 2.8, 0.7, 2.4, 0.06)
    else:
        B2[STONE].box(5.0 - 1.4, -2.6, 0, 0.8, 1.2, 3.0)
        B2[STONE].box(5.0 + 1.4, -2.6, 0, 0.8, 1.2, 3.0)
    m.add(0, B0.join("al_weir"), "weir")
    m.add(1, B1.join("al_mill"), "mill")
    m.add(2, B2.join("al_wheel"), "wheel")
    return m


# ================================================================ palaces and baths
def umayyad_alcazar():
    """An interpretation: a crenellated enclosure with the Bab al-Sudda on the river side, halls round two courts, a garden."""
    m = Model("umayyad-alcazar")
    W, D = 160.0, 140.0
    m.add(0, box("ua_g", W, D, 0.3, (0, 0, 0), GROUND), "ground")
    walls = wall_run("ua_walls", [(-78, -68), (78, -68), (78, 68), (-78, 68), (-78, -68)], 10.0, 2.4, (0, 0, 0.3), STONE, True, 3.2, 26.0, False, "square")
    B0, B1, B2 = Bufs(), Bufs(), Bufs()
    stepped_merlons(B0[STONE], -79.2, -69.2, 79.2, 69.2, 10.3, 0.9, 0.9, "SNEW", 1.0)
    m.add(0, join([walls, B0.join("ua_mer")], "ua_walls"), "walls")
    # Bab al-Sudda on the river side, with a loggia above
    B1[STONE].box(0, -66.5, 0.3, 22.0, 9.0, 13.0)
    objs = [arch_panel("ua_sudda", 6.0, 9.5, (0, -71.05, 0.3), "S", DARK, False, 0.3)]
    voussoirs(B1, "x", 0, -71.1, 9.5 - 3.0, 3.02, 4.2, -18, 198, 15, 0.2)
    B1[STONE_L].box(0, -66.5, 13.3, 18.0, 7.0, 3.6)
    for k in range(-2, 3):
        objs.append(arch_panel(f"ua_log{k}", 2.2, 3.0, (k * 3.4, -70.05, 13.3), "S", DARK, False, 0.2))
    B1[TILE].gable_x(-66.5, -9.0, 9.0, 7.0, 16.9, 2.2)
    # the main court with its halls (east half)
    cx, cy = 28.0, -6.0
    B1[PAVE].box(cx, cy, 0.3, 60.0, 56.0, 0.15)
    for (x, y, w, d, h) in ((cx, cy + 34.0, 64.0, 14.0, 11.0), (cx, cy - 32.0, 64.0, 10.0, 8.0), (cx - 34.0, cy, 10.0, 54.0, 8.0), (cx + 34.0, cy, 10.0, 54.0, 8.0)):
        B1[LIME].box(x, y, 0.3, w, d, h)
        if w > d:
            B1[TILE].gable_x(y, x - w / 2, x + w / 2, d, h + 0.3, d * 0.32)
        else:
            B1[TILE].gable_y(x, y - d / 2, y + d / 2, w, h + 0.3, w * 0.32)
    for k in range(-5, 6):
        objs.append(arch_panel(f"ua_hall{k}", 2.4, 6.0, (cx + k * 5.0, cy + 26.95, 0.3), "S", DARK, False, 0.25))
    voussoirs(B1, "x", cx, cy + 26.9, 6.5, 2.0, 2.9, -18, 198, 13, 0.25)
    B1[WATER_C].box(cx, cy, 0.45, 24.0, 8.0, 0.15)
    for k in (-1, 1):
        tree_into(B1, cx + k * 20.0, cy + 12.0, 0.45, 2.2, "round")
        tree_into(B1, cx + k * 20.0, cy - 12.0, 0.45, 2.2, "palm")
    # a domed audience hall at the head of the court
    B2[LIME].box(cx, cy + 34.0, 11.3, 12.0, 12.0, 4.0)
    B2[TILE_D].lathe([(5.8, 0), (5.2, 2.2), (3.4, 4.2), (0, 5.4)], cx, cy + 34.0, 15.3, 12)
    # the garden (west half)
    B1[GREEN].box(-38.0, -14.0, 0.3, 64.0, 70.0, 0.2)
    for x0, y0, x1, y1 in ((-71.0, -50.0, -5.0, -47.0), (-71.0, 19.0, -5.0, 22.0)):
        B1[STONE_L].box2(x0, y0, x1, y1, 0.3, 4.0)
    B1[PAVE].box(-38.0, -14.0, 0.5, 64.0, 2.0, 0.1)
    B1[PAVE].box(-38.0, -14.0, 0.5, 2.0, 70.0, 0.1)
    B1[WATER_C].box(-38.0, -14.0, 0.62, 62.0, 0.8, 0.06)
    B1[WATER_C].box(-38.0, -14.0, 0.62, 0.8, 68.0, 0.06)
    B1[WATER_C].prism([(-38.0 + px, -14.0 + py) for px, py in oct_pts(4.0)], 0.5, 0.7)
    for i in range(4):
        for j in range(4):
            tx = -38.0 + (i - 1.5) * 15.0
            ty = -14.0 + (j - 1.5) * 16.0
            tree_into(B1, tx, ty, 0.5, 2.6 if (i + j) % 3 else 2.2, "palm" if (i * 3 + j) % 5 == 0 else ("cypress" if (i + j) % 4 == 1 else "round"))
    # north-west service court and a residence block
    B1[LIME].box(-40.0, 46.0, 0.3, 66.0, 34.0, 7.0)
    B1[TILE].gable_x(46.0, -73.0, -7.0, 34.0, 7.3, 4.5)
    # the covered passage (sabat) toward the mosque
    B2[STONE].box(70.0, 48.0, 6.0, 20.0, 5.0, 4.0)
    B2[TILE].gable_x(48.0, 60.0, 80.0, 5.0, 10.0, 1.4)
    B2[STONE].box(79.0, 48.0, 0.3, 2.0, 5.0, 5.8)
    m.add(1, join(objs + [B1.join("ua_inner")], "ua_inner"), "halls")
    m.add(2, B2.join("ua_top"), "domes")
    return m


def alcazar_reyes():
    m = Model("alcazar-reyes")
    W, D = 70.0, 64.0
    m.add(0, box("ar_g", W, D, 0.3, (0, 0, 0), GROUND), "ground")
    col = "#CDB58C"
    B0, B1, B2 = Bufs(), Bufs(), Bufs()
    h = 13.0
    for x0, y0, x1, y1 in ((-29, -26, 29, -23), (-29, 23, 29, 26), (-29, -26, -26, 26), (26, -26, 29, 26)):
        B0[col].box2(x0, y0, x1, y1, 0.3, h)
    box_merlons(B0[col], -29, -26, 29, 26, h + 0.3, 1.0, 1.0, "SNEW", 1.0)
    # inner ranges on the north and east, the Mudéjar court with its pool
    B1[LIME].box2(-26, 12, 26, 23, 0.3, 10.0)
    B1[TILE].gable_x(17.5, -26, 26, 11.0, 10.3, 3.0)
    B1[LIME].box2(14, -23, 26, 12, 0.3, 9.0)
    B1[TILE].gable_y(20.0, -23, 12, 12.0, 9.3, 3.0)
    B1[PAVE].box2(-26, -23, 14, 12, 0.3, 0.45)
    B1[WATER_C].box(-6.0, -5.5, 0.45, 18.0, 4.0, 0.15)
    for k in range(-3, 4):
        B1[DARK].box(-6.0 + k * 5.0, 11.95, 0.3, 2.2, 0.15, 3.6)
    for x in (-20, -12, 4, 10):
        tree_into(B1, x, -16.0, 0.45, 1.6, "round", ORANGE_LEAF)
    objs = []
    # corner towers: Homage (NE), Lions (NW), the round Inquisition (SW), the Dove (SE)
    B2[col].box(27.0, 24.0, 0.3, 13.0, 13.0, 24.0)
    box_merlons(B2[col], 20.5, 17.5, 33.5, 30.5, 24.3, 1.0, 0.9, "SNEW", 0.9)
    B2[col].box(-27.0, 24.0, 0.3, 11.0, 11.0, 20.0)
    box_merlons(B2[col], -32.5, 18.5, -21.5, 29.5, 20.3, 1.0, 0.9, "SNEW", 0.9)
    B2[col].lathe([(6.4, 0), (6.2, 19.0)], -27.0, -24.0, 0.3, 20)
    B2[shade(col, -0.06)].lathe([(6.8, 0), (6.8, 0.8)], -27.0, -24.0, 19.3, 20)
    for i in range(12):
        a = math.tau * i / 12
        B2[col].box(-27.0 + 6.4 * math.cos(a), -24.0 + 6.4 * math.sin(a), 20.1, 1.0, 1.0, 1.2, a)
    B2[col].box(27.0, -24.0, 0.3, 12.0, 12.0, 22.0)
    box_merlons(B2[col], 21.0, -30.0, 33.0, -18.0, 22.3, 1.0, 0.9, "SNEW", 0.9)
    for (x, y) in ((27.0, 24.0), (-27.0, 24.0), (27.0, -24.0)):
        for zz in (8.0, 15.0):
            B2[DARK].box(x, y - 6.6, zz, 1.0, 0.15, 2.2)
    objs.append(arch_panel("ar_gate", 4.0, 7.0, (0, 26.05, 0.3), "N", DARK, True, 0.3))
    B1[col].box(0, 27.0, 0.3, 9.0, 3.0, 14.5)
    box_merlons(B1[col], -4.5, 25.5, 4.5, 28.5, 14.8, 0.9, 0.8, "SNEW", 0.8)
    m.add(0, B0.join("ar_walls"), "walls")
    m.add(1, join(objs + [B1.join("ar_inner")], "ar_inner"), "court")
    m.add(2, B2.join("ar_towers"), "towers")
    return m


def _barrel(Bb, x, y0, y1, w, z, n=8):
    """A half-cylinder vault with its axis along Y."""
    r = w / 2
    for k in range(n):
        a0, a1 = math.pi * k / n, math.pi * (k + 1) / n
        p = [(x + r * math.cos(a0), z + r * math.sin(a0)), (x + r * math.cos(a1), z + r * math.sin(a1))]
        Bb.hexa([(p[0][0], y0, p[0][1]), (p[1][0], y0, p[1][1]), (p[1][0], y1, p[1][1]), (p[0][0], y1, p[0][1]),
                 (p[0][0], y0, p[0][1] + 0.35), (p[1][0], y0, p[1][1] + 0.35), (p[1][0], y1, p[1][1] + 0.35), (p[0][0], y1, p[0][1] + 0.35)])


def _stars(Bb, x, y0, y1, w, z, rows=(-0.5, 0.0, 0.5), every=3.0):
    """Star-shaped skylights on a barrel vault (eight-pointed, drawn as two crossed squares)."""
    r = w / 2
    n = int((y1 - y0) / every)
    for frac in rows:
        a = math.pi / 2 + frac
        px, pz = x + (r + 0.36) * math.cos(a), z + (r + 0.36) * math.sin(a)
        for i in range(n):
            y = y0 + (i + 0.5) * (y1 - y0) / n
            Bb.box(px, y, pz - 0.05, 0.55, 0.55, 0.1)
            Bb.box(px, y, pz - 0.04, 0.55, 0.55, 0.1, math.pi / 4)


def caliphal_baths():
    m = Model("caliphal-baths")
    m.add(0, box("cb_g", 36, 26, 0.3, (0, 0, 0), GROUND), "ground")
    B0, B1, B2 = Bufs(), Bufs(), Bufs()
    # rooms in a row from west (changing hall and court) to east (hot room and furnace)
    rooms = [(-12.0, 9.0, 4.2), (-3.0, 7.0, 4.6), (5.5, 8.0, 5.2), (13.0, 5.0, 4.4)]
    for x, w, h in rooms:
        B0[STONE].box(x, 1.0, 0.3, w, 20.0, h)
        _barrel(B1[STONE_L], x, -9.0, 11.0, w * 0.92, h + 0.3)
        _stars(B2[DARK], x, -9.0, 11.0, w * 0.92, h + 0.3)
    B0[PAVE].box(-12.0, -11.0, 0.3, 12.0, 4.0, 0.15)
    B0[STONE].box(16.0, -10.5, 0.3, 4.0, 4.0, 3.0)                   # furnace
    B2[DARK].lathe([(0.6, 0), (0.5, 3.2)], 16.0, -10.5, 3.3, 8)       # flue
    objs = [arch_panel("cb_door", 2.0, 3.2, (-12.0, -9.05, 0.3), "S", DARK, False, 0.2)]
    voussoirs(B1, "x", -12.0, -9.15, 2.2, 1.0, 1.5, -20, 200, 9, 0.15)
    for x, w, h in rooms[1:]:
        B1[STONE_L].tri_y(x, -9.0, w, h + 0.3, 0.01, 0.1)
    m.add(0, B0.join("cb_walls"), "walls")
    m.add(1, join(objs + [B1.join("cb_vaults")], "cb_vaults"), "vaults")
    m.add(2, B2.join("cb_stars"), "skylights")
    return m


# ================================================================ Roman Corduba
MARBLE_R = "#ECE6DA"


def roman_temple():
    m = Model("roman-temple")
    W, D = 36.0, 64.0
    m.add(0, box("rt_g", W, D, 0.3, (0, 0, 0), PAVE), "precinct")
    B0, B2 = Bufs(), Bufs()
    # porticoes on three sides of the precinct
    for s in (-1, 1):
        x = s * (W / 2 - 2.5)
        B0[STONE_L].box(x + s * 1.8, 2.0, 0.3, 1.2, D - 4.0, 7.0)
        for j in range(14):
            y = -D / 2 + 4.0 + j * (D - 6.0) / 13
            B0[MARBLE_R].lathe([(0.4, 0), (0.34, 5.6)], x - s * 1.4, y, 0.3, 8)
        B0[TILE].gable_y(x, -D / 2 + 3.0, D / 2 - 1.0, 5.0, 6.0, 1.6)
    B0[STONE_L].box(0, D / 2 - 1.0, 0.3, W, 2.0, 7.0)
    base, body, roof = mini_temple("rt", 16.0, 32.0, 3.6, 12.0, 6, 10, (0, 12.0, 0.3), MARBLE_R, TILE)
    m.add(1, join([base, body], "rt_temple"), "temple")
    m.add(2, roof, "roof")
    B0[STONE].box(0, -14.0, 0.3, 4.6, 3.2, 1.8)                       # altar
    for s in (-1, 1):
        B0[STONE_L].box(s * 11.0, -4.0, 0.3, 4.0, 14.0, 0.6)
        B0[WATER_C].box(s * 11.0, -4.0, 0.9, 3.2, 13.2, 0.06)
    for k in (-1, 1):
        B2[STONE_L].box(k * 6.0, -24.0, 0.3, 1.4, 1.4, 2.4)
        B2[BRONZE].lathe([(0.45, 0), (0.4, 1.8), (0.55, 2.2), (0, 2.6)], k * 6.0, -24.0, 2.7, 6)
    m.add(0, B0.join("rt_porticoes"), "precinct")
    m.add(2, B2.join("rt_statues"))
    return m


def roman_theatre():
    m = Model("roman-theatre")
    W, D = 124.0, 72.0
    yc = -24.0                          # stage line: the orchestra's centre
    B0, B1, B2 = Bufs(), Bufs(), Bufs()
    B0[GROUND].box(0, 0, 0, W, D, 0.3)
    tiers = [(10.0, 26.0, 4.0), (26.0, 44.0, 9.5), (44.0, 60.0, 15.0)]
    objs = []
    # rows of seats: thin concentric steps rising outward, a gangway (praecinctio) between the three tiers
    z0 = 0.0
    for i, (r0, r1, h) in enumerate(tiers):
        nrow = int((r1 - r0) / 2.0)
        for j in range(nrow):
            ra, rb = r0 + (r1 - r0) * j / nrow, r1
            hh = z0 + (h - z0) * (j + 1) / nrow
            objs.append(ellipse_ring(f"th_cav{i}_{j}", rb, rb, ra / rb, hh, (0, yc, 0.3), STONE_L if (j % 2) else STONE, n=36, arc=math.pi, start=0.0))
        z0 = h + 0.6
    m.add(0, join(objs, "th_cavea"), "cavea")
    # stairs radiating up the cavea and the praecinctiones
    for k in range(1, 8):
        a = math.pi * k / 8
        for (r0, r1, h), zs in zip(tiers, (0.0, 4.6, 10.1)):
            p0 = (r0 * math.cos(a), yc + r0 * math.sin(a), zs + (h - zs) / int((r1 - r0) / 2.0) + 0.32)
            p1 = (r1 * math.cos(a), yc + r1 * math.sin(a), h + 0.32)
            B1[STONE_D].beam(p0, p1, (-math.sin(a), math.cos(a), 0), 1.0, 0.1)
    # outer arcade on the top wall
    for k in range(18):
        a = math.pi * (k + 0.5) / 18
        o = arch_panel(f"th_out{k}", 4.0, 7.5, (0, 0, 0), "S", DARK, False, 0.4)
        o = rot(o, math.degrees(a) + 90)
        objs2 = move(o, 60.05 * math.cos(a), yc + 60.05 * math.sin(a), 6.0)
        m.add(1, objs2)
    # orchestra, stage and scaenae frons
    B1[MARBLE_R].lathe([(10.0, 0), (10.0, 0.25)], 0, yc, 0.3, 24)
    B1[STONE_L].box(0, yc - 4.0, 0.3, 64.0, 8.0, 1.6)
    B1[STONE_L].box(0, yc - 10.5, 0.3, 70.0, 5.0, 17.0)
    for side in (-1, 1):
        B1[STONE].box(side * 40.0, yc - 6.0, 0.3, 10.0, 14.0, 15.0)
    for lvl, z in enumerate((1.9, 9.6)):
        for k in range(-7, 8):
            B2[MARBLE_R].lathe([(0.45, 0), (0.38, 6.6)], k * 4.2, yc - 7.6, z, 8)
        B2[STONE_L].box(0, yc - 7.6, z + 6.6, 64.0, 1.4, 0.9)
    for k in (-1, 0, 1):
        objs3 = arch_panel(f"th_valva{k}", 4.4 if k == 0 else 3.2, 7.0 if k == 0 else 5.6, (k * 14.0, yc - 7.95, 1.9), "N", DARK, False, 0.2)
        m.add(1, objs3)
    B2[TILE].gable_x(yc - 10.5, -35.0, 35.0, 5.0, 17.3, 1.8)
    m.add(0, B0.join("th_ground"), "cavea")
    m.add(1, B1.join("th_stage"), "stage")
    m.add(2, B2.join("th_frons"), "scaenae frons")
    return m


def roman_forum():
    m = Model("roman-forum")
    W, D = 90.0, 100.0
    B0, B1, B2 = Bufs(), Bufs(), Bufs()
    B0[PAVE].box(0, 0, 0, W, D, 0.35)
    B0[MARBLE_R].box(0, -8.0, 0.35, 56.0, 54.0, 0.1)
    # porticoes east and west
    for s in (-1, 1):
        x = s * (W / 2 - 6.0)
        B1[STONE_L].box(x + s * 4.0, -2.0, 0.35, 2.0, 70.0, 8.0)
        for j in range(16):
            B1[MARBLE_R].lathe([(0.45, 0), (0.38, 6.8)], x - s * 3.0, -36.0 + j * 4.6, 0.35, 8)
        B1[STONE_L].box(x, -2.0, 7.15, 8.0, 70.0, 0.6)
        B2[TILE].gable_y(x, -37.0, 33.0, 9.0, 7.75, 2.0)
        for j in range(6):
            B1[DARK].box(x + s * 2.95, -30.0 + j * 11.0, 0.35, 0.12, 3.0, 3.6)   # shops (tabernae)
    # the basilica along the south side
    B1[STONE_L].box(0, -44.0, 0.35, 74.0, 12.0, 11.0)
    B2[TILE].gable_x(-44.0, -37.0, 37.0, 12.0, 11.35, 3.6)
    for k in range(-8, 9):
        B1[MARBLE_R].lathe([(0.45, 0), (0.38, 7.0)], k * 4.3, -37.4, 0.35, 8)
    B1[STONE_L].box(0, -37.4, 7.35, 74.0, 1.2, 0.8)
    # the temple at the head of the square
    base, body, roof = mini_temple("rf_t", 18.0, 28.0, 3.4, 11.0, 6, 8, (0, 34.0, 0.35), MARBLE_R, TILE)
    m.add(1, join([base, body], "rf_temple"))
    m.add(2, roof)
    # statues on inscribed bases, and the curia beside the temple
    for k in range(-3, 4):
        for row in (-22.0, 6.0):
            B2[STONE_L].box(k * 7.0, row, 0.35, 1.2, 1.6, 1.8)
            B2[BRONZE if k % 2 else MARBLE_R].lathe([(0.35, 0), (0.32, 1.5), (0.4, 1.8), (0, 2.2)], k * 7.0, row, 2.15, 6)
    B1[STONE_L].box(-30.0, 38.0, 0.35, 14.0, 18.0, 9.0)
    B2[TILE].gable_y(-30.0, 29.0, 47.0, 14.0, 9.35, 3.4)
    B1[STONE_L].box(30.0, 38.0, 0.35, 14.0, 18.0, 9.0)
    B2[TILE].gable_y(30.0, 29.0, 47.0, 14.0, 9.35, 3.4)
    m.add(0, B0.join("rf_pave"), "square")
    m.add(1, B1.join("rf_porticoes"), "porticoes")
    m.add(2, B2.join("rf_roofs"), "roofs")
    return m


def roman_mausoleum():
    m = Model("roman-mausoleum")
    B0, B1, B2 = Bufs(), Bufs(), Bufs()
    B0[GROUND].box(0, 0, 0, 16.0, 16.0, 0.3)
    B0[STONE_D].lathe([(7.6, 0), (7.6, 0.6), (7.1, 0.6), (7.1, 1.2), (6.6, 1.2), (6.6, 1.8)], 0, 0, 0.3, 32)
    B1[STONE_L].lathe([(6.2, 0), (6.2, 7.0)], 0, 0, 2.1, 40)
    for zz in (3.5, 4.9, 6.3, 7.7):
        B1[STONE].lathe([(6.24, 0), (6.24, 0.08)], 0, 0, zz, 40)
    for i in range(16):
        a = math.tau * i / 16
        B1[STONE].box(6.25 * math.cos(a), 6.25 * math.sin(a), 2.1, 0.7, 0.7, 6.4, a)
    B1[STONE].lathe([(6.3, 0), (6.9, 0.5), (6.9, 0.9), (6.4, 1.1)], 0, 0, 9.1, 40)
    B2[TILE].lathe([(6.5, 0), (4.6, 1.6), (2.0, 3.3), (0.6, 4.1), (0, 4.3)], 0, 0, 10.2, 32)
    B2[STONE_L].lathe([(0.6, 0), (0.75, 0.6), (0.55, 1.4), (0, 1.9)], 0, 0, 14.4, 10)
    o = arch_panel("rm_door", 1.6, 2.6, (0, -6.25, 2.1), "S", DARK, False, 0.2)
    m.add(0, B0.join("rm_base"), "base")
    m.add(1, join([o, B1.join("rm_drum")], "rm_drum"), "drum")
    m.add(2, B2.join("rm_roof"), "roof")
    return m


# ================================================================ walls and gates
def puerta_almodovar():
    m = Model("puerta-almodovar")
    W, D = 60.0, 20.0
    m.add(0, box("pa_g", W, D, 0.3, (0, 0, 0), GROUND), "ground")
    col = "#CFB58A"
    B0, B1, B2 = Bufs(), Bufs(), Bufs()
    B0[col].box2(-30, 1.5, -5, 4.5, 0.3, 10.0)
    B0[col].box2(5, 1.5, 30, 4.5, 0.3, 10.0)
    box_merlons(B0[col], -30, 1.5, -5, 4.5, 10.3, 1.0, 1.0, "SN", 0.8)
    box_merlons(B0[col], 5, 1.5, 30, 4.5, 10.3, 1.0, 1.0, "SN", 0.8)
    for x in (-25.0, 22.0):
        B1[shade(col, -0.04)].box(x, 1.0, 0.3, 6.0, 7.0, 12.0)
        box_merlons(B1[col], x - 3, -2.5, x + 3, 4.5, 12.3, 0.9, 0.8, "SNEW", 0.8)
    B1[col].box(0, 2.0, 0.3, 4.0, 7.0, 11.0)
    for s in (-1, 1):
        B1[col].box(s * 4.5, 1.0, 0.3, 6.0, 10.0, 15.0)
        box_merlons(B1[col], s * 4.5 - 3, -4.0, s * 4.5 + 3, 6.0, 15.3, 0.9, 0.8, "SNEW", 0.8)
        B1[DARK].box(s * 4.5, -4.05, 10.0, 0.7, 0.12, 1.8)
    box_merlons(B1[col], -1.5, -1.5, 1.5, 5.5, 11.3, 0.8, 0.7, "SN", 0.7)
    objs = [arch_panel("pa_gate_s", 3.2, 7.0, (0, -1.55, 0.3), "S", DARK, True, 0.3), arch_panel("pa_gate_n", 3.2, 7.0, (0, 5.55, 0.3), "N", DARK, True, 0.3)]
    B2[STONE_L].box(0, -1.6, 7.6, 3.6, 0.15, 1.6)
    # the dry moat in front of the wall
    B0["#B7A07A"].box(0, -6.5, 0.3, 60.0, 5.0, 0.05)
    m.add(0, B0.join("pa_wall"), "wall")
    m.add(1, join(objs + [B1.join("pa_towers")], "pa_towers"), "towers")
    m.add(2, B2.join("pa_shield"))
    return m


def puerta_sevilla():
    m = Model("puerta-sevilla")
    m.add(0, box("ps_g", 36, 16, 0.3, (0, 0, 0), GROUND), "ground")
    col = "#CDB386"
    B0, B1 = Bufs(), Bufs()
    B0[col].box2(-18, -1.5, -4, 1.5, 0.3, 8.0)
    B0[col].box2(9, -1.5, 18, 1.5, 0.3, 8.0)
    box_merlons(B0[col], -18, -1.5, -4, 1.5, 8.3, 0.9, 0.9, "SN", 0.7)
    box_merlons(B0[col], 9, -1.5, 18, 1.5, 8.3, 0.9, 0.9, "SN", 0.7)
    B1[col].box2(-4, -2.0, 9, 2.0, 0.3, 9.0)
    B1[col].box(12.0, 0, 0.3, 6.5, 6.5, 12.5)
    box_merlons(B1[col], 8.75, -3.25, 15.25, 3.25, 12.8, 0.9, 0.8, "SNEW", 0.8)
    box_merlons(B1[col], -4, -2.0, 9, 2.0, 9.3, 0.9, 0.9, "SN", 0.7)
    objs = []
    for k, (x, pointed) in enumerate(((-0.5, False), (5.0, False))):
        objs.append(arch_panel(f"ps_a{k}", 3.2, 5.8, (x, -2.05, 0.3), "S", DARK, pointed, 0.3))
        objs.append(arch_panel(f"ps_b{k}", 3.2, 5.8, (x, 2.05, 0.3), "N", DARK, pointed, 0.3))
        voussoirs(B1, "x", x, -2.1, 5.8 - 1.6, 1.62, 2.2, -20 if k else 0, 200 if k else 180, 9, 0.15, (STONE_L, col))
    m.add(0, B0.join("ps_wall"), "wall")
    m.add(1, join(objs + [B1.join("ps_gate")], "ps_gate"), "gate")
    return m


def malmuerta():
    m = Model("malmuerta")
    m.add(0, box("mm_g", 18, 34, 0.3, (0, 0, 0), GROUND), "ground")
    col = "#CBB085"
    B0, B1, B2 = Bufs(), Bufs(), Bufs()
    # the city wall (south) and the free-standing octagonal tower (north), joined by an arch
    B0[col].box2(-9, -17, 9, -13, 0.3, 10.0)
    box_merlons(B0[col], -9, -17, 9, -13, 10.3, 0.9, 0.9, "SN", 0.8)
    ty = 8.0
    B1[col].prism([(px, ty + py) for px, py in oct_pts(6.4)], 0.3, 22.0)
    B1[shade(col, -0.06)].prism([(px, ty + py) for px, py in oct_pts(6.9)], 22.0, 22.8)
    for i in range(8):
        a = math.pi / 8 + i * math.pi / 4 + math.pi / 8
        B2[col].box(6.5 * math.cos(a), ty + 6.5 * math.sin(a), 22.8, 1.4, 1.0, 1.4, a + math.pi / 2)
    for zz in (8.0, 15.0):
        for i in (1, 3, 5, 7):
            a = i * math.pi / 4
            B1[DARK].box(6.0 * math.cos(a), ty + 6.0 * math.sin(a), zz, 1.0, 1.0, 1.8, a)
    # the bridge-arch
    B1[col].box(0, -5.5, 8.0, 4.2, 15.0, 5.0)
    B1[DARK].box(0, -5.5, 0.3, 3.0, 11.0, 7.0)
    box_merlons(B1[col], -2.1, -13.0, 2.1, 2.0, 13.0, 0.7, 0.8, "EW", 0.6)
    B2[STONE_L].box(0, ty - 6.6, 11.0, 2.0, 0.2, 2.6)                 # inscription panel
    m.add(0, B0.join("mm_wall"), "wall")
    m.add(1, B1.join("mm_tower"), "tower")
    m.add(2, B2.join("mm_top"), "battlements")
    return m


# ================================================================ Castilian Córdoba
def synagogue():
    m = Model("synagogue")
    m.add(0, box("sy_g", 20, 26, 0.3, (0, 0, 0), GROUND), "ground")
    B0, B1, B2 = Bufs(), Bufs(), Bufs()
    # the entrance court on the street (south), vestibule with the women's gallery, the square prayer hall
    B0[PAVE].box(0, -8.0, 0.3, 12.0, 8.0, 0.12)
    B0[LIME].box2(-6, -12.5, 6, -11.7, 0.3, 3.6)
    B0[DARK].box(0, -12.55, 0.3, 1.6, 0.1, 2.6)
    B1[LIME].box(0, -1.5, 0.3, 9.0, 5.0, 8.5)
    B1[TILE].gable_x(-1.5, -4.5, 4.5, 5.0, 8.8, 1.6)
    B1[LIME].box(0, 6.0, 0.3, 9.0, 9.0, 10.5)
    B1[DARK].box(0, -4.05, 0.3, 1.4, 0.1, 2.6)
    for x in (-2.5, 0, 2.5):
        B1[DARK].box(x, -4.05, 5.6, 0.7, 0.1, 1.4)                    # gallery windows
    for x in (-2.6, 2.6):
        B1[DARK].box(x, 10.55, 7.4, 0.8, 0.1, 1.8)
    roof = hip_roof("sy_roof", 9.0, 9.0, 3.2, (0, 6.0, 10.8), TILE, ridge=0.0, overhang=0.4)
    # neighbouring houses of the Judería round it
    for i, (x, y, w, d, h) in enumerate(((-8.0, 6.0, 4.0, 12.0, 6.5), (8.0, 4.0, 4.0, 16.0, 7.0), (-8.0, -6.0, 4.0, 10.0, 5.5), (8.0, -8.0, 4.0, 8.0, 6.0), (0, 11.8, 12.0, 2.4, 5.5))):
        house_into(B0, x, y, w, d, h, 0.3, None, "tile", i)
    tree_into(B0, -3.5, -9.0, 0.42, 1.0, "round", ORANGE_LEAF)
    m.add(0, B0.join("sy_houses"), "houses")
    m.add(1, B1.join("sy_hall"), "hall")
    m.add(2, roof, "roof")
    return m


def _church(name, L, nave_w, aisle_w, nave_h, aisle_h, x0=0.0, y0=0.0, col=STONE, rose_r=0.0, apses=3, porch=False):
    """A Fernandine church along X: west front at -X, three polygonal apses at +X, buttresses, a rose window."""
    B = Bufs()
    xa, xb = x0 - L / 2, x0 + L / 2
    B[col].box2(xa, y0 - nave_w / 2, xb, y0 + nave_w / 2, 0.3, nave_h)
    B[TILE].gable_x(y0, xa, xb, nave_w, nave_h, nave_w * 0.32, 0.3)
    for s in (-1, 1):
        yc = y0 + s * (nave_w / 2 + aisle_w / 2)
        B[col].box2(xa, yc - aisle_w / 2, xb - 2.0, yc + aisle_w / 2, 0.3, aisle_h)
        # lean-to roof
        hi, lo = y0 + s * nave_w / 2, y0 + s * (nave_w / 2 + aisle_w + 0.3)
        b = len(B[TILE].v)
        B[TILE].v += [(xa, hi, aisle_h + 2.2), (xa, lo, aisle_h), (xb - 2.0, lo, aisle_h), (xb - 2.0, hi, aisle_h + 2.2), (xa, hi, aisle_h), (xb - 2.0, hi, aisle_h)]
        B[TILE].f += [(b, b + 1, b + 2, b + 3), (b + 4, b + 1, b), (b + 5, b + 3, b + 2), (b + 4, b + 5, b + 2, b + 1), (b, b + 3, b + 5, b + 4)]
        n = max(3, int(L / 6.5))
        for i in range(n + 1):
            x = xa + 1.0 + i * (L - 4.0) / n
            B[shade(col, -0.07)].box(x, y0 + s * (nave_w / 2 + aisle_w + 0.7), 0.3, 1.2, 1.4, aisle_h + 1.0)
            if i < n:
                xm = x + (L - 4.0) / n / 2
                B[GLASS].box(xm, y0 + s * (nave_w / 2 + 0.03), aisle_h + 1.6, 0.9, 0.1, (nave_h - aisle_h) * 0.5)
                B[DARK].box(xm, y0 + s * (nave_w / 2 + aisle_w + 0.03), aisle_h * 0.35, 0.8, 0.1, aisle_h * 0.4)
    # apses: a big polygonal one on the nave, smaller ones on the aisles
    for k, (yc, r, h) in enumerate([(y0, nave_w / 2, nave_h)] + ([(y0 - nave_w / 2 - aisle_w / 2, aisle_w / 2, aisle_h), (y0 + nave_w / 2 + aisle_w / 2, aisle_w / 2, aisle_h)] if apses == 3 else [])):
        xc = xb if k == 0 else xb - 2.0
        pts = [(xc + r * math.cos(a), yc + r * math.sin(a)) for a in [-math.pi / 2 + math.pi * i / 4 for i in range(5)]]
        B[col].prism(pts, 0.3, h)
        B[TILE].lathe([(r * 1.04, 0), (0, r * 0.6)], xc, yc, h, 8, -math.pi / 2)
        for i in range(1, 4):
            a = -math.pi / 2 + math.pi * i / 4 + math.pi / 8
            B[GLASS].box(xc + (r - 0.1) * math.cos(a), yc + (r - 0.1) * math.sin(a), h * 0.4, 0.4, 0.6, h * 0.4, a)
    # west front
    B[col].box(xa - 0.4, y0, 0.3, 0.8, nave_w + 2 * aisle_w, nave_h * 0.75)
    gw = len(B[col].v)
    B[col].v += [(xa - 0.8, y0 - nave_w / 2, nave_h), (xa - 0.8, y0 + nave_w / 2, nave_h), (xa - 0.8, y0, nave_h + nave_w * 0.32),
                 (xa, y0 - nave_w / 2, nave_h), (xa, y0 + nave_w / 2, nave_h), (xa, y0, nave_h + nave_w * 0.32)]
    B[col].f += [(gw, gw + 1, gw + 2), (gw + 5, gw + 4, gw + 3), (gw, gw + 3, gw + 4, gw + 1), (gw + 1, gw + 4, gw + 5, gw + 2), (gw + 2, gw + 5, gw + 3, gw)]
    objs = [B.join(name + "_body")]
    if rose_r:
        r = cylinder(name + "_rose_f", rose_r + 0.5, 0.4, (0, 0, -0.2), shade(col, -0.12), verts=24)
        r = place_x(r, xa - 0.85, y0, nave_h * 0.66)
        g = cylinder(name + "_rose_g", rose_r, 0.4, (0, 0, -0.2), GLASS, verts=24)
        g = place_x(g, xa - 0.95, y0, nave_h * 0.66)
        c = cylinder(name + "_rose_c", rose_r * 0.25, 0.4, (0, 0, -0.2), shade(col, -0.12), verts=12)
        c = place_x(c, xa - 1.05, y0, nave_h * 0.66)
        objs += [r, g, c]
    if porch:
        P = Bufs()
        pw = nave_w + 2 * aisle_w
        P[col].box(xa - 2.8, y0, 0.3, 4.0, pw, 7.0)
        b = len(P[TILE].v)
        P[TILE].v += [(xa - 4.9, y0 - pw / 2, 7.3), (xa - 4.9, y0 + pw / 2, 7.3), (xa - 0.8, y0 + pw / 2, 8.8), (xa - 0.8, y0 - pw / 2, 8.8)]
        P[TILE].f += [(b, b + 1, b + 2, b + 3)]
        P[TILE].v += [(xa - 4.9, y0 - pw / 2, 7.2), (xa - 4.9, y0 + pw / 2, 7.2), (xa - 0.8, y0 + pw / 2, 8.7), (xa - 0.8, y0 - pw / 2, 8.7)]
        P[TILE].f += [(b + 7, b + 6, b + 5, b + 4)]
        objs.append(P.join(name + "_porch"))
        for k in (-1, 0, 1):
            objs.append(place(arch_panel(f"{name}_pa{k}", pw * 0.22, 5.4, (0, 0, 0), "S", DARK, True, 0.3), -90, xa - 4.85, y0 + k * pw * 0.3, 0.3))
    else:
        objs.append(place(arch_panel(name + "_door", nave_w * 0.32, nave_h * 0.42, (0, 0, 0), "S", DARK, True, 0.4), -90, xa - 0.85, y0, 0.3))
    return join(objs, name)


def place_x(o, x, y, z):
    """Stand a disc (built flat) up to face -X, then move it."""
    o.rotation_euler[1] += math.pi / 2
    bpy.ops.object.select_all(action="DESELECT")
    o.select_set(True)
    bpy.context.view_layer.objects.active = o
    bpy.ops.object.transform_apply(rotation=True)
    return move(o, x, y, z)


def _church_tower(name, x, y, w, h, col, top="plain"):
    B = Bufs()
    B[col].box(x, y, 0.3, w, w, h)
    for f, (dx, dy) in (("S", (0, -w / 2)), ("N", (0, w / 2)), ("E", (w / 2, 0)), ("W", (-w / 2, 0))):
        B[DARK].box(x + dx * 1.02, y + dy * 1.02, h - 4.5, 1.2 if f in "SN" else 0.12, 0.12 if f in "SN" else 1.2, 2.8)
    if top == "plain":
        box_merlons(B[col], x - w / 2, y - w / 2, x + w / 2, y + w / 2, h + 0.3, 0.8, 0.7, "SNEW", 0.6)
        B[TILE].lathe([(w * 0.5, 0), (0, w * 0.45)], x, y, h + 0.3, 4, math.pi / 4)
    else:
        b = w * 0.82
        B[STONE_L].box(x, y, h + 0.3, w + 0.5, w + 0.5, 0.5)
        B[STONE_L].box(x, y, h + 0.8, b, b, 5.5)
        for f, (dx, dy) in (("S", (0, -b / 2)), ("N", (0, b / 2)), ("E", (b / 2, 0)), ("W", (-b / 2, 0))):
            B[DARK].box(x + dx * 1.02, y + dy * 1.02, h + 1.6, 1.4 if f in "SN" else 0.12, 0.12 if f in "SN" else 1.4, 2.8)
            B[DARK].lathe([(0.7, 0), (0.5, 0.5), (0, 0.7)], x + dx * 1.02, y + dy * 1.02, h + 4.4, 6)
        B[STONE_L].box(x, y, h + 6.3, b + 0.5, b + 0.5, 0.4)
        B[STONE_L].box(x, y, h + 6.7, b * 0.6, b * 0.6, 2.4)
        B[TILE_D].lathe([(b * 0.36, 0), (b * 0.3, 0.9), (b * 0.15, 1.8), (0, 2.2)], x, y, h + 9.1, 8)
        B[BRONZE].box(x, y, h + 11.3, 0.2, 0.2, 1.6)
    return B.join(name)


def san_pablo():
    m = Model("san-pablo")
    m.add(0, box("sp_g", 70, 34, 0.3, (0, 0, 0), GROUND), "ground")
    body = _church("sp", 56.0, 10.0, 6.5, 17.0, 10.0, x0=-2.0, y0=-4.0, col=STONE, rose_r=0.0, apses=3)
    m.add(1, body, "church")
    m.add(2, _church_tower("sp_tower", -26.0, 11.0, 6.0, 24.0, STONE), "tower")
    # the cloister walk on the north side
    B = Bufs()
    B[LIME].box2(-18, 8.5, 26, 16.5, 0.3, 6.0)
    B[TILE].gable_x(12.5, -18, 26, 8.0, 6.3, 2.0)
    for k in range(10):
        B[DARK].box(-15.0 + k * 4.4, 8.45, 0.3, 2.0, 0.1, 3.4)
    m.add(1, B.join("sp_cloister"))
    return m


def san_lorenzo(variant="1300"):
    m = Model("san-lorenzo-" + variant)
    m.add(0, box("sl_g", 44, 26, 0.3, (0, 0, 0), GROUND), "ground")
    body = _church("sl", 32.0, 9.0, 6.0, 15.0, 9.0, x0=0.2, y0=0.0, col="#D1B98F", rose_r=2.6, apses=3, porch=True)
    m.add(1, body, "church")
    m.add(2, _church_tower("sl_tower", -12.0, 10.0, 5.6, 20.0 if variant == "1300" else 21.0, "#D1B98F", "plain" if variant == "1300" else "renaissance"), "tower")
    return m


def minaret_san_juan():
    m = Model("minaret-san-juan")
    B0, B1, B2 = Bufs(), Bufs(), Bufs()
    B0[GROUND].box(0, 0, 0, 6.0, 6.0, 0.3)
    s, h = 3.6, 12.5
    B1[STONE].box(0, 0, 0.3, s + 0.4, s + 0.4, 1.0)
    B1[STONE].box(0, 0, 1.3, s, s, h - 1.0)
    for z in (3.0, 5.0, 7.0):
        B1[STONE_D].box(0, 0, z, s + 0.06, s + 0.06, 0.12)
    for f in "SNEW":
        for k in (-1, 1):
            u = k * 0.55
            if f in "SN":
                py = (s / 2 + 0.03) * (1 if f == "N" else -1)
                B1[STONE_L].box(0, py, 8.5, 2.5, 0.08, 3.0)
                B1[DARK].box(u, py * 1.01, 8.8, 0.7, 0.08, 1.5)
                voussoirs(B1, "x", u, py * 1.02, 10.3, 0.36, 0.55, -25, 205, 7, 0.06)
            else:
                px = (s / 2 + 0.03) * (1 if f == "E" else -1)
                B1[STONE_L].box(px, 0, 8.5, 0.08, 2.5, 3.0)
                B1[DARK].box(px * 1.01, u, 8.8, 0.08, 0.7, 1.5)
                voussoirs(B1, "y", u, px * 1.02, 10.3, 0.36, 0.55, -25, 205, 7, 0.06)
        if f in "SN":
            B1[MARBLES[1]].box(0, (s / 2 + 0.05) * (1 if f == "N" else -1), 8.8, 0.16, 0.12, 1.5)
        else:
            B1[MARBLES[1]].box((s / 2 + 0.05) * (1 if f == "E" else -1), 0, 8.8, 0.12, 0.16, 1.5)
    stepped_merlons(B2[STONE], -s / 2, -s / 2, s / 2, s / 2, h + 0.3, 0.5, 0.35, "SNEW", 0.4)
    B2[STONE_L].box(0, 0, h + 0.3, 1.8, 1.8, 2.0)
    B2[STONE_L].lathe([(1.0, 0), (0.85, 0.5), (0.4, 1.0), (0, 1.15)], 0, 0, h + 2.3, 8)
    B2[GOLD].lathe([(0, 0), (0.25, 0.25), (0, 0.5)], 0, 0, h + 3.5, 6)
    m.add(0, B0.join("sj_g"), "base")
    m.add(1, B1.join("sj_shaft"), "shaft")
    m.add(2, B2.join("sj_top"), "top")
    return m


BUILDERS = {
    "cordoba/mezquita": lambda: mezquita("950"),
    "cordoba/mezquita-786": lambda: mezquita("786"),
    "cordoba/mezquita-1300": lambda: mezquita("1300"),
    "cordoba/mezquita-1600": lambda: mezquita("1600"),
    "cordoba/roman-bridge": roman_bridge,
    "cordoba/puerta-del-puente": lambda: puerta_del_puente("medieval"),
    "cordoba/puerta-del-puente-roman": lambda: puerta_del_puente("roman"),
    "cordoba/puerta-del-puente-1600": lambda: puerta_del_puente("1600"),
    "cordoba/calahorra": calahorra,
    "cordoba/albolafia": lambda: albolafia(True),
    "cordoba/albolafia-1600": lambda: albolafia(False),
    "cordoba/umayyad-alcazar": umayyad_alcazar,
    "cordoba/alcazar-reyes": alcazar_reyes,
    "cordoba/caliphal-baths": caliphal_baths,
    "cordoba/roman-temple": roman_temple,
    "cordoba/roman-theatre": roman_theatre,
    "cordoba/roman-forum": roman_forum,
    "cordoba/roman-mausoleum": roman_mausoleum,
    "cordoba/puerta-almodovar": puerta_almodovar,
    "cordoba/puerta-sevilla": puerta_sevilla,
    "cordoba/malmuerta": malmuerta,
    "cordoba/synagogue": synagogue,
    "cordoba/san-pablo": san_pablo,
    "cordoba/san-lorenzo": lambda: san_lorenzo("1300"),
    "cordoba/san-lorenzo-1600": lambda: san_lorenzo("1600"),
    "cordoba/minaret-san-juan": minaret_san_juan,
}
