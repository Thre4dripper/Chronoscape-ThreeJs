import type { City, Period, STYLES, Vec2 } from "@/content/schema";
import { polygonArea as polyArea } from "./scatter";
import { OccGrid, clipParcel, obbOverlap, SegGrid, bbox, centroid, distToSeg, hash, inRRect, mulberry32, pointInPolygon, type RRect, type Seg } from "./geom";

/**
 * Procedural urban fabric: city blocks, building lots, courtyards, towers,
 * fields, vineyards and trees, generated deterministically per city + period
 * from the content's block / garden / road polygons. Both the engraved map and
 * the 3D diorama draw from the same data, so they always agree.
 */

export type LotKind = "house" | "court" | "tower" | "villa" | "palazzo" | "hut";
export type Lot = { x: number; y: number; w: number; d: number; a: number; h: number; kind: LotKind; roof: "tile" | "flat"; tone: number; g: number };
/** A city block (insula / isolato): the unit that rises when you hover the map. */
export type Insula = { id: number; x: number; y: number; w: number; d: number; a: number; density: "dense" | "loose"; type: "block" | "court" | "villa" | "palazzo"; lot0: number; lot1: number; hMax: number };
export type FieldKind = "furrow" | "pasture" | "orchard" | "vineyard";
export type Field = { pts: Vec2[]; kind: FieldKind; angle: number; cx: number; cy: number };
export type Tree = { x: number; y: number; r: number };
export type Style = (typeof STYLES)[number];
export type Fabric = { lots: Lot[]; insulae: Insula[]; fields: Field[]; trees: Tree[]; style: Style; index: InsulaIndex; occ: OccGrid };

const cache = new Map<string, Fabric>();

/** Forget one city's street fabric (every era) when it is left. */
export function forgetFabric(city: string) {
  for (const key of [...cache.keys()]) if (key.startsWith(`${city}:`)) cache.delete(key);
}

export function getFabric(city: City, periodId: string): Fabric {
  // while one city hands over to another, the outgoing 3D scene can render once with the new city's era
  if (!city.periods.some((p) => p.id === periodId)) periodId = city.defaultPeriodId;
  const key = `${city.id}:${periodId}`;
  let f = cache.get(key);
  if (!f) {
    f = generate(city, periodId);
    cache.set(key, f);
  }
  return f;
}

/* ---- off the main thread: a worker builds other eras' fabric while the user looks around ---- */

const KINDS: LotKind[] = ["house", "court", "tower", "villa", "palazzo", "hut"];
export type PackedFabric = { lots: Float32Array; lotKind: Uint8Array; insulae: Insula[]; fields: Field[]; trees: Float32Array; style: Style; occ: { W: number; H: number; cell: number; cells: Uint8Array } };

export function packFabric(f: Fabric): { packed: PackedFabric; transfer: ArrayBuffer[] } {
  const lots = new Float32Array(f.lots.length * 8);
  const lotKind = new Uint8Array(f.lots.length);
  f.lots.forEach((l, i) => {
    lots.set([l.x, l.y, l.w, l.d, l.a, l.h, l.tone, l.g], i * 8);
    lotKind[i] = KINDS.indexOf(l.kind) | (l.roof === "flat" ? 128 : 0);
  });
  const trees = new Float32Array(f.trees.length * 3);
  f.trees.forEach((t, i) => trees.set([t.x, t.y, t.r], i * 3));
  const packed: PackedFabric = { lots, lotKind, insulae: f.insulae, fields: f.fields, trees, style: f.style, occ: { W: f.occ.W, H: f.occ.H, cell: f.occ.cell, cells: f.occ.cells } };
  return { packed, transfer: [lots.buffer as ArrayBuffer, lotKind.buffer as ArrayBuffer, trees.buffer as ArrayBuffer, f.occ.cells.buffer as ArrayBuffer] };
}

export function unpackFabric(p: PackedFabric): Fabric {
  const n = p.lotKind.length;
  const lots: Lot[] = new Array(n);
  for (let i = 0; i < n; i++) {
    const o = i * 8, k = p.lotKind[i];
    lots[i] = { x: p.lots[o], y: p.lots[o + 1], w: p.lots[o + 2], d: p.lots[o + 3], a: p.lots[o + 4], h: p.lots[o + 5], tone: p.lots[o + 6], g: p.lots[o + 7], kind: KINDS[k & 127], roof: k & 128 ? "flat" : "tile" };
  }
  const trees: Tree[] = new Array(p.trees.length / 3);
  for (let i = 0; i < trees.length; i++) trees[i] = { x: p.trees[i * 3], y: p.trees[i * 3 + 1], r: p.trees[i * 3 + 2] };
  return { lots, insulae: p.insulae, fields: p.fields, trees, style: p.style, index: new InsulaIndex(p.insulae), occ: new OccGrid(p.occ.W, p.occ.H, p.occ.cell, p.occ.cells) };
}

