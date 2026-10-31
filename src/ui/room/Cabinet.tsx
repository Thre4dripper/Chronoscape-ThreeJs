import { useEffect, useMemo, useRef, useState } from "react";
import { useFrame, useThree, type ThreeEvent } from "@react-three/fiber";
import { Outlines } from "@react-three/drei";
import * as THREE from "three";
import { mergeGeometries } from "three/addons/utils/BufferGeometryUtils.js";
import type { Atlas, AtlasMap } from "@/content/schema";
import { useNav } from "@/nav";
import { BRASS, cartoucheTexture, coverTexture, GILT, inlayTexture, labelTexture, OUTLINE, PAPER_T, ROMAN, toon, toonGradient, WOOD, WOOD_DARK, WOOD_LIGHT } from "./toon";
import { tipHandlers, useRoom } from "./roomState";
import { DrawerBoard, MeasureTools, WritingTools, type DrawerKind } from "./DrawerTools";
import { bookplateTexture, indexTexture } from "./pages";

/**
 * The map press: a carved walnut library cabinet. Fluted pilasters with gilt
 * capitals divide arched niches, one per atlas; a dentil cornice carries a
 * swan-neck pediment with a scroll cartouche, urns and a turning armillary
 * sphere; the plinth has two inlaid drawers (the ready maps, and the map
 * maker's instruments). All the fixed carving is merged into a few meshes,
 * one per colour, so it costs a handful of draw calls; nothing is coplanar,
 * so nothing flickers.
 */
export const CELL_W = 1.05, CELL_H = 1.18, BAR = 0.16, SHELF = 0.1, DEPTH = 0.8;
export const COVER_W = 0.72, COVER_H = 1.0;
const PLINTH = 0.64, CORNICE = 0.35, CREST = 1.12;

export function cabinetSize(cols: number, rows: number) {
  return { w: cols * CELL_W + (cols + 1) * BAR, h: rows * CELL_H + (rows + 1) * SHELF, plinth: PLINTH, cornice: CORNICE + CREST };
}

/* ------------------------------------------------------------------ static carving, merged per colour */

export type Part = { g: THREE.BufferGeometry; c: string; o?: boolean };
export const B = (w: number, h: number, d: number, x: number, y: number, z: number) => new THREE.BoxGeometry(w, h, d).translate(x, y, z);

export function merge(parts: Part[]) {
  const by = new Map<string, THREE.BufferGeometry[]>();
  for (const p of parts) {
    let g = p.g.index ? p.g.toNonIndexed() : p.g;
    g = g.clone();
    g.clearGroups();
    for (const name of Object.keys(g.attributes)) if (!["position", "normal", "uv"].includes(name)) g.deleteAttribute(name);
    const k = `${p.c}|${p.o ? 1 : 0}`;
    if (!by.has(k)) by.set(k, []);
    by.get(k)!.push(g);
    p.g.dispose();
  }
  return [...by].map(([k, gs]) => {
    const [color, o] = k.split("|");
    const geom = mergeGeometries(gs)!;
    gs.forEach((g) => g.dispose());
    geom.computeBoundingSphere();
    return { geom, color, outline: o === "1" };
  });
}

/** A turned profile (urns, feet, the armillary's pedestal): [radius, height] pairs from the bottom up. */
const lathe = (pts: [number, number][], x: number, y: number, z: number, seg = 18) => new THREE.LatheGeometry(pts.map(([r, h]) => new THREE.Vector2(r, h)), seg).translate(x, y, z);

/** One swan-neck scroll of the pediment (right side; mirror for the left) with the tympanum under it. */
function swanNeck(x0: number, x1: number, hgt: number, thick: number): { scroll: THREE.BufferGeometry; fill: THREE.BufferGeometry; end: THREE.Vector2 } {
  const c = new THREE.CubicBezierCurve(new THREE.Vector2(x0, 0.03), new THREE.Vector2(x0 - 0.15, hgt * 0.95), new THREE.Vector2(x1 + 0.6, hgt * 0.15), new THREE.Vector2(x1, hgt));
  const pts = c.getPoints(28);
  const up: THREE.Vector2[] = [], dn: THREE.Vector2[] = [];
  for (let i = 0; i < pts.length; i++) {
    const a = pts[Math.max(0, i - 1)], b = pts[Math.min(pts.length - 1, i + 1)];
    const t = new THREE.Vector2(b.x - a.x, b.y - a.y).normalize();
    const n = new THREE.Vector2(-t.y, t.x);
    up.push(pts[i].clone().addScaledVector(n, thick / 2));
    dn.push(pts[i].clone().addScaledVector(n, -thick / 2));
  }
  const shape = new THREE.Shape([...up, ...dn.reverse()]);
  const scroll = new THREE.ExtrudeGeometry(shape, { depth: 0.12, bevelEnabled: true, bevelThickness: 0.015, bevelSize: 0.012, bevelSegments: 1, curveSegments: 4 });
  const fillShape = new THREE.Shape([new THREE.Vector2(x0, 0), ...pts, new THREE.Vector2(x1, 0)]);
  const fill = new THREE.ExtrudeGeometry(fillShape, { depth: 0.05, bevelEnabled: false });
  return { scroll, fill, end: pts[pts.length - 1] };
}

