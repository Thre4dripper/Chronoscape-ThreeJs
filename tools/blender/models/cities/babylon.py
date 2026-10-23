"""Babylon landmark miniatures: the Ishtar Gate and Processional Way, the palaces, Etemenanki and Esagila,
the bridge on stone piers, the outer wall, the neighbourhood temples and the Hellenistic theatre.

Conventions as in FORMAT.md: metres, origin at the ground centre, +X east, +Y north, main front toward -Y
unless a builder says otherwise; the landmark rotation turns it on the map. Most geometry is collected in a
Batch (one mesh per colour) so that glazed friezes of hundreds of beasts stay quick to build.
"""
import math
from chronokit import Model, box, cylinder, dome, join, shade, mesh_from
from worldkit import *

BAKED, BAKED_LT, BAKED_DK = "#B8956A", "#C8A87E", "#9A7A54"
MUD, MUD_LT, MUD_DK = "#BFA27A", "#D2BC96", "#A88B64"
WHITE_PL = "#E8E0CB"
GLZ, GLZ_DK, GLZ_LT = "#2A4E95", "#1F3E7A", "#4A72B8"
BEAST_Y, BEAST_W, BEAST_O, HORN = "#E0BA4C", "#F1EBD8", "#C57A38", "#3E9A8E"
PAVE, PAVE_RED, EARTH = "#DCD0B6", "#A6604A", "#B9A27C"
SOIL, LEAF, PALM_C = "#7E6A48", "#6F8A4E", "#6A8A50"
STONE_DK, LIME = "#45413B", "#D3C7AC"
BOX_FACES = [(0, 3, 2, 1), (4, 5, 6, 7), (0, 1, 5, 4), (1, 2, 6, 5), (2, 3, 7, 6), (3, 0, 4, 7)]


# ---------------------------------------------------------------- batched geometry

class Batch:
    """Collects boxes and prisms per colour and emits one mesh per colour (fast for thousands of parts)."""

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
        """Box between two corners."""
        self.box((x0 + x1) / 2, (y0 + y1) / 2, z, abs(x1 - x0), abs(y1 - y0), h, color)

    def frustum(self, cx, cy, z, w0, d0, w1, d1, h, color):
        v = [(cx - w0 / 2, cy - d0 / 2, z), (cx + w0 / 2, cy - d0 / 2, z), (cx + w0 / 2, cy + d0 / 2, z), (cx - w0 / 2, cy + d0 / 2, z),
             (cx - w1 / 2, cy - d1 / 2, z + h), (cx + w1 / 2, cy - d1 / 2, z + h), (cx + w1 / 2, cy + d1 / 2, z + h), (cx - w1 / 2, cy + d1 / 2, z + h)]
        self._add(color, v, BOX_FACES)

    def poly(self, pts, z, h, color):
        n = len(pts)
        v = [(x, y, z) for x, y in pts] + [(x, y, z + h) for x, y in pts]
        f = [tuple(range(n))[::-1], tuple(range(n, 2 * n))] + [(i, (i + 1) % n, n + (i + 1) % n, n + i) for i in range(n)]
        self._add(color, v, f)

    def sector(self, cx, cy, r0, r1, a0, a1, z, h, color, seg=16):
        """An annular sector (a slice of a ring) from angle a0 to a1, extruded up by h."""
        outer = [(cx + r1 * math.cos(a0 + (a1 - a0) * i / seg), cy + r1 * math.sin(a0 + (a1 - a0) * i / seg)) for i in range(seg + 1)]
        inner = [(cx + r0 * math.cos(a0 + (a1 - a0) * i / seg), cy + r0 * math.sin(a0 + (a1 - a0) * i / seg)) for i in range(seg + 1)]
        self.poly(outer + inner[::-1], z, h, color)

    def obj(self, suffix=""):
        self.k += 1
        objs = [mesh_from(f"{self.name}{suffix}_{self.k}_{i}", v, f, (0, 0, 0), col) for i, (col, (v, f)) in enumerate(self.geo.items()) if v]
        self.geo = {}
        return join(objs, f"{self.name}{suffix}_{self.k}")


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


# relief beasts in units of length L and height H, facing +u: (u offset, z offset, length, height, accent?)
BEASTS = {
    "dragon": [(0.0, 0.30, 0.46, 0.22, 0), (0.25, 0.44, 0.10, 0.40, 0), (0.33, 0.80, 0.22, 0.12, 0), (0.31, 0.92, 0.04, 0.12, 1),
               (-0.30, 0.40, 0.18, 0.07, 0), (-0.40, 0.40, 0.05, 0.30, 0), (0.17, 0.0, 0.06, 0.31, 0), (-0.16, 0.0, 0.07, 0.31, 0),
               (-0.16, 0.0, 0.15, 0.05, 1)],
    "bull": [(0.0, 0.30, 0.52, 0.32, 0), (0.22, 0.45, 0.14, 0.24, 0), (0.33, 0.47, 0.12, 0.22, 0), (0.31, 0.69, 0.04, 0.17, 1),
             (0.37, 0.69, 0.03, 0.12, 1), (0.20, 0.0, 0.06, 0.31, 0), (0.12, 0.0, 0.06, 0.31, 0), (-0.14, 0.0, 0.06, 0.31, 0),
             (-0.21, 0.0, 0.06, 0.31, 0), (-0.28, 0.24, 0.03, 0.30, 0)],
    "lion": [(-0.02, 0.30, 0.50, 0.25, 0), (0.20, 0.30, 0.16, 0.42, 1), (0.32, 0.50, 0.12, 0.20, 0), (0.20, 0.0, 0.06, 0.31, 0),
             (0.11, 0.0, 0.06, 0.31, 0), (-0.14, 0.0, 0.06, 0.31, 0), (-0.22, 0.0, 0.06, 0.31, 0), (-0.32, 0.47, 0.11, 0.04, 0),
             (-0.38, 0.47, 0.04, 0.10, 1)],
}
BEAST_COLORS = {"dragon": (BEAST_W, BEAST_Y), "bull": (BEAST_Y, HORN), "lion": (BEAST_W, BEAST_Y), "lion2": (BEAST_Y, BEAST_O)}


def frieze(B, face, fixed, u0, u1, z, kind, L=2.6, H=1.9, dirn=1, dn=0.32, gap=0.45, off=0.0, alt=False):
    """A row of raised glazed beasts along a wall face between u0 and u1, walking toward +u (dirn=1) or -u."""
    n = max(1, int((u1 - u0) / (L + gap)))
    step = (u1 - u0) / n
    for i in range(n):
        uc = u0 + step * (i + 0.5)
        ck = "lion2" if (alt and kind == "lion" and i % 2) else kind
        body, acc = BEAST_COLORS[ck]
        for du_o, zo, du, hh, a in BEASTS[kind]:
            fbox(B, face, fixed, uc + dirn * du_o * L, z + zo * H, du * L, dn * (1.25 if a else 1.0), hh * H, acc if a else body, off)


def rosettes(B, face, fixed, u0, u1, z, size=0.5, gap=0.35, off=0.0, band=True):
    """A band of white-and-yellow rosettes (shown as raised squares) on a glazed face."""
    if band:
        fbox(B, face, fixed, (u0 + u1) / 2, z - 0.12, u1 - u0, 0.06, size + 0.24, GLZ_DK, off)
    n = max(1, int((u1 - u0) / (size + gap)))
    step = (u1 - u0) / n
    for i in range(n):
        u = u0 + step * (i + 0.5)
        fbox(B, face, fixed, u, z, size, 0.14, size, BEAST_W, off)
        fbox(B, face, fixed, u, z + size * 0.3, size * 0.4, 0.22, size * 0.4, BEAST_Y, off)


def crenel_line(B, ax, ay, bx, by, z, size, color, t=None):
    """Babylonian stepped crenellations (three steps) along a wall top from (ax, ay) to (bx, by)."""
    L = math.hypot(bx - ax, by - ay)
    a = math.atan2(by - ay, bx - ax)
    t = t or size * 0.7
    n = max(1, int(L / (size * 1.3)))
    for i in range(n):
        f = (i + 0.5) / n
        x, y = ax + (bx - ax) * f, ay + (by - ay) * f
        B.box(x, y, z, size, t, size * 0.42, color, a)
        B.box(x, y, z + size * 0.42, size * 0.64, t, size * 0.38, color, a)
        B.box(x, y, z + size * 0.8, size * 0.3, t, size * 0.34, color, a)


def crenel_rect(B, cx, cy, w, d, z, size, color, inset=None):
    i = size * 0.4 if inset is None else inset
    x0, x1, y0, y1 = cx - w / 2 + i, cx + w / 2 - i, cy - d / 2 + i, cy + d / 2 - i
    for (ax, ay), (bx, by) in (((x0, y0), (x1, y0)), ((x1, y0), (x1, y1)), ((x1, y1), (x0, y1)), ((x0, y1), (x0, y0))):
        crenel_line(B, ax, ay, bx, by, z, size, color)


def buttresses(B, face, fixed, u0, u1, z, h, every, bw, dn, color, groove=True, skip=(), off=0.0):
    """Toothed buttresses with a recessed groove in each, the signature of Babylonian temple and palace walls.
    A negative `off` sinks them into a battered (sloping) wall so that they stay attached to it all the way up."""
    n = max(1, int((u1 - u0) / every))
    step = (u1 - u0) / n
    for i in range(n + 1):
        u = u0 + step * i
        if any(a <= u <= b for a, b in skip):
            continue
        fbox(B, face, fixed, u, z, bw, dn - off, h, color, off)
        if groove:
            fbox(B, face, fixed, u, z + h * 0.06, bw * 0.28, 0.08, h * 0.82, shade(color, -0.28), dn)


def rect_walls(B, cx, cy, w, d, t, z, h, color):
    B.box(cx, cy - d / 2 + t / 2, z, w, t, h, color)
    B.box(cx, cy + d / 2 - t / 2, z, w, t, h, color)
    B.box(cx - w / 2 + t / 2, cy, z, t, d - 2 * t, h, color)
    B.box(cx + w / 2 - t / 2, cy, z, t, d - 2 * t, h, color)


def all_buttresses(B, cx, cy, w, d, z, h, every, bw, dn, color, skip=None):
    """Buttresses on all four outer faces of a w x d block; skip = {face: [(u0, u1), ...]} for gates."""
    skip = skip or {}
    buttresses(B, "S", cy - d / 2, cx - w / 2, cx + w / 2, z, h, every, bw, dn, color, skip=skip.get("S", ()))
    buttresses(B, "N", cy + d / 2, cx - w / 2, cx + w / 2, z, h, every, bw, dn, color, skip=skip.get("N", ()))
    buttresses(B, "W", cx - w / 2, cy - d / 2, cy + d / 2, z, h, every, bw, dn, color, skip=skip.get("W", ()))
    buttresses(B, "E", cx + w / 2, cy - d / 2, cy + d / 2, z, h, every, bw, dn, color, skip=skip.get("E", ()))


def tower_pair(B, face, fixed, u, gap, tw, proj, depth_in, z, h, color, crown=None, size=0.9):
    """Two gate towers flanking position u on a wall face, projecting `proj` and sunk `depth_in` into the wall."""
    nx, ny = {"S": (0, -1), "N": (0, 1), "E": (1, 0), "W": (-1, 0)}[face]
    for s in (-1, 1):
        uu = u + s * gap
        fbox(B, face, fixed, uu, z, tw, proj + depth_in, h, color, -depth_in)
        if crown:
            c = fixed + (proj - depth_in) / 2
            cx, cy = (uu, c) if face in ("S", "N") else (c, uu)
            if face in ("S", "W"):
                cx, cy = (uu, fixed - (proj - depth_in) / 2) if face == "S" else (fixed - (proj - depth_in) / 2, uu)
            wx, wy = (tw, proj + depth_in) if face in ("S", "N") else (proj + depth_in, tw)
            crenel_rect(B, cx, cy, wx, wy, z + h, size, crown, inset=size * 0.35)


def door(B, face, fixed, u, z, w, h, color=DARK):
    fbox(B, face, fixed, u, z, w, 0.25, h, color)


def stepped_ramp(B, x0, x1, y0, y1, z0, z1, n, color, axis="y", parapet=None):
    """A solid flight of n steps climbing from (x0|y0, z0) to (x1|y1, z1) along the axis; each tread runs to the far end."""
    rise = (z1 - z0) / n
    for i in range(n):
        if axis == "y":
            ya = y0 + (y1 - y0) * i / n
            B.span(x0, x1, ya, y1, z0 + rise * i, rise, color)
            if parapet:
                for xe in (x0, x1):
                    B.box(xe, (ya + y1) / 2, z0 + rise * i, 0.9, abs(y1 - ya), rise + 1.0, parapet)
        else:
            xa = x0 + (x1 - x0) * i / n
            B.span(xa, x1, y0, y1, z0 + rise * i, rise, color)
            if parapet:
                ye = y0 if abs(y0) > abs(y1) else y1
                B.box((xa + x1) / 2, ye, z0 + rise * i, abs(x1 - xa), 0.9, rise + 1.0, parapet)


def court_unit(B, x0, x1, y0, y1, court, h, color, rib_every=3.2, door_every=9.0, roof_div=12.0, skip=None):
    """Ranges of rooms filling a rectangle round one open court (cx, cy, cw, cd): ribbed court facades, doors, roof divisions."""
    cx, cy, cw, cd = court
    cx0, cx1, cy0, cy1 = cx - cw / 2, cx + cw / 2, cy - cd / 2, cy + cd / 2
    hs = [h, h * 0.92, h * 1.06, h * 0.96]
    B.span(x0, x1, cy1, y1, 0, hs[0], color)                       # north range
    B.span(x0, x1, y0, cy0, 0, hs[1], shade(color, -0.03))         # south range
    B.span(x0, cx0, cy0, cy1, 0, hs[2], shade(color, 0.03))        # west range
    B.span(cx1, x1, cy0, cy1, 0, hs[3], color)                     # east range
    B.span(cx0, cx1, cy0, cy1, 0, 0.35, PAVE)                      # court paving
    skip = skip or {}
    for face, fixed, u0, u1, hh in (("S", cy1, cx0, cx1, hs[0]), ("N", cy0, cx0, cx1, hs[1]), ("E", cx0, cy0, cy1, hs[2]), ("W", cx1, cy0, cy1, hs[3])):
        sk = skip.get(face, ())
        buttresses(B, face, fixed, u0 + 1, u1 - 1, 0, hh, rib_every, 0.9, 0.45, shade(color, 0.05), groove=False, skip=sk)
        k = max(1, int((u1 - u0) / door_every))
        for j in range(k):
            u = u0 + (u1 - u0) * (j + 0.5) / k
            if not any(a <= u <= b for a, b in sk):
                door(B, face, fixed, u, 0.35, 1.8, 3.4)
    # roof divisions (room walls standing above the flat roofs) and dark light-wells
    for (a0, a1, b0, b1, hh) in ((x0, x1, cy1, y1, hs[0]), (x0, x1, y0, cy0, hs[1])):
        n = max(1, int((a1 - a0) / roof_div))
        for j in range(1, n):
            B.box(a0 + (a1 - a0) * j / n, (b0 + b1) / 2, hh, 0.7, abs(b1 - b0), 0.6, shade(color, -0.06))
        if abs(b1 - b0) > 14 and (a1 - a0) > 20:
            B.box(a0 + (a1 - a0) * 0.3, (b0 + b1) / 2, hh, 4.5, 4.5, 0.08, shade(color, -0.45))
            B.box(a0 + (a1 - a0) * 0.72, (b0 + b1) / 2, hh, 4.0, 4.0, 0.08, shade(color, -0.45))


def arch(name, w, h, loc, face="S", depth=0.4):
    return arch_panel(name, w, h, loc, face, DARK, False, depth)


# ---------------------------------------------------------------- the Ishtar Gate

def ishtar_gate():
    """The double gate: the smaller outer gate (in Nemetti-Enlil) in front of the taller main gate (in Imgur-Enlil).
    Built with its outer front toward -Y; the landmark is turned 180 degrees so that the front faces north."""
    m = Model("ishtar-gate")
    B = Batch("ig")
    B.box(0, 0, 0, 50, 52, 0.25, EARTH)
    B.box(0, 0, 0.25, 12, 52, 0.3, PAVE)
    for s in (-1, 1):
        B.box(s * 6.6, 0, 0.25, 1.2, 52, 0.32, PAVE_RED)
        B.span(s * 16, s * 25, -17, -13, 0.25, 11, BAKED)            # Nemetti-Enlil stubs
        B.span(s * 20, s * 25, 4.5, 11.5, 0.25, 15, BAKED_DK)        # Imgur-Enlil stubs
    m.add(0, B.obj("_ground"), "walls")

    # outer gate
    for s in (-1, 1):
        B.box(s * 11, -15, 0, 10, 13, 17, GLZ)
        B.box(s * 11, -15, 0, 10.4, 13.4, 1.0, GLZ_DK)
    B.box(0, -15, 0, 12, 10, 13, GLZ)
    rows = [1.6 + 2.3 * k for k in range(6)]
    for k, z in enumerate(rows):
        kind = "bull" if k % 2 == 0 else "dragon"
        frieze(B, "S", -21.5, -15.6, -6.4, z, kind, dirn=1)
        frieze(B, "S", -21.5, 6.4, 15.6, z, kind, dirn=-1)
        frieze(B, "W", -16, -21, -9, z, kind, dirn=-1)
        frieze(B, "E", 16, -21, -9, z, kind, dirn=-1)
    for k, z in enumerate((8.9, 10.9)):
        kind = "dragon" if k else "bull"
        frieze(B, "S", -20, -5.8, -0.3, z, kind, L=2.2, H=1.5, dirn=1)
        frieze(B, "S", -20, 0.3, 5.8, z, kind, L=2.2, H=1.5, dirn=-1)
    rosettes(B, "S", -21.5, -15.7, -6.3, 15.1)
    rosettes(B, "S", -21.5, 6.3, 15.7, 15.1)
    rosettes(B, "S", -20, -5.8, 5.8, 12.6, size=0.32, gap=0.25)
    g1 = B.obj("_outer")
    m.add(1, join([g1, arch("ig_a1", 5, 8.5, (0, -20.05, 0), "S"), arch("ig_a2", 5, 8.5, (0, -9.95, 0), "N")], "ig_outer"), "outer gate")

    # main gate
    for s in (-1, 1):
        B.box(s * 13.5, 8, 0, 13, 26, 26, GLZ)
        B.box(s * 13.5, 8, 0, 13.4, 26.4, 1.0, GLZ_DK)
    B.box(0, 8, 0, 14, 22, 21, GLZ)
    for k in range(10):
        z = 1.6 + 2.3 * k
        kind = "bull" if k % 2 == 0 else "dragon"
        frieze(B, "W", -20, -4.6, 20.6, z, kind, dirn=-1)
        frieze(B, "E", 20, -4.6, 20.6, z, kind, dirn=-1)
        if k < 9:
            frieze(B, "N", 21, -19.6, -7.4, z, kind, dirn=-1)
            frieze(B, "N", 21, 7.4, 19.6, z, kind, dirn=1)
        if z > 16:
            frieze(B, "S", -5, -19.6, -7.4, z, kind, dirn=1)
            frieze(B, "S", -5, 7.4, 19.6, z, kind, dirn=-1)
    for k, z in enumerate((13.6, 15.9, 18.2)):
        kind = "bull" if k % 2 == 0 else "dragon"
        frieze(B, "S", -3, -6.8, -0.3, z, kind, L=2.3, H=1.7, dirn=1)
        frieze(B, "S", -3, 0.3, 6.8, z, kind, L=2.3, H=1.7, dirn=-1)
    for face, fixed, u0, u1 in (("S", -5, -19.8, -7.2), ("S", -5, 7.2, 19.8), ("N", 21, -19.8, -7.2), ("N", 21, 7.2, 19.8), ("W", -20, -4.8, 20.8), ("E", 20, -4.8, 20.8)):
        rosettes(B, face, fixed, u0, u1, 24.4)
    g2 = B.obj("_main")
    m.add(2, join([g2, arch("ig_a3", 5.5, 11, (0, -3.05, 0), "S"), arch("ig_a4", 5.5, 11, (0, 19.05, 0), "N")], "ig_main"), "main gate")

    # stepped crenellations
    for s in (-1, 1):
        crenel_rect(B, s * 11, -15, 10, 13, 17, 1.1, GLZ_LT)
        crenel_rect(B, s * 13.5, 8, 13, 26, 26, 1.2, GLZ_LT)
        crenel_line(B, s * 16.4, -15, s * 25, -15, 11.25, 0.9, BAKED_LT)
        crenel_line(B, s * 20.4, 8, s * 25, 8, 15.25, 1.0, BAKED_LT)
    crenel_rect(B, 0, -15, 12, 10, 13, 1.0, GLZ_LT)
    crenel_rect(B, 0, 8, 14, 22, 21, 1.1, GLZ_LT)
    m.add(3, B.obj("_crown"), "crenellations")
    return m


# ---------------------------------------------------------------- the Processional Way north of the gate

def processional_way():
    """The walled street with its glazed lions, running north-south (Y) 170 m; the lions walk south toward the gate."""
    m = Model("processional-way")
    B = Batch("pw")
    B.box(0, 0, 0, 36, 170, 0.2, EARTH)
    B.box(0, 0, 0.2, 14, 170, 0.45, PAVE)
    for s in (-1, 1):
        B.box(s * 8.5, 0, 0.2, 3, 170, 0.42, PAVE_RED)
    for j in range(-8, 9):
        B.box(0, j * 10, 0.65, 14, 0.12, 0.02, shade(PAVE, -0.12))
    m.add(0, B.obj("_street"), "street")
    for s in (-1, 1):
        B.box(s * 13, 0, 0, 6, 170, 11, BAKED)
        for j in range(-4, 5):
            B.box(s * 16.9, j * 20, 0, 1.8, 7, 12.5, BAKED_DK)
    m.add(1, B.obj("_walls"), "walls")
    for s, face in ((-1, "E"), (1, "W")):
        fixed = s * 10
        fbox(B, face, fixed, 0, 0.6, 170, 0.12, 10.2, GLZ)
        rosettes(B, face, fixed, -84.5, 84.5, 1.0, size=0.42, gap=0.42, off=0.12, band=False)
        frieze(B, face, fixed, -84.5, 84.5, 1.85, "lion", L=2.5, H=1.75, dirn=-1, gap=0.5, off=0.12, alt=True)
        rosettes(B, face, fixed, -84.5, 84.5, 4.05, size=0.42, gap=0.42, off=0.12, band=False)
        fbox(B, face, fixed, 0, 7.0, 170, 0.2, 0.35, BEAST_W, 0.12)
        fbox(B, face, fixed, 0, 9.6, 170, 0.2, 0.3, BEAST_Y, 0.12)
    m.add(2, B.obj("_lions"), "lions")
    for s in (-1, 1):
        crenel_line(B, s * 13, -85, s * 13, 85, 11, 1.0, BAKED_LT)
        for j in range(-4, 5):
            crenel_line(B, s * 16.9, j * 20 - 3.2, s * 16.9, j * 20 + 3.2, 12.5, 0.9, BAKED_LT)
    m.add(3, B.obj("_crown"), "crenellations")
    return m


# ---------------------------------------------------------------- the Southern Palace

SP_UNITS = [  # x0, x1, court (cx, cy, cw, cd)
    (92, 144, (118, 18, 36, 46)),
    (38, 92, (65, 18, 38, 44)),
    (-30, 38, (4, 22, 56, 50)),
    (-88, -30, (-59, 16, 42, 44)),
    (-144, -88, (-116, 16, 38, 40)),
]


def southern_palace():
    """Five courts in a row, east to west; the throne room on the south of the central court, its glazed facade facing the court."""
    m = Model("southern-palace")
    B = Batch("sp")
    B.box(0, 0, 0, 300, 190, 1.2, BAKED_DK)
    rect_walls(B, 0, 0, 300, 190, 6, 1.2, 13, BAKED)
    for face, fixed, u0, u1 in (("S", -95, -150, 150), ("N", 95, -150, 150), ("W", -150, -95, 95), ("E", 150, -95, 95)):
        n = int((u1 - u0) / 15)
        for i in range(n + 1):
            u = u0 + (u1 - u0) * i / n
            if face == "E" and -4 < u < 26:
                continue
            u = max(u0 + 3.25, min(u1 - 3.25, u))
            fbox(B, face, fixed, u, 0, 6.5, 4.2, 15.5, shade(BAKED, -0.05), -2.0)
    m.add(0, B.obj("_walls"), "walls")

    for x0, x1, court in SP_UNITS:
        cx, cy, cw, cd = court
        central = abs(cx - 4) < 1
        court_unit(B, x0 + 1.5, x1 - 1.5, -89, 89, court, 10.5, MUD_LT, skip={"N": [(cx - 27, cx + 27)]} if central else None)
        for xe in (x0, x1):
            if -144 < xe < 144:
                B.box(xe, 0, 0, 3, 178, 12, MUD)
        if not central:
            # each court's reception suite on its south side: a broad hall rising above the ranges
            hy = cy - cd / 2
            B.span(cx - cw * 0.36, cx + cw * 0.36, hy - 10, hy + 0.05, 0, 14, shade(MUD_LT, 0.05))
            crenel_rect(B, cx, hy - 4.97, cw * 0.72, 10.05, 14, 0.9, BAKED_LT, inset=0.4)
            door(B, "N", hy + 0.05, cx, 0.35, 3, 6.5)
    m.add(1, B.obj("_ranges"), "courts and halls")

    # throne room: 52 x 17 m south of the central court, taller, with the glazed facade on the court side
    tx, tw, td, th = 4, 52, 17, 18
    cy0 = 22 - 25
    tcy = cy0 + 0.05 - td / 2
    B.box(tx, tcy, 0, tw, td, th, MUD_LT)
    B.box(tx, tcy, th, tw + 0.6, td + 0.6, 0.8, shade(MUD_LT, -0.08))
    fy = cy0 + 0.05
    fbox(B, "N", fy, tx, 0.35, tw, 0.15, 14.5, GLZ)
    frieze(B, "N", fy, tx - 25, tx + 25, 0.8, "lion", L=2.4, H=1.6, dirn=1, off=0.15, alt=True)
    for u in (-20, -13, 13, 20):
        fbox(B, "N", fy, tx + u, 3.2, 1.3, 0.35, 8.6, BEAST_W, 0.15)
        fbox(B, "N", fy, tx + u, 3.2, 0.5, 0.45, 8.6, BEAST_Y, 0.15)
        for k, (wv, c) in enumerate(((3.0, BEAST_Y), (2.4, BEAST_W), (3.0, GLZ_LT), (2.4, BEAST_Y))):
            fbox(B, "N", fy, tx + u, 11.8 + k * 0.45, wv, 0.4, 0.45, c, 0.15)
    rosettes(B, "N", fy, tx - 25.5, tx + 25.5, 13.6, size=0.5, off=0.15, band=False)
    for u in (-8, 8):
        door(B, "N", fy, tx + u, 0.35, 3, 7.5, DARK)
    # east gate into the first court, from the Processional Way
    B.span(136, 150, -2, 24, 0, 16, BAKED)
    for yy in (-2, 24):
        B.box(147, yy, 0, 8, 7, 19, shade(BAKED, -0.05))
    door(B, "E", 150, 11, 0, 5, 9)
    m.add(2, join([B.obj("_throne"), arch("sp_door", 5, 10, (tx, fy + 0.25, 0.35), "N")], "sp_throne"), "throne room")

    crenel_rect(B, 0, 0, 300, 190, 14.2, 1.3, BAKED_LT, inset=3)
    crenel_rect(B, tx, tcy, tw, td, th + 0.8, 1.1, GLZ_LT, inset=0.6)
    crenel_rect(B, 143, 11, 14, 26, 16, 1.1, BAKED_LT, inset=0.6)
    m.add(3, B.obj("_crown"), "crenellations")
    return m


# ---------------------------------------------------------------- the Hanging Gardens (interpretation)

def hanging_gardens():
    """The western outwork by the river, with planted terraces on vaults above it: an interpretation of the Greek accounts."""
    m = Model("hanging-gardens")
    B = Batch("hg")
    B.frustum(0, 0, 0, 110, 150, 104, 146, 12, BAKED_DK)
    for face, fixed, u0, u1 in (("W", -55, -74, 74), ("S", -75, -54, 54), ("N", 75, -54, 54)):
        buttresses(B, face, fixed, u0, u1, 0, 11.5, 7.0, 2.2, 1.0, shade(BAKED_DK, 0.06), groove=False, off=-3.0)
    for z in (3.5, 7.0, 10.5):
        B.box(0, 0, z, 110.6, 150.6, 0.25, shade(BAKED_DK, -0.25))
    for y in (-30, 10, 50):
        door(B, "W", -55, y, 0, 4, 5)
    m.add(0, B.obj("_outwork"), "outwork")

    terraces = [(100, 140, 12, 0, 0), (76, 110, 7, 6, 8), (50, 76, 7, 10, 14)]
    z = 12
    for i, (w, d, h, ox, oy) in enumerate(terraces):
        if i:
            B.box(ox, oy, z, w, d, h, shade(BAKED, 0.04 * i))
            fy = oy - d / 2
            n = int(w / 6)
            for j in range(n):
                fbox(B, "S", fy, ox - w / 2 + (j + 0.5) * w / n, z + 0.5, 3.2, 0.3, h - 2.2, DARK)
            fx = ox - w / 2
            n = int(d / 6)
            for j in range(n):
                fbox(B, "W", fx, oy - d / 2 + (j + 0.5) * d / n, z + 0.5, 3.2, 0.3, h - 2.2, DARK)
            z += h
        B.box(ox, oy, z, w - 1, d - 1, 0.6, SOIL)
        B.box(ox, oy, z + 0.6, w - 3, d - 3, 0.15, LEAF)
        crenel_rect(B, ox, oy, w, d, z, 0.9, BAKED_LT, inset=0.5)
    # water: a lifting shaft at the river side, a raised channel to the top terrace, and runnels cascading south
    B.box(-42, 30, 0, 7, 7, 29, BAKED)
    B.box(-42, 30, 29, 8, 8, 1.0, TIMBER)
    for k in range(5):
        B.box(-45.8, 30, 2 + k * 5.4, 0.6, 3.5, 3.5, TIMBER)
    B.span(-38.5, -14, 29.2, 30.8, 27.2, 0.8, BAKED)
    B.span(-38.5, -14, 29.6, 30.4, 28.0, 0.15, WATER)
    B.box(-30, 30, 12.75, 2, 2, 14.45, BAKED)
    B.box(-20, 30, 19.75, 2, 2, 7.45, BAKED)
    B.box(10, -10, 26.75, 1.4, 28, 0.2, WATER)
    B.box(10, -35.5, 19.75, 1.4, 23, 0.2, WATER)
    B.box(10, -60, 12.75, 1.4, 26, 0.2, WATER)
    for fixed, z0, h in ((-24, 19.75, 7.0), (-47, 12.75, 7.0), (-75, 0.0, 12.75)):
        fbox(B, "S", fixed, 10, z0, 1.6, 0.35, h, WATER)
    m.add(1, B.obj("_terraces"), "terraces")

    trees = []
    k = 0
    import random
    rnd = random.Random(7)
    for (w, d, zt, ox, oy, kinds) in ((100, 140, 12.75, 0, 0, ("palm", "round")), (76, 110, 19.75, 6, 8, ("round", "cypress", "palm")), (50, 76, 26.75, 10, 14, ("palm", "round"))):
        for _ in range(int(w * d / 110)):
            x = ox + rnd.uniform(-w / 2 + 4, w / 2 - 4)
            y = oy + rnd.uniform(-d / 2 + 4, d / 2 - 4)
            if under_upper(x, y, terraces, zt):
                continue
            kind = rnd.choice(kinds)
            r = rnd.uniform(2.6, 3.8)
            trees.append(tree(f"hg_t{k}", r, (x, y, zt), PALM_C if kind == "palm" else ("#5E7A48" if kind == "cypress" else LEAF), TIMBER, kind))
            k += 1
    m.add(2, join(trees, "hg_trees"), "trees")
    return m


def under_upper(x, y, terraces, zt):
    """True when (x, y) on a terrace at height zt lies under a higher terrace (so no tree grows inside its wall)
    or on the line of the water runnel."""
    level = 0 if zt < 15 else (1 if zt < 22 else 2)
    if abs(x - 10) < 2.5:
        return True
    for w, d, h, ox, oy in terraces[level + 1:]:
        if abs(x - ox) < w / 2 + 2.5 and abs(y - oy) < d / 2 + 2.5:
            return True
    return level == 0 and abs(x + 42) < 7 and abs(y - 30) < 7


# ---------------------------------------------------------------- the Persian pavilion

def persian_pavilion():
    m = Model("persian-pavilion")
    B = Batch("pp")
    B.box(0, 0, 0, 40, 26, 1.6, LIME)
    for s in (-1, 1):
        stepped_ramp(B, s * 10 - 3, s * 10 + 3, -16, -13, 0, 1.6, 5, LIME)
    m.add(0, B.obj("_terrace"), "terrace")
    B.box(0, 5, 1.6, 30, 14, 9.5, WHITE_PL)
    fbox(B, "S", -2, 0, 7.4, 30, 0.2, 1.6, GLZ)
    frieze(B, "S", -2, -14.5, 14.5, 7.55, "lion", L=1.6, H=1.2, dirn=1, dn=0.2, off=0.2)
    for x in (-10, 0, 10):
        door(B, "S", -2, x, 1.6, 2.4 if x else 3.2, 4.8 if x else 5.6)
    for x in range(-14, 15, 4):
        for y in (-10.5, -6):
            B.box(x, y, 1.6, 1.2, 1.2, 0.6, STONE_DK)
            B.box(x, y, 2.2, 0.7, 0.7, 6.4, STONE_DK)
            B.box(x, y, 8.6, 2.6, 0.9, 1.2, shade(STONE_DK, 0.15))
    B.box(0, -8.2, 9.8, 32, 7.4, 1.0, TIMBER)
    B.box(0, 5, 11.1, 31, 15, 0.6, shade(WHITE_PL, -0.1))
    m.add(1, B.obj("_hall"), "hall and portico")
    crenel_rect(B, 0, 5, 30, 14, 11.7, 0.9, WHITE_PL, inset=0.5)
    m.add(2, B.obj("_crown"), "crenellations")
    return m


# ---------------------------------------------------------------- the Northern Palace

def northern_palace():
    m = Model("northern-palace")
    B = Batch("np")
    B.frustum(0, 0, 0, 170, 120, 166, 116, 4, BAKED_DK)
    for face, fixed, u0, u1 in (("S", -60, -84, 84), ("N", 60, -84, 84), ("W", -85, -59, 59), ("E", 85, -59, 59)):
        buttresses(B, face, fixed, u0, u1, 0, 4, 6, 2.4, 0.8, shade(BAKED_DK, 0.05), groove=False, off=-2.0)
    rect_walls(B, 0, 0, 164, 114, 5, 4, 12, BAKED)
    for face, fixed, u0, u1 in (("S", -57, -82, 82), ("N", 57, -82, 82), ("W", -82, -57, 57), ("E", 82, -57, 57)):
        n = int((u1 - u0) / 14)
        for i in range(n + 1):
            u = u0 + (u1 - u0) * i / n
            if face == "E" and -8 < u < 8:
                continue
            fbox(B, face, fixed, u, 4, 6, 2, 14, shade(BAKED, -0.05))
    B.span(-82, 82, 50, 57, 4, 16, BAKED_DK)   # the massive north wall
    m.add(0, B.obj("_base"), "platform and walls")
    Bz = Batch("np_r")
    court_unit(Bz, -77, -2, -52, 50, (-38, 2, 46, 40), 9.5, MUD_LT)
    court_unit(Bz, 2, 77, -52, 50, (38, 2, 38, 34), 9, MUD_LT)
    Bz.box(0, 0, 0, 4, 102, 11, MUD)
    o = Bz.obj()
    o = move(o, 0, 0, 4)
    m.add(1, o, "courts")
    B.span(76, 85, -9, 9, 4, 17, BAKED)
    door(B, "E", 85, 0, 4, 4.5, 8)
    crenel_rect(B, 0, 0, 164, 114, 16, 1.2, BAKED_LT, inset=2.5)
    crenel_line(B, -82, 53.5, 82, 53.5, 20, 1.2, BAKED_LT)
    m.add(2, B.obj("_crown"), "gate and crenellations")
    return m


# ---------------------------------------------------------------- the Summer Palace (Babil)

def summer_palace():
    m = Model("summer-palace")
    B = Batch("su")
    B.frustum(0, 4, 0, 200, 172, 188, 160, 14, BAKED_DK)
    for face, fixed, u0, u1 in (("S", -82, -98, 98), ("N", 90, -98, 98), ("W", -100, -82, 88), ("E", 100, -82, 88)):
        buttresses(B, face, fixed, u0, u1, 0, 13.5, 8, 3.2, 1.4, shade(BAKED_DK, 0.06), groove=True, off=-6.0)
    for z in (4.5, 9.0):
        B.frustum(0, 4, z, 200.4 - z * 12 / 14, 172.4 - z * 12 / 14, 200.4 - z * 12 / 14, 172.4 - z * 12 / 14, 0.3, shade(BAKED_DK, -0.25))
    stepped_ramp(B, -9, 9, -90, -75, 0, 14, 16, BAKED, axis="y", parapet=BAKED_DK)
    m.add(0, B.obj("_platform"), "platform")
    Bz = Batch("su_r")
    rect_walls(Bz, 0, 4, 176, 148, 5, 0, 9, BAKED)
    court_unit(Bz, -83, 83, -65, 73, (0, 4, 74, 62), 8, MUD_LT)
    for sx in (-1, 1):
        for sy in (-1, 1):
            Bz.box(sx * 84, 4 + sy * 70, 0, 12, 12, 14, shade(BAKED, -0.05))
            crenel_rect(Bz, sx * 84, 4 + sy * 70, 12, 12, 14, 1.0, BAKED_LT, inset=0.5)
    for (x, y) in ((-50, 40), (-30, 52), (40, 47), (55, -40), (-45, -45), (20, -52)):
        Bz.box(x, y, 8.0, 3, 3, 0.1, DARK)
    Bz.span(-7, 7, -73, -66, 0, 12, BAKED)
    door(Bz, "S", -73, 0, 0, 4, 7)
    o = move(Bz.obj(), 0, 0, 14)
    m.add(1, o, "palace")
    crenel_rect(B, 0, 4, 176, 148, 23, 1.1, BAKED_LT, inset=2.5)
    m.add(2, B.obj("_crown"), "crenellations")
    return m


# ---------------------------------------------------------------- Etemenanki

ET_CY = 29.25          # the tower's centre; its great stair runs south to the edge of the footprint (y = -75)
ET_STAGES = [(91.5, 33), (78, 18), (60, 6), (51, 6), (42, 6), (33, 6)]


def _stage(B, cx, cy, w, z, h, color, every, bw, dn, mats=True):
    B.frustum(cx, cy, z, w, w, w - 0.8, w - 0.8, h, color)
    for face, fixed, u0, u1, c in (("S", cy - w / 2, cx - w / 2, cx + w / 2, cx), ("N", cy + w / 2, cx - w / 2, cx + w / 2, cx),
                                   ("W", cx - w / 2, cy - w / 2, cy + w / 2, cy), ("E", cx + w / 2, cy - w / 2, cy + w / 2, cy)):
        buttresses(B, face, fixed, u0 + 1.0, u1 - 1.0, z, h * 0.985, every, bw, dn, shade(color, 0.05), groove=True, off=-0.5)
    if mats:
        k = 1
        while k * 3.0 < h - 1:
            B.box(cx, cy, z + k * 3.0, w + dn * 2 + 0.2, w + dn * 2 + 0.2, 0.22, shade(color, -0.3))
            k += 1


def etemenanki():
    m = Model("etemenanki")
    B = Batch("et")
    B.box(0, 0, 0, 110, 150, 0.3, PAVE)
    cy = ET_CY
    _stage(B, 0, cy, 91.5, 0.3, 33, BAKED, 4.6, 1.8, 0.9)
    m.add(0, B.obj("_s1"), "first stage")
    # the triple stair: a great central flight to the second stage, two side flights along the south face to the first
    s1y = cy - 91.5 / 2
    stepped_ramp(B, -5, 5, -75, s1y + 12.5, 0.3, 51.3, 72, BAKED_LT, axis="y", parapet=BAKED)
    B.span(-6.5, 6.5, s1y, s1y + 12.5, 33.3, 18, BAKED_LT)
    for s in (-1, 1):
        stepped_ramp(B, s * 45.5, s * 9, s1y - 7, s1y, 0.3, 33.3, 46, BAKED_LT, axis="x")
        B.span(s * 45.5, s * 9, s1y - 7.6, s1y - 7, 0.3, 1.2, BAKED)
    B.span(-9, 9, s1y - 7, s1y, 0.3, 33, BAKED)
    # gate houses where the flights arrive
    B.box(0, s1y - 3.5, 33.3, 14, 6, 8, BAKED)
    door(B, "S", s1y - 6.5, 0, 33.3, 3.2, 5.2)
    z = 33.3
    _stage(B, 0, cy, 78, z, 18, shade(BAKED, 0.04), 4.6, 1.6, 0.8)
    m.add(1, B.obj("_s2"), "stairs and second stage")
    z += 18
    for i, (w, h) in enumerate(ET_STAGES[2:]):
        _stage(B, 0, cy, w, z, h, shade(BAKED, 0.07 + i * 0.03), 3.6, 1.2, 0.6, mats=False)
        stepped_ramp(B, -3, 3, cy - w / 2 - 3.5, cy - w / 2, z, z + 3, 8, BAKED_LT, axis="y")
        z += h
    m.add(2, B.obj("_upper"), "upper stages")
    for (w, h), zt in zip(ET_STAGES, (33.3, 51.3, 57.3, 63.3, 69.3, 75.3)):
        crenel_rect(B, 0, cy, w - 0.8, w - 0.8, zt, 1.2 if w > 70 else 0.9, BAKED_LT, inset=0.6)
    # the temple on top, glazed blue: 24 x 21 m and 15 m high
    B.box(0, cy, z, 24, 21, 15, GLZ)
    all_buttresses(B, 0, cy, 24, 21, z, 14.6, 2.6, 0.9, 0.4, GLZ_LT, skip={"S": [(-2.5, 2.5)]})
    door(B, "S", cy - 10.5, 0, z, 3, 6.5)
    B.box(0, cy, z + 15, 24.6, 21.6, 0.6, BEAST_Y)
    crenel_rect(B, 0, cy, 24.6, 21.6, z + 15.6, 1.0, GLZ_LT, inset=0.5)
    for sx in (-1, 1):
        for sy in (-1, 1):
            B.box(sx * 11.5, cy + sy * 10, z + 15.6, 1.2, 1.2, 2.4, GILT)
    m.add(3, B.obj("_temple"), "temple")
    return m


def etemenanki_early():
    """An earlier, smaller tower of mud brick (second millennium BCE; form unknown, drawn as a guess)."""
    m = Model("etemenanki-early")
    B = Batch("ete")
    B.box(0, 0, 0, 110, 150, 0.3, EARTH)
    cy = 22
    _stage(B, 0, cy, 64, 0.3, 16, MUD, 4.0, 1.6, 0.7)
    m.add(0, B.obj("_s1"), "first stage")
    stepped_ramp(B, -4, 4, cy - 32 - 26, cy - 32, 0.3, 16.3, 26, MUD_LT, axis="y", parapet=MUD)
    _stage(B, 0, cy, 46, 16.3, 10, shade(MUD, 0.05), 3.6, 1.3, 0.6)
    m.add(1, B.obj("_s2"), "second stage")
    _stage(B, 0, cy, 32, 26.3, 8, shade(MUD, 0.09), 3.2, 1.1, 0.5, mats=False)
    stepped_ramp(B, -3, 3, cy - 23 - 4, cy - 23, 16.3, 21, 6, MUD_LT, axis="y")
    B.box(0, cy, 34.3, 16, 13, 7, WHITE_PL)
    door(B, "S", cy - 6.5, 0, 34.3, 2.4, 4.2)
    crenel_rect(B, 0, cy, 16, 13, 41.3, 0.8, WHITE_PL, inset=0.4)
    for w, zt in ((63.2, 16.3), (45.2, 26.3), (31.2, 34.3)):
        crenel_rect(B, 0, cy, w, w, zt, 0.9, MUD_LT, inset=0.5)
    m.add(2, B.obj("_top"), "shrine")
    return m


def etemenanki_ruin():
    """The ruined tower in 323 BCE: the baked-brick mantle stripped away in a jagged ring, the mud-brick core cut down,
    the lower flights of the stair, rubble heaps, spoil tracks and workers from Alexander's clearance."""
    import random
    rnd = random.Random(11)
    m = Model("etemenanki-ruin")
    B = Batch("etr")
    B.box(0, 0, 0, 110, 150, 0.3, EARTH)
    cy = ET_CY
    # the lowest courses of the first stage survive all round
    B.frustum(0, cy, 0.3, 91.5, 91.5, 91.0, 91.0, 5, BAKED)
    buttresses(B, "S", cy - 45.75, -44, 44, 0.3, 5, 4.6, 1.8, 0.9, shade(BAKED, 0.05), off=-0.3)
    # the mantle, 15 m thick, broken into a jagged ring of stumps; gaps where the bricks have been carted off
    for face in "SNWE":
        for j in range(18):
            u = -45.75 + (j + 0.5) * 91.5 / 18
            h = rnd.choice((0, 0, 2, 4, 6, 9, 12, 15)) * (1.0 if face in "SW" else 0.8)
            if h <= 0:
                continue
            w = 91.5 / 18 + 0.2
            if face == "S":
                B.box(u, cy - 45.75 + 7.5, 5.3, w, 15, h, shade(BAKED, rnd.uniform(-0.06, 0.04)))
            elif face == "N":
                B.box(u, cy + 45.75 - 7.5, 5.3, w, 15, h, shade(BAKED, rnd.uniform(-0.06, 0.04)))
            elif face == "W" and abs(u) < 30.75:
                B.box(-45.75 + 7.5, cy + u, 5.3, 15, w, h, shade(BAKED, rnd.uniform(-0.06, 0.04)))
            elif face == "E" and abs(u) < 30.75:
                B.box(45.75 - 7.5, cy + u, 5.3, 15, w, h, shade(BAKED, rnd.uniform(-0.06, 0.04)))
    # the exposed mud-brick core, cut down into an uneven mound with reed-mat layers showing
    B.frustum(0, cy, 5.3, 61, 61, 44, 44, 14, MUD_DK)
    for k in range(1, 5):
        B.box(0, cy, 5.3 + k * 2.8, 61.2 - k * 3.4, 61.2 - k * 3.4, 0.2, shade(MUD_DK, -0.3))
    for _ in range(26):
        x, y = rnd.uniform(-17, 17), cy + rnd.uniform(-17, 17)
        B.box(x, y, 19.3, rnd.uniform(4, 10), rnd.uniform(4, 10), rnd.uniform(1, 6), shade(MUD_DK, rnd.uniform(-0.06, 0.08)), rnd.uniform(0, 0.5))
    m.add(0, B.obj("_core"), "ruined tower")
    # the lower part of the great stair, and ramps of spoil down which baskets were carried
    stepped_ramp(B, -5, 5, -75, -45, 0.3, 17, 24, BAKED_LT, axis="y", parapet=BAKED)
    for s in (-1, 1):
        stepped_ramp(B, s * 45.5, s * 26, cy - 52.75, cy - 45.75, 0.3, 10, 14, BAKED_LT, axis="x")
    for (x, y, w, d, h) in ((-20, cy - 36, 10, 26, 10), (26, cy + 12, 24, 10, 8)):
        B.frustum(x, y, 0.3, w, d, w * 0.5, d * 0.5, h, shade(MUD_DK, 0.08))
    for _ in range(26):
        r = rnd.uniform(3, 6)
        x, y = rnd.choice((rnd.uniform(-54 + r, -38), rnd.uniform(38, 54 - r))), rnd.uniform(-70, 70)
        B.frustum(x, y, 0.3, r * 2, r * 1.7, r * 0.5, r * 0.4, rnd.uniform(1.5, 4), shade("#B69B74", rnd.uniform(-0.08, 0.08)))
    for _ in range(90):
        x, y = rnd.uniform(-50, 50), rnd.uniform(-73, -22)
        if abs(x) < 7:
            continue
        B.box(x, y, 0.3, rnd.uniform(1.0, 3.0), rnd.uniform(1.0, 3.0), rnd.uniform(0.4, 1.4), shade(BAKED, rnd.uniform(-0.1, 0.05)), rnd.uniform(0, 1.5))
    for x0, a in ((30, 0.25), (-28, -0.2)):
        B.box(x0, -45, 0.3, 4, 60, 0.12, shade(EARTH, -0.12), a)
    m.add(1, B.obj("_rubble"), "rubble and clearance")
    # workers' shelters, stacked salvaged bricks, carts and the workers themselves
    for x, y in ((-46, -62), (44, -60), (-48, 62), (47, 66)):
        B.box(x, y, 0.3, 8, 5, 2.6, MUD_LT)
        B.box(x, y, 2.9, 9, 6, 0.3, "#9A8A5E")
    for k in range(8):
        x, y = (16 + (k % 4) * 4.5, -56) if k < 4 else (-30 + (k % 4) * 4.5, -62)
        B.box(x, y, 0.3, 3.4, 2.0, 1.6, BAKED_LT)
        B.box(x, y, 1.9, 3.0, 1.6, 0.4, shade(BAKED_LT, -0.08))
    for x, y, a in ((24, -30, 0.2), (-26, -36, -0.2), (34, 0, 0.0)):
        B.box(x, y, 0.9, 2.2, 3.4, 1.0, TIMBER, a)
        for s in (-1, 1):
            B.box(x + s * 1.25 * math.cos(a), y + s * 1.25 * math.sin(a), 0.3, 0.3, 1.4, 1.4, shade(TIMBER, -0.3), a)
    for _ in range(46):
        x, y = rnd.uniform(-44, 44), rnd.uniform(-70, 10)
        if abs(x) < 8 and y < -44:
            continue
        z = 0.3
        if abs(x) < 45 and cy - 45 < y:
            continue
        B.box(x, y, z, 0.5, 0.4, 1.2, "#8A5A3C")
        B.box(x, y, z + 1.2, 0.36, 0.36, 0.4, "#B07A55")
        if rnd.random() < 0.5:
            B.box(x, y, z + 1.6, 0.7, 0.7, 0.35, THATCH)
    m.add(2, B.obj("_works"), "works")
    return m


# ---------------------------------------------------------------- Esagila

def esagila():
    """The main temple (86 x 79 m) on the west and the forecourt (about 112 x 103 m) on the east."""
    m = Model("esagila")
    B = Batch("es")
    B.box(0, 0, 0, 200, 105, 0.3, PAVE)
    m.add(0, B.obj("_ground"), "ground")
    # main temple
    mx, mw, md, mh = -57, 86, 79, 14
    rect_walls(B, mx, 0, mw, md, 6, 0.3, mh, BAKED_LT)
    all_buttresses(B, mx, 0, mw, md, 0.3, mh, 3.6, 1.6, 0.8, shade(BAKED_LT, 0.04),
                   skip={"E": [(-7, 7)], "N": [(-64, -50)], "S": [(-64, -50)]})
    court_unit(B, mx - mw / 2 + 6, mx + mw / 2 - 6, -md / 2 + 6, md / 2 - 6, (mx + 6, 0, 36, 34), 11, MUD_LT)
    # Marduk's shrine (E-umusha) on the west of the court, taller
    B.span(mx - 37, mx - 13, -18, 18, 0.3, 18, BAKED_LT)
    door(B, "E", mx - 13, 0, 0.3, 4, 8)
    B.span(mx - 37.3, mx - 12.7, -18.3, 18.3, 18.3, 0.7, GILT)
    for face, fixed, u, proj in (("E", mx + mw / 2, 0, 1.6), ("N", md / 2, mx, 2.5), ("S", -md / 2, mx, 2.5)):
        tower_pair(B, face, fixed, u, 7, 6, proj, 6, 0.3, mh + 4, shade(BAKED_LT, -0.04), BAKED, 0.8)
        door(B, face, fixed, u, 0.3, 4, 8)
    m.add(1, B.obj("_temple"), "temple")
    # forecourt
    fx, fw, fd = 44, 112, 103
    rect_walls(B, fx, 0, fw, fd, 4, 0.3, 10, BAKED_LT)
    all_buttresses(B, fx, 0, fw, fd, 0.3, 10, 4.0, 1.4, 0.7, shade(BAKED_LT, 0.04),
                   skip={"W": [(-7, 7)], "E": [(-7, 7)], "N": [(fx - 7, fx + 7)], "S": [(fx - 7, fx + 7)]})
    for (x0, x1, y0, y1) in ((fx - 52, fx + 52, 37, 47.5), (fx - 52, fx + 52, -47.5, -37), (fx - 52, fx - 42, -37, 37), (fx + 42, fx + 52, -37, 37)):
        B.span(x0, x1, y0, y1, 0.3, 8, MUD_LT)
    for face, fixed, u0, u1 in (("S", 37, fx - 42, fx + 42), ("N", -37, fx - 42, fx + 42), ("E", fx - 42, -37, 37), ("W", fx + 42, -37, 37)):
        k = int((u1 - u0) / 7)
        for j in range(k):
            door(B, face, fixed, u0 + (u1 - u0) * (j + 0.5) / k, 0.3, 1.8, 3.4)
    for (x, y, w, d) in ((fx - 18, 16, 14, 10), (fx + 20, -14, 12, 10), (fx + 20, 18, 10, 8)):
        B.box(x, y, 0.3, w, d, 6, WHITE_PL)
        crenel_rect(B, x, y, w, d, 6.3, 0.7, WHITE_PL, inset=0.3)
    B.box(fx - 10, -12, 0.3, 3, 3, 1.0, BAKED_DK)
    for face, fixed, u in (("E", fx + fw / 2, 0), ("N", fd / 2, fx), ("S", -fd / 2, fx), ("W", fx - fw / 2, 0)):
        if face != "W":
            tower_pair(B, face, fixed, u, 6.5, 5, 2.2, 4, 0.3, 13.7, shade(BAKED_LT, -0.04), BAKED, 0.8)
        door(B, face, fixed, u, 0.3, 3.6, 7)
    m.add(2, B.obj("_forecourt"), "forecourt")
    crenel_rect(B, mx, 0, mw, md, mh + 0.3, 1.1, BAKED, inset=1.2)
    crenel_rect(B, fx, 0, fw, fd, 10.3, 1.0, BAKED, inset=1.0)
    crenel_rect(B, mx - 25, 0, 24, 36, 19, 0.9, GILT, inset=0.5)
    m.add(3, B.obj("_crown"), "crenellations")
    return m


# ---------------------------------------------------------------- neighbourhood temples

def court_temple(name, w, d, h, color, gates=((0,),), cella_d=10, t=3.0, every=2.4):
    """A Babylonian court temple: toothed outer walls, towered gate(s) on the south, a court, the cella block on the north."""
    m = Model(name)
    B = Batch(name[:4])
    B.box(0, 0, 0, w + 2, d + 2, 0.25, EARTH)
    rect_walls(B, 0, 0, w, d, t, 0.25, h, color)
    gate_skip = [(u - 5, u + 5) for (u,) in gates]
    all_buttresses(B, 0, 0, w, d, 0.25, h, every, 1.0, 0.5, shade(color, 0.03), skip={"S": gate_skip})
    m.add(0, B.obj("_walls"), "walls")
    # ranges round the court and the cella on the north
    inner_w, inner_d = w - 2 * t, d - 2 * t
    B.span(-inner_w / 2, inner_w / 2, d / 2 - t - cella_d, d / 2 - t, 0.25, h + 2.5, shade(color, 0.04))
    B.span(-inner_w / 2, -inner_w / 2 + 5, -inner_d / 2, d / 2 - t - cella_d, 0.25, h - 1, color)
    B.span(inner_w / 2 - 5, inner_w / 2, -inner_d / 2, d / 2 - t - cella_d, 0.25, h - 1, color)
    B.span(-inner_w / 2 + 5, inner_w / 2 - 5, -inner_d / 2, -inner_d / 2 + 4, 0.25, h - 1, color)
    B.span(-inner_w / 2 + 5, inner_w / 2 - 5, -inner_d / 2 + 4, d / 2 - t - cella_d, 0.25, 0.2, PAVE)
    door(B, "S", d / 2 - t - cella_d, 0, 0.25, 2.4, 4.8)
    buttresses(B, "S", d / 2 - t - cella_d, -inner_w / 2 + 6, inner_w / 2 - 6, 0.25, h + 2.3, 1.8, 0.7, 0.35, shade(color, 0.07), skip=[(-1.6, 1.6)])
    B.box(-inner_w / 4, -inner_d / 2 + 9, 0.25, 1.4, 1.4, 0.9, BAKED_DK)     # well
    m.add(1, B.obj("_court"), "court and cella")
    for (u,) in gates:
        for s in (-1, 1):
            B.box(u + s * 3.2, -d / 2 + 0.4, 0.25, 3.0, t + 3.0, h + 3.5, shade(color, -0.03))
            crenel_rect(B, u + s * 3.2, -d / 2 + 0.4, 3.0, t + 3.0, h + 3.75, 0.7, color, inset=0.25)
            buttresses(B, "S", -d / 2 - 1.1, u + s * 3.2 - 1.2, u + s * 3.2 + 1.2, 0.25, h + 3.3, 1.2, 0.5, 0.25, shade(color, 0.05))
        B.box(u, -d / 2 + 0.4, 0.25, 3.4, t + 2.0, h + 1.5, color)
        door(B, "S", -d / 2 + 0.4 - (t + 2.0) / 2, u, 0.25, 2.0, 4.6)
    crenel_rect(B, 0, 0, w, d, h + 0.25, 0.75, color, inset=0.5)
    crenel_rect(B, 0, d / 2 - t - cella_d / 2, inner_w, cella_d, h + 2.75, 0.7, color, inset=0.3)
    m.add(2, B.obj("_gates"), "gate towers")
    return m


def emah():
    return court_temple("emah", 53, 38, 8.5, WHITE_PL, gates=((0,),), cella_d=11)


def emashdari():
    return court_temple("emashdari", 38, 34, 7.5, WHITE_PL, gates=((0,),), cella_d=9)


def nabu_sha_hare():
    return court_temple("nabu-sha-hare", 48, 38, 8, MUD_LT, gates=((0,),), cella_d=10)


def ninurta_temple():
    return court_temple("ninurta-temple", 58, 48, 8.5, MUD_LT, gates=((-17,), (0,), (17,)), cella_d=12)


# ---------------------------------------------------------------- the bridge on piers

def bridge():
    """About 135 m of boat-shaped piers between brick abutments (X across the river); the cutwaters point north, upstream."""
    m = Model("bridge")
    B = Batch("br")
    for k in range(8):
        x = -63 + k * 18
        pts = [(x - 4.5, -6.5), (x, -9.6), (x + 4.5, -6.5), (x + 4.5, 6.5), (x, 9.6), (x - 4.5, 6.5)]
        B.poly(pts, 0, 6.8, BAKED)
        for z in (1.6, 3.4, 5.2):
            B.poly([(px + (0.15 if px > x else -0.15), py * 1.015) for px, py in pts], z, 0.4, LIME)
        B.poly([(px * 1.0, py) for px, py in pts], 6.8, 0.4, shade(BAKED, -0.15))
    for s in (-1, 1):
        B.span(s * 76.5, s * 90, -10, 10, 0, 8, BAKED_DK)
        for i in range(8):
            B.span(s * 76.5, s * (77.5 + i * 1.5), 6.5, 10, 0, 8 - i, BAKED)
        crenel_line(B, s * 77, -9.6, s * 90, -9.6, 8, 0.8, BAKED_LT)
    m.add(0, B.obj("_piers"), "piers")
    B.box(0, 0, 7.2, 153, 6, 0.5, TIMBER)
    for y in (-2.4, -0.8, 0.8, 2.4):
        B.box(0, y, 6.7, 153, 0.45, 0.5, shade(TIMBER, -0.2))
    for s in (-1, 1):
        B.box(0, s * 2.9, 8.4, 153, 0.2, 0.2, shade(TIMBER, 0.1))
        for i in range(103):
            B.box(-76 + i * 1.5, s * 2.9, 7.7, 0.22, 0.22, 0.9, shade(TIMBER, 0.1))
    for i in range(70):
        B.box(-75.5 + i * 2.2, 0, 7.7, 0.15, 6, 0.04, shade(TIMBER, -0.3))
    m.add(1, B.obj("_deck"), "timber deck")
    return m


# ---------------------------------------------------------------- the outer wall and a gate

def outer_gate():
    """A 90 m stretch of Nebuchadnezzar's outer wall (X along the wall) with its gate; the outer side and moat toward -Y."""
    m = Model("outer-gate")
    B = Batch("og")
    B.box(0, 0, 0, 90, 44, 0.2, EARTH)
    B.span(-45, 45, -22, -18.5, 0, 0.12, WATER)
    B.span(-45, 45, -18.5, -15.5, 0, 4.5, BAKED_DK)                    # the quay wall on the moat
    m.add(0, B.obj("_quay"), "moat and quay")
    B.span(-45, 45, -12, -4, 0, 12, BAKED)                             # baked-brick outer wall
    B.span(-45, 45, -4, 4, 0, 9, EARTH)                                # filled space, a road on top
    B.span(-45, 45, 4, 11, 0, 13, MUD)                                 # mud-brick inner wall
    for x in (-36, -18, 18, 36):
        B.box(x, -13.2, 0, 8, 2.6, 14, shade(BAKED, -0.05))
        B.box(x, 12.2, 0, 7, 2.6, 15, shade(MUD, -0.05))
    for s in (-1, 1):
        B.box(s * 8, -9, 0, 8, 14, 17, shade(BAKED, -0.06))
        B.box(s * 7, 8, 0, 7, 12, 16, shade(MUD, -0.06))
    B.box(0, -8, 0, 8, 10, 14, BAKED)
    B.box(0, 8, 0, 7, 8, 14, MUD)
    B.span(-3.5, 3.5, -18.5, 22, 0.2, 0.25, PAVE)
    m.add(1, join([B.obj("_walls"), arch("og_a1", 4.2, 8, (0, -13.05, 0.2), "S"), arch("og_a2", 4.0, 7.5, (0, 12.05, 0.2), "N")], "og_walls"), "walls and gate")
    crenel_line(B, -45, -11.5, -12, -11.5, 12, 1.1, BAKED_LT)
    crenel_line(B, 12, -11.5, 45, -11.5, 12, 1.1, BAKED_LT)
    crenel_line(B, -45, 10.5, -10.5, 10.5, 13, 1.0, MUD_LT)
    crenel_line(B, 10.5, 10.5, 45, 10.5, 13, 1.0, MUD_LT)
    crenel_line(B, -45, -15.6, 45, -15.6, 4.5, 0.7, BAKED)
    for x in (-36, -18, 18, 36):
        crenel_rect(B, x, -13.2, 8, 2.6, 14, 0.9, BAKED_LT, inset=0.3)
        crenel_rect(B, x, 12.2, 7, 2.6, 15, 0.9, MUD_LT, inset=0.3)
    for s in (-1, 1):
        crenel_rect(B, s * 8, -9, 8, 14, 17, 1.0, BAKED_LT, inset=0.4)
        crenel_rect(B, s * 7, 8, 7, 12, 16, 1.0, MUD_LT, inset=0.4)
    crenel_rect(B, 0, -8, 8, 10, 14, 0.9, BAKED_LT, inset=0.4)
    m.add(2, B.obj("_crown"), "crenellations")
    return m


# ---------------------------------------------------------------- the Greek theatre

def theatre():
    """A Hellenistic theatre of mud brick: the cavea opens south toward the stage building."""
    m = Model("theatre")
    B = Batch("th")
    B.box(0, 0, 0, 76, 64, 0.2, EARTH)
    cx, cy = 0, -8
    a0, a1 = math.radians(-12), math.radians(192)
    B.sector(cx, cy, 36, 37.6, a0, a1, 0.2, 10.4, MUD, seg=28)
    rows = 17
    for i in range(rows):
        r0 = 10.5 + i * (25.5 / rows)
        B.sector(cx, cy, r0, 36, a0, a1, 0.2 + i * 0.58, 0.58, shade(MUD_LT, 0.04 if i % 2 else 0.0), seg=40)
    for ang in (30, 60, 90, 120, 150):
        a = math.radians(ang)
        for i in range(rows):
            r = 10.5 + (i + 0.5) * (25.5 / rows)
            B.box(cx + r * math.cos(a), cy + r * math.sin(a), 0.2 + (i + 1) * 0.58, 1.3, 1.1, 0.06, shade(MUD_LT, 0.2), a + math.pi / 2)
    m.add(0, B.obj("_cavea"), "cavea")
    for i in range(41):
        a = a0 + (a1 - a0) * i / 40
        B.box(cx + 35.2 * math.cos(a), cy + 35.2 * math.sin(a), 10.06, 0.6, 0.6, 2.6, WHITE_PL)
    B.sector(cx, cy, 34.4, 37.6, a0, a1, 12.66, 0.4, shade(TIMBER, 0.1), seg=40)
    B.sector(cx, cy, 34.6, 36.0, a0, a1, 10.06, 0.15, PAVE, seg=40)
    B.poly([(cx + 10.3 * math.cos(math.tau * i / 28), cy + 10.3 * math.sin(math.tau * i / 28)) for i in range(28)], 0.2, 0.15, PAVE)
    B.box(0, -24.5, 0.2, 40, 6, 7.5, MUD_LT)
    B.box(0, -24.5, 7.7, 41, 7, 0.5, shade(MUD_LT, -0.1))
    for x in (-10, 0, 10):
        door(B, "N", -21.5, x, 0.2, 2.4 if x else 3, 4.2)
    B.box(0, -19.6, 0.2, 30, 3.8, 3.2, WHITE_PL)
    for i in range(12):
        B.box(-14 + i * (28 / 11), -17.9, 0.2, 0.5, 0.5, 3.2, shade(WHITE_PL, -0.06))
    for s in (-1, 1):
        B.box(s * 24, -17, 0.2, 6, 4, 4.5, MUD)
    m.add(1, B.obj("_stage"), "stage")
    return m


BUILDERS = {
    "babylon/ishtar-gate": ishtar_gate,
    "babylon/processional-way": processional_way,
    "babylon/southern-palace": southern_palace,
    "babylon/hanging-gardens": hanging_gardens,
    "babylon/persian-pavilion": persian_pavilion,
    "babylon/northern-palace": northern_palace,
    "babylon/summer-palace": summer_palace,
    "babylon/etemenanki": etemenanki,
    "babylon/etemenanki-early": etemenanki_early,
    "babylon/etemenanki-ruin": etemenanki_ruin,
    "babylon/esagila": esagila,
    "babylon/emah": emah,
    "babylon/emashdari": emashdari,
    "babylon/nabu-sha-hare": nabu_sha_hare,
    "babylon/ninurta-temple": ninurta_temple,
    "babylon/bridge": bridge,
    "babylon/outer-gate": outer_gate,
    "babylon/theatre": theatre,
}
