/**
 * Bake every period's whole-city map plate to assets/plates/<city>/<period>.webp,
 * so the app shows the map immediately instead of drawing it at load.
 *
 *   npm run dev            # in another terminal
 *   npm run plates:bake    # CHROME=/path/to/chrome to override
 */
import { spawn } from "node:child_process";
import { mkdirSync, writeFileSync, readFileSync, mkdtempSync } from "node:fs";
import { join, resolve } from "node:path";
import { tmpdir } from "node:os";

const ROOT = resolve(import.meta.dirname, "..");
const BASE = process.env.APP_URL ?? "http://localhost:5173";
const CHROME = process.env.CHROME ?? "/Users/ijlalahmad/Applications/Google Chrome.app/Contents/MacOS/Google Chrome";
const PORT = +(process.env.PORT ?? 9333);
const cities = JSON.parse(readFileSync(join(ROOT, "content/cities/index.json"), "utf8")).cities.map((c) => c.id);
const only = process.argv[2];

const profile = mkdtempSync(join(tmpdir(), "bake-"));
const chrome = spawn(CHROME, ["--headless=new", `--remote-debugging-port=${PORT}`, `--user-data-dir=${profile}`, "--window-size=800,600", "about:blank"], { stdio: "ignore" });
const sleep = (ms) => new Promise((r) => setTimeout(r, ms));
try {
  let list;
  for (let i = 0; i < 40 && !list; i++) {
    await sleep(250);
    list = await fetch(`http://127.0.0.1:${PORT}/json`).then((r) => r.json()).catch(() => null);
  }
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
    await send("Page.navigate", { url: `${BASE}/?city=${city}` });
    let meta = null;
    for (let i = 0; i < 120 && !meta; i++) {
      await sleep(250);
      meta = await evalv("window.__plateMeta ? window.__plateMeta() : null").catch(() => null);
    }
    if (!meta) throw new Error(`bake hook not found for ${city} (is the dev server running at ${BASE}?)`);
    const dir = join(ROOT, "assets/plates", city);
    mkdirSync(dir, { recursive: true });
    const periods = {};
    for (const p of meta.periods) {
      const t = Date.now();
      const out = await evalv(`window.__bakePlate(${JSON.stringify(p)})`);
      const full = `${p}.webp`, preview = `${p}.preview.webp`;
      writeFileSync(join(dir, full), Buffer.from(out.full, "base64"));
      writeFileSync(join(dir, preview), Buffer.from(out.preview, "base64"));
      periods[p] = { full, preview };
      console.log(`${city}/${p}  full ${(out.full.length * 0.75 / 1048576).toFixed(2)} MB, preview ${Math.round(out.preview.length * 0.75 / 1024)} KB  ${Date.now() - t} ms`);
    }
    writeFileSync(join(dir, "manifest.json"), JSON.stringify({ version: meta.version, content: meta.content, periods }, null, 1));
  }
  ws.close();
} finally {
  chrome.kill();
}