function carving(cols: number, rows: number) {
  const { w, h } = cabinetSize(cols, rows);
  const y0 = PLINTH, yb = y0 + h, yt = yb + CORNICE;
  const P: Part[] = [];
  const front = DEPTH / 2;
  // carcass: back, sides, dividers, shelves
  P.push({ g: B(w, h, 0.04, 0, y0 + h / 2, -front + 0.02), c: WOOD_DARK });
  const xs = Array.from({ length: cols + 1 }, (_, c) => -w / 2 + c * (CELL_W + BAR) + BAR / 2);
  xs.forEach((x, i) => {
    const outer = i === 0 || i === cols;
    P.push({ g: B(outer ? BAR : BAR - 0.02, h, outer ? DEPTH : DEPTH - 0.06, x, y0 + h / 2, outer ? 0 : -0.03), c: WOOD, o: outer });
    // fluted pilaster with base and capital
    P.push({ g: B(0.12, h - 0.18, 0.04, x, y0 + h / 2, front + 0.02), c: WOOD_LIGHT, o: true });
    for (let k = -1; k <= 1; k++) P.push({ g: B(0.013, h - 0.42, 0.01, x + k * 0.032, y0 + h / 2, front + 0.043), c: WOOD_DARK });
    P.push({ g: B(0.17, 0.13, 0.085, x, y0 + 0.065, front + 0.022), c: WOOD, o: true });
    P.push({ g: B(0.18, 0.075, 0.09, x, yb - 0.04, front + 0.025), c: WOOD, o: true });
    P.push({ g: B(0.182, 0.024, 0.092, x, yb - 0.09, front + 0.025), c: GILT });
    for (const s of [-1, 1]) P.push({ g: new THREE.CylinderGeometry(0.024, 0.024, 0.02, 12).rotateX(Math.PI / 2).translate(x + s * 0.068, yb - 0.04, front + 0.075), c: GILT });
  });
  for (let r = 0; r <= rows; r++) P.push({ g: B(w - 0.02, SHELF, DEPTH - 0.04, 0, y0 + r * (CELL_H + SHELF) + SHELF / 2, -0.02), c: WOOD_LIGHT, o: r === 0 || r === rows });
  // per niche: a moulded lip with a gilt bead, and a segmental arch with keystone and rosettes
  const archH = 0.16;
  const arch = (() => {
    const W = CELL_W;
    const s = new THREE.Shape();
    s.moveTo(-W / 2, 0);
    s.quadraticCurveTo(0, 2 * (archH - 0.035), W / 2, 0);
    s.lineTo(W / 2, archH);
    s.lineTo(-W / 2, archH);
    s.closePath();
    return new THREE.ExtrudeGeometry(s, { depth: 0.04, bevelEnabled: false, curveSegments: 16 });
  })();
  for (let r = 0; r < rows; r++)
    for (let c = 0; c < cols; c++) {
      const cx = -w / 2 + BAR + c * (CELL_W + BAR) + CELL_W / 2;
      const floor = y0 + SHELF + r * (CELL_H + SHELF);
      const top = floor + CELL_H;
      P.push({ g: B(CELL_W, 0.06, 0.04, cx, floor - 0.03, front + 0.01), c: WOOD, o: true });
      P.push({ g: B(CELL_W, 0.012, 0.01, cx, floor - 0.03, front + 0.035), c: GILT });
      P.push({ g: arch.clone().translate(cx, top - archH, front - 0.045), c: WOOD, o: true });
      P.push({ g: B(0.07, 0.095, 0.05, cx, top - 0.048, front - 0.005), c: GILT });
      for (const s of [-1, 1]) P.push({ g: new THREE.CylinderGeometry(0.03, 0.03, 0.02, 14).rotateX(Math.PI / 2).translate(cx + s * CELL_W * 0.34, top - 0.065, front + 0.0), c: GILT });
    }
  arch.dispose();
  // cornice: architrave, frieze with dentils, two crowns with a gilt bead
  P.push({ g: B(w + 0.08, 0.07, DEPTH + 0.04, 0, yb + 0.035, 0), c: WOOD, o: true });
  P.push({ g: B(w + 0.04, 0.14, DEPTH, 0, yb + 0.14, 0), c: WOOD_LIGHT, o: true });
  const nd = Math.floor((w + 0.02) / 0.11);
  for (let i = 0; i < nd; i++) P.push({ g: B(0.05, 0.05, 0.04, -((nd - 1) * 0.11) / 2 + i * 0.11, yb + 0.18, front + 0.03), c: WOOD });
  P.push({ g: B(w + 0.26, 0.06, DEPTH + 0.2, 0, yb + 0.24, 0.01), c: WOOD, o: true });
  P.push({ g: B(w + 0.4, 0.08, DEPTH + 0.3, 0, yb + 0.31, 0.01), c: WOOD_DARK, o: true });
  P.push({ g: B(w + 0.41, 0.016, 0.012, 0, yb + 0.275, 0.01 + (DEPTH + 0.3) / 2 + 0.002), c: GILT });
  // pediment: swan-neck scrolls with volutes over a tympanum, urns at the corners
  for (const sgn of [1, -1]) {
    const { scroll, fill, end } = swanNeck(w / 2 - 0.12, 1.42, 0.62, 0.13);
    const m = new THREE.Matrix4().makeScale(sgn, 1, 1);
    const place = (g: THREE.BufferGeometry, z: number) => {
      g.applyMatrix4(m);
      if (sgn < 0) {
        if (g.index) g.index.array.reverse();
        else flipWinding(g);
      }
      return g.translate(0, yt, z);
    };
    P.push({ g: place(scroll, -0.06), c: WOOD, o: true });
    P.push({ g: place(fill, -0.12), c: WOOD_DARK });
    P.push({ g: new THREE.CylinderGeometry(0.1, 0.1, 0.14, 20).rotateX(Math.PI / 2).translate(sgn * end.x, yt + end.y - 0.02, 0.02), c: WOOD, o: true });
    P.push({ g: new THREE.CylinderGeometry(0.05, 0.05, 0.03, 16).rotateX(Math.PI / 2).translate(sgn * end.x, yt + end.y - 0.02, 0.1), c: GILT });
    const ux = sgn * (w / 2 + 0.02);
    P.push({ g: lathe([[0, 0], [0.12, 0], [0.12, 0.04], [0.06, 0.07], [0.05, 0.1], [0.11, 0.17], [0.12, 0.24], [0.08, 0.3], [0.04, 0.32], [0.06, 0.35], [0.0, 0.42]], ux, yt, 0.12), c: GILT, o: true });
  }
  // the cartouche's carved back: a gilt rim round a walnut board
  const board = (r: number, half: number) => {
    const s = new THREE.Shape();
    s.moveTo(-half, -r);
    s.lineTo(half, -r);
    s.absarc(half, 0, r, -Math.PI / 2, Math.PI / 2, false);
    s.lineTo(-half, r);
    s.absarc(-half, 0, r, Math.PI / 2, (3 * Math.PI) / 2, false);
    return new THREE.ExtrudeGeometry(s, { depth: 0.06, bevelEnabled: true, bevelThickness: 0.015, bevelSize: 0.015, bevelSegments: 2, curveSegments: 18 });
  };
  P.push({ g: board(0.27, 0.8).translate(0, yt + 0.36, -0.02), c: GILT, o: true });
  P.push({ g: board(0.235, 0.78).translate(0, yt + 0.36, 0.0), c: WOOD_DARK });
  // the armillary's pedestal
  P.push({ g: lathe([[0, 0], [0.1, 0], [0.1, 0.03], [0.04, 0.06], [0.03, 0.12], [0.07, 0.15], [0, 0.16]], 0, yt + 0.66, 0.0), c: GILT, o: true });
  // plinth: bun feet, base moulding, drawer carcass with a centre stile, top moulding
  for (const sx of [-1, 1]) P.push({ g: lathe([[0, 0], [0.09, 0.01], [0.11, 0.05], [0.09, 0.09], [0.07, 0.1], [0, 0.1]], sx * (w / 2 - 0.12), 0, front - 0.08), c: WOOD_DARK, o: true });
  P.push({ g: B(w + 0.16, 0.08, DEPTH + 0.12, 0, 0.14, 0.02), c: WOOD_DARK, o: true });
  P.push({ g: B(w, 0.4, DEPTH, 0, 0.38, 0), c: WOOD, o: true });
  P.push({ g: B(0.14, 0.4, 0.05, 0, 0.38, front + 0.01), c: WOOD_LIGHT, o: true });
  P.push({ g: B(w + 0.12, 0.06, DEPTH + 0.1, 0, 0.61, 0.02), c: WOOD_DARK, o: true });
  return merge(P);
}

