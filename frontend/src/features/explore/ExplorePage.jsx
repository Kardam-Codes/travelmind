/*
Feature: Explore
File Purpose: Render the destination discovery interface with search and editorial cards
Owner: Jay
Dependencies: React, Icon, Fetch
Last Updated: 2026-03-13
*/
import { useEffect, useState } from "react";
import Icon from "../../components/Icon";
import { apiRequest } from "../../utils/apiClient";

function cityAccent(index) {
  return index % 2 === 0
    ? "from-primary/20 via-transparent to-tertiary/15"
    : "from-tertiary/15 via-transparent to-primary/20";
}

function ExplorePage() {
  const [cities, setCities] = useState([]);
  const [query, setQuery] = useState("");
  const [error, setError] = useState("");

  useEffect(() => {
    async function loadCities() {
      try {
        const response = await apiRequest("/cities/");
        setCities(response);
      } catch (requestError) {
        setError(requestError.message);
      }
    }

    loadCities();
  }, []);

  const filteredCities = cities.filter((city) => {
    const haystack = `${city.city} ${city.state} ${city.tourism_type || ""}`.toLowerCase();
    return haystack.includes(query.toLowerCase());
  });

  return (
    <main className="mx-auto max-w-7xl px-4 pb-20 pt-10 md:px-6">
      <section className="grid gap-10 lg:grid-cols-[1.1fr,0.9fr]">
        <div>
          <p className="label-md text-tertiary">Explore destinations</p>
          <h1 className="mt-3 max-w-3xl text-5xl font-extrabold leading-[1.05] text-balance md:text-[3.5rem]">
            Uncover your next masterpiece journey.
          </h1>
        </div>
        <div className="space-y-4">
          <div className="card-surface flex items-center gap-4 rounded-[2rem] px-5 py-4">
            <Icon className="h-5 w-5 text-primary" name="search" />
            <input
              className="w-full bg-transparent text-base placeholder:text-text/40 focus:outline-none dark:placeholder:text-white/35"
              onChange={(event) => setQuery(event.target.value)}
              placeholder="Where do you want to feel inspired?"
              type="text"
              value={query}
            />
          </div>
          <div className="flex flex-wrap gap-3 text-sm text-text/60 dark:text-white/60">
            <span className="secondary-pill px-4 py-3">{filteredCities.length} supported cities</span>
            <span className="secondary-pill px-4 py-3">Curated from PostgreSQL travel data</span>
          </div>
        </div>
      </section>

      <section className="mt-16 space-y-12">
        {error ? <p className="text-sm text-tertiary">{error}</p> : null}
        {filteredCities.map((destination, index) => (
          <article
            key={destination.id}
            className={`grid gap-8 ${index % 2 === 0 ? "lg:grid-cols-[1.1fr,0.9fr]" : "lg:grid-cols-[0.9fr,1.1fr]"}`}
          >
            <div className={`${index % 2 === 1 ? "lg:order-2" : ""} overflow-hidden rounded-[2.5rem] shadow-float`}>
              <div className={`flex h-[24rem] w-full items-end bg-gradient-to-br ${cityAccent(index)} p-8`}>
                <div className="glass-panel rounded-[1.75rem] px-5 py-4">
                  <p className="label-md text-primary/70 dark:text-white/55">{destination.state}</p>
                  <h3 className="mt-2 text-2xl font-bold">{destination.city}</h3>
                </div>
              </div>
            </div>
            <div className={`flex items-center ${index % 2 === 1 ? "lg:order-1 lg:pr-10" : "lg:pl-10"}`}>
              <div className="space-y-5">
                <p className="label-md text-primary/70 dark:text-white/55">Supported destination</p>
                <h2 className="text-4xl font-bold">{destination.city}</h2>
                <div className="inline-flex items-center gap-2 rounded-full bg-secondary-container px-4 py-2 text-sm font-semibold text-tertiary dark:bg-white/10 dark:text-white">
                  <Icon className="h-4 w-4" name="sparkles" />
                  Popularity {destination.popularity_score ?? "N/A"}
                </div>
                <p className="max-w-xl text-lg leading-8 text-text/65 dark:text-white/65">
                  {destination.notes || `${destination.city} is suited for ${destination.tourism_type || "multi-style"} travel.`}
                </p>
                <div className="flex flex-wrap gap-3 text-sm text-text/60 dark:text-white/60">
                  <span className="secondary-pill px-4 py-3">Best season: {destination.best_season || "Anytime"}</span>
                  <span className="secondary-pill px-4 py-3">{destination.tourism_type || "Curated travel"}</span>
                </div>
              </div>
            </div>
          </article>
        ))}
        {!error && !filteredCities.length ? <p className="text-sm text-text/60 dark:text-white/60">No cities matched your search.</p> : null}
      </section>
    </main>
  );
}

export default ExplorePage;
