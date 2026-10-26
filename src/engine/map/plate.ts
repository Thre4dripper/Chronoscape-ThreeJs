import type { City, KitParams, Vec2 } from "@/content/schema";
import { getFabric, type Lot } from "./fabric";
import { planFor } from "./plans";
import { ctx2d, makeCanvas, type AnyCanvas, type Ctx2D } from "./canvas";

/** Bump when the drawing changes, so baked plates are re-baked. */
export const PLATE_VERSION = 11;
import { centroid, chaikin, hash, mulberry32, offsetPath, pathLength, pointAlong, rectCorners } from "./geom";

/**
 * The engraved atlas plate. Everything is drawn in map units through a canvas
 * transform, so one function renders both the whole-city texture and the sharp
 * close-up tiles. Detail is chosen by pixels-per-unit (ppu): hatching, roof
 * ridges, furrows and wells only appear when there are pixels to show them.
 */
export type View = { x0: number; y0: number; x1: number; y1: number };

const PAPER_LIGHT = "#efe2c3";

export function drawPlate(canvas: AnyCanvas, city: City, periodId: string, view: View) {
  const ctx = ctx2d(canvas);
  const W = canvas.width, H = canvas.height;
  const ppu = W / (view.x1 - view.x0);
  const pal = city.map.palette;
  const ink = pal.ink;
  const m = city.map;
  const [MW, MH] = m.size;
  const inP = (f: { periods?: string[] }) => !f.periods || f.periods.includes(periodId);
  const period = city.periods.find((p) => p.id === periodId)!;
  const fabric = getFabric(city, periodId);
  const lw = (units: number, minPx = 0.6) => Math.max(units, minPx / ppu);
  const margin = 40;
  const vis = (x0: number, y0: number, x1: number, y1: number) => x1 >= view.x0 - margin && x0 <= view.x1 + margin && y1 >= view.y0 - margin && y0 <= view.y1 + margin;
  const visPt = (x: number, y: number, r: number) => vis(x - r, y - r, x + r, y + r);
  const visPath = (pts: Vec2[], pad: number) => {
    let x0 = Infinity, y0 = Infinity, x1 = -Infinity, y1 = -Infinity;
    for (const [x, y] of pts) {
      if (x < x0) x0 = x;
      if (y < y0) y0 = y;
      if (x > x1) x1 = x;
      if (y > y1) y1 = y;
    }
    return vis(x0 - pad, y0 - pad, x1 + pad, y1 + pad);
  };

  /* ---------------- paper (screen-space grain + map-space stains) ---------------- */
  ctx.setTransform(1, 0, 0, 1, 0, 0);
  ctx.globalCompositeOperation = "source-over";
  ctx.globalAlpha = 1;
  ctx.fillStyle = pal.parchment;
  ctx.fillRect(0, 0, W, H);
  ctx.save();
  ctx.globalCompositeOperation = "multiply";
  ctx.fillStyle = ctx.createPattern(paperTile(), "repeat")!;
  ctx.fillRect(0, 0, W, H);
  ctx.restore();

  ctx.setTransform(ppu, 0, 0, ppu, -view.x0 * ppu, -view.y0 * ppu);
  {
    const rs = mulberry32(hash(city.id + "stains"));
    for (let i = 0; i < 40; i++) {
      const x = rs() * MW, y = rs() * MH, r = 120 + rs() * 600, a = 0.03 + rs() * 0.05;
      if (!visPt(x, y, r)) continue;
      const g = ctx.createRadialGradient(x, y, 0, x, y, r);
      g.addColorStop(0, hexA(ink, a));
      g.addColorStop(0.7, hexA(ink, a * 0.4));
      g.addColorStop(1, hexA(ink, 0));
      ctx.fillStyle = g;
      ctx.fillRect(x - r, y - r, 2 * r, 2 * r);
    }
  }

  /* ---------------- countryside: fields, vineyards, pasture ---------------- */
  {
    const seed = hash(city.id + periodId + "fields");
    const hedge = new Path2D();
    const stipple = new Path2D();
    fabric.fields.forEach((f, idx) => {
      if (!visPath(f.pts, 10)) return;
      const rf = mulberry32(seed + idx * 7919);
      const poly = new Path2D();
      f.pts.forEach(([x, y], i) => (i === 0 ? poly.moveTo(x, y) : poly.lineTo(x, y)));
      poly.closePath();
      hedge.addPath(poly);
      ctx.fillStyle = f.kind === "pasture" ? hexA(pal.hill, 0.1) : f.kind === "vineyard" ? hexA(pal.hill, 0.15) : f.kind === "orchard" ? hexA(pal.hill, 0.12) : hexA(ink, 0.04 + rf() * 0.05);
      ctx.fill(poly);
      if (ppu < 0.3) return;
      const c = Math.cos(f.angle), s = Math.sin(f.angle);
      const R = 130;
      if (f.kind === "furrow" || f.kind === "vineyard") {
        const step = f.kind === "furrow" ? 7 : 6;
        const lines = new Path2D();
        const dots = new Path2D();
        for (let k = -R; k <= R; k += step) {
          const x0 = f.cx - c * R - s * k, y0 = f.cy - s * R + c * k;
          const x1 = f.cx + c * R - s * k, y1 = f.cy + s * R + c * k;
          if (f.kind === "furrow" || ppu < 0.6) {
            lines.moveTo(x0, y0);
            lines.lineTo(x1, y1);
          } else {
            for (let t = 0; t <= 1; t += 3 / (2 * R)) dots.rect(x0 + (x1 - x0) * t - 0.6, y0 + (y1 - y0) * t - 0.6, 1.2, 1.2);
          }
        }
        ctx.save();
        ctx.clip(poly);
        ctx.strokeStyle = hexA(ink, f.kind === "furrow" ? 0.15 : 0.25);
        ctx.lineWidth = lw(0.6, 0.4);
        ctx.stroke(lines);
        ctx.fillStyle = hexA(ink, 0.45);
        ctx.fill(dots);
        ctx.restore();
      } else if (f.kind === "pasture") {
        for (let i = 0; i < 50; i++) {
          const x = f.cx + (rf() - 0.5) * 140, y = f.cy + (rf() - 0.5) * 120;
          stipple.rect(x - 0.8, y - 0.8, 1.6, 1.6);
        }
      } else {
        for (let k = -R; k <= R; k += 18)
          for (let t = -R; t <= R; t += 18) {
            const x = f.cx + c * t - s * k, y = f.cy + s * t + c * k;
            stipple.moveTo(x + 2.4, y);
            stipple.arc(x, y, 2.4, 0, Math.PI * 2);
          }
      }
    });
    ctx.fillStyle = hexA(ink, 0.3);
    ctx.fill(stipple);
    ctx.strokeStyle = hexA(pal.hill, 0.55);
    ctx.lineWidth = lw(1.6, 0.6);
    ctx.setLineDash([lw(2.2), lw(3.2)]);
    ctx.lineCap = "round";
    ctx.stroke(hedge);
    ctx.setLineDash([]);
    ctx.lineCap = "butt";
  }

  /* ---------------- marsh ---------------- */
  for (const f of m.marsh.filter(inP)) {
    if (!visPath(f.polygon, 10)) continue;
    const poly = polyPath(f.polygon);
    ctx.fillStyle = hexA(pal.water, 0.16);
    ctx.fill(poly);
    ctx.save();
    ctx.clip(poly);
    const b = bounds(f.polygon);
    const rm = mulberry32(hash(f.name ?? "marsh"));
    ctx.strokeStyle = hexA(pal.water, 0.75);
    ctx.lineWidth = lw(1, 0.5);
    for (let y = b.y0; y < b.y1; y += 9)
      for (let x = b.x0 + (rm() * 12); x < b.x1; x += 18 + rm() * 10) {
        ctx.beginPath();
        ctx.moveTo(x, y);
        ctx.lineTo(x + 8, y);
        ctx.moveTo(x + 2, y - 4);
        ctx.lineTo(x + 4, y);
        ctx.lineTo(x + 6, y - 4);
        ctx.stroke();
      }
    ctx.restore();
  }

  /* ---------------- hills: wash, contours and engraved hachures ---------------- */
  for (const h of m.hills.filter(inP)) {
    const [cx, cy] = h.center;
    const r = h.radius;
    if (!visPt(cx, cy, r * 1.1)) continue;
    const wash = ctx.createRadialGradient(cx - r * 0.15, cy - r * 0.15, 0, cx, cy, r * 1.05);
    wash.addColorStop(0, hexA(pal.hill, 0.3));
    wash.addColorStop(0.75, hexA(pal.hill, 0.16));
    wash.addColorStop(1, hexA(pal.hill, 0));
    ctx.fillStyle = wash;
    ctx.fillRect(cx - r * 1.1, cy - r * 1.1, r * 2.2, r * 2.2);
    const rh = mulberry32(hash((h.id ?? h.name) + "hill"));
    const s1 = rh() * 10, s2 = rh() * 10;
    const wob = (t: number) => 1 + 0.07 * Math.sin(t * 3 + s1) + 0.045 * Math.sin(t * 7 + s2);
    // contours
    ctx.strokeStyle = hexA(ink, 0.22);
    ctx.lineWidth = lw(0.8, 0.5);
    for (const f of [0.35, 0.6, 0.85]) {
      ctx.beginPath();
      for (let a = 0; a <= 96; a++) {
        const t = (a / 96) * Math.PI * 2;
        const x = cx + Math.cos(t) * r * f * wob(t), y = cy + Math.sin(t) * r * f * wob(t) * 0.92;
        a === 0 ? ctx.moveTo(x, y) : ctx.lineTo(x, y);
      }
      ctx.closePath();
      ctx.stroke();
    }
    // hachures, darker on the shaded south-east slopes
    const buckets = [new Path2D(), new Path2D(), new Path2D()];
    const n = Math.round(r * 1.3);
    for (const [ri, ro] of [[0.38, 0.66], [0.64, 1.0]]) {
      for (let i = 0; i < n; i++) {
        const t = (i / n) * Math.PI * 2 + (rh() - 0.5) * 0.02;
        const light = 0.5 + 0.5 * Math.cos(t - Math.PI / 4);
        if (rh() > 0.35 + light * 0.65) continue;
        const len = (ro - ri) * (0.55 + rh() * 0.45);
        const a0 = ri + (ro - ri - len) * rh();
        const w = wob(t);
        const p = buckets[light > 0.7 ? 2 : light > 0.35 ? 1 : 0];
        p.moveTo(cx + Math.cos(t) * r * a0 * w, cy + Math.sin(t) * r * a0 * w * 0.92);
        p.lineTo(cx + Math.cos(t) * r * (a0 + len) * w, cy + Math.sin(t) * r * (a0 + len) * w * 0.92);
      }
    }
    buckets.forEach((p, i) => {
      ctx.strokeStyle = hexA(ink, [0.12, 0.22, 0.36][i]);
      ctx.lineWidth = lw(0.9, 0.45);
      ctx.stroke(p);
    });
  }

  /* ---------------- trees (parks, villas, hedgerows) ---------------- */
  {
    const shadows = new Path2D(), crowns = new Path2D();
    for (const t of fabric.trees) {
      if (!visPt(t.x, t.y, t.r)) continue;
      shadows.moveTo(t.x + t.r * 0.5 + t.r, t.y + t.r * 0.5);
      shadows.arc(t.x + t.r * 0.5, t.y + t.r * 0.5, t.r, 0, Math.PI * 2);
      crowns.moveTo(t.x + t.r, t.y);
      crowns.arc(t.x, t.y, t.r, 0, Math.PI * 2);
    }
    ctx.fillStyle = hexA(ink, 0.18);
    ctx.fill(shadows);
    ctx.fillStyle = hexA(pal.hill, 0.75);
    ctx.fill(crowns);
    ctx.strokeStyle = hexA(ink, 0.6);
    ctx.lineWidth = lw(0.45, 0.45);
    ctx.stroke(crowns);
  }

  /* ---------------- water ---------------- */
  // in passes over every channel (hatching, ink edge, fill, then ripples), so rivers, canals and lagoons
  // drawn as overlapping ribbons merge into one body of water without seams
  const waters = m.water
    .filter(inP)
    .map((w) => ({ w, pts: chaikin(w.path, 3), rw: mulberry32(hash((w.id ?? w.name) + "shore")) }))
    .filter(({ w, pts }) => visPath(pts, w.width));
  for (const { w, pts, rw } of waters) {
    // shore hatching
    ctx.strokeStyle = hexA(ink, 0.28);
    ctx.lineWidth = lw(0.7, 0.45);
    for (const side of [-1, 1]) {
      const bank = offsetPath(pts, (side * w.width) / 2);
      const L = pathLength(bank);
      ctx.beginPath();
      for (let d = 0; d < L; d += 5) {
        const at = pointAlong(bank, d);
        if (!at || !visPt(at.x, at.y, 20)) continue;
        const nx = -Math.sin(at.angle) * side, ny = Math.cos(at.angle) * side;
        const len = 6 + rw() * 9;
        ctx.moveTo(at.x + nx * 2, at.y + ny * 2);
        ctx.lineTo(at.x + nx * (2 + len), at.y + ny * (2 + len));
      }
      ctx.stroke();
    }
  }
  for (const { w, pts } of waters) stroke(ctx, pts, hexA(ink, 0.85), w.width + lw(4), "round");
  for (const { w, pts } of waters) stroke(ctx, pts, hexA(pal.water, 0.92), w.width, "round");
  for (const { w, pts, rw } of waters) {
    // engraved ripples running with the current
    ctx.setLineDash([lw(18), lw(9)]);
    for (let k = -0.4; k <= 0.41; k += 0.1) {
      const off = offsetPath(pts, k * w.width);
      ctx.lineDashOffset = rw() * 30;
      stroke(ctx, off, hexA(k % 0.2 === 0 ? "#ffffff" : ink, 0.18), lw(0.8, 0.5), "butt");
    }
    ctx.setLineDash([]);
    // boats
    const L = pathLength(pts);
    const n = Math.max(3, Math.round(L / 500));
    for (let i = 0; i < n; i++) {
      const at = pointAlong(pts, ((i + 0.3 + rw() * 0.4) / n) * L);
      if (!at || !visPt(at.x, at.y, 30)) continue;
      boat(ctx, at.x + (rw() - 0.5) * w.width * 0.4, at.y, at.angle, 9, ink);
    }
  }
  for (const isl of m.islands.filter(inP)) {
    if (!visPath(isl.polygon, 10)) continue;
    const poly = polyPath(isl.polygon);
    ctx.fillStyle = pal.parchment;
    ctx.fill(poly);
    ctx.strokeStyle = hexA(ink, 0.85);
    ctx.lineWidth = lw(2);
    ctx.stroke(poly);
  }

  /* ---------------- the urban fabric (Nolli-style engraved blocks) ---------------- */
  {
    const vl: Lot[] = [];
    for (const l of fabric.lots) {
      const r = Math.max(l.w, l.d);
      if (visPt(l.x, l.y, r)) vl.push(l);
    }
    const huts = vl.filter((l) => l.kind === "hut");
    const houses = vl.filter((l) => l.kind !== "court" && l.kind !== "hut");
    if (huts.length) {
      const sh = new Path2D(), body = new Path2D();
      for (const l of huts) {
        sh.moveTo(l.x + 2 + l.w / 2, l.y + 2);
        sh.ellipse(l.x + 2, l.y + 2, l.w / 2, l.d / 2, l.a, 0, Math.PI * 2);
        body.moveTo(l.x + l.w / 2, l.y);
        body.ellipse(l.x, l.y, l.w / 2, l.d / 2, l.a, 0, Math.PI * 2);
      }
      ctx.fillStyle = hexA(ink, 0.2);
      ctx.fill(sh);
      ctx.fillStyle = hexA("#b49a62", 0.85);
      ctx.fill(body);
      ctx.strokeStyle = hexA(ink, 0.75);
      ctx.lineWidth = lw(0.4, 0.5);
      ctx.stroke(body);
      if (ppu >= 1.2) {
        // thatch: radial strokes from the ridge
        ctx.strokeStyle = hexA(ink, 0.35);
        ctx.lineWidth = lw(0.2, 0.4);
        ctx.beginPath();
        for (const l of huts)
          for (let k = 0; k < 14; k++) {
            const tt = (k / 14) * Math.PI * 2;
            ctx.moveTo(l.x + Math.cos(tt) * l.w * 0.08, l.y + Math.sin(tt) * l.d * 0.08);
            ctx.lineTo(l.x + Math.cos(tt) * l.w * 0.48, l.y + Math.sin(tt) * l.d * 0.48);
          }
        ctx.stroke();
      }
    }
    const courts = vl.filter((l) => l.kind === "court");
    // cast shadows toward the south-east, longer for taller buildings
    const shadow = new Path2D();
    for (const l of houses) {
      const s = Math.min(9, l.h * 0.22);
      rectPath(shadow, l.x + s * 0.8, l.y + s, l.w, l.d, l.a);
    }
    ctx.fillStyle = hexA(ink, 0.2);
    ctx.fill(shadow);
    const all = new Path2D();
    for (const l of houses) rectPath(all, l.x, l.y, l.w, l.d, l.a);
    if (ppu < 1.1) {
      // overview: tonal masses
      const tones = [new Path2D(), new Path2D(), new Path2D()];
      const towers = new Path2D();
      for (const l of houses) rectPath(l.kind === "tower" ? towers : tones[l.tone < 0.33 ? 0 : l.tone < 0.66 ? 1 : 2], l.x, l.y, l.w, l.d, l.a);
      [0.3, 0.36, 0.42].forEach((a, i) => {
        ctx.fillStyle = hexA(ink, a);
        ctx.fill(tones[i]);
      });
      ctx.fillStyle = hexA(ink, 0.62);
      ctx.fill(towers);
    } else {
      // close up: every tiled roof as four facets lit from the north-west; flat roofs hatched
      const LX = -Math.SQRT1_2, LY = -Math.SQRT1_2;
      const facets = [new Path2D(), new Path2D(), new Path2D(), new Path2D(), new Path2D()];
      const flat = new Path2D();
      const towers = new Path2D();
      const ridges = new Path2D();
      const pick = (nx: number, ny: number) => {
        const lit = (nx * LX + ny * LY + 1) / 2; // 1 = facing the light
        return facets[Math.min(4, Math.floor((1 - lit) * 5))];
      };
      for (const l of houses) {
        if (l.kind === "tower") {
          rectPath(towers, l.x, l.y, l.w, l.d, l.a);
          continue;
        }
        if (l.roof !== "tile") {
          rectPath(flat, l.x, l.y, l.w, l.d, l.a);
          continue;
        }
        const c = Math.cos(l.a), sn = Math.sin(l.a);
        // local axes: u along the longer side
        const long = l.w >= l.d;
        const ux = long ? c : -sn, uy = long ? sn : c;
        const vx = -uy, vy = ux;
        const hl = (long ? l.w : l.d) / 2, hs = (long ? l.d : l.w) / 2;
        const P = (a: number, b: number): [number, number] => [l.x + ux * a + vx * b, l.y + uy * a + vy * b];
        const c0 = P(-hl, -hs), c1 = P(hl, -hs), c2 = P(hl, hs), c3 = P(-hl, hs);
        const r0 = P(-hl + hs, 0), r1 = P(hl - hs, 0);
        const quad = (path: Path2D, pts: [number, number][]) => {
          path.moveTo(pts[0][0], pts[0][1]);
          for (let i = 1; i < pts.length; i++) path.lineTo(pts[i][0], pts[i][1]);
          path.closePath();
        };
        quad(pick(-vx, -vy), [c0, c1, r1, r0]);
        quad(pick(vx, vy), [c3, c2, r1, r0]);
        quad(pick(-ux, -uy), [c0, r0, c3]);
        quad(pick(ux, uy), [c1, r1, c2]);
        ridges.moveTo(r0[0], r0[1]);
        ridges.lineTo(r1[0], r1[1]);
        for (const [a, b] of [[c0, r0], [c3, r0], [c1, r1], [c2, r1]] as [[number, number], [number, number]][]) {
          ridges.moveTo(a[0], a[1]);
          ridges.lineTo(b[0], b[1]);
        }
      }
      [0.14, 0.22, 0.3, 0.4, 0.5].forEach((a, i) => {
        ctx.fillStyle = hexA(ink, a);
        ctx.fill(facets[i]);
      });
      ctx.fillStyle = hexA(ink, 0.3);
      ctx.fill(flat);
      ctx.save();
      ctx.clip(flat);
      ctx.strokeStyle = hexA(ink, 0.3);
      ctx.lineWidth = lw(0.3, 0.5);
      const step = Math.max(1.6, 3 / ppu);
      ctx.beginPath();
      for (let k = view.x0 - (view.y1 - view.y0); k < view.x1; k += step) {
        ctx.moveTo(k, view.y0);
        ctx.lineTo(k + (view.y1 - view.y0), view.y1);
      }
      ctx.stroke();
      ctx.restore();
      ctx.fillStyle = hexA(ink, 0.65);
      ctx.fill(towers);
      ctx.strokeStyle = hexA(ink, 0.45);
      ctx.lineWidth = lw(0.25, 0.4);
      ctx.stroke(ridges);
      if (ppu >= 1.5) {
        ctx.strokeStyle = hexA(pal.parchment, 0.6);
        ctx.beginPath();
        for (const l of houses) {
          if (l.kind !== "tower") continue;
          const k4 = rectCorners(l.x, l.y, l.w * 0.6, l.d * 0.6, l.a);
          ctx.moveTo(k4[0], k4[1]);
          ctx.lineTo(k4[4], k4[5]);
          ctx.moveTo(k4[2], k4[3]);
          ctx.lineTo(k4[6], k4[7]);
        }
        ctx.stroke();
      }
    }
    ctx.strokeStyle = hexA(ink, 0.8);
    ctx.lineWidth = lw(0.35, 0.5);
    ctx.stroke(all);
    const cp = new Path2D();
    for (const l of courts) rectPath(cp, l.x, l.y, l.w, l.d, l.a);
    ctx.fillStyle = PAPER_LIGHT;
    ctx.fill(cp);
    ctx.strokeStyle = hexA(ink, 0.55);
    ctx.lineWidth = lw(0.3, 0.45);
    ctx.stroke(cp);
    if (ppu >= 1.5) {
      ctx.fillStyle = hexA(ink, 0.55);
      for (const l of courts) {
        if (l.w < 6 || l.d < 6) continue;
        ctx.beginPath();
        ctx.arc(l.x, l.y, 0.9, 0, Math.PI * 2);
        ctx.fill();
      }
    }
  }

  /* ---------------- landmark plans ---------------- */
  // biggest first, so a monument standing inside a larger one (a tomb in a mosque court, a temple in a
  // precinct) is drawn on top of it, and every cleared margin is laid before any plan is drawn
  const lms = city.landmarks
    .filter((l) => l.activePeriods.includes(periodId))
    .sort((a, b) => b.footprint[0] * b.footprint[1] * b.scale * b.scale - a.footprint[0] * a.footprint[1] * a.scale * a.scale);
  for (const l of lms) {
    const fw = l.footprint[0] * l.scale, fd = l.footprint[1] * l.scale;
    if (!visPt(l.position[0], l.position[1], Math.max(fw, fd))) continue;
    const model = (l.variants[periodId]?.model ?? l.model) as KitParams | { glb: string };
    if (!("glb" in model) || !planFor(model.glb)) continue;
    const m = 10;
    ctx.save();
    ctx.translate(l.position[0], l.position[1]);
    ctx.rotate((l.rotation * Math.PI) / 180);
    ctx.shadowColor = hexA(pal.parchment, 0.9);
    ctx.shadowBlur = Math.max(2, 14 * ppu);
    ctx.fillStyle = hexA(PAPER_LIGHT, 0.85);
    ctx.fillRect(-fw / 2 - m, -fd / 2 - m, fw + 2 * m, fd + 2 * m);
    ctx.restore();
  }
  for (const l of lms) {
    const fw = l.footprint[0] * l.scale, fd = l.footprint[1] * l.scale;
    if (!visPt(l.position[0], l.position[1], Math.max(fw, fd))) continue;
    const v = l.variants[periodId];
    const model = (v?.model ?? l.model) as KitParams | { glb: string; fallback?: KitParams };
    const kit = "kit" in model ? model : model.fallback;
    const drawn = "glb" in model ? planFor(model.glb) : undefined;
    ctx.save();
    ctx.translate(l.position[0], l.position[1]);
    ctx.rotate((l.rotation * Math.PI) / 180);
    if (drawn) {
      // a cleared margin of pale paper, then the model's own plan with a cast shadow
      const m = 10;
      ctx.save();
      ctx.scale(l.scale, l.scale);
      ctx.shadowColor = hexA(ink, 0.35);
      ctx.shadowBlur = Math.max(2, 5 * ppu);
      ctx.shadowOffsetX = Math.max(1.5, 4 * ppu);
      ctx.shadowOffsetY = Math.max(1.5, 5 * ppu);
      ctx.globalCompositeOperation = "multiply";
      ctx.drawImage(drawn.img, drawn.cx - drawn.size / 2, drawn.cy - drawn.size / 2, drawn.size, drawn.size);
      ctx.restore();
      // an inked double border so the monument reads at a glance
      ctx.strokeStyle = hexA(ink, 0.75);
      ctx.lineWidth = lw(1.4);
      ctx.strokeRect(-fw / 2 - m * 0.6, -fd / 2 - m * 0.6, fw + m * 1.2, fd + m * 1.2);
      ctx.lineWidth = lw(0.5);
      ctx.strokeRect(-fw / 2 - m, -fd / 2 - m, fw + 2 * m, fd + 2 * m);
    } else {
      plan(ctx, kit, l.category, fw, fd, ink, pal.parchment, lw);
    }
    ctx.restore();
  }

  /* ---------------- roads: edges first, then fills, so crossings merge ---------------- */
  const roads = m.roads.filter(inP).filter((r) => visPath(r.path, r.width));
  for (const r of roads) stroke(ctx, r.path, hexA(ink, r.style === "major" ? 0.85 : 0.65), r.width + lw(r.style === "major" ? 2.6 : 1.8), "round");
  for (const r of roads) stroke(ctx, r.path, PAPER_LIGHT, r.width, "round");
  if (ppu >= 1.6) {
    ctx.setLineDash([lw(1.5), lw(5)]);
    for (const r of roads.filter((x) => x.style === "major")) stroke(ctx, r.path, hexA(ink, 0.25), lw(0.6), "round");
    ctx.setLineDash([]);
  }

  /* ---------------- bridges, aqueducts, walls, gates ---------------- */
  for (const b of m.bridges.filter(inP)) {
    if (!visPath(b.path, 20)) continue;
    stroke(ctx, b.path, hexA(ink, 0.95), lw(11), "butt");
    stroke(ctx, b.path, PAPER_LIGHT, lw(7), "butt");
    const L = pathLength(b.path);
    ctx.strokeStyle = hexA(ink, 0.85);
    ctx.lineWidth = lw(0.8);
    for (let d = 6; d < L - 3; d += 12) {
      const at = pointAlong(b.path, d)!;
      ctx.save();
      ctx.translate(at.x, at.y);
      ctx.rotate(at.angle);
      ctx.beginPath();
      ctx.arc(0, 7, 4, Math.PI, 0);
      ctx.stroke();
      ctx.restore();
    }
  }
  for (const a of m.aqueducts.filter(inP)) {
    if (!visPath(a.path, 20)) continue;
    // a fine double line (the channel on its arcade) with small arch marks on one side
    for (const off of [-1.8, 1.8]) stroke(ctx, offsetPath(a.path, off), hexA(ink, 0.55), lw(0.7, 0.5), "butt");
    if (ppu >= 0.5) {
      const L = pathLength(a.path);
      ctx.strokeStyle = hexA(ink, 0.4);
      ctx.lineWidth = lw(0.5, 0.4);
      ctx.beginPath();
      for (let d = 4; d < L; d += 8) {
        const at = pointAlong(a.path, d)!;
        const nx = -Math.sin(at.angle), ny = Math.cos(at.angle);
        const cx = at.x + nx * 2.6, cy = at.y + ny * 2.6;
        ctx.moveTo(cx + Math.cos(at.angle) * 3, cy + Math.sin(at.angle) * 3);
        ctx.arc(cx, cy, 3, at.angle, at.angle + Math.PI, false);
      }
      ctx.stroke();
    }
  }
  for (const wl of m.walls.filter(inP)) {
    const pts = wl.closed ? [...wl.path, wl.path[0]] : wl.path;
    if (!visPath(pts, 30)) continue;
    // a solid inked curtain with square towers projecting to one side, as on old city plans
    stroke(ctx, pts, hexA(ink, 0.82), lw(4.2), "round");
    stroke(ctx, pts, hexA(pal.parchment, 0.55), lw(1.2), "round");
    const L = pathLength(pts);
    ctx.fillStyle = hexA(ink, 0.82);
    for (let d = 15; d < L; d += 30) {
      const at = pointAlong(pts, d)!;
      if (!visPt(at.x, at.y, 10)) continue;
      ctx.save();
      ctx.translate(at.x, at.y);
      ctx.rotate(at.angle);
      ctx.fillRect(-3, -1, 6, 6.5);
      ctx.restore();
    }
  }
  for (const g of m.gates.filter(inP)) {
    const [x, y] = g.position;
    if (!visPt(x, y, 60)) continue;
    ctx.fillStyle = PAPER_LIGHT;
    ctx.strokeStyle = hexA(ink, 0.95);
    ctx.lineWidth = lw(2);
    ctx.fillRect(x - 13, y - 13, 26, 26);
    ctx.strokeRect(x - 13, y - 13, 26, 26);
    ctx.beginPath();
    ctx.arc(x, y + 6, 6, Math.PI, 0);
    ctx.stroke();
  }

  /* ---------------- districts ---------------- */
  ctx.setLineDash([lw(14), lw(6), lw(3), lw(6)]);
  for (const d of m.districts.filter(inP)) {
    if (!visPath(d.polygon, 20)) continue;
    ctx.strokeStyle = hexA(ink, 0.5);
    ctx.lineWidth = lw(1.8);
    ctx.stroke(polyPath(d.polygon));
  }
  ctx.setLineDash([]);

  /* ---------------- vignette ---------------- */
  {
    const g = ctx.createRadialGradient(MW / 2, MH / 2, Math.min(MW, MH) * 0.32, MW / 2, MH / 2, Math.hypot(MW, MH) * 0.55);
    g.addColorStop(0, hexA(ink, 0));
    g.addColorStop(1, hexA(ink, 0.32));
    ctx.fillStyle = g;
    ctx.fillRect(Math.max(0, view.x0), Math.max(0, view.y0), Math.min(MW, view.x1) - Math.max(0, view.x0), Math.min(MH, view.y1) - Math.max(0, view.y0));
  }

  /* ---------------- lettering ---------------- */
  const label = (s: string, x: number, y: number, size: number, opts: { italic?: boolean; rot?: number; alpha?: number; tracking?: number } = {}) => {
    if (!visPt(x, y, size * s.length * 0.8)) return;
    text(ctx, s, x, y, size, ink, pal.parchment, opts);
  };
  for (const d of m.districts.filter(inP)) {
    const [x, y] = centroid(d.polygon);
    label(d.name.toUpperCase(), x, y, 44, { alpha: 0.6, tracking: 0.45 });
  }
  for (const l of m.labels.filter(inP)) label(l.size === "lg" ? l.text.toUpperCase() : l.text, l.position[0], l.position[1], l.size === "lg" ? 70 : l.size === "md" ? 42 : 28, { rot: (l.rotation * Math.PI) / 180, italic: l.size !== "lg", alpha: 0.75, tracking: l.size === "lg" ? 0.5 : 0.2 });
  for (const h of m.hills.filter(inP)) if (h.label) label(h.name, h.center[0], h.center[1] - h.radius * 0.1, Math.min(48, 18 + h.radius * 0.08), { italic: true, alpha: 0.7, tracking: 0.25 });
  for (const w of m.water.filter(inP)) textAlongPath(ctx, w.name.toUpperCase(), chaikin(w.path, 3), 34, "#f5ecd6", null, 0.35, 0.85, vis);
  for (const r of m.roads.filter(inP)) if (r.labelled) textAlongPath(ctx, r.name.toUpperCase(), r.path, r.style === "major" ? 13 : 10, ink, null, 0.2, 0.8, vis, r.width / 2 + 9);
  for (const g of m.gates.filter(inP)) label(g.name, g.position[0], g.position[1] + 34, 16, { italic: true, alpha: 0.85, tracking: 0.12 });

  /* ---------------- frame, cartouche, compass, scale ---------------- */
  frame(ctx, MW, MH, ink, lw, vis);
  if (m.compass && visPt(m.compass[0], m.compass[1], 300)) compass(ctx, m.compass[0], m.compass[1], 150, ink, pal.parchment);
  {
    // the box grows to fit long names and subtitles, and stays inside the frame
    ctx.font = `92px "IM Fell English", "Cormorant Garamond", Georgia, serif`;
    const nameW = ctx.measureText(city.name.toUpperCase()).width + 92 * 0.18 * city.name.length;
    ctx.font = `italic 34px "IM Fell English", "Cormorant Garamond", Georgia, serif`;
    const subW = ctx.measureText(`${period.label} · ${period.year}`).width + 34 * 0.12 * (period.label.length + 8);
    const bw = Math.max(900, nameW + 180, subW + 180), bh = 300;
    let [cx, cy] = m.cartouche ?? [MW * 0.03, MH * 0.97];
    cx = Math.max(MW * 0.02 + 40, Math.min(cx, MW * 0.98 - bw - 40));
    cy = Math.max(bh + MH * 0.02 + 40, Math.min(cy, MH * 0.98 - 120));
    if (vis(cx, cy - bh, cx + bw, cy + 120)) cartouche(ctx, cx, cy - bh, bw, bh, city.name, period, ink, pal.parchment);
  }

  ctx.setTransform(1, 0, 0, 1, 0, 0);
}

