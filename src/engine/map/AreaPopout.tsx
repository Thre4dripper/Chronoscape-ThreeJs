import { Suspense, useEffect, useMemo, useRef, useState } from "react";
import { useFrame } from "@react-three/fiber";
import * as THREE from "three";
import type { City, Vec2 } from "@/content/schema";
import { frameOf } from "../coords";
import { getFabric } from "./fabric";
import { useStore } from "../store";
import { groundPointer } from "./pointer";
import { hash, pointInPolygon } from "./geom";
import { distToEdges, polygonArea, rectInPolygon, rowsInPolygon, scatterInPolygon } from "./scatter";
import { prefersReducedMotion } from "../motion";
import { bakedMaterial, bakeify, shaded } from "../render/baked";
import { useModel } from "../render/models";

/**
 * Hover open land and the whole parcel rises out of the paper along its exact
 * boundary: a field with its plough teams, a pasture with its flocks, a
 * vineyard with its rows, an orchard or park with its trees, a marsh with its
 * reeds. One parcel at a time, a few draw calls each.
 */
type AreaKind = "furrow" | "pasture" | "vineyard" | "orchard" | "park" | "marsh";
type Area = { key: string; kind: AreaKind; pts: Vec2[]; angle: number; name?: string };

const SLAB_M = 1.4; // slab thickness in metres
/** Half sizes of each Blender scene in prop metres: across (hx) and along its walking line (hy), motion included. */
const PROP_EXTENT: Record<string, { hx: number; hy: number }> = {
  farmer: { hx: 3.4, hy: 11.5 }, // furrows 18 m long; the plough team walks 6 m either way
  shepherd: { hx: 6.6, hy: 3.6 }, // the flock grazes 1.5 m sideways
  cart: { hx: 3.3, hy: 4.3 },
};
/** Crown or body radius of instanced plants and animals, in map metres. */
const PLANT_RADIUS = { vine: 1, tree: 5, reed: 0.6, sheep: 1.2 } as const;
const EXAG = 2.2; // props and plants read a little larger than life


export function AreaPopout({ city }: { city: City }) {
  const periodId = useStore((s) => s.periodId) ?? city.defaultPeriodId;
  const fabric = useMemo(() => getFabric(city, periodId), [city, periodId]);
  const gardens = useMemo(() => city.map.gardens.filter((g) => !g.periods || g.periods.includes(periodId)), [city, periodId]);
  const marsh = useMemo(() => city.map.marsh.filter((g) => !g.periods || g.periods.includes(periodId)), [city, periodId]);
  const [areas, setAreas] = useState<Area[]>([]);
  const current = useRef<string | null>(null);

  useFrame(() => {
    const st = useStore.getState();
    let found: Area | null = null;
    const busy = st.hoveredBlockId !== null || st.hoveredId !== null || (st.hoveredFeature && st.hoveredFeature.kind !== "district" && st.hoveredFeature.kind !== "hill");
    if (groundPointer.valid && !busy && st.mode !== "immersed") {
      const { mx, my } = groundPointer;
      for (let i = 0; i < fabric.fields.length && !found; i++) {
        const fl = fabric.fields[i];
        if (Math.abs(fl.cx - mx) > 160 || Math.abs(fl.cy - my) > 160) continue;
        if (pointInPolygon(mx, my, fl.pts)) found = { key: `field:${periodId}:${i}`, kind: fl.kind, pts: fl.pts, angle: fl.angle };
      }
      for (let i = 0; i < gardens.length && !found; i++) {
        const g = gardens[i];
        if (pointInPolygon(mx, my, g.polygon)) found = { key: `garden:${periodId}:${i}`, kind: g.kind === "vineyard" ? "vineyard" : g.kind === "orchard" ? "orchard" : "park", pts: g.polygon, angle: 0, name: g.name };
      }
      for (let i = 0; i < marsh.length && !found; i++) {
        const g = marsh[i];
        if (pointInPolygon(mx, my, g.polygon)) found = { key: `marsh:${periodId}:${i}`, kind: "marsh", pts: g.polygon, angle: 0, name: g.name };
      }
    }
    st.setHoveredArea(found ? { kind: found.kind, name: found.name } : null);
    const key = found ? found.key : null;
    if (key !== current.current) {
      current.current = key;
      setAreas((prev) => {
        const rest = prev.filter((a) => a.key !== key);
        return found ? [...rest, found] : rest;
      });
    }
  });

  return (
    <group>
      {areas.map((a) => (
        <Parcel key={a.key} city={city} area={a} active={current.current === a.key} onGone={() => setAreas((prev) => prev.filter((p) => p.key !== a.key))} />
      ))}
    </group>
  );
}

