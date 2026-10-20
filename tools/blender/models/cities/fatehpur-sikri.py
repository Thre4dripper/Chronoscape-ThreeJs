"""Fatehpur Sikri landmark miniatures: Babur's garden at Sikri, Akbar's red sandstone capital (1571-85)
and the court-less city of Jahangir's day. Helpers for stairs, kiosks, octagons and arcaded blocks
follow tools/blender/models/cities/delhi.py."""
import math
import random
import bpy
from chronokit import Model, box, cylinder, dome, join, shade, gable_roof, hip_roof, mesh_from
from worldkit import *

SIKRI = "#A9583F"                       # the ridge's own red sandstone, quarried on the spot
SIKRI_LT = shade(SIKRI, 0.12)
SIKRI_DK = shade(SIKRI, -0.08)
PAVE = shade(SIKRI, 0.32)
ROCK = "#8E6A55"
BUFF = "#D9C3A0"                         # lime-plastered domes and stucco
TILE = "#4A86A8"                         # blue glazed roof tiles of Jodh Bai's palace
FACE_ROT = {"S": 0, "N": 180, "E": 90, "W": -90}


# ---------------------------------------------------------------- helpers (after delhi.py)

def turn(o, deg):
    """Rotate about the world Z axis (not the object's own origin) and apply."""
    bpy.context.scene.cursor.location = (0, 0, 0)
    bpy.ops.object.select_all(action="DESELECT")
    o.select_set(True)
    bpy.context.view_layer.objects.active = o
    bpy.ops.object.origin_set(type="ORIGIN_CURSOR")
    return rot(o, deg)


def stair_up(name, w, rise, run, n, x, y, side="S", color=SIKRI):
    """A flight of n steps on the `side` of a building: high end against the building edge at (x, y), running outward."""
    parts = []
    for i in range(n):
        dep = run * (n - i) / n
        parts.append(box(f"{name}{i}", w, dep, rise * (i + 1) / n, (0, -dep / 2, 0), color))
    o = turn(join(parts, name), FACE_ROT[side])
    return move(o, x, y, 0)


def chhajja(name, w, d, loc, over=1.0, h=0.5, color=SIKRI):
    """A thin sloping eave slab round a w x d block (wider at the top)."""
    return frustum(name, w, d, w + 2 * over, d + 2 * over, h, loc, color)


def oct_pts(r, start=math.pi / 8):
    return [(r * math.cos(start + i * math.pi / 4), r * math.sin(start + i * math.pi / 4)) for i in range(8)]


def oct_prism(name, r, h, loc=(0, 0, 0), color=SIKRI):
    return prism(name, oct_pts(r), h, loc, color)


def arcade_box(name, w, d, h, loc=(0, 0, 0), color=SIKRI, nx=5, ny=3, faces="SNEW", fill=0.7, ah=0.78, pointed=True, panel=DARK):
    x, y, z = loc
    parts = [box(name + "_b", w, d, h, loc, color)]
    for f in faces:
        if f in "SN":
            s = 1 if f == "N" else -1
            parts.append(arcade(f"{name}_a{f}", w * 0.94, h * ah, nx, (x, y + s * (d / 2 + 0.05), z), f, panel, pointed, fill))
        else:
            s = 1 if f == "E" else -1
            parts.append(arcade(f"{name}_a{f}", d * 0.94, h * ah, ny, (x + s * (w / 2 + 0.05), y, z), f, panel, pointed, fill))
    return join(parts, name)


def kiosk(name, r, h, loc, color=SIKRI_LT, dome_color=None):
    """A light four-pillared kiosk with a small dome."""
    x, y, z = loc
    parts = [box(f"{name}_p{i}", r * 0.24, r * 0.24, h * 0.5, (x + sx * r * 0.7, y + sy * r * 0.7, z), color) for i, (sx, sy) in enumerate(((-1, -1), (1, -1), (1, 1), (-1, 1)))]
    parts.append(box(name + "_eave", r * 2.3, r * 2.3, h * 0.08, (x, y, z + h * 0.5), color))
    parts.append(dome(name + "_d", r * 0.95, (x, y, z + h * 0.58), dome_color or color, squash=1.3, segments=10, rings=5))
    parts.append(cylinder(name + "_f", r * 0.08, h * 0.22, (x, y, z + h * 0.58 + r * 1.2), GILT, verts=5))
    return join(parts, name)


def kiosk_row(name, x0, y0, x1, y1, n, z, r=1.1, h=3.4, color=SIKRI_LT, dome_color=None):
    out = []
    for k in range(n):
        t = (k + 0.5) / n
        out.append(kiosk(f"{name}{k}", r, h, (x0 + (x1 - x0) * t, y0 + (y1 - y0) * t, z), color, dome_color))
    return join(out, name)


def vault(name, length, r, loc, color, n=10):
    """A half-cylinder barrel vault along X."""
    prof = [(r * math.cos(math.pi * i / n), r * math.sin(math.pi * i / n)) for i in range(n + 1)]
    verts = [(-length / 2, py, pz) for py, pz in prof] + [(length / 2, py, pz) for py, pz in prof]
    k = n + 1
    faces = [(i, i + 1, k + i + 1, k + i) for i in range(n)] + [tuple(range(k)), tuple(range(2 * k - 1, k - 1, -1))]
    return mesh_from(name, verts, faces, loc, color)


def colonnade(name, w, d, h, loc, color=SIKRI, step=2.4, faces="SNEW", r=0.22):
    """Square trabeate pillars round the edge of a w x d rectangle (the Fatehpur post-and-lintel verandah)."""
    x, y, z = loc
    out = []
    nx, ny = max(2, round(w / step) + 1), max(2, round(d / step) + 1)
    pts = set()
    for f in faces:
        if f in "SN":
            yy = y + (d / 2 if f == "N" else -d / 2)
            for i in range(nx):
                pts.add((round(x - w / 2 + w * i / (nx - 1), 3), round(yy, 3)))
        else:
            xx = x + (w / 2 if f == "E" else -w / 2)
            for j in range(ny):
                pts.add((round(xx, 3), round(y - d / 2 + d * j / (ny - 1), 3)))
    for i, (px, py) in enumerate(sorted(pts)):
        out.append(box(f"{name}{i}", r * 2, r * 2, h, (px, py, z), color))
    return join(out, name)


def parapet(name, w, d, z, h=0.8, t=0.3, loc=(0, 0), color=SIKRI):
    x, y = loc
    return join([box(name + "_s", w, t, h, (x, y - d / 2 + t / 2, z), color), box(name + "_n", w, t, h, (x, y + d / 2 - t / 2, z), color),
                 box(name + "_w", t, d, h, (x - w / 2 + t / 2, y, z), color), box(name + "_e", t, d, h, (x + w / 2 - t / 2, y, z), color)], name)


def trees(name, pts, r=2.5, color="#6F8A5C", z=0.0):
    return join([tree(f"{name}{i}", r, (x, y, z), color) for i, (x, y) in enumerate(pts)], name)


def city_gate(name, w=22, d=16, h=13, wall=19, color=SIKRI, trim=SIKRI_LT, wall_h=9):
    """A gate of the city wall: a gatehouse facing south with stubs of the crenellated wall to east and west."""
    parts = [gatehouse(name + "_g", w, d, h, (0, 0, 0), "S", color, trim)]
    for s in (-1, 1):
        parts.append(box(f"{name}_w{s}", wall, 4.5, wall_h, (s * (w / 2 + wall / 2), d * 0.15, 0), SIKRI_DK))
        n = int(wall / 2.2)
        for k in range(n):
            parts.append(box(f"{name}_m{s}{k}", 1.1, 4.0, 1.2, (s * (w / 2 + wall * (k + 0.5) / n), d * 0.15, wall_h), SIKRI_DK))
    return join(parts, name)


