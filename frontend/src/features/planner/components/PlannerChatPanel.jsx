import { useState } from "react";
import Icon from "../../../components/Icon";

const suggestedPrompts = ["Make day 2 lighter", "Add local food stops", "Reduce travel time"];

function PlannerChatPanel({ messages = [], onSendMessage, websocketReady }) {
  const [draft, setDraft] = useState("");
  const canSend = websocketReady && draft.trim().length > 0;

  function handleSubmit(event) {
    event.preventDefault();
    if (!canSend) {
      return;
    }
    onSendMessage?.(draft.trim());
    setDraft("");
  }

  return (
    <section className="section-shell flex h-full min-h-[36rem] flex-col gap-4">
      <div className="flex items-center justify-between">
        <div>
          <p className="label-md text-tertiary">Planning chat</p>
          <h3 className="mt-2 text-xl font-semibold">Refine the plan</h3>
        </div>
        <span className="rounded-full bg-surface-container-lowest px-3 py-2 text-xs font-semibold text-text/60 dark:bg-dark-card dark:text-white/70">
          {websocketReady ? "Live" : "Offline"}
        </span>
      </div>

      <div className="hide-scrollbar flex-1 space-y-3 overflow-y-auto pr-1">
        {messages.length ? (
          messages.map((entry) => (
            <div key={`${entry.speaker}-${entry.id}`} className="rounded-[1.25rem] bg-surface-container-lowest px-4 py-4 text-sm dark:bg-dark-card">
              <div className="flex items-center gap-2 text-xs font-semibold uppercase tracking-label text-text/45 dark:text-white/45">
                <Icon className="h-4 w-4" name={entry.speaker === "You" ? "chat" : "sparkles"} />
                <span>{entry.speaker}</span>
              </div>
              <p className="mt-3 text-sm leading-7 text-text/75 dark:text-white/75">{entry.text}</p>
            </div>
          ))
        ) : (
          <div className="rounded-[1.25rem] bg-surface-container-lowest px-4 py-4 text-sm leading-7 text-text/70 dark:bg-dark-card dark:text-white/70">
            Ask for refinements and the itinerary will update.
          </div>
        )}
      </div>

      <div className="flex flex-wrap gap-2">
        {suggestedPrompts.map((prompt) => (
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

      <form className="flex items-center gap-2 rounded-full bg-surface-container-lowest px-4 py-3 dark:bg-dark-card" onSubmit={handleSubmit}>
        <input
          className="flex-1 bg-transparent text-sm text-text placeholder:text-text/35 focus:outline-none dark:text-white dark:placeholder:text-white/35"
          onChange={(event) => setDraft(event.target.value)}
          placeholder="Refine the itinerary..."
          type="text"
          value={draft}
        />
        <button
          aria-label="Send message"
          className="flex h-10 w-10 items-center justify-center rounded-full bg-tertiary text-white disabled:cursor-not-allowed disabled:opacity-60"
          disabled={!canSend}
          type="submit"
        >
          <Icon className="h-4 w-4" name="send" />
        </button>
      </form>
    </section>
  );
}

export default PlannerChatPanel;
