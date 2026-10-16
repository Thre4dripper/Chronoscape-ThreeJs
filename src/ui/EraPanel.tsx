import type { City } from "@/content/schema";
import { useStore, resolveSpot } from "@/engine/store";
import { formatYear } from "./Hud";

/** What this era is like: summary, population, events to visit, small things to find. */
export function EraPanel({ city }: { city: City }) {
  const open = useStore((s) => s.eraOpen);
  const periodId = useStore((s) => s.periodId);
  const { toggleEra, focusEvent, focusSpot, focus } = useStore.getState();
  if (!open || !periodId) return null;
  const period = city.periods.find((p) => p.id === periodId)!;
  const events = city.events.filter((e) => e.periodId === periodId);
  const spots = city.spots.filter((s) => s.activePeriods.includes(periodId));
  const landmarks = city.landmarks.filter((l) => l.activePeriods.includes(periodId));
  const kinds = [...new Set(spots.map((s) => s.kind))].sort();
  return (
    <aside className="era" aria-label="This era">
      <div className="era__head">
        <div>
          <div className="panel__eyebrow">{formatYear(period.year)} · {period.startYear < 0 ? `${-period.startYear} BCE` : `${period.startYear} CE`}–{period.endYear < 0 ? `${-period.endYear} BCE` : `${period.endYear} CE`}</div>
          <h2 className="panel__title">{period.label}</h2>
        </div>
        <button className="changes__close" onClick={() => toggleEra(false)} aria-label="Close">
          ×
        </button>
      </div>
      <div className="era__body">
        <p className="panel__lead">{period.summary}</p>
        {period.feel && <p className="era__feel">{period.feel}</p>}
        <div className="era__stats">
          {period.population && <span>Population {period.population}</span>}
          <span>{landmarks.length} monuments</span>
          <span>{spots.length} places of daily life</span>
        </div>
        {events.length > 0 && (
          <section className="panel__section">
            <h3>Happening in this era</h3>
            <ul className="era__list">
              {events.map((e) => (
                <li key={e.id}>
                  <button onClick={() => focusEvent(e.id)}>
                    <span className="era__date">{e.date}</span>
                    <strong>{e.title}</strong>
                  </button>
                </li>
              ))}
            </ul>
          </section>
        )}
        <section className="panel__section">
          <h3>Monuments</h3>
          <ul className="era__chips">
            {landmarks.map((l) => (
              <li key={l.id}>
                <button onClick={() => focus(l.id)}>{(l.variants[periodId]?.name ?? l.name).replace(/\s*\(.*\)$/, "")}</button>
              </li>
            ))}
          </ul>
        </section>
        {kinds.map((k) => (
          <section className="panel__section" key={k}>
            <h3>{k}</h3>
            <ul className="era__chips">
              {spots
                .filter((s) => s.kind === k)
                .map((s) => (
                  <li key={s.id}>
                    <button onClick={() => focusSpot(s.id)}>{resolveSpot(s, periodId).name}</button>
                  </li>
                ))}
            </ul>
          </section>
        ))}
      </div>
    </aside>
  );
}
