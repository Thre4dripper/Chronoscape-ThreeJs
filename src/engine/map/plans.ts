import type { City } from "@/content/schema";
import { ctx2d, makeCanvas, type AnyCanvas } from "./canvas";

/**
 * Engraved top-down plans of the landmark models, rendered in Blender
 * (tools/blender/render_plans.py). Loaded lazily, only for the landmarks a
 * drawing actually covers, and tinted once. Works in a worker.
 */
export type Plan = { size: number; cx: number; cy: number; img: AnyCanvas };
type Meta = { size: number; cx: number; cy: number; ext?: string };

const plans = new Map<string, Plan>();
const pending = new Map<string, Promise<void>>();
let manifest: Promise<Record<string, Meta>> | null = null;

export function planKey(glb: string): string {
  return glb.replace(/^models\//, "").replace(/\.glb$/, "");
}

export function planFor(glb: string): Plan | undefined {
  return plans.get(planKey(glb));
}

function getManifest() {
  if (!manifest) manifest = fetch("/models/plans/manifest.json").then((r) => (r.ok ? r.json() : {})).catch(() => ({}));
  return manifest;
}

async function loadOne(key: string): Promise<void> {
  if (plans.has(key)) return;
  let p = pending.get(key);
  if (!p) {
    p = (async () => {
      const meta = (await getManifest())[key];
      if (!meta) return;
      try {
        const blob = await (await fetch(`/models/plans/${key}.${meta.ext ?? "png"}`)).blob();
        const bmp = await createImageBitmap(blob);
        // warm the sepia plan toward terracotta so monuments stand apart from the ordinary fabric
        const c = makeCanvas(bmp.width, bmp.height);
        const ctx = ctx2d(c);
        ctx.drawImage(bmp, 0, 0);
        ctx.globalCompositeOperation = "source-atop";
        ctx.fillStyle = "rgba(196, 118, 76, 0.16)";
        ctx.fillRect(0, 0, c.width, c.height);
        bmp.close();
        plans.set(key, { size: meta.size, cx: meta.cx, cy: meta.cy, img: c });
      } catch {
        /* the map falls back to a drawn plan */
      }
    })();
    pending.set(key, p);
  }
  return p;
}

/** Load the plans for landmarks standing in `periodId` whose footprint touches the view (map units). */
export async function loadPlansFor(city: City, periodId: string, view: { x0: number; y0: number; x1: number; y1: number }): Promise<void> {
  const keys: string[] = [];
  for (const l of city.landmarks) {
    if (!l.activePeriods.includes(periodId)) continue;
    const r = Math.max(l.footprint[0], l.footprint[1]) * l.scale;
    const [x, y] = l.position;
    if (x + r < view.x0 || x - r > view.x1 || y + r < view.y0 || y - r > view.y1) continue;
    const m = l.variants[periodId]?.model ?? l.model;
    if (m && "glb" in m) keys.push(planKey(m.glb));
  }
  await Promise.all(keys.map(loadOne));
}
