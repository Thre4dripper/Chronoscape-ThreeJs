import { lazy, Suspense, useEffect } from "react";
import { useStore } from "./engine/store";
import { syncFromUrl, useNav } from "./nav";
import { TitlePage } from "./ui/title/TitlePage";
import { Flight } from "./ui/Flight";

// three.js and everything 3D load only when they are needed
const CityView = lazy(() => import("./CityView"));
const MapRoom = lazy(() => import("./ui/room/MapRoom"));

export function App() {
  const view = useNav((s) => s.view);
  const flight = useNav((s) => s.flight);
  const city = useStore((s) => s.city);
  const cityId = useStore((s) => s.cityId);
  const loading = useStore((s) => s.loading);
  const error = useStore((s) => s.error);

  useEffect(() => {
    syncFromUrl();
    addEventListener("popstate", syncFromUrl);
    return () => removeEventListener("popstate", syncFromUrl);
  }, []);

  return (
    <div className="app" data-view={view}>
      {view === "title" && <TitlePage />}
      {view === "room" && (
        <Suspense fallback={<div className="loading">Opening the map room …</div>}>
          <MapRoom />
        </Suspense>
      )}
      {view === "city" && city && (
        <Suspense fallback={null}>
          <CityView key={city.id} city={city} />
        </Suspense>
      )}
      {flight && <Flight key={`${flight.kind}:${flight.map.title}:${flight.image}`} flight={flight} />}
      {view === "city" && loading && !flight && <div className="loading">Unrolling {cityId} …</div>}
      {error && <div className="loading loading--error">{error}</div>}
    </div>
  );
}
