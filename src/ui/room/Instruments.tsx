import { useEffect, useMemo, useRef } from "react";
import { useFrame, type ThreeEvent } from "@react-three/fiber";
import { Outlines } from "@react-three/drei";
import * as THREE from "three";
import { mergeGeometries } from "three/addons/utils/BufferGeometryUtils.js";
import { B, merge, type Part } from "./Cabinet";
import { astrolabePlateTexture, celestialTexture } from "./charts";
import { BRASS, GILT, OUTLINE, toon, toonGradient, WOOD, WOOD_DARK, WOOD_LIGHT } from "./toon";
import { tipHandlers } from "./roomState";

/**
 * The navigator's and astronomer's instruments set out on the plan chest and
 * against the wall: an astrolabe, a mariner's quadrant on its stand, a pair
 * of dividers, a log glass and a cross-staff. Each tells you what it was for,
 * and does its one trick when clicked (the rete turns, the quadrant sights a
 * star, the dividers step, the glass is turned, the cross slides). Fixed
 * parts are merged per colour; the moving parts are a mesh or two each, and
 * every animation sleeps until it is clicked.
 */
const STEEL = "#9aa0a6", BRASS_DARK = "#b8863a", INKY = "#5a3a1e";
type V3 = [number, number, number];

let tintedMat: THREE.MeshToonMaterial | null = null;
/** One toon material for every merged prop: the colours ride in the vertices. */
const tinted = () => (tintedMat ??= new THREE.MeshToonMaterial({ vertexColors: true, gradientMap: toonGradient() }));

/**
 * Merge parts into at most two meshes (outlined, and not), each part's colour
 * written into its vertices, so a whole prop costs a draw call or two
 * whatever its palette.
 */
export function tint(parts: Part[]) {
  const by = new Map<boolean, THREE.BufferGeometry[]>();
  const col = new THREE.Color();
  for (const p of merge(parts)) {
    col.set(p.color);
    const n = p.geom.getAttribute("position").count;
    const a = new Float32Array(n * 3);
    for (let i = 0; i < n; i++) ((a[i * 3] = col.r), (a[i * 3 + 1] = col.g), (a[i * 3 + 2] = col.b));
    p.geom.setAttribute("color", new THREE.BufferAttribute(a, 3));
    if (!by.has(p.outline)) by.set(p.outline, []);
    by.get(p.outline)!.push(p.geom);
  }
  return [...by].map(([outline, gs]) => {
    const geom = gs.length === 1 ? gs[0] : mergeGeometries(gs)!;
    if (gs.length > 1) gs.forEach((g) => g.dispose());
    geom.computeBoundingSphere();
    return { geom, outline };
  });
}

/** Static parts merged (see tint), freed with the component. */
export function useParts(build: () => Part[], deps: unknown[] = []) {
  // eslint-disable-next-line react-hooks/exhaustive-deps
  const parts = useMemo(() => tint(build()), deps);
  useEffect(() => () => parts.forEach((p) => p.geom.dispose()), [parts]);
  return parts;
}

export function Parts({ parts, shadow = false, thickness = 0.006 }: { parts: ReturnType<typeof tint>; shadow?: boolean; thickness?: number }) {
  return (
    <>
      {parts.map((p, i) => (
        <mesh key={i} geometry={p.geom} material={tinted()} castShadow={shadow} receiveShadow={shadow}>
          {p.outline && <Outlines thickness={thickness} color={OUTLINE} angle={0.5} />}
        </mesh>
      ))}
    </>
  );
}

const ease = (x: number) => (x <= 0 ? 0 : x >= 1 ? 1 : x * x * (3 - 2 * x));
const click = (run: () => void) => (e: ThreeEvent<MouseEvent>) => {
  e.stopPropagation();
  run();
};

/* ------------------------------------------------------------------ astrolabe */

