"""Hero miniatures, part 2: circus, arches, basilicas, theatres, mausolea, churches, the Forum, the Curia."""
import math, random
import bpy
import bmesh
from chronokit import Model, box, cylinder, dome, join, shade, ellipse_ring, ellipse_disc, stadium_ring, stadium_pts, slab_from_pts, gable_roof, hip_roof, boolean_cut, obelisk
from archkit import (MARBLE, TRAV, BRICK, TILE, BRONZE, GOLD, DARK, PLASTER, place, copy_at, cyl_x, cyl_y, half_cyl_x, half_cyl_y, column, colonnade,
                     entablature, pediment, statue, steps_front, tiled_hip_roof, arch_bay, thermal_window, stepped_dome, ring_of)
from rome_hero import trees, temple, tholos, SAND, GRASS, WATER

TIMBER = "#9C7A58"


def along_stadium(proto_fn, L, W, z, n, name, inset=0.0):
    """Lay pieces along a stadium outline (flat end at -x, round end at +x), each facing outward."""
    r = W / 2 - inset
    straight = L - W / 2 - inset * 0  # from -L/2 to L/2 - r
    x0, x1 = -L / 2 + inset, L / 2 - W / 2
    perim = 2 * (x1 - x0) + math.pi * r
    proto = proto_fn()
    objs = []
    for i in range(n):
        s = perim * (i + 0.5) / n
        if s < (x1 - x0):
            x, y, rot = x0 + s, -r, 0.0
        elif s < (x1 - x0) + math.pi * r:
            a = -math.pi / 2 + (s - (x1 - x0)) / r
            x, y, rot = x1 + r * math.cos(a), r * math.sin(a), a + math.pi / 2
        else:
            x, y, rot = x1 - (s - (x1 - x0) - math.pi * r), r, math.pi
        objs.append(copy_at(proto, (x, y, z), rot, name=f"{name}{i}"))
    bpy.data.objects.remove(proto, do_unlink=True)
    return join(objs, name)


# ====================================================================== Circus Maximus

def circus(variant="imperial"):
    m = Model("circus-maximus" + ("" if variant == "imperial" else "-" + variant))
    L, W = (621, 118) if variant in ("imperial", "late") else (600, 110) if variant == "republic" else (560, 100)
    wood = variant in ("regal", "republic")
    stand = TIMBER if wood else TRAV
    m.add(0, slab_from_pts("arena", stadium_pts(L - 40, W - 40), 0.4, color=SAND), "arena")
    # euripus: water channel at the foot of the stands
    if variant != "regal":
        m.add(0, stadium_ring("euripus", L - 36, W - 36, 2.2, 0.5, color=WATER))
    tiers = 1 if variant == "regal" else 2 if wood else 3
    for k in range(6 if not wood else 4):
        f = k / (6 if not wood else 4)
        m.add(1, stadium_ring(f"seats{k}", L - 30 + f * 26, W - 30 + f * 26, 4.5, 2 + f * 14 * tiers / 3, color=shade(stand, -0.04 + 0.03 * (k % 2))), "stands")
    if not wood:
        def bay(h=11.0):
            return join([arch_bay("cbay", 7.0, h, 2.2, 2.2, h * 0.6, TRAV), column("chc", -3.5, -1.15, 0, h - 1.1, 0.5, "tuscan", shade(TRAV, 0.05)),
                         box("cband", 7.0, 1.0, 1.1, (0, -0.3, h - 1.1), shade(TRAV, 0.07))], "cbay")
        for t in range(2):
            m.add(1, along_stadium(lambda: bay(11.0), L, W, t * 11.0, int((2 * (L - W / 2) + math.pi * W / 2) / 7.0), f"facade{t}"))
        m.add(2, stadium_ring("attic", L, W, 2.2, 6, (0, 0, 22.0), color=shade(TRAV, 0.04)), "upper")
        m.add(2, stadium_ring("roof", L - 1, W - 1, 6, 0.8, (0, 0, 28.0), color=shade(TILE, -0.08)))
    else:
        posts = []
        for k in range(int((L * 2) / 6)):
            x = -L / 2 + 6 + (k % int(L / 6)) * 6
            y = (W / 2 - 1) * (1 if k < L / 6 else -1)
            if x > L / 2 - W / 2:
                continue
            posts.append(box(f"post{k}", 0.5, 0.5, 9, (x, y, 0), shade(TIMBER, -0.15)))
        m.add(1, join(posts, "posts"))
    # spina with obelisks, metae, shrines and the lap counters
    sl = L * 0.55
    sx = L * 0.02
    m.add(1, box("spina", sl, 8, 1.8, (sx, 0, 0.4), shade(MARBLE, -0.05) if not wood else shade(TIMBER, 0.1)), "spina")
    if not wood:
        m.add(1, box("spina_basin", sl * 0.9, 4.5, 0.4, (sx, 0, 2.2), WATER))
    for s in (-1, 1):
        mx = sx + s * (sl / 2 + 6)
        m.add(1, box(f"meta_base{s}", 6, 8, 2, (mx, 0, 0.4), shade(MARBLE, -0.05)))
        for i in range(3):
            m.add(1, cylinder(f"meta{s}{i}", 0.9, 7, (mx, (i - 1) * 2.4, 2.4), GOLD if not wood else TIMBER, verts=10, r_top=0.15))
    obs = {"regal": [], "republic": [], "imperial": [sx], "late": [sx - sl * 0.2, sx + sl * 0.18]}[variant]
    for i, x in enumerate(obs):
        m.add(1, box(f"ob_ped{i}", 4.6, 4.6, 3.5, (x, 0, 2.2), MARBLE))
        m.add(1, obelisk(f"obelisk{i}", 2.6, 24 if i == 0 else 32, (x, 0, 5.7), "#C2A27A"))
    if not wood:
        for i, x in enumerate([sx - sl * 0.32, sx - sl * 0.08, sx + sl * 0.3]):
            m.add(2, box(f"aedicula{i}", 4, 5, 5, (x, 0, 2.2), MARBLE))
            m.add(2, gable_roof(f"aed_roof{i}", 4, 5, 1.4, (x, 0, 7.2), TILE))
        for k in range(7):
            m.add(2, dome(f"egg{k}", 0.55, (sx + sl * 0.15 + k * 1.3, 0, 6.0), GOLD, squash=1.5, segments=8, rings=4))
            m.add(2, box(f"dolphin{k}", 1.0, 0.4, 0.5, (sx - sl * 0.18 + k * 1.3, 0, 6.0), BRONZE))
        m.add(2, box("egg_frame", 10, 0.5, 0.4, (sx + sl * 0.15 + 3.9, 0, 5.6), MARBLE))
        m.add(2, box("dolphin_frame", 10, 0.5, 0.4, (sx - sl * 0.18 + 3.9, 0, 5.6), MARBLE))
    # carceres: twelve starting gates on a slight curve, with towers (oppida) at the corners
    gate_proto = lambda: join([arch_bay("cg", W / 14, 9, 3, W / 40, 5.5, TRAV if not wood else TIMBER, keystone=not wood), box("cg_top", W / 14, 3.4, 1.0, (0, 0, 9), shade(TRAV, 0.06))], "cg")
    g = gate_proto()
    gates = []
    for k in range(12):
        t = (k + 0.5) / 12 - 0.5
        x = -L / 2 + 8 + abs(t) * 10
        gates.append(copy_at(g, (x, t * (W - 30), 0.4), -math.pi / 2 + t * 0.3))
    bpy.data.objects.remove(g, do_unlink=True)
    m.add(2, join(gates, "carceres"), "gates")
    for s in (-1, 1):
        m.add(2, box(f"oppidum{s}", 14, 12, 18, (-L / 2 + 8, s * (W / 2 - 6), 0), TRAV if not wood else TIMBER))
        m.add(2, tiled_hip_roof(f"oppidum_roof{s}", 14, 12, 4, (-L / 2 + 8, s * (W / 2 - 6), 18)))
    m.add(2, box("porta_pompae", 12, 10, 16, (-L / 2 + 6, 0, 0), MARBLE))
    if not wood:
        # pulvinar: the imperial box, a temple front on the Palatine side
        m.add(2, box("pulvinar", 30, 14, 18, (L * 0.05, W / 2 + 4, 0), MARBLE))
        m.add(2, pediment("pulvinar_ped", 30, 14, 18, 5, W / 2 - 3, MARBLE, TILE, statues=False))
        m.add(2, colonnade("pulvinar_cols", [(L * 0.05 - 12 + k * 4.8, W / 2 - 2.5) for k in range(6)], 6, 12, 0.6, "corinthian"))
        # the triumphal arch in the curved end
        m.add(2, box("arch_east", 18, 8, 20, (L / 2 - 2, 0, 0), MARBLE))
    return m


