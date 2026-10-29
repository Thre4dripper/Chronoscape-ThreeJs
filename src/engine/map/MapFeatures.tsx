import { useEffect, useMemo, useRef } from "react";
import * as THREE from "three";
import type { ThreeEvent } from "@react-three/fiber";
import type { City, Vec2 } from "@/content/schema";
import { frameOf, mapToWorld } from "../coords";
import { useStore, type HoveredFeature } from "../store";
import { featurePick } from "./touchLens";

/**
 * Invisible pick geometry over the map so roads, districts, hills, walls and the
 * river answer to the pointer. Hovering lights the feature and shows its name
 * and blurb; the drawing itself stays in the parchment texture.
 */
export function MapFeatures({ city }: { city: City }) {
  const f = frameOf(city);
  const periodId = useStore((s) => s.periodId);
  const hovered = useStore((s) => s.hoveredFeature);
  const hoverFeature = useStore((s) => s.hoverFeature);
  const inPeriod = (periods?: string[]) => !periods || (!!periodId && periods.includes(periodId));

  const items = useMemo(() => {
    const out: { key: string; feature: HoveredFeature; geom: THREE.BufferGeometry; periods?: string[] }[] = [];
    const toW = (p: Vec2) => {
      const [x, , z] = mapToWorld(f, p);
      return [x, z] as [number, number];
    };
    city.map.roads.forEach((r, i) => {
      out.push({ key: `road${i}`, feature: { kind: "road", id: r.id ?? `road${i}`, name: r.name, blurb: r.blurb }, geom: ribbon(r.path.map(toW), Math.max(r.width * 2.2, 22) * f.scale), periods: r.periods });
    });
    city.map.walls.forEach((w, i) => {
      out.push({ key: `wall${i}`, feature: { kind: "wall", id: w.id ?? `wall${i}`, name: w.name, blurb: w.blurb }, geom: ribbon(w.path.map(toW), 30 * f.scale, w.closed), periods: w.periods });
    });
    city.map.water.forEach((w, i) => {
      out.push({ key: `water${i}`, feature: { kind: "water", id: w.id ?? `water${i}`, name: w.name, blurb: w.blurb }, geom: ribbon(w.path.map(toW), w.width * f.scale), periods: w.periods });
    });
    city.map.bridges.forEach((b, i) => {
      // a bridge with its own detailed model is hovered through that landmark instead (in the periods it stands)
      const lm = b.landmarkId ? city.landmarks.find((l) => l.id === b.landmarkId) : undefined;
      const periods = lm ? b.periods?.filter((p) => !lm.activePeriods.includes(p)) : b.periods;
      if (periods && periods.length === 0) return;
      out.push({ key: `bridge${i}`, feature: { kind: "bridge", id: b.id ?? `bridge${i}`, name: b.name, blurb: b.blurb }, geom: ribbon(b.path.map(toW), 34 * f.scale), periods });
    });
    city.map.aqueducts.forEach((a, i) => {
      out.push({ key: `aqueduct${i}`, feature: { kind: "aqueduct", id: `aqueduct${i}`, name: a.name, blurb: "An aqueduct: water carried on arches from springs in the hills, falling gently all the way to the city's fountains and baths." }, geom: ribbon(a.path.map(toW), 24 * f.scale), periods: a.periods });
    });
    city.map.districts.forEach((d) => {
      out.push({ key: `district-${d.id}`, feature: { kind: "district", id: d.id, name: d.name, blurb: d.description }, geom: polygonGeom(d.polygon.map(toW)), periods: d.periods });
    });
    city.map.hills.forEach((h, i) => {
      const [x, z] = toW(h.center);
      const g = new THREE.CircleGeometry(h.radius * f.scale * 0.75, 32);
      g.rotateX(-Math.PI / 2);
      g.translate(x, 0, z);
      out.push({ key: `hill${i}`, feature: { kind: "hill", id: h.id ?? `hill${i}`, name: h.name, blurb: h.blurb }, geom: g, periods: h.periods });
    });
    city.map.gates.forEach((g, i) => {
      const [x, z] = toW(g.position);
      const geo = new THREE.CircleGeometry(26 * f.scale, 12);
      geo.rotateX(-Math.PI / 2);
      geo.translate(x, 0, z);
      out.push({ key: `gate${i}`, feature: { kind: "gate", id: g.id ?? `gate${i}`, name: g.name }, geom: geo, periods: g.periods });
    });
    return out;
  }, [city, f]);

  const over = (feature: HoveredFeature) => (e: ThreeEvent<PointerEvent>) => {
    // landmarks and spots stop propagation themselves, so anything reaching here is a plain map feature
    e.stopPropagation();
    // a finger panning the map is not pointing at anything: on touch the lens chooses the feature
    if (e.pointerType === "touch") return;
    hoverFeature(feature);
  };
  const out = (e: ThreeEvent<PointerEvent>) => {
    if (e.pointerType !== "touch") hoverFeature(null);
  };

  // Draw order: districts first (large), then hills, then water, walls, roads, gates so small things win the hit test.
  const order: Record<HoveredFeature["kind"], number> = { district: 0, hill: 1, water: 2, aqueduct: 3, wall: 4, road: 5, bridge: 6, gate: 7, spot: 8, event: 9 };
  const sorted = [...items].sort((a, b) => order[a.feature.kind] - order[b.feature.kind]);

  const root = useRef<THREE.Group>(null);
  useEffect(() => {
    featurePick.root = root.current;
    return () => void (featurePick.root = null);
  }, []);
  const litItem = hovered ? items.find((it) => it.feature.kind === hovered.kind && it.feature.id === hovered.id) : undefined;
  return (
    <group position-y={0.006} ref={root}>
      {sorted.filter((it) => inPeriod(it.periods)).map((it, i) => (
        // invisible pick geometry: raycast only, never drawn
        <mesh key={it.key} geometry={it.geom} material={PICK_MAT} position-y={i * 0.0004} visible={false} userData={{ feature: it.feature }} onPointerOver={over(it.feature)} onPointerOut={out} />
      ))}
      {litItem && (
        <mesh geometry={litItem.geom} position-y={0.02} raycast={() => null}>
          <meshBasicMaterial color={litItem.feature.kind === "water" ? "#65888A" : "#6F4D34"} transparent opacity={litItem.feature.kind === "district" ? 0.08 : 0.28} depthWrite={false} side={THREE.DoubleSide} />
        </mesh>
      )}
    </group>
  );
}

