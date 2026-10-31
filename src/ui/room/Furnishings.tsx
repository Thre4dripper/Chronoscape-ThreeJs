import { useEffect, useMemo, useRef, useState } from "react";
import { useFrame, type ThreeEvent } from "@react-three/fiber";
import * as THREE from "three";
import { B, type Part } from "./Cabinet";
import { ATLAS_TABLES, atlasSpreadTexture, portolanTexture, worldMapTexture } from "./charts";
import { Astrolabe, CelestialGlobe, CrossStaff, Dividers, Parts, Quadrant, Sandglass, tint, useParts } from "./Instruments";
import { BRASS, GILT, PAPER_T, toonGradient, WOOD, WOOD_DARK, WOOD_LIGHT } from "./toon";
import { tipHandlers, useRoom } from "./roomState";

/**
 * The rest of the map room, for the wall either side of the cabinet: a
 * barrel of rolled charts, a plan chest with the instruments set out on it, a
 * lectern with an atlas lying open, a Dutch world map tacked to the wall
 * with its corners curling, a portolan chart on its calfskin, a sea chest
 * with a cross-staff leaning by it, and books and scrolls piled on the floor.
 * Most of it lies beyond the part of the room the camera frames, so it shows
 * on wide screens and is hidden behind the label on narrower ones; nothing
 * stands in front of the cabinet, the desk or the pictures.
 */
type V3 = [number, number, number];
const IRON = "#3b332c";
const PAPERS = ["#efe0bd", "#e6d2a4", "#f4e8cb", "#dcc493", "#e9d9b0"];
const TIES = ["#8a2f24", "#2f5a46", "#3c4a66", "#b07a2a"];
const BOOKS = ["#4f6b4a", "#7a2f22", "#3c4a66", "#6b4a2a", "#5a2f3e"];

function rng(seed: number) {
  let s = seed;
  return () => ((s = (s * 16807) % 2147483647) / 2147483647);
}

/** A rolled map from `from` along `axis`: the roll, its darker rolled ends, maybe a tie, maybe wooden rollers. */
type Roll = { from: THREE.Vector3; axis: THREE.Vector3; len: number; r: number; paper: string; tie?: string; tieAt?: number; knobs?: boolean };
function rollParts(P: Part[], s: Roll, local = false) {
  // (local: upright at the origin, for a roll that is placed and moved on its own)
  const m = local ? new THREE.Matrix4() : new THREE.Matrix4().compose(s.from, new THREE.Quaternion().setFromUnitVectors(new THREE.Vector3(0, 1, 0), s.axis), new THREE.Vector3(1, 1, 1));
  const at = (g: THREE.BufferGeometry) => g.applyMatrix4(m);
  P.push({ g: at(new THREE.CylinderGeometry(s.r, s.r, s.len, 10).translate(0, s.len / 2, 0)), c: s.paper, o: true });
  P.push({ g: at(new THREE.CylinderGeometry(s.r * 0.55, s.r * 0.55, s.len + 0.01, 7).translate(0, s.len / 2, 0)), c: "#b89a66" });
  if (s.tie) P.push({ g: at(new THREE.CylinderGeometry(s.r + 0.005, s.r + 0.005, 0.03, 10).translate(0, s.len * (s.tieAt ?? 0.5), 0)), c: s.tie });
  if (s.knobs)
    for (const y of [-0.03, s.len + 0.03]) {
      P.push({ g: at(new THREE.CylinderGeometry(s.r * 0.5, s.r * 0.5, 0.06, 7).translate(0, y, 0)), c: WOOD_DARK });
      P.push({ g: at(new THREE.SphereGeometry(s.r * 0.6, 7, 5).translate(0, y + Math.sign(y) * 0.035, 0)), c: WOOD_DARK });
    }
}
/** A roll lying on its side on a surface at height y, pointing along `yaw` (0 = along x). */
function lying(x: number, y: number, z: number, yaw: number, len: number, r: number, paper: string, tie?: string, knobs?: boolean): Roll {
  const axis = new THREE.Vector3(Math.cos(yaw), 0, -Math.sin(yaw));
  return { from: new THREE.Vector3(x, y + r, z).addScaledVector(axis, -len / 2), axis, len, r, paper, tie, knobs };
}
/** A pile of books lying flat, each with a page block and a gilt band on its spine. */
function bookParts(P: Part[], x: number, y0: number, z: number, books: { w: number; d: number; h: number; c: string; r: number }[]) {
  let y = y0;
  for (const b of books) {
    const m = new THREE.Matrix4().compose(new THREE.Vector3(x, y + b.h / 2, z), new THREE.Quaternion().setFromAxisAngle(new THREE.Vector3(0, 1, 0), b.r), new THREE.Vector3(1, 1, 1));
    P.push({ g: new THREE.BoxGeometry(b.w, b.h, b.d).applyMatrix4(m), c: b.c, o: true });
    P.push({ g: new THREE.BoxGeometry(b.w - 0.03, b.h - 0.018, b.d + 0.004).translate(0.012, 0, 0).applyMatrix4(m), c: "#efe0bd" });
    P.push({ g: new THREE.BoxGeometry(0.006, b.h * 0.3, b.d * 0.7).translate(-b.w / 2 - 0.002, 0, 0).applyMatrix4(m), c: GILT });
    y += b.h;
  }
  return y;
}

