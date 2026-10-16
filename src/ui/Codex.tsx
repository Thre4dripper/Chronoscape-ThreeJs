import { useEffect, useMemo, useRef, useState } from "react";
import type { City, Landmark } from "@/content/schema";
import { useStore, landmarkById, landmarkForEvent, resolveVariant } from "@/engine/store";
import {
  addLaurels, bearing, fmtYear, loadElevations, loadPictures, loadPlans, modelKey, questionsFor, readLaurels, riddleFor,
  type Elevation, type Laurels, type Picture, type Plan, type Riddle,
} from "@/engine/codex";

/**
 * The left-hand notebook. When a place is open: pictures from the sources
 * (engravings, paintings, plans, photographs, with credits), measured drawings
 * rendered from the model, how it changed through the eras, and a short quiz.
 * Below it, always: the map hunt, a riddle you answer by finding the place.
 */
type Tab = "pictures" | "drawings" | "ages" | "quiz";
const TABS: { id: Tab; label: string; latin: string }[] = [
  { id: "pictures", label: "Pictures", latin: "Imagines" },
  { id: "drawings", label: "Drawings", latin: "Delineatio" },
  { id: "ages", label: "Ages", latin: "Tempora" },
  { id: "quiz", label: "Quiz", latin: "Quaestio" },
];

const store = {
  get: (k: string) => {
    try {
      return localStorage.getItem(k);
    } catch {
      return null;
    }
  },
  set: (k: string, v: string) => {
    try {
      localStorage.setItem(k, v);
    } catch {
      /* not kept */
    }
  },
};

export function LeftColumn({ city }: { city: City }) {
  const focusedId = useStore((s) => s.focusedId);
  const focusedEventId = useStore((s) => s.focusedEventId);
  const eraOpen = useStore((s) => s.eraOpen);
  const storyId = useStore((s) => s.storyId);
  const lmId = focusedId ?? landmarkForEvent(city, focusedEventId);
  const l = landmarkById(city, lmId);
  if (eraOpen || storyId) return null;
  return (
    <div className={`leftcol ${l ? "has-codex" : ""}`}>
      {l && <Codex key={l.id} city={city} l={l} />}
      <Hunt city={city} />
    </div>
  );
}

/* ================================================================== codex */

function Codex({ city, l }: { city: City; l: Landmark }) {
  const periodId = useStore((s) => s.periodId);
  const [tab, setTab] = useState<Tab>(() => (store.get("codex.tab") as Tab) || "pictures");
  const narrow = useNarrow();
  const [open, setOpen] = useState(!narrow);
  useEffect(() => setOpen(!narrow), [narrow]);
  const choose = (t: Tab) => {
    setTab(t);
    store.set("codex.tab", t);
  };
  const name = resolveVariant(l, periodId).name;
  return (
    <aside className={`codex ${open ? "" : "is-closed"}`} data-hud-block aria-label={`Notebook: ${name}`}>
      <header className="codex__head">
        <button className="codex__title" onClick={() => narrow && setOpen(!open)} aria-expanded={open}>
          <span className="codex__eyebrow">
            Codex{narrow && <span className="codex__toggle">{open ? "Close ▾" : "Pictures, drawings, quiz ▸"}</span>}
          </span>
          <span className="codex__name">{name}</span>
        </button>
        {open && (
          <nav className="codex__tabs" role="tablist">
            {TABS.map((t) => (
              <button key={t.id} role="tab" aria-selected={tab === t.id} className={tab === t.id ? "is-active" : ""} onClick={() => choose(t.id)}>
                <span className="codex__latin">{t.latin}</span>
                {t.label}
              </button>
            ))}
          </nav>
        )}
      </header>
      {open && (
        <div className="codex__body">
          {tab === "pictures" && <Pictures city={city} l={l} />}
          {tab === "drawings" && <Drawings l={l} periodId={periodId} />}
          {tab === "ages" && <Ages city={city} l={l} />}
          {tab === "quiz" && <Quiz city={city} l={l} />}
        </div>
      )}
    </aside>
  );
}

