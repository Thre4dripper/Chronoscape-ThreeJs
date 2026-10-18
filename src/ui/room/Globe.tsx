import { useEffect, useMemo, useRef, useState } from "react";
import { useFrame, useThree, type ThreeEvent } from "@react-three/fiber";
import { Outlines } from "@react-three/drei";
import * as THREE from "three";
import type { Atlas, AtlasMap } from "@/content/schema";
import { atlasCatalog } from "@/content/registry";
import { useNav } from "@/nav";
import { drawMap } from "@/world/world";
import { BRASS, GILT, globeCanvas, OUTLINE, toon, toonGradient, WOOD } from "./toon";
import { useRoom } from "./roomState";

/**
 * A desk globe: turned walnut pedestal, a brass meridian ring holding the
 * Earth on its axis tilted 23.4 degrees. It idles round; drag it to spin it.
 * When an atlas is hovered or open it turns to that part of the world and
 * washes the region in the atlas's colour. Point at a town on it to read its
 * name; click to open its atlas (or unfold the map, if it is ready).
 */
const R = 0.6;
const TILT = 0.41;
const RING_YAW = -0.55; // the meridian is seen a little from the side

export function Globe({ atlas, at }: { atlas: Atlas | null; at: [number, number, number] }) {
  const [base, setBase] = useState<HTMLCanvasElement | null>(null);
  const skin = useMemo(() => {
    const c = document.createElement("canvas");
    c.width = 2048;
    c.height = 1024;
    const t = new THREE.CanvasTexture(c);
    t.colorSpace = THREE.SRGBColorSpace;
    t.anisotropy = 8;
    return t;
  }, []);
  useEffect(() => {
    let alive = true;
    void globeCanvas().then((c) => alive && setBase(c));
    return () => {
      alive = false;
      skin.dispose();
    };
  }, [skin]);
  // repaint the skin with the region of the atlas in hand, and every town on the shelf
  useEffect(() => {
    if (!base) return;
    const c = skin.image as HTMLCanvasElement;
    const ctx = c.getContext("2d")!;
    ctx.drawImage(base, 0, 0);
    const v = { lon0: -180, lon1: 180, lat0: -90, lat1: 90, x: 0, y: 0, w: 2048, h: 1024 };
    drawMap(ctx, v, {
      land: [],
      sea: "rgba(0,0,0,0)",
      highlight: atlas ? { area: atlas.area, color: atlas.color } : null,
      pins: atlasCatalog.atlases.flatMap((a) => a.maps.map((m) => ({ at: m.at, color: a.color, open: !!m.city && (!atlas || atlas === a) }))),
      weight: atlas ? 2 : 1.6,
    });
    skin.needsUpdate = true;
  }, [base, atlas, skin]);

  const spin = useRef<THREE.Group>(null);
  const drag = useRef<{ x: number; t: number } | null>(null);
  const vel = useRef(0.18);
  const touched = useRef(-99);
  const { gl, camera, clock } = useThree();
  const target = useMemo(() => {
    if (!atlas) return null;
    let lon = 0;
    for (const [a] of atlas.area) lon += a;
    return lon / atlas.area.length;
  }, [atlas]);
  const groupRef = useRef<THREE.Group>(null);
  useFrame((_, dtRaw) => {
    const dt = Math.min(dtRaw, 0.05);
    const s = spin.current;
    if (!s || drag.current) return;
    const recent = clock.elapsedTime - touched.current < 4;
    if (target !== null && !recent) {
      // turn the region's middle toward the camera (see the sphere's uv layout: u = (lon + 180) / 360)
      const gp = groupRef.current!.getWorldPosition(new THREE.Vector3());
      const toCam = Math.atan2(camera.position.x - gp.x, camera.position.z - gp.z);
      const phi = ((target + 180) / 360) * Math.PI * 2;
      const want = toCam + Math.PI / 2 - phi - RING_YAW;
      let d = want - s.rotation.y;
      d = ((((d + Math.PI) % (Math.PI * 2)) + Math.PI * 2) % (Math.PI * 2)) - Math.PI;
      s.rotation.y += d * (1 - Math.exp(-4 * dt));
      vel.current = 0;
    } else {
      // free spin with friction, settling back to a slow idle turn
      vel.current += ((recent ? 0 : 0.18) - vel.current) * (1 - Math.exp(-1.2 * dt));
      s.rotation.y += vel.current * dt;
    }
  });
  useEffect(() => {
    const el = gl.domElement;
    const move = (e: PointerEvent) => {
      if (!drag.current || !spin.current) return;
      const now = performance.now();
      const dx = e.clientX - drag.current.x;
      spin.current.rotation.y += dx * 0.012;
      vel.current = ((dx * 0.012) / Math.max(1, now - drag.current.t)) * 1000 * 0.6;
      drag.current = { x: e.clientX, t: now };
    };
    const up = () => {
      if (!drag.current) return;
      drag.current = null;
      touched.current = clock.elapsedTime;
      el.style.cursor = "";
    };
    addEventListener("pointermove", move);
    addEventListener("pointerup", up);
    return () => {
      removeEventListener("pointermove", move);
      removeEventListener("pointerup", up);
    };
  }, [gl, clock]);

  /** The town nearest the pointer on the globe's skin, if any. */
  const townAt = (e: ThreeEvent<PointerEvent | MouseEvent>): { a: Atlas; m: AtlasMap } | null => {
    if (!e.uv) return null;
    const lon = e.uv.x * 360 - 180, lat = (e.uv.y - 0.5) * 180;
    let best: { d: number; a: Atlas; m: AtlasMap } | null = null;
    for (const a of atlasCatalog.atlases)
      for (const m of a.maps) {
        const d = Math.hypot((m.at[0] - lon) * Math.cos((lat * Math.PI) / 180), m.at[1] - lat);
        if (d < 4.5 && (!best || d < best.d || (atlas === a && d < best.d + 1))) best = { d, a, m };
      }
    return best;
  };
  const skinMat = useMemo(() => new THREE.MeshToonMaterial({ map: skin, gradientMap: toonGradient() }), [skin]);
  useEffect(() => () => skinMat.dispose(), [skinMat]);
  const pedestal = useMemo(
    () =>
      new THREE.LatheGeometry(
        ([[0, 0], [0.36, 0], [0.37, 0.03], [0.33, 0.06], [0.2, 0.09], [0.12, 0.13], [0.1, 0.2], [0.13, 0.24], [0.06, 0.3], [0.05, 0.42], [0.08, 0.46], [0, 0.48]] as [number, number][]).map(([r, h]) => new THREE.Vector2(r, h)),
        28,
      ),
    [],
  );
  useEffect(() => () => pedestal.dispose(), [pedestal]);
  const centerY = 0.48 + R + 0.06;
  return (
    <group position={at} ref={groupRef}>
      <mesh geometry={pedestal} material={toon(WOOD)} castShadow receiveShadow>
        <Outlines thickness={0.01} color={OUTLINE} />
      </mesh>
      <mesh position={[0, 0.03, 0]} rotation={[Math.PI / 2, 0, 0]} material={toon(GILT)}>
        <torusGeometry args={[0.35, 0.012, 6, 40]} />
      </mesh>
      {/* the stem meets the bottom of the meridian ring, straight below the centre */}
      <mesh position={[0, 0.48 + 0.04, 0]} material={toon(BRASS)}>
        <cylinderGeometry args={[0.035, 0.05, 0.08, 14]} />
        <Outlines thickness={0.006} color={OUTLINE} />
      </mesh>
      <group position={[0, centerY, 0]} rotation={[0, RING_YAW, 0]}>
        {/* the meridian: a full brass ring in the plane of the axis */}
        <mesh material={toon(BRASS)}>
          <torusGeometry args={[R + 0.06, 0.022, 10, 72]} />
          <Outlines thickness={0.006} color={OUTLINE} />
        </mesh>
        <group rotation={[0, 0, TILT]}>
          {[1, -1].map((s) => (
            <mesh key={s} position={[0, s * (R + 0.03), 0]} material={toon(BRASS)}>
              <cylinderGeometry args={[0.018, 0.018, 0.08, 10]} />
            </mesh>
          ))}
          <group ref={spin}>
            <mesh
              material={skinMat}
              castShadow
              onPointerDown={(e) => {
                e.stopPropagation();
                drag.current = { x: e.nativeEvent.clientX, t: performance.now() };
                touched.current = clock.elapsedTime;
                gl.domElement.style.cursor = "grabbing";
              }}
              onPointerMove={(e) => {
                e.stopPropagation();
                if (drag.current) return;
                const hit = townAt(e);
                useRoom.getState().setTip(
                  hit
                    ? { title: hit.m.title, text: `${hit.m.subtitle} · ${hit.a.title}`, hint: hit.m.city ? "Click to unfold the map" : "Click to open its atlas" }
                    : { title: "A terrestrial globe", text: "Every town on the shelf is marked on it.", hint: "Drag to spin it" },
                );
                document.body.style.cursor = hit ? "pointer" : "grab";
              }}
              onPointerOut={() => {
                useRoom.getState().setTip(null);
                document.body.style.cursor = "";
              }}
              onClick={(e) => {
                e.stopPropagation();
                if (Math.abs(vel.current) > 0.8) return; // that was a spin, not a click
                const hit = townAt(e);
                if (!hit) return;
                if (hit.m.city) useNav.getState().openMap(hit.a.id, hit.m, { x: e.nativeEvent.clientX - 40, y: e.nativeEvent.clientY - 50, w: 80, h: 100 });
                else useNav.getState().openAtlas(hit.a.id);
              }}
            >
              <sphereGeometry args={[R, 64, 40]} />
              <Outlines thickness={0.012} color={OUTLINE} />
            </mesh>
          </group>
        </group>
        {/* a little brass hour circle at the north pole of the meridian */}
        <group rotation={[0, 0, TILT]}>
          <mesh position={[0, R + 0.075, 0]} rotation={[Math.PI / 2, 0, 0]} material={toon(GILT)}>
            <torusGeometry args={[0.05, 0.008, 6, 20]} />
          </mesh>
        </group>
      </group>
    </group>
  );
}
