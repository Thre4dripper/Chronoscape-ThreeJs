import type { SpotKind } from "@/content/schema";

/** Small single-colour glyphs for the spot markers, one per kind. */
export function SpotIcon({ kind }: { kind: SpotKind }) {
  const d = GLYPHS[kind] ?? GLYPHS.shop;
  return (
    <svg viewBox="0 0 24 24" width="14" height="14" aria-hidden="true">
      <path d={d} fill="currentColor" />
    </svg>
  );
}

const GLYPHS: Record<string, string> = {
  tavern: "M6 3h12l-1 9a5 5 0 0 1-10 0L6 3zm2 2 .7 7a3 3 0 0 0 6.6 0L16 5H8zM10 17h4v2h2v2H8v-2h2v-2z",
  bakery: "M4 12a8 5 0 0 1 16 0v3H4v-3zm2 0v1h12v-1a6 3 0 0 0-12 0zM4 17h16v2H4z",
  market: "M3 9l2-5h14l2 5v2a3 3 0 0 1-6 0 3 3 0 0 1-6 0 3 3 0 0 1-6 0V9zm2 6h14v6H5v-6zm2 2v2h4v-2H7z",
  shop: "M4 4h16v3H4V4zm0 5h16l-1 11H5L4 9zm5 2v6h2v-6H9zm4 0v6h2v-6h-2z",
  workshop: "M14.7 3.3l2 2L13 9l2 2 3.7-3.7 2 2L17 13l-2-2-9 9-2-2 9-9-2-2 3.7-3.7z",
  house: "M12 3l9 8h-3v9h-5v-6h-2v6H6v-9H3l9-8z",
  inn: "M3 10h18v9H3v-9zm2 2v5h14v-5H5zm3-8h8v4H8V4zm9 15h2v2h-2zm-14 0h2v2H4z",
  school: "M12 3l10 5-10 5L2 8l10-5zm-6 9.5l6 3 6-3V17l-6 3-6-3v-4.5z",
  bath: "M5 11h14a2 2 0 0 1 2 2v2a5 5 0 0 1-5 5H8a5 5 0 0 1-5-5v-2a2 2 0 0 1 2-2zm1-7h3v6H6V4zm4 2h2v4h-2V6z",
  shrine: "M12 2l3 4h-6l3-4zM5 8h14v2H5V8zm1 3h12v8H6v-8zm2 2v4h2v-4H8zm6 0v4h2v-4h-2zM4 20h16v2H4z",
  fountain: "M12 2a4 4 0 0 1 4 4v3h-8V6a4 4 0 0 1 4-4zm-7 9h14l-2 4H7l-2-4zm2 5h10v2H7v-2zm-2 3h14v2H5v-2z",
  works: "M4 4h2v16H4V4zm14 0h2v16h-2V4zM7 7h10v2H7V7zm0 4h10v2H7v-2zm0 4h10v2H7v-2z",
  dock: "M3 15h18l-2 5H5l-2-5zm9-12l6 5h-4v5h-4V8H6l6-5z",
  prison: "M4 3h16v18H4V3zm2 2v14h2V5H6zm4 0v14h2V5h-2zm4 0v14h2V5h-2zm4 0v14h-1V5h1z",
  civic: "M12 2l10 5v2H2V7l10-5zM4 10h16v8H4v-8zm2 2v4h2v-4H6zm5 0v4h2v-4h-2zm5 0v4h2v-4h-2zM3 19h18v3H3v-3z",
  monument: "M10 2h4l1 12H9l1-12zm-3 13h10v2H7v-2zm-2 3h14v4H5v-4z",
  garden: "M12 2c3 3 3 7 0 10-3-3-3-7 0-10zm-7 7c4 0 7 3 7 7-4 0-7-3-7-7zm14 0c0 4-3 7-7 7 0-4 3-7 7-7zM11 15h2v7h-2z",
  bank: "M12 3l9 4v2H3V7l9-4zM5 10h14v7H5v-7zm2 2v3h2v-3H7zm4 0v3h2v-3h-2zm4 0v3h2v-3h-2zM3 18h18v3H3v-3z",
  church: "M11 2h2v3h3v2h-3v3h-2V7H8V5h3V2zm-5 10h12l2 10H4l2-10zm4 4v6h4v-6h-4z",
};
