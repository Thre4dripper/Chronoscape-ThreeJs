import type { AtlasMap } from "@/content/schema";

/**
 * Little engraved drawings of buildings, in the manner of the town vignettes
 * on old maps: paper-filled shapes with an ink line and a few strokes of
 * hatching on the shaded side. Drawn on a canvas, standing on (x, y) with a
 * height of about s pixels.
 */
export type Glyph = AtlasMap["glyph"];

const INK = "#3d2a1c", PAPER = "#f4e8c9", SHADE = "#dcc596", ACCENT = "#a65238";

type Ctx = CanvasRenderingContext2D;

function shape(ctx: Ctx, pts: [number, number][], fill = PAPER) {
  ctx.beginPath();
  pts.forEach(([x, y], i) => (i ? ctx.lineTo(x, y) : ctx.moveTo(x, y)));
  ctx.closePath();
  ctx.fillStyle = fill;
  ctx.fill();
  ctx.stroke();
}
function rect(ctx: Ctx, x: number, y: number, w: number, h: number, fill = PAPER) {
  ctx.fillStyle = fill;
  ctx.fillRect(x, y, w, h);
  ctx.strokeRect(x, y, w, h);
}
function hatch(ctx: Ctx, x: number, y: number, w: number, h: number, gap: number) {
  ctx.save();
  ctx.beginPath();
  ctx.rect(x, y, w, h);
  ctx.clip();
  ctx.beginPath();
  for (let k = -h; k < w; k += gap) {
    ctx.moveTo(x + k, y + h);
    ctx.lineTo(x + k + h, y);
  }
  ctx.globalAlpha = 0.55;
  ctx.stroke();
  ctx.restore();
}
function dome(ctx: Ctx, cx: number, base: number, r: number, h: number, fill = PAPER) {
  ctx.beginPath();
  ctx.moveTo(cx - r, base);
  ctx.bezierCurveTo(cx - r, base - h * 1.1, cx + r, base - h * 1.1, cx + r, base);
  ctx.closePath();
  ctx.fillStyle = fill;
  ctx.fill();
  ctx.stroke();
}
function windows(ctx: Ctx, x: number, y: number, w: number, n: number, h: number) {
  ctx.fillStyle = INK;
  for (let i = 0; i < n; i++) ctx.fillRect(x + ((i + 0.5) * w) / n - h * 0.18, y, h * 0.36, h);
}