function flipWinding(g: THREE.BufferGeometry) {
  // mirrored non-indexed geometry: swap two corners of every triangle so it faces outwards again
  for (const name of ["position", "normal", "uv"]) {
    const a = g.getAttribute(name) as THREE.BufferAttribute | undefined;
    if (!a) continue;
    const n = a.itemSize;
    for (let i = 0; i < a.count; i += 3)
      for (let k = 0; k < n; k++) {
        const t = a.array[(i + 1) * n + k];
        (a.array as Float32Array)[(i + 1) * n + k] = a.array[(i + 2) * n + k];
        (a.array as Float32Array)[(i + 2) * n + k] = t;
      }
  }
  // (normals were already mirrored correctly by applyMatrix4)
}

/* ------------------------------------------------------------------ the cabinet */

export function Cabinet({ atlases, cols, openId, onOpen }: { atlases: Atlas[]; cols: number; openId: string | null; onOpen: (id: string) => void }) {
  const rows = Math.ceil(atlases.length / cols);
  const { w, h } = cabinetSize(cols, rows);
  const y0 = PLINTH, yt = y0 + h + CORNICE;
  const parts = useMemo(() => carving(cols, rows), [cols, rows]);
  useEffect(() => () => parts.forEach((p) => p.geom.dispose()), [parts]);
  const crest = useMemo(() => cartoucheTexture("MAPPAE · MVNDI", "atlantes urbium per saecula"), []);
  useEffect(() => () => crest.dispose(), [crest]);
  return (
    <group>
      {parts.map((p, i) => (
        <mesh key={i} geometry={p.geom} material={toon(p.color)} castShadow receiveShadow>
          {p.outline && <Outlines thickness={0.01} color={OUTLINE} angle={0.5} />}
        </mesh>
      ))}
      <mesh position={[0, yt + 0.36, 0.105]}>
        <planeGeometry args={[2.24, 0.56]} />
        <meshBasicMaterial map={crest} transparent alphaTest={0.4} toneMapped={false} />
      </mesh>
      <Armillary at={[0, yt + 0.98, 0.0]} />
      {atlases.map((a, i) => {
        const c = i % cols, r = rows - 1 - Math.floor(i / cols);
        const x = -w / 2 + BAR + c * (CELL_W + BAR) + CELL_W / 2;
        const y = y0 + SHELF + r * (CELL_H + SHELF);
        return <Bundle key={a.id} atlas={a} index={i} at={[x, y, 0]} openId={openId} onOpen={onOpen} />;
      })}
      <Drawers w={w} />
    </group>
  );
}

