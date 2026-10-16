"""
Life props: small study-model scenes that rise on hover (forge, farmer, wagon,
stall, bakery, cart, shepherd, crowd). Grey massing with a few colour accents.
Metres, origin at ground centre, facing -Y (south). Animated parts are separate
top-level objects named anim_<kind>_<name>; the web app animates them.
Everything else is merged into p0_base so each prop costs only a few draw calls.
"""
import math
from chronokit import *

class Prop:
    """Keeps named top-level parts separate, each with its own pivot, for animation in the web app."""

    def __init__(self, name):
        self.name = name
        self.objects = []

    def add(self, name, objs, pivot=(0, 0, 0)):
        objs = objs if isinstance(objs, list) else [objs]
        o = join(objs, name)
        bpy.ops.object.select_all(action="DESELECT")
        o.select_set(True)
        bpy.context.view_layer.objects.active = o
        bpy.ops.object.transform_apply(location=True, rotation=True, scale=True)
        bpy.context.scene.cursor.location = pivot
        bpy.ops.object.origin_set(type="ORIGIN_CURSOR")
        bpy.ops.object.shade_flat()
        self.objects.append(o)
        return o

    def marker(self, name, loc):
        e = bpy.data.objects.new(name, None)
        bpy.context.collection.objects.link(e)
        e.location = loc
        self.objects.append(e)

    def finish(self):
        return self.objects

    def export(self, path):
        return _export(self, path)


def _export(prop, path):
    bpy.ops.object.select_all(action="DESELECT")
    for o in prop.objects:
        o.select_set(True)
    kwargs = dict(filepath=path, export_format="GLB", use_selection=True, export_apply=True)
    props = bpy.ops.export_scene.gltf.get_rna_type().properties.keys()
    for k, v in dict(export_yup=True, export_animations=False, export_texcoords=False, export_normals=True, export_cameras=False, export_lights=False, export_extras=False).items():
        if k in props:
            kwargs[k] = v
    bpy.ops.export_scene.gltf(**kwargs)
    faces = sum(len(o.data.polygons) for o in prop.objects if o.type == "MESH")
    return {"file": path, "stages": [o.name for o in prop.objects], "faces": faces}


G1, G2, G3 = "#D9D8D3", "#C2C1BB", "#A9A8A2"     # study-model greys
SKIN, CLOTH_A, CLOTH_B, CLOTH_C = "#C9A27E", "#8E5A3C", "#6E7A58", "#5D6E80"
WOOD, IRON, FIRE, STRAW = "#8A6A4A", "#4A4A4A", "#D96A2B", "#C9B26A"


def person(name, loc=(0, 0, 0), cloth=CLOTH_A, h=1.75, rot=0.0, arms=True):
    x, y, z = loc
    parts = [
        cylinder(name + "_legs", 0.17, h * 0.45, (x, y, z), G3, verts=8, r_top=0.2),
        cylinder(name + "_body", 0.22, h * 0.36, (x, y, z + h * 0.45), cloth, verts=8, r_top=0.17),
        dome(name + "_head", 0.13, (x, y, z + h * 0.84), SKIN, squash=1.6, segments=10, rings=6),
    ]
    if arms:
        for s in (-1, 1):
            a = cylinder(f"{name}_arm{s}", 0.06, h * 0.33, (x + s * 0.26, y, z + h * 0.5), cloth, verts=6)
            parts.append(a)
    return join(parts, name)


def ox(name, loc=(0, 0, 0), rot=0.0, color="#9C8A72"):
    x, y, z = loc
    parts = [box(name + "_body", 0.8, 2.0, 0.9, (x, y, z + 0.7), color)]
    for sx in (-0.3, 0.3):
        for sy in (-0.7, 0.7):
            parts.append(box(f"{name}_leg{sx}{sy}", 0.18, 0.18, 0.7, (x + sx, y + sy, z), shade(color, -0.15)))
    parts.append(box(name + "_head", 0.45, 0.6, 0.5, (x, y - 1.15, z + 1.05), shade(color, -0.05)))
    for s in (-1, 1):
        parts.append(box(f"{name}_horn{s}", 0.35, 0.08, 0.08, (x + s * 0.3, y - 1.2, z + 1.5), "#EDE6D6"))
    o = join(parts, name)
    o.rotation_euler[2] = rot
    return o


def wheel(name, r, loc, axis="x", color=WOOD):
    o = cylinder(name, r, 0.12, (0, 0, 0), color, verts=12)
    o.rotation_euler = (0, math.pi / 2, 0) if axis == "x" else (math.pi / 2, 0, 0)
    bpy.ops.object.select_all(action="DESELECT")
    o.select_set(True)
    bpy.context.view_layer.objects.active = o
    bpy.ops.object.transform_apply(rotation=True)
    o.location = loc
    bpy.ops.object.transform_apply(location=True)
    return o


