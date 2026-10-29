import { Suspense, useEffect, useMemo, useRef } from "react";
import { Canvas, useFrame, useThree } from "@react-three/fiber";
import * as THREE from "three";
import type { City } from "@/content/schema";
import { ParchmentMap } from "./map/ParchmentMap";
import { MapFeatures } from "./map/MapFeatures";
import { Landmark } from "./landmarks/Landmark";
import { CameraRig } from "./camera/CameraRig";
import { Figures } from "./activity/Figures";
import { HoverMassing } from "./map/HoverMassing";
import { TouchLens } from "./map/LensRing";
import { Study } from "./map/Study";
import { LifeProps } from "./map/LifeProps";
import { AreaPopout } from "./map/AreaPopout";
import { LinePopout } from "./map/LinePopout";
import { StreetLife } from "./map/StreetLife";
import { OverlayProjector } from "./overlay/Projector";
import { Smoke } from "./effects/Smoke";
import { useStore, currentFocus, landmarkById, eventById } from "./store";
import { frameOf, mapToWorld } from "./coords";
import { bakedMaterial, dayTint, tintForHour } from "./render/baked";
import { warmupMaterials } from "./render/warmup";

export function Scene({ city }: { city: City }) {
  const f = frameOf(city);
  const span = Math.max(f.width, f.height) * f.scale;
  const ortho = city.camera?.projection === "orthographic";
  const focusedId = useStore((s) => s.focusedId);
  const focusedSpotId = useStore((s) => s.focusedSpotId);
  const focusedEventId = useStore((s) => s.focusedEventId);
  const periodId = useStore((s) => s.periodId);
  const focus = useMemo(() => currentFocus({ city, focusedId, focusedSpotId, focusedEventId, periodId }), [city, focusedId, focusedSpotId, focusedEventId, periodId]);
  const hour = useStore((s) => s.hour);
  const desk = useStore((s) => s.desk);
  const landmark = landmarkById(city, focusedId);
  const event = eventById(city, focusedEventId);

  let figures: { center: [number, number]; radius: number; count: number; scale: number } | null = null;
  if (focus?.kind === "landmark" && landmark?.activity) figures = { center: landmark.position, radius: landmark.activity.radius, count: landmark.activity.figures, scale: Math.max(1, landmark.scale * 0.8) };

  else if (focus?.kind === "event" && event) figures = { center: focus.position, radius: Math.max(40, focus.size * 0.8), count: event.effect === "crowd" || event.effect === "procession" ? 90 : 24, scale: 1.4 };

  const night = hour < 6 || hour > 20;
  const bg = night ? "#0c0907" : "#17110c";

  return (
    <Canvas
      dpr={[1, 1.5]}
      gl={{ antialias: true, toneMapping: THREE.NoToneMapping, powerPreference: "high-performance" }}
      onCreated={({ gl, camera, size, scene }) => {
        // in production don't block on shader error checks
        gl.debug.checkShaderErrors = import.meta.env.DEV;
        if (import.meta.env.DEV) {
          const w = window as unknown as Record<string, unknown>;
          w.__gl = gl;
          w.__scene = scene;
          // dev probe: map units -> screen pixels, for scripted hover checks
          w.__project = (mx: number, my: number) => {
            const [x, , z] = mapToWorld(f, [mx, my]);
            const v = new THREE.Vector3(x, 0, z).project(camera);
            return [Math.round(((v.x + 1) / 2) * size.width), Math.round(((1 - v.y) / 2) * size.height)];
          };
        }
      }}
      orthographic={ortho}
      camera={ortho ? { near: 0.1, far: span * 6, position: [0, span, span] } : { fov: 28, near: 0.1, far: span * 6, position: [0, span, span] }}
      onPointerMissed={() => {
        const st = useStore.getState();
        if (st.mode === "previewing") st.hover(null);
      }}
      style={{ background: bg, transition: "background 1s" }}
    >
      <DayTint />
      <ShaderWarmup />
      {desk && <Study city={city} />}
      <ParchmentMap city={city} />
      <MapFeatures city={city} />
      {city.landmarks.map((l) => (
        <Landmark key={l.id} city={city} def={l} />
      ))}
      {figures && <Figures key={`${focus!.kind}:${focus!.id}`} city={city} center={figures.center} radius={figures.radius} count={figures.count} visualScale={figures.scale} />}
      {event && event.effect === "fire" && focus && <Smoke position={mapToWorld(f, focus.position)} size={Math.max(0.4, focus.size * f.scale * 0.5)} />}
      <HoverMassing city={city} />
      <TouchLens city={city} />
      <Suspense fallback={null}>
        <LifeProps city={city} />
        <AreaPopout city={city} />
        <LinePopout city={city} />
        <StreetLife city={city} />
      </Suspense>
      <OverlayProjector />
      <CameraRig city={city} />
    </Canvas>
  );
}

