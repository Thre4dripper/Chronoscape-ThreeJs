import { useEffect } from "react";
import { Scene } from "./engine/Scene";
import { useStore } from "./engine/store";
import { cityIndex, loadCity } from "./content/registry";
import { Hud } from "./ui/Hud";
import { Timeline } from "./ui/Timeline";
import { LandmarkPanel } from "./ui/LandmarkPanel";
import { StoryBar } from "./ui/StoryBar";
import { ChangesCard } from "./ui/ChangesCard";
import { FeatureTooltip } from "./ui/FeatureTooltip";
import { SpotPanel } from "./ui/SpotPanel";
import { EventCard } from "./ui/EventCard";
import { EraPanel } from "./ui/EraPanel";
import { DayDial } from "./ui/DayDial";
import { MapOverlay } from "./ui/MapOverlay";
import { LeftColumn } from "./ui/Codex";

export function App() {
  const city = useStore((s) => s.city);
  const cityId = useStore((s) => s.cityId);
  const loading = useStore((s) => s.loading);
  const error = useStore((s) => s.error);

  useEffect(() => {
    const params = new URLSearchParams(location.search);
    const wanted = params.get("city") ?? cityIndex.cities[0].id;
    // Deep links: ?city=rome&period=late-400ce&focus=colosseum
    void switchCity(wanted).then(() => {
      const st = useStore.getState();
      const period = params.get("period");
      const focus = params.get("focus");
      const spot = params.get("spot");
      const event = params.get("event");
      const hour = params.get("hour");
      if (period) st.setPeriod(period);
      if (hour) st.setHour(parseFloat(hour));
      if (focus) useStore.getState().focus(focus);
      if (spot) useStore.getState().focusSpot(spot);
      if (event) useStore.getState().focusEvent(event);
      useStore.getState().dismissChange();
    });
  }, []);

  return (
    <div className="app">
      {city && <Scene key={city.id} city={city} />}
      {city && (
        <>
          <MapOverlay city={city} />
          <Hud city={city} onSwitchCity={switchCity} />
          <Timeline city={city} />
          <LandmarkPanel city={city} />
          <LeftColumn city={city} />
          <SpotPanel city={city} />
          <EventCard city={city} />
          <EraPanel city={city} />
          <StoryBar city={city} />
          <ChangesCard city={city} />
          <FeatureTooltip city={city} />
          <DayDial />
        </>
      )}
      {loading && <div className="loading">Unrolling {cityId} …</div>}
      {error && <div className="loading loading--error">{error}</div>}
    </div>
  );
}

export async function switchCity(id: string) {
  const st = useStore.getState();
  if (st.cityId === id && st.city) return;
  st.setLoading(id);
  try {
    const city = await loadCity(id);
    useStore.getState().setCity(id, city);
    const url = new URL(location.href);
    url.searchParams.set("city", id);
    history.replaceState(null, "", url);
  } catch (e) {
    useStore.getState().setError((e as Error).message);
  }
}
