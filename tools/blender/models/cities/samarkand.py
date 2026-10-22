"""Samarkand landmark miniatures: Sogdian Afrasiyab, Timur's city, Ulugh Beg's Registan and observatory, the Uzbek madrasas.

Conventions as in FORMAT.md: metres, origin at the ground centre, +X east, +Y north, main front toward -Y unless a
builder says otherwise; the landmark rotation turns it on the map. Most tilework is built with a Batch that gathers
thousands of small boxes and panels into one mesh per colour, which keeps the banna'i patterns, tile frames and
fluted domes cheap to build.
"""
import math
from chronokit import Model, box, cylinder, dome, join, shade, mesh_from
from worldkit import *

# ---------------------------------------------------------------- palette
BRICK_T = "#C9A375"      # Timurid fired brick
BRICK_LT = "#DABD92"
BRICK_DK = "#A9875F"
TURQ = "#2C9FAF"         # Samarkand turquoise
TURQ_LT = "#5CBEC6"
COBALT = "#23428F"
DEEP = "#1F2F5C"         # deep blue of glazed iwan recesses
TWHITE = "#EEEADF"
TYEL = "#D9A83A"
TGREEN = "#3D8C69"
DOME = "#33A8B6"
PAKHSA, PAKHSA_DK, PAKHSA_LT = "#C8A87B", "#AE8F62", "#D6BC92"
MUD = "#C3A278"
GROUND, PAVE, PAVE_DK = "#D8C49C", "#D6C3A0", "#BFA982"
LAWN, LEAF, LEAF_DK = "#86A06A", "#6F8C55", "#5D7A48"
WOOD, WOOD_DK = "#8A6744", "#6A4E33"
AWNINGS = ["#B8553E", "#D9C9A0", "#4E6E8E", "#C49A45", "#8E5A7A"]
RUBBLE = "#B9A07A"
WATER_C = "#5F8E94"
DOOR = DARK


# ---------------------------------------------------------------- mesh batch

class Batch:
    """Collects geometry per colour and builds one joined object: boxes, extruded panels, lathes, prisms."""

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

    def panel(self, c, outline, O, ang, depth=0.25, off=0.0):
        """Extrude a flat outline [(u, v)] lying on a wall plane through O whose outward normal is at angle ang (radians)."""
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
        self.add(c, V, F)

    def build(self):
        objs = [mesh_from(f"{self.name}_{i}", V, F, (0, 0, 0), c) for i, (c, (V, F)) in enumerate(self.g.items()) if F]
        return join(objs, self.name)


# ---------------------------------------------------------------- transforms

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


FACING = {"S": 0, "E": 90, "N": 180, "W": -90}     # rz turning a front built toward -Y to face that way
SOUTH, EAST, NORTH, WEST = -math.pi / 2, 0.0, math.pi / 2, math.pi  # outward normals of wall faces


def ngon(r, n, start=None):
    s = math.pi / n if start is None else start
    return [(r * math.cos(s + k * math.tau / n), r * math.sin(s + k * math.tau / n)) for k in range(n)]


def arch_outline(w, h, R=0.66, n=3):
    """A Timurid pointed arch (two-centred) of span w and total height h, as a convex outline."""
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


def sq_off(s, u, v):
    return [(u - s / 2, v - s / 2), (u + s / 2, v - s / 2), (u + s / 2, v + s / 2), (u - s / 2, v + s / 2)]


# ---------------------------------------------------------------- tile ornament

def kufic_band(B, O, ang, u0, u1, v0, v1, ground=COBALT, letter=TWHITE, off=0.0, pitch=None):
    """An inscription frieze: a coloured band with white upright strokes and a base line, like square Kufic or thuluth."""
    B.rect(ground, O, ang, u0, u1, v0, v1, 0.16, off)
    h = v1 - v0
    pitch = pitch or h * 0.55
    n = max(2, int((u1 - u0) / pitch))
    for i in range(n):
        u = u0 + (i + 0.5) * (u1 - u0) / n
        tall = 0.78 if i % 3 != 1 else 0.45
        B.rect(letter, O, ang, u - pitch * 0.13, u + pitch * 0.13, v0 + h * 0.16, v0 + h * tall, 0.08, off + 0.16)
    B.rect(letter, O, ang, u0 + pitch * 0.2, u1 - pitch * 0.2, v0 + h * 0.12, v0 + h * 0.22, 0.08, off + 0.16)


def lozenge_field(B, O, ang, u0, u1, v0, v1, step, colors=(TURQ, COBALT), off=0.0, size=0.62, dark=None):
    """Banna'i: glazed lozenges set in the brick, in staggered rows."""
    rows = max(1, int((v1 - v0) / step))
    cols = max(1, int((u1 - u0) / step))
    for j in range(rows):
        for i in range(cols):
            u = u0 + (i + 0.5 + (0.5 if j % 2 else 0)) * (u1 - u0) / cols
            if u > u1 - step * 0.3:
                continue
            v = v0 + (j + 0.5) * (v1 - v0) / rows
            c = colors[(i + j) % len(colors)]
            B.panel(c, [(u + x, v + y) for x, y in diamond(step * size)], O, ang, 0.12, off)


def ring_pattern(B, x, y, z0, z1, r0, r1, per_row, rows, colors=(TURQ, COBALT), size=0.7):
    """Lozenges round a (tapering) cylindrical shaft."""
    for j in range(rows):
        t = (j + 0.5) / rows
        z = z0 + (z1 - z0) * t
        r = r0 + (r1 - r0) * t
        s = (z1 - z0) / rows * size
        for i in range(per_row):
            a = math.tau * (i + (0.5 if j % 2 else 0)) / per_row
            B.panel(colors[(i + j) % len(colors)], [(px, py - s / 2) for px, py in diamond(s)], (x + r * math.cos(a), y + r * math.sin(a), z), a, 0.1, -0.02)


def kufic_ring(B, x, y, z, h, r, n, ground=COBALT, letter=TWHITE, sides=None):
    """Giant letters round a drum: a coloured band and white upright strokes."""
    sides = sides or max(16, n)
    B.lathe(ground, [(r * 1.02, 0), (r * 1.02, h)], x, y, z, sides)
    for i in range(n):
        a = math.tau * (i + 0.5) / n
        tall = 0.85 if i % 4 != 2 else 0.5
        w = math.tau * r / n * 0.32
        B.panel(letter, [(-w / 2, h * 0.12), (w / 2, h * 0.12), (w / 2, h * tall), (-w / 2, h * tall)], (x + r * 1.02 * math.cos(a), y + r * 1.02 * math.sin(a), z), a, 0.12)
    B.lathe(letter, [(r * 1.05, h * 0.06), (r * 1.05, h * 0.14)], x, y, z, sides, cap_top=False, cap_bottom=False)


def melon_dome(B, r, x, y, z, ribs=32, height=1.55, color=DOME, amp=0.07, bulb=1.12, rings=14, finial=GILT, rib_color=None, pointed=True):
    """A fluted Timurid dome: a bulbous profile with deep gores; rib count as on the building (64 at the Gur-e-Amir)."""
    H = r * height
    base = [(1.0, 0.0), (1.06, 0.10), (bulb, 0.24), (bulb * 0.995, 0.36), (bulb * 0.95, 0.48), (0.86, 0.60), (0.72, 0.72), (0.55, 0.82), (0.36, 0.91), (0.17, 0.97), (0.0, 1.0)]
    if not pointed:
        base = [(1.0, 0.0), (1.04, 0.12), (1.05, 0.28), (1.0, 0.45), (0.9, 0.6), (0.74, 0.74), (0.54, 0.86), (0.28, 0.96), (0.0, 1.0)]
    # resample the profile to the asked number of rings
    prof = []
    for k in range(rings + 1):
        t = k / rings * (len(base) - 1)
        i = min(int(t), len(base) - 2)
        f = t - i
        rr = base[i][0] * (1 - f) + base[i + 1][0] * f
        hh = base[i][1] * (1 - f) + base[i + 1][1] * f
        prof.append((r * rr, H * hh))
    prof[-1] = (0.0, H)
    n = ribs * 4 if ribs else 32
    mod = (lambda a, t: 1.0 + amp * (2 * abs(math.cos(ribs * a / 2)) - 1.2) * (1 - t * 0.6)) if ribs else None
    B.lathe(color, prof, x, y, z, n, mod, cap_bottom=True)
    if finial:
        B.lathe(finial, [(r * 0.06, 0), (r * 0.09, r * 0.06), (r * 0.03, r * 0.16), (r * 0.07, r * 0.24), (r * 0.02, r * 0.34), (0.0, r * 0.5)], x, y, z + H - r * 0.02, 8)
    return z + H


def smooth_dome(B, r, x, y, z, color=DOME, height=1.2, n=32, finial=GILT, rings=8):
    return melon_dome(B, r, x, y, z, ribs=0, height=height, color=color, amp=0.0, rings=rings, finial=finial, pointed=True)


def tree_b(B, x, y, z, r, kind="round", color=LEAF):
    B.box(WOOD_DK, x, y, z, r * 0.25, r * 0.25, r * 1.3)
    if kind == "poplar":
        B.lathe(color, [(r * 0.15, 0), (r * 0.5, r * 0.8), (r * 0.42, r * 2.6), (0.0, r * 3.8)], x, y, z + r * 0.8, 6)
    else:
        B.lathe(color, [(r * 0.2, 0), (r * 0.95, r * 0.45), (r * 0.9, r * 1.2), (r * 0.45, r * 1.7), (0.0, r * 1.85)], x, y, z + r * 0.9, 7)


# ---------------------------------------------------------------- Timurid parts

def portal(name, w, h, depth, body=BRICK_T, frame=TURQ, field=COBALT, recess=DEEP, aw=0.56, ah=0.74, guldasta=True, spandrel=None,
           pattern=(TURQ, TWHITE), muqarnas=True, crest=True, lite=False):
    """A pishtaq built at the origin with its face on y = 0 toward -Y and its body back along +Y: tile frames, an
    inscription band, banna'i side fields, a deep glazed arch with muqarnas, a door and corner guldastas."""
    B = Batch(name)
    B.box(body, 0, depth / 2, 0, w, depth, h)
    O = (0, 0, 0)
    a_w, a_h = w * aw, h * ah
    b = w * 0.028
    # outer frame and rope borders
    for s in (-1, 1):
        B.rect(frame, O, SOUTH, s * w * 0.47 - b / 2, s * w * 0.47 + b / 2, h * 0.02, h * 0.97, 0.22)
        B.rect(field, O, SOUTH, s * w * 0.435 - b * 0.35, s * w * 0.435 + b * 0.35, h * 0.02, h * 0.85, 0.2)
    B.rect(frame, O, SOUTH, -w * 0.47, w * 0.47, h * 0.955, h * 0.985, 0.22)
    if lite:
        B.rect(field, O, SOUTH, -w * 0.43, w * 0.43, h * 0.865, h * 0.945, 0.16)
        muqarnas = guldasta = False
    else:
        kufic_band(B, O, SOUTH, -w * 0.43, w * 0.43, h * 0.865, h * 0.945, field, TWHITE)
    # banna'i fields beside the arch
    side_u0 = a_w / 2 + w * 0.05
    for s in (-1, 1):
        u0, u1 = (side_u0, w * 0.415) if s > 0 else (-w * 0.415, -side_u0)
        if u1 - u0 > w * 0.04:
            B.rect(field, O, SOUTH, u0, u1, h * 0.03, h * 0.84, 0.1)
            if not lite:
                lozenge_field(B, O, SOUTH, u0, u1, h * 0.05, h * 0.82, max(0.9, (u1 - u0) / 3), pattern, 0.1)
    # spandrels and arch frame
    sp_top = min(h * 0.84, a_h + w * 0.1)
    B.rect(field, O, SOUTH, -a_w / 2 - w * 0.035, a_w / 2 + w * 0.035, a_h * 0.55, sp_top, 0.14)
    if spandrel == "tiger":
        for s in (-1, 1):
            cx = s * (a_w / 2 - a_w * 0.08)
            cz = a_h * 0.86
            # a tiger striding toward the centre with the sun-face on its back, a deer before it
            B.rect(TYEL, O, SOUTH, cx - s * a_w * 0.0 - a_w * 0.11, cx + a_w * 0.11, cz, cz + a_w * 0.07, 0.12, 0.14)
            B.rect(TYEL, O, SOUTH, cx + s * -a_w * 0.13 - a_w * 0.035, cx + s * -a_w * 0.13 + a_w * 0.035, cz + a_w * 0.03, cz + a_w * 0.1, 0.12, 0.14)
            for k in range(3):
                B.rect(DARK, O, SOUTH, cx - a_w * 0.08 + k * a_w * 0.06, cx - a_w * 0.065 + k * a_w * 0.06, cz + a_w * 0.01, cz + a_w * 0.06, 0.06, 0.26)
            sun = [(cx + a_w * 0.06 * math.cos(math.tau * i / 12), cz + a_w * 0.16 + a_w * 0.06 * math.sin(math.tau * i / 12)) for i in range(12)]
            B.panel(TYEL, sun, O, SOUTH, 0.12, 0.14)
            B.panel(TWHITE, [(u * 0.55 + cx * 0.45, (v - cz - a_w * 0.16) * 0.55 + cz + a_w * 0.16) for u, v in sun], O, SOUTH, 0.08, 0.26)
            B.rect(TWHITE, O, SOUTH, cx - s * a_w * 0.2 - a_w * 0.04, cx - s * a_w * 0.2 + a_w * 0.04, cz - a_w * 0.05, cz + a_w * 0.0, 0.12, 0.14)
    elif spandrel:
        for s in (-1, 1):
            cx = s * (a_w / 2 - a_w * 0.02)
            ring = [(cx + a_w * 0.07 * math.cos(math.tau * i / 10), a_h * 0.9 + a_w * 0.07 * math.sin(math.tau * i / 10)) for i in range(10)]
            B.panel(spandrel, ring, O, SOUTH, 0.1, 0.14)
    B.panel(frame, arch_outline(a_w + w * 0.05, a_h + w * 0.04), O, SOUTH, 0.24)
    B.panel(recess, arch_outline(a_w, a_h), O, SOUTH, 0.3)
    if muqarnas:
        # tiers of small cells in the arch head
        for t in range(4):
            v = a_h * (0.62 + t * 0.075)
            span = a_w * (0.86 - t * 0.2)
            n = max(2, 7 - t * 2)
            for i in range(n):
                u = -span / 2 + (i + 0.5) * span / n
                B.panel(TURQ_LT if (i + t) % 2 else TWHITE, arch_outline(span / n * 0.7, a_h * 0.06), (0, 0, v), SOUTH, 0.12, 0.3)
    # door, window grille and tiled dado inside the recess
    B.panel(DOOR, arch_outline(a_w * 0.34, a_h * 0.38), O, SOUTH, 0.15, 0.3)
    B.rect(TURQ_LT, O, SOUTH, -a_w * 0.08, a_w * 0.08, a_h * 0.45, a_h * 0.56, 0.1, 0.3)
    for s in (-1, 1):
        B.rect(frame, O, SOUTH, s * a_w * 0.3 - a_w * 0.09, s * a_w * 0.3 + a_w * 0.09, a_h * 0.06, a_h * 0.42, 0.1, 0.3)
        B.panel(DEEP, arch_outline(a_w * 0.12, a_h * 0.3), (s * a_w * 0.3, 0, a_h * 0.08), SOUTH, 0.08, 0.4)
    if guldasta:
        for s in (-1, 1):
            gx = s * w * 0.5
            gr = max(0.35, w * 0.032)
            B.lathe(frame, [(gr, 0), (gr * 0.9, h * 1.03)], gx, gr * 0.6, 0, 10)
            for k in range(1, 6):
                B.lathe(field, [(gr * 1.06, h * k / 6), (gr * 1.06, h * k / 6 + gr * 0.8)], gx, gr * 0.6, 0, 10, cap_top=False, cap_bottom=False)
            B.lathe(TWHITE, [(gr * 1.3, h * 1.03), (gr * 1.2, h * 1.03 + gr)], gx, gr * 0.6, 0, 10)
            B.lathe(TURQ, [(gr * 1.0, h * 1.03 + gr), (gr * 0.8, h * 1.03 + gr * 1.6), (0.0, h * 1.03 + gr * 2.6)], gx, gr * 0.6, 0, 10)
    if crest:
        n = max(4, int(w / 2.5))
        for i in range(n):
            B.box(body, -w / 2 + (i + 0.5) * w / n, depth * 0.3, h, w / n * 0.5, 0.5, 0.7)
    return B.build()


def place_portal(o, x, y, z=0.0, facing="S"):
    return put(o, x, y, z, FACING[facing])


def t_minaret(name, r, h, x, y, z=0.0, body=BRICK_T, colors=(TURQ, COBALT), cap="lantern", sides=16, taper=0.84, rows=None, broken=None):
    """A Timurid minaret: octagonal plinth, tapering brick shaft netted with glazed lozenges, inscription bands,
    a muqarnas balcony and a small domed lantern. broken = height at which a ruined shaft stops."""
    B = Batch(name)
    B.prism(BRICK_DK, ngon(r * 1.22, 8), z, r * 1.6, x, y)
    B.prism(COBALT, ngon(r * 1.25, 8), z + r * 1.2, r * 0.3, x, y)
    top = broken or h
    rt = r * (1 - (1 - taper) * top / h)
    B.lathe(body, [(r, 0), (rt, top)], x, y, z + r * 1.6, sides, cap_top=bool(broken))
    shaft_top = z + r * 1.6 + top
    bands = [0.28, 0.62, 0.9]
    zs = [z + r * 1.6] + [z + r * 1.6 + h * f for f in bands if h * f < top - r * 0.6]
    for k, zb in enumerate(zs[1:], 1):
        rb = r * (1 - (1 - taper) * (zb - z - r * 1.6) / h)
        kufic_ring(B, x, y, zb, r * 0.8, rb, max(8, int(rb * 4.2)), COBALT, TWHITE, sides)
    # lozenge net between the bands
    segs = list(zip(zs, zs[1:] + [shaft_top - r * 0.3]))
    for k, (z0, z1) in enumerate(segs):
        z0 += r * (0.9 if k else 0.3)
        if z1 - z0 < r:
            continue
        r0 = r * (1 - (1 - taper) * (z0 - z - r * 1.6) / h)
        r1 = r * (1 - (1 - taper) * (z1 - z - r * 1.6) / h)
        nrow = rows or max(2, int((z1 - z0) / (r * 1.25)))
        ring_pattern(B, x, y, z0, z1, r0, r1, max(8, int(r0 * 4.2)), nrow, colors)
    if broken:
        for i in range(5):
            a = math.tau * i / 5
            B.box(body, x + rt * 0.7 * math.cos(a), y + rt * 0.7 * math.sin(a), shaft_top, rt * 0.5, rt * 0.5, r * (0.4 + 0.3 * (i % 2)), a)
        return B.build()
    # muqarnas balcony
    B.lathe(TURQ, [(rt * 1.0, 0), (rt * 1.12, r * 0.35), (rt * 1.22, r * 0.36), (rt * 1.32, r * 0.7), (rt * 1.42, r * 0.72), (rt * 1.5, r * 1.05)], x, y, shaft_top, sides)
    for i in range(0, sides, 2):
        a = math.tau * (i + 0.5) / sides
        B.panel(TWHITE, arch_outline(rt * 0.5, r * 0.3), (x + rt * 1.15 * math.cos(a), y + rt * 1.15 * math.sin(a), shaft_top + r * 0.38), a, 0.06)
    B.lathe(BRICK_LT, [(rt * 1.5, 0), (rt * 1.5, r * 0.5)], x, y, shaft_top + r * 1.05, sides)
    if cap == "lantern":
        lz = shaft_top + r * 1.55
        B.prism(BRICK_LT, ngon(rt * 0.72, 8), lz - r * 0.5, rt * 1.6 + r * 0.5, x, y)
        for i in range(8):
            a = math.tau * i / 8
            B.panel(DARK, arch_outline(rt * 0.4, rt * 1.0), (x + rt * 0.72 * math.cos(math.pi / 8) * math.cos(a), y + rt * 0.72 * math.cos(math.pi / 8) * math.sin(a), lz + rt * 0.2), a, 0.06)
        melon_dome(B, rt * 0.8, x, y, lz + rt * 1.6, ribs=8, height=1.3, color=TURQ, amp=0.05, rings=6)
    elif cap == "stump":
        B.lathe(BRICK_LT, [(rt * 1.0, 0), (rt * 0.9, r * 0.8)], x, y, shaft_top + r * 1.55, sides)
    return B.build()


def niche_row_at(B, cx, cy, z0, ang, u0, u1, h, n, storeys=2, frame=TURQ, recess=DEEP, field=None, off=0.0, spandrel=None):
    """Like niche_rows but placing each niche at its own centre on a wall plane through (cx, cy) with outward normal ang."""
    ux, uy = -math.sin(ang), math.cos(ang)
    sh = h / storeys
    bay = (u1 - u0) / n
    for st in range(storeys):
        for i in range(n):
            u = u0 + (i + 0.5) * bay
            O = (cx + ux * u, cy + uy * u, z0 + st * sh)
            if field:
                B.rect(field, O, ang, -bay * 0.47, bay * 0.47, sh * 0.03, sh * 0.97, 0.1, off)
                if spandrel:
                    for s in (-1, 1):
                        B.panel(spandrel, diamond(bay * 0.1), (O[0] + ux * s * bay * 0.36, O[1] + uy * s * bay * 0.36, O[2] + sh * 0.84), ang, 0.08, off + 0.1)
            B.panel(frame, arch_outline(bay * 0.72, sh * 0.86), (O[0], O[1], O[2] + sh * 0.05), ang, 0.16, off)
            B.panel(recess, arch_outline(bay * 0.6, sh * 0.78), (O[0], O[1], O[2] + sh * 0.06), ang, 0.24, off)


def drum_dome(B, r, x, y, z, drum_h, ribs=24, color=DOME, height=1.45, kufic=True, drum=BRICK_T, n_letters=None, amp=0.07, rings=12):
    """A drum (with giant letters) and a ribbed dome on top; returns the top height."""
    if kufic:
        B.lathe(drum, [(r * 0.98, 0), (r * 0.98, drum_h * 0.18)], x, y, z, max(24, ribs * 2))
        kufic_ring(B, x, y, z + drum_h * 0.18, drum_h * 0.72, r * 0.98, n_letters or max(12, int(r * 3)), COBALT, TWHITE, max(24, ribs * 2))
        B.lathe(TURQ, [(r * 1.02, drum_h * 0.9), (r * 1.06, drum_h)], x, y, z, max(24, ribs * 2))
    else:
        B.lathe(drum, [(r * 0.98, 0), (r * 0.98, drum_h)], x, y, z, max(24, ribs * 2))
    return melon_dome(B, r, x, y, z + drum_h, ribs=ribs, height=height, color=color, amp=amp, rings=rings)


def madrasa(name, W, D, H, portal_w, portal_h, minaret_h=0.0, minarets="front", corner_domes=True, dome_ribs=24, dome_color=DOME, bays=3,
            spandrel=None, court_iwans=True, big_dome=None, body=BRICK_T, pattern=(TURQ, COBALT), field=None, extra=None):
    """A madrasa facing -Y at the origin: two-storey ring of cells round a court, a facade of niche loggias either side of a
    great pishtaq, domed lecture halls at the front corners and minarets at the corners. Returns a list of objects."""
    out = []
    B = Batch(name + "_body")
    dep = D * 0.2
    # ranges of cells
    B.box(body, 0, -D / 2 + dep / 2, 0, W, dep, H)
    B.box(body, 0, D / 2 - dep / 2, 0, W, dep, H)
    B.box(body, -W / 2 + dep / 2, 0, 0, dep, D - 2 * dep, H)
    B.box(body, W / 2 - dep / 2, 0, 0, dep, D - 2 * dep, H)
    B.box(PAVE, 0, 0, 0, W - 2 * dep, D - 2 * dep, 0.25)
    B.box(WATER_C, 0, 0, 0, 4, 4, 0.4)
    for s in (-1, 1):
        tree_b(B, s * (W / 2 - dep - 4), D * 0.1, 0.25, 1.6)
    # parapet line and tile cornice
    for (cx, cy, w, d) in ((0, -D / 2 + dep / 2, W, dep), (0, D / 2 - dep / 2, W, dep), (-W / 2 + dep / 2, 0, dep, D), (W / 2 - dep / 2, 0, dep, D)):
        B.box(BRICK_LT, cx, cy, H, w + 0.3, d + 0.3, 0.5)
    # facade: niche loggias and an inscription frieze
    fy = -D / 2
    side_w = (W - portal_w) / 2
    for s in (-1, 1):
        u0 = s * portal_w / 2 if s > 0 else -W / 2 + (6 if minarets else 1)
        u1 = W / 2 - (6 if minarets else 1) if s > 0 else -portal_w / 2
        niche_row_at(B, 0, fy, H * 0.06, SOUTH, u0, u1, H * 0.86, bays, 2, TURQ, DEEP, field or COBALT, 0.0, TWHITE)
    kufic_band(B, (0, fy, 0), SOUTH, -W / 2 + 1, W / 2 - 1, H * 0.92, H * 0.99, COBALT, TWHITE, 0.0, 1.8)
    lozenge_field(B, (0, fy, 0), SOUTH, -W / 2 + 1, W / 2 - 1, 0.2, H * 0.06, 1.0, pattern, 0.0)
    # sides and back: tile bands and a row of niches
    for ang, cx, cy, L in ((WEST, -W / 2, 0, D), (EAST, W / 2, 0, D), (NORTH, 0, D / 2, W)):
        niche_row_at(B, cx, cy, H * 0.12, ang, -L / 2 + 6, L / 2 - 6, H * 0.7, max(3, int(L / 9)), 1, BRICK_LT, DEEP, None)
        kufic_band(B, (cx, cy, 0), ang, -L / 2 + 1, L / 2 - 1, H * 0.9, H * 0.98, COBALT, TWHITE, 0.0, 2.6)
    # court facades: iwans on the axes and two storeys of hujra niches
    for ang, cx, cy, L in ((NORTH, 0, -D / 2 + dep, W - 2 * dep), (SOUTH, 0, D / 2 - dep, W - 2 * dep), (EAST, -W / 2 + dep, 0, D - 2 * dep), (WEST, W / 2 - dep, 0, D - 2 * dep)):
        niche_row_at(B, cx, cy, 0.25, ang, -L / 2 + 1, L / 2 - 1, H * 0.85, max(3, int(L / 8)), 2, BRICK_LT, DEEP, None)
    if corner_domes:
        for s in (-1, 1):
            x0 = s * (W / 2 - dep / 2 - 1)
            drum_dome(B, dep * 0.32, x0, -D / 2 + dep / 2, H, dep * 0.25, 16, dome_color, 1.4, rings=10)
    if big_dome:
        bx, by, br = big_dome
        B.box(body, bx, by, 0, br * 2.4, br * 2.4, H * 1.15)
        drum_dome(B, br, bx, by, H * 1.15, br * 0.7, dome_ribs, dome_color, 1.0, kufic=True)
    if extra:
        extra(B)
    out.append(B.build())
    # the great portal on the facade
    p = portal(name + "_portal", portal_w, portal_h, 5.0, BRICK_T, TURQ, COBALT, DEEP, spandrel=spandrel, pattern=pattern)
    out.append(put(p, 0, fy - 2, 0))
    if court_iwans:
        for f, (cx, cy) in (("N", (0, -D / 2 + dep + 0.1)), ("S", (0, D / 2 - dep - 0.1)), ("E", (-W / 2 + dep + 0.1, 0)), ("W", (W / 2 - dep - 0.1, 0))):
            iw = portal(f"{name}_iw{f}", min(W, D) * 0.2, H * 1.25, 2.0, BRICK_T, TURQ, COBALT, DEEP, crest=False, lite=True)
            out.append(put(iw, cx, cy, 0, FACING[f]))
    if minaret_h:
        spots = [(-W / 2, -D / 2), (W / 2, -D / 2)] + ([(-W / 2, D / 2), (W / 2, D / 2)] if minarets == "all" else [])
        r = max(1.6, minaret_h * 0.06)
        for i, (mx, my) in enumerate(spots):
            out.append(t_minaret(f"{name}_min{i}", r, minaret_h, mx, my, 0, BRICK_T, pattern, "lantern"))
    return out


# ---------------------------------------------------------------- small common pieces

def stalls(B, x0, y0, nx, ny, sx=5.0, sy=6.0, z=0.3, seed=0, heaps=True):
    """Rows of market booths with cloth awnings and heaps of produce."""
    k = seed
    for j in range(ny):
        for i in range(nx):
            x, y = x0 + i * sx, y0 + j * sy
            B.box(MUD, x, y + sy * 0.18, z, sx * 0.86, sy * 0.3, 2.4)
            B.box(AWNINGS[(i + j + k) % len(AWNINGS)], x, y - sy * 0.05, z + 2.3, sx * 0.9, sy * 0.55, 0.18)
            for s in (-1, 1):
                B.box(WOOD_DK, x + s * sx * 0.4, y - sy * 0.3, z, 0.18, 0.18, 2.3)
            if heaps and (i + j + k) % 2 == 0:
                c = ["#D8B848", "#8FA65A", "#C0623F", "#E0C27A"][(i * 3 + j + k) % 4]
                B.lathe(c, [(0.9, 0), (0.75, 0.45), (0.0, 0.75)], x, y - sy * 0.45, z, 7)


def flat_houses(B, specs, z=0.3, color=MUD):
    """Plain flat-roofed houses: (x, y, w, d, h)."""
    for i, (x, y, w, d, h) in enumerate(specs):
        c = [color, shade(color, 0.1), shade(color, -0.08)][i % 3]
        B.box(c, x, y, z, w, d, h)
        B.box(shade(c, -0.12), x, y, z + h, w + 0.3, d + 0.3, 0.35)
        B.rect(DOOR, (x, y - d / 2, z), SOUTH, -0.6, 0.6, 0, 2.0, 0.1)


def tim_dome(B, x, y, z, r, h, color=BRICK_LT, arms=True):
    """A domed market crossing: square hall with four arms, a drum with windows and a dome."""
    B.box(color, x, y, z, r * 2.2, r * 2.2, h)
    if arms:
        B.box(color, x, y, z, r * 4.4, r * 1.1, h * 0.75)
        B.box(color, x, y, z, r * 1.1, r * 4.4, h * 0.75)
        for ang, dx, dy in ((SOUTH, 0, -r * 2.2), (NORTH, 0, r * 2.2), (EAST, r * 2.2, 0), (WEST, -r * 2.2, 0)):
            B.panel(DOOR, arch_outline(r * 0.6, h * 0.6), (x + dx, y + dy, z), ang, 0.12)
    B.prism(color, ngon(r * 0.95, 8), z + h, r * 0.35, x, y)
    for i in range(8):
        a = math.tau * i / 8
        B.panel(DARK, arch_outline(r * 0.22, r * 0.25), (x + r * 0.95 * math.cos(math.pi / 8) * math.cos(a), y + r * 0.95 * math.cos(math.pi / 8) * math.sin(a), z + h + r * 0.04), a, 0.05)
    smooth_dome(B, r * 0.92, x, y, z + h + r * 0.35, color, 1.1, finial=None)


def wall_ring(B, pts, h, t, color, towers=0.0, tower_h=None, every=None, merlons=True, z=0.0, square=False):
    """A closed wall along points with towers at the corners (and every `every` metres)."""
    n = len(pts)
    for i in range(n):
        (ax, ay), (bx, by) = pts[i], pts[(i + 1) % n]
        L = math.hypot(bx - ax, by - ay)
        a = math.atan2(by - ay, bx - ax)
        B.box(color, (ax + bx) / 2, (ay + by) / 2, z, L + t, t, h, a)
        if merlons:
            k = max(1, int(L / 2.4))
            for j in range(k):
                u = -L / 2 + (j + 0.5) * L / k
                B.box(color, (ax + bx) / 2 + math.cos(a) * u, (ay + by) / 2 + math.sin(a) * u, z + h, 1.1, t * 0.8, 1.1, a)
        if towers:
            m = max(1, round(L / every)) if every else 1
            for j in range(m):
                tx, ty = ax + (bx - ax) * j / m, ay + (by - ay) * j / m
                th = tower_h or h * 1.25
                if square:
                    B.box(shade(color, -0.05), tx, ty, z, towers * 2, towers * 2, th, a)
                else:
                    B.lathe(shade(color, -0.05), [(towers * 1.06, 0), (towers, th)], tx, ty, z, 12)


# ---------------------------------------------------------------- the Registan

def _khanaqah(name):
    """Ulugh Beg's khanaqah: a great domed hall behind a portal, with wings (facing -Y)."""
    out = []
    B = Batch(name)
    B.box(BRICK_T, 0, 6, 0, 54, 44, 12)
    B.box(BRICK_T, 0, 8, 0, 30, 30, 18)
    niche_row_at(B, 0, -16, 0.6, SOUTH, -27, -13, 10.5, 2, 2, TURQ, DEEP, COBALT, 0.0, TWHITE)
    niche_row_at(B, 0, -16, 0.6, SOUTH, 13, 27, 10.5, 2, 2, TURQ, DEEP, COBALT, 0.0, TWHITE)
    kufic_band(B, (0, -16, 0), SOUTH, -26.5, 26.5, 10.8, 11.8, COBALT, TWHITE)
    kufic_band(B, (0, -7, 0), SOUTH, -14.5, 14.5, 16.4, 17.6, COBALT, TWHITE)
    drum_dome(B, 11, 0, 8, 18, 7, 32, DOME, 1.35)
    for s in (-1, 1):
        drum_dome(B, 4.5, s * 20, 18, 12, 2.5, 16, DOME, 1.3, kufic=False)
    out.append(B.build())
    out.append(put(portal(name + "_p", 24, 28, 9, spandrel=TWHITE), 0, -18))
    return out


def _caravanserai(name, W=96, D=44, H=9):
    out = []
    B = Batch(name)
    dep = 9
    for (cx, cy, w, d) in ((0, -D / 2 + dep / 2, W, dep), (0, D / 2 - dep / 2, W, dep), (-W / 2 + dep / 2, 0, dep, D), (W / 2 - dep / 2, 0, dep, D)):
        B.box(BRICK_T, cx, cy, 0, w, d, H)
        B.box(BRICK_LT, cx, cy, H, w + 0.3, d + 0.3, 0.4)
    B.box(PAVE, 0, 0, 0, W - 2 * dep, D - 2 * dep, 0.25)
    niche_row_at(B, 0, -D / 2, 0.5, SOUTH, -W / 2 + 2, -10, H * 0.85, 6, 2, BRICK_LT, DEEP, None)
    niche_row_at(B, 0, -D / 2, 0.5, SOUTH, 10, W / 2 - 2, H * 0.85, 6, 2, BRICK_LT, DEEP, None)
    for ang, cx, cy, L in ((NORTH, 0, -D / 2 + dep, W - 2 * dep), (SOUTH, 0, D / 2 - dep, W - 2 * dep)):
        niche_row_at(B, cx, cy, 0.25, ang, -L / 2, L / 2, H * 0.85, int(L / 5), 2, BRICK_LT, DARK, None)
    for i in range(6):
        B.box(["#B8553E", "#D9C9A0", "#4E6E8E"][i % 3], -30 + i * 12, 0, 0.25, 3, 2, 1.4)
    for s in (-1, 1):
        B.lathe(BRICK_T, [(2.6, 0), (2.4, H * 1.3)], s * W / 2, -D / 2, 0, 12)
        smooth_dome(B, 2.4, s * W / 2, -D / 2, H * 1.3, BRICK_LT, 0.9, finial=None)
    out.append(B.build())
    out.append(put(portal(name + "_p", 18, 16, dep + 2, BRICK_T, BRICK_LT, COBALT, DEEP, guldasta=False, pattern=(TURQ, BRICK_LT)), 0, -D / 2 - 2))
    return out


def registan(era="1440"):
    m = Model("registan-" + era)
    G = Batch("reg_ground")
    G.box(GROUND, 0, 0, 0, 196, 184, 0.3)
    G.box(PAVE, 0, -30, 0.3, 70, 120, 0.12)
    if era != "1404":
        G.box(PAVE_DK, 0, -10, 0.3, 66, 54, 0.16)
    m.add(0, G.build(), "square")
    if era == "1404":
        B = Batch("reg_market")
        stalls(B, -26, -70, 11, 3, 5.2, 7, 0.3, 0)
        stalls(B, -26, 10, 11, 2, 5.2, 7, 0.3, 2)
        tim_dome(B, -62, -10, 0.3, 7, 7)
        tim_dome(B, 62, 20, 0.3, 6, 6)
        B.box(WATER_C, 40, -40, 0.3, 3, 70, 0.4)
        for i in range(6):
            tree_b(B, 46, -70 + i * 12, 0.3, 2.2)
        B.box(WATER_C, 0, -24, 0.3, 9, 9, 0.45)
        B.box(BRICK_LT, 0, -24, 0.3, 10, 10, 0.3)
        flat_houses(B, [(-80, 40, 18, 20, 5), (-80, 70, 18, 22, 6), (-55, 70, 16, 20, 5), (75, -60, 22, 18, 5), (80, -20, 16, 22, 6), (78, 60, 20, 26, 5),
                        (-78, -60, 20, 20, 5), (-58, -78, 16, 12, 4), (55, -82, 18, 12, 4), (20, 75, 22, 18, 5), (-20, 78, 20, 14, 5), (50, 70, 18, 20, 6)])
        m.add(1, B.build(), "market")
        # a small mosque of the square with a ribbed dome
        Q = Batch("reg_mosque")
        Q.box(BRICK_T, 70, -10, 0.3, 18, 18, 7)
        drum_dome(Q, 6, 70, -10, 7.3, 2.5, 16, DOME, 1.3, kufic=False)
        m.add(2, Q.build(), "mosque")
        m.add(2, put(portal("reg_mq_p", 9, 10, 2, guldasta=False, muqarnas=False), 61, -10, 0, FACING["W"]), "mosque")
        return m
    # Ulugh Beg's madrasa on the west, facing east
    for o in madrasa("ub", 56, 58, 14, 30, 34, 33, "all", True, 24, DOME, 3, spandrel=TWHITE):
        m.add(1, put(o, -65, -10, 0, FACING["E"]), "ulugh beg madrasa")
    if era == "1440":
        for o in _khanaqah("khanaqah"):
            m.add(2, put(o, 65, -10, 0, FACING["W"]), "khanaqah")
        for o in _caravanserai("mirzoi"):
            m.add(2, put(o, 0, 62, 0, FACING["S"]), "caravanserai")
        B = Batch("reg_stalls")
        stalls(B, -24, -80, 10, 2, 5.2, 7, 0.3, 1)
        B.box(WATER_C, 0, -45, 0.3, 8, 8, 0.45)
        B.box(TWHITE, 0, -45, 0.3, 9, 9, 0.3)
        m.add(2, B.build(), "market")
    else:
        # Sher-Dor, mirroring Ulugh Beg's madrasa, with its tigers and two great ribbed domes
        def sd_domes(B):
            for s in (-1, 1):
                B.box(BRICK_T, s * 20, -14, 0, 13, 13, 17)
                drum_dome(B, 6.2, s * 20, -14, 17, 5.5, 24, DOME, 1.55)
        for o in madrasa("sherdor", 56, 58, 14, 30, 34, 31, "front", False, 24, DOME, 3, spandrel="tiger", pattern=(TURQ, TYEL), extra=sd_domes):
            m.add(2, put(o, 65, -10, 0, FACING["W"]), "sher-dor")
        # Tilya-Kori: a long two-storey front, corner towers, the mosque dome on the west of its court
        for o in madrasa("tilyakori", 110, 52, 12, 26, 30, 16, "front", False, 24, TURQ, 5, pattern=(TURQ, TYEL), big_dome=(-30, 8, 8.5)):
            m.add(2, put(o, 0, 62, 0, FACING["S"]), "tilya-kori")
    return m


# ---------------------------------------------------------------- Bibi-Khanym

def bibi_khanym(ruin=False):
    m = Model("bibi-khanym" + ("-1650" if ruin else ""))
    W, D = 109, 167
    G = Batch("bk_ground")
    G.box(GROUND, 0, 0, 0, W + 4, D + 4, 0.3)
    G.box(PAVE, 0, -16, 0.3, 90, 112, 0.12)
    G.box(TWHITE, 0, 18, 0.3, 4.2, 2.6, 0.7)
    G.box(TWHITE, 0, 18, 1.0, 3.6, 1.8, 1.6)
    G.frustum(TWHITE, 0, 18, 2.6, 3.6, 1.8, 0.5, 1.8, 1.0)
    for x, y in ((-30, -45), (30, -45), (-30, -10), (30, -10), (-20, 30), (20, 30)):
        tree_b(G, x, y, 0.3, 3.0 if not ruin else 2.4)
    if ruin:
        for x, y, s in ((8, 50, 10), (-10, 60, 8), (36, 6, 7), (-14, -70, 5)):
            G.frustum(RUBBLE, x, y, 0.3, s, s * 0.8, s * 0.3, s * 0.25, s * 0.25)
    m.add(0, G.build(), "court")
    # enclosure ranges with galleries
    B = Batch("bk_walls")
    t, H = 8, 13
    for (cx, cy, w, d) in ((-W / 2 + t / 2, 0, t, D), (W / 2 - t / 2, 0, t, D), (-(W / 2 + 24) / 2 - 0.0, -D / 2 + t / 2, W / 2 - 22, t), ((W / 2 + 24) / 2, -D / 2 + t / 2, W / 2 - 22, t),
                           (-(W / 2 + 24) / 2, D / 2 - t / 2, W / 2 - 24, t), ((W / 2 + 24) / 2, D / 2 - t / 2, W / 2 - 24, t)):
        B.box(BRICK_T, cx, cy, 0, w, d, H if not ruin else H * 0.8)
        B.box(BRICK_LT, cx, cy, H if not ruin else H * 0.8, w + 0.3, d + 0.3, 0.4)
    hh = H if not ruin else H * 0.8
    # outer faces: blind niches and banna'i bands, inner faces: the galleries of the court
    for ang, cx, cy, L in ((WEST, -W / 2, 0, D), (EAST, W / 2, 0, D)):
        niche_row_at(B, cx, cy, 0.4, ang, -L / 2 + 4, L / 2 - 4, hh * 0.8, 14, 1, BRICK_LT, DEEP, None)
        lozenge_field(B, (cx, cy, 0), ang, -L / 2 + 2, L / 2 - 2, hh * 0.84, hh * 0.98, 1.6, (TURQ, COBALT))
        inner = cx - math.copysign(t, cx)
        niche_row_at(B, inner, cy, 0.3, ang + math.pi, -L / 2 + 10, L / 2 - 10, hh * 0.8, 18, 1, BRICK_LT, DARK, None)
    for s in (-1, 1):
        x0, x1 = (24, W / 2) if s > 0 else (-W / 2, -24)
        for ang, cy in ((SOUTH, -D / 2), (NORTH, D / 2)):
            uu = (x0, x1) if ang == SOUTH else (-x1, -x0)
            niche_row_at(B, 0, cy, 0.4, ang, uu[0] + 2, uu[1] - 2, hh * 0.8, 3, 1, BRICK_LT, DEEP, None)
            lozenge_field(B, (0, cy, 0), ang, uu[0] + 1, uu[1] - 1, hh * 0.84, hh * 0.98, 1.6, (TURQ, COBALT))
        niche_row_at(B, 0, -D / 2 + t, 0.3, NORTH, -x1 + 2, -x0 - 2, hh * 0.8, 3, 1, BRICK_LT, DARK, None)
    m.add(0, B.build(), "walls")
    # main portal with its two great minarets
    if not ruin:
        m.add(1, put(portal("bk_portal", 46, 35, 14, spandrel=TWHITE), 0, -D / 2 - 2), "portal")
    else:
        P = portal("bk_portal", 46, 29, 14, crest=False, guldasta=False, muqarnas=False)
        m.add(1, put(P, 0, -D / 2 - 2), "portal")
        R = Batch("bk_portal_break")
        for i in range(9):
            R.box(BRICK_T, -20 + i * 5, -D / 2 + 5, 29, 4, 12, 1.0 + (i * 7 % 5) * 0.8)
        m.add(1, R.build(), "portal")
    for s in (-1, 1):
        m.add(1, t_minaret(f"bk_pm{s}", 3.4, 47, s * 25, -D / 2 + 3, 0, BRICK_T, (TURQ, COBALT), "lantern", broken=(30 if s < 0 else 20) if ruin else None), "portal")
    # side mosques with ribbed domes facing the court
    S2 = Batch("bk_side")
    for s in (-1, 1):
        x = s * (W / 2 - 14)
        S2.box(BRICK_T, x, 0, 0, 28, 28, 16)
        niche_row_at(S2, x - s * 0, -14, 0.4, SOUTH, -12, 12, 12, 3, 1, BRICK_LT, DEEP, None)
        niche_row_at(S2, x, 14, 0.4, NORTH, -12, 12, 12, 3, 1, BRICK_LT, DEEP, None)
        if ruin and s > 0:
            S2.lathe(BRICK_T, [(8.2, 0), (8.2, 2.5)], x, 0, 16, 32)
            S2.frustum(RUBBLE, x, 0, 18.5, 10, 10, 4, 4, 2)
        else:
            drum_dome(S2, 8.4, x, 0, 16, 5, 24, DOME, 1.4)
    m.add(2, S2.build(), "side mosques")
    for s in (-1, 1):
        f = "E" if s < 0 else "W"
        m.add(2, put(portal(f"bk_sp{s}", 20, 25, 3, spandrel=TWHITE), s * (W / 2 - 28), 0, 0, FACING[f]), "side mosques")
    # the sanctuary and its giant dome
    T = Batch("bk_sanct")
    T.box(BRICK_T, 0, 64, 0, 50, 42, 24)
    for ang, cx, cy, L in ((WEST, -25, 64, 42), (EAST, 25, 64, 42), (NORTH, 0, 85, 50)):
        niche_row_at(T, cx, cy, 0.5, ang, -L / 2 + 2, L / 2 - 2, 20, 4, 2, TURQ, DEEP, COBALT, 0.0, TWHITE)
        kufic_band(T, (cx, cy, 0), ang, -L / 2 + 0.5, L / 2 - 0.5, 21.5, 23.5, COBALT, TWHITE)
    if ruin:
        T.lathe(COBALT, [(14.2, 0), (14.2, 9)], 0, 66, 24, 48, cap_top=False)
        prof = [(14.2 * f, 9 + 16 * h) for f, h in ((1.0, 0.0), (1.1, 0.25), (1.08, 0.45), (0.95, 0.62), (0.75, 0.78))]
        T.lathe(DOME, prof, 0, 66, 24, 64, start=0.4, arc=math.tau * 0.62, cap_top=False, cap_bottom=False)
        T.frustum(RUBBLE, 0, 62, 24, 18, 16, 6, 6, 3)
    else:
        drum_dome(T, 14.2, 0, 66, 24, 9, 36, DOME, 1.3, n_letters=40)
    m.add(3, T.build(), "dome")
    m.add(3, put(portal("bk_sanct_p", 40, 38 if not ruin else 33, 6, spandrel=TWHITE, crest=not ruin), 0, 41), "dome")
    if not ruin:
        for s in (-1, 1):
            m.add(3, t_minaret(f"bk_sm{s}", 2.3, 40, s * 22, 41.5, 0, BRICK_T, (TURQ, COBALT), "lantern"), "dome")
    for i, (sx, sy) in enumerate(((-1, -1), (1, -1), (-1, 1), (1, 1))):
        if ruin and i in (1, 2):
            continue
        m.add(3, t_minaret(f"bk_cm{i}", 3.0, 36, sx * W / 2, sy * D / 2, 0, BRICK_T, (TURQ, COBALT), "lantern", broken=(12 if i == 0 else 22) if ruin else None), "minarets")
    return m


# ---------------------------------------------------------------- Gur-e-Amir

def gur_e_amir():
    """Built with the entrance portal toward -Y and the tomb at +Y; the landmark is turned 180 degrees so the portal faces north."""
    m = Model("gur-e-amir")
    G = Batch("ga_ground")
    G.box(GROUND, 0, 0, 0, 82, 102, 0.3)
    G.box(PAVE, 0, -16, 0.3, 42, 44, 0.12)
    G.box(WATER_C, 0, -16, 0.3, 3.5, 3.5, 0.45)
    for x, y in ((-14, -28), (14, -28), (-14, -6), (14, -6)):
        tree_b(G, x, y, 0.3, 2.4)
    m.add(0, G.build(), "court")
    # Muhammad Sultan's madrasa (west) and khanaqah (east) round the court, and the front wall
    B = Batch("ga_court")
    for s in (-1, 1):
        x = s * 31
        B.box(BRICK_T, x, -19, 0, 18, 54, 9)
        B.box(BRICK_LT, x, -19, 9, 18.3, 54.3, 0.4)
        niche_row_at(B, x - s * 9, -19, 0.3, EAST if s < 0 else WEST, -25, 25, 8, 6, 2, BRICK_LT, DEEP, None)
        niche_row_at(B, x + s * 9, -19, 0.6, WEST if s < 0 else EAST, -25, 25, 7, 5, 1, BRICK_LT, DEEP, None)
        kufic_band(B, (x + s * 9, -19, 0), WEST if s < 0 else EAST, -26, 26, 7.6, 8.8, COBALT, TWHITE)
        B.box(BRICK_T, s * 15.5, -46, 0, 13, 3, 8)
        lozenge_field(B, (s * 15.5, -47.5, 0), SOUTH, -6, 6, 1.0, 7.4, 1.3, (TURQ, COBALT))
    drum_dome(B, 6, 31, -19, 9.4, 2.5, 20, DOME, 1.4, kufic=False)
    B.box(BRICK_T, -31, -38, 9.4, 8, 8, 3)
    smooth_dome(B, 3.6, -31, -38, 12.4, BRICK_LT, 1.15, finial=None)
    m.add(0, B.build(), "madrasa and khanaqah")
    m.add(1, put(portal("ga_portal", 18, 22, 5, spandrel=TWHITE), 0, -50), "portal")
    # the tomb: octagonal chamber, tile-netted walls, a drum of giant letters, the 64-ribbed dome
    T = Batch("ga_tomb")
    ty, R, Hb = 28, 13.5, 14.0
    T.prism(BRICK_T, ngon(R, 8), 0, Hb, 0, ty)
    T.prism(BRICK_LT, ngon(R * 1.03, 8), Hb, 0.6, 0, ty)
    apo = R * math.cos(math.pi / 8)
    side = 2 * R * math.sin(math.pi / 8)
    for k in range(8):
        a = math.tau * k / 8
        O = (apo * math.cos(a), ty + apo * math.sin(a), 0)
        T.rect(BRICK_LT, O, a, -side * 0.44, side * 0.44, 0.5, Hb - 0.8, 0.1)
        lozenge_field(T, O, a, -side * 0.42, side * 0.42, Hb * 0.62, Hb - 1.2, 1.15, (TURQ, COBALT), 0.1)
        T.panel(TURQ, arch_outline(side * 0.62, Hb * 0.56), (O[0], O[1], 0.6), a, 0.2, 0.1)
        T.panel(DEEP, arch_outline(side * 0.5, Hb * 0.5), (O[0], O[1], 0.7), a, 0.26, 0.1)
        kufic_band(T, O, a, -side * 0.5, side * 0.5, Hb - 1.1, Hb - 0.1, COBALT, TWHITE, 0.0, 0.8)
    # gallery added by Ulugh Beg round the back
    T.box(BRICK_T, 0, ty + R + 3, 0, 22, 6, 7)
    niche_row_at(T, 0, ty + R + 6, 0.4, NORTH, -10, 10, 6, 4, 1, BRICK_LT, DEEP, None)
    zd = Hb + 0.6
    T.lathe(BRICK_LT, [(9.2, 0), (9.2, 1.2)], 0, ty, zd, 64)
    kufic_ring(T, 0, ty, zd + 1.2, 8.0, 9.0, 18, COBALT, TWHITE, 64)
    T.lathe(TURQ, [(9.3, 9.2), (9.6, 9.8)], 0, ty, zd, 64)
    melon_dome(T, 9.2, 0, ty, zd + 9.8, ribs=64, height=1.42, color=DOME, amp=0.055, bulb=1.13, rings=16)
    m.add(2, T.build(), "tomb")
    m.add(2, put(portal("ga_tomb_p", 9, 15, 2.0, guldasta=False), 0, ty - apo - 1.6), "tomb")
    for s in (-1, 1):
        m.add(3, t_minaret(f"ga_min{s}", 2.0, 27, s * 20.5, 7, 0, BRICK_T, (TURQ, COBALT), "lantern"), "minarets")
    return m


# ---------------------------------------------------------------- Shah-i-Zinda

def _slope_solid(B, color, x0, x1, ys, zf, base=0.0, lift=0.0):
    """A ground solid between x0 and x1 whose top follows zf(y) through the sample ys."""
    V, F = [], []
    for y in ys:
        zt = zf(y) + lift
        V += [(x0, y, base), (x1, y, base), (x1, y, zt), (x0, y, zt)]
    n = len(ys)
    for i in range(n - 1):
        a, b = 4 * i, 4 * (i + 1)
        for k in range(4):
            F.append((a + k, a + (k + 1) % 4, b + (k + 1) % 4, b + k))
    F.append((3, 2, 1, 0))
    F.append((4 * (n - 1), 4 * (n - 1) + 1, 4 * (n - 1) + 2, 4 * (n - 1) + 3))
    B.add(color, V, F)


def _zinda_tomb(B, objs, name, x, y, z, s, face, dome="ribbed", dome_color=DOME, drum_h=None, tile=(TURQ, COBALT), oct_drum=False, body=BRICK_T):
    """A mausoleum of the street: a square chamber, a tiled pishtaq toward the lane, a drum and a dome."""
    B.box(body, x, y, z - 1.0, s, s, s * 0.95 + 1.0)
    B.box(BRICK_LT, x, y, z + s * 0.95, s + 0.3, s + 0.3, 0.35)
    ang = EAST if face == "E" else WEST
    for a2, (dx, dy) in ((SOUTH, (0, -s / 2)), (NORTH, (0, s / 2))):
        B.panel(BRICK_DK, arch_outline(s * 0.4, s * 0.6), (x + dx, y + dy, z + 0.6), a2, 0.12)
    zt = z + s * 0.95 + 0.35
    r = s * 0.36
    dh = drum_h if drum_h is not None else s * 0.3
    if oct_drum:
        B.prism(body, ngon(r * 1.12, 8), zt, dh, x, y)
    if dome == "ribbed":
        drum_dome(B, r, x, y, zt, dh, 16, dome_color, 1.45, kufic=dh > 1.0, n_letters=12)
    elif dome == "conical":
        B.lathe(body, [(r, 0), (r, dh)], x, y, zt, 24)
        B.lathe(dome_color, [(r * 1.04, 0), (r * 0.5, r * 0.9), (0.0, r * 1.5)], x, y, zt + dh, 24)
    else:
        B.lathe(body, [(r, 0), (r, dh)], x, y, zt, 24)
        smooth_dome(B, r, x, y, zt + dh, dome_color, 1.05, rings=7)
    p = portal(name, s * 0.92, s * 1.3, 1.4, body, TURQ, COBALT, DEEP, guldasta=True, pattern=tile, muqarnas=s > 8.5, crest=False)
    objs.append(put(p, x + (s / 2 + 1.3) * (1 if face == "E" else -1), y, z - 0.4, FACING[face]))


def shah_i_zinda(era="1440"):
    m = Model("shah-i-zinda" + ("-1404" if era == "1404" else ""))
    zf = lambda y: 0.0 if y < -96 else (3.5 + (y + 70) / 200 * 9.0 if y > -70 else 3.5 * (y + 96) / 26)
    ys = [-130, -96, -88, -80, -70, -40, 0, 40, 80, 130]
    G = Batch("sz_ground")
    _slope_solid(G, GROUND, -35, 35, ys, zf, 0.0, 0.3)
    _slope_solid(G, PAVE, -3.2, 3.2, [-128, -96, -92, -70, -40, 0, 40, 80, 112], zf, 0.0, 0.45)
    for i in range(18):
        y = -96 + i * 26 / 18
        G.box(PAVE_DK, 0, y + 0.7, 0, 6.6, 1.45, zf(y + 1.4) + 0.5)
    for x, y in ((-26, -116), (26, -112), (-25, -80), (24, -84), (-28, 20), (28, 70), (-27, 100)):
        tree_b(G, x, y, zf(y) + 0.3, 2.2, "poplar" if (x > 0) else "round")
    m.add(0, G.build(), "slope")
    objs = []
    T = Batch("sz_tombs")
    tombs = [("W", -64, 9.0, "ribbed", DOME), ("E", -60, 10.0, "ribbed", DOME), ("W", -46, 8.5, "smooth", TURQ), ("E", -42, 9.0, "ribbed", TURQ),
             ("W", -29, 8.0, "ribbed", DOME), ("E", -24, 8.0, "smooth", DOME), ("W", -11, 8.5, "ribbed", TURQ), ("E", -2, 9.5, "conical", TURQ),
             ("W", 8, 9.0, "smooth", BRICK_LT), ("E", 18, 8.5, "ribbed", DOME), ("W", 28, 10.0, "ribbed", DOME), ("E", 40, 9.0, "smooth", TURQ),
             ("W", 50, 9.5, "ribbed", DOME), ("E", 60, 8.5, "ribbed", DOME)]
    for i, (side, y, s, kind, col) in enumerate(tombs):
        x = (3.6 + s / 2) * (-1 if side == "W" else 1)
        tile = [(TURQ, COBALT), (TURQ, TWHITE), (COBALT, TURQ), (TURQ, TGREEN)][i % 4]
        _zinda_tomb(T, objs, f"sz_t{i}", x, y, zf(y), s, "E" if side == "W" else "W", kind, col, s * (0.45 if i % 3 == 0 else 0.25), tile)
    # Qutham ibn Abbas: the shrine complex at the top, a mosque portal across the lane, domed rooms and a small minaret
    zt = zf(90)
    T.box(BRICK_T, 0, 98, zt - 1, 40, 30, 10)
    T.box(BRICK_LT, 0, 98, zt + 9, 40.3, 30.3, 0.4)
    for x, y, r in ((-10, 100, 5.0), (8, 104, 6.0), (-2, 90, 4.0)):
        drum_dome(T, r, x, y, zt + 9.4, 2.5 if r > 4.5 else 1.0, 16 if r < 6 else 24, DOME if r != 4.0 else TURQ, 1.45, kufic=r >= 5.0)
    T.box(BRICK_T, -16, 112, zt - 1, 8, 8, 4)
    m.add(1, T.build(), "tombs")
    objs.append(put(portal("sz_qutham_p", 16, 18, 3, spandrel=TWHITE), 0, 81, zt - 0.6))
    objs.append(t_minaret("sz_qmin", 1.3, 13, 16, 108, zt + 9, BRICK_T, (TURQ, COBALT), "lantern"))
    for o in objs:
        m.add(1, o, "tombs")
    if era != "1404":
        # Ulugh Beg's lower gateway (1434-35) and the double-domed tomb at the foot of the street
        L = Batch("sz_lower")
        for s in (-1, 1):
            L.box(BRICK_T, s * 14, -121, 0, 14, 8, 6)
        L.box(BRICK_T, -17, -104, 0, 18, 26, 9)
        L.box(BRICK_LT, -17, -104, 9, 18.3, 26.3, 0.4)
        niche_row_at(L, -8, -104, 0.4, EAST, -12, 12, 8, 3, 1, TURQ, DEEP, COBALT)
        drum_dome(L, 6.0, -17, -110, 9.4, 4.5, 24, DOME, 1.4, n_letters=16)
        drum_dome(L, 4.0, -17, -97, 9.4, 2.0, 16, TURQ, 1.35, kufic=False)
        m.add(2, L.build(), "lower gateway")
        m.add(2, put(portal("sz_darvaza", 14, 16, 6, spandrel=TWHITE), 0, -126), "lower gateway")
    return m


# ---------------------------------------------------------------- the observatory

def observatory(ruin=False):
    m = Model("observatory" + ("-ruin" if ruin else ""))
    G = Batch("obs_hill")
    G.frustum(GROUND, 0, 0, 0, 66, 66, 56, 56, 1.4)
    G.box(PAVE, 0, 0, 1.4, 54, 54, 0.15)
    if not ruin:
        for i in range(10):
            a = math.tau * (i + 0.5) / 10
            tree_b(G, 26 * math.cos(a), 26 * math.sin(a), 1.4, 1.8, "poplar" if i % 2 else "round")
    m.add(0, G.build(), "hill")
    R, z0 = 23.0, 1.4
    B = Batch("obs_body")
    if ruin:
        B.lathe(BRICK_T, [(R, 0), (R, 2.4), (R - 3, 2.4), (R - 3, 0)], 0, 0, z0, 48, cap_top=False, cap_bottom=False)
        for i in range(26):
            a = math.tau * i / 26
            B.box(BRICK_T, (R - 1.5) * math.cos(a), (R - 1.5) * math.sin(a), z0 + 2.4, 3, 2.6, 0.6 + (i * 5 % 7) * 0.35, a + math.pi / 2)
        for x, y, s in ((-12, 8, 9), (10, -10, 8), (12, 12, 6)):
            B.frustum(RUBBLE, x, y, z0, s, s * 1.2, s * 0.3, s * 0.4, 1.8)
        # the arc's trench, still with the lower part of the marble rails
        B.box(DARK, 0, -2, z0, 6.0, 44, 0.2)
        for s in (-1, 1):
            for k in range(12):
                y = -22 + k * 3.6
                B.box(TWHITE, s * 2.0, y, z0, 0.5, 3.4, 0.3 + 0.1 * k)
        m.add(1, B.build(), "ruins")
        return m
    storeys = [(0.0, 11.0, R), (11.0, 9.5, R - 1.2), (20.5, 8.5, R - 2.4)]
    for k, (zb, h, rr) in enumerate(storeys):
        B.lathe(BRICK_T, [(rr, 0), (rr, h)], 0, 0, z0 + zb, 48)
        n = 40
        if k:
            B.lathe(TURQ, [(rr + 1.2, -0.4), (rr + 1.2, 0.0)], 0, 0, z0 + zb, 48)
        for i in range(n):
            a = math.tau * (i + 0.5) / n
            O = (rr * math.cos(a), rr * math.sin(a), z0 + zb + 0.6)
            B.panel(TURQ if k != 1 else COBALT, arch_outline(rr * math.tau / n * 0.7, h * 0.78), O, a, 0.16)
            B.panel(DEEP if k != 0 else DARK, arch_outline(rr * math.tau / n * 0.52, h * 0.7), O, a, 0.24)
        kufic_ring(B, 0, 0, z0 + zb + h - 1.2, 1.2, rr, 60, COBALT, TWHITE, 48)
        ring_pattern(B, 0, 0, z0 + zb + h * 0.8, z0 + zb + h - 1.3, rr, rr, 64, 2, (TURQ, TWHITE), 0.8)
    top = z0 + 29.0
    B.lathe(BRICK_LT, [(R - 2.4, 0), (R - 2.1, 0.8)], 0, 0, top, 48)
    for i in range(40):
        a = math.tau * i / 40
        B.box(BRICK_LT, (R - 2.6) * math.cos(a), (R - 2.6) * math.sin(a), top + 0.8, 1.2, 0.6, 0.9, a + math.pi / 2)
    m.add(1, B.build(), "building")
    # the Fakhri sextant: a marble-railed arc along the meridian, cut down into the hill and rising out of the roof to the north
    A = Batch("obs_arc")
    A.box(DARK, 0, -2, top + 0.8, 4.6, 40, 0.15)
    for k in range(20):
        y0, y1 = -22 + k * 2.1, -22 + (k + 1) * 2.1
        t = (k + 0.5) / 20
        hh = 0.6 + 6.5 * t ** 2.2
        for s_ in (-1, 1):
            A.box(TWHITE, s_ * 2.8, (y0 + y1) / 2, top + 0.8, 1.0, 2.15, hh + 0.5)
            A.box(BRICK_LT, s_ * 4.0, (y0 + y1) / 2, top + 0.8, 1.4, 2.15, hh)
        A.box(BRICK_DK, 0, (y0 + y1) / 2, top + 0.8, 4.6, 2.15, max(0.2, hh - 1.2))
        A.box(GILT if k % 3 == 0 else TWHITE, 0, y0 + 0.1, top + 0.8 + max(0.2, hh - 1.2), 4.6, 0.25, 0.2)
    A.box(BRICK_LT, 0, 19.5, top + 0.8, 11, 4, 8.5)
    A.panel(DARK, arch_outline(3.2, 5.0), (0, 17.5, top + 0.8 + 2.0), SOUTH, 0.1)
    A.panel(TURQ, [(-5.5, 7.0), (5.5, 7.0), (5.5, 8.2), (-5.5, 8.2)], (0, 17.5, top + 0.8), SOUTH, 0.12)
    m.add(2, A.build(), "meridian arc")
    m.add(2, put(portal("obs_portal", 12, 14, 3, guldasta=False), 0, -R - 1.5, z0), "meridian arc")
    return m


# ---------------------------------------------------------------- Afrasiyab

