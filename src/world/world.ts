/**
 * Engraved world and regional maps drawn on a canvas from Natural Earth
 * coastlines (assets/world, built by scripts/build-world.mjs). One renderer
 * for the title page's drifting world, the map room's globe and the covers of
 * the atlases: parchment, coasts with water-lining, rhumb lines from compass
 * roses, Latin names, and a highlighted region with its cities.
 */
export type LonLat = [number, number];
type Ring = LonLat[];

const cache = new Map<string, Promise<Ring[]>>();
export function loadLand(res: "110m" | "50m" = "110m"): Promise<Ring[]> {
  let p = cache.get(res);
  if (!p) {
    p = fetch(`/world/land-${res}.json`)
      .then((r) => (r.ok ? (r.json() as Promise<Ring[]>) : []))
      .catch(() => []);
    cache.set(res, p);
  }
  return p;
}

export const INK = "#4a3322";
export const PAPER = "#efe2c3";
export const PAPER_DARK = "#e3d1a8";
export const SEA = "#e9dbb8";

/** Equirectangular view of a lon/lat box onto a canvas rectangle. */
export type View = { lon0: number; lat0: number; lon1: number; lat1: number; x: number; y: number; w: number; h: number };
export const project = (v: View, [lon, lat]: LonLat): [number, number] => [v.x + ((lon - v.lon0) / (v.lon1 - v.lon0)) * v.w, v.y + ((v.lat1 - lat) / (v.lat1 - v.lat0)) * v.h];

function path(ctx: CanvasRenderingContext2D, v: View, ring: Ring, shift = 0) {
  ring.forEach((p, i) => {
    const [x, y] = project(v, [p[0] + shift, p[1]]);
    if (i === 0) ctx.moveTo(x, y);
    else ctx.lineTo(x, y);
  });
  ctx.closePath();
}

export type DrawOpts = {
  land: Ring[];
  /** Repeat the land 360 degrees either side (seamless panning world). */
  wrap?: boolean;
  graticule?: number;
  rhumbs?: LonLat[];
  labels?: { text: string; at: LonLat; size: number; italic?: boolean; spacing?: number }[];
  highlight?: { area: LonLat[]; color: string } | null;
  pins?: { at: LonLat; color: string; label?: string; open?: boolean }[];
  /** Line weights scale with this (a 4096-wide world wants ~2). */
  weight?: number;
  paper?: string;
  sea?: string;
};

