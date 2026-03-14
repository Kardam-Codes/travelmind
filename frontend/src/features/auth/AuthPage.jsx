/*
Feature: Authentication
File Purpose: Render the login and signup access page
Owner: Jay
Dependencies: React, Icon, Fetch
Last Updated: 2026-03-13
*/
import { useState } from "react";
import { useNavigate } from "react-router-dom";
import Icon from "../../components/Icon";
import { apiRequest } from "../../utils/apiClient";
import { setActiveOrgId, setStoredUser } from "../../utils/session";
import heroImage from "../../assets/hero.svg";

function AuthPage() {
  const navigate = useNavigate();
  const [mode, setMode] = useState("login");
  const [form, setForm] = useState({ email: "", password: "", name: "" });
  const [error, setError] = useState("");
  const [isSubmitting, setIsSubmitting] = useState(false);
  const [showPassword, setShowPassword] = useState(false);

  function updateField(field, value) {
    setForm((current) => ({ ...current, [field]: value }));
  }

  async function handleSubmit() {
    setIsSubmitting(true);
    setError("");

    try {
      const response =
        mode === "signup"
          ? await apiRequest("/auth/signup", {
              method: "POST",
              body: JSON.stringify({ email: form.email, password: form.password, name: form.name }),
            })
          : await apiRequest("/auth/login", {
              method: "POST",
              body: JSON.stringify({ email: form.email, password: form.password }),
            });

      setStoredUser(response);
      if (response.default_org_id) {
        setActiveOrgId(response.default_org_id);
      }
      navigate(mode === "signup" ? "/start" : "/my-trips");
    } catch (requestError) {
      setError(requestError.message);
    } finally {
      setIsSubmitting(false);
    }
  }

  async function handleGoogleAuth() {
    setIsSubmitting(true);
    setError("");

    try {
      const response = await apiRequest("/auth/google", {
        method: "POST",
        body: JSON.stringify({
          email: form.email,
          name: form.name || form.email.split("@")[0],
        }),
      });
      setStoredUser(response);
      if (response.default_org_id) {
        setActiveOrgId(response.default_org_id);
      }
      navigate("/my-trips");
    } catch (requestError) {
      setError(requestError.message);
    } finally {
      setIsSubmitting(false);
    }
  }

  return (
    <main className="min-h-[calc(100vh-6rem)] px-4 pb-16 pt-12 md:px-6">
      <div className="mx-auto grid max-w-6xl items-center gap-10 lg:grid-cols-[1.1fr,30rem]">
        <section className="hidden lg:block">
          <div className="space-y-5">
            <p className="label-md text-tertiary">Access your concierge</p>
            <h1 className="max-w-xl text-6xl font-extrabold leading-[1.02] text-balance">
              Experience luxury beyond borders.
            </h1>
            <p className="max-w-lg text-lg leading-8 text-text/65 dark:text-white/65">
              Access your itineraries, curated stays, and route-aware planning sessions in one focused space.
            </p>
          </div>
          <div className="mt-10 overflow-hidden rounded-[2.5rem] shadow-float">
            <img
              alt="Travel inspiration"
              className="h-[34rem] w-full object-cover"
              onError={(event) => {
                event.currentTarget.src = heroImage;
              }}
              src={heroImage}
            />
          </div>
        </section>

        <section className="section-shell mx-auto w-full max-w-md bg-secondary-container/60 dark:bg-dark-low">
          <div className="card-surface rounded-[2.5rem] p-8 md:p-10">
            <div className="flex items-center justify-between gap-4">
              <div>
                <p className="label-md text-primary/70 dark:text-white/55">Welcome</p>
                <h2 className="mt-2 text-3xl font-bold">{mode === "signup" ? "Create your portal" : "Login to your portal"}</h2>
              </div>
              <div className="flex rounded-full bg-surface-container-low p-1 dark:bg-dark-low">
                <button
                  className={`rounded-full px-4 py-2 text-sm font-medium transition ${
                    mode === "login" ? "bg-white text-primary shadow-soft dark:bg-white/10 dark:text-white" : "text-text/60 dark:text-white/60"
                  }`}
                  onClick={() => setMode("login")}
                  type="button"
                >
                  Login
                </button>
                <button
                  className={`rounded-full px-4 py-2 text-sm font-medium transition ${
                    mode === "signup" ? "bg-white text-primary shadow-soft dark:bg-white/10 dark:text-white" : "text-text/60 dark:text-white/60"
                  }`}
                  onClick={() => setMode("signup")}
                  type="button"
                >
                  Sign up
                </button>
              </div>
            </div>
            <p className="mt-3 text-sm leading-7 text-text/65 dark:text-white/65">
              Keep authentication simple so planning starts immediately.
            </p>

            <form className="mt-8 space-y-5" onSubmit={(event) => event.preventDefault()}>
              {mode === "signup" ? (
                <label className="block">
                  <span className="label-md text-text/55 dark:text-white/55">Name</span>
                  <input
                    className="soft-focus mt-2 w-full rounded-[1.5rem] bg-surface-container-low px-5 py-4 dark:bg-dark-low"
                    onChange={(event) => updateField("name", event.target.value)}
                    placeholder="Curated traveler"
                    type="text"
                    value={form.name}
                  />
                </label>
              ) : null}
              <label className="block">
                <span className="label-md text-text/55 dark:text-white/55">Email</span>
                <input
                  className="soft-focus mt-2 w-full rounded-[1.5rem] bg-surface-container-low px-5 py-4 dark:bg-dark-low"
                  onChange={(event) => updateField("email", event.target.value)}
                  placeholder="curator@travelmind.com"
                  type="email"
                  value={form.email}
                />
              </label>
              <label className="block">
                <span className="label-md text-text/55 dark:text-white/55">Password</span>
                <div className="soft-focus mt-2 flex items-center rounded-[1.5rem] bg-surface-container-low px-5 py-4 dark:bg-dark-low">
                  <input
                    className="w-full bg-transparent focus:outline-none"
                    onChange={(event) => updateField("password", event.target.value)}
                    placeholder="Enter password"
                    type={showPassword ? "text" : "password"}
                    value={form.password}
                  />
                  <button
                    aria-label={showPassword ? "Hide password" : "Show password"}
                    className="ml-3 text-text/60 transition hover:text-primary dark:text-white/60 dark:hover:text-white"
                    onClick={() => setShowPassword((prev) => !prev)}
                    type="button"
                  >
                    <Icon className="h-5 w-5" name={showPassword ? "eyeOff" : "eye"} />
                  </button>
                </div>
              </label>
              {error ? <p className="text-sm text-tertiary">{error}</p> : null}

              <button className="primary-pill w-full py-4" disabled={isSubmitting} onClick={handleSubmit} type="button">
                {isSubmitting ? (mode === "signup" ? "Creating account..." : "Logging in...") : mode === "signup" ? "Create account" : "Login"}
              </button>
              {mode === "signup" ? (
                <p className="text-center text-sm text-text/60 dark:text-white/60">
                  Already have an account?{" "}
                  <button className="font-semibold text-primary hover:underline dark:text-white" onClick={() => setMode("login")} type="button">
                    Login
                  </button>
                </p>
              ) : (
                <p className="text-center text-sm text-text/60 dark:text-white/60">
                  New here?{" "}
                  <button className="font-semibold text-primary hover:underline dark:text-white" onClick={() => setMode("signup")} type="button">
                    Create an account
                  </button>
                </p>
              )}
              <button
                className="flex w-full items-center justify-center gap-3 rounded-full bg-surface-container-low px-5 py-4 font-medium dark:bg-dark-low disabled:opacity-60"
                disabled={isSubmitting || !form.email}
                onClick={handleGoogleAuth}
                type="button"
              >
                <Icon className="h-5 w-5" name="sparkles" />
                Continue with Google
              </button>
            </form>
          </div>
        </section>
      </div>
    </main>
  );
}

export default AuthPage;
