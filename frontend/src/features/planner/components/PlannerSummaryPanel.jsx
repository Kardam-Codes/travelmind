import Icon from "../../../components/Icon";

function PlannerSummaryPanel({ inviteStatus, onInvite, trip, tripRole }) {
  const canInvite = tripRole === "owner";
  const tripBudget = trip?.budget_total ? `Rs ${trip.budget_total}` : "Flexible";

  function handleInvite(event) {
    event.preventDefault();
    const form = event.currentTarget;
    const email = form.email?.value?.trim();
    const role = form.role?.value || "viewer";
    if (!email) {
      return;
    }
    onInvite?.(email, role);
    form.reset();
  }

  return (
    <section className="section-shell travel-panel flex min-h-[36rem] flex-col gap-5">
      <div>
        <p className="label-md text-tertiary">Trip summary</p>
        <h2 className="mt-2 text-2xl font-semibold">{trip ? `${trip.destination_city} plan` : "Trip overview"}</h2>
        <p className="mt-2 text-sm text-text/60 dark:text-white/60">{trip?.preferences || "Curated for balanced pacing and route efficiency."}</p>
      </div>

      <div className="grid gap-3">
        <div className="rounded-[1.25rem] bg-surface-container-lowest px-4 py-3 text-sm dark:bg-dark-card">
          <p className="label-md text-text/45 dark:text-white/45">Duration</p>
          <p className="mt-1 font-semibold">{trip?.duration_days || 0} days</p>
        </div>
        <div className="rounded-[1.25rem] bg-surface-container-lowest px-4 py-3 text-sm dark:bg-dark-card">
          <p className="label-md text-text/45 dark:text-white/45">Budget</p>
          <p className="mt-1 font-semibold">{tripBudget}</p>
        </div>
        <div className="rounded-[1.25rem] bg-surface-container-lowest px-4 py-3 text-sm dark:bg-dark-card">
          <p className="label-md text-text/45 dark:text-white/45">Traveler</p>
          <p className="mt-1 font-semibold capitalize">{trip?.traveler_type || "curated"}</p>
        </div>
      </div>

      <div className="mt-2">
        <p className="label-md text-tertiary">Quick actions</p>
        <form className="mt-3 space-y-3" onSubmit={handleInvite}>
          <input
            className="soft-focus w-full rounded-[1.5rem] bg-surface-container-lowest px-4 py-3 text-sm text-text placeholder:text-text/35 dark:bg-dark-card dark:text-white dark:placeholder:text-white/35"
            name="email"
            placeholder="Invite by email"
            type="email"
            disabled={!canInvite}
          />
          <div className="flex items-center gap-3">
            <select
              className="h-11 flex-1 rounded-full bg-surface-container-lowest px-4 text-sm font-medium text-text dark:bg-dark-card dark:text-white"
              name="role"
              disabled={!canInvite}
              defaultValue="viewer"
            >
              <option value="viewer">Viewer</option>
              <option value="editor">Editor</option>
            </select>
            <button
              aria-label="Send invite"
              className="flex h-11 w-11 items-center justify-center rounded-full bg-secondary-container text-[#6d6356] dark:bg-white/10 dark:text-white disabled:opacity-60"
              disabled={!canInvite}
              type="submit"
            >
              <Icon className="h-4 w-4" name="send" />
            </button>
          </div>
          {!canInvite ? <p className="text-xs text-text/55 dark:text-white/55">Only owners can invite collaborators.</p> : null}
          {inviteStatus ? <p className="text-xs text-primary">{inviteStatus}</p> : null}
        </form>
      </div>
    </section>
  );
}

export default PlannerSummaryPanel;
