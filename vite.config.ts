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
