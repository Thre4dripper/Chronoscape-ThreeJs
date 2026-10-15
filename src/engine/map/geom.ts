import type { Vec2 } from "@/content/schema";

export type Seg = { ax: number; ay: number; bx: number; by: number; hw: number };
export type RRect = { cx: number; cy: number; hw: number; hd: number; a: number };

export function mulberry32(seed: number) {
  let a = seed >>> 0;
  return () => {
    a = (a + 0x6d2b79f5) >>> 0;
    let t = a;
    t = Math.imul(t ^ (t >>> 15), t | 1);
    t ^= t + Math.imul(t ^ (t >>> 7), t | 61);
    return ((t ^ (t >>> 14)) >>> 0) / 4294967296;
  };
}

export function hash(s: string): number {
  let h = 2166136261;
  for (let i = 0; i < s.length; i++) h = Math.imul(h ^ s.charCodeAt(i), 16777619);
  return h >>> 0;
}

export function pointInPolygon(px: number, py: number, poly: Vec2[]): boolean {
  let inside = false;
  for (let i = 0, j = poly.length - 1; i < poly.length; j = i++) {
    const xi = poly[i][0], yi = poly[i][1], xj = poly[j][0], yj = poly[j][1];
    if (yi > py !== yj > py && px < ((xj - xi) * (py - yi)) / (yj - yi) + xi) inside = !inside;
  }
  return inside;
}

export function distToSeg(px: number, py: number, s: { ax: number; ay: number; bx: number; by: number }): number {
  const dx = s.bx - s.ax, dy = s.by - s.ay;
  const L2 = dx * dx + dy * dy || 1;
  let t = ((px - s.ax) * dx + (py - s.ay) * dy) / L2;
  t = t < 0 ? 0 : t > 1 ? 1 : t;
  const x = s.ax + dx * t - px, y = s.ay + dy * t - py;
  return Math.sqrt(x * x + y * y);
}

export function inRRect(px: number, py: number, r: RRect): boolean {
  const dx = px - r.cx, dy = py - r.cy;
  const c = Math.cos(r.a), s = Math.sin(r.a);
  const lx = dx * c + dy * s, ly = -dx * s + dy * c;
  return Math.abs(lx) <= r.hw && Math.abs(ly) <= r.hd;
}

export function bbox(pts: Vec2[]) {
  let x0 = Infinity, y0 = Infinity, x1 = -Infinity, y1 = -Infinity;
  for (const [x, y] of pts) {
    if (x < x0) x0 = x;
    if (y < y0) y0 = y;
    if (x > x1) x1 = x;
    if (y > y1) y1 = y;
  }
  return { x0, y0, x1, y1 };
}

export function centroid(pts: Vec2[]): Vec2 {
  let x = 0, y = 0;
  for (const p of pts) {
    x += p[0];
    y += p[1];
  }
  return [x / pts.length, y / pts.length];
}

/** Corner-cutting smoothing for polylines (keeps the end points). */
export function chaikin(pts: Vec2[], iterations = 2): Vec2[] {
  let p = pts;
  for (let k = 0; k < iterations; k++) {
    const out: Vec2[] = [p[0]];
    for (let i = 0; i < p.length - 1; i++) {
      const [x0, y0] = p[i], [x1, y1] = p[i + 1];
      out.push([x0 * 0.75 + x1 * 0.25, y0 * 0.75 + y1 * 0.25], [x0 * 0.25 + x1 * 0.75, y0 * 0.25 + y1 * 0.75]);
    }
    out.push(p[p.length - 1]);
    p = out;
  }
  return p;
}

/** Parallel offset of a polyline using averaged vertex normals. */
export function offsetPath(pts: Vec2[], d: number): Vec2[] {
  return pts.map((p, i) => {
    const a = pts[Math.max(0, i - 1)], b = pts[Math.min(pts.length - 1, i + 1)];
    const dx = b[0] - a[0], dy = b[1] - a[1];
    const L = Math.hypot(dx, dy) || 1;
    return [p[0] + (-dy / L) * d, p[1] + (dx / L) * d] as Vec2;
  });
}

export function pathLength(pts: Vec2[]): number {
  let L = 0;
  for (let i = 1; i < pts.length; i++) L += Math.hypot(pts[i][0] - pts[i - 1][0], pts[i][1] - pts[i - 1][1]);
  return L;
}

export function pointAlong(pts: Vec2[], d: number): { x: number; y: number; angle: number } | null {
  let acc = 0;
  for (let i = 1; i < pts.length; i++) {
    const [x0, y0] = pts[i - 1], [x1, y1] = pts[i];
    const L = Math.hypot(x1 - x0, y1 - y0);
    if (acc + L >= d) {
      const t = L > 0 ? (d - acc) / L : 0;
      return { x: x0 + (x1 - x0) * t, y: y0 + (y1 - y0) * t, angle: Math.atan2(y1 - y0, x1 - x0) };
    }
    acc += L;
  }
  return null;
}