def elephant(name, loc, face_deg=0, color="#9A8A7C", plinth=2.5):
    """A stone elephant on a plinth, built facing -Y then turned by face_deg."""
    parts = [box(name + "_pl", 3.6, 6.2, plinth, (0, 0, 0), SIKRI_DK)]
    z = plinth
    parts.append(box(name + "_body", 2.6, 4.6, 2.5, (0, 0, z + 2.0), color))
    parts.append(box(name + "_back", 2.2, 3.6, 0.6, (0, 0.2, z + 4.5), color))
    for lx in (-0.8, 0.8):
        for ly in (-1.6, 1.6):
            parts.append(box(f"{name}_l{lx}{ly}", 0.8, 0.8, 2.1, (lx, ly, z), color))
    parts.append(box(name + "_head", 2.2, 1.6, 2.2, (0, -2.9, z + 2.7), color))
    parts.append(box(name + "_ears", 3.4, 0.3, 1.8, (0, -2.4, z + 2.8), color))
    parts.append(box(name + "_trunk", 0.6, 0.6, 2.6, (0, -3.9, z + 0.6), color))
    for sx in (-0.6, 0.6):
        parts.append(box(f"{name}_tusk{sx}", 0.25, 1.2, 0.25, (sx, -4.0, z + 2.0), MARBLE))
    o = turn(join(parts, name), face_deg)
    return move(o, *loc)


# ---------------------------------------------------------------- the Jama Masjid (qibla west)

def jama_masjid():
    m = Model("jama-masjid")
    W, D = 160, 140
    hall_x0, hall_x1 = -80, -45
    cx = (hall_x1 + 80) / 2                 # court centre x
    m.add(0, box("plate", W, D, 0.4, (0, 0, 0), ROCK), "court")
    m.add(0, box("pave", 124, 120, 0.25, (cx, 0, 0.4), PAVE))
    # cloister ranges on the north, south and east; the Buland Darwaza stands outside the south range at x = 18
    rh, rd = 9.0, 10.0
    m.add(0, box("range_s", 125, rd, rh, (cx, -D / 2 + rd / 2, 0), SIKRI))
    m.add(0, box("range_n", 125, rd, rh, (cx, D / 2 - rd / 2, 0), SIKRI))
    m.add(0, box("range_e", rd, D - 2 * rd, rh, (80 - rd / 2, 0, 0), SIKRI))
    m.add(0, arcade("arc_s", 120, rh * 0.7, 17, (cx, -D / 2 + rd + 0.05, 0.4), "N", DARK, True, 0.66))
    m.add(0, arcade("arc_n", 120, rh * 0.7, 17, (cx, D / 2 - rd - 0.05, 0.4), "S", DARK, True, 0.66))
    m.add(0, arcade("arc_e", D - 2 * rd - 4, rh * 0.7, 16, (80 - rd - 0.05, 0, 0.4), "W", DARK, True, 0.66))
    # outer faces: rows of blind arches
    m.add(0, arcade("out_n", 120, rh * 0.55, 20, (cx, D / 2 + 0.05, 0), "N", SIKRI_DK, True, 0.6))
    m.add(0, arcade("out_e", D - 10, rh * 0.55, 22, (80.05, 0, 0), "E", SIKRI_DK, True, 0.6))
    m.add(0, box("pool_rim", 9, 9, 0.6, (cx, -18, 0.4), SIKRI_LT))
    m.add(0, box("pool", 7, 7, 0.7, (cx, -18, 0.4), WATER))
    # rows of small chhatris along the cloister roofs
    m.add(1, kiosk_row("kn", hall_x1 + 4, D / 2 - rd / 2, 76, D / 2 - rd / 2, 14, rh, 1.15, 3.6), "kiosks and gates")
    m.add(1, kiosk_row("ks_w", hall_x1 + 4, -D / 2 + rd / 2, -6, -D / 2 + rd / 2, 6, rh, 1.15, 3.6))
    m.add(1, kiosk_row("ks_e", 44, -D / 2 + rd / 2, 76, -D / 2 + rd / 2, 4, rh, 1.15, 3.6))
    m.add(1, kiosk_row("ke_s", 80 - rd / 2, -D / 2 + 14, 80 - rd / 2, -14, 6, rh, 1.15, 3.6))
    m.add(1, kiosk_row("ke_n", 80 - rd / 2, 14, 80 - rd / 2, D / 2 - 14, 6, rh, 1.15, 3.6))
    # the Badshahi Darwaza (east, the emperor's gate) with its stair, and the inner face of the Buland Darwaza
    m.add(1, box("gate_e", 10, 26, 15, (75, 0, 0), SIKRI))
    m.add(1, iwan("gate_e_iw", 15, 18, 3, (80, 0, 0), "E", SIKRI, SIKRI_LT))
    m.add(1, iwan("gate_e_in", 12, 14, 2, (69.5, 0, 0.4), "W", SIKRI, SIKRI_LT))
    for k in (-1, 0, 1):
        m.add(1, kiosk(f"gate_e_c{k}", 1.6, 4.6, (75, k * 8, 15), SIKRI_LT, BUFF))
    m.add(1, iwan("bd_inner", 16, 15, 2, (18, -D / 2 + rd + 1, 0.4), "N", SIKRI, SIKRI_LT))
    m.add(1, box("gate_n", 18, 14, 12, (cx, D / 2 - 7, 0), SIKRI))
    m.add(1, iwan("gate_n_iw", 11, 13, 2, (cx, D / 2 + 1.5, 0), "N", SIKRI, SIKRI_LT))
    # the prayer hall on the west: arcaded wings and a tall central pishtaq
    hx, hd, hl, hh = (hall_x0 + hall_x1) / 2, hall_x1 - hall_x0, 132, 13
    m.add(2, box("hall", hd, hl, hh, (hx, 0, 0), SIKRI), "prayer hall")
    m.add(2, box("hall_plinth", hd + 2, hl + 2, 0.6, (hx, 0, 0), SIKRI_DK))
    for s in (-1, 1):
        m.add(2, arcade(f"hall_arc{s}", 50, hh * 0.66, 7, (hall_x1 + 0.05, s * 38, 0.4), "E", DARK, True, 0.72))
    m.add(2, chhajja("hall_ch", hd, hl, (hx, 0, hh - 0.6), 0.9, 0.5, SIKRI_LT))
    m.add(2, box("pish_back", 12, 30, 24, (hall_x1 - 4, 0, 0), SIKRI))
    m.add(2, iwan("pishtaq", 26, 26, 4, (hall_x1 + 1.5, 0, 0), "E", SIKRI, MARBLE))
    m.add(2, kiosk_row("hall_k_s", hall_x1 - 2, -62, hall_x1 - 2, -18, 5, hh, 1.2, 3.8))
    m.add(2, kiosk_row("hall_k_n", hall_x1 - 2, 18, hall_x1 - 2, 62, 5, hh, 1.2, 3.8))
    for sy in (-1, 1):
        m.add(2, kiosk(f"hall_corner{sy}", 2.4, 7.5, (hall_x0 + 4, sy * (hl / 2 - 4), hh), SIKRI_LT, BUFF))
    # three domes: the large one over the central chamber, two over the side chambers
    m.add(3, box("drum_c", 16, 16, 3, (hx - 2, 0, hh), SIKRI), "domes")
    m.add(3, onion_dome("dome_c", 7.6, (hx - 2, 0, hh + 3), BUFF, bulb=1.08, height=1.3, drum=0.35))
    for sy in (-1, 1):
        m.add(3, box(f"drum{sy}", 11, 11, 2, (hx - 2, sy * 32, hh), SIKRI))
        m.add(3, onion_dome(f"dome{sy}", 5.2, (hx - 2, sy * 32, hh + 2), BUFF, bulb=1.08, height=1.3, drum=0.35))
    return m


# ---------------------------------------------------------------- the Buland Darwaza

