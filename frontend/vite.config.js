/*
Feature: Frontend Infrastructure
File Purpose: Configure the Vite frontend build
Owner: Jay
Dependencies: Vite, @vitejs/plugin-react
Last Updated: 2026-03-13
*/
import { defineConfig } from "vite";
import react from "@vitejs/plugin-react";

export default defineConfig({
  plugins: [react()],
  server: {
    port: 5173,
  },
});
