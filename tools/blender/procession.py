"""
The title page's procession: one cartoon traveller for each atlas on the shelf,
modelled here and rendered as an 8-frame walk-cycle sprite sheet (Workbench,
flat two-tone shading with ink outlines), 3/4 view, walking right.

    exec(open(".../procession.py").read()); render_all()

Output: assets/title/procession/<id>.webp and manifest.json.
"""
import json, math, os, sys
import bpy
import numpy as np

ROOT = "/Users/ijlalahmad/Desktop/test/Chronoscape"
for p in (os.path.join(ROOT, "tools", "blender"), os.path.join(ROOT, "tools", "blender", "models")):
    if p not in sys.path:
        sys.path.insert(0, p)
import importlib, chronokit
importlib.reload(chronokit)
from chronokit import box, cylinder, join, reset_scene, _finish

OUT = os.path.join(ROOT, "assets", "title", "procession")
FRAMES = 8
PPM = 130          # render pixels per metre (displayed at half)
SKIN, SKIN_D = "#e8b48a", "#b97a52"
INK = "#2b1a10"


def part(name, objs, pivot):
    """Join objects into one part whose origin is the pivot (so it can swing)."""
    o = join([x for x in objs if x], name)
    bpy.context.scene.cursor.location = pivot
    bpy.ops.object.select_all(action="DESELECT")
    o.select_set(True)
    bpy.context.view_layer.objects.active = o
    bpy.ops.object.origin_set(type="ORIGIN_CURSOR")
    bpy.ops.object.shade_smooth()
    return o


def ball(name, r, at, color, squash=1.0):
    """A whole (smooth) sphere, squashed vertically if asked."""
    bpy.ops.mesh.primitive_uv_sphere_add(segments=24, ring_count=14, radius=r, location=at)
    o = bpy.context.active_object
    o.scale = (1, 1, squash)
    bpy.ops.object.transform_apply(scale=True)
    return _finish(o, name, color)


def tilted(o, rot, loc):
    """Rotate and move an object and bake it into the mesh (so joining keeps the pose)."""
    o.rotation_euler = rot
    o.location = loc
    bpy.ops.object.select_all(action="DESELECT")
    o.select_set(True)
    bpy.context.view_layer.objects.active = o
    bpy.ops.object.transform_apply(location=True, rotation=True, scale=True)
    return o


