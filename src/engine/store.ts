import { create } from "zustand";
import type { City, HistoricalEvent, Landmark, Spot, Story, Vec2 } from "@/content/schema";

export type Mode = "exploring" | "previewing" | "focused" | "immersed";

export type PeriodChange = {
  fromId: string;
  toId: string;
  entries: { landmarkId: string; name: string; kind: "appears" | "disappears" | "changes"; note?: string }[];
};

export type HoveredFeature = { kind: "road" | "district" | "hill" | "water" | "wall" | "spot" | "gate" | "event" | "aqueduct" | "bridge" | "object"; id: string; name: string; blurb?: string; hint?: string };

/** What the camera and panels are centred on. */
export type Focus =
  | { kind: "landmark"; id: string; position: Vec2; size: number; name: string }
  | { kind: "spot"; id: string; position: Vec2; size: number; name: string }
  | { kind: "event"; id: string; position: Vec2; size: number; name: string };

type State = {
  city: City | null;
  cityId: string | null;
  loading: boolean;
  error: string | null;
  mode: Mode;
  hoveredId: string | null;
  focusedId: string | null;
  focusedSpotId: string | null;
  focusedEventId: string | null;
  hoveredFeature: HoveredFeature | null;
  hoveredDistrictId: string | null;
  periodId: string | null;
  periodChange: PeriodChange | null;
  storyId: string | null;
  storyStep: number;
  /** Hour of the day, 0–24, drives lighting and vignettes. */
  hour: number;
  eraOpen: boolean;
  /** The ordinary city block under the pointer (rises as a massing model). */
  hoveredBlockId: number | null;
  /** A piece of open land under the pointer: field, pasture, vineyard, orchard, park or marsh. */
  hoveredArea: { kind: string; name?: string } | null;
  zoomLevel: "city" | "district" | "landmark";
  touch: boolean;
  /** The writing table and the things on it, round the map (remembered between visits). */
  desk: boolean;
};

type Actions = {
  setCity: (id: string, city: City, periodId?: string | null) => void;
  setLoading: (id: string) => void;
  setError: (msg: string) => void;
  hover: (id: string | null) => void;
  hoverFeature: (f: HoveredFeature | null) => void;
  focus: (id: string) => void;
  focusSpot: (id: string) => void;
  focusEvent: (id: string) => void;
  immerse: () => void;
  back: () => void;
  setPeriod: (id: string) => void;
  dismissChange: () => void;
  startStory: (id: string) => void;
  storyNext: () => void;
  storyPrev: () => void;
  endStory: () => void;
  setHour: (h: number) => void;
  toggleEra: (open?: boolean) => void;
  setHoveredBlock: (id: number | null) => void;
  setHoveredArea: (a: { kind: string; name?: string } | null) => void;
  setZoomLevel: (z: State["zoomLevel"]) => void;
  setTouch: (t: boolean) => void;
  toggleDesk: () => void;
};

export type Store = State & Actions;

const initial: State = {
  city: null,
  cityId: null,
  loading: false,
  error: null,
  mode: "exploring",
  hoveredId: null,
  focusedId: null,
  focusedSpotId: null,
  focusedEventId: null,
  hoveredFeature: null,
  hoveredDistrictId: null,
  periodId: null,
  periodChange: null,
  storyId: null,
  storyStep: 0,
  hour: 10,
  eraOpen: false,
  hoveredBlockId: null,
  hoveredArea: null,
  zoomLevel: "city",
  touch: false,
  desk: readDesk(),
};

