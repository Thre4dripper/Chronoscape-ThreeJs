import { useEffect } from "react";
import { atlasCatalog } from "./content/registry";
import { loadPictures } from "./engine/codex";
import { useStore } from "./engine/store";
import { metaFor, type PageMeta, type Route } from "./meta";
import { useNav } from "./nav";

/**
 * Keeps the head in step with the view as the visitor moves around: title, description, keywords,
 * canonical link, social-card tags and structured data. What goes in them comes from metaFor (src/meta.ts),
 * the same source the build bakes into each page's HTML (scripts/build-pages.ts), so a page reads the same
 * whether a crawler fetched it or the visitor navigated to it.
 */
function meta(attr: "name" | "property", key: string, content: string | undefined) {
  let el = document.head.querySelector<HTMLMetaElement>(`meta[${attr}="${key}"]`);
  if (content === undefined) return el?.remove();
  if (!el) {
    el = document.createElement("meta");
    el.setAttribute(attr, key);
    document.head.appendChild(el);
  }
  el.content = content;
}

function apply(m: PageMeta) {
  const url = location.origin + m.path;
  const img = new URL(m.image.src, location.origin).href;
  document.title = m.title;
  meta("name", "description", m.description);
  meta("name", "keywords", m.keywords.join(", "));
  meta("property", "og:title", m.title);
  meta("property", "og:description", m.shareDescription);
  meta("property", "og:url", url);
  meta("property", "og:image", img);
  meta("property", "og:image:alt", m.image.alt);
  meta("property", "og:image:width", m.image.w ? String(m.image.w) : undefined);
  meta("property", "og:image:height", m.image.h ? String(m.image.h) : undefined);
  meta("name", "twitter:card", "summary_large_image");
  meta("name", "twitter:title", m.title);
  meta("name", "twitter:description", m.shareDescription);
  meta("name", "twitter:image", img);
  meta("name", "twitter:image:alt", m.image.alt);
  let link = document.head.querySelector<HTMLLinkElement>('link[rel="canonical"]');
  if (!link) {
    link = document.createElement("link");
    link.rel = "canonical";
    document.head.appendChild(link);
  }
  link.href = url;
  let ld = document.head.querySelector<HTMLScriptElement>('script[type="application/ld+json"]');
  if (!ld) {
    ld = document.createElement("script");
    ld.type = "application/ld+json";
    document.head.appendChild(ld);
  }
  ld.textContent = JSON.stringify({ ...m.jsonLd, url });
}

export function useSeo() {
  const view = useNav((s) => s.view);
  const atlasId = useNav((s) => s.atlasId);
  const city = useStore((s) => s.city);
  const periodId = useStore((s) => s.periodId);
  const focusedId = useStore((s) => s.focusedId);
  useEffect(() => {
    const route: Route = view === "room" ? { view: "room", atlasId } : view === "city" && city ? { view: "city", city: city.id, period: periodId, landmark: focusedId } : { view: "title" };
    const ctx = { atlases: atlasCatalog, city: view === "city" ? city : null };
    apply(metaFor(route, ctx));
    // a monument's card is its own first picture, once the city's picture index is in
    if (route.view !== "city" || !route.landmark || !city) return;
    let live = true;
    void loadPictures(city.id).then((all) => {
      const pic = all?.[route.landmark!]?.[0];
      if (live && pic) apply(metaFor(route, { ...ctx, picture: pic }));
    });
    return () => void (live = false);
  }, [view, atlasId, city, periodId, focusedId]);
}
