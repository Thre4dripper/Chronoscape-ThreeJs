import { useEffect } from "react";
import { atlasCatalog } from "@/content/registry";
import { useStore } from "@/engine/store";
import { enterCity, playableMaps, useNav } from "@/nav";
import type { Atlas, AtlasMap } from "@/content/schema";
import { FoldedMap } from "./FoldedMap";

/**
 * The map case: every atlas and its maps, folded, in a drawer at the side of
 * a city. Click another map and it unfolds over this one; click this city in
 * another era and the city simply turns to it.
 */
export function MapCase({ open, onClose }: { open: boolean; onClose: () => void }) {
  const cityId = useStore((s) => s.cityId);
  const periodId = useStore((s) => s.periodId);
  const fromAtlas = useNav((s) => s.fromAtlas);
  useEffect(() => {
    if (!open) return;
    const onKey = (e: KeyboardEvent) => {
      if (e.key === "Escape") {
        e.preventDefault();
        e.stopPropagation();
        onClose();
      }
    };
    addEventListener("keydown", onKey, true);
    return () => removeEventListener("keydown", onKey, true);
  }, [open, onClose]);
  // the atlas this map came from first (or any holding this city), then the rest
  const rank = (a: Atlas) => (a.id === fromAtlas ? 0 : a.maps.some((m) => m.city === cityId) ? 1 : 2);
  const atlases = [...atlasCatalog.atlases].sort((a, b) => rank(a) - rank(b));
  const ready = playableMaps();
  const pick = (a: Atlas, m: AtlasMap, r: DOMRect) => {
    const here = m.city === cityId && m.period === periodId;
    onClose();
    if (here) return;
    if (m.city === cityId) {
      // the same city in another era: just turn the ages
      void enterCity(m.city, m.period ?? null);
      useNav.setState({ fromAtlas: a.id });
      return;
    }
    useNav.getState().openMap(a.id, m, { x: r.x, y: r.y, w: r.width, h: r.height });
  };
  return (
    <>
      <div className={`mapcase__scrim ${open ? "is-open" : ""}`} onClick={onClose} aria-hidden="true" />
      <aside className={`mapcase ${open ? "is-open" : ""}`} data-hud-block aria-label="Map case" aria-hidden={!open}>
        <header className="mapcase__head">
          <div>
            <div className="mapcase__kicker">Chronoscape</div>
            <h2>The Map Case</h2>
          </div>
          <button className="mapcase__close" onClick={onClose} aria-label="Close the map case">
            ×
          </button>
        </header>
        <div className="mapcase__nav">
          <button className="btn" onClick={() => (onClose(), useNav.getState().leaveCity())}>
            Back to the Map Room
          </button>
          <button className="btn btn--ghost" onClick={() => (onClose(), useNav.getState().goTitle())}>
            Title page
          </button>
        </div>
        <div className="mapcase__body">
          <section className="mapcase__atlas mapcase__atlas--ready">
            <h3>
              Ready to unfold
              <span>{ready.length} maps you can open now</span>
            </h3>
            <div className="mapcase__maps">
              {ready.map(({ atlas: a, map: m }) => {
                const here = m.city === cityId && m.period === periodId;
                return (
                  <div key={`${a.id}:${m.title}`} className={`mapcase__map ${here ? "is-here" : ""}`} style={{ ["--tie" as string]: a.color }}>
                    <FoldedMap map={m} color={a.color} size="sm" onOpen={(r) => pick(a, m, r)} />
                    {here && <span className="mapcase__here">You are here</span>}
                  </div>
                );
              })}
            </div>
          </section>
          {atlases.map((a) => (
            <section key={a.id} className="mapcase__atlas" style={{ ["--tie" as string]: a.color }}>
              <h3>
                {a.title}
                <span>{a.era}</span>
              </h3>
              <div className="mapcase__maps">
                {a.maps.map((m) => {
                  const here = m.city === cityId && m.period === periodId;
                  return (
                    <div key={m.title} className={`mapcase__map ${here ? "is-here" : ""}`}>
                      <FoldedMap
                        map={m}
                        color={a.color}
                        size="sm"
                        onOpen={(r) => pick(a, m, r)}
                      />
                      {here && <span className="mapcase__here">You are here</span>}
                    </div>
                  );
                })}
              </div>
            </section>
          ))}
        </div>
      </aside>
    </>
  );
}
