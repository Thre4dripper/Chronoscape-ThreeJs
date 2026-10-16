"""
Re-render only the shadow decals (no texture bake) inside the live Blender, one model per timer tick.
    exec(open(".../shadow_queue.py").read()); start(keys)
Logs to tools/blender/baked/shadow_log.jsonl.
"""
import json, os, time, traceback
import bpy

ROOT = "/Users/ijlalahmad/Desktop/test/Chronoscape"
LOG = os.path.join(ROOT, "tools", "blender", "baked", "shadow_log.jsonl")
_ns = {"__name__": "bake_assets"}
exec(open(os.path.join(ROOT, "tools", "blender", "bake_assets.py")).read(), _ns)
STATE = {"queue": [], "B": None}


def _log(rec):
    with open(LOG, "a") as fh:
        fh.write(json.dumps(rec) + "\n")


def one(key):
    import chronokit
    B = STATE["B"]
    chronokit.reset_scene()
    m = B[key]()
    if hasattr(m, "stages"):
        m.finish()
    objs = [o for o in bpy.context.scene.objects if o.type == "MESH"]
    size = max(max(o.dimensions) for o in objs)
    _ns["set_cycles"](48)
    _ns["lighting"]()
    return _ns["render_shadow"](key, objs, size)


def _tick():
    if not STATE["queue"]:
        _log({"done": time.strftime("%H:%M:%S")})
        return None
    k = STATE["queue"].pop(0)
    t = time.time()
    try:
        r = {"key": k, **one(k)}
    except Exception as e:
        r = {"key": k, "error": str(e), "trace": traceback.format_exc()[-600:]}
    r["s"] = round(time.time() - t, 1)
    r["left"] = len(STATE["queue"])
    _log(r)
    return 0.2


def start(keys):
    STATE["B"] = _ns["builders"]()
    STATE["queue"] = list(keys)
    _log({"start": time.strftime("%H:%M:%S"), "count": len(keys)})
    if bpy.app.timers.is_registered(_tick):
        bpy.app.timers.unregister(_tick)
    bpy.app.timers.register(_tick, first_interval=0.5)
