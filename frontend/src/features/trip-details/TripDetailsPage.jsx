/*
Feature: Trip Details
File Purpose: Render the detailed trip summary with overview, itinerary, map, and budget tabs
Owner: Jay
Dependencies: React, mockData, Icon
Last Updated: 2026-03-13
*/
import { useState } from "react";
import { budgetBreakdown, itineraryDays, mapPlaces } from "../../data/mockData";

const tabs = ["Overview", "Itinerary", "Map", "Budget"];

function TripDetailsPage() {
  const [activeTab, setActiveTab] = useState("Overview");

  return (
    <main className="mx-auto max-w-7xl px-4 pb-20 pt-10 md:px-6">
      <section className="relative overflow-hidden rounded-[2.5rem] shadow-float">
        <img
          alt="Jaipur trip"
          className="h-[28rem] w-full object-cover"
          src="https://commons.wikimedia.org/wiki/Special:Redirect/file/Hawa%20Mahal-Jaipur-Rajasthan.jpg"
        />
        <div className="absolute inset-0 bg-gradient-to-t from-black/70 via-black/20 to-transparent" />
        <div className="absolute bottom-0 left-0 right-0 p-8 text-white md:p-10">
          <p className="label-md text-white/70">Trip details</p>
          <h1 className="mt-3 text-5xl font-extrabold">Jaipur Curations</h1>
          <div className="mt-5 flex flex-wrap gap-3 text-sm">
            <span className="glass-panel rounded-full px-4 py-3">October 14 - 20</span>
            <span className="glass-panel rounded-full px-4 py-3">4 participants</span>
            <span className="glass-panel rounded-full px-4 py-3">Jaipur, India</span>
          </div>
        </div>
      </section>

      <section className="mt-10 flex flex-wrap gap-3">
        {tabs.map((tab) => (
          <button
            key={tab}
            className={activeTab === tab ? "primary-pill" : "secondary-pill"}
            onClick={() => setActiveTab(tab)}
            type="button"
          >
            {tab}
          </button>
        ))}
      </section>

      <section className="mt-10">
        {activeTab === "Overview" ? (
          <div className="grid gap-6 lg:grid-cols-[1.1fr,0.9fr]">
            <div className="card-surface space-y-5">
              <p className="label-md text-tertiary">Trip summary</p>
              <h2 className="text-3xl font-bold">A calm, route-aware week in Jaipur.</h2>
              <p className="max-w-2xl text-lg leading-8 text-text/65 dark:text-white/65">
                This trip balances quiet stays, early cultural experiences, and highly walkable evenings. The purpose here is review, not editing.
              </p>
            </div>
            <div className="section-shell">
              <p className="label-md text-primary/70 dark:text-white/55">Participants</p>
              <div className="mt-5 flex gap-3">
                {["Jay", "Misha", "Kardam", "Yug"].map((person) => (
                  <div key={person} className="rounded-full bg-surface-container-lowest px-4 py-3 text-sm dark:bg-dark-card">
                    {person}
                  </div>
                ))}
              </div>
            </div>
          </div>
        ) : null}

        {activeTab === "Itinerary" ? (
          <div className="grid gap-5">
            {itineraryDays.map((day) => (
              <article key={day.day} className="card-surface grid gap-6 lg:grid-cols-[7rem,1fr]">
                <div className="flex items-start gap-4">
                  <div className="flex h-14 w-14 items-center justify-center rounded-full bg-primary text-lg font-semibold text-white">
                    {day.day}
                  </div>
                  <div>
                    <h3 className="text-xl font-bold">{day.title}</h3>
                    <p className="mt-2 text-sm text-text/55 dark:text-white/55">{day.date}</p>
                  </div>
                </div>
                <div className="grid gap-4 md:grid-cols-2">
                  {day.items.map((item) => (
                    <div key={`${day.day}-${item.label}`} className="rounded-[1.5rem] bg-surface-container-low px-5 py-5 dark:bg-dark-low">
                      <p className="label-md text-primary/70 dark:text-white/55">{item.time}</p>
                      <p className="mt-2 font-medium">{item.label}</p>
                      <p className="mt-3 text-sm text-text/55 dark:text-white/55">{item.travel}</p>
                    </div>
                  ))}
                </div>
              </article>
            ))}
          </div>
        ) : null}

        {activeTab === "Map" ? (
          <div className="section-shell relative min-h-[34rem] overflow-hidden">
            <div className="absolute inset-4 rounded-[2rem] bg-[radial-gradient(circle_at_top_left,rgba(0,109,119,0.16),transparent_28%),radial-gradient(circle_at_bottom_right,rgba(140,37,0,0.12),transparent_25%)] dark:bg-[radial-gradient(circle_at_top_left,rgba(0,109,119,0.25),transparent_28%),radial-gradient(circle_at_bottom_right,rgba(140,37,0,0.20),transparent_25%)]" />
            {mapPlaces.map((place) => (
              <div key={place.id} className="absolute" style={{ left: place.x, top: place.y }}>
                <div className="glass-panel rounded-full px-4 py-3 text-sm font-semibold shadow-ambient">{place.title}</div>
              </div>
            ))}
          </div>
        ) : null}

        {activeTab === "Budget" ? (
          <div className="grid gap-6 md:grid-cols-2 xl:grid-cols-4">
            {budgetBreakdown.map((item) => (
              <article key={item.label} className="card-surface">
                <p className="label-md text-primary/70 dark:text-white/55">{item.label}</p>
                <h3 className="mt-4 text-3xl font-bold">{item.value}</h3>
                <p className="mt-3 text-sm leading-7 text-text/60 dark:text-white/60">
                  Estimated category spend for the current curated plan.
                </p>
              </article>
            ))}
          </div>
        ) : null}
      </section>
    </main>
  );
}

export default TripDetailsPage;