export const useStore = create<Store>((set, get) => ({
  ...initial,

  setLoading: (id) => set({ loading: true, error: null, cityId: id }),
  setError: (msg) => set({ loading: false, error: msg }),
  setCity: (id, city, periodId) =>
    set({
      ...initial,
      touch: get().touch,
      desk: get().desk,
      hour: get().hour,
      city,
      cityId: id,
      periodId: periodId && city.periods.some((p) => p.id === periodId) ? periodId : city.defaultPeriodId,
    }),

  hover: (id) => {
    const s = get();
    if (id && !isActive(s, id)) return;
    if (s.mode === "exploring" || s.mode === "previewing") {
      set({ hoveredId: id, mode: id ? "previewing" : "exploring" });
    } else {
      set({ hoveredId: id });
    }
  },

  hoverFeature: (f) => {
    const s = get();
    if (f?.id === s.hoveredFeature?.id && f?.kind === s.hoveredFeature?.kind) return;
    set({ hoveredFeature: f, hoveredDistrictId: f?.kind === "district" ? f.id : null });
  },

  focus: (id) => {
    const s = get();
    if (!isActive(s, id)) return;
    set({ focusedId: id, focusedSpotId: null, focusedEventId: null, hoveredId: null, mode: "focused", eraOpen: false });
  },

  focusSpot: (id) => {
    const s = get();
    if (!isSpotActive(s, id)) return;
    set({ focusedSpotId: id, focusedId: null, focusedEventId: null, hoveredId: null, mode: "focused", eraOpen: false });
  },

  focusEvent: (id) => {
    const s = get();
    const e = s.city?.events.find((x) => x.id === id);
    if (!e) return;
    if (s.periodId !== e.periodId) get().setPeriod(e.periodId);
    set({ focusedEventId: id, focusedId: null, focusedSpotId: null, hoveredId: null, mode: "focused", eraOpen: false, periodChange: null });
  },

  immerse: () => {
    if (get().mode === "focused") set({ mode: "immersed" });
  },

  back: () => {
    const s = get();
    if (s.eraOpen) {
      set({ eraOpen: false });
    } else if (s.storyId) {
      set({ storyId: null, storyStep: 0, focusedId: null, focusedSpotId: null, focusedEventId: null, hoveredId: null, mode: "exploring" });
    } else if (s.mode === "immersed") {
      set({ mode: "focused" });
    } else if (s.mode === "focused") {
      set({ focusedId: null, focusedSpotId: null, focusedEventId: null, hoveredId: null, mode: "exploring" });
    } else if (s.mode === "previewing") {
      set({ hoveredId: null, mode: "exploring" });
    }
  },

  setPeriod: (id) => {
    const s = get();
    if (!s.city || s.periodId === id || !s.city.periods.some((p) => p.id === id)) return;
    const change = diffPeriods(s.city, s.periodId!, id);
    const next: Partial<State> = { periodId: id, periodChange: change };
    const lm = (lid: string | null) => lid && s.city!.landmarks.find((l) => l.id === lid);
    const sp = (sid: string | null) => sid && s.city!.spots.find((x) => x.id === sid);
    const focusedLm = lm(s.focusedId);
    const focusedSp = sp(s.focusedSpotId);
    const ev = s.focusedEventId ? s.city.events.find((e) => e.id === s.focusedEventId) : null;
    if ((focusedLm && !focusedLm.activePeriods.includes(id)) || (focusedSp && !focusedSp.activePeriods.includes(id)) || (ev && ev.periodId !== id)) {
      next.focusedId = null;
      next.focusedSpotId = null;
      next.focusedEventId = null;
      next.mode = "exploring";
    }
    const hov = lm(s.hoveredId);
    if (hov && !hov.activePeriods.includes(id)) {
      next.hoveredId = null;
      if (s.mode === "previewing") next.mode = "exploring";
    }
    set(next);
  },

  dismissChange: () => set({ periodChange: null }),

  startStory: (id) => {
    const s = get();
    const story = s.city?.stories.find((st) => st.id === id);
    if (!story) return;
    if (s.periodId !== story.periodId) get().setPeriod(story.periodId);
    set({ storyId: id, storyStep: 0, periodChange: null, eraOpen: false });
    focusStep(get, story.steps[0]);
  },

  storyNext: () => {
    const s = get();
    const story = currentStory(s);
    if (!story) return;
    const step = Math.min(s.storyStep + 1, story.steps.length - 1);
    set({ storyStep: step });
    focusStep(get, story.steps[step]);
  },

  storyPrev: () => {
    const s = get();
    const story = currentStory(s);
    if (!story) return;
    const step = Math.max(s.storyStep - 1, 0);
    set({ storyStep: step });
    focusStep(get, story.steps[step]);
  },

  endStory: () => set({ storyId: null, storyStep: 0, focusedId: null, focusedSpotId: null, focusedEventId: null, hoveredId: null, mode: "exploring" }),

  setHour: (h) => set({ hour: ((h % 24) + 24) % 24 }),
  toggleEra: (open) => set({ eraOpen: open ?? !get().eraOpen }),
  setHoveredBlock: (id) => set({ hoveredBlockId: id }),
  setHoveredArea: (a) => {
    const c = get().hoveredArea;
    if (c?.kind === a?.kind && c?.name === a?.name) return;
    set({ hoveredArea: a });
  },
  setZoomLevel: (zoomLevel) => {
    if (get().zoomLevel !== zoomLevel) set({ zoomLevel });
  },
  setTouch: (touch) => set({ touch }),
  toggleDesk: () => {
    const desk = !get().desk;
    try {
      localStorage.setItem("chronoscape.desk", desk ? "1" : "0");
    } catch {
      /* private mode: just for this visit */
    }
    set({ desk });
  },
}));