/** Draw a glyph standing on (x, y), about s pixels tall. */
export function drawGlyph(ctx: Ctx, kind: Glyph, x: number, y: number, s: number) {
  ctx.save();
  ctx.translate(x, y);
  const u = s / 20; // drawn on a 20-unit grid
  ctx.scale(u, u);
  ctx.lineWidth = 1.1 / Math.max(0.6, u * 0.9);
  ctx.strokeStyle = INK;
  ctx.lineJoin = "round";
  const lw = ctx.lineWidth;
  switch (kind) {
    case "temple": {
      shape(ctx, [[-10, -12], [0, -17], [10, -12]]);
      rect(ctx, -10, -12, 20, 2);
      for (let i = 0; i < 6; i++) rect(ctx, -9 + i * 3.4, -10, 1.4, 8.5);
      rect(ctx, -11, -1.5, 22, 1.5, SHADE);
      break;
    }
    case "arena": {
      ctx.beginPath();
      ctx.ellipse(0, -9, 11, 9, 0, Math.PI, 0);
      ctx.lineTo(11, -1);
      ctx.ellipse(0, -1, 11, 3, 0, 0, Math.PI);
      ctx.closePath();
      ctx.fillStyle = PAPER;
      ctx.fill();
      ctx.stroke();
      ctx.beginPath();
      ctx.ellipse(0, -9, 11, 2.6, 0, 0, Math.PI * 2);
      ctx.fillStyle = SHADE;
      ctx.fill();
      ctx.stroke();
      for (const row of [-6.6, -3.6])
        for (let i = 0; i < 7; i++) {
          const ax = -9 + i * 3;
          ctx.beginPath();
          ctx.arc(ax, row + 1.8, 0.9, Math.PI, 0);
          ctx.lineTo(ax + 0.9, row + 2.6);
          ctx.lineTo(ax - 0.9, row + 2.6);
          ctx.closePath();
          ctx.fillStyle = INK;
          ctx.fill();
        }
      break;
    }
    case "obelisk": {
      shape(ctx, [[-1.6, 0], [-1.1, -16], [0, -19], [1.1, -16], [1.6, 0]]);
      hatch(ctx, 0, -16, 1.6, 16, 1.6);
      shape(ctx, [[6, 0], [6.4, -9], [7, -10.5], [7.6, -9], [8, 0]]);
      rect(ctx, -6, -4, 4, 4, SHADE);
      rect(ctx, -9, -1, 18, 1, SHADE);
      break;
    }
    case "ziggurat": {
      rect(ctx, -11, -4, 22, 4);
      rect(ctx, -8, -8, 16, 4);
      rect(ctx, -5, -12, 10, 4);
      rect(ctx, -2.5, -15.5, 5, 3.5, SHADE);
      shape(ctx, [[-1, 0], [-1, -12], [1, -12], [1, 0]], SHADE);
      hatch(ctx, 5, -8, 3, 4, 1.4);
      hatch(ctx, 8, -4, 3, 4, 1.4);
      break;
    }
    case "lighthouse": {
      shape(ctx, [[-5, 0], [-4, -8], [4, -8], [5, 0]]);
      shape(ctx, [[-3, -8], [-2.5, -14], [2.5, -14], [3, -8]]);
      shape(ctx, [[-1.6, -14], [-1.4, -17.5], [1.4, -17.5], [1.6, -14]]);
      ctx.beginPath();
      ctx.arc(0, -19, 1.6, 0, Math.PI * 2);
      ctx.fillStyle = "#e0b04a";
      ctx.fill();
      ctx.stroke();
      ctx.beginPath();
      for (let a = -0.6; a <= 0.6; a += 0.3) {
        ctx.moveTo(2.2 * Math.cos(a), -19 + 2.2 * Math.sin(a));
        ctx.lineTo(5.5 * Math.cos(a), -19 + 5.5 * Math.sin(a));
      }
      ctx.stroke();
      hatch(ctx, 1, -8, 4, 8, 1.5);
      break;
    }
    case "stupa": {
      rect(ctx, -10, -3, 20, 3, SHADE);
      dome(ctx, 0, -3, 8, 9);
      rect(ctx, -2.2, -13.5, 4.4, 2);
      ctx.beginPath();
      ctx.moveTo(0, -13.5);
      ctx.lineTo(0, -19);
      ctx.stroke();
      for (const [yy, w] of [[-17.5, 3], [-16, 4]] as const) {
        ctx.beginPath();
        ctx.moveTo(-w / 2, yy);
        ctx.lineTo(w / 2, yy);
        ctx.stroke();
      }
      ctx.save();
      ctx.beginPath();
      ctx.rect(0, -12, 9, 9);
      ctx.clip();
      hatch(ctx, 0, -12, 9, 9, 1.6);
      ctx.restore();
      break;
    }
    case "dome": {
      rect(ctx, -8, -7, 16, 7);
      dome(ctx, 0, -7, 6, 7, SHADE);
      ctx.beginPath();
      ctx.moveTo(0, -14.5);
      ctx.lineTo(0, -16.5);
      ctx.stroke();
      rect(ctx, 9, -16, 2.4, 16);
      shape(ctx, [[8.6, -16], [10.2, -19], [11.8, -16]], SHADE);
      rect(ctx, 8.4, -11, 3.6, 0.9, SHADE);
      windows(ctx, -8, -5, 16, 4, 3);
      break;
    }
    case "pagoda": {
      for (let i = 0; i < 4; i++) {
        const y0 = -2 - i * 4.2, w = 9 - i * 1.7;
        rect(ctx, -w / 2 + 1, y0 - 2.6, w - 2, 2.6);
        shape(ctx, [[-w / 2 - 1.5, y0 - 2.2], [-w / 2 + 0.5, y0 - 4], [w / 2 - 0.5, y0 - 4], [w / 2 + 1.5, y0 - 2.2]], i % 2 ? SHADE : ACCENT);
      }
      ctx.beginPath();
      ctx.moveTo(0, -19);
      ctx.lineTo(0, -21);
      ctx.stroke();
      rect(ctx, -6, -1, 12, 1, SHADE);
      break;
    }
    case "cathedral": {
      rect(ctx, -9, -9, 18, 9);
      shape(ctx, [[-9, -9], [0, -14], [9, -9]], SHADE);
      rect(ctx, -12, -15, 4, 15);
      shape(ctx, [[-12, -15], [-10, -21], [-8, -15]], SHADE);
      dome(ctx, 3, -14, 3.6, 4);
      ctx.beginPath();
      ctx.arc(0, -5, 2, 0, Math.PI * 2);
      ctx.stroke();
      windows(ctx, -12, -11, 4, 1, 3);
      break;
    }
    case "tower": {
      rect(ctx, -3, -18, 6, 18);
      for (let i = 0; i < 3; i++) rect(ctx, -3 + i * 2.2, -20, 1.4, 2);
      windows(ctx, -3, -14, 6, 2, 3);
      windows(ctx, -3, -8, 6, 1, 3);
      hatch(ctx, 1, -18, 2, 18, 1.4);
      rect(ctx, 4, -8, 7, 8);
      shape(ctx, [[4, -8], [7.5, -11], [11, -8]], ACCENT);
      rect(ctx, -11, -6, 7, 6);
      shape(ctx, [[-11, -6], [-7.5, -9], [-4, -6]], ACCENT);
      break;
    }
    case "mughal": {
      rect(ctx, -9, -8, 18, 8);
      ctx.beginPath();
      ctx.moveTo(-2.5, 0);
      ctx.lineTo(-2.5, -4.5);
      ctx.quadraticCurveTo(0, -7.5, 2.5, -4.5);
      ctx.lineTo(2.5, 0);
      ctx.fillStyle = INK;
      ctx.fill();
      ctx.beginPath();
      ctx.moveTo(-5, -8);
      ctx.bezierCurveTo(-6, -14, -1.5, -15, 0, -18);
      ctx.bezierCurveTo(1.5, -15, 6, -14, 5, -8);
      ctx.closePath();
      ctx.fillStyle = PAPER;
      ctx.fill();
      ctx.stroke();
      for (const sx of [-1, 1]) {
        rect(ctx, sx * 11 - 1, -15, 2, 15);
        dome(ctx, sx * 11, -15, 1.5, 2, SHADE);
        dome(ctx, sx * 6.5, -8, 1.8, 2.2, SHADE);
      }
      break;
    }
    case "adobe": {
      shape(ctx, [[-10, 0], [-9, -9], [-5, -9], [-4.5, -15], [-1, -17], [2.5, -15], [3, -9], [9, -9], [10, 0]], "#e6cfa0");
      ctx.beginPath();
      for (const [px, py] of [[-7, -6], [-3, -12], [0, -14], [5, -6], [-7, -3], [6, -3]]) {
        ctx.moveTo(px - 1.6, py);
        ctx.lineTo(px + 1.6, py);
      }
      ctx.stroke();
      hatch(ctx, 3, -9, 6, 9, 1.6);
      break;
    }
    case "enclosure": {
      ctx.beginPath();
      ctx.ellipse(0, -3, 11, 4, 0, 0, Math.PI * 2);
      ctx.fillStyle = SHADE;
      ctx.fill();
      ctx.stroke();
      ctx.beginPath();
      ctx.ellipse(0, -6.5, 11, 4, 0, Math.PI, 0);
      ctx.lineTo(11, -3);
      ctx.ellipse(0, -3, 11, 4, 0, 0, Math.PI);
      ctx.closePath();
      ctx.fillStyle = PAPER;
      ctx.fill();
      ctx.stroke();
      ctx.beginPath();
      for (let yy = -5.6; yy < -1; yy += 1.2) {
        ctx.moveTo(-10, yy);
        ctx.lineTo(10, yy);
      }
      ctx.globalAlpha = 0.45;
      ctx.stroke();
      ctx.globalAlpha = 1;
      shape(ctx, [[2, -6.5], [3, -14], [4.5, -16], [6, -14], [7, -6.5]]);
      hatch(ctx, 4.5, -16, 2.5, 10, 1.4);
      break;
    }
    case "steps": {
      for (let i = 0; i < 4; i++) rect(ctx, -11 + i * 2.5, -3.5 - i * 3.5, 22 - i * 5, 3.5, i % 2 ? SHADE : PAPER);
      rect(ctx, -3, -18, 6, 3.5, ACCENT);
      shape(ctx, [[-1.5, 0], [-1.5, -14], [1.5, -14], [1.5, 0]], PAPER);
      ctx.beginPath();
      for (let yy = -13; yy < 0; yy += 1.6) {
        ctx.moveTo(-1.5, yy);
        ctx.lineTo(1.5, yy);
      }
      ctx.stroke();
      break;
    }
  }
  void lw;
  ctx.restore();
}

/** A glyph on its own little canvas, for the hover cartouche (rendered once, cached). */
const cache = new Map<string, string>();
export function glyphImage(kind: Glyph, px = 120): string {
  const key = `${kind}:${px}`;
  let u = cache.get(key);
  if (!u) {
    const c = document.createElement("canvas");
    c.width = px;
    c.height = px;
    const ctx = c.getContext("2d")!;
    // a little patch of ground under it
    ctx.fillStyle = "rgba(74,51,34,0.08)";
    ctx.beginPath();
    ctx.ellipse(px / 2, px * 0.86, px * 0.42, px * 0.05, 0, 0, Math.PI * 2);
    ctx.fill();
    drawGlyph(ctx, kind, px / 2, px * 0.86, px * 0.72);
    u = c.toDataURL();
    cache.set(key, u);
  }
  return u;
}