def buland_darwaza():
    m = Model("buland-darwaza")
    P = 10.0                                    # the ridge edge the gate stands on, reached by the great stair
    m.add(0, box("terrace", 46, 26, P, (0, 9, 0), ROCK), "terrace and steps")
    m.add(0, arcade("terrace_arc", 40, P * 0.6, 8, (0, -4.05, 0), "S", shade(ROCK, -0.25), True, 0.5))
    m.add(0, stair_up("steps", 30, P, 18, 26, 0, -4, "S", shade(SIKRI, 0.18)))
    for s in (-1, 1):
        m.add(0, frustum(f"cheek{s}", 4, 18, 3, 18, P, (s * 17, -13, 0), SIKRI_DK))
    z = P
    # the half-octagonal front: a 22 m central face, angled wings, sides running back to the mosque wall
    plan = [(-11, -2), (11, -2), (16.7, 3.7), (16.7, 22), (-16.7, 22), (-16.7, 3.7)]
    m.add(1, prism("body", plan, 30, (0, 0, z), SIKRI), "gate")
    m.add(1, box("pish_frame", 24, 4, 39, (0, -1.0, z), SIKRI))
    m.add(1, arch_panel("pish_arch", 15, 30, (0, -3.05, z), "S", DARK, True, 0.5))
    m.add(1, arch_panel("door", 5, 9, (0, -3.3, z), "S", "#1E1712", True, 0.4))
    # white marble inlay bands framing the pishtaq
    for s in (-1, 1):
        m.add(1, box(f"band_v{s}", 0.7, 0.4, 34.5, (s * 9.6, -3.05, z + 1), MARBLE))
    m.add(1, box("band_h", 20, 0.4, 0.8, (0, -3.05, z + 35), MARBLE))
    m.add(1, box("band_h2", 24.4, 0.4, 0.6, (0, -3.05, z + 38.2), MARBLE))
    # angled wings: arches in three tiers
    for s in (-1, 1):
        cxw, cyw = s * 13.85, 0.85
        for k, (zz, hh) in enumerate(((0, 11), (12.5, 7), (21, 6))):
            a = arch_panel(f"wing{s}{k}", 4.2, hh, (0, 0, 0), "S", DARK, True, 0.4)
            a = turn(a, s * 45)
            m.add(1, move(a, cxw + s * 0.1, cyw - 0.1, z + zz + 0.5))
        for k, zz in enumerate((0.5, 13, 21.5)):
            m.add(1, arch_panel(f"side{s}{k}", 5, 8 if k == 0 else 6, (s * 16.75, 12, z + zz), "E" if s > 0 else "W", DARK, True, 0.3))
    m.add(1, arch_panel("back", 10, 16, (0, 22.05, z), "N", DARK, True, 0.3))
    big = [(-11.4, -2.6), (11.4, -2.6), (17.3, 3.4), (17.3, 22.4), (-17.3, 22.4), (-17.3, 3.4)]
    m.add(1, prism("eave", big, 0.6, (0, 0, z + 29.2), SIKRI_LT))
    m.add(1, prism("parapet", plan, 1.2, (0, 0, z + 29.8), SIKRI))
    # crown: a row of small kiosks on the pishtaq, corner pinnacles, larger chhatris on the roof
    m.add(2, kiosk_row("crown", -11, -1.0, 11, -1.0, 11, z + 39, 0.85, 3.0, SIKRI_LT, BUFF), "chhatris")
    for s in (-1, 1):
        m.add(2, cylinder(f"pin{s}", 0.9, 41, (s * 12.6, -1.5, z), SIKRI_LT, verts=8, r_top=0.6))
        m.add(2, kiosk(f"pin_k{s}", 1.0, 3.2, (s * 12.6, -1.5, z + 41), SIKRI_LT, BUFF))
    for k, (cxk, cyk, r) in enumerate(((-9, 9, 2.6), (0, 11, 3.0), (9, 9, 2.6), (-13, 17, 2.0), (13, 17, 2.0))):
        m.add(2, chhatri(f"roof_ch{k}", r, r * 2.8, (cxk, cyk, z + 30.6), SIKRI_LT, BUFF, 8))
    return m


# ---------------------------------------------------------------- tombs in the mosque court

def salim_chishti_tomb():
    m = Model("salim-chishti-tomb")
    m.add(0, box("plinth", 18, 18, 1.0, (0, 0, 0), MARBLE), "plinth")
    m.add(0, box("plinth_band", 18.2, 18.2, 0.25, (0, 0, 0.75), "#D6CFC2"))
    z = 1.0
    S, H = 13.0, 5.2
    # the jali verandah round the tomb chamber
    m.add(1, box("core", S - 3, S - 3, H + 1.8, (0, 0, z), MARBLE), "screens")
    for f, (dx, dy) in (("S", (0, -S / 2)), ("N", (0, S / 2)), ("E", (S / 2, 0)), ("W", (-S / 2, 0))):
        m.add(1, jali_wall(f"jali{f}", S, H, (dx, dy, z), f, MARBLE, 6))
    m.add(1, box("lintel", S + 0.2, S + 0.2, 0.6, (0, 0, z + H), MARBLE))
    # the south porch
    m.add(1, box("porch_roof", 5.5, 3.2, 0.5, (0, -S / 2 - 1.6, z + H - 0.5), MARBLE))
    for s in (-1, 1):
        m.add(1, box(f"porch_p{s}", 0.5, 0.5, H - 0.5, (s * 2.4, -S / 2 - 2.9, z), MARBLE))
    m.add(1, arch_panel("door", 1.8, 3.4, (0, -S / 2 + 1.4, z), "S", DARK, True, 0.2))
    # the deep chhajja on serpentine brackets
    m.add(2, frustum("chhajja", S + 0.6, S + 0.6, S + 4.0, S + 4.0, 0.5, (0, 0, z + H + 0.4), MARBLE), "roof and dome")
    for f in "SNEW":
        for k in range(7):
            t = -S / 2 + 0.8 + k * (S - 1.6) / 6
            for j, (off, zz, hh) in enumerate(((0.45, z + H - 0.3, 0.6), (1.05, z + H + 0.05, 0.4))):
                x, y = {"S": (t, -S / 2 - off), "N": (t, S / 2 + off), "E": (S / 2 + off, t), "W": (-S / 2 - off, t)}[f]
                m.add(2, box(f"br{f}{k}{j}", 0.3 if f in "SN" else 0.9, 0.9 if f in "SN" else 0.3, hh, (x, y, zz), "#E2DCCF"))
    m.add(2, parapet("par", S + 0.6, S + 0.6, z + H + 0.9, 0.7, 0.3, (0, 0), MARBLE))
    m.add(2, box("drum", 8.2, 8.2, 1.2, (0, 0, z + H + 0.9), MARBLE))
    m.add(2, shallow_dome("dome", 3.8, (0, 0, z + H + 2.1), MARBLE, rise=0.95, drum=0.8, finial=True))
    for sx in (-1, 1):
        for sy in (-1, 1):
            m.add(2, cylinder(f"guld{sx}{sy}", 0.25, 2.2, (sx * (S / 2), sy * (S / 2), z + H + 0.9), MARBLE, verts=8, r_top=0.08))
    return m


def islam_khan_tomb():
    m = Model("islam-khan-tomb")
    m.add(0, box("plinth", 18, 18, 0.8, (0, 0, 0), SIKRI_DK), "plinth")
    z = 0.8
    S, H = 15.0, 5.0
    m.add(1, box("core", 10, 10, H + 2.5, (0, 0, z), SIKRI), "verandah")
    for f, (dx, dy) in (("S", (0, -S / 2)), ("N", (0, S / 2)), ("E", (S / 2, 0)), ("W", (-S / 2, 0))):
        m.add(1, jali_wall(f"jali{f}", S, H, (dx, dy, z), f, SIKRI, 5))
    m.add(1, arch_panel("door", 2.0, 3.6, (0, -S / 2 - 0.25, z), "S", DARK, True, 0.2))
    m.add(1, chhajja("ch", S, S, (0, 0, z + H), 0.9, 0.5, SIKRI_LT))
    m.add(1, box("roof", S, S, 0.6, (0, 0, z + H + 0.5), SIKRI))
    # 36 little chhatris round the roof edge, the tomb's mark
    zr = z + H + 1.1
    ring = []
    n = 10
    for k in range(n):
        t = -S / 2 + 0.7 + k * (S - 1.4) / (n - 1)
        for (x, y) in ((t, -S / 2 + 0.7), (t, S / 2 - 0.7)):
            ring.append((x, y))
        if 0 < k < n - 1:
            for (x, y) in ((-S / 2 + 0.7, t), (S / 2 - 0.7, t)):
                ring.append((x, y))
    for i, (x, y) in enumerate(ring):
        m.add(2, kiosk(f"k{i}", 0.5, 2.0, (x, y, zr), SIKRI_LT, SIKRI_LT), "dome and chhatris")
    m.add(2, box("drum", 9, 9, 1.5, (0, 0, zr), SIKRI))
    m.add(2, shallow_dome("dome", 4.3, (0, 0, zr + 1.5), SIKRI, rise=0.9, drum=1.0, finial=True))
    return m


