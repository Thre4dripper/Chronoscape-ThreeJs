"""
Regional street-life props: the Islamic world (Cairo, Baghdad, Cordoba, Samarkand, Delhi, Agra,
Fatehpur Sikri, Ottoman Istanbul, Athens), sub-Saharan Africa (Timbuktu, Great Zimbabwe, Aksum)
and Venice. The same cast as Rome's props.py, redrawn: simple primitives in the grey study-model
style with a few colour accents, metres, origin at ground centre, facing -Y.

Keys: props/islamic/<name>, props/african/<name>, props/venetian/{boat,skiff}.
Animated parts keep Rome's names (anim_hammer, anim_walk, anim_spin, anim_graze).
"""
import math
import random
import bpy
import bmesh
from mathutils import Vector, Matrix, Euler
from chronokit import box, cylinder, dome, join, shade, mesh_from, _finish
from props import Prop, wheel, WOOD, IRON, FIRE, STRAW, G1, G2, G3, SKIN

# ---------------------------------------------------------------- palette
WHITE, CREAM, INDIGO, MADDER, SAFFRON, OLIVE = "#ECE6D6", "#D9CBAA", "#3F4F6E", "#8E3B2E", "#C98A2E", "#6E7A58"
BLACK, PLUM, TEAL, ROSE = "#2F2B2B", "#6B4A5E", "#4E7A78", "#B0605A"
BRASS, COPPER, CLAY, CLAY_D, POT_B = "#C9A24A", "#B0643A", "#B5654A", "#8E4A32", "#3A3330"
SKIN_M, SKIN_D = "#A87A55", "#5E3E2A"
CAMEL, DONKEY, GOAT = "#C2A27A", "#8C857A", "#2E2A28"
MUD, THATCH, SALT, WATER = "#B59670", "#B8A060", "#E4E0D6", "#65888A"
TROUSER, DARKWOOD = "#7A6650", "#5A4030"

I4 = Matrix.Identity(4)


# ---------------------------------------------------------------- geometry helpers
def flat(o):
    """Bake an object's transform into its mesh so it sits in world space with an identity matrix."""
    o.data.transform(o.matrix_basis)
    o.matrix_basis = I4.copy()
    return o


def tilt(o, rx=0.0, ry=0.0, rz=0.0):
    """Rotate a part about its own centre (chronokit's box() applies its location, so rotation_euler would turn it about the world origin)."""
    flat(o)
    c = sum((v.co for v in o.data.vertices), Vector()) / len(o.data.vertices)
    o.data.transform(Matrix.Translation(c) @ Euler((rx, ry, rz)).to_matrix().to_4x4() @ Matrix.Translation(-c))
    return o


def grp(parts, name, loc=(0, 0, 0), rot=0.0, scale=1.0, lean=0.0, pivot=(0, 0, 0)):
    """Join parts built about the origin, optionally lean them about a pivot (X axis, +lean tips toward -Y),
    then scale, turn about Z and move to loc."""
    parts = [flat(p) for p in parts if p is not None]
    o = flat(join(parts, name))
    loc = tuple(loc) + (0.0,) * (3 - len(loc))
    M = Matrix.Translation(Vector(loc)) @ Matrix.Rotation(rot, 4, "Z") @ Matrix.Scale(scale, 4)
    if lean:
        pv = Vector(pivot)
        M = M @ Matrix.Translation(pv) @ Matrix.Rotation(lean, 4, "X") @ Matrix.Translation(-pv)
    o.data.transform(M)
    return o


def rod(name, p0, p1, r, color, verts=6, r_top=None):
    """A cylinder (or cone) from point p0 to point p1."""
    a, b = Vector(p0), Vector(p1)
    d = b - a
    if r_top is None:
        bpy.ops.mesh.primitive_cylinder_add(vertices=verts, radius=r, depth=d.length, location=(0, 0, 0))
    else:
        bpy.ops.mesh.primitive_cone_add(vertices=verts, radius1=r, radius2=r_top, depth=d.length, location=(0, 0, 0))
    o = bpy.context.active_object
    o.data.transform(Matrix.Translation((a + b) / 2) @ d.normalized().to_track_quat("Z", "Y").to_matrix().to_4x4())
    o.matrix_basis = I4.copy()
    return _finish(o, name, color)


def ball(name, r, c, color, squash=1.0, seg=8, rings=5):
    """A low-poly sphere centred at c."""
    bpy.ops.mesh.primitive_uv_sphere_add(segments=seg, ring_count=rings, radius=r, location=(0, 0, 0))
    o = bpy.context.active_object
    o.data.transform(Matrix.Translation(Vector(c)) @ Matrix.Diagonal((1, 1, squash, 1)))
    o.matrix_basis = I4.copy()
    return _finish(o, name, color)


def disc(name, r, c, normal, color, t=0.03, verts=12):
    n = Vector(normal).normalized() * (t / 2)
    return rod(name, Vector(c) - n, Vector(c) + n, r, color, verts=verts)


def sheet(name, pts, t, color):
    """A thin triangular plate (a sail)."""
    a, b, c = [Vector(p) for p in pts]
    n = (b - a).cross(c - a).normalized() * (t / 2)
    vs = [tuple(v) for v in (a - n, b - n, c - n, a + n, b + n, c + n)]
    return mesh_from(name, vs, [(0, 1, 2), (3, 5, 4), (0, 3, 4, 1), (1, 4, 5, 2), (2, 5, 3, 0)], color=color)


def vault(name, r, L, c, color, verts=12, down=False):
    """Half cylinder along Y with its springing line at c (a canopy, or with down=True a sling/trough)."""
    o = rod(name, (c[0], c[1] - L / 2, c[2]), (c[0], c[1] + L / 2, c[2]), r, color, verts=verts)
    bm = bmesh.new()
    bm.from_mesh(o.data)
    kill = [v for v in bm.verts if (v.co.z > c[2] + 1e-3 if down else v.co.z < c[2] - 1e-3)]
    bmesh.ops.delete(bm, geom=kill, context="VERTS")
    bm.to_mesh(o.data)
    bm.free()
    return o


def hullx(name, L, B, D, color, bow=0.5, stern=0.5, fine=0.1, keel=0.55, n=9):
    """A boat hull along Y, bow at -Y: pointed ends, sheer rising toward bow and stern, closed on top."""
    verts, faces = [], []
    for i in range(n):
        t = -1 + 2 * i / (n - 1)
        hw = (fine + (1 - fine) * (1 - abs(t) ** 2.4)) * B / 2
        zt = D + (bow if t < 0 else stern) * abs(t) ** 2
        zb = 0.35 * D * abs(t) ** 3
        y = t * L / 2
        verts += [(-hw * keel, y, zb), (hw * keel, y, zb), (hw, y, zt), (-hw, y, zt)]
    for i in range(n - 1):
        a, b = 4 * i, 4 * (i + 1)
        for k in range(4):
            faces.append((a + k, a + (k + 1) % 4, b + (k + 1) % 4, b + k))
    e = 4 * (n - 1)
    faces += [(0, 1, 2, 3), (e + 3, e + 2, e + 1, e)]
    return mesh_from(name, verts, faces, color=color)


def deck_slab(name, L, B, y0, y1, z0, z1, color, fine=0.1, shrink=0.94, n=6):
    """A flat slab (deck, poop, floor) whose outline follows hullx's waterplane, so it never overhangs the tapered hull."""
    verts, faces = [], []
    for i in range(n):
        y = y0 + (y1 - y0) * i / (n - 1)
        t = min(1.0, abs(y) / (L / 2))
        hw = (fine + (1 - fine) * (1 - t ** 2.4)) * B / 2 * shrink
        verts += [(-hw, y, z0), (hw, y, z0), (hw, y, z1), (-hw, y, z1)]
    for i in range(n - 1):
        a, b = 4 * i, 4 * (i + 1)
        for k in range(4):
            faces.append((a + k, a + (k + 1) % 4, b + (k + 1) % 4, b + k))
    e = 4 * (n - 1)
    faces += [(0, 1, 2, 3), (e + 3, e + 2, e + 1, e)]
    return mesh_from(name, verts, faces, color=color)


def scatter(n, xr, yr, dmin, seed, avoid=()):
    rnd = random.Random(seed)
    pts, tries = [], 0
    while len(pts) < n and tries < 20000:
        tries += 1
        p = (rnd.uniform(*xr), rnd.uniform(*yr))
        if all(math.dist(p, q) >= dmin for q in pts) and all(math.dist(p, a[:2]) >= a[2] for a in avoid):
            pts.append(p)
    return pts, rnd


# ---------------------------------------------------------------- people
def headgear(n, hz, kind, c, s=1.0):
    if kind == "turban":
        return [cylinder(n + "_tb", 0.15 * s, 0.1 * s, (0, 0, hz + 0.08 * s), c, verts=10), dome(n + "_tt", 0.155 * s, (0, 0, hz + 0.17 * s), c, squash=0.7, segments=10, rings=4)]
    if kind == "tagel":  # Tuareg indigo turban with the face veil
        return [cylinder(n + "_tb", 0.15 * s, 0.12 * s, (0, 0, hz + 0.07 * s), c, verts=10), dome(n + "_tt", 0.155 * s, (0, 0, hz + 0.18 * s), c, squash=0.6, segments=10, rings=4),
                box(n + "_mask", 0.24 * s, 0.1 * s, 0.11 * s, (0, -0.075 * s, hz - 0.01 * s), c)]
    if kind == "veil":
        return [dome(n + "_veil", 0.158 * s, (0, 0.035 * s, hz - 0.03 * s), c, squash=1.45, segments=10, rings=5)]
    if kind == "cap":
        return [dome(n + "_cap", 0.135 * s, (0, 0, hz + 0.09 * s), c, squash=0.6, segments=10, rings=4)]
    if kind == "wrap":
        return [cylinder(n + "_wr", 0.13 * s, 0.18 * s, (0, 0.01 * s, hz + 0.09 * s), c, verts=10, r_top=0.18 * s)]
    if kind == "hat":  # flat straw boater
        return [cylinder(n + "_brim", 0.23 * s, 0.02 * s, (0, 0, hz + 0.15 * s), c, verts=12), cylinder(n + "_crown", 0.13 * s, 0.09 * s, (0, 0, hz + 0.15 * s), c, verts=10)]
    if kind == "cone":  # Fulani straw hat
        return [cylinder(n + "_cone", 0.3 * s, 0.24 * s, (0, 0, hz + 0.13 * s), c, verts=10, r_top=0.03 * s)]
    if kind == "hair":
        return [dome(n + "_hair", 0.13 * s, (0, 0.02 * s, hz + 0.06 * s), c, squash=0.9, segments=10, rings=4)]
    return []


def figure(n, loc=(0, 0, 0), rot=0.0, robe=WHITE, top=None, head="turban", hc=WHITE, skin=SKIN, h=1.72, hands=None,
           lean=0.0, legs=None, arm=None, boubou=False, sash=None, carry=(), band=None):
    """A standing robed figure facing -Y. hands=(left, right) in local metres, None for hanging, "x" for no arm.
    legs=<colour> gives a knee-length tunic over bare legs or trousers. carry= parts on the upper body (leans with it)."""
    s = h / 1.72
    top = top or robe
    arm = arm or top
    low = []
    if legs:
        low += [rod(n + "_ll", (-0.1 * s, 0.06 * s, 0), (-0.1 * s, 0, 0.62 * s), 0.075 * s, legs), rod(n + "_rl", (0.1 * s, -0.06 * s, 0), (0.1 * s, 0, 0.62 * s), 0.075 * s, legs),
                cylinder(n + "_robe", 0.25 * s, 0.42 * s, (0, 0, 0.56 * s), robe, verts=10, r_top=0.21 * s)]
    else:
        low.append(cylinder(n + "_robe", 0.27 * s, 0.98 * s, (0, 0, 0), robe, verts=10, r_top=0.21 * s))
    if band:  # a contrasting hem band on a wrapper
        low.append(cylinder(n + "_band", 0.272 * s, 0.14 * s, (0, 0, 0.12 * s), band, verts=10, r_top=0.262 * s))
    if sash:
        low.append(cylinder(n + "_sash", 0.218 * s, 0.09 * s, (0, 0, 0.9 * s), sash, verts=10))
    hz = 1.36 * s
    up = [cylinder(n + "_chest", 0.21 * s, 0.38 * s, (0, 0, 0.97 * s), top, verts=10, r_top=0.16 * s),
          dome(n + "_head", 0.125 * s, (0, 0, hz), skin, squash=1.5, segments=10, rings=6)]
    if boubou:
        up.append(box(n + "_boubou", 0.64 * s, 0.26 * s, 0.6 * s, (0, 0, 0.74 * s), robe))
    up += headgear(n, hz, head, hc, s)
    L, R = hands or (None, None)
    for nm, sx, hnd in (("l", -1, L), ("r", 1, R)):
        if hnd == "x":
            continue
        hnd = hnd or (sx * 0.28 * s, 0.0, 0.78 * s)
        up.append(rod(f"{n}_arm{nm}", (sx * 0.23 * s, 0, 1.3 * s), hnd, 0.055 * s, arm))
    up += list(carry)
    upo = grp(up, n + "_up", lean=lean, pivot=(0, 0, 0.95 * s))
    return grp(low + [upo], n, loc=loc, rot=rot)


