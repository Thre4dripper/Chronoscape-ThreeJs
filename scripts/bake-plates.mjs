/**
 * Bake every period's whole-city map plate into .plate-cache/<city>/<period>.webp (and a preview), so the
 * production site shows the map at once instead of drawing it at load. Plates are build output, not source:
 * the cache is git-ignored, a city is only baked again when its content or PLATE_VERSION changes, and
 * `npm run build` copies the cache into dist/plates. The dev server serves the cache if it exists and draws
 * any plate it lacks in a worker.
 *
 *   npm run plates:bake                   # every city
 *   node scripts/bake-plates.mjs rome     # one city
 *   node scripts/bake-plates.mjs --out dist/plates   # bake what is stale, check, then copy into the build
 *   --force bakes again even if the cache is current. CHROME=/path/to/chrome overrides the browser;
 *   APP_URL=http://localhost:5173 uses a running dev server instead of starting one.
 */
import { spawn } from "node:child_process";
import { cpSync, existsSync, mkdirSync, mkdtempSync, readFileSync, rmSync, writeFileSync } from "node:fs";
import { join, resolve } from "node:path";
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

/** The cached plates of a city, if they were baked from exactly this content. */
function cached(city, meta) {
  const mp = join(CACHE, city, "manifest.json");
  if (!existsSync(mp)) return false;
  const m = JSON.parse(readFileSync(mp, "utf8"));
  return (
    m.version === meta.version &&
    m.content === meta.content &&
    meta.periods.every((p) => m.periods[p] && existsSync(join(CACHE, city, m.periods[p].full)) && existsSync(join(CACHE, city, m.periods[p].preview)))
  );
}

const sleep = (ms) => new Promise((r) => setTimeout(r, ms));
let server = null;
let base = process.env.APP_URL;
if (!base) {
  const { createServer } = await import("vite");
  server = await createServer({ root: ROOT, logLevel: "error", server: { port: 5199, strictPort: false, hmr: false } });
  await server.listen();
  base = server.resolvedUrls.local[0].replace(/\/$/, "");
}
const profile = mkdtempSync(join(tmpdir(), "bake-"));
const chromeArgs = ["--headless=new", `--remote-debugging-port=${PORT}`, `--user-data-dir=${profile}`, "--window-size=800,600"];
if (process.env.CI) chromeArgs.push("--no-sandbox"); // CI runners forbid the sandbox's user namespaces
const chrome = spawn(findChrome(), [...chromeArgs, "about:blank"], { stdio: "ignore" });
let baked = 0, kept = 0;
const t0 = Date.now();
try {
  let list;
  for (let i = 0; i < 80 && !list; i++) {
    await sleep(250);
    list = await fetch(`http://127.0.0.1:${PORT}/json`).then((r) => r.json()).catch(() => null);
  }
  if (!list) throw new Error("Chrome did not start");
  const ws = new WebSocket(list.find((t) => t.type === "page").webSocketDebuggerUrl);
  await new Promise((r) => (ws.onopen = r));
  let id = 0;
  const pending = new Map();
  ws.onmessage = (ev) => {
    const m = JSON.parse(ev.data);
    if (m.id && pending.has(m.id)) pending.get(m.id)(m), pending.delete(m.id);
  };
  const send = (method, params = {}) => new Promise((res) => { const i = ++id; pending.set(i, res); ws.send(JSON.stringify({ id: i, method, params })); });
  const evalv = async (expression) => {
    const r = await send("Runtime.evaluate", { expression, returnByValue: true, awaitPromise: true });
    if (r.result?.exceptionDetails) throw new Error(r.result.exceptionDetails.exception?.description);
    return r.result.result.value;
  };
  for (const city of cities) {
    if (only && only !== city) continue;
    await send("Page.navigate", { url: `${base}/?city=${city}` });
    let meta = null;
    for (let i = 0; i < 240 && !meta; i++) {
      await sleep(250);
      meta = await evalv("window.__plateMeta ? window.__plateMeta() : null").catch(() => null);
    }
    if (!meta) throw new Error(`bake hook not found for ${city} (is ${base} a dev server?)`);
    if (!flag("--force") && cached(city, meta)) {
      kept++;
      continue;
    }
    const dir = join(CACHE, city);
    rmSync(dir, { recursive: true, force: true });
    mkdirSync(dir, { recursive: true });
    const periods = {};
    for (const p of meta.periods) {
      const t = Date.now();
      const res = await evalv(`window.__bakePlate(${JSON.stringify(p)})`);
      const full = `${p}.webp`, preview = `${p}.preview.webp`;
      writeFileSync(join(dir, full), Buffer.from(res.full, "base64"));
      writeFileSync(join(dir, preview), Buffer.from(res.preview, "base64"));
      periods[p] = { full, preview };
      console.log(`${city}/${p}  full ${(res.full.length * 0.75 / 1048576).toFixed(2)} MB, preview ${Math.round(res.preview.length * 0.75 / 1024)} KB  ${Date.now() - t} ms`);
    }
    writeFileSync(join(dir, "manifest.json"), JSON.stringify({ version: meta.version, content: meta.content, periods }, null, 1));
    baked++;
  }
  ws.close();
} finally {
  chrome.kill();
  await server?.close();
  rmSync(profile, { recursive: true, force: true });
}
console.log(`plates: ${baked} cities baked, ${kept} already current (${Math.round((Date.now() - t0) / 1000)} s)`);

if (out) {
  // every playable map on the shelf must have a preview to fold, or the build fails
  const atlases = JSON.parse(readFileSync(join(ROOT, "content/atlases.json"), "utf8")).atlases;
  const missing = atlases.flatMap((a) => a.maps.filter((m) => m.city && m.period && !existsSync(join(CACHE, m.city, `${m.period}.preview.webp`))).map((m) => `${m.city}/${m.period}`));
  if (missing.length) {
    console.error(`plates: no baked preview for ${missing.join(", ")}`);
    process.exit(1);
  }
  rmSync(out, { recursive: true, force: true });
  for (const city of cities) if (existsSync(join(CACHE, city))) cpSync(join(CACHE, city), join(out, city), { recursive: true });
  console.log(`plates: copied into ${out}`);
}
