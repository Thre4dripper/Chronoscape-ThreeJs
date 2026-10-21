"""Delhi landmark miniatures: Firoz Shah's Firozabad to Bahadur Shah Zafar's Shahjahanabad.

Supersedes tools/blender/models/delhi.py (the old three-model test draft); these
BUILDERS are loaded after it by citymods and win on the shared keys.
"""
import math
import random
from chronokit import Model, box, cylinder, dome, join, shade, gable_roof, hip_roof, mesh_from
from worldkit import *

QUARTZITE, RUBBLE, LIME, BLACK = "#8F877B", "#A69A84", "#DCD3C1", "#2F2C29"
LAWN, DUST, OCHRE, CREAM, COPPER = "#86A06E", "#CDB894", "#D6B26C", "#EDE5D3", "#6F9384"
PAVE = shade(RED_SANDSTONE, 0.32)
HOUSE_COLORS = ["#D8C3A0", "#CFB089", "#E2D3B8", "#C99F78", "#D9CBB0", "#BFA07E"]
FACE_ROT = {"S": 0, "N": 180, "E": 90, "W": -90}


# ---------------------------------------------------------------- helpers

def stair_up(name, w, rise, run, n, x, y, side="S", color=RED_SANDSTONE):
    """A flight of n steps on the `side` of a building: high end against the building edge at (x, y), running outward."""
    parts = []
    for i in range(n):
        dep = run * (n - i) / n
        parts.append(box(f"{name}{i}", w, dep, rise * (i + 1) / n, (0, -dep / 2, 0), color))
    o = rot(join(parts, name), FACE_ROT[side])
    return move(o, x, y, 0)


def chhajja(name, w, d, loc, over=1.0, h=0.5, color=RED_SANDSTONE):
    """A thin sloping eave slab round a w x d block (wider at the top)."""
    return frustum(name, w, d, w + 2 * over, d + 2 * over, h, loc, color)


def oct_pts(r, start=math.pi / 8):
    return [(r * math.cos(start + i * math.pi / 4), r * math.sin(start + i * math.pi / 4)) for i in range(8)]


def oct_prism(name, r, h, loc=(0, 0, 0), color=RED_SANDSTONE):
    return prism(name, oct_pts(r), h, loc, color)


def oct_arches(name, r, h, z, loc=(0, 0, 0), per_face=1, color=DARK, fill=0.6, pointed=True, depth=0.3):
    """Arched recesses on all eight faces of an octagon of circumradius r (as oct_prism)."""
    x0, y0, _ = loc
    ap, flen = r * math.cos(math.pi / 8), 2 * r * math.sin(math.pi / 8)
    out = []
    for j in range(8):
        phi = j * math.pi / 4
        bay = flen / per_face
        grp = [arch_panel(f"{name}{j}_{k}", bay * fill, h, (-flen / 2 + bay * (k + 0.5), 0, z), "S", color, pointed, depth) for k in range(per_face)]
        g = rot(join(grp, f"{name}{j}"), math.degrees(phi) + 90)
        out.append(move(g, x0 + (ap + 0.02) * math.cos(phi), y0 + (ap + 0.02) * math.sin(phi), 0))
    return join(out, name)


def onion_prof(r, bulb=1.18, height=1.55, drum=0.5):
    R, H = r, r * height
    return [(R, 0), (R, drum * r), (R * 1.04, drum * r), (R * bulb, drum * r + H * 0.28), (R * bulb * 0.98, drum * r + H * 0.45), (R * 0.82, drum * r + H * 0.66),
            (R * 0.45, drum * r + H * 0.84), (R * 0.16, drum * r + H * 0.95)]


def lune_stripes(name, prof, loc, n=16, width=0.07, color=BLACK, grow=1.015):
    """n thin vertical bands laid over a surface of revolution (striped domes, marble-banded minarets)."""
    x, y, z = loc
    verts, faces = [], []
    for k in range(n):
        a0 = math.tau * k / n - width / 2
        angs = [a0, a0 + width / 2, a0 + width]
        base = len(verts)
        for r, zz in prof:
            for a in angs:
                verts.append((x + r * grow * math.cos(a), y + r * grow * math.sin(a), z + zz))
        for i in range(len(prof) - 1):
            for j in range(2):
                a = base + i * 3 + j
                faces.append((a, a + 1, a + 4, a + 3))
    return mesh_from(name, verts, faces, (0, 0, 0), color)


def striped_onion(name, r, loc, color=MARBLE, stripe=BLACK, n=16, bulb=1.18, height=1.55, drum=0.5):
    d = onion_dome(name, r, loc, color, bulb=bulb, height=height, drum=drum)
    prof = onion_prof(r, bulb, height, drum)[2:]
    return join([d, lune_stripes(name + "_st", prof, loc, n, 0.06, stripe)], name)


def striped_minaret(name, r, h, loc, color=RED_SANDSTONE, band=MARBLE, balconies=3, stripes=10):
    mn = minaret(name, r, h, loc, color, band, balconies, "chhatri")
    st = lune_stripes(name + "_st", [(r, 0), (r * (1 - 0.25 * 0.5), h * 0.5), (r * 0.75, h)], loc, stripes, 0.12, band, 1.02)
    return join([mn, st], name)


def arcade_box(name, w, d, h, loc=(0, 0, 0), color=RED_SANDSTONE, nx=5, ny=3, faces="SNEW", fill=0.7, ah=0.78, pointed=True, panel=DARK):
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


def kiosk(name, r, h, loc, color=MARBLE, dome_color=None):
    """A light four-pillared kiosk with a small dome (cheaper than worldkit.chhatri, for rows of them)."""
    x, y, z = loc
    parts = [box(f"{name}_p{i}", r * 0.24, r * 0.24, h * 0.5, (x + sx * r * 0.7, y + sy * r * 0.7, z), color) for i, (sx, sy) in enumerate(((-1, -1), (1, -1), (1, 1), (-1, 1)))]
    parts.append(box(name + "_eave", r * 2.3, r * 2.3, h * 0.08, (x, y, z + h * 0.5), color))
    parts.append(dome(name + "_d", r * 0.95, (x, y, z + h * 0.58), dome_color or color, squash=1.3, segments=10, rings=5))
    parts.append(cylinder(name + "_f", r * 0.08, h * 0.22, (x, y, z + h * 0.58 + r * 1.2), GILT, verts=5))
    return join(parts, name)


def fort_gate(name, w=44, d=26, h=22, face="S", color=RED_SANDSTONE, trim=MARBLE, n_kiosks=7):
    """The Red Fort's great gates: a deep pishtaq between octagonal towers crowned by chhatris, a row of kiosks over the arch."""
    parts = [box(name + "_b", w, d, h, (0, 0, 0), color)]
    parts.append(iwan(name + "_iw", w * 0.45, h * 0.92, 2.0, (0, -d / 2 - 0.6, 0), "S", color, trim))
    parts.append(arch_panel(name + "_back", w * 0.25, h * 0.6, (0, d / 2 + 0.05, 0), "N", DARK))
    parts.append(arcade(name + "_gal", w * 0.5, h * 0.18, 5, (0, -d / 2 - 0.05, h * 0.62), "S", DARK, True, 0.5))
    parts.append(box(name + "_band", w + 0.4, d + 0.4, 0.7, (0, 0, h - 1.2), trim))
    parts.append(merlons(name + "_mer", w, d, h, 0.9, 0.9, color, "box"))
    for s in (-1, 1):
        tx, ty = s * (w / 2 + 2), -d * 0.2
        parts.append(oct_prism(f"{name}_tw{s}", w * 0.15, h * 1.3, (tx, ty, 0), shade(color, -0.05)))
        parts.append(oct_arches(f"{name}_twa{s}", w * 0.15, h * 0.16, h * 0.95, (tx, ty, 0), 1, DARK, 0.5))
        parts.append(chhatri(f"{name}_tc{s}", w * 0.12, w * 0.3, (tx, ty, h * 1.3), trim, trim, 8))
    for k in range(n_kiosks):
        kx = -w * 0.3 + w * 0.6 * k / max(1, n_kiosks - 1)
        parts.append(kiosk(f"{name}_k{k}", 1.5, 4.6, (kx, -d / 2 + 2.2, h), trim, trim))
    o = rot(join(parts, name), FACE_ROT[face])
    return o


def pavilion(name, w, d, h, loc=(0, 0, 0), color=MARBLE, trim=None, nx=5, ny=3, plinth=1.0, chhatris=True, dome_color=GILT, faces="SNEW"):
    """A flat-roofed arcaded Mughal pavilion on a plinth, with a chhajja, parapet and corner kiosks."""
    x, y, z = loc
    trim = trim or shade(color, -0.12)
    parts = [box(name + "_pl", w + 2, d + 2, plinth, (x, y, z), shade(color, -0.06))]
    zb = z + plinth
    parts.append(arcade_box(name + "_body", w, d, h, (x, y, zb), color, nx, ny, faces))
    parts.append(chhajja(name + "_ch", w, d, (x, y, zb + h - 0.4), 1.1, 0.4, trim))
    parts.append(box(name + "_par", w, d, 0.8, (x, y, zb + h), color))
    if chhatris:
        k = min(w, d)
        for sx in (-1, 1):
            for sy in (-1, 1):
                parts.append(kiosk(f"{name}_c{sx}{sy}", k * 0.07, k * 0.3, (x + sx * (w / 2 - k * 0.08), y + sy * (d / 2 - k * 0.08), zb + h + 0.8), color, dome_color))
    return join(parts, name)


def vault(name, length, r, loc, color, n=10):
    """A half-cylinder barrel vault along X."""
    prof = [(r * math.cos(math.pi * i / n), r * math.sin(math.pi * i / n)) for i in range(n + 1)]
    verts = [(-length / 2, py, pz) for py, pz in prof] + [(length / 2, py, pz) for py, pz in prof]
    k = n + 1
    faces = [(i, i + 1, k + i + 1, k + i) for i in range(n)] + [tuple(range(k)), tuple(range(2 * k - 1, k - 1, -1))]
    return mesh_from(name, verts, faces, loc, color)


def flat_block(name, w, d, h, loc, color):
    x, y, z = loc
    return join([box(name, w, d, h, loc, color), box(name + "_p", w + 0.3, d + 0.3, 0.5, (x, y, z + h), shade(color, -0.08))], name)


def _ov(a, b):
    return not (a[2] < b[0] or b[2] < a[0] or a[3] < b[1] or b[3] < a[1])


def houses(name, seed, n, xr, yr, avoid=(), size=(6, 12), h=(3, 6), colors=HOUSE_COLORS, z=0.0, gap=1.5):
    """Scatter n flat-roofed houses in a rectangle, keeping clear of `avoid` rects (x0, y0, x1, y1)."""
    rng = random.Random(seed)
    out, placed = [], list(avoid)
    for _ in range(n * 30):
        if len(out) >= n:
            break
        w, d = rng.uniform(*size), rng.uniform(*size)
        x, y = rng.uniform(xr[0] + w / 2, xr[1] - w / 2), rng.uniform(yr[0] + d / 2, yr[1] - d / 2)
        r = (x - w / 2 - gap, y - d / 2 - gap, x + w / 2 + gap, y + d / 2 + gap)
        if any(_ov(r, a) for a in placed):
            continue
        placed.append(r)
        out.append(flat_block(f"{name}{len(out)}", w, d, rng.uniform(*h), (x, y, z), rng.choice(colors)))
    return join(out, name) if out else None


def trees(name, pts, r=2.5, color="#6F8A5C", z=0.0):
    return join([tree(f"{name}{i}", r, (x, y, z), color) for i, (x, y) in enumerate(pts)], name)


def city_gate(name, w=26, d=16, h=13, wall=30, color=RED_SANDSTONE, trim=MARBLE, wall_h=9):
    """A Shahjahanabad gate: a gatehouse facing south with stubs of the city wall to east and west."""
    parts = [gatehouse(name + "_g", w, d, h, (0, 0, 0), "S", color, trim)]
    for s in (-1, 1):
        parts.append(box(f"{name}_w{s}", wall, 4.5, wall_h, (s * (w / 2 + wall / 2), d * 0.15, 0), shade(color, -0.04)))
        n = int(wall / 2.2)
        for k in range(n):
            parts.append(cylinder(f"{name}_m{s}{k}", 0.55, 1.0, (s * (w / 2 + wall * (k + 0.5) / n), d * 0.15, wall_h), shade(color, -0.04), verts=6))
    return join(parts, name)


# ---------------------------------------------------------------- Red Fort