/** The day clock: one tint shared by every unlit material (map, baked models, props). */
function DayTint() {
  const target = useMemo(() => new THREE.Color(), []);
  useFrame((_, dt) => {
    tintForHour(useStore.getState().hour, target);
    const c = dayTint.value;
    const k = 1 - Math.exp(-3 * Math.min(dt, 0.1));
    if (Math.abs(c.r - target.r) + Math.abs(c.g - target.g) + Math.abs(c.b - target.b) > 0.002) c.lerp(target, k);
  });
  return null;
}

/**
 * Compile every shader program the app will ever need in the background,
 * right after the map appears, so the first hover or click never stalls on
 * shader compilation.
 */
function ShaderWarmup() {
  const { gl, scene, camera } = useThree();
  const done = useRef(false);
  useEffect(() => {
    if (done.current) return;
    done.current = true;
    const group = new THREE.Group();
    group.position.y = -50; // below the board, never seen
    const box = new THREE.BoxGeometry(1, 1, 1);
    const tex = new THREE.DataTexture(new Uint8Array([255, 255, 255, 255]), 1, 1);
    tex.needsUpdate = true;
    const add = (o: THREE.Object3D) => group.add(o);
    const inst = (m: THREE.Material, color: boolean) => {
      const im = new THREE.InstancedMesh(box, m, 1);
      if (color) im.setColorAt(0, new THREE.Color(1, 1, 1));
      return im;
    };
    for (const m of warmupMaterials()) {
      add(new THREE.Mesh(box, m));
      add(inst(m, false));
      add(inst(m, true));
    }
    add(new THREE.Mesh(box, bakedMaterial({ map: tex, key: "tex" })));
    add(new THREE.Mesh(box, bakedMaterial({ map: tex, transparent: true, depthWrite: false, polygonOffset: 1 })));
    add(new THREE.Mesh(box, bakedMaterial({ map: tex, transparent: true, key: "tex" })));
    add(new THREE.Mesh(box, new THREE.MeshBasicMaterial({ transparent: true, side: THREE.DoubleSide, depthWrite: false })));
    add(new THREE.Mesh(box, new THREE.MeshBasicMaterial({ transparent: true, depthWrite: false })));
    add(new THREE.LineSegments(new THREE.EdgesGeometry(box), new THREE.LineBasicMaterial({ transparent: true })));
    add(new THREE.Line(new THREE.BufferGeometry().setFromPoints([new THREE.Vector3(), new THREE.Vector3(1, 0, 0)]), new THREE.LineBasicMaterial()));
    const pts = new THREE.BufferGeometry();
    pts.setAttribute("position", new THREE.Float32BufferAttribute([0, 0, 0], 3));
    add(new THREE.Points(pts, new THREE.PointsMaterial({ map: tex, transparent: true, depthWrite: false })));
    // compiled against the live scene's settings, but never added to it
    const run = () =>
      gl
        .compileAsync(group, camera, scene)
        .catch(() => undefined)
        .finally(() => {
          box.dispose();
          tex.dispose();
        });
    const idle = (window as Window & { requestIdleCallback?: (f: () => void) => number }).requestIdleCallback;
    // after the map has had time to appear
    setTimeout(() => (idle ? idle(run) : run()), 1200);
  }, [gl, scene, camera]);
  return null;
}
