"""Model builders of every city after Rome (tools/blender/models/cities/<id>.py, BUILDERS keyed "<id>/<model>") and the
regional street-life prop sets (tools/blender/models/props_sets/*.py, keyed "props/<set>/<prop>")."""
import glob, importlib, importlib.util, os

ROOT = "/Users/ijlalahmad/Desktop/test/Chronoscape"


def city_builders():
    import worldkit
    importlib.reload(worldkit)
    out = {}
    files = glob.glob(os.path.join(ROOT, "tools", "blender", "models", "cities", "*.py")) + glob.glob(os.path.join(ROOT, "tools", "blender", "models", "props_sets", "*.py"))
    for f in sorted(files):
        if os.path.basename(f).startswith("_"):
            continue
        # a module still being written must not stop every other city from building
        try:
            spec = importlib.util.spec_from_file_location("city_" + os.path.basename(f)[:-3], f)
            mod = importlib.util.module_from_spec(spec)
            spec.loader.exec_module(mod)
            out.update(mod.BUILDERS)
        except Exception as e:
            print(f"citymods: skipping {os.path.basename(f)}: {e!r}")
    return out
