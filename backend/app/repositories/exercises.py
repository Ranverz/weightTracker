from __future__ import annotations

from typing import Any, Dict, List

from backend.app.db import get_conn


def list_by_day(user_id: int, day: int) -> List[Dict[str, Any]]:
    """Return exercises for a day with last workout and max weight."""
    with get_conn() as conn:
        cur = conn.cursor()
        cur.execute(
            """
            SELECT
                e.id,
                e.name,
                e.default_unit,
                lw.weight,
                lw.weight_unit,
                lw.reps,
                lw.sets,
                lw.created_at,
                mx.max_weight,
                mx.max_unit,
                mc.max_combo_weight,
                mc.max_combo_reps,
                mc.max_combo_value,
                mc.max_combo_unit
            FROM exercises e
            LEFT JOIN LATERAL (
                SELECT w.weight, w.weight_unit, w.reps, w.sets, w.created_at
                FROM workouts w
                WHERE w.exercise_id = e.id AND w.user_id = %s
                ORDER BY w.created_at DESC
                LIMIT 1
            ) lw ON true
            LEFT JOIN LATERAL (
                SELECT MAX(w.weight) AS max_weight, w.weight_unit AS max_unit
                FROM workouts w
                WHERE w.exercise_id = e.id AND w.user_id = %s
                  AND (lw.weight_unit IS NULL OR w.weight_unit = lw.weight_unit)
                GROUP BY w.weight_unit
                ORDER BY w.weight_unit
                LIMIT 1
            ) mx ON true
            LEFT JOIN LATERAL (
                SELECT
                    w.weight AS max_combo_weight,
                    w.reps AS max_combo_reps,
                    (w.weight * w.reps) AS max_combo_value,
                    w.weight_unit AS max_combo_unit
                FROM workouts w
                WHERE w.exercise_id = e.id AND w.user_id = %s
                  AND (lw.weight_unit IS NULL OR w.weight_unit = lw.weight_unit)
                ORDER BY (w.weight * w.reps) DESC, w.created_at DESC
                LIMIT 1
            ) mc ON true
            WHERE e.day_of_week = %s AND e.user_id = %s
            ORDER BY e.id
            """,
            (user_id, user_id, user_id, day, user_id),
        )

        return [
            {
                "id": row[0],
                "name": row[1],
                "default_unit": row[2],
                "last_weight": row[3],
                "last_unit": row[4],
                "last_reps": row[5],
                "last_sets": row[6],
                "last_date": row[7],
                "max_weight": row[8],
                "max_unit": row[9],
                "max_combo_weight": row[10],
                "max_combo_reps": row[11],
                "max_combo_value": row[12],
                "max_combo_unit": row[13],
            }
            for row in cur.fetchall()
        ]


def get_by_id(user_id: int, ex_id: int) -> Dict[str, Any] | None:
    """Fetch a single exercise by id, scoped to user."""
    with get_conn() as conn:
        cur = conn.cursor()
        cur.execute(
            "SELECT id, name, day_of_week, default_unit FROM exercises WHERE id = %s AND user_id = %s",
            (ex_id, user_id),
        )
        row = cur.fetchone()
        if not row:
            return None
        return {"id": row[0], "name": row[1], "day": row[2], "default_unit": row[3]}


def create_with_first_workout(
    user_id: int,
    day: int,
    name: str,
    weight: float,
    weight_unit: str,
    reps: int,
    sets: int,
) -> int:
    """Create an exercise and its first workout entry."""
    with get_conn() as conn:
        cur = conn.cursor()
        cur.execute(
            """
            INSERT INTO exercises (user_id, name, day_of_week, default_unit, default_weight, default_reps, default_sets)
            VALUES (%s, %s, %s, %s, %s, %s, %s)
            RETURNING id
            """,
            (user_id, name, day, weight_unit, weight, reps, sets),
        )
        ex_id = cur.fetchone()[0]
        cur.execute(
            """
            INSERT INTO workouts (user_id, exercise_id, weight, weight_unit, reps, sets)
            VALUES (%s, %s, %s, %s, %s, %s)
            """,
            (user_id, ex_id, weight, weight_unit, reps, sets),
        )
        conn.commit()
        return ex_id


def update_exercise(user_id: int, ex_id: int, name: str, default_unit: str) -> bool:
    """Update exercise name and default unit."""
    with get_conn() as conn:
        cur = conn.cursor()
        cur.execute(
            """
            UPDATE exercises
            SET name = %s, default_unit = %s
            WHERE id = %s AND user_id = %s
            """,
            (name, default_unit, ex_id, user_id),
        )
        conn.commit()
        return cur.rowcount > 0


def delete_exercise(user_id: int, ex_id: int) -> bool:
    """Delete exercise and its workouts."""
    with get_conn() as conn:
        cur = conn.cursor()
        cur.execute(
            "DELETE FROM workouts WHERE exercise_id = %s AND user_id = %s",
            (ex_id, user_id),
        )
        cur.execute(
            "DELETE FROM exercises WHERE id = %s AND user_id = %s",
            (ex_id, user_id),
        )
        conn.commit()
        return cur.rowcount > 0
