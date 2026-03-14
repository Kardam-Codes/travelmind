def optimize_itinerary_items(items: list) -> list:
    return sorted(items, key=lambda item: (item["day_number"], item["item_order"]))
