"""Small, deterministic scheduling helpers used by the Flask routes."""

from datetime import date, timedelta


DIFFICULTY_WEIGHT = {"Easy": 1, "Medium": 2, "Hard": 3}


def parse_topics(names: list[str], difficulties: list[str]) -> list[dict]:
    """Validate repeated topic form fields and return normalized topic records."""
    topics = []
    for name, difficulty in zip(names, difficulties):
        name = name.strip()
        if not name:
            continue
        if difficulty not in DIFFICULTY_WEIGHT:
            raise ValueError("Choose Easy, Medium, or Hard for every topic.")
        topics.append({"name": name, "difficulty": difficulty, "weight": DIFFICULTY_WEIGHT[difficulty]})
    if not topics:
        raise ValueError("Add at least one chapter or topic.")
    return topics


def build_schedule(topics: list[dict], days: int, daily_hours: float, start: date) -> list[dict]:
    """Allocate more study time to harder topics, while filling each day."""
    total_hours = days * daily_hours
    total_weight = sum(topic["weight"] for topic in topics)
    remaining = {
        topic["name"]: total_hours * topic["weight"] / total_weight for topic in topics
    }
    schedule = []
    for day_number in range(days):
        study_date = start + timedelta(days=day_number)
        available = daily_hours
        # Rotate the first topic so the same subject is not always first.
        ordered = topics[day_number % len(topics) :] + topics[: day_number % len(topics)]
        for topic in ordered:
            if available < 0.25 or remaining[topic["name"]] <= 0:
                continue
            duration = min(remaining[topic["name"]], available)
            duration = round(duration, 2)
            if duration < 0.25:
                continue
            schedule.append(
                {
                    "date": study_date.isoformat(),
                    "topic": topic["name"],
                    "difficulty": topic["difficulty"],
                    "hours": duration,
                }
            )
            remaining[topic["name"]] = round(remaining[topic["name"]] - duration, 2)
            available = round(available - duration, 2)
    return schedule
