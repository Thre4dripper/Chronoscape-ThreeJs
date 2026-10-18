"""
Regional street-life props for East Asia (Chang'an, Kaifeng, Khanbaliq, Nara, Kyoto, Edo),
Mesoamerica (Tenochtitlan, Teotihuacan) and the Andes (Cusco), redrawn after Rome's set in
props.py: the same functional slots, the same study-model style (simple primitives, grey
massing with a few colour accents), metres, origin at ground centre, facing -Y.

Animated parts keep Rome's names (anim_hammer, anim_walk, anim_spin, anim_graze) and pivots
conventions so the web app (LifeProps.tsx) drives them unchanged:
  * anim_hammer rotates about +X at its pivot (the shoulder), swinging the arm forward (-Y) and up;
  * anim_walk slides 6 m either way along Y;  anim_graze slides 1.5 m either way along X;
  * anim_spin turns about the vertical through its pivot (a point at +X moves toward +Y).

Keys: props/eastasian/<slot>, props/americas/<slot>, props/andean/<slot>.
"""
import math
import random
import bpy
import bmesh
from mathutils import Matrix, Vector
from chronokit import box, cylinder, dome, join, shade, mesh_from, hip_roof, gable_roof
from props import Prop, hull, wheel, ox, G1, G2, G3, SKIN, WOOD, IRON, FIRE, STRAW

# ---------------------------------------------------------------- small geometry helpers


def _apply(o):
    bpy.ops.object.select_all(action="DESELECT")
    o.select_set(True)
    bpy.context.view_layer.objects.active = o
    bpy.ops.object.transform_apply(location=True, rotation=True, scale=True)
    return o


def place(objs, loc=(0, 0, 0), rz=0.0, s=1.0, name=None):
    """Join a group built at the origin, then turn it about Z, scale it and move it to loc."""
    objs = [o for o in (objs if isinstance(objs, list) else [objs]) if o is not None]
    o = _apply(join(objs, name or objs[0].name))
    o.data.transform(Matrix.Translation(Vector(loc)) @ Matrix.Rotation(rz, 4, "Z") @ Matrix.Scale(s, 4))
    o.data.update()
    return o


def rod(name, r, a, b, color, verts=6, r_top=None):
    """A cylinder from point a to point b."""
    a, b = Vector(a), Vector(b)
    d = b - a
    o = _apply(cylinder(name, r, d.length, (0, 0, 0), color, verts=verts, r_top=r_top))
    q = Vector((0, 0, 1)).rotation_difference(d.normalized())
    o.data.transform(Matrix.Translation(a) @ q.to_matrix().to_4x4())
    o.data.update()
    return o


def blk(name, w, d, h, c, color, rot=(0, 0, 0)):
    """A box centred on c, turned by rot (about its centre)."""
    o = box(name, w, d, h, (0, 0, -h / 2), color)
    o.rotation_euler = rot
    o.location = c
    return o


def disc(name, r, c, normal, t, color, verts=12):
    n = Vector(normal).normalized() * (t / 2)
    return rod(name, r, Vector(c) - n, Vector(c) + n, color, verts=verts)


def half_tube(name, r, length, c, color, verts=12):
    """An arched cover (half cylinder) running along Y, springing from height c[2]."""
    o = _apply(cylinder(name, r, length, (0, 0, -length / 2), color, verts=verts))
    o.data.transform(Matrix.Translation(Vector(c)) @ Matrix.Rotation(math.pi / 2, 4, "X"))
    bm = bmesh.new()
    bm.from_mesh(o.data)
    bmesh.ops.delete(bm, geom=[v for v in bm.verts if v.co.z < c[2] - 1e-4], context="VERTS")
    bm.to_mesh(o.data)
    bm.free()
    return o


def slab(name, pts, t, color, x=0.0):
    """A thin plate in the YZ plane (pts are (y, z)), t thick, centred on x: sails and blinds."""
    n = len(pts)
    verts = [(x - t / 2, u, z) for u, z in pts] + [(x + t / 2, u, z) for u, z in pts]
    faces = [tuple(range(n))[::-1], tuple(range(n, 2 * n))] + [(i, (i + 1) % n, n + (i + 1) % n, n + i) for i in range(n)]
    return mesh_from(name, verts, faces, (0, 0, 0), color)


def tube(name, sections, color, n=8):
    """A lofted tube along Y through elliptical sections (y, rx, rz, zc), capped at both ends."""
    verts, faces = [], []
    for y, rx, rz, zc in sections:
        for k in range(n):
            a = math.tau * k / n
            verts.append((rx * math.cos(a), y, zc + rz * math.sin(a)))
    for i in range(len(sections) - 1):
        for k in range(n):
            a, b = i * n + k, i * n + (k + 1) % n
            faces.append((a, b, b + n, a + n))
    faces.append(tuple(range(n))[::-1])
    last = (len(sections) - 1) * n
    faces.append(tuple(range(last, last + n)))
    return mesh_from(name, verts, faces, (0, 0, 0), color)


def scatter(n, xr, yr, rnd, gap):
    """n points in the rectangle |x|<=xr, |y|<=yr, at least gap apart (so figures never overlap)."""
    pts = []
    tries = 0
    while len(pts) < n and tries < 4000:
        tries += 1
        p = (rnd.uniform(-xr, xr), rnd.uniform(-yr, yr))
        if all((p[0] - q[0]) ** 2 + (p[1] - q[1]) ** 2 >= gap * gap for q in pts):
            pts.append(p)
    return pts


# ---------------------------------------------------------------- palettes
BLACK, PAPER, GOLD, LACQUER = "#2A2622", "#EDE3C8", "#C9A24A", "#9A2E25"
INDIGO, ROBE_GREY, ROBE_BROWN, ROBE_BLUE, ROBE_GREEN, ROBE_WHITE, PLUM = "#3E4A6B", "#7D8890", "#8A6A4E", "#55687E", "#5E7457", "#E6DED0", "#7D5A6B"
ROOF_D, BAMBOO, MAT, WATER, PADDY, EARTH = "#5A5650", "#B9A06A", "#A88A5A", "#65888A", "#8FA8A0", "#8A7350"
SKIN_AM, HAIR = "#A9764F", "#221C18"
COTTON, CREAM, RED, TEAL, OCHRE, OBSIDIAN = "#EEE8DA", "#E3D5B8", "#A6493A", "#2F7A6A", "#C9A24A", "#26262C"
CLAY, CLAY_D, ADOBE, THATCH, STONE_A = "#B5654A", "#5A3B2C", "#E3DACB", "#B9A06A", "#A8A08E"


def _hands(n, xs, z, skin, y=0.0):
    return [dome(f"{n}_hand{i}", 0.045, (x, y, z), skin, squash=1.0, segments=6, rings=4) for i, x in enumerate(xs)]


# ================================================================ EAST ASIA
def ea_man(n, robe, hat="straw", short=False, sash=None, legs_col="#8F7A62"):
    """A man in a long crossed-collar robe (or, short=True, a labourer's jacket and leggings)."""
    if short:
        p = [cylinder(n + "_ll", 0.085, 0.78, (-0.1, 0.08, 0), legs_col, verts=6), cylinder(n + "_rl", 0.085, 0.78, (0.1, -0.08, 0), legs_col, verts=6),
             cylinder(n + "_robe", 0.22, 0.5, (0, 0, 0.62), robe, verts=8, r_top=0.19), cylinder(n + "_chest", 0.19, 0.25, (0, 0, 1.1), robe, verts=8, r_top=0.15)]
        for s in (-1, 1):
            p.append(cylinder(f"{n}_arm{s}", 0.065, 0.48, (s * 0.24, 0, 0.82), SKIN, verts=6))
    else:
        p = [cylinder(n + "_robe", 0.24, 1.08, (0, 0, 0), robe, verts=10, r_top=0.19), cylinder(n + "_chest", 0.19, 0.3, (0, 0, 1.05), robe, verts=10, r_top=0.15)]
        for s in (-1, 1):
            p.append(cylinder(f"{n}_sl{s}", 0.1, 0.5, (s * 0.24, 0, 0.6), robe, verts=6, r_top=0.07))
    p += [cylinder(n + "_sash", 0.205, 0.07, (0, 0, 0.98), sash or shade(robe, -0.35), verts=8),
          dome(n + "_head", 0.12, (0, 0, 1.37), SKIN, squash=1.45, segments=10, rings=6)]
    if hat == "straw":
        p.append(cylinder(n + "_hat", 0.3, 0.17, (0, 0, 1.47), STRAW, verts=10, r_top=0.0))
    elif hat == "cap":   # black gauze cap (futou / eboshi)
        p += [dome(n + "_hair", 0.125, (0, 0.015, 1.44), HAIR, squash=0.85, segments=10, rings=4), cylinder(n + "_cap", 0.09, 0.26, (0, 0.03, 1.46), BLACK, verts=8, r_top=0.07)]
    else:                # topknot
        p += [dome(n + "_hair", 0.125, (0, 0.015, 1.44), HAIR, squash=0.85, segments=10, rings=4), cylinder(n + "_knot", 0.045, 0.1, (0, 0.03, 1.5), HAIR, verts=6)]
    return p


def ea_woman(n, robe, obi, hair=HAIR):
    """A woman in a long robe (kimono / ruqun) with a wide sash bowed at the back, hair in a bun."""
    p = [cylinder(n + "_robe", 0.23, 1.12, (0, 0, 0), robe, verts=10, r_top=0.2), cylinder(n + "_obi", 0.215, 0.2, (0, 0, 0.8), obi, verts=10),
         blk(n + "_bow", 0.28, 0.1, 0.16, (0, 0.24, 0.9), obi), cylinder(n + "_chest", 0.19, 0.28, (0, 0, 1.0), robe, verts=10, r_top=0.15),
         dome(n + "_head", 0.115, (0, 0, 1.33), SKIN, squash=1.45, segments=10, rings=6),
         dome(n + "_hair", 0.125, (0, 0.02, 1.4), hair, squash=0.85, segments=10, rings=4), dome(n + "_bun", 0.08, (0, 0.06, 1.5), hair, segments=8, rings=4),
         rod(n + "_pin", 0.012, (-0.12, 0.06, 1.55), (0.12, 0.06, 1.55), GOLD, verts=4)]
    for s in (-1, 1):
        p.append(blk(f"{n}_sl{s}", 0.08, 0.24, 0.42, (s * 0.24, 0.02, 0.83), robe))
    return p


def ea_seated(n, robe, hat="topknot", hs=0.42):
    """A robed figure sitting on a bench of height hs, facing -Y (hs≈0.18: kneeling)."""
    p = [blk(n + "_thigh", 0.36, 0.42, 0.16, (0, -0.15, hs + 0.08), robe), cylinder(n + "_body", 0.2, 0.55, (0, 0.05, hs), robe, verts=8, r_top=0.15)]
    if hs > 0.25:
        p.append(blk(n + "_shin", 0.3, 0.14, hs, (0, -0.33, hs / 2), robe))
    for s in (-1, 1):
        p.append(cylinder(f"{n}_sl{s}", 0.075, 0.4, (s * 0.22, -0.05, hs + 0.12), robe, verts=6))
    hz = hs + 0.6
    p.append(dome(n + "_head", 0.115, (0, 0.05, hz), SKIN, squash=1.45, segments=10, rings=6))
    if hat == "straw":
        p.append(cylinder(n + "_hat", 0.28, 0.16, (0, 0.05, hz + 0.1), STRAW, verts=10, r_top=0.0))
    elif hat == "bun":
        p += [dome(n + "_hair", 0.122, (0, 0.06, hz + 0.07), HAIR, squash=0.85, segments=10, rings=4), dome(n + "_bun", 0.075, (0, 0.1, hz + 0.15), HAIR, segments=8, rings=4)]
    else:
        p += [dome(n + "_hair", 0.122, (0, 0.06, hz + 0.07), HAIR, squash=0.85, segments=10, rings=4), cylinder(n + "_knot", 0.04, 0.1, (0, 0.07, hz + 0.12), HAIR, verts=6)]
    return p


def parasol(n, hand, top, r, color):
    return [rod(n + "_stick", 0.015, hand, top, WOOD, verts=4), dome(n + "_canopy", r, (top[0], top[1], top[2] - 0.12), color, squash=0.35, segments=12, rings=4),
            cylinder(n + "_tip", 0.03, 0.08, (top[0], top[1], top[2] - 0.12 + r * 0.35), BLACK, verts=6)]


def buffalo(n, color="#4F4C48"):
    """A water buffalo facing -Y: low head and wide swept-back horns."""
    p = [blk(n + "_body", 0.85, 1.85, 0.8, (0, 0.1, 1.0), color), blk(n + "_withers", 0.75, 0.6, 0.15, (0, -0.45, 1.45), color),
         blk(n + "_head", 0.42, 0.62, 0.42, (0, -1.1, 0.95), shade(color, -0.12), rot=(0.35, 0, 0)), blk(n + "_muzzle", 0.3, 0.2, 0.22, (0, -1.42, 0.8), shade(color, 0.15)),
         rod(n + "_tail", 0.03, (0, 1.02, 1.3), (0, 1.12, 0.7), shade(color, -0.2), verts=4)]
    for sx in (-0.27, 0.27):
        for sy in (-0.55, 0.75):
            p.append(box(f"{n}_leg{sx}{sy}", 0.17, 0.17, 0.65, (sx, sy, 0), shade(color, -0.2)))
    for s in (-1, 1):
        p += [rod(f"{n}_horn{s}", 0.05, (s * 0.12, -1.05, 1.22), (s * 0.5, -0.85, 1.3), "#D8CDB0", verts=5, r_top=0.035),
              rod(f"{n}_tip{s}", 0.035, (s * 0.5, -0.85, 1.3), (s * 0.45, -0.62, 1.42), "#D8CDB0", verts=5, r_top=0.01)]
    return p


def ea_walker():
    m = Prop("prop-eastasian-walker")
    m.add("base", ea_man("w", INDIGO, hat="straw") + [rod("staff", 0.02, (0.3, -0.1, 0.0), (0.27, -0.08, 1.35), BAMBOO, verts=4)])
    return m


def ea_matron():
    m = Prop("prop-eastasian-matron")
    m.add("base", ea_woman("m", PLUM, GOLD) + parasol("ps", (0.22, -0.12, 0.85), (0.0, 0.02, 2.0), 0.34, "#B5523A"))
    return m


def ea_porter():
    """A carrier with a shoulder pole (biandan / tenbin) and two baskets, fore and aft."""
    m = Prop("prop-eastasian-porter")
    x = 0.17
    p = ea_man("p", INDIGO, hat="straw", short=True)
    p.append(rod("pole", 0.03, (x, -0.37, 1.36), (x, 0.37, 1.36), BAMBOO, verts=6))
    for sy, fill in ((-1, "#D9792B"), (1, "#8FAF6A")):
        y = sy * 0.25
        p += [cylinder(f"bk{sy}", 0.12, 0.22, (x, y, 0.36), STRAW, verts=8, r_top=0.14), dome(f"fill{sy}", 0.13, (x, y, 0.58), fill, squash=0.55, segments=8, rings=4),
              rod(f"rope{sy}", 0.012, (x, y, 0.6), (x, y, 1.36), "#5A4632", verts=4)]
    m.add("base", p)
    return m


