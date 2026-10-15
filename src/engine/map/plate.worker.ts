/// <reference lib="webworker" />
import type { City } from "@/content/schema";
import { drawPlate, featherEdges, type View } from "./plate";
import { loadPlansFor } from "./plans";
import { loadFonts } from "./canvas";

/**
 * Draws map plates off the main thread. Requests that were superseded before
 * their turn came are skipped, so a fast pan never builds a backlog.
 */
type Req = { type: "draw"; id: number; channel: string; periodId: string; view: View; w: number; h: number; feather: boolean };
type Msg = { type: "init"; city: City } | Req;

let city: City | null = null;
const fonts = loadFonts();
const latest = new Map<string, number>();
let queue: Promise<void> = Promise.resolve();

self.onmessage = (e: MessageEvent<Msg>) => {
  const m = e.data;
  if (m.type === "init") {
    city = m.city;
    return;
  }
  latest.set(m.channel, m.id);
  queue = queue.then(() => run(m)).catch((err) => {
    (self as unknown as Worker).postMessage({ id: m.id, error: String(err) });
  });
};

async function run(m: Req) {
  if (!city || latest.get(m.channel) !== m.id) {
    (self as unknown as Worker).postMessage({ id: m.id, skipped: true });
    return;
  }
  await fonts;
  await loadPlansFor(city, m.periodId, m.view);
  if (latest.get(m.channel) !== m.id) {
    (self as unknown as Worker).postMessage({ id: m.id, skipped: true });
    return;
  }
  const canvas = new OffscreenCanvas(m.w, m.h);
  drawPlate(canvas, city, m.periodId, m.view);
  if (m.feather) featherEdges(canvas);
  const bitmap = canvas.transferToImageBitmap();
  (self as unknown as Worker).postMessage({ id: m.id, bitmap }, [bitmap]);
}
