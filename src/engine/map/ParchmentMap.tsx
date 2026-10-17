import { useEffect, useMemo, useRef, useState } from "react";
import { useFrame, useThree } from "@react-three/fiber";
import * as THREE from "three";
import { prefetchFabrics } from "./fabricPrefetch";
import type { City } from "@/content/schema";
import { frameOf, mapToWorld } from "../coords";
import type { View } from "./plate";
import { BASE_EDGE, PlateService, installBakeHook } from "./plateService";
import { useStore } from "../store";
import { prefersReducedMotion } from "../motion";
import { bakedMaterial } from "../render/baked";

const TILE_PX = 2048;
const SETTLE_S = 0.3;

/**
 * The atlas plate. Nothing is drawn on the main thread:
 *  - the whole-city plate for each period is a pre-baked image decoded off-thread
 *    (drawn in a worker if no bake exists), crossfaded on period change;
 *  - a sharp close-up tile is drawn in the worker once the camera has settled,
 *    and faded in over the base.
 * Layers sit at y = 0 with polygon offset so nothing standing on the map z-fights with it.
 */
export function ParchmentMap({ city }: { city: City }) {
  const f = frameOf(city);
  const [MW, MH] = city.map.size;
  const storePeriod = useStore((s) => s.periodId);
  // during a hand-over between cities the store can briefly hold the next city's era
  const periodId = storePeriod && city.periods.some((p) => p.id === storePeriod) ? storePeriod : city.defaultPeriodId;
  const { camera, gl } = useThree();
  // one service (and worker) per mounted city; created in an effect so it survives React's dev double-mount
  const [service, setService] = useState<PlateService | null>(null);
  useEffect(() => {
    const sv = new PlateService(city);
    setService(sv);
    if (import.meta.env.DEV) installBakeHook(city);
    return () => sv.dispose();
  }, [city]);

  /* ---------- base layer ---------- */
  const textures = useRef(new Map<string, THREE.Texture>());
  const [base, setBase] = useState<{ cur: THREE.Texture | null; prev: THREE.Texture | null }>({ cur: null, prev: null });
  // what is on screen right now, kept outside React so cleanup never races a pending render
  const shown = useRef<{ cur: THREE.Texture | null; prev: THREE.Texture | null }>({ cur: null, prev: null });
  const baseFade = useRef(1);
  // unlit plate materials (the paper is a picture, not a lit surface), tinted by the day clock
  const mats = useMemo(
    () => ({
      prev: bakedMaterial({ polygonOffset: 3, key: "tex" }),
      cur: bakedMaterial({ transparent: true, polygonOffset: 2, key: "tex" }),
      blank: bakedMaterial({ color: city.map.palette.parchment, shade: false }),
      tiles: [0, 1].map(() => bakedMaterial({ transparent: true, depthWrite: false, polygonOffset: 1, key: "tex" })),
      board: bakedMaterial({ color: "#cdb78f", polygonOffset: 8 }),
      desk: bakedMaterial({ color: "#3a2a1e", shade: false }),
    }),
    [city],
  );
  useEffect(() => () => Object.values(mats).flat().forEach((m) => (m as THREE.Material).dispose()), [mats]);
  const curMat = useRef<THREE.MeshBasicMaterial>(mats.cur);
  curMat.current = mats.cur;

  useEffect(() => {
    const cache = textures.current;
    return () => {
      cache.forEach((t) => disposeTex(t));
      cache.clear();
    };
  }, [city]);

  useEffect(() => {
    if (!service) return;
    let alive = true;
    const t0 = performance.now();
    const show = (t: THREE.Texture) => {
      performance.mark(`plate-ready:${periodId}`);
      performance.measure(`base:${periodId}`, { start: t0, end: performance.now() });
      const cur = shown.current.cur;
      if (cur === t) return;
      // keep only the incoming plate and the one it fades from
      for (const [k, v] of textures.current)
        if (v !== t && v !== cur) {
          disposeTex(v);
          textures.current.delete(k);
        }
      baseFade.current = cur && !prefersReducedMotion() ? 0 : 1;
      shown.current = { cur: t, prev: cur };
      setBase(shown.current);
    };
    const cached = textures.current.get(periodId);
    if (cached) show(cached);
    else {
      let full = false;
      // the small preview first (instant), then the full plate replaces it
      service.preview(periodId).then((bmp) => {
        if (!bmp) return;
        if (!alive || full) return bmp.close();
        const t = bitmapTexture(bmp, gl);
        textures.current.set(`${periodId}:preview`, t);
        show(t);
      });
      service.base(periodId).then((bmp) => {
        if (!bmp) return;
        if (!alive) return bmp.close();
        full = true;
        const t = bitmapTexture(bmp, gl);
        textures.current.set(periodId, t);
        show(t);
      });
    }
    // warm the neighbouring periods while the user looks around
    const i = city.periods.findIndex((p) => p.id === periodId);
    const idle = (cb: () => void) => ("requestIdleCallback" in window ? (window as Window & { requestIdleCallback: (f: () => void) => number }).requestIdleCallback(cb) : setTimeout(cb, 400));
    idle(() => [city.periods[i - 1], city.periods[i + 1]].forEach((p) => p && service.prefetch(p.id)));
    // and every era's urban fabric (lots, fields, the occupancy grid), built in a worker, nearest era first
    const order = city.periods.map((p, k) => ({ id: p.id, d: Math.abs(k - i) + (k > i ? 0 : 0.5) })).filter((p) => p.d > 0).sort((a, b) => a.d - b.d).map((p) => p.id);
    const stopFabric = prefetchFabrics(city, order);
    return () => {
      alive = false;
      stopFabric();
    };
  }, [city, periodId, service, gl]);

  /* ---------- close-up tiles (two slots, the new one fades in over the old) ---------- */
  type Slot = { tex: THREE.Texture | null; view: View | null; period: string; opacity: number; target: number };
  const slots = useRef<Slot[]>([0, 1].map(() => ({ tex: null, view: null, period: "", opacity: 0, target: 0 })));
  const meshes = [useRef<THREE.Mesh>(null), useRef<THREE.Mesh>(null)];
  const active = useRef(0);
  const inflight = useRef<string | null>(null);
  const settle = useRef({ x: 0, z: 0, d: 0, still: 0 });
  const dir = useMemo(() => new THREE.Vector3(), []);
  useEffect(() => () => slots.current.forEach((s) => s.tex && disposeTex(s.tex)), []);

  useFrame((_, dtRaw) => {
    const dt = Math.min(dtRaw, 0.05);
    if (baseFade.current < 1) {
      baseFade.current = Math.min(1, baseFade.current + dt * 1.8);
      if (curMat.current) curMat.current.opacity = baseFade.current;
      if (baseFade.current >= 1) {
        shown.current = { cur: shown.current.cur, prev: null };
        setBase(shown.current);
      }
    }

    camera.getWorldDirection(dir);
    if (dir.y > -0.05) return;
    const t = -camera.position.y / dir.y;
    const tx = camera.position.x + dir.x * t, tz = camera.position.z + dir.z * t;
    const dist = Math.hypot(camera.position.x - tx, camera.position.y, camera.position.z - tz);
    const s = settle.current;
    const moved = Math.hypot(tx - s.x, tz - s.z) + Math.abs(dist - s.d);
    s.still = moved < dist * 0.0008 ? s.still + dt : 0;
    s.x = tx;
    s.z = tz;
    s.d = dist;

    const side = Math.min(Math.max((dist / f.scale) * 1.5, 160), Math.max(MW, MH));
    const wanted = TILE_PX / side > (BASE_EDGE / Math.max(MW, MH)) * 1.35;
    const sl = slots.current;
    const cur = sl[active.current];
    const cx = tx / f.scale + MW / 2, cy = tz / f.scale + MH / 2;
    if (!wanted) cur.target = 0;
    else {
      const v = cur.view;
      const stale = !v || cur.period !== periodId || Math.hypot((v.x0 + v.x1) / 2 - cx, (v.y0 + v.y1) / 2 - cy) > (v.x1 - v.x0) * 0.2 || side / (v.x1 - v.x0) > 1.35 || side / (v.x1 - v.x0) < 0.65;
      if (!stale) cur.target = 1;
      else if (service && (s.still > SETTLE_S || (cur.period !== periodId && s.still > 0.05))) {
        const view: View = { x0: cx - side / 2, y0: cy - side / 2, x1: cx + side / 2, y1: cy + side / 2 };
        const key = `${periodId}:${Math.round(view.x0)}:${Math.round(view.y0)}:${Math.round(side)}`;
        if (inflight.current !== key) {
          inflight.current = key;
          service.tile(periodId, view, TILE_PX).then((bmp) => {
            if (inflight.current !== key) return bmp?.close();
            inflight.current = null;
            if (!bmp) return;
            const nextIdx = 1 - active.current;
            const next = sl[nextIdx];
            if (next.tex) disposeTex(next.tex);
            next.tex = bitmapTexture(bmp, gl);
            next.view = view;
            next.period = periodId;
            next.opacity = 0;
            next.target = 1;
            const mesh = meshes[nextIdx].current;
            if (mesh) {
              const [wx, , wz] = mapToWorld(f, [(view.x0 + view.x1) / 2, (view.y0 + view.y1) / 2]);
              mesh.position.set(wx, 0, wz);
              mesh.scale.set(side * f.scale, side * f.scale, 1);
              mesh.renderOrder = 2;
              (mesh.material as THREE.MeshBasicMaterial).map = next.tex;
              (mesh.material as THREE.MeshBasicMaterial).needsUpdate = true;
            }
            const old = meshes[active.current].current;
            if (old) old.renderOrder = 1;
            sl[active.current].target = 0;
            active.current = nextIdx;
          });
        }
      }
    }
    sl.forEach((slot, i) => {
      const incoming = sl[active.current];
      const hold = i !== active.current && incoming.target === 1 && incoming.opacity < 0.98;
      const rate = slot.target > slot.opacity ? 3.5 : 2;
      if (!hold) slot.opacity += (slot.target - slot.opacity) * (1 - Math.exp(-rate * 3 * dt));
      if (Math.abs(slot.opacity - slot.target) < 0.004) slot.opacity = slot.target;
      const mesh = meshes[i].current;
      if (mesh) {
        (mesh.material as THREE.MeshBasicMaterial).opacity = slot.opacity;
        mesh.visible = slot.opacity > 0.002 && !!slot.tex;
      }
    });
  });

  const w = MW * f.scale;
  const h = MH * f.scale;
  const plane = useMemo(() => flippedPlane(w, h), [w, h]);
  const unit = useMemo(() => flippedPlane(1, 1), []);

  if (mats.prev.map !== base.prev) {
    mats.prev.map = base.prev;
    mats.prev.needsUpdate = true;
  }
  if (mats.cur.map !== base.cur) {
    mats.cur.map = base.cur;
    mats.cur.needsUpdate = true;
  }
  mats.cur.opacity = baseFade.current;

  return (
    <group>
      <group rotation-x={-Math.PI / 2}>
        {base.prev && <mesh geometry={plane} material={mats.prev} renderOrder={0} />}
        <mesh geometry={plane} material={base.cur ? mats.cur : mats.blank} renderOrder={0} />
      </group>
      {[0, 1].map((i) => (
        <mesh key={i} ref={meshes[i]} geometry={unit} material={mats.tiles[i]} rotation-x={-Math.PI / 2} visible={false} />
      ))}
      <mesh position-y={-0.36} material={mats.board}>
        <boxGeometry args={[w + 0.4, 0.7, h + 0.4]} />
      </mesh>
      <mesh rotation-x={-Math.PI / 2} position-y={-0.75} material={mats.desk}>
        <planeGeometry args={[w * 4, h * 4]} />
      </mesh>
    </group>
  );
}

/** ImageBitmaps can't be flipped on upload, so the plane's UVs are flipped instead. */
function flippedPlane(w: number, h: number) {
  const g = new THREE.PlaneGeometry(w, h);
  const uv = g.getAttribute("uv") as THREE.BufferAttribute;
  for (let i = 0; i < uv.count; i++) uv.setY(i, 1 - uv.getY(i));
  uv.needsUpdate = true;
  return g;
}

function bitmapTexture(bmp: ImageBitmap, gl: THREE.WebGLRenderer) {
  const t = new THREE.Texture(bmp);
  t.flipY = false;
  t.colorSpace = THREE.SRGBColorSpace;
  t.anisotropy = Math.min(8, gl.capabilities.getMaxAnisotropy());
  t.generateMipmaps = true;
  t.minFilter = THREE.LinearMipmapLinearFilter;
  t.needsUpdate = true;
  return t;
}

function disposeTex(t: THREE.Texture) {
  t.dispose();
  const img = t.image as ImageBitmap | undefined;
  if (img && "close" in img) img.close();
}
