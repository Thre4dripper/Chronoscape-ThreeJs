"""Timbuktu landmark miniatures: the banco mosques of Djinguereber, Sankore and Sidi Yahya, Mansa Musa's palace,
the market and the caravan ground, the Moroccans' kasbah, scholars' and merchants' houses, the saints' tombs,
the well of Buktu, the Tuareg camp and the landing of the Kabara channel.

Conventions as in FORMAT.md: metres, origin at the ground centre, +X east, +Y north, +Z up. The mosques are built
with their qibla (prayer) wall toward -Y; the landmark rotation turns it toward Mecca (east-north-east).

Most small parts (toron beams, pilasters, pinnacles, studs, animals, slabs) are collected per colour in a
Parts buffer and made into one mesh each, which keeps hundreds of beams cheap to build.
"""
import math
from chronokit import Model, box, cylinder, dome, join, shade, mesh_from
from worldkit import *

BANCO, BANCO_LT, BANCO_DK = "#BC9C74", "#CDB08A", "#A3845E"
ALHOR = "#CDBC9C"
SAND, SAND_DK, SAND_WET = "#DCC69C", "#CFB78D", "#B9A27C"
TORON = "#5E4630"
DOOR, IRON = "#5A3C24", "#2E2A26"
MAT, STRAW, REED = "#B39960", "#C6AC6C", "#A89466"
LEATHER, LEATHER_DK = "#93603B", "#6C4429"
SALT = "#E7E2D6"
CAMEL_C, DONKEY_C, GOAT_C, HORSE_C = "#B48C5E", "#8C8277", "#6E5A48", "#7A5236"
ACACIA, THORN = "#7A8A52", "#66683F"
EGG, POT, GRAIN, CLOTH = "#F3EFE6", "#9C5E3C", "#D6B86A", "#3F5E8C"
WATER_C, FIRE = "#5F878C", "#C8642E"
BOAT = "#5E4532"
FACES = {"S": (0, -1), "N": (0, 1), "E": (1, 0), "W": (-1, 0)}
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
                q = [p[i] + a * u[i] + b * v[i] for i in range(3)]
                q[2] = max(0.0, q[2])
                verts.append(tuple(q))
        self.poly(color, verts, BOX_FACES)

    def build(self):
        objs = [mesh_from(f"{self.name}_{i}", vs, fs, (0, 0, 0), color) for i, (color, (vs, fs)) in enumerate(self.g.items()) if fs]
        return join(objs, self.name)


# ---------------------------------------------------------------- Sahelian banco architecture

def fbox(P, color, x, y, z0, along, out, h, face, off=0.0):
    """A box on a wall face: `along` the face, `out` across it, centred `off` metres out from (x, y)."""
    nx, ny = FACES[face]
    if nx == 0:
        P.cube(color, x, y + ny * off, z0, along, out, h)
    else:
        P.cube(color, x + nx * off, y, z0, out, along, h)


def tangent(face):
    nx, ny = FACES[face]
    return (abs(ny), abs(nx))


def face_line(cx, cy, w, d, face):
    """The middle, length and outward normal of one face of a w x d block."""
    nx, ny = FACES[face]
    if nx == 0:
        return (cx, cy + ny * d / 2), w, (nx, ny)
    return (cx + nx * w / 2, cy), d, (nx, ny)


def parapet(P, cx, cy, z, w, d, color, t=0.35, h=0.55):
    P.cube(color, cx, cy - d / 2 + t / 2, z, w, t, h)
    P.cube(color, cx, cy + d / 2 - t / 2, z, w, t, h)
    P.cube(color, cx - w / 2 + t / 2, cy, z, t, d - 2 * t, h)
    P.cube(color, cx + w / 2 - t / 2, cy, z, t, d - 2 * t, h)


def sahel_block(P, cx, cy, w, d, h, z0=0.0, color=BANCO, faces="NSEW", every=3.2, pil=0.8, out=0.45, spikes=True,
                toron=(0.4, 0.72), stick=0.8, para=0.55, toron_on="both", spike_h=1.0):
    """A banco block: flat roof behind a parapet, tapering pilasters rising into pinnacles, rows of toron beams."""
    P.cube(color, cx, cy, z0, w, d, h)
    parapet(P, cx, cy, z0 + h, w, d, shade(color, -0.04), h=para)
    for face in faces:
        (mx, my), L, (nx, ny) = face_line(cx, cy, w, d, face)
        tx, ty = tangent(face)
        n = max(1, round(L / every))
        for i in range(n + 1):
            u = -L / 2 + L * i / n
            px, py = mx + tx * u, my + ty * u
            fx, fy = px + nx * out / 2, py + ny * out / 2
            if nx == 0:
                P.frustum(color, fx, fy, z0, pil, out, pil * 0.72, out * 0.55, h + para)
            else:
                P.frustum(color, fx, fy, z0, out, pil, out * 0.55, pil * 0.72, h + para)
            if spikes:
                P.cone(shade(color, 0.03), fx, fy, z0 + h + para, pil * 0.36, 0.05, spike_h, 6)
            spots = []
            if toron and toron_on in ("both", "pilaster"):
                spots.append((px, py, out))
            if toron and toron_on in ("both", "bay") and i < n:
                spots.append((px + tx * L / n / 2, py + ty * L / n / 2, 0.0))
            for sx, sy, o in spots:
                for t in toron:
                    z = z0 + h * t
                    P.cube(TORON, sx + nx * (o + stick / 2 - 0.1), sy + ny * (o + stick / 2 - 0.1), z, stick if nx else 0.14, stick if ny else 0.14, 0.14)


def plain_block(P, cx, cy, w, d, h, z0=0.0, color=BANCO, para=0.45, spikes=0):
    """A simple banco box with a parapet (houses, stores) and optional corner pinnacles."""
    P.cube(color, cx, cy, z0, w, d, h)
    parapet(P, cx, cy, z0 + h, w, d, shade(color, -0.05), 0.3, para)
    if spikes:
        for sx in (-1, 1):
            for sy in (-1, 1):
                P.cone(color, cx + sx * (w / 2 - 0.2), cy + sy * (d / 2 - 0.2), z0 + h + para, 0.3, 0.04, spikes, 6)


def crest_spikes(P, cx, cy, w, d, z, every=1.6, color=BANCO, h=0.7, faces="NSEW"):
    """Small pinnacles all along the parapet of a house roof."""
    for face in faces:
        (mx, my), L, (nx, ny) = face_line(cx, cy, w - 0.3, d - 0.3, face)
        tx, ty = tangent(face)
        n = max(1, int(L / every))
        for i in range(n + 1):
            u = -L / 2 + L * i / n
            P.cone(color, mx + tx * u, my + ty * u, z, 0.2, 0.03, h, 5)


def cone_tower(P, x, y, r, h, color=BANCO, levels=4, sticks=6, egg=True, n=12, z0=0.0, top=0.3):
    """A conical buttress or mihrab tower of banco, toron sticking out all round, an ostrich-egg finial."""
    rt = r * top
    P.cone(color, x, y, z0, r, rt, h, n)
    P.dome(color, x, y, z0 + h, rt * 1.02, 1.1, n, 3)
    if egg:
        P.cone(color, x, y, z0 + h + rt * 0.9, 0.12, 0.08, 0.6, 6)
        P.dome(EGG, x, y, z0 + h + rt * 0.9 + 0.55, 0.26, 1.5, 8, 3)
    for k in range(levels):
        z = h * (0.16 + 0.72 * k / max(1, levels - 1)) if levels > 1 else h * 0.5
        rz = r + (rt - r) * z / h
        for j in range(sticks):
            a = math.tau * j / sticks + (k % 2) * math.pi / sticks
            P.beam(TORON, (x + (rz - 0.25) * math.cos(a), y + (rz - 0.25) * math.sin(a), z0 + z), (x + (rz + 0.75) * math.cos(a), y + (rz + 0.75) * math.sin(a), z0 + z), 0.15)


def square_tower(P, x, y, w0, w1, h, color=BANCO, rows=5, cols=3, z0=0.0, stick=0.85, lantern=True, door_face=None):
    """A tapering square minaret of banco (Djinguereber, Sidi Yahya): toron in rows on every face, pinnacles and an egg."""
    P.frustum(color, x, y, z0, w0, w0, w1, w1, h)
    for k in range(rows):
        z = h * (0.1 + 0.8 * k / max(1, rows - 1))
        half = (w0 + (w1 - w0) * z / h) / 2
        for face, (nx, ny) in FACES.items():
            tx, ty = tangent(face)
            for c in range(cols):
                u = half * (-0.66 + 1.32 * c / (cols - 1)) if cols > 1 else 0.0
                bx, by = x + nx * half + tx * u, y + ny * half + ty * u
                P.beam(TORON, (bx - nx * 0.25, by - ny * 0.25, z0 + z), (bx + nx * stick, by + ny * stick, z0 + z), 0.15)
    zt = z0 + h
    parapet(P, x, y, zt, w1 + 0.3, w1 + 0.3, shade(color, -0.04), 0.3, 0.6)
    for sx in (-1, 1):
        for sy in (-1, 1):
            P.cone(color, x + sx * (w1 / 2), y + sy * (w1 / 2), zt, 0.42, 0.05, 1.5, 6)
    if lantern:
        lw = w1 * 0.45
        P.frustum(color, x, y, zt, lw, lw, lw * 0.75, lw * 0.75, 2.0)
        P.cone(color, x, y, zt + 2.0, lw * 0.35, 0.06, 0.9, 6)
        P.dome(EGG, x, y, zt + 2.8, 0.3, 1.5, 8, 3)
    if door_face:
        nx, ny = FACES[door_face]
        fbox(P, DARK, x + nx * w0 / 2, y + ny * w0 / 2, z0, 1.2, 0.2, 2.2, door_face, 0.02)


