/*
Feature: API Client
File Purpose: Provide lightweight helpers for frontend API integration
Owner: Jay
Dependencies: Fetch
Last Updated: 2026-03-13
*/
import { getActiveOrgId, getStoredUser } from "./session";

const API_BASE_URL = import.meta.env.VITE_API_BASE_URL || "http://localhost:8000";

export async function apiRequest(path, options = {}) {
  const storedUser = getStoredUser();
  const activeOrgId = getActiveOrgId();
  const authHeader = storedUser?.access_token ? { Authorization: `Bearer ${storedUser.access_token}` } : {};
  const orgHeader = activeOrgId ? { "X-Org-Id": activeOrgId } : {};
  const response = await fetch(`${API_BASE_URL}${path}`, {
    headers: {
      "Content-Type": "application/json",
      ...authHeader,
      ...orgHeader,
      ...(options.headers || {}),
    },
    ...options,
  });

  if (!response.ok) {
    let detail = `API request failed with status ${response.status}`;

    try {
      const errorBody = await response.json();
      detail = errorBody.detail || errorBody.message || detail;
    } catch {
      // Keep the default message when the response body is not JSON.
    }

    throw new Error(detail);
  }

  if (response.status === 204) {
    return null;
  }

  return response.json();
}

export function buildTripWebSocketUrl(tripId, userId = "") {
  const base = API_BASE_URL.replace(/^http/, "ws");
  const storedUser = getStoredUser();
  const token = storedUser?.access_token;
  const queryParts = [];
  if (token) {
    queryParts.push(`token=${encodeURIComponent(token)}`);
  }
  if (userId) {
    queryParts.push(`user_id=${encodeURIComponent(userId)}`);
  }
  const query = queryParts.length ? `?${queryParts.join("&")}` : "";
  return `${base}/ws/trip/${tripId}${query}`;
}
