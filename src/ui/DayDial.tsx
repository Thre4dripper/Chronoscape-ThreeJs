import { useStore } from "@/engine/store";

/** Hour-of-day control: lighting, crowds and the shop vignettes follow it. */
export function DayDial() {
  const hour = useStore((s) => s.hour);
  const setHour = useStore((s) => s.setHour);
  const label = `${String(Math.floor(hour)).padStart(2, "0")}:${hour % 1 ? "30" : "00"}`;
  const phase = hour < 5 || hour >= 21 ? "night" : hour < 8 ? "dawn" : hour < 18 ? "day" : "dusk";
  return (
    <div className={`daydial daydial--${phase}`} aria-label="Hour of the day">
      <span className="daydial__glyph" aria-hidden="true">
        {phase === "night" ? "☾" : "☼"}
      </span>
      <input type="range" min={0} max={23.5} step={0.5} value={hour} onChange={(e) => setHour(parseFloat(e.target.value))} />
      <span className="daydial__label">{label}</span>
    </div>
  );
}
