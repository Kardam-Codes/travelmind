/*
Feature: Frontend Infrastructure
File Purpose: Define the TravelMind design tokens for Tailwind CSS
Owner: Jay
Dependencies: Tailwind CSS
Last Updated: 2026-03-13
*/
/** @type {import('tailwindcss').Config} */
export default {
  darkMode: "class",
  content: ["./index.html", "./src/**/*.{js,jsx}"],
  theme: {
    extend: {
      colors: {
        primary: "#00535b",
        "primary-container": "#006d77",
        surface: "#f8f9fa",
        "surface-container-low": "#f3f4f5",
        "surface-container-lowest": "#ffffff",
        tertiary: "#8c2500",
        "secondary-container": "#eee0d0",
        text: "#191c1d",
        "dark-base": "#0f1416",
        "dark-surface": "#131a1d",
        "dark-low": "#182125",
        "dark-card": "#1d282c",
        "dark-muted": "#8fa0a4"
      },
      fontFamily: {
        headline: ['"Playfair Display"', "serif"],
        body: ["Manrope", "sans-serif"]
      },
      borderRadius: {
        DEFAULT: "1rem",
        lg: "1.5rem",
        xl: "2rem",
        "2xl": "2.5rem",
        "3xl": "3rem"
      },
      boxShadow: {
        ambient: "0 30px 80px rgba(15, 23, 28, 0.08)",
        float: "0 20px 60px rgba(15, 23, 28, 0.12)"
      },
      backgroundImage: {
        "brand-gradient": "linear-gradient(135deg, #00535b 0%, #006d77 100%)"
      },
      letterSpacing: {
        label: "0.05em"
      }
    }
  },
  plugins: []
};
