import type { City, Vec2 } from "@/content/schema";

/**
 * Draws the illustrated atlas plate for a city *in a given period* from its
 * vector description. Everything is city-agnostic: it only reads city.map and
 * the period-filtered landmark footprints.
 */
export function drawParchment(city: City, periodId: string, maxEdge = city.map.resolution): HTMLCanvasElement {
  const [mw, mh] = city.map.size;
  const k = maxEdge / Math.max(mw, mh);
  const W = Math.round(mw * k);
  const H = Math.round(mh * k);
  const canvas = document.createElement("canvas");
  canvas.width = W;
  canvas.height = H;
  const ctx = canvas.getContext("2d")!;
  const pal = city.map.palette;
  const P = (p: Vec2): [number, number] => [p[0] * k, p[1] * k];
  const rnd = mulberry32(hash(city.id + periodId));
  const lw = (units: number) => Math.max(0.8, units * k); // line width in px from map units
  const inPeriod = <T extends { periods?: string[] }>(f: T) => !f.periods || f.periods.includes(periodId);
  const period = city.periods.find((p) => p.id === periodId);
  const m = city.map;

  /* ---------- paper ---------- */
  ctx.fillStyle = pal.parchment;
  ctx.fillRect(0, 0, W, H);
  paintNoise(ctx, W, H, rnd, 0.1);
  grain(ctx, W, H, rnd);
  for (let i = 0; i < 14; i++) {
    const x = rnd() * W,
      y = rnd() * H,
      r = (0.06 + rnd() * 0.18) * Math.min(W, H);
    const g = ctx.createRadialGradient(x, y, 0, x, y, r);
    g.addColorStop(0, hexA(pal.ink, 0.05 + rnd() * 0.05));
    g.addColorStop(1, hexA(pal.ink, 0));
    ctx.fillStyle = g;
    ctx.fillRect(x - r, y - r, 2 * r, 2 * r);
  }
  const vg = ctx.createRadialGradient(W / 2, H / 2, Math.min(W, H) * 0.3, W / 2, H / 2, Math.max(W, H) * 0.72);
  vg.addColorStop(0, hexA(pal.ink, 0));
  vg.addColorStop(1, hexA(pal.ink, 0.4));
  ctx.fillStyle = vg;
  ctx.fillRect(0, 0, W, H);

  /* ---------- marsh, gardens, built-up blocks ---------- */
  const marshPat = pattern(64, (c) => {
    c.strokeStyle = hexA(pal.water, 0.7);
    c.lineWidth = 1.2;
    for (let i = 0; i < 4; i++) {
      const y = 8 + i * 15 + (i % 2) * 4;
      const x = (i % 2) * 20;
      c.beginPath();
      c.moveTo(x, y);
      c.lineTo(x + 20, y);
      c.stroke();
      c.beginPath();
      c.moveTo(x + 6, y - 5);
      c.lineTo(x + 10, y);
      c.lineTo(x + 14, y - 5);
      c.stroke();
    }
  });
  for (const f of m.marsh.filter(inPeriod)) {
    polygon(ctx, f.polygon.map(P));
    ctx.fillStyle = hexA(pal.water, 0.12);
    ctx.fill();
    ctx.fillStyle = marshPat;
    ctx.fill();
  }
  const treePat = pattern(56, (c) => {
    c.fillStyle = hexA(pal.hill, 0.75);
    c.strokeStyle = hexA(pal.ink, 0.55);
    c.lineWidth = 1;
    const pts = [[12, 14], [38, 10], [26, 34], [48, 42], [8, 44]];
    for (const [x, y] of pts) {
      c.beginPath();
      c.arc(x, y, 4.2, 0, Math.PI * 2);
      c.fill();
      c.stroke();
      c.beginPath();
      c.moveTo(x, y + 4);
      c.lineTo(x, y + 8);
      c.stroke();
    }
  });
  for (const f of m.gardens.filter(inPeriod)) {
    polygon(ctx, f.polygon.map(P));
    ctx.fillStyle = hexA(pal.hill, 0.12);
    ctx.fill();
    ctx.fillStyle = treePat;
    ctx.fill();
  }
  const blockPat = (dense: boolean) =>
    pattern(48, (c) => {
      c.fillStyle = hexA(pal.ink, dense ? 0.22 : 0.14);
      c.strokeStyle = hexA(pal.ink, 0.5);
      c.lineWidth = 0.8;
      const n = dense ? 7 : 4;
      for (let i = 0; i < n; i++) {
        const x = (i * 17 + (i % 3) * 5) % 40;
        const y = (i * 11 + (i % 2) * 9) % 40;
        const w = 5 + (i % 3) * 2,
          h = 4 + (i % 2) * 3;
        c.fillRect(x, y, w, h);
        c.strokeRect(x + 0.5, y + 0.5, w, h);
      }
    });
  const densePat = blockPat(true),
    loosePat = blockPat(false);
  for (const f of m.blocks.filter(inPeriod)) {
    polygon(ctx, f.polygon.map(P));
    ctx.fillStyle = hexA(pal.ink, f.density === "dense" ? 0.07 : 0.04);
    ctx.fill();
    ctx.fillStyle = f.density === "dense" ? densePat : loosePat;
    ctx.fill();
  }

  /* ---------- hills: contour rings + hachures ---------- */
  for (const h of m.hills.filter(inPeriod)) {
    const [cx, cy] = P(h.center);
    const r = h.radius * k;
    const fill = ctx.createRadialGradient(cx, cy, 0, cx, cy, r);
    fill.addColorStop(0, hexA(pal.hill, 0.42));
    fill.addColorStop(1, hexA(pal.hill, 0));
    ctx.fillStyle = fill;
    ctx.fillRect(cx - r, cy - r, 2 * r, 2 * r);
    const rings = r > 200 * k ? 6 : 4;
    for (let i = 1; i <= rings; i++) {
      const rr = (r * i) / rings;
      ctx.beginPath();
      const seed = rnd() * 100;
      for (let a = 0; a <= 72; a++) {
        const t = (a / 72) * Math.PI * 2;
        const wob = 1 + 0.06 * Math.sin(t * 3 + seed) + 0.04 * Math.sin(t * 7 + seed * 2);
        const x = cx + Math.cos(t) * rr * wob;
        const y = cy + Math.sin(t) * rr * wob * 0.9;
        a === 0 ? ctx.moveTo(x, y) : ctx.lineTo(x, y);
      }
      ctx.closePath();
      ctx.strokeStyle = hexA(pal.ink, 0.42 - i * 0.03);
      ctx.lineWidth = lw(2.2);
      ctx.stroke();
    }
    ctx.strokeStyle = hexA(pal.ink, 0.3);
    ctx.lineWidth = lw(1.6);
    for (let i = 0; i < 48; i++) {
      const t = Math.PI * 0.1 + (i / 48) * Math.PI * 0.9;
      ctx.beginPath();
      ctx.moveTo(cx + Math.cos(t) * r * 0.72, cy + Math.sin(t) * r * 0.65);
      ctx.lineTo(cx + Math.cos(t) * r * 1.02, cy + Math.sin(t) * r * 0.92);
      ctx.stroke();
    }
  }

  /* ---------- districts ---------- */
  for (const d of m.districts.filter(inPeriod)) {
    polygon(ctx, d.polygon.map(P));
    ctx.fillStyle = hexA(pal.ink, 0.035);
    ctx.fill();
    ctx.setLineDash([lw(10), lw(7)]);
    ctx.strokeStyle = hexA(pal.ink, 0.55);
    ctx.lineWidth = lw(2.4);
    ctx.stroke();
    ctx.setLineDash([]);
  }

  /* ---------- water, islands, boats ---------- */
  for (const w of m.water.filter(inPeriod)) {
    const pts = w.path.map(P);
    const wpx = w.width * k;
    strokePath(ctx, pts, hexA(pal.ink, 0.55), wpx + lw(5), "round");
    strokePath(ctx, pts, hexA(pal.water, 0.9), wpx, "round");
    strokePath(ctx, pts, hexA("#ffffff", 0.14), wpx * 0.55, "round");
    // engraved wave lines along the banks
    ctx.save();
    ctx.setLineDash([lw(14), lw(10)]);
    strokePath(ctx, pts, hexA("#ffffff", 0.25), lw(1.6), "round", false, wpx * 0.3);
    strokePath(ctx, pts, hexA("#ffffff", 0.25), lw(1.6), "round", false, -wpx * 0.3);
    ctx.restore();
    // boats
    const len = pathLength(pts);
    const n = Math.max(2, Math.round(len / (900 * k)));
    for (let i = 0; i < n; i++) {
      const at = pointAlong(pts, ((i + 0.5 + rnd() * 0.3) / n) * len);
      if (!at) continue;
      drawBoat(ctx, at.x + (rnd() - 0.5) * wpx * 0.5, at.y, at.angle, lw(10), pal.ink);
    }
  }
  for (const isl of m.islands.filter(inPeriod)) {
    polygon(ctx, isl.polygon.map(P));
    ctx.fillStyle = pal.parchment;
    ctx.fill();
    ctx.strokeStyle = hexA(pal.ink, 0.7);
    ctx.lineWidth = lw(2.4);
    ctx.stroke();
  }

  /* ---------- aqueducts: arcades ---------- */
  for (const a of m.aqueducts.filter(inPeriod)) {
    const pts = a.path.map(P);
    strokePath(ctx, pts, hexA(pal.ink, 0.5), lw(3.5), "butt");
    const len = pathLength(pts);
    const step = 26 * k;
    ctx.strokeStyle = hexA(pal.ink, 0.6);
    ctx.lineWidth = lw(1.6);
    for (let d = step / 2; d < len; d += step) {
      const at = pointAlong(pts, d)!;
      ctx.save();
      ctx.translate(at.x, at.y);
      ctx.rotate(at.angle);
      ctx.beginPath();
      ctx.arc(0, 0, step * 0.4, Math.PI, 0);
      ctx.stroke();
      ctx.restore();
    }
  }

  /* ---------- walls: crenellated line with towers ---------- */
  for (const wl of m.walls.filter(inPeriod)) {
    const pts = wl.path.map(P);
    ctx.beginPath();
    pts.forEach(([x, y], i) => (i === 0 ? ctx.moveTo(x, y) : ctx.lineTo(x, y)));
    if (wl.closed) ctx.closePath();
    ctx.strokeStyle = hexA(pal.ink, 0.8);
    ctx.lineWidth = lw(7);
    ctx.lineJoin = "round";
    ctx.stroke();
    ctx.strokeStyle = hexA(pal.parchment, 0.85);
    ctx.lineWidth = lw(2.5);
    ctx.setLineDash([lw(9), lw(9)]);
    ctx.stroke();
    ctx.setLineDash([]);
    const len = pathLength(pts);
    const tStep = 120 * k;
    ctx.fillStyle = hexA(pal.ink, 0.85);
    for (let d = tStep / 2; d < len; d += tStep) {
      const at = pointAlong(pts, d)!;
      ctx.save();
      ctx.translate(at.x, at.y);
      ctx.rotate(at.angle);
      ctx.fillRect(-lw(6), -lw(6), lw(12), lw(12));
      ctx.restore();
    }
  }
  for (const g of m.gates.filter(inPeriod)) {
    const [x, y] = P(g.position);
    ctx.fillStyle = hexA(pal.parchment, 1);
    ctx.strokeStyle = hexA(pal.ink, 0.9);
    ctx.lineWidth = lw(2.5);
    ctx.beginPath();
    ctx.rect(x - lw(12), y - lw(12), lw(24), lw(24));
    ctx.fill();
    ctx.stroke();
    ctx.beginPath();
    ctx.arc(x, y, lw(6), Math.PI, 0);
    ctx.stroke();
    text(ctx, g.name, x, y + lw(30), 15 * k * 1.9, pal.ink, 0, 0.8);
  }

  /* ---------- bridges ---------- */
  for (const b of m.bridges.filter(inPeriod)) {
    const pts = b.path.map(P);
    strokePath(ctx, pts, hexA(pal.ink, 0.9), lw(9), "butt");
    strokePath(ctx, pts, hexA(pal.parchment, 1), lw(5), "butt");
    const len = pathLength(pts);
    ctx.strokeStyle = hexA(pal.ink, 0.8);
    ctx.lineWidth = lw(1.4);
    for (let d = lw(8); d < len; d += lw(10)) {
      const at = pointAlong(pts, d)!;
      ctx.save();
      ctx.translate(at.x, at.y);
      ctx.rotate(at.angle);
      ctx.beginPath();
      ctx.arc(0, lw(6), lw(3.5), Math.PI, 0);
      ctx.stroke();
      ctx.restore();
    }
  }

  /* ---------- roads ---------- */
  const roads = m.roads.filter(inPeriod);
  for (const r of roads) {
    const pts = r.path.map(P);
    const w = r.width * k;
    if (r.style === "major") {
      strokePath(ctx, pts, hexA(pal.ink, 0.85), w + lw(3), "round");
      strokePath(ctx, pts, hexA(pal.parchment, 1), w, "round");
      strokePath(ctx, pts, hexA(pal.road, 0.45), w, "round");
    } else {
      strokePath(ctx, pts, hexA(pal.ink, 0.7), Math.max(lw(2), w * 0.5), "round");
    }
  }
  for (const r of roads.filter((x) => x.labelled)) {
    const pts = r.path.map(P);
    const seg = longestSegment(pts);
    if (!seg) continue;
    const size = 16 * k * (r.style === "major" ? 1.8 : 1.4);
    textAlong(ctx, r.name.toUpperCase(), seg, size, pal.ink, r.width * k * 0.5 + size * 0.55);
  }

  /* ---------- landmark footprints (only those standing in this period) ---------- */
  for (const l of city.landmarks.filter((x) => x.activePeriods.includes(periodId))) {
    const [cx, cy] = P(l.position);
    const [fw, fd] = [l.footprint[0] * k * l.scale, l.footprint[1] * k * l.scale];
    ctx.save();
    ctx.translate(cx, cy);
    ctx.rotate((l.rotation * Math.PI) / 180);
    ctx.fillStyle = hexA(pal.ink, 0.1);
    ctx.strokeStyle = hexA(pal.ink, 0.65);
    ctx.lineWidth = lw(1.6);
    ctx.beginPath();
    if (l.category === "entertainment" && Math.abs(fw - fd) < fw * 0.4) ctx.ellipse(0, 0, fw / 2, fd / 2, 0, 0, Math.PI * 2);
    else ctx.rect(-fw / 2, -fd / 2, fw, fd);
    ctx.fill();
    ctx.stroke();
    ctx.restore();
  }

  /* ---------- compass, cartouche, scale bar, border ---------- */
  if (m.compass) {
    const [cx, cy] = P(m.compass);
    drawCompass(ctx, cx, cy, Math.min(W, H) * 0.045, pal.ink, k);
  }
  {
    const [cx, cy] = m.cartouche ? P(m.cartouche) : [W * 0.03, H * 0.97];
    const bw = Math.min(W, H) * 0.3;
    const bh = bw * 0.36;
    const x0 = cx,
      y0 = cy - bh;
    ctx.fillStyle = hexA("#ffffff", 0.22);
    ctx.fillRect(x0, y0, bw, bh);
    ctx.strokeStyle = hexA(pal.ink, 0.85);
    ctx.lineWidth = lw(3);
    ctx.strokeRect(x0, y0, bw, bh);
    ctx.lineWidth = lw(1.2);
    ctx.strokeRect(x0 + lw(6), y0 + lw(6), bw - lw(12), bh - lw(12));
    text(ctx, "CHRONOSCAPE · ILLVSTRATED ATLAS", x0 + bw / 2, y0 + bh * 0.2, bh * 0.1, pal.ink, 0, 0.8, 0.3);
    text(ctx, city.name.toUpperCase(), x0 + bw / 2, y0 + bh * 0.52, bh * 0.3, pal.ink, 0, 0.95, 0.12);
    if (period) text(ctx, `${period.label.toUpperCase()} · ${formatYear(period.year)}`, x0 + bw / 2, y0 + bh * 0.72, bh * 0.11, pal.ink, 0, 0.85, 0.25);
    // scale bar: 500 map units
    const sx = x0,
      sy = y0 + bh + lw(28);
    const sl = 500 * k;
    ctx.strokeStyle = hexA(pal.ink, 0.85);
    ctx.lineWidth = lw(2);
    ctx.beginPath();
    ctx.moveTo(sx, sy);
    ctx.lineTo(sx + sl, sy);
    ctx.stroke();
    for (let i = 0; i <= 5; i++) {
      ctx.beginPath();
      ctx.moveTo(sx + (sl * i) / 5, sy - lw(5));
      ctx.lineTo(sx + (sl * i) / 5, sy + lw(5));
      ctx.stroke();
    }
    text(ctx, "500 M", sx + sl / 2, sy + lw(24), bh * 0.09, pal.ink, 0, 0.8, 0.2);
  }
  // double frame with corner ornaments
  ctx.strokeStyle = hexA(pal.ink, 0.7);
  ctx.lineWidth = lw(4);
  ctx.strokeRect(lw(14), lw(14), W - lw(28), H - lw(28));
  ctx.lineWidth = lw(1.5);
  ctx.strokeRect(lw(24), lw(24), W - lw(48), H - lw(48));
  for (const [x, y] of [[lw(19), lw(19)], [W - lw(19), lw(19)], [lw(19), H - lw(19)], [W - lw(19), H - lw(19)]]) {
    ctx.fillStyle = hexA(pal.ink, 0.8);
    ctx.beginPath();
    ctx.moveTo(x, y - lw(9));
    ctx.lineTo(x + lw(9), y);
    ctx.lineTo(x, y + lw(9));
    ctx.lineTo(x - lw(9), y);
    ctx.closePath();
    ctx.fill();
  }

  return canvas;
}