export const hasFabric = (city: City, periodId: string) => cache.has(`${city.id}:${periodId}`);
export function putFabric(city: City, periodId: string, f: Fabric) {
  const key = `${city.id}:${periodId}`;
  if (!cache.has(key)) cache.set(key, f);
}
export { generate as generateFabric };

export function styleFor(year: number): Style {
  return year < -400 ? "archaic" : year < 500 ? "antique" : year < 1450 ? "medieval" : "early-modern";
}

/** The period's own building tradition, or the Mediterranean one for its year. */
export const styleOf = (p: Period): Style => p.style ?? styleFor(p.year);

type Params = { u: [number, number]; v: [number, number]; street: [number, number]; lot: [number, number]; h: [number, number];
  /** Storey mix: [share, min height, max height]. Overrides h for ordinary houses. */
  mix?: [number, number, number][];
  /** Lots may be this many times deeper than wide (narrow gabled houses, machiya); 1 = square-ish. */
  deep?: number;
  court: number; keep: number; tower: number; palazzo: number; flat: number; jitter: number };

const PARAMS: Record<Style, { dense: Params; loose: Params }> = {
  archaic: {
    dense: { u: [30, 50], v: [26, 44], street: [6, 10], lot: [5, 8], h: [3, 4.5], court: 0, keep: 0.8, tower: 0, palazzo: 0, flat: 0, jitter: 0.5 },
    loose: { u: [34, 60], v: [30, 54], street: [8, 14], lot: [5, 8], h: [3, 4.5], court: 0, keep: 0.6, tower: 0, palazzo: 0, flat: 0, jitter: 0.6 },
  },
  antique: {
    dense: { u: [30, 64], v: [22, 46], street: [4, 7], lot: [8, 17], h: [6, 17], mix: [[0.5, 6, 8], [0.33, 9.5, 12], [0.17, 13, 17]], court: 0.35, keep: 0.96, tower: 0, palazzo: 0, flat: 0.08, jitter: 0.07 },
    loose: { u: [44, 80], v: [34, 62], street: [6, 11], lot: [12, 22], h: [4, 7.5], court: 0.7, keep: 0.5, tower: 0, palazzo: 0, flat: 0.05, jitter: 0.04 },
  },
  medieval: {
    dense: { u: [18, 40], v: [14, 30], street: [3, 5], lot: [6, 12], h: [6, 13], mix: [[0.55, 6, 8.5], [0.35, 9, 11.5], [0.1, 12, 14]], court: 0.12, keep: 0.92, tower: 0.012, palazzo: 0, flat: 0.08, jitter: 0.12 },
    loose: { u: [22, 44], v: [18, 36], street: [4, 7], lot: [7, 12], h: [5, 9], court: 0.25, keep: 0.35, tower: 0.04, palazzo: 0, flat: 0.05, jitter: 0.15 },
  },
  "early-modern": {
    dense: { u: [30, 62], v: [22, 42], street: [5, 8], lot: [10, 20], h: [8, 18], mix: [[0.4, 8, 10.5], [0.45, 11, 14], [0.15, 15, 18]], court: 0.3, keep: 1, tower: 0.004, palazzo: 0.07, flat: 0.05, jitter: 0.05 },
    loose: { u: [36, 66], v: [26, 50], street: [6, 10], lot: [10, 18], h: [7, 12], court: 0.4, keep: 0.5, tower: 0, palazzo: 0.04, flat: 0.05, jitter: 0.06 },
  },
  // northern Europe: narrow gabled houses of timber and plaster, steep roofs, jettied upper floors
  gothic: {
    dense: { u: [20, 44], v: [16, 30], street: [3, 6], lot: [6, 9], deep: 2.4, h: [7, 14], mix: [[0.45, 7, 9.5], [0.4, 10, 12.5], [0.15, 13, 15]], court: 0.08, keep: 0.93, tower: 0.004, palazzo: 0, flat: 0, jitter: 0.12 },
    loose: { u: [24, 50], v: [20, 40], street: [4, 8], lot: [7, 12], h: [5, 9], court: 0.15, keep: 0.4, tower: 0, palazzo: 0, flat: 0, jitter: 0.15 },
  },
  // the Islamic, Persian, Indian, Egyptian and Mesopotamian city: inward-looking courtyard houses with flat roof terraces
  courtyard: {
    dense: { u: [26, 56], v: [22, 44], street: [3, 6], lot: [9, 16], h: [4.5, 10], mix: [[0.5, 4.5, 6.5], [0.4, 7, 9], [0.1, 9.5, 12]], court: 0.55, keep: 0.94, tower: 0, palazzo: 0.03, flat: 1, jitter: 0.14 },
    loose: { u: [40, 80], v: [34, 64], street: [6, 12], lot: [12, 22], h: [4, 7], court: 0.75, keep: 0.45, tower: 0, palazzo: 0, flat: 1, jitter: 0.1 },
  },
  // the Chinese walled ward: single-storey courtyard compounds with grey-tiled roofs
  sinic: {
    dense: { u: [40, 64], v: [34, 56], street: [4, 7], lot: [12, 18], deep: 2.6, h: [4.5, 7], court: 0.75, keep: 0.88, tower: 0, palazzo: 0.04, flat: 0, jitter: 0.02 },
    loose: { u: [50, 84], v: [42, 70], street: [6, 10], lot: [14, 22], deep: 2.6, h: [4, 6], court: 0.8, keep: 0.42, tower: 0, palazzo: 0, flat: 0, jitter: 0.02 },
  },
  // Japanese machiya: narrow, deep timber town houses of one or two storeys
  japanese: {
    dense: { u: [30, 50], v: [24, 40], street: [4, 7], lot: [6, 9], deep: 3, h: [4.5, 8], mix: [[0.55, 4.5, 6], [0.45, 6.5, 8]], court: 0.12, keep: 0.94, tower: 0, palazzo: 0, flat: 0, jitter: 0.02 },
    loose: { u: [40, 70], v: [34, 60], street: [6, 10], lot: [10, 18], h: [4, 6], court: 0.6, keep: 0.45, tower: 0, palazzo: 0, flat: 0, jitter: 0.03 },
  },
  // Mesoamerica: whitewashed adobe and stone compounds around patios, flat roofs
  mesoamerican: {
    dense: { u: [24, 46], v: [22, 42], street: [3, 6], lot: [8, 14], h: [3.5, 5.5], court: 0.6, keep: 0.92, tower: 0, palazzo: 0.02, flat: 1, jitter: 0.03 },
    loose: { u: [30, 56], v: [28, 50], street: [5, 9], lot: [8, 14], h: [3, 4.5], court: 0.5, keep: 0.5, tower: 0, palazzo: 0, flat: 1, jitter: 0.05 },
  },
  // the Andes: kancha, stone-walled enclosures of single rooms with steep thatched roofs
  andean: {
    dense: { u: [30, 50], v: [26, 44], street: [3, 5], lot: [8, 12], h: [3.5, 5], court: 0.75, keep: 0.92, tower: 0, palazzo: 0, flat: 0, jitter: 0.03 },
    loose: { u: [34, 56], v: [30, 50], street: [5, 9], lot: [8, 12], h: [3, 4.5], court: 0.6, keep: 0.5, tower: 0, palazzo: 0, flat: 0, jitter: 0.06 },
  },
  // the Sahel: banco (mud-brick) courtyard houses with flat roofs
  sahel: {
    dense: { u: [22, 44], v: [20, 40], street: [3, 6], lot: [8, 13], h: [3.5, 7], mix: [[0.7, 3.5, 4.5], [0.3, 6, 7.5]], court: 0.6, keep: 0.9, tower: 0, palazzo: 0, flat: 1, jitter: 0.2 },
    loose: { u: [30, 56], v: [26, 50], street: [5, 10], lot: [8, 14], h: [3, 4.5], court: 0.6, keep: 0.5, tower: 0, palazzo: 0, flat: 1, jitter: 0.25 },
  },
  // southern Africa: round daga houses with conical thatch, in walled family yards
  kraal: {
    dense: { u: [26, 44], v: [24, 40], street: [6, 10], lot: [5, 8], h: [3.2, 4.5], court: 0, keep: 0.85, tower: 0, palazzo: 0, flat: 0, jitter: 0.5 },
    loose: { u: [32, 56], v: [30, 50], street: [8, 14], lot: [5, 8], h: [3, 4.2], court: 0, keep: 0.6, tower: 0, palazzo: 0, flat: 0, jitter: 0.6 },
  },
};

