"""Pataliputra / Patna landmark miniatures: Pataligama's stockade to Sher Shah's fort.

Mauryan buildings are interpretations: timber halls with pointed horseshoe barrel
roofs (after the rock-cut facade of the Lomas Rishi cave and the Sanchi reliefs),
polished Chunar sandstone pillars, double palisades of sal posts.
"""
import math
import random
import bpy
from chronokit import Model, box, cylinder, dome, join, shade, gable_roof, hip_roof, mesh_from, _finish
from worldkit import *

POLISH = "#DCCBA4"       # Chunar sandstone, polished
SAL = "#7A5A3A"          # sal timber
SAL_LT = "#9A7651"
SAL_DARK = "#4E3A29"
EARTH = "#B49A72"
DUST = "#CDB894"
SILT = "#A99B84"
BRICKR = "#A9654A"
TILE = "#9C5B3E"
LIME = "#E4DAC6"
ASH = "#5B544C"
LAWN = "#86A06E"
HOUSE_COLORS = ["#C9A47A", "#B8936A", "#D6BC94", "#A98260", "#CDB48E"]
FACE_ROT = {"S": 0, "N": 180, "E": 90, "W": -90}


# ---------------------------------------------------------------- helpers

def _rot_move(o, deg, x, y, z=0.0):
    if deg:
        o = rot(o, deg)
    return move(o, x, y, z)


def roof_profile(w, h):
    """Cross-section of a pointed horseshoe barrel roof (the Lomas Rishi arch), from one eave over the apex to the other."""
    P = [(0.46, 0.0), (0.5, 0.16), (0.5, 0.34), (0.47, 0.52), (0.41, 0.67), (0.32, 0.80), (0.21, 0.90), (0.10, 0.97), (0.0, 1.05)]
    right = [(w * a, h * b) for a, b in P]
    left = [(-y, z) for y, z in reversed(right[:-1])]
    return right + left


def _arch_prism(name, prof, x0, x1, color):
    """Extrude a closed (y, z) profile along X from x0 to x1."""
    n = len(prof)
    verts = [(x0, y, z) for y, z in prof] + [(x1, y, z) for y, z in prof]
    faces = [tuple(range(n)), tuple(range(2 * n - 1, n - 1, -1))] + [(i, (i + 1) % n, n + (i + 1) % n, n + i) for i in range(n)]
    return mesh_from(name, verts, faces, (0, 0, 0), color)


def chaitya_roof(name, length, w, h, loc=(0, 0, 0), color=THATCH, axis="x", gables=True, frame=SAL_LT, finials=0):
    """A barrel roof whose gable ends show the pointed horseshoe arch, with a timber frame and a dark tympanum."""
    x, y, z = loc
    L = length
    parts = [_arch_prism(name + "_r", roof_profile(w, h), -L / 2, L / 2, color)]
    if gables:
        for s in (-1, 1):
            fr = [(py * 0.86, pz * 0.86) for py, pz in roof_profile(w, h)]
            dk = [(py * 0.68, pz * 0.68) for py, pz in roof_profile(w, h)]
            parts.append(_arch_prism(f"{name}_f{s}", fr, s * L / 2, s * (L / 2 + 0.12), frame))
            parts.append(_arch_prism(f"{name}_d{s}", dk, s * L / 2, s * (L / 2 + 0.2), DARK))
    for i in range(finials):
        fx = -L / 2 + L * (i + 0.5) / finials
        parts.append(lathe(f"{name}_k{i}", [(0.0, 0), (w * 0.03, 0.0), (w * 0.05, w * 0.04), (w * 0.03, w * 0.08), (w * 0.012, w * 0.1), (0.0, w * 0.13)], (fx, 0, h * 1.03), GILT, verts=8))
    o = join(parts, name)
    if axis == "y":
        o = rot(o, 90)
    return move(o, x, y, z)


def posts_mesh(name, pts, r, h, color=SAL, sides=5, point=0.45, jitter=0.08, seed=1):
    """Many upright logs with pointed tops as one mesh. pts = [(x, y, z0), ...]."""
    rng = random.Random(seed)
    verts, faces = [], []
    for (px, py, pz) in pts:
        hh = h * (1 + rng.uniform(-jitter, jitter))
        a0 = rng.random()
        angs = [a0 + math.tau * i / sides for i in range(sides)]
        b = len(verts)
        verts += [(px + r * math.cos(a), py + r * math.sin(a), pz) for a in angs]
        verts += [(px + r * math.cos(a), py + r * math.sin(a), pz + hh) for a in angs]
        verts.append((px, py, pz + hh + point))
        for i in range(sides):
            j = (i + 1) % sides
            faces.append((b + i, b + j, b + sides + j, b + sides + i))
            faces.append((b + sides + i, b + sides + j, b + 2 * sides))
    return mesh_from(name, verts, faces, (0, 0, 0), color)


def line_pts(p0, p1, spacing, z=0.0):
    (ax, ay), (bx, by) = p0, p1
    L = math.hypot(bx - ax, by - ay)
    n = max(1, int(L / spacing))
    return [(ax + (bx - ax) * (k + 0.5) / n, ay + (by - ay) * (k + 0.5) / n, z) for k in range(n)]


def palisade_x(name, x0, x1, y, h=5.0, gap=4.5, spacing=0.62, z=0.0, seed=1, walk=True):
    """Megasthenes' wooden wall along X: two rows of sal posts with a walkway and rails between."""
    pts = line_pts((x0, y - gap / 2), (x1, y - gap / 2), spacing, z) + line_pts((x0, y + gap / 2), (x1, y + gap / 2), spacing, z)
    parts = [posts_mesh(name + "_p", pts, 0.3, h, SAL, seed=seed)]
    L, cx = x1 - x0, (x0 + x1) / 2
    for s in (-1, 1):
        parts.append(box(f"{name}_rl{s}", L, 0.25, 0.3, (cx, y + s * (gap / 2 + 0.3), z + 1.2), SAL_DARK))
        parts.append(box(f"{name}_rh{s}", L, 0.25, 0.3, (cx, y + s * (gap / 2 + 0.3), z + h - 0.9), SAL_DARK))
    if walk:
        parts.append(box(name + "_walk", L, gap - 0.4, 0.35, (cx, y, z + h - 1.6), SAL_LT))
    return join(parts, name)


def timber_tower(name, s, h, loc, roof=THATCH, axis="y", footing=BRICKR):
    """A square timber tower on a brick footing, a gallery, loopholes and a barrel roof."""
    x, y, z = loc
    parts = [box(name + "_f", s + 1.2, s + 1.2, 1.6, (x, y, z), footing)]
    parts.append(box(name + "_b", s, s, h - 1.6, (x, y, z + 1.6), SAL))
    parts.append(box(name + "_g", s + 1.6, s + 1.6, 0.4, (x, y, z + h * 0.72), SAL_DARK))
    for k in range(3):
        u = (k - 1) * s * 0.28
        for f, (dx, dy) in (("S", (u, -s / 2 - 0.04)), ("N", (u, s / 2 + 0.04)), ("E", (s / 2 + 0.04, u)), ("W", (-s / 2 - 0.04, u))):
            parts.append(box(f"{name}_l{f}{k}", 0.35 if f in "SN" else 0.12, 0.12 if f in "SN" else 0.35, 1.4, (x + dx, y + dy, z + h * 0.78), DARK))
    parts.append(box(name + "_top", s + 0.8, s + 0.8, 0.3, (x, y, z + h), SAL_DARK))
    parts.append(chaitya_roof(name + "_r", s + 1.4, s + 1.6, s * 0.75, (x, y, z + h + 0.3), roof, axis, finials=1))
    return join(parts, name)


