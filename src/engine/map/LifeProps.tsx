import { Suspense, useEffect, useMemo, useRef, useState } from "react";
import { useFrame } from "@react-three/fiber";
import * as THREE from "three";
import type { City, SpotKind, Vec2 } from "@/content/schema";
import { frameOf, mapToWorld } from "../coords";

import { useStore } from "../store";

import { OccGrid, distToSeg } from "./geom";
import { getFabric } from "./fabric";
import { Smoke } from "../effects/Smoke";
import { prefersReducedMotion } from "../motion";
import { bakeify } from "../render/baked";
import { useModel } from "../render/models";
import { propUrl, usePropSet } from "../render/propSets";

/**
 * Small scenes of daily life that rise out of the map on hover: the forge
 * behind a workshop marker, a stall in front of an ordinary block, a wagon on
 * a road, a ploughing team in a field. Simple study models from Blender
 * (assets/models/props), shown a little larger than life so they read.
 */
type PropName = "forge" | "farmer" | "wagon" | "stall" | "bakery" | "cart" | "shepherd" | "crowd";

const EXAGGERATE = 2.2;

const BY_KIND: Partial<Record<SpotKind, PropName>> = {
  workshop: "forge", bakery: "bakery", market: "stall", shop: "stall", bank: "stall", tavern: "stall", inn: "wagon", dock: "cart", works: "cart", garden: "shepherd",
};

type Scene = { key: string; prop: PropName; x: number; y: number; angle: number; exag: number; road?: { path: Vec2[]; s0: number } };

/** Half sizes of each Blender scene in prop metres: across (x) and along (y) the way it faces, motion included. */
const EXTENT: Record<PropName, [number, number]> = {
  forge: [3.8, 5.3], farmer: [3.1, 11.5], wagon: [1.9, 5.1], stall: [1.8, 1.8], bakery: [3.5, 4.1], cart: [3.2, 4.2], shepherd: [6.4, 3.3], crowd: [3.4, 2.8],
};

export function LifeProps({ city }: { city: City }) {
  const periodId = useStore((s) => s.periodId) ?? city.defaultPeriodId;

  const roads = useMemo(() => city.map.roads.filter((r) => !r.periods || r.periods.includes(periodId)), [city, periodId]);
  const fabric = useMemo(() => getFabric(city, periodId), [city, periodId]);
  useEffect(() => placed.current.clear(), [fabric]);
  const [scenes, setScenes] = useState<Scene[]>([]);
  const active = useRef(new Set<string>());

  // nearest point on any road: used to put scenes on the street, facing along it
  const nearestRoad = (x: number, y: number) => {
    let best = { d: Infinity, px: x, py: y, angle: 0, path: null as Vec2[] | null, s: 0 };
    for (const r of roads) {
      let acc = 0;
      for (let i = 1; i < r.path.length; i++) {
        const [ax, ay] = r.path[i - 1], [bx, by] = r.path[i];
        const seg = { ax, ay, bx, by };
        const d = distToSeg(x, y, seg);
        const L = Math.hypot(bx - ax, by - ay);
        if (d < best.d) {
          const t = Math.max(0, Math.min(1, ((x - ax) * (bx - ax) + (y - ay) * (by - ay)) / (L * L || 1)));
          best = { d, px: ax + (bx - ax) * t, py: ay + (by - ay) * t, angle: Math.atan2(by - ay, bx - ax), path: r.path, s: acc + L * t };
        }
        acc += L;
      }
    }
    return best;
  };

  // Find open ground near a spot for its scene: never on houses, monuments or water. The nearest
  // street is preferred; big scenes shrink a little when only a small square is free.
  const placed = useRef(new Map<string, Omit<Scene, "key" | "prop"> | null>());
  const placeScene = (x: number, y: number, prop: PropName) => {
    const key = `${x}:${y}:${prop}`;
    if (placed.current.has(key)) return placed.current.get(key)!;
    const BLOCK = OccGrid.BUILT | OccGrid.WATER;
    const r = nearestRoad(x, y);
    const [ex, ey] = EXTENT[prop];
    let out: Omit<Scene, "key" | "prop"> | null = null;
    for (const exag of [EXAGGERATE, 1.7, 1.3]) {
      const hx = ex * exag, hy = ey * exag;
      const tryAt = (cx: number, cy: number, angle: number) => !fabric.occ.rectHits(cx, cy, angle, hx, hy, BLOCK) && !landmarkHit(cx, cy, Math.hypot(hx, hy));
      if (r.d < 80 && tryAt(r.px, r.py, r.angle)) out = { x: r.px, y: r.py, angle: r.angle, exag };
      for (let rad = 4; !out && rad <= 90; rad += 4)
        for (let k = 0; k < 24 && !out; k++) {
          const a = (k / 24) * Math.PI * 2;
          const cx = x + Math.cos(a) * rad, cy = y + Math.sin(a) * rad;
          if (tryAt(cx, cy, r.angle)) out = { x: cx, y: cy, angle: r.angle, exag };
        }
      if (out) break;
    }
    placed.current.set(key, out);
    return out;
  };
  const landmarkHit = (x: number, y: number, rad: number) =>
    city.landmarks.some((l) => l.activePeriods.includes(periodId) && Math.hypot(l.position[0] - x, l.position[1] - y) < (Math.max(l.footprint[0], l.footprint[1]) * l.scale) / 2 + rad);

  useFrame(() => {
    const st = useStore.getState();
    const want: Scene[] = [];

    // 1. a shop / workshop marker hovered or being visited
    const spotId = st.focusedSpotId ?? (st.hoveredFeature?.kind === "spot" ? st.hoveredFeature.id : null);
    if (spotId) {
      const sp = city.spots.find((s) => s.id === spotId);
      const prop = sp && (BY_KIND[sp.kind] ?? "crowd");
      if (sp && prop) {
        const at = placeScene(sp.position[0], sp.position[1], prop);
        if (at) want.push({ key: `spot:${sp.id}`, prop, ...at });
      }
    }
    // ordinary blocks and streets: see StreetLife (people, carts and stalls moving along the street)
    const keys = new Set(want.map((w) => w.key));
    let changed = keys.size !== active.current.size;
    if (!changed) for (const k of keys) if (!active.current.has(k)) changed = true;
    if (changed) {
      active.current = keys;
      setScenes((prev) => {
        const keep = prev.filter((p) => !keys.has(p.key));
        return [...keep.map((p) => ({ ...p, leaving: true }) as Scene & { leaving?: boolean }), ...want];
      });
    }
  });

  return (
    <group>
      {scenes.map((s) => (
        <Suspense key={s.key} fallback={null}>
          <PropScene city={city} scene={s} active={active.current.has(s.key)} onGone={() => setScenes((prev) => prev.filter((p) => p.key !== s.key))} />
        </Suspense>
      ))}
    </group>
  );
}