# ---------------------------------------------------------------- the palace (Daulat Khana)

def diwan_i_khas():
    m = Model("diwan-i-khas")
    S = 14.0
    m.add(0, box("plinth", S + 2, S + 2, 1.2, (0, 0, 0), SIKRI_DK), "hall")
    z = 1.2
    H1, H2 = 5.4, 5.0
    m.add(0, box("lower", S, S, H1, (0, 0, z), SIKRI))
    m.add(0, box("upper", S, S, H2, (0, 0, z + H1), SIKRI))
    for f, (dx, dy) in (("S", (0, -S / 2)), ("N", (0, S / 2)), ("E", (S / 2, 0)), ("W", (-S / 2, 0))):
        sx, sy = (1, 0) if f in "SN" else (0, 1)
        m.add(0, arch_panel(f"door{f}", 2.6, 4.2, (dx * 1.005, dy * 1.005, z), f, DARK, False, 0.3))
        for s in (-1, 1):
            m.add(0, box(f"win{f}{s}", 1.3 if f in "SN" else 0.3, 0.3 if f in "SN" else 1.3, 2.0, (dx * 1.01 + s * sx * 4.3, dy * 1.01 + s * sy * 4.3, z + 1.2), DARK))
        for k in (-1, 0, 1):
            m.add(0, box(f"uwin{f}{k}", 1.2 if f in "SN" else 0.3, 0.3 if f in "SN" else 1.2, 2.2, (dx * 1.01 + k * sx * 3.6, dy * 1.01 + k * sy * 3.6, z + H1 + 1.3), DARK))
    # the balcony eave at mid-height and the deep roof chhajja
    m.add(1, chhajja("mid_ch", S, S, (0, 0, z + H1 - 0.2), 1.0, 0.4, SIKRI_LT), "eaves and kiosks")
    m.add(1, box("mid_rail", S + 1.6, S + 1.6, 0.5, (0, 0, z + H1 + 0.2), SIKRI))
    m.add(1, chhajja("roof_ch", S, S, (0, 0, z + H1 + H2 - 0.5), 1.4, 0.5, SIKRI_LT))
    m.add(1, parapet("par", S, S, z + H1 + H2, 0.9, 0.35, (0, 0), SIKRI))
    for sx in (-1, 1):
        for sy in (-1, 1):
            for j, zz in enumerate((z + H1 - 1.2, z + H1 + H2 - 1.5)):
                m.add(1, box(f"brk{sx}{sy}{j}", 0.5, 0.5, 1.0, (sx * (S / 2 + 0.25), sy * (S / 2 + 0.25), zz), SIKRI_DK))
    # four corner kiosks with domes
    zt = z + H1 + H2
    for sx in (-1, 1):
        for sy in (-1, 1):
            x, y = sx * (S / 2 - 1.3), sy * (S / 2 - 1.3)
            parts = [box(f"kp{sx}{sy}{i}", 0.35, 0.35, 2.6, (x + px * 0.95, y + py * 0.95, zt), SIKRI) for i, (px, py) in enumerate(((-1, -1), (1, -1), (1, 1), (-1, 1)))]
            parts.append(box(f"ke{sx}{sy}", 2.9, 2.9, 0.3, (x, y, zt + 2.6), SIKRI_LT))
            parts.append(box(f"kd{sx}{sy}", 2.1, 2.1, 0.6, (x, y, zt + 2.9), SIKRI))
            parts.append(onion_dome(f"kdome{sx}{sy}", 1.0, (x, y, zt + 3.5), SIKRI_LT, bulb=1.12, height=1.35, drum=0.2))
            m.add(2, join(parts, f"kiosk{sx}{sy}"), "corner kiosks")
    return m


def panch_mahal():
    m = Model("panch-mahal")
    m.add(0, box("plinth", 26, 18, 0.8, (0, 0, 0), SIKRI_DK), "ground storey")
    # (columns across, columns deep, bay x, bay y, storey height, centre x): 84, 56, 20, 12 and 4 pillars
    floors = [(12, 7, 2.2, 2.8, 3.6, 0.0), (8, 7, 2.2, 2.8, 3.3, 4.4), (5, 4, 2.2, 2.8, 3.0, 4.4), (4, 3, 2.2, 2.8, 2.8, 4.4)]
    z = 0.8
    for i, (nx, ny, bx, by, h, cx) in enumerate(floors):
        w, d = (nx - 1) * bx, (ny - 1) * by
        st = 0 if i == 0 else (1 if i < 3 else 2)
        cols = [box(f"c{i}_{a}_{b}", 0.4, 0.4, h, (cx - w / 2 + a * bx, -d / 2 + b * by, z), SIKRI) for a in range(nx) for b in range(ny)]
        m.add(st, join(cols, f"cols{i}"), ["ground storey", "upper storeys", "top"][st])
        m.add(st, box(f"beam{i}", w + 0.6, d + 0.6, 0.4, (cx, 0, z + h - 0.4), SIKRI_LT))
        m.add(st, chhajja(f"ch{i}", w + 0.6, d + 0.6, (cx, 0, z + h - 0.35), 0.6, 0.3, SIKRI_LT))
        m.add(st, box(f"slab{i}", w + 1.0, d + 1.0, 0.35, (cx, 0, z + h), SIKRI))
        z += h + 0.35
        # the screened parapet round the open roof of this storey
        m.add(st, parapet(f"par{i}", w + 1.0, d + 1.0, z, 0.8, 0.15, (cx, 0), SIKRI_DK))
    # the fifth storey: a four-pillared kiosk with a dome
    cx = 4.4
    parts = [box(f"top_p{i}", 0.4, 0.4, 2.6, (cx + px * 1.3, py * 1.3, z), SIKRI) for i, (px, py) in enumerate(((-1, -1), (1, -1), (1, 1), (-1, 1)))]
    parts.append(chhajja("top_ch", 3.0, 3.0, (cx, 0, z + 2.3), 0.6, 0.3, SIKRI_LT))
    parts.append(box("top_slab", 3.4, 3.4, 0.3, (cx, 0, z + 2.6), SIKRI))
    parts.append(onion_dome("top_dome", 1.5, (cx, 0, z + 2.9), SIKRI_LT, bulb=1.1, height=1.35, drum=0.3))
    m.add(2, join(parts, "top_kiosk"))
    return m


def anup_talao():
    m = Model("anup-talao")
    S, P = 36.0, 29.0
    m.add(0, box("court", S, S, 0.3, (0, 0, 0), PAVE), "tank")
    for name, (w, d, x, y) in {"s": (S, (S - P) / 2, 0, -(S + P) / 4), "n": (S, (S - P) / 2, 0, (S + P) / 4),
                               "w": ((S - P) / 2, P, -(S + P) / 4, 0), "e": ((S - P) / 2, P, (S + P) / 4, 0)}.items():
        m.add(0, box("walk_" + name, w, d, 1.0, (x, y, 0), SIKRI_LT))
    m.add(0, box("water", P, P, 0.35, (0, 0, 0), WATER))
    # balustrade round the edge, broken for the four causeways
    for f in "SNEW":
        for s in (-1, 1):
            L = P / 2 - 1.2
            c = s * (1.2 + L / 2)
            x, y, w, d = {"S": (c, -P / 2, L, 0.3), "N": (c, P / 2, L, 0.3), "E": (P / 2, c, 0.3, L), "W": (-P / 2, c, 0.3, L)}[f]
            m.add(1, box(f"rail{f}{s}", w, d, 0.8, (x, y, 1.0), SIKRI), "platform and causeways")
    # the central platform and its four narrow bridges
    m.add(1, box("platform", 8.5, 8.5, 1.3, (0, 0, 0), SIKRI_LT))
    m.add(1, parapet("plat_rail", 8.5, 8.5, 1.3, 0.7, 0.25, (0, 0), SIKRI))
    for f in "SNEW":
        L = (P - 8.5) / 2
        c = 4.25 + L / 2
        x, y, w, d = {"S": (0, -c, 1.8, L), "N": (0, c, 1.8, L), "E": (c, 0, L, 1.8), "W": (-c, 0, L, 1.8)}[f]
        m.add(1, box(f"bridge{f}", w, d, 0.4, (x, y, 0.6), SIKRI_LT))
        for k in range(3):
            t = -L / 2 + L * (k + 0.5) / 3
            bx, by = (x, y + t) if f in "SN" else (x + t, y)
            m.add(1, box(f"pier{f}{k}", 1.2 if f in "SN" else 0.6, 0.6 if f in "SN" else 1.2, 0.6, (bx, by, 0.0), SIKRI_DK))
    for sx in (-1, 1):
        for sy in (-1, 1):
            m.add(1, box(f"post{sx}{sy}", 0.6, 0.6, 1.2, (sx * 4.0, sy * 4.0, 1.3), SIKRI_LT))
    return m


