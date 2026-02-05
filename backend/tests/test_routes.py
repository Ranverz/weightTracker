from __future__ import annotations

from unittest.mock import Mock

from backend.app.services import exercises as exercises_service
from backend.app.services import workouts as workouts_service


def test_stats_page_renders(client, monkeypatch):
    monkeypatch.setattr(workouts_service, "list_stats", Mock(return_value=[]))
    res = client.get("/miniapp/stats")
    assert res.status_code == 200
    assert b"canvas" in res.data


def test_exercise_add_validation(client):
    res = client.post("/miniapp/day/1/add", data={"name": "", "weight": "-1", "reps": "0", "sets": "0"})
    assert res.status_code == 400


def test_exercise_create_flow(client, monkeypatch):
    monkeypatch.setattr(exercises_service, "create", Mock(return_value=1))
    res = client.post("/miniapp/day/1/add", data={"name": "Reverse", "weight": "10", "reps": "10", "sets": "3"})
    assert res.status_code == 302