/* ---------- helpers ---------- */

function formatYear(y: number) {
  return y < 0 ? `${-y} BCE` : `${y} CE`;
}

function polygon(ctx: CanvasRenderingContext2D, pts: [number, number][]) {
  ctx.beginPath();
  pts.forEach(([x, y], i) => (i === 0 ? ctx.moveTo(x, y) : ctx.lineTo(x, y)));
  ctx.closePath();
}

function strokePath(ctx: CanvasRenderingContext2D, pts: [number, number][], style: string, width: number, cap: CanvasLineCap, dashed = false, offset = 0) {
  ctx.beginPath();
  if (offset !== 0) {
    // crude parallel offset: shift each point along the local normal
    for (let i = 0; i < pts.length; i++) {
      const a = pts[Math.max(0, i - 1)],
        b = pts[Math.min(pts.length - 1, i + 1)];
      const dx = b[0] - a[0],
        dy = b[1] - a[1];
      const L = Math.hypot(dx, dy) || 1;
      const x = pts[i][0] + (-dy / L) * offset,
        y = pts[i][1] + (dx / L) * offset;
      i === 0 ? ctx.moveTo(x, y) : ctx.lineTo(x, y);
    }
  } else {
    pts.forEach(([x, y], i) => (i === 0 ? ctx.moveTo(x, y) : ctx.lineTo(x, y)));
  }
  ctx.strokeStyle = style;
  ctx.lineWidth = width;
  ctx.lineCap = cap;
  ctx.lineJoin = "round";
  if (dashed) ctx.setLineDash([3, 4]);
  ctx.stroke();
  if (dashed) ctx.setLineDash([]);
}