export function Furnishings({ cabW, desk }: { cabW: number; desk: THREE.Vector3 }) {
  const L = -cabW / 2; // the cabinet's left side
  const R = desk.x + 1.25; // the desk's right end
  return (
    <>
      <ScrollStand at={[L - 0.7, 0, 0.5]} />
      <PlanChest at={[L - 2.3, 0, -0.215]} />
      <Lectern at={[L - 4.15, 0, 0.3]} />
      <WallMap kind="world" at={[L - 3.45, 3.85, -0.578]} w={3.0} h={1.97} />
      <WallMap kind="portolan" at={[R + 2.75, 3.65, -0.578]} w={1.72} h={1.15} />
      <SeaChest at={[R + 2.55, 0, -0.3]} />
      <CrossStaff at={[R + 3.45, 0, -0.2]} lean={0.248} />
      <FloorPiles desk={desk} L={L} R={R} />
      {/* only the widest screens reach these */}
      <MapRack at={[L - 6.1, 0, -0.39]} />
      <CelestialGlobe at={[R + 4.15, 0, 0.3]} />
      <Bookcase at={[R + 5.75, 0, -0.4]} />
    </>
  );
}

/* ------------------------------------------------------------------ a barrel of rolled charts */

const BARREL_H = 0.72;
/** Rolls that can be drawn out of the barrel, by their index. */
const LIFTS = [3, 6, 8]; // (the ones on the side toward the room)

function ScrollStand({ at }: { at: V3 }) {
  const rolls = useMemo(() => {
    const r = rng(11);
    const n = 11;
    return Array.from({ length: n }, (_, i): Roll => {
      const a = i * 2.39996 + 0.3;
      const rr = 0.03 + r() * 0.02;
      // fanned out: each roll leans from near the middle of the floor to its place at the rim
      const rim = Math.min(0.21 * Math.sqrt((i + 0.5) / n), 0.215 - rr);
      const from = new THREE.Vector3(Math.cos(a) * rim * 0.3, 0.06, Math.sin(a) * rim * 0.3);
      const axis = new THREE.Vector3(Math.cos(a) * rim, BARREL_H, Math.sin(a) * rim).sub(from).normalize();
      const k = r();
      return { from, axis, len: 0.9 + r() * 0.55, r: rr, paper: PAPERS[i % PAPERS.length], tie: k < 0.55 ? TIES[i % TIES.length] : undefined, tieAt: 0.62 + r() * 0.2, knobs: k > 0.75 };
    });
  }, []);
  const parts = useParts(() => {
    const P: Part[] = [];
    // the barrel: staves (a faceted lathe), iron hoops, and darkness inside
    const lathe = new THREE.LatheGeometry(([[0.235, 0], [0.268, 0.18], [0.278, 0.36], [0.268, 0.54], [0.25, BARREL_H], [0.228, BARREL_H], [0.24, BARREL_H - 0.08]] as [number, number][]).map(([x, y]) => new THREE.Vector2(x, y)), 14);
    const staves = lathe.toNonIndexed();
    lathe.dispose();
    staves.computeVertexNormals();
    P.push({ g: staves, c: WOOD_LIGHT, o: true });
    P.push({ g: new THREE.CylinderGeometry(0.236, 0.236, 0.01, 14).translate(0, BARREL_H - 0.12, 0), c: "#2a170c" });
    for (const [y, rad] of [[0.05, 0.248], [0.16, 0.272], [0.58, 0.272]]) P.push({ g: new THREE.TorusGeometry(rad, 0.012, 5, 28).rotateX(Math.PI / 2).translate(0, y, 0), c: IRON });
    rolls.forEach((s, i) => !LIFTS.includes(i) && rollParts(P, s));
    return P;
  });
  const lifted = useMemo(() => LIFTS.map((i) => {
    const P: Part[] = [];
    rollParts(P, rolls[i], true);
    // drawn out until its top stands well clear of the tallest roll
    const by = Math.max(0.5, 1.95 - rolls[i].from.y - rolls[i].len);
    return { parts: tint(P), q: new THREE.Quaternion().setFromUnitVectors(new THREE.Vector3(0, 1, 0), rolls[i].axis), from: rolls[i].from, by };
  }), [rolls]);
  useEffect(() => () => lifted.forEach((l) => l.parts.forEach((p) => p.geom.dispose())), [lifted]);
  const refs = useRef<(THREE.Group | null)[]>([]);
  const s = useRef({ t: -1, which: 0 });
  useFrame((_, dt) => {
    const q = s.current;
    if (q.t < 0) return;
    q.t += Math.min(dt, 0.05);
    const o = refs.current[q.which];
    // drawn out, turned in the hand to look at it, and slid back
    const k = Math.min(1, q.t / 0.5) ** 0.5 * (1 - smooth((q.t - 1.4) / 0.6));
    if (o) {
      o.position.y = k * lifted[q.which].by;
      o.rotation.y = k * Math.sin(q.t * 2.2) * 0.6;
    }
    if (q.t > 2.0) {
      if (o) o.position.y = o.rotation.y = 0;
      q.t = -1;
    }
  });
  return (
    <group
      position={at}
      {...tipHandlers({ title: "A stand of rolled charts", text: "Sea charts and town plans were kept rolled like these, and only unrolled on a table under weights to be read.", hint: "Click to draw one out" })}
      onClick={(e: ThreeEvent<MouseEvent>) => {
        e.stopPropagation();
        const q = s.current;
        if (q.t >= 0) return;
        q.which = (q.which + 1) % LIFTS.length;
        q.t = 0;
      }}
    >
      <Parts parts={parts} shadow thickness={0.007} />
      {lifted.map((l, i) => (
        <group key={i} position={l.from} quaternion={l.q}>
          <group ref={(g) => void (refs.current[i] = g)}>
            <Parts parts={l.parts} />
          </group>
        </group>
      ))}
    </group>
  );
}
const smooth = (x: number) => (x <= 0 ? 0 : x >= 1 ? 1 : x * x * (3 - 2 * x));