def seated(n, loc=(0, 0, 0), rot=0.0, robe=WHITE, top=None, head="turban", hc=WHITE, skin=SKIN, hands=None, lean=0.0, arm=None, carry=()):
    """A figure sitting cross-legged, facing -Y. Shoulders at (+-0.23, -0.46 sin lean, 0.2 + 0.46 cos lean)."""
    top = top or robe
    arm = arm or top
    low = [cylinder(n + "_lap", 0.36, 0.2, (0, -0.06, 0), robe, verts=10, r_top=0.3)]
    hz = 0.74
    up = [cylinder(n + "_chest", 0.22, 0.52, (0, 0, 0.18), top, verts=10, r_top=0.16), dome(n + "_head", 0.125, (0, 0, hz), skin, squash=1.5, segments=10, rings=6)]
    up += headgear(n, hz, head, hc)
    L, R = hands or (None, None)
    for nm, sx, hnd in (("l", -1, L), ("r", 1, R)):
        if hnd == "x":
            continue
        hnd = hnd or (sx * 0.24, -0.28, 0.24)
        up.append(rod(f"{n}_arm{nm}", (sx * 0.23, 0, 0.66), hnd, 0.055, arm))
    up += list(carry)
    upo = grp(up, n + "_up", lean=lean, pivot=(0, 0, 0.2))
    return grp(low + [upo], n, loc=loc, rot=rot)


def shoulder_seated(loc, lean, side=1):
    return (loc[0] + side * 0.23, loc[1] - 0.46 * math.sin(lean), (loc[2] if len(loc) > 2 else 0) + 0.2 + 0.46 * math.cos(lean))


def hammer_arm(S, skin, sleeve, head_c=IRON):
    """The smith's striking arm about the shoulder S, bent, the hammer held out in front. With the app's swing
    (rotation.x from -0.2 to -1.6) the head strikes at about S + (0, -0.83, -0.30) and lifts above the shoulder."""
    sx, sy, sz = S
    E = (sx + 0.03, sy - 0.18, sz - 0.3)
    H = (sx + 0.03, sy - 0.45, sz - 0.32)
    return [rod("uarm", S, E, 0.055, sleeve), rod("farm", E, H, 0.05, skin), rod("handle", H, (H[0], sy - 0.78, sz - 0.34), 0.022, WOOD),
            box("hammer_head", 0.09, 0.12, 0.17, (H[0], sy - 0.78, sz - 0.46), head_c)]


# ---------------------------------------------------------------- animals
def camel(n, loc=(0, 0, 0), rot=0.0, s=1.0, color=CAMEL, load="bags", c1=MADDER, c2=INDIGO):
    """A dromedary facing -Y, 2.1 m nose to tail (y -1.36..0.74), 1.9 m to the hump."""
    leg = shade(color, -0.12)
    p = [rod(f"{n}_leg{sx}{sy}", (sx, sy, 0), (sx, sy * 0.95, 1.05), 0.065, leg) for sx in (-0.15, 0.15) for sy in (-0.42, 0.45)]
    p += [box(n + "_body", 0.5, 1.3, 0.55, (0, 0.02, 0.95), color), dome(n + "_hump", 0.36, (0, 0.07, 1.48), color, squash=1.15, segments=10, rings=6),
          rod(n + "_neck", (0, -0.5, 1.3), (0, -1.0, 1.74), 0.12, color, r_top=0.085), box(n + "_head", 0.2, 0.46, 0.22, (0, -1.13, 1.66), shade(color, -0.06)),
          rod(n + "_tail", (0, 0.66, 1.42), (0, 0.74, 0.98), 0.03, leg)]
    if load == "bags":
        p += [dome(n + "_rug", 0.4, (0, 0.07, 1.46), c1, squash=0.95, segments=10, rings=4)]
        for sx in (-1, 1):
            p += [box(f"{n}_bag{sx}", 0.2, 0.7, 0.5, (sx * 0.35, 0.07, 0.9), c1), box(f"{n}_stripe{sx}", 0.21, 0.71, 0.08, (sx * 0.35, 0.07, 1.12), c2)]
        p.append(rod(n + "_roll", (-0.42, 0.55, 1.62), (0.42, 0.55, 1.62), 0.12, c2, verts=8))
    elif load == "salt":
        p += [dome(n + "_rug", 0.4, (0, 0.07, 1.46), c1, squash=0.95, segments=10, rings=4)]
        for sx in (-1, 1):
            for k in range(2):
                p.append(box(f"{n}_slab{sx}{k}", 0.07, 0.95, 0.42, (sx * (0.3 + 0.08 * k), 0.07, 0.86 + 0.04 * k), SALT))
            p.append(box(f"{n}_cord{sx}", 0.1, 0.05, 0.44, (sx * 0.35, 0.07, 0.86), "#5A4632"))
    elif load == "bales":
        p += [dome(n + "_rug", 0.4, (0, 0.07, 1.46), c1, squash=0.95, segments=10, rings=4)]
        for sx in (-1, 1):
            p += [box(f"{n}_bale{sx}", 0.3, 0.62, 0.5, (sx * 0.39, 0.07, 0.92), CREAM), box(f"{n}_rope{sx}", 0.31, 0.06, 0.51, (sx * 0.39, 0.07, 0.92), "#5A4632")]
    return grp(p, n, loc=loc, rot=rot, scale=s)


def zebu(n, loc=(0, 0, 0), rot=0.0, color="#D8D0C0", horns="#3A332C", long_horns=False):
    """A humped ox facing -Y, y -1.25..0.85. long_horns gives the lyre horns of the African sanga."""
    leg = shade(color, -0.15)
    p = [box(n + "_body", 0.62, 1.55, 0.7, (0, 0, 0.62), color)]
    p += [box(f"{n}_leg{sx}{sy}", 0.15, 0.15, 0.64, (sx, sy, 0), leg) for sx in (-0.2, 0.2) for sy in (-0.55, 0.55)]
    p += [dome(n + "_hump", 0.24 if not long_horns else 0.17, (0, -0.48, 1.28), shade(color, -0.05), squash=1.3, segments=8, rings=4),
          box(n + "_dewlap", 0.16, 0.4, 0.45, (0, -0.86, 0.55), shade(color, -0.04)), box(n + "_head", 0.3, 0.48, 0.34, (0, -1.0, 0.9), shade(color, -0.08)),
          rod(n + "_tail", (0, 0.77, 1.25), (0, 0.84, 0.45), 0.03, leg)]
    for sx in (-1, 1):
        p.append(box(f"{n}_ear{sx}", 0.16, 0.06, 0.07, (sx * 0.22, -0.86, 1.08), shade(color, -0.08)))
        if long_horns:
            p.append(rod(f"{n}_horn{sx}", (sx * 0.1, -0.92, 1.22), (sx * 0.52, -0.84, 1.72), 0.05, "#E9E0CC", r_top=0.018))
        else:
            p.append(rod(f"{n}_horn{sx}", (sx * 0.1, -0.92, 1.22), (sx * 0.2, -0.86, 1.46), 0.035, horns, r_top=0.015))
    return grp(p, n, loc=loc, rot=rot)


def donkey(n, loc=(0, 0, 0), rot=0.0, color=DONKEY, s=1.0):
    """A small donkey facing -Y, y -1.03..0.52, back at 1.05."""
    leg = shade(color, -0.18)
    p = [box(n + "_body", 0.42, 0.95, 0.45, (0, 0, 0.6), color)]
    p += [box(f"{n}_leg{sx}{sy}", 0.1, 0.1, 0.62, (sx, sy, 0), leg) for sx in (-0.13, 0.13) for sy in (-0.33, 0.33)]
    p += [rod(n + "_neck", (0, -0.38, 0.92), (0, -0.62, 1.2), 0.1, color), box(n + "_head", 0.2, 0.42, 0.22, (0, -0.82, 1.06), shade(color, -0.08)),
          rod(n + "_tail", (0, 0.47, 0.98), (0, 0.52, 0.55), 0.025, leg)]
    for sx in (-1, 1):
        p.append(rod(f"{n}_ear{sx}", (sx * 0.06, -0.66, 1.25), (sx * 0.1, -0.6, 1.5), 0.03, color))
    return grp(p, n, loc=loc, rot=rot, scale=s)


def goat(n, loc=(0, 0, 0), rot=0.0, color=GOAT):
    leg = shade(color, -0.1)
    p = [box(n + "_body", 0.3, 0.62, 0.32, (0, 0, 0.36), color)]
    p += [rod(f"{n}_leg{sx}{sy}", (sx, sy, 0), (sx, sy, 0.38), 0.03, leg, verts=4) for sx in (-0.09, 0.09) for sy in (-0.22, 0.22)]
    p += [box(n + "_head", 0.14, 0.26, 0.17, (0, -0.38, 0.58), color), rod(n + "_horns", (0, -0.32, 0.74), (0, -0.2, 0.88), 0.03, "#8A7A62", verts=4),
          box(n + "_ear", 0.3, 0.05, 0.05, (0, -0.32, 0.68), color)]
    return grp(p, n, loc=loc, rot=rot)


# ---------------------------------------------------------------- stalls
def bazaar_stall(name, awning, goods, vendor=None):
    """A bazaar stall: a raised mud-brick bench before a shop wall, a cloth awning on two poles, the trader
    sitting cross-legged among his goods. Bench top at z 0.47, y -0.43..0.83; goods also on the ground at y -0.7."""
    m = Prop(name)
    p = [box("bench", 2.4, 1.25, 0.42, (0, 0.2, 0), MUD), box("bench_top", 2.5, 1.35, 0.05, (0, 0.2, 0.42), shade(MUD, 0.15)),
         box("back", 2.7, 0.12, 2.36, (0, 0.95, 0), G1)]
    for sx in (-1.2, 1.2):
        p.append(box(f"pole{sx}", 0.08, 0.08, 2.05, (sx, -0.85, 0), WOOD))
    aw = box("awning", 2.8, 1.92, 0.04, (0, 0.05, 2.18), awning)
    tilt(aw, 0.165)
    p += [aw, box("valance", 2.8, 0.03, 0.2, (0, -0.91, 1.86), shade(awning, 0.3))]
    for k in range(4):
        p.append(box(f"stripe{k}", 0.22, 1.92, 0.045, (-1.05 + k * 0.7, 0.05, 2.18), shade(awning, 0.35)))
        tilt(p[-1], 0.165)
    p += goods
    p.append(vendor if vendor is not None else seated("vendor", (0.6, 0.5, 0.47), robe=CREAM, top=INDIGO, hc=WHITE))
    m.add("base", p)
    return m


def mat_stall(name, goods, vendor=None, roof=THATCH):
    """An African market pitch: goods set out on a mat under a flat thatched shade on forked posts. Mat y -0.8..0.9."""
    m = Prop(name)
    p = [box("mat", 2.4, 1.7, 0.03, (0, 0.05, 0), STRAW)]
    for sx in (-1.2, 1.2):
        for sy in (-0.85, 0.95):
            p.append(rod(f"post{sx}{sy}", (sx, sy, 0), (sx, sy, 2.0 if sy > 0 else 1.85), 0.055, DARKWOOD))
        p.append(box(f"beam{sx}", 0.1, 2.0, 0.1, (sx, 0.05, 1.86), DARKWOOD))
    shade_roof = box("shade", 2.8, 2.15, 0.14, (0, 0.05, 1.93), roof)
    tilt(shade_roof, 0.08)
    p += [shade_roof] + goods
    p.append(vendor if vendor is not None else seated("vendor", (0.65, 0.55, 0.03), robe=SAFFRON, top=INDIGO, head="wrap", hc=MADDER, skin=SKIN_D, arm=SKIN_D))
    m.add("base", p)
    return m


