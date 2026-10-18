import { useEffect, useMemo, useRef } from "react";
import { useFrame, useThree } from "@react-three/fiber";
import * as THREE from "three";
import type { City } from "@/content/schema";
import { frameOf } from "../coords";
import { getFabric, type Insula } from "./fabric";
import { useStore } from "../store";
import { prefersReducedMotion } from "../motion";
import { groundPointer } from "./pointer";
import { piecesFor, type Piece, type PieceMesh } from "./massingKit";
import { bakedMaterial } from "../render/baked";
import { registerForWarmup } from "../render/warmup";

const CAP: Record<PieceMesh, number> = { body: 3000, roof: 2500, trim: 6000, hutBody: 400, hutRoof: 400 };
const NEIGHBOUR_R = 45;

/**
 * Hover any city block on the drawn map and its buildings rise as plain grey
 * massing blocks with crisp edges (an architect's study model), with the
 * neighbouring blocks rising a little lower. Hovering or visiting a shop or
 * workshop raises its block too, with that building picked out in terracotta.
 * Only a few hundred boxes ever exist at once.
 */
export function HoverMassing({ city }: { city: City }) {
  const f = frameOf(city);
  const periodId = useStore((s) => s.periodId) ?? city.defaultPeriodId;
  const fabric = useMemo(() => getFabric(city, periodId), [city, periodId]);
  const { camera, gl } = useThree();
  const progress = useRef(new Map<number, number>()); // insula id -> 0..1
  const pointer = useRef<{ x: number; y: number; inside: boolean; buttons: number }>({ x: 0, y: 0, inside: false, buttons: 0 });
  const dummy = useMemo(() => new THREE.Object3D(), []);
  const ray = useMemo(() => new THREE.Raycaster(), []);
  const plane = useMemo(() => new THREE.Plane(new THREE.Vector3(0, 1, 0), 0), []);
  const hit = useMemo(() => new THREE.Vector3(), []);
  const accent = useMemo(() => new THREE.Color("#b5654a"), []);

  const geometries = useMemo(() => {
    const box = new THREE.BoxGeometry(1, 1, 1).translate(0, 0.5, 0);
    const roof = new THREE.ConeGeometry(Math.SQRT1_2, 1, 4, 1).rotateY(Math.PI / 4).translate(0, 0.5, 0);
    const hutBody = new THREE.CylinderGeometry(0.5, 0.5, 1, 10).translate(0, 0.5, 0);
    const hutRoof = new THREE.ConeGeometry(0.5, 1, 10).translate(0, 0.5, 0);
    return { body: box, roof, trim: box.clone(), hutBody, hutRoof } as Record<PieceMesh, THREE.BufferGeometry>;
  }, []);
  // facade rhythm per era, shared by every massing material (uniforms, so no recompiles)
  const uniforms = useMemo(
    () => ({ uStorey: { value: 3.3 * f.scale }, uBay: { value: 3.0 * f.scale }, uWinW: { value: 0.14 }, uWinH: { value: 0.38 }, uArch: { value: 0 } }),
    [f.scale],
  );
  useEffect(() => {
    const F: Record<string, [number, number, number, number, number]> = {
      // storey, bay, half window width, window height, arched shop openings
      archaic: [3.0, 4.0, 0.0, 0.0, 0],
      antique: [3.4, 4.2, 0.1, 0.32, 1],
      medieval: [3.2, 3.6, 0.1, 0.34, 1],
      "early-modern": [3.6, 3.3, 0.12, 0.42, 0],
      gothic: [3.0, 2.8, 0.13, 0.42, 0],
      courtyard: [3.6, 4.6, 0.07, 0.22, 1],
      sinic: [4.2, 3.4, 0.0, 0.0, 0],
      japanese: [3.0, 1.9, 0.3, 0.42, 0],
      mesoamerican: [3.2, 4.4, 0.0, 0.0, 0],
      andean: [3.0, 3.6, 0.05, 0.3, 0],
      sahel: [3.3, 3.8, 0.04, 0.16, 0],
      kraal: [3.0, 4.0, 0.0, 0.0, 0],
    };
    const [st, bay, ww, wh, arch] = F[fabric.style] ?? F.antique;
    uniforms.uStorey.value = st * f.scale;
    uniforms.uBay.value = bay * f.scale;
    uniforms.uWinW.value = ww;
    uniforms.uWinH.value = wh;
    uniforms.uArch.value = arch;
  }, [fabric.style, uniforms, f.scale]);
  const materials = useMemo(() => {
    // unlit study-model look: fixed light, window grid and inked edges, all in one tiny shader
    // Facades per era: Roman insulae have few small windows over wide arched shop
    // openings; later houses get taller, more regular windows.
    const windows = `
      if (abs(vBN.y) < 0.5) {
        vec2 tg = normalize(vec2(-vBN.z, vBN.x));
        float t = dot(vWP.xz, tg) / uBay;
        float y = vWP.y / uStorey;
        float fx = fract(t), fy = fract(y);
        float dx = (fx - 0.5) / 0.36;
        float archTop = mix(0.72, 0.56 + 0.2 * sqrt(max(0.0, 1.0 - dx * dx)), uArch);
        float shop = step(0.14, fx) * step(fx, 0.86) * step(fy, archTop) * (1.0 - step(1.0, y));
        float win = step(0.5 - uWinW, fx) * step(fx, 0.5 + uWinW) * step(0.36, fy) * step(fy, 0.36 + uWinH) * step(1.0, y);
        float band = (1.0 - smoothstep(0.0, fwidth(y) * 1.5, abs(fy))) * step(1.0, y);
        float vis = clamp(1.4 - fwidth(t) * 4.0, 0.0, 1.0);
        gl_FragColor.rgb = mix(gl_FragColor.rgb, vec3(0.16, 0.11, 0.08), shop * 0.78 * vis);
        gl_FragColor.rgb = mix(gl_FragColor.rgb, vec3(0.12, 0.09, 0.07), win * 0.72 * vis);
        gl_FragColor.rgb = mix(gl_FragColor.rgb, gl_FragColor.rgb * 0.82, band * 0.6 * vis);
      }
      // a little darker where the walls meet the ground, like a painted miniature
      gl_FragColor.rgb *= mix(0.8, 1.0, smoothstep(0.0, uStorey * 0.9, vWP.y));`;
    const edges = `
      float e = min(min(vUv.x, 1.0 - vUv.x), min(vUv.y, 1.0 - vUv.y));
      float line = 1.0 - smoothstep(0.0, fwidth(e) * 1.4, e);
      gl_FragColor.rgb = mix(gl_FragColor.rgb, vec3(0.04, 0.035, 0.03), line * 0.8);`;
    const withWin = bakedMaterial({ extraFrag: windows + edges, extraUniforms: uniforms, key: "massing-w" });
    const plain = () => bakedMaterial({ extraFrag: edges, extraUniforms: uniforms, key: "massing" });
    const out = { body: withWin, roof: plain(), trim: plain(), hutBody: plain(), hutRoof: plain() } as Record<PieceMesh, THREE.MeshBasicMaterial>;
    registerForWarmup(out.body, out.roof);
    return out;
  }, [uniforms]);
  // soft contact shadows under raised buildings (a baked blur, one draw call)
  const shadow = useMemo(() => {
    const c = document.createElement("canvas");
    c.width = c.height = 64;
    const g = c.getContext("2d")!;
    g.filter = "blur(7px)";
    g.fillStyle = "#000";
    g.fillRect(14, 14, 36, 36);
    const tex = new THREE.CanvasTexture(c);
    const mat = new THREE.MeshBasicMaterial({ map: tex, color: "#3a2a1e", transparent: true, opacity: 0.42, depthWrite: false, toneMapped: false });
    const geo = new THREE.PlaneGeometry(1, 1).rotateX(-Math.PI / 2);
    registerForWarmup(mat);
    return { tex, mat, geo };
  }, []);
  const shadowMesh = useRef<THREE.InstancedMesh>(null);
  useEffect(
    () => () => {
      Object.values(geometries).forEach((g) => g.dispose());
      Object.values(materials).forEach((m) => m.dispose());
      shadow.tex.dispose();
      shadow.mat.dispose();
      shadow.geo.dispose();
    },
    [geometries, materials, shadow],
  );
  const meshes = useRef<Partial<Record<PieceMesh, THREE.InstancedMesh | null>>>({});
  const pieceCache = useRef(new Map<number, Piece[]>());
  const color = useMemo(() => new THREE.Color(), []);
  useEffect(() => {
    progress.current.clear();
    pieceCache.current.clear();
  }, [fabric]);

  useEffect(() => {
    const el = gl.domElement;
    const move = (e: PointerEvent) => {
      const r = el.getBoundingClientRect();
      pointer.current = { x: ((e.clientX - r.left) / r.width) * 2 - 1, y: -((e.clientY - r.top) / r.height) * 2 + 1, inside: true, buttons: e.buttons };
    };
    const leave = () => (pointer.current.inside = false);
    el.addEventListener("pointermove", move);
    el.addEventListener("pointerleave", leave);
    return () => {
      el.removeEventListener("pointermove", move);
      el.removeEventListener("pointerleave", leave);
    };
  }, [gl]);

  useFrame((_, dtRaw) => {
    const dt = Math.min(dtRaw, 0.1);
    const st = useStore.getState();
    const [MW, MH] = city.map.size;

    /* ---- which blocks should be up ---- */
    const want = new Map<number, number>(); // id -> target height factor
    let accentLot = -1;
    const raise = (b: Insula | null, primary: number) => {
      if (!b) return;
      want.set(b.id, Math.max(want.get(b.id) ?? 0, primary));
      for (const n of fabric.index.near(b.x, b.y, NEIGHBOUR_R)) if (!want.has(n.id)) want.set(n.id, 0.55);
    };
    // pointer over the map (not while dragging, not while a landmark is under it)
    let hovered: Insula | null = null;
    const p = pointer.current;
    groundPointer.valid = false;
    if (p.inside && p.buttons === 0 && !st.hoveredId && st.mode !== "immersed") {
      ray.setFromCamera(new THREE.Vector2(p.x, p.y), camera);
      if (ray.ray.intersectPlane(plane, hit)) {
        groundPointer.valid = true;
        groundPointer.mx = hit.x / f.scale + MW / 2;
        groundPointer.my = hit.z / f.scale + MH / 2;
        hovered = fabric.index.at(groundPointer.mx, groundPointer.my, 6);
        raise(hovered, 1);
      }
    }
    if (st.hoveredBlockId !== (hovered ? hovered.id : null)) st.setHoveredBlock(hovered ? hovered.id : null);
    // shops and workshops: hovered marker or the place being visited
    const spotId = st.focusedSpotId ?? (st.hoveredFeature?.kind === "spot" ? st.hoveredFeature.id : null);
    if (spotId) {
      const sp = city.spots.find((s) => s.id === spotId);
      if (sp) {
        const b = fabric.index.at(sp.position[0], sp.position[1], 40);
        if (b) {
          raise(b, 1);
          let best = Infinity;
          for (let i = b.lot0; i < b.lot1; i++) {
            const l = fabric.lots[i];
            if (l.kind === "court") continue;
            const d = Math.hypot(l.x - sp.position[0], l.y - sp.position[1]);
            if (d < best) {
              best = d;
              accentLot = i;
            }
          }
        }
      }
    }

    /* ---- animate ---- */
    const prog = progress.current;
    const k = prefersReducedMotion() ? 1 : 1 - Math.exp(-6 * dt);
    for (const [id, t] of want) prog.set(id, (prog.get(id) ?? 0) + (t - (prog.get(id) ?? 0)) * k);
    for (const [id, v] of prog) {
      if (want.has(id)) continue;
      const nv = v * (1 - k);
      if (nv < 0.01) prog.delete(id);
      else prog.set(id, nv);
    }

    /* ---- write instances ---- */
    const counts: Record<PieceMesh, number> = { body: 0, roof: 0, trim: 0, hutBody: 0, hutRoof: 0 };
    let shadows = 0;
    const sm = shadowMesh.current;
    const sc = f.scale;
    const ox = -MW / 2, oy = -MH / 2;
    for (const [id, v] of prog) {
      const b = fabric.insulae[id];
      let pieces = pieceCache.current.get(id);
      if (!pieces) {
        pieces = piecesFor(fabric.style, b, fabric.lots, city.world);
        pieceCache.current.set(id, pieces);
      }
      const primary = (want.get(id) ?? 0) >= 1;
      const ease = 1 - Math.pow(1 - Math.min(1, v), 3);
      for (let k = 0; k < pieces.length; k++) {
        const pc = pieces[k];
        const m = meshes.current[pc.mesh];
        if (!m || counts[pc.mesh] >= CAP[pc.mesh]) continue;
        dummy.position.set((pc.x + ox) * sc, pc.z * ease * sc, (pc.y + oy) * sc);
        dummy.rotation.set(0, -pc.a, 0);
        dummy.scale.set(pc.w * sc, Math.max(0.0001, pc.h * ease) * sc, pc.d * sc);
        dummy.updateMatrix();
        const n = counts[pc.mesh]++;
        m.setMatrixAt(n, dummy.matrix);
        if (sm && pc.z === 0 && (pc.mesh === "body" || pc.mesh === "hutBody") && shadows < CAP.body) {
          // shadow falls toward the south-east, longer for taller buildings
          const len = pc.h * ease * 0.35;
          dummy.position.set((pc.x + len * 0.55 + ox) * sc, 0.004, (pc.y + len * 0.7 + oy) * sc);
          dummy.scale.set((pc.w + len) * sc * 1.25, 1, (pc.d + len) * sc * 1.25);
          dummy.updateMatrix();
          sm.setMatrixAt(shadows++, dummy.matrix);
        }
        color.set(pc.color);
        if (!primary) color.multiplyScalar(0.92);
        m.setColorAt(n, color);
      }
    }
    // the visited shop's own building, picked out in terracotta
    if (accentLot >= 0) {
      const l = fabric.lots[accentLot];
      const m = meshes.current.trim;
      if (m && counts.trim < CAP.trim) {
        const v = prog.get(l.g) ?? 0;
        const ease = 1 - Math.pow(1 - Math.min(1, v), 3);
        dummy.position.set((l.x + ox) * sc, 0, (l.y + oy) * sc);
        dummy.rotation.set(0, -l.a, 0);
        dummy.scale.set(l.w * 1.02 * sc, Math.max(0.0001, l.h * 1.01 * ease) * sc, l.d * 1.02 * sc);
        dummy.updateMatrix();
        const n = counts.trim++;
        m.setMatrixAt(n, dummy.matrix);
        m.setColorAt(n, accent);
      }
    }
    if (sm) {
      sm.count = shadows;
      sm.visible = shadows > 0;
      if (shadows) sm.instanceMatrix.needsUpdate = true;
    }
    for (const key of Object.keys(counts) as PieceMesh[]) {
      const m = meshes.current[key];
      if (!m) continue;
      m.count = counts[key];
      m.visible = counts[key] > 0;
      if (counts[key] > 0) {
        m.instanceMatrix.needsUpdate = true;
        if (m.instanceColor) m.instanceColor.needsUpdate = true;
      }
    }
  });

  return (
    <group>
      {(Object.keys(geometries) as PieceMesh[]).map((k) => (
        <instancedMesh key={k} ref={(m) => (meshes.current[k] = m)} args={[geometries[k], materials[k], CAP[k]]} frustumCulled={false} raycast={() => null} />
      ))}
      <instancedMesh ref={shadowMesh} args={[shadow.geo, shadow.mat, CAP.body]} frustumCulled={false} raycast={() => null} renderOrder={3} />
    </group>
  );
}