/* ------------------------------------------------------------------ plan chest, with the instruments on top */

const CHEST_W = 1.9, CHEST_D = 0.72, CHEST_TOP = 0.85;

function PlanChest({ at }: { at: V3 }) {
  const W = CHEST_W, D = CHEST_D, front = D / 2;
  const drawerY = (i: number) => 0.71 - i * 0.15;
  const parts = useParts(() => {
    const P: Part[] = [];
    for (const sx of [-1, 1])
      for (const sz of [-1, 1]) P.push({ g: new THREE.LatheGeometry(([[0, 0], [0.06, 0.005], [0.07, 0.04], [0.055, 0.075], [0, 0.08]] as [number, number][]).map(([r, y]) => new THREE.Vector2(r, y)), 10).translate(sx * (W / 2 - 0.1), 0, sz * (D / 2 - 0.1)), c: WOOD_DARK });
    P.push({ g: B(W, 0.08, D, 0, 0.12, 0), c: WOOD_DARK, o: true });
    P.push({ g: B(W - 0.04, 0.66, D - 0.02, 0, 0.49, -0.01), c: WOOD, o: true });
    P.push({ g: B(W + 0.08, 0.05, D + 0.06, 0, CHEST_TOP - 0.025, 0), c: WOOD_DARK, o: true });
    // three fixed drawers (the top one opens), each with two brass pulls and a label frame
    for (let i = 1; i < 4; i++) drawerFront(P, W, drawerY(i), front);
    // on the top: rolled maps lying at the back, a pair of books
    const rolls = [lying(-0.62, CHEST_TOP, -0.25, 0.04, 0.82, 0.045, PAPERS[0], TIES[0]), lying(-0.5, CHEST_TOP, -0.16, -0.06, 0.66, 0.04, PAPERS[3]), lying(-0.56, CHEST_TOP + 0.075, -0.205, 0.1, 0.74, 0.038, PAPERS[2], TIES[2], true)];
    rolls.forEach((r) => rollParts(P, r));
    bookParts(P, 0.72, CHEST_TOP, -0.15, [
      { w: 0.42, d: 0.3, h: 0.07, c: BOOKS[3], r: 0.12 },
      { w: 0.36, d: 0.27, h: 0.06, c: BOOKS[0], r: -0.05 },
    ]);
    return P;
  });
  const drawer = useParts(() => {
    const P: Part[] = [];
    drawerFront(P, W, 0, front);
    const dw = W - 0.2, dd = 0.62;
    P.push({ g: B(dw, 0.012, dd, 0, -0.055, front - dd / 2), c: WOOD_LIGHT });
    for (const sx of [-1, 1]) P.push({ g: B(0.015, 0.1, dd, sx * (dw / 2), -0.01, front - dd / 2), c: WOOD });
    // sheets lying flat inside: engraved plates waiting for the colourist
    [PAPERS[2], PAPERS[0], PAPERS[1]].forEach((c, k) => P.push({ g: B(dw * 0.86 - k * 0.06, 0.006, 0.5, 0, 0, 0).rotateY((k - 1) * 0.04).translate((k - 1) * 0.05, -0.045 + k * 0.007, front - 0.3), c }));
    return P;
  });
  const g = useRef<THREE.Group>(null);
  const [open, setOpen] = useState(false);
  const moving = useRef(false);
  useFrame((_, dt) => {
    if (!moving.current || !g.current) return;
    const want = open ? 0.36 : 0;
    g.current.position.z += (want - g.current.position.z) * (1 - Math.exp(-8 * Math.min(dt, 0.05)));
    if (Math.abs(want - g.current.position.z) < 1e-3) ((g.current.position.z = want), (moving.current = false));
  });
  return (
    <group position={at}>
      <group
        {...tipHandlers({ title: "A plan chest", text: "Wide, shallow drawers keep big sheets flat: engraved plates, sea charts and town plans waiting for the colourist.", hint: open ? "Click to close the drawer" : "Click to open the top drawer" })}
        onClick={(e: ThreeEvent<MouseEvent>) => {
          e.stopPropagation();
          setOpen(!open);
          moving.current = true;
          useRoom.getState().setTip({ title: "A plan chest", text: "Wide, shallow drawers keep big sheets flat: engraved plates, sea charts and town plans waiting for the colourist.", hint: open ? "Click to open the top drawer" : "Click to close the drawer" });
        }}
      >
        <Parts parts={parts} shadow thickness={0.008} />
        <group ref={g} position={[0, drawerY(0), 0]}>
          <Parts parts={drawer} thickness={0.008} />
        </group>
      </group>
      {/* the instruments, each with its own trick */}
      <Quadrant at={[-0.72, CHEST_TOP, 0.06]} />
      <Sandglass at={[-0.22, CHEST_TOP, 0.12]} />
      <Astrolabe at={[0.2, CHEST_TOP, -0.12]} />
      <Dividers at={[0.62, CHEST_TOP, 0.2]} ry={-0.2} />
    </group>
  );
}

