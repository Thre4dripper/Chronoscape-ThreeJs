import { Suspense, useEffect, useMemo, useRef, useState } from "react";
import { useFrame } from "@react-three/fiber";
import * as THREE from "three";
import type { City, Vec2 } from "@/content/schema";
import { frameOf } from "../coords";
import { useStore } from "../store";
import { groundPointer } from "./pointer";
import { OccGrid, chaikin, distToSeg, hash, mulberry32, pathLength, pointAlong } from "./geom";
import { getFabric } from "./fabric";
import { prefersReducedMotion } from "../motion";
import { InstancedGlb } from "./InstancedGlb";
import { bakeify, shaded } from "../render/baked";
import { useModel } from "../render/models";

/**
 * Linear things that rise around the pointer: a stretch of city wall with
 * towers and crenellations, a gatehouse, an aqueduct arcade, boats working the
 * river, trees and goats on a hillside.
 */
const EXAG = 2.2;

type Run = { key: string; kind: "wall" | "aqueduct" | "river" | "hill" | "bridge"; path: Vec2[]; s0: number; gate?: Vec2; width?: number; center?: Vec2; radius?: number; build?: "stone" | "timber"; arches?: number };

export function LinePopout({ city }: { city: City }) {
  const periodId = useStore((s) => s.periodId) ?? city.defaultPeriodId;
  const inP = (f: { periods?: string[] }) => !f.periods || f.periods.includes(periodId);
  const [runs, setRuns] = useState<Run[]>([]);
  const current = useRef<string | null>(null);
  const rivers = useMemo(() => city.map.water.filter(inP).map((w) => ({ ...w, smooth: chaikin(w.path, 3) })), [city, periodId]); // eslint-disable-line react-hooks/exhaustive-deps

  useFrame(() => {
    const st = useStore.getState();
    const feat = st.hoveredFeature;
    let run: Run | null = null;
    if (feat && groundPointer.valid && st.mode !== "immersed") {
      const { mx, my } = groundPointer;
      if (feat.kind === "wall") {
        const w = city.map.walls.find((x, i) => (x.id ?? `wall${i}`) === feat.id);
        if (w) {
          const path = w.closed ? [...w.path, w.path[0]] : w.path;
          const s0 = nearestS(path, mx, my);
          run = { key: `wall:${feat.id}:${Math.round(s0 / 80)}`, kind: "wall", path, s0: Math.round(s0 / 80) * 80 };
        }
      } else if (feat.kind === "gate") {
        const g = city.map.gates.find((x, i) => (x.id ?? `gate${i}`) === feat.id);
        const walls = city.map.walls.filter(inP);
        if (g && walls.length) {
          let best = walls[0], bd = Infinity;
          for (const w of walls) {
            const path = w.closed ? [...w.path, w.path[0]] : w.path;
            const d = distPath(path, g.position[0], g.position[1]);
            if (d < bd) {
              bd = d;
              best = w;
            }
          }
          const path = best.closed ? [...best.path, best.path[0]] : best.path;
          run = { key: `gate:${feat.id}`, kind: "wall", path, s0: nearestS(path, g.position[0], g.position[1]), gate: g.position };
        }
      } else if (feat.kind === "aqueduct") {
        const idx = Number(feat.id.replace("aqueduct", ""));
        const a = city.map.aqueducts[idx];
        if (a) {
          const s0 = nearestS(a.path, mx, my);
          run = { key: `aq:${idx}:${Math.round(s0 / 90)}`, kind: "aqueduct", path: a.path, s0: Math.round(s0 / 90) * 90 };
        }
      } else if (feat.kind === "water") {
        const r = rivers.find((w, i) => (w.id ?? `water${i}`) === feat.id) ?? rivers[0];
        if (r) {
          const s0 = nearestS(r.smooth, mx, my);
          run = { key: `river:${feat.id}:${Math.round(s0 / 250)}`, kind: "river", path: r.smooth, s0, width: r.width };
        }
      } else if (feat.kind === "bridge") {
        const b = city.map.bridges.find((x, i) => (x.id ?? `bridge${i}`) === feat.id);
        if (b) run = { key: `bridge:${feat.id}`, kind: "bridge", path: b.path, s0: 0, build: b.build, arches: b.arches };
      } else if (feat.kind === "hill" && st.hoveredBlockId === null && !st.hoveredArea && !getFabric(city, periodId).index.at(mx, my, 30)) {
        const h = city.map.hills.find((x, i) => (x.id ?? `hill${i}`) === feat.id);
        if (h) run = { key: `hill:${feat.id}`, kind: "hill", path: [], s0: 0, center: h.center, radius: h.radius };
      }
    }
    const key = run ? run.key : null;
    if (key !== current.current) {
      current.current = key;
      setRuns((prev) => {
        const rest = prev.filter((r) => r.key !== key);
        return run ? [...rest, run] : rest;
      });
    }
  });

  return (
    <group>
      {runs.map((r) => {
        const props = { city, run: r, active: current.current === r.key, onGone: () => setRuns((prev) => prev.filter((p) => p.key !== r.key)) };
        return (
          <Suspense key={r.key} fallback={null}>
            {r.kind === "river" ? <Boats {...props} /> : r.kind === "hill" ? <Hillside {...props} /> : r.kind === "bridge" ? <Bridge {...props} /> : <Masonry {...props} />}
          </Suspense>
        );
      })}
    </group>
  );
}

