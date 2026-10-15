import { useEffect, useRef } from "react";
import { useFrame, useThree } from "@react-three/fiber";
import * as THREE from "three";
import type { City } from "@/content/schema";
import { useStore, landmarkById, resolveVariant, currentFocus, type Focus } from "../store";
import { frameOf, mapToWorld, worldBounds, degToRad } from "../coords";
import { clamp, prefersReducedMotion } from "../motion";

/**
 * Orbit-style rig expressed as {target, distance, tilt, heading}.
 * The user and the app both only ever edit the *goal* pose; the rendered pose
 * damps toward it every frame. That makes every transition interruptible by
 * construction: new input simply moves the goal.
 */
export type Pose = { tx: number; tz: number; distance: number; tilt: number; heading: number };

const FOV = 28;

function startPose(city: City): Pose {
  const f = frameOf(city);
  const cam = city.camera;
  if (cam) {
    const [x, , z] = mapToWorld(f, cam.start.target);
    return { tx: x, tz: z, distance: cam.start.distance, tilt: degToRad(cam.start.tilt), heading: degToRad(cam.start.heading) };
  }
  return { tx: 0, tz: 0, distance: Math.max(f.width, f.height) * f.scale * 0.9, tilt: degToRad(50), heading: 0 };
}

export function CameraRig({ city }: { city: City }) {
  const { camera, gl, size } = useThree();
  const goal = useRef<Pose>(startPose(city));
  const cur = useRef<Pose>({ ...goal.current });
  const returnPose = useRef<Pose | null>(null);
  const prevMode = useRef(useStore.getState().mode);
  const rate = useRef(8);
  const f = frameOf(city);
  const bounds = worldBounds(f);
  const minD = city.camera?.minDistance ?? 3;
  const maxD = city.camera?.maxDistance ?? Math.max(f.width, f.height) * f.scale * 1.6;
  // dev probe: jump the camera to a map point (distance in world units, angles in degrees) for scripted checks
  useEffect(() => {
    if (!import.meta.env.DEV) return;
    (window as unknown as { __pose: unknown }).__pose = (mx: number, my: number, distance: number, tilt = 45, heading = 0) => {
      const [x, , z] = mapToWorld(f, [mx, my]);
      goal.current = { tx: x, tz: z, distance, tilt: degToRad(tilt), heading: degToRad(heading) };
      cur.current = { ...goal.current };
    };
  }, [f]);

  // Reset on city change.
  useEffect(() => {
    goal.current = startPose(city);
    cur.current = { ...goal.current };
    returnPose.current = null;
    prevKey.current = null;
  }, [city]);

  // React to focus / immersion changes from the store.
  const prevKey = useRef<string | null>(null);
  useEffect(() => {
      const onState = (s: ReturnType<typeof useStore.getState>) => {
        const focus = currentFocus(s);
        const key = focus ? `${focus.kind}:${focus.id}` : null;
        const poseFor = (fc: Focus, immersed: boolean) => {
          const [x, , z] = mapToWorld(f, fc.position);
          const l = fc.kind === "landmark" ? landmarkById(city, fc.id) : null;
          // tall, narrow monuments (arches, columns) need room for their height as well as their footprint
          const md = l?.model as { height?: number; fallback?: { height?: number } } | undefined;
          const fb = md?.fallback ?? md;
          const tall = (fb?.height ?? 0) * (l?.scale ?? 1) * 2.2;
          const fp = Math.max(fc.size, tall, 30) * f.scale;
          // wide screens show the notebook on the left as well: the subject sits in a narrower gap
          const both = size.width > 1100 && fc.kind !== "spot";
          const distance = immersed ? clamp(fp * 1.5, minD, maxD) : l?.focus?.distance ?? clamp(fp * (both ? 2.75 : 2.4), minD, maxD);
          const tilt = immersed ? 26 : l?.focus?.tilt ?? 42;
          const heading = l?.focus?.heading !== undefined ? degToRad(l.focus.heading) : goal.current.heading;
          // The info panel covers the right edge on wide screens: shift the target so the subject sits in the open area.
          // right panel 426 px, notebook 398 px: centre the subject between them
          const panelPx = both ? 14 : size.width > 900 ? 210 : 0;
          const perPx = (2 * distance * Math.tan(degToRad(FOV) / 2)) / size.height;
          const off = panelPx * perPx;
          return { tx: x + Math.cos(heading) * off, tz: z - Math.sin(heading) * off, distance, tilt: degToRad(tilt), heading };
        };
        if (key !== prevKey.current) {
          if (focus && !prevKey.current) returnPose.current = { ...goal.current };
          if (focus) {
            goal.current = poseFor(focus, s.mode === "immersed");
            rate.current = 3.2;
          } else if (returnPose.current) {
            goal.current = { ...returnPose.current };
            returnPose.current = null;
            rate.current = 3.2;
          }
          prevKey.current = key;
        }
        if (s.mode !== prevMode.current) {
          if (focus && (s.mode === "immersed" || (s.mode === "focused" && prevMode.current === "immersed"))) {
            goal.current = poseFor(focus, s.mode === "immersed");
            rate.current = 2.6;
          }
          prevMode.current = s.mode;
        }
      };
      onState(useStore.getState()); // a deep link may have focused something before the rig mounted
      return useStore.subscribe(onState);
    },
    [city, f, minD, maxD, size.width, size.height],
  );

  /* ---------- pointer / wheel / keyboard / touch input ---------- */
  useEffect(() => {
    const el = gl.domElement;
    const pointers = new Map<number, { x: number; y: number }>();
    let dragging = false;
    let rotating = false;
    let pinchDist = 0;
    let moved = 0;

    const groundPointAt = (clientX: number, clientY: number): THREE.Vector3 | null => {
      const rect = el.getBoundingClientRect();
      const ndc = new THREE.Vector2(((clientX - rect.left) / rect.width) * 2 - 1, -((clientY - rect.top) / rect.height) * 2 + 1);
      const ray = new THREE.Raycaster();
      ray.setFromCamera(ndc, camera);
      const hit = new THREE.Vector3();
      return ray.ray.intersectPlane(new THREE.Plane(new THREE.Vector3(0, 1, 0), 0), hit) ? hit : null;
    };

    const worldPerPixel = () => (2 * cur.current.distance * Math.tan(degToRad(FOV) / 2)) / size.height;

    const pan = (dx: number, dy: number) => {
      const g = goal.current;
      const k = worldPerPixel();
      const rx = Math.cos(g.heading),
        rz = -Math.sin(g.heading); // right vector
      const fx = -Math.sin(g.heading),
        fz = -Math.cos(g.heading); // ground-forward (away from viewer)
      const ky = k / Math.max(0.35, Math.sin(cur.current.tilt));
      g.tx += -rx * dx * k + fx * dy * ky;
      g.tz += -rz * dx * k + fz * dy * ky;
      g.tx = clamp(g.tx, bounds.minX, bounds.maxX);
      g.tz = clamp(g.tz, bounds.minZ, bounds.maxZ);
      rate.current = 10;
    };

    const zoomBy = (factor: number, clientX?: number, clientY?: number) => {
      const g = goal.current;
      const next = clamp(g.distance * factor, minD, maxD);
      const real = next / g.distance;
      if (clientX !== undefined && clientY !== undefined) {
        const p = groundPointAt(clientX, clientY);
        if (p) {
          // zoom toward the cursor: keep the ground point under the cursor fixed.
          g.tx = clamp(p.x + (g.tx - p.x) * real, bounds.minX, bounds.maxX);
          g.tz = clamp(p.z + (g.tz - p.z) * real, bounds.minZ, bounds.maxZ);
        }
      }
      g.distance = next;
      rate.current = 10;
    };

    const onDown = (e: PointerEvent) => {
      pointers.set(e.pointerId, { x: e.clientX, y: e.clientY });
      if (e.pointerType === "touch") useStore.getState().setTouch(true);
      if (pointers.size === 1) {
        dragging = true;
        rotating = e.button === 2 || e.shiftKey || e.ctrlKey;
        moved = 0;
      } else if (pointers.size === 2) {
        const [a, b] = [...pointers.values()];
        pinchDist = Math.hypot(a.x - b.x, a.y - b.y);
      }
      el.setPointerCapture(e.pointerId);
    };
    const onMove = (e: PointerEvent) => {
      const prev = pointers.get(e.pointerId);
      if (!prev) return;
      const dx = e.clientX - prev.x,
        dy = e.clientY - prev.y;
      pointers.set(e.pointerId, { x: e.clientX, y: e.clientY });
      if (pointers.size === 2) {
        const [a, b] = [...pointers.values()];
        const d = Math.hypot(a.x - b.x, a.y - b.y);
        if (pinchDist > 0) zoomBy(pinchDist / d);
        pinchDist = d;
        return;
      }
      if (!dragging) return;
      moved += Math.abs(dx) + Math.abs(dy);
      if (rotating) {
        goal.current.heading -= dx * 0.005;
        goal.current.tilt = clamp(goal.current.tilt + dy * 0.004, degToRad(18), degToRad(85));
        rate.current = 10;
      } else {
        pan(dx, dy);
      }
      if (moved > 4) el.style.cursor = "grabbing";
    };
    const onUp = (e: PointerEvent) => {
      pointers.delete(e.pointerId);
      if (pointers.size === 0) {
        dragging = false;
        rotating = false;
        el.style.cursor = "";
      }
      pinchDist = 0;
    };
    const onWheel = (e: WheelEvent) => {
      e.preventDefault();
      const factor = Math.exp(clamp(e.deltaY, -120, 120) * 0.0025);
      zoomBy(factor, e.clientX, e.clientY);
    };
    const onKey = (e: KeyboardEvent) => {
      // overlays (the picture viewer) handle their own keys first
      if (e.defaultPrevented || (e.target as HTMLElement)?.tagName === "INPUT") return;
      const step = 40;
      switch (e.key) {
        case "ArrowLeft":
          pan(step, 0);
          break;
        case "ArrowRight":
          pan(-step, 0);
          break;
        case "ArrowUp":
          pan(0, step);
          break;
        case "ArrowDown":
          pan(0, -step);
          break;
        case "+":
        case "=":
          zoomBy(0.8);
          break;
        case "-":
        case "_":
          zoomBy(1.25);
          break;
        case "q":
          goal.current.heading += 0.2;
          break;
        case "e":
          goal.current.heading -= 0.2;
          break;
        case "Escape":
          useStore.getState().back();
          break;
        default:
          return;
      }
      e.preventDefault();
    };
    const onContext = (e: Event) => e.preventDefault();

    el.addEventListener("pointerdown", onDown);
    el.addEventListener("pointermove", onMove);
    el.addEventListener("pointerup", onUp);
    el.addEventListener("pointercancel", onUp);
    el.addEventListener("wheel", onWheel, { passive: false });
    el.addEventListener("contextmenu", onContext);
    window.addEventListener("keydown", onKey);
    el.style.touchAction = "none";
    return () => {
      el.removeEventListener("pointerdown", onDown);
      el.removeEventListener("pointermove", onMove);
      el.removeEventListener("pointerup", onUp);
      el.removeEventListener("pointercancel", onUp);
      el.removeEventListener("wheel", onWheel);
      el.removeEventListener("contextmenu", onContext);
      window.removeEventListener("keydown", onKey);
    };
  }, [gl, camera, size.height, bounds.minX, bounds.maxX, bounds.minZ, bounds.maxZ, minD, maxD]);

  /* ---------- per-frame damping and camera placement ---------- */
  useFrame((_, dt) => {
    const d = Math.min(dt, 0.05);
    const g = goal.current,
      c = cur.current;
    const r = prefersReducedMotion() ? 1000 : rate.current;
    const k = 1 - Math.exp(-r * d);
    c.tx += (g.tx - c.tx) * k;
    c.tz += (g.tz - c.tz) * k;
    c.distance += (g.distance - c.distance) * k;
    c.tilt += (g.tilt - c.tilt) * k;
    c.heading += (g.heading - c.heading) * k;

    const px = c.tx + c.distance * Math.cos(c.tilt) * Math.sin(c.heading);
    const py = c.distance * Math.sin(c.tilt);
    const pz = c.tz + c.distance * Math.cos(c.tilt) * Math.cos(c.heading);
    camera.position.set(px, py, pz);
    camera.lookAt(c.tx, 0, c.tz);

    if (camera instanceof THREE.PerspectiveCamera) {
      // keep the depth range tight around what is visible: near grows with distance
      const near = Math.min(8, Math.max(0.02, c.distance * 0.06));
      const far = c.distance * 6 + Math.max(f.width, f.height) * f.scale * 1.5;
      if (camera.fov !== FOV || Math.abs(camera.near - near) > near * 0.05 || Math.abs(camera.far - far) > far * 0.05) {
        camera.fov = FOV;
        camera.near = near;
        camera.far = far;
        camera.updateProjectionMatrix();
      }
    } else if (camera instanceof THREE.OrthographicCamera) {
      const zoom = size.height / (2 * c.distance * Math.tan(degToRad(FOV) / 2));
      if (Math.abs(camera.zoom - zoom) > 1e-3) {
        camera.zoom = zoom;
        camera.updateProjectionMatrix();
      }
    }

    const span = Math.max(f.width, f.height) * f.scale;
    const level = c.distance > span * 0.55 ? "city" : c.distance > span * 0.22 ? "district" : "landmark";
    useStore.getState().setZoomLevel(level);
  });

  return null;
}

/** Period-aware name for HUD use. */
export function focusedName(city: City | null, id: string | null, periodId: string | null) {
  const l = landmarkById(city, id);
  return l ? resolveVariant(l, periodId).name : "";
}
