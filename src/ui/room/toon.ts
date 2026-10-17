import * as THREE from "three";
import type { Atlas } from "@/content/schema";
import { compassRose, drawMap, hexA, INK, loadLand, project, regionView, spaced, type View } from "@/world/world";

/**
 * The map room's cartoon look: flat toon shading in three tones with ink
 * outlines (drei <Outlines>), warm saturated colours, and parchment textures
 * drawn on canvases with the same engraved map renderer as the title page.
 */
let gradient: THREE.DataTexture | null = null;
export function toonGradient() {
  if (!gradient) {
    gradient = new THREE.DataTexture(new Uint8Array([95, 95, 95, 255, 170, 170, 170, 255, 232, 232, 232, 255, 255, 255, 255, 255]), 4, 1, THREE.RGBAFormat);
    gradient.minFilter = gradient.magFilter = THREE.NearestFilter;
    gradient.generateMipmaps = false;
    gradient.needsUpdate = true;
  }
  return gradient;
}

const mats = new Map<string, THREE.MeshToonMaterial>();
/** A shared toon material for a flat colour. */
export function toon(color: string) {
  let m = mats.get(color);
  if (!m) {
    m = new THREE.MeshToonMaterial({ color, gradientMap: toonGradient() });
    mats.set(color, m);
  }
  return m;
}

// walnut, with gilt for the carving
export const WOOD = "#6e4126", WOOD_DARK = "#3e2314", WOOD_LIGHT = "#8c5733", BRASS = "#c9a24a", GILT = "#d4ae55", PAPER_T = "#f1e3c2", OUTLINE = "#22140b";

export async function fontsReady() {
  await Promise.race([
    Promise.all([document.fonts.load('600 40px "Cinzel"'), document.fonts.load('italic 30px "IM Fell English"'), document.fonts.load('30px "IM Fell English"')]),
    new Promise((r) => setTimeout(r, 2000)),
  ]);
}

function paper(ctx: CanvasRenderingContext2D, w: number, h: number, seed: number) {
  const g = ctx.createLinearGradient(0, 0, w, h);
  g.addColorStop(0, "#f4e8cb");
  g.addColorStop(1, "#e6d3a9");
  ctx.fillStyle = g;
  ctx.fillRect(0, 0, w, h);
  let s = seed;
  const rnd = () => ((s = (s * 16807) % 2147483647) / 2147483647);
  for (let i = 0; i < 900; i++) {
    ctx.fillStyle = `rgba(110,80,40,${rnd() * 0.07})`;
    ctx.fillRect(rnd() * w, rnd() * h, 1 + rnd() * 2, 1 + rnd() * 2);
  }
}

function wrapLines(ctx: CanvasRenderingContext2D, text: string, maxW: number) {
  const words = text.split(" ");
  const lines: string[] = [];
  let cur = "";
  for (const w of words) {
    const t = cur ? cur + " " + w : w;
    if (ctx.measureText(t).width > maxW && cur) {
      lines.push(cur);
      cur = w;
    } else cur = t;
  }
  if (cur) lines.push(cur);
  return lines;
}

