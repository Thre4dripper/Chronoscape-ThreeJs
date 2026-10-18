"""
List a finished city in content/cities/index.json and make its atlas map(s) playable.

    python3 tools/content/register_city.py <id> "<atlas-id>:<map title>:<period-id>" [...]
"""
import json, os, sys

ROOT = os.path.abspath(os.path.join(os.path.dirname(os.path.abspath(__file__)), "..", ".."))
cid, maps = sys.argv[1], sys.argv[2:]
city = json.load(open(os.path.join(ROOT, "content", "cities", cid, "city.json")))

ip = os.path.join(ROOT, "content", "cities", "index.json")
index = json.load(open(ip))
entry = {"id": cid, "name": city["name"], "subtitle": city["subtitle"], "status": "playable"}
index["cities"] = [c for c in index["cities"] if c["id"] != cid] + [entry]
with open(ip, "w") as f:
    f.write('{\n  "cities": [\n' + ",\n".join("    { " + json.dumps(c, ensure_ascii=False, separators=(", ", ": "))[1:-1] + " }" for c in index["cities"]) + "\n  ]\n}\n")

ap = os.path.join(ROOT, "content", "atlases.json")
text = open(ap).read()
cat = json.loads(text)
for spec in maps:
    atlas_id, title, period = spec.split(":")
    assert any(p["id"] == period for p in city["periods"]), f"{cid} has no period {period}"
    # edit the text in place (keeps the hand formatting of the file): find the atlas, then the map's title line
    a0 = text.index(f'"id": "{atlas_id}"')
    t0 = text.index(f'"title": "{title}"', a0)
    line_end = text.index("\n", t0)
    indent = text[text.rindex("\n", 0, t0) + 1:t0]
    obj_end = text.index("}", t0)
    t0 = text.index("\n", text.rindex("{", 0, t0)) + 1 + len(indent)
    block = text[t0:obj_end]
    block = "\n".join(l for l in block.split("\n") if '"city":' not in l and '"period":' not in l).lstrip()
    block = block.rstrip()
    if not block.endswith(","):
        block += ","
    block += f'\n{indent}"city": "{cid}",\n{indent}"period": "{period}"\n{indent[:-2]}'
    text = text[:t0] + block + text[obj_end:]
    print(f"{atlas_id}: {title} -> {cid}/{period}")
json.loads(text)
open(ap, "w").write(text)