def mauryan_pillar(name, h, r, loc, color=POLISH, crown="lion", face="S"):
    """A polished monolith with a lotus-bell capital, a round abacus with a frieze and an animal crown."""
    x, y, z = loc
    parts = [lathe(name + "_sh", [(r, 0), (r * 0.94, h * 0.5), (r * 0.8, h)], (x, y, z), color, verts=16)]
    k = r / 0.45
    zc = z + h
    bell = [(0.38, 0.0), (0.62, 0.06), (0.6, 0.18), (0.5, 0.45), (0.4, 0.7), (0.33, 0.85), (0.34, 0.9), (0.3, 0.98)]
    parts.append(lathe(name + "_bell", [(a * k, b * k) for a, b in bell], (x, y, zc), color, verts=24 if crown else 12))
    if crown:
        for i in range(16):
            a = math.tau * i / 16
            parts.append(box(f"{name}_pt{i}", 0.06 * k, 0.04 * k, 0.5 * k, (x + 0.57 * k * math.cos(a), y + 0.57 * k * math.sin(a), zc + 0.08 * k), shade(color, -0.1), rot_z=a + math.pi / 2))
    zc += 0.98 * k
    parts.append(cylinder(name + "_ab", 0.62 * k, 0.32 * k, (x, y, zc), shade(color, -0.05), verts=20))
    for i in range(12):
        a = math.tau * i / 12
        parts.append(box(f"{name}_gz{i}", 0.16 * k, 0.05 * k, 0.14 * k, (x + 0.63 * k * math.cos(a), y + 0.63 * k * math.sin(a), zc + 0.09 * k), shade(color, -0.2), rot_z=a + math.pi / 2))
    zc += 0.32 * k
    if crown == "lion":
        parts.append(lion(name + "_lion", 1.1 * k, (x, y, zc), color, face))
    elif crown == "bull":
        parts.append(box(name + "_bull", 0.4 * k, 0.9 * k, 0.6 * k, (x, y, zc), color))
    return join(parts, name)


def lion(name, s, loc, color=POLISH, face="S"):
    """A seated lion facing -Y, blocked out in a few masses: haunches, chest, forelegs, mane and muzzle."""
    x, y, z = loc
    parts = [box(name + "_h", 0.42 * s, 0.55 * s, 0.42 * s, (0, 0.18 * s, 0), color)]
    parts.append(box(name + "_c", 0.4 * s, 0.32 * s, 0.75 * s, (0, -0.1 * s, 0), color))
    for sx in (-1, 1):
        parts.append(box(f"{name}_l{sx}", 0.11 * s, 0.13 * s, 0.5 * s, (sx * 0.12 * s, -0.3 * s, 0), color))
    bpy.ops.mesh.primitive_ico_sphere_add(subdivisions=3, radius=0.3 * s, location=(0, -0.16 * s, 0.82 * s))
    parts.append(_finish(bpy.context.active_object, name + "_m", shade(color, -0.06)))
    parts.append(box(name + "_mz", 0.17 * s, 0.2 * s, 0.17 * s, (0, -0.42 * s, 0.72 * s), color))
    parts.append(box(name + "_tl", 0.06 * s, 0.3 * s, 0.06 * s, (0.18 * s, 0.4 * s, 0.02 * s), color))
    o = rot(join(parts, name), FACE_ROT[face])
    return move(o, x, y, z)


def timber_hall(name, w, d, h, loc=(0, 0, 0), plinth=1.2, plinth_color=BRICKR, wall=LIME, roof=THATCH, roof_h=None, post_every=3.2, axis="x", finials=3, door="S"):
    """A Mauryan timber hall: brick platform, plastered timber walls on a ring of posts, a pointed barrel roof."""
    x, y, z = loc
    parts = [box(name + "_pl", w + 4, d + 4, plinth, (x, y, z), plinth_color)]
    zb = z + plinth
    parts.append(box(name + "_b", w, d, h, (x, y, zb), wall))
    pts = []
    W, D = w + 2.4, d + 2.4
    for (ax, ay), (bx, by) in (((-W / 2, -D / 2), (W / 2, -D / 2)), ((W / 2, -D / 2), (W / 2, D / 2)), ((W / 2, D / 2), (-W / 2, D / 2)), ((-W / 2, D / 2), (-W / 2, -D / 2))):
        n = max(2, int(math.hypot(bx - ax, by - ay) / post_every))
        pts += [(x + ax + (bx - ax) * k / n, y + ay + (by - ay) * k / n, zb) for k in range(n)]
    parts.append(posts_mesh(name + "_po", pts, 0.28, h - 0.2, SAL, sides=6, point=0.0, jitter=0.0))
    parts.append(box(name + "_beam", W + 0.6, D + 0.6, 0.5, (x, y, zb + h - 0.2), SAL_DARK))
    if axis == "x":
        parts.append(chaitya_roof(name + "_r", w + 3.0, d + 3.4, roof_h or (d + 3.4) * 0.5, (x, y, zb + h + 0.3), roof, "x", finials=finials))
    else:
        parts.append(chaitya_roof(name + "_r", d + 3.0, w + 3.4, roof_h or (w + 3.4) * 0.5, (x, y, zb + h + 0.3), roof, "y", finials=finials))
    if door:
        dx, dy = {"S": (0, -d / 2 - 0.05), "N": (0, d / 2 + 0.05), "E": (w / 2 + 0.05, 0), "W": (-w / 2 - 0.05, 0)}[door]
        parts.append(arch_panel(name + "_door", min(w, d) * 0.22, h * 0.75, (x + dx, y + dy, zb), door, DARK, False))
        sx, sy = {"S": (0, -(d + 4) / 2 - 1.2), "N": (0, (d + 4) / 2 + 1.2), "E": ((w + 4) / 2 + 1.2, 0), "W": (-(w + 4) / 2 - 1.2, 0)}[door]
        parts.append(stair(name + "_st", min(w, d) * 0.35, plinth, 2.4, 4, (x + sx, y + sy, z), door, plinth_color))
    return join(parts, name)


def hut(name, w, d, h, loc, wall=EARTH, roof=THATCH, rot_deg=0.0):
    x, y, z = loc
    parts = [box(name + "_w", w, d, h, (0, 0, 0), wall), gable_roof(name + "_r", w, d, h * 0.8, (0, 0, h), roof, 0.4)]
    parts.append(box(name + "_d", w * 0.25, 0.1, h * 0.7, (0, -d / 2 - 0.02, 0), DARK))
    return _rot_move(join(parts, name), rot_deg, x, y, z)


def barrel_house(name, w, d, h, loc, wall, roof, rot_deg=0.0):
    """A small timber house with a little barrel roof (the common roof of the Sanchi and Bharhut reliefs)."""
    x, y, z = loc
    parts = [box(name + "_w", w, d, h, (0, 0, 0), wall), box(name + "_b", w + 0.4, d + 0.4, 0.3, (0, 0, h), SAL_DARK)]
    parts.append(chaitya_roof(name + "_r", w + 0.6, d + 0.8, (d + 0.8) * 0.45, (0, 0, h + 0.3), roof, "x", gables=False))
    parts.append(box(name + "_d", w * 0.18, 0.1, h * 0.65, (0, -d / 2 - 0.02, 0), DARK))
    return _rot_move(join(parts, name), rot_deg, x, y, z)


def _ov(a, b):
    return not (a[2] < b[0] or b[2] < a[0] or a[3] < b[1] or b[3] < a[1])


def scatter(name, seed, n, xr, yr, maker, avoid=(), size=(5, 9), gap=1.6):
    """Place n buildings from maker(name, w, d, x, y, rng) in a rectangle, avoiding rects (x0, y0, x1, y1)."""
    rng = random.Random(seed)
    out, placed = [], list(avoid)
    for _ in range(n * 40):
        if len(out) >= n:
            break
        w, d = rng.uniform(*size), rng.uniform(*size)
        x, y = rng.uniform(xr[0] + w / 2, xr[1] - w / 2), rng.uniform(yr[0] + d / 2, yr[1] - d / 2)
        r = (x - w / 2 - gap, y - d / 2 - gap, x + w / 2 + gap, y + d / 2 + gap)
        if any(_ov(r, a) for a in placed):
            continue
        placed.append(r)
        out.append(maker(f"{name}{len(out)}", w, d, x, y, rng))
    return join(out, name) if out else None


def trees(name, pts, r=3.0, color="#6F8A5C", z=0.0, kind="round"):
    return join([tree(f"{name}{i}", r, (x, y, z), color, kind=kind) for i, (x, y) in enumerate(pts)], name)


def boat(name, L, w, loc, deg=0.0, awning=True, sail=False):
    """A Ganges country boat: a pointed hull with a thatched barrel awning amidships."""
    x, y, z = loc
    hull = [(-L / 2, 0), (-L * 0.32, -w / 2), (L * 0.32, -w / 2), (L / 2, 0), (L * 0.32, w / 2), (-L * 0.32, w / 2)]
    parts = [prism(name + "_h", hull, 0.9, (0, 0, 0), SAL_DARK), box(name + "_in", L * 0.6, w * 0.7, 0.1, (0, 0, 0.85), SAL)]
    if awning:
        parts.append(chaitya_roof(name + "_aw", L * 0.35, w * 0.9, w * 0.55, (0, 0, 0.9), THATCH, "x", gables=False))
    if sail:
        parts.append(cylinder(name + "_m", 0.12, L * 0.7, (L * 0.15, 0, 0.9), SAL_DARK, verts=5))
        parts.append(box(name + "_s", 0.08, w * 1.4, L * 0.4, (L * 0.15, 0, 0.9 + L * 0.25), "#E8DFC8"))
    return _rot_move(join(parts, name), deg, x, y, z)