function useNarrow() {
  const q = "(max-width: 1100px)";
  const [n, setN] = useState(() => typeof matchMedia !== "undefined" && matchMedia(q).matches);
  useEffect(() => {
    const m = matchMedia(q);
    const on = () => setN(m.matches);
    m.addEventListener("change", on);
    return () => m.removeEventListener("change", on);
  }, []);
  return n;
}

function useAsync<T>(fn: () => Promise<T>, deps: unknown[]): T | undefined {
  const [v, setV] = useState<T>();
  useEffect(() => {
    let alive = true;
    fn().then((x) => alive && setV(x));
    return () => {
      alive = false;
    };
    // eslint-disable-next-line react-hooks/exhaustive-deps
  }, deps);
  return v;
}

/* ------------------------------------------------------------------ pictures */

function Pictures({ city, l }: { city: City; l: Landmark }) {
  const index = useAsync(() => loadPictures(city.id), [city.id]);
  const [i, setI] = useState(0);
  const [zoom, setZoom] = useState(false);
  if (index === undefined) return <p className="codex__quiet">Opening the folio…</p>;
  const pics = index?.[l.id] ?? [];
  if (!pics.length) return <p className="codex__quiet">No freely licensed pictures of this place were found in its sources.</p>;
  const p = pics[Math.min(i, pics.length - 1)];
  return (
    <div className="pics">
      <figure className="pics__main">
        <button className="pics__frame" onClick={() => setZoom(true)} aria-label="Enlarge picture">
          <img src={`/${p.src}`} width={p.w} height={p.h} alt={p.caption} decoding="async" />
        </button>
        <figcaption>
          <div className="pics__kind">
            {p.kind}
            {p.date ? ` · ${p.date}` : ""}
          </div>
          <p className="pics__caption">{p.caption}</p>
          <Credit p={p} />
        </figcaption>
      </figure>
      {pics.length > 1 && (
        <div className="pics__strip">
          {pics.map((q, k) => (
            <button key={q.src} className={k === i ? "is-active" : ""} onClick={() => setI(k)} aria-label={`Picture ${k + 1}: ${q.kind}`}>
              <img src={`/${q.thumb ?? q.src}`} alt="" loading="lazy" decoding="async" />
            </button>
          ))}
        </div>
      )}
      {zoom && <Lightbox p={p} onClose={() => setZoom(false)} onStep={(d) => setI((k) => (k + d + pics.length) % pics.length)} />}
    </div>
  );
}

function Credit({ p }: { p: Picture }) {
  return (
    <div className="pics__credit">
      {p.artist}
      {" · "}
      {p.licenseUrl ? (
        <a href={p.licenseUrl} target="_blank" rel="noreferrer">
          {p.license}
        </a>
      ) : (
        p.license
      )}
      {" · "}
      <a href={p.page} target="_blank" rel="noreferrer">
        Wikimedia Commons
      </a>
    </div>
  );
}

function Lightbox({ p, onClose, onStep }: { p: Picture; onClose: () => void; onStep: (d: number) => void }) {
  useEffect(() => {
    const onKey = (e: KeyboardEvent) => {
      if (e.key === "Escape") onClose();
      else if (e.key === "ArrowRight") onStep(1);
      else if (e.key === "ArrowLeft") onStep(-1);
      else return;
      // keep the map from also stepping back or panning
      e.preventDefault();
      e.stopPropagation();
    };
    window.addEventListener("keydown", onKey, true);
    return () => window.removeEventListener("keydown", onKey, true);
  }, [onClose, onStep]);
  return (
    <div className="lightbox" role="dialog" aria-label={p.caption} onClick={onClose}>
      <figure onClick={(e) => e.stopPropagation()}>
        <img src={`/${p.src}`} alt={p.caption} />
        <figcaption>
          <p>{p.caption}</p>
          <Credit p={p} />
        </figcaption>
        <button className="lightbox__close" onClick={onClose} aria-label="Close">
          ×
        </button>
      </figure>
    </div>
  );
}

/* ------------------------------------------------------------------ drawings */

