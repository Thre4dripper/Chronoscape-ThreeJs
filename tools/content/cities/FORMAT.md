# A city pack: format and quality bar

Rome (`content/cities/rome/city.json`, built by `tools/content/build_rome.py`) is the
reference: 8 eras, 52 monuments with Blender miniatures, 52 spots of daily life,
34 events, 4 stories. Every other city is written as three plain Python data
modules plus one Blender module, and assembled by:

    python3 tools/content/build_city.py <id>      # writes content/cities/<id>/city.json
    pnpm validate                              # schema + cross-reference check (all cities)

| file | what |
| --- | --- |
| `tools/content/cities/<id>/geo.py` | `CITY`, `FRAME`, `PERIODS`, the map geography, `SOURCES` |
| `tools/content/cities/<id>/landmarks.py` | `LANDMARKS`, `SOURCES` |
| `tools/content/cities/<id>/life.py` | `SPOTS`, `EVENTS`, `STORIES`, `SOURCES` |
| `tools/blender/models/cities/<id>.py` | `BUILDERS = {"<id>/<model>": fn}` (one per model key used in landmarks.py) |

Modules are plain Python: literals, small helper lists like `ALL = [...]`, nothing
imported except `math`. Strings in double quotes, valid Python. All positions are
`(lat, lon)` tuples in decimal degrees (WGS84, as on OpenStreetMap / Wikipedia);
all sizes are metres. The build projects everything onto the map grid.

## geo.py

```python
CITY = dict(
    name="Delhi", subtitle="City of Cities",             # name as shown on the map cartouche
    description="One or two sentences: what span of history and which area this map covers. Positions are projected from real coordinates; the drawing is an illustration, not a survey.",
    defaultPeriodId="shahjahan-1660",                    # the era the atlas map opens at
    world=dict(heightScale=1.0, walls=["#E2CFAC", ...], roofs=["#C9B28C"]),   # all optional (scale defaults to 0.01)
    camera=dict(target=(28.656, 77.236), distance=38),   # where the camera starts (lat, lon)
)
FRAME = ((28.690, 77.190), (28.590, 77.270))   # map bounds: north-west corner, south-east corner
```

- Frame: about 4–7 km on a side (Rome: 6.0 × 5.4 km). It must hold every era's city
  with some countryside round it. Keep it roughly landscape (wider than tall) or square.
- `PALETTE = dict(parchment="#E6D3AA", ink="#6F4D34", water="#65888A", hill="#777D5A", road="#8A6A4A")` optional.
- `COMPASS = (lat, lon)`, `CARTOUCHE = (lat, lon)` (bottom-left corner of the title box) in empty corners.

### PERIODS (3 to 6 eras; pick the moments that changed the city most)

```python
PERIODS = [
    dict(id="sultanate-1325", label="Tughlaq Delhi", year=1325, startYear=1320, endYear=1413,
         summary="≤ 70 words: what the city was, who ruled, what it looked like, building materials.",
         population="perhaps 400,000",
         feel="One sensory sentence: sounds, smells, crowds.",
         style="courtyard",                                  # house-building tradition, see below
         houses=dict(title="Courtyard houses of Jahanpanah", text="≤ 50 words: what an ordinary dense block was here and now."),
         outskirts=dict(title="Gardens and villages", text="≤ 40 words: what a loose block was.")),
]
```

Period ids: `<short-name>-<year>` (`edo-1800`, `tang-750`, `bce` as `-450` → `classical-450bce`).
The atlas map's era (given in your brief) must be one of them.

`style` decides the generated houses (shape, roof, colour, window rhythm, text):
`antique` (Greco-Roman), `medieval` / `early-modern` (Italian), `gothic` (northern Europe),
`courtyard` (Islamic, Persian, Indian, Egyptian, Mesopotamian: flat roofs round courts),
`sinic` (Chinese walled wards), `japanese` (machiya), `mesoamerican`, `andean`, `sahel`,
`kraal` (round huts), `archaic` (wattle-and-daub hut villages). `houses` / `outskirts`
make the hover text specific to this city and era — always write them.

### Geography lists (each item may carry `periods=[...]`; omitted = every era)

