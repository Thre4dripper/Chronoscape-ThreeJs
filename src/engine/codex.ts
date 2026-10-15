import type { City, Landmark } from "@/content/schema";
import { resolveVariant } from "./store";

/**
 * Data behind the Codex (the left-hand notebook): pictures from the sources,
 * measured drawings rendered from the models, and questions generated from the
 * content pack. Everything is fetched lazily the first time a place is opened,
 * so the map's first load is unaffected. City-agnostic.
 */

export type Picture = {
  src: string;
  /** ~200 px thumbnail, for the strip */
  thumb?: string;
  w: number;
  h: number;
  kind: string;
  caption: string;
  artist: string;
  date: string;
  license: string;
  licenseUrl: string | null;
  page: string;
};
/** A front elevation rendered from a model: metres per pixel and where the ground line is. */
export type Elevation = { w: number; h: number; px: [number, number]; mpp: number; ground: number; x0px: number };
/** A top-down plan rendered from a model: it covers `size` metres square. */
export type Plan = { size: number; w: number; d: number; px: number; ext?: string };

const cache = new Map<string, Promise<unknown>>();
function json<T>(url: string): Promise<T | null> {
  let p = cache.get(url) as Promise<T | null> | undefined;
  if (!p) {
    p = fetch(url)
      .then((r) => (r.ok ? (r.json() as Promise<T>) : null))
      .catch(() => null);
    cache.set(url, p);
  }
  return p;
}

export const loadPictures = (cityId: string) => json<Record<string, Picture[]>>(`/media/${cityId}/index.json`);
export const loadElevations = () => json<Record<string, Elevation>>("/media/elevations/manifest.json");
export const loadPlans = () => json<Record<string, Plan>>("/models/plans/manifest.json");

