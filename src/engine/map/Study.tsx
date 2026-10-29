import { Suspense, useEffect, useMemo, useRef } from "react";
import { useFrame, type ThreeEvent } from "@react-three/fiber";
import * as THREE from "three";
import { mergeGeometries } from "three/addons/utils/BufferGeometryUtils.js";
import type { City } from "@/content/schema";
import { atlasCatalog } from "@/content/registry";
import { useNav } from "@/nav";
import { frameOf } from "../coords";
import { bakedMaterial } from "../render/baked";
import { useStore, type HoveredFeature } from "../store";
import { tintFactor, tintGeometry, useStudyModels, type StudyModel, type StudyPart } from "./studyAssets";

/**
 * The writing table the map lies on, standing in the dark: no room round it, so nothing competes with the
 * map (the Desk button in the HUD clears the table away altogether). On the table,
 * the things a map reader keeps at hand, a few of them from the map's own part of the world: an oil lamp or
 * a candle (it lights the evening), a sandglass (it turns the hours), the atlases (they open the map case),
 * rolled maps, and an inkstone, an astrolabe, a quipu or a clay tablet, depending on the atlas.
 *
 * The map is what the room is for, so the room stays in the dark: everything here is lit by a pool of lamp
 * light on the sheet that falls off, warm and desaturated, into darkness with distance from the board's edge. The board
 * casts a soft shadow on a tooled inset, and the props stand well back in the margins of the table.
 *
 * The table and the things on it are Blender models (tools/blender/models/study, see studyAssets.ts): colour and
 * occlusion baked into the vertices, drawn unlit with the lamp pool on top. The table's size follows the map, so it
 * comes as parts (mouldings, apron and stretchers stretched along their length, legs, drawers and carvings at their
 * true size) merged here into one mesh. Kept light: one shared material, a few small canvas textures, no lights,
 * nothing animated unless it was clicked. Everything is in metres (the group is scaled by U) with no coplanar faces.
 */
type Theme = "classical" | "medieval" | "renaissance" | "neareast" | "india" | "silk" | "china" | "islamic" | "mughal" | "japan" | "africa" | "americas";
const THEME_OF: Record<string, Theme> = {
  "classical-mediterranean": "classical", "medieval-europe": "medieval", "renaissance-europe": "renaissance", "egypt-near-east": "neareast",
  "ancient-india": "india", "silk-road": "silk", "imperial-china": "china", "islamic-golden-age": "islamic", "mughal-india": "mughal",
  japan: "japan", africa: "africa", americas: "americas",
};

/* ------------------------------------------------------------------ the lamp pool */

/** The board's half size and one metre, in world units: set by the study on mount. */
const POOL_U = { uPool: { value: new THREE.Vector3(1, 1, 1) } };
/** Darker, warmer and greyer away from the board, and down the legs into the dark. */
const POOL = `
  vec2 pq = max(abs(vWP.xz) - uPool.xy, 0.0);
  float pd = length(pq) / uPool.z;
  float pk = mix(1.0, 0.48, smoothstep(0.0, 0.32, pd)) * mix(1.0, 0.45, smoothstep(0.6, 3.6, pd));
  pk *= mix(0.25, 1.0, smoothstep(-0.7, -0.05, vWP.y / uPool.z));
  float pl = dot(gl_FragColor.rgb, vec3(0.3, 0.59, 0.11));
  gl_FragColor.rgb = mix(vec3(pl), gl_FragColor.rgb, 0.5 + 0.5 * pk) * pk * mix(vec3(0.95, 0.82, 0.68), vec3(1.0), pk);`;

/** Every Blender part: its colour and occlusion are in the vertices, the fixed light comes from its normals. */
const vcMat = bakedMaterial({ vertexColors: true, extraFrag: POOL, extraUniforms: POOL_U, key: "study-vc" });
const texMats = new Map<THREE.Texture, THREE.MeshBasicMaterial>();
const texMat = (t: THREE.Texture) => {
  let m = texMats.get(t);
  if (!m) texMats.set(t, (m = bakedMaterial({ map: t, extraFrag: POOL, extraUniforms: POOL_U, key: "study-tex" })));
  return m;
};
const sandMat = bakedMaterial({ color: "#C9A86A", extraFrag: POOL, extraUniforms: POOL_U, key: "study" });
const glassMat = bakedMaterial({ color: "#dfe6e2", transparent: true, opacity: 0.22, depthWrite: false, extraFrag: POOL, extraUniforms: POOL_U, key: "study" });
const flameMat = new THREE.MeshBasicMaterial({ color: "#ffb347", toneMapped: false });
const glowMat = new THREE.MeshBasicMaterial({ color: "#ffd9a0", toneMapped: false });

/* ------------------------------------------------------------------ painted textures (cached) */

const texs = new Map<string, THREE.CanvasTexture>();
function canvasTex(key: string, w: number, h: number, draw: (g: CanvasRenderingContext2D, w: number, h: number) => void, keep = true) {
  const old = keep && texs.get(key);
  if (old) return old;
  const c = document.createElement("canvas");
  c.width = w;
  c.height = h;
  draw(c.getContext("2d")!, w, h);
  const t = new THREE.CanvasTexture(c);
  t.colorSpace = THREE.SRGBColorSpace;
  t.anisotropy = 4;
  if (keep) texs.set(key, t);
  return t;
}
/** A small seeded random, so the painted textures are the same every visit. */
function rand(seed: number) {
  return () => ((seed = (seed * 16807) % 2147483647) - 1) / 2147483646;
}

