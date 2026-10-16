"""Shahjahanabad (Delhi) landmark miniatures."""
import math
from chronokit import *


def red_fort(variant="1660"):
    m = Model("red-fort")
    W, D, T = 550, 950, 9  # x = east-west, y = north-south; river (east) side lower
    m.add(0, box("ground", W, D, 1, color=shade("sandstone", 0.3)), "walls")
    m.add(0, box("wall_w", T, D, 30, (-W / 2, 0, 0), "sandstone"))
    m.add(0, box("wall_e", T, D, 18, (W / 2, 0, 0), shade("sandstone", -0.03)))
    m.add(0, box("wall_n", W, T, 24, (0, D / 2, 0), "sandstone"))
    m.add(0, box("wall_s", W, T, 24, (0, -D / 2, 0), "sandstone"))
    towers = []
    for i in range(9):
        y = -D / 2 + D * i / 8
        towers.append(cylinder(f"tw{i}", 11, 34, (-W / 2, y, 0), shade("sandstone", -0.05), verts=10))
        towers.append(cylinder(f"te{i}", 10, 22, (W / 2, y, 0), shade("sandstone", -0.05), verts=10))
    for i in range(1, 5):
        x = -W / 2 + W * i / 5
        towers.append(cylinder(f"tn{i}", 10, 28, (x, D / 2, 0), shade("sandstone", -0.05), verts=10))
        towers.append(cylinder(f"ts{i}", 10, 28, (x, -D / 2, 0), shade("sandstone", -0.05), verts=10))
    m.add(0, join(towers, "bastions"))
    for (x, y, h) in [(-W / 2, D / 2, 34), (-W / 2, -D / 2, 34), (W / 2, D / 2, 22), (W / 2, -D / 2, 22)]:
        m.add(0, dome(f"chhatri{x:.0f}{y:.0f}", 7, (x, y, h), "white"))
    # gates (stage 1)
    m.add(1, box("lahori_gate", 40, 28, 34, (-W / 2, 0, 0), shade("sandstone", 0.02)), "gates")
    for s in (-1, 1):
        m.add(1, cylinder(f"lahori_t{s}", 8, 44, (-W / 2 - 6, s * 24, 0), shade("sandstone", -0.04), verts=8))
        m.add(1, dome(f"lahori_d{s}", 7, (-W / 2 - 6, s * 24, 44), "white"))
    m.add(1, box("lahori_arch", 14, 2, 18, (-W / 2 - 20.5, 0, 2), "dark"))
    if variant == "1660":
        m.add(1, box("barbican_n", 70, 8, 16, (-W / 2 - 50, 36, 0), shade("sandstone", -0.02)))
        m.add(1, box("barbican_s", 70, 8, 16, (-W / 2 - 50, -36, 0), shade("sandstone", -0.02)))
        m.add(1, box("barbican_w", 8, 80, 16, (-W / 2 - 85, 0, 0), shade("sandstone", -0.02)))
    m.add(1, box("delhi_gate", 34, 24, 30, (0, -D / 2, 0), shade("sandstone", 0.02)))
    for s in (-1, 1):
        m.add(1, cylinder(f"delhi_t{s}", 7, 38, (s * 20, -D / 2 - 5, 0), shade("sandstone", -0.04), verts=8))
        m.add(1, dome(f"delhi_d{s}", 6, (s * 20, -D / 2 - 5, 38), "white"))
    m.add(1, box("delhi_arch", 2, 12, 16, (0, -D / 2 - 17.5, 2), "dark"))
    # interior (stage 2): the axis from the Lahori Gate east to the Diwan-i-Aam, river palaces along the east wall
    m.add(2, box("chhatta_chowk", 70, 14, 11, (-W / 2 + 60, 0, 1), shade("sandstone", 0.08)), "palaces")
    m.add(2, box("naubat_khana", 26, 16, 16, (-W / 2 + 125, 0, 1), "sandstone"))
    m.add(2, box("diwan_i_aam_base", 70, 30, 2, (-30, 0, 1), shade("sandstone", -0.06)))
    m.add(2, box("diwan_i_aam", 60, 24, 10, (-30, 0, 3), shade("#D9B8A2", 0.0)))
    pil = [box(f"daa_p{i}", 1.6, 1.6, 9, (-30 - 27 + 54 * i / 8, -11, 3), "white") for i in range(9)]
    m.add(2, join(pil, "diwan_pillars"))
    m.add(2, box("diwan_i_aam_roof", 62, 26, 1.5, (-30, 0, 13), shade("sandstone", 0.04)))
    # river-front marble pavilions
    for name, y, w, d, h in [("mumtaz_mahal", -150, 30, 22, 9), ("rang_mahal", -60, 50, 26, 10), ("khas_mahal", 10, 30, 20, 10), ("diwan_i_khas", 75, 34, 20, 10), ("hammam", 130, 26, 20, 9)]:
        m.add(2, box(name, w, d, h, (W / 2 - 60, y, 1), "white"))
        m.add(2, box(name + "_roof", w + 1.5, d + 1.5, 1.2, (W / 2 - 60, y, 1 + h), shade("white", -0.05)))
        for sx in (-1, 1):
            for sy in (-1, 1):
                m.add(2, dome(f"{name}_c{sx}{sy}", 2.4, (W / 2 - 60 + sx * (w / 2 - 3), y + sy * (d / 2 - 3), 1 + h + 1.2), "white"))
    m.add(2, box("nahr", 6, 300, 0.6, (W / 2 - 60, -10, 1), "water"))
    if variant == "1660":
        m.add(2, box("moti_masjid", 16, 12, 8, (W / 2 - 100, 170, 1), "white"))
        for i in (-1, 0, 1):
            m.add(2, dome(f"moti_d{i}", 2.6, (W / 2 - 100 + i * 5, 170, 9), "white", squash=1.2))
    m.add(2, box("hayat_baksh", 150, 170, 0.6, (W / 2 - 120, 300, 1), "green"))
    m.add(2, box("sawan", 14, 14, 7, (W / 2 - 120, 385, 1.6), "white"))
    m.add(2, box("bhadon", 14, 14, 7, (W / 2 - 120, 215, 1.6), "white"))
    return m