function Parcel({ city, area, active, onGone }: { city: City; area: Area; active: boolean; onGone: () => void }) {
  const f = frameOf(city);
  const [MW, MH] = city.map.size;
  const toW = (p: Vec2): [number, number] => [(p[0] - MW / 2) * f.scale, (p[1] - MH / 2) * f.scale];
  const depth = SLAB_M * EXAG * f.scale;
  const group = useRef<THREE.Group>(null);
  const progress = useRef(0);
  const gone = useRef(false);

  /* ---- slab with exact boundary ---- */
  const { geom, outline, mats } = useMemo(() => {
    const shape = new THREE.Shape(area.pts.map((p) => {
      const [x, z] = toW(p);
      return new THREE.Vector2(x, -z);
    }));
    const g = new THREE.ExtrudeGeometry(shape, { depth, bevelEnabled: false });
    g.rotateX(-Math.PI / 2);
    const pts = area.pts.map((p) => {
      const [x, z] = toW(p);
      return new THREE.Vector3(x, depth * 1.002, z);
    });
    pts.push(pts[0].clone());
    const o = new THREE.Line(new THREE.BufferGeometry().setFromPoints(pts), new THREE.LineBasicMaterial({ color: "#3e2a1c" }));
    o.raycast = () => {};
    const tex = parcelTexture(area.kind);
    tex.wrapS = tex.wrapT = THREE.RepeatWrapping;
    const tileWorld = 24 * f.scale; // one texture tile = 24 m
    tex.repeat.set(1 / tileWorld, 1 / tileWorld);
    tex.rotation = -area.angle;
    tex.colorSpace = THREE.SRGBColorSpace;
    const top = bakedMaterial({ map: tex, key: "tex" });
    const side = bakedMaterial({ color: area.kind === "marsh" ? "#6f7d6a" : "#8a7150" });
    return { geom: g, outline: o, mats: [top, side] };
    // eslint-disable-next-line react-hooks/exhaustive-deps
  }, [area.key]);
  useEffect(
    () => () => {
      geom.dispose();
      outline.geometry.dispose();
      (outline.material as THREE.Material).dispose();
      mats.forEach((m) => {
        (m as THREE.MeshBasicMaterial).map?.dispose();
        m.dispose();
      });
    },
    [geom, outline, mats],
  );

  /* ---- what lives on it ---- */
  const area_m2 = polygonArea(area.pts);
  const seed = hash(area.key);
  const plants = useMemo(() => {
    // widen the spacing on big parcels so the whole parcel is covered within the instance budget
    const fit = (cellArea: number, cap: number) => Math.max(1, Math.sqrt(area_m2 / (cellArea * cap)));
    switch (area.kind) {
      case "vineyard": {
        const k = fit(3.2 * 2.6, 2400);
        return { kind: "vine" as const, pts: rowsInPolygon(area.pts, area.angle, 3.2 * k, 2.6 * k, 2600) };
      }
      case "orchard": {
        const k = fit(81, 900);
        return { kind: "tree" as const, pts: rowsInPolygon(area.pts, area.angle, 9 * k, 9 * k, 1000) };
      }
      case "park": {
        const k = fit(121, 900);
        return { kind: "tree" as const, pts: scatterInPolygon(area.pts, 11 * k, seed, 0.45, 1000) };
      }
      case "marsh": {
        const k = fit(10, 2400);
        return { kind: "reed" as const, pts: scatterInPolygon(area.pts, 3.2 * k, seed, 0.5, 2600) };
      }
      case "pasture": {
        const k = fit(81 * 3, 140);
        return { kind: "sheep" as const, pts: scatterInPolygon(area.pts, 9 * k, seed, 0.5, 1200).filter((_, i) => (seed + i * 7) % 3 === 0) };
      }
      default:
        return null;
    }
  }, [area, seed, area_m2]);
  const actors = useMemo(() => {
    const prop = area.kind === "furrow" ? "farmer" : area.kind === "pasture" ? "shepherd" : area.kind === "vineyard" || area.kind === "orchard" ? "cart" : null;
    if (!prop) return [];
    // each scene's footprint on the ground (prop metres x exaggeration), including how far it walks or grazes
    const ext = PROP_EXTENT[prop];
    const hx = ext.hx * EXAG + 1.5, hy = ext.hy * EXAG + 1.5;
    const n = Math.max(1, Math.min(4, Math.round(area_m2 / 9000)));
    const cand = scatterInPolygon(area.pts, Math.max(6, Math.min(hx, hy) * 0.6), seed + 1, 0.3, 1200);
    const out: { p: Vec2; prop: string; rot: number; hx: number; hy: number }[] = [];
    for (let i = 0; i < cand.length && out.length < n; i++) {
      const p = cand[(i * 7919) % cand.length];
      const rot = area.angle + (out.length % 2 ? Math.PI : 0);
      if (!rectInPolygon(area.pts, p[0], p[1], rot, hx, hy)) continue;
      // never on top of another scene
      if (out.some((o) => Math.hypot(o.p[0] - p[0], o.p[1] - p[1]) < Math.hypot(hx, hy) * 2)) continue;
      out.push({ p, prop, rot, hx, hy });
    }
    return out;
  }, [area, area_m2, seed]);
  // plants stay inside the boundary by their own radius, and off the scenes
  const plantsInside = useMemo(() => {
    if (!plants) return null;
    const r = PLANT_RADIUS[plants.kind];
    const pts = plants.pts.filter(([x, y]) => {
      if (distToEdges(x, y, area.pts) < r) return false;
      for (const a of actors) {
        const dx = x - a.p[0], dy = y - a.p[1];
        const c = Math.cos(a.rot), sn = Math.sin(a.rot);
        if (Math.abs(dx * c + dy * sn) < a.hy + r && Math.abs(-dx * sn + dy * c) < a.hx + r) return false;
      }
      return true;
    });
    return { kind: plants.kind, pts };
  }, [plants, actors, area.pts]);

  useFrame((_, dtRaw) => {
    const dt = Math.min(dtRaw, 0.1);
    progress.current += ((active ? 1 : 0) - progress.current) * (prefersReducedMotion() ? 1 : 1 - Math.exp(-6 * dt));
    if (!active && progress.current < 0.01 && !gone.current) {
      gone.current = true;
      onGone();
    }
    const g = group.current;
    if (g) g.scale.y = Math.max(0.001, 1 - Math.pow(1 - progress.current, 3));
  });

  return (
    <group ref={group}>
      <mesh geometry={geom} material={mats} raycast={() => null} />
      <primitive object={outline} />
      {plantsInside && plantsInside.pts.length > 0 && <Plants kind={plantsInside.kind} pts={plantsInside.pts} toW={toW} y={depth} scale={f.scale} angle={area.angle} />}
      <Suspense fallback={null}>
        {actors.map((a, i) => (
          <Actor key={i} prop={a.prop} pos={toW(a.p)} y={depth} rot={a.rot} s={f.scale * EXAG} />
        ))}
      </Suspense>
    </group>
  );
}

