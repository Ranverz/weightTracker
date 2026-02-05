from __future__ import annotations

from flask import Flask

from backend.app.config import AppConfig
from backend.app.errors import register_error_handlers
from backend.app.logging_config import configure_logging
from backend.app.routes.miniapp import miniapp_bp


def create_app() -> Flask:
    """Application factory for Flask."""
    configure_logging()
    app = Flask(
        __name__,
        template_folder="templates",
        static_folder="static",
    )
    app.config.from_object(AppConfig())

    app.register_blueprint(miniapp_bp)
    register_error_handlers(app)
    return app
