import { describe, it, expect, beforeEach } from "vitest";
import { readFileSync } from "node:fs";
import { join, resolve } from "node:path";
import { useStore, diffPeriods } from "../src/engine/store";
import { validateCity } from "../src/content/validate";

const raw = JSON.parse(readFileSync(join(resolve(__dirname, ".."), "content/cities/rome/city.json"), "utf8"));
const rome = validateCity(raw).city!;

describe("interaction state machine", () => {
  beforeEach(() => useStore.getState().setCity("rome", rome));

  it("starts exploring in the default period", () => {
    const s = useStore.getState();
    expect(s.mode).toBe("exploring");
    expect(s.periodId).toBe("empire-100ce");
  });

  it("hover previews, leaving returns to exploring", () => {
    useStore.getState().hover("colosseum");
    expect(useStore.getState().mode).toBe("previewing");
    useStore.getState().hover(null);
    expect(useStore.getState().mode).toBe("exploring");
  });

  it("click focuses, immerse deepens, escape unwinds one layer at a time", () => {
    const s = useStore.getState();
    s.focus("colosseum");
    expect(useStore.getState().mode).toBe("focused");
    useStore.getState().immerse();
    expect(useStore.getState().mode).toBe("immersed");
    useStore.getState().back();
    expect(useStore.getState().mode).toBe("focused");
    useStore.getState().back();
    expect(useStore.getState().mode).toBe("exploring");
    expect(useStore.getState().focusedId).toBeNull();
  });

  it("refuses to focus a landmark that does not exist in the current period", () => {
    useStore.getState().setPeriod("republic-50bce");
    useStore.getState().focus("colosseum");
    expect(useStore.getState().focusedId).toBeNull();
  });

  it("a period change that removes the focused landmark returns to the map with an explanation", () => {
    useStore.getState().focus("colosseum");
    useStore.getState().setPeriod("republic-50bce");
    const s = useStore.getState();
    expect(s.mode).toBe("exploring");
    expect(s.periodChange?.entries.some((e) => e.landmarkId === "colosseum" && e.kind === "disappears")).toBe(true);
  });

  it("stories step through landmarks and set their period", () => {
    useStore.getState().setPeriod("late-400ce");
    useStore.getState().startStory("triumph-71ce");
    let s = useStore.getState();
    expect(s.periodId).toBe("empire-100ce");
    expect(s.focusedId).toBe("circus-maximus");
    useStore.getState().storyNext();
    expect(useStore.getState().focusedId).toBe("arch-of-titus");
    useStore.getState().back();
    s = useStore.getState();
    expect(s.storyId).toBeNull();
    expect(s.mode).toBe("exploring");
  });

  it("diffPeriods reports appearances and notes", () => {
    const d = diffPeriods(rome, "republic-50bce", "empire-100ce");
    expect(d.entries.find((e) => e.landmarkId === "colosseum")?.kind).toBe("appears");
    expect(d.entries.find((e) => e.landmarkId === "temple-of-saturn")?.kind).toBe("changes");
  });
});