/** Draw land, sea and decorations for a view. */
export function drawMap(ctx: CanvasRenderingContext2D, v: View, o: DrawOpts) {
  const k = o.weight ?? 1;
  const shifts = o.wrap ? [-360, 0, 360] : [0];
  ctx.save();
  ctx.beginPath();
  ctx.rect(v.x, v.y, v.w, v.h);
  ctx.clip();
  ctx.fillStyle = o.sea ?? SEA;
  ctx.fillRect(v.x, v.y, v.w, v.h);

  // rhumb lines from each compass rose: the portolan web
  if (o.rhumbs?.length) {
    ctx.lineWidth = 0.6 * k;
    for (const r of o.rhumbs) {
      const [cx, cy] = project(v, r);
      for (let i = 0; i < 32; i++) {
        const a = (i / 32) * Math.PI * 2;
        ctx.strokeStyle = i % 4 === 0 ? "rgba(74,51,34,0.22)" : i % 2 === 0 ? "rgba(140,62,38,0.16)" : "rgba(74,90,60,0.12)";
        ctx.beginPath();
        ctx.moveTo(cx, cy);
        ctx.lineTo(cx + Math.cos(a) * v.w * 2, cy + Math.sin(a) * v.w * 2);
        ctx.stroke();
      }
    }
  }
  // graticule
  if (o.graticule) {
    ctx.strokeStyle = "rgba(74,51,34,0.13)";
    ctx.lineWidth = 0.7 * k;
    ctx.setLineDash([3 * k, 4 * k]);
    for (let lon = -180; lon <= 180; lon += o.graticule)
      for (const s of shifts) {
        const [x] = project(v, [lon + s, 0]);
        ctx.beginPath();
        ctx.moveTo(x, v.y);
        ctx.lineTo(x, v.y + v.h);
        ctx.stroke();
      }
    for (let lat = -90; lat <= 90; lat += o.graticule) {
      const [, y] = project(v, [0, lat]);
      ctx.beginPath();
      ctx.moveTo(v.x, y);
      ctx.lineTo(v.x + v.w, y);
      ctx.stroke();
    }
    ctx.setLineDash([]);
  }
  // water-lining: the coast echoed outward in fading strokes, as on engraved charts
  ctx.beginPath();
  for (const s of shifts) for (const ring of o.land) path(ctx, v, ring, s);
  for (const [w, a] of [
    [9, 0.05],
    [6, 0.07],
    [3.5, 0.1],
  ] as const) {
    ctx.strokeStyle = `rgba(74,51,34,${a})`;
    ctx.lineWidth = w * k;
    ctx.lineJoin = "round";
    ctx.stroke();
  }
  // land
  ctx.fillStyle = o.paper ?? PAPER;
  ctx.fill("evenodd");
  // a shaded inner edge, like hachured coasts
  ctx.save();
  ctx.clip("evenodd");
  ctx.strokeStyle = "rgba(120,86,50,0.16)";
  ctx.lineWidth = 5 * k;
  ctx.stroke();
  ctx.restore();
  ctx.strokeStyle = INK;
  ctx.lineWidth = 1.1 * k;
  ctx.stroke();

  // the region of an atlas
  if (o.highlight) {
    for (const s of shifts) {
      ctx.beginPath();
      path(ctx, v, o.highlight.area.map(([a, b]) => [a + s, b] as LonLat));
      ctx.fillStyle = hexA(o.highlight.color, 0.26);
      ctx.fill();
      ctx.setLineDash([6 * k, 4 * k]);
      ctx.strokeStyle = hexA(o.highlight.color, 0.95);
      ctx.lineWidth = 2 * k;
      ctx.stroke();
      ctx.setLineDash([]);
    }
  }
  // names
  for (const l of o.labels ?? [])
    for (const s of o.wrap ? shifts : [0]) {
      const [x, y] = project(v, [l.at[0] + s, l.at[1]]);
      ctx.font = `${l.italic ? "italic " : ""}${l.size * k}px ${l.italic ? '"IM Fell English"' : '"Cinzel", "IM Fell English"'}, Georgia, serif`;
      ctx.fillStyle = l.italic ? "rgba(74,51,34,0.7)" : "rgba(74,51,34,0.8)";
      ctx.textAlign = "center";
      ctx.textBaseline = "middle";
      spaced(ctx, l.text, x, y, (l.spacing ?? 0.3) * l.size * k);
    }
  // cities
  for (const p of o.pins ?? []) {
    const [x, y] = project(v, p.at);
    ctx.fillStyle = p.open ? p.color : PAPER;
    ctx.strokeStyle = INK;
    ctx.lineWidth = 1.2 * k;
    ctx.beginPath();
    ctx.arc(x, y, 4.2 * k, 0, Math.PI * 2);
    ctx.fill();
    ctx.stroke();
    if (p.open) {
      ctx.beginPath();
      ctx.arc(x, y, 7.5 * k, 0, Math.PI * 2);
      ctx.strokeStyle = hexA(p.color, 0.8);
      ctx.stroke();
    }
    if (p.label) {
      ctx.font = `italic ${13 * k}px "IM Fell English", Georgia, serif`;
      ctx.fillStyle = INK;
      ctx.textBaseline = "middle";
      // names that would run off the map's right edge go on the left of their town
      const right = x + 9 * k + ctx.measureText(p.label).width <= v.x + v.w - 4;
      ctx.textAlign = right ? "left" : "right";
      const lx = right ? x + 9 * k : x - 9 * k;
      ctx.lineWidth = 3 * k;
      ctx.strokeStyle = "rgba(239,226,195,0.85)";
      ctx.strokeText(p.label, lx, y);
      ctx.fillText(p.label, lx, y);
    }
  }
  ctx.restore();
}

/** Text with letter spacing, centred. */
export function spaced(ctx: CanvasRenderingContext2D, text: string, x: number, y: number, gap: number) {
  const chars = [...text];
  const widths = chars.map((c) => ctx.measureText(c).width);
  const total = widths.reduce((a, b) => a + b, 0) + gap * (chars.length - 1);
  const align = ctx.textAlign;
  ctx.textAlign = "left";
  let cx = x - total / 2;
  chars.forEach((c, i) => {
    ctx.fillText(c, cx, y);
    cx += widths[i] + gap;
  });
  ctx.textAlign = align;
}

