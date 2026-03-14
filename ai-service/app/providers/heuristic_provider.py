import json
import re

from providers.base import LLMProvider


class HeuristicProvider(LLMProvider):
    provider_name = "heuristic-fallback"

    def generate_json(self, prompt: str) -> str:
        user_query_match = re.search(r'(?:User Query|Query):\s*"(.+?)"', prompt, re.DOTALL | re.IGNORECASE)
        city_match = re.search(r"Supported cities:\s*(.+?)\nAllowed preference tags:", prompt, re.DOTALL | re.IGNORECASE)
        tags_match = re.search(r"Allowed preference tags:\s*(.+?)\nAllowed traveler types:", prompt, re.DOTALL | re.IGNORECASE)
        traveler_types_match = re.search(r"Allowed traveler types:\s*(.+?)\nReturn this exact key set:", prompt, re.DOTALL | re.IGNORECASE)

        user_query = user_query_match.group(1) if user_query_match else prompt
        normalized_query = user_query.strip().lower()
        supported_cities = [city.strip() for city in city_match.group(1).split(",")] if city_match else []
        allowed_tags = [tag.strip() for tag in tags_match.group(1).split(",")] if tags_match else []
        allowed_travelers = [traveler.strip() for traveler in traveler_types_match.group(1).split(",")] if traveler_types_match else []

        destination_city = next((city for city in supported_cities if city.lower() in normalized_query), None)
        unsupported_city = None if destination_city else _extract_unknown_city_name(user_query)
        duration_match = re.search(r"(\d+)\s*(day|days|night|nights)", normalized_query)
        budget_match = re.search(r"(?:under|below|budget|within)\s*(?:rs\.?|inr)?\s*([\d,]+(?:\.\d+)?)\s*([kK]?)", normalized_query)
        duration_days = int(duration_match.group(1)) if duration_match else None

        budget_total = None
        if budget_match:
            budget_total = float(budget_match.group(1).replace(",", ""))
            if budget_match.group(2):
                budget_total *= 1000

        preferences = [tag for tag in allowed_tags if tag in normalized_query]
        traveler_type = next((traveler for traveler in allowed_travelers if traveler in normalized_query), None)

        missing_fields = []
        if not destination_city:
            missing_fields.append("destination_city")
        if duration_days is None:
            missing_fields.append("duration_days")

        return json.dumps(
            {
                "destination_city": destination_city,
                "unsupported_city": unsupported_city,
                "duration_days": duration_days,
                "budget_total": budget_total,
                "budget_level": _infer_budget_level(budget_total),
                "preferences": preferences,
                "traveler_type": traveler_type,
                "confidence": 0.82 if not missing_fields else 0.3,
                "missing_fields": missing_fields,
                "raw_reasoning_summary": "Fallback extraction based on supported cities and known keywords.",
                "normalized_query": user_query.strip(),
            }
        )


def _extract_unknown_city_name(query: str) -> str | None:
    patterns = [
        r"\btrip\s+(?:to|for)\s+([A-Za-z][A-Za-z\s]+?)(?:\s+for\s+\d+\s*(?:day|days|night|nights)|\s+under|\s+with|\s+within|$)",
        r"\bvisit\s+([A-Za-z][A-Za-z\s]+?)(?:\s+for\s+\d+\s*(?:day|days|night|nights)|\s+under|\s+with|\s+within|$)",
    ]
    for pattern in patterns:
        match = re.search(pattern, query, re.IGNORECASE)
        if match:
            return match.group(1).strip().title()
    return None


def _infer_budget_level(budget_total: float | None) -> str | None:
    if budget_total is None:
        return None
    if budget_total < 15000:
        return "low"
    if budget_total < 35000:
        return "moderate"
    return "high"
