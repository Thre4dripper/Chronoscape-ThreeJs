import { useEffect, useMemo, useRef, useState } from "react";
import { atlasCatalog } from "@/content/registry";
import { readRegister, useNav } from "@/nav";
import { readLaurels } from "@/engine/codex";
import { useRoom } from "./roomState";

/**
 * The visitors' register, opened: on the left your journeys (maps unfolded,
 * atlases opened, laurels from the quizzes and the map hunt, all kept in this
 * browser), on the right a curiosity drawn from the atlases, with the next
 * one a page-turn away.
 */
export function Register() {
  const open = useRoom((s) => s.register);
  const close = () => useRoom.getState().setRegister(false);
  const [n, setN] = useState(() => Math.floor(Math.random() * 1000));
  const [turning, setTurning] = useState(false);
  const log = useMemo(() => (open ? readRegister() : { travels: [], atlases: [] }), [open]);
  const laurels = useMemo(() => (open ? readLaurels() : { asked: 0, right: 0, found: 0 }), [open]);
  const all = useMemo(() => atlasCatalog.atlases.flatMap((a) => a.maps.map((m) => ({ a, m }))), []);
  const cur = all[n % all.length];
  const timer = useRef<number | null>(null);
  useEffect(() => {
    if (!open) return;
    const onKey = (e: KeyboardEvent) => {
      if (e.key === "Escape") {
        e.preventDefault();
        e.stopPropagation();
        close();
      } else if (e.key === "ArrowRight") turn(1);
      else if (e.key === "ArrowLeft") turn(-1);
    };
    addEventListener("keydown", onKey, true);
    return () => removeEventListener("keydown", onKey, true);
  });
  const turn = (d: number) => {
    setTurning(true);
    if (timer.current) clearTimeout(timer.current);
    timer.current = window.setTimeout(() => {
      setN((x) => x + d + all.length);
      setTurning(false);
    }, 260);
  };
  if (!open) return null;
  const opened = log.atlases.map((id) => atlasCatalog.atlases.find((a) => a.id === id)).filter(Boolean);
  const unseen = atlasCatalog.atlases.filter((a) => !log.atlases.includes(a.id));
  return (
    <div className="register" role="dialog" aria-label="The visitors' register" onClick={close}>
      <div className="register__book" onClick={(e) => e.stopPropagation()}>
        <section className="register__page register__page--left">
          <div className="register__kicker">Liber viatorum</div>
          <h2>Your travels</h2>
          {log.travels.length ? (
            <ol className="register__list">
              {log.travels.slice(0, 7).map((t) => {
                const [title, sub] = t.split("|");
                return (
                  <li key={t}>
                    <strong>{title}</strong> <em>{sub}</em>
                  </li>
                );
              })}
            </ol>
          ) : (
            <p className="register__quiet">No maps unfolded yet. The drawer of ready maps, under the shelf, is a good place to begin.</p>
          )}
          <div className="register__tally">
            <span>
              <b>{opened.length}</b> of {atlasCatalog.atlases.length} atlases opened
            </span>
            <span>
              <b>{laurels.right}</b> of {laurels.asked} questions answered right
            </span>
            <span>
              <b>{laurels.found}</b> places found on the map
            </span>
          </div>
          {unseen.length > 0 && (
            <p className="register__next">
              Not yet opened:{" "}
              {unseen.slice(0, 4).map((a, i) => (
                <span key={a.id}>
                  {i ? ", " : ""}
                  <button onClick={() => (close(), useNav.getState().openAtlas(a.id))}>{a.title}</button>
                </span>
              ))}
              {unseen.length > 4 ? "…" : "."}
            </p>
          )}
        </section>
        <section className={`register__page register__page--right ${turning ? "is-turning" : ""}`}>
          <div className="register__kicker">Curiosum · {cur.a.era}</div>
          <h2>{cur.m.title}</h2>
          <div className="register__sub">{cur.m.subtitle}</div>
          <p className="register__text">{cur.m.blurb}</p>
          <p className="register__from">
            From the atlas <i style={{ color: cur.a.color }}>{cur.a.title}</i>.
          </p>
          <div className="register__actions">
            <button className="btn" onClick={() => turn(-1)} aria-label="Previous curiosity">
              ‹
            </button>
            <button className="btn btn--primary" onClick={() => (close(), useNav.getState().openAtlas(cur.a.id))}>
              {cur.m.city ? "Open its atlas to unfold it" : "Open its atlas"}
            </button>
            <button className="btn" onClick={() => turn(1)} aria-label="Next curiosity">
              ›
            </button>
          </div>
        </section>
        <button className="register__close" onClick={close} aria-label="Close the register">
          ×
        </button>
      </div>
    </div>
  );
}

/** The label that follows the pointer over things in the room. */
export function RoomTip() {
  const tip = useRoom((s) => s.tip);
  const el = useRef<HTMLDivElement>(null);
  useEffect(() => {
    const move = (e: PointerEvent) => {
      const d = el.current;
      if (!d) return;
      const w = d.offsetWidth, h = d.offsetHeight;
      const x = e.clientX + 18 + w > innerWidth - 8 ? e.clientX - w - 14 : e.clientX + 18;
      const y = e.clientY + 20 + h > innerHeight - 8 ? e.clientY - h - 12 : e.clientY + 20;
      d.style.transform = `translate3d(${x}px, ${y}px, 0)`;
    };
    addEventListener("pointermove", move, { passive: true });
    return () => removeEventListener("pointermove", move);
  }, []);
  return (
    <div className="room-tip" ref={el} aria-hidden={!tip}>
      {tip && (
        <div className="room-tip__card" key={tip.title}>
          <strong>{tip.title}</strong>
          {tip.text && <span>{tip.text}</span>}
          {tip.hint && <em>{tip.hint}</em>}
        </div>
      )}
    </div>
  );
}
