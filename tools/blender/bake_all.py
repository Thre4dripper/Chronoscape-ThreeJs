"""
Bake every model the content packs reference, then re-render the map plans.
Headless:  Blender -b -P tools/blender/bake_all.py -- [filter]
Progress is appended to tools/blender/baked/bake_log.jsonl (one JSON line per model).
"""
import json, os, sys, glob, traceback, time
ROOT = "/Users/ijlalahmad/Desktop/test/Chronoscape"
sys.path.insert(0, os.path.join(ROOT, "tools", "blender"))
ns = {"__name__": "bake_assets"}
exec(open(os.path.join(ROOT, "tools", "blender", "bake_assets.py")).read(), ns)
argv = sys.argv[sys.argv.index("--") + 1:] if "--" in sys.argv else []
flt = argv[0] if argv else None

keys = set()
scale = {}   # the app enlarges small monuments; give them proportionally more texels
for f in glob.glob(os.path.join(ROOT, "content", "cities", "*", "city.json")):
    c = json.load(open(f))
    for l in c["landmarks"]:
        for mdl in [l["model"]] + [v.get("model") for v in l.get("variants", {}).values()]:
            if mdl and "glb" in mdl:
                k = mdl["glb"][len("models/"):-len(".glb")]
                keys.add(k)
                scale[k] = max(scale.get(k, 1.0), l.get("scale", 1.0))
min_scale = float(os.environ.get("MIN_SCALE", "0"))
B = ns["builders"]()
keys |= {k for k in B if k.startswith("props/") and k not in ("props/aqueduct-bay", "props/wall-bay", "props/wall-tower", "props/gatehouse")} | {"props/aqueduct-bay", "props/wall-bay", "props/wall-tower", "props/gatehouse"}
todo = sorted(k for k in keys if k in B and (not flt or flt in k) and (scale.get(k, 1.0) >= min_scale or k.startswith("props/")))
missing = sorted(k for k in keys if k not in B)
log = os.path.join(ROOT, "tools", "blender", "baked", "bake_log.jsonl")
os.makedirs(os.path.dirname(log), exist_ok=True)
if os.environ.get("SKIP_DONE") and os.path.exists(log):
    done = {json.loads(l).get("key") for l in open(log) if '"tris"' in l}
    todo = [k for k in todo if k not in done]
with open(log, "a") as fh:
    fh.write(json.dumps({"start": time.strftime("%H:%M:%S"), "count": len(todo), "missing_builders": missing}) + "\n")
for i, k in enumerate(todo):
    try:
        r = ns["bake_vc"](k)
        r["i"] = i + 1
    except Exception as e:
        r = {"key": k, "error": str(e), "trace": traceback.format_exc()[-600:]}
    with open(log, "a") as fh:
        fh.write(json.dumps(r) + "\n")
# plans from the final geometry
pns = {"__name__": "render_plans", "__file__": os.path.join(ROOT, "tools", "blender", "render_plans.py")}
exec(open(os.path.join(ROOT, "tools", "blender", "render_plans.py")).read(), pns)
pns["render_all"](flt)
with open(log, "a") as fh:
    fh.write(json.dumps({"done": time.strftime("%H:%M:%S")}) + "\n")