class Walker:
    """A chunky cartoon person facing +X: big head, short legs, swinging arms."""

    def __init__(self, skin=SKIN, tunic="#a65238", legs="#6b4a32", shoes="#4a3322", robe=None, robe_len=0.62, sleeves=None, belt=None, hold=None):
        self.parts = {}
        self.statics = []
        hip = 0.62
        self.hip = hip
        # legs (pivot at the hip)
        for s, side in ((1, "l"), (-1, "r")):
            leg = [cylinder(f"leg{side}", 0.08, hip - 0.06, (0, s * 0.1, 0.06), legs, verts=10), box(f"foot{side}", 0.24, 0.13, 0.08, (0.05, s * 0.1, 0), shoes)]
            self.parts[f"leg{side}"] = part(f"leg_{side}", leg, (0, s * 0.1, hip))
        # torso, or a long robe over the legs
        torso = [cylinder("torso", 0.21, 0.5, (0, 0, hip - 0.02), tunic, verts=16, r_top=0.17)]
        if robe:
            torso.append(cylinder("robe", 0.3, robe_len, (0, 0, max(0.1, hip - robe_len + 0.12)), robe, verts=18, r_top=0.2))
        if belt:
            torso.append(cylinder("belt", 0.205, 0.07, (0, 0, hip + 0.06), belt, verts=16))
        self.statics.append(part("torso", torso, (0, 0, hip)))
        # head with eyes and cheeks, looking right
        head = [ball("head", 0.3, (0.02, 0, 1.4), skin), ball("eyew_l", 0.06, (0.27, 0.11, 1.44), "#fbf6ea"), ball("eyew_r", 0.06, (0.27, -0.11, 1.44), "#fbf6ea"),
                ball("eye_l", 0.034, (0.32, 0.11, 1.44), INK), ball("eye_r", 0.034, (0.32, -0.11, 1.44), INK),
                ball("nose", 0.05, (0.32, 0, 1.36), SKIN_D if skin == SKIN else skin), ball("ear", 0.065, (0.0, 0.29, 1.4), skin),
                ball("cheek", 0.05, (0.25, 0.17, 1.33), "#e8907a", 0.6)]
        self.statics.append(part("head", head, (0, 0, 1.15)))
        # arms (pivot at the shoulder)
        sl = sleeves or tunic
        for s, side in ((1, "l"), (-1, "r")):
            arm = [cylinder(f"arm{side}", 0.065, 0.42, (0, s * 0.25, 0.68), sl, verts=10), ball(f"hand{side}", 0.075, (0, s * 0.25, 0.66), skin)]
            self.parts[f"arm{side}"] = part(f"arm_{side}", arm, (0, s * 0.25, 1.08))
        self.hold = hold  # "l"/"r": that arm holds something and doesn't swing

    def attach(self, where, objs, at=None):
        """Add objects to a part (moving with it) or to the body ("body")."""
        objs = [o for o in (objs if isinstance(objs, list) else [objs]) if o]
        if where == "body":
            self.statics.append(part(f"acc{len(self.statics)}", objs, (0, 0, 0)))
            return
        p = self.parts[where]
        acc = part(f"acc_{where}{len(objs)}", objs, tuple(p.location))
        acc.parent = p
        acc.matrix_parent_inverse = p.matrix_world.inverted()

    def pose(self, phase):
        a = math.sin(phase)
        self.parts["legl"].rotation_euler = (0, a * 0.55, 0)
        self.parts["legr"].rotation_euler = (0, -a * 0.55, 0)
        for side, sign in (("l", -1), ("r", 1)):
            arm = self.parts[f"arm{side}"]
            arm.rotation_euler = (0, -0.5, 0) if self.hold == side else (0, sign * a * 0.6, 0)
        bob = abs(math.cos(phase)) * 0.035
        for o in self.statics + [self.parts[k] for k in self.parts]:
            o["z0"] = o.get("z0", o.location.z)
            o.location.z = o["z0"] + bob


# ---------------------------------------------------------------- the travellers

def scribe():
    w = Walker(tunic=SKIN, legs=SKIN, shoes="#c9a24a", robe="#f4efe2", robe_len=0.5, sleeves=SKIN, belt="#c9a24a", hold="l")
    w.attach("body", [ball("wig", 0.3, (-0.03, 0, 1.43), "#1e1a18", 1.05), box("collar", 0.05, 0.42, 0.12, (0.15, 0, 1.0), "#3c8c8c")])
    w.attach("arml", [cylinder("scroll", 0.05, 0.36, (0.12, 0.25, 0.52), "#efe2b8", verts=10)])
    return w


def legionary():
    w = Walker(tunic="#b23a2e", legs=SKIN, shoes="#6b4a32", robe="#b23a2e", robe_len=0.34, sleeves="#b23a2e", hold="r")
    w.attach("body", [cylinder("armour", 0.23, 0.36, (0, 0, 0.74), "#9aa0a6", verts=16, r_top=0.2), cylinder("band1", 0.235, 0.05, (0, 0, 0.82), "#c9a24a", verts=16),
                      ball("helmet", 0.33, (-0.03, 0, 1.52), "#c9a24a", 0.72), cylinder("brim", 0.35, 0.04, (-0.03, 0, 1.47), "#b08a3a", verts=20),
                      ball("crest", 0.16, (-0.06, 0, 1.78), "#c0392b", 1.0), box("crest_b", 0.36, 0.08, 0.14, (-0.06, 0, 1.72), "#c0392b")])
    w.attach("arml", [box("shield", 0.07, 0.42, 0.62, (0.12, 0.42, 0.42), "#b23a2e"), ball("boss", 0.07, (0.17, 0.42, 0.73), "#c9a24a")])
    w.attach("armr", [cylinder("spear", 0.025, 2.0, (0.1, -0.25, 0.1), "#7a5634", verts=8), cylinder("spearhead", 0.045, 0.2, (0.1, -0.25, 2.1), "#c9ccd0", verts=8, r_top=0.0)])
    return w


