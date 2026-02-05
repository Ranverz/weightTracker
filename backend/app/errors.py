from __future__ import annotations

import logging

import psycopg
from flask import Flask, render_template
from pydantic import ValidationError

logger = logging.getLogger(__name__)


def register_error_handlers(app: Flask) -> None:
    """Attach error handlers to the Flask app."""

    @app.errorhandler(404)
    def not_found(_err):  # type: ignore[no-untyped-def]
        return render_template(
            "error.html",
            title="Не найдено",
            code=404,
            message="Страница не найдена.",
        ), 404

    @app.errorhandler(psycopg.Error)
    def db_error(err):  # type: ignore[no-untyped-def]
        logger.exception("Database error: %s", err)
        return render_template(
            "error.html",
            title="Ошибка базы данных",
            code=500,
            message="Произошла ошибка базы данных. Попробуйте позже.",
        ), 500

    @app.errorhandler(ValidationError)
    def validation_error(err):  # type: ignore[no-untyped-def]
        logger.warning("Validation error: %s", err)
        return render_template(
            "error.html",
            title="Ошибка ввода",
            code=400,
            message="Проверьте введенные значения.",
        ), 400

    @app.errorhandler(Exception)
    def unhandled_error(err):  # type: ignore[no-untyped-def]
        logger.exception("Unhandled error: %s", err)
        return render_template(
            "error.html",
            title="Ошибка",
            code=500,
            message="Произошла непредвиденная ошибка. Попробуйте позже.",
        ), 500