/* ------------------------------------------------------------------ armillary sphere finial */

function Armillary({ at }: { at: [number, number, number] }) {
  const g = useRef<THREE.Group>(null);
  const boost = useRef(0);
  const rings = useMemo(() => {
    const r = 0.16;
    return [
      new THREE.TorusGeometry(r, 0.012, 8, 40),
      new THREE.TorusGeometry(r, 0.012, 8, 40).rotateY(Math.PI / 2),
      new THREE.TorusGeometry(r, 0.012, 8, 40).rotateX(Math.PI / 2),
      new THREE.TorusGeometry(r * 0.98, 0.02, 8, 40).rotateX(Math.PI / 2).rotateZ(0.41),
    ];
  }, []);
  useFrame((_, dt) => {
    boost.current = Math.max(0, boost.current - dt * 0.8);
    if (g.current) g.current.rotation.y += dt * (0.25 + boost.current * 4);
  });
  return (
    <group position={at}>
      <group rotation={[0, 0, 0.41]}>
        <group ref={g}>
          {rings.map((geo, i) => (
            <mesh key={i} geometry={geo} material={toon(i === 3 ? "#b8863a" : GILT)}>
              <Outlines thickness={0.005} color={OUTLINE} />
            </mesh>
          ))}
          <mesh material={toon("#4f7a8a")}>
            <sphereGeometry args={[0.05, 16, 12]} />
          </mesh>
        </group>
        <mesh material={toon(GILT)}>
          <cylinderGeometry args={[0.008, 0.008, 0.44, 8]} />
        </mesh>
      </group>
      <mesh
        visible={false}
        {...tipHandlers({ title: "An armillary sphere", text: "Rings for the equator, the tropics and the path of the sun, round a small Earth: the old model of the heavens.", hint: "Click to set it turning" })}
        onClick={(e) => {
          e.stopPropagation();
          boost.current = 1;
        }}
      >
        <sphereGeometry args={[0.22, 8, 8]} />
      </mesh>
    </group>
  );
}

/* ------------------------------------------------------------------ the drawers in the plinth */

function Drawers({ w }: { w: number }) {
  const fw = (w - 0.34) / 2;
  const cx = 0.07 + 0.03 + fw / 2;
  return (
    <>
      <Drawer kind="writing" x={-cx} fw={fw} label="CALAMI · SIGILLA" seed={7} />
      <Drawer kind="instruments" x={cx} fw={fw} label="INSTRVMENTA" seed={19} />
    </>
  );
}

function Drawer({ kind, x, fw, label, seed }: { kind: DrawerKind; x: number; fw: number; label: string; seed: number }) {
  const g = useRef<THREE.Group>(null);
  const open = useRoom((s) => s.drawer === kind);
  const inlay = useMemo(() => inlayTexture(seed), [seed]);
  const plate = useMemo(() => labelTexture(label, 512, 80, { bg: BRASS, fg: "#3d2a1c", size: 40, spacing: 6 }), [label]);
  useEffect(() => () => (inlay.dispose(), plate.dispose()), [inlay, plate]);
  const tray = useMemo(() => {
    const d = 0.62, ww = fw - 0.06;
    return merge([
      { g: B(ww, 0.02, d, 0, -0.13, -d / 2), c: WOOD_LIGHT },
      { g: B(0.02, 0.22, d, -ww / 2, -0.03, -d / 2), c: WOOD },
      { g: B(0.02, 0.22, d, ww / 2, -0.03, -d / 2), c: WOOD },
      { g: B(ww, 0.22, 0.02, 0, -0.03, -d), c: WOOD },
      { g: B(ww - 0.04, 0.005, d - 0.04, 0, -0.117, -d / 2), c: kind === "writing" ? "#5d2f2a" : "#2f4a3a" },
    ]);
  }, [fw, kind]);
  useFrame((_, dt) => {
    if (!g.current) return;
    const want = open ? 0.62 : 0;
    g.current.position.z += (want - g.current.position.z) * (1 - Math.exp(-8 * Math.min(dt, 0.05)));
  });
  const tip =
    kind === "writing"
      ? { title: "The writing drawer", text: "A quill and ink, a seal and its wax, and a candle to melt it: how a finished chart was signed and sealed.", hint: open ? "Click to close" : "Click to pull it out" }
      : { title: "The map maker's instruments", text: "Dividers, a pocket compass and a reading glass, for measuring and reading the old charts.", hint: open ? "Click to close" : "Click to pull it out" };
  return (
    <group position={[x, 0.38, DEPTH / 2 + 0.02]}>
      <group ref={g}>
        <group
          {...tipHandlers(tip)}
          onClick={(e) => {
            e.stopPropagation();
            useRoom.getState().setDrawer(open ? null : kind);
          }}
        >
          <mesh material={toon(WOOD_LIGHT)} castShadow>
            <boxGeometry args={[fw, 0.32, 0.04]} />
            <Outlines thickness={0.008} color={OUTLINE} />
          </mesh>
          <mesh position={[0, -0.02, 0.022]}>
            <planeGeometry args={[fw - 0.08, 0.24]} />
            <meshToonMaterial map={inlay} gradientMap={toonGradient()} polygonOffset polygonOffsetFactor={-2} />
          </mesh>
          <mesh position={[0, 0.125, 0.024]}>
            <planeGeometry args={[0.46, 0.072]} />
            <meshToonMaterial map={plate} gradientMap={toonGradient()} polygonOffset polygonOffsetFactor={-2} />
          </mesh>
          {[-1, 1].map((s) => (
            <mesh key={s} position={[s * fw * 0.4, -0.02, 0.05]} material={toon(BRASS)}>
              <sphereGeometry args={[0.03, 14, 10]} />
              <Outlines thickness={0.005} color={OUTLINE} />
            </mesh>
          ))}
        </group>
        {tray.map((p, i) => (
          <mesh key={i} geometry={p.geom} material={toon(p.color)} receiveShadow />
        ))}
        {kind === "writing" ? (
          <DrawerBoard kind="writing" color="#5a2a22">
            <WritingTools />
          </DrawerBoard>
        ) : (
          <DrawerBoard kind="instruments" color="#2f4a3a">
            <MeasureTools />
          </DrawerBoard>
        )}
      </group>
    </group>
  );
}