/* ======================================================================= helpers */

function plan(ctx: Ctx2D, kit: KitParams | undefined, category: string, fw: number, fd: number, ink: string, paper: string, lw: (u: number, m?: number) => number) {
  const hw = fw / 2, hd = fd / 2;
  ctx.lineWidth = lw(1.1);
  ctx.strokeStyle = hexA(ink, 0.9);
  const k = kit?.kit;
  if (k === "amphitheater") {
    const arc = kit && "arc" in kit ? ((kit.arc ?? 360) * Math.PI) / 180 : Math.PI * 2;
    const full = arc >= Math.PI * 2 - 0.01;
    const start = full ? 0 : Math.PI;
    ctx.fillStyle = hexA(ink, 0.32);
    ctx.beginPath();
    ctx.ellipse(0, 0, hw, full ? hd : hw, 0, start, start + arc);
    if (!full) ctx.closePath();
    ctx.fill();
    ctx.stroke();
    ctx.fillStyle = "#d8c08e";
    ctx.beginPath();
    ctx.ellipse(0, 0, hw * 0.42, (full ? hd : hw) * 0.42, 0, start, start + arc);
    if (!full) ctx.closePath();
    ctx.fill();
    ctx.stroke();
    ctx.strokeStyle = hexA(paper, 0.7);
    ctx.lineWidth = lw(0.5);
    for (const f of [0.6, 0.78, 0.92]) {
      ctx.beginPath();
      ctx.ellipse(0, 0, hw * f, (full ? hd : hw) * f, 0, start, start + arc);
      ctx.stroke();
    }
    ctx.beginPath();
    for (let t = start; t <= start + arc; t += 0.12) {
      ctx.moveTo(Math.cos(t) * hw * 0.44, Math.sin(t) * (full ? hd : hw) * 0.44);
      ctx.lineTo(Math.cos(t) * hw, Math.sin(t) * (full ? hd : hw));
    }
    ctx.stroke();
    if (!full) {
      ctx.fillStyle = hexA(ink, 0.5);
      ctx.fillRect(-hw, -hw * 0.18, fw, hw * 0.16);
    }
    return;
  }
  if (k === "circus" || fw / fd > 2.4) {
    const r = hd;
    const p = new Path2D();
    p.moveTo(-hw, -hd);
    p.lineTo(hw - r, -hd);
    p.arc(hw - r, 0, r, -Math.PI / 2, Math.PI / 2);
    p.lineTo(-hw, hd);
    p.closePath();
    ctx.fillStyle = hexA(ink, 0.3);
    ctx.fill(p);
    ctx.stroke(p);
    ctx.save();
    ctx.scale(0.86, 0.72);
    ctx.fillStyle = "#d8c08e";
    ctx.fill(p);
    ctx.stroke(p);
    ctx.restore();
    ctx.lineWidth = lw(2.4);
    ctx.beginPath();
    ctx.moveTo(-hw * 0.5, 0);
    ctx.lineTo(hw * 0.55, 0);
    ctx.stroke();
    return;
  }
  // rectangular buildings
  ctx.fillStyle = hexA(ink, category === "temple" || category === "religious" ? 0.42 : 0.34);
  ctx.fillRect(-hw, -hd, fw, fd);
  ctx.strokeRect(-hw, -hd, fw, fd);
  if (category === "temple") {
    ctx.fillStyle = hexA(ink, 0.75);
    ctx.fillRect(-hw * 0.6, -hd * 0.45, fw * 0.6, fd * 0.85);
    ctx.fillStyle = hexA(paper, 0.95);
    const n = Math.max(4, Math.round(fw / 4));
    for (let i = 0; i < n; i++) {
      const x = -hw * 0.85 + (fw * 0.85 * i) / (n - 1);
      ctx.beginPath();
      ctx.arc(x, -hd * 0.85, Math.min(1.4, fw * 0.03), 0, Math.PI * 2);
      ctx.fill();
    }
  } else if (category === "religious") {
    ctx.fillStyle = hexA(ink, 0.7);
    ctx.fillRect(-hw * 0.25, -hd * 0.95, fw * 0.5, fd * 1.9);
    ctx.beginPath();
    ctx.arc(0, hd * 0.95, fw * 0.25, 0, Math.PI);
    ctx.fill();
  } else {
    ctx.strokeStyle = hexA(paper, 0.7);
    ctx.lineWidth = lw(0.6);
    ctx.strokeRect(-hw * 0.7, -hd * 0.7, fw * 0.7, fd * 0.7);
  }
}

