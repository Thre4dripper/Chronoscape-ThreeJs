"""Mohenjo-daro landmark miniatures: the Great Bath, the Great Hall ('granary'), the 'College', the Pillared Hall,
the Citadel platform and its south-east towers, First Street with its covered drains, House I of the HR area,
a DK-G well, the 'Priest-King' house, the Moneer workshops, and the Kushan stupa and monastery.

Conventions as in FORMAT.md: metres, origin at the ground centre, +X east, +Y north, main front toward -Y
unless a builder says otherwise. Fired brick of the Indus cities is a warm red-brown; mud brick and earth
roofs are paler. Most geometry is collected in a Batch (one mesh per colour) so that brick courses, paving
and drain covers stay quick to build.
"""
import math
from chronokit import Model, box, cylinder, dome, join, shade, mesh_from
from worldkit import *

FB, FB_LT, FB_DK = "#B07A54", "#C4926A", "#936246"          # fired brick
MB, MB_LT, MB_DK = "#B89C76", "#CBB38E", "#9F8462"          # mud brick, mud plaster
ROOF, ROOF_DK = "#BCA584", "#A58E6C"                          # earth roofs on timber
TIMB, TIMB_LT = "#7A5A3E", "#9C7A56"
PAVE, PAVE_DK = "#C79A72", "#B3845E"                          # brick paving
EARTH, EARTH_DK = "#B9A07A", "#9C8462"
WATER_C, WATER_DK = "#4F7F86", "#2A3A38"
POT, POT_DK = "#A75A3C", "#7E3F2A"
PLASTER_K, PLASTER_K_DK = "#DCCBA6", "#C4B08A"                # Kushan mud plaster
REED = "#B7A06C"
SHELL = "#E8E0CE"
CARNELIAN = "#B8442C"
BOX_FACES = [(0, 3, 2, 1), (4, 5, 6, 7), (0, 1, 5, 4), (1, 2, 6, 5), (2, 3, 7, 6), (3, 0, 4, 7)]


def rnd(i, salt=0):
    """A deterministic pseudo-random number in [0, 1)."""
    return ((i * 7919 + salt * 104729 + 13) % 997) / 997.0


# ---------------------------------------------------------------- batched geometry

class Batch:
    """Collects boxes, prisms and rings per colour and emits one mesh per colour."""

    def __init__(self, name):
        self.name, self.geo, self.k = name, {}, 0

    def _add(self, color, verts, faces):
        v, f = self.geo.setdefault(color, ([], []))
        n = len(v)
        v.extend(verts)
        f.extend(tuple(i + n for i in fc) for fc in faces)

    def box(self, cx, cy, z, w, d, h, color, rz=0.0):
        if w <= 0 or d <= 0 or h <= 0:
            return
        c, s = math.cos(rz), math.sin(rz)
        pts = [(cx + x * c - y * s, cy + x * s + y * c) for x, y in ((-w / 2, -d / 2), (w / 2, -d / 2), (w / 2, d / 2), (-w / 2, d / 2))]
        self._add(color, [(x, y, z) for x, y in pts] + [(x, y, z + h) for x, y in pts], BOX_FACES)

    def span(self, x0, x1, y0, y1, z, h, color):
        self.box((x0 + x1) / 2, (y0 + y1) / 2, z, abs(x1 - x0), abs(y1 - y0), h, color)

    def poly(self, pts, z, h, color):
        n = len(pts)
        v = [(x, y, z) for x, y in pts] + [(x, y, z + h) for x, y in pts]
        f = [tuple(range(n))[::-1], tuple(range(n, 2 * n))] + [(i, (i + 1) % n, n + (i + 1) % n, n + i) for i in range(n)]
        self._add(color, v, f)

    def cyl(self, cx, cy, z, r, h, color, seg=12, r_top=None):
        rt = r if r_top is None else r_top
        n = seg
        v = [(cx + r * math.cos(math.tau * i / n), cy + r * math.sin(math.tau * i / n), z) for i in range(n)]
        v += [(cx + rt * math.cos(math.tau * i / n), cy + rt * math.sin(math.tau * i / n), z + h) for i in range(n)]
        f = [tuple(range(n))[::-1], tuple(range(n, 2 * n))] + [(i, (i + 1) % n, n + (i + 1) % n, n + i) for i in range(n)]
        self._add(color, v, f)

    def ring(self, cx, cy, z, r0, r1, h, color, seg=16):
        n = seg
        c = [(math.cos(math.tau * i / n), math.sin(math.tau * i / n)) for i in range(n)]
        v = [(cx + r1 * a, cy + r1 * b, z) for a, b in c] + [(cx + r1 * a, cy + r1 * b, z + h) for a, b in c]
        v += [(cx + r0 * a, cy + r0 * b, z) for a, b in c] + [(cx + r0 * a, cy + r0 * b, z + h) for a, b in c]
        f = []
        for i in range(n):
            j = (i + 1) % n
            f.append((i, j, n + j, n + i))                     # outer wall
            f.append((2 * n + j, 2 * n + i, 3 * n + i, 3 * n + j))   # inner wall
            f.append((n + i, n + j, 3 * n + j, 3 * n + i))     # top
            f.append((j, i, 2 * n + i, 2 * n + j))             # bottom
        self._add(color, v, f)

    def ext_y(self, prof, y0, y1, color):
        """Extrude a profile [(x, z), ...] along Y from y0 to y1."""
        n = len(prof)
        v = [(x, y0, z) for x, z in prof] + [(x, y1, z) for x, z in prof]
        f = [tuple(range(n))[::-1], tuple(range(n, 2 * n))] + [(i, (i + 1) % n, n + (i + 1) % n, n + i) for i in range(n)]
        self._add(color, v, f)

    def ext_x(self, prof, x0, x1, color):
        """Extrude a profile [(y, z), ...] along X from x0 to x1."""
        n = len(prof)
        v = [(x0, y, z) for y, z in prof] + [(x1, y, z) for y, z in prof]
        f = [tuple(range(n))[::-1], tuple(range(n, 2 * n))] + [(i, (i + 1) % n, n + (i + 1) % n, n + i) for i in range(n)]
        self._add(color, v, f)

    def obj(self, suffix=""):
        self.k += 1
        objs = [mesh_from(f"{self.name}{suffix}_{self.k}_{i}", v, f, (0, 0, 0), col) for i, (col, (v, f)) in enumerate(self.geo.items()) if v]
        self.geo = {}
        return join(objs, f"{self.name}{suffix}_{self.k}")


# ---------------------------------------------------------------- Indus building parts

def fbox(B, face, fixed, u, z, du, dn, h, color, off=0.0):
    """A box standing on a wall face: `fixed` is the face plane, u the position along it, dn how far it projects."""
    if face == "S":
        B.box(u, fixed - off - dn / 2, z, du, dn, h, color)
    elif face == "N":
        B.box(u, fixed + off + dn / 2, z, du, dn, h, color)
    elif face == "E":
        B.box(fixed + off + dn / 2, u, z, dn, du, h, color)
    else:
        B.box(fixed - off - dn / 2, u, z, dn, du, h, color)


def door(B, face, fixed, u, z, w, h, color=DARK):
    fbox(B, face, fixed, u, z, w, 0.1, h, color)


def courses(B, x0, x1, y0, y1, z0, z1, color, every=0.5, out=0.035, th=0.07, faces="NSEW"):
    """Thin projecting bands round a rectangular mass: the brick coursing that reads at miniature scale."""
    z = z0 + every
    while z < z1 - 0.1:
        if "S" in faces:
            B.box((x0 + x1) / 2, y0 - out / 2, z, x1 - x0 + 2 * out, out, th, color)
        if "N" in faces:
            B.box((x0 + x1) / 2, y1 + out / 2, z, x1 - x0 + 2 * out, out, th, color)
        if "W" in faces:
            B.box(x0 - out / 2, (y0 + y1) / 2, z, out, y1 - y0, th, color)
        if "E" in faces:
            B.box(x1 + out / 2, (y0 + y1) / 2, z, out, y1 - y0, th, color)
        z += every


def parapet(B, x0, x1, y0, y1, z, color, t=0.3, h=0.5):
    B.span(x0, x1, y0, y0 + t, z, h, color)
    B.span(x0, x1, y1 - t, y1, z, h, color)
    B.span(x0, x0 + t, y0 + t, y1 - t, z, h, color)
    B.span(x1 - t, x1, y0 + t, y1 - t, z, h, color)


def massing(B, x0, x1, y0, y1, courts, h, color, z=0.0, hvar=None):
    """Fill a rectangle with roofed rooms, leaving the courts [(cx, cy, cw, cd), ...] open.
    The rectangle is cut along every court edge; each cell outside the courts becomes one block."""
    xs = sorted({x0, x1} | {c[0] - c[2] / 2 for c in courts} | {c[0] + c[2] / 2 for c in courts})
    ys = sorted({y0, y1} | {c[1] - c[3] / 2 for c in courts} | {c[1] + c[3] / 2 for c in courts})
    xs = [x for x in xs if x0 <= x <= x1]
    ys = [y for y in ys if y0 <= y <= y1]
    for i in range(len(xs) - 1):
        for j in range(len(ys) - 1):
            cx, cy = (xs[i] + xs[i + 1]) / 2, (ys[j] + ys[j + 1]) / 2
            if any(abs(cx - c[0]) < c[2] / 2 and abs(cy - c[1]) < c[3] / 2 for c in courts):
                continue
            hh = hvar(cx, cy) if hvar else h
            B.span(xs[i], xs[i + 1], ys[j], ys[j + 1], z, hh, color)


def court_fittings(B, court, z, h, color, doors=None, paving=PAVE, beams=True, rim=True):
    """Paving, doors on the inner faces, beam ends under the roof edge and a roof rim round an open court."""
    cx, cy, cw, cd = court
    x0, x1, y0, y1 = cx - cw / 2, cx + cw / 2, cy - cd / 2, cy + cd / 2
    B.span(x0, x1, y0, y1, z, 0.1, paving)
    doors = doors if doors is not None else {"N": [cx], "S": [cx], "E": [cy], "W": [cy]}
    for face, us in doors.items():
        for u in us:
            # the wall on the court's south edge faces north, and so on
            if face == "S":
                door(B, "N", y0, u, z + 0.1, 1.0, 2.1)
            elif face == "N":
                door(B, "S", y1, u, z + 0.1, 1.0, 2.1)
            elif face == "W":
                door(B, "E", x0, u, z + 0.1, 1.0, 2.1)
            else:
                door(B, "W", x1, u, z + 0.1, 1.0, 2.1)
    if beams:
        for face, fixed, a0, a1 in (("N", y0, x0, x1), ("S", y1, x0, x1), ("E", x0, y0, y1), ("W", x1, y0, y1)):
            n = max(1, int((a1 - a0) / 0.75))
            for k in range(n):
                fbox(B, face, fixed, a0 + (a1 - a0) * (k + 0.5) / n, z + h - 0.55, 0.16, 0.22, 0.16, TIMB)
    if rim:
        t = 0.25
        B.span(x0 - t, x1 + t, y0 - t, y0, z + h, 0.35, shade(color, -0.05))
        B.span(x0 - t, x1 + t, y1, y1 + t, z + h, 0.35, shade(color, -0.05))
        B.span(x0 - t, x0, y0, y1, z + h, 0.35, shade(color, -0.05))
        B.span(x1, x1 + t, y0, y1, z + h, 0.35, shade(color, -0.05))


