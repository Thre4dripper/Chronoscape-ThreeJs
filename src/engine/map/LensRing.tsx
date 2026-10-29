import { useMemo, useRef } from "react";
import { useFrame } from "@react-three/fiber";
import * as THREE from "three";
import type { City } from "@/content/schema";
import { frameOf, mapToWorld } from "../coords";
import { useStore, type HoveredFeature } from "../store";
import { featurePick, touchLens } from "./touchLens";

/**
 * The lens a finger sets on the map (touchLens.ts): an inked ring on the paper where it rests, and the
 * road, river, wall or district under it is "hovered" so streets fill with life and bridges and boats rise,
 * as they do under a mouse.
 */
export function TouchLens({ city }: { city: City }) {
  const f = frameOf(city);
  const ring = useRef<THREE.Group>(null);
  const ray = useMemo(() => new THREE.Raycaster(), []);
  const down = useMemo(() => new THREE.Vector3(0, -1, 0), []);
  const from = useMemo(() => new THREE.Vector3(), []);
  const was = useRef(false);
  const last = useRef({ mx: NaN, my: NaN });

  useFrame(({ camera, clock }) => {
    const st = useStore.getState();
    const g = ring.current;
    const on = touchLens.active && st.mode !== "immersed";
    if (g) g.visible = on;
    if (!on) {
      if (was.current) {
        was.current = false;
        last.current = { mx: NaN, my: NaN };
        if (st.hoveredFeature && st.hoveredFeature.kind !== "spot" && st.hoveredFeature.kind !== "event") st.hoverFeature(null);
      }
      return;
    }
    was.current = true;
    const [x, , z] = mapToWorld(f, [touchLens.mx, touchLens.my]);
    if (g) {
      g.position.set(x, 0.03, z);
      // a constant size on screen whatever the zoom, breathing a little while it glides
      const s = camera.position.distanceTo(g.position) * 0.022 * (touchLens.gliding ? 1.15 + Math.sin(clock.elapsedTime * 8) * 0.05 : 1);
      g.scale.setScalar(s);
    }
    // the feature under the lens, looked up only when the lens has moved
    if (touchLens.mx === last.current.mx && touchLens.my === last.current.my) return;
    last.current = { mx: touchLens.mx, my: touchLens.my };
    let feature: HoveredFeature | null = null;
    if (featurePick.root) {
      from.set(x, 50, z);
      ray.set(from, down);
      const hits = ray.intersectObject(featurePick.root, true);
      // the pick meshes are stacked a hair apart, small features on top: the first hit wins, as under a mouse
      for (const h of hits) {
        const ft = h.object.userData?.feature as HoveredFeature | undefined;
        if (ft && h.object.parent?.visible !== false) {
          feature = ft;
          break;
        }
      }
    }
    const cur = st.hoveredFeature;
    if ((cur?.kind ?? null) !== (feature?.kind ?? null) || (cur?.id ?? null) !== (feature?.id ?? null)) st.hoverFeature(feature);
  });

  return (
    <group ref={ring} visible={false}>
      <mesh rotation-x={-Math.PI / 2} raycast={() => null} renderOrder={5}>
        <ringGeometry args={[0.82, 1, 48]} />
        <meshBasicMaterial color="#5a2412" transparent opacity={0.85} depthTest={false} depthWrite={false} toneMapped={false} />
      </mesh>
      <mesh rotation-x={-Math.PI / 2} raycast={() => null} renderOrder={5}>
        <ringGeometry args={[0.12, 0.2, 24]} />
        <meshBasicMaterial color="#5a2412" transparent opacity={0.85} depthTest={false} depthWrite={false} toneMapped={false} />
      </mesh>
    </group>
  );
}
