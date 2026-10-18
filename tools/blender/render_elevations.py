"""
Render a front elevation of every landmark model as a sepia architectural
drawing (orthographic, looking north at the facade, which faces south in every
builder). Output: assets/media/elevations/<city>/<name>.png plus manifest.json
with the drawing's extent in metres, so the app can draw a scale bar and a
human figure at the right size.

In a live Blender:  exec(open(".../render_elevations.py").read()); start(keys)
"""
import json, os, sys, time, importlib, traceback
import bpy
import numpy as np
from mathutils import Vector

ROOT = "/Users/ijlalahmad/Desktop/test/Chronoscape"
for p in (os.path.join(ROOT, "tools", "blender"), os.path.join(ROOT, "tools", "blender", "models")):
    if p not in sys.path:
        sys.path.insert(0, p)
import chronokit, archkit, rome, rome_more, rome_fora, delhi, rome_hero, rome_hero2, props
for _m in (chronokit, archkit, rome, rome_more, rome_fora, delhi, rome_hero, rome_hero2, props):
    importlib.reload(_m)
BUILDERS = {**rome.BUILDERS, **rome_more.BUILDERS, **rome_fora.BUILDERS, **delhi.BUILDERS, **rome_hero.BUILDERS, **rome_hero2.BUILDERS}
import citymods
importlib.reload(citymods)
BUILDERS.update(citymods.city_builders())

INK = np.array([0x4a, 0x33, 0x22]) / 255.0
PAPER = np.array([0xf3, 0xe8, 0xce]) / 255.0
OUT = os.path.join(ROOT, "assets", "media", "elevations")
LOG = os.path.join(ROOT, "tools", "blender", "baked", "elevation_log.jsonl")


def render_elevation(key):
    chronokit.reset_scene()
    m = BUILDERS[key]()
    if hasattr(m, "finish"):
        m.finish()
    meshes = [o for o in bpy.context.scene.objects if o.type == "MESH"]
    pts = [o.matrix_world @ Vector(c) for o in meshes for c in o.bound_box]
    x0, x1 = min(p.x for p in pts), max(p.x for p in pts)
    y0 = min(p.y for p in pts)
    z0, z1 = 0.0, max(p.z for p in pts)
    w, h = x1 - x0, z1 - z0
    pad = max(w, h) * 0.04 + 1
    W, H = w + 2 * pad, h + 2 * pad
    scene = bpy.context.scene
    cam_data = bpy.data.cameras.new("elev_cam")
    cam_data.type = "ORTHO"
    cam_data.ortho_scale = max(W, H)
    cam_data.clip_end = 5000
    cam = bpy.data.objects.new("elev_cam", cam_data)
    scene.collection.objects.link(cam)
    cam.location = ((x0 + x1) / 2, y0 - 1000, h / 2)
    cam.rotation_euler = (1.5707963, 0, 0)  # looking north (+Y), up is +Z
    scene.camera = cam
    try:
        scene.render.engine = "BLENDER_WORKBENCH"
    except TypeError:
        pass
    sh = scene.display.shading
    sh.light = "STUDIO"
    sh.color_type = "MATERIAL"
    sh.show_shadows = False
    sh.show_cavity = True
    sh.cavity_type = "BOTH"
    sh.cavity_ridge_factor = 1.6
    sh.cavity_valley_factor = 1.6
    sh.show_object_outline = True
    sh.object_outline_color = (0.12, 0.08, 0.05)
    scene.render.film_transparent = True
    k = min(1400 / W, 900 / H, 12.0)
    scene.render.resolution_x = max(64, int(W * k))
    scene.render.resolution_y = max(64, int(H * k))
    scene.render.resolution_percentage = 100
    path = os.path.join(OUT, key + ".png")
    os.makedirs(os.path.dirname(path), exist_ok=True)
    scene.render.filepath = path
    scene.render.image_settings.file_format = "PNG"
    scene.render.image_settings.color_mode = "RGBA"
    bpy.ops.render.render(write_still=True)
    bpy.data.objects.remove(cam, do_unlink=True)
    bpy.data.cameras.remove(cam_data)
    # sepia ink on transparent paper
    img = bpy.data.images.load(path, check_existing=False)
    a = np.array(img.pixels[:], dtype=np.float32).reshape(-1, 4)
    lum = np.clip(a[:, 0] * 0.3 + a[:, 1] * 0.55 + a[:, 2] * 0.15, 0, 1)
    lum = np.clip((lum - 0.12) / 0.62, 0, 1) ** 1.05
    a[:, :3] = INK[None, :] + (PAPER - INK)[None, :] * lum[:, None]
    # flatten onto the drawing-sheet colour and keep a light JPEG (the PNG is removed)
    bg = np.array([0xf7, 0xee, 0xd6], dtype=np.float32) / 255.0
    al = a[:, 3:4]
    a[:, :3] = a[:, :3] * al + bg * (1 - al)
    a[:, 3] = 1
    img.pixels = a.ravel()
    img.filepath_raw = path[:-4] + ".jpg"
    img.file_format = "JPEG"
    img.save(quality=84)
    bpy.data.images.remove(img)
    os.remove(path)
    rx, ry = scene.render.resolution_x, scene.render.resolution_y
    # metres per pixel, and where the ground line sits (pixels from the top)
    mpp = max(W, H) / max(rx, ry)
    ground = ry / 2 + (h / 2) / mpp
    return {"w": round(w, 2), "h": round(h, 2), "px": [rx, ry], "mpp": round(mpp, 5), "ground": round(ground, 1), "x0px": round(rx / 2 - (w / 2) / mpp, 1)}


