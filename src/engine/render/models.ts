import { useGLTF } from "@react-three/drei";

/** Baked models are Draco-compressed; the decoder (wasm) is self-hosted and fetched with the first model (the study's, when the desk is on). */
export const DRACO_PATH = "/draco/";

export function useModel(url: string) {
  return useGLTF(url, DRACO_PATH);
}

const preloaded = new Set<string>();
/** Fetch and decode a model ahead of use (once), so the first hover finds it ready. */
export function preloadModel(url: string) {
  if (preloaded.has(url)) return;
  preloaded.add(url);
  useGLTF.preload(url, DRACO_PATH);
}
