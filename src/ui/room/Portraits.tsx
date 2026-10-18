import { useEffect, useMemo, useRef, useState } from "react";
import { useFrame, type ThreeEvent } from "@react-three/fiber";
import { Outlines } from "@react-three/drei";
import * as THREE from "three";
import { atlasCatalog } from "@/content/registry";
import { useNav } from "@/nav";
import { BRASS, GILT, labelTexture, OUTLINE, toon, toonGradient, WOOD_DARK } from "./toon";
import { useRoom } from "./roomState";

/**
 * Historic views of the shelf's cities, framed and hung on the wall in a
 * salon hang: woodcuts, a bird's-eye view, an aquatint, a ukiyo-e print
 * (public domain, from Wikimedia Commons; credits in the manifest). Each hangs
 * from a nail on a cord: point at one and it swings a little and tells you
 * what it shows; click it to open its city's atlas, or unfold the map.
 */
type Portrait = { id: string; src: string; w: number; h: number; caption: string; atlas: string; map: string; artist: string; license: string; page: string };

let manifest: Promise<Portrait[]> | null = null;
const loadManifest = () =>
  (manifest ??= fetch("/room/portraits/manifest.json")
    .then((r) => (r.ok ? (r.json() as Promise<Portrait[]>) : []))
    .catch(() => []));

export function Portraits({ x0, x1, y0, y1, z, cols = 2, only }: { x0: number; x1: number; y0: number; y1: number; z: number; cols?: number; only?: string[] }) {
  const [list, setList] = useState<Portrait[]>([]);
  useEffect(() => {
    let alive = true;
    // (the list of ids is fixed for the life of the room)
    void loadManifest().then((m) => alive && setList(only ? only.map((id) => m.find((p) => p.id === id)).filter((p): p is Portrait => !!p) : m));
    return () => {
      alive = false;
    };
  }, []);
  if (!list.length) return null;
  const rows = Math.ceil(list.length / cols);
  const gap = 0.2;
  const slotW = (x1 - x0 - gap * (cols - 1)) / cols, slotH = (y1 - y0 - gap * (rows - 1)) / rows;
  return (
    <group>
      {list.map((p, i) => {
        const c = i % cols, r = Math.floor(i / cols);
        const cx = x0 + slotW / 2 + c * (slotW + gap);
        const cy = y1 - slotH / 2 - r * (slotH + gap);
        // fit the picture (plus its frame) inside the slot, keeping its proportions; vary sizes a little
        const aspect = p.w / p.h;
        const k = 1 - ((i * 37) % 3) * 0.06;
        let pw = slotW * 0.84 * k, ph = pw / aspect;
        if (ph > slotH * 0.66 * k) ((ph = slotH * 0.66 * k), (pw = ph * aspect));
        return <Frame key={p.id} p={p} at={[cx, cy, z]} pw={pw} ph={ph} gilt={i % 2 === 0} />;
      })}
    </group>
  );
}

function ringShape(ow: number, oh: number, iw: number, ih: number) {
  const s = new THREE.Shape();
  s.moveTo(-ow / 2, -oh / 2);
  s.lineTo(ow / 2, -oh / 2);
  s.lineTo(ow / 2, oh / 2);
  s.lineTo(-ow / 2, oh / 2);
  s.closePath();
  const hole = new THREE.Path();
  hole.moveTo(-iw / 2, -ih / 2);
  hole.lineTo(-iw / 2, ih / 2);
  hole.lineTo(iw / 2, ih / 2);
  hole.lineTo(iw / 2, -ih / 2);
  hole.closePath();
  s.holes.push(hole);
  return s;
}

