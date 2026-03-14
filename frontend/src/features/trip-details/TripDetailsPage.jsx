/*
Feature: Trip Details
File Purpose: Render the detailed trip summary with overview, itinerary, map, and budget tabs
Owner: Jay
Dependencies: React, Fetch
Last Updated: 2026-03-13
*/
import { useEffect, useState } from "react";
import { useParams } from "react-router-dom";
import TripMap from "../../components/TripMap";
import { apiRequest } from "../../utils/apiClient";
import { getStoredUser } from "../../utils/session";

const tabs = ["Overview", "Itinerary", "Map", "Budget"];

function TripDetailsPage() {
  const { tripId } = useParams();
  const [activeTab, setActiveTab] = useState("Overview");
  const [dashboard, setDashboard] = useState(null);
  const [mapRoute, setMapRoute] = useState(null);
  const [message, setMessage] = useState("");

  useEffect(() => {
    async function loadDashboard() {
      try {
        const response = await apiRequest(`/trips/${tripId}/dashboard`);
        setDashboard(response);
      } catch (requestError) {
        setMessage(requestError.message);
      }
    }

    async function loadMapRoute() {
      try {
        const response = await apiRequest(`/maps/trips/${tripId}/route`);
        setMapRoute(response);
      } catch (requestError) {
        setMapRoute({
          provider_status: "unavailable",
          warning: requestError.message,
          path: [],
          stops: [],
        });
      }
    }

    loadDashboard();
    loadMapRoute();
  }, [tripId]);

  async function addToWishlist(itemId, itemType) {
    const user = getStoredUser();
    if (!user) {
      setMessage("Login before saving items to the wishlist.");
      return;
    }

    try {
      await apiRequest("/wishlist/", {
        method: "POST",
        body: JSON.stringify({
          user_id: String(user.user_id),
          item_id: itemId,
          item_type: itemType,
        }),
      });
      setMessage("Saved to wishlist.");
    } catch (requestError) {
      setMessage(requestError.message);
    }
  }

  const trip = dashboard?.trip;
  const budgetBreakdown = [
    { label: "Budget", value: trip?.budget_total ? `Rs ${trip.budget_total}` : "Flexible" },
    { label: "Hotels", value: String(dashboard?.hotels?.length || 0) },
    { label: "Places", value: String(dashboard?.places?.length || 0) },
    { label: "Activities", value: String(dashboard?.activities?.length || 0) },
  ];

  return (
    <main className="mx-auto max-w-7xl px-4 pb-20 pt-10 md:px-6">
      <section className="relative overflow-hidden rounded-[2.5rem] shadow-float">
        <div className="h-[28rem] w-full bg-[radial-gradient(circle_at_top_left,rgba(0,109,119,0.28),transparent_32%),radial-gradient(circle_at_bottom_right,rgba(140,37,0,0.22),transparent_28%),linear-gradient(135deg,rgba(241,233,223,0.95),rgba(223,236,238,0.9))]" />
        <div className="absolute inset-0 bg-gradient-to-t from-black/70 via-black/20 to-transparent" />
        <div className="absolute bottom-0 left-0 right-0 p-8 text-white md:p-10">
          <p className="label-md text-white/70">Trip details</p>
          <h1 className="mt-3 text-5xl font-extrabold">{trip ? `${trip.destination_city} Curations` : "Loading trip"}</h1>
          <div className="mt-5 flex flex-wrap gap-3 text-sm">
            <span className="glass-panel rounded-full px-4 py-3">{trip?.duration_days || 0} days</span>
            <span className="glass-panel rounded-full px-4 py-3">{trip?.traveler_type || "curated"}</span>
            <span className="glass-panel rounded-full px-4 py-3">{trip ? `${trip.destination_city}, ${trip.state}` : "TravelMind"}</span>
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
        {message ? <p className="mb-6 text-sm text-tertiary">{message}</p> : null}
        {activeTab === "Overview" ? (
          <div className="grid gap-6 lg:grid-cols-[1.1fr,0.9fr]">
            <div className="card-surface space-y-5">
              <p className="label-md text-tertiary">Trip summary</p>
              <h2 className="text-3xl font-bold">{trip ? `A route-aware plan for ${trip.destination_city}.` : "Trip summary"}</h2>
              <p className="max-w-2xl text-lg leading-8 text-text/65 dark:text-white/65">
                {trip?.preferences
                  ? `Preferences applied: ${trip.preferences}.`
                  : "This trip balances travel time, city coverage, and current budget guidance."}
              </p>
              <div className="grid gap-4 md:grid-cols-2">
                {(dashboard?.places || []).slice(0, 4).map((place) => (
                  <div key={place.id} className="rounded-[1.5rem] bg-surface-container-low px-5 py-5 dark:bg-dark-low">
                    <p className="label-md text-primary/70 dark:text-white/55">{place.category}</p>
                    <p className="mt-2 font-medium">{place.name}</p>
                    <button className="mt-4 text-sm font-semibold text-primary dark:text-white" onClick={() => addToWishlist(place.id, "place")} type="button">
                      Save to wishlist
                    </button>
                  </div>
                ))}
              </div>
            </div>
            <div className="section-shell">
              <p className="label-md text-primary/70 dark:text-white/55">Recommended stays</p>
              <div className="mt-5 grid gap-3">
                {(dashboard?.hotels || []).slice(0, 3).map((hotel) => (
                  <div key={hotel.id} className="rounded-[1.5rem] bg-surface-container-lowest px-4 py-4 text-sm dark:bg-dark-card">
                    <p className="font-semibold">{hotel.name}</p>
                    <p className="mt-2 text-text/60 dark:text-white/60">
                      {hotel.nearby_area || hotel.city} | {hotel.budget_category || "curated"} | Rs {hotel.price_per_night || "N/A"}
                    </p>
                    <button className="mt-3 text-sm font-semibold text-primary dark:text-white" onClick={() => addToWishlist(hotel.id, "hotel")} type="button">
                      Save to wishlist
                    </button>
                  </div>
                ))}
              </div>
            </div>
          </div>
        ) : null}

        {activeTab === "Itinerary" ? (
          <div className="grid gap-5">
            {(dashboard?.itinerary?.days || []).map((day) => (
              <article key={day.day_number} className="card-surface grid gap-6 lg:grid-cols-[7rem,1fr]">
                <div className="flex items-start gap-4">
                  <div className="flex h-14 w-14 items-center justify-center rounded-full bg-primary text-lg font-semibold text-white">
                    {String(day.day_number).padStart(2, "0")}
                  </div>
                  <div>
                    <h3 className="text-xl font-bold">Day {day.day_number}</h3>
                    <p className="mt-2 text-sm text-text/55 dark:text-white/55">{trip?.destination_city}</p>
                  </div>
                </div>
                <div className="grid gap-4 md:grid-cols-2">
                  {day.items.map((item) => (
                    <div key={item.id} className="rounded-[1.5rem] bg-surface-container-low px-5 py-5 dark:bg-dark-low">
                      <p className="label-md text-primary/70 dark:text-white/55">{item.item_type}</p>
                      <p className="mt-2 font-medium">{item.title}</p>
                      <p className="mt-3 text-sm text-text/55 dark:text-white/55">{item.description}</p>
                    </div>
                  ))}
                </div>
              </article>
            ))}
          </div>
        ) : null}

        {activeTab === "Map" ? (
          <div className="section-shell">
            <TripMap className="min-h-[34rem]" fallbackMessage={mapRoute?.warning || ""} places={dashboard?.places || []} route={mapRoute} />
          </div>
        ) : null}

        {activeTab === "Budget" ? (
          <div className="grid gap-6 md:grid-cols-2 xl:grid-cols-4">
            {budgetBreakdown.map((item) => (
              <article key={item.label} className="card-surface">
                <p className="label-md text-primary/70 dark:text-white/55">{item.label}</p>
                <h3 className="mt-4 text-3xl font-bold">{item.value}</h3>
                <p className="mt-3 text-sm leading-7 text-text/60 dark:text-white/60">
                  Estimated category coverage for the current curated plan.
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
