import { useGLTF } from "@react-three/drei";

/** Baked models are Draco-compressed; the decoder (wasm) is self-hosted and only fetched on first hover. */
export const DRACO_PATH = "/draco/";

export function useModel(url: string) {
  return useGLTF(url, DRACO_PATH);
}
