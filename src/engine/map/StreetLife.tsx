import { Suspense, useMemo, useRef, useState } from "react";
import { useFrame } from "@react-three/fiber";
import * as THREE from "three";
import type { City, Vec2 } from "@/content/schema";
import { frameOf } from "../coords";
import { useStore } from "../store";
import { groundPointer } from "./pointer";
import { OccGrid, distToSeg, hash, mulberry32, pathLength, pointAlong } from "./geom";
import { getFabric } from "./fabric";
import { prefersReducedMotion } from "../motion";
import { useModel } from "../render/models";
import { bakedMaterial, miniatureMaterial, shaded } from "../render/baked";

/**
 * Street life on hover: a stretch of the hovered street (or the street in front
 * of a hovered block) fills with people walking both ways, a porter, a pack
 * mule, a handcart, a litter, and market stalls along the kerbs. Blender
 * miniatures, one instanced mesh per kind, a few dozen matrices updated per
 * frame: about ten draw calls in all, gone again when the pointer leaves.
 */
const EXAG = 2.2; // drawn larger than life so they read on the map
const HALF = 110; // metres of street either side of the pointer

type Kind = "walker" | "matron" | "porter" | "mule" | "handcart" | "litter" | "cart" | "stall-fruit" | "stall-pots" | "stall-cloth";
const URL = (k: Kind) => `/models/props/${k}.glb`;

type Stretch = { key: string; path: Vec2[]; s0: number; width: number; town: boolean };
type Mover = { kind: Kind; s: number; dir: 1 | -1; lane: number; speed: number; phase: number };
type Fixed = { kind: Kind; x: number; y: number; rot: number };

export function StreetLife({ city }: { city: City }) {
  const periodId = useStore((s) => s.periodId) ?? city.defaultPeriodId;
  const roads = useMemo(() => city.map.roads.filter((r) => !r.periods || r.periods.includes(periodId)), [city, periodId]);
  const fabric = useMemo(() => getFabric(city, periodId), [city, periodId]);
  const [list, setList] = useState<Stretch[]>([]);
  const current = useRef<string | null>(null);

  const nearest = (x: number, y: number, only?: Vec2[]) => {
    let best = { d: Infinity, s: 0, path: null as Vec2[] | null, width: 8 };
    for (const r of roads) {
      if (only && r.path !== only) continue;
      let acc = 0;
      for (let i = 1; i < r.path.length; i++) {
        const [ax, ay] = r.path[i - 1], [bx, by] = r.path[i];
        const L = Math.hypot(bx - ax, by - ay);
        const d = distToSeg(x, y, { ax, ay, bx, by });
        if (d < best.d) {
          const t = Math.max(0, Math.min(1, ((x - ax) * (bx - ax) + (y - ay) * (by - ay)) / (L * L || 1)));
          best = { d, s: acc + L * t, path: r.path, width: r.width };
        }
        acc += L;
      }
    }
    return best;
  };

  useFrame(() => {
    const st = useStore.getState();
    let want: Stretch | null = null;
    if (st.mode !== "immersed" && groundPointer.valid) {
      if (st.hoveredFeature?.kind === "road") {
        const road = roads.find((r) => (r.id ?? "") === st.hoveredFeature!.id);
        if (road) {
          const n = nearest(groundPointer.mx, groundPointer.my, road.path);
          // re-centre only when the pointer has moved well along the street
          const s0 = Math.round(n.s / 90) * 90;
          want = { key: `road:${road.id}:${s0}`, path: road.path, s0, width: road.width, town: false };
        }
      } else if (st.hoveredBlockId !== null && !st.focusedSpotId) {
        const b = fabric.insulae[st.hoveredBlockId];
        if (b) {
          const n = nearest(b.x, b.y);
          if (n.path && n.d < Math.max(b.w, b.d) * 0.9 + 12) want = { key: `block:${b.id}`, path: n.path, s0: n.s, width: n.width, town: true };
          else {
            // no named road close by: the lane beside the block, centred in the actual gap to the next block
            const c = Math.cos(b.a), sn = Math.sin(b.a);
            const occ = fabric.occ;
            let best: { gap: number; mid: number; nx: number; ny: number; tx: number; ty: number; len: number } | null = null;
            for (const [nu, nv] of [[0, 1], [0, -1], [1, 0], [-1, 0]]) {
              const nx = c * nu - sn * nv, ny = sn * nu + c * nv; // outward normal
              const tx = -ny, ty = nx; // along the side
              const edge = nu !== 0 ? b.w / 2 : b.d / 2;
              const len = nu !== 0 ? b.d : b.w;
              let t0 = -1, t1 = 24;
              for (let t = 0.25; t < 24; t += 0.25) {
                const free = !occ.at(b.x + nx * (edge + t), b.y + ny * (edge + t), OccGrid.BUILT | OccGrid.WATER);
                if (t0 < 0 && free) t0 = t;
                else if (t0 >= 0 && !free) {
                  t1 = t;
                  break;
                }
              }
              if (t0 < 0) continue;
              const gap = t1 - t0;
              if (!best || gap * Math.sqrt(len) > best.gap * Math.sqrt(best.len)) best = { gap, mid: edge + (t0 + t1) / 2, nx, ny, tx, ty, len };
            }
            if (best && best.gap >= 1.2) {
              const half = best.len / 2 + 8;
              const cx = b.x + best.nx * best.mid, cy = b.y + best.ny * best.mid;
              want = { key: `block:${b.id}`, path: [[cx - best.tx * half, cy - best.ty * half], [cx + best.tx * half, cy + best.ty * half]], s0: half, width: best.gap, town: true };
            }
          }
        }
      }
    }
    if (want && !want.town) {
      // a street through town (houses close by) gets stalls and a busier crowd
      const at = pointAlong(want.path, want.s0);
      want.town = !!at && fabric.index.near(at.x, at.y, 30).length > 0;
    }
    const key = want?.key ?? null;
    if (key !== current.current) {
      current.current = key;
      setList((prev) => {
        const rest = prev.filter((p) => p.key !== key);
        return want ? [...rest, want] : rest;
      });
    }
  });

  return (
    <group>
      {list.map((s) => (
        <StretchLife key={s.key} city={city} stretch={s} active={current.current === s.key} onGone={() => setList((p) => p.filter((x) => x.key !== s.key))} />
      ))}
    </group>
  );
}