function frame(ctx: Ctx2D, W: number, H: number, ink: string, lw: (u: number, m?: number) => number, vis: (a: number, b: number, c: number, d: number) => boolean) {
  const o = 18, band = 26;
  if (!(vis(0, 0, W, o + band + 10) || vis(0, H - o - band - 10, W, H) || vis(0, 0, o + band + 10, H) || vis(W - o - band - 10, 0, W, H))) return;
  ctx.strokeStyle = hexA(ink, 0.9);
  ctx.lineWidth = lw(5);
  ctx.strokeRect(o, o, W - 2 * o, H - 2 * o);
  ctx.lineWidth = lw(1.5);
  ctx.strokeRect(o + band, o + band, W - 2 * (o + band), H - 2 * (o + band));
  // graduated bar
  ctx.fillStyle = hexA(ink, 0.85);
  const seg = 100;
  for (let x = o; x < W - o; x += seg * 2) {
    ctx.fillRect(x, o + band * 0.35, Math.min(seg, W - o - x), band * 0.3);
    ctx.fillRect(x, H - o - band * 0.65, Math.min(seg, W - o - x), band * 0.3);
  }
  for (let y = o; y < H - o; y += seg * 2) {
    ctx.fillRect(o + band * 0.35, y, band * 0.3, Math.min(seg, H - o - y));
    ctx.fillRect(W - o - band * 0.65, y, band * 0.3, Math.min(seg, H - o - y));
  }
  for (const [x, y] of [[o + band / 2, o + band / 2], [W - o - band / 2, o + band / 2], [o + band / 2, H - o - band / 2], [W - o - band / 2, H - o - band / 2]]) {
    ctx.beginPath();
    ctx.moveTo(x, y - 20);
    ctx.lineTo(x + 20, y);
    ctx.lineTo(x, y + 20);
    ctx.lineTo(x - 20, y);
    ctx.closePath();
    ctx.fill();
  }
}

