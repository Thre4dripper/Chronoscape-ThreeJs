import { describe, it, expect } from "vitest";
import { mapToWorld, worldToMap, worldBounds, type Frame } from "../src/engine/coords";

const f: Frame = { scale: 0.02, width: 2400, height: 1800 };

describe("coords", () => {
  it("maps the map centre to the world origin", () => {
    expect(mapToWorld(f, [1200, 900])).toEqual([0, 0, 0]);
  });
  it("maps top-left to negative x and negative z (north is -z)", () => {
    const [x, y, z] = mapToWorld(f, [0, 0]);
    expect(x).toBeCloseTo(-24);
    expect(y).toBe(0);
    expect(z).toBeCloseTo(-18);
  });
  it("round-trips", () => {
    const p: [number, number] = [868, 788];
    const [mx, my] = worldToMap(f, mapToWorld(f, p));
    expect(mx).toBeCloseTo(p[0]);
    expect(my).toBeCloseTo(p[1]);
  });
  it("bounds match the map extent", () => {
    expect(worldBounds(f)).toEqual({ minX: -24, maxX: 24, minZ: -18, maxZ: 18 });
  });
});
