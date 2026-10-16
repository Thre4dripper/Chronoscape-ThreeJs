"""Hero miniatures: the main monuments at real architectural detail (baked to light meshes by bake_assets.py)."""
import math, random
import bpy
from chronokit import Model, box, cylinder, dome, join, shade, ellipse_ring, ellipse_disc, stadium_ring, stadium_pts, slab_from_pts, gable_roof, hip_roof, boolean_cut, mesh_from
from archkit import (MARBLE, TRAV, BRICK, TILE, BRONZE, GOLD, DARK, PLASTER, place, copy_at, cyl_x, cyl_y, half_cyl_x, half_cyl_y, column, colonnade,
                     entablature, pediment, statue, steps_front, tiled_hip_roof, arch_bay, thermal_window, stepped_dome, ring_of)

SAND, GRASS, WATER, TREE = "#C8A574", "#8FA07A", "#65888A", "#5d7a46"


def trees(name, pts, r=3.0, color=TREE):
    objs = []
    for i, (x, y, z) in enumerate(pts):
        objs.append(cylinder(f"{name}_t{i}", r * 0.12, r * 0.9, (x, y, z), "#6a5238", verts=6))
        objs.append(dome(f"{name}_c{i}", r, (x, y, z + r * 0.8), color, squash=1.25, segments=10, rings=6))
    return join(objs, name) if objs else None


# ====================================================================== Colosseum

