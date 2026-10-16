"""
Build every landmark miniature and export it to assets/models/<city>/<name>.glb.

Headless:   blender -b -P tools/blender/build_all.py -- [filter]
In-session: exec(open("tools/blender/build_all.py").read()) with BUILD_FILTER set,
            or call build(key) / build_all() after importing.
"""
import importlib
import os
import sys

ROOT = os.path.abspath(os.path.join(os.path.dirname(os.path.abspath(__file__)), "..", "..")) if "__file__" in globals() else os.getcwd()
TOOLS = os.path.join(ROOT, "tools", "blender")
for p in (TOOLS, os.path.join(TOOLS, "models")):
    if p not in sys.path:
        sys.path.insert(0, p)

import chronokit
importlib.reload(chronokit)
import rome, delhi, rome_more, rome_fora, props
for _m in (rome, rome_more, rome_fora, delhi, props):
    importlib.reload(_m)

BUILDERS = {**rome.BUILDERS, **rome_more.BUILDERS, **rome_fora.BUILDERS, **delhi.BUILDERS, **props.BUILDERS}


def build(key, export=True):
    chronokit.reset_scene()
    m = BUILDERS[key]()
    m.finish()
    info = {"key": key, "stages": [o.name for o in m.objects]}
    if export:
        path = os.path.join(ROOT, "assets", "models", key + ".glb")
        os.makedirs(os.path.dirname(path), exist_ok=True)
        info.update(m.export(path))
        info["bytes"] = os.path.getsize(path)
    return info


def build_all(filter_text=None, export=True):
    out = []
    for key in BUILDERS:
        if filter_text and filter_text not in key:
            continue
        out.append(build(key, export))
    return out


if __name__ == "__main__" and "-b" in sys.argv:
    argv = sys.argv[sys.argv.index("--") + 1:] if "--" in sys.argv else []
    for info in build_all(argv[0] if argv else None):
        print(info)
