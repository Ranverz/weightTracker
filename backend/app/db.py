from __future__ import annotations

from contextlib import contextmanager
from typing import Generator

import psycopg
from flask import current_app


@contextmanager
def get_conn() -> Generator[psycopg.Connection, None, None]:
    """Provide a short-lived DB connection using app config."""
    database_url = current_app.config.get("DATABASE_URL", "")
    if not database_url:
        raise RuntimeError("DATABASE_URL is not configured")

    with psycopg.connect(database_url) as conn:
        yield conn
