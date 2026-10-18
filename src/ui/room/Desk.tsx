import { useMemo, useRef, useState } from "react";
import { useFrame, type ThreeEvent } from "@react-three/fiber";
import { Outlines } from "@react-three/drei";
import * as THREE from "three";
import { BRASS, GILT, OUTLINE, PAPER_T, toon, WOOD, WOOD_DARK, WOOD_LIGHT } from "./toon";
import { tipHandlers, useRoom } from "./roomState";

/**
 * The reading desk: turned legs and a moulded top; on it the visitors'
 * register (open it to see your travels and a curiosity from the atlases), an
 * oil lamp (light it for the evening), an inkwell and quill, and a stack of
 * old books. The globe stands at its far end.
 */
export const DESK_TOP = 1.08;
export const LAMP_AT = new THREE.Vector3(1.0, DESK_TOP, -0.22);
/** Where the globe stands on the desk (desk-local). */
export const GLOBE_AT = new THREE.Vector3(-0.78, DESK_TOP, -0.12);

const lathe = (pts: [number, number][], seg = 16) => new THREE.LatheGeometry(pts.map(([r, h]) => new THREE.Vector2(r, h)), seg);

export function Desk({ at }: { at: [number, number, number] }) {
  const leg = useMemo(() => lathe([[0.06, 0], [0.08, 0.05], [0.05, 0.12], [0.07, 0.3], [0.04, 0.55], [0.06, 0.8], [0.075, 0.86], [0.06, 0.96]], 12), []);
  return (
    <group position={at}>
      <mesh position={[0, DESK_TOP - 0.06, 0]} material={toon(WOOD)} castShadow receiveShadow>
        <boxGeometry args={[2.5, 0.08, 1.35]} />
        <Outlines thickness={0.01} color={OUTLINE} />
      </mesh>
      <mesh position={[0, DESK_TOP - 0.115, 0]} material={toon(WOOD_DARK)}>
        <boxGeometry args={[2.38, 0.05, 1.24]} />
      </mesh>
      {/* apron with a drawer front */}
      <mesh position={[0, DESK_TOP - 0.22, 0.6]} material={toon(WOOD_LIGHT)} castShadow>
        <boxGeometry args={[2.2, 0.16, 0.04]} />
        <Outlines thickness={0.008} color={OUTLINE} />
      </mesh>
      <mesh position={[0, DESK_TOP - 0.22, 0.625]} material={toon(BRASS)}>
        <sphereGeometry args={[0.025, 10, 8]} />
      </mesh>
      {[-1, 1].flatMap((sx) =>
        [-1, 1].map((sz) => (
          <mesh key={`${sx}${sz}`} geometry={leg} position={[sx * 1.1, 0, sz * 0.55]} material={toon(WOOD_DARK)} castShadow>
            <Outlines thickness={0.008} color={OUTLINE} />
          </mesh>
        )),
      )}
      <Register at={[0.08, DESK_TOP, 0.24]} />
      <Lamp at={[LAMP_AT.x, LAMP_AT.y, LAMP_AT.z]} />
      <BookStack at={[0.45, DESK_TOP, -0.36]} />
      {/* inkwell and quill */}
      <group position={[0.82, DESK_TOP, 0.38]} {...tipHandlers({ title: "Inkwell and quill", text: "Oak-gall ink: map makers drew every coast and street by hand before it was engraved." }, "default")}>
        <mesh position={[0, 0.06, 0]} material={toon("#2c3a4a")} castShadow>
          <cylinderGeometry args={[0.07, 0.085, 0.12, 14]} />
          <Outlines thickness={0.006} color={OUTLINE} />
        </mesh>
        <mesh position={[0.04, 0.24, -0.02]} rotation={[0.2, 0, -0.35]} material={toon("#f6f0e2")}>
          <coneGeometry args={[0.03, 0.42, 6]} />
          <Outlines thickness={0.005} color={OUTLINE} />
        </mesh>
      </group>
    </group>
  );
}

/** The visitors' register, lying open; its pages riffle when you point at it. */
function Register({ at }: { at: [number, number, number] }) {
  const leaf = useRef<THREE.Group>(null);
  const [hot, setHot] = useState(false);
  useFrame((s, dt) => {
    if (!leaf.current) return;
    const want = hot ? 0.9 + Math.sin(s.clock.elapsedTime * 5) * 0.35 : 0.08;
    leaf.current.rotation.z += (want - leaf.current.rotation.z) * (1 - Math.exp(-8 * Math.min(dt, 0.05)));
  });
  const page = toon(PAPER_T);
  const h = tipHandlers({ title: "The visitors' register", text: "Where travellers sign their names: your journeys through the map room, and a curiosity.", hint: "Click to open it" });
  return (
    <group
      position={at}
      rotation={[0, 0.3, 0]}
      onPointerOver={(e) => (h.onPointerOver(e), setHot(true))}
      onPointerOut={() => (h.onPointerOut(), setHot(false))}
      onClick={(e: ThreeEvent<MouseEvent>) => {
        e.stopPropagation();
        useRoom.getState().setRegister(true);
      }}
    >
      {/* the boards, bound in red leather */}
      <mesh position={[0, 0.012, 0]} material={toon("#7a2f22")} castShadow>
        <boxGeometry args={[0.86, 0.024, 0.58]} />
        <Outlines thickness={0.006} color={OUTLINE} />
      </mesh>
      {[-1, 1].map((s) => (
        <mesh key={s} position={[s * 0.205, 0.045, 0]} rotation={[0, 0, s * -0.06]} material={page}>
          <boxGeometry args={[0.4, 0.04, 0.54]} />
          <Outlines thickness={0.005} color={OUTLINE} />
        </mesh>
      ))}
      {/* a few written lines on each page */}
      {[-1, 1].flatMap((s) =>
        [0, 1, 2, 3, 4].map((k) => (
          <mesh key={`${s}${k}`} position={[s * 0.205, 0.067 + s * -0.004, -0.18 + k * 0.08]} rotation={[-Math.PI / 2, 0, 0]}>
            <planeGeometry args={[0.28 - (k % 2) * 0.06, 0.008]} />
            <meshBasicMaterial color="#6a4a32" />
          </mesh>
        )),
      )}
      {/* a leaf that lifts and riffles */}
      <group ref={leaf} position={[0.01, 0.068, 0]}>
        <mesh position={[0.19, 0, 0]} material={page}>
          <boxGeometry args={[0.38, 0.004, 0.52]} />
        </mesh>
      </group>
      {/* a red ribbon bookmark */}
      <mesh position={[0.02, 0.07, 0.3]} rotation={[-Math.PI / 2, 0, 0.1]}>
        <planeGeometry args={[0.025, 0.14]} />
        <meshBasicMaterial color="#a83a2a" side={THREE.DoubleSide} />
      </mesh>
    </group>
  );
}