function compass(ctx: Ctx2D, cx: number, cy: number, r: number, ink: string, paper: string) {
  ctx.save();
  ctx.translate(cx, cy);
  ctx.strokeStyle = hexA(ink, 0.85);
  ctx.lineWidth = 2;
  for (const f of [1, 0.92, 0.45]) {
    ctx.beginPath();
    ctx.arc(0, 0, r * f, 0, Math.PI * 2);
    ctx.stroke();
  }
  for (let i = 0; i < 64; i++) {
    const a = (i / 64) * Math.PI * 2;
    ctx.beginPath();
    ctx.moveTo(Math.cos(a) * r * 0.92, Math.sin(a) * r * 0.92);
    ctx.lineTo(Math.cos(a) * r * (i % 4 === 0 ? 0.82 : 0.87), Math.sin(a) * r * (i % 4 === 0 ? 0.82 : 0.87));
    ctx.stroke();
  }
  for (let i = 0; i < 16; i++) {
    const a = (i / 16) * Math.PI * 2 - Math.PI / 2;
    const len = i % 4 === 0 ? r * 1.05 : i % 2 === 0 ? r * 0.7 : r * 0.45;
    const wdt = i % 4 === 0 ? 0.16 : 0.12;
    for (const side of [-1, 1]) {
      ctx.beginPath();
      ctx.moveTo(0, 0);
      ctx.lineTo(Math.cos(a) * len, Math.sin(a) * len);
      ctx.lineTo(Math.cos(a + side * wdt * 2) * r * 0.16, Math.sin(a + side * wdt * 2) * r * 0.16);
      ctx.closePath();
      ctx.fillStyle = side < 0 ? hexA(ink, 0.85) : hexA(paper, 0.95);
      ctx.fill();
      ctx.stroke();
    }
  }
  ctx.font = `${Math.round(r * 0.32)}px "IM Fell English", Georgia, serif`;
  ctx.fillStyle = hexA(ink, 0.95);
  ctx.textAlign = "center";
  ctx.textBaseline = "middle";
  ctx.fillText("N", 0, -r * 1.25);
  ctx.fillText("S", 0, r * 1.25);
  ctx.fillText("E", r * 1.25, 0);
  ctx.fillText("O", -r * 1.25, 0);
  ctx.restore();
}

