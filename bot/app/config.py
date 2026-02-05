from __future__ import annotations

import os
from dataclasses import dataclass

from dotenv import load_dotenv

load_dotenv()


@dataclass(frozen=True)
class BotConfig:
    bot_token: str
    webapp_url: str
    database_url: str

    @staticmethod
    def from_env() -> "BotConfig":
        bot_token = os.getenv("BOT_TOKEN", "").strip().strip("'\"")
        webapp_url = os.getenv("WEBAPP_URL", "").strip().strip("'\"")
        database_url = os.getenv("DATABASE_URL", "").strip().strip("'\"")

        if not bot_token:
            raise RuntimeError("BOT_TOKEN is required")
        if not webapp_url:
            raise RuntimeError("WEBAPP_URL is required")
        if not database_url:
            raise RuntimeError("DATABASE_URL is required")

        return BotConfig(
            bot_token=bot_token,
            webapp_url=webapp_url,
            database_url=database_url,
        )
