import { CitySchema, type City } from "./schema";

export type Issue = { level: "error" | "warn"; path: string; message: string };

/**
 * Parse + cross-reference checks for one city pack. Pure: no file system access,
 * so it runs in the browser (dev), in the validator script, and in tests.
 */
export function validateCity(raw: unknown, opts: { assetExists?: (path: string) => boolean } = {}): { city: City | null; issues: Issue[] } {
  const parsed = CitySchema.safeParse(raw);
  if (!parsed.success) {
    return {
      city: null,
      issues: parsed.error.issues.map((i) => ({ level: "error", path: i.path.join("."), message: i.message })),
    };
  }
  const city = parsed.data;
  const issues: Issue[] = [];
  const err = (path: string, message: string) => issues.push({ level: "error", path, message });
  const warn = (path: string, message: string) => issues.push({ level: "warn", path, message });

  const periodIds = new Set(city.periods.map((p) => p.id));
  const sourceIds = new Set(city.sources.map((s) => s.id));
  const landmarkIds = new Set(city.landmarks.map((l) => l.id));
  const spotIds = new Set(city.spots.map((s) => s.id));
  const [mapW, mapH] = city.map.size;

  const dup = (ids: string[], label: string) => {
    const seen = new Set<string>();
    for (const id of ids) {
      if (seen.has(id)) err(label, `duplicate id "${id}"`);
      seen.add(id);
    }
  };
  dup(city.periods.map((p) => p.id), "periods");
  dup(city.sources.map((s) => s.id), "sources");
  dup(city.landmarks.map((l) => l.id), "landmarks");
  dup(city.spots.map((s) => s.id), "spots");
  dup(city.events.map((e) => e.id), "events");
  dup(city.stories.map((s) => s.id), "stories");

  city.map.bridges.forEach((b, i) => {
    if (b.landmarkId && !landmarkIds.has(b.landmarkId)) err(`map.bridges[${i}].landmarkId`, `unknown landmark "${b.landmarkId}"`);
  });
  if (!periodIds.has(city.defaultPeriodId)) err("defaultPeriodId", `unknown period "${city.defaultPeriodId}"`);

  city.periods.forEach((p, i) => {
    if (p.startYear > p.endYear) err(`periods[${i}]`, "startYear is after endYear");
    if (p.year < p.startYear || p.year > p.endYear) err(`periods[${i}]`, "representative year is outside the period range");
  });

  const inMap = ([x, y]: [number, number]) => x >= 0 && y >= 0 && x <= mapW && y <= mapH;
  const checkPeriods = (path: string, periods?: string[]) => {
    for (const pid of periods ?? []) if (!periodIds.has(pid)) err(path, `unknown period "${pid}"`);
  };
  const checkSources = (path: string, ids: string[]) => {
    for (const sid of ids) if (!sourceIds.has(sid)) err(path, `unknown source "${sid}"`);
  };

  /* map features */
  const m = city.map;
  const featureLists: [string, { periods?: string[] }[]][] = [
    ["water", m.water], ["islands", m.islands], ["hills", m.hills], ["roads", m.roads], ["walls", m.walls], ["gates", m.gates],
    ["bridges", m.bridges], ["aqueducts", m.aqueducts], ["blocks", m.blocks], ["gardens", m.gardens], ["marsh", m.marsh], ["districts", m.districts], ["labels", m.labels],
  ];
  for (const [name, list] of featureLists) list.forEach((f, i) => checkPeriods(`map.${name}[${i}]`, f.periods));
  m.hills.forEach((h, i) => { if (!inMap(h.center)) err(`map.hills[${i}]`, "centre outside the map"); });
  m.gates.forEach((g, i) => { if (!inMap(g.position)) err(`map.gates[${i}]`, "position outside the map"); });
  dup(m.districts.map((d) => d.id), "map.districts");

  const checkModel = (path: string, model: City["landmarks"][number]["model"]) => {
    if ("glb" in model && opts.assetExists && !opts.assetExists(model.glb)) err(path, `missing asset assets/${model.glb}`);
  };

  city.landmarks.forEach((l, i) => {
    const p = `landmarks[${i}] (${l.id})`;
    if (!inMap(l.position)) err(p, `position ${l.position} is outside the map ${mapW}x${mapH}`);
    checkPeriods(p, l.activePeriods);
    for (const pid of Object.keys(l.variants)) {
      if (!periodIds.has(pid)) err(p, `variants references unknown period "${pid}"`);
      const v = l.variants[pid];
      if (v.model) checkModel(`${p}.variants.${pid}.model`, v.model);
    }
    checkSources(p, l.sourceIds);
    checkModel(`${p}.model`, l.model);
    if (l.confidence !== "documented" && l.details.length === 0) warn(p, "reconstruction/interpretation without details explaining the basis");
  });

  city.spots.forEach((s, i) => {
    const p = `spots[${i}] (${s.id})`;
    if (!inMap(s.position)) err(p, `position ${s.position} is outside the map`);
    checkPeriods(p, s.activePeriods);
    checkPeriods(p, Object.keys(s.variants));
    checkSources(p, s.sourceIds);
    if (s.vignettes.length < 2) warn(p, "fewer than 2 vignettes; the day clock will have little to show");
  });

  const activeIn = (kind: "landmark" | "spot", id: string, periodId: string) => {
    const item = kind === "landmark" ? city.landmarks.find((l) => l.id === id) : city.spots.find((s) => s.id === id);
    return !!item && item.activePeriods.includes(periodId);
  };

  city.events.forEach((e, i) => {
    const p = `events[${i}] (${e.id})`;
    if (!periodIds.has(e.periodId)) err(p, `unknown period "${e.periodId}"`);
    if ("landmarkId" in e.at) {
      if (!landmarkIds.has(e.at.landmarkId)) err(p, `unknown landmark "${e.at.landmarkId}"`);
      else if (!activeIn("landmark", e.at.landmarkId, e.periodId)) err(p, `landmark "${e.at.landmarkId}" is not present in period "${e.periodId}"`);
    } else if ("spotId" in e.at) {
      if (!spotIds.has(e.at.spotId)) err(p, `unknown spot "${e.at.spotId}"`);
      else if (!activeIn("spot", e.at.spotId, e.periodId)) err(p, `spot "${e.at.spotId}" is not present in period "${e.periodId}"`);
    } else if (!inMap(e.at.position)) err(p, "position outside the map");
    checkSources(p, e.sourceIds);
  });

  city.stories.forEach((s, i) => {
    const p = `stories[${i}] (${s.id})`;
    if (!periodIds.has(s.periodId)) err(p, `unknown period "${s.periodId}"`);
    checkSources(p, s.sourceIds);
    s.steps.forEach((step, j) => {
      if (step.landmarkId) {
        if (!landmarkIds.has(step.landmarkId)) err(`${p}.steps[${j}]`, `unknown landmark "${step.landmarkId}"`);
        else if (!activeIn("landmark", step.landmarkId, s.periodId)) err(`${p}.steps[${j}]`, `landmark "${step.landmarkId}" does not exist in period "${s.periodId}"`);
      }
      if (step.spotId) {
        if (!spotIds.has(step.spotId)) err(`${p}.steps[${j}]`, `unknown spot "${step.spotId}"`);
        else if (!activeIn("spot", step.spotId, s.periodId)) err(`${p}.steps[${j}]`, `spot "${step.spotId}" does not exist in period "${s.periodId}"`);
      }
      checkSources(`${p}.steps[${j}]`, step.sourceIds);
    });
  });

  return { city, issues };
}