def red_fort(variant="1660"):
    """Plan follows the real axis: Lahori Gate - Chhatta Chowk - Naubat Khana - Diwan-i-Am - Rang Mahal on the river terrace."""
    late = variant == "1850"
    m = Model("red-fort")
    dz = 0.6
    octo = [(-275, -385), (-215, -475), (215, -475), (275, -420), (275, 420), (215, 475), (-215, 475), (-275, 385)]
    m.add(0, prism("plate", octo, dz, (0, 0, 0), "#CDB792"), "walls")
    city_side = [(275, -420), (215, -475), (-215, -475), (-275, -385), (-275, 385), (-215, 475), (215, 475), (275, 420)]
    m.add(0, wall_run("wall_city", city_side, 22, 9, color=RED_SANDSTONE, tower_r=10, tower_every=95, merlon="box", batter=0.15))
    m.add(0, wall_run("wall_river", [(275, 420), (275, -420)], 15, 7, color=RED_SANDSTONE, tower_r=8, tower_every=140, merlon="box"))
    m.add(0, box("moat_w", 12, 760, 0.35, (-288, 0, 0), WATER))
    for s in (-1, 1):
        m.add(0, box(f"moat_{s}", 420, 12, 0.35, (0, s * 488, 0), WATER))
    for (x, y) in [(-275, -385), (-215, -475), (-275, 385), (-215, 475), (215, -475), (215, 475)]:
        m.add(0, kiosk(f"bch{x}{y}", 5.0, 12, (x, y, 26), MARBLE, MARBLE))
    for nm, y in (("asad", -420), ("shah", 420)):
        m.add(0, oct_prism(f"{nm}_burj", 13, 19, (268, y, 0), RED_SANDSTONE))
        m.add(0, oct_arches(f"{nm}_arc", 13, 5, 12, (268, y, 0), 1, DARK, 0.55))
        m.add(0, chhatri(f"{nm}_ch", 9, 16, (268, y, 19), MARBLE, MARBLE if nm == "shah" else GILT))
    # ranges of rooms along the inside of the walls
    for nm, (w, d, x, y, f, n) in {"rw_s": (10, 290, -259, -235, "E", 18), "rw_n": (10, 290, -259, 235, "E", 18), "rs_w": (95, 10, -167, -459, "N", 10),
                                   "rs_e": (250, 10, 65, -459, "N", 16), "rn_w": (275, 10, -62, 459, "S", 16), "rn_e": (100, 10, 160, 459, "S", 10)}.items():
        m.add(0, arcade_box(nm, w, d, 6, (x, y, dz), shade(RED_SANDSTONE, 0.1), n if f in "SN" else 2, n if f in "EW" else 2, f, 0.33, 0.6))

    # ---- gates, the bazaar axis and the Diwan-i-Am court
    m.add(1, move(fort_gate("lahori", 46, 28, 24, "W"), -275, 0, 0), "gates")
    m.add(1, move(fort_gate("delhi_gate", 42, 26, 22, "S", n_kiosks=5), -90, -475, 0))
    m.add(1, gatehouse("water_gate", 22, 14, 12, (275, -300, 0), "E", RED_SANDSTONE, MARBLE))
    if not late:  # Shah Jahan's stone elephants outside the Delhi Gate, removed by Aurangzeb
        for s in (-1, 1):
            ex = -90 + s * 17
            m.add(1, box(f"eleph{s}", 2.6, 5.2, 2.6, (ex, -500, 2.2), "#8D877F"))
            m.add(1, box(f"eleph{s}h", 2.2, 2.2, 2.6, (ex, -503.5, 2.8), "#8D877F"))
            for lx in (-0.8, 0.8):
                for ly in (-1.8, 1.8):
                    m.add(1, box(f"eleph{s}l{lx}{ly}", 0.8, 0.8, 2.2, (ex + lx, -500 + ly, 0), "#8D877F"))
    else:  # Aurangzeb's barbicans
        m.add(1, wall_run("barb_l", [(-275, -42), (-340, -42), (-340, 42), (-275, 42)], 15, 7, color=RED_SANDSTONE, tower_r=7, tower_every=60, merlon="box"))
        m.add(1, gatehouse("barb_lg", 22, 12, 14, (-322, 42, 0), "N", RED_SANDSTONE, MARBLE))
        m.add(1, wall_run("barb_d", [(-125, -475), (-125, -532), (-55, -532), (-55, -475)], 15, 7, color=RED_SANDSTONE, tower_r=7, tower_every=60, merlon="box"))
        m.add(1, gatehouse("barb_dg", 24, 14, 14, (-125, -500, 0), "W", RED_SANDSTONE, MARBLE))
    # Chhatta Chowk: two storeys of shops under a barrel vault, an open octagon at its middle
    m.add(1, arcade_box("chhatta", 112, 26, 6, (-205, 0, dz), RED_SANDSTONE, 16, 3, "SN", 0.65))
    m.add(1, arcade_box("chhatta_up", 112, 26, 4.5, (-205, 0, dz + 6), shade(RED_SANDSTONE, 0.05), 16, 3, "SN", 0.5))
    m.add(1, vault("chhatta_vault", 112, 12, (-205, 0, dz + 10.5), shade(RED_SANDSTONE, 0.12)))
    m.add(1, oct_prism("chhatta_oct", 10, 15, (-205, 0, dz), shade(RED_SANDSTONE, 0.04)))
    m.add(1, oct_arches("chhatta_oct_a", 10, 6, dz + 7, (-205, 0, 0), 1, DARK, 0.5))
    m.add(1, box("square", 100, 120, 0.2, (-100, 0, dz), DUST))
    m.add(1, box("street_ns", 14, 400, 0.22, (-100, -260, dz), DUST))
    for s in (-1, 1):  # bazaar ranges along the street from the Delhi Gate
        m.add(1, arcade_box(f"delhi_bazaar{s}", 9, 330, 6, (-100 + s * 13, -275, dz), RED_SANDSTONE, 3, 22, "E" if s < 0 else "W", 0.38))
    # Naubat Khana, the drum house, gateway to the Diwan-i-Am court
    m.add(1, arcade_box("naubat", 20, 38, 17, (-38, 0, dz), RED_SANDSTONE, 3, 6, "EW", 0.55, 0.42))
    m.add(1, arch_panel("naubat_gw", 10, 12, (-48.1, 0, dz), "W", DARK))
    m.add(1, arch_panel("naubat_ge", 10, 12, (-27.9, 0, dz), "E", DARK))
    m.add(1, box("naubat_band", 20.6, 38.6, 0.8, (-38, 0, dz + 15), MARBLE))
    m.add(1, move(merlons("naubat_mer", 20, 38, dz + 17, 0.9, 0.9, RED_SANDSTONE, "box"), -38, 0, 0))
    for sy in (-1, 1):
        m.add(1, kiosk(f"naubat_c{sy}", 3.0, 8, (-38, sy * 16, dz + 17), MARBLE, GILT))
    m.add(1, courtyard_ring("diwan_court", 150, 180, 7, 8, (42, 0, dz), RED_SANDSTONE, DARK))
    m.add(1, box("diwan_court_pave", 134, 164, 0.2, (42, 0, dz), PAVE))
    # walled courts: palace enclosure behind the Diwan-i-Am, the Hayat Bakhsh garden, the Mahtab Bagh
    cw = shade(RED_SANDSTONE, 0.04)
    for i, (w, d, x, y) in enumerate(((3, 470, 118, 15), (157, 3, 196.5, -220), (3, 125, 85, 335), (3, 125, 215, 335), (130, 3, 150, 395), (130, 3, 150, 275),
                                      (3, 125, -45, 335), (130, 3, 20, 395), (130, 3, 20, 275))):
        m.add(1, box(f"court_wall{i}", w, d, 5.5, (x, y, dz), cw))

    # ---- the Diwan-i-Am: nine arches facing the court, the marble throne canopy at the back
    m.add(2, box("dia_plinth", 32, 68, 1.8, (100, 0, dz), shade(RED_SANDSTONE, -0.05)), "palaces")
    m.add(2, stair_up("dia_st", 10, 1.8, 4, 4, 84, 0, "W", shade(RED_SANDSTONE, 0.1)))
    zb = dz + 1.8
    m.add(2, arcade_box("dia_hall", 26, 62, 11.5, (100, 0, zb), "#C46A50", 3, 9, "WNS", 0.82, 0.82))
    m.add(2, chhajja("dia_ch", 26, 62, (100, 0, zb + 11.0), 1.6, 0.5, MARBLE))
    m.add(2, box("dia_par", 26, 62, 1.0, (100, 0, zb + 11.5), "#C46A50"))
    for sy in (-1, 1):
        m.add(2, kiosk(f"dia_c{sy}", 2.6, 8, (88, sy * 29, zb + 12.5), MARBLE, MARBLE))
        m.add(2, kiosk(f"dia_cb{sy}", 2.6, 8, (112, sy * 29, zb + 12.5), MARBLE, MARBLE))
    m.add(2, box("jharokha", 9, 12, 7, (114, 0, zb + 3), MARBLE))
    m.add(2, arch_panel("jharokha_a", 6, 5, (109.45, 0, zb + 3.5), "W", "#7A5A40"))
    m.add(2, move(rot(vault("jharokha_roof", 12, 4.6, (0, 0, 0), GILT), 90), 114, 0, zb + 10))
    m.add(2, box("wazir_dais", 4, 7, 1.2, (82, 0, dz), MARBLE))
    # the palace court in front of the Rang Mahal (Imtiaz Mahal garden)
    m.add(2, box("imtiaz_pave", 90, 465, 0.2, (163, 17, dz), PAVE))
    m.add(2, charbagh("imtiaz", 70, 90, (163, 0, dz + 0.2), MARBLE, LAWN, WATER, False))
    # the river terrace with the Nahr-i-Bihisht
    tz = dz + 1.6
    m.add(2, box("terrace", 62, 455, 1.6, (241, 27, dz), "#E4D8C4"))
    m.add(2, box("nahr_edge", 6, 455, 0.25, (213, 27, tz), MARBLE))
    m.add(2, box("nahr", 3.2, 455, 0.32, (213, 27, tz), WATER))
    m.add(2, box("nahr_e", 70, 3.2, 0.3, (179, 0, dz + 0.3), WATER))
    # river pavilions, south to north, long sides along the river
    m.add(2, pavilion("mumtaz", 26, 40, 8, (243, -150, tz), MARBLE, nx=4, ny=7))
    m.add(2, pavilion("rang_mahal", 34, 60, 10, (240, 0, tz), MARBLE, nx=5, ny=9))
    m.add(2, box("rang_lotus", 10, 10, 0.4, (220, 0, tz), WATER))
    m.add(2, pavilion("khas_mahal", 26, 46, 9, (243, 88, tz), MARBLE, nx=4, ny=7))
    m.add(2, oct_prism("musamman", 10, 18, (277, 88, 0), MARBLE))
    m.add(2, oct_arches("mus_arc", 10, 6.5, 10, (277, 88, 0), 1, DARK, 0.6))
    m.add(2, oct_prism("mus_ch", 10.8, 0.5, (277, 88, 17.4), MARBLE))
    m.add(2, pavilion("diwan_khas", 30, 40, 10.5, (242, 165, tz), MARBLE, nx=5, ny=5, plinth=2.0, chhatris=False))
    for sx in (-1, 1):
        for sy in (-1, 1):
            m.add(2, chhatri(f"dik_c{sx}{sy}", 3.2, 11, (242 + sx * 12.5, 165 + sy * 17.5, tz + 12.5), MARBLE, GILT, 8))
    m.add(2, arcade_box("hammam", 24, 30, 8, (244, 232, tz), MARBLE, 4, 5, "SNW", 0.55))
    # Moti Masjid (Aurangzeb, 1659-60): marble prayer hall in a red-walled court
    m.add(2, box("moti_wall", 32, 30, 7.5, (178, 232, dz), RED_SANDSTONE))
    m.add(2, box("moti_court", 20, 26, 7.6, (184, 232, dz), "#EFE9DD"))
    m.add(2, box("moti_hall", 11, 26, 9.5, (167, 232, dz), MARBLE))
    m.add(2, arcade("moti_arc", 22, 6.5, 3, (172.6, 232, dz), "E", DARK))
    # Hayat Bakhsh garden with Sawan and Bhadon
    m.add(2, charbagh("hayat_bakhsh", 126, 116, (150, 335, dz), RED_SANDSTONE, LAWN, WATER, False))
    m.add(2, trees("hb_t", [(x, y) for x in (110, 128, 172, 190) for y in (300, 370)], 3.4, z=dz))
    m.add(2, box("hb_tank", 24, 24, 0.7, (150, 335, dz), WATER))
    for nm, y in (("sawan", 386), ("bhadon", 284)):
        m.add(2, pavilion(nm, 20, 10, 6.5, (150, y, dz), MARBLE, nx=4, ny=2, plinth=0.6))
    if late:
        m.add(2, pavilion("zafar_mahal", 10, 10, 4.5, (150, 335, dz + 0.4), RED_SANDSTONE, nx=3, ny=3, plinth=0.6, dome_color=MARBLE))
        for i, (x, y) in enumerate(((-15, 305), (40, 305), (-15, 365), (40, 365))):  # the salatin's crowded courts in the old Mahtab Bagh
            m.add(2, courtyard_ring(f"salatin{i}", 48, 44, 5, 7, (x, y, dz), shade(RED_SANDSTONE, 0.15), DARK, inner_arcade=False))
    else:
        m.add(2, charbagh("mahtab_bagh", 120, 116, (20, 335, dz), BUFF_SANDSTONE, LAWN, WATER, False))
        m.add(2, trees("mahtab_t", [(x, y) for x in (-20, 0, 40, 60) for y in (300, 370)], 3.4, z=dz))
    # princes' and workshop courts in the western and southern quarters
    courts = [(-190, 200), (-190, 330), (-190, -250), (-190, -380), (20, -330)]
    if late:
        courts += [(-150, 120), (-100, 200), (-100, 330), (-180, -150), (100, -330), (-30, -180), (60, -150)]
    for i, (x, y) in enumerate(courts):
        m.add(2, courtyard_ring(f"court{i}", 64, 54, 5.5, 8, (x, y, dz), shade(RED_SANDSTONE, 0.12 + 0.04 * (i % 3)), DARK, inner_arcade=i < 3))
    if not late:
        m.add(2, box("lawn_s", 120, 120, 0.25, (40, -195, dz), LAWN))
        m.add(2, trees("lawn_s_t", [(x, y) for x in (-5, 25, 55, 85) for y in (-235, -155)], 3.0, z=dz))
        m.add(2, box("lawn_nw", 110, 100, 0.25, (-120, 120, dz), LAWN))
        m.add(2, trees("lawn_nw_t", [(x, y) for x in (-150, -90) for y in (95, 145)], 3.0, z=dz))
    else:
        m.add(2, houses("q_late", 15, 12, (-250, 100), (-450, -100), [(-125, -460, -75, 0), (-225, -410, -155, -120), (-62, -210, 135, -120), (-65, -360, 135, -300)], (12, 22), (4, 7)))

    # ---- domes
    m.add(3, onion_dome("mus_dome", 7.0, (277, 88, 17.9), GILT, height=1.35, drum=0.35), "domes")
    for i, y in enumerate((224, 232, 240)):
        m.add(3, onion_dome(f"moti_d{i}", 3.8 if i != 1 else 4.4, (165, y, dz + 9.5), MARBLE, height=1.55, drum=0.45))
    for i, y in enumerate((224, 232, 240)):
        m.add(3, shallow_dome(f"hammam_d{i}", 3.4, (240, y, tz + 8), MARBLE, rise=0.8, finial=True))
    return m


