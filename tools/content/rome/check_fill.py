"""Report empty fields in a content module. Usage: python3 check_fill.py landmarks_a.py"""
import ast, sys

def walk(node, path, out):
    if isinstance(node, dict):
        for k, v in node.items():
            walk(v, f"{path}.{k}", out)
    elif isinstance(node, list):
        if len(node) == 0 and path.rsplit(".", 1)[-1] in ("details", "sourceIds", "vignettes", "steps"):
            out.append(f"{path}: empty list")
        for i, v in enumerate(node):
            walk(v, f"{path}[{i}]", out)
    elif node == "":
        out.append(f"{path}: empty string")

def main(file):
    tree = ast.parse(open(file).read())
    ns = {}
    exec(compile(tree, file, "exec"), ns)
    problems = []
    for name in ("LANDMARKS", "SPOTS", "EVENTS", "DISTRICTS", "ROADS", "HILLS", "WATER", "STORIES", "PERIODS"):
        if name in ns:
            for item in ns[name]:
                label = item.get("id", "?")
                walk(item, f"{name}[{label}]", problems)
    # source references
    ids = {s["id"] for s in ns.get("SOURCES", [])}
    def refs(node):
        if isinstance(node, dict):
            for k, v in node.items():
                if k == "sourceIds":
                    for s in v:
                        if s not in ids:
                            problems.append(f"unknown source id {s!r}")
                else:
                    refs(v)
        elif isinstance(node, list):
            for v in node:
                refs(v)
    for name in ("LANDMARKS", "SPOTS", "EVENTS", "STORIES"):
        refs(ns.get(name, []))
    if "SPOTS" in ns:
        for s in ns["SPOTS"]:
            if len(s.get("vignettes", [])) < 3:
                problems.append(f"SPOTS[{s['id']}]: needs 3 vignettes")
    print(f"{file}: {len(problems)} problem(s)")
    for p in problems[:400]:
        print("  -", p)
    return 1 if problems else 0

if __name__ == "__main__":
    sys.exit(main(sys.argv[1]))
