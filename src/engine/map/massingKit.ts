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
  gothic: ["#e4d8c0", "#d9cbb0", "#cdbf9f", "#e9e0cc"],
  courtyard: ["#e2cfac", "#d8bf96", "#ead9bb", "#cdb089"],
  sinic: ["#cfc5b3", "#c4b8a2", "#d9cfbd", "#b9ac95"],
  japanese: ["#d9c8a8", "#cdb895", "#e2d5bb"],
  mesoamerican: ["#ece4d2", "#e4d9c2", "#f1ebdd"],
  andean: ["#b8ab95", "#a99c86", "#c2b6a1"],
  sahel: ["#c99f72", "#be9266", "#d1aa7e"],
  kraal: ["#b98f68", "#ad8560"],
};
const ROOFS: Record<Style, string[]> = {
  archaic: ["#a99a72"],
  antique: ["#b0614a", "#a65a44", "#bb6c52"],
  medieval: ["#a6644d", "#9a5d47", "#af6d54"],
  "early-modern": ["#b4674d", "#be7258", "#a95f47"],
  gothic: ["#6f6a6c", "#7c6458", "#8a5a48", "#666468"],
  courtyard: ["#c9b28c"],
  sinic: ["#6c6a68", "#5f5e5e", "#757371"],
  japanese: ["#5f5c5a", "#6a6560", "#8a7a5c"],
  mesoamerican: ["#d9cdb4"],
  andean: ["#a8925c", "#9c8854"],
  sahel: ["#b38a5e"],
  kraal: ["#a8955f", "#9d8a56"],
};
/** Roof pitch (height / span) and eaves overhang per tradition: low Mediterranean tile, steep northern slate, wide East Asian eaves, steep Andean thatch. */
const PITCH: Partial<Record<Style, [number, number]>> = {
  archaic: [0.3, 1.04], gothic: [0.62, 1.04], sinic: [0.3, 1.16], japanese: [0.34, 1.14], andean: [0.6, 1.08],
};
const AWNINGS = ["#b5735a", "#c2a66d", "#8f9a7a", "#9a8fa8", "#b9b0a0"];
const TIMBER = "#8c7259";
const STONE = "#c9c2b4";

export type MassingPalette = { walls?: string[]; roofs?: string[] };

