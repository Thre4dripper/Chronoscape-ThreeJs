import * as THREE from "three";
import { compassRose, drawMap, INK, loadLand, serpent, ship, spaced, WORLD_LABELS, WORLD_ROSES, type View } from "@/world/world";

/**
 * The loose maps of the room, drawn once each on a canvas with the engraved
 * renderer: a Dutch wall map of the world, a portolan chart on its vellum
 * skin, and the open spread of the atlas on the lectern. Each sheet is
 * browned at the edges and foxed, as old paper is.
 */
function rng(seed: number) {
  let s = seed;
  return () => ((s = (s * 16807) % 2147483647) / 2147483647);
}

/** Browned edges and foxing spots over a finished sheet. */
function age(g: CanvasRenderingContext2D, w: number, h: number, seed: number) {
  const r = rng(seed);
  const v = g.createRadialGradient(w / 2, h / 2, Math.min(w, h) * 0.3, w / 2, h / 2, Math.hypot(w, h) * 0.55);
  v.addColorStop(0, "rgba(120,80,40,0)");
  v.addColorStop(1, "rgba(120,80,40,0.3)");
  g.fillStyle = v;
  g.fillRect(0, 0, w, h);
  for (let i = 0; i < 40; i++) {
    g.fillStyle = `rgba(140,96,50,${0.04 + r() * 0.08})`;
    g.beginPath();
    g.arc(r() * w, r() * h, 2 + r() * 9, 0, Math.PI * 2);
    g.fill();
  }
}

function canvasTexture(c: HTMLCanvasElement) {
  const t = new THREE.CanvasTexture(c);
  t.colorSpace = THREE.SRGBColorSpace;
  t.anisotropy = 8;
  return t;
}

/** A neatline with alternating degree bars, as engraved world maps have. */
function degreeBorder(g: CanvasRenderingContext2D, x: number, y: number, w: number, h: number, n: number) {
  g.fillStyle = "#f1e3c0";
  g.fillRect(x - 8, y - 8, w + 16, 8);
  g.fillRect(x - 8, y + h, w + 16, 8);
  g.fillRect(x - 8, y, 8, h);
  g.fillRect(x + w, y, 8, h);
  g.fillStyle = INK;
  for (let i = 0; i < n; i += 2) {
    const a = x + (i / n) * w, b = (1 / n) * w;
    g.fillRect(a, y - 8, b, 4);
    g.fillRect(a, y + h + 4, b, 4);
  }
  const m = Math.round((n * h) / w);
  for (let i = 0; i < m; i += 2) {
    const a = y + (i / m) * h, b = (1 / m) * h;
    g.fillRect(x - 8, a, 4, b);
    g.fillRect(x + w + 4, a, 4, b);
  }
  g.strokeStyle = INK;
  g.lineWidth = 1.5;
  g.strokeRect(x - 8, y - 8, w + 16, h + 16);
  g.strokeRect(x, y, w, h);
}

/** A Dutch wall map of the whole world, with its title over the top. */
export async function worldMapTexture() {
  const land = await loadLand("110m");
  const W = 1024, H = 672;
  const c = document.createElement("canvas");
  c.width = W;
  c.height = H;
  const g = c.getContext("2d")!;
  g.fillStyle = "#efe0bb";
  g.fillRect(0, 0, W, H);
  // the title, lettered across the head of the sheet
  g.fillStyle = INK;
  g.textAlign = "center";
  g.textBaseline = "middle";
  g.font = '600 30px "Cinzel", Georgia, serif';
  spaced(g, "NOVA TOTIVS TERRARVM ORBIS TABVLA", W / 2, 40, 5);
  g.font = 'italic 17px "IM Fell English", Georgia, serif';
  g.fillText("auctore Guiljelmo Blaeuw · Amstelodami", W / 2, 68);
  const v: View = { lon0: -180, lon1: 180, lat0: -62, lat1: 80, x: 44, y: 92, w: W - 88, h: H - 150 };
  drawMap(g, v, { land, wrap: true, graticule: 30, rhumbs: WORLD_ROSES, labels: WORLD_LABELS, weight: 0.8, sea: "#e6d4a8", paper: "#f3e6c4" });
  g.save();
  g.beginPath();
  g.rect(v.x, v.y, v.w, v.h);
  g.clip();
  for (const [lon, lat] of WORLD_ROSES) {
    const x = v.x + ((lon + 180) / 360) * v.w, y = v.y + ((80 - lat) / 142) * v.h;
    compassRose(g, x, y, 30);
  }
  ship(g, v.x + v.w * 0.33, v.y + v.h * 0.62, 0.8, 0.05, 1);
  ship(g, v.x + v.w * 0.86, v.y + v.h * 0.4, 0.7, -0.04, -1);
  serpent(g, v.x + v.w * 0.08, v.y + v.h * 0.72, 0.7, 1.2);
  g.restore();
  degreeBorder(g, v.x, v.y, v.w, v.h, 36);
  // a scale of miles and the date at the foot
  g.fillStyle = INK;
  g.font = 'italic 15px "IM Fell English", Georgia, serif';
  g.textAlign = "left";
  g.fillText("Milliaria Germanica communia", v.x, H - 28);
  for (let i = 0; i < 6; i++) {
    g.fillStyle = i % 2 ? "#f3e6c4" : INK;
    g.fillRect(v.x + 200 + i * 26, H - 34, 26, 7);
  }
  g.strokeRect(v.x + 200, H - 34, 156, 7);
  g.fillStyle = INK;
  g.textAlign = "right";
  g.fillText("Anno MDCXXXV", v.x + v.w, H - 28);
  age(g, W, H, 41);
  return canvasTexture(c);
}

