import type { City } from "@/content/schema";
import { useStore } from "@/engine/store";
import { formatYear } from "./Hud";

export function Timeline({ city }: { city: City }) {
  const periodId = useStore((s) => s.periodId);
  const setPeriod = useStore((s) => s.setPeriod);
  const storyId = useStore((s) => s.storyId);
  const sorted = [...city.periods].sort((a, b) => a.year - b.year);
  return (
    <nav className="timeline" aria-label="Historical period">
      <div className="timeline__rail" />
      {sorted.map((p) => (
        <button
          key={p.id}
          className={`timeline__stop ${p.id === periodId ? "is-active" : ""}`}
          onClick={() => setPeriod(p.id)}
          disabled={!!storyId}
          title={storyId ? "Finish or exit the story to change period" : p.summary}
        >
          <span className="timeline__year">{formatYear(p.year)}</span>
          <span className="timeline__label">{p.label}</span>
        </button>
      ))}
    </nav>
  );
}
