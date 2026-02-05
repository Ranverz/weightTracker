from __future__ import annotations

import os


class AppConfig:
    """Centralized app configuration.

    In production you would pull these from environment variables or a
    secrets manager. For now we keep defaults minimal and explicit.
    """

    DATABASE_URL: str = os.getenv("DATABASE_URL", "")
    DEFAULT_USER_ID: int = int(os.getenv("DEFAULT_USER_ID", "123"))
    TELEGRAM_BOT_TOKEN: str = os.getenv("BOT_TOKEN", "")