/** The cover of a folded atlas: title, era, an engraved map of the region with its cities, fold creases. */
export async function coverTexture(a: Atlas, w = 512, h = 712): Promise<THREE.CanvasTexture> {
  const land = await loadLand("50m");
  const c = document.createElement("canvas");
  c.width = w;
  c.height = h;
  const ctx = c.getContext("2d")!;
  paper(ctx, w, h, a.id.length * 97 + 13);
  // frame
  ctx.strokeStyle = INK;
  ctx.lineWidth = 3;
  ctx.strokeRect(14, 14, w - 28, h - 28);
  ctx.lineWidth = 1;
  ctx.strokeRect(22, 22, w - 44, h - 44);
  // title
  ctx.fillStyle = INK;
  ctx.textAlign = "center";
  ctx.textBaseline = "middle";
  let size = 40;
  let lines: string[] = [];
  for (; size > 22; size -= 2) {
    ctx.font = `600 ${size}px "Cinzel", Georgia, serif`;
    lines = wrapLines(ctx, a.title.toUpperCase(), w - 90);
    if (lines.length <= 3) break;
  }
  const top = 66;
  lines.forEach((l, i) => ctx.fillText(l, w / 2, top + i * size * 1.12));
  const afterTitle = top + lines.length * size * 1.12;
  ctx.font = 'italic 26px "IM Fell English", Georgia, serif';
  ctx.fillStyle = hexA(a.color, 1);
  ctx.fillText(a.era, w / 2, afterTitle + 8);
  // the region
  const mx = 40, my = afterTitle + 34, mw = w - 80, mh = h - my - 92;
  const rv = regionView(a.area, mw / mh, 0.45);
  const v: View = { ...rv, x: mx, y: my, w: mw, h: mh };
  drawMap(ctx, v, {
    land,
    graticule: 10,
    highlight: { area: a.area, color: a.color },
    pins: a.maps.map((m) => ({ at: m.at, color: a.color, open: !!m.city, label: m.title })),
    weight: 1.1,
  });
  // where each town sits on the cover, in texture coordinates (the held atlas answers to them)
  const pins = a.maps.map((m) => {
    const [px, py] = project(v, m.at);
    return { u: px / w, v: 1 - py / h, title: m.title };
  });
  ctx.strokeStyle = INK;
  ctx.lineWidth = 1.5;
  ctx.strokeRect(mx, my, mw, mh);
  // foot
  ctx.fillStyle = INK;
  ctx.font = '22px "IM Fell English", Georgia, serif';
  ctx.fillText(a.region, w / 2, h - 66);
  ctx.font = '600 15px "Cinzel", Georgia, serif';
  const open = a.maps.filter((m) => m.city).length;
  spaced(ctx, `${a.maps.length} MAPS${open ? ` · ${open} OPEN` : ""}`, w / 2, h - 40, 3);
  // fold creases: a fold down the middle and across in thirds, catching the light
  const crease = (x0: number, y0: number, x1: number, y1: number, horiz: boolean) => {
    const g = horiz ? ctx.createLinearGradient(0, y0 - 6, 0, y0 + 6) : ctx.createLinearGradient(x0 - 6, 0, x0 + 6, 0);
    g.addColorStop(0, "rgba(90,60,30,0)");
    g.addColorStop(0.45, "rgba(90,60,30,0.16)");
    g.addColorStop(0.55, "rgba(255,250,235,0.25)");
    g.addColorStop(1, "rgba(255,250,235,0)");
    ctx.fillStyle = g;
    if (horiz) ctx.fillRect(x0, y0 - 6, x1 - x0, 12);
    else ctx.fillRect(x0 - 6, y0, 12, y1 - y0);
  };
  crease(w / 2, 0, w / 2, h, false);
  crease(0, h / 3, w, h / 3, true);
  crease(0, (2 * h) / 3, w, (2 * h) / 3, true);
  const t = new THREE.CanvasTexture(c);
  t.colorSpace = THREE.SRGBColorSpace;
  t.anisotropy = 8;
  t.userData.pins = pins;
  return t;
}

/** The cabinet's crest: a parchment banner with rolled ends, lettered in Roman capitals. */
export function cartoucheTexture(title: string, motto: string) {
  const W = 1200, H = 300;
  const c = document.createElement("canvas");
  c.width = W;
  c.height = H;
  const g = c.getContext("2d")!;
  const x0 = 90, x1 = W - 90, y0 = 60, y1 = H - 60;
  // banner body with a gentle wave
  g.beginPath();
  g.moveTo(x0, y0 + 10);
  g.bezierCurveTo(W * 0.35, y0 - 14, W * 0.65, y0 + 30, x1, y0 + 6);
  g.lineTo(x1, y1 - 6);
  g.bezierCurveTo(W * 0.65, y1 + 24, W * 0.35, y1 - 20, x0, y1 + 4);
  g.closePath();
  const grad = g.createLinearGradient(0, y0, 0, y1);
  grad.addColorStop(0, "#f6ebcd");
  grad.addColorStop(1, "#e2cd9c");
  g.fillStyle = grad;
  g.fill();
  g.lineWidth = 5;
  g.strokeStyle = "#3d2a1c";
  g.stroke();
  // rolled ends
  for (const [x, dir] of [[x0, -1], [x1, 1]] as const) {
    g.beginPath();
    g.ellipse(x + dir * 22, (y0 + y1) / 2 + 4, 34, (y1 - y0) / 2 + 8, 0, 0, Math.PI * 2);
    g.fillStyle = "#d9c08a";
    g.fill();
    g.stroke();
    g.beginPath();
    g.ellipse(x + dir * 30, (y0 + y1) / 2 + 4, 14, (y1 - y0) / 2 - 18, 0, 0, Math.PI * 2);
    g.fillStyle = "#b8975e";
    g.fill();
    g.stroke();
  }
  g.fillStyle = "#3d2a1c";
  g.textAlign = "center";
  g.textBaseline = "middle";
  g.font = '700 92px "Cinzel", Georgia, serif';
  spaced(g, title, W / 2, H / 2 - 18, 18);
  g.font = 'italic 40px "IM Fell English", Georgia, serif';
  g.fillStyle = "#8a3f26";
  g.fillText(motto, W / 2, H / 2 + 52);
  const t = new THREE.CanvasTexture(c);
  t.colorSpace = THREE.SRGBColorSpace;
  t.anisotropy = 8;
  return t;
}