function PropScene({ city, scene, active, onGone }: { city: City; scene: Scene; active: boolean; onGone: () => void }) {
  const f = frameOf(city);
  const gltf = useModel(propUrl(usePropSet(city), scene.prop));
  const root = useMemo(() => {
    const r = bakeify(gltf.scene.clone(true));
    return r;
  }, [gltf]);
  const parts = useMemo(
    () => ({
      hammer: root.getObjectByName("anim_hammer"),
      spin: root.getObjectByName("anim_spin"),
      walk: root.getObjectByName("anim_walk"),
      graze: root.getObjectByName("anim_graze"),
      smoke: root.getObjectByName("marker_smoke"),
    }),
    [root],
  );
  const base = useMemo(() => ({ walkZ: parts.walk?.position.z ?? 0, grazeX: parts.graze?.position.x ?? 0 }), [parts]);
  const group = useRef<THREE.Group>(null);
  const progress = useRef(0);
  const goneSent = useRef(false);
  const travel = useRef(0);
  const s = f.scale * scene.exag;
  const [smokePos, setSmokePos] = useState<[number, number, number] | null>(null);

  useEffect(() => {
    if (!parts.smoke) return;
    root.updateMatrixWorld(true);
    const v = new THREE.Vector3();
    parts.smoke.getWorldPosition(v);
    setSmokePos([v.x, v.y, v.z]);
  }, [parts, root]);

  useFrame((state, dtRaw) => {
    const dt = Math.min(dtRaw, 0.1);
    const t = state.clock.elapsedTime;
    const target = active ? 1 : 0;
    progress.current += (target - progress.current) * (prefersReducedMotion() ? 1 : 1 - Math.exp(-7 * dt));
    if (!active && progress.current < 0.01 && !goneSent.current) {
      goneSent.current = true;
      onGone();
    }
    const g = group.current;
    if (!g) return;
    const p = Math.max(0.0001, 1 - Math.pow(1 - progress.current, 3));
    g.scale.set(s, s * p, s);
    // placement: fixed, or travelling along the road
    let x = scene.x, y = scene.y, angle = scene.angle;
    if (scene.road) {
      travel.current += dt * 9; // metres per second, a little brisk for legibility
      const L = pathLen(scene.road.path);
      const span = 160;
      const u = ((travel.current % (2 * span)) + 2 * span) % (2 * span);
      const along = Math.min(L, Math.max(0, scene.road.s0 - span / 2 + (u < span ? u : 2 * span - u)));
      const at = pointOn(scene.road.path, along);
      if (at) {
        x = at.x;
        y = at.y;
        angle = at.angle + (u < span ? 0 : Math.PI);
      }
    }
    const [wx, , wz] = mapToWorld(f, [x, y]);
    g.position.set(wx, 0, wz);
    // props face -Y in Blender (= +Z in three); turn them to face along the street
    g.rotation.set(0, -angle - Math.PI / 2, 0);
    if (parts.hammer) parts.hammer.rotation.x = -0.2 - Math.max(0, Math.sin(t * 7)) * 1.4;
    if (parts.spin) parts.spin.rotation.y = t * 0.7;
    if (parts.walk) parts.walk.position.z = base.walkZ + Math.sin(t * 0.25) * 6;
    if (parts.graze) parts.graze.position.x = base.grazeX + Math.sin(t * 0.15) * 1.2;
  });

  return (
    <group ref={group}>
      <primitive object={root} />
      {smokePos && active && <Smoke position={smokePos} size={1.6} />}
    </group>
  );
}

function pathLen(p: Vec2[]) {
  let L = 0;
  for (let i = 1; i < p.length; i++) L += Math.hypot(p[i][0] - p[i - 1][0], p[i][1] - p[i - 1][1]);
  return L;
}

function pointOn(p: Vec2[], d: number) {
  let acc = 0;
  for (let i = 1; i < p.length; i++) {
    const L = Math.hypot(p[i][0] - p[i - 1][0], p[i][1] - p[i - 1][1]);
    if (acc + L >= d) {
      const t = L ? (d - acc) / L : 0;
      return { x: p[i - 1][0] + (p[i][0] - p[i - 1][0]) * t, y: p[i - 1][1] + (p[i][1] - p[i - 1][1]) * t, angle: Math.atan2(p[i][1] - p[i - 1][1], p[i][0] - p[i - 1][0]) };
    }
    acc += L;
  }
  return null;
}
