import { defineConfig } from "vitest/config";
import react from "@vitejs/plugin-react";
import { fileURLToPath } from "node:url";
import { createReadStream, existsSync, statSync } from "node:fs";
import { extname, join, normalize } from "node:path";
import type { Plugin } from "vite";

/**
 * Baked map plates are build output (scripts/bake-plates.mjs writes .plate-cache/, `pnpm build` copies it
 * into dist/plates). The dev server serves the cache at /plates when it has one; a plate it lacks is a 404,
 * and the app draws that plate in a worker instead.
 */
function platesFromCache(): Plugin {
  const dir = fileURLToPath(new URL("./.plate-cache", import.meta.url));
  const types: Record<string, string> = { ".webp": "image/webp", ".json": "application/json" };
  return {
    name: "chronoscape-plates",
    configureServer(server) {
      server.middlewares.use("/plates", (req, res) => {
        const file = normalize(join(dir, decodeURIComponent((req.url ?? "/").split("?")[0])));
        if (!file.startsWith(dir) || !existsSync(file) || !statSync(file).isFile()) {
          res.statusCode = 404;
          res.end();
          return;
        }
        res.setHeader("Content-Type", types[extname(file)] ?? "application/octet-stream");
        res.setHeader("Cache-Control", "no-cache");
        createReadStream(file).pipe(res);
      });
    },
  };
}

// `assets/` is served at the site root, so a model at assets/models/rome/x.glb
// is fetched as /models/rome/x.glb. Content packs reference that URL form.
export default defineConfig({
  plugins: [react(), platesFromCache()],
  publicDir: "assets",
  resolve: {
    alias: { "@": fileURLToPath(new URL("./src", import.meta.url)) },
  },
  server: { port: 5173 },
  build: {
    target: "es2022",
    rolldownOptions: {
      output: {
        // three.js and React Three Fiber in one chunk of their own, shared by the map room and the cities
        advancedChunks: { groups: [{ name: "three", test: /node_modules[\\/](three|@react-three|three-stdlib|troika|maath|meshline|camera-controls)/ }] },
      },
    },
  },
  test: {
    environment: "node",
    include: ["tests/**/*.test.ts"],
  },
});
