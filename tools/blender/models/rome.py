"""Rome landmark miniatures. Each builder returns a chronokit.Model ready to finish()/export()."""
import math
from chronokit import *


def temple_of_saturn():
    m = Model("temple-of-saturn")
    W, D, P, CH = 40, 22, 9, 11
    m.add(0, box("podium", W, D, P, color=shade("limestone", -0.08)), "podium")
    m.add(0, steps("steps", 16, P, 7, (0, -D / 2, 0), shade("limestone", -0.06)))
    pts = peristyle(W - 2.2, D - 2.2, 6, 0)
    pts += [(-(W - 2.2) / 2, -D / 2 + 1.1 + 5.5), ((W - 2.2) / 2, -D / 2 + 1.1 + 5.5)]
    m.add(1, columns("cols", pts, 1.05, CH, (0, 0, P), "limestone"), "columns")
    m.add(1, box("cella", 30, 14, CH, (0, 2.5, P), shade("limestone", -0.04)))
    m.add(1, box("door", 5, 0.6, 6.5, (0, 2.5 - 7 - 0.2, P), "dark"))
    z = P + CH + 0.85
    m.add(2, box("entablature", W, D, 1.8, (0, 0, z), shade("limestone", 0.04)), "roof")
    m.add(2, gable_roof("roof", W, D, 5.6, (0, 0, z + 1.8), "terracotta"))
    return m


def curia_julia(variant="imperial"):
    m = Model("curia-julia")
    W, D, H = 17.6, 25.6, 21
    wall = "brick" if variant == "imperial" else "#B9A28A"
    m.add(0, box("base", W + 2.4, D + 2.4, 1.5, color=shade("limestone", -0.1)), "hall")
    m.add(0, box("walls", W, D, H, (0, 0, 1.5), wall))
    m.add(0, box("marble_dado", W + 0.4, D + 0.4, 7, (0, 0, 1.5), "marble"))
    m.add(0, box("door", 4, 0.6, 9.5, (0, -D / 2 - 0.2, 1.5), "dark"))
    for i in (-1, 0, 1):
        m.add(0, box(f"win{i}", 2.4, 0.6, 4.2, (i * 5.2, -D / 2 - 0.2, 1.5 + 13), "dark"))
    m.add(0, columns("porch", [(-6, -D / 2 - 3), (-2, -D / 2 - 3), (2, -D / 2 - 3), (6, -D / 2 - 3)], 0.6, 8, (0, 0, 1.5), shade("limestone", 0.05)))
    m.add(0, box("porch_roof", 15, 4.5, 1.0, (0, -D / 2 - 2.6, 1.5 + 8 + 0.5), shade("limestone", 0.05)))
    m.add(1, gable_roof("roof", W, D, 4.8, (0, 0, 1.5 + H), "terracotta"), "roof")
    return m


def colosseum():
    m = Model("colosseum")
    RX, RY, T = 94.5, 78, 14
    m.add(0, ellipse_disc("arena", RX * 0.45, RY * 0.45, 0.8, color="sand"), "arena")
    for k in range(4):
        outer = 0.45 + 0.13 * (k + 1)
        inner = (0.45 + 0.13 * k) / outer
        m.add(0 if k < 2 else 1, ellipse_ring(f"cavea{k}", RX * outer, RY * outer, inner, 8 * (k + 1), color=shade("travertine", -0.02 * k)))
    n = 80
    for tier in range(3):
        stage = tier + 1
        z = tier * T
        m.add(stage, ellipse_ring(f"wall{tier}", RX * 0.975, RY * 0.975, 0.94 / 0.975, T, (0, 0, z), color=shade("travertine", -0.04)), ["arcade1", "arcade2", "arcade3"][tier])
        pillars = []
        for i in range(n):
            a = math.tau * i / n
            x, y = RX * 0.985 * math.cos(a), RY * 0.985 * math.sin(a)
            pillars.append(box(f"pil{tier}_{i}", 3.0, 2.6, T, (x, y, z), shade("travertine", 0.06), rot_z=math.atan2(y * RX, x * RY)))
        m.add(stage, join(pillars, f"pillars{tier}"))
        m.add(stage, ellipse_ring(f"cornice{tier}", RX * 1.005, RY * 1.005, 0.93, 1.5, (0, 0, z + T - 1.5), color=shade("travertine", 0.1)))
    m.add(4, ellipse_ring("attic", RX, RY, 0.95, 6, (0, 0, 3 * T), color=shade("travertine", 0.02)), "attic")
    masts = []
    for i in range(40):
        a = math.tau * i / 40
        masts.append(box(f"mast{i}", 1.2, 1.2, 4, (RX * 0.975 * math.cos(a), RY * 0.975 * math.sin(a), 3 * T + 6), shade("travertine", 0.12)))
    m.add(4, join(masts, "masts"))
    return m