```python
WATER = [dict(id="yamuna", name="Yamuna", path=[(lat, lon), ...], width=250, blurb="≤ 50 words")]   # rivers, canals (width = metres)
ISLANDS = [dict(name="...", polygon=[(lat, lon), ...])]          # land inside water
HILLS = [dict(id="ridge", name="The Ridge", center=(lat, lon), radius=300, blurb="...")]
ROADS = [dict(id="chandni-chowk", name="Chandni Chowk", path=[...], width=30, style="major", labelled=True, blurb="...", periods=[...])]
WALLS = [dict(id="...", name="...", path=[...], closed=True, blurb="...", periods=[...])]
GATES = [dict(id="...", name="Kashmiri Gate", position=(lat, lon), periods=[...])]
BRIDGES = [dict(id="...", name="...", path=[(lat, lon), (lat, lon)], build="stone"|"timber", arches=5, blurb="...", landmarkId=None, periods=[...])]   # across WATER
AQUEDUCTS = [dict(name="Nahr-i-Bihisht canal", path=[...], periods=[...])]   # aqueducts or raised canals
BLOCKS = [dict(name="Dariba", polygon=[...], density="dense"|"loose", periods=[...])]   # built-up areas, generated as houses
GARDENS = [dict(name="Begum Bagh", polygon=[...], kind="park"|"orchard"|"vineyard", periods=[...])]
MARSH = [dict(name="...", polygon=[...], periods=[...])]
DISTRICTS = [dict(id="...", name="...", polygon=[...], description="≤ 50 words", periods=[...])]
LABELS = [dict(text="Yamuna", position=(lat, lon), size="lg"|"md"|"sm", rotation=-80, periods=[...])]
```

- Coastline: the sea is drawn as a very wide `WATER` path along the shore (width 600–2000 m)
  or a lake as a wide path through its middle. Coastline accuracy matters more than street accuracy.
- Roads: 8–25, the real main streets and the roads out of the gates, per era. `width` 6–40 m.
- Blocks: the built-up area of each era as 5–20 polygons that do not cross the main roads
  or rivers (the generator keeps roads, water, walls and landmarks clear by itself, but a block
  that straddles a river wastes its area). Use `loose` for suburbs, villas, gardens, villages.
  Blocks are what makes the map look like a city: cover each era's real extent.
- Walls follow their real trace; `closed=True` for a full circuit.
- Name things in the period's own language/script transliterated where it helps (Tiberis / Tevere).

## landmarks.py (12–24 monuments; the city's famous buildings across its eras)

```python
LANDMARKS = [
    dict(id="red-fort", placeId="qila-mubarak", name="Red Fort (Qila-i-Mubarak)", category="military",
         latlon=(28.6562, 77.2410), rotation=0, footprint=(550, 950), scale=1.0, model="delhi/red-fort",
         activePeriods=["shahjahan-1660", "late-mughal-1800"],
         variants={
             "shahjahan-1660": dict(note="≤ 35 words: the building in this era"),
             "late-mughal-1800": dict(model="delhi/red-fort-1800", note="...", name="optional other name in this era", confidence="reconstruction"),
         },
         summary="One sentence ≤ 40 words.",
         details=["Paragraph ≤ 70 words: construction, form, history.", "Paragraph ≤ 70 words: what the miniature shows, what is simplified or uncertain."],
         built="1639–1648", function="Imperial palace-fortress", confidence="documented"|"reconstruction"|"interpretation",
         sourceIds=["wiki-red-fort", "koch-mughal"], activity=dict(figures=40, radius=300)),
]
```

- `category`: temple, civic, entertainment, religious, military, commercial, district, monument.
- `footprint` (w east–west, d north–south, metres, before rotation) must match the model.
  `rotation` in degrees clockwise seen from above. `scale` > 1 (up to 3) only to make a small
  monument readable (a 6 m stele, a column); big buildings stay at 1.
- `activePeriods`: every era in which it stands. Add a `variants` note for each of them, plus a note
  for the era just before it is built (what stood there) and just after it is gone, if those eras exist.
  A variant `model` when it looks clearly different (ruined, rebuilt, enlarged); each such key needs a builder.
- Sources: every landmark cites its English Wikipedia article as a source with the full URL
  (`dict(id="wiki-red-fort", title="Red Fort", author="Wikipedia", url="https://en.wikipedia.org/wiki/Red_Fort")`)
  — the picture fetcher uses it — plus a book or scholarly source where you know one.
- Positions to ~20 m: take them from your knowledge of the real coordinates. Do not let
  landmark footprints overlap each other or sit in the river.

## life.py

```python
SPOTS = [dict(id="ghantewala", name="Ghantewala Halwai", kind="shop", latlon=(lat, lon), activePeriods=[...],
              summary="≤ 35 words", details=["≤ 60 words"], confidence="documented", sourceIds=[...],
              vignettes=[dict(hour=6, text="≤ 35 words"), dict(hour=13, text="..."), dict(hour=21, text="...")],
              variants={"pid": dict(note="≤ 30 words", name="optional")})]
EVENTS = [dict(id="nadir-shah-1739", title="≤ 8 words", periodId="...", date="22 March 1739", kind="riot",
               at=dict(landmarkId="...") | dict(spotId="...") | dict(latlon=(lat, lon)), effect="fire"|"crowd"|"construction"|"procession"|"none",
               text="≤ 70 words: what happened, why it matters, one vivid detail", sourceIds=[...])]
STORIES = [dict(id="...", title="...", periodId="...", summary="≤ 40 words", sourceIds=[...],
                steps=[dict(landmarkId="..." or spotId="...", title="...", text="≤ 50 words", when="optional")])]   # 4–7 steps
```

