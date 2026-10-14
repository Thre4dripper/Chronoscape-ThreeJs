import { defineConfig } from "vitest/config";
import react from "@vitejs/plugin-react";
import { fileURLToPath } from "node:url";

// `assets/` is served at the site root, so a model at assets/models/rome/x.glb
// is fetched as /models/rome/x.glb. Content packs reference that URL form.
export default defineConfig({
  plugins: [react()],
  publicDir: "assets",
  resolve: {
    alias: { "@": fileURLToPath(new URL("./src", import.meta.url)) },
  },
  server: { port: 5173 },
  build: { target: "es2022" },
  test: {
    environment: "node",
    include: ["tests/**/*.test.ts"],
  },
});