# ================================================================ ISLAMIC
def i_walker():
    """A townsman in a white turban and a long qaba, sash at the waist, mid-stride."""
    m = Prop("prop-islamic-walker")
    f = figure("w", robe=INDIGO, top=INDIGO, hc=WHITE, sash=SAFFRON, hands=((-0.27, -0.2, 0.82), (0.27, 0.18, 0.82)), arm=INDIGO)
    m.add("base", [f, box("foot_l", 0.1, 0.22, 0.07, (-0.1, -0.24, 0), "#4A3426"), box("foot_r", 0.1, 0.22, 0.07, (0.1, 0.16, 0), "#4A3426")])
    return m


def i_matron():
    """A woman in a black chador carrying a clay water jar on her head, one hand steadying it."""
    m = Prop("prop-islamic-matron")
    hz = 1.36
    jar = [cylinder("jar_b", 0.09, 0.16, (0, 0, hz + 0.2), CLAY, verts=10, r_top=0.15), cylinder("jar_s", 0.15, 0.16, (0, 0, hz + 0.36), CLAY, verts=10, r_top=0.07),
           cylinder("jar_n", 0.05, 0.08, (0, 0, hz + 0.52), CLAY_D, verts=8, r_top=0.06)]
    f = figure("m", robe=BLACK, head="veil", hc=BLACK, hands=((-0.26, -0.05, 0.8), (0.14, -0.02, 1.62)), carry=jar)
    m.add("base", [f])
    return m


def i_porter():
    """A hammal bent under a great sack on his back, steadying the ropes at his chest."""
    m = Prop("prop-islamic-porter")
    sack = [box("sack", 0.5, 0.36, 0.56, (0, 0.3, 0.98), CREAM), box("pad", 0.42, 0.1, 0.4, (0, 0.11, 1.0), MADDER), dome("sack_top", 0.22, (0, 0.3, 1.52), CREAM, squash=0.5, segments=8, rings=4)]
    f = figure("p", (0, -0.06), robe=SAFFRON, top=SAFFRON, legs=TROUSER, head="cap", hc=WHITE, skin=SKIN_M, lean=0.45,
               hands=((-0.17, -0.18, 1.18), (0.17, -0.18, 1.18)), carry=sack)
    m.add("base", [f])
    return m


def i_mule():
    """A camel with saddlebags led on a rope by its driver (a small dromedary, inside the mule's budget)."""
    m = Prop("prop-islamic-mule")
    c = camel("camel", (-0.17, 0.27), s=0.88)
    d = figure("drv", (0.52, -1.24), robe=WHITE, top=OLIVE, hc=WHITE, skin=SKIN_M, hands=((-0.2, 0.2, 1.0), None))
    m.add("base", [c, d, rod("rope", (0.32, -1.04, 1.0), (-0.17, -0.7, 1.45), 0.015, "#5A4632", verts=4)])
    return m


def i_litter():
    """A palki: a curtained palanquin slung under one pole, carried by four bearers in line."""
    m = Prop("prop-islamic-litter")
    p = [box("cabin", 0.84, 1.5, 0.7, (0, 0, 0.55), MADDER), box("roof", 0.96, 1.62, 0.08, (0, 0, 1.25), BRASS),
         box("curtain_l", 0.03, 1.1, 0.5, (-0.43, 0, 0.62), CREAM), box("curtain_r", 0.03, 1.1, 0.5, (0.43, 0, 0.62), CREAM),
         dome("canopy", 0.36, (0, 0, 1.33), MADDER, squash=0.6, segments=10, rings=4), dome("finial", 0.06, (0, 0, 1.53), BRASS, squash=1.6, segments=6, rings=4),
         rod("pole", (0, -2.24, 1.42), (0, 2.24, 1.42), 0.05, WOOD, verts=6)]
    for sy in (-1, 1):
        p.append(rod(f"hanger{sy}", (0, sy * 0.7, 1.3), (0, sy * 0.7, 1.42), 0.03, IRON, verts=4))
    for i, (sy, sx) in enumerate([(-1.98, 0.16), (-1.42, -0.16), (1.42, 0.16), (1.98, -0.16)]):
        # each bearer takes the pole on the shoulder nearest it and steadies it with one hand
        hand = (-sx / abs(sx) * 0.15, 0, 1.42)
        hands = (hand, None) if sx > 0 else (None, (0.15, 0, 1.42))
        p.append(figure(f"b{i}", (sx, sy), robe=WHITE, top=WHITE, legs=SKIN_M, head="turban", hc=[MADDER, SAFFRON][i % 2], skin=SKIN_M, arm=SKIN_M, hands=hands, h=1.66))
    m.add("base", p)
    return m


def i_handcart():
    """A donkey with panniers of melons, driven from behind by a market gardener with a switch."""
    m = Prop("prop-islamic-handcart")
    p = [donkey("donkey", (0, -0.36)), box("saddlecloth", 0.5, 0.6, 0.04, (0, -0.36, 1.05), MADDER)]
    for sx in (-1, 1):
        p.append(cylinder(f"basket{sx}", 0.2, 0.36, (sx * 0.36, -0.36, 0.5), STRAW, verts=8, r_top=0.23))
        for k in range(3):
            p.append(ball(f"melon{sx}{k}", 0.11, (sx * 0.36 + (k - 1) * 0.08, -0.36 + (k % 2 - 0.5) * 0.12, 0.92), ["#7E8F4E", "#D2B04A", "#6E8048"][k], squash=0.85, seg=8, rings=5))
    p.append(figure("drv", (0.1, 1.0), robe=CREAM, top=OLIVE, hc=WHITE, skin=SKIN_M, hands=(None, (0.25, -0.3, 1.0))))
    p.append(rod("switch", (0.35, 0.7, 1.0), (0.3, 0.1, 1.45), 0.012, WOOD, verts=4))
    m.add("base", p)
    return m


def i_cart():
    """A bullock cart: two humped zebu oxen under a yoke, a covered body with an arched cloth hood, the driver
    on the front. Serves as the street cart and the cart scene."""
    m = Prop("prop-islamic-cart")
    dy = 0.17
    p = [zebu("ox_l", (-0.46, -1.45 + dy), color="#E2DACA"), zebu("ox_r", (0.46, -1.45 + dy), color="#C9BCA6"),
         box("yoke", 1.6, 0.12, 0.12, (0, -2.1 + dy, 1.22), WOOD), rod("pole", (0, -2.1 + dy, 1.2), (0, 0.45 + dy, 0.95), 0.06, WOOD),
         box("bed", 1.5, 2.0, 0.15, (0, 1.35 + dy, 0.9), WOOD), box("rail_l", 0.06, 2.0, 0.2, (-0.72, 1.35 + dy, 1.05), WOOD), box("rail_r", 0.06, 2.0, 0.2, (0.72, 1.35 + dy, 1.05), WOOD),
         wheel("wl", 0.72, (-0.86, 1.45 + dy, 0.72)), wheel("wr", 0.72, (0.86, 1.45 + dy, 0.72)),
         vault("hood", 0.72, 1.55, (0, 1.6 + dy, 1.05), MADDER, verts=12), box("hood_trim", 1.5, 0.06, 0.1, (0, 0.82 + dy, 1.05), SAFFRON),
         dome("finial", 0.08, (0, 0.85 + dy, 1.74), BRASS, squash=1.5, segments=6, rings=4),
         seated("driver", (0, 0.55 + dy, 1.05), robe=WHITE, top=WHITE, hc=SAFFRON, skin=SKIN_M, hands=((-0.2, -0.35, 0.5), (0.2, -0.35, 0.5)))]
    for sx in (-1, 1):
        p.append(rod(f"rein{sx}", (sx * 0.2, 0.2 + dy, 1.55), (sx * 0.46, -2.3 + dy, 1.1), 0.012, "#5A4632", verts=4))
    p.append(figure("walker", (1.45, -0.3), robe=CREAM, top=TEAL, hc=WHITE, skin=SKIN_M))
    m.add("base", p)
    return m


