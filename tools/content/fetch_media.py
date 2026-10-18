"""
Fetch freely licensed pictures for every landmark from its Wikipedia article
(Wikimedia Commons): historic engravings, paintings, plans and reconstructions
first, then a photograph or two. Each image is downscaled, saved under
assets/media/<city>/<landmark>/, and listed in assets/media/<city>/index.json
with its artist, date, licence and a link back to the file page.

    python3 tools/content/fetch_media.py rome [--only colosseum,pantheon] [--force]
"""
import html, json, os, re, ssl, subprocess, sys, time, urllib.error, urllib.parse, urllib.request

ROOT = os.path.dirname(os.path.dirname(os.path.dirname(os.path.abspath(__file__))))
UA = "Chronoscape/0.1 (educational map prototype; offline asset build)"
API = "https://en.wikipedia.org/w/api.php"
MAX_PER = 5
# python.org builds ship without a CA bundle: use the system one
CTX = ssl.create_default_context(cafile="/etc/ssl/cert.pem") if os.path.exists("/etc/ssl/cert.pem") else ssl.create_default_context()
WIDTH = 960
MAIN = 800    # the notebook shows pictures ~340 px wide (lightbox up to 800)
THUMB = 200

FREE = re.compile(r"(public domain|^pd\b|cc0|cc[ -]by|cc[ -]by[ -]sa|gfdl|attribution)", re.I)
SKIP = re.compile(r"(\.svg$|\.gif$|logo|icon|flag|locator|location|commons-|wiki|edit-|padlock|question_book|ambox|oojs|symbol|portal|disambig|coat_of_arms|stub|map_of_|_map\.|mappa|globe|crystal_clear|nuvola|red_pog|speaker|sound|audio)", re.I)
HISTORIC = [(r"piranesi", 6), (r"\bvasi\b|giuseppe_vasi", 5), (r"panini|pannini", 4), (r"canaletto|bellotto|van_wittel|vanvitelli", 4),
            (r"engraving|etching|incisione|stampa|veduta|vedute", 4), (r"reconstruct|ricostruz|rekonstruk|plastico|model|maquette|gismondi", 4),
            (r"\bplan\b|pianta|_plan|grundriss|plan_of|floor_plan|ground_plan", 3), (r"painting|dipinto|oil_on|fresco", 3), (r"drawing|disegno|sketch", 3),
            (r"lanciani|forma_urbis|nolli|bufalini|tempesta|du_p[eé]rac|dupérac", 5), (r"coin|sestertius|denarius|aureus|medal", 3)]


def get(params):
    params = {**params, "format": "json", "formatversion": "2"}
    req = urllib.request.Request(API + "?" + urllib.parse.urlencode(params), headers={"User-Agent": UA})
    for attempt in range(8):
        try:
            with urllib.request.urlopen(req, timeout=30, context=CTX) as r:
                return json.load(r)
        except urllib.error.HTTPError as e:
            err = e
            # rate-limited: wait as long as the server asks (or back off), then try again
            wait = float(e.headers.get("Retry-After") or 0) or 8 * (attempt + 1) if e.code in (429, 503) else 1.5 * (attempt + 1)
            time.sleep(min(wait, 120))
        except Exception as e:
            time.sleep(1.5 * (attempt + 1))
            err = e
    raise err


def fetch_bytes(url):
    """Download with polite pacing; on 429 wait as long as the server asks."""
    req = urllib.request.Request(url, headers={"User-Agent": UA})
    for attempt in range(8):
        try:
            with urllib.request.urlopen(req, timeout=60, context=CTX) as r:
                return r.read()
        except urllib.error.HTTPError as e:
            if e.code not in (429, 503) or attempt == 7:
                raise
            wait = float(e.headers.get("Retry-After") or 0) or 5 * (attempt + 1)
            time.sleep(min(wait, 120))
    raise RuntimeError("unreachable")


def shrink(dst):
    """Main picture at most MAIN px, JPEG quality 62; a THUMB px thumbnail beside it (t<n>.jpg)."""
    subprocess.run(["sips", "-s", "format", "jpeg", "-s", "formatOptions", "62", "-Z", str(MAIN), dst, "--out", dst], capture_output=True)
    d, f = os.path.split(dst)
    subprocess.run(["sips", "-s", "format", "jpeg", "-s", "formatOptions", "55", "-Z", str(THUMB), dst, "--out", os.path.join(d, "t" + f)], capture_output=True)


def strip(s, n=None):
    s = html.unescape(re.sub(r"<[^>]+>", "", s or "")).strip()
    s = re.sub(r"\s+", " ", s)
    if n and len(s) > n:
        cut = s[:n]
        dot = max(cut.rfind(". "), cut.rfind("; "))
        s = (cut[: dot + 1] if dot > n * 0.5 else cut.rsplit(" ", 1)[0] + "…")
    return s


def clean_date(d):
    d = re.sub(r"QS:\S+", "", d)
    d = re.sub(r"date\s*…?$|date…", "", d)
    d = re.sub(r"\s+", " ", d).strip(" ;,")
    return d


