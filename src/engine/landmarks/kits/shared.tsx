import { createContext, useContext, useMemo, useRef, type MutableRefObject, type ReactNode } from "react";
import { useFrame } from "@react-three/fiber";
import * as THREE from "three";
import { easeOutCubic, stageProgress } from "../../motion";
import { shaded } from "../../render/baked";

/* ---------- reveal plumbing ---------- */

export type RevealCtx = { progress: MutableRefObject<number>; mode: "rise" | "assemble" };
export const RevealContext = createContext<RevealCtx>({ progress: { current: 1 }, mode: "rise" });

/** Height fraction a landmark keeps while idle: an embossed footprint on the paper. */
export const PROXY_FLOOR = 0;

/**
 * One stage of a staggered reveal. Stage 0 is the base and never fully disappears;
 * later stages pop in as the overall progress advances.
 */
export function Stage({ index, count, children, position }: { index: number; count: number; children: ReactNode; position?: [number, number, number] }) {
  const ref = useRef<THREE.Group>(null);
  const { progress, mode } = useContext(RevealContext);
  useFrame(() => {
    const g = ref.current;
    if (!g) return;
    const p = mode === "assemble" ? stageProgress(progress.current, index, count) : progress.current;
    const floor = index === 0 ? PROXY_FLOOR : 0;
    const s = floor + (1 - floor) * easeOutCubic(p);
    g.scale.y = Math.max(s, 0.0001);
    g.visible = s > 0.001;
  });
  return (
    <group ref={ref} position={position}>
      {children}
    </group>
  );
}

/* ---------- materials ---------- */

const matCache = new Map<string, THREE.Material>();
export function mat(color: string, opts: { roughness?: number; emissive?: string } = {}): THREE.Material {
  const key = `${color}|${opts.roughness ?? 0.9}|${opts.emissive ?? ""}`;
  let m = matCache.get(key);
  if (!m) {
    m = shaded(color);
    matCache.set(key, m);
  }
  return m;
}

/** Slightly lighter / darker variants to break up flat clay surfaces. */
export function shade(hex: string, amount: number): string {
  const c = new THREE.Color(hex);
  const hsl = { h: 0, s: 0, l: 0 };
  c.getHSL(hsl);
  c.setHSL(hsl.h, hsl.s, Math.min(1, Math.max(0, hsl.l + amount)));
  return `#${c.getHexString()}`;
}

/* ---------- primitives (metres, origin at ground centre, +y up) ---------- */

export function Box({ w, h, d, x = 0, y = 0, z = 0, color, rotY = 0 }: { w: number; h: number; d: number; x?: number; y?: number; z?: number; color: string; rotY?: number }) {
  return (
    <mesh position={[x, y + h / 2, z]} rotation-y={rotY} material={mat(color)}>
      <boxGeometry args={[w, h, d]} />
    </mesh>
  );
}

export function Cyl({ r, h, x = 0, y = 0, z = 0, color, rTop, seg = 14 }: { r: number; h: number; x?: number; y?: number; z?: number; color: string; rTop?: number; seg?: number }) {
  return (
    <mesh position={[x, y + h / 2, z]} material={mat(color)}>
      <cylinderGeometry args={[rTop ?? r, r, h, seg]} />
    </mesh>
  );
}

export function Dome({ r, x = 0, y = 0, z = 0, color, squash = 1 }: { r: number; x?: number; y?: number; z?: number; color: string; squash?: number }) {
  return (
    <mesh position={[x, y, z]} scale={[1, squash, 1]} material={mat(color)}>
      <sphereGeometry args={[r, 20, 12, 0, Math.PI * 2, 0, Math.PI / 2]} />
    </mesh>
  );
}

/** Gabled roof: a triangular prism spanning `w` (ridge runs along z through depth `d`). */
export function GableRoof({ w, d, h, x = 0, y = 0, z = 0, color, overhang = 0.6 }: { w: number; d: number; h: number; x?: number; y?: number; z?: number; color: string; overhang?: number }) {
  const geom = useMemo(() => {
    const W = w + overhang * 2;
    const shape = new THREE.Shape();
    shape.moveTo(-W / 2, 0);
    shape.lineTo(W / 2, 0);
    shape.lineTo(0, h);
    shape.closePath();
    const g = new THREE.ExtrudeGeometry(shape, { depth: d + overhang * 2, bevelEnabled: false });
    g.translate(0, 0, -(d + overhang * 2) / 2);
    return g;
  }, [w, d, h, overhang]);
  return <mesh geometry={geom} position={[x, y, z]} material={mat(color)} />;
}

