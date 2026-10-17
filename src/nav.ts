import { create } from "zustand";
import type { AtlasMap } from "@/content/schema";
import { atlasCatalog, loadCity } from "@/content/registry";
import { useStore } from "@/engine/store";

/**
 * Where the visitor is: the title page, the map room (with an atlas open or
 * not), or inside a city map. Kept in the address bar so links, reloads and
 * the back button all work:
 *   /                      title page
 *   ?room                  the map room
 *   ?room=medieval-europe  the map room with that atlas taken off the shelf
 *   ?city=rome&period=…    a city map (existing deep links keep working)
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
  const u = new URL(location.href);
  u.search = "";
  if (view === "room") u.search = atlasId ? `?room=${atlasId}` : "?room";
  if (view === "city" && city) {
    u.searchParams.set("city", city);
    if (period) u.searchParams.set("period", period);
  }
  return u.toString();
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
  const p = new URLSearchParams(location.search);
  const city = p.get("city");
  if (city) {
    useNav.setState({ view: "city", atlasId: null, flight: null });
    void enterCity(city, p.get("period")).then(() => {
      const st = useStore.getState();
      const hour = p.get("hour");
      if (hour) st.setHour(parseFloat(hour));
      if (p.get("focus")) st.focus(p.get("focus")!);
      if (p.get("spot")) st.focusSpot(p.get("spot")!);
      if (p.get("event")) st.focusEvent(p.get("event")!);
      st.dismissChange();
    });
    return;
  }
  if (p.has("room")) {
    const a = p.get("room");
    useNav.setState({ view: "room", atlasId: a && atlasCatalog.atlases.some((x) => x.id === a) ? a : null, flight: null });
    return;
  }
  useNav.setState({ view: "title", atlasId: null, flight: null });
}

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