/* ------------------------------------------------------------------ an atlas: a bundle of folded maps, tied and sealed */

/**
 * Where an opened atlas is held up: in the free part of the screen (left of the atlas card,
 * below the heading), facing the viewer, at a size that fills most of that space. When its
 * cover is open it moves right, so the cover swings into view.
 */
export function heldPose(camera: THREE.Camera, size: { width: number; height: number }, out: { p: THREE.Vector3; q: THREE.Quaternion; s: number }, t: number, coverOpen: number, pointer: THREE.Vector2) {
  const cam = camera as THREE.PerspectiveCamera;
  const card = Math.min(470, size.width - 52) + 52;
  const wide = size.width > 760;
  const x0 = 26, x1 = wide ? size.width - card : size.width - 26;
  const y0 = 120, y1 = wide ? size.height - 30 : size.height * 0.3;
  const ndcX = ((x0 + x1) / 2 / size.width) * 2 - 1, ndcY = -(((y0 + y1) / 2 / size.height) * 2 - 1);
  const bandH = (y1 - y0) / size.height;
  const bandW = (x1 - x0) / size.width;
  const tan = Math.tan((cam.fov * Math.PI) / 360);
  const aspect = size.width / size.height;
  // big enough to read, small enough that the open cover still fits beside it
  const s = 1.7;
  const dH = (s * COVER_H) / (0.82 * bandH * 2 * tan);
  const dW = (s * COVER_W * (1 + coverOpen * 0.95)) / (0.9 * bandW * 2 * tan * aspect);
  const d = Math.max(dH, dW);
  const dir = new THREE.Vector3(ndcX, ndcY, 0.5).unproject(cam).sub(cam.position);
  const fwd = new THREE.Vector3(0, 0, -1).applyQuaternion(cam.quaternion);
  dir.multiplyScalar(d / dir.dot(fwd));
  const up = new THREE.Vector3(0, 1, 0).applyQuaternion(cam.quaternion);
  const right = new THREE.Vector3(1, 0, 0).applyQuaternion(cam.quaternion);
  out.p.copy(cam.position).add(dir).addScaledVector(up, -(COVER_H / 2 + 0.01) * s + Math.sin(t * 1.2) * 0.02).addScaledVector(right, coverOpen * COVER_W * s * 0.45);
  // it leans toward the pointer, as if held in the hand
  const turn = 0.16 - coverOpen * 0.12;
  out.q.copy(cam.quaternion).multiply(new THREE.Quaternion().setFromEuler(new THREE.Euler(-0.04 + Math.sin(t * 0.9) * 0.02 - pointer.y * 0.12, turn + Math.sin(t * 0.7) * 0.03 + pointer.x * 0.16, 0.015)));
  out.s = s;
}

