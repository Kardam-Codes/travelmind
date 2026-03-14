const DEMO_MODE_KEY = "travelmind-demo-mode";
const ENV_DEMO_MODE = (import.meta.env.VITE_DEMO_MODE || "").toLowerCase() === "true";

export const DEMO_PROMPT = "Plan a 4 day Jaipur trip under 25000 with heritage and food";

export function getDemoMode() {
  if (ENV_DEMO_MODE) {
    return true;
  }
  const stored = localStorage.getItem(DEMO_MODE_KEY);
  return stored === "true";
}

export function setDemoMode(value) {
  localStorage.setItem(DEMO_MODE_KEY, value ? "true" : "false");
}

export function getDemoLabel() {
  return "Demo mode is on -- use the sample prompt to drive the judge walkthrough.";
}
