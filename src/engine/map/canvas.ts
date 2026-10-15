/** Canvas helpers that work both on the main thread and inside a worker. */
export type AnyCanvas = HTMLCanvasElement | OffscreenCanvas;
export type Ctx2D = CanvasRenderingContext2D | OffscreenCanvasRenderingContext2D;

export function makeCanvas(w: number, h: number): AnyCanvas {
  if (typeof OffscreenCanvas !== "undefined") return new OffscreenCanvas(w, h);
  const c = document.createElement("canvas");
  c.width = w;
  c.height = h;
  return c;
}

export function ctx2d(c: AnyCanvas): Ctx2D {
  return c.getContext("2d") as Ctx2D;
}

export const FONT_FACES: { family: string; url: string; style: string; weight: string }[] = [
  { family: "IM Fell English", url: "/fonts/imfell-regular.woff2", style: "normal", weight: "400" },
  { family: "IM Fell English", url: "/fonts/imfell-italic.woff2", style: "italic", weight: "400" },
  { family: "Cormorant Garamond", url: "/fonts/cormorant-var.woff2", style: "normal", weight: "500 600" },
];

/** Load the map's lettering faces into whichever FontFaceSet this context has (document or worker). */
export async function loadFonts(): Promise<void> {
  const g = globalThis as unknown as { fonts?: FontFaceSet; document?: Document };
  const set = g.document?.fonts ?? g.fonts;
  if (!set) return;
  await Promise.all(
    FONT_FACES.map(async (f) => {
      try {
        const ff = new FontFace(f.family, `url(${f.url})`, { style: f.style, weight: f.weight });
        await ff.load();
        set.add(ff);
      } catch {
        /* fall back to serif */
      }
    }),
  );
}
