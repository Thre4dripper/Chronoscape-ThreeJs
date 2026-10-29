/**
 * Bake every period's whole-city map plate into .plate-cache/<city>/<period>.webp (and a preview), so the
 * production site shows the map at once instead of drawing it at load. Plates are build output, not source:
 * the cache is git-ignored and `pnpm build` copies it into dist/plates. Each era's plate is drawn again only
 * when what it is drawn from changes (its map features, monuments, plan images, era name, PLATE_VERSION; not
 * the prose), and cities are baked in parallel, one headless Chrome per job (PLATE_JOBS, default: cores - 2,
 * at most 8). The dev server serves the cache if it exists and draws any plate it lacks in a worker.
 *
 *   pnpm plates:bake                   # every city
 *   node scripts/bake-plates.mjs rome     # one city
 *   node scripts/bake-plates.mjs --out dist/plates   # bake what is stale, check, then copy into the build
 *   --force bakes again even if the cache is current. CHROME=/path/to/chrome overrides the browser;
 *   APP_URL=http://localhost:5173 uses a running dev server instead of starting one.
 *
 * Each era also gets a share card (<period>.card.jpg, 1200 x 630: the map with the city's name and era on it)
 * and each atlas one made of its maps (_atlas/<atlas>.card.jpg). They are the pages' pictures in link previews
 * and search results (src/meta.ts), and are cached and redrawn on the same terms as the plates.
 */
import { spawn } from "node:child_process";
import { cpSync, existsSync, mkdirSync, mkdtempSync, readFileSync, rmSync, writeFileSync } from "node:fs";
import { join, resolve } from "node:path";
import { createHash } from "node:crypto";
import { availableParallelism } from "node:os";
import { tmpdir } from "node:os";

const ROOT = resolve(import.meta.dirname, "..");
const CACHE = join(ROOT, ".plate-cache");
const PORT = +(process.env.PORT ?? 9333);
const args = process.argv.slice(2);
const flag = (f) => args.includes(f);
const outIdx = args.indexOf("--out");
const out = outIdx >= 0 ? resolve(ROOT, args[outIdx + 1]) : null;
const only = args.find((a, i) => !a.startsWith("--") && args[i - 1] !== "--out");
const cities = JSON.parse(readFileSync(join(ROOT, "content/cities/index.json"), "utf8")).cities.map((c) => c.id);

function findChrome() {
  if (process.env.CHROME) return process.env.CHROME;
  const home = process.env.HOME ?? "";
  const candidates = [
    `${home}/Applications/Google Chrome.app/Contents/MacOS/Google Chrome`,
    "/Applications/Google Chrome.app/Contents/MacOS/Google Chrome",
    "/usr/bin/google-chrome",
    "/usr/bin/google-chrome-stable",
    "/usr/bin/chromium",
    "/usr/bin/chromium-browser",
  ];
  const found = candidates.find((c) => existsSync(c));
  if (!found) throw new Error("no Chrome found: set CHROME=/path/to/chrome");
  return found;
}

/** A digest of the plan images (Blender top-down renders) an era's plate uses: re-rendered plans redraw it. */
const planManifest = existsSync(join(ROOT, "assets/models/plans/manifest.json")) ? JSON.parse(readFileSync(join(ROOT, "assets/models/plans/manifest.json"), "utf8")) : {};
function plansDigest(keys) {
  const h = createHash("sha1");
  for (const k of keys) {
    const f = join(ROOT, "assets/models/plans", `${k}.${planManifest[k]?.ext ?? "png"}`);
    h.update(k);
    if (existsSync(f)) h.update(readFileSync(f));
  }
  return h.digest("hex").slice(0, 12);
}

/** The city's cached manifest, if any. */
function cachedManifest(city) {
  const mp = join(CACHE, city, "manifest.json");
  return existsSync(mp) ? JSON.parse(readFileSync(mp, "utf8")) : null;
}

const sleep = (ms) => new Promise((r) => setTimeout(r, ms));
const hash = (s) => createHash("sha1").update(s).digest("hex").slice(0, 12);
const fmtYear = (y) => (y < 0 ? `${-y} BCE` : `${y} CE`);
/** Bump to redraw every share card (a new layout). */
const CARD_VERSION = 1;

/*
 * The share cards are drawn in the page (its fonts are the app's): a map cropped to 1200 x 630, darkened toward
 * the bottom, with a small kicker, the name and a line under it, in a thin gilt frame. An atlas card lays its
 * maps side by side instead of one map.
 */
