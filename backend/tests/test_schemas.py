from __future__ import annotations

import pytest
from pydantic import ValidationError

from backend.app.schemas import ExerciseCreateInput, WorkoutInput


def test_workout_input_valid():
    payload = WorkoutInput(exercise_id=1, weight=20, weight_unit="kg", reps=8, sets=3)
    assert payload.exercise_id == 1
    assert payload.weight == 20


def test_workout_input_invalid():
    with pytest.raises(ValidationError):
        WorkoutInput(exercise_id=0, weight=-1, weight_unit="kg", reps=0, sets=0)


def test_exercise_create_valid():
    payload = ExerciseCreateInput(name="Reverse", weight=10, weight_unit="kg", reps=10, sets=4)
    assert payload.name == "Reverse"


def test_exercise_create_invalid():
    with pytest.raises(ValidationError):
        ExerciseCreateInput(name="", weight=-5, weight_unit="kg", reps=0, sets=0)