function generate(city: City, periodId: string): Fabric {
  const period = city.periods.find((p) => p.id === periodId)!;
  const style = styleOf(period);
  // a city can make its houses taller or lower than the era's default (Rome uses the defaults)
  const hScale = city.world.heightScale ?? 1;
  const rnd = mulberry32(hash(`${city.id}:${periodId}:fabric`));
  const R = (a: number, b: number) => a + (b - a) * rnd();
  const m = city.map;
  const inP = (f: { periods?: string[] }) => !f.periods || f.periods.includes(periodId);
  const [W, H] = m.size;

  /* ---- corridors that must stay clear: roads, water, walls, aqueducts, bridges ---- */
  const segs: Seg[] = [];
  const addPath = (path: Vec2[], hw: number) => {
    for (let i = 1; i < path.length; i++) segs.push({ ax: path[i - 1][0], ay: path[i - 1][1], bx: path[i][0], by: path[i][1], hw });
  };
  const roads = m.roads.filter(inP);
  for (const r of roads) addPath(r.path, r.width / 2 + (r.style === "major" ? 3 : 1.5));
  for (const w of m.water.filter(inP)) addPath(w.path, w.width / 2 + 7);
  for (const w of m.walls.filter(inP)) addPath(w.closed ? [...w.path, w.path[0]] : w.path, 8);
  for (const a of m.aqueducts.filter(inP)) addPath(a.path, 3);
  for (const b of m.bridges.filter(inP)) addPath(b.path, 6);
  const grid = new SegGrid(segs);
  const waterGrid = new SegGrid(m.water.filter(inP).flatMap((w) => w.path.slice(1).map((p, i) => ({ ax: w.path[i][0], ay: w.path[i][1], bx: p[0], by: p[1], hw: w.width / 2 + 10 }))));

  const lmRects: RRect[] = city.landmarks
    .filter((l) => l.activePeriods.includes(periodId))
    .map((l) => ({ cx: l.position[0], cy: l.position[1], hw: (l.footprint[0] * l.scale) / 2 + 7, hd: (l.footprint[1] * l.scale) / 2 + 7, a: (l.rotation * Math.PI) / 180 }));
  const islands = m.islands.filter(inP).map((i) => i.polygon);
  const marsh = m.marsh.filter(inP).map((x) => x.polygon);
  const blocked = (x: number, y: number) => {
    if (x < 60 || y < 60 || x > W - 60 || y > H - 60) return true;
    if (grid.near(x, y)) return true;
    for (const r of lmRects) if (inRRect(x, y, r)) return true;
    for (const p of marsh) if (pointInPolygon(x, y, p)) return true;
    return false;
  };

  const roadSegs = roads.flatMap((r) => r.path.slice(1).map((p, i) => ({ ax: r.path[i][0], ay: r.path[i][1], bx: p[0], by: p[1], major: r.style === "major" })));
  const orientationAt = (x: number, y: number): number => {
    let best = Infinity, ang = 0;
    for (const s of roadSegs) {
      const d = distToSeg(x, y, s) * (s.major ? 0.7 : 1);
      if (d < best) {
        best = d;
        ang = Math.atan2(s.by - s.ay, s.bx - s.ax);
      }
    }
    return ang;
  };

  const lots: Lot[] = [];
  const insulae: Insula[] = [];
  const trees: Tree[] = [];
  const blocks = m.blocks.filter(inP);
  const denseBlocks = blocks.filter((b) => b.density === "dense").map((b) => b.polygon);

  // insulae already laid out, on a coarse grid, for overlap tests (a street's width apart at least)
  const GAP = 3;
  const placedGrid = new Map<number, number[]>();
  const placedRects: [number, number, number, number, number][] = [];
  const PG = 80;
  const placeRect = (x: number, y: number, w: number, d: number, a: number) => {
    const id = placedRects.length;
    placedRects.push([x, y, w, d, a]);
    const r = Math.hypot(w, d) / 2;
    for (let gx = Math.floor((x - r) / PG); gx <= Math.floor((x + r) / PG); gx++)
      for (let gy = Math.floor((y - r) / PG); gy <= Math.floor((y + r) / PG); gy++) {
        const k = gx * 100003 + gy;
        let l = placedGrid.get(k);
        if (!l) placedGrid.set(k, (l = []));
        l.push(id);
      }
  };
  const overlapsPlaced = (x: number, y: number, w: number, d: number, a: number) => {
    const r = Math.hypot(w, d) / 2;
    const seen = new Set<number>();
    for (let gx = Math.floor((x - r) / PG); gx <= Math.floor((x + r) / PG); gx++)
      for (let gy = Math.floor((y - r) / PG); gy <= Math.floor((y + r) / PG); gy++)
        for (const id of placedGrid.get(gx * 100003 + gy) ?? []) {
          if (seen.has(id)) continue;
          seen.add(id);
          const [bx, by, bw, bd, ba] = placedRects[id];
          if (obbOverlap(x, y, w / 2 + GAP / 2, d / 2 + GAP / 2, a, bx, by, bw / 2 + GAP / 2, bd / 2 + GAP / 2, ba)) return true;
        }
    return false;
  };

  for (const block of blocks) {
    const P = PARAMS[style][block.density];
    const poly = block.polygon;
    const [cx0, cy0] = centroid(poly);
    const baseAng = orientationAt(cx0, cy0) + (rnd() - 0.5) * P.jitter * 2;
    const c = Math.cos(baseAng), s = Math.sin(baseAng);
    const proj = poly.map(([x, y]) => [x * c + y * s, -x * s + y * c] as Vec2);
    const b = bbox(proj);
    let v = b.y0;
    while (v < b.y1) {
      const dv = R(P.v[0], P.v[1]);
      let u = b.x0 - rnd() * P.u[0];
      while (u < b.x1) {
        const du = R(P.u[0], P.u[1]);
        const st = R(P.street[0], P.street[1]);
        const cu = u + du / 2, cv = v + dv / 2;
        const ang = baseAng + (rnd() - 0.5) * P.jitter;
        const x = cu * c - cv * s, y = cu * s + cv * c;
        const w = du - st, d = dv - st;
        u += du;
        if (w < 6 || d < 6) continue;
        if (rnd() > P.keep) continue;
        // test the insula: centre, corners and edge midpoints must be inside and clear
        const ca = Math.cos(ang), sa = Math.sin(ang);
        let ok = true, inside = 0;
        for (const [lu, lv] of [[0, 0], [-0.5, -0.5], [0.5, -0.5], [0.5, 0.5], [-0.5, 0.5], [0, -0.5], [0.5, 0], [0, 0.5], [-0.5, 0]]) {
          const px = x + ca * lu * w - sa * lv * d, py = y + sa * lu * w + ca * lv * d;
          if (pointInPolygon(px, py, poly)) inside++;
          if (blocked(px, py)) {
            ok = false;
            break;
          }
        }
        if (!ok || inside < 8) continue;
        if (islands.length && !islands.some((p) => pointInPolygon(x, y, p)) && waterGrid.near(x, y)) continue;
        // never overlap a block already laid out (neighbouring content blocks can meet at different street
        // angles): shrink it to fit the gap, or leave the ground open
        let fit = 0;
        for (const k of [1, 0.86, 0.72]) if (!overlapsPlaced(x, y, w * k, d * k, ang)) {
          fit = k;
          break;
        }
        if (!fit || w * fit < 6 || d * fit < 6) continue;
        placeRect(x, y, w * fit, d * fit, ang);
        emitInsula(x, y, w * fit, d * fit, ang, block.density, P);
      }
      v += dv;
    }
  }

  function emitInsula(x: number, y: number, w: number, d: number, a: number, density: "dense" | "loose", P: Params) {
    const lot0 = lots.length;
    let type: Insula["type"] = "block";
    const g = insulae.length;
    try {
      emitInsulaInner();
    } finally {
      if (lots.length > lot0) {
        let hMax = 0;
        for (let i = lot0; i < lots.length; i++) hMax = Math.max(hMax, lots[i].h);
        insulae.push({ id: g, x, y, w, d, a, density, type, lot0, lot1: lots.length, hMax });
      }
    }
    function emitInsulaInner() {
    const houseH = () => {
      if (!P.mix) return R(P.h[0], P.h[1]);
      let x = rnd();
      for (const [share, lo, hi] of P.mix) {
        if (x < share) return R(lo, hi);
        x -= share;
      }
      const last = P.mix[P.mix.length - 1];
      return R(last[1], last[2]);
    };
    const tone = rnd();
    const ca = Math.cos(a), sa = Math.sin(a);
    const at = (lu: number, lv: number): [number, number] => [x + ca * lu - sa * lv, y + sa * lu + ca * lv];
    const push = (lu: number, lv: number, lw: number, ld: number, kind: LotKind, h: number) => {
      const [px, py] = at(lu, lv);
      lots.push({ x: px, y: py, w: Math.max(1.5, lw - 0.5), d: Math.max(1.5, ld - 0.5), a, h, kind, roof: kind === "court" ? "flat" : rnd() < P.flat ? "flat" : "tile", tone: tone * 0.6 + rnd() * 0.4, g });
    };
    // archaic villages and southern African homesteads: round huts with thatched roofs, a fenced yard
    if (style === "archaic" || style === "kraal") {
      type = "villa";
      const n = 2 + Math.floor(rnd() * 4);
      for (let i = 0; i < n; i++) {
        const lu = (rnd() - 0.5) * (w - 10), lv = (rnd() - 0.5) * (d - 10);
        const [px, py] = at(lu, lv);
        const hw = R(4.5, 7);
        lots.push({ x: px, y: py, w: hw, d: hw * R(0.7, 0.95), a: a + rnd() * Math.PI, h: R(P.h[0], P.h[1]), kind: "hut", roof: "tile", tone: rnd(), g });
      }
      for (let i = 0; i < 2; i++) {
        const [tx, ty] = at((rnd() - 0.5) * w, (rnd() - 0.5) * d);
        trees.push({ x: tx, y: ty, r: R(3, 5) });
      }
      return;
    }
    // villa / domus / garden house in its grounds
    if (density === "loose" && (style === "antique" || style === "courtyard" || style === "sinic" || style === "japanese")) {
      type = "villa";
      const bw = w * R(0.45, 0.65), bd = d * R(0.45, 0.65);
      const ox = (rnd() - 0.5) * (w - bw) * 0.6, oy = (rnd() - 0.5) * (d - bd) * 0.6;
      ring(ox, oy, bw, bd, Math.min(bw, bd) * 0.28, "villa", R(P.h[0], P.h[1]));
      for (let i = 0; i < 6; i++) {
        const lu = (rnd() - 0.5) * w, lv = (rnd() - 0.5) * d;
        if (Math.abs(lu - ox) < bw / 2 + 2 && Math.abs(lv - oy) < bd / 2 + 2) continue;
        const [tx, ty] = at(lu, lv);
        trees.push({ x: tx, y: ty, r: R(2.5, 4.5) });
      }
      return;
    }
    // palazzo with a cortile
    if (rnd() < P.palazzo && w > 30 && d > 22) {
      type = "palazzo";
      ring(0, 0, w, d, Math.min(w, d) * 0.3, "palazzo", R(16, 24));
      return;
    }
    // insula with a central courtyard, or a plain subdivided block
    if (rnd() < P.court && w > 26 && d > 20) {
      type = "court";
      ring(0, 0, w, d, Math.min(R(8, 12), Math.min(w, d) * 0.33), "house", 0);
    } else split(0, 0, w, d, 0);

    function ring(ox: number, oy: number, rw: number, rd: number, depth: number, kind: LotKind, h: number) {
      const strips: [number, number, number, number][] = [
        [ox, oy - rd / 2 + depth / 2, rw, depth],
        [ox, oy + rd / 2 - depth / 2, rw, depth],
        [ox - rw / 2 + depth / 2, oy, depth, rd - depth * 2],
        [ox + rw / 2 - depth / 2, oy, depth, rd - depth * 2],
      ];
      for (const [sx, sy, sw, sd] of strips) {
        if (kind === "house") split(sx, sy, sw, sd, 0);
        else push(sx, sy, sw, sd, kind, h);
      }
      push(ox, oy, rw - depth * 2, rd - depth * 2, "court", 0);
    }

    function split(lu: number, lv: number, lw: number, ld: number, depthLevel: number) {
      const max = R(P.lot[0], P.lot[1]);
      const deep = P.deep ?? 1;
      if ((Math.min(lw, ld) <= max && Math.max(lw, ld) <= max * deep) || depthLevel > 6) {
        if (rnd() < P.tower && lw > 5 && ld > 5) {
          const t = Math.min(lw, ld, R(6, 8.5));
          push(lu, lv, t, t, "tower", R(24, 42));
          return;
        }
        if (density === "dense" && rnd() < 0.05 && lw > 6 && ld > 6) {
          push(lu, lv, lw, ld, "court", 0);
          return;
        }
        push(lu, lv, lw, ld, "house", houseH() * hScale);
        return;
      }
      const t = R(0.35, 0.65);
      // deep plots: cut the long side only while it is too long, then cut the short side down to a narrow frontage
      const cutW = deep > 1 && Math.max(lw, ld) <= max * deep ? lw < ld : lw >= ld;
      if (cutW) {
        const a1 = lw * t;
        split(lu - lw / 2 + a1 / 2, lv, a1, ld, depthLevel + 1);
        split(lu - lw / 2 + a1 + (lw - a1) / 2, lv, lw - a1, ld, depthLevel + 1);
      } else {
        const a1 = ld * t;
        split(lu, lv - ld / 2 + a1 / 2, lw, a1, depthLevel + 1);
        split(lu, lv - ld / 2 + a1 + (ld - a1) / 2, lw, ld - a1, depthLevel + 1);
      }
    }
    }
  }

  /* ---- what is built, as a raster: open land (fields, trees) must never overlap it ---- */
  const occ = new OccGrid(W, H, 4);
  for (const r of roads) addOcc(r.path, r.width / 2 + (r.style === "major" ? 3 : 1.5), OccGrid.WAY);
  for (const w of m.water.filter(inP)) addOcc(w.path, w.width / 2 + 7, OccGrid.WATER);
  for (const w of m.walls.filter(inP)) addOcc(w.closed ? [...w.path, w.path[0]] : w.path, 8, OccGrid.WAY);
  for (const a of m.aqueducts.filter(inP)) addOcc(a.path, 3, OccGrid.WAY);
  for (const b of m.bridges.filter(inP)) addOcc(b.path, 6, OccGrid.WAY);
  function addOcc(path: Vec2[], hw: number, bit: number) {
    for (let i = 1; i < path.length; i++) occ.seg(path[i - 1][0], path[i - 1][1], path[i][0], path[i][1], hw, bit);
  }
  for (const r of lmRects) occ.rect(r.cx, r.cy, r.hw, r.hd, r.a);
  for (const b of insulae) occ.rect(b.x, b.y, b.w / 2, b.d / 2, b.a, 1);
  for (const p of marsh) occ.poly(p);
  // the same obstacles as exact geometry, for crisp parcel edges
  const index = new InsulaIndex(insulae);
  let takenPolys: Vec2[][] = [];
  let takenBoxes: ReturnType<typeof bbox>[] = [];
  const exact = (x: number, y: number) => {
    if (x < 60 || y < 60 || x > W - 60 || y > H - 60) return true;
    if (grid.near(x, y)) return true;
    if (index.at(x, y, 0)) return true;
    for (const r of lmRects) if (Math.abs(x - r.cx) < r.hw + r.hd && Math.abs(y - r.cy) < r.hw + r.hd && inRRect(x, y, r)) return true;
    for (const p of marsh) if (pointInPolygon(x, y, p)) return true;
    for (let i = 0; i < takenPolys.length; i++) {
      const b = takenBoxes[i];
      if (x >= b.x0 && x <= b.x1 && y >= b.y0 && y <= b.y1 && pointInPolygon(x, y, takenPolys[i])) return true;
    }
    return false;
  };
  const centroidOf = (pts: Vec2[]): Vec2 => [pts.reduce((a, q) => a + q[0], 0) / pts.length, pts.reduce((a, q) => a + q[1], 0) / pts.length];
  /** A parcel clipped to open land; big losses retry as four smaller parcels. */
  const parcels = (quad: Vec2[], minArea: number, skip?: (x: number, y: number) => boolean): Vec2[][] => {
    const full = polyArea(quad);
    const [qx, qy] = centroidOf(quad);
    const whole = skip?.(qx, qy) ? null : clipParcel(quad, occ, exact);
    if (whole && polyArea(whole) >= full * 0.45) return [whole];
    const mid = (a: Vec2, b: Vec2): Vec2 => [(a[0] + b[0]) / 2, (a[1] + b[1]) / 2];
    const [a, b, c, d] = quad;
    const e = mid(a, b), f = mid(b, c), g = mid(c, d), h = mid(d, a), o = mid(e, g);
    const out: Vec2[][] = [];
    for (const q of [[a, e, o, h], [e, b, f, o], [o, f, c, g], [h, o, g, d]] as Vec2[][]) {
      const [sx, sy] = centroidOf(q);
      if (skip?.(sx, sy)) continue;
      const piece = clipParcel(q, occ, exact);
      if (piece && polyArea(piece) >= minArea) out.push(piece);
    }
    return out;
  };

  /* ---- gardens: parks become trees, vineyards become row fields ---- */
  const fields: Field[] = [];
  const gardens = m.gardens.filter(inP);
  for (const g of gardens) {
    const b = bbox(g.polygon);
    if (g.kind === "vineyard" || g.kind === "orchard") {
      const step = 70;
      for (let gx = b.x0; gx < b.x1; gx += step)
        for (let gy = b.y0; gy < b.y1; gy += step) {
          const cx = gx + step / 2, cy = gy + step / 2;
          if (!pointInPolygon(cx, cy, g.polygon) || blocked(cx, cy) || denseBlocks.some((p) => pointInPolygon(cx, cy, p))) continue;
          if (lots.length && rnd() < 0.08) continue;
          const j = () => (rnd() - 0.5) * 10;
          const quad: Vec2[] = [[gx + j(), gy + j()], [gx + step + j(), gy + j()], [gx + step + j(), gy + step + j()], [gx + j(), gy + step + j()]];
          const kind: FieldKind = g.kind === "vineyard" && rnd() < 0.8 ? "vineyard" : "orchard";
          const angle = rnd() < 0.5 ? 0 : Math.PI / 2;
          for (const pts of parcels(quad, 500)) {
            const [px, py] = centroidOf(pts);
            fields.push({ pts, kind, angle, cx: px, cy: py });
          }
        }
      continue;
    }
    const step = 13;
    for (let gx = b.x0; gx < b.x1; gx += step)
      for (let gy = b.y0; gy < b.y1; gy += step) {
        const x = gx + (rnd() - 0.5) * step, y = gy + (rnd() - 0.5) * step;
        if (rnd() < 0.35 || !pointInPolygon(x, y, g.polygon) || blocked(x, y) || occ.at(x, y)) continue;
        if (denseBlocks.some((p) => pointInPolygon(x, y, p))) continue;
        trees.push({ x, y, r: R(3, 5.5) });
      }
  }

  // vineyards and parks are taken too: countryside fields stop at their edges
  for (const g of gardens) occ.poly(g.polygon);
  for (const fl of fields) occ.poly(fl.pts);
  takenPolys = gardens.map((g) => g.polygon);
  takenBoxes = takenPolys.map(bbox);

  /* ---- countryside: a patchwork of fields wherever nothing is built ---- */
  const cell = 160;
  const nx = Math.ceil(W / cell) + 1, ny = Math.ceil(H / cell) + 1;
  const lattice: Vec2[] = [];
  for (let j = 0; j < ny; j++) for (let i = 0; i < nx; i++) lattice.push([i * cell + (rnd() - 0.5) * cell * 0.45, j * cell + (rnd() - 0.5) * cell * 0.45]);
  const L = (i: number, j: number) => lattice[j * nx + i];
  const builtUp = blocks.map((b) => b.polygon);
  const gardenPolys = gardens.map((g) => g.polygon);
  for (let j = 0; j < ny - 1; j++)
    for (let i = 0; i < nx - 1; i++) {
      const pts = [L(i, j), L(i + 1, j), L(i + 1, j + 1), L(i, j + 1)];
      const cx = (pts[0][0] + pts[2][0]) / 2, cy = (pts[0][1] + pts[2][1]) / 2;
      if (cx < 80 || cy < 80 || cx > W - 80 || cy > H - 80) continue;
      if (builtUp.some((p) => pointInPolygon(cx, cy, p)) || gardenPolys.some((p) => pointInPolygon(cx, cy, p))) continue;
      if (waterGrid.near(cx, cy, 30) || marsh.some((p) => pointInPolygon(cx, cy, p))) continue;
      if (lmRects.some((r) => inRRect(cx, cy, { ...r, hw: r.hw + 40, hd: r.hd + 40 }))) continue;
      const roll = rnd();
      const kind: FieldKind = style === "antique" ? (roll < 0.5 ? "furrow" : roll < 0.8 ? "pasture" : "orchard") : roll < 0.35 ? "vineyard" : roll < 0.7 ? "furrow" : roll < 0.9 ? "pasture" : "orchard";
      const angle = rnd() * Math.PI;
      const hedge = rnd() < 0.45, he = rnd(), ht = [rnd(), rnd(), rnd()], hr = [R(3, 5), R(3, 5), R(3, 5)];
      for (const piece of parcels(pts, 900, (x, y) => builtUp.some((p) => pointInPolygon(x, y, p)))) {
        const [px, py] = centroidOf(piece);
        fields.push({ pts: piece, kind, angle, cx: px, cy: py });
        // hedgerow trees along one edge, only on open ground
        if (hedge) {
          const e = Math.floor(he * piece.length);
          const [ax, ay] = piece[e], [bx, by] = piece[(e + 1) % piece.length];
          for (let k = 0; k < 3; k++) {
            const x = ax + (bx - ax) * ht[k], y = ay + (by - ay) * ht[k];
            if (!occ.at(x, y)) trees.push({ x, y, r: hr[k] });
          }
        }
      }
    }

  return { lots, insulae, fields, trees, style, index, occ };
}