def monk():
    w = Walker(tunic="#e08a2c", legs=SKIN, shoes="#7a5634", robe="#e08a2c", robe_len=0.6, sleeves="#e08a2c", hold="r")
    w.attach("body", [ball("scalp", 0.282, (0.02, 0, 1.4), SKIN_D, 1.0), box("drape", 0.36, 0.08, 0.6, (0, 0.12, 0.62), "#c9701e")])
    w.attach("armr", [cylinder("staff", 0.03, 1.9, (0.12, -0.25, 0.0), "#7a5634", verts=8), ball("finial", 0.08, (0.12, -0.25, 1.92), "#c9a24a")])
    w.attach("arml", [cylinder("bowl", 0.11, 0.08, (0.08, 0.25, 0.58), "#4a3322", verts=14, r_top=0.14)])
    return w


def merchant_camel():
    w = Walker(tunic="#3f6f9a", legs="#efe2c8", shoes="#7a5634", robe="#3f6f9a", robe_len=0.5, sleeves="#3f6f9a", belt="#e0b04a", hold="l")
    w.attach("body", [ball("turban", 0.3, (0.0, 0, 1.55), "#f1e6cc", 0.7), ball("beard", 0.13, (0.22, 0, 1.25), "#3c2a1e")])
    w.attach("arml", [cylinder("rope", 0.015, 0.9, (-0.3, 0.25, 0.65), "#5a3e24", verts=6)])
    # the camel behind him, walking with its legs in pairs
    C = "#c89a5e"
    cx = -1.55
    body = [ball("cbody", 0.62, (cx, 0, 1.45), C, 0.6), ball("hump", 0.4, (cx - 0.05, 0, 1.78), C, 0.9), box("rug", 0.7, 0.86, 0.06, (cx - 0.05, 0, 1.7), "#b23a2e"),
            box("bag1", 0.35, 0.18, 0.4, (cx - 0.3, 0.42, 1.25), "#e0b04a"), box("bag2", 0.35, 0.18, 0.4, (cx - 0.3, -0.42, 1.25), "#e0b04a"),
            ball("tail", 0.08, (cx - 0.65, 0, 1.4), "#8a6a40")]
    # the neck leans forward from the chest; cylinders pivot on their centre, so place the centre half way up
    lean, L = 0.65, 0.85
    bx, bz = cx + 0.4, 1.45
    neck = tilted(cylinder("cneck", 0.14, L, (0, 0, -L / 2), C, verts=12), (0, lean, 0), (bx + L / 2 * math.sin(lean), 0, bz + L / 2 * math.cos(lean)))
    hx, hz = bx + L * math.sin(lean), bz + L * math.cos(lean)
    head = [neck, ball("chead", 0.21, (hx + 0.05, 0, hz), C, 0.85), ball("snout", 0.14, (hx + 0.25, 0, hz - 0.05), "#b0864e", 0.9), ball("ceye", 0.04, (hx + 0.15, 0.15, hz + 0.06), INK),
            ball("cear", 0.06, (hx - 0.08, 0.12, hz + 0.16), C)]
    w.attach("body", body + head)
    w.camel = []
    for k, (dx, s) in enumerate([(0.38, 1), (0.38, -1), (-0.42, 1), (-0.42, -1)]):
        leg = [cylinder(f"cl{k}", 0.08, 1.05, (cx + dx, s * 0.2, 0.08), "#b08a56", verts=10), box(f"chf{k}", 0.2, 0.18, 0.08, (cx + dx, s * 0.2, 0), "#6b4a32")]
        w.camel.append(part(f"camel_leg{k}", leg, (cx + dx, s * 0.2, 1.13)))
    base = w.pose

    def pose(phase):
        base(phase)
        a = math.sin(phase + 1.0)
        for k, leg in enumerate(w.camel):
            leg.rotation_euler = (0, (a if k in (0, 3) else -a) * 0.35, 0)
    w.pose = pose
    return w


