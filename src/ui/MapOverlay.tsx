import { useLayoutEffect, useRef } from "react";
import * as THREE from "three";
import type { City } from "@/content/schema";
import { frameOf, mapToWorld } from "@/engine/coords";
import { useStore, resolveVariant, resolveSpot, eventPlace } from "@/engine/store";
import { overlay } from "@/engine/overlay/registry";
import { SpotIcon } from "@/engine/spots/icons";
import { pointInPolygon } from "@/engine/map/geom";

const KIND_GLYPH: Record<string, string> = { construction: "⚒", festival: "♪", procession: "⚜", riot: "✦", disaster: "✶", civic: "§", ceremony: "✠", daily: "☉" };

type Item = { id: string; pos: [number, number, number]; priority: number; force: boolean; candidate: boolean; offsetY: number; node: React.ReactNode; className: string };

/**
 * Landmark names, places of daily life and events, as one decluttered DOM
 * layer over the canvas. Rendering decides *what could* show; the projector
 * decides *what fits*.
 */
export function MapOverlay({ city }: { city: City }) {
  const f = frameOf(city);
  const periodId = useStore((s) => s.periodId);
  const zoom = useStore((s) => s.zoomLevel);
  const hoveredId = useStore((s) => s.hoveredId);
  const focusedId = useStore((s) => s.focusedId);
  const focusedSpotId = useStore((s) => s.focusedSpotId);
  const focusedEventId = useStore((s) => s.focusedEventId);
  const hoveredDistrictId = useStore((s) => s.hoveredDistrictId);
  // only spot / event hover matters here: a stable string, so crossing roads and districts doesn't re-render the overlay
  const litMarker = useStore((s) => (s.hoveredFeature && (s.hoveredFeature.kind === "spot" || s.hoveredFeature.kind === "event") ? `${s.hoveredFeature.kind}:${s.hoveredFeature.id}` : null));
  const storyId = useStore((s) => s.storyId);
  const { hover, focus, focusSpot, focusEvent, hoverFeature } = useStore.getState();
  const district = hoveredDistrictId ? city.map.districts.find((d) => d.id === hoveredDistrictId) : null;

  const items: Item[] = [];
  for (const l of city.landmarks) {
    const active = !!periodId && l.activePeriods.includes(periodId);
    const lit = hoveredId === l.id || focusedId === l.id;
    const size = Math.max(l.footprint[0], l.footprint[1]) * l.scale;
    const [x, , z] = mapToWorld(f, l.position);
    const raised = lit;
    const y = raised ? Math.min(45, 10 + size * 0.12) * f.scale * Math.max(1, l.scale * 0.7) : 0.01;
    items.push({
      id: `lm:${l.id}`,
      pos: [x, y, z],
      priority: 30 + Math.min(20, size / 25),
      force: lit,
      candidate: active && (lit || zoom !== "city" || size >= 70),
      offsetY: raised ? 10 : 0,
      className: `landmark-label ${lit ? "is-lit" : ""} ${zoom === "city" && !lit ? "is-far" : ""}`,
      node: (
        <span
          onPointerEnter={() => hover(l.id)}
          onPointerLeave={() => useStore.getState().hoveredId === l.id && hover(null)}
          onClick={(e) => {
            e.stopPropagation();
            focus(l.id);
          }}
        >
          {resolveVariant(l, periodId).name}
        </span>
      ),
    });
  }
  for (const sp of city.spots) {
    const active = !!periodId && sp.activePeriods.includes(periodId);
    const inDistrict = !!district && pointInPolygon(sp.position[0], sp.position[1], district.polygon);
    const lit = focusedSpotId === sp.id || litMarker === `spot:${sp.id}`;
    const [x, , z] = mapToWorld(f, sp.position);
    const name = resolveSpot(sp, periodId).name;
    items.push({
      id: `sp:${sp.id}`,
      pos: [x, 0.02, z],
      priority: inDistrict ? 45 : 20,
      force: lit,
      candidate: active && !storyId && (zoom !== "city" || inDistrict || lit),
      offsetY: 0,
      className: `spot spot--${sp.kind} ${lit ? "is-lit" : ""}`,
      node: (
        <button
          aria-label={name}
          onPointerEnter={() => hoverFeature({ kind: "spot", id: sp.id, name, blurb: sp.summary })}
          onPointerLeave={() => hoverFeature(null)}
          onClick={(e) => {
            e.stopPropagation();
            focusSpot(sp.id);
          }}
        >
          <SpotIcon kind={sp.kind} />
        </button>
      ),
    });
  }
  for (const e of city.events) {
    const pl = eventPlace(city, e);
    const [x, , z] = mapToWorld(f, pl.position);
    const lit = focusedEventId === e.id || litMarker === `event:${e.id}`;
    items.push({
      id: `ev:${e.id}`,
      pos: [x, 4 * f.scale, z],
      priority: 55,
      force: lit,
      candidate: e.periodId === periodId && !storyId,
      offsetY: 26,
      className: `event-marker event-marker--${e.kind} ${lit ? "is-lit" : ""}`,
      node: (
        <button
          title={e.title}
          onPointerEnter={() => hoverFeature({ kind: "event", id: e.id, name: e.title, blurb: e.date })}
          onPointerLeave={() => hoverFeature(null)}
          onClick={(ev) => {
            ev.stopPropagation();
            focusEvent(e.id);
          }}
        >
          <span className="event-marker__glyph">{KIND_GLYPH[e.kind] ?? "•"}</span>
          <span className="event-marker__label">{e.title}</span>
        </button>
      ),
    });
  }

  const refs = useRef(new Map<string, HTMLDivElement>());
  useLayoutEffect(() => {
    const seen = new Set<string>();
    for (const it of items) {
      const el = refs.current.get(it.id);
      if (!el) continue;
      seen.add(it.id);
      let e = overlay.entries.get(it.id);
      if (!e) {
        e = { el, pos: new THREE.Vector3(), priority: 0, force: false, candidate: false, offsetY: 0, w: 0, h: 0, shown: false };
        overlay.entries.set(it.id, e);
      }
      e.el = el;
      e.pos.set(...it.pos);
      e.priority = it.priority;
      e.force = it.force;
      e.candidate = it.candidate;
      e.offsetY = it.offsetY;
      // measure lazily (in the projector) and only when the element's look changed
      if (el.dataset.cls !== it.className) {
        el.dataset.cls = it.className;
        e.w = 0;
      }
    }
    for (const id of [...overlay.entries.keys()]) if (!seen.has(id)) overlay.entries.delete(id);
  });
  useLayoutEffect(() => () => overlay.entries.clear(), [city]);

  return (
    <div className="map-overlay">
      {items.map((it) => (
        <div
          key={it.id}
          ref={(el) => {
            if (el) refs.current.set(it.id, el);
            else refs.current.delete(it.id);
          }}
          className={`ov-item ${it.className}`}
        >
          {it.node}
        </div>
      ))}
    </div>
  );
}