function drawerFront(P: Part[], W: number, y: number, front: number) {
  P.push({ g: B(W - 0.14, 0.13, 0.03, 0, y, front + 0.005), c: WOOD_LIGHT, o: true });
  for (const sx of [-1, 1]) P.push({ g: B(0.11, 0.022, 0.025, sx * W * 0.27, y - 0.015, front + 0.03), c: BRASS });
  P.push({ g: B(0.13, 0.05, 0.008, 0, y + 0.02, front + 0.022), c: GILT });
}

/* ------------------------------------------------------------------ lectern with an open atlas */

function Lectern({ at }: { at: V3 }) {
  // a few tables of the atlas, a spread each, drawn once
  const [texs, setTexs] = useState<THREE.CanvasTexture[] | null>(null);
  useEffect(() => {
    let alive = true;
    void Promise.all(Array.from({ length: ATLAS_TABLES }, (_, i) => atlasSpreadTexture(i))).then((ts) => (alive ? setTexs(ts) : ts.forEach((t) => t.dispose())));
    return () => {
      alive = false;
    };
  }, []);
  useEffect(() => () => texs?.forEach((t) => t.dispose()), [texs]);
  const TOP = 1.05, TILT = 0.42, BW = 0.74, BD = 0.48;
  const HW = (BW - 0.06) / 2, PD = BD - 0.04;
  const parts = useParts(() => {
    const P: Part[] = [
      { g: new THREE.LatheGeometry(([[0, 0], [0.27, 0], [0.28, 0.04], [0.2, 0.08], [0.08, 0.13], [0.05, 0.3], [0.07, 0.52], [0.045, 0.82], [0.065, 0.95], [0.1, TOP - 0.02], [0, TOP - 0.02]] as [number, number][]).map(([r, y]) => new THREE.Vector2(r, y)), 14), c: WOOD, o: true },
    ];
    return P;
  });
  // the slanted desk and the book on it, in the desk's own frame (tilted toward the viewer)
  const top = useParts(() => [
    { g: B(BW + 0.06, 0.03, BD + 0.04, 0, 0, 0), c: WOOD_DARK, o: true },
    { g: B(BW + 0.06, 0.05, 0.03, 0, 0.03, BD / 2 + 0.03), c: WOOD_DARK, o: true },
    // the open book: boards, and the two page blocks rising from the gutter
    { g: B(BW, 0.016, BD, 0, 0.023, 0), c: "#7a2f22", o: true },
    { g: B(BW / 2 - 0.03, 0.03, BD - 0.03, -BW / 4 + 0.005, 0.045, 0), c: PAPER_T },
    { g: B(BW / 2 - 0.03, 0.03, BD - 0.03, BW / 4 - 0.005, 0.045, 0), c: PAPER_T },
  ]);
  // each page swells up from the gutter and settles at its edge
  const swell = (r: number) => 0.022 * Math.pow(Math.max(0, Math.sin((Math.PI * Math.abs(r)) / HW)), 0.7);
  const halves = useMemo(
    () =>
      [-1, 1].map((side) => {
        const g = new THREE.PlaneGeometry(HW, PD, 10, 1).rotateX(-Math.PI / 2).translate((side * HW) / 2, 0, 0);
        const p = g.attributes.position as THREE.BufferAttribute, uv = g.attributes.uv as THREE.BufferAttribute;
        for (let i = 0; i < p.count; i++) {
          p.setY(i, 0.062 + swell(p.getX(i)));
          uv.setX(i, 0.5 + (0.5 * p.getX(i)) / HW);
        }
        g.computeVertexNormals();
        return g;
      }),
    [], // eslint-disable-line react-hooks/exhaustive-deps
  );
  useEffect(() => () => halves.forEach((g) => g.dispose()), [halves]);
  // the spread asked for, the one the landed leaves show, and the leaves in the air (click fast and several turn at once)
  const [target, setTarget] = useState(0);
  const [settled, setSettled] = useState(0);
  const [leaves, setLeaves] = useState<number[]>([]);
  const n = texs?.length ?? 1;
  const turn = () => {
    if (!texs) return;
    setLeaves((ls) => [...ls, target]);
    setTarget((x) => x + 1);
  };
  const land = (from: number) => {
    setLeaves((ls) => ls.filter((l) => l !== from));
    setSettled(from + 1);
  };
  const pageMat = (i: number) => (texs ? <meshToonMaterial key={i % n} map={texs[i % n]} gradientMap={toonGradient()} /> : <meshToonMaterial color={PAPER_T} gradientMap={toonGradient()} />);
  return (
    <group position={at} rotation={[0, 0.25, 0]} {...tipHandlers({ title: "An atlas lying open", text: "Ortelius's Theatrum Orbis Terrarum of 1570 was the first modern atlas: maps of the whole world drawn to one plan and bound in one book.", hint: "Click to turn a page" })} onClick={(e: ThreeEvent<MouseEvent>) => (e.stopPropagation(), turn())}>
      <Parts parts={parts} thickness={0.008} />
      <group position={[0, TOP + 0.02, 0]} rotation={[TILT, 0, 0]}>
        <Parts parts={top} thickness={0.006} />
        {/* the left page is the last leaf landed, the right the spread being turned to */}
        <mesh geometry={halves[0]}>{pageMat(settled)}</mesh>
        <mesh geometry={halves[1]}>{pageMat(target)}</mesh>
        {texs && leaves.map((from, k) => <AtlasLeaf key={from} front={texs[from % n]} back={texs[(from + 1) % n]} hw={HW} pd={PD} swell={swell} lift={0.0015 * (k + 1)} onDone={() => land(from)} />)}
      </group>
    </group>
  );
}

