/*
Feature: Profile
File Purpose: Render the user's trip portfolio without planner or chat tools
Owner: Jay
Dependencies: React, Fetch
Last Updated: 2026-03-13
*/
import { useEffect, useState } from "react";
import { Link } from "react-router-dom";
import { apiRequest } from "../../utils/apiClient";
import { getStoredUser } from "../../utils/session";

function TripCard({ trip }) {
  return (
    <article className="overflow-hidden rounded-[2rem] bg-surface-container-lowest shadow-ambient dark:bg-dark-card">
      <div className="h-56 w-full bg-[radial-gradient(circle_at_top_left,rgba(0,109,119,0.22),transparent_28%),radial-gradient(circle_at_bottom_right,rgba(140,37,0,0.18),transparent_24%),linear-gradient(135deg,rgba(241,233,223,0.95),rgba(223,236,238,0.9))]" />
      <div className="p-6">
        <p className="label-md text-primary/70 dark:text-white/55">{trip.dates}</p>
        <h3 className="mt-3 text-2xl font-bold">{trip.name}</h3>
        <p className="mt-3 text-sm text-text/60 dark:text-white/60">{trip.people}</p>
      </div>
    </article>
  );
}

function ProfileTripsPage() {
  const [trips, setTrips] = useState([]);
  const [error, setError] = useState("");
  const user = getStoredUser();

  useEffect(() => {
    async function loadTrips() {
      try {
        if (!user?.access_token) {
          return;
        }
        const response = await apiRequest("/trips/");
        setTrips(response);
      } catch (requestError) {
        setError(requestError.message);
      }
    }

    loadTrips();
  }, [user]);

  const upcomingTrips = trips.filter((trip) => trip.status === "draft");
  const archivedTrips = trips.filter((trip) => trip.status !== "draft");

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
          <h2 className="mt-3 text-3xl font-bold">{user?.email || "Guest traveler"}</h2>
          <p className="mt-4 max-w-md leading-8 text-text/65 dark:text-white/65">
            {user ? "Your saved trips stay synced with the backend." : "Login to keep your trip history in one place."}
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
          {upcomingTrips.map((trip) => (
            <Link key={trip.id} to={`/trip/${trip.id}`}>
              <TripCard
                trip={{
                  name: trip.destination_city,
                  dates: `${trip.duration_days} days`,
                  people: trip.preferences || "Curated preferences",
                }}
              />
            </Link>
          ))}
          {!upcomingTrips.length ? <p className="text-sm text-text/60 dark:text-white/60">No upcoming trips yet.</p> : null}
        </div>
      </section>

      <section className="mt-16">
        <div className="mb-8">
          <p className="label-md text-primary/70 dark:text-white/55">Past trips</p>
          <h2 className="mt-2 text-3xl font-bold">Places already lived through</h2>
        </div>
        <div className="grid gap-8 md:grid-cols-2">
          {archivedTrips.map((trip) => (
            <Link key={trip.id} to={`/trip/${trip.id}`}>
              <TripCard
                trip={{
                  name: trip.destination_city,
                  dates: `${trip.duration_days} days`,
                  people: trip.preferences || "Saved trip",
                }}
              />
            </Link>
          ))}
          {!archivedTrips.length ? <p className="text-sm text-text/60 dark:text-white/60">Generated trips remain here as your archive grows.</p> : null}
        </div>
      </section>

      <section className="mt-16">
      </section>
      {error ? <p className="mt-8 text-sm text-tertiary">{error}</p> : null}
    </main>
  );
}

export default ProfileTripsPage;
