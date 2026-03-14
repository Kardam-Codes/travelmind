/*
Feature: Planner Dashboard
File Purpose: Render the premium map-first planner studio with live route and itinerary editing
Owner: Jay
Dependencies: PlannerHeader, PlannerSidebar, PlannerMapStage, PlannerTimeline, Fetch
Last Updated: 2026-03-14
*/
import { useEffect, useMemo, useRef, useState } from "react";
import { useLocation, useSearchParams } from "react-router-dom";
import { apiRequest, buildTripWebSocketUrl } from "../../utils/apiClient";
import { getActiveTripId, getStoredUser, setActiveTripId } from "../../utils/session";
import PlannerHeader from "./components/PlannerHeader";
import PlannerMapStage from "./components/PlannerMapStage";
import PlannerTimeline from "./components/PlannerTimeline";
import PlannerChatPanel from "./components/PlannerChatPanel";
import PlannerSummaryPanel from "./components/PlannerSummaryPanel";

function PlannerDashboard() {
  const [searchParams] = useSearchParams();
  const location = useLocation();
  const socketRef = useRef(null);
  const [dashboard, setDashboard] = useState(() => {
    const navigationDashboard = location.state?.dashboard;
    return navigationDashboard?.trip ? navigationDashboard : null;
  });
  const [error, setError] = useState("");
  const [operationError, setOperationError] = useState("");
  const [chatError, setChatError] = useState("");
  const [chatMessages, setChatMessages] = useState([]);
  const [comments, setComments] = useState([]);
  const [commentError, setCommentError] = useState("");
  const [inviteStatus, setInviteStatus] = useState("");
  const [isLoading, setIsLoading] = useState(false);
  const [mapRoute, setMapRoute] = useState(null);
  const [selectedDay, setSelectedDay] = useState(null);
  const [selectedStopId, setSelectedStopId] = useState(null);
  const [collapsedDays, setCollapsedDays] = useState({});
  const [websocketReady, setWebsocketReady] = useState(false);
  const [shareNotice, setShareNotice] = useState("");
  const tripId = searchParams.get("tripId") || getActiveTripId();
  const user = getStoredUser();
  const userId = String(user?.user_id || "guest");

  if (!user?.access_token) {
    return (
      <main className="mx-auto max-w-3xl px-4 pb-12 pt-10 md:px-6">
        <div className="section-shell">
          <h1 className="text-3xl font-bold">Login required</h1>
          <p className="mt-4 text-sm text-text/65 dark:text-white/65">
            Please login to access collaborative planning, org features, and booking workflows.
          </p>
        </div>
      </main>
    );
  }

  async function loadDashboard() {
    if (!tripId) {
      return;
    }

    setIsLoading(true);
    try {
      const response = await apiRequest(`/trips/${tripId}/dashboard`);
      setDashboard(response);
      setActiveTripId(response.trip.id);
      setError("");
    } catch (requestError) {
      setError(requestError.message);
    } finally {
      setIsLoading(false);
    }
  }

  async function loadRoute() {
    if (!tripId) {
      return;
    }

    try {
      const response = await apiRequest(`/maps/trips/${tripId}/route`);
      setMapRoute(response);
    } catch (requestError) {
      setMapRoute({
        provider_status: "unavailable",
        warning: requestError.message,
        path: [],
        stops: [],
        legs: [],
      });
    }
  }

  async function loadComments() {
    if (!tripId) {
      return;
    }
    try {
      const response = await apiRequest(`/trips/${tripId}/comments`);
      setComments(response);
      setCommentError("");
    } catch (requestError) {
      setCommentError(requestError.message);
    }
  }

  useEffect(() => {
    const navigationDashboard = location.state?.dashboard;
    if (navigationDashboard?.trip && String(navigationDashboard.trip.id) === String(tripId)) {
      setDashboard(navigationDashboard);
      setActiveTripId(navigationDashboard.trip.id);
      setError("");
    }
  }, [location.state, tripId]);

  useEffect(() => {
    loadDashboard();
  }, [tripId]);

  useEffect(() => {
    if (tripId) {
      loadRoute();
    }
  }, [tripId, dashboard?.trip?.version]);

  useEffect(() => {
    if (tripId) {
      loadComments();
    }
  }, [tripId]);

  useEffect(() => {
    const firstItem = dashboard?.itinerary?.days?.[0]?.items?.[0];
    if (firstItem && !selectedStopId) {
      setSelectedStopId(firstItem.id);
    }
  }, [dashboard, selectedStopId]);

  useEffect(() => {
    if (!tripId) {
      return undefined;
    }

    const socket = new WebSocket(buildTripWebSocketUrl(tripId, userId));
    socketRef.current = socket;

    socket.addEventListener("open", () => {
      setWebsocketReady(true);
      setChatError("");
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
      setChatError("Chat is temporarily unavailable.");
    });

    socket.addEventListener("close", () => {
      setWebsocketReady(false);
      setChatError("Live collaboration disconnected.");
    });

    return () => {
      socket.close();
      socketRef.current = null;
    };
  }, [tripId, userId]);

  function sendChatMessage(text) {
    if (!text.trim()) {
      return;
    }

    if (!socketRef.current || socketRef.current.readyState !== WebSocket.OPEN) {
      setChatError("Live collaboration is still connecting. Try again in a moment.");
      return;
    }

    socketRef.current.send(
      JSON.stringify({
        type: "CHAT_MESSAGE",
        payload: { message: text.trim() },
      }),
    );
    setChatError("");
  }

  async function handleInvite(email, role) {
    if (!tripId) {
      return;
    }
    try {
      await apiRequest("/invites", {
        method: "POST",
        body: JSON.stringify({
          scope: "trip",
          trip_id: Number(tripId),
          email,
          role,
        }),
      });
      setInviteStatus("Invite sent.");
    } catch (requestError) {
      setInviteStatus(requestError.message);
    }
  }

  async function handleAddComment(body) {
    if (!tripId) {
      return;
    }
    try {
      await apiRequest(`/trips/${tripId}/comments`, {
        method: "POST",
        body: JSON.stringify({ body }),
      });
      loadComments();
    } catch (requestError) {
      setCommentError(requestError.message);
    }
  }

  async function handleRequestBooking() {
    if (!tripId) {
      return;
    }
    const travelerName = window.prompt("Traveler name");
    if (!travelerName) {
      return;
    }
    const travelerEmail = window.prompt("Traveler email");
    if (!travelerEmail) {
      return;
    }
    try {
      await apiRequest("/bookings/requests", {
        method: "POST",
        body: JSON.stringify({
          trip_id: Number(tripId),
          traveler_name: travelerName,
          traveler_email: travelerEmail,
        }),
      });
    } catch (requestError) {
      setOperationError(requestError.message);
    }
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

  function handleSelectStop(itemId) {
    setSelectedStopId(itemId);
    const day = dashboard?.itinerary?.days?.find((entry) => entry.items.some((item) => item.id === itemId));
    if (day) {
      setSelectedDay(day.day_number);
      setCollapsedDays((current) => ({ ...current, [day.day_number]: false }));
    }
  }

  function handleToggleDay(dayNumber) {
    setCollapsedDays((current) => ({ ...current, [dayNumber]: !current[dayNumber] }));
  }

  const selectedStop =
    dashboard?.itinerary?.days
      ?.flatMap((day) => day.items)
      .find((item) => item.id === selectedStopId) || null;
  const sidebarMessages = chatMessages.slice(-12);

  function handleShare() {
    if (!tripId) {
      return;
    }
    navigator.clipboard
      .writeText(window.location.href)
      .then(() => setShareNotice("Share link copied."))
      .catch(() => setShareNotice("Unable to copy link."));
  }

  function handleStartGroup() {
    setInviteStatus("Invite collaborators to start a group plan.");
  }

  return (
    <main className="mx-auto max-w-[1600px] px-4 pb-12 pt-8 md:px-6">
      <div className="space-y-6">
        <PlannerHeader onShare={handleShare} onStartGroup={handleStartGroup} trip={dashboard?.trip} />
        {shareNotice ? <p className="text-sm text-primary">{shareNotice}</p> : null}

        <section className="grid gap-6 xl:grid-cols-[20rem,minmax(0,1fr),22rem]">
          <PlannerSummaryPanel inviteStatus={inviteStatus} onInvite={handleInvite} trip={dashboard?.trip} tripRole={dashboard?.trip_role} />
          <div className="space-y-4">
            {isLoading ? <p className="rounded-[1.25rem] bg-white/80 px-4 py-3 text-sm text-primary shadow-ambient">Loading planner...</p> : null}
            {error ? <p className="rounded-[1.25rem] bg-white/80 px-4 py-3 text-sm text-tertiary shadow-ambient">{error}</p> : null}
            <PlannerMapStage
              mapRoute={mapRoute}
              onSelectDay={setSelectedDay}
              onSelectStop={handleSelectStop}
              places={dashboard?.places || []}
              selectedDay={selectedDay}
              selectedStop={selectedStop}
              trip={dashboard?.trip}
            />
          </div>
          <PlannerChatPanel messages={sidebarMessages} onSendMessage={sendChatMessage} websocketReady={websocketReady} />
        </section>

        <section className="section-shell">
          <PlannerTimeline
            collapsedDays={collapsedDays}
            currentUserId={userId}
            itinerary={dashboard?.itinerary}
            onAddItem={handleAddItem}
            onLockDay={handleLockDay}
            onMoveItem={handleMoveItem}
            onRemoveItem={handleRemoveItem}
            onSelectStop={handleSelectStop}
            onToggleDay={handleToggleDay}
            onUnlockDay={handleUnlockDay}
            onUpdateItem={handleUpdateItem}
            operationError={operationError}
            places={dashboard?.places || []}
            activities={dashboard?.activities || []}
            hotels={dashboard?.hotels || []}
            route={mapRoute}
            selectedDay={selectedDay}
            selectedStopId={selectedStopId}
            trip={dashboard?.trip}
            tripRole={dashboard?.trip_role}
          />
        </section>
      </div>
    </main>
  );
}

export default PlannerDashboard;
