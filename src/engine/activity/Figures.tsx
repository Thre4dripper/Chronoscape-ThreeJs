import { useMemo, useRef } from "react";
import { useFrame } from "@react-three/fiber";
import * as THREE from "three";
import type { City, Vec2 } from "@/content/schema";
import { frameOf, mapToWorld } from "../coords";
import { useStore } from "../store";
import { shaded } from "../render/baked";
import { getFabric } from "../map/fabric";
import { OccGrid } from "../map/geom";

/**
 * Tiny wandering figures around the focused place. They prefer to walk along
 * nearby streets, thin out at night, and swell for crowd events. Instanced.
 */
export function Figures({ city, center, radius, count, visualScale = 1 }: { city: City; center: Vec2; radius: number; count: number; visualScale?: number }) {
  const f = frameOf(city);
  const mode = useStore((s) => s.mode);
  const hour = useStore((s) => s.hour);
  const r = radius * f.scale;
  const [cx, , cz] = mapToWorld(f, center);
  const ref = useRef<THREE.InstancedMesh>(null);
  const fade = useRef(0);
  const dummy = useMemo(() => new THREE.Object3D(), []);
  const n = Math.max(1, count);

  // street segments within reach, in world coordinates relative to the centre
  const streets = useMemo(() => {
    const segs: [number, number, number, number][] = [];
    for (const road of city.map.roads) {
      const pts = road.path.map((p) => mapToWorld(f, p));
      for (let i = 1; i < pts.length; i++) {
        const [x0, , z0] = pts[i - 1],
          [x1, , z1] = pts[i];
        const mx = (x0 + x1) / 2 - cx,
          mz = (z0 + z1) / 2 - cz;
        if (Math.hypot(mx, mz) < r * 1.2) segs.push([x0 - cx, z0 - cz, x1 - cx, z1 - cz]);
      }
    }
    return segs;
  }, [city, f, cx, cz, r]);

  // open ground only: never inside houses, monuments or the river, and never walking through them
  const periodId = useStore((s) => s.periodId) ?? city.defaultPeriodId;
  const occ = useMemo(() => getFabric(city, periodId).occ, [city, periodId]);
  const free = (x: number, z: number) => !occ.at(center[0] + x / f.scale, center[1] + z / f.scale, OccGrid.BUILT | OccGrid.WATER);
  const clearPath = (x0: number, z0: number, x1: number, z1: number) => {
    const n = Math.ceil(Math.hypot(x1 - x0, z1 - z0) / (2 * f.scale));
    for (let k = 1; k <= n; k++) if (!free(x0 + ((x1 - x0) * k) / n, z0 + ((z1 - z0) * k) / n)) return false;
    return true;
  };
  const agents = useMemo(
    () =>
      Array.from({ length: n }, (_, i) => {
        let x = 0, z = 0, ok = false;
        for (let k = 0; k < 24 && !ok; k++) {
          const a = (i / n) * Math.PI * 2 + k * 0.7;
          const rr = r * (0.3 + Math.random() * 0.7);
          x = Math.cos(a) * rr;
          z = Math.sin(a) * rr;
          ok = free(x, z);
        }
        return { x, z, tx: x, tz: z, ok, speed: 0.6 + Math.random() * 0.6, phase: Math.random() * 10, t: 0 };
      }),
    // eslint-disable-next-line react-hooks/exhaustive-deps
    [n, r, occ],
  );
  const h = 1.8 * f.scale * Math.min(visualScale, 1.6) * 1.1;

  useFrame((_, dt) => {
    const m = ref.current;
    if (!m) return;
    const daylight = hour >= 7 && hour <= 19 ? 1 : hour >= 5 && hour <= 21 ? 0.55 : 0.15;
    const want = mode === "immersed" || mode === "focused" ? daylight : 0;
    fade.current += (want - fade.current) * (1 - Math.exp(-3 * dt));
    m.visible = fade.current > 0.02;
    if (!m.visible) return;
    const t = performance.now() / 1000;
    const shown = Math.round(n * Math.min(1, fade.current / Math.max(daylight, 0.01)));
    agents.forEach((a, i) => {
      a.t -= dt;
      if (a.t <= 0 && a.ok) {
        // a new destination: along a nearby street or across open ground, reachable in a straight line
        for (let k = 0; k < 8; k++) {
          let tx: number, tz: number;
          if (streets.length > 0 && Math.random() < 0.65) {
            const s = streets[Math.floor(Math.random() * streets.length)];
            const u = Math.random();
            tx = s[0] + (s[2] - s[0]) * u + (Math.random() - 0.5) * 3 * f.scale;
            tz = s[1] + (s[3] - s[1]) * u + (Math.random() - 0.5) * 3 * f.scale;
          } else {
            const ang = Math.random() * Math.PI * 2;
            const rr = r * (0.2 + Math.random() * 0.8);
            tx = Math.cos(ang) * rr;
            tz = Math.sin(ang) * rr;
          }
          if (free(tx, tz) && clearPath(a.x, a.z, tx, tz)) {
            a.tx = tx;
            a.tz = tz;
            break;
          }
        }
        a.t = 3 + Math.random() * 6;
      }
      const dx = a.tx - a.x,
        dz = a.tz - a.z;
      const d = Math.hypot(dx, dz) || 1;
      const step = Math.min(d, a.speed * f.scale * 1.4 * dt * 4);
      a.x += (dx / d) * step;
      a.z += (dz / d) * step;
      const bob = Math.abs(Math.sin(t * 6 + a.phase)) * 0.15 * h;
      const vis = i < shown && a.ok ? Math.min(1, fade.current * 2) : 0;
      dummy.position.set(cx + a.x, h / 2 + bob, cz + a.z);
      dummy.rotation.set(0, -Math.atan2(dz, dx), 0);
      dummy.scale.setScalar(vis);
      dummy.updateMatrix();
      m.setMatrixAt(i, dummy.matrix);
    });
    m.instanceMatrix.needsUpdate = true;
  });

  return (
    <instancedMesh ref={ref} args={[undefined, undefined, n]} material={shaded("#8a8580")}>
      <capsuleGeometry args={[h * 0.22, h * 0.55, 3, 6]} />
    </instancedMesh>
  );
}
