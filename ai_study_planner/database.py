"""SQLite persistence for plans and task completion state."""

import sqlite3
from contextlib import contextmanager
from pathlib import Path

from planner import build_schedule


@contextmanager
def connect(path: Path):
    """Open and reliably close a SQLite connection, including on Windows."""
    connection = sqlite3.connect(path)
    connection.row_factory = sqlite3.Row
    try:
        yield connection
        connection.commit()
    finally:
        connection.close()


def init_db(path: Path) -> None:
    with connect(path) as db:
        db.executescript(
            """
            CREATE TABLE IF NOT EXISTS plans (
                id INTEGER PRIMARY KEY AUTOINCREMENT,
                exam_date TEXT NOT NULL,
                days INTEGER NOT NULL,
                daily_hours REAL NOT NULL,
                topics TEXT NOT NULL
            );
            CREATE TABLE IF NOT EXISTS tasks (
                id INTEGER PRIMARY KEY AUTOINCREMENT,
                plan_id INTEGER NOT NULL REFERENCES plans(id) ON DELETE CASCADE,
                task_date TEXT NOT NULL,
                topic TEXT NOT NULL,
                difficulty TEXT NOT NULL,
                hours REAL NOT NULL,
                completed INTEGER NOT NULL DEFAULT 0
            );
            """
        )


def create_plan(path, exam_date, days, daily_hours, topics, schedule) -> int:
    import json

    with connect(path) as db:
        cursor = db.execute(
            "INSERT INTO plans (exam_date, days, daily_hours, topics) VALUES (?, ?, ?, ?)",
            (exam_date, days, daily_hours, json.dumps(topics)),
        )
        plan_id = cursor.lastrowid
        db.executemany(
            """INSERT INTO tasks
            (plan_id, task_date, topic, difficulty, hours)
            VALUES (?, ?, ?, ?, ?)""",
            [(plan_id, item["date"], item["topic"], item["difficulty"], item["hours"]) for item in schedule],
        )
        return plan_id


def get_plan(path, plan_id):
    import json

    with connect(path) as db:
        row = db.execute("SELECT * FROM plans WHERE id = ?", (plan_id,)).fetchone()
    if row is None:
        return None
    plan = dict(row)
    plan["topics"] = json.loads(plan["topics"])
    return plan


def get_tasks(path, plan_id):
    with connect(path) as db:
        return [dict(row) for row in db.execute(
            "SELECT * FROM tasks WHERE plan_id = ? ORDER BY task_date, id", (plan_id,)
        )]


def mark_task_complete(path, task_id, plan_id, completed):
    with connect(path) as db:
        db.execute(
            "UPDATE tasks SET completed = ? WHERE id = ? AND plan_id = ?",
            (int(completed), task_id, plan_id),
        )


def rebalance_pending_tasks(path, plan, start_date):
    """Move unfinished tasks into the remaining days after a completion change."""
    topics = plan["topics"]
    pending = []
    with connect(path) as db:
        rows = db.execute(
            "SELECT * FROM tasks WHERE plan_id = ? AND completed = 0 ORDER BY id",
            (plan["id"],),
        ).fetchall()
        pending = [dict(row) for row in rows]
        if not pending:
            return
        remaining_days = max(1, plan["days"])
        new_schedule = build_schedule(
            topics, remaining_days, plan["daily_hours"], start_date
        )
        for old_task, new_task in zip(pending, new_schedule):
            db.execute(
                "UPDATE tasks SET task_date = ?, topic = ?, difficulty = ?, hours = ? WHERE id = ?",
                (new_task["date"], new_task["topic"], new_task["difficulty"], new_task["hours"], old_task["id"]),
            )
        for old_task in pending[len(new_schedule) :]:
            db.execute("DELETE FROM tasks WHERE id = ?", (old_task["id"],))
