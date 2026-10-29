import { useEffect, useState } from "react";
import type { City } from "@/content/schema";
import { Scene } from "./engine/Scene";
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
import { MapCase } from "./ui/MapCase";
import { installBakeHook } from "./engine/map/plateService";

/** A city map with everything around it. Loaded on demand: the title page and map room never pay for three.js city code. */
export default function CityView({ city }: { city: City }) {
  // the plate baker (dev server only, /<city>/?bake) needs the drawing hooks, not the city: rendering it in software
  // on a GPU-less CI runner would cost minutes and gigabytes per city
  const [bake] = useState(() => import.meta.env.DEV && new URLSearchParams(location.search).has("bake"));
  if (bake) return <BakeOnly city={city} />;
  return <CityScreen city={city} />;
}

function BakeOnly({ city }: { city: City }) {
  useEffect(() => installBakeHook(city), [city]);
  return null;
}

function CityScreen({ city }: { city: City }) {
  const [caseOpen, setCaseOpen] = useState(false);
  // the atlases on the study table open the map case too
  useEffect(() => {
    const open = () => setCaseOpen(true);
    addEventListener("chronoscape:open-mapcase", open);
    return () => removeEventListener("chronoscape:open-mapcase", open);
  }, []);
  return (
    <>
      <Scene key={city.id} city={city} />
      <MapOverlay city={city} />
      <Hud city={city} onMapCase={() => setCaseOpen(true)} />
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
      <MapCase open={caseOpen} onClose={() => setCaseOpen(false)} />
    </>
  );
}
