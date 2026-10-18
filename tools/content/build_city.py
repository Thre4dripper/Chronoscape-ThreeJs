"""
Assemble content/cities/<id>/city.json from a city's data modules, written in
latitude/longitude and metres (see tools/content/cities/FORMAT.md):

    tools/content/cities/<id>/geo.py        city, frame, periods and the map's geography
    tools/content/cities/<id>/landmarks.py  monuments (each with a Blender model)
    tools/content/cities/<id>/life.py       spots of daily life, events, stories

    python3 tools/content/build_city.py <id> [<id> ...]     (or --all)

Rome predates this and keeps its own script, build_rome.py.
"""
import importlib.util, json, math, os, sys

HERE = os.path.dirname(os.path.abspath(__file__))
ROOT = os.path.abspath(os.path.join(HERE, "..", ".."))
CITIES = os.path.join(HERE, "cities")

PLAN_MANIFEST = os.path.join(ROOT, "assets", "models", "plans", "manifest.json")


def load(cid, name):
    path = os.path.join(CITIES, cid, name + ".py")
    if not os.path.exists(path):
        return None
    spec = importlib.util.spec_from_file_location(f"{cid}_{name}", path)
    mod = importlib.util.module_from_spec(spec)
    spec.loader.exec_module(mod)
    return mod


class Frame:
    """Equirectangular projection onto a local grid in metres: origin top-left, y down."""

    def __init__(self, nw, se):
        (self.lat0, self.lon0), (lat1, lon1) = nw, se
        mid = math.radians((self.lat0 + lat1) / 2)
        self.kx = 111320.0 * math.cos(mid)
        self.ky = 110950.0
        self.size = [round((lon1 - self.lon0) * self.kx), round((self.lat0 - lat1) * self.ky)]

    def P(self, latlon):
        lat, lon = latlon
        return [round((lon - self.lon0) * self.kx), round((self.lat0 - lat) * self.ky)]

    def path(self, pts):
        return [self.P(p) for p in pts]


def fallback_for(lm):
    w, d = lm["footprint"]
    if "fallback" in lm:
        return lm["fallback"]
    cat, key = lm["category"], lm["model"].split("/")[-1]
    if "mosque" in key or "masjid" in key:
        return dict(kit="mosque", width=w, depth=d, domes=3, minaretHeight=max(20, w * 0.3))
    if cat == "military" or "fort" in key or "gate" in key or "wall" in key:
        return dict(kit="fort", width=w, depth=d, wallHeight=max(8, min(w, d) * 0.2), bastions=8)
    if cat == "temple":
        return dict(kit="temple", width=w, depth=d, columnsFront=6, columnsSide=0, podium=max(1.5, min(w, d) * 0.1), columnHeight=max(6, min(w, d) * 0.4))
    if cat in ("district", "commercial"):
        return dict(kit="cluster", plaza=dict(width=w, depth=d), buildings=[dict(offset=[-w * 0.25, -d * 0.25], width=w * 0.3, depth=d * 0.3, height=8), dict(offset=[w * 0.25, d * 0.2], width=w * 0.3, depth=d * 0.3, height=7)])
    return dict(kit="hall", width=w, depth=d, height=max(8, min(w, d) * 0.4), roof="flat" if cat == "monument" else "pitched")


