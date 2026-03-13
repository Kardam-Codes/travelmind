/*
Feature: Trip Input
File Purpose: UI component to capture user travel request
Owner: Jay
Dependencies: React
Last Updated: 2026-03-13
*/
import Icon from "../../components/Icon";

function TripInput({ compact = false, placeholder = "Plan a 4 day trip to Jaipur with forts and street food" }) {
  return (
    <div className={`relative ${compact ? "max-w-2xl" : "max-w-3xl"}`}>
      <div className="absolute inset-0 rounded-[3rem] bg-primary/10 blur-2xl dark:bg-primary-container/20" />
      <div className="card-surface soft-focus relative flex items-center gap-4 rounded-[3rem] px-5 py-4 md:px-7">
        <div className="flex h-12 w-12 items-center justify-center rounded-full bg-secondary-container text-primary dark:bg-white/10 dark:text-white">
          <Icon name="sparkles" />
        </div>
        <div className="flex-1">
          <p className="label-md mb-1 text-primary/70 dark:text-white/60">AI travel request</p>
          <input
            className="w-full bg-transparent text-base text-text placeholder:text-text/40 focus:outline-none dark:text-white dark:placeholder:text-white/35 md:text-lg"
            placeholder={placeholder}
            type="text"
          />
        </div>
        <button className="primary-pill flex h-14 items-center gap-2 px-6" type="button">
          <span className="hidden md:inline">Plan</span>
          <Icon className="h-4 w-4" name="arrow" />
        </button>
      </div>
    </div>
  );
}

export default TripInput;