const CARD_JS = `window.__card = async ({ srcs, kicker, title, line }) => {
  const W = 1200, H = 630;
  const c = document.createElement("canvas");
  c.width = W;
  c.height = H;
  const g = c.getContext("2d");
  g.fillStyle = "#2a1d14";
  g.fillRect(0, 0, W, H);
  const imgs = await Promise.all(srcs.map((src) => new Promise((res, rej) => { const i = new Image(); i.onload = () => res(i); i.onerror = rej; i.src = src; })));
  const cw = W / imgs.length;
  imgs.forEach((img, k) => {
    // cover each column, a little zoomed in toward the middle of the map, where the city is
    const s = Math.max(cw / img.width, H / img.height) * (imgs.length > 1 ? 1.05 : 1.12);
    const dw = img.width * s, dh = img.height * s;
    g.save();
    g.beginPath();
    g.rect(k * cw, 0, cw, H);
    g.clip();
    g.drawImage(img, k * cw + (cw - dw) / 2, (H - dh) / 2, dw, dh);
    g.restore();
    if (k) { g.fillStyle = "rgba(42,29,20,0.85)"; g.fillRect(k * cw - 2, 0, 4, H); }
  });
  const shade = g.createLinearGradient(0, H * 0.35, 0, H);
  shade.addColorStop(0, "rgba(28,19,12,0)");
  shade.addColorStop(1, "rgba(28,19,12,0.9)");
  g.fillStyle = shade;
  g.fillRect(0, 0, W, H);
  g.strokeStyle = "rgba(233,200,154,0.75)";
  g.lineWidth = 2;
  g.strokeRect(18, 18, W - 36, H - 36);
  await document.fonts.ready;
  const fam = getComputedStyle(document.documentElement).getPropertyValue("--display").trim() || "Georgia, serif";
  const text = (t, size, color, y, spacing) => {
    g.font = size + "px " + fam;
    g.letterSpacing = spacing + "px";
    // shrink a long name until it fits the frame
    let s = size;
    while (g.measureText(t).width > W - 140 && s > 24) { s -= 2; g.font = s + "px " + fam; }
    g.fillStyle = color;
    g.shadowColor = "rgba(0,0,0,0.6)";
    g.shadowBlur = 8;
    g.fillText(t, 64, y);
    g.shadowBlur = 0;
  };
  text(kicker.toUpperCase(), 20, "#e9c89a", H - 168, 7);
  text(title.toUpperCase(), 72, "#f6e9c9", H - 92, 4);
  text(line, 30, "#efe0bd", H - 50, 1);
  return c.toDataURL("image/jpeg", 0.84).split(",")[1];
};`;
let server = null;
let base = process.env.APP_URL;
if (!base) {
  const { createServer } = await import("vite");
  server = await createServer({ root: ROOT, logLevel: "error", server: { port: 5199, strictPort: false, hmr: false } });
  await server.listen();
  base = server.resolvedUrls.local[0].replace(/\/$/, "");
}
// one headless Chrome per job: each draws its plates on its own CPU core (tabs of one Chrome can share a
// renderer process, which would draw them one after another)
const JOBS = Math.max(1, Math.min(+(process.env.PLATE_JOBS ?? 0) || Math.max(1, availableParallelism() - 2), 8));
const queue = cities.filter((c) => !only || only === c);
let baked = 0, kept = 0;
const t0 = Date.now();

async function startChrome(port) {
  const profile = mkdtempSync(join(tmpdir(), "bake-"));
  const chromeArgs = ["--headless=new", `--remote-debugging-port=${port}`, `--user-data-dir=${profile}`, "--window-size=800,600"];
  if (process.env.CI) chromeArgs.push("--no-sandbox"); // CI runners forbid the sandbox's user namespaces
  const proc = spawn(findChrome(), [...chromeArgs, "about:blank"], { stdio: "ignore" });
  let list;
  for (let i = 0; i < 80 && !list; i++) {
    await sleep(250);
    list = await fetch(`http://127.0.0.1:${port}/json`).then((r) => r.json()).catch(() => null);
  }
  if (!list) throw new Error("Chrome did not start");
  const ws = new WebSocket(list.find((t) => t.type === "page").webSocketDebuggerUrl);
  await new Promise((res, rej) => {
    ws.onopen = res;
    ws.onerror = () => rej(new Error("could not connect to Chrome"));
    setTimeout(() => rej(new Error("Chrome did not accept the connection")), 20000);
  });
  let id = 0;
  const pending = new Map();
  ws.onmessage = (ev) => {
    const m = JSON.parse(ev.data);
    if (m.id && pending.has(m.id)) pending.get(m.id)(m), pending.delete(m.id);
  };
  ws.onclose = () => pending.forEach((res) => res({ result: { exceptionDetails: { exception: { description: "Chrome closed the connection" } } } }));
  // every call has a deadline: a tab that stops answering counts as a failure (and gets a fresh browser)
  // instead of holding the build forever
  const send = (method, params = {}, ms = 60000) =>
    new Promise((res, rej) => {
      const i = ++id;
      const timer = setTimeout(() => (pending.delete(i), rej(new Error(`Chrome did not answer ${method} within ${ms / 1000} s`))), ms);
      pending.set(i, (m) => (clearTimeout(timer), res(m)));
      ws.send(JSON.stringify({ id: i, method, params }));
    });
  const evalv = async (expression, ms) => {
    const r = await send("Runtime.evaluate", { expression, returnByValue: true, awaitPromise: true }, ms);
    if (r.result?.exceptionDetails) throw new Error(r.result.exceptionDetails.exception?.description);
    return r.result.result.value;
  };
  const close = () => {
    ws.close();
    proc.kill();
    // Chrome may still be writing its profile as it exits
    proc.once("exit", () => rmSync(profile, { recursive: true, force: true, maxRetries: 5, retryDelay: 200 }));
  };
  return { send, evalv, close };
}