export function rectCorners(x: number, y: number, w: number, d: number, a: number): [number, number, number, number, number, number, number, number] {
  const c = Math.cos(a), s = Math.sin(a);
  const hw = w / 2, hd = d / 2;
  return [
    x - c * hw + s * hd, y - s * hw - c * hd,
    x + c * hw + s * hd, y + s * hw - c * hd,
    x + c * hw - s * hd, y + s * hw + c * hd,
    x - c * hw - s * hd, y - s * hw + c * hd,
  ];
}

/** Uniform grid of segments for fast "is this point near a corridor" queries. */
export class SegGrid {
  private cells = new Map<number, Seg[]>();
  constructor(segs: Seg[], private cell = 120) {
    for (const s of segs) {
      const pad = s.hw;
      const x0 = Math.floor((Math.min(s.ax, s.bx) - pad) / cell), x1 = Math.floor((Math.max(s.ax, s.bx) + pad) / cell);
      const y0 = Math.floor((Math.min(s.ay, s.by) - pad) / cell), y1 = Math.floor((Math.max(s.ay, s.by) + pad) / cell);
      for (let gx = x0; gx <= x1; gx++)
        for (let gy = y0; gy <= y1; gy++) {
          const k = gx * 100003 + gy;
          let l = this.cells.get(k);
          if (!l) this.cells.set(k, (l = []));
          l.push(s);
        }
    }
  }
  near(px: number, py: number, extra = 0): boolean {
    const k = Math.floor(px / this.cell) * 100003 + Math.floor(py / this.cell);
    const l = this.cells.get(k);
    if (!l) return false;
    for (const s of l) if (distToSeg(px, py, s) < s.hw + extra) return true;
    return false;
  }
}

/**
 * Raster of "something is here" at a few metres per cell: houses, monuments,
 * roads, water, walls. Used to keep open land (fields, trees, props) from ever
 * overlapping what is built, in O(1) per query.
 */
export class OccGrid {
  /** Layers: what kind of thing occupies a cell. */
  static readonly BUILT = 1; // houses and monuments
  static readonly WAY = 2; // roads, walls, aqueducts, bridges
  static readonly WATER = 4;
  static readonly LAND = 8; // fields, gardens, marsh
  static readonly ALL = 15;
  readonly cells: Uint8Array;
  readonly nx: number;
  readonly ny: number;
  constructor(readonly W: number, readonly H: number, readonly cell = 4, cells?: Uint8Array) {
    this.nx = Math.ceil(W / cell);
    this.ny = Math.ceil(H / cell);
    this.cells = cells ?? new Uint8Array(this.nx * this.ny);
  }
  at(x: number, y: number, mask = OccGrid.ALL): boolean {
    const i = Math.floor(x / this.cell), j = Math.floor(y / this.cell);
    if (i < 0 || j < 0 || i >= this.nx || j >= this.ny) return true;
    return (this.cells[j * this.nx + i] & mask) !== 0;
  }
  /** Anything in this cell or the eight around it? (A quick "definitely clear" test.) */
  nearAny(x: number, y: number, mask = OccGrid.ALL): boolean {
    const i = Math.floor(x / this.cell), j = Math.floor(y / this.cell);
    for (let dj = -1; dj <= 1; dj++)
      for (let di = -1; di <= 1; di++) {
        const ii = i + di, jj = j + dj;
        if (ii < 0 || jj < 0 || ii >= this.nx || jj >= this.ny) return true;
        if (this.cells[jj * this.nx + ii] & mask) return true;
      }
    return false;
  }
  /** Is anything at all inside an axis-aligned box? */
  anyIn(b: { x0: number; y0: number; x1: number; y1: number }, mask = OccGrid.ALL): boolean {
    const c = this.cell;
    const i0 = Math.max(0, Math.floor(b.x0 / c)), i1 = Math.min(this.nx - 1, Math.floor(b.x1 / c));
    const j0 = Math.max(0, Math.floor(b.y0 / c)), j1 = Math.min(this.ny - 1, Math.floor(b.y1 / c));
    if (i0 > i1 || j0 > j1) return true;
    for (let j = j0; j <= j1; j++) {
      const row = j * this.nx;
      for (let i = i0; i <= i1; i++) if (this.cells[row + i] & mask) return true;
    }
    return false;
  }
  /** Is any cell under a rotated rectangle (half sizes across/along `angle`) in the mask? */
  rectHits(cx: number, cy: number, angle: number, hx: number, hy: number, mask: number): boolean {
    const ax = Math.cos(angle), ay = Math.sin(angle);
    const st = this.cell * 0.75;
    for (let v = -hy; v <= hy + 1e-6; v += Math.min(st, hy * 2 || st))
      for (let u = -hx; u <= hx + 1e-6; u += Math.min(st, hx * 2 || st)) if (this.at(cx + ax * v - ay * u, cy + ay * v + ax * u, mask)) return true;
    return false;
  }
  /** Fill a rotated rectangle (centre, half sizes, angle), grown by a margin. */
  rect(cx: number, cy: number, hw: number, hd: number, a: number, margin = 0, bit = OccGrid.BUILT) {
    hw += margin;
    hd += margin;
    const c = Math.cos(a), s = Math.sin(a);
    const R = Math.hypot(hw, hd);
    this.each(cx - R, cy - R, cx + R, cy + R, bit, (x, y) => {
      const dx = x - cx, dy = y - cy;
      const u = dx * c + dy * s, v = -dx * s + dy * c;
      return Math.abs(u) <= hw && Math.abs(v) <= hd;
    });
  }
  /** Fill a capsule around a segment. */
  seg(ax: number, ay: number, bx: number, by: number, hw: number, bit = OccGrid.WAY) {
    this.each(Math.min(ax, bx) - hw, Math.min(ay, by) - hw, Math.max(ax, bx) + hw, Math.max(ay, by) + hw, bit, (x, y) => distToSeg(x, y, { ax, ay, bx, by }) <= hw);
  }
  poly(pts: Vec2[], bit = OccGrid.LAND) {
    const b = bbox(pts);
    this.each(b.x0, b.y0, b.x1, b.y1, bit, (x, y) => pointInPolygon(x, y, pts));
  }
  private each(x0: number, y0: number, x1: number, y1: number, bit: number, test: (x: number, y: number) => boolean) {
    const c = this.cell;
    const i0 = Math.max(0, Math.floor(x0 / c)), i1 = Math.min(this.nx - 1, Math.floor(x1 / c));
    const j0 = Math.max(0, Math.floor(y0 / c)), j1 = Math.min(this.ny - 1, Math.floor(y1 / c));
    for (let j = j0; j <= j1; j++)
      for (let i = i0; i <= i1; i++) {
        const k = j * this.nx + i;
        if (this.cells[k] & bit) continue;
        if (test((i + 0.5) * c, (j + 0.5) * c)) this.cells[k] |= bit;
      }
  }
}

