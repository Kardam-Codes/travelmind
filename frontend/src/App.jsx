/*
Feature: Frontend Infrastructure
File Purpose: Define application routes and the shared shell
Owner: Jay
Dependencies: React Router, TopNavBar
Last Updated: 2026-03-13
*/
import { Navigate, Route, Routes } from "react-router-dom";
import TopNavBar from "./components/TopNavBar";
import AuthPage from "./features/auth/AuthPage";
import ExplorePage from "./features/explore/ExplorePage";
import LandingPage from "./features/landing/LandingPage";
import PlannerDashboard from "./features/planner/PlannerDashboard";
import ProfileTripsPage from "./features/profile/ProfileTripsPage";
import TripDetailsPage from "./features/trip-details/TripDetailsPage";
import AgencyDashboard from "./features/agency/AgencyDashboard";

function App() {
  return (
    <div className="min-h-screen bg-surface text-text transition-colors duration-500 dark:bg-dark-base dark:text-white">
      <TopNavBar />
      <Routes>
        <Route path="/" element={<LandingPage />} />
        <Route path="/login" element={<AuthPage />} />
        <Route path="/planner" element={<PlannerDashboard />} />
        <Route path="/agency" element={<AgencyDashboard />} />
        <Route path="/explore" element={<ExplorePage />} />
        <Route path="/trip/:tripId" element={<TripDetailsPage />} />
        <Route path="/my-trips" element={<ProfileTripsPage />} />
        <Route path="*" element={<Navigate to="/" replace />} />
      </Routes>
    </div>
  );
}

export default App;
