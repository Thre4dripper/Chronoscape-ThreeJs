import { useMemo } from "react";
import { useFrame } from "@react-three/fiber";
import * as THREE from "three";
import { overlay, type OverlayEntry } from "./registry";

const PAD = 4;

/** Panels and other HUD pieces labels must keep clear of, re-measured a few times a second. */
let blockers: [number, number, number, number][] = [];
let blockersAt = 0;
function hudBlockers(now: number) {
  if (now - blockersAt > 250) {
    blockersAt = now;
    blockers = [];
    for (const el of document.querySelectorAll<HTMLElement>("aside.panel, [data-hud-block]")) {
      const r = el.getBoundingClientRect();
      if (r.width > 0 && r.height > 0) blockers.push([r.left, r.top, r.right, r.bottom]);
    }
  }
  return blockers;
}

export function OverlayProjector() {
  const v = useMemo(() => new THREE.Vector3(), []);
  useFrame(({ camera, size, clock }) => {
    const list: { e: OverlayEntry; x: number; y: number; key: number }[] = [];
    for (const e of overlay.entries.values()) {
      if (!e.candidate) {
        hide(e);
        continue;
      }
      v.copy(e.pos).project(camera);
      if (v.z > 1 || v.z < -1) {
        hide(e);
        continue;
      }
      const x = (v.x + 1) * 0.5 * size.width;
      const y = (1 - v.y) * 0.5 * size.height - e.offsetY;
      if (x < -50 || y < -50 || x > size.width + 50 || y > size.height + 50) {
        hide(e);
        continue;
      }
      // hysteresis: items already on screen keep a small edge so borderline pairs don't trade places
      list.push({ e, x, y, key: (e.force ? 1000 : 0) + e.priority + (e.shown ? 2 : 0) });
    }
    list.sort((a, b) => b.key - a.key);
    // read phase: measure every unmeasured element before any style is written (one layout, not one per label)
    for (const it of list) {
      if (!it.e.w) {
        it.e.w = it.e.el.offsetWidth;
        it.e.h = it.e.el.offsetHeight;
      }
    }
    // keep clear of the HUD: title and timeline across the top, status and controls along the bottom
    const placed: [number, number, number, number][] = [
      [0, 0, size.width, 140],
      [0, size.height - 100, size.width, size.height],
      ...hudBlockers(clock.elapsedTime * 1000),
    ];
    const hits = (r: [number, number, number, number]) => {
      for (const p of placed) if (r[0] < p[2] && r[2] > p[0] && r[1] < p[3] && r[3] > p[1]) return true;
      return false;
    };
    let z = list.length + 10;
    for (const it of list) {
      const { e } = it;
      const x0 = Math.round(it.x - e.w / 2);
      let y0 = Math.round(it.y - e.h / 2);
      let r: [number, number, number, number] = [x0 - PAD, y0 - PAD, x0 + e.w + PAD, y0 + e.h + PAD];
      if (hits(r)) {
        if (!e.force) {
          hide(e);
          continue;
        }
        // a label that must show (the focused or hovered one) steps up or down out of the way instead
        for (const k of [-1, 1, -2, 2, -3, 3]) {
          const yy = y0 + k * (e.h + PAD * 2);
          const rr: [number, number, number, number] = [x0 - PAD, yy - PAD, x0 + e.w + PAD, yy + e.h + PAD];
          if (!hits(rr)) {
            y0 = yy;
            r = rr;
            break;
          }
        }
      }
      placed.push(r);
      const tf = `translate3d(${x0}px, ${y0}px, 0)`;
      if (e.el.style.transform !== tf) e.el.style.transform = tf;
      const zs = String(z--);
      if (e.el.style.zIndex !== zs) e.el.style.zIndex = zs;
      if (!e.shown || e.el.dataset.shown !== "1") {
        e.shown = true;
        e.el.dataset.shown = "1";
      }
    }
  });
  return null;
}

function hide(e: OverlayEntry) {
  if (e.shown || e.el.dataset.shown === "1") {
    e.shown = false;
    delete e.el.dataset.shown;
  }
}