function pathLength(pts: [number, number][]) {
  let L = 0;
  for (let i = 1; i < pts.length; i++) L += Math.hypot(pts[i][0] - pts[i - 1][0], pts[i][1] - pts[i - 1][1]);
  return L;
}

function pointAlong(pts: [number, number][], d: number): { x: number; y: number; angle: number } | null {
  let acc = 0;
  for (let i = 1; i < pts.length; i++) {
    const [x0, y0] = pts[i - 1],
      [x1, y1] = pts[i];
    const L = Math.hypot(x1 - x0, y1 - y0);
    if (acc + L >= d) {
      const t = (d - acc) / L;
      return { x: x0 + (x1 - x0) * t, y: y0 + (y1 - y0) * t, angle: Math.atan2(y1 - y0, x1 - x0) };
    }
    acc += L;
  }
  return null;
}

function longestSegment(pts: [number, number][]): { x0: number; y0: number; x1: number; y1: number } | null {
  let best = null as { x0: number; y0: number; x1: number; y1: number } | null;
  let bestL = 0;
  for (let i = 1; i < pts.length; i++) {
    const L = Math.hypot(pts[i][0] - pts[i - 1][0], pts[i][1] - pts[i - 1][1]);
    if (L > bestL) {
      bestL = L;
      best = { x0: pts[i - 1][0], y0: pts[i - 1][1], x1: pts[i][0], y1: pts[i][1] };
    }
  }
  return best;
}

