import Icon from "../../../components/Icon";

function PlannerHeader({ onConfirm, route, trip, tripRole, websocketReady }) {
  const statusLabel = websocketReady ? "Live synced" : "Offline sync";
  const routeLabel =
    route?.provider_status === "ok"
      ? `${route.legs?.length || 0} routed legs`
      : route?.provider_status === "directions_unavailable"
        ? "Markers only"
        : "Route pending";

  return (
    <section className="section-shell flex flex-col gap-5 lg:flex-row lg:items-center lg:justify-between">
      <div className="space-y-4">
        <div className="flex flex-wrap items-center gap-3">
          <span className="label-md text-tertiary">Planner studio</span>
          <span className="rounded-full bg-secondary-container px-3 py-2 text-xs font-semibold text-tertiary dark:bg-white/10 dark:text-white">
            {statusLabel}
          </span>
          <span className="rounded-full bg-surface-container-lowest px-3 py-2 text-xs font-semibold text-text/65 dark:bg-dark-card dark:text-white/70">
            {routeLabel}
          </span>
          {tripRole ? (
            <span className="rounded-full bg-surface-container-lowest px-3 py-2 text-xs font-semibold uppercase text-text/65 dark:bg-dark-card dark:text-white/70">
              {tripRole}
            </span>
          ) : null}
        </div>
        <div>
          <h1 className="text-4xl font-bold tracking-tight">{trip ? `${trip.destination_city}, ${trip.state || "Curated route"}` : "Planner"}</h1>
          <p className="mt-2 max-w-3xl text-sm leading-7 text-text/65 dark:text-white/65">
            Map-first planning with live itinerary editing, route context, and collaborative refinements in one focused workspace.
          </p>
        </div>
        <div className="flex flex-wrap gap-3 text-sm">
          <div className="rounded-[1.25rem] bg-surface-container-lowest px-4 py-3 dark:bg-dark-card">
            <p className="label-md text-text/45 dark:text-white/45">Duration</p>
            <p className="mt-1 font-semibold">{trip?.duration_days || 0} days</p>
          </div>
          <div className="rounded-[1.25rem] bg-surface-container-lowest px-4 py-3 dark:bg-dark-card">
            <p className="label-md text-text/45 dark:text-white/45">Traveler</p>
            <p className="mt-1 font-semibold capitalize">{trip?.traveler_type || "Curated"}</p>
          </div>
          <div className="rounded-[1.25rem] bg-surface-container-lowest px-4 py-3 dark:bg-dark-card">
            <p className="label-md text-text/45 dark:text-white/45">Budget</p>
            <p className="mt-1 font-semibold">{trip?.budget_total ? `Rs ${trip.budget_total}` : "Flexible"}</p>
          </div>
          <div className="rounded-[1.25rem] bg-surface-container-lowest px-4 py-3 dark:bg-dark-card">
            <p className="label-md text-text/45 dark:text-white/45">Version</p>
            <p className="mt-1 font-semibold">
              v{trip?.version || 1}
              {trip?.locked_day_number ? ` | Day ${trip.locked_day_number} locked` : ""}
            </p>
          </div>
        </div>
      </div>

      <div className="flex flex-wrap gap-3 lg:justify-end">
        <button className="secondary-pill inline-flex items-center gap-2" type="button">
          <Icon className="h-4 w-4" name="heart" />
          Save
        </button>
        <button className="secondary-pill inline-flex items-center gap-2" type="button">
          <Icon className="h-4 w-4" name="users" />
          Share
        </button>
        <button className="secondary-pill inline-flex items-center gap-2" type="button">
          <Icon className="h-4 w-4" name="calendar" />
          Export
        </button>
        <button className="primary-pill inline-flex items-center gap-2" onClick={onConfirm} type="button">
          <Icon className="h-4 w-4" name="sparkles" />
          Confirm itinerary
        </button>
      </div>
    </section>
  );
}

export default PlannerHeader;