/* ------------------------------------------------------------------ which models each atlas puts on the table */

type LampKind = "candle" | "oil" | "bronze" | "andon" | "brazier";
const lampOf = (t: Theme): LampKind => (t === "medieval" || t === "renaissance" ? "candle" : t === "japan" ? "andon" : t === "china" ? "bronze" : t === "americas" ? "brazier" : "oil");
const THEMED: Record<Theme, string[]> = {
  china: ["inkstone", "seal", "brush"], japan: ["inkstone", "seal", "brush"],
  islamic: ["astrolabe", "quill", "dividers"], silk: ["astrolabe", "quill", "dividers"], mughal: ["astrolabe", "quill", "dividers"], medieval: ["astrolabe", "quill"],
  renaissance: ["dividers", "quill", "lens"], neareast: ["clay-tablet", "palette"], classical: ["wax-tablet", "scroll"],
  india: ["palm-leaf", "reed"], africa: ["manuscript", "reed"], americas: ["quipu", "codex"],
};

/** The table's wood, by atlas, matched to the painted top (the models are baked in figured walnut). */
const TABLE_WOOD = "#5A3822";
const woodOf = (t: Theme) => (t === "japan" || t === "china" ? "#2a1a14" : t === "renaissance" || t === "islamic" || t === "mughal" ? "#4e3020" : t === "medieval" ? "#6a4a2a" : "#5a3822");

export function Study({ city }: { city: City }) {
  const f = frameOf(city);
  const w = f.width * f.scale, h = f.height * f.scale;
  // one metre of the study in world units: the map's long side is a 90 cm sheet
  const U = Math.max(w, h) / 0.9;
  const topY = -0.72;
  // the board (ParchmentMap's, in metres) and a table with wide margins round it
  const bw = (w + 0.4) / U, bd = (h + 0.4) / U;
  const Tw = bw + 0.78, Td = bd + 0.62;
  const fromAtlas = useNav((s) => s.fromAtlas);
  const theme: Theme = useMemo(() => {
    const id = fromAtlas && atlasCatalog.atlases.find((a) => a.id === fromAtlas && a.maps.some((m) => m.city === city.id)) ? fromAtlas : atlasCatalog.atlases.find((a) => a.maps.some((m) => m.city === city.id))?.id;
    return THEME_OF[id ?? ""] ?? "renaissance";
  }, [city.id, fromAtlas]);
  POOL_U.uPool.value.set((w + 0.4) / 2, (h + 0.4) / 2, U);

  const local = useMemo(() => {
    const top = canvasTex("top", 1024, Math.round((1024 * Td) / Tw), (g, cw, ch) => paintTop(g, cw, ch, theme, Tw, bw, bd), false);
    const shadow = canvasTex("shadow", 512, Math.round((512 * (bd + 0.24)) / (bw + 0.24)), (g, cw, ch) => paintShadow(g, cw, ch, (0.12 / (bw + 0.24)) * cw), false);
    shadow.colorSpace = THREE.NoColorSpace;
    const m = {
      top: bakedMaterial({ map: top, extraFrag: POOL, extraUniforms: POOL_U, key: "study-tex" }),
      shadow: new THREE.MeshBasicMaterial({ map: shadow, transparent: true, depthWrite: false, toneMapped: false, polygonOffset: true, polygonOffsetFactor: -2, polygonOffsetUnits: -2 }),
    };
    return { t: [top, shadow], m };
  }, [theme, Tw, Td, bw, bd]);
  useEffect(
    () => () => {
      local.t.forEach((t) => t.dispose());
      [local.m.top, local.m.shadow].forEach((m) => m.dispose());
    },
    [local],
  );

  // the margins of the table round the board, where the things on it stand (x east, z toward the viewer)
  const hx = bw / 2, hz = bd / 2;
  return (
    <group name="study" position-y={topY} scale={U}>
      {/* the top: figured wood with a tooled inset round the board (painted), its moulded edge is the frame's */}
      <mesh rotation-x={-Math.PI / 2} material={local.m.top}>
        <planeGeometry args={[Tw, Td]} />
      </mesh>
      {/* the board's shadow on the inset, so the map lifts off the table */}
      <mesh rotation-x={-Math.PI / 2} position-y={0.001} material={local.m.shadow} raycast={() => null} renderOrder={1}>
        <planeGeometry args={[bw + 0.24, bd + 0.24]} />
      </mesh>
      <Suspense fallback={null}>
        <Furniture theme={theme} Tw={Tw} Td={Td} hx={hx} hz={hz} />
      </Suspense>
    </group>
  );
}