/** Douglas-Peucker simplification of a closed ring (the first point is kept as the anchor). */
export function simplifyRing(pts: Vec2[], tol: number): Vec2[] {
  if (pts.length < 5) return pts;
  const ext = [...pts, pts[0]];
  const keep = new Uint8Array(ext.length);
  keep[0] = keep[ext.length - 1] = 1;
  const stack: [number, number][] = [[0, ext.length - 1]];
  while (stack.length) {
    const [a, b] = stack.pop()!;
    let best = -1, bd = tol;
    for (let i = a + 1; i < b; i++) {
      const d = distToSeg(ext[i][0], ext[i][1], { ax: ext[a][0], ay: ext[a][1], bx: ext[b][0], by: ext[b][1] });
      if (d > bd) {
        bd = d;
        best = i;
      }
    }
    if (best >= 0) {
      keep[best] = 1;
      stack.push([a, best], [best, b]);
    }
  }
  return pts.filter((_, i) => keep[i]);
}

/**
 * Shrink a parcel so it never covers anything in the occupancy grid: rays from
 * an interior point to points along the boundary stop just before the first
 * occupied spot. The raster finds the hit quickly; `exact` (true geometry: road
 * capsules, house rectangles) then pins it down, so edges along a road come out
 * straight instead of stepped. Returns null when too little open land is left.
 */
