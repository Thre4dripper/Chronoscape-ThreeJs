import { useEffect, useRef, useState } from "react";
import type { Atlas, AtlasMap } from "@/content/schema";
import { atlasCatalog } from "@/content/registry";
import { useNav } from "@/nav";
import { compassRose, drawMap, hexA, loadLand, project, serpent, ship, WORLD_LABELS, WORLD_ROSES, type LonLat, type View } from "@/world/world";
import { drawGlyph, glyphImage, type Glyph } from "@/world/glyphs";

/**
 * The title page's world: an engraved chart drifting slowly east, with ships
 * under sail, a sea serpent and compass roses. Drag it left or right; let go
 * and it eases back to its own pace. Every city on the shelf has a town mark;
 * point at one and a drawing of the place rises from the paper with its atlas
 * and eras; click to unfold it (or open its atlas). The ships, the serpent and
 * the roses answer to the pointer too.
 *
 * The chart is drawn once into an offscreen tile; each frame copies it and
 * draws only the few moving things.
 */
const LAT_TOP = 78, LAT_BOTTOM = -60;
const LANES: { lane: [LonLat, LonLat]; caption: string }[] = [
  { lane: [[-62, 33], [-22, 14]], caption: "A galleon homeward from the Indies, laden with silver" },
  { lane: [[-48, -6], [-12, -30]], caption: "A carrack running south for the Cape of Good Hope" },
  { lane: [[52, -8], [94, -26]], caption: "A spice ship crossing the Indian Ocean on the monsoon wind" },
  { lane: [[-170, 14], [-128, -4]], caption: "The Manila galleon, on its long Pacific crossing" },
  { lane: [[150, 22], [178, 4]], caption: "A trading junk bound for the islands" },
  { lane: [[-30, 46], [-12, 38]], caption: "A caravel feeling its way along the Atlantic coast" },
];
const ROSE_CAPTION = "A compass rose. Its rhumb lines gave sailors their bearings across open sea.";
const SERPENT_CAPTION = "Hic sunt dracones: here be dragons. Map-makers filled unknown seas with monsters.";

/** The cities of every atlas, one town mark per place (Rome is in three atlases). */
type Place = { title: string; at: LonLat; glyph: Glyph; entries: { atlas: Atlas; map: AtlasMap }[] };
function places(): Place[] {
  const by = new Map<string, Place>();
  for (const a of atlasCatalog.atlases)
    for (const m of a.maps) {
      const key = `${m.title}:${m.at.join(",")}`;
      let p = by.get(key);
      if (!p) by.set(key, (p = { title: m.title, at: m.at, glyph: m.glyph, entries: [] }));
      p.entries.push({ atlas: a, map: m });
    }
  return [...by.values()];
}

type Hover =
  | { kind: "place"; place: Place }
  | { kind: "ship"; caption: string }
  | { kind: "serpent" }
  | { kind: "rose"; index: number }
  | null;

