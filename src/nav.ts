import { create } from "zustand";
import type { AtlasMap } from "@/content/schema";
import { atlasCatalog, loadCity } from "@/content/registry";
import { useStore } from "@/engine/store";
import { parsePath, pathFor, monumentEra } from "./meta";

/**
 * Where the visitor is: the title page, the map room (with an atlas open or
 * not), or inside a city map. Kept in the address bar as a real path, so links,
 * reloads and the back button all work and every page has its own baked HTML
 * (the addresses are listed in src/meta.ts):
 *   /  ·  /atlases/  ·  /atlases/<atlas>/  ·  /<city>/  ·  /<city>/<era>/  ·  /<city>/<monument>/
 */
export type View = "title" | "room" | "city";

/** A map on its way between the shelf and the screen. */
export type Flight = {
  kind: "unfold" | "fold";
  atlasId: string | null;
  map: AtlasMap;
  /** Where the folded map starts (unfold) or ends (fold), in screen pixels. */
  rect: { x: number; y: number; w: number; h: number } | null;
  image: string;
};

type Nav = {
  view: View;
  atlasId: string | null;
  flight: Flight | null;
  /** Atlas the city was opened from: the map case opens on it. */
  fromAtlas: string | null;
  goTitle: () => void;
  goRoom: (atlasId?: string | null) => void;
  openAtlas: (atlasId: string | null) => void;
  openMap: (atlasId: string | null, map: AtlasMap, rect: Flight["rect"]) => void;
  /** Called by the flight overlay when the unfolded map has handed over to the live city. */
  landed: () => void;
  leaveCity: (atlasId?: string | null) => void;
};

export const previewOf = (city: string, period?: string) => `/plates/${city}/${period ?? ""}.preview.webp`;

function urlFor(view: View, atlasId: string | null, city?: string, period?: string | null) {
  if (view === "room") return pathFor({ view: "room", atlasId });
  if (view === "city" && city) return pathFor({ view: "city", city, period });
  return "/";
}

export const useNav = create<Nav>((set, get) => ({
  view: "title",
  atlasId: null,
  flight: null,
  fromAtlas: null,

  goTitle: () => {
    history.pushState(null, "", urlFor("title", null));
    set({ view: "title", atlasId: null, flight: null });
  },

  goRoom: (atlasId = null) => {
    history.pushState(null, "", urlFor("room", atlasId));
    set({ view: "room", atlasId, flight: null });
  },

  openAtlas: (atlasId) => {
    history.replaceState(null, "", urlFor("room", atlasId));
    if (atlasId) remember("atlases", atlasId);
    set({ atlasId });
  },

  openMap: (atlasId, map, rect) => {
    if (!map.city) return;
    const city = map.city;
    remember("travels", `${map.title}|${map.subtitle}`);
    // start loading at once: the city arrives while the map flies and unfolds
    void loadCity(city).catch(() => undefined);
    set({ flight: { kind: "unfold", atlasId, map, rect, image: previewOf(city, map.period ?? defaultPeriod(city)) }, fromAtlas: atlasId });
    // the city takes over the screen only once the unfolded map covers it
    const covered = new Promise<void>((res) => {
      const done = () => (removeEventListener("chronoscape:covered", done), res());
      addEventListener("chronoscape:covered", done);
      setTimeout(done, 5000);
    });
    // the pack loads during the flight; the city itself changes only under the covering map
    void Promise.all([loadCity(city).catch(() => undefined), covered]).then(() => enterCity(city, map.period ?? null)).then(() => {
      history.pushState(null, "", urlFor("city", null, city, map.period ?? useStore.getState().periodId));
      set({ view: "city", atlasId: null });
    });
  },

  landed: () => set({ flight: null }),

  leaveCity: (atlasId) => {
    const st = useStore.getState();
    // back into the atlas it came from, or the first one that holds this city at this era
    const holds = (pred: (m: AtlasMap) => boolean) => atlasCatalog.atlases.find((x) => x.maps.some(pred))?.id;
    const a = atlasId ?? get().fromAtlas ?? holds((m) => m.city === st.cityId && m.period === st.periodId) ?? holds((m) => m.city === st.cityId) ?? null;
    const atlas = atlasCatalog.atlases.find((x) => x.id === a);
    const map = atlas?.maps.find((m) => m.city === st.cityId && m.period === st.periodId) ?? atlas?.maps.find((m) => m.city === st.cityId) ?? { title: st.city?.name ?? "", subtitle: "", blurb: "", at: [0, 0] as [number, number], glyph: "temple" as const, city: st.cityId ?? undefined };
    history.pushState(null, "", urlFor("room", a ?? null));
    set({
      view: "room",
      atlasId: a ?? null,
      flight: st.cityId ? { kind: "fold", atlasId: a ?? null, map, rect: null, image: previewOf(st.cityId, st.periodId ?? undefined) } : null,
    });
  },
}));

