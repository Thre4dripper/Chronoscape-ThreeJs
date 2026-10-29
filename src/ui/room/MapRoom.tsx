import { useEffect, useMemo, useRef, useState } from "react";
import { Canvas, useFrame, useThree } from "@react-three/fiber";
import { Sparkles } from "@react-three/drei";
import * as THREE from "three";
import { atlasCatalog } from "@/content/registry";
import { playableMaps, useNav } from "@/nav";
import { Cabinet, cabinetSize } from "./Cabinet";
import { Globe } from "./Globe";
import { toon, WOOD, WOOD_DARK, WOOD_LIGHT, fontsReady } from "./toon";
import { mergeGeometries } from "three/addons/utils/BufferGeometryUtils.js";
import { Desk, GLOBE_AT, LAMP_AT } from "./Desk";
import { Portraits } from "./Portraits";
import { Register, RoomTip } from "./Register";
import { useRoom } from "./roomState";
import { AtlasCard } from "./AtlasCard";
import { EraRuler } from "./EraRuler";

/**
 * The map room: a cartoon library corner with the map cabinet, a globe on a
 * reading desk and a shaft of light from a high window. Atlases are taken
 * from the shelf by hovering and clicking (or from the era ruler below); an
 * opened atlas shows its maps on a card, and a map unfolds into its city.
 */
export default function MapRoom() {
  const atlases = atlasCatalog.atlases;
  const openId = useNav((s) => s.atlasId);
  const openAtlas = useNav((s) => s.openAtlas);
  const goTitle = useNav((s) => s.goTitle);
  const hoverId = useRoom((s) => s.hoverId);
  const evening = useRoom((s) => s.evening);
  const [ready, setReady] = useState(false);
  useEffect(() => {
    void fontsReady().then(() => setReady(true));
    return () => {
      useRoom.getState().setHover(null);
      document.body.style.cursor = "";
    };
  }, []);
  useEffect(() => {
    const onKey = (e: KeyboardEvent) => {
      if (e.key !== "Escape" || e.defaultPrevented) return;
      if (useNav.getState().atlasId) openAtlas(null);
    };
    addEventListener("keydown", onKey);
    return () => removeEventListener("keydown", onKey);
  }, [openAtlas]);
  // putting an atlas back leaves nothing hovered (the pointer is over the card, not the shelf)
  useEffect(() => {
    if (!openId) useRoom.getState().setHover(null);
    useRoom.getState().setTip(null);
  }, [openId]);
  const focus = atlases.find((a) => a.id === (openId ?? hoverId)) ?? null;
  const hovered = !openId ? atlases.find((a) => a.id === hoverId) ?? null : null;

  return (
    <div className={`room ${openId ? "has-open" : ""} ${evening ? "is-evening" : ""}`}>
      <Canvas
        className="room__canvas"
        shadows
        dpr={[1, 1.75]}
        camera={{ fov: 30, near: 0.4, far: 80, position: [0, 3, 12] }}
        gl={{ antialias: true }}
        onPointerMissed={(e) => {
          useRoom.getState().setHover(null);
          useRoom.getState().setTip(null);
          // a click on empty space in the room puts an open atlas back on the shelf
          if (e.type === "click" && useNav.getState().atlasId) openAtlas(null);
        }}
      >
        <color attach="background" args={["#d8c299"]} />
        <fog attach="fog" args={["#d8c299", 16, 34]} />
        {ready && <Room atlases={atlases} focus={focus} openId={openId} onOpen={(id) => openAtlas(id)} />}
      </Canvas>
      <div className="room__vignette" aria-hidden="true" />

      <header className="room__top">
        <button className="room__back" onClick={goTitle}>
          <span aria-hidden="true">←</span> <span className="room__back-text">Title page</span>
        </button>
        <div className="room__heading">
          <div className="room__kicker">Chronoscape</div>
          <h1>The Map Room</h1>
          <p>Twelve atlases. Take one from the shelf.</p>
        </div>
      </header>

      {!openId && <RoomLabel hovered={hovered} />}

      <EraRuler atlases={atlases} />

      {openId && <AtlasCard key={openId} atlas={atlases.find((a) => a.id === openId)!} index={atlases.findIndex((a) => a.id === openId)} onClose={() => openAtlas(null)} />}

      <RoomTip />
      <Register />

      {/* the same shelf as a plain list, for keyboards and screen readers */}
      <nav className="sr-only" aria-label="Atlases">
        <ul>
          {atlases.map((a) => (
            <li key={a.id}>
              <button onClick={() => openAtlas(a.id)} onFocus={() => useRoom.getState().setHover(a.id)}>
                {a.title}, {a.era}
              </button>
            </li>
          ))}
        </ul>
      </nav>
    </div>
  );
}

