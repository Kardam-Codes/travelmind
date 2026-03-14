import Icon from "../../../components/Icon";

function PlannerHeader({ onShare, onStartGroup, trip }) {
  return (
    <section className="section-shell flex flex-col gap-4 lg:flex-row lg:items-center lg:justify-between">
      <div>
        <p className="label-md text-tertiary">Planner</p>
        <h1 className="mt-2 text-3xl font-bold tracking-tight">
          {trip ? `${trip.destination_city}, ${trip.state || "Curated route"}` : "Planner"}
        </h1>
        <div className="mt-3 flex flex-wrap gap-3 text-sm">
          <span className="rounded-full bg-surface-container-lowest px-4 py-2 font-semibold dark:bg-dark-card">
            {trip?.duration_days || 0} days
          </span>
          <span className="rounded-full bg-surface-container-lowest px-4 py-2 font-semibold dark:bg-dark-card">
            {trip?.budget_total ? `Rs ${trip.budget_total}` : "Flexible"}
          </span>
        </div>
      </div>

      <div className="flex flex-wrap gap-3 lg:justify-end">
        <button className="primary-pill inline-flex items-center gap-2" onClick={onStartGroup} type="button">
          <Icon className="h-4 w-4" name="users" />
          Start Group Plan
        </button>
        <button className="secondary-pill inline-flex items-center gap-2" onClick={onShare} type="button">
          <Icon className="h-4 w-4" name="arrow" />
          Share
        </button>
      </div>
    </section>
  );
}

export default PlannerHeader;