/** The table's frame and everything on it, once their models have loaded (all at once, in parallel). */
function Furniture({ theme, Tw, Td, hx, hz }: { theme: Theme; Tw: number; Td: number; hx: number; hz: number }) {
  const lamp = lampOf(theme);
  const names = useMemo(() => ["table", "atlases", "rolled-maps", "map-case", "sandglass", `lamp-${lamp}`, ...THEMED[theme]], [theme, lamp]);
  const m = useStudyModels(names);
  const left: At = [-(hx + 0.21), 0, -hz * 0.55], mid: At = [-hx * 0.3, 0, hz + 0.16], right: At = [hx * 0.45, 0, hz + 0.16];
  return (
    <>
      <TableFrame m={m.table} Tw={Tw} Td={Td} theme={theme} />
      <Atlases m={m.atlases} at={[-(hx + 0.2), 0, hz + 0.16]} />
      <RolledMaps m={m["rolled-maps"]} at={[hx * 0.2, 0, -(hz + 0.12)]} />
      <MapCase m={m["map-case"]} at={[-hx * 0.35, 0, -(hz + 0.25)]} />
      <Lamp m={m[`lamp-${lamp}`]} kind={lamp} brass={theme === "islamic" || theme === "mughal" || theme === "silk"} at={[hx + 0.2, 0, -(hz + 0.1)]} />
      <Sandglass m={m.sandglass} at={[hx + 0.21, 0, hz * 0.55]} />
      <Themed theme={theme} m={m} left={left} mid={mid} right={right} />
    </>
  );
}

/* ------------------------------------------------------------------ the table */

/** Where the table's parts sit, in metres (tools/blender/models/study/study_table.py). */
const T = { inLeg: 0.09, inApron: 0.075, block: 0.0375, floor: -0.785, apronBot: -0.132, drawerY: -0.076, stretcherY: -0.665 };

/**
 * The frame of the table, merged into one mesh: the top's moulded edge, the apron with its drawers, drops and
 * brackets, the legs and the stretchers. Straight runs are stretched along their length to the table's size;
 * turned and carved parts are placed at their true size. The wood takes the atlas's finish, the brasses keep theirs.
 */
function TableFrame({ m, Tw, Td, theme }: { m: StudyModel; Tw: number; Td: number; theme: Theme }) {
  const geom = useMemo(() => {
    const k = tintFactor(TABLE_WOOD, woodOf(theme));
    const span = (g: THREE.BufferGeometry, axis: "x" | "z") => {
      if (!g.boundingBox) g.computeBoundingBox();
      return g.boundingBox!.max[axis] - g.boundingBox!.min[axis];
    };
    const out: THREE.BufferGeometry[] = [];
    const M = new THREE.Matrix4(), tr = new THREE.Matrix4(), sc = new THREE.Matrix4();
    const put = (name: string, ry: number, x: number, y: number, z: number, len?: number, depth?: number) => {
      const p = m[name];
      if (!p) return;
      M.makeRotationY(ry)
        .multiply(tr.makeTranslation(x, y, z))
        .multiply(sc.makeScale(len ? len / span(p.geometry, "x") : 1, 1, depth ? depth / span(p.geometry, "z") : 1));
      const g = p.geometry.clone().applyMatrix4(M);
      if (!name.includes("brass")) tintGeometry(g, k);
      out.push(g);
    };
    const sides: [number, number, number][] = [
      [0, Tw / 2, Td / 2],
      [Math.PI / 2, Td / 2, Tw / 2],
      [Math.PI, Tw / 2, Td / 2],
      [-Math.PI / 2, Td / 2, Tw / 2],
    ];
    sides.forEach(([ry, half, edge], i) => {
      const apron = edge - T.inApron, inner = half - T.inLeg;
      put("top_run", ry, 0, 0, edge, 2 * half);
      put("top_corner", ry, half, 0, edge);
      put("apron_run", ry, 0, 0, apron, 2 * inner);
      put("stretcher", ry, 0, T.stretcherY, edge - T.inLeg, 2 * inner);
      put("leg", ry, inner, T.floor, edge - T.inLeg);
      put("pendant", ry, 0, T.apronBot, apron);
      put("bracket_r", ry, inner - T.block, T.apronBot, apron);
      put("bracket_l", ry, -(inner - T.block), T.apronBot, apron);
      if (i % 2 === 0)
        for (const s of [-1, 1]) {
          put("drawer", ry, s * Tw * 0.2, T.drawerY, apron);
          put("drawer_brass", ry, s * Tw * 0.2, T.drawerY, apron);
        }
    });
    put("core", 0, 0, 0, 0, Tw, Td);
    const merged = mergeGeometries(out);
    out.forEach((g) => g.dispose());
    return merged;
  }, [m, Tw, Td, theme]);
  useEffect(() => () => geom?.dispose(), [geom]);
  return geom ? <mesh geometry={geom} material={vcMat} raycast={() => null} /> : null;
}

/* ------------------------------------------------------------------ interaction */

function useTip(f: Omit<HoveredFeature, "kind">) {
  return {
    onPointerOver: (e: ThreeEvent<PointerEvent>) => {
      e.stopPropagation();
      useStore.getState().hoverFeature({ kind: "object", ...f });
      document.body.style.cursor = "pointer";
    },
    onPointerOut: () => {
      const st = useStore.getState();
      if (st.hoveredFeature?.kind === "object") st.hoverFeature(null);
      document.body.style.cursor = "";
    },
  };
}

/** A small one-shot animation: 0 → 1 over `secs` after each click. */
function usePulse(secs: number) {
  const t = useRef(1);
  const start = () => (t.current = 0);
  useFrame((_, dt) => {
    if (t.current < 1) t.current = Math.min(1, t.current + dt / secs);
  });
  return { t, start };
}
const smooth = (t: number) => (t < 1 ? t * t * (3 - 2 * t) : 1);