# ====================================================================== triumphal arches

def triumphal_arch(name, w, h, d, bays=1, attic_statues=False):
    m = Model(name)
    pier_h = h * 0.62
    body = box("body", w, d, pier_h + h * 0.14, (0, 0, 0), MARBLE)
    spans = [(0, w * 0.17)] if bays == 1 else [(0, w * 0.15), (-w * 0.33, w * 0.08), (w * 0.33, w * 0.08)]
    for x, r in spans:
        spring = pier_h * (0.62 if r == spans[0][1] else 0.48)
        bpy.ops.mesh.primitive_cylinder_add(vertices=28, radius=r, depth=d + 2, location=(x, 0, spring), rotation=(math.pi / 2, 0, 0))
        body = boolean_cut(body, bpy.context.active_object)
        bpy.ops.mesh.primitive_cube_add(size=1, location=(x, 0, spring / 2 - 0.02))
        c = bpy.context.active_object
        c.scale = (r * 2, d + 2, spring + 0.04)
        bpy.ops.object.transform_apply(scale=True)
        body = boolean_cut(body, c)
    m.add(0, body, "body")
    m.add(0, box("plinth", w + 0.8, d + 0.8, 0.8, (0, 0, 0), shade(MARBLE, -0.08)))
    # columns on pedestals, front and back, with entablature breaks above them
    xs = [-w / 2 + w * 0.06, -w * 0.21, w * 0.21, w / 2 - w * 0.06] if bays == 3 else [-w / 2 + w * 0.08, -w * 0.25, w * 0.25, w / 2 - w * 0.08]
    for side in (-1, 1):
        yy = side * (d / 2 + 0.75)
        pts = [(x, yy) for x in xs]
        m.add(1, join([box(f"ped{side}{i}", 1.8, 1.8, 2.4, (x, yy, 0.8), shade(MARBLE, -0.04)) for i, (x, _) in enumerate(pts)], f"pedestals{side}"), "columns")
        m.add(1, colonnade(f"cols{side}", pts, 3.2, pier_h - 2.4, 0.6, "corinthian", shade(MARBLE, 0.02)))
        m.add(1, join([box(f"break{side}{i}", 2.0, 1.8, 1.6, (x, yy, pier_h + 0.8), shade(MARBLE, 0.05)) for i, (x, _) in enumerate(pts)], f"breaks{side}"))
        # relief panels and spandrel victories
        for i, x in enumerate(xs[:-1]):
            cx = (x + xs[i + 1]) / 2
            if bays == 3 and abs(cx) > w * 0.2:
                m.add(1, box(f"relief{side}{i}", w * 0.12, 0.3, 2.4, (cx, side * (d / 2 + 0.1), pier_h * 0.78), shade(MARBLE, -0.1)))
        for s in (-1, 1):
            m.add(1, statue(f"victory{side}{s}", s * spans[0][1] * 0.95, side * (d / 2 + 0.15), pier_h * 0.75, 2.2, shade(MARBLE, -0.12)))
    m.add(1, box("keystone", 1.2, d + 0.4, 1.6, (0, 0, pier_h * 0.62 + spans[0][1] - 0.8), shade(MARBLE, 0.06)))
    zt = pier_h + h * 0.14
    m.add(2, entablature("ent", -w / 2, w / 2, -d / 2, d / 2, zt - 1.8, 1.8, MARBLE), "attic")
    m.add(2, box("attic", w - 0.6, d - 0.4, h * 0.24, (0, 0, zt), shade(MARBLE, -0.02)))
    for side in (-1, 1):
        m.add(2, box(f"inscription{side}", w * 0.42, 0.25, h * 0.15, (0, side * (d / 2 - 0.05), zt + h * 0.04), "#b9a77f"))
        m.add(2, join([box(f"letters{side}{k}", w * 0.38, 0.3, 0.18, (0, side * (d / 2 - 0.02), zt + h * 0.06 + k * h * 0.035), BRONZE) for k in range(3)], f"letters{side}"))
        if attic_statues:
            for x in xs:
                m.add(2, statue(f"dacian{side}{x:.0f}", x, side * (d / 2 + 0.2), zt, 3.2, "#9a7f6a"))
    m.add(2, box("attic_cornice", w, d, 0.6, (0, 0, zt + h * 0.24), shade(MARBLE, 0.05)))
    # quadriga
    zq = zt + h * 0.24 + 0.6
    for i in range(4):
        m.add(2, box(f"horse{i}", 0.8, 2.6, 1.8, (-1.5 + i, -0.6, zq), BRONZE))
    m.add(2, box("chariot", 2.6, 1.6, 1.5, (0, 1.2, zq), BRONZE))
    m.add(2, statue("emperor", 0, 1.2, zq + 1.5, 2.2, GOLD))
    return m


# ====================================================================== Basilica of Maxentius

def basilica_nova(ruin=False):
    m = Model("basilica-of-maxentius" + ("-ruin" if ruin else ""))
    W, D = 100, 65
    m.add(0, box("platform", W, D, 2, (0, 0, 0), shade(BRICK, -0.12)), "platform")
    z0 = 2
    nh = 35
    if not ruin:
        m.add(1, box("nave_walls", 80, 25, nh, (0, 0, z0), BRICK), "nave")
        bays = [half_cyl_y(f"nave_cross{k}", 26.6 / 2, 25, (-26.6 + k * 26.6, 0, z0 + nh), shade(TILE, -0.06), verts=24) for k in range(3)]
        bays.append(half_cyl_x("nave_barrel", 12.5, 80, (0, 0, z0 + nh), shade(TILE, -0.06), verts=24))
        m.add(2, join(bays, "nave_vaults"), "vaults")
        for k in range(3):
            for s in (-1, 1):
                m.add(2, thermal_window(f"nw{k}{s}", 8, 1.2, (-26.6 + k * 26.6, s * 12.6, z0 + nh - 9), PLASTER, rot_z=0 if s < 0 else math.pi))
        m.add(1, cylinder("apse_w", 10, 26, (-40, 0, z0), BRICK, verts=24))
        m.add(1, colonnade("nave_cols", [(-26.6 * 1.5 + k * 26.6, s * 12.4) for k in range(4) for s in (-1, 1)], z0 + 22, 13, 0.9, "corinthian", MARBLE))
        m.add(1, box("porch", 80, 8, 14, (0, -D / 2 + 4, z0), shade(BRICK, 0.05)))
        m.add(1, colonnade("porch_cols", [(-36 + k * 9, -D / 2 + 1) for k in range(9)], z0, 12, 0.7, "corinthian", MARBLE))
    aisles = [(-1, k) for k in range(3)] + ([] if ruin else [(1, k) for k in range(3)])
    for s, k in aisles:
        x = -26.6 + k * 26.6
        y = s * 20
        m.add(1, box(f"aisle{s}{k}", 22.6, 16, 24, (x, y, z0), BRICK), "aisles")
        m.add(2, half_cyl_y(f"aisle_vault{s}{k}", 11.3, 16, (x, y, z0 + 24), shade(TILE, -0.05), verts=20))
        m.add(1, box(f"aisle_arch{s}{k}", 18, 0.6, 18, (x, y - s * 8.1, z0), DARK))
    if ruin:
        m.add(1, join([box(f"stump{k}", 4, 4, 4 + k * 2.5, (-30 + k * 15, -6, z0), BRICK) for k in range(5)], "stumps"))
        m.add(2, trees("ruin_trees", [(random.Random(k).uniform(-40, 40), random.Random(k + 9).uniform(-25, 5), z0) for k in range(10)], 3))
        m.add(2, column("last_column", -13, -12.4, z0, 14.5, 0.9, "corinthian", MARBLE))
    return m


# ====================================================================== theatres

