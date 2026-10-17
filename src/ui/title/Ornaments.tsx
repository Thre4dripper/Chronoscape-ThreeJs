/** Engraved ornaments in SVG: frame corners, a rule with a star, and small emblems for the title page. */

export function Corner({ className }: { className?: string }) {
  return (
    <svg className={className} viewBox="0 0 120 120" aria-hidden="true">
      <g fill="none" stroke="currentColor" strokeLinecap="round">
        <path d="M6 114 V30 Q6 6 30 6 H114" strokeWidth="2.2" />
        <path d="M14 114 V36 Q14 14 36 14 H114" strokeWidth="1" />
        <path d="M24 60 C24 34 34 24 60 24" strokeWidth="1.4" />
        <path d="M30 86 C40 70 30 52 46 46 C52 44 58 48 56 54 C54 60 46 58 48 52" strokeWidth="1.2" />
        <path d="M86 30 C70 40 52 30 46 46" strokeWidth="1.2" />
        <path d="M36 36 L54 54" strokeWidth="1" />
      </g>
      <circle cx="30" cy="30" r="5" fill="currentColor" />
      <circle cx="30" cy="30" r="9" fill="none" stroke="currentColor" strokeWidth="1" />
      <path d="M44 44 l6 -2 l-2 6 z" fill="currentColor" />
    </svg>
  );
}

export function Rule({ className }: { className?: string }) {
  return (
    <svg className={className} viewBox="0 0 420 28" aria-hidden="true">
      <g stroke="currentColor" fill="none" strokeLinecap="round">
        <path d="M10 14 H170" strokeWidth="1.2" />
        <path d="M250 14 H410" strokeWidth="1.2" />
        <path d="M60 10 H170 M250 18 H360" strokeWidth="0.6" />
        <path d="M170 14 C184 2 196 26 210 14 C224 2 236 26 250 14" strokeWidth="1.3" />
      </g>
      <g fill="currentColor">
        <path d="M210 2 L213 11 L222 14 L213 17 L210 26 L207 17 L198 14 L207 11 Z" />
        <circle cx="10" cy="14" r="2.4" />
        <circle cx="410" cy="14" r="2.4" />
      </g>
    </svg>
  );
}

/** Small engraved emblems for the four "how it works" medallions. */
export function Emblem({ kind }: { kind: "rise" | "ages" | "codex" | "hunt" }) {
  const common = { fill: "none", stroke: "currentColor", strokeWidth: 1.6, strokeLinecap: "round" as const, strokeLinejoin: "round" as const };
  return (
    <svg viewBox="0 0 48 48" aria-hidden="true" className="emblem">
      {kind === "rise" && (
        <g {...common}>
          <path d="M6 38 L24 30 L42 38 L24 46 Z" />
          <path d="M14 34 V20 L24 14 L34 20 V34" />
          <path d="M14 20 L24 26 L34 20 M24 26 V40" />
          <path d="M24 4 V10 M20 7 L24 3 L28 7" />
        </g>
      )}
      {kind === "ages" && (
        <g {...common}>
          <circle cx="24" cy="24" r="17" />
          <path d="M24 12 V24 L32 29" />
          <path d="M7 24 H4 M44 24 H41 M24 7 V4 M24 44 V41" />
          <path d="M11 11 L9 9 M37 37 L39 39 M37 11 L39 9 M11 37 L9 39" />
        </g>
      )}
      {kind === "codex" && (
        <g {...common}>
          <path d="M6 10 C14 7 20 8 24 12 C28 8 34 7 42 10 V38 C34 35 28 36 24 40 C20 36 14 35 6 38 Z" />
          <path d="M24 12 V40" />
          <path d="M11 17 C15 16 18 16 20 18 M11 23 C15 22 18 22 20 24 M28 18 C30 16 33 16 37 17 M28 24 C30 22 33 22 37 23" />
        </g>
      )}
      {kind === "hunt" && (
        <g {...common}>
          <circle cx="21" cy="21" r="12" />
          <path d="M30 30 L42 42" strokeWidth="3" />
          <path d="M21 13 L23 19 L29 21 L23 23 L21 29 L19 23 L13 21 L19 19 Z" />
        </g>
      )}
    </svg>
  );
}