function text(ctx: CanvasRenderingContext2D, s: string, x: number, y: number, size: number, ink: string, rot = 0, alpha = 0.85, tracking = 0.2) {
  ctx.save();
  ctx.translate(x, y);
  ctx.rotate(rot);
  ctx.font = `${Math.round(size)}px "IM Fell English", "Cormorant Garamond", Georgia, serif`;
  ctx.fillStyle = hexA(ink, alpha);
  ctx.textBaseline = "middle";
  ctx.textAlign = "center";
  // letter-spacing is not universally supported on canvas: draw per character
  const chars = s.split("");
  const widths = chars.map((c) => ctx.measureText(c).width);
  const total = widths.reduce((a, b) => a + b, 0) + tracking * size * (chars.length - 1);
  let cx = -total / 2;
  chars.forEach((c, i) => {
    ctx.textAlign = "left";
    ctx.fillText(c, cx, 0);
    cx += widths[i] + tracking * size;
  });
  ctx.restore();
}

function textAlong(ctx: CanvasRenderingContext2D, s: string, seg: { x0: number; y0: number; x1: number; y1: number }, size: number, ink: string, offset: number) {
  let angle = Math.atan2(seg.y1 - seg.y0, seg.x1 - seg.x0);
  if (angle > Math.PI / 2 || angle < -Math.PI / 2) angle += Math.PI; // keep text upright
  const mx = (seg.x0 + seg.x1) / 2,
    my = (seg.y0 + seg.y1) / 2;
  const nx = -Math.sin(angle),
    ny = Math.cos(angle);
  text(ctx, s, mx - nx * offset, my - ny * offset, size, ink, angle, 0.75, 0.22);
}

