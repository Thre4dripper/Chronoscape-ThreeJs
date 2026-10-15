/// <reference lib="webworker" />
import type { City } from "@/content/schema";
import { generateFabric, packFabric } from "./fabric";

/** Builds an era's urban fabric off the main thread; the result comes back packed in typed arrays. */
let city: City | null = null;
self.onmessage = (e: MessageEvent<{ type: "city"; city: City } | { type: "gen"; id: number; periodId: string }>) => {
  const m = e.data;
  if (m.type === "city") {
    city = m.city;
    return;
  }
  if (!city) return;
  const { packed, transfer } = packFabric(generateFabric(city, m.periodId));
  (self as unknown as Worker).postMessage({ id: m.id, periodId: m.periodId, packed }, transfer);
};