function Frame({ p, at, pw, ph, gilt }: { p: Portrait; at: [number, number, number]; pw: number; ph: number; gilt: boolean }) {
  const [tex, setTex] = useState<THREE.Texture | null>(null);
  useEffect(() => {
    let alive = true;
    new THREE.TextureLoader().load(`/${p.src}`, (t) => {
      t.colorSpace = THREE.SRGBColorSpace;
      t.anisotropy = 8;
      if (alive) setTex(t);
      else t.dispose();
    });
    return () => {
      alive = false;
    };
  }, [p.src]);
  useEffect(() => () => tex?.dispose(), [tex]);
  const f = 0.09; // moulding width
  const geo = useMemo(() => {
    const outer = new THREE.ExtrudeGeometry(ringShape(pw + f * 2, ph + f * 2, pw + 0.01, ph + 0.01), { depth: 0.035, bevelEnabled: true, bevelThickness: 0.02, bevelSize: 0.022, bevelSegments: 2 });
    const slip = new THREE.ExtrudeGeometry(ringShape(pw + 0.03, ph + 0.03, pw, ph), { depth: 0.02, bevelEnabled: false });
    return { outer, slip };
  }, [pw, ph]);
  useEffect(() => () => (geo.outer.dispose(), geo.slip.dispose()), [geo]);
  const short = p.caption.split(",")[0].toUpperCase();
  const plate = useMemo(() => labelTexture(short, 384, 72, { bg: BRASS, fg: "#3d2a1c", size: 32, spacing: 5 }), [short]);
  useEffect(() => () => plate.dispose(), [plate]);

  // a damped swing on its nail when touched
  const g = useRef<THREE.Group>(null);
  const swing = useRef({ a: 0, v: 0 });
  const [hot, setHot] = useState(false);
  useFrame((_, dtRaw) => {
    const dt = Math.min(dtRaw, 0.05);
    const s = swing.current;
    s.v += (-s.a * 28 - s.v * 2.6) * dt;
    s.a += s.v * dt;
    if (g.current) {
      g.current.rotation.z = s.a;
      const want = hot ? 1.035 : 1;
      g.current.scale.setScalar(g.current.scale.x + (want - g.current.scale.x) * (1 - Math.exp(-10 * dt)));
    }
  });
  const atlas = atlasCatalog.atlases.find((a) => a.id === p.atlas);
  const map = atlas?.maps.find((m) => m.title === p.map);
  const nailY = ph / 2 + f + 0.22;
  const cord = useMemo(() => {
    const half = pw / 2 + f - 0.08;
    const pts = [new THREE.Vector3(-half, ph / 2 + f - 0.02, 0.0), new THREE.Vector3(0, nailY, 0.01), new THREE.Vector3(half, ph / 2 + f - 0.02, 0.0)];
    return new THREE.BufferGeometry().setFromPoints(pts);
  }, [pw, ph, nailY]);
  const cordLine = useMemo(() => new THREE.Line(cord, new THREE.LineBasicMaterial({ color: "#5a3a24" })), [cord]);
  useEffect(() => () => (cord.dispose(), (cordLine.material as THREE.Material).dispose()), [cord, cordLine]);
  return (
    <group position={[at[0], at[1] + nailY, at[2]]}>
      <mesh material={toon(BRASS)} position={[0, 0, 0.02]}>
        <sphereGeometry args={[0.025, 10, 8]} />
      </mesh>
      {/* everything below hangs from the nail and swings about it */}
      <group ref={g}>
        <group position={[0, -nailY, 0]}>
          <primitive object={cordLine} />
          <group
            onPointerOver={(e: ThreeEvent<PointerEvent>) => {
              e.stopPropagation();
              setHot(true);
              swing.current.v += 0.9;
              useRoom.getState().setTip({ title: p.caption, text: map ? `${map.subtitle} · ${atlas?.title}` : undefined, hint: map?.city ? "Click to unfold the map" : "Click to open its atlas" });
              document.body.style.cursor = "pointer";
            }}
            onPointerOut={() => {
              setHot(false);
              useRoom.getState().setTip(null);
              document.body.style.cursor = "";
            }}
            onClick={(e: ThreeEvent<MouseEvent>) => {
              e.stopPropagation();
              if (!atlas) return;
              if (map?.city) useNav.getState().openMap(atlas.id, map, { x: e.nativeEvent.clientX - 40, y: e.nativeEvent.clientY - 50, w: 80, h: 100 });
              else useNav.getState().openAtlas(atlas.id);
            }}
          >
            <mesh geometry={geo.outer} material={toon(gilt ? GILT : WOOD_DARK)} position={[0, 0, -0.035]} castShadow>
              <Outlines thickness={0.008} color={OUTLINE} />
            </mesh>
            <mesh geometry={geo.slip} material={toon(gilt ? "#3e2314" : "#b8863a")} position={[0, 0, -0.02]} />
            <mesh position={[0, 0, -0.005]}>
              <planeGeometry args={[pw, ph]} />
              <meshToonMaterial key={tex ? "pic" : "blank"} map={tex} color={tex ? "#f4ead8" : "#e3cfa2"} gradientMap={toonGradient()} />
            </mesh>
          </group>
          <mesh position={[0, -ph / 2 - f - 0.09, 0.0]}>
            <planeGeometry args={[Math.min(0.62, pw * 0.7), 0.1]} />
            <meshToonMaterial map={plate} gradientMap={toonGradient()} />
          </mesh>
        </group>
      </group>
    </group>
  );
}
