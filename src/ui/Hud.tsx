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
  const subjectName = subject ? resolveVariant(subject, periodId).name : focus ? focus.name : city.name;

  return (
    <>
      <header className="hud hud--top-left">
        <div className="brand">Chronoscape</div>
        <div className="city-line">
          <span className="city-name">{city.name}</span>
          <span className="dot">·</span>
          <span className="city-sub">{city.subtitle}</span>
        </div>
      </header>

      <div className="hud hud--top-right">
        <button className={`btn btn--era ${eraOpen ? "is-active" : ""}`} onClick={() => useStore.getState().toggleEra()}>
          This era
        </button>
        <button className="btn btn--case" onClick={onMapCase} aria-label="Open the map case: every atlas and map">
          <span className="btn--case__icon" aria-hidden="true" />
          Map case
        </button>
      </div>

      <footer className="hud hud--bottom-left">
        <div className="status-subject">{subjectName}</div>
        <div className="status-line">
          <span>{period ? formatYear(period.year) : ""}</span>
          <span className="dot">·</span>
          <span className="status-mode">{mode}</span>
        </div>
        <div className="status-hint">{touch && mode === "exploring" ? "Tap a landmark to preview · tap again to enter" : HINTS[mode]}</div>
      </footer>
    </>
  );
}

export function formatYear(y: number): string {
  return y < 0 ? `${-y} BCE` : `${y} CE`;
}
