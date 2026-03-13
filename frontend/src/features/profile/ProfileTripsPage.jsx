/*
Feature: Profile
File Purpose: Render the user's trip portfolio without planner or chat tools
Owner: Jay
Dependencies: React, mockData, Wishlist
Last Updated: 2026-03-13
*/
import { profileTrips } from "../../data/mockData";
import Wishlist from "../wishlist/Wishlist";

function TripCard({ trip }) {
  return (
    <article className="overflow-hidden rounded-[2rem] bg-surface-container-lowest shadow-ambient dark:bg-dark-card">
      <img alt={trip.name} className="h-56 w-full object-cover" src={trip.image} />
      <div className="p-6">
        <p className="label-md text-primary/70 dark:text-white/55">{trip.dates}</p>
        <h3 className="mt-3 text-2xl font-bold">{trip.name}</h3>
        <p className="mt-3 text-sm text-text/60 dark:text-white/60">{trip.people}</p>
      </div>
    </article>
  );
}

function ProfileTripsPage() {
  return (
    <main className="mx-auto max-w-7xl px-4 pb-20 pt-10 md:px-6">
      <section className="grid gap-8 lg:grid-cols-[1fr,0.9fr]">
        <div>
          <p className="label-md text-tertiary">Profile and trips</p>
          <h1 className="mt-3 max-w-3xl text-5xl font-extrabold leading-[1.05] text-balance md:text-[3.5rem]">
            A personal archive of what is next, what is done, and what still lingers.
          </h1>
        </div>
        <div className="section-shell">
          <p className="label-md text-primary/70 dark:text-white/55">Profile snapshot</p>
          <h2 className="mt-3 text-3xl font-bold">Jay Bardolia</h2>
          <p className="mt-4 max-w-md leading-8 text-text/65 dark:text-white/65">
            Frontend-focused traveler with a preference for map-led planning, quieter stays, and editorial trip curation.
          </p>
        </div>
      </section>

      <section className="mt-16">
        <div className="mb-8 flex items-end justify-between">
          <div>
            <p className="label-md text-primary/70 dark:text-white/55">Upcoming trips</p>
            <h2 className="mt-2 text-3xl font-bold">Trips on the horizon</h2>
          </div>
        </div>
        <div className="grid gap-8 md:grid-cols-2">
          {profileTrips.upcoming.map((trip) => (
            <TripCard key={trip.name} trip={trip} />
          ))}
        </div>
      </section>

      <section className="mt-16">
        <div className="mb-8">
          <p className="label-md text-primary/70 dark:text-white/55">Past trips</p>
          <h2 className="mt-2 text-3xl font-bold">Places already lived through</h2>
        </div>
        <div className="grid gap-8 md:grid-cols-2">
          {profileTrips.past.map((trip) => (
            <TripCard key={trip.name} trip={trip} />
          ))}
        </div>
      </section>

      <section className="mt-16">
        <Wishlist />
      </section>
    </main>
  );
}

export default ProfileTripsPage;