/** A round length for a scale bar about a fifth of the drawing wide. */
function niceLength(m: number) {
  const target = m / 5;
  for (const v of [1, 2, 5, 10, 20, 25, 50, 100, 200, 250, 500]) if (v >= target) return v;
  return 1000;
}

function Drawings({ l, periodId }: { l: Landmark; periodId: string | null }) {
  const key = modelKey(l, periodId);
  const elev = useAsync(() => loadElevations(), []);
  const plans = useAsync(() => loadPlans(), []);
  const e = key ? elev?.[key] : undefined;
  const p = key ? plans?.[key] : undefined;
  const w = e?.w ?? l.footprint[0], d = l.footprint[1], h = e?.h;
  const area = w * d;
  const storeys = h ? Math.max(1, Math.round(h / 3.3)) : null;
  const pitches = area / 7140;
  return (
    <div className="drawings">
      {e && key ? <ElevationSheet e={e} src={`/media/elevations/${key}.jpg`} /> : elev === undefined ? <p className="codex__quiet">Unrolling the drawings…</p> : null}
      {/* small buildings have small plan images: only show a plan that stays sharp at this size */}
      {p && key && (Math.max(p.w, p.d) / p.size) * p.px >= 220 && <PlanSheet p={p} src={`/models/plans/${key}.${p.ext ?? "webp"}`} />}
      <section className="facts">
        <h4>By the numbers</h4>
        <dl>
          <dt>Footprint</dt>
          <dd>
            {Math.round(l.footprint[0])} × {Math.round(l.footprint[1])} m
          </dd>
          {h && (
            <>
              <dt>Height</dt>
              <dd>
                {Math.round(h)} m{storeys ? `, as tall as a ${storeys}-storey house` : ""}
              </dd>
            </>
          )}
          <dt>Ground covered</dt>
          <dd>
            {Math.round(area / 100) * 100 >= 1000 ? `${Math.round(area / 100) * 100} m²` : `${Math.round(area)} m²`}
            {pitches >= 0.3 ? `, about ${pitches >= 1.5 ? Math.round(pitches) : pitches.toFixed(1)} football pitch${pitches >= 1.5 ? "es" : ""}` : ""}
          </dd>
          {l.built && (
            <>
              <dt>Built</dt>
              <dd>{l.built}</dd>
            </>
          )}
        </dl>
      </section>
    </div>
  );
}

/** Front elevation with dimension lines, a scale bar and a person for scale. */
function ElevationSheet({ e, src }: { e: Elevation; src: string }) {
  const [W, H] = e.px;
  const px = (m: number) => m / e.mpp;
  const g = e.ground, x0 = e.x0px, x1 = x0 + px(e.w), top = g - px(e.h);
  const bar = niceLength(e.w);
  const person = px(1.75);
  // labels about 12 px on screen whatever the drawing's proportions (the sheet is ~334 x at most 300 px)
  const fs = 12 / Math.min(334 / (W * 1.12), 300 / (H * 1.25));
  return (
    <figure className="sheet">
      <div className="sheet__title">Front elevation</div>
      <svg viewBox={`${-fs * 2.6} 0 ${W + fs * 2.6} ${H + fs * 3.2}`} className="sheet__svg" role="img" aria-label={`Front elevation, ${Math.round(e.w)} m wide and ${Math.round(e.h)} m high`}>
        <image href={src} x={0} y={0} width={W} height={H} />
        <line x1={x0 - fs} x2={x1 + fs} y1={g} y2={g} className="ink" />
        {/* width */}
        <g className="dim">
          <line x1={x0} x2={x1} y1={H + fs * 0.9} y2={H + fs * 0.9} />
          <line x1={x0} x2={x0} y1={g + 2} y2={H + fs * 1.3} />
          <line x1={x1} x2={x1} y1={g + 2} y2={H + fs * 1.3} />
          <text x={(x0 + x1) / 2} y={H + fs * 2.2} fontSize={fs}>
            {Math.round(e.w)} m
          </text>
        </g>
        {/* height */}
        <g className="dim">
          <line x1={-fs * 1.1} x2={-fs * 1.1} y1={top} y2={g} />
          <line x1={-fs * 1.6} x2={x0 - 4} y1={top} y2={top} />
          <text x={-fs * 1.5} y={(top + g) / 2} fontSize={fs} transform={`rotate(-90 ${-fs * 1.5} ${(top + g) / 2})`}>
            {Math.round(e.h)} m
          </text>
        </g>
        {/* a person, 1.75 m, standing in front */}
        {person > 1.5 && <Person x={x1 - Math.max(person, 3) * 0.6} ground={g} h={person} />}
        {/* scale bar */}
        <g className="scalebar" transform={`translate(${x0}, ${H + fs * 2.8})`}>
          <rect x={0} y={-fs * 0.3} width={px(bar) / 2} height={fs * 0.3} />
          <rect x={px(bar) / 2} y={-fs * 0.3} width={px(bar) / 2} height={fs * 0.3} className="hollow" />
          <text x={px(bar) + fs * 0.4} y={0} fontSize={fs * 0.85}>
            {bar} m
          </text>
        </g>
      </svg>
      <figcaption>Drawn from the model, looking at the main front. The small figure is 1.75 m tall.</figcaption>
    </figure>
  );
}

