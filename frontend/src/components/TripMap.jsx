import { useEffect, useMemo, useRef, useState } from "react";
import L from "leaflet";
import {
  MapContainer,
  Marker,
  Polyline,
  ScaleControl,
  TileLayer,
  Tooltip,
  useMap,
  useMapEvents,
  ZoomControl,
} from "react-leaflet";

function normalizeLatLng(value) {
  return [Number(value.lat), Number(value.lng)];
}

const INDIA_CENTER = [22.9734, 78.6569];
const INDIA_BOUNDS = [
  [6.5, 68.0],
  [35.9, 97.4],
];

function FitToDataControlled({ bounds, points, fitToken }) {
  const map = useMap();

  useEffect(() => {
    if (bounds) {
      map.fitBounds(bounds, { padding: [64, 64], animate: true });
      return;
    }

    if (!points.length) {
      map.setView(INDIA_CENTER, 5.8, { animate: true });
      return;
    }

    if (points.length === 1) {
      map.setView(points[0], 11, { animate: true });
      return;
    }

    map.fitBounds(points, { padding: [64, 64], animate: true });
  }, [map, bounds, points, fitToken]);

  return null;
}

function MapInteractionWatcher({ userHasMovedRef }) {
  useMapEvents({
    dragstart: () => {
      userHasMovedRef.current = true;
    },
    zoomstart: () => {
      userHasMovedRef.current = true;
    },
  });
  return null;
}

const DAY_COLORS = ["#FF7A00", "#0094FF", "#7E3FF2", "#17B26A", "#F24E1E", "#FFC107"];

function getDayColor(dayNumber) {
  if (dayNumber == null) {
    return "#00535B";
  }
  return DAY_COLORS[(dayNumber - 1) % DAY_COLORS.length];
}

function createStopIcon({ color, isSelected, order, dimmed }) {
  const size = isSelected ? 36 : 30;
  const ring = isSelected ? "0 0 0 3px rgba(255,255,255,0.9)" : "0 0 0 1px rgba(255,255,255,0.65)";
  const opacity = dimmed ? 0.4 : 1;
  return L.divIcon({
    className: "",
    iconSize: [size, size],
    iconAnchor: [size / 2, size / 2],
    html: `<div style="
      width:${size}px;height:${size}px;border-radius:999px;
      background:${color};color:#fff;font-weight:700;font-size:12px;
      display:flex;align-items:center;justify-content:center;
      box-shadow:${ring};opacity:${opacity};
    ">${order}</div>`,
  });
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
  const userHasMovedRef = useRef(false);
  const [fitToken, setFitToken] = useState(0);
  const lastSelectedDayRef = useRef(selectedDay);
  const initializedRef = useRef(false);
  const routeStops = useMemo(() => {
    const stops = route?.stops || [];
    return stops
      .filter((stop) => stop.latitude != null && stop.longitude != null)
      .filter((stop) => selectedDay == null || stop.day_number === selectedDay)
      .map((stop) => ({
        id: stop.item_id || `${stop.source_type}-${stop.source_id}`,
        label: stop.title,
        itemId: stop.item_id,
        dayNumber: stop.day_number,
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
        dayNumber: null,
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
  const bounds = useMemo(() => {
    if (!route?.bounds) {
      return null;
    }
    return [
      [route.bounds.south, route.bounds.west],
      [route.bounds.north, route.bounds.east],
    ];
  }, [route]);
  const statusMessage = fallbackMessage;
  const showRouteWarning = route?.provider_status === "directions_unavailable" || route?.provider_status === "partial";

  useEffect(() => {
    if (!initializedRef.current && (markerPoints.length || routePath.length)) {
      initializedRef.current = true;
      setFitToken((value) => value + 1);
    }
  }, [markerPoints.length, routePath.length]);

  useEffect(() => {
    if (lastSelectedDayRef.current !== selectedDay) {
      lastSelectedDayRef.current = selectedDay;
      userHasMovedRef.current = false;
      setFitToken((value) => value + 1);
    }
  }, [selectedDay]);

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
        zoomControl={false}
      >
        <TileLayer
          attribution='&copy; <a href="https://carto.com/attributions">CARTO</a> &copy; <a href="https://www.openstreetmap.org/copyright">OpenStreetMap</a>'
          url="https://{s}.basemaps.cartocdn.com/light_all/{z}/{x}/{y}{r}.png"
        />
        <ZoomControl position="bottomright" />
        <ScaleControl position="bottomleft" />
        <MapInteractionWatcher userHasMovedRef={userHasMovedRef} />
        <FitToDataControlled bounds={bounds} points={fitPoints} fitToken={fitToken} />
        {markerPoints.map((markerPoint, index) => {
          const stopDay = markerPoint.dayNumber;
          const dayColor = getDayColor(stopDay);
          const dimmed = selectedDay != null && stopDay !== selectedDay;
          return (
            <Marker
              key={markerPoint.id}
              position={markerPoint.position}
              eventHandlers={markerPoint.itemId && onSelectStop ? { click: () => onSelectStop(markerPoint.itemId) } : undefined}
              icon={createStopIcon({
                color: dayColor,
                isSelected: markerPoint.itemId === selectedStopId,
                order: index + 1,
                dimmed,
              })}
            >
              <Tooltip>
                {index + 1}. {markerPoint.label}
              </Tooltip>
            </Marker>
          );
        })}
        {routePath.length >= 2 ? (
          <Polyline
            pathOptions={{
              color: selectedDay != null ? getDayColor(selectedDay) : "#00535B",
              opacity: selectedDay != null ? 0.9 : 0.75,
              weight: 4,
              dashArray: selectedDay != null ? "6 10" : undefined,
            }}
            positions={routePath}
          />
        ) : null}
      </MapContainer>
      <div className="pointer-events-none absolute right-4 top-4 flex flex-col gap-2">
        <button
          className="pointer-events-auto rounded-full bg-white/85 px-3 py-2 text-xs font-semibold text-primary shadow-ambient"
          onClick={() => {
            userHasMovedRef.current = false;
            setFitToken((value) => value + 1);
          }}
          type="button"
        >
          Reset view
        </button>
        {showRouteWarning ? (
          <div className="rounded-full bg-white/85 px-3 py-2 text-xs font-semibold text-tertiary shadow-ambient">
            Route unavailable
          </div>
        ) : null}
      </div>
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