/** An astrolabe hung by its ring from a little stand; click and the rete of stars turns a full day. */
export function Astrolabe({ at, ry = 0 }: { at: V3; ry?: number }) {
  const R = 0.16, Y = 0.31;
  const plate = useMemo(astrolabePlateTexture, []);
  useEffect(() => () => plate.dispose(), [plate]);
  const body = useParts(() => [
    // the stand: a walnut foot, a post and the pin the ring hangs on
    { g: B(0.26, 0.04, 0.14, 0, 0.02, -0.03), c: WOOD_DARK, o: true },
    { g: new THREE.CylinderGeometry(0.012, 0.017, 0.52, 8).translate(0, 0.28, -0.05), c: WOOD },
    { g: new THREE.CylinderGeometry(0.005, 0.005, 0.07, 6).rotateX(Math.PI / 2).translate(0, Y + R + 0.074, -0.02), c: BRASS },
    // the mater with its raised limb, the throne and the shackle ring
    { g: new THREE.CylinderGeometry(R, R, 0.02, 36).rotateX(Math.PI / 2).translate(0, Y, 0), c: BRASS, o: true },
    { g: new THREE.TorusGeometry(R - 0.008, 0.011, 5, 40).translate(0, Y, 0.011), c: GILT },
    { g: B(0.06, 0.045, 0.02, 0, Y + R + 0.012, 0), c: BRASS, o: true },
    { g: new THREE.TorusGeometry(0.025, 0.006, 6, 16).translate(0, Y + R + 0.06, 0), c: GILT },
  ]);
  const rete = useParts(() => {
    const P: Part[] = [
      { g: new THREE.TorusGeometry(R * 0.8, 0.005, 4, 36), c: BRASS_DARK },
      { g: new THREE.TorusGeometry(R * 0.48, 0.006, 4, 32).translate(0, R * 0.26, 0), c: BRASS_DARK },
      { g: B(R * 1.6, 0.008, 0.004, 0, 0, 0), c: BRASS_DARK },
      { g: B(0.008, R * 1.6, 0.004, 0, 0, 0), c: BRASS_DARK },
    ];
    // star pointers, flame-shaped, each for a named star
    const stars: [number, number, number][] = [[0.55, 0.3, 0.5], [0.62, 1.5, -1], [0.4, 2.4, 2.2], [0.7, 3.4, 1.4], [0.5, 4.3, -0.4], [0.66, 5.2, 2.8], [0.3, 5.9, 0.9]];
    for (const [r, a, turn] of stars) P.push({ g: new THREE.ConeGeometry(0.008, 0.04, 4).rotateZ(turn).translate(Math.cos(a) * r * R, Math.sin(a) * r * R, 0), c: GILT });
    return P;
  });
  const rule = useParts(() => [
    { g: B(R * 1.9, 0.016, 0.004, 0, 0, 0), c: BRASS_DARK },
    { g: new THREE.CylinderGeometry(0.012, 0.012, 0.03, 10).rotateX(Math.PI / 2), c: GILT },
  ]);
  const reteRef = useRef<THREE.Group>(null);
  const ruleRef = useRef<THREE.Group>(null);
  const t = useRef(-1);
  useFrame((_, dt) => {
    if (t.current < 0) return;
    t.current += Math.min(dt, 0.05);
    const k = ease(t.current / 2.6);
    if (reteRef.current) reteRef.current.rotation.z = -k * Math.PI * 2;
    if (ruleRef.current) ruleRef.current.rotation.z = 0.5 + k * Math.PI;
    if (t.current > 2.6) t.current = -1;
  });
  return (
    <group position={at} rotation={[0, ry, 0]} {...tipHandlers({ title: "An astrolabe", text: "A brass model of the sky: turn the rete of stars over the plate and it tells the hour, by day or night, and the height of the sun. Perfected by astronomers of the Islamic world.", hint: "Click to turn the rete" })} onClick={click(() => t.current < 0 && (t.current = 0))}>
      <Parts parts={body} />
      <mesh position={[0, Y, 0.0105]}>
        <circleGeometry args={[R * 0.86, 32]} />
        <meshToonMaterial map={plate} gradientMap={toonGradient()} />
      </mesh>
      <group ref={reteRef} position={[0, Y, 0.016]}>
        <Parts parts={rete} />
      </group>
      <group ref={ruleRef} position={[0, Y, 0.022]} rotation={[0, 0, 0.5]}>
        <Parts parts={rule} />
      </group>
    </group>
  );
}

