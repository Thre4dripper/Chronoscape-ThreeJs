import { useEffect, useMemo, useRef, useState, type ReactNode } from "react";
import { useFrame, type ThreeEvent } from "@react-three/fiber";
import { Outlines } from "@react-three/drei";
import * as THREE from "three";
import { compassRose } from "@/world/world";
import { Parts, useParts } from "./Instruments";
import type { Part } from "./Cabinet";
import { BRASS, GILT, OUTLINE, toon, toonGradient, WOOD_DARK } from "./toon";
import { tipHandlers, useRoom } from "./roomState";

/**
 * What lies in the two drawers of the cabinet's plinth, each set on a board
 * that rises and tilts toward you when its drawer opens (or the drawer front
 * would hide it). The instruments: dividers that walk out a distance, a
 * pocket compass that swings and finds north again, and a reading glass that
 * travels over a little chart, magnifying it. The writing things: a quill
 * that signs a slip of paper, a seal pressed into red wax, and the candle
 * that melts it. Board-local frame: x right, y off the board, z toward you.
 * Every animation sleeps until it is clicked.
 */
type V3 = [number, number, number];
export type DrawerKind = "writing" | "instruments";

const STEEL = "#9aa0a6", INK = "#2b1a10", WAX = "#a3271c";
const ease = (x: number) => (x <= 0 ? 0 : x >= 1 ? 1 : x * x * (3 - 2 * x));
const span = (t: number, a: number, b: number) => ease((t - a) / (b - a));
const click = (run: () => void) => (e: ThreeEvent<MouseEvent>) => {
  e.stopPropagation();
  run();
};

const UP = new THREE.Vector3(0, 1, 0);
/** A tapered rod from a (radius r0) to b (radius r1). */
function rod(a: V3, b: V3, r0: number, r1: number, seg = 8) {
  const A = new THREE.Vector3(...a), D = new THREE.Vector3(...b).sub(A);
  const g = new THREE.CylinderGeometry(r1, r0, D.length(), seg).translate(0, D.length() / 2, 0);
  g.applyQuaternion(new THREE.Quaternion().setFromUnitVectors(UP, D.normalize()));
  return g.translate(A.x, A.y, A.z);
}

function canvasTexture(size: number, draw: (g: CanvasRenderingContext2D, S: number) => void) {
  const c = document.createElement("canvas");
  c.width = c.height = size;
  draw(c.getContext("2d")!, size);
  const t = new THREE.CanvasTexture(c);
  t.colorSpace = THREE.SRGBColorSpace;
  t.anisotropy = 8;
  return t;
}

/** A texture made once per mount and freed with it. */
function useTexture(make: () => THREE.Texture) {
  // eslint-disable-next-line react-hooks/exhaustive-deps
  const t = useMemo(make, []);
  useEffect(() => () => t.dispose(), [t]);
  return t;
}

/* ------------------------------------------------------------------ the rising board */

export function DrawerBoard({ kind, color, children }: { kind: DrawerKind; color: string; children: ReactNode }) {
  const open = useRoom((s) => s.drawer === kind);
  const g = useRef<THREE.Group>(null);
  const t = useRef(0);
  useFrame((_, dt) => {
    const o = g.current;
    if (!o || t.current === (open ? 1 : 0)) return;
    t.current = Math.max(0, Math.min(1, t.current + (open ? dt : -dt) * 2.4));
    const k = ease(t.current);
    o.position.set(0, -0.1 + 0.6 * k, -0.3 + 0.44 * k);
    o.rotation.x = 1.15 * k;
    o.scale.setScalar(1 + 0.5 * k);
  });
  // the board takes every pointer that lands on it, between the tools too, so nothing behind it (the atlases on the shelf) answers
  const block = (e: { stopPropagation: () => void }) => e.stopPropagation();
  return (
    <group ref={g} position={[0, -0.1, -0.3]} onClick={block} onPointerOver={block} onPointerMove={block} onPointerDown={block}>
      <mesh position={[0, -0.006, 0]} material={toon(color)}>
        <boxGeometry args={[0.9, 0.012, 0.36]} />
        <Outlines thickness={0.005} color={OUTLINE} />
      </mesh>
      {children}
    </group>
  );
}

/* ------------------------------------------------------------------ the instruments */

export function MeasureTools() {
  return (
    <>
      <WalkingDividers />
      <PocketCompass at={[0.03, 0, 0.01]} />
      <ChartAndGlass />
    </>
  );
}