function Actor({ prop, pos, y, rot, s }: { prop: string; pos: [number, number]; y: number; rot: number; s: number }) {
  const gltf = useModel(`/models/props/${prop}.glb`);
  const root = useMemo(() => {
    return bakeify(gltf.scene.clone(true));
  }, [gltf]);
  const walk = useMemo(() => root.getObjectByName("anim_walk"), [root]);
  const graze = useMemo(() => root.getObjectByName("anim_graze"), [root]);
  const base = useMemo(() => ({ wz: walk?.position.z ?? 0, gx: graze?.position.x ?? 0 }), [walk, graze]);
  const phase = useMemo(() => Math.random() * 10, []);
  useFrame(({ clock }) => {
    const t = clock.elapsedTime + phase;
    if (walk) walk.position.z = base.wz + Math.sin(t * 0.25) * 6;
    if (graze) graze.position.x = base.gx + Math.sin(t * 0.15) * 1.5;
  });
  return <primitive object={root} position={[pos[0], y, pos[1]]} rotation={[0, -rot - Math.PI / 2, 0]} scale={[s, s, s]} />;
}

/** Instanced vegetation / animals sitting on top of the slab. */
function Plants({ kind, pts, toW, y, scale, angle }: { kind: "vine" | "tree" | "reed" | "sheep"; pts: Vec2[]; toW: (p: Vec2) => [number, number]; y: number; scale: number; angle: number }) {
  const parts = useMemo(() => {
    const s = scale * 2; // plants drawn at twice life size so they read
    if (kind === "vine") return [{ g: new THREE.CylinderGeometry(0.35 * s, 0.45 * s, 1.6 * s, 6).translate(0, 0.8 * s, 0), c: "#6f8a4a" }];
    if (kind === "reed") return [{ g: new THREE.ConeGeometry(0.25 * s, 2.2 * s, 4).translate(0, 1.1 * s, 0), c: "#8a9a62" }];
    if (kind === "sheep") return [{ g: new THREE.BoxGeometry(0.6 * s, 0.55 * s, 1.0 * s).translate(0, 0.55 * s, 0), c: "#efe8da" }, { g: new THREE.BoxGeometry(0.3 * s, 0.3 * s, 0.3 * s).translate(0, 0.75 * s, 0.6 * s), c: "#4a4038" }];
    return [
      { g: new THREE.CylinderGeometry(0.25 * s, 0.35 * s, 2.4 * s, 6).translate(0, 1.2 * s, 0), c: "#6a5238" },
      { g: new THREE.IcosahedronGeometry(2.4 * s, 0).translate(0, 3.6 * s, 0), c: "#6f8a4a" },
    ];
  }, [kind, scale]);
  const refs = useRef<(THREE.InstancedMesh | null)[]>([]);
  useEffect(() => {
    const d = new THREE.Object3D();
    const rnd = (i: number) => ((Math.sin(i * 12.9898) * 43758.5453) % 1 + 1) % 1;
    refs.current.forEach((m) => {
      if (!m) return;
      pts.forEach((p, i) => {
        const [x, z] = toW(p);
        const k = 0.8 + rnd(i) * 0.45;
        d.position.set(x, y, z);
        d.rotation.set(0, kind === "sheep" ? rnd(i + 3) * Math.PI * 2 : -angle + rnd(i) * 0.6, 0);
        d.scale.setScalar(k);
        d.updateMatrix();
        m.setMatrixAt(i, d.matrix);
      });
      m.instanceMatrix.needsUpdate = true;
      m.computeBoundingSphere();
    });
  }, [pts, toW, y, angle, kind]);
  useEffect(() => () => parts.forEach((p) => p.g.dispose()), [parts]);
  return (
    <>
      {parts.map((p, i) => (
        <instancedMesh key={i} ref={(m) => (refs.current[i] = m)} args={[p.g, shaded(p.c), pts.length]} raycast={() => null} />
      ))}
    </>
  );
}