/** The museum label beside the cabinet: the hovered atlas, or how the room works. */
function RoomLabel({ hovered }: { hovered: (typeof atlasCatalog.atlases)[number] | null }) {
  if (!hovered) {
    const ready = playableMaps();
    const names = [...new Set(ready.map((r) => r.map.title))];
    return (
      <aside className="room__hover room__hover--idle" data-hud-block>
        <div className="room__hover-era">How to use the room</div>
        <p>Point at an atlas to read about it. Click to take it down and see the maps folded inside. The ribbons below show the centuries each atlas covers.</p>
        <div className="room__ready">
          <span>{ready.length} maps ready to unfold</span>
          <p className="room__ready-list">
            {names.map((n, i) => {
              const k = ready.filter((r) => r.map.title === n).length;
              return (
                <span key={n}>
                  <strong>
                    {n}
                    {k > 1 && <em> ×{k}</em>}
                  </strong>
                  {i < names.length - 1 ? " · " : ""}
                </span>
              );
            })}
          </p>
        </div>
      </aside>
    );
  }
  const n = hovered.maps.filter((m) => m.city).length;
  return (
    <aside className="room__hover" data-hud-block key={hovered.id} style={{ ["--tie" as string]: hovered.color }}>
      <div className="room__hover-era">{hovered.era}</div>
      <h2>{hovered.title}</h2>
      <div className="room__hover-region">{hovered.region}</div>
      <p>{hovered.blurb}</p>
      <ul className="room__hover-maps">
        {hovered.maps.map((m) => (
          <li key={m.title} className={m.city ? "is-ready" : ""}>
            {m.title}
            <em>{m.subtitle.split(", ").pop()}</em>
          </li>
        ))}
      </ul>
      <div className="room__hover-count">{n ? `${n} of ${hovered.maps.length} ready to unfold` : "All in preparation"}</div>
    </aside>
  );
}

function Room({ atlases, focus, openId, onOpen }: { atlases: typeof atlasCatalog.atlases; focus: (typeof atlasCatalog.atlases)[number] | null; openId: string | null; onOpen: (id: string) => void }) {
  const { size } = useThree();
  const portrait = size.width / size.height < 1;
  const cols = portrait ? 3 : 4;
  const rows = Math.ceil(atlases.length / cols);
  const cab = cabinetSize(cols, rows);
  const totalH = cab.h + cab.cornice + cab.plinth + 0.3;
  const desk = new THREE.Vector3(cab.w / 2 + 1.6, 0, 1.3);
  return (
    <>
      <Lights lamp={desk.clone().add(LAMP_AT).add(new THREE.Vector3(0, 0.42, 0))} />
      <CameraRig totalH={totalH} cabW={cab.w} portrait={portrait} open={!!openId} />
      <Walls />
      <Cabinet atlases={atlases} cols={cols} openId={openId} onOpen={onOpen} />
      {!portrait && (
        <>
          <Desk at={[desk.x, desk.y, desk.z]} />
          <Globe atlas={focus} at={[desk.x + GLOBE_AT.x, GLOBE_AT.y, desk.z + GLOBE_AT.z]} />
          <Portraits x0={cab.w / 2 + 0.35} x1={cab.w / 2 + 3.85} y0={3.05} y1={Math.min(totalH - 0.55, 5.6)} z={-0.5} only={["rome", "constantinople", "delhi", "edo"]} />
          <LightShaft at={[-cab.w / 2 - 0.6, 3.2, 0.6]} />
        </>
      )}
      <Sparkles count={60} scale={[8, 5, 3]} position={[-1, 3, 1.5]} size={2.2} speed={0.25} opacity={0.5} color="#fff3d2" />
    </>
  );
}

