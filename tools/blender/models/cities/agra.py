"""Agra landmark miniatures: the Taj, the fort and the riverfront gardens of Mughal Agra.

Built on the real orientation (+Y north): the Taj's facade faces south toward its garden,
the fort's flat side runs along the river on the east, the east-bank gardens face the river
on the west, so every landmark is placed with rotation 0.
"""
import math
import random
import bpy
from chronokit import Model, box, cylinder, dome, join, shade, mesh_from, ring_extrude
from worldkit import *

RED = RED_SANDSTONE
RED_DK = shade(RED_SANDSTONE, -0.18)
RED_LT = shade(RED_SANDSTONE, 0.22)
RED_RECESS = "#5C2E22"
WHITE = MARBLE
WHITE_LINE = shade(MARBLE, -0.10)
NICHE = "#8E8577"          # shaded recess in white marble
CALLIG = "#3B3936"         # black marble inlay bands
PAVE = shade(RED_SANDSTONE, 0.32)
GROUND = "#D6C29A"
LAWN = "#7F9C6A"
LAWN_WILD = "#6B7F4C"
DRY = "#A8956F"
PLASTER_W = "#E8DECB"
INLAY = "#E5D2B2"
BRICK_FORT = "#A9664A"


# ---------------------------------------------------------------- transforms and small parts

def _apply_loc(o):
    L = o.location.copy()
    if L.length > 0:
        for v in o.data.vertices:
            v.co += L
        o.location = (0, 0, 0)
    return o


def rz(o, deg, px=0.0, py=0.0):
    """Rotate an object's mesh about the vertical axis through (px, py), counter-clockwise."""
    _apply_loc(o)
    a = math.radians(deg)
    c, s = math.cos(a), math.sin(a)
    for v in o.data.vertices:
        x, y = v.co.x - px, v.co.y - py
        v.co.x, v.co.y = px + x * c - y * s, py + x * s + y * c
    o.data.update()
    return o


def mv(o, x=0.0, y=0.0, z=0.0):
    _apply_loc(o)
    for v in o.data.vertices:
        v.co.x += x
        v.co.y += y
        v.co.z += z
    o.data.update()
    return o


FACE = {"S": 0, "E": 90, "N": 180, "W": -90}


def oct_pts(r, n=8):
    return [(r * math.cos(math.pi / n + k * math.tau / n), r * math.sin(math.pi / n + k * math.tau / n)) for k in range(n)]


def chamfer_pts(S, c):
    s = S / 2
    return [(-s + c, -s), (s - c, -s), (s, -s + c), (s, s - c), (s - c, s), (-s + c, s), (-s, s - c), (-s, -s + c)]


def niche(name, w, h, x, y, z, ang, dist=0.0, color=DARK, pointed=True, depth=0.35):
    """An arched recess on a wall whose outward normal is the south direction turned by ang; dist = wall offset from (x, y)."""
    o = arch_panel(name, w, h, (0, -dist, z), "S", color, pointed, depth)
    rz(o, ang)
    return mv(o, x, y, 0)


def kalash(name, s, loc, color=GILT):
    x, y, z = loc
    prof = [(0.0, 0), (0.22 * s, 0.03 * s), (0.3 * s, 0.14 * s), (0.12 * s, 0.28 * s), (0.26 * s, 0.38 * s), (0.28 * s, 0.47 * s), (0.1 * s, 0.58 * s),
            (0.17 * s, 0.66 * s), (0.04 * s, 0.82 * s), (0.0, s)]
    return lathe(name, prof, (x, y, z), color, verts=10)


def flight(name, w, rise, run, n, x, y, ang=0, color=PAVE):
    """A flight of steps rising toward the building; built rising toward +y, turned by ang (0 = building to the north)."""
    parts = []
    for i in range(n):
        d = run * (n - i) / n
        parts.append(box(f"{name}{i}", w, d, rise / n, (0, run - d / 2, rise * i / n), color))
    o = join(parts, name)
    rz(o, ang)
    return mv(o, x, y, 0)


def pishtaq(name, w, h, x, y, z, ang, dist=0.0, color=WHITE, border=None, recess=NICHE, door=DARK, depth=1.2, guldasta=True, callig=None):
    """A tall rectangular portal frame round a pointed arch (the pishtaq), with corner pinnacles; faces south turned by ang."""
    b = border or shade(color, -0.1)
    parts = [box(name + "_f", w, depth, h, (0, -dist - depth / 2, z), color)]
    aw, ah = w * 0.62, h * 0.78
    band = callig or b
    parts.append(box(name + "_bt", aw + w * 0.14, 0.25, h * 0.035, (0, -dist - depth - 0.1, z + ah + h * 0.05), band))
    for s in (-1, 1):
        parts.append(box(f"{name}_bs{s}", w * 0.035, 0.25, ah + h * 0.085, (s * (aw / 2 + w * 0.055), -dist - depth - 0.1, z), band))
    parts.append(box(name + "_top", w + 0.4, depth + 0.4, h * 0.03, (0, -dist - depth / 2, z + h - h * 0.03), b))
    parts.append(arch_panel(name + "_a", aw, ah, (0, -dist - depth - 0.05, z), "S", recess, True, 0.4))
    parts.append(arch_panel(name + "_d", aw * 0.42, ah * 0.4, (0, -dist - depth - 0.3, z), "S", door, True, 0.4))
    if guldasta:
        for s in (-1, 1):
            gx = s * (w / 2 - w * 0.02)
            parts.append(cylinder(f"{name}_g{s}", w * 0.03, h * 1.1, (gx, -dist - depth / 2, z), color, verts=8))
            parts.append(onion_dome(f"{name}_gd{s}", w * 0.04, (gx, -dist - depth / 2, z + h * 1.1), color, height=1.4, drum=0.2, finial=False))
    o = join(parts, name)
    rz(o, ang)
    return mv(o, x, y, 0)


def oct_tower(name, r, h, x, y, z=0.0, color=RED, cap=WHITE, storeys=2, chhatri_cap=True, niches=True, dome_cap=None):
    parts = [prism(name + "_s", oct_pts(r), h, (x, y, z), color)]
    for k in range(1, storeys):
        parts.append(prism(f"{name}_b{k}", oct_pts(r * 1.07), 0.5, (x, y, z + h * k / storeys), shade(color, -0.12)))
    parts.append(prism(name + "_c", oct_pts(r * 1.14), 0.7, (x, y, z + h), shade(color, -0.1)))
    apo = r * math.cos(math.pi / 8)
    if niches:
        for k in range(storeys):
            for ang in (0, 90, 180, -90):
                parts.append(niche(f"{name}_n{k}_{ang}", r * 0.55, h / storeys * 0.62, x, y, z + h * k / storeys + h / storeys * 0.15, ang, apo, RED_RECESS if color != WHITE else NICHE))
    if chhatri_cap:
        parts.append(kiosk(name + "_ch", r * 0.85, r * 2.7, (x, y, z + h + 0.7), cap, pillars=6))
    elif dome_cap:
        parts.append(onion_dome(name + "_d", r * 0.8, (x, y, z + h + 0.7), dome_cap, height=1.3, drum=0.25))
    return join(parts, name)


def bangla_roof(name, w, d, h, loc=(0, 0, 0), color=GILT, n=10, droop=0.35):
    """A curved Bengali hut roof: ridge and eaves both bow down toward the ends (ridge along x)."""
    x0, y0, z0 = loc
    verts, faces = [], []
    for i in range(n + 1):
        t = -1 + 2 * i / n
        x = t * w / 2
        e = h * droop * (1 - t * t)
        r = h * (1 - 0.3 * t * t)
        verts += [(x, -d / 2, e), (x, 0, r), (x, d / 2, e), (x, 0, e * 0.4)]
    for i in range(n):
        a, b = 4 * i, 4 * (i + 1)
        for k in range(4):
            faces.append((a + k, a + (k + 1) % 4, b + (k + 1) % 4, b + k))
    faces.append((3, 2, 1, 0))
    faces.append((4 * n, 4 * n + 1, 4 * n + 2, 4 * n + 3))
    return mesh_from(name, verts, faces, (x0, y0, z0), color)


def chevron_dome(name, r, loc, colors=(RED, WHITE), height=1.45, bulb=1.14, drum=0.45, bands=9, zig=12):
    """A bulbous dome striped in zigzag bands of two colours (the Agra Jama Masjid's domes)."""
    x, y, z = loc
    H = r * height
    prof = [(r, 0), (r, drum * r), (r * 1.04, drum * r), (r * bulb, drum * r + H * 0.28), (r * bulb * 0.98, drum * r + H * 0.45), (r * 0.82, drum * r + H * 0.66),
            (r * 0.45, drum * r + H * 0.84), (r * 0.16, drum * r + H * 0.95), (0.0, drum * r + H)]

    def rad(zz):
        for (r0, z0), (r1, z1) in zip(prof, prof[1:]):
            if z0 <= zz <= z1 and z1 > z0:
                return r0 + (r1 - r0) * (zz - z0) / (z1 - z0)
        return prof[-1][0] if zz > prof[-1][1] else prof[0][0]

    parts = [cylinder(name + "_drum", r * 1.02, drum * r, (x, y, z), colors[0], verts=zig * 2)]
    z_lo, z_hi = drum * r, drum * r + H * 0.84
    N = zig * 2
    edges = [z_lo + (z_hi - z_lo) * k / bands for k in range(bands + 1)]
    amp = (z_hi - z_lo) / bands * 0.42
    for k in range(bands):
        verts, faces = [], []
        for ring, zz in enumerate((edges[k], edges[k + 1])):
            flat = (ring == 0 and k == 0) or (ring == 1 and k == bands - 1)
            for i in range(N):
                a = math.tau * i / N
                zo = zz + (0 if flat else (amp if i % 2 else -amp))
                rr = rad(zo) * 1.003
                verts.append((rr * math.cos(a), rr * math.sin(a), zo))
        for i in range(N):
            j = (i + 1) % N
            faces.append((i, j, N + j, N + i))
        parts.append(mesh_from(f"{name}_band{k}", verts, faces, (x, y, z), colors[k % 2]))
    tip = [(rad(z_hi), z_hi), (r * 0.16, drum * r + H * 0.95), (0.0, drum * r + H)]
    parts.append(lathe(name + "_tip", tip, (x, y, z), colors[1], verts=N, cap_bottom=False))
    parts.append(kalash(name + "_fin", r * 0.65, (x, y, z + drum * r + H - r * 0.04)))
    return join(parts, name)


def kiosk(name, r, h, loc, color=WHITE, pillars=4, dome_color=None):
    """A light chhatri for rows of small kiosks: square pillars, an eave and a small bulb."""
    x, y, z = loc
    parts = []
    for i in range(pillars):
        a = math.tau * (i + 0.5) / pillars
        parts.append(box(f"{name}_p{i}", r * 0.18, r * 0.18, h * 0.5, (x + r * 0.72 * math.cos(a), y + r * 0.72 * math.sin(a), z), color))
    parts.append(cylinder(name + "_e", r * 1.2, h * 0.07, (x, y, z + h * 0.5), color, verts=8, r_top=r * 0.95))
    prof = [(r * 0.85, 0), (r * 0.98, h * 0.12), (r * 0.9, h * 0.25), (r * 0.55, h * 0.36), (r * 0.15, h * 0.44), (0.0, h * 0.5)]
    parts.append(lathe(name + "_d", prof, (x, y, z + h * 0.57), dome_color or color, verts=10))
    return join(parts, name)