/**
 * One leaf of the lectern's atlas turning from right to left about the gutter: its face is the right
 * half of this spread, its back the left half of the next. It keeps the pages' swell, flattening as
 * it stands up and bowing the other way as it comes down, so it lies exactly on each page at the ends.
 */
function AtlasLeaf({ front, back, hw, pd, swell, lift, onDone }: { front: THREE.Texture; back: THREE.Texture; hw: number; pd: number; swell: (r: number) => number; lift: number; onDone: () => void }) {
  const SEG = 16;
  const [geoF, geoB] = useMemo(() => {
    const uvF: number[] = [], uvB: number[] = [], iF: number[] = [], iB: number[] = [];
    for (let i = 0; i <= SEG; i++)
      for (let j = 0; j < 2; j++) {
        uvF.push(0.5 + (0.5 * i) / SEG, 1 - j);
        uvB.push(0.5 - (0.5 * i) / SEG, 1 - j);
      }
    for (let i = 0; i < SEG; i++) {
      const a = 2 * i, b = a + 1, c = a + 2, d = a + 3;
      iF.push(a, b, c, c, b, d);
      iB.push(a, c, b, c, d, b);
    }
    const pos = new THREE.BufferAttribute(new Float32Array((SEG + 1) * 2 * 3), 3);
    const make = (uv: number[], idx: number[]) => {
      const g = new THREE.BufferGeometry();
      g.setAttribute("position", pos);
      g.setAttribute("uv", new THREE.Float32BufferAttribute(uv, 2));
      g.setIndex(idx);
      return g;
    };
    return [make(uvF, iF), make(uvB, iB)];
  }, []);
  useEffect(() => () => (geoF.dispose(), geoB.dispose()), [geoF, geoB]);
  const t = useRef(0);
  const done = useRef(false);
  useFrame((_, dt) => {
    t.current = Math.min(1, t.current + Math.min(dt, 0.05) / 0.9);
    const th = Math.PI * smooth(t.current), c = Math.cos(th), s = Math.sin(th);
    const p = geoF.attributes.position as THREE.BufferAttribute;
    for (let i = 0; i <= SEG; i++) {
      const r = (hw * i) / SEG, h = swell(r) * c + lift;
      for (let j = 0; j < 2; j++) p.setXYZ(2 * i + j, r * c - h * s, 0.062 + r * s + h * c, -pd / 2 + pd * j);
    }
    p.needsUpdate = true;
    geoF.computeVertexNormals();
    geoB.computeVertexNormals();
    geoF.computeBoundingSphere();
    if (t.current >= 1 && !done.current) {
      done.current = true;
      onDone();
    }
  });
  return (
    <>
      <mesh geometry={geoF} frustumCulled={false}>
        <meshToonMaterial map={front} gradientMap={toonGradient()} />
      </mesh>
      <mesh geometry={geoB} frustumCulled={false}>
        <meshToonMaterial map={back} gradientMap={toonGradient()} />
      </mesh>
    </>
  );
}

/* ------------------------------------------------------------------ maps on the wall */

/** A sheet with gently cockled paper and some corners curling away from the wall. */
function sheetGeometry(w: number, h: number, curls: { sx: number; sy: number; reach: number; r: number }[], sx = 40, sy = 26) {
  const g = new THREE.PlaneGeometry(w, h, sx, sy);
  const p = g.attributes.position as THREE.BufferAttribute;
  for (let i = 0; i < p.count; i++) {
    let x = p.getX(i), y = p.getY(i);
    let z = 0.006 * Math.sin(x * 6.3 + 1) * Math.sin(y * 4.1 + 0.4);
    for (const c of curls) {
      // past a fold line across the corner the paper rolls round a small cylinder, off the wall
      const dx = -c.sx * Math.SQRT1_2, dy = -c.sy * Math.SQRT1_2;
      const d = (x - (c.sx * w) / 2) * dx + (y - (c.sy * h) / 2) * dy;
      const s = c.reach - d;
      if (s > 0) {
        const th = s / c.r;
        const back = s - c.r * Math.sin(th);
        x += dx * back;
        y += dy * back;
        z += c.r * (1 - Math.cos(th));
      }
    }
    p.setXYZ(i, x, y, z);
  }
  g.computeVertexNormals();
  return g;
}

