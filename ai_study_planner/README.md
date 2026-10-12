# AI Study Planner

A beginner-friendly Flask study planner that creates a weighted schedule from
your topics, difficulty levels, exam date, and daily study hours.

## Run locally

```powershell
cd ai_study_planner
..\.venv\Scripts\python.exe app.py
```

Then open <http://127.0.0.1:5000>.

The SQLite database is created automatically as `study_planner.db` the first
time the app starts. It stores the active plan and completion state between
sessions.

## Routes

- `/` — dashboard and upcoming tasks
- `/plan` — workload and exam-date form
- `/schedule` — calendar-style schedule
- `/update` — POST endpoint used to toggle completion and rebalance pending work

The scheduler gives hard topics three weight units, medium topics two, and easy
topics one. When a task is completed, unfinished tasks are redistributed across
the remaining plan days.