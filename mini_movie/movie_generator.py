import json
import uuid
from datetime import datetime
from pathlib import Path


BASE_DIR = Path(__file__).resolve().parent
DATA_FILE = BASE_DIR / "movie_data.json"
SAVED_FILE = BASE_DIR / "saved_movies.json"


def load_movie_data():
    with DATA_FILE.open("r", encoding="utf-8") as file:
        return json.load(file)


def read_saved_movies():
    if not SAVED_FILE.exists():
        return []
    try:
        with SAVED_FILE.open("r", encoding="utf-8") as file:
            data = json.load(file)
    except (OSError, json.JSONDecodeError):
        return []
    return data if isinstance(data, list) else []


def write_saved_movies(movies):
    temporary_file = SAVED_FILE.with_suffix(".tmp")
    with temporary_file.open("w", encoding="utf-8") as file:
        json.dump(movies, file, indent=2)
    temporary_file.replace(SAVED_FILE)


class MovieGenerator:
    """Creates short scripts from simple, explainable local story rules."""

    def __init__(self, data):
        self.data = data
        self.saved_movies = read_saved_movies()

    def options(self):
        return {
            "genres": self.data["genres"],
            "moods": self.data["moods"],
            "settings": self.data["settings"],
            "lengths": self.data["lengths"],
        }

    def generate(self, details):
        title = str(details.get("title", "")).strip()
        genre = str(details.get("genre", "")).strip().lower()
        mood = str(details.get("mood", "")).strip().lower()
        setting = str(details.get("setting", "")).strip().lower()
        characters = str(details.get("characters", "")).strip()
        length = str(details.get("length", "short")).strip().lower()

        if not title:
            raise ValueError("Please give your movie a title.")
        if genre not in self.data["genres"]:
            raise ValueError("Please choose a valid genre.")
        if mood not in self.data["moods"]:
            raise ValueError("Please choose a valid mood.")
        if setting not in self.data["settings"]:
            raise ValueError("Please choose a valid setting.")
        if length not in self.data["lengths"]:
            raise ValueError("Please choose a valid movie length.")

        names = [name.strip() for name in characters.split(",") if name.strip()]
        if not names:
            names = ["Alex", "Sam"]
        genre_stories = self.data["stories"][genre]
        story = genre_stories.get(mood) or next(iter(genre_stories.values()))
        location = self.data["settings"][setting]
        duration = self.data["lengths"][length]["minutes"]
        scenes = self._scenes(names, story, location, duration)

        return {
            "id": uuid.uuid4().hex,
            "title": title,
            "genre": genre.title(),
            "mood": mood.title(),
            "setting": location["name"],
            "characters": names,
            "length": self.data["lengths"][length]["label"],
            "logline": f"When {story['inciting']}, {names[0]} must {story['goal']} before time runs out.",
            "script": self._script(title, names, story, location, scenes),
            "scenes": scenes,
            "created_at": datetime.now().isoformat(timespec="seconds"),
        }

    def save(self, project):
        if not project.get("title") or not project.get("scenes"):
            raise ValueError("Generate a movie before saving it.")
        saved = dict(project)
        saved["id"] = saved.get("id") or uuid.uuid4().hex
        saved["saved_at"] = datetime.now().isoformat(timespec="seconds")
        self.saved_movies = [movie for movie in self.saved_movies if movie["id"] != saved["id"]]
        self.saved_movies.insert(0, saved)
        self.saved_movies = self.saved_movies[:20]
        write_saved_movies(self.saved_movies)
        return saved

    def delete(self, movie_id):
        original_count = len(self.saved_movies)
        self.saved_movies = [movie for movie in self.saved_movies if movie["id"] != movie_id]
        if len(self.saved_movies) == original_count:
            return False
        write_saved_movies(self.saved_movies)
        return True

    @staticmethod
    def _scenes(names, story, location, duration):
        lead = names[0]
        friend = names[1] if len(names) > 1 else "a mysterious stranger"
        return [
            {"number": 1, "title": "The ordinary moment", "time": "0:00–1:00", "visual": f"{location['visual']} at dawn.", "action": f"{lead} notices a clue that changes an ordinary day.", "dialogue": f'{lead}: "{story["opening"]}"'},
            {"number": 2, "title": "The impossible choice", "time": "1:00–2:00", "visual": f"Close-ups of {lead} and {friend} as the world grows quieter.", "action": f"{lead} discovers the real challenge: {story['obstacle']}", "dialogue": f'{friend}: "You still have a choice."'},
            {"number": 3, "title": "The brave step", "time": "2:00–3:00", "visual": f"Movement through {location['name']}; light and shadow mirror the decision.", "action": f"{lead} {story['action']} and faces the consequence.", "dialogue": f'{lead}: "{story["turn"]}"'},
            {"number": 4, "title": "A new beginning", "time": f"{max(duration - 1, 3)}:00–{duration}:00", "visual": "A wide final shot holds on the changed world.", "action": story["ending"], "dialogue": f'{lead}: "{story["final_line"]}"'},
        ]

    @staticmethod
    def _script(title, names, story, location, scenes):
        lines = [f"TITLE: {title.upper()}", f"SETTING: {location['name']}", f"CHARACTERS: {', '.join(names)}", "", f"LOGLINE: When {story['inciting']}, {names[0]} must {story['goal']} before time runs out.", ""]
        for scene in scenes:
            lines.extend([f"SCENE {scene['number']}: {scene['title'].upper()} ({scene['time']})", f"VISUAL: {scene['visual']}", f"ACTION: {scene['action']}", f"DIALOGUE: {scene['dialogue']}", ""])
        return "\n".join(lines)
