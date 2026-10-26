import { useEffect, useState } from "react";
import { atlasCatalog } from "@/content/registry";
import { playableMaps, useNav } from "@/nav";
import { WorldDrift } from "./WorldDrift";
import { Corner, Emblem, Rule } from "./Ornaments";
import { Procession } from "./Procession";

/**
 * The frontispiece: what Chronoscape is, over an engraved world chart that
 * drifts east with ships under sail, and a procession of travellers from
 * every age crossing the foot of the page. One way in: the Map Room.
 */
const WAYS = [
  { kind: "rise" as const, title: "Hover, and it rises", text: "Every building on the drawn map lifts into a small model when you point at it." },
  { kind: "ages" as const, title: "Turn the ages", text: "Step through the centuries and watch the streets, walls and monuments change." },
  { kind: "codex" as const, title: "Open the codex", text: "Old engravings, measured drawings and the story of each place, from the sources." },
  { kind: "hunt" as const, title: "Find it on the map", text: "Riddles, a quiz for every monument, and laurels for the sharp-eyed." },
];

export function TitlePage() {
  const goRoom = useNav((s) => s.goRoom);
  const openMap = useNav((s) => s.openMap);
  const [leaving, setLeaving] = useState(false);
  const atlases = atlasCatalog.atlases.length;
  const open = playableMaps();
  const rome = open.find((p) => p.map.city === "rome" && p.map.period === "empire-100ce") ?? open[0];

  // warm the map room's code while the visitor reads
  useEffect(() => {
    const idle = (window as Window & { requestIdleCallback?: (f: () => void) => number }).requestIdleCallback ?? ((f: () => void) => setTimeout(f, 1200));
    idle(() => void import("../room/MapRoom"));
  }, []);

  const enter = () => {
    if (leaving) return;
    setLeaving(true);
    setTimeout(() => goRoom(), matchMedia("(prefers-reduced-motion: reduce)").matches ? 0 : 750);
  };

  return (
    <div className={`title-page ${leaving ? "is-leaving" : ""}`}>
      <WorldDrift speed={leaving ? 6 : 1} />
      <div className="title-page__grain" aria-hidden="true" />
      <main className="frontis">
        <div className="frontis__frame">
          <Corner className="frontis__corner frontis__corner--tl" />
          <Corner className="frontis__corner frontis__corner--tr" />
          <Corner className="frontis__corner frontis__corner--bl" />
          <Corner className="frontis__corner frontis__corner--br" />
          <p className="frontis__kicker">An illustrated atlas of the world's cities through time</p>
          <h1 className="frontis__title">Chronoscape</h1>
          <Rule className="frontis__rule" />
          <p className="frontis__lead">
            Take a map from the shelf and watch it unfold into a living city. Point at a temple and it rises from the paper; turn the ages and see the city grow, burn,
            and rise again, from the temples of Thebes to the shogun's Edo.
          </p>
          <div className="frontis__actions">
            <button className="seal-btn" onClick={enter}>
              <span className="seal-btn__wax" aria-hidden="true">
                C
              </span>
              <span className="seal-btn__text">
                Enter the Map Room
                <small>
                  {atlases} atlases · {open.length} maps ready to unfold
                </small>
              </span>
            </button>
            {rome && (
              <button className="frontis__shortcut" onClick={(e) => openMap(rome.atlas.id, rome.map, rectOf(e.currentTarget))}>
                or unfold {rome.map.title}, {rome.map.subtitle.split(", ").pop()} <span aria-hidden="true">→</span>
              </button>
            )}
          </div>
        </div>
      </main>
      <ol className="ways" aria-label="How it works">
        {WAYS.map((w) => (
          <li key={w.kind} className="ways__item">
            <span className="ways__medal">
              <Emblem kind={w.kind} />
            </span>
            <strong>{w.title}</strong>
            <span>{w.text}</span>
          </li>
        ))}
      </ol>
      <Procession />
    </div>
  );
}

function rectOf(el: Element) {
  const r = el.getBoundingClientRect();
  // a small folded packet rising from the link
  return { x: r.x + r.width / 2 - 40, y: r.y - 40, w: 80, h: 100 };
}
