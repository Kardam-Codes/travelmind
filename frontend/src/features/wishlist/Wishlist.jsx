/*
Feature: Wishlist
File Purpose: Display and manage saved travel items
Owner: Jay
Dependencies: React, Fetch
Last Updated: 2026-03-13
*/
import { useEffect, useState } from "react";
import Icon from "../../components/Icon";
import { apiRequest } from "../../utils/apiClient";
import { getStoredUser } from "../../utils/session";

function Wishlist() {
  const [items, setItems] = useState([]);
  const [error, setError] = useState("");

  useEffect(() => {
    async function loadWishlist() {
      const user = getStoredUser();
      if (!user) {
        return;
      }

      try {
        const response = await apiRequest("/wishlist/");
        setItems(response);
      } catch (requestError) {
        setError(requestError.message);
      }
    }

    loadWishlist();
  }, []);

  const savedPlaces = items.filter((item) => item.item_type === "place");
  const futureIdeas = items.filter((item) => item.item_type !== "place");

  return (
    <div className="grid gap-6 lg:grid-cols-[1.3fr,1fr]">
      <div className="card-surface space-y-5">
        <div>
          <p className="label-md text-tertiary">Saved places</p>
          <h3 className="mt-2 text-2xl font-bold">Places waiting for a trip</h3>
        </div>
        <div className="flex flex-wrap gap-3">
          {savedPlaces.map((place) => (
            <span
              key={place.id}
              className="inline-flex items-center gap-2 rounded-full bg-surface-container-low px-4 py-3 text-sm dark:bg-dark-low"
            >
              <Icon className="h-4 w-4 text-tertiary" name="pin" />
              {place.item_name}
            </span>
          ))}
          {!savedPlaces.length ? <p className="text-sm text-text/60 dark:text-white/60">No saved places yet.</p> : null}
        </div>
      </div>

      <div className="card-surface space-y-5">
        <div>
          <p className="label-md text-primary/70 dark:text-white/55">Wishlist</p>
          <h3 className="mt-2 text-2xl font-bold">Future ideas</h3>
        </div>
        <div className="space-y-3">
          {futureIdeas.map((item) => (
            <div
              key={item.id}
              className="rounded-[1.5rem] bg-surface-container-low px-4 py-4 text-sm text-text/75 dark:bg-dark-low dark:text-white/75"
            >
              {item.item_name}
            </div>
          ))}
          {error ? <p className="text-sm text-tertiary">{error}</p> : null}
          {!futureIdeas.length ? <p className="text-sm text-text/60 dark:text-white/60">Wishlist items appear here after saving hotels or activities.</p> : null}
        </div>
      </div>
    </div>
  );
}

export default Wishlist;