function drawBoat(ctx: CanvasRenderingContext2D, x: number, y: number, angle: number, size: number, ink: string) {
  ctx.save();
  ctx.translate(x, y);
  ctx.rotate(angle);
  ctx.strokeStyle = hexA(ink, 0.8);
  ctx.fillStyle = hexA(ink, 0.25);
  ctx.lineWidth = Math.max(0.8, size * 0.12);
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
  ctx.lineTo(0, -size * 1.3);
  ctx.stroke();
  ctx.beginPath();
  ctx.moveTo(0, -size * 1.25);
  ctx.lineTo(size * 0.55, -size * 0.55);
  ctx.lineTo(0, -size * 0.55);
  ctx.closePath();
  ctx.fill();
  ctx.restore();
}

function drawCompass(ctx: CanvasRenderingContext2D, cx: number, cy: number, r: number, ink: string, k: number) {
  ctx.save();
  ctx.translate(cx, cy);
  ctx.strokeStyle = hexA(ink, 0.75);
  ctx.fillStyle = hexA(ink, 0.75);
  ctx.lineWidth = Math.max(1, 1.4 * k * 2);
  ctx.beginPath();
  ctx.arc(0, 0, r, 0, Math.PI * 2);
  ctx.stroke();
  ctx.beginPath();
  ctx.arc(0, 0, r * 0.82, 0, Math.PI * 2);
  ctx.stroke();
  for (let i = 0; i < 16; i++) {
    const a = (i / 16) * Math.PI * 2 - Math.PI / 2;
    const len = i % 4 === 0 ? r * 0.95 : i % 2 === 0 ? r * 0.6 : r * 0.35;
    ctx.beginPath();
    ctx.moveTo(Math.cos(a) * len, Math.sin(a) * len);
    ctx.lineTo(Math.cos(a + 0.3) * r * 0.14, Math.sin(a + 0.3) * r * 0.14);
    ctx.lineTo(Math.cos(a - 0.3) * r * 0.14, Math.sin(a - 0.3) * r * 0.14);
    ctx.closePath();
    i % 4 === 0 ? ctx.fill() : ctx.stroke();
  }
  ctx.font = `${Math.round(r * 0.5)}px "IM Fell English", Georgia, serif`;
  ctx.textAlign = "center";
  ctx.textBaseline = "middle";
  ctx.fillText("N", 0, -r * 1.25);
  ctx.restore();
}

function pattern(size: number, draw: (c: CanvasRenderingContext2D) => void): CanvasPattern {
  const t = document.createElement("canvas");
  t.width = t.height = size;
  const c = t.getContext("2d")!;
  draw(c);
  return c.createPattern(t, "repeat")!;
}

function paintNoise(ctx: CanvasRenderingContext2D, W: number, H: number, rnd: () => number, strength: number) {
  const n = 128;
  const small = document.createElement("canvas");
  small.width = n;
  small.height = Math.max(8, Math.round((n * H) / W));
  const sctx = small.getContext("2d")!;
  const img = sctx.createImageData(small.width, small.height);
  for (let i = 0; i < img.data.length; i += 4) {
    const v = 128 + (rnd() - 0.5) * 255 * strength * 2;
    img.data[i] = img.data[i + 1] = img.data[i + 2] = v;
    img.data[i + 3] = 255;
  }
  sctx.putImageData(img, 0, 0);
  ctx.save();
  ctx.globalCompositeOperation = "multiply";
  ctx.globalAlpha = 0.55;
  ctx.imageSmoothingEnabled = true;
  ctx.drawImage(small, 0, 0, W, H);
  ctx.globalCompositeOperation = "screen";
  ctx.globalAlpha = 0.25;
  ctx.drawImage(small, 0, 0, W, H);
  ctx.restore();
}