def year_of(meta):
    d = clean_date(strip(meta.get("DateTimeOriginal", {}).get("value", "")))
    m = re.search(r"\b(1[0-9]{3}|20[0-2][0-9])\b", d)
    return (int(m.group(1)) if m else None), d


def kind_of(name, desc, yr):
    t = (name + " " + desc).lower()
    if re.search(r"reconstruct|ricostruz|plastico|model|maquette|gismondi", t):
        return "reconstruction"
    if re.search(r"\bplan\b|pianta|grundriss|floor plan|ground plan|forma urbis", t):
        return "plan"
    if re.search(r"coin|sestertius|denarius|aureus|medal", t):
        return "coin"
    if re.search(r"piranesi|vasi|engraving|etching|incisione|veduta|print", t):
        return "engraving"
    if re.search(r"painting|dipinto|oil on|canvas|panini|canaletto|fresco|watercolou?r|drawing|disegno", t):
        return "painting"
    if re.search(r"photograph|albumen|alinari|anderson|brogi|calotype|daguerre", t) and yr and yr < 1940:
        return "historic photograph"
    if yr and yr < 1900:
        return "artwork"
    return "photograph"


def score(f):
    t = (f["name"] + " " + f["desc"]).lower()
    s = 0.0
    for pat, w in HISTORIC:
        if re.search(pat, t):
            s += w
    if f["year"] and f["year"] < 1900:
        s += 3
    if f["lead"]:
        s += 2.5
    s += min(f["width"], 4000) / 4000  # bigger originals are usually better pictures
    return s


def fetch_city(city_id, only=None, force=False):
    city = json.load(open(os.path.join(ROOT, "content", "cities", city_id, "city.json")))
    srcs = {s["id"]: s for s in city["sources"]}
    out_dir = os.path.join(ROOT, "assets", "media", city_id)
    os.makedirs(out_dir, exist_ok=True)
    idx_path = os.path.join(out_dir, "index.json")
    index = json.load(open(idx_path)) if os.path.exists(idx_path) and not force else {}
    for l in city["landmarks"]:
        if only and l["id"] not in only:
            continue
        if l["id"] in index and not force and not only:
            continue
        wiki = next((srcs[i]["url"] for i in l["sourceIds"] if "wikipedia.org/wiki/" in srcs.get(i, {}).get("url", "")), None)
        if not wiki:
            continue
        title = urllib.parse.unquote(wiki.split("/wiki/")[1]).replace("_", " ")
        page = get({"action": "query", "titles": title, "prop": "images|pageimages", "imlimit": "200", "piprop": "name", "redirects": "1"})["query"]["pages"][0]
        lead = page.get("pageimage")
        names = [im["title"] for im in page.get("images", []) if not SKIP.search(im["title"])]
        files = []
        for k in range(0, len(names), 40):
            q = get({"action": "query", "titles": "|".join(names[k:k + 40]), "prop": "imageinfo", "iiprop": "url|size|mime|extmetadata", "iiurlwidth": str(WIDTH)})
            for p in q["query"]["pages"]:
                ii = (p.get("imageinfo") or [None])[0]
                if not ii or ii.get("mime") not in ("image/jpeg", "image/png", "image/tiff", "image/webp"):
                    continue
                meta = ii.get("extmetadata", {})
                lic = strip(meta.get("LicenseShortName", {}).get("value", ""))
                if meta.get("NonFree", {}).get("value") in ("true", True) or not FREE.search(lic):
                    continue
                if ii.get("width", 0) < 500 or ii.get("height", 0) < 300:
                    continue
                yr, date = year_of(meta)
                desc = strip(meta.get("ImageDescription", {}).get("value", ""))
                files.append({
                    "name": p["title"], "thumb": ii.get("thumburl"), "width": ii["width"], "height": ii["height"], "page": ii.get("descriptionurl"),
                    "desc": desc, "year": yr, "date": date, "license": lic, "licenseUrl": strip(meta.get("LicenseUrl", {}).get("value", "")) or None,
                    "artist": strip(meta.get("Artist", {}).get("value", ""), 90) or "Unknown", "lead": lead is not None and p["title"].replace("File:", "").replace(" ", "_") == lead,
                })
        files.sort(key=score, reverse=True)
        chosen, photos = [], 0
        for f in files:
            kind = kind_of(f["name"], f["desc"], f["year"])
            if kind == "photograph":
                if photos >= 2:
                    continue
                photos += 1
            f["kind"] = kind
            chosen.append(f)
            if len(chosen) >= MAX_PER:
                break
        items = []
        ldir = os.path.join(out_dir, l["id"])
        os.makedirs(ldir, exist_ok=True)
        for n, f in enumerate(chosen, 1):
            dst = os.path.join(ldir, f"{n}.jpg")
            data = fetch_bytes(f["thumb"])
            with open(dst, "wb") as fh:
                fh.write(data)
            shrink(dst)
            dims = subprocess.run(["sips", "-g", "pixelWidth", "-g", "pixelHeight", dst], capture_output=True, text=True).stdout
            w = int(re.search(r"pixelWidth: (\d+)", dims).group(1)); h = int(re.search(r"pixelHeight: (\d+)", dims).group(1))
            caption = re.sub(r"\s*-\s*Google Art Project\.?", "", strip(f["desc"], 220))
            if len(caption.split()) < 4 or re.fullmatch(r"[\w .-]*\d[\w .-]*", caption):
                # file-name-like descriptions say nothing: describe the picture instead
                who = f["artist"] if f["artist"] != "Unknown" else ""
                caption = f"{f['kind'].capitalize()}{' by ' + who if who else ''}{', ' + clean_date(f['date']) if f['date'] else ''}."
            items.append({"src": f"media/{city_id}/{l['id']}/{n}.jpg", "thumb": f"media/{city_id}/{l['id']}/t{n}.jpg", "w": w, "h": h, "kind": f["kind"], "caption": caption, "artist": f["artist"], "date": strip(clean_date(f["date"]), 40),
                          "license": f["license"], "licenseUrl": f["licenseUrl"], "page": f["page"]})
            time.sleep(1.5)
        index[l["id"]] = items
        json.dump(index, open(idx_path, "w"), indent=1, ensure_ascii=False)
        print(l["id"], len(files), "free ->", [i["kind"] for i in items], flush=True)
        time.sleep(0.5)
    return index


