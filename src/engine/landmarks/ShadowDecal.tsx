import { useContext, useEffect, useMemo, useRef, useState } from "react";
import { useFrame } from "@react-three/fiber";
import * as THREE from "three";
import { RevealContext } from "./kits/shared";

/** Baked top-down shadow (rendered in Blender) laid on the paper under a risen model. */
type Meta = { size: number; cx: number; cy: number };
let manifest: Promise<Record<string, Meta>> | null = null;
const textures = new Map<string, Promise<THREE.Texture | null>>();

function loadShadow(key: string) {
  let p = textures.get(key);
  if (!p) {
    p = new Promise((resolve) => {
      new THREE.TextureLoader().load(`/models/shadows/${key}.webp`, (t) => {
        t.colorSpace = THREE.SRGBColorSpace;
        resolve(t);
      }, undefined, () => resolve(null));
    });
    textures.set(key, p);
  }
  return p;
}

export function ShadowDecal({ glb }: { glb: string }) {
  const key = glb.replace(/^\/?models\//, "").replace(/\.glb$/, "");
  const [state, setState] = useState<{ meta: Meta; tex: THREE.Texture } | null>(null);
  const { progress } = useContext(RevealContext);
  const mat = useMemo(() => new THREE.MeshBasicMaterial({ transparent: true, depthWrite: false, opacity: 0, toneMapped: false, polygonOffset: true, polygonOffsetFactor: -1, polygonOffsetUnits: -1 }), []);
  const mesh = useRef<THREE.Mesh>(null);
  useEffect(() => {
    let alive = true;
    if (!manifest) manifest = fetch("/models/shadows/manifest.json").then((r) => (r.ok ? r.json() : {})).catch(() => ({}));
    manifest.then(async (m) => {
      const meta = m[key];
      if (!meta) return;
      const tex = await loadShadow(key);
      if (alive && tex) {
        mat.map = tex;
        mat.needsUpdate = true;
        setState({ meta, tex });
      }
    });
    return () => {
      alive = false;
    };
  }, [key, mat]);
  useEffect(() => () => mat.dispose(), [mat]);
  useFrame(() => {
    // only a fully risen model casts a shadow: it fades out the moment the model starts to sink
    const p = Math.max(0, Math.min(1, (progress.current - 0.7) / 0.3));
    mat.opacity = p * p * (3 - 2 * p) * 0.85;
    if (mesh.current) mesh.current.visible = p > 0.001;
  });
  if (!state) return null;
  return (
    <mesh ref={mesh} material={mat} position={[state.meta.cx, 0.02, state.meta.cy]} rotation-x={-Math.PI / 2} renderOrder={3} raycast={() => null}>
      <planeGeometry args={[state.meta.size, state.meta.size]} />
    </mesh>
  );
}