def build(cid):
    geo, lms, life = load(cid, "geo"), load(cid, "landmarks"), load(cid, "life")
    if geo is None or lms is None:
        raise SystemExit(f"{cid}: needs geo.py and landmarks.py in {os.path.join(CITIES, cid)}")
    F = Frame(*geo.FRAME)
    P, path = F.P, F.path
    plans = json.load(open(PLAN_MANIFEST)) if os.path.exists(PLAN_MANIFEST) else {}
    G = lambda name: getattr(geo, name, [])

    def per(d, out):
        if d.get("periods"):
            out["periods"] = list(d["periods"])
        return out

    def opt(d, out, *keys):
        for k in keys:
            if d.get(k) not in (None, "", []):
                out[k] = d[k]
        return out

    water = [per(w, opt(w, dict(name=w["name"], path=path(w["path"]), width=w["width"]), "id", "blurb")) for w in G("WATER")]
    islands = [per(i, dict(name=i["name"], polygon=path(i["polygon"]))) for i in G("ISLANDS")]
    hills = [per(h, opt(h, dict(name=h["name"], center=P(h["center"]), radius=h["radius"], label=h.get("label", True)), "id", "blurb")) for h in G("HILLS")]
    roads = [per(r, opt(r, dict(name=r["name"], path=path(r["path"]), width=r.get("width", 8), style=r.get("style", "minor"), labelled=r.get("labelled", False)), "id", "blurb")) for r in G("ROADS")]
    walls = [per(w, opt(w, dict(name=w["name"], path=path(w["path"]), closed=w.get("closed", False)), "id", "blurb")) for w in G("WALLS")]
    gates = [per(g, opt(g, dict(name=g["name"], position=P(g["position"])), "id")) for g in G("GATES")]
    bridges = [per(b, opt(b, dict(name=b["name"], path=path(b["path"]), build=b.get("build", "stone"), arches=b.get("arches", 4)), "id", "blurb", "landmarkId")) for b in G("BRIDGES")]
    aqueducts = [per(a, dict(name=a["name"], path=path(a["path"]))) for a in G("AQUEDUCTS")]
    blocks = [per(b, opt(b, dict(polygon=path(b["polygon"]), density=b.get("density", "dense")), "name")) for b in G("BLOCKS")]
    gardens = [per(g, opt(g, dict(polygon=path(g["polygon"]), kind=g.get("kind", "park")), "name")) for g in G("GARDENS")]
    marsh = [per(m, opt(m, dict(polygon=path(m["polygon"])), "name")) for m in G("MARSH")]
    districts = [per(d, opt(d, dict(id=d["id"], name=d["name"], polygon=path(d["polygon"])), "description")) for d in G("DISTRICTS")]
    labels = [per(l, dict(text=l["text"], position=P(l["position"]), size=l.get("size", "md"), rotation=l.get("rotation", 0))) for l in G("LABELS")]
    mp = dict(size=F.size, resolution=getattr(geo, "RESOLUTION", 4096), water=water, islands=islands, hills=hills, roads=roads, walls=walls, gates=gates,
              bridges=bridges, aqueducts=aqueducts, blocks=blocks, gardens=gardens, marsh=marsh, districts=districts, labels=labels)
    if getattr(geo, "PALETTE", None):
        mp["palette"] = geo.PALETTE
    if getattr(geo, "COMPASS", None):
        mp["compass"] = P(geo.COMPASS)
    if getattr(geo, "CARTOUCHE", None):
        mp["cartouche"] = P(geo.CARTOUCHE)

    def model(lm, key):
        return dict(glb=f"models/{key}.glb", fallback=fallback_for({**lm, "model": key}))

    def footprint(lm):
        p = plans.get(lm["model"])
        if p and p.get("w") and p.get("d"):
            return [round(p["w"], 1), round(p["d"], 1)]
        return list(lm["footprint"])

    def landmark(lm):
        out = dict(id=lm["id"], placeId=lm.get("placeId", lm["id"]), name=lm["name"], category=lm["category"], position=P(lm["latlon"]), rotation=lm.get("rotation", 0),
                   footprint=footprint(lm), scale=lm.get("scale", 1), model=model(lm, lm["model"]), reveal="assemble", activePeriods=lm["activePeriods"], variants={},
                   summary=lm["summary"], details=lm.get("details", []), confidence=lm["confidence"], sourceIds=lm["sourceIds"])
        opt(lm, out, "built", "function", "focus", "activity")
        for pid, v in lm.get("variants", {}).items():
            vv = {k: val for k, val in v.items() if k != "model" and val not in ("", None)}
            if v.get("model"):
                vv["model"] = model(lm, v["model"])
            out["variants"][pid] = vv
        return out

    def spot(s):
        out = dict(id=s["id"], name=s["name"], kind=s["kind"], position=P(s["latlon"]), activePeriods=s["activePeriods"], summary=s["summary"], details=s.get("details", []),
                   confidence=s["confidence"], sourceIds=s["sourceIds"], vignettes=s.get("vignettes", []), variants={})
        for pid, v in s.get("variants", {}).items():
            out["variants"][pid] = {k: val for k, val in v.items() if val not in ("", None)}
        return out

    def event(e):
        at = dict(e["at"])
        if "latlon" in at:
            at = dict(position=P(at["latlon"]))
        return dict(id=e["id"], title=e["title"], periodId=e["periodId"], date=e["date"], kind=e["kind"], at=at, effect=e.get("effect", "none"), text=e["text"], sourceIds=e["sourceIds"])

    def story(s):
        steps = [{k: v for k, v in st.items() if v not in ("", None)} for st in s["steps"]]
        return dict(id=s["id"], title=s["title"], periodId=s["periodId"], summary=s["summary"], steps=steps, sourceIds=s["sourceIds"])

    sources = {}
    for mod in (geo, lms, life):
        for src in getattr(mod, "SOURCES", []) if mod else []:
            sources.setdefault(src["id"], src)

    C = geo.CITY
    cam = C.get("camera", {})
    city = dict(
        id=cid, name=C["name"], subtitle=C["subtitle"], description=C["description"], defaultPeriodId=C["defaultPeriodId"],
        world={"scale": 0.01, **C.get("world", {})},
        camera=dict(projection="perspective", start=dict(target=P(cam.get("target", C.get("center"))), distance=cam.get("distance", 38), tilt=cam.get("tilt", 52), heading=0),
                    minDistance=cam.get("minDistance", 1.6), maxDistance=cam.get("maxDistance", 130)),
        map=mp,
        periods=[dict(p) for p in geo.PERIODS],
        landmarks=[landmark(l) for l in lms.LANDMARKS],
        spots=[spot(s) for s in getattr(life, "SPOTS", [])] if life else [],
        events=[event(e) for e in getattr(life, "EVENTS", [])] if life else [],
        stories=[story(s) for s in getattr(life, "STORIES", [])] if life else [],
        sources=list(sources.values()),
    )
    os.makedirs(os.path.join(ROOT, "content", "cities", cid), exist_ok=True)
    out = os.path.join(ROOT, "content", "cities", cid, "city.json")
    with open(out, "w") as f:
        json.dump(city, f, indent=1, ensure_ascii=False)
    print(f"{cid}: {F.size[0]}x{F.size[1]} m, {len(city['periods'])} periods, {len(city['landmarks'])} landmarks, {len(city['spots'])} spots, "
          f"{len(city['events'])} events, {len(city['stories'])} stories, {len(city['sources'])} sources, {os.path.getsize(out) // 1024} KB")
    return city


if __name__ == "__main__":
    ids = sys.argv[1:]
    if ids == ["--all"]:
        ids = sorted(d for d in os.listdir(CITIES) if os.path.exists(os.path.join(CITIES, d, "geo.py")))
    for cid in ids:
        build(cid)