function defaultPeriod(city: string) {
  for (const a of atlasCatalog.atlases) for (const m of a.maps) if (m.city === city && m.period) return m.period;
  return undefined;
}

/** Load a city pack and show it at an era (without the period-change card). */
export async function enterCity(id: string, period: string | null) {
  const st = useStore.getState();
  if (st.cityId === id && st.city) {
    if (period && st.periodId !== period) {
      st.setPeriod(period);
      st.dismissChange();
    }
    return;
  }
  st.setLoading(id);
  try {
    const city = await loadCity(id);
    useStore.getState().setCity(id, city, period);
  } catch (e) {
    useStore.getState().setError((e as Error).message);
  }
}

/** Read the address bar into the navigation state (first load and the back button). */
export function syncFromUrl() {
  const r = parsePath(location.pathname);
  if (r.view === "city") return openCityAt(r.city, r.segment, new URLSearchParams(location.search));
  if (r.view === "room") {
    useNav.setState({ view: "room", atlasId: r.atlasId && atlasCatalog.atlases.some((x) => x.id === r.atlasId) ? r.atlasId : null, flight: null });
    return;
  }
  useNav.setState({ view: "title", atlasId: null, flight: null });
}

/**
 * A city from the address: `segment` names an era or a monument (or neither), resolved once the pack has
 * loaded; ?period, ?hour, ?spot and ?event refine it.
 */
function openCityAt(id: string, segment: string | null, p: URLSearchParams) {
  useNav.setState({ view: "city", atlasId: null, flight: null });
  void loadCity(id)
    .then((city) => {
      const isEra = !!segment && city.periods.some((x) => x.id === segment);
      const landmark = !isEra && segment && city.landmarks.some((l) => l.id === segment) ? segment : null;
      const asked = p.get("period");
      const period = isEra ? segment : asked && city.periods.some((x) => x.id === asked) ? asked : landmark ? monumentEra(city, landmark) : null;
      return enterCity(id, period).then(() => {
        const st = useStore.getState();
        const hour = p.get("hour");
        if (hour) st.setHour(parseFloat(hour));
        if (landmark) st.focus(landmark);
        if (p.get("spot")) st.focusSpot(p.get("spot")!);
        if (p.get("event")) st.focusEvent(p.get("event")!);
        st.dismissChange();
      });
    })
    .catch(() => enterCity(id, null)); // an unknown city: let the city view show its error
}

/*
 * Inside a city the address follows the visitor: changing the era or opening a monument rewrites it in place
 * (no new history entry, so Back still leaves the city), and closing a monument returns to its era's page.
 */
useStore.subscribe((s, prev) => {
  if (useNav.getState().view !== "city" || !s.city || !s.cityId) return;
  if (s.periodId === prev.periodId && s.focusedId === prev.focusedId && s.city === prev.city) return;
  const path = pathFor({ view: "city", city: s.cityId, period: s.periodId, landmark: s.focusedId }, s.city);
  // (bake: the plate baker's dev-only mode, src/CityView.tsx)
  const keep = new URLSearchParams([...new URLSearchParams(location.search)].filter(([k]) => ["hour", "spot", "event", "bake"].includes(k)));
  const next = path + (keep.size ? (path.includes("?") ? "&" : "?") + keep : "");
  if (location.pathname + location.search !== next) history.replaceState(null, "", next);
});

/** Every playable map, for the map case and the title page's shortcuts. */
export function playableMaps() {
  return atlasCatalog.atlases.flatMap((a) => a.maps.filter((m) => m.city).map((m) => ({ atlas: a, map: m })));
}

/* ---------------------------------------------------------------- the visitor's register (this browser only) */

const LOG = "chronoscape.register";
type Log = { travels: string[]; atlases: string[] };
export function readRegister(): Log {
  try {
    return { travels: [], atlases: [], ...JSON.parse(localStorage.getItem(LOG) ?? "{}") };
  } catch {
    return { travels: [], atlases: [] };
  }
}
function remember(kind: keyof Log, item: string) {
  try {
    const r = readRegister();
    r[kind] = [item, ...r[kind].filter((x) => x !== item)].slice(0, 24);
    localStorage.setItem(LOG, JSON.stringify(r));
  } catch {
    /* private mode: nothing is kept */
  }
}

/**
 * Where an unfolded map comes to rest on screen, centred and whole (the sheet's last frame). The city's
 * camera opens looking straight down at exactly this framing, so the paper sheet and the live map line
 * up and the hand-over is invisible.
 */
export function introFit(aspect: number, vw: number, vh: number): { w: number; h: number } {
  const h = Math.min(vh * 0.86, (vw * 0.9) / aspect);
  return { w: h * aspect, h };
}