type At = [number, number, number];

/** One part of a model, at its pivot. */
function Part({ p, material = vcMat, renderOrder }: { p?: StudyPart; material?: THREE.Material; renderOrder?: number }) {
  if (!p) return null;
  return <mesh geometry={p.geometry} position={p.position} quaternion={p.quaternion} material={material} renderOrder={renderOrder} />;
}

/* ------------------------------------------------------------------ the things on the table (in metres) */

/** Three bound atlases, stacked: raised bands on rounded spines, gilt rules, brass corners, a clasp and a boss. */
function Atlases({ m, at }: { m: StudyModel; at: At }) {
  const tip = useTip({ id: "atlases", name: "The atlases", blurb: "Twelve atlases of the world's cities, from the Nile to the Andes.", hint: "Click to open the map case" });
  return (
    <group position={at} {...tip} onClick={(e) => (e.stopPropagation(), dispatchEvent(new CustomEvent("chronoscape:open-mapcase")))}>
      <Part p={m.base} />
    </group>
  );
}

/** Rolled sheets (a true spiral of paper at their ends), tied with tape. */
function RolledMaps({ m, at }: { m: StudyModel; at: At }) {
  const tip = useTip({ id: "rolled-maps", name: "Rolled maps", blurb: "Sheets waiting their turn, tied with tape so they keep their curl." });
  return (
    <group position={at} {...tip}>
      <Part p={m.base} />
    </group>
  );
}

function MapCase({ m, at }: { m: StudyModel; at: At }) {
  const tip = useTip({ id: "map-case", name: "A map tube", blurb: "Boiled leather with brass caps: how a surveyor carried sheets through rain and dust." });
  return (
    <group position={at} {...tip}>
      <Part p={m.base} />
    </group>
  );
}

/** The light of the room: click it to light the evening or put it out. */
function Lamp({ m, kind, brass, at }: { m: StudyModel; kind: LampKind; brass: boolean; at: At }) {
  const hour = useStore((s) => s.hour);
  const lit = hour >= 19 || hour < 6;
  const names = { candle: "A beeswax candle", andon: "An andon lantern", bronze: "A bronze oil lamp", brazier: "A clay brazier", oil: "An oil lamp" };
  const tip = useTip({ id: "lamp", name: names[kind], blurb: lit ? "Lit: the city is shown at night." : "The day is still bright.", hint: lit ? "Click to put it out" : "Click to light the evening" });
  const flame = useRef<THREE.Group>(null);
  useFrame(({ clock }) => {
    if (flame.current) flame.current.scale.setScalar(lit ? 1 + Math.sin(clock.elapsedTime * 11) * 0.1 : 0.001);
  });
  const toggle = (e: ThreeEvent<MouseEvent>) => {
    e.stopPropagation();
    useStore.getState().setHour(lit ? 10 : 21);
  };
  // the clay oil lamp, cast in brass in the Islamic world
  const base = useMemo(() => (kind === "oil" && brass && m.base ? tintGeometry(m.base.geometry.clone(), tintFactor("#8E5034", "#A8823A")) : null), [m, kind, brass]);
  useEffect(() => () => base?.dispose(), [base]);
  const [fx, fy] = ({ candle: [0, 0.27], oil: [0.075, 0.048], bronze: [0, 0.2], andon: [0, 0.07], brazier: [0, 0.085] } as const)[kind];
  return (
    <group position={at} {...tip} onClick={toggle}>
      {base ? <mesh geometry={base} material={vcMat} /> : <Part p={m.base} />}
      {m.paper && <Part p={m.paper} material={lit ? glowMat : vcMat} />}
      {m.coals && <Part p={m.coals} material={lit ? flameMat : vcMat} />}
      <group ref={flame} position={[fx, fy, 0]}>
        <mesh position-y={0.018} material={flameMat}>
          <coneGeometry args={[0.009, 0.04, 8]} />
        </mesh>
        <mesh position-y={0.012} material={glowMat}>
          <sphereGeometry args={[0.006, 8, 6]} />
        </mesh>
      </group>
    </group>
  );
}

