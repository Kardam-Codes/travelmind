/*
Feature: Trip Input
File Purpose: UI component to capture user travel request
Owner: Jay
Dependencies: React
Last Updated: 2026-03-13
*/
import Icon from "../../components/Icon";

function TripInput({
  compact = false,
  disabled = false,
  error = "",
  onSubmit,
  placeholder = "Plan a 4 day trip to Jaipur with forts and street food",
  submitLabel = "Plan",
  value = "",
  onChange,
}) {
  function handleSubmit(event) {
    event.preventDefault();
    onSubmit?.();
  }

  return (
    <form className={`relative ${compact ? "max-w-2xl" : "max-w-3xl"}`} onSubmit={handleSubmit}>
      <div className="absolute inset-0 rounded-[3rem] bg-primary/10 blur-2xl dark:bg-primary-container/20" />
      <div className="card-surface soft-focus relative flex items-center gap-4 rounded-[3rem] px-5 py-4 md:px-7">
        <div className="flex h-12 w-12 items-center justify-center rounded-full bg-secondary-container text-primary dark:bg-white/10 dark:text-white">
          <Icon name="sparkles" />
        </div>
        <div className="flex-1">
          <p className="label-md mb-1 text-primary/70 dark:text-white/60">AI travel request</p>
          <textarea
            className="min-h-[4.5rem] w-full resize-none bg-transparent text-base text-text placeholder:text-text/40 focus:outline-none dark:text-white dark:placeholder:text-white/35 md:text-lg"
            disabled={disabled}
            onChange={(event) => onChange?.(event.target.value)}
            placeholder={placeholder}
            rows={2}
            value={value}
          />
        </div>
        <button
          aria-label={submitLabel}
          className="flex h-14 w-14 items-center justify-center rounded-full bg-tertiary text-white transition-transform duration-300 hover:-translate-y-0.5 disabled:cursor-not-allowed disabled:opacity-70"
          disabled={disabled}
          type="submit"
        >
          <Icon className="h-5 w-5" name="arrow" />
        </button>
      </div>
      {error ? <p className="mt-3 px-4 text-sm text-tertiary">{error}</p> : null}
    </form>
  );
}

export default TripInput;
