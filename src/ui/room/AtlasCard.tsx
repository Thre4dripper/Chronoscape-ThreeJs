import { useEffect, useRef, useState } from "react";
import type { Atlas } from "@/content/schema";
import { playableMaps, useNav } from "@/nav";
import { FoldedMap } from "../FoldedMap";
import { ROMAN } from "./toon";

/** An atlas taken from the shelf: what it covers, and its maps, folded, ready to open. */
export function AtlasCard({ atlas, index, onClose }: { atlas: Atlas; index: number; onClose: () => void }) {
  const openMap = useNav((s) => s.openMap);
  const open = atlas.maps.filter((m) => m.city);
  // a map picked on the atlas itself (its cover or index page) is shown here
  const [picked, setPicked] = useState<string | null>(null);
  const root = useRef<HTMLElement>(null);
  useEffect(() => {
    let timer = 0;
    const on = (e: Event) => {
      const d = (e as CustomEvent<{ atlas: string; title: string }>).detail;
      if (d.atlas !== atlas.id) return;
      setPicked(d.title);
      root.current?.querySelector(`[data-title="${CSS.escape(d.title)}"]`)?.scrollIntoView({ behavior: "smooth", block: "center" });
      clearTimeout(timer);
      timer = window.setTimeout(() => setPicked(null), 1800);
    };
    addEventListener("chronoscape:pick-map", on);
    return () => (removeEventListener("chronoscape:pick-map", on), clearTimeout(timer));
  }, [atlas.id]);
  return (
    <aside ref={root} className="atlas-card" data-hud-block aria-label={atlas.title} style={{ ["--tie" as string]: atlas.color }}>
      <button className="atlas-card__close" onClick={onClose} aria-label="Put the atlas back">
        ×
      </button>
      <div className="atlas-card__eyebrow">
        Atlas {ROMAN[index] ?? index + 1} · {atlas.region}
      </div>
      <h2 className="atlas-card__title">{atlas.title}</h2>
      <div className="atlas-card__era">{atlas.era}</div>
      <p className="atlas-card__blurb">{atlas.blurb}</p>
      {atlas.themes.length > 0 && (
        <ul className="atlas-card__themes">
          {atlas.themes.map((t) => (
            <li key={t}>{t}</li>
          ))}
        </ul>
      )}
      <h3 className="atlas-card__h">
        Maps in this atlas <span>{open.length ? `${open.length} of ${atlas.maps.length} ready to unfold` : "all in preparation"}</span>
      </h3>
      <div className="atlas-card__maps">
        {atlas.maps.map((m) => (
          <div key={m.title} className={`atlas-card__map ${picked === m.title ? "is-picked" : ""}`} data-title={m.title}>
            <FoldedMap map={m} color={atlas.color} slot={`${atlas.id}:${m.title}`} onOpen={(r) => openMap(atlas.id, m, { x: r.x, y: r.y, w: r.width, h: r.height })} />
            <p>{m.blurb}</p>
          </div>
        ))}
      </div>
      <p className="atlas-card__foot">
        {open.length ? "Click a map to unfold it." : `Its cities are still being drawn. ${[...new Set(playableMaps().map((p) => p.map.title))].join(" and ")} can be unfolded from other atlases on the shelf.`}
      </p>
    </aside>
  );
}
