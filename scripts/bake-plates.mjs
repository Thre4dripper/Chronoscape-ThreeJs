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
  await new Promise((r) => (ws.onopen = r));
  let id = 0;
  const pending = new Map();
  ws.onmessage = (ev) => {
    const m = JSON.parse(ev.data);
    if (m.id && pending.has(m.id)) pending.get(m.id)(m), pending.delete(m.id);
  };
  ws.onclose = () => pending.forEach((res) => res({ result: { exceptionDetails: { exception: { description: "Chrome closed the connection" } } } }));
  const send = (method, params = {}) => new Promise((res) => { const i = ++id; pending.set(i, res); ws.send(JSON.stringify({ id: i, method, params })); });
  const evalv = async (expression) => {
    const r = await send("Runtime.evaluate", { expression, returnByValue: true, awaitPromise: true });
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
  await b.send("Page.navigate", { url: `${base}/?city=${city}` });
  let meta = null;
  for (let i = 0; i < 240 && !meta; i++) {
    await sleep(250);
    meta = await b.evalv("window.__plateMeta ? window.__plateMeta() : null").catch(() => null);
  }
  if (!meta) throw new Error(`bake hook not found for ${city} (is ${base} a dev server?)`);
  const dir = join(CACHE, city);
  const old = cachedManifest(city);
  const periods = {};
  let drew = 0;
  for (const p of meta.periods) {
    // an era is current if its drawn inputs and its plan images are what its plate was baked from
    const key = `${p.hash}:${plansDigest(p.plans)}`;
    const prev = old?.version === meta.version ? old.periods?.[p.id] : null;
    if (!flag("--force") && prev?.key === key && existsSync(join(dir, prev.full)) && existsSync(join(dir, prev.preview))) {
      periods[p.id] = prev;
      continue;
    }
    const t = Date.now();
    const res = await b.evalv(`window.__bakePlate(${JSON.stringify(p.id)})`);
    const full = `${p.id}.webp`, preview = `${p.id}.preview.webp`;
    mkdirSync(dir, { recursive: true });
    writeFileSync(join(dir, full), Buffer.from(res.full, "base64"));
    writeFileSync(join(dir, preview), Buffer.from(res.preview, "base64"));
    periods[p.id] = { full, preview, hash: p.hash, key };
    drew++;
    console.log(`${city}/${p.id}  full ${(res.full.length * 0.75 / 1048576).toFixed(2)} MB, preview ${Math.round(res.preview.length * 0.75 / 1024)} KB  ${Date.now() - t} ms`);
  }
  mkdirSync(dir, { recursive: true });
  writeFileSync(join(dir, "manifest.json"), JSON.stringify({ version: meta.version, periods }, null, 1));
  baked += drew;
  kept += meta.periods.length - drew;
}

const browsers = [];
try {
  const jobs = Math.min(JOBS, queue.length);
  // on a fresh install Vite pre-bundles the app's dependencies on the first page load and then reloads it;
  // let one browser go through that alone before the others connect
  browsers.push(await startChrome(PORT));
  if (queue.length) {
    await browsers[0].send("Page.navigate", { url: `${base}/?city=${queue[0]}` });
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
  for (const city of cities) if (existsSync(join(CACHE, city))) cpSync(join(CACHE, city), join(out, city), { recursive: true });
  console.log(`plates: copied into ${out}`);
}
