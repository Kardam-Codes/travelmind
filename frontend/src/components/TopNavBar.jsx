/*
Feature: Shared UI
File Purpose: Render the global floating navigation with theme switching
Owner: Jay
Dependencies: React Router, ThemeProvider, Icon
Last Updated: 2026-03-13
*/
import { NavLink } from "react-router-dom";
import { useState } from "react";
import { useTheme } from "./ThemeProvider";
import Icon from "./Icon";
import OrgSwitcher from "./OrgSwitcher";

const navItems = [
  { label: "Explore", to: "/explore" },
  { label: "Planner", to: "/planner" },
  { label: "My Trips", to: "/my-trips" },
  { label: "Agency", to: "/agency" },
];

function navClass({ isActive }) {
  return `rounded-full px-4 py-2 text-sm font-medium transition-colors ${
    isActive
      ? "bg-white/70 text-primary dark:bg-white/10 dark:text-white"
      : "text-text/70 hover:text-primary dark:text-white/70 dark:hover:text-white"
  }`;
}

function TopNavBar() {
  const { theme, toggleTheme } = useTheme();
  const [showTour, setShowTour] = useState(false);

  return (
    <div className="sticky top-0 z-50">
      <nav className="nav-panel w-full">
        <div className="mx-auto flex max-w-7xl items-center justify-between px-4 py-3 md:px-6">
          <div className="flex items-center gap-3 md:gap-8">
            <NavLink className="font-headline text-xl font-extrabold tracking-tight text-primary dark:text-white" to="/">
              TravelMind
            </NavLink>
            <div className="hidden items-center gap-2 md:flex">
              {navItems.map((item) => (
                <NavLink key={item.to} className={navClass} to={item.to}>
                  {item.label}
                </NavLink>
              ))}
            </div>
          </div>

          <div className="flex items-center gap-2 md:gap-3">
            <OrgSwitcher />
            <button
              aria-label="Open app tour"
              className="flex h-11 w-11 items-center justify-center rounded-full bg-white/50 text-text transition-colors hover:text-primary dark:bg-white/10 dark:text-white"
              onClick={() => setShowTour(true)}
              type="button"
            >
              <Icon className="h-5 w-5" name="info" />
            </button>
            <button
              className="flex h-11 w-11 items-center justify-center rounded-full bg-white/50 text-text transition-colors hover:text-primary dark:bg-white/10 dark:text-white"
              type="button"
            >
              <Icon className="h-5 w-5" name="bell" />
            </button>
            <button
              className="flex h-11 items-center gap-2 rounded-full bg-white/50 px-4 text-sm font-medium text-text transition-colors hover:text-primary dark:bg-white/10 dark:text-white"
              onClick={toggleTheme}
              type="button"
            >
              <Icon className="h-4 w-4" name={theme === "light" ? "moon" : "sun"} />
              <span className="hidden sm:inline">{theme === "light" ? "Dark" : "Light"}</span>
            </button>
            <NavLink
              className="flex h-11 w-11 items-center justify-center rounded-full bg-brand-gradient text-sm font-semibold text-white"
              to="/login"
            >
              J
            </NavLink>
          </div>
        </div>
      </nav>
      {showTour ? (
        <div className="fixed inset-0 z-50 flex items-center justify-center bg-black/40 px-4">
          <div className="w-full max-w-xl rounded-[2rem] bg-surface-container-lowest p-6 shadow-float dark:bg-dark-card">
            <div className="flex items-start justify-between gap-4">
              <div>
                <p className="label-md text-tertiary">App tour</p>
                <h2 className="mt-2 text-2xl font-bold">How to use TravelMind</h2>
                <p className="mt-2 text-sm text-text/60 dark:text-white/60">
                  Quick walkthrough for first-time users.
                </p>
              </div>
              <button
                aria-label="Close tour"
                className="flex h-10 w-10 items-center justify-center rounded-full bg-secondary-container text-[#6d6356] dark:bg-white/10 dark:text-white"
                onClick={() => setShowTour(false)}
                type="button"
              >
                <Icon className="h-4 w-4" name="arrow" />
              </button>
            </div>
            <ol className="mt-5 space-y-3 text-sm text-text/70 dark:text-white/70">
              <li>1. Describe your trip on the Start page.</li>
              <li>2. Review the map and refine with the planning chat.</li>
              <li>3. Adjust day-wise itinerary cards below.</li>
              <li>4. Share or start a group plan from the header.</li>
            </ol>
          </div>
        </div>
      ) : null}
    </div>
  );
}

export default TopNavBar;