/* ------------------------------------------------------------------ quadrant */

/** A mariner's quadrant pivoted on a stand; click and it sights a star while its plumb line keeps hanging true. */
export function Quadrant({ at, ry = 0 }: { at: V3; ry?: number }) {
  const R = 0.3, AP = 0.5, L = 0.25;
  const stand = useParts(() => [
    { g: B(0.2, 0.04, 0.14, 0, 0.02, -0.02), c: WOOD_DARK, o: true },
    { g: new THREE.CylinderGeometry(0.013, 0.018, AP, 8).translate(0, AP / 2 + 0.02, -0.035), c: WOOD },
    { g: new THREE.CylinderGeometry(0.008, 0.008, 0.06, 8).rotateX(Math.PI / 2).translate(0, AP, -0.01), c: BRASS },
  ]);
  const plate = useParts(() => {
    // the quarter disc, apex at the pivot, one edge level and one hanging down; the sights on the level edge
    const s = new THREE.Shape();
    s.moveTo(0, 0);
    s.lineTo(R, 0);
    s.absarc(0, 0, R, 0, -Math.PI / 2, true);
    s.lineTo(0, 0);
    const P: Part[] = [
      { g: new THREE.ExtrudeGeometry(s, { depth: 0.01, bevelEnabled: false, curveSegments: 16 }).translate(0, 0, -0.005), c: BRASS, o: true },
      { g: B(0.022, 0.04, 0.014, 0.05, 0.02, 0), c: BRASS_DARK },
      { g: B(0.022, 0.04, 0.014, R - 0.04, 0.02, 0), c: BRASS_DARK },
      { g: new THREE.TorusGeometry(R - 0.055, 0.002, 3, 24, Math.PI / 2).rotateZ(-Math.PI / 2).translate(0, 0, 0.006), c: INKY },
    ];
    // the degree scale round the arc
    for (let d = 0; d <= 90; d += 5) {
      const a = (-d * Math.PI) / 180, len = d % 10 ? 0.018 : 0.032;
      P.push({ g: B(len, 0.003, 0.002, 0, 0, 0).rotateZ(a).translate(Math.cos(a) * (R - 0.012 - len / 2), Math.sin(a) * (R - 0.012 - len / 2), 0.006), c: INKY });
    }
    return P;
  });
  const plumb = useParts(() => [
    { g: new THREE.CylinderGeometry(0.0016, 0.0016, L, 4).translate(0, -L / 2, 0), c: "#e8dcc0" },
    { g: new THREE.ConeGeometry(0.014, 0.036, 8).rotateX(Math.PI).translate(0, -L - 0.016, 0), c: BRASS },
  ]);
  const plateRef = useRef<THREE.Group>(null);
  const plumbRef = useRef<THREE.Group>(null);
  const s = useRef({ t: -1, th: 0, w: 0, prev: 0, prevV: 0 });
  useFrame((_, dtRaw) => {
    const q = s.current;
    if (q.t < 0 && Math.abs(q.th) + Math.abs(q.w) < 1e-3) return;
    const dt = Math.min(dtRaw, 0.05);
    let tilt = 0;
    if (q.t >= 0) {
      q.t += dt;
      // up to a star at about 35 degrees, hold while the line settles, and back down
      tilt = -0.62 * (ease(q.t / 0.9) - ease((q.t - 2.4) / 0.9));
      if (q.t > 3.3) q.t = -1;
    }
    // the plumb bob is a damped pendulum pushed about by the plate's turning
    const v = (tilt - q.prev) / Math.max(dt, 1e-4);
    const acc = (v - q.prevV) / Math.max(dt, 1e-4);
    q.prev = tilt;
    q.prevV = v;
    q.w += (-45 * q.th - 2.2 * q.w - Math.max(-30, Math.min(30, acc)) * 0.6) * dt;
    q.th += q.w * dt;
    if (plateRef.current) plateRef.current.rotation.z = tilt;
    if (plumbRef.current) plumbRef.current.rotation.z = q.th;
  });
  return (
    <group position={at} rotation={[0, ry, 0]} {...tipHandlers({ title: "A mariner's quadrant", text: "Sight the Pole Star along its edge and the plumb line falls across your latitude: Portuguese pilots carried it down the coast of Africa in the 1400s.", hint: "Click to sight a star" })} onClick={click(() => s.current.t < 0 && (s.current.t = 0))}>
      <Parts parts={stand} />
      <group ref={plateRef} position={[0, AP, 0]}>
        <Parts parts={plate} />
      </group>
      <group ref={plumbRef} position={[0, AP, 0.012]}>
        <Parts parts={plumb} />
      </group>
    </group>
  );
}