/** Pick geometry is hit from above whatever the winding of its path. */
const PICK_MAT = new THREE.MeshBasicMaterial({ side: THREE.DoubleSide });

/** Flat ribbon along a polyline, lying on the ground (y = 0). */
function ribbon(pts: [number, number][], width: number, closed = false): THREE.BufferGeometry {
  const p = closed ? [...pts, pts[0]] : pts;
  const verts: number[] = [];
  const idx: number[] = [];
  for (let i = 0; i < p.length; i++) {
    const a = p[Math.max(0, i - 1)],
      b = p[Math.min(p.length - 1, i + 1)];
    const dx = b[0] - a[0],
      dz = b[1] - a[1];
    const L = Math.hypot(dx, dz) || 1;
    const nx = (-dz / L) * (width / 2),
      nz = (dx / L) * (width / 2);
    verts.push(p[i][0] + nx, 0, p[i][1] + nz, p[i][0] - nx, 0, p[i][1] - nz);
    if (i > 0) {
      const k = i * 2;
      idx.push(k - 2, k - 1, k, k - 1, k + 1, k);
    }
  }
  const g = new THREE.BufferGeometry();
  g.setAttribute("position", new THREE.Float32BufferAttribute(verts, 3));
  g.setIndex(idx);
  g.computeVertexNormals();
  return g;
}

function polygonGeom(pts: [number, number][]): THREE.BufferGeometry {
  const shape = new THREE.Shape(pts.map(([x, z]) => new THREE.Vector2(x, -z)));
  const g = new THREE.ShapeGeometry(shape);
  g.rotateX(-Math.PI / 2);
  return g;
}