/** A map tacked to the wall by its top edge (at = the middle of that edge); it lifts in the draught when pointed at. */
function WallMap({ kind, at, w, h }: { kind: "world" | "portolan"; at: V3; w: number; h: number }) {
  const [tex, setTex] = useState<THREE.CanvasTexture | null>(null);
  useEffect(() => {
    let alive = true;
    void (kind === "world" ? worldMapTexture() : portolanTexture()).then((t) => (alive ? setTex(t) : t.dispose()));
    return () => {
      alive = false;
    };
  }, [kind]);
  useEffect(() => () => tex?.dispose(), [tex]);
  const geo = useMemo(
    () =>
      kind === "world"
        ? sheetGeometry(w, h, [
            { sx: -1, sy: -1, reach: 0.26, r: 0.06 },
            { sx: 1, sy: -1, reach: 0.34, r: 0.07 },
            { sx: 1, sy: 1, reach: 0.12, r: 0.05 },
          ])
        : sheetGeometry(w, h, [], 16, 10),
    [kind, w, h],
  );
  useEffect(() => () => geo.dispose(), [geo]);
  const swing = useRef({ a: 0, v: 0, hot: false, live: false });
  const g = useRef<THREE.Group>(null);
  useFrame((_, dtRaw) => {
    const q = swing.current;
    if (!q.live || !g.current) return;
    const dt = Math.min(dtRaw, 0.05);
    // a damped spring about the tacked top edge, lifted a little off the wall while pointed at
    q.v += ((q.hot ? -0.035 : 0) - q.a) * 30 * dt - q.v * 3.2 * dt;
    q.a = Math.min(0.004, q.a + q.v * dt);
    g.current.rotation.x = q.a;
    if (!q.hot && Math.abs(q.a) + Math.abs(q.v) < 1e-4) ((q.live = false), (g.current.rotation.x = 0));
  });
  const tip =
    kind === "world"
      ? { title: "A wall map of the world", text: "Amsterdam's map makers, the Blaeus and Hondius, sold great world maps like this to hang in merchants' houses, the seas full of ships and monsters." }
      : { title: "A portolan chart", text: "Drawn on a calfskin from sailors' compass bearings, with rhumb lines fanning out from the wind roses: the working charts of the Mediterranean from the 1300s on." };
  const h_ = tipHandlers(tip, "default");
  const tacks: [number, number][] = kind === "world" ? [[-w / 2 + 0.06, -0.06], [0, -0.05], [w / 2 - 0.09, -0.12], [-w / 2 + 0.07, -h + 0.32]] : [[-w / 2 + 0.22, -0.06], [w / 2 - 0.06, -0.06], [-w / 2 + 0.05, -h / 2], [w / 2 - 0.06, -h + 0.06], [-w / 2 + 0.22, -h + 0.07]];
  const tackParts = useParts(() => tacks.map(([x, y]) => ({ g: new THREE.SphereGeometry(0.022, 8, 6).translate(x, y, 0.012), c: BRASS })), [kind, w, h]);
  return (
    <group position={at}>
      <group
        ref={g}
        onPointerOver={(e: ThreeEvent<PointerEvent>) => {
          h_.onPointerOver(e);
          swing.current.hot = swing.current.live = true;
        }}
        onPointerOut={() => {
          h_.onPointerOut();
          swing.current.hot = false;
        }}
      >
        <mesh geometry={geo} position={[0, -h / 2, 0]}>
          <meshToonMaterial key={tex ? "map" : "blank"} map={tex} color={tex ? "#ffffff" : PAPER_T} gradientMap={toonGradient()} transparent={kind === "portolan"} alphaTest={kind === "portolan" ? 0.5 : 0} />
        </mesh>
        {kind === "world" && (
          <mesh geometry={geo} position={[0, -h / 2, 0]} material={backPaper()} />
        )}
        <Parts parts={tackParts} />
      </group>
    </group>
  );
}
let back: THREE.MeshToonMaterial | null = null;
/** The back of a sheet, seen where its corners curl over. */
const backPaper = () => (back ??= new THREE.MeshToonMaterial({ color: "#d9c393", gradientMap: toonGradient(), side: THREE.BackSide }));

/* ------------------------------------------------------------------ the sea chest, and the piles on the floor */

function SeaChest({ at }: { at: V3 }) {
  const W = 1.15, H = 0.5, D = 0.55;
  const parts = useParts(() => {
    const P: Part[] = [
      { g: B(W, H - 0.08, D, 0, (H - 0.08) / 2 + 0.02, 0), c: WOOD, o: true },
      { g: B(W + 0.04, 0.09, D + 0.04, 0, H - 0.02, 0), c: WOOD_DARK, o: true },
      { g: B(W + 0.02, 0.03, D + 0.02, 0, 0.02, 0), c: WOOD_DARK },
      { g: B(0.1, 0.12, 0.02, 0, H - 0.1, D / 2 + 0.02), c: BRASS, o: true },
    ];
    // iron straps over the lid and down the front, rope handles at the ends
    for (const sx of [-1, 1]) {
      P.push({ g: B(0.05, H + 0.005, 0.012, sx * 0.36, H / 2 + 0.005, D / 2 + 0.022), c: IRON });
      P.push({ g: B(0.05, 0.012, D + 0.05, sx * 0.36, H + 0.03, 0), c: IRON });
      P.push({ g: new THREE.TorusGeometry(0.07, 0.014, 5, 14, Math.PI).rotateY(Math.PI / 2).rotateX(Math.PI).translate(sx * (W / 2 + 0.01), H - 0.14, 0), c: "#a88a5a" });
    }
    // on the lid: books and two tied charts
    const lid = H + 0.025;
    bookParts(P, -0.25, lid, 0.0, [
      { w: 0.46, d: 0.34, h: 0.08, c: BOOKS[2], r: 0.06 },
      { w: 0.42, d: 0.3, h: 0.06, c: BOOKS[4], r: -0.1 },
      { w: 0.36, d: 0.26, h: 0.07, c: BOOKS[0], r: 0.15 },
    ]);
    rollParts(P, lying(0.28, lid, -0.06, 0.15, 0.62, 0.045, PAPERS[1], TIES[3]));
    rollParts(P, lying(0.3, lid, 0.07, 0.08, 0.56, 0.04, PAPERS[4], TIES[1]));
    return P;
  });
  return (
    <group position={at} {...tipHandlers({ title: "A sea chest", text: "A navigator's chest: his charts, a rutter of sailing directions and the instruments of his trade went to sea in it."}, "default")}>
      <Parts parts={parts} thickness={0.008} />
    </group>
  );
}

