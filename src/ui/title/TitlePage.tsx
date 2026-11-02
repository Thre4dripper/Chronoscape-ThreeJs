import { useEffect, useState } from "react";
import { atlasCatalog } from "@/content/registry";
import { playableMaps, useNav } from "@/nav";
import { SOURCE } from "@/meta";
import { WorldDrift } from "./WorldDrift";
import { Corner, Emblem, Rule } from "./Ornaments";
import { Procession } from "./Procession";

/**
 * The frontispiece: what Chronoscape is, over an engraved world chart that
 * drifts east with ships under sail, and a procession of travellers from
 * every age crossing the foot of the page. One way in: the Map Room; and a
 * silk ribbon marking where the source is kept.
 */
const WAYS = [
  { kind: "rise" as const, title: "Hover, and it rises", text: "Every building on the drawn map lifts into a small model when you point at it." },
  { kind: "ages" as const, title: "Turn the ages", text: "Step through the centuries and watch the streets, walls and monuments change." },
  { kind: "codex" as const, title: "Open the codex", text: "Old engravings, measured drawings and the story of each place, from the sources." },
  { kind: "hunt" as const, title: "Find it on the map", text: "Riddles, a quiz for every monument, and laurels for the sharp-eyed." },
];

export function TitlePage() {
  const goRoom = useNav((s) => s.goRoom);
  const [leaving, setLeaving] = useState(false);
  const atlases = atlasCatalog.atlases.length;
  const open = playableMaps();

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
      <a className="ribbon" href={SOURCE} target="_blank" rel="noopener" aria-label="Read the source on GitHub" title="Read the source on GitHub">
        <span className="ribbon__silk">
          <span className="ribbon__medal">
            <GitHubMark />
          </span>
          <span className="ribbon__label">Fons</span>
        </span>
      </a>
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

/** The GitHub mark, struck in gilt on the ribbon's medal. */
function GitHubMark() {
  return (
    <svg viewBox="0 0 16 16" aria-hidden="true">
      <path
        fill="currentColor"
        d="M8 0C3.58 0 0 3.58 0 8c0 3.54 2.29 6.53 5.47 7.59.4.07.55-.17.55-.38 0-.19-.01-.82-.01-1.49-2.01.37-2.53-.49-2.69-.94-.09-.23-.48-.94-.82-1.13-.28-.15-.68-.52-.01-.53.63-.01 1.08.58 1.23.82.72 1.21 1.87.87 2.33.66.07-.52.28-.87.51-1.07-1.78-.2-3.64-.89-3.64-3.95 0-.87.31-1.59.82-2.15-.08-.2-.36-1.02.08-2.12 0 0 .67-.21 2.2.82.64-.18 1.32-.27 2-.27.68 0 1.36.09 2 .27 1.53-1.04 2.2-.82 2.2-.82.44 1.1.16 1.92.08 2.12.51.56.82 1.27.82 2.15 0 3.07-1.87 3.75-3.65 3.95.29.25.54.73.54 1.48 0 1.07-.01 1.93-.01 2.2 0 .21.15.46.55.38A8.013 8.013 0 0016 8c0-4.42-3.58-8-8-8z"
      />
    </svg>
  );
}
