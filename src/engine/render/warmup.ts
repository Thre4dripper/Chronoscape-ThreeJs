import type * as THREE from "three";

/** Materials registered by components so the warm-up pass can compile their programs ahead of use. */
const registry = new Set<THREE.Material>();

export function registerForWarmup(...mats: THREE.Material[]) {
  for (const m of mats) registry.add(m);
}

export function warmupMaterials(): THREE.Material[] {
  return [...registry];
}
