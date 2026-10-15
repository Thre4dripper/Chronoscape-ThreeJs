import type { City } from "@/content/schema";
import { drawPlate, featherEdges, PLATE_VERSION, type View } from "./plate";
import { loadPlansFor } from "./plans";
import { loadFonts, makeCanvas } from "./canvas";
import { hash } from "./geom";

/**
 * Supplies map plates as ImageBitmaps without ever blocking the main thread:
 *  - whole-city plates come pre-baked (assets/plates/<city>/<period>.webp) and
 *    are decoded off-thread; if a bake is missing or stale they are drawn in the worker;
 *  - close-up tiles are always drawn in the worker.
 */
export const BASE_EDGE = 4096;

type BakeManifest = { version: number; content: string; periods: Record<string, { full: string; preview: string }> };

export function contentHash(city: City): string {
  return `${PLATE_VERSION}:${hash(JSON.stringify(city)).toString(36)}`;
}

export class PlateService {
  private worker: Worker | null = null;
  private seq = 0;
  private waiting = new Map<number, (b: ImageBitmap | null) => void>();
  private manifest: Promise<BakeManifest | null>;
  private blobs = new Map<string, Promise<Blob | null>>();
  private previews = new Map<string, Promise<Blob | null>>();
  readonly hash: string;

  constructor(private city: City) {
    this.hash = contentHash(city);
    this.manifest = fetch(`/plates/${city.id}/manifest.json`)
      .then((r) => (r.ok ? r.json() : null))
      .then((m: BakeManifest | null) => {
        if (!m) return null;
        if (m.content !== this.hash) {
          console.info(`[plates] baked plates for ${city.id} are stale; drawing in a worker. Run npm run plates:bake.`);
          return null;
        }
        return m;
      })
      .catch(() => null);
    if (typeof Worker !== "undefined" && typeof OffscreenCanvas !== "undefined") {
      this.worker = new Worker(new URL("./plate.worker.ts", import.meta.url), { type: "module" });
      this.worker.onmessage = (e: MessageEvent<{ id: number; bitmap?: ImageBitmap; skipped?: boolean; error?: string }>) => {
        const cb = this.waiting.get(e.data.id);
        this.waiting.delete(e.data.id);
        if (e.data.error) console.warn("[plates]", e.data.error);
        cb?.(e.data.bitmap ?? null);
      };
      this.worker.postMessage({ type: "init", city });
    }
  }

  dispose() {
    this.worker?.terminate();
    this.waiting.forEach((cb) => cb(null));
    this.waiting.clear();
  }

  private fetchBaked(cache: Map<string, Promise<Blob | null>>, periodId: string, which: "full" | "preview"): Promise<Blob | null> {
    let p = cache.get(periodId);
    if (!p) {
      p = this.manifest.then(async (m) => {
        const file = m?.periods[periodId]?.[which];
        if (!file) return null;
        const r = await fetch(`/plates/${this.city.id}/${file}`);
        return r.ok ? r.blob() : null;
      });
      cache.set(periodId, p);
    }
    return p;
  }

  /** Fetch the compressed baked plates for a period (cheap; used to prefetch neighbours). */
  prefetch(periodId: string): Promise<Blob | null> {
    this.fetchBaked(this.previews, periodId, "preview");
    return this.fetchBaked(this.blobs, periodId, "full");
  }

  /** A small preview of the period's plate, if baked: shown at once while the full plate arrives. */
  async preview(periodId: string): Promise<ImageBitmap | null> {
    const blob = await this.fetchBaked(this.previews, periodId, "preview");
    return blob ? createImageBitmap(blob) : null;
  }

  async base(periodId: string): Promise<ImageBitmap | null> {
    const blob = await this.prefetch(periodId);
    if (blob) return createImageBitmap(blob);
    const [MW, MH] = this.city.map.size;
    const k = BASE_EDGE / Math.max(MW, MH);
    return this.draw("base", periodId, { x0: 0, y0: 0, x1: MW, y1: MH }, Math.round(MW * k), Math.round(MH * k), false);
  }

  tile(periodId: string, view: View, px: number): Promise<ImageBitmap | null> {
    return this.draw("tile", periodId, view, px, px, true);
  }

  private draw(channel: string, periodId: string, view: View, w: number, h: number, feather: boolean): Promise<ImageBitmap | null> {
    const id = ++this.seq;
    if (!this.worker) return drawOnMainThread(this.city, periodId, view, w, h, feather);
    return new Promise((resolve) => {
      this.waiting.set(id, resolve);
      this.worker!.postMessage({ type: "draw", id, channel, periodId, view, w, h, feather });
    });
  }
}

async function drawOnMainThread(city: City, periodId: string, view: View, w: number, h: number, feather: boolean) {
  await loadFonts();
  await loadPlansFor(city, periodId, view);
  const c = makeCanvas(w, h);
  drawPlate(c, city, periodId, view);
  if (feather) featherEdges(c);
  return createImageBitmap(c);
}

/** Dev only: lets scripts/bake-plates.mjs render every period's plate in the browser. */
export function installBakeHook(city: City) {
  const w = window as unknown as Record<string, unknown>;
  w.__plateMeta = () => ({ city: city.id, version: PLATE_VERSION, content: contentHash(city), periods: city.periods.map((p) => p.id) });
  w.__bakePlate = async (periodId: string, quality = 0.8) => {
    const [MW, MH] = city.map.size;
    const k = BASE_EDGE / Math.max(MW, MH);
    await loadFonts();
    await loadPlansFor(city, periodId, { x0: 0, y0: 0, x1: MW, y1: MH });
    const c = new OffscreenCanvas(Math.round(MW * k), Math.round(MH * k));
    drawPlate(c, city, periodId, { x0: 0, y0: 0, x1: MW, y1: MH });
    const small = new OffscreenCanvas(Math.round(c.width / 4), Math.round(c.height / 4));
    const sctx = small.getContext("2d")!;
    sctx.imageSmoothingQuality = "high";
    sctx.drawImage(c, 0, 0, small.width, small.height);
    const b64 = async (blob: Blob) => {
      const buf = new Uint8Array(await blob.arrayBuffer());
      let bin = "";
      for (let i = 0; i < buf.length; i += 0x8000) bin += String.fromCharCode(...buf.subarray(i, i + 0x8000));
      return btoa(bin);
    };
    return {
      full: await b64(await c.convertToBlob({ type: "image/webp", quality })),
      preview: await b64(await small.convertToBlob({ type: "image/webp", quality: 0.75 })),
    };
  };
}
