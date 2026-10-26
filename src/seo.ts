import { useEffect } from "react";
import { atlasCatalog } from "./content/registry";
import { useStore } from "./engine/store";
import { useNav } from "./nav";

/**
 * Per-page title, description, canonical link and social-card tags. The site
 * is one page that changes with the URL (title page, map room, an atlas, a city
 * in an era, a monument), so the head follows the view.
 */
const SITE = "Chronoscape";
const DEFAULT_DESC =
  "An illustrated atlas of the world's cities through time: unfold a hand-drawn map of Rome, Delhi, Kyoto, Tenochtitlan and 30 more cities, turn the ages, and watch temples, palaces and streets rise in 3D.";

type Seo = { title: string; description: string; image?: string };

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
  const img = new URL(image ?? "/apple-touch-icon.png", location.origin).href;
  meta("property", "og:image", img);
  meta("name", "twitter:image", img);
  meta("name", "twitter:card", image ? "summary_large_image" : "summary");
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
      if (a)
        return apply({
          title: `${a.title}, ${a.era} · ${SITE}`,
          description: `${a.blurb} Maps in this atlas: ${a.maps.map((m) => `${m.title} (${m.subtitle})`).join("; ")}.`,
        });
      return apply({
        title: `The Map Room · ${SITE}`,
        description: `Twelve atlases of the world's cities through time, from the Nile and Mesopotamia to Edo and the Andes: ${atlasCatalog.atlases.map((x) => x.title).join(", ")}.`,
      });
    }
    if (view === "city" && city) {
      const p = city.periods.find((x) => x.id === periodId) ?? city.periods.find((x) => x.id === city.defaultPeriodId)!;
      const lm = focusedId ? city.landmarks.find((l) => l.id === focusedId) : null;
      const image = `/plates/${city.id}/${p.id}.preview.webp`;
      if (lm) {
        const name = lm.variants[p.id]?.name ?? lm.name;
        return apply({ title: `${name} · ${city.name}, ${fmt(p.year)} · ${SITE}`, description: `${lm.summary} ${lm.variants[p.id]?.note ?? ""}`.trim(), image });
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
