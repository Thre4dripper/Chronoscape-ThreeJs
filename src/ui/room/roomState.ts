import { create } from "zustand";

/** A label that follows the pointer over something in the room. */
export type Tip = { title: string; text?: string; hint?: string } | null;

/** The room's shared state: what is hovered, the pointer label, the lamp, the drawers, the register. */
export const useRoom = create<{
  hoverId: string | null;
  setHover: (id: string | null) => void;
  tip: Tip;
  setTip: (t: Tip) => void;
  evening: boolean;
  toggleEvening: () => void;
  drawer: "writing" | "instruments" | null;
  setDrawer: (d: "writing" | "instruments" | null) => void;
  register: boolean;
  setRegister: (on: boolean) => void;
}>((set) => ({
  hoverId: null,
  setHover: (hoverId) => set({ hoverId }),
  tip: null,
  setTip: (tip) => set({ tip }),
  evening: false,
  toggleEvening: () => set((s) => ({ evening: !s.evening })),
  drawer: null,
  setDrawer: (drawer) => set({ drawer }),
  register: false,
  setRegister: (register) => set({ register }),
}));

/** Pointer-label helpers for a 3D object: show on over, clear on out (only if it is still ours). */
export function tipHandlers(tip: NonNullable<Tip>, cursor = "pointer") {
  return {
    onPointerOver: (e: { stopPropagation: () => void }) => {
      e.stopPropagation();
      useRoom.getState().setTip(tip);
      document.body.style.cursor = cursor;
    },
    onPointerOut: () => {
      if (useRoom.getState().tip?.title === tip.title) useRoom.getState().setTip(null);
      document.body.style.cursor = "";
    },
  };
}
