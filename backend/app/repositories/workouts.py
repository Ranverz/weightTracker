from __future__ import annotations

from typing import Any, Dict, List

from backend.app.db import get_conn


def create_entry(
    user_id: int,
    exercise_id: int,
    weight: float,
    weight_unit: str,
    reps: int,
    sets: int,
) -> None:
    """Insert a single workout entry."""
    with get_conn() as conn:
        cur = conn.cursor()
        cur.execute(
            """
            INSERT INTO workouts (user_id, exercise_id, weight, weight_unit, reps, sets)
            VALUES (%s, %s, %s, %s, %s, %s)
            """,
            (user_id, exercise_id, weight, weight_unit, reps, sets),
        )
        conn.commit()


def list_recent(user_id: int, exercise_id: int, limit: int = 10) -> List[Dict[str, Any]]:
    """Return recent workouts for an exercise, scoped to user."""
    with get_conn() as conn:
        cur = conn.cursor()
        cur.execute(
            """
            SELECT weight, weight_unit, reps, sets, created_at
            FROM workouts
            WHERE exercise_id = %s AND user_id = %s
            ORDER BY created_at DESC
            LIMIT %s
            """,
            (exercise_id, user_id, limit),
        )
        return [
            {
                "weight": r[0],
                "weight_unit": r[1],
                "reps": r[2],
                "sets": r[3],
                "created_at": r[4],
            }
            for r in cur.fetchall()
        ]


def list_stats(user_id: int) -> List[Dict[str, Any]]:
    """Return time-series stats for charts."""
    with get_conn() as conn:
        cur = conn.cursor()
        cur.execute(
            """
            SELECT w.created_at, e.name, w.weight, w.weight_unit
            FROM workouts w
            JOIN exercises e ON e.id = w.exercise_id
            WHERE w.user_id = %s
            ORDER BY w.created_at ASC
            """,
            (user_id,),
        )
        return [
            {
                "datetime": r[0].strftime("%Y-%m-%d %H:%M"),
                "exercise": r[1],
                "weight": float(r[2]),
                "unit": r[3],
            }
            for r in cur.fetchall()
        ]
