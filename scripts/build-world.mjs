/**
 * Coastlines for the engraved world and regional maps (title page, map room,
 * atlas covers): Natural Earth land (public domain) via world-atlas, decoded
 * from TopoJSON and written as plain rings of [lon, lat] rounded to 0.05 deg.
 * Two levels: 110m for the world view, 50m for regional close-ups.
 *
 *   node scripts/build-world.mjs
 */
import { readFileSync, writeFileSync, mkdirSync } from "node:fs";
import { feature } from "topojson-client";

/** Douglas-Peucker on an open chain (rings keep their first and last point). */
function simplify(pts, tol) {
  if (pts.length < 5) return pts;
  const keep = new Uint8Array(pts.length);
  keep[0] = keep[pts.length - 1] = 1;
  const stack = [[0, pts.length - 1]];
  while (stack.length) {
    const [a, b] = stack.pop();
    const [ax, ay] = pts[a], [bx, by] = pts[b];
    const dx = bx - ax, dy = by - ay, L2 = dx * dx + dy * dy || 1e-12;
    let best = -1, bd = tol;
    for (let i = a + 1; i < b; i++) {
      const t = Math.max(0, Math.min(1, ((pts[i][0] - ax) * dx + (pts[i][1] - ay) * dy) / L2));
      const d = Math.hypot(pts[i][0] - ax - dx * t, pts[i][1] - ay - dy * t);
      if (d > bd) ((bd = d), (best = i));
    }
    if (best >= 0) ((keep[best] = 1), stack.push([a, best], [best, b]));
  }
  return pts.filter((_, i) => keep[i]);
}

const out = {};
for (const res of ["110m", "50m"]) {
  const topo = JSON.parse(readFileSync(`node_modules/world-atlas/land-${res}.json`, "utf8"));
  const land = feature(topo, topo.objects.land);
  const q = res === "110m" ? 10 : 20; // 0.1 deg / 0.05 deg
  const rings = [];
  for (const f of land.features) {
    const polys = f.geometry.type === "Polygon" ? [f.geometry.coordinates] : f.geometry.coordinates;
    for (const poly of polys)
      for (const ring of poly) {
        const r = [];
        let last = null;
        for (const [lon, lat] of ring) {
          const p = [Math.round(lon * q) / q, Math.round(lat * q) / q];
          if (last && last[0] === p[0] && last[1] === p[1]) continue;
          r.push(p);
          last = p;
        }
        // drop specks: at 110m keep rings with a few points, at 50m only those bigger than ~0.3 deg across
        // rings that cross the antimeridian jump from +180 to -180: unwrap them so they stay continuous
        // (the renderer draws the world three times side by side, so the overhang shows up on the other edge)
        let off = 0;
        for (let i = 1; i < r.length; i++) {
          const d = r[i][0] + off - r[i - 1][0];
          if (d > 180) off -= 360;
          else if (d < -180) off += 360;
          r[i] = [r[i][0] + off, r[i][1]];
        }
        const rs = res === "50m" ? simplify(r, 0.03) : [...r];
        r.length = 0;
        r.push(...rs);
        if (r.length >= 4) {
          let x0 = 999, x1 = -999, y0 = 999, y1 = -999;
          for (const [x, y] of r) ((x0 = Math.min(x0, x)), (x1 = Math.max(x1, x)), (y0 = Math.min(y0, y)), (y1 = Math.max(y1, y)));
          if (res === "110m" || x1 - x0 + y1 - y0 > 0.3) rings.push(r);
        }
      }
  }
  out[res] = rings;
  console.log(res, rings.length, "rings", rings.reduce((a, r) => a + r.length, 0), "points");
}
mkdirSync("assets/world", { recursive: true });
writeFileSync("assets/world/land-110m.json", JSON.stringify(out["110m"]));
writeFileSync("assets/world/land-50m.json", JSON.stringify(out["50m"]));