/** The seal's wax: a disc with an uneven rim, an embossed ring and a centre boss, split into two halves (so it can break). */
function sealHalves() {
  const half = (start: number) => {
    const disc = new THREE.CylinderGeometry(0.062, 0.066, 0.022, 10, 1, false, start, Math.PI);
    const pos = disc.getAttribute("position") as THREE.BufferAttribute;
    for (let i = 0; i < pos.count; i++) {
      const x = pos.getX(i), z = pos.getZ(i), r = Math.hypot(x, z);
      if (r > 0.05) {
        const k = 1 + Math.sin(Math.atan2(z, x) * 7 + 1.3) * 0.08;
        pos.setX(i, x * k);
        pos.setZ(i, z * k);
      }
    }
    disc.computeVertexNormals();
    const ring = new THREE.TorusGeometry(0.038, 0.006, 6, 14, Math.PI).rotateX(Math.PI / 2).rotateY(-start).translate(0, 0.012, 0);
    const boss = new THREE.CylinderGeometry(0.018, 0.018, 0.012, 10, 1, false, start, Math.PI).translate(0, 0.014, 0);
    const g = merge([
      { g: disc, c: "a" },
      { g: ring, c: "a" },
      { g: boss, c: "a" },
    ])[0].geom;
    return g.rotateX(Math.PI / 2);
  };
  return [half(0), half(Math.PI)];
}