def drop_box(o, x0, x1, y0, y1, z0, z1):
    """Delete the faces of a joined mesh lying wholly inside a box (to remove a misplaced part)."""
    import bmesh
    _apply_loc(o)
    bm = bmesh.new()
    bm.from_mesh(o.data)
    inside = lambda v: x0 <= v.co.x <= x1 and y0 <= v.co.y <= y1 and z0 <= v.co.z <= z1
    dead = [f for f in bm.faces if all(inside(v) for v in f.verts)]
    bmesh.ops.delete(bm, geom=dead, context="FACES")
    loose = [v for v in bm.verts if not v.link_faces]
    bmesh.ops.delete(bm, geom=loose, context="VERTS")
    bm.to_mesh(o.data)
    bm.free()
    o.data.update()
    return o


def kit_mosque(name, w, d, color, trim, dome_color, domes=3, plinth=0.0, court=True, style="mughal", hall_depth=None):
    """worldkit.mosque facing west, with its hall cornice moved back over the hall (the kit centres it on the court)."""
    o = mosque(name, w, d, (0, 0, 0), color, trim, dome_color, domes=domes, minarets=0, plinth=plinth, court=court, style=style, hall_depth=hall_depth)
    hd = hall_depth or d * 0.28
    hall_h = max(8.0, min(w, d) * 0.14)
    dd = d * 0.9 if court else d
    zt = plinth + hall_h
    drop_box(o, -hd / 2 - 0.45, hd / 2 + 0.45, -dd / 2 - 0.45, dd / 2 + 0.45, zt - 0.02, zt + 0.52)
    hx = -w / 2 + hd / 2
    c = box(name + "_cornice", hd + 0.8, dd + 0.8, 0.5, (hx, 0, zt), trim)
    return join([o, c], name)


def garden_quarters(name, x0, x1, y0, y1, walk=10, sub=True, trees=3, tree_r=3.0, wild=False, channel=True, seed=1, path_color=PAVE, lawn=None, cypress=False):
    """A charbagh between x0..x1, y0..y1: sunken beds, raised walks with water channels, trees in the beds."""
    rnd = random.Random(seed)
    cx, cy, W, D = (x0 + x1) / 2, (y0 + y1) / 2, x1 - x0, y1 - y0
    lawn = lawn or (LAWN_WILD if wild else LAWN)
    parts = [box(name + "_lawn", W, D, 0.42, (cx, cy, 0), lawn)]
    parts.append(box(name + "_wx", W, walk, 0.9, (cx, cy, 0), path_color))
    parts.append(box(name + "_wy", walk, D, 0.9, (cx, cy, 0), path_color))
    sw = max(2.5, walk * 0.35)
    if sub:
        for s in (-1, 1):
            parts.append(box(f"{name}_sx{s}", W, sw, 0.7, (cx, cy + s * D / 4, 0), path_color))
            parts.append(box(f"{name}_sy{s}", sw, D, 0.7, (cx + s * W / 4, cy, 0), path_color))
    if channel:
        wc = DRY if wild else WATER
        parts.append(box(name + "_cx", W * 0.97, walk * 0.2, 0.95, (cx, cy, 0), wc))
        parts.append(box(name + "_cy", walk * 0.2, D * 0.97, 0.95, (cx, cy, 0), wc))
    if cypress and not wild:
        n = int(D / 12)
        for i in range(n):
            ty = y0 + D * (i + 0.5) / n
            if abs(ty - cy) < walk * 1.6:
                continue
            for s in (-1, 1):
                parts.append(tree(f"{name}_cy{i}{s}", 1.9, (cx + s * walk * 0.62, ty, 0.9), "#4F6B45", kind="cypress"))
    # trees in the beds
    nb = 4 if sub else 2
    bw, bd = W / nb, D / nb
    for i in range(nb):
        for j in range(nb):
            bx, by = x0 + bw * (i + 0.5), y0 + bd * (j + 0.5)
            k = trees + (1 if wild else 0)
            for a in range(k):
                for b in range(k):
                    tx = bx + (a - (k - 1) / 2) * bw * 0.6 / max(1, k - 1) if k > 1 else bx
                    ty = by + (b - (k - 1) / 2) * bd * 0.6 / max(1, k - 1) if k > 1 else by
                    rr = tree_r
                    if wild:
                        tx += rnd.uniform(-3, 3)
                        ty += rnd.uniform(-3, 3)
                        rr = tree_r * rnd.uniform(1.0, 1.6)
                    parts.append(tree(f"{name}_t{i}{j}{a}{b}", rr, (tx, ty, 0.3), "#6E8A58" if not wild else "#5D7446"))
    return join(parts, name)


# ---------------------------------------------------------------- the Taj Mahal

def taj_mosque(name, cx, cy, z, ang):
    """The red sandstone mosque (or its twin, the jawab) of the Taj terrace, built facing south then turned."""
    p = [box(name + "_plat", 64, 30, 1.0, (0, 0, 0), RED_LT)]
    p.append(box(name + "_body", 56, 23, 14, (0, 0, 1.0), RED))
    p.append(box(name + "_par", 56.6, 23.6, 0.7, (0, 0, 15.0), WHITE))
    p.append(pishtaq(name + "_pish", 17, 21, 0, -11.5, 1.0, 0, 0, RED, WHITE, RED_RECESS, DARK, 1.2, True))
    for s in (-1, 1):
        for k, bx in enumerate((13.5, 22.0)):
            p.append(box(f"{name}_fr{s}{k}", 7.0, 0.3, 10.6, (s * bx, -11.6, 1.0), WHITE))
            p.append(niche(f"{name}_ar{s}{k}", 5.6, 9.6, s * bx, -11.8, 1.0, 0, 0, RED_RECESS))
    for k, (dx, r) in enumerate(((0, 6.2), (-17, 4.4), (17, 4.4))):
        p.append(cylinder(f"{name}_dr{k}", r * 1.02, 2.6, (dx, 1.5, 15.7), RED, verts=24))
        p.append(onion_dome(f"{name}_dm{k}", r, (dx, 1.5, 18.3), WHITE, bulb=1.15, height=1.5, drum=0.25))
    for sx in (-1, 1):
        for sy in (-1, 1):
            p.append(oct_tower(f"{name}_tw{sx}{sy}", 2.5, 18, sx * 28, sy * 11.5, 1.0, RED, WHITE, storeys=3, niches=False))
    o = join(p, name)
    rz(o, ang)
    return mv(o, cx, cy, z)


def taj_gate(name, cx, cy):
    """The Darwaza-i Rauza: a red sandstone block with marble-framed pishtaqs on both faces, octagonal corner towers and rows of chhatris."""
    W, D, H = 41, 34, 21
    p = [box(name + "_body", W, D, H, (0, 0, 0), RED)]
    p.append(box(name + "_corn", W + 0.6, D + 0.6, 0.9, (0, 0, H - 0.8), WHITE))
    p.append(box(name + "_roof", W - 1.0, D - 1.0, 0.15, (0, 0, H), shade(RED, 0.15)))
    for face in ("S", "N"):
        ang = FACE[face]
        p.append(pishtaq(f"{name}_p{face}", 20, 24, 0, 0, 0, ang, D / 2, RED, WHITE, RED_RECESS, DARK, 1.4, False, CALLIG))
        for s in (-1, 1):
            for k, zz in enumerate((1.0, 11.0)):
                p.append(rz(box(f"{name}_fr{face}{s}{k}", 6.2, 0.3, 8.6, (s * 15.2, -D / 2 - 0.15, zz), WHITE), ang))
                p.append(rz(arch_panel(f"{name}_n{face}{s}{k}", 4.8, 7.8, (s * 15.2, -D / 2 - 0.35, zz), "S", RED_RECESS, True, 0.3), ang))
    for face in ("E", "W"):
        p.append(niche(f"{name}_n{face}", 7.0, 13.0, 0, 0, 1.0, FACE[face], W / 2 + 0.05, RED_RECESS))
    # rows of eleven little chhatris over the two main faces
    for sy in (-1, 1):
        for i in range(11):
            p.append(kiosk(f"{name}_c{sy}{i}", 1.15, 4.2, (-15 + 3 * i, sy * (D / 2 - 1.6), H), WHITE, pillars=4))
    for sx in (-1, 1):
        for sy in (-1, 1):
            p.append(oct_tower(f"{name}_tw{sx}{sy}", 3.3, 25, sx * (W / 2), sy * (D / 2), 0, RED, WHITE, storeys=3, niches=False))
    o = join(p, name)
    return mv(o, cx, cy, 0)


def taj_tomb(name, cx, cy, z):
    """The mausoleum on its plinth: chamfered body, pishtaqs, double dome on a tall drum, chhatris, minarets."""
    p = []
    PL, PH = 95, 6.7
    p.append(box(name + "_plinth", PL, PL, PH, (cx, cy, z), WHITE))
    p.append(box(name + "_plband", PL + 0.6, PL + 0.6, 0.6, (cx, cy, z + PH - 0.6), WHITE_LINE))
    for f in ("S", "N", "E", "W"):
        arc = arcade(name + "_plarc" + f, PL * 0.92, PH * 0.72, 15, (0, -PL / 2 - 0.05, z + 0.5), "S", shade(WHITE, -0.2), True, 0.72, 0.25)
        p.append(mv(rz(arc, FACE[f]), cx, cy, 0))
    p.append(flight(name + "_steps", 12, PH, 10, 10, cx, cy - PL / 2 - 10, 0, WHITE))
    zb = z + PH
    S, C, BH = 56, 9.5, 27
    p.append(prism(name + "_body", chamfer_pts(S, C), BH, (cx, cy, zb), WHITE))
    p.append(prism(name + "_par", chamfer_pts(S + 1.0, C + 0.4), 1.2, (cx, cy, zb + BH), WHITE_LINE))
    apo = S / 2
    for f in ("S", "N", "E", "W"):
        ang = FACE[f]
        p.append(pishtaq(name + "_pish" + f, 22, 33, cx, cy, zb, ang, apo, WHITE, WHITE_LINE, NICHE, DARK, 1.0, True, CALLIG))
        for s in (-1, 1):
            for k, zz in enumerate((1.2, 14.4)):
                n = arch_panel(f"{name}_fl{f}{s}{k}", 5.4, 10.6, (s * 15.0, -apo - 0.05, zb + zz), "S", NICHE, True, 0.4)
                p.append(mv(rz(n, ang), cx, cy, 0))
    dch = (S / 2 - C / 2) * math.sqrt(2)
    for k, ang in enumerate((45, 135, -135, -45)):
        for j, zz in enumerate((1.2, 14.4)):
            p.append(niche(f"{name}_ch{k}{j}", 6.6, 10.6, cx, cy, zb + zz, ang, dch + 0.02, NICHE))
    for k, (vx, vy) in enumerate(chamfer_pts(S, C)):
        p.append(cylinder(f"{name}_gul{k}", 0.6, BH + 3.5, (cx + vx * 1.005, cy + vy * 1.005, zb), WHITE, verts=8))
        p.append(onion_dome(f"{name}_guld{k}", 0.75, (cx + vx * 1.005, cy + vy * 1.005, zb + BH + 3.5), WHITE, height=1.4, drum=0.2, finial=False))
    # drum and the great dome
    zd = zb + BH + 1.2
    R = 10.0
    p.append(cylinder(name + "_drum", R, 8.6, (cx, cy, zd), WHITE, verts=36))
    p.append(cylinder(name + "_drumband", R + 0.35, 0.8, (cx, cy, zd + 7.2), WHITE_LINE, verts=36))
    p.append(cylinder(name + "_drumbase", R + 0.6, 0.9, (cx, cy, zd), WHITE_LINE, verts=36))
    zq = zd + 8.6
    prof = [(R, 0), (R * 1.03, 0.8), (R * 1.12, 2.5), (R * 1.2, 5.0), (R * 1.22, 7.4), (R * 1.17, 10.0), (R * 1.03, 12.6), (R * 0.82, 15.0), (R * 0.56, 17.3),
            (R * 0.32, 19.2), (R * 0.14, 20.6), (R * 0.05, 21.4), (0.0, 21.8)]
    p.append(lathe(name + "_dome", prof, (cx, cy, zq), WHITE, verts=40))
    p.append(lathe(name + "_lotus", [(R * 0.22, 19.4), (R * 0.36, 18.9), (R * 0.39, 19.2), (R * 0.2, 20.8), (R * 0.06, 21.5)], (cx, cy, zq), WHITE_LINE, verts=16))
    p.append(kalash(name + "_finial", 9.0, (cx, cy, zq + 21.6)))
    for sx in (-1, 1):
        for sy in (-1, 1):
            p.append(chhatri(f"{name}_cht{sx}{sy}", 4.3, 12.5, (cx + sx * 17, cy + sy * 17, zb + BH + 1.2), WHITE, pillars=8, base=2.2))
    # minarets on the plinth corners
    for sx in (-1, 1):
        for sy in (-1, 1):
            mx, my = cx + sx * 43, cy + sy * 43
            p.append(prism(f"{name}_mb{sx}{sy}", oct_pts(3.7), 1.6, (mx, my, zb), WHITE_LINE))
            p.append(minaret(f"{name}_min{sx}{sy}", 2.8, 32.5, (mx, my, zb + 1.6), WHITE, WHITE_LINE, 2, "chhatri", 16, 0.86))
            p.append(cylinder(f"{name}_mg{sx}{sy}", 2.8 * 0.86 * 1.45, 0.55, (mx, my, zb + 1.6 + 32.5 - 0.55), WHITE_LINE, verts=16))
    return p