def tiles(B, x0, x1, y0, y1, z, size, colors, hole=None, th=0.04, gap=0.05):
    """Brick paving laid as separate slabs (skipping an optional hole rectangle)."""
    nx, ny = max(1, int((x1 - x0) / size)), max(1, int((y1 - y0) / size))
    sx, sy = (x1 - x0) / nx, (y1 - y0) / ny
    for i in range(nx):
        for j in range(ny):
            cx, cy = x0 + sx * (i + 0.5), y0 + sy * (j + 0.5)
            if hole and hole[0] - sx / 2 < cx < hole[1] + sx / 2 and hole[2] - sy / 2 < cy < hole[3] + sy / 2:
                continue
            B.box(cx, cy, z, sx - gap, sy - gap, th, colors[(i + j * 3) % len(colors)])


def well(B, x, y, z, r0=0.55, r1=1.0, h=0.8, color=FB, n_courses=6, grooves=4):
    """A round brick well shaft with dark water, coursed in rings, rope grooves on the rim."""
    hh = h / n_courses
    for k in range(n_courses):
        B.ring(x, y, z + k * hh, r0, r1 + (0.03 if k % 2 else 0.0), hh, color if k % 2 else shade(color, -0.06), seg=16)
    B.cyl(x, y, z - 0.05, r0 + 0.01, h - 0.55, WATER_DK, seg=16)
    for g in range(grooves):
        a = math.tau * (g + 0.3) / grooves
        B.box(x + (r0 + 0.1) * math.cos(a), y + (r0 + 0.1) * math.sin(a), z + h - 0.02, 0.12, 0.22, 0.04, DARK, a)


def drain(B, ax, ay, bx, by, z=0.0, w=0.8, h=0.32, holes=(), seg=0.62, color=FB, cover=True):
    """A brick drain channel along a line, covered with brick slabs; `holes` are indices of open covers."""
    L = math.hypot(bx - ax, by - ay)
    a = math.atan2(by - ay, bx - ax)
    ux, uy = math.cos(a), math.sin(a)
    nx, ny = -uy, ux
    cx, cy = (ax + bx) / 2, (ay + by) / 2
    for s in (-1, 1):
        B.box(cx + nx * s * (w / 2 - 0.1), cy + ny * s * (w / 2 - 0.1), z, L, 0.2, h, shade(color, -0.04), a)
    B.box(cx, cy, z, L, w - 0.4, h - 0.12, DARK, a)
    if not cover:
        return
    n = max(1, int(L / seg))
    for k in range(n):
        if k in holes:
            continue
        t = -L / 2 + L * (k + 0.5) / n
        B.box(cx + ux * t, cy + uy * t, z + h, L / n - 0.05, w + 0.06, 0.07, PAVE if k % 3 else PAVE_DK, a)


def sump(B, x, y, z=0.0, s=1.6, color=FB):
    B.box(x, y, z, s, s, 0.45, shade(color, -0.05))
    B.box(x, y, z + 0.45, s * 0.62, s * 0.62, 0.01, DARK)


def chute(B, face, fixed, u, z0, z1, color=FB_DK):
    """A vertical drain chute down a house wall to the street drain."""
    fbox(B, face, fixed, u, z0, 0.32, 0.22, z1 - z0, color)
    fbox(B, face, fixed, u, z0, 0.14, 0.24, z1 - z0, DARK, 0.0)


def pot(B, x, y, z, s=1.0, color=POT):
    prof = [(0.10, 0.0), (0.22, 0.12), (0.24, 0.25), (0.16, 0.42), (0.09, 0.48), (0.12, 0.54)]
    for (r0, z0), (r1, z1) in zip(prof, prof[1:]):
        B.cyl(x, y, z + z0 * s, r0 * s, (z1 - z0) * s, color, seg=10, r_top=r1 * s)


def bath_platform(B, x, y, z, w, d, chute_face=None, chute_fixed=0.0, chute_u=0.0):
    """A bathing floor of fitted brick with a curb and an outlet."""
    B.box(x, y, z, w, d, 0.12, FB_LT)
    tiles(B, x - w / 2 + 0.1, x + w / 2 - 0.1, y - d / 2 + 0.1, y + d / 2 - 0.1, z + 0.12, 0.3, [FB_LT, PAVE], th=0.03, gap=0.03)
    parapet(B, x - w / 2, x + w / 2, y - d / 2, y + d / 2, z + 0.12, FB, t=0.12, h=0.12)
    B.box(x + w / 2 - 0.25, y - d / 2 + 0.25, z + 0.15, 0.18, 0.18, 0.01, DARK)


def cart(B, x, y, z=0.0, oxen=True):
    """A solid-wheeled ox-cart (as in the clay models) facing north."""
    B.box(x, y, z + 0.75, 1.2, 2.0, 0.12, TIMB_LT)
    for s in (-1, 1):
        B.box(x + s * 0.58, y, z + 0.87, 0.06, 2.0, 0.35, TIMB)
        prof = [(y + 0.55 * math.cos(math.tau * i / 12), z + 0.55 + 0.55 * math.sin(math.tau * i / 12)) for i in range(12)]
        B.ext_x(prof, x + s * 0.68 - 0.06, x + s * 0.68 + 0.06, TIMB)
    B.box(x, y + 1.9, z + 0.75, 0.1, 1.9, 0.1, TIMB)
    B.box(x, y + 0.2, z + 0.87, 1.0, 1.3, 0.35, REED)
    if oxen:
        for s in (-1, 1):
            ox, oy = x + s * 0.5, y + 2.6
            B.box(ox, oy, z + 0.6, 0.45, 1.3, 0.55, "#8E8478")
            B.box(ox, oy + 0.35, z + 1.15, 0.3, 0.3, 0.2, "#8E8478")
            B.box(ox, oy + 0.8, z + 0.85, 0.28, 0.4, 0.3, "#7E7468")
            for lx in (-0.14, 0.14):
                for ly in (-0.5, 0.5):
                    B.box(ox + lx, oy + ly, z, 0.1, 0.1, 0.6, "#7E7468")


# ---------------------------------------------------------------- the Great Bath

