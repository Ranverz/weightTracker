from __future__ import annotations

from typing import Any, Dict, List

from backend.app.repositories import workouts as workouts_repo


def create(
    user_id: int,
    exercise_id: int,
    weight: float,
    weight_unit: str,
    reps: int,
    sets: int,
) -> None:
    """Create a workout entry."""
    workouts_repo.create_entry(
        user_id=user_id,
        exercise_id=exercise_id,
        weight=weight,
        weight_unit=weight_unit,
        reps=reps,
        sets=sets,
    )


def list_recent(user_id: int, exercise_id: int, limit: int = 10) -> List[Dict[str, Any]]:
    """Fetch recent workouts for an exercise."""
    return workouts_repo.list_recent(user_id=user_id, exercise_id=exercise_id, limit=limit)


def list_stats(user_id: int) -> List[Dict[str, Any]]:
    """Fetch workout stats for charts."""
    return workouts_repo.list_stats(user_id=user_id)