def i_stall_fruit():
    g = []
    for k, x in enumerate((-0.95, -0.45)):  # trays of dates
        g += [cylinder(f"tray{k}", 0.24, 0.06, (x, -0.2, 0.47), STRAW, verts=10), dome(f"dates{k}", 0.21, (x, -0.2, 0.53), "#5A3A28", squash=0.6, segments=8, rings=4)]
    for k in range(4):  # melons
        g.append(ball(f"melon{k}", 0.14, (0.05 + (k % 2) * 0.27, -0.25 + (k // 2) * 0.25, 0.6), ["#7E8F4E", "#D2B04A"][k % 2], squash=0.8))
    for k in range(5):  # pomegranates
        g.append(ball(f"pom{k}", 0.075, (-1.0 + k * 0.14, 0.2, 0.55), "#A6332E", seg=6, rings=4))
    for k, x in enumerate((-0.8, 0.0, 0.8)):  # baskets on the ground
        col = ["#A6332E", "#D2B04A", "#5A3A28"][k]
        g += [cylinder(f"bk{k}", 0.24, 0.3, (x, -0.68, 0), STRAW, verts=10, r_top=0.28), dome(f"bkf{k}", 0.25, (x, -0.68, 0.3), col, squash=0.5, segments=8, rings=4)]
    g.append(rod("dates_hang", (-0.6, -0.8, 1.8), (-0.6, -0.8, 1.4), 0.08, "#7A4A28", verts=6, r_top=0.03))
    return bazaar_stall("prop-islamic-stall-fruit", "#B5654A", g)


def i_stall_pots():
    g = []
    for k in range(5):  # copper cauldrons and brass pots on the bench
        x = -1.0 + k * 0.28
        col = [COPPER, BRASS][k % 2]
        g += [cylinder(f"pot{k}", 0.12, 0.16, (x, -0.2, 0.47), col, verts=10, r_top=0.14), dome(f"lid{k}", 0.13, (x, -0.2, 0.63), col, squash=0.6, segments=8, rings=4)]
    for k in range(3):  # trays leaning on the wall
        g.append(disc(f"tray{k}", 0.3 - k * 0.04, (-0.85 + k * 0.5, 0.86, 0.9 + k * 0.1), (0, 1, 0.25), [BRASS, COPPER, BRASS][k]))
    for k in range(3):  # ewers
        x = -0.95 + k * 0.4
        g += [cylinder(f"ewer{k}", 0.1, 0.32, (x, 0.3, 0.47), BRASS, verts=8, r_top=0.05), rod(f"spout{k}", (x - 0.06, 0.3, 0.6), (x - 0.18, 0.3, 0.78), 0.02, BRASS, verts=4)]
    for k, x in enumerate((-0.75, 0.0, 0.75)):  # big cauldrons on the ground
        g += [cylinder(f"caul{k}", 0.2, 0.32, (x, -0.68, 0), COPPER, verts=10, r_top=0.26)]
    for k, x in enumerate((-0.7, 0.0, 0.7)):  # hanging lamps
        g += [rod(f"chain{k}", (x, -0.65, 1.65), (x, -0.65, 2.07), 0.01, IRON, verts=4), dome(f"lamp{k}", 0.11, (x, -0.65, 1.5), BRASS, squash=1.3, segments=8, rings=4),
              cylinder(f"lampb{k}", 0.05, 0.08, (x, -0.65, 1.42), BRASS, verts=6, r_top=0.11)]
    return bazaar_stall("prop-islamic-stall-pots", OLIVE, g)


def i_stall_cloth():
    g = []
    cols = [MADDER, INDIGO, SAFFRON, PLUM, TEAL]
    for k in range(3):  # carpets hung on the shop wall, each with a border
        x = -0.85 + k * 0.85
        g += [box(f"carpet{k}", 0.72, 0.03, 1.3, (x, 0.875, 0.75), cols[k]), box(f"field{k}", 0.52, 0.03, 1.08, (x, 0.86, 0.86), cols[(k + 3) % 5])]
    for k in range(5):  # a stack of folded carpets
        g.append(box(f"stack{k}", 0.9 - k * 0.04, 0.6, 0.07, (-0.55, -0.15, 0.47 + k * 0.07), cols[k]))
    for k in range(4):  # silk bolts
        g.append(rod(f"bolt{k}", (0.0, -0.4 + k * 0.17, 0.53), (0.42, -0.4 + k * 0.17, 0.53), 0.075, ["#C2506A", "#5E8A9A", "#D9B24A", "#7D5A9B"][k], verts=8))
    for k, x in enumerate((-0.6, 0.3)):  # carpets rolled on the ground
        g.append(rod(f"roll{k}", (x - 0.45, -0.68, 0.14), (x + 0.45, -0.68, 0.14), 0.14, cols[k + 1], verts=8))
    return bazaar_stall("prop-islamic-stall-cloth", INDIGO, g)


def i_stall():
    """A spice stall: open sacks topped with cones of red, ochre and green spice, a balance on the bench, a buyer."""
    g = []
    spice = ["#A8322A", "#D9A520", "#C2502C", "#7A8A3A", "#7A5636", "#3A3330"]
    for k in range(6):  # sacks on the bench
        x, y = -1.0 + (k % 3) * 0.38, -0.25 + (k // 3) * 0.42
        g += [cylinder(f"sack{k}", 0.16, 0.24, (x, y, 0.47), CREAM, verts=8, r_top=0.17), cylinder(f"cone{k}", 0.16, 0.26, (x, y, 0.71), spice[k], verts=8, r_top=0.0)]
    for k in range(4):  # big sacks on the ground
        x = -0.95 + k * 0.63
        g += [cylinder(f"gsack{k}", 0.24, 0.4, (x, -0.72, 0), CREAM, verts=8, r_top=0.25), cylinder(f"gcone{k}", 0.24, 0.32, (x, -0.72, 0.4), spice[(k + 2) % 6], verts=8, r_top=0.0)]
    g += [rod("scale_post", (0.2, -0.2, 0.47), (0.2, -0.2, 0.95), 0.02, BRASS, verts=4), box("scale_beam", 0.5, 0.03, 0.03, (0.2, -0.2, 0.95), BRASS)]
    for sx in (-1, 1):
        g += [rod(f"cord{sx}", (0.2 + sx * 0.23, -0.2, 0.95), (0.2 + sx * 0.23, -0.2, 0.68), 0.006, IRON, verts=3), cylinder(f"pan{sx}", 0.09, 0.03, (0.2 + sx * 0.23, -0.2, 0.66), BRASS, verts=8)]
    g.append(figure("buyer", (-0.6, -1.45), robe=BLACK, head="veil", hc=BLACK, hands=(None, (0.15, -0.3, 0.9))))
    g.append(figure("buyer2", (0.75, -1.4), robe=CREAM, top=MADDER, hc=WHITE, skin=SKIN_M, h=1.4))
    return bazaar_stall("prop-islamic-stall", "#C98A2E", g)


def i_forge():
    """A coppersmith's shop: the smith sits cross-legged beating a tray on a low stake, finished pots on
    shelves and trays on the wall, a brazier, a customer and her donkey at the door."""
    m = Prop("prop-islamic-forge")
    base = [box("floor", 7, 6, 0.15, color=G2), box("back_wall", 7, 0.4, 3.2, (0, 2.8, 0), G1),
            box("side_l", 0.4, 6, 1.2, (-3.3, 0, 0), G1), box("side_l_back", 0.4, 3, 3.2, (-3.3, 1.5, 0), G1),
            box("side_r", 0.4, 6, 1.2, (3.3, 0, 0), G1), box("side_r_back", 0.4, 3, 3.2, (3.3, 1.5, 0), G1),
            box("roof", 7.6, 3.0, 0.25, (0, 1.8, 3.2), G2)]
    for z in (1.3, 2.1):  # shelves of finished ware
        base.append(box(f"shelf{z}", 5.6, 0.45, 0.06, (0.2, 2.35, z), WOOD))
        for k in range(8):
            x = -2.3 + k * 0.68
            col = [COPPER, BRASS][(k + int(z * 10)) % 2]
            base += [cylinder(f"ware{z}{k}", 0.17, 0.26, (x, 2.35, z + 0.06), col, verts=8, r_top=0.12), dome(f"warel{z}{k}", 0.12, (x, 2.35, z + 0.32), col, squash=0.6, segments=6, rings=3)]
    for k in range(4):  # trays hung high on the wall
        base.append(disc(f"wtray{k}", 0.34, (-2.0 + k * 1.3, 2.57, 2.75), (0, 1, 0), [BRASS, COPPER][k % 2]))
    base += [cylinder("brazier", 0.35, 0.35, (-1.9, 0.9, 0.15), IRON, verts=10, r_top=0.4), cylinder("coals", 0.36, 0.04, (-1.9, 0.9, 0.5), FIRE, verts=10),
             seated("boy", (-1.9, 1.75, 0.15), robe=CREAM, top=CREAM, head="cap", hc=WHITE, skin=SKIN_M, hands=((-0.15, -0.4, 0.4), (0.15, -0.4, 0.4))),
             box("bellows", 0.3, 0.4, 0.14, (-1.9, 1.3, 0.2), "#6A4A30")]
    for k in range(3):  # trays stacked by the right wall
        base.append(disc(f"stack{k}", 0.4, (2.75, 0.6 + k * 0.12, 0.6), (0.15, 1, 0), [BRASS, COPPER, BRASS][k]))
    sm = (0.4, 0.75, 0.15)
    lean = 0.25
    base.append(seated("smith", sm, robe=CREAM, top=INDIGO, hc=WHITE, skin=SKIN_M, lean=lean, hands=((-0.2, -0.5, 0.15), "x")))
    S = shoulder_seated(sm, lean, 1)
    tx, ty = S[0] - 0.05, S[1] - 0.82
    base += [cylinder("stake", 0.05, 0.12, (tx, ty, 0.15), IRON, verts=6), cylinder("tray", 0.3, 0.03, (tx, ty, 0.27), COPPER, verts=14)]
    for k, (x, y, r) in enumerate(((-1.2, -1.2, 0.32), (-0.55, -1.75, 0.24), (-1.6, -2.1, 0.2), (1.6, -0.9, 0.26))):  # finished cauldrons on the floor
        base.append(cylinder(f"caul{k}", r * 0.8, r * 1.1, (x, y, 0.15), [COPPER, BRASS][k % 2], verts=10, r_top=r))
    base += [seated("tinner", (-0.6, 0.0, 0.15), rot=0.5, robe=CREAM, top=OLIVE, hc=WHITE, skin=SKIN_M, lean=0.3, hands=((-0.15, -0.45, 0.35), (0.15, -0.45, 0.35))),
             cylinder("tinpot", 0.22, 0.25, (-0.85, -0.42, 0.15), COPPER, verts=10, r_top=0.26)]
    base += [figure("customer", (1.9, -1.9), robe=BLACK, head="veil", hc=BLACK), donkey("donkey", (1.0, -4.1), color="#9A9184"),
             box("pannier_l", 0.2, 0.5, 0.35, (0.75, -4.1, 0.6), STRAW), box("pannier_r", 0.2, 0.5, 0.35, (1.25, -4.1, 0.6), STRAW)]
    m.add("base", base)
    m.add("anim_hammer", hammer_arm(S, SKIN_M, INDIGO), pivot=S)
    m.marker("marker_smoke", (-1.9, 0.9, 1.6))
    m.marker("marker_sparks", (tx, ty, 0.35))
    return m


def i_farmer():
    """A ploughman behind two zebu oxen and a wooden ard, walking the field; a veiled sower and an irrigation channel stay put."""
    m = Prop("prop-islamic-farmer")
    team = [zebu("ox_l", (-0.45, 0), color="#E2DACA"), zebu("ox_r", (0.45, 0), color="#BDB09A"), box("yoke", 1.5, 0.12, 0.12, (0, -0.65, 1.24), WOOD),
            rod("beam", (0, -0.65, 1.22), (0, 2.55, 0.2), 0.05, WOOD), box("share", 0.18, 0.5, 0.18, (0, 2.65, 0.02), IRON),
            rod("stilt", (0, 2.45, 0.15), (0.05, 3.05, 1.0), 0.04, WOOD),
            figure("ploughman", (0.12, 3.35), robe=WHITE, top=WHITE, legs=SKIN_M, head="turban", hc=WHITE, skin=SKIN_M, arm=SKIN_M, lean=0.15,
                   hands=((-0.1, -0.35, 0.95), (0.3, -0.3, 1.1))),
            rod("goad", (0.42, 3.05, 1.1), (0.55, 1.4, 1.9), 0.015, WOOD, verts=4)]
    m.add("anim_walk", team, pivot=(0, 2, 0))
    furrows = [box(f"furrow{i}", 0.25, 18, 0.06, (-3 + i * 0.6, 0, 0), "#8A7350") for i in range(10)]
    base = furrows + [box("channel_bank", 0.36, 18, 0.1, (2.85, 0, 0), "#9C8662"), box("channel", 0.2, 18, 0.03, (2.85, 0, 0.1), WATER),
                      figure("sower", (-2.55, -3), robe=BLACK, head="veil", hc=BLACK, hands=(None, (0.45, -0.1, 1.0))),
                      cylinder("basket", 0.2, 0.3, (-2.15, -3.25, 0), STRAW, verts=8, r_top=0.24)]
    m.add("base", base)
    return m


def i_wagon():
    """A camel caravan: three camels nose to tail with bags and bales, the leader on foot and a second driver behind."""
    m = Prop("prop-islamic-wagon")
    p = []
    ys = (-2.55, -0.15, 2.25)
    for k, y in enumerate(ys):
        p.append(camel(f"camel{k}", (0, y), load=["bags", "bales", "bags"][k], c1=[MADDER, OLIVE, INDIGO][k], c2=[INDIGO, MADDER, SAFFRON][k], color=[CAMEL, "#B8956A", "#CDB08A"][k]))
        if k:
            p.append(rod(f"lead{k}", (0, y - 1.3, 1.72), (0, ys[k - 1] + 0.7, 1.5), 0.015, "#5A4632", verts=4))
    p += [figure("leader", (0.45, -4.65), robe=WHITE, top=WHITE, hc=WHITE, skin=SKIN_M, sash=MADDER, hands=((-0.2, 0.25, 1.05), None)),
          rod("halter", (0.25, -4.4, 1.05), (0, -3.85, 1.62), 0.015, "#5A4632", verts=4),
          figure("driver", (-0.55, 3.95), robe=CREAM, top=OLIVE, hc=WHITE, skin=SKIN_M, hands=(None, (0.25, -0.35, 1.2))),
          rod("stick", (-0.3, 3.6, 1.2), (-0.25, 3.0, 1.9), 0.015, WOOD, verts=4)]
    m.add("base", p)
    return m


def i_bakery():
    """A bread bakery: a tandoor in a mud platform, the baker slapping a flat round of dough on the oven wall,
    an apprentice rolling dough, flatbreads stacked for sale; in the yard a blindfolded donkey turns the mill."""
    m = Prop("prop-islamic-bakery")
    tx, ty = -1.7, 1.35
    p = [box("floor", 7, 6, 0.15, color=G2), box("back", 7, 0.4, 3.0, (0, 2.8, 0), G1), box("side", 0.4, 6, 3.0, (3.3, 0, 0), G1),
         box("platform", 2.2, 1.9, 0.6, (tx, ty, 0.15), MUD), cylinder("tandoor", 0.6, 0.4, (tx, ty, 0.75), CLAY, verts=12, r_top=0.42),
         cylinder("mouth", 0.33, 0.03, (tx, ty, 1.15), POT_B, verts=12), cylinder("fire", 0.22, 0.02, (tx, ty, 1.17), FIRE, verts=10),
         box("woodpile", 0.8, 0.5, 0.35, (tx - 0.2, ty + 1.0, 0.15), WOOD)]
    for k in range(3):  # rounds stuck to the oven's mouth
        a = 0.9 + k * 0.8
        p.append(disc(f"round{k}", 0.13, (tx + 0.3 * math.cos(a), ty + 0.3 * math.sin(a), 1.12), (math.cos(a), math.sin(a), 1.4), "#D9B27A", t=0.02, verts=8))
    # the baker leans in from the east with a round on his palm
    p.append(figure("baker", (tx + 1.05, ty - 0.05, 0.15), rot=-math.pi / 2, robe=WHITE, top=WHITE, head="cap", hc=WHITE, skin=SKIN_M, lean=0.45,
                    hands=((-0.12, -0.45, 1.15), (0.12, -0.5, 1.15)), carry=[disc("dough", 0.14, (0.12, -0.6, 1.2), (0, -0.3, 1), "#E8D6AE", t=0.02, verts=8)]))
    p += [box("table", 2.2, 0.8, 0.75, (1.4, 1.7, 0.15), WOOD), box("cloth", 1.0, 0.7, 0.02, (1.9, 1.7, 0.9), CREAM)]
    for k in range(5):
        p.append(dome(f"ball{k}", 0.09, (0.6 + k * 0.2, 1.6, 0.9), "#E8D6AE", squash=0.7, segments=8, rings=4))
    for k in range(3):
        p.append(cylinder(f"stack{k}", 0.2, 0.12 + 0.04 * k, (1.65 + (k % 2) * 0.45, 1.6 + (k // 2) * 0.2, 0.92), "#D9B27A", verts=10))
    p.append(figure("apprentice", (0.9, 2.25, 0.15), rot=math.pi, robe=CREAM, top=CREAM, head="cap", hc=WHITE, skin=SKIN_M, lean=0.3, hands=((-0.15, -0.4, 0.95), (0.15, -0.4, 0.95))))
    p += [box("counter", 2.4, 0.6, 0.8, (1.1, -1.4, 0.15), MUD)]
    for k in range(4):
        p.append(cylinder(f"pile{k}", 0.22, 0.1 + 0.05 * k, (0.2 + k * 0.6, -1.4, 0.95), "#D9B27A", verts=10))
    p.append(figure("buyer", (1.4, -2.15, 0.0), robe=BLACK, head="veil", hc=BLACK))
    m.add("base", p)
    mx, my = 0.6, -3.0
    mill = [cylinder("mill_lower", 0.6, 1.0, (mx, my, 0), G3, verts=12), cylinder("mill_upper", 0.55, 0.8, (mx, my, 1.0), G2, verts=12, r_top=0.3),
            box("mill_bar", 2.4, 0.1, 0.1, (mx + 0.9, my, 1.4), WOOD), donkey("mill_donkey", (mx + 2.2, my + 0.25), color="#8A8072"),
            box("blindfold", 0.22, 0.12, 0.08, (mx + 2.2, my - 0.48, 1.18), MADDER)]
    m.add("anim_spin", mill, pivot=(mx, my, 0))
    m.marker("marker_smoke", (tx, ty, 2.2))
    return m


def i_shepherd():
    """A goatherd with a flock of black goats; the flock grazes to and fro, the herd, his staff and an acacia stay."""
    m = Prop("prop-islamic-shepherd")
    pts, rnd = scatter(15, (-4.5, 2.7), (-2.75, 2.75), 1.0, 11)
    flock = [goat(f"g{i}", (x, y), rot=rnd.uniform(-math.pi, math.pi), color=[GOAT, GOAT, "#4A3B2E", "#E6DCC8"][i % 4]) for i, (x, y) in enumerate(pts)]
    m.add("anim_graze", flock)
    base = [figure("goatherd", (4.8, 1.0), robe=CREAM, top=OLIVE, hc=WHITE, skin=SKIN_M, hands=(None, (0.3, -0.15, 1.1))),
            rod("staff", (5.12, 0.85, 0), (5.1, 0.85, 1.9), 0.025, WOOD, verts=4), box("dog", 0.26, 0.7, 0.38, (4.2, 0.1, 0.12), "#8A6A4A"),
            rod("trunk", (5.3, -1.9, 0), (5.25, -1.85, 2.1), 0.12, DARKWOOD), cylinder("crown", 0.95, 0.35, (5.25, -1.85, 2.0), "#6E7A48", verts=10, r_top=0.8)]
    m.add("base", base)
    return m


def i_crowd():
    """Townsfolk at a sebil (public fountain): men in turbans and robes, veiled women, a sherbet seller."""
    m = Prop("prop-islamic-crowd")
    people = [
        ((-2.7, -1.6), "m", INDIGO, WHITE), ((-1.75, -0.45), "w", BLACK, BLACK), ((-2.5, 1.2), "m", WHITE, MADDER), ((-1.0, 1.9), "m", OLIVE, WHITE),
        ((-0.7, -1.55), "w", PLUM, CREAM), ((0.15, 0.35), "m", CREAM, INDIGO), ((0.9, -1.75), "m", MADDER, WHITE), ((1.15, 0.95), "w", BLACK, BLACK),
        ((-0.15, 2.2), "m", WHITE, SAFFRON),
    ]
    p = []
    for i, ((x, y), kind, robe, hc) in enumerate(people):
        if kind == "m":
            p.append(figure(f"p{i}", (x, y), rot=(i * 1.3) % 6.28, robe=robe, top=robe, hc=hc, skin=[SKIN, SKIN_M][i % 2], sash=[None, SAFFRON, MADDER][i % 3], h=[1.72, 1.66, 1.78][i % 3]))
        else:
            p.append(figure(f"p{i}", (x, y), rot=(i * 1.3) % 6.28, robe=robe, head="veil", hc=hc, h=1.6))
    # the sherbet seller with his great jar slung on his back and brass cups in hand
    jar = [ball("sjar", 0.24, (0, 0.33, 1.1), BRASS, squash=1.3, seg=8, rings=5), rod("sspout", (0, 0.3, 1.35), (0.25, 0.05, 1.55), 0.025, BRASS, verts=4)]
    p.append(figure("seller", (2.45, -1.15), rot=0.4, robe=MADDER, top=MADDER, legs=TROUSER, head="cap", hc=MADDER, skin=SKIN_M, hands=(None, (0.3, -0.25, 1.05)), carry=jar))
    p += [cylinder("sebil", 0.75, 0.6, (2.3, 1.45, 0), G2, verts=8), cylinder("water", 0.62, 0.02, (2.3, 1.45, 0.6), WATER, verts=8),
          cylinder("spout", 0.12, 0.6, (2.3, 1.45, 0.6), G3, verts=8, r_top=0.08), dome("cap", 0.14, (2.3, 1.45, 1.2), G3, squash=1.2, segments=8, rings=4)]
    m.add("base", p)
    return m


def i_boat():
    """A dhow under a lateen sail: raised poop, mast raked forward, a long yard, cargo of sacks and jars, crew of three."""
    m = Prop("prop-islamic-boat")
    p = [hullx("hull", 14, 3.4, 1.15, WOOD, bow=0.9, stern=1.1), deck_slab("deck", 14, 3.4, -5.0, 4.0, 1.0, 1.18, shade(WOOD, 0.18)),
         deck_slab("poop", 14, 3.4, 3.3, 6.3, 1.1, 1.65, shade(WOOD, -0.1), shrink=0.97), box("poop_rail", 1.9, 0.08, 0.35, (0, 3.32, 1.65), WOOD),
         rod("mast", (0, -0.9, 1.1), (0, -1.5, 8.4), 0.12, WOOD, r_top=0.08), rod("yard", (0, -6.3, 4.2), (0, 4.4, 11.4), 0.09, WOOD, r_top=0.05),
         sheet("sail", ((0.15, -6.1, 4.3), (0.15, 4.2, 11.2), (0.15, 4.4, 2.6)), 0.05, "#E6DCC8"),
         rod("sheet_line", (0.15, 4.4, 2.6), (0.6, 5.2, 1.7), 0.015, "#5A4632", verts=3), rod("tiller", (0, 6.2, 1.75), (0.3, 5.0, 1.85), 0.04, WOOD, verts=4),
         box("rudder", 0.12, 0.5, 1.4, (0, 6.6, 0.3), shade(WOOD, -0.15))]
    for k in range(6):
        p.append(box(f"sack{k}", 0.7, 0.55, 0.45, (-0.75 + (k % 3) * 0.75, -3.9 + (k // 3) * 0.65, 1.18), CREAM))
    for k in range(4):
        p.append(cylinder(f"jar{k}", 0.22, 0.7, (-0.7 + (k % 2) * 1.4, 1.2 + (k // 2) * 0.7, 1.18), CLAY, verts=8, r_top=0.09))
    p += [figure("helmsman", (0.6, 5.3, 1.65), robe=WHITE, top=WHITE, hc=WHITE, skin=SKIN_M, h=1.66, hands=(None, (0.0, -0.3, 1.2))),
          seated("sailor", (-0.6, 0.2, 1.18), robe=INDIGO, top=INDIGO, hc=WHITE, skin=SKIN_M), figure("bowman", (0, -5.0, 1.1), robe=CREAM, legs=SKIN_M, hc=MADDER, skin=SKIN_M, arm=SKIN_M, h=1.6)]
    m.add("base", p)
    return m


def i_skiff():
    """A small rowing boat with two oarsmen pulling (facing aft), a net piled in the bow."""
    m = Prop("prop-islamic-skiff")
    p = [hullx("hull", 6, 1.4, 0.6, WOOD, bow=0.35, stern=0.25), box("thwart_a", 1.1, 0.25, 0.05, (0, -0.6, 0.55), shade(WOOD, 0.2)),
         box("thwart_b", 1.1, 0.25, 0.05, (0, 1.1, 0.55), shade(WOOD, 0.2)), dome("net", 0.4, (0, -2.0, 0.6), "#8A7A5A", squash=0.6, segments=8, rings=4)]
    for k, (y, col) in enumerate(((-0.6, OLIVE), (1.1, INDIGO))):
        p.append(seated(f"rower{k}", (0, y, 0.55), rot=math.pi, robe=col, top=col, hc=WHITE, skin=SKIN_M, lean=-0.15,
                        hands=((-0.35, -0.35, 0.55), (0.35, -0.35, 0.55))))
        for sx in (-1, 1):
            p.append(rod(f"oar{k}{sx}", (sx * 0.38, y + 0.35, 0.95), (sx * 0.86, y - 0.75, 0.02), 0.03, WOOD, verts=4))
            p.append(box(f"blade{k}{sx}", 0.06, 0.32, 0.12, (sx * 0.86, y - 0.8, 0.0), WOOD))
    m.add("base", p)
    return m


# ================================================================ AFRICAN
def a_walker():
    """A man of Timbuktu in a wide white boubou and an indigo turban veiled across the face."""
    m = Prop("prop-african-walker")
    f = figure("w", robe=WHITE, top=WHITE, head="tagel", hc=INDIGO, skin=SKIN_D, boubou=True, arm=SKIN_D, hands=((-0.3, -0.18, 0.8), (0.3, 0.16, 0.8)))
    m.add("base", [f, box("foot_l", 0.1, 0.22, 0.07, (-0.1, -0.24, 0), "#4A3426"), box("foot_r", 0.1, 0.22, 0.07, (0.1, 0.16, 0), "#4A3426")])
    return m


def a_matron():
    """A woman in a printed wrapper and head-tie carrying a calabash of millet on her head."""
    m = Prop("prop-african-matron")
    hz = 1.36
    cal = [cylinder("cal", 0.13, 0.12, (0, 0, hz + 0.26), "#C9A24A", verts=10, r_top=0.25), dome("millet", 0.24, (0, 0, hz + 0.38), "#D8C27A", squash=0.4, segments=10, rings=4)]
    f = figure("m", robe=SAFFRON, top=INDIGO, head="wrap", hc=MADDER, skin=SKIN_D, arm=SKIN_D, band=INDIGO, hands=((-0.15, 0.0, 1.66), None), carry=cal)
    m.add("base", [f])
    return m


def a_porter():
    """A porter with a bundle wrapped in cloth balanced on his head, both hands up to steady it."""
    m = Prop("prop-african-porter")
    hz = 1.36
    load = [cylinder("pad", 0.12, 0.05, (0, 0, hz + 0.18), STRAW, verts=8), box("bundle", 0.56, 0.46, 0.34, (0, 0, hz + 0.22), CREAM),
            box("tie", 0.58, 0.06, 0.36, (0, 0, hz + 0.21), MADDER)]
    f = figure("p", robe=OLIVE, top=OLIVE, legs=SKIN_D, head="none", skin=SKIN_D, arm=SKIN_D, hands=((-0.24, 0.0, 1.62), (0.24, 0.0, 1.62)), carry=load)
    m.add("base", [f])
    return m


def a_mule():
    """A donkey loaded with bars of Taoudenni rock salt, led by its driver."""
    m = Prop("prop-african-mule")
    p = [donkey("donkey", (-0.12, 0.35), s=1.05)]
    for sx in (-1, 1):
        for k in range(2):
            p.append(box(f"slab{sx}{k}", 0.06, 0.9, 0.36, (-0.12 + sx * (0.27 + 0.07 * k), 0.35, 0.56 + 0.05 * k), SALT))
        p.append(box(f"cord{sx}", 0.18, 0.05, 0.4, (-0.12 + sx * 0.3, 0.35, 0.56), "#5A4632"))
    p += [box("slab_top", 0.5, 0.9, 0.07, (-0.12, 0.35, 1.08), SALT), box("band", 0.52, 0.05, 0.09, (-0.12, 0.35, 1.07), "#5A4632")]
    p += [figure("drv", (0.5, -1.2), robe=INDIGO, top=INDIGO, head="tagel", hc=INDIGO, skin=SKIN_D, arm=SKIN_D, hands=((-0.2, 0.22, 1.0), None)),
          rod("rope", (0.3, -0.98, 1.0), (-0.12, -0.45, 1.15), 0.015, "#5A4632", verts=4)]
    m.add("base", p)
    return m


def a_litter():
    """A chief carried in a hammock slung from a pole by four bearers, shaded by a great red-and-gold umbrella."""
    m = Prop("prop-african-litter")
    p = [rod("pole", (0, -2.24, 1.45), (0, 2.24, 1.45), 0.055, DARKWOOD), vault("hammock", 0.42, 1.9, (0, 0, 1.15), "#C9A24A", verts=12, down=True)]
    for sy in (-1, 1):
        p.append(rod(f"sling{sy}", (0, sy * 0.95, 1.15), (0, sy * 1.15, 1.45), 0.02, "#5A4632", verts=4))
    p += [seated("chief", (0, 0.15, 0.82), robe="#C9A24A", top=MADDER, head="cap", hc="#D9B24A", skin=SKIN_D, arm=SKIN_D, lean=-0.45),
          rod("shaft", (0, -0.55, 1.45), (0, -0.4, 2.5), 0.025, DARKWOOD, verts=4), dome("umbrella", 0.82, (0, -0.4, 2.2), MADDER, squash=0.38, segments=12, rings=4),
          cylinder("fringe", 0.84, 0.12, (0, -0.4, 2.1), "#D9B24A", verts=12), dome("umbrella_top", 0.08, (0, -0.4, 2.5), "#D9B24A", squash=1.5, segments=6, rings=3)]
    for i, (sy, sx) in enumerate([(-1.98, 0.16), (-1.42, -0.16), (1.42, 0.16), (1.98, -0.16)]):
        hands = ((-0.15, 0, 1.45), None) if sx > 0 else (None, (0.15, 0, 1.45))
        p.append(figure(f"b{i}", (sx, sy), robe=[INDIGO, CREAM][i % 2], top=SKIN_D, legs=SKIN_D, head="none", skin=SKIN_D, arm=SKIN_D, hands=hands, h=1.68))
    m.add("base", p)
    return m


def a_handcart():
    """A woman with a great basket of millet on her head and a girl beside her with a smaller one."""
    m = Prop("prop-african-handcart")
    hz = 1.36
    big = [cylinder("pad", 0.12, 0.05, (0, 0, hz + 0.18), STRAW, verts=8), cylinder("basket", 0.24, 0.26, (0, 0, hz + 0.21), STRAW, verts=10, r_top=0.4),
           dome("grain", 0.39, (0, 0, hz + 0.47), "#D8B95A", squash=0.35, segments=10, rings=4)]
    p = [figure("woman", (0, -0.45), robe=INDIGO, top=SAFFRON, head="wrap", hc=SAFFRON, skin=SKIN_D, arm=SKIN_D, band=WHITE,
                hands=((-0.3, 0.0, 1.66), (0.3, 0.0, 1.66)), carry=big)]
    hz2 = 1.36 * 1.2 / 1.72
    small = [cylinder("sbasket", 0.12, 0.14, (0, 0, hz2 + 0.15), STRAW, verts=8, r_top=0.2), dome("sgrain", 0.19, (0, 0, hz2 + 0.29), "#D8B95A", squash=0.4, segments=8, rings=4)]
    p.append(figure("girl", (0.22, 0.75), robe=MADDER, top=MADDER, head="hair", hc="#1E1814", skin=SKIN_D, arm=SKIN_D, h=1.2, hands=((-0.05, 0.0, 1.17), None), carry=small))
    m.add("base", p)
    return m


def a_cart():
    """Two pack donkeys nose to tail with sacks of grain, driven by a man with a stick."""
    m = Prop("prop-african-cart")
    p = []
    for k, (x, y) in enumerate(((0.0, -1.75), (0.15, 0.4))):
        p.append(donkey(f"donkey{k}", (x, y), color=[DONKEY, "#7A6E60"][k], s=1.05))
        for sx in (-1, 1):
            p.append(box(f"sack{k}{sx}", 0.24, 0.55, 0.42, (x + sx * 0.34, y, 0.55), [CREAM, "#C9B48E"][k]))
        p.append(rod(f"bundle{k}", (x - 0.3, y + 0.05, 1.18), (x + 0.3, y + 0.05, 1.18), 0.13, [INDIGO, MADDER][k], verts=8))
        if k:
            p.append(rod("tether", (x, y - 1.0, 1.15), (0, -1.75 + 0.5, 1.05), 0.015, "#5A4632", verts=4))
    p += [figure("drv", (-0.25, 2.2), robe=WHITE, top=WHITE, boubou=True, head="cap", hc=WHITE, skin=SKIN_D, arm=SKIN_D, hands=(None, (0.3, -0.35, 1.05))),
          rod("stick", (0.05, 1.85, 1.05), (0.1, 1.2, 1.7), 0.015, WOOD, verts=4),
          figure("boy", (0.85, -1.55), robe=OLIVE, top=OLIVE, legs=SKIN_D, head="none", skin=SKIN_D, arm=SKIN_D, h=1.35)]
    m.add("base", p)
    return m


def a_stall_fruit():
    g = []
    for k in range(4):  # calabashes of millet and sorghum
        x, y = -0.95 + k * 0.45, -0.45
        g += [cylinder(f"cal{k}", 0.12, 0.12, (x, y, 0.03), "#C9A24A", verts=10, r_top=0.2), dome(f"grain{k}", 0.19, (x, y, 0.15), ["#D8C27A", "#B5803A", "#D8C27A", "#9A6A40"][k], squash=0.45, segments=8, rings=4)]
    for k in range(3):  # piles of kola nuts, red and white
        x = -0.9 + k * 0.35
        g += [dome(f"kola{k}", 0.15, (x, 0.1, 0.03), ["#A6493A", "#E6DCC0", "#A6493A"][k], squash=0.6, segments=8, rings=4)]
    for k in range(3):  # shea butter in bowls
        x = 0.05 + k * 0.32
        g += [cylinder(f"bowl{k}", 0.1, 0.1, (x, -0.45, 0.03), CLAY_D, verts=8, r_top=0.15), dome(f"shea{k}", 0.13, (x, -0.45, 0.13), "#EFE6C8", squash=0.8, segments=8, rings=4)]
    g += [cylinder("basket", 0.22, 0.35, (-0.2, 0.55, 0.03), STRAW, verts=10, r_top=0.26)]
    return mat_stall("prop-african-stall-fruit", g)


def a_stall_pots():
    g = []
    for k in range(5):  # water jars
        x, y = -1.0 + (k % 3) * 0.48, -0.45 + (k // 3) * 0.5
        col = [CLAY, CLAY_D, POT_B][k % 3]
        g += [cylinder(f"jb{k}", 0.14, 0.18, (x, y, 0.03), col, verts=10, r_top=0.24), dome(f"js{k}", 0.24, (x, y, 0.21), col, squash=0.75, segments=10, rings=4),
              cylinder(f"jn{k}", 0.09, 0.08, (x, y, 0.38), col, verts=8, r_top=0.11)]
    for k in range(3):  # cooking pots, upside down
        g.append(dome(f"pot{k}", 0.2, (0.2 + k * 0.32, -0.5, 0.03), [CLAY_D, POT_B, CLAY][k], squash=0.9, segments=8, rings=4))
    g += [dome("stack_a", 0.22, (0.05, 0.25, 0.03), CLAY, squash=0.8, segments=8, rings=4), dome("stack_b", 0.17, (0.05, 0.25, 0.2), CLAY_D, squash=0.8, segments=8, rings=4)]
    return mat_stall("prop-african-stall-pots", g)


def a_stall_cloth():
    g = [rod("line", (-1.2, 0.95, 1.65), (1.2, 0.95, 1.65), 0.015, "#5A4632", verts=4)]
    cols = [(INDIGO, WHITE), (SAFFRON, MADDER), (WHITE, "#2F3E5C"), (MADDER, "#D9B24A")]
    for c, (a, b) in enumerate(cols):  # strip-woven cloths: narrow strips sewn edge to edge, hung on the line
        x0 = -1.02 + c * 0.56
        for k in range(4):
            g.append(box(f"strip{c}{k}", 0.12, 0.03, 1.1, (x0 + k * 0.12, 0.92, 0.55), a if k % 2 == 0 else b))
    for k in range(4):  # folded cloths on the mat
        g.append(box(f"fold{k}", 0.5, 0.4, 0.08, (-0.85 + (k % 2) * 0.55, -0.35, 0.03 + (k // 2) * 0.08), [INDIGO, WHITE, SAFFRON, MADDER][k]))
    g += [box("fold_s", 0.5, 0.4, 0.2, (0.3, -0.45, 0.03), "#2F3E5C"), box("fold_t", 0.5, 0.06, 0.21, (0.3, -0.45, 0.03), WHITE)]
    return mat_stall("prop-african-stall-cloth", g)


def a_stall():
    """Salt and gold: slabs of Saharan salt stacked and leaning, a merchant weighing gold dust on a small balance."""
    g = []
    for k in range(4):  # a stack of slabs
        g.append(box(f"slab{k}", 1.0, 0.4, 0.07, (-0.6, -0.35, 0.03 + k * 0.07), SALT))
        g.append(box(f"seam{k}", 1.01, 0.41, 0.012, (-0.6, -0.35, 0.03 + k * 0.07 + 0.06), "#B9A88C"))
    for k in range(3):  # slabs leaning upright
        s = box(f"lean{k}", 0.07, 0.42, 1.0, (-1.08 + k * 0.12, 0.4 - k * 0.12, 0.03), SALT)
        tilt(s, 0, 0.12, 0.2)
        g.append(s)
    g += [box("cloth", 0.7, 0.5, 0.02, (0.35, -0.3, 0.03), INDIGO), rod("bal_post", (0.35, -0.2, 0.05), (0.35, -0.2, 0.45), 0.012, BRASS, verts=4),
          box("bal_beam", 0.36, 0.02, 0.02, (0.35, -0.2, 0.44), BRASS)]
    for sx in (-1, 1):
        g += [rod(f"bal_cord{sx}", (0.35 + sx * 0.17, -0.2, 0.44), (0.35 + sx * 0.17, -0.2, 0.25), 0.005, IRON, verts=3), cylinder(f"bal_pan{sx}", 0.06, 0.02, (0.35 + sx * 0.17, -0.2, 0.23), BRASS, verts=8)]
    for k in range(4):  # brass weights and a pouch of gold dust
        g.append(box(f"wt{k}", 0.04 + 0.01 * k, 0.04 + 0.01 * k, 0.04, (0.15 + k * 0.1, -0.45, 0.05), BRASS))
    g.append(dome("pouch", 0.07, (0.62, -0.45, 0.05), "#D9B24A", squash=1.2, segments=6, rings=3))
    g.append(figure("buyer", (0.3, -1.42), robe=WHITE, top=WHITE, boubou=True, head="cap", hc=WHITE, skin=SKIN_D, arm=SKIN_D, hands=(None, (0.25, -0.3, 0.9))))
    vendor = seated("vendor", (0.4, 0.45, 0.03), robe=INDIGO, top=INDIGO, head="tagel", hc=INDIGO, skin=SKIN_D, arm=INDIGO, hands=((-0.15, -0.45, 0.35), (0.15, -0.45, 0.35)))
    return mat_stall("prop-african-stall", g, vendor=vendor)


def a_forge():
    """A village forge under a thatched shade: drum bellows worked by an apprentice, a clay tuyere into the hearth,
    the smith on a low stool striking iron on a stone anvil; hoes and spear blades laid out for a customer."""
    m = Prop("prop-african-forge")
    base = [box("yard", 7, 6, 0.08, color=G2)]
    for sx in (-3.1, 0, 3.1):
        for sy in (0.6, 2.7):
            base.append(rod(f"post{sx}{sy}", (sx, sy, 0), (sx, sy, 2.6), 0.08, DARKWOOD))
    base += [box("beam_a", 6.6, 0.12, 0.12, (0, 0.6, 2.55), DARKWOOD), box("beam_b", 6.6, 0.12, 0.12, (0, 2.7, 2.55), DARKWOOD)]
    shade_roof = box("thatch", 7.4, 3.0, 0.3, (0, 1.65, 2.65), THATCH)
    tilt(shade_roof, -0.1)
    base.append(shade_roof)
    hx, hy = -1.0, 1.4
    base += [cylinder("hearth", 0.5, 0.3, (hx, hy, 0.08), MUD, verts=10, r_top=0.42), cylinder("coals", 0.36, 0.03, (hx, hy, 0.38), FIRE, verts=10),
             rod("tuyere", (hx - 1.1, hy + 0.1, 0.25), (hx - 0.3, hy, 0.35), 0.07, CLAY_D)]
    for k, dy in enumerate((-0.25, 0.45)):  # drum bellows: two clay pots under leather, pumped with sticks
        bx, by = hx - 1.55, hy + dy
        base += [cylinder(f"bpot{k}", 0.3, 0.3, (bx, by, 0.08), CLAY_D, verts=10, r_top=0.26), dome(f"bskin{k}", 0.27, (bx, by, 0.38), "#7A5236", squash=0.3, segments=8, rings=3),
                 rod(f"bstick{k}", (bx, by, 0.42), (bx, by, 1.05 + 0.15 * k), 0.025, WOOD, verts=4)]
    base.append(seated("apprentice", (hx - 2.25, hy + 0.1, 0.08), rot=math.pi / 2 + math.pi, robe=OLIVE, top=SKIN_D, head="none", skin=SKIN_D, arm=SKIN_D,
                       hands=((-0.3, -0.45, 0.85), (0.3, -0.45, 0.95))))
    base += [dome("charcoal", 0.45, (-2.3, 2.3, 0.08), POT_B, squash=0.6, segments=8, rings=4), box("logs", 0.9, 0.4, 0.3, (1.2, 2.3, 0.08), WOOD)]
    sm = (0.5, 0.75, 0.38)
    lean = 0.2
    base += [box("stool", 0.42, 0.4, 0.3, (sm[0], sm[1], 0.08), WOOD),
             seated("smith", sm, robe=INDIGO, top=SKIN_D, head="cap", hc=MADDER, skin=SKIN_D, arm=SKIN_D, lean=lean, hands=((-0.25, -0.55, 0.0), "x"))]
    S = shoulder_seated(sm, lean, 1)
    ax, ay = S[0] - 0.02, S[1] - 0.82
    base += [cylinder("stump", 0.24, 0.42, (ax, ay, 0.08), DARKWOOD, verts=8), box("anvil", 0.3, 0.24, 0.12, (ax, ay, 0.5), "#6A665E"),
             box("bloom", 0.14, 0.08, 0.04, (ax, ay, 0.62), FIRE), rod("tongs", (ax - 0.4, ay + 0.35, 0.3), (ax - 0.02, ay, 0.64), 0.015, IRON, verts=4)]
    for k in range(5):  # finished hoes and spear blades on a mat
        base.append(box(f"hoe{k}", 0.16, 0.22, 0.03, (1.9 + (k % 3) * 0.3, -0.9 + (k // 3) * 0.35, 0.1), IRON))
        base.append(rod(f"haft{k}", (1.9 + (k % 3) * 0.3, -0.8 + (k // 3) * 0.35, 0.12), (1.9 + (k % 3) * 0.3, -0.35 + (k // 3) * 0.35, 0.12), 0.02, WOOD, verts=4))
    base += [box("goods_mat", 1.3, 1.0, 0.02, (2.2, -0.8, 0.08), STRAW),
             figure("customer", (2.3, -2.3, 0.08), robe=WHITE, top=WHITE, boubou=True, head="tagel", hc=INDIGO, skin=SKIN_D, arm=SKIN_D),
             figure("wife", (-1.6, -2.1, 0.08), rot=0.6, robe=MADDER, top=SAFFRON, head="wrap", hc=INDIGO, skin=SKIN_D, arm=SKIN_D, band=WHITE)]
    m.add("base", base)
    m.add("anim_hammer", hammer_arm(S, SKIN_D, SKIN_D), pivot=S)
    m.marker("marker_smoke", (hx, hy, 3.4))
    m.marker("marker_sparks", (ax, ay, 0.7))
    return m


def a_farmer():
    """A hoeing party: three men bent over short-handled hoes work up the ridges, a drummer behind them keeping time;
    the ridged field, a stand of millet and a woman bringing water stay put."""
    m = Prop("prop-african-farmer")
    team = []
    for k, x in enumerate((-1.2, 0.0, 1.2)):
        y = 0.1 * (k % 2)
        # hands given before the 0.7 rad stoop; after it they sit at about (x +- 0.1, y - 0.55, 0.65)
        team.append(figure(f"hoer{k}", (x, y), robe=[INDIGO, OLIVE, WHITE][k], top=SKIN_D, legs=SKIN_D, head="none", skin=SKIN_D, arm=SKIN_D, lean=0.7,
                           hands=((-0.06, -0.61, 1.07), (0.12, -0.61, 1.07))))
        team += [rod(f"haft{k}", (x + 0.04, y - 0.5, 0.7), (x + 0.06, y - 1.0, 0.1), 0.025, WOOD, verts=4), box(f"blade{k}", 0.18, 0.08, 0.16, (x + 0.06, y - 1.04, 0.0), IRON)]
    drum = [cylinder("drum", 0.16, 0.45, (0.0, -0.25, 0.75), "#7A4A2A", verts=8, r_top=0.12)]
    team.append(figure("drummer", (0.0, 1.6), robe=WHITE, top=WHITE, legs=SKIN_D, head="cap", hc=MADDER, skin=SKIN_D, arm=SKIN_D, hands=((-0.12, -0.3, 1.25), (0.12, -0.3, 1.25)), carry=drum))
    m.add("anim_walk", team, pivot=(0, 0, 0))
    ridges = [box(f"ridge{i}", 0.38, 18, 0.18, (-2.7 + i * 0.6, 0, 0), "#8A6A48") for i in range(10)]
    base = ridges
    rnd = random.Random(5)
    for k in range(10):  # a stand of millet at the head of the field
        x, y = -2.7 + (k % 5) * 0.3 + rnd.uniform(-0.05, 0.05), 7.3 + (k // 5) * 0.9
        base += [rod(f"millet{k}", (x, y, 0.1), (x, y, 2.1 + rnd.uniform(-0.2, 0.2)), 0.03, "#9A9A50", verts=4), rod(f"head{k}", (x, y, 1.95), (x, y, 2.35), 0.05, "#B5803A", verts=5)]
    hz = 1.36
    cal = [cylinder("cal", 0.12, 0.12, (0, 0, hz + 0.26), "#C9A24A", verts=8, r_top=0.22), dome("water", 0.2, (0, 0, hz + 0.37), WATER, squash=0.15, segments=8, rings=3)]
    base.append(figure("woman", (2.55, -6.0), robe=SAFFRON, top=INDIGO, head="wrap", hc=MADDER, skin=SKIN_D, arm=SKIN_D, band=INDIGO, hands=((-0.15, 0, 1.66), None), carry=cal))
    m.add("base", base)
    return m


def a_wagon():
    """The azalai: a salt caravan of three camels carrying slabs of rock salt, a veiled Tuareg leading and another behind."""
    m = Prop("prop-african-wagon")
    p = []
    ys = (-2.55, -0.15, 2.25)
    for k, y in enumerate(ys):
        p.append(camel(f"camel{k}", (0, y), load="salt", c1=[INDIGO, MADDER, "#5A4632"][k], color=[CAMEL, "#D2BC98", "#B8956A"][k]))
        if k:
            p.append(rod(f"lead{k}", (0, y - 1.3, 1.72), (0, ys[k - 1] + 0.7, 1.5), 0.015, "#5A4632", verts=4))
    p += [figure("leader", (0.45, -4.65), robe=INDIGO, top=INDIGO, head="tagel", hc=INDIGO, skin=SKIN_M, hands=((-0.2, 0.25, 1.05), None)),
          rod("halter", (0.25, -4.4, 1.05), (0, -3.85, 1.62), 0.015, "#5A4632", verts=4),
          figure("driver", (-0.55, 3.95), robe=WHITE, top=WHITE, boubou=True, head="tagel", hc=BLACK, skin=SKIN_M, arm=SKIN_M, hands=(None, (0.25, -0.35, 1.2))),
          rod("stick", (-0.3, 3.6, 1.2), (-0.25, 3.0, 1.9), 0.015, WOOD, verts=4)]
    m.add("base", p)
    return m


def a_bakery():
    """A compound yard where women pound millet in tall wooden mortars, a granary under its thatch hat, and a pot
    of millet porridge on the three-stone hearth stirred with a paddle (the paddle turns: anim_spin)."""
    m = Prop("prop-african-bakery")
    p = [box("yard", 7, 6, 0.06, color=G2), box("wall", 7, 0.35, 1.5, (0, 2.85, 0), MUD), box("wall_side", 0.35, 3.0, 1.5, (-3.3, 1.5, 0), MUD),
         cylinder("granary", 0.8, 1.5, (2.45, 1.75, 0.35), MUD, verts=10, r_top=0.72), cylinder("granary_hat", 1.0, 0.95, (2.45, 1.75, 1.75), THATCH, verts=10, r_top=0.05)]
    for k in range(3):
        a = k * math.tau / 3
        p.append(cylinder(f"gstone{k}", 0.16, 0.35, (2.45 + 0.45 * math.cos(a), 1.75 + 0.45 * math.sin(a), 0), G3, verts=6))
    # two mortars, each with a woman driving a tall pestle; one pestle up, one down
    for k, (mx, my, up) in enumerate(((-1.3, 0.3, True), (0.45, -0.35, False))):
        p += [cylinder(f"mortar{k}", 0.27, 0.62, (mx, my, 0.06), DARKWOOD, verts=10, r_top=0.23), cylinder(f"grain{k}", 0.2, 0.02, (mx, my, 0.68), "#D8C27A", verts=8)]
        z0 = 1.25 if up else 0.5
        p.append(rod(f"pestle{k}", (mx, my, z0), (mx, my, z0 + 2.0), 0.05, WOOD, verts=6))
        hz = z0 + (0.85 if up else 0.65)
        p.append(figure(f"pounder{k}", (mx, my + 0.55), robe=[SAFFRON, INDIGO][k], top=[INDIGO, MADDER][k], head="wrap", hc=[MADDER, SAFFRON][k], skin=SKIN_D, arm=SKIN_D,
                        band=[INDIGO, WHITE][k], hands=((-0.05, -0.5, hz - 0.15), (0.05, -0.5, hz)), lean=0.1))
    p += [seated("winnower", (1.85, -1.4, 0.06), rot=0.4, robe=MADDER, top=OLIVE, head="wrap", hc=INDIGO, skin=SKIN_D, arm=SKIN_D,
                 hands=((-0.3, -0.4, 0.4), (0.3, -0.4, 0.4))), disc("winnow_tray", 0.38, (1.68, -1.75, 0.42), (0.1, -0.2, 1), STRAW, t=0.04, verts=10),
          cylinder("grain_heap", 0.35, 0.12, (2.5, -2.2, 0.06), "#D8C27A", verts=8, r_top=0.05)]
    for k in range(3):  # baskets of grain against the wall
        p += [cylinder(f"basket{k}", 0.24, 0.3, (-2.6 + k * 0.55, 2.35, 0.06), STRAW, verts=8, r_top=0.28), dome(f"bgrain{k}", 0.27, (-2.6 + k * 0.55, 2.35, 0.36), "#D8C27A", squash=0.35, segments=8, rings=3)]
    px, py = -1.9, -1.75
    for k in range(3):
        a = k * math.tau / 3 + 0.5
        p.append(box(f"hstone{k}", 0.2, 0.2, 0.22, (px + 0.33 * math.cos(a), py + 0.33 * math.sin(a), 0.06), G3))
    p += [cylinder("embers", 0.22, 0.04, (px, py, 0.06), FIRE, verts=8), cylinder("pot", 0.28, 0.25, (px, py, 0.26), POT_B, verts=10, r_top=0.36),
          cylinder("pot_top", 0.36, 0.12, (px, py, 0.51), POT_B, verts=10, r_top=0.3), cylinder("porridge", 0.29, 0.02, (px, py, 0.6), "#D8C9A0", verts=10)]
    p.append(figure("cook", (px + 0.8, py + 0.05), rot=math.pi / 2, robe=INDIGO, top=SAFFRON, head="wrap", hc=SAFFRON, skin=SKIN_D, arm=SKIN_D, band=MADDER,
                    lean=0.25, hands=((-0.08, -0.45, 1.05), (0.08, -0.5, 1.15))))
    m.add("base", p)
    paddle = [rod("paddle", (px + 0.12, py, 0.45), (px + 0.38, py, 1.4), 0.025, WOOD, verts=4), box("paddle_blade", 0.1, 0.03, 0.2, (px + 0.1, py, 0.42), WOOD)]
    m.add("anim_spin", paddle, pivot=(px, py, 0))
    m.marker("marker_smoke", (px, py, 1.6))
    return m


def a_shepherd():
    """A Fulani herder in his conical hat with long-horned cattle; the herd grazes to and fro, the herder, a boy and a tree stay."""
    m = Prop("prop-african-shepherd")
    pts, rnd = scatter(8, (-4.3, 2.6), (-2.0, 2.0), 1.9, 4)
    cols = ["#E8E0D0", "#8A4A30", "#C9B79A", "#3A302A", "#A86A40", "#E8E0D0", "#6E4A32", "#D8CCB8"]
    herd = [zebu(f"c{i}", (x, y), rot=rnd.uniform(-math.pi, math.pi), color=cols[i % len(cols)], long_horns=True) for i, (x, y) in enumerate(pts)]
    m.add("anim_graze", herd)
    base = [figure("herder", (5.0, 0.9), robe=INDIGO, top=INDIGO, head="cone", hc=STRAW, skin=SKIN_M, arm=SKIN_M,
                   hands=((-0.45, 0.1, 1.42), (0.45, 0.1, 1.42))),
            rod("staff", (4.4, 1.0, 1.4), (5.6, 1.0, 1.4), 0.025, WOOD, verts=4),
            figure("boy", (4.3, -0.6), robe=WHITE, top=WHITE, legs=SKIN_M, head="none", skin=SKIN_M, arm=SKIN_M, h=1.3),
            rod("trunk", (5.4, -2.2, 0), (5.35, -2.1, 2.0), 0.14, DARKWOOD), cylinder("crown", 0.95, 0.4, (5.35, -2.1, 1.9), "#6E7A48", verts=10, r_top=0.75)]
    m.add("base", base)
    return m


def a_crowd():
    """Market-day crowd: men in boubous and indigo turbans, women in wrappers and head-ties, a griot with his kora."""
    m = Prop("prop-african-crowd")
    people = [((-2.7, -1.5), "m", WHITE, INDIGO), ((-1.8, -0.3), "w", SAFFRON, MADDER), ((-2.5, 1.3), "m", INDIGO, WHITE), ((-1.0, 2.0), "w", MADDER, INDIGO),
              ((-0.7, -1.6), "m", "#B5A88A", INDIGO), ((0.2, 0.4), "w", INDIGO, SAFFRON), ((1.0, -1.7), "m", WHITE, BLACK), ((1.2, 1.1), "w", OLIVE, MADDER),
              ((2.6, -0.6), "m", INDIGO, INDIGO), ((2.3, 1.9), "w", TEAL, SAFFRON)]
    p = []
    for i, ((x, y), kind, robe, hc) in enumerate(people):
        if kind == "m":
            p.append(figure(f"p{i}", (x, y), rot=(i * 1.3) % 6.28, robe=robe, top=robe, boubou=True, head=["tagel", "cap", "turban"][i % 3], hc=hc, skin=SKIN_D, arm=SKIN_D, h=[1.74, 1.68, 1.8][i % 3]))
        else:
            p.append(figure(f"p{i}", (x, y), rot=(i * 1.3) % 6.28, robe=robe, top=hc, head="wrap", hc=hc, skin=SKIN_D, arm=SKIN_D, band=WHITE, h=1.62))
    kora = [dome("kora_gourd", 0.2, (0, -0.35, 0.3), "#C9A24A", squash=1.0, segments=8, rings=4), rod("kora_neck", (0, -0.35, 0.4), (0, -0.5, 1.2), 0.025, DARKWOOD, verts=4)]
    p.append(seated("griot", (0.6, 2.25), robe=WHITE, top=WHITE, head="cap", hc=MADDER, skin=SKIN_D, arm=SKIN_D, hands=((-0.15, -0.45, 0.65), (0.15, -0.35, 0.4)), carry=kora))
    m.add("base", p)
    return m


def a_boat():
    """A long Niger pirogue under a vaulted palm-mat shelter, poled from bow and stern, with sacks and a passenger."""
    m = Prop("prop-african-boat")
    p = [hullx("hull", 14, 2.0, 0.7, DARKWOOD, bow=0.6, stern=0.6, fine=0.06, keel=0.6), deck_slab("band", 14, 2.0, -4.6, 4.6, 0.5, 0.6, MADDER, fine=0.06, shrink=1.03),
         deck_slab("floor", 14, 2.0, -4.8, 4.8, 0.6, 0.73, shade(DARKWOOD, 0.2), fine=0.06, shrink=0.85), vault("shelter", 0.85, 4.2, (0, 0.6, 0.7), STRAW, verts=12)]
    for k in range(4):
        p.append(rod(f"hoop{k}", (-0.86, -1.4 + k * 1.33, 0.7), (0.86, -1.4 + k * 1.33, 0.7), 0.02, DARKWOOD, verts=4))
    for k in range(4):
        p.append(box(f"sack{k}", 0.6, 0.5, 0.4, (-0.35 + (k % 2) * 0.7, -2.6 - (k // 2) * 0.6, 0.7), [CREAM, "#C9B48E"][k % 2]))
    p += [figure("poler_s", (0.15, 5.4, 0.85), robe=WHITE, top=SKIN_D, legs=SKIN_D, head="cap", hc=WHITE, skin=SKIN_D, arm=SKIN_D, lean=0.3,
                 hands=((0.25, -0.3, 1.45), (0.3, -0.3, 1.1))),
          rod("pole_s", (0.45, 5.05, 2.9), (0.95, 2.8, 0.0), 0.03, WOOD, verts=4),
          figure("poler_b", (-0.15, -5.3, 0.85), robe=INDIGO, top=SKIN_D, legs=SKIN_D, head="none", skin=SKIN_D, arm=SKIN_D, lean=0.3,
                 hands=((-0.3, -0.3, 1.1), (-0.2, -0.3, 1.45))),
          rod("pole_b", (-0.4, -5.6, 2.9), (-0.95, -3.4, 0.0), 0.03, WOOD, verts=4),
          seated("passenger", (0.2, 3.3, 0.7), robe=SAFFRON, top=INDIGO, head="wrap", hc=MADDER, skin=SKIN_D, arm=SKIN_D),
          cylinder("jar", 0.2, 0.5, (-0.45, 3.3, 0.7), CLAY, verts=8, r_top=0.1)]
    m.add("base", p)
    return m


def a_skiff():
    """A small dugout canoe with a kneeling paddler and a conical fish trap."""
    m = Prop("prop-african-skiff")
    p = [hullx("hull", 5.8, 0.9, 0.42, DARKWOOD, bow=0.25, stern=0.2, fine=0.08, keel=0.65),
         seated("paddler", (0, 1.4, 0.38), robe=INDIGO, top=SKIN_D, head="none", skin=SKIN_D, arm=SKIN_D, lean=0.2, hands=((0.1, -0.35, 0.85), (0.35, -0.3, 0.45))),
         rod("paddle", (0.25, 1.05, 1.3), (0.42, 0.95, 0.15), 0.02, WOOD, verts=4), box("paddle_blade", 0.04, 0.16, 0.4, (0.42, 0.95, 0.0), WOOD),
         rod("trap", (0, -1.0, 0.55), (0, -2.1, 0.55), 0.28, STRAW, verts=8, r_top=0.03), dome("catch", 0.18, (0, -0.2, 0.4), "#8A9AA0", squash=0.5, segments=6, rings=3)]
    m.add("base", p)
    return m


# ================================================================ VENETIAN
def v_boat():
    """A peata: a broad flat Venetian cargo barge loaded with wine barrels, a cloth-covered tiemo at the stern,
    rowed standing in the Venetian way by a man fore and a man aft."""
    m = Prop("prop-venetian-boat")
    p = [hullx("hull", 13.6, 3.4, 1.1, "#4A3A2E", bow=0.75, stern=0.45, fine=0.2, keel=0.7), deck_slab("deck", 13.6, 3.4, -5.4, 5.4, 1.0, 1.13, shade(WOOD, 0.15), fine=0.2),
         deck_slab("wale", 13.6, 3.4, -4.6, 4.6, 0.82, 0.96, "#7A2E2A", fine=0.2, shrink=1.03), vault("tiemo", 0.85, 1.9, (0, 4.1, 1.12), "#7A2E2A", verts=12)]
    for k in range(12):  # barrels lying athwartships, two tiers
        tier = k // 8
        i = k % 8
        x = -0.55 + (i % 2) * 1.1 if tier == 0 else 0.0
        y = -3.6 + (i // 2) * 0.95 + (0.45 if tier else 0)
        z = 1.12 + 0.4 + tier * 0.72
        p.append(rod(f"barrel{k}", (x - 0.45, y, z), (x + 0.45, y, z), 0.38, "#8A6A4A", verts=10))
        p.append(rod(f"hoop{k}", (x - 0.06, y, z), (x + 0.06, y, z), 0.395, IRON, verts=10))
    p += [box("forcola_a", 0.14, 0.2, 0.6, (1.45, 5.4, 1.1), WOOD), box("forcola_b", 0.14, 0.2, 0.6, (-1.4, -4.6, 1.1), WOOD),
          figure("rower_aft", (0.5, 5.75, 1.1), robe="#ECE6D6", top="#ECE6D6", legs="#3A3A44", head="cap", hc="#7A2E2A", lean=0.25, hands=((0.15, -0.4, 1.2), (0.6, -0.4, 1.25))),
          rod("oar_aft", (0.95, 5.2, 1.85), (1.95, 0.6, 0.0), 0.035, WOOD, verts=4),
          figure("rower_fore", (-0.5, -4.25, 1.1), robe="#55687E", top="#55687E", legs="#3A3A44", head="hair", hc="#3A2A1E", lean=0.25, hands=((-0.6, -0.4, 1.25), (-0.15, -0.4, 1.2))),
          rod("oar_fore", (-0.95, -4.8, 1.85), (-1.95, -6.8, 0.0), 0.035, WOOD, verts=4)]
    m.add("base", p)
    return m


def v_skiff():
    """A black gondola with its toothed iron ferro at the bow, a cushioned seat, and the gondolier standing
    on the stern rowing on the forcola."""
    m = Prop("prop-venetian-skiff")
    GB = "#1E1E22"
    p = [hullx("hull", 6.3, 1.15, 0.42, GB, bow=0.55, stern=0.45, fine=0.12, keel=0.6, n=11), box("floor", 0.9, 3.0, 0.03, (0, 0.1, 0.42), "#3A2A22"),
         box("seat", 0.8, 0.7, 0.28, (0, 0.2, 0.42), "#7A2E2A"), box("seat_back", 0.8, 0.12, 0.42, (0, 0.6, 0.42), "#7A2E2A"),
         box("ferro", 0.04, 0.16, 0.62, (0, -3.0, 0.82), "#C8C8C0"), box("ferro_top", 0.04, 0.3, 0.12, (0, -3.02, 1.36), "#C8C8C0")]
    for k in range(6):  # the six teeth of the ferro, pointing forward
        p.append(box(f"tooth{k}", 0.03, 0.16, 0.035, (0, -3.12, 0.88 + k * 0.08), "#C8C8C0"))
    p += [box("stern_deck", 0.6, 0.7, 0.05, (0, 2.55, 0.62), "#3A2A22"), box("forcola", 0.08, 0.14, 0.42, (0.48, 1.85, 0.52), WOOD),
          seated("passenger", (0, 0.05, 0.7), robe="#55687E", top="#7D5A6B", head="veil", hc="#E6DCC8", hands=((-0.15, -0.3, 0.35), (0.15, -0.3, 0.35))),
          figure("gondolier", (0.05, 2.5, 0.67), robe="#ECE6D6", top="#ECE6D6", legs="#2A2A33", head="hat", hc=STRAW, lean=0.15,
                 hands=((0.15, -0.45, 1.2), (0.42, -0.35, 1.2))),
          box("sash", 0.44, 0.44, 0.06, (0.05, 2.5, 1.55), "#55687E"),
          rod("oar", (0.38, 2.05, 1.8), (0.86, -0.3, 0.02), 0.03, WOOD, verts=4), box("oar_blade", 0.06, 0.36, 0.1, (0.86, -0.42, 0.0), WOOD)]
    m.add("base", p)
    return m


BUILDERS = {}
for _set, _fns in {
    "islamic": {"walker": i_walker, "matron": i_matron, "porter": i_porter, "mule": i_mule, "litter": i_litter, "handcart": i_handcart, "cart": i_cart,
                "stall-fruit": i_stall_fruit, "stall-pots": i_stall_pots, "stall-cloth": i_stall_cloth, "stall": i_stall, "forge": i_forge, "farmer": i_farmer,
                "wagon": i_wagon, "bakery": i_bakery, "shepherd": i_shepherd, "crowd": i_crowd, "boat": i_boat, "skiff": i_skiff},
    "african": {"walker": a_walker, "matron": a_matron, "porter": a_porter, "mule": a_mule, "litter": a_litter, "handcart": a_handcart, "cart": a_cart,
                "stall-fruit": a_stall_fruit, "stall-pots": a_stall_pots, "stall-cloth": a_stall_cloth, "stall": a_stall, "forge": a_forge, "farmer": a_farmer,
                "wagon": a_wagon, "bakery": a_bakery, "shepherd": a_shepherd, "crowd": a_crowd, "boat": a_boat, "skiff": a_skiff},
    "venetian": {"boat": v_boat, "skiff": v_skiff},
}.items():
    for _name, _fn in _fns.items():
        BUILDERS[f"props/{_set}/{_name}"] = _fn
