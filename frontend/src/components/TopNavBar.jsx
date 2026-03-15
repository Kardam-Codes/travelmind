/*
Feature: Shared UI
File Purpose: Render the global floating navigation with theme switching
Owner: Jay
Dependencies: React Router, ThemeProvider, Icon
Last Updated: 2026-03-13
*/
import { NavLink } from "react-router-dom";
import { useEffect, useState } from "react";
import { useTheme } from "./ThemeProvider";
import OrgSwitcher from "./OrgSwitcher";
import Icon from "./Icon";

const navItems = [
  { label: "Planner", to: "/planner" },
  { label: "My Trips", to: "/my-trips" },
  { label: "Explore", to: "/explore" },
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
  const [isCompact, setIsCompact] = useState(false);
  const [scrollProgress, setScrollProgress] = useState(0);

  useEffect(() => {
    function handleScroll() {
      const scrollTop = window.scrollY || document.documentElement.scrollTop;
      const docHeight = document.documentElement.scrollHeight - document.documentElement.clientHeight;
      const progress = docHeight > 0 ? Math.min(1, scrollTop / docHeight) : 0;
      setScrollProgress(progress);
      setIsCompact(scrollTop > 12);
    }

    handleScroll();
    window.addEventListener("scroll", handleScroll, { passive: true });
    return () => window.removeEventListener("scroll", handleScroll);
  }, []);

  return (
    <div className="sticky top-0 z-50">
      <nav className={`nav-panel w-full ${isCompact ? "nav-compact" : ""}`}>
        <div
          className={`mx-auto flex max-w-7xl items-center justify-between px-4 md:px-6 ${
            isCompact ? "py-1.5" : "py-3"
          }`}
        >
          <div className="flex items-center gap-3 md:gap-8">
            <NavLink
              className={`font-headline font-extrabold tracking-tight text-primary transition-all dark:text-white ${
                isCompact ? "text-lg" : "text-xl"
              }`}
              to="/"
            >
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
              className="flex h-11 items-center gap-2 rounded-full bg-white/50 px-4 text-sm font-medium text-text transition-colors hover:text-primary dark:bg-white/10 dark:text-white"
              onClick={toggleTheme}
              type="button"
            >
              <Icon className="h-4 w-4" name={theme === "light" ? "moon" : "sun"} />
              <span className="hidden sm:inline">{theme === "light" ? "Dark" : "Light"}</span>
            </button>
          </div>
        </div>
        <div className="h-[4px] w-full overflow-hidden rounded-full bg-primary/10">
          <div
            className="h-full rounded-full bg-primary transition-[width] duration-300 ease-out"
            style={{ width: `${scrollProgress * 100}%` }}
          />
        </div>
      </nav>
    </div>
  );
}

export default TopNavBar;
