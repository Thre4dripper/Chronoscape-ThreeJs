import type { City } from "@/content/schema";
import { useStore, eventById } from "@/engine/store";

export function EventCard({ city }: { city: City }) {
  const id = useStore((s) => s.focusedEventId);
  const { back, focus, focusSpot } = useStore.getState();
  const e = eventById(city, id);
  if (!e) return null;
  const sources = e.sourceIds.map((sid) => city.sources.find((s) => s.id === sid)!).filter(Boolean);
  const at = e.at;
  const place = "landmarkId" in at ? city.landmarks.find((l) => l.id === at.landmarkId) : "spotId" in at ? city.spots.find((s) => s.id === at.spotId) : null;
  return (
    <aside className="panel panel--event" aria-label="Event">
      <div className="panel__head">
        <div className="panel__eyebrow">
          {e.kind} · {e.date}
        </div>
        <h2 className="panel__title">{e.title}</h2>
        {place && <div className="panel__meta">At: {place.name}</div>}
      </div>
      <div className="panel__body">
        <p className="panel__lead">{e.text}</p>
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
              </li>
            ))}
          </ol>
        </section>
      </div>
      <div className="panel__actions">
        {place && (
          <button
            className="btn btn--primary"
            onClick={() => {
              if ("landmarkId" in at) focus(at.landmarkId);
              else if ("spotId" in at) focusSpot(at.spotId);
            }}
          >
            About the place
          </button>
        )}
        <button className="btn" onClick={back}>
          Return to map
        </button>
      </div>
    </aside>
  );
}