def jama_masjid():
    """Built in the kit frame: prayer hall to the north (+y); content rotates it to face west."""
    m = Model("jama-masjid")
    W, D, P = 120, 100, 8
    m.add(0, box("platform", W + 24, D + 24, P, color=shade("sandstone", -0.08)), "platform")
    m.add(0, steps("steps_s", 34, P, 7, (0, -(D + 24) / 2, 0), shade("sandstone", -0.06), tread=1.6, direction=-1))
    for s in (-1, 1):
        st = steps(f"steps_{s}", 30, P, 7, (0, 0, 0), shade("sandstone", -0.06), tread=1.6, direction=-1)
        st.rotation_euler[2] = s * math.pi / 2
        st.location = (s * (W + 24) / 2, 0, 0)
        bpy.ops.object.transform_apply(rotation=True, location=True)
        m.add(0, st)
    # courtyard arcades + gates (stage 1)
    hall_d = 28
    for s in (-1, 1):
        m.add(1, box(f"riwaq_{s}", 5, D - hall_d, 7, (s * W / 2, -hall_d / 2, P), "sandstone"), "courtyard")
        arc = [box(f"ra{s}{i}", 1.6, 1.6, 6, (s * (W / 2 - 3.5), -D / 2 + 6 + (D - hall_d - 12) * i / 9, P), shade("sandstone", 0.08)) for i in range(10)]
        m.add(1, join(arc, f"riwaq_arc{s}"))
        m.add(1, box(f"gate_{s}", 18, 14, 17, (s * W / 2, -hall_d / 2, P), shade("sandstone", 0.02)))
        m.add(1, dome(f"gate_d{s}", 3, (s * W / 2, -hall_d / 2, P + 17), "white"))
    m.add(1, box("riwaq_s", W, 5, 7, (0, -D / 2, P), "sandstone"))
    arc = [box(f"rs{i}", 1.6, 1.6, 6, (-W / 2 + 6 + (W - 12) * i / 15, -D / 2 + 3.5, P), shade("sandstone", 0.08)) for i in range(16)]
    m.add(1, join(arc, "riwaq_arc_s"))
    m.add(1, box("gate_main", 28, 16, 22, (0, -D / 2, P), shade("sandstone", 0.02)))
    m.add(1, box("gate_main_arch", 10, 1, 14, (0, -D / 2 - 8.3, P + 1), "dark"))
    for s in (-1, 1):
        m.add(1, dome(f"gate_main_d{s}", 3, (s * 10, -D / 2, P + 22), "white"))
    m.add(1, cylinder("hauz", 9, 1.2, (0, -hall_d / 2, P), "water", verts=8))
    m.add(1, cylinder("hauz_rim", 10, 0.8, (0, -hall_d / 2, P), "white", verts=8))
    # prayer hall, domes, minarets (stage 2)
    hall_y = D / 2 - hall_d / 2
    m.add(2, box("hall", W - 10, hall_d, 16, (0, hall_y, P), "sandstone"), "prayer_hall")
    arc = [box(f"ha{i}", 2, 2, 12, (-W / 2 + 10 + (W - 20) * i / 10, hall_y - hall_d / 2 + 1.2, P), shade("sandstone", 0.06)) for i in range(11)]
    m.add(2, join(arc, "hall_arcade"))
    m.add(2, box("pishtaq", 30, 18, 26, (0, hall_y - 4, P), shade("sandstone", 0.03)))
    m.add(2, box("pishtaq_arch", 14, 1, 18, (0, hall_y - 13.5, P + 2), "dark"))
    for i, x in enumerate((-33, 0, 33)):
        r = 12.5 if i == 1 else 10.5
        m.add(2, cylinder(f"drum{i}", r * 0.95, 4, (x, hall_y + 2, P + 16), shade("sandstone", 0.02), verts=24))
        m.add(2, dome(f"dome{i}", r, (x, hall_y + 2, P + 20), "white", squash=1.18, segments=24, rings=12))
        m.add(2, cylinder(f"finial{i}", 0.9, 4, (x, hall_y + 2, P + 20 + r * 1.18), "gold", verts=6, r_top=0.2))
    for s in (-1, 1):
        x = s * (W / 2 - 3)
        m.add(2, cylinder(f"minaret{s}", 3.4, 40, (x, hall_y - hall_d / 2 + 2, P), "sandstone", verts=8, r_top=2.6))
        for k in range(3):
            m.add(2, cylinder(f"min_band{s}{k}", 3.6 - k * 0.25, 1.2, (x, hall_y - hall_d / 2 + 2, P + 12 * (k + 1)), "white", verts=8))
        m.add(2, cylinder(f"min_gallery{s}", 4.4, 1.0, (x, hall_y - hall_d / 2 + 2, P + 40), "white", verts=8))
        m.add(2, dome(f"min_dome{s}", 3.4, (x, hall_y - hall_d / 2 + 2, P + 41), "white"))
    return m


