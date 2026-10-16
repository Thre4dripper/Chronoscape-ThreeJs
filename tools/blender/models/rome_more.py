"""Rome: the expanded landmark set (ancient, late antique, medieval, Renaissance). Parametric families."""
import math
from chronokit import *
from chronokit import _finish
import rome as base


# ---------------------------------------------------------------- generic families

def cross_vault_block(m, stage, name, w, d, h, loc, color):
    """A big vaulted hall: a box with a half-barrel vault on top (ridge along x)."""
    m.add(stage, box(name, w, d, h, loc, color))
    bpy.ops.mesh.primitive_cylinder_add(vertices=20, radius=d / 2, depth=w, location=(loc[0], loc[1], loc[2] + h), rotation=(0, math.pi / 2, 0))
    o = bpy.context.active_object
    bpy.ops.object.transform_apply(location=True, rotation=True, scale=True)
    bm = bmesh.new()
    bm.from_mesh(o.data)
    bmesh.ops.bisect_plane(bm, geom=bm.verts[:] + bm.edges[:] + bm.faces[:], plane_co=(0, 0, loc[2] + h), plane_no=(0, 0, 1), clear_inner=True)
    bmesh.ops.contextual_create(bm, geom=[e for e in bm.edges if abs(e.verts[0].co.z - (loc[2] + h)) < 1e-4 and abs(e.verts[1].co.z - (loc[2] + h)) < 1e-4])
    bm.to_mesh(o.data)
    bm.free()
    m.add(stage, _finish(o, name + "_vault", shade(color, 0.05)))


def rotunda(name, r, h, dome_color="bronze", color="brick", portico=(8, 0), drum_steps=2, oculus=False):
    m = Model(name)
    m.add(0, cylinder("base", r + 1.5, 1.5, color=shade(color, -0.1)), "base")
    for i in range(drum_steps):
        m.add(1 if i == 0 else 1, cylinder(f"drum{i}", r - i * 1.2, h / drum_steps, (0, 0, 1.5 + i * h / drum_steps), shade(color, -0.02 * i), verts=40), "drum")
    m.add(2, dome("dome", r - (drum_steps - 1) * 1.2, (0, 0, 1.5 + h), dome_color, squash=0.6, segments=36, rings=14), "dome")
    if oculus:
        m.add(2, cylinder("oculus", r * 0.2, 1.2, (0, 0, 1.5 + h + (r) * 0.6 - 0.4), "dark", verts=16))
    cols, depth = portico
    if cols:
        pw = r * 1.4
        m.add(1, box("porch_base", pw, depth, 1.5, (0, -r - depth / 2, 0), shade(color, -0.1)))
        pts = peristyle(pw - 3, depth - 3, cols, 3)
        m.add(1, columns("porch_cols", pts, 1.2, h * 0.75, (0, -r - depth / 2, 1.5), "limestone"))
        m.add(2, box("porch_ent", pw, depth, 2, (0, -r - depth / 2, 1.5 + h * 0.75 + 1)))
        m.add(2, gable_roof("porch_roof", pw, depth, pw * 0.16, (0, -r - depth / 2, 1.5 + h * 0.75 + 3), "terracotta"))
        m.add(1, box("transition", pw * 0.8, 6, h, (0, -r, 1.5), color))
    return m


def theatre(name, rx, tiers=2, tier_h=11, scaena_h=None, color="travertine", top=None):
    m = Model(name)
    arc, start = math.pi, 0.0
    m.add(0, ellipse_ring("orchestra", rx * 0.35, rx * 0.35, 0.01, 0.6, color="sand", arc=arc, start=start), "cavea")
    for k in range(3):
        outer = 0.35 + 0.2 * (k + 1)
        inner = (0.35 + 0.2 * k) / outer
        m.add(0, ellipse_ring(f"cavea{k}", rx * outer, rx * outer, inner, 6 * (k + 1), color=shade(color, -0.02 * k), arc=arc, start=start))
    for t in range(tiers):
        z = t * tier_h
        m.add(1, ellipse_ring(f"wall{t}", rx * 0.975, rx * 0.975, 0.94 / 0.975, tier_h, (0, 0, z), color=shade(color, -0.04), arc=arc, start=start), "arcades")
        pil = []
        for i in range(int(rx / 3)):
            a = start + arc * (i + 0.5) / int(rx / 3)
            x, y = rx * 0.985 * math.cos(a), rx * 0.985 * math.sin(a)
            pil.append(box(f"p{t}_{i}", 2.6, 2.6, tier_h, (x, y, z), shade(color, 0.06), rot_z=a))
        m.add(1, join(pil, f"pillars{t}"))
    sh = scaena_h or tiers * tier_h
    m.add(2, box("scaena", rx * 1.9, rx * 0.22, sh, (0, -rx * 0.11, 0), shade(color, 0.02)), "scaena")
    m.add(2, box("stage", rx * 1.4, rx * 0.16, 1.5, (0, rx * 0.08, 0), "timber"))
    m.add(2, gable_roof("scaena_roof", rx * 1.9, rx * 0.22, 5, (0, -rx * 0.11, sh), "terracotta"))
    if top == "fortress":
        for s in (-1, 1):
            m.add(2, box(f"tower{s}", 12, 12, 22, (s * rx * 0.7, rx * 0.4, tiers * tier_h), "brick"))
        m.add(2, box("keep", 30, 16, 14, (0, rx * 0.55, tiers * tier_h), "brick"))
    if top == "palazzo":
        m.add(2, box("palazzo", rx * 1.3, rx * 0.5, 16, (0, rx * 0.45, tiers * tier_h), "#D8C7A8"))
        m.add(2, box("palazzo_roof", rx * 1.3 + 1, rx * 0.5 + 1, 1.2, (0, rx * 0.45, tiers * tier_h + 16), "terracotta"))
    return m


def imperial_forum(name, w, d, temple_w=None, construction=False, column=False, basilica=False, hemicycle=False, exedrae=False):
    m = Model(name)
    m.add(0, box("plaza", w, d, 0.8, color="plaza"), "plaza")
    for s in (-1, 1):
        m.add(1, box(f"portico{s}", 8, d, 12, (s * (w / 2 - 4), 0, 0.8), "marble"), "porticoes")
        m.add(1, columns(f"pcols{s}", [(s * (w / 2 - 9), -d / 2 + 4 + (d - 8) * i / 11) for i in range(12)], 0.9, 10, (0, 0, 0.8), "marble"))
        m.add(2, box(f"portico_roof{s}", 10, d + 1, 1.2, (s * (w / 2 - 4), 0, 12.8), "terracotta"), "roofs")
        if exedrae:
            # semicircular halls behind the porticoes, opening onto the forum
            m.add(1, ellipse_ring(f"exedra{s}", 26, 26, 0.84, 14, (s * (w / 2 - 2), d * 0.08, 0.8), color=shade("marble", -0.05), arc=math.pi, start=(-math.pi / 2 if s > 0 else math.pi / 2)))
    if basilica:
        m.add(1, box("basilica", w + 10, d * 0.22, 16, (0, d / 2 - d * 0.11, 0.8), "marble"))
        m.add(1, columns("bcols", [(-w / 2 + 6 + (w - 12) * i / 15, d / 2 - d * 0.22 + 3) for i in range(16)], 1.1, 12, (0, 0, 0.8), "marble"))
        m.add(2, hip_roof("basilica_roof", w + 10, d * 0.22, 7, (0, d / 2 - d * 0.11, 16.8), "terracotta"))
    tw = temple_w or w * 0.4
    if construction:
        m.add(1, box("temple_podium", tw, tw * 1.3, 4, (0, d / 2 - tw * 0.65 - 2, 0.8), shade("limestone", -0.08)))
        scaf = []
        for i in range(6):
            for j in range(2):
                scaf.append(box(f"scaf{i}{j}", 0.5, 0.5, 14, (-tw / 2 + 2 + (tw - 4) * i / 5, d / 2 - tw * 1.3 * (0.2 + 0.6 * j) - 2, 4.8), "timber"))
        m.add(1, join(scaf, "scaffold"))
        m.add(1, box("crane", 1.2, 1.2, 20, (tw / 2 + 6, d / 2 - 20, 0.8), "timber"))
        for i in range(5):
            m.add(0, box(f"blocks{i}", 4, 3, 2.5, (-w / 3 + i * 9, -d / 4, 0.8), "marble"))
    elif not column:
        base_, body, roof = mini_temple("temple", tw, tw * 1.3, 4, 14, 8, 0, (0, d / 2 - tw * 0.65 - 2, 0.8), "marble")
        m.add(1, base_); m.add(1, body); m.add(2, roof)
    if column:
        m.add(2, cylinder("column", 1.85, 30, (0, d / 2 - 20, 0.8), "marble", verts=16))
        m.add(2, box("col_base", 6, 6, 5, (0, d / 2 - 20, 0.8), "marble"))
        m.add(2, cylinder("statue", 1.2, 5, (0, d / 2 - 20, 35.8), "bronze", verts=8))
    if hemicycle:
        # Trajan's Markets: a brick hemicycle wrapped against the cut face of the Quirinal, just beyond the east exedra
        cx, cy = w / 2 + 6, -d * 0.05
        m.add(1, ellipse_ring("markets", 52, 52, 0.72, 16, (cx, cy, 0.8), color="brick", arc=math.pi, start=-math.pi / 2), "markets")
        m.add(2, ellipse_ring("markets_upper", 50, 50, 0.78, 8, (cx, cy, 16.8), color=shade("brick", 0.08), arc=math.pi, start=-math.pi / 2))
        m.add(2, ellipse_ring("markets_roof", 53, 53, 0.7, 1, (cx, cy, 16.8), color="terracotta", arc=math.pi, start=-math.pi / 2))
    return m