/** Dividers lying open on the baize: click and they walk two spans along, pivoting on alternate points, and back. */
function WalkingDividers() {
  const d = 0.09, L = 0.15, hz = -Math.sqrt(L * L - (d * d) / 4);
  const parts = useParts(() => {
    const P: Part[] = [];
    const H: V3 = [0, 0.01, hz];
    for (const s of [-1, 1]) {
      const K: V3 = [s * (d / 2) * 0.38, 0.0085, hz * 0.62];
      P.push({ g: rod(H, K, 0.007, 0.006), c: BRASS, o: true }, { g: rod(K, [s * (d / 2), 0.004, 0], 0.005, 0.0008), c: STEEL, o: true });
    }
    P.push({ g: new THREE.CylinderGeometry(0.016, 0.016, 0.01, 16).translate(0, 0.012, hz), c: BRASS, o: true });
    P.push({ g: new THREE.SphereGeometry(0.006, 8, 6).translate(0, 0.019, hz), c: GILT });
    return P;
  });
  const HOME = { cx: -0.33, cz: 0.03 };
  const SEQ = [1, 1, -1, -1], STEP = 0.55;
  const g = useRef<THREE.Group>(null);
  const st = useRef({ ...HOME, phi: 0, i: -1, t: 0, px: 0, pz: 0, sg: 1, phi0: 0 });
  // pivot on the point that leads the way; the other swings over it to the far side
  const begin = () => {
    const s = st.current, dir = SEQ[s.i];
    const tx = (sg: number) => s.cx + sg * (d / 2) * Math.cos(s.phi);
    s.sg = dir * tx(1) > dir * tx(-1) ? 1 : -1;
    s.px = tx(s.sg);
    s.pz = s.cz - s.sg * (d / 2) * Math.sin(s.phi);
    s.phi0 = s.phi;
    s.t = 0;
  };
  const place = (lift: number) => {
    const s = st.current;
    g.current?.position.set(s.cx, lift, s.cz);
    if (g.current) g.current.rotation.y = s.phi;
  };
  useEffect(() => place(0), []); // eslint-disable-line react-hooks/exhaustive-deps
  useFrame((_, dt) => {
    const s = st.current;
    if (s.i < 0) return;
    s.t += Math.min(dt, 0.05) / STEP;
    const e = ease(Math.min(1, s.t));
    s.phi = s.phi0 - SEQ[s.i] * Math.PI * e;
    s.cx = s.px - s.sg * (d / 2) * Math.cos(s.phi);
    s.cz = s.pz + s.sg * (d / 2) * Math.sin(s.phi);
    place(0.008 * Math.sin(Math.PI * e));
    if (s.t < 1) return;
    if (++s.i < SEQ.length) begin();
    else Object.assign(s, HOME, { phi: 0, i: -1 });
  });
  return (
    <group ref={g} {...tipHandlers({ title: "Brass dividers", text: "Opened to a span on the scale of miles, then walked point over point along a route: so many spans, so many miles.", hint: "Click to walk them" })} onClick={click(() => st.current.i < 0 && ((st.current.i = 0), begin()))}>
      <Parts parts={parts} thickness={0.004} />
      <mesh position={[0, 0.012, hz / 2]} visible={false}>
        <boxGeometry args={[d + 0.03, 0.03, -hz + 0.03]} />
      </mesh>
    </group>
  );
}

