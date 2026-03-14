const USER_STORAGE_KEY = "travelmind-user";
const ACTIVE_TRIP_STORAGE_KEY = "travelmind-active-trip";

export function getStoredUser() {
  const rawValue = localStorage.getItem(USER_STORAGE_KEY);
  if (!rawValue) {
    return null;
  }

  try {
    return JSON.parse(rawValue);
  } catch {
    localStorage.removeItem(USER_STORAGE_KEY);
    return null;
  }
}

export function setStoredUser(user) {
  localStorage.setItem(USER_STORAGE_KEY, JSON.stringify(user));
}

export function clearStoredUser() {
  localStorage.removeItem(USER_STORAGE_KEY);
}

export function getActiveTripId() {
  return localStorage.getItem(ACTIVE_TRIP_STORAGE_KEY);
}

export function setActiveTripId(tripId) {
  localStorage.setItem(ACTIVE_TRIP_STORAGE_KEY, String(tripId));
}
