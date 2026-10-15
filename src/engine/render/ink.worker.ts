/// <reference lib="webworker" />
/**
 * Ink lines for a model: every crease sharper than the threshold and every open
 * edge, as line-segment endpoints. Same rule as three's EdgesGeometry, run off the
 * main thread so a 200k-triangle monument never stalls a hover.
 */
type Req = { id: number; pos: Float32Array; index: Uint32Array | null; angle: number };

self.onmessage = (e: MessageEvent<Req>) => {
  const { id, pos, index, angle } = e.data;
  const thr = Math.cos((angle * Math.PI) / 180);
  const triCount = index ? index.length / 3 : pos.length / 9;
  // weld by quantised position so split vertices (colour seams) still share edges
  const q = 1e3;
  const ids = new Map<string, number>();
  const weld = (vi: number) => {
    const k = `${Math.round(pos[vi * 3] * q)},${Math.round(pos[vi * 3 + 1] * q)},${Math.round(pos[vi * 3 + 2] * q)}`;
    let w = ids.get(k);
    if (w === undefined) {
      w = ids.size;
      ids.set(k, w);
    }
    return w;
  };
  const edges = new Map<number, { a: number; b: number; nx: number; ny: number; nz: number; shared: boolean; keep: boolean }>();
  const out: number[] = [];
  for (let t = 0; t < triCount; t++) {
    const v = [0, 1, 2].map((j) => (index ? index[t * 3 + j] : t * 3 + j));
    const p = v.map((vi) => [pos[vi * 3], pos[vi * 3 + 1], pos[vi * 3 + 2]]);
    const ux = p[1][0] - p[0][0], uy = p[1][1] - p[0][1], uz = p[1][2] - p[0][2];
    const wx = p[2][0] - p[0][0], wy = p[2][1] - p[0][1], wz = p[2][2] - p[0][2];
    let nx = uy * wz - uz * wy, ny = uz * wx - ux * wz, nz = ux * wy - uy * wx;
    const L = Math.hypot(nx, ny, nz);
    if (L < 1e-12) continue;
    nx /= L; ny /= L; nz /= L;
    const w = v.map(weld);
    for (let j = 0; j < 3; j++) {
      const a = w[j], b = w[(j + 1) % 3];
      if (a === b) continue;
      const key = a < b ? a * 4194304 + b : b * 4194304 + a;
      const hit = edges.get(key);
      if (!hit) edges.set(key, { a: v[j], b: v[(j + 1) % 3], nx, ny, nz, shared: false, keep: false });
      else if (!hit.shared) {
        hit.shared = true;
        if (hit.nx * nx + hit.ny * ny + hit.nz * nz <= thr) hit.keep = true;
      }
    }
  }
  for (const e2 of edges.values()) {
    if (e2.shared && !e2.keep) continue;
    out.push(pos[e2.a * 3], pos[e2.a * 3 + 1], pos[e2.a * 3 + 2], pos[e2.b * 3], pos[e2.b * 3 + 1], pos[e2.b * 3 + 2]);
  }
  const arr = new Float32Array(out);
  (self as unknown as Worker).postMessage({ id, lines: arr }, [arr.buffer]);
};
