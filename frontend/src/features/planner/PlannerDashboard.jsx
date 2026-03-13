/*
Feature: Planner Dashboard
File Purpose: Render the AI-first trip planner with chat, map, and itinerary builder
Owner: Jay
Dependencies: CollaborationPanel, ItineraryView, mockData, Icon
Last Updated: 2026-03-13
*/
import CollaborationPanel from "../collaboration/CollaborationPanel";
import ItineraryView from "../itinerary/ItineraryView";
import { mapPlaces } from "../../data/mockData";
import Icon from "../../components/Icon";

function PlannerDashboard() {
  return (
    <main className="mx-auto max-w-[1500px] px-4 pb-12 pt-8 md:px-6">
      <section className="grid gap-6 xl:grid-cols-[22rem,minmax(0,1fr),25rem]">
        <CollaborationPanel />

        <div className="section-shell relative min-h-[700px] overflow-hidden p-0">
          <div className="absolute inset-0 bg-[radial-gradient(circle_at_top_left,rgba(0,109,119,0.18),transparent_28%),radial-gradient(circle_at_bottom_right,rgba(140,37,0,0.14),transparent_26%)]" />
          <div className="absolute inset-4 rounded-[2rem] bg-[url('https://commons.wikimedia.org/wiki/Special:Redirect/file/Amber%20Fort-Jaipur-India0010.JPG')] bg-cover bg-center opacity-40 dark:opacity-25" />
          <svg className="absolute inset-0 h-full w-full" viewBox="0 0 900 700">
            <path
              d="M170 420 C 260 280, 460 260, 590 350 S 760 460, 810 220"
              fill="none"
              stroke="rgba(0,83,91,0.45)"
              strokeDasharray="10 12"
              strokeWidth="4"
            />
          </svg>

          <div className="absolute left-8 top-8 flex gap-3">
            {["map", "route", "pin"].map((control) => (
              <button
                key={control}
                className="glass-panel flex h-12 w-12 items-center justify-center rounded-full text-text shadow-ambient dark:text-white"
                type="button"
              >
                <Icon name={control} />
              </button>
            ))}
          </div>

          <div className="glass-panel absolute bottom-8 left-8 max-w-sm rounded-[1.75rem] p-5 shadow-float">
            <p className="label-md text-primary/70 dark:text-white/55">Pinned highlight</p>
            <h2 className="mt-2 text-2xl font-bold">Samode Haveli</h2>
            <p className="mt-3 text-sm leading-7 text-text/70 dark:text-white/70">
              Riverside arrival, private boat access, and an easy transition into a quieter first evening.
            </p>
            <div className="mt-4 flex items-center gap-4 text-sm">
              <span className="rounded-full bg-secondary-container px-3 py-2 text-tertiary dark:bg-white/10 dark:text-white">
                Top choice
              </span>
              <span className="text-primary dark:text-white">20 min from airport</span>
            </div>
          </div>

          {mapPlaces.map((place) => (
            <div key={place.id} className="absolute" style={{ left: place.x, top: place.y }}>
              <div className="group relative">
                <button
                  className={`flex h-12 w-12 items-center justify-center rounded-full ${place.accent} text-sm font-semibold text-white shadow-float transition-transform hover:scale-105`}
                  type="button"
                >
                  {place.id}
                </button>
                <div className="glass-panel pointer-events-none absolute left-1/2 top-14 w-48 -translate-x-1/2 rounded-full px-4 py-3 text-center text-xs font-semibold opacity-0 shadow-ambient transition-opacity group-hover:opacity-100">
                  {place.title}
                </div>
              </div>
            </div>
          ))}
        </div>

        <ItineraryView />
      </section>
    </main>
  );
}

export default PlannerDashboard;
