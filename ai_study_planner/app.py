"""Flask entry point for the AI Study Planner."""

from datetime import date
from pathlib import Path

from flask import Flask, flash, redirect, render_template, request, session, url_for

from database import (
    create_plan,
    get_plan,
    get_tasks,
    init_db,
    mark_task_complete,
    rebalance_pending_tasks,
)
from planner import build_schedule, parse_topics


BASE_DIR = Path(__file__).resolve().parent
app = Flask(__name__)
app.config["SECRET_KEY"] = "change-this-development-key"
app.config["DATABASE"] = BASE_DIR / "study_planner.db"

init_db(app.config["DATABASE"])


@app.route("/")
def dashboard():
    """Show the current plan's next tasks, or guide a new user to the form."""
    plan_id = session.get("plan_id")
    if not plan_id:
        return render_template("dashboard.html", plan=None, tasks=[])

    plan = get_plan(app.config["DATABASE"], plan_id)
    tasks = get_tasks(app.config["DATABASE"], plan_id)
    if plan is None:
        session.pop("plan_id", None)
        return render_template("dashboard.html", plan=None, tasks=[])
    return render_template("dashboard.html", plan=plan, tasks=tasks)


@app.route("/plan", methods=["GET", "POST"])
def plan_form():
    """Collect workload details and generate a new plan."""
    if request.method == "POST":
        try:
            topic_names = request.form.getlist("topic_name")
            difficulties = request.form.getlist("difficulty")
            topics = parse_topics(topic_names, difficulties)
            days = int(request.form["days"])
            hours = float(request.form["hours"])
            exam_date = date.fromisoformat(request.form["exam_date"])
            if exam_date < date.today():
                raise ValueError("The exam date must be today or later.")
            if days < 1 or hours <= 0:
                raise ValueError("Days and study hours must be greater than zero.")
            schedule = build_schedule(topics, days, hours, date.today())
            plan_id = create_plan(
                app.config["DATABASE"], exam_date.isoformat(), days, hours, topics, schedule
            )
            session["plan_id"] = plan_id
            return redirect(url_for("schedule"))
        except (KeyError, ValueError) as error:
            flash(str(error), "error")

    return render_template("plan.html", today=date.today().isoformat())


@app.route("/schedule")
def schedule():
    """Display the full calendar-style schedule."""
    plan_id = session.get("plan_id")
    if not plan_id:
        return redirect(url_for("plan_form"))
    plan = get_plan(app.config["DATABASE"], plan_id)
    tasks = get_tasks(app.config["DATABASE"], plan_id)
    if plan is None:
        session.pop("plan_id", None)
        return redirect(url_for("plan_form"))
    return render_template("schedule.html", plan=plan, tasks=tasks)


@app.post("/update")
def update():
    """Mark a task complete and redistribute the remaining unfinished work."""
    plan_id = session.get("plan_id")
    task_id = request.form.get("task_id", type=int)
    if not plan_id or task_id is None:
        flash("That task could not be updated.", "error")
        return redirect(url_for("schedule"))

    completed = request.form.get("completed") == "on"
    mark_task_complete(app.config["DATABASE"], task_id, plan_id, completed)
    plan = get_plan(app.config["DATABASE"], plan_id)
    if plan:
        rebalance_pending_tasks(app.config["DATABASE"], plan, date.today())
    return redirect(request.referrer or url_for("schedule"))


if __name__ == "__main__":
    app.run(debug=True)