def forge():
    m = Prop("prop-forge")
    base = [
        box("floor", 7, 6, 0.15, color=G2),
        box("back_wall", 7, 0.4, 3.2, (0, 2.8, 0), G1),
        box("side_l", 0.4, 6, 1.2, (-3.3, 0, 0), G1),
        box("side_l_back", 0.4, 3, 3.2, (-3.3, 1.5, 0), G1),
        box("side_r", 0.4, 6, 1.2, (3.3, 0, 0), G1),
        box("side_r_back", 0.4, 3, 3.2, (3.3, 1.5, 0), G1),
        box("roof", 7.6, 3.0, 0.25, (0, 1.8, 3.2), G2),
        box("hearth", 1.8, 1.4, 0.9, (-2.0, 1.8, 0), G3),
        box("embers", 1.2, 0.9, 0.08, (-2.0, 1.8, 0.9), FIRE),
        box("chimney", 1.0, 1.0, 3.2, (-2.0, 2.3, 0.9), G3),
        box("bellows", 0.9, 0.6, 0.35, (-0.8, 2.0, 0.6), WOOD),
        cylinder("anvil_stump", 0.35, 0.55, (0.4, 0.0, 0), WOOD, verts=10),
        box("anvil", 0.75, 0.3, 0.25, (0.4, 0.0, 0.55), IRON),
        box("trough", 1.2, 0.5, 0.5, (1.9, 0.6, 0), G3),
        box("water", 1.05, 0.38, 0.05, (1.9, 0.6, 0.45), "#65888A"),
        box("rack", 0.15, 2.0, 1.6, (3.0, 0.5, 0), WOOD),
        person("customer", (2.2, -2.3, 0), CLOTH_B),
        box("horse_body", 0.7, 2.2, 0.9, (0.0, -4.0, 0.8), "#7B6650"),
        box("horse_neck", 0.4, 0.6, 0.9, (0.0, -5.0, 1.4), "#7B6650"),
    ]
    for sx in (-0.25, 0.25):
        for sy in (-0.8, 0.8):
            base.append(box(f"horse_leg{sx}{sy}", 0.16, 0.16, 0.8, (sx, -4.0 + sy, 0), "#5f4e3d"))
    base.append(person("smith", (0.4, -0.8, 0), CLOTH_A, arms=False))
    m.add("base", base)
    # the smith's hammer arm swings about the shoulder
    sx, sy, sz = 0.62, -0.75, 1.42
    m.add("anim_hammer", [cylinder("arm", 0.07, 0.62, (sx, sy, sz - 0.62), SKIN, verts=6), cylinder("handle", 0.03, 0.4, (sx, sy, sz - 0.95), WOOD, verts=6), box("hammer_head", 0.14, 0.3, 0.14, (sx, sy, sz - 1.0), IRON)], pivot=(sx, sy, sz))
    m.marker("marker_smoke", (-2.0, 2.3, 4.2))
    m.marker("marker_sparks", (0.4, 0.0, 0.85))
    return m


def farmer():
    m = Prop("prop-farmer")
    team = [ox("ox_l", (-0.55, 0, 0)), ox("ox_r", (0.55, 0, 0)), box("yoke", 1.9, 0.15, 0.15, (0, -0.9, 1.25), WOOD),
            box("beam", 0.12, 3.0, 0.12, (0, 2.3, 0.7), WOOD), box("share", 0.3, 0.6, 0.5, (0, 3.8, 0.1), IRON),
            box("handle", 0.1, 0.9, 0.08, (0, 4.2, 0.9), WOOD), person("ploughman", (0, 4.8, 0), CLOTH_B)]
    m.add("anim_walk", team, pivot=(0, 2, 0))
    furrows = [box(f"furrow{i}", 0.25, 18, 0.06, (-3 + i * 0.6, 0, 0), "#8A7350") for i in range(10)]
    m.add("base", furrows + [person("sower", (-2.8, -3, 0), CLOTH_C), box("basket", 0.5, 0.5, 0.45, (-2.4, -3.2, 0), STRAW)])
    return m


def wagon():
    m = Prop("prop-wagon")
    parts = [box("bed", 1.8, 3.6, 0.3, (0, 0.8, 0.9), WOOD)]
    for sy in (-0.2, 1.8):
        for sx in (-1.0, 1.0):
            parts.append(wheel(f"wheel{sx}{sy}", 0.6, (sx, sy, 0.6)))
    for i in range(5):
        a = math.pi * i / 4
        parts.append(box(f"hoop{i}", 1.9, 0.08, 0.08, (0, 0.8 - 1.6 + i * 0.8, 1.9), WOOD))
    cover = cylinder("cover", 1.0, 3.4, (0, 0, 0), "#E6DCC8", verts=12)
    cover.rotation_euler = (math.pi / 2, 0, 0)
    bpy.ops.object.select_all(action="DESELECT"); cover.select_set(True); bpy.context.view_layer.objects.active = cover
    bpy.ops.object.transform_apply(rotation=True)
    cover.location = (0, 0.8, 1.2)
    bpy.ops.object.transform_apply(location=True)
    bm = bmesh.new(); bm.from_mesh(cover.data)
    bmesh.ops.delete(bm, geom=[v for v in bm.verts if v.co.z < 1.2 + 0.05], context="VERTS")
    bm.to_mesh(cover.data); bm.free()
    parts.append(cover)
    parts += [box("pole", 0.12, 2.6, 0.12, (0, -2.2, 0.9), WOOD), ox("ox_l", (-0.55, -3.6, 0), color="#8C7A62"), ox("ox_r", (0.55, -3.6, 0), color="#A08E74"),
              person("driver", (0, -1.2, 1.2), CLOTH_A, h=1.5), box("chest", 0.8, 0.6, 0.5, (0.3, 2.3, 1.2), G3), cylinder("amphora", 0.25, 0.9, (-0.5, 2.2, 1.2), "#B5654A", verts=8, r_top=0.12)]
    parts.append(person("walker", (1.6, -1.0, 0), CLOTH_C))
    m.add("base", parts)
    return m


