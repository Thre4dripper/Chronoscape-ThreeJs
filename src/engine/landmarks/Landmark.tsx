import { useEffect, useMemo, useRef, useState } from "react";
import { useFrame, type ThreeEvent } from "@react-three/fiber";
import * as THREE from "three";
import type { City, Landmark as LandmarkDef } from "@/content/schema";
import { useStore, resolveVariant, landmarkForEvent } from "../store";
import { frameOf, mapToWorld, degToRad } from "../coords";
import { damp, prefersReducedMotion } from "../motion";
import { Kit } from "./kits";
import { RevealContext } from "./kits/shared";
import { GlbModel } from "./GlbModel";
import { ShadowDecal } from "./ShadowDecal";

const HOVER_EXIT_DELAY = 220;

/**
 * One landmark on the map. Owns its emergence progress (0 = embossed proxy,
 * 1 = fully risen) and damps it toward a target derived from the store, so
 * hover/focus/period changes are all interruptible and never queue.
 */
export function Landmark({ city, def }: { city: City; def: LandmarkDef }) {
  const f = frameOf(city);
  const [x, , z] = mapToWorld(f, def.position);
  const s = f.scale * def.scale;
  const progress = useRef(0);
  const ring = useRef<THREE.Mesh>(null);
  const root = useRef<THREE.Group>(null);
  const exitTimer = useRef<number | null>(null);
  const periodId = useStore((st) => st.periodId);
  // a monument standing inside a larger one (a mosque in the Round City, temples in a sacred precinct)
  // rises with it, so the bigger model's courts never bury it
  const outer = useMemo(() => enclosing(city, def), [city, def]);
  const hovered = useStore((st) => st.hoveredId === def.id || (!!st.hoveredId && outer.includes(st.hoveredId)));
  const withOuter = useStore((st) => !!st.focusedId && outer.includes(st.focusedId));
  // focused directly, or an event happening here is focused (from its marker, a story or the panel)
  const focused = useStore((st) => st.focusedId === def.id || (!!st.focusedEventId && landmarkForEvent(city, st.focusedEventId) === def.id));
  const active = !!periodId && def.activePeriods.includes(periodId);
  const variant = resolveVariant(def, periodId);
  const ctx = useMemo(() => ({ progress, mode: def.reveal }), [def.reveal]);

  const target = !active ? -0.3 : focused || hovered || withOuter ? 1 : 0;
  // the 3D model only exists while it is wanted (hover / focus) or still animating out
  const [mounted, setMounted] = useState(false);

  useFrame((_, dt) => {
    const rate = prefersReducedMotion() ? 1000 : target > progress.current ? 4.5 : 3;
    progress.current = damp(progress.current, target, rate, Math.min(dt, 0.05));
    const p = Math.max(0, progress.current);
    if (root.current) {
      // Absent-in-this-period landmarks sink below the paper and vanish.
      const sink = Math.min(0, progress.current) * 3;
      root.current.position.y = sink * s * 10;
      root.current.visible = progress.current > -0.28;
      const want = target > 0 || progress.current > 0.003;
      if (want !== mounted) setMounted(want);
    }
    if (ring.current) {
      const m = ring.current.material as THREE.MeshBasicMaterial;
      m.opacity = p * 0.55;
      ring.current.visible = p > 0.01;
      ring.current.scale.setScalar(1 + (1 - p) * 0.15);
    }
  });

  useEffect(
    () => () => {
      if (exitTimer.current) window.clearTimeout(exitTimer.current);
    },
    [],
  );

  const onOver = (e: ThreeEvent<PointerEvent>) => {
    e.stopPropagation();
    if (!active) return;
    if (exitTimer.current) {
      window.clearTimeout(exitTimer.current);
      exitTimer.current = null;
    }
    useStore.getState().hover(def.id);
    document.body.style.cursor = "pointer";
  };
  const onOut = (e: ThreeEvent<PointerEvent>) => {
    e.stopPropagation();
    document.body.style.cursor = "";
    exitTimer.current = window.setTimeout(() => {
      const st = useStore.getState();
      if (st.hoveredId === def.id) st.hover(null);
    }, HOVER_EXIT_DELAY);
  };
  const onClick = (e: ThreeEvent<MouseEvent>) => {
    e.stopPropagation();
    if (!active) return;
    const st = useStore.getState();
    // Touch: first tap previews, second tap enters.
    if (st.touch && st.hoveredId !== def.id && st.focusedId !== def.id) {
      st.hover(def.id);
      return;
    }
    if (st.focusedId !== def.id) st.focus(def.id);
  };

  const [fw, fd] = [def.footprint[0] * s, def.footprint[1] * s];
  const ringR = Math.max(fw, fd) * 0.62;

  return (
    <group position={[x, 0, z]} rotation-y={-degToRad(def.rotation)}>
      <group ref={root} onPointerOver={onOver} onPointerOut={onOut} onClick={onClick}>
        {/* invisible hit area so the proxy state is as hoverable as the full model */}
        <mesh position-y={0.02 * s * 10} visible={false}>
          <boxGeometry args={[fw, Math.max(0.05, s * 8), fd]} />
          <meshBasicMaterial />
        </mesh>
        <group scale={[s, s, s]}>
          <RevealContext.Provider value={ctx}>
            {mounted && ("glb" in variant.model ? <GlbModel key={variant.model.glb} url={`/${variant.model.glb}`} fallback={variant.model.fallback} /> : <Kit key={variant.model.kit} params={variant.model} />)}
            {mounted && "glb" in variant.model && <ShadowDecal key={`sh:${variant.model.glb}`} glb={variant.model.glb} />}
          </RevealContext.Provider>
        </group>
      </group>
      <mesh ref={ring} rotation-x={-Math.PI / 2} position-y={0.012}>
        <ringGeometry args={[ringR * 0.92, ringR, 48]} />
        <meshBasicMaterial color="#6F4D34" transparent opacity={0} depthWrite={false} />
      </mesh>
    </group>
  );
}

const enclosers = new WeakMap<LandmarkDef, string[]>();
/** Larger landmarks whose footprint contains this one's centre. */
function enclosing(city: City, def: LandmarkDef): string[] {
  let out = enclosers.get(def);
  if (out) return out;
  const area = def.footprint[0] * def.footprint[1] * def.scale * def.scale;
  out = city.landmarks
    .filter((o) => o !== def && o.footprint[0] * o.footprint[1] * o.scale * o.scale > area * 1.5)
    .filter((o) => {
      const a = (-o.rotation * Math.PI) / 180;
      const dx = def.position[0] - o.position[0], dy = def.position[1] - o.position[1];
      const u = dx * Math.cos(a) - dy * Math.sin(a), v = dx * Math.sin(a) + dy * Math.cos(a);
      return Math.abs(u) <= (o.footprint[0] * o.scale) / 2 && Math.abs(v) <= (o.footprint[1] * o.scale) / 2;
    })
    .map((o) => o.id);
  enclosers.set(def, out);
  return out;
}
