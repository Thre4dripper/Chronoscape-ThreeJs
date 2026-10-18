# Chronoscape MVP — what it is and how it is built

> Rendering rebuilt (27 Oct 2026): procedural urban fabric (about 50,000 buildings in imperial Rome) drawn as an engraved Nolli-style plan and raised as an instanced miniature city; sharp close-up map tiles that follow the camera; decluttered labels; stable shadows; no z-fighting.
>
> Updated for the Rome expansion: 8 eras, 52 monuments, 52 places of daily life,
> 34 events, 4 stories, period-aware map, day clock. See VISION.md for what is next.

The MVP proves the one thing the blueprint says everything else depends on: an
illustrated map that turns into a miniature 3D reconstruction, driven entirely by
content so that a second city needs no renderer changes.

## The idea in one paragraph

A parchment atlas plate fills the screen. Landmarks sit on it as faint embossed
footprints. Hover one and a clay-style miniature rises out of the paper in stages
(podium, columns, roof). Click and the camera glides in, tiny figures start to
move around it, and a panel explains what it was, when, how sure we are, and where
that knowledge comes from. A timeline switches the period: buildings that did not
exist yet sink back into the paper, rebuilt ones swap models, and a card explains
every change instead of silently substituting. A story walks the camera through
several places with sourced narration. Switch city and the same engine unrolls a
different plate: Mughal Delhi, with its own river, walls, palette and miniatures.

## What is in the MVP

| Area | Delivered |
| --- | --- |
| Map | 4096 px parchment plate drawn per period from vector data projected from real coordinates: hills, river with boats, island, walls with towers, gates, bridges, aqueduct arcades, built-up blocks, gardens, marsh, districts, street names, cartouche, scale bar. Roads, districts, hills, walls and the river are hoverable. |
| Landmarks | 52 Roman landmarks with 118 period variants (118 GLB miniatures built in Blender from `tools/blender/`), plus 3 in Delhi. Procedural kits remain as fallbacks. |
| Small things | 52 spots (taverns, bakeries, workshops, markets, prisons, guild streets, the Ghetto, lime-burners, floating mills) with three hourly vignettes each, shown as markers and revealed by hovering their district. |
| Events | 34 dated events across the eras, listed in the era panel and marked on the map; fire events smoke, crowd events swell the figures. |
| Day clock | Hour slider drives sun and sky, crowd density and which vignette a spot shows. |
| Interaction | Explicit state machine: exploring → previewing → focused → immersed. Hover reveal, click to focus, Esc unwinds one layer, camera pose restored on exit. Every animation is damped toward a goal, so it is interruptible by construction. |
| Time | Rome: 600 BCE, 200 BCE, 50 BCE, 100 CE, 215 CE, 400 CE, 1300, 1560. Delhi: 1648 / 1660. The map itself is period-aware (walls, marsh, vineyards, labels, streets) and crossfades. Period variants per landmark; a "what changed" card on every switch. |
| Stories | One multi-stop story per city with per-step sources. |
| History | Every landmark has a confidence label (documented / reconstruction / interpretation), period notes and source references, shown in the panel. |
| Platform | City registry + lazy pack loading; zod schema; cross-reference validator (`npm run validate`) that fails the build on bad references or missing assets; vitest suites for content, coordinates and the state machine. |
| Input | Mouse (drag, wheel zoom-to-cursor, right-drag orbit), touch (pan, pinch, tap-to-preview then tap-to-enter), keyboard (arrows, +/-, Q/E, Esc), reduced-motion respected. |

## What is deliberately not in the MVP

- Photorealism, textures, baked lighting. The look is a crafted miniature.
- Audio, character animation beyond wandering figures, interior scenes.
- A backend, accounts, saved journeys, CMS.
- Level-of-detail switching and asset unloading (models are small enough for now).
- Geographic accuracy. Maps are illustrative; positions are approximate.

## Performance architecture (27 Oct 2026)

Measured on the production build in headless Chrome (software GPU, so real hardware is faster). On the Metal GPU (Apple M5 Max) the map is visible in 0.27 s and hovering or focusing a monument, raising blocks and street life all hold 60 fps with no long tasks.

| | before | after |
| --- | --- | --- |
| downloaded at load | 45 MB | 2.6 MB |
| map visible | 11.5 s | 0.5 s |
| era switch (preview / full) | 3.9 s | 0.07 / 0.18 s |
| zoom stall | 2.1 s | none |
| first hover / click stall | 3.1 s | none |