/** A small tileable texture for the top of each kind of parcel. */
function parcelTexture(kind: AreaKind): THREE.CanvasTexture {
  const S = 128;
  const c = document.createElement("canvas");
  c.width = c.height = S;
  const g = c.getContext("2d")!;
  const base: Record<AreaKind, string> = { furrow: "#b39566", pasture: "#a9ad74", vineyard: "#a69a6a", orchard: "#9fa572", park: "#93a46e", marsh: "#8fa08e" };
  g.fillStyle = base[kind];
  g.fillRect(0, 0, S, S);
  if (kind === "furrow") {
    for (let i = 0; i < 8; i++) {
      g.fillStyle = "rgba(70,48,28,0.35)";
      g.fillRect(0, i * 16 + 2, S, 5);
      g.fillStyle = "rgba(255,240,200,0.2)";
      g.fillRect(0, i * 16 + 9, S, 3);
    }
  } else {
    for (let i = 0; i < 260; i++) {
      g.fillStyle = i % 2 ? "rgba(60,70,30,0.22)" : "rgba(255,250,220,0.18)";
      g.fillRect((i * 37) % S, (i * 91) % S, 2, 2);
    }
    if (kind === "marsh")
      for (let i = 0; i < 6; i++) {
        g.fillStyle = "rgba(90,130,140,0.4)";
        g.beginPath();
        g.ellipse((i * 47) % S, (i * 29) % S, 14, 6, 0, 0, Math.PI * 2);
        g.fill();
      }
  }
  return new THREE.CanvasTexture(c);
}
