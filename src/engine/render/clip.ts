import * as THREE from "three";

/**
 * The sheet's edge. Map data runs past the drawn sheet (a sea, a river leaving the frame), so anything
 * drawn on the map from that data (close-up tiles, hover highlights) is cut at the edge in the shader,
 * and the pointer stops finding features once it leaves the paper. World units, centred on the map.
 */
export const MAP_CLIP = { uMapHalf: { value: new THREE.Vector2(1e6, 1e6) } };
/** For bakedMaterial's extraFrag (it has vWP). */
export const CLIP_FRAG = "if (abs(vWP.x) > uMapHalf.x || abs(vWP.z) > uMapHalf.y) discard;";
export const onMap = (x: number, z: number) => Math.abs(x) <= MAP_CLIP.uMapHalf.value.x && Math.abs(z) <= MAP_CLIP.uMapHalf.value.y;