def great_bath():
    """33 x 55 m. Tank 7 x 11.9 m, 2.4 m deep, steps at north and south, a colonnaded court, ranges of rooms, the drain."""
    m = Model("great-bath")
    B = Batch("gbath")
    F = 2.6                                   # deck level on its brick plinth
    tx0, tx1, ty0, ty1 = -3.5, 3.5, -7.0, 4.9
    PY0 = -25.0                               # the plinth's south face; the entrance stairs stand in front
    # plinth round the tank
    B.span(-16.5, 16.5, PY0, ty0, 0, F, FB)
    B.span(-16.5, 16.5, ty1, 27.5, 0, F, FB)
    B.span(-16.5, tx0, ty0, ty1, 0, F, FB)
    B.span(tx1, 16.5, ty0, ty1, 0, F, FB)
    courses(B, -16.5, 16.5, PY0, 27.5, 0, F, FB_DK, every=0.45)
    # the tank: floor, light brick lining, water, coping
    B.span(tx0, tx1, ty0, ty1, 0, 0.2, FB_DK)
    for x0, x1, y0, y1 in ((tx0, tx1, ty0, ty0 + 0.12), (tx0, tx1, ty1 - 0.12, ty1), (tx0, tx0 + 0.12, ty0, ty1), (tx1 - 0.12, tx1, ty0, ty1)):
        B.span(x0, x1, y0, y1, 0.2, F - 0.2, FB_LT)
    for k in range(5):
        z = 1.75 + k * 0.17
        B.span(tx0 + 0.12, tx0 + 0.14, ty0 + 0.12, ty1 - 0.12, z, 0.05, FB)
        B.span(tx1 - 0.14, tx1 - 0.12, ty0 + 0.12, ty1 - 0.12, z, 0.05, FB)
    B.span(tx0 + 0.12, tx1 - 0.12, ty0 + 0.12, ty1 - 0.12, 0.2, 1.5, WATER_C)
    parapet(B, tx0 - 0.35, tx1 + 0.35, ty0 - 0.35, ty1 + 0.35, F, PAVE_DK, t=0.35, h=0.1)
    # steps down at both ends, 9 risers, once with timber treads
    n, run, sw = 9, 0.3, 4.2
    rise = (F - 0.2) / n
    for k in range(1, n + 1):
        L = run * (n - k + 1)
        B.span(-sw / 2, sw / 2, ty0 + 0.12, ty0 + 0.12 + L, 0.2, rise * k, FB_LT if k % 2 else PAVE)
        B.span(-sw / 2, sw / 2, ty1 - 0.12 - L, ty1 - 0.12, 0.2, rise * k, FB_LT if k % 2 else PAVE)
        B.span(-sw / 2, sw / 2, ty0 + 0.12 + L - 0.06, ty0 + 0.12 + L, rise * k, 0.03, TIMB)
        B.span(-sw / 2, sw / 2, ty1 - 0.12 - L, ty1 - 0.12 - L + 0.06, rise * k, 0.03, TIMB)
    B.span(-sw / 2, sw / 2, ty0 + 0.12, ty0 + 0.12 + run * n + 0.7, 0.2, 0.25, FB_LT)
    B.span(-sw / 2, sw / 2, ty1 - 0.12 - run * n - 0.7, ty1 - 0.12, 0.2, 0.25, FB_LT)
    # the court deck: fitted brick paving
    CX0, CX1, CY0, CY1 = -7.4, 7.4, -12.5, 10.4
    tiles(B, CX0, CX1, CY0, CY1, F, 0.74, [PAVE, FB_LT, PAVE, PAVE_DK], hole=(tx0 - 0.35, tx1 + 0.35, ty0 - 0.35, ty1 + 0.35))
    # the drain: covers from the tank's south-west corner to the west range, and the corbelled outlet on the west face
    drain(B, tx0 - 0.4, ty0 + 0.5, CX0, ty0 + 0.5, z=F - 0.25, w=0.9, h=0.3, color=FB)
    B.span(-16.5 - 0.6, -16.5, ty0 - 0.2, ty0 + 1.4, 0.4, 1.4, FB_DK)
    B.ext_x([(ty0 - 0.2, 1.8), (ty0 + 1.4, 1.8), (ty0 + 0.6, 2.5)], -17.1, -16.5, FB_DK)
    B.ext_x([(ty0 + 0.2, 0.4), (ty0 + 1.0, 0.4), (ty0 + 1.0, 1.4), (ty0 + 0.6, 1.9), (ty0 + 0.2, 1.4)], -17.15, -17.08, DARK)
    # entrance stairs on the south
    for sx in (-5.0, 5.0):
        ns = 9
        for k in range(1, ns + 1):
            L = (-PY0 - 22.5) * (ns - k + 1) / ns + 0.0
            B.span(sx - 1.3, sx + 1.3, PY0 - L, PY0, 0, F * k / ns, PAVE if k % 2 else FB_LT)
        B.span(sx - 1.6, sx - 1.3, PY0 - 2.5, PY0, 0, F + 0.5, FB_DK)
        B.span(sx + 1.3, sx + 1.6, PY0 - 2.5, PY0, 0, F + 0.5, FB_DK)
    m.add(0, B.obj("_tank"), "brick platform and tank")

    # ---- colonnade, ranges of rooms, the well room
    H = 3.8
    for k in range(9):
        y = CY0 + (CY1 - CY0) * k / 8
        for x in (CX0 - 0.5, CX1 + 0.5):
            B.box(x, y, F, 1.0, 1.0, 3.0, FB)
            courses(B, x - 0.5, x + 0.5, y - 0.5, y + 0.5, F, F + 3.0, FB_DK, every=0.6, out=0.03)
    for k in range(1, 6):
        x = CX0 + (CX1 - CX0) * k / 6
        for y in (CY0 - 0.5, CY1 + 0.5):
            B.box(x, y, F, 1.0, 1.0, 3.0, FB)
            courses(B, x - 0.5, x + 0.5, y - 0.5, y + 0.5, F, F + 3.0, FB_DK, every=0.6, out=0.03)
    AMB = (0.0, -1.0, 21.2, 28.0)                 # ambulatory and court: x -10.6..10.6, y -15..13
    PASS = (0.0, 20.5, 24.0, 1.6)                 # passage between the small rooms of the north range
    WELLR = (13.55, 0.0, 3.4, 3.6)                # the well room, open to the sky in the miniature
    hv = lambda x, y: H - 0.4 if x > 10.6 else (H + 0.4 if y < -15 else H)
    massing(B, -16.5, 16.5, PY0, 27.5, [AMB, PASS, WELLR], H, MB_LT, z=F, hvar=hv)
    courses(B, -16.5, 16.5, PY0, 27.5, F, F + H, shade(MB_LT, -0.08), every=0.55)
    for x0, x1, y0, y1 in ((-10.6, 10.6, -15.0, CY0), (-10.6, 10.6, CY1, 13.0), (-10.6, CX0, CY0, CY1), (CX1, 10.6, CY0, CY1)):
        B.span(x0, x1, y0, y1, F, 0.05, PAVE_DK)
    B.span(-12.0, 12.0, 19.7, 21.3, F, 0.06, PAVE_DK)
    drain(B, -12.0, 20.5, 12.0, 20.5, z=F, w=0.6, h=0.12, color=FB, cover=False)
    for i in range(8):
        x = -10.5 + i * 3.0
        door(B, "N", 19.7, x, F, 0.8, 2.0)
        door(B, "S", 21.3, x, F, 0.8, 2.0)
    for u in (-5.0, 5.0):
        door(B, "S", PY0, u, F, 1.6, 2.6)
        door(B, "N", -15.0, u, F, 1.5, 2.4)
    door(B, "W", 10.6, 0.0, F, 1.2, 2.2)
    for u in (-9.0, 7.0):
        door(B, "W", 10.6, u, F, 1.0, 2.2)
        door(B, "E", -10.6, u, F, 1.0, 2.2)
    door(B, "S", 13.0, -4.0, F, 1.2, 2.2)
    door(B, "S", 13.0, 4.0, F, 1.2, 2.2)
    well(B, WELLR[0], WELLR[1], F, r0=0.5, r1=0.95, h=0.75)
    B.span(WELLR[0] - 1.7, WELLR[0] + 1.7, WELLR[1] - 1.8, WELLR[1] + 1.8, F, 0.06, PAVE)
    m.add(1, B.obj("_rooms"), "colonnade and rooms")

    # ---- roofs: the ambulatory roof on the piers, range roofs with parapets, spouts and a stair head
    RZ = F + 3.0
    for x0, x1, y0, y1 in ((-10.6, 10.6, -15.0, CY0 - 0.0), (-10.6, 10.6, CY1, 13.0), (-10.6, CX0, CY0, CY1), (CX1, 10.6, CY0, CY1)):
        B.span(x0, x1, y0, y1, RZ, 0.3, ROOF)
    for face, fixed, a0, a1 in (("N", CY0, CX0, CX1), ("S", CY1, CX0, CX1), ("E", CX0, CY0, CY1), ("W", CX1, CY0, CY1)):
        n = int((a1 - a0) / 0.55)
        for k in range(n):
            fbox(B, face, fixed, a0 + (a1 - a0) * (k + 0.5) / n, RZ - 0.18, 0.14, 0.25, 0.16, TIMB)
    parapet(B, CX0, CX1, CY0, CY1, RZ + 0.3, ROOF_DK, t=0.22, h=0.25)
    parapet(B, -16.5, 16.5, PY0, 27.5, F + H, shade(MB_LT, -0.06), t=0.35, h=0.6)
    for y in (-21.0, -18.0, 16.0, 24.5):
        B.span(-16.2, 16.2, y - 0.12, y + 0.12, F + H, 0.3, ROOF_DK)
    for x in (-13.5, 13.5):
        for y in (-7.0, 7.0, 21.5):
            B.span(x - 2.6, x + 2.6, y - 0.1, y + 0.1, F + H - 0.4 if x > 0 else F + H, 0.3, ROOF_DK)
    for x0, x1, y0, y1, hh in ((-16.5, -10.6, -15.0, 13.0, H), (10.6, 16.5, -15.0, 13.0, H - 0.4), (-16.5, 16.5, PY0, -15.0, H + 0.4), (-16.5, 16.5, 13.0, 27.5, H)):
        B.span(x0 + 0.3, x1 - 0.3, y0 + 0.3, y1 - 0.3, F + hh, 0.04, ROOF)
    B.span(-15.6, -12.8, 23.0, 26.6, F + H, 2.2, MB_LT)
    door(B, "E", -12.8, 24.8, F + H, 0.8, 1.8)
    B.span(-15.8, -12.6, 22.8, 26.8, F + H + 2.2, 0.25, ROOF_DK)
    for k in range(9):
        u = -14.0 + k * 3.5
        fbox(B, "S", PY0, u, F + H - 0.2, 0.25, 0.6, 0.2, TIMB)
        fbox(B, "N", 27.5, u, F + H - 0.2, 0.25, 0.6, 0.2, TIMB)
    for k in range(12):
        u = -23.0 + k * 4.4
        fbox(B, "W", -16.5, u, F + H - 0.2, 0.25, 0.6, 0.2, TIMB)
        fbox(B, "E", 16.5, u, F + H - 0.6, 0.25, 0.6, 0.2, TIMB)
    m.add(2, B.obj("_roofs"), "roofs")
    return m


# ---------------------------------------------------------------- the Great Hall ("granary")

def great_hall():
    """50 x 27 m. 27 brick blocks in three rows divided by passages, a loading platform on the north,
    a timber superstructure (reconstructed) roofed over its western two-thirds."""
    m = Model("great-hall")
    B = Batch("ghall")
    Hb = 4.2
    gx, gy = 1.0, 1.3
    bw = (50 - 8 * gx) / 9
    bd = (23.5 - 2 * gy) / 3
    B.span(-25, 25, -13.5, 10.0, 0, 0.08, EARTH_DK)
    blocks = []
    for i in range(9):
        for j in range(3):
            x0 = -25 + i * (bw + gx)
            y0 = -13.5 + j * (bd + gy)
            blocks.append((x0, x0 + bw, y0, y0 + bd))
            B.span(x0, x0 + bw, y0, y0 + bd, 0, Hb, FB if (i + j) % 2 else shade(FB, 0.03))
            courses(B, x0, x0 + bw, y0, y0 + bd, 0, Hb, FB_DK, every=0.6)
            for k in range(2):
                B.box(x0 + bw * (0.3 + 0.4 * k), y0 + bd / 2, Hb, 0.4, 0.4, 0.02, DARK)
    # the loading platform on the north and its stair
    B.span(-25, 25, 10.0, 13.5, 0, 2.2, FB_DK)
    courses(B, -25, 25, 10.0, 13.5, 0, 2.2, FB, every=0.55)
    m.add(0, B.obj("_podium"), "brick podium")

    # ---- timber frame: floor beams across the passages, posts, wall plates, screens
    for (x0, x1, y0, y1) in blocks:
        for px in (x0 + 0.6, x1 - 0.6):
            for py in (y0 + 0.6, y1 - 0.6):
                B.box(px, py, Hb, 0.32, 0.32, 3.0, TIMB)
    for i in range(9):
        x0 = -25 + i * (bw + gx)
        for px in (x0 + 0.6, x0 + bw - 0.6):
            B.box(px, -1.75, Hb, 0.3, 23.5, 0.3, TIMB_LT)
            B.box(px, -1.75, Hb + 3.0, 0.3, 23.5, 0.32, TIMB_LT)
    for j in range(3):
        y0 = -13.5 + j * (bd + gy)
        for py in (y0 + 0.6, y0 + bd - 0.6):
            B.box(0, py, Hb + 2.7, 50.0, 0.3, 0.3, TIMB)
    B.span(-25.0, 25.0, -13.5, 10.0, Hb + 0.3, 0.12, TIMB_LT)
    for i in range(9):
        x0 = -25 + i * (bw + gx)
        for (y, face) in ((-13.5, "S"), (10.0, "N")):
            fbox(B, face, y, x0 + bw / 2, Hb + 0.42, bw - 1.0, 0.12, 1.9, REED)
            for k in range(6):
                fbox(B, face, y, x0 + 0.6 + (bw - 1.2) * (k + 0.5) / 6, Hb + 0.42, 0.06, 0.18, 1.9, TIMB)
    for (x, face) in ((-25.0, "W"), (25.0, "E")):
        for j in range(3):
            y0 = -13.5 + j * (bd + gy)
            fbox(B, face, x, y0 + bd / 2, Hb + 0.42, bd - 1.0, 0.12, 1.9, REED)
    # stair from the loading platform up to the hall floor
    for k in range(1, 7):
        B.span(-2.0, 2.0, 10.0, 10.0 + 3.2 * (7 - k) / 6, 2.2, (Hb + 0.42 - 2.2) * k / 6, PAVE if k % 2 else FB_LT)
    for k in range(1, 9):
        B.span(18.0, 21.0, 13.5 - 3.4 * (9 - k) / 8, 13.5, 0, 2.2 * k / 8, PAVE if k % 2 else FB_LT)
    m.add(1, B.obj("_frame"), "timber frame")

    # ---- the roof over the western two-thirds; joists bare over the east to show the frame
    RZ = Hb + 3.32
    B.span(-25.6, 8.3, -14.1, 10.6, RZ, 0.38, ROOF)
    B.span(-25.6, 8.3, -14.1, -13.8, RZ + 0.38, 0.3, ROOF_DK)
    B.span(-25.6, 8.3, 10.3, 10.6, RZ + 0.38, 0.3, ROOF_DK)
    B.span(-25.6, -25.3, -14.1, 10.6, RZ + 0.38, 0.3, ROOF_DK)
    for k in range(10):
        x = -23 + k * 3.4
        B.span(x - 0.1, x + 0.1, -13.8, 10.3, RZ + 0.38, 0.2, ROOF_DK)
    n = int((25.0 - 8.3) / 0.7)
    for k in range(n):
        x = 8.6 + k * 0.7
        B.box(x, -1.75, RZ, 0.2, 24.6, 0.22, TIMB_LT)
    for k in range(int(33.9 / 0.6)):
        x = -25.4 + k * 0.6
        B.box(x, -14.0, RZ - 0.2, 0.15, 0.4, 0.15, TIMB)
        B.box(x, 10.5, RZ - 0.2, 0.15, 0.4, 0.15, TIMB)
    m.add(2, B.obj("_roof"), "roof")
    return m


# ---------------------------------------------------------------- the "College"