/** Daylight from the high window, or (with the lamp lit) a warm evening around the desk. */
function Lights({ lamp }: { lamp: THREE.Vector3 }) {
  const evening = useRoom((s) => s.evening);
  const hemi = useRef<THREE.HemisphereLight>(null);
  const sun = useRef<THREE.DirectionalLight>(null);
  const glow = useRef<THREE.PointLight>(null);
  const { scene } = useThree();
  const day = useMemo(() => new THREE.Color("#d8c299"), []);
  const dusk = useMemo(() => new THREE.Color("#3b2a1d"), []);
  const k = useRef(0);
  useFrame((s, dt) => {
    k.current += ((evening ? 1 : 0) - k.current) * (1 - Math.exp(-3 * Math.min(dt, 0.05)));
    const e = k.current;
    if (hemi.current) hemi.current.intensity = 1.15 - 0.8 * e;
    if (sun.current) sun.current.intensity = 2.1 - 1.8 * e;
    if (glow.current) glow.current.intensity = e * (16 + Math.sin(s.clock.elapsedTime * 11) * 0.8 + Math.sin(s.clock.elapsedTime * 4.3) * 0.6);
    if (scene.background instanceof THREE.Color) scene.background.copy(day).lerp(dusk, e);
    if (scene.fog) scene.fog.color.copy(day).lerp(dusk, e);
    shaftOpacity.value = 1 - e;
  });
  return (
    <>
      <hemisphereLight ref={hemi} args={["#fff1d6", "#6b4a2e", 1.15]} />
      <directionalLight
        ref={sun}
        position={[-5, 8, 7]}
        intensity={2.1}
        color="#ffe2b0"
        castShadow
        shadow-mapSize={[2048, 2048]}
        shadow-camera-left={-8}
        shadow-camera-right={8}
        shadow-camera-top={8}
        shadow-camera-bottom={-2}
        shadow-bias={-0.0006}
        shadow-normalBias={0.03}
      />
      <pointLight ref={glow} position={lamp} intensity={0} distance={11} decay={1.4} color="#ffb764" />
    </>
  );
}
const shaftOpacity = { value: 1 };

/** Frames the cabinet beside the label column and above the ruler; follows the pointer a little (less when an atlas is held). */
function CameraRig({ totalH, cabW, portrait, open }: { totalH: number; cabW: number; portrait: boolean; open: boolean }) {
  const { camera, size } = useThree();
  const pointer = useRef({ x: 0, y: 0 });
  useEffect(() => {
    const move = (e: PointerEvent) => {
      pointer.current.x = (e.clientX / innerWidth) * 2 - 1;
      pointer.current.y = (e.clientY / innerHeight) * 2 - 1;
    };
    addEventListener("pointermove", move);
    return () => removeEventListener("pointermove", move);
  }, []);
  const look = useMemo(() => new THREE.Vector3(), []);
  const want = useMemo(() => ({ pos: new THREE.Vector3(), look: new THREE.Vector3() }), []);
  const intro = useRef(0);
  // the screen band the cabinet must fit in: below the header, above the era ruler
  const band = useRef({ top: 24, bottom: 170, left: 0, at: 0 });
  useFrame((_, dtRaw) => {
    const now = performance.now();
    if (now - band.current.at > 500) {
      // measure the HUD the scene must stay clear of: the ruler below, the heading and label on the left (or above, on a phone)
      band.current.at = now;
      const r = document.querySelector(".ruler")?.getBoundingClientRect();
      band.current.bottom = r && r.height > 0 ? innerHeight - r.top + 12 : 24; // a hidden ruler (short screens) takes no room
      const boxes = [".room__heading", ".room__back", ".room__hover"].map((q) => document.querySelector(q)?.getBoundingClientRect()).filter((b): b is DOMRect => !!b);
      if (portrait) {
        band.current.left = 0;
        band.current.top = Math.max(24, ...boxes.filter((b) => b.width > 0).map((b) => b.bottom + 6));
      } else {
        band.current.top = 24;
        band.current.left = Math.min(0.45, (Math.max(0, ...boxes.map((b) => b.right)) + 24) / size.width);
      }
    }
    const dt = Math.min(dtRaw, 0.05);
    intro.current = Math.min(1, intro.current + dt / 1.6);
    const cam = camera as THREE.PerspectiveCamera;
    const aspect = size.width / size.height;
    const vfov = (cam.fov * Math.PI) / 180;
    // fit the cabinet (and the desk beside it on wide screens) with a margin
    const sceneW = portrait ? cabW + 0.6 : cabW + 4.4;
    const H = size.height;
    const frac = Math.max(0.4, (H - band.current.top - band.current.bottom) / H); // share of the screen height
    const mid = (band.current.bottom - band.current.top) / H; // band centre above screen centre, in NDC
    const distH = (totalH / 2 + 0.35) / (Math.tan(vfov / 2) * frac);
    // on wide screens the left of the screen holds the heading and the label: the scene fits to its right
    const left = band.current.left;
    const distW = (sceneW / 2) / (Math.tan(vfov / 2) * aspect * (1 - left));
    const dist = Math.max(distH, distW);
    const sceneCx = portrait ? 0 : 1.75;
    const cx = sceneCx - left * dist * Math.tan(vfov / 2) * aspect;
    const lookY = totalH / 2 - 0.15 - mid * dist * Math.tan(vfov / 2);
    // the camera stays put when an atlas is opened: the atlas comes to the viewer instead
    want.look.set(cx, lookY, 0);
    want.pos.set(cx, lookY + 0.4, dist);
    // a slow dolly in when the room first appears
    const e = 1 - Math.pow(1 - intro.current, 3);
    want.pos.z += (1 - e) * 4;
    want.pos.y += (1 - e) * 0.8;
    const sway = open ? 0.08 : 1;
    want.pos.x += pointer.current.x * 0.35 * sway;
    want.pos.y -= pointer.current.y * 0.2 * sway;
    const k = 1 - Math.exp(-3.5 * dt);
    cam.position.lerp(want.pos, k);
    look.lerp(want.look, k);
    cam.lookAt(look);
  });
  return null;
}