def theatre(name, R, tiers=2, top=None, scaena_h=None, porticus=False, temple_top=False):
    m = Model(name)
    tier_h = 11.0
    m.add(0, ellipse_disc("orchestra", R * 0.28, R * 0.28, 0.4, (0, 0, 0), MARBLE, verts=40), "cavea")
    for k in range(14):
        f0, f1 = 0.3 + 0.67 * k / 14, 0.3 + 0.67 * (k + 1) / 14
        m.add(0, ellipse_ring(f"seat{k}", R * f1, R * f1, f0 / f1, 1.2 + k * (tiers * tier_h - 2) / 14, (0, 0, 0), shade(TRAV, -0.04 + 0.03 * (k % 2)), n=72, arc=math.pi, start=0))
    nb = int(math.pi * R / 6.5)
    for t in range(tiers):
        order = ["tuscan", "ionic", "corinthian"][t]
        def bay(order=order):
            w = math.pi * R / nb + 0.15
            return join([arch_bay("tb", w, tier_h, 2.4, 2.1, tier_h * 0.6, TRAV), column("tc", -w / 2, -1.25, 0, tier_h - 1.1, 0.5, order, shade(TRAV, 0.05)),
                         box("tband", w, 1.0, 1.1, (0, -0.35, tier_h - 1.1), shade(TRAV, 0.07))], "tbay")
        proto = bay()
        objs = []
        for i in range(nb):
            a = math.pi * (i + 0.5) / nb
            objs.append(copy_at(proto, (R * math.cos(a), R * math.sin(a), t * tier_h), a + math.pi / 2))
        bpy.data.objects.remove(proto, do_unlink=True)
        m.add(1, join(objs, f"facade{t}"), "facade")
    m.add(1, ellipse_ring("attic", R, R, 0.95, 5, (0, 0, tiers * tier_h), shade(TRAV, 0.04), n=72, arc=math.pi, start=0))
    # stage and scaenae frons: three storeys of columns in front of a tall wall
    sh = scaena_h or tiers * tier_h + 6
    m.add(2, box("stage", R * 1.3, R * 0.14, 1.6, (0, -R * 0.05, 0), TIMBER), "stage")
    m.add(2, box("scaena", R * 1.9, R * 0.12, sh, (0, -R * 0.18, 0), shade(MARBLE, -0.03)))
    for t in range(3):
        zz = 1.6 + t * (sh - 4) / 3
        m.add(2, colonnade(f"frons{t}", [(-R * 0.6 + k * R * 1.2 / 11, -R * 0.11) for k in range(12)], zz, (sh - 4) / 3 - 0.8, 0.45, "corinthian", MARBLE))
        m.add(2, box(f"frons_ent{t}", R * 1.3, 1.6, 0.8, (0, -R * 0.11, zz + (sh - 4) / 3 - 0.8), MARBLE))
    m.add(2, box("roof_over_stage", R * 1.4, R * 0.16, 0.8, (0, -R * 0.12, sh), TILE))
    # the back of the stage building, seen from the street: pilasters, arched doors, windows, string courses
    yb = -R * 0.24
    nb2 = int(R * 1.9 / 7)
    back = []
    for k in range(nb2 + 1):
        x = -R * 0.95 + k * R * 1.9 / nb2
        back.append(box(f"bp{k}", 1.4, 0.8, sh - 1.2, (x, yb - 0.4, 0), shade(MARBLE, 0.02)))
        if k < nb2:
            cx = x + R * 0.95 / nb2
            if k % 3 == 1:
                back += [box(f"bd{k}", 3.0, 0.4, 5.0, (cx, yb - 0.2, 0), DARK), cyl_y(f"bda{k}", 1.5, 0.4, (cx, yb - 0.2, 5.0), DARK, verts=12)]
            for j, z in enumerate((sh * 0.42, sh * 0.7)):
                back.append(box(f"bw{k}{j}", 1.6, 0.4, 2.6, (cx, yb - 0.2, z), DARK))
    for z in (sh * 0.36, sh * 0.64):
        back.append(box(f"bs{z:.0f}", R * 1.92, 1.0, 0.6, (0, yb - 0.5, z), shade(MARBLE, 0.05)))
    back.append(box("bcornice", R * 1.94, 1.6, 1.0, (0, yb - 0.6, sh - 1.2), shade(MARBLE, 0.06)))
    m.add(2, join(back, "scaena_back"))
    if temple_top:
        b = temple("venus_victrix", 24, 30, 2, 12, 6, 2, "corinthian", MARBLE)
        objs = b.finish() if False else None
        for k, (stage, lst) in enumerate(sorted(b.stages.items())):
            for o in lst:
                o.location.y += R * 0.95
                o.location.z += tiers * tier_h
                m.add(2, o)
    if porticus:
        PW, PD = R * 2.2, R * 2.0
        py = -R * 0.2 - PD / 2
        m.add(0, box("porticus_garden", PW, PD, 0.4, (0, py, 0), GRASS))
        for s in (-1, 1):
            m.add(1, colonnade(f"port_x{s}", [(-PW / 2 + 3 + k * (PW - 6) / 23, py + s * (PD / 2 - 3)) for k in range(24)], 0.4, 9, 0.5, "ionic", MARBLE))
            m.add(1, colonnade(f"port_y{s}", [(s * (PW / 2 - 3), py - PD / 2 + 3 + k * (PD - 6) / 21) for k in range(22)], 0.4, 9, 0.5, "ionic", MARBLE))
            m.add(2, box(f"port_roof_x{s}", PW, 6, 0.6, (0, py + s * (PD / 2 - 3), 9.6), TILE))
            m.add(2, box(f"port_roof_y{s}", 6, PD, 0.6, (s * (PW / 2 - 3), py, 9.6), TILE))
        m.add(1, trees("grove", [(-PW * 0.3 + (k % 6) * PW * 0.12, py - PD * 0.3 + (k // 6) * PD * 0.2, 0.4) for k in range(24)], 3.0))
        m.add(1, box("curia_pompei", 18, 14, 14, (0, py - PD / 2 + 4, 0.4), BRICK))
    if top == "fortress":
        for s in (-1, 1):
            m.add(2, box(f"tower{s}", 12, 12, 22, (s * R * 0.7, R * 0.45, tiers * tier_h), BRICK))
        m.add(2, box("keep", 30, 16, 14, (0, R * 0.6, tiers * tier_h), BRICK))
    if top == "palazzo":
        m.add(2, box("palazzo", R * 1.3, R * 0.5, 16, (0, R * 0.45, tiers * tier_h), PLASTER))
        m.add(2, join([box(f"pwin{k}{j}", 1.6, 0.3, 2.4, (-R * 0.6 + k * R * 1.2 / 11, R * 0.2 - 0.1, tiers * tier_h + 3 + j * 6), DARK) for k in range(12) for j in range(2)], "palazzo_windows"))
        m.add(2, tiled_hip_roof("palazzo_roof", R * 1.3, R * 0.5, 4, (0, R * 0.45, tiers * tier_h + 16)))
    return m


# ====================================================================== mausolea

def hadrianeum(variant="mausoleum"):
    m = Model({"mausoleum": "mausoleum-of-hadrian", "late": "castel-santangelo-late", "medieval": "castel-santangelo-medieval", "renaissance": "castel-santangelo-renaissance"}[variant])
    m.add(0, box("base", 89, 89, 10, (0, 0, 0), MARBLE if variant == "mausoleum" else shade(TRAV, -0.1)), "base")
    if variant == "mausoleum":
        m.add(0, join([box(f"pil{s}{k}", 1.4, 0.5, 9, (-42 + k * 7, s * 44.7, 0.5), shade(MARBLE, 0.04)) for s in (-1, 1) for k in range(13)], "pilasters"))
        m.add(0, join([box(f"pilx{s}{k}", 0.5, 1.4, 9, (s * 44.7, -42 + k * 7, 0.5), shade(MARBLE, 0.04)) for s in (-1, 1) for k in range(13)], "pilasters_x"))
        m.add(0, entablature("base_ent", -44.5, 44.5, -44.5, 44.5, 10, 1.6, MARBLE, dentils=False))
    m.add(1, cylinder("drum", 32, 21, (0, 0, 10), TRAV, verts=64), "drum")
    if variant == "mausoleum":
        m.add(1, join([box(f"niche{k}", 3, 0.6, 7, (32.2 * math.cos(math.tau * k / 24), 32.2 * math.sin(math.tau * k / 24), 16), DARK, rot_z=math.tau * k / 24 + math.pi / 2) for k in range(24)], "niches"))
        m.add(1, ring_of(lambda: statue("st", 0, 0, 0, 3.0, shade(MARBLE, -0.08)), 28, 31, 31, 31.5, "drum_statues"))
        m.add(2, cylinder("mound", 29, 9, (0, 0, 31), GRASS, verts=48, r_top=20), "top")
        m.add(2, ring_of(lambda: join([cylinder("cy", 0.9, 8, (0, 0, 0), "#3f5a33", verts=6, r_top=0.15)], "cyp"), 24, 24, 24, 34, "cypresses", face_out=False))
        m.add(2, cylinder("tholos_base", 10, 4, (0, 0, 40), MARBLE, verts=32))
        m.add(2, ring_of(lambda: column("tc", 0, 0, 0, 8, 0.45, "corinthian"), 16, 8.5, 8.5, 44, "tholos_cols", face_out=False))
        m.add(2, cylinder("tholos_cella", 6, 8, (0, 0, 44), shade(MARBLE, -0.04), verts=24))
        m.add(2, dome("tholos_dome", 9, (0, 0, 52.5), BRONZE, squash=0.5, segments=24, rings=8))
        for i in range(4):
            m.add(2, box(f"q_horse{i}", 0.9, 2.8, 2.0, (-1.6 + i * 1.1, -0.5, 57), BRONZE))
        m.add(2, statue("hadrian", 0, 1.6, 57, 3.2, GOLD))
    else:
        m.add(1, cylinder("upper_drum", 30, 10, (0, 0, 31), BRICK, verts=48))
        m.add(1, ring_of(lambda: box("merlon", 1.6, 1.0, 1.8, (0, 0, 0), BRICK), 48, 30, 30, 41, "drum_merlons"))
        m.add(2, box("keep", 22, 22, 16, (0, 0, 41), BRICK), "castle")
        m.add(2, tiled_hip_roof("keep_roof", 22, 22, 5, (0, 0, 57)))
        if variant in ("medieval", "renaissance"):
            m.add(2, box("papal_apartments", 30, 14, 10, (6, -12, 41), PLASTER))
            m.add(2, tiled_hip_roof("apt_roof", 30, 14, 4, (6, -12, 51)))
            m.add(2, box("angel_tower", 7, 7, 10, (0, 0, 62), BRICK))
            m.add(2, statue("archangel", 0, 0, 72, 4.5, BRONZE))
        if variant == "medieval":
            curt = [box(f"wall{s}", 108, 5, 12, (0, s * 54, 0), BRICK) for s in (-1, 1)] + [box(f"wallx{s}", 5, 108, 12, (s * 54, 0, 0), BRICK) for s in (-1, 1)]
            curt += [cylinder(f"ct{sx}{sy}", 7, 16, (sx * 54, sy * 54, 0), shade(BRICK, -0.05), verts=16) for sx in (-1, 1) for sy in (-1, 1)]
            m.add(0, join(curt, "curtain"))
        if variant == "renaissance":
            curt = []
            for sx in (-1, 1):
                for sy in (-1, 1):
                    curt.append(box(f"bastion{sx}{sy}", 28, 28, 12, (sx * 60, sy * 60, 0), shade(BRICK, -0.06), rot_z=math.pi / 4))
            curt += [box(f"w{s}", 120, 7, 10, (0, s * 60, 0), BRICK) for s in (-1, 1)] + [box(f"wx{s}", 7, 120, 10, (s * 60, 0, 0), BRICK) for s in (-1, 1)]
            curt.append(box("passetto", 6, 80, 8, (-40, 100, 0), BRICK))
            m.add(0, join(curt, "bastions"))
        if variant == "late":
            m.add(0, box("aurelian_link", 10, 70, 12, (-52, 0, 0), BRICK))
    return m


def mausoleum_augustus(variant="tomb"):
    m = Model({"tomb": "mausoleum-of-augustus", "fortress": "mausoleum-of-augustus-fortress", "ruin": "mausoleum-of-augustus-ruin"}[variant])
    R = 45
    m.add(0, cylinder("outer_drum", R, 12, (0, 0, 0), TRAV if variant == "tomb" else shade(TRAV, -0.1), verts=72), "drum")
    if variant == "tomb":
        m.add(0, join([box(f"pil{k}", 1.2, 0.5, 11, (R * math.cos(math.tau * k / 36), R * math.sin(math.tau * k / 36), 0.5), shade(TRAV, 0.05), rot_z=math.tau * k / 36 + math.pi / 2) for k in range(36)], "pilasters"))
        m.add(0, box("entrance", 8, 3, 9, (0, -R - 0.5, 0), DARK))
        for s in (-1, 1):
            m.add(0, obelisk(f"ob{s}", 1.8, 14, (s * 10, -R - 10, 0), "#C2A27A"))
            m.add(0, box(f"res_gestae{s}", 5, 0.4, 7, (s * 5.5, -R - 0.4, 0), BRONZE))
        for k, (rr, zz) in enumerate([(R * 0.8, 12), (R * 0.58, 20), (R * 0.36, 28)]):
            m.add(1, cylinder(f"terrace{k}", rr, 8, (0, 0, zz), GRASS, verts=48), "terraces")
            m.add(1, ring_of(lambda: cylinder("cy", 0.9, 7, (0, 0, 0), "#3f5a33", verts=6, r_top=0.12), 28 - k * 6, rr - 2, rr - 2, zz + 8, f"cypress{k}", face_out=False))
        m.add(2, cylinder("summit", R * 0.18, 10, (0, 0, 36), TRAV, verts=24), "summit")
        m.add(2, statue("augustus", 0, 0, 46, 5, GOLD))
    elif variant == "fortress":
        m.add(1, cylinder("inner_wall", R * 0.85, 14, (0, 0, 12), BRICK, verts=48), "walls")
        m.add(1, ring_of(lambda: box("merlon", 1.6, 1.0, 1.8, (0, 0, 0), BRICK), 56, R * 0.85, R * 0.85, 26, "merlons"))
        m.add(2, box("keep", 14, 14, 22, (0, 0, 12), BRICK), "keep")
    else:
        m.add(1, cylinder("garden", R * 0.8, 6, (0, 0, 12), GRASS, verts=48), "garden")
        m.add(2, trees("garden_trees", [(R * 0.45 * math.cos(a), R * 0.45 * math.sin(a), 18) for a in [math.tau * k / 10 for k in range(10)]], 3.5), "trees")
        m.add(2, join([statue(f"ant{k}", R * 0.25 * math.cos(math.tau * k / 6), R * 0.25 * math.sin(math.tau * k / 6), 18, 2.4, MARBLE) for k in range(6)], "antiquities"))
    return m


# ====================================================================== Christian basilicas

def church(name, w, d, nave_h=22, atrium=False, campanile=False, transept=False, porch=True, facade_mosaic=False, color=BRICK, early=False):
    m = Model(name)
    nave_w = w * 0.46
    aisle_w = (w - nave_w) / 2
    m.add(0, box("platform", w + 4, d + 4, 1.0, (0, 0, 0), shade(TRAV, -0.1)), "base")
    z0 = 1.0
    m.add(1, box("nave", nave_w, d, nave_h, (0, 0, z0), color), "nave")
    # clerestory windows: round-headed, dark
    nwin = max(6, int(d / 5))
    wins = []
    for s in (-1, 1):
        for k in range(nwin):
            y = -d / 2 + (k + 0.5) * d / nwin
            wins.append(box(f"cw{s}{k}", 0.4, 1.8, 3.4, (s * (nave_w / 2 + 0.05), y, z0 + nave_h - 6), DARK))
            wins.append(cyl_x(f"cwa{s}{k}", 0.9, 0.4, (s * (nave_w / 2 + 0.05), y, z0 + nave_h - 2.6), DARK, verts=10))
    m.add(1, join(wins, "clerestory"))
    for s in (-1, 1):
        m.add(1, box(f"aisle{s}", aisle_w, d, nave_h * 0.55, (s * (nave_w / 2 + aisle_w / 2), 0, z0), shade(color, -0.04)))
        # lean-to aisle roofs
        from archkit import mesh_from as _mf
        m.add(2, box(f"aisle_roof{s}", aisle_w + 0.8, d + 0.8, 0.6, (s * (nave_w / 2 + aisle_w / 2), 0, z0 + nave_h * 0.55), TILE), "roofs")
    m.add(2, pediment("nave_roof", nave_w, d, z0 + nave_h, nave_w * 0.28, -d / 2, PLASTER if not early else color, TILE, ridges=True, statues=False))
    m.add(1, cylinder("apse", nave_w / 2, nave_h * 0.75, (0, d / 2, z0), color, verts=24))
    m.add(2, dome("apse_roof", nave_w / 2 + 0.4, (0, d / 2, z0 + nave_h * 0.75), TILE, squash=0.45, segments=24, rings=6))
    if transept:
        m.add(1, box("transept", w * 1.25, d * 0.18, nave_h, (0, d / 2 - d * 0.12, z0), color))
        m.add(2, tiled_hip_roof("transept_roof", w * 1.25, d * 0.18, nave_h * 0.25, (0, d / 2 - d * 0.12, z0 + nave_h)))
    if facade_mosaic:
        m.add(1, box("mosaic", nave_w * 0.75, 0.3, nave_h * 0.35, (0, -d / 2 - 0.1, z0 + nave_h * 0.55), GOLD))
    m.add(1, box("door", nave_w * 0.25, 0.4, nave_h * 0.35, (0, -d / 2 - 0.15, z0), BRONZE))
    if porch:
        m.add(1, colonnade("porch_cols", [(-nave_w / 2 + 1 + k * (nave_w - 2) / 5, -d / 2 - 4) for k in range(6)], z0, nave_h * 0.4, 0.55, "ionic", MARBLE), "porch")
        m.add(2, box("porch_roof", nave_w + 2, 6, 0.6, (0, -d / 2 - 3, z0 + nave_h * 0.4), TILE))
    if atrium:
        aw, ad = w, d * 0.6
        ay = -d / 2 - ad / 2 - 6
        m.add(0, box("atrium_floor", aw, ad, 0.4, (0, ay, z0), "#D6C39E"))
        pts = [(s * (aw / 2 - 2), ay - ad / 2 + 2 + k * (ad - 4) / 9) for s in (-1, 1) for k in range(10)] + [(-aw / 2 + 2 + k * (aw - 4) / 9, ay - ad / 2 + 2) for k in range(1, 9)]
        m.add(1, colonnade("atrium_cols", pts, z0, 6, 0.4, "ionic", MARBLE), "atrium")
        for s in (-1, 1):
            m.add(2, box(f"atrium_roof{s}", 5, ad, 0.5, (s * (aw / 2 - 2), ay, z0 + 6.4), TILE))
        m.add(2, box("atrium_roof_front", aw, 5, 0.5, (0, ay - ad / 2 + 2, z0 + 6.4), TILE))
        m.add(1, box("gatehouse", 16, 8, 12, (0, ay - ad / 2, z0), color))
        m.add(1, cylinder("cantharus", 2.5, 1.2, (0, ay, z0 + 0.4), WATER, verts=12))
        m.add(1, dome("cantharus_canopy", 3.0, (0, ay, z0 + 5), BRONZE, squash=0.8, segments=12, rings=5))
    if campanile:
        cx, cy = w / 2 + 3.5, -d / 2 + 5
        storeys = 6
        sh = nave_h * 1.9 / storeys
        for k in range(storeys):
            m.add(2, box(f"camp{k}", 5.5, 5.5, sh, (cx, cy, z0 + k * sh), color), "campanile")
            m.add(2, box(f"camp_band{k}", 6.0, 6.0, 0.35, (cx, cy, z0 + (k + 1) * sh - 0.35), PLASTER))
            if k >= 2:
                for a in range(4):
                    ang = a * math.pi / 2
                    m.add(2, box(f"camp_open{k}{a}", 2.2 if k < storeys - 1 else 3.0, 0.3, sh * 0.5, (cx + 2.8 * math.cos(ang), cy + 2.8 * math.sin(ang), z0 + k * sh + sh * 0.25), DARK, rot_z=ang + math.pi / 2))
        m.add(2, cylinder("camp_spire", 4.0, 4.5, (cx, cy, z0 + storeys * sh), TILE, verts=4, r_top=0))
    return m


LEAD = "#8E8C86"


def _about(o, ang, pivot=(0, 0, 0)):
    """Rotate an object about a pivot (z axis) and apply."""
    bpy.context.scene.cursor.location = pivot
    bpy.ops.object.select_all(action="DESELECT")
    o.select_set(True)
    bpy.context.view_layer.objects.active = o
    bpy.ops.object.origin_set(type="ORIGIN_CURSOR")
    o.rotation_euler[2] += ang
    bpy.ops.object.transform_apply(location=True, rotation=True, scale=True)
    return o


def _giant_bay(bw, H, color=TRAV):
    """One bay of Michelangelo's giant order, facing -Y with its origin on the wall face:
    a colossal pilaster on the left edge, an aedicule window below and a square window above."""
    hi = shade(color, 0.07)
    parts = [box("gp", 2.6, 1.1, H, (-bw / 2, -0.55, 0), shade(color, 0.03)), box("gp_base", 3.2, 1.5, 1.8, (-bw / 2, -0.75, 0), shade(color, -0.04)),
             box("gp_cap", 3.4, 1.6, 2.0, (-bw / 2, -0.8, H - 2.0), hi)]
    ww = min(3.2, bw * 0.34)
    parts += [box("w1", ww, 0.5, H * 0.24, (0, -0.25, H * 0.16), DARK), box("w1_l", 0.45, 0.7, H * 0.24, (-ww / 2 - 0.22, -0.35, H * 0.16), hi),
              box("w1_r", 0.45, 0.7, H * 0.24, (ww / 2 + 0.22, -0.35, H * 0.16), hi), box("w1_lintel", ww + 1.4, 0.9, 0.6, (0, -0.45, H * 0.4), hi)]
    ped = box("w1_ped", ww + 1.8, 0.9, 1.0, (0, -0.45, H * 0.4 + 0.6), hi)
    bm = bmesh.new()
    bm.from_mesh(ped.data)
    for v in bm.verts:  # pinch the top into a triangle
        if v.co.z > 0.2:
            v.co.x *= 0.05
    bm.to_mesh(ped.data)
    bm.free()
    parts += [ped, box("w2", ww * 0.85, 0.5, H * 0.13, (0, -0.25, H * 0.62), DARK), box("w2_sill", ww * 0.85 + 1.0, 0.8, 0.4, (0, -0.4, H * 0.62 - 0.4), hi),
              box("w2_frame", ww * 0.85 + 0.8, 0.7, 0.4, (0, -0.35, H * 0.62 + H * 0.13), hi)]
    return join(parts, "gbay")


def _attic_bay(bw, h, color=TRAV):
    return join([box("ap", 2.0, 0.8, h, (-bw / 2, -0.4, 0), shade(color, 0.04)), box("aw", min(2.2, bw * 0.3), 0.4, h * 0.45, (0, -0.2, h * 0.28), DARK)], "abay")


def _michelangelo_arm(name, W, L, H, attic, roofed=True):
    """A crossing arm along +Y from y=0 (the crossing) to y=L, ending in a half-round apse of radius W/2.
    Giant order outside, entablature, attic, and a lead-covered barrel vault and half dome."""
    R = W / 2
    hi = shade(TRAV, 0.07)
    objs = [box(f"{name}_wall", W, L, H + attic, (0, L / 2, 0), shade(TRAV, -0.03)),
            cylinder(f"{name}_apse", R, H + attic, (0, L, 0), shade(TRAV, -0.03), verts=40)]
    # straight sides: bays along both long walls
    nb = max(1, round(L / 9))
    bw = L / nb
    for side in (-1, 1):
        proto = _giant_bay(bw, H)
        at = _attic_bay(bw, attic * 0.8)
        for k in range(nb):
            y = (k + 0.5) * bw
            objs.append(copy_at(proto, (side * R, y, 0), -side * math.pi / 2))
            objs.append(copy_at(at, (side * (R - 0.6), y, H + attic * 0.2), -side * math.pi / 2))
        bpy.data.objects.remove(proto, do_unlink=True)
        bpy.data.objects.remove(at, do_unlink=True)
    # the apse: bays around the outer half circle
    na = max(5, round(math.pi * R / 9))
    proto = _giant_bay(math.pi * R / na, H)
    at = _attic_bay(math.pi * R / na, attic * 0.8)
    for k in range(na):
        a = math.pi * (k + 0.5) / na  # 0..pi over the +Y half
        x, y = R * math.cos(a), L + R * math.sin(a)
        objs.append(copy_at(proto, (x, y, 0), a + math.pi / 2))
        objs.append(copy_at(at, ((R - 0.6) * math.cos(a), L + (R - 0.6) * math.sin(a), H + attic * 0.2), a + math.pi / 2))
    bpy.data.objects.remove(proto, do_unlink=True)
    bpy.data.objects.remove(at, do_unlink=True)
    # entablature and attic cornice all round
    objs += [box(f"{name}_ent", W + 2.4, L, 2.2, (0, L / 2, H - 0.2), hi), ellipse_ring(f"{name}_ent_apse", R + 1.2, R + 1.2, (R - 1) / (R + 1.2), 2.2, (0, L, H - 0.2), hi, n=48, arc=math.pi, start=0),
             box(f"{name}_cornice", W + 1.4, L, 1.0, (0, L / 2, H + attic), hi), ellipse_ring(f"{name}_cor_apse", R + 0.7, R + 0.7, (R - 1) / (R + 0.7), 1.0, (0, L, H + attic), hi, n=48, arc=math.pi, start=0)]
    if roofed:
        # low lead roofs, mostly hidden behind the attic: a flattened barrel over the arm, a half dome over the apse
        z0 = H + attic + 1.0
        vault = half_cyl_y(f"{name}_vault", R * 0.92, L + 0.2, (0, L / 2, z0), LEAD, verts=24)
        semi = dome(f"{name}_semidome", R * 0.92, (0, L, z0), LEAD, squash=1.0, segments=32, rings=10)
        bm = bmesh.new()
        bm.from_mesh(semi.data)
        bmesh.ops.bisect_plane(bm, geom=bm.verts[:] + bm.edges[:] + bm.faces[:], plane_co=(0, 0, 0), plane_no=(0, -1, 0), clear_outer=True)
        bmesh.ops.bisect_plane(bm, geom=bm.verts[:] + bm.edges[:] + bm.faces[:], plane_co=(0, 0, 0), plane_no=(0, 0, -1), clear_outer=True)
        bm.to_mesh(semi.data)
        bm.free()
        for o in (vault, semi):
            mw = o.matrix_world
            for v in o.data.vertices:
                w = mw @ v.co
                w.z = z0 + max(0.0, w.z - z0) * 0.32
                v.co = mw.inverted() @ w
        objs += [vault, semi]
    return join(objs, name)


def new_st_peters():
    """St Peter's around 1560: Michelangelo's crossing arms and apses up to the attic, the drum rising
    under scaffolding, centring for a vault, a stone yard; the old basilica's nave still in use behind
    Antonio da Sangallo's dividing wall of 1538."""
    m = Model("new-st-peters-construction")
    CY = 84            # the crossing, west of the old nave (model +Y)
    S = 46             # crossing square
    W, L, H, attic = 40, 16, 30, 8
    m.add(0, box("platform", 170, 210, 1.0, (0, 40, 0), shade(TRAV, -0.1)), "base")
    # the old nave, cut short at the dividing wall
    old = church("old_nave", 64, 86, 30, transept=False, porch=False, early=True, facade_mosaic=True)
    for stage, lst in sorted(old.stages.items()):
        for o in lst:
            if o.name.startswith("apse") or o.name == "platform":
                bpy.data.objects.remove(o, do_unlink=True)
                continue
            place(o, (0, -12, 0))
            m.add(min(stage, 2), o)
    m.add(1, box("dividing_wall", 66, 3, 34, (0, 32, 1.0), BRICK), "walls")
    # crossing piers and the four great arches between them
    for sx in (-1, 1):
        for sy in (-1, 1):
            m.add(1, box(f"pier{sx}{sy}", 16, 16, H + attic, (sx * (S / 2 - 8), CY + sy * (S / 2 - 8), 1.0), shade(TRAV, -0.05)))
    for k, (dx, dy, rot) in enumerate([(0, -S / 2 + 8, 0), (0, S / 2 - 8, 0), (-S / 2 + 8, 0, math.pi / 2), (S / 2 - 8, 0, math.pi / 2)]):
        arch = box(f"xarch{k}", S - 32 + 2, 8, 9, (0, 0, H + attic - 8), shade(TRAV, 0.03))
        place(arch, (dx, CY + dy, 1.0), rot)
        m.add(1, arch)
    # three arms with apses: west (+Y), north and south (x); the east arm is the old nave's place
    for name, ang, roofed in (("arm_w", 0.0, True), ("arm_n", math.pi / 2, True), ("arm_s", -math.pi / 2, False)):
        a = _michelangelo_arm(name, W, L, H, attic, roofed)
        place(a, (0, S / 2, 1.0))
        _about(a, ang, (0, 0, 0))
        place(a, (0, CY, 0))
        m.add(1, a, "arms")
    # the drum: 16 paired-column buttresses, windows with alternating pediments, rising under scaffolding
    dz = H + attic + 1.0
    Rd, Hd = 22, 13
    m.add(2, cylinder("drum_base", Rd + 2, 3, (0, CY, dz), shade(TRAV, -0.02), verts=48), "drum")
    m.add(2, cylinder("drum", Rd, Hd, (0, CY, dz + 3), TRAV, verts=48))

    def buttress():
        return join([box("bt", 3.2, 4.0, Hd, (0, -2.0, 0), shade(TRAV, 0.03)),
                     column("bc1", -1.1, -4.3, 0, Hd - 1.6, 0.55, "corinthian", shade(TRAV, 0.07)),
                     column("bc2", 1.1, -4.3, 0, Hd - 1.6, 0.55, "corinthian", shade(TRAV, 0.07)),
                     box("bent", 4.0, 5.2, 1.6, (0, -2.6, Hd - 1.6), shade(TRAV, 0.07))], "buttress")
    m.add(2, place(ring_of(buttress, 16, Rd, Rd, dz + 3, "drum_buttresses"), (0, CY, 0)))

    def drum_window():
        w = box("dw", 2.6, 0.6, 5.0, (0, -0.3, 2.5), DARK)
        top = box("dwp", 3.6, 0.9, 0.9, (0, -0.45, 7.6), shade(TRAV, 0.07))
        return join([w, top], "dwin")
    wins = []
    proto = drum_window()
    for i in range(16):
        a = math.tau * (i + 0.5) / 16
        wins.append(copy_at(proto, ((Rd + 0.2) * math.cos(a), CY + (Rd + 0.2) * math.sin(a), dz + 3), a + math.pi / 2))
    bpy.data.objects.remove(proto, do_unlink=True)
    m.add(2, join(wins, "drum_windows"))
    from rome_fora import scaffold, crane, stone_stack
    m.add(2, place(ring_of(lambda: join([box("sp", 0.4, 0.4, Hd + 8, (0, -6.5, 0), TIMBER), box("sp2", 0.4, 0.4, Hd + 8, (1.6, -6.5, 0), TIMBER),
                                   box("sb1", 2.2, 0.3, 0.3, (0.8, -6.5, 4), TIMBER), box("sb2", 2.2, 0.3, 0.3, (0.8, -6.5, 9), TIMBER),
                                   box("sb3", 2.2, 0.3, 0.3, (0.8, -6.5, 14), TIMBER), box("plank", 2.6, 1.4, 0.15, (0.8, -5.8, 9.2), TIMBER)], "scaf"),
                       14, Rd, Rd, dz + 3, "drum_scaffold", skip=lambda i, a: 2 <= i <= 5), (0, CY, 0)), "site")
    m.add(2, crane("crane_a", 10, CY + 4, dz + Hd + 6))
    m.add(2, crane("crane_b", -12, CY - 6, dz + Hd + 2))
    # wooden centring in the open south arm, and the stone yard
    cent = []
    for k in range(5):
        rib = half_cyl_x(f"rib{k}", W * 0.46, 0.5, (-S / 2 - 4 - k * 3, CY, H + attic + 1.0), TIMBER, verts=16)
        cent.append(rib)
    m.add(2, join(cent, "centring"))
    for i, (x, y) in enumerate([(-60, 20), (-50, 10), (55, 15), (62, 30), (-62, 140), (60, 140)]):
        m.add(1, stone_stack(f"blocks{i}", x, y, 6))
    m.add(1, box("lime_pit", 10, 6, 0.6, (50, -2, 1.0), "#EDE6D6"))
    return m


# ====================================================================== Stadium of Domitian / Piazza Navona

def stadium(variant="stadium"):
    m = Model({"stadium": "stadium-of-domitian", "medieval": "stadium-medieval", "piazza": "piazza-navona"}[variant])
    L, W = 275, 106
    if variant == "stadium":
        m.add(0, slab_from_pts("track", stadium_pts(L - 30, W - 30), 0.4, color=SAND), "track")
        for k in range(5):
            m.add(0, stadium_ring(f"seat{k}", L - 28 + k * 5, W - 28 + k * 5, 3.0, 1.5 + k * 3.2, color=shade(TRAV, -0.04 + 0.03 * (k % 2))))
        def bay():
            return join([arch_bay("sb", 6.5, 10.5, 2.2, 2.0, 6.0, TRAV), column("sc", -3.25, -1.15, 0, 9.5, 0.45, "ionic", shade(TRAV, 0.05))], "sbay")
        perim = 2 * (L - W / 2) + math.pi * W / 2
        for t in range(2):
            m.add(1, along_stadium(bay, L, W, t * 10.5, int(perim / 6.5), f"facade{t}"), "facade")
        m.add(2, stadium_ring("roof", L, W, 4, 0.8, (0, 0, 21.0), color=TILE), "roof")
    else:
        m.add(0, slab_from_pts("piazza", stadium_pts(L - 20, W - 20), 0.4, color="#D6C39E"), "piazza")
        rnd = random.Random(7)
        houses = []
        perim_pts = []
        for i in range(44):
            s = i / 44
            if s < 0.4:
                x, y, a = -L / 2 + 10 + s / 0.4 * (L - W / 2 - 10), -W / 2 - 4, 0
            elif s < 0.6:
                t = (s - 0.4) / 0.2
                a = -math.pi / 2 + t * math.pi
                x, y = L / 2 - W / 2 + (W / 2 + 4) * math.cos(a), (W / 2 + 4) * math.sin(a)
                a = a + math.pi / 2
            else:
                x, y, a = L / 2 - W / 2 - (s - 0.6) / 0.4 * (L - W / 2 - 10), W / 2 + 4, math.pi
            h = rnd.uniform(9, 16) if variant == "medieval" else rnd.uniform(13, 20)
            col = rnd.choice([BRICK, shade(BRICK, 0.08)]) if variant == "medieval" else rnd.choice([PLASTER, "#E6C9A0", "#DDD5C4"])
            houses.append(box(f"h{i}", 11, 12, h, (x, y, 0), col, rot_z=a))
            houses.append(box(f"hr{i}", 11.6, 12.6, 0.8, (x, y, h), TILE, rot_z=a))

        m.add(1, join(houses, "houses"), "houses")
        if variant == "medieval":
            m.add(2, box("tower", 8, 8, 26, (L * 0.25, W / 2 + 8, 0), BRICK), "tower")
            m.add(2, box("sant_agnese", 14, 22, 12, (0, W / 2 + 10, 0), BRICK))
        else:
            for k, x in enumerate((-L * 0.32, 0, L * 0.3)):
                m.add(2, cylinder(f"basin{k}", 6, 1.0, (x, 0, 0.4), MARBLE, verts=24), "fountains")
                m.add(2, cylinder(f"water{k}", 5.4, 1.1, (x, 0, 0.4), WATER, verts=24))
                m.add(2, statue(f"triton{k}", x, 0, 1.4, 2.4, MARBLE))
            stalls = [box(f"stall{i}", 3, 2, 2.2, (-L * 0.4 + L * 0.8 * i / 15, (i % 2 - 0.5) * 16, 0.4), TIMBER) for i in range(16)]
            stalls += [box(f"awn{i}", 3.4, 2.6, 0.15, (-L * 0.4 + L * 0.8 * i / 15, (i % 2 - 0.5) * 16, 2.6), random.Random(i).choice(["#b5735a", "#c2a66d", "#8f9a7a"])) for i in range(16)]
            m.add(2, join(stalls, "market"))
            m.add(2, box("sant_agnese", 16, 24, 14, (0, W / 2 + 10, 0), PLASTER))
    return m


# ====================================================================== Curia

def curia(variant="julia"):
    m = Model({"julia": "curia-julia", "hostilia": "curia-hostilia", "church": "curia-church"}[variant])
    W, D, H = 17.6, 25.6, 21
    wall = BRICK if variant != "hostilia" else "#B9A28A"
    m.add(0, box("podium", W + 2.4, D + 2.4, 1.5, (0, 0, 0), shade(TRAV, -0.1)), "podium")
    m.add(0, steps_front("steps", 9, 1.5, 4, -D / 2 - 1.2, 0, TRAV, tread=0.6))
    m.add(1, box("walls", W, D, H, (0, 0, 1.5), wall), "walls")
    m.add(1, box("marble_dado", W + 0.3, D + 0.3, 7, (0, 0, 1.5), MARBLE if variant != "church" else PLASTER))
    for s in (-1, 1):
        m.add(1, box(f"buttress{s}", 1.6, 1.0, H, (s * (W / 2 - 0.3), -D / 2 - 0.4, 1.5), shade(wall, 0.05)))
    m.add(1, box("door", 4, 0.5, 9.5, (0, -D / 2 - 0.2, 1.5), BRONZE if variant == "julia" else DARK))
    m.add(1, box("door_frame", 5.6, 0.4, 11, (0, -D / 2 - 0.1, 1.5), MARBLE))
    for i in (-1, 0, 1):
        m.add(1, box(f"win{i}", 2.4, 0.5, 4.4, (i * 5.2, -D / 2 - 0.2, 14.5), DARK))
        m.add(1, box(f"winframe{i}", 3.0, 0.3, 5.0, (i * 5.2, -D / 2 - 0.1, 14.2), PLASTER))
    m.add(1, box("cornice", W + 1, D + 1, 0.8, (0, 0, 1.5 + H), shade(TRAV, 0.04)))
    m.add(2, pediment("pediment", W, D, 2.3 + H, 4.6, -D / 2, PLASTER, TILE, statues=False), "roof")
    if variant == "julia":
        m.add(1, colonnade("porch", [(-6, -D / 2 - 3), (-2, -D / 2 - 3), (2, -D / 2 - 3), (6, -D / 2 - 3)], 1.5, 8, 0.55, "ionic", MARBLE), "porch")
        m.add(1, box("porch_roof", 15, 4.5, 0.8, (0, -D / 2 - 2.6, 9.5), TILE))
    if variant == "church":
        m.add(2, box("campanile", 4, 4, 30, (W / 2 + 3, D / 2 - 4, 1.5), BRICK), "church")
        m.add(2, box("camp_open", 4.1, 4.1, 2.2, (W / 2 + 3, D / 2 - 4, 27), DARK))
        m.add(2, cylinder("cross", 0.2, 3, (0, -D / 2, 2.3 + H + 4.6), GOLD, verts=6))
    return m


# ====================================================================== the Roman Forum ensemble

def forum(variant="imperial"):
    m = Model({"imperial": "roman-forum", "republic": "roman-forum-republic", "regal": "roman-forum-regal", "medieval": "roman-forum-medieval"}[variant])
    if variant == "regal":
        from rome_more import forum_regal
        return forum_regal()
    if variant == "medieval":
        from rome_more import forum_medieval
        return forum_medieval()
    imperial = variant == "imperial"
    m.add(0, box("paving", 170, 70, 0.6, (0, 0, 0), "#D6C39E" if imperial else SAND), "paving")
    m.add(0, join([box(f"pave{k}", 170, 0.1, 0.05, (0, -35 + k * 3.5, 0.6), "#c4b08a") for k in range(20)], "paving_lines"))
    # Basilica Julia (south) / Sempronia: two-storey arcade around a tall nave
    bw, bd = (101, 49) if imperial else (70, 26)
    by = -36 - bd / 2
    col = MARBLE if imperial else BRICK
    m.add(0, box("bj_steps", bw + 2, bd + 2, 1.2, (0, by, 0), shade(TRAV, -0.08)))
    nb = int(bw / 6.2)
    def bjbay(h):
        return join([arch_bay("bjb", bw / nb + 0.05, h, 1.6, 1.9, h * 0.6, col), column("bjc", -bw / nb / 2, -0.8, 0, h - 0.8, 0.45, "tuscan", shade(col, 0.05))], "bjbay")
    for t, h in enumerate((8.5, 7.5)):
        proto = bjbay(h)
        objs = [copy_at(proto, (-bw / 2 + (k + 0.5) * bw / nb, by + bd / 2 - 0.8, 1.2 + t * 8.5)) for k in range(nb)]
        objs += [copy_at(proto, (-bw / 2 + 0.8, by - bd / 2 + (k + 0.5) * bd / int(bd / 6.2), 1.2 + t * 8.5), -math.pi / 2) for k in range(int(bd / 6.2))]
        bpy.data.objects.remove(proto, do_unlink=True)
        m.add(1, join(objs, f"bj_arcade{t}"), "basilicas")
    m.add(1, box("bj_nave", bw * 0.7, bd * 0.55, 22, (0, by, 1.2), shade(col, -0.04)))
    m.add(2, tiled_hip_roof("bj_roof", bw * 0.7, bd * 0.55, 6, (0, by, 23.2)), "roofs")
    m.add(2, box("bj_gallery_roof", bw, bd, 0.6, (0, by, 17.2), shade(TILE, -0.05)))
    # Basilica Aemilia (north), with the row of shops along its front
    aw, ad = (90, 28) if imperial else (80, 26)
    ay = 36 + ad / 2
    m.add(1, box("ba_body", aw, ad, 16, (10, ay, 0), col))
    m.add(1, join([box(f"ba_shop{k}", 5, 0.5, 4, (10 - aw / 2 + 3 + k * 6, ay - ad / 2 - 0.2, 0), DARK) for k in range(int(aw / 6))], "tabernae"))
    m.add(1, colonnade("ba_portico", [(10 - aw / 2 + 2 + k * (aw - 4) / 15, ay - ad / 2 - 3) for k in range(16)], 0, 9, 0.5, "doric", MARBLE))
    m.add(2, box("ba_portico_roof", aw, 5, 0.6, (10, ay - ad / 2 - 2.5, 9), TILE))
    m.add(2, tiled_hip_roof("ba_roof", aw, ad, 6, (10, ay, 16)))
    # Temple of Castor and Pollux, Temple of Vesta, Temple of Divus Julius
    for name, kw, (dx, dy) in [("castor", dict(w=32 if imperial else 26, d=50 if imperial else 40, podium=7 if imperial else 5, col_h=14 if imperial else 11, front=8 if imperial else 6, side=11, order="corinthian", kind="peripteral"), (62, -50 if imperial else -46))] + ([("divus_julius", dict(w=27, d=30, podium=3.5, col_h=10, front=6, side=2, order="corinthian", kind="prostyle"), (92, 8))] if imperial else []):
        t = temple(name, color=MARBLE if imperial else TRAV, statues=imperial, **kw)
        for stage, lst in sorted(t.stages.items()):
            for o in lst:
                o.rotation_euler[2] = math.pi if name == "divus_julius" else 0
                place(o, (dx, dy, 0))
                m.add(min(stage, 2), o)
    v = tholos("vesta", 5.8, 7.5)
    for stage, lst in sorted(v.stages.items()):
        for o in lst:
            place(o, (84, -18, 0))
            m.add(min(stage, 2), o)
    # Rostra with ship's beaks and statues, honorific columns
    rx, ry = (-78, 0) if imperial else (-60, 28)
    m.add(0, box("rostra", 24, 12, 3.4, (rx, ry, 0), MARBLE))
    m.add(1, join([cyl_x(f"beak{i}", 0.35, 2.4, (rx - 12.5, ry - 5 + i * 2, 1.6), BRONZE, verts=6) for i in range(6)], "beaks"))
    m.add(1, join([statue(f"rst{i}", rx - 9 + i * 4.5, ry, 3.4, 2.6, BRONZE) for i in range(5)], "rostra_statues"))
    for i, (x, y) in enumerate([(-40, 12), (-20, -14), (30, 10), (5, 18)]):
        m.add(1, box(f"colbase{i}", 3, 3, 2.5, (x, y, 0.6), MARBLE))
        m.add(1, column(f"hcol{i}", x, y, 3.1, 12 if imperial else 7, 0.7, "corinthian", "#9a9690" if imperial else TRAV))
        m.add(1, statue(f"hstat{i}", x, y, 3.1 + (12 if imperial else 7), 2.4, GOLD))
    m.add(1, box("lacus_curtius", 6, 4, 0.8, (-10, -2, 0.6), shade(MARBLE, -0.1)))
    return m


BUILDERS = {
    "rome/circus-maximus": lambda: circus("imperial"),
    "rome/circus-maximus-late": lambda: circus("late"),
    "rome/circus-maximus-republic": lambda: circus("republic"),
    "rome/circus-maximus-regal": lambda: circus("regal"),
    "rome/arch-of-titus": lambda: triumphal_arch("arch-of-titus", 13.5, 15.4, 4.75, 1),
    "rome/arch-of-septimius-severus": lambda: triumphal_arch("arch-of-septimius-severus", 23, 21, 11, 3),
    "rome/arch-of-constantine": lambda: triumphal_arch("arch-of-constantine", 26, 21, 7.4, 3, attic_statues=True),
    "rome/basilica-of-maxentius": lambda: basilica_nova(False),
    "rome/basilica-of-maxentius-ruin": lambda: basilica_nova(True),
    "rome/theatre-of-marcellus": lambda: theatre("theatre-of-marcellus", 65, 2),
    "rome/theatre-of-marcellus-fortress": lambda: theatre("theatre-of-marcellus-fortress", 65, 2, top="fortress"),
    "rome/theatre-of-marcellus-palazzo": lambda: theatre("theatre-of-marcellus-palazzo", 65, 2, top="palazzo"),
    "rome/theatre-of-pompey": lambda: theatre("theatre-of-pompey", 75, 3, scaena_h=36, porticus=True, temple_top=True),
    "rome/mausoleum-of-hadrian": lambda: hadrianeum("mausoleum"),
    "rome/castel-santangelo-late": lambda: hadrianeum("late"),
    "rome/castel-santangelo-medieval": lambda: hadrianeum("medieval"),
    "rome/castel-santangelo-renaissance": lambda: hadrianeum("renaissance"),
    "rome/mausoleum-of-augustus": lambda: mausoleum_augustus("tomb"),
    "rome/mausoleum-of-augustus-fortress": lambda: mausoleum_augustus("fortress"),
    "rome/mausoleum-of-augustus-ruin": lambda: mausoleum_augustus("ruin"),
    "rome/old-st-peters": lambda: church("old-st-peters", 64, 120, 30, atrium=True, transept=True, facade_mosaic=True, early=True),
    "rome/old-st-peters-medieval": lambda: church("old-st-peters-medieval", 64, 120, 30, atrium=True, transept=True, campanile=True, facade_mosaic=True, early=True),
    "rome/new-st-peters-construction": new_st_peters,
    "rome/lateran-basilica": lambda: church("lateran-basilica", 56, 100, 28, transept=True, early=True),
    "rome/lateran-medieval": lambda: church("lateran-medieval", 56, 100, 28, transept=True, campanile=True, facade_mosaic=True),
    "rome/santa-maria-maggiore": lambda: church("santa-maria-maggiore", 36, 80, 22, campanile=True, facade_mosaic=True),
    "rome/santa-maria-in-aracoeli": lambda: church("santa-maria-in-aracoeli", 34, 68, 20, porch=False),
    "rome/santa-maria-in-cosmedin": lambda: church("santa-maria-in-cosmedin", 22, 40, 14, campanile=True),
    "rome/santa-maria-in-trastevere": lambda: church("santa-maria-in-trastevere", 32, 56, 18, campanile=True, facade_mosaic=True),
    "rome/santa-maria-in-trastevere-early": lambda: church("santa-maria-in-trastevere-early", 30, 50, 14, porch=False, early=True),
    "rome/san-clemente": lambda: church("san-clemente", 28, 50, 16, atrium=True, campanile=True, porch=False),
    "rome/san-clemente-early": lambda: church("san-clemente-early", 28, 50, 14, porch=False, early=True),
    "rome/tiber-island-church": lambda: church("tiber-island-church", 24, 44, 14, campanile=True, porch=True),
    "rome/stadium-of-domitian": lambda: stadium("stadium"),
    "rome/stadium-medieval": lambda: stadium("medieval"),
    "rome/piazza-navona": lambda: stadium("piazza"),
    "rome/curia-julia": lambda: curia("julia"),
    "rome/curia-hostilia": lambda: curia("hostilia"),
    "rome/curia-church": lambda: curia("church"),
    "rome/roman-forum": lambda: forum("imperial"),
    "rome/roman-forum-republic": lambda: forum("republic"),
}
