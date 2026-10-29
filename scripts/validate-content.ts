/**
 * Build-time content validation: every city pack must parse, cross-reference
 * cleanly, and point at assets that exist. Run with `pnpm validate`.
 */
import { readFileSync, existsSync, readdirSync } from "node:fs";
import { join, resolve } from "node:path";
import { AtlasCatalogSchema, CityIndexSchema } from "../src/content/schema";
import { validateCity } from "../src/content/validate";

const root = resolve(import.meta.dirname, "..");
const citiesDir = join(root, "content", "cities");
const assetsDir = join(root, "assets");

let errors = 0;
let warnings = 0;

const index = CityIndexSchema.safeParse(JSON.parse(readFileSync(join(citiesDir, "index.json"), "utf8")));
if (!index.success) {
  console.error("index.json invalid:", index.error.issues);
  process.exit(1);
}
const listed = new Set(index.data.cities.map((c) => c.id));
const dirs = readdirSync(citiesDir, { withFileTypes: true })
  .filter((d) => d.isDirectory())
  .map((d) => d.name);
for (const d of dirs) if (!listed.has(d)) console.warn(`warn  content/cities/${d} exists but is not listed in index.json`), warnings++;
for (const id of listed) if (!dirs.includes(id)) console.error(`error index.json lists "${id}" but content/cities/${id}/ does not exist`), errors++;

for (const id of new Set([...listed, ...dirs])) {
  const file = join(citiesDir, id, "city.json");
  if (!existsSync(file)) {
    console.error(`error ${id}: missing city.json`);
    errors++;
    continue;
  }
  const raw = JSON.parse(readFileSync(file, "utf8"));
  const { city, issues } = validateCity(raw, { assetExists: (p) => existsSync(join(assetsDir, p)) });
  for (const i of issues) {
    const isMissingAsset = i.message.startsWith("missing asset");
    // A missing glb with a declared fallback kit is survivable; without one it is not.
    const level = isMissingAsset && hasFallback(raw, i.path) ? "warn" : i.level;
    if (level === "error") errors++;
    else warnings++;
    console[level === "error" ? "error" : "warn"](`${level.padEnd(5)} ${id}: ${i.path}: ${i.message}`);
  }
  if (city) {
    const glbs = city.landmarks.flatMap((l) => [l.model, ...Object.values(l.variants).map((v) => v.model)]).filter((m): m is { glb: string } => !!m && "glb" in m);
    console.log(`ok    ${id}: ${city.periods.length} periods, ${city.landmarks.length} landmarks, ${city.stories.length} stories, ${city.sources.length} sources, ${glbs.length} glb refs`);
  }
  if (city && city.id !== id) console.error(`error ${id}: city.id is "${city.id}"`), errors++;
}

// the map room: every playable map must open a real city at a real era
const cat = AtlasCatalogSchema.safeParse(JSON.parse(readFileSync(join(root, "content", "atlases.json"), "utf8")));
if (!cat.success) {
  console.error("atlases.json invalid:", cat.error.issues);
  errors++;
} else {
  const ids = new Set<string>();
  for (const a of cat.data.atlases) {
    if (ids.has(a.id)) console.error(`error atlases: duplicate id "${a.id}"`), errors++;
    ids.add(a.id);
    if (a.from >= a.to) console.error(`error atlases.${a.id}: from is not before to`), errors++;
    for (const m of a.maps) {
      if (!m.city) continue;
      if (!listed.has(m.city)) {
        console.error(`error atlases.${a.id}: map "${m.title}" opens unknown city "${m.city}"`), errors++;
        continue;
      }
      const raw = JSON.parse(readFileSync(join(citiesDir, m.city, "city.json"), "utf8"));
      if (m.period && !raw.periods.some((p: { id: string }) => p.id === m.period)) console.error(`error atlases.${a.id}: map "${m.title}" opens unknown era "${m.period}"`), errors++;
    }
  }
  console.log(`ok    atlases: ${cat.data.atlases.length} atlases, ${cat.data.atlases.reduce((n, a) => n + a.maps.filter((m) => m.city).length, 0)} playable maps`);
}

console.log(`\n${errors} error(s), ${warnings} warning(s)`);
process.exit(errors > 0 ? 1 : 0);

function hasFallback(raw: unknown, path: string): boolean {
  // path looks like "landmarks[3] (id).model" or "...variants.<pid>.model"
  const m = /^landmarks\[(\d+)\][^.]*\.(.*)$/.exec(path);
  if (!m) return false;
  const lm = (raw as { landmarks: Record<string, unknown>[] }).landmarks[Number(m[1])];
  const model = m[2].split(".").reduce<unknown>((o, k) => (o && typeof o === "object" ? (o as Record<string, unknown>)[k] : undefined), lm);
  return !!model && typeof model === "object" && "fallback" in (model as object);
}