def khwabgah():
    m = Model("khwabgah")
    m.add(0, box("plinth", 30, 22, 0.8, (0, 0, 0), SIKRI_DK), "lower storey")
    z = 0.8
    m.add(0, arcade_box("lower", 28, 20, 6.0, (0, 0, z), SIKRI, 7, 5, "SNEW", 0.6, 0.7, False))
    m.add(0, chhajja("lower_ch", 28, 20, (0, 0, z + 5.6), 0.9, 0.4, SIKRI_LT))
    m.add(0, parapet("lower_par", 28, 20, z + 6.0, 0.8, 0.3, (0, 0), SIKRI))
    m.add(0, box("roof", 28, 20, 0.2, (0, 0, z + 6.0), PAVE))
    z2 = z + 6.0
    # the emperor's sleeping chamber on the roof, ringed by a pillared verandah
    m.add(1, box("chamber", 7.5, 7.5, 4.6, (4, 2, z2), SIKRI), "the sleeping chamber")
    for f, (dx, dy) in (("S", (0, -3.75)), ("N", (0, 3.75)), ("E", (3.75, 0)), ("W", (-3.75, 0))):
        m.add(1, arch_panel(f"cw{f}", 1.6, 2.6, (4 + dx * 1.01, 2 + dy * 1.01, z2), f, DARK, False, 0.2))
    m.add(1, colonnade("ver", 11, 11, 3.6, (4, 2, z2), SIKRI, 2.2))
    m.add(1, chhajja("ver_ch", 11.4, 11.4, (4, 2, z2 + 3.4), 0.7, 0.3, SIKRI_LT))
    m.add(1, box("ver_roof", 11.8, 11.8, 0.3, (4, 2, z2 + 3.6), SIKRI))
    m.add(1, kiosk("stair_k", 1.4, 4.0, (-10, -6, z2), SIKRI_LT))
    m.add(2, box("ch_top", 7.6, 7.6, 0.4, (4, 2, z2 + 4.6), SIKRI_LT), "kiosk")
    m.add(2, chhatri("crown", 2.4, 6.0, (4, 2, z2 + 5.0), SIKRI_LT, BUFF, 8))
    return m


def jodh_bai_palace():
    m = Model("jodh-bai-palace")
    W, D, dep, h = 72.0, 68.0, 12.0, 9.0
    m.add(0, box("court_pave", W - 2 * dep, D - 2 * dep, 0.3, (0, 0, 0), PAVE), "walls")
    m.add(0, courtyard_ring("ring", W, D, h, dep, (0, 0, 0), SIKRI, DARK, inner_arcade=True))
    m.add(0, merlons("mer", W, D, h, 0.7, 1.3, SIKRI, "box"))
    m.add(0, box("tulsi", 3, 3, 1.2, (0, 0, 0.3), SIKRI_LT))
    # the east entrance: a projecting gate with its porch
    m.add(1, box("gate", 16, 14, 12, (W / 2 - 8, 0, 0), SIKRI), "gate and pavilions")
    m.add(1, iwan("gate_iw", 11, 11, 2.5, (W / 2 + 0.5, 0, 0), "E", SIKRI, SIKRI_LT))
    for s in (-1, 1):
        m.add(1, kiosk(f"gate_k{s}", 1.6, 4.4, (W / 2 - 6, s * 5, 12), SIKRI_LT, BUFF))
    # north and south pavilions with ridged roofs of blue glazed tile
    for sy in (-1, 1):
        y = sy * (D / 2 - dep / 2)
        m.add(1, box(f"pav{sy}", 22, dep, 13, (0, y, 0), SIKRI))
        m.add(1, arcade(f"pav_arc{sy}", 18, 4.4, 5, (0, y - sy * (dep / 2 + 0.05), h - 1.0), "N" if sy < 0 else "S", DARK, False, 0.6))
        m.add(2, vault(f"pav_roof{sy}", 23, 4.2, (0, y, 13), TILE, 10), "blue roofs and domes")
        m.add(2, box(f"pav_gable{sy}", 23.4, 8.8, 0.4, (0, y, 12.8), SIKRI_LT))
    # domed pavilions over the west range (the shrine side) and at the four corners
    m.add(1, box("west_pav", dep, 16, 12, (-W / 2 + dep / 2, 0, 0), SIKRI))
    m.add(2, chhatri("west_dome", 4.6, 11, (-W / 2 + dep / 2, 0, 12), SIKRI_LT, BUFF, 8))
    for sx in (-1, 1):
        for sy in (-1, 1):
            x, y = sx * (W / 2 - 5), sy * (D / 2 - 5)
            m.add(1, box(f"cor{sx}{sy}", 9, 9, 3.2, (x, y, h), SIKRI))
            m.add(2, shallow_dome(f"cor_d{sx}{sy}", 3.6, (x, y, h + 3.2), BUFF, rise=0.85, drum=0.4, finial=True))
    # the Hawa Mahal, a screened wind pavilion on the north side
    m.add(2, jali_wall("hawa", 10, 4, (-18, D / 2 - 0.5, h), "N", SIKRI_LT, 5))
    m.add(2, box("hawa_roof", 11, 4, 0.5, (-18, D / 2 - 2, h + 4), SIKRI_LT))
    return m


def birbal_house():
    m = Model("birbal-house")
    m.add(0, box("plinth", 20, 18, 1.0, (0, 0, 0), SIKRI_DK), "ground storey")
    z = 1.0
    m.add(0, box("ground", 16, 14, 6.5, (0, 0, z), SIKRI))
    for f, (dx, dy) in (("S", (0, -7)), ("N", (0, 7)), ("E", (8, 0)), ("W", (-8, 0))):
        sx, sy = (1, 0) if f in "SN" else (0, 1)
        for k in (-1, 1):
            m.add(0, arch_panel(f"d{f}{k}", 1.6, 3.4, (dx * 1.01 + k * sx * 4, dy * 1.01 + k * sy * 4, z), f, DARK, False, 0.2))
    m.add(0, chhajja("ch", 16, 14, (0, 0, z + 6.0), 1.0, 0.5, SIKRI_LT))
    m.add(0, parapet("par", 16, 14, z + 6.5, 0.9, 0.3, (0, 0), SIKRI))
    # the two entrance porches with pyramidal stone roofs (south-west and north-east)
    for k, (x, y) in enumerate(((-6.5, -8.5), (6.5, 8.5))):
        m.add(1, colonnade(f"porch{k}", 3.6, 3.0, 4.0, (x, y, z), SIKRI, 1.8), "porches and upper rooms")
        m.add(1, frustum(f"porch_roof{k}", 4.8, 4.2, 1.2, 1.0, 1.6, (x, y, z + 4.0), SIKRI_LT))
    # the two upper chambers, set diagonally, each with a fluted dome
    zu = z + 6.5
    for k, (x, y) in enumerate(((-3.5, 3), (3.5, -3))):
        m.add(1, box(f"up{k}", 6.4, 6.4, 4.0, (x, y, zu), SIKRI))
        for f, (dx, dy) in (("S", (0, -3.2)), ("N", (0, 3.2)), ("E", (3.2, 0)), ("W", (-3.2, 0))):
            m.add(1, arch_panel(f"uw{k}{f}", 1.4, 2.4, (x + dx * 1.01, y + dy * 1.01, zu), f, DARK, False, 0.2))
        m.add(1, chhajja(f"up_ch{k}", 6.4, 6.4, (x, y, zu + 3.6), 0.8, 0.4, SIKRI_LT))
        m.add(2, oct_prism(f"drum{k}", 3.0, 1.2, (x, y, zu + 4.0), SIKRI), "domes")
        m.add(2, ribbed_dome(f"dome{k}", 2.6, (x, y, zu + 5.2), SIKRI_LT, height=1.3, ribs=12, drum=0.25, drum_color=SIKRI))
    return m


def mariam_house():
    m = Model("mariam-house")
    m.add(0, box("plinth", 20, 14, 0.8, (0, 0, 0), SIKRI_DK), "house")
    z = 0.8
    m.add(0, box("rooms", 18, 8, 5.0, (0, 2.5, z), SIKRI))
    m.add(0, arcade("rooms_d", 16, 3.6, 5, (0, -1.55, z), "S", DARK, False, 0.5))
    m.add(0, colonnade("ver", 18, 4.4, 4.6, (0, -3.6, z), SIKRI, 2.25, "S"))
    m.add(0, box("ver_roof", 18.6, 4.8, 0.4, (0, -3.4, z + 4.6), SIKRI))
    m.add(0, box("gilt", 18.6, 0.2, 0.5, (0, -5.85, z + 4.0), GILT))
    m.add(0, chhajja("ch", 18, 12, (0, 0, z + 4.6), 0.8, 0.4, SIKRI_LT))
    m.add(0, parapet("par", 18.4, 12.4, z + 5.0, 0.8, 0.3, (0, 0), SIKRI))
    # the upper room and its kiosk
    zu = z + 5.0
    m.add(1, box("upper", 8, 6, 3.6, (3, 2.5, zu), SIKRI), "upper room")
    m.add(1, arcade("upper_d", 6, 2.4, 3, (3, -0.55, zu), "S", DARK, False, 0.5))
    m.add(1, box("upper_gilt", 8.2, 0.2, 0.4, (3, -0.6, zu + 3.0), GILT))
    m.add(1, chhajja("upper_ch", 8, 6, (3, 2.5, zu + 3.3), 0.7, 0.3, SIKRI_LT))
    m.add(2, chhatri("kiosk", 1.8, 4.8, (-5, 2.5, zu), SIKRI_LT, BUFF, 6), "kiosk")
    m.add(2, kiosk("upper_k", 1.4, 3.8, (3, 2.5, zu + 3.6), SIKRI_LT, BUFF))
    return m


def diwan_i_am():
    m = Model("diwan-i-am")
    W, D = 60.0, 110.0
    m.add(0, box("court", W - 12, D - 12, 0.25, (0, 0, 0), "#CDB894"), "cloisters")
    m.add(0, courtyard_ring("ring", W, D, 5.5, 6, (0, 0, 0), SIKRI, DARK, inner_arcade=True))
    m.add(0, chhajja("ring_ch_e", 6, D, (W / 2 - 3, 0, 5.1), 0.5, 0.4, SIKRI_LT))
    m.add(0, chhajja("ring_ch_w", 6, D, (-W / 2 + 3, 0, 5.1), 0.5, 0.4, SIKRI_LT))
    m.add(0, chhajja("ring_ch_s", W, 6, (0, -D / 2 + 3, 5.1), 0.5, 0.4, SIKRI_LT))
    m.add(0, chhajja("ring_ch_n", W, 6, (0, D / 2 - 3, 5.1), 0.5, 0.4, SIKRI_LT))
    # gates on the east and the north
    m.add(1, box("gate_e", 10, 16, 10, (W / 2 - 5, 0, 0), SIKRI), "gates and throne")
    m.add(1, iwan("gate_e_iw", 9, 9.5, 2, (W / 2 + 0.5, 0, 0), "E", SIKRI, SIKRI_LT))
    m.add(1, box("gate_n", 14, 8, 9, (0, D / 2 - 3, 0), SIKRI))
    m.add(1, iwan("gate_n_iw", 8, 8.5, 2, (0, D / 2 + 0.5, 0), "N", SIKRI, SIKRI_LT))
    # the throne pavilion on the west side, its jali screens and sloping stone roof
    tx = -W / 2 + 6 + 5
    m.add(1, box("throne_back", 10, 22, 9, (-W / 2 + 6, 0, 0), SIKRI))
    m.add(1, box("throne_plinth", 10, 16, 1.4, (tx, 0, 0), SIKRI_LT))
    m.add(1, colonnade("throne_cols", 9, 15, 5.0, (tx, 0, 1.4), SIKRI, 3.0, "E"))
    m.add(1, jali_wall("throne_jn", 9, 2.0, (tx, 7.5, 1.4), "N", SIKRI_LT, 4))
    m.add(1, jali_wall("throne_js", 9, 2.0, (tx, -7.5, 1.4), "S", SIKRI_LT, 4))
    m.add(1, arch_panel("throne_alcove", 3.6, 4.6, (-W / 2 + 11.05, 0, 1.4), "E", DARK, False, 0.3))
    m.add(2, frustum("throne_roof", 11, 17, 8, 13, 1.4, (tx, 0, 6.4), SIKRI_LT), "kiosks")
    m.add(2, box("throne_crest", 7, 12, 0.5, (tx, 0, 7.8), SIKRI))
    for s in (-1, 1):
        m.add(2, kiosk(f"throne_k{s}", 1.5, 4.4, (-W / 2 + 6, s * 8, 9), SIKRI_LT, BUFF))
    for sx in (-1, 1):
        for sy in (-1, 1):
            m.add(2, kiosk(f"corner{sx}{sy}", 1.7, 5.0, (sx * (W / 2 - 3), sy * (D / 2 - 3), 5.5), SIKRI_LT, BUFF))
    return m


def ibadat_khana():
    """Abu'l-Fazl's four halls round a central chamber: the plan is reconstructed from his description, the site is uncertain."""
    m = Model("ibadat-khana")
    m.add(0, box("plinth", 40, 40, 1.0, (0, 0, 0), SIKRI_DK), "plinth")
    z = 1.0
    m.add(1, box("centre", 14, 14, 10, (0, 0, z), SIKRI), "four halls")
    for f, (dx, dy) in (("S", (0, -1)), ("N", (0, 1)), ("E", (1, 0)), ("W", (-1, 0))):
        L, Wd = 13.0, 12.0
        cx, cy = dx * (7 + L / 2), dy * (7 + L / 2)
        w, d = (Wd, L) if f in "SN" else (L, Wd)
        m.add(1, box(f"hall{f}", w, d, 6.5, (cx, cy, z), SIKRI))
        m.add(1, arcade(f"hall_arc{f}", Wd * 0.9, 4.8, 3, (dx * (7 + L + 0.05), dy * (7 + L + 0.05), z), f, DARK, False, 0.75))
        m.add(1, chhajja(f"hall_ch{f}", w, d, (cx, cy, z + 6.1), 0.8, 0.4, SIKRI_LT))
        m.add(1, parapet(f"hall_par{f}", w, d, z + 6.5, 0.7, 0.3, (cx, cy), SIKRI))
        m.add(1, arch_panel(f"clere{f}", 4.0, 2.8, (dx * 7.05, dy * 7.05, z + 6.9), f, DARK, True, 0.2))
    m.add(2, chhajja("centre_ch", 14, 14, (0, 0, z + 9.6), 0.8, 0.4, SIKRI_LT), "dome")
    m.add(2, oct_prism("drum", 6.0, 2.0, (0, 0, z + 10), SIKRI))
    m.add(2, onion_dome("dome", 4.8, (0, 0, z + 12), BUFF, bulb=1.1, height=1.35, drum=0.3))
    for sx in (-1, 1):
        for sy in (-1, 1):
            m.add(2, kiosk(f"k{sx}{sy}", 1.3, 3.8, (sx * 5.6, sy * 5.6, z + 10), SIKRI_LT, BUFF))
    return m


