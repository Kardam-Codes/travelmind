import Icon from "../../../components/Icon";
import TripMap from "../../../components/TripMap";

function PlannerMapStage({
  mapRoute,
  onSelectDay,
  onSelectStop,
  places,
  routeLeg,
  selectedDay,
  selectedStop,
  trip,
}) {
  const dayNumbers = Array.from(new Set((mapRoute?.stops || []).map((stop) => stop.day_number))).sort((left, right) => left - right);
  const routeMessage =
    mapRoute?.provider_status === "ok"
      ? "Route synced to the confirmed itinerary."
      : mapRoute?.warning || "Marker view is active while the route is loading.";

  return (
    <section className="section-shell relative min-h-[48rem] overflow-hidden p-0">
      <div className="absolute inset-0 bg-[radial-gradient(circle_at_top_left,rgba(0,109,119,0.16),transparent_28%),radial-gradient(circle_at_bottom_right,rgba(140,37,0,0.12),transparent_26%)]" />
      <div className="absolute inset-4">
        <TripMap
          className="h-full w-full"
          fallbackMessage={mapRoute?.warning || ""}
          onSelectStop={onSelectStop}
          places={places}
          route={mapRoute}
          selectedDay={selectedDay}
          selectedStopId={selectedStop?.id || null}
        />
      </div>

      <div className="absolute left-8 right-8 top-8 flex flex-col gap-4 xl:flex-row xl:items-start xl:justify-between">
        <div className="glass-panel rounded-[1.5rem] px-5 py-4 shadow-ambient">
          <p className="label-md text-primary/70 dark:text-white/55">Map focus</p>
          <div className="mt-3 flex flex-wrap gap-2">
            <button className={selectedDay == null ? "primary-pill px-4 py-2 text-sm" : "secondary-pill px-4 py-2 text-sm"} onClick={() => onSelectDay(null)} type="button">
              All days
            </button>
            {dayNumbers.map((dayNumber) => (
              <button
                key={dayNumber}
                className={selectedDay === dayNumber ? "primary-pill px-4 py-2 text-sm" : "secondary-pill px-4 py-2 text-sm"}
                onClick={() => onSelectDay(dayNumber)}
                type="button"
              >
                Day {dayNumber}
              </button>
            ))}
          </div>
        </div>

        <div className="glass-panel max-w-md rounded-[1.5rem] px-5 py-4 shadow-ambient">
          <div className="flex items-center gap-2">
            <Icon className="h-4 w-4 text-primary" name="route" />
            <p className="label-md text-primary/70 dark:text-white/55">Route status</p>
          </div>
          <p className="mt-3 text-sm leading-7 text-text/75 dark:text-white/75">{routeMessage}</p>
          {routeLeg ? (
            <p className="mt-3 rounded-full bg-surface-container-lowest px-4 py-3 text-sm font-semibold text-text/70 dark:bg-dark-card dark:text-white/75">
              Next leg: {routeLeg.distance_text || "Distance pending"} • {routeLeg.duration_text || "Duration pending"}
            </p>
          ) : null}
        </div>
      </div>

      <div className="absolute bottom-8 left-8 right-8 grid gap-4 xl:grid-cols-[minmax(0,1fr),22rem]">
        <div className="glass-panel rounded-[1.75rem] px-5 py-5 shadow-float">
          <p className="label-md text-primary/70 dark:text-white/55">Highlighted stop</p>
          <h2 className="mt-2 text-2xl font-bold">{selectedStop?.title || trip?.destination_city || "Planner route"}</h2>
          <p className="mt-3 max-w-2xl text-sm leading-7 text-text/75 dark:text-white/75">
            {selectedStop?.description ||
              "Select a stop from the itinerary or the map to inspect how it fits into the route and the pacing of the day."}
          </p>
        </div>
        <div className="glass-panel rounded-[1.75rem] px-5 py-5 shadow-float">
          <p className="label-md text-primary/70 dark:text-white/55">Trip posture</p>
          <div className="mt-3 space-y-3 text-sm text-text/75 dark:text-white/75">
            <p>{mapRoute?.stops?.length || 0} mapped stops</p>
            <p>{mapRoute?.legs?.length || 0} routed legs</p>
            <p>{selectedDay == null ? "Viewing the full route." : `Focused on day ${selectedDay}.`}</p>
          </div>
        </div>
      </div>
    </section>
  );
}

export default PlannerMapStage;