/** A decorative compass rose (16 points, fleur-de-lis north), drawn at x,y with radius r. */
export function compassRose(ctx: CanvasRenderingContext2D, x: number, y: number, r: number, spin = 0) {
  ctx.save();
  ctx.translate(x, y);
  ctx.rotate(spin);
  ctx.lineWidth = Math.max(0.6, r / 90);
  for (const [n, len, w, dark, light] of [
    [16, 0.62, 0.06, "#8c3e26", "#d9a97f"],
    [8, 0.8, 0.09, "#4a3322", "#e8d6ae"],
    [4, 1, 0.13, "#4a3322", "#f3e7c9"],
  ] as const) {
    for (let i = 0; i < n; i++) {
      const a = (i / n) * Math.PI * 2 - Math.PI / 2;
      const tip = [Math.cos(a) * r * len, Math.sin(a) * r * len];
      const side = (s: number) => [Math.cos(a + s * Math.PI / 2) * r * w, Math.sin(a + s * Math.PI / 2) * r * w];
      for (const s of [1, -1]) {
        const [sx, sy] = side(s);
        ctx.beginPath();
        ctx.moveTo(0, 0);
        ctx.lineTo(sx, sy);
        ctx.lineTo(tip[0], tip[1]);
        ctx.closePath();
        ctx.fillStyle = s > 0 ? dark : light;
        ctx.fill();
        ctx.strokeStyle = "rgba(74,51,34,0.8)";
        ctx.stroke();
      }
    }
  }
  ctx.beginPath();
  ctx.arc(0, 0, r * 0.08, 0, Math.PI * 2);
  ctx.fillStyle = "#c9a24a";
  ctx.fill();
  ctx.stroke();
  for (const rr of [0.36, 0.4]) {
    ctx.beginPath();
    ctx.arc(0, 0, r * rr, 0, Math.PI * 2);
    ctx.strokeStyle = "rgba(74,51,34,0.55)";
    ctx.stroke();
  }
  // north mark
  ctx.font = `${r * 0.22}px "Cinzel", Georgia, serif`;
  ctx.fillStyle = "#4a3322";
  ctx.textAlign = "center";
  ctx.textBaseline = "middle";
  ctx.fillText("N", 0, -r * 1.14);
  ctx.restore();
}

/** A small galleon in ink, facing +x (flip with scale(-1,1) for -x). */
export function ship(ctx: CanvasRenderingContext2D, x: number, y: number, s: number, rock = 0, dir = 1) {
  ctx.save();
  ctx.translate(x, y);
  ctx.rotate(rock);
  ctx.scale(s * dir, s);
  ctx.lineWidth = 1 / s;
  ctx.strokeStyle = INK;
  // hull
  ctx.beginPath();
  ctx.moveTo(-14, 0);
  ctx.quadraticCurveTo(-12, 7, 0, 7);
  ctx.quadraticCurveTo(12, 7, 16, -1);
  ctx.lineTo(11, 1);
  ctx.lineTo(-11, 1);
  ctx.lineTo(-15, -3);
  ctx.closePath();
  ctx.fillStyle = "#7a4e2e";
  ctx.fill();
  ctx.stroke();
  // masts and sails
  for (const [mx, h, w] of [
    [-6, 17, 6],
    [2, 21, 7.5],
    [9, 14, 5],
  ]) {
    ctx.beginPath();
    ctx.moveTo(mx, 1);
    ctx.lineTo(mx, -h);
    ctx.stroke();
    for (const [y0, y1, ww] of [
      [-h + 2, -h * 0.55, w * 0.8],
      [-h * 0.52, -2, w],
    ]) {
      ctx.beginPath();
      ctx.moveTo(mx - ww / 2, y0);
      ctx.quadraticCurveTo(mx + ww * 0.25, (y0 + y1) / 2, mx - ww / 2, y1);
      ctx.lineTo(mx + ww / 2, y1);
      ctx.quadraticCurveTo(mx + ww, (y0 + y1) / 2, mx + ww / 2, y0);
      ctx.closePath();
      ctx.fillStyle = "#f6ecd2";
      ctx.fill();
      ctx.stroke();
    }
  }
  // pennant
  ctx.beginPath();
  ctx.moveTo(2, -21);
  ctx.lineTo(9, -19.5);
  ctx.lineTo(2, -18);
  ctx.fillStyle = "#a65238";
  ctx.fill();
  // wake
  ctx.strokeStyle = "rgba(74,51,34,0.35)";
  for (const k of [1, 2]) {
    ctx.beginPath();
    ctx.moveTo(-15 - k * 5, 4 + k);
    ctx.quadraticCurveTo(-20 - k * 6, 5 + k * 2, -26 - k * 7, 4 + k);
    ctx.stroke();
  }
  ctx.restore();
}