def taj_mahal(neglect=False):
    m = Model("taj-mahal")
    ZT = 1.6  # riverfront terrace height
    # ---- stage 0: ground, terrace, enclosure walls and towers
    m.add(0, box("ground", 300, 540, 0.3, (0, 0, 0), GROUND), "walls")
    m.add(0, box("terrace", 300, 108, ZT, (0, 214, 0), shade(RED, 0.28)))
    lines = [box(f"tl{i}", 0.8, 108, ZT + 0.02, (-150 + 300 * i / 10, 214, 0), WHITE) for i in range(1, 10)]
    lines += [box(f"tm{i}", 300, 0.8, ZT + 0.02, (0, 160 + 108 * i / 4, 0), WHITE) for i in range(1, 4)]
    m.add(0, join(lines, "terrace_lines"))
    m.add(0, box("riverwall", 300, 3, ZT + 1.4, (0, 266.5, 0), RED_DK))
    m.add(0, wall_run("gwall", [(-150, 266), (-150, -140), (150, -140), (150, 266)], 7, 2.6, (0, 0, 0), RED, towers=False, merlon="round"))
    m.add(0, wall_run("jwall", [(-150, -140), (-150, -268), (150, -268), (150, -140)], 6, 2.4, (0, 0, 0), RED, towers=False, merlon="round"))
    for s in (-1, 1):
        m.add(0, oct_tower(f"rtower{s}", 7.5, 22, s * 144, 262, ZT, RED, WHITE, storeys=3))
        m.add(0, oct_tower(f"gtower{s}", 5.5, 13, s * 150, -140, 0, RED, WHITE, storeys=2))
        m.add(0, oct_tower(f"jtower{s}", 3.8, 9, s * 150, -268, 0, RED, WHITE, storeys=1))
        m.add(0, arcade(f"sarc{s}", 110, 4.8, 11, (s * 82, -138.6, 0.3), "N", RED_RECESS, True, 0.7, 0.3))
    # ---- stage 1: garden, great gate, forecourt
    m.add(1, garden_quarters("bagh", -146, 146, -137, 159, walk=16, sub=True, trees=3 if not neglect else 3, tree_r=3.0, wild=neglect, channel=True, seed=7, cypress=True), "garden")
    if not neglect:
        jets = [cylinder(f"jet{i}", 0.25, 1.8, (0, -128 + 12 * i, 0.95), WHITE, verts=6) for i in range(24) if abs(-128 + 12 * i - 11) > 18]
        m.add(1, join(jets, "jets"))
    m.add(1, box("tank_plat", 30, 30, 1.6, (0, 11, 0), WHITE))
    m.add(1, box("tank", 22, 22, 1.7, (0, 11, 0), DRY if neglect else WATER))
    if not neglect:
        m.add(1, join([cylinder(f"tj{i}", 0.3, 2.6, (dx, 11 + dy, 1.7), WHITE, verts=6) for i, (dx, dy) in enumerate(((0, 0), (6, 6), (-6, 6), (6, -6), (-6, -6)))], "tank_jets"))
    for s in (-1, 1):
        pv = [box(f"pav{s}", 14, 26, 11, (s * 146, 11, 0), RED), box(f"pavc{s}", 14.6, 26.6, 0.7, (s * 146, 11, 11), WHITE)]
        pv.append(arcade(f"pava{s}", 22, 7, 3, (s * 139 - s * 0.05, 11, 0), "W" if s > 0 else "E", RED_RECESS))
        for sy in (-1, 1):
            pv.append(chhatri(f"pavch{s}{sy}", 1.8, 5.5, (s * 146, 11 + sy * 9.5, 11.7), WHITE, pillars=6))
        m.add(1, join(pv, f"pavilion{s}"))
    m.add(1, taj_gate("gate", 0, -140))
    m.add(1, box("forecourt", 140, 118, 0.35, (0, -205, 0), PAVE))
    for s in (-1, 1):
        m.add(1, courtyard_ring(f"khawass{s}", 72, 100, 6, 9, (s * 108, -205, 0), RED, RED_RECESS))
        m.add(1, mgate(f"jgate{s}", 16, 12, 12, (s * 150, -205, 0), "E" if s > 0 else "W", RED, WHITE, 1))
        m.add(1, tomb(f"saheli{s}", 11, 8, (s * 58, -250, 0), RED, WHITE, plinth=1.2, chhatris=0, octagonal=True))
    m.add(1, mgate("sgate", 18, 12, 12, (0, -268, 0), "S", RED, WHITE, 1))
    # ---- stage 2: plinth, tomb body, mosque and jawab
    cx, cy = 0, 212
    tomb_parts = taj_tomb("tomb", cx, cy, ZT)
    top = ("tomb_dome", "tomb_lotus", "tomb_finial", "tomb_cht")
    mins = ("tomb_min", "tomb_mg", "tomb_mb")
    body = [t for t in tomb_parts if not t.name.startswith(top + mins)]
    domes = [t for t in tomb_parts if t.name.startswith(top)]
    minars = [t for t in tomb_parts if t.name.startswith(mins)]
    m.add(2, join(body, "tomb_body"), "tomb")
    m.add(2, taj_mosque("mosque", -112, 214, ZT, 90))
    m.add(2, taj_mosque("jawab", 112, 214, ZT, -90))
    # ---- stage 3: the dome, chhatris and minarets
    m.add(3, join(domes, "tomb_domes"), "domes")
    m.add(3, join(minars, "minarets"))
    return m


# ---------------------------------------------------------------- Taj Ganj

def taj_ganj():
    m = Model("taj-ganj")
    m.add(0, box("ground", 300, 280, 0.3, (0, 0, 0), GROUND), "sarais")
    m.add(0, box("bazaar_x", 300, 22, 0.4, (0, 0, 0), PAVE))
    m.add(0, box("bazaar_y", 22, 280, 0.4, (0, 0, 0), PAVE))
    for sx in (-1, 1):
        for sy in (-1, 1):
            x, y = sx * 78, sy * 72
            m.add(0, courtyard_ring(f"sarai{sx}{sy}", 116, 104, 7, 11, (x, y, 0), RED if (sx + sy) else shade(MUDBRICK, 0.1), RED_RECESS))
            m.add(0, box(f"court{sx}{sy}", 92, 80, 0.35, (x, y, 0), shade(PAVE, 0.15)))
            m.add(0, cylinder(f"well{sx}{sy}", 2.2, 1.0, (x, y, 0), WHITE, verts=10))
            for t in range(4):
                m.add(0, tree(f"tr{sx}{sy}{t}", 3.2, (x + (t - 1.5) * 18, y + (-1) ** t * 18, 0.3)))
    for sx in (-1, 1):
        for sy in (-1, 1):
            x, y = sx * 78, sy * 72
            # gateways of each sarai onto the bazaar
            m.add(1, pishtaq(f"sgx{sx}{sy}", 12, 11, x, y - sy * 52, 0, 0 if sy > 0 else 180, 0.0, RED, WHITE, RED_RECESS, DARK, 2.0, True), "gates")
            # shop rows facing the bazaar
            m.add(1, box(f"shops_x{sx}{sy}", 120, 7, 4.2, (sx * 82, sy * 14.5, 0), shade(RED, 0.1)))
            m.add(1, arcade(f"shopa_x{sx}{sy}", 116, 3.4, 14, (sx * 82, sy * 14.5 - sy * 3.55, 0), "S" if sy > 0 else "N", RED_RECESS, True, 0.75, 0.3))
            m.add(1, box(f"shops_y{sx}{sy}", 7, 110, 4.2, (sx * 14.5, sy * 72, 0), shade(RED, 0.1)))
            m.add(1, arcade(f"shopa_y{sx}{sy}", 106, 3.4, 13, (sx * 14.5 - sx * 3.55, sy * 72, 0), "W" if sx > 0 else "E", RED_RECESS, True, 0.75, 0.3))
    # the chowk at the crossing: four little gateways and a central platform
    m.add(2, box("chowk", 26, 26, 0.6, (0, 0, 0), WHITE), "chowk")
    for ang, (gx, gy) in ((0, (0, -11)), (180, (0, 11)), (90, (11, 0)), (-90, (-11, 0))):
        g = mughal_gate(f"cg{ang}", 9, 4, 8, RED, WHITE, 0)
        m.add(2, mv(rz(g, ang), gx, gy, 0))
    for i in range(6):
        m.add(2, box(f"awn{i}", 6, 4, 0.2, (-60 + 24 * i, -6, 3.2), "#C8A86A"))
    return m


# ---------------------------------------------------------------- Mahtab Bagh