/** A portolan chart of the Mediterranean on a calfskin, its neck to the left; transparent outside the skin. */
export async function portolanTexture() {
  const land = await loadLand("50m");
  const W = 768, H = 512;
  const c = document.createElement("canvas");
  c.width = W;
  c.height = H;
  const g = c.getContext("2d")!;
  // the skin: a rectangle with the rounded neck of the animal at one end
  const skin = new Path2D();
  skin.moveTo(120, 18);
  skin.lineTo(W - 18, 14);
  skin.lineTo(W - 12, H - 16);
  skin.lineTo(120, H - 20);
  skin.bezierCurveTo(80, H - 30, 70, H * 0.68, 22, H * 0.6);
  skin.bezierCurveTo(4, H * 0.55, 4, H * 0.45, 22, H * 0.4);
  skin.bezierCurveTo(70, H * 0.32, 80, 30, 120, 18);
  skin.closePath();
  g.fillStyle = "#d9bd84";
  g.fill(skin);
  g.save();
  g.clip(skin);
  const v: View = { lon0: -12, lon1: 40, lat0: 26, lat1: 50, x: 40, y: 0, w: W - 40, h: H };
  drawMap(g, v, { land, wrap: true, rhumbs: [[15, 38], [-2, 38.5], [29, 36]], weight: 1.4, sea: "#dfc590", paper: "#f3e3bb" });
  // the islands painted in red, blue and gold, as the chart makers of Majorca did
  const isles: [number, number, string][] = [[9, 40, "#a8452f"], [14, 37.5, "#c9a24a"], [24.9, 35.2, "#2f5a7a"], [33.2, 35, "#a8452f"], [2.9, 39.6, "#2f5a7a"]];
  for (const [lon, lat, col] of isles) {
    const x = v.x + ((lon - v.lon0) / (v.lon1 - v.lon0)) * v.w, y = v.y + ((v.lat1 - lat) / (v.lat1 - v.lat0)) * v.h;
    g.fillStyle = col;
    g.globalAlpha = 0.55;
    g.beginPath();
    g.arc(x, y, 9, 0, Math.PI * 2);
    g.fill();
    g.globalAlpha = 1;
  }
  compassRose(g, v.x + ((15 + 12) / 52) * v.w, v.y + ((50 - 38) / 24) * v.h, 46);
  g.fillStyle = "rgba(168,69,47,0.85)";
  g.font = 'italic 22px "IM Fell English", Georgia, serif';
  g.textAlign = "center";
  spaced(g, "MARE MEDITERRANEVM", W * 0.42, H * 0.86, 4);
  g.restore();
  g.strokeStyle = "rgba(74,51,34,0.85)";
  g.lineWidth = 5;
  g.stroke(skin);
  age(g, W, H, 77);
  // keep the outside of the skin clear (age() painted the whole canvas)
  g.globalCompositeOperation = "destination-in";
  g.fillStyle = "#000";
  g.fill(skin);
  g.globalCompositeOperation = "source-over";
  return canvasTexture(c);
}

/** The atlas open on the lectern: a page of text on the left, a map of Europe on the right. */
export async function atlasSpreadTexture() {
  const land = await loadLand("110m");
  const W = 1024, H = 640;
  const c = document.createElement("canvas");
  c.width = W;
  c.height = H;
  const g = c.getContext("2d")!;
  g.fillStyle = "#f2e5c4";
  g.fillRect(0, 0, W, H);
  const r = rng(5);
  // the left page: a heading and blocks of text
  g.fillStyle = INK;
  g.textAlign = "center";
  g.textBaseline = "middle";
  g.font = '600 30px "Cinzel", Georgia, serif';
  spaced(g, "EVROPA", W / 4, 74, 8);
  g.font = 'italic 19px "IM Fell English", Georgia, serif';
  g.fillText("Theatrum Orbis Terrarum · Tab. VI", W / 4, 112);
  g.fillStyle = "rgba(74,51,34,0.55)";
  for (let y = 150, k = 0; y < H - 60; y += 22, k++) {
    if (k % 8 === 7) continue; // a break between paragraphs
    const indent = k < 2 ? 50 : 0; // room for the initial
    const w = k % 8 === 6 ? 200 : 340 + r() * 40;
    g.fillRect(W / 4 - 190 + indent, y, Math.min(380, w) - indent, 5);
  }
  // a red initial
  g.fillStyle = "#a8452f";
  g.fillRect(W / 4 - 190, 144, 40, 34);
  // the right page: the map
  const v: View = { lon0: -14, lon1: 44, lat0: 33, lat1: 66, x: W / 2 + 46, y: 50, w: W / 2 - 92, h: H - 100 };
  drawMap(g, v, { land, wrap: true, graticule: 10, weight: 0.9, sea: "#e8d6aa", paper: "#f3e6c4", labels: [{ text: "EVROPA", at: [16, 54], size: 22, spacing: 0.5 }] });
  g.strokeStyle = INK;
  g.lineWidth = 2;
  g.strokeRect(v.x, v.y, v.w, v.h);
  // the gutter, shaded where the pages dip into the binding
  const gut = g.createLinearGradient(W / 2 - 60, 0, W / 2 + 60, 0);
  gut.addColorStop(0, "rgba(90,60,30,0)");
  gut.addColorStop(0.5, "rgba(90,60,30,0.35)");
  gut.addColorStop(1, "rgba(90,60,30,0)");
  g.fillStyle = gut;
  g.fillRect(W / 2 - 60, 0, 120, H);
  age(g, W, H, 13);
  return canvasTexture(c);
}

