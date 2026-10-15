/** Frame-rate independent exponential approach. rate ~ "how many times per second we close most of the gap". */
export function damp(current: number, target: number, rate: number, dt: number): number {
  return current + (target - current) * (1 - Math.exp(-rate * dt));
}

export function clamp(v: number, lo: number, hi: number): number {
  return Math.min(hi, Math.max(lo, v));
}

export function easeOutCubic(t: number): number {
  const u = clamp(t, 0, 1);
  return 1 - Math.pow(1 - u, 3);
}

export function easeOutBack(t: number): number {
  const u = clamp(t, 0, 1);
  const c1 = 1.2;
  const c3 = c1 + 1;
  return 1 + c3 * Math.pow(u - 1, 3) + c1 * Math.pow(u - 1, 2);
}

/** Progress of one stage in a staggered reveal: stage i of n gets window [i/n*overlap-adjusted]. */
export function stageProgress(p: number, stage: number, stages: number): number {
  if (stages <= 1) return clamp(p, 0, 1);
  const span = 1 / (stages * 0.6 + 0.4); // each stage overlaps the next by ~40%
  const start = stage * span * 0.6;
  return clamp((p - start) / span, 0, 1);
}

let reduced: boolean | null = null;
export function prefersReducedMotion(): boolean {
  if (reduced === null) {
    reduced = typeof window !== "undefined" && !!window.matchMedia?.("(prefers-reduced-motion: reduce)").matches;
  }
  return reduced;
}
