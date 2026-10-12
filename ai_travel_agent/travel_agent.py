import json
from datetime import datetime
from pathlib import Path


BASE_DIR = Path(__file__).resolve().parent
PLACES_FILE = BASE_DIR / "places.json"
MEMORY_FILE = BASE_DIR / "travel_memory.json"


def load_places():
    with PLACES_FILE.open("r", encoding="utf-8") as file:
        return json.load(file)


def load_memory():
    if not MEMORY_FILE.exists():
        return []
    try:
        with MEMORY_FILE.open("r", encoding="utf-8") as file:
            data = json.load(file)
    except (OSError, json.JSONDecodeError):
        return []
    return data if isinstance(data, list) else []


def save_memory(memory):
    temporary_file = MEMORY_FILE.with_suffix(".tmp")
    with temporary_file.open("w", encoding="utf-8") as file:
        json.dump(memory, file, indent=2)
    temporary_file.replace(MEMORY_FILE)


class TravelAgent:
    """An explainable travel planner using local destination and activity data."""

    def __init__(self, places):
        self.places = places
        self.memory = load_memory()

    def destinations(self):
        return sorted(self.places)

    def destination_options(self, details):
        people = self._positive_integer(details.get("people", 1), "Number of people")
        days = self._positive_integer(details.get("days", 3), "Trip duration")
        budget = self._positive_number(details.get("budget"), "Budget")
        requested = str(details.get("destination", "")).strip().lower()
        candidates = [
            destination
            for name, destination in self.places.items()
            if not requested or requested in name.lower()
        ]
        if not candidates:
            raise ValueError("No destination matches your search.")

        options = []
        for destination in candidates:
            estimate = self._estimate_cost(destination, people, days)
            options.append(
                {
                    "name": destination["name"],
                    "summary": destination["summary"],
                    "image": destination["image"],
                    "highlights": destination["highlights"],
                    "best_for": destination["best_for"],
                    "estimated_total": estimate["total"],
                    "within_budget": estimate["total"] <= budget,
                    "costs": estimate,
                }
            )
        return options

    def create_plan(self, details):
        destination_name = str(details.get("destination", "")).strip()
        if destination_name not in self.places:
            raise ValueError("Please choose one of the available destinations.")

        people = self._positive_integer(details.get("people", 1), "Number of people")
        days = self._positive_integer(details.get("days"), "Trip duration")
        budget = self._positive_number(details.get("budget"), "Budget")
        destination = self.places[destination_name]
        estimate = self._estimate_cost(destination, people, days)
        if estimate["total"] > budget:
            raise ValueError(
                f"This plan is estimated at INR {estimate['total']:,}. "
                "Increase your budget or choose another destination."
            )

        activities = destination["activities"]
        itinerary = []
        for day in range(days):
            activity = activities[day % len(activities)]
            itinerary.append(
                {
                    "day": day + 1,
                    "theme": ["Arrival & explore", "Sightseeing", "Local life", "Relaxation"][
                        day % 4
                    ],
                    "morning": activity["morning"],
                    "afternoon": activity["afternoon"],
                    "evening": activity["evening"],
                    "activity_cost": activity["cost"] * people,
                }
            )

        plan = {
            "destination": destination_name,
            "summary": destination["summary"],
            "image": destination["image"],
            "people": people,
            "days": days,
            "budget": budget,
            "costs": estimate,
            "itinerary": itinerary,
            "accommodation": destination["accommodation"],
            "transport": destination["transport"],
            "food": destination["food"],
            "tip": self._tip(estimate["total"], budget),
        }
        self._remember(plan)
        return plan

    def _estimate_cost(self, destination, people, days=3):
        stay = destination["accommodation"][0]["nightly"] * max(days - 1, 1)
        travel = destination["transport"]["round_trip"] * people
        food = destination["food"]["daily"] * people * days
        activities = sum(
            item["cost"] for item in destination["activities"][: min(days, 4)]
        ) * people
        total = stay + travel + food + activities
        return {
            "stay": stay,
            "travel": travel,
            "food": food,
            "activities": activities,
            "total": total,
        }

    @staticmethod
    def _positive_number(value, label):
        try:
            number = float(value)
        except (TypeError, ValueError):
            raise ValueError(f"{label} must be a number.") from None
        if number <= 0:
            raise ValueError(f"{label} must be greater than zero.")
        return round(number, 2)

    @staticmethod
    def _positive_integer(value, label):
        try:
            number = int(value)
        except (TypeError, ValueError):
            raise ValueError(f"{label} must be a whole number.") from None
        if number <= 0:
            raise ValueError(f"{label} must be greater than zero.")
        return number

    @staticmethod
    def _tip(total, budget):
        remaining = budget - total
        if remaining > budget * 0.2:
            return "This plan leaves a healthy buffer for shopping and unexpected travel costs."
        return "This plan is close to budget, so book early and keep a small emergency buffer."

    def _remember(self, plan):
        saved_plan = dict(plan)
        saved_plan["created_at"] = datetime.now().isoformat(timespec="seconds")
        self.memory.insert(0, saved_plan)
        self.memory = self.memory[:10]
        save_memory(self.memory)