def water(name, w, d, loc):
    return box(name, w, d, 0.3, loc, WATER)


# ---------------------------------------------------------------- the Mauryan palace (hero)

def mauryan_palace():
    m = Model("mauryan-palace")
    W, D = 240, 170
    m.add(0, box("ground", W, D, 0.3, (0, 0, 0), DUST), "platforms")
    wall = [(-117, -82), (117, -82), (117, 82), (-117, 82), (-117, -82)]
    m.add(0, wall_run("enclosure", wall, 3.2, 1.2, (0, 0, 0.3), BRICKR, towers=False, merlon=None))
    m.add(0, box("court", 150, 64, 0.25, (0, -40, 0.3), shade(DUST, 0.12)))
    # main audience hall on a brick terrace, facing south
    m.add(0, box("terrace", 76, 44, 2.6, (0, 8, 0.3), BRICKR))
    m.add(0, stair("terrace_st", 24, 2.6, 6, 6, (0, -17, 0.3), "S", BRICKR))
    m.add(1, timber_hall("audience", 58, 26, 8.5, (0, 12, 2.9), plinth=0.6, roof=TILE, roof_h=14, finials=5, door="S"), "halls")
    # front veranda of polished stone pillars with bell capitals
    for i in range(12):
        px = -27.5 + i * 5.0
        m.add(2, mauryan_pillar(f"vp{i}", 7.2, 0.42, (px, -5.5, 2.9), POLISH, crown=None), "pillars and roofs")
    m.add(2, box("veranda_roof", 62, 6.5, 0.6, (0, -3.5, 2.9 + 7.2 + 0.9), SAL_DARK))
    for i, gx in enumerate((-20, 0, 20)):
        m.add(2, chaitya_roof(f"gable{i}", 8, 11 if gx else 13, 8 if gx else 10, (gx, -3.8, 2.9 + 8.6), TILE, "y", finials=1))
    # side halls with their horseshoe gables to the court
    for s in (-1, 1):
        m.add(1, timber_hall(f"side{s}", 22, 44, 7, (s * 84, 8, 0.3), plinth=1.6, roof=THATCH, axis="y", finials=3, door="S"))
    # the many-storeyed pleasure pavilion behind
    zz = 0.3
    m.add(1, box("prasada_pl", 30, 22, 2.0, (0, 58, zz), BRICKR))
    zz += 2.0
    for k, (sw, sd, sh) in enumerate(((22, 15, 6.0), (16, 11, 5.0), (11, 8, 4.0))):
        m.add(1, box(f"pr{k}", sw, sd, sh, (0, 58, zz), LIME if k % 2 == 0 else SAL_LT))
        m.add(1, arcade(f"pra{k}", sw * 0.8, sh * 0.6, 4 + k, (0, 58 - sd / 2 - 0.05, zz), "S", DARK, False))
        m.add(2, box(f"pre{k}", sw + 2.4, sd + 2.4, 0.4, (0, 58, zz + sh), SAL_DARK))
        zz += sh + 0.4
    m.add(2, chaitya_roof("prasada_r", 12, 9.5, 6.5, (0, 58, zz), TILE, "y", finials=1))
    for s in (-1, 1):
        m.add(2, chaitya_roof(f"pr_wing{s}", 7, 6, 4, (s * 13.5, 58, 2.3 + 6.4), TILE, "y"))
    # south gate pavilion
    m.add(1, box("gate_b", 18, 9, 5, (0, -82, 0.3), BRICKR))
    m.add(1, arch_panel("gate_a", 5, 4.4, (0, -86.6, 0.3), "S", DARK, False))
    m.add(1, box("gate_up", 15, 7.5, 3.4, (0, -82, 5.3), SAL_LT))
    m.add(2, chaitya_roof("gate_r", 9, 17, 7.5, (0, -82, 8.7), TILE, "y", finials=1))
    # fishponds, parks and trees
    for s in (-1, 1):
        m.add(3, box(f"pond_rim{s}", 34, 20, 0.6, (s * 58, -46, 0.3), BRICKR), "parks and ponds")
        m.add(3, box(f"pond{s}", 31, 17, 0.7, (s * 58, -46, 0.3), WATER))
        m.add(3, chaitya_roof(f"pond_kiosk{s}", 5, 5, 3.4, (s * 58, -46, 4.1), THATCH, "y"))
        m.add(3, posts_mesh(f"pond_kp{s}", [(s * 58 + a, -46 + b, 1.0) for a in (-2, 2) for b in (-2, 2)], 0.2, 3.1, SAL, 6, 0.0, 0.0))
        m.add(3, trees(f"pt{s}", [(s * 58 + dx, -46 + dy) for dx, dy in ((-22, -12), (-22, 12), (22, -12), (22, 12), (0, 15), (-10, -15), (10, -15))], 3.2, z=0.3))
    m.add(3, trees("park", [(x, y) for x in (-100, -82, -64, -46, 46, 64, 82, 100) for y in (50, 68)] + [(-30, 75), (30, 75), (-104, -20), (104, -20), (-104, -60), (104, -60)], 3.6, z=0.3))
    m.add(3, box("lawn_w", 70, 40, 0.15, (-75, 58, 0.3), LAWN))
    m.add(3, box("lawn_e", 70, 40, 0.15, (75, 58, 0.3), LAWN))
    return m


# ---------------------------------------------------------------- the 80-pillared hall at Kumhrar (hero)

HALL_Y = 14.0
COLS_X = [-20.7 + 4.6 * i for i in range(10)]
COLS_Y = [HALL_Y - 16.1 + 4.6 * j for j in range(8)]


def _hall_base(m):
    m.add(0, box("ground", 60, 80, 0.3, (0, 0, 0), DUST), "floor and landing")
    m.add(0, box("floor", 49, 40, 0.9, (0, HALL_Y, 0.3), BRICKR))
    m.add(0, box("floor_top", 47, 38, 0.1, (0, HALL_Y, 1.2), LIME))
    # the timber landing stages Spooner found south of the hall, stepping down to a canal
    for k in range(7):
        m.add(0, box(f"stage{k}", 24, 2.6, 1.15 - k * 0.14, (0, HALL_Y - 21.3 - k * 2.6, 0.3), SAL if k % 2 == 0 else SAL_LT))
    m.add(0, box("canal_rev", 60, 9, 0.35, (0, -36.5, 0.0), BRICKR))
    m.add(0, water("canal", 60, 7, (0, -36.5, 0.05)))


