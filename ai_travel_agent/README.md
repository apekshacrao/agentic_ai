# WanderWise Travel Agent

WanderWise is a beginner-friendly travel-planning web application. It uses a small rule-based Python agent to compare complete vacation options and create activity itineraries from local JSON data. It does not need a paid AI API or an API key.

## Features

- Homepage search for destination, travellers, budget, and duration
- Multiple destination cards with images, summaries, highlights, and estimated totals
- Calendar-style, day-by-day itinerary with morning, afternoon, and evening plans
- Accommodation, transportation, and local food suggestions
- Estimated costs for stay, travel, food, and activities
- Booking/contact enquiry form
- Persistent memory of the ten most recent plans
- Separate Flask backend and HTML/CSS/JavaScript frontend
- JSON files that are easy to edit for a college demonstration

## Project structure

```text
ai_travel_agent/
├── app.py
├── travel_agent.py
├── places.json
├── travel_memory.json
├── requirements.txt
├── README.md
├── .gitignore
├── templates/
│   ├── index.html
│   ├── results.html
│   ├── itinerary.html
│   └── booking.html
└── static/
    ├── script.js
    └── style.css
```

## Run locally

1. Open PowerShell in this folder.
2. Create a virtual environment:

   ```powershell
   python -m venv venv
   ```

3. Activate it:

   ```powershell
   .\venv\Scripts\Activate.ps1
   ```

   If PowerShell prevents activation, use the direct interpreter command shown below instead.

4. Install the only dependency:

   ```powershell
   python -m pip install -r requirements.txt
   ```

5. Start the server:

   ```powershell
   python app.py
   ```

6. Open <http://127.0.0.1:5000> in a browser.

Direct command without activation:

```powershell
& ".\venv\Scripts\python.exe" ".\app.py"
```

## How the rule-based agent works

`travel_agent.py`:

1. Reads destination profiles from `places.json`.
2. Validates the submitted traveller count, budget, and trip duration.
3. Compares every destination against the requested budget.
4. Estimates stay, travel, food, and activity costs.
5. Builds a balanced day-by-day itinerary.
6. Saves the result to `travel_memory.json`.

## Routes

- `/` — homepage search form
- `/results` — multiple destination options
- `/itinerary` — detailed vacation plan and cost breakdown
- `/booking` — booking/contact enquiry form
- `/api/destinations` — destination names as JSON
- `/api/plan` — create a plan using a JSON POST request

The planner stores at most ten recent plans. The memory file is created and updated safely using a temporary file before replacement.

## Customizing travel data

Edit `places.json` and add a destination with attractions in this format:

```json
{
  "name": "Example Museum",
  "cost": 40,
  "open": true,
  "category": "history"
}
```

Supported categories in the starter UI are `nature`, `history`, and `adventure`.

## GitHub

This project is ready to initialize as a Git repository, but it is not automatically committed or pushed:

```powershell
git init
git add .
git commit -m "Create rule-based travel agent"
```