def afrasiyab_citadel(ruin=False):
    m = Model("afrasiyab-citadel" + ("-ruin" if ruin else ""))
    G = Batch("afc_mound")
    G.box(GROUND, 0, 0, 0, 202, 162, 0.3)
    if ruin:
        G.frustum(PAKHSA_DK, 0, 0, 0.3, 186, 146, 150, 112, 5.0)
        G.frustum(PAKHSA_DK, 0, 34, 5.3, 56, 44, 26, 20, 9.0)
        G.frustum(PAKHSA, -40, -14, 5.3, 44, 30, 26, 16, 2.5)
        G.frustum(PAKHSA, 42, -6, 5.3, 34, 28, 18, 14, 2.0)
        for i in range(30):
            a = math.tau * i / 30
            x, y = 84 * math.cos(a), 64 * math.sin(a)
            G.frustum(PAKHSA, x, y, 5.3, 10, 8, 3, 2, 1.0 + (i * 7 % 5) * 0.8)
        for i in range(12):
            G.box(TWHITE if i % 3 else BRICK_LT, -60 + (i % 6) * 6, -50 + (i // 6) * 5, 5.3, 1.0, 2.2, 0.5)
        m.add(0, G.build(), "ruin mound")
        return m
    G.frustum(PAKHSA_DK, 0, 0, 0.3, 196, 156, 182, 142, 6.0)
    m.add(0, G.build(), "platform")
    B = Batch("afc_walls")
    pts = [(-88, -68), (88, -68), (92, 30), (60, 70), (-60, 70), (-92, 30)]
    wall_ring(B, pts, 9, 4.5, PAKHSA, towers=4.5, tower_h=12, every=26, z=6.3, square=True)
    B.box(PAVE, 0, 0, 6.3, 160, 120, 0.15)
    for i in range(6):
        B.panel(DARK, [(-0.3, 0), (0.3, 0), (0.3, 2.2), (-0.3, 2.2)], (-75 + i * 30, -68 - 2.3, 10), SOUTH, 0.1)
    m.add(1, B.build(), "walls")
    K = Batch("afc_keep")
    K.frustum(PAKHSA, 0, 36, 6.3, 50, 40, 44, 34, 16)
    for ang, O, L in ((SOUTH, (0, 16, 6.3), 46), (EAST, (25, 36, 6.3), 36), (WEST, (-25, 36, 6.3), 36)):
        for i in range(6):
            u = -L / 2 + (i + 0.5) * L / 6
            K.panel(DARK, [(u - 0.4, 0), (u + 0.4, 0), (u + 0.4, 3.0), (u - 0.4, 3.0)], (O[0], O[1], O[2] + 9), ang, 0.1, 1.2)
    for i in range(10):
        K.box(PAKHSA_LT, -20 + i * 4.4, 19.4, 22.3, 1.6, 1.2, 1.4)
    K.box(PAKHSA_LT, 0, 40, 22.3, 22, 16, 4)
    m.add(2, K.build(), "keep")
    P = Batch("afc_palace")
    # the ikhshid's halls: a columned portico before a square hall with a lantern, and a second hall with its court
    P.box(PAKHSA_LT, -40, -10, 6.3, 50, 32, 8)
    P.box(shade(PAKHSA_LT, -0.1), -40, -10, 14.3, 50.4, 32.4, 0.5)
    P.box(PAKHSA_LT, -40, -6, 14.8, 12, 12, 3)
    for i in range(8):
        P.lathe(WOOD, [(0.45, 0), (0.4, 6.0), (0.75, 6.4), (0.75, 6.8)], -61 + i * 6, -30, 6.3, 8)
    P.box(WOOD_DK, -40, -30, 13.1, 50, 3, 0.8)
    P.box(PAKHSA, -40, -28.5, 13.9, 50, 6, 0.5)
    P.rect("#9A3F33", (-40, -26, 6.3), SOUTH, -20, 20, 1.5, 6, 0.08)
    P.rect("#3E5C9A", (-40, -26, 6.3), SOUTH, -14, 14, 2.5, 5, 0.08, 0.08)
    P.box(PAKHSA_LT, 42, -6, 6.3, 36, 30, 7)
    P.box(PAKHSA_LT, 42, -6, 13.3, 10, 10, 2.5)
    for i in range(5):
        P.box(MUD, -10 + i * 9, -48, 6.3, 7, 10, 4)
    gx = 0
    P.box(PAKHSA, gx, -68, 6.3, 20, 10, 12)
    for s in (-1, 1):
        P.box(shade(PAKHSA, -0.05), gx + s * 10, -68, 6.3, 7, 12, 15)
    P.panel(DARK, arch_outline(6, 8, 0.6), (gx, -73.1, 6.3), SOUTH, 0.2)
    m.add(2, P.build(), "palace")
    return m


def ambassadors_hall():
    m = Model("ambassadors-hall")
    B = Batch("amb")
    B.box(GROUND, 0, 0, 0, 40, 40, 0.3)
    wall_ring(B, [(-19, -19), (19, -19), (19, 19), (-19, 19)], 4.5, 1.2, PAKHSA, merlons=False, z=0.3)
    B.box(PAVE, 0, -8, 0.3, 30, 12, 0.12)
    B.panel(DOOR, [(-1.5, 0), (1.5, 0), (1.5, 3), (-1.5, 3)], (0, -19.6, 0.3), SOUTH, 0.15)
    m.add(0, B.build(), "walls")
    H = Batch("amb_hall")
    # the painted hall: about 11 m square inside, flat roof on four columns, a lantern
    H.box(PAKHSA_LT, 0, 7, 0.3, 15, 15, 8)
    H.box(shade(PAKHSA_LT, -0.12), 0, 7, 8.3, 15.4, 15.4, 0.5)
    H.box(PAKHSA_LT, 0, 7, 8.8, 5, 5, 1.8)
    for s in (-1, 1):
        H.panel(DARK, [(-1.2, 0.3), (1.2, 0.3), (1.2, 1.4), (-1.2, 1.4)], (s * 2.5, 7, 8.8), EAST if s > 0 else WEST, 0.08)
    # porch (ayvan) of carved wooden columns before the hall, with the paintings glimpsed inside
    for i in range(4):
        H.lathe(WOOD, [(0.32, 0), (0.28, 5.0), (0.55, 5.4), (0.55, 5.8)], -6 + i * 4, -3.6, 0.3, 8)
    H.box(WOOD_DK, 0, -3.6, 6.1, 15, 0.8, 0.6)
    H.box(PAKHSA, 0, -2, 6.7, 15.4, 4.2, 0.45)
    H.rect("#B04A3A", (0, -0.5, 0.3), SOUTH, -6.8, 6.8, 0.5, 5.8, 0.06)
    H.rect("#3E5C9A", (0, -0.5, 0.3), SOUTH, -6.2, 6.2, 1.2, 4.6, 0.06, 0.06)
    for i in range(7):
        H.rect(["#E8D6A8", "#C9A24A", "#7A9A6A", "#E8D6A8"][i % 4], (0, -0.5, 0.3), SOUTH, -5.6 + i * 1.6, -4.9 + i * 1.6, 1.6, 3.6 - (i % 2) * 0.6, 0.05, 0.12)
    H.panel(DOOR, [(-1.0, 0), (1.0, 0), (1.0, 2.8), (-1.0, 2.8)], (0, -0.5, 0.3), SOUTH, 0.1, 0.12)
    # side wings of two storeys
    for s in (-1, 1):
        H.box(PAKHSA, s * 13.5, 2, 0.3, 9, 30, 7)
        H.box(shade(PAKHSA, -0.12), s * 13.5, 2, 7.3, 9.3, 30.3, 0.4)
        for i in range(4):
            H.panel(DARK, [(-0.5, 0), (0.5, 0), (0.5, 1.4), (-0.5, 1.4)], (s * 9.0, -9 + i * 6, 4.0), WEST if s > 0 else EAST, 0.08)
    H.box(PAKHSA, 0, 17, 0.3, 18, 4, 6)
    H.box(WOOD_DK, -6, -10, 0.3, 2.0, 1.2, 0.8)
    tree_b(H, 6, -12, 0.3, 1.6)
    m.add(1, H.build(), "hall")
    return m


def sogdian_temple():
    m = Model("sogdian-temple")
    B = Batch("tmp_walls")
    B.box(GROUND, 0, 0, 0, 92, 92, 0.3)
    B.box(PAVE, 0, 0, 0.3, 80, 80, 0.12)
    wall_ring(B, [(-43, -43), (43, -43), (43, 43), (-43, 43)], 7, 3, PAKHSA, towers=3.2, tower_h=9, every=22, z=0.3, square=True)
    for s in (-1, 1):
        B.box(shade(PAKHSA, -0.06), s * 8, -44, 0.3, 8, 9, 12)
    B.box(PAKHSA, 0, -44, 0.3, 10, 6, 9)
    B.panel(DARK, arch_outline(4.2, 6.5, 0.6), (0, -47.1, 0.3), SOUTH, 0.2)
    m.add(0, B.build(), "walls")
    T = Batch("tmp_sanct")
    # raised sanctuary with a portico of wooden columns, a fire chamber and an altar in the court
    T.frustum(PAKHSA_DK, 0, 16, 0.3, 40, 32, 36, 28, 2.2)
    T.box(PAKHSA_LT, 0, 22, 2.5, 28, 18, 9)
    T.frustum(shade(PAKHSA_LT, -0.08), 0, 22, 11.5, 29, 19, 18, 9, 3)
    T.box(PAKHSA_LT, 0, 22, 14.5, 8, 6, 2.5)
    for i in range(6):
        T.lathe(WOOD, [(0.45, 0), (0.4, 6.5), (0.8, 6.9), (0.8, 7.3)], -12.5 + i * 5, 9.5, 2.5, 8)
    T.box(WOOD_DK, 0, 9.5, 9.8, 30, 1.2, 0.8)
    T.box(PAKHSA, 0, 11, 10.6, 30, 4.2, 0.6)
    T.rect("#9A3F33", (0, 13, 2.5), SOUTH, -10, 10, 0.5, 7, 0.08)
    T.panel(DOOR, arch_outline(3, 5, 0.6), (0, 12.9, 2.5), SOUTH, 0.1, 0.08)
    for i in range(5):
        T.box(PAKHSA_DK, 0, 0.0 - i * 0.7 + 0.2, 0.3, 10, 0.7 + i * 0.0, 2.2 - i * 0.44)
    T.frustum(PAKHSA_LT, 0, -16, 0.3, 4, 4, 2.6, 2.6, 1.6)
    T.box(PAKHSA_LT, 0, -16, 1.9, 2.0, 2.0, 0.8)
    T.lathe("#E07A2A", [(0.7, 0), (0.4, 0.9), (0.0, 1.8)], 0, -16, 2.7, 7)
    for s in (-1, 1):
        T.box(MUD, s * 32, 0, 0.3, 12, 60, 5)
        T.box(shade(MUD, -0.1), s * 32, 0, 5.3, 12.3, 60.3, 0.4)
    m.add(1, T.build(), "sanctuary")
    return m


def afrasiyab_mosque():
    """Qibla to the west: a hypostyle hall of wooden columns along the west side, arcades round the court, a brick minaret."""
    m = Model("afrasiyab-mosque")
    B = Batch("afm_walls")
    B.box(GROUND, 0, 0, 0, 92, 92, 0.3)
    B.box(PAVE, 10, 0, 0.3, 54, 70, 0.12)
    wall_ring(B, [(-44, -44), (44, -44), (44, 44), (-44, 44)], 7, 2.5, BRICK_T, towers=2.6, tower_h=8, merlons=False, z=0.3)
    for (cx, cy, w, d) in ((12, -38, 60, 10), (12, 38, 60, 10), (39, 0, 10, 66)):
        B.box(BRICK_LT, cx, cy, 0.3, w, d, 6)
        B.box(shade(BRICK_LT, -0.1), cx, cy, 6.3, w + 0.3, d + 0.3, 0.4)
    niche_row_at(B, 12, -33, 0.3, NORTH, -30, 30, 5, 10, 1, BRICK_DK, DARK, None)
    niche_row_at(B, 12, 33, 0.3, SOUTH, -30, 30, 5, 10, 1, BRICK_DK, DARK, None)
    niche_row_at(B, 34, 0, 0.3, WEST, -28, 28, 5, 9, 1, BRICK_DK, DARK, None)
    B.box(WATER_C, 10, 0, 0.3, 4, 4, 0.5)
    m.add(0, B.build(), "walls")
    H = Batch("afm_hall")
    H.box(BRICK_T, -41, 0, 0.3, 4, 84, 8)
    H.box(BRICK_DK, -42, 0, 0.3, 3, 6, 9)
    for i in range(4):
        for j in range(12):
            H.lathe(WOOD, [(0.4, 0), (0.35, 6.6), (0.7, 7.0), (0.7, 7.4)], -36 + i * 5.5, -38 + j * 6.9, 0.3, 8)
    H.box(MUD, -24, 0, 7.7, 38, 86, 0.8)
    H.box(shade(MUD, -0.1), -24, 0, 8.5, 38.4, 86.4, 0.35)
    for j in range(6):
        H.box(MUD, -24, -35 + j * 14, 8.8, 4, 4, 1.4)
    H.lathe(BRICK_T, [(3.2, 0), (2.4, 30)], -12, -40, 0.3, 16)
    for k in range(6):
        H.lathe(BRICK_DK if k % 2 else BRICK_LT, [(3.2 - 0.8 * (k * 5 + 4) / 30 + 0.05, k * 5 + 3), (3.2 - 0.8 * (k * 5 + 5) / 30 + 0.05, k * 5 + 4.2)], -12, -40, 0.3, 16, cap_top=False, cap_bottom=False)
    H.lathe(BRICK_LT, [(2.4, 0), (3.0, 1.2), (3.0, 2.0), (1.6, 2.0), (1.6, 4.0), (0.0, 5.2)], -12, -40, 30.3, 16)
    m.add(1, H.build(), "hall and minaret")
    return m


# ---------------------------------------------------------------- the Ark and the city's smaller buildings

def kok_saray():
    m = Model("kok-saray")
    B = Batch("ark_walls")
    B.box(GROUND, 0, 0, 0, 242, 242, 0.3)
    B.box(PAVE, 0, 0, 0.3, 220, 220, 0.1)
    wall_ring(B, [(-114, -114), (114, -114), (114, 114), (-114, 114)], 12, 6, BRICK_DK, towers=5.5, tower_h=15, every=38, z=0.3)
    m.add(0, B.build(), "walls")
    m.add(0, put(portal("ark_gate", 20, 20, 12, spandrel=TWHITE), 117, 0, 0, FACING["E"]), "walls")
    K = Batch("kok_saray")
    # the Blue Palace: four storeys of tiled loggias round a block, with corner towers
    kx, ky, kw, kd, kh = -25, 25, 56, 38, 25
    K.box(BRICK_T, kx, ky, 0.3, kw, kd, kh)
    K.box(BRICK_LT, kx, ky, kh + 0.3, kw + 0.4, kd + 0.4, 0.6)
    for ang, cx, cy, L in ((SOUTH, kx, ky - kd / 2, kw), (EAST, kx + kw / 2, ky, kd), (WEST, kx - kw / 2, ky, kd), (NORTH, kx, ky + kd / 2, kw)):
        segs = [(-L / 2 + 3, -12), (12, L / 2 - 3)] if ang == SOUTH else [(-L / 2 + 3, L / 2 - 3)]
        for u0, u1 in segs:
            niche_row_at(K, cx, cy, 0.8, ang, u0, u1, kh - 3, max(2, int((u1 - u0) / 5)), 4, TURQ, DEEP, COBALT, 0.0, TWHITE)
        kufic_band(K, (cx, cy, 0.3), ang, -L / 2 + 0.5, L / 2 - 0.5, kh - 1.8, kh - 0.2, COBALT, TWHITE)
    for sx in (-1, 1):
        for sy in (-1, 1):
            x, y = kx + sx * kw / 2, ky + sy * kd / 2
            K.lathe(BRICK_T, [(3.2, 0), (3.0, kh + 4)], x, y, 0.3, 16)
            ring_pattern(K, x, y, 3, kh + 3, 3.2, 3.0, 12, 8, (TURQ, COBALT))
            drum_dome(K, 3.0, x, y, kh + 4.3, 1.0, 12, DOME, 1.3, kufic=False)
    drum_dome(K, 9, kx, ky + 4, kh + 0.9, 4.0, 32, DOME, 1.4)
    m.add(1, K.build(), "kok saray")
    m.add(1, put(portal("kok_p", 22, 31, 4, spandrel=TWHITE), kx, ky - kd / 2 - 2.5), "kok saray")
    O = Batch("ark_court")
    # Bustan Saray with its ayvan, a mosque, workshops and barracks along the walls, gardens
    O.box(BRICK_LT, 50, 55, 0.3, 40, 26, 9)
    for i in range(8):
        O.lathe(WOOD, [(0.4, 0), (0.35, 6.0), (0.7, 6.4)], 33 + i * 5, 39, 0.3, 8)
    O.box(WOOD_DK, 50, 41, 6.7, 40, 6, 0.6)
    O.rect(TGREEN, (50, 42, 0.3), SOUTH, -18, 18, 1.0, 5.6, 0.06)
    O.box(BRICK_T, 60, -45, 0.3, 22, 22, 10)
    drum_dome(O, 7, 60, -45, 10.3, 2.5, 24, DOME, 1.35, kufic=False)
    O.panel(DEEP, arch_outline(6, 8), (60, -56.1, 0.3), SOUTH, 0.2)
    for i in range(7):
        O.box(MUD, -90 + i * 28, -100, 0.3, 24, 12, 5)
        O.box(shade(MUD, -0.12), -90 + i * 28, -100, 5.3, 24.3, 12.3, 0.4)
    for i in range(5):
        O.box(MUD, -100, -60 + i * 28, 0.3, 12, 24, 5)
    for i in range(14):
        tree_b(O, 20 + (i % 7) * 12, 80 + (i // 7) * 14, 0.3, 2.6)
    for i in range(6):
        tree_b(O, -70 + i * 14, -40, 0.3, 2.4, "poplar")
    O.box(WATER_C, 50, 75, 0.3, 14, 6, 0.5)
    m.add(2, O.build(), "court buildings")
    return m


def rukhabad():
    m = Model("rukhabad")
    B = Batch("rukh")
    B.box(GROUND, 0, 0, 0, 26, 26, 0.3)
    B.box(BRICK_DK, 0, 0, 0.3, 19, 19, 0.6)
    B.box(BRICK_T, 0, 1, 0.9, 16, 16, 9)
    for ang, O in ((EAST, (8, 1, 0.9)), (WEST, (-8, 1, 0.9)), (NORTH, (0, 9, 0.9))):
        B.panel(BRICK_DK, arch_outline(6, 7), O, ang, 0.2)
        B.panel(DARK, arch_outline(1.6, 2.6), O, ang, 0.1, 0.2)
    B.prism(BRICK_T, ngon(7.6, 8), 9.9, 2.4, 0, 1)
    for k in range(8):
        a = math.tau * k / 8
        B.panel(DARK, arch_outline(1.0, 1.4), (7.6 * math.cos(math.pi / 8) * math.cos(a), 1 + 7.6 * math.cos(math.pi / 8) * math.sin(a), 10.3), a, 0.06)
    B.lathe(BRICK_LT, [(7.0, 0), (7.0, 0.8)], 0, 1, 12.3, 32)
    smooth_dome(B, 6.8, 0, 1, 13.1, BRICK_LT, 0.95, finial=BRONZE, rings=9)
    m.add(0, B.build(), "body")
    m.add(1, put(portal("rukh_p", 10, 13, 2.5, BRICK_T, BRICK_DK, BRICK_LT, DARK, guldasta=False, pattern=(BRICK_DK, BRICK_LT), muqarnas=False), 0, -8.4, 0.9), "portal")
    return m


def ak_saray():
    m = Model("ak-saray")
    B = Batch("aks")
    B.box(GROUND, 0, 0, 0, 26, 26, 0.3)
    B.box(BRICK_T, 0, 0, 0.3, 17, 17, 10)
    for ang, (dx, dy) in ((SOUTH, (0, -1)), (NORTH, (0, 1)), (EAST, (1, 0)), (WEST, (-1, 0))):
        B.box(BRICK_T, dx * 9.5, dy * 9.5, 0.3, 8 if dx == 0 else 2.2, 2.2 if dx == 0 else 8, 11)
        B.panel(DEEP if ang == SOUTH else BRICK_DK, arch_outline(5.0, 8.5), (dx * 10.6, dy * 10.6, 0.3), ang, 0.2)
        B.panel(DARK, arch_outline(1.8, 3.0), (dx * 10.6, dy * 10.6, 0.3), ang, 0.1, 0.2)
        if ang == SOUTH:
            B.rect(TURQ, (0, -10.6, 0.3), SOUTH, -3.9, -3.1, 0.4, 9.0, 0.1)
            B.rect(TURQ, (0, -10.6, 0.3), SOUTH, 3.1, 3.9, 0.4, 9.0, 0.1)
            kufic_band(B, (0, -10.6, 0.3), SOUTH, -3.8, 3.8, 9.2, 10.4, COBALT, TWHITE, 0.0, 0.6)
    B.prism(BRICK_T, ngon(7.0, 8), 10.3, 1.6, 0, 0)
    smooth_dome(B, 6.6, 0, 0, 11.9, BRICK_LT, 0.6, finial=None, rings=6)
    for i in range(6):
        B.box(RUBBLE, -6 + i * 2.5, 9, 0.3, 1.6, 1.4, 0.5 + (i % 3) * 0.3)
    m.add(0, B.build(), "body")
    return m


def hazrat_khizr():
    m = Model("hazrat-khizr")
    B = Batch("khizr")
    B.frustum(GROUND, 0, 0, 0, 40, 36, 34, 30, 2.5)
    B.box(PAVE, 0, 0, 2.5, 33, 29, 0.1)
    for i in range(6):
        B.box(PAVE_DK, -10, -16.2 - 0.0 + i * 0.5, 0, 6, 3.0 - i * 0.5, 0.42 * (i + 1))
    B.box(BRICK_LT, -4, 5, 2.5, 13, 13, 7.5)
    B.prism(BRICK_LT, ngon(5.8, 8), 10.0, 1.4, -4, 5)
    smooth_dome(B, 5.0, -4, 5, 11.4, BRICK_LT, 1.1, finial=BRONZE, rings=8)
    for ang, O in ((EAST, (2.5, 5, 2.5)), (SOUTH, (-4, -1.5, 2.5))):
        B.panel(DOOR, arch_outline(2.2, 3.4), O, ang, 0.1)
    # ayvan: a flat roof on carved wooden columns along the south and east, its ceiling painted
    for i in range(6):
        B.lathe(WOOD, [(0.28, 0), (0.24, 5.0), (0.5, 5.3), (0.5, 5.6)], -12 + i * 4.4, -6.5, 2.5, 8)
    for j in range(4):
        B.lathe(WOOD, [(0.28, 0), (0.24, 5.0), (0.5, 5.3), (0.5, 5.6)], 10, -6.5 + j * 4.5, 2.5, 8)
    B.box(WOOD_DK, -1, -4.5, 8.1, 25, 5.2, 0.45)
    B.box(WOOD_DK, 8, 2.5, 8.1, 5.2, 19, 0.45)
    B.box(TGREEN, -1, -4.5, 7.95, 24, 4.8, 0.15)
    m.add(0, B.build(), "mosque")
    m.add(1, t_minaret("khizr_min", 1.1, 11, 14, 12, 2.5, BRICK_LT, (BRICK_DK, TURQ), "lantern"), "minaret")
    return m


def siab_bazaar():
    m = Model("siab-bazaar")
    B = Batch("siab")
    B.box(GROUND, 0, 0, 0, 72, 52, 0.3)
    B.box(PAVE_DK, 0, 0, 0.3, 66, 46, 0.1)
    wall_ring(B, [(-34, -24), (34, -24), (34, 24), (-34, 24)], 3.2, 1.0, MUD, merlons=False, z=0.3)
    B.box(BRICK_LT, 0, -24, 0.3, 8, 3, 6)
    B.panel(DOOR, arch_outline(3.2, 4.4), (0, -25.6, 0.3), SOUTH, 0.12)
    stalls(B, -27, -16, 11, 2, 5.4, 8, 0.4, 0)
    stalls(B, -27, 4, 4, 2, 5.4, 8, 0.4, 3)
    stalls(B, 11, 4, 4, 2, 5.4, 8, 0.4, 1)
    tim_dome(B, 0, 13, 0.4, 5.5, 6, BRICK_LT, arms=False)
    B.box(WATER_C, 0, -4, 0.4, 6, 4, 0.4)
    for x in (-5, 5):
        tree_b(B, x, -4, 0.4, 2.6)
    m.add(0, B.build(), "market")
    return m


def chorsu():
    m = Model("chorsu")
    B = Batch("chorsu")
    B.box(GROUND, 0, 0, 0, 36, 36, 0.3)
    B.box(PAVE, 0, 0, 0.3, 34, 6, 0.1)
    B.box(PAVE, 0, 0, 0.3, 6, 34, 0.1)
    B.prism(BRICK_LT, ngon(11.5, 8, 0.0), 0.3, 7.5, 0, 0)
    apo = 11.5 * math.cos(math.pi / 8)
    for k in range(8):
        a = math.pi / 8 + math.tau * k / 8
        O = (apo * math.cos(a), apo * math.sin(a), 0.3)
        if k % 2 == 0:
            B.panel(BRICK_DK, arch_outline(5.5, 7.0), O, a, 0.2)
            B.panel(DARK, arch_outline(3.6, 5.6), O, a, 0.12, 0.2)
        else:
            B.panel(DARK, arch_outline(2.2, 3.2), O, a, 0.1)
            B.rect(TURQ, O, a, -3.0, 3.0, 6.2, 7.0, 0.1)
    B.prism(BRICK_LT, ngon(8.0, 16, 0.0), 7.8, 2.6, 0, 0)
    for k in range(16):
        a = math.tau * (k + 0.5) / 16
        B.panel(DARK, arch_outline(1.0, 1.6), (8.0 * math.cos(math.pi / 16) * math.cos(a), 8.0 * math.cos(math.pi / 16) * math.sin(a), 8.2), a, 0.06)
    smooth_dome(B, 7.6, 0, 0, 10.4, BRICK_LT, 0.9, finial=BRONZE, rings=8)
    for k in range(4):
        a = math.pi / 4 + math.tau * k / 4
        x, y = 14.5 * math.cos(a), 14.5 * math.sin(a)
        B.box(MUD, x, y, 0.3, 6, 6, 3.6, a)
        B.box(AWNINGS[k], x - 1.5 * math.cos(a), y - 1.5 * math.sin(a), 3.3, 7, 4, 0.18, a)
    m.add(0, B.build(), "dome")
    return m


def bagh_i_dilkusha():
    m = Model("bagh-i-dilkusha")
    B = Batch("dil_walls")
    B.box(GROUND, 0, 0, 0, 202, 202, 0.3)
    wall_ring(B, [(-98, -98), (98, -98), (98, 98), (-98, 98)], 5, 1.6, MUD, towers=4.0, tower_h=7.5, every=49, merlons=False, z=0.3)
    m.add(0, B.build(), "walls")
    m.add(0, put(portal("dil_gate", 18, 19, 8, spandrel=TWHITE), 0, -102), "walls")
    m.add(1, charbagh("dil_garden", 186, 186, (0, 0, 0.3), PAVE, LAWN, WATER_C, trees=True), "garden")
    P = Batch("dil_pav")
    P.box(PAVE_DK, 0, 0, 0.3, 32, 32, 2.0)
    P.box(WATER_C, 0, 0, 0.3, 40, 40, 0.6)
    P.box(BRICK_T, 0, 0, 2.3, 18, 18, 11)
    P.box(BRICK_LT, 0, 0, 13.3, 18.4, 18.4, 0.5)
    for ang, (dx, dy) in ((SOUTH, (0, -9)), (NORTH, (0, 9)), (EAST, (9, 0)), (WEST, (-9, 0))):
        P.rect(TURQ, (dx, dy, 2.3), ang, -6.5, 6.5, 0.3, 10.6, 0.16)
        P.panel(DEEP, arch_outline(8.2, 9.2), (dx, dy, 2.3), ang, 0.25)
        P.panel(TWHITE, arch_outline(2.4, 3.6), (dx, dy, 2.3), ang, 0.1, 0.25)
        kufic_band(P, (dx, dy, 2.3), ang, -8.5, 8.5, 9.6, 10.6, COBALT, TWHITE)
    drum_dome(P, 6.2, 0, 0, 13.8, 3.0, 24, DOME, 1.45)
    for i in range(10):
        for s in (-1, 1):
            tree_b(P, s * 8.5, -90 + i * 7.5 if i < 5 else 20 + (i - 5) * 15, 0.3, 1.8, "poplar")
    # silk tents of the court in the garden
    for x, y, c in ((-48, -40, "#B8553E"), (48, -36, "#C9A24A"), (-44, 46, "#4E6E8E")):
        P.lathe(c, [(7, 0), (7, 4.0), (6.4, 4.2), (0.0, 8.5)], x, y, 0.3, 16)
        P.lathe(TWHITE, [(7.05, 3.2), (7.05, 4.0)], x, y, 0.3, 16, cap_top=False, cap_bottom=False)
        P.panel(DARK, [(-1.4, 0), (1.4, 0), (1.4, 3.2), (-1.4, 3.2)], (x, y - 7, 0.3), SOUTH, 0.1)
    m.add(2, P.build(), "pavilion")
    return m


BUILDERS = {
    "samarkand/registan-1404": lambda: registan("1404"),
    "samarkand/registan-1440": lambda: registan("1440"),
    "samarkand/registan-1650": lambda: registan("1650"),
    "samarkand/bibi-khanym": lambda: bibi_khanym(False),
    "samarkand/bibi-khanym-1650": lambda: bibi_khanym(True),
    "samarkand/gur-e-amir": gur_e_amir,
    "samarkand/shah-i-zinda": lambda: shah_i_zinda("1440"),
    "samarkand/shah-i-zinda-1404": lambda: shah_i_zinda("1404"),
    "samarkand/observatory": lambda: observatory(False),
    "samarkand/observatory-ruin": lambda: observatory(True),
    "samarkand/afrasiyab-citadel": lambda: afrasiyab_citadel(False),
    "samarkand/afrasiyab-citadel-ruin": lambda: afrasiyab_citadel(True),
    "samarkand/ambassadors-hall": ambassadors_hall,
    "samarkand/sogdian-temple": sogdian_temple,
    "samarkand/afrasiyab-mosque": afrasiyab_mosque,
    "samarkand/kok-saray": kok_saray,
    "samarkand/rukhabad": rukhabad,
    "samarkand/ak-saray": ak_saray,
    "samarkand/hazrat-khizr": hazrat_khizr,
    "samarkand/siab-bazaar": siab_bazaar,
    "samarkand/chorsu": chorsu,
    "samarkand/bagh-i-dilkusha": bagh_i_dilkusha,
}