def college():
    """70 x 24 m. Rooms round a cloistered court, smaller courts, an upper storey on the east (reconstructed)."""
    m = Model("college")
    B = Batch("college")
    H = 4.0
    COURT = (-4.0, 1.0, 15.0, 14.0)        # court with its verandah
    INNER = (-4.0, 1.0, 11.0, 10.0)
    EAST = (21.0, -4.0, 7.0, 6.0)
    WEST = (-27.0, 2.0, 5.0, 5.0)
    B.span(-35.3, 35.3, -12.3, 12.3, 0, 0.35, FB_DK)
    massing(B, -35, 35, -12, 12, [COURT, EAST, WEST], H, MB_LT, z=0.35)
    courses(B, -35, 35, -12, 12, 0.35, H + 0.35, shade(MB_LT, -0.08), every=0.5)
    B.span(-35.3, 35.3, -12.3, 12.3, 0.35, 0.6, FB)
    court_fittings(B, INNER, 0.35, H - 0.6, MB_LT, doors={"N": [-6, -2], "S": [-4], "E": [1], "W": [1]}, beams=False, rim=False)
    tiles(B, INNER[0] - INNER[2] / 2, INNER[0] + INNER[2] / 2, INNER[1] - INNER[3] / 2, INNER[1] + INNER[3] / 2, 0.45, 0.7, [PAVE, FB_LT, PAVE_DK])
    court_fittings(B, EAST, 0.35, H, MB_LT, doors={"N": [21], "W": [-4]})
    court_fittings(B, WEST, 0.35, H, MB_LT, doors={"E": [2], "S": [-27]})
    # verandah floor and doors behind it
    B.span(COURT[0] - COURT[2] / 2, COURT[0] + COURT[2] / 2, COURT[1] - COURT[3] / 2, COURT[1] + COURT[3] / 2, 0.35, 0.08, PAVE_DK)
    for u in (-9.0, -4.0, 1.0):
        door(B, "N", COURT[1] - COURT[3] / 2, u, 0.43, 1.0, 2.2)
        door(B, "S", COURT[1] + COURT[3] / 2, u, 0.43, 1.0, 2.2)
    for u in (-3.0, 1.0, 5.0):
        door(B, "E", COURT[0] - COURT[2] / 2, u, 0.43, 1.0, 2.2)
        door(B, "W", COURT[0] + COURT[2] / 2, u, 0.43, 1.0, 2.2)
    # the south entrance with its porch, side doors
    door(B, "S", -12.0, -4.0, 0.35, 2.0, 2.8)
    for s in (-1, 1):
        B.box(-4.0 + s * 1.6, -12.6, 0.35, 0.9, 1.2, 3.4, FB)
    for u in (14.0, 26.0):
        door(B, "S", -12.0, u, 0.35, 1.1, 2.3)
    door(B, "W", -35.0, -6.0, 0.35, 1.1, 2.3)
    door(B, "E", 35.0, 4.0, 0.35, 1.1, 2.3)
    # stair in the west court
    for k in range(1, 9):
        B.span(-29.4, -28.4, -0.5, -0.5 + 4.6 * k / 8, 0.35, H * k / 8, FB_LT)
    m.add(0, B.obj("_walls"), "walls and courts")

    # ---- verandah piers and roof
    cx, cy, cw, cd = INNER
    for k in range(6):
        x = cx - cw / 2 + cw * k / 5
        for y in (cy - cd / 2, cy + cd / 2):
            B.box(x, y, 0.35, 0.8, 0.8, 3.0, FB)
            courses(B, x - 0.4, x + 0.4, y - 0.4, y + 0.4, 0.35, 3.35, FB_DK, every=0.6, out=0.03)
    for k in range(1, 5):
        y = cy - cd / 2 + cd * k / 5
        for x in (cx - cw / 2, cx + cw / 2):
            B.box(x, y, 0.35, 0.8, 0.8, 3.0, FB)
            courses(B, x - 0.4, x + 0.4, y - 0.4, y + 0.4, 0.35, 3.35, FB_DK, every=0.6, out=0.03)
    vz = 3.35
    X0, X1, Y0, Y1 = COURT[0] - COURT[2] / 2, COURT[0] + COURT[2] / 2, COURT[1] - COURT[3] / 2, COURT[1] + COURT[3] / 2
    ix0, ix1, iy0, iy1 = cx - cw / 2 - 0.4, cx + cw / 2 + 0.4, cy - cd / 2 - 0.4, cy + cd / 2 + 0.4
    for x0, x1, y0, y1 in ((X0, X1, Y0, iy0), (X0, X1, iy1, Y1), (X0, ix0, iy0, iy1), (ix1, X1, iy0, iy1)):
        B.span(x0, x1, y0, y1, vz, 0.3, ROOF)
    for face, fixed, a0, a1 in (("N", iy0, ix0, ix1), ("S", iy1, ix0, ix1), ("E", ix0, iy0, iy1), ("W", ix1, iy0, iy1)):
        n = int((a1 - a0) / 0.6)
        for k in range(n):
            fbox(B, face, fixed, a0 + (a1 - a0) * (k + 0.5) / n, vz - 0.16, 0.14, 0.22, 0.15, TIMB)
    parapet(B, ix0, ix1, iy0, iy1, vz + 0.3, ROOF_DK, t=0.2, h=0.25)
    m.add(1, B.obj("_cloister"), "cloister")

    # ---- roofs, parapets, the upper storey on the east
    top = H + 0.35
    parapet(B, -35, 35, -12, 12, top, shade(MB_LT, -0.06), t=0.35, h=0.6)
    for x in (-31.0, -22.0, -16.0, 8.0, 14.0, 28.0):
        B.span(x - 0.12, x + 0.12, -11.7, 11.7, top, 0.3, ROOF_DK)
    for y in (-8.0, 8.0):
        B.span(-34.7, -12.0, y - 0.12, y + 0.12, top, 0.3, ROOF_DK)
    B.span(-34.7, 34.7, -11.7, 11.7, top - 0.02, 0.04, ROOF)
    UX0, UX1, UY0, UY1 = 9.0, 33.0, 1.5, 11.5
    B.span(UX0, UX1, UY0, UY1, top, 2.9, MB_LT)
    courses(B, UX0, UX1, UY0, UY1, top, top + 2.9, shade(MB_LT, -0.08), every=0.5)
    parapet(B, UX0, UX1, UY0, UY1, top + 2.9, shade(MB_LT, -0.06), t=0.3, h=0.5)
    for u in (12.0, 18.0, 24.0, 30.0):
        door(B, "S", UY0, u, top, 0.9, 1.9)
    for x in (15.0, 21.0, 27.0):
        B.span(x - 0.1, x + 0.1, UY0 + 0.3, UY1 - 0.3, top + 2.9, 0.25, ROOF_DK)
    B.span(-30.4, -27.6, -1.0, 2.0, top, 2.2, MB_LT)
    door(B, "N", 2.0, -29.0, top, 0.8, 1.8)
    for k in range(14):
        u = -33.0 + k * 5.0
        fbox(B, "S", -12.0, u, top - 0.25, 0.25, 0.6, 0.2, TIMB)
        fbox(B, "N", 12.0, u, top - 0.25, 0.25, 0.6, 0.2, TIMB)
    m.add(2, B.obj("_roofs"), "roofs and upper storey")
    return m


# ---------------------------------------------------------------- the Pillared Hall

def pillared_hall():
    """28 x 28 m. Twenty brick piers in four rows of five, paved aisles, a low outer wall with doors;
    the roof is left off the southern half to show the piers."""
    m = Model("pillared-hall")
    B = Batch("phall")
    P = 0.5
    B.span(-14, 14, -14, 14, 0, P, FB_DK)
    courses(B, -14, 14, -14, 14, 0, P, FB, every=0.25)
    tiles(B, -12.8, 12.8, -12.8, 12.8, P, 1.0, [PAVE, FB_LT, PAVE_DK, PAVE])
    xs = [-10.0, -5.0, 0.0, 5.0, 10.0]
    ys = [-9.0, -3.0, 3.0, 9.0]
    for y in ys:
        B.span(-12.8, 12.8, y - 1.6, y + 1.6, P, 0.06, FB)
    m.add(0, B.obj("_floor"), "floor")

    W = 4.4
    for x0, x1, y0, y1 in ((-14, 14, -14, -12.8), (-14, 14, 12.8, 14), (-14, -12.8, -12.8, 12.8), (12.8, 14, -12.8, 12.8)):
        B.span(x0, x1, y0, y1, P, W - P, MB_LT)
    courses(B, -14, 14, -14, 14, P, W, shade(MB_LT, -0.08), every=0.5)
    for u in (-7.5, 0.0, 7.5):
        door(B, "S", -14, u, P, 1.8, 2.6)
        door(B, "N", -12.8, u, P, 1.8, 2.6)
    for f, fx, fi in (("W", -14, -12.8), ("E", 14, 12.8)):
        door(B, f, fx, 0.0, P, 1.8, 2.6)
        door(B, "E" if f == "W" else "W", fi, 0.0, P, 1.8, 2.6)
    door(B, "N", 14, 6.0, P, 1.4, 2.4)
    for x in xs:
        for y in ys:
            B.box(x, y, P, 1.5, 1.5, W - P - 0.4, FB)
            courses(B, x - 0.75, x + 0.75, y - 0.75, y + 0.75, P, W - 0.4, FB_DK, every=0.42, out=0.03)
            B.box(x, y, W - 0.6, 1.8, 1.8, 0.2, FB_LT)
    for k in range(4):
        B.box(-11.6, -10.5 + k * 7.0, P, 0.9, 0.5, 0.45, FB_LT)
        B.box(11.6, -10.5 + k * 7.0, P, 0.9, 0.5, 0.45, FB_LT)
    m.add(1, B.obj("_piers"), "walls and piers")

    for y in ys:
        B.span(-13.4, 13.4, y - 0.25, y + 0.25, W - 0.4, 0.4, TIMB)
    for k in range(int(26.8 / 0.8)):
        x = -13.0 + k * 0.8
        B.span(x - 0.09, x + 0.09, -13.4, 0.0, W, 0.2, TIMB_LT)
    B.span(-14, 14, 0.0, 14, W, 0.4, ROOF)
    parapet(B, -14, 14, 0.0, 14, W + 0.4, ROOF_DK, t=0.3, h=0.45)
    B.span(-14, 14, -14, -13.6, W, 0.3, ROOF_DK)
    B.span(-14, -13.6, -13.6, 0.0, W, 0.3, ROOF_DK)
    B.span(13.6, 14, -13.6, 0.0, W, 0.3, ROOF_DK)
    for x in (-7.0, 0.0, 7.0):
        B.span(x - 0.1, x + 0.1, 0.4, 13.6, W + 0.4, 0.2, ROOF_DK)
    for k in range(9):
        u = -12.0 + k * 3.0
        fbox(B, "N", 14, u, W - 0.2, 0.25, 0.6, 0.2, TIMB)
    m.add(2, B.obj("_roof"), "roof")
    return m


# ---------------------------------------------------------------- the Citadel platform (east face)