function Walls() {
  const wall = useMemo(() => wallTexture(), []);
  useEffect(() => () => wall.dispose(), [wall]);
  // oak wainscot panelling round the lower wall, with a chair rail
  const wainscot = useMemo(() => {
    const gs: THREE.BufferGeometry[] = [new THREE.BoxGeometry(40, 1.15, 0.04).translate(0, 0.575, -0.58)];
    const panels: THREE.BufferGeometry[] = [];
    for (let x = -19.5; x < 20; x += 0.95) panels.push(new THREE.BoxGeometry(0.75, 0.7, 0.025).translate(x, 0.62, -0.555));
    const rail = new THREE.BoxGeometry(40, 0.07, 0.09).translate(0, 1.17, -0.56);
    return { back: mergeGeometries(gs)!, panels: mergeGeometries(panels)!, rail };
  }, []);
  useEffect(() => () => Object.values(wainscot).forEach((g) => g.dispose()), [wainscot]);
  return (
    <group>
      <mesh position={[0, 6, -0.6]} receiveShadow>
        <planeGeometry args={[40, 16]} />
        <meshToonMaterial map={wall} />
      </mesh>
      <mesh rotation={[-Math.PI / 2, 0, 0]} position={[0, 0, 6]} receiveShadow>
        <planeGeometry args={[40, 14]} />
        <meshToonMaterial color="#6e4a2e" />
      </mesh>
      <mesh geometry={wainscot.back} material={toon(WOOD_DARK)} receiveShadow />
      <mesh geometry={wainscot.panels} material={toon(WOOD)} receiveShadow />
      <mesh geometry={wainscot.rail} material={toon(WOOD_LIGHT)} receiveShadow />
    </group>
  );
}

/** Striped damask wallpaper and floorboards, drawn once. */
function wallTexture() {
  const c = document.createElement("canvas");
  c.width = 512;
  c.height = 512;
  const g = c.getContext("2d")!;
  g.fillStyle = "#cfb488";
  g.fillRect(0, 0, 512, 512);
  for (let x = 0; x < 512; x += 64) {
    g.fillStyle = "rgba(255,240,205,0.22)";
    g.fillRect(x, 0, 30, 512);
    g.fillStyle = "rgba(120,80,40,0.08)";
    g.fillRect(x + 30, 0, 2, 512);
  }
  for (let y = 32; y < 512; y += 96)
    for (let x = 15; x < 512; x += 64) {
      g.fillStyle = "rgba(140,90,50,0.16)";
      g.beginPath();
      g.ellipse(x, y, 6, 10, 0, 0, Math.PI * 2);
      g.fill();
    }
  const t = new THREE.CanvasTexture(c);
  t.wrapS = t.wrapT = THREE.RepeatWrapping;
  t.repeat.set(10, 4);
  t.colorSpace = THREE.SRGBColorSpace;
  return t;
}

/** Sunlight from a high window: a soft additive wedge. */
function LightShaft({ at }: { at: [number, number, number] }) {
  const mat = useMemo(
    () =>
      new THREE.ShaderMaterial({
        transparent: true,
        depthWrite: false,
        blending: THREE.AdditiveBlending,
        uniforms: { uTime: { value: 0 }, uOpacity: shaftOpacity },
        vertexShader: "varying vec2 vUv; void main(){ vUv = uv; gl_Position = projectionMatrix * modelViewMatrix * vec4(position,1.0); }",
        fragmentShader:
          "varying vec2 vUv; uniform float uTime; uniform float uOpacity; void main(){ float edge = smoothstep(0.0,0.25,vUv.x)*smoothstep(1.0,0.75,vUv.x); float fall = smoothstep(0.0,0.9,vUv.y); float flick = 0.9 + 0.1*sin(uTime*0.7 + vUv.y*6.0); gl_FragColor = vec4(vec3(1.0,0.9,0.7)*0.22*edge*fall*flick*uOpacity, 1.0); }",
      }),
    [],
  );
  useFrame((s) => (mat.uniforms.uTime.value = s.clock.elapsedTime));
  return (
    <mesh position={at} rotation={[0.1, 0.5, -0.5]} material={mat}>
      <planeGeometry args={[2.2, 7.5]} />
    </mesh>
  );
}
