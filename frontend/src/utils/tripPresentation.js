function toNumber(value) {
  return typeof value === "number" ? value : Number(value);
}

export function buildMapPlaces(places = []) {
  if (!places.length) {
    return [];
  }

  const latitudes = places.map((place) => toNumber(place.latitude));
  const longitudes = places.map((place) => toNumber(place.longitude));
  const minLat = Math.min(...latitudes);
  const maxLat = Math.max(...latitudes);
  const minLng = Math.min(...longitudes);
  const maxLng = Math.max(...longitudes);
  const latRange = Math.max(maxLat - minLat, 0.01);
  const lngRange = Math.max(maxLng - minLng, 0.01);

  return places.map((place, index) => ({
    ...place,
    accent: index % 2 === 0 ? "bg-primary" : "bg-tertiary",
    x: `${18 + ((toNumber(place.longitude) - minLng) / lngRange) * 58}%`,
    y: `${18 + (1 - (toNumber(place.latitude) - minLat) / latRange) * 52}%`,
  }));
}

export function formatTripRange(trip) {
  return `${trip.duration_days} day${trip.duration_days === 1 ? "" : "s"} in ${trip.destination_city}`;
}
