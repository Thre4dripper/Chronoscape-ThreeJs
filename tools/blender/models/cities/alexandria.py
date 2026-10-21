"""Alexandria landmark miniatures: the Pharos, the Serapeum, Ptolemaic palaces and temples, late antique churches, the Mamluk-Ottoman town."""
import math
import bpy
from chronokit import Model, box, cylinder, dome, join, shade, gable_roof, hip_roof, mesh_from, ellipse_ring, obelisk, peristyle
from worldkit import *
from archkit import column, colonnade, entablature, pediment, statue, steps_front, tiled_hip_roof, cyl_y, half_cyl_x, half_cyl_y

# ---------------------------------------------------------------- palette
LIME = "#E4D9C0"        # stuccoed Alexandrian limestone
LIME_D = "#CDBF9F"      # bare limestone, foundations
MARB = "#EFEADF"        # marble and white stucco
RGRAN = "#9C5B4C"       # red Aswan granite
GREYGRAN = "#8D8A86"    # grey granite
TILE_R = "#B0603F"
ROCK = "#B6AA8E"
SAND = "#D9C8A0"
PAVE = "#D3C6A6"
GRASS = "#8E9A62"
PALM = "#6E8A55"
FIRE = "#E89A3C"
MAM = "#D8C7A3"         # Mamluk ashlar
MAM_D = "#BFAE8A"


