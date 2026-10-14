import { describe, it, expect } from "vitest";
import { readFileSync, readdirSync, existsSync } from "node:fs";
import { join, resolve } from "node:path";
import { validateCity } from "../src/content/validate";
import { CityIndexSchema } from "../src/content/schema";

const root = resolve(__dirname, "..");
const citiesDir = join(root, "content", "cities");
const index = CityIndexSchema.parse(JSON.parse(readFileSync(join(citiesDir, "index.json"), "utf8")));

describe("content packs", () => {
  it("lists every city directory in index.json", () => {
    const dirs = readdirSync(citiesDir, { withFileTypes: true }).filter((d) => d.isDirectory()).map((d) => d.name).sort();
    expect(index.cities.map((c) => c.id).sort()).toEqual(dirs);
  });

  for (const c of index.cities) {
    it(`${c.id} validates with no errors`, () => {
      const raw = JSON.parse(readFileSync(join(citiesDir, c.id, "city.json"), "utf8"));
      const { city, issues } = validateCity(raw, { assetExists: (p) => existsSync(join(root, "assets", p)) });
      const errors = issues.filter((i) => i.level === "error");
      expect(errors, JSON.stringify(errors, null, 2)).toEqual([]);
      expect(city?.id).toBe(c.id);
    });
  }

  it("rejects a landmark that references a missing period", () => {
    const raw = JSON.parse(readFileSync(join(citiesDir, "rome", "city.json"), "utf8"));
    raw.landmarks[0].activePeriods.push("not-a-period");
    const { issues } = validateCity(raw);
    expect(issues.some((i) => i.level === "error" && i.message.includes("not-a-period"))).toBe(true);
  });

  it("rejects a story step whose landmark is absent in the story period", () => {
    const raw = JSON.parse(readFileSync(join(citiesDir, "rome", "city.json"), "utf8"));
    raw.stories[0].periodId = "republic-50bce"; // the Arch of Titus does not exist yet
    const { issues } = validateCity(raw);
    expect(issues.some((i) => i.level === "error" && i.message.includes("arch-of-titus"))).toBe(true);
  });
});
