import { describe, it, expect } from "vitest";
import { readFileSync } from "node:fs";
import { join, resolve } from "node:path";
import { validateCity } from "../src/content/validate";
import { firstYear, questionsFor, riddleFor, bearing } from "../src/engine/codex";
import { OccGrid, clipParcel, obbOverlap, pointInPolygon } from "../src/engine/map/geom";
import { getFabric } from "../src/engine/map/fabric";
import { landmarkForEvent } from "../src/engine/store";

const root = resolve(__dirname, "..");
const { city } = validateCity(JSON.parse(readFileSync(join(root, "content", "cities", "rome", "city.json"), "utf8")));

describe("codex: dates and questions", () => {
  it("reads the first dated year from free text", () => {
    expect(firstYear("c. 72–80 CE; top storey under Domitian")).toBe(72);
    expect(firstYear("Begun under Caesar; dedicated 13 or 11 BCE")).toBe(-13);
    expect(firstYear("Timber seating 6th century BCE (traditional); starting gates 329 BCE")).toBe(-329);
    expect(firstYear("rebuilt 1560")).toBe(1560);
    expect(firstYear("unknown")).toBeNull();
  });

  it("asks well-formed questions about every landmark", () => {
    for (const l of city!.landmarks) {
      const qs = questionsFor(city!, l, l.activePeriods[0]);
      expect(qs.length).toBeGreaterThan(0);
      for (const q of qs) {
        expect(q.options.length).toBeGreaterThanOrEqual(3);
        expect(new Set(q.options).size).toBe(q.options.length); // no duplicate answers
        expect(q.answer).toBeGreaterThanOrEqual(0);
        expect(q.answer).toBeLessThan(q.options.length);
      }
    }
  });

  it("keeps the answer's name out of map riddles", () => {
    for (const p of city!.periods) {
      const r = riddleFor(city!, p.id, new Set(), 1);
      if (!r) continue;
      const l = city!.landmarks.find((x) => x.id === r.landmarkId)!;
      for (const w of l.name.split(/\W+/).filter((w) => w.length > 3)) expect(r.text.toLowerCase()).not.toContain(w.toLowerCase());
    }
  });

  it("gives directions between places", () => {
    expect(bearing(city!, "colosseum", "circus-maximus")).toMatch(/^about [\d.]+ k?m (north|south|east|west|north-east|north-west|south-east|south-west)$/);
  });

  it("raises the landmark an event takes place at", () => {
    const e = city!.events.find((x) => "landmarkId" in x.at)!;
    expect(landmarkForEvent(city!, e.id)).toBe((e.at as { landmarkId: string }).landmarkId);
  });
});

describe("open land never overlaps what is built", () => {
  it("detects overlapping rotated rectangles", () => {
    expect(obbOverlap(0, 0, 5, 5, 0, 9, 0, 5, 5, Math.PI / 4)).toBe(true);
    expect(obbOverlap(0, 0, 5, 5, 0, 20, 0, 5, 5, Math.PI / 4)).toBe(false);
  });

  it("clips a parcel back from a house", () => {
    const occ = new OccGrid(400, 400, 4);
    occ.rect(200, 200, 20, 20, 0); // a house in the middle of the field's east half
    const field: [number, number][] = [[100, 150], [220, 150], [220, 250], [100, 250]];
    const out = clipParcel(field, occ)!;
    expect(out).not.toBeNull();
    // nothing of the clipped field lies on the house
    for (let x = 181; x < 219; x += 3) for (let y = 181; y < 219; y += 3) expect(pointInPolygon(x, y, out)).toBe(false);
  });

  it("keeps Rome's fields off houses, monuments, roads and the river", () => {
    for (const pid of ["empire-100ce", "medieval-1300"]) {
      const fab = getFabric(city!, pid);
      let bad = 0, total = 0;
      for (const f of fab.fields) {
        // sample inside each field: no point may sit on a house or monument
        for (let k = 0; k < 6; k++) {
          const a = f.pts[k % f.pts.length], b = f.pts[(k + 2) % f.pts.length];
          const x = f.cx + (a[0] - f.cx) * 0.7 + (b[0] - f.cx) * 0.2, y = f.cy + (a[1] - f.cy) * 0.7 + (b[1] - f.cy) * 0.2;
          if (!pointInPolygon(x, y, f.pts)) continue;
          total++;
          if (fab.occ.at(x, y, OccGrid.BUILT)) bad++;
        }
      }
      expect(total).toBeGreaterThan(100);
      expect(bad / total).toBeLessThan(0.01);
    }
  });

  it("never lays two blocks of houses on top of each other", () => {
    const fab = getFabric(city!, "empire-100ce");
    const ins = fab.insulae;
    let hits = 0;
    for (let i = 0; i < ins.length; i++)
      for (const j of fab.index.near(ins[i].x, ins[i].y, Math.hypot(ins[i].w, ins[i].d))) {
        if (j.id <= ins[i].id) continue;
        const a = ins[i], b = j;
        if (obbOverlap(a.x, a.y, a.w / 2, a.d / 2, a.a, b.x, b.y, b.w / 2, b.d / 2, b.a)) hits++;
      }
    expect(hits).toBe(0);
  });
});