/** An oil lamp: click to light it, and the room turns to evening. */
function Lamp({ at }: { at: [number, number, number] }) {
  const evening = useRoom((s) => s.evening);
  const flame = useRef<THREE.Mesh>(null);
  const geo = useMemo(
    () => ({
      base: lathe([[0, 0], [0.12, 0], [0.13, 0.02], [0.08, 0.05], [0.04, 0.09], [0.035, 0.2], [0.05, 0.22], [0, 0.22]]),
      font: lathe([[0, 0], [0.05, 0], [0.1, 0.04], [0.11, 0.08], [0.09, 0.12], [0.04, 0.14], [0, 0.14]]),
      chimney: lathe([[0.045, 0], [0.05, 0.02], [0.075, 0.08], [0.06, 0.16], [0.035, 0.22], [0.035, 0.34]], 20),
    }),
    [],
  );
  useFrame((s) => {
    if (!flame.current) return;
    const t = s.clock.elapsedTime;
    const k = evening ? 1 : 0.0001;
    flame.current.scale.set(k * (1 + Math.sin(t * 13) * 0.08), k * (1 + Math.sin(t * 9.3) * 0.15 + Math.sin(t * 21) * 0.05), k);
  });
  return (
    <group
      position={at}
      {...tipHandlers({ title: "An oil lamp", text: evening ? "Lit for the evening." : "Its wick trimmed and ready.", hint: evening ? "Click to put it out" : "Click to light it for the evening" })}
      onClick={(e: ThreeEvent<MouseEvent>) => {
        e.stopPropagation();
        useRoom.getState().toggleEvening();
        useRoom.getState().setTip(null);
      }}
    >
      <mesh geometry={geo.base} material={toon(BRASS)} castShadow>
        <Outlines thickness={0.006} color={OUTLINE} />
      </mesh>
      <mesh geometry={geo.font} position={[0, 0.22, 0]} material={toon(GILT)}>
        <Outlines thickness={0.006} color={OUTLINE} />
      </mesh>
      <mesh ref={flame} position={[0, 0.39, 0]}>
        <coneGeometry args={[0.022, 0.08, 10]} />
        <meshBasicMaterial color="#ffb347" toneMapped={false} />
      </mesh>
      <mesh geometry={geo.chimney} position={[0, 0.33, 0]}>
        <meshBasicMaterial color="#fff4dc" transparent opacity={evening ? 0.35 : 0.22} depthWrite={false} side={THREE.DoubleSide} />
      </mesh>
      {/* the hit area: generous, so the thin lamp is easy to click */}
      <mesh position={[0, 0.3, 0]} visible={false}>
        <cylinderGeometry args={[0.14, 0.14, 0.62, 8]} />
      </mesh>
    </group>
  );
}

function BookStack({ at }: { at: [number, number, number] }) {
  const books = [
    { w: 0.5, d: 0.36, h: 0.07, c: "#4f6b4a", r: 0.05 },
    { w: 0.46, d: 0.33, h: 0.06, c: "#7a2f22", r: -0.08 },
    { w: 0.42, d: 0.3, h: 0.08, c: "#3c4a66", r: 0.12 },
  ];
  let y = 0;
  return (
    <group position={at} {...tipHandlers({ title: "Old atlases", text: "Ptolemy's Geography, Ortelius's Theatrum Orbis Terrarum, Blaeu's Atlas Maior: the books this room is named after." }, "default")}>
      {books.map((b, i) => {
        const yy = y + b.h / 2;
        y += b.h;
        return (
          <group key={i} position={[0, yy, 0]} rotation={[0, b.r, 0]}>
            <mesh material={toon(b.c)} castShadow>
              <boxGeometry args={[b.w, b.h, b.d]} />
              <Outlines thickness={0.005} color={OUTLINE} />
            </mesh>
            <mesh position={[0.012, 0, 0]} material={toon("#efe0bd")}>
              <boxGeometry args={[b.w - 0.02, b.h - 0.02, b.d + 0.004]} />
            </mesh>
            <mesh position={[-b.w / 2 - 0.001, 0, 0]} rotation={[0, -Math.PI / 2, 0]}>
              <planeGeometry args={[b.d * 0.6, 0.012]} />
              <meshBasicMaterial color={GILT} />
            </mesh>
          </group>
        );
      })}
    </group>
  );
}
