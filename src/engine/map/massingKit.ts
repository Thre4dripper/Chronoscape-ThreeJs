import type { Insula, Lot, Style } from "./fabric";

/**
 * Turns the lots of a city block into simple architectural pieces for the
 * hover model: bodies (with window grids from the shader), hipped roofs,
 * roof terraces, setbacks, jettied upper floors, cornices, chimneys, awnings
 * and balconies on the street side, crenellated towers, thatched huts.
 * Deterministic per lot, varied per era.
 */
export type PieceMesh = "body" | "roof" | "trim" | "hutBody" | "hutRoof";
export type Piece = { mesh: PieceMesh; x: number; y: number; a: number; w: number; d: number; h: number; z: number; color: string };

const r = (i: number, k: number) => {
  const v = Math.sin(i * 12.9898 + k * 78.233) * 43758.5453;
  return v - Math.floor(v);
};

// warm plaster, brick and travertine, like a painted architectural miniature
const WALLS: Record<Style, string[]> = {
  archaic: ["#c8b08a", "#bfa47f"],
  antique: ["#e0cba8", "#d6b78f", "#e6d6bb", "#c99a74", "#dcc29c", "#cfa883"],
  medieval: ["#d6c4a5", "#cbb491", "#ddcdb1", "#c2a888"],
  "early-modern": ["#e7d5b5", "#ddc199", "#eadbc2", "#d4b089"],
};
const ROOFS: Record<Style, string[]> = {
  archaic: ["#a99a72"],
  antique: ["#b0614a", "#a65a44", "#bb6c52"],
  medieval: ["#a6644d", "#9a5d47", "#af6d54"],
  "early-modern": ["#b4674d", "#be7258", "#a95f47"],
};
const AWNINGS = ["#b5735a", "#c2a66d", "#8f9a7a", "#9a8fa8", "#b9b0a0"];
const TIMBER = "#8c7259";
const STONE = "#c9c2b4";