type PartProps = { city: City; run: Run; active: boolean; onGone: () => void };

function useRise(active: boolean, onGone: () => void, rate = 6) {
  const group = useRef<THREE.Group>(null);
  const p = useRef(0);
  const gone = useRef(false);
  useFrame((_, dtRaw) => {
    const dt = Math.min(dtRaw, 0.1);
    p.current += ((active ? 1 : 0) - p.current) * (prefersReducedMotion() ? 1 : 1 - Math.exp(-rate * dt));
    if (!active && p.current < 0.01 && !gone.current) {
      gone.current = true;
      onGone();
    }
    if (group.current) group.current.scale.y = Math.max(0.001, 1 - Math.pow(1 - p.current, 3));
  });
  return { group, p };
}

/** Wall or aqueduct stretch: Blender bays (curtain, towers, gatehouse, arches) laid along the path around s0. */
const BAY = { wall: 6, aqueduct: 8 }; // metres per bay in the Blender pieces

function Masonry({ city, run, active, onGone }: PartProps) {
  const f = frameOf(city);
  const [MW, MH] = city.map.size;
  const { group } = useRise(active, onGone);
  const ex = run.kind === "wall" ? 1.5 : 1.35; // a little larger than life so it reads
  const sets = useMemo(() => {
    const L = pathLength(run.path);
    const half = run.kind === "wall" ? 170 : 200;
    const a0 = Math.max(0, run.s0 - half), a1 = Math.min(L, run.s0 + half);
    const s = f.scale * ex;
    const step = (run.kind === "wall" ? BAY.wall : BAY.aqueduct) * ex;
    const mk = (x: number, y: number, angle: number, sx = 1) => {
      const m = new THREE.Matrix4();
      // Blender pieces run along +Y (three -Z after export); turn them to follow the path
      m.compose(new THREE.Vector3((x - MW / 2) * f.scale, 0, (y - MH / 2) * f.scale), new THREE.Quaternion().setFromEuler(new THREE.Euler(0, -angle - Math.PI / 2, 0)), new THREE.Vector3(s, s, s * sx));
      return m;
    };
    const bays: THREE.Matrix4[] = [], towers: THREE.Matrix4[] = [], gates: THREE.Matrix4[] = [];
    let gateS = -1;
    if (run.gate) gateS = run.s0;
    for (let d = a0 + step / 2; d < a1; d += step) {
      if (gateS >= 0 && Math.abs(d - gateS) < 16 * ex) continue;
      const at = pointAlong(run.path, d);
      if (!at) continue;
      // stretch each bay a little so consecutive bays close the gap on bends
      bays.push(mk(at.x, at.y, at.angle, 1.04));
    }
    if (run.kind === "wall") {
      for (let d = Math.ceil(a0 / 30) * 30; d < a1; d += 30) {
        if (gateS >= 0 && Math.abs(d - gateS) < 20 * ex) continue;
        const at = pointAlong(run.path, d);
        if (at) towers.push(mk(at.x, at.y, at.angle));
      }
      if (gateS >= 0) {
        const at = pointAlong(run.path, gateS);
        if (at) gates.push(mk(at.x, at.y, at.angle));
      }
    }
    return { bays, towers, gates };
  }, [run, f.scale, MW, MH, ex]);
  return (
    <group ref={group}>
      <InstancedGlb url={run.kind === "wall" ? "/models/props/wall-bay.glb" : "/models/props/aqueduct-bay.glb"} matrices={sets.bays} />
      {sets.towers.length > 0 && <InstancedGlb url="/models/props/wall-tower.glb" matrices={sets.towers} />}
      {sets.gates.length > 0 && <InstancedGlb url="/models/props/gatehouse.glb" matrices={sets.gates} />}
    </group>
  );
}

