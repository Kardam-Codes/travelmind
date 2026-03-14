import { useEffect, useMemo } from "react";
import { CircleMarker, MapContainer, Polyline, TileLayer, Tooltip, useMap } from "react-leaflet";

function normalizeLatLng(value) {
  return [Number(value.lat), Number(value.lng)];
}

const INDIA_CENTER = [22.9734, 78.6569];
const INDIA_BOUNDS = [
  [6.5, 68.0],
  [35.9, 97.4],
];

function FitToData({ points }) {
  const map = useMap();

  useEffect(() => {
    if (!points.length) {
      map.setView(INDIA_CENTER, 5.8, { animate: true });
      return;
    }

    if (points.length === 1) {
      map.setView(points[0], 11, { animate: true });
      return;
    }

    map.fitBounds(points, { padding: [64, 64], animate: true });
  }, [map, points]);

  return null;
}

function TripMap({
  className = "",
  emptyMessage = "No map points are available for this trip yet.",
  fallbackMessage = "",
  places = [],
  route = null,
  selectedStopId = null,
  selectedDay = null,
  onSelectStop,
}) {
  const routeStops = useMemo(() => {
    const stops = route?.stops || [];
    return stops
      .filter((stop) => stop.latitude != null && stop.longitude != null)
      .filter((stop) => selectedDay == null || stop.day_number === selectedDay)
      .map((stop) => ({
        id: stop.item_id || `${stop.source_type}-${stop.source_id}`,
        label: stop.title,
        itemId: stop.item_id,
        position: [Number(stop.latitude), Number(stop.longitude)],
      }));
  }, [route, selectedDay]);
  const markerPoints = useMemo(() => {
    if (routeStops.length) {
      return routeStops;
    }

    return places
      .filter((place) => place.latitude != null && place.longitude != null)
      .map((place) => ({
        id: place.id,
        label: place.name,
        itemId: null,
        position: [Number(place.latitude), Number(place.longitude)],
      }));
  }, [places, routeStops]);
  const routePath = useMemo(() => {
    if (!route?.path?.length) {
      return [];
    }

    if (selectedDay != null && routeStops.length) {
      return routeStops.map((stop) => stop.position);
    }

    return route.path.map(normalizeLatLng);
  }, [route, routeStops, selectedDay]);
  const fitPoints = routePath.length >= 2 ? routePath : markerPoints.map((markerPoint) => markerPoint.position);
  const statusMessage = fallbackMessage;

  return (
    <div className={`relative overflow-hidden rounded-[2rem] bg-surface-container-lowest dark:bg-dark-card ${className}`}>
      <MapContainer
        center={INDIA_CENTER}
        className="h-full min-h-[20rem] w-full"
        maxBounds={INDIA_BOUNDS}
        maxBoundsViscosity={1}
        minZoom={5}
        maxZoom={16}
        scrollWheelZoom
        zoom={6}
        zoomDelta={0.5}
        zoomSnap={0.5}
        wheelDebounceTime={40}
      >
        <TileLayer
          attribution='&copy; <a href="https://carto.com/attributions">CARTO</a> &copy; <a href="https://www.openstreetmap.org/copyright">OpenStreetMap</a>'
          url="https://{s}.basemaps.cartocdn.com/light_all/{z}/{x}/{y}{r}.png"
        />
        <FitToData points={fitPoints} />
        {markerPoints.map((markerPoint) => (
          <CircleMarker
            key={markerPoint.id}
            center={markerPoint.position}
            eventHandlers={markerPoint.itemId && onSelectStop ? { click: () => onSelectStop(markerPoint.itemId) } : undefined}
            pathOptions={{
              color: markerPoint.itemId === selectedStopId ? "#8C2500" : "#00535B",
              fillColor: markerPoint.itemId === selectedStopId ? "#8C2500" : "#D97706",
              fillOpacity: 0.95,
              weight: markerPoint.itemId === selectedStopId ? 3 : 2,
            }}
            radius={markerPoint.itemId === selectedStopId ? 10 : 8}
          >
            <Tooltip>{markerPoint.label}</Tooltip>
          </CircleMarker>
        ))}
        {routePath.length >= 2 ? <Polyline pathOptions={{ color: "#00535B", opacity: 0.9, weight: 4 }} positions={routePath} /> : null}
      </MapContainer>
      {!markerPoints.length ? (
        <div className="absolute inset-0 flex items-center justify-center bg-surface-container-lowest/95 px-6 text-center text-sm text-text/65 dark:bg-dark-card/95 dark:text-white/65">
          {emptyMessage}
        </div>
      ) : null}
      {statusMessage ? (
        <div className="absolute left-4 right-4 top-4 rounded-[1rem] bg-white/90 px-4 py-3 text-sm text-tertiary shadow-ambient dark:bg-dark-card/90">
          {statusMessage}
        </div>
      ) : null}
    </div>
  );
}

export default TripMap;