def pillared_hall():
    m = Model("pillared-hall")
    _hall_base(m)
    H = 9.4
    for i, cx in enumerate(COLS_X):
        for j, cy in enumerate(COLS_Y):
            m.add(1, lathe(f"col{i}_{j}", [(0.5, 0), (0.48, 0.3), (0.46, 0.4), (0.43, H * 0.6), (0.39, H)], (cx, cy, 1.3), POLISH, verts=14), "columns")
            m.add(1, box(f"cap{i}_{j}", 1.1, 1.1, 0.35, (cx, cy, 1.3 + H), SAL))
    zt = 1.3 + H + 0.35
    for j, cy in enumerate(COLS_Y):
        m.add(2, box(f"beamx{j}", 46, 0.5, 0.55, (0, cy, zt), SAL_DARK), "beams")
    for i, cx in enumerate(COLS_X):
        m.add(2, box(f"beamy{i}", 0.5, 37.5, 0.5, (cx, HALL_Y, zt + 0.55), SAL_DARK))
    # timber railing (vedika) round the floor
    rail = []
    for (ax, ay), (bx, by) in (((-24, HALL_Y - 19.5), (24, HALL_Y - 19.5)), ((24, HALL_Y - 19.5), (24, HALL_Y + 19.5)), ((24, HALL_Y + 19.5), (-24, HALL_Y + 19.5)), ((-24, HALL_Y + 19.5), (-24, HALL_Y - 19.5))):
        rail += [p for p in line_pts((ax, ay), (bx, by), 1.1, 1.3) if not (ay == by == HALL_Y - 19.5 and abs(p[0]) < 12)]
    m.add(2, posts_mesh("vedika", rail, 0.12, 1.1, SAL_LT, 4, 0.0, 0.0))
    for s, (w, d, x, y) in enumerate(((48, 0.2, 0, HALL_Y + 19.5), (0.2, 39, 24, HALL_Y), (0.2, 39, -24, HALL_Y))):
        m.add(2, box(f"vrail{s}", w, d, 0.18, (x, y, 2.3), SAL_LT))
    # roof: a central pointed barrel over the middle rows, lean-to roofs over the outer rows
    zr = zt + 1.05
    m.add(3, box("ceiling", 48, 39, 0.3, (0, HALL_Y, zr), SAL), "roof")
    m.add(3, chaitya_roof("nave", 48.5, 20, 10, (0, HALL_Y, zr + 0.3), TILE, "x", finials=7))
    for s in (-1, 1):
        y_in, y_out = HALL_Y + s * 9.6, HALL_Y + s * 20.6
        verts = [(-24.2, y_in, zr + 3.4), (24.2, y_in, zr + 3.4), (24.2, y_out, zr + 0.3), (-24.2, y_out, zr + 0.3),
                 (-24.2, y_in, zr + 3.1), (24.2, y_in, zr + 3.1), (24.2, y_out, zr), (-24.2, y_out, zr)]
        faces = [(0, 1, 2, 3), (7, 6, 5, 4), (0, 4, 5, 1), (1, 5, 6, 2), (2, 6, 7, 3), (3, 7, 4, 0)]
        m.add(3, mesh_from(f"aisle{s}", verts, faces, (0, 0, 0), shade(TILE, 0.06)))
        for k in range(24):
            rx = -23 + k * 2.0
            rv = [(rx - 0.14, y_in, zr + 3.4), (rx + 0.14, y_in, zr + 3.4), (rx + 0.14, y_out, zr + 0.3), (rx - 0.14, y_out, zr + 0.3)]
            rv += [(a, b, c + 0.16) for a, b, c in rv]
            m.add(3, mesh_from(f"rib{s}_{k}", rv, faces, (0, 0, 0), shade(TILE, -0.15)))
    # porch toward the landing stages
    m.add(3, chaitya_roof("porch", 7, 12, 7.5, (0, HALL_Y - 19.5, zr - 0.2), TILE, "y", finials=1))
    for s in (-1, 1):
        m.add(1, mauryan_pillar(f"porchcol{s}", zr - 1.5, 0.38, (s * 4.6, HALL_Y - 21.5, 1.3), POLISH, crown=None))
    return m


def pillared_hall_ruin():
    m = Model("pillared-hall-ruin")
    _hall_base(m)
    rng = random.Random(7)
    m.add(1, box("ash", 46, 37, 0.25, (0, HALL_Y, 1.25), ASH), "stumps")
    for i, cx in enumerate(COLS_X):
        for j, cy in enumerate(COLS_Y):
            if rng.random() < 0.18:
                continue
            h = rng.uniform(0.4, 2.6) if rng.random() > 0.06 else rng.uniform(5, 7)
            m.add(1, lathe(f"stump{i}_{j}", [(0.5, 0), (0.47, h * 0.9), (0.4, h)], (cx, cy, 1.3), shade(POLISH, -0.08), verts=12))
    for k in range(9):
        x, y = rng.uniform(-20, 20), rng.uniform(HALL_Y - 15, HALL_Y + 15)
        L = rng.uniform(4, 8)
        drum = _arch_prism(f"fallen{k}", [(0.42 * math.cos(a), 0.42 + 0.42 * math.sin(a)) for a in [math.tau * t / 10 for t in range(10)]], -L / 2, L / 2, shade(POLISH, -0.1))
        m.add(2, _rot_move(drum, rng.uniform(0, 180), x, y, 1.3), "fallen and burnt")
    for k in range(16):
        x, y = rng.uniform(-22, 22), rng.uniform(HALL_Y - 17, HALL_Y + 17)
        m.add(2, box(f"beam{k}", rng.uniform(3, 9), 0.45, 0.4, (x, y, 1.3), "#2F2A25", rot_z=rng.uniform(0, math.pi)))
    for k in range(6):
        x, y = rng.uniform(-25, 25), rng.uniform(-28, 36)
        m.add(3, frustum(f"silt{k}", rng.uniform(8, 14), rng.uniform(6, 10), 3, 2, rng.uniform(0.8, 1.6), (x, y, 0.3), SILT), "silt and scrub")
    m.add(3, trees("scrub", [(-26, 34), (26, 30), (-27, -4), (25, -12), (8, 37)], 2.2, z=0.3))
    return m


# ---------------------------------------------------------------- the palisade at Bulandi Bagh (hero)

def palisade():
    m = Model("palisade")
    m.add(0, box("ground", 260, 70, 0.3, (0, 0, 0), DUST), "ditch")
    m.add(0, box("berm", 260, 4, 0.5, (0, -12, 0.3), EARTH))
    m.add(0, box("ditch_bank", 260, 20, 0.15, (0, -24, 0.0), SILT))
    m.add(0, water("ditch", 260, 17, (0, -24, 0.05)))
    m.add(0, box("street", 260, 7, 0.12, (0, 8.5, 0.3), shade(DUST, 0.1)))
    # double row of sal posts with a walkway, broken by towers and a gate
    towers = [-120, -80, -40, 40, 80, 120]
    gate_w = 10
    segs = []
    edges = [-130] + sorted(sum([[t - 4.5, t + 4.5] for t in towers], []) + [-gate_w / 2 - 6, gate_w / 2 + 6]) + [130]
    for a, b in zip(edges[::2], edges[1::2]):
        if b - a > 1:
            segs.append((a, b))
    for k, (a, b) in enumerate(segs):
        m.add(1, palisade_x(f"pal{k}", a, b, 0.0, 5.2, 4.5, 0.6, 0.3, seed=k + 3), "palisade")
    for k, tx in enumerate(towers):
        m.add(2, timber_tower(f"tw{k}", 8, 10.5, (tx, 0, 0.3), THATCH, "y"), "towers and gate")
    # the gate: two towers joined by a gallery with a horseshoe gable to the ditch, and a bridge
    for s in (-1, 1):
        m.add(2, timber_tower(f"gt{s}", 8, 12, (s * (gate_w / 2 + 4), 0, 0.3), TILE, "y"))
    m.add(2, box("gallery", gate_w + 2, 7, 3.2, (0, 0, 8.5), SAL))
    m.add(2, arcade("gallery_w", gate_w, 2.2, 3, (0, -3.55, 8.9), "S", DARK, False))
    m.add(2, chaitya_roof("gallery_r", 8, gate_w + 3, 6, (0, 0, 11.7), TILE, "y", finials=1))
    m.add(2, box("bridge", 5, 22, 0.5, (0, -22, 1.2), SAL_LT))
    m.add(2, posts_mesh("bridge_p", [(sx, y, 0.0) for sx in (-2.2, 2.2) for y in (-31, -25, -19, -13)], 0.2, 1.2, SAL_DARK, 5, 0.0, 0.0))
    # houses of the quarter behind the wall
    mk = lambda nm, w, d, x, y, rng: barrel_house(nm, w, d, rng.uniform(3.2, 5.5), (x, y, 0.3), rng.choice(HOUSE_COLORS), rng.choice([THATCH, TILE, THATCH]))
    m.add(3, scatter("houses", 11, 46, (-128, 128), (13, 34), mk, avoid=[(-8, 10, 8, 35)], size=(5, 9)), "quarter behind the wall")
    m.add(3, trees("tr", [(-100, 31), (-35, 33), (25, 32), (95, 33)], 3.0, z=0.3))
    return m


# ---------------------------------------------------------------- the south gate

