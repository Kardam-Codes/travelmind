/*
Feature: First Trip
File Purpose: Dedicated "Plan your first trip" experience with a focused input
Owner: Jay
Dependencies: TripInput, Icon, apiClient
Last Updated: 2026-03-15
*/
import { useEffect, useState } from "react";
import { Link, useNavigate } from "react-router-dom";
import Icon from "../../components/Icon";
import TripInput from "../trip-input/TripInput";
import { apiRequest } from "../../utils/apiClient";
import { getStoredUser, setActiveTripId } from "../../utils/session";
import { DEMO_PROMPT, getDemoLabel, getDemoMode, setDemoMode } from "../../utils/demo";

function FirstTripPage() {
  const navigate = useNavigate();
  const [tripQuery, setTripQuery] = useState("");
  const [demoMode, setDemoModeState] = useState(() => getDemoMode());
  const [isSubmitting, setIsSubmitting] = useState(false);
  const [error, setError] = useState("");
  const user = getStoredUser();

  useEffect(() => {
    if (demoMode && !tripQuery.trim()) {
      setTripQuery(DEMO_PROMPT);
    }
  }, [demoMode, tripQuery]);

  async function handlePlanTrip() {
    if (!tripQuery.trim()) {
      setError("Tell us a city, duration, or budget to get started.");
      return;
    }
    if (!user?.access_token) {
      setError("Login required to generate your first trip.");
      return;
    }

    setIsSubmitting(true);
    setError("");

    try {
      const response = await apiRequest("/trips/generate-from-query", {
        method: "POST",
        body: JSON.stringify({ query: tripQuery }),
      });

      if (response.status === "clarification_needed") {
        const promptText = response.suggested_questions?.length
          ? response.suggested_questions.join(" ")
          : "I need a few more details before I can generate the trip.";
        setError(promptText);
        return;
      }

      setActiveTripId(response.trip.id);
      navigate(`/planner?tripId=${response.trip.id}`, {
        state: {
          dashboard: response,
        },
      });
    } catch (requestError) {
      setError(requestError.message);
    } finally {
      setIsSubmitting(false);
    }
  }

  return (
    <main className="mx-auto flex min-h-[calc(100vh-6rem)] max-w-6xl flex-col justify-center gap-12 px-4 pb-16 pt-12 md:px-6">
      <section className="relative overflow-hidden rounded-[2.75rem] bg-brand-gradient px-6 py-14 text-white shadow-float md:px-12 md:py-20">
        <div className="absolute inset-0 bg-[radial-gradient(circle_at_top_left,rgba(255,255,255,0.22),transparent_35%)]" />
        <div className="relative z-10 grid gap-10 lg:grid-cols-[1.2fr,0.8fr] lg:items-center">
          <div>
            <p className="label-md text-white/70">Plan your first trip</p>
            <h1 className="mt-4 text-5xl font-extrabold leading-[1.05] text-balance md:text-[3.4rem]">
              Start with a single request. We&apos;ll build the route.
            </h1>
            <p className="mt-5 max-w-2xl text-lg leading-8 text-white/80">
              Describe the trip you want and TravelMind will compose a day-by-day itinerary with places, stays, and a route-aware
              plan.
            </p>
            <div className="mt-8">
              <TripInput
                disabled={isSubmitting}
                error={error}
                onChange={setTripQuery}
                onSubmit={handlePlanTrip}
                submitLabel={isSubmitting ? "Planning..." : "Plan my trip"}
                value={tripQuery}
              />
            </div>
            <div className="mt-6 flex flex-wrap items-center gap-3 text-xs text-white/70">
              <button
                className={`rounded-full px-4 py-2 font-semibold transition ${
                  demoMode ? "bg-white/25 text-white" : "bg-white/10 text-white/70 hover:bg-white/20"
                }`}
                onClick={() => {
                  const next = !demoMode;
                  setDemoModeState(next);
                  setDemoMode(next);
                }}
                type="button"
              >
                {demoMode ? "Demo mode on" : "Enable demo mode"}
              </button>
              {demoMode ? <span>{getDemoLabel()}</span> : null}
            </div>
            {!user?.access_token ? (
              <div className="mt-6 flex flex-wrap items-center gap-3 text-sm text-white/70">
                <span>New here?</span>
                <Link className="inline-flex items-center gap-2 font-semibold text-white" to="/login">
                  Login to continue
                  <Icon className="h-4 w-4" name="arrow" />
                </Link>
              </div>
            ) : null}
          </div>
          <div className="relative overflow-hidden rounded-[2rem] bg-white/10 p-6 backdrop-blur-xl">
            <p className="label-md text-white/70">What you get</p>
            <ul className="mt-4 space-y-4 text-sm text-white/85">
              {[
                "A trip dashboard with map-first planning.",
                "Auto-sequenced itinerary stops with travel logic.",
                "Recommendations tuned to your budget and traveler type.",
              ].map((item) => (
                <li key={item} className="flex items-start gap-3">
                  <span className="mt-1 h-2 w-2 rounded-full bg-white" />
                  <span>{item}</span>
                </li>
              ))}
            </ul>
            <div className="mt-6 rounded-2xl bg-white/10 p-4 text-xs text-white/70">
              Tip: Try “Plan a 4 day Jaipur trip under 25000 with heritage and food”.
            </div>
          </div>
        </div>
      </section>
    </main>
  );
}

export default FirstTripPage;