export function WorldDrift({ speed = 1 }: { speed?: number }) {
  const ref = useRef<HTMLCanvasElement>(null);
  const pop = useRef<HTMLDivElement>(null);
  const speedRef = useRef(speed);
  speedRef.current = speed;
  const [hover, setHover] = useState<Hover>(null);
  const hoverRef = useRef<Hover>(null);
  hoverRef.current = hover;

  useEffect(() => {
    const canvas = ref.current!;
    const ctx = canvas.getContext("2d")!;
    let raf = 0;
    let alive = true;
    let tile: HTMLCanvasElement | null = null;
    let tileView: View | null = null;
    const reduced = matchMedia("(prefers-reduced-motion: reduce)").matches;
    const towns = places();

    const size = () => {
      const dpr = Math.min(1.5, devicePixelRatio || 1);
      canvas.width = Math.round(innerWidth * dpr);
      canvas.height = Math.round(innerHeight * dpr);
      return dpr;
    };
    let dpr = size();

    const build = async () => {
      await Promise.race([Promise.all([document.fonts.load('15px "IM Fell English"'), document.fonts.load('italic 15px "IM Fell English"'), document.fonts.load('15px "Cinzel"')]), new Promise((r) => setTimeout(r, 1500))]);
      const land = await loadLand("110m");
      if (!alive) return;
      // one 360-degree tile, a little taller than the screen so it can breathe vertically
      const h = Math.round(canvas.height * 1.12);
      const w = Math.round(h * (360 / (LAT_TOP - LAT_BOTTOM)));
      const t = document.createElement("canvas");
      t.width = w;
      t.height = h;
      const v: View = { lon0: -180, lon1: 180, lat0: LAT_BOTTOM, lat1: LAT_TOP, x: 0, y: 0, w, h };
      const k = h / 900;
      drawMap(t.getContext("2d")!, v, { land, wrap: true, graticule: 15, rhumbs: WORLD_ROSES, labels: WORLD_LABELS, weight: Math.max(0.8, k * 1.4) });
      const tc = t.getContext("2d")!;
      for (const r of WORLD_ROSES) {
        const [x, y] = project(v, r);
        compassRose(tc, x, y, 46 * k);
      }
      // town marks: a ringed dot, filled red where a map is ready to unfold
      for (const p of towns) {
        const [x, y] = project(v, p.at);
        const ready = p.entries.some((e) => e.map.city);
        tc.lineWidth = 1.2 * k;
        tc.strokeStyle = "#3d2a1c";
        tc.fillStyle = "#f4e8c9";
        tc.beginPath();
        tc.arc(x, y, 4.2 * k, 0, Math.PI * 2);
        tc.fill();
        tc.stroke();
        tc.beginPath();
        tc.arc(x, y, 1.8 * k, 0, Math.PI * 2);
        tc.fillStyle = ready ? "#a65238" : "#3d2a1c";
        tc.fill();
      }
      tile = t;
      tileView = v;
    };
    void build();

    /* ---- drag: grab the chart, fling it; it eases back to its own pace ---- */
    const BASE = () => 14 * dpr * speedRef.current;
    let pan = 0;
    let vel = BASE();
    let drag: { x: number; last: number; t: number; moved: number } | null = null;

    const ships = LANES.map((l, i) => ({ ...l, u: (i * 0.37) % 1, dir: (i % 2 ? -1 : 1) as 1 | -1, s: 0.012 + (i % 3) * 0.004, sx: -999, sy: -999 }));
    const serp = { x: -999, y: -999, shown: false };
    const roses = WORLD_ROSES.map(() => ({ x: -999, y: -999 }));
    let roseSpin = 0;
    let rise = 0; // 0..1, the hovered drawing rising from the paper

    const toScreen = (p: LonLat, off = 0, y0 = 0): [number, number] => {
      const [x, y] = project(tileView!, p);
      return [x + pan + off, y + y0];
    };
    const wrapX = (x: number) => {
      const W = tile!.width;
      // the copy of x that is nearest the middle of the screen
      let best = x;
      for (const off of [-W, 0, W, 2 * W, -2 * W]) if (Math.abs(x + off - canvas.width / 2) < Math.abs(best - canvas.width / 2)) best = x + off;
      return best;
    };

    const pick = (px: number, py: number): Hover => {
      if (!tile || !tileView) return null;
      const x = px * dpr, y = py * dpr;
      const k = tile.height / 900;
      let best: { d: number; h: Hover } = { d: Infinity, h: null };
      const y0 = currentY0;
      for (const p of towns) {
        const [tx, ty] = toScreen(p.at, 0, y0);
        const d = Math.hypot(wrapX(tx) - x, ty - y);
        if (d < 15 * k * 1.2 && d < best.d) best = { d, h: { kind: "place", place: p } };
      }
      if (best.h) return best.h;
      for (const s of ships) {
        const d = Math.hypot(s.sx - x, s.sy - 10 * k - y);
        if (d < 26 * k && d < best.d) best = { d, h: { kind: "ship", caption: s.caption } };
      }
      if (serp.shown && Math.hypot(serp.x - x, serp.y - y) < 40 * k) return { kind: "serpent" };
      roses.forEach((r, i) => {
        const d = Math.hypot(r.x - x, r.y - y);
        if (d < 50 * k && d < best.d) best = { d, h: { kind: "rose", index: i } };
      });
      return best.h;
    };
    const sameHover = (a: Hover, b: Hover) =>
      a === b || (!!a && !!b && a.kind === b.kind && (a.kind !== "place" || a.place === (b as { place: Place }).place) && (a.kind !== "ship" || a.caption === (b as { caption: string }).caption) && (a.kind !== "rose" || a.index === (b as { index: number }).index));

    const onDown = (e: PointerEvent) => {
      canvas.setPointerCapture(e.pointerId);
      drag = { x: e.clientX, last: e.clientX, t: performance.now(), moved: 0 };
      canvas.style.cursor = "grabbing";
    };
    const onMove = (e: PointerEvent) => {
      // a mouse whose button is no longer down has let go (even if the release happened elsewhere)
      if (drag && e.pointerType === "mouse" && e.buttons === 0) onUp(e);
      if (drag) {
        const now = performance.now();
        const dx = e.clientX - drag.last;
        pan += dx * dpr;
        drag.moved += Math.abs(dx);
        const dt = Math.max(1, now - drag.t) / 1000;
        vel = vel * 0.6 + ((dx * dpr) / dt) * 0.4;
        drag.last = e.clientX;
        drag.t = now;
        if (drag.moved > 4 && hoverRef.current) setHover(null);
        return;
      }
      const h = pick(e.clientX, e.clientY);
      if (!sameHover(h, hoverRef.current)) {
        rise = 0;
        setHover(h);
      }
      canvas.style.cursor = h?.kind === "place" ? "pointer" : "grab";
    };
    const onUp = (e: PointerEvent) => {
      if (!drag) return;
      const click = drag.moved < 5;
      drag = null;
      canvas.style.cursor = "grab";
      if (performance.now() - (lastMoveAt || 0) > 80) vel = BASE(); // let go without a fling
      if (click) {
        const h = pick(e.clientX, e.clientY);
        if (h?.kind === "place") openPlace(h.place, e.clientX, e.clientY);
      }
    };
    let lastMoveAt = 0;
    const onMoveStamp = () => (lastMoveAt = performance.now());
    const onLeave = () => {
      if (!drag) setHover(null);
    };
    canvas.addEventListener("pointerdown", onDown);
    canvas.addEventListener("pointermove", onMove);
    canvas.addEventListener("pointermove", onMoveStamp);
    canvas.addEventListener("pointerup", onUp);
    canvas.addEventListener("pointercancel", onUp);
    canvas.addEventListener("pointerleave", onLeave);

    /** Put the cartouche over (x, y), kept inside the screen; its pointer still aims at the place. */
    const placePop = (x: number, y: number) => {
      const el = pop.current;
      const card = el?.firstElementChild as HTMLElement | null;
      if (!el || !card) return;
      const half = card.offsetWidth / 2, h = card.offsetHeight;
      const cx = Math.max(half + 10, Math.min(innerWidth - half - 10, x));
      const below = y - h - 12 < 8;
      el.style.transform = `translate3d(${Math.round(x)}px, ${Math.round(below ? y + 70 : y)}px, 0)`;
      el.style.setProperty("--shift", `${Math.round(cx - x)}px`);
      el.classList.toggle("is-below", below);
      el.style.visibility = "visible";
    };
    let last = performance.now();
    let currentY0 = 0;
    const frame = (now: number) => {
      raf = requestAnimationFrame(frame);
      const dt = Math.min(0.05, (now - last) / 1000);
      last = now;
      if (!tile || !tileView) {
        ctx.fillStyle = "#e9dbb8";
        ctx.fillRect(0, 0, canvas.width, canvas.height);
        return;
      }
      const W = tile.width, H = tile.height;
      const k = H / 900;
      // drift: while held, the hand moves it; after a fling it eases back to its own pace
      if (!drag) {
        const base = reduced ? 0 : BASE();
        vel += (base - vel) * (1 - Math.exp(-2.2 * dt));
        // pause the drift under the pointer when it rests on something, so the drawing can be read
        const hold = hoverRef.current && Math.abs(vel - base) < base * 0.3 ? 0.08 : 1;
        pan += vel * dt * hold;
      }
      pan = ((pan % W) + W) % W;
      const y0 = -(H - canvas.height) / 2 + Math.sin(now / 9000) * (H - canvas.height) * 0.3;
      currentY0 = y0;
      for (let x = pan - W; x < canvas.width; x += W) ctx.drawImage(tile, Math.round(x), Math.round(y0));

      // ships
      for (const sh of ships) {
        if (!reduced) {
          sh.u += sh.dir * sh.s * dt;
          if (sh.u > 1 || sh.u < 0) {
            sh.dir = -sh.dir as 1 | -1;
            sh.u = Math.max(0, Math.min(1, sh.u));
          }
        }
        const [a, b] = sh.lane;
        const p: LonLat = [a[0] + (b[0] - a[0]) * sh.u, a[1] + (b[1] - a[1]) * sh.u];
        const east = (b[0] - a[0]) * sh.dir > 0 ? 1 : -1;
        const [x0, y] = toScreen(p, 0, y0);
        const x = wrapX(x0);
        sh.sx = x;
        sh.sy = y;
        const lit = hoverRef.current?.kind === "ship" && hoverRef.current.caption === sh.caption;
        for (const off of [-W, 0, W]) {
          if (x + off < -60 || x + off > canvas.width + 60) continue;
          ship(ctx, x + off, y + Math.sin(now / 700 + sh.s * 900) * 1.5 * k, (lit ? 1.7 : 1.25) * k, Math.sin(now / (lit ? 400 : 900) + sh.u * 9) * (lit ? 0.12 : 0.05), east);
        }
      }
      // the serpent of the southern ocean, surfacing now and then (and staying up while you look at it)
      const phase = (now / 1000) % 24;
      const lookingAtSerpent = hoverRef.current?.kind === "serpent";
      serp.shown = phase < 10 || lookingAtSerpent;
      if (serp.shown) {
        const [x0, y] = toScreen([60, -44], 0, y0);
        const x = wrapX(x0);
        serp.x = x;
        serp.y = y;
        ctx.globalAlpha = lookingAtSerpent ? 1 : Math.min(1, phase / 1.5, (10 - phase) / 1.5);
        serpent(ctx, x, y, (lookingAtSerpent ? 2.1 : 1.6) * k, now / (lookingAtSerpent ? 500 : 1000));
        ctx.globalAlpha = 1;
      }
      // roses: the hovered one spins
      roseSpin += dt * (hoverRef.current?.kind === "rose" ? 1.4 : 0);
      WORLD_ROSES.forEach((r, i) => {
        const [x0, y] = toScreen(r, 0, y0);
        const x = wrapX(x0);
        roses[i].x = x;
        roses[i].y = y;
        if (hoverRef.current?.kind === "rose" && hoverRef.current.index === i) {
          ctx.fillStyle = "#e9dbb8";
          ctx.beginPath();
          ctx.arc(x, y, 50 * k, 0, Math.PI * 2);
          ctx.fill();
          compassRose(ctx, x, y, 46 * k * 1.08, roseSpin);
        }
      });
      // the hovered place: its atlas's region washed in colour, and its drawing rising from the paper
      const hv = hoverRef.current;
      if (hv?.kind === "place") {
        rise = Math.min(1, rise + dt * 3.2);
        const e = 1 - Math.pow(1 - rise, 3);
        for (const en of hv.place.entries.slice(0, 1)) {
          ctx.save();
          ctx.beginPath();
          en.atlas.area.forEach((pt, i) => {
            const [ax, ay] = toScreen(pt, 0, y0);
            const xx = wrapX(ax);
            if (i) ctx.lineTo(xx, ay);
            else ctx.moveTo(xx, ay);
          });
          ctx.closePath();
          ctx.fillStyle = hexA(en.atlas.color, 0.18 * e);
          ctx.fill();
          ctx.setLineDash([6 * k, 4 * k]);
          ctx.strokeStyle = hexA(en.atlas.color, 0.8 * e);
          ctx.lineWidth = 1.8 * k;
          ctx.stroke();
          ctx.restore();
        }
        const [px0, py] = toScreen(hv.place.at, 0, y0);
        const px = wrapX(px0);
        ctx.beginPath();
        ctx.ellipse(px, py, 18 * k * e, 5 * k * e, 0, 0, Math.PI * 2);
        ctx.fillStyle = "rgba(74,51,34,0.18)";
        ctx.fill();
        drawGlyph(ctx, hv.place.glyph, px, py - 2 * k, 34 * k * (0.3 + 0.7 * e));
        // the cartouche follows its place (in CSS pixels)
        placePop(px / dpr, (py - 44 * k) / dpr);
      } else if (hv && pop.current) {
        const at = hv.kind === "ship" ? ships.find((s) => s.caption === hv.caption)! : hv.kind === "serpent" ? { sx: serp.x, sy: serp.y } : { sx: roses[hv.index].x, sy: roses[hv.index].y };
        const ax = "sx" in at ? at.sx : 0, ay = "sy" in at ? at.sy : 0;
        placePop(ax / dpr, (ay - (hv.kind === "rose" ? 56 : 30) * k) / dpr);
      }
    };
    raf = requestAnimationFrame(frame);
    // dev probe: where a town is on screen right now (CSS pixels), for scripted checks
    if (import.meta.env.DEV)
      (window as unknown as { __townAt: unknown }).__townAt = (title: string) => {
        const p = towns.find((t) => t.title === title);
        if (!p || !tileView) return null;
        const [x, y] = toScreen(p.at, 0, currentY0);
        return [Math.round(wrapX(x) / dpr), Math.round(y / dpr)];
      };
    const onResize = () => {
      dpr = size();
      tile = null;
      void build();
    };
    addEventListener("resize", onResize);
    return () => {
      alive = false;
      cancelAnimationFrame(raf);
      removeEventListener("resize", onResize);
      canvas.removeEventListener("pointerdown", onDown);
      canvas.removeEventListener("pointermove", onMove);
      canvas.removeEventListener("pointermove", onMoveStamp);
      canvas.removeEventListener("pointerup", onUp);
      canvas.removeEventListener("pointercancel", onUp);
      canvas.removeEventListener("pointerleave", onLeave);
    };
  }, []);

  return (
    <>
      <canvas ref={ref} className="world-drift" aria-label="A world chart: drag to turn it, point at a town to see what is there" />
      {hover && (
        <div className="world-pop" ref={pop} aria-live="polite">
          <div className={`world-pop__card world-pop__card--${hover.kind}`}>
            {hover.kind === "place" ? <PlaceCard place={hover.place} /> : <p>{hover.kind === "ship" ? hover.caption : hover.kind === "serpent" ? SERPENT_CAPTION : ROSE_CAPTION}</p>}
          </div>
        </div>
      )}
    </>
  );
}

function PlaceCard({ place }: { place: Place }) {
  const ready = place.entries.filter((e) => e.map.city);
  return (
    <>
      <img className="world-pop__glyph" src={glyphImage(place.glyph)} alt="" />
      <div className="world-pop__text">
        <strong>{place.title}</strong>
        {place.entries.map((e) => (
          <span key={e.atlas.id} className="world-pop__line">
            <em style={{ color: e.atlas.color }}>{e.atlas.title}</em> · {e.map.subtitle}
          </span>
        ))}
        <span className={`world-pop__status ${ready.length ? "is-ready" : ""}`}>{ready.length ? "Click to unfold the map" : "In preparation · click to open its atlas"}</span>
      </div>
    </>
  );
}

function openPlace(place: Place, x: number, y: number) {
  const ready = place.entries.find((e) => e.map.city);
  if (ready) useNav.getState().openMap(ready.atlas.id, ready.map, { x: x - 40, y: y - 50, w: 80, h: 100 });
  else useNav.getState().goRoom(place.entries[0].atlas.id);
}