async function bakeCity(b, city) {
  await b.send("Page.navigate", { url: `${base}/${city}/` });
  let meta = null;
  for (let i = 0; i < 240 && !meta; i++) {
    await sleep(250);
    meta = await b.evalv("window.__plateMeta ? window.__plateMeta() : null").catch(() => null);
  }
  if (!meta) throw new Error(`bake hook not found for ${city} (is ${base} a dev server?)`);
  await b.evalv(CARD_JS);
  const pack = JSON.parse(readFileSync(join(ROOT, "content/cities", city, "city.json"), "utf8"));
  const dir = join(CACHE, city);
  const old = cachedManifest(city);
  const periods = {};
  let drew = 0;
  for (const p of meta.periods) {
    // an era is current if its drawn inputs and its plan images are what its plate was baked from
    const key = `${p.hash}:${plansDigest(p.plans)}`;
    const prev = old?.version === meta.version ? old.periods?.[p.id] : null;
    if (!flag("--force") && prev?.key === key && existsSync(join(dir, prev.full)) && existsSync(join(dir, prev.preview))) {
      periods[p.id] = { ...prev };
      await card(b, city, pack, p.id, periods[p.id], prev);
      continue;
    }
    const t = Date.now();
    // the biggest plates take a few minutes on a CPU-only CI runner
    const res = await b.evalv(`window.__bakePlate(${JSON.stringify(p.id)})`, 15 * 60000);
    const full = `${p.id}.webp`, preview = `${p.id}.preview.webp`;
    mkdirSync(dir, { recursive: true });
    writeFileSync(join(dir, full), Buffer.from(res.full, "base64"));
    writeFileSync(join(dir, preview), Buffer.from(res.preview, "base64"));
    periods[p.id] = { full, preview, hash: p.hash, key };
    drew++;
    console.log(`${city}/${p.id}  full ${(res.full.length * 0.75 / 1048576).toFixed(2)} MB, preview ${Math.round(res.preview.length * 0.75 / 1024)} KB  ${Date.now() - t} ms`);
    await card(b, city, pack, p.id, periods[p.id], prev);
  }
  mkdirSync(dir, { recursive: true });
  writeFileSync(join(dir, "manifest.json"), JSON.stringify({ version: meta.version, periods }, null, 1));
  baked += drew;
  kept += meta.periods.length - drew;
}

/** An era's share card, drawn again only when its map or its words change. */
async function card(b, city, pack, periodId, entry, prev) {
  const per = pack.periods.find((x) => x.id === periodId);
  const words = { kicker: `Chronoscape · ${pack.subtitle}`, title: pack.name, line: `${fmtYear(per.year)} · ${per.label}` };
  const key = hash(`${CARD_VERSION}:${entry.key}:${JSON.stringify(words)}`);
  const file = `${periodId}.card.jpg`;
  if (!flag("--force") && prev?.card?.key === key && existsSync(join(CACHE, city, file))) return void (entry.card = prev.card);
  try {
    const jpg = await b.evalv(`window.__card(${JSON.stringify({ srcs: [`/plates/${city}/${entry.full}`], ...words })})`, 120000);
    writeFileSync(join(CACHE, city, file), Buffer.from(jpg, "base64"));
    entry.card = { file, key };
  } catch (e) {
    // a missing card costs a link preview, not the build
    console.warn(`plates: no share card for ${city}/${periodId} (${e.message.split("\n")[0]})`);
  }
}