def citadel_platform():
    """20 x 100 m, built facing east (toward the Lower Town) with rotation 0: the battered brick face of the
    platform, two solid towers, drain outlets, a stair up the face and buildings on top."""
    m = Model("citadel-platform")
    B = Batch("cplat")
    H = 10.0
    xo = lambda z: 6.0 - 3.5 * z / H
    B.span(6.0, 10.0, -50, 50, 0, 0.05, EARTH)
    B.ext_y([(-10, 0), (6.0, 0), (2.5, H), (-10, H)], -50, 50, MB)
    B.ext_y([(5.6, 0.0), (6.3, 0.0), (5.95, 1.0), (5.25, 1.0)], -50, 50, FB_DK)
    segs = [(-50, -30), (-18, 18), (30, 50)]
    z = 0.45
    while z < H - 0.2:
        for a, b in segs:
            B.box(xo(z) + 0.04, (a + b) / 2, z, 0.12, b - a, 0.08, FB_DK)
        z += 0.45
    # patches of fired-brick facing over the mud-brick core
    for k, (y0, y1, z0, z1) in enumerate(((-12, -2, 1.0, 6.0), (4, 14, 2.0, 8.5), (34, 46, 0.5, 5.5), (-28, -20, 3.0, 9.0))):
        zz = z0
        while zz < z1:
            B.box(xo(zz) + 0.02, (y0 + y1) / 2, zz, 0.08, y1 - y0, 0.45, FB if (k + int(zz * 2)) % 2 else FB_LT)
            zz += 0.45
    m.add(0, B.obj("_face"), "platform")

    # ---- towers, drain outlets, the stair
    TH = H + 2.0
    xt = lambda z: 9.6 - 1.4 * z / TH
    for yc in (-24.0, 24.0):
        B.ext_y([(-2, 0), (9.6, 0), (8.2, TH), (-2, TH)], yc - 6, yc + 6, FB)
        z = 0.5
        while z < TH - 0.2:
            B.box(xt(z) + 0.04, yc, z, 0.12, 12.0, 0.08, FB_DK)
            for s in (-1, 1):
                x0 = xo(z) if z < H else 2.5
                B.box((x0 + xt(z)) / 2, yc + s * 6.04, z, xt(z) - x0, 0.1, 0.08, FB_DK)
            z += 0.5
        parapet(B, -2, 8.2, yc - 6, yc + 6, TH, FB_DK, t=0.4, h=0.8)
        B.span(0.0, 4.0, yc - 2.0, yc + 2.0, TH, 2.3, MB_LT)
        door(B, "E", 4.0, yc, TH, 0.8, 1.7)
        B.span(-0.2, 4.2, yc - 2.2, yc + 2.2, TH + 2.3, 0.25, ROOF_DK)
    for y in (-12.0, 0.0, 12.0, 38.0, 44.0):
        zc = 7.6
        B.box(xo(zc) + 0.02, y, zc - 0.2, 0.1, 0.7, 0.7, DARK)
        B.box(xo(zc) + 0.45, y, zc, 0.9, 0.5, 0.2, FB_DK)
        B.box(xo(zc) + 0.85, y, zc - 0.2, 0.1, 0.36, 0.2, DARK)
        B.box(xo(3.5) + 0.03, y, 0.0, 0.08, 0.7, zc - 0.3, shade(MB, -0.12))
    n, rise, run, ys = 25, H / 25, 0.6, -47.0
    for k in range(1, n + 1):
        zt = rise * k
        y0 = ys + (k - 1) * run
        B.span(0.0, xo(zt) + 2.2, y0, y0 + run, 0, zt, PAVE if k % 2 else FB_LT)
        B.span(xo(zt) + 2.2, xo(zt) + 2.5, y0, y0 + run, 0, zt + 0.8, FB_DK)
    m.add(1, B.obj("_towers"), "towers, drains and stair")

    # ---- the top: parapet along the edge and buildings
    for a, b in ((-32.0, -30.0), (-18, 18), (30, 50)):
        B.span(2.0, 2.6, a, b, H, 0.9, FB_DK)
    B.span(-10, 2.5, -50, 50, H, 0.06, EARTH)
    for (y0, y1, court) in ((-46.0, -33.0, (-5.0, -39.5, 4.0, 4.5)), (-15.0, -3.0, (-5.5, -9.0, 4.0, 4.0)), (2.0, 15.0, (-4.5, 8.5, 4.5, 5.0)), (33.0, 48.0, (-5.0, 40.5, 4.0, 5.0))):
        massing(B, -9.6, -0.5, y0, y1, [court], 3.4, MB_LT, z=H)
        court_fittings(B, court, H, 3.4, MB_LT, doors={"N": [court[0]], "W": [court[1]]})
        parapet(B, -9.6, -0.5, y0, y1, H + 3.4, shade(MB_LT, -0.06), t=0.3, h=0.45)
        door(B, "E", -0.5, (y0 + y1) / 2, H, 1.0, 2.2)
        courses(B, -9.6, -0.5, y0, y1, H, H + 3.4, shade(MB_LT, -0.08), every=0.5)
        well(B, court[0] + 1.0, court[1] + 1.0, H + 0.1, r0=0.35, r1=0.65, h=0.6, n_courses=4)
    m.add(2, B.obj("_top"), "buildings on top")
    return m


# ---------------------------------------------------------------- the south-east towers

def southern_defences():
    """50 x 25 m, facing south: the platform's battered south face, three solid towers, a postern and a stair."""
    m = Model("southern-defences")
    B = Batch("sdef")
    H = 9.0
    yf = lambda z: -7.5 + 3.0 * z / H
    B.span(-25, 25, -12.5, -7.5, 0, 0.05, EARTH)
    B.ext_x([(12.5, 0), (-7.5, 0), (-4.5, H), (12.5, H)], -25, 25, MB)
    B.ext_x([(-7.1, 0.0), (-7.8, 0.0), (-7.45, 0.9), (-6.75, 0.9)], -25, 25, FB_DK)
    segs = [(-25, -20.5), (-11.5, -4.5), (4.5, 11.5), (20.5, 25)]
    z = 0.45
    while z < H - 0.2:
        for a, b in segs:
            B.box((a + b) / 2, yf(z) - 0.04, z, b - a, 0.12, 0.08, FB_DK)
        z += 0.45
    for k, (x0, x1, z0, z1) in enumerate(((-24, -21, 0.5, 7.0), (-11, -5, 0.0, 8.5), (5, 11, 1.0, 6.0), (21, 25, 0.0, 8.5))):
        zz = z0
        while zz < z1:
            B.box((x0 + x1) / 2, yf(zz) - 0.02, zz, x1 - x0, 0.08, 0.45, FB if (k + int(zz * 2)) % 2 else FB_LT)
            zz += 0.45
    m.add(0, B.obj("_face"), "platform face")

    TH = H + 2.5
    yt = lambda z: -12.3 + 1.3 * z / TH
    for xc in (-16.0, 0.0, 16.0):
        B.ext_x([(2, 0), (-12.3, 0), (-11.0, TH), (2, TH)], xc - 4.5, xc + 4.5, FB)
        z = 0.5
        while z < TH - 0.2:
            B.box(xc, yt(z) - 0.04, z, 9.0, 0.12, 0.08, FB_DK)
            for s in (-1, 1):
                y1 = yf(z) if z < H else -4.5
                B.box(xc + s * 4.54, (yt(z) + y1) / 2, z, 0.1, y1 - yt(z), 0.08, FB_DK)
            z += 0.5
        # a band of rougher late repair brick near the base
        B.box(xc, yt(1.2) - 0.06, 0.6, 7.0, 0.1, 1.4, FB_DK)
        parapet(B, xc - 4.5, xc + 4.5, -11.0, 2.0, TH, FB_DK, t=0.4, h=0.8)
        B.span(xc - 2.0, xc + 2.0, -3.0, 1.5, TH, 2.2, MB_LT)
        door(B, "S", -3.0, xc, TH, 0.8, 1.7)
        B.span(xc - 2.2, xc + 2.2, -3.2, 1.7, TH + 2.2, 0.25, ROOF_DK)
    # the postern between the western towers
    B.span(-9.6, -6.4, -9.0, -5.5, 0, 3.4, FB)
    courses(B, -9.6, -6.4, -9.0, -5.5, 0, 3.4, FB_DK, every=0.45, faces="SEW")
    door(B, "S", -9.0, -8.0, 0.0, 1.2, 2.4)
    B.span(-9.8, -6.2, -9.2, -5.5, 3.4, 0.3, FB_DK)
    # stair up the face between the central and eastern towers
    n, rise, run = 20, H / 20, 0.3
    for k in range(1, n + 1):
        zt = rise * k
        x0 = 5.0 + (k - 1) * run
        B.span(x0, x0 + run, yf(zt) - 2.0, 4.0, 0, zt, PAVE if k % 2 else FB_LT)
        B.span(x0, x0 + run, yf(zt) - 2.3, yf(zt) - 2.0, 0, zt + 0.8, FB_DK)
    m.add(1, B.obj("_towers"), "towers, postern and stair")

    for a, b in ((-25, -20.5), (-11.5, -4.5), (4.5, 11.5), (20.5, 25)):
        B.span(a, b, -4.9, -4.3, H, 1.0, FB_DK)
    B.span(-25, 25, -4.5, 12.5, H, 0.06, EARTH)
    for (x0, x1, court) in ((-24.0, -9.0, (-16.5, 7.5, 4.0, 3.5)), (-6.0, 6.0, (0.0, 8.0, 3.5, 3.0)), (9.0, 24.0, (16.5, 7.5, 4.0, 3.5))):
        massing(B, x0, x1, 3.5, 12.5, [court], 3.2, MB_LT, z=H)
        court_fittings(B, court, H, 3.2, MB_LT, doors={"S": [court[0]], "N": [court[0] - 1.0]})
        parapet(B, x0, x1, 3.5, 12.5, H + 3.2, shade(MB_LT, -0.06), t=0.3, h=0.45)
        courses(B, x0, x1, 3.5, 12.5, H, H + 3.2, shade(MB_LT, -0.08), every=0.5)
        door(B, "S", 3.5, (x0 + x1) / 2 + 2.5, H, 1.0, 2.1)
    m.add(2, B.obj("_top"), "parapet and buildings")
    return m


# ---------------------------------------------------------------- First Street and its drains

