import { useState } from "react";
import Icon from "../../../components/Icon";

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
    <section className="section-shell travel-panel flex h-full min-h-[36rem] flex-col gap-4">
      <div className="hide-scrollbar flex-1 space-y-3 overflow-y-auto pr-1">
        {messages.length ? (
          messages.map((entry) => (
            <div key={`${entry.speaker}-${entry.id}`} className="rounded-[1.25rem] bg-surface-container-lowest px-4 py-4 text-sm dark:bg-dark-card">
              <p className="text-xs font-semibold uppercase tracking-label text-text/45 dark:text-white/45">{entry.speaker}</p>
              <p className="mt-3 text-sm leading-7 text-text/75 dark:text-white/75">{entry.text}</p>
            </div>
          ))
        ) : (
          <div className="flex h-full items-center justify-center">
            <div className="rounded-[1.5rem] bg-surface-container-lowest px-6 py-6 text-center text-lg font-semibold text-text/75 shadow-ambient dark:bg-dark-card dark:text-white/80">
              Tell what changes do you want to make.
            </div>
          </div>
        )}
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