def ea_mule():
    """A pack horse with bales, led by its groom."""
    m = Prop("prop-eastasian-mule")
    c = "#6B5440"
    p = [box("body", 0.5, 1.45, 0.6, (0, 0.25, 0.8), c), blk("neck", 0.26, 0.3, 0.7, (0, -0.55, 1.38), c, rot=(0.5, 0, 0)),
         blk("mane", 0.07, 0.12, 0.7, (0, -0.46, 1.48), BLACK, rot=(0.5, 0, 0)), blk("head", 0.22, 0.55, 0.26, (0, -0.92, 1.62), shade(c, -0.1), rot=(0.55, 0, 0)),
         box("ear_l", 0.05, 0.06, 0.16, (-0.07, -0.78, 1.82), c), box("ear_r", 0.05, 0.06, 0.16, (0.07, -0.78, 1.82), c),
         rod("tail", 0.04, (0, 0.95, 1.3), (0, 1.1, 0.7), BLACK, verts=4), box("saddlecloth", 0.62, 0.7, 0.04, (0, 0.25, 1.4), LACQUER)]
    for sx in (-0.16, 0.16):
        for sy in (-0.3, 0.8):
            p.append(box(f"leg{sx}{sy}", 0.12, 0.12, 0.8, (sx, sy, 0), shade(c, -0.2)))
    for s in (-1, 1):
        p.append(box(f"bale{s}", 0.28, 0.62, 0.45, (s * 0.41, 0.25, 0.92), STRAW))
        p.append(box(f"band{s}", 0.29, 0.06, 0.46, (s * 0.41, 0.25, 0.915), "#5A4632"))
    p.append(box("topload", 0.5, 0.55, 0.28, (0, 0.25, 1.44), "#C9B79A"))
    g = place(ea_man("g", ROBE_BROWN, hat="straw", short=True), (0.55, -1.2, 0))
    p += [g, rod("lead", 0.012, (0.32, -1.22, 0.95), (0.08, -1.12, 1.45), "#5A4632", verts=4)]
    m.add("base", p)
    return m


def ea_litter():
    """A sedan chair (jiao / kago): a lacquered cabin on two poles, four bearers."""
    m = Prop("prop-eastasian-litter")
    p = [box("skirt", 0.86, 1.06, 0.1, (0, 0, 0.7), BLACK), box("cabin", 0.8, 1.0, 1.05, (0, 0, 0.8), LACQUER),
         hip_roof("roof", 0.8, 1.0, 0.35, (0, 0, 1.85), BLACK, ridge=0.3, overhang=0.13), dome("finial", 0.08, (0, 0, 2.17), GOLD, segments=8, rings=4),
         box("door", 0.5, 0.03, 0.72, (0, -0.51, 0.95), GOLD), box("win_l", 0.03, 0.42, 0.34, (-0.41, 0, 1.3), PAPER), box("win_r", 0.03, 0.42, 0.34, (0.41, 0, 1.3), PAPER)]
    for s in (-1, 1):
        p += [rod(f"pole{s}", 0.045, (s * 0.5, -2.05, 1.3), (s * 0.5, 2.05, 1.3), BLACK, verts=6), box(f"bracket{s}", 0.12, 0.8, 0.1, (s * 0.45, 0, 1.22), BLACK)]
    cols = [INDIGO, ROBE_BLUE, ROBE_BROWN, INDIGO]
    for i, (sx, sy) in enumerate([(-1, -1), (1, -1), (-1, 1), (1, 1)]):
        p.append(place(ea_man(f"b{i}", cols[i], hat="straw", short=True), (sx * 0.62, sy * 1.75, 0)))
    m.add("base", p)
    return m


def ea_handcart():
    """A Chinese wheelbarrow: one big central wheel, loads slung either side, pushed from behind."""
    m = Prop("prop-eastasian-handcart")
    p = [wheel("wheel", 0.42, (0, -0.3, 0.42)), box("hub_frame", 0.14, 0.95, 0.12, (0, -0.25, 0.86), WOOD)]
    for s in (-1, 1):
        p += [box(f"deck{s}", 0.36, 1.0, 0.06, (s * 0.28, -0.25, 0.5), WOOD),
              rod(f"handle{s}", 0.03, (s * 0.3, -0.75, 0.52), (s * 0.34, 0.85, 0.78), WOOD, verts=5),
              rod(f"leg{s}", 0.025, (s * 0.3, 0.2, 0.52), (s * 0.3, 0.25, 0.0), WOOD, verts=4),
              box(f"sack{s}", 0.32, 0.5, 0.36, (s * 0.3, -0.45, 0.56), "#C9B79A" if s < 0 else STRAW),
              cylinder(f"jar{s}", 0.14, 0.34, (s * 0.3, 0.1, 0.56), CLAY, verts=8, r_top=0.08)]
    p.append(place(ea_man("pusher", ROBE_GREY, hat="straw", short=True), (0, 1.12, 0)))
    p.append(rod("strap", 0.015, (-0.34, 0.85, 0.78), (0.0, 1.0, 1.35), "#5A4632", verts=4))
    m.add("base", p)
    return m


def ea_cart():
    """An ox cart (Heian gissha / Tang ox carriage): two tall wheels, a black ox, a roofed body."""
    m = Prop("prop-eastasian-cart")
    yb = 1.05
    p = [wheel("wl", 0.95, (-0.8, yb, 0.95), color=BLACK), wheel("wr", 0.95, (0.8, yb, 0.95), color=BLACK),
         rod("axle", 0.05, (-0.8, yb, 0.95), (0.8, yb, 0.95), BLACK), box("body", 1.25, 2.1, 1.1, (0, yb, 0.85), "#3A3330"),
         box("panel_l", 0.03, 1.5, 0.55, (-0.63, yb, 1.25), "#C9B79A"), box("panel_r", 0.03, 1.5, 0.55, (0.63, yb, 1.25), "#C9B79A"),
         half_tube("roof", 0.72, 2.5, (0, yb, 1.95), "#D8CDB0"), box("eave", 1.46, 2.5, 0.06, (0, yb, 1.92), BLACK),
         box("blind", 0.95, 0.03, 0.75, (0, yb - 1.06, 1.1), BAMBOO), box("blind_hem", 0.95, 0.04, 0.22, (0, yb - 1.07, 0.88), "#6B4A72"),
         box("step", 0.7, 0.3, 0.08, (0, yb + 1.2, 0.55), BLACK)]
    for s in (-1, 1):
        p.append(rod(f"shaft{s}", 0.04, (s * 0.5, yb - 1.0, 0.95), (s * 0.5, -2.35, 1.25), BLACK, verts=5))
    p += [box("yoke", 1.15, 0.12, 0.1, (0, -2.3, 1.3), BLACK), place(ox("ox", (0, 0, 0), color="#2E2A28"), (0, -1.35, 0))]
    p += [place(ea_man("drover", ROBE_WHITE, hat="cap", short=True), (0.95, -2.55, 0)), rod("nose_rope", 0.012, (0.75, -2.55, 1.0), (0.12, -2.65, 1.1), "#C9B79A", verts=4),
          place(ea_man("attendant", ROBE_WHITE, hat="cap"), (-1.05, -0.15, 0))]
    m.add("base", p)
    return m


def _ea_stall(name, roof_col, goods, vendor, curtain=INDIGO):
    """A street stall: low bench, lean-to roof on four posts, short noren curtains at the eave."""
    m = Prop(name)
    p = [box("bench", 2.2, 0.85, 0.55, (0, 0.05, 0), WOOD), box("top", 2.3, 0.95, 0.05, (0, 0.05, 0.55), shade(WOOD, 0.25))]
    for sx in (-1.15, 1.15):
        p += [rod(f"postf{sx}", 0.045, (sx, -0.55, 0), (sx, -0.55, 2.12), WOOD, verts=5), rod(f"postb{sx}", 0.045, (sx, 1.05, 0), (sx, 1.05, 2.45), WOOD, verts=5)]
    p.append(blk("roof", 2.66, 1.95, 0.1, (0, 0.25, 2.3), roof_col, rot=(0.2, 0, 0)))
    for k, x in enumerate((-0.8, 0.0, 0.8)):
        p.append(box(f"noren{k}", 0.62, 0.025, 0.32, (x, -0.68, 1.82), curtain))
    p += goods
    p.append(place(vendor, (0.35, 0.82, 0)))
    m.add("base", p)
    return m


def ea_stall_fruit():
    cols = ["#D9792B", "#8FAF6A", "#4A3557", "#C9A24A", "#A6493A"]
    goods = []
    for i in range(4):
        x = -0.8 + i * 0.53
        goods += [cylinder(f"bk{i}", 0.2, 0.14, (x, 0.0, 0.6), STRAW, verts=8, r_top=0.24), dome(f"pile{i}", 0.21, (x, 0.0, 0.72), cols[i], squash=0.55, segments=8, rings=4)]
    for i in range(4):
        goods.append(rod(f"daikon{i}", 0.04, (-0.9 + i * 0.12, 0.38, 0.62), (-0.9 + i * 0.12, 0.38 - 0.42, 0.62), "#F1EBE0", verts=5, r_top=0.015))
    for i in range(3):
        x = -0.75 + i * 0.75
        goods += [cylinder(f"gb{i}", 0.26, 0.3, (x, -0.85, 0), STRAW, verts=8, r_top=0.3), dome(f"gp{i}", 0.27, (x, -0.85, 0.3), cols[(i + 1) % 5], squash=0.5, segments=8, rings=4)]
    return _ea_stall("prop-eastasian-stall-fruit", STRAW, goods, ea_man("v", ROBE_BROWN, hat="topknot", short=True))


def ea_stall_pots():
    goods = []
    for i in range(6):
        x = -0.85 + i * 0.34
        if i % 3 == 0:
            goods.append(cylinder(f"jar{i}", 0.13, 0.36, (x, 0.05, 0.58), "#DCE3E8", verts=10, r_top=0.07))
            goods.append(cylinder(f"jarband{i}", 0.125, 0.06, (x, 0.05, 0.72), "#3E5A8A", verts=10))
        elif i % 3 == 1:
            for k in range(3):
                goods.append(dome(f"bowl{i}{k}", 0.15 - 0.02 * k, (x, 0.05, 0.58 + 0.07 * k), "#8FA89A", squash=0.45, segments=10, rings=4))
        else:
            for k in range(4):
                goods.append(cylinder(f"lacq{i}{k}", 0.13, 0.06, (x, 0.05, 0.58 + 0.065 * k), LACQUER if k % 2 else BLACK, verts=10, r_top=0.15))
    for i in range(3):
        goods.append(cylinder(f"crock{i}", 0.24, 0.55, (-0.75 + i * 0.75, -0.85, 0), "#6E5A44" if i % 2 else "#8A6E52", verts=10, r_top=0.14))
    return _ea_stall("prop-eastasian-stall-pots", "#8A8378", goods, ea_man("v", ROBE_GREY, hat="topknot", short=True), curtain="#7A2E2A")


