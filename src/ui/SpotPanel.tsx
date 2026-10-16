import type { City } from "@/content/schema";
import { useStore, spotById, resolveSpot } from "@/engine/store";
import { formatYear } from "./Hud";

const CONF: Record<string, string> = { documented: "Documented", reconstruction: "Evidence-based reconstruction", interpretation: "Artistic interpretation" };

export function SpotPanel({ city }: { city: City }) {
  const id = useStore((s) => s.focusedSpotId);
  const periodId = useStore((s) => s.periodId);
  const hour = useStore((s) => s.hour);
  const storyId = useStore((s) => s.storyId);
  const mode = useStore((s) => s.mode);
  const { back, immerse, setHour } = useStore.getState();
  const sp = spotById(city, id);
  if (!sp || storyId) return null;
  const v = resolveSpot(sp, periodId);
  const period = city.periods.find((p) => p.id === periodId)!;
  const sources = sp.sourceIds.map((sid) => city.sources.find((s) => s.id === sid)!).filter(Boolean);
  const sorted = [...sp.vignettes].sort((a, b) => a.hour - b.hour);
  let nearest = sorted[0];
  for (const vg of sorted) if (Math.min(Math.abs(vg.hour - hour), 24 - Math.abs(vg.hour - hour)) < Math.min(Math.abs(nearest.hour - hour), 24 - Math.abs(nearest.hour - hour))) nearest = vg;

  return (
    <aside className="panel panel--spot" aria-label="Place information">
      <div className="panel__head">
        <div className="panel__eyebrow">
          {sp.kind} · {formatYear(period.year)}
        </div>
        <h2 className="panel__title">{v.name}</h2>
      </div>
      <div className="panel__body">
        <p className="panel__lead">{sp.summary}</p>
        {v.note && (
          <p className="panel__note">
            <strong>In {period.label}:</strong> {v.note}
          </p>
        )}
        {sorted.length > 0 && (
          <section className="panel__section">
            <h3>Through the day</h3>
            <ul className="day-list">
              {sorted.map((vg) => (
                <li key={vg.hour} className={vg === nearest ? "is-now" : ""}>
                  <button onClick={() => setHour(vg.hour)}>
                    <span className="day-list__hour">{String(vg.hour).padStart(2, "0")}:00</span>
                    <span>{vg.text}</span>
                  </button>
                </li>
              ))}
            </ul>
          </section>
        )}
        {sp.details.map((d, i) => (
          <p key={i}>{d}</p>
        ))}
        <div className={`confidence confidence--${sp.confidence}`}>
          <span className="confidence__dot" /> {CONF[sp.confidence]}
        </div>
        <section className="panel__section">
          <h3>Sources</h3>
          <ol className="sources">
            {sources.map((s) => (
              <li key={s.id}>
                {s.url ? (
                  <a href={s.url} target="_blank" rel="noreferrer">
                    {s.title}
                  </a>
                ) : (
                  s.title
                )}
                {s.author ? `, ${s.author}` : ""}
                {s.year ? ` (${s.year})` : ""}
              </li>
            ))}
          </ol>
        </section>
      </div>
      <div className="panel__actions">
        {mode === "focused" && (
          <button className="btn btn--primary" onClick={immerse}>
            Street level
          </button>
        )}
        <button className="btn" onClick={back}>
          {mode === "immersed" ? "Step back" : "Return to map"}
        </button>
      </div>
    </aside>
  );
}
