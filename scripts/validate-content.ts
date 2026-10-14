/**
 * Build-time content validation: every city pack must parse, cross-reference
 * cleanly, and point at assets that exist. Run with `npm run validate`.
 */
import { readFileSync, existsSync, readdirSync } from "node:fs";
import { join, resolve } from "node:path";
import { CityIndexSchema } from "../src/content/schema";
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

for (const id of listed) {
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
