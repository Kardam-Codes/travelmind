import { useMemo, useState } from "react";
import Icon from "../../../components/Icon";

const defaultPrompts = [
  "Reduce travel time across all days",
  "Make day 2 lighter and more relaxed",
  "Add more local food stops",
  "Prioritize heritage landmarks",
];

function PlannerSidebar({ chatError, messages, onSendMessage, route, trip, websocketReady }) {
  const [draft, setDraft] = useState("");
  const canSend = websocketReady && draft.trim().length > 0;
  const routeInsight = useMemo(() => {
    const stopCount = route?.stops?.length || 0;
    const legCount = route?.legs?.length || 0;
    const durationPreview = route?.legs?.slice(0, 2).map((leg) => leg.duration_text).filter(Boolean).join(" • ");
    return {
      stopCount,
      legCount,
      durationPreview: durationPreview || "Travel times appear here when the route is available.",
    };
  }, [route]);

  function handleSubmit(event) {
    event.preventDefault();
    if (!canSend) {
      return;
    }
    onSendMessage?.(draft.trim());
    setDraft("");
  }

  return (
    <aside className="flex min-h-[40rem] flex-col gap-5">
      <section className="section-shell space-y-4">
        <div className="flex items-center justify-between gap-3">
          <div>
            <p className="label-md text-tertiary">AI refinements</p>
            <h2 className="mt-2 text-2xl font-bold">{trip ? `${trip.destination_city} planning desk` : "Planning desk"}</h2>
          </div>
          <span className="rounded-full bg-surface-container-lowest px-3 py-2 text-xs font-semibold text-text/65 dark:bg-dark-card dark:text-white/70">
            {websocketReady ? "Live" : "Connecting"}
          </span>
        </div>
        <p className="text-sm leading-7 text-text/65 dark:text-white/65">
          Refine pacing, route shape, and stop mix with action-style prompts instead of a generic chat workflow.
        </p>
        <form className="space-y-3" onSubmit={handleSubmit}>
          <textarea
            className="soft-focus min-h-[7.5rem] w-full rounded-[1.5rem] bg-surface-container-lowest px-4 py-4 text-sm leading-7 text-text placeholder:text-text/35 dark:bg-dark-card dark:text-white dark:placeholder:text-white/35"
            onChange={(event) => setDraft(event.target.value)}
            placeholder="Tell the planner what to change. Example: Make day 3 shorter and add one premium dinner stop."
            value={draft}
          />
          <div className="flex items-center justify-between gap-3">
            <div className="flex flex-wrap gap-2">
              {defaultPrompts.map((prompt) => (
                <button
                  key={prompt}
                  className="rounded-full bg-secondary-container px-3 py-2 text-xs font-semibold text-[#6d6356] dark:bg-white/10 dark:text-white"
                  onClick={() => onSendMessage?.(prompt)}
                  type="button"
                >
                  {prompt}
                </button>
              ))}
            </div>
            <button className="primary-pill inline-flex items-center gap-2" disabled={!canSend} type="submit">
              <Icon className="h-4 w-4" name="send" />
              Send
            </button>
          </div>
        </form>
      </section>

      <section className="section-shell space-y-4">
        <div className="flex items-center justify-between">
          <div>
            <p className="label-md text-tertiary">Trip insights</p>
            <h3 className="mt-2 text-xl font-semibold">Route posture</h3>
          </div>
          <Icon className="h-5 w-5 text-primary" name="route" />
        </div>
        <div className="grid gap-3 sm:grid-cols-3 lg:grid-cols-1">
          <div className="rounded-[1.5rem] bg-surface-container-lowest px-4 py-4 dark:bg-dark-card">
            <p className="label-md text-text/45 dark:text-white/45">Mapped stops</p>
            <p className="mt-2 text-2xl font-bold">{routeInsight.stopCount}</p>
          </div>
          <div className="rounded-[1.5rem] bg-surface-container-lowest px-4 py-4 dark:bg-dark-card">
            <p className="label-md text-text/45 dark:text-white/45">Legs</p>
            <p className="mt-2 text-2xl font-bold">{routeInsight.legCount}</p>
          </div>
          <div className="rounded-[1.5rem] bg-surface-container-lowest px-4 py-4 dark:bg-dark-card">
            <p className="label-md text-text/45 dark:text-white/45">Preview</p>
            <p className="mt-2 text-sm leading-6 text-text/70 dark:text-white/70">{routeInsight.durationPreview}</p>
          </div>
        </div>
      </section>

      <section className="section-shell flex min-h-[18rem] flex-1 flex-col gap-4">
        <div className="flex items-center justify-between">
          <div>
            <p className="label-md text-tertiary">Collaboration</p>
            <h3 className="mt-2 text-xl font-semibold">Live planning feed</h3>
          </div>
          <Icon className="h-5 w-5 text-primary" name="users" />
        </div>
        <p className="text-xs text-text/55 dark:text-white/55">
          {websocketReady ? "Changes and messages are live." : "Live connection is still initializing."}
        </p>
        <div className="hide-scrollbar flex-1 space-y-3 overflow-y-auto pr-1">
          {messages.length ? (
            messages.map((entry) => (
              <div key={`${entry.speaker}-${entry.id}`} className="rounded-[1.4rem] bg-surface-container-lowest px-4 py-4 dark:bg-dark-card">
                <div className="flex items-center gap-2 text-xs font-semibold uppercase tracking-label text-text/45 dark:text-white/45">
                  <Icon className="h-4 w-4" name={entry.speaker === "You" ? "chat" : "sparkles"} />
                  <span>{entry.speaker}</span>
                </div>
                <p className="mt-3 text-sm leading-7 text-text/75 dark:text-white/75">{entry.text}</p>
              </div>
            ))
          ) : (
            <div className="rounded-[1.4rem] bg-surface-container-lowest px-4 py-4 text-sm leading-7 text-text/70 dark:bg-dark-card dark:text-white/70">
              Start the collaboration thread with a refinement request or planning note.
            </div>
          )}
        </div>
        {chatError ? <p className="text-sm text-tertiary">{chatError}</p> : null}
      </section>
    </aside>
  );
}

export default PlannerSidebar;
