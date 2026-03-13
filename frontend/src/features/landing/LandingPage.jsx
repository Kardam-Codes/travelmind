/*
Feature: Landing Page
File Purpose: Introduce TravelMind with an editorial digital concierge experience
Owner: Jay
Dependencies: TripInput, mockData, Icon
Last Updated: 2026-03-13
*/
import { features, inspirationCards } from "../../data/mockData";
import Icon from "../../components/Icon";
import TripInput from "../trip-input/TripInput";
import { Link } from "react-router-dom";

function imageShape(size) {
  if (size === "large") {
    return "md:col-span-7 md:row-span-2 aspect-[4/5] md:aspect-auto";
  }
  if (size === "tall") {
    return "md:col-span-5 aspect-[4/5]";
  }
  return "md:col-span-5 aspect-square";
}

function LandingPage() {
  return (
    <main className="mx-auto flex max-w-7xl flex-col gap-24 px-4 pb-20 pt-12 md:px-6 md:pt-16">
      <section className="relative overflow-hidden rounded-[2.5rem] bg-brand-gradient px-6 py-16 text-white shadow-float md:px-12 md:py-24">
        <div className="absolute inset-0 bg-[radial-gradient(circle_at_top_right,rgba(255,255,255,0.16),transparent_28%)]" />
        <div className="relative z-10 max-w-4xl">
          <p className="label-md text-white/70">Luxury travel, intelligently composed</p>
          <h1 className="mt-4 max-w-3xl text-5xl font-extrabold leading-[1.05] text-balance md:text-[3.5rem]">
            Your Next Journey, Perfectly Planned
          </h1>
          <p className="mt-6 max-w-2xl text-lg leading-8 text-white/80">
            TravelMind combines editorial calm with AI-assisted planning so every destination feels considered, mapped, and personal.
          </p>
          <div className="mt-10">
            <TripInput />
          </div>
        </div>
      </section>

      <section className="grid gap-8 md:grid-cols-12">
        <div className="md:col-span-4">
          <p className="label-md text-tertiary">Inspiration gallery</p>
          <h2 className="mt-3 max-w-sm text-4xl font-bold leading-tight text-balance">
            The calm confidence of a digital concierge.
          </h2>
        </div>
        <div className="grid gap-8 md:col-span-8 md:grid-cols-12">
          {inspirationCards.map((card) => (
            <article
              key={card.title}
              className={`${imageShape(card.size)} group relative overflow-hidden rounded-[2rem] shadow-ambient`}
            >
              <img alt={card.title} className="h-full w-full object-cover transition-transform duration-700 group-hover:scale-105" src={card.image} />
              <div className="absolute inset-0 bg-gradient-to-t from-black/60 via-black/10 to-transparent" />
              <div className="absolute bottom-0 left-0 right-0 p-6 text-white md:p-8">
                <p className="label-md text-white/70">{card.eyebrow}</p>
                <h3 className="mt-3 text-2xl font-bold">{card.title}</h3>
                <p className="mt-3 max-w-md text-sm leading-7 text-white/80">{card.summary}</p>
              </div>
            </article>
          ))}
        </div>
      </section>

      <section className="grid gap-8 lg:grid-cols-[0.85fr,1.15fr]">
        <div className="space-y-4">
          <p className="label-md text-primary/70 dark:text-white/55">Core experience</p>
          <h2 className="text-4xl font-bold text-balance">Three features, kept editorial instead of mechanical.</h2>
        </div>
        <div className="grid gap-6 md:grid-cols-3">
          {features.map((feature, index) => (
            <article
              key={feature.title}
              className={`card-surface ${index === 1 ? "md:translate-y-8" : ""}`}
            >
              <div className="flex h-14 w-14 items-center justify-center rounded-full bg-secondary-container text-primary dark:bg-white/10 dark:text-white">
                <Icon name={feature.icon} />
              </div>
              <h3 className="mt-6 text-2xl font-bold">{feature.title}</h3>
              <p className="mt-4 leading-7 text-text/65 dark:text-white/65">{feature.description}</p>
            </article>
          ))}
        </div>
      </section>

      <section className="grid gap-10 lg:grid-cols-[0.9fr,1.1fr]">
        <div className="card-surface">
          <p className="label-md text-tertiary">Sample itinerary</p>
          <h2 className="mt-3 text-4xl font-bold">A Jaipur preview, not a dashboard.</h2>
          <div className="mt-8 space-y-6">
            {[
              "Arrival at a heritage haveli with an evening stroll through Johari Bazaar.",
              "A palace-and-fort circuit paced for quiet mornings and rooftop dining.",
              "A Nahargarh sunrise before the city fully wakes up.",
            ].map((step, index) => (
              <div key={step} className="flex gap-4">
                <div className="flex h-10 w-10 items-center justify-center rounded-full bg-primary text-sm font-semibold text-white">
                  0{index + 1}
                </div>
                <p className="pt-1 leading-7 text-text/70 dark:text-white/70">{step}</p>
              </div>
            ))}
          </div>
        </div>
        <div className="section-shell overflow-hidden">
          <div className="relative min-h-[24rem] rounded-[2rem] bg-[url('https://commons.wikimedia.org/wiki/Special:Redirect/file/Nahargarh%20Fort%20Jaipur,%20Rajasthan.jpg')] bg-cover bg-center">
            <div className="absolute inset-0 bg-gradient-to-t from-black/55 via-black/5 to-transparent" />
            <div className="glass-panel absolute right-6 top-6 rounded-full px-4 py-3 text-sm font-medium text-text dark:text-white">
              Live planner
            </div>
            <div className="absolute bottom-6 left-6 right-6 rounded-[1.75rem] bg-white/14 p-6 text-white backdrop-blur-xl">
              <p className="label-md text-white/70">Route logic</p>
              <h3 className="mt-2 text-2xl font-bold">Stops are sequenced around distance and mood.</h3>
              <p className="mt-3 max-w-xl leading-7 text-white/80">
                TravelMind keeps transit visible without turning the experience into spreadsheet planning.
              </p>
            </div>
          </div>
        </div>
      </section>

      <section className="card-surface flex flex-col items-start gap-6 rounded-[2.5rem] px-8 py-10 md:flex-row md:items-center md:justify-between">
        <div>
          <p className="label-md text-primary/70 dark:text-white/55">Start planning</p>
          <h2 className="mt-3 text-4xl font-bold">Ready to see the world differently?</h2>
        </div>
        <Link className="primary-pill inline-flex items-center gap-2" to="/planner">
          Start your journey
          <Icon className="h-4 w-4" name="arrow" />
        </Link>
      </section>
    </main>
  );
}

export default LandingPage;