# ---------------------------------------------------------------- Salimgarh

def salimgarh():
    m = Model("salimgarh")
    pts = [(-60, -138), (60, -138), (98, -60), (98, 80), (40, 138), (-50, 133), (-98, 60), (-98, -80), (-60, -138)]
    m.add(0, prism("plate", pts[:-1], 0.5, (0, 0, 0), "#BFAE8E"), "walls")
    m.add(0, wall_run("wall", pts, 11, 7, color=QUARTZITE, tower_r=8, tower_every=48, merlon="box", batter=0.2))
    m.add(1, gatehouse("gate", 22, 14, 13, (0, -138, 0), "S", QUARTZITE, RED_SANDSTONE, "mughal"), "buildings")
    m.add(1, houses("barracks", 5, 9, (-80, 80), (-110, 110), [(-25, -20, 25, 20)], (14, 30), (4, 6), ["#BBA98A", "#C9B696", "#D2C3A6"]))
    m.add(1, box("mosque", 18, 10, 6, (0, 0, 0.5), LIME))
    m.add(1, arcade("mosque_a", 16, 4, 3, (9.05, 0, 0.5), "E", DARK))
    m.add(2, trees("t", [(-60, 40), (50, -60), (30, 90), (-40, -90), (70, 30), (-75, -20)], 4.0), "trees")
    for i, y in enumerate((-3.5, 0, 3.5)):
        m.add(2, shallow_dome(f"md{i}", 2.6 if i == 1 else 2.0, (-2, y, 6.5), LIME, rise=0.9, finial=True))
    return m


# ---------------------------------------------------------------- Jama Masjid

def jama_masjid():
    m = Model("jama-masjid")
    P, z0, ph = 100, 3.0, 6.0
    zt = z0 + ph
    m.add(0, frustum("rock", 148, 148, 106, 106, z0, (0, 0, 0), "#8E7B63"), "plinth")
    m.add(0, box("plinth", P, P, ph, (0, 0, z0), RED_SANDSTONE))
    for f, (x, y) in (("S", (0, -P / 2 - 0.05)), ("N", (0, P / 2 + 0.05)), ("E", (P / 2 + 0.05, 0)), ("W", (-P / 2 - 0.05, 0))):
        m.add(0, arcade(f"plarc{f}", P * 0.9, ph * 0.7, 15, (x, y, z0), f, DARK, True, 0.62))
    m.add(0, box("pave", P - 1, P - 1, 0.3, (0, 0, zt), PAVE))
    # court with cloisters, corner pavilions and a pool
    m.add(1, courtyard_ring("court", P, P, 6.5, 7, (0, 0, zt), RED_SANDSTONE, DARK), "court")
    m.add(1, courtyard_ring("court_band", P, P, 0.5, 7.2, (0, 0, zt + 6.5), MARBLE, DARK, inner_arcade=False))
    m.add(1, box("pool_rim", 18, 18, 0.5, (14, 0, zt), MARBLE))
    m.add(1, box("pool", 15, 15, 0.6, (14, 0, zt), WATER))
    for sx in (-1, 1):
        for sy in (-1, 1):
            if sx < 0:
                continue
            m.add(1, chhatri(f"corner{sx}{sy}", 4.2, 11, (sx * (P / 2 - 4), sy * (P / 2 - 4), zt + 7), MARBLE, MARBLE, 8))
    # three stepped gateways: the royal east gate and the north and south gates
    m.add(1, box("gateE", 16, 32, 15, (P / 2, 0, zt), RED_SANDSTONE))
    m.add(1, iwan("gateE_iw", 18, 21, 3, (P / 2 + 8, 0, zt), "E", RED_SANDSTONE, MARBLE))
    m.add(1, stair_up("stE", 36, zt, 15, 20, P / 2 + 9.5, 0, "E", shade(RED_SANDSTONE, 0.1)))
    for sy, f in ((-1, "S"), (1, "N")):
        m.add(1, box(f"gate{f}", 26, 14, 13, (8, sy * P / 2, zt), RED_SANDSTONE))
        m.add(1, iwan(f"gate{f}_iw", 15, 17, 3, (8, sy * (P / 2 + 7), zt), f, RED_SANDSTONE, MARBLE))
        m.add(1, stair_up(f"st{f}", 26, zt, 16, 18, 8, sy * (P / 2 + 8.5), f, shade(RED_SANDSTONE, 0.1)))
        for k in (-1, 0, 1):
            m.add(1, chhatri(f"gate{f}_c{k}", 1.8, 5, (8 + k * 8, sy * P / 2, zt + 13), MARBLE, MARBLE))
    for k in (-1, 0, 1):
        m.add(1, chhatri(f"gateE_c{k}", 2.0, 6, (P / 2, k * 10, zt + 15), MARBLE, MARBLE))
    # prayer hall on the west with its pishtaq
    hx, hd, hl, hh = -36, 28, 64, 14
    m.add(2, box("hall", hd, hl, hh, (hx, 0, zt), RED_SANDSTONE), "prayer hall")
    m.add(2, arcade("hall_arc", hl * 0.92, hh * 0.68, 10, (hx + hd / 2 + 0.05, 0, zt), "E", DARK, True, 0.7))
    m.add(2, box("hall_band", 0.5, hl, 1.0, (hx + hd / 2 + 0.2, 0, zt + hh - 1.6), MARBLE))
    for k in range(-5, 6):
        m.add(2, box(f"hall_strip{k}", 0.5, 0.6, hh - 2, (hx + hd / 2 + 0.25, k * hl / 11, zt), MARBLE))
    m.add(2, iwan("pishtaq", 22, 24, 4, (hx + hd / 2 + 1.5, 0, zt), "E", RED_SANDSTONE, MARBLE))
    m.add(2, chhajja("hall_ch", hd, hl, (hx, 0, zt + hh - 0.5), 0.9, 0.5, MARBLE))
    for k in range(-3, 4):
        if k:
            m.add(2, chhatri(f"hall_kiosk{k}", 1.2, 3.6, (hx + hd / 2 - 1, k * 9, zt + hh), MARBLE, MARBLE))
    # domes and minarets
    m.add(3, striped_onion("dome_c", 9.5, (hx - 2, 0, zt + hh), MARBLE, BLACK, 20, 1.16, 1.5, 0.6), "domes")
    for sy in (-1, 1):
        m.add(3, striped_onion(f"dome{sy}", 7.0, (hx - 2, sy * 20, zt + hh), MARBLE, BLACK, 16, 1.16, 1.5, 0.55))
        m.add(3, striped_minaret(f"min{sy}", 2.6, 40, (hx + hd / 2 + 2, sy * (hl / 2 + 2), zt), RED_SANDSTONE, MARBLE, 3))
    return m


# ---------------------------------------------------------------- Chandni Chowk and the Kotwali

def shop_row(name, x0, x1, side, color, h, balconies=False):
    L = x1 - x0
    cx, cy = (x0 + x1) / 2, side * 25
    face = "S" if side > 0 else "N"
    fy = side * 18 - side * 0.05
    parts = [box(name, L, 14, h, (cx, cy, 0), color)]
    parts.append(arcade(name + "_a", L * 0.96, 3.4, max(2, int(L / 4)), (cx, fy, 0), face, DARK, True, 0.72))
    parts.append(arcade(name + "_w", L * 0.9, 2.0, max(2, int(L / 5)), (cx, fy, 4.4), face, DARK, False, 0.4))
    parts.append(box(name + "_ch", L, 1.6, 0.3, (cx, side * 17.4, 3.8), shade(color, -0.15)))
    parts.append(box(name + "_par", L, 14.3, 0.6, (cx, cy, h), shade(color, -0.07)))
    if balconies:
        for k in range(max(1, int(L / 12))):
            bx = x0 + (k + 0.5) * L / max(1, int(L / 12))
            parts.append(box(f"{name}_bal{k}", 3.2, 1.4, 1.8, (bx, side * 17.2, 4.2), TIMBER))
    return join(parts, name)


def chandni_chowk(variant="1660"):
    late = variant == "1850"
    m = Model("chandni-chowk")
    L = 300
    m.add(0, box("street", L, 36, 0.3, (0, 0, 0), DUST), "street")
    m.add(0, box("canal_edge", L, 6, 0.45, (0, 0, 0), BUFF_SANDSTONE))
    m.add(0, box("canal", L, 3.4, 0.5, (0, 0, 0), WATER))
    for x in (-95, 105):
        m.add(0, box(f"pool_rim{x}", 13, 13, 0.45, (x, 0, 0), BUFF_SANDSTONE))
        m.add(0, box(f"pool{x}", 10, 10, 0.5, (x, 0, 0), WATER))
    m.add(1, trees("trees", [(x, s * 6.5) for x in range(-144, 146, 12) if abs(x + 95) > 9 and abs(x - 105) > 9 for s in (-1, 1)], 2.4, z=0.3), "trees")
    north = [(-150, -102), (-96, -42), (-36, 18), (24, 88), (94, 150)]
    south = [(-150, -102), (-96, -42), (-36, 18), (94, 150)]
    cols = ["#D2B48C", "#C9A27A", "#DCC6A2", "#C49A72", "#D8BE98"] if not late else ["#E6D8BE", "#DCCAA8", "#EDE1CA", "#D7C19C", "#E3D2B3"]
    for i, (a, b) in enumerate(north):
        m.add(2, shop_row(f"n{i}", a, b, 1, cols[i % 5], 7.5 + (i % 3), late), "shops")
    for i, (a, b) in enumerate(south):
        m.add(2, shop_row(f"s{i}", a, b, -1, cols[(i + 2) % 5], 7 + (i % 2) * 1.5, late))
    # the Kotwali: magistrate's building with its platform on the street
    m.add(2, box("kotwali", 28, 14, 8, (38, -25, 0), "#C08A62"))
    m.add(2, arcade("kotwali_a", 26, 4.5, 5, (38, -17.95, 0), "N", DARK))
    m.add(2, move(merlons("kotwali_mer", 28, 14, 8, 0.8, 0.8, "#C08A62", "round"), 38, -25, 0))
    m.add(2, box("chabutra", 20, 6, 1.4, (38, -15.4, 0), BUFF_SANDSTONE))
    m.add(2, iwan("kotwali_gate", 7, 9, 2, (38, -17.2, 0), "N", "#C08A62", BUFF_SANDSTONE))
    if late:
        # Roshan-ud-Daula's Sunehri Masjid (1721): three gilded domes over a plinth of shops
        m.add(2, box("sunehri_plinth", 26, 14, 4, (68, -25, 0), "#C9A27A"))
        m.add(2, arcade("sunehri_shops", 24, 3, 5, (68, -17.95, 0), "N", DARK))
        m.add(2, box("sunehri_hall", 20, 9, 5.5, (68, -27, 4), BUFF_SANDSTONE))
        m.add(2, arcade("sunehri_arc", 18, 4, 3, (68, -22.45, 4), "N", DARK))
        for i, x in enumerate((61, 68, 75)):
            m.add(3, onion_dome(f"sunehri_d{i}", 2.6 if i == 1 else 2.1, (x, -27, 9.5), GILT, height=1.5, drum=0.5), "domes")
        for s in (-1, 1):
            m.add(3, minaret(f"sunehri_m{s}", 0.7, 9, (68 + s * 10.5, -22.5, 4), BUFF_SANDSTONE, GILT, 1, "dome"))
    else:
        m.add(2, shop_row("s_k", 56, 88, -1, cols[4], 8))
    return m


# ---------------------------------------------------------------- Jahanara's Sarai

