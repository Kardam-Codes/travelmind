import os

# -----------------------------
# Helper to create file
# -----------------------------
def create_file(path, header):
    directory = os.path.dirname(path)

    # Only create directory if it exists
    if directory != "":
        os.makedirs(directory, exist_ok=True)

    if not os.path.exists(path):
        with open(path, "w", encoding="utf-8") as f:
            f.write(header + "\n")


# -----------------------------
# File Header Template
# -----------------------------
def header(feature, purpose, owner, deps=""):
    return f"""\"\"\"
Feature: {feature}
File Purpose: {purpose}
Owner: {owner}
Dependencies: {deps}
Last Updated: Initial Setup
\"\"\""""


# -----------------------------
# Project Structure
# -----------------------------
structure = {

    # FRONTEND
    "frontend/src/features/trip-input/TripInput.jsx":
        header("Trip Input", "UI component to capture user travel request", "Kardam", "React"),

    "frontend/src/features/itinerary/ItineraryView.jsx":
        header("Itinerary", "Display generated itinerary", "Kardam", "React"),

    "frontend/src/features/wishlist/Wishlist.jsx":
        header("Wishlist", "Display and manage saved travel items", "Kardam", "React"),

    "frontend/src/features/collaboration/CollaborationPanel.jsx":
        header("Collaboration", "Real-time trip collaboration UI", "Kardam", "WebSockets"),

    "frontend/src/utils/apiClient.js":
        header("API Client", "Handles frontend API requests", "Kardam", "Fetch/Axios"),


    # BACKEND
    "backend/src/features/trip-planning/tripController.js":
        header("Trip Planning", "Handles trip generation requests", "Misha", "Express"),

    "backend/src/features/recommendation/recommendationService.js":
        header("Recommendation Engine", "Fetch recommendations from catalog data", "Misha", "Database"),

    "backend/src/features/wishlist/wishlistController.js":
        header("Wishlist", "API for wishlist operations", "Misha", "Express"),

    "backend/src/features/collaboration/collaborationController.js":
        header("Collaboration", "Handles real-time trip collaboration", "Misha", "WebSockets"),

    "backend/src/database/db.js":
        header("Database", "Database connection and configuration", "Misha", "PostgreSQL"),


    # AI SERVICE
    "ai-service/app/features/intent-extraction/intent_parser.py":
        header("Intent Extraction", "Extract travel parameters from user input", "Yug", "LLM API"),

    "ai-service/app/features/itinerary-generator/itinerary_generator.py":
        header("Itinerary Generator", "Generate day-by-day itinerary", "Yug", "Python"),

    "ai-service/app/features/recommendation-engine/recommendation_engine.py":
        header("Recommendation Engine", "Filter travel catalog data", "Yug", "Python"),

    "ai-service/app/prompts/trip_prompt.txt":
        header("Prompt", "Prompt template for LLM travel parsing", "Yug", "LLM"),

    "ai-service/app/main.py":
        header("FastAPI Server", "Main AI API service", "Yug", "FastAPI"),


    # DOCUMENTATION
    "docs/architecture.md":
        header("Architecture", "System architecture documentation", "Jay"),

    "docs/api-spec.md":
        header("API Specification", "API contract for frontend-backend-AI", "Jay"),

    "docs/pitch-notes.md":
        header("Pitch", "Notes for hackathon presentation", "Jay"),


    # DATASETS
    "datasets/README.md":
        header("Dataset", "Travel catalog dataset description", "Jay"),


    # ROOT FILES
    "INSTRUCTION.md":
        header("Project Rules", "Team collaboration and architecture rules", "Kardam"),

    "README.md":
        header("Project Overview", "Project description and setup guide", "Kardam")
}

# -----------------------------
# Create Structure
# -----------------------------
for path, head in structure.items():
    create_file(path, head)

print("✅ Project structure created successfully.")