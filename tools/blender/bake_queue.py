"""
Run the bake inside a live Blender session without blocking it: a timer bakes one
model per tick and appends to tools/blender/baked/bake_log.jsonl.
    exec(open(".../bake_queue.py").read()); start(keys, density_by_key)
"""
import json, os, time, traceback
import bpy

ROOT = "/Users/ijlalahmad/Desktop/test/Chronoscape"
LOG = os.path.join(ROOT, "tools", "blender", "baked", "bake_log.jsonl")
_ns = {"__name__": "bake_assets"}
exec(open(os.path.join(ROOT, "tools", "blender", "bake_assets.py")).read(), _ns)
STATE = {"queue": [], "density": {}, "after": None}


def _log(rec):
    with open(LOG, "a") as fh:
        fh.write(json.dumps(rec) + "\n")


def _tick():
    if not STATE["queue"]:
        if STATE["after"]:
            try:
                STATE["after"]()
            except Exception as e:
                _log({"after_error": str(e)})
        _log({"done": time.strftime("%H:%M:%S")})
        return None
    k = STATE["queue"].pop(0)
    try:
        r = _ns["bake_vc"](k)
    except Exception as e:
        r = {"key": k, "error": str(e), "trace": traceback.format_exc()[-600:]}
    r["left"] = len(STATE["queue"])
    _log(r)
    return 0.2


def start(keys, density=None, after=None):
    STATE["queue"] = list(keys)
    STATE["density"] = density or {}
    STATE["after"] = after
    _log({"start": time.strftime("%H:%M:%S"), "count": len(keys)})
    if bpy.app.timers.is_registered(_tick):
        bpy.app.timers.unregister(_tick)
    bpy.app.timers.register(_tick, first_interval=0.5)