def jahanara_sarai():
    m = Model("jahanara-sarai")
    W, D = 90, 64
    m.add(0, box("pave", W, D, 0.3, (0, 0, 0), PAVE), "court")
    m.add(0, courtyard_ring("r1", W, D, 5.2, 9, (0, 0, 0), RED_SANDSTONE, DARK))
    for f, (x, y) in (("S", (0, -D / 2 - 0.05)), ("E", (W / 2 + 0.05, 0)), ("W", (-W / 2 - 0.05, 0))):
        L = W if f in "SN" else D
        m.add(0, arcade(f"out{f}", L * 0.9, 3.8, int(L / 5.5), (x, y, 0), f, DARK, True, 0.6))
    m.add(1, courtyard_ring("r2", W, D, 4.4, 9, (0, 0, 5.2), shade(RED_SANDSTONE, 0.07), DARK), "upper")
    m.add(1, courtyard_ring("cornice", W + 1.6, D + 1.6, 0.5, 1.4, (0, 0, 9.4), BUFF_SANDSTONE, DARK, inner_arcade=False))
    m.add(1, charbagh("garden", W - 20, D - 20, (0, 0, 0.3), BUFF_SANDSTONE, LAWN, WATER, False))
    m.add(1, trees("gt", [(x, y) for x in (-26, -12, 12, 26) for y in (-12, 12)], 2.6, z=0.3))
    m.add(1, box("mosque", 8, 12, 5, (-31, 0, 0.3), BUFF_SANDSTONE))
    m.add(2, iwan("gate", 20, 16, 11, (0, -D / 2 + 3.5, 0), "S", RED_SANDSTONE, MARBLE), "gate")
    for s in (-1, 1):
        m.add(2, chhatri(f"gate_c{s}", 2.0, 6, (s * 8.5, -D / 2 + 3.5, 16), MARBLE, MARBLE))
    for sx in (-1, 1):
        for sy in (-1, 1):
            m.add(2, oct_prism(f"tw{sx}{sy}", 4.2, 11, (sx * (W / 2 - 2), sy * (D / 2 - 2), 0), shade(RED_SANDSTONE, -0.05)))
            m.add(2, chhatri(f"twc{sx}{sy}", 3.0, 7, (sx * (W / 2 - 2), sy * (D / 2 - 2), 11), MARBLE, MARBLE))
    m.add(2, onion_dome("mosque_d", 2.6, (-31, 0, 5.3), MARBLE, height=1.4, drum=0.4))
    return m


# ---------------------------------------------------------------- Fatehpuri Masjid

def fatehpuri_masjid():
    m = Model("fatehpuri-masjid")
    m.add(0, box("pave", 80, 75, 0.3, (0, 0, 0), PAVE), "base")
    o = mosque("fm", 80, 75, (0, 0, 0), RED_SANDSTONE, shade(RED_SANDSTONE, 0.25), "#E8DFCD", domes=1, minarets=2, minaret_h=30, hall_depth=22, style="mughal", qibla="W")
    m.add(1, o, "mosque")
    m.add(2, lune_stripes("fm_flutes", onion_prof(9.0, 1.18, 1.55, 0.5)[2:], (-31.2, 0, 10.5), 24, 0.04, "#C9BBA2"), "dome")
    return m


# ---------------------------------------------------------------- Kotla of Firoz Shah

def kotla_pyramid(name, ruin=False):
    """The three-storey arcaded pyramid of Firoz Shah carrying the Ashokan pillar."""
    parts = []
    z = 0.0
    col = LIME if not ruin else RUBBLE
    for i, (w, h, n) in enumerate(((34, 6, 7), (26, 5.5, 5), (18, 5, 3))):
        parts.append(box(f"{name}_t{i}", w, w, h, (0, 0, z), shade(col, -0.04 * i)))
        for f, (x, y) in (("S", (0, -w / 2 - 0.05)), ("N", (0, w / 2 + 0.05)), ("E", (w / 2 + 0.05, 0)), ("W", (-w / 2 - 0.05, 0))):
            parts.append(arcade(f"{name}_a{i}{f}", w * 0.86, h * 0.72, n, (x, y, z), f, DARK, False, 0.6))
        if not ruin or i < 2:
            parts.append(box(f"{name}_par{i}", w, w, 0.7, (0, 0, z + h), shade(col, -0.1)))
        z += h
    parts.append(stair_up(f"{name}_st", 5, 6, 8, 8, 0, -17, "S", col))
    parts.append(box(f"{name}_base", 3, 3, 0.8, (0, 0, z), "#B9A98A"))
    parts.append(cylinder(f"{name}_pillar", 0.75, 13.1, (0, 0, z + 0.8), "#D2BE8C", verts=16, r_top=0.52))
    parts.append(lathe(f"{name}_bell", [(0.52, 0), (0.75, 0.3), (0.68, 0.8), (0.36, 1.0)], (0, 0, z + 13.9), "#D2BE8C", verts=16))
    if not ruin:
        parts.append(lathe(f"{name}_kalash", [(0.36, 0), (0.7, 0.6), (0.5, 1.3), (0.15, 1.8), (0.06, 2.8), (0.0, 3.1)], (0, 0, z + 14.9), GILT, verts=12))
    return join(parts, name)


def kotla(variant="1380"):
    ruin = variant == "ruin"
    m = Model("kotla")
    W, D = 260, 330
    wcol = LIME if not ruin else RUBBLE
    m.add(0, box("plate", W, D, 0.5, (0, 0, 0), "#C9B78F" if not ruin else "#BBA986"), "walls")
    if not ruin:
        pts = [(-W / 2 + 6, -D / 2 + 6), (W / 2 - 6, -D / 2 + 6), (W / 2 - 6, D / 2 - 6), (-W / 2 + 6, D / 2 - 6), (-W / 2 + 6, -D / 2 + 6)]
        m.add(0, wall_run("wall", pts, 12, 6, color=QUARTZITE, tower_r=7, tower_every=55, merlon="box", batter=0.25))
        m.add(0, gatehouse("gate_w", 22, 14, 13, (-W / 2 + 6, -40, 0), "W", QUARTZITE, LIME, "roman"))
    else:  # broken runs of wall
        for i, seg in enumerate(([(-124, -159), (40, -159)], [(80, -159), (124, -159), (124, 60)], [(124, 110), (124, 159), (-30, 159)], [(-124, 159), (-124, -20)], [(-124, -80), (-124, -159)])):
            m.add(0, wall_run(f"wall{i}", seg, 8, 6, color=QUARTZITE, tower_r=7, tower_every=55, merlon=None, batter=0.25))
    # Jami Masjid on its arcaded undercroft
    mx, my = 40, -40
    m.add(1, box("jm_under", 62, 56, 5, (mx, my, 0.5), wcol), "mosque")
    for f, (x, y) in (("S", (mx, my - 28.05)), ("N", (mx, my + 28.05)), ("E", (mx + 31.05, my)), ("W", (mx - 31.05, my))):
        m.add(1, arcade(f"jm_cells{f}", (62 if f in "SN" else 56) * 0.9, 3.6, 11, (x, y, 0.5), f, DARK, True, 0.6))
    m.add(1, stair_up("jm_st", 8, 5.5, 8, 8, mx, my - 28, "S", wcol))
    if not ruin:
        m.add(1, courtyard_ring("jm_court", 62, 56, 5, 7, (mx, my, 5.5), wcol, DARK))
        m.add(1, box("jm_hall", 12, 50, 6.5, (mx - 25, my, 5.5), wcol))
        for i, y in enumerate((-14, 0, 14)):
            m.add(3, shallow_dome(f"jm_d{i}", 5.0 if i == 1 else 4.0, (mx - 25, my + y, 12), LIME, rise=0.85, finial=True), "domes")
    else:
        for i, (x, y, w, d) in enumerate(((mx - 25, my, 10, 44), (mx, my - 24, 40, 6), (mx + 26, my + 5, 6, 30))):
            m.add(1, box(f"jm_ruin{i}", w, d, 3.2, (x, y, 5.5), RUBBLE))
            m.add(1, arcade(f"jm_ruin_a{i}", max(w, d) * 0.8, 2.5, 5, (x + (w / 2 + 0.05 if d > w else 0), y + (0 if d > w else d / 2 + 0.05), 5.5), "E" if d > w else "N", DARK))
    # the pyramid and pillar
    m.add(2, move(kotla_pyramid("lat", ruin), 30, 70, 0.5), "pillar")
    # circular baoli
    bx, by = -50, 80
    m.add(1, lathe("baoli_ring", [(16, 0), (16, 6), (11, 6), (11, 0.6)], (bx, by, 0.5), wcol, verts=32, cap_top=False, cap_bottom=False))
    m.add(1, lathe("baoli_ring2", [(16.2, 0), (16.2, 5.5)], (bx, by, 0.5), wcol, verts=32, cap_top=False, cap_bottom=False))
    m.add(1, cylinder("baoli_step", 11, 0.3, (bx, by, 0.5), shade(wcol, -0.15), verts=32))
    m.add(1, cylinder("baoli_water", 7, 0.4, (bx, by, 0.5), WATER, verts=24))
    m.add(1, oct_arches("baoli_arc", 16.4, 3.5, 1.0, (bx, by, 0), 2, DARK, 0.5))
    # palace ranges
    if not ruin:
        for i, (x, y, w, d, h) in enumerate(((100, 30, 22, 120, 9), (95, 125, 40, 40, 11), (-60, -20, 60, 22, 7), (-80, -110, 70, 30, 8), (-30, 145, 70, 18, 7))):
            m.add(2, arcade_box(f"palace{i}", w, d, h, (x, y, 0.5), wcol, max(3, int(w / 7)), max(3, int(d / 7)), "SNEW", 0.6))
            m.add(2, box(f"palace{i}_par", w + 0.4, d + 0.4, 0.8, (x, y, h + 0.5), shade(wcol, -0.08)))
        m.add(2, charbagh("garden", 70, 60, (-40, 20, 0.5), RUBBLE, LAWN, WATER, True))
    else:
        rng = random.Random(7)
        for i, (x, y, w, d) in enumerate(((100, 30, 22, 120), (95, 125, 40, 40), (-60, -20, 60, 22), (-80, -110, 70, 30), (-30, 145, 70, 18))):
            m.add(2, box(f"palace_r{i}", w, d, 1.2 + rng.uniform(0, 2), (x, y, 0.5), RUBBLE))
            for k in range(3):
                m.add(2, box(f"palace_r{i}w{k}", 2, rng.uniform(8, d * 0.6), rng.uniform(3, 6), (x + rng.uniform(-w / 2, w / 2), y, 0.5), RUBBLE))
        m.add(2, houses("village", 21, 10, (-120, 0), (-150, 150), [(-70, 60, -30, 100), (-92, -33, -28, -7), (-117, -127, -43, -93), (-67, 134, 7, 156), (-78, -12, -2, 52)], (6, 10), (3, 4.5), ["#C9AE88", "#BFA27C", "#D2BC9A"], z=0.5))
    return m


# ---------------------------------------------------------------- Kalan Masjid

def kalan_masjid():
    m = Model("kalan-masjid")
    W, D, ph = 48, 50, 5
    col = "#8D877C"
    m.add(0, box("plinth", W, D, ph, (0, 0, 0), col), "plinth")
    for f, (x, y) in (("S", (0, -D / 2 - 0.05)), ("N", (0, D / 2 + 0.05)), ("W", (-W / 2 - 0.05, 0))):
        m.add(0, arcade(f"cells{f}", (W if f in "SN" else D) * 0.88, 3.6, 9, (x, y, 0), f, DARK, True, 0.6))
    m.add(0, stair_up("st", 9, ph, 7, 10, W / 2, 0, "E", col))  # the flight projects beyond the east face
    # battered enclosure with tapering corner towers
    m.add(1, frustum("wall_s", W - 2, 3.0, W - 2, 2.0, 7, (0, -D / 2 + 2.5, ph), col), "walls")
    m.add(1, frustum("wall_n", W - 2, 3.0, W - 2, 2.0, 7, (0, D / 2 - 2.5, ph), col))
    m.add(1, frustum("wall_w", 3.0, D - 2, 2.0, D - 2, 7, (-W / 2 + 2.5, 0, ph), col))
    m.add(1, frustum("wall_e", 3.0, D - 2, 2.0, D - 2, 7, (W / 2 - 2.5, 0, ph), col))
    for sx in (-1, 1):
        for sy in (-1, 1):
            m.add(1, cylinder(f"tw{sx}{sy}", 3.0, 10, (sx * (W / 2 - 2.5), sy * (D / 2 - 2.5), 0), shade(col, -0.05), verts=12, r_top=2.1))
    m.add(1, box("gate", 12, 12, 10, (W / 2 - 4, 0, 0), shade(col, 0.05)))
    m.add(1, arch_panel("gate_arch", 5, 4.5, (W / 2 + 2.05, 0, ph), "E", DARK))
    # cloisters and prayer hall roofed with rows of small domes
    m.add(2, box("hall", 14, D - 6, 5.5, (-W / 2 + 10, 0, ph), shade(col, 0.1)), "domes")
    m.add(2, box("cl_n", W - 22, 7, 4.5, (4, D / 2 - 6.5, ph), shade(col, 0.1)))
    m.add(2, box("cl_s", W - 22, 7, 4.5, (4, -D / 2 + 6.5, ph), shade(col, 0.1)))
    for i in range(5):
        for j in range(2):
            m.add(2, shallow_dome(f"hd{i}{j}", 2.7, (-W / 2 + 7 + j * 6, -16 + i * 8, ph + 5.5), shade(col, 0.15), rise=0.8))
    for x in range(-6, 16, 6):
        for sy in (-1, 1):
            m.add(2, shallow_dome(f"cd{x}{sy}", 2.4, (x, sy * (D / 2 - 6.5), ph + 4.5), shade(col, 0.15), rise=0.8))
    m.add(2, shallow_dome("gate_d", 4.5, (W / 2 - 4, 0, 10), shade(col, 0.15), rise=0.85, finial=True))
    return m