/**
 * A bridge across the river: stone arches (or timber pile bays for the Pons
 * Sublicius) laid end to end along its line, a little wider than life so it reads.
 */
function Bridge({ city, run, active, onGone }: PartProps) {
  const f = frameOf(city);
  const [MW, MH] = city.map.size;
  const { group } = useRise(active, onGone, 5);
  const timber = run.build === "timber";
  const matrices = useMemo(() => {
    const L = pathLength(run.path);
    const ex = 1.3;
    const bay = timber ? 12 : 20; // metres per Blender piece along +Y
    const n = Math.max(run.arches ?? 3, timber ? Math.round(L / 14) : 1);
    const s = f.scale * ex;
    const sx = L / (n * bay * ex);
    const out: THREE.Matrix4[] = [];
    for (let i = 0; i < n; i++) {
      const at = pointAlong(run.path, (i + 0.5) * (L / n));
      if (!at) continue;
      const m = new THREE.Matrix4();
      m.compose(new THREE.Vector3((at.x - MW / 2) * f.scale, 0, (at.y - MH / 2) * f.scale), new THREE.Quaternion().setFromEuler(new THREE.Euler(0, -at.angle - Math.PI / 2, 0)), new THREE.Vector3(s, s, s * sx));
      out.push(m);
    }
    return out;
  }, [run, f.scale, MW, MH, timber]);
  return (
    <group ref={group}>
      <InstancedGlb url={timber ? "/models/props/bridge-timber.glb" : "/models/props/bridge-arch.glb"} matrices={matrices} />
    </group>
  );
}

/** Barges and skiffs working the river around the pointer. */
function Boats({ city, run, active, onGone }: PartProps) {
  const f = frameOf(city);
  const [MW, MH] = city.map.size;
  const { group } = useRise(active, onGone, 4);
  const boatG = useModel("/models/props/boat.glb");
  const skiffG = useModel("/models/props/skiff.glb");
  const L = pathLength(run.path);
  const RANGE = 220;
  const boats = useMemo(() => {
    const rnd = mulberry32(hash(run.key));
    // two lanes, one each way, each at one speed with even spacing: boats never run into each other
    const half = (run.width ?? 60) / 2;
    const out: { obj: THREE.Object3D; s: number; dir: 1 | -1; lane: number; speed: number; phase: number }[] = [];
    for (const dir of [1, -1] as const) {
      const n = 3;
      const speed = 4.5;
      const off = rnd() * (2 * RANGE / n);
      for (let i = 0; i < n; i++) {
        const type = (i + (dir > 0 ? 0 : 1)) % 3 === 0 ? "skiff" : "boat";
        const obj = bakeify((type === "boat" ? boatG : skiffG).scene.clone(true));
        out.push({ obj, s: run.s0 - RANGE + off + (i * 2 * RANGE) / n, dir, lane: dir * half * (type === "boat" ? 0.42 : 0.3), speed, phase: rnd() * 10 });
      }
    }
    return out;
  }, [run, boatG, skiffG]);
  useFrame(({ clock }, dtRaw) => {
    const dt = Math.min(dtRaw, 0.1);
    const a0 = Math.max(0, run.s0 - RANGE), a1 = Math.min(L, run.s0 + RANGE), span = a1 - a0;
    for (const b of boats) {
      if (!prefersReducedMotion()) b.s += b.dir * b.speed * dt;
      // wrap around the stretch, shrinking away at its ends
      if (b.s > a1) b.s -= span;
      if (b.s < a0) b.s += span;
      const at = pointAlong(run.path, b.s);
      if (!at) continue;
      const nx = -Math.sin(at.angle), ny = Math.cos(at.angle);
      b.obj.position.set((at.x + nx * b.lane - MW / 2) * f.scale, Math.sin(clock.elapsedTime * 1.5 + b.phase) * 0.003, (at.y + ny * b.lane - MH / 2) * f.scale);
      b.obj.rotation.set(0, -(at.angle + (b.dir > 0 ? 0 : Math.PI)) - Math.PI / 2, 0);
      const edge = Math.max(0.001, Math.min(1, Math.min(b.s - a0, a1 - b.s) / 25));
      const sc = f.scale * EXAG * edge;
      b.obj.scale.set(sc, sc, sc);
    }
  });
  return (
    <group ref={group}>
      {boats.map((b, i) => (
        <primitive key={i} object={b.obj} />
      ))}
    </group>
  );
}

