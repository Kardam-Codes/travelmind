/*
Feature: Collaboration
File Purpose: Real-time trip collaboration UI
Owner: Jay
Dependencies: WebSockets
Last Updated: 2026-03-13
*/
import { useEffect, useState } from "react";
import Icon from "../../components/Icon";
import { apiRequest } from "../../utils/apiClient";

const suggestedPrompts = [
  "Suggest a quieter first evening",
  "Prioritize places with short travel times",
  "Add a market stop before dinner",
];

function CollaborationPanel({ messages, onSendMessage, trip, tripId, websocketReady }) {
  const [draft, setDraft] = useState("");
  const [history, setHistory] = useState([]);
  const [error, setError] = useState("");

  useEffect(() => {
    if (!tripId) {
      setHistory([]);
      return;
    }

    async function loadHistory() {
      try {
        const response = await apiRequest(`/collaboration/${tripId}/events`);
        setHistory(
          response
            .filter((event) => event.event_type === "CHAT_MESSAGE")
            .map((event) => {
              const payload = event.payload ? JSON.parse(event.payload) : {};
              return {
                id: event.id,
                speaker: event.user_id,
                text: payload.message || "",
              };
            }),
        );
      } catch (requestError) {
        setError(requestError.message);
      }
    }

    loadHistory();
  }, [tripId]);

  const mergedMessages = [...history, ...messages];

  return (
    <aside className="section-shell flex h-full min-h-[700px] flex-col gap-8 lg:w-[22rem]">
      <div className="space-y-3">
        <p className="label-md text-tertiary">Digital concierge</p>
        <h1 className="text-3xl font-bold text-balance">{trip ? `${trip.destination_city} Curations` : "Trip collaboration"}</h1>
        <p className="max-w-sm text-sm leading-7 text-text/65 dark:text-white/65">
          The AI layer stays focused on curation, route logic, and collaborative planning prompts.
        </p>
      </div>

      <div className="space-y-5">
        {mergedMessages.map((entry) => (
          <div key={`${entry.speaker}-${entry.id}`} className="space-y-2">
            <div className="flex items-center gap-2">
              <div
                className={`flex h-8 w-8 items-center justify-center rounded-full ${
                  entry.speaker === "You"
                    ? "bg-secondary-container text-tertiary dark:bg-white/10 dark:text-white"
                    : "bg-primary text-white"
                }`}
              >
                <Icon className="h-4 w-4" name={entry.speaker === "You" ? "chat" : "sparkles"} />
              </div>
              <span className="text-xs font-semibold uppercase tracking-label text-text/55 dark:text-white/55">
                {entry.speaker}
              </span>
            </div>
            <div className="rounded-[1.75rem] bg-surface-container-lowest/85 p-5 leading-7 text-text/80 shadow-ambient dark:bg-dark-card/80 dark:text-white/80">
              {entry.text}
            </div>
          </div>
        ))}
        {!mergedMessages.length ? (
          <div className="rounded-[1.75rem] bg-surface-container-lowest/85 p-5 text-sm leading-7 text-text/70 shadow-ambient dark:bg-dark-card/80 dark:text-white/70">
            Start the collaboration feed with a prompt or send a message below.
          </div>
        ) : null}
        {error ? <p className="text-sm text-tertiary">{error}</p> : null}
      </div>

      <div className="space-y-3">
        <p className="label-md text-text/50 dark:text-white/50">Suggested prompts</p>
        <div className="space-y-3">
          {suggestedPrompts.map((prompt) => (
            <button
              key={prompt}
              className="flex w-full items-center justify-between rounded-full bg-surface-container-lowest/80 px-5 py-4 text-left text-sm text-text/75 transition-transform hover:-translate-y-0.5 dark:bg-dark-card/80 dark:text-white/75"
              onClick={() => onSendMessage?.(prompt)}
              type="button"
            >
              <span>{prompt}</span>
              <Icon className="h-4 w-4" name="arrow" />
            </button>
          ))}
        </div>
      </div>

      <div className="mt-auto flex items-center gap-3 rounded-full bg-surface-container-lowest/85 px-5 py-4 shadow-ambient dark:bg-dark-card/85">
        <input
          className="flex-1 bg-transparent text-sm text-text placeholder:text-text/35 focus:outline-none dark:text-white dark:placeholder:text-white/35"
          onChange={(event) => setDraft(event.target.value)}
          placeholder="Ask your concierge..."
          type="text"
          value={draft}
        />
        <button
          className="flex h-10 w-10 items-center justify-center rounded-full bg-primary text-white"
          disabled={!websocketReady}
          onClick={() => {
            onSendMessage?.(draft);
            setDraft("");
          }}
          type="button"
        >
          <Icon className="h-4 w-4" name="send" />
        </button>
      </div>
    </aside>
  );
}

export default CollaborationPanel;
