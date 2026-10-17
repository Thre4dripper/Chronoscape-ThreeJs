import { AtlasCatalogSchema, CityIndexSchema, type AtlasCatalog, type CityIndex, type City } from "./schema";
import { validateCity } from "./validate";
import indexJson from "../../content/cities/index.json";
import atlasJson from "../../content/atlases.json";

/** City packs are code-split: a city's JSON is only fetched when selected. */
const packs = import.meta.glob("../../content/cities/*/city.json");

export const cityIndex: CityIndex = CityIndexSchema.parse(indexJson);
/** The map-room shelf: atlases of regions and ages, each holding city maps. */
export const atlasCatalog: AtlasCatalog = AtlasCatalogSchema.parse(atlasJson);

const cache = new Map<string, Promise<City>>();

export function loadCity(id: string): Promise<City> {
  let p = cache.get(id);
  if (!p) {
    p = (async () => {
      const key = Object.keys(packs).find((k) => k.endsWith(`/cities/${id}/city.json`));
      if (!key) throw new Error(`No content pack for city "${id}"`);
      const mod = (await packs[key]()) as { default: unknown };
      const { city, issues } = validateCity(mod.default);
      for (const i of issues) (i.level === "error" ? console.error : console.warn)(`[content:${id}] ${i.path}: ${i.message}`);
      if (!city) throw new Error(`City "${id}" failed validation`);
      return city;
    })();
    cache.set(id, p);
  }
  return p;
}