/** Instanced columns with a square capital. */
export function Columns({ positions, r, h, color }: { positions: [number, number][]; r: number; h: number; color: string }) {
  const shaft = useRef<THREE.InstancedMesh>(null);
  const cap = useRef<THREE.InstancedMesh>(null);
  useMemo(() => {
    void positions;
  }, [positions]);
  const dummy = useMemo(() => new THREE.Object3D(), []);
  const setup = (m: THREE.InstancedMesh | null, yOff: number) => {
    if (!m) return;
    positions.forEach(([x, z], i) => {
      dummy.position.set(x, yOff, z);
      dummy.updateMatrix();
      m.setMatrixAt(i, dummy.matrix);
    });
    m.instanceMatrix.needsUpdate = true;
  };
  return (
    <>
      <instancedMesh
        ref={(m) => {
          shaft.current = m;
          setup(m, h / 2);
        }}
        args={[undefined, undefined, positions.length]}
        material={mat(color)}
      >
        <cylinderGeometry args={[r * 0.9, r, h, 10]} />
      </instancedMesh>
      <instancedMesh
        ref={(m) => {
          cap.current = m;
          setup(m, h + r * 0.4);
        }}
        args={[undefined, undefined, positions.length]}
        material={mat(shade(color, 0.05))}
      >
        <boxGeometry args={[r * 2.6, r * 0.8, r * 2.6]} />
      </instancedMesh>
    </>
  );
}

/** Column grid around a rectangle: `front` along x at ±z edges, `side` along z. */
export function peristyle(w: number, d: number, front: number, side: number, inset = 0): [number, number][] {
  const out: [number, number][] = [];
  const x0 = -w / 2 + inset,
    x1 = w / 2 - inset,
    z0 = -d / 2 + inset,
    z1 = d / 2 - inset;
  for (let i = 0; i < front; i++) {
    const x = front === 1 ? 0 : x0 + ((x1 - x0) * i) / (front - 1);
    out.push([x, z1]);
    if (side > 0) out.push([x, z0]);
  }
  if (side > 2) {
    for (let j = 1; j < side - 1; j++) {
      const z = z0 + ((z1 - z0) * j) / (side - 1);
      out.push([x0, z]);
      out.push([x1, z]);
    }
  }
  return out;
}

/** Ring of points around an ellipse (optionally a partial arc, in radians). */
export function ellipseRing(rx: number, rz: number, n: number, arc = Math.PI * 2, start = 0): [number, number][] {
  const out: [number, number][] = [];
  for (let i = 0; i < n; i++) {
    const t = start + (arc * i) / (arc === Math.PI * 2 ? n : n - 1);
    out.push([Math.cos(t) * rx, Math.sin(t) * rz]);
  }
  return out;
}

export function ellipseShape(rx: number, rz: number, arc: number, start: number): THREE.Shape {
  const s = new THREE.Shape();
  s.absellipse(0, 0, rx, rz, start, start + arc, false, 0);
  if (arc < Math.PI * 2) s.lineTo(0, 0);
  s.closePath();
  return s;
}

/** Elliptical annulus extruded to height h, lying flat with +y up. */
export function Annulus({ rx, rz, inner, h, y = 0, color, arc = Math.PI * 2, start = 0 }: { rx: number; rz: number; inner: number; h: number; y?: number; color: string; arc?: number; start?: number }) {
  const geom = useMemo(() => {
    const outer = ellipseShape(rx, rz, arc, start);
    const hole = new THREE.Path();
    hole.absellipse(0, 0, rx * inner, rz * inner, start, start + arc, false, 0);
    if (arc < Math.PI * 2) hole.lineTo(0, 0);
    hole.closePath();
    outer.holes.push(hole);
    const g = new THREE.ExtrudeGeometry(outer, { depth: h, bevelEnabled: false, curveSegments: 48 });
    g.rotateX(-Math.PI / 2);
    g.translate(0, h, 0);
    return g;
  }, [rx, rz, inner, h, arc, start]);
  return <mesh geometry={geom} position-y={y} material={mat(color)} />;
}

/** Stadium (hippodrome) annulus: flat at -x, rounded at +x. */
export function StadiumRing({ length, width, thickness, h, y = 0, color }: { length: number; width: number; thickness: number; h: number; y?: number; color: string }) {
  const geom = useMemo(() => {
    const mk = (L: number, W: number) => {
      const r = W / 2;
      const s = new THREE.Shape();
      s.moveTo(-L / 2, -r);
      s.lineTo(L / 2 - r, -r);
      s.absarc(L / 2 - r, 0, r, -Math.PI / 2, Math.PI / 2, false);
      s.lineTo(-L / 2, r);
      s.closePath();
      return s;
    };
    const outer = mk(length, width);
    const innerS = mk(length - thickness * 2, width - thickness * 2);
    const hole = new THREE.Path(innerS.getPoints(40));
    outer.holes.push(hole);
    const g = new THREE.ExtrudeGeometry(outer, { depth: h, bevelEnabled: false, curveSegments: 40 });
    g.rotateX(-Math.PI / 2);
    g.translate(0, h, 0);
    return g;
  }, [length, width, thickness, h]);
  return <mesh geometry={geom} position-y={y} material={mat(color)} />;
}
