import * as THREE from "three";

/**
 * Shared between the DOM overlay (outside the canvas) and the projector (inside
 * it). The DOM side registers elements with a world position and a priority;
 * the projector places them every frame, hiding any that would overlap a
 * higher-priority item. Positions are rounded to whole pixels so text never
 * shimmers, and z-order is fixed by priority so labels never swap places.
 */
export type OverlayEntry = {
  el: HTMLElement;
  pos: THREE.Vector3;
  priority: number;
  force: boolean;
  candidate: boolean;
  offsetY: number;
  w: number;
  h: number;
  shown: boolean;
};

export const overlay = {
  entries: new Map<string, OverlayEntry>(),
};
