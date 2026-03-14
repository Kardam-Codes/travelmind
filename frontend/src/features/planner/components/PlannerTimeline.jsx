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
  places = [],
  activities = [],
  hotels = [],
  route,
  selectedDay,
  selectedStopId,
  trip,
  tripRole,
}) {
  const days = itinerary?.days || [];
  const canEdit = tripRole === "owner" || tripRole === "editor";
  const palette = ["#FFE8D6", "#E0F2FE", "#FDE68A", "#EBD8FF", "#DCFCE7", "#FFE4E6"];

  function findLegForItem(item) {
    const stopIndex = route?.stops?.findIndex((stop) => stop.item_id === item.id) ?? -1;
    if (stopIndex < 0) {
      return null;
    }
    return route?.legs?.[stopIndex] || null;
  }

  function findImageForItem(item) {
    if (item.place_id) {
      return places.find((place) => place.id === item.place_id)?.image_url || "";
    }
    if (item.activity_id) {
      return activities.find((activity) => activity.id === item.activity_id)?.image_url || "";
    }
    if (item.hotel_id) {
      return hotels.find((hotel) => hotel.id === item.hotel_id)?.image_url || "";
    }
    return "";
  }

  const visibleDays = selectedDay == null ? days : days.filter((day) => day.day_number === selectedDay);

  return (
    <section className="flex min-h-[30rem] flex-col">
      <div className="mb-4">
        <p className="label-md text-primary/65 dark:text-white/55">Day-wise itinerary</p>
        <h2 className="mt-2 text-2xl font-bold">{trip ? `${trip.destination_city} plan` : "Trip timeline"}</h2>
      </div>

      <div className="space-y-6">
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
                    aria-label="Add stop"
                    className={`flex h-10 w-10 items-center justify-center rounded-full bg-secondary-container text-[#6d6356] transition dark:bg-white/10 dark:text-white ${
                      !canEdit ? "cursor-not-allowed opacity-60" : ""
                    }`}
                    onClick={() => {
                      if (canEdit) {
                        onAddItem?.(day.day_number);
                      }
                    }}
                    type="button"
                  >
                    <Icon className="h-4 w-4" name="plus" />
                  </button>
                  {isLockedByCurrentUser ? (
                    <button
                      aria-label="Unlock day"
                      className="flex h-10 w-10 items-center justify-center rounded-full bg-secondary-container text-[#6d6356] dark:bg-white/10 dark:text-white"
                      onClick={() => onUnlockDay?.(day.day_number)}
                      type="button"
                    >
                      <Icon className="h-4 w-4" name="unlock" />
                    </button>
                  ) : isLocked ? (
                    <span className="flex h-10 w-10 items-center justify-center rounded-full bg-secondary-container text-[#6d6356] opacity-70 dark:bg-white/10 dark:text-white">
                      <Icon className="h-4 w-4" name="lock" />
                    </span>
                  ) : (
                    <button
                      aria-label="Lock day"
                      className={`flex h-10 w-10 items-center justify-center rounded-full bg-secondary-container text-[#6d6356] transition dark:bg-white/10 dark:text-white ${
                        !canEdit ? "cursor-not-allowed opacity-60" : ""
                      }`}
                      onClick={() => {
                        if (canEdit) {
                          onLockDay?.(day.day_number);
                        }
                      }}
                      type="button"
                    >
                      <Icon className="h-4 w-4" name="lock" />
                    </button>
                  )}
                </div>
              </div>

              {!isCollapsed ? (
                <div className="mt-5">
                  <div className="hide-scrollbar flex gap-4 overflow-x-auto pb-2">
                    {day.items.map((item, itemIndex) => {
                      const leg = findLegForItem(item);
                      const isSelected = selectedStopId === item.id;
                      const imageUrl = findImageForItem(item);
                      const cardTone = palette[itemIndex % palette.length];

                      return (
                        <button
                          key={`${day.day_number}-${item.id}`}
                          className={`relative flex w-64 flex-shrink-0 flex-col rounded-[1.5rem] border p-4 text-left transition ${
                            isSelected
                              ? "border-tertiary shadow-ambient dark:border-white/20"
                              : "border-transparent hover:border-primary/20"
                          }`}
                          onClick={() => onSelectStop?.(item.id)}
                          style={{ backgroundColor: cardTone }}
                          type="button"
                        >
                          {imageUrl ? (
                            <img alt={item.title} className="mb-3 h-28 w-full rounded-[1.25rem] object-cover" loading="lazy" src={imageUrl} />
                          ) : null}
                          <div className="text-xs font-semibold uppercase tracking-label text-text/55">
                            {item.item_type} - Stop {itemIndex + 1}
                          </div>
                          <p className="mt-2 text-base font-semibold">{item.title}</p>
                          <p className="mt-2 text-sm text-text/70">{item.description || "Scheduled stop"}</p>
                          {leg ? (
                            <p className="mt-3 inline-flex items-center gap-2 rounded-full bg-white/70 px-3 py-2 text-xs font-semibold text-text/65">
                              <Icon className="h-4 w-4" name="route" />
                              {leg.distance_text || "Distance pending"} - {leg.duration_text || "Duration pending"}
                            </p>
                          ) : null}
                        </button>
                      );
                    })}
                  </div>
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