# ---------------------------------------------------------------- Pir Ghaib

def pir_ghaib():
    m = Model("pir-ghaib")
    m.add(0, box("terrace", 30, 26, 0.8, (0, 0, 0), RUBBLE), "base")
    m.add(1, arcade_box("lower", 22, 16, 5, (0, 0, 0.8), RUBBLE, 4, 3, "SNEW", 0.55, 0.7), "storeys")
    m.add(1, box("lower_par", 22.4, 16.4, 0.5, (0, 0, 5.8), shade(RUBBLE, -0.1)))
    m.add(2, arcade_box("upper", 12, 16, 4.2, (-5, 0, 6.3), RUBBLE, 2, 3, "SNW", 0.5, 0.65), "upper")
    m.add(2, box("upper_par", 12.4, 16.4, 0.6, (-5, 0, 10.5), shade(RUBBLE, -0.1)))
    m.add(2, cylinder("shaft", 1.6, 2.2, (6, 4, 6.3), shade(RUBBLE, -0.1), verts=12))
    m.add(2, box("cenotaph", 2.4, 1.2, 0.8, (5, -3, 6.3), LIME))
    m.add(2, stair_up("st", 3, 5.0, 7, 9, 11, -4, "E", RUBBLE))
    return m


# ---------------------------------------------------------------- Purana Qila

def qila_i_kuhna(name):
    """Sher Shah's mosque (1541): five inlaid arched bays, one dome, oriel towers at the rear corners. Faces east."""
    hd, hl, hh = 15, 51, 12
    parts = [box(name + "_hall", hd, hl, hh, (0, 0, 0.6), RED_SANDSTONE)]
    parts.append(box(name + "_plinth", hd + 30, hl + 4, 0.6, (12, 0, 0), BUFF_SANDSTONE))
    bays = [(-19.5, 8, 13), (-9.5, 8, 13), (0, 12, 18), (9.5, 8, 13), (19.5, 8, 13)]
    for i, (y, w, h) in enumerate(bays):
        parts.append(iwan(f"{name}_bay{i}", w + 1.5, h, 1.6, (hd / 2 + 0.8, y, 0.6), "E", RED_SANDSTONE if i != 2 else "#B9604A", MARBLE))
        parts.append(box(f"{name}_inlay{i}", 0.3, w * 0.9, 0.5, (hd / 2 + 1.75, y, 0.6 + h * 0.84), BLACK))
    parts.append(box(name + "_quartz_band", hd + 0.4, hl + 0.4, 1.2, (0, 0, 0.6 + hh - 1.2), QUARTZITE))
    parts.append(merlons(name + "_mer", hd, hl, 0.6 + hh, 0.7, 0.8, RED_SANDSTONE, "round"))
    for sy in (-1, 1):
        parts.append(oct_prism(f"{name}_oriel{sy}", 3.4, hh + 2, (-hd / 2, sy * (hl / 2 - 1), 0.6), shade(RED_SANDSTONE, -0.05)))
        parts.append(chhatri(f"{name}_oc{sy}", 2.6, 5, (-hd / 2, sy * (hl / 2 - 1), hh + 2.6), BUFF_SANDSTONE, MARBLE))
    parts.append(cylinder(name + "_drum", 6.6, 3.0, (-1, 0, 0.6 + hh), RED_SANDSTONE, verts=24))
    parts.append(shallow_dome(name + "_dome", 6.6, (-1, 0, 3.6 + hh), "#D8CDBA", rise=0.95, finial=True))
    return join(parts, name)


def sher_mandal(name):
    """Two-storey octagonal pavilion of red sandstone, with a kiosk on top: Humayun's library."""
    parts = [oct_prism(name + "_s1", 9, 6.5, (0, 0, 0), RED_SANDSTONE)]
    parts.append(oct_arches(name + "_a1", 9, 5, 0, (0, 0, 0), 1, DARK, 0.62))
    parts.append(oct_prism(name + "_band1", 9.3, 0.7, (0, 0, 6.5), MARBLE))
    parts.append(oct_prism(name + "_s2", 7.4, 5.5, (0, 0, 7.2), RED_SANDSTONE))
    parts.append(oct_arches(name + "_a2", 7.4, 4, 7.2, (0, 0, 0), 1, DARK, 0.55))
    parts.append(oct_prism(name + "_band2", 7.7, 0.6, (0, 0, 12.7), MARBLE))
    parts.append(chhatri(name + "_kiosk", 4.4, 9, (0, 0, 13.3), MARBLE, MARBLE, 8))
    return join(parts, name)


def purana_qila(variant="1545"):
    village = variant == "village"
    m = Model("purana-qila")
    W, D = 320, 520
    pts = [(-160, -230), (-130, -260), (130, -260), (160, -230), (160, 230), (130, 260), (-130, 260), (-160, 230)]
    m.add(0, prism("plate", pts, 0.5, (0, 0, 0), "#C8B690"), "walls")
    m.add(0, wall_run("wall", pts + [pts[0]], 16, 9, color=QUARTZITE, tower_r=9.5, tower_every=62, merlon="round", batter=0.25))
    m.add(0, box("moat_w", 10, 440, 0.3, (-170, 0, 0), WATER))
    # three gates: Bara Darwaza (west), Humayun Darwaza (south), Talaqi Darwaza (north)
    for nm, (x, y), f, w in (("bara", (-160, 30), "W", 46), ("humayun", (40, -260), "S", 40), ("talaqi", (-30, 260), "N", 40)):
        m.add(1, gatehouse(nm, w, 26, 20, (x, y, 0), f, RED_SANDSTONE, MARBLE), "gates")
        dx, dy = {"W": (0, 1), "S": (1, 0), "N": (1, 0)}[f]
        for s in (-1, 1):
            bx, by = x + s * dx * (w / 2 + 6), y + s * dy * (w / 2 + 6)
            m.add(1, cylinder(f"{nm}_b{s}", 9, 22, (bx, by, 0), shade(QUARTZITE, -0.05), verts=16, r_top=7.8))
            m.add(1, chhatri(f"{nm}_bc{s}", 5.2, 12, (bx, by, 22), RED_SANDSTONE, MARBLE, 8))
    for nm, (w, d, x, y) in (("path_w", (150, 8, -85, 30)), ("path_s", (8, 230, 40, -145)), ("path_n", (8, 200, -30, 160)), ("path_x", (90, 8, 0, -30))):
        m.add(1, box(nm, w, d, 0.15, (x, y, 0.5), DUST))
    # Qila-i-Kuhna mosque and Sher Mandal
    m.add(2, move(qila_i_kuhna("kuhna"), -30, 40, 0), "mosque and library")
    m.add(2, move(sher_mandal("sher_mandal"), 50, -60, 0))
    m.add(2, box("hammam", 16, 12, 5, (95, -20, 0), RUBBLE))
    m.add(2, cylinder("baoli", 6, 1.0, (-60, -90, 0), QUARTZITE, verts=20))
    m.add(2, cylinder("baoli_w", 4, 1.1, (-60, -90, 0), WATER, verts=20))
    if village:
        avoid = [(-60, 5, 20, 75), (30, -80, 70, -40), (-70, -100, -50, -80), (80, -30, 110, -10)]
        m.add(3, houses("vil", 31, 70, (-140, 140), (-240, 240), avoid, (6, 12), (3, 5), ["#C9AE88", "#BFA27C", "#D2BC9A", "#B89A76"]), "village")
        m.add(3, trees("vt", [(-110, 160), (100, 180), (120, -150), (-100, -190), (0, 200), (60, 120)], 4.0))
    else:
        m.add(3, box("lawn", 120, 160, 0.3, (60, 120, 0.5), LAWN), "grounds")
        m.add(3, trees("gt", [(x, y) for x in (20, 60, 100) for y in (60, 120, 180)], 4.0, z=0.8))
        m.add(3, houses("palace", 32, 10, (-140, 140), (-240, -120), [(10, -280, 70, -222)], (12, 24), (5, 8), ["#C9A27A", "#B9906A", "#D6BC96"]))
    return m


# ---------------------------------------------------------------- Sher Shah Gate and Khair-ul-Manazil

def sher_shah_gate():
    m = Model("sher-shah-gate")
    m.add(0, box("block", 20, 16, 14, (0, 0, 0), RED_SANDSTONE), "gate")
    m.add(0, box("quartz", 20.4, 16.4, 3, (0, 0, 0), QUARTZITE))
    for f, y in (("S", -8.05), ("N", 8.05)):
        m.add(0, arch_panel(f"arch{f}", 7, 10.5, (0, y, 0), f, DARK))
    for s in (-1, 1):
        m.add(0, arcade(f"shops{s}", 14, 3, 3, (s * 10.05, 0, 0), "E" if s > 0 else "W", DARK))
        m.add(1, cylinder(f"bast{s}", 5.8, 15, (s * 12.5, -4, 0), shade(RED_SANDSTONE, -0.05), verts=16, r_top=5.2), "bastions")
        m.add(1, chhatri(f"bc{s}", 3.4, 8, (s * 12.5, -4, 15), RED_SANDSTONE, MARBLE))
    m.add(1, merlons("mer", 20, 16, 14, 0.8, 0.8, RED_SANDSTONE, "round"))
    m.add(1, box("band", 20.6, 0.4, 0.8, (0, -8.2, 11.5), MARBLE))
    return m


def khair_ul_manazil():
    m = Model("khair-ul-manazil")
    m.add(0, box("pave", 56, 56, 0.3, (0, 0, 0), BUFF_SANDSTONE), "madrasa")
    m.add(0, courtyard_ring("r1", 56, 56, 4.2, 7, (0, 0, 0), RUBBLE, DARK))
    m.add(0, courtyard_ring("r2", 56, 56, 3.8, 7, (0, 0, 4.2), shade(RUBBLE, 0.06), DARK))
    m.add(1, box("hall", 12, 42, 8.5, (-20, 0, 0), LIME), "mosque")
    m.add(1, arcade("hall_a", 38, 6, 5, (-13.95, 0, 0), "E", DARK))
    m.add(1, iwan("hall_iw", 11, 11, 1.6, (-13.2, 0, 0), "E", LIME, RED_SANDSTONE))
    m.add(1, iwan("gate", 12, 12, 7, (25, 0, 0), "E", RED_SANDSTONE, MARBLE))
    m.add(2, cylinder("drum", 5.2, 2, (-20, 0, 8.5), LIME, verts=24), "dome")
    m.add(2, shallow_dome("dome", 5.2, (-20, 0, 10.5), LIME, rise=0.95, finial=True))
    return m


# ---------------------------------------------------------------- Humayun's Tomb

def tomb_body(name, w, h, cut, z, color=RED_SANDSTONE, trim=MARBLE):
    """Square tomb with chamfered corners; a tall pishtaq on each face and two storeys of arches on the wings and chamfers."""
    a = w / 2
    pts = [(-a + cut, -a), (a - cut, -a), (a, -a + cut), (a, a - cut), (a - cut, a), (-a + cut, a), (-a, a - cut), (-a, -a + cut)]
    parts = [prism(name + "_b", pts, h, (0, 0, z), color)]
    parts.append(prism(name + "_band", [(x * 1.006, y * 1.006) for x, y in pts], 0.8, (0, 0, z + h - 1.6), trim))
    for f in "SNEW":
        n = {"S": (0, -1), "N": (0, 1), "E": (1, 0), "W": (-1, 0)}[f]
        px, py = n[0] * (a + 0.9), n[1] * (a + 0.9)
        parts.append(iwan(f"{name}_pish{f}", w * 0.36, h * 1.12, 2.4, (px, py, z), f, color, trim))
        for s in (-1, 1):
            wing = a - cut - w * 0.18
            off = s * (w * 0.18 + wing / 2)
            ox, oy = (off, n[1] * (a + 0.05)) if f in "SN" else (n[0] * (a + 0.05), off)
            for k, zz in enumerate((z + 0.5, z + h * 0.52)):
                parts.append(arch_panel(f"{name}_wing{f}{s}{k}", wing * 0.78, h * 0.4, (ox, oy, zz), f, DARK))
    # chamfered corners: two storeys of arches on each diagonal face
    for sx in (-1, 1):
        for sy in (-1, 1):
            ang = math.degrees(math.atan2(sy, sx))
            cx, cy = sx * (a - cut / 2 + 0.05), sy * (a - cut / 2 + 0.05)
            for k, zz in enumerate((z + 0.5, z + h * 0.52)):
                p = arch_panel(f"{name}_ch{sx}{sy}{k}", cut * 0.55, h * 0.4, (0, 0, zz), "S", DARK)
                p = rot(p, ang + 90)
                parts.append(move(p, cx, cy, 0))
    return join(parts, name)


