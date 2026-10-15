import { useState } from "react";
import type { City } from "@/content/schema";
import { useStore, currentStory } from "@/engine/store";

export function StoryBar({ city }: { city: City }) {
  const storyId = useStore((s) => s.storyId);
  const step = useStore((s) => s.storyStep);
  const story = useStore((s) => currentStory(s));
  const { startStory, storyNext, storyPrev, endStory } = useStore.getState();
  const [open, setOpen] = useState(false);
  if (city.stories.length === 0) return null;

  if (!storyId || !story) {
    return (
      <div className="story-launcher">
        <button className="btn" onClick={() => setOpen((o) => !o)} aria-expanded={open}>
          Stories
        </button>
        {open && (
          <ul className="story-menu">
            {city.stories.map((s) => (
              <li key={s.id}>
                <button
                  onClick={() => {
                    setOpen(false);
                    startStory(s.id);
                  }}
                >
                  <strong>{s.title}</strong>
                  <span>{s.summary}</span>
                </button>
              </li>
            ))}
          </ul>
        )}
      </div>
    );
  }

  const cur = story.steps[step];
  const last = step === story.steps.length - 1;
  const stepSources = cur.sourceIds.map((id) => city.sources.find((s) => s.id === id)!).filter(Boolean);
  return (
    <div className="story" role="dialog" aria-label={story.title}>
      <div className="story__head">
        <span className="story__eyebrow">{story.title}</span>
        <span className="story__progress">
          {step + 1} / {story.steps.length}
        </span>
      </div>
      <h3 className="story__title">
        {cur.title}
        {cur.when ? <span className="story__when"> · {cur.when}</span> : null}
      </h3>
      <p className="story__text">{cur.text}</p>
      {stepSources.length > 0 && (
        <p className="story__sources">
          Sources:{" "}
          {stepSources.map((s, i) => (
            <span key={s.id}>
              {i > 0 ? "; " : ""}
              {s.url ? (
                <a href={s.url} target="_blank" rel="noreferrer">
                  {s.title}
                </a>
              ) : (
                s.title
              )}
            </span>
          ))}
        </p>
      )}
      <div className="story__actions">
        <button className="btn" onClick={storyPrev} disabled={step === 0}>
          ← Back
        </button>
        {last ? (
          <button className="btn btn--primary" onClick={endStory}>
            Finish
          </button>
        ) : (
          <button className="btn btn--primary" onClick={storyNext}>
            Next →
          </button>
        )}
        <button className="btn btn--ghost" onClick={endStory}>
          Exit story
        </button>
      </div>
      <div className="story__dots">
        {story.steps.map((_, i) => (
          <span key={i} className={i === step ? "is-active" : ""} />
        ))}
      </div>
    </div>
  );
}
