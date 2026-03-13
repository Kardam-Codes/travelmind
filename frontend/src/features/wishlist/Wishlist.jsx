/*
Feature: Wishlist
File Purpose: Display and manage saved travel items
Owner: Jay
Dependencies: React
<<<<<<< HEAD
Last Updated: 2026-03-13
*/
import { profileTrips } from "../../data/mockData";
import Icon from "../../components/Icon";

function Wishlist() {
  return (
    <div className="grid gap-6 lg:grid-cols-[1.3fr,1fr]">
      <div className="card-surface space-y-5">
        <div>
          <p className="label-md text-tertiary">Saved places</p>
          <h3 className="mt-2 text-2xl font-bold">Places waiting for a trip</h3>
        </div>
        <div className="flex flex-wrap gap-3">
          {profileTrips.savedPlaces.map((place) => (
            <span
              key={place}
              className="inline-flex items-center gap-2 rounded-full bg-surface-container-low px-4 py-3 text-sm dark:bg-dark-low"
            >
              <Icon className="h-4 w-4 text-tertiary" name="pin" />
              {place}
            </span>
          ))}
        </div>
      </div>

      <div className="card-surface space-y-5">
        <div>
          <p className="label-md text-primary/70 dark:text-white/55">Wishlist</p>
          <h3 className="mt-2 text-2xl font-bold">Future ideas</h3>
        </div>
        <div className="space-y-3">
          {profileTrips.wishlist.map((item) => (
            <div
              key={item}
              className="rounded-[1.5rem] bg-surface-container-low px-4 py-4 text-sm text-text/75 dark:bg-dark-low dark:text-white/75"
            >
              {item}
            </div>
          ))}
        </div>
      </div>
    </div>
  );
}

export default Wishlist;
=======
Last Updated: Initial Setup
*/
>>>>>>> 638a1aea47b64a810dd39dd868634e645b090689