function Bundle({ atlas, index, at, openId, onOpen }: { atlas: Atlas; index: number; at: [number, number, number]; openId: string | null; onOpen: (id: string) => void }) {
  const [tex, setTex] = useState<THREE.CanvasTexture | null>(null);
  const [index_, setIndex] = useState<THREE.CanvasTexture | null>(null);
  const plaque = useMemo(() => labelTexture(ROMAN[index] ?? String(index + 1), 128, 64, { bg: BRASS, fg: "#4a3322", size: 34, spacing: 4 }), [index]);
  useEffect(() => {
    // one cover per frame or so, so the room never stalls while they are drawn
    let alive = true;
    const timer = setTimeout(() => void coverTexture(atlas).then((t) => (alive ? setTex(t) : t.dispose())), 120 + index * 70);
    return () => {
      alive = false;
      clearTimeout(timer);
    };
  }, [atlas, index]);
  const open = openId === atlas.id;
  const [plate, setPlate] = useState<THREE.CanvasTexture | null>(null);
  useEffect(() => {
    if (!open || index_) return;
    setIndex(indexTexture(atlas));
    setPlate(bookplateTexture(atlas));
  }, [open, index_, atlas]);
  useEffect(() => () => plate?.dispose(), [plate]);
  useEffect(() => () => tex?.dispose(), [tex]);
  useEffect(() => () => index_?.dispose(), [index_]);
  useEffect(() => () => plaque.dispose(), [plaque]);
  const coverMat = useMemo(() => new THREE.MeshToonMaterial({ map: tex, color: tex ? "#ffffff" : PAPER_T, gradientMap: toonGradient() }), [tex]);
  const ribbon = useMemo(() => new THREE.MeshToonMaterial({ color: atlas.color, gradientMap: toonGradient() }), [atlas.color]);
  const seal = useMemo(() => new THREE.MeshToonMaterial({ color: new THREE.Color(atlas.color).multiplyScalar(0.62), gradientMap: toonGradient() }), [atlas.color]);
  useEffect(() => () => (coverMat.dispose(), ribbon.dispose(), seal.dispose()), [coverMat, ribbon, seal]);
  const geo = useMemo(() => {
    const papers = merge(
      ["#efdcb4", "#e7d2a6", "#f4e6c6"].map((_, k) => ({
        g: new THREE.BoxGeometry(COVER_W * 0.98, COVER_H * 0.97, 0.03).rotateZ((k - 1) * 0.035).translate((k - 1) * 0.022, -0.01 * k, -0.06 - k * 0.035),
        c: "p",
      })),
    )[0].geom;
    // the ribbon: a thin band right round the bundle, with two tails hanging from the seal
    const y = -COVER_H * 0.28, t = 0.012, bw = 0.05, back = -0.17, frontZ = 0.027;
    const band = merge([
      { g: B(COVER_W + 0.03, bw, t, 0, y, frontZ), c: "r" },
      { g: B(COVER_W + 0.03, bw, t, 0, y, back), c: "r" },
      { g: B(t, bw, frontZ - back, -(COVER_W + 0.03) / 2, y, (frontZ + back) / 2), c: "r" },
      { g: B(t, bw, frontZ - back, (COVER_W + 0.03) / 2, y, (frontZ + back) / 2), c: "r" },
      { g: B(0.04, 0.16, t, 0, 0, 0).translate(0, -0.08, 0).rotateZ(0.32).translate(0.15, y - 0.01, frontZ + 0.006), c: "r" },
      { g: B(0.04, 0.14, t, 0, 0, 0).translate(0, -0.07, 0).rotateZ(-0.12).translate(0.19, y - 0.01, frontZ + 0.006), c: "r" },
    ])[0].geom;
    const [s0, s1] = sealHalves();
    return { papers, band, s0, s1 };
  }, []);
  useEffect(() => () => Object.values(geo).forEach((g) => g.dispose()), [geo]);

  const g = useRef<THREE.Group>(null);
  const hinge = useRef<THREE.Group>(null);
  const bandRef = useRef<THREE.Mesh>(null);
  const halves = useRef<(THREE.Mesh | null)[]>([]);
  const papersRef = useRef<THREE.Mesh>(null);
  const hovered = useRoom((s) => s.hoverId === atlas.id);
  const setHover = useRoom((s) => s.setHover);
  const dim = !!openId && !open;
  // the held atlas: 0 sealed, then the seal breaks and the cover opens like a book
  const [opened, setOpened] = useState(false);
  const [broken, setBroken] = useState(false);
  const brokeAt = useRef(0);
  useEffect(() => {
    if (!open) {
      setOpened(false);
      setBroken(false);
    }
  }, [open]);
  const tmp = useMemo(() => ({ p: new THREE.Vector3(), q: new THREE.Quaternion(), e: new THREE.Euler(), home: new THREE.Vector3(...at), cover: 0 }), [at]);
  const { camera, size, clock } = useThree();
  const held = useMemo(() => ({ p: new THREE.Vector3(), q: new THREE.Quaternion(), s: 1 }), []);
  useFrame((state, dtRaw) => {
    const o = g.current;
    if (!o) return;
    const dt = Math.min(dtRaw, 0.05);
    const k = 1 - Math.exp(-7 * dt);
    tmp.cover += ((opened ? 1 : 0) - tmp.cover) * (1 - Math.exp(-5 * dt));
    if (open) {
      heldPose(camera, size, held, state.clock.elapsedTime, tmp.cover, state.pointer);
      tmp.p.copy(held.p);
      tmp.q.copy(held.q);
      o.scale.lerp(new THREE.Vector3(held.s, held.s, held.s), k);
    } else {
      tmp.p.copy(tmp.home).add(new THREE.Vector3(0, hovered ? 0.05 : 0, hovered ? 0.34 : 0));
      tmp.e.set(hovered ? -0.02 : -0.13, hovered ? 0.06 : 0, 0);
      tmp.q.setFromEuler(tmp.e);
      o.scale.lerp(new THREE.Vector3(1, 1, 1).multiplyScalar(hovered ? 1.04 : 1), k);
    }
    o.position.lerp(tmp.p, k);
    o.quaternion.slerp(tmp.q, k);
    // the cover swings open on its left edge, like the board of a book
    if (hinge.current) hinge.current.rotation.y = -tmp.cover * 2.0;
    if (papersRef.current) papersRef.current.rotation.z = tmp.cover * 0.02;
    // breaking the seal: the halves fly apart and drop, the ribbon slips off
    const t = broken ? state.clock.elapsedTime - brokeAt.current : 0;
    halves.current.forEach((m, i) => {
      if (!m) return;
      const s = i ? 1 : -1;
      m.position.set(0.17 + s * t * 0.35, -COVER_H * 0.28 - t * t * 2.2, 0.04 + t * 0.4);
      m.rotation.set(0, 0, s * t * 4);
      m.visible = t < 0.9;
    });
    if (bandRef.current) {
      bandRef.current.position.y = -t * t * 3;
      bandRef.current.visible = t < 0.7;
    }
    const target = dim ? 0.45 : 1;
    for (const m of [coverMat, ribbon]) {
      const cur = (m.userData.dim as number | undefined) ?? 1;
      const next = cur + (target - cur) * k;
      if (Math.abs(next - cur) > 0.001) {
        m.userData.base ??= m.color.clone();
        m.color.copy(m.userData.base as THREE.Color).multiplyScalar(next);
        m.userData.dim = next;
      }
    }
  });

  const over = (e: ThreeEvent<PointerEvent>) => {
    e.stopPropagation();
    if (openId) return;
    setHover(atlas.id);
    document.body.style.cursor = "pointer";
  };
  const out = () => {
    if (useRoom.getState().hoverId === atlas.id) setHover(null);
    document.body.style.cursor = "";
  };
  const clickShelf = (e: ThreeEvent<MouseEvent>) => {
    e.stopPropagation();
    document.body.style.cursor = "";
    onOpen(atlas.id);
  };
  const openBook = () => {
    useRoom.getState().setTip(null);
    if (!broken) {
      setBroken(true);
      brokeAt.current = clock.elapsedTime;
      setTimeout(() => setOpened(true), 320);
    } else setOpened((v) => !v);
  };
  /* ---- the held atlas answers to the pointer: its towns, its seal, its pages ---- */
  const townAt = (e: ThreeEvent<PointerEvent | MouseEvent>) => {
    if (!e.uv || e.face?.materialIndex !== 4) return null;
    const pins = (tex?.userData.pins ?? []) as { u: number; v: number; title: string }[];
    let best: { d: number; m: AtlasMap } | null = null;
    for (const p of pins) {
      const d = Math.hypot((p.u - e.uv.x) * COVER_W, (p.v - e.uv.y) * COVER_H);
      const m = atlas.maps.find((x) => x.title === p.title);
      if (m && d < 0.045 && (!best || d < best.d)) best = { d, m };
    }
    return best?.m ?? null;
  };
  const rowAt = (e: ThreeEvent<PointerEvent | MouseEvent>) => {
    if (!e.uv || !index_) return null;
    const rows = (index_.userData.rows ?? []) as { v0: number; v1: number; title: string }[];
    const r = rows.find((x) => e.uv!.y <= x.v0 && e.uv!.y >= x.v1);
    return r ? atlas.maps.find((m) => m.title === r.title) ?? null : null;
  };
  const showMap = (m: AtlasMap | null, fallback: { title: string; text?: string; hint?: string }) => {
    useRoom.getState().setTip(
      m ? { title: m.title, text: m.subtitle, hint: m.city ? "Click to unfold the map" : "In preparation: click to find it on the card" } : fallback,
    );
    document.body.style.cursor = "pointer";
  };
  const pickMap = (m: AtlasMap, e: ThreeEvent<MouseEvent>) => {
    if (m.city) {
      const r = e.nativeEvent;
      useNav.getState().openMap(atlas.id, m, { x: r.clientX - 40, y: r.clientY - 50, w: 80, h: 100 });
    } else dispatchEvent(new CustomEvent("chronoscape:pick-map", { detail: { atlas: atlas.id, title: m.title } }));
  };
  const leave = () => {
    useRoom.getState().setTip(null);
    document.body.style.cursor = "";
  };
  const sealedTip = { title: atlas.title, text: "Sealed with wax and tied with a ribbon.", hint: "Click to break the seal and open it" };
  const coverHandlers = open
    ? {
        onPointerMove: (e: ThreeEvent<PointerEvent>) => {
          e.stopPropagation();
          if (opened) showMap(null, { title: atlas.title, hint: "Click to close the cover" });
          else showMap(townAt(e), broken ? { title: atlas.title, hint: "Click to open the cover" } : sealedTip);
        },
        onPointerOut: leave,
        onClick: (e: ThreeEvent<MouseEvent>) => {
          e.stopPropagation();
          const m = !opened ? townAt(e) : null;
          if (m) pickMap(m, e);
          else openBook();
        },
      }
    : {};
  const pageHandlers = open
    ? {
        onPointerMove: (e: ThreeEvent<PointerEvent>) => {
          e.stopPropagation();
          showMap(rowAt(e), { title: "Index mapparum", text: "The maps in this atlas." });
        },
        onPointerOut: leave,
        onClick: (e: ThreeEvent<MouseEvent>) => {
          e.stopPropagation();
          const m = rowAt(e);
          if (m) pickMap(m, e);
        },
      }
    : {};
  return (
    <>
      {/* brass number plaque on the niche's lip */}
      <mesh position={[at[0], at[1] - 0.03, DEPTH / 2 + 0.044]}>
        <planeGeometry args={[0.2, 0.09]} />
        <meshToonMaterial map={plaque} gradientMap={toonGradient()} polygonOffset polygonOffsetFactor={-2} />
      </mesh>
      <group ref={g} position={at} onPointerOver={open ? undefined : over} onPointerOut={open ? undefined : out} onClick={open ? undefined : clickShelf}>
        {/* the bundle stands on the shelf: origin at its foot */}
        <group position={[0, COVER_H / 2 + 0.01, 0.08]}>
          <mesh ref={papersRef} geometry={geo.papers} material={toon("#ebd8ae")} castShadow>
            <Outlines thickness={0.006} color={OUTLINE} />
          </mesh>
          {/* the index page under the cover */}
          {open && (
            <mesh position={[0, 0, -0.026]} {...pageHandlers}>
              <planeGeometry args={[COVER_W * 0.96, COVER_H * 0.96]} />
              <meshToonMaterial key={index_ ? "index" : "blank"} map={index_} color={index_ ? "#ffffff" : PAPER_T} gradientMap={toonGradient()} />
            </mesh>
          )}
          <group ref={hinge} position={[-COVER_W / 2, 0, 0]}>
            <mesh position={[COVER_W / 2, 0, 0]} castShadow {...coverHandlers}>
              <boxGeometry args={[COVER_W, COVER_H, 0.04]} />
              <meshToonMaterial attach="material-0" color={PAPER_T} gradientMap={toonGradient()} />
              <meshToonMaterial attach="material-1" color={PAPER_T} gradientMap={toonGradient()} />
              <meshToonMaterial attach="material-2" color={PAPER_T} gradientMap={toonGradient()} />
              <meshToonMaterial attach="material-3" color={PAPER_T} gradientMap={toonGradient()} />
              <primitive object={coverMat} attach="material-4" />
              <meshToonMaterial key={plate ? "plate" : "plain"} attach="material-5" map={plate} color={plate ? "#ffffff" : "#e7d3a6"} gradientMap={toonGradient()} />
              <Outlines thickness={0.008} color={OUTLINE} />
            </mesh>
          </group>
          <mesh ref={bandRef} geometry={geo.band} material={ribbon}>
            <Outlines thickness={0.004} color={OUTLINE} />
          </mesh>
          {[geo.s0, geo.s1].map((sg, i) => (
            <mesh
              key={i}
              ref={(m) => {
                halves.current[i] = m;
              }}
              geometry={sg}
              material={seal}
              position={[0.17, -COVER_H * 0.28, 0.04]}
              onClick={
                open
                  ? (e: ThreeEvent<MouseEvent>) => {
                      e.stopPropagation();
                      openBook();
                    }
                  : undefined
              }
            >
              <Outlines thickness={0.004} color={OUTLINE} />
            </mesh>
          ))}
        </group>
      </group>
      {/* an invisible, generous hit box so the whole niche answers to the pointer (only on the shelf); it stays in the
          niche rather than sliding out with a pointed-at atlas, or it would reach over the drawers below and take their clicks */}
      {!open && (
        <mesh position={[at[0], at[1] + CELL_H / 2, 0.1]} visible={false} onPointerOver={over} onPointerOut={out} onClick={clickShelf}>
          <boxGeometry args={[CELL_W, CELL_H, 0.6]} />
        </mesh>
      )}
    </>
  );
}