def stall():
    m = Prop("prop-stall")
    parts = [box("counter", 3.2, 1.0, 1.0, (0, 0, 0), WOOD), box("top", 3.4, 1.2, 0.08, (0, 0, 1.0), G1)]
    for sx in (-1.6, 1.6):
        for sy in (-0.5, 1.5):
            parts.append(box(f"post{sx}{sy}", 0.1, 0.1, 2.5, (sx, sy, 0), WOOD))
    awning = box("awning", 3.6, 2.4, 0.06, (0, 0.6, 2.5), "#B5654A")
    awning.rotation_euler[0] = 0.18
    parts.append(awning)
    for i in range(6):
        parts.append(box(f"crate{i}", 0.5, 0.4, 0.3, (-1.3 + i * 0.52, 0, 1.08), ["#C9A24A", "#8E5A3C", "#6E7A58"][i % 3]))
    for i in range(3):
        parts.append(cylinder(f"jar{i}", 0.22, 0.7, (-1.2 + i * 0.5, 1.3, 0), "#B5654A", verts=8, r_top=0.1))
    parts += [person("vendor", (0.4, 1.2, 0), CLOTH_A), person("buyer_a", (-0.6, -1.3, 0), CLOTH_C), person("buyer_b", (1.2, -1.6, 0), CLOTH_B, h=1.3)]
    m.add("base", parts)
    return m


