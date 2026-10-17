import { useEffect, useRef, useState } from "react";
import type { AtlasMap } from "@/content/schema";
import { previewOf } from "@/nav";
import { drawMap, loadLand, type View } from "@/world/world";

/**
 * A map folded into a packet: the face shows the middle of the map, the
 * edges of the folds stack behind it, and on hover the front flap lifts to
 * show the inside. Playable maps carry the city's real plate; maps still in
 * preparation show an engraved snippet of their region and a stamp.
 */
const snippets = new Map<string, Promise<string>>();
export function snippetFor(m: AtlasMap, color: string): Promise<string> {
  const key = `${m.title}:${m.at.join(",")}`;
  let p = snippets.get(key);
  if (!p) {
    p = loadLand("50m").then((land) => {
      const c = document.createElement("canvas");
      c.width = 420;
      c.height = 520;
      const ctx = c.getContext("2d")!;
      const kx = Math.cos((m.at[1] * Math.PI) / 180);
      const halfH = 5.5, halfW = (halfH * (420 / 520)) / kx;
      const v: View = { lon0: m.at[0] - halfW, lon1: m.at[0] + halfW, lat0: m.at[1] - halfH, lat1: m.at[1] + halfH, x: 0, y: 0, w: 420, h: 520 };
      drawMap(ctx, v, { land, graticule: 2, pins: [{ at: m.at, color, open: false, label: m.title }], weight: 1.2, sea: "#e3d2a6", paper: "#f1e4c3" });
      return c.toDataURL("image/jpeg", 0.82);
    });
    snippets.set(key, p);
  }
  return p;
}

export function FoldedMap({
  map,
  color,
  onOpen,
  size = "md",
  slot,
}: {
  map: AtlasMap;
  color: string;
  onOpen?: (rect: DOMRect) => void;
  size?: "sm" | "md";
  /** Lets the fold animation find this packet again. */
  slot?: string;
}) {
  const playable = !!map.city;
  const [img, setImg] = useState<string | null>(playable ? previewOf(map.city!, map.period) : null);
  useEffect(() => {
    if (playable) return;
    let alive = true;
    void snippetFor(map, color).then((u) => alive && setImg(u));
    return () => {
      alive = false;
    };
  }, [map, color, playable]);
  const packet = useRef<HTMLDivElement>(null);
  const label = (
    <span className="fmap__label">
      <strong>{map.title}</strong>
      <span>{map.subtitle}</span>
    </span>
  );
  const body = (
    <div className="fmap__packet" ref={packet} data-map-slot={slot} style={{ ["--img" as string]: img ? `url("${img}")` : "none", ["--tie" as string]: color }}>
      <div className="fmap__edges" aria-hidden="true" />
      <div className="fmap__inside" aria-hidden="true" />
      <div className="fmap__flap" aria-hidden="true">
        <div className="fmap__face" />
        <div className="fmap__back" />
      </div>
      <div className="fmap__tie" aria-hidden="true" />
      {playable ? (
        <span className="fmap__seal" aria-hidden="true">
          ✦
        </span>
      ) : (
        <span className="fmap__stamp">In preparation</span>
      )}
    </div>
  );
  if (!playable || !onOpen)
    return (
      <div className={`fmap fmap--${size} ${playable ? "" : "is-planned"}`} title={map.blurb}>
        {body}
        {label}
      </div>
    );
  return (
    <button className={`fmap fmap--${size} is-open`} onClick={() => onOpen(packet.current!.getBoundingClientRect())} title={map.blurb}>
      {body}
      {label}
    </button>
  );
}