/** A drawer front: burl veneer with an inlaid compass rose and a stringing line. */
export function inlayTexture(seed: number) {
  const W = 512, H = 192;
  const c = document.createElement("canvas");
  c.width = W;
  c.height = H;
  const g = c.getContext("2d")!;
  g.fillStyle = "#8c5733";
  g.fillRect(0, 0, W, H);
  let s = seed;
  const rnd = () => ((s = (s * 16807) % 2147483647) / 2147483647);
  for (let i = 0; i < 70; i++) {
    g.strokeStyle = `rgba(${60 + rnd() * 40},${30 + rnd() * 20},14,${0.15 + rnd() * 0.2})`;
    g.lineWidth = 1 + rnd() * 2;
    g.beginPath();
    const y = rnd() * H;
    g.moveTo(0, y);
    g.bezierCurveTo(W * 0.3, y + (rnd() - 0.5) * 40, W * 0.7, y + (rnd() - 0.5) * 40, W, y + (rnd() - 0.5) * 20);
    g.stroke();
  }
  g.strokeStyle = "#e8cf93";
  g.lineWidth = 4;
  g.strokeRect(14, 14, W - 28, H - 28);
  g.strokeStyle = "#3e2314";
  g.lineWidth = 2;
  g.strokeRect(22, 22, W - 44, H - 44);
  g.fillStyle = "#c79a5c";
  g.beginPath();
  g.arc(W / 2, H / 2, 66, 0, Math.PI * 2);
  g.fill();
  compassRose(g, W / 2, H / 2, 58);
  const t = new THREE.CanvasTexture(c);
  t.colorSpace = THREE.SRGBColorSpace;
  t.anisotropy = 8;
  return t;
}

/** A small engraved label: a Roman numeral plaque, or the crest of the cabinet. */
export function labelTexture(text: string, w: number, h: number, opts: { bg: string; fg: string; size: number; font?: string; spacing?: number }) {
  const c = document.createElement("canvas");
  c.width = w;
  c.height = h;
  const ctx = c.getContext("2d")!;
  ctx.fillStyle = opts.bg;
  ctx.fillRect(0, 0, w, h);
  ctx.strokeStyle = opts.fg;
  ctx.lineWidth = Math.max(2, h / 24);
  ctx.strokeRect(ctx.lineWidth * 1.5, ctx.lineWidth * 1.5, w - ctx.lineWidth * 3, h - ctx.lineWidth * 3);
  ctx.fillStyle = opts.fg;
  ctx.font = opts.font ?? `600 ${opts.size}px "Cinzel", Georgia, serif`;
  ctx.textAlign = "center";
  ctx.textBaseline = "middle";
  spaced(ctx, text, w / 2, h / 2 + opts.size * 0.05, opts.spacing ?? opts.size * 0.2);
  const t = new THREE.CanvasTexture(c);
  t.colorSpace = THREE.SRGBColorSpace;
  t.anisotropy = 8;
  return t;
}

/** The globe's skin: an engraved world on the equirectangular grid three's sphere expects. */
export async function globeCanvas(): Promise<HTMLCanvasElement> {
  const land = await loadLand("110m");
  const c = document.createElement("canvas");
  c.width = 2048;
  c.height = 1024;
  const ctx = c.getContext("2d")!;
  drawMap(ctx, { lon0: -180, lon1: 180, lat0: -90, lat1: 90, x: 0, y: 0, w: 2048, h: 1024 }, { land, graticule: 15, weight: 1.6, sea: "#d8c79c", paper: "#f2e4c0" });
  return c;
}

export const ROMAN = ["I", "II", "III", "IV", "V", "VI", "VII", "VIII", "IX", "X", "XI", "XII", "XIII", "XIV", "XV", "XVI"];