export function piecesFor(style: Style, b: Insula, lots: Lot[]): Piece[] {
  const out: Piece[] = [];
  const cb = Math.cos(b.a), sb = Math.sin(b.a);
  for (let i = b.lot0; i < b.lot1; i++) {
    const l = lots[i];
    if (l.kind === "court") continue;
    const ca = Math.cos(l.a), sa = Math.sin(l.a);
    const at = (ou: number, ov: number): [number, number] => [l.x + ca * ou - sa * ov, l.y + sa * ou + ca * ov];
    const wall = WALLS[style][Math.floor(r(i, 1) * WALLS[style].length)];
    const roofC = ROOFS[style][Math.floor(r(i, 2) * ROOFS[style].length)];
    const push = (mesh: PieceMesh, ou: number, ov: number, w: number, d: number, h: number, z: number, color: string) => {
      const [x, y] = at(ou, ov);
      out.push({ mesh, x, y, a: l.a, w, d, h, z, color });
    };

    if (l.kind === "hut") {
      out.push({ mesh: "hutBody", x: l.x, y: l.y, a: l.a, w: l.w, d: l.d, h: l.h * 0.55, z: 0, color: "#b9a582" });
      out.push({ mesh: "hutRoof", x: l.x, y: l.y, a: l.a, w: l.w * 1.12, d: l.d * 1.12, h: l.h * 0.85, z: l.h * 0.55, color: "#a8955f" });
      continue;
    }

    if (l.kind === "tower") {
      push("body", 0, 0, l.w, l.d, l.h, 0, STONE);
      const m = Math.max(0.8, l.w * 0.16);
      for (const [u, v] of [[-1, -1], [1, -1], [1, 1], [-1, 1], [0, -1], [0, 1], [-1, 0], [1, 0]]) push("trim", (u * (l.w - m)) / 2, (v * (l.d - m)) / 2, m, m, 1.4, l.h, STONE);
      continue;
    }

    // which side of the block does this lot face the street on?
    const dx = l.x - b.x, dy = l.y - b.y;
    const lu = dx * cb + dy * sb, lv = -dx * sb + dy * cb;
    let street: [number, number] | null = null;
    if (lu + l.w / 2 > b.w / 2 - 1.5) street = [1, 0];
    else if (lu - l.w / 2 < -b.w / 2 + 1.5) street = [-1, 0];
    else if (lv + l.d / 2 > b.d / 2 - 1.5) street = [0, 1];
    else if (lv - l.d / 2 < -b.d / 2 + 1.5) street = [0, -1];

    const roll = r(i, 3);
    let h = l.h;
    const flat = l.roof === "flat";

    if (style === "medieval" && roll < 0.45 && h > 6) {
      // jettied house: the upper floors overhang the lower one
      const low = h * 0.45;
      push("body", 0, 0, l.w, l.d, low, 0, wall);
      // the overhang stays inside the lot's own half-metre margin, so neighbours never intersect
      const jw = Math.min(l.w * 1.06, l.w + 0.4), jd = Math.min(l.d * 1.08, l.d + 0.4);
      push("body", 0, 0, jw, jd, h - low, low, shadeHex(wall, 0.04));
      push("trim", 0, 0, jw + 0.1, jd + 0.1, 0.25, low, TIMBER);
    } else if ((style === "antique" || style === "early-modern") && roll < 0.22 && h > 9) {
      // setback attic storey
      const low = h * 0.78;
      push("body", 0, 0, l.w, l.d, low, 0, wall);
      push("body", 0, 0, l.w * 0.72, l.d * 0.72, h - low, low, shadeHex(wall, 0.05));
      push("trim", 0, 0, l.w, l.d, 0.35, low, shadeHex(wall, -0.08));
      h = h; // roof sits on the attic
    } else {
      push("body", 0, 0, l.w, l.d, h, 0, wall);
    }

    const roofW = roll < 0.22 && style !== "medieval" && h > 9 ? 0.72 : 1;
    if (flat) {
      // roof terrace: parapet and a small rooftop room or pergola
      const p = 0.3;
      push("trim", 0, -(l.d * roofW) / 2 + p / 2, l.w * roofW, p, 1.0, h, shadeHex(wall, -0.05));
      push("trim", 0, (l.d * roofW) / 2 - p / 2, l.w * roofW, p, 1.0, h, shadeHex(wall, -0.05));
      push("trim", -(l.w * roofW) / 2 + p / 2, 0, p, l.d * roofW, 1.0, h, shadeHex(wall, -0.05));
      push("trim", (l.w * roofW) / 2 - p / 2, 0, p, l.d * roofW, 1.0, h, shadeHex(wall, -0.05));
      if (r(i, 4) < 0.5) push("body", l.w * 0.15, l.d * 0.1, l.w * 0.35, l.d * 0.35, 2.6, h, shadeHex(wall, 0.03));
    } else {
      if (style === "early-modern") push("trim", 0, 0, l.w * roofW * 1.05, l.d * roofW * 1.05, 0.5, h - 0.5, shadeHex(wall, 0.06));
      // Roman and Italian tile roofs are low (about 20 degrees); northern-style roofs would be steeper
      const pitch = style === "archaic" ? 0.3 : 0.17;
      push("roof", 0, 0, l.w * roofW * 1.04, l.d * roofW * 1.04, Math.min(l.w, l.d) * roofW * pitch, h, roofC);
      if (style !== "antique" && r(i, 5) < 0.45) push("trim", l.w * 0.25, -l.d * 0.2, 0.7, 0.7, Math.min(l.w, l.d) * 0.3 + 1.2, h, shadeHex(wall, -0.1));
      if (style === "early-modern" && r(i, 6) < 0.1) push("body", -l.w * 0.2, 0, l.w * 0.3, l.d * 0.3, 3, h + Math.min(l.w, l.d) * 0.12, shadeHex(wall, 0.05)); // altana
    }

    // street front: shop awnings, timber balconies
    if (street) {
      const [su, sv] = street;
      const side = su !== 0 ? l.d : l.w;
      const ou = (su * l.w) / 2, ov = (sv * l.d) / 2;
      const depth = 1.6;
      const aw = su !== 0 ? [depth, side * 0.8] : [side * 0.8, depth];
      if (style === "medieval" && r(i, 7) < 0.4) {
        push("trim", ou + (su * depth) / 2, ov + (sv * depth) / 2, aw[0], aw[1], 0.3, Math.min(h * 0.55, 5.5), TIMBER);
      } else if (style === "antique" && h > 9 && r(i, 7) < 0.45) {
        // maenianum: a timber balcony along the first floor of an insula, over the shops
        push("trim", ou + (su * 0.6) / 2, ov + (sv * 0.6) / 2, su !== 0 ? 1.2 : side * 0.9, su !== 0 ? side * 0.9 : 1.2, 0.25, 3.6, TIMBER);
        push("trim", ou + su * 1.1, ov + sv * 1.1, su !== 0 ? 0.12 : side * 0.9, su !== 0 ? side * 0.9 : 0.12, 0.9, 3.85, TIMBER);
      } else if (r(i, 7) < (style === "archaic" ? 0 : style === "antique" ? 0.4 : 0.6)) {
        push("trim", ou + (su * depth) / 2, ov + (sv * depth) / 2, aw[0], aw[1], 0.18, 3.0, AWNINGS[Math.floor(r(i, 8) * AWNINGS.length)]);
      }
    }
  }
  return out;
}

export function shadeHex(hex: string, amt: number): string {
  const n = parseInt(hex.slice(1), 16);
  const ch = (v: number) => Math.max(0, Math.min(255, Math.round(amt > 0 ? v + (255 - v) * amt : v * (1 + amt))));
  const rr = ch((n >> 16) & 255), gg = ch((n >> 8) & 255), bb = ch(n & 255);
  return `#${((1 << 24) | (rr << 16) | (gg << 8) | bb).toString(16).slice(1)}`;
}