function cartouche(ctx: Ctx2D, x: number, y: number, w: number, h: number, name: string, period: { label: string; year: number }, ink: string, paper: string) {
  ctx.fillStyle = hexA(paper, 0.92);
  ctx.fillRect(x, y, w, h);
  ctx.strokeStyle = hexA(ink, 0.9);
  ctx.lineWidth = 6;
  ctx.strokeRect(x, y, w, h);
  ctx.lineWidth = 2;
  ctx.strokeRect(x + 14, y + 14, w - 28, h - 28);
  // scrolls on the sides
  for (const sx of [x, x + w]) {
    ctx.beginPath();
    ctx.arc(sx, y + h / 2, 40, 0, Math.PI * 2);
    ctx.fillStyle = hexA(paper, 0.95);
    ctx.fill();
    ctx.stroke();
    ctx.beginPath();
    ctx.arc(sx, y + h / 2, 22, 0, Math.PI * 1.6);
    ctx.stroke();
  }
  text(ctx, "ICHNOGRAPHIA · CHRONOSCAPE", x + w / 2, y + h * 0.2, 26, ink, paper, { alpha: 0.85, tracking: 0.35 });
  text(ctx, name.toUpperCase(), x + w / 2, y + h * 0.5, 92, ink, paper, { alpha: 0.95, tracking: 0.18 });
  const yr = period.year < 0 ? `${-period.year} BCE` : `${period.year} CE`;
  text(ctx, `${period.label} · ${yr}`, x + w / 2, y + h * 0.78, 34, ink, paper, { italic: true, alpha: 0.9, tracking: 0.12 });
  // scale bar
  const sy = y + h + 70;
  const seg = 100;
  for (let i = 0; i < 5; i++) {
    ctx.fillStyle = i % 2 === 0 ? hexA(ink, 0.9) : hexA(paper, 0.95);
    ctx.fillRect(x + i * seg, sy, seg, 14);
  }
  ctx.strokeStyle = hexA(ink, 0.9);
  ctx.lineWidth = 2;
  ctx.strokeRect(x, sy, 5 * seg, 14);
  for (let i = 0; i <= 5; i++) text(ctx, `${i * 100}`, x + i * seg, sy + 40, 22, ink, paper, { alpha: 0.85, tracking: 0 });
  text(ctx, "METRES", x + 5 * seg + 80, sy + 8, 22, ink, paper, { alpha: 0.85, tracking: 0.3 });
}