/** A pocket compass: its needle sways a little; jostle it and it swings wildly, then settles on north. */
function PocketCompass({ at }: { at: V3 }) {
  const body = useParts(() => [
    { g: new THREE.CylinderGeometry(0.075, 0.078, 0.022, 28).translate(0, 0.011, 0), c: BRASS, o: true },
    { g: new THREE.TorusGeometry(0.071, 0.005, 6, 28).rotateX(Math.PI / 2).translate(0, 0.022, 0), c: GILT },
    { g: new THREE.CylinderGeometry(0.008, 0.008, 0.016, 8).rotateX(Math.PI / 2).translate(0, 0.011, -0.082), c: BRASS },
    { g: new THREE.TorusGeometry(0.014, 0.0035, 6, 16).rotateX(Math.PI / 2).translate(0, 0.011, -0.1), c: BRASS, o: true },
  ]);
  const needle = useParts(() => [
    { g: new THREE.ConeGeometry(0.009, 0.055, 4).translate(0, 0.0275, 0).rotateX(-Math.PI / 2).scale(1, 0.35, 1), c: "#a65238" },
    { g: new THREE.ConeGeometry(0.009, 0.055, 4).translate(0, 0.0275, 0).rotateX(Math.PI / 2).scale(1, 0.35, 1), c: "#3d2a1c" },
    { g: new THREE.CylinderGeometry(0.005, 0.005, 0.006, 10), c: GILT },
  ]);
  const dial = useTexture(() =>
    canvasTexture(256, (g, S) => {
      g.fillStyle = "#efe2c3";
      g.fillRect(0, 0, S, S);
      g.strokeStyle = "#5a3a1e";
      g.lineWidth = 2;
      g.beginPath();
      g.arc(S / 2, S / 2, S * 0.46, 0, Math.PI * 2);
      g.stroke();
      for (let i = 0; i < 32; i++) {
        const a = (i / 32) * Math.PI * 2, r0 = S * (i % 4 ? 0.42 : 0.39);
        g.beginPath();
        g.moveTo(S / 2 + Math.cos(a) * r0, S / 2 + Math.sin(a) * r0);
        g.lineTo(S / 2 + Math.cos(a) * S * 0.46, S / 2 + Math.sin(a) * S * 0.46);
        g.stroke();
      }
      compassRose(g, S / 2, S / 2, S * 0.36);
    }),
  );
  const n = useRef<THREE.Group>(null);
  const kick = useRef(-1);
  useFrame((s, dt) => {
    if (!n.current) return;
    const t = s.clock.elapsedTime;
    let a = Math.sin(t * 1.3) * 0.12 + Math.sin(t * 3.1) * 0.03;
    if (kick.current >= 0) {
      kick.current += Math.min(dt, 0.05);
      a += 5 * Math.exp(-1.4 * kick.current) * Math.cos(7 * kick.current);
      if (kick.current > 4.5) kick.current = -1;
    }
    n.current.rotation.y = a;
  });
  return (
    <group position={at} {...tipHandlers({ title: "A pocket compass", text: "A magnetised needle on a pin: knock it and it swings, but it always comes back to north.", hint: "Click to jostle it" })} onClick={click(() => (kick.current = 0))}>
      <Parts parts={body} thickness={0.004} />
      <mesh position={[0, 0.0225, 0]} rotation-x={-Math.PI / 2}>
        <circleGeometry args={[0.066, 32]} />
        <meshToonMaterial map={dial} gradientMap={toonGradient()} />
      </mesh>
      <group ref={n} position={[0, 0.027, 0]}>
        <Parts parts={needle} />
      </group>
    </group>
  );
}

