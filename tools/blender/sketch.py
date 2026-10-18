"""
Build one or more models without baking and render a quick studio preview of each,
to check a builder while writing it.

    Blender -b -P tools/blender/sketch.py -- <out_dir> <key> [<key> ...]
    (a key ending in "/" sketches every model of that city, e.g. "delhi/")
"""
import os, sys, json, traceback
ROOT = "/Users/ijlalahmad/Desktop/test/Chronoscape"
sys.path.insert(0, os.path.join(ROOT, "tools", "blender"))
ns = {"__name__": "bake_assets"}
exec(open(os.path.join(ROOT, "tools", "blender", "bake_assets.py")).read(), ns)
pv = {"__name__": "preview"}
exec(open(os.path.join(ROOT, "tools", "blender", "preview.py")).read(), pv)
import bpy, chronokit

argv = sys.argv[sys.argv.index("--") + 1:]
out_dir, keys = argv[0], argv[1:]
os.makedirs(out_dir, exist_ok=True)
B = ns["builders"]()
todo = [k for want in keys for k in (sorted(x for x in B if x.startswith(want)) if want.endswith("/") else [want])]
for k in todo:
    try:
        chronokit.reset_scene()
        m = B[k]()
        if hasattr(m, "stages"):
            m.finish()
        objs = [o for o in bpy.context.scene.objects if o.type == "MESH"]
        lo = [min(min((o.matrix_world @ __import__("mathutils").Vector(c))[i] for c in o.bound_box) for o in objs) for i in range(3)]
        hi = [max(max((o.matrix_world @ __import__("mathutils").Vector(c))[i] for c in o.bound_box) for o in objs) for i in range(3)]
        tris = sum(len(o.data.polygons) for o in objs)
        path = os.path.join(out_dir, k.replace("/", "__") + ".png")
        pv["shoot"](path, el=32, az=-35, w=900, h=620, textured=False)
        print("SKETCH", json.dumps({"key": k, "size": [round(hi[i] - lo[i], 1) for i in range(3)], "min_z": round(lo[2], 2), "faces": tris, "png": path}))
    except Exception as e:
        print("SKETCH", json.dumps({"key": k, "error": str(e), "trace": traceback.format_exc()[-800:]}))