def mehtab_bagh():
    m = Model("mehtab-bagh")
    m.add(0, box("ground", 290, 290, 0.3, (0, 0, 0), GROUND), "walls")
    m.add(0, wall_run("wall", [(-145, -128), (-145, 145), (145, 145), (145, -128)], 5, 2.2, (0, 0, 0), RED, towers=False, merlon="round"))
    m.add(0, box("riverwall", 290, 3, 3.4, (0, -143.5, 0), RED_DK))
    m.add(0, box("terrace", 286, 60, 1.6, (0, -113, 0), shade(RED, 0.28)))
    for s in (-1, 1):
        m.add(0, oct_tower(f"rt{s}", 6.0, 15, s * 140, -138, 0, RED, WHITE, storeys=2))
        m.add(0, oct_tower(f"nt{s}", 4.0, 9, s * 145, 145, 0, RED, WHITE, storeys=1))
    m.add(0, mgate("ngate", 16, 10, 10, (0, 145, 0), "N", RED, WHITE, 1))
    m.add(1, garden_quarters("bagh", -142, 142, -82, 142, walk=12, sub=True, trees=3, tree_r=3.2, seed=3, cypress=False), "garden")
    # the great octagonal pool on the riverside terrace
    m.add(2, prism("pool_rim", oct_pts(26), 1.9, (0, -112, 0), WHITE), "pool")
    m.add(2, prism("pool", oct_pts(23.5), 2.0, (0, -112, 0), WATER))
    m.add(2, join([cylinder(f"jet{i}", 0.25, 2.4, (16 * math.cos(math.tau * i / 8), -112 + 16 * math.sin(math.tau * i / 8), 2.0), WHITE, verts=6) for i in range(8)], "jets"))
    for s in (-1, 1):
        pv = [box(f"pav{s}", 22, 12, 7, (s * 62, -115, 1.6), RED), box(f"pavr{s}", 23, 13, 0.6, (s * 62, -115, 8.6), WHITE)]
        pv.append(arcade(f"pava{s}", 20, 5, 3, (s * 62, -121.05, 1.6), "S", RED_RECESS))
        pv.append(chhatri(f"pavc{s}", 2.4, 6.5, (s * 62, -115, 9.2), WHITE, pillars=6))
        m.add(2, join(pv, f"pavilion{s}"))
    return m


# ---------------------------------------------------------------- the fort

def arc_pts(Ex, rx, ry, n=28, k=0.7):
    out = []
    for i in range(n + 1):
        t = math.pi / 2 - math.pi * i / n
        c, s = max(0.0, math.cos(t)), math.sin(t)
        out.append((Ex - rx * c ** k, ry * s))
    return out


def arc_point(Ex, rx, ry, deg, k=0.7):
    """Point on the arc at parameter angle deg and the outward normal there (math angle, degrees)."""
    t = math.radians(deg)
    f = lambda tt: (Ex - rx * max(0.0, math.cos(tt)) ** k, ry * math.sin(tt))
    (x0, y0), (x1, y1) = f(t - 0.01), f(t + 0.01)
    tx, ty = x1 - x0, y1 - y0
    nx, ny = ty, -tx  # outward (west side) for an arc traced north-to-south... checked below
    x, y = f(t)
    if nx * (x - Ex) + ny * y < 0:
        nx, ny = -nx, -ny
    return x, y, math.degrees(math.atan2(ny, nx))


def mughal_gate(name, w, d, h, color=RED, trim=WHITE, kiosks=3):
    """A fort gate facing south: a block with a framed arch, two big octagonal towers with domed kiosks, kiosks on the parapet."""
    p = [box(name + "_b", w, d, h, (0, 0, 0), color)]
    p.append(box(name + "_band", w + 0.4, d + 0.4, 0.8, (0, 0, h - 1.6), trim))
    p.append(pishtaq(name + "_p", w * 0.42, h * 0.9, 0, 0, 0, 0, d / 2, color, trim, RED_RECESS, DARK, 1.0, False, trim))
    p.append(arch_panel(name + "_back", w * 0.22, h * 0.55, (0, d / 2 + 0.05, 0), "N", DARK))
    tr = w * 0.17
    for s in (-1, 1):
        p.append(prism(f"{name}_t{s}", oct_pts(tr), h * 1.15, (s * w / 2, -d * 0.18, 0), shade(color, -0.04)))
        p.append(prism(f"{name}_tb{s}", oct_pts(tr * 1.08), 0.7, (s * w / 2, -d * 0.18, h * 0.6), trim))
        p.append(prism(f"{name}_tc{s}", oct_pts(tr * 1.12), 0.7, (s * w / 2, -d * 0.18, h * 1.15), shade(color, -0.12)))
        p.append(kiosk(f"{name}_tk{s}", tr * 0.8, tr * 2.6, (s * w / 2, -d * 0.18, h * 1.15 + 0.7), trim, pillars=6))
    for i in range(kiosks):
        kx = (i - (kiosks - 1) / 2) * w * 0.16
        p.append(kiosk(f"{name}_k{i}", w * 0.04, w * 0.12, (kx, -d / 2 + 1.0, h), trim))
    return join(p, name)


def mgate(name, w, d, h, loc=(0, 0, 0), face="S", color=RED, trim=WHITE, kiosks=3):
    g = mughal_gate(name, w, d, h, color, trim, kiosks)
    rz(g, FACE[face])
    return mv(g, *loc)


def fort_gate(name, w, d, h, x, y, normal_deg, color=RED, trim=WHITE, style="mughal", out=0.0):
    g = mughal_gate(name, w, d, h, color, trim) if style == "mughal" else gatehouse(name, w, d, h, (0, 0, 0), "S", color, trim, style)
    rz(g, normal_deg + 90)
    a = math.radians(normal_deg)
    return mv(g, x + math.cos(a) * out, y + math.sin(a) * out, 0)


def agra_fort(era="1650"):
    m = Model("agra-fort")
    Ex = 224
    inner = arc_pts(Ex, 420, 420)
    outer = arc_pts(Ex, 436, 438)
    moat = arc_pts(Ex, 452, 452)
    # ---- stage 0: ground, moat, double walls
    m.add(0, prism("ground", [(Ex + 4, -444)] + list(reversed(outer))[1:-1] + [(Ex + 4, 444)], 0.4, (0, 0, 0), shade(RED, 0.4)), "walls")
    m.add(0, prism("inner_ground", list(reversed(inner)), 0.8, (0, 0, 0), "#CDB492"))
    m.add(0, wall_run("moat", moat, 0.35, 10, (0, 0, 0), WATER, towers=False, merlon=None))
    m.add(0, wall_run("outer", outer, 10, 4.5, (0, 0, 0), RED, towers=True, tower_r=6.5, tower_every=55, merlon="box"))
    m.add(0, wall_run("inner", inner, 20, 8, (0, 0, 0), RED, towers=True, tower_r=11, tower_every=65, merlon="round", batter=0.15))
    m.add(0, wall_run("river", [(Ex, 420), (Ex, -420)], 16, 7, (0, 0, 0), RED, towers=True, tower_r=9, tower_every=95, merlon="round"))
    m.add(0, box("riverbank", 10, 860, 0.5, (Ex + 1, 0, 0), shade(RED, 0.35)))
    # ---- stage 1: gates
    dx, dy, dn = arc_point(Ex, 420, 420, 8)
    m.add(1, fort_gate("delhi_gate", 56, 34, 26, dx, dy, dn, out=5), "gates")
    ox, oy, on = arc_point(Ex, 436, 438, 8)
    m.add(1, fort_gate("delhi_outer", 26, 14, 13, ox, oy, on, out=2))
    mx, my, mn = arc_point(Ex, 452, 452, 8)
    m.add(1, mv(rz(box("delhi_bridge", 16, 8, 0.8, (0, 0, 0), TIMBER), mn), mx, my, 0))
    sx_, sy_, sn = arc_point(Ex, 420, 420, -50)
    m.add(1, fort_gate("amar_singh_gate", 46, 30, 23, sx_, sy_, sn, out=5))
    ox, oy, on = arc_point(Ex, 436, 438, -50)
    m.add(1, fort_gate("amar_outer", 24, 14, 12, ox, oy, on, out=2))
    mx, my, mn = arc_point(Ex, 452, 452, -50)
    m.add(1, mv(rz(box("amar_bridge", 14, 8, 0.8, (0, 0, 0), TIMBER), mn), mx, my, 0))
    m.add(1, mv(rz(mughal_gate("water_gate", 20, 10, 14, RED, WHITE, kiosks=1), 90), Ex, 250, 0))
    # roads inside
    m.add(1, box("road_delhi", 150, 10, 0.95, (-105, 60, 0), PAVE))
    m.add(1, mv(rz(box("road_amar", 250, 10, 0.95, (0, 0, 0), PAVE), 36), 25, -240, 0))
    # ---- stage 2: palaces
    pal = []
    marble = era == "1650"
    hall_color = PLASTER_W if marble else RED
    # Diwan-i Am and its court
    pal.append(courtyard_ring("dia_court", 150, 130, 7, 8, (40, 40, 0.8), RED, RED_RECESS))
    pal.append(box("dia_pave", 134, 114, 0.3, (40, 40, 0.8), shade(PAVE, 0.1)))
    pal.append(box("dia_plinth", 30, 72, 1.4, (128, 40, 0.8), RED))
    pal.append(box("dia_hall", 24, 66, 10, (128, 40, 2.2), hall_color))
    pal.append(arcade("dia_arc", 62, 7.5, 9, (115.9, 40, 2.2), "W", DARK if marble else RED_RECESS, True, 0.82, 0.4))
    pal.append(box("dia_roof", 25, 67, 1.0, (128, 40, 12.2), shade(hall_color, -0.08)))
    for s in (-1, 1):
        pal.append(chhatri(f"dia_ch{s}", 2.6, 7.0, (118, 40 + s * 31, 13.2), WHITE if marble else RED, pillars=6))
    # Machchhi Bhawan
    pal.append(courtyard_ring("machchhi", 62, 72, 9, 9, (176, 40, 0.8), RED if not marble else shade(RED, 0.05), RED_RECESS))
    pal.append(box("machchhi_pave", 44, 54, 0.3, (176, 40, 0.8), LAWN))
    # Jahangiri Mahal (Akbar's red palace)
    pal.append(courtyard_ring("jahangiri", 76, 70, 13, 15, (180, -152, 0.8), RED, RED_RECESS))
    pal.append(box("jahangiri_band", 76.6, 70.6, 0.9, (180, -152, 11.5), WHITE))
    pal.append(pishtaq("jahangiri_gate", 15, 17, 142, -152, 0.8, -90, 0.0, RED, WHITE, RED_RECESS, DARK, 1.6, False))
    for s in (-1, 1):
        pal.append(oct_tower(f"jahangiri_t{s}", 3.6, 16, 142, -152 + s * 34, 0.8, RED, WHITE, storeys=2, niches=False))
    pal.append(courtyard_ring("akbari_mahal", 58, 58, 10, 12, (190, -238, 0.8), RED, RED_RECESS))
    # inland buildings: barracks, stores, a garden
    pal.append(box("mina_bazaar_n", 118, 8, 6, (-108, 71, 0.8), shade(RED, 0.08)))
    pal.append(box("mina_bazaar_s", 118, 8, 6, (-108, 49, 0.8), shade(RED, 0.08)))
    pal.append(arcade("mina_an", 114, 4, 16, (-108, 66.95, 0.8), "S", RED_RECESS, True, 0.75, 0.3))
    pal.append(arcade("mina_as", 114, 4, 16, (-108, 53.05, 0.8), "N", RED_RECESS, True, 0.75, 0.3))
    pal.append(courtyard_ring("barracks_w", 60, 46, 6, 8, (-95, -60, 0.8), shade(RED, 0.06), RED_RECESS))
    pal.append(courtyard_ring("stores", 52, 40, 6, 8, (-40, 250, 0.8), shade(RED, 0.06), RED_RECESS))
    pal.append(garden_quarters("fort_garden", -120, -50, -190, -120, walk=5, sub=False, trees=2, tree_r=3.0, seed=11))
    pal.append(courtyard_ring("barracks_s", 70, 40, 6, 8, (20, -150, 0.8), shade(RED, 0.06), RED_RECESS))
    # houses of officers, stores, stables and kitchens filling the rest of the fort
    rnd = random.Random(23)
    keep_out = [(-35, 120, -25, 105), (-170, -45, 40, 80), (-130, -60, -85, -35), (-125, -45, -195, -115), (-15, 55, -175, -125),
                (-70, -10, 225, 275), (0, 85, 150, 215), (125, 224, -280, 110), (100, 150, 0, 80)]
    n = 0
    while n < 34:
        hx, hy = rnd.uniform(-170, 120), rnd.uniform(-330, 330)
        lim = Ex - 420 * max(0.0, 1 - (hy / 420) ** 2) ** 0.35 + 30
        if hx < lim or any(a <= hx <= b and c <= hy <= d for a, b, c, d in keep_out):
            continue
        if abs(hy - (-240 + (hx - 25) * 0.73)) < 18 and -120 < hx < 140:
            continue  # keep the road from the Amar Singh Gate clear
        hw, hd_ = rnd.uniform(14, 30), rnd.uniform(12, 24)
        pal.append(flat_house(f"q{n}", hw, hd_, rnd.uniform(5, 8), (hx, hy, 0.8), rnd.choice([shade(RED, 0.05), RED_LT, PLASTER_W]), door_face=rnd.choice("SNEW")))
        n += 1
    for i in range(22):
        tx, ty = rnd.uniform(-150, 110), rnd.uniform(-300, 300)
        if tx > Ex - 420 * max(0.0, 1 - (ty / 420) ** 2) ** 0.35 + 25 and not any(a <= tx <= b and c <= ty <= d for a, b, c, d in keep_out):
            pal.append(tree(f"ft{i}", 4.0, (tx, ty, 0.8)))
    m.add(2, join(pal, "palaces"), "palaces")
    # ---- stage 3: river palaces (marble under Shah Jahan, red under Akbar) and the Moti Masjid
    rp = []
    if marble:
        # Diwan-i Khas on its terrace
        rp.append(box("dik_terrace", 34, 64, 2.2, (204, 82, 0.8), shade(WHITE, -0.06)))
        rp.append(box("dik_hall", 16, 30, 8, (212, 92, 3.0), WHITE))
        rp.append(arcade("dik_arc", 28, 6, 5, (203.95, 92, 3.0), "W", NICHE, True, 0.8, 0.3))
        for sy in (-1, 1):
            rp.append(chhatri(f"dik_ch{sy}", 2.2, 6, (212, 92 + sy * 12, 11.0), WHITE, pillars=6))
        # Musamman Burj
        rp.append(prism("mb_bastion", oct_pts(13), 16, (Ex + 3, 18, 0), RED))
        rp.append(prism("mb_pav", oct_pts(9), 9, (Ex + 3, 18, 16), WHITE))
        for ang in (0, 45, 90, 135, 180, -45, -90, -135):
            rp.append(niche(f"mb_n{ang}", 4.0, 6.8, Ex + 3, 18, 16.4, ang, 9 * math.cos(math.pi / 8), NICHE))
        rp.append(prism("mb_corn", oct_pts(10), 0.7, (Ex + 3, 18, 25), WHITE_LINE))
        rp.append(shallow_dome("mb_dome", 6.6, (Ex + 3, 18, 25.7), WHITE, rise=0.95, drum=1.4))
        rp.append(kalash("mb_fin", 4.0, (Ex + 3, 18, 25.7 + 1.4 + 6.2)))
        # Khas Mahal, the Anguri Bagh and the golden pavilions
        rp.append(box("km_terrace", 30, 100, 2.0, (209, -48, 0.8), shade(WHITE, -0.06)))
        rp.append(box("km_hall", 16, 40, 9, (214, -48, 2.8), WHITE))
        rp.append(arcade("km_arc", 34, 7, 5, (205.95, -48, 2.8), "W", NICHE, True, 0.78, 0.3))
        for sy in (-1, 1):
            rp.append(chhatri(f"km_ch{sy}", 2.0, 5.5, (214, -48 + sy * 15, 11.8), WHITE, pillars=6))
            rp.append(box(f"gp{sy}", 10, 14, 6, (214, -48 + sy * 33, 2.8), WHITE))
            rp.append(bangla_roof(f"gpr{sy}", 14, 11, 5.0, (214, -48 + sy * 33, 8.8), GILT))
            rp[-1] = rz(rp[-1], 90, 214, -48 + sy * 33)
        rp.append(garden_quarters("anguri", 128, 196, -84, -12, walk=4, sub=True, trees=1, tree_r=2.4, seed=5))
        for s in (-1, 1):
            rp.append(box(f"ang_r{s}", 72, 7, 6, (162, -48 + s * 39, 0.8), RED))
        rp.append(box("ang_w", 7, 84, 6, (124, -48, 0.8), RED))
        # Moti Masjid (1648-54)
        mm = kit_mosque("moti", 70, 52, WHITE, WHITE, WHITE, domes=3, plinth=3.0, style="mughal")
        rp.append(mv(mm, 40, 182, 0.8))
        for k in range(-3, 4):
            rp.append(kiosk(f"moti_c{k}", 1.0, 3.6, (57 - 40, 182 + k * 6.5, 0.8 + 3.0 + 8.0), WHITE, pillars=6))
    else:
        # Akbar's river palaces of carved red sandstone
        for k, (y, w, d, h) in enumerate(((92, 18, 34, 9), (18, 20, 28, 10), (-48, 18, 40, 9))):
            rp.append(box(f"ap_terr{k}", 30, d + 16, 2.0, (209, y, 0.8), RED_LT))
            rp.append(box(f"ap{k}", w, d, h, (212, y, 2.8), RED))
            rp.append(arcade(f"apa{k}", d - 4, h * 0.7, max(3, int(d / 7)), (212 - w / 2 - 0.05, y, 2.8), "W", RED_RECESS, True, 0.78, 0.3))
            for sy in (-1, 1):
                rp.append(chhatri(f"ap_ch{k}{sy}", 2.0, 5.5, (212, y + sy * (d / 2 - 3), 2.8 + h), RED, pillars=6))
        rp.append(prism("shah_burj", oct_pts(12), 15, (Ex + 3, 18, 0), RED))
        rp.append(garden_quarters("anguri", 128, 196, -84, -12, walk=4, sub=False, trees=2, tree_r=2.6, seed=5))
        rp.append(courtyard_ring("akbar_zenana", 60, 50, 8, 10, (40, 182, 0.8), RED, RED_RECESS))
    m.add(3, join(rp, "river_palaces"), "river palaces")
    return m