/** "models/rome/colosseum.glb" -> "rome/colosseum" */
export function modelKey(l: Landmark, periodId: string | null): string | null {
  const m = resolveVariant(l, periodId).model;
  return "glb" in m ? m.glb.replace(/^\/?models\//, "").replace(/\.glb$/, "") : null;
}

/* ------------------------------------------------------------------ dates */

/** First year mentioned with an era marker: "c. 72–80 CE" -> 72, "dedicated 13 or 11 BCE" -> -13. */
export function firstYear(text: string | undefined): number | null {
  if (!text) return null;
  const re = /(\d{1,4})(?:\s*(?:–|-|or|to|and)\s*(\d{1,4}))?\s*(BCE|BC|CE|AD)\b/g;
  const m = re.exec(text);
  if (!m) {
    const c = /\b(1[0-9]{3})\b/.exec(text); // a bare later year, "1560"
    return c ? parseInt(c[1], 10) : null;
  }
  const y = parseInt(m[1], 10);
  return m[3] === "BCE" || m[3] === "BC" ? -y : y;
}

export const fmtYear = (y: number) => (y < 0 ? `${-y} BCE` : `${y} CE`);

/* ------------------------------------------------------------------ quiz */

export type Question = { id: string; prompt: string; options: string[]; answer: number; explain: string };

function rng(seed: string) {
  let h = 2166136261;
  for (let i = 0; i < seed.length; i++) h = Math.imul(h ^ seed.charCodeAt(i), 16777619);
  return () => {
    h = Math.imul(h ^ (h >>> 15), 2246822507);
    h = Math.imul(h ^ (h >>> 13), 3266489909);
    return ((h ^= h >>> 16) >>> 0) / 4294967296;
  };
}
function shuffle<T>(a: T[], r: () => number): T[] {
  const b = [...a];
  for (let i = b.length - 1; i > 0; i--) {
    const j = Math.floor(r() * (i + 1));
    [b[i], b[j]] = [b[j], b[i]];
  }
  return b;
}
function pick<T>(pool: T[], n: number, r: () => number, ok: (x: T) => boolean): T[] {
  return shuffle(pool, r).filter(ok).slice(0, n);
}
function mc(id: string, prompt: string, right: string, wrong: string[], explain: string, r: () => number): Question | null {
  if (wrong.length < 2) return null;
  const options = shuffle([right, ...wrong.slice(0, 3)], r);
  return { id, prompt, options, answer: options.indexOf(right), explain };
}
const firstClause = (s: string | undefined) => (s ?? "").split(/[;:]/)[0].trim();
const cap = (s: string) => s.charAt(0).toUpperCase() + s.slice(1);

/** Three or four multiple-choice questions about one landmark, from the content pack alone. */
export function questionsFor(city: City, l: Landmark, periodId: string | null, attempt = 0): Question[] {
  const r = rng(`${city.id}:${l.id}:${attempt}`);
  const others = city.landmarks.filter((x) => x.id !== l.id);
  const name = resolveVariant(l, periodId).name;
  const out: (Question | null)[] = [];

  // when was it built?
  const y = firstYear(l.built);
  if (y !== null) {
    const years = [...new Set(others.map((o) => firstYear(o.built)).filter((v): v is number => v !== null && Math.abs(v - y) >= 60))];
    const wrong = pick(years, 3, r, () => true).sort((a, b) => a - b);
    out.push(mc(`${l.id}:built`, `When was the ${name} begun?`, `c. ${fmtYear(y)}`, wrong.map((v) => `c. ${fmtYear(v)}`), cap(l.built ?? ""), r));
  }

  // what was it for?
  const fn = firstClause(l.function);
  if (fn) {
    const wrong = pick(others.map((o) => firstClause(o.function)), 3, r, (f) => !!f && f.toLowerCase() !== fn.toLowerCase());
    out.push(mc(`${l.id}:fn`, `What was the ${name} built for?`, cap(fn), wrong.map(cap), l.summary, r));
  }

  // what was it called later, or when did it first stand?
  const renamed = city.periods.find((p) => l.activePeriods.includes(p.id) && resolveVariant(l, p.id).name !== l.name);
  if (renamed) {
    const later = resolveVariant(l, renamed.id).name;
    const wrong = pick(others.map((o) => o.name), 3, r, (n) => n !== later && n !== l.name);
    out.push(mc(`${l.id}:name`, `By ${fmtYear(renamed.year)} the ${l.name} was known as…`, later, wrong, resolveVariant(l, renamed.id).note ?? "", r));
  } else {
    const first = city.periods.filter((p) => l.activePeriods.includes(p.id)).sort((a, b) => a.year - b.year)[0];
    if (first) {
      const wrong = pick(city.periods, 3, r, (p) => p.id !== first.id).map((p) => `${p.label} (${fmtYear(p.year)})`);
      out.push(mc(`${l.id}:era`, `In which era does the ${name} first appear on this map?`, `${first.label} (${fmtYear(first.year)})`, wrong, l.variants[first.id]?.note ?? l.summary, r));
    }
  }

  // how big?
  const size = Math.max(l.footprint[0], l.footprint[1]);
  if (size > 12) {
    const right = Math.round(size / 5) * 5;
    const wrong = [0.4, 2.2, 3.6].map((k) => Math.round((size * k) / 5) * 5).filter((v) => v > 0 && v !== right);
    out.push(mc(`${l.id}:size`, `Roughly how long is the ${name} at its longest side?`, `${right} m`, wrong.map((v) => `${v} m`), `The model, like the remains, measures about ${Math.round(l.footprint[0])} × ${Math.round(l.footprint[1])} m on the ground.`, r));
  }
  return out.filter((q): q is Question => !!q);
}

/* ------------------------------------------------------------------ map hunt */

export type Riddle = { landmarkId: string; text: string; hint: string };

/** A riddle for a landmark standing in this period: what it was for, with its name kept out. */
export function riddleFor(city: City, periodId: string, seen: Set<string>, attempt: number): Riddle | null {
  const pool = city.landmarks.filter((l) => l.activePeriods.includes(periodId) && !!l.function && !seen.has(l.id));
  if (!pool.length) return null;
  const r = rng(`${city.id}:${periodId}:hunt:${attempt}`);
  const l = pool[Math.floor(r() * pool.length)];
  const v = resolveVariant(l, periodId);
  const hide = new Set([...l.name.split(/\W+/), ...v.name.split(/\W+/)].filter((w) => w.length > 3).map((w) => w.toLowerCase()));
  const mask = (s: string) => s.replace(/[A-Za-zÀ-ÿ']+/g, (w) => (hide.has(w.toLowerCase()) ? "…" : w));
  const fn = mask(firstClause(l.function));
  const built = firstYear(l.built);
  return {
    landmarkId: l.id,
    text: `Find the ${l.category === "district" ? "quarter" : "building"} used as: ${fn.toLowerCase()}.`,
    hint: built !== null ? `It was begun around ${fmtYear(built)}.` : mask(l.summary.split(". ")[0]) + ".",
  };
}

/** "about 600 m north-east" from one landmark to another. */
export function bearing(city: City, fromId: string, toId: string): string {
  const a = city.landmarks.find((l) => l.id === fromId), b = city.landmarks.find((l) => l.id === toId);
  if (!a || !b) return "";
  const dx = b.position[0] - a.position[0], dy = b.position[1] - a.position[1];
  const metres = Math.hypot(dx, dy); // map units are metres
  const dirs = ["east", "south-east", "south", "south-west", "west", "north-west", "north", "north-east"];
  const dir = dirs[Math.round(((Math.atan2(dy, dx) + Math.PI * 2) % (Math.PI * 2)) / (Math.PI / 4)) % 8];
  const d = metres > 1000 ? `${(metres / 1000).toFixed(1)} km` : `${Math.max(50, Math.round(metres / 50) * 50)} m`;
  return `about ${d} ${dir}`;
}

/* ------------------------------------------------------------------ scores (this browser only) */

const KEY = "chronoscape.laurels";
export type Laurels = { asked: number; right: number; found: number };
export function readLaurels(): Laurels {
  try {
    return { asked: 0, right: 0, found: 0, ...JSON.parse(localStorage.getItem(KEY) ?? "{}") };
  } catch {
    return { asked: 0, right: 0, found: 0 };
  }
}
export function addLaurels(d: Partial<Laurels>): Laurels {
  const cur = readLaurels();
  const next = { asked: cur.asked + (d.asked ?? 0), right: cur.right + (d.right ?? 0), found: cur.found + (d.found ?? 0) };
  try {
    localStorage.setItem(KEY, JSON.stringify(next));
  } catch {
    /* private mode: scores just aren't kept */
  }
  return next;
}
