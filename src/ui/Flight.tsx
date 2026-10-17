import { useEffect, useRef, useState } from "react";
import { useNav, type Flight as FlightT } from "@/nav";

/**
 * A map between the shelf and the screen. Unfold: the folded packet flies
 * from where it was clicked to the middle of the screen, opens along its
 * horizontal fold, then its accordion folds one by one, and the sheet grows
 * to fill the screen; it waits there until the live city has painted its
 * first plate, then fades away into it. Fold is the same, backwards, ending
 * in the atlas card it came from.
 *
 * The sheet is 4 x 2 panels built as nested 3D-transformed elements, each
 * showing its slice of the map on the front and plain paper on the back.
 */
const COLS = 4, ROWS = 2;

const clamp01 = (x: number) => Math.max(0, Math.min(1, x));
const ease = (x: number) => (x < 0.5 ? 4 * x * x * x : 1 - Math.pow(-2 * x + 2, 3) / 2);
const span = (t: number, a: number, b: number) => ease(clamp01((t - a) / (b - a)));

export function Flight({ flight }: { flight: FlightT }) {
  const [aspect, setAspect] = useState<number | null>(null);
  useEffect(() => {
    const img = new Image();
    img.onload = () => setAspect(img.naturalWidth / img.naturalHeight || 1.1);
    img.onerror = () => setAspect(1.1);
    img.src = flight.image;
  }, [flight.image]);
  if (!aspect) return <div className="flight flight--wait" />;
  return <Sheet flight={flight} aspect={aspect} />;
}