def _street_houses(B, side, plots, y_start, lane_edges, upper):
    """A row of courtyard houses along one side of the street (side -1 west, +1 east)."""
    xa, xb = (5.4, 15.0) if side > 0 else (-15.0, -5.4)
    street_face = "E" if side < 0 else "W"
    street_x = xb if side < 0 else xa
    y = y_start
    for k, L in enumerate(plots):
        y0, y1 = y + 0.12, y + L - 0.12
        y += L
        r = rnd(k + (0 if side < 0 else 50) + int(y_start), 3)
        h = 3.6 + r * 1.4
        cw, cd = 3.6 + r * 1.0, min(L * 0.45, 5.0)
        cx = (xa + xb) / 2 + side * (1.2 + r * 0.6)
        cy = (y0 + y1) / 2 + (r - 0.5) * 1.5
        court = (cx, cy, cw, cd)
        massing(B, xa, xb, y0, y1, [court], h, MB_LT if k % 3 else shade(MB_LT, -0.04))
        courses(B, xa, xb, y0, y1, 0, h, shade(MB_LT, -0.1), every=0.6, faces=street_face)
        doors = {"N": [cx], "S": [cx - 0.6]}
        doors["E" if side < 0 else "W"] = [cy]
        court_fittings(B, court, 0.0, h, MB_LT, doors=doors)
        if k % 2 == 0:
            well(B, cx - side * (cw / 2 - 0.8), cy + cd / 2 - 0.8, 0.1, r0=0.32, r1=0.6, h=0.6, n_courses=4)
        bath_platform(B, cx + side * (cw / 2 - 0.75), cy - cd / 2 + 0.75, 0.1, 1.3, 1.3)
        # bathroom and latrine chutes down the blank street wall into the drain
        for u in ((y0 + y1) / 2 - L * 0.22, (y0 + y1) / 2 + L * 0.25)[: 1 + (k % 2)]:
            chute(B, street_face, street_x, u, 0.0, h * (0.55 if k % 3 else 0.9))
        # roof: parapet, room divisions, a stair head on some
        parapet(B, xa, xb, y0, y1, h, shade(MB_LT, -0.06), t=0.25, h=0.45)
        B.span(xa + 0.25, xb - 0.25, y0 + 0.25, y1 - 0.25, h, 0.03, ROOF)
        for f in (0.3, 0.7):
            yy = y0 + (y1 - y0) * f
            if abs(yy - cy) > cd / 2 + 0.3:
                B.span(xa + 0.25, xb - 0.25, yy - 0.1, yy + 0.1, h, 0.25, ROOF_DK)
        if k in upper:
            ux0, ux1 = (xb - 3.6, xb) if side > 0 else (xa, xa + 3.6)
            B.span(ux0, ux1, y0, y1, h, 2.8, MB_LT)
            parapet(B, ux0, ux1, y0, y1, h + 2.8, shade(MB_LT, -0.06), t=0.25, h=0.4)
            door(B, "W" if side > 0 else "E", ux0 if side > 0 else ux1, (y0 + y1) / 2, h, 0.8, 1.8)
            for kk in range(int((y1 - y0) / 0.8)):
                fbox(B, "E" if side > 0 else "W", ux1 if side > 0 else ux0, y0 + 0.4 + kk * 0.8, h + 0.1, 0.12, 0.25, 0.12, TIMB)
        elif k % 3 == 1:
            sx = (xb - 1.6) if side > 0 else (xa + 1.6)
            B.box(sx, y1 - 1.6, h, 1.8, 2.4, 2.0, MB_LT)
            B.box(sx, y1 - 1.6, h + 2.0, 2.0, 2.6, 0.2, ROOF_DK)
        # doors on the side lane only
        if abs(y0 - lane_edges[1]) < 0.3:
            door(B, "N", y0, (xa + xb) / 2 + side * 1.5, 0.0, 1.0, 2.2)
        if abs(y1 - lane_edges[0]) < 0.3:
            door(B, "S", y1, (xa + xb) / 2 + side * 1.5, 0.0, 1.0, 2.2)


def main_street():
    """30 x 140 m along First Street (Y = north): the street with covered drains on both sides, sump pits,
    inspection holes, a side lane with its own drain, a public well and blank-walled courtyard houses."""
    m = Model("main-street")
    B = Batch("street")
    B.span(-5.0, 5.0, -70, 70, 0, 0.06, EARTH)
    LANE = (8.0, 12.0)
    B.span(-15.0, -5.0, LANE[0], LANE[1], 0, 0.05, EARTH)
    B.span(5.0, 15.0, LANE[0], LANE[1], 0, 0.05, EARTH)
    for s in (-1, 1):
        drain(B, s * 4.3, -70, s * 4.3, 70, z=0.0, w=0.9, h=0.32, holes=(17, 51, 83, 120, 160, 199), color=FB)
        drain(B, s * 15.0, 10.0, s * 5.0, 10.0, z=0.0, w=0.55, h=0.25, holes=(4,), color=FB)
        for y in (-40.0, 10.0, 46.0):
            sump(B, s * 4.3, y, 0.0, 1.7)
    # silt dug out of a sump and piled beside it
    B.box(-2.6, -40.0, 0.0, 1.6, 2.6, 0.35, EARTH_DK)
    B.box(-2.6, -40.0, 0.35, 0.9, 1.6, 0.25, shade(EARTH_DK, -0.08))
    m.add(0, B.obj("_street"), "street and drains")

    _street_houses(B, -1, [12, 9, 14, 10, 11, 13, 9.0], -70.0, LANE, upper={1, 4})
    _street_houses(B, -1, [10, 13, 9, 12, 14.0], 12.0, LANE, upper={2})
    _street_houses(B, 1, [10, 13, 11, 9, 14, 12, 9.0], -70.0, LANE, upper={2, 5})
    _street_houses(B, 1, [12, 9, 14, 10, 13.0], 12.0, LANE, upper={0, 3})
    m.add(1, B.obj("_houses"), "houses")

    # the public well at the lane corner, carts and pots
    B.span(-9.6, -6.6, LANE[0] + 0.3, LANE[1] - 0.3, 0.05, 0.25, FB_LT)
    tiles(B, -9.6, -6.6, LANE[0] + 0.3, LANE[1] - 0.3, 0.3, 0.5, [PAVE, FB_LT], th=0.03)
    well(B, -8.1, 10.0, 0.3, r0=0.5, r1=0.95, h=0.75)
    for (px, py) in ((-6.9, 8.6), (-6.9, 11.3), (-9.4, 11.4)):
        pot(B, px, py, 0.3, 1.0)
    cart(B, 1.6, -22.0)
    cart(B, -1.6, 32.0, oxen=True)
    for k in range(5):
        pot(B, 2.2 + k * 0.5, 14.5, 0.06, 0.9, POT if k % 2 else POT_DK)
    m.add(2, B.obj("_props"), "well and carts")
    return m


# ---------------------------------------------------------------- House I, HR area

def hr_house():
    """32 x 26 m: two courts, a double entrance on the south, a ring of brick in the main court, a well room,
    bathing platform and chutes, an upper storey over the north-west (reconstructed)."""
    m = Model("hr-house")
    B = Batch("hrhouse")
    H = 4.4
    BIG = (-5.0, 1.5, 9.0, 8.5)
    EAST = (8.5, 3.5, 5.5, 5.0)
    WELLR = (11.5, -7.5, 2.6, 2.6)
    B.span(-16.2, 16.2, -13.2, 13.2, 0, 0.3, FB_DK)
    massing(B, -16, 16, -13, 13, [BIG, EAST, WELLR], H, FB, z=0.3)
    courses(B, -16, 16, -13, 13, 0.3, H + 0.3, FB_DK, every=0.42)
    court_fittings(B, BIG, 0.3, H, FB, doors={"N": [-7.0, -3.0], "S": [-5.0], "E": [0.0], "W": [3.0]})
    tiles(B, BIG[0] - BIG[2] / 2, BIG[0] + BIG[2] / 2, BIG[1] - BIG[3] / 2, BIG[1] + BIG[3] / 2, 0.4, 0.6, [PAVE, FB_LT, PAVE_DK],
          hole=(BIG[0] - 1.6, BIG[0] + 1.6, BIG[1] - 1.6, BIG[1] + 1.6))
    B.ring(BIG[0], BIG[1], 0.4, 1.0, 1.5, 0.45, FB_DK, seg=20)
    B.cyl(BIG[0], BIG[1], 0.4, 1.0, 0.2, EARTH_DK, seg=20)
    court_fittings(B, EAST, 0.3, H, FB, doors={"W": [3.5], "N": [8.5]})
    bath_platform(B, EAST[0] + 1.6, EAST[1] - 1.4, 0.4, 1.6, 1.6)
    well(B, WELLR[0], WELLR[1], 0.4, r0=0.45, r1=0.85, h=0.7)
    B.span(WELLR[0] - 1.3, WELLR[0] + 1.3, WELLR[1] - 1.3, WELLR[1] + 1.3, 0.3, 0.08, PAVE)
    m.add(0, B.obj("_walls"), "walls and courts")

    # double entrance with a central pier, side doors, chutes, a stair
    for u in (-6.3, -3.7):
        door(B, "S", -13.0, u, 0.3, 1.5, 2.8)
    B.box(-5.0, -13.35, 0.0, 0.9, 0.7, 3.6, FB_LT)
    for s in (-1, 1):
        B.box(-5.0 + s * 2.3, -13.45, 0.0, 0.9, 0.9, 3.8, FB_LT)
    B.span(-7.9, -2.1, -13.9, -13.0, 3.8, 0.35, FB_DK)
    door(B, "E", 16.0, 6.0, 0.3, 1.1, 2.4)
    door(B, "W", -16.0, -8.0, 0.3, 1.1, 2.4)
    for u in (2.5, 4.5):
        chute(B, "E", 16.0, u, 0.0, H * 0.6)
    chute(B, "W", -16.0, 6.0, 0.0, H + 2.8)
    for k in range(1, 10):
        B.span(-9.4, -8.6, -2.5, -2.5 + 5.0 * k / 9, 0.4, H * k / 9, FB_LT)
    m.add(1, B.obj("_entrance"), "entrance, stair and drains")

    top = H + 0.3
    parapet(B, -16, 16, -13, 13, top, FB_DK, t=0.35, h=0.55)
    B.span(-15.65, 15.65, -12.65, 12.65, top - 0.02, 0.04, ROOF)
    for x in (-12.0, 2.0, 6.0, 13.0):
        B.span(x - 0.12, x + 0.12, -12.6, 12.6, top, 0.28, ROOF_DK)
    for y in (-9.5, 9.0):
        B.span(-15.6, 15.6, y - 0.12, y + 0.12, top, 0.28, ROOF_DK)
    UX0, UX1, UY0, UY1 = -15.6, 3.5, 6.0, 12.6
    B.span(UX0, UX1, UY0, UY1, top, 2.8, FB)
    courses(B, UX0, UX1, UY0, UY1, top, top + 2.8, FB_DK, every=0.42, faces="SEW")
    parapet(B, UX0, UX1, UY0, UY1, top + 2.8, FB_DK, t=0.3, h=0.5)
    for u in (-12.0, -7.0, -2.0, 1.5):
        door(B, "S", UY0, u, top, 0.85, 1.9)
    for k in range(24):
        fbox(B, "S", UY0, UX0 + 0.4 + k * 0.8, top + 2.4, 0.12, 0.25, 0.12, TIMB)
    m.add(2, B.obj("_upper"), "roofs and upper storey")
    return m


# ---------------------------------------------------------------- a DK-G well