function grain(ctx: CanvasRenderingContext2D, W: number, H: number, rnd: () => number) {
  const t = document.createElement("canvas");
  t.width = t.height = 256;
  const tctx = t.getContext("2d")!;
  const img = tctx.createImageData(256, 256);
  for (let i = 0; i < img.data.length; i += 4) {
    const v = 120 + (rnd() - 0.5) * 70;
    img.data[i] = img.data[i + 1] = img.data[i + 2] = v;
    img.data[i + 3] = 255;
  }
  tctx.putImageData(img, 0, 0);
  ctx.save();
  ctx.globalCompositeOperation = "overlay";
  ctx.globalAlpha = 0.26;
  ctx.fillStyle = ctx.createPattern(t, "repeat")!;
  ctx.fillRect(0, 0, W, H);
  ctx.restore();
}

export function hexA(hex: string, a: number): string {
  const r = parseInt(hex.slice(1, 3), 16),
    g = parseInt(hex.slice(3, 5), 16),
    b = parseInt(hex.slice(5, 7), 16);
  return `rgba(${r},${g},${b},${a})`;
}

function hash(s: string): number {
  let h = 2166136261;
  for (let i = 0; i < s.length; i++) h = Math.imul(h ^ s.charCodeAt(i), 16777619);
  return h >>> 0;
}

function mulberry32(seed: number) {
  let a = seed >>> 0;
  return () => {
    a = (a + 0x6d2b79f5) >>> 0;
    let t = a;
    t = Math.imul(t ^ (t >>> 15), t | 1);
    t ^= t + Math.imul(t ^ (t >>> 7), t | 61);
    return ((t ^ (t >>> 14)) >>> 0) / 4294967296;
  };
}