def bakery():
    m = Prop("prop-bakery")
    parts = [box("floor", 7, 6, 0.15, color=G2), box("back", 7, 0.4, 3.0, (0, 2.8, 0), G1), box("side", 0.4, 6, 3.0, (3.3, 0, 0), G1),
             box("oven_base", 2.4, 2.4, 1.0, (-1.8, 1.6, 0), G3), dome("oven", 1.15, (-1.8, 1.6, 1.0), G2, squash=0.85),
             box("oven_mouth", 0.6, 0.1, 0.45, (-1.8, 0.45, 1.05), FIRE), box("chimney", 0.5, 0.5, 1.6, (-1.8, 2.3, 1.8), G3),
             box("table", 2.0, 0.9, 0.85, (1.4, 1.6, 0), WOOD), person("baker", (1.4, 0.7, 0), "#EDE6D6")]
    for i in range(6):
        parts.append(dome(f"loaf{i}", 0.16, (0.7 + i * 0.28, 1.6, 0.86), "#C9A24A", squash=0.6, segments=8, rings=4))
    m.add("base", parts)
    mx, my = 0.6, -3.0
    mill = [cylinder("mill_lower", 0.6, 1.0, (mx, my, 0), G3, verts=12), cylinder("mill_upper", 0.55, 0.8, (mx, my, 1.0), G2, verts=12, r_top=0.3),
            box("mill_bar", 2.6, 0.1, 0.1, (mx + 0.9, my, 1.4), WOOD)]
    donkey = [box("d_body", 0.5, 1.2, 0.6, (mx + 2.2, my, 0.6), "#8A8072")] + [box(f"d_leg{i}", 0.1, 0.1, 0.6, (mx + 2.2 + (i % 2 - 0.5) * 0.3, my + (i // 2 - 0.5) * 0.8, 0), "#6a6256") for i in range(4)] + [box("d_head", 0.3, 0.5, 0.4, (mx + 2.2, my - 0.8, 1.0), "#8A8072")]
    m.add("anim_spin", mill + donkey, pivot=(mx, my, 0))
    m.marker("marker_smoke", (-1.8, 2.3, 3.5))
    return m


def cart():
    m = Prop("prop-cart")
    parts = [box("bed", 1.6, 2.4, 0.25, (0, 0, 0.8), WOOD), wheel("wl", 0.65, (-0.9, 0.2, 0.65)), wheel("wr", 0.65, (0.9, 0.2, 0.65)),
             box("shafts", 1.0, 2.4, 0.1, (0, -2.2, 0.8), WOOD), box("mule", 0.55, 1.6, 0.75, (0, -3.4, 0.8), "#7B6650")]
    for i in range(6):
        parts.append(cylinder(f"amph{i}", 0.2, 0.8, (-0.45 + (i % 3) * 0.45, -0.5 + (i // 3) * 0.8, 1.05), "#B5654A", verts=8, r_top=0.08))
    parts += [person("porter_a", (1.6, 0.6, 0), CLOTH_B), person("porter_b", (-1.6, -0.4, 0), CLOTH_A), box("sack", 0.6, 0.4, 0.4, (1.6, 1.4, 0), STRAW),
              box("sacks", 1.2, 0.8, 0.6, (2.6, 0.0, 0), STRAW)]
    m.add("base", parts)
    return m


def shepherd():
    m = Prop("prop-shepherd")
    sheep = []
    import random
    rnd = random.Random(7)
    for i in range(14):
        x, y = rnd.uniform(-4, 4), rnd.uniform(-3, 3)
        sheep += [box(f"s{i}", 0.5, 0.8, 0.45, (x, y, 0.35), "#EDE6D6"), box(f"sh{i}", 0.22, 0.25, 0.25, (x, y - 0.5, 0.55), "#5a524a")]
        sheep += [box(f"sl{i}{j}", 0.08, 0.08, 0.35, (x + (j % 2 - 0.5) * 0.3, y + (j // 2 - 0.5) * 0.5, 0), "#5a524a") for j in range(4)]
    m.add("anim_graze", sheep)
    m.add("base", [person("shepherd", (4.5, 1.5, 0), CLOTH_B), box("crook", 0.06, 0.06, 2.0, (4.85, 1.5, 0), WOOD), box("dog", 0.3, 0.7, 0.4, (3.8, 0.6, 0.15), "#4a3b2c")])
    return m


def crowd():
    m = Prop("prop-crowd")
    import random
    rnd = random.Random(3)
    ppl = [person(f"p{i}", (rnd.uniform(-3, 3), rnd.uniform(-2, 2), 0), [CLOTH_A, CLOTH_B, CLOTH_C, "#EDE6D6"][i % 4], h=rnd.uniform(1.5, 1.8)) for i in range(9)]
    ppl += [box("bench", 2.4, 0.4, 0.45, (0, 2.6, 0), WOOD), cylinder("well", 0.6, 0.8, (2.8, -1.5, 0), G2, verts=12)]
    m.add("base", ppl)
    return m


BUILDERS = {
    "props/forge": forge, "props/farmer": farmer, "props/wagon": wagon, "props/stall": stall,
    "props/bakery": bakery, "props/cart": cart, "props/shepherd": shepherd, "props/crowd": crowd,
}


def hull(name, length, beam, depth, color=WOOD):
    """Simple tapered hull: a box whose bow and stern are pinched."""
    o = box(name, beam, length, depth, (0, 0, 0), color)
    bm = bmesh.new()
    bm.from_mesh(o.data)
    for v in bm.verts:
        if abs(v.co.y) > length * 0.49:
            v.co.x *= 0.15
            v.co.z += depth * 0.35 if v.co.z > depth * 0.5 else 0
    bm.to_mesh(o.data)
    bm.free()
    return o


def boat():
    """A river barge (codicaria) with a square sail and cargo of amphorae."""
    m = Prop("prop-boat")
    parts = [hull("hull", 14, 3.6, 1.4), box("deck", 3.0, 10, 0.12, (0, 0, 1.3), shade(WOOD, 0.15)),
             box("mast", 0.2, 0.2, 9, (0, 1.5, 1.3), WOOD), box("yard", 5.0, 0.15, 0.15, (0, 1.5, 9.0), WOOD),
             box("sail", 4.6, 0.06, 5.0, (0, 1.6, 3.8), "#E6DCC8"), box("cabin", 2.2, 2.4, 1.2, (0, -4.6, 1.3), G2),
             box("steering_oar", 0.2, 3.0, 0.15, (1.6, -6.8, 0.8), WOOD), person("helmsman", (0.6, -5.8, 1.3), CLOTH_A, h=1.6)]
    for i in range(8):
        parts.append(cylinder(f"amph{i}", 0.22, 0.85, (-0.7 + (i % 3) * 0.7, -2.6 + (i // 3) * 1.1, 1.4), "#B5654A", verts=8, r_top=0.08))
    m.add("base", parts)
    return m


def skiff():
    """A small rowing boat with two oarsmen and a fishing net."""
    m = Prop("prop-skiff")
    parts = [hull("hull", 6, 1.6, 0.7), person("rower_a", (0, 0.6, 0.6), CLOTH_B, h=1.3), person("rower_b", (0, -1.2, 0.6), CLOTH_C, h=1.3),
             box("oar_l", 3.2, 0.12, 0.08, (-1.4, 0.6, 1.1), WOOD), box("oar_r", 3.2, 0.12, 0.08, (1.4, 0.6, 1.1), WOOD), box("net", 0.9, 0.9, 0.3, (0, 2.0, 0.6), STRAW)]
    m.add("base", parts)
    return m


BUILDERS.update({"props/boat": boat, "props/skiff": skiff})


# ---------------------------------------------------------------- line bays (laid along walls and aqueducts)
STONE, STONE_D, STONE_L = "#C9B79A", "#A8967A", "#DCCDB3"


def aqueduct_bay():
    """One bay of an aqueduct: two half piers and a round arch, channel on top. 8 m long along +Y, origin at ground centre."""
    m = Prop("prop-aqueduct-bay")
    span, depth, pier_h, r = 8.0, 3.2, 10.0, 2.6
    body = box("body", depth, span, pier_h + r + 1.2, (0, 0, 0), STONE)
    bpy.ops.mesh.primitive_cylinder_add(vertices=20, radius=r, depth=depth + 2, location=(0, 0, pier_h), rotation=(0, math.pi / 2, 0))
    body = boolean_cut(body, bpy.context.active_object)
    bpy.ops.mesh.primitive_cube_add(size=1, location=(0, 0, pier_h / 2 - 0.01))
    c = bpy.context.active_object
    c.scale = (depth + 2, r * 2, pier_h)
    bpy.ops.object.transform_apply(scale=True)
    body = boolean_cut(body, c)
    top = pier_h + r + 1.2
    parts = [body, box("impost", depth + 0.4, 0.9, 0.4, (0, -span / 2 + 0.45, pier_h - 0.4), STONE_L), box("impost2", depth + 0.4, 0.9, 0.4, (0, span / 2 - 0.45, pier_h - 0.4), STONE_L),
             box("cornice", depth + 0.6, span, 0.5, (0, 0, top), STONE_L), box("channel", depth - 0.6, span, 1.8, (0, 0, top + 0.5), STONE_D),
             box("water", depth - 1.4, span, 0.1, (0, 0, top + 2.25), "#65888A"), box("cap", depth - 0.2, span, 0.3, (0, 0, top + 2.3), STONE)]
    m.add("base", parts)
    return m


def wall_bay():
    """A 6 m bay of city wall: battered base, curtain, wall-walk and merlons. Long axis +Y."""
    m = Prop("prop-wall-bay")
    L, T, H = 6.0, 3.4, 9.0
    parts = [box("plinth", T + 0.8, L, 1.2, (0, 0, 0), STONE_D), box("curtain", T, L, H, (0, 0, 0), STONE), box("walk", T - 1.0, L, 0.2, (0, 0, H), STONE_D),
             box("string", T + 0.25, L, 0.3, (0, 0, H - 0.3), STONE_L)]
    for k in range(3):
        parts.append(box(f"merlon{k}", 0.8, 1.1, 1.4, (T / 2 - 0.4, -L / 2 + 1.0 + k * 2.0, H), STONE_L))
    for k in range(2):
        parts.append(box(f"slit{k}", 0.1, 0.3, 1.2, (T / 2 + 0.01, -L / 4 + k * L / 2, 4.5), "#3A2A1E"))
    m.add("base", parts)
    return m


def wall_tower():
    """A square projecting tower with crenellations and arrow slits."""
    m = Prop("prop-wall-tower")
    W, H = 7.5, 14.0
    parts = [box("plinth", W + 0.8, W + 0.8, 1.2, (1.2, 0, 0), STONE_D), box("body", W, W, H, (1.2, 0, 0), STONE_D), box("string", W + 0.3, W + 0.3, 0.3, (1.2, 0, H - 0.3), STONE_L),
             box("roof", W - 1.0, W - 1.0, 0.2, (1.2, 0, H), STONE)]
    for side in range(4):
        for k in range(3):
            a = side * math.pi / 2
            off = -W / 2 + 1.3 + k * 2.45
            x, y = (W / 2 - 0.4) * math.cos(a) - off * math.sin(a), (W / 2 - 0.4) * math.sin(a) + off * math.cos(a)
            parts.append(box(f"m{side}{k}", 1.0 if side % 2 == 0 else 1.1, 1.1 if side % 2 == 0 else 1.0, 1.5, (1.2 + x, y, H), STONE_L))
    for z in (5.0, 9.5):
        for s in (-1, 1):
            parts.append(box(f"slit{z}{s}", 0.1, 0.3, 1.3, (1.2 + W / 2 + 0.01, s * 1.6, z), "#3A2A1E"))
    m.add("base", parts)
    return m


def gatehouse():
    """A double-arched gate between two round towers (Aurelian type)."""
    m = Prop("prop-gatehouse")
    W, T, H = 16.0, 8.0, 13.0
    body = box("body", T, W, H, (0, 0, 0), STONE)
    for s in (-1, 1):
        bpy.ops.mesh.primitive_cylinder_add(vertices=16, radius=2.0, depth=T + 2, location=(0, s * 2.8, 5.0), rotation=(0, math.pi / 2, 0))
        body = boolean_cut(body, bpy.context.active_object)
        bpy.ops.mesh.primitive_cube_add(size=1, location=(0, s * 2.8, 2.5))
        c = bpy.context.active_object
        c.scale = (T + 2, 4.0, 5.0)
        bpy.ops.object.transform_apply(scale=True)
        body = boolean_cut(body, c)
    parts = [body, box("attic", T - 1, W - 2, 3.0, (0, 0, H), STONE_L)]
    for k in range(6):
        parts.append(box(f"win{k}", 0.1, 1.0, 1.4, (T / 2 + 0.01, -5 + k * 2, H + 0.7), "#3A2A1E"))
    for s in (-1, 1):
        parts.append(cylinder(f"tower{s}", 5.0, H + 5, (1.0, s * (W / 2 + 3.5), 0), STONE_D, verts=16))
        for k in range(10):
            a = math.tau * k / 10
            parts.append(box(f"tm{s}{k}", 1.0, 1.0, 1.4, (1.0 + 4.6 * math.cos(a), s * (W / 2 + 3.5) + 4.6 * math.sin(a), H + 5), STONE_L))
    m.add("base", parts)
    return m


BUILDERS.update({"props/aqueduct-bay": aqueduct_bay, "props/wall-bay": wall_bay, "props/wall-tower": wall_tower, "props/gatehouse": gatehouse})


# ---------------------------------------------------------------- bridges (spans laid across the river)

def bridge_arch():
    """One stone span of a Roman bridge: an arch between two half piers with cutwaters, deck and parapets.
    20 m along +Y (the crossing), 9 m wide, origin at the waterline centre."""
    m = Prop("prop-bridge-arch")
    span, width, spring, r = 20.0, 9.0, 4.0, 7.2
    body = box("body", width, span, spring + r + 1.6, (0, 0, 0), STONE)
    bpy.ops.mesh.primitive_cylinder_add(vertices=28, radius=r, depth=width + 2, location=(0, 0, spring), rotation=(0, math.pi / 2, 0))
    body = boolean_cut(body, bpy.context.active_object)
    bpy.ops.mesh.primitive_cube_add(size=1, location=(0, 0, spring / 2 - 0.01))
    c = bpy.context.active_object
    c.scale = (width + 2, r * 2, spring)
    bpy.ops.object.transform_apply(scale=True)
    body = boolean_cut(body, c)
    deck = spring + r + 1.6
    parts = [body]
    # voussoir ring and keystone picked out in lighter stone
    for k in range(13):
        a = math.pi * k / 12
        parts.append(box(f"vous{k}", width + 0.25, 0.55, 0.9, (0, -math.cos(a) * (r + 0.2), spring + math.sin(a) * (r + 0.2) - 0.45), STONE_L if k % 2 else STONE))
    # cutwaters: pointed prows on the piers, upstream and downstream
    for sy in (-1, 1):
        for sx in (-1, 1):
            # a square prism turned 45 degrees: its point splits the current
            parts.append(cylinder(f"cut{sx}{sy}", 1.9, spring + 1.2, (sx * (width / 2), sy * span / 2, 0), STONE_D, verts=4))
    parts += [box("deck", width + 0.3, span, 0.35, (0, 0, deck - 0.05), STONE_L), box("road", width - 2.2, span, 0.08, (0, 0, deck + 0.3), "#B9A88C")]
    for sx in (-1, 1):
        parts += [box(f"parapet{sx}", 0.6, span, 1.1, (sx * (width / 2 - 0.3), 0, deck + 0.3), STONE),
                  box(f"coping{sx}", 0.75, span, 0.15, (sx * (width / 2 - 0.3), 0, deck + 1.4), STONE_L),
                  box(f"string{sx}", 0.2, span, 0.3, (sx * (width / 2 + 0.1), 0, deck - 0.6), STONE_L)]
    m.add("base", parts)
    return m


def bridge_timber():
    """One timber bay of a pile bridge (the Pons Sublicius type): pile bents, bracing, plank deck and rails. 12 m along +Y."""
    m = Prop("prop-bridge-timber")
    span, width, deck = 12.0, 7.0, 7.5
    T, TD = "#8A6A4A", "#6E5238"
    parts = []
    for sy in (-1, 1):
        y = sy * (span / 2 - 0.3)
        for k in range(4):
            x = -width / 2 + 0.6 + k * (width - 1.2) / 3
            parts.append(cylinder(f"pile{sy}{k}", 0.28, deck, (x, y, 0), TD, verts=8))
        parts.append(box(f"cap{sy}", width + 0.6, 0.6, 0.5, (0, y, deck - 0.5), T))
        brace = box(f"brace{sy}", 0.2, 0.2, deck * 1.15, (0, y, 0.6), TD)
        brace.rotation_euler[1] = 0.62
        parts.append(brace)
    for k in range(5):
        parts.append(box(f"stringer{k}", 0.4, span, 0.5, (-width / 2 + 0.7 + k * (width - 1.4) / 4, 0, deck), T))
    for k in range(int(span / 0.6)):
        parts.append(box(f"plank{k}", width, 0.55, 0.12, (0, -span / 2 + 0.3 + k * 0.6, deck + 0.5), "#A0805C" if k % 2 else "#94765A"))
    for sx in (-1, 1):
        for k in range(5):
            parts.append(box(f"post{sx}{k}", 0.18, 0.18, 1.2, (sx * (width / 2 - 0.2), -span / 2 + 0.5 + k * (span - 1.0) / 4, deck + 0.6), TD))
        parts.append(box(f"rail{sx}", 0.16, span, 0.16, (sx * (width / 2 - 0.2), 0, deck + 1.7), T))
    m.add("base", parts)
    return m


# ---------------------------------------------------------------- street life (moved along the streets by the web app)
STOLA, TOGA, TUNIC_R, TUNIC_B, TUNIC_G, TUNIC_O = "#C9B48E", "#EEE8DA", "#9A4E36", "#55687E", "#6E7A58", "#B07A3E"


def walker():
    """A townsman in a belted tunic, mid-stride. Faces -Y, the way it walks."""
    m = Prop("prop-walker")
    p = [cylinder("lleg", 0.09, 0.8, (-0.11, 0.12, 0), "#8F6B4E", verts=6), cylinder("rleg", 0.09, 0.8, (0.11, -0.14, 0), "#8F6B4E", verts=6),
         cylinder("tunic", 0.26, 0.75, (0, 0, 0.62), TUNIC_R, verts=10, r_top=0.2), box("belt", 0.44, 0.38, 0.06, (0, 0, 1.06), "#4A3426"),
         cylinder("chest", 0.2, 0.3, (0, 0, 1.12), TUNIC_R, verts=10, r_top=0.17),
         cylinder("larm", 0.06, 0.55, (-0.27, -0.08, 0.85), SKIN, verts=6), cylinder("rarm", 0.06, 0.55, (0.27, 0.08, 0.85), SKIN, verts=6),
         dome("head", 0.13, (0, 0, 1.48), SKIN, squash=1.5, segments=10, rings=6), dome("hair", 0.135, (0, 0.02, 1.56), "#3A2A1E", squash=0.7, segments=10, rings=4)]
    m.add("base", p)
    return m


def matron():
    """A woman in a long stola with a palla over the head, carrying a basket."""
    m = Prop("prop-matron")
    p = [cylinder("stola", 0.3, 1.25, (0, 0, 0), STOLA, verts=12, r_top=0.19), cylinder("palla", 0.22, 0.32, (0, 0, 1.22), "#7D5A6B", verts=10, r_top=0.15),
         dome("head", 0.12, (0, 0, 1.52), SKIN, squash=1.5, segments=10, rings=6), dome("veil", 0.14, (0, 0.03, 1.58), "#7D5A6B", squash=0.9, segments=10, rings=5),
         cylinder("arm", 0.06, 0.5, (0.27, 0, 0.75), "#7D5A6B", verts=6), cylinder("basket", 0.2, 0.22, (0.38, -0.05, 0.62), STRAW, verts=10, r_top=0.24),
         dome("fruit", 0.16, (0.38, -0.05, 0.84), "#A6493A", squash=0.5, segments=8, rings=4)]
    m.add("base", p)
    return m


def porter():
    """A porter bent under an amphora on his shoulder."""
    m = Prop("prop-porter")
    p = [cylinder("lleg", 0.1, 0.78, (-0.12, 0.15, 0), "#8F6B4E", verts=6), cylinder("rleg", 0.1, 0.78, (0.12, -0.12, 0), "#8F6B4E", verts=6),
         cylinder("tunic", 0.27, 0.7, (0, 0, 0.6), TUNIC_O, verts=10, r_top=0.22), cylinder("chest", 0.22, 0.3, (0, -0.05, 1.08), TUNIC_O, verts=10, r_top=0.18),
         dome("head", 0.13, (0, -0.12, 1.42), SKIN, squash=1.5, segments=10, rings=6)]
    amph = cylinder("amphora", 0.2, 1.0, (0, 0, 0), "#B5654A", verts=10, r_top=0.06)
    amph.rotation_euler = (0.5, 0, 0)
    amph.location = (0.22, 0.25, 1.25)
    p += [amph, cylinder("arm", 0.06, 0.6, (0.28, 0, 1.05), SKIN, verts=6)]
    m.add("base", p)
    return m


def mule():
    """A pack mule with panniers, led by its driver on a rope. Faces -Y."""
    m = Prop("prop-mule")
    body = "#7B6650"
    p = [box("body", 0.55, 1.5, 0.6, (0, 0.2, 0.75), body), box("neck", 0.3, 0.5, 0.45, (0, -0.65, 1.15), body), box("head", 0.26, 0.55, 0.3, (0, -1.0, 1.35), shade(body, -0.1)),
         box("ear_l", 0.06, 0.08, 0.25, (-0.08, -0.85, 1.65), body), box("ear_r", 0.06, 0.08, 0.25, (0.08, -0.85, 1.65), body)]
    for sx in (-0.18, 0.18):
        for sy in (-0.4, 0.75):
            p.append(box(f"leg{sx}{sy}", 0.12, 0.12, 0.78, (sx, sy, 0), shade(body, -0.2)))
    for sx in (-1, 1):
        p.append(box(f"pannier{sx}", 0.35, 0.8, 0.55, (sx * 0.45, 0.2, 0.75), STRAW))
    p += [box("load", 0.6, 0.7, 0.35, (0, 0.2, 1.35), "#C9B79A")]
    drv = [cylinder("d_legs", 0.15, 0.78, (0.7, -1.5, 0), "#8F6B4E", verts=6, r_top=0.17), cylinder("d_body", 0.24, 0.65, (0.7, -1.5, 0.78), TUNIC_B, verts=10, r_top=0.18),
           dome("d_head", 0.13, (0.7, -1.5, 1.55), SKIN, squash=1.5, segments=10, rings=6), dome("d_hat", 0.2, (0.7, -1.5, 1.62), STRAW, squash=0.35, segments=10, rings=4),
           box("rope", 0.04, 0.7, 0.04, (0.35, -1.25, 1.2), "#5A4632")]
    m.add("base", p + drv)
    return m


def litter():
    """A covered litter (lectica) carried by four bearers, a rich passenger behind the curtains."""
    m = Prop("prop-litter")
    p = [box("cabin", 0.9, 2.0, 0.9, (0, 0, 1.15), "#7A2E2A"), box("roof", 1.1, 2.2, 0.12, (0, 0, 2.05), "#C9A24A"),
         box("curtain_l", 0.04, 1.6, 0.6, (-0.47, 0, 1.3), "#E6DCC8"), box("curtain_r", 0.04, 1.6, 0.6, (0.47, 0, 1.3), "#E6DCC8")]
    for sx in (-1, 1):
        p.append(box(f"pole{sx}", 0.1, 4.4, 0.1, (sx * 0.62, 0, 1.25), WOOD))
    for i, (sx, sy) in enumerate([(-1, -1), (1, -1), (-1, 1), (1, 1)]):
        x, y = sx * 0.75, sy * 1.85
        p += [cylinder(f"b{i}_legs", 0.15, 0.8, (x, y, 0), "#8F6B4E", verts=6, r_top=0.17), cylinder(f"b{i}_body", 0.24, 0.55, (x, y, 0.8), TUNIC_R if i % 2 else TUNIC_B, verts=10, r_top=0.19),
              dome(f"b{i}_head", 0.13, (x, y, 1.48), "#8A5E40", squash=1.5, segments=10, rings=6)]
    m.add("base", p)
    return m


def handcart():
    """A two-wheeled handcart of produce pushed by a market gardener."""
    m = Prop("prop-handcart")
    p = [box("bed", 1.1, 1.5, 0.2, (0, 0, 0.6), WOOD), box("side_l", 0.08, 1.5, 0.35, (-0.55, 0, 0.8), WOOD), box("side_r", 0.08, 1.5, 0.35, (0.55, 0, 0.8), WOOD),
         wheel("wl", 0.5, (-0.65, 0.1, 0.5)), wheel("wr", 0.5, (0.65, 0.1, 0.5)), box("handles", 0.9, 1.2, 0.06, (0, 1.3, 0.85), WOOD)]
    for i in range(6):
        p.append(dome(f"veg{i}", 0.2, (-0.3 + (i % 3) * 0.3, -0.35 + (i // 3) * 0.6, 0.8), ["#6E7A58", "#C9A24A", "#A6493A"][i % 3], squash=0.8, segments=8, rings=4))
    p += [cylinder("g_legs", 0.15, 0.78, (0, 2.0, 0), "#8F6B4E", verts=6, r_top=0.17), cylinder("g_body", 0.24, 0.62, (0, 2.0, 0.78), TUNIC_G, verts=10, r_top=0.18),
          dome("g_head", 0.13, (0, 2.0, 1.52), SKIN, squash=1.5, segments=10, rings=6)]
    m.add("base", p)
    return m


def _stall(name, awning, goods):
    """A street stall under an awning with its vendor. Counter faces -Y (the street)."""
    m = Prop(name)
    p = [box("counter", 2.4, 0.9, 0.95, (0, 0, 0), WOOD), box("top", 2.6, 1.05, 0.07, (0, 0, 0.95), shade(WOOD, 0.25))]
    for sx in (-1.2, 1.2):
        for sy in (-0.45, 1.3):
            p.append(box(f"post{sx}{sy}", 0.09, 0.09, 2.3 if sy < 0 else 2.6, (sx, sy, 0), WOOD))
    aw = box("awning", 2.8, 2.2, 0.05, (0, 0.42, 2.38), awning)
    aw.rotation_euler[0] = -0.16
    p.append(aw)
    for k in range(7):
        p.append(box(f"stripe{k}", 0.18, 2.2, 0.052, (-1.2 + k * 0.4, 0.42, 2.385), shade(awning, 0.35)) if k % 2 == 0 else box(f"s{k}", 0.01, 0.01, 0.01, (0, 0, 0), awning))
    p += goods
    p += [cylinder("v_body", 0.25, 1.0, (0.3, 0.95, 0), TUNIC_B, verts=10, r_top=0.18), dome("v_head", 0.13, (0.3, 0.95, 1.12), SKIN, squash=1.5, segments=10, rings=6)]
    m.add("base", p)
    return m


def stall_fruit():
    goods = [dome(f"f{i}", 0.17, (-0.95 + (i % 6) * 0.38, -0.15 + (i // 6) * 0.32, 1.0), ["#A6493A", "#C9A24A", "#6E7A58"][i % 3], squash=0.8, segments=8, rings=4) for i in range(12)]
    goods += [cylinder(f"bk{i}", 0.28, 0.4, (-0.9 + i * 0.9, -0.85, 0), STRAW, verts=10, r_top=0.32) for i in range(3)]
    return _stall("prop-stall-fruit", "#B5654A", goods)


def stall_pots():
    goods = [cylinder(f"pot{i}", 0.16 + 0.04 * (i % 2), 0.35 + 0.1 * (i % 3), (-0.95 + (i % 6) * 0.38, -0.1 + (i // 6) * 0.35, 1.0), "#B5654A" if i % 3 else "#8E5A3C", verts=10, r_top=0.08) for i in range(10)]
    goods += [cylinder(f"amph{i}", 0.22, 1.0, (-1.0 + i * 0.45, -0.95, 0), "#B5654A", verts=10, r_top=0.07) for i in range(5)]
    return _stall("prop-stall-pots", "#6E7A58", goods)


def stall_cloth():
    goods = [box(f"bolt{i}", 0.5, 0.35, 0.18, (-0.85 + (i % 4) * 0.56, -0.1 + (i // 4) * 0.4, 1.0 + 0.18 * (i // 8)), ["#7D5A6B", "#55687E", "#C9A24A", "#9A4E36"][i % 4]) for i in range(8)]
    goods += [box(f"hang{i}", 0.5, 0.04, 1.1, (-0.9 + i * 0.6, -0.45, 1.15), ["#9A4E36", "#55687E", "#C9A24A", "#7D5A6B"][i % 4]) for i in range(4)]
    return _stall("prop-stall-cloth", "#55687E", goods)


BUILDERS.update({
    "props/bridge-arch": bridge_arch, "props/bridge-timber": bridge_timber,
    "props/walker": walker, "props/matron": matron, "props/porter": porter, "props/mule": mule, "props/litter": litter, "props/handcart": handcart,
    "props/stall-fruit": stall_fruit, "props/stall-pots": stall_pots, "props/stall-cloth": stall_cloth,
})