/** The little chart under the glass: coast, rhumb lines, towns and a scale of miles, too small to read without it. */
function drawChart(g: CanvasRenderingContext2D, S: number) {
  let seed = 11;
  const rnd = () => ((seed = (seed * 16807) % 2147483647) / 2147483647);
  g.fillStyle = "#efe0bb";
  g.fillRect(0, 0, S, S);
  // rhumb lines from a point at sea
  g.strokeStyle = "rgba(122,62,38,0.35)";
  g.lineWidth = 1.2;
  for (let i = 0; i < 16; i++) {
    const a = (i / 16) * Math.PI * 2;
    g.beginPath();
    g.moveTo(S * 0.22, S * 0.6);
    g.lineTo(S * 0.22 + Math.cos(a) * S * 1.2, S * 0.6 + Math.sin(a) * S * 1.2);
    g.stroke();
  }
  // the coast, with the engraver's water lines running along it
  const coast: [number, number][] = [];
  for (let y = -10; y <= S + 10; y += 14) coast.push([S * 0.42 + Math.sin(y / 60) * 40 + (rnd() - 0.5) * 18, y]);
  for (let k = 6; k >= 0; k--) {
    g.strokeStyle = k ? `rgba(70,45,25,${0.32 - k * 0.04})` : "#4a3020";
    g.lineWidth = k ? 1.2 : 2.6;
    g.beginPath();
    coast.forEach(([x, y], i) => (i ? g.lineTo(x - k * 9, y) : g.moveTo(x - k * 9, y)));
    g.stroke();
  }
  g.fillStyle = "#e6d3a6";
  g.beginPath();
  coast.forEach(([x, y], i) => (i ? g.lineTo(x, y) : g.moveTo(x, y)));
  g.lineTo(S + 10, S + 10);
  g.lineTo(S + 10, -10);
  g.fill();
  // hills and a river inland
  g.strokeStyle = "#5a3a1e";
  g.lineWidth = 2;
  for (let i = 0; i < 9; i++) {
    const x = S * 0.62 + rnd() * S * 0.32, y = S * 0.08 + rnd() * S * 0.5;
    g.beginPath();
    g.moveTo(x - 12, y + 6);
    g.quadraticCurveTo(x, y - 12, x + 12, y + 6);
    g.stroke();
  }
  g.lineWidth = 2.4;
  g.beginPath();
  g.moveTo(coast[22][0], coast[22][1]);
  g.bezierCurveTo(S * 0.6, S * 0.7, S * 0.75, S * 0.55, S * 0.98, S * 0.62);
  g.stroke();
  // towns
  g.fillStyle = "#3d2a1c";
  g.font = 'italic 22px "IM Fell English", Georgia, serif';
  for (const [x, y, name] of [
    [0.55, 0.2, "Portus Magnus"],
    [0.66, 0.42, "Castrum"],
    [0.52, 0.8, "S. Maria"],
    [0.72, 0.88, "Villa Nova"],
  ] as const) {
    g.beginPath();
    g.arc(S * x, S * y, 5, 0, Math.PI * 2);
    g.fill();
    g.fillText(name, S * x + 9, S * y + 7);
  }
  g.font = '600 20px "Cinzel", Georgia, serif';
  g.fillText("M A R E", S * 0.06, S * 0.3);
  // a scale of miles
  const x0 = S * 0.56, y0 = S * 0.66, w = S * 0.36;
  g.strokeStyle = "#3d2a1c";
  g.lineWidth = 2;
  g.strokeRect(x0, y0, w, 10);
  for (let i = 0; i < 4; i++) if (i % 2 === 0) g.fillRect(x0 + (w / 4) * i, y0, w / 4, 10);
  g.font = '15px "IM Fell English", Georgia, serif';
  ["0", "10", "20", "30", "40"].forEach((s, i) => g.fillText(s, x0 + (w / 4) * i - 4, y0 + 28));
  g.font = 'italic 15px "IM Fell English", Georgia, serif';
  g.fillText("Scala milliarium", x0 + 20, y0 - 8);
  g.lineWidth = 3;
  g.strokeRect(5, 5, S - 10, S - 10);
}

/** A chart on the baize and a reading glass on it; click and the glass travels over the chart, magnifying what it passes. */
function ChartAndGlass() {
  const X0 = 0.15, X1 = 0.43, Z0 = -0.14, Z1 = 0.14, W = X1 - X0, D = Z1 - Z0;
  const R = 0.05, M = 2.6;
  const chart = useTexture(() => canvasTexture(512, drawChart));
  const lensTex = useTexture(() => {
    const t = chart.clone();
    t.needsUpdate = true;
    t.wrapS = t.wrapT = THREE.ClampToEdgeWrapping;
    t.repeat.set((2 * R) / (M * W), (2 * R) / (M * D));
    return t;
  });
  const frame = useParts(() => [
    { g: new THREE.TorusGeometry(R, 0.007, 8, 32).rotateX(Math.PI / 2), c: BRASS, o: true },
    { g: rod([-0.6 * R, 0, 0.8 * R], [-0.6 * (R + 0.02), 0, 0.8 * (R + 0.02)], 0.006, 0.006), c: BRASS },
    { g: rod([-0.6 * (R + 0.02), 0, 0.8 * (R + 0.02)], [-0.6 * (R + 0.1), 0, 0.8 * (R + 0.1)], 0.009, 0.011), c: WOOD_DARK, o: true },
  ]);
  const REST = new THREE.Vector3(0.35, 0.012, 0.075);
  const path = useMemo(
    () => new THREE.CatmullRomCurve3([REST.clone(), new THREE.Vector3(0.3, 0.03, -0.02), new THREE.Vector3(0.21, 0.03, -0.08), new THREE.Vector3(0.32, 0.03, -0.09), new THREE.Vector3(0.36, 0.03, 0.02), new THREE.Vector3(0.24, 0.03, 0.08), REST.clone()]),
    [], // eslint-disable-line react-hooks/exhaustive-deps
  );
  const lens = useRef<THREE.Group>(null);
  const t = useRef(-1);
  const at = useMemo(() => new THREE.Vector3(), []);
  const aim = (p: THREE.Vector3) => {
    lens.current?.position.copy(p);
    // show the part of the chart under the glass, M times larger
    lensTex.offset.set((p.x - X0) / W - lensTex.repeat.x / 2, (Z1 - p.z) / D - lensTex.repeat.y / 2);
  };
  useEffect(() => aim(REST), []); // eslint-disable-line react-hooks/exhaustive-deps
  useFrame((_, dt) => {
    if (t.current < 0) return;
    t.current = Math.min(1, t.current + Math.min(dt, 0.05) / 4.5);
    aim(path.getPoint(ease(t.current), at));
    if (t.current >= 1) t.current = -1;
  });
  return (
    <>
      <mesh position={[(X0 + X1) / 2, 0.002, (Z0 + Z1) / 2]} rotation-x={-Math.PI / 2}>
        <planeGeometry args={[W, D]} />
        <meshToonMaterial map={chart} gradientMap={toonGradient()} />
      </mesh>
      <group ref={lens} {...tipHandlers({ title: "A reading glass", text: "Map makers crowded their sheets with names too small for the eye: a glass to read them by.", hint: "Click to read the chart" })} onClick={click(() => t.current < 0 && (t.current = 0))}>
        <Parts parts={frame} thickness={0.003} />
        <mesh rotation-x={-Math.PI / 2} position-y={0.001}>
          <circleGeometry args={[R, 32]} />
          <meshToonMaterial map={lensTex} gradientMap={toonGradient()} />
        </mesh>
        <mesh rotation-x={-Math.PI / 2} position-y={0.003} raycast={() => null}>
          <ringGeometry args={[R * 0.55, R * 0.78, 20, 1, 2.2, 1.1]} />
          <meshBasicMaterial color="#ffffff" transparent opacity={0.3} depthWrite={false} />
        </mesh>
      </group>
    </>
  );
}