def column_monument(name, h, shaft_r, base_w):
    m = Model(name)
    m.add(0, box("base", base_w, base_w, base_w * 0.9, color="marble"), "base")
    m.add(1, cylinder("shaft", shaft_r, h, (0, 0, base_w * 0.9), "marble", verts=18), "shaft")
    m.add(2, box("capital", shaft_r * 2.6, shaft_r * 2.6, 2, (0, 0, base_w * 0.9 + h), "marble"), "statue")
    m.add(2, cylinder("statue", shaft_r * 0.6, shaft_r * 2.4, (0, 0, base_w * 0.9 + h + 2), "bronze", verts=8))
    return m


def baths(name, w, d, variant="full"):
    m = Model(name)
    col = "brick"
    m.add(0, box("enclosure", w, d, 1, color="plaza"), "enclosure")
    if variant == "church":
        col = "#D8C7A8"
    if variant in ("full", "church", "construction"):
        bw, bd = w * 0.62, d * 0.4
        m.add(0, box("ground", bw, bd, 2, (0, -d * 0.05, 1), shade(col, -0.08)))
        cross_vault_block(m, 1, "frigidarium", bw * 0.42, bd * 0.35, 26, (0, -d * 0.05, 3), col)
        m.add(1, box("tepidarium", bw * 0.22, bd * 0.3, 18, (0, -d * 0.05 - bd * 0.3, 3), col), "halls")
        m.add(1, cylinder("caldarium", bd * 0.3, 20, (0, -d * 0.05 - bd * 0.55, 3), col, verts=24))
        m.add(2, dome("caldarium_dome", bd * 0.3, (0, -d * 0.05 - bd * 0.55, 23), "bronze" if variant != "church" else "white", squash=0.6), "roofs")
        for s in (-1, 1):
            m.add(1, box(f"palaestra{s}", bw * 0.22, bd * 0.4, 12, (s * bw * 0.36, -d * 0.05, 3), col))
            m.add(2, box(f"palaestra_roof{s}", bw * 0.22 + 1, bd * 0.4 + 1, 1, (s * bw * 0.36, -d * 0.05, 15), "terracotta"))
            m.add(1, box(f"wing{s}", bw * 0.16, bd * 0.3, 16, (s * bw * 0.42, -d * 0.05 - bd * 0.3, 3), col))
        m.add(2, box("natatio_roof", bw * 0.4, bd * 0.2, 1, (0, -d * 0.05 + bd * 0.32, 15), "terracotta"))
        m.add(1, box("natatio", bw * 0.38, bd * 0.18, 0.5, (0, -d * 0.05 + bd * 0.32, 3), "water"))
        for s in (-1, 1):
            m.add(0, box(f"outer_wing{s}", 14, d * 0.7, 10, (s * (w / 2 - 7), 0, 1), shade(col, -0.04)))
        m.add(0, box("outer_back", w * 0.6, 12, 10, (0, d / 2 - 6, 1), shade(col, -0.04)))
        if variant == "church":
            m.add(2, box("cross", 1, 0.4, 6, (0, -d * 0.05, 29), "gold"))
        if variant == "construction":
            m.add(1, join([box(f"sc{i}", 0.5, 0.5, 24, (-bw * 0.2 + bw * 0.4 * i / 7, -d * 0.05 + bd * 0.2, 3), "timber") for i in range(8)], "scaffold"))
    else:  # ruin
        bw, bd = w * 0.62, d * 0.4
        m.add(0, box("ground", bw, bd, 2, (0, -d * 0.05, 1), shade(col, -0.08)))
        m.add(1, box("wall_a", bw * 0.4, 4, 22, (0, -d * 0.05 + bd * 0.17, 3), col), "walls")
        m.add(1, box("wall_b", 4, bd * 0.3, 18, (bw * 0.2, -d * 0.05, 3), col))
        m.add(1, box("wall_c", 4, bd * 0.3, 15, (-bw * 0.2, -d * 0.05, 3), col))
        m.add(1, box("wall_d", bw * 0.22, 4, 12, (-bw * 0.3, -d * 0.05 - bd * 0.3, 3), col))
        m.add(2, join([dome(f"tree{i}", 3 + (i % 3), (-w * 0.3 + w * 0.6 * ((i * 7) % 10) / 9, -d * 0.3 + d * 0.5 * ((i * 3) % 7) / 6, 1), "green", squash=1.3, segments=8, rings=5) for i in range(14)], "trees"), "vegetation")
    return m


def mausoleum_round(name, r, variant="tomb"):
    m = Model(name)
    m.add(0, cylinder("drum", r, 12, color="travertine", verts=40), "drum")
    if variant in ("tomb", "late"):
        m.add(1, cylinder("mound", r * 0.8, 10, (0, 0, 12), "green", verts=36, r_top=r * 0.6), "mound")
        m.add(1, join([cylinder(f"cyp{i}", 1.4, 9, (r * 0.62 * math.cos(math.tau * i / 14), r * 0.62 * math.sin(math.tau * i / 14), 22), "#4f6a3f", verts=6, r_top=0.2) for i in range(14)], "cypresses"))
        m.add(2, cylinder("tumulus", r * 0.3, 10, (0, 0, 22), "travertine", verts=24), "top")
        m.add(2, cylinder("statue", 1.5, 6, (0, 0, 32), "bronze", verts=8))
    if variant == "fortress":
        m.add(1, cylinder("wall", r * 0.9, 14, (0, 0, 12), "brick", verts=32), "walls")
        m.add(2, box("keep", 14, 14, 20, (0, 0, 26), "brick"), "keep")
        m.add(2, join([box(f"m{i}", 2, 2, 2.5, (r * 0.9 * math.cos(math.tau * i / 24), r * 0.9 * math.sin(math.tau * i / 24), 26), "brick") for i in range(24)], "merlons"))
    if variant == "ruin":
        m.add(1, cylinder("mound", r * 0.8, 6, (0, 0, 12), "green", verts=36, r_top=r * 0.7), "garden")
        m.add(2, join([dome(f"tree{i}", 3.5, (r * 0.5 * math.cos(math.tau * i / 8), r * 0.5 * math.sin(math.tau * i / 8), 18), "green", squash=1.3, segments=8, rings=5) for i in range(8)], "trees"), "trees")
    return m


def hadrianeum(name, variant):
    m = Model(name)
    m.add(0, box("base", 89, 89, 10, color="marble"), "base")
    m.add(1, cylinder("drum", 32, 21, (0, 0, 10), "travertine", verts=40), "drum")
    if variant == "mausoleum":
        m.add(1, cylinder("mound", 28, 8, (0, 0, 31), "green", verts=36, r_top=22))
        m.add(2, cylinder("tholos", 10, 10, (0, 0, 39), "marble", verts=24), "top")
        m.add(2, cylinder("quadriga", 2.5, 6, (0, 0, 49), "bronze", verts=8))
    else:
        m.add(1, cylinder("upper", 30, 10, (0, 0, 31), "brick", verts=36))
        m.add(2, box("keep", 20, 20, 16, (0, 0, 41), "brick"), "castle")
        if variant in ("medieval", "renaissance"):
            m.add(2, box("tower", 8, 8, 10, (0, 0, 57), "brick"))
            m.add(2, cylinder("angel", 1.2, 5, (0, 0, 67), "bronze", verts=6))
        if variant == "late":
            m.add(0, box("wall_link", 12, 60, 10, (-50, 0, 0), "brick"))
        if variant == "medieval":
            m.add(0, join([box(f"wall{s}", 100, 6, 12, (0, s * 50, 0), "brick") for s in (-1, 1)] + [box(f"wallx{s}", 6, 100, 12, (s * 50, 0, 0), "brick") for s in (-1, 1)], "curtain"))
        if variant == "renaissance":
            for sx in (-1, 1):
                for sy in (-1, 1):
                    m.add(0, box(f"bastion{sx}{sy}", 30, 30, 12, (sx * 58, sy * 58, 0), shade("brick", -0.05), rot_z=math.pi / 4))
            m.add(0, join([box(f"w{s}", 118, 8, 10, (0, s * 58, 0), "brick") for s in (-1, 1)] + [box(f"wx{s}", 8, 118, 10, (s * 58, 0, 0), "brick") for s in (-1, 1)], "curtain"))
    return m


def altar_enclosure(name):
    m = Model(name)
    m.add(0, box("platform", 13, 12, 1.2, color="marble"), "platform")
    m.add(1, box("wall_n", 11.6, 0.8, 6, (0, 5.5, 1.2), "marble"), "enclosure")
    m.add(1, box("wall_s", 11.6, 0.8, 6, (0, -5.5, 1.2), "marble"))
    m.add(1, box("wall_e", 0.8, 3.5, 6, (5.4, -3.5, 1.2), "marble"))
    m.add(1, box("wall_e2", 0.8, 3.5, 6, (5.4, 3.5, 1.2), "marble"))
    m.add(1, box("wall_w", 0.8, 3.5, 6, (-5.4, -3.5, 1.2), "marble"))
    m.add(1, box("wall_w2", 0.8, 3.5, 6, (-5.4, 3.5, 1.2), "marble"))
    m.add(2, steps("altar_steps", 5, 2, 4, (0, 2.5, 1.2), "marble", tread=0.6), "altar")
    m.add(2, box("altar", 5, 3, 2.5, (0, 0, 3.2), "marble"))
    return m