def stepped_minaret(P, x, y, w, h, tiers=5, color=BANCO, z0=0.0, cols=3, stick=0.85):
    """Sankore's minaret: a stepped, tapering pyramid of banco in tiers, toron on every tier, an egg on top."""
    th = h / tiers
    for t in range(tiers):
        wb = w * (1 - 0.15 * t)
        wt = wb * 0.88
        z = z0 + t * th
        P.frustum(color, x, y, z, wb, wb, wt, wt, th)
        P.frustum(shade(color, -0.05), x, y, z + th - 0.25, wt + 0.5, wt + 0.5, wt + 0.3, wt + 0.3, 0.3)
        half = (wb + wt) / 4
        nc = cols if t < tiers - 2 else 2
        for face, (nx, ny) in FACES.items():
            tx, ty = tangent(face)
            for c in range(nc):
                u = half * (-0.6 + 1.2 * c / (nc - 1)) if nc > 1 else 0.0
                bx, by = x + nx * half + tx * u, y + ny * half + ty * u
                for zz in (0.35, 0.72):
                    P.beam(TORON, (bx - nx * 0.25, by - ny * 0.25, z + th * zz), (bx + nx * stick, by + ny * stick, z + th * zz), 0.15)
    wtop = w * (1 - 0.15 * (tiers - 1)) * 0.88
    zt = z0 + h
    for sx in (-1, 1):
        for sy in (-1, 1):
            P.cone(color, x + sx * wtop * 0.4, y + sy * wtop * 0.4, zt, 0.35, 0.05, 1.2, 6)
    P.cone(color, x, y, zt, wtop * 0.3, 0.1, 1.6, 8)
    P.dome(EGG, x, y, zt + 1.55, 0.32, 1.5, 8, 3)


def roof_vents(P, x0, x1, y0, y1, z, step=4.0, color=BANCO_DK):
    """Roof openings with their clay lids, in a grid on a flat roof."""
    nx, ny = max(1, int((x1 - x0) / step)), max(1, int((y1 - y0) / step))
    for i in range(nx):
        for j in range(ny):
            x = x0 + (i + 0.5) * (x1 - x0) / nx
            y = y0 + (j + 0.5) * (y1 - y0) / ny
            if (i + j) % 2 == 0:
                P.cube(DARK, x, y, z, 0.6, 0.6, 0.05)
                P.cone(color, x + 0.5, y, z, 0.32, 0.26, 0.28, 6)


def carved_door(P, x, y, w, h, face, z0=0.0, studs=True, frame=BANCO_LT):
    """A wooden door in a moulded frame, studded with iron (Timbuktu's carved doors)."""
    tx, ty = tangent(face)
    fbox(P, frame, x, y, z0, w + 0.6, 0.3, h + 0.45, face, 0.1)
    fbox(P, DOOR, x, y, z0, w, 0.12, h, face, 0.28)
    if studs:
        for r in range(4):
            for c in range(3):
                u = w * (-0.32 + 0.32 * c)
                fbox(P, IRON, x + tx * u, y + ty * u, z0 + h * (0.18 + 0.22 * r), 0.09, 0.08, 0.09, face, 0.37)
        fbox(P, IRON, x, y, z0 + h * 0.5, 0.25, 0.08, 0.25, face, 0.37)


def moroccan_window(P, x, y, z, face, w=1.1, h=1.3):
    """A carved wooden window frame with a grille, of the kind brought in after the Moroccan conquest."""
    tx, ty = tangent(face)
    fbox(P, TORON, x, y, z, w + 0.3, 0.22, h + 0.3, face, 0.1)
    fbox(P, DARK, x, y, z + 0.15, w, 0.1, h, face, 0.2)
    for c in range(3):
        u = w * (-0.3 + 0.3 * c)
        fbox(P, TORON, x + tx * u, y + ty * u, z + 0.15, 0.08, 0.1, h, face, 0.26)
    fbox(P, TORON, x, y, z + 0.15 + h * 0.5, w, 0.1, 0.08, face, 0.26)
    fbox(P, BANCO_LT, x, y, z + h + 0.35, w + 0.7, 0.45, 0.18, face, 0.22)


def sudan_window(P, x, y, z, face, w=0.6, h=0.8):
    tx, ty = tangent(face)
    fbox(P, BANCO_LT, x, y, z - 0.15, w + 0.4, 0.2, h + 0.3, face, 0.08)
    fbox(P, DARK, x, y, z, w, 0.08, h, face, 0.18)


def spouts(P, cx, cy, w, d, z, face, n, color=TORON):
    """Roof drain spouts sticking out over the lane."""
    (mx, my), L, (nx, ny) = face_line(cx, cy, w, d, face)
    tx, ty = tangent(face)
    for i in range(n):
        u = -L / 2 + L * (i + 0.5) / n
        fbox(P, color, mx + tx * u, my + ty * u, z, 0.22, 0.8, 0.2, face, 0.35)


# ---------------------------------------------------------------- life on the ground

def acacia(P, x, y, r=3.0, h=4.2):
    P.beam(TIMBER, (x, y, 0), (x + 0.3, y + 0.2, h * 0.68), 0.32)
    P.beam(TIMBER, (x + 0.3, y + 0.2, h * 0.66), (x - 0.9, y - 0.2, h * 0.86), 0.2)
    P.beam(TIMBER, (x + 0.3, y + 0.2, h * 0.66), (x + 1.3, y + 0.6, h * 0.86), 0.2)
    P.cone(ACACIA, x + 0.15, y + 0.1, h * 0.82, r, r * 0.72, h * 0.2, 9)


def hut(P, x, y, r=1.8, color=STRAW, door="S"):
    """A domed hut of mats and straw over bent poles (the Bella and herders' huts)."""
    P.dome(color, x, y, 0, r, 0.78, 10, 4)
    nx, ny = FACES[door]
    fbox(P, DARK, x + nx * r * 0.9, y + ny * r * 0.9, 0, min(0.7, r * 0.4), 0.3, min(1.0, r * 0.42), door, 0.0)
    P.cone(shade(color, -0.12), x, y, r * 0.74, 0.25, 0.05, 0.35, 6)


def tent(P, x, y, w=5.0, d=3.6, h=1.7, color=LEATHER):
    """A Tuareg tent of tanned goatskins on poles, a mat screen at the back."""
    for px in (-w / 2 + 0.3, 0, w / 2 - 0.3):
        for py in (-d / 2 + 0.3, d / 2 - 0.3):
            P.beam(TORON, (x + px, y + py, 0), (x + px, y + py, h), 0.1)
    P.frustum(color, x, y, h - 0.25, w - 0.2, d - 0.4, w + 0.6, d + 0.5, 0.25)
    P.frustum(color, x, y, h, w + 0.6, d + 0.5, w * 0.5, d * 0.35, 0.35)
    P.cube(MAT, x, y + d / 2 - 0.1, 0, w - 0.2, 0.08, h - 0.3)
    P.cube(LEATHER_DK, x - w * 0.25, y + d / 2 - 0.6, 0, 0.8, 0.6, 0.5)
    P.cube(CLOTH, x + w * 0.2, y + d / 2 - 0.6, 0, 1.0, 0.5, 0.35)


def stall(P, x, y, w=4.0, d=3.0, h=2.2, roof=MAT, goods=GRAIN):
    for px in (-w / 2 + 0.15, w / 2 - 0.15):
        for py in (-d / 2 + 0.15, d / 2 - 0.15):
            P.beam(TORON, (x + px, y + py, 0), (x + px, y + py, h + (0.25 if py > 0 else 0)), 0.1)
    P.frustum(roof, x, y, h, w + 0.4, d + 0.4, w + 0.2, d + 0.2, 0.18)
    P.cube(MAT, x, y, 0, w * 0.7, d * 0.5, 0.3)
    P.dome(goods, x - w * 0.15, y, 0.3, 0.45, 0.8, 8, 2)
    P.dome(shade(goods, -0.2), x + w * 0.18, y, 0.3, 0.38, 0.8, 8, 2)


def salt_stack(P, x, y, levels=6, rows=2, along_x=True):
    """Slabs of rock salt from the Saharan mines, stacked crosswise."""
    for k in range(levels):
        for r in range(rows):
            off = (r - (rows - 1) / 2) * 0.5
            if (k % 2 == 0) == along_x:
                P.cube(SALT, x, y + off, k * 0.11, 1.1, 0.45, 0.1)
            else:
                P.cube(SALT, x + off, y, k * 0.11, 0.45, 1.1, 0.1)


def pot(P, x, y, r=0.3, h=0.6, color=POT):
    P.cone(color, x, y, 0, r * 0.7, r, h * 0.55, 8)
    P.cone(color, x, y, h * 0.55, r, r * 0.55, h * 0.45, 8)