/** A sea serpent's coils breaking the water. */
export function serpent(ctx: CanvasRenderingContext2D, x: number, y: number, s: number, t: number) {
  ctx.save();
  ctx.translate(x, y);
  ctx.scale(s, s);
  ctx.lineWidth = 1.2 / s;
  ctx.strokeStyle = INK;
  for (let i = 0; i < 3; i++) {
    const cx = i * 13, h = 6 + Math.sin(t * 1.3 + i) * 1.5;
    ctx.beginPath();
    ctx.moveTo(cx - 5, 0);
    ctx.bezierCurveTo(cx - 5, -h * 1.4, cx + 5, -h * 1.4, cx + 5, 0);
    ctx.fillStyle = i === 0 ? "#6d7a46" : "#7f8c55";
    ctx.fill();
    ctx.stroke();
  }
  // head
  ctx.beginPath();
  ctx.moveTo(-6, 0);
  ctx.quadraticCurveTo(-12, -14, -18, -11);
  ctx.quadraticCurveTo(-21, -9, -17, -7);
  ctx.quadraticCurveTo(-11, -8, -9, 0);
  ctx.fillStyle = "#6d7a46";
  ctx.fill();
  ctx.stroke();
  ctx.beginPath();
  ctx.arc(-16, -10, 0.9, 0, Math.PI * 2);
  ctx.fillStyle = INK;
  ctx.fill();
  // ripples
  ctx.strokeStyle = "rgba(74,51,34,0.4)";
  for (const r of [-14, 33]) {
    ctx.beginPath();
    ctx.moveTo(r - 6, 1);
    ctx.lineTo(r + 6, 1);
    ctx.stroke();
  }
  ctx.restore();
}

export function hexA(hex: string, a: number) {
  const n = parseInt(hex.slice(1), 16);
  return `rgba(${(n >> 16) & 255},${(n >> 8) & 255},${n & 255},${a})`;
}

/** Bounding box of an atlas region, padded and widened to an aspect ratio. */
export function regionView(area: LonLat[], aspect: number, pad = 0.35): Omit<View, "x" | "y" | "w" | "h"> {
  let lon0 = 999, lon1 = -999, lat0 = 999, lat1 = -999;
  for (const [a, b] of area) {
    lon0 = Math.min(lon0, a);
    lon1 = Math.max(lon1, a);
    lat0 = Math.min(lat0, b);
    lat1 = Math.max(lat1, b);
  }
  let w = (lon1 - lon0) * (1 + pad), h = (lat1 - lat0) * (1 + pad);
  const cx = (lon0 + lon1) / 2, cy = (lat0 + lat1) / 2;
  // keep degrees roughly square on the page (shrink lon by cos(lat) for a fair look)
  const kx = Math.cos((cy * Math.PI) / 180);
  if ((w * kx) / h > aspect) h = (w * kx) / aspect;
  else w = (h * aspect) / kx;
  return { lon0: cx - w / 2, lon1: cx + w / 2, lat0: cy - h / 2, lat1: cy + h / 2 };
}

/** Old names for the oceans and continents, for the world views. */
export const WORLD_LABELS: DrawOpts["labels"] = [
  { text: "OCEANVS ATLANTICVS", at: [-38, 24], size: 15, italic: true, spacing: 0.4 },
  { text: "MARE PACIFICVM", at: [-140, 6], size: 17, italic: true, spacing: 0.5 },
  { text: "MARE PACIFICVM", at: [168, 18], size: 13, italic: true, spacing: 0.4 },
  { text: "OCEANVS INDICVS", at: [78, -24], size: 15, italic: true, spacing: 0.4 },
  { text: "OCEANVS AETHIOPICVS", at: [-14, -24], size: 12, italic: true, spacing: 0.3 },
  { text: "EVROPA", at: [16, 52], size: 15, spacing: 0.45 },
  { text: "ASIA", at: [92, 50], size: 22, spacing: 0.7 },
  { text: "AFRICA", at: [20, 6], size: 19, spacing: 0.6 },
  { text: "AMERICA SEPTENTRIONALIS", at: [-100, 47], size: 13, spacing: 0.3 },
  { text: "AMERICA MERIDIONALIS", at: [-60, -14], size: 12, spacing: 0.3 },
  { text: "TERRA AVSTRALIS", at: [134, -26], size: 11, spacing: 0.3 },
];
export const WORLD_ROSES: LonLat[] = [
  [-35, 8],
  [72, -12],
  [-150, 20],
  [150, -8],
];