KIND_ORDER = ["engraving", "reconstruction", "plan", "artwork", "painting", "historic photograph", "photograph", "coin"]


def tidy(city_id):
    """Drop pictures that illustrate the whole city rather than the place (they turn up on many pages),
    keep upload timestamps out of the dates, describe pictures whose caption is in another script,
    and put drawings and prints of the building first."""
    idx_path = os.path.join(ROOT, "assets", "media", city_id, "index.json")
    index = json.load(open(idx_path))
    seen = {}
    for items in index.values():
        for it in items:
            seen[it["page"]] = seen.get(it["page"], 0) + 1
    for lid, items in index.items():
        keep = []
        for it in items:
            if seen[it["page"]] >= 3:
                continue
            d = it.get("date") or ""
            y = re.search(r"\b(1[0-9]{3}|20[0-9]{2})\b", d)
            if y and int(y.group(1)) >= 2000 and it["kind"] != "photograph":
                d = ""  # an upload date, not when the work was made
            d = re.sub(r"\s*\d{1,2}:\d{2}(:\d{2})?", "", d)
            d = re.sub(r"^(\d{4})-\d{2}-\d{2}$", r"\1", d.strip(" ,"))
            it["date"] = d
            generated = re.match(r"^(Engraving|Reconstruction|Plan|Artwork|Painting|Historic photograph|Photograph|Coin)( by [^,]*)?(, .*)?\.$", it["caption"])
            if generated or re.search(r"[\u0370-\u03ff\u0400-\u04ff\u0590-\u06ff\u3040-\u9fff]", it["caption"]) or len(it["caption"]) < 6:
                who = it["artist"] if it["artist"] != "Unknown" else ""
                it["caption"] = f"{it['kind'].capitalize()}{' by ' + who if who else ''}{', ' + d if d else ''}."
            keep.append(it)
        keep.sort(key=lambda it: KIND_ORDER.index(it["kind"]) if it["kind"] in KIND_ORDER else 9)
        index[lid] = keep
    json.dump(index, open(idx_path, "w"), indent=1, ensure_ascii=False)


def reshrink(city_id):
    """Re-encode every fetched picture and add thumbnails (for folders fetched before shrink() existed)."""
    out_dir = os.path.join(ROOT, "assets", "media", city_id)
    idx_path = os.path.join(out_dir, "index.json")
    index = json.load(open(idx_path))
    for lid, items in index.items():
        for it in items:
            dst = os.path.join(ROOT, "assets", it["src"])
            if not os.path.exists(dst):
                continue
            shrink(dst)
            dims = subprocess.run(["sips", "-g", "pixelWidth", "-g", "pixelHeight", dst], capture_output=True, text=True).stdout
            it["w"] = int(re.search(r"pixelWidth: (\d+)", dims).group(1)); it["h"] = int(re.search(r"pixelHeight: (\d+)", dims).group(1))
            it["thumb"] = it["src"].rsplit("/", 1)[0] + "/t" + it["src"].rsplit("/", 1)[1]
    json.dump(index, open(idx_path, "w"), indent=1, ensure_ascii=False)


if __name__ == "__main__":
    args = sys.argv[1:]
    if "--reshrink" in args:
        reshrink(args[0])
        sys.exit(0)
    if "--tidy" in args:
        tidy(args[0])
        sys.exit(0)
    city = args[0] if args and not args[0].startswith("--") else "rome"
    only = None
    if "--only" in args:
        only = set(args[args.index("--only") + 1].split(","))
    fetch_city(city, only, "--force" in args)
    tidy(city)