def dk_g_well():
    """10 x 10 m (shown at double scale): the round brick shaft, a paved platform with a curb and drain,
    pot stands, a trough, a bench and the corners of the houses round the well."""
    m = Model("dk-g-well")
    B = Batch("dkwell")
    B.span(-5, 5, -5, 5, 0, 0.05, EARTH)
    B.span(-4.0, 4.0, -4.0, 4.0, 0.05, 0.25, FB_DK)
    tiles(B, -3.8, 3.8, -3.8, 3.8, 0.3, 0.38, [PAVE, FB_LT, PAVE_DK, PAVE], hole=(-0.8, 0.8, -0.8, 0.8), th=0.035, gap=0.04)
    parapet(B, -4.0, 4.0, -4.0, 4.0, 0.3, FB, t=0.25, h=0.18)
    drain(B, 0.0, 3.8, 0.0, 5.0, z=0.05, w=0.5, h=0.25, color=FB, cover=False)
    drain(B, -3.6, 3.6, 3.6, 3.6, z=0.3, w=0.3, h=0.02, color=FB, cover=False)
    m.add(0, B.obj("_platform"), "platform")

    well(B, 0.0, 0.0, 0.3, r0=0.55, r1=1.1, h=0.85, n_courses=8, grooves=6)
    B.ring(0.0, 0.0, 1.15, 0.55, 1.15, 0.08, FB_LT, seg=16)
    for k in range(10):
        a = math.tau * k / 10
        B.box(1.13 * math.cos(a), 1.13 * math.sin(a), 0.32, 0.18, 0.3, 0.8, FB_DK, a)
    m.add(1, B.obj("_shaft"), "well shaft")

    for (sx, sy) in ((2.7, -2.6), (-2.7, -2.6)):
        B.box(sx, sy, 0.3, 0.7, 0.7, 0.5, FB)
        pot(B, sx, sy, 0.8, 1.2, POT)
    for k, (px, py) in enumerate(((1.1, 0.9), (-1.6, 2.4), (2.2, -1.2), (-2.4, -1.0), (1.8, 2.6))):
        pot(B, px, py, 0.31 if k else 1.23, 1.0 if k else 0.8, POT if k % 2 else POT_DK)
    B.box(2.8, 2.0, 0.3, 1.6, 0.6, 0.4, FB)
    B.box(2.8, 2.0, 0.65, 1.3, 0.35, 0.06, WATER_C)
    B.box(-3.5, 0.6, 0.3, 0.5, 3.4, 0.45, FB_LT)
    for (x0, x1, y0, y1) in ((-5.0, -4.3, 1.2, 5.0), (-5.0, -1.6, 4.3, 5.0), (4.3, 5.0, 1.8, 5.0), (1.6, 5.0, 4.3, 5.0), (-5.0, -4.3, -5.0, -2.0), (4.3, 5.0, -5.0, -2.4)):
        B.span(x0, x1, y0, y1, 0.0, 3.4, MB_LT)
        courses(B, x0, x1, y0, y1, 0.0, 3.4, shade(MB_LT, -0.1), every=0.5)
        B.span(x0 - 0.05, x1 + 0.05, y0 - 0.05, y1 + 0.05, 3.4, 0.35, shade(MB_LT, -0.06))
    chute(B, "E", -4.3, 2.4, 0.0, 2.6)
    chute(B, "S", 4.3, 3.0, 0.0, 2.2)
    m.add(2, B.obj("_props"), "pots and houses")
    return m


# ---------------------------------------------------------------- the "Priest-King" house

def priest_king_house():
    """24 x 20 m: a courtyard house with a south wall of ornamental brickwork, a niche, a well room,
    a bathing platform and an upper storey on the east."""
    m = Model("priest-king-house")
    B = Batch("pkhouse")
    H = 4.2
    COURT = (-1.5, 1.0, 7.0, 6.0)
    WELLR = (-8.5, 6.0, 2.4, 2.4)
    B.span(-12.2, 12.2, -10.2, 10.2, 0, 0.3, FB_DK)
    massing(B, -12, 12, -10, 10, [COURT, WELLR], H, FB, z=0.3)
    courses(B, -12, 12, -10, 10, 0.3, H + 0.3, FB_DK, every=0.42, faces="NEW")
    courses(B, 1.5, 12, -10, -10, 0.3, H + 0.3, FB_DK, every=0.42, faces="S")
    courses(B, -12, -9.5, -10, -10, 0.3, H + 0.3, FB_DK, every=0.42, faces="S")
    court_fittings(B, COURT, 0.3, H, FB, doors={"S": [-3.5], "E": [2.0], "W": [-0.5]})
    tiles(B, COURT[0] - COURT[2] / 2, COURT[0] + COURT[2] / 2, COURT[1] - COURT[3] / 2, COURT[1] + COURT[3] / 2, 0.4, 0.55, [PAVE, FB_LT, PAVE_DK])
    well(B, WELLR[0], WELLR[1], 0.4, r0=0.45, r1=0.85, h=0.7)
    bath_platform(B, COURT[0] + 2.6, COURT[1] - 2.0, 0.4, 1.6, 1.6)
    # the niche in the court's north wall
    fbox(B, "S", COURT[1] + COURT[3] / 2, COURT[0] + 0.8, 0.9, 1.0, 0.12, 1.6, DARK)
    fbox(B, "S", COURT[1] + COURT[3] / 2, COURT[0] + 0.8, 2.5, 1.5, 0.2, 0.2, FB_LT)
    fbox(B, "S", COURT[1] + COURT[3] / 2, COURT[0] + 0.8, 0.7, 1.5, 0.2, 0.2, FB_LT)
    m.add(0, B.obj("_walls"), "walls and court")

    # ornamental brickwork: a wall face of bricks set in a stepped, diamond-like pattern
    for r in range(18):
        z = 0.4 + r * 0.2
        for c in range(26):
            x = -9.3 + c * 0.42 + (0.21 if r % 2 else 0.0)
            if x > 1.3:
                continue
            d = abs((c % 6) - 3) == (r % 4) or (r % 4 == 0)
            fbox(B, "S", -10.0, x, z, 0.36, 0.08 if d else 0.04, 0.16, FB_LT if d else FB)
    fbox(B, "S", -10.0, -4.0, H + 0.0, 11.0, 0.16, 0.25, FB_DK)
    door(B, "W", -12.0, -5.0, 0.3, 1.1, 2.4)
    for u in (-2.0, 5.0):
        chute(B, "E", 12.0, u, 0.0, H * 0.6)
    for k in range(1, 9):
        B.span(4.0, 4.9, -6.0, -6.0 + 4.0 * k / 8, 0.3, H * k / 8, FB_LT)
    m.add(1, B.obj("_ornament"), "ornamental wall")

    top = H + 0.3
    parapet(B, -12, 12, -10, 10, top, FB_DK, t=0.3, h=0.5)
    B.span(-11.7, 11.7, -9.7, 9.7, top - 0.02, 0.04, ROOF)
    for x in (-6.0, 7.5):
        B.span(x - 0.12, x + 0.12, -9.6, 9.6, top, 0.28, ROOF_DK)
    UX0, UX1, UY0, UY1 = 5.0, 11.7, -9.7, 9.7
    B.span(UX0, UX1, UY0, UY1, top, 2.7, FB)
    courses(B, UX0, UX1, UY0, UY1, top, top + 2.7, FB_DK, every=0.42, faces="WNS")
    parapet(B, UX0, UX1, UY0, UY1, top + 2.7, FB_DK, t=0.3, h=0.45)
    for u in (-6.0, 0.0, 5.0):
        door(B, "W", UX0, u, top, 0.85, 1.9)
    m.add(2, B.obj("_upper"), "roofs and upper storey")
    return m


# ---------------------------------------------------------------- the Moneer workshops