def circus_maximus(variant="imperial"):
    m = Model("circus-maximus")
    if variant == "republic":
        L, W, stand, rings = 600, 110, "timber", 2
    else:
        L, W, stand, rings = 621, 118, "travertine", 3
    m.add(0, slab_from_pts("track", stadium_pts(L - 26, W - 26), 0.6, color="sand"), "track")
    for k in range(rings):
        m.add(0, stadium_ring(f"stand{k}", L - 8 * k, W - 8 * k, 8, 5 + 4 * k, color=shade(stand, 0.03 * k)))
    spina_l = L * 0.55
    m.add(1, box("spina", spina_l, 8, 2.5, (L * 0.02, 0, 0), shade(stand, 0.08)), "spina")
    for s in (-1, 1):
        for i in range(3):
            m.add(1, cylinder(f"meta{s}{i}", 1.6, 7, (L * 0.02 + s * (spina_l / 2 + 6 + i * 2.2), (i - 1) * 2.6, 0.6), shade(stand, 0.12), verts=10, r_top=0.3))
    m.add(1, box("shrine1", 6, 4, 5, (L * 0.02 - 60, 0, 2.5), shade(stand, 0.1)))
    m.add(1, box("shrine2", 6, 4, 5, (L * 0.02 + 60, 0, 2.5), shade(stand, 0.1)))
    m.add(1, box("lapcounter", 10, 3, 4, (L * 0.02 + 120, 0, 2.5), "bronze"))
    obelisks = {"republic": [], "imperial": [L * 0.02], "late": [L * 0.02 - spina_l * 0.2, L * 0.02 + spina_l * 0.2]}[variant]
    for i, x in enumerate(obelisks):
        m.add(1, obelisk(f"obelisk{i}", 2.4, 24 if i == 0 else 32, (x, 0, 2.5), "sand"))
    gates = []
    inner_w = W - 40
    for i in range(12):
        gates.append(box(f"gate{i}", 6, inner_w / 12 - 1.5, 8, (-L / 2 + 10, -inner_w / 2 + inner_w / 12 * (i + 0.5), 0), shade(stand, 0.05)))
    m.add(2, join(gates, "carceres"), "gates")
    m.add(2, box("towerA", 14, 8, 14, (-L / 2 + 10, -W / 2 + 4, 0), shade(stand, 0.1)))
    m.add(2, box("towerB", 14, 8, 14, (-L / 2 + 10, W / 2 - 4, 0), shade(stand, 0.1)))
    if variant != "republic":
        m.add(2, box("pulvinar", 30, 14, 16, (L * 0.05, W / 2 - 4, 0), shade(stand, 0.1)))
        m.add(2, gable_roof("pulvinar_roof", 30, 14, 5, (L * 0.05, W / 2 - 4, 16), "terracotta"))
    return m


