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

type BakeManifest = { version: number; periods: Record<string, { full: string; preview: string; hash: string }> };

/** Texts the plate never draws (they only appear in panels and tooltips): editing them must not redraw it. */
const PROSE = new Set(["blurb", "description", "summary", "details", "feel", "population", "houses", "outskirts", "note", "sources", "sourceIds", "function", "built", "confidence", "activity", "focus"]);

/**
 * Everything one era's plate is drawn from: the map features standing in that era, the monuments
 * standing then (where, how big, which model and so which plan), the era's name, year and house style,
 * and the city's name, frame and palette. Prose is left out, so fact-checking a text never makes a plate stale.
 */
export function plateInputs(city: City, periodId: string) {
  const strip = (o: unknown): unknown =>
    Array.isArray(o) ? o.map(strip) : o && typeof o === "object" ? Object.fromEntries(Object.entries(o).filter(([k]) => !PROSE.has(k)).map(([k, v]) => [k, strip(v)])) : o;
  const inP = (f: unknown) => !(f && typeof f === "object" && "periods" in f && Array.isArray(f.periods)) || f.periods.includes(periodId);
  // lists of features keep only those standing in this era (map.size, a pair of numbers, passes untouched)
  const map = Object.fromEntries(Object.entries(city.map).map(([k, v]) => [k, Array.isArray(v) ? strip((v as unknown[]).filter(inP)) : v]));
  const landmarks = city.landmarks
    .filter((l) => l.activePeriods.includes(periodId))
    .map((l) => ({ id: l.id, category: l.category, position: l.position, rotation: l.rotation, footprint: l.footprint, scale: l.scale, model: l.variants[periodId]?.model ?? l.model }));
  return { id: city.id, name: city.name, world: city.world, period: strip(city.periods.find((p) => p.id === periodId)), map, landmarks };
}

/** The key of one era's baked plate. */
export function periodHash(city: City, periodId: string): string {
  return `${PLATE_VERSION}:${hash(JSON.stringify(plateInputs(city, periodId))).toString(36)}`;
}

/** The plan images (Blender top-down renders) an era's plate uses, as "<city>/<model>" keys. */
export function plansOf(city: City, periodId: string): string[] {
  const keys = plateInputs(city, periodId).landmarks.map((l) => ("glb" in l.model ? l.model.glb.replace(/^models\//, "").replace(/\.glb$/, "") : null));
  return [...new Set(keys.filter((k): k is string => !!k))].sort();
}

export class PlateService {
  private worker: Worker | null = null;
  private seq = 0;
  private waiting = new Map<number, (b: ImageBitmap | null) => void>();
  private manifest: Promise<BakeManifest | null>;
  private blobs = new Map<string, Promise<Blob | null>>();
  private previews = new Map<string, Promise<Blob | null>>();
  constructor(private city: City) {
    // each era's baked plate is used only if it was drawn from exactly this era's inputs; a stale one is
    // drawn in the worker instead, the others stay baked
    this.manifest = fetch(`/plates/${city.id}/manifest.json`)
      .then((r) => (r.ok ? r.json() : null))
      .then((m: BakeManifest | null) => {
        if (!m?.periods) return null;
        const fresh = Object.fromEntries(Object.entries(m.periods).filter(([p, e]) => e.hash === periodHash(city, p)));
        const stale = city.periods.filter((p) => !fresh[p.id]).map((p) => p.id);
        if (stale.length) console.info(`[plates] ${city.id}: no current baked plate for ${stale.join(", ")}; drawing in a worker. Run pnpm plates:bake.`);
        return { ...m, periods: fresh };
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
  w.__plateMeta = () => ({ city: city.id, version: PLATE_VERSION, periods: city.periods.map((p) => ({ id: p.id, hash: periodHash(city, p.id), plans: plansOf(city, p.id) })) });
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