/** A sandglass: click to turn it, and the hours move on. */
function Sandglass({ m, at }: { m: StudyModel; at: At }) {
  const tip = useTip({ id: "sandglass", name: "A sandglass", blurb: "Each turn runs about an hour of reading.", hint: "Click to turn it: the day moves on three hours" });
  const g = useRef<THREE.Group>(null);
  const { t, start } = usePulse(0.8);
  const flips = useRef(0);
  // the sand in each bulb (0..1, together 1): bulb A starts at the bottom, full. Once a turn has finished,
  // the bulb now on top runs into the one below in about five seconds: a pile grows on the floor of the lower
  // bulb, and what is left above sinks into the funnel toward the neck.
  const fill = useRef({ a: 1 });
  const sand = [useRef<THREE.Mesh>(null), useRef<THREE.Mesh>(null)];
  useFrame((_, dt) => {
    if (g.current) g.current.rotation.z = (flips.current - 1 + smooth(t.current)) * Math.PI;
    const aDown = flips.current % 2 === 0;
    if (t.current >= 1) fill.current.a = Math.min(1, Math.max(0, fill.current.a + (aDown ? 1 : -1) * Math.min(dt, 0.1) / 5));
    [fill.current.a, 1 - fill.current.a].forEach((v, i) => {
      const mesh = sand[i].current;
      if (!mesh) return;
      // i = 0 is bulb A (below the neck in the glass's own frame), i = 1 is bulb B
      const s = i === 0 ? -1 : 1, down = (i === 0) === aDown, k = Math.cbrt(v);
      mesh.visible = v > 0.01;
      mesh.rotation.x = s > 0 ? Math.PI : 0; // the cone's tip always points at the neck
      if (down) {
        const h = 0.025 * k;
        mesh.scale.set(k, k, k);
        mesh.position.y = s * (0.078 - h / 2);
      } else {
        const h = 0.03 * k;
        mesh.scale.set(0.8 * k, 1.2 * k, 0.8 * k);
        mesh.position.y = s * (0.008 + h / 2);
      }
    });
  });
  const turn = (e: ThreeEvent<MouseEvent>) => {
    e.stopPropagation();
    flips.current++;
    start();
    const st = useStore.getState();
    st.setHour((st.hour + 3) % 24);
  };
  return (
    <group position={at} {...tip} onClick={turn}>
      <group ref={g} position-y={0.092}>
        <group position-y={-0.092}>
          <Part p={m.base} />
          <Part p={m.glass} material={glassMat} renderOrder={2} />
        </group>
        {sand.map((r, i) => (
          <mesh key={i} ref={r} material={sandMat}>
            <coneGeometry args={[0.031, 0.025, 20]} />
          </mesh>
        ))}
      </group>
    </group>
  );
}

/** Two or three things from the map's own world. */
function Themed({ theme, m, left, mid, right }: { theme: Theme; m: Record<string, StudyModel>; left: At; mid: At; right: At }) {
  switch (theme) {
    case "china":
    case "japan":
      return (
        <>
          <Inkstone m={m.inkstone} at={left} />
          <Seal m={m.seal} at={right} />
          <Brush m={m.brush} at={mid} />
        </>
      );
    case "islamic":
    case "silk":
    case "mughal":
    case "medieval":
      return (
        <>
          <Astrolabe m={m.astrolabe} at={left} />
          <Quill m={m.quill} at={mid} />
          {theme !== "medieval" && <Dividers m={m.dividers} at={right} />}
        </>
      );
    case "renaissance":
      return (
        <>
          <Dividers m={m.dividers} at={left} />
          <Quill m={m.quill} at={mid} />
          <Lens m={m.lens} at={right} />
        </>
      );
    case "neareast":
      return (
        <>
          <ClayTablet m={m["clay-tablet"]} at={left} />
          <Palette m={m.palette} at={mid} />
        </>
      );
    case "classical":
      return (
        <>
          <WaxTablet m={m["wax-tablet"]} at={left} />
          <Scroll m={m.scroll} at={right} />
        </>
      );
    case "india":
      return (
        <>
          <PalmLeaf m={m["palm-leaf"]} at={left} />
          <Reed m={m.reed} at={mid} />
        </>
      );
    case "africa":
      return (
        <>
          <PalmLeaf m={m.manuscript} at={left} africa />
          <Reed m={m.reed} at={mid} />
        </>
      );
    case "americas":
      return (
        <>
          <Quipu m={m.quipu} at={left} />
          <Codex m={m.codex} at={right} />
        </>
      );
  }
}

/** The engraved face of the astrolabe's plate: the limb's degree scale, circles of altitude and the horizon. */
const astroFace = () =>
  canvasTex("astro", 256, 256, (g) => {
    const grad = g.createRadialGradient(118, 110, 10, 128, 128, 128);
    grad.addColorStop(0, "#d4ae5c");
    grad.addColorStop(1, "#9a7632");
    g.fillStyle = grad;
    g.fillRect(0, 0, 256, 256);
    g.strokeStyle = "rgba(60,40,12,0.75)";
    g.lineWidth = 1;
    for (const r of [124, 110, 104]) (g.beginPath(), g.arc(128, 128, r, 0, Math.PI * 2), g.stroke());
    for (let i = 0; i < 72; i++) {
      const a = (i / 72) * Math.PI * 2, l = i % 6 ? 6 : 14;
      g.beginPath();
      g.moveTo(128 + Math.cos(a) * 124, 128 + Math.sin(a) * 124);
      g.lineTo(128 + Math.cos(a) * (124 - l), 128 + Math.sin(a) * (124 - l));
      g.stroke();
    }
    // the almucantars: circles of equal altitude, crowding toward the zenith
    for (let k = 0; k < 9; k++) {
      const r = 86 - k * 9, cy = 128 - k * 7;
      g.beginPath();
      g.arc(128, cy, r, 0, Math.PI * 2);
      g.stroke();
    }
    g.beginPath();
    g.moveTo(24, 128);
    g.lineTo(232, 128);
    g.moveTo(128, 24);
    g.lineTo(128, 232);
    g.stroke();
  });

