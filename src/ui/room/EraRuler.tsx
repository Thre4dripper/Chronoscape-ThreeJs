import { useEffect, useMemo, useState } from "react";
import type { Atlas } from "@/content/schema";
import { useNav } from "@/nav";
import { useRoom } from "./roomState";

/**
 * The ages at a glance: a ruler from 3000 BCE to 1900 CE with every atlas's
 * span as a ribbon. Ribbons never overlap: each takes the first free lane.
 * Hovering a ribbon is the same as hovering its atlas on the shelf.
 */
const T0 = -3000, T1 = 1900, KNEE = -1000, KNEE_U = 0.14;
/** Early millennia are compressed: most of the shelf is after 1000 BCE. */
export const yearU = (y: number) => (y < KNEE ? (KNEE_U * (y - T0)) / (KNEE - T0) : KNEE_U + ((1 - KNEE_U) * (y - KNEE)) / (T1 - KNEE));
const TICKS = [-3000, -2000, -1000, -500, 1, 500, 1000, 1500, 1900];
const fmt = (y: number) => (y < 0 ? `${-y} BCE` : y === 1 ? "1 CE" : `${y}`);

export function EraRuler({ atlases }: { atlases: Atlas[] }) {
  const hoverId = useRoom((s) => s.hoverId);
  // year labels never overlap: drop the ones that would sit too close to the last one shown
  const [width, setWidth] = useState(() => innerWidth);
  useEffect(() => {
    const on = () => setWidth(innerWidth);
    addEventListener("resize", on);
    return () => removeEventListener("resize", on);
  }, []);
  const ticks = useMemo(() => {
    const px = width - 80;
    const out: number[] = [];
    for (const t of TICKS) {
      const w = fmt(t).length * 7 + 14;
      if (!out.length || (yearU(t) - yearU(out[out.length - 1])) * px >= w) out.push(t);
    }
    // always keep the last year, replacing its neighbour if needed
    const last = TICKS[TICKS.length - 1];
    if (out[out.length - 1] !== last) out[out.length - 1] = last;
    return out;
  }, [width]);
  const openId = useNav((s) => s.atlasId);
  const lanes = useMemo(() => {
    const ends: number[] = [];
    const out = new Map<string, number>();
    for (const a of [...atlases].sort((x, y) => x.from - y.from)) {
      const u0 = yearU(a.from);
      let lane = ends.findIndex((e) => e + 0.012 < u0);
      if (lane < 0) lane = ends.length;
      ends[lane] = yearU(a.to);
      out.set(a.id, lane);
    }
    return { of: out, count: ends.length };
  }, [atlases]);
  return (
    <section className="ruler" data-hud-block aria-label="The ages on the shelf">
      <div className="ruler__lanes" style={{ height: lanes.count * 13 + 6 }}>
        {atlases.map((a) => {
          const u0 = yearU(a.from), u1 = yearU(a.to);
          const lit = a.id === hoverId || a.id === openId;
          return (
            <button
              key={a.id}
              className={`ruler__bar ${lit ? "is-lit" : ""}`}
              style={{ left: `${u0 * 100}%`, width: `${(u1 - u0) * 100}%`, top: lanes.of.get(a.id)! * 13 + 3, background: a.color }}
              onPointerEnter={() => !openId && useRoom.getState().setHover(a.id)}
              onPointerLeave={() => useRoom.getState().hoverId === a.id && useRoom.getState().setHover(null)}
              onClick={() => useNav.getState().openAtlas(a.id)}
              title={`${a.title}, ${a.era}`}
              aria-label={`${a.title}, ${a.era}`}
            >
              <span>{a.title}</span>
            </button>
          );
        })}
      </div>
      <div className="ruler__axis">
        {ticks.map((t) => (
          <span key={t} style={{ left: `${yearU(t) * 100}%` }}>
            {fmt(t)}
          </span>
        ))}
      </div>
    </section>
  );
}