/** Grid index over block footprints for "which block is under the pointer". */
export class InsulaIndex {
  private cells = new Map<number, number[]>();
  constructor(private insulae: Insula[], private cell = 60) {
    for (const b of insulae) {
      const r = Math.hypot(b.w, b.d) / 2;
      for (let gx = Math.floor((b.x - r) / cell); gx <= Math.floor((b.x + r) / cell); gx++)
        for (let gy = Math.floor((b.y - r) / cell); gy <= Math.floor((b.y + r) / cell); gy++) {
          const k = gx * 100003 + gy;
          let l = this.cells.get(k);
          if (!l) this.cells.set(k, (l = []));
          l.push(b.id);
        }
    }
  }
  /** The block under a point; within `tolerance` metres of a block edge also counts (streets pick the nearest block). */
  at(x: number, y: number, tolerance = 0): Insula | null {
    let best: Insula | null = null, bestD = Infinity;
    const r = Math.ceil(tolerance / this.cell);
    for (let gx = Math.floor(x / this.cell) - r; gx <= Math.floor(x / this.cell) + r; gx++)
      for (let gy = Math.floor(y / this.cell) - r; gy <= Math.floor(y / this.cell) + r; gy++)
        for (const id of this.cells.get(gx * 100003 + gy) ?? []) {
          const b = this.insulae[id];
          const c = Math.cos(b.a), s = Math.sin(b.a);
          const dx = x - b.x, dy = y - b.y;
          const lx = Math.abs(dx * c + dy * s) - b.w / 2, ly = Math.abs(-dx * s + dy * c) - b.d / 2;
          const d = Math.hypot(Math.max(0, lx), Math.max(0, ly));
          if (d <= tolerance && d < bestD) {
            bestD = d;
            best = b;
            if (d === 0) return b;
          }
        }
    return best;
  }
  near(x: number, y: number, r: number): Insula[] {
    const out = new Set<number>();
    for (let gx = Math.floor((x - r) / this.cell); gx <= Math.floor((x + r) / this.cell); gx++)
      for (let gy = Math.floor((y - r) / this.cell); gy <= Math.floor((y + r) / this.cell); gy++)
        for (const id of this.cells.get(gx * 100003 + gy) ?? []) {
          const b = this.insulae[id];
          if (Math.hypot(b.x - x, b.y - y) <= r) out.add(id);
        }
    return [...out].map((id) => this.insulae[id]);
  }
}
