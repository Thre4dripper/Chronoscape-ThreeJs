import type { City, Vec2 } from "@/content/schema";

/**
 * Map space: map units (metres on the illustrated grid), origin top-left, y down.
 * World space: three.js units, map centre at (0,0,0), x east, z south, y up.
 */
export type Frame = { scale: number; width: number; height: number };

export function frameOf(city: City): Frame {
  return { scale: city.world.scale, width: city.map.size[0], height: city.map.size[1] };
}

export function mapToWorld(f: Frame, [mx, my]: Vec2): [number, number, number] {
  return [(mx - f.width / 2) * f.scale, 0, (my - f.height / 2) * f.scale];
}

export function worldToMap(f: Frame, [wx, , wz]: [number, number, number]): Vec2 {
  return [wx / f.scale + f.width / 2, wz / f.scale + f.height / 2];
}

/** Map-unit length to world length. */
export function mapLength(f: Frame, m: number): number {
  return m * f.scale;
}

/** World-space bounds of the map plane. */
export function worldBounds(f: Frame): { minX: number; maxX: number; minZ: number; maxZ: number } {
  const hw = (f.width * f.scale) / 2;
  const hh = (f.height * f.scale) / 2;
  return { minX: -hw, maxX: hw, minZ: -hh, maxZ: hh };
}

export const degToRad = (d: number) => (d * Math.PI) / 180;
