"""List the baked regional prop sets: assets/models/props/sets.json = {set: [prop names]}."""
import json, os
ROOT = os.path.abspath(os.path.join(os.path.dirname(os.path.abspath(__file__)), "..", ".."))
d = os.path.join(ROOT, "assets", "models", "props")
sets = {s: sorted(f[:-4] for f in os.listdir(os.path.join(d, s)) if f.endswith(".glb")) for s in sorted(os.listdir(d)) if os.path.isdir(os.path.join(d, s))}
json.dump(sets, open(os.path.join(d, "sets.json"), "w"), indent=1)
print({k: len(v) for k, v in sets.items()})