- **Baked map plates.** `npm run plates:bake` renders each era's whole-city plate (and a 1024 px preview) to `assets/plates/<city>/`. The app shows the preview at once and swaps in the full plate; neighbouring eras are prefetched while idle. A content hash in the manifest detects stale bakes, and the app then draws in a worker instead.
- **Worker drawing.** Close-up tiles are drawn in `plate.worker.ts` with OffscreenCanvas, only once the camera has settled. Nothing is drawn on the main thread.
- **3D only on hover.** Landmark models are fetched when hovered (Draco-compressed, decoder self-hosted in `assets/draco/`) and released when they sink. Nothing 3D is loaded at start.
- **Unlit, baked rendering.** No lights and no shadow maps. Landmarks and props are clean miniatures: flat material colours with ambient occlusion baked into the vertices in Blender (`bake_vc` in `tools/blender/bake_assets.py`), no textures, so they stay crisp at any zoom (all 128 models: 8.5 MB). The fixed sun comes from face normals in a tiny shader (`src/engine/render/baked.ts`), and ink lines on the creases are computed in a worker (`src/engine/render/ink.worker.ts`) so a 200k-triangle monument never stalls a hover. The day clock is one tint uniform. Shadows are baked decals (`assets/models/shadows/`), masked to the model's own footprint and faded out as soon as a model starts to sink.
- **Shader warm-up.** Every program is compiled in the background with `compileAsync` right after the map appears, so the first hover never stalls.
- **Overlay.** Labels are measured lazily in one read pass; the tooltip moves without React renders.

## Detailed monuments

`tools/blender/models/archkit.py` is an architectural kit (orders with bases and capitals, entablatures with dentils, pediments with statues, tiled roofs, arcade bays with engaged columns, thermal windows, stepped domes). `rome_hero.py` and `rome_hero2.py` build the hero monuments with it: Colosseum, the three imperial baths, Pantheon, temples, Circus Maximus, triumphal arches, Basilica of Maxentius, theatres, mausolea, Castel Sant'Angelo, Christian basilicas, Stadium of Domitian, Curia, the Forum. `tools/blender/bake_all.py` bakes everything the content references (Cycles on the GPU, denoised, Draco), then re-renders the map plans. The older texture bake (`bake`) is kept but no longer used: one atlas over a 200 m monument blurred at close range.

## The Codex and the map hunt (left side)

- **Codex** (`src/ui/Codex.tsx`, data in `src/engine/codex.ts`): opens on the left whenever a monument is focused, directly or through an event held there. Four tabs:
  - **Pictures:** freely licensed images from each landmark's Wikipedia article on Wikimedia Commons, such as Piranesi and Vasi etchings, Panini paintings, plans, reconstructions and a few photographs. Each one credits its artist and licence and links back to its Commons page. They are fetched by `tools/content/fetch_media.py` into `assets/media/<city>/` with an `index.json` (rate-limit aware; `--tidy` drops city-wide maps and upload dates; `--reshrink` re-encodes and makes thumbnails). Loaded only when the tab opens.
  - **Drawings:** a front elevation rendered from the model (`tools/blender/render_elevations.py`) with dimension lines, a scale bar and a 1.75 m figure, the plan cropped to the building, and the numbers (footprint, height in storeys, area in football pitches).
  - **Ages:** a timeline of every era. It shows what stood there, the era note, and an elevation of each different model, so the drawings show how the building changed. A click switches the era.
  - **Quiz:** questions generated from the content (date begun, purpose, later name or first era, size), with explanations.
- **Map hunt** (Quaestio, under the Codex): a riddle from a landmark's function with its name masked; you answer by clicking the building on the map. A wrong click gets a direction ("about 600 m north-east of it") and there is a hint. Scores are kept in this browser only.
- **Overlaps:** labels and tooltips keep clear of every panel (`aside`, `[data-hud-block]`); the focused label steps aside rather than hiding.

## No overlaps on the map (`fabric.ts`, `geom.ts`)

- An occupancy raster per era (`OccGrid`, 4 m cells, layers for buildings, ways, water and land) records what is built.
- Fields and vineyards are clipped to open land with exact geometry near obstacles (`clipParcel`), so their edges stay straight along roads and never cover houses or monuments.
- City blocks never overlap one another (separating-axis test).
- Hillside trees, figures around a monument and life scenes all check the raster before they are placed.
- Street life walks in lanes inside the drawn street. Each direction keeps to its own side at one speed and spacing, carts take the outer lane, and figures shrink in narrow alleys and vanish where a street passes under a building.
- Every era's fabric is built in a worker after load (`fabric.worker.ts`), so era switches never wait for it.

## Title page, map room and map case (navigation)

- **Title page** (`src/ui/title/`): a frontispiece over an engraved world chart that drifts east (drag it; it eases back to its own pace; every atlas city has a town mark that raises an engraved drawing of the place on hover, `src/world/glyphs.ts`) (Natural Earth coastlines from `scripts/build-world.mjs`, drawn once to a canvas), with ships, a sea serpent and compass roses, four "how it works" medallions, and a procession of twelve cartoon travellers, one per atlas (Blender walk cycles from `tools/blender/procession.py`, rendered as hand-tinted engraving sprite sheets in `assets/title/procession/`). All twelve walk at one pace on one loop, spaced by their own width, so none ever overlap. No three.js is loaded for this page; it warms the map room's code while idle.
- **Map room** (`src/ui/room/`): a toon-shaded library corner with ink outlines. It holds a map cabinet with one pigeonhole per atlas, a globe on a desk that turns to the region in focus, a light shaft and floating dust. Hover a bundle and it slides out while a label describes the atlas; click it and the atlas is held up to the viewer beside a card listing its maps, folded. An era ruler underneath shows each atlas's centuries in non-overlapping lanes and hovers in step with the shelf. The camera measures the heading, label and ruler and fits the scene into the space left.
- **Map room furniture** (`src/ui/room/`): a carved walnut library press (`Cabinet.tsx`) with fluted pilasters, arched niches, dentil cornice, swan-neck pediment, scroll cartouche, urns and a turning armillary sphere. The fixed carving is merged into one mesh per colour, and no faces are coplanar, so it does not flicker. Interactive pieces:
  - **The atlas, held:** it leans toward the pointer and its towns answer on the cover. Clicking breaks the wax seal, the ribbon slips off and the cover opens like a book onto an index of maps (`pages.ts`), with a marbled endpaper and bookplate inside the board.
  - **Drawers:** the ready-maps drawer pulls out and its maps rise to be clicked; the instruments drawer holds dividers, a compass with a swinging needle, and a reading glass.
  - **The globe** (`Globe.tsx`): a turned pedestal and a brass meridian with the axis tilted. Drag it to spin; point at a town to read it, click to open its atlas.
  - **City views on the wall** (`Portraits.tsx`): public-domain prints from Wikimedia Commons, fetched by `tools/content/fetch_portraits.py` with credits in their manifest. They hang on cords, swing when touched, and open their atlas.
  - **The desk** (`Desk.tsx`): an oil lamp that turns the room to evening, and a visitors' register (`Register.tsx`) with your travels, laurels and a curiosity from the atlases.
- **Atlases** live in `content/atlases.json` (schema `AtlasCatalogSchema`). Each holds a region outline, an era span, colours and maps. A map with `city` and `period` opens a city pack. A map without one shows "In preparation" with an engraved snippet of its region, so new cities are added by writing the pack and filling in those two fields. `npm run validate` and `tests/atlases.test.ts` check that every playable map points at a real city, era and baked preview plate.
- **Unfolding** (`src/ui/Flight.tsx`): the clicked packet flies to the centre, opens along its fold, opens its accordion folds column by column and grows to fill the screen. The city pack loads during the flight and only replaces what is behind once the map covers the screen. The map then waits for the city's first plate before fading into it. Leaving a city plays the same flight backwards into the atlas card.
- **Map case** (`src/ui/MapCase.tsx`): the drawer in a city that replaces the old city dropdown. It lists every map, folded, with the ready ones first and "You are here" on the current one. It can open any map, turn the same city to another era, or go back to the room or the title page.
- **Addresses**: `/` is the title page, `?room` the map room, `?room=<atlas>` an open atlas, and `?city=…&period=…` a city (old deep links still work). The browser's back and forward buttons follow (`src/nav.ts`).

## Rendering notes