/** One card per atlas: its maps side by side (up to four), with the atlas's name and age. */
async function atlasCards(b) {
  const atlases = JSON.parse(readFileSync(join(ROOT, "content/atlases.json"), "utf8")).atlases;
  const dir = join(CACHE, "_atlas");
  mkdirSync(dir, { recursive: true });
  const mf = join(dir, "manifest.json");
  const old = existsSync(mf) ? JSON.parse(readFileSync(mf, "utf8")) : {};
  const next = {};
  let drew = 0;
  await b.evalv(CARD_JS);
  for (const a of atlases) {
    const maps = a.maps.filter((m) => m.city && m.period && existsSync(join(CACHE, m.city, `${m.period}.preview.webp`))).slice(0, 4);
    if (!maps.length) continue;
    const plateKeys = maps.map((m) => JSON.parse(readFileSync(join(CACHE, m.city, "manifest.json"), "utf8")).periods?.[m.period]?.key ?? "");
    const words = { kicker: `Chronoscape · Atlas · ${a.region}`, title: a.title, line: `${a.era} · ${a.maps.map((m) => m.title).join(", ")}` };
    const key = hash(`${CARD_VERSION}:${plateKeys.join(",")}:${JSON.stringify(words)}`);
    const file = `${a.id}.card.jpg`;
    if (!flag("--force") && old[a.id] === key && existsSync(join(dir, file))) {
      next[a.id] = key;
      continue;
    }
    try {
      const srcs = maps.map((m) => `/plates/${m.city}/${m.period}.preview.webp`);
      writeFileSync(join(dir, file), Buffer.from(await b.evalv(`window.__card(${JSON.stringify({ srcs, ...words })})`, 120000), "base64"));
      next[a.id] = key;
      drew++;
    } catch (e) {
      console.warn(`plates: no share card for the atlas ${a.id} (${e.message.split("\n")[0]})`);
    }
  }
  writeFileSync(mf, JSON.stringify(next, null, 1));
  console.log(`plates: atlas cards ${drew} drawn, ${Object.keys(next).length - drew} already current`);
}

const browsers = [];
try {
  const jobs = Math.min(JOBS, queue.length);
  // on a fresh install Vite pre-bundles the app's dependencies on the first page load and then reloads it;
  // let one browser go through that alone before the others connect
  browsers.push(await startChrome(PORT));
  if (queue.length) {
    await browsers[0].send("Page.navigate", { url: `${base}/${queue[0]}/` });
    for (let i = 0; i < 480; i++) {
      await sleep(250);
      if (await browsers[0].evalv("!!window.__plateMeta").catch(() => false)) break;
    }
  }
  for (let i = 1; i < jobs; i++) browsers.push(await startChrome(PORT + i));
  const failed = [];
  await Promise.all(
    browsers.map(async (b, i) => {
      for (let city = queue.shift(); city; city = queue.shift()) {
        try {
          await bakeCity(b, city);
        } catch (e) {
          // a crashed tab (out of memory on a huge plate) gets a fresh browser and one more try
          console.warn(`plates: ${city} failed (${e.message.split("\n")[0]}); retrying`);
          b.close();
          b = browsers[i] = await startChrome(PORT + i);
          await bakeCity(b, city).catch((e2) => failed.push(`${city}: ${e2.message.split("\n")[0]}`));
        }
      }
    }),
  );
  if (failed.length) throw new Error(`plates failed for ${failed.join("; ")}`);
  if (!only) await atlasCards(browsers[0]);
} finally {
  browsers.forEach((b) => b.close());
  await server?.close();
}
console.log(`plates: ${baked} drawn, ${kept} already current, ${JOBS} jobs (${Math.round((Date.now() - t0) / 1000)} s)`);

if (out) {
  // every playable map on the shelf must have a preview to fold, or the build fails
  const atlases = JSON.parse(readFileSync(join(ROOT, "content/atlases.json"), "utf8")).atlases;
  const missing = atlases.flatMap((a) => a.maps.filter((m) => m.city && m.period && !existsSync(join(CACHE, m.city, `${m.period}.preview.webp`))).map((m) => `${m.city}/${m.period}`));
  if (missing.length) {
    console.error(`plates: no baked preview for ${missing.join(", ")}`);
    process.exit(1);
  }
  rmSync(out, { recursive: true, force: true });
  for (const city of [...cities, "_atlas"]) if (existsSync(join(CACHE, city))) cpSync(join(CACHE, city), join(out, city), { recursive: true });
  console.log(`plates: copied into ${out}`);
}