def badalgarh():
    """The Lodi brick fort, reconstructed: a brick circuit with round bastions, a palace by the river, a mosque and houses."""
    m = Model("badalgarh")
    Ex = 226
    wall = arc_pts(Ex, 380, 390, n=22, k=0.75)
    ditch = arc_pts(Ex, 398, 406, n=22, k=0.75)
    m.add(0, prism("ground", [(Ex + 4, -410)] + list(reversed(ditch))[1:-1] + [(Ex + 4, 410)], 0.3, (0, 0, 0), GROUND), "walls")
    m.add(0, prism("inner_ground", list(reversed(wall)), 0.6, (0, 0, 0), "#C9AE88"))
    m.add(0, wall_run("ditch", ditch, 0.3, 12, (0, 0, 0), "#9B8461", towers=False, merlon=None))
    m.add(0, wall_run("wall", wall, 12, 7, (0, 0, 0), BRICK_FORT, towers=True, tower_r=8, tower_every=50, merlon="box", batter=0.2))
    m.add(0, wall_run("river", [(Ex, 390), (Ex, -390)], 10, 6, (0, 0, 0), BRICK_FORT, towers=True, tower_r=7, tower_every=80, merlon="box"))
    gx, gy, gn = arc_point(Ex, 380, 390, 8, 0.75)
    m.add(1, fort_gate("west_gate", 30, 20, 15, gx, gy, gn, BRICK_FORT, PLASTER, style="roman", out=3), "gates")
    gx, gy, gn = arc_point(Ex, 380, 390, -50, 0.75)
    m.add(1, fort_gate("south_gate", 26, 18, 14, gx, gy, gn, BRICK_FORT, PLASTER, style="roman", out=3))
    m.add(1, gatehouse("river_gate", 14, 9, 11, (Ex, 200, 0), "E", BRICK_FORT, PLASTER, style="roman"))
    p = []
    p.append(courtyard_ring("palace", 80, 90, 9, 12, (170, 20, 0.6), PLASTER, DARK))
    p.append(box("palace_court", 56, 66, 0.3, (170, 20, 0.6), LAWN))
    for sx in (-1, 1):
        for sy in (-1, 1):
            p.append(cylinder(f"palace_t{sx}{sy}", 4.5, 12, (170 + sx * 40, 20 + sy * 45, 0.6), shade(PLASTER, -0.08), verts=12))
            p.append(dome(f"palace_td{sx}{sy}", 4.5, (170 + sx * 40, 20 + sy * 45, 12.6), PLASTER, segments=12, rings=6))
    mq = kit_mosque("lodi_mosque", 44, 30, PLASTER, shade(PLASTER, -0.1), PLASTER, domes=3, court=False, style="sultanate", hall_depth=16)
    p.append(mv(mq, 40, 150, 0.6))
    p.append(courtyard_ring("stores", 60, 40, 6, 8, (60, -140, 0.6), BRICK, DARK))
    rnd = random.Random(5)
    p.append(box("tank", 30, 30, 0.9, (-40, -40, 0.6), WATER))
    p.append(box("tank_rim", 36, 36, 0.8, (-40, -40, 0.6), BRICK))
    for k, (cx_, cy_) in enumerate(((-20, 60), (80, -60), (-70, 160), (20, -220), (100, 140))):
        p.append(courtyard_ring(f"noble{k}", 34, 30, 5, 6, (cx_, cy_, 0.6), rnd.choice([PLASTER, BRICK]), DARK, inner_arcade=False))
    n = 0
    while n < 70:
        hx, hy = rnd.uniform(-140, 200), rnd.uniform(-330, 330)
        lim = Ex - 380 * max(0.0, 1 - (hy / 390) ** 2) ** 0.375 + 18
        busy = [(130, 210, -25, 65), (18, 62, 135, 165), (30, 90, -160, -120), (-58, -22, -58, -22), (-37, -3, 45, 75), (63, 97, -75, -45),
                (-87, -53, 145, 175), (3, 37, -235, -205), (83, 117, 125, 155)]
        if hx < lim or hx > Ex - 15 or any(a <= hx <= b and c <= hy <= d for a, b, c, d in busy):
            continue
        p.append(flat_house(f"h{n}", rnd.uniform(8, 16), rnd.uniform(8, 13), rnd.uniform(3.5, 5.5), (hx, hy, 0.6), rnd.choice([MUDBRICK, BRICK, PLASTER]), door_face=rnd.choice("SNEW")))
        n += 1
    for i in range(30):
        tx, ty = rnd.uniform(-140, 200), rnd.uniform(-320, 320)
        if tx > Ex - 380 * max(0.0, 1 - (ty / 390) ** 2) ** 0.375 + 15 and tx < Ex - 15:
            p.append(tree(f"t{i}", 3.8, (tx, ty, 0.6)))
    m.add(2, join(p, "palace"), "palace")
    return m


# ---------------------------------------------------------------- the city