export function clipParcel(pts: Vec2[], occ: OccGrid, exact?: (x: number, y: number) => boolean, margin = 3, sample = 8): Vec2[] | null {
  let cx = 0, cy = 0;
  for (const [x, y] of pts) {
    cx += x;
    cy += y;
  }
  cx /= pts.length;
  cy /= pts.length;
  // exact geometry is only consulted next to cells the raster marks: everywhere else is clear
  const hit = (x: number, y: number) => (exact ? occ.nearAny(x, y) && exact(x, y) : occ.at(x, y));
  if (occ.at(cx, cy) || hit(cx, cy)) return null;
  // nothing at all under the parcel's bounding box: it stays as it is
  if (!occ.anyIn(bbox(pts))) return pts;
  const step = occ.cell * 0.75;
  const rays: { ux: number; uy: number; stop: number }[] = [];
  for (let e = 0; e < pts.length; e++) {
    const [ax, ay] = pts[e], [bx, by] = pts[(e + 1) % pts.length];
    const n = Math.max(1, Math.ceil(Math.hypot(bx - ax, by - ay) / sample));
    for (let k = 0; k < n; k++) {
      const px = ax + ((bx - ax) * k) / n, py = ay + ((by - ay) * k) / n;
      const L = Math.hypot(px - cx, py - cy);
      if (L < 1e-6) continue;
      const ux = (px - cx) / L, uy = (py - cy) / L;
      let stop = L;
      for (let t = step; t <= L + 1e-6; t += step) {
        if (!occ.at(cx + ux * t, cy + uy * t)) continue;
        // the raster says "something near here": find the true first hit in fine steps around it
        let first = -1;
        for (let u = Math.max(0, t - step * 2); u <= Math.min(L, t + step * 2); u += 1)
          if (hit(cx + ux * u, cy + uy * u)) {
            // bisect the last metre
            let lo = Math.max(0, u - 1), hi = u;
            for (let b = 0; b < 3; b++) {
              const mid = (lo + hi) / 2;
              if (hit(cx + ux * mid, cy + uy * mid)) hi = mid;
              else lo = mid;
            }
            first = hi;
            break;
          }
        if (first >= 0) {
          stop = Math.max(0, first - margin);
          break;
        }
      }
      rays.push({ ux, uy, stop });
    }
  }
  // Where neighbouring rays stop at very different distances (the edge of a house's "shadow"),
  // step along the ray first, so the outline follows the shadow edge instead of cutting the corner.
  const out: Vec2[] = [];
  for (let i = 0; i < rays.length; i++) {
    const r = rays[i], q = rays[(i + rays.length - 1) % rays.length];
    if (r.stop < q.stop - 1.5) out.push([cx + q.ux * r.stop, cy + q.uy * r.stop]);
    else if (q.stop < r.stop - 1.5) out.push([cx + r.ux * q.stop, cy + r.uy * q.stop]);
    out.push([cx + r.ux * r.stop, cy + r.uy * r.stop]);
  }
  // Joining neighbouring ray ends can still clip the corner of a house: walk every edge in short steps
  // and pull any point that lands on something back toward the centre.
  const clear = (ring: Vec2[]) => {
    for (let i = 0; i < ring.length; i++) {
      const [ax, ay] = ring[i], [bx, by] = ring[(i + 1) % ring.length];
      const n = Math.max(1, Math.ceil(Math.hypot(bx - ax, by - ay)));
      for (let k = 1; k < n; k++) if (hit(ax + ((bx - ax) * k) / n, ay + ((by - ay) * k) / n)) return false;
    }
    return true;
  };
  // usually the outline is already clear
  const first = simplifyRing(out, 1.2);
  if (first.length >= 3 && clear(first)) return first;
  const pull = (x: number, y: number): Vec2 => {
    if (!hit(x, y)) return [x, y];
    const L = Math.hypot(x - cx, y - cy);
    const ux = (x - cx) / L, uy = (y - cy) / L;
    let t = L;
    while (t > 0 && hit(cx + ux * t, cy + uy * t)) t -= 0.5;
    t = Math.max(0, t - margin);
    return [cx + ux * t, cy + uy * t];
  };
  const dense: Vec2[] = [];
  for (let i = 0; i < out.length; i++) {
    const [ax, ay] = out[i], [bx, by] = out[(i + 1) % out.length];
    const n = Math.max(1, Math.ceil(Math.hypot(bx - ax, by - ay) / 2));
    for (let k = 0; k < n; k++) dense.push(pull(ax + ((bx - ax) * k) / n, ay + ((by - ay) * k) / n));
  }
  for (const tol of [1.2, 0.6, 0.3]) {
    const simple = simplifyRing(dense, tol);
    if (simple.length >= 3 && clear(simple)) return simple;
  }
  return dense.length >= 3 ? dense : null;
}

/** Do two rotated rectangles (centre, half sizes, angle) overlap? Separating-axis test. */
export function obbOverlap(ax: number, ay: number, ahw: number, ahd: number, aa: number, bx: number, by: number, bhw: number, bhd: number, ba: number): boolean {
  const dx = bx - ax, dy = by - ay;
  if (Math.hypot(dx, dy) > Math.hypot(ahw, ahd) + Math.hypot(bhw, bhd)) return false;
  const axes = [aa, aa + Math.PI / 2, ba, ba + Math.PI / 2];
  const ca = Math.cos(aa), sa = Math.sin(aa), cb = Math.cos(ba), sb = Math.sin(ba);
  for (const t of axes) {
    const ux = Math.cos(t), uy = Math.sin(t);
    const ra = ahw * Math.abs(ca * ux + sa * uy) + ahd * Math.abs(-sa * ux + ca * uy);
    const rb = bhw * Math.abs(cb * ux + sb * uy) + bhd * Math.abs(-sb * ux + cb * uy);
    if (Math.abs(dx * ux + dy * uy) > ra + rb) return false;
  }
  return true;
}
