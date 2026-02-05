from __future__ import annotations

from flask import Blueprint, current_app, make_response, redirect, render_template, request
from pydantic import ValidationError

from backend.app.schemas import ExerciseCreateInput, ExerciseUpdateInput, WorkoutInput
from backend.app.services import exercises as exercises_service
from backend.app.services import workouts as workouts_service
from backend.app.telegram import verify_init_data

miniapp_bp = Blueprint("miniapp", __name__)


def get_user_id() -> int | None:
    """Resolve user id from cookie."""
    cookie_uid = request.cookies.get("tg_uid")
    if cookie_uid:
        try:
            return int(cookie_uid)
        except ValueError:
            current_app.logger.warning("Invalid tg_uid cookie: %s", cookie_uid)
            return None
    return None


def require_user_id():
    """Return user id or a loading screen response."""
    uid = get_user_id()
    if uid is None:
        response = make_response(
            render_template(
                "loading.html",
                title="Загрузка",
            ),
            200,
        )
        return None, response
    return uid, None


@miniapp_bp.route("/health")
def health_check():
    return {"status": "ok"}, 200


@miniapp_bp.route("/miniapp")
def miniapp_days():
    uid, error_response = require_user_id()
    if error_response:
        return error_response
    return render_template("miniapp_days.html", title="Weight Tracker")


@miniapp_bp.route("/miniapp/auth", methods=["POST"])
def miniapp_auth():
    """Verify Telegram initData and set user cookie."""
    payload = request.get_json(silent=True) or {}
    init_data = payload.get("initData", "")
    user = verify_init_data(init_data, current_app.config.get("TELEGRAM_BOT_TOKEN", ""))
    if not user or "id" not in user:
        current_app.logger.warning("Telegram initData verification failed")
        return ("", 401)

    resp = make_response("", 204)
    resp.set_cookie(
        "tg_uid",
        str(user["id"]),
        max_age=60 * 60 * 24 * 30,
        httponly=True,
        samesite="Lax",
        secure=request.is_secure,
        path="/",
    )
    return resp


@miniapp_bp.route("/miniapp/day/<int:day>")
def miniapp_exercises(day: int):
    user_id, error_response = require_user_id()
    if error_response:
        return error_response
    exercises = exercises_service.list_day(user_id=user_id, day=day)
    return render_template(
        "miniapp_exercises.html",
        title="Упражнения",
        exercises=exercises,
        day=day,
    )


@miniapp_bp.route("/miniapp/day/<int:day>/add", methods=["GET", "POST"])
def miniapp_add_exercise(day: int):
    user_id, error_response = require_user_id()
    if error_response:
        return error_response

    if request.method == "POST":
        try:
            payload = ExerciseCreateInput(
                name=request.form["name"].strip(),
                weight=request.form["weight"],
                weight_unit=request.form.get("weight_unit", "kg"),
                reps=request.form["reps"],
                sets=request.form["sets"],
            )
        except ValidationError:
            return render_template(
                "error.html",
                title="Ошибка ввода",
                code=400,
                message="Проверьте введенные значения.",
            ), 400

        exercises_service.create(
            user_id=user_id,
            day=day,
            name=payload.name,
            weight=payload.weight,
            weight_unit=payload.weight_unit,
            reps=payload.reps,
            sets=payload.sets,
        )
        return redirect(f"/miniapp/day/{day}")

    return render_template(
        "miniapp_add_exercise.html",
        title="Добавить упражнение",
        day=day,
    )


@miniapp_bp.route("/miniapp/exercise/<int:ex_id>")
def miniapp_input(ex_id: int):
    user_id, error_response = require_user_id()
    if error_response:
        return error_response
    exercise = exercises_service.get(user_id=user_id, ex_id=ex_id)
    if not exercise:
        return redirect("/miniapp")

    history = workouts_service.list_recent(user_id=user_id, exercise_id=ex_id, limit=10)
    return render_template(
        "miniapp_input.html",
        title=exercise["name"],
        exercise=exercise,
        history=history,
    )


@miniapp_bp.route("/miniapp/save", methods=["POST"])
def miniapp_save():
    user_id, error_response = require_user_id()
    if error_response:
        return error_response

    try:
        payload = WorkoutInput(
            exercise_id=request.form["exercise_id"],
            weight=request.form["weight"],
            weight_unit=request.form.get("weight_unit", "kg"),
            reps=request.form["reps"],
            sets=request.form["sets"],
        )
    except ValidationError:
        return render_template(
            "error.html",
            title="Ошибка ввода",
            code=400,
            message="Проверьте введенные значения.",
        ), 400

    exercise = exercises_service.get(user_id=user_id, ex_id=payload.exercise_id)
    if not exercise:
        return render_template(
            "error.html",
            title="Не найдено",
            code=404,
            message="Упражнение не найдено.",
        ), 404

    workouts_service.create(
        user_id=user_id,
        exercise_id=payload.exercise_id,
        weight=payload.weight,
        weight_unit=payload.weight_unit,
        reps=payload.reps,
        sets=payload.sets,
    )

    return redirect(f"/miniapp/day/{exercise['day']}")


@miniapp_bp.route("/miniapp/stats")
def miniapp_stats():
    user_id, error_response = require_user_id()
    if error_response:
        return error_response
    data = workouts_service.list_stats(user_id=user_id)
    return render_template(
        "miniapp_stats.html",
        title="Статистика",
        data=data,
    )


@miniapp_bp.route("/miniapp/exercise/<int:ex_id>/edit", methods=["GET", "POST"])
def miniapp_edit_exercise(ex_id: int):
    user_id, error_response = require_user_id()
    if error_response:
        return error_response
    exercise = exercises_service.get(user_id=user_id, ex_id=ex_id)
    if not exercise:
        return redirect("/miniapp")

    if request.method == "POST":
        try:
            payload = ExerciseUpdateInput(
                name=request.form["name"].strip(),
                default_unit=request.form.get("default_unit", "kg"),
            )
        except ValidationError:
            return render_template(
                "error.html",
                title="Ошибка ввода",
                code=400,
                message="Проверьте введенные значения.",
            ), 400

        exercises_service.update(
            user_id=user_id,
            ex_id=ex_id,
            name=payload.name,
            default_unit=payload.default_unit,
        )
        return redirect(f"/miniapp/day/{exercise['day']}")

    return render_template(
        "miniapp_edit_exercise.html",
        title="Редактировать",
        exercise=exercise,
    )


@miniapp_bp.route("/miniapp/exercise/<int:ex_id>/delete", methods=["POST"])
def miniapp_delete_exercise(ex_id: int):
    user_id, error_response = require_user_id()
    if error_response:
        return error_response
    exercises_service.delete(user_id=user_id, ex_id=ex_id)
    return redirect("/miniapp")
