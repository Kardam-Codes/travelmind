import { useEffect, useState } from "react";
import { apiRequest } from "../../utils/apiClient";
import { getActiveOrgId, getStoredUser } from "../../utils/session";

const DEMO_REPORT = {
  kpis: {
    total_requests: 12,
    total_offers: 8,
    total_clicks: 21,
    total_commission: 42500,
  },
};

const DEMO_REQUESTS = [
  { id: 1, traveler_name: "Aanya Mehta", traveler_email: "aanya@demo.com", status: "assigned", assigned_agent_id: 12 },
  { id: 2, traveler_name: "Rishi Kulkarni", traveler_email: "rishi@demo.com", status: "quoted", assigned_agent_id: 9 },
  { id: 3, traveler_name: "Leena Das", traveler_email: "leena@demo.com", status: "pending", assigned_agent_id: null },
];

const DEMO_MEMBERS = [
  { id: 1, user_id: 12, role: "admin" },
  { id: 2, user_id: 9, role: "agent" },
  { id: 3, user_id: 7, role: "agent" },
];

function StatCard({ label, value }) {
  return (
    <div className="rounded-[1.25rem] bg-surface-container-lowest px-5 py-4 shadow-ambient dark:bg-dark-card">
      <p className="label-md text-text/45 dark:text-white/45">{label}</p>
      <p className="mt-2 text-2xl font-bold">{value}</p>
    </div>
  );
}

function AgencyDashboard() {
  const storedUser = getStoredUser();
  const activeOrgId = getActiveOrgId() || storedUser?.default_org_id;
  const [members, setMembers] = useState([]);
  const [requests, setRequests] = useState([]);
  const [report, setReport] = useState(null);
  const [error, setError] = useState("");

  useEffect(() => {
    if (!activeOrgId) {
      return;
    }

    async function loadAgencyData() {
      try {
        const [membersResponse, requestsResponse, reportResponse] = await Promise.all([
          apiRequest(`/orgs/${activeOrgId}/members`),
          apiRequest("/bookings/requests"),
          apiRequest("/reports/agency"),
        ]);
        const resolvedMembers = membersResponse || [];
        const resolvedRequests = requestsResponse || [];
        const resolvedReport = reportResponse || null;
        if (!resolvedRequests.length || !resolvedReport?.kpis) {
          setMembers(resolvedMembers.length ? resolvedMembers : DEMO_MEMBERS);
          setRequests(resolvedRequests.length ? resolvedRequests : DEMO_REQUESTS);
          setReport(resolvedReport?.kpis ? resolvedReport : DEMO_REPORT);
        } else {
          setMembers(resolvedMembers);
          setRequests(resolvedRequests);
          setReport(resolvedReport);
        }
        setError("");
      } catch (requestError) {
        setMembers(DEMO_MEMBERS);
        setRequests(DEMO_REQUESTS);
        setReport(DEMO_REPORT);
        setError(requestError.message);
      }
    }

    loadAgencyData();
  }, [activeOrgId]);

  async function updateRequest(requestId, status, assignedAgentId) {
    try {
      const payload = {
        status,
        assigned_agent_id: assignedAgentId ? Number(assignedAgentId) : null,
      };
      await apiRequest(`/bookings/requests/${requestId}`, {
        method: "PATCH",
        body: JSON.stringify(payload),
      });
      const refreshed = await apiRequest("/bookings/requests");
      setRequests(refreshed || []);
    } catch (requestError) {
      setError(requestError.message);
    }
  }

  if (!storedUser) {
    return (
      <main className="mx-auto max-w-6xl px-4 pb-16 pt-10 md:px-6">
        <div className="section-shell">
          <h1 className="text-3xl font-bold">Agency workspace</h1>
          <p className="mt-4 text-sm text-text/60 dark:text-white/60">Login to access org management and reporting.</p>
        </div>
      </main>
    );
  }

  return (
    <main className="mx-auto max-w-7xl px-4 pb-16 pt-10 md:px-6">
      <section className="section-shell">
        <p className="label-md text-tertiary">Agency command</p>
        <h1 className="mt-2 text-4xl font-bold">Operations, bookings, and performance</h1>
        <p className="mt-3 text-sm text-text/65 dark:text-white/65">
          Track booking requests, manage your team, and review performance across active trips.
        </p>
      </section>

      <section className="mt-10 grid gap-4 md:grid-cols-4">
        <StatCard label="Requests" value={report?.kpis?.total_requests ?? "—"} />
        <StatCard label="Offers" value={report?.kpis?.total_offers ?? "—"} />
        <StatCard label="Clicks" value={report?.kpis?.total_clicks ?? "—"} />
        <StatCard label="Commission" value={report?.kpis?.total_commission ? `Rs ${report.kpis.total_commission}` : "—"} />
      </section>

      <section className="mt-12 grid gap-6 lg:grid-cols-[1.1fr,1fr]">
        <div className="section-shell">
          <div className="flex items-center justify-between">
            <div>
              <p className="label-md text-tertiary">Booking requests</p>
              <h2 className="mt-2 text-2xl font-semibold">Queue</h2>
            </div>
          </div>
          <div className="mt-6 space-y-4">
            {requests.length ? (
              requests.map((request) => (
                <div key={request.id} className="rounded-[1.25rem] bg-surface-container-lowest px-4 py-4 dark:bg-dark-card">
                  <p className="text-sm font-semibold">{request.traveler_name}</p>
                  <p className="mt-1 text-xs text-text/55 dark:text-white/55">{request.traveler_email}</p>
                  <p className="mt-3 text-xs text-text/60 dark:text-white/60">
                    Status: <span className="font-semibold">{request.status}</span>
                  </p>
                  <div className="mt-4 grid gap-2">
                    <select
                      className="h-10 rounded-full bg-surface-container-low px-4 text-xs font-semibold text-text dark:bg-dark-low dark:text-white"
                      defaultValue={request.status}
                      onChange={(event) => updateRequest(request.id, event.target.value, request.assigned_agent_id)}
                    >
                      <option value="pending">pending</option>
                      <option value="assigned">assigned</option>
                      <option value="quoted">quoted</option>
                      <option value="closed">closed</option>
                    </select>
                    <input
                      className="h-10 rounded-full bg-surface-container-low px-4 text-xs text-text dark:bg-dark-low dark:text-white"
                      defaultValue={request.assigned_agent_id || ""}
                      onBlur={(event) => updateRequest(request.id, request.status, event.target.value)}
                      placeholder="Assign agent id"
                      type="number"
                    />
                  </div>
                </div>
              ))
            ) : (
              <p className="text-sm text-text/60 dark:text-white/60">No booking requests yet.</p>
            )}
          </div>
        </div>

        <div className="section-shell">
          <div>
            <p className="label-md text-tertiary">Team</p>
            <h2 className="mt-2 text-2xl font-semibold">Members</h2>
          </div>
          <div className="mt-6 space-y-3">
            {members.length ? (
              members.map((member) => (
                <div key={member.id} className="flex items-center justify-between rounded-[1.25rem] bg-surface-container-lowest px-4 py-3 dark:bg-dark-card">
                  <p className="text-sm font-medium">User {member.user_id}</p>
                  <span className="text-xs font-semibold uppercase tracking-wide text-text/50 dark:text-white/50">{member.role}</span>
                </div>
              ))
            ) : (
              <p className="text-sm text-text/60 dark:text-white/60">No members yet.</p>
            )}
          </div>
        </div>
      </section>

      {error ? <p className="mt-8 text-sm text-tertiary">{error}</p> : null}
    </main>
  );
}

export default AgencyDashboard;
