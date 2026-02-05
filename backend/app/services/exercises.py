from __future__ import annotations

from typing import Any, Dict, List

from backend.app.repositories import exercises as exercises_repo


def list_day(user_id: int, day: int) -> List[Dict[str, Any]]:
    """List exercises for a given day."""
    return exercises_repo.list_by_day(user_id=user_id, day=day)


def get(user_id: int, ex_id: int) -> Dict[str, Any] | None:
    """Return exercise if it belongs to the user."""
    return exercises_repo.get_by_id(user_id=user_id, ex_id=ex_id)


def create(
    user_id: int,
    day: int,
    name: str,
    weight: float,
    weight_unit: str,
    reps: int,
    sets: int,
) -> int:
    """Create an exercise and its first workout entry."""
    return exercises_repo.create_with_first_workout(
        user_id=user_id,
        day=day,
        name=name,
        weight=weight,
        weight_unit=weight_unit,
        reps=reps,
        sets=sets,
    )


def update(user_id: int, ex_id: int, name: str, default_unit: str) -> bool:
    """Update exercise metadata."""
    return exercises_repo.update_exercise(
        user_id=user_id,
        ex_id=ex_id,
        name=name,
        default_unit=default_unit,
    )


def delete(user_id: int, ex_id: int) -> bool:
    """Delete exercise and related workouts."""
    return exercises_repo.delete_exercise(user_id=user_id, ex_id=ex_id)