/** Trees and goats on the open slopes of a hill (never on top of buildings). */
function Hillside({ city, run, active, onGone }: PartProps) {
  const f = frameOf(city);
  const [MW, MH] = city.map.size;
  const periodId = useStore((s) => s.periodId) ?? city.defaultPeriodId;
  const { group } = useRise(active, onGone);
  const pts = useMemo(() => {
    const fabric = getFabric(city, periodId);
    const rnd = mulberry32(hash(run.key + periodId));
    const out: { x: number; y: number; goat: boolean }[] = [];
    const [cx, cy] = run.center!;
    const R = run.radius! * 0.85;
    for (let i = 0; i < 900 && out.length < 220; i++) {
      const a = rnd() * Math.PI * 2, r = Math.sqrt(rnd()) * R;
      const x = cx + Math.cos(a) * r, y = cy + Math.sin(a) * r * 0.92;
      const goat = rnd() < 0.18;
      // a tree crown is about 5 m across the map at this exaggeration: keep it clear of houses, monuments, roads, water and fields
      const rad = goat ? 1.5 : 5.5;
      if (fabric.occ.rectHits(x, y, 0, rad, rad, OccGrid.ALL)) continue;
      if (out.some((o) => Math.hypot(o.x - x, o.y - y) < rad + (o.goat ? 1.5 : 5.5))) continue;
      out.push({ x, y, goat });
    }
    return out;
  }, [city, periodId, run]);
  const trees = pts.filter((p) => !p.goat), goats = pts.filter((p) => p.goat);
  const geo = useMemo(() => {
    const s = f.scale * 2;
    return {
      trunk: new THREE.CylinderGeometry(0.25 * s, 0.35 * s, 2.4 * s, 6).translate(0, 1.2 * s, 0),
      crown: new THREE.IcosahedronGeometry(2.6 * s, 0).translate(0, 3.8 * s, 0),
      goat: new THREE.BoxGeometry(0.5 * s, 0.6 * s, 0.9 * s).translate(0, 0.6 * s, 0),
    };
  }, [f.scale]);
  const refs = useRef<(THREE.InstancedMesh | null)[]>([]);
  useEffect(() => {
    const d = new THREE.Object3D();
    const place = (m: THREE.InstancedMesh | null, list: { x: number; y: number }[]) => {
      if (!m) return;
      list.forEach((p, i) => {
        d.position.set((p.x - MW / 2) * f.scale, 0, (p.y - MH / 2) * f.scale);
        d.rotation.set(0, (i * 1.7) % 6.28, 0);
        d.scale.setScalar(0.8 + ((i * 37) % 10) / 20);
        d.updateMatrix();
        m.setMatrixAt(i, d.matrix);
      });
      m.instanceMatrix.needsUpdate = true;
      m.computeBoundingSphere();
    };
    place(refs.current[0], trees);
    place(refs.current[1], trees);
    place(refs.current[2], goats);
  }, [trees, goats, f.scale, MW, MH]);
  useEffect(() => () => Object.values(geo).forEach((g) => g.dispose()), [geo]);
  return (
    <group ref={group}>
      <instancedMesh ref={(m) => (refs.current[0] = m)} args={[geo.trunk, shaded("#6a5238"), Math.max(1, trees.length)]} raycast={() => null} />
      <instancedMesh ref={(m) => (refs.current[1] = m)} args={[geo.crown, shaded("#6f8a4a"), Math.max(1, trees.length)]} raycast={() => null} />
      <instancedMesh ref={(m) => (refs.current[2] = m)} args={[geo.goat, shaded("#d9cfbf"), Math.max(1, goats.length)]} raycast={() => null} />
    </group>
  );
}

function nearestS(path: Vec2[], x: number, y: number): number {
  let best = Infinity, bs = 0, acc = 0;
  for (let i = 1; i < path.length; i++) {
    const [ax, ay] = path[i - 1], [bx, by] = path[i];
    const L = Math.hypot(bx - ax, by - ay);
    const d = distToSeg(x, y, { ax, ay, bx, by });
    if (d < best) {
      best = d;
      const t = L ? Math.max(0, Math.min(1, ((x - ax) * (bx - ax) + (y - ay) * (by - ay)) / (L * L))) : 0;
      bs = acc + L * t;
    }
    acc += L;
  }
  return bs;
}

function distPath(path: Vec2[], x: number, y: number): number {
  let best = Infinity;
  for (let i = 1; i < path.length; i++) best = Math.min(best, distToSeg(x, y, { ax: path[i - 1][0], ay: path[i - 1][1], bx: path[i][0], by: path[i][1] }));
  return best;
}
