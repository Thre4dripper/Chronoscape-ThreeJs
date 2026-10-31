import { useGLTF } from "@react-three/drei";

/** Baked models are Draco-compressed; the decoder (wasm) is self-hosted and fetched with the first model (the study's, when the desk is on). */
export const DRACO_PATH = "/draco/";

const loadedUrls: Record<string, true> = {};

export function useModel(url: string) {
  loadedUrls[url] = true;
  return useGLTF(url, DRACO_PATH);
}

const preloaded = new Set<string>();
/** Fetch and decode a model ahead of use (once), so the first hover finds it ready. */
export function preloadModel(url: string) {
  if (preloaded.has(url)) return;
  preloaded.add(url);
  loadedUrls[url] = true;
  useGLTF.preload(url, DRACO_PATH);
}

/** Drop the decoded models under `prefix` (a city's folder) once it is left. */
export function forgetModels(prefix: string) {
  for (const url of [...preloaded]) if (url.startsWith(prefix)) preloaded.delete(url);
  useGLTF.clear(Object.keys(loadedUrls).filter((u) => u.startsWith(prefix)));
  for (const u of Object.keys(loadedUrls)) if (u.startsWith(prefix)) delete loadedUrls[u];
}
