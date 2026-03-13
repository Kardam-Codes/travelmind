/*
Feature: Explore
File Purpose: Render the destination discovery interface with search and editorial cards
Owner: Jay
Dependencies: React, mockData, Icon
Last Updated: 2026-03-13
*/
import { exploreDestinations } from "../../data/mockData";
import Icon from "../../components/Icon";

function ExplorePage() {
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
              placeholder="Where do you want to feel inspired?"
              type="text"
            />
          </div>
          <div className="flex flex-wrap gap-3">
            {["City", "Category", "Rating", "Budget"].map((filter) => (
              <button key={filter} className="secondary-pill px-4 py-3 text-sm" type="button">
                {filter}
              </button>
            ))}
          </div>
        </div>
      </section>

      <section className="mt-16 space-y-12">
        {exploreDestinations.map((destination, index) => (
          <article
            key={destination.name}
            className={`grid gap-8 ${index % 2 === 0 ? "lg:grid-cols-[1.1fr,0.9fr]" : "lg:grid-cols-[0.9fr,1.1fr]"}`}
          >
            <div className={`${index % 2 === 1 ? "lg:order-2" : ""} overflow-hidden rounded-[2.5rem] shadow-float`}>
              <img alt={destination.name} className="h-[24rem] w-full object-cover" src={destination.image} />
            </div>
            <div className={`flex items-center ${index % 2 === 1 ? "lg:order-1 lg:pr-10" : "lg:pl-10"}`}>
              <div className="space-y-5">
                <p className="label-md text-primary/70 dark:text-white/55">AI generated summary</p>
                <h2 className="text-4xl font-bold">{destination.name}</h2>
                <div className="inline-flex items-center gap-2 rounded-full bg-secondary-container px-4 py-2 text-sm font-semibold text-tertiary dark:bg-white/10 dark:text-white">
                  <Icon className="h-4 w-4" name="sparkles" />
                  {destination.rating} rating
                </div>
                <p className="max-w-xl text-lg leading-8 text-text/65 dark:text-white/65">{destination.summary}</p>
              </div>
            </div>
          </article>
        ))}
      </section>
    </main>
  );
}

export default ExplorePage;