function Person({ x, ground, h }: { x: number; ground: number; h: number }) {
  const r = h * 0.11;
  return (
    <g className="person">
      <circle cx={x} cy={ground - h + r} r={r} />
      <path d={`M${x - h * 0.13} ${ground - h * 0.08} L${x - h * 0.1} ${ground - h * 0.72} L${x + h * 0.1} ${ground - h * 0.72} L${x + h * 0.13} ${ground - h * 0.08} Z`} />
    </g>
  );
}

/** Top-down plan, cropped to the building, with a scale bar. */
function PlanSheet({ p, src }: { p: Plan; src: string }) {
  const mpp = p.size / p.px;
  const bar = niceLength(Math.max(p.w, p.d));
  // the plan image is a square centred on the building: crop to the building plus a margin
  const bw = Math.min(p.px, p.w / mpp * 1.08), bd = Math.min(p.px, p.d / mpp * 1.08);
  const x0 = (p.px - bw) / 2, y0 = (p.px - bd) / 2;
  const fs = 12 / Math.min(334 / bw, 300 / (bd * 1.2));
  return (
    <figure className="sheet">
      <div className="sheet__title">Plan</div>
      <svg viewBox={`${x0} ${y0} ${bw} ${bd + fs * 2.2}`} className="sheet__svg sheet__svg--plan" role="img" aria-label={`Plan, ${Math.round(p.w)} by ${Math.round(p.d)} m`}>
        <image href={src} x={0} y={0} width={p.px} height={p.px} />
        <g className="scalebar" transform={`translate(${x0 + fs}, ${y0 + bd + fs * 1.4})`}>
          <rect x={0} y={-fs * 0.3} width={bar / mpp / 2} height={fs * 0.3} />
          <rect x={bar / mpp / 2} y={-fs * 0.3} width={bar / mpp / 2} height={fs * 0.3} className="hollow" />
          <text x={bar / mpp + fs * 0.4} y={0} fontSize={fs * 0.9}>
            {bar} m
          </text>
        </g>
        <text x={x0 + bw - fs * 3} y={y0 + bd + fs * 1.3} fontSize={fs * 0.85} className="sheet__note">
          main front ↓
        </text>
      </svg>
    </figure>
  );
}

/* ------------------------------------------------------------------ ages */

