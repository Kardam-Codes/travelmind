/*
Feature: API Client
File Purpose: Provide lightweight helpers for frontend API integration
Owner: Jay
Dependencies: Fetch
Last Updated: 2026-03-13
*/
const API_BASE_URL = import.meta.env.VITE_API_BASE_URL || "http://localhost:8000";

export async function apiRequest(path, options = {}) {
  const response = await fetch(`${API_BASE_URL}${path}`, {
    headers: {
      "Content-Type": "application/json",
      ...(options.headers || {}),
    },
    ...options,
  });

  if (!response.ok) {
    throw new Error(`API request failed with status ${response.status}`);
  }

  return response.json();
}

export function buildTripWebSocketUrl(tripId) {
  const base = API_BASE_URL.replace(/^http/, "ws");
  return `${base}/ws/trip/${tripId}`;
}
