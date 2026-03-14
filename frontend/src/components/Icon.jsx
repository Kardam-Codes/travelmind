/*
Feature: Shared UI
File Purpose: Render a small set of inline SVG icons without external icon libraries
Owner: Jay
Dependencies: React
Last Updated: 2026-03-13
*/
const paths = {
  bell: "M15 17h5l-1.4-1.4A2 2 0 0 1 18 14.2V11a6 6 0 1 0-12 0v3.2a2 2 0 0 1-.6 1.4L4 17h5m3 0v1a2 2 0 1 1-4 0v-1m4 0H8",
  sun: "M12 4V2m0 20v-2m8-8h2M2 12h2m12.95 6.95 1.41 1.41M4.64 4.64l1.41 1.41m10.9-1.41-1.41 1.41M6.05 17.95l-1.41 1.41M12 16a4 4 0 1 0 0-8 4 4 0 0 0 0 8Z",
  moon: "M20 14.5A8.5 8.5 0 1 1 9.5 4 7 7 0 0 0 20 14.5Z",
  sparkles: "m12 3 1.7 4.3L18 9l-4.3 1.7L12 15l-1.7-4.3L6 9l4.3-1.7L12 3Zm7 10 1 2.5L22.5 17 20 18l-1 2.5L18 18l-2.5-1 2.5-1.5L19 13Zm-14 4 1 2.5L8.5 21 6 22l-1 2.5L4 22l-2.5-1L4 19.5 5 17Z",
  map: "M3 6.5 9 4l6 2.5L21 4v13.5L15 20l-6-2.5L3 20V6.5Zm6-2.5v13.5m6-11V20",
  compass: "M12 22a10 10 0 1 0 0-20 10 10 0 0 0 0 20Zm4-14-2.5 6.5L7 17l2.5-6.5L16 8Z",
  search: "m21 21-4.3-4.3m1.3-5.2a6.5 6.5 0 1 1-13 0 6.5 6.5 0 0 1 13 0Z",
  arrow: "M5 12h14m-5-5 5 5-5 5",
  route: "M5 18a2 2 0 1 0 0-4 2 2 0 0 0 0 4Zm14-10a2 2 0 1 0 0-4 2 2 0 0 0 0 4ZM7 16c4.5-6 6-6 10-10",
  calendar: "M7 3v3m10-3v3M4 9h16M6 5h12a2 2 0 0 1 2 2v11a2 2 0 0 1-2 2H6a2 2 0 0 1-2-2V7a2 2 0 0 1 2-2Z",
  users: "M16 21v-2a4 4 0 0 0-4-4H7a4 4 0 0 0-4 4v2m18 0v-2a4 4 0 0 0-3-3.9m-4-9.6a4 4 0 1 1-8 0 4 4 0 0 1 8 0Zm6 4a4 4 0 1 1-4-4",
  wallet: "M3 7.5A2.5 2.5 0 0 1 5.5 5H19a2 2 0 0 1 2 2v1H5.5A2.5 2.5 0 0 0 3 10.5v7A2.5 2.5 0 0 0 5.5 20H20a2 2 0 0 0 2-2v-7H17a2 2 0 1 1 0-4h5",
  plus: "M12 5v14m7-7H5",
  send: "m22 2-7 20-4-9-9-4 20-7Z",
  drag: "M10 6h4M10 12h4m-4 6h4",
  pin: "M12 21s-6-5.2-6-10a6 6 0 1 1 12 0c0 4.8-6 10-6 10Zm0-8.5a2.5 2.5 0 1 0 0-5 2.5 2.5 0 0 0 0 5Z",
  heart: "m12 20-1.4-1.3C5.4 14 2 10.9 2 7a5 5 0 0 1 9-3 5 5 0 0 1 9 3c0 3.9-3.4 7-8.6 11.7L12 20Z",
  clock: "M12 7v5l3 2m7-2a10 10 0 1 1-20 0 10 10 0 0 1 20 0Z",
  chat: "M7 18 3 21V5a2 2 0 0 1 2-2h14a2 2 0 0 1 2 2v11a2 2 0 0 1-2 2H7Z",
  eye: "M2 12s3.5-6 10-6 10 6 10 6-3.5 6-10 6-10-6-10-6Zm10 4a4 4 0 1 0 0-8 4 4 0 0 0 0 8Z",
  eyeOff:
    "m3 5 16 16M10.6 6.5A9.7 9.7 0 0 1 12 6c6.5 0 10 6 10 6a18.8 18.8 0 0 1-3.3 4.2M6.2 8.3A18.8 18.8 0 0 0 2 12s3.5 6 10 6c1.6 0 3-.3 4.3-.9M9.5 9.5a4 4 0 0 0 5.6 5.6",
};

function Icon({ name, className = "h-5 w-5", strokeWidth = 1.8 }) {
  return (
    <svg
      aria-hidden="true"
      className={className}
      fill="none"
      stroke="currentColor"
      strokeLinecap="round"
      strokeLinejoin="round"
      strokeWidth={strokeWidth}
      viewBox="0 0 24 24"
    >
      <path d={paths[name]} />
    </svg>
  );
}

export default Icon;
