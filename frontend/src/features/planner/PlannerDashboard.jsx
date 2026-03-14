/*
Feature: Planner Dashboard
File Purpose: Render the AI-first trip planner with chat, map, and itinerary builder
Owner: Jay
Dependencies: CollaborationPanel, ItineraryView, Icon, Fetch
Last Updated: 2026-03-13
*/
import { useEffect, useRef, useState } from "react";
import { useSearchParams } from "react-router-dom";
import CollaborationPanel from "../collaboration/CollaborationPanel";
import ItineraryView from "../itinerary/ItineraryView";
import Icon from "../../components/Icon";
import { apiRequest, buildTripWebSocketUrl } from "../../utils/apiClient";
import { getActiveTripId, getStoredUser, setActiveTripId } from "../../utils/session";
import { buildMapPlaces } from "../../utils/tripPresentation";

function PlannerDashboard() {
  const [searchParams] = useSearchParams();
  const socketRef = useRef(null);
  const [dashboard, setDashboard] = useState(null);
  const [error, setError] = useState("");
  const [operationError, setOperationError] = useState("");
  const [chatMessages, setChatMessages] = useState([]);
  const [websocketReady, setWebsocketReady] = useState(false);
  const tripId = searchParams.get("tripId") || getActiveTripId();
  const user = getStoredUser();
  const userId = String(user?.user_id || "guest");

  async function loadDashboard() {
    if (!tripId) {
      return;
    }

    try {
      const response = await apiRequest(`/trips/${tripId}/dashboard`);
      setDashboard(response);
      setActiveTripId(response.trip.id);
    } catch (requestError) {
      setError(requestError.message);
    }
  }

  useEffect(() => {
    loadDashboard();
  }, [tripId]);

  useEffect(() => {
    if (!tripId) {
      return undefined;
    }

    const socket = new WebSocket(buildTripWebSocketUrl(tripId, userId));
    socketRef.current = socket;

    socket.addEventListener("open", () => {
      setWebsocketReady(true);
    });

    socket.addEventListener("message", (event) => {
      const message = JSON.parse(event.data);

      if (message.type === "CHAT_MESSAGE") {
        setChatMessages((current) => [
          ...current,
          {
            id: `${message.user_id}-${Date.now()}`,
            speaker: message.user_id === userId ? "You" : message.user_id,
            text: message.payload?.message || "",
          },
        ]);
        return;
      }

      if (message.type === "SYNC_SNAPSHOT" || message.type === "DAY_LOCK_CHANGED") {
        setDashboard((current) =>
          current
            ? {
                ...current,
                trip: {
                  ...current.trip,
                  version: message.payload.version,
                  locked_by: message.payload.locked_by,
                  locked_day_number: message.payload.locked_day_number,
                },
              }
            : current,
        );
        return;
      }

      if (message.type === "ITINERARY_APPLIED") {
        setOperationError("");
        loadDashboard();
        return;
      }

      if (message.type === "ITINERARY_REJECTED") {
        setOperationError(message.detail || "The itinerary changed. Reloading the latest version.");
        loadDashboard();
      }
    });

    socket.addEventListener("error", () => {
      setWebsocketReady(false);
      setOperationError("Live collaboration is unavailable.");
    });

    socket.addEventListener("close", () => {
      setWebsocketReady(false);
    });

    return () => {
      socket.close();
      socketRef.current = null;
    };
  }, [tripId, userId]);

  function sendChatMessage(text) {
    if (!text.trim() || !socketRef.current || socketRef.current.readyState !== WebSocket.OPEN) {
      return;
    }

    socketRef.current.send(
      JSON.stringify({
        type: "CHAT_MESSAGE",
        payload: { message: text.trim() },
      }),
    );
  }

  function sendOperation(type, payload) {
    if (!socketRef.current || socketRef.current.readyState !== WebSocket.OPEN || !dashboard?.trip) {
      setOperationError("WebSocket connection is not ready.");
      return;
    }

    socketRef.current.send(
      JSON.stringify({
        type,
        operation_id: `${type}-${Date.now()}`,
        base_version: dashboard.trip.version,
        payload,
      }),
    );
  }

  function handleAddItem(dayNumber) {
    const title = window.prompt("Title for the new itinerary item");
    if (!title) {
      return;
    }
    const description = window.prompt("Optional description") || "";
    sendOperation("ADD_ITEM", {
      day_number: dayNumber,
      item_type: "note",
      title,
      description,
    });
  }

  function handleUpdateItem(item) {
    const title = window.prompt("Edit title", item.title);
    if (title === null) {
      return;
    }
    const description = window.prompt("Edit description", item.description || "");
    if (description === null) {
      return;
    }
    sendOperation("UPDATE_ITEM", {
      item_id: item.id,
      title,
      description,
    });
  }

  function handleMoveItem(itemId, dayNumber, targetOrder) {
    sendOperation("MOVE_ITEM", {
      item_id: itemId,
      target_day_number: dayNumber,
      target_item_order: targetOrder,
    });
  }

  function handleRemoveItem(itemId) {
    sendOperation("REMOVE_ITEM", { item_id: itemId });
  }

  function handleLockDay(dayNumber) {
    sendOperation("LOCK_DAY", { day_number: dayNumber });
  }

  function handleUnlockDay(dayNumber) {
    sendOperation("UNLOCK_DAY", { day_number: dayNumber });
  }

  const mapPlaces = buildMapPlaces(dashboard?.places || []);
  const topHotel = dashboard?.hotels?.[0];

  return (
    <main className="mx-auto max-w-[1500px] px-4 pb-12 pt-8 md:px-6">
      <section className="grid gap-6 xl:grid-cols-[22rem,minmax(0,1fr),25rem]">
        <CollaborationPanel
          messages={chatMessages}
          onSendMessage={sendChatMessage}
          trip={dashboard?.trip}
          tripId={dashboard?.trip?.id}
          websocketReady={websocketReady}
        />

        <div className="section-shell relative min-h-[700px] overflow-hidden p-0">
          <div className="absolute inset-0 bg-[radial-gradient(circle_at_top_left,rgba(0,109,119,0.18),transparent_28%),radial-gradient(circle_at_bottom_right,rgba(140,37,0,0.14),transparent_26%)]" />
          <div className="absolute inset-4 rounded-[2rem] bg-[url('https://commons.wikimedia.org/wiki/Special:Redirect/file/Amber%20Fort-Jaipur-India0010.JPG')] bg-cover bg-center opacity-40 dark:opacity-25" />
          <svg className="absolute inset-0 h-full w-full" viewBox="0 0 900 700">
            <path
              d="M170 420 C 260 280, 460 260, 590 350 S 760 460, 810 220"
              fill="none"
              stroke="rgba(0,83,91,0.45)"
              strokeDasharray="10 12"
              strokeWidth="4"
            />
          </svg>

          <div className="absolute left-8 top-8 flex gap-3">
            {["map", "route", "pin"].map((control) => (
              <button
                key={control}
                className="glass-panel flex h-12 w-12 items-center justify-center rounded-full text-text shadow-ambient dark:text-white"
                type="button"
              >
                <Icon name={control} />
              </button>
            ))}
          </div>

          <div className="glass-panel absolute bottom-8 left-8 max-w-sm rounded-[1.75rem] p-5 shadow-float">
            <p className="label-md text-primary/70 dark:text-white/55">Pinned highlight</p>
            <h2 className="mt-2 text-2xl font-bold">{topHotel?.name || dashboard?.places?.[0]?.name || "Waiting for a trip"}</h2>
            <p className="mt-3 text-sm leading-7 text-text/70 dark:text-white/70">
              {topHotel
                ? `Top stay near ${topHotel.nearby_area || topHotel.city}, budget category ${topHotel.budget_category || "curated"}.`
                : "Generate a trip from the landing page to pin a recommendation here."}
            </p>
            <div className="mt-4 flex items-center gap-4 text-sm">
              <span className="rounded-full bg-secondary-container px-3 py-2 text-tertiary dark:bg-white/10 dark:text-white">
                Top choice
              </span>
              <span className="text-primary dark:text-white">{dashboard?.trip?.destination_city || "No destination selected"}</span>
            </div>
          </div>

          {mapPlaces.map((place) => (
            <div key={place.id} className="absolute" style={{ left: place.x, top: place.y }}>
              <div className="group relative">
                <button
                  className={`flex h-12 w-12 items-center justify-center rounded-full ${place.accent} text-sm font-semibold text-white shadow-float transition-transform hover:scale-105`}
                  type="button"
                >
                  {place.id}
                </button>
                <div className="glass-panel pointer-events-none absolute left-1/2 top-14 w-48 -translate-x-1/2 rounded-full px-4 py-3 text-center text-xs font-semibold opacity-0 shadow-ambient transition-opacity group-hover:opacity-100">
                  {place.name}
                </div>
              </div>
            </div>
          ))}
          {error ? <p className="absolute right-8 top-24 rounded-full bg-white/80 px-4 py-3 text-sm text-tertiary">{error}</p> : null}
        </div>

        <ItineraryView
          currentUserId={userId}
          itinerary={dashboard?.itinerary}
          operationError={operationError}
          onAddItem={handleAddItem}
          onLockDay={handleLockDay}
          onMoveItem={handleMoveItem}
          onRemoveItem={handleRemoveItem}
          onUnlockDay={handleUnlockDay}
          onUpdateItem={handleUpdateItem}
          trip={dashboard?.trip}
        />
      </section>
    </main>
  );
}

export default PlannerDashboard;