def tripolia():
    m = Model("tripolia")
    m.add(0, box("ground", 100, 100, 0.3, (0, 0, 0), PAVE), "shops")
    out_p, in_p = oct_pts(50), oct_pts(36)
    m.add(0, ring_extrude("ring", out_p, in_p, 7, (0, 0, 0.3), shade(RED, 0.05)))
    m.add(0, ring_extrude("ring_top", oct_pts(50.4), oct_pts(35.6), 0.4, (0, 0, 7.3), shade(RED, 0.2)))
    m.add(0, ring_extrude("ring_edge", oct_pts(50.6), oct_pts(49.4), 0.9, (0, 0, 7.3), WHITE))
    apo_in = 36 * math.cos(math.pi / 8)
    side_in = 2 * 36 * math.sin(math.pi / 8)
    arcs = []
    for k in range(8):
        a = math.radians(45 * k)  # inner face centred on this direction; its arches face the centre
        fx, fy = (apo_in - 0.12) * math.cos(a), (apo_in - 0.12) * math.sin(a)
        ar = arcade(f"ia{k}", side_in * 0.9, 4.6, 5, (0, 0, 0.3), "S", RED_RECESS, True, 0.75, 0.3)
        arcs.append(mv(rz(ar, 45 * k - 90), fx, fy, 0))
    m.add(0, join(arcs, "inner_arcades"))
    m.add(1, box("tripolia_gate", 14, 30, 14, (-44, 0, 0.3), RED), "gates")
    g = [box("tg_top", 14.6, 30.6, 0.8, (-44, 0, 14.3), WHITE)]
    for k, yy in enumerate((-9, 0, 9)):
        g.append(niche(f"tg_a{k}", 6.5 if k != 1 else 7.5, 10 if k != 1 else 12, -44, yy, 0.3, -90, 7.05, DARK))
        g.append(niche(f"tg_b{k}", 6.5 if k != 1 else 7.5, 10 if k != 1 else 12, -44, yy, 0.3, 90, 7.05, DARK))
    for s in (-1, 1):
        g.append(oct_tower(f"tg_t{s}", 2.8, 17, -44, s * 15, 0.3, RED, WHITE, storeys=2, niches=False))
    for i in range(-2, 3):
        g.append(chhatri(f"tg_c{i}", 1.1, 3.8, (-44, i * 5, 15.1), WHITE, pillars=6))
    m.add(1, join(g, "tripolia"))
    m.add(1, mgate("fort_side", 16, 10, 10, (44, 0, 0.3), "E", RED, WHITE, 1))
    for s in (-1, 1):
        m.add(1, gatehouse(f"side{s}", 12, 10, 9, (0, s * 44, 0.3), "N" if s > 0 else "S", RED, WHITE, style="roman"))
    st = [box(f"stall{i}", 5, 3, 2.2, (12 * math.cos(math.tau * i / 10), 12 * math.sin(math.tau * i / 10), 0.3), "#C8A86A") for i in range(10)]
    m.add(2, join(st, "stalls"), "stalls")
    return m


def jama_masjid():
    m = Model("jama-masjid")
    W, D, P = 120, 95, 4.0
    mq = kit_mosque("jama", W, D, RED, WHITE, WHITE, domes=0, plinth=P, style="mughal")
    m.add(0, box("ground", W + 10, D + 16, 0.3, (0, 0, 0), PAVE), "plinth")
    m.add(0, mq)
    cells = []
    for f, L in (("S", W + 6), ("N", W + 6), ("E", D + 6), ("W", D + 6)):
        a = arcade(f"cells{f}", L * 0.94, P * 0.72, int(L / 5), (0, -(D + 6) / 2 - 0.05 if f in "SN" else -(W + 6) / 2 - 0.05, 0.2), "S", RED_RECESS, True, 0.7, 0.3)
        cells.append(rz(a, FACE[f]))
    m.add(0, join(cells, "plinth_cells"))
    hd = D * 0.28
    hall_h = max(8.0, min(W, D) * 0.14)
    hx = -W / 2 + hd / 2
    z = P + hall_h
    domes = []
    for i, (py, r) in enumerate(((0, 11.0), (-D * 0.27, 7.8), (D * 0.27, 7.8))):
        domes.append(chevron_dome(f"cd{i}", r, (hx - hd * 0.1, py, z), (RED, WHITE), height=1.5, bulb=1.14, drum=0.55))
    for sy in (-1, 1):
        for sx in (-1, 1):
            domes.append(chhatri(f"hc{sx}{sy}", 2.4, 7.0, (hx + sx * hd * 0.42, sy * D * 0.43, z), WHITE, pillars=6))
    for k, fy in enumerate((-37, -31, -25, -19, 19, 25, 31, 37)):
        domes.append(chhatri(f"fc{k}", 0.9, 3.2, (hx + hd / 2 - 1.0, fy, z), WHITE, pillars=6))
    m.add(1, join(domes, "domes"), "domes")
    return m


def kinari_bazaar():
    m = Model("kinari-bazaar")
    rnd = random.Random(12)
    m.add(0, box("lane", 7, 240, 0.35, (0, 0, 0), shade(PAVE, 0.12)), "shops")
    walls = ["#D9C3A0", "#C99E78", "#E3D3B6", "#B97F5E", "#CDB08A", "#E6DCC8"]
    houses, fronts, tops = [], [], []
    for s in (-1, 1):
        y = -118.0
        i = 0
        while y < 116:
            w = rnd.uniform(7, 12)
            if y + w > 118:
                w = 118 - y
            d = rnd.uniform(15, 19)
            h = rnd.choice([7.0, 8.5, 10.0, 11.5])
            col = rnd.choice(walls)
            x = s * (3.5 + d / 2 + 0.3)
            yc = y + w / 2
            houses.append(box(f"h{s}{i}", d, w - 0.3, h, (x, yc, 0), col))
            houses.append(box(f"hp{s}{i}", d + 0.2, w - 0.1, 0.7, (x, yc, h), shade(col, -0.1)))
            fx = s * 3.8
            ang = 90 if s < 0 else -90
            fronts.append(box(f"sh{s}{i}", 0.3, w * 0.7, 2.6, (fx, yc, 0.35), DARK))
            fronts.append(box(f"ch{s}{i}", 1.6, w * 0.9, 0.25, (s * (3.5 + 0.3 - 0.5), yc, 3.2), shade(col, -0.2)))
            if h > 8:
                fronts.append(box(f"jh{s}{i}", 1.4, w * 0.5, 2.4, (s * (3.5 + 0.3 - 0.4), yc, 4.4), shade(col, -0.12)))
                fronts.append(box(f"jhr{s}{i}", 1.8, w * 0.56, 0.3, (s * (3.5 + 0.3 - 0.4), yc, 6.8), shade(col, -0.25)))
            if rnd.random() < 0.45:
                fronts.append(box(f"aw{s}{i}", 2.4, w * 0.8, 0.12, (s * (3.5 - 0.6), yc, 2.9), rnd.choice(["#B34A3A", "#C9A24A", "#5E7FA0", "#D8C59A"])))
            if rnd.random() < 0.25:
                tops.append(chhatri(f"rc{s}{i}", 1.3, 3.6, (x, yc, h + 0.7), shade(col, 0.1), pillars=4))
            y += w
            i += 1
    m.add(0, join(houses, "houses"))
    for k in range(7):
        fronts.append(box(f"lane_awn{k}", 7.6, rnd.uniform(4, 7), 0.12, (0, -100 + 32 * k, rnd.uniform(4.6, 5.4)), ["#B34A3A", "#C9A24A", "#5E7FA0", "#D8C59A", "#8E5A8A", "#B34A3A", "#C9A24A"][k]))
    m.add(1, join(fronts, "shopfronts"), "fronts")
    m.add(2, join(tops, "roofs"), "roofs")
    return m


def mubarak_manzil():
    m = Model("mubarak-manzil")
    m.add(0, box("terrace", 60, 50, 1.2, (0, 0, 0), shade(RED, 0.3)), "body")
    m.add(0, box("body", 44, 34, 13, (0, -2, 1.2), PLASTER_W))
    m.add(0, box("band", 44.6, 34.6, 0.7, (0, -2, 7.2), RED))
    m.add(0, box("par", 44.8, 34.8, 1.0, (0, -2, 14.2), shade(PLASTER_W, -0.1)))
    arcs = []
    for f, L, dd in (("S", 44, 17), ("N", 44, 17), ("E", 34, 22), ("W", 34, 22)):
        for k, zz in enumerate((1.2, 7.9)):
            a = arcade(f"a{f}{k}", L * 0.78, 5.0, 5 if f in "SN" else 4, (0, -dd - 0.05, zz), "S", DARK, True, 0.65, 0.3)
            arcs.append(mv(rz(a, FACE[f]), 0, -2, 0))
    m.add(1, join(arcs, "arcades"), "arcades")
    tw = []
    for sx in (-1, 1):
        for sy in (-1, 1):
            tw.append(oct_tower(f"t{sx}{sy}", 3.6, 16.5, sx * 22, -2 + sy * 17, 1.2, PLASTER_W, PLASTER_W, storeys=2, chhatri_cap=False, niches=False, dome_cap=PLASTER_W))
    tw.append(chhatri("roof_ch", 3.0, 7.0, (0, -2, 15.2), PLASTER_W, pillars=8))
    m.add(2, join(tw, "towers"), "towers")
    return m


def riverfront_house(name, W, D, river="E", seed=1, scale=1.0):
    """A noble's riverfront haveli: town court, hall court, garden and a river terrace with towers (built with the river to the east)."""
    m = Model(name)
    rnd = random.Random(seed)
    m.add(0, box("ground", W, D, 0.3, (0, 0, 0), GROUND), "courts")
    m.add(0, wall_run("wall", [(W / 2 - 14, D / 2), (-W / 2, D / 2), (-W / 2, -D / 2), (W / 2 - 14, -D / 2)], 6, 1.6, (0, 0, 0), PLASTER_W, towers=False, merlon="round"))
    m.add(0, courtyard_ring("town_court", W * 0.32, D * 0.42, 7, 6, (-W * 0.31, -D * 0.24, 0), PLASTER_W, DARK))
    m.add(0, courtyard_ring("hall_court", W * 0.4, D * 0.44, 10, 8, (-W * 0.18, D * 0.24, 0), shade(PLASTER_W, -0.04), DARK))
    m.add(0, mgate("gate", 12, 8, 9, (-W / 2 + 2, -D * 0.24, 0), "W", RED, WHITE, 1))
    m.add(1, garden_quarters("garden", -W * 0.1, W / 2 - 16, -D / 2 + 3, D * 0.0 + 2, walk=4, sub=False, trees=2, tree_r=2.6, seed=seed), "garden")
    # river terrace with a pavilion and two towers
    tx = W / 2 - 8
    m.add(2, box("terrace", 16, D, 4.0, (tx, 0, 0), RED), "river terrace")
    m.add(2, arcade("terrace_arc", D * 0.9, 3.0, int(D / 6), (tx + 8.05, 0, 0.3), "E", RED_RECESS, True, 0.7, 0.3))
    m.add(2, box("pav", 10, 22, 6.5, (tx - 1, D * 0.12, 4.0), PLASTER_W))
    m.add(2, box("pav_roof", 11, 23, 0.6, (tx - 1, D * 0.12, 10.5), RED))
    m.add(2, arcade("pav_arc", 20, 4.8, 5, (tx + 4.05, D * 0.12, 4.0), "E", DARK, True, 0.75, 0.3))
    m.add(2, bangla_roof("pav_bangla", 10, 6, 3.0, (tx - 1, D * 0.12, 11.1), shade(PLASTER_W, -0.05)))
    for s in (-1, 1):
        m.add(2, oct_tower(f"rt{s}", 4.2, 12, tx + 2, s * (D / 2 - 5), 0, PLASTER_W, WHITE, storeys=2, niches=False))
    return m