/* ------------------------------------------------------------------ the writing things */

export function WritingTools() {
  return (
    <>
      <QuillAndPaper />
      <SealAndWax />
      <Candle at={[0.36, 0, -0.07]} />
    </>
  );
}

const PAPER = { x0: -0.42, x1: -0.04, z0: -0.12, z1: 0.12 };

/** The flourish the quill writes: looping cursive along the slip, and a swash back under it. */
function flourish(): THREE.Vector2[] {
  const pts: THREE.Vector2[] = [];
  const N = 220;
  for (let i = 0; i <= N; i++) {
    const t = i / N;
    if (t < 0.78) {
      const u = t / 0.78;
      pts.push(new THREE.Vector2(-0.37 + 0.25 * u + 0.012 * Math.sin(u * Math.PI * 12), -0.005 - 0.016 * Math.cos(u * Math.PI * 12) * (0.6 + 0.4 * Math.sin(u * 7))));
    } else {
      const u = (t - 0.78) / 0.22;
      pts.push(new THREE.Vector2(-0.108 - 0.25 * u, 0.025 + 0.022 * Math.sin(u * Math.PI) - 0.012 * u));
    }
  }
  return pts;
}

/** A ribbon of ink along the points, thick and thin like a cut nib held at 45°. */
function inkRibbon(pts: THREE.Vector2[]) {
  const pos: number[] = [], idx: number[] = [];
  for (let i = 0; i < pts.length; i++) {
    const a = pts[Math.max(0, i - 1)], b = pts[Math.min(pts.length - 1, i + 1)];
    const tx = b.x - a.x, tz = b.y - a.y, l = Math.hypot(tx, tz) || 1;
    const w = 0.0036 * (0.3 + 0.7 * Math.abs(Math.sin(Math.atan2(tz, tx) - Math.PI / 4)));
    const nx = (-tz / l) * w, nz = (tx / l) * w;
    pos.push(pts[i].x + nx, 0.0025, pts[i].y + nz, pts[i].x - nx, 0.0025, pts[i].y - nz);
    if (i) idx.push(2 * i - 2, 2 * i - 1, 2 * i, 2 * i - 1, 2 * i + 1, 2 * i);
  }
  const g = new THREE.BufferGeometry();
  g.setAttribute("position", new THREE.Float32BufferAttribute(pos, 3));
  g.setIndex(idx);
  g.setDrawRange(0, 0);
  return g;
}