def humayuns_tomb():
    m = Model("humayuns-tomb")
    S = 280
    h2 = S / 2 - 2
    m.add(0, box("lawn", S, S, 0.3, (0, 0, 0), LAWN), "garden")
    m.add(0, wall_run("wall", [(-h2, -h2), (h2, -h2), (h2, h2), (-h2, h2), (-h2, -h2)], 6, 2.4, color=RUBBLE, tower_r=3.2, tower_every=300, merlon=None))
    for sx in (-1, 1):
        for sy in (-1, 1):
            m.add(0, chhatri(f"wc{sx}{sy}", 2.6, 7, (sx * h2, sy * h2, 7.1), RED_SANDSTONE, MARBLE))
    # khiyabans (raised walks) with channels: two main axes and secondary walks making 36 squares
    for k in range(-3, 4):
        main = k == 0
        t = k * h2 / 3
        ww = 9 if main else 5
        m.add(0, box(f"walk_x{k}", 2 * h2, ww, 0.7, (0, t, 0), RED_SANDSTONE if main else shade(RED_SANDSTONE, 0.18)))
        m.add(0, box(f"walk_y{k}", ww, 2 * h2, 0.7, (t, 0, 0), RED_SANDSTONE if main else shade(RED_SANDSTONE, 0.18)))
        m.add(0, box(f"ch_x{k}", 2 * h2 - 4, 1.4 if main else 0.9, 0.8, (0, t, 0), WATER))
        m.add(0, box(f"ch_y{k}", 1.4 if main else 0.9, 2 * h2 - 4, 0.8, (t, 0, 0), WATER))
    for i in (-2, 0, 2):
        for j in (-2, 0, 2):
            if i or j:
                m.add(0, box(f"pool{i}{j}", 7, 7, 0.85, (i * h2 / 3, j * h2 / 3, 0), WATER))
    tp = [((i + 0.5) * h2 / 3, (j + 0.5) * h2 / 3) for i in range(-3, 3) for j in range(-3, 3) if not (-1 <= i <= 0 and -1 <= j <= 0)]
    m.add(0, trees("trees", tp, 4.0, "#68855A", 0.3))
    # gates: west (main) and south; a baradari on the east wall, a hammam on the north
    for nm, f, (x, y) in (("gate_w", "W", (-h2, 0)), ("gate_s", "S", (0, -h2))):
        blk = box(nm, 34 if f == "W" else 30, 20, 12, (0, 0, 0), RED_SANDSTONE)
        blk = rot(blk, FACE_ROT[f])
        m.add(0, move(blk, x, y, 0))
        nx, ny = {"W": (-1, 0), "S": (0, -1)}[f]
        m.add(0, iwan(nm + "_iw", 14, 15, 2, (x + nx * 10.5, y + ny * 10.5, 0), f, RED_SANDSTONE, MARBLE))
        for s in (-1, 1):
            cx, cy = (x + 2 * nx, y + s * 13) if f == "W" else (x + s * 11, y + 2 * ny)
            m.add(0, chhatri(f"{nm}_c{s}", 2.8, 8, (cx, cy, 12), MARBLE, MARBLE))
    m.add(0, pavilion("baradari", 12, 26, 6, (h2 - 4, 0, 0), RED_SANDSTONE, nx=3, ny=5, plinth=0.6, chhatris=False))
    # the platform with its arcaded cells and four stairs
    P, ph = 96, 7.0
    m.add(1, box("platform", P, P, ph, (0, 0, 0), RED_SANDSTONE), "platform")
    for f, (x, y) in (("S", (0, -P / 2 - 0.05)), ("N", (0, P / 2 + 0.05)), ("E", (P / 2 + 0.05, 0)), ("W", (-P / 2 - 0.05, 0))):
        m.add(1, arcade(f"cells{f}", P * 0.94, ph * 0.72, 17, (x, y, 0), f, DARK, True, 0.66))
        m.add(1, box(f"pband{f}", P + 0.6 if f in "SN" else 0.5, 0.5 if f in "SN" else P + 0.6, 0.6, (x, y, ph - 0.9), MARBLE))
        m.add(1, stair_up(f"st{f}", 10, ph, 9, 14, x * 1.0 + (0.05 if f == "E" else -0.05 if f == "W" else 0), y + (0.05 if f == "N" else -0.05 if f == "S" else 0), f, shade(RED_SANDSTONE, 0.12)))
    m.add(1, box("plat_top", P, P, 0.3, (0, 0, ph), shade(RED_SANDSTONE, 0.35)))
    # the tomb
    Bw, Bh = 50, 20
    m.add(2, tomb_body("tomb", Bw, Bh, 11, ph, RED_SANDSTONE, MARBLE), "tomb")
    m.add(2, box("roof", Bw - 8, Bw - 8, 1.2, (0, 0, ph + Bh), shade(RED_SANDSTONE, 0.05)))
    zr = ph + Bh
    for f in "SNEW":
        n = {"S": (0, -1), "N": (0, 1), "E": (1, 0), "W": (-1, 0)}[f]
        for s in (-1, 1):
            gx = n[0] * (Bw / 2 + 0.9) + (s * Bw * 0.18 if f in "SN" else 0)
            gy = n[1] * (Bw / 2 + 0.9) + (s * Bw * 0.18 if f in "EW" else 0)
            m.add(2, cylinder(f"guld{f}{s}", 0.7, 4.0, (gx, gy, zr + 2.4), MARBLE, verts=8, r_top=0.3))
    # drum, double dome and chhatris
    m.add(3, cylinder("drum", 13.6, 5.5, (0, 0, zr), MARBLE, verts=40), "dome")
    m.add(3, cylinder("drum_band", 13.9, 0.8, (0, 0, zr + 4.0), RED_SANDSTONE, verts=40))
    m.add(3, arcade("drum_n", 14, 3, 3, (0, 13.65, zr + 0.6), "N", DARK, True, 0.5))
    m.add(3, arcade("drum_s", 14, 3, 3, (0, -13.65, zr + 0.6), "S", DARK, True, 0.5))
    m.add(3, arcade("drum_e", 14, 3, 3, (13.65, 0, zr + 0.6), "E", DARK, True, 0.5))
    m.add(3, arcade("drum_w", 14, 3, 3, (-13.65, 0, zr + 0.6), "W", DARK, True, 0.5))
    prof = [(13.6, 0), (14.2, 3.0), (14.4, 6.0), (13.9, 9.2), (12.5, 12.2), (9.8, 14.8), (6.0, 16.6), (2.4, 17.6), (0.0, 17.9)]
    m.add(3, lathe("dome", prof, (0, 0, zr + 5.5), MARBLE, verts=40))
    m.add(3, lathe("finial", [(0.9, 0), (1.3, 0.6), (0.5, 1.4), (0.9, 2.2), (0.3, 3.0), (0.5, 3.6), (0.12, 4.4), (0.0, 5.5)], (0, 0, zr + 5.5 + 17.8), BRONZE, verts=12))
    for sx in (-1, 1):
        for sy in (-1, 1):
            m.add(3, chhatri(f"chh{sx}{sy}", 4.0, 11.5, (sx * 17.5, sy * 17.5, zr + 1.2), RED_SANDSTONE, MARBLE, 8, base=1.0))
    for f in "SNEW":
        n = {"S": (0, -1), "N": (0, 1), "E": (1, 0), "W": (-1, 0)}[f]
        m.add(3, chhatri(f"chh{f}", 2.4, 7, (n[0] * 19.5, n[1] * 19.5, zr + 1.2), RED_SANDSTONE, MARBLE, 6))
    return m


# ---------------------------------------------------------------- Isa Khan's Tomb and Arab Sarai

def isa_khan_tomb():
    m = Model("isa-khan-tomb")
    m.add(0, prism("plate", oct_pts(35), 0.3, (0, 0, 0), "#C6B793"), "enclosure")
    pts = oct_pts(34)
    m.add(0, wall_run("enc", pts + [pts[0]], 4.2, 1.6, color=QUARTZITE, tower_r=2.0, tower_every=200, merlon="box"))
    m.add(0, box("gate", 8, 6, 6, (0, -31, 0), QUARTZITE))
    m.add(0, arch_panel("gate_a", 3.4, 4.6, (0, -34.05, 0), "S", DARK))
    # mosque on the west side of the enclosure
    m.add(1, box("mosque", 7, 18, 6, (-25, 0, 0), QUARTZITE), "mosque")
    m.add(1, arcade("mosque_a", 16, 4.2, 3, (-21.45, 0, 0), "E", DARK))
    m.add(1, shallow_dome("mosque_d", 3.0, (-25, 0, 6), LIME, rise=0.95, finial=True))
    # the tomb: verandah of three arches a side round an octagonal chamber
    m.add(1, oct_prism("plinth", 15, 1.2, (0, 0, 0), QUARTZITE))
    m.add(1, oct_prism("ver", 13, 6, (0, 0, 1.2), QUARTZITE), "tomb")
    m.add(1, oct_arches("ver_a", 13, 4.6, 1.2, (0, 0, 0), 3, DARK, 0.62))
    m.add(1, oct_prism("chajja", 13.8, 0.4, (0, 0, 7.0), RED_SANDSTONE))
    m.add(1, oct_prism("tiles", 13.1, 0.5, (0, 0, 6.2), GLAZE_TURQ))
    m.add(2, oct_prism("chamber", 8, 4.0, (0, 0, 7.4), QUARTZITE), "dome")
    m.add(2, oct_prism("tiles2", 8.1, 0.5, (0, 0, 10.6), GLAZE_BLUE))
    m.add(2, shallow_dome("dome", 7.4, (0, 0, 11.4), LIME, rise=0.95, finial=True))
    for j in range(8):
        a = j * math.pi / 4
        m.add(2, chhatri(f"k{j}", 1.4, 4.2, (11.3 * math.cos(a), 11.3 * math.sin(a), 7.4), RED_SANDSTONE, LIME, 6))
    return m


def arab_sarai():
    m = Model("arab-sarai")
    m.add(0, box("pave", 50, 30, 0.3, (0, 0, 0), BUFF_SANDSTONE), "walls")
    for s in (-1, 1):
        m.add(0, arcade_box(f"cells{s}", 16, 8, 6, (s * 16.5, 6, 0), RUBBLE, 4, 2, "S", 0.6))
        m.add(0, box(f"cells{s}_back", 8, 16, 6, (s * 21, 14, 0), RUBBLE))
    m.add(1, box("gate_b", 16, 12, 13, (0, 0, 0), RED_SANDSTONE), "gate")
    m.add(1, iwan("gate_iw", 13, 15.5, 2.0, (0, -6.5, 0), "S", RED_SANDSTONE, MARBLE))
    m.add(1, box("tile_band", 13.4, 0.3, 0.8, (0, -7.7, 12), GLAZE_BLUE))
    for s in (-1, 1):
        m.add(1, oct_prism(f"tw{s}", 1.6, 14, (s * 7.2, -5.6, 0), RED_SANDSTONE))
        m.add(1, chhatri(f"twc{s}", 1.5, 4.5, (s * 7.2, -5.6, 14), MARBLE, MARBLE))
    m.add(1, merlons("mer", 16, 12, 13, 0.7, 0.8, RED_SANDSTONE, "round"))
    return m


# ---------------------------------------------------------------- Nizamuddin