def dara_shikoh_haveli():
    return riverfront_house("dara-shikoh-haveli", 90, 110, seed=4)


def riverfront_haveli():
    m = riverfront_house("riverfront-haveli", 80, 100, seed=9)
    # built with the river to the east; turn so the river terrace faces north
    for st in m.stages.values():
        for o in st:
            rz(o, 90)
    return m


def ghats():
    m = Model("ghats")
    W, D = 30, 120
    n = 9
    # steps rise toward the west (town); the lowest is at the river on the east
    steps = [box(f"st{i}", W - W * i / n, D, 4.0 * (i + 1) / n - 4.0 * i / n, (-W * i / n / 2, 0, 4.0 * i / n), shade(BUFF_SANDSTONE, -0.06 * (i % 2))) for i in range(n)]
    m.add(0, join(steps, "steps"), "steps")
    m.add(0, box("landing", 8, D, 4.0, (-W / 2 + 4, 0, 0), shade(BUFF_SANDSTONE, -0.04)))
    m.add(0, box("landing_wall", 2, D, 5.2, (-W / 2 + 1, 0, 0), BUFF_SANDSTONE))
    for s in (-1, 1):
        m.add(0, box(f"div{s}", W, 3.5, 4.4, (0, s * 22, 0), shade(BUFF_SANDSTONE, -0.1)))
    m.add(1, shikhara_temple("shrine_n", 3.4, 9.0, (-10, 40, 4.0), BUFF_SANDSTONE, mandapa=False), "shrines")
    m.add(1, shikhara_temple("shrine_s", 2.8, 7.5, (-10, -45, 4.0), WHITE, mandapa=False))
    m.add(1, chhatri("chhatri", 3.2, 8.0, (-10, 0, 4.0), BUFF_SANDSTONE, pillars=8, base=0.6))
    for k in range(5):
        m.add(1, box(f"slab{k}", 2.0, 1.2, 0.5, (12, -50 + 22 * k, 0.5), GRANITE))
        m.add(1, box(f"cloth{k}", 3.0, 0.1, 1.6, (6, -46 + 22 * k, 1.0), ["#F0EBE0", "#B34A3A", "#5E7FA0", "#E0C060", "#F0EBE0"][k]))
    return m


def akbars_church():
    m = Model("akbars-church")
    m.add(0, box("yard", 30, 50, 0.3, (0, 0, 0), GROUND), "church")
    m.add(0, wall_run("wall", [(-15, -25), (-15, 25), (15, 25), (15, -25), (4, -25)], 2.2, 0.7, (0, 0, 0), WHITEWASH, towers=False, merlon=None))
    m.add(0, box("nave", 13, 32, 9, (0, 2, 0), WHITEWASH))
    m.add(0, box("nave_roof", 13.6, 32.6, 0.6, (0, 2, 9), shade(WHITEWASH, -0.12)))
    m.add(0, box("apse", 9, 6, 7.5, (0, 21, 0), WHITEWASH))
    m.add(1, box("front", 15, 2, 12, (0, -14.5, 0), shade(WHITEWASH, -0.03)), "front")
    m.add(1, prism("pediment", [(-7.5, 0), (7.5, 0), (0, 4.2)], 2, (0, -15.5, 0), shade(WHITEWASH, -0.03)))
    ped = m.stages[1][-1]
    for v in ped.data.vertices:  # stand the triangle up on the facade
        x, y, z = v.co.x, v.co.y, v.co.z
        v.co.x, v.co.y, v.co.z = x, -15.5 + z, 12 + (y + 15.5)
    ped.data.update()
    m.add(1, arch_panel("door", 3.4, 5.5, (0, -15.55, 0), "S", DARK, False))
    m.add(1, cylinder("rose", 1.6, 0.3, (0, -15.7, 8.6), DARK, verts=16))
    m.stages[1][-1].rotation_euler[0] = math.pi / 2
    for s in (-1, 1):
        for k in range(3):
            m.add(1, arch_panel(f"win{s}{k}", 1.6, 3.6, (s * 6.55, -6 + 9 * k, 4.0), "E" if s > 0 else "W", DARK, False, 0.2))
    m.add(2, box("bellcote", 4, 1.6, 4.2, (0, -14.5, 15.4), WHITEWASH), "bell")
    m.add(2, arch_panel("bell_open", 2.2, 2.6, (0, -15.35, 16.0), "S", DARK, False, 0.2))
    m.add(2, box("cross_v", 0.4, 0.4, 2.6, (0, -14.5, 19.6), TIMBER))
    m.add(2, box("cross_h", 1.6, 0.4, 0.4, (0, -14.5, 21.2), TIMBER))
    m.add(2, tree("tamarind", 4.5, (9, 14, 0.3)))
    return m


def humayun_mosque():
    m = Model("humayun-mosque")
    m.add(0, box("platform", 24, 40, 1.0, (0, 0, 0), shade(PLASTER, -0.08)), "hall")
    m.add(0, box("hall", 13, 34, 8.5, (-4, 0, 1.0), PLASTER))
    m.add(0, box("par", 13.4, 34.4, 0.6, (-4, 0, 9.5), shade(PLASTER, -0.1)))
    m.add(1, pishtaq("pish", 12, 14, 2.5, 0, 1.0, 90, 0.0, PLASTER, shade(PLASTER, -0.12), "#6E6252", DARK, 1.4, True), "arches")
    for s in (-1, 1):
        for k, by in enumerate((9.5, 14.5)):
            m.add(1, niche(f"a{s}{k}", 3.6, 6.0, 2.55, s * by, 1.0, 90, 0, DARK))
        m.add(1, cylinder(f"turret{s}", 0.9, 11.5, (2.0, s * 17, 1.0), PLASTER, verts=8, r_top=0.6))
    m.add(2, cylinder("drum", 5.2, 2.2, (-4.5, 0, 10.1), PLASTER, verts=24), "dome")
    m.add(2, shallow_dome("dome", 5.4, (-4.5, 0, 12.3), PLASTER, rise=0.9, finial=True))
    for s in (-1, 1):
        m.add(2, shallow_dome(f"sdome{s}", 3.0, (-4.5, s * 11, 10.1), PLASTER, rise=0.6))
    return m


# ---------------------------------------------------------------- the east bank

def itimad_ud_daulah():
    m = Model("itimad-ud-daulah")
    G = 165
    m.add(0, box("ground", G, G, 0.3, (0, 0, 0), GROUND), "garden")
    m.add(0, wall_run("wall", [(-G / 2, -G / 2), (G / 2, -G / 2), (G / 2, G / 2), (-G / 2, G / 2), (-G / 2, -G / 2)], 5, 2.0, (0, 0, 0), RED, towers=False, merlon="round"))
    for sx in (-1, 1):
        for sy in (-1, 1):
            m.add(0, oct_tower(f"ct{sx}{sy}", 4.0, 9, sx * G / 2, sy * G / 2, 0, RED, WHITE, storeys=1, niches=False))
    m.add(0, garden_quarters("bagh", -G / 2 + 3, G / 2 - 3, -G / 2 + 3, G / 2 - 3, walk=9, sub=False, trees=3, tree_r=3.0, seed=21))
    # east gate, false gates north and south, river pavilion west
    m.add(1, box("egate", 12, 22, 11, (G / 2 - 6, 0, 0), RED), "gates")
    m.add(1, pishtaq("egate_p", 12, 12.5, G / 2 - 6, 0, 0, 90, 6.0, RED, WHITE, RED_RECESS, DARK, 1.0, False))
    m.add(1, pishtaq("egate_pi", 12, 12.5, G / 2 - 6, 0, 0, -90, 6.0, RED, WHITE, RED_RECESS, DARK, 1.0, False))
    for s in (-1, 1):
        m.add(1, oct_tower(f"egt{s}", 2.0, 13, G / 2 - 1.5, s * 11, 0, RED, WHITE, storeys=2, niches=False))
        m.add(1, box(f"fgate{s}", 20, 12, 9, (0, s * (G / 2 - 6), 0), RED))
        m.add(1, pishtaq(f"fgate_p{s}", 11, 10, 0, s * (G / 2 - 6), 0, 180 if s > 0 else 0, 6.0, RED, WHITE, RED_RECESS, RED_RECESS, 1.0, False))
    m.add(1, box("rpav_terr", 14, 40, 2.0, (-G / 2 + 7, 0, 0), RED_LT))
    m.add(1, box("rpav", 10, 26, 6.5, (-G / 2 + 7, 0, 2.0), RED))
    m.add(1, arcade("rpav_a", 22, 4.5, 3, (-G / 2 + 12.05, 0, 2.0), "E", RED_RECESS))
    m.add(1, box("rpav_roof", 11, 27, 0.6, (-G / 2 + 7, 0, 8.5), WHITE))
    # the tomb
    t = []
    t.append(box("plat", 50, 50, 1.2, (0, 0, 0.3), RED_LT))
    t.append(box("plat_inlay", 44, 44, 1.25, (0, 0, 0.3), shade(RED, 0.4)))
    t.append(box("body", 21, 21, 7.6, (0, 0, 1.5), INLAY))
    t.append(box("body_band", 21.4, 21.4, 0.6, (0, 0, 8.5), WHITE))
    for f in ("S", "N", "E", "W"):
        for k, (dx, w, h) in enumerate(((-6.0, 3.0, 4.6), (0, 4.6, 6.0), (6.0, 3.0, 4.6))):
            n = arch_panel(f"tarc{f}{k}", w, h, (dx, -10.55, 1.5), "S", "#6F6455", True, 0.3)
            t.append(rz(n, FACE[f]))
    t.append(jali_wall("jali_s", 18, 1.6, (0, -9, 9.1), "S", WHITE, 6))
    t.append(jali_wall("jali_n", 18, 1.6, (0, 9, 9.1), "N", WHITE, 6))
    t.append(jali_wall("jali_e", 18, 1.6, (9, 0, 9.1), "E", WHITE, 6))
    t.append(jali_wall("jali_w", 18, 1.6, (-9, 0, 9.1), "W", WHITE, 6))
    t.append(box("roof", 21, 21, 0.3, (0, 0, 9.1), WHITE_LINE))
    m.add(2, join(t, "tomb"), "tomb")
    up = []
    for sx in (-1, 1):
        for sy in (-1, 1):
            up.append(prism(f"tw{sx}{sy}", oct_pts(2.3), 12.5, (sx * 10.5, sy * 10.5, 1.5), INLAY))
            up.append(prism(f"twb{sx}{sy}", oct_pts(2.6), 0.4, (sx * 10.5, sy * 10.5, 9.0), WHITE))
            up.append(chhatri(f"twc{sx}{sy}", 2.0, 5.0, (sx * 10.5, sy * 10.5, 14.0), WHITE, pillars=8))
    up.append(box("pavilion", 9, 9, 4.2, (0, 0, 9.4), INLAY))
    for f in ("S", "N", "E", "W"):
        up.append(rz(arch_panel(f"pav_a{f}", 2.6, 3.2, (0, -4.55, 9.4), "S", "#6F6455", True, 0.25), FACE[f]))
    up.append(box("pav_eave", 10.6, 10.6, 0.35, (0, 0, 13.6), WHITE))
    up.append(frustum("pav_roof", 10.0, 10.0, 2.0, 2.0, 2.8, (0, 0, 13.95), WHITE))
    up.append(box("pav_ridge", 2.4, 2.4, 0.4, (0, 0, 16.75), WHITE_LINE))
    for sx in (-1, 1):
        for sy in (-1, 1):
            up.append(kalash(f"pav_k{sx}{sy}", 1.2, (sx * 4.9, sy * 4.9, 13.95)))
    up.append(kalash("pav_fin", 2.2, (0, 0, 17.1)))
    m.add(3, join(up, "towers"), "towers")
    return m