/* ------------------------------------------------------------------ dividers */

/** A pair of brass and steel dividers standing on their points; click and they step out a distance. */
export function Dividers({ at, ry = 0 }: { at: V3; ry?: number }) {
  const L = 0.3;
  const leg = useParts(() => [
    { g: new THREE.CylinderGeometry(0.011, 0.012, L * 0.32, 8).translate(0, -L * 0.16, 0), c: BRASS, o: true },
    { g: new THREE.CylinderGeometry(0.009, 0.0015, L * 0.68, 8).translate(0, -L * 0.66, 0), c: STEEL, o: true },
  ]);
  const head = useParts(() => [
    { g: new THREE.CylinderGeometry(0.022, 0.022, 0.03, 14).rotateX(Math.PI / 2), c: BRASS, o: true },
    { g: new THREE.CylinderGeometry(0.006, 0.01, 0.05, 8).translate(0, 0.035, 0), c: BRASS },
    { g: new THREE.SphereGeometry(0.012, 10, 8).translate(0, 0.065, 0), c: GILT },
  ]);
  const hinge = useRef<THREE.Group>(null);
  const legs = useRef<(THREE.Group | null)[]>([]);
  const t = useRef(-1);
  const pose = (h: number, x: number) => {
    if (hinge.current) hinge.current.position.set(x, L * Math.cos(h), 0);
    legs.current.forEach((g, i) => g && (g.rotation.z = (i ? 1 : -1) * h));
  };
  useEffect(() => pose(0.2, 0), []); // eslint-disable-line react-hooks/exhaustive-deps
  useFrame((_, dt) => {
    if (t.current < 0) return;
    t.current += Math.min(dt, 0.05);
    // open, close, open, close: two steps along a scale, then home
    const k = Math.min(1, t.current / 2.4);
    pose(0.2 + 0.26 * Math.pow(Math.sin(k * Math.PI * 2), 2), Math.sin(k * Math.PI) * 0.05);
    if (t.current > 2.4) t.current = -1;
  });
  return (
    <group position={at} rotation={[0, ry, 0]} {...tipHandlers({ title: "Brass dividers", text: "Opened to a span on the scale of miles and walked along a route, they measured distances on a chart.", hint: "Click to step them" })} onClick={click(() => t.current < 0 && (t.current = 0))}>
      <group ref={hinge}>
        <Parts parts={head} />
        {[0, 1].map((i) => (
          <group key={i} ref={(g) => void (legs.current[i] = g)} position={[0, 0, i ? 0.006 : -0.006]}>
            <Parts parts={leg} />
          </group>
        ))}
      </group>
      {/* the hit area: the legs are thin */}
      <mesh position={[0, 0.17, 0]} visible={false}>
        <boxGeometry args={[0.24, 0.36, 0.08]} />
      </mesh>
    </group>
  );
}