def nizamuddin(variant="1562"):
    early = variant == "early"
    m = Model("nizamuddin")
    m.add(0, box("pave", 110, 90, 0.3, (0, 0, 0), "#D3C4A4"), "court")
    # the baoli: a long stepped tank between walls of houses
    bx, by = -8, 26
    for nm, (w, d, x, y) in (("s", (46, 2, bx, by - 9)), ("n", (46, 2, bx, by + 9)), ("e", (2, 20, bx + 22, by)), ("w", (2, 20, bx - 22, by))):
        m.add(0, box(f"baoli_wall_{nm}", w, d, 4.0, (x, y, 0), QUARTZITE))
    m.add(0, arcade("baoli_arc", 40, 2.6, 8, (bx, by + 7.95, 0.8), "S", DARK, True, 0.55))
    for i in range(4):
        m.add(0, box(f"baoli_step{i}", 10 - i * 2, 16 - i * 3, 2.4 - i * 0.6, (bx - 17 + i * 2, by, 0), shade(QUARTZITE, 0.12 + i * 0.05)))
    m.add(0, box("baoli_water", 32, 15, 0.35, (bx + 5, by, 0), WATER))
    m.add(0, houses("basti", 3, 16, (-55, 55), (37, 45), (), (6, 10), (4, 7)))
    m.add(0, houses("basti_s", 4, 10, (-55, 55), (-45, -36), (), (6, 10), (4, 7)))
    # Jamaat Khana mosque, red sandstone with three domes (west)
    m.add(1, box("jk", 12, 28, 8, (-40, -10, 0), RED_SANDSTONE), "mosque")
    m.add(1, arcade("jk_a", 26, 6, 3, (-33.95, -10, 0), "E", DARK))
    for i, y in enumerate((-19, -10, -1)):
        m.add(3, shallow_dome(f"jk_d{i}", 3.6 if i == 1 else 3.0, (-40, y, 8), RED_SANDSTONE if not early else LIME, rise=0.85, finial=True), "domes")
    # the saint's tomb
    tx, ty = 8, -12
    if early:
        m.add(2, box("tomb", 10, 10, 6, (tx, ty, 0.3), LIME), "tomb")
        m.add(2, arch_panel("tomb_door", 3, 4.5, (tx, ty - 5.05, 0.3), "S", DARK))
        m.add(3, shallow_dome("tomb_d", 4.6, (tx, ty, 6.3), LIME, rise=0.9, finial=True))
    else:
        m.add(2, box("ver_pl", 18, 18, 0.8, (tx, ty, 0.3), MARBLE), "tomb")
        m.add(2, arcade_box("ver", 16, 16, 4.6, (tx, ty, 1.1), MARBLE, 5, 5, "SNEW", 0.72))
        m.add(2, chhajja("ver_ch", 16, 16, (tx, ty, 5.4), 1.0, 0.4, MARBLE))
        m.add(2, box("chamber", 10, 10, 2.8, (tx, ty, 5.7), MARBLE))
        m.add(3, striped_onion("tomb_d", 4.4, (tx, ty, 8.5), MARBLE, BLACK, 16, 1.15, 1.45, 0.45))
        for sx in (-1, 1):
            for sy in (-1, 1):
                m.add(3, chhatri(f"tc{sx}{sy}", 1.0, 3.2, (tx + sx * 7, ty + sy * 7, 5.8), MARBLE, GILT, 6))
        m.add(2, jali_wall("khusrau_jali", 10, 2.2, (34, -24, 0.3), "S", MARBLE, 5))
        m.add(2, box("khusrau", 7, 7, 4.2, (34, -18, 0.3), MARBLE))
        m.add(3, shallow_dome("khusrau_d", 3.0, (34, -18, 4.5), MARBLE, rise=0.9, finial=True))
    m.add(2, box("khusrau_old", 5, 5, 3.0, (34, -2, 0.3), LIME))
    m.add(2, trees("t", [(-20, 0), (25, 8), (45, -30), (-45, 18)], 3.0, z=0.3))
    return m


# ---------------------------------------------------------------- Zinat-ul-Masajid

def zinat_ul_masajid():
    m = Model("zinat-ul-masajid")
    W, D, ph = 60, 50, 4.0
    m.add(0, box("platform", W, D, ph, (0, 0, 0), RED_SANDSTONE), "platform")
    m.add(0, arcade("plat_e", D * 0.9, 3, 9, (W / 2 + 0.05, 0, 0), "E", DARK, True, 0.6))
    m.add(0, box("court", W - 2, D - 2, 0.3, (0, 0, ph), PAVE))
    m.add(0, stair_up("st", 10, ph, 6, 8, 0, -D / 2, "S"))
    m.add(1, box("court_wall_n", W - 16, 1.4, 3, (8, D / 2 - 0.7, ph), RED_SANDSTONE), "court")
    m.add(1, box("court_wall_s", W - 16, 1.4, 3, (8, -D / 2 + 0.7, ph), RED_SANDSTONE))
    m.add(1, box("court_wall_e", 1.4, D, 3, (W / 2 - 0.7, 0, ph), RED_SANDSTONE))
    m.add(1, box("tank", 8, 8, 0.6, (12, 0, ph), WATER))
    hx, hd, hl, hh = -W / 2 + 8, 15, 46, 10
    m.add(2, box("hall", hd, hl, hh, (hx, 0, ph), RED_SANDSTONE), "prayer hall")
    m.add(2, arcade("hall_a", hl * 0.92, hh * 0.66, 7, (hx + hd / 2 + 0.05, 0, ph), "E", DARK, True, 0.7))
    m.add(2, iwan("pishtaq", 13, 15, 2.4, (hx + hd / 2 + 1.2, 0, ph), "E", RED_SANDSTONE, MARBLE))
    m.add(2, box("hall_band", 0.4, hl, 0.8, (hx + hd / 2 + 0.2, 0, ph + hh - 1.4), MARBLE))
    m.add(3, striped_onion("dome_c", 6.0, (hx - 1, 0, ph + hh), MARBLE, BLACK, 18, 1.15, 1.45, 0.5), "domes")
    for sy in (-1, 1):
        m.add(3, striped_onion(f"dome{sy}", 4.6, (hx - 1, sy * 14, ph + hh), MARBLE, BLACK, 14, 1.15, 1.45, 0.5))
        m.add(3, striped_minaret(f"min{sy}", 1.8, 28, (hx + hd / 2 + 1.5, sy * (hl / 2 + 1.5), ph), RED_SANDSTONE, MARBLE, 3))
    return m


# ---------------------------------------------------------------- gates of Shahjahanabad

def kashmiri_gate(variant="1660"):
    m = Model("kashmiri-gate")
    if variant != "1850":
        m.add(0, city_gate("kg", 24, 16, 12, 10, RED_SANDSTONE, MARBLE), "gate")
        m.add(1, cylinder("bastion", 8, 10, (15, 9, 0), shade(RED_SANDSTONE, -0.05), verts=16, r_top=7.2), "bastion")
        return m
    # the British rebuilding of 1835: twin carriage arches, guard rooms, a bastion with gun embrasures, a ditch
    col = "#B07A5A"
    m.add(0, box("ditch", 45, 5, 0.25, (0, -13, 0), WATER), "gate")
    m.add(0, box("block", 30, 14, 11, (0, 0, 0), col))
    for s in (-1, 1):
        for f, y in (("S", -7.05), ("N", 7.05)):
            m.add(0, arch_panel(f"arch{s}{f}", 5.4, 8, (s * 6, y, 0), f, DARK, False))
    m.add(0, box("cornice", 31, 15, 0.8, (0, 0, 11), shade(col, 0.15)))
    m.add(0, merlons("mer", 30, 14, 11.8, 0.9, 1.4, col, "box"))
    for s in (-1, 1):
        m.add(1, box(f"wall{s}", 8, 6, 9, (s * 19, 2, 0), shade(col, -0.05)), "walls")
        for k in range(3):
            m.add(1, box(f"emb{s}{k}", 1.2, 0.4, 1.2, (s * (16.5 + k * 2.5), -1.05, 6.5), DARK))
    m.add(1, prism("bastion", [(15, -6), (22, -12), (22, 8), (15, 8)], 9.5, (0, 0, 0), shade(col, -0.08)))
    m.add(1, box("bridge", 6, 6, 0.8, (-6, -12.5, 0), TIMBER))
    return m


def delhi_gate():
    m = Model("delhi-gate")
    m.add(0, city_gate("dg", 26, 18, 14, 8, RED_SANDSTONE, MARBLE, 10), "gate")
    for s in (-1, 1):
        m.add(1, oct_prism(f"oct{s}", 4.4, 16, (s * 16, -5, 0), shade(RED_SANDSTONE, -0.04)), "bastions")
        m.add(1, chhatri(f"octc{s}", 3.4, 8, (s * 16, -5, 16), MARBLE, MARBLE))
    return m


def ajmeri_gate():
    m = Model("ajmeri-gate")
    m.add(0, city_gate("ag", 22, 16, 12, 8, RED_SANDSTONE, MARBLE, 9), "gate")
    m.add(1, box("guard", 10, 6, 5, (0, 10, 0), shade(RED_SANDSTONE, 0.06)), "guard")
    return m


def lahori_gate():
    m = Model("lahori-gate")
    m.add(0, city_gate("lg", 22, 16, 12.5, 8, RED_SANDSTONE, MARBLE, 9), "gate")
    m.add(1, box("guard", 9, 6, 5, (-4, 10, 0), shade(RED_SANDSTONE, 0.06)), "guard")
    return m


# ---------------------------------------------------------------- British and late Mughal buildings

def columns_row(name, n, x0, x1, y, h, r=0.45, color=CREAM, z=0.0, along="x"):
    out = []
    for i in range(n):
        t = x0 + (x1 - x0) * i / max(1, n - 1)
        loc = (t, y, z) if along == "x" else (y, t, z)
        out.append(cylinder(f"{name}{i}", r, h, loc, color, verts=10))
    return join(out, name)


def st_james_church():
    m = Model("st-james-church")
    m.add(0, box("plinth", 40, 40, 1.0, (0, 0, 0), shade(OCHRE, -0.15)), "body")
    m.add(0, box("arm_ew", 38, 14, 9, (0, 0, 1), OCHRE))
    m.add(0, box("arm_ns", 14, 38, 9, (0, 0, 1), OCHRE))
    m.add(0, box("cornice_ew", 38.6, 14.6, 0.6, (0, 0, 10), CREAM))
    m.add(0, box("cornice_ns", 14.6, 38.6, 0.6, (0, 0, 10), CREAM))
    for f in "SNEW":
        n = {"S": (0, -1), "N": (0, 1), "E": (1, 0), "W": (-1, 0)}[f]
        for s in (-1, 1):
            wx, wy = (n[0] * 19.05, s * 3.5) if f in "EW" else (s * 3.5, n[1] * 19.05)
            m.add(0, arch_panel(f"win{f}{s}", 1.8, 4.5, (wx, wy, 3), f, "#4A5568", False))
        for s in (-1, 1):  # side windows on the arms
            if f in "SN":
                m.add(0, arch_panel(f"aw{f}{s}", 1.8, 4.5, (s * 13, n[1] * 7.05, 3), f, "#4A5568", False))
            else:
                m.add(0, arch_panel(f"aw{f}{s}", 1.8, 4.5, (n[0] * 7.05, s * 13, 3), f, "#4A5568", False))
    # gabled ends (pediments) on each arm
    m.add(1, rot(gable_roof("roof_ew", 14, 38, 2.8, (0, 0, 10.6), OCHRE, 0.3), 90), "roofs")
    m.add(1, gable_roof("roof_ns", 14, 38, 2.8, (0, 0, 10.6), OCHRE, 0.3))
    # porticoes on south, east and west
    for f in "SEW":
        n = {"S": (0, -1), "E": (1, 0), "W": (-1, 0)}[f]
        if f == "S":
            m.add(1, columns_row(f"col{f}", 4, -5, 5, -21.5, 7.5, 0.5, CREAM, 1.0))
            m.add(1, box(f"ent{f}", 13, 4, 1.2, (0, -21, 8.5), CREAM))
            m.add(1, gable_roof(f"ped{f}", 13, 4, 2.4, (0, -21, 9.7), CREAM, 0.2))
        else:
            m.add(1, columns_row(f"col{f}", 4, -5, 5, n[0] * 21.5, 7.5, 0.5, CREAM, 1.0, "y"))
            m.add(1, box(f"ent{f}", 4, 13, 1.2, (n[0] * 21, 0, 8.5), CREAM))
            m.add(1, move(rot(gable_roof(f"ped{f}", 13, 4, 2.4, (0, 0, 0), CREAM, 0.2), 90), n[0] * 21, 0, 9.7))
    # drum, dome, lantern, ball and cross
    m.add(2, cylinder("drum", 6.5, 4.5, (0, 0, 10.6), OCHRE, verts=24), "dome")
    m.add(2, cylinder("drum_c", 6.9, 0.5, (0, 0, 15.1), CREAM, verts=24))
    for j in range(8):
        a = j * math.pi / 4
        p = arch_panel(f"dw{j}", 1.2, 2.6, (0, 0, 11.4), "S", "#4A5568", False, 0.3)
        p = rot(p, math.degrees(a) + 90)
        m.add(2, move(p, 6.52 * math.cos(a), 6.52 * math.sin(a), 0))
    m.add(2, shallow_dome("dome", 6.6, (0, 0, 15.6), COPPER, rise=0.85))
    m.add(2, cylinder("lantern", 1.4, 2.4, (0, 0, 21.2), CREAM, verts=12))
    m.add(2, dome("lantern_d", 1.5, (0, 0, 23.6), COPPER, segments=12, rings=6))
    m.add(2, lathe("ball", [(0.0, 0), (0.6, 0.15), (0.9, 0.7), (0.6, 1.3), (0.0, 1.5)], (0, 0, 25), GILT, verts=12))
    m.add(2, box("cross_v", 0.25, 0.25, 2.4, (0, 0, 26.4), GILT))
    m.add(2, box("cross_h", 1.3, 0.25, 0.25, (0, 0, 27.7), GILT))
    return m