def chini_ka_rauza():
    m = Model("chini-ka-rauza")
    m.add(0, box("ground", 70, 70, 0.3, (0, 0, 0), GROUND), "terrace")
    m.add(0, box("terrace", 56, 56, 1.6, (0, 0, 0), shade(BRICK, 0.15)))
    m.add(0, prism("body", chamfer_pts(30, 4.5), 13, (0, 0, 1.6), "#C79A6B"))
    tiles = []
    S, C = 30, 4.5
    for f in ("S", "N", "E", "W"):
        ang = FACE[f]
        tiles.append(pishtaq(f"p{f}", 13, 15, 0, 0, 1.6, ang, S / 2, GLAZE_BLUE, TILE_GOLD, "#23465F", DARK, 0.8, False, GLAZE_TURQ))
        for s in (-1, 1):
            for k, zz in enumerate((2.0, 8.0)):
                pnl = box(f"tp{f}{s}{k}", 3.4, 0.3, 4.8, (s * 8.6, -S / 2 - 0.15, 1.6 + zz), [GLAZE_TURQ, TILE_GOLD, "#C8743A", "#5F8A5A"][(k + (s > 0)) % 4])
                tiles.append(rz(pnl, ang))
                tiles.append(rz(arch_panel(f"tn{f}{s}{k}", 2.2, 3.8, (s * 8.6, -S / 2 - 0.35, 1.6 + zz + 0.4), "S", "#2F3A44", True, 0.2), ang))
    dch = (S / 2 - C / 2) * math.sqrt(2)
    for k, ang in enumerate((45, 135, -135, -45)):
        tiles.append(niche(f"cn{k}", 3.4, 8, 0, 0, 2.6, ang, dch + 0.05, GLAZE_TURQ))
    tiles.append(prism("frieze", chamfer_pts(30.6, 4.7), 1.2, (0, 0, 13.0), GLAZE_TURQ))
    for k, (vx, vy) in enumerate(chamfer_pts(S, C)):
        tiles.append(cylinder(f"gul{k}", 0.3, 16.0, (vx * 1.005, vy * 1.005, 1.6), "#B88A5C", verts=6))
    m.add(1, join(tiles, "tilework"), "tiles")
    m.add(2, cylinder("drum", 9.0, 5.5, (0, 0, 14.2), "#C79A6B", verts=32), "dome")
    m.add(2, cylinder("drum_band", 9.2, 1.2, (0, 0, 17.5), GLAZE_BLUE, verts=32))
    m.add(2, onion_dome("dome", 9.0, (0, 0, 19.7), "#BFA584", bulb=1.1, height=1.25, drum=0.1))
    return m


def aram_bagh():
    m = Model("aram-bagh")
    W, D = 220, 260
    m.add(0, box("ground", W, D, 0.3, (0, 0, 0), GROUND), "walls")
    m.add(0, wall_run("wall", [(-W / 2 + 4, D / 2), (W / 2, D / 2), (W / 2, -D / 2), (-W / 2 + 4, -D / 2)], 5.5, 2.2, (0, 0, 0), RED, towers=False, merlon="round"))
    m.add(0, box("riverwall", 6, D, 4.5, (-W / 2 + 3, 0, 0), RED_DK))
    for s in (-1, 1):
        m.add(0, oct_tower(f"rt{s}", 6.5, 15, -W / 2 + 4, s * (D / 2 - 6), 0, RED, PLASTER_W, storeys=2))
        m.add(0, oct_tower(f"lt{s}", 3.8, 8, W / 2, s * D / 2, 0, RED, PLASTER_W, storeys=1, niches=False))
    m.add(0, mgate("egate", 16, 10, 10, (W / 2 - 3, 0, 0), "E", RED, PLASTER_W, 1))
    # terraced garden (upper terrace by the river, garden stepping east)
    m.add(1, box("terrace", 40, D - 8, 3.0, (-W / 2 + 26, 0, 0), shade(RED, 0.3)), "garden")
    m.add(1, garden_quarters("bagh", -W / 2 + 46, W / 2 - 4, -D / 2 + 4, D / 2 - 4, walk=9, sub=True, trees=2, tree_r=3.4, seed=17, cypress=False))
    m.add(1, join([box(f"chadar{k}", 3, 2.4, 3.0 - k * 0.6, (-W / 2 + 46 + k * 2.4, 0, 0), WATER) for k in range(5)], "cascade"))
    m.add(2, box("tank", 22, 22, 3.3, (-W / 2 + 24, 0, 0), WATER), "pavilions")
    m.add(2, box("tank_rim", 26, 26, 3.15, (-W / 2 + 24, 0, 0), PLASTER_W))
    for s in (-1, 1):
        y = s * 34
        p = [box(f"pav{s}", 16, 26, 7.5, (-W / 2 + 24, y, 3.0), PLASTER_W), box(f"pavr{s}", 17, 27, 0.7, (-W / 2 + 24, y, 10.5), RED)]
        p.append(arcade(f"pava{s}", 22, 5.5, 3, (-W / 2 + 24, y - s * 13.05, 3.0), "S" if s > 0 else "N", DARK))
        p.append(arcade(f"pave{s}", 22, 5.5, 3, (-W / 2 + 32.05, y, 3.0), "E", DARK))
        for sx in (-1, 1):
            for sy in (-1, 1):
                p.append(chhatri(f"pc{s}{sx}{sy}", 1.5, 4.5, (-W / 2 + 24 + sx * 6, y + sy * 10.5, 11.2), PLASTER_W, pillars=6))
        m.add(2, join(p, f"pavilion{s}"))
    return m


def zohra_bagh():
    m = Model("zohra-bagh")
    W, D = 150, 170
    m.add(0, box("ground", W, D, 0.3, (0, 0, 0), GROUND), "walls")
    m.add(0, wall_run("wall", [(-W / 2 + 3, D / 2), (W / 2, D / 2), (W / 2, -D / 2), (-W / 2 + 3, -D / 2)], 5, 2.0, (0, 0, 0), RED, towers=False, merlon="round"))
    m.add(0, box("riverwall", 5, D, 4, (-W / 2 + 2.5, 0, 0), RED_DK))
    for s in (-1, 1):
        m.add(0, oct_tower(f"rt{s}", 5.0, 12, -W / 2 + 3, s * (D / 2 - 5), 0, RED, PLASTER_W, storeys=2, niches=False))
    m.add(0, mgate("egate", 14, 9, 9, (W / 2 - 3, 0, 0), "E", RED, PLASTER_W, 1))
    m.add(1, garden_quarters("bagh", -W / 2 + 34, W / 2 - 3, -D / 2 + 3, D / 2 - 3, walk=8, sub=True, trees=2, tree_r=3.2, seed=33), "garden")
    m.add(2, box("terrace", 30, 64, 2.5, (-W / 2 + 18, 0, 0), shade(RED, 0.25)), "pavilion")
    m.add(2, box("pavilion", 22, 46, 13, (-W / 2 + 18, 0, 2.5), "#B98A66"))
    m.add(2, box("pav_band", 22.6, 46.6, 0.7, (-W / 2 + 18, 0, 8.6), RED))
    m.add(2, box("pav_par", 22.8, 46.8, 1.0, (-W / 2 + 18, 0, 15.5), RED_DK))
    for k, zz in enumerate((2.5, 9.3)):
        m.add(2, arcade(f"pav_a{k}", 42, 5.6, 7, (-W / 2 + 29.05, 0, zz), "E", DARK, True, 0.7, 0.3))
        m.add(2, arcade(f"pav_w{k}", 42, 5.6, 7, (-W / 2 + 6.95, 0, zz), "W", DARK, True, 0.6, 0.3))
    for sy in (-1, 1):
        m.add(2, chhatri(f"pav_c{sy}", 2.2, 6.0, (-W / 2 + 18, sy * 18, 16.5), PLASTER_W, pillars=6))
    return m


def jaswant_singh_chhatri():
    m = Model("jaswant-singh-chhatri")
    m.add(0, box("ground", 30, 30, 0.3, (0, 0, 0), GROUND), "enclosure")
    walls = []
    for f in ("S", "N", "E", "W"):
        jw = jali_wall(f"jw{f}", 28, 1.8, (0, 0, 0.3), "S", RED, 7)
        walls.append(mv(rz(mv(jw, 0, -14, 0), FACE[f]), 0, 0, 0))
    m.add(0, join(walls, "screens"))
    m.add(0, box("plinth1", 14, 14, 1.2, (0, 0, 0.3), RED_LT))
    m.add(0, box("plinth2", 11.5, 11.5, 1.0, (0, 0, 1.5), RED))
    pil = []
    for i in range(4):
        for j in range(4):
            if 0 < i < 3 and 0 < j < 3:
                continue
            px, py = -4.2 + 2.8 * i, -4.2 + 2.8 * j
            pil.append(box(f"p{i}{j}", 0.7, 0.7, 4.8, (px, py, 2.5), RED))
            pil.append(box(f"pc{i}{j}", 1.1, 1.1, 0.4, (px, py, 7.0), RED_DK))
    m.add(1, join(pil, "pillars"), "pillars")
    m.add(1, box("beam", 10, 10, 0.8, (0, 0, 7.3), RED))
    m.add(1, frustum("chhajja", 12.4, 12.4, 10.0, 10.0, 0.6, (0, 0, 7.7), RED_DK))
    m.add(2, frustum("drum", 9.6, 9.6, 7.6, 7.6, 1.4, (0, 0, 8.3), RED), "dome")
    m.add(2, ribbed_dome("dome", 3.8, (0, 0, 9.7), RED, height=1.2, ribs=12, drum=0.2, drum_color=RED))
    for sx in (-1, 1):
        for sy in (-1, 1):
            m.add(2, chhatri(f"ck{sx}{sy}", 0.9, 2.8, (sx * 4.3, sy * 4.3, 8.3), RED, pillars=4))
    return m


BUILDERS = {
    "agra/taj-mahal": taj_mahal,
    "agra/taj-mahal-1780": lambda: taj_mahal(neglect=True),
    "agra/taj-ganj": taj_ganj,
    "agra/mehtab-bagh": mehtab_bagh,
    "agra/agra-fort": agra_fort,
    "agra/agra-fort-1580": lambda: agra_fort("1580"),
    "agra/badalgarh": badalgarh,
    "agra/tripolia": tripolia,
    "agra/jama-masjid": jama_masjid,
    "agra/kinari-bazaar": kinari_bazaar,
    "agra/mubarak-manzil": mubarak_manzil,
    "agra/dara-shikoh-haveli": dara_shikoh_haveli,
    "agra/ghats": ghats,
    "agra/riverfront-haveli": riverfront_haveli,
    "agra/akbars-church": akbars_church,
    "agra/humayun-mosque": humayun_mosque,
    "agra/itimad-ud-daulah": itimad_ud_daulah,
    "agra/chini-ka-rauza": chini_ka_rauza,
    "agra/aram-bagh": aram_bagh,
    "agra/zohra-bagh": zohra_bagh,
    "agra/jaswant-singh-chhatri": jaswant_singh_chhatri,
}
