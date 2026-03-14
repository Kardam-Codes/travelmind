import Icon from "../../../components/Icon";

function PlannerTimeline({
  collapsedDays,
  currentUserId,
  itinerary,
  onAddItem,
  onLockDay,
  onMoveItem,
  onRemoveItem,
  onSelectStop,
  onToggleDay,
  onUnlockDay,
  onUpdateItem,
  operationError,
  route,
  selectedDay,
  selectedStopId,
  trip,
  tripRole,
}) {
  const days = itinerary?.days || [];
  const canEdit = tripRole === "owner" || tripRole === "editor";

  function findLegForItem(item) {
    const stopIndex = route?.stops?.findIndex((stop) => stop.item_id === item.id) ?? -1;
    if (stopIndex < 0) {
      return null;
    }
    return route?.legs?.[stopIndex] || null;
  }

  const visibleDays = selectedDay == null ? days : days.filter((day) => day.day_number === selectedDay);

  return (
    <section className="section-shell flex min-h-[48rem] flex-col">
      <div className="mb-6 flex items-center justify-between gap-4">
        <div>
          <p className="label-md text-primary/65 dark:text-white/55">Timeline rail</p>
          <h2 className="mt-2 text-2xl font-bold">{trip ? `${trip.destination_city} itinerary` : "Trip timeline"}</h2>
          <p className="mt-2 text-sm text-text/60 dark:text-white/60">Structured day cards, route-aware stop selection, and confirmed editing controls.</p>
        </div>
        <div className="rounded-[1.25rem] bg-surface-container-lowest px-4 py-3 text-sm dark:bg-dark-card">
          <p className="label-md text-text/45 dark:text-white/45">Route status</p>
          <p className="mt-1 font-semibold capitalize">{route?.provider_status?.replaceAll("_", " ") || "Pending"}</p>
        </div>
      </div>

      <div className="hide-scrollbar flex-1 space-y-5 overflow-y-auto pr-2">
        {visibleDays.map((day) => {
          const isLocked = trip?.locked_day_number === day.day_number && trip?.locked_by && trip.locked_by !== currentUserId;
          const isLockedByCurrentUser = trip?.locked_day_number === day.day_number && trip?.locked_by === currentUserId;
          const isCollapsed = collapsedDays[day.day_number];

          return (
            <article key={day.day_number} className="rounded-[1.75rem] bg-surface-container-lowest/90 p-5 shadow-ambient dark:bg-dark-card/90">
              <div className="flex flex-wrap items-start justify-between gap-4">
                <button className="text-left" onClick={() => onToggleDay(day.day_number)} type="button">
                  <p className="label-md text-primary/65 dark:text-white/55">Day {String(day.day_number).padStart(2, "0")}</p>
                  <h3 className="mt-2 text-xl font-semibold">{trip?.destination_city}</h3>
                  <p className="mt-2 text-sm text-text/55 dark:text-white/55">{day.items.length} stops planned</p>
                </button>
                <div className="flex flex-wrap gap-2">
                  <button
                    className={`secondary-pill px-4 py-2 text-xs ${!canEdit ? "cursor-not-allowed opacity-60" : ""}`}
                    onClick={() => {
                      if (canEdit) {
                        onAddItem?.(day.day_number);
                      }
                    }}
                    type="button"
                  >
                    Add stop
                  </button>
                  {isLockedByCurrentUser ? (
                    <button className="secondary-pill px-4 py-2 text-xs" onClick={() => onUnlockDay?.(day.day_number)} type="button">
                      Unlock day
                    </button>
                  ) : isLocked ? (
                    <span className="secondary-pill px-4 py-2 text-xs opacity-70">Locked</span>
                  ) : (
                    <button
                      className={`secondary-pill px-4 py-2 text-xs ${!canEdit ? "cursor-not-allowed opacity-60" : ""}`}
                      onClick={() => {
                        if (canEdit) {
                          onLockDay?.(day.day_number);
                        }
                      }}
                      type="button"
                    >
                      Lock day
                    </button>
                  )}
                </div>
              </div>

              {!isCollapsed ? (
                <div className="mt-5 space-y-4">
                  {day.items.map((item, itemIndex) => {
                    const leg = findLegForItem(item);
                    const isSelected = selectedStopId === item.id;

                    return (
                      <button
                        key={`${day.day_number}-${item.id}`}
                        className={`w-full rounded-[1.5rem] border px-4 py-4 text-left transition ${
                          isSelected
                            ? "border-tertiary bg-secondary-container/70 shadow-ambient dark:border-white/20 dark:bg-white/10"
                            : "border-transparent bg-surface-container-low/80 hover:border-primary/20 dark:bg-dark-low/80"
                        }`}
                        onClick={() => onSelectStop?.(item.id)}
                        type="button"
                      >
                        <div className="flex flex-wrap items-start justify-between gap-4">
                          <div>
                            <div className="flex items-center gap-2 text-xs font-semibold uppercase tracking-label text-text/45 dark:text-white/45">
                              <span>{item.item_type}</span>
                              <span>•</span>
                              <span>Stop {itemIndex + 1}</span>
                            </div>
                            <p className="mt-2 text-base font-semibold">{item.title}</p>
                            <p className="mt-2 text-sm leading-7 text-text/70 dark:text-white/70">{item.description || "Scheduled stop"}</p>
                            {leg ? (
                              <p className="mt-3 inline-flex items-center gap-2 rounded-full bg-surface-container-lowest px-3 py-2 text-xs font-semibold text-text/65 dark:bg-dark-card dark:text-white/70">
                                <Icon className="h-4 w-4" name="route" />
                                {leg.distance_text || "Distance pending"} • {leg.duration_text || "Duration pending"}
                              </p>
                            ) : null}
                          </div>
                          <div className="flex flex-wrap gap-2">
                            <span className="rounded-full bg-surface-container-lowest px-3 py-2 text-xs font-semibold text-primary dark:bg-dark-card dark:text-white">
                              {isSelected ? "Selected" : "View"}
                            </span>
                          </div>
                        </div>
                        <div className="mt-4 flex flex-wrap gap-2 text-xs">
                          <span
                            className={`secondary-pill px-3 py-2 ${isLocked || !canEdit ? "cursor-not-allowed opacity-60" : ""}`}
                            onClick={(event) => {
                              event.stopPropagation();
                              if (!isLocked && canEdit) {
                                onUpdateItem?.(item);
                              }
                            }}
                          >
                            Edit
                          </span>
                          <span
                            className={`secondary-pill px-3 py-2 ${
                              isLocked || itemIndex === 0 || !canEdit ? "cursor-not-allowed opacity-60" : ""
                            }`}
                            onClick={(event) => {
                              event.stopPropagation();
                              if (!isLocked && itemIndex !== 0 && canEdit) {
                                onMoveItem?.(item.id, day.day_number, itemIndex);
                              }
                            }}
                          >
                            Move up
                          </span>
                          <span
                            className={`secondary-pill px-3 py-2 ${
                              isLocked || itemIndex === day.items.length - 1 || !canEdit ? "cursor-not-allowed opacity-60" : ""
                            }`}
                            onClick={(event) => {
                              event.stopPropagation();
                              if (!isLocked && itemIndex !== day.items.length - 1 && canEdit) {
                                onMoveItem?.(item.id, day.day_number, itemIndex + 2);
                              }
                            }}
                          >
                            Move down
                          </span>
                          <span
                            className={`secondary-pill px-3 py-2 ${isLocked || !canEdit ? "cursor-not-allowed opacity-60" : ""}`}
                            onClick={(event) => {
                              event.stopPropagation();
                              if (!isLocked && canEdit) {
                                onRemoveItem?.(item.id);
                              }
                            }}
                          >
                            Remove
                          </span>
                        </div>
                      </button>
                    );
                  })}
                </div>
              ) : null}
            </article>
          );
        })}

        {!visibleDays.length ? <p className="text-sm text-text/60 dark:text-white/60">No itinerary days match the current filter.</p> : null}
        {operationError ? <p className="text-sm text-tertiary">{operationError}</p> : null}
      </div>
    </section>
  );
}

export default PlannerTimeline;
