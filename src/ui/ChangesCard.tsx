import type { City } from "@/content/schema";
import { useStore } from "@/engine/store";
import { formatYear } from "./Hud";

/** Explains what changed when the period switched, instead of silently swapping models. */
export function ChangesCard({ city }: { city: City }) {
  const change = useStore((s) => s.periodChange);
  const dismiss = useStore((s) => s.dismissChange);
  const focus = useStore((s) => s.focus);
  if (!change) return null;
  const to = city.periods.find((p) => p.id === change.toId)!;
  return (
    <div className="changes" role="status">
      <div className="changes__head">
        <span>
          {to.label} · {formatYear(to.year)}
        </span>
        <button className="changes__close" onClick={dismiss} aria-label="Dismiss">
          ×
        </button>
      </div>
      <p className="changes__summary">{to.summary}</p>
      {change.entries.length > 0 && (
        <ul className="changes__list">
          {change.entries.map((e) => (
            <li key={e.landmarkId} className={`changes__item changes__item--${e.kind}`}>
              <button
                onClick={() => {
                  if (e.kind !== "disappears") focus(e.landmarkId);
                }}
                disabled={e.kind === "disappears"}
              >
                <span className="changes__kind">{e.kind}</span> <strong>{e.name}</strong>
                {e.note ? <span className="changes__note"> — {e.note}</span> : null}
              </button>
            </li>
          ))}
        </ul>
      )}
    </div>
  );
}
