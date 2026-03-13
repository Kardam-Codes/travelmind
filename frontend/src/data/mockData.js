/*
Feature: Frontend Data
File Purpose: Provide mock content for the TravelMind frontend experience
Owner: Jay
Dependencies: None
Last Updated: 2026-03-13
*/
const imageUrls = {
  jaipurHawaMahal:
    "https://commons.wikimedia.org/wiki/Special:Redirect/file/Hawa%20Mahal-Jaipur-Rajasthan.jpg",
  goaBeach:
    "https://commons.wikimedia.org/wiki/Special:Redirect/file/Goa%20beautiful%20beach.JPG",
  munnarTeaGardens:
    "https://commons.wikimedia.org/wiki/Special:Redirect/file/Munnar%20%28Kerala%29%20Tea%20Gardens.jpg",
  varanasiGhat:
    "https://commons.wikimedia.org/wiki/Special:Redirect/file/Varanasi%20ghat.jpg",
  keralaBackwaters:
    "https://commons.wikimedia.org/wiki/Special:Redirect/file/A%20Houseboat%20in%20Backwaters%20of%20Kerala.jpg",
  udaipurLakePalace:
    "https://commons.wikimedia.org/wiki/Special:Redirect/file/Lake%20palace%20-%20Udaipur.jpg",
};

export const inspirationCards = [
  {
    title: "Jaipur at First Light",
    eyebrow: "Royal heritage",
    summary: "Palace courtyards, old-city bazaars, and sunrise fort views shaped into a composed Rajasthan escape.",
    image: imageUrls.jaipurHawaMahal,
    size: "large",
  },
  {
    title: "Goa by Monsoon Tide",
    eyebrow: "Coastal editorial",
    summary: "Beach clubs, Portuguese lanes, and late golden-hour drives along the Konkan edge.",
    image: imageUrls.goaBeach,
    size: "tall",
  },
  {
    title: "Munnar in Cloud Mist",
    eyebrow: "Highland calm",
    summary: "Tea hills, cool weather, and long scenic drives with a quieter, slower rhythm.",
    image: imageUrls.munnarTeaGardens,
    size: "square",
  },
];

export const features = [
  {
    title: "AI itinerary generation",
    description:
      "Natural-language requests become day-by-day plans with pacing, dining, stay, and activity logic.",
    icon: "sparkles",
  },
  {
    title: "Map-based trip planning",
    description:
      "Pins, routes, and travel-time context stay central so the itinerary always reflects geography.",
    icon: "map",
  },
  {
    title: "Smart recommendations",
    description:
      "Recommendations adapt to budget, group style, and destination mood without turning the UI into a dashboard.",
    icon: "compass",
  },
];

export const plannerChat = [
  {
    speaker: "TravelMind AI",
    text: "I found three heritage stays near Jaipur's old city with short drives between City Palace, Johari Bazaar, and Amber Fort. Want me to pin them on the map?",
  },
  {
    speaker: "You",
    text: "Keep the route relaxed, heritage-focused, and easy for evening bazaar walks.",
  },
];

export const suggestedPrompts = [
  "Find a haveli stay in Jaipur",
  "Suggest street food near Johari Bazaar",
  "Add a sunrise fort visit",
];

export const mapPlaces = [
  {
    id: 1,
    title: "Samode Haveli",
    category: "Stay",
    x: "22%",
    y: "38%",
    accent: "bg-primary",
  },
  {
    id: 2,
    title: "City Palace",
    category: "Dining",
    x: "58%",
    y: "48%",
    accent: "bg-tertiary",
  },
  {
    id: 3,
    title: "Amber Fort",
    category: "Morning",
    x: "68%",
    y: "26%",
    accent: "bg-primary-container",
  },
];

export const itineraryDays = [
  {
    day: "01",
    title: "Arrival and old city stroll",
    date: "Mon, Oct 14",
    items: [
      { time: "15:00", label: "Check in at a heritage haveli", travel: "25 min transfer" },
      { time: "18:30", label: "Evening walk through Johari Bazaar", travel: "12 min walk" },
    ],
  },
  {
    day: "02",
    title: "Palace and fort circuit",
    date: "Tue, Oct 15",
    items: [
      { time: "09:00", label: "Amber Fort and courtyard coffee stop", travel: "18 min drive" },
      { time: "19:30", label: "Rajasthani tasting dinner on a rooftop", travel: "10 min taxi" },
    ],
  },
  {
    day: "03",
    title: "Nahargarh sunrise morning",
    date: "Wed, Oct 16",
    items: [{ time: "08:00", label: "Nahargarh lookout before the crowds", travel: "35 min drive" }],
  },
];

export const exploreDestinations = [
  {
    name: "Jaipur",
    rating: "4.9",
    summary: "TravelMind recommends early fort visits, palace museums, and quieter dinners above the old city markets.",
    image: imageUrls.jaipurHawaMahal,
  },
  {
    name: "Varanasi",
    rating: "4.8",
    summary: "Sunrise boat rides, old ghats, and intimate heritage stays make the city feel cinematic without rushing it.",
    image: imageUrls.varanasiGhat,
  },
  {
    name: "Alleppey",
    rating: "4.7",
    summary: "Backwater houseboats, coconut groves, and slow waterfront evenings deliver a softer Kerala itinerary.",
    image: imageUrls.keralaBackwaters,
  },
];

export const budgetBreakdown = [
  { label: "Hotels", value: "$1,480" },
  { label: "Food", value: "$520" },
  { label: "Transportation", value: "$290" },
  { label: "Activities", value: "$410" },
];

export const profileTrips = {
  upcoming: [
    {
      name: "Jaipur Curations",
      dates: "Oct 14 - Oct 20",
      people: "4 travelers",
      image: imageUrls.jaipurHawaMahal,
    },
    {
      name: "Goa Slow Escape",
      dates: "Nov 04 - Nov 09",
      people: "2 travelers",
      image: imageUrls.goaBeach,
    },
  ],
  past: [
    {
      name: "Udaipur Courtyards",
      dates: "May 02 - May 07",
      people: "3 travelers",
      image: imageUrls.udaipurLakePalace,
    },
  ],
  savedPlaces: ["Johari Bazaar", "Mehrangarh Fort", "Varkala Cliff"],
  wishlist: ["Ladakh monastery loop", "Kerala backwaters", "Hampi heritage trail"],
};