/* ------------------------------------------------------------------ sandglass */

/** A half-minute log glass between turned posts; click to turn it, and the sand runs. */
export function Sandglass({ at, ry = 0 }: { at: V3; ry?: number }) {
  const HH = 0.15; // half the height
  const frame = useParts(() => {
    const P: Part[] = [];
    for (const s of [-1, 1]) {
      P.push({ g: new THREE.CylinderGeometry(0.088, 0.088, 0.022, 18).translate(0, s * (HH - 0.011), 0), c: WOOD_DARK, o: true });
      P.push({ g: new THREE.CylinderGeometry(0.07, 0.08, 0.012, 18).translate(0, s * (HH - 0.028), 0), c: WOOD_LIGHT });
    }
    for (let i = 0; i < 3; i++) {
      const a = (i / 3) * Math.PI * 2 + 0.5;
      P.push({ g: new THREE.LatheGeometry([[0.008, -HH + 0.02], [0.011, -HH + 0.05], [0.006, -0.06], [0.01, 0], [0.006, 0.06], [0.011, HH - 0.05], [0.008, HH - 0.02]].map(([r, y]) => new THREE.Vector2(r, y)), 6).translate(Math.cos(a) * 0.068, 0, Math.sin(a) * 0.068), c: WOOD });
    }
    return P;
  });
  const geo = useMemo(() => {
    const bulb = new THREE.LatheGeometry(([[0.0, -0.13], [0.048, -0.124], [0.06, -0.08], [0.048, -0.036], [0.012, -0.008], [0.007, 0], [0.012, 0.008], [0.048, 0.036], [0.06, 0.08], [0.048, 0.124], [0, 0.13]] as [number, number][]).map(([r, y]) => new THREE.Vector2(r, y)), 18);
    const heap = new THREE.ConeGeometry(0.05, 0.065, 14).translate(0, 0.0325, 0);
    const funnel = new THREE.ConeGeometry(0.052, 0.07, 14).rotateX(Math.PI).translate(0, 0.035, 0);
    const stream = new THREE.CylinderGeometry(0.0022, 0.0022, 1, 4).translate(0, -0.5, 0);
    return { bulb, heap, funnel, stream };
  }, []);
  useEffect(() => () => Object.values(geo).forEach((g) => g.dispose()), [geo]);
  const glass = useMemo(() => new THREE.MeshBasicMaterial({ color: "#eef6f2", transparent: true, opacity: 0.28, depthWrite: false }), []);
  useEffect(() => () => glass.dispose(), [glass]);
  const sand = toon("#d9b26a");
  const g = useRef<THREE.Group>(null);
  const top = useRef<THREE.Mesh>(null);
  const bottom = useRef<THREE.Mesh>(null);
  const stream = useRef<THREE.Mesh>(null);
  // a: the share of the sand in the upper bulb; flip: how far through being turned over (-1 when standing)
  const s = useRef({ a: 0, flip: -1, dirty: true });
  useFrame((_, dtRaw) => {
    const q = s.current;
    if (q.flip < 0 && q.a <= 0 && !q.dirty) return;
    q.dirty = false;
    const dt = Math.min(dtRaw, 0.05);
    if (q.flip >= 0) {
      q.flip += dt / 0.7;
      if (q.flip >= 1) {
        // the glass is the same either way up: stand it back at rest and swap the bulbs' sand instead
        q.flip = -1;
        q.a = 1 - q.a;
      }
    } else q.a = Math.max(0, q.a - dt / 10);
    const f = q.flip >= 0 ? ease(q.flip) : 0;
    if (g.current) {
      g.current.rotation.z = f * Math.PI;
      g.current.position.y = HH + 0.004 + Math.sin(f * Math.PI) * 0.06;
    }
    const kt = Math.cbrt(q.a), kb = Math.cbrt(1 - q.a);
    if (top.current) (top.current.scale.setScalar(Math.max(kt, 1e-3)), (top.current.visible = kt > 0.02));
    if (bottom.current) (bottom.current.scale.setScalar(Math.max(kb, 1e-3)), (bottom.current.visible = kb > 0.02));
    if (stream.current) {
      stream.current.visible = q.flip < 0 && q.a > 0;
      stream.current.scale.y = 0.118 - 0.065 * kb;
    }
  });
  return (
    <group position={at} rotation={[0, ry, 0]} {...tipHandlers({ title: "A log glass", text: "Turned as the knotted log line ran out over the stern: the knots counted before the sand ran through gave a ship's speed, which is why we still say knots.", hint: "Click to turn it" })} onClick={click(() => s.current.flip < 0 && ((s.current.flip = 0), (s.current.dirty = true)))}>
      <group ref={g} position={[0, HH + 0.004, 0]}>
        <Parts parts={frame} />
        <mesh ref={top} geometry={geo.funnel} material={sand} position={[0, 0.006, 0]} visible={false} />
        <mesh ref={bottom} geometry={geo.heap} material={sand} position={[0, -0.122, 0]} />
        <mesh ref={stream} geometry={geo.stream} material={sand} position={[0, 0, 0]} visible={false} />
        <mesh geometry={geo.bulb} material={glass} renderOrder={2} />
      </group>
    </group>
  );
}