function text(ctx: Ctx2D, s: string, x: number, y: number, size: number, ink: string, halo: string, o: { italic?: boolean; rot?: number; alpha?: number; tracking?: number } = {}) {
  ctx.save();
  ctx.translate(x, y);
  ctx.rotate(o.rot ?? 0);
  ctx.font = `${o.italic ? "italic " : ""}${size}px "IM Fell English", "Cormorant Garamond", Georgia, serif`;
  ctx.textBaseline = "middle";
  ctx.textAlign = "left";
  const tracking = (o.tracking ?? 0.2) * size;
  const chars = [...s];
  const widths = chars.map((c) => ctx.measureText(c).width);
  const total = widths.reduce((a, b) => a + b, 0) + tracking * (chars.length - 1);
  let cx = -total / 2;
  ctx.lineJoin = "round";
  ctx.strokeStyle = hexA(halo, 0.75);
  ctx.lineWidth = size * 0.18;
  chars.forEach((c, i) => {
    ctx.strokeText(c, cx, 0);
    cx += widths[i] + tracking;
  });
  cx = -total / 2;
  ctx.fillStyle = hexA(ink, o.alpha ?? 0.85);
  chars.forEach((c, i) => {
    ctx.fillText(c, cx, 0);
    cx += widths[i] + tracking;
  });
  ctx.restore();
}