function Astrolabe({ m, at }: { m: StudyModel; at: At }) {
  const tip = useTip({ id: "astrolabe", name: "An astrolabe", blurb: "A brass model of the sky: turn the star map (the rete) to the hour and it tells the time, the height of the sun and the direction of Mecca.", hint: "Click to turn the rete" });
  const rete = useRef<THREE.Group>(null);
  const { t, start } = usePulse(1.2);
  const turns = useRef(0);
  useFrame(() => {
    if (rete.current) rete.current.rotation.y = (turns.current - 1 + smooth(t.current)) * 0.9;
  });
  const r = m.anim_rete;
  return (
    <group position={at} rotation-y={0.3} {...tip} onClick={(e) => (e.stopPropagation(), turns.current++, start())}>
      <Part p={m.base} />
      <Part p={m.tex_face} material={texMat(astroFace())} />
      {r && (
        <group ref={rete} position={r.position}>
          <mesh geometry={r.geometry} material={vcMat} />
        </group>
      )}
    </group>
  );
}

function Dividers({ m, at }: { m: StudyModel; at: At }) {
  const tip = useTip({ id: "dividers", name: "A pair of dividers", blurb: "Set to the map's scale bar, they step off distances along a road or a coast.", hint: "Click to measure" });
  const a = useRef<THREE.Group>(null), b = useRef<THREE.Group>(null);
  const { t, start } = usePulse(1.1);
  useFrame(() => {
    const ang = 0.16 + (t.current < 1 ? Math.sin(t.current * Math.PI) : 0) * 0.35;
    if (a.current) a.current.rotation.y = ang;
    if (b.current) b.current.rotation.y = -ang;
  });
  return (
    <group position={[at[0], 0.007, at[2]]} rotation-y={-0.4} {...tip} onClick={(e) => (e.stopPropagation(), start())}>
      {m.anim_leg_a && (
        <group ref={a} position={m.anim_leg_a.position}>
          <mesh geometry={m.anim_leg_a.geometry} material={vcMat} />
        </group>
      )}
      {m.anim_leg_b && (
        <group ref={b} position={m.anim_leg_b.position}>
          <mesh geometry={m.anim_leg_b.geometry} material={vcMat} />
        </group>
      )}
      <Part p={m.base} />
    </group>
  );
}

function Quill({ m, at }: { m: StudyModel; at: At }) {
  const tip = useTip({ id: "quill", name: "Ink and a quill", blurb: "Oak-gall ink and a goose feather: map makers drew every coast and street by hand." });
  return (
    <group position={at} {...tip}>
      <Part p={m.base} />
    </group>
  );
}

function Lens({ m, at }: { m: StudyModel; at: At }) {
  const tip = useTip({ id: "lens", name: "A reading glass", blurb: "For the small print of an engraved plate: the street names and the scale." });
  return (
    <group position={[at[0], 0.008, at[2]]} rotation-y={0.6} {...tip}>
      <Part p={m.base} />
      <Part p={m.glass} material={glassMat} renderOrder={2} />
    </group>
  );
}

function Inkstone({ m, at }: { m: StudyModel; at: At }) {
  const tip = useTip({ id: "inkstone", name: "An inkstone", blurb: "A stick of pine-soot ink is ground with a little water on the stone, as scribes did for two thousand years." });
  return (
    <group position={at} rotation-y={0.15} {...tip}>
      <Part p={m.base} />
    </group>
  );
}

function Brush({ m, at }: { m: StudyModel; at: At }) {
  const tip = useTip({ id: "brush", name: "A writing brush", blurb: "Bamboo and goat hair: maps, poems and accounts were all written with the same brush." });
  return (
    <group position={at} {...tip}>
      <Part p={m.base} />
    </group>
  );
}

function Seal({ m, at }: { m: StudyModel; at: At }) {
  const tip = useTip({ id: "seal", name: "A name seal and red paste", blurb: "Stamped in cinnabar paste, a seal signed a map, a letter or a painting." });
  return (
    <group position={at} {...tip}>
      <Part p={m.base} />
    </group>
  );
}

/** Rows of wedges pressed into clay. */
const cuneiform = () =>
  canvasTex("cuneiform", 128, 176, (g) => {
    g.fillStyle = "#9a7a50";
    g.fillRect(0, 0, 128, 176);
    const r = rand(3);
    g.fillStyle = "rgba(50,32,16,0.6)";
    for (let y = 12; y < 170; y += 14) {
      g.fillRect(6, y + 10, 116, 1);
      for (let x = 10; x < 118; x += 5 + r() * 6) {
        g.beginPath();
        const v = r() > 0.6;
        if (v) (g.moveTo(x, y), g.lineTo(x + 4, y), g.lineTo(x + 2, y + 9));
        else (g.moveTo(x, y + 2), g.lineTo(x, y + 6), g.lineTo(x + 7, y + 4));
        g.fill();
      }
    }
  });

function ClayTablet({ m, at }: { m: StudyModel; at: At }) {
  const tip = useTip({ id: "tablet", name: "A clay tablet", blurb: "Wedge-shaped signs pressed into wet clay with a reed: the oldest known city plans, of Nippur and Babylon, were drawn this way." });
  return (
    <group position={at} {...tip}>
      <Part p={m.base} />
      <Part p={m.tex_face} material={texMat(cuneiform())} />
    </group>
  );
}

function Palette({ m, at }: { m: StudyModel; at: At }) {
  const tip = useTip({ id: "palette", name: "A scribe's palette", blurb: "A slip of wood with two wells, for black soot ink and red ochre, and a slot for the reed pens." });
  return (
    <group position={at} {...tip}>
      <Part p={m.base} />
    </group>
  );
}

