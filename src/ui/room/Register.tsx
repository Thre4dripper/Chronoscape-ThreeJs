import { useEffect, useMemo, useRef, useState } from "react";
import { atlasCatalog } from "@/content/registry";
import type { Atlas, AtlasMap } from "@/content/schema";
import { readRegister, useNav } from "@/nav";
import { readLaurels } from "@/engine/codex";
import { useRoom } from "./roomState";

/**
 * The visitors' register, opened: a book whose first page is your journeys
 * (maps unfolded, atlases opened, laurels from the quizzes and the map hunt,
 * all kept in this browser) and every page after it a curiosity from the
 * atlases, two to a spread. Turning a leaf carries its page over the spine,
 * its back becoming the new left page; click fast and several leaves are in
 * the air at once, landing one after another.
 */
type Curio = { a: Atlas; m: AtlasMap };
type Leaf = { id: number; from: number; dir: 1 | -1 };

export function Register() {
  const open = useRoom((s) => s.register);
  const close = () => useRoom.getState().setRegister(false);
  const log = useMemo(() => (open ? readRegister() : { travels: [], atlases: [] }), [open]);
  const laurels = useMemo(() => (open ? readLaurels() : { asked: 0, right: 0, found: 0 }), [open]);
  const all = useMemo<Curio[]>(() => atlasCatalog.atlases.flatMap((a) => a.maps.map((m) => ({ a, m }))), []);
  // your travels, a curiosity on every page after, and an endpaper if the last spread needs one
  const pages = 1 + all.length + ((1 + all.length) % 2);
  const spreads = pages / 2;
  // the spread asked for, the spread the landed leaves show, and the leaves still turning
  const [target, setTarget] = useState(0);
  const [settled, setSettled] = useState(0);
  const [leaves, setLeaves] = useState<Leaf[]>([]);
  const ids = useRef(0);
  useEffect(() => {
    if (!open) return;
    setTarget(0);
    setSettled(0);
    setLeaves([]);
  }, [open]);
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
  const turn = (d: 1 | -1) => {
    const to = target + d;
    if (to < 0 || to >= spreads) return;
    setTarget(to);
    if (matchMedia("(max-width: 720px), (prefers-reduced-motion: reduce)").matches) {
      setLeaves([]);
      setSettled(to);
      return;
    }
    // turning back the other way: the leaves still in the air land at once
    const reversing = leaves.length > 0 && leaves[0].dir !== d;
    if (reversing) setSettled(target);
    setLeaves((ls) => [...(reversing ? [] : ls), { id: ++ids.current, from: target, dir: d }]);
  };
  const land = (leaf: Leaf) => {
    setLeaves((ls) => ls.filter((l) => l.id !== leaf.id));
    setSettled(leaf.from + leaf.dir);
  };
  if (!open) return null;

  const page = (i: number) => {
    if (i === 0) return <TravelsPage log={log} laurels={laurels} close={close} />;
    if (i <= all.length) return <CurioPage cur={all[i - 1]} close={close} />;
    return <EndPage />;
  };
  // under leaves turning forward the left page is the last one landed and the right the one being turned to; backward, the other way round
  const forward = (leaves[0]?.dir ?? 1) > 0;
  const left = 2 * (forward ? settled : target);
  const right = 2 * (forward ? target : settled) + 1;
  return (
    <div className="register" role="dialog" aria-label="The visitors' register" onClick={close}>
      <div className="register__book" onClick={(e) => e.stopPropagation()}>
        <section className="register__page register__page--left">
          {page(left)}
          <Folio n={left} />
        </section>
        <section className="register__page register__page--right">
          {page(right)}
          <Folio n={right} />
        </section>
        <div className="register__leaves" aria-hidden="true">
          {leaves.map((l) => {
            // forward, the leaf is the right page leaving; backward, the left page coming back
            const front = l.dir > 0 ? 2 * l.from + 1 : 2 * l.from - 1;
            return (
              <div key={l.id} className={`register__leaf register__leaf--${l.dir > 0 ? "next" : "prev"}`} onAnimationEnd={(e) => e.target === e.currentTarget && land(l)}>
                <section className="register__page register__page--right register__leaf-front">
                  {page(front)}
                  <Folio n={front} />
                  <div className="register__shade" />
                </section>
                <section className="register__page register__page--left register__leaf-back">
                  {page(front + 1)}
                  <Folio n={front + 1} />
                  <div className="register__shade" />
                </section>
              </div>
            );
          })}
        </div>
        <button className="register__turn register__turn--prev" onClick={() => turn(-1)} disabled={target === 0} aria-label="Turn back a page">
          ‹
        </button>
        <button className="register__turn register__turn--next" onClick={() => turn(1)} disabled={target === spreads - 1} aria-label="Turn the page">
          ›
        </button>
        <button className="register__close" onClick={close} aria-label="Close the register">
          ×
        </button>
      </div>
    </div>
  );
}

const Folio = ({ n }: { n: number }) => <div className="register__folio">{n + 1}</div>;

/** The first page: where you have been, what you have won, and the atlases still to open. */
function TravelsPage({ log, laurels, close }: { log: ReturnType<typeof readRegister>; laurels: ReturnType<typeof readLaurels>; close: () => void }) {
  const opened = log.atlases.filter((id) => atlasCatalog.atlases.some((a) => a.id === id));
  const unseen = atlasCatalog.atlases.filter((a) => !log.atlases.includes(a.id));
  return (
    <>
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
        <p className="register__quiet">No maps unfolded yet. Take an atlas from the shelf and unfold one of its maps to begin.</p>
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
    </>
  );
}

/** A page with one curiosity, and the way to its atlas. */
function CurioPage({ cur, close }: { cur: Curio; close: () => void }) {
  return (
    <>
      <div className="register__kicker">Curiosum · {cur.a.era}</div>
      <h2>{cur.m.title}</h2>
      <div className="register__sub">{cur.m.subtitle}</div>
      <p className="register__text">{cur.m.blurb}</p>
      <p className="register__from">
        From the atlas <i style={{ color: cur.a.color }}>{cur.a.title}</i>.
      </p>
      <button className="btn btn--primary register__open" onClick={() => (close(), useNav.getState().openAtlas(cur.a.id))}>
        {cur.m.city ? "Open its atlas to unfold it" : "Open its atlas"}
      </button>
    </>
  );
}

function EndPage() {
  return <div className="register__finis">Finis</div>;
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