function textAlongPath(ctx: Ctx2D, s: string, path: Vec2[], size: number, ink: string, halo: string | null, tracking: number, alpha: number, vis: (a: number, b: number, c: number, d: number) => boolean, offset = 0) {
  let pts = path;
  if (pts[pts.length - 1][0] < pts[0][0]) pts = [...pts].reverse();
  if (offset) pts = offsetPath(pts, -offset);
  const L = pathLength(pts);
  ctx.save();
  ctx.font = `${size}px "IM Fell English", "Cormorant Garamond", Georgia, serif`;
  const chars = [...s];
  const widths = chars.map((c) => ctx.measureText(c).width);
  const total = widths.reduce((a, b) => a + b, 0) + tracking * size * (chars.length - 1);
  if (total > L * 0.9) {
    ctx.restore();
    return;
  }
  // repeat the name along long paths
  const reps = Math.max(1, Math.floor(L / (total * 4)));
  ctx.textBaseline = "middle";
  ctx.textAlign = "center";
  for (let r = 0; r < reps; r++) {
    let d = (L * (r + 0.5)) / reps - total / 2;
    for (let i = 0; i < chars.length; i++) {
      const at = pointAlong(pts, d + widths[i] / 2);
      d += widths[i] + tracking * size;
      if (!at || !vis(at.x - size, at.y - size, at.x + size, at.y + size)) continue;
      ctx.save();
      ctx.translate(at.x, at.y);
      ctx.rotate(at.angle);
      if (halo) {
        ctx.strokeStyle = hexA(halo, 0.7);
        ctx.lineWidth = size * 0.2;
        ctx.strokeText(chars[i], 0, 0);
      }
      ctx.fillStyle = hexA(ink, alpha);
      ctx.fillText(chars[i], 0, 0);
      ctx.restore();
    }
  }
  ctx.restore();
}