def ea_stall_cloth():
    cols = ["#A83A32", "#4F8A6E", "#D9A93A", "#4C6E9A", PLUM, "#E6DED0"]
    goods = []
    for i in range(10):
        goods.append(rod(f"bolt{i}", 0.09, (-0.95 + (i % 5) * 0.47, -0.2 + (i // 5) * 0.3, 0.68 + 0.04 * (i // 5)), (-0.95 + (i % 5) * 0.47, 0.1 + (i // 5) * 0.3, 0.68 + 0.04 * (i // 5)), cols[i % 6], verts=8))
    goods.append(rod("rail", 0.025, (-1.15, -0.5, 1.95), (1.15, -0.5, 1.95), BAMBOO, verts=5))
    for i in range(4):
        goods.append(box(f"hang{i}", 0.42, 0.03, 1.0, (-0.82 + i * 0.55, -0.5, 0.95), cols[(i + 2) % 6]))
    return _ea_stall("prop-eastasian-stall-cloth", "#6E6A62", goods, ea_woman("v", ROBE_BLUE, "#C9A24A"), curtain="#E6DED0")


def ea_stall():
    """A noodle (soba) yatai: counter with a steaming pot, red lanterns, a bench of customers."""
    m = Prop("prop-eastasian-stall")
    p = [box("counter", 1.9, 0.8, 0.95, (0, 0.25, 0), WOOD), box("top", 2.0, 0.9, 0.05, (0, 0.25, 0.95), shade(WOOD, 0.25)),
         box("roof", 2.3, 1.35, 0.08, (0, 0.25, 2.1), "#4A4038"), box("ridge", 2.3, 0.3, 0.1, (0, 0.25, 2.18), BLACK),
         cylinder("pot", 0.24, 0.22, (0.45, 0.35, 1.0), IRON, verts=10), cylinder("lid", 0.25, 0.04, (0.45, 0.35, 1.22), WOOD, verts=10),
         box("bowls", 0.4, 0.25, 0.1, (-0.35, 0.3, 1.0), LACQUER), cylinder("bucket", 0.18, 0.4, (-0.75, 0.3, 1.0), WOOD, verts=8),
         box("bench", 1.6, 0.3, 0.42, (0, -0.95, 0), WOOD)]
    for sx in (-0.95, 0.95):
        for sy in (-0.12, 0.62):
            p.append(rod(f"post{sx}{sy}", 0.04, (sx, sy, 0.95), (sx, sy, 2.1), WOOD, verts=5))
    for k, x in enumerate((-0.66, -0.22, 0.22, 0.66)):
        p.append(box(f"noren{k}", 0.4, 0.025, 0.42, (x, -0.43, 1.66), INDIGO))
    for s in (-1, 1):
        x = s * 1.05
        p += [cylinder(f"lant{s}a", 0.12, 0.16, (x, -0.42, 1.38), "#C23B2B", verts=8, r_top=0.15), cylinder(f"lant{s}b", 0.15, 0.16, (x, -0.42, 1.54), "#C23B2B", verts=8, r_top=0.12),
              cylinder(f"lant{s}c", 0.08, 0.05, (x, -0.42, 1.7), BLACK, verts=8), rod(f"lant{s}h", 0.01, (x, -0.42, 1.75), (x, -0.42, 2.1), BLACK, verts=4)]
    p.append(place(ea_man("cook", ROBE_WHITE, hat="topknot", sash=INDIGO), (0, 0.98, 0)))
    p.append(place(ea_seated("c1", INDIGO, "straw"), (-0.45, -0.98, 0), rz=math.pi))
    p.append(place(ea_seated("c2", ROBE_BROWN, "topknot"), (0.45, -0.98, 0), rz=math.pi))
    m.add("base", p)
    return m


def ea_forge():
    """A swordsmith's shed: clay hearth and box bellows, the master at the anvil, a striker swinging."""
    m = Prop("prop-eastasian-forge")
    p = [box("floor", 6.6, 5.6, 0.15, (0, 0.6, 0), G2), box("back", 6.6, 0.3, 2.8, (0, 3.25, 0), G1),
         box("side_l", 0.3, 2.4, 2.8, (-3.15, 2.0, 0), G1), box("side_r", 0.3, 2.4, 2.8, (3.15, 2.0, 0), G1),
         hip_roof("roof", 6.0, 3.0, 1.2, (0, 1.95, 2.8), ROOF_D, ridge=0.4, overhang=0.28),
         rod("post_l", 0.1, (-3.0, 0.6, 0), (-3.0, 0.6, 2.8), WOOD, verts=6), rod("post_r", 0.1, (3.0, 0.6, 0), (3.0, 0.6, 2.8), WOOD, verts=6),
         box("hearth", 1.3, 1.1, 0.55, (-1.6, 2.3, 0.15), "#B9A88C"), box("embers", 0.8, 0.6, 0.06, (-1.6, 2.2, 0.7), FIRE),
         box("hood", 1.0, 0.8, 1.0, (-1.6, 2.6, 1.6), "#B9A88C"), box("flue", 0.5, 0.5, 1.6, (-1.6, 2.7, 2.6), "#A8977C"),
         box("bellows", 0.5, 1.0, 0.55, (-2.65, 2.2, 0.15), WOOD), rod("bellows_rod", 0.03, (-2.65, 1.7, 0.45), (-2.65, 1.3, 0.45), WOOD, verts=4),
         box("anvil_block", 0.5, 0.4, 0.3, (0.3, 0.0, 0.15), WOOD), box("anvil", 0.4, 0.26, 0.12, (0.3, 0.0, 0.45), IRON),
         box("trough", 1.0, 0.4, 0.35, (1.6, 1.2, 0.15), WOOD), box("water", 0.9, 0.3, 0.03, (1.6, 1.2, 0.48), WATER),
         box("rack", 1.4, 0.12, 1.2, (2.2, 3.0, 0.15), WOOD)]
    for k in range(4):
        p.append(rod(f"blade{k}", 0.02, (1.65 + k * 0.32, 2.9, 0.45), (1.65 + k * 0.32 + 0.05, 2.9, 1.3), "#BFC3C6", verts=4))
    # shimenawa: a sacred straw rope with paper streamers across the open front
    p.append(rod("rope", 0.06, (-3.0, 0.6, 2.4), (3.0, 0.6, 2.4), STRAW, verts=6))
    for k in range(5):
        p.append(box(f"shide{k}", 0.08, 0.02, 0.3, (-2.0 + k, 0.6, 2.05), "#F4F1EA"))
    p.append(place(ea_seated("bellows_man", ROBE_GREY, "topknot", hs=0.18), (-2.65, 1.25, 0.15)))
    p.append(place(ea_seated("master", ROBE_WHITE, "cap", hs=0.18), (0.3, -0.55, 0.15), rz=math.pi))
    p.append(rod("tongs", 0.02, (0.3, -0.35, 0.6), (0.3, 0.05, 0.6), IRON, verts=4))
    # the striker stands behind the anvil, facing -Y; his right arm is the animated part
    sx, sy, sz = 0.52, 0.72, 1.5
    striker = ea_man("striker", INDIGO, hat="topknot", short=True)
    p.append(place([o for o in striker if not o.name.endswith("_arm1")], (0.3, 0.72, 0.15)))
    p.append(place(ea_man("customer", "#3A3346", hat="cap"), (2.4, -1.9, 0)))
    p.append(rod("customer_sword", 0.025, (2.15, -1.75, 0.95), (1.95, -1.3, 0.75), BLACK, verts=4))
    m.add("base", p)
    phi = 0.21
    d = Vector((0, -math.sin(phi), -math.cos(phi)))
    S = Vector((sx, sy, sz))
    m.add("anim_hammer", [rod("arm", 0.065, S, S + d * 0.55, SKIN, verts=6), rod("handle", 0.025, S + d * 0.5, S + d * 0.95, WOOD, verts=5),
                          blk("hammer_head", 0.12, 0.12, 0.3, S + d * 0.97, IRON, rot=(-phi, 0, 0))], pivot=(sx, sy, sz))
    m.marker("marker_smoke", (-1.6, 2.7, 4.4))
    m.marker("marker_sparks", (0.3, 0.0, 0.6))
    return m


def ea_farmer():
    """A rice farmer harrowing a flooded paddy behind a water buffalo; seedlings planted alongside."""
    m = Prop("prop-eastasian-farmer")
    team = place(buffalo("buf"), (0.8, 0, 0))
    harrow = [rod("trace_l", 0.02, (0.55, 0.2, 1.1), (0.25, 1.4, 0.3), "#5A4632", verts=4), rod("trace_r", 0.02, (1.05, 0.2, 1.1), (1.35, 1.4, 0.3), "#5A4632", verts=4),
              box("harrow", 1.4, 0.14, 0.14, (0.8, 1.45, 0.2), WOOD)]
    for k in range(6):
        harrow.append(box(f"tine{k}", 0.05, 0.05, 0.22, (0.25 + k * 0.22, 1.45, 0.0), WOOD))
    harrow += [rod("handle_l", 0.025, (0.45, 1.45, 0.3), (0.55, 2.05, 1.0), WOOD, verts=4), rod("handle_r", 0.025, (1.15, 1.45, 0.3), (1.05, 2.05, 1.0), WOOD, verts=4),
               box("grip", 0.6, 0.06, 0.06, (0.8, 2.05, 0.97), WOOD)]
    m.add("anim_walk", [team] + harrow + [place(ea_man("farmer", INDIGO, hat="straw", short=True, legs_col=SKIN), (0.8, 2.45, 0))], pivot=(0, 0, 0))
    base = []
    for k, y0 in enumerate((-9, -3, 3)):
        base.append(box(f"paddy{k}", 5.8, 6.0, 0.04, (0, y0 + 3, 0), PADDY))
    for k, y in enumerate((-9, -3, 3, 9)):
        base.append(box(f"bund_y{k}", 6.1, 0.3, 0.18, (0, max(-8.85, min(8.85, y)), 0), EARTH))
    for s in (-1, 1):
        base.append(box(f"bund_x{s}", 0.3, 18, 0.18, (s * 2.9, 0, 0), EARTH))
    for r in range(3):
        for k in range(28):
            y = -8.4 + k * 0.62
            if abs(y + 3) < 0.25 or abs(y - 3) < 0.25:
                continue
            base.append(box(f"seed{r}_{k}", 0.12, 0.12, 0.22, (-2.4 + r * 0.45, y, 0), "#6E9A4A"))
    base.append(place(ea_man("planter", ROBE_BLUE, hat="straw", short=True, legs_col=SKIN), (-1.0, -4.5, 0)))
    base += [cylinder("seedlings", 0.22, 0.25, (-0.55, -4.9, 0), STRAW, verts=8, r_top=0.25), dome("seedling_tops", 0.2, (-0.55, -4.9, 0.25), "#6E9A4A", squash=0.6, segments=8, rings=4)]
    m.add("base", base)
    return m


def ea_wagon():
    """An ox cart heaped with roped bales and sacks, a yoked pair of oxen, a drover."""
    m = Prop("prop-eastasian-wagon")
    yb = 1.1
    p = [box("bed", 1.6, 3.2, 0.2, (0, yb, 0.8), WOOD), wheel("wl", 0.8, (-0.92, yb, 0.8), color="#6E5238"), wheel("wr", 0.8, (0.92, yb, 0.8), color="#6E5238"),
         box("rail_l", 0.08, 3.2, 0.3, (-0.78, yb, 1.0), WOOD), box("rail_r", 0.08, 3.2, 0.3, (0.78, yb, 1.0), WOOD)]
    for i in range(3):
        for j in range(2):
            p.append(box(f"bale{i}{j}", 0.7, 0.95, 0.55, (-0.37 + j * 0.74, yb - 1.05 + i * 1.05, 1.0), STRAW if (i + j) % 2 else "#C9B79A"))
    for i in range(3):
        p.append(box(f"sack{i}", 0.6, 0.8, 0.45, (-0.3 + i * 0.3, yb - 1.0 + i * 1.0, 1.55), "#C9B79A" if i % 2 else "#B5A27E"))
    p.append(box("mat", 1.5, 2.9, 0.05, (0, yb, 2.0), MAT))
    for k in range(3):
        p.append(box(f"rope{k}", 1.62, 0.05, 0.05, (0, yb - 1.0 + k, 2.05), "#5A4632"))
    p += [rod("pole", 0.06, (0, yb - 1.6, 0.85), (0, -2.9, 1.25), WOOD), box("yoke", 1.9 - 0.1, 0.14, 0.14, (0, -2.95, 1.3), WOOD),
          place(ox("ox_l", (0, 0, 0), color="#6B5A4A"), (-0.5, -2.15, 0)), place(ox("ox_r", (0, 0, 0), color="#8C7A62"), (0.5, -2.15, 0))]
    p.append(place(ea_man("drover", ROBE_BROWN, hat="straw", short=True), (1.45, -0.6, 0)))
    p.append(rod("goad", 0.015, (1.25, -0.65, 0.9), (1.1, -1.8, 1.7), BAMBOO, verts=4))
    p.append(place(ea_man("follower", ROBE_GREY, hat="straw"), (-1.35, 3.0, 0)))
    m.add("base", p)
    return m


def ea_bakery():
    """A steamed-bun and tea house: stove with bamboo steamers, a counter, a red tea umbrella,
    and a millstone turned by a blindfolded donkey."""
    m = Prop("prop-eastasian-bakery")
    p = [box("floor", 6.4, 4.0, 0.12, (0, 1.6, 0), G2), box("back", 6.4, 0.25, 2.6, (0, 3.475, 0), G1), box("side", 0.25, 4.0, 2.6, (3.075, 1.6, 0), G1),
         hip_roof("roof", 6.0, 3.6, 1.3, (0, 1.6, 2.6), ROOF_D, ridge=0.45, overhang=0.22),
         box("stove", 1.7, 0.9, 0.8, (-1.9, 2.7, 0.12), "#B9A88C"), box("stove_mouth", 0.5, 0.05, 0.35, (-1.9, 2.24, 0.25), FIRE)]
    for x in (-3.0, 0.0, 2.9):
        p.append(rod(f"post{x}", 0.09, (x, -0.3, 0.12), (x, -0.3, 2.6), WOOD, verts=6))
    for k, x in enumerate((-2.35, -1.45)):
        for j in range(4):
            p.append(cylinder(f"steamer{k}{j}", 0.3, 0.13, (x, 2.7, 0.92 + j * 0.14), BAMBOO if j % 2 else shade(BAMBOO, -0.12), verts=10))
        p.append(dome(f"steam_lid{k}", 0.3, (x, 2.7, 1.48), BAMBOO, squash=0.35, segments=10, rings=4))
    p += [box("counter", 2.0, 0.6, 0.9, (0.4, 0.45, 0.12), WOOD), box("tray", 1.6, 0.45, 0.04, (0.4, 0.45, 1.02), BAMBOO)]
    for i in range(8):
        p.append(dome(f"bun{i}", 0.08, (-0.25 + (i % 4) * 0.4 + 0.05 * (i // 4), 0.36 + (i // 4) * 0.18, 1.06), "#F2EDE2", squash=0.7, segments=6, rings=4))
    p += [place(ea_man("cook", ROBE_WHITE, hat="topknot", sash=INDIGO), (-1.9, 1.75, 0.12)), place(ea_woman("seller", ROBE_BLUE, "#C9A24A"), (0.4, 1.15, 0.12))]
    for k, x in enumerate((-2.3, -1.15, 0.0, 1.15)):
        p.append(box(f"noren{k}", 0.9, 0.03, 0.5, (x, -0.42, 1.95), INDIGO))
    # tea under a red umbrella: a bench with a red cloth, two guests, a teapot
    tx, ty = -1.7, -2.4
    p += [box("tea_bench", 1.7, 0.6, 0.42, (tx, ty, 0), WOOD), box("tea_cloth", 1.75, 0.65, 0.03, (tx, ty, 0.42), "#B03A2E"),
          cylinder("teapot", 0.08, 0.12, (tx + 0.1, ty - 0.05, 0.45), BLACK, verts=8), cylinder("cup", 0.04, 0.06, (tx - 0.1, ty - 0.1, 0.45), "#DCE3E8", verts=6)]
    p += parasol("tea_umbrella", (tx + 0.75, ty + 0.25, 0.0), (tx + 0.75, ty + 0.25, 2.5), 1.2, "#B03A2E")
    p += [place(ea_seated("guest1", INDIGO, "topknot"), (tx - 0.5, ty, 0)), place(ea_seated("guest2", PLUM, "bun"), (tx + 0.4, ty, 0))]
    mx, my = 1.4, -2.25
    p += [cylinder("mill_bed", 0.7, 0.45, (mx, my, 0), G3, verts=12), cylinder("mill_lower", 0.55, 0.15, (mx, my, 0.45), G2, verts=12)]
    m.add("base", p)
    mill = [cylinder("mill_upper", 0.5, 0.3, (mx, my, 0.6), G2, verts=12), rod("mill_bar", 0.04, (mx, my, 0.85), (mx + 1.2, my, 0.95), WOOD, verts=5)]
    dk = "#8A8072"
    donkey = [box("d_body", 0.36, 0.95, 0.45, (mx + 1.2, my, 0.55), dk), blk("d_neck", 0.18, 0.3, 0.45, (mx + 1.2, my + 0.5, 1.05), dk, rot=(-0.5, 0, 0)),
              blk("d_head", 0.18, 0.42, 0.2, (mx + 1.2, my + 0.68, 1.22), dk, rot=(-0.4, 0, 0)), box("d_blind", 0.22, 0.12, 0.08, (mx + 1.2, my + 0.62, 1.28), BLACK),
              box("d_ear_l", 0.04, 0.05, 0.18, (mx + 1.15, my + 0.58, 1.32), dk), box("d_ear_r", 0.04, 0.05, 0.18, (mx + 1.25, my + 0.58, 1.32), dk)]
    donkey += [box(f"d_leg{i}", 0.09, 0.09, 0.55, (mx + 1.2 + (i % 2 - 0.5) * 0.22, my + (i // 2 - 0.5) * 0.7, 0), shade(dk, -0.2)) for i in range(4)]
    m.add("anim_spin", mill + donkey, pivot=(mx, my, 0))
    m.marker("marker_smoke", (-1.9, 2.7, 4.3))
    return m


def duck(n, white=True):
    body = "#EDE6D6" if white else "#7A6048"
    head = "#EDE6D6" if white else "#2F5A40"
    return [box(n + "_b", 0.22, 0.38, 0.16, (0, 0.02, 0.06), body), box(n + "_tail", 0.12, 0.1, 0.08, (0, 0.24, 0.14), body),
            box(n + "_neck", 0.07, 0.07, 0.16, (0, -0.15, 0.18), head), box(n + "_head", 0.09, 0.13, 0.08, (0, -0.17, 0.32), head),
            box(n + "_beak", 0.05, 0.08, 0.03, (0, -0.27, 0.33), "#D9A03A")]


def ea_shepherd():
    """A duck-herd driving his flock across a paddy with a long bamboo pole; a cowherd boy rides a buffalo."""
    m = Prop("prop-eastasian-shepherd")
    rnd = random.Random(11)
    flock = []
    for i, (x, y) in enumerate(scatter(20, 3.4, 2.2, rnd, 0.6)):
        flock.append(place(duck(f"d{i}", white=i % 4 != 0), (x, y, 0), rz=rnd.uniform(-0.8, 0.8) + (math.pi / 2 if i % 3 == 0 else 0)))
    m.add("anim_graze", flock)
    base = [box("pond", 9.0, 5.4, 0.03, (-0.6, 0, 0), PADDY), box("bund", 9.6, 0.3, 0.18, (-0.6, 2.85, 0), EARTH),
            place(ea_man("herd", ROBE_BROWN, hat="straw", short=True, legs_col=SKIN), (5.0, 0.9, 0)),
            rod("pole", 0.025, (4.8, 0.75, 1.0), (3.4, 0.0, 2.9), BAMBOO, verts=5), box("flag", 0.03, 0.25, 0.35, (3.4, 0.12, 2.6), "#C23B2B"),
            place(buffalo("buf", "#5A5652"), (5.0, -1.55, 0))]
    boy = ea_seated("boy", "#8FA0A8", "straw", hs=0.0)
    base.append(place(boy, (5.0, -1.4, 1.38), rz=0.0, s=0.8))
    base.append(rod("flute", 0.012, (4.9, -1.75, 2.15), (5.2, -1.9, 2.1), BAMBOO, verts=4))
    m.add("base", base)
    return m


def ea_crowd():
    """Robed townsfolk, several under oiled-paper umbrellas, by a stone lantern and a bench."""
    m = Prop("prop-eastasian-crowd")
    rnd = random.Random(5)
    pts = scatter(8, 2.5, 1.7, rnd, 1.25)
    robes = [INDIGO, ROBE_BROWN, ROBE_BLUE, ROBE_GREY, ROBE_GREEN]
    ppl = []
    for i, (x, y) in enumerate(pts):
        rz = rnd.uniform(-math.pi, math.pi)
        if i % 3 == 1:
            fig = ea_woman(f"w{i}", [PLUM, ROBE_BLUE, "#A86A4A"][i % 3], GOLD)
        else:
            fig = ea_man(f"m{i}", robes[i % 5], hat="topknot" if i % 2 == 0 else ["straw", "cap"][i % 4 // 2])
        if i % 2 == 0:
            fig += parasol(f"u{i}", (0.22, -0.1, 0.9), (0.05, 0.0, 2.05), 0.5, ["#B5523A", "#C9A24A", "#5D6E80", "#7A2E2A"][i % 4])
        ppl.append(place(fig, (x, y, 0), rz=rz))
    ppl += [box("bench", 2.0, 0.4, 0.42, (-0.6, 2.45, 0), WOOD), box("lantern_base", 0.5, 0.5, 0.25, (2.9, -2.2, 0), G3),
            cylinder("lantern_post", 0.12, 0.8, (2.9, -2.2, 0.25), G3, verts=6), box("lantern_box", 0.42, 0.42, 0.35, (2.9, -2.2, 1.05), G2),
            hip_roof("lantern_cap", 0.4, 0.4, 0.25, (2.9, -2.2, 1.4), G3, ridge=0.0, overhang=0.1)]
    m.add("base", ppl)
    return m


def ea_boat():
    """A river junk: flat-sheered hull, mat-roofed deckhouse, a battened lug sail, a great stern rudder."""
    m = Prop("prop-eastasian-boat")
    H = "#6E5238"
    p = [hull("hull", 12.9, 3.4, 1.3, H), box("deck", 3.0, 9.8, 0.1, (0, 0, 1.25), shade(H, 0.25)), box("stern_deck", 2.6, 2.2, 0.8, (0, 4.9, 1.3), H),
         box("cabin", 2.3, 2.6, 1.0, (0, 2.5, 1.35), G2), half_tube("cabin_roof", 1.2, 2.9, (0, 2.5, 2.35), MAT),
         blk("rudder", 0.14, 0.75, 1.9, (0, 6.45, 0.75), H), rod("tiller", 0.04, (0, 6.3, 1.75), (0, 5.2, 2.2), WOOD, verts=4),
         rod("mast", 0.11, (0, -1.6, 1.3), (0, -1.6, 10.2), WOOD, verts=8)]
    sail_pts = [(-2.3, 2.9), (2.4, 2.9), (2.0, 9.6), (-1.6, 9.9)]
    sail = slab("sail", sail_pts, 0.05, "#B9875A", x=0.12)
    battens = [rod(f"batten{k}", 0.035, (0.16, -2.3 + k * 0.1, 3.0 + k * 1.1), (0.16, 2.4 - k * 0.07, 3.0 + k * 1.1), "#5A4632", verts=4) for k in range(7)]
    p.append(place([sail] + battens, (0, 0, 0), rz=0.12))
    for k, (x, y) in enumerate([(-0.65, -3.8), (0.65, -3.8), (-0.65, -2.8), (0.65, -2.8), (0, 0.2)]):
        p.append(box(f"bale{k}", 1.1, 0.8, 0.6, (x, y, 1.35), STRAW if k % 2 else "#C9B79A"))
    for k in range(4):
        p.append(cylinder(f"jar{k}", 0.24, 0.6, (-0.9 + k * 0.6, 0.9, 1.35), CLAY, verts=8, r_top=0.12))
    for s in (-1, 1):
        p += [box(f"eye{s}", 0.03, 0.45, 0.3, (s * 0.85, -5.95, 1.1), "#F4F1EA"), box(f"pupil{s}", 0.04, 0.2, 0.2, (s * 0.87, -5.95, 1.14), BLACK)]
    p += [place(ea_man("helm", ROBE_BROWN, hat="straw", short=True), (0.35, 5.0, 2.1)), place(ea_man("bowman", INDIGO, hat="straw", short=True), (0.6, -4.9, 1.35)),
          rod("bow_pole", 0.03, (0.85, -4.95, 1.9), (1.4, -6.0, 0.0), BAMBOO, verts=4)]
    m.add("base", p)
    return m


def ea_skiff():
    """A sampan: mat awning amidships, the boatman sculling a yuloh over the stern."""
    m = Prop("prop-eastasian-skiff")
    p = [hull("hull", 5.6, 1.45, 0.6, "#7A5C40"), box("floor", 1.1, 4.0, 0.05, (0, 0, 0.5), "#9C7A58"),
         half_tube("awning", 0.62, 1.7, (0, 0.1, 0.62), MAT), box("box", 0.5, 0.4, 0.3, (0, -1.7, 0.55), STRAW),
         place(ea_man("sculler", INDIGO, hat="straw", short=True), (0.12, 1.85, 0.55)),
         rod("yuloh", 0.035, (0.3, 1.65, 1.45), (0.12, 3.05, 0.1), WOOD, verts=5), blk("blade", 0.05, 0.4, 0.14, (0.12, 2.95, 0.15), WOOD, rot=(-0.85, 0, 0))]
    m.add("base", p)
    return m


# ================================================================ MESOAMERICA (Tenochtitlan, Teotihuacan)
def am_man(n, cloak=CREAM, border=RED, loin=COTTON, cloak_on=True):
    """A man in a white loincloth (maxtlatl); with cloak_on, a knotted tilmatli cloak over it."""
    p = [cylinder(n + "_ll", 0.085, 0.8, (-0.1, 0.08, 0), SKIN_AM, verts=6), cylinder(n + "_rl", 0.085, 0.8, (0.1, -0.08, 0), SKIN_AM, verts=6),
         cylinder(n + "_loin", 0.19, 0.16, (0, 0, 0.72), loin, verts=8), blk(n + "_flap", 0.14, 0.03, 0.32, (0, -0.19, 0.6), loin),
         cylinder(n + "_torso", 0.17, 0.5, (0, 0, 0.86), SKIN_AM, verts=8, r_top=0.2),
         dome(n + "_head", 0.115, (0, 0, 1.38), SKIN_AM, squash=1.45, segments=10, rings=6), dome(n + "_hair", 0.125, (0, 0.015, 1.45), HAIR, squash=0.85, segments=10, rings=4)]
    for s in (-1, 1):
        p.append(cylinder(f"{n}_arm{s}", 0.06, 0.55, (s * 0.25, 0, 0.78), SKIN_AM, verts=6))
    if cloak_on:
        p += [cylinder(n + "_cloak", 0.26, 0.66, (0, 0.02, 0.68), cloak, verts=10, r_top=0.21), cylinder(n + "_border", 0.265, 0.06, (0, 0.02, 0.68), border, verts=10),
              dome(n + "_knot", 0.06, (0.13, -0.13, 1.3), cloak, segments=6, rings=4)]
    return p


def am_woman(n, huipil=COTTON, band=RED, skirt="#4A5A78"):
    """A woman in a huipil and a wrap skirt (cueitl), hair twisted into two 'horns'."""
    p = [cylinder(n + "_skirt", 0.25, 0.8, (0, 0, 0), skirt, verts=10, r_top=0.21), cylinder(n + "_huipil", 0.25, 0.55, (0, 0, 0.7), huipil, verts=10, r_top=0.2),
         cylinder(n + "_band", 0.255, 0.07, (0, 0, 0.7), band, verts=10), blk(n + "_neck", 0.16, 0.02, 0.1, (0, -0.2, 1.17), band),
         dome(n + "_head", 0.112, (0, 0, 1.27), SKIN_AM, squash=1.45, segments=10, rings=6), dome(n + "_hair", 0.122, (0, 0.015, 1.34), HAIR, squash=0.85, segments=10, rings=4)]
    for s in (-1, 1):
        p += [cylinder(f"{n}_arm{s}", 0.055, 0.45, (s * 0.25, 0, 0.76), SKIN_AM, verts=6), cylinder(f"{n}_horn{s}", 0.04, 0.12, (s * 0.05, -0.04, 1.42), HAIR, verts=5, r_top=0.012)]
    return p


def am_kneel(n, huipil=COTTON, band=RED, skirt="#4A5A78"):
    """A woman kneeling (vendor, cook), facing -Y."""
    p = [cylinder(n + "_skirt", 0.3, 0.32, (0, 0.05, 0), skirt, verts=10, r_top=0.24), cylinder(n + "_huipil", 0.24, 0.5, (0, 0.05, 0.3), huipil, verts=10, r_top=0.19),
         cylinder(n + "_band", 0.245, 0.06, (0, 0.05, 0.3), band, verts=10),
         dome(n + "_head", 0.112, (0, 0.05, 0.85), SKIN_AM, squash=1.45, segments=10, rings=6), dome(n + "_hair", 0.122, (0, 0.065, 0.92), HAIR, squash=0.85, segments=10, rings=4)]
    for s in (-1, 1):
        p += [rod(f"{n}_arm{s}", 0.05, (s * 0.22, 0.05, 0.75), (s * 0.15, -0.25, 0.4), SKIN_AM, verts=5), cylinder(f"{n}_horn{s}", 0.04, 0.12, (s * 0.05, 0.01, 1.0), HAIR, verts=5, r_top=0.012)]
    return p


def tlameme(n, load="bundle", color="#C9B79A", loin=COTTON):
    """A tlameme: a porter with a carrying frame (cacaxtli) on his back, held by a tumpline across his forehead."""
    p = am_man(n, cloak_on=False, loin=loin)
    for s in (-1, 1):
        p += [rod(f"{n}_up{s}", 0.02, (s * 0.17, 0.22, 0.45), (s * 0.17, 0.22, 1.32), WOOD, verts=4),
              rod(f"{n}_tump{s}", 0.014, (s * 0.15, 0.2, 1.22), (s * 0.1, -0.05, 1.47), "#C9B79A", verts=4)]
    p += [rod(n + "_bar", 0.02, (-0.19, 0.22, 0.5), (0.19, 0.22, 0.5), WOOD, verts=4), box(n + "_band", 0.2, 0.03, 0.04, (0, -0.09, 1.46), "#C9B79A")]
    if load == "pots":
        p += [cylinder(n + "_pot1", 0.16, 0.32, (0, 0.25, 0.52), CLAY, verts=8, r_top=0.09), cylinder(n + "_pot2", 0.14, 0.28, (0, 0.25, 0.84), CLAY_D, verts=8, r_top=0.07)]
    elif load == "maize":
        p += [cylinder(n + "_basket", 0.17, 0.5, (0, 0.24, 0.52), STRAW, verts=8, r_top=0.19), dome(n + "_cobs", 0.18, (0, 0.24, 1.02), "#E0B84A", squash=0.6, segments=8, rings=4)]
    else:
        p += [blk(n + "_load", 0.4, 0.26, 0.55, (0, 0.25, 0.85), color), box(n + "_rope", 0.41, 0.27, 0.04, (0, 0.25, 0.8), "#5A4632")]
    return p


def turkey(n):
    p = [blk(n + "_body", 0.3, 0.46, 0.28, (0, 0.02, 0.42), "#3E3330"), blk(n + "_tail", 0.48, 0.05, 0.38, (0, 0.27, 0.6), "#5A4636", rot=(-0.35, 0, 0)),
         box(n + "_tip", 0.48, 0.055, 0.06, (0, 0.335, 0.76), CREAM), box(n + "_neck", 0.06, 0.06, 0.22, (0, -0.2, 0.5), "#7C93A6"),
         box(n + "_head", 0.08, 0.12, 0.08, (0, -0.22, 0.72), "#7C93A6"), box(n + "_wattle", 0.035, 0.035, 0.1, (0, -0.27, 0.64), "#B0302A")]
    for s in (-1, 1):
        p.append(rod(f"{n}_leg{s}", 0.018, (s * 0.07, 0.0, 0.3), (s * 0.07, 0.0, 0.0), "#B07A5A", verts=4))
    return p


def am_walker():
    m = Prop("prop-americas-walker")
    m.add("base", am_man("w"))
    return m


def am_matron():
    m = Prop("prop-americas-matron")
    p = am_woman("m") + [cylinder("basket", 0.13, 0.16, (0.12, -0.24, 0.66), STRAW, verts=8, r_top=0.15), dome("tomatoes", 0.13, (0.12, -0.24, 0.82), "#C9573A", squash=0.5, segments=8, rings=4)]
    m.add("base", p)
    return m


def am_porter():
    m = Prop("prop-americas-porter")
    m.add("base", tlameme("p", "bundle", "#C9B79A"))
    return m


def am_mule():
    m = Prop("prop-americas-mule")
    m.add("base", [place(tlameme("a", "maize"), (0.1, -0.8, 0)), place(tlameme("b", "bundle", "#9A8A6A"), (-0.1, 0.75, 0))])
    return m


def am_litter():
    """A lord's litter under a feather canopy, carried by four bearers."""
    m = Prop("prop-americas-litter")
    p = [box("platform", 1.0, 1.3, 0.14, (0, 0, 1.08), "#7A2E2A"), box("seat_back", 0.9, 0.12, 0.6, (0, 0.55, 1.22), GOLD)]
    for sx in (-0.45, 0.45):
        for sy in (-0.58, 0.58):
            p.append(rod(f"post{sx}{sy}", 0.03, (sx, sy, 1.22), (sx, sy, 2.25), GOLD, verts=5))
    p += [box("canopy", 1.15, 1.4, 0.12, (0, 0, 2.25), TEAL), dome("knob", 0.12, (0, 0, 2.37), GOLD, segments=8, rings=4)]
    fringe_cols = ["#2F7A5A", "#B0302A", "#2F7A5A", GOLD]
    for k in range(8):
        x = -0.5 + k * (1.0 / 7)
        p += [box(f"ff{k}", 0.1, 0.04, 0.28, (x, -0.7, 2.0), fringe_cols[k % 4]), box(f"fb{k}", 0.1, 0.04, 0.28, (x, 0.7, 2.0), fringe_cols[(k + 1) % 4])]
    for k in range(6):
        y = -0.55 + k * 0.22
        p += [box(f"fl{k}", 0.04, 0.1, 0.28, (-0.575, y, 2.0), fringe_cols[k % 4]), box(f"fr{k}", 0.04, 0.1, 0.28, (0.575, y, 2.0), fringe_cols[(k + 1) % 4])]
    # the lord, seated cross-legged, with a turquoise diadem and a feather plume
    p += [box("lord_lap", 0.5, 0.4, 0.18, (0, 0.0, 1.22), CREAM), cylinder("lord_body", 0.2, 0.5, (0, 0.15, 1.22), "#3E7A8A", verts=8, r_top=0.16),
          dome("lord_head", 0.11, (0, 0.15, 1.8), SKIN_AM, squash=1.45, segments=10, rings=6), cylinder("diadem", 0.12, 0.12, (0, 0.15, 1.85), "#3FA0A0", verts=8),
          blk("plume", 0.3, 0.05, 0.3, (0, 0.24, 2.0), "#2F7A5A", rot=(-0.3, 0, 0))]
    for s in (-1, 1):
        p.append(rod(f"pole{s}", 0.045, (s * 0.6, -2.05, 1.25), (s * 0.6, 2.05, 1.25), WOOD, verts=6))
    for i, (sx, sy) in enumerate([(-1, -1), (1, -1), (-1, 1), (1, 1)]):
        p.append(place(am_man(f"b{i}", cloak_on=False), (sx * 0.62, sy * 1.75, 0)))
    m.add("base", p)
    return m


def am_handcart():
    """A woman with a big basket on her back, held by a tumpline; her child beside her."""
    m = Prop("prop-americas-handcart")
    w = am_woman("w", skirt="#6E5A44")
    w += [cylinder("basket", 0.22, 0.5, (0, 0.33, 0.6), STRAW, verts=8, r_top=0.26), dome("load", 0.25, (0, 0.33, 1.1), "#E0B84A", squash=0.55, segments=8, rings=4),
          rod("tump_l", 0.014, (-0.2, 0.3, 1.08), (-0.1, -0.05, 1.36), "#C9B79A", verts=4), rod("tump_r", 0.014, (0.2, 0.3, 1.08), (0.1, -0.05, 1.36), "#C9B79A", verts=4)]
    child = place(am_man("child", cloak_on=False), (0.45, -0.55, 0), s=0.62)
    m.add("base", [place(w, (-0.12, 0.2, 0)), child])
    return m


def am_cart():
    m = Prop("prop-americas-cart")
    m.add("base", [place(tlameme("a", "pots"), (0.25, -1.9, 0)), place(tlameme("b", "bundle", "#C9B79A"), (-0.2, 0.0, 0)), place(tlameme("c", "maize"), (0.2, 1.9, 0))])
    return m


def _mat_stall(name, goods, vendor, shade_col=COTTON, big=False):
    """A market place on a petate mat under a cloth shade on four poles; the vendor kneels behind."""
    m = Prop(name)
    k = 1.25 if big else 1.0
    p = [box("mat", 2.2 * k, 1.8 * k, 0.03, (0, 0.1, 0), STRAW)]
    for i in range(4):
        p.append(box(f"weave{i}", 2.2 * k, 0.05, 0.035, (0, 0.1 - 0.7 * k + i * 0.47 * k, 0), "#B39C55"))
    for sx in (-1.15 * k, 1.15 * k):
        p += [rod(f"polef{sx}", 0.035, (sx, -0.75 * k, 0), (sx, -0.75 * k, 1.85), WOOD, verts=5), rod(f"poleb{sx}", 0.035, (sx, 1.0 * k, 0), (sx, 1.0 * k, 2.2), WOOD, verts=5)]
    p.append(blk("shade", 2.45 * k, 2.0 * k, 0.04, (0, 0.12 * k, 2.03), shade_col, rot=(0.19, 0, 0)))
    p += goods
    p.append(place(vendor, (0.35 * k, 0.75 * k, 0)))
    m.add("base", p)
    return m


def am_stall_fruit():
    goods = []
    piles = [("#E0B84A", "maize"), ("#B0302A", "chillies"), ("#C9573A", "tomatoes"), ("#6B4A32", "cacao"), ("#6E8A3A", "squash"), ("#7A3A5A", "maize")]
    for i, (col, _) in enumerate(piles):
        x, y = -0.75 + (i % 3) * 0.75, -0.45 + (i // 3) * 0.55
        goods += [cylinder(f"bk{i}", 0.24, 0.14, (x, y, 0.03), STRAW, verts=8, r_top=0.27), dome(f"pile{i}", 0.24, (x, y, 0.17), col, squash=0.55, segments=8, rings=4)]
    for i in range(5):
        goods.append(rod(f"cob{i}", 0.05, (-0.95 + i * 0.12, -0.95, 0.06), (-0.95 + i * 0.12, -0.7, 0.06), "#E0B84A", verts=5))
    return _mat_stall("prop-americas-stall-fruit", goods, am_kneel("v"))


def am_stall_pots():
    goods = []
    for i in range(6):
        x, y = -0.8 + (i % 3) * 0.8, -0.5 + (i // 3) * 0.55
        goods.append(cylinder(f"olla{i}", 0.2, 0.34, (x, y, 0.03), CLAY if i % 2 else "#C27A4A", verts=10, r_top=0.11))
        goods.append(cylinder(f"rim{i}", 0.12, 0.05, (x, y, 0.37), shade(CLAY, -0.2), verts=10))
    for i in range(3):
        goods += [cylinder(f"comal{i}", 0.26, 0.03, (-0.7 + i * 0.7, -0.92, 0.03), CLAY_D, verts=12), dome(f"bowl{i}", 0.13, (-0.4 + i * 0.6, 0.05, 0.03), "#D8C3A0", squash=0.5, segments=8, rings=4)]
    return _mat_stall("prop-americas-stall-pots", goods, am_kneel("v", skirt="#6E5A44"), shade_col=CREAM)


def am_stall_cloth():
    goods = []
    for i in range(6):
        x, y = -0.8 + (i % 3) * 0.75, -0.55 + (i // 3) * 0.5
        goods += [box(f"stack{i}", 0.5, 0.38, 0.16 + 0.04 * (i % 3), (x, y, 0.03), COTTON), box(f"stripe{i}", 0.51, 0.06, 0.17 + 0.04 * (i % 3), (x, y - 0.12, 0.03), [RED, "#4C6E9A", OCHRE][i % 3])]
    goods.append(rod("line", 0.02, (-1.15, 0.95, 1.6), (1.15, 0.95, 1.6), "#5A4632", verts=4))
    for i in range(3):
        goods.append(box(f"manta{i}", 0.55, 0.03, 0.9, (-0.7 + i * 0.7, 0.95, 0.7), [COTTON, "#C9A24A", "#4C6E9A"][i]))
    for i, col in enumerate(("#2F7A5A", "#B0302A", "#3FA0A0")):
        x = -0.9 + i * 0.9
        goods += [disc(f"shield{i}", 0.24, (x, -1.0, 0.35), (0, -1, 0.35), 0.04, col, verts=12), disc(f"boss{i}", 0.08, (x, -1.025, 0.36), (0, -1, 0.35), 0.03, GOLD, verts=8),
                  rod(f"stand{i}", 0.02, (x, -0.95, 0.0), (x, -0.98, 0.3), WOOD, verts=4)]
    return _mat_stall("prop-americas-stall-cloth", goods, am_kneel("v", huipil=CREAM, band="#4C6E9A"), shade_col="#C9B79A")


def am_stall():
    """Obsidian blades laid out on a mat, and turkeys for sale tethered beside it."""
    goods = []
    for i in range(14):
        goods.append(box(f"blade{i}", 0.05, 0.28, 0.02, (-0.95 + (i % 7) * 0.2, -0.55 + (i // 7) * 0.4, 0.04), OBSIDIAN, rot_z=0.1 * (i % 3 - 1)))
    for i in range(4):
        goods.append(cylinder(f"core{i}", 0.08, 0.2, (-0.6 + i * 0.3, 0.25, 0.03), OBSIDIAN, verts=6, r_top=0.03))
    goods += [disc("mirror", 0.16, (0.75, 0.25, 0.08), (0, -0.3, 1), 0.03, "#3A3A44", verts=10)]
    for i, (x, y, rz) in enumerate([(-1.05, -1.25, 0.4), (-0.2, -1.4, -0.2), (0.75, -1.2, 0.9)]):
        goods.append(place(turkey(f"t{i}"), (x, y, 0), rz=rz))
    goods.append(rod("tether", 0.01, (-1.05, -1.25, 0.05), (0.75, -1.2, 0.05), "#5A4632", verts=4))
    return _mat_stall("prop-americas-stall", goods, am_man("v", cloak="#C9A24A", border="#4C6E9A"), shade_col="#D8CDB0", big=True)


def am_forge():
    """An obsidian workshop: a knapper striking blades from a core, a polisher, piles of debitage."""
    m = Prop("prop-americas-forge")
    p = [box("ground", 7.0, 7.6, 0.08, (0, 0.6, 0), "#CDBE9E"), box("wall", 6.6, 0.4, 2.2, (0, 3.6, 0.08), ADOBE),
         hip_roof("ramada", 5.0, 3.2, 1.0, (0, 1.9, 2.4), THATCH, ridge=0.5, overhang=0.35)]
    for sx in (-2.4, 2.4):
        for sy in (0.4, 3.3):
            p.append(rod(f"post{sx}{sy}", 0.08, (sx, sy, 0.08), (sx, sy, 2.4), WOOD, verts=6))
    p += [box("anvil_stone", 0.55, 0.5, 0.42, (0.3, 0.0, 0.08), "#8C8A84"), cylinder("core", 0.1, 0.22, (0.3, 0.0, 0.5), OBSIDIAN, verts=6, r_top=0.04)]
    for i in range(12):
        a = i * 2.4
        p.append(box(f"chip{i}", 0.06, 0.04, 0.02, (0.3 + 0.55 * math.cos(a) * (0.6 + 0.04 * i), -0.1 + 0.4 * math.sin(a), 0.08), OBSIDIAN, rot_z=a))
    p += [box("blade_mat", 1.6, 0.9, 0.02, (-1.6, -0.8, 0.08), STRAW)]
    for i in range(10):
        p.append(box(f"blade{i}", 0.05, 0.3, 0.02, (-2.2 + i * 0.13, -0.8, 0.1), OBSIDIAN))
    for i in range(3):
        p += [cylinder(f"nod_basket{i}", 0.26, 0.3, (1.7 + i * 0.6, 2.6, 0.08), STRAW, verts=8, r_top=0.28), dome(f"nodules{i}", 0.25, (1.7 + i * 0.6, 2.6, 0.38), OBSIDIAN, squash=0.5, segments=8, rings=4)]
    p += [place(am_kneel("polisher", huipil=COTTON, skirt="#6E5A44"), (-1.6, 1.4, 0.08)), box("polish_stone", 0.5, 0.35, 0.15, (-1.6, 1.0, 0.08), "#8C8A84"),
          box("hearth", 0.7, 0.7, 0.12, (-2.4, 2.7, 0.08), "#6E6A62"), box("embers", 0.45, 0.45, 0.05, (-2.4, 2.7, 0.2), FIRE)]
    # a customer: a warrior come for a new macuahuitl
    p += [place(am_man("warrior", cloak="#E9E1CF", border="#2F7A5A"), (2.3, -2.3, 0.08)), rod("macuahuitl", 0.035, (2.55, -2.25, 0.85), (2.6, -2.6, 0.08 + 0.1), WOOD, verts=4)]
    # the knapper stands behind the core, facing -Y; his striking arm (with an antler billet) is animated
    kn = am_man("knapper", cloak_on=False)
    kn = [o for o in kn if not o.name.endswith("_arm1")]
    p.append(place(kn, (0.3, 0.72, 0.08)))
    m.add("base", p)
    sx, sy, sz = 0.55, 0.72, 1.33
    phi = 0.35
    d = Vector((0, -math.sin(phi), -math.cos(phi)))
    S = Vector((sx, sy, sz))
    m.add("anim_hammer", [rod("arm", 0.06, S, S + d * 0.55, SKIN_AM, verts=6), rod("billet", 0.03, S + d * 0.5, S + d * 0.82, CREAM, verts=5),
                          dome("hammerstone", 0.07, S + d * 0.82 - Vector((0, 0, 0.05)), "#7C7A74", segments=6, rings=4)], pivot=(sx, sy, sz))
    m.marker("marker_smoke", (-2.4, 2.7, 3.6))
    return m


def maize(n, h=2.0):
    p = [rod(n + "_stalk", 0.035, (0, 0, 0.1), (0, 0, h), "#7A9A4A", verts=4)]
    for k, (a, z) in enumerate(((0.6, 0.6), (2.6, 1.0), (4.4, 1.4))):
        p.append(rod(f"{n}_leaf{k}", 0.03, (0, 0, z), (0.45 * math.cos(a), 0.45 * math.sin(a), z + 0.25), "#6E9A4A", verts=3, r_top=0.005))
    p.append(box(n + "_ear", 0.07, 0.07, 0.22, (0.05, 0, 0.95), "#D8C07A"))
    return p


def am_farmer():
    """A milpa: maize on mounds; a farmer with a digging stick (coa) plants a row, his wife sows behind."""
    m = Prop("prop-americas-farmer")
    team = am_man("farmer", cloak_on=False)
    team += [rod("coa", 0.03, (0.25, -0.15, 1.0), (0.3, -0.75, 0.0), WOOD, verts=4), box("coa_rest", 0.12, 0.04, 0.04, (0.29, -0.6, 0.18), WOOD),
             rod("coa_top", 0.03, (0.25, -0.15, 1.0), (0.22, 0.05, 1.3), WOOD, verts=4)]
    team = [place(team, (0.3, 0, 0))]
    team += [place(am_woman("wife", skirt="#6E5A44") + [cylinder("seedbag", 0.12, 0.2, (0.28, -0.05, 0.62), COTTON, verts=6)], (0.4, 1.4, 0))]
    team += [box(f"hole{i}", 0.25, 0.25, 0.08, (0.6, 1.0 + i * 0.8, 0.06), "#6E5A40") for i in range(3)]
    m.add("anim_walk", team, pivot=(0, 0, 0))
    base = [box("soil", 5.8, 18, 0.06, (0, 0, 0), EARTH)]
    for r, x in enumerate((-2.6, -1.85, -1.1)):
        for k in range(13):
            y = -8.4 + k * 1.4 + (0.35 if r % 2 else 0)
            base.append(box(f"mound{r}_{k}", 0.42, 0.42, 0.14, (x, y, 0.06), "#7A6448"))
            base.append(place(maize(f"mz{r}_{k}", 1.7 + 0.25 * ((k + r) % 3)), (x, y, 0.15), rz=(k * 1.7 + r)))
    for r, x in enumerate((1.4, 2.15)):
        for k in range(13):
            y = -8.4 + k * 1.4 + (0.35 if r % 2 else 0)
            base += [box(f"ym{r}_{k}", 0.42, 0.42, 0.14, (x, y, 0.06), "#7A6448"), box(f"sprout{r}_{k}", 0.1, 0.1, 0.25, (x, y, 0.2), "#7A9A4A")]
    for k in range(6):
        base.append(dome(f"squash{k}", 0.18, (-0.4 + 0.1 * (k % 2), -7.5 + k * 3.0, 0.06), "#C98A3A" if k % 2 else "#6E8A3A", squash=0.7, segments=6, rings=4))
    m.add("base", base)
    return m


def am_wagon():
    m = Prop("prop-americas-wagon")
    p = [place(am_man("merchant", cloak="#4C6E9A", border=OCHRE) + [rod("staff", 0.02, (0.3, -0.1, 0), (0.3, -0.1, 1.7), "#3A2A1E", verts=4)], (0.0, -4.55, 0))]
    for i, (load, col) in enumerate((("bundle", "#C9B79A"), ("pots", None), ("maize", None), ("bundle", "#9A8A6A"))):
        p.append(place(tlameme(f"t{i}", load, col or "#C9B79A"), (0.15 * (-1) ** i, -3.2 + i * 2.1, 0)))
    m.add("base", p)
    return m


def am_bakery():
    """A house-yard kitchen: a woman grinds maize on a metate, tortillas on a comal over the three
    hearthstones, a pot of nixtamal stirred with a paddle (the spinning part)."""
    m = Prop("prop-americas-bakery")
    p = [box("yard", 6.6, 7.0, 0.08, (0, 0, 0), "#D9CDB5"), box("house", 5.6, 2.3, 2.3, (0, 2.3, 0.08), ADOBE), box("door", 0.9, 0.05, 1.5, (-0.8, 1.13, 0.08), "#3A2A1E"),
         hip_roof("roof", 5.6, 2.3, 1.4, (0, 2.3, 2.38), THATCH, ridge=0.45, overhang=0.3)]
    # the hearth: three stones, fire, comal with tortillas
    hx, hy = -1.4, -0.4
    for k in range(3):
        a = k * math.tau / 3 + 0.3
        p.append(cylinder(f"tenamaztli{k}", 0.12, 0.28, (hx + 0.3 * math.cos(a), hy + 0.3 * math.sin(a), 0.08), "#6E6A62", verts=6))
    p += [box("fire", 0.3, 0.3, 0.1, (hx, hy, 0.08), FIRE), cylinder("comal", 0.45, 0.04, (hx, hy, 0.36), CLAY_D, verts=12)]
    for k in range(3):
        p.append(cylinder(f"tortilla{k}", 0.12, 0.015, (hx - 0.2 + k * 0.2, hy + 0.05 * (k - 1), 0.4), "#E8DDB8", verts=8))
    # the metate and the woman grinding
    mx, my = -1.4, -1.9
    p += [blk("metate", 0.4, 0.7, 0.1, (mx, my, 0.28), "#7C7A74", rot=(-0.18, 0, 0)), rod("mano", 0.05, (mx - 0.25, my - 0.05, 0.38), (mx + 0.25, my - 0.05, 0.38), "#8C8A84", verts=6)]
    for sx, sy in ((-0.15, -0.28), (0.15, -0.28), (0, 0.28)):
        p.append(box(f"mleg{sx}{sy}", 0.08, 0.08, 0.24, (mx + sx, my + sy, 0.08), "#7C7A74"))
    p.append(place(am_kneel("grinder"), (mx, my - 0.7, 0.08), rz=math.pi))
    p += [cylinder("maize_basket", 0.25, 0.25, (-2.4, -1.6, 0.08), STRAW, verts=8, r_top=0.28), dome("cobs", 0.25, (-2.4, -1.6, 0.33), "#E0B84A", squash=0.5, segments=8, rings=4)]
    # the nixtamal pot over a second fire, the cook beside it
    px, py = 1.4, -1.0
    for k in range(3):
        a = k * math.tau / 3
        p.append(cylinder(f"pstone{k}", 0.1, 0.22, (px + 0.4 * math.cos(a), py + 0.4 * math.sin(a), 0.08), "#6E6A62", verts=6))
    p += [box("pfire", 0.3, 0.3, 0.1, (px, py, 0.08), FIRE), cylinder("olla", 0.42, 0.45, (px, py, 0.25), CLAY, verts=12, r_top=0.32),
          cylinder("olla_rim", 0.34, 0.08, (px, py, 0.7), shade(CLAY, -0.2), verts=12), cylinder("lime", 0.3, 0.02, (px, py, 0.72), "#E8DDB8", verts=12),
          place(am_woman("cook", skirt="#6E5A44"), (px + 0.85, py + 0.3, 0.08), rz=math.pi / 2)]
    p += [cylinder("water_jar", 0.22, 0.6, (2.5, 0.6, 0.08), CLAY_D, verts=8, r_top=0.1), cylinder("water_jar2", 0.2, 0.55, (2.0, 0.75, 0.08), CLAY, verts=8, r_top=0.09)]
    p += [place(turkey("t0"), (2.4, -2.8, 0.08), rz=0.6), place(am_man("child", cloak_on=False), (-0.2, -2.9, 0.08), s=0.62)]
    m.add("base", p)
    m.add("anim_spin", [rod("paddle", 0.025, (px + 0.12, py, 0.55), (px + 0.2, py, 1.35), WOOD, verts=5), blk("paddle_blade", 0.1, 0.04, 0.25, (px + 0.12, py, 0.6), WOOD)], pivot=(px, py, 0))
    m.marker("marker_smoke", (hx, hy, 1.4))
    return m


def am_shepherd():
    """A turkey keeper with his flock, a hairless dog (xoloitzcuintli) and a cane pen."""
    m = Prop("prop-americas-shepherd")
    rnd = random.Random(17)
    flock = [place(turkey(f"t{i}"), (x, y, 0), rz=rnd.uniform(-math.pi, math.pi)) for i, (x, y) in enumerate(scatter(13, 3.4, 2.3, rnd, 0.85))]
    m.add("anim_graze", flock)
    base = [place(am_man("keeper", cloak="#D8CDB0", border="#6E5A44") + [rod("stick", 0.02, (0.3, -0.1, 0), (0.35, -0.3, 1.5), WOOD, verts=4)], (4.9, 0.9, 0))]
    dog = [box("dog_body", 0.22, 0.55, 0.22, (0, 0, 0.28), "#4A4A4C"), box("dog_head", 0.15, 0.22, 0.15, (0, -0.35, 0.48), "#4A4A4C"),
           box("dog_ear_l", 0.04, 0.03, 0.12, (-0.05, -0.3, 0.6), "#4A4A4C"), box("dog_ear_r", 0.04, 0.03, 0.12, (0.05, -0.3, 0.6), "#4A4A4C")]
    dog += [box(f"dog_leg{i}", 0.06, 0.06, 0.3, ((i % 2 - 0.5) * 0.14, (i // 2 - 0.5) * 0.4, 0), "#3A3A3C") for i in range(4)]
    base.append(place(dog, (4.2, -0.2, 0), rz=0.4))
    px, py = 5.3, -1.9
    for i in range(14):
        a = math.tau * i / 14
        base.append(rod(f"cane{i}", 0.025, (px + 0.8 * math.cos(a), py + 0.7 * math.sin(a), 0), (px + 0.8 * math.cos(a), py + 0.7 * math.sin(a), 0.9), BAMBOO, verts=4))
    base.append(box("pen_floor", 1.4, 1.2, 0.02, (px, py, 0), STRAW))
    m.add("base", base)
    return m


def am_crowd():
    m = Prop("prop-americas-crowd")
    rnd = random.Random(23)
    cloaks = [(CREAM, RED), ("#C9A24A", "#4C6E9A"), ("#4F7A74", CREAM), ("#D8CDB0", "#6E5A44"), (COTTON, TEAL)]
    ppl = []
    for i, (x, y) in enumerate(scatter(9, 2.6, 1.8, rnd, 1.05)):
        if i % 3 == 1:
            fig = am_woman(f"w{i}", skirt=["#4A5A78", "#6E5A44", COTTON][i % 3], band=[RED, TEAL, OCHRE][i % 3])
        elif i == 4:   # a warrior in quilted cotton armour with a round shield
            fig = am_man(f"m{i}", cloak="#E8DDB8", border="#E8DDB8") + [disc("shield", 0.28, (-0.3, -0.05, 0.9), (1, -0.3, 0), 0.04, "#2F7A5A", verts=10)]
        else:
            c, b = cloaks[i % 5]
            fig = am_man(f"m{i}", cloak=c, border=b)
        ppl.append(place(fig, (x, y, 0), rz=rnd.uniform(-math.pi, math.pi)))
    ppl += [box("bench", 2.2, 0.45, 0.42, (-0.4, 2.45, 0), G2), box("altar", 1.0, 1.0, 0.4, (2.8, -2.2, 0), G3), box("altar2", 0.7, 0.7, 0.35, (2.8, -2.2, 0.4), G2),
            cylinder("brazier", 0.18, 0.25, (2.8, -2.2, 0.75), CLAY, verts=8, r_top=0.22)]
    m.add("base", ppl)
    return m


def am_boat():
    """A large dugout canoe (acalli) loaded with goods: a poler at the stern, a paddler at the bow."""
    m = Prop("prop-americas-boat")
    H = "#6B4A32"
    p = [hull("hull", 12.0, 1.5, 0.7, H), box("inside", 1.15, 10.6, 0.03, (0, 0, 0.67), shade(H, -0.35))]
    loads = [("bundle", "#C9B79A"), ("pots", None), ("maize", None), ("bundle", "#9A8A6A"), ("pots", None), ("bundle", COTTON)]
    for i, (kind, col) in enumerate(loads):
        y = -3.4 + i * 1.3
        if kind == "pots":
            p += [cylinder(f"pot{i}a", 0.24, 0.42, (-0.22, y, 0.62), CLAY, verts=8, r_top=0.12), cylinder(f"pot{i}b", 0.22, 0.38, (0.24, y + 0.1, 0.62), CLAY_D, verts=8, r_top=0.1)]
        elif kind == "maize":
            p += [cylinder(f"bk{i}", 0.4, 0.35, (0, y, 0.62), STRAW, verts=8, r_top=0.45), dome(f"cobs{i}", 0.42, (0, y, 0.97), "#E0B84A", squash=0.5, segments=8, rings=4)]
        else:
            p.append(box(f"bale{i}", 1.0, 0.9, 0.5, (0, y, 0.62), col))
    p += [place(am_man("poler", cloak_on=False), (0, 4.6, 0.62)), rod("pole", 0.03, (0.25, 4.5, 1.6), (0.75, 5.8, -0.4), WOOD, verts=4),
          place(am_kneel("paddler", huipil="#D8CDB0", band="#6E5A44", skirt="#D8CDB0"), (0, -4.7, 0.62)),
          rod("paddle", 0.025, (0.22, -4.9, 1.2), (0.6, -5.2, 0.1), WOOD, verts=4), blk("paddle_blade", 0.04, 0.16, 0.4, (0.62, -5.2, 0.2), WOOD, rot=(0.3, 0.33, 0))]
    m.add("base", p)
    return m


def am_skiff():
    m = Prop("prop-americas-skiff")
    p = [hull("hull", 4.6, 0.85, 0.45, "#7A5C40"), box("inside", 0.6, 3.8, 0.03, (0, 0, 0.43), "#4A3426"),
         place(am_man("paddler", cloak_on=False), (0, 0.9, 0.35), s=0.92), rod("paddle", 0.022, (0.2, 0.75, 1.15), (0.55, 0.4, 0.05), WOOD, verts=4),
         blk("blade", 0.03, 0.14, 0.35, (0.57, 0.38, 0.15), WOOD, rot=(0, 0.3, 0)), box("net", 0.4, 0.5, 0.15, (0, -1.1, 0.43), "#C9B79A"),
         box("fish", 0.08, 0.3, 0.06, (0.1, -0.5, 0.45), "#9AA4A8")]
    m.add("base", p)
    return m


# ================================================================ ANDES (Cusco)
SKIN_AN = "#A9764F"
ANBLK, ANRED, ANYEL, ANBLUE, ANGREEN = "#2E2B2A", "#A8322A", "#D9A93A", "#3E5A8A", "#4E6B3A"


def an_man(n, uncu=ANBLK, check=True, mantle="#8A6A4E", cap=ANRED, cape=True):
    """A man in an uncu (tunic) with a checker panel and red yoke, a mantle behind, a knitted cap."""
    p = [cylinder(n + "_ll", 0.08, 0.5, (-0.1, 0.07, 0), SKIN_AN, verts=6), cylinder(n + "_rl", 0.08, 0.5, (0.1, -0.07, 0), SKIN_AN, verts=6),
         box(n + "_uncu", 0.46, 0.34, 0.8, (0, 0, 0.47), uncu), blk(n + "_yoke", 0.17, 0.02, 0.17, (0, -0.172, 1.15), ANRED, rot=(0, math.pi / 4, 0)),
         cylinder(n + "_neck", 0.06, 0.08, (0, 0, 1.26), SKIN_AN, verts=6), dome(n + "_head", 0.115, (0, 0, 1.33), SKIN_AN, squash=1.45, segments=10, rings=6),
         cylinder(n + "_cap", 0.125, 0.22, (0, 0, 1.42), cap, verts=8, r_top=0.035)]
    if check:   # a tocapu checker panel
        for i in range(4):
            p.append(box(f"{n}_chk{i}", 0.1, 0.02, 0.1, (-0.06 + 0.12 * (i % 2), -0.171, 0.62 + 0.1 * (i // 2)), "#EDE6D6" if (i % 2) == (i // 2) else ANRED))
    for s in (-1, 1):
        p += [cylinder(f"{n}_arm{s}", 0.055, 0.5, (s * 0.27, 0, 0.72), SKIN_AN, verts=6), box(f"{n}_flap{s}", 0.04, 0.09, 0.14, (s * 0.115, 0, 1.33), cap)]
    if cape:
        p.append(box(n + "_mantle", 0.52, 0.06, 0.72, (0, 0.2, 0.55), mantle))
    return p


def an_woman(n, aksu="#3A3346", lliclla=ANRED, belt=ANYEL, head=ANRED):
    """A woman in an aksu dress, a lliclla shawl pinned with a tupu, braids and a folded head cloth."""
    p = [cylinder(n + "_aksu", 0.25, 1.22, (0, 0, 0), aksu, verts=10, r_top=0.2), cylinder(n + "_belt", 0.226, 0.08, (0, 0, 0.72), belt, verts=10),
         cylinder(n + "_lliclla", 0.235, 0.34, (0, 0, 0.92), lliclla, verts=10, r_top=0.17), cylinder(n + "_stripe", 0.236, 0.04, (0, 0, 1.0), ANYEL, verts=10),
         rod(n + "_tupu", 0.012, (0, -0.23, 1.24), (0.04, -0.23, 1.04), "#BFC3C6", verts=4), disc(n + "_tupu_head", 0.05, (0, -0.24, 1.25), (0, -1, 0), 0.02, "#BFC3C6", verts=8),
         dome(n + "_head", 0.112, (0, 0, 1.26), SKIN_AN, squash=1.45, segments=10, rings=6), dome(n + "_hair", 0.122, (0, 0.015, 1.33), HAIR, squash=0.85, segments=10, rings=4),
         box(n + "_cloth", 0.26, 0.28, 0.04, (0, 0.02, 1.4), head)]
    for s in (-1, 1):
        p.append(rod(f"{n}_braid{s}", 0.025, (s * 0.07, 0.08, 1.33), (s * 0.08, 0.15, 0.92), HAIR, verts=4))
    return p


def an_kneel(n, aksu="#3A3346", lliclla=ANRED, head=ANRED):
    p = [cylinder(n + "_aksu", 0.3, 0.32, (0, 0.05, 0), aksu, verts=10, r_top=0.24), cylinder(n + "_body", 0.22, 0.32, (0, 0.05, 0.3), aksu, verts=10, r_top=0.2),
         cylinder(n + "_lliclla", 0.235, 0.3, (0, 0.05, 0.5), lliclla, verts=10, r_top=0.17),
         dome(n + "_head", 0.112, (0, 0.05, 0.84), SKIN_AN, squash=1.45, segments=10, rings=6), dome(n + "_hair", 0.122, (0, 0.065, 0.91), HAIR, squash=0.85, segments=10, rings=4),
         box(n + "_cloth", 0.26, 0.28, 0.04, (0, 0.07, 0.98), head)]
    for s in (-1, 1):
        p.append(rod(f"{n}_arm{s}", 0.05, (s * 0.2, 0.05, 0.72), (s * 0.14, -0.25, 0.4), SKIN_AN, verts=5))
    return p


def llama(n, color="#EDE6D6", load=True, sack=ANRED):
    p = [box(n + "_body", 0.36, 0.95, 0.45, (0, 0.1, 0.72), color), blk(n + "_neck", 0.16, 0.18, 0.65, (0, -0.3, 1.38), color, rot=(0.15, 0, 0)),
         box(n + "_head", 0.15, 0.3, 0.15, (0, -0.44, 1.65), shade(color, -0.08)), box(n + "_tail", 0.08, 0.1, 0.18, (0, 0.6, 1.0), color)]
    for s in (-1, 1):
        p += [box(f"{n}_ear{s}", 0.04, 0.04, 0.14, (s * 0.05, -0.36, 1.78), color), box(f"{n}_tassel{s}", 0.05, 0.05, 0.06, (s * 0.06, -0.36, 1.88), ANRED)]
    for sx in (-0.11, 0.11):
        for sy in (-0.25, 0.45):
            p.append(box(f"{n}_leg{sx}{sy}", 0.09, 0.09, 0.75, (sx, sy, 0), shade(color, -0.15)))
    if load:
        for s in (-1, 1):
            p += [box(f"{n}_sack{s}", 0.15, 0.5, 0.34, (s * 0.25, 0.1, 0.78), sack), box(f"{n}_sackband{s}", 0.155, 0.08, 0.345, (s * 0.25, 0.1, 0.78), ANYEL)]
        p.append(box(n + "_blanket", 0.62, 0.5, 0.04, (0, 0.1, 1.17), "#C9B79A"))
    return p


def alpaca(n, color):
    p = [box(n + "_body", 0.4, 0.72, 0.42, (0, 0.06, 0.45), color), box(n + "_neck", 0.18, 0.2, 0.45, (0, -0.24, 0.78), color),
         box(n + "_head", 0.16, 0.24, 0.16, (0, -0.32, 1.18), shade(color, -0.05)), box(n + "_top", 0.18, 0.14, 0.08, (0, -0.28, 1.34), color)]
    for s in (-1, 1):
        p.append(box(f"{n}_ear{s}", 0.035, 0.035, 0.1, (s * 0.05, -0.24, 1.37), color))
    for sx in (-0.11, 0.11):
        for sy in (-0.2, 0.3):
            p.append(box(f"{n}_leg{sx}{sy}", 0.09, 0.09, 0.45, (sx, sy, 0), shade(color, -0.2)))
    return p


def an_walker():
    m = Prop("prop-andean-walker")
    m.add("base", an_man("w"))
    return m


def an_matron():
    m = Prop("prop-andean-matron")
    m.add("base", an_woman("m"))
    return m


def an_carrier(n, cloth=ANRED, uncu="#6E5A44"):
    """A carrier with a cloth bundle (q'ipi) on his back, its ends knotted across his chest."""
    p = an_man(n, uncu=uncu, check=False, cape=False, cap="#3E5A8A")
    p += [blk(n + "_bundle", 0.44, 0.28, 0.46, (0, 0.24, 0.95), cloth), box(n + "_bstripe", 0.45, 0.29, 0.06, (0, 0.24, 0.93), ANYEL),
          rod(n + "_end_l", 0.03, (-0.17, 0.2, 1.15), (0.0, -0.19, 1.05), cloth, verts=4), rod(n + "_end_r", 0.03, (0.17, 0.2, 1.15), (0.0, -0.19, 1.05), cloth, verts=4),
          dome(n + "_knot", 0.05, (0, -0.2, 1.02), cloth, segments=6, rings=4)]
    return p


def an_porter():
    m = Prop("prop-andean-porter")
    m.add("base", an_carrier("p"))
    return m


def an_mule():
    m = Prop("prop-andean-mule")
    p = [place(llama("l", "#EDE6D6"), (0, 0.35, 0)), place(an_man("herder", uncu="#6E5A44", check=False), (0.55, -1.0, 0)),
         rod("lead", 0.01, (0.3, -0.95, 0.95), (0.0, -0.05, 1.68), "#5A4632", verts=4)]
    m.add("base", p)
    return m


def an_litter():
    """The Inca's litter: a gilded seat under a canopy, carried by bearers in blue livery."""
    m = Prop("prop-andean-litter")
    p = [box("platform", 1.0, 1.3, 0.16, (0, 0, 1.06), GOLD), box("throne", 0.6, 0.5, 0.3, (0, 0.2, 1.22), shade(GOLD, -0.2)),
         box("back", 0.8, 0.1, 0.65, (0, 0.55, 1.22), GOLD)]
    for sx in (-0.45, 0.45):
        for sy in (-0.58, 0.58):
            p.append(rod(f"post{sx}{sy}", 0.03, (sx, sy, 1.22), (sx, sy, 2.3), GOLD, verts=5))
    p += [box("canopy", 1.12, 1.36, 0.1, (0, 0, 2.3), ANRED), hip_roof("canopy_top", 1.0, 1.25, 0.28, (0, 0, 2.4), GOLD, ridge=0.2, overhang=0.04)]
    for k in range(7):
        x = -0.48 + k * 0.16
        p += [box(f"ff{k}", 0.08, 0.03, 0.2, (x, -0.69, 2.12), GOLD if k % 2 else ANRED), box(f"fb{k}", 0.08, 0.03, 0.2, (x, 0.69, 2.12), GOLD if k % 2 else ANRED)]
    p += [box("inca_lap", 0.48, 0.38, 0.16, (0, 0.0, 1.52), "#2E2B2A"), cylinder("inca_body", 0.19, 0.5, (0, 0.18, 1.52), "#2E2B2A", verts=8, r_top=0.15)]
    for i in range(4):
        p.append(box(f"inca_chk{i}", 0.08, 0.02, 0.08, (-0.05 + 0.1 * (i % 2), 0.0, 1.62 + 0.09 * (i // 2)), "#EDE6D6" if (i % 2) == (i // 2) else ANRED))
    p += [dome("inca_head", 0.11, (0, 0.18, 2.0), SKIN_AN, squash=1.45, segments=10, rings=6), cylinder("llautu", 0.12, 0.06, (0, 0.18, 2.06), ANRED, verts=8),
          box("mascapaycha", 0.14, 0.02, 0.08, (0, 0.06, 1.98), "#C23B2B"), box("feathers", 0.04, 0.04, 0.16, (0, 0.18, 2.14), "#EDE6D6")]
    for s in (-1, 1):
        p.append(rod(f"pole{s}", 0.05, (s * 0.6, -2.05, 1.25), (s * 0.6, 2.05, 1.25), shade(GOLD, -0.3), verts=6))
    for i, (sx, sy) in enumerate([(-1, -1), (1, -1), (-1, 1), (1, 1)]):
        p.append(place(an_man(f"b{i}", uncu=ANBLUE, check=False, cape=False, cap="#EDE6D6"), (sx * 0.62, sy * 1.75, 0)))
    m.add("base", p)
    return m


def an_handcart():
    """A woman carrying a bundle of firewood on her back, a dog at her heel."""
    m = Prop("prop-andean-handcart")
    w = an_woman("w", lliclla="#8A5A9A")
    for k in range(7):
        w.append(rod(f"stick{k}", 0.035, (-0.42, 0.25 + 0.04 * (k % 2), 0.85 + 0.07 * k), (0.42, 0.25 + 0.04 * ((k + 1) % 2), 0.85 + 0.07 * k + 0.03), "#7A5C40", verts=5))
    w += [rod("rope_l", 0.014, (-0.15, 0.25, 1.3), (-0.08, -0.2, 1.05), "#C9B79A", verts=4), rod("rope_r", 0.014, (0.15, 0.25, 1.3), (0.08, -0.2, 1.05), "#C9B79A", verts=4)]
    dog = [box("dog_body", 0.2, 0.5, 0.22, (0, 0, 0.26), "#8A6A4E"), box("dog_head", 0.15, 0.2, 0.15, (0, -0.32, 0.44), "#8A6A4E"),
           box("dog_tail", 0.04, 0.12, 0.04, (0, 0.3, 0.45), "#8A6A4E")] + [box(f"dog_leg{i}", 0.06, 0.06, 0.28, ((i % 2 - 0.5) * 0.12, (i // 2 - 0.5) * 0.36, 0), "#6E5238") for i in range(4)]
    m.add("base", [place(w, (-0.1, 0.25, 0)), place(dog, (0.45, -0.55, 0), rz=0.2)])
    return m


def an_cart():
    m = Prop("prop-andean-cart")
    p = [place(llama("l1", "#EDE6D6"), (0.3, -1.0, 0)), place(llama("l2", "#6E5238", sack="#3E5A8A"), (-0.2, 1.2, 0)),
         place(an_man("herder", uncu="#6E5A44", check=False), (-0.55, -2.45, 0)), rod("lead", 0.01, (-0.3, -2.4, 0.95), (0.3, -1.5, 1.68), "#5A4632", verts=4)]
    m.add("base", p)
    return m


def an_stall_fruit():
    goods = []
    cols = ["#8A6A4A", "#6B3A5A", "#D9B85A", "#E0C070", "#EDE3C8", "#7A3A5A"]  # potatoes (brown, purple, yellow), maize (yellow, white, purple)
    for i, col in enumerate(cols):
        x, y = -0.75 + (i % 3) * 0.75, -0.45 + (i // 3) * 0.55
        goods.append(cylinder(f"cloth{i}", 0.3, 0.02, (x, y, 0.03), [ANRED, ANBLUE, ANYEL][i % 3], verts=8))
        for k in range(5):
            a = k * 1.3
            goods.append(dome(f"tuber{i}{k}", 0.09, (x + 0.12 * math.cos(a) * (k > 0), y + 0.12 * math.sin(a) * (k > 0), 0.05 + 0.06 * (k == 0)), col, squash=0.8, segments=6, rings=4))
    for i in range(3):
        goods += [cylinder(f"sack{i}", 0.2, 0.4, (-0.7 + i * 0.7, -0.95, 0.03), "#C9B79A", verts=8, r_top=0.17)]
    return _mat_stall("prop-andean-stall-fruit", goods, an_kneel("v"), shade_col="#C9B79A")


def aryballo(n, h=0.5, col=CLAY):
    r = h * 0.38
    return [cylinder(n + "_base", r * 0.25, h * 0.45, (0, 0, 0), col, verts=8, r_top=r), cylinder(n + "_shoulder", r, h * 0.35, (0, 0, h * 0.45), col, verts=8, r_top=r * 0.3),
            cylinder(n + "_band", r * 0.98, h * 0.08, (0, 0, h * 0.38), CREAM, verts=8),
            cylinder(n + "_neck", r * 0.22, h * 0.22, (0, 0, h * 0.78), col, verts=8, r_top=r * 0.4)]


def an_stall_pots():
    goods = []
    for i in range(6):
        x, y = -0.8 + (i % 3) * 0.8, -0.5 + (i // 3) * 0.6
        goods.append(place(aryballo(f"ar{i}", 0.5 + 0.1 * (i % 2), CLAY if i % 3 else "#C27A4A"), (x, y, 0.03)))
    for i in range(4):
        goods += [cylinder(f"kero{i}", 0.07, 0.16, (-0.9 + i * 0.25, -0.95, 0.03), "#8A5A3A", verts=8, r_top=0.09), dome(f"plate{i}", 0.13, (0.25 + i * 0.25, -0.95, 0.03), "#D8C3A0", squash=0.35, segments=8, rings=4)]
    return _mat_stall("prop-andean-stall-pots", goods, an_kneel("v", lliclla="#3E5A8A"), shade_col="#D8CDB0")


def an_stall_cloth():
    goods = []
    cols = [ANRED, ANBLUE, ANYEL, "#6B3A5A", ANGREEN, "#EDE6D6"]
    for i in range(6):
        x, y = -0.8 + (i % 3) * 0.75, -0.55 + (i // 3) * 0.5
        h = 0.14 + 0.04 * (i % 3)
        goods += [box(f"stack{i}", 0.5, 0.38, h, (x, y, 0.03), cols[i]), box(f"stripe{i}", 0.51, 0.39, 0.03, (x, y, 0.03 + h * 0.5), cols[(i + 2) % 6])]
    goods.append(rod("line", 0.02, (-1.15, 0.95, 1.6), (1.15, 0.95, 1.6), "#5A4632", verts=4))
    for i in range(3):
        goods += [box(f"manta{i}", 0.55, 0.03, 0.9, (-0.7 + i * 0.7, 0.95, 0.7), cols[i]), box(f"mstripe{i}", 0.56, 0.035, 0.08, (-0.7 + i * 0.7, 0.95, 1.1), cols[i + 3])]
    goods += [box(f"awayu{i}", 0.45, 0.32, 0.08, (0.55 + 0.5 * i, -0.98, 0.03), cols[(i + 1) % 6]) for i in range(2)]
    return _mat_stall("prop-andean-stall-cloth", goods, an_kneel("v", lliclla=ANGREEN), shade_col="#C9B79A")


def an_stall():
    """A coca seller: leaves dried on cloths, woven bags (chuspa), a buyer counting out."""
    goods = []
    for i in range(5):
        x, y = -0.85 + (i % 3) * 0.8, -0.55 + (i // 3) * 0.6
        goods += [box(f"cloth{i}", 0.6, 0.5, 0.02, (x, y, 0.03), [ANRED, ANBLUE, ANYEL][i % 3]), dome(f"coca{i}", 0.24, (x, y, 0.05), ANGREEN if i % 2 else "#6E8A4A", squash=0.35, segments=8, rings=4)]
    for i in range(4):
        goods.append(box(f"chuspa{i}", 0.2, 0.06, 0.24, (0.6 + 0.24 * (i % 2), 0.15 + 0.15 * (i // 2), 0.03), [ANRED, "#6B3A5A", ANBLUE, ANYEL][i]))
    goods.append(place(an_man("buyer", uncu="#6E5A44", check=False), (-0.6, -1.3, 0), rz=math.pi * 0.9))
    return _mat_stall("prop-andean-stall", goods, an_kneel("v", lliclla="#6B3A5A"), shade_col="#D8CDB0", big=True)


def an_forge():
    """An Inca stone yard: a mason dresses an ashlar with a hammerstone; a fitted wall rises behind,
    a block waits on its sledge with the haulers' ropes."""
    m = Prop("prop-andean-forge")
    p = [box("ground", 7.2, 8.4, 0.08, (0, 0.6, 0), "#BDAE92")]
    rnd = random.Random(3)
    tones = ["#A8A08E", "#9C9483", "#B3AB98", "#A39A86"]
    z = 0.08
    for course, hgt in enumerate((1.0, 0.85, 0.7)):
        x = -3.2 + (0.4 if course % 2 else 0)
        k = 0
        while x < 3.1:
            w = min(rnd.uniform(1.0, 1.7), 3.2 - x)
            if w > 0.3:
                p.append(box(f"ash{course}_{k}", w - 0.03, 1.1 - 0.12 * course, hgt - 0.03, (x + w / 2, 3.4 + 0.06 * course, z), tones[(course + k) % 4]))
            x += w
            k += 1
        z += hgt
    p += [box("block", 1.3, 0.9, 0.75, (0.3, -0.25, 0.08), "#B3AB98"), box("dressed_face", 1.31, 0.02, 0.6, (0.3, -0.7, 0.15), "#C9C1AE")]
    for i in range(10):
        a = i * 2.2
        p.append(box(f"chip{i}", 0.12, 0.09, 0.05, (0.3 + 1.0 * math.cos(a), -0.3 + 0.75 * math.sin(a), 0.08), "#C9C1AE", rot_z=a))
    for i in range(3):
        p.append(dome(f"hammerstones{i}", 0.08, (1.4 + i * 0.18, 0.5, 0.08), "#5A5650", segments=6, rings=4))
    p += [box("sledge_l", 0.12, 2.0, 0.12, (-2.5, -2.4, 0.08), WOOD), box("sledge_r", 0.12, 2.0, 0.12, (-1.5, -2.4, 0.08), WOOD),
          box("sledge_block", 1.2, 1.1, 0.8, (-2.0, -2.35, 0.2), "#A39A86"), rod("rope_a", 0.025, (-2.3, -2.9, 0.5), (-2.4, -4.3, 1.05), STRAW, verts=4),
          rod("rope_b", 0.025, (-1.7, -2.9, 0.5), (-1.6, -4.5, 1.05), STRAW, verts=4), rod("bar", 0.03, (-2.5, -1.4, 0.08), (-3.2, -0.6, 0.9), "#8A7A58", verts=4)]
    p += [place(an_man("hauler1", uncu="#6E5A44", check=False, cape=False), (-2.4, -4.55, 0.08)), place(an_man("hauler2", uncu="#8A6A4E", check=False, cape=False), (-1.55, -4.75, 0.08))]
    p += [place(an_man("overseer", uncu=ANBLK) + [rod("quipu", 0.012, (0.27, -0.05, 0.6), (0.27, -0.05, 0.25), "#C9A24A", verts=4)], (2.4, -2.2, 0.08), rz=0.4)]
    mz = 0.08
    mason = an_man("mason", uncu="#8A6A4E", check=False, cape=False)
    mason = [o for o in mason if not o.name.endswith("_arm1")]
    my = 0.66
    p.append(place(mason, (0.3, my, mz)))
    m.add("base", p)
    sx, sy, sz = 0.57, my, mz + 1.2
    phi = 0.6
    d = Vector((0, -math.sin(phi), -math.cos(phi)))
    S = Vector((sx, sy, sz))
    m.add("anim_hammer", [rod("arm", 0.055, S, S + d * 0.5, SKIN_AN, verts=6), dome("hammerstone", 0.11, S + d * 0.58 - Vector((0, 0, 0.08)), "#5A5650", squash=1.2, segments=8, rings=4)], pivot=(sx, sy, sz))
    return m


def an_farmer():
    """Terraced fields: two men turn the soil with the chaki taklla foot-plough, a woman breaks the clods."""
    m = Prop("prop-andean-farmer")

    def taklla(n, x, y):
        f = an_man(n, uncu="#6E5A44", check=False, cape=False)
        f += [rod(n + "_shaft", 0.03, (0.22, -0.2, 1.25), (0.25, -0.75, 0.0), WOOD, verts=4), box(n + "_step", 0.14, 0.05, 0.04, (0.3, -0.62, 0.32), WOOD),
              rod(n + "_handle", 0.025, (0.1, -0.2, 1.25), (0.35, -0.2, 1.3), WOOD, verts=4)]
        return place(f, (x, y, 0))

    team = [taklla("ploughman1", 0.2, 0.0), taklla("ploughman2", 1.2, 0.5), place(an_kneel("clodbreaker", lliclla="#6B3A5A"), (0.7, 1.7, 0), rz=math.pi),
            rod("clod_club", 0.025, (0.6, 1.4, 0.45), (0.65, 1.1, 0.1), WOOD, verts=4)]
    for k in range(4):
        team.append(box(f"turned{k}", 0.35, 0.5, 0.1, (0.2 + (k % 2), -0.9 - 0.6 * (k // 2), 0.04), "#6E5A40"))
    m.add("anim_walk", team, pivot=(0, 0, 0))
    base = [box("level0", 3.9, 18, 0.05, (1.05, 0, 0), EARTH), box("riser0", 0.3, 18, 0.8, (-0.85, 0, 0), STONE_A),
            box("level1", 1.25, 18, 0.8, (-1.6, 0, 0), EARTH), box("riser1", 0.3, 18, 1.6, (-2.2, 0, 0), STONE_A),
            box("level2", 0.75, 18, 1.6, (-2.7, 0, 0), EARTH)]
    for k in range(4):   # furrows already turned
        base.append(box(f"furrow{k}", 0.2, 18, 0.05, (1.8 + k * 0.32, 0, 0.05), "#6E5A40"))
    for r, (x, z) in enumerate(((-1.85, 0.8), (-1.35, 0.8), (-2.7, 1.6))):
        for k in range(16):
            y = -8.4 + k * 1.12
            base.append(box(f"potato{r}_{k}", 0.32, 0.32, 0.22, (x, y, z), "#5E7A44"))
    for k in range(4):   # stone steps projecting from the riser walls
        base.append(box(f"step{k}", 0.25, 0.4, 0.06, (-0.6 if k < 2 else -1.95, 4.0, 0.25 + 0.3 * (k % 2) + 0.8 * (k // 2)), STONE_A))
    base.append(box("seed_sack", 0.4, 0.3, 0.45, (2.6, -4.0, 0.05), "#C9B79A"))
    m.add("base", base)
    return m


def an_wagon():
    m = Prop("prop-andean-wagon")
    p = [place(an_man("leader", uncu="#6E5A44", check=False), (0.45, -4.25, 0)),
         place(llama("l1", "#EDE6D6"), (0.0, -2.75, 0)), place(llama("l2", "#6E5238", sack=ANBLUE), (0.15, -0.6, 0)), place(llama("l3", "#2E2B2A", sack=ANYEL), (-0.1, 1.55, 0)),
         place(an_man("drover", uncu="#8A6A4E", check=False, cap="#3E5A8A"), (-0.4, 3.35, 0)),
         rod("lead", 0.01, (0.3, -4.15, 0.95), (0.0, -3.25, 1.68), "#5A4632", verts=4)]
    m.add("base", p)
    return m


def an_bakery():
    """A chicha brewery in a house yard: a woman stirs a great jar on the fire (the spinning paddle),
    aryballos stand ready, another woman grinds maize on a batan."""
    m = Prop("prop-andean-bakery")
    p = [box("yard", 6.6, 7.0, 0.08, (0, 0, 0), "#C9BB9E"), box("house", 5.6, 2.3, 2.3, (0, 2.2, 0.08), STONE_A),
         box("door", 0.7, 0.05, 1.5, (-1.0, 1.03, 0.08), "#3A2A1E")]
    roof = gable_roof("roof", 2.3, 5.6, 1.6, (0, 0, 0), THATCH, overhang=0.3)
    p.append(place(roof, (0, 2.2, 2.38), rz=math.pi / 2))
    for i in range(5):
        p.append(place(aryballo(f"ar{i}", 0.9, CLAY if i % 2 else "#C27A4A"), (-2.4 + i * 0.6 + (1.0 if i > 1 else 0), 0.55, 0.08)))
    jx, jy = -1.2, -1.0
    for k in range(3):
        a = k * math.tau / 3
        p.append(cylinder(f"stone{k}", 0.12, 0.25, (jx + 0.5 * math.cos(a), jy + 0.5 * math.sin(a), 0.08), "#6E6A62", verts=6))
    p += [box("fire", 0.35, 0.35, 0.1, (jx, jy, 0.08), FIRE), cylinder("jar", 0.55, 0.7, (jx, jy, 0.25), CLAY, verts=12, r_top=0.4),
          cylinder("jar_mouth", 0.38, 0.08, (jx, jy, 0.95), shade(CLAY, -0.2), verts=12), cylinder("chicha", 0.33, 0.02, (jx, jy, 0.98), "#D9B87A", verts=12)]
    p.append(place(an_woman("brewer"), (jx - 0.9, jy - 0.15, 0.08), rz=-math.pi / 2))
    bx, by = 1.5, -1.5
    p += [box("batan", 0.7, 0.9, 0.12, (bx, by, 0.08), "#7C7A74"), blk("una", 0.5, 0.18, 0.2, (bx, by - 0.1, 0.3), "#8C8A84", rot=(0, 0.25, 0)),
          place(an_kneel("grinder", lliclla="#3E5A8A"), (bx, by + 0.75, 0.08)),
          cylinder("maize_basket", 0.25, 0.25, (2.5, -0.6, 0.08), STRAW, verts=8, r_top=0.28), dome("maize", 0.25, (2.5, -0.6, 0.33), "#E0C070", squash=0.5, segments=8, rings=4),
          place(an_man("drinker", uncu="#6E5A44", check=False), (1.2, -2.9, 0.08), rz=0.6), cylinder("kero", 0.06, 0.14, (1.0, -3.15, 0.95), "#8A5A3A", verts=6, r_top=0.08)]
    m.add("base", p)
    m.add("anim_spin", [rod("paddle", 0.03, (jx + 0.15, jy, 0.75), (jx + 0.3, jy, 1.75), WOOD, verts=5), blk("paddle_blade", 0.12, 0.04, 0.3, (jx + 0.15, jy, 0.8), WOOD)], pivot=(jx, jy, 0))
    m.marker("marker_smoke", (jx, jy, 2.0))
    return m


def an_shepherd():
    """A herder with alpacas on the puna, spinning wool with a drop spindle; a stone corral."""
    m = Prop("prop-andean-shepherd")
    rnd = random.Random(29)
    cols = ["#EDE6D6", "#8A6A4E", "#3A322C", "#C9B79A", "#EDE6D6", "#6E5238"]
    herd = [place(alpaca(f"a{i}", cols[i % 6]), (x, y, 0), rz=rnd.uniform(-math.pi, math.pi)) for i, (x, y) in enumerate(scatter(11, 3.5, 2.4, rnd, 1.25))]
    m.add("anim_graze", herd)
    base = [place(an_woman("herder", lliclla="#6B3A5A") + [rod("spindle", 0.012, (0.25, -0.2, 0.9), (0.25, -0.2, 0.45), WOOD, verts=4),
                                                         cylinder("whorl", 0.05, 0.03, (0.25, -0.2, 0.5), CLAY_D, verts=8), dome("wool", 0.08, (-0.22, -0.1, 1.05), "#EDE6D6", segments=6, rings=4)], (4.9, 0.9, 0))]
    for k in range(9):
        a = -0.6 + k * 0.32
        base.append(box(f"pirka{k}", 0.5, 0.35, 0.6 - 0.1 * (k % 2), (5.2 + 1.0 * math.cos(a + math.pi / 2) * 0.0 + 0.9 * math.sin(a), -1.9 + 0.9 * math.cos(a), 0), STONE_A, rot_z=a))
    for k in range(7):
        x, y = rnd.uniform(-4.5, 4.5), rnd.choice((-1, 1)) * rnd.uniform(2.7, 3.1)
        base.append(cylinder(f"ichu{k}", 0.18, 0.35, (x, y, 0), STRAW, verts=6, r_top=0.02))
    m.add("base", base)
    return m


def an_crowd():
    m = Prop("prop-andean-crowd")
    rnd = random.Random(31)
    ppl = []
    uncus = [ANBLK, "#6E5A44", ANBLUE, "#8A6A4E", ANRED]
    for i, (x, y) in enumerate(scatter(9, 2.6, 1.8, rnd, 1.05)):
        if i % 3 == 1:
            fig = an_woman(f"w{i}", aksu=["#3A3346", "#4A3A30", "#2E3A48"][i % 3], lliclla=[ANRED, "#6B3A5A", ANGREEN, ANBLUE][i % 4])
        else:
            fig = an_man(f"m{i}", uncu=uncus[i % 5], check=i % 4 == 0, cap=[ANRED, ANBLUE, ANYEL, "#EDE6D6"][i % 4])
        ppl.append(place(fig, (x, y, 0), rz=rnd.uniform(-math.pi, math.pi)))
    ppl += [box("bench", 2.2, 0.45, 0.42, (-0.4, 2.45, 0), STONE_A), box("channel", 0.4, 1.6, 0.35, (2.9, -1.8, 0), "#9C9483"), box("channel_water", 0.2, 1.6, 0.02, (2.9, -1.8, 0.35), WATER),
            box("basin", 0.9, 0.7, 0.3, (2.9, -2.4, 0), STONE_A)]
    m.add("base", ppl)
    return m


def reed_hull(n, length, beam, depth, curl, color="#C9B26A", bands=4):
    secs = []
    N = 15
    for i in range(N):
        t = -1 + 2 * i / (N - 1)
        s = max(0.12, (1 - abs(t) ** 2.4) ** 0.5)
        secs.append((t * length / 2, beam / 2 * s, depth / 2 * s, depth / 2 + curl * abs(t) ** 3.5))
    p = [tube(n, secs, color)]
    for b in range(bands):
        t = -0.75 + 1.5 * b / max(1, bands - 1)
        s = max(0.12, (1 - abs(t) ** 2.4) ** 0.5)
        zc = depth / 2 + curl * abs(t) ** 3.5
        y = t * length / 2
        p.append(tube(f"{n}_band{b}", [(y - 0.06, beam / 2 * s * 1.04, depth / 2 * s * 1.04, zc), (y + 0.06, beam / 2 * s * 1.04, depth / 2 * s * 1.04, zc)], "#8A7A48"))
    return p


def an_boat():
    """A totora reed boat with upswept ends and a reed-mat sail on a bipod mast; a poler and a passenger."""
    m = Prop("prop-andean-boat")
    p = reed_hull("hull", 11.0, 2.0, 1.0, 1.4)
    p += [box("deck", 1.2, 6.0, 0.04, (0, 0, 0.98), "#B39C55")]
    for s in (-1, 1):
        p.append(rod(f"mast{s}", 0.05, (s * 0.55, -1.2, 1.0), (0, -1.2, 5.4), WOOD, verts=5))
    p += [box("sail", 2.2, 0.06, 2.8, (0, -1.1, 2.3), "#C9B26A"), rod("yard_top", 0.035, (-1.15, -1.1, 5.1), (1.15, -1.1, 5.1), WOOD, verts=4),
          rod("yard_bot", 0.035, (-1.15, -1.1, 2.3), (1.15, -1.1, 2.3), WOOD, verts=4)]
    for k in range(5):
        p.append(box(f"sail_line{k}", 2.2, 0.065, 0.04, (0, -1.1, 2.75 + k * 0.5), "#A88A4A"))
    p += [box("bundle_a", 0.9, 0.8, 0.45, (0, 0.9, 1.0), ANRED), box("bundle_b", 0.8, 0.7, 0.4, (0.05, 1.8, 1.0), "#C9B79A"),
          place(an_man("poler", uncu="#6E5A44", check=False, cape=False), (0, 3.2, 1.0)), rod("pole", 0.03, (0.25, 3.0, 2.0), (0.9, 4.6, -0.4), WOOD, verts=4),
          place(an_kneel("passenger", lliclla=ANBLUE), (0, -2.6, 1.0))]
    m.add("base", p)
    return m


def an_skiff():
    m = Prop("prop-andean-skiff")
    p = reed_hull("hull", 5.0, 0.85, 0.5, 0.6, bands=3)
    p += [place(an_kneel("fisher", lliclla="#6E5A44", head="#6E5A44"), (0, 0.5, 0.45)), rod("cane", 0.022, (0.2, 0.25, 1.0), (0.55, -0.6, 0.0), BAMBOO, verts=4),
          box("net", 0.35, 0.4, 0.12, (0, -0.8, 0.45), "#C9B79A")]
    m.add("base", p)
    return m


# ---------------------------------------------------------------- registry
_SLOTS = ["walker", "matron", "porter", "mule", "litter", "handcart", "cart", "stall-fruit", "stall-pots", "stall-cloth", "stall",
          "forge", "farmer", "wagon", "bakery", "shepherd", "crowd", "boat", "skiff"]
_SETS = {
    "eastasian": [ea_walker, ea_matron, ea_porter, ea_mule, ea_litter, ea_handcart, ea_cart, ea_stall_fruit, ea_stall_pots, ea_stall_cloth, ea_stall,
                  ea_forge, ea_farmer, ea_wagon, ea_bakery, ea_shepherd, ea_crowd, ea_boat, ea_skiff],
    "americas": [am_walker, am_matron, am_porter, am_mule, am_litter, am_handcart, am_cart, am_stall_fruit, am_stall_pots, am_stall_cloth, am_stall,
                 am_forge, am_farmer, am_wagon, am_bakery, am_shepherd, am_crowd, am_boat, am_skiff],
    "andean": [an_walker, an_matron, an_porter, an_mule, an_litter, an_handcart, an_cart, an_stall_fruit, an_stall_pots, an_stall_cloth, an_stall,
               an_forge, an_farmer, an_wagon, an_bakery, an_shepherd, an_crowd, an_boat, an_skiff],
}
BUILDERS = {f"props/{s}/{slot}": fn for s, fns in _SETS.items() for slot, fn in zip(_SLOTS, fns)}