def tang_official():
    w = Walker(tunic="#b8322b", legs="#3a2a22", shoes="#1e1a18", robe="#b8322b", robe_len=0.62, sleeves="#b8322b", belt="#e0b04a", hold="l")
    w.attach("body", [cylinder("cap", 0.22, 0.24, (-0.02, 0, 1.55), "#1e1a18", verts=16, r_top=0.18), box("wings", 0.08, 0.95, 0.06, (-0.12, 0, 1.68), "#1e1a18")])
    w.attach("arml", [box("tablet", 0.05, 0.1, 0.42, (0.16, 0.25, 0.52), "#f1e6cc")])
    return w


def baghdad_scholar():
    w = Walker(tunic="#2f7f6a", legs="#efe2c8", shoes="#e0b04a", robe="#2f7f6a", robe_len=0.62, sleeves="#f1e6cc", belt="#c9a24a", hold="l")
    w.attach("body", [ball("turban", 0.31, (0.0, 0, 1.56), "#f4efe2", 0.72), ball("beard", 0.15, (0.2, 0, 1.24), "#5a4232"), box("mantle", 0.3, 0.5, 0.5, (-0.1, 0, 0.62), "#1f5e4e")])
    astro = tilted(cylinder("astrolabe", 0.16, 0.03, (0, 0, 0), "#c9a24a", verts=24), (math.pi / 2, 0, 0), (0.2, 0.3, 0.6))
    w.attach("arml", [astro, box("books", 0.22, 0.12, 0.28, (0.05, 0.36, 0.42), "#7a2f22")])
    return w


def knight():
    w = Walker(tunic="#f1ece0", legs="#8f959b", shoes="#6b7076", robe="#f1ece0", robe_len=0.42, sleeves="#8f959b", belt="#4a3322", hold="l")
    w.attach("body", [box("cross_v", 0.02, 0.1, 0.42, (0.21, 0, 0.66), "#c0392b"), box("cross_h", 0.02, 0.3, 0.1, (0.21, 0, 0.84), "#c0392b"),
                      cylinder("helm", 0.3, 0.42, (0.02, 0, 1.18), "#a7adb3", verts=18), box("visor", 0.04, 0.4, 0.04, (0.31, 0, 1.42), INK),
                      ball("helmtop", 0.3, (0.02, 0, 1.6), "#a7adb3", 0.4)])
    sh = box("kshield", 0.07, 0.42, 0.55, (0.14, 0.42, 0.42), "#f1ece0")
    w.attach("arml", [sh, box("kcross_v", 0.02, 0.08, 0.45, (0.18, 0.42, 0.47), "#c0392b"), box("kcross_h", 0.02, 0.32, 0.08, (0.18, 0.42, 0.72), "#c0392b")])
    w.attach("armr", [cylinder("sword", 0.03, 0.7, (0.08, -0.25, 0.08), "#c9ccd0", verts=8), box("guard", 0.04, 0.22, 0.04, (0.08, -0.25, 0.78), "#c9a24a")])
    return w


