"""
Render a top-down engraved plan of every landmark model, so the drawn map shows
exactly what rises in 3D. Output: assets/models/plans/<city>/<name>.png (sepia,
transparent) and assets/models/plans/manifest.json with each plan's size and
centre in metres (map axes: x east, y south).
"""
import json, math, os, sys, importlib
import bpy
import numpy as np
from mathutils import Vector

ROOT = os.path.abspath(os.path.join(os.path.dirname(os.path.abspath(__file__)), "..", "..")) if "__file__" in globals() else "/Users/ijlalahmad/Desktop/test/Chronoscape"
for p in (os.path.join(ROOT, "tools", "blender"), os.path.join(ROOT, "tools", "blender", "models")):
    if p not in sys.path:
        sys.path.insert(0, p)
import chronokit, archkit, rome, rome_more, rome_fora, delhi, rome_hero, rome_hero2
for _m in (chronokit, archkit, rome, rome_more, rome_fora, delhi, rome_hero, rome_hero2):
    importlib.reload(_m)
BUILDERS = {**rome.BUILDERS, **rome_more.BUILDERS, **rome_fora.BUILDERS, **delhi.BUILDERS, **rome_hero.BUILDERS, **rome_hero2.BUILDERS}
import citymods
importlib.reload(citymods)
BUILDERS.update(citymods.city_builders())

INK = np.array([0x4e, 0x36, 0x25]) / 255.0
PAPER = np.array([0xf2, 0xe7, 0xcc]) / 255.0


def render_plan(key, out_dir):
    chronokit.reset_scene()
    m = BUILDERS[key]()
    m.finish()
    meshes = [o for o in bpy.context.scene.objects if o.type == "MESH"]
    pts = [o.matrix_world @ Vector(c) for o in meshes for c in o.bound_box]
    x0, x1 = min(p.x for p in pts), max(p.x for p in pts)
    y0, y1 = min(p.y for p in pts), max(p.y for p in pts)
    z1 = max(p.z for p in pts)
    cx, cy = (x0 + x1) / 2, (y0 + y1) / 2
    size = max(x1 - x0, y1 - y0) * 1.04
    scene = bpy.context.scene
    cam_data = bpy.data.cameras.new("plan_cam")
    cam_data.type = "ORTHO"
    cam_data.ortho_scale = size
    cam_data.clip_end = z1 + 500
    cam = bpy.data.objects.new("plan_cam", cam_data)
    scene.collection.objects.link(cam)
    cam.location = (cx, cy, z1 + 200)
    cam.rotation_euler = (0, 0, 0)
    scene.camera = cam
    try:
        scene.render.engine = "BLENDER_WORKBENCH"
    except TypeError:
        pass
    sh = scene.display.shading
    sh.light = "STUDIO"
    sh.color_type = "MATERIAL"
    sh.show_shadows = True
    sh.show_cavity = True
    sh.cavity_type = "BOTH"
    sh.show_object_outline = True
    sh.object_outline_color = (0.15, 0.1, 0.06)
    scene.display.shadow_shift = 0.1
    scene.render.film_transparent = True
    px = int(min(1024, max(192, round(size * 3))))
    scene.render.resolution_x = px
    scene.render.resolution_y = px
    scene.render.resolution_percentage = 100
    path = os.path.join(out_dir, key + ".png")
    os.makedirs(os.path.dirname(path), exist_ok=True)
    scene.render.filepath = path
    scene.render.image_settings.file_format = "PNG"
    scene.render.image_settings.color_mode = "RGBA"
    bpy.ops.render.render(write_still=True)
    bpy.data.objects.remove(cam, do_unlink=True)
    bpy.data.cameras.remove(cam_data)
    # sepia: map luminance onto an ink-to-paper ramp, keep alpha
    img = bpy.data.images.load(path, check_existing=False)
    a = np.array(img.pixels[:]).reshape(-1, 4)
    lum = np.clip(a[:, 0] * 0.3 + a[:, 1] * 0.55 + a[:, 2] * 0.15, 0, 1)
    # light surfaces (plazas, marble) go to paper; only shadows, outlines and roofs carry ink
    lum = np.clip((lum - 0.06) / 0.5, 0, 1) ** 0.75
    rgb = INK[None, :] + (PAPER - INK)[None, :] * lum[:, None]
    a[:, :3] = rgb
    img.pixels = a.ravel()
    webp = path[:-4] + ".webp"
    img.filepath_raw = webp
    img.file_format = "WEBP"
    try:
        scene.render.image_settings.quality = 88
    except Exception:
        pass
    img.save()
    bpy.data.images.remove(img)
    os.remove(path)
    # map axes: y points south, Blender y points north
    return {"size": round(size, 2), "cx": round(cx, 2), "cy": round(-cy, 2), "w": round(x1 - x0, 2), "d": round(y1 - y0, 2), "px": px, "ext": "webp"}


def render_all(filter_text=None):
    out_dir = os.path.join(ROOT, "assets", "models", "plans")
    manifest_path = os.path.join(out_dir, "manifest.json")
    manifest = json.load(open(manifest_path)) if os.path.exists(manifest_path) else {}
    for key in BUILDERS:
        if filter_text and filter_text not in key:
            continue
        manifest[key] = render_plan(key, out_dir)
    os.makedirs(out_dir, exist_ok=True)
    with open(manifest_path, "w") as f:
        json.dump(manifest, f, indent=1, sort_keys=True)
    return manifest


if __name__ == "__main__" and "-b" in sys.argv:
    argv = sys.argv[sys.argv.index("--") + 1:] if "--" in sys.argv else []
    print(len(render_all(argv[0] if argv else None)), "plans")