- Spots (12–20): the small things — markets, shops, workshops, baths, inns, schools, shrines,
  wells, docks, caravanserais, houses — spread across eras and districts.
  `kind`: tavern, bakery, market, shop, workshop, house, inn, school, bath, shrine, fountain, works,
  dock, prison, civic, monument, garden, bank, church.
  Vignettes: dawn, midday, evening/night, concrete and sensory, grounded in sources (travellers'
  accounts, chronicles, archaeology). Second person is fine.
- Events (10–16) across all eras; `kind`: construction, festival, procession, riot, disaster, civic, ceremony, daily.
- Stories (1–3): a walk through one era, 4–7 steps, each at a landmark or spot.

Style: plain, vivid, specific. No "nestled", no marketing. Dates "52 BCE", "80 CE". Metres.
Mark uncertainty honestly ("probably", "the usual reconstruction"). Facts you are unsure of:
leave them out or hedge them.

## Blender models: tools/blender/models/cities/<id>.py

```python
"""<City> landmark miniatures."""
import math
from chronokit import Model, box, cylinder, dome, join, shade, gable_roof, hip_roof, steps, columns, mini_temple
from worldkit import *          # lathe, prism, frustum, rot, move, arch_panel, arcade, merlons, cornice, stair,
                                # onion_dome, shallow_dome, ribbed_dome, chhatri, minaret, iwan, jali_wall, courtyard_ring,
                                # mosque, tomb, charbagh, tree, stupa, shikhara_temple, wall_run, gatehouse,
                                # eaved_roof, east_asian_hall, pagoda, torii, castle_keep, gothic_church, campanile,
                                # domed_basilica, palazzo, pylon, hypostyle, ziggurat, apadana, glazed_gate, flat_house,
                                # step_pyramid, ballcourt, kancha, adobe_mosque, great_enclosure, stele + colour constants

def red_fort(variant="1660"):
    m = Model("red-fort")
    m.add(0, box("ground", 550, 950, 1, color=shade(RED_SANDSTONE, 0.3)), "walls")   # stage 0 rises first
    m.add(0, wall_run("walls", [(-275, -475), (275, -475), (275, 475), (-275, 475), (-275, -475)], 24, 9))
    m.add(1, gatehouse("lahori", 40, 28, 30, (-275, 0, 0), "W"), "gates")
    m.add(2, ..., "palaces")
    return m

BUILDERS = {"delhi/red-fort": red_fort, "delhi/red-fort-1800": lambda: red_fort("1800")}
```

Conventions (the app depends on them):
- Metres; origin at the ground centre of the footprint; +X east, +Y north, +Z up; nothing below z = 0
  except foundations hidden in the ground plate.
- The main facade faces south (−Y) in the builder; the landmark's `rotation` turns it on the map.
- The model's plan should fill its `footprint` (w along X, d along Y).
- `Model.add(stage, obj, label)`: stages 0, 1, 2 (…) rise one after another when the monument is
  revealed; 2–4 stages, foundations/walls first, roofs/domes/towers last.
- Flat colours only (hex or worldkit constants). Strong, legible silhouettes over fine detail:
  this is a painted miniature seen from 30–200 m. 2,000–40,000 faces per model.
- Openings are dark panels (`arch_panel`, `arcade`), not boolean holes.
- Use worldkit parts and add bespoke geometry for what makes each building recognisable (the
  Qutb Minar's flutes, the Hagia Sophia's buttresses, the Pantheon-like oculus). Read
  `tools/blender/models/worldkit.py` before starting; write helpers in your own module if you need
  new parts (do not edit worldkit.py, other cities depend on it).

Check your models by sketching them (fast, no baking; ~2 s per model):

    /Users/ijlalahmad/Applications/Blender.app/Contents/MacOS/Blender -b -P tools/blender/sketch.py -- <scratch_dir> <id>/

It prints one `SKETCH {...}` line per model (size, faces, errors) and writes a PNG per model; look
at a few with the Read tool and fix anything that looks wrong (floating parts, roofs through walls,
wrong proportions). Run only one Blender at a time and never open the Blender UI.

## Done means

1. `python3 tools/content/build_city.py <id>` prints the counts without errors.
2. `pnpm validate` reports 0 errors for your city (warnings about missing preview plates or
   the city not being listed in index.json are expected).
3. Every model key in landmarks.py (including variant models) has a builder, and the sketch run
   shows no errors.
4. Do not edit shared files: `content/atlases.json`, `content/cities/index.json`, anything in `src/`,
   worldkit.py, chronokit.py, build_city.py, other cities' files. Do not bake, commit, or start servers.

## Network etiquette

If you query Wikipedia or Commons (for example to check that an article exists), use the project's
User-Agent `Chronoscape/0.1 (educational map prototype)` and never put any personal data — names,
email addresses — in headers, URLs or payloads.