def arch_of_titus():
    m = Model("arch-of-titus")
    W, H, D = 13.5, 15.4, 4.75
    pier_w, opening = 3.6, 6.3
    for s in (-1, 1):
        m.add(0, box(f"pier{s}", pier_w, D, 6.4, (s * (opening / 2 + pier_w / 2), 0, 0), "marble"), "piers")
        for x in (s * (W / 2 - 0.9), s * (opening / 2 + 0.7)):
            for y in (-D / 2 - 0.3, D / 2 + 0.3):
                m.add(0, cylinder(f"col{s}{x:.0f}{y:.0f}", 0.5, 9.6, (x, y, 0), shade("marble", 0.04), verts=10, r_top=0.44))
    span = box("spandrel", W, D, 5.7, (0, 0, 6.4), "marble")
    cutter = cylinder("cutter", opening / 2, D + 2, (0, 0, 0), "marble", verts=32)
    cutter.rotation_euler = (math.pi / 2, 0, 0)
    cutter.location = (0, 0, 6.4)
    bpy.ops.object.transform_apply(rotation=True)
    m.add(1, boolean_cut(span, cutter), "arch")
    m.add(1, box("cornice", W + 0.6, D + 0.6, 0.6, (0, 0, 12.1), shade("marble", 0.06)))
    m.add(2, box("attic", W - 0.4, D - 0.4, 3.3, (0, 0, 12.7), shade("marble", -0.02)), "attic")
    m.add(2, box("inscription", 7, 0.3, 2.2, (0, -D / 2 + 0.1, 13.2), "bronze"))
    m.add(2, box("quadriga", 4, 2.5, 2.4, (0, 0, 16), "bronze"))
    return m


def temple_of_jupiter(variant="imperial"):
    m = Model("temple-of-jupiter")
    W, D, P, CH = 54, 62, 6, 17
    roof = "gold" if variant == "imperial" else "terracotta"
    m.add(0, box("podium", W, D, P, color=shade("limestone", -0.08)), "podium")
    m.add(0, steps("steps", 30, P, 5, (0, -D / 2, 0), shade("limestone", -0.06)))
    pts = []
    for row in range(3):
        y = -D / 2 + 4 + row * 7
        for i in range(6):
            pts.append((-W / 2 + 4 + (W - 8) * i / 5, y))
    for j in range(1, 6):
        y = -D / 2 + 4 + 14 + (D - 22) * j / 5
        pts += [(-W / 2 + 4, y), (W / 2 - 4, y)]
    m.add(1, columns("cols", pts, 1.15, CH, (0, 0, P), "limestone"), "colonnade")
    m.add(1, box("cella", 44, 38, CH, (0, 9, P), shade("limestone", -0.04)))
    for x in (-7.3, 7.3):
        m.add(1, box(f"groove{x:.0f}", 0.5, 0.6, CH, (x, 9 - 19 - 0.2, P), "dark"))
    for x in (-14.6, 0, 14.6):
        m.add(1, box(f"door{x:.0f}", 4.5, 0.6, 9, (x, 9 - 19 - 0.2, P), "dark"))
    z = P + CH + 0.9
    m.add(2, box("entablature", W, D, 2.2, (0, 0, z), shade("limestone", 0.04)), "roof")
    m.add(2, gable_roof("roof", W, D, 8.5, (0, 0, z + 2.2), roof))
    m.add(2, box("quadriga", 5, 4, 3.2, (0, 0, z + 2.2 + 8.5), "bronze"))
    return m


