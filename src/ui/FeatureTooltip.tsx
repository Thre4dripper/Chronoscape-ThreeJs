import { useEffect, useRef } from "react";
import type { City } from "@/content/schema";
import { useStore, spotById, vignetteAt, resolveSpot } from "@/engine/store";
import { getFabric } from "@/engine/map/fabric";
import { describeBlock, describeField, gardenText } from "@/engine/map/blockInfo";
import { pointInPolygon } from "@/engine/map/geom";

/** Follows the pointer; names whatever map feature is under it. */
export function FeatureTooltip({ city }: { city: City }) {
  const wrap = useRef<HTMLDivElement>(null);
  useEffect(() => {
    // panels the tooltip must not cover (re-measured a few times a second)
    let blocks: DOMRect[] = [];
    let measured = 0;
    const onMove = (e: PointerEvent) => {
      const el = wrap.current;
      if (!el) return;
      const now = performance.now();
      if (now - measured > 300) {
        measured = now;
        blocks = [...document.querySelectorAll<HTMLElement>("aside, [data-hud-block]")].map((b) => b.getBoundingClientRect());
      }
      const W = 330, H = Math.max(80, (el.firstElementChild as HTMLElement | null)?.offsetHeight ?? 160);
      const fits = (x: number, y: number) => !blocks.some((r) => x < r.right && x + W > r.left && y < r.bottom && y + H > r.top);
      const cands: [number, number][] = [
        [e.clientX + 18, e.clientY + 18],
        [e.clientX - W - 18, e.clientY + 18],
        [e.clientX + 18, e.clientY - H - 18],
        [e.clientX - W - 18, e.clientY - H - 18],
      ].map(([x, y]) => [Math.max(8, Math.min(x, window.innerWidth - W - 8)), Math.max(8, Math.min(y, window.innerHeight - H - 8))]);
      const spot = cands.find(([cx, cy]) => fits(cx, cy));
      const [x, y] = spot ?? cands[0];
      el.style.transform = `translate3d(${x}px, ${y}px, 0)`;
      // over a panel, the notebook or the timeline: the map's tooltip has nothing to say
      const over = (e.target as Element | null)?.closest?.("aside, [data-hud-block], .hud, .timeline, .daydial, .story, .lightbox");
      el.style.visibility = over || !spot ? "hidden" : "";
    };
    window.addEventListener("pointermove", onMove, { passive: true });
    return () => window.removeEventListener("pointermove", onMove);
  }, []);
  return (
    <div ref={wrap} className="tooltip-anchor">
      <TooltipBody city={city} />
    </div>
  );
}

function TooltipBody({ city }: { city: City }) {
  const feature = useStore((s) => s.hoveredFeature);
  const blockId = useStore((s) => s.hoveredBlockId);
  const area = useStore((s) => s.hoveredArea);
  const hour = useStore((s) => s.hour);
  const periodId = useStore((s) => s.periodId);
  const focusedEventId = useStore((s) => s.focusedEventId);
  const focusedSpotId = useStore((s) => s.focusedSpotId);
  // an ordinary city block wins over the broad district / road it sits in, but not over markers
  if (blockId !== null && periodId && (!feature || (feature.kind !== "spot" && feature.kind !== "event"))) {
    const fabric = getFabric(city, periodId);
    const b = fabric.insulae[blockId];
    if (b) {
      const info = describeBlock(fabric.style, b, fabric.lots, city.periods.find((p) => p.id === periodId));
      const district = city.map.districts.find((d) => (!d.periods || d.periods.includes(periodId)) && pointInPolygon(b.x, b.y, d.polygon));
      return (
        <div className="tooltip tooltip--block" >
          <div className="tooltip__kind">{district ? district.name : "City block"}</div>
          <div className="tooltip__name">{info.title}</div>
          <div className="tooltip__blurb">{info.text}</div>
          <div className="tooltip__hint">{info.facts}</div>
        </div>
      );
    }
  }
  if (area && periodId && (!feature || feature.kind === "district" || feature.kind === "hill")) {
    const fabric = getFabric(city, periodId);
    const info =
      area.kind === "park"
        ? { title: area.name ?? "Garden", text: gardenText(fabric.style) }
        : area.kind === "marsh"
          ? { title: area.name ?? "Marsh", text: "Low wet ground where streams pooled before the valleys were drained: reeds, frogs and fever. Fishermen and reed-cutters worked it." }
          : describeField(fabric.style, area.kind as "furrow" | "pasture" | "vineyard" | "orchard");
    return (
      <div className="tooltip tooltip--field" >
        <div className="tooltip__kind">{area.kind === "park" ? "Gardens" : area.kind === "marsh" ? "Wetland" : "Countryside"}</div>
        <div className="tooltip__name">{area.name && area.kind !== "park" && area.kind !== "marsh" ? `${info.title} · ${area.name}` : info.title}</div>
        <div className="tooltip__blurb">{info.text}</div>
      </div>
    );
  }
  if (!feature) return null;
  // the marker that was just clicked: its details are in the panel now, not in a tooltip on top of it
  if ((feature.kind === "event" && feature.id === focusedEventId) || (feature.kind === "spot" && feature.id === focusedSpotId)) return null;
  const spot = feature.kind === "spot" ? spotById(city, feature.id) : null;
  const vignette = spot ? vignetteAt(spot, hour) : null;
  return (
    <div className={`tooltip tooltip--${feature.kind}`}>
      <div className="tooltip__kind">{spot ? spot.kind : feature.kind === "object" ? "On the table" : feature.kind}</div>
      <div className="tooltip__name">{spot ? resolveSpot(spot, periodId).name : feature.name}</div>
      {vignette ? (
        <div className="tooltip__blurb">
          <span className="tooltip__hour">{String(vignette.hour).padStart(2, "0")}:00</span> {vignette.text}
        </div>
      ) : feature.blurb ? (
        <div className="tooltip__blurb">{feature.blurb}</div>
      ) : null}
      {spot && <div className="tooltip__hint">Click to visit</div>}
      {feature.hint && <div className="tooltip__hint">{feature.hint}</div>}
      {feature.kind === "district" && <div className="tooltip__hint">Its shops and workshops are shown while you hover</div>}
    </div>
  );
}