def craft_quarter():
    """40 x 30 m: a walled yard with a brick storehouse, two updraft kilns, open sheds for bead-makers,
    shell-workers and potters, a well and a drain (a reconstruction)."""
    m = Model("craft-quarter")
    B = Batch("craft")
    B.span(-20, 20, -15, 15, 0, 0.06, EARTH)
    for (x, y, r) in ((12.0, 0.0, 3.0), (9.0, 6.0, 2.0)):
        B.cyl(x, y, 0.06, r, 0.02, EARTH_DK, seg=14)
    t, h = 0.6, 2.4
    for (x0, x1, y0, y1) in ((-20, -1.5, -15, -15 + t), (1.5, 20, -15, -15 + t), (-20, 20, 15 - t, 15), (-20, -20 + t, -15, 15), (20 - t, 20, -15, 15)):
        B.span(x0, x1, y0, y1, 0, h, MB)
        B.span(x0 - 0.05, x1 + 0.05, y0 - 0.05, y1 + 0.05, h, 0.2, MB_DK)
    for s in (-1, 1):
        B.box(s * 1.9, -14.7, 0, 0.9, 1.2, 3.0, FB)
    # storehouse
    SX0, SX1, SY0, SY1 = -18.8, 4.0, 5.5, 14.4
    massing(B, SX0, SX1, SY0, SY1, [(-7.5, 10.0, 4.0, 3.0)], 4.2, FB)
    courses(B, SX0, SX1, SY0, SY1, 0, 4.2, FB_DK, every=0.42)
    for k in range(9):
        fbox(B, "S", SY0, SX0 + 1.0 + k * 2.6, 0, 0.6, 0.4, 4.0, FB_DK)
    for u in (-14.0, -2.5):
        door(B, "S", SY0 - 0.4, u + 1.3, 0, 1.4, 2.4)
    court_fittings(B, (-7.5, 10.0, 4.0, 3.0), 0.0, 4.2, FB, doors={"S": [-7.5]})
    # well and drain
    B.span(-3.5, -0.5, -5.5, -2.5, 0.06, 0.2, FB_LT)
    well(B, -2.0, -4.0, 0.26, r0=0.45, r1=0.85, h=0.7)
    drain(B, -2.0, -5.5, -2.0, -14.4, z=0.06, w=0.5, h=0.22, color=FB, holes=(5,))
    m.add(0, B.obj("_yard"), "yard and storehouse")

    # kilns
    for (kx, ky) in ((12.0, 9.0), (15.5, 3.0)):
        B.cyl(kx, ky, 0.06, 1.9, 1.4, FB_DK, seg=16)
        B.cyl(kx, ky, 1.46, 1.75, 1.3, MB_DK, seg=16, r_top=1.0)
        B.cyl(kx, ky, 2.76, 1.0, 0.02, DARK, seg=16)
        B.box(kx, ky - 1.9, 0.06, 0.8, 0.5, 0.75, DARK)
        B.box(kx, ky - 2.6, 0.06, 1.4, 1.2, 0.1, EARTH_DK)
    for k in range(12):
        B.box(17.5 + (k % 3) * 0.12, 8.0 + (k // 3) * 0.12, 0.06 + (k % 4) * 0.12, 0.08, 2.0, 0.08, TIMB, 0.2 * (k % 3))
    for k in range(10):
        B.cyl(9.0 + (k % 5) * 0.5, 12.6 + (k // 5) * 0.5, 0.06 + (k // 5) * 0.06, 0.22, 0.06, EARTH_DK, seg=8)
    # sheds on posts
    for (x0, x1, y0, y1) in ((-18.8, -8.0, -13.8, -3.0), (4.0, 14.0, -13.8, -6.5)):
        nx, ny = int((x1 - x0) / 3.5) + 1, int((y1 - y0) / 3.5) + 1
        for i in range(nx):
            for j in range(ny):
                B.box(x0 + (x1 - x0) * i / (nx - 1), y0 + (y1 - y0) * j / (ny - 1), 0.06, 0.22, 0.22, 2.6, TIMB)
    # bead-makers' and shell-workers' benches, heaps
    for k in range(4):
        B.box(-16.5 + k * 2.6, -8.0, 0.06, 1.6, 0.6, 0.45, FB_LT)
        for j in range(3):
            B.box(-17.0 + k * 2.6 + j * 0.4, -8.0, 0.51, 0.1, 0.1, 0.06, CARNELIAN)
    for (hx, hy) in ((-12.0, -11.5), (-16.0, -12.0)):
        B.cyl(hx, hy, 0.06, 1.0, 0.5, SHELL, seg=10, r_top=0.3)
    B.cyl(-9.6, -4.5, 0.06, 0.7, 0.4, CARNELIAN, seg=8, r_top=0.2)
    for k in range(3):
        B.cyl(6.0 + k * 2.6, -9.0, 0.06, 0.45, 0.5, TIMB, seg=12)
    for k in range(18):
        pot(B, 5.5 + (k % 9) * 0.85, -12.2 - (k // 9) * 0.8, 0.06, 1.0, POT if k % 3 else POT_DK)
    m.add(1, B.obj("_work"), "kilns and workshops")

    for (x0, x1, y0, y1) in ((-18.8, -8.0, -13.8, -3.0), (4.0, 14.0, -13.8, -6.5)):
        B.span(x0 - 0.5, x1 + 0.5, y0 - 0.5, y1 + 0.5, 2.66, 0.18, REED)
        for k in range(int((x1 - x0 + 1.0) / 0.9)):
            B.span(x0 - 0.4 + k * 0.9, x0 - 0.3 + k * 0.9, y0 - 0.5, y1 + 0.5, 2.84, 0.06, shade(REED, -0.1))
    parapet(B, SX0, SX1, SY0, SY1, 4.2, FB_DK, t=0.3, h=0.5)
    B.span(SX0 + 0.3, SX1 - 0.3, SY0 + 0.3, SY1 - 0.3, 4.18, 0.04, ROOF)
    for x in (-13.0, -2.0):
        B.span(x - 0.12, x + 0.12, SY0 + 0.3, SY1 - 0.3, 4.2, 0.28, ROOF_DK)
    for k in range(10):
        fbox(B, "S", SY0, SX0 + 1.2 + k * 2.3, 3.9, 0.2, 0.5, 0.2, TIMB)
    m.add(2, B.obj("_roofs"), "roofs")
    return m


# ---------------------------------------------------------------- the Kushan stupa and monastery

def kushan_stupa():
    """60 x 45 m on the Citadel mound: the stupa on a square terrace in a walled court (west), votive stupas,
    the monastery's cells round a court with a verandah (east)."""
    m = Model("stupa")
    B = Batch("stupa")
    B.span(-30, 30, -22.5, 22.5, 0, 0.4, "#B39A76")
    for k in range(14):
        B.box(-28 + rnd(k, 1) * 56, -21 + rnd(k, 2) * 42, 0.4, 0.6 + rnd(k, 3), 0.4 + rnd(k, 4), 0.08, FB_DK, rnd(k, 5) * 3)
    Z = 0.4
    # the stupa court wall with gates east and south
    t, h = 0.7, 2.4
    for (x0, x1, y0, y1) in ((-29, -1, -21, -21 + t), (-29, -1, 21 - t, 21), (-29, -29 + t, -21, 21), (-1 - t, -1, -21, -1.6), (-1 - t, -1, 1.6, 21)):
        B.span(x0, x1, y0, y1, Z, h, MB)
        B.span(x0 - 0.05, x1 + 0.05, y0 - 0.05, y1 + 0.05, Z + h, 0.18, MB_DK)
    for s in (-1, 1):
        B.box(-1.35, s * 2.0, Z, 1.0, 1.0, 3.0, PLASTER_K_DK)
    courses(B, -29, -1, -21, 21, Z, Z + h, MB_DK, every=0.4, out=0.03)
    for k in range(40):
        B.box(-28.2 + k * 0.7, -20.3, Z + h + 0.18, 0.3, 0.5, 0.25, MB_DK)
        B.box(-28.2 + k * 0.7, 20.3, Z + h + 0.18, 0.3, 0.5, 0.25, MB_DK)
    # the terrace, with pilasters and a cornice, and its stair on the east
    TX, TS, TH = -15.5, 15.0, 3.2
    B.box(TX, 0, Z, TS, TS, TH, PLASTER_K)
    B.box(TX, 0, Z, TS + 0.5, TS + 0.5, 0.4, PLASTER_K_DK)
    B.box(TX, 0, Z + TH - 0.3, TS + 0.4, TS + 0.4, 0.3, PLASTER_K_DK)
    for k in range(9):
        u = -TS / 2 + 0.8 + k * (TS - 1.6) / 8
        for face, fixed in (("S", -TS / 2), ("N", TS / 2)):
            fbox(B, face, fixed, TX + u, Z + 0.4, 0.4, 0.15, TH - 0.7, PLASTER_K_DK)
        fbox(B, "W", TX - TS / 2, u, Z + 0.4, 0.4, 0.15, TH - 0.7, PLASTER_K_DK)
        if abs(u) > 2.0:
            fbox(B, "E", TX + TS / 2, u, Z + 0.4, 0.4, 0.15, TH - 0.7, PLASTER_K_DK)
    n = 10
    for k in range(1, n + 1):
        B.span(TX + TS / 2, TX + TS / 2 + 3.6 * (n - k + 1) / n, -1.6, 1.6, Z, TH * k / n, PLASTER_K if k % 2 else PLASTER_K_DK)
    B.ring(TX, 0, Z + TH, 5.9, 6.6, 0.12, PLASTER_K_DK, seg=24)
    # monastery: cells round a court, verandah, doors
    MX0, MX1, MY0, MY1 = 2.0, 29.0, -14.0, 14.0
    COURT = (15.5, 0.0, 18.0, 19.0)
    massing(B, MX0, MX1, MY0, MY1, [COURT], 3.6, PLASTER_K, z=Z)
    B.span(COURT[0] - COURT[2] / 2, COURT[0] + COURT[2] / 2, -COURT[3] / 2, COURT[3] / 2, Z, 0.08, EARTH)
    tiles(B, COURT[0] - COURT[2] / 2 + 2.2, COURT[0] + COURT[2] / 2 - 2.2, -COURT[3] / 2 + 2.2, COURT[3] / 2 - 2.2, Z + 0.08, 0.8, [PAVE, FB_LT, PAVE_DK], hole=(14.5, 16.5, 2.0, 4.0))
    tiles(B, TX - TS / 2 + 0.3, TX + TS / 2 - 0.3, -TS / 2 + 0.3, TS / 2 - 0.3, Z + TH, 0.75, [PLASTER_K, PLASTER_K_DK], hole=(TX - 6.0, TX + 6.0, -6.0, 6.0))
    cx0, cx1, cy0, cy1 = COURT[0] - COURT[2] / 2, COURT[0] + COURT[2] / 2, -COURT[3] / 2, COURT[3] / 2
    for face, fixed, a0, a1 in (("N", cy0, cx0, cx1), ("S", cy1, cx0, cx1), ("E", cx0, cy0, cy1), ("W", cx1, cy0, cy1)):
        n = int((a1 - a0) / 2.6)
        for k in range(n):
            door(B, face, fixed, a0 + (a1 - a0) * (k + 0.5) / n, Z + 0.08, 0.9, 1.9)
    door(B, "W", MX0, 0.0, Z, 1.4, 2.4)
    for s in (-1, 1):
        B.box(MX0 - 0.4, s * 1.3, Z, 0.8, 0.6, 3.0, PLASTER_K_DK)
    well(B, 15.5, 3.0, Z + 0.08, r0=0.45, r1=0.85, h=0.7)
    courses(B, MX0, MX1, MY0, MY1, Z, Z + 3.6, PLASTER_K_DK, every=0.9, out=0.03)
    m.add(0, B.obj("_terrace"), "terrace, court and monastery walls")

    # ---- the stupa and votive stupas
    s = stupa("stupa_main", 5.0, (TX, 0, Z + TH), color=PLASTER_K, drum=0.3, rail=False, gateways=0, harmika=True, umbrellas=3, base_color=PLASTER_K_DK)
    for (vx, vy) in ((-25.0, -16.0), (-25.0, 16.0), (-6.0, -16.0), (-6.0, 16.0), (-25.5, 0.0), (-15.5, -17.5), (-15.5, 17.5)):
        B.box(vx, vy, Z, 1.8, 1.8, 0.7, PLASTER_K_DK)
        B.cyl(vx, vy, Z + 0.7, 0.75, 0.35, PLASTER_K, seg=14)
        B.cyl(vx, vy, Z + 1.05, 0.75, 0.45, PLASTER_K, seg=14, r_top=0.55)
        B.cyl(vx, vy, Z + 1.5, 0.55, 0.3, PLASTER_K, seg=14, r_top=0.15)
        B.box(vx, vy, Z + 1.75, 0.28, 0.28, 0.2, PLASTER_K_DK)
        B.cyl(vx, vy, Z + 1.95, 0.04, 0.4, TIMB, seg=6)
        B.cyl(vx, vy, Z + 2.25, 0.25, 0.05, PLASTER_K_DK, seg=10)
    m.add(1, join([s, B.obj("_votive")], "stupa_all"), "stupa")

    # ---- monastery roofs, verandah
    vz = Z + 3.0
    ix0, ix1, iy0, iy1 = cx0 + 2.0, cx1 - 2.0, cy0 + 2.0, cy1 - 2.0
    for x0, x1, y0, y1 in ((cx0, cx1, cy0, iy0), (cx0, cx1, iy1, cy1), (cx0, ix0, iy0, iy1), (ix1, cx1, iy0, iy1)):
        B.span(x0, x1, y0, y1, vz, 0.22, ROOF)
    for k in range(8):
        for (x, y) in ((ix0 + (ix1 - ix0) * k / 7, iy0), (ix0 + (ix1 - ix0) * k / 7, iy1)):
            B.box(x, y, Z, 0.24, 0.24, 3.0, TIMB)
    for k in range(1, 7):
        for (x, y) in ((ix0, iy0 + (iy1 - iy0) * k / 7), (ix1, iy0 + (iy1 - iy0) * k / 7)):
            B.box(x, y, Z, 0.24, 0.24, 3.0, TIMB)
    parapet(B, MX0, MX1, MY0, MY1, Z + 3.6, PLASTER_K_DK, t=0.3, h=0.5)
    for x0, x1, y0, y1 in ((MX0 + 0.3, MX1 - 0.3, MY0 + 0.3, cy0), (MX0 + 0.3, MX1 - 0.3, cy1, MY1 - 0.3), (MX0 + 0.3, cx0, cy0, cy1), (cx1, MX1 - 0.3, cy0, cy1)):
        B.span(x0, x1, y0, y1, Z + 3.58, 0.03, ROOF)
    for k in range(10):
        x = MX0 + 2.6 * (k + 0.5)
        B.span(x - 0.1, x + 0.1, MY0 + 0.3, cy0, Z + 3.6, 0.25, ROOF_DK)
        B.span(x - 0.1, x + 0.1, cy1, MY1 - 0.3, Z + 3.6, 0.25, ROOF_DK)
    for k in range(7):
        y = cy0 + 2.6 * (k + 0.5)
        B.span(MX0 + 0.3, cx0, y - 0.1, y + 0.1, Z + 3.6, 0.25, ROOF_DK)
        B.span(cx1, MX1 - 0.3, y - 0.1, y + 0.1, Z + 3.6, 0.25, ROOF_DK)
    m.add(2, B.obj("_roofs"), "monastery roofs")
    return m


BUILDERS = {
    "mohenjo-daro/great-bath": great_bath,
    "mohenjo-daro/great-hall": great_hall,
    "mohenjo-daro/college": college,
    "mohenjo-daro/pillared-hall": pillared_hall,
    "mohenjo-daro/citadel-platform": citadel_platform,
    "mohenjo-daro/southern-defences": southern_defences,
    "mohenjo-daro/main-street": main_street,
    "mohenjo-daro/hr-house": hr_house,
    "mohenjo-daro/dk-g-well": dk_g_well,
    "mohenjo-daro/priest-king-house": priest_king_house,
    "mohenjo-daro/craft-quarter": craft_quarter,
    "mohenjo-daro/stupa": kushan_stupa,
}