def residency(variant="1660"):
    m = Model("residency")
    if variant != "1850":
        m.add(0, box("terrace", 60, 40, 1.2, (0, 0, 0), BUFF_SANDSTONE), "terrace")
        m.add(1, pavilion("library", 38, 22, 8, (0, 2, 1.2), RED_SANDSTONE, BUFF_SANDSTONE, 7, 4, 0.6, True, MARBLE), "pavilion")
        m.add(1, box("tank", 14, 6, 0.4, (0, -14, 1.2), WATER))
        m.add(2, trees("t", [(-24, -14), (24, -14), (-24, 14), (24, 14)], 3.0, z=1.2), "garden")
        return m
    m.add(0, box("terrace", 60, 40, 1.4, (0, 0, 0), shade(CREAM, -0.08)), "terrace")
    m.add(1, arcade_box("core", 36, 22, 8, (0, 2, 1.4), shade(RED_SANDSTONE, 0.2), 5, 3, "N", 0.55), "core")
    m.add(1, box("veranda_floor", 46, 30, 0.4, (0, 0, 1.4), CREAM))
    m.add(1, columns_row("colS", 12, -22, 22, -14.5, 7.8, 0.5, CREAM, 1.8))
    m.add(1, columns_row("colE", 6, -12, 12, 22.5, 7.8, 0.5, CREAM, 1.8, "y"))
    m.add(1, columns_row("colW", 6, -12, 12, -22.5, 7.8, 0.5, CREAM, 1.8, "y"))
    m.add(2, box("entab", 47, 31, 1.2, (0, 0, 9.6), CREAM), "roof")
    m.add(2, box("balustrade", 47, 31, 1.0, (0, 0, 10.8), shade(CREAM, -0.05)))
    m.add(2, box("roof_in", 44, 28, 1.05, (0, 0, 10.8), shade(CREAM, -0.15)))
    m.add(2, stair_up("st", 8, 1.8, 3, 4, 0, -15, "S", CREAM))
    return m


def magazine():
    m = Model("magazine")
    m.add(0, box("yard", 80, 60, 0.3, (0, 0, 0), DUST), "walls")
    m.add(0, wall_run("wall", [(-39, -29), (39, -29), (39, 29), (-39, 29), (-39, -29)], 3.5, 1.2, color="#B9A07E", tower_r=2.2, tower_every=100, merlon=None))
    m.add(0, box("gate", 5, 10, 6.5, (-39, 0, 0), "#D8C6A2"))
    m.add(0, arch_panel("gate_a", 3.6, 4.6, (-41.55, 0, 0), "W", DARK, False))
    for i, (x, y, w, d) in enumerate(((-12, 16, 44, 10), (-12, -16, 44, 10), (24, 0, 12, 40))):
        m.add(1, box(f"store{i}", w, d, 5, (x, y, 0), "#D3BE98"), "stores")
        if d > w:
            m.add(2, gable_roof(f"roof{i}", w, d, 2.6, (x, y, 5), SLATE, 0.5), "roofs")
        else:
            m.add(2, move(rot(gable_roof(f"roof{i}", d, w, 2.6, (0, 0, 0), SLATE, 0.5), 90), x, y, 5), "roofs")
    for k in range(5):  # parked guns on their carriages
        gx = -26 + k * 6
        m.add(1, box(f"gun{k}", 0.6, 3.2, 0.6, (gx, 0, 0.9), BRONZE))
        m.add(1, box(f"carriage{k}", 1.4, 1.8, 0.9, (gx, -0.6, 0.3), TIMBER))
    return m


def begum_samru_palace():
    m = Model("begum-samru-palace")
    m.add(0, box("garden", 60, 40, 0.3, (0, 0, 0), LAWN), "basement")
    m.add(0, arcade_box("basement", 44, 26, 3.6, (0, 2, 0), shade(CREAM, -0.1), 9, 5, "SNEW", 0.55, 0.7, False))
    m.add(1, box("block", 40, 22, 8.5, (0, 3, 3.6), CREAM), "house")
    for f, y in (("S", -8.05), ("N", 14.05)):
        m.add(1, arcade(f"win{f}", 36, 4.5, 9, (0, y, 5), f, "#5A5048", False, 0.35))
    m.add(1, box("cornice", 41, 23, 0.8, (0, 3, 12.1), shade(CREAM, -0.05)))
    m.add(1, box("parapet", 40, 22, 1.0, (0, 3, 12.9), CREAM))
    m.add(2, box("portico_floor", 18, 8, 0.4, (0, -12, 3.6), CREAM), "portico")
    m.add(2, columns_row("cols", 6, -7.5, 7.5, -15, 8.4, 0.55, "#F2EDE2", 4.0))
    m.add(2, box("entab", 18, 8, 1.2, (0, -12, 12.4), CREAM))
    m.add(2, gable_roof("pediment", 18, 8, 2.6, (0, -12, 13.6), CREAM, 0.2))
    for s in (-1, 1):
        m.add(2, stair_up(f"st{s}", 3.2, 3.6, 7, 10, s * 10.5, -11, "S", shade(CREAM, -0.1)))
    return m


def ghaziuddin_madrasa():
    m = Model("ghaziuddin-madrasa")
    W, D = 100, 90
    m.add(0, box("court", W, D, 0.3, (0, 0, 0), PAVE), "cells")
    m.add(0, courtyard_ring("r1", W, D, 4.8, 9, (0, 0, 0), RED_SANDSTONE, DARK))
    m.add(1, courtyard_ring("r2", W - 4, D - 4, 4.2, 7, (0, 0, 4.8), shade(RED_SANDSTONE, 0.06), DARK), "upper")
    m.add(1, iwan("gate", 16, 14, 9, (W / 2 - 3, 0, 0), "E", RED_SANDSTONE, MARBLE))
    m.add(1, trees("t", [(-5, 20), (20, -20), (25, 22), (-5, -24)], 3.0, z=0.3))
    # mosque on the west with three domes, and the founder's marble-screened tomb
    m.add(2, box("mosque", 12, 36, 9, (-W / 2 + 15, 0, 0), RED_SANDSTONE), "mosque")
    m.add(2, arcade("mosque_a", 33, 6, 5, (-W / 2 + 21.05, 0, 0), "E", DARK))
    m.add(2, box("mosque_band", 0.4, 36, 0.8, (-W / 2 + 21.2, 0, 7.6), MARBLE))
    for i, y in enumerate((-11, 0, 11)):
        m.add(3, onion_dome(f"md{i}", 4.2 if i == 1 else 3.4, (-W / 2 + 15, y, 9), RED_SANDSTONE, height=1.45, drum=0.45, finial_color=MARBLE), "domes")
    for f, (x, y) in (("S", (-12, -26)), ("N", (-12, -14)), ("E", (-6, -20)), ("W", (-18, -20))):
        m.add(2, jali_wall(f"jali{f}", 12, 2.6, (x, y, 0.3), f, MARBLE, 5))
    m.add(2, box("grave", 2.4, 1.2, 0.8, (-12, -20, 0.3), MARBLE))
    for sy in (-1, 1):
        m.add(3, minaret(f"min{sy}", 1.0, 13, (-W / 2 + 21.5, sy * 18.5, 0), RED_SANDSTONE, MARBLE, 2, "chhatri"))
    return m


def flagstaff_tower():
    m = Model("flagstaff-tower")
    col = "#CBBEA4"
    m.add(0, cylinder("mound", 7, 0.6, (0, 0, 0), "#9C8E72", verts=20), "tower")
    m.add(0, cylinder("tower", 4.6, 9, (0, 0, 0.6), col, verts=20))
    m.add(0, cylinder("band", 4.8, 0.4, (0, 0, 5.0), shade(col, -0.12), verts=20))
    m.add(0, arch_panel("door", 1.4, 2.6, (0, -4.6, 0.6), "S", DARK, True))
    for k, a in enumerate((0, 90, 180)):
        p = arch_panel(f"slit{k}", 0.5, 1.4, (0, 0, 6.2), "S", DARK, False, 0.25)
        p = rot(p, a + 90)
        m.add(0, move(p, 4.6 * math.cos(math.radians(a)), 4.6 * math.sin(math.radians(a)), 0))
    m.add(1, join([box(f"mer{k}", 0.9, 0.7, 1.0, (4.3 * math.cos(k * math.tau / 16), 4.3 * math.sin(k * math.tau / 16), 9.6), col, rot_z=k * math.tau / 16 + math.pi / 2) for k in range(16)], "mer"), "battlements")
    m.add(1, cylinder("turret", 1.4, 11.2, (3.6, 2.6, 0.6), col, verts=12))
    m.add(1, cylinder("turret_cap", 1.6, 0.4, (3.6, 2.6, 11.8), shade(col, -0.12), verts=12))
    m.add(2, cylinder("staff", 0.14, 11, (0, 0, 9.6), TIMBER, verts=6), "flag")
    m.add(2, box("flag", 0.1, 2.6, 1.6, (0, 1.4, 18.4), "#B23A2A"))
    return m


def hindu_rao_house():
    m = Model("hindu-rao-house")
    m.add(0, box("terrace", 50, 35, 1.2, (0, 0, 0), "#B9A584"), "terrace")
    m.add(1, box("main", 28, 16, 9, (0, 1, 1.2), CREAM), "house")
    m.add(1, arcade("win_s", 24, 4, 6, (0, -7.05, 4.6), "S", "#5A5048", False, 0.35))
    for s in (-1, 1):
        m.add(1, box(f"wing{s}", 10, 13, 6.5, (s * 19, 2, 1.2), shade(CREAM, -0.06)))
    m.add(1, box("veranda_roof", 30, 5, 0.6, (0, -9.5, 6.6), shade(CREAM, -0.04)))
    m.add(1, columns_row("cols", 8, -14, 14, -11.5, 5.4, 0.4, "#F2EDE2", 1.2))
    m.add(2, box("parapet", 28.6, 16.6, 1.0, (0, 1, 10.2), shade(CREAM, -0.08)), "roof")
    for s in (-1, 1):
        m.add(2, box(f"wing_par{s}", 10.4, 13.4, 0.8, (s * 19, 2, 7.7), shade(CREAM, -0.12)))
    m.add(2, stair_up("st", 6, 1.2, 2.5, 3, 0, -12.5, "S", "#B9A584"))
    return m


def metcalfe_house():
    m = Model("metcalfe-house")
    m.add(0, box("terrace", 50, 40, 1.5, (0, 0, 0), "#C2B08E"), "terrace")
    m.add(1, box("core", 24, 16, 8.5, (0, 0, 1.5), "#F1ECE2"), "house")
    m.add(1, box("veranda_floor", 34, 26, 0.3, (0, 0, 1.5), CREAM))
    m.add(1, columns_row("colS", 9, -16, 16, -12.5, 4.8, 0.45, "#F4F0E6", 1.8))
    m.add(1, columns_row("colN", 9, -16, 16, 12.5, 4.8, 0.45, "#F4F0E6", 1.8))
    m.add(1, columns_row("colE", 6, -10, 10, 16.5, 4.8, 0.45, "#F4F0E6", 1.8, "y"))
    m.add(1, columns_row("colW", 6, -10, 10, -16.5, 4.8, 0.45, "#F4F0E6", 1.8, "y"))
    m.add(2, box("veranda_roof", 35, 27, 0.7, (0, 0, 6.6), shade(CREAM, -0.06)), "roof")
    m.add(2, box("parapet", 24.6, 16.6, 0.9, (0, 0, 10.0), shade(CREAM, -0.08)))
    m.add(2, box("portico", 8, 5, 0.7, (0, -16, 6.6), shade(CREAM, -0.06)))
    m.add(2, columns_row("pcol", 2, -3.4, 3.4, -18, 4.8, 0.4, "#F4F0E6", 1.8))
    m.add(2, stair_up("st", 6, 1.5, 3, 4, 0, -20, "S", "#C2B08E"))
    return m


BUILDERS = {
    "delhi/red-fort": lambda: red_fort("1660"),
    "delhi/red-fort-1850": lambda: red_fort("1850"),
    "delhi/salimgarh": salimgarh,
    "delhi/jama-masjid": jama_masjid,
    "delhi/chandni-chowk": lambda: chandni_chowk("1660"),
    "delhi/chandni-chowk-1850": lambda: chandni_chowk("1850"),
    "delhi/jahanara-sarai": jahanara_sarai,
    "delhi/fatehpuri-masjid": fatehpuri_masjid,
    "delhi/kotla": lambda: kotla("1380"),
    "delhi/kotla-ruin": lambda: kotla("ruin"),
    "delhi/kalan-masjid": kalan_masjid,
    "delhi/pir-ghaib": pir_ghaib,
    "delhi/purana-qila": lambda: purana_qila("1545"),
    "delhi/purana-qila-village": lambda: purana_qila("village"),
    "delhi/sher-shah-gate": sher_shah_gate,
    "delhi/khair-ul-manazil": khair_ul_manazil,
    "delhi/humayuns-tomb": humayuns_tomb,
    "delhi/isa-khan-tomb": isa_khan_tomb,
    "delhi/arab-sarai": arab_sarai,
    "delhi/nizamuddin": lambda: nizamuddin("1562"),
    "delhi/nizamuddin-early": lambda: nizamuddin("early"),
    "delhi/zinat-ul-masajid": zinat_ul_masajid,
    "delhi/kashmiri-gate": lambda: kashmiri_gate("1660"),
    "delhi/kashmiri-gate-1850": lambda: kashmiri_gate("1850"),
    "delhi/delhi-gate": delhi_gate,
    "delhi/ajmeri-gate": ajmeri_gate,
    "delhi/lahori-gate": lahori_gate,
    "delhi/st-james-church": st_james_church,
    "delhi/residency": lambda: residency("1660"),
    "delhi/residency-1850": lambda: residency("1850"),
    "delhi/magazine": magazine,
    "delhi/begum-samru-palace": begum_samru_palace,
    "delhi/ghaziuddin-madrasa": ghaziuddin_madrasa,
    "delhi/flagstaff-tower": flagstaff_tower,
    "delhi/hindu-rao-house": hindu_rao_house,
    "delhi/metcalfe-house": metcalfe_house,
}