function readDesk() {
  try {
    return localStorage.getItem("chronoscape.desk") !== "0";
  } catch {
    return true;
  }
}

function focusStep(get: () => Store, step: Story["steps"][number]) {
  if (step.landmarkId) get().focus(step.landmarkId);
  else if (step.spotId) get().focusSpot(step.spotId);
}

/* ---------- selectors / helpers ---------- */

export function isActive(s: Pick<State, "city" | "periodId">, landmarkId: string): boolean {
  const l = s.city?.landmarks.find((x) => x.id === landmarkId);
  return !!l && !!s.periodId && l.activePeriods.includes(s.periodId);
}

export function isSpotActive(s: Pick<State, "city" | "periodId">, spotId: string): boolean {
  const sp = s.city?.spots.find((x) => x.id === spotId);
  return !!sp && !!s.periodId && sp.activePeriods.includes(s.periodId);
}

export function currentStory(s: Pick<State, "city" | "storyId">): Story | null {
  return s.city?.stories.find((st) => st.id === s.storyId) ?? null;
}

export function landmarkById(city: City | null, id: string | null): Landmark | null {
  return (id && city?.landmarks.find((l) => l.id === id)) || null;
}

export function spotById(city: City | null, id: string | null): Spot | null {
  return (id && city?.spots.find((s) => s.id === id)) || null;
}

export function eventById(city: City | null, id: string | null): HistoricalEvent | null {
  return (id && city?.events.find((e) => e.id === id)) || null;
}

/** Name/model/note for a landmark in a given period, merging the period variant over the base. */
export function resolveVariant(l: Landmark, periodId: string | null) {
  const v = (periodId && l.variants[periodId]) || {};
  return {
    name: v.name ?? l.name,
    model: v.model ?? l.model,
    note: v.note,
    confidence: v.confidence ?? l.confidence,
  };
}

export function resolveSpot(sp: Spot, periodId: string | null) {
  const v = (periodId && sp.variants[periodId]) || {};
  return { name: v.name ?? sp.name, note: v.note };
}

/**
 * The landmark an event takes place at: named directly, or the one whose
 * footprint contains the event's position. Focusing the event raises it.
 */
const eventLandmarkCache = new WeakMap<City, Map<string, string | null>>();
export function landmarkForEvent(city: City, eventId: string | null): string | null {
  if (!eventId) return null;
  let m = eventLandmarkCache.get(city);
  if (!m) eventLandmarkCache.set(city, (m = new Map()));
  if (m.has(eventId)) return m.get(eventId)!;
  const e = city.events.find((x) => x.id === eventId);
  let out: string | null = null;
  if (e) {
    const at = e.at;
    if ("landmarkId" in at) out = at.landmarkId;
    else if ("position" in at) {
      const [px, py] = at.position;
      for (const l of city.landmarks) {
        if (!l.activePeriods.includes(e.periodId)) continue;
        const a = (l.rotation * Math.PI) / 180;
        const dx = px - l.position[0], dy = py - l.position[1];
        const u = dx * Math.cos(a) + dy * Math.sin(a), v = -dx * Math.sin(a) + dy * Math.cos(a);
        if (Math.abs(u) <= (l.footprint[0] * l.scale) / 2 && Math.abs(v) <= (l.footprint[1] * l.scale) / 2) {
          out = l.id;
          break;
        }
      }
    }
  }
  m.set(eventId, out);
  return out;
}

/** Where an event happens, resolved to a map position. */
export function eventPlace(city: City, e: HistoricalEvent): { position: Vec2; size: number; name: string } {
  const at = e.at;
  if ("landmarkId" in at) {
    const l = city.landmarks.find((x) => x.id === at.landmarkId)!;
    return { position: l.position, size: Math.max(l.footprint[0], l.footprint[1]) * l.scale, name: l.name };
  }
  if ("spotId" in at) {
    const s = city.spots.find((x) => x.id === at.spotId)!;
    return { position: s.position, size: 40, name: s.name };
  }
  return { position: at.position, size: 60, name: e.title };
}

/** The current focus target, if any. */
export function currentFocus(s: Pick<State, "city" | "focusedId" | "focusedSpotId" | "focusedEventId" | "periodId">): Focus | null {
  const city = s.city;
  if (!city) return null;
  if (s.focusedId) {
    const l = city.landmarks.find((x) => x.id === s.focusedId)!;
    return { kind: "landmark", id: l.id, position: l.position, size: Math.max(l.footprint[0], l.footprint[1]) * l.scale, name: resolveVariant(l, s.periodId).name };
  }
  if (s.focusedSpotId) {
    const sp = city.spots.find((x) => x.id === s.focusedSpotId)!;
    return { kind: "spot", id: sp.id, position: sp.position, size: 40, name: resolveSpot(sp, s.periodId).name };
  }
  if (s.focusedEventId) {
    const e = city.events.find((x) => x.id === s.focusedEventId)!;
    const pl = eventPlace(city, e);
    return { kind: "event", id: e.id, position: pl.position, size: pl.size, name: e.title };
  }
  return null;
}

/** The vignette closest to the given hour (wrapping around midnight). */
export function vignetteAt(sp: Spot, hour: number) {
  if (sp.vignettes.length === 0) return null;
  let best = sp.vignettes[0];
  let bestD = 99;
  for (const v of sp.vignettes) {
    const d = Math.min(Math.abs(v.hour - hour), 24 - Math.abs(v.hour - hour));
    if (d < bestD) {
      bestD = d;
      best = v;
    }
  }
  return best;
}

export function diffPeriods(city: City, fromId: string, toId: string): PeriodChange {
  const entries: PeriodChange["entries"] = [];
  for (const l of city.landmarks) {
    const was = l.activePeriods.includes(fromId);
    const now = l.activePeriods.includes(toId);
    const to = resolveVariant(l, toId);
    if (!was && now) entries.push({ landmarkId: l.id, name: to.name, kind: "appears", note: to.note });
    else if (was && !now) entries.push({ landmarkId: l.id, name: l.name, kind: "disappears", note: l.variants[toId]?.note });
    else if (now && to.note) entries.push({ landmarkId: l.id, name: to.name, kind: "changes", note: to.note });
  }
  const order = { appears: 0, disappears: 1, changes: 2 };
  entries.sort((a, b) => order[a.kind] - order[b.kind]);
  return { fromId, toId, entries };
}