def colosseum(variant="intact"):
    m = Model("colosseum" + ("" if variant == "intact" else "-" + variant))
    RX, RY = 94.5, 78.0
    N = 80
    storeys = [(0.0, 10.5, "tuscan"), (10.5, 11.8, "ionic"), (22.3, 11.6, "corinthian")]
    attic_z, attic_h = 33.9, 9.2
    ruined = lambda i, a: variant == "ruin" and (math.radians(195) < a < math.radians(300))

    # ---- arena, podium and cavea
    m.add(0, ellipse_disc("arena", RX * 0.42, RY * 0.36, 0.5, (0, 0, 0), SAND, verts=64), "arena")
    hyp = [box(f"hyp{k}", RX * 0.7, 0.35, 0.05, (0, -RY * 0.25 + k * RY * 0.05, 0.5), "#9c7a52") for k in range(11)]
    hyp.append(box("hyp_axis", 0.6, RY * 0.62, 0.05, (0, 0, 0.5), "#9c7a52"))
    m.add(0, join(hyp, "hypogeum_lines"))
    m.add(0, ellipse_ring("podium", RX * 0.45, RY * 0.39, 0.93, 4.0, (0, 0, 0), MARBLE, n=96))
    m.add(0, ellipse_ring("podium_parapet", RX * 0.45, RY * 0.39, 0.985, 1.0, (0, 0, 4.0), shade(MARBLE, 0.05), n=96))
    rows = 26
    for k in range(rows):
        t0, t1 = k / rows, (k + 1) / rows
        f0, f1 = 0.45 + 0.5 * t0, 0.45 + 0.5 * t1
        z = 4.0 + t0 * 30.0
        band = 1 if k % 7 == 6 else 0   # praecinctio walls between the tiers
        col = shade(TRAV, -0.06 if k % 2 else -0.02)
        m.add(1 if k < 14 else 2, ellipse_ring(f"seat{k}", RX * f1, RY * f1, f0 / f1, 30.0 / rows * (1.6 if band else 1), (0, 0, z), col, n=120))
    vom = []
    for i in range(40):
        a = math.tau * i / 40
        for f, z in ((0.58, 11.0), (0.74, 20.5)):
            vom.append(box(f"vom{i}_{f}", 2.2, 1.2, 2.2, (RX * f * math.cos(a), RY * f * math.sin(a), z), DARK, rot_z=a + math.pi / 2))
    m.add(1, join(vom, "vomitoria"))
    # colonnade of the summum maenianum at the top of the seating
    m.add(3, ring_of(lambda: column("smc", 0, 0, 0, 7.0, 0.35, "corinthian", PLASTER), 96, RX * 0.94, RY * 0.94, 34.0, "summum_cols"), "upper")
    m.add(3, ellipse_ring("summum_roof", RX * 0.955, RY * 0.955, 0.965, 0.8, (0, 0, 41.0), shade(TILE, -0.05), n=120))

    # ---- outer facade: three arcaded storeys
    for si, (z, h, order) in enumerate(storeys):
        def bay(h=h, order=order, si=si):
            w = 2 * math.pi * math.sqrt((RX ** 2 + RY ** 2) / 2) / N + 0.15
            parts = [arch_bay(f"bay{si}", w, h, 2.4, 2.15, h * 0.62, TRAV)]
            parts.append(column(f"halfcol{si}", -w / 2, -1.25, 0, h - 1.2, 0.55, order, shade(TRAV, 0.05)))
            parts.append(box(f"band{si}", w, 1.0, 1.2, (0, -0.35, h - 1.2), shade(TRAV, 0.07)))
            if si > 0:
                parts.append(statue(f"st{si}", 0, -0.2, 0.2, 2.6, shade(MARBLE, -0.06)))
            return join(parts, f"bay{si}")
        skip = (lambda i, a, si=si: ruined(i, a) and si >= 1)
        m.add(si + 1, ring_of(bay, N, RX, RY, z, f"storey{si}", skip=skip), f"storey{si}")
        m.add(si + 1, ellipse_ring(f"inner_wall{si}", RX * 0.985, RY * 0.985, 0.955, h, (0, 0, z), shade(TRAV, -0.12), n=120))

    # ---- attic: pilasters, small windows, corbels and the velarium masts
    def attic_bay(i_odd=[0]):
        w = 2 * math.pi * math.sqrt((RX ** 2 + RY ** 2) / 2) / N + 0.15
        i_odd[0] += 1
        parts = [box("attic_wall", w, 2.4, attic_h, (0, 0, 0), TRAV),
                 box("pilaster", 0.9, 0.5, attic_h - 1.0, (-w / 2, -1.3, 0), shade(TRAV, 0.06)),
                 box("attic_cornice", w, 1.4, 1.0, (0, -0.4, attic_h - 1.0), shade(TRAV, 0.08))]
        if i_odd[0] % 2:
            parts.append(box("attic_win", 1.4, 0.4, 2.0, (0, -1.25, attic_h * 0.42), DARK))
        else:
            parts.append(box("shield", 1.6, 0.25, 1.6, (0, -1.3, attic_h * 0.42), GOLD))
        for s in (-1, 1):
            parts.append(box(f"corbel{s}", 0.5, 0.6, 0.6, (s * w * 0.3, -1.4, attic_h - 2.6), shade(TRAV, 0.05)))
        parts.append(cylinder("mast", 0.22, 5.0, (w * 0.3, -0.6, attic_h), "#8a6a4a", verts=6))
        return join(parts, "attic_bay")
    if variant != "ruin":
        m.add(4, ring_of(attic_bay, N, RX, RY, attic_z, "attic"), "attic")
    else:
        m.add(4, ring_of(attic_bay, N, RX, RY, attic_z, "attic", skip=lambda i, a: ruined(i, a)), "attic")
        rnd = random.Random(4)
        rub = [box(f"rub{i}", rnd.uniform(2, 6), rnd.uniform(2, 5), rnd.uniform(1, 3), (RX * 1.05 * math.cos(a), RY * 1.05 * math.sin(a), 0), shade(TRAV, -0.1), rot_z=rnd.random() * 3)
               for i, a in enumerate([math.radians(200 + k * 5) for k in range(18)])]
        m.add(4, join(rub, "rubble"))
        m.add(4, trees("ruin_trees", [(RX * 0.7 * math.cos(a), RY * 0.7 * math.sin(a), 6 + 20 * rnd.random()) for a in [math.radians(rnd.uniform(0, 360)) for _ in range(14)]], 2.6))
    if variant == "fortress":
        for k, a in enumerate([0.4, 1.9, 3.3, 4.8]):
            x, y = RX * 0.93 * math.cos(a), RY * 0.93 * math.sin(a)
            m.add(4, box(f"keep{k}", 9, 9, 16, (x, y, 43), BRICK))
            m.add(4, join([box(f"merlon{k}_{j}", 1.4, 1.4, 1.6, (x + (j % 3 - 1) * 3.2, y + (j // 3 - 1) * 3.2, 59), BRICK) for j in range(9) if j != 4], f"merlons{k}"))
        m.add(4, box("frangipane_hall", 34, 16, 14, (0, RY * 0.66, 34), BRICK))
        m.add(4, tiled_hip_roof("frangipane_roof", 34, 16, 5, (0, RY * 0.66, 48)))
    return m


# ====================================================================== Imperial baths

def thermae(name, W, D, variant="intact", cb=(0.62, 0.44)):
    m = Model(name)
    intact = variant in ("intact", "church", "construction")
    roofless = variant in ("ruin",)
    rnd = random.Random(len(name))
    # ---- precinct: garden ground, perimeter shops, side exedrae, cisterns and stadium at the back
    m.add(0, box("ground", W, D, 0.6, (0, 0, 0), GRASS), "precinct")
    m.add(0, box("paths_x", W * 0.9, 6, 0.1, (0, -D * 0.3, 0.6), "#D6C39E"))
    shop_w = 6.0
    def shop():
        return join([arch_bay("shop", shop_w, 7.0, 7.0, 1.6, 3.6, BRICK, keystone=False), box("shop_roof", shop_w, 7.4, 0.8, (0, 0, 7.0), TILE)], "shop")
    proto = shop()
    shops = []
    for k in range(int(W / shop_w)):
        x = -W / 2 + shop_w * (k + 0.5)
        if abs(x) < 14:
            continue
        shops.append(copy_at(proto, (x, -D / 2 + 3.5, 0.6)))
    for k in range(int(D * 0.55 / shop_w)):
        y = -D / 2 + 10 + shop_w * k
        shops.append(copy_at(proto, (-W / 2 + 3.5, y, 0.6), math.pi / 2))
        shops.append(copy_at(proto, (W / 2 - 3.5, y, 0.6), -math.pi / 2))
    bpy.data.objects.remove(proto, do_unlink=True)
    m.add(0, join(shops, "tabernae"))
    m.add(0, box("gate", 24, 9, 12, (0, -D / 2 + 4.5, 0.6), MARBLE))
    m.add(2, pediment("gate_ped", 24, 9, 12.6, 3.5, -D / 2, MARBLE, TILE, ridges=False, statues=False))
    for s in (-1, 1):
        m.add(0, ellipse_ring(f"exedra{s}", 34, 34, 0.86, 14, (s * (W / 2 - 4), D * 0.05, 0.6), BRICK, n=40, arc=math.pi, start=(math.pi / 2 if s > 0 else -math.pi / 2)))
        if intact:
            m.add(2, half_cyl_y(f"exedra_vault{s}", 5, 1, (0, 0, 0), TILE) if False else box(f"exedra_roofline{s}", 3, 3, 0.1, (s * (W / 2 - 4), D * 0.05, 14.6), TILE))
    m.add(0, box("cisterns", W * 0.5, 16, 10, (0, D / 2 - 9, 0.6), shade(BRICK, -0.05)))
    m.add(0, join([box(f"cistern_arch{k}", 4, 0.4, 5, (-W * 0.24 + k * W * 0.48 / 11, D / 2 - 17.2, 0.6), DARK) for k in range(12)], "cistern_arches"))
    m.add(1, ellipse_ring("stadium_seats", W * 0.26, 26, 0.7, 9, (0, D / 2 - 18, 0.6), shade(MARBLE, -0.06), n=48, arc=math.pi, start=math.pi))
    m.add(1, trees("garden", [(rnd.uniform(-W * 0.42, W * 0.42), rnd.uniform(-D * 0.42, -D * 0.27), 0.6) for _ in range(22)] + [(rnd.uniform(-W * 0.42, W * 0.42), rnd.uniform(D * 0.2, D * 0.36), 0.6) for _ in range(18)], 3.2))

    # ---- the central bath block
    cw, cd = W * cb[0], D * cb[1]
    cy = -D * 0.02
    wall = PLASTER if variant == "church" else BRICK
    m.add(0, box("platform", cw + 4, cd + 4, 1.4, (0, cy, 0.6), shade(MARBLE, -0.1)))
    z0 = 2.0
    # frigidarium: three groin-vaulted bays along X with thermal windows in the clerestory
    fw, fd, fh = cw * 0.34, cd * 0.42, 26.0
    if intact:
        m.add(1, box("frig_walls", fw, fd, fh, (0, cy, z0), wall), "halls")
        bay_w = fw / 3
        vaults = [half_cyl_x("frig_vault_x", fd / 2, fw, (0, cy, z0 + fh), TILE if variant != "church" else shade(TILE, -0.05), verts=24)]
        for k in range(3):
            x = -fw / 2 + bay_w * (k + 0.5)
            vaults.append(half_cyl_y(f"frig_vault_y{k}", bay_w / 2, fd + 1.0, (x, cy, z0 + fh), TILE, verts=20))
            for s in (-1, 1):
                vaults.append(thermal_window(f"frig_win{k}{s}", bay_w * 0.36, 1.2, (x, cy + s * (fd / 2 + 0.1), z0 + fh - 6), PLASTER, rot_z=0 if s < 0 else math.pi))
        m.add(2, join(vaults, "frig_vaults"), "vaults")
        # buttresses along the long sides
        m.add(1, join([box(f"butt{k}{s}", 3, 6, fh * 0.75, (-fw / 2 + k * fw / 3, cy + s * (fd / 2 + 3), z0), shade(wall, -0.05)) for k in range(4) for s in (-1, 1)], "buttresses"))
    # tepidarium and the caldarium rotunda to the south (front)
    tw, td = fw * 0.35, cd * 0.16
    cr = cd * 0.24
    ccy = cy - fd / 2 - td - cr * 0.85
    if intact:
        m.add(1, box("tepidarium", tw, td, 18, (0, cy - fd / 2 - td / 2, z0), wall))
        m.add(2, half_cyl_x("tep_vault", td / 2, tw, (0, cy - fd / 2 - td / 2, z0 + 18), TILE, verts=16))
        m.add(1, cylinder("caldarium", cr, 30, (0, ccy, z0), wall, verts=40))
        wins = []
        for k in range(9):
            a = math.pi + math.pi * (k + 0.5) / 9
            for zz in (8, 19):
                wins.append(box(f"cw{k}_{zz}", 3.2, 1.0, 6.5, ((cr + 0.1) * math.cos(a), ccy + (cr + 0.1) * math.sin(a), z0 + zz), DARK, rot_z=a + math.pi / 2))
        m.add(1, join(wins, "caldarium_windows"))
        m.add(2, stepped_dome("caldarium_dome", cr * 1.02, z0 + 30, shade(TILE, -0.08), steps=3), "domes")
    # natatio: open-air pool to the north with a monumental screen wall
    nw, nd = fw * 1.25, cd * 0.26
    ny = cy + fd / 2 + nd / 2
    m.add(1, box("natatio_floor", nw, nd, 0.6, (0, ny, z0), MARBLE))
    m.add(1, box("natatio_water", nw - 4, nd - 4, 0.3, (0, ny, z0 + 0.5), WATER))
    if intact:
        m.add(1, box("screen_wall", nw, 3, 22, (0, ny + nd / 2, z0), MARBLE))
        for tier, (zz, hh) in enumerate([(0, 9), (9, 8)]):
            m.add(1, colonnade(f"screen_cols{tier}", [(-nw / 2 + 3 + k * (nw - 6) / 13, ny + nd / 2 - 2.2) for k in range(14)], z0 + zz, hh - 1, 0.45, "corinthian", MARBLE))
            for k in range(13):
                m.add(1, statue(f"niche_st{tier}{k}", -nw / 2 + 3 + (k + 0.5) * (nw - 6) / 13, ny + nd / 2 - 1.2, z0 + zz + 0.5, 3.0, shade(MARBLE, -0.08)))
    # palaestrae: colonnaded courts to east and west, each with an apsed hall
    for s in (-1, 1):
        px = s * (fw / 2 + (cw / 2 - fw / 2) / 2 + 2)
        pw, pd = (cw / 2 - fw / 2) - 6, cd * 0.62
        m.add(0, box(f"pal_floor{s}", pw, pd, 0.4, (px, cy, z0), "#D6C39E"))
        pts = [(px - pw / 2 + 2 + k * (pw - 4) / 9, cy + t * (pd / 2 - 2)) for k in range(10) for t in (-1, 1)] + [(px + t * (pw / 2 - 2), cy - pd / 2 + 2 + k * (pd - 4) / 9) for k in range(1, 9) for t in (-1, 1)]
        if intact:
            m.add(1, colonnade(f"pal_cols{s}", pts, z0, 8, 0.4, "ionic", MARBLE))
            for t in (-1, 1):
                m.add(2, box(f"pal_roof{s}{t}", pw, 5, 0.6, (px, cy + t * (pd / 2 - 2), z0 + 8), TILE))
            m.add(1, ellipse_ring(f"pal_exedra{s}", pd * 0.22, pd * 0.22, 0.85, 16, (px + s * pw / 2, cy, z0), wall, n=24, arc=math.pi, start=(-math.pi / 2 if s > 0 else math.pi / 2)))
        # side halls between the courts and the frigidarium
        if intact:
            for t in (-1, 1):
                hy = cy + t * (pd / 2 + (cd / 2 - pd / 2) / 2)
                hd = (cd / 2 - pd / 2) - 2
                m.add(1, box(f"side_hall{s}{t}", pw, hd, 16, (px, hy, z0), wall))
                m.add(2, tiled_hip_roof(f"side_roof{s}{t}", pw, hd, 4, (px, hy, z0 + 16)))
    # ---- variants
    if variant == "church":
        m.add(3, box("church_front", 26, 4, 22, (0, cy - fd / 2 - 2, z0), PLASTER), "church")
        m.add(3, cylinder("cross_post", 0.3, 6, (0, cy, z0 + fh + fd / 2), GOLD, verts=6))
        m.add(3, box("cross_bar", 2.4, 0.3, 0.3, (0, cy, z0 + fh + fd / 2 + 4), GOLD))
    if variant == "construction":
        from rome_fora import scaffold, crane
        m.add(1, box("frig_walls_part", fw, fd, fh * 0.6, (0, cy, z0), wall), "site")
        m.add(2, scaffold("frig_scaffold", -fw / 2, fw / 2, cy - fd / 2, cy + fd / 2, fh * 0.75), "scaffold")
        m.add(2, crane("crane1", -fw / 2 - 8, cy, 34))
        m.add(2, crane("crane2", fw / 2 + 8, cy - 10, 30))
        m.add(1, cylinder("caldarium_part", cr, 12, (0, ccy, z0), wall, verts=40))
    if roofless:
        # standing walls of the great halls, broken off at different heights, with trees growing in them
        segs = []
        for k in range(16):
            a = rnd.random() * math.tau
            x, y = rnd.uniform(-cw * 0.45, cw * 0.45), cy + rnd.uniform(-cd * 0.45, cd * 0.45)
            segs.append(box(f"ruin_wall{k}", rnd.uniform(8, 30), 3, rnd.uniform(6, 26), (x, y, z0), shade(BRICK, rnd.uniform(-0.1, 0.05)), rot_z=round(a / (math.pi / 2)) * math.pi / 2))
        m.add(1, join(segs, "ruin_walls"), "ruins")
        m.add(1, box("frig_shell", fw, 3, fh, (0, cy - fd / 2, z0), BRICK))
        m.add(1, box("frig_shell2", fw, 3, fh * 0.8, (0, cy + fd / 2, z0), BRICK))
        m.add(1, ellipse_ring("caldarium_shell", cr, cr, 0.92, 22, (0, ccy, z0), BRICK, n=32, arc=math.pi * 1.3, start=math.pi * 0.85))
        m.add(2, trees("ruin_trees", [(rnd.uniform(-cw / 2, cw / 2), cy + rnd.uniform(-cd / 2, cd / 2), z0) for _ in range(24)], 3.4), "vegetation")
    return m


# ====================================================================== Pantheon

def pantheon():
    m = Model("pantheon")
    R, H = 28.0, 21.0
    m.add(0, box("piazza", 70, 95, 0.4, (0, -8, 0), "#D6C39E"), "base")
    m.add(0, cylinder("plinth", R + 1.2, 1.5, (0, 0, 0.4), shade(BRICK, -0.08), verts=64))
    # drum with three cornices and brick relieving arches
    for k, (z, h) in enumerate([(1.9, 8.2), (10.1, 6.8), (16.9, 6.0)]):
        m.add(1, cylinder(f"drum{k}", R - k * 0.15, h, (0, 0, z), BRICK if k else shade(BRICK, 0.04), verts=64), "drum")
        m.add(1, cylinder(f"drum_cornice{k}", R + 0.5 - k * 0.15, 0.7, (0, 0, z + h - 0.35), MARBLE, verts=64))
    arches = []
    for i in range(24):
        a = math.tau * i / 24
        if -math.pi * 0.62 < math.atan2(math.sin(a), math.cos(a)) < -math.pi * 0.38:
            continue
        arches.append(box(f"relief{i}", 4.5, 0.4, 0.4, ((R + 0.05) * math.cos(a), (R + 0.05) * math.sin(a), 13.5), shade(BRICK, 0.12), rot_z=a + math.pi / 2))
    m.add(1, join(arches, "relieving_arches"))
    m.add(2, stepped_dome("dome", R - 0.4, 1.9 + H + 0.2, "#9aa0a0", steps=6, oculus=4.5), "dome")
    # intermediate block with pilasters and a second pediment
    m.add(1, box("block", 34, 8, 30, (0, -R + 0.5, 1.9), BRICK))
    m.add(1, join([box(f"pilaster{k}", 1.4, 0.5, 14, (-15 + k * 6, -R - 3.3, 1.9), MARBLE) for k in range(6)], "pilasters"))
    m.add(2, pediment("upper_pediment", 34, 4, 31.9, 5.2, -R - 3.5, MARBLE, "#8a8f8c", ridges=False, statues=False))
    # portico: 8 front columns of grey granite, 16 in all, on a stepped podium, under a bronze-tiled roof
    py0 = -R - 4 - 15.6
    m.add(0, box("portico_floor", 34, 15.6, 1.5, (0, py0 + 7.8, 0.4), MARBLE))
    m.add(0, steps_front("portico_steps", 34, 1.5, 5, py0, 0.4, MARBLE, tread=0.5))
    pts = [(-14.7 + k * 4.2, py0 + 1.3) for k in range(8)] + [(x, py0 + 6.2) for x in (-14.7, -6.3, 6.3, 14.7)] + [(x, py0 + 11.0) for x in (-14.7, -6.3, 6.3, 14.7)]
    m.add(1, colonnade("portico_cols", pts, 1.9, 14.2, 0.75, "corinthian", "#9a9690"), "portico")
    m.add(1, box("door", 7, 0.6, 12, (0, py0 + 15.3, 1.9), BRONZE))
    m.add(2, entablature("portico_ent", -17, 17, py0, py0 + 15.6, 16.1, 3.2, MARBLE), "roof")
    m.add(2, pediment("pediment", 34, 15.6, 19.3, 6.8, py0, MARBLE, "#8a8f8c"))
    m.add(2, box("inscription", 18, 0.3, 1.0, (0, py0 - 0.4, 17.4), BRONZE))
    return m


# ====================================================================== temples

def temple(name, w, d, podium, col_h, front, side, order="corinthian", color=MARBLE, roof=TILE, kind="prostyle", cella=None, steps_w=None, statues=True, ruin=False, church=False):
    """kind: prostyle (porch only), peripteral (all round), pseudo (porch + engaged half columns on the cella)."""
    m = Model(name)
    r = min(w / (front * 4.3), 1.25)
    y_front = -d / 2
    # podium with base and crown mouldings, front stair between cheek walls
    m.add(0, box("podium_base", w + 0.8, d + 0.8, podium * 0.15, (0, 0, 0), shade(color, -0.1)), "podium")
    m.add(0, box("podium", w, d, podium, (0, 0, 0), shade(color, -0.07)))
    m.add(0, box("podium_crown", w + 0.6, d + 0.6, podium * 0.12, (0, 0, podium * 0.88), shade(color, -0.02)))
    sw = steps_w or w * 0.62
    sd = podium * 1.2
    m.add(0, steps_front("steps", sw, podium, max(4, int(podium / 0.35)), y_front, 0, shade(color, -0.04), tread=sd / max(4, int(podium / 0.35))))
    for s in (-1, 1):
        m.add(0, box(f"cheek{s}", 1.4, sd, podium, (s * (sw / 2 + 0.7), y_front - sd / 2, 0), shade(color, -0.07)))
    z = podium
    # columns
    inset = r * 1.4
    xs = [-w / 2 + inset + k * (w - 2 * inset) / (front - 1) for k in range(front)]
    pts = [(x, y_front + inset) for x in xs]
    porch_depth = d * (0.38 if kind != "peripteral" else 1)
    if kind == "prostyle":
        for k in range(1, max(2, side)):
            yy = y_front + inset + k * (porch_depth - inset) / max(1, side - 1)
            pts += [(xs[0], yy), (xs[-1], yy)]
    elif kind == "peripteral":
        nside = max(side, int(d / (w / front)))
        ys = [y_front + inset + k * (d - 2 * inset) / (nside - 1) for k in range(nside)]
        pts += [(x, ys[-1]) for x in xs] + [(xs[0], y) for y in ys[1:-1]] + [(xs[-1], y) for y in ys[1:-1]]
    elif kind == "pseudo":
        pts += [(xs[0], y_front + inset + porch_depth * 0.5), (xs[-1], y_front + inset + porch_depth * 0.5)]
    if ruin:
        pts = pts[:front + 2]
    m.add(1, colonnade("cols", pts, z, col_h, r, order, color), "columns")
    # cella with door, corner pilasters and (pseudo-peripteral) engaged half columns
    if not ruin:
        ccolor = cella or shade(color, -0.04)
        if kind == "peripteral":
            cw, cd, cy0 = w - 4 * inset, d - 4 * inset, y_front + 2 * inset
        else:
            cw, cd, cy0 = w - 2 * r, d - porch_depth, y_front + porch_depth
        m.add(1, box("cella", cw, cd, col_h, (0, cy0 + cd / 2, z), ccolor if not church else BRICK))
        m.add(1, box("door", cw * 0.22, 0.4, col_h * 0.62, (0, cy0 - 0.15, z), BRONZE if not church else DARK))
        m.add(1, join([box(f"anta{s}", 1.0, 0.6, col_h, (s * (cw / 2 - 0.5), cy0 - 0.25, z), shade(color, 0.04)) for s in (-1, 1)], "antae"))
        if kind == "pseudo":
            n = max(3, int(cd / (w / front)))
            half = [(s * (cw / 2 + 0.05), cy0 + (k + 0.5) * cd / n) for k in range(n) for s in (-1, 1)]
            m.add(1, colonnade("half_cols", half, z, col_h, r * 0.85, order, color))
        zt = z + col_h
        m.add(2, entablature("entablature", -w / 2, w / 2, y_front, d / 2, zt, col_h * 0.24, color), "roof")
        m.add(2, pediment("pediment", w, d, zt + col_h * 0.24, w * 0.2, y_front, color, roof, statues=statues))
    else:
        zt = z + col_h
        m.add(2, entablature("entablature_frag", -w / 2, w / 2, y_front, y_front + inset * 2, zt, col_h * 0.24, color, dentils=True), "roof")
        m.add(2, trees("weeds", [(random.Random(3).uniform(-w / 3, w / 3), random.Random(k).uniform(-d / 4, d / 3), podium) for k in range(4)], 1.8))
    if church:
        m.add(2, box("campanile", 4, 4, col_h * 2.2, (w / 2 + 3, d / 2 - 4, 0), BRICK), "church")
        m.add(2, box("bell_openings", 4.1, 4.1, 1.8, (w / 2 + 3, d / 2 - 4, col_h * 2.2 - 3), DARK))
        m.add(2, cylinder("spire", 3.0, 3.2, (w / 2 + 3, d / 2 - 4, col_h * 2.2), TILE, verts=4, r_top=0))
    return m


def tholos(name, r, col_h, church=False):
    """Round temple (Hercules Victor): 20 Corinthian columns around a marble cella, conical roof."""
    m = Model(name)
    m.add(0, cylinder("crepis", r + 2.2, 0.6, (0, 0, 0), shade(MARBLE, -0.1), verts=48), "base")
    for k in range(3):
        m.add(0, cylinder(f"step{k}", r + 1.9 - k * 0.45, 0.45, (0, 0, 0.6 + k * 0.45), shade(MARBLE, -0.06 + k * 0.02), verts=48))
    z = 1.95
    pts = [(r * math.cos(math.tau * i / 20), r * math.sin(math.tau * i / 20)) for i in range(20)]
    m.add(1, colonnade("cols", pts, z, col_h, 0.5, "corinthian", MARBLE), "columns")
    m.add(1, cylinder("cella", r * 0.72, col_h, (0, 0, z), BRICK if church else shade(MARBLE, -0.04), verts=32))
    m.add(1, box("door", 1.6, 0.4, col_h * 0.6, (0, -r * 0.72 - 0.1, z), BRONZE))
    m.add(2, cylinder("architrave", r + 0.7, 1.2, (0, 0, z + col_h), MARBLE, verts=48), "roof")
    m.add(2, cylinder("roof", r + 1.6, col_h * 0.38, (0, 0, z + col_h + 1.2), TILE, verts=48, r_top=0.8))
    rib = [box(f"rib{i}", (r + 1.6) * 1.0, 0.18, 0.15, (0, 0, 0), shade(TILE, 0.1)) for i in range(24)]
    for i, rb in enumerate(rib):
        a = math.tau * i / 24
        rb.rotation_euler = (0, math.atan2(col_h * 0.38, r + 0.8), a)
        place(rb, ((r + 0.8) / 2 * math.cos(a), (r + 0.8) / 2 * math.sin(a), z + col_h + 1.2 + col_h * 0.19))
    m.add(2, join(rib, "roof_ribs"))
    if church:
        m.add(2, cylinder("cross", 0.15, 2.2, (0, 0, z + col_h * 1.38 + 1.2), GOLD, verts=6))
    return m


BUILDERS = {
    "rome/colosseum": lambda: colosseum("intact"),
    "rome/colosseum-fortress": lambda: colosseum("fortress"),
    "rome/colosseum-ruin": lambda: colosseum("ruin"),
    "rome/baths-of-trajan": lambda: thermae("baths-of-trajan", 330, 215, cb=(0.66, 0.5)),
    "rome/baths-of-trajan-construction": lambda: thermae("baths-of-trajan-construction", 330, 215, "construction", cb=(0.66, 0.5)),
    "rome/baths-of-caracalla": lambda: thermae("baths-of-caracalla", 337, 328),
    "rome/baths-of-caracalla-ruin": lambda: thermae("baths-of-caracalla-ruin", 337, 328, "ruin"),
    "rome/baths-of-diocletian": lambda: thermae("baths-of-diocletian", 380, 370),
    "rome/baths-of-diocletian-ruin": lambda: thermae("baths-of-diocletian-ruin", 380, 370, "ruin"),
    "rome/baths-of-diocletian-church": lambda: thermae("baths-of-diocletian-church", 380, 370, "church"),
    "rome/pantheon": pantheon,
    # Agrippa's Pantheon as rebuilt under Domitian: a broad transverse temple with an octastyle Corinthian porch
    "rome/pantheon-agrippa": lambda: temple("pantheon-agrippa", 44, 20, 3, 12, 8, 2, "corinthian", "#E4DAC6", kind="prostyle", steps_w=30),
    "rome/temple-of-saturn": lambda: temple("temple-of-saturn", 40, 22, 9, 11, 6, 3, "ionic", "#D9CBB0", kind="prostyle"),
    "rome/temple-of-saturn-ruin": lambda: temple("temple-of-saturn-ruin", 40, 22, 9, 11, 6, 3, "ionic", "#D9CBB0", kind="prostyle", ruin=True),
    "rome/temple-of-jupiter": lambda: temple("temple-of-jupiter", 54, 62, 6, 17, 6, 7, "corinthian", MARBLE, GOLD, kind="peripteral", steps_w=34),
    "rome/temple-of-jupiter-republic": lambda: temple("temple-of-jupiter-republic", 54, 62, 6, 16, 6, 7, "corinthian", "#E2D6BE", TILE, kind="peripteral", steps_w=34),
    "rome/temple-of-jupiter-archaic": lambda: temple("temple-of-jupiter-archaic", 54, 62, 5, 14, 6, 3, "tuscan", "#C9A98A", TILE, kind="prostyle", steps_w=30),
    "rome/temple-of-portunus": lambda: temple("temple-of-portunus", 11, 19, 2.5, 8, 4, 2, "ionic", TRAV, kind="pseudo"),
    "rome/temple-of-portunus-church": lambda: temple("temple-of-portunus-church", 11, 19, 2.5, 8, 4, 2, "ionic", TRAV, kind="pseudo", church=True, statues=False),
    "rome/temple-of-hercules-victor": lambda: tholos("temple-of-hercules-victor", 7.4, 10.6),
    "rome/temple-of-hercules-church": lambda: tholos("temple-of-hercules-church", 7.4, 10.6, church=True),
    "rome/tiber-island-temple": lambda: temple("tiber-island-temple", 24, 44, 3, 10, 6, 3, "ionic", TRAV, kind="prostyle"),
}
