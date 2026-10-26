# Content review checklist

You are fact-checking city packs that were written quickly, mostly from memory. Readers will
take every sentence as true, so accuracy matters more than anything else. Work through each city's
`tools/content/cities/<id>/{geo,landmarks,life}.py` (Rome: `tools/content/rome/*.py` with
`tools/content/build_rome.py`), fix what is wrong in place, and rebuild.

Check, for every text (period summaries, houses/outskirts, blurbs, landmark summary/details/variant
notes/built/function, spot summaries/details/vignettes, events, story steps):

1. **Facts**: dates, rulers, dynasties, names, numbers (heights, populations, dimensions),
   attributions (who built what, who wrote what), sequence of events. Correct errors; where the
   scholarship is uncertain, say so ("probably", "traditionally", "the usual reconstruction"), and
   set `confidence` honestly (documented / reconstruction / interpretation).
2. **Anachronisms**: a building, person, object or custom described in an era where it did not yet
   or no longer exist. Each landmark's `activePeriods` must match when it actually stood; an event's
   date must fall within its era's `startYear`–`endYear` (fix the range or move the event).
3. **Invented specifics**: precise-sounding details with no basis (an exact number of shops, a quoted
   saying, a named person in a vignette presented as real). Soften them or remove them; vignettes
   may be imaginative scenes, but must not present inventions as recorded fact.
4. **Positions**: famous landmarks should be within ~50 m of their real coordinates. If one is clearly
   misplaced (wrong side of a river, inside another monument), fix `latlon` (keep `footprint` and
   `model` as they are, since the Blender model depends on them).
5. **Sources**: each landmark keeps a Wikipedia source whose URL is a real article (check the exact
   title; fix the URL or point to the nearest real article). Keep scholarly sources only when they
   exist (real author, real title).
6. **Writing**: plain and specific, British spelling is fine, no "nestled", no marketing words, no
   doubled sentences, word limits from FORMAT.md, sensitive topics (slavery, sacrifice, massacres,
   religion) stated factually and respectfully, with debates acknowledged.

Do not change ids, period ids, model keys, footprints or the Blender modules. Change geography
(`geo.py`) only to fix clear errors (a river on the wrong side, a wall through a monument), and say so
in your report because those cities' map plates must be redrawn.

If you query Wikipedia, use the User-Agent `Chronoscape/0.1 (educational map prototype)`, pace
requests (it rate-limits), and never send any personal data.

After each city: `python3 tools/content/build_city.py <id>` (Rome: `python3 tools/content/build_rome.py`)
and `npm run validate` must show 0 errors.

Report per city in a few lines: the corrections made (most important first), what remains
uncertain, and whether `geo.py` changed.
