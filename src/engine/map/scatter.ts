import type { Vec2 } from "@/content/schema";
import { mulberry32, pointInPolygon } from "./geom";

/** Deterministic points inside a polygon on a jittered grid. */
export function scatterInPolygon(poly: Vec2[], spacing: number, seed: number, jitter = 0.4, cap = 3000): Vec2[] {
  let x0 = Infinity, y0 = Infinity, x1 = -Infinity, y1 = -Infinity;
  for (const [x, y] of poly) {
    x0 = Math.min(x0, x);
    y0 = Math.min(y0, y);
    x1 = Math.max(x1, x);
    y1 = Math.max(y1, y);
  }
  const rnd = mulberry32(seed);
  const out: Vec2[] = [];
  for (let y = y0 + spacing / 2; y < y1; y += spacing)
    for (let x = x0 + spacing / 2; x < x1; x += spacing) {
      const px = x + (rnd() - 0.5) * spacing * jitter * 2, py = y + (rnd() - 0.5) * spacing * jitter * 2;
      if (pointInPolygon(px, py, poly)) out.push([px, py]);
      if (out.length >= cap) return out;
    }
  return out;
}

/** Points along parallel rows at an angle, clipped to a polygon (vine rows, orchards). */
export function rowsInPolygon(poly: Vec2[], angle: number, rowGap: number, step: number, cap = 3000): Vec2[] {
  let cx = 0, cy = 0;
  for (const [x, y] of poly) {
    cx += x;
    cy += y;
  }
  cx /= poly.length;
  cy /= poly.length;
  let R = 0;
  for (const [x, y] of poly) R = Math.max(R, Math.hypot(x - cx, y - cy));
  const c = Math.cos(angle), s = Math.sin(angle);
  const out: Vec2[] = [];
  for (let k = -R; k <= R; k += rowGap)
    for (let t = -R; t <= R; t += step) {
      const x = cx + c * t - s * k, y = cy + s * t + c * k;
      if (pointInPolygon(x, y, poly)) out.push([x, y]);
      if (out.length >= cap) return out;
    }
  return out;
}

export function polygonArea(poly: Vec2[]): number {
  let a = 0;
  for (let i = 0, j = poly.length - 1; i < poly.length; j = i++) a += (poly[j][0] + poly[i][0]) * (poly[j][1] - poly[i][1]);
  return Math.abs(a / 2);
}

/** Distance from a point to the nearest edge of a polygon. */
export function distToEdges(x: number, y: number, poly: Vec2[]): number {
  let best = Infinity;
  for (let i = 0, j = poly.length - 1; i < poly.length; j = i++) {
    const [ax, ay] = poly[j], [bx, by] = poly[i];
    const dx = bx - ax, dy = by - ay;
    const L2 = dx * dx + dy * dy || 1;
    const t = Math.max(0, Math.min(1, ((x - ax) * dx + (y - ay) * dy) / L2));
    best = Math.min(best, Math.hypot(x - ax - dx * t, y - ay - dy * t));
  }
  return best;
}

/** Does a rotated rectangle (half sizes hx across, hy along `angle`) sit wholly inside the polygon? */
export function rectInPolygon(poly: Vec2[], cx: number, cy: number, angle: number, hx: number, hy: number): boolean {
  const ax = Math.cos(angle), ay = Math.sin(angle); // along
  const px = -ay, py = ax; // across
  for (const [u, v] of [[-1, -1], [1, -1], [1, 1], [-1, 1], [0, -1], [0, 1], [-1, 0], [1, 0]]) {
    const x = cx + ax * hy * v + px * hx * u, y = cy + ay * hy * v + py * hx * u;
    if (!pointInPolygon(x, y, poly)) return false;
  }
  // a reflex corner of the polygon poking into the rectangle
  for (const [x, y] of poly) {
    const dx = x - cx, dy = y - cy;
    if (Math.abs(dx * ax + dy * ay) < hy && Math.abs(dx * px + dy * py) < hx) return false;
  }
  return true;
}
