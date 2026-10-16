# Rome content: format for writers

Each file is a plain Python module of literals (no imports, no code). The build
script `tools/content/build_rome.py` turns them into `content/cities/rome/city.json`.

**Do not change** any of these fixed fields: `id`, `placeId`, `latlon`, `rotation`,
`footprint`, `scale`, `model`, `activePeriods`, `kind`, `periodId`, `at`, `date`,
and the `model` keys inside `variants`. Fill the empty strings / lists.

## Period ids (fixed)

| id | label | year | range |
| --- | --- | --- | --- |
| kingdom-600bce | Regal Rome | -600 | 753–509 BCE |
| republic-200bce | Middle Republic | -200 | 508–134 BCE |
| republic-50bce | Late Republic | -50 | 133–27 BCE |
| empire-100ce | High Empire | 100 | 27 BCE–192 CE |
| empire-215ce | Severan Rome | 215 | 193–284 CE |
| late-400ce | Late Antiquity | 400 | 285–476 CE |
| medieval-1300 | Medieval Rome | 1300 | 477–1420 |
| renaissance-1560 | Renaissance Rome | 1560 | 1421–1600 |

## Landmark fields to fill

- `summary`: one sentence, ≤ 40 words, what it is and why it matters.
- `details`: 2 short paragraphs (≤ 70 words each): 1) construction/form/history, 2) what the miniature shows and what is simplified or uncertain.
- `built`: short phrase ("Dedicated 509 BCE; rebuilt 69 BCE, 80s CE").
- `function`: short phrase.
- `confidence`: "documented" | "reconstruction" | "interpretation" (overall).
- `sourceIds`: 2–4 ids from the SOURCES list in the same file (add sources as needed; Wikipedia URLs are fine, plus standard references such as Claridge, Coarelli, Platner & Ashby, Krautheimer, Richardson).
- `variants`: for every period in `activePeriods`, a `note` (≤ 35 words) saying what the building was like *in that period*. Also add notes for the period just before it first appears (what stood there) and the first period after it disappears (what happened to it). Add `name` where the name changed (e.g. church names), `confidence` where it differs from the overall value. Keep every `model` key exactly as given; add `note`/`name`/`confidence` next to it.
- `activity`: leave as given.

## Spot fields to fill (small things: shops, workshops, markets, streets, daily life)

- `summary` (≤ 35 words), `details` (1–2 paragraphs ≤ 60 words), `confidence`, `sourceIds`.
- `vignettes`: 3 entries `{hour: int 0–23, text: ≤ 35 words}` describing what is happening there at that hour of a typical day (dawn, midday, evening/night). Concrete, sensory, grounded in evidence (Martial, Juvenal, Pompeian parallels, medieval statutes, travellers' accounts).
- `variants`: per period in `activePeriods`, an optional `note` (≤ 30 words) if it changed.

## Event fields to fill

- `title` (≤ 8 words), `text` (≤ 70 words: what happened, why it matters, one vivid detail), `sourceIds`.
- `effect`: one of "fire", "crowd", "construction", "procession", "none" (fixed where already set).

## Style

- Plain, vivid, specific. No "nestled", no marketing. Second-person is fine in vignettes ("you smell...").
- Dates: "52 BCE", "80 CE". Metres. Name the ancient sources inline where it helps ("Martial complains...").
- Mark uncertainty honestly in the text ("probably", "the usual reconstruction").
- Write valid Python literals: double-quoted strings, escape internal quotes, no trailing commas problems. Check with `python3 -c "import ast,sys; ast.parse(open('FILE').read())"`.
