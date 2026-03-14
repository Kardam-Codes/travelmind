/*
Feature: Shared UI
File Purpose: Render the global floating navigation with theme switching
Owner: Jay
Dependencies: React Router, ThemeProvider, Icon
Last Updated: 2026-03-13
*/
import { NavLink } from "react-router-dom";
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

  return (
    <div className="sticky top-0 z-50 px-4 pt-4 md:px-6">
      <nav className="glass-panel mx-auto flex max-w-7xl items-center justify-between rounded-[2rem] px-5 py-4 shadow-float md:px-7">
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
            className="flex h-11 w-11 items-center justify-center rounded-full bg-white/65 text-text transition-colors hover:text-primary dark:bg-white/10 dark:text-white"
            type="button"
          >
            <Icon className="h-5 w-5" name="bell" />
          </button>
          <button
            className="flex h-11 items-center gap-2 rounded-full bg-white/65 px-4 text-sm font-medium text-text transition-colors hover:text-primary dark:bg-white/10 dark:text-white"
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
      </nav>
    </div>
  );
}

export default TopNavBar;
