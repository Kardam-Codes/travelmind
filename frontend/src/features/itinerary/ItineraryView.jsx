/*
Feature: Itinerary
File Purpose: Display generated itinerary
Owner: Jay
Dependencies: React
Last Updated: 2026-03-13
*/
import Icon from "../../components/Icon";
import { formatTripRange } from "../../utils/tripPresentation";

function ItineraryView({
  compact = false,
  currentUserId = "guest",
  itinerary,
  trip,
  operationError = "",
  onAddItem,
  onLockDay,
  onMoveItem,
  onRemoveItem,
  onUnlockDay,
  onUpdateItem,
}) {
  const days = itinerary?.days || [];

  return (
    <section className={`section-shell flex h-full flex-col ${compact ? "" : "lg:w-[25rem]"}`}>
      <div className="mb-8 flex items-center justify-between">
        <div>
          <p className="label-md text-primary/65 dark:text-white/55">Trip timeline</p>
          <h2 className="mt-2 text-2xl font-bold">{trip ? trip.destination_city : "Trip plan"}</h2>
          <p className="mt-2 text-sm text-text/60 dark:text-white/60">
            {trip ? formatTripRange(trip) : "Create a trip to see the generated itinerary"}
          </p>
          {trip ? (
            <p className="mt-2 text-xs text-text/50 dark:text-white/50">
              Version {trip.version} {trip.locked_day_number ? `| Day ${trip.locked_day_number} locked by ${trip.locked_by}` : ""}
            </p>
          ) : null}
        </div>
        <div className="flex -space-x-3">
          {[trip?.destination_city?.[0] || "T", String(trip?.duration_days || 0), "AI"].map((avatar) => (
            <div
              key={avatar}
              className="flex h-11 w-11 items-center justify-center rounded-full bg-surface-container-lowest text-sm font-semibold text-primary shadow-ambient dark:bg-dark-card dark:text-white"
            >
              {avatar}
            </div>
          ))}
        </div>
      </div>

      <div className="hide-scrollbar flex-1 space-y-10 overflow-y-auto pr-2">
        {days.map((day, index) => {
          const isLocked = trip?.locked_day_number === day.day_number && trip?.locked_by && trip.locked_by !== currentUserId;
          const isLockedByCurrentUser = trip?.locked_day_number === day.day_number && trip?.locked_by === currentUserId;

          return (
            <div key={day.day_number} className="relative flex gap-5">
              {index < days.length - 1 ? (
                <div className="absolute left-[1.2rem] top-12 h-[calc(100%+1.75rem)] w-px bg-primary/15" />
              ) : null}
              <div className="relative z-10 flex h-10 w-10 items-center justify-center rounded-full bg-primary text-sm font-semibold text-white shadow-lg shadow-primary/20">
                {String(day.day_number).padStart(2, "0")}
              </div>
              <div className="flex-1 space-y-4 pb-4">
                <div className="flex items-center justify-between gap-4">
                  <div>
                    <h3 className="text-xl font-semibold">Day {day.day_number}</h3>
                    <p className="mt-1 text-sm text-text/55 dark:text-white/55">{trip?.destination_city}</p>
                  </div>
                  <div className="flex gap-2">
                      <button className="secondary-pill px-4 py-2 text-xs" onClick={() => onAddItem?.(day.day_number)} type="button">
                        Add
                      </button>
                    {isLockedByCurrentUser ? (
                      <button className="secondary-pill px-4 py-2 text-xs" onClick={() => onUnlockDay?.(day.day_number)} type="button">
                        Unlock
                      </button>
                    ) : isLocked ? (
                      <span className="secondary-pill px-4 py-2 text-xs opacity-70">Locked</span>
                    ) : (
                      <button className="secondary-pill px-4 py-2 text-xs" onClick={() => onLockDay?.(day.day_number)} type="button">
                        Lock
                      </button>
                    )}
                  </div>
                </div>
                {day.items.map((item, itemIndex) => (
                  <div
                    key={`${day.day_number}-${item.id}`}
                    className="rounded-[1.75rem] bg-surface-container-lowest/90 p-5 shadow-ambient transition-transform hover:-translate-y-0.5 dark:bg-dark-card/90"
                  >
                    <div className="flex items-center justify-between text-xs font-semibold uppercase tracking-label text-text/45 dark:text-white/45">
                      <span>{item.item_type}</span>
                      <Icon className="h-4 w-4" name="drag" />
                    </div>
                    <p className="mt-3 text-base font-medium">{item.title}</p>
                    <div className="mt-3 flex items-center gap-2 text-sm text-primary dark:text-white">
                      <Icon className="h-4 w-4" name="clock" />
                      <span>{item.description || "Scheduled stop"}</span>
                    </div>
                    <div className="mt-4 flex flex-wrap gap-2 text-xs">
                      <button className="secondary-pill px-3 py-2" disabled={Boolean(isLocked)} onClick={() => onUpdateItem?.(item)} type="button">
                        Edit
                      </button>
                      <button className="secondary-pill px-3 py-2" disabled={Boolean(isLocked) || itemIndex === 0} onClick={() => onMoveItem?.(item.id, day.day_number, itemIndex)} type="button">
                        Up
                      </button>
                      <button
                        className="secondary-pill px-3 py-2"
                        disabled={Boolean(isLocked) || itemIndex === day.items.length - 1}
                        onClick={() => onMoveItem?.(item.id, day.day_number, itemIndex + 2)}
                        type="button"
                      >
                        Down
                      </button>
                      <button className="secondary-pill px-3 py-2" disabled={Boolean(isLocked)} onClick={() => onRemoveItem?.(item.id)} type="button">
                        Remove
                      </button>
                    </div>
                  </div>
                ))}
              </div>
            </div>
          );
        })}
        {!days.length ? <p className="text-sm text-text/60 dark:text-white/60">The itinerary appears here after a trip is generated.</p> : null}
        {operationError ? <p className="text-sm text-tertiary">{operationError}</p> : null}
      </div>

      <button className="primary-pill mt-8 w-full py-4 text-center" type="button">
        Confirm itinerary
      </button>
    </section>
  );
}

export default ItineraryView;