function Ages({ city, l }: { city: City; l: Landmark }) {
  const periodId = useStore((s) => s.periodId);
  const elev = useAsync(() => loadElevations(), []);
  const periods = [...city.periods].sort((a, b) => a.year - b.year);
  let lastKey: string | null = null;
  const go = (pid: string) => {
    const st = useStore.getState();
    st.setPeriod(pid);
    if (useStore.getState().focusedId !== l.id) useStore.getState().focus(l.id);
  };
  return (
    <ol className="ages">
      {periods.map((p) => {
        const present = l.activePeriods.includes(p.id);
        const v = resolveVariant(l, p.id);
        const key = present ? modelKey(l, p.id) : null;
        const changed = !!key && key !== lastKey;
        if (key) lastKey = key;
        const e = key && changed ? elev?.[key] : undefined;
        const note = l.variants[p.id]?.note;
        return (
          <li key={p.id} className={`ages__row ${p.id === periodId ? "is-now" : ""} ${present ? "" : "is-absent"}`}>
            <button disabled={!present || p.id === periodId} onClick={() => go(p.id)} title={present ? `Show ${fmtYear(p.year)}` : "Not standing in this era"}>
              <span className="ages__year">{fmtYear(p.year)}</span>
              <span className="ages__era">{p.label}</span>
            </button>
            <div className="ages__what">
              <strong>{present ? v.name : "Not standing"}</strong>
              {note && <p>{note}</p>}
              {e && key && <img className="ages__elev" src={`/media/elevations/${key}.jpg`} alt={`${v.name}, front elevation`} loading="lazy" />}
              {present && !changed && <span className="ages__same">Unchanged in the drawing</span>}
            </div>
          </li>
        );
      })}
    </ol>
  );
}

/* ------------------------------------------------------------------ quiz */

function Quiz({ city, l }: { city: City; l: Landmark }) {
  const periodId = useStore((s) => s.periodId);
  const [attempt, setAttempt] = useState(0);
  const qs = useMemo(() => questionsFor(city, l, periodId, attempt), [city, l, periodId, attempt]);
  const [k, setK] = useState(0);
  const [chosen, setChosen] = useState<number | null>(null);
  const [score, setScore] = useState(0);
  const [laurels, setLaurels] = useState<Laurels>(readLaurels);
  if (!qs.length) return <p className="codex__quiet">No questions for this place yet.</p>;
  if (k >= qs.length)
    return (
      <div className="quiz quiz--done">
        <div className="quiz__laurel" aria-hidden="true">
          {score === qs.length ? "❦" : "✦"}
        </div>
        <p className="quiz__result">
          {score} of {qs.length} right{score === qs.length ? ": a laurel for you." : "."}
        </p>
        <p className="codex__quiet">
          All told: {laurels.right} of {laurels.asked} answered right, {laurels.found} places found on the map.
        </p>
        <button
          className="btn"
          onClick={() => {
            setAttempt((a) => a + 1);
            setK(0);
            setScore(0);
            setChosen(null);
          }}
        >
          Ask me again
        </button>
      </div>
    );
  const q = qs[k];
  const answer = (i: number) => {
    if (chosen !== null) return;
    setChosen(i);
    const right = i === q.answer;
    if (right) setScore((s) => s + 1);
    setLaurels(addLaurels({ asked: 1, right: right ? 1 : 0 }));
  };
  return (
    <div className="quiz">
      <div className="quiz__count">
        Question {k + 1} of {qs.length}
      </div>
      <p className="quiz__prompt">{q.prompt}</p>
      <ol className="quiz__options">
        {q.options.map((o, i) => (
          <li key={i}>
            <button
              className={chosen === null ? "" : i === q.answer ? "is-right" : i === chosen ? "is-wrong" : "is-dim"}
              onClick={() => answer(i)}
              disabled={chosen !== null}
            >
              <span className="quiz__letter">{"ABCD"[i]}</span>
              {o}
            </button>
          </li>
        ))}
      </ol>
      {chosen !== null && (
        <div className="quiz__explain">
          <strong>{chosen === q.answer ? "Rightly answered." : "Not quite."}</strong> {q.explain}
          <div>
            <button className="btn btn--primary" onClick={() => (setK(k + 1), setChosen(null))}>
              {k + 1 < qs.length ? "Next question" : "See the result"}
            </button>
          </div>
        </div>
      )}
    </div>
  );
}

/* ================================================================== map hunt */