function StretchLife({ city, stretch, active, onGone }: { city: City; stretch: Stretch; active: boolean; onGone: () => void }) {
  const f = frameOf(city);
  const [MW, MH] = city.map.size;
  const periodId = useStore((s) => s.periodId) ?? city.defaultPeriodId;
  const hour = useStore((s) => s.hour);
  const fabric = getFabric(city, periodId);
  const night = hour < 6 || hour >= 21;
  const ancient = fabric.style === "antique" || fabric.style === "archaic";
  const L = pathLength(stretch.path);
  const a0 = Math.max(0, stretch.s0 - HALF), a1 = Math.min(L, stretch.s0 + HALF);

  const { movers, fixed, exag } = useMemo(() => {
    const rnd = mulberry32(hash(stretch.key + periodId));
    const occ = fabric.occ;
    const BLOCK = OccGrid.BUILT | OccGrid.WATER;
    // how much clear ground there is each side of the street's centre line (houses and water only)
    // a typical value along the stretch (a monument across one end must not empty the whole street;
    // figures that would pass through it are hidden frame by frame instead)
    const probe = (side: 1 | -1) => {
      const ds: number[] = [];
      for (let k = 0; k <= 10; k++) {
        const at = pointAlong(stretch.path, a0 + ((a1 - a0) * k) / 10);
        if (!at) continue;
        const nx = -Math.sin(at.angle) * side, ny = Math.cos(at.angle) * side;
        if (occ.at(at.x, at.y, BLOCK)) continue;
        let d = 0;
        while (d < 30 && !occ.at(at.x + nx * (d + 0.5), at.y + ny * (d + 0.5), BLOCK)) d += 0.5;
        ds.push(d);
      }
      if (!ds.length) return 0;
      ds.sort((a, b) => a - b);
      return ds[Math.floor(ds.length * 0.3)];
    };
    // usable half width each side of the centre line: the drawn street, and clear of houses
    const halfW = stretch.width / 2;
    const room = { 1: Math.min(probe(1), halfW), [-1]: Math.min(probe(-1), halfW) } as Record<1 | -1, number>;
    const narrow = Math.min(room[1], room[-1]);
    // figures are drawn larger than life where the street allows, life size in alleys
    // (a little smaller still where that lets a mule or handcart pass beside a file of walkers)
    const exagPeople = Math.max(1.0, Math.min(EXAG, (narrow - 0.15) / 0.75));
    const exagCarts = (narrow - 0.45) / 2.5;
    const exag = !night && exagCarts >= 1.25 ? Math.min(exagPeople, exagCarts) : exagPeople;
    const ph = 0.35 * exag; // half width of a person on the map
    const single = narrow < ph * 2 + 0.2; // an alley: one file, one way
    // stalls on the kerbs, in town by day, only where a whole stall fits inside the street and off the houses
    const fixed: Fixed[] = [];
    const stallIn: Record<1 | -1, number> = { 1: room[1], [-1]: room[-1] };
    const shx = 1.05 * exag, shy = 1.5 * exag;
    if (stretch.town && !night && !single && narrow >= shx * 2 + ph * 2 + 0.6) {
      const kinds: Kind[] = ["stall-fruit", "stall-pots", "stall-cloth"];
      let k = 0;
      for (let d = a0 + 18; d < a1 - 10 && fixed.length < 6; d += 30 + rnd() * 18) {
        const at = pointAlong(stretch.path, d);
        if (!at) continue;
        const side: 1 | -1 = k % 2 ? 1 : -1;
        k++;
        const nx = -Math.sin(at.angle) * side, ny = Math.cos(at.angle) * side;
        const off = room[side] - shx - 0.1; // stall centre, against the kerb
        const cx = at.x + nx * off, cy = at.y + ny * off;
        if (occ.rectHits(cx, cy, at.angle, shx, shy, BLOCK)) continue;
        if (fixed.some((o) => Math.hypot(o.x - cx, o.y - cy) < shy * 2.4)) continue;
        // the counter faces back across the street
        fixed.push({ kind: kinds[k % 3], x: cx, y: cy, rot: Math.atan2(-nx, -ny) });
        stallIn[side] = Math.min(stallIn[side], off - shx - 0.15);
      }
    }
    // Lanes: each direction keeps to its own side; everyone in a lane walks at the same speed and
    // spacing, so nobody overtakes or passes through anybody. Carts and animals take the outer lane.
    const movers: Mover[] = [];
    const crowd = night ? 0.25 : stretch.town ? 1 : 0.5;
    const people: Kind[] = [];
    for (let i = 0; i < Math.round(10 * crowd); i++) people.push("walker");
    for (let i = 0; i < Math.round(5 * crowd); i++) people.push("matron");
    for (let i = 0; i < Math.round(3 * crowd); i++) people.push("porter");
    const VEH: Partial<Record<Kind, [number, number]>> = { mule: [0.9, 3.2], handcart: [0.8, 3.0], litter: [1.05, 4.6], cart: [1.9, 6.5] }; // half width, length (m)
    const vehicles: Kind[] = night ? [] : ["mule", "handcart", ...(ancient && stretch.town ? (["litter"] as Kind[]) : []), ...(!stretch.town ? (["cart"] as Kind[]) : [])];
    const span = a1 - a0;
    const fill = (lane: { off: number; speed: number; len: number; kinds: Kind[] }, dir: 1 | -1) => {
      const n = lane.kinds.length;
      if (!n) return;
      const slots = Math.min(n, Math.floor(span / (lane.len * 1.8)));
      const start = rnd() * (span / Math.max(1, slots));
      for (let i = 0; i < slots; i++) movers.push({ kind: lane.kinds[i], s: a0 + ((start + (i * span) / slots) % span), dir, lane: dir * lane.off, speed: lane.speed, phase: rnd() * 10 });
    };
    if (single) {
      fill({ off: 0, speed: 2.6, len: 0.8 * exag, kinds: people.slice(0, 6) }, 1);
    } else {
      for (const dir of [1, -1] as const) {
        const limit = stallIn[dir] - 0.1;
        const mine = vehicles.filter((_, i) => i % 2 === (dir > 0 ? 0 : 1)).filter((v) => (VEH[v]![0] * exag) * 2 + ph * 2 + 0.3 <= limit);
        const vh = mine.length ? Math.max(...mine.map((v) => VEH[v]![0])) * exag : 0;
        const vehOff = limit - vh;
        const pedLimit = mine.length ? vehOff - vh - 0.15 : limit;
        const lanes: { off: number; speed: number; len: number; kinds: Kind[] }[] = [];
        for (let off = ph + 0.1; off + ph <= pedLimit && lanes.length < 3; off += ph * 2.3) lanes.push({ off, speed: 2.7, len: 0.8 * exag, kinds: [] });
        if (!lanes.length) continue;
        people.filter((_, i) => i % 2 === (dir > 0 ? 0 : 1)).forEach((kind, i) => lanes[i % lanes.length].kinds.push(kind));
        for (const l of lanes) fill(l, dir);
        if (mine.length) fill({ off: vehOff, speed: 2.1, len: Math.max(...mine.map((v) => VEH[v]![1])) * exag, kinds: mine }, dir);
      }
    }
    return { movers, fixed, exag };
  }, [stretch, periodId, night, ancient, a0, a1, fabric]);

  const group = useRef<THREE.Group>(null);
  const p = useRef(0);
  const gone = useRef(false);
  useFrame((_, dtRaw) => {
    const dt = Math.min(dtRaw, 0.1);
    p.current += ((active ? 1 : 0) - p.current) * (prefersReducedMotion() ? 1 : 1 - Math.exp(-6 * dt));
    if (!active && p.current < 0.01 && !gone.current) {
      gone.current = true;
      onGone();
    }
    if (group.current) group.current.scale.y = Math.max(0.001, 1 - Math.pow(1 - p.current, 3));
  });

  const kinds = useMemo(() => [...new Set<Kind>([...movers.map((m) => m.kind), ...fixed.map((x) => x.kind)])], [movers, fixed]);
  const toWorld = (x: number, y: number) => [(x - MW / 2) * f.scale, (y - MH / 2) * f.scale] as const;
  return (
    <group ref={group}>
      {kinds.map((k) => (
        <Suspense key={k} fallback={null}>
          <Kinds
            url={URL(k)}
            movers={movers.filter((m) => m.kind === k)}
            fixed={fixed.filter((x) => x.kind === k)}
            path={stretch.path}
            range={[a0, a1]}
            scale={f.scale * exag}
            toWorld={toWorld}
            blocked={(x, y) => fabric.occ.at(x, y, OccGrid.BUILT | OccGrid.WATER)}
          />
        </Suspense>
      ))}
    </group>
  );
}