def roman_forum(variant="imperial"):
    m = Model("roman-forum")
    m.add(0, box("plaza", 170, 70, 0.8, color="plaza"), "plaza")
    imperial = variant == "imperial"
    # south: Basilica Julia (imperial) / Basilica Sempronia (republic)
    if imperial:
        bw, bd, bh, bcol = 101, 49, 18, "marble"
    else:
        bw, bd, bh, bcol = 70, 26, 12, "brick"
    m.add(0, box("bj_base", bw + 2, bd + 2, 1.2, (0, -36 - bd / 2, 0), shade("limestone", -0.1)))
    m.add(1, box("bj_body", bw * 0.8, bd * 0.8, bh, (0, -36 - bd / 2, 1.2), shade(bcol, -0.03)), "halls")
    arc = []
    n = 18 if imperial else 10
    for i in range(n):
        x = -bw / 2 + 2 + (bw - 4) * i / (n - 1)
        arc.append(box(f"bj_p{i}", 1.8, 1.8, bh * 0.55, (x, -36 - 1.6, 1.2), bcol))
    m.add(1, join(arc, "bj_arcade"))
    m.add(1, box("bj_gallery", bw, bd, bh * 0.55, (0, -36 - bd / 2, 1.2 + bh * 0.55), shade(bcol, 0.04)))
    m.add(2, hip_roof("bj_roof", bw * 0.8, bd * 0.8, 7, (0, -36 - bd / 2, 1.2 + bh), "terracotta"), "roofs")
    m.add(2, box("bj_gallery_roof", bw + 1, bd + 1, 0.8, (0, -36 - bd / 2, 1.2 + bh * 1.1), shade("terracotta", -0.05)))
    # north: Basilica Aemilia
    aw, ad, ah = (90, 28, 16) if imperial else (80, 26, 14)
    acol = "marble" if imperial else "brick"
    m.add(0, box("ba_base", aw + 2, ad + 2, 1.2, (10, 36 + ad / 2, 0), shade("limestone", -0.1)))
    m.add(1, box("ba_body", aw, ad, ah, (10, 36 + ad / 2, 1.2), acol))
    arc = []
    for i in range(16 if imperial else 10):
        x = 10 - aw / 2 + 2 + (aw - 4) * i / ((16 if imperial else 10) - 1)
        arc.append(box(f"ba_p{i}", 1.6, 1.6, ah * 0.5, (x, 36 - 1.6, 1.2), shade(acol, 0.05)))
    m.add(1, join(arc, "ba_arcade"))
    m.add(2, hip_roof("ba_roof", aw, ad, 6, (10, 36 + ad / 2, 1.2 + ah), "terracotta"))
    # Temple of Castor and Pollux (south-east)
    if imperial:
        base, body, roof = mini_temple("castor", 32, 50, 7, 14, 8, 11, (62, -50, 0), "marble")
    else:
        base, body, roof = mini_temple("castor", 26, 40, 5, 11, 6, 9, (62, -46, 0), "limestone")
    m.add(0, base); m.add(1, body); m.add(2, roof)
    # Temple of Vesta (round)
    m.add(0, cylinder("vesta_podium", 8, 1.5, (84, -18, 0), shade("limestone", -0.08), verts=24))
    m.add(1, columns("vesta_cols", [(6.3 * math.cos(math.tau * i / 20), 6.3 * math.sin(math.tau * i / 20)) for i in range(20)], 0.45, 6, (84, -18, 1.5), "marble", capital=False))
    m.add(1, cylinder("vesta_cella", 4.6, 6, (84, -18, 1.5), shade("marble", -0.04), verts=24))
    m.add(2, cylinder("vesta_roof", 8.6, 3.2, (84, -18, 7.5), "terracotta", verts=24, r_top=1.0))
    # east end: Temple of Divus Julius (imperial only)
    if imperial:
        base, body, roof = mini_temple("divus_julius", 27, 30, 3.5, 10, 6, 0, (92, 8, 0), "marble")
        m.add(0, base); m.add(1, body); m.add(2, roof)
    # Rostra
    rx, ry = (-78, 0) if imperial else (-60, 28)
    m.add(0, box("rostra", 24, 12, 3, (rx, ry, 0), shade("limestone", -0.02)))
    beaks = [cylinder(f"beak{i}", 0.5, 2.5, (rx - 12.2, ry - 5 + i * 2, 1.2), "bronze", verts=6) for i in range(6)]
    for b in beaks:
        b.rotation_euler = (0, -math.pi / 2, 0)
    m.add(1, join(beaks, "rostra_beaks"))
    # honorific column / statue bases
    for i, (x, y) in enumerate([(-40, 12), (-20, -14), (30, 10)]):
        m.add(1, box(f"base{i}", 3, 3, 2.5, (x, y, 0.8), shade("limestone", 0.05)))
        m.add(1, cylinder(f"column{i}", 0.9, 12 if imperial else 7, (x, y, 3.3), "marble", verts=10))
    return m


BUILDERS = {
    "rome/temple-of-saturn": lambda: temple_of_saturn(),
    "rome/curia-julia": lambda: curia_julia("imperial"),
    "rome/colosseum": lambda: colosseum(),
    "rome/circus-maximus": lambda: circus_maximus("imperial"),
    "rome/circus-maximus-republic": lambda: circus_maximus("republic"),
    "rome/circus-maximus-late": lambda: circus_maximus("late"),
    "rome/arch-of-titus": lambda: arch_of_titus(),
    "rome/temple-of-jupiter": lambda: temple_of_jupiter("imperial"),
    "rome/temple-of-jupiter-republic": lambda: temple_of_jupiter("republic"),
    "rome/roman-forum": lambda: roman_forum("imperial"),
    "rome/roman-forum-republic": lambda: roman_forum("republic"),
}
