import { useState } from "react";
import type { City } from "@/content/schema";
import { useStore } from "@/engine/store";
import { formatYear } from "./Hud";

/**
 * The eras as a slim row of years. The chosen era's name sits in one caption under the row; pointing at
 * another year shows that one's name instead, so the bar stays small with five or six eras.
 */
export function Timeline({ city }: { city: City }) {
  const periodId = useStore((s) => s.periodId);
  const setPeriod = useStore((s) => s.setPeriod);
  const storyId = useStore((s) => s.storyId);
  const [hover, setHover] = useState<string | null>(null);
  const sorted = [...city.periods].sort((a, b) => a.year - b.year);
  const shown = sorted.find((p) => p.id === (hover ?? periodId));
  return (
    <nav className="timeline" aria-label="Historical period" onPointerLeave={() => setHover(null)}>
      <div className="timeline__stops">
        {sorted.map((p) => (
          <button
            key={p.id}
            className={`timeline__stop ${p.id === periodId ? "is-active" : ""}`}
            onClick={() => setPeriod(p.id)}
            onPointerEnter={(e) => e.pointerType === "mouse" && setHover(p.id)}
            onFocus={() => setHover(p.id)}
            onBlur={() => setHover(null)}
            disabled={!!storyId}
            title={storyId ? "Finish or exit the story to change period" : p.summary}
          >
            <span className="timeline__year">{formatYear(p.year)}</span>
            <span className="timeline__label">{p.label}</span>
          </button>
        ))}
      </div>
      {shown && (
        <div className={`timeline__caption ${hover && hover !== periodId ? "is-preview" : ""}`} aria-hidden="true">
          {shown.label}
        </div>
      )}
    </nav>
  );
}