/* ------------------------------------------------------------------ cross-staff */

/** A cross-staff leaning on the wall: foot on the floor at `at`, top against the wall; click to slide the cross. */
export function CrossStaff({ at, lean, len = 1.5 }: { at: V3; lean: number; len?: number }) {
  const staff = useParts(() => {
    const P: Part[] = [
      { g: B(0.032, len, 0.032, 0, len / 2, 0), c: WOOD_LIGHT, o: true },
      { g: new THREE.CylinderGeometry(0.02, 0.02, 0.05, 8).translate(0, 0.025, 0), c: BRASS },
      { g: new THREE.CylinderGeometry(0.02, 0.016, 0.04, 8).translate(0, len - 0.02, 0), c: BRASS },
    ];
    // the scale of degrees, marked down the staff
    for (let y = 0.3; y < len - 0.1; y += 0.075) P.push({ g: B(0.034, 0.005, 0.034, 0, y, 0), c: WOOD_DARK });
    return P;
  }, [len]);
  const cross = useParts(() => [
    { g: B(0.5, 0.03, 0.03, 0, 0, 0.03), c: WOOD_LIGHT, o: true },
    { g: B(0.05, 0.07, 0.05, 0, 0, 0), c: WOOD_DARK, o: true },
    { g: B(0.016, 0.06, 0.036, -0.245, 0, 0.03), c: BRASS },
    { g: B(0.016, 0.06, 0.036, 0.245, 0, 0.03), c: BRASS },
  ]);
  const c = useRef<THREE.Group>(null);
  const t = useRef(-1);
  const rest = len * 0.66;
  useFrame((_, dt) => {
    if (t.current < 0 || !c.current) return;
    t.current += Math.min(dt, 0.05);
    // slid down toward the eye until it spans horizon to sun, then back to its place
    const k = Math.min(1, t.current / 2.6);
    c.current.position.y = rest - Math.sin(k * Math.PI) * len * 0.34 + Math.sin(k * Math.PI * 3) * 0.02 * (1 - k);
    if (t.current > 2.6) t.current = -1;
  });
  return (
    <group position={at} rotation={[-lean, 0, 0]} {...tipHandlers({ title: "A cross-staff", text: "Slide the cross until its ends touch the horizon and the sun, and the mark on the staff gives the sun's height, and so your latitude.", hint: "Click to slide the cross" })} onClick={click(() => t.current < 0 && (t.current = 0))}>
      <Parts parts={staff} />
      <group ref={c} position={[0, rest, 0]}>
        <Parts parts={cross} />
      </group>
      <mesh position={[0, len / 2, 0]} visible={false}>
        <boxGeometry args={[0.2, len, 0.1]} />
      </mesh>
    </group>
  );
}