def stadium(name, length, width, variant="stadium"):
    m = Model(name)
    if variant == "stadium":
        m.add(0, slab_from_pts("track", stadium_pts(length - 20, width - 20), 0.6, color="sand"), "track")
        for k in range(2):
            m.add(1 if k else 0, stadium_ring(f"ring{k}", length - 6 * k, width - 6 * k, 7, 6 + 5 * k, color=shade("travertine", 0.03 * k)), "stands")
        m.add(2, join([box(f"pil{i}", 2.4, 2.4, 12, (-length / 2 + 10 + (length - 20) * i / 29, s * (width / 2 - 2), 0), shade("travertine", 0.08)) for i in range(30) for s in (-1, 1)], "arcade"), "arcade")
    elif variant == "medieval":
        m.add(0, slab_from_pts("piazza", stadium_pts(length - 20, width - 20), 0.6, color="plaza"), "piazza")
        houses = []
        for i in range(18):
            for s in (-1, 1):
                x = -length / 2 + 12 + (length - 24) * i / 17
                houses.append(box(f"h{i}{s}", 10, 12 + (i % 3) * 3, 9 + (i * 5) % 7, (x, s * (width / 2 + 2), 0), ["brick", shade("brick", 0.08), shade("brick", -0.06)][i % 3]))
        m.add(1, join(houses, "houses"), "houses")
        m.add(2, box("tower", 8, 8, 24, (length * 0.3, width / 2 + 6, 0), "brick"), "tower")
    else:  # piazza navona 1560
        m.add(0, slab_from_pts("piazza", stadium_pts(length - 20, width - 20), 0.6, color="plaza"), "piazza")
        houses = []
        for i in range(16):
            for s in (-1, 1):
                x = -length / 2 + 12 + (length - 24) * i / 15
                houses.append(box(f"h{i}{s}", 14, 14, 13 + (i * 5) % 6, (x, s * (width / 2 + 4), 0), ["#D8C7A8", "#E1D2B3", "#CDB997"][i % 3]))
                houses.append(box(f"r{i}{s}", 14.6, 14.6, 1, (x, s * (width / 2 + 4), 13 + (i * 5) % 6), "terracotta"))
        m.add(1, join(houses, "palazzi"), "palazzi")
        m.add(2, cylinder("fountain", 6, 1.2, (0, 0, 0.6), "water", verts=16), "fountains")
        m.add(2, cylinder("fountain_s", 5, 1.2, (length * 0.32, 0, 0.6), "water", verts=16))
        m.add(2, cylinder("fountain_n", 5, 1.2, (-length * 0.32, 0, 0.6), "water", verts=16))
        m.add(2, join([box(f"stall{i}", 3, 2, 2.2, (-length * 0.4 + length * 0.8 * i / 11, (i % 2 - 0.5) * 10, 0.6), "timber") for i in range(12)], "market"))
    return m


def church_from_temple(m, w, d, z=0):
    m.add(2, box("campanile", 4, 4, 22, (w / 2 + 3, -d / 2 + 3, z), "brick"), "church")
    m.add(2, box("cross", 0.6, 0.3, 3, (0, 0, z + 20), "gold"))


def small_temple(name, w, d, podium, col_h, front, side, church=False, color="limestone"):
    m = Model(name)
    b, body, roof = mini_temple("t", w, d, podium, col_h, front, side, color=color)
    m.add(0, b, "podium"); m.add(1, body, "columns"); m.add(2, roof, "roof")
    if church:
        m.add(1, box("infill", w * 0.86, d * 0.86, col_h, (0, 0, podium), "brick"))
        church_from_temple(m, w, d, podium)
    return m


def round_temple(name, r, col_h, church=False):
    m = Model(name)
    m.add(0, cylinder("podium", r + 2, 1.5, color=shade("marble", -0.08), verts=32), "podium")
    m.add(0, steps("steps", r, 1.5, 2, (0, -r - 2, 0), shade("marble", -0.06), tread=1.0))
    m.add(1, columns("cols", [(r * math.cos(math.tau * i / 20), r * math.sin(math.tau * i / 20)) for i in range(20)], 0.6, col_h, (0, 0, 1.5), "marble", capital=True), "columns")
    m.add(1, cylinder("cella", r * 0.72, col_h, (0, 0, 1.5), shade("marble", -0.04) if not church else "brick", verts=24))
    m.add(2, cylinder("roof", r + 2.5, col_h * 0.45, (0, 0, 1.5 + col_h + 0.5), "terracotta", verts=24, r_top=1.0), "roof")
    if church:
        m.add(2, box("cross", 0.5, 0.3, 3, (0, 0, 1.5 + col_h * 1.45 + 0.5), "gold"))
    return m


def bridge(name, length, arches, width=9, color="travertine", towers=False, houses=False):
    m = Model(name)
    span = length / arches
    deck_z = 9.0
    wall = box("spandrels", length, width, deck_z, (0, 0, 0), color)
    for i in range(arches):
        x = -length / 2 + span * (i + 0.5)
        r = span * 0.4
        bpy.ops.mesh.primitive_cylinder_add(vertices=24, radius=r, depth=width + 2, location=(x, 0, deck_z - 1.6 - r), rotation=(math.pi / 2, 0, 0))
        cutter = bpy.context.active_object
        wall = boolean_cut(wall, cutter)
    m.add(0, wall, "arches")
    # cutwaters on the upstream face of each pier
    m.add(0, join([cylinder(f"cutwater{i}", span * 0.12, 5, (-length / 2 + span * i, -width / 2, 0), shade(color, -0.08), verts=3) for i in range(1, arches)] or [box("pad", 0.1, 0.1, 0.1, (0, 0, 0), color)], "cutwaters"))
    m.add(1, box("road", length, width - 1.2, 0.3, (0, 0, deck_z), "plaza"), "deck")
    m.add(1, box("parapet_n", length, 0.6, 1.2, (0, width / 2 - 0.3, deck_z), shade(color, 0.05)))
    m.add(1, box("parapet_s", length, 0.6, 1.2, (0, -width / 2 + 0.3, deck_z), shade(color, 0.05)))
    if towers:
        m.add(2, box("tower", 8, 8, 18, (-length / 2 + 6, 0, deck_z), "brick"), "tower")
    if houses:
        m.add(2, join([box(f"h{i}", 6, 4, 6, (-length / 3 + i * 8, (i % 2 - 0.5) * (width + 2), deck_z), "brick") for i in range(6)], "houses"), "houses")
    return m


