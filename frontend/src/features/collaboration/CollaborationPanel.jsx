/*
Feature: Collaboration
File Purpose: Real-time trip collaboration UI
Owner: Jay
Dependencies: WebSockets
Last Updated: 2026-03-13
*/
import { plannerChat, suggestedPrompts } from "../../data/mockData";
import Icon from "../../components/Icon";

function CollaborationPanel() {
  return (
    <aside className="section-shell flex h-full min-h-[700px] flex-col gap-8 lg:w-[22rem]">
      <div className="space-y-3">
        <p className="label-md text-tertiary">Digital concierge</p>
        <h1 className="text-3xl font-bold text-balance">Jaipur Curations</h1>
        <p className="max-w-sm text-sm leading-7 text-text/65 dark:text-white/65">
          The AI layer stays focused on curation, route logic, and collaborative planning prompts.
        </p>
      </div>

      <div className="space-y-5">
        {plannerChat.map((entry) => (
          <div key={`${entry.speaker}-${entry.text}`} className="space-y-2">
            <div className="flex items-center gap-2">
              <div
                className={`flex h-8 w-8 items-center justify-center rounded-full ${
                  entry.speaker === "TravelMind AI"
                    ? "bg-primary text-white"
                    : "bg-secondary-container text-tertiary dark:bg-white/10 dark:text-white"
                }`}
              >
                <Icon className="h-4 w-4" name={entry.speaker === "TravelMind AI" ? "sparkles" : "chat"} />
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
      </div>

      <div className="space-y-3">
        <p className="label-md text-text/50 dark:text-white/50">Suggested prompts</p>
        <div className="space-y-3">
          {suggestedPrompts.map((prompt) => (
            <button
              key={prompt}
              className="flex w-full items-center justify-between rounded-full bg-surface-container-lowest/80 px-5 py-4 text-left text-sm text-text/75 transition-transform hover:-translate-y-0.5 dark:bg-dark-card/80 dark:text-white/75"
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
          placeholder="Ask your concierge..."
          type="text"
        />
        <button className="flex h-10 w-10 items-center justify-center rounded-full bg-primary text-white" type="button">
          <Icon className="h-4 w-4" name="send" />
        </button>
      </div>
    </aside>
  );
}

export default CollaborationPanel;
