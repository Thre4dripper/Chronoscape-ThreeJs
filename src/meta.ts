import type { AtlasCatalog, City } from "@/content/schema";

/**
 * Every page of the site, its address, and what a search engine or a link preview should say about it.
 *
 * One source for both sides: the app uses it to keep the address bar and the head current as the visitor
 * moves around, and the build (scripts/build-pages.ts) uses it to bake a real HTML file per page, with the
 * title, description, keywords, picture and structured data already in its head, for crawlers and link
 * previews that never run the app.
 *
 *   /                          the title page
 *   /atlases/                  the map room
 *   /atlases/<atlas>/          an atlas taken off the shelf
 *   /<city>/                   a city, at its usual era
 *   /<city>/<era>/             a city at an era (every map in every atlas is one of these)
 *   /<city>/<monument>/        a monument (one page for all its eras; ?period=<era> shows another one)
 *
 * Era and monument ids never collide within a city (scripts/build-pages.ts checks), so a city's second path
 * segment is whichever of the two it names.
 */
export type Route =
  | { view: "title" }
  | { view: "room"; atlasId: string | null }
  | { view: "city"; city: string; period?: string | null; landmark?: string | null };

export const SITE = "Chronoscape";
export const TAGLINE = "An illustrated atlas of the world's cities through time";
const HOME_DESC =
  "An illustrated atlas of the world's cities through time: unfold a hand-drawn map of Rome, Delhi, Kyoto, Tenochtitlan and 32 more cities, turn the ages, and watch temples, palaces and streets rise in 3D.";

export type PageImage = { src: string; alt: string; w?: number; h?: number };
export type PageMeta = {
  path: string;
  title: string;
  /** For search results (about 160 characters). */
  description: string;
  /** For link previews, which show more. */
  shareDescription: string;
  keywords: string[];
  image: PageImage;
  jsonLd: Record<string, unknown>;
};
/** A monument's first picture from its codex (media/<city>/index.json). */
export type Picture = { src: string; w: number; h: number; caption?: string };

const CARD = { w: 1200, h: 630 };
export const cardOf = (city: string, period: string) => `/plates/${city}/${period}.card.jpg`;
export const atlasCardOf = (atlas: string) => `/plates/_atlas/${atlas}.card.jpg`;

export const fmtYear = (y: number) => (y < 0 ? `${-y} BCE` : `${y} CE`);

/** The era a monument's page shows by default: the city's usual era if it stood then, else its last. */
export function monumentEra(city: City, landmarkId: string): string | null {
  const lm = city.landmarks.find((l) => l.id === landmarkId);
  if (!lm || !lm.activePeriods.length) return null;
  return lm.activePeriods.includes(city.defaultPeriodId) ? city.defaultPeriodId : lm.activePeriods[lm.activePeriods.length - 1];
}

export function pathFor(r: Route, city?: City | null): string {
  if (r.view === "title") return "/";
  if (r.view === "room") return r.atlasId ? `/atlases/${r.atlasId}/` : "/atlases/";
  if (r.landmark) {
    const usual = city ? monumentEra(city, r.landmark) : null;
    return `/${r.city}/${r.landmark}/` + (r.period && usual && r.period !== usual ? `?period=${r.period}` : "");
  }
  return r.period ? `/${r.city}/${r.period}/` : `/${r.city}/`;
}

/** The address bar, read back: the city's second segment is resolved against its pack once it has loaded. */
export function parsePath(pathname: string): { view: "title" } | { view: "room"; atlasId: string | null } | { view: "city"; city: string; segment: string | null } {
  const seg = pathname.split("/").filter(Boolean).map(decodeURIComponent);
  if (!seg.length) return { view: "title" };
  if (seg[0] === "atlases") return { view: "room", atlasId: seg[1] ?? null };
  return { view: "city", city: seg[0], segment: seg[1] ?? null };
}

const clip = (s: string, n: number) => (s.length <= n ? s : s.slice(0, n - 1).replace(/[\s,;:.]+\S*$/, "") + "…");
const uniq = (xs: string[]) => [...new Set(xs.filter(Boolean))];

