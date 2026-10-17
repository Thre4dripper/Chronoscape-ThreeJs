import { useEffect, useMemo, useState } from "react";

/**
 * "The procession of the ages": travellers from every atlas on the shelf
 * walking across the foot of the title page. Cartoon figures rendered in
 * Blender as walk-cycle sprite sheets (assets/title/procession). Everyone
 * walks at one pace on one loop, spaced by their own width, so nobody ever
 * walks into anybody.
 */
type Figure = { id: string; label: string; era: string; src: string; frames: number; w: number; h: number; fps?: number };
type Manifest = { figures: Figure[]; scale?: number };

const SPEED = 30; // px per second
const GAP = 36;

export function Procession() {
  const [m, setM] = useState<Manifest | null>(null);
  const [width, setWidth] = useState(() => innerWidth);
  useEffect(() => {
    let alive = true;
    fetch("/title/procession/manifest.json")
      .then((r) => (r.ok ? r.json() : null))
      .then((j) => alive && setM(j))
      .catch(() => undefined);
    const onResize = () => setWidth(innerWidth);
    addEventListener("resize", onResize);
    return () => {
      alive = false;
      removeEventListener("resize", onResize);
    };
  }, []);
  const layout = useMemo(() => {
    if (!m) return null;
    // every figure fits the band whole: the tallest (a spear, a camel's head) sets the scale
    const band = innerHeight < 760 ? 118 : 146;
    const tallest = Math.max(...m.figures.map((f) => f.h));
    const scale = Math.min((m.scale ?? 1) * (innerHeight < 760 ? 0.8 : 1), band / tallest);
    const figs = m.figures.map((f) => ({ ...f, dw: f.w * scale, dh: f.h * scale }));
    const maxW = Math.max(...figs.map((f) => f.dw));
    // the loop must be longer than the screen plus one figure, and long enough for everyone
    const sum = figs.reduce((a, f) => a + f.dw + GAP, 0);
    const track = Math.max(width + maxW * 2, sum);
    // each walker keeps its own width plus a gap behind the one in front (offsets grow leftwards)
    const extra = Math.max(0, (track - sum) / figs.length);
    let off = 0;
    const placed = figs.map((f) => {
      off += f.dw + GAP + extra;
      return { ...f, offset: off };
    });
    return { placed, track, maxW, period: track / SPEED };
  }, [m, width]);
  if (!layout) return <div className="procession procession--empty" aria-hidden="true" />;
  return (
    <div className="procession" aria-label="A procession of travellers from the ages on the shelf">
      <div className="procession__ground" aria-hidden="true" />
      {layout.placed.map((f) => (
        <div
          key={f.id}
          className="procession__walker"
          style={
            {
              width: f.dw,
              height: f.dh,
              "--from": `${-layout.maxW}px`,
              "--to": `${layout.track - layout.maxW}px`,
              animationDuration: `${layout.period}s`,
              animationDelay: `${-(layout.track - f.offset) / SPEED}s`,
            } as React.CSSProperties
          }
        >
          <div
            className="procession__sprite"
            role="img"
            aria-label={`${f.label}, ${f.era}`}
            style={
              {
                backgroundImage: `url("/title/procession/${f.src}")`,
                backgroundSize: `${f.dw * f.frames}px ${f.dh}px`,
                "--steps": f.frames,
                "--sheet": `${-f.dw * f.frames}px`,
                animationDuration: `${f.frames / (f.fps ?? 9)}s`,
              } as React.CSSProperties
            }
          />
          <span className="procession__tag">
            {f.label}
            <em>{f.era}</em>
          </span>
        </div>
      ))}
    </div>
  );
}
