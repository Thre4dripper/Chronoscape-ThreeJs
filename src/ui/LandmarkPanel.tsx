import type { City } from "@/content/schema";
import { useStore, landmarkById, resolveVariant } from "@/engine/store";
import { formatYear } from "./Hud";

const CONFIDENCE: Record<string, { label: string; blurb: string }> = {
  documented: { label: "Documented", blurb: "Form and location are well attested by remains and sources." },
  reconstruction: { label: "Evidence-based reconstruction", blurb: "Built from partial remains and descriptions; details are inferred." },
  interpretation: { label: "Artistic interpretation", blurb: "Location is known, but the appearance is largely imagined." },
};

export function LandmarkPanel({ city }: { city: City }) {
  const focusedId = useStore((s) => s.focusedId);
  const periodId = useStore((s) => s.periodId);
  const mode = useStore((s) => s.mode);
  const storyId = useStore((s) => s.storyId);
  const { back, immerse } = useStore.getState();
  const l = landmarkById(city, focusedId);
  if (!l || storyId) return null;
  const v = resolveVariant(l, periodId);
  const period = city.periods.find((p) => p.id === periodId)!;
  const sources = l.sourceIds.map((id) => city.sources.find((s) => s.id === id)!).filter(Boolean);
  const conf = CONFIDENCE[v.confidence];
  const otherPeriods = city.periods
    .filter((p) => p.id !== periodId)
    .sort((a, b) => a.year - b.year)
    .map((p) => ({ p, present: l.activePeriods.includes(p.id), note: l.variants[p.id]?.note, name: resolveVariant(l, p.id).name }));

  return (
    <aside className="panel" aria-label="Landmark information">
      <div className="panel__head">
        <div className="panel__eyebrow">
          {l.category} · {formatYear(period.year)}
        </div>
        <h2 className="panel__title">{v.name}</h2>
        {l.built && <div className="panel__meta">Built: {l.built}</div>}
        {l.function && <div className="panel__meta">Function: {l.function}</div>}
      </div>
      <div className="panel__body">
        <p className="panel__lead">{l.summary}</p>
        {v.note && (
          <p className="panel__note">
            <strong>In {period.label}:</strong> {v.note}
          </p>
        )}
        {l.details.map((d, i) => (
          <p key={i}>{d}</p>
        ))}
        <div className={`confidence confidence--${v.confidence}`} title={conf.blurb}>
          <span className="confidence__dot" /> {conf.label}
          <div className="confidence__blurb">{conf.blurb}</div>
        </div>
        {otherPeriods.length > 0 && (
          <section className="panel__section">
            <h3>Across time</h3>
            <ul className="period-list">
              {otherPeriods.map(({ p, present, note, name }) => (
                <li key={p.id}>
                  <span className="period-list__year">{formatYear(p.year)}</span>
                  <span>{present ? `${name}${note ? ` — ${note}` : ""}` : `Not yet standing${note ? ` — ${note}` : ""}`}</span>
                </li>
              ))}
            </ul>
          </section>
        )}
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
                {s.note ? <span className="sources__note"> — {s.note}</span> : null}
              </li>
            ))}
          </ol>
        </section>
      </div>
      <div className="panel__actions">
        {mode === "focused" && l.activity && (
          <button className="btn btn--primary" onClick={immerse}>
            Enter scene
          </button>
        )}
        <button className="btn" onClick={back}>
          {mode === "immersed" ? "Step back" : "Return to map"}
        </button>
      </div>
    </aside>
  );
}