def hakims_hammam():
    m = Model("hakims-hammam")
    m.add(0, box("base", 28, 20, 4.2, (0, 0, 0), SIKRI), "bath halls")
    m.add(0, box("plaster", 26, 18, 0.4, (0, 0, 4.2), BUFF))
    m.add(0, iwan("door", 5, 5.6, 1.2, (-6, -10.4, 0), "S", SIKRI, SIKRI_LT))
    m.add(0, arcade("side", 12, 2.2, 4, (5, -10.05, 0.8), "S", SIKRI_DK, True, 0.5))
    # the water tank and furnace block at the east end
    m.add(1, box("tank", 7, 9, 6.5, (11.5, 4, 0), SIKRI_DK), "tank and domes")
    m.add(1, merlons("tank_mer", 7, 9, 6.5, 0.5, 0.8, SIKRI_DK, "box"))
    # small plastered domes over the bath chambers, a larger one over the hot room
    for i, x in enumerate((-9, -3, 3)):
        for j, y in enumerate((-5, 0, 5)):
            r = 2.6 if (i, j) == (1, 1) else 1.7
            m.add(2, shallow_dome(f"d{i}{j}", r, (x, y, 4.6), BUFF, rise=0.75, drum=0.3, finial=(i, j) == (1, 1)), "domes")
    return m


# ---------------------------------------------------------------- gates

def naubat_khana():
    m = Model("naubat-khana")
    m.add(0, box("block", 28, 12, 10, (0, 0, 0), SIKRI), "gate")
    m.add(0, arch_panel("pass_s", 6, 8, (0, -6.05, 0), "S", DARK))
    m.add(0, arch_panel("pass_n", 6, 8, (0, 6.05, 0), "N", DARK))
    for s in (-1, 1):
        m.add(0, arcade(f"side_s{s}", 9, 4.6, 3, (s * 9, -6.05, 1.0), "S", DARK, True, 0.55))
        m.add(0, arcade(f"side_n{s}", 9, 4.6, 3, (s * 9, 6.05, 1.0), "N", DARK, True, 0.55))
    m.add(0, chhajja("ch", 28, 12, (0, 0, 9.6), 0.8, 0.4, SIKRI_LT))
    m.add(0, merlons("mer", 28, 12, 10, 0.7, 1.2, SIKRI, "box"))
    # the drummers' gallery over the arch
    m.add(1, box("gallery", 14, 9, 4.6, (0, 0, 10), SIKRI), "drum gallery")
    m.add(1, arcade("gal_s", 12, 3.2, 5, (0, -4.55, 10.2), "S", DARK, True, 0.6))
    m.add(1, arcade("gal_n", 12, 3.2, 5, (0, 4.55, 10.2), "N", DARK, True, 0.6))
    m.add(1, chhajja("gal_ch", 14, 9, (0, 0, 14.2), 0.7, 0.4, SIKRI_LT))
    for sx in (-1, 1):
        m.add(2, kiosk(f"k{sx}", 1.8, 5.2, (sx * 6.2, 0, 14.6), SIKRI_LT, BUFF), "kiosks")
        for sy in (-1, 1):
            m.add(2, kiosk(f"kc{sx}{sy}", 1.2, 3.8, (sx * 12.6, sy * 4.6, 10.4), SIKRI_LT, BUFF))
    return m


def agra_gate():
    m = Model("agra-gate")
    m.add(0, city_gate("ag", 22, 16, 13, 19, SIKRI, SIKRI_LT, 9.5), "gate")
    for s in (-1, 1):
        m.add(1, cylinder(f"bastion{s}", 5.2, 11, (s * 17, -5, 0), SIKRI_DK, verts=16, r_top=4.6), "bastions")
        m.add(1, kiosk(f"bast_k{s}", 2.0, 5.4, (s * 17, -5, 11), SIKRI_LT, BUFF))
    return m


def ajmeri_gate():
    m = Model("ajmeri-gate")
    m.add(0, city_gate("aj", 20, 15, 12, 20, SIKRI, SIKRI_LT, 9), "gate")
    for s in (-1, 1):
        m.add(1, cylinder(f"bastion{s}", 4.6, 10.5, (s * 14, -5, 0), SIKRI_DK, verts=16, r_top=4.1), "bastions")
    m.add(1, box("guard", 9, 6, 4.5, (0, 10, 0), SIKRI_LT))
    return m


def hathi_pol():
    m = Model("hathi-pol")
    m.add(0, box("block", 20, 12, 13, (0, 0, 0), SIKRI), "gate")
    m.add(0, iwan("iw", 11, 12.5, 2, (0, -6.6, 0), "S", SIKRI, SIKRI_LT))
    m.add(0, arch_panel("back", 5, 7, (0, 6.05, 0), "N", DARK))
    m.add(0, chhajja("ch", 20, 12, (0, 0, 12.6), 0.7, 0.4, SIKRI_LT))
    m.add(0, merlons("mer", 20, 12, 13, 0.7, 1.1, SIKRI, "box"))
    for s in (-1, 1):
        m.add(0, box(f"wall{s}", 5, 5, 9, (s * 12.5, 2, 0), SIKRI_DK))
        m.add(1, oct_prism(f"tw{s}", 2.6, 15, (s * 11.8, -4, 0), shade(SIKRI, -0.04)), "towers and elephants")
        m.add(1, kiosk(f"tw_k{s}", 1.7, 4.8, (s * 11.8, -4, 15), SIKRI_LT, BUFF))
    # the two stone elephants on their brackets either side of the arch, turned towards each other
    for s in (-1, 1):
        m.add(2, elephant(f"eleph{s}", (s * 7.6, -7.4, 0), -s * 40, "#9A8A7C", 3.0), "elephants")
    return m


# ---------------------------------------------------------------- by the lake

def hiran_minar():
    m = Model("hiran-minar")
    m.add(0, oct_prism("plat", 4.0, 0.8, (0, 0, 0), SIKRI_DK), "base")
    m.add(0, oct_prism("base", 2.3, 4.0, (0, 0, 0.8), SIKRI))
    m.add(0, box("door", 0.9, 0.3, 1.8, (0, -2.15, 0.8), DARK))
    z0 = 4.8
    H, r0, r1 = 12.8, 1.9, 1.55
    m.add(1, cylinder("shaft", r0, H, (0, 0, z0), SIKRI, verts=16, r_top=r1), "shaft")
    # the stone 'tusks' that stud the shaft
    verts, faces = [], []
    rows, per = 8, 12
    for i in range(rows):
        zz = z0 + 0.8 + i * (H - 1.6) / (rows - 1)
        rr = r0 + (r1 - r0) * (zz - z0) / H
        for k in range(per):
            a = math.tau * (k + 0.5 * (i % 2)) / per
            c, s = math.cos(a), math.sin(a)
            tx, ty = -s, c
            bx, by = rr * c, rr * s
            b = len(verts)
            q = 0.13
            for (u, v) in ((-q, -q), (q, -q), (q, q), (-q, q)):
                verts.append((bx + tx * u, by + ty * u, zz + v))
            verts.append((bx + c * 0.95, by + s * 0.95, zz + 0.3))
            faces += [(b, b + 1, b + 4), (b + 1, b + 2, b + 4), (b + 2, b + 3, b + 4), (b + 3, b, b + 4), (b + 3, b + 2, b + 1, b)]
    m.add(1, mesh_from("tusks", verts, faces, (0, 0, 0), "#E0D2BC"))
    zt = z0 + H
    m.add(2, cylinder("corbel", r1, 0.6, (0, 0, zt - 0.6), SIKRI_LT, verts=16, r_top=r1 * 1.5), "kiosk")
    m.add(2, cylinder("balcony", r1 * 1.55, 0.3, (0, 0, zt), SIKRI_LT, verts=16))
    m.add(2, chhatri("top", 1.25, 3.6, (0, 0, zt + 0.3), SIKRI_LT, BUFF, 8))
    return m