def painter():
    w = Walker(tunic="#6d3a7a", legs="#c8a24a", shoes="#4a3322", sleeves="#e7c86a", belt="#4a3322", hold="l")
    w.attach("body", [cylinder("beret", 0.3, 0.1, (-0.02, 0, 1.6), "#2c2c3c", verts=18, r_top=0.33), ball("hair", 0.29, (-0.06, 0, 1.36), "#5a3a24"),
                      cylinder("collar", 0.17, 0.06, (0, 0, 1.1), "#f4efe2", verts=16)])
    w.attach("arml", [box("canvas", 0.05, 0.6, 0.48, (0.14, 0.42, 0.62), "#f4efe2"), box("frame", 0.04, 0.66, 0.54, (0.12, 0.42, 0.59), "#9a6a3a"),
                      ball("dab1", 0.06, (0.17, 0.32, 0.86), "#c0392b"), ball("dab2", 0.06, (0.17, 0.5, 0.78), "#3f6f9a")])
    w.attach("armr", [cylinder("brush", 0.015, 0.4, (0.14, -0.25, 0.6), "#7a5634", verts=6), ball("tip", 0.03, (0.14, -0.25, 1.0), "#c0392b")])
    return w


def mughal_courtier():
    w = Walker(tunic="#f4efe2", legs="#c0392b", shoes="#e0b04a", robe="#f4efe2", robe_len=0.6, sleeves="#f4efe2", belt="#e08a2c", hold="r")
    w.attach("body", [ball("pagri", 0.31, (0.0, 0, 1.55), "#c0392b", 0.75), ball("jewel", 0.05, (0.27, 0, 1.62), "#3f9a6a"), cylinder("plume", 0.02, 0.3, (0.18, 0, 1.68), "#f4efe2", verts=6),
                      ball("mustache", 0.08, (0.27, 0, 1.3), "#2c2018", 0.5), cylinder("sash", 0.22, 0.1, (0, 0, 0.66), "#e08a2c", verts=16)])
    w.attach("armr", [ball("rose", 0.07, (0.15, -0.28, 0.62), "#d24a6a")])
    return w


def samurai():
    w = Walker(tunic="#2c3e6b", legs="#1e2a44", shoes="#c9b48e", robe="#3f4f7a", robe_len=0.55, sleeves="#2c3e6b", belt="#e9d4a6", hold="l")
    w.attach("body", [ball("hair", 0.29, (-0.05, 0, 1.4), "#141218"), cylinder("topknot", 0.05, 0.22, (-0.05, 0, 1.63), "#141218", verts=8),
                      box("katana", 0.9, 0.05, 0.05, (-0.12, 0.24, 0.7), "#1e1a18"), box("wakizashi", 0.6, 0.05, 0.05, (-0.02, 0.27, 0.66), "#7a2f22")])
    return w


def timbuktu_trader():
    w = Walker(skin="#8a5a3a", tunic="#2a3a7a", legs="#8a5a3a", shoes="#c9a24a", robe="#2a3a7a", robe_len=0.62, sleeves="#2a3a7a", hold="r")
    w.attach("body", [ball("tagelmust", 0.31, (0.0, 0, 1.5), "#1f2a5a", 0.85), box("veil", 0.06, 0.4, 0.14, (0.25, 0, 1.3), "#1f2a5a")])
    slab = box("salt", 0.5, 0.14, 0.3, (0.0, -0.3, 1.5), "#f4f1ea")
    w.attach("armr", [slab])
    return w


def chasqui():
    w = Walker(skin="#b5764e", tunic="#c0392b", legs="#b5764e", shoes="#7a5634", sleeves="#b5764e", belt="#e0b04a", hold="l")
    w.attach("body", [ball("hair", 0.29, (-0.05, 0, 1.4), "#141218"), cylinder("headband", 0.29, 0.06, (0.0, 0, 1.47), "#e0b04a", verts=18),
                      box("check1", 0.02, 0.12, 0.12, (0.21, 0.07, 0.86), "#f4efe2"), box("check2", 0.02, 0.12, 0.12, (0.21, -0.07, 0.74), "#f4efe2"),
                      box("check3", 0.02, 0.12, 0.12, (0.21, 0.07, 0.62), "#1e1a18")])
    w.attach("arml", [cylinder("conch", 0.08, 0.22, (0.12, 0.25, 0.58), "#f3dcc6", verts=12, r_top=0.02), box("quipu", 0.05, 0.12, 0.3, (0.0, 0.3, 0.36), "#e0b04a")])
    return w


