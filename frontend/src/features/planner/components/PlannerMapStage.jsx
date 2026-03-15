import TripMap from "../../../components/TripMap";

function PlannerMapStage({
  mapRoute,
  onSelectDay,
  onSelectStop,
  places,
  selectedDay,
  selectedStop,
  trip,
}) {
  const dayNumbers = Array.from(new Set((mapRoute?.stops || []).map((stop) => stop.day_number))).sort((left, right) => left - right);

  return (
    <section className="section-shell travel-panel relative min-h-[48rem] overflow-hidden p-0">
      <div className="absolute inset-0 bg-[radial-gradient(circle_at_top_left,rgba(0,109,119,0.16),transparent_28%),radial-gradient(circle_at_bottom_right,rgba(217,119,6,0.12),transparent_26%)]" />
      <div className="absolute inset-4">
        <TripMap
          className="map-frame h-full w-full"
          fallbackMessage={mapRoute?.warning || ""}
          onSelectStop={onSelectStop}
          places={places}
          route={mapRoute}
          selectedDay={selectedDay}
          selectedStopId={selectedStop?.id || null}
        />
      </div>

      <div className="pointer-events-none absolute left-8 right-8 top-8 flex flex-col gap-4 xl:flex-row xl:items-start xl:justify-between">
        <div className="pointer-events-auto glass-panel rounded-[1.5rem] px-5 py-4 shadow-ambient">
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
      </div>

      <div className="absolute bottom-8 left-8 right-8">
        <div className="glass-panel hidden rounded-[1.75rem] px-5 py-5 shadow-float sm:block">
          <p className="label-md text-primary/70 dark:text-white/55">Highlighted stop</p>
          <h2 className="mt-2 text-2xl font-bold">{selectedStop?.title || trip?.destination_city || "Planner route"}</h2>
          <p className="mt-3 max-w-2xl text-sm leading-7 text-text/75 dark:text-white/75">
            {selectedStop?.description ||
              "Select a stop from the itinerary or the map to inspect how it fits into the route and the pacing of the day."}
          </p>
        </div>
        <div className="glass-panel inline-flex items-center rounded-full px-4 py-3 text-sm font-semibold text-text/80 shadow-float sm:hidden">
          {selectedStop?.title || trip?.destination_city || "Planner route"}
        </div>
      </div>
    </section>
  );
}

export default PlannerMapStage;
