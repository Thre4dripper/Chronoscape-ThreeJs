import * as THREE from "three";
import { useGLTF } from "@react-three/drei";
import { DRACO_PATH } from "../render/models";

/**
 * The study's Blender models: the writing table's parts and the things on it (built by
 * tools/blender/models/study/*.py, baked by tools/blender/bake_study.py into assets/models/study/<name>.glb).
 * Each model is a few named parts with their pivots: `base` (everything that stays still, merged), `anim_*`
 * (turned by the study's click animations), and parts the study paints itself (glass, paper, coals, tex_*).
 * Colour and baked occlusion are in the vertices; normals are exported, so the fixed light shades them.
 */
export type StudyPart = { geometry: THREE.BufferGeometry; position: THREE.Vector3; quaternion: THREE.Quaternion };
export type StudyModel = Record<string, StudyPart>;

type GLTF = { scene: THREE.Object3D };

export const studyUrl = (name: string) => `/models/study/${name}.glb`;

const parts = new WeakMap<object, StudyModel>();
function partsOf(gltf: GLTF): StudyModel {
  let out = parts.get(gltf);
  if (!out) {
    out = {};
    for (const node of gltf.scene.children) {
      let mesh: THREE.Mesh | undefined;
      node.traverse((o) => {
        if (!mesh && (o as THREE.Mesh).isMesh) mesh = o as THREE.Mesh;
      });
      if (mesh) out[node.name] = { geometry: mesh.geometry, position: node.position.clone(), quaternion: node.quaternion.clone() };
    }
    parts.set(gltf, out);
  }
  return out;
}

/** Load several study models at once (in parallel, one suspension), keyed by name. */
export function useStudyModels<K extends string>(names: readonly K[]): Record<K, StudyModel> {
  const gltfs = useGLTF(names.map(studyUrl), DRACO_PATH) as unknown as GLTF[];
  const out = {} as Record<K, StudyModel>;
  names.forEach((n, i) => (out[n] = partsOf(gltfs[i])));
  return out;
}

/** A copy of a part's geometry with its vertex colours multiplied (per channel, linear). */
export function tintGeometry(g: THREE.BufferGeometry, k: THREE.Color) {
  const c = g.getAttribute("color") as THREE.BufferAttribute | undefined;
  if (!c) return g;
  for (let i = 0; i < c.count; i++) c.setXYZ(i, Math.min(1, c.getX(i) * k.r), Math.min(1, c.getY(i) * k.g), Math.min(1, c.getZ(i) * k.b));
  c.needsUpdate = true;
  return g;
}

/** The per-channel factor that turns colour `from` into colour `to` (both sRGB hex), in linear space. */
export function tintFactor(from: string, to: string) {
  const a = new THREE.Color(from), b = new THREE.Color(to);
  return new THREE.Color(b.r / Math.max(1e-4, a.r), b.g / Math.max(1e-4, a.g), b.b / Math.max(1e-4, a.b));
}