export function piecesFor(style: Style, b: Insula, lots: Lot[], pal: MassingPalette = {}): Piece[] {
  const walls = pal.walls ?? WALLS[style], roofs = pal.roofs ?? ROOFS[style];
  const thatch = style === "kraal" || style === "archaic";
  const out: Piece[] = [];
  const cb = Math.cos(b.a), sb = Math.sin(b.a);
  for (let i = b.lot0; i < b.lot1; i++) {
    const l = lots[i];
    if (l.kind === "court") continue;
    const ca = Math.cos(l.a), sa = Math.sin(l.a);
    const at = (ou: number, ov: number): [number, number] => [l.x + ca * ou - sa * ov, l.y + sa * ou + ca * ov];
    const wall = walls[Math.floor(r(i, 1) * walls.length)];
    const roofC = roofs[Math.floor(r(i, 2) * roofs.length)];
    const push = (mesh: PieceMesh, ou: number, ov: number, w: number, d: number, h: number, z: number, color: string) => {
      const [x, y] = at(ou, ov);
      out.push({ mesh, x, y, a: l.a, w, d, h, z, color });
    };

    if (l.kind === "hut") {
      out.push({ mesh: "hutBody", x: l.x, y: l.y, a: l.a, w: l.w, d: l.d, h: l.h * 0.55, z: 0, color: thatch && !pal.walls ? (style === "kraal" ? wall : "#b9a582") : wall });
      out.push({ mesh: "hutRoof", x: l.x, y: l.y, a: l.a, w: l.w * 1.12, d: l.d * 1.12, h: l.h * 0.85, z: l.h * 0.55, color: style === "archaic" && !pal.roofs ? "#a8955f" : roofC });
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

    if ((style === "medieval" || style === "gothic") && roll < (style === "gothic" ? 0.6 : 0.45) && h > 6) {
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

    const roofW = roll < 0.22 && (style === "antique" || style === "early-modern") && h > 9 ? 0.72 : 1;
    if (flat) {
      // roof terrace: parapet and a small rooftop room or pergola
      const p = 0.3;
      push("trim", 0, -(l.d * roofW) / 2 + p / 2, l.w * roofW, p, 1.0, h, shadeHex(wall, -0.05));
      push("trim", 0, (l.d * roofW) / 2 - p / 2, l.w * roofW, p, 1.0, h, shadeHex(wall, -0.05));
      push("trim", -(l.w * roofW) / 2 + p / 2, 0, p, l.d * roofW, 1.0, h, shadeHex(wall, -0.05));
      push("trim", (l.w * roofW) / 2 - p / 2, 0, p, l.d * roofW, 1.0, h, shadeHex(wall, -0.05));
      const roomy = style === "courtyard" || style === "sahel" ? 0.35 : style === "mesoamerican" ? 0.15 : 0.5;
      if (r(i, 4) < roomy) push("body", l.w * 0.15, l.d * 0.1, l.w * 0.35, l.d * 0.35, 2.6, h, shadeHex(wall, 0.03));
      // a wind-catcher or a little domed kiosk on some courtyard-house roofs
      else if (style === "courtyard" && r(i, 4) > 0.9 && h > 6) push("trim", -l.w * 0.2, -l.d * 0.2, 1.4, 1.4, 3.2, h, shadeHex(wall, -0.04));
    } else {
      if (style === "early-modern") push("trim", 0, 0, l.w * roofW * 1.05, l.d * roofW * 1.05, 0.5, h - 0.5, shadeHex(wall, 0.06));
      // Roman and Italian tile roofs are low (about 20 degrees); northern and Andean roofs are steep
      const [pitch, eave] = PITCH[style] ?? [0.17, 1.04];
      // East Asian houses stand on a low stone plinth under wide eaves
      if (style === "sinic" || style === "japanese") push("trim", 0, 0, l.w * 1.02, l.d * 1.02, 0.45, 0, STONE);
      push("roof", 0, 0, l.w * roofW * eave, l.d * roofW * eave, Math.min(l.w, l.d) * roofW * pitch, h, roofC);
      const chimneys = style === "medieval" || style === "early-modern" || style === "gothic" ? 0.45 : 0;
      if (r(i, 5) < chimneys) push("trim", l.w * 0.25, -l.d * 0.2, 0.7, 0.7, Math.min(l.w, l.d) * pitch * 1.6 + 1.2, h, shadeHex(wall, -0.1));
      if (style === "early-modern" && r(i, 6) < 0.1) push("body", -l.w * 0.2, 0, l.w * 0.3, l.d * 0.3, 3, h + Math.min(l.w, l.d) * 0.12, shadeHex(wall, 0.05)); // altana
    }

    // street front: shop awnings, timber balconies
    if (street) {
      const [su, sv] = street;
      const side = su !== 0 ? l.d : l.w;
      const ou = (su * l.w) / 2, ov = (sv * l.d) / 2;
      const depth = 1.6;
      const aw = su !== 0 ? [depth, side * 0.8] : [side * 0.8, depth];
      const shops = style === "archaic" || style === "kraal" || style === "andean" ? 0 : style === "antique" ? 0.4 : style === "sinic" || style === "mesoamerican" ? 0.25 : 0.6;
      if ((style === "medieval" || style === "gothic") && r(i, 7) < 0.4) {
        push("trim", ou + (su * depth) / 2, ov + (sv * depth) / 2, aw[0], aw[1], 0.3, Math.min(h * 0.55, 5.5), TIMBER);
      } else if (style === "antique" && h > 9 && r(i, 7) < 0.45) {
        // maenianum: a timber balcony along the first floor of an insula, over the shops
        push("trim", ou + (su * 0.6) / 2, ov + (sv * 0.6) / 2, su !== 0 ? 1.2 : side * 0.9, su !== 0 ? side * 0.9 : 1.2, 0.25, 3.6, TIMBER);
        push("trim", ou + su * 1.1, ov + sv * 1.1, su !== 0 ? 0.12 : side * 0.9, su !== 0 ? side * 0.9 : 0.12, 0.9, 3.85, TIMBER);
      } else if (r(i, 7) < shops) {
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
