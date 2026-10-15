import type { City } from "@/content/schema";
import { hasFabric, putFabric, unpackFabric, type PackedFabric } from "./fabric";

/**
 * Warm every era's fabric in a worker, nearest era first, so switching eras
 * never waits for lots, fields and the occupancy grid to be laid out.
 * Unpacking on the main thread is a few milliseconds per era.
 */
let worker: Worker | null = null;
let workerCity: string | null = null;
let seq = 0;
const pending = new Map<number, () => void>();

export function prefetchFabrics(city: City, periodIds: string[]): () => void {
  let cancelled = false;
  if (!worker) {
    worker = new Worker(new URL("./fabric.worker.ts", import.meta.url), { type: "module" });
    worker.onmessage = (e: MessageEvent<{ id: number; periodId: string; packed: PackedFabric }>) => {
      const done = pending.get(e.data.id);
      pending.delete(e.data.id);
      if (workerCity && !hasFabric(currentCity!, e.data.periodId)) putFabric(currentCity!, e.data.periodId, unpackFabric(e.data.packed));
      done?.();
    };
  }
  if (workerCity !== city.id) {
    worker.postMessage({ type: "city", city });
    workerCity = city.id;
  }
  currentCity = city;
  const queue = periodIds.filter((p) => !hasFabric(city, p));
  const next = () => {
    if (cancelled) return;
    const p = queue.shift();
    if (!p) return;
    if (hasFabric(city, p)) return next();
    const id = ++seq;
    pending.set(id, next);
    worker!.postMessage({ type: "gen", id, periodId: p });
  };
  next();
  return () => {
    cancelled = true;
  };
}
let currentCity: City | null = null;
