import { useEffect, useMemo, useRef } from "react";
import * as THREE from "three";
import { shaded, bakedMaterial, miniatureMaterial } from "../render/baked";
import { useModel } from "../render/models";

/**
 * Draws one Blender piece (a wall bay, an aqueduct arch...) many times with
 * instancing: one instanced mesh per primitive in the glTF, all sharing the
 * same list of placement matrices.
 */
export function InstancedGlb({ url, matrices }: { url: string; matrices: THREE.Matrix4[] }) {
  const gltf = useModel(url);
  const parts = useMemo(() => {
    gltf.scene.updateMatrixWorld(true);
    const out: { geometry: THREE.BufferGeometry; material: THREE.Material; local: THREE.Matrix4 }[] = [];
    gltf.scene.traverse((o) => {
      const m = o as THREE.Mesh;
      if (m.isMesh) out.push({ geometry: m.geometry, material: toUnlit(m.material as THREE.Material, m.geometry), local: m.matrixWorld.clone() });
    });
    return out;
  }, [gltf]);
  const refs = useRef<(THREE.InstancedMesh | null)[]>([]);
  useEffect(() => {
    const tmp = new THREE.Matrix4();
    parts.forEach((p, i) => {
      const mesh = refs.current[i];
      if (!mesh) return;
      matrices.forEach((mx, k) => mesh.setMatrixAt(k, tmp.multiplyMatrices(mx, p.local)));
      mesh.count = matrices.length;
      mesh.instanceMatrix.needsUpdate = true;
      mesh.computeBoundingSphere();
    });
  }, [parts, matrices]);
  const cap = Math.max(1, matrices.length);
  return (
    <>
      {parts.map((p, i) => (
        <instancedMesh key={`${i}:${cap}`} ref={(m) => (refs.current[i] = m)} args={[p.geometry, p.material, cap]} raycast={() => null} />
      ))}
    </>
  );
}

function toUnlit(m: THREE.Material, g: THREE.BufferGeometry): THREE.Material {
  const std = m as THREE.MeshStandardMaterial;
  if (std.map) return bakedMaterial({ map: std.map, key: "tex" });
  if (g.getAttribute("color")) return miniatureMaterial(!g.getAttribute("normal"));
  return g.getAttribute("normal") ? shaded(std.color ?? 0xcccccc) : bakedMaterial({ color: std.color ?? 0xcccccc, flat: true, key: "flat" });
}