/** One prop kind: an instanced mesh per glTF primitive, matrices rewritten every frame for the movers. */
function Kinds({ url, movers, fixed, path, range, scale, toWorld, blocked }: { url: string; movers: Mover[]; fixed: Fixed[]; path: Vec2[]; range: [number, number]; scale: number; toWorld: (x: number, y: number) => readonly [number, number]; blocked: (x: number, y: number) => boolean }) {
  const gltf = useModel(url);
  const parts = useMemo(() => {
    gltf.scene.updateMatrixWorld(true);
    const out: { geometry: THREE.BufferGeometry; material: THREE.Material; local: THREE.Matrix4 }[] = [];
    gltf.scene.traverse((o) => {
      const m = o as THREE.Mesh;
      if (!m.isMesh) return;
      const g = m.geometry;
      const mat = g.getAttribute("color") ? miniatureMaterial(!g.getAttribute("normal")) : g.getAttribute("normal") ? shaded((m.material as THREE.MeshStandardMaterial).color ?? 0xcccccc) : bakedMaterial({ flat: true, key: "flat" });
      out.push({ geometry: g, material: mat, local: m.matrixWorld.clone() });
    });
    return out;
  }, [gltf]);
  const meshes = useRef<(THREE.InstancedMesh | null)[]>([]);
  const n = movers.length + fixed.length;
  const tmp = useMemo(() => ({ m: new THREE.Matrix4(), q: new THREE.Quaternion(), e: new THREE.Euler(), p: new THREE.Vector3(), s: new THREE.Vector3(), o: new THREE.Matrix4() }), []);
  const span = range[1] - range[0];

  useFrame(({ clock }, dtRaw) => {
    const dt = Math.min(dtRaw, 0.1);
    const t = clock.elapsedTime;
    let i = 0;
    const put = (x: number, y: number, rot: number, k: number, bob: number) => {
      const [wx, wz] = toWorld(x, y);
      tmp.p.set(wx, bob, wz);
      tmp.q.setFromEuler(tmp.e.set(0, rot, 0));
      tmp.s.setScalar(scale * k);
      tmp.o.compose(tmp.p, tmp.q, tmp.s);
      for (let j = 0; j < parts.length; j++) meshes.current[j]?.setMatrixAt(i, tmp.m.multiplyMatrices(tmp.o, parts[j].local));
      i++;
    };
    for (const mv of movers) {
      if (!prefersReducedMotion()) mv.s += mv.dir * mv.speed * dt;
      // wrap around the stretch, fading in and out at its ends
      if (mv.s > range[1]) mv.s -= span;
      if (mv.s < range[0]) mv.s += span;
      const at = pointAlong(path, mv.s);
      if (!at) continue;
      const nx = -Math.sin(at.angle), ny = Math.cos(at.angle);
      const edge = Math.min(mv.s - range[0], range[1] - mv.s);
      const px = at.x + nx * mv.lane, py = at.y + ny * mv.lane;
      // shrink away where the street passes under a building or a monument (never walk through walls)
      const k = blocked(px, py) ? 0.001 : Math.max(0.001, Math.min(1, edge / 14));
      const a = mv.dir > 0 ? at.angle : at.angle + Math.PI;
      const bob = Math.abs(Math.sin(t * mv.speed * 2.2 + mv.phase)) * scale * 0.05;
      put(px, py, Math.atan2(Math.cos(a), Math.sin(a)), k, bob);
    }
    for (const fx of fixed) put(fx.x, fx.y, fx.rot, 1, 0);
    for (const m of meshes.current) {
      if (!m) continue;
      m.count = i;
      m.instanceMatrix.needsUpdate = true;
    }
  });

  if (!n) return null;
  return (
    <>
      {parts.map((p, j) => (
        <instancedMesh key={`${j}:${n}`} ref={(m) => (meshes.current[j] = m)} args={[p.geometry, p.material, n]} frustumCulled={false} raycast={() => null} />
      ))}
    </>
  );
}