/** The plate of an astrolabe: the circles of the tropics and the altitude lines for one latitude, and the hour scale round the rim. */
export function astrolabePlateTexture() {
  const S = 256;
  const c = document.createElement("canvas");
  c.width = c.height = S;
  const g = c.getContext("2d")!;
  g.fillStyle = "#d8b45e";
  g.fillRect(0, 0, S, S);
  g.strokeStyle = "rgba(61,42,28,0.8)";
  g.lineWidth = 1.5;
  const m = S / 2;
  for (const rr of [0.98, 0.84, 0.6, 0.38]) {
    g.beginPath();
    g.arc(m, m, rr * m, 0, Math.PI * 2);
    g.stroke();
  }
  // almucantars: circles of equal altitude, crowding toward the zenith
  g.lineWidth = 1;
  for (let i = 0; i < 9; i++) {
    const rr = 0.6 * m * (1 - i * 0.1);
    g.beginPath();
    g.arc(m, m - 0.22 * m * (i / 9) - 0.12 * m, rr, 0, Math.PI * 2);
    g.stroke();
  }
  // the hour scale on the limb
  for (let i = 0; i < 72; i++) {
    const a = (i / 72) * Math.PI * 2;
    const r0 = i % 6 === 0 ? 0.84 : 0.91;
    g.beginPath();
    g.moveTo(m + Math.cos(a) * r0 * m, m + Math.sin(a) * r0 * m);
    g.lineTo(m + Math.cos(a) * 0.98 * m, m + Math.sin(a) * 0.98 * m);
    g.stroke();
  }
  g.beginPath();
  g.moveTo(0, m);
  g.lineTo(S, m);
  g.moveTo(m, 0);
  g.lineTo(m, S);
  g.stroke();
  return canvasTexture(c);
}

/** The skin of a celestial globe: gold stars and constellation figures on blue, with the ecliptic and the equator. */
export function celestialTexture() {
  const W = 1024, H = 512;
  const c = document.createElement("canvas");
  c.width = W;
  c.height = H;
  const g = c.getContext("2d")!;
  g.fillStyle = "#24364f";
  g.fillRect(0, 0, W, H);
  const r = rng(29);
  // the equator, the ecliptic (a sine on this projection) and the colures
  g.strokeStyle = "rgba(230,200,120,0.75)";
  g.lineWidth = 2;
  g.beginPath();
  g.moveTo(0, H / 2);
  g.lineTo(W, H / 2);
  g.stroke();
  g.lineWidth = 10;
  g.strokeStyle = "rgba(230,200,120,0.22)";
  g.beginPath();
  for (let x = 0; x <= W; x += 8) g.lineTo(x, H / 2 - Math.sin((x / W) * Math.PI * 2) * H * 0.13);
  g.stroke();
  g.lineWidth = 1;
  g.strokeStyle = "rgba(230,200,120,0.35)";
  for (let x = 0; x < W; x += W / 12) {
    g.beginPath();
    g.moveTo(x, 0);
    g.lineTo(x, H);
    g.stroke();
  }
  // constellations: a few stars joined into figures
  for (let k = 0; k < 16; k++) {
    const cx = r() * W, cy = H * 0.12 + r() * H * 0.76;
    const pts = Array.from({ length: 4 + Math.floor(r() * 4) }, () => [cx + (r() - 0.5) * 120, cy + (r() - 0.5) * 80] as const);
    g.strokeStyle = "rgba(240,215,150,0.5)";
    g.beginPath();
    pts.forEach(([x, y], i) => (i ? g.lineTo(x, y) : g.moveTo(x, y)));
    g.stroke();
    for (const [x, y] of pts) {
      g.fillStyle = "#f3d98a";
      g.beginPath();
      g.arc(x, y, 2.5 + r() * 3, 0, Math.PI * 2);
      g.fill();
    }
  }
  for (let i = 0; i < 260; i++) {
    g.fillStyle = `rgba(243,217,138,${0.4 + r() * 0.5})`;
    g.fillRect(r() * W, r() * H, 1.5, 1.5);
  }
  return canvasTexture(c);
}