export function metaFor(r: Route, ctx: { atlases: AtlasCatalog; city?: City | null; picture?: Picture | null }): PageMeta {
  const page = (path: string, title: string, desc: string, keywords: string[], image: PageImage, jsonLd: Record<string, unknown>): PageMeta => ({
    path,
    title,
    description: clip(desc, 160),
    shareDescription: clip(desc, 300),
    keywords: uniq([...keywords, "historical atlas", "illustrated map", "history", SITE]),
    image: { ...image, alt: clip(image.alt, 125) },
    jsonLd: { "@context": "https://schema.org", ...jsonLd },
  });
  const home: PageImage = { src: "/og/home.jpg", alt: "The Chronoscape title page: an old world map with the title plaque and a procession of travellers", ...CARD };
  const room: PageImage = { src: "/og/room.jpg", alt: "The map room: a cabinet of twelve atlases, a globe and framed city views", ...CARD };

  if (r.view === "room" && r.atlasId) {
    const a = ctx.atlases.atlases.find((x) => x.id === r.atlasId);
    if (a) {
      const cities = uniq(a.maps.map((m) => m.title));
      return page(
        pathFor(r),
        `${a.title}, ${a.era} · ${SITE}`,
        `${a.blurb} Maps in this atlas: ${a.maps.map((m) => `${m.title} (${m.subtitle})`).join("; ")}.`,
        [a.title, a.region, a.era, ...cities, ...a.themes.map((t) => t)],
        { src: atlasCardOf(a.id), alt: `${a.title}: illustrated maps of ${cities.join(", ")}`, ...CARD },
        { "@type": "CollectionPage", name: a.title, description: a.blurb, about: cities.map((name) => ({ "@type": "City", name })) },
      );
    }
  }
  if (r.view === "room")
    return page(
      "/atlases/",
      `The Map Room · ${SITE}`,
      `Twelve atlases of the world's cities through time, from the Nile and Mesopotamia to Edo and the Andes: ${ctx.atlases.atlases.map((x) => x.title).join(", ")}.`,
      ctx.atlases.atlases.map((x) => x.title),
      room,
      { "@type": "CollectionPage", name: "The Map Room", description: "Twelve atlases of the world's cities through time." },
    );

  if (r.view === "city" && ctx.city) {
    const city = ctx.city;
    const lm = r.landmark ? city.landmarks.find((l) => l.id === r.landmark) : null;
    if (lm) {
      const era = (r.period && lm.activePeriods.includes(r.period) ? r.period : monumentEra(city, lm.id)) ?? city.defaultPeriodId;
      const p = city.periods.find((x) => x.id === era)!;
      const name = lm.variants[p.id]?.name ?? lm.name;
      const eras = lm.activePeriods.map((id) => city.periods.find((x) => x.id === id)).filter(Boolean).map((x) => `${x!.label} (${fmtYear(x!.year)})`);
      const pic = ctx.picture;
      return page(
        pathFor({ view: "city", city: city.id, landmark: lm.id }, city),
        `${name}, ${city.name} · ${SITE}`,
        `${lm.summary} Shown on the map of ${city.name} in ${eras.length > 1 ? `${eras.length} eras, from ${eras[0]} to ${eras[eras.length - 1]}` : eras[0] ?? fmtYear(p.year)}.`,
        [lm.name, name, `${lm.name} ${city.name}`, city.name, `history of ${city.name}`, lm.category, ...(lm.function ? [lm.function.split(/[;,.]/)[0]] : [])],
        pic ? { src: `/${pic.src.replace(/^\//, "")}`, alt: pic.caption || `${name}, ${city.name}`, w: pic.w, h: pic.h } : { src: cardOf(city.id, p.id), alt: `${name} on the illustrated map of ${city.name}, ${fmtYear(p.year)}`, ...CARD },
        {
          "@type": "LandmarksOrHistoricalBuildings",
          name: lm.name,
          description: lm.summary,
          containedInPlace: { "@type": "City", name: city.name },
          ...(pic ? { image: `/${pic.src.replace(/^\//, "")}` } : {}),
        },
      );
    }
    const p = city.periods.find((x) => x.id === r.period) ?? city.periods.find((x) => x.id === city.defaultPeriodId)!;
    const standing = city.landmarks.filter((l) => l.activePeriods.includes(p.id));
    const top = standing.slice(0, 8).map((l) => l.variants[p.id]?.name ?? l.name);
    return page(
      // /<city>/ shows the usual era, so that era's page is the one address search engines keep
      pathFor({ view: "city", city: city.id, period: p.id }),
      `${city.name} in ${fmtYear(p.year)}: ${p.label} · ${SITE}`,
      `${p.summary} Explore ${standing.length} monuments of ${city.name} in ${fmtYear(p.year)} on an illustrated map${top.length ? `, among them ${top.slice(0, 4).join(", ")}` : ""}.`,
      [city.name, `${city.name} ${fmtYear(p.year)}`, `${city.name} ${p.label}`, `map of ${city.name}`, `history of ${city.name}`, city.subtitle, ...top],
      { src: cardOf(city.id, p.id), alt: `Illustrated map of ${city.name} in ${fmtYear(p.year)}: ${p.label}`, ...CARD },
      {
        "@type": "Map",
        name: `${city.name} in ${fmtYear(p.year)}: ${p.label}`,
        description: p.summary,
        temporalCoverage: `${p.startYear}/${p.endYear}`,
        about: { "@type": "City", name: city.name },
      },
    );
  }

  return page("/", `${SITE} · ${TAGLINE}`, HOME_DESC, ["historical maps", "ancient cities", "world history", "3D city reconstruction"], home, {
    "@type": "WebSite",
    name: SITE,
    description: HOME_DESC,
  });
}