/** A slip of paper, an inkwell and a goose quill: click and the quill is dipped and signs the slip with a flourish. */
function QuillAndPaper() {
  const pts = useMemo(flourish, []);
  const ink = useMemo(() => inkRibbon(pts), [pts]);
  useEffect(() => () => ink.dispose(), [ink]);
  const paper = useTexture(() =>
    canvasTexture(256, (g, S) => {
      g.fillStyle = "#f3e7cc";
      g.fillRect(0, 0, S, S);
      g.strokeStyle = "rgba(122,80,40,0.18)";
      g.lineWidth = 1;
      for (let y = 40; y < S; y += 30) {
        g.beginPath();
        g.moveTo(14, y);
        g.lineTo(S - 14, y);
        g.stroke();
      }
      g.strokeStyle = "rgba(122,80,40,0.35)";
      g.strokeRect(6, 6, S - 12, S - 12);
    }),
  );
  const well = useParts(() => [
    { g: new THREE.CylinderGeometry(0.032, 0.04, 0.045, 18).translate(0, 0.0225, 0), c: "#26332c", o: true },
    { g: new THREE.CylinderGeometry(0.022, 0.024, 0.01, 18).translate(0, 0.05, 0), c: BRASS, o: true },
    { g: new THREE.CylinderGeometry(0.017, 0.017, 0.002, 16).translate(0, 0.0555, 0), c: "#0e0906" },
  ]);
  const quill = useParts(() => [
    { g: new THREE.ConeGeometry(0.0032, 0.022, 8).rotateX(Math.PI).translate(0, 0.011, 0), c: INK },
    { g: rod([0, 0.02, 0], [0, 0.25, 0], 0.0032, 0.0018), c: "#e8dcc0", o: true },
    { g: new THREE.SphereGeometry(1, 14, 8).scale(0.017, 0.09, 0.0025).translate(0.007, 0.165, 0), c: "#f2ece0", o: true },
    { g: new THREE.SphereGeometry(1, 12, 8).scale(0.009, 0.075, 0.002).translate(-0.004, 0.17, 0), c: "#e4dccb", o: true },
  ]);
  const WELL: V3 = [0.07, 0, -0.06];
  const DIP = new THREE.Vector3(WELL[0], 0.035, WELL[2]);
  const lean = useMemo(() => new THREE.Quaternion().setFromUnitVectors(UP, new THREE.Vector3(0.45, 0.75, -0.5).normalize()), []);
  const q = useRef<THREE.Group>(null);
  const t = useRef(-1);
  const tip = useMemo(() => new THREE.Vector3(), []);
  const wob = useMemo(() => new THREE.Quaternion(), []);
  const pose = (p: THREE.Vector3, wobble = 0) => {
    const o = q.current;
    if (!o) return;
    o.position.copy(p);
    o.quaternion.copy(lean).multiply(wob.setFromAxisAngle(UP, wobble));
  };
  useEffect(() => pose(DIP), []); // eslint-disable-line react-hooks/exhaustive-deps
  // out of the well, over to the slip, the writing, then home
  const T = { lift: 0.4, travel: 0.9, down: 1.05, write: 3.1, up: 3.35, back: 4.0, end: 4.3 };
  const start = new THREE.Vector3(pts[0].x, 0.0025, pts[0].y);
  useFrame((_, dt) => {
    if (t.current < 0) return;
    const s = (t.current += Math.min(dt, 0.05));
    const above = (v: THREE.Vector3, h: number) => tip.copy(v).setY(v.y + h);
    if (s < T.lift) pose(above(DIP, 0.07 * span(s, 0, T.lift)));
    else if (s < T.travel) pose(above(DIP, 0.07).lerp(above(start, 0.05).clone(), span(s, T.lift, T.travel)));
    else if (s < T.down) pose(above(start, 0.05 * (1 - span(s, T.travel, T.down))));
    else if (s < T.write) {
      if (s - Math.min(dt, 0.05) < T.down) ink.setDrawRange(0, 0);
      const k = Math.min(pts.length - 1, Math.floor(((s - T.down) / (T.write - T.down)) * (pts.length - 1)));
      ink.setDrawRange(0, 6 * k);
      pose(tip.set(pts[k].x, 0.0025, pts[k].y), Math.sin(s * 9) * 0.08);
    } else if (s < T.up) pose(above(tip.set(pts[pts.length - 1].x, 0.0025, pts[pts.length - 1].y), 0.06 * span(s, T.write, T.up)));
    else if (s < T.back) {
      const from = new THREE.Vector3(pts[pts.length - 1].x, 0.0625, pts[pts.length - 1].y);
      pose(from.lerp(above(DIP, 0.07).clone(), span(s, T.up, T.back)));
    } else if (s < T.end) pose(above(DIP, 0.07 * (1 - span(s, T.back, T.end))));
    else {
      pose(DIP);
      t.current = -1;
    }
  });
  return (
    <>
      <mesh position={[(PAPER.x0 + PAPER.x1) / 2, 0.001, (PAPER.z0 + PAPER.z1) / 2]} rotation-x={-Math.PI / 2}>
        <planeGeometry args={[PAPER.x1 - PAPER.x0, PAPER.z1 - PAPER.z0]} />
        <meshToonMaterial map={paper} gradientMap={toonGradient()} />
      </mesh>
      <mesh geometry={ink} raycast={() => null}>
        <meshBasicMaterial color={INK} side={THREE.DoubleSide} polygonOffset polygonOffsetFactor={-2} />
      </mesh>
      <group position={WELL}>
        <Parts parts={well} thickness={0.004} />
      </group>
      <group ref={q} {...tipHandlers({ title: "A goose quill and ink", text: "Oak-gall ink and a freshly cut quill: every name on a chart was lettered by hand.", hint: "Click to sign the slip" })} onClick={click(() => t.current < 0 && (t.current = 0))}>
        <Parts parts={quill} thickness={0.003} />
        <mesh position={[0, 0.14, 0]} visible={false}>
          <boxGeometry args={[0.05, 0.26, 0.03]} />
        </mesh>
      </group>
    </>
  );
}