- **Map plate** (`src/engine/map/plate.ts`) is drawn in map units, so the same code renders the whole-city texture (4096 px per era) and close-up tiles (2048 px around the camera, redrawn when the camera settles, faded in over the base).
- **Urban fabric** (`src/engine/map/fabric.ts`) is generated per era from block, garden and road polygons: insulae split into lots, courtyards, medieval towers, Renaissance palazzi, villas, fields, vineyards and trees. Deterministic, under 50 ms per era.
- **2D by default.** The plate is the map. At close zoom every tiled roof is drawn as shaded facets lit from the north-west; flat roofs are hatched; Regal-era villages are drawn as thatched huts.
- **Hover to raise** (`src/engine/map/HoverMassing.tsx`, `massingKit.ts`): the city block under the pointer and its neighbours rise as warm painted miniatures (plaster and brick walls, low terracotta roofs, arched shopfronts, small Roman windows, inked edges). Heights follow a storey mix per era (`PARAMS.mix` in `fabric.ts`): ancient Rome is mostly two and three storeys with a few four- and five-storey insulae under Augustus' 20 m cap; a city pack can scale all heights with `world.heightScale`, so the tall-block kit stays available for other cities. Real variety per era: tiled hip roofs or roof terraces with parapets and rooftop rooms, setback attic storeys, jettied medieval upper floors, crenellated towers, chimneys, Renaissance cornices and altane, shop awnings and timber balconies on the street side, and window grids and shop openings drawn by the shader. Archaic Rome rises as thatched huts.
- **Walls and aqueducts** rise as real Blender bays laid along the line (`InstancedGlb.tsx`): arcaded aqueduct arches with the water channel, crenellated wall bays, towers every 30 m, a double-arched gatehouse at gates.
- **Monuments stand out**: on the map their plans are warm-tinted, set in a cleared paper margin with a cast shadow and an inked double border; in 3D every landmark model carries crisp edge lines.
- **Landmark plans come from the models.** `tools/blender/render_plans.py` renders a sepia top-down plan of every landmark model; the map prints those plans, and content footprints are taken from the model extents, so the drawing and the 3D that rises from it are the same building.
- **Whole-area popouts** (`src/engine/map/AreaPopout.tsx`): hover a field, pasture, vineyard, orchard, park or marsh and the entire parcel rises along its exact boundary, planted and populated (plough teams, flocks, vine rows, trees, reeds).
- **Line popouts** (`src/engine/map/LinePopout.tsx`): a stretch of wall with towers and crenellations, gatehouses, aqueduct arcades, boats working the river, trees and goats on hill slopes, and every bridge: stone arch spans with cutwaters, or timber pile bays for the Pons Sublicius. Bridges with their own detailed model (Fabricius, Aemilius, Aelius, Sisto) raise that landmark instead.
- **Street life** (`src/engine/map/StreetLife.tsx`): hover a street, or a block (its street or the lane along its front), and that stretch fills with Blender miniatures moving along it: townsmen, women with baskets, porters with amphorae, a pack mule, a handcart, a litter with four bearers, and fruit, pottery and cloth stalls on the kerbs. Fewer people and no stalls at night. One instanced mesh per kind, about ten draw calls.
- **Life scenes** (`src/engine/map/LifeProps.tsx`, Blender `tools/blender/models/props.py`): a forge with a swinging hammer and smoke for workshops, an oven and donkey mill for bakeries, stalls, porters' carts, a ploughing team or shepherd in hovered fields.
- **Labels, spots and events** are one DOM overlay placed by a per-frame declutter pass (`src/engine/overlay/`), rounded to whole pixels with fixed z-order.
- **No flicker**: map layers sit at y = 0 with polygon offset; the camera's near/far planes follow the zoom; the shadow camera follows the view in quantised sizes and is snapped to shadow-map texels.

## How it fits together

```
content/cities/<id>/city.json   ← the only thing that differs between cities
        │  zod schema + validator (src/content)
        ▼
src/engine/store.ts              ← interaction state machine (zustand)
src/engine/Scene.tsx             ← map + landmarks + labels + figures + camera
   map/parchment.ts              ← draws the plate from city.map
   landmarks/Landmark.tsx        ← hover/click, emergence progress
   landmarks/GlbModel.tsx        ← loads assets/models/*.glb, splits reveal stages by name prefix p0_/p1_/p2_
   landmarks/kits/               ← procedural fallbacks (temple, amphitheater, circus, hall, cluster, arch, fort, mosque, street)
   camera/CameraRig.tsx          ← damped goal-pose rig, input handling
src/ui/*                         ← HUD, timeline, landmark panel, story bar, change card
tools/blender/                   ← bpy scripts that build and export every miniature
```

Coordinates: content positions are map units (metres on the plate, origin
top-left, y down). `src/engine/coords.ts` converts to world units with
`world.scale`. Models are authored in metres with the origin at ground centre, so
one `scale` number per landmark exaggerates small monuments for readability.

## Adding a city (content only)

1. Create `content/cities/<id>/city.json` following `src/content/schema.ts`
   (map vectors, periods, landmarks, stories, sources) and list it in
   `content/cities/index.json`.
2. Either reference procedural kits in `model`, or build miniatures in Blender:
   add builders to `tools/blender/models/<id>.py`, run `npm run assets:build`
   (or build in a live Blender session), which exports to `assets/models/<id>/`.
3. `npm run validate` must pass. `npm test` checks every pack.

No renderer code changes are required. Delhi was added this way to prove it.

## Next steps (in order)

1. **Polish the reveal**: per-stage easing curves, dust/paper-lift effect, label
   choreography.
2. **Interior scene for the Curia** to test the "immersed" state with a real
   interior rather than wandering figures.
3. **LOD + unloading**: dispose GLBs for non-active periods, lower-poly proxies at
   city zoom.
4. **Historical review pass** with a specialist on every note and confidence label.
5. **Second Roman period content**: 50 BCE Forum variants beyond the current
   simplified set.
6. **Device matrix + performance measurements** (the blueprint's P4 targets).
