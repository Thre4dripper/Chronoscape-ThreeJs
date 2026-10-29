import { useEffect, useState } from "react";
import type { City } from "@/content/schema";
import { useStore, landmarkById, resolveVariant, currentFocus } from "@/engine/store";

const HINTS: Record<string, string> = {
  exploring: "Drag to explore · scroll to zoom · right-drag to rotate",
  previewing: "Click to enter",
  focused: "Esc to return · Enter scene for street level",
  immersed: "Esc to step back",
};

export function Hud({ city, onMapCase }: { city: City; onMapCase: () => void }) {
  const mode = useStore((s) => s.mode);
  const periodId = useStore((s) => s.periodId);
  const hoveredId = useStore((s) => s.hoveredId);
  const focusedId = useStore((s) => s.focusedId);
  const touch = useStore((s) => s.touch);
  const period = city.periods.find((p) => p.id === periodId);
  const subject = landmarkById(city, focusedId ?? hoveredId);
  const focusedSpotId = useStore((s) => s.focusedSpotId);
  const focusedEventId = useStore((s) => s.focusedEventId);
  const focus = currentFocus({ city, focusedId, focusedSpotId, focusedEventId, periodId });
  const eraOpen = useStore((s) => s.eraOpen);
  const desk = useStore((s) => s.desk);
  const subjectName = subject ? resolveVariant(subject, periodId).name : focus ? focus.name : city.name;

  return (
    <>
      {touch && <TouchTip />}
      <header className="hud hud--top-left">
        <div className="brand">Chronoscape</div>
        <div className="city-line">
          <span className="city-name">{city.name}</span>
          <span className="dot">·</span>
          <span className="city-sub">{city.subtitle}</span>
        </div>
      </header>

      <div className="hud hud--top-right">
        <button className={`btn btn--desk ${desk ? "is-active" : ""}`} onClick={() => useStore.getState().toggleDesk()} aria-pressed={desk} aria-label="Desk" title={desk ? "Clear the table: just the map" : "Lay the map on the writing table"}>
          <span className="btn--desk__icon" aria-hidden="true" />
          <span className="btn--desk__label">Desk</span>
        </button>
        <button className={`btn btn--era ${eraOpen ? "is-active" : ""}`} onClick={() => useStore.getState().toggleEra()}>
          This era
        </button>
        <button className="btn btn--case" onClick={onMapCase} aria-label="Open the map case: every atlas and map">
          <span className="btn--case__icon" aria-hidden="true" />
          <span className="btn--case__label">Map case</span>
        </button>
      </div>

      <footer className="hud hud--bottom-left">
        <div className="status-subject">{subjectName}</div>
        <div className="status-line">
          <span>{period ? formatYear(period.year) : ""}</span>
          <span className="dot">·</span>
          <span className="status-mode">{mode}</span>
        </div>
        <div className="status-hint">{touch && mode === "exploring" ? "Tap a monument to raise it · tap the map to raise its streets" : HINTS[mode]}</div>
      </footer>
    </>
  );
}

export function formatYear(y: number): string {
  return y < 0 ? `${-y} BCE` : `${y} CE`;
}

/** Shown once on a touch screen: how a finger explores the map without hover. */
function TouchTip() {
  const KEY = "chronoscape.touch-tip";
  const [show, setShow] = useState(() => {
    try {
      return !localStorage.getItem(KEY);
    } catch {
      return true;
    }
  });
  useEffect(() => {
    if (!show) return;
    const done = () => {
      setShow(false);
      try {
        localStorage.setItem(KEY, "1");
      } catch {
        /* private mode: show it again next time */
      }
    };
    const t = setTimeout(done, 9000);
    return () => clearTimeout(t);
  }, [show]);
  if (!show) return null;
  return (
    <div className="touch-tip" role="note" onClick={() => setShow(false)}>
      <strong>Exploring with a finger</strong>
      <span>Tap a monument to raise it · tap the map to raise its streets, fields and boats</span>
      <span>Hold and slide to glide the lens · two fingers twist to turn, slide up or down to tilt</span>
    </div>
  );
}