FIGURES = [
    ("scribe", "A scribe of Thebes", "Egypt, 1250 BCE", scribe),
    ("legionary", "A Roman legionary", "Rome, 100 CE", legionary),
    ("monk", "A monk on pilgrimage", "India, 250 BCE", monk),
    ("merchant", "A Silk Road merchant", "Samarkand, 1400", merchant_camel),
    ("official", "A Tang official", "Chang'an, 750", tang_official),
    ("scholar", "A scholar of the House of Wisdom", "Baghdad, 830", baghdad_scholar),
    ("knight", "A crusader knight", "Europe, 1190", knight),
    ("painter", "A painter's apprentice", "Florence, 1490", painter),
    ("courtier", "A Mughal courtier", "Delhi, 1660", mughal_courtier),
    ("samurai", "A samurai", "Edo, 1800", samurai),
    ("trader", "A salt trader", "Timbuktu, 1450", timbuktu_trader),
    ("chasqui", "An Inca runner", "Cusco, 1500", chasqui),
]


def setup_render():
    scene = bpy.context.scene
    try:
        scene.render.engine = "BLENDER_WORKBENCH"
    except TypeError:
        pass
    sh = scene.display.shading
    sh.light = "STUDIO"
    sh.color_type = "MATERIAL"
    sh.show_shadows = True
    scene.display.shadow_shift = 0.35
    scene.display.shadow_focus = 0.0
    sh.shadow_intensity = 0.45
    sh.show_cavity = False
    sh.show_specular_highlight = False
    sh.show_object_outline = True
    sh.object_outline_color = (0.17, 0.1, 0.06)
    scene.display.light_direction = (-0.55, 0.45, 0.7)
    scene.render.film_transparent = True
    scene.render.image_settings.file_format = "PNG"
    scene.render.image_settings.color_mode = "RGBA"
    scene.render.resolution_percentage = 100


PAPER = np.array([0.953, 0.906, 0.792], dtype=np.float32)
INK_RGB = np.array([0.24, 0.16, 0.1], dtype=np.float32)


def engrave(a):
    """Turn a flat-shaded render into a hand-tinted engraving: cream paper tinted faintly with the figure's
    colours, hatching for the half-tones, cross-hatching for the shadows, a firm ink outline."""
    h, w = a.shape[:2]
    rgb, al = a[..., :3], a[..., 3]
    L = np.clip((rgb[..., 0] * 0.3 + rgb[..., 1] * 0.55 + rgb[..., 2] * 0.15) * 1.45, 0, 1)
    # a whisper of colour, as if washed by hand over the print
    grey = L[..., None]
    tint = PAPER * 0.8 + (rgb / np.maximum(grey, 0.05) * PAPER) * 0.2
    tint = np.clip(tint * (0.82 + 0.18 * np.clip(L * 1.6, 0, 1))[..., None], 0, 1)
    yy, xx = np.mgrid[0:h, 0:w]
    d1 = ((xx + yy) % 7) < 1.6
    d2 = ((xx - yy) % 7) < 1.6
    out = tint.copy()
    half = (L < 0.52) & (L >= 0.34)
    dark = (L < 0.34) & (L >= 0.18)
    ink = L < 0.18
    out[half & d1] = INK_RGB * 0.85 + out[half & d1] * 0.15
    out[dark & (d1 | d2)] = INK_RGB
    out[ink] = INK_RGB
    # outline: 2 px of ink wherever the figure meets the background
    solid = al > 0.5
    edge = np.zeros_like(solid)
    for dy in (-2, -1, 0, 1, 2):
        for dx in (-2, -1, 0, 1, 2):
            if dx * dx + dy * dy > 5:
                continue
            edge |= ~np.roll(np.roll(solid, dy, 0), dx, 1)
    edge &= solid
    out[edge] = INK_RGB
    res = np.concatenate([out, al[..., None]], axis=-1)
    res[~solid] = 0
    return res