/* ------------------------------------------------------------------ celestial globe */

/** A celestial globe on a three-legged stand, set in its horizon ring; click to set the heavens turning. */
export function CelestialGlobe({ at }: { at: V3 }) {
  const RG = 0.3, CY = 1.12;
  const skin = useMemo(celestialTexture, []);
  useEffect(() => () => skin.dispose(), [skin]);
  const stand = useParts(() => {
    const P: Part[] = [
      { g: new THREE.LatheGeometry(([[0, 0], [0.05, 0], [0.06, 0.08], [0.04, 0.3], [0.055, 0.45], [0.035, 0.62], [0.06, 0.7], [0, 0.72]] as [number, number][]).map(([r, y]) => new THREE.Vector2(r, y)), 10).translate(0, 0.1, 0), c: WOOD, o: true },
      // the horizon ring, broad and flat, painted with the zodiac
      { g: new THREE.TorusGeometry(RG + 0.05, 0.03, 4, 36).rotateX(Math.PI / 2).scale(1, 0.4, 1).translate(0, CY, 0), c: WOOD_LIGHT, o: true },
      { g: new THREE.TorusGeometry(RG + 0.05, 0.012, 4, 36).rotateX(Math.PI / 2).translate(0, CY + 0.013, 0), c: GILT },
    ];
    // the legs splay out to scroll feet; four quadrant arms carry the horizon ring
    for (let i = 0; i < 3; i++) {
      const a = (i / 3) * Math.PI * 2 + 0.4;
      P.push({ g: B(0.04, 0.05, 0.36, 0, 0.06, 0.16).rotateY(a), c: WOOD_DARK, o: true });
    }
    for (let i = 0; i < 4; i++) {
      const a = (i / 4) * Math.PI * 2 + Math.PI / 4;
      P.push({ g: new THREE.TorusGeometry(RG * 0.9, 0.012, 4, 10, Math.PI / 2.4).rotateZ(-Math.PI / 2).translate(0, CY, 0).rotateY(a), c: WOOD_DARK });
    }
    return P;
  });
  const meridian = useParts(() => [
    { g: new THREE.TorusGeometry(RG + 0.03, 0.012, 6, 48), c: BRASS, o: true },
    { g: new THREE.CylinderGeometry(0.008, 0.008, 2 * RG + 0.1, 6), c: BRASS },
  ]);
  const spin = useRef<THREE.Mesh>(null);
  const v = useRef(0);
  useFrame((_, dt) => {
    if (!spin.current || v.current < 1e-3) return;
    v.current *= Math.exp(-0.9 * Math.min(dt, 0.05));
    spin.current.rotation.y += v.current * Math.min(dt, 0.05);
  });
  return (
    <group position={at} {...tipHandlers({ title: "A celestial globe", text: "The heavens seen from outside, so every constellation is drawn back to front. Globe makers sold them in pairs with an Earth.", hint: "Click to turn the heavens" })} onClick={click(() => (v.current = 5))}>
      <Parts parts={stand} thickness={0.007} />
      <group position={[0, CY, 0]} rotation={[0, -0.5, 0.6]}>
        <Parts parts={meridian} />
        <mesh ref={spin}>
          <sphereGeometry args={[RG, 32, 20]} />
          <meshToonMaterial map={skin} gradientMap={toonGradient()} />
          <Outlines thickness={0.01} color={OUTLINE} />
        </mesh>
      </group>
    </group>
  );
}
