# SceneSpark Mini Movie Maker

SceneSpark is a beginner-friendly Flask web application for creating short film scripts and storyboards. It uses simple rule-based story templates and local JSON files, so it needs no paid AI service, API key, or external backend.

## Features

- Movie title, genre, mood, setting, length, and character inputs
- Rule-based script generation
- Logline and four-scene storyboard
- Visual, action, and dialogue notes for every scene
- Save up to 20 projects locally
- Load saved project history
- Delete saved projects
- Responsive HTML and CSS interface

This application creates written scripts and storyboards only. It does not create or export actual video files.

## Project structure

```text
mini_movie/
├── app.py
├── movie_generator.py
├── movie_data.json
├── saved_movies.json
├── requirements.txt
├── README.md
├── .gitignore
├── templates/
│   └── index.html
└── static/
    ├── style.css
    └── script.js
```

## Run locally

Open PowerShell in this folder:

```powershell
cd "C:\Users\Apeksha\OneDrive\Desktop\agentic_ai\mini_movie"
python -m venv venv
.\venv\Scripts\Activate.ps1
python -m pip install -r requirements.txt
python app.py
```

If you already have the shared project environment:

```powershell
& "C:\Users\Apeksha\OneDrive\Desktop\agentic_ai\.venv\Scripts\python.exe" app.py
```

Open <http://127.0.0.1:5000>.

## How it works

1. The browser loads available choices from `/api/options`.
2. The form sends choices to `/api/generate` using `fetch()`.
3. `movie_generator.py` combines local story fragments based on genre and mood.
4. Flask returns a logline, formatted script, and storyboard.
5. Saving sends the project to `/api/movies`.
6. `saved_movies.json` stores projects safely through a temporary file.

## Customizing stories

Edit `movie_data.json` to add genres, moods, settings, or story templates. Each story template provides an inciting event, goal, obstacle, action, turning line, ending, and final line.

## GitHub

The project is ready for Git, but no commit or push is performed automatically:

```powershell
git init
git add .
git commit -m "Create SceneSpark mini movie maker"
```