def porticus(name, w, d, variant="octavia"):
    m = Model(name)
    m.add(0, box("platform", w, d, 1.2, color="plaza"), "platform")
    if variant in ("octavia", "metelli"):
        col = "marble" if variant == "octavia" else "limestone"
        for s in (-1, 1):
            m.add(1, columns(f"side{s}", [(s * (w / 2 - 4), -d / 2 + 4 + (d - 8) * i / 11) for i in range(12)], 1, 9, (0, 0, 1.2), col), "colonnade")
            m.add(2, box(f"side_roof{s}", 10, d, 1, (s * (w / 2 - 4), 0, 11.2), "terracotta"), "roofs")
            m.add(1, columns(f"end{s}", [(-w / 2 + 4 + (w - 8) * i / 11, s * (d / 2 - 4)) for i in range(12)], 1, 9, (0, 0, 1.2), col))
            m.add(2, box(f"end_roof{s}", w, 10, 1, (0, s * (d / 2 - 4), 11.2), "terracotta"))
        m.add(1, box("propylon", 26, 12, 14, (0, -d / 2 + 2, 1.2), col))
        m.add(2, gable_roof("propylon_roof", 26, 12, 4, (0, -d / 2 + 2, 15.2), "terracotta"))
        for i, x in enumerate((-w * 0.2, w * 0.2)):
            b, body, roof = mini_temple(f"temple{i}", 24, 40, 3, 11, 6, 0, (x, 0, 1.2), col)
            m.add(1, b); m.add(1, body); m.add(2, roof)
    else:  # ghetto / fish market
        m.add(1, box("propylon", 26, 12, 14, (0, -d / 2 + 2, 1.2), shade("marble", -0.1)), "propylon")
        m.add(1, columns("surviving", [(-10, -d / 2 + 2), (10, -d / 2 + 2)], 1, 9, (0, 0, 1.2), "marble"))
        m.add(2, box("church", 24, 30, 12, (0, -d / 2 + 24, 1.2), "brick"), "houses")
        m.add(2, box("campanile", 4, 4, 20, (14, -d / 2 + 12, 1.2), "brick"))
        houses = []
        for i in range(24):
            x = -w / 2 + 6 + (w - 12) * (i % 8) / 7
            y = -d / 2 + 44 + (i // 8) * 22
            houses.append(box(f"h{i}", 10, 14, 10 + (i * 5) % 8, (x, y, 1.2), ["brick", shade("brick", 0.08), shade("brick", -0.08)][i % 3]))
        m.add(2, join(houses, "ghetto_houses"))
        m.add(2, join([box(f"stall{i}", 3, 2, 2.2, (-12 + i * 4, -d / 2 + 10, 1.2), "timber") for i in range(7)], "fish_stalls"))
    return m


def basilica_nova(name, ruin=False):
    m = Model(name)
    m.add(0, box("platform", 100, 65, 2, color=shade("brick", -0.1)), "platform")
    if not ruin:
        cross_vault_block(m, 1, "nave", 80, 25, 35, (0, 0, 2), "brick")
        m.add(1, box("apse", 12, 20, 24, (-46, 0, 2), "brick"), "aisles")
    for i in range(3):
        x = -30 + i * 30
        cross_vault_block(m, 1, f"aisle_n{i}", 24, 18, 24, (x, 21, 2), "brick")
        if not ruin:
            cross_vault_block(m, 1, f"aisle_s{i}", 24, 18, 24, (x, -21, 2), "brick")
    if ruin:
        m.add(2, join([box(f"stub{i}", 3, 3, 5 + i, (-30 + i * 15, -18, 2), "brick") for i in range(5)], "stubs"), "ruins")
    else:
        m.add(2, box("roof", 82, 27, 1.2, (0, 0, 37), "terracotta"), "roof")
    return m


def arch3(name, w, h, d):
    m = Model(name)
    piers = []
    xs = [-w / 2 + w * 0.09, -w * 0.17, w * 0.17, w / 2 - w * 0.09]
    for i, x in enumerate(xs):
        piers.append(box(f"pier{i}", w * 0.16, d, h * 0.6, (x, 0, 0), "marble"))
    m.add(0, join(piers, "piers"), "piers")
    cols = []
    for x in xs:
        for s in (-1, 1):
            cols.append(cylinder(f"c{x:.0f}{s}", 0.9, h * 0.62, (x, s * (d / 2 + 0.6), 0), shade("marble", 0.04), verts=10, r_top=0.8))
    m.add(0, join(cols, "columns"))
    span = box("spandrel", w, d, h * 0.2, (0, 0, h * 0.6), "marble")
    cut = cylinder("cut", w * 0.13, d + 2, (0, 0, 0), "marble", verts=24)
    cut.rotation_euler = (math.pi / 2, 0, 0); bpy.ops.object.transform_apply(rotation=True); cut.location = (0, 0, h * 0.6)
    span = boolean_cut(span, cut)
    for s in (-1, 1):
        cut2 = cylinder(f"cut{s}", w * 0.075, d + 2, (0, 0, 0), "marble", verts=20)
        cut2.rotation_euler = (math.pi / 2, 0, 0); bpy.ops.object.transform_apply(rotation=True); cut2.location = (s * w * 0.33, 0, h * 0.5)
        span = boolean_cut(span, cut2)
    m.add(1, span, "arches")
    m.add(1, box("cornice", w + 0.6, d + 0.6, 0.6, (0, 0, h * 0.8), shade("marble", 0.06)))
    m.add(2, box("attic", w - 0.4, d - 0.4, h * 0.2, (0, 0, h * 0.8 + 0.6), shade("marble", -0.02)), "attic")
    m.add(2, box("inscription", w * 0.5, 0.3, h * 0.12, (0, -d / 2 + 0.1, h * 0.84), "bronze"))
    m.add(2, box("quadriga", w * 0.3, d * 0.6, h * 0.14, (0, 0, h + 0.6), "bronze"))
    return m


def double_temple(name, church=False):
    m = Model(name)
    m.add(0, box("platform", 145, 100, 3, color=shade("marble", -0.1)), "platform")
    m.add(0, columns("platform_cols", [(-70 + 140 * i / 19, s * 48) for i in range(20) for s in (-1, 1)], 0.9, 8, (0, 0, 3), "limestone"))
    m.add(0, box("podium", 110, 53, 3, (0, 0, 3), shade("marble", -0.06)))
    if not church:
        m.add(1, columns("cols", peristyle(104, 48, 10, 20), 1.4, 17, (0, 0, 6), "marble"), "columns")
        m.add(1, box("cella", 80, 26, 17, (0, 0, 6), shade("marble", -0.04)))
        for s in (-1, 1):
            m.add(1, cylinder(f"apse{s}", 12, 17, (s * 4, 0, 6), shade("marble", -0.06), verts=24))
        m.add(2, box("ent", 110, 53, 2, (0, 0, 24)), "roof")
        m.add(2, gable_roof("roof", 110, 53, 14, (0, 0, 26), "terracotta"))
    else:
        m.add(1, cylinder("apse_w", 12, 17, (-4, 0, 6), shade("marble", -0.06), verts=24), "remains")
        m.add(1, columns("stubs", [(-50, -22), (-40, -22), (50, 22), (40, 22), (50, -22)], 1.4, 6, (0, 0, 6), "marble"))
        m.add(2, box("church", 36, 22, 16, (30, 0, 6), "#D8C7A8"), "church")
        m.add(2, gable_roof("church_roof", 36, 22, 6, (30, 0, 22), "terracotta"))
        m.add(2, box("campanile", 5, 5, 34, (14, -12, 6), "brick"))
    return m


def christian_basilica(name, w, d, nave_h=22, atrium=False, campanile=False, transept=False, portico=True, color="brick"):
    m = Model(name)
    m.add(0, box("platform", w + 6, d + (d * 0.6 if atrium else 0) + 6, 1.2, (0, -(d * 0.3) if atrium else 0, 0), shade("limestone", -0.1)), "platform")
    nave_w = w * 0.46
    m.add(1, box("nave", nave_w, d, nave_h, (0, 0, 1.2), color), "nave")
    for s in (-1, 1):
        m.add(1, box(f"aisle{s}", (w - nave_w) / 2, d, nave_h * 0.55, (s * (nave_w / 2 + (w - nave_w) / 4), 0, 1.2), shade(color, -0.04)))
        m.add(2, box(f"aisle_roof{s}", (w - nave_w) / 2 + 0.6, d + 0.6, 0.8, (s * (nave_w / 2 + (w - nave_w) / 4), 0, 1.2 + nave_h * 0.55), "terracotta"), "roof")
    m.add(1, cylinder("apse", nave_w / 2, nave_h * 0.8, (0, d / 2, 1.2), color, verts=20))
    m.add(2, dome("apse_dome", nave_w / 2, (0, d / 2, 1.2 + nave_h * 0.8), "terracotta", squash=0.5, segments=16, rings=6))
    if transept:
        m.add(1, box("transept", w * 1.2, d * 0.2, nave_h, (0, d / 2 - d * 0.15, 1.2), color))
        m.add(2, gable_roof("transept_roof", d * 0.2, w * 1.2, nave_h * 0.3, (0, d / 2 - d * 0.15, 1.2 + nave_h), "terracotta"))
    m.add(2, gable_roof("nave_roof", nave_w, d, nave_h * 0.3, (0, 0, 1.2 + nave_h), "terracotta"))
    if portico:
        m.add(1, columns("porch", [(-nave_w / 2 + 1 + (nave_w - 2) * i / 5, -d / 2 - 4) for i in range(6)], 0.7, nave_h * 0.5, (0, 0, 1.2), "marble"))
        m.add(2, box("porch_roof", nave_w + 2, 6, 0.8, (0, -d / 2 - 3, 1.2 + nave_h * 0.5), "terracotta"))
    if atrium:
        aw, ad = w, d * 0.6
        for s in (-1, 1):
            m.add(1, columns(f"atrium{s}", [(s * (aw / 2 - 2), -d / 2 - 3 - ad * i / 9) for i in range(10)], 0.6, 6, (0, 0, 1.2), "marble"), "atrium")
            m.add(2, box(f"atrium_roof{s}", 5, ad, 0.6, (s * (aw / 2 - 2), -d / 2 - ad / 2 - 3, 7.2), "terracotta"))
        m.add(1, columns("atrium_front", [(-aw / 2 + 2 + (aw - 4) * i / 9, -d / 2 - ad - 3) for i in range(10)], 0.6, 6, (0, 0, 1.2), "marble"))
        m.add(2, box("atrium_front_roof", aw, 5, 0.6, (0, -d / 2 - ad - 3, 7.2), "terracotta"))
        m.add(1, cylinder("cantharus", 2.5, 1.2, (0, -d / 2 - ad / 2 - 3, 1.2), "water", verts=12))
    if campanile:
        m.add(2, box("campanile", 5, 5, nave_h * 1.9, (w / 2 + 3, -d / 2 + 4, 1.2), "brick"), "campanile")
        m.add(2, cylinder("spire", 3.2, 5, (w / 2 + 3, -d / 2 + 4, 1.2 + nave_h * 1.9), "terracotta", verts=4, r_top=0))
    return m


def new_st_peters(name):
    m = Model(name)
    m.add(0, box("platform", 160, 160, 2, color=shade("limestone", -0.1)), "platform")
    m.add(0, box("old_nave", 55, 90, 20, (0, -70, 2), "brick"))  # the old nave still in use to the east
    m.add(0, gable_roof("old_nave_roof", 55, 90, 7, (0, -70, 22), "terracotta"))
    m.add(0, box("dividing_wall", 60, 3, 24, (0, -24, 2), "brick"))
    for sx in (-1, 1):
        for sy in (-1, 1):
            m.add(1, box(f"pier{sx}{sy}", 22, 22, 44, (sx * 22, sy * 22 + 10, 2), "travertine"), "piers")
    for s in (-1, 1):
        m.add(1, box(f"arm{s}", 26, 40, 40, (s * 50, 10, 2), "travertine"))
        m.add(1, cylinder(f"apse{s}", 14, 36, (s * 66, 10, 2), "travertine", verts=20))
    m.add(1, box("arm_n", 40, 26, 40, (0, 60, 2), "travertine"))
    m.add(2, cylinder("drum", 24, 16, (0, 10, 46), "travertine", verts=32), "drum")
    m.add(2, join([box(f"buttress{i}", 3, 3, 16, (24 * math.cos(math.tau * i / 16), 10 + 24 * math.sin(math.tau * i / 16), 46), "travertine") for i in range(16)], "buttresses"))
    m.add(2, join([box(f"sc{i}", 0.5, 0.5, 30, (28 * math.cos(math.tau * i / 10), 10 + 28 * math.sin(math.tau * i / 10), 40), "timber") for i in range(10)], "scaffold"))
    m.add(2, box("crane", 1.2, 1.2, 40, (34, 10, 2), "timber"))
    return m


def tower(name, w, h, color="brick"):
    m = Model(name)
    m.add(0, box("base", w + 4, w + 4, 3, color=shade(color, -0.1)), "base")
    m.add(1, box("tower", w, w, h * 0.6, (0, 0, 3), color), "tower")
    m.add(2, box("upper", w * 0.8, w * 0.8, h * 0.4, (0, 0, 3 + h * 0.6), shade(color, 0.03)), "top")
    m.add(2, join([box(f"m{i}", 1.2, 1.2, 1.8, (w * 0.4 * math.cos(math.tau * i / 12), w * 0.4 * math.sin(math.tau * i / 12), 3 + h), color) for i in range(12)], "merlons"))
    return m


def tabularium(name, variant):
    m = Model(name)
    m.add(0, box("substructure", 73, 42, 14, color="limestone"), "substructure")
    m.add(0, join([box(f"arc{i}", 2.5, 2, 9, (-33 + 66 * i / 10, -21, 5), shade("limestone", 0.08)) for i in range(11)], "arcade"))
    if variant == "tabularium":
        m.add(1, box("gallery", 73, 42, 10, (0, 0, 14), "brick"), "upper")
        m.add(1, columns("cols", [(-33 + 66 * i / 10, -20) for i in range(11)], 0.9, 8, (0, 0, 24), "limestone"))
        m.add(2, box("roof", 74, 43, 1.2, (0, 0, 33), "terracotta"), "roof")
    elif variant == "medieval":
        m.add(1, box("palazzo", 60, 30, 16, (0, 2, 14), "brick"), "palazzo")
        m.add(2, box("tower_c", 10, 10, 24, (0, 2, 30), "brick"), "towers")
        m.add(2, box("tower_a", 7, 7, 14, (-26, 2, 30), "brick"))
        m.add(2, box("tower_b", 7, 7, 14, (26, 2, 30), "brick"))
    else:
        m.add(1, box("palazzo", 62, 30, 18, (0, 2, 14), "#D8C7A8"), "palazzo")
        m.add(1, steps("double_stair", 20, 10, 8, (0, -13, 14), "travertine", tread=1.5))
        m.add(2, box("tower_c", 10, 10, 28, (0, 4, 32), "#D8C7A8"), "tower")
        m.add(2, box("piazza", 60, 60, 0.8, (0, -52, 0), "plaza"))
        m.add(2, cylinder("statue_base", 3, 4, (0, -52, 0.8), "marble", verts=12))
        m.add(2, box("statue", 2, 4, 3, (0, -52, 4.8), "bronze"))
        m.add(2, join([box(f"sc{i}", 0.5, 0.5, 16, (-28 + 56 * i / 7, -24, 0.8), "timber") for i in range(8)], "scaffold"))
    return m


def palazzo(name, w, d, h, color="#D8C7A8", courtyard=True):
    m = Model(name)
    m.add(0, box("ground", w, d, 0.8, color=shade(color, -0.12)), "ground")
    if courtyard:
        t = min(w, d) * 0.28
        m.add(1, join([box("wn", w, t, h, (0, d / 2 - t / 2, 0.8), color), box("ws", w, t, h, (0, -d / 2 + t / 2, 0.8), color), box("we", t, d, h, (w / 2 - t / 2, 0, 0.8), color), box("ww", t, d, h, (-w / 2 + t / 2, 0, 0.8), color)], "block"), "block")
    else:
        m.add(1, box("block", w, d, h, (0, 0, 0.8), color), "block")
    m.add(1, join([box(f"win{i}{j}", 1.6, 0.4, 2.6, (-w / 2 + 3 + (w - 6) * i / 8, -d / 2 - 0.1, 0.8 + 3 + j * (h / 3)), "dark") for i in range(9) for j in range(3)], "windows"))
    m.add(2, box("cornice", w + 2, d + 2, 1.4, (0, 0, 0.8 + h), shade(color, 0.06)), "roof")
    m.add(2, hip_roof("roof", w, d, 4, (0, 0, 2.2 + h), "terracotta", ridge=0.5))
    return m


def villa(name):
    m = Model(name)
    m.add(0, box("garden", 70, 60, 0.6, color="green"), "garden")
    m.add(0, box("terrace", 48, 42, 1.2, (0, 0, 0.6), "plaza"))
    m.add(1, box("main", 30, 24, 12, (0, 4, 1.8), "#E1D2B3"), "villa")
    for s in (-1, 1):
        m.add(1, box(f"wing{s}", 10, 16, 12, (s * 20, -8, 1.8), "#E1D2B3"))
    m.add(1, box("loggia", 20, 6, 10, (0, -11, 1.8), "#E1D2B3"))
    m.add(1, join([box(f"arc{i}", 1.2, 1.2, 8, (-8 + 16 * i / 4, -14, 1.8), "marble") for i in range(5)], "loggia_arcade"))
    m.add(2, hip_roof("roof", 30, 24, 3.5, (0, 4, 13.8), "terracotta"), "roof")
    for s in (-1, 1):
        m.add(2, hip_roof(f"wing_roof{s}", 10, 16, 2.5, (s * 20, -8, 13.8), "terracotta"))
    m.add(2, join([dome(f"tree{i}", 2.5, (-30 + 60 * (i % 6) / 5, 22 + (i // 6) * 6, 0.6), "#4f6a3f", squash=1.6, segments=8, rings=5) for i in range(12)], "trees"))
    return m


def pyramid(name, base_w, h):
    m = Model(name)
    m.add(0, box("base", base_w + 4, base_w + 4, 1.5, color=shade("marble", -0.08)), "base")
    o = cylinder("pyramid", base_w / math.sqrt(2), h, (0, 0, 1.5), "marble", verts=4, r_top=0)
    o.rotation_euler[2] = math.pi / 4
    bpy.ops.object.transform_apply(rotation=True)
    m.add(1, o, "pyramid")
    m.add(2, join([cylinder(f"col{sx}{sy}", 0.7, 6, (sx * (base_w / 2 + 1.5), sy * (base_w / 2 + 1.5), 1.5), "marble", verts=8) for sx in (-1, 1) for sy in (-1, 1)], "corner_columns"), "columns")
    return m


def city_gate(name, variant):
    m = Model(name)
    if variant == "aqueduct":
        m.add(0, box("base", 32, 7, 2, color="travertine"), "base")
        piers = [box(f"pier{i}", 4, 7, 14, (-13 + 13 * i, 0, 2), "travertine") for i in range(3)]
        m.add(1, join(piers, "piers"), "arches")
        m.add(1, box("attic", 32, 7, 8, (0, 0, 16), "travertine"))
        m.add(2, box("channel", 32, 5, 5, (0, 0, 24), shade("travertine", 0.08)), "channels")
        m.add(2, box("channel2", 32, 5, 4, (0, 0, 29), shade("travertine", 0.12)))
    else:
        m.add(0, box("wall", 60, 8, 14, color="brick"), "wall")
        m.add(1, box("gate", 16, 12, 18, (0, 0, 0), shade("brick", 0.03)), "gate")
        m.add(1, box("passage", 6, 13, 9, (0, 0, 0), "dark"))
        for s in (-1, 1):
            m.add(2, cylinder(f"tower{s}", 6, 28, (s * 14, 0, 0), shade("brick", -0.04), verts=12), "towers")
            m.add(2, join([box(f"m{s}{i}", 1.2, 1.2, 1.6, (s * 14 + 6 * math.cos(math.tau * i / 10), 6 * math.sin(math.tau * i / 10), 28), "brick") for i in range(10)], f"merlons{s}"))
    return m


def castra(name):
    m = Model(name)
    W, D = 440, 380
    m.add(0, box("ground", W, D, 0.6, color="plaza"), "walls")
    m.add(0, join([box("wn", W, 6, 8, (0, D / 2, 0), "brick"), box("ws", W, 6, 8, (0, -D / 2, 0), "brick"), box("we", 6, D, 8, (W / 2, 0, 0), "brick"), box("ww", 6, D, 8, (-W / 2, 0, 0), "brick")], "curtain"))
    m.add(1, join([box(f"gate{i}", 20, 12, 12, p, shade("brick", 0.04)) for i, p in enumerate([(0, D / 2, 0), (0, -D / 2, 0), (W / 2, 0, 0), (-W / 2, 0, 0)])], "gates"), "gates")
    barracks = []
    for i in range(10):
        for j in range(6):
            barracks.append(box(f"b{i}{j}", 30, 12, 6, (-W / 2 + 40 + i * 40, -D / 2 + 40 + j * 55, 0.6), ["brick", shade("brick", 0.05)][(i + j) % 2]))
    m.add(2, join(barracks, "barracks"), "barracks")
    m.add(2, box("principia", 60, 40, 12, (0, 0, 0.6), shade("brick", 0.08)))
    return m


def emporium(name):
    m = Model(name)
    m.add(0, box("quay", 400, 40, 3, (0, 60, 0), "travertine"), "quay")
    m.add(0, join([box(f"ramp{i}", 10, 14, 1.5, (-180 + 40 * i, 68, 1.5), shade("travertine", -0.06)) for i in range(10)], "ramps"))
    m.add(1, box("porticus_aemilia", 380, 50, 12, (0, 10, 0), "brick"), "warehouses")
    m.add(2, join([gable_roof(f"vault{i}", 7, 50, 3, (-180 + 7.6 * i, 10, 12), "terracotta", overhang=0.2) for i in range(50)], "vaults"), "roofs")
    horrea = []
    for i in range(6):
        for j in range(2):
            horrea.append(box(f"h{i}{j}", 50, 30, 9, (-150 + i * 60, -40 - j * 40, 0), shade("brick", -0.04)))
    m.add(1, join(horrea, "horrea"))
    m.add(2, join([box(f"amph{i}", 2, 2, 2, (-190 + i * 12, 75, 3), "sand") for i in range(30)], "cargo"))
    return m


def ludus(name):
    m = Model(name)
    m.add(0, box("ground", 75, 60, 0.8, color="plaza"), "ground")
    m.add(0, ellipse_disc("arena", 31, 21, 0.6, (0, 0, 0.8), "sand", verts=40))
    m.add(1, ellipse_ring("seats", 36, 26, 0.86, 5, (0, 0, 0.8), color="travertine"), "seats")
    cells = []
    for i in range(14):
        cells.append(box(f"c_n{i}", 4.5, 5, 7, (-34 + 68 * i / 13, 27, 0.8), "brick"))
        cells.append(box(f"c_s{i}", 4.5, 5, 7, (-34 + 68 * i / 13, -27, 0.8), "brick"))
    m.add(2, join(cells, "cells"), "cells")
    m.add(2, box("roof_n", 75, 6, 0.8, (0, 27, 7.8), "terracotta"))
    m.add(2, box("roof_s", 75, 6, 0.8, (0, -27, 7.8), "terracotta"))
    return m


def hospital(name):
    m = Model(name)
    m.add(0, box("ground", 126, 36, 0.8, color=shade("brick", -0.1)), "ground")
    m.add(1, box("corsia", 120, 14, 14, (0, 0, 0.8), "brick"), "wards")
    m.add(1, box("octagon", 16, 16, 20, (0, 0, 0.8), shade("brick", 0.05)))
    m.add(1, join([box(f"win{i}", 1.4, 0.5, 4, (-56 + 112 * i / 20, -7.1, 7), "dark") for i in range(21)], "windows"))
    m.add(2, gable_roof("roof", 120, 14, 4, (0, 0, 14.8), "terracotta"), "roof")
    m.add(2, dome("lantern", 8, (0, 0, 20.8), "terracotta", squash=0.8, segments=8, rings=5))
    m.add(2, box("church", 30, 18, 14, (-70, 0, 0.8), "#D8C7A8"))
    m.add(2, gable_roof("church_roof", 30, 18, 5, (-70, 0, 14.8), "terracotta"))
    return m


# ---------------------------------------------------------------- variants of existing models

def forum_regal():
    m = Model("roman-forum-regal")
    m.add(0, box("ground", 170, 70, 0.6, color="sand"), "ground")
    m.add(0, box("cloaca", 170, 3, 0.4, (0, -5, 0.6), "water"))
    huts = []
    for i in range(10):
        x, y = -70 + 140 * ((i * 7) % 10) / 9, -25 + 50 * ((i * 3) % 7) / 6
        huts.append(cylinder(f"hut{i}", 4, 3, (x, y, 0.6), "timber", verts=8))
        huts.append(cylinder(f"roof{i}", 5, 3.5, (x, y, 3.6), "#8a7a58", verts=8, r_top=0.3))
    m.add(1, join(huts, "huts"), "huts")
    m.add(1, cylinder("vesta", 5, 4, (60, -10, 0.6), "timber", verts=10))
    m.add(2, cylinder("vesta_roof", 6, 4, (60, -10, 4.6), "#8a7a58", verts=10, r_top=0.3), "shrines")
    m.add(2, box("regia", 14, 10, 5, (78, 8, 0.6), "timber"))
    m.add(2, gable_roof("regia_roof", 14, 10, 3, (78, 8, 5.6), "#8a7a58"))
    m.add(2, box("comitium", 20, 20, 1, (-70, 20, 0.6), "limestone"))
    return m


def forum_medieval():
    m = Model("roman-forum-medieval")
    m.add(0, box("field", 170, 70, 0.6, color="#b7a66f"), "field")
    m.add(0, join([cylinder(f"cow{i}", 1.1, 1.6, (-60 + 120 * ((i * 7) % 11) / 10, -25 + 50 * ((i * 5) % 9) / 8, 0.6), "#8a6a4a", verts=6) for i in range(12)], "cattle"))
    m.add(1, columns("saturn_cols", [(-70 + 3 * i, -8) for i in range(8)], 1.1, 12, (0, 0, 0.6), "limestone"), "ruins")
    m.add(1, columns("castor_cols", [(55, -32), (59, -32), (63, -32)], 1.2, 14, (0, 0, 0.6), "marble"))
    m.add(1, box("ent", 12, 3, 2, (59, -32, 14.6), "marble"))
    m.add(1, join([box(f"base{i}", 3, 3, 1.5, (-40 + 20 * i, 10, 0.6), "limestone") for i in range(5)], "bases"))
    m.add(2, box("church_a", 22, 14, 12, (10, 36, 0.6), "brick"), "churches")
    m.add(2, gable_roof("church_a_roof", 22, 14, 4, (10, 36, 12.6), "terracotta"))
    m.add(2, box("campanile_a", 4, 4, 22, (24, 30, 0.6), "brick"))
    m.add(2, box("church_b", 18, 12, 10, (-20, -40, 0.6), "brick"))
    m.add(2, gable_roof("church_b_roof", 18, 12, 3.5, (-20, -40, 10.6), "terracotta"))
    m.add(2, join([dome(f"tree{i}", 3, (-80 + 160 * ((i * 13) % 17) / 16, -30 + 60 * ((i * 7) % 11) / 10, 0.6), "green", squash=1.3, segments=8, rings=5) for i in range(10)], "trees"))
    return m


def saturn_ruin():
    m = Model("temple-of-saturn-ruin")
    m.add(0, box("podium", 40, 22, 9, color=shade("limestone", -0.08)), "podium")
    pts = peristyle(37.8, 19.8, 6, 0) + [(-18.9, -5.4), (18.9, -5.4)]
    m.add(1, columns("cols", pts, 1.05, 11, (0, 0, 9), "limestone"), "columns")
    m.add(2, box("entablature", 40, 6, 1.8, (0, -8, 20.85), shade("limestone", 0.04)), "entablature")
    m.add(2, join([dome(f"bush{i}", 2, (-15 + 10 * i, 4, 9), "green", squash=1.2, segments=8, rings=5) for i in range(4)], "bushes"))
    return m


def curia_church():
    m = base.curia_julia("imperial")
    m.name = "curia-church"
    m.add(1, box("campanile", 4, 4, 30, (12, -10, 1.5), "brick"))
    m.add(1, box("cross", 0.5, 0.3, 3, (0, 0, 27.5), "gold"))
    return m


def jupiter_construction():
    m = Model("temple-of-jupiter-construction")
    m.add(0, box("podium", 54, 62, 6, color=shade("limestone", -0.08)), "podium")
    m.add(1, join([box(f"sc{i}{j}", 0.6, 0.6, 20, (-23 + 46 * i / 5, -27 + 7 * j, 6), "timber") for i in range(6) for j in range(3)], "scaffold"), "scaffold")
    m.add(1, join([box(f"blk{i}", 4, 3, 2.5, (-20 + 8 * i, 20, 6), "limestone") for i in range(6)], "blocks"))
    m.add(2, box("crane", 1.2, 1.2, 26, (30, 10, 6), "timber"), "cranes")
    m.add(2, box("crane2", 1.2, 1.2, 22, (-30, -10, 6), "timber"))
    m.add(2, columns("started", [(-19, -27), (-10.8, -27), (-2.6, -27)], 1.15, 9, (0, 0, 6), "limestone"))
    return m


def jupiter_archaic():
    m = base.temple_of_jupiter("republic")
    m.name = "temple-of-jupiter-archaic"
    return m


def colosseum_variant(kind):
    m = base.colosseum()
    m.name = "colosseum-" + kind
    if kind == "fortress":
        for i in range(4):
            a = math.tau * i / 4 + 0.4
            m.add(4, box(f"tower{i}", 8, 8, 16, (94.5 * 0.9 * math.cos(a), 78 * 0.9 * math.sin(a), 48), "brick"))
        m.add(4, box("keep", 24, 14, 14, (0, 60, 32), "brick"))
    else:
        # ruin: strip the pillars/attic on the south-west half by re-adding a collapsed look
        m.add(4, join([box(f"rubble{i}", 5, 4, 3, (-60 + 10 * i, -70 - (i % 3) * 6, 0), shade("travertine", -0.1)) for i in range(12)], "rubble"))
        m.add(4, join([dome(f"shrub{i}", 2.5, (70 * math.cos(math.tau * i / 9), 55 * math.sin(math.tau * i / 9), 20), "green", squash=1.2, segments=8, rings=5) for i in range(9)], "shrubs"))
    return m


def circus_regal():
    m = Model("circus-maximus-regal")
    m.add(0, slab_from_pts("track", stadium_pts(560, 100), 0.6, color="sand"), "track")
    m.add(1, join([box(f"post{i}", 1, 1, 5, (-270 + 540 * i / 39, s * 52, 0), "timber") for i in range(40) for s in (-1, 1)], "posts"), "stands")
    m.add(1, join([box(f"bench{i}", 40, 4, 1.5, (-260 + 36 * i, s * 54, 0), "timber") for i in range(15) for s in (-1, 1)], "benches"))
    m.add(2, join([cylinder(f"meta{s}{i}", 1.4, 6, (s * 160 + s * i * 3, (i - 1) * 2.5, 0.6), "limestone", verts=8, r_top=0.3) for s in (-1, 1) for i in range(3)], "metae"), "metae")
    return m


def orti_farnesiani():
    m = Model("orti-farnesiani")
    # three shallow garden terraces climbing the Palatine, with parterres, hedges, avenues and aviaries
    m.add(0, box("terrace_low", 240, 280, 1.0, color="#9DB08A"), "terraces")
    m.add(0, box("terrace_mid", 180, 180, 1.2, (0, 30, 1.0), "#A9B994"))
    m.add(0, box("terrace_top", 110, 110, 1.2, (0, 60, 2.2), "#B3C29E"))
    m.add(0, join([box(f"wall{i}", w, 2, 3, (0, y, z), "#D8C7A8") for i, (w, y, z) in enumerate([(180, -60, 0.6), (110, 5, 1.8)])], "retaining"))
    m.add(0, steps("stair", 14, 3.4, 6, (0, -60, 0), "#D8C7A8", tread=1.6))
    beds = []
    for i in range(4):
        for j in range(3):
            beds.append(box(f"bed{i}{j}", 34, 24, 0.5, (-60 + i * 40, -110 + j * 30, 1.0), "#7E9A6A"))
    m.add(1, join(beds, "parterres"), "garden")
    m.add(1, join([box(f"hedge{i}", 2, 260, 1.4, (-100 + i * 50, 0, 1.0), "#4f6a3f") for i in range(5)], "hedges"))
    m.add(1, join([dome(f"tree{i}", 4.5, (-95 + 190 * ((i * 7) % 12) / 11, -125 + 250 * ((i * 5) % 9) / 8, 1.0), "#4f6a3f", squash=1.5, segments=8, rings=5) for i in range(22)], "trees"))
    m.add(1, join([cylinder(f"cyp{i}", 1.3, 9, (s * 10, -120 + i * 12, 1.0), "#3f5a33", verts=6, r_top=0.2) for i in range(10) for s in (-1, 1)], "cypress_avenue"))
    m.add(2, box("gate", 24, 6, 12, (0, -142, 0), "#D8C7A8"), "pavilions")
    m.add(2, gable_roof("gate_roof", 24, 6, 3, (0, -142, 12), "terracotta"))
    for sx in (-1, 1):
        m.add(2, box(f"aviary{sx}", 14, 14, 9, (sx * 30, 95, 3.4), "#E1D2B3"))
        m.add(2, dome(f"aviary_dome{sx}", 6, (sx * 30, 95, 12.4), "#7f8f7a", squash=1.1))
    m.add(2, cylinder("fountain", 6, 1.0, (0, 30, 2.2), "water", verts=16))
    m.add(2, cylinder("fountain_rim", 6.8, 0.8, (0, 30, 2.2), "#D8C7A8", verts=16))
    return m


def palatine_palace():
    """Domitian's palace on the Palatine: Domus Flavia (state rooms, west), Domus Augustana
    (residence, east, stepping down to the Circus), and the garden 'stadium'. Footprint 260 x 300, +Y north."""
    m = Model("palatine-palace")
    M, B, T = "marble", "brick", "terracotta"
    m.add(0, box("platform", 250, 290, 4, color=shade(B, -0.12)), "platform")
    # substructure arcade along the south face, looking over the Circus
    arc = [box(f"sub{i}", 4, 3, 10, (-110 + i * 11, -146, -6), shade(B, -0.06)) for i in range(21)]
    m.add(0, join(arc, "substructures"))

    # ---- Domus Flavia (west half): Aula Regia, basilica and lararium across the north front
    fx = -60
    m.add(1, box("aula_regia", 32, 40, 28, (fx, 112, 4), B), "state_rooms")
    m.add(2, gable_roof("aula_roof", 32, 40, 8, (fx, 112, 32), T), "roofs")
    m.add(1, box("basilica", 22, 30, 22, (fx - 30, 117, 4), shade(B, 0.04)))
    m.add(2, gable_roof("basilica_roof", 22, 30, 6, (fx - 30, 117, 26), T))
    m.add(1, box("lararium", 16, 24, 18, (fx + 27, 120, 4), shade(B, 0.04)))
    m.add(2, gable_roof("lararium_roof", 16, 24, 5, (fx + 27, 120, 22), T))
    m.add(1, columns("north_porch", [(fx - 40 + i * 8, 90) for i in range(11)], 0.8, 10, (0, 0, 4), M))
    # peristyle with the octagonal fountain-maze
    px0, px1, py0, py1 = fx - 38, fx + 38, 18, 86
    for name, w, d, x, y in [("pn", px1 - px0, 10, fx, py1 - 5), ("ps", px1 - px0, 10, fx, py0 + 5), ("pw", 10, py1 - py0, px0 + 5, (py0 + py1) / 2), ("pe", 10, py1 - py0, px1 - 5, (py0 + py1) / 2)]:
        m.add(1, box(name, w, d, 9, (x, y, 4), shade(M, -0.05)))
        m.add(2, box(name + "_roof", w + 1, d + 1, 0.8, (x, y, 13), shade(T, -0.05)))
    m.add(1, columns("peristyle_cols", peristyle(px1 - px0 - 22, py1 - py0 - 22, 10, 7), 0.6, 8, (fx, (py0 + py1) / 2, 4), M))
    m.add(1, box("garden", px1 - px0 - 22, py1 - py0 - 22, 0.4, (fx, (py0 + py1) / 2, 4), "#8FA07A"))
    m.add(1, cylinder("fountain_basin", 14, 0.6, (fx, (py0 + py1) / 2, 4.4), "water", verts=8))
    m.add(1, cylinder("fountain_island", 7, 1.4, (fx, (py0 + py1) / 2, 4.4), M, verts=8))
    # the great triclinium (Cenatio Iovis) with its apse, nymphaea at either side
    m.add(1, box("triclinium", 34, 32, 22, (fx, -6, 4), B))
    m.add(1, cylinder("triclinium_apse", 12, 20, (fx, -22, 4), shade(B, -0.04), verts=20))
    m.add(2, gable_roof("triclinium_roof", 34, 32, 8, (fx, -6, 26), T))
    for s in (-1, 1):
        m.add(1, box(f"nymphaeum{s}", 14, 28, 6, (fx + s * 26, -6, 4), shade(M, -0.04)))
        m.add(1, cylinder(f"nymph_pool{s}", 4.5, 0.6, (fx + s * 26, -6, 10), "water", verts=8))

    # ---- Domus Augustana (east): upper peristyle with island temple, lower sunken court, curved south facade
    ax = 40
    m.add(1, box("upper_court_rooms", 70, 80, 14, (ax, 70, 4), B), "residence")
    m.add(1, box("upper_court", 50, 58, 0.6, (ax, 70, 18), "plaza"))
    m.add(1, box("upper_pool", 34, 40, 0.4, (ax, 70, 18.6), "water"))
    m.add(1, box("island_temple", 10, 14, 7, (ax, 70, 18.6), M))
    m.add(2, gable_roof("island_temple_roof", 10, 14, 3, (ax, 70, 25.6), T))
    m.add(2, box("upper_roof_n", 72, 12, 1, (ax, 104, 18), shade(T, -0.05)))
    m.add(2, box("upper_roof_s", 72, 12, 1, (ax, 36, 18), shade(T, -0.05)))
    # lower peristyle, 10 m below, with its pelta-shaped fountain
    m.add(1, box("lower_rooms", 70, 70, 10, (ax, -40, -6), shade(B, -0.04)))
    m.add(1, box("lower_court", 46, 46, 0.4, (ax, -40, 4), "plaza"))
    m.add(1, cylinder("lower_fountain", 9, 0.6, (ax, -40, 4.4), "water", verts=12))
    m.add(1, columns("lower_cols", peristyle(42, 42, 8, 8), 0.6, 7, (ax, -40, 4.4), M))
    m.add(1, ellipse_ring("south_exedra", 38, 22, 0.82, 18, (ax, -78, -6), shade(M, -0.04), arc=math.pi, start=math.pi))
    m.add(2, box("lower_roof", 72, 14, 1, (ax, -10, 14), shade(T, -0.05)))

    # ---- the garden stadium along the east edge
    sx = 108
    m.add(1, box("stadium_floor", 40, 160, 0.4, (sx, 10, -2), "#8FA07A"), "stadium")
    m.add(1, ellipse_ring("stadium_curve", 20, 20, 0.8, 9, (sx, 90, -2), shade(M, -0.04), arc=math.pi, start=0))
    for s in (-1, 1):
        m.add(1, box(f"stadium_wall{s}", 4, 160, 11, (sx + s * 22, 10, -2), B))
        m.add(1, columns(f"stadium_cols{s}", [(sx + s * 18, -66 + i * 9.5) for i in range(17)], 0.6, 8, (0, 0, -1.6), M))
    m.add(2, box("imperial_box", 16, 10, 14, (sx + 24, 20, -2), M))
    m.add(2, gable_roof("box_roof", 16, 10, 3, (sx + 24, 20, 12), T))
    m.add(1, join([dome(f"hedge{i}", 2, (sx + (i % 2 - 0.5) * 12, -60 + i * 8, -1.6), "#4f6a3f", squash=0.8, segments=8, rings=4) for i in range(18)], "hedges"))
    return m

BUILDERS = {
    "rome/roman-forum-regal": forum_regal,
    "rome/roman-forum-medieval": forum_medieval,
    "rome/temple-of-saturn-ruin": saturn_ruin,
    "rome/curia-hostilia": lambda: (lambda m: (setattr(m, "name", "curia-hostilia"), m)[1])(base.curia_julia("republic")),
    "rome/curia-church": curia_church,
    "rome/temple-of-jupiter-construction": jupiter_construction,
    "rome/temple-of-jupiter-archaic": jupiter_archaic,
    "rome/colosseum-fortress": lambda: colosseum_variant("fortress"),
    "rome/colosseum-ruin": lambda: colosseum_variant("ruin"),
    "rome/circus-maximus-regal": circus_regal,
    "rome/pantheon": lambda: rotunda("pantheon", 22, 22, dome_color="bronze", color="brick", portico=(8, 20), oculus=True),
    "rome/pantheon-agrippa": lambda: small_temple("pantheon-agrippa", 44, 20, 3, 12, 8, 0, color="limestone"),
    "rome/theatre-of-marcellus": lambda: theatre("theatre-of-marcellus", 65, tiers=2, tier_h=11),
    "rome/theatre-of-marcellus-fortress": lambda: theatre("theatre-of-marcellus-fortress", 65, tiers=2, tier_h=11, top="fortress"),
    "rome/theatre-of-marcellus-palazzo": lambda: theatre("theatre-of-marcellus-palazzo", 65, tiers=2, tier_h=11, top="palazzo"),
    "rome/theatre-of-pompey": lambda: theatre("theatre-of-pompey", 75, tiers=3, tier_h=11, scaena_h=36),
    "rome/forum-of-caesar": lambda: imperial_forum("forum-of-caesar", 75, 160, temple_w=30),
    "rome/forum-of-caesar-construction": lambda: imperial_forum("forum-of-caesar-construction", 75, 160, temple_w=30, construction=True),
    "rome/forum-of-augustus": lambda: imperial_forum("forum-of-augustus", 125, 118, temple_w=40, exedrae=True),
    "rome/forum-of-trajan": lambda: imperial_forum("forum-of-trajan", 120, 300, column=True, basilica=True, hemicycle=True),
    "rome/forum-of-trajan-construction": lambda: imperial_forum("forum-of-trajan-construction", 120, 300, construction=True, hemicycle=True),
    "rome/trajans-column": lambda: column_monument("trajans-column", 30, 1.85, 6),
    "rome/palatine-palace": palatine_palace,
    "rome/orti-farnesiani": orti_farnesiani,
    "rome/baths-of-caracalla": lambda: baths("baths-of-caracalla", 337, 328),
    "rome/baths-of-caracalla-ruin": lambda: baths("baths-of-caracalla-ruin", 337, 328, "ruin"),
    "rome/baths-of-diocletian": lambda: baths("baths-of-diocletian", 380, 370),
    "rome/baths-of-diocletian-ruin": lambda: baths("baths-of-diocletian-ruin", 380, 370, "ruin"),
    "rome/baths-of-diocletian-church": lambda: baths("baths-of-diocletian-church", 380, 370, "church"),
    "rome/baths-of-trajan": lambda: baths("baths-of-trajan", 330, 215),
    "rome/baths-of-trajan-construction": lambda: baths("baths-of-trajan-construction", 330, 215, "construction"),
    "rome/mausoleum-of-augustus": lambda: mausoleum_round("mausoleum-of-augustus", 45),
    "rome/mausoleum-of-augustus-fortress": lambda: mausoleum_round("mausoleum-of-augustus-fortress", 45, "fortress"),
    "rome/mausoleum-of-augustus-ruin": lambda: mausoleum_round("mausoleum-of-augustus-ruin", 45, "ruin"),
    "rome/mausoleum-of-hadrian": lambda: hadrianeum("mausoleum-of-hadrian", "mausoleum"),
    "rome/castel-santangelo-late": lambda: hadrianeum("castel-santangelo-late", "late"),
    "rome/castel-santangelo-medieval": lambda: hadrianeum("castel-santangelo-medieval", "medieval"),
    "rome/castel-santangelo-renaissance": lambda: hadrianeum("castel-santangelo-renaissance", "renaissance"),
    "rome/ara-pacis": lambda: altar_enclosure("ara-pacis"),
    "rome/stadium-of-domitian": lambda: stadium("stadium-of-domitian", 275, 106),
    "rome/stadium-medieval": lambda: stadium("stadium-medieval", 275, 106, "medieval"),
    "rome/piazza-navona": lambda: stadium("piazza-navona", 275, 106, "piazza"),
    "rome/temple-of-portunus": lambda: small_temple("temple-of-portunus", 11, 19, 2.5, 7, 4, 0, color="travertine"),
    "rome/temple-of-portunus-church": lambda: small_temple("temple-of-portunus-church", 11, 19, 2.5, 7, 4, 0, church=True, color="travertine"),
    "rome/temple-of-hercules-victor": lambda: round_temple("temple-of-hercules-victor", 7.5, 8),
    "rome/temple-of-hercules-church": lambda: round_temple("temple-of-hercules-church", 7.5, 8, church=True),
    "rome/tiber-island-temple": lambda: small_temple("tiber-island-temple", 24, 44, 3, 9, 6, 0, color="travertine"),
    "rome/tiber-island-church": lambda: christian_basilica("tiber-island-church", 24, 44, nave_h=14, campanile=True, portico=False),
    "rome/pons-fabricius": lambda: bridge("pons-fabricius", 62, 2),
    "rome/pons-aemilius": lambda: bridge("pons-aemilius", 140, 6),
    "rome/pons-aelius": lambda: bridge("pons-aelius", 135, 5, width=11, color="marble"),
    "rome/pons-aurelius": lambda: bridge("pons-aurelius", 108, 4),
    "rome/ponte-sisto": lambda: bridge("ponte-sisto", 108, 4, color="travertine"),
    "rome/porticus-octaviae": lambda: porticus("porticus-octaviae", 130, 120),
    "rome/porticus-metelli": lambda: porticus("porticus-metelli", 130, 120, "metelli"),
    "rome/ghetto": lambda: porticus("ghetto", 130, 120, "ghetto"),
    "rome/basilica-of-maxentius": lambda: basilica_nova("basilica-of-maxentius"),
    "rome/basilica-of-maxentius-ruin": lambda: basilica_nova("basilica-of-maxentius-ruin", ruin=True),
    "rome/arch-of-septimius-severus": lambda: arch3("arch-of-septimius-severus", 23, 21, 11),
    "rome/arch-of-constantine": lambda: arch3("arch-of-constantine", 26, 21, 7),
    "rome/temple-of-venus-and-roma": lambda: double_temple("temple-of-venus-and-roma"),
    "rome/santa-francesca-romana": lambda: double_temple("santa-francesca-romana", church=True),
    "rome/column-of-marcus-aurelius": lambda: column_monument("column-of-marcus-aurelius", 30, 1.9, 10),
    "rome/old-st-peters": lambda: christian_basilica("old-st-peters", 64, 120, nave_h=30, atrium=True, transept=True),
    "rome/old-st-peters-medieval": lambda: christian_basilica("old-st-peters-medieval", 64, 120, nave_h=30, atrium=True, transept=True, campanile=True),
    "rome/new-st-peters-construction": lambda: new_st_peters("new-st-peters-construction"),
    "rome/lateran-basilica": lambda: christian_basilica("lateran-basilica", 56, 100, nave_h=28, transept=True),
    "rome/lateran-medieval": lambda: christian_basilica("lateran-medieval", 56, 100, nave_h=28, transept=True, campanile=True),
    "rome/santa-maria-maggiore": lambda: christian_basilica("santa-maria-maggiore", 36, 80, nave_h=22, campanile=True),
    "rome/santa-maria-in-aracoeli": lambda: christian_basilica("santa-maria-in-aracoeli", 34, 68, nave_h=20, portico=False),
    "rome/torre-delle-milizie": lambda: tower("torre-delle-milizie", 14, 46),
    "rome/santa-maria-in-cosmedin": lambda: christian_basilica("santa-maria-in-cosmedin", 22, 40, nave_h=14, campanile=True),
    "rome/tabularium": lambda: tabularium("tabularium", "tabularium"),
    "rome/palazzo-senatorio-medieval": lambda: tabularium("palazzo-senatorio-medieval", "medieval"),
    "rome/campidoglio": lambda: tabularium("campidoglio", "campidoglio"),
    "rome/palazzo-farnese": lambda: palazzo("palazzo-farnese", 56, 60, 24),
    "rome/villa-farnesina": lambda: villa("villa-farnesina"),
    "rome/santa-maria-in-trastevere-early": lambda: christian_basilica("santa-maria-in-trastevere-early", 30, 50, nave_h=14, portico=False),
    "rome/santa-maria-in-trastevere": lambda: christian_basilica("santa-maria-in-trastevere", 32, 56, nave_h=18, campanile=True),
    "rome/san-clemente-early": lambda: christian_basilica("san-clemente-early", 28, 50, nave_h=14, portico=False),
    "rome/san-clemente": lambda: christian_basilica("san-clemente", 28, 50, nave_h=16, atrium=True, campanile=True, portico=False),
    "rome/pyramid-of-cestius": lambda: pyramid("pyramid-of-cestius", 30, 36),
    "rome/porta-maggiore-aqueduct": lambda: city_gate("porta-maggiore-aqueduct", "aqueduct"),
    "rome/porta-maggiore": lambda: city_gate("porta-maggiore", "gate"),
    "rome/porta-appia": lambda: city_gate("porta-appia", "gate"),
    "rome/castra-praetoria": lambda: castra("castra-praetoria"),
    "rome/emporium": lambda: emporium("emporium"),
    "rome/ludus-magnus": lambda: ludus("ludus-magnus"),
    "rome/ospedale-santo-spirito": lambda: hospital("ospedale-santo-spirito"),
}
