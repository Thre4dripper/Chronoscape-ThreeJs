"""
Historic city views for the map room's walls: public-domain prints and
paintings from Wikimedia Commons (woodcuts from the Nuremberg Chronicle,
bird's-eye views, aquatints, ukiyo-e). Each picture is searched for, checked
for a free licence and a decent size, downscaled and saved under
assets/room/portraits/ with a manifest of credits.

    python3 tools/content/fetch_portraits.py
"""
import json, os, re, ssl, subprocess, sys, time, urllib.error, urllib.parse, urllib.request

ROOT = os.path.dirname(os.path.dirname(os.path.dirname(os.path.abspath(__file__))))
OUT = os.path.join(ROOT, "assets", "room", "portraits")
UA = "Chronoscape/0.1 (educational map prototype; offline asset build)"
API = "https://commons.wikimedia.org/w/api.php"
CTX = ssl.create_default_context(cafile="/etc/ssl/cert.pem") if os.path.exists("/etc/ssl/cert.pem") else ssl.create_default_context()

# id, caption, opens (atlas id, map title), search queries in order of preference
WANTED = [
    ("rome", "Rome, from the Nuremberg Chronicle, 1493", ("classical-mediterranean", "Rome"), ["Nuremberg chronicles Roma", "Schedelsche Weltchronik Rom", "Roma Nuremberg Chronicle woodcut"]),
    ("venice", "Venice, after Jacopo de' Barbari, 1500", ("medieval-europe", "Venice"), ["Jacopo de' Barbari view of Venice", "de Barbari Venetie MD"]),
    ("constantinople", "Constantinople, Braun and Hogenberg, 1572", ("medieval-europe", "Constantinople"), ["Braun Hogenberg Constantinopolis", "Civitates orbis terrarum Constantinopolis", "Byzantium Constantinopolis Braun"]),
    ("tenochtitlan", "Tenochtitlan, the Nuremberg map of 1524", ("americas", "Tenochtitlan"), ["Nuremberg map Tenochtitlan 1524", "Tenochtitlan 1524 map"]),
    ("delhi", "The Jama Masjid, Delhi, Thomas Daniell, 1795", ("mughal-india", "Delhi"), ["Daniell Jama Masjid Delhi", "Thomas Daniell Delhi aquatint", "Jumma Musjid Delhi Daniell"]),
    ("edo", "Nihonbashi, Edo, Hiroshige, 1833", ("japan", "Edo"), ["Hiroshige Nihonbashi morning", "Hiroshige Nihonbashi 53 stations", "Hiroshige Edo Nihonbashi"]),
]

FREE = re.compile(r"(public domain|^pd\b|cc0|cc[ -]by)", re.I)


def get(params):
    params = {**params, "format": "json", "formatversion": "2"}
    req = urllib.request.Request(API + "?" + urllib.parse.urlencode(params), headers={"User-Agent": UA})
    for attempt in range(6):
        try:
            with urllib.request.urlopen(req, timeout=30, context=CTX) as r:
                return json.load(r)
        except urllib.error.HTTPError as e:
            if e.code not in (429, 503):
                raise
            time.sleep(float(e.headers.get("Retry-After") or 0) or 5 * (attempt + 1))
    raise RuntimeError("rate limited")


def fetch(url):
    req = urllib.request.Request(url, headers={"User-Agent": UA})
    for attempt in range(6):
        try:
            with urllib.request.urlopen(req, timeout=60, context=CTX) as r:
                return r.read()
        except urllib.error.HTTPError as e:
            if e.code not in (429, 503):
                raise
            time.sleep(float(e.headers.get("Retry-After") or 0) or 5 * (attempt + 1))
    raise RuntimeError("rate limited")


def strip(s):
    return re.sub(r"\s+", " ", re.sub(r"<[^>]+>", "", s or "")).strip()


def find(queries):
    for q in queries:
        res = get({"action": "query", "list": "search", "srsearch": q, "srnamespace": "6", "srlimit": "12"})
        titles = [h["title"] for h in res["query"]["search"] if re.search(r"\.(jpe?g|png|tiff?)$", h["title"], re.I)]
        if not titles:
            continue
        info = get({"action": "query", "titles": "|".join(titles), "prop": "imageinfo", "iiprop": "url|size|extmetadata", "iiurlwidth": "900"})
        pages = {p["title"]: p for p in info["query"]["pages"]}
        for t in titles:
            ii = (pages.get(t, {}).get("imageinfo") or [None])[0]
            if not ii or ii.get("width", 0) < 800:
                continue
            meta = ii.get("extmetadata", {})
            lic = strip(meta.get("LicenseShortName", {}).get("value", ""))
            if not FREE.search(lic):
                continue
            return {"title": t, "thumb": ii["thumburl"], "page": ii["descriptionurl"], "license": lic, "artist": strip(meta.get("Artist", {}).get("value", ""))[:90] or "Unknown", "query": q}
        time.sleep(1)
    return None


def main():
    os.makedirs(OUT, exist_ok=True)
    manifest = []
    for pid, caption, (atlas, mapTitle), queries in WANTED:
        hit = find(queries)
        if not hit:
            print("no picture for", pid, flush=True)
            continue
        dst = os.path.join(OUT, f"{pid}.jpg")
        open(dst, "wb").write(fetch(hit["thumb"]))
        subprocess.run(["sips", "-s", "format", "jpeg", "-s", "formatOptions", "70", "-Z", "720", dst, "--out", dst], capture_output=True)
        dims = subprocess.run(["sips", "-g", "pixelWidth", "-g", "pixelHeight", dst], capture_output=True, text=True).stdout
        w = int(re.search(r"pixelWidth: (\d+)", dims).group(1)); h = int(re.search(r"pixelHeight: (\d+)", dims).group(1))
        manifest.append({"id": pid, "src": f"room/portraits/{pid}.jpg", "w": w, "h": h, "caption": caption, "atlas": atlas, "map": mapTitle, "artist": hit["artist"], "license": hit["license"], "page": hit["page"], "file": hit["title"]})
        print(pid, "->", hit["title"], w, h, hit["license"], flush=True)
        time.sleep(1.5)
    json.dump(manifest, open(os.path.join(OUT, "manifest.json"), "w"), indent=1, ensure_ascii=False)


if __name__ == "__main__":
    main()