# ---------------------------------------------------------------- parts
def portico(name, length, depth, h, col_r=0.55, spacing=4.0, order="doric", color=LIME, roof=TILE_R, doors=False, wall_h=None):
    """A one-aisle stoa along X centred on the origin: back wall at +Y, columns along the open -Y side, a lean-to tiled roof."""
    parts = [box(name + "_floor", length, depth, 0.4, (0, 0, 0), shade(color, -0.08))]
    wh = wall_h or h + 1.4
    parts.append(box(name + "_wall", length, 0.9, wh + 0.4, (0, depth / 2 - 0.45, 0), shade(color, -0.03)))
    cy = -depth / 2 + col_r * 1.4
    n = max(2, int((length - 3 * col_r) / spacing) + 1)
    pts = [(-length / 2 + col_r * 1.5 + i * (length - 3 * col_r) / (n - 1), cy) for i in range(n)]
    parts.append(colonnade(name + "_cols", pts, 0.4, h, col_r, order, color))
    parts.append(box(name + "_arch", length, col_r * 2.6, h * 0.13, (0, cy, 0.4 + h), shade(color, 0.03)))
    z1, z2 = 0.4 + h * 1.13, 0.4 + wh + 0.2
    y1, y2 = -depth / 2 - 0.4, depth / 2 + 0.1
    t = 0.35
    v = [(-length / 2 - 0.3, y1, z1), (length / 2 + 0.3, y1, z1), (length / 2 + 0.3, y2, z2), (-length / 2 - 0.3, y2, z2)]
    v += [(x, y, z + t) for x, y, z in v]
    f = [(0, 1, 2, 3), (7, 6, 5, 4), (0, 4, 5, 1), (1, 5, 6, 2), (2, 6, 7, 3), (3, 7, 4, 0)]
    parts.append(mesh_from(name + "_roof", v, f, (0, 0, 0), roof))
    if doors:
        nd = max(1, n // 2)
        for i in range(nd):
            x = -length / 2 + (i + 0.5) * length / nd
            parts.append(box(f"{name}_door{i}", min(2.2, length / nd * 0.4), 0.3, h * 0.6, (x, depth / 2 - 1.0, 0.4), DARK))
    return join(parts, name)


def court(name, w, d, depth, h, col_r=0.55, spacing=4.0, order="doric", color=LIME, roof=TILE_R, doors=False, skip=()):
    """Four porticoes facing inward round a w x d court centred on the origin. skip: sides to leave out ('S', 'N', 'E', 'W')."""
    out = []
    if "S" not in skip:
        out.append(move(rot(portico(name + "_s", w, depth, h, col_r, spacing, order, color, roof, doors), 180), 0, -d / 2 + depth / 2, 0))
    if "N" not in skip:
        out.append(move(portico(name + "_n", w, depth, h, col_r, spacing, order, color, roof, doors), 0, d / 2 - depth / 2, 0))
    if "W" not in skip:
        out.append(move(rot(portico(name + "_w", d - 2 * depth, depth, h, col_r, spacing, order, color, roof, doors), 90), -w / 2 + depth / 2, 0, 0))
    if "E" not in skip:
        out.append(move(rot(portico(name + "_e", d - 2 * depth, depth, h, col_r, spacing, order, color, roof, doors), -90), w / 2 - depth / 2, 0, 0))
    return join(out, name)


def temple(name, w, d, podium, col_h, nf, ns, order="corinthian", color=MARB, roof=TILE_R, col_r=None, peripteral=True, statues=True, steps=True, stair_w=None):
    """A classical temple facing -Y, centred on the origin. Returns (base, columns+cella, entablature+roof)."""
    col_r = col_r or min(w / (nf * 4.2), 1.2)
    m = col_r * 1.7
    z = podium
    base = [box(name + "_pod", w, d, podium, (0, 0, 0), shade(color, -0.1)),
            box(name + "_podc", w + 0.6, d + 0.6, 0.45, (0, 0, podium - 0.45), shade(color, -0.04))]
    if steps:
        base.append(steps_front(name + "_steps", stair_w or w * 0.8, podium, max(3, int(podium / 0.32)), -d / 2, 0, shade(color, -0.06)))
    if peripteral:
        pts = peristyle(w - 2 * m, d - 2 * m, nf, ns)
        cw, cd, cy = w - 4.6 * m, d - 6.0 * m, m * 0.8
    else:
        x0 = -w / 2 + m
        pts = [(x0 + i * (w - 2 * m) / (nf - 1), -d / 2 + m) for i in range(nf)] + [(x0 + i * (w - 2 * m) / (nf - 1), -d / 2 + m + col_r * 5) for i in (0, nf - 1)]
        cw, cd, cy = w - 1.2, d * 0.62, d / 2 - d * 0.31 - 0.6
    body = [colonnade(name + "_cols", pts, z, col_h, col_r, order, color),
            box(name + "_cella", cw, cd, col_h, (0, cy, z), shade(color, -0.04)),
            box(name + "_door", cw * 0.2, 0.4, col_h * 0.55, (0, cy - cd / 2 - 0.15, z), DARK)]
    eh = col_h * 0.2
    top = [entablature(name + "_ent", -w / 2 + m * 0.4, w / 2 - m * 0.4, -d / 2 + m * 0.4, d / 2 - m * 0.4, z + col_h, eh, color, dentils=w < 30),
           pediment(name + "_ped", w - m * 0.8, d - m * 0.8, z + col_h + eh, w * 0.16, -d / 2 + m * 0.4, color, roof, ridges=True, statues=statues)]
    return join(base, name + "_base"), join(body, name + "_body"), join(top, name + "_top")


def place_all(parts, x=0, y=0, z=0, deg=0):
    out = []
    for p in parts:
        if p is None:
            continue
        if deg:
            p = rot(p, deg)
        out.append(move(p, x, y, z))
    return out


def red_obelisk(name, h, loc=(0, 0, 0), color=RGRAN, base=True):
    x, y, z = loc
    b = h * 0.1
    parts = []
    if base:
        parts.append(box(name + "_ped", b * 1.9, b * 1.9, h * 0.08, (x, y, z), LIME_D))
        for k in range(4):
            a = math.pi / 4 + k * math.pi / 2
            parts.append(dome(f"{name}_crab{k}", b * 0.32, (x + math.cos(a) * b * 0.55, y + math.sin(a) * b * 0.55, z + h * 0.08), BRONZE, squash=0.6, segments=8, rings=4))
        z += h * 0.08 + b * 0.18
    parts.append(obelisk(name + "_sh", b, h, (x, y, z), color))
    parts.append(cylinder(name + "_pyr", b * 0.7 / math.sqrt(2) * 0.98, b * 1.2, (x, y, z + h), GILT, verts=4, r_top=0))
    parts[-1].rotation_euler[2] = math.pi / 4
    return join(parts, name)


def fallen_obelisk(name, h, loc=(0, 0, 0), deg=20, color=RGRAN):
    b = h * 0.1
    o = obelisk(name, b, h, (0, 0, 0), color)
    o.rotation_euler = (math.radians(88), 0, 0)
    bpy.ops.object.select_all(action="DESELECT")
    o.select_set(True)
    bpy.context.view_layer.objects.active = o
    bpy.ops.object.transform_apply(rotation=True)
    o = rot(o, deg)
    return move(o, loc[0], loc[1], loc[2] + b * 0.25)


def palm(name, loc, r=2.4):
    return tree(name, r, loc, PALM, TIMBER, kind="palm")


def palms(name, pts, r=2.4):
    return join([palm(f"{name}{i}", (x, y, z), r) for i, (x, y, z) in enumerate(pts)], name)


def apse_x(name, r, h, loc, color=LIME, roof=TILE_R, sign=1):
    """A half-round apse bulging toward +X (sign=1) or -X, with a half-dome roof."""
    x, y, z = loc
    n = 10
    pts = [(sign * r * math.cos(-math.pi / 2 + math.pi * i / n), r * math.sin(-math.pi / 2 + math.pi * i / n)) for i in range(n + 1)]
    if sign < 0:
        pts = pts[::-1]
    wall = prism(name + "_w", pts, h, (x, y, z), color)
    cap = dome(name + "_c", r * 1.02, (x, y, z + h), roof, squash=0.55, segments=16, rings=6)
    bpy.ops.object.select_all(action="DESELECT")
    import bmesh
    bm = bmesh.new()
    bm.from_mesh(cap.data)
    bmesh.ops.delete(bm, geom=[v for v in bm.verts if (v.co.x - x) * sign < -1e-3], context="VERTS")
    bm.to_mesh(cap.data)
    bm.free()
    return join([wall, cap], name)


def basilica(name, length, width, h, color=LIME, roof=TILE_R, aisles=True, apse=True, narthex=True):
    """An early Christian basilica along X: entrance at -X, apse at +X. Nave clerestory, lower aisles, gabled roofs."""
    parts = []
    nave_w = width * (0.48 if aisles else 1.0)
    parts.append(box(name + "_nave", length, nave_w, h, (0, 0, 0), color))
    parts.append(rot(gable_roof(name + "_nroof", nave_w, length, nave_w * 0.32, (0, 0, h), roof, 0.5), 90))
    if aisles:
        aw = (width - nave_w) / 2
        for s in (-1, 1):
            yy = s * (nave_w / 2 + aw / 2)
            parts.append(box(f"{name}_aisle{s}", length, aw, h * 0.58, (0, yy, 0), shade(color, -0.04)))
            v = [(-length / 2 - 0.3, yy - s * aw / 2, h * 0.58 + aw * 0.3), (length / 2 + 0.3, yy - s * aw / 2, h * 0.58 + aw * 0.3),
                 (length / 2 + 0.3, yy + s * (aw / 2 + 0.4), h * 0.58), (-length / 2 - 0.3, yy + s * (aw / 2 + 0.4), h * 0.58)]
            v += [(a, b, c + 0.3) for a, b, c in v]
            parts.append(mesh_from(f"{name}_aroof{s}", v, [(0, 1, 2, 3), (7, 6, 5, 4), (0, 4, 5, 1), (1, 5, 6, 2), (2, 6, 7, 3), (3, 7, 4, 0)], (0, 0, 0), roof))
            for k in range(max(3, int(length / 5))):
                xx = -length / 2 + (k + 0.5) * length / max(3, int(length / 5))
                parts.append(box(f"{name}_cw{s}_{k}", 1.1, 0.3, h * 0.2, (xx, s * (nave_w / 2 + 0.05), h * 0.68), DARK))
                parts.append(arch_panel(f"{name}_aw{s}_{k}", 1.0, h * 0.28, (xx, s * (width / 2 + 0.05), h * 0.18), "S" if s < 0 else "N", DARK, pointed=False))
    if apse:
        parts.append(apse_x(name + "_apse", nave_w * 0.42, h * 0.8, (length / 2, 0, 0), color, roof))
    if narthex:
        parts.append(box(name + "_narthex", 5, width, h * 0.5, (-length / 2 - 2.5, 0, 0), shade(color, -0.05)))
        parts.append(rot(arcade(name + "_narc", width * 0.8, h * 0.36, 5, (0, 0, 0), "S", DARK, pointed=False), -90))
        parts[-1] = move(parts[-1], -length / 2 - 5.05, 0, 0)
        parts.append(box(name + "_nroof", 5.6, width + 0.6, 0.5, (-length / 2 - 2.5, 0, h * 0.5), roof))
    parts.append(box(name + "_cross", 0.3, 0.3, 2.2, (-length / 2 + 0.5, 0, h + nave_w * 0.32), BRONZE))
    parts.append(box(name + "_crossb", 0.3, 1.3, 0.3, (-length / 2 + 0.5, 0, h + nave_w * 0.32 + 1.4), BRONZE))
    return join(parts, name)


def mamluk_minaret(name, loc, h=28, color=MAM, trim=MAM_D):
    """A Mamluk minaret: square shaft, octagonal middle, round top storey with a bulb on columns."""
    x, y, z = loc
    s = h * 0.13
    h1, h2, h3 = h * 0.4, h * 0.28, h * 0.16
    parts = [box(name + "_sq", s, s, h1, (x, y, z), color),
             box(name + "_b1", s * 1.25, s * 1.25, 0.6, (x, y, z + h1), trim)]
    o = cylinder(name + "_oct", s * 0.48, h2, (x, y, z + h1 + 0.6), color, verts=8)
    o.rotation_euler[2] = math.pi / 8
    parts.append(o)
    parts.append(cylinder(name + "_b2", s * 0.68, 0.5, (x, y, z + h1 + 0.6 + h2), trim, verts=16))
    z3 = z + h1 + 1.1 + h2
    for i in range(6):
        a = math.tau * i / 6
        parts.append(cylinder(f"{name}_p{i}", 0.14, h3, (x + math.cos(a) * s * 0.3, y + math.sin(a) * s * 0.3, z3), trim, verts=6))
    parts.append(cylinder(name + "_core", s * 0.18, h3, (x, y, z3), color, verts=8))
    parts.append(onion_dome(name + "_bulb", s * 0.36, (x, y, z3 + h3), color, bulb=1.15, height=1.5, drum=0.2, finial_color=BRONZE))
    for k in range(4):
        parts.append(arch_panel(f"{name}_w{k}", s * 0.22, s * 0.6, (x + [0, s / 2 + 0.05, 0, -s / 2 - 0.05][k], y + [-s / 2 - 0.05, 0, s / 2 + 0.05, 0][k], z + h1 * 0.55), "SENW"[k], DARK))
    return join(parts, name)


def rubble(name, n, w, d, seed=1, color=LIME_D, size=2.0):
    """Scattered fallen blocks and column drums over a w x d area."""
    import random
    r = random.Random(seed)
    parts = []
    for i in range(n):
        x, y = r.uniform(-w / 2, w / 2), r.uniform(-d / 2, d / 2)
        if r.random() < 0.4:
            c = cyl_y(f"{name}_dr{i}", size * 0.4, size * r.uniform(0.8, 1.6), (x, y, size * 0.4), shade(color, r.uniform(-0.05, 0.08)), verts=10)
            parts.append(c)
        else:
            parts.append(box(f"{name}_bl{i}", size * r.uniform(0.6, 1.5), size * r.uniform(0.5, 1.2), size * r.uniform(0.3, 0.8), (x, y, 0), shade(color, r.uniform(-0.08, 0.05)), rot_z=r.uniform(0, 3)))
    return join(parts, name)


def windows_ring(name, w, d, z, n, ww, wh, color=DARK):
    """Dark window slots on all four faces of a w x d block at height z."""
    out = []
    for k in range(n):
        t = -0.5 + (k + 0.5) / n
        out += [box(f"{name}_s{k}", ww, 0.3, wh, (t * w * 0.8, -d / 2 - 0.05, z), color), box(f"{name}_n{k}", ww, 0.3, wh, (t * w * 0.8, d / 2 + 0.05, z), color),
                box(f"{name}_w{k}", 0.3, ww, wh, (-w / 2 - 0.05, t * d * 0.8, z), color), box(f"{name}_e{k}", 0.3, ww, wh, (w / 2 + 0.05, t * d * 0.8, z), color)]
    return join(out, name)


# ---------------------------------------------------------------- the Pharos (hero)
def pharos():
    m = Model("pharos")
    # the rock and the walled terrace (Thiersch: a court with a parapet and corner towers round the tower)
    rock = [(-64, -40), (-50, -60), (-10, -64), (40, -60), (62, -36), (64, 10), (52, 50), (20, 64), (-30, 62), (-58, 40)]
    m.add(0, prism("rock", rock, 2.0, (0, 0, 0), ROCK), "terrace")
    m.add(0, box("terrace", 96, 96, 6.0, (0, 0, 2.0), LIME_D))
    m.add(0, box("terrace_c", 97.5, 97.5, 0.7, (0, 0, 7.3), LIME))
    m.add(0, wall_run("parapet", [(-47, -47), (47, -47), (47, 47), (-47, 47), (-47, -47)], 2.2, 1.2, (0, 0, 8.0), LIME, towers=True, tower_r=3.2, tower_every=47, merlon="box"))
    m.add(0, steps_front("ramp", 14, 8.0, 18, -48, 0, LIME_D, tread=0.9))
    m.add(0, box("gate", 16, 4, 6, (0, -47, 8), LIME))
    m.add(0, box("gate_d", 5, 0.4, 4.2, (0, -49.1, 8), DARK))
    # a colonnade round the inside of the court
    m.add(0, move(court("court", 88, 88, 6.0, 4.5, 0.32, 3.6, "doric", LIME, TILE_R), 0, 0, 8.0))
    # tier 1: square shaft, slightly tapering, with windows and a corner cornice
    z0 = 8.0
    m.add(1, frustum("shaft", 30.5, 30.5, 27.5, 27.5, 55.0, (0, 0, z0), MARB), "tiers")
    for row in range(7):
        zz = z0 + 6 + row * 7.0
        wv = 30.5 - (27.5 - 30.5) * -1 * (zz - z0) / 55.0
        half = (30.5 - 3.0 * (zz - z0) / 55.0) / 2
        for k in range(4):
            t = -0.32 + k * 0.213
            m.add(1, box(f"w1s{row}_{k}", 0.9, 0.4, 1.8, (t * half * 2, -half - 0.05, zz), DARK))
            m.add(1, box(f"w1n{row}_{k}", 0.9, 0.4, 1.8, (t * half * 2, half + 0.05, zz), DARK))
            m.add(1, box(f"w1w{row}_{k}", 0.4, 0.9, 1.8, (-half - 0.05, t * half * 2, zz), DARK))
            m.add(1, box(f"w1e{row}_{k}", 0.4, 0.9, 1.8, (half + 0.05, t * half * 2, zz), DARK))
    m.add(1, box("door1", 3.0, 0.5, 5.0, (0, -15.3, z0), DARK))
    z1 = z0 + 55.0
    m.add(1, entablature("cor1", -14.5, 14.5, -14.5, 14.5, z1, 2.4, MARB, dentils=True))
    m.add(1, box("plat1", 29.8, 29.8, 0.5, (0, 0, z1 + 2.4), LIME))
    m.add(1, merlons("mer1", 29, 29, z1 + 2.9, 0.7, 1.1, MARB))
    for i, (sx, sy) in enumerate([(-1, -1), (1, -1), (1, 1), (-1, 1)]):
        m.add(1, cylinder(f"triton_b{i}", 1.4, 1.2, (sx * 12.8, sy * 12.8, z1 + 2.9), MARB, verts=10))
        m.add(1, statue(f"triton{i}", sx * 12.8, sy * 12.8, z1 + 4.1, 4.2, BRONZE))
        m.add(1, cylinder(f"conch{i}", 0.35, 1.6, (sx * 12.8 + sx * 0.6, sy * 12.8, z1 + 7.0), BRONZE, verts=6, r_top=0.6))
    # tier 2: octagon
    z2 = z1 + 2.9
    oc = cylinder("oct", 9.6, 27.0, (0, 0, z2), MARB, verts=8, r_top=8.9)
    oc.rotation_euler[2] = math.pi / 8
    m.add(2, oc, "lantern")
    for row in range(3):
        for k in range(8):
            a = math.tau * k / 8
            rr = 9.6 - 0.7 * (5 + row * 8) / 27.0
            w = box(f"w2_{row}_{k}", 0.4, 1.0, 2.0, (math.cos(a) * rr * 0.93, math.sin(a) * rr * 0.93, z2 + 5 + row * 8), DARK)
            w.rotation_euler[2] = a
            m.add(2, w)
    z3 = z2 + 27.0
    oc2 = cylinder("oct_c", 10.0, 1.6, (0, 0, z3), LIME, verts=8, r_top=10.4)
    oc2.rotation_euler[2] = math.pi / 8
    m.add(2, oc2)
    m.add(2, cylinder("oct_p", 9.4, 1.0, (0, 0, z3 + 1.6), MARB, verts=16))
    # tier 3: round lantern of eight columns round the fire, a conical cap and the statue
    z4 = z3 + 2.6
    m.add(3, cylinder("lan_floor", 6.0, 0.6, (0, 0, z4), LIME, verts=24), "lantern-top")
    cols = [(math.cos(math.tau * i / 8) * 5.0, math.sin(math.tau * i / 8) * 5.0) for i in range(8)]
    m.add(3, colonnade("lan_cols", cols, z4 + 0.6, 7.5, 0.42, "corinthian", MARB))
    m.add(3, cylinder("fire_core", 2.6, 5.5, (0, 0, z4 + 0.6), FIRE, verts=12, r_top=1.4))
    m.add(3, cylinder("lan_ent", 5.9, 1.2, (0, 0, z4 + 8.1), MARB, verts=24))
    m.add(3, cylinder("lan_cone", 5.6, 4.2, (0, 0, z4 + 9.3), BRONZE, verts=24, r_top=1.2))
    m.add(3, cylinder("st_base", 1.4, 1.5, (0, 0, z4 + 13.5), MARB, verts=10))
    m.add(3, statue("zeus", 0, 0, z4 + 15.0, 7.5, BRONZE))
    m.add(3, cylinder("trident", 0.12, 7.0, (1.2, 0, z4 + 15.0), BRONZE, verts=6))
    return m


def qaitbay():
    m = Model("qaitbay")
    rock = [(-64, -40), (-50, -60), (-10, -64), (40, -60), (62, -36), (64, 10), (52, 50), (20, 64), (-30, 62), (-58, 40)]
    m.add(0, prism("rock", rock, 2.0, (0, 0, 0), ROCK), "walls")
    m.add(0, box("yard", 112, 112, 0.6, (0, 0, 2.0), SAND))
    m.add(0, wall_run("curtain", [(-55, -55), (55, -55), (55, 55), (-55, 55), (-55, -55)], 9.0, 2.6, (0, 0, 2.0), MAM, towers=True, tower_r=4.2, tower_every=27, merlon="box"))
    m.add(0, gatehouse("gate", 16, 10, 11, (0, -55, 2.0), "S", MAM, MAM_D, style="roman"))
    m.add(0, box("barracks_w", 8, 90, 5, (-48, 0, 2.0), MAM_D))
    m.add(0, box("barracks_e", 8, 90, 5, (48, 0, 2.0), MAM_D))
    m.add(0, arcade("barr_w_arc", 86, 3.6, 14, (-43.9, 0, 2.0), "E", DARK, pointed=True))
    m.add(0, arcade("barr_e_arc", 86, 3.6, 14, (43.9, 0, 2.0), "W", DARK, pointed=True))
    # the keep on the old lighthouse base
    z = 2.0
    m.add(1, box("keep", 32, 32, 17, (0, 10, z), MAM), "keep")
    m.add(1, box("keep_band", 32.6, 32.6, 0.6, (0, 10, z + 11), MAM_D))
    for i, (sx, sy) in enumerate([(-1, -1), (1, -1), (1, 1), (-1, 1)]):
        m.add(1, cylinder(f"ktower{i}", 4.8, 20.5, (sx * 16, 10 + sy * 16, z), shade(MAM, -0.03), verts=16))
        m.add(1, cylinder(f"ktcap{i}", 5.1, 0.6, (sx * 16, 10 + sy * 16, z + 20.5), MAM_D, verts=16))
        for k in range(8):
            a = math.tau * k / 8
            m.add(1, box(f"ktmer{i}_{k}", 1.0, 0.8, 1.2, (sx * 16 + math.cos(a) * 4.6, 10 + sy * 16 + math.sin(a) * 4.6, z + 21.1), MAM, rot_z=a))
    m.add(1, move(merlons("kmer", 32, 32, z + 17, 0.9, 0.9, MAM, "stepped"), 0, 10, 0))
    for row, zz in enumerate((z + 4, z + 12.5)):
        m.add(1, arcade(f"kw_s{row}", 22, 3.2, 5, (0, 10 - 16.05, zz), "S", DARK))
        m.add(1, arcade(f"kw_n{row}", 22, 3.2, 5, (0, 10 + 16.05, zz), "N", DARK))
        m.add(1, arcade(f"kw_w{row}", 22, 3.2, 5, (-16.05, 10, zz), "W", DARK))
        m.add(1, arcade(f"kw_e{row}", 22, 3.2, 5, (16.05, 10, zz), "E", DARK))
    m.add(1, iwan("kdoor", 8, 11, 2.0, (0, 10 - 16.5, z), "S", MAM, MAM_D))
    m.add(2, mamluk_minaret("minaret", (0, 10, z + 17), 13, MAM, MAM_D), "minaret")
    m.add(2, shallow_dome("kdome", 4.5, (8, 16, z + 17), MAM, rise=0.7, drum=1.0))
    for i, x in enumerate((-30, -10, 10, 30)):
        m.add(2, cylinder(f"cannon{i}", 0.35, 3.0, (x, -53, 11.5), BRONZE, verts=8))
    return m


# ---------------------------------------------------------------- the Heptastadion
def heptastadion():
    m = Model("heptastadion")
    L, W = 1200.0, 22.0
    gaps = [(-260.0, 26.0), (230.0, 26.0)]    # bridged openings (centre, span)
    edges = [-L / 2] + [g for c, s in gaps for g in (c - s / 2, c + s / 2)] + [L / 2]
    for i in range(0, len(edges), 2):
        a, b = edges[i], edges[i + 1]
        mid, ln = (a + b) / 2, b - a
        m.add(0, frustum(f"mole{i}", W + 4, ln, W, ln, 2.6, (0, mid, 0), LIME_D), "causeway")
        m.add(0, box(f"road{i}", W - 3, ln, 0.3, (0, mid, 2.6), PAVE))
        for s in (-1, 1):
            m.add(0, box(f"par{i}{s}", 0.8, ln, 1.1, (s * (W / 2 - 0.4), mid, 2.6), LIME))
        m.add(0, box(f"conduit{i}", 1.6, ln, 1.2, (W / 2 - 2.4, mid, 2.6), shade(LIME, -0.06)))
        for k in range(int(ln / 24)):
            yy = a + (k + 0.5) * ln / int(ln / 24)
            for s2 in (-1, 1):
                m.add(0, box(f"course{i}_{k}{s2}", 0.5, 0.6, 2.2, (s2 * (W / 2 + 1.7), yy, 0.2), shade(LIME_D, -0.08)))
        n = int(ln / 30)
        for k in range(n):
            yy = a + (k + 0.5) * ln / n
            m.add(0, box(f"bol{i}_{k}", 0.6, 0.6, 0.9, (-W / 2 - 1.2, yy, 1.2), DARK))
    for j, (c, s) in enumerate(gaps):
        m.add(1, box(f"deck{j}", W, s + 6, 1.4, (0, c, 3.2), LIME), "bridges")
        for sy in (-1, 1):
            m.add(1, box(f"pier{j}{sy}", W + 2, 4, 4.6, (0, c + sy * (s / 2 - 1), 0), LIME_D))
        m.add(1, box(f"pierm{j}", W + 2, 3, 3.2, (0, c, 0), LIME_D))
        for sx in (-1, 1):
            for sy in (-1, 1):
                m.add(1, arch_panel(f"bay{j}{sx}{sy}", 5.0, 3.6, (sx * (W / 2 + 1.05), c + sy * (s / 4 + 0.8), 0), "E" if sx > 0 else "W", DARK, pointed=False, depth=0.5))
            m.add(1, box(f"bpar{j}{sx}", 0.8, s + 6, 1.2, (sx * (W / 2 - 0.4), c, 4.6), LIME))
        for sy in (-1, 1):
            m.add(2, box(f"gtower{j}{sy}", 7, 7, 9, (-W / 2 - 2.5, c + sy * (s / 2 + 5), 0), LIME), "towers")
            m.add(2, move(merlons(f"gtm{j}{sy}", 7, 7, 9, 0.7, 0.8, LIME), -W / 2 - 2.5, c + sy * (s / 2 + 5), 0))
    return m


# ---------------------------------------------------------------- palaces on Lochias
def royal_palaces(variant="ptol"):
    m = Model("royal-palaces")
    W, D = 260, 300
    m.add(0, box("terrace", W, D, 2.5, (0, 0, 0), LIME_D), "terraces")
    m.add(0, box("quay", 12, D, 1.4, (-W / 2 + 6, 0, 0), shade(LIME_D, -0.1)))
    if variant == "ruin":
        m.add(0, box("garden", 200, 230, 0.3, (10, 0, 2.5), GRASS))
        m.add(1, move(rubble("rub1", 160, 180, 220, 7, LIME_D, 2.6), 10, 0, 2.5), "ruins")
        for i, (x, y, l, d, h) in enumerate([(-30, -60, 90, 1.5, 4.5), (-75, -20, 1.5, 70, 3.0), (40, 40, 60, 1.5, 6.0), (70, 10, 1.5, 60, 3.5), (0, 110, 70, 1.5, 2.5), (-20, 60, 1.5, 40, 5.0)]):
            m.add(1, box(f"wall{i}", l, d, h, (x, y, 2.5), shade(LIME, -0.08)))
        stand = [(-60, -100), (-48, -100), (-36, -100), (30, 70), (42, 70), (-90, 40), (-90, 52)]
        m.add(1, colonnade("stand", stand, 2.5, 8.0, 0.6, "ionic", MARB))
        m.add(1, box("archfrag", 14, 1.4, 1.2, (-48, -100, 10.5), MARB))
        m.add(2, palms("palm", [(x, y, 2.5) for x, y in [(-60, 0), (20, -40), (80, -90), (60, 100), (-30, 100), (100, 30), (-100, -60), (0, 20)]], 3.0), "trees")
        m.add(2, cylinder("well", 2, 1.2, (20, 0, 2.5), LIME, verts=12))
        return m
    m.add(0, box("garden", 120, 110, 0.3, (40, -70, 2.5), GRASS))
    m.add(0, box("canal", 4, 80, 0.4, (40, -70, 2.5), WATER))
    # main peristyle palace
    z = 2.5
    m.add(1, move(court("peri", 110, 90, 9, 7.5, 0.5, 4.0, "ionic", MARB, TILE_R, doors=True), -45, 70, z), "palaces")
    m.add(1, box("peri_pave", 92, 72, 0.2, (-45, 70, z), PAVE))
    m.add(1, box("pool", 20, 10, 0.4, (-45, 70, z), WATER))
    # audience hall on the north side of the court, with a pediment
    hall = temple("hall", 44, 34, 3.5, 11, 6, 0, "corinthian", MARB, TILE_R, col_r=0.85, peripteral=False, statues=True)
    for p in place_all(hall, -45, 135, z):
        m.add(2, p, "halls")
    # second palace east: a two-storey block with loggia
    m.add(1, box("pal2", 70, 46, 9, (70, 80, z), LIME))
    m.add(1, box("pal2_up", 70, 46, 6, (70, 80, z + 9), shade(LIME, 0.04)))
    m.add(1, arcade("pal2_arc", 64, 6, 12, (70, 80 - 23.05, z), "S", DARK, pointed=False))
    m.add(1, move(windows_ring("pal2_w", 70, 46, z + 11, 9, 1.2, 2.4), 70, 80, 0))
    m.add(1, box("pal2_balc", 66, 4, 0.5, (70, 80 - 25, z + 8.6), MARB))
    m.add(2, tiled_hip_roof("pal2_roof", 70, 46, 7, (70, 80, z + 15), TILE_R))
    m.add(1, colonnade("pal2_log", [(70 - 30 + i * 6, 80 - 26) for i in range(11)], z + 9, 5.5, 0.4, "ionic", MARB))
    # a round pavilion (tholos) in the garden and a small temple of Isis by the point
    m.add(2, cylinder("tholos_b", 8, 1.2, (40, -60, z), MARB, verts=24))
    m.add(2, colonnade("tholos_c", [(40 + 6.5 * math.cos(a), -60 + 6.5 * math.sin(a)) for a in [math.tau * i / 10 for i in range(10)]], z + 1.2, 6, 0.4, "ionic", MARB))
    m.add(2, dome("tholos_d", 7.2, (40, -60, z + 7.6), TILE_R, squash=0.55, segments=20, rings=6))
    isis = temple("isis", 16, 24, 2.5, 7, 4, 0, "ionic", MARB, TILE_R, col_r=0.5, peripteral=False, statues=False)
    for p in place_all(isis, 0, 0, 0, 180):
        m.add(2, move(p, 70, 135, z))
    # the sea palace: a long colonnaded wing on the west quay, and a banqueting hall south of the garden
    m.add(1, move(rot(portico("quay_stoa", 150, 10, 6.5, 0.42, 4.2, "ionic", MARB, TILE_R, doors=True), 90), -W / 2 + 19, -40, z))
    m.add(1, box("banquet", 56, 30, 10, (-40, -105, z), LIME))
    m.add(1, arcade("banquet_arc", 50, 7, 9, (-40, -105 - 15.05, z), "S", DARK, pointed=False))
    m.add(2, tiled_hip_roof("banquet_roof", 56, 30, 7, (-40, -105, z + 10), TILE_R))
    m.add(1, colonnade("banquet_cols", [(-40 - 25 + i * 5, -125) for i in range(11)], z, 8.0, 0.45, "corinthian", MARB))
    m.add(1, box("banquet_porch", 56, 6, 0.9, (-40, -122, z + 8.0), MARB))
    m.add(1, box("banquet_terr", 64, 12, 0.4, (-40, -126, z), PAVE))
    # sphinxes along the quay
    for i in range(8):
        y = -120 + i * 34
        m.add(1, box(f"sph{i}", 2.0, 5.0, 1.6, (-W / 2 + 9, y, 1.4), GREYGRAN))
        m.add(1, box(f"sphh{i}", 1.6, 1.6, 1.6, (-W / 2 + 9, y - 2.4, 3.0), GREYGRAN))
    m.add(2, palms("palm", [(x, y, z) for x, y in [(0, -30), (80, -30), (0, -110), (80, -110), (100, -70), (-20, -70), (-100, -40), (-100, -100), (110, 20), (-110, 10)]], 3.0), "trees")
    return m


# ---------------------------------------------------------------- Museum and Library
def museum():
    m = Model("museum")
    m.add(0, box("plinth", 170, 130, 1.2, (0, 0, 0), LIME_D), "court")
    m.add(0, box("garden", 96, 60, 0.2, (0, -12, 1.2), GRASS))
    m.add(0, move(court("peripatos", 120, 84, 7.0, 6.0, 0.42, 3.4, "ionic", MARB, TILE_R, doors=False, skip=("N",)), 0, -12, 1.2))
    for i in range(6):
        for j in range(2):
            m.add(0, tree(f"tr{i}{j}", 2.6, (-14 + i * 11, -24 + j * 22, 1.4), PALM if (i + j) % 2 else "#6F8A5C", kind="palm" if (i + j) % 2 else "round"))
    # exedra with curved seats on the court's west side
    m.add(1, ellipse_ring("exedra", 13, 13, 0.72, 4.0, (-36, -12, 1.2), LIME, n=24, arc=math.pi, start=math.pi / 2), "halls")
    m.add(1, ellipse_ring("exedra_seat", 9.4, 9.4, 0.8, 1.0, (-36, -12, 1.2), MARB, n=20, arc=math.pi, start=math.pi / 2))
    # the great hall (oikos) where the scholars dined, closing the north side
    hall = temple("oikos", 52, 30, 2.0, 10, 6, 0, "corinthian", MARB, TILE_R, col_r=0.75, peripteral=False, statues=True)
    for p in place_all(hall, 0, 46, 1.2):
        m.add(1, p)
    # book stores: two long wings with niche windows east and west of the hall
    for s in (-1, 1):
        m.add(1, box(f"books{s}", 36, 22, 9, (s * 62, 46, 1.2), LIME))
        m.add(1, move(windows_ring(f"booksw{s}", 36, 22, 4.5, 5, 1.0, 2.4), s * 62, 46, 1.2))
        m.add(2, tiled_hip_roof(f"books_roof{s}", 36, 22, 4.5, (s * 62, 46, 10.2), TILE_R), "roofs")
    # entrance propylon on the south
    m.add(2, box("prop", 22, 8, 8, (0, -58, 1.2), MARB))
    m.add(2, box("prop_d", 6, 0.4, 5.5, (0, -62.1, 1.2), DARK))
    m.add(2, pediment("prop_ped", 22, 8, 9.2, 3.2, -62, MARB, TILE_R, ridges=False, statues=False))
    m.add(2, statue("muse1", -7, -63.5, 1.2, 3.0, MARB))
    m.add(2, statue("muse2", 7, -63.5, 1.2, 3.0, MARB))
    return m


# ---------------------------------------------------------------- the Sema
def sema():
    m = Model("sema")
    m.add(0, box("ground", 110, 110, 0.5, (0, 0, 0), PAVE), "precinct")
    m.add(0, wall_run("temenos", [(-54, -54), (54, -54), (54, 54), (-54, 54), (-54, -54)], 5.0, 1.4, (0, 0, 0.5), LIME, towers=False, merlon=None))
    m.add(0, box("propylon", 18, 7, 8, (0, -54, 0.5), MARB))
    m.add(0, box("prop_d", 5, 0.4, 5, (0, -57.6, 0.5), DARK))
    m.add(0, pediment("prop_ped", 18, 7, 8.5, 2.6, -57.5, MARB, TILE_R, ridges=False, statues=False))
    m.add(0, box("walk", 6, 30, 0.2, (0, -36, 0.5), MARB))
    for k in range(18):
        t = -51 + k * 6
        for (x, y) in ((t, -53.6), (t, 53.6), (-53.6, t), (53.6, t)):
            m.add(0, box(f"pil{k}_{x}_{y}", 0.9, 0.9, 5.6, (x, y, 0.5), MARB))
    for i, (x, y) in enumerate([(-30, -30), (30, -30), (-30, 30), (30, 30)]):
        m.add(2, cylinder(f"sbase{i}", 1.2, 2.0, (x, y, 0.5), MARB, verts=12))
        m.add(2, statue(f"ptolemy{i}", x, y, 2.5, 3.4, BRONZE))
    # mausoleum: podium, Doric ring, stepped pyramid, the finial
    m.add(1, box("pod", 32, 32, 6.5, (0, 0, 0.5), LIME_D), "mausoleum")
    m.add(1, box("pod_c", 33, 33, 0.6, (0, 0, 6.4), LIME))
    m.add(1, steps_front("stairs", 12, 6.5, 16, -16, 0.5, LIME_D))
    m.add(1, cylinder("drum", 10.5, 10, (0, 0, 7.0), LIME, verts=32))
    m.add(1, colonnade("ring", [(13 * math.cos(math.tau * i / 20), 13 * math.sin(math.tau * i / 20)) for i in range(20)], 7.0, 9.0, 0.55, "ionic", MARB))
    m.add(1, box("door", 2.4, 0.4, 4, (0, -10.6, 7.0), DARK))
    m.add(2, cylinder("ent", 14.2, 1.6, (0, 0, 16.0), MARB, verts=32), "roof")
    for k in range(6):
        m.add(2, cylinder(f"step{k}", 13.5 - k * 2.1, 1.5, (0, 0, 17.6 + k * 1.5), shade(LIME, 0.02 * (k % 2)), verts=32))
    m.add(2, cylinder("cone", 2.5, 3.0, (0, 0, 26.6), MARB, verts=16, r_top=1.0))
    m.add(2, statue("alexander", 0, 0, 29.6, 4.2, GILT))
    for i, (x, y) in enumerate([(-38, -38), (38, -38), (-38, 38), (38, 38), (-38, 0), (38, 0)]):
        m.add(2, tree(f"cyp{i}", 1.6, (x, y, 0.5), "#4F6B45", kind="cypress"))
    return m


# ---------------------------------------------------------------- the Serapeum (hero)
def serapeum(variant="roman"):
    m = Model("serapeum")
    W, D = 160.0, 100.0
    hz = 7.0    # platform height
    m.add(0, frustum("hill", W, D, W - 6, D - 6, 3.0, (0, 0, 0), ROCK), "platform")
    m.add(0, box("platform", W - 8, D - 8, hz - 3.0, (0, 0, 3.0), LIME_D))
    m.add(0, box("plat_c", W - 7, D - 7, 0.6, (0, 0, hz - 0.6), LIME))
    # the hundred steps: a broad stair up the south face
    m.add(0, steps_front("stair", 34, hz, 24, -(D - 8) / 2, 0, LIME_D, tread=0.75))
    for s in (-1, 1):
        m.add(0, box(f"cheek{s}", 3, 18, hz + 0.6, (s * 18.5, -(D - 8) / 2 - 9, 0), LIME))
        m.add(0, box(f"sphinx{s}", 2.4, 6, 2.0, (s * 18.5, -(D - 8) / 2 - 15, hz + 0.6 - hz), GREYGRAN))
        m.add(0, box(f"sphh{s}", 1.8, 1.8, 1.8, (s * 18.5, -(D - 8) / 2 - 17.8, 2.0), GREYGRAN))
    if variant == "ruin":
        m.add(1, box("pave", W - 12, D - 12, 0.2, (0, 0, hz), SAND), "ruins")
        m.add(1, move(rubble("rub", 120, W - 20, D - 20, 3, LIME_D, 2.4), 0, 0, hz))
        frag = [(-70 + i * 5.2, -37) for i in range(7)] + [(-70, -30 + i * 5.2) for i in range(4)]
        m.add(1, colonnade("frag", frag, hz, 6.0, 0.42, "doric", LIME))
        m.add(1, box("frag_ent", 36, 1.4, 0.9, (-54.4, -37, hz + 6.0), LIME))
        m.add(1, box("temple_pod", 28, 48, 3.0, (0, 6, hz), shade(MARB, -0.12)))
        for i, (x, y, h) in enumerate([(-11, -15, 9), (-6, -15, 5), (11, 20, 7), (11, 26, 4), (-11, 28, 11)]):
            m.add(1, column(f"stub{i}", x, y, hz + 3, h, 0.75, "tuscan", MARB))
        for i in range(4):
            m.add(1, cylinder(f"drum{i}", 0.8, 1.8, (25 + i * 3, -10 + i * 4, hz), MARB, verts=12))
        # the martyrium of St John built in the ruins
        b = basilica("martyrium", 30, 16, 9, LIME, TILE_R, aisles=True)
        m.add(2, move(rot(b, 180), 46, 18, hz), "church")
        m.add(2, palms("palm", [(x, y, hz) for x, y in [(-40, 20), (-50, 5), (30, -25), (60, -20)]], 2.6), "trees")
        return m
    m.add(0, box("pave", W - 12, D - 12, 0.2, (0, 0, hz), PAVE))
    # colonnades round the court, the daughter library in the rooms behind them
    m.add(1, move(court("stoa", W - 10, D - 10, 7.5, 6.2, 0.4, 3.6, "doric", LIME, TILE_R, doors=True), 0, 0, hz), "colonnades")
    m.add(1, box("gate", 16, 9, 10.5, (0, -(D - 10) / 2 + 4.5, hz), MARB))
    m.add(1, box("gate_d", 6, 0.4, 7, (0, -(D - 10) / 2 - 0.2, hz), DARK))
    m.add(1, pediment("gate_ped", 16, 9, hz + 10.5, 2.8, -(D - 10) / 2, MARB, TILE_R, ridges=False, statues=False))
    # the temple of Sarapis: Corinthian, peripteral, on a podium
    tp = temple("temple", 26, 46, 3.2, 14.0, 6, 11, "corinthian", MARB, TILE_R, col_r=0.78, peripteral=True, statues=True, stair_w=16)
    labels = ("temple", None, "roof")
    for i, p in enumerate(place_all(tp, 0, 8, hz)):
        m.add(2 + (1 if i == 2 else 0), p, labels[i] if labels[i] else None)
    # altar, Apis bull statue and obelisk-like markers in the court
    m.add(2, box("altar", 6, 3.5, 1.6, (0, -24, hz), MARB))
    m.add(2, box("apis", 2.0, 4.0, 2.2, (-14, -22, hz + 1.0), BASALT))
    m.add(2, box("apis_b", 3, 5, 1.0, (-14, -22, hz), MARB))
    for s in (-1, 1):
        m.add(2, red_obelisk(f"obl{s}", 9.0, (s * 9, -30, hz), RGRAN))
    # a small shrine of Harpocrates in the south-east corner and palms
    m.add(3, palms("palm", [(x, y, hz) for x, y in [(-35, -22), (35, -22), (-35, 30), (35, 30), (-55, 0), (55, 0)]], 2.6))
    return m


def pompeys_pillar():
    m = Model("pompeys-pillar")
    m.add(0, box("ground", 20, 20, 0.3, (0, 0, 0), SAND), "base")
    m.add(0, box("found", 7.6, 7.6, 1.2, (0, 0, 0.3), LIME_D))
    m.add(0, box("pedestal", 4.6, 4.6, 3.0, (0, 0, 1.5), RGRAN))
    m.add(0, box("ped_c", 5.0, 5.0, 0.4, (0, 0, 4.1), shade(RGRAN, 0.05)))
    m.add(0, box("ped_b", 5.0, 5.0, 0.3, (0, 0, 1.5), shade(RGRAN, 0.05)))
    m.add(0, box("inscr", 1.6, 0.1, 0.8, (0, -2.35, 3.0), shade(RGRAN, -0.15)))
    m.add(1, column("col", 0, 0, 4.5, 22.5, 1.35, "corinthian", RGRAN, flutes=40), "shaft")
    m.add(1, lathe("torus", [(1.75, 0), (1.85, 0.25), (1.7, 0.5), (1.55, 0.6)], (0, 0, 4.5), shade(RGRAN, 0.06), verts=40))
    for k in range(16):
        a = math.tau * k / 16
        m.add(1, box(f"leaf{k}", 0.55, 0.3, 1.1, (math.cos(a) * 1.25, math.sin(a) * 1.25, 4.5 + 22.5 - 2.9 + (k % 2) * 0.5), shade(RGRAN, -0.05), rot_z=a))
    m.add(2, box("top", 2.6, 2.6, 0.6, (0, 0, 27.0), shade(RGRAN, 0.05)), "top")
    for i, (x, y, r) in enumerate([(-7, -6, 0.3), (6, -7, 1.2), (7, 6, 2.0), (-6, 7, 0.7)]):
        m.add(2, box(f"blk{i}", 2.2, 1.4, 0.9, (x, y, 0.3), LIME_D, rot_z=r))
    m.add(2, move(rubble("rub", 45, 18, 18, 21, LIME_D, 0.9), 0, 0, 0.3))
    m.add(2, box("sphinx", 1.0, 2.6, 1.0, (-5, 0, 0.3), RGRAN))
    m.add(2, box("sphinx2", 1.0, 2.6, 1.0, (5, 0, 0.3), RGRAN))
    return m


# ---------------------------------------------------------------- the Caesareum
def caesareum(variant="roman"):
    m = Model("caesareum")
    W, D = 150.0, 110.0
    if variant == "needles":
        m.add(0, box("sand", W, D, 0.4, (0, 0, 0), SAND), "ground")
        m.add(0, move(rubble("rub", 110, W - 30, D - 30, 11, LIME_D, 2.2), 0, 10, 0.4))
        m.add(0, move(rubble("rubm", 30, 40, 20, 12, MARB, 1.4), -20, -30, 0.4))
        m.add(0, box("seawall", W, 4, 3.0, (0, -D / 2 + 2, 0), MAM_D))
        m.add(1, red_obelisk("needle_standing", 21.0, (-12, -38, 0.4), RGRAN), "needles")
        m.add(1, fallen_obelisk("needle_fallen", 21.0, (12, -38, 0.0), 80))
        m.add(1, box("needle_sand", 24, 5, 0.7, (22, -39.8, 0.3), SAND, rot_z=-0.17))
        for i, (x, y) in enumerate([(-40, 10), (35, 20), (-20, 30), (50, -10)]):
            m.add(1, box(f"wallfrag{i}", 12, 1.6, 3.5, (x, y, 0.4), shade(LIME, -0.1), rot_z=i * 0.4))
        m.add(2, palms("palm", [(x, y, 0.4) for x, y in [(-55, 30), (-45, 40), (40, 40), (60, 30), (20, 0)]], 2.6), "palms")
        return m
    m.add(0, box("plinth", W, D, 1.0, (0, 0, 0), LIME_D), "precinct")
    m.add(0, box("pave", W - 10, D - 10, 0.2, (0, 0, 1.0), PAVE))
    m.add(1, move(court("stoa", W - 8, D - 8, 8, 7.0, 0.45, 3.8, "corinthian" if variant == "roman" else "doric", MARB, TILE_R, doors=True, skip=("S",)), 0, 0, 1.0), "porticoes")
    m.add(1, box("front_wall", W - 8, 1.4, 6, (0, -D / 2 + 4.7, 1.0), LIME))
    m.add(1, box("propylon", 20, 9, 11, (0, -D / 2 + 4.5, 1.0), MARB))
    m.add(1, box("prop_d", 6.5, 0.4, 7.5, (0, -D / 2 - 0.05, 1.0), DARK))
    m.add(1, pediment("prop_ped", 20, 9, 12.0, 3.0, -D / 2, MARB, TILE_R, ridges=False, statues=False))
    # the obelisks before the gate
    for s in (-1, 1):
        m.add(2, red_obelisk(f"needle{s}", 21.0, (s * 16, -D / 2 + 1.5, 1.0), RGRAN), "obelisks")
    if variant == "church":
        b = basilica("kaisarion", 46, 26, 13, LIME, TILE_R)
        m.add(2, move(rot(b, 90), 0, 12, 1.2), "church")
        m.add(2, box("atrium_font", 3, 3, 1.0, (0, -20, 1.2), MARB))
        m.add(3, move(rubble("rub", 14, 60, 20, 5, MARB, 1.6), 30, -22, 1.2), "spoils")
        return m
    tp = temple("sebasteion", 30, 42, 3.6, 15, 6, 0, "corinthian", MARB, TILE_R, col_r=0.85, peripteral=False, statues=True, stair_w=24)
    for i, p in enumerate(place_all(tp, 0, 16, 1.2)):
        m.add(2 + (1 if i == 2 else 0), p, "temple" if i == 0 else ("roof" if i == 2 else None))
    m.add(2, box("altar", 6, 3, 1.5, (0, -20, 1.2), MARB))
    for i, (x, y) in enumerate([(-45, -20), (45, -20), (-45, 10), (45, 10), (-25, -30), (25, -30)]):
        m.add(3, tree(f"grove{i}", 2.6, (x, y, 1.2), "#6F8A5C"))
    return m


# ---------------------------------------------------------------- Timonium and the Poseidion mole
def timonium():
    m = Model("timonium")
    L = 340.0
    m.add(0, frustum("mole", 20, L - 60, 16, L - 60, 2.4, (0, -30, 0), LIME_D), "mole")
    m.add(0, box("mole_top", 15, L - 60, 0.3, (0, -30, 2.4), PAVE))
    m.add(0, frustum("tip", 66, 70, 62, 66, 2.4, (0, L / 2 - 35, 0), LIME_D))
    for k in range(10):
        m.add(0, box(f"bol{k}", 0.7, 0.7, 1.0, (-8.5, -150 + k * 26, 2.4), DARK))
    # the Poseidion: a small Doric temple at the root of the mole
    tp = temple("poseidion", 14, 22, 2.0, 7.0, 4, 0, "doric", MARB, TILE_R, col_r=0.5, peripteral=False, statues=False)
    for p in place_all(tp, 0, -150, 0, 0):
        m.add(1, p, "poseidion")
    m.add(1, statue("poseidon", 0, -165, 0, 5.0, BRONZE))
    # Antony's retreat at the tip: a peristyle pavilion with a hipped roof
    z = 2.4
    m.add(2, box("tim_base", 50, 50, 1.2, (0, L / 2 - 35, z), MARB), "timonium")
    m.add(2, box("tim_hall", 30, 30, 8, (0, L / 2 - 35, z + 1.2), LIME))
    pts = peristyle(44, 44, 9, 9)
    m.add(2, colonnade("tim_cols", [(x, y + L / 2 - 35) for x, y in pts], z + 1.2, 6.5, 0.42, "ionic", MARB))
    m.add(2, box("tim_ent", 46, 46, 1.0, (0, L / 2 - 35, z + 7.7), MARB))
    m.add(3, tiled_hip_roof("tim_roof", 46, 46, 6.5, (0, L / 2 - 35, z + 8.7), TILE_R), "roof")
    m.add(3, box("tim_up", 18, 18, 4, (0, L / 2 - 35, z + 9.2), LIME))
    m.add(3, hip_roof("tim_up_roof", 18, 18, 3, (0, L / 2 - 35, z + 13.2), TILE_R))
    m.add(3, box("boathouse", 10, 18, 5, (-24, L / 2 - 70, 2.4), LIME))
    return m


# ---------------------------------------------------------------- the Gymnasium
def gymnasium():
    m = Model("gymnasium")
    W, D = 220.0, 190.0
    m.add(0, box("plinth", W, D, 0.8, (0, 0, 0), LIME_D), "grounds")
    m.add(0, box("sand", W - 30, D - 60, 0.15, (0, -15, 0.8), SAND))
    # the great court with its porticoes over a stade long
    m.add(1, move(court("court", W, D - 50, 9, 7.0, 0.45, 5.0, "doric", LIME, TILE_R, skip=("N",)), 0, -25, 0.8), "porticoes")
    # xystos: a long covered running track along the north side
    m.add(1, box("xystos_floor", W, 14, 0.5, (0, D / 2 - 32, 0.8), SAND))
    xy = portico("xystos", W, 14, 7.5, 0.48, 4.6, "doric", LIME, TILE_R)
    m.add(1, move(xy, 0, D / 2 - 32, 0.8))
    # palaestra: rooms round a square wrestling court
    m.add(2, move(court("palaestra", 60, 40, 7, 6.0, 0.4, 3.8, "ionic", MARB, TILE_R, doors=True), 60, -20, 0.8), "palaestra")
    m.add(2, box("pal_sand", 44, 24, 0.2, (60, -20, 0.8), SAND))
    # baths with vaulted halls
    m.add(2, box("bath", 44, 30, 8, (-60, -20, 0.8), LIME))
    for k in range(3):
        m.add(2, half_cyl_y(f"vault{k}", 6.5, 30, (-75 + k * 14.5, -20, 8.8), TILE_R, verts=12))
    m.add(2, arcade("bath_arc", 40, 5, 6, (-60, -35.05, 0.8), "S", DARK, pointed=False))
    # statues and a herm row along the track
    for i in range(10):
        m.add(3, statue(f"herm{i}", -90 + i * 20, -60, 0.8, 2.4, MARB), "statues")
    m.add(3, box("altar", 3, 2, 1.2, (0, -40, 0.8), MARB))
    for i, (x, y) in enumerate([(-30, -55), (30, -55), (0, 5), (-20, 0), (20, 0)]):
        m.add(3, tree(f"plane{i}", 3.2, (x, y, 0.8), "#6F8A5C"))
    return m


# ---------------------------------------------------------------- the Paneion
def paneion():
    m = Model("paneion")
    R, H = 66.0, 30.0
    prof = []
    for i in range(13):
        t = i / 12
        prof.append((R * (1 - t) ** 1.25 + 7.0 * t, H * t))
    m.add(0, lathe("cone", prof, (0, 0, 0), "#A49B72", verts=40), "hill")
    m.add(0, cylinder("foot", R + 2, 0.8, (0, 0, 0), GRASS, verts=40))
    # the spiral road: blocks laid along a helix on the slope
    path = []
    turns, n = 2.6, 150
    for i in range(n):
        t = i / (n - 1)
        a = -math.pi / 2 + t * turns * math.tau
        z = H * t
        r = R * (1 - t) ** 1.25 + 7.0 * t + 0.6
        path.append((r * math.cos(a), r * math.sin(a), z))
    for i in range(n - 1):
        (x0, y0, z0), (x1, y1, z1) = path[i], path[i + 1]
        L = math.hypot(x1 - x0, y1 - y0) + 0.4
        a = math.atan2(y1 - y0, x1 - x0)
        m.add(1, box(f"road{i}", L, 3.2, 0.7, ((x0 + x1) / 2, (y0 + y1) / 2, max(0.0, min(z0, z1) - 0.1)), PAVE, rot_z=a), "road")
    for i in range(0, n - 1, 8):
        x, y, z = path[i]
        k = 1.12
        m.add(1, tree(f"pine{i}", 1.7, (x * k, y * k, max(0.0, z - 1.5)), "#5E7A4E", kind="cypress"))
    for i, a in enumerate([math.tau * j / 9 for j in range(9)]):
        m.add(1, tree(f"foot_tree{i}", 2.6, (math.cos(a) * (R - 4), math.sin(a) * (R - 4), 0.8), "#6F8A5C"))
    # shrine of Pan on the summit
    m.add(2, cylinder("sum", 7.5, 0.8, (0, 0, H), LIME, verts=24), "shrine")
    m.add(2, colonnade("tholos", [(4.6 * math.cos(a), 4.6 * math.sin(a)) for a in [math.tau * i / 8 for i in range(8)]], H + 0.8, 4.5, 0.32, "ionic", MARB))
    m.add(2, cylinder("tholos_ent", 5.2, 0.6, (0, 0, H + 5.3), MARB, verts=24))
    m.add(2, dome("tholos_roof", 5.2, (0, 0, H + 5.9), TILE_R, squash=0.6, segments=20, rings=6))
    m.add(2, statue("pan", 0, 0, H + 0.8, 2.6, BRONZE))
    return m


# ---------------------------------------------------------------- Kom el-Dikka
def kom_el_dikka():
    m = Model("kom-el-dikka")
    m.add(0, box("ground", 90, 90, 0.4, (0, 0, 0), PAVE), "theatre")
    # horseshoe cavea, opening south toward the stage
    rows, r0 = 13, 8.0
    for k in range(rows):
        r = r0 + k * 1.15
        m.add(0, ellipse_ring(f"row{k}", r + 1.15, r + 1.15, r / (r + 1.15), 0.4 + k * 0.42, (0, 4, 0.4), MARB if k % 2 == 0 else shade(MARB, -0.06), n=32, arc=math.pi * 1.25, start=-math.pi * 0.125))
    rt = r0 + rows * 1.15
    m.add(1, ellipse_ring("outer", rt + 2.2, rt + 2.2, rt / (rt + 2.2), 6.4, (0, 4, 0.4), LIME, n=32, arc=math.pi * 1.25, start=-math.pi * 0.125), "gallery")
    gal = [(0 + (rt + 1.1) * math.cos(a), 4 + (rt + 1.1) * math.sin(a)) for a in [-math.pi * 0.1 + i * math.pi * 1.2 / 13 for i in range(14)]]
    m.add(1, colonnade("gallery_cols", gal, 6.8, 3.8, 0.28, "ionic", MARB))
    m.add(1, box("orch", 13, 9, 0.2, (0, 2, 0.4), shade(MARB, 0.04)))
    m.add(1, box("stage", 26, 6, 3.5, (0, -10, 0.4), LIME))
    m.add(1, box("scaena", 30, 3, 7, (0, -14, 0.4), LIME))
    m.add(1, colonnade("scaena_cols", [(-12 + i * 4, -12.2) for i in range(7)], 3.9, 3.6, 0.25, "corinthian", MARB))
    # dome over the cavea (6th century roof, shown light)
    m.add(2, ellipse_ring("dome_ring", rt + 2.2, rt + 2.2, 0.92, 1.0, (0, 4, 6.8), shade(LIME, -0.05), n=32), "roof")
    # portico and lecture halls along the east side
    m.add(2, box("portico_floor", 18, 80, 0.4, (34, 0, 0.4), PAVE))
    m.add(2, colonnade("portico", [(26, -36 + i * 6) for i in range(13)], 0.8, 5.0, 0.32, "doric", MARB))
    for i in range(5):
        y = -32 + i * 16
        m.add(2, box(f"aud{i}", 13, 12, 5.5, (37.5, y, 0.4), LIME))
        m.add(2, box(f"aud_r{i}", 13.6, 12.6, 0.4, (37.5, y, 5.9), TILE_R))
        m.add(2, box(f"aud_d{i}", 0.3, 2.2, 3, (30.9, y, 0.4), DARK))
    # baths to the west
    m.add(2, box("bath", 20, 30, 7, (-34, -20, 0.4), shade(LIME, -0.04)))
    for k in range(2):
        m.add(2, half_cyl_y(f"bvault{k}", 4.8, 30, (-39 + k * 10, -20, 7.4), TILE_R, verts=10))
    m.add(2, box("cistern", 12, 12, 2.0, (-34, 22, 0.4), LIME_D))
    return m


# ---------------------------------------------------------------- gates
def city_gate():
    m = Model("city-gate")
    m.add(0, box("road", 14, 24, 0.3, (0, 0, 0), PAVE), "walls")
    for s in (-1, 1):
        m.add(0, box(f"wall{s}", 16, 6, 10, (s * 22, 0, 0), LIME_D))
        m.add(0, move(merlons(f"wmer{s}", 16, 6, 10, 0.8, 1.0, LIME_D), s * 22, 0, 0))
    m.add(1, box("gate", 24, 14, 12, (0, 0, 0), LIME), "gate")
    m.add(1, arch_panel("pass_s", 6.0, 8.5, (0, -7.05, 0), "S", DARK, pointed=False, depth=0.6))
    m.add(1, arch_panel("pass_n", 6.0, 8.5, (0, 7.05, 0), "N", DARK, pointed=False, depth=0.6))
    for s in (-1, 1):
        m.add(1, cylinder(f"tower{s}", 6.2, 16, (s * 13, -2.5, 0), LIME, verts=20))
        m.add(1, cylinder(f"tband{s}", 6.5, 0.5, (s * 13, -2.5, 11.5), MARB, verts=20))
        for k in range(10):
            a = math.tau * k / 10
            m.add(2, box(f"tmer{s}{k}", 1.2, 0.8, 1.3, (s * 13 + math.cos(a) * 5.8, -2.5 + math.sin(a) * 5.8, 16), LIME, rot_z=a), "battlements")
        for k in range(3):
            a = -math.pi / 2 + (k - 1) * 0.6
            w = box(f"slit{s}{k}", 0.6, 0.4, 1.8, (s * 13 + math.cos(a) * 6.2, -2.5 + math.sin(a) * 6.2, 12.5), DARK)
            w.rotation_euler[2] = a + math.pi / 2
            m.add(2, w)
    m.add(2, move(merlons("gmer", 24, 14, 12, 0.9, 1.0, LIME), 0, 0, 0))
    m.add(2, entablature("gent", -8, 8, -7.4, -6.6, 9.2, 1.2, MARB, dentils=True))
    m.add(2, entablature("gentn", -8, 8, 6.6, 7.4, 9.2, 1.2, MARB, dentils=True))
    for s in (-1, 1):
        for k in range(2):
            m.add(1, column(f"pil{s}{k}", s * (4.6 + k * 2.6), -7.3, 0, 9.0, 0.35, "ionic", MARB))
        m.add(1, lathe(f"tbase{s}", [(6.8, 0), (6.8, 1.2), (6.3, 1.6)], (s * 13, -2.5, 0), LIME_D, verts=32))
    m.add(2, statue("gstat", 0, -7.5, 12.0, 3.2, BRONZE))
    return m


def bab_rashid():
    m = Model("bab-rashid")
    m.add(0, box("road", 10, 26, 0.3, (0, 0, 0), SAND), "walls")
    for s in (-1, 1):
        m.add(0, box(f"wall{s}", 10, 5, 9, (s * 17, 0, 0), MAM_D))
        m.add(0, move(merlons(f"wmer{s}", 10, 5, 9, 0.8, 0.9, MAM_D, "stepped"), s * 17, 0, 0))
    m.add(1, box("gate", 14, 12, 11, (0, 0, 0), MAM), "gate")
    m.add(1, iwan("arch_s", 8, 10, 1.0, (0, -6.5, 0), "S", MAM, MAM_D))
    m.add(1, arch_panel("arch_n", 4.5, 7, (0, 6.05, 0), "N", DARK, pointed=True))
    for s in (-1, 1):
        m.add(1, box(f"tower{s}", 10, 12, 15, (s * 11, -0.5, 0), shade(MAM, -0.03)))
        m.add(1, move(merlons(f"tmer{s}", 10, 12, 15, 0.9, 0.9, MAM, "stepped"), s * 11, -0.5, 0))
        m.add(1, arch_panel(f"slit{s}", 0.9, 2.4, (s * 11, -6.55, 10), "S", DARK))
    m.add(2, move(merlons("gmer", 14, 12, 11, 0.9, 0.9, MAM, "stepped"), 0, 0, 0), "battlements")
    m.add(2, box("inscr", 6, 0.3, 0.8, (0, -6.7, 9.6), MAM_D))
    for s in (-1, 1):
        for k in range(4):
            m.add(2, box(f"band{s}{k}", 10.4, 12.4, 0.35, (s * 11, -0.5, 3 + k * 3), MAM_D))
        m.add(2, box(f"mach{s}", 4, 1.6, 2.0, (s * 11, -7.2, 12.2), MAM))
        for k in range(4):
            m.add(2, box(f"corb{s}{k}", 0.5, 1.2, 0.6, (s * 11 - 1.5 + k, -6.6, 11.6), MAM_D))
    return m


# ---------------------------------------------------------------- Kom el-Shoqafa
def kom_el_shoqafa():
    m = Model("kom-el-shoqafa")
    m.add(0, box("ground", 50, 50, 0.6, (0, 0, 0), ROCK), "ground")
    # the round light shaft with its parapet, the spiral stair dropping into it
    m.add(0, ellipse_ring("shaft_wall", 4.6, 4.6, 0.8, 1.4, (0, 0, 0.6), LIME, n=24))
    m.add(0, cylinder("shaft", 3.7, 0.2, (0, 0, 0.55), DARK, verts=24))
    for k in range(12):
        a = math.tau * k / 12
        m.add(0, box(f"stair{k}", 1.2, 0.8, 0.15, (math.cos(a) * 3.2, math.sin(a) * 3.2, 0.62), shade(LIME_D, -0.2), rot_z=a))
    # small kiosk over the stair head, Egyptian cornice
    m.add(1, box("kiosk", 7, 7, 4.5, (0, -9, 0.6), LIME), "kiosk")
    m.add(1, frustum("cavetto", 7.0, 7.0, 8.0, 8.0, 0.8, (0, -9, 5.1), MARB))
    m.add(1, box("kiosk_d", 2, 0.3, 3, (0, -12.55, 0.6), DARK))
    for s in (-1, 1):
        m.add(1, column(f"kcol{s}", s * 2.4, -12.9, 0.6, 4.4, 0.32, "tuscan", MARB))
    # funeral banquet hall (triclinium) above ground, and family tomb markers
    m.add(1, box("tric", 12, 9, 4, (12, 8, 0.6), LIME))
    m.add(1, gable_roof("tric_roof", 12, 9, 2, (12, 8, 4.6), TILE_R, 0.4))
    for i, (x, y) in enumerate([(-14, 10), (-10, 16), (-16, -6), (-12, -16), (14, -14), (16, -6)]):
        m.add(2, box(f"stele{i}", 1.2, 0.5, 2.0, (x, y, 0.6), LIME), "graves")
        m.add(2, box(f"grave{i}", 1.8, 2.8, 0.5, (x, y + 1.8, 0.6), LIME_D))
    m.add(2, palms("palm", [(x, y, 0.6) for x, y in [(-18, 18), (18, 18), (-20, -18), (20, 2)]], 2.4))
    m.add(2, statue("anubis", 4.8, -9.5, 0.6, 2.2, BASALT))
    m.add(2, move(rubble("rocks", 40, 46, 46, 31, ROCK, 1.2), 0, 0, 0.6))
    for i in range(6):
        x = -20 + i * 8
        m.add(2, box(f"loculi{i}", 5, 2.2, 2.6, (x, 21.5, 0.6), LIME_D))
        m.add(2, box(f"loc_d{i}", 1.2, 0.3, 1.6, (x, 20.3, 0.6), DARK))
        m.add(2, frustum(f"loc_c{i}", 5, 2.2, 5.6, 2.6, 0.5, (x, 21.5, 3.2), LIME))
    return m


# ---------------------------------------------------------------- churches and mosques
def st_mark():
    m = Model("st-mark")
    m.add(0, box("ground", 64, 36, 0.5, (0, 0, 0), PAVE), "church")
    b = basilica("martyrium", 34, 20, 11, LIME, TILE_R)
    m.add(1, move(b, 10, 0, 0.5))
    m.add(1, move(court("atrium", 16, 20, 3.2, 4.0, 0.25, 2.4, "ionic", MARB, TILE_R, skip=("E",)), -20, 0, 0.5))
    m.add(2, box("tomb_chapel", 8, 8, 6, (24, 12, 0.5), LIME), "chapel")
    m.add(2, shallow_dome("tomb_dome", 4.2, (24, 12, 6.5), TILE_R, rise=0.6))
    m.add(2, box("hospice", 14, 7, 5, (-12, 14.4, 0.5), shade(LIME, -0.05)))
    m.add(2, move(rot(gable_roof("hospice_r", 7, 14, 2.0, (0, 0, 0), TILE_R, 0.3), 90), -12, 14.4, 5.5))
    m.add(2, palms("palm", [(x, y, 0.5) for x, y in [(-26, -12), (-20, -14), (26, -12)]], 2.4))
    return m


def st_athanasius(variant="church"):
    m = Model("st-athanasius")
    W, D = 60.0, 56.0
    m.add(0, box("ground", W, D, 0.5, (0, 0, 0), PAVE), "court")
    if variant == "church":
        m.add(0, move(court("atrium", 22, 30, 4, 4.5, 0.32, 3.2, "ionic", MARB, TILE_R), -18, 0, 0.5))
        m.add(0, cylinder("font", 1.6, 0.8, (-18, 0, 0.5), MARB, verts=12))
        b = basilica("basilica", 30, 24, 12, LIME, TILE_R, narthex=True)
        m.add(1, move(b, 13, 0, 0.5), "church")
        m.add(2, box("bapt", 8, 8, 6, (13, -20, 0.5), LIME), "baptistery")
        m.add(2, shallow_dome("bapt_d", 4.2, (13, -20, 6.5), TILE_R, rise=0.6))
        return m
    # the mosque: hypostyle prayer hall on the south-east (qibla) side, open court, minaret, the sarcophagus kiosk
    m.add(0, box("court_pave", 34, 30, 0.2, (-10, -6, 0.5), SAND))
    m.add(0, courtyard_ring("court", 56, 52, 7, 6, (0, 0, 0.5), MAM, DARK))
    m.add(1, box("hall", 54, 18, 9, (0, 16, 0.5), MAM), "hall")
    m.add(1, arcade("hall_arc", 50, 6.5, 10, (0, 6.95, 0.5), "S", DARK, pointed=True))
    m.add(1, box("hall_roof", 55, 19, 0.6, (0, 16, 9.5), MAM_D))
    m.add(1, move(merlons("hall_mer", 54, 18, 10.1, 0.6, 0.8, MAM, "stepped"), 0, 16, 0))
    m.add(1, shallow_dome("mihrab_dome", 4.5, (0, 22, 10.1), MAM, rise=0.7, drum=1.2))
    m.add(2, mamluk_minaret("minaret", (24, -22, 0.5), 30, MAM, MAM_D), "minaret")
    m.add(2, box("kiosk_b", 6, 6, 0.6, (-10, -6, 0.7), MAM_D))
    for i, (x, y) in enumerate([(-12.4, -8.4), (-7.6, -8.4), (-7.6, -3.6), (-12.4, -3.6)]):
        m.add(2, cylinder(f"kc{i}", 0.25, 3.5, (x, y, 1.3), MARB, verts=6))
    m.add(2, shallow_dome("kiosk_d", 3.4, (-10, -6, 4.8), MAM, rise=0.7))
    m.add(2, box("sarcophagus", 1.8, 3.2, 1.3, (-10, -6, 1.3), "#3E4A42"))
    m.add(2, palms("palm", [(x, y, 0.7) for x, y in [(-22, -16), (4, -16)]], 2.4))
    return m


def al_mursi():
    m = Model("al-mursi")
    m.add(0, box("ground", 40, 50, 0.4, (0, 0, 0), SAND), "court")
    m.add(0, courtyard_ring("court", 34, 22, 5, 3.5, (0, -12, 0.4), MAM, DARK))
    m.add(1, box("hall", 34, 20, 8, (0, 10, 0.4), MAM), "hall")
    m.add(1, arcade("hall_arc", 30, 6, 6, (0, -0.05, 0.4), "S", DARK))
    m.add(1, move(merlons("hall_mer", 34, 20, 8.4, 0.6, 0.8, MAM, "stepped"), 0, 10, 0))
    m.add(1, box("hall_roof", 34.4, 20.4, 0.4, (0, 10, 8.0), MAM_D))
    m.add(1, box("tomb", 12, 12, 10, (-8, 14, 0.4), MAM))
    m.add(1, cylinder("tomb_oct", 6.2, 2.4, (-8, 14, 10.4), MAM, verts=8))
    m.add(2, ribbed_dome("dome", 5.6, (-8, 14, 12.8), MAM, height=1.25, ribs=20, drum=0.35, drum_color=MAM_D), "dome")
    m.add(2, mamluk_minaret("minaret", (13, 22, 0.4), 26, MAM, MAM_D), "minaret")
    m.add(2, iwan("gate", 7, 9, 2, (0, -23.5, 0.4), "S", MAM, MAM_D))
    return m


BUILDERS = {
    "alexandria/pharos": pharos,
    "alexandria/qaitbay": qaitbay,
    "alexandria/heptastadion": heptastadion,
    "alexandria/royal-palaces": royal_palaces,
    "alexandria/royal-palaces-ruin": lambda: royal_palaces("ruin"),
    "alexandria/museum": museum,
    "alexandria/sema": sema,
    "alexandria/serapeum": serapeum,
    "alexandria/serapeum-ruin": lambda: serapeum("ruin"),
    "alexandria/pompeys-pillar": pompeys_pillar,
    "alexandria/caesareum": caesareum,
    "alexandria/caesareum-church": lambda: caesareum("church"),
    "alexandria/needles": lambda: caesareum("needles"),
    "alexandria/timonium": timonium,
    "alexandria/gymnasium": gymnasium,
    "alexandria/paneion": paneion,
    "alexandria/kom-el-dikka": kom_el_dikka,
    "alexandria/city-gate": city_gate,
    "alexandria/bab-rashid": bab_rashid,
    "alexandria/kom-el-shoqafa": kom_el_shoqafa,
    "alexandria/st-mark": st_mark,
    "alexandria/st-athanasius": st_athanasius,
    "alexandria/attarine": lambda: st_athanasius("mosque"),
    "alexandria/al-mursi": al_mursi,
}