def caravanserai():
    m = Model("caravanserai")
    W, D = 140.0, 60.0
    m.add(0, box("court", W - 16, D - 16, 0.25, (0, 0, 0), "#CDB894"), "ranges")
    m.add(0, courtyard_ring("ring", W, D, 6.5, 8, (0, 0, 0), SIKRI, DARK, inner_arcade=True))
    m.add(0, arcade("out_s", W - 30, 3.0, 26, (0, -D / 2 - 0.05, 0.6), "S", SIKRI_DK, True, 0.5))
    m.add(0, merlons("mer", W, D, 6.5, 0.6, 1.4, SIKRI, "box"))
    # an upper storey of rooms on the lake (north) side
    m.add(1, box("upper_n", W - 20, 6, 3.6, (0, D / 2 - 4, 6.5), SIKRI_LT), "gates and towers")
    m.add(1, arcade("upper_arc", W - 24, 2.4, 22, (0, D / 2 - 7.05, 6.5), "S", DARK, True, 0.55))
    m.add(1, box("gate_s", 16, 12, 11, (0, -D / 2 + 5, 0), SIKRI))
    m.add(1, iwan("gate_s_iw", 11, 11, 2, (0, -D / 2 - 0.5, 0), "S", SIKRI, SIKRI_LT))
    m.add(1, box("gate_n", 12, 10, 9.5, (0, D / 2 - 5, 0), SIKRI))
    m.add(1, iwan("gate_n_iw", 8, 9, 2, (0, D / 2 + 0.5, 0), "N", SIKRI, SIKRI_LT))
    for sx in (-1, 1):
        for sy in (-1, 1):
            m.add(1, cylinder(f"tw{sx}{sy}", 3.6, 9, (sx * (W / 2 - 1.5), sy * (D / 2 - 1.5), 0), SIKRI_DK, verts=12))
            m.add(2, kiosk(f"tw_k{sx}{sy}", 1.6, 4.4, (sx * (W / 2 - 1.5), sy * (D / 2 - 1.5), 9), SIKRI_LT, BUFF), "kiosks and well")
    for s in (-1, 1):
        m.add(2, kiosk(f"gate_k{s}", 1.5, 4.2, (s * 5, -D / 2 + 5, 11), SIKRI_LT, BUFF))
    # a well and a little mosque in the court
    m.add(2, cylinder("well", 2.2, 1.0, (30, 0, 0), SIKRI_LT, verts=12))
    m.add(2, cylinder("well_w", 1.6, 1.05, (30, 0, 0), WATER, verts=12))
    m.add(2, box("mosque", 6, 12, 4.5, (-W / 2 + 14, 0, 0), SIKRI))
    for k in (-1, 0, 1):
        m.add(2, shallow_dome(f"mq_d{k}", 1.6, (-W / 2 + 13.5, k * 3.8, 4.5), BUFF, rise=0.9))
    return m


def baoli():
    m = Model("baoli")
    W, D, t, h = 24.0, 40.0, 3.0, 1.8
    m.add(0, box("rim_w", t, D, h, (-W / 2 + t / 2, 0, 0), SIKRI), "rim and steps")
    m.add(0, box("rim_e", t, D, h, (W / 2 - t / 2, 0, 0), SIKRI))
    m.add(0, box("rim_s", W, t, h, (0, -D / 2 + t / 2, 0), SIKRI))
    m.add(0, box("rim_n", W, t, h, (0, D / 2 - t / 2, 0), SIKRI))
    # the flight of steps going down from the south rim to the water and the well shaft at the north end
    iw = W - 2 * t
    n, y0, y1 = 14, -D / 2 + t, D / 2 - t - 11
    for i in range(n):
        m.add(0, box(f"step{i}", iw, (y1 - y0) / n, h * (n - i) / n, (0, y0 + (y1 - y0) * (i + 0.5) / n, 0), shade(SIKRI, 0.06 if i % 2 else 0.0)))
    m.add(0, box("water", iw, 11, 0.3, (0, D / 2 - t - 5.5, 0), WATER))
    # galleries on the inner side walls
    for s, f in ((-1, "E"), (1, "W")):
        m.add(1, arcade(f"gal{s}", D - 2 * t - 2, 1.5, 7, (s * (W / 2 - t - 0.05), 0, 0.1), f, DARK, True, 0.6), "galleries and well-head")
    m.add(1, lathe("shaft", [(3.6, 0), (3.6, 3.2), (2.8, 3.2), (2.8, 0.3)], (0, D / 2 - t - 5.5, 0), SIKRI_LT, verts=20, cap_top=True, cap_bottom=False))
    # the wheel-house over the well that lifted water towards the palace
    m.add(1, box("wheel_house", 9, 5, 5.5, (0, D / 2 - 2.5, 0), SIKRI))
    m.add(1, box("wheel", 0.5, 4.0, 4.0, (0, D / 2 - t - 5.5, 3.2), TIMBER))
    for s in (-1, 1):
        m.add(1, box(f"wheel_post{s}", 0.4, 0.4, 7.4, (s * 1.0, D / 2 - t - 5.5, 0), TIMBER))
    m.add(2, kiosk("head_k", 1.8, 5.0, (0, D / 2 - 2.5, 5.5), SIKRI_LT, BUFF), "kiosks")
    for s in (-1, 1):
        m.add(2, kiosk(f"ent_k{s}", 1.3, 4.0, (s * (W / 2 - 1.5), -D / 2 + 1.5, h), SIKRI_LT, BUFF))
    return m


def babur_garden():
    m = Model("babur-garden")
    S = 80.0
    m.add(0, charbagh("bagh", S, S, (0, 0, 0), SIKRI, "#86A06E", WATER, True), "garden")
    m.add(0, wall_run("wall", [(-S / 2, -S / 2), (S / 2, -S / 2), (S / 2, S / 2), (-S / 2, S / 2), (-S / 2, -S / 2)], 2.2, 0.8, color=SIKRI_DK, towers=True, tower_r=1.4, tower_every=80, merlon=None))
    m.add(0, box("gate", 6, 4, 4.0, (0, -S / 2, 0), SIKRI))
    m.add(0, arch_panel("gate_a", 2.4, 3.0, (0, -S / 2 - 2.05, 0), "S", DARK))
    # Babur's step-well in the north-east bed
    bx, by = 24, 24
    m.add(1, box("well_rim", 9, 14, 1.0, (bx, by, 0.3), SIKRI_LT), "step-well and pavilion")
    for i in range(6):
        m.add(1, box(f"ws{i}", 6, 1.4, 0.9 * (6 - i) / 6, (bx, by - 5.6 + i * 1.4, 1.3), SIKRI))
    m.add(1, box("well_water", 6, 3.4, 0.1, (bx, by + 4.5, 1.3), WATER))
    # an octagonal pavilion on a platform at the head of the garden, towards the lake
    m.add(1, oct_prism("chabutra", 7.5, 1.2, (0, S / 2 - 12, 0.3), SIKRI))
    m.add(2, chhatri("pav", 4.4, 9, (0, S / 2 - 12, 1.5), SIKRI_LT, BUFF, 8), "pavilion")
    return m


BUILDERS = {
    "fatehpur-sikri/jama-masjid": jama_masjid,
    "fatehpur-sikri/buland-darwaza": buland_darwaza,
    "fatehpur-sikri/salim-chishti-tomb": salim_chishti_tomb,
    "fatehpur-sikri/islam-khan-tomb": islam_khan_tomb,
    "fatehpur-sikri/diwan-i-khas": diwan_i_khas,
    "fatehpur-sikri/panch-mahal": panch_mahal,
    "fatehpur-sikri/anup-talao": anup_talao,
    "fatehpur-sikri/khwabgah": khwabgah,
    "fatehpur-sikri/jodh-bai-palace": jodh_bai_palace,
    "fatehpur-sikri/birbal-house": birbal_house,
    "fatehpur-sikri/mariam-house": mariam_house,
    "fatehpur-sikri/diwan-i-am": diwan_i_am,
    "fatehpur-sikri/ibadat-khana": ibadat_khana,
    "fatehpur-sikri/hakims-hammam": hakims_hammam,
    "fatehpur-sikri/naubat-khana": naubat_khana,
    "fatehpur-sikri/agra-gate": agra_gate,
    "fatehpur-sikri/ajmeri-gate": ajmeri_gate,
    "fatehpur-sikri/hathi-pol": hathi_pol,
    "fatehpur-sikri/hiran-minar": hiran_minar,
    "fatehpur-sikri/caravanserai": caravanserai,
    "fatehpur-sikri/baoli": baoli,
    "fatehpur-sikri/babur-garden": babur_garden,
}
