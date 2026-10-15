import * as THREE from "three";

/** Off-thread crease lines for a geometry; resolves to segment endpoints in the geometry's space. */
let worker: Worker | null = null;
let seq = 0;
const waiting = new Map<number, (a: Float32Array) => void>();

function getWorker() {
  if (!worker) {
    worker = new Worker(new URL("./ink.worker.ts", import.meta.url), { type: "module" });
    worker.onmessage = (e: MessageEvent<{ id: number; lines: Float32Array }>) => {
      waiting.get(e.data.id)?.(e.data.lines);
      waiting.delete(e.data.id);
    };
  }
  return worker;
}

export function inkLines(geometry: THREE.BufferGeometry, angle = 30): Promise<Float32Array> {
  const pos = geometry.getAttribute("position") as THREE.BufferAttribute;
  // copies: the geometry keeps its own buffers for rendering
  const p = new Float32Array(pos.count * 3);
  for (let i = 0; i < pos.count; i++) {
    p[i * 3] = pos.getX(i);
    p[i * 3 + 1] = pos.getY(i);
    p[i * 3 + 2] = pos.getZ(i);
  }
  const idx = geometry.index ? new Uint32Array(geometry.index.array as ArrayLike<number>) : null;
  const id = ++seq;
  return new Promise((resolve) => {
    waiting.set(id, resolve);
    getWorker().postMessage({ id, pos: p, index: idx, angle }, idx ? [p.buffer, idx.buffer] : [p.buffer]);
  });
}

/** The shared ink: a warm dark brown, soft enough to read as a drawn line, not a wireframe. */
export const INK_MAT = new THREE.LineBasicMaterial({ color: "#3b2a1d", transparent: true, opacity: 0.42, depthWrite: false });