/** Books and scrolls on the floor: under the desk, in front of the barrel, and by the sea chest. */
function FloorPiles({ desk, L, R }: { desk: THREE.Vector3; L: number; R: number }) {
  const under = useParts(() => {
    const P: Part[] = [];
    bookParts(P, desk.x - 0.55, 0, desk.z - 0.15, [
      { w: 0.5, d: 0.36, h: 0.09, c: BOOKS[1], r: 0.05 },
      { w: 0.46, d: 0.34, h: 0.08, c: BOOKS[3], r: -0.12 },
      { w: 0.44, d: 0.3, h: 0.07, c: BOOKS[2], r: 0.1 },
      { w: 0.38, d: 0.27, h: 0.06, c: BOOKS[0], r: -0.04 },
    ]);
    rollParts(P, lying(desk.x + 0.3, 0, desk.z - 0.05, 0.25, 0.85, 0.05, PAPERS[2], TIES[0]));
    rollParts(P, lying(desk.x + 0.36, 0, desk.z + 0.08, 0.18, 0.7, 0.045, PAPERS[3]));
    return P;
  }, [desk.x, desk.z]);
  const rolled = useParts(() => {
    const P: Part[] = [];
    rollParts(P, lying(L - 0.95, 0, 1.0, -0.35, 0.8, 0.045, PAPERS[1], TIES[2], true));
    bookParts(P, L - 1.55, 0, 0.75, [
      { w: 0.44, d: 0.32, h: 0.08, c: BOOKS[4], r: -0.2 },
      { w: 0.4, d: 0.3, h: 0.07, c: BOOKS[1], r: 0.05 },
    ]);
    // three tied rolls stacked like logs
    rollParts(P, lying(R + 1.35, 0, 0.75, 0.3, 0.9, 0.05, PAPERS[0], TIES[1]));
    rollParts(P, lying(R + 1.39, 0, 0.87, 0.26, 0.8, 0.05, PAPERS[3], TIES[0]));
    rollParts(P, lying(R + 1.37, 0.085, 0.81, 0.28, 0.85, 0.045, PAPERS[2], undefined, true));
    return P;
  }, [L, R]);
  const tip = tipHandlers({ title: "Waiting for the shelf", text: "Sailing directions, a herbal and a town chronicle: a map room always gathers more books than it has shelves." }, "default");
  const rolls = tipHandlers({ title: "Rolled charts", text: "Tied with tape until they were wanted, so the paper kept its curl and the sea air kept out." }, "default");
  return (
    <>
      <group {...tip}>
        <Parts parts={under} thickness={0.006} />
      </group>
      <group {...rolls}>
        <Parts parts={rolled} thickness={0.006} />
      </group>
    </>
  );
}

/* ------------------------------------------------------------------ the map rack and the bookcase, at the far ends */

/** Pigeonholes of rolled maps, their ends showing, as in a chart seller's shop. */
function MapRack({ at }: { at: V3 }) {
  const W = 1.5, H = 2.3, D = 0.4, cols = 4, rows = 5;
  const parts = useParts(() => {
    const P: Part[] = [
      { g: B(W, H, 0.03, 0, H / 2, -D / 2 + 0.015), c: WOOD_DARK },
      { g: B(W + 0.06, 0.14, D + 0.04, 0, 0.07, 0), c: WOOD_DARK, o: true },
      { g: B(W + 0.08, 0.06, D + 0.06, 0, H + 0.03, 0.01), c: WOOD, o: true },
      { g: B(W + 0.16, 0.06, D + 0.12, 0, H + 0.09, 0.02), c: WOOD_DARK, o: true },
      { g: B(W + 0.17, 0.014, 0.01, 0, H + 0.07, D / 2 + 0.081), c: GILT },
    ];
    for (const sx of [-1, 1]) P.push({ g: B(0.05, H - 0.14, D, sx * (W / 2 - 0.025), 0.14 + (H - 0.14) / 2, 0), c: WOOD, o: true });
    const x0 = -W / 2 + 0.05, cw = (W - 0.1) / cols, y0 = 0.14, ch = (H - 0.14) / rows;
    for (let r = 0; r <= rows; r++) P.push({ g: B(W - 0.1, 0.03, D - 0.01, 0, y0 + r * ch - (r === rows ? 0.015 : 0), 0), c: WOOD_LIGHT, o: r === 0 });
    for (let c = 1; c < cols; c++) P.push({ g: B(0.03, H - 0.14, D - 0.01, x0 + c * cw, y0 + (H - 0.14) / 2, 0), c: WOOD_LIGHT });
    // two to four rolls in each hole, ends out, lying on the shelf or on each other
    const rnd = rng(53);
    const axis = new THREE.Vector3(0, 0, 1);
    for (let r = 0; r < rows; r++)
      for (let c = 0; c < cols; c++) {
        const n = 2 + Math.floor(rnd() * 3);
        const left = x0 + c * cw + 0.03;
        let x = left;
        for (let k = 0; k < n; k++) {
          const rr = 0.032 + rnd() * 0.02;
          const stack = k === n - 1 && n > 2;
          const cx = stack ? left + cw * 0.35 : x + rr;
          if (!stack) x += rr * 2 + 0.004;
          if (cx + rr > left + cw - 0.06) continue;
          const y = y0 + r * ch + 0.015 + rr + (stack ? 0.06 : 0);
          rollParts(P, { from: new THREE.Vector3(cx, y, -D / 2 + 0.04), axis, len: D - 0.02 + rnd() * 0.06, r: rr, paper: PAPERS[Math.floor(rnd() * PAPERS.length)], tie: rnd() < 0.35 ? TIES[Math.floor(rnd() * TIES.length)] : undefined, tieAt: 0.85 });
        }
        // a paper label tacked under each hole
        P.push({ g: B(0.12, 0.035, 0.006, x0 + c * cw + cw / 2, y0 + r * ch - 0.0, D / 2 + 0.005), c: PAPER_T });
      }
    return P;
  });
  return (
    <group position={at} {...tipHandlers({ title: "A map rack", text: "Pigeonholes of rolled maps, each hole labelled by region: how a chart seller's shop kept its stock."}, "default")}>
      <Parts parts={parts} thickness={0.008} />
    </group>
  );
}

/** A tall bookcase of pilots' books and atlases, a few lying flat, a roll or two on top. */
function Bookcase({ at }: { at: V3 }) {
  const W = 1.4, H = 2.2, D = 0.36, shelves = 4;
  const parts = useParts(() => {
    const P: Part[] = [
      { g: B(W, H, 0.03, 0, H / 2, -D / 2 + 0.015), c: WOOD_DARK },
      { g: B(W + 0.06, 0.12, D + 0.04, 0, 0.06, 0), c: WOOD_DARK, o: true },
      { g: B(W + 0.14, 0.07, D + 0.1, 0, H + 0.035, 0.02), c: WOOD_DARK, o: true },
    ];
    for (const sx of [-1, 1]) P.push({ g: B(0.06, H - 0.12, D, sx * (W / 2 - 0.03), 0.12 + (H - 0.12) / 2, 0), c: WOOD, o: true });
    const inner = W - 0.12, sh = (H - 0.12) / shelves;
    const rnd = rng(71);
    for (let i = 0; i < shelves; i++) {
      const y = 0.12 + i * sh;
      P.push({ g: B(inner, 0.035, D - 0.02, 0, y + 0.0175, 0), c: WOOD_LIGHT, o: true });
      // a row of books standing, one leaning at the end, sometimes a short pile lying flat
      let x = -inner / 2 + 0.01;
      const flat = rnd() < 0.5;
      const end = inner / 2 - (flat ? 0.36 : 0.08);
      while (x < end) {
        const t = 0.04 + rnd() * 0.05, hh = sh * (0.55 + rnd() * 0.3), d = D * (0.7 + rnd() * 0.2);
        const c = BOOKS[Math.floor(rnd() * BOOKS.length)];
        P.push({ g: B(t, hh, d, x + t / 2, y + 0.035 + hh / 2, -D / 2 + 0.03 + d / 2), c, o: true });
        if (rnd() < 0.6) P.push({ g: B(t + 0.004, 0.012, 0.004, x + t / 2, y + 0.035 + hh * 0.75, -D / 2 + 0.032 + d), c: GILT });
        x += t + 0.003;
      }
      if (flat) bookParts(P, inner / 2 - 0.2, y + 0.035, 0, [
        { w: 0.3, d: 0.24, h: 0.06, c: BOOKS[(i + 1) % BOOKS.length], r: 0.05 },
        { w: 0.27, d: 0.22, h: 0.05, c: BOOKS[(i + 3) % BOOKS.length], r: -0.08 },
      ]);
    }
    P.push({ g: B(inner, 0.035, D - 0.02, 0, H - 0.0175, 0), c: WOOD_LIGHT });
    rollParts(P, lying(-0.15, H + 0.07, 0.0, 0.08, 0.9, 0.05, PAPERS[1], TIES[0]));
    rollParts(P, lying(0.1, H + 0.07, 0.05, -0.12, 0.8, 0.045, PAPERS[2], undefined, true));
    return P;
  });
  return (
    <group position={at} {...tipHandlers({ title: "Pilots' books", text: "Rutters of sailing directions, star tables and drawings of coasts seen from the sea: what a navigator read before he trusted a chart." }, "default")}>
      <Parts parts={parts} thickness={0.008} />
    </group>
  );
}

