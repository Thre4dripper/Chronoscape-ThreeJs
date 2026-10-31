import { Component, Suspense, useLayoutEffect, useMemo, type ReactNode } from "react";
import * as THREE from "three";
import { bakeify } from "../render/baked";
import type { KitParams } from "@/content/schema";
import { Kit } from "./kits";
import { Stage } from "./kits/shared";
import { useModel } from "../render/models";
import { inkLines, INK_MAT } from "../render/ink";

/**
 * Loads a glTF miniature and splits its top-level nodes into reveal stages by
 * name prefix: "p0_podium", "p1_columns", "p2_roof" ... Nodes without a prefix
 * join stage 0. Model units are metres, origin at ground centre, +y up.
 */
const prepared = new Map<string, THREE.Group[]>();

/** Forget the split stages of the models under `prefix` (see forgetModels). */
export function forgetStages(prefix: string) {
  for (const url of [...prepared.keys()]) if (url.startsWith(prefix)) prepared.delete(url);
}

function GlbStages({ url, onReady }: { url: string; onReady?: () => void }) {
  const gltf = useModel(url);
  const stages = useMemo(() => {
    const hit = prepared.get(url);
    if (hit) return hit;
    const root = gltf.scene.clone(true);
    const buckets = new Map<number, THREE.Group>();
    for (const child of [...root.children]) {
      const m = /^p(\d+)_/.exec(child.name);
      const idx = m ? parseInt(m[1], 10) : 0;
      let g = buckets.get(idx);
      if (!g) {
        g = new THREE.Group();
        buckets.set(idx, g);
      }
      g.add(child);
    }
    const meshes: THREE.Mesh[] = [];
    let baked = false;
    for (const g of buckets.values()) {
      g.traverse((o) => {
        const m = o as THREE.Mesh;
        if (!m.isMesh) return;
        meshes.push(m);
        if ((m.material as THREE.MeshStandardMaterial).map) baked = true;
      });
      bakeify(g);
    }
    // models without a baked texture get crisp inked creases, like a drawn miniature;
    // computed off the main thread and added when ready (fading in with the rise)
    if (!baked)
      for (const m of meshes) {
        const mesh = m;
        inkLines(mesh.geometry, 30).then((arr) => {
          if (!arr.length) return;
          const g = new THREE.BufferGeometry();
          g.setAttribute("position", new THREE.BufferAttribute(arr, 3));
          const lines = new THREE.LineSegments(g, INK_MAT);
          lines.raycast = () => {};
          lines.frustumCulled = false;
          mesh.add(lines);
        });
      }
    const count = Math.max(...buckets.keys()) + 1;
    const out = Array.from({ length: count }, (_, i) => buckets.get(i) ?? new THREE.Group());
    prepared.set(url, out);
    return out;
  }, [gltf, url]);
  useLayoutEffect(() => onReady?.(), [onReady, stages]);

  return (
    <>
      {stages.map((g, i) => (
        <Stage key={i} index={i} count={stages.length}>
          <primitive object={g} />
        </Stage>
      ))}
    </>
  );
}

class Boundary extends Component<{ fallback: ReactNode; children: ReactNode; onError?: (e: unknown) => void }, { failed: boolean }> {
  state = { failed: false };
  static getDerivedStateFromError() {
    return { failed: true };
  }
  componentDidCatch(e: unknown) {
    this.props.onError?.(e);
  }
  render() {
    return this.state.failed ? this.props.fallback : this.props.children;
  }
}

/** `onReady` fires once there is something to show (the model, or its stand-in if it failed), so the rise can wait for it. */
export function GlbModel({ url, fallback, onReady }: { url: string; fallback?: KitParams; onReady?: () => void }) {
  const stand = fallback ? <Kit params={fallback} /> : <Placeholder />;
  return (
    <Boundary
      fallback={stand}
      onError={(e) => {
        console.warn(`[asset] failed to load ${url}`, e);
        onReady?.();
      }}
    >
      <Suspense fallback={null}>
        <GlbStages url={url} onReady={onReady} />
      </Suspense>
    </Boundary>
  );
}

function Placeholder() {
  return (
    <Stage index={0} count={1}>
      <mesh position-y={4}>
        <boxGeometry args={[20, 8, 20]} />
        <meshBasicMaterial color="#c9b48b" />
      </mesh>
    </Stage>
  );
}
