from __future__ import annotations

from typing import Literal

from pydantic import BaseModel, Field


class WorkoutInput(BaseModel):
    """Validated payload for a workout entry."""

    exercise_id: int = Field(..., gt=0)
    weight: float = Field(..., ge=0)
    weight_unit: Literal["kg", "plates"]
    reps: int = Field(..., ge=1)
    sets: int = Field(..., ge=1)


class ExerciseCreateInput(BaseModel):
    """Validated payload for creating an exercise + first workout."""

    name: str = Field(..., min_length=1, max_length=120)
    weight: float = Field(..., ge=0)
    weight_unit: Literal["kg", "plates"]
    reps: int = Field(..., ge=1)
    sets: int = Field(..., ge=1)


class ExerciseUpdateInput(BaseModel):
    """Validated payload for updating an exercise."""

    name: str = Field(..., min_length=1, max_length=120)
    default_unit: Literal["kg", "plates"]