def city_gate():
    m = Model("city-gate")
    m.add(0, box("ground", 70, 60, 0.3, (0, 0, 0), DUST), "ditch and bridge")
    m.add(0, box("road", 7, 60, 0.12, (0, 0, 0.3), shade(DUST, 0.12)))
    m.add(0, box("ditch_bank", 70, 16, 0.15, (0, -21, 0.0), SILT))
    m.add(0, water("ditch", 70, 13, (0, -21, 0.05)))
    m.add(0, box("bridge", 6, 20, 0.5, (0, -20, 1.2), SAL_LT))
    m.add(0, posts_mesh("bridge_p", [(sx, y, 0.0) for sx in (-2.6, 2.6) for y in (-28, -22, -16, -11)], 0.22, 1.2, SAL_DARK, 5, 0.0, 0.0))
    for s in (-1, 1):
        m.add(1, palisade_x(f"pal{s}", s * 14, s * 35, 0.0, 5.2, 4.5, 0.6, 0.3, seed=5 + s), "palisade")
        m.add(2, timber_tower(f"tw{s}", 10, 13, (s * 9, 0, 0.3), TILE, "y"), "gate towers")
        m.add(2, lathe(f"pot{s}", [(0, 0), (0.6, 0.2), (0.8, 0.9), (0.4, 1.5), (0.5, 1.7), (0, 1.75)], (s * 4.6, -6.5, 0.3), BRICKR, verts=10))
    m.add(2, box("gallery", 9, 8, 3.6, (0, 0, 9.0), SAL))
    m.add(2, arcade("gallery_w", 7, 2.6, 3, (0, -4.05, 9.4), "S", DARK, False))
    m.add(2, box("lintel", 9, 8.4, 0.6, (0, 0, 8.4), SAL_DARK))
    m.add(3, chaitya_roof("gallery_r", 9, 10, 7, (0, 0, 12.6), TILE, "y", finials=1), "roof")
    m.add(3, box("guardhouse", 8, 6, 3, (-14, 13, 0.3), LIME))
    m.add(3, chaitya_roof("guardhouse_r", 8.6, 6.8, 3.4, (-14, 13, 3.3), THATCH, "x", gables=False))
    m.add(3, trees("tr", [(20, 16), (28, 22), (-26, 22)], 3.0, z=0.3))
    return m


# ---------------------------------------------------------------- Pataligama

def pataligama():
    m = Model("pataligama")
    W, D = 280, 180
    m.add(0, box("ground", 300, 200, 0.3, (0, 0, 0), DUST), "rampart")
    for nm, w0, d0, w1, d1, x, y in (("rs", W + 10, 10, W + 4, 4, 0, -D / 2), ("rn", W + 10, 10, W + 4, 4, 0, D / 2),
                                     ("rw", 10, D - 10, 4, D - 10, -W / 2, 0), ("re", 10, D - 10, 4, D - 10, W / 2, 0)):
        m.add(0, frustum(nm, w0, d0, w1, d1, 4.0, (x, y, 0.3), EARTH))
    m.add(0, box("ditch_s", W + 18, 6, 0.1, (0, -D / 2 - 7.5, 0.3), "#7A6A55"))
    pts = []
    for (ax, ay), (bx, by) in (((-W / 2, -D / 2), (W / 2, -D / 2)), ((W / 2, -D / 2), (W / 2, D / 2)), ((W / 2, D / 2), (-W / 2, D / 2)), ((-W / 2, D / 2), (-W / 2, -D / 2))):
        pts += [p for p in line_pts((ax, ay), (bx, by), 1.25, 4.3) if not (abs(p[0]) < 9 and abs(abs(p[1]) - D / 2) < 1)]
    m.add(1, posts_mesh("stockade", pts, 0.22, 3.4, SAL, 5, 0.4, 0.1, seed=4), "stockade")
    for k, (tx, ty) in enumerate(((-W / 2, -D / 2), (W / 2, -D / 2), (W / 2, D / 2), (-W / 2, D / 2))):
        m.add(1, timber_tower(f"ct{k}", 7, 9, (tx, ty, 2.3), THATCH, "y", footing=EARTH))
    for f, gy in (("S", -D / 2), ("N", D / 2)):
        for s in (-1, 1):
            m.add(1, timber_tower(f"g{f}{s}", 6, 9, (s * 8, gy, 2.3), THATCH, "y", footing=EARTH))
        m.add(1, box(f"g{f}_lintel", 11, 5, 1.2, (0, gy, 8.0), SAL))
    # inside: the hall, granaries and huts
    m.add(2, timber_hall("hall", 26, 14, 5.5, (0, 30, 0.3), plinth=1.0, roof=THATCH, finials=3), "town")
    for k, gx in enumerate((-70, -55)):
        m.add(2, posts_mesh(f"gran_p{k}", [(gx + a, 50 + b, 0.3) for a in (-4, 0, 4) for b in (-3, 3)], 0.25, 2.0, SAL, 5, 0.0, 0.0))
        m.add(2, box(f"gran{k}", 10, 8, 3, (gx, 50, 2.3), EARTH))
        m.add(2, chaitya_roof(f"gran_r{k}", 10.6, 8.8, 4, (gx, 50, 5.3), THATCH, "x", gables=False))
    m.add(2, cylinder("well", 2.0, 0.8, (20, 0, 0.3), BRICKR, verts=12))
    m.add(2, cylinder("well_w", 1.4, 0.85, (20, 0, 0.3), WATER, verts=12))
    mk = lambda nm, w, d, x, y, rng: hut(nm, w, d, rng.uniform(2.4, 3.4), (x, y, 0.3), rng.choice([EARTH, "#BFA27C", "#C9AE88"]), THATCH, rng.choice([0, 90]))
    m.add(3, scatter("huts", 21, 70, (-128, 128), (-80, 80), mk, avoid=[(-16, 20, 16, 40), (-78, 42, -48, 58), (16, -4, 24, 4), (-10, -90, 10, -70), (-10, 70, 10, 90)], size=(4, 7), gap=2.5), "huts")
    m.add(3, trees("tr", [(-110, 60), (100, 60), (110, -50), (-100, -55), (40, 70), (-30, -60)], 3.4, z=0.3))
    return m


# ---------------------------------------------------------------- the river harbour

def harbour():
    m = Model("harbour")
    m.add(0, box("bank", 220, 37, 3.4, (0, -26.5, 0), EARTH), "bank and ghat")
    m.add(0, box("bank_top", 220, 36, 0.15, (0, -26.5, 3.4), DUST))
    m.add(0, water("river", 220, 37, (0, 26.5, 0.0)))
    for k in range(10):
        dep = 1.9 * (10 - k)
        m.add(0, box(f"ghat{k}", 110, dep, 3.4 * (10 - k) / 10, (0, -8 + dep / 2, 0), BRICKR if k % 2 else shade(BRICKR, 0.1)))
    for s in (-1, 1):
        verts = [(s * 55, -8, 3.4), (s * 110, -8, 3.4), (s * 110, 11, 0.3), (s * 55, 11, 0.3), (s * 55, -8, 0), (s * 110, -8, 0), (s * 110, 11, 0), (s * 55, 11, 0)]
        faces = [(0, 1, 2, 3), (4, 7, 6, 5), (0, 4, 5, 1), (1, 5, 6, 2), (2, 6, 7, 3), (3, 7, 4, 0)]
        m.add(0, mesh_from(f"slope{s}", verts, faces, (0, 0, 0), SILT))
    for k, jx in enumerate((-82, 80, 98)):
        m.add(1, posts_mesh(f"jet_p{k}", [(jx + a, y, 0.0) for a in (-1.6, 1.6) for y in range(12, 40, 4)], 0.22, 1.5, SAL_DARK, 5, 0.0, 0.0), "jetties and boats")
        m.add(1, box(f"jet{k}", 4.2, 30, 0.35, (jx, 25, 1.5), SAL_LT))
    rng = random.Random(9)
    for k, (bx, by, deg, sail) in enumerate(((-70, 22, 90, False), (-94, 26, 88, True), (68, 20, 92, False), (88, 30, 90, True), (-30, 18, 5, False),
                                               (-10, 30, 0, True), (20, 22, -8, False), (45, 36, 3, True), (-52, 38, 12, False))):
        L = rng.uniform(10, 16)
        m.add(1, boat(f"boat{k}", L, L * 0.28, (bx, by, 0.1), deg, True, sail))
    for k, wx in enumerate((-85, -50, 50, 85)):
        m.add(2, box(f"wh{k}", 26, 10, 4.2, (wx, -30, 3.5), LIME if k % 2 else "#D6BC94"), "warehouses")
        m.add(2, chaitya_roof(f"wh_r{k}", 26.8, 11.2, 5, (wx, -30, 7.7), THATCH, "x", finials=2))
        m.add(2, arcade(f"wh_a{k}", 22, 3.0, 5, (wx, -24.95, 3.5), "N", DARK, False))
    for k in range(18):
        m.add(2, box(f"bale{k}", 1.6, 1.2, 1.0, (rng.uniform(-40, 40), rng.uniform(-22, -12), 3.5), rng.choice(["#E3D6B8", "#B39A5E", "#C9A47A"])))
    m.add(2, timber_hall("toll", 12, 8, 4, (0, -36, 3.5), plinth=0.5, roof=TILE, finials=1, door="N"))
    m.add(3, trees("tr", [(-108, -40), (-30, -42), (30, -42), (108, -40), (-66, -14), (66, -14)], 3.3, z=3.5), "trees")
    return m


