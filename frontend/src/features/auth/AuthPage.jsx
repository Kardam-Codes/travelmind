/*
Feature: Authentication
File Purpose: Render the login and signup access page
Owner: Jay
Dependencies: React, Icon
Last Updated: 2026-03-13
*/
import Icon from "../../components/Icon";

function AuthPage() {
  return (
    <main className="min-h-[calc(100vh-6rem)] px-4 pb-16 pt-12 md:px-6">
      <div className="mx-auto grid max-w-6xl items-center gap-10 lg:grid-cols-[1fr,28rem]">
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
              src="https://commons.wikimedia.org/wiki/Special:Redirect/file/Munnar%20%28Kerala%29%20Tea%20Gardens.jpg"
            />
          </div>
        </section>

        <section className="section-shell mx-auto w-full max-w-md bg-secondary-container/60 dark:bg-dark-low">
          <div className="card-surface rounded-[2.5rem] p-8 md:p-10">
            <p className="label-md text-primary/70 dark:text-white/55">Welcome back</p>
            <h2 className="mt-3 text-3xl font-bold">Login to your portal</h2>
            <p className="mt-3 text-sm leading-7 text-text/65 dark:text-white/65">
              Keep authentication simple so planning starts immediately.
            </p>

            <form className="mt-8 space-y-5">
              <label className="block">
                <span className="label-md text-text/55 dark:text-white/55">Email</span>
                <input
                  className="soft-focus mt-2 w-full rounded-[1.5rem] bg-surface-container-low px-5 py-4 dark:bg-dark-low"
                  placeholder="curator@travelmind.com"
                  type="email"
                />
              </label>
              <label className="block">
                <span className="label-md text-text/55 dark:text-white/55">Password</span>
                <input
                  className="soft-focus mt-2 w-full rounded-[1.5rem] bg-surface-container-low px-5 py-4 dark:bg-dark-low"
                  placeholder="••••••••••"
                  type="password"
                />
              </label>

              <button className="primary-pill w-full py-4" type="button">
                Login
              </button>
              <button className="secondary-pill w-full py-4" type="button">
                Sign up
              </button>
              <button
                className="flex w-full items-center justify-center gap-3 rounded-full bg-surface-container-low px-5 py-4 font-medium dark:bg-dark-low"
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
