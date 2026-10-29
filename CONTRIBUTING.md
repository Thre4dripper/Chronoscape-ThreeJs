# Contributing to Chronoscape

Thank you for helping. Chronoscape is an atlas people will read as true, so the most valuable contributions are often
the smallest: a wrong date, a monument on the wrong side of a river, a source that no longer resolves. Code, models and
new cities are welcome too.

By taking part you agree to the [Code of Conduct](CODE_OF_CONDUCT.md).

## Ways to help

| You want to… | Start here |
|---|---|
| Fix a historical error | Open a **Content correction** issue, or edit the city's sources (below) and open a pull request |
| Report a bug | Open a **Bug report** issue with the page address, browser and device |
| Suggest an idea | Open a **Feature request** issue |
| Add or extend a city | Read `tools/content/cities/FORMAT.md` and the "Adding a city" section of [docs/MVP.md](docs/MVP.md) first |
| Improve a 3D model | Edit its builder under `tools/blender/models/` |
| Report a security problem | Don't open an issue; see [SECURITY.md](SECURITY.md) |

## Setting up

You need Node.js 24, pnpm (the version is pinned in `package.json`, so `corepack enable` is enough) and Google Chrome
(the build bakes the map plates in headless Chrome). Python 3 is needed for content work, and Blender for models.

```bash
pnpm install
cp .env.example .env     # SITE_URL, used by the build
pnpm dev                 # http://localhost:5173
```

Before opening a pull request:

```bash
pnpm validate            # content and asset checks: 0 errors
pnpm typecheck
pnpm test
pnpm build               # optional locally; CI runs it on every pull request
```

## Content: history first

City packs are generated. Never edit `content/cities/<id>/city.json` by hand: change the sources and rebuild.

```
tools/content/cities/<id>/geo.py         geography: rivers, walls, roads, blocks (latitude/longitude and metres)
tools/content/cities/<id>/landmarks.py   monuments, their eras and texts
tools/content/cities/<id>/life.py        eras, daily-life spots, events, stories
```

```bash
python3 tools/content/build_city.py <id>     # Rome: python3 tools/content/build_rome.py
pnpm validate
```

Every text is held to `tools/content/cities/REVIEW.md`. In short:

- **Facts** (dates, rulers, names, numbers, attributions) must be right; where scholars disagree, say so
  ("probably", "the usual reconstruction") and set `confidence` honestly.
- **No anachronisms**: a monument appears only in the eras it actually stood (`activePeriods`).
- **No invented specifics** presented as fact. Vignettes may imagine a scene, but not invent records.
- **Sources** must be real: a real Wikipedia article, a real author and title.
- **Sensitive subjects** (slavery, sacrifice, massacres, religion) are stated factually and respectfully, with the
  debates acknowledged.
- **Writing** is plain and specific; British spelling is fine.

In a pull request that changes facts, cite your source for each change.

## Code

- TypeScript, React 19 and react-three-fiber. Match the style of the code around you: comment density, naming, idiom.
- The renderer is unlit by design: lighting is baked into models in Blender and the day is one tint (see
  `src/engine/render/baked.ts`). Keep draw calls and shader programs low; new materials should reuse `bakedMaterial`.
- Nothing on the map may overlap: fields, blocks, figures, labels and props respect each other's space
  (the fabric uses an occupancy grid).
- Map plates are build output (`.plate-cache/`, never committed). If you change how plates are drawn, bump
  `PLATE_VERSION` so every era is redrawn.

## 3D models

Each model is a Python script run in Blender, exported as a Draco GLB into `assets/models/`. Metres, origin at
ground centre, top-level parts `p0_…`, `p1_…`, `p2_…` for the staged reveal. No coplanar overlapping faces (they
flicker).

```bash
BAKE_CPU=1 Blender -b -P tools/blender/bake_all.py     # only what changed
```

Commit the builder script and the exported GLB together.

## Commits and pull requests

- One logical change per commit, with an imperative, sentence-case subject and no prefix:
  `Fix the Pons Aemilius's position on the Tiber`, not `fix: pons aemilius`. Explain the why in the body.
- Keep pull requests focused. Each one gets its own preview deployment; check your change there, and add a
  screenshot for anything visual.
- Never put personal data (names, emails, tokens) into code, content, headers or request user agents. Scripts that
  query Wikipedia use the agent `Chronoscape/0.1 (educational map prototype)`.

## Licence

By contributing, you agree that your code is licensed under the project's [MIT License](LICENSE) and your content
(texts, geography, maps and models) under [CC BY-NC 4.0](LICENSE-CONTENT).
Pictures you add must be freely licensed or public domain, with their artist, date, licence and source recorded.