function Hunt({ city }: { city: City }) {
  const periodId = useStore((s) => s.periodId) ?? city.defaultPeriodId;
  const focusedId = useStore((s) => s.focusedId);
  const [open, setOpen] = useState(false);
  const [attempt, setAttempt] = useState(0);
  const seen = useRef(new Set<string>());
  const [riddle, setRiddle] = useState<Riddle | null>(null);
  const [state, setState] = useState<{ kind: "ask" | "found" | "miss"; text?: string }>({ kind: "ask" });
  const [hint, setHint] = useState(false);
  const [laurels, setLaurels] = useState<Laurels>(readLaurels);

  const next = () => {
    let r = riddleFor(city, periodId, seen.current, attempt + 1);
    if (!r) {
      seen.current.clear();
      r = riddleFor(city, periodId, seen.current, attempt + 1);
    }
    setAttempt((a) => a + 1);
    setRiddle(r);
    setHint(false);
    setState({ kind: "ask" });
  };
  // a new era: the old riddle may not stand any more
  useEffect(() => {
    if (open && riddle && !city.landmarks.find((l) => l.id === riddle.landmarkId)?.activePeriods.includes(periodId)) next();
    // eslint-disable-next-line react-hooks/exhaustive-deps
  }, [periodId]);
  // the answer is a click on the map
  const lastFocus = useRef<string | null>(null);
  useEffect(() => {
    if (!open || !riddle || !focusedId || focusedId === lastFocus.current || state.kind === "found") {
      lastFocus.current = focusedId;
      return;
    }
    lastFocus.current = focusedId;
    if (focusedId === riddle.landmarkId) {
      seen.current.add(riddle.landmarkId);
      setLaurels(addLaurels({ found: 1 }));
      setState({ kind: "found" });
    } else {
      const there = landmarkById(city, focusedId);
      setState({ kind: "miss", text: `That is the ${there ? resolveVariant(there, periodId).name : "wrong place"}. The one you seek lies ${bearing(city, focusedId, riddle.landmarkId)} of it.` });
    }
    // eslint-disable-next-line react-hooks/exhaustive-deps
  }, [focusedId]);

  if (!open)
    return (
      <button
        className="hunt hunt--closed"
        data-hud-block
        onClick={() => {
          setOpen(true);
          if (!riddle) next();
        }}
      >
        <span className="hunt__seal" aria-hidden="true">
          Q
        </span>
        <span>
          <span className="hunt__latin">Quaestio</span>
          Find it on the map
        </span>
        {laurels.found > 0 && <span className="hunt__score">{laurels.found} found</span>}
      </button>
    );
  const target = riddle ? landmarkById(city, riddle.landmarkId) : null;
  return (
    <section className="hunt" data-hud-block aria-label="Find it on the map">
      <header className="hunt__head">
        <span className="hunt__latin">Quaestio · find it on the map</span>
        <button className="hunt__close" onClick={() => setOpen(false)} aria-label="Close">
          ×
        </button>
      </header>
      {!riddle ? (
        <p>Every place standing in this era has been found. Try another era.</p>
      ) : state.kind === "found" ? (
        <>
          <p className="hunt__riddle">
            Found: the <strong>{target ? resolveVariant(target, periodId).name : ""}</strong>.
          </p>
          <div className="hunt__actions">
            <button className="btn btn--primary" onClick={next}>
              Next riddle
            </button>
            <span className="hunt__score">{laurels.found} found</span>
          </div>
        </>
      ) : (
        <>
          <p className="hunt__riddle">{riddle.text}</p>
          {state.kind === "miss" && <p className="hunt__miss">{state.text}</p>}
          {hint && <p className="hunt__hint">{riddle.hint}</p>}
          <div className="hunt__actions">
            {!hint && (
              <button className="btn" onClick={() => setHint(true)}>
                A hint
              </button>
            )}
            <button className="btn btn--ghost" onClick={next}>
              Skip
            </button>
            <span className="hunt__score">{laurels.found} found</span>
          </div>
          <p className="hunt__how">Click a building on the map to answer.</p>
        </>
      )}
    </section>
  );
}
