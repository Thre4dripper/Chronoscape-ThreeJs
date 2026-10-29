"""
Bake every model the content packs reference, then re-render the map plans of the models baked.
Headless:  Blender -b -P tools/blender/bake_all.py -- [filter]
Progress is appended to tools/blender/baked/bake_log.jsonl (one JSON line per model).

Incremental: a model is baked again only when something it is built from changes: its builder's source
file (for Rome's older modules, any of them), the shared kits (chronokit, worldkit, archkit, props), the bake
code itself, or the scale it is shown at. The digests are kept in assets/models/bake-manifest.json, next to
the models. FORCE=1 bakes everything again; SEED=1 records the models on disk as current without baking.
"""
import hashlib, json, os, sys, glob, traceback, time
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

# ---- skip models whose inputs have not changed since they were last baked
TB = os.path.join(ROOT, "tools", "blender")
SHARED = [os.path.join(TB, f) for f in ("chronokit.py", "bake_assets.py", "citymods.py")] + [os.path.join(TB, "models", f) for f in ("worldkit.py", "archkit.py", "props.py")]
ROME_ERA = sorted(glob.glob(os.path.join(TB, "models", "*.py")))  # Rome's modules import each other
_file_digest = {}


def _digest_files(files):
    h = hashlib.sha1()
    for f in files:
        if f not in _file_digest:
            _file_digest[f] = hashlib.sha1(open(f, "rb").read()).hexdigest() if os.path.exists(f) else "-"
        h.update(f.encode() + _file_digest[f].encode())
    return h.hexdigest()


def model_digest(k):
    src = os.path.abspath(B[k].__code__.co_filename)
    own = [src] if os.sep + "cities" + os.sep in src or os.sep + "props_sets" + os.sep in src else ROME_ERA
    return _digest_files(sorted(set(own + SHARED))) + f":{scale.get(k, 1.0)}"


MANIFEST = os.path.join(ROOT, "assets", "models", "bake-manifest.json")
baked_before = json.load(open(MANIFEST)) if os.path.exists(MANIFEST) else {}
digests = {k: model_digest(k) for k in todo}


def current(k):
    glb = os.path.join(ROOT, "assets", "models", k + ".glb")
    shadow_ok = k.startswith("props/") or glob.glob(os.path.join(ROOT, "assets", "models", "shadows", k + ".*"))
    return baked_before.get(k) == digests[k] and os.path.exists(glb) and shadow_ok


if os.environ.get("SEED"):
    # record the current models as baked from the current sources (after a full bake made outside this script)
    for k in todo:
        if os.path.exists(os.path.join(ROOT, "assets", "models", k + ".glb")):
            baked_before[k] = digests[k]
    json.dump(baked_before, open(MANIFEST, "w"), indent=1, sort_keys=True)
    print(f"bake: seeded {len(baked_before)} digests", flush=True)
    sys.exit(0)

if not os.environ.get("FORCE"):
    kept = [k for k in todo if current(k)]
    todo = [k for k in todo if k not in set(kept)]
    print(f"bake: {len(todo)} to bake, {len(kept)} unchanged", flush=True)
log = os.path.join(ROOT, "tools", "blender", "baked", "bake_log.jsonl")
os.makedirs(os.path.dirname(log), exist_ok=True)
if os.environ.get("SKIP_DONE") and os.path.exists(log):
    done = {json.loads(l).get("key") for l in open(log) if '"tris"' in l}
    todo = [k for k in todo if k not in done]
with open(log, "a") as fh:
    fh.write(json.dumps({"start": time.strftime("%H:%M:%S"), "count": len(todo), "missing_builders": missing}) + "\n")
done = []
for i, k in enumerate(todo):
    try:
        r = ns["bake_vc"](k)
        r["i"] = i + 1
        done.append(k)
        baked_before[k] = digests[k]
        # record as we go, so an interrupted run resumes where it stopped
        with open(MANIFEST, "w") as fh:
            json.dump(baked_before, fh, indent=1, sort_keys=True)
    except Exception as e:
        r = {"key": k, "error": str(e), "trace": traceback.format_exc()[-600:]}
    with open(log, "a") as fh:
        fh.write(json.dumps(r) + "\n")
# plans from the final geometry, for the models just baked
pns = {"__name__": "render_plans", "__file__": os.path.join(ROOT, "tools", "blender", "render_plans.py")}
exec(open(os.path.join(ROOT, "tools", "blender", "render_plans.py")).read(), pns)
pns["render_keys"](done)
with open(log, "a") as fh:
    fh.write(json.dumps({"done": time.strftime("%H:%M:%S")}) + "\n")

# the study (the writing table and the things on it) bakes from its own builders, incrementally, into assets/models/study
sns = {"__name__": "bake_study"}
exec(open(os.path.join(ROOT, "tools", "blender", "bake_study.py")).read(), sns)
sns["main"]()