# ---------------------------------------------------------------- Ashoka's pillar, stupa and well

def ashoka_pillar():
    m = Model("ashoka-pillar")
    m.add(0, cylinder("ground", 3.0, 0.2, (0, 0, 0), DUST, verts=20), "base")
    m.add(0, box("slab", 2.0, 2.0, 0.3, (0, 0, 0.2), shade(POLISH, -0.12)))
    m.add(1, lathe("shaft", [(0.5, 0), (0.49, 2.0), (0.47, 6.0), (0.44, 9.0), (0.4, 12.2)], (0, 0, 0.5), POLISH, verts=32), "shaft")
    m.add(0, posts_mesh("rail", [(2.6 * math.cos(math.tau * k / 36), 2.6 * math.sin(math.tau * k / 36), 0.2) for k in range(36)], 0.07, 0.9, SAL_LT, 6, 0.1, 0.0))
    m.add(0, lathe("railtop", [(2.68, 0), (2.68, 0.1), (2.52, 0.1), (2.52, 0)], (0, 0, 1.0), SAL_LT, verts=36, cap_top=False, cap_bottom=False))
    cap = mauryan_pillar("cap_src", 0.01, 0.45, (0, 0, 12.7), POLISH, "lion", "S")
    m.add(2, cap, "capital and lion")
    return m


def ashoka_stupa():
    m = Model("ashoka-stupa")
    m.add(0, box("ground", 40, 40, 0.3, (0, 0, 0), DUST), "drum")
    m.add(0, cylinder("pave", 17.5, 0.3, (0, 0, 0.3), shade(BRICKR, 0.2), verts=40))
    s = stupa("stupa", 11, (0, 0, 0.6), "#EDE6D6", drum=0.28, rail=True, gateways=4, harmika=True, umbrellas=3, base_color=BRICKR)
    m.add(1, s, "dome and railing")
    m.add(2, box("footprint", 1.6, 2.6, 0.35, (0, -12.8, 0.6), shade(POLISH, -0.15)), "offerings")
    for k in range(8):
        a = math.tau * (k + 0.5) / 8
        m.add(2, cylinder(f"lamp{k}", 0.25, 1.4, (14.5 * math.cos(a), 14.5 * math.sin(a), 0.6), BRICKR, verts=6))
    m.add(2, trees("tr", [(-17, 17), (17, 17), (-17, -17), (17, -17)], 2.4, z=0.3))
    for k in range(8):
        a = math.tau * (k + 0.5) / 8
        m.add(2, stupa(f"votive{k}", 0.9, (17.6 * math.cos(a) * 0.98, 17.6 * math.sin(a) * 0.98, 0.3), "#E4DCCB", rail=False, umbrellas=1, base_color=BRICKR) if k % 2 else box(f"votive{k}", 1.2, 1.2, 1.0, (17.6 * math.cos(a), 17.6 * math.sin(a), 0.3), BRICKR))
    m.add(1, lathe("anda_band", [(11.05, 0), (11.05, 0.5), (10.98, 0.5)], (0, 0, 0.6 + 11 * 0.28 + 0.6), BRICKR, verts=48, cap_top=False, cap_bottom=False))
    m.add(2, posts_mesh("flags", [(1.6 * math.cos(math.tau * k / 6), 1.6 * math.sin(math.tau * k / 6), 0.6 + 11 * 1.2) for k in range(6)], 0.05, 1.6, SAL_DARK, 4, 0.0, 0.0))
    return m


def agam_kuan():
    m = Model("agam-kuan")
    m.add(0, box("ground", 28, 28, 0.3, (0, 0, 0), DUST), "platform")
    m.add(0, cylinder("plat", 7.8, 0.8, (0, 0, 0.3), shade(BRICKR, 0.1), verts=24))
    m.add(0, stair("steps", 4, 0.8, 2, 3, (0, -9, 0.3), "S", BRICKR))
    m.add(1, cylinder("drum", 5.5, 3.8, (0, 0, 1.1), BRICKR, verts=24), "well-house")
    for k in range(8):
        a = math.tau * k / 8
        p = arch_panel(f"win{k}", 1.6, 2.6, (0, 0, 0), "S", DARK, False, 0.4)
        p = rot(p, math.degrees(a) + 90)
        m.add(1, move(p, 5.52 * math.cos(a), 5.52 * math.sin(a), 1.6))
    m.add(1, cylinder("cornice", 6.0, 0.4, (0, 0, 4.9), shade(BRICKR, -0.1), verts=24))
    m.add(2, cylinder("roof", 6.2, 2.6, (0, 0, 5.3), TILE, verts=48, r_top=0.8), "roof")
    m.add(2, lathe("finial", [(0.0, 0), (0.6, 0.1), (0.7, 0.5), (0.3, 0.9), (0.15, 1.4), (0, 1.6)], (0, 0, 7.9), GILT, verts=10))
    # the little Shitala Devi shrine beside the well
    m.add(2, box("shrine", 4, 4, 2.6, (-9, 7, 0.3), WHITEWASH))
    m.add(2, frustum("shrine_t", 4, 4, 1.0, 1.0, 3.2, (-9, 7, 2.9), WHITEWASH))
    m.add(2, cylinder("shrine_k", 0.7, 0.4, (-9, 7, 6.1), GILT, verts=8))
    m.add(2, box("shrine_d", 1.0, 0.1, 1.7, (-9, 4.95, 0.3), DARK))
    m.add(3, trees("tr", [(9, 9), (-10, -9), (10, -10), (-11, 11), (11, 0)], 2.6, z=0.3), "trees")
    m.add(1, posts_mesh("rail", [(7.4 * math.cos(math.tau * k / 60), 7.4 * math.sin(math.tau * k / 60), 1.1) for k in range(60) if not (k > 42 and k < 48)], 0.09, 0.9, BRICKR, 6, 0.1, 0.0))
    for k in range(3):
        m.add(1, lathe(f"course{k}", [(5.56, 0), (5.56, 0.18), (5.5, 0.18)], (0, 0, 1.4 + k * 1.15), shade(BRICKR, -0.15), verts=48, cap_top=False, cap_bottom=False))
    for k in range(10):
        a = math.tau * k / 10
        m.add(3, lathe(f"lamp{k}", [(0, 0), (0.25, 0.05), (0.3, 0.2), (0.12, 0.3), (0, 0.32)], (6.6 * math.cos(a), 6.6 * math.sin(a), 1.1), "#C98A55", verts=10))
    return m


# ---------------------------------------------------------------- monasteries, hospital, temple

def vihara(name, w, d, h, loc, color=BRICKR):
    """A brick monastery: a plinth, cells round an open court with a veranda, a gate on the south."""
    x, y, z = loc
    parts = [box(name + "_pl", w + 3, d + 3, 0.9, (x, y, z), shade(color, -0.08))]
    parts.append(courtyard_ring(name + "_ring", w, d, h, 7, (x, y, z + 0.9), color, DARK, True))
    parts.append(box(name + "_court", w - 14, d - 14, 0.1, (x, y, z + 0.9), shade(DUST, 0.1)))
    vp = []
    for (ax, ay), (bx, by) in (((-w / 2 + 8, -d / 2 + 8), (w / 2 - 8, -d / 2 + 8)), ((w / 2 - 8, -d / 2 + 8), (w / 2 - 8, d / 2 - 8)), ((w / 2 - 8, d / 2 - 8), (-w / 2 + 8, d / 2 - 8)), ((-w / 2 + 8, d / 2 - 8), (-w / 2 + 8, -d / 2 + 8))):
        vp += line_pts((x + ax, y + ay), (x + bx, y + by), 3.0, z + 0.9)
    parts.append(posts_mesh(name + "_vp", vp, 0.2, h - 0.6, SAL, 6, 0.0, 0.0))
    W2, D2 = w - 14.5, d - 14.5
    for nm, bw, bd, bx, by in (("s", W2 + 3, 2.0, 0, -D2 / 2 - 0.5), ("n", W2 + 3, 2.0, 0, D2 / 2 + 0.5), ("w", 2.0, D2, -W2 / 2 - 0.5, 0), ("e", 2.0, D2, W2 / 2 + 0.5, 0)):
        parts.append(box(f"{name}_ver{nm}", bw, bd, 0.3, (x + bx, y + by, z + 0.9 + h - 0.6), TILE))
    parts.append(box(name + "_roof", w + 0.6, d + 0.6, 0.5, (x, y, z + 0.9 + h), shade(color, -0.12)))
    parts.append(box(name + "_gate", 10, 9, h + 2.2, (x, y - d / 2, z + 0.9), color))
    parts.append(arch_panel(name + "_gatea", 3.4, h, (x, y - d / 2 - 4.55, z + 0.9), "S", DARK, False))
    parts.append(chaitya_roof(name + "_gater", 9.5, 10.6, 5.2, (x, y - d / 2, z + 0.9 + h + 2.2), TILE, "y", finials=1))
    return join(parts, name)