/** A brass seal on a turned handle, and a stick of red wax: click and the seal is pressed into a blob of wax on the slip. */
function SealAndWax() {
  const seal = useParts(() => [
    { g: new THREE.CylinderGeometry(0.02, 0.02, 0.008, 18).translate(0, 0.004, 0), c: BRASS, o: true },
    { g: new THREE.CylinderGeometry(0.008, 0.011, 0.014, 10).translate(0, 0.015, 0), c: BRASS },
    { g: new THREE.CylinderGeometry(0.012, 0.016, 0.06, 12).translate(0, 0.052, 0), c: WOOD_DARK, o: true },
    { g: new THREE.SphereGeometry(0.016, 12, 8).translate(0, 0.084, 0), c: WOOD_DARK, o: true },
  ]);
  const stick = useParts(() => [
    { g: rod([0.27, 0.008, 0.15], [0.41, 0.008, 0.115], 0.008, 0.008), c: WAX, o: true },
    { g: rod([0.41, 0.008, 0.115], [0.416, 0.008, 0.1135], 0.008, 0.005), c: "#6e1810" },
  ]);
  const face = useTexture(() =>
    canvasTexture(128, (g, S) => {
      g.fillStyle = WAX;
      g.fillRect(0, 0, S, S);
      g.strokeStyle = "#5e1209";
      g.lineWidth = 5;
      g.beginPath();
      g.arc(S / 2, S / 2, S * 0.36, 0, Math.PI * 2);
      g.stroke();
      g.fillStyle = "#5e1209";
      g.font = '700 64px "Cinzel", Georgia, serif';
      g.textAlign = "center";
      g.textBaseline = "middle";
      g.fillText("C", S / 2, S / 2 + 4);
      g.fillStyle = "rgba(255,190,170,0.35)";
      g.fillText("C", S / 2 - 2, S / 2 + 2);
    }),
  );
  const REST = new THREE.Vector3(0.21, 0.02, 0.09);
  const AT = new THREE.Vector3(-0.1, 0, 0.075);
  const s = useRef<THREE.Group>(null);
  const wax = useRef<THREE.Group>(null);
  const t = useRef(-1);
  const p = useMemo(() => new THREE.Vector3(), []);
  // lying on its side (r = 1), or standing on its face (r = 0)
  const pose = (v: THREE.Vector3, r: number) => {
    s.current?.position.copy(v);
    if (s.current) s.current.rotation.z = (Math.PI / 2) * r;
  };
  useEffect(() => {
    pose(REST, 1);
    wax.current?.scale.setScalar(0.0001);
  }, []); // eslint-disable-line react-hooks/exhaustive-deps
  const HIGH = 0.07;
  useFrame((_, dt) => {
    if (t.current < 0) return;
    const k = (t.current += Math.min(dt, 0.05));
    const over = p.copy(AT).setY(HIGH);
    if (k < 0.7) pose(p.copy(REST).lerp(over, span(k, 0, 0.7)), 1 - span(k, 0, 0.7));
    else if (k < 1.0) pose(over.setY(HIGH * (1 - span(k, 0.7, 1.0))), 0);
    else if (k < 1.3) pose(over.setY(0), 0);
    else if (k < 1.6) pose(over.setY(HIGH * span(k, 1.3, 1.6)), 0);
    else if (k < 2.3) pose(p.copy(over).lerp(REST, span(k, 1.6, 2.3)), span(k, 1.6, 2.3));
    else {
      pose(REST, 1);
      t.current = -1;
    }
    // the wax: a fresh blob spreads under the seal as it is pressed
    const w = k < 0.75 ? 0 : 0.25 + 0.75 * span(k, 0.75, 1.05);
    wax.current?.scale.set(Math.max(w, 0.0001), 1, Math.max(w, 0.0001));
  });
  return (
    <>
      <Parts parts={stick} thickness={0.003} />
      <group ref={wax} position={[AT.x, 0, AT.z]}>
        <mesh position-y={0.002} material={toon(WAX)}>
          <cylinderGeometry args={[0.026, 0.028, 0.004, 20]} />
        </mesh>
        <mesh position-y={0.0042} rotation-x={-Math.PI / 2}>
          <circleGeometry args={[0.02, 24]} />
          <meshToonMaterial map={face} gradientMap={toonGradient()} />
        </mesh>
      </group>
      <group ref={s} {...tipHandlers({ title: "A seal and sealing wax", text: "A finished chart was folded and closed with the maker's mark pressed into hot wax.", hint: "Click to seal the slip" })} onClick={click(() => t.current < 0 && (t.current = 0))}>
        <Parts parts={seal} thickness={0.003} />
      </group>
    </>
  );
}

