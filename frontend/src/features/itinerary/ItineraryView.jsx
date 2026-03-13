/*
Feature: Itinerary
File Purpose: Display generated itinerary
Owner: Jay
Dependencies: React
Last Updated: 2026-03-13
*/
import { itineraryDays } from "../../data/mockData";
import Icon from "../../components/Icon";

function ItineraryView({ compact = false }) {
  return (
    <section className={`section-shell flex h-full flex-col ${compact ? "" : "lg:w-[25rem]"}`}>
      <div className="mb-8 flex items-center justify-between">
        <div>
          <p className="label-md text-primary/65 dark:text-white/55">Trip timeline</p>
          <h2 className="mt-2 text-2xl font-bold">October 14 - 20</h2>
          <p className="mt-2 text-sm text-text/60 dark:text-white/60">7 days in Jaipur and Rajasthan</p>
        </div>
        <div className="flex -space-x-3">
          {["A", "J", "+2"].map((avatar) => (
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
        {itineraryDays.map((day, index) => (
          <div key={day.day} className="relative flex gap-5">
            {index < itineraryDays.length - 1 ? (
              <div className="absolute left-[1.2rem] top-12 h-[calc(100%+1.75rem)] w-px bg-primary/15" />
            ) : null}
            <div className="relative z-10 flex h-10 w-10 items-center justify-center rounded-full bg-primary text-sm font-semibold text-white shadow-lg shadow-primary/20">
              {day.day}
            </div>
            <div className="flex-1 space-y-4 pb-4">
              <div>
                <h3 className="text-xl font-semibold">{day.title}</h3>
                <p className="mt-1 text-sm text-text/55 dark:text-white/55">{day.date}</p>
              </div>
              {day.items.map((item) => (
                <div
                  key={`${day.day}-${item.time}-${item.label}`}
                  className="rounded-[1.75rem] bg-surface-container-lowest/90 p-5 shadow-ambient transition-transform hover:-translate-y-0.5 dark:bg-dark-card/90"
                >
                  <div className="flex items-center justify-between text-xs font-semibold uppercase tracking-label text-text/45 dark:text-white/45">
                    <span>{item.time}</span>
                    <Icon className="h-4 w-4" name="drag" />
                  </div>
                  <p className="mt-3 text-base font-medium">{item.label}</p>
                  <div className="mt-3 flex items-center gap-2 text-sm text-primary dark:text-white">
                    <Icon className="h-4 w-4" name="clock" />
                    <span>{item.travel}</span>
                  </div>
                </div>
              ))}
            </div>
          </div>
        ))}
      </div>

      <button className="primary-pill mt-8 w-full py-4 text-center" type="button">
        Confirm itinerary
      </button>
    </section>
  );
}

export default ItineraryView;