function Sheet({ flight, aspect }: { flight: FlightT; aspect: number }) {
  const root = useRef<HTMLDivElement>(null);
  const sheet = useRef<HTMLDivElement>(null);
  const bottom = useRef<HTMLDivElement>(null);
  const hinges = useRef<(HTMLDivElement | null)[]>([]);
  const shade = useRef<HTMLDivElement>(null);
  const reduced = typeof matchMedia !== "undefined" && matchMedia("(prefers-reduced-motion: reduce)").matches;

  // the sheet at "natural" size: as large as fits comfortably
  const vw = innerWidth, vh = innerHeight;
  const H = Math.min(vh * 0.78, (vw * 0.84) / aspect);
  const W = H * aspect;
  const pw = W / COLS, ph = H / ROWS;

  useEffect(() => {
    let raf = 0;
    let ready = flight.kind === "fold";
    let readyAt = 0;
    let covered = false;
    let coveredAt = Infinity;
    const onPlate = (e: Event) => {
      const d = (e as CustomEvent).detail as { city: string };
      if (d.city === flight.map.city) ready = true;
    };
    addEventListener("chronoscape:plate", onPlate);
    const unfold = flight.kind === "unfold";
    // the folded packet's screen box at the start (unfold) or the end (fold)
    // when folding, the atlas card (and its slot) may still be loading: keep looking for it
    const slot = () => {
      if (unfold || !flight.atlasId) return null;
      const el = document.querySelector<HTMLElement>(`[data-map-slot="${CSS.escape(`${flight.atlasId}:${flight.map.title}`)}"]`);
      if (!el) return null;
      const r = el.getBoundingClientRect();
      return r.width > 0 ? { x: r.x, y: r.y, w: r.width, h: r.height } : null;
    };
    let target = flight.rect ?? slot() ?? { x: vw / 2 - 60, y: vh / 2 - 70, w: 120, h: 120 / (pw / ph) };
    let found = !!flight.rect || !!slot();
    const fill = Math.max(vw / W, vh / H) * 1.03;
    const T = reduced ? { fly: 0.01, rows: 0.02, cols: 0.03, fill: 0.04 } : { fly: 0.6, rows: 1.1, cols: 1.95, fill: 2.6 };
    const t0 = performance.now();
    const frame = (now: number) => {
      raf = requestAnimationFrame(frame);
      if (!found) {
        const r = slot();
        if (r) {
          target = r;
          found = true;
        }
      }
      let t = (now - t0) / 1000;
      // fold plays the same timeline backwards, starting from the filled screen
      if (!unfold) t = Math.max(0, T.fill - t * 1.15);
      const fly = span(t, 0, T.fly);
      const rows = span(t, T.fly, T.rows);
      const cols = [span(t, T.rows - 0.05, T.rows + 0.45), span(t, T.rows + 0.15, T.rows + 0.65), span(t, T.rows + 0.3, T.cols)];
      const grow = span(t, T.cols + 0.05, T.fill);
      // how much of the sheet is open decides where its visible middle is
      const openW = pw * (1 + cols[0] + cols[1] + cols[2]);
      const openH = ph * (1 + rows);
      // scale: from the packet's size, to natural, to filling the screen
      const s0 = target.w / pw;
      const s = (s0 + (1 - s0) * fly) * (1 + (fill - 1) * grow);
      const startCx = target.x + target.w / 2, startCy = target.y + target.h / 2;
      const cx = startCx + (vw / 2 - startCx) * fly, cy = startCy + (vh / 2 - startCy) * fly;
      const tx = cx - (openW / 2) * s, ty = cy - (openH / 2) * s;
      const tilt = (1 - fly) * 8 + Math.sin(fly * Math.PI) * -6;
      sheet.current!.style.transform = `translate3d(${tx}px, ${ty}px, 0) scale(${s}) rotateZ(${(1 - fly) * -4}deg) rotateX(${tilt * (1 - grow)}deg)`;
      bottom.current!.style.transform = `rotateX(${-179.4 * (1 - rows)}deg)`;
      hinges.current.forEach((h, i) => {
        if (!h) return;
        const col = (i % (COLS - 1));
        const sign = col % 2 === 0 ? 1 : -1;
        h.style.transform = `rotateY(${sign * 179.4 * (1 - cols[col])}deg)`;
      });
      shade.current!.style.opacity = String(0.55 * (1 - grow));
      root.current!.style.setProperty("--fold-shade", String(1 - grow));
      // the map covers the screen: the room behind can give way to the city
      if (unfold && grow > 0.97 && !covered) {
        covered = true;
        coveredAt = now;
        dispatchEvent(new CustomEvent("chronoscape:covered"));
      }
      // unfold: hold the filled screen until the city has painted, then fade into it
      if (unfold && t >= T.fill) {
        // (the plate may have been painted before this listener existed: check the last one too)
        const last = (window as unknown as { __lastPlate?: { city: string; t: number } }).__lastPlate;
        if (!ready && last && last.city === flight.map.city && last.t >= coveredAt) ready = true;
        if (ready && !readyAt) readyAt = now;
        const waited = (now - t0) / 1000 - T.fill;
        if (!readyAt && waited > 6) readyAt = now; // never wait forever
        if (readyAt) {
          const f = clamp01((now - readyAt) / 450);
          root.current!.style.opacity = String(1 - f);
          if (f >= 1) {
            cancelAnimationFrame(raf);
            useNav.getState().landed();
          }
        }
      }
      if (!unfold) {
        // fold: fade in fast over the city, finish small and fade at the target
        const elapsed = (now - t0) / 1000;
        root.current!.style.opacity = String(Math.min(1, elapsed / 0.15) * (t > 0.05 ? 1 : clamp01(1 - (elapsed - T.fill / 1.15) / 0.3)));
        if (elapsed > T.fill / 1.15 + 0.35) {
          cancelAnimationFrame(raf);
          useNav.getState().landed();
        }
      }
    };
    raf = requestAnimationFrame(frame);
    return () => {
      cancelAnimationFrame(raf);
      removeEventListener("chronoscape:plate", onPlate);
    };
  }, [flight, W, H, pw, ph, reduced, vw, vh]);

  const panelStyle = (c: number, r: number) => ({
    width: pw,
    height: ph,
    backgroundImage: `url("${flight.image}")`,
    backgroundSize: `${W}px ${H}px`,
    backgroundPosition: `${-c * pw}px ${-r * ph}px`,
  });
  // a chain of panels: each hinge holds the next panel on its left edge
  const row = (r: number) => {
    let inner: React.ReactElement | null = null;
    for (let c = COLS - 1; c >= 0; c--) {
      const idx = r * (COLS - 1) + (c - 1);
      const panel = (
        <div className="flight__panel" style={{ width: pw, height: ph }}>
          <div className="flight__front" style={panelStyle(c, r)} />
          <div className="flight__back">{r === 1 && c === 0 && <Cover title={flight.map.title} subtitle={flight.map.subtitle} />}</div>
          <div className="flight__crease" />
          {inner}
        </div>
      );
      inner =
        c === 0 ? (
          panel
        ) : (
          <div className="flight__hinge" style={{ left: pw, width: pw, height: ph }} ref={(el) => {
              hinges.current[idx] = el;
            }}>
            {panel}
          </div>
        );
    }
    return inner;
  };
  return (
    <div className="flight" ref={root} aria-hidden="true">
      <div className="flight__shade" ref={shade} />
      <div className="flight__sheet" ref={sheet} style={{ width: W, height: H }}>
        <div className="flight__row" style={{ top: 0 }}>
          {row(0)}
        </div>
        <div className="flight__row flight__row--bottom" ref={bottom} style={{ top: ph, transformOrigin: "50% 0" }}>
          {row(1)}
        </div>
      </div>
    </div>
  );
}

/** The outside of the folded packet: what you see before it opens. */
function Cover({ title, subtitle }: { title: string; subtitle: string }) {
  return (
    <div className="flight__cover">
      <div className="flight__cover-k">Chronoscape</div>
      <div className="flight__cover-t">{title}</div>
      <div className="flight__cover-s">{subtitle}</div>
    </div>
  );
}