/** A candle in a brass chamberstick, to melt the wax: its flame flickers; click to snuff it, and again to light it. */
function Candle({ at }: { at: V3 }) {
  const stick = useParts(() => [
    { g: new THREE.CylinderGeometry(0.045, 0.05, 0.008, 22).translate(0, 0.004, 0), c: BRASS, o: true },
    { g: new THREE.CylinderGeometry(0.02, 0.022, 0.016, 14).translate(0, 0.016, 0), c: BRASS, o: true },
    { g: new THREE.TorusGeometry(0.014, 0.004, 6, 14).translate(0.058, 0.01, 0), c: BRASS, o: true },
    { g: new THREE.CylinderGeometry(0.014, 0.015, 0.08, 14).translate(0, 0.064, 0), c: "#efe4c8", o: true },
    { g: new THREE.CylinderGeometry(0.0012, 0.0012, 0.008, 4).translate(0, 0.108, 0), c: INK },
  ]);
  const [lit, setLit] = useState(true);
  const flame = useRef<THREE.Group>(null);
  const k = useRef(1);
  const q = useMemo(() => new THREE.Quaternion(), []);
  useFrame((s, dt) => {
    const f = flame.current;
    if (!f) return;
    k.current = Math.max(0, Math.min(1, k.current + (lit ? dt : -dt) * 4));
    // the flame burns upward whatever the board's tilt
    f.parent!.getWorldQuaternion(q);
    f.quaternion.copy(q.invert());
    const t = s.clock.elapsedTime;
    const fl = 1 + Math.sin(t * 17) * 0.1 + Math.sin(t * 31) * 0.06;
    f.scale.set(k.current * (1 - (fl - 1) * 0.5), Math.max(k.current * fl, 0.0001), k.current * (1 - (fl - 1) * 0.5));
    f.visible = k.current > 0.01;
  });
  return (
    <group position={at} {...tipHandlers({ title: "A tallow candle", text: "To melt the sealing wax, and to work by once the light had gone.", hint: lit ? "Click to snuff it" : "Click to light it" })} onClick={click(() => setLit((l) => !l))}>
      <Parts parts={stick} thickness={0.004} />
      <group ref={flame} position={[0, 0.11, 0]}>
        <mesh position-y={0.014} raycast={() => null}>
          <coneGeometry args={[0.008, 0.03, 10]} />
          <meshBasicMaterial color="#ffb347" toneMapped={false} />
        </mesh>
        <mesh position-y={0.01} raycast={() => null}>
          <coneGeometry args={[0.0045, 0.016, 8]} />
          <meshBasicMaterial color="#fff4c9" toneMapped={false} />
        </mesh>
      </group>
    </group>
  );
}
