import type * as THREE from "three";

/**
 * Touch screens have no hover, so a finger sets a "lens" on the map instead: tap an empty spot and the
 * houses, streets, fields and boats around it rise as they would under a mouse; press, hold and slide to
 * glide the lens without panning. The lens lives in map units, so it stays put on the ground while the
 * map is panned, zoomed or turned. Tapping it again, or tapping a monument, lifts it.
 */
export const touchLens = { active: false, mx: 0, my: 0, gliding: false };

export function setLens(mx: number, my: number) {
  touchLens.active = true;
  touchLens.mx = mx;
  touchLens.my = my;
}

export function clearLens() {
  touchLens.active = false;
  touchLens.gliding = false;
}

/** The invisible pick meshes of roads, rivers, walls, districts…, for finding the feature under the lens. */
export const featurePick: { root: THREE.Object3D | null } = { root: null };
