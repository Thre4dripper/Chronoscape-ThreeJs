import { create } from "zustand";
import type { City } from "@/content/schema";
import { styleOf, type Style } from "../map/fabric";
import { useStore } from "../store";

/**
 * Regional sets of the little Blender scenes of daily life: who walks the
 * streets, what carries the loads, what the stalls sell and which boats ply the
 * water. Rome's props are the default; a set replaces them for its region and
 * age (camels and dhows in Cairo, sedan chairs and sampans in Edo, porters and
 * canoes in Tenochtitlan, llamas in Cusco, gondolas in Venice). Which props each
 * set has baked is listed in models/props/sets.json; anything missing falls back
 * to Rome's.
 */
export type PropSet = NonNullable<City["world"]["props"]>;

const BY_STYLE: Partial<Record<Style, PropSet>> = {
  courtyard: "islamic", sinic: "eastasian", japanese: "eastasian", mesoamerican: "americas", andean: "andean", sahel: "african", kraal: "african",
};

const useSets = create<{ sets: Record<string, string[]> }>(() => ({ sets: {} }));
let asked = false;
function loadSets() {
  if (asked) return;
  asked = true;
  fetch("/models/props/sets.json")
    .then((r) => (r.ok ? r.json() : {}))
    .then((sets: Record<string, string[]>) => useSets.setState({ sets }))
    .catch(() => {});
}

export const propSetFor = (city: City, style: Style): PropSet | null => city.world.props ?? BY_STYLE[style] ?? null;

/** The era on show's prop set, with the props it has baked. */
export function usePropSet(city: City): { set: PropSet; has: string[] } | null {
  loadSets();
  const periodId = useStore((s) => s.periodId) ?? city.defaultPeriodId;
  const sets = useSets((s) => s.sets);
  const period = city.periods.find((p) => p.id === periodId) ?? city.periods[0];
  const set = propSetFor(city, styleOf(period));
  return set && sets[set] ? { set, has: sets[set] } : null;
}

export function propUrl(s: { set: PropSet; has: string[] } | null, name: string): string {
  return s && s.has.includes(name) ? `/models/props/${s.set}/${name}.glb` : `/models/props/${name}.glb`;
}
