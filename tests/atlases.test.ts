import { describe, it, expect } from "vitest";
import { readFileSync, existsSync } from "node:fs";
import { join, resolve } from "node:path";
import { AtlasCatalogSchema, CityIndexSchema } from "../src/content/schema";
import { yearU } from "../src/ui/room/EraRuler";

const root = resolve(__dirname, "..");
const catalog = AtlasCatalogSchema.parse(JSON.parse(readFileSync(join(root, "content", "atlases.json"), "utf8")));
const index = CityIndexSchema.parse(JSON.parse(readFileSync(join(root, "content", "cities", "index.json"), "utf8")));

describe("the map room's atlases", () => {
  it("open real cities at real eras, with a baked preview to fold", () => {
    for (const a of catalog.atlases)
      for (const m of a.maps.filter((x) => x.city)) {
        expect(index.cities.map((c) => c.id)).toContain(m.city);
        const city = JSON.parse(readFileSync(join(root, "content", "cities", m.city!, "city.json"), "utf8"));
        expect(city.periods.map((p: { id: string }) => p.id)).toContain(m.period);
        expect(existsSync(join(root, "assets", "plates", m.city!, `${m.period}.preview.webp`))).toBe(true);
      }
  });

  it("have unique ids, sensible spans, and cities inside their own region's bounds", () => {
    expect(new Set(catalog.atlases.map((a) => a.id)).size).toBe(catalog.atlases.length);
    for (const a of catalog.atlases) {
      expect(a.from).toBeLessThan(a.to);
      const lons = a.area.map((p) => p[0]), lats = a.area.map((p) => p[1]);
      for (const m of a.maps) {
        expect(m.at[0]).toBeGreaterThanOrEqual(Math.min(...lons) - 6);
        expect(m.at[0]).toBeLessThanOrEqual(Math.max(...lons) + 6);
        expect(m.at[1]).toBeGreaterThanOrEqual(Math.min(...lats) - 6);
        expect(m.at[1]).toBeLessThanOrEqual(Math.max(...lats) + 6);
      }
    }
  });

  it("lay the era ruler out monotonically, inside 0..1", () => {
    let last = -1;
    for (let y = -3000; y <= 1900; y += 50) {
      const u = yearU(y);
      expect(u).toBeGreaterThan(last);
      expect(u).toBeGreaterThanOrEqual(0);
      expect(u).toBeLessThanOrEqual(1);
      last = u;
    }
  });

  it("every atlas has at least one ready map, or Rome or Delhi is reachable from elsewhere", () => {
    const playable = catalog.atlases.flatMap((a) => a.maps.filter((m) => m.city));
    expect(playable.length).toBeGreaterThanOrEqual(4);
  });
});