function boat(ctx: Ctx2D, x: number, y: number, angle: number, size: number, ink: string) {
  ctx.save();
  ctx.translate(x, y);
  ctx.rotate(angle);
  ctx.strokeStyle = hexA(ink, 0.85);
  ctx.fillStyle = hexA(ink, 0.3);
  ctx.lineWidth = size * 0.12;
  ctx.beginPath();
  ctx.moveTo(-size, -size * 0.25);
  ctx.quadraticCurveTo(0, size * 0.6, size, -size * 0.25);
  ctx.lineTo(size * 0.8, -size * 0.35);
  ctx.lineTo(-size * 0.8, -size * 0.35);
  ctx.closePath();
  ctx.fill();
  ctx.stroke();
  ctx.beginPath();
  ctx.moveTo(0, -size * 0.35);
  ctx.lineTo(0, -size * 1.4);
  ctx.stroke();
  ctx.beginPath();
  ctx.moveTo(0, -size * 1.3);
  ctx.lineTo(size * 0.6, -size * 0.55);
  ctx.lineTo(0, -size * 0.55);
  ctx.closePath();
  ctx.fill();
  ctx.stroke();
  ctx.restore();
}

function stroke(ctx: Ctx2D, pts: Vec2[], style: string, width: number, cap: CanvasLineCap) {
  ctx.beginPath();
  pts.forEach(([x, y], i) => (i === 0 ? ctx.moveTo(x, y) : ctx.lineTo(x, y)));
  ctx.strokeStyle = style;
  ctx.lineWidth = width;
  ctx.lineCap = cap;
  ctx.lineJoin = "round";
  ctx.stroke();
}

function rectPath(p: Path2D, x: number, y: number, w: number, d: number, a: number) {
  const c = rectCorners(x, y, w, d, a);
  p.moveTo(c[0], c[1]);
  p.lineTo(c[2], c[3]);
  p.lineTo(c[4], c[5]);
  p.lineTo(c[6], c[7]);
  p.closePath();
}

function polyPath(pts: Vec2[]): Path2D {
  const p = new Path2D();
  pts.forEach(([x, y], i) => (i === 0 ? p.moveTo(x, y) : p.lineTo(x, y)));
  p.closePath();
  return p;
}

function bounds(pts: Vec2[]) {
  let x0 = Infinity, y0 = Infinity, x1 = -Infinity, y1 = -Infinity;
  for (const [x, y] of pts) {
    x0 = Math.min(x0, x);
    y0 = Math.min(y0, y);
    x1 = Math.max(x1, x);
    y1 = Math.max(y1, y);
  }
  return { x0, y0, x1, y1 };
}

let paperCanvas: AnyCanvas | null = null;
/** A seamless 512px paper texture: soft mottling, fibres and fine grain (applied with multiply). */
function paperTile(): AnyCanvas {
  if (paperCanvas) return paperCanvas;
  const S = 512;
  const c = makeCanvas(S, S);
  const ctx = ctx2d(c);
  ctx.fillStyle = "#ffffff";
  ctx.fillRect(0, 0, S, S);
  const rnd = mulberry32(42);
  // soft mottling: periodic value noise (wraps seamlessly at the tile edge)
  const img0 = ctx.getImageData(0, 0, S, S);
  const octaves: [number, number][] = [[4, 0.035], [16, 0.03], [64, 0.022]];
  const lattices = octaves.map(([n]) => Array.from({ length: n * n }, () => rnd()));
  const smooth = (t: number) => t * t * (3 - 2 * t);
  for (let y = 0; y < S; y++)
    for (let x = 0; x < S; x++) {
      let v = 0;
      octaves.forEach(([n, a], o) => {
        const fx = (x / S) * n, fy = (y / S) * n;
        const x0 = Math.floor(fx), y0 = Math.floor(fy);
        const tx = smooth(fx - x0), ty = smooth(fy - y0);
        const L = lattices[o];
        const g = (i: number, j: number) => L[((j % n) + n) % n * n + (((i % n) + n) % n)];
        const top = g(x0, y0) * (1 - tx) + g(x0 + 1, y0) * tx;
        const bot = g(x0, y0 + 1) * (1 - tx) + g(x0 + 1, y0 + 1) * tx;
        v += (top * (1 - ty) + bot * ty - 0.5) * a * 2;
      });
      const i = (y * S + x) * 4;
      const k = 1 - Math.max(0, v + 0.04);
      img0.data[i] = 255 * k;
      img0.data[i + 1] = 255 * k * 0.995;
      img0.data[i + 2] = 255 * k * 0.98;
      img0.data[i + 3] = 255;
    }
  ctx.putImageData(img0, 0, 0);
  // fibres
  ctx.strokeStyle = "rgba(120,95,60,0.07)";
  ctx.lineWidth = 0.7;
  for (let i = 0; i < 420; i++) {
    const x = rnd() * S, y = rnd() * S, a = rnd() * Math.PI, l = 4 + rnd() * 14;
    ctx.beginPath();
    ctx.moveTo(x, y);
    ctx.quadraticCurveTo(x + Math.cos(a) * l * 0.5 + (rnd() - 0.5) * 3, y + Math.sin(a) * l * 0.5 + (rnd() - 0.5) * 3, x + Math.cos(a) * l, y + Math.sin(a) * l);
    ctx.stroke();
  }
  // fine grain
  const img = ctx.getImageData(0, 0, S, S);
  for (let i = 0; i < img.data.length; i += 4) {
    const g = (rnd() - 0.5) * 14;
    img.data[i] += g;
    img.data[i + 1] += g;
    img.data[i + 2] += g;
  }
  ctx.putImageData(img, 0, 0);
  paperCanvas = c;
  return c;
}

export function hexA(hex: string, a: number): string {
  const r = parseInt(hex.slice(1, 3), 16), g = parseInt(hex.slice(3, 5), 16), b = parseInt(hex.slice(5, 7), 16);
  return `rgba(${r},${g},${b},${a})`;
}

/** Fade the outer 9% of a tile to transparent so it blends into the base plate. */
export function featherEdges(canvas: AnyCanvas) {
  const ctx = ctx2d(canvas);
  const W = canvas.width, H = canvas.height, b = Math.round(W * 0.09);
  ctx.save();
  ctx.setTransform(1, 0, 0, 1, 0, 0);
  ctx.globalCompositeOperation = "destination-out";
  const band = (x0: number, y0: number, x1: number, y1: number, rx: number, ry: number, rw: number, rh: number) => {
    const g = ctx.createLinearGradient(x0, y0, x1, y1);
    g.addColorStop(0, "rgba(0,0,0,1)");
    g.addColorStop(1, "rgba(0,0,0,0)");
    ctx.fillStyle = g;
    ctx.fillRect(rx, ry, rw, rh);
  };
  band(0, 0, b, 0, 0, 0, b, H);
  band(W, 0, W - b, 0, W - b, 0, b, H);
  band(0, 0, 0, b, 0, 0, W, b);
  band(0, H, 0, H - b, 0, H - b, W, b);
  ctx.restore();
}
