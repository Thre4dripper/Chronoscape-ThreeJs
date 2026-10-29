/**
 * Bake one HTML file per page into dist, each with its own head: title, description, keywords, canonical link,
 * social-card tags and structured data, from the same metaFor the app uses (src/meta.ts). Link previews and
 * crawlers that never run the app read these; the body is the same app shell everywhere, and the app takes over
 * from the address. Also writes sitemap.xml and robots.txt.
 *
 *   pnpm build                      (runs this last)
 *   tsx scripts/build-pages.ts      (on an existing dist)
 *
 * SITE_URL (required) is the site's public address, e.g. https://chronoscape.example: canonical links, share
 * images and the sitemap must be absolute, and a build has no request to read its own address from. Set it in
 * .env for local builds (see .env.example) and as the repository variable SITE_URL for GitHub Actions.
 */
import { existsSync, mkdirSync, readdirSync, readFileSync, writeFileSync } from "node:fs";
import { join, resolve } from "node:path";
import { AtlasCatalogSchema, type City } from "../src/content/schema";
import { validateCity } from "../src/content/validate";
import { metaFor, pathFor, type PageMeta, type Picture, type Route } from "../src/meta";

const ROOT = resolve(import.meta.dirname, "..");
const DIST = join(ROOT, "dist");
if (existsSync(join(ROOT, ".env"))) process.loadEnvFile(join(ROOT, ".env"));
const SITE_URL = (process.env.SITE_URL ?? "").trim().replace(/\/$/, "");
if (!/^https?:\/\/[^/]+$/.test(SITE_URL)) {
  console.error(`pages: SITE_URL must be the site's address, like https://chronoscape.example (got "${process.env.SITE_URL ?? ""}"). Set it in .env, or as the SITE_URL repository variable in CI.`);
  process.exit(1);
}

const shell = readFileSync(join(DIST, "index.html"), "utf8");
const OPEN = shell.indexOf("<!-- seo"), CLOSE = shell.indexOf("<!-- /seo -->");
if (OPEN < 0 || CLOSE < 0) throw new Error("index.html has no <!-- seo --> … <!-- /seo --> block");

const esc = (s: string) => s.replace(/&/g, "&amp;").replace(/"/g, "&quot;").replace(/</g, "&lt;").replace(/>/g, "&gt;");
const abs = (p: string) => (/^https?:/.test(p) ? p : SITE_URL + (p.startsWith("/") ? p : `/${p}`));

function head(m: PageMeta) {
  const url = abs(m.path), img = abs(m.image.src);
  const tags = [
    `<title>${esc(m.title)}</title>`,
    `<meta name="description" content="${esc(m.description)}" />`,
    `<meta name="keywords" content="${esc(m.keywords.join(", "))}" />`,
    `<link rel="canonical" href="${esc(url)}" />`,
    `<meta property="og:url" content="${esc(url)}" />`,
    `<meta property="og:title" content="${esc(m.title)}" />`,
    `<meta property="og:description" content="${esc(m.shareDescription)}" />`,
    `<meta property="og:image" content="${esc(img)}" />`,
    ...(m.image.w && m.image.h ? [`<meta property="og:image:width" content="${m.image.w}" />`, `<meta property="og:image:height" content="${m.image.h}" />`] : []),
    `<meta property="og:image:alt" content="${esc(m.image.alt)}" />`,
    `<meta name="twitter:card" content="summary_large_image" />`,
    `<meta name="twitter:title" content="${esc(m.title)}" />`,
    `<meta name="twitter:description" content="${esc(m.shareDescription)}" />`,
    `<meta name="twitter:image" content="${esc(img)}" />`,
    `<meta name="twitter:image:alt" content="${esc(m.image.alt)}" />`,
    // (a "</" inside the JSON would end the script element early)
    `<script type="application/ld+json">${JSON.stringify({ ...m.jsonLd, url, ...(m.jsonLd.image ? { image: abs(String(m.jsonLd.image)) } : { image: img }) }).replace(/<\//g, "<\\/")}</script>`,
  ];
  return "<!-- seo -->\n    " + tags.join("\n    ") + "\n    ";
}

const written = new Map<string, PageMeta>();
function page(at: string, m: PageMeta) {
  const html = shell.slice(0, OPEN) + head(m) + shell.slice(CLOSE);
  const dir = join(DIST, ...at.split("/").filter(Boolean));
  mkdirSync(dir, { recursive: true });
  writeFileSync(join(dir, "index.html"), html);
  written.set(at, m);
}

const atlases = AtlasCatalogSchema.parse(JSON.parse(readFileSync(join(ROOT, "content/atlases.json"), "utf8")));
const ids: string[] = JSON.parse(readFileSync(join(ROOT, "content/cities/index.json"), "utf8")).cities.map((c: { id: string }) => c.id);
const reserved = new Set(["atlases", "assets", "plates", "models", "media", "og", "fonts", "draco", "room", "title", "world"]);

const all = (r: Route, city?: City | null, picture?: Picture | null) => metaFor(r, { atlases, city, picture });

page("/", all({ view: "title" }));
page("/atlases/", all({ view: "room", atlasId: null }));
for (const a of atlases.atlases) page(`/atlases/${a.id}/`, all({ view: "room", atlasId: a.id }));

for (const id of ids) {
  if (reserved.has(id)) throw new Error(`a city id "${id}" would shadow the site's own /${id}/ folder`);
  const { city } = validateCity(JSON.parse(readFileSync(join(ROOT, "content/cities", id, "city.json"), "utf8")));
  if (!city) throw new Error(`city ${id} failed validation`);
  const clash = city.periods.filter((p) => city.landmarks.some((l) => l.id === p.id)).map((p) => p.id);
  if (clash.length) throw new Error(`${id}: ${clash.join(", ")} is both an era and a monument: /${id}/<id>/ would be ambiguous`);
  const picsFile = join(ROOT, "assets/media", id, "index.json");
  const pics: Record<string, Picture[]> = existsSync(picsFile) ? JSON.parse(readFileSync(picsFile, "utf8")) : {};
  page(`/${id}/`, all({ view: "city", city: id }, city));
  for (const p of city.periods) page(`/${id}/${p.id}/`, all({ view: "city", city: id, period: p.id }, city));
  for (const l of city.landmarks) page(pathFor({ view: "city", city: id, landmark: l.id }, city), all({ view: "city", city: id, landmark: l.id }, city, pics[l.id]?.[0] ?? null));
}

// every picture a page names must be in the build
const missing = [...written.values()].map((m) => m.image.src).filter((src) => !existsSync(join(DIST, src)));
if (missing.length) console.warn(`pages: ${missing.length} share pictures missing from dist, e.g. ${[...new Set(missing)].slice(0, 3).join(", ")}`);

// the sitemap lists each page once, at its canonical address (/<city>/ is its usual era's page)
const canon = [...new Set([...written.values()].map((m) => m.path))];
writeFileSync(
  join(DIST, "sitemap.xml"),
  `<?xml version="1.0" encoding="UTF-8"?>\n<urlset xmlns="http://www.sitemaps.org/schemas/sitemap/0.9">\n${canon.map((p) => `  <url><loc>${esc(abs(p))}</loc></url>`).join("\n")}\n</urlset>\n`,
);
writeFileSync(join(DIST, "robots.txt"), `User-agent: *\nAllow: /\n\nSitemap: ${SITE_URL}/sitemap.xml\n`);
const files = readdirSync(DIST, { recursive: true }).filter((f) => String(f).endsWith("index.html")).length;
console.log(`pages: ${written.size} pages baked (${files} index.html files), ${canon.length} in the sitemap, for ${SITE_URL}`);
