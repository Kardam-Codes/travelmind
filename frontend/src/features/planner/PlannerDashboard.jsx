/*
Feature: Planner Dashboard
File Purpose: Render the premium map-first planner studio with live route and itinerary editing
Owner: Jay
Dependencies: PlannerMapStage, PlannerTimeline, Fetch
Last Updated: 2026-03-14
*/
import { useEffect, useRef, useState } from "react";
import { useLocation, useSearchParams } from "react-router-dom";
import { apiRequest, buildTripWebSocketUrl } from "../../utils/apiClient";
import { getActiveTripId, getStoredUser, setActiveTripId } from "../../utils/session";
import PlannerMapStage from "./components/PlannerMapStage";
import PlannerTimeline from "./components/PlannerTimeline";
import PlannerChatPanel from "./components/PlannerChatPanel";
import Icon from "../../components/Icon";

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
  const [chatMessages, setChatMessages] = useState([]);
  const [inviteStatus, setInviteStatus] = useState("");
  const [isLoading, setIsLoading] = useState(false);
  const [mapRoute, setMapRoute] = useState(null);
  const [selectedDay, setSelectedDay] = useState(null);
  const [selectedStopId, setSelectedStopId] = useState(null);
  const [collapsedDays, setCollapsedDays] = useState({});
  const [websocketReady, setWebsocketReady] = useState(false);
  const [shareNotice, setShareNotice] = useState("");
  const [sidebarOpen, setSidebarOpen] = useState(false);
  const [activeModal, setActiveModal] = useState(null);
  const [modalForm, setModalForm] = useState({ title: "", description: "", email: "", role: "viewer", link: "" });
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
    if (!text.trim()) {
      return;
    }

    if (!socketRef.current || socketRef.current.readyState !== WebSocket.OPEN) {
      return;
    }

    socketRef.current.send(
      JSON.stringify({
        type: "CHAT_MESSAGE",
        payload: { message: text.trim() },
      }),
    );
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

  async function handleRequestBooking() {
    if (!tripId) {
      return;
    }
    setActiveModal({ type: "booking" });
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
    setModalForm({ title: "", description: "", email: "", role: "viewer", link: "" });
    setActiveModal({ type: "add-item", dayNumber });
  }

  function handleUpdateItem(item) {
    setModalForm({ title: item.title || "", description: item.description || "", email: "", role: "viewer", link: "" });
    setActiveModal({ type: "edit-item", item });
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
    const shareLink = window.location.href;
    setModalForm((current) => ({ ...current, link: shareLink }));
    setActiveModal({ type: "share" });
  }

  function handleStartGroup() {
    setActiveModal({ type: "invite" });
  }

  return (
    <main className="mx-auto max-w-[1600px] px-4 pb-12 pt-8 md:px-6">
      <div className="space-y-6">
        <div className="flex items-center justify-between">
          <div>
            <p className="label-md text-tertiary">Planner</p>
            <h1 className="mt-2 text-3xl font-bold">{dashboard?.trip ? `${dashboard.trip.destination_city} plan` : "Planner"}</h1>
          </div>
        </div>
        {shareNotice ? <p className="text-sm text-primary">{shareNotice}</p> : null}

        <section className="grid gap-6 xl:grid-cols-[auto,minmax(0,1fr),22rem]">
          <aside className={`section-shell flex flex-col items-center gap-4 transition-all duration-300 ${sidebarOpen ? "w-48" : "w-14"}`}>
            <button
              aria-label="Toggle sidebar"
              className="flex h-10 w-10 items-center justify-center rounded-full bg-secondary-container text-[#6d6356] dark:bg-white/10 dark:text-white"
              onClick={() => setSidebarOpen((current) => !current)}
              type="button"
            >
              {sidebarOpen ? "<" : ">"}
            </button>
            <button className="flex h-11 w-11 items-center justify-center rounded-full bg-tertiary text-white" onClick={handleStartGroup} type="button">
              <Icon className="h-4 w-4" name="users" />
            </button>
            {sidebarOpen ? <span className="text-xs font-semibold">Start Group Chat</span> : null}
            <button
              className="flex h-11 w-11 items-center justify-center rounded-full bg-secondary-container text-[#6d6356] dark:bg-white/10 dark:text-white"
              onClick={handleShare}
              type="button"
            >
              <Icon className="h-4 w-4" name="arrow" />
            </button>
            {sidebarOpen ? <span className="text-xs font-semibold">Share</span> : null}
          </aside>

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
      {activeModal?.type ? (
        <div className="fixed inset-0 z-50 flex items-center justify-center bg-black/40 px-4">
          <div className="w-full max-w-lg rounded-[2rem] bg-surface-container-lowest p-6 shadow-float dark:bg-dark-card">
            {activeModal.type === "add-item" ? (
              <>
                <h2 className="text-xl font-semibold">Add stop</h2>
                <div className="mt-4 space-y-3">
                  <input
                    className="soft-focus w-full rounded-[1.2rem] bg-surface-container-low px-4 py-3 text-sm dark:bg-dark-low"
                    placeholder="Title"
                    value={modalForm.title}
                    onChange={(event) => setModalForm((current) => ({ ...current, title: event.target.value }))}
                  />
                  <textarea
                    className="soft-focus w-full rounded-[1.2rem] bg-surface-container-low px-4 py-3 text-sm dark:bg-dark-low"
                    placeholder="Description"
                    value={modalForm.description}
                    onChange={(event) => setModalForm((current) => ({ ...current, description: event.target.value }))}
                  />
                </div>
                <div className="mt-5 flex justify-end gap-2">
                  <button className="secondary-pill" onClick={() => setActiveModal(null)} type="button">
                    Cancel
                  </button>
                  <button
                    className="primary-pill"
                    onClick={() => {
                      if (!modalForm.title.trim()) {
                        return;
                      }
                      sendOperation("ADD_ITEM", {
                        day_number: activeModal.dayNumber,
                        item_type: "note",
                        title: modalForm.title.trim(),
                        description: modalForm.description.trim(),
                      });
                      setActiveModal(null);
                    }}
                    type="button"
                  >
                    Add
                  </button>
                </div>
              </>
            ) : null}
            {activeModal.type === "edit-item" ? (
              <>
                <h2 className="text-xl font-semibold">Edit stop</h2>
                <div className="mt-4 space-y-3">
                  <input
                    className="soft-focus w-full rounded-[1.2rem] bg-surface-container-low px-4 py-3 text-sm dark:bg-dark-low"
                    placeholder="Title"
                    value={modalForm.title}
                    onChange={(event) => setModalForm((current) => ({ ...current, title: event.target.value }))}
                  />
                  <textarea
                    className="soft-focus w-full rounded-[1.2rem] bg-surface-container-low px-4 py-3 text-sm dark:bg-dark-low"
                    placeholder="Description"
                    value={modalForm.description}
                    onChange={(event) => setModalForm((current) => ({ ...current, description: event.target.value }))}
                  />
                </div>
                <div className="mt-5 flex justify-end gap-2">
                  <button className="secondary-pill" onClick={() => setActiveModal(null)} type="button">
                    Cancel
                  </button>
                  <button
                    className="primary-pill"
                    onClick={() => {
                      sendOperation("UPDATE_ITEM", {
                        item_id: activeModal.item?.id,
                        title: modalForm.title.trim(),
                        description: modalForm.description.trim(),
                      });
                      setActiveModal(null);
                    }}
                    type="button"
                  >
                    Save
                  </button>
                </div>
              </>
            ) : null}
            {activeModal.type === "booking" ? (
              <>
                <h2 className="text-xl font-semibold">Request booking</h2>
                <div className="mt-4 space-y-3">
                  <input
                    className="soft-focus w-full rounded-[1.2rem] bg-surface-container-low px-4 py-3 text-sm dark:bg-dark-low"
                    placeholder="Traveler name"
                    value={modalForm.title}
                    onChange={(event) => setModalForm((current) => ({ ...current, title: event.target.value }))}
                  />
                  <input
                    className="soft-focus w-full rounded-[1.2rem] bg-surface-container-low px-4 py-3 text-sm dark:bg-dark-low"
                    placeholder="Traveler email"
                    value={modalForm.email}
                    onChange={(event) => setModalForm((current) => ({ ...current, email: event.target.value }))}
                  />
                </div>
                <div className="mt-5 flex justify-end gap-2">
                  <button className="secondary-pill" onClick={() => setActiveModal(null)} type="button">
                    Cancel
                  </button>
                  <button
                    className="primary-pill"
                    onClick={async () => {
                      if (!modalForm.title.trim() || !modalForm.email.trim()) {
                        return;
                      }
                      try {
                        await apiRequest("/bookings/requests", {
                          method: "POST",
                          body: JSON.stringify({
                            trip_id: Number(tripId),
                            traveler_name: modalForm.title.trim(),
                            traveler_email: modalForm.email.trim(),
                          }),
                        });
                        setActiveModal(null);
                      } catch (requestError) {
                        setOperationError(requestError.message);
                      }
                    }}
                    type="button"
                  >
                    Send
                  </button>
                </div>
              </>
            ) : null}
            {activeModal.type === "invite" ? (
              <>
                <h2 className="text-xl font-semibold">Start group chat</h2>
                <div className="mt-4 space-y-3">
                  <input
                    className="soft-focus w-full rounded-[1.2rem] bg-surface-container-low px-4 py-3 text-sm dark:bg-dark-low"
                    placeholder="Email address"
                    value={modalForm.email}
                    onChange={(event) => setModalForm((current) => ({ ...current, email: event.target.value }))}
                  />
                  <select
                    className="h-11 w-full rounded-[1.2rem] bg-surface-container-low px-4 text-sm dark:bg-dark-low"
                    value={modalForm.role}
                    onChange={(event) => setModalForm((current) => ({ ...current, role: event.target.value }))}
                  >
                    <option value="viewer">Viewer</option>
                    <option value="editor">Editor</option>
                  </select>
                </div>
                <div className="mt-5 flex justify-end gap-2">
                  <button className="secondary-pill" onClick={() => setActiveModal(null)} type="button">
                    Cancel
                  </button>
                  <button
                    className="primary-pill"
                    onClick={() => {
                      if (!modalForm.email.trim()) {
                        return;
                      }
                      handleInvite(modalForm.email.trim(), modalForm.role);
                      setActiveModal(null);
                    }}
                    type="button"
                  >
                    Invite
                  </button>
                </div>
              </>
            ) : null}
            {activeModal.type === "share" ? (
              <>
                <h2 className="text-xl font-semibold">Share trip</h2>
                <div className="mt-4 space-y-3">
                  <input
                    className="soft-focus w-full rounded-[1.2rem] bg-surface-container-low px-4 py-3 text-sm dark:bg-dark-low"
                    readOnly
                    value={modalForm.link}
                  />
                </div>
                <div className="mt-5 flex justify-end gap-2">
                  <button className="secondary-pill" onClick={() => setActiveModal(null)} type="button">
                    Close
                  </button>
                  <button
                    className="primary-pill"
                    onClick={() => {
                      navigator.clipboard
                        .writeText(modalForm.link)
                        .then(() => setShareNotice("Link copied."))
                        .catch(() => setShareNotice("Unable to copy link."));
                      setActiveModal(null);
                    }}
                    type="button"
                  >
                    Copy link
                  </button>
                </div>
              </>
            ) : null}
          </div>
        </div>
      ) : null}
    </main>
  );
}

export default PlannerDashboard;