def chandni_chowk():
    m = Model("chandni-chowk")
    L, W = 1300, 40
    m.add(0, box("street", L, W + 44, 0.8, color="plaza"), "street")
    m.add(0, box("canal", L * 0.95, 7, 1.0, color="water"))
    m.add(0, cylinder("pool_rim", 16, 1.0, (0, 0, 0.2), "white", verts=8))
    m.add(0, cylinder("pool", 14, 1.4, (0, 0, 0.2), "water", verts=8))
    n = 40
    sl = L / n
    shops = []
    for i in range(n):
        x = -L / 2 + sl * (i + 0.5)
        for s in (-1, 1):
            h = 7 + ((i * 7 + (s + 1)) % 5)
            d = 14 + ((i * 3) % 6)
            col = shade("brick", 0.08) if (i + s) % 3 == 0 else ("brick" if (i + s) % 4 else shade("brick", -0.06))
            shops.append(box(f"shop{i}{s}", sl - 1.6, d, h, (x, s * (W / 2 + 3 + d / 2), 0.8), col))
            shops.append(box(f"roof{i}{s}", sl - 1.0, d + 0.8, 0.8, (x, s * (W / 2 + 3 + d / 2), 0.8 + h), "#8E5A3C"))
            shops.append(box(f"arc{i}{s}", sl - 1.6, 4, 4.5, (x, s * (W / 2 + 3 + 1.5), 0.8), shade("brick", 0.14)))
    m.add(1, join(shops, "shops"), "shops")
    m.add(1, box("kotwali", 40, 26, 14, (60, W / 2 + 3 + 13, 0.8), "sandstone"))
    m.add(1, box("kotwali_roof", 41, 27, 1.2, (60, W / 2 + 3 + 13, 14.8), shade("sandstone", 0.1)))
    # Fatehpuri Masjid at the west end (stage 2) and trees along the canal
    fx = -L / 2 - 30
    m.add(2, box("fatehpuri_platform", 56, 48, 2, (fx, 0, 0), shade("sandstone", -0.08)), "mosque")
    m.add(2, box("fatehpuri_hall", 44, 14, 11, (fx - 18, 0, 2), "sandstone"))
    m.add(2, dome("fatehpuri_dome", 7.5, (fx - 18, 0, 13), "white", squash=1.15))
    for s in (-1, 1):
        m.add(2, cylinder(f"fatehpuri_min{s}", 2, 20, (fx - 18, s * 21, 2), "sandstone", verts=8))
        m.add(2, dome(f"fatehpuri_md{s}", 2.2, (fx - 18, s * 21, 22), "white"))
    m.add(2, box("fatehpuri_wall", 2, 46, 5, (fx + 26, 0, 2), "sandstone"))
    trees = []
    for i in range(18):
        x = -L / 2 + 40 + (L - 80) * i / 17
        if abs(x) < 24:
            continue
        for s in (-1, 1):
            trees.append(cylinder(f"trunk{i}{s}", 0.7, 4, (x, s * 9, 0.8), "timber", verts=6))
            trees.append(dome(f"crown{i}{s}", 4, (x, s * 9, 4.2), "green", squash=1.3, segments=10, rings=6))
    m.add(2, join(trees, "trees"))
    return m


BUILDERS = {
    "delhi/red-fort": lambda: red_fort("1660"),
    "delhi/jama-masjid": lambda: jama_masjid(),
    "delhi/chandni-chowk": lambda: chandni_chowk(),
}