def sacks(P, x, y, n=4, color=GRAIN):
    for i in range(n):
        P.cube(shade(color, -0.04 * (i % 3)), x + (i % 2) * 0.75, y + (i // 2) * 0.6, 0, 0.7, 0.5, 0.45)
    if n > 2:
        P.cube(color, x + 0.37, y + 0.3, 0.45, 0.7, 0.5, 0.42)


def animal(P, kind, x, y, deg=0.0, kneel=False, load=None):
    """A low-poly camel, donkey, horse or goat, facing +X turned by deg."""
    c, s = math.cos(math.radians(deg)), math.sin(math.radians(deg))

    def T(px, py, pz):
        return (x + px * c - py * s, y + px * s + py * c, pz)

    L, zb, t, col, nk, hd, leg = {
        "camel": (1.0, 1.55, 0.72, CAMEL_C, (1.45, 0.95), 0.52, 0.17),
        "donkey": (0.55, 0.8, 0.4, DONKEY_C, (0.8, 0.45), 0.35, 0.1),
        "horse": (0.8, 1.15, 0.52, HORSE_C, (1.05, 0.7), 0.45, 0.13),
        "goat": (0.34, 0.45, 0.26, GOAT_C, (0.5, 0.25), 0.2, 0.07),
    }[kind]
    if kneel:
        zb = t * 0.75
    P.beam(col, T(-L, 0, zb), T(L, 0, zb + 0.05), t, t * 0.95)
    P.beam(col, T(L * 0.8, 0, zb + 0.05), T(nk[0], 0, zb + nk[1]), t * 0.38)
    P.beam(col, T(nk[0] - 0.05, 0, zb + nk[1]), T(nk[0] + hd, 0, zb + nk[1] - hd * 0.25), t * 0.36)
    if kind == "camel":
        hx, hy, _ = T(-0.05, 0, 0)
        P.cone(col, hx, hy, zb + t * 0.35, 0.42, 0.12, 0.55, 6)
    if kind == "donkey":
        for e in (-0.06, 0.06):
            P.beam(col, T(nk[0], e, zb + nk[1] + 0.05), T(nk[0] - 0.08, e * 2, zb + nk[1] + 0.32), 0.05)
    if kind == "goat":
        P.beam("#3A3028", T(nk[0], 0, zb + nk[1] + 0.05), T(nk[0] - 0.12, 0, zb + nk[1] + 0.22), 0.04)
    if kneel:
        P.beam(col, T(-L * 0.9, 0, t * 0.15), T(L * 0.9, 0, t * 0.15), t * 1.25, t * 0.3)
    else:
        for lx in (-L * 0.75, L * 0.7):
            for ly in (-t * 0.3, t * 0.3):
                P.beam(col, T(lx, ly, zb - t * 0.35), T(lx, ly, 0), leg)
    if kind == "horse":
        P.beam("#3A2A1E", T(-L, 0, zb + 0.1), T(-L - 0.25, 0, zb - 0.5), 0.1)
    if load == "salt":
        for side in (-1, 1):
            P.beam(SALT, T(-0.5, side * (t / 2 + 0.08), zb - 0.05), T(0.5, side * (t / 2 + 0.08), zb - 0.05), 0.11, 0.48)
    elif load == "sacks":
        for side in (-1, 1):
            P.beam(GRAIN, T(-L * 0.4, side * (t / 2 + 0.12), zb - 0.05), T(L * 0.4, side * (t / 2 + 0.12), zb - 0.05), 0.28, 0.35)
    elif load == "saddle":
        P.beam(LEATHER, T(-0.25, 0, zb + t / 2 + 0.25), T(0.25, 0, zb + t / 2 + 0.25), 0.7, 0.18)


def pirogue(P, x, y, deg=0.0, L=9.0, B=1.2, H=0.55, canopy=False):
    """A Niger pirogue: a long plank boat with raised pointed ends, sometimes a mat shelter amidships."""
    c, s = math.cos(math.radians(deg)), math.sin(math.radians(deg))

    def T(px, py, pz):
        return (x + px * c - py * s, y + px * s + py * c, pz)

    top = [(-L / 2, 0), (-L * 0.33, -B / 2), (L * 0.33, -B / 2), (L / 2, 0), (L * 0.33, B / 2), (-L * 0.33, B / 2)]
    zt = [H + 0.3, H, H, H + 0.3, H, H]
    v = [T(px * 0.86, py * 0.45, 0.0) for px, py in top] + [T(px, py, z) for (px, py), z in zip(top, zt)]
    f = [tuple(range(6))[::-1], tuple(range(6, 12))] + [(i, (i + 1) % 6, 6 + (i + 1) % 6, 6 + i) for i in range(6)]
    P.poly(BOAT, v, f)
    inner = [T(px * 0.8, py * 0.7, H + 0.02) for px, py in top[1:3] + top[4:6]]
    P.poly(DARK, [inner[0], inner[1], inner[2], inner[3]], [(0, 1, 2, 3)])
    if canopy:
        a, b = -1.3, 1.3
        hw = B / 2 + 0.05
        pts = [(a, -hw, H), (b, -hw, H), (b, hw, H), (a, hw, H), (a, 0, H + 1.1), (b, 0, H + 1.1)]
        v = [T(*p) for p in pts]
        P.poly(MAT, v, [(0, 1, 5, 4), (3, 4, 5, 2), (0, 4, 3), (1, 2, 5)])


def thorn_pen(P, x, y, r=5.0, n=16):
    for i in range(n):
        if i == 0:
            continue
        a = math.tau * i / n
        P.cone(THORN, x + r * math.cos(a), y + r * math.sin(a), 0, 0.75, 0.3, 0.9, 6)


def graves(P, x0, x1, y0, y1, n, seed=1, color=ALHOR):
    """Rows of graves: a low mound of sand between a head and foot stone."""
    k = seed
    cols = max(1, int(math.sqrt(n * (x1 - x0) / max(1, y1 - y0))))
    rows = max(1, n // cols)
    for i in range(cols):
        for j in range(rows):
            k = (k * 1103515245 + 12345) % 2147483648
            jx = (k % 100) / 100 - 0.5
            x = x0 + (i + 0.5 + jx * 0.4) * (x1 - x0) / cols
            y = y0 + (j + 0.5) * (y1 - y0) / rows
            P.cube(SAND_DK, x, y, 0, 0.8, 1.9, 0.25)
            P.cube(color, x, y - 1.0, 0, 0.35, 0.15, 0.55)
            P.cube(color, x, y + 1.0, 0, 0.3, 0.15, 0.4)


def rnd(seed):
    """A tiny deterministic random sequence in [0, 1)."""
    k = seed
    while True:
        k = (k * 1103515245 + 12345) % 2147483648
        yield (k >> 8) / 8388608.0


# ---------------------------------------------------------------- the great mosques

def djinguereber(variant="1450"):
    m = Model("djinguereber")
    W, D = 82, 70
    g = Parts("dj_ground")
    g.cube(SAND, 0, 0, 0, W, D, 0.25)
    if variant == "1340":
        x0, x1, y0, y1, hh, cy1 = -20, 30, -31, -11, 5.5, 14
    elif variant == "1700":
        x0, x1, y0, y1, hh, cy1 = -39, 39, -30.5, -6, 7.0, 23
    else:
        x0, x1, y0, y1, hh, cy1 = -30, 39, -30.5, -8, 6.5, 28
    hcx, hcy, hw, hd = (x0 + x1) / 2, (y0 + y1) / 2, x1 - x0, y1 - y0
    g.cube(SAND_DK, hcx, (y1 + cy1) / 2, 0, hw - 2, cy1 - y1, 0.35)
    walls = Parts("dj_walls")
    roof = Parts("dj_roof")
    towers = Parts("dj_towers")
    openings = []
    # prayer hall: rows of earth pillars under a flat roof; the court side opens in a long arcade
    sahel_block(walls, hcx, hcy, hw, hd, hh, faces="SEW", every=3.0, toron=(0.32, 0.6, 0.86), pil=0.9, out=0.55)
    openings.append(arcade("dj_hall_arc", hw - 3, hh * 0.72, max(4, int(hw / 3.2)), (hcx, y1 + 0.02, 0), "N", DARK, True, 0.6, 0.3))
    for xp in [x0 + 1.6 + i * 3.2 for i in range(int((hw - 3) / 3.2) + 1)]:
        roof.cube(BANCO_DK, xp, y1 + 0.45, 0, 1.1, 0.9, hh * 0.85)
    roof_vents(roof, x0 + 2, x1 - 2, y0 + 2, y1 - 2, hh, 3.6)
    # raised clerestory over the mihrab aisle
    plain_block(roof, hcx, (y0 + 3 + y1 - 4) / 2, 9, (y1 - 4) - (y0 + 3), 1.3, z0=hh, color=BANCO_LT, spikes=0.9)
    for k in range(3):
        roof.cube(DARK, hcx + 4.55, y0 + 6 + k * 5, hh + 0.3, 0.1, 1.0, 0.6)
        roof.cube(DARK, hcx - 4.55, y0 + 6 + k * 5, hh + 0.3, 0.1, 1.0, 0.6)
    if variant != "1340":
        # the stone (alhor) end of the hall: the one part of the north facade built of limestone
        walls.cube(ALHOR, x1 + 0.12, hcy, 0, 0.3, hd - 2, hh * 0.92)
        for k in range(5):
            walls.cube(shade(ALHOR, -0.08), x1 + 0.3, hcy, hh * (0.12 + 0.18 * k), 0.1, hd - 2, 0.12)
    # court and its galleries
    if variant == "1340":
        for (cx, cy, w, d, faces) in ((hcx, cy1 - 0.5, hw, 1.0, "N"), (x0 + 0.5, (y1 + cy1) / 2, 1.0, cy1 - y1, "W"), (x1 - 0.5, (y1 + cy1) / 2, 1.0, cy1 - y1, "E")):
            sahel_block(walls, cx, cy, w, d, 3.2, faces=faces, every=3.0, toron=(0.5,), toron_on="pilaster", pil=0.7, out=0.4)
        carved_door(walls, x0 - 0.0, (y1 + cy1) / 2, 1.5, 2.4, "W")
        carved_door(walls, hcx - 8, cy1, 1.5, 2.4, "N")
    else:
        gd = 6.0
        sahel_block(walls, hcx, cy1 - gd / 2, hw, gd, 4.6, faces="NEW", every=3.0, toron=(0.42, 0.78), pil=0.8)
        openings.append(arcade("dj_n_arc", hw - 12, 3.4, max(4, int((hw - 12) / 3.0)), (hcx, cy1 - gd - 0.02, 0), "S", DARK, True, 0.6, 0.3))
        for (cx, face) in ((x0 + 2.5, "W"), (x1 - 2.5, "E")):
            sahel_block(walls, cx, (y1 + cy1 - gd) / 2, 5.0, cy1 - gd - y1, 4.4, faces=face, every=3.0, toron=(0.42, 0.78), pil=0.8)
            inner = "E" if face == "W" else "W"
            nx, _ = FACES[inner]
            openings.append(arcade(f"dj_{face}_arc", cy1 - gd - y1 - 2, 3.2, max(3, int((cy1 - gd - y1) / 3.2)), (cx + nx * 2.52, (y1 + cy1 - gd) / 2, 0), inner, DARK, True, 0.6, 0.3))
        roof_vents(roof, x0, x1, cy1 - gd + 1, cy1 - 1, 4.6, 4.0)
        carved_door(walls, hcx - 6, cy1, 1.8, 2.8, "N")
        carved_door(walls, x0, (y1 + cy1 - gd) / 2 + 3, 1.6, 2.6, "W")
        carved_door(walls, x1, (y1 + cy1 - gd) / 2 + 3, 1.6, 2.6, "E")
        if variant == "1700":
            # al-Aqib's southern addition: a second court beyond a pillared cross-range
            sahel_block(walls, -19, (y1 + cy1 - gd) / 2, 4.0, cy1 - gd - y1, 4.4, faces="", toron=())
            openings.append(arcade("dj_x_arc_e", cy1 - gd - y1 - 2, 3.2, 4, (-16.98, (y1 + cy1 - gd) / 2, 0), "E", DARK, True, 0.6, 0.3))
            openings.append(arcade("dj_x_arc_w", cy1 - gd - y1 - 2, 3.2, 4, (-21.02, (y1 + cy1 - gd) / 2, 0), "W", DARK, True, 0.6, 0.3))
            # the wall round the cemetery to the west (+Y)
            for (cx, cy, w, d, faces) in ((0, 34.4, 80, 1.0, "N"), (-39.5, 29.2, 1.0, 11.4, "W"), (39.5, 29.2, 1.0, 11.4, "E")):
                sahel_block(walls, cx, cy, w, d, 2.0, faces=faces, every=4.0, toron=(), pil=0.6, out=0.35, spike_h=0.7)
            graves(g, -34, 30, 25.5, 33, 26, 3)
            # a third, small court in the north-east corner
            sahel_block(walls, 21, (y1 + cy1 - gd) / 2, 3.5, cy1 - gd - y1, 4.4, faces="", toron=())
            openings.append(arcade("dj_y_arc", cy1 - gd - y1 - 2, 3.2, 4, (18.73, (y1 + cy1 - gd) / 2, 0), "W", DARK, True, 0.6, 0.3))
            for (ax, ay) in ((-30, 30), (14, 29.5), (33, 30.5)):
                acacia(g, ax, ay, 2.6, 3.8)
        else:
            graves(g, -36, 34, 30.5, 34.5, 14, 5)
            # a pillared cross-range divides the court in two
            sahel_block(walls, 12, (y1 + cy1 - gd) / 2, 4.0, cy1 - gd - y1, 4.4, faces="", toron=())
            openings.append(arcade("dj_x_arc_e", cy1 - gd - y1 - 2, 3.2, 5, (14.02, (y1 + cy1 - gd) / 2, 0), "E", DARK, True, 0.6, 0.3))
            openings.append(arcade("dj_x_arc_w", cy1 - gd - y1 - 2, 3.2, 5, (9.98, (y1 + cy1 - gd) / 2, 0), "W", DARK, True, 0.6, 0.3))
            for (ax, ay) in ((-36, 31.5), (20, 32.5)):
                acacia(g, ax, ay, 2.4, 3.6)
            # the imam's house and a small yard on the south side (-X)
            plain_block(walls, -35.5, -22, 7.5, 12, 4.2, spikes=0.8)
            carved_door(walls, -35.5, -16, 1.2, 2.2, "N")
            plain_block(walls, -35.5, -4, 7.5, 9, 2.4)
    if variant == "1340":
        for (ax, ay, r) in ((-33, 22, 2.6), (34, 26, 2.4), (-35, -20, 2.2), (36, -28, 2.0)):
            acacia(g, ax, ay, r, 3.6)
        for (hx, hy) in ((-34, 6), (-30, 30), (-24, 25), (25, 28)):
            hut(g, hx, hy, 1.9)
    # mihrab tower and conical buttresses on the qibla wall; the tapering minaret over the court
    cone_tower(towers, hcx, y0 - 1.2, 3.0 if variant != "1340" else 2.6, hh + (6.0 if variant != "1340" else 4.0), levels=4, sticks=7)
    for xb in (x0 + 0.2, x1 - 0.2):
        cone_tower(towers, xb, y0 - 0.2, 2.0, hh + 2.6, levels=2, sticks=5, egg=False)
    if variant == "1340":
        square_tower(towers, x1 - 6, cy1 - 3, 4.8, 2.6, 12.0, rows=4, cols=2, door_face="S")
    else:
        square_tower(towers, x1 - 8, cy1 - gd / 2 - 0.5, 7.4, 3.8, 16.5, rows=6, cols=3, door_face="S")
        if variant == "1700":
            square_tower(towers, x0 + 6, cy1 - gd / 2 - 0.5, 4.6, 2.6, 10.5, rows=4, cols=2)
    m.add(0, g.build(), "ground")
    m.add(1, join([walls.build()] + openings, "dj_hall"), "walls")
    m.add(2, roof.build(), "roof")
    m.add(3, towers.build(), "minaret")
    return m


def sankore(variant="1450"):
    m = Model("sankore")
    g = Parts("sk_ground")
    g.cube(SAND, 0, 0, 0, 56, 50, 0.25)
    walls, roof, tw = Parts("sk_walls"), Parts("sk_roof"), Parts("sk_tower")
    openings = []
    late = variant == "1700"
    # prayer hall along the qibla wall
    x0, x1, y0, y1, hh = -26, 26, -21, -4, 5.6
    sahel_block(walls, 0, (y0 + y1) / 2, x1 - x0, y1 - y0, hh, faces="SEW", every=2.6, toron=(0.3, 0.56, 0.82), pil=0.85, out=0.5)
    openings.append(arcade("sk_hall_arc", 46, 4.0, 14, (0, y1 + 0.02, 0), "N", DARK, True, 0.58, 0.3))
    for xp in [-23 + i * 46 / 13 for i in range(14)]:
        roof.cube(BANCO_DK, xp, y1 + 0.4, 0, 0.9, 0.8, hh * 0.8)
    roof_vents(roof, x0 + 2, x1 - 2, y0 + 2, y1 - 2, hh, 3.4)
    for xb in (x0, x1):
        cone_tower(walls, xb, y0, 1.8, hh + 2.4, levels=3, sticks=6, egg=False)
        cone_tower(walls, xb, 23.4, 1.3, 6.6, levels=2, sticks=6, egg=False)
    # the court, rebuilt by al-Aqib to the Kaaba's measurements (it is said); before 1578 a looser court
    if late:
        cx0, cx1, cy0, cy1 = -9, 9, -4, 14
    else:
        cx0, cx1, cy0, cy1 = -14, 12, -4, 17
    g.cube(SAND_DK, (cx0 + cx1) / 2, (cy0 + cy1) / 2, 0, cx1 - cx0, cy1 - cy0, 0.35)
    rh = 4.4
    # west and east ranges of rooms for teaching
    for (bx0, bx1, face) in ((-26, cx0, "W"), (cx1, 26, "E")):
        bw = bx1 - bx0
        sahel_block(walls, (bx0 + bx1) / 2, (cy0 + 24) / 2, bw, 24 - cy0, rh, faces=face + "N", every=2.6, toron=(0.35, 0.7), pil=0.8)
        inner = "E" if face == "W" else "W"
        ix = bx1 if face == "W" else bx0
        openings.append(arcade(f"sk_{face}_arc", cy1 - cy0 - 2, 3.1, 4 if late else 5, (ix + FACES[inner][0] * 0.02, (cy0 + cy1) / 2, 0), inner, DARK, True, 0.6, 0.3))
        roof_vents(roof, bx0 + 1, bx1 - 1, cy0 + 1, 23, rh, 3.6)
        for k in range(3):
            sudan_window(walls, bx0 if face == "W" else bx1, cy0 + 5 + k * 6, 2.0, face)
    # north range with the entrance
    sahel_block(walls, (cx0 + cx1) / 2, (cy1 + 24) / 2, cx1 - cx0, 24 - cy1, rh, faces="N", every=2.6, toron=(0.35, 0.7), pil=0.8)
    openings.append(arcade("sk_n_arc", cx1 - cx0 - 2, 3.1, 4, ((cx0 + cx1) / 2, cy1 - 0.02, 0), "S", DARK, True, 0.6, 0.3))
    carved_door(walls, (cx0 + cx1) / 2, 24, 1.7, 2.7, "N")
    carved_door(walls, -26, 8, 1.4, 2.4, "W")
    for (ax, ay) in ((-24, 22.5), (23, -23)):
        acacia(g, ax, ay, 2.2, 3.4)
    # the stepped pyramid of the minaret on the qibla side
    stepped_minaret(tw, 0, y0 + 3.0, 11.5 if late else 10.0, 17.0 if late else 14.5, tiers=5 if late else 4, cols=4)
    m.add(0, g.build(), "ground")
    m.add(1, join([walls.build()] + openings, "sk_hall"), "walls")
    m.add(2, roof.build(), "roof")
    m.add(3, tw.build(), "minaret")
    return m


def sidi_yahya():
    m = Model("sidi-yahya")
    g = Parts("sy_ground")
    g.cube(SAND, 0, 0, 0, 42, 36, 0.25)
    walls, roof, tw = Parts("sy_walls"), Parts("sy_roof"), Parts("sy_tower")
    openings = []
    hh = 5.2
    sahel_block(walls, 0, -9.5, 38, 13, hh, faces="SEW", every=2.8, toron=(0.36, 0.7), pil=0.8)
    openings.append(arcade("sy_hall_arc", 34, 3.8, 10, (0, -2.98, 0), "N", DARK, True, 0.58, 0.3))
    roof_vents(roof, -17, 17, -14.5, -4.5, hh, 3.4)
    # the saint's tomb chamber, raised over the roof
    plain_block(roof, 11, -9.5, 5.5, 5.5, 1.6, z0=hh, color=BANCO_LT, spikes=0.9)
    g.cube(SAND_DK, 0, 4.5, 0, 26, 13, 0.35)
    for (cx, face) in ((-16, "W"), (16, "E")):
        sahel_block(walls, cx, 4.5, 6, 15, 4.2, faces=face, every=2.8, toron=(0.45, 0.8), pil=0.75)
        inner = "E" if face == "W" else "W"
        openings.append(arcade(f"sy_{face}_arc", 11, 3.0, 3, (cx + FACES[inner][0] * 3.02, 4.5, 0), inner, DARK, True, 0.6, 0.3))
    sahel_block(walls, 0, 14.0, 38, 5, 4.4, faces="NEW", every=2.8, toron=(0.45, 0.8), pil=0.8)
    openings.append(arcade("sy_n_arc", 22, 3.0, 6, (2.5, 11.48, 0), "S", DARK, True, 0.6, 0.3))
    # the great carved door of the facade, said never to be opened
    carved_door(walls, 4, 16.5, 2.0, 3.3, "N")
    for k in (-1, 1):
        sudan_window(walls, 4 + k * 5, 16.5, 2.2, "N")
    cone_tower(tw, 0, -16.1, 2.0, hh + 4.0, levels=3, sticks=6)
    # squat minaret over the entrance range
    square_tower(tw, -9, 13.5, 6.0, 4.2, 10.5, rows=4, cols=3, z0=0.0)
    acacia(g, 18, -16.5, 1.8, 3.2)
    m.add(0, g.build(), "ground")
    m.add(1, join([walls.build()] + openings, "sy_hall"), "walls")
    m.add(2, join([roof.build(), tw.build()], "sy_top"), "minaret")
    return m


# ---------------------------------------------------------------- palaces and fortress

def madugu():
    m = Model("madugu")
    g = Parts("md_ground")
    g.cube(SAND, 0, 0, 0, 60, 50, 0.25)
    g.cube(SAND_DK, 0, -6, 0, 52, 30, 0.3)
    walls, house, top = Parts("md_walls"), Parts("md_house"), Parts("md_top")
    # enclosure wall with buttresses
    for (cx, cy, w, d, f) in ((0, -22.9, 57, 1.2, "S"), (0, 23.9, 57, 1.2, "N"), (-28.0, 0.5, 1.2, 46, "W"), (28.0, 0.5, 1.2, 46, "E")):
        sahel_block(walls, cx, cy, w, d, 3.8, faces=f, every=3.6, toron=(0.35, 0.7), pil=0.8, out=0.45)
    # gate block with conical buttresses
    sahel_block(walls, 0, -22.5, 9, 4, 5.6, faces="SEW", every=2.2, toron=(0.4, 0.75), pil=0.8)
    carved_door(walls, 0, -24.5, 2.2, 3.3, "S")
    for gx in (-4.6, 4.6):
        cone_tower(walls, gx, -24.0, 1.3, 6.6, levels=2, sticks=5)
    # audience house: two storeys on the north side of the court
    sahel_block(house, -6, 12, 26, 14, 4.6, faces="NSEW", every=2.6, toron=(0.4, 0.78), pil=0.85)
    sahel_block(house, -8, 13, 16, 10, 3.6, z0=4.6 + 0.0, faces="SEW", every=2.6, toron=(0.5,), pil=0.75, out=0.4)
    carved_door(house, -6, 5, 2.0, 3.0, "S")
    for k in (-2, -1, 1, 2):
        sudan_window(house, -8 + k * 3.4, 8, 5.9, "S")
    roof_vents(top, -18, 6, 6, 18, 4.6, 4.0)
    # store rooms, a stable shed for the cavalry and guards' huts
    for i in range(4):
        plain_block(house, 22, -16 + i * 8.5, 9, 7.5, 3.4, spikes=0.6)
        carved_door(house, 17.5, -16 + i * 8.5, 1.1, 2.0, "W", studs=False)
    plain_block(house, -22, 8, 9, 20, 3.0)
    for i in range(3):
        stall(top, -21 + i * 0.0, -6 - i * 5, 6.5, 4.0, 2.4, roof=REED, goods=GRAIN)
    for i, (hx, hy) in enumerate(((-12, -16), (-7, -18), (8, -17), (13, -16))):
        hut(top, hx, hy, 1.7, STRAW, "N")
    for i, (ax, ay, deg) in enumerate(((-14, -6, 20), (-12, -10, 200), (-8, -4, 90))):
        animal(top, "horse", ax, ay, deg, load="saddle" if i == 0 else None)
    acacia(top, 4, -6, 3.0, 4.6)
    pot(top, 2, -3, 0.45, 0.9)
    m.add(0, g.build(), "ground")
    m.add(1, walls.build(), "walls")
    m.add(2, house.build(), "palace")
    m.add(3, top.build(), "court")
    return m


def kasbah():
    m = Model("kasbah")
    g = Parts("kb_ground")
    g.cube(SAND, 0, 0, 0, 130, 110, 0.25)
    g.cube(SAND_DK, 5, 0, 0, 110, 92, 0.3)
    walls, inside, top = Parts("kb_walls"), Parts("kb_inside"), Parts("kb_top")
    wh, wt = 6.0, 2.2
    for (cx, cy, w, d, f) in ((0, -50.9, 118, wt, "S"), (0, 50.9, 118, wt, "N"), (-60.9, 0, wt, 99.6, "W"), (60.9, 0, wt, 99.6, "E")):
        sahel_block(walls, cx, cy, w, d, wh, faces=f, every=4.0, toron=(0.5,), toron_on="pilaster", pil=1.0, out=0.55, spike_h=1.2)
    # square towers at the corners and along the walls
    for tx in (-60, 60):
        for ty in (-50, 50):
            sahel_block(walls, tx, ty, 8, 8, 8.8, faces="NSEW", every=2.6, toron=(0.35, 0.7), pil=0.8)
    for (tx, ty) in ((-20, -50.5), (20, -50.5), (-20, 50.5), (20, 50.5), (-60.5, -17), (-60.5, 17), (60.5, -26), (60.5, 26)):
        sahel_block(walls, tx, ty, 6, 6, 7.8, faces="NSEW", every=3.0, toron=(0.45,), pil=0.8)
    # the gate toward the Kabara road (east)
    sahel_block(walls, 59.5, 0, 9, 13, 9.2, faces="NSEW", every=2.6, toron=(0.35, 0.65, 0.88), pil=0.9)
    carved_door(walls, 64.0, 0, 3.0, 4.2, "E")
    for gy in (-6.8, 6.8):
        cone_tower(walls, 63.2, gy, 1.5, 9.6, levels=3, sticks=5)
    # the pasha's house, two storeys with Moroccan windows
    sahel_block(inside, -32, 22, 34, 22, 5.0, faces="NSEW", every=2.8, toron=(0.42, 0.8), pil=0.85)
    sahel_block(inside, -34, 24, 22, 14, 4.0, z0=5.0, faces="SEW", every=2.8, toron=(0.5,), pil=0.75, out=0.4)
    carved_door(inside, -32, 11, 2.2, 3.2, "S")
    for k in (-2, -1, 1, 2):
        moroccan_window(inside, -34 + k * 4.4, 17, 6.3, "S")
    spouts(inside, -32, 22, 34, 22, 4.5, "S", 6)
    roof_vents(top, -48, -16, 12, 32, 5.0, 4.5)
    # barracks of the Arma
    for i in range(3):
        plain_block(inside, -20, -40 + i * 11, 52, 6, 3.4, spikes=0.6)
        for k in range(7):
            fbox(inside, DARK, -42 + k * 7.3, -40 + i * 11 + 3, 0, 1.0, 0.2, 2.0, "N", 0.0)
    # a small mosque with a square minaret
    sahel_block(inside, 30, 32, 22, 16, 4.6, faces="NSEW", every=2.8, toron=(0.45, 0.8), pil=0.8)
    square_tower(top, 37, 38, 4.6, 2.8, 10.5, rows=4, cols=2)
    roof_vents(top, 20, 40, 25, 39, 4.6, 4.0)
    # stores and a powder magazine
    for i in range(3):
        plain_block(inside, 40, -30 + i * 10, 12, 8, 3.6, spikes=0.7)
        carved_door(inside, 34, -30 + i * 10, 1.3, 2.2, "W", studs=False)
    # parade yard: a well, cannon, horses
    pot(top, 8, 4, 0.5, 0.9, BANCO_DK)
    top.cone(BANCO, 8, 0, 0, 1.2, 1.15, 0.8, 10)
    top.cube(DARK, 8, 0, 0.8, 1.2, 1.2, 0.02)
    for (cx, cy) in ((48, -8), (48, 8)):
        top.beam(BASALT, (cx - 1.8, cy, 0.7), (cx + 1.6, cy, 0.85), 0.42)
        top.cube(TIMBER, cx - 1.0, cy, 0, 2.2, 1.2, 0.5)
    for i, (ax, ay, deg) in enumerate(((10, -14, 30), (14, -18, 200), (2, -18, 90))):
        animal(top, "horse", ax, ay, deg, load="saddle")
    for (ax, ay) in ((-6, 6), (20, 14), (-50, -12)):
        acacia(top, ax, ay, 2.8, 4.4)
    m.add(0, g.build(), "ground")
    m.add(1, walls.build(), "walls")
    m.add(2, inside.build(), "buildings")
    m.add(3, top.build(), "towers")
    return m


# ---------------------------------------------------------------- trade

def great_market():
    m = Model("great-market")
    g = Parts("mk_ground")
    g.cube(SAND, 0, 0, 0, 90, 70, 0.25)
    g.cube(SAND_DK, 0, -3, 0, 70, 52, 0.3)
    shops, stalls, goods = Parts("mk_shops"), Parts("mk_stalls"), Parts("mk_goods")
    r = rnd(7)
    # banco shops and houses round the north and west edges, one door each onto the square
    x = -44.0
    while x < 42:
        w = 5 + next(r) * 4
        h = 3.2 + next(r) * 2.4
        plain_block(shops, x + w / 2, 30.5, w - 0.2, 8, h, color=shade(BANCO, (next(r) - 0.5) * 0.08), spikes=0.6 if next(r) > 0.5 else 0)
        carved_door(shops, x + w / 2, 26.5, 1.1, 2.0, "S", studs=False)
        x += w
    y = -34.0
    while y < 26:
        d = 5 + next(r) * 4
        h = 3.2 + next(r) * 2.0
        plain_block(shops, -40.5, y + d / 2, 8, d - 0.2, h, color=shade(BANCO, (next(r) - 0.5) * 0.08))
        carved_door(shops, -36.5, y + d / 2, 1.1, 2.0, "E", studs=False)
        y += d
    for (cx, cy, w, d) in ((40, 12, 9, 22), (40, -18, 9, 26)):
        sahel_block(shops, cx, cy, w, d, 4.6, faces="W", every=3.0, toron=(0.55,), pil=0.7)
        carved_door(shops, cx - w / 2, cy, 1.2, 2.2, "W")
    # rows of mat-roofed stalls on poles
    goods_cols = [GRAIN, "#8A6A3E", CLOTH, "#B04A32", "#5C7A3A", "#D9C27A", POT]
    for i in range(6):
        for j in range(4):
            sx, sy = -26 + i * 10.0, -20 + j * 10.5
            if (i, j) in ((4, 0), (5, 0), (5, 1)):
                continue
            stall(stalls, sx, sy, 4.4, 3.2, 2.2 + next(r) * 0.3, roof=shade(MAT, (next(r) - 0.5) * 0.12), goods=goods_cols[(i + j) % len(goods_cols)])
    # salt slabs, sacks and pots; a well
    for (sx, sy, al) in ((18, -23, True), (21, -23, False), (24, -21, True), (27, -16, False), (24, -14, True)):
        salt_stack(goods, sx, sy, 5 + int(next(r) * 4), 2, al)
    for (sx, sy) in ((-30, 22), (-16, 22), (6, 22), (-32, -28)):
        sacks(goods, sx, sy, 5)
    for k in range(8):
        pot(goods, -22 + k * 1.1, -27.5, 0.34, 0.65)
    goods.cone(BANCO, 30, 5, 0, 1.2, 1.15, 0.8, 10)
    goods.cube(DARK, 30, 5, 0.8, 1.3, 1.3, 0.02)
    goods.cube(BANCO_DK, 30, 7.6, 0, 2.6, 0.7, 0.5)
    for (ax, ay) in ((32, 18), (-4, -31)):
        acacia(goods, ax, ay, 3.0, 4.4)
    for (ax, ay, deg) in ((14, -30, 10), (12, -32, 190), (34, -5, 90)):
        animal(goods, "donkey", ax, ay, deg, load="sacks")
    animal(goods, "camel", 24, -30, 180, kneel=True, load="salt")
    m.add(0, g.build(), "ground")
    m.add(1, shops.build(), "shops")
    m.add(2, stalls.build(), "stalls")
    m.add(3, goods.build(), "goods")
    return m


def azalai_ground():
    m = Model("azalai-ground")
    g = Parts("az_ground")
    g.cube(SAND, 0, 0, 0, 80, 60, 0.25)
    g.cone(SAND_DK, -22, 20, 0.25, 9, 4, 0.9, 10)
    stores, camp, beasts = Parts("az_stores"), Parts("az_camp"), Parts("az_beasts")
    r = rnd(11)
    # salt stores of the merchants on the town side (south) and a walled salt yard
    for i in range(3):
        cx = -32 + i * 11.5
        plain_block(stores, cx, -25, 10.5, 8, 3.4 + (i % 2) * 0.8, spikes=0.6)
        carved_door(stores, cx, -21, 1.3, 2.2, "N", studs=i % 2 == 0)
        sudan_window(stores, cx + 3, -21, 1.6, "N", 0.5, 0.6)
    for (cx, cy, w, d, f) in ((22, -28.5, 30, 0.9, "S"), (7.5, -19, 0.9, 19, "W"), (36.5, -19, 0.9, 19, "E")):
        sahel_block(stores, cx, cy, w, d, 2.4, faces=f, every=3.0, toron=(0.6,), toron_on="pilaster", pil=0.6, out=0.35, spike_h=0.6)
    for k in range(9):
        salt_stack(stores, 13 + (k % 3) * 7, -24 + (k // 3) * 5, 6 + (k % 4), 2, k % 2 == 0)
    # the caravan men's tents and a stone well with its trough
    for (tx, ty) in ((-32, 22), (-20, 25), (24, 24), (34, 19)):
        tent(camp, tx, ty, 5.4, 3.8)
    camp.cone(ALHOR, 0, 18, 0, 1.4, 1.3, 0.9, 12)
    camp.cube(DARK, 0, 18, 0.9, 1.4, 1.4, 0.02)
    camp.cube(BANCO_DK, 3.2, 18, 0, 3.0, 0.8, 0.45)
    camp.cube(WATER_C, 3.2, 18, 0.45, 2.6, 0.5, 0.02)
    for bx in (-1.4, 1.4):
        camp.beam(TORON, (bx, 18, 0), (bx * 0.85, 18, 2.4), 0.14)
    camp.beam(TORON, (-1.4, 18, 2.35), (1.4, 18, 2.35), 0.12)
    for (ax, ay) in ((-37, 4), (37, 2), (8, 26)):
        acacia(camp, ax, ay, 2.6, 3.8)
    for k in range(6):
        camp.cube(LEATHER_DK, -8 + k * 1.6, 24, 0, 1.0, 0.7, 0.55)
        camp.cube(CLOTH if k % 2 else LEATHER, -8 + k * 1.6, 24, 0.55, 0.8, 0.5, 0.3)
    # the Azalai: camels kneeling in lines beside their unloaded slabs, a few still loaded
    for row in range(4):
        for k in range(9):
            ax = -33 + k * 6.6 + next(r) * 1.4 + (row % 2) * 2.0
            ay = 10 - row * 6.0 + next(r) * 1.2
            if -4 < ax < 7 and row == 0:
                continue
            if ax > 6 and row == 3:
                continue
            kneel = next(r) > 0.2
            animal(beasts, "camel", ax, ay, 80 + next(r) * 25, kneel=kneel, load="salt" if (not kneel or next(r) > 0.6) else "saddle")
            if kneel and next(r) > 0.3:
                salt_stack(beasts, ax + 0.2, ay - 1.7, 2 + int(next(r) * 3), 2, True)
    m.add(0, g.build(), "ground")
    m.add(1, stores.build(), "stores")
    m.add(2, camp.build(), "camp")
    m.add(3, beasts.build(), "caravan")
    return m


def kabara_landing():
    m = Model("kabara-landing")
    g = Parts("kl_ground")
    g.cube(SAND, 0, 0, 0, 70, 50, 0.25)
    g.cube(SAND_WET, -28, 0, 0, 14, 50, 0.28)
    boats, huts, loads = Parts("kl_boats"), Parts("kl_huts"), Parts("kl_loads")
    for i, (bx, by, deg, L, can) in enumerate(((-29, -18, 95, 10, True), (-31, -6, 80, 8.5, False), (-28, 6, 100, 11, True), (-31, 17, 85, 8, False), (-24, 21, 60, 7, False))):
        pirogue(boats, bx, by, deg, L, 1.3 if L > 9 else 1.1, 0.6, can)
    for (px, py) in ((-25, -12), (-25, 0), (-25, 12)):
        boats.beam(TIMBER, (px, py, 0), (px - 0.2, py, 2.0), 0.14)
    # poles and paddles leaning on the posts, fish drying on racks
    for k in range(6):
        boats.beam(TIMBER, (-24.6, -13 + k * 5, 0), (-25.6, -12.5 + k * 5, 3.2), 0.07)
    for (rx, ry) in ((-20, -22), (-20, 18)):
        for dx in (-2, 2):
            boats.beam(TIMBER, (rx + dx, ry, 0), (rx + dx, ry, 1.5), 0.1)
        boats.beam(TIMBER, (rx - 2.2, ry, 1.5), (rx + 2.2, ry, 1.5), 0.08)
        for k in range(9):
            boats.cube("#8E8A80", rx - 1.8 + k * 0.45, ry, 0.95, 0.12, 0.25, 0.5)
    for (hx, hy, r) in ((-6, 16, 2.2), (0, 20, 2.0), (8, 17, 2.4), (16, 20, 2.0), (22, 14, 2.2), (2, 8, 1.9), (18, 4, 2.1), (26, -4, 2.0)):
        hut(huts, hx, hy, r, shade(STRAW, (hx % 3 - 1) * 0.05), "S")
    stall(huts, -12, -2, 6.0, 4.0, 2.2, roof=REED, goods=GRAIN)
    # a reed fence round the boatmen's huts
    for k in range(40):
        fx = -10 + k * 0.9
        huts.beam(REED, (fx, 24.0, 0), (fx + 0.1, 24.0, 1.6), 0.12)
    for (hx, hy, r) in ((-2, 13, 1.6), (12, 22, 1.7), (28, 8, 1.9), (24, -12, 1.8)):
        hut(huts, hx, hy, r, STRAW, "W")
    stall(huts, 10, -14, 5.0, 3.6, 2.0, roof=REED, goods="#8A6A3E")
    for (sx, sy) in ((-18, -8), (-18, 4), (-14, 9), (-4, -14)):
        sacks(loads, sx, sy, 6)
    for k in range(10):
        pot(loads, -8 + (k % 5) * 0.9, -20 + (k // 5) * 0.9, 0.36, 0.7)
    for (ax, ay, deg, ld) in ((-2, -6, 0, "sacks"), (1, -8, 10, "sacks"), (4, -10, 20, None), (8, -6, 180, "sacks"), (12, -4, 200, None), (6, 2, 90, "sacks")):
        animal(loads, "donkey", ax, ay, deg, load=ld)
    for (ax, ay) in ((28, 20), (30, -18)):
        acacia(loads, ax, ay, 2.6, 3.8)
    for k in range(5):
        salt_stack(loads, -16 + k * 1.4, -16, 4, 1, False)
    loads.cube(TIMBER, -14, 14, 0, 4.0, 0.5, 0.4)
    loads.cube(TIMBER, -14, 14.6, 0, 4.0, 0.5, 0.4)
    loads.cube(TIMBER, -14, 14.3, 0.4, 4.0, 0.5, 0.4)
    m.add(0, g.build(), "ground")
    m.add(1, boats.build(), "boats")
    m.add(2, huts.build(), "huts")
    m.add(3, loads.build(), "loads")
    return m


# ---------------------------------------------------------------- houses

def town_house(name, w, d, moroccan=False, tree=False, library=False):
    """A two-storey banco courtyard house: pilastered facade to the south, carved door, roof terraces."""
    m = Model(name)
    g = Parts(name + "_g")
    g.cube(SAND, 0, 0, 0, w, d, 0.25)
    low, up, det = Parts(name + "_low"), Parts(name + "_up"), Parts(name + "_det")
    h1, h2 = 3.6, 3.2
    fd = 7.0
    # ground floor: front range with the vestibule, side ranges of stores, rear range; a court in the middle
    sahel_block(low, 0, -d / 2 + fd / 2, w, fd, h1, faces="SEW", every=2.4, toron=(), pil=0.7, out=0.4, spikes=False, para=0.3)
    plain_block(low, -w / 2 + 2.2, 1.0, 4.4, d - fd - 5.0 - 2.0 + 2.0, h1, para=0.4)
    plain_block(low, w / 2 - 2.2, 1.0, 4.4, d - fd - 5.0 - 2.0 + 2.0, h1, para=0.4)
    plain_block(low, 0, d / 2 - 2.5, w, 5.0, h1, para=0.5)
    g.cube(SAND_DK, 0, -d / 2 + fd + (d - fd - 5) / 2, 0, w - 8.8, d - fd - 5, 0.32)
    carved_door(low, 0, -d / 2, 1.5, 2.5, "S")
    for k in (-1, 1):
        sudan_window(low, k * w * 0.3, -d / 2, 1.4, "S", 0.5, 0.6)
    crest_spikes(low, -w / 2 + 2.2, 1.0, 4.4, d - fd - 5.0, h1 + 0.4, 1.5, faces="W")
    crest_spikes(low, w / 2 - 2.2, 1.0, 4.4, d - fd - 5.0, h1 + 0.4, 1.5, faces="E")
    crest_spikes(low, 0, d / 2 - 2.5, w, 5.0, h1 + 0.5, 1.5, faces="NEW")
    # a frieze of small niches under the parapet and a moulded band over the door
    for i in range(int(w / 1.2)):
        fbox(low, DARK, -w / 2 + 0.9 + i * 1.2, -d / 2, h1 - 0.7, 0.35, 0.1, 0.45, "S", 0.03)
    fbox(low, BANCO_LT, 0, -d / 2, 2.95, 3.6, 0.35, 0.25, "S", 0.15)
    for k in (-1, 1):
        cone_tower(low, k * (w / 2 - 0.3), -d / 2 + 0.3, 0.7, h1 + 1.4, BANCO, levels=0, sticks=0, egg=False, n=8)
    court_y = -d / 2 + fd
    arcs = [arcade(name + "_carc", w - 10, 2.6, 4, (0, court_y + 0.02, 0), "N", DARK, False, 0.6, 0.3)]
    # upper storey over the front range (the master's rooms; in a scholar's house the library)
    sahel_block(up, 0, -d / 2 + fd / 2 - 0.0, w - 2.0, fd - 1.0, h2, z0=h1, faces="SEW", every=2.4, toron=(), pil=0.65, out=0.35, spike_h=0.9)
    crest_spikes(up, 0, -d / 2 + fd / 2, w - 2.0, fd - 1.0, h1 + h2 + 0.55, 1.2, faces="N", h=0.6)
    for i in range(int((w - 2) / 1.2)):
        fbox(up, DARK, -w / 2 + 1.8 + i * 1.2, -d / 2 + 0.5, h1 + h2 - 0.65, 0.3, 0.1, 0.4, "S", 0.03)
    if moroccan:
        for k in (-1, 1):
            moroccan_window(up, k * w * 0.22, -d / 2 + 0.5, h1 + 0.8, "S")
    else:
        for k in (-1, 0, 1):
            sudan_window(up, k * w * 0.24, -d / 2 + 0.5, h1 + 1.2, "S")
    # a small upper room on the rear range, with its stair
    plain_block(up, w / 2 - 4.5, d / 2 - 2.5, 7, 4.4, 2.8, z0=h1, para=0.5, spikes=0.6)
    det.beam(BANCO_DK, (-w / 2 + 5.0, d / 2 - 6.0, 0.3), (-w / 2 + 5.0, d / 2 - 5.0 + 0.5, h1), 1.2, 0.3)
    spouts(det, 0, -d / 2 + fd / 2, w - 2.0, fd - 1.0, h1 + h2 - 0.5, "S", 3)
    spouts(det, 0, 0, w, d, h1 - 0.4, "E", 2)
    spouts(det, 0, 0, w, d, h1 - 0.4, "W", 2)
    if tree:
        acacia(det, 2.0, -d / 2 + fd + 3.5, 1.8, 3.0)
    # in the court: a mortar for pounding millet, a mat, a water jar on a stand, a goat
    det.cone(TIMBER, -3.0, court_y + 2.5, 0.3, 0.35, 0.3, 0.7, 8)
    det.beam(TIMBER, (-3.0, court_y + 2.5, 0.9), (-2.9, court_y + 2.6, 2.1), 0.1)
    det.cube(MAT, 4.0, court_y + 4.5, 0.32, 2.2, 1.5, 0.04)
    for k in range(4):
        det.beam(TIMBER, (5.5 + (k % 2) * 0.6, court_y + 1.2 + (k // 2) * 0.6, 0.3), (5.8, court_y + 1.5, 1.0), 0.06)
    pot(det, 5.8, court_y + 1.5, 0.35, 0.7)
    animal(det, "goat", -1.0, court_y + 5.5, 30)
    for k in range(3):
        pot(det, -w / 2 + 6.0 + k * 0.9, d / 2 - 6.0, 0.3, 0.7)
    if library:
        # book chests on the roof terrace being aired, and a reading mat
        for k in range(5):
            det.cube(LEATHER if k % 2 else LEATHER_DK, -w / 2 + 3 + k * 1.3, d / 2 - 2.5, h1 + 0.5, 1.0, 0.6, 0.55)
            for j in range(3):
                det.cube(shade(LEATHER, 0.1 * j), -w / 2 + 3 + k * 1.3, d / 2 - 2.5, h1 + 1.05 + j * 0.08, 0.7, 0.45, 0.07)
        det.cube(MAT, 3.0, d / 2 - 2.5, h1 + 0.5, 2.4, 1.6, 0.04)
    else:
        sacks(det, -w / 2 + 6.5, -d / 2 + fd + 1.0, 4, GRAIN)
        salt_stack(det, w / 2 - 6.5, -d / 2 + fd + 1.5, 4, 1, True)
    m.add(0, g.build(), "ground")
    m.add(1, low.build(), "ground floor")
    m.add(1, join(arcs, name + "_arcs"))
    m.add(2, join([up.build(), det.build()], name + "_top"), "upper storey")
    return m


def merchant_house():
    return town_house("merchant-house", 24, 22, moroccan=True)


def aqit_house():
    return town_house("aqit-house", 26, 22, moroccan=False, tree=True, library=True)


# ---------------------------------------------------------------- saints, the well, the camp

def mausoleum(P, x, y, w, h, dome_r=0.0, color=BANCO_LT, door="S"):
    """A saint's tomb: a cube of banco with corner pinnacles, sometimes a low dome."""
    P.frustum(color, x, y, 0, w + 0.3, w + 0.3, w, w, h)
    parapet(P, x, y, h, w, w, shade(color, -0.04), 0.25, 0.45)
    for sx in (-1, 1):
        for sy in (-1, 1):
            P.cone(color, x + sx * (w / 2 - 0.15), y + sy * (w / 2 - 0.15), h + 0.45, 0.32, 0.04, 1.0, 6)
    if dome_r:
        P.dome(color, x, y, h, dome_r, 0.75, 12, 4)
        P.dome(EGG, x, y, h + dome_r * 0.72, 0.22, 1.4, 8, 3)
    nx, ny = FACES[door]
    fbox(P, DOOR, x + nx * w / 2, y + ny * w / 2, 0, 0.8, 0.2, 1.5, door, 0.1)


def saints_cemetery():
    m = Model("saints-cemetery")
    g = Parts("sc_ground")
    g.cube(SAND, 0, 0, 0, 80, 70, 0.25)
    walls, tombs = Parts("sc_walls"), Parts("sc_tombs")
    for (cx, cy, w, d, f) in ((-22, -34.4, 34, 0.8, "S"), (22, -34.4, 34, 0.8, "S"), (0, 34.4, 78, 0.8, "N"), (-39.4, 0, 0.8, 68, "W"), (39.4, 0, 0.8, 68, "E")):
        sahel_block(walls, cx, cy, w, d, 1.5, faces=f, every=4.0, toron=(), pil=0.5, out=0.3, spike_h=0.6, para=0.3)
    graves(g, -34, -6, -28, 28, 40, 7)
    graves(g, 6, 34, -28, -2, 26, 13)
    graves(g, 10, 34, 12, 30, 16, 17)
    # Sidi Mahmud's tomb on a stepped base, and smaller mausolea of the saints
    tombs.cube(BANCO_DK, 0, 4, 0, 11, 11, 0.5)
    tombs.cube(BANCO_DK, 0, 4, 0.5, 9.5, 9.5, 0.4)
    mausoleum(tombs, 0, 4, 6.5, 3.8, 2.6)
    tombs.cube(MAT, 0, -2.8, 0, 5, 3, 0.04)
    for (mx, my, w, dr) in ((-14, 18, 3.6, 0), (16, 22, 4.0, 1.5), (20, 4, 3.4, 0), (-20, -18, 3.8, 1.4), (14, -16, 3.2, 0), (-26, 6, 3.0, 0)):
        mausoleum(tombs, mx, my, w, 2.6 + w * 0.15, dr)
    for (ax, ay) in ((-30, 26), (30, -26), (-6, -26), (28, 30)):
        acacia(tombs, ax, ay, 2.6, 3.8)
    for k in range(6):
        pot(tombs, -4 + k * 1.6, -5.0, 0.25, 0.5)
    m.add(0, g.build(), "ground")
    m.add(1, walls.build(), "walls")
    m.add(2, tombs.build(), "tombs")
    return m


def well_of_buktu():
    m = Model("well-of-buktu")
    g = Parts("wb_ground")
    g.cube(SAND, 0, 0, 0, 12, 12, 0.2)
    for ring, (rr, n) in enumerate(((1.95, 14), (2.85, 20))):
        for k in range(n):
            a = math.tau * (k + 0.5 * ring) / n
            g.cube(shade(ALHOR, -0.05 * ((k + ring) % 3)), rr * math.cos(a), rr * math.sin(a), 0, 0.85, 0.85, 0.26 - 0.06 * ring)
    well, frame = Parts("wb_well"), Parts("wb_frame")
    well.cone(BANCO, 0, 0, 0, 1.25, 1.15, 0.85, 20)
    well.cone(BANCO_LT, 0, 0, 0.85, 1.2, 1.2, 0.12, 20)
    well.cone(DARK, 0, 0, 0.97, 0.78, 0.78, 0.02, 20)
    for k in range(10):
        a = math.tau * k / 10
        well.cube(ALHOR, 1.22 * math.cos(a), 1.22 * math.sin(a), 0.25, 0.4, 0.4, 0.25)
    # a low banco bench round the north side and a shade of mats on poles
    for k in range(9):
        a = math.pi * (0.15 + 0.7 * k / 8)
        well.cube(BANCO_DK, 4.6 * math.cos(a), 4.6 * math.sin(a), 0, 0.9, 0.9, 0.45)
    stall(well, -3.6, -3.6, 2.6, 2.2, 1.9, roof=REED, goods=GRAIN)
    # trough for the animals, jars and the leather bucket
    well.cube(BANCO_DK, 2.9, -1.6, 0, 2.6, 0.9, 0.5)
    well.cube(WATER_C, 2.9, -1.6, 0.5, 2.3, 0.6, 0.02)
    for k, (px, py) in enumerate(((-2.4, -2.2), (-2.9, -1.5), (-2.2, 2.6), (2.6, 2.4))):
        pot(well, px, py, 0.3 + 0.05 * (k % 2), 0.65 + 0.1 * (k % 2))
    # forked posts, cross-beam and pulley
    for s in (-1, 1):
        frame.beam(TIMBER, (s * 1.6, 0, 0), (s * 1.35, 0, 2.6), 0.2)
        frame.beam(TIMBER, (s * 1.35, 0, 2.5), (s * 1.6, 0, 3.0), 0.12)
        frame.beam(TIMBER, (s * 1.35, 0, 2.5), (s * 1.1, 0, 3.0), 0.12)
    frame.beam(TIMBER, (-1.75, 0, 2.75), (1.75, 0, 2.75), 0.16)
    frame.cone(TIMBER, 0, 0, 2.58, 0.25, 0.25, 0.08, 8)
    frame.beam("#CBB98F", (0.2, 0, 2.7), (0.2, 0, 1.5), 0.04)
    frame.cone(LEATHER, 0.2, 0, 1.15, 0.18, 0.25, 0.35, 8)
    acacia(frame, -4.0, 3.6, 2.2, 3.6)
    hut(frame, 4.6, -0.2, 1.1, STRAW, "W")
    for k in range(3):
        frame.beam(LEATHER_DK, (-1.2 + k * 0.5, -4.8, 0.05), (-1.0 + k * 0.5, -5.4, 0.05), 0.3, 0.1)
    animal(frame, "goat", 3.5, -3.6, 160)
    animal(frame, "donkey", 1.2, -4.6, 15, load="sacks")
    animal(frame, "goat", 4.4, -2.7, 200)
    animal(frame, "camel", 3.0, 3.4, -20, kneel=True)
    m.add(0, g.build(), "ground")
    m.add(1, well.build(), "well")
    m.add(2, frame.build(), "frame")
    return m


def tuareg_camp():
    m = Model("tuareg-camp")
    g = Parts("tc_ground")
    g.cube(SAND, 0, 0, 0, 80, 60, 0.25)
    for (dx, dy, rr) in ((-30, 21, 8), (31, -21, 9)):
        g.cone(SAND_DK, dx, dy, 0.25, rr, rr * 0.45, 1.2, 12)
    shelters, life = Parts("tc_tents"), Parts("tc_life")
    r = rnd(23)
    for (tx, ty, w, d) in ((-24, -5, 5.6, 3.8), (-16, 4, 5.0, 3.6), (-8, -10, 6.0, 4.0), (-2, 8, 5.2, 3.6), (8, -3, 5.6, 4.0), (17, 6, 5.0, 3.4),
                           (24, -9, 5.6, 3.8), (10, 17, 5.0, 3.6)):
        tent(shelters, tx, ty, w, d, 1.6 + next(r) * 0.3, shade(LEATHER, (next(r) - 0.5) * 0.12))
    for (hx, hy) in ((-30, 7), (-21, 15), (-6, 19), (22, 18), (31, 3), (-14, -21), (3, -19), (-33, -6)):
        hut(shelters, hx, hy, 1.9 + next(r) * 0.5, shade(STRAW, (next(r) - 0.5) * 0.1), "S")
    for (px, py, rr) in ((-31, -19, 5), (18, -21, 5.5), (32, 19, 4.5)):
        thorn_pen(life, px, py, rr)
        for k in range(6):
            animal(life, "goat", px + (next(r) - 0.5) * rr, py + (next(r) - 0.5) * rr, next(r) * 360)
    for k in range(10):
        cx, cy = -34 + k * 7.4 + next(r) * 2, -27 + (k % 3) * 3 + next(r) * 1.5
        if k in (4, 5, 6):
            cy = 25 + next(r) * 2
        animal(life, "camel", cx, cy, next(r) * 360, kneel=next(r) > 0.4, load=None if next(r) > 0.5 else "saddle")
    for (fx, fy) in ((-12, -2), (12, 2)):
        life.cone(BASALT, fx, fy, 0, 0.7, 0.6, 0.2, 8)
        life.cone(FIRE, fx, fy, 0.2, 0.4, 0.04, 0.6, 6)
        pot(life, fx + 1.2, fy, 0.35, 0.6, "#3A332C")
        life.cube(MAT, fx - 1.6, fy + 0.8, 0, 2.0, 1.4, 0.04)
    for (ax, ay) in ((-37, 26), (-36, -14), (37, -6), (0, 27), (-20, -26), (37, 27), (8, -27)):
        acacia(life, ax, ay, 2.4 + next(r), 3.6 + next(r))
    for k in range(6):
        life.cube(GRAIN, -4 + k * 1.1, 1, 0, 0.8, 0.6, 0.5)
    for k in range(4):
        salt_stack(life, 2 + k * 1.5, 1.5, 3, 1, False)
    m.add(0, g.build(), "ground")
    m.add(1, shelters.build(), "tents")
    m.add(2, life.build(), "herds")
    return m


BUILDERS = {
    "timbuktu/djinguereber": djinguereber,
    "timbuktu/djinguereber-1340": lambda: djinguereber("1340"),
    "timbuktu/djinguereber-1700": lambda: djinguereber("1700"),
    "timbuktu/sankore": sankore,
    "timbuktu/sankore-1700": lambda: sankore("1700"),
    "timbuktu/sidi-yahya": sidi_yahya,
    "timbuktu/madugu": madugu,
    "timbuktu/kasbah": kasbah,
    "timbuktu/great-market": great_market,
    "timbuktu/azalai-ground": azalai_ground,
    "timbuktu/kabara-landing": kabara_landing,
    "timbuktu/merchant-house": merchant_house,
    "timbuktu/aqit-house": aqit_house,
    "timbuktu/saints-cemetery": saints_cemetery,
    "timbuktu/well-of-buktu": well_of_buktu,
    "timbuktu/tuareg-camp": tuareg_camp,
}