def render_figure(fid, builder):
    reset_scene()
    setup_render()
    w = builder()
    objs = [o for o in bpy.context.scene.objects if o.type == "MESH"]
    # three-quarter view, walking right
    root = bpy.data.objects.new("root", None)
    bpy.context.scene.collection.objects.link(root)
    for o in objs:
        if o.parent is None:
            o.parent = root
    root.rotation_euler = (0, 0, -0.42)
    bpy.context.view_layer.update()
    # frame: the whole figure across the walk cycle
    xs, zs = [], []
    for i in range(FRAMES):
        w.pose(math.tau * i / FRAMES)
        bpy.context.view_layer.update()
        for o in objs:
            for c in o.bound_box:
                v = o.matrix_world @ __import__("mathutils").Vector(c)
                xs.append(v.x)
                zs.append(v.z)
    x0, x1, z1 = min(xs) - 0.12, max(xs) + 0.12, max(zs) + 0.1
    z0 = -0.06
    W, H = x1 - x0, z1 - z0
    scene = bpy.context.scene
    cam_data = bpy.data.cameras.new("cam")
    cam_data.type = "ORTHO"
    cam_data.ortho_scale = max(W, H)
    cam = bpy.data.objects.new("cam", cam_data)
    scene.collection.objects.link(cam)
    cam.location = ((x0 + x1) / 2, -20, (z0 + z1) / 2 + 0.6)
    cam.rotation_euler = (math.radians(88.3), 0, 0)
    scene.camera = cam
    scene.render.resolution_x = int(round(W * PPM))
    scene.render.resolution_y = int(round(H * PPM))
    # when W != H the ortho scale fits the larger side: keep pixels square by fitting the frame exactly
    cam_data.sensor_fit = "HORIZONTAL" if W >= H else "VERTICAL"
    frames = []
    tmp = os.path.join(bpy.app.tempdir or "/tmp", f"proc_{fid}.png")
    for i in range(FRAMES):
        w.pose(math.tau * i / FRAMES)
        bpy.context.view_layer.update()
        scene.render.filepath = tmp
        bpy.ops.render.render(write_still=True)
        img = bpy.data.images.load(tmp, check_existing=False)
        a = np.array(img.pixels[:], dtype=np.float32).reshape(img.size[1], img.size[0], 4)
        frames.append(engrave(a))
        bpy.data.images.remove(img)
    sheet = np.concatenate(frames, axis=1)
    h, wpx = sheet.shape[0], sheet.shape[1]
    out = bpy.data.images.new(f"sheet_{fid}", wpx, h, alpha=True)
    out.pixels = sheet.ravel()
    os.makedirs(OUT, exist_ok=True)
    path = os.path.join(OUT, f"{fid}.webp")
    out.filepath_raw = path
    out.file_format = "WEBP"
    out.save(quality=86)
    bpy.data.images.remove(out)
    fw = wpx // FRAMES
    return {"src": f"{fid}.webp", "frames": FRAMES, "w": round(fw / 2), "h": round(h / 2)}


def render_all(only=None):
    figs = []
    for fid, label, era, builder in FIGURES:
        if only and fid not in only:
            continue
        r = render_figure(fid, builder)
        figs.append({"id": fid, "label": label, "era": era, **r, "fps": 9})
    if not only:
        json.dump({"figures": figs, "scale": 1.0}, open(os.path.join(OUT, "manifest.json"), "w"), indent=1)
    return figs
