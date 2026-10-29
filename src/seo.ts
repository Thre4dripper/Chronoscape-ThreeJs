import { useEffect } from "react";
import { atlasCatalog } from "./content/registry";
import { loadPictures } from "./engine/codex";
import { useStore } from "./engine/store";
import { useNav } from "./nav";

/**
 * Per-page title, description, canonical link and social-card tags. The site
 * is one page that changes with the URL (title page, map room, an atlas, a city
 * in an era, a monument), so the head follows the view. Every view has its own
 * picture: a screenshot for the title page and the map room, the atlas's first
 * map, the city's map in that era, and a monument's first engraving or photo.
 */
const SITE = "Chronoscape";
const DEFAULT_DESC =
  "An illustrated atlas of the world's cities through time: unfold a hand-drawn map of Rome, Delhi, Kyoto, Tenochtitlan and 30 more cities, turn the ages, and watch temples, palaces and streets rise in 3D.";

type Image = { src: string; alt: string; w?: number; h?: number };
type Seo = { title: string; description: string; image?: Image };

const HOME: Image = { src: "/og/home.jpg", alt: "The Chronoscape title page: an old world map with the title plaque and a procession of travellers", w: 1200, h: 630 };
const ROOM: Image = { src: "/og/room.jpg", alt: "The map room: a cabinet of twelve atlases, a globe and framed city views", w: 1200, h: 630 };
const plate = (city: string, period: string, alt: string): Image => ({ src: `/plates/${city}/${period}.preview.webp`, alt });

function meta(attr: "name" | "property", key: string, content: string) {
  let el = document.head.querySelector<HTMLMetaElement>(`meta[${attr}="${key}"]`);
  if (!el) {
    el = document.createElement("meta");
    el.setAttribute(attr, key);
    document.head.appendChild(el);
  }
  el.content = content;
}

function apply({ title, description, image }: Seo) {
  document.title = title;
  const desc = description.length > 300 ? description.slice(0, 297).replace(/\s+\S*$/, "") + "…" : description;
  meta("name", "description", desc);
  meta("property", "og:title", title);
  meta("property", "og:description", desc);
  meta("property", "og:url", location.href);
  meta("name", "twitter:title", title);
  meta("name", "twitter:description", desc);
  const im = image ?? HOME;
  const img = new URL(im.src, location.origin).href;
  meta("property", "og:image", img);
  meta("property", "og:image:alt", im.alt);
  // sizes only where they are known; a stale size is worse than none
  for (const [k, v] of [["og:image:width", im.w], ["og:image:height", im.h]] as const) {
    if (v) meta("property", k, String(v));
    else document.head.querySelector(`meta[property="${k}"]`)?.remove();
  }
  meta("name", "twitter:image", img);
  meta("name", "twitter:image:alt", im.alt);
  meta("name", "twitter:card", "summary_large_image");
  let link = document.head.querySelector<HTMLLinkElement>('link[rel="canonical"]');
  if (!link) {
    link = document.createElement("link");
    link.rel = "canonical";
    document.head.appendChild(link);
  }
  link.href = location.origin + location.pathname + location.search;
}

const fmt = (y: number) => (y < 0 ? `${-y} BCE` : `${y} CE`);

export function useSeo() {
  const view = useNav((s) => s.view);
  const atlasId = useNav((s) => s.atlasId);
  const city = useStore((s) => s.city);
  const periodId = useStore((s) => s.periodId);
  const focusedId = useStore((s) => s.focusedId);
  useEffect(() => {
    if (view === "room") {
      const a = atlasId ? atlasCatalog.atlases.find((x) => x.id === atlasId) : null;
      if (a) {
        const first = a.maps.find((m) => m.city && m.period);
        return apply({
          title: `${a.title}, ${a.era} · ${SITE}`,
          description: `${a.blurb} Maps in this atlas: ${a.maps.map((m) => `${m.title} (${m.subtitle})`).join("; ")}.`,
          image: first ? plate(first.city!, first.period!, `Illustrated map of ${first.title}, ${first.subtitle}`) : ROOM,
        });
      }
      return apply({
        title: `The Map Room · ${SITE}`,
        description: `Twelve atlases of the world's cities through time, from the Nile and Mesopotamia to Edo and the Andes: ${atlasCatalog.atlases.map((x) => x.title).join(", ")}.`,
        image: ROOM,
      });
    }
    if (view === "city" && city) {
      const p = city.periods.find((x) => x.id === periodId) ?? city.periods.find((x) => x.id === city.defaultPeriodId)!;
      const lm = focusedId ? city.landmarks.find((l) => l.id === focusedId) : null;
      const image = plate(city.id, p.id, `Illustrated map of ${city.name} in ${fmt(p.year)}: ${p.label}`);
      if (lm) {
        const name = lm.variants[p.id]?.name ?? lm.name;
        const seo = { title: `${name} · ${city.name}, ${fmt(p.year)} · ${SITE}`, description: `${lm.summary} ${lm.variants[p.id]?.note ?? ""}`.trim(), image };
        apply(seo);
        // then the monument's own first picture (an engraving, a reconstruction or a photo), once the index is in
        let live = true;
        loadPictures(city.id).then((all) => {
          const pic = all?.[lm.id]?.[0];
          if (live && pic) apply({ ...seo, image: { src: `/${pic.src.replace(/^\//, "")}`, alt: pic.caption || name, w: pic.w, h: pic.h } });
        });
        return () => void (live = false);
      }
      return apply({
        title: `${city.name}: ${p.label}, ${fmt(p.year)} · ${SITE}`,
        description: `${p.summary} Explore ${city.landmarks.filter((l) => l.activePeriods.includes(p.id)).length} monuments of ${city.name} in ${fmt(p.year)} on an illustrated map.`,
        image,
      });
    }
    apply({ title: `${SITE} · An illustrated atlas of the world's cities through time`, description: DEFAULT_DESC });
  }, [view, atlasId, city, periodId, focusedId]);
}