def kukkutarama():
    m = Model("kukkutarama")
    m.add(0, box("ground", 110, 90, 0.3, (0, 0, 0), DUST), "monastery")
    m.add(1, vihara("vihara", 56, 56, 5.5, (-14, -8, 0.3)), "monastery")
    m.add(2, stupa("court_stupa", 4.2, (-14, -8, 1.3), "#EDE6D6", rail=False, umbrellas=2, base_color=BRICKR), "stupa and shrine")
    m.add(2, timber_hall("shrine", 12, 18, 6, (-14, 32, 0.3), plinth=1.4, plinth_color=BRICKR, wall=LIME, roof=TILE, axis="y", finials=2, door="S"))
    m.add(3, box("tank_rim", 24, 34, 0.7, (36, -6, 0.3), BRICKR), "tank and grove")
    m.add(3, box("tank", 21, 31, 0.75, (36, -6, 0.3), WATER))
    m.add(3, stair("tank_st", 5, 0.7, 2, 3, (36, -24, 0.3), "S", BRICKR))
    m.add(3, trees("tr", [(36, 22), (48, 30), (24, 32), (52, -30), (20, -34), (-48, 30), (-48, -38), (10, 36)], 3.6, z=0.3))
    return m


def arogya_vihara():
    m = Model("arogya-vihara")
    m.add(0, box("ground", 70, 56, 0.3, (0, 0, 0), DUST), "hospital")
    m.add(1, vihara("vihara", 42, 38, 4.6, (-6, -2, 0.3), "#C49072"), "hospital")
    m.add(2, cylinder("well", 1.5, 1.0, (-6, -2, 1.2), BRICKR, verts=12), "court and garden")
    m.add(2, cylinder("well_w", 1.0, 1.05, (-6, -2, 1.2), WATER, verts=12))
    m.add(2, timber_hall("pharmacy", 10, 7, 3.6, (24, 12, 0.3), plinth=0.6, roof=THATCH, finials=1, door="W"))
    for k in range(6):
        m.add(2, box(f"bed{k}", 3.2, 7, 0.4, (19 + (k % 3) * 4.6, -12 - (k // 3) * 8.5, 0.3), "#6E8A57"))
    m.add(2, stupa("small_stupa", 2.4, (24, -2, 0.3), "#EDE6D6", rail=False, umbrellas=1, base_color=BRICKR))
    m.add(3, trees("tr", [(31, 24), (-30, 24), (-31, -24), (31, -26), (14, 24), (-32, 0), (32, 4), (0, 25), (-18, -25), (6, -25)], 3.0, z=0.3), "trees")
    for k in range(12):
        m.add(3, lathe(f"pot{k}", [(0, 0), (0.35, 0.05), (0.45, 0.4), (0.25, 0.7), (0.3, 0.8), (0, 0.8)], (18 + (k % 6) * 2.4, -27.0 + (k // 6) * 1.6, 0.3), "#B0704C", verts=8))
    return m


def gupta_temple():
    """A Bhitargaon-type brick temple facing east: stepped plinth, sanctum, a tiered tower of chaitya niches, a porch."""
    m = Model("gupta-temple")
    m.add(0, box("ground", 60, 40, 0.3, (0, 0, 0), DUST), "plinth")
    for k, (w, d, h) in enumerate(((34, 26, 1.2), (30, 22, 1.2), (26, 18, 1.0))):
        m.add(0, box(f"plinth{k}", w, d, h, (-2, 0, 0.3 + k * 1.2), BRICKR if k % 2 == 0 else shade(BRICKR, 0.1)))
    zb = 0.3 + 3.4
    m.add(0, stair("steps", 6, 3.4, 6, 8, (14, 0, 0.3), "E", BRICKR))
    m.add(1, box("sanctum", 11, 11, 7, (-5, 0, zb), BRICKR), "sanctum and tower")
    for f, (dx, dy) in (("N", (0, 5.55)), ("S", (0, -5.55)), ("W", (-5.55, 0))):
        m.add(1, arch_panel(f"niche{f}", 2.6, 4.2, (-5 + dx, dy, zb + 1.2), f, "#7D4632", False))
    z = zb + 7
    for k in range(6):
        s = 11.6 - k * 1.5
        m.add(1, box(f"tier{k}", s, s, 1.9, (-5, 0, z), BRICKR if k % 2 == 0 else shade(BRICKR, -0.06)))
        for f, (dx, dy) in (("S", (0, -s / 2 - 0.05)), ("N", (0, s / 2 + 0.05)), ("E", (s / 2 + 0.05, 0)), ("W", (-s / 2 - 0.05, 0))):
            for q in (-1, 0, 1):
                ox, oy = (q * s * 0.3, 0) if f in "SN" else (0, q * s * 0.3)
                m.add(2, arch_panel(f"chn{k}{f}{q}", s * (0.18 if q == 0 else 0.11), 1.5 if q == 0 else 1.1, (-5 + dx + ox, dy + oy, z + 0.15), f, "#6E3E2C", False, 0.2))
        z += 1.9
    m.add(2, lathe("amalaka", [(0.3, 0), (2.0, 0.3), (2.2, 0.9), (1.6, 1.4), (0.5, 1.6), (0.4, 2.2), (0.8, 2.5), (0, 3.4)], (-5, 0, z), shade(BRICKR, 0.05), verts=20), "amalaka and porch")
    m.add(2, box("porch", 8, 9, 0.5, (5.5, 0, zb + 4.6), BRICKR))
    for sx in (2.2, 8.8):
        for sy in (-3.6, 3.6):
            m.add(2, cylinder(f"porchcol{sx}{sy}", 0.4, 4.6, (sx, sy, zb), shade(BRICKR, 0.15), verts=8))
    m.add(2, arch_panel("door", 2.8, 4.6, (0.55, 0, zb), "E", DARK, False))
    m.add(3, trees("tr", [(-24, 15), (-24, -15), (22, 15), (22, -15)], 2.8, z=0.3), "trees")
    m.add(3, wall_run("compound", [(26, 4), (26, 18), (-28, 18), (-28, -18), (26, -18), (26, -4)], 2.2, 0.8, (0, 0, 0.3), BRICKR, towers=False, merlon=None))
    for k in range(20):
        m.add(1, box(f"panel{k}", 1.0, 0.12, 0.8, (-14 + k * 1.25, -13.06, 1.0), "#C57E5C" if k % 2 else "#9E5A40"))
        m.add(1, box(f"paneln{k}", 1.0, 0.12, 0.8, (-14 + k * 1.25, 13.06, 1.0), "#C57E5C" if k % 2 else "#9E5A40"))
    return m


# ---------------------------------------------------------------- Sher Shah's Patna

def patna_fort():
    m = Model("patna-fort")
    W, D = 300, 220
    m.add(0, box("ground", 320, 240, 0.3, (0, 0, 0), DUST), "walls")
    pts = [(-W / 2, -D / 2), (W / 2, -D / 2), (W / 2, D / 2), (-W / 2, D / 2), (-W / 2, -D / 2)]
    m.add(0, wall_run("wall", pts, 11, 5, (0, 0, 0.3), "#B07A5A", towers=True, tower_r=6.5, tower_every=60, merlon="round", batter=0.2))
    m.add(1, gatehouse("south_gate", 26, 16, 15, (0, -D / 2, 0.3), "S", "#B07A5A", LIME, "mughal"), "gates")
    m.add(1, gatehouse("water_gate", 18, 12, 12, (40, D / 2, 0.3), "N", "#B07A5A", LIME, "mughal"))
    for k in range(5):
        m.add(1, box(f"ghat{k}", 24, 2.0 * (5 - k), 0.25 * (5 - k), (40, D / 2 + 6 + (5 - k), 0.3), shade(BRICKR, 0.1)))
    m.add(2, courtyard_ring("palace", 90, 64, 8, 10, (-40, 40, 0.3), PLASTER, DARK, True), "palace and mosque")
    m.add(2, box("palace_court", 70, 44, 0.15, (-40, 40, 0.3), shade(DUST, 0.15)))
    m.add(2, box("palace_pool", 14, 10, 0.4, (-40, 40, 0.3), WATER))
    for sx in (-1, 1):
        for sy in (-1, 1):
            m.add(2, chhatri(f"pk{sx}{sy}", 2.6, 6, (-40 + sx * 42, 40 + sy * 29, 8.3), PLASTER, LIME))
    m.add(2, box("darbar", 30, 16, 9, (-40, 63, 0.3), PLASTER))
    m.add(2, arcade("darbar_a", 26, 6.5, 7, (-40, 54.95, 0.3), "S", DARK, True))
    m.add(2, move(mosque("fort_mosque", 34, 26, (0, 0, 0), PLASTER, LIME, LIME, domes=3, minarets=0, court=True), 70, 20, 0.3))
    mk = lambda nm, w, d, x, y, rng: flat_house(nm, w, d, rng.uniform(3.5, 5.5), (x, y, 0.3), rng.choice(["#C99F78", "#D8C3A0", "#BFA07E"]), True, "S")
    m.add(3, scatter("barracks", 17, 34, (-140, 140), (-100, 100), mk, avoid=[(-90, 2, 10, 78), (48, 2, 92, 38), (-16, -112, 16, -60), (25, 90, 55, 112)], size=(8, 16), gap=3), "quarters")
    m.add(3, trees("tr", [(-110, -80), (-60, -70), (110, -80), (110, 60), (20, 70), (-120, 80), (60, -60)], 3.6, z=0.3))
    return m


def sher_shah_mosque():
    """Afghan-style mosque facing east: a five-bay hall under a great central dome, smaller corner domes and kiosks, a walled court."""
    m = Model("sher-shah-mosque")
    m.add(0, box("ground", 60, 50, 0.3, (0, 0, 0), DUST), "plinth and court")
    m.add(0, box("plinth", 56, 46, 1.2, (0, 0, 0.3), shade(PLASTER, -0.1)))
    m.add(0, box("court", 34, 42, 0.1, (9, 0, 1.5), shade(DUST, 0.2)))
    m.add(0, wall_run("court_wall", [(-6, -22), (27, -22), (27, 22), (-6, 22)], 3.0, 1.0, (0, 0, 1.5), PLASTER, towers=False, merlon="round"))
    m.add(0, iwan("east_gate", 8, 7, 3, (27, 0, 1.5), "E", PLASTER, LIME))
    m.add(0, box("tank", 7, 7, 0.4, (12, 0, 1.5), WATER))
    hx, hd, hl, hh = -16, 18, 36, 10
    zb = 1.5
    m.add(1, box("hall", hd, hl, hh, (hx, 0, zb), "#E2D6BF"), "prayer hall")
    bays = [(-13.6, 5, 7.5), (-6.8, 5, 7.5), (0, 7, 9.0), (6.8, 5, 7.5), (13.6, 5, 7.5)]
    for i, (y, w, h) in enumerate(bays):
        m.add(1, iwan(f"bay{i}", w + 1, h, 1.2, (hx + hd / 2 + 0.6, y, zb), "E", "#E2D6BF", LIME))
    m.add(1, move(merlons("mer", hd, hl, zb + hh, 0.6, 0.7, "#E2D6BF", "round"), hx, 0, 0))
    m.add(1, box("band", hd + 0.4, hl + 0.4, 0.6, (hx, 0, zb + hh - 1.4), "#B9A98C"))
    m.add(2, cylinder("drum", 7.2, 3.0, (hx, 0, zb + hh), "#E2D6BF", verts=24), "domes")
    m.add(2, shallow_dome("dome", 7.2, (hx, 0, zb + hh + 3.0), "#EDE5D3", rise=0.95, finial=True))
    for sx in (-1, 1):
        for sy in (-1, 1):
            m.add(2, cylinder(f"sd_drum{sx}{sy}", 2.6, 1.6, (hx + sx * 5.2, sy * 12.5, zb + hh), "#E2D6BF", verts=16))
            m.add(2, shallow_dome(f"sd{sx}{sy}", 2.6, (hx + sx * 5.2, sy * 12.5, zb + hh + 1.6), "#EDE5D3", rise=0.9, finial=True))
            m.add(2, oct_tower_simple(f"ct{sx}{sy}", 1.8, hh + 3.5, (hx + sx * (hd / 2 + 0.6), sy * (hl / 2 + 0.6), zb)))
    return m


def oct_tower_simple(name, r, h, loc):
    x, y, z = loc
    pts = [(r * math.cos(math.pi / 8 + i * math.pi / 4), r * math.sin(math.pi / 8 + i * math.pi / 4)) for i in range(8)]
    parts = [prism(name + "_b", pts, h, (x, y, z), "#D8CCB4")]
    parts.append(chhatri(name + "_c", r * 0.95, r * 3.2, (x, y, z + h), "#E2D6BF", "#EDE5D3", 8))
    return join(parts, name)


def kamaldah():
    m = Model("kamaldah")
    m.add(0, frustum("mound", 36, 36, 28, 28, 1.8, (0, 0, 0), EARTH), "mound and wall")
    m.add(0, box("court", 26, 26, 0.1, (0, 0, 1.8), shade(DUST, 0.15)))
    m.add(0, wall_run("wall", [(-13, -13), (13, -13), (13, 13), (-13, 13), (-13, -13)], 2.4, 0.7, (0, 0, 1.8), WHITEWASH, towers=False, merlon=None))
    m.add(0, box("gate", 5, 3, 4.2, (0, -13, 1.8), WHITEWASH))
    m.add(0, arch_panel("gate_a", 1.8, 3.0, (0, -14.55, 1.8), "S", DARK, True))
    m.add(0, stair("gate_st", 4, 1.8, 3.4, 5, (0, -16, 0), "S", shade(EARTH, 0.1)))
    m.add(1, move(shikhara_temple("sthulabhadra", 4.2, 11, (0, 0, 0), WHITEWASH, True, "S"), 3, 3, 1.8), "shrines")
    m.add(1, move(shikhara_temple("sudarshan", 3.2, 8, (0, 0, 0), WHITEWASH, True, "S"), -6, 4, 1.8))
    m.add(2, trees("tr", [(9, -8), (-9, -8), (-15, 15), (15, 15)], 2.0, z=1.8), "trees")
    for sx in (-1, 1):
        for sy in (-1, 1):
            m.add(2, chhatri(f"kiosk{sx}{sy}", 1.3, 3.4, (sx * 12, sy * 12, 4.2), WHITEWASH, WHITEWASH, 6))
    m.add(2, lathe("manastambha", [(0.8, 0), (0.8, 0.6), (0.35, 0.7), (0.3, 6.5), (0.6, 6.8), (0.6, 7.3), (0.0, 8.2)], (-6, -6, 1.8), WHITEWASH, verts=16))
    m.add(2, chhatri("pillar_kiosk", 0.7, 1.8, (-6, -6, 9.0), WHITEWASH, GILT, 4))
    return m


BUILDERS = {
    "pataliputra/mauryan-palace": mauryan_palace,
    "pataliputra/pillared-hall": pillared_hall,
    "pataliputra/pillared-hall-ruin": pillared_hall_ruin,
    "pataliputra/palisade": palisade,
    "pataliputra/city-gate": city_gate,
    "pataliputra/pataligama": pataligama,
    "pataliputra/harbour": harbour,
    "pataliputra/ashoka-pillar": ashoka_pillar,
    "pataliputra/ashoka-stupa": ashoka_stupa,
    "pataliputra/agam-kuan": agam_kuan,
    "pataliputra/kukkutarama": kukkutarama,
    "pataliputra/arogya-vihara": arogya_vihara,
    "pataliputra/gupta-temple": gupta_temple,
    "pataliputra/patna-fort": patna_fort,
    "pataliputra/sher-shah-mosque": sher_shah_mosque,
    "pataliputra/kamaldah": kamaldah,
}