STATE = {"queue": [], "manifest": None}


def _tick():
    if not STATE["queue"]:
        json.dump(STATE["manifest"], open(os.path.join(OUT, "manifest.json"), "w"), indent=1, sort_keys=True)
        with open(LOG, "a") as fh:
            fh.write(json.dumps({"done": time.strftime("%H:%M:%S")}) + "\n")
        return None
    k = STATE["queue"].pop(0)
    try:
        STATE["manifest"][k] = render_elevation(k)
        rec = {"key": k, **STATE["manifest"][k]}
    except Exception as e:
        rec = {"key": k, "error": str(e), "trace": traceback.format_exc()[-400:]}
    rec["left"] = len(STATE["queue"])
    with open(LOG, "a") as fh:
        fh.write(json.dumps(rec) + "\n")
    if len(STATE["queue"]) % 10 == 0:
        json.dump(STATE["manifest"], open(os.path.join(OUT, "manifest.json"), "w"), indent=1, sort_keys=True)
    return 0.1


def start(keys):
    os.makedirs(OUT, exist_ok=True)
    mp = os.path.join(OUT, "manifest.json")
    STATE["manifest"] = json.load(open(mp)) if os.path.exists(mp) else {}
    STATE["queue"] = [k for k in keys if k in BUILDERS]
    with open(LOG, "a") as fh:
        fh.write(json.dumps({"start": time.strftime("%H:%M:%S"), "count": len(STATE["queue"])}) + "\n")
    if bpy.app.timers.is_registered(_tick):
        bpy.app.timers.unregister(_tick)
    bpy.app.timers.register(_tick, first_interval=0.3)


def render_now(keys):
    """Headless: Blender -b -P tools/blender/render_elevations.py -- <prefix> renders every model whose key starts with it."""
    os.makedirs(OUT, exist_ok=True)
    mp = os.path.join(OUT, "manifest.json")
    man = json.load(open(mp)) if os.path.exists(mp) else {}
    for k in keys:
        try:
            man[k] = render_elevation(k)
        except Exception as e:
            print("elevation failed", k, e)
    json.dump(man, open(mp, "w"), indent=1, sort_keys=True)


if __name__ == "__main__" and "--" in sys.argv:
    pre = sys.argv[sys.argv.index("--") + 1:]
    render_now([k for k in BUILDERS if any(k.startswith(p) for p in pre)])
