def build_trip_extraction_prompt(user_input: str) -> str:
    return (
        "Extract the following travel fields from the user request as JSON: "
        "destination_city, duration_days, budget_total, preferences, traveler_type. "
        f"User request: {user_input}"
    )