function Reed({ m, at }: { m: StudyModel; at: At }) {
  const tip = useTip({ id: "reed", name: "A reed pen and ink pot", blurb: "A cut reed dipped in soot ink, the pen of scribes from Egypt to India." });
  return (
    <group position={at} {...tip}>
      <Part p={m.base} />
    </group>
  );
}

function WaxTablet({ m, at }: { m: StudyModel; at: At }) {
  const tip = useTip({ id: "wax", name: "A wax tablet and stylus", blurb: "Notes scratched in wax and smoothed away again: the Romans' scratch pad." });
  return (
    <group position={at} {...tip}>
      <Part p={m.base} />
    </group>
  );
}

/** Columns of writing on an opened papyrus. */
const papyrusText = () =>
  canvasTex("papyrus", 256, 96, (g) => {
    g.fillStyle = "#cdb47c";
    g.fillRect(0, 0, 256, 96);
    g.fillStyle = "rgba(80,58,30,0.12)";
    for (let x = 0; x < 256; x += 3) g.fillRect(x, 0, 1, 96);
    const r = rand(11);
    g.fillStyle = "rgba(30,22,14,0.7)";
    for (let c = 0; c < 4; c++) for (let y = 10; y < 86; y += 6) g.fillRect(14 + c * 60, y, 30 + r() * 14, 2);
  });

function Scroll({ m, at }: { m: StudyModel; at: At }) {
  const tip = useTip({ id: "papyrus", name: "A papyrus roll", blurb: "Books were rolls in the ancient world: read by unrolling with one hand and rolling up with the other." });
  return (
    <group position={at} {...tip}>
      <Part p={m.base} />
      <Part p={m.tex_sheet} material={texMat(papyrusText())} />
    </group>
  );
}

function PalmLeaf({ m, at, africa }: { m: StudyModel; at: At; africa?: boolean }) {
  const tip = useTip(
    africa
      ? { id: "manuscript", name: "A manuscript in its leather case", blurb: "Loose leaves of paper kept in a tooled leather wallet, as in the libraries of Timbuktu." }
      : { id: "palm-leaf", name: "A palm-leaf manuscript", blurb: "Strips of dried palm leaf, incised and inked, strung on a cord between wooden boards." },
  );
  return (
    <group position={at} {...tip}>
      <Part p={m.base} />
    </group>
  );
}

function Quipu({ m, at }: { m: StudyModel; at: At }) {
  const tip = useTip({ id: "quipu", name: "A quipu", blurb: "Knotted cords of cotton or wool: the Inca kept counts, and perhaps stories, in the kind and place of the knots." });
  return (
    <group position={at} {...tip}>
      <Part p={m.base} />
    </group>
  );
}

/** The codex's four painted panels side by side, one texture for the whole screenfold. */
const codexPanels = () =>
  canvasTex("codex", 384, 96, (g) => {
    for (let p = 0; p < 4; p++) {
      const ox = p * 96;
      g.fillStyle = "#d2c3a0";
      g.fillRect(ox, 0, 96, 96);
      const r = rand(5 + p);
      g.strokeStyle = "#8a2a1a";
      g.lineWidth = 2;
      g.strokeRect(ox + 6, 6, 84, 84);
      for (let i = 0; i < 6; i++) {
        g.fillStyle = ["#8a2a1a", "#1e1a16", "#c08a2a", "#3a6a5a"][Math.floor(r() * 4)];
        g.fillRect(ox + 12 + r() * 56, 12 + r() * 56, 8 + r() * 14, 8 + r() * 14);
      }
    }
  });

function Codex({ m, at }: { m: StudyModel; at: At }) {
  const tip = useTip({ id: "codex", name: "A screenfold codex", blurb: "A long strip of deerskin or bark paper, folded like a screen and painted on both sides." });
  return (
    <group position={at} {...tip}>
      <Part p={m.base} />
      <Part p={m.tex_panels} material={texMat(codexPanels())} />
    </group>
  );
}

/* ------------------------------------------------------------------ painted textures */

/** The table top: figured wood with crossbanded edges and stringing, and a tooled inset round the board. */
function paintTop(g: CanvasRenderingContext2D, W: number, H: number, theme: Theme, Tw: number, bw: number, bd: number) {
  const pal: Record<"wood" | "lacquer" | "walnut" | "oak", { wood: string; grain: string; inset: string; gilt: string }> = {
    wood: { wood: "#5a3822", grain: "#2e1a0e", inset: "#3a1a15", gilt: "#a8873e" },
    walnut: { wood: "#4e3020", grain: "#24140a", inset: "#22302a", gilt: "#a8873e" },
    oak: { wood: "#6a4a2a", grain: "#3a2614", inset: "#3a2a1e", gilt: "#9a7a3a" },
    lacquer: { wood: "#2a1a14", grain: "#140c08", inset: "#3a1512", gilt: "#a8873e" },
  };
  const p = pal[theme === "japan" || theme === "china" ? "lacquer" : theme === "renaissance" || theme === "islamic" || theme === "mughal" ? "walnut" : theme === "medieval" ? "oak" : "wood"];
  const px = W / Tw; // pixels per metre
  const r = rand(17);
  g.fillStyle = p.wood;
  g.fillRect(0, 0, W, H);
  // long grain, gently wavy, with a few darker figure lines
  for (let i = 0; i < 260; i++) {
    const y0 = r() * H, amp = 2 + r() * 6, fr = 0.002 + r() * 0.006, ph = r() * 6;
    g.strokeStyle = r() > 0.5 ? `rgba(0,0,0,${0.05 + r() * 0.1})` : `rgba(255,220,170,${0.02 + r() * 0.04})`;
    g.lineWidth = 0.6 + r() * 1.6;
    g.beginPath();
    for (let x = 0; x <= W; x += 16) g.lineTo(x, y0 + Math.sin(x * fr + ph) * amp);
    g.stroke();
  }
  for (let i = 0; i < 4; i++) {
    const x = r() * W, y = r() * H;
    g.strokeStyle = "rgba(20,10,4,0.25)";
    for (let k = 1; k < 5; k++) (g.beginPath(), g.ellipse(x, y, k * 7, k * 2.5, 0, 0, Math.PI * 2), g.stroke());
  }
  // crossbanding round the edge, its grain running across
  const band = 0.06 * px;
  g.fillStyle = p.wood;
  g.fillRect(0, 0, W, band), g.fillRect(0, H - band, W, band), g.fillRect(0, 0, band, H), g.fillRect(W - band, 0, band, H);
  g.lineWidth = 1;
  for (let x = 0; x < W; x += 3) {
    g.strokeStyle = `rgba(0,0,0,${0.04 + r() * 0.1})`;
    g.beginPath(), g.moveTo(x, 0), g.lineTo(x + r() * 3, band), g.moveTo(x, H - band), g.lineTo(x + r() * 3, H), g.stroke();
  }
  for (let y = 0; y < H; y += 3) {
    g.strokeStyle = `rgba(0,0,0,${0.04 + r() * 0.1})`;
    g.beginPath(), g.moveTo(0, y), g.lineTo(band, y + r() * 3), g.moveTo(W - band, y), g.lineTo(W, y + r() * 3), g.stroke();
  }
  // boxwood stringing either side of the band
  for (const [o, c] of [[band, "#c9a874"], [band + 3, "#1a0f08"], [4, "#c9a874"]] as const) {
    g.strokeStyle = c;
    g.lineWidth = 1.5;
    g.strokeRect(o, o, W - 2 * o, H - 2 * o);
  }
  // the inset: leather (lacquer in the east) round the board, with a tooled gilt border
  const iw = (bw + 0.14) * px, id = (bd + 0.14) * px;
  const ix = (W - iw) / 2, iy = (H - id) / 2;
  g.fillStyle = p.inset;
  g.fillRect(ix, iy, iw, id);
  for (let i = 0; i < 1600; i++) (g.fillStyle = `rgba(${r() > 0.5 ? "255,230,200" : "0,0,0"},${r() * 0.05})`), g.fillRect(ix + r() * iw, iy + r() * id, 3, 3);
  g.strokeStyle = p.gilt;
  g.lineWidth = 1.4;
  const m1 = 0.012 * px, m2 = 0.024 * px;
  g.strokeRect(ix + m1, iy + m1, iw - 2 * m1, id - 2 * m1);
  g.lineWidth = 0.8;
  g.strokeRect(ix + m2, iy + m2, iw - 2 * m2, id - 2 * m2);
  g.fillStyle = p.gilt;
  const mid = (m1 + m2) / 2, step = 0.02 * px;
  for (let x = ix + m2; x < ix + iw - m2; x += step) g.fillRect(x, iy + mid - 1, 2, 2), g.fillRect(x, iy + id - mid - 1, 2, 2);
  for (let y = iy + m2; y < iy + id - m2; y += step) g.fillRect(ix + mid - 1, y, 2, 2), g.fillRect(ix + iw - mid - 1, y, 2, 2);
  g.strokeStyle = "#140a05";
  g.lineWidth = 2;
  g.strokeRect(ix, iy, iw, id);
  // wear: the edges handled darker, a few pale scratches
  const v = g.createRadialGradient(W / 2, H / 2, Math.min(W, H) * 0.3, W / 2, H / 2, Math.max(W, H) * 0.62);
  v.addColorStop(0, "rgba(0,0,0,0)");
  v.addColorStop(1, "rgba(0,0,0,0.35)");
  g.fillStyle = v;
  g.fillRect(0, 0, W, H);
  g.strokeStyle = "rgba(255,230,190,0.07)";
  g.lineWidth = 1;
  for (let i = 0; i < 40; i++) {
    const x = r() * W, y = r() * H, a = r() * Math.PI;
    g.beginPath(), g.moveTo(x, y), g.lineTo(x + Math.cos(a) * 30, y + Math.sin(a) * 30), g.stroke();
  }
}

/** A soft dark rim round a rectangle `m` pixels in from each side: the board's shadow. */
function paintShadow(g: CanvasRenderingContext2D, W: number, H: number, m: number) {
  g.clearRect(0, 0, W, H);
  g.shadowColor = "rgba(0,0,0,0.7)";
  g.shadowBlur = m * 0.8;
  g.shadowOffsetX = W * 2;
  g.fillStyle = "#000";
  g.fillRect(m * 0.75 - W * 2, m * 0.8, W - m * 1.5, H - m * 1.5);
}
