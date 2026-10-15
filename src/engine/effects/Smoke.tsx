import { useMemo, useRef } from "react";
import { useFrame } from "@react-three/fiber";
import * as THREE from "three";

/** Rising smoke for fire events: a few dozen soft sprites, one draw call. */
export function Smoke({ position, size, color = "#5a4a3c" }: { position: [number, number, number]; size: number; color?: string }) {
  const n = 70;
  const ref = useRef<THREE.Points>(null);
  const seeds = useMemo(() => Array.from({ length: n }, () => ({ a: Math.random() * Math.PI * 2, r: Math.random(), t: Math.random(), s: 0.6 + Math.random() * 0.8 })), []);
  const geom = useMemo(() => {
    const g = new THREE.BufferGeometry();
    g.setAttribute("position", new THREE.Float32BufferAttribute(new Float32Array(n * 3), 3));
    return g;
  }, []);
  const sprite = useMemo(() => {
    const c = document.createElement("canvas");
    c.width = c.height = 64;
    const ctx = c.getContext("2d")!;
    const g = ctx.createRadialGradient(32, 32, 0, 32, 32, 32);
    g.addColorStop(0, "rgba(255,255,255,0.9)");
    g.addColorStop(0.5, "rgba(255,255,255,0.35)");
    g.addColorStop(1, "rgba(255,255,255,0)");
    ctx.fillStyle = g;
    ctx.fillRect(0, 0, 64, 64);
    const t = new THREE.CanvasTexture(c);
    return t;
  }, []);
  useFrame((_, dt) => {
    const p = ref.current;
    if (!p) return;
    const arr = (p.geometry.getAttribute("position") as THREE.BufferAttribute).array as Float32Array;
    seeds.forEach((s, i) => {
      s.t += dt * 0.12 * s.s;
      if (s.t > 1) {
        s.t = 0;
        s.a = Math.random() * Math.PI * 2;
        s.r = Math.random();
      }
      const spread = size * (0.15 + s.t * 0.9) * s.r;
      arr[i * 3] = Math.cos(s.a + s.t * 2) * spread;
      arr[i * 3 + 1] = s.t * size * 1.6;
      arr[i * 3 + 2] = Math.sin(s.a + s.t * 2) * spread;
    });
    (p.geometry.getAttribute("position") as THREE.BufferAttribute).needsUpdate = true;
  });
  return (
    <points ref={ref} position={position} geometry={geom}>
      <pointsMaterial map={sprite} color={color} size={size * 0.5} transparent opacity={0.5} depthWrite={false} sizeAttenuation />
    </points>
  );
}
