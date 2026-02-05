from __future__ import annotations

import pytest

from backend.app import create_app


@pytest.fixture()
def app():
    app = create_app()
    app.config.update(TESTING=True)
    yield app


@pytest.fixture()
def client(app):
    client = app.test_client()
    client.set_cookie("localhost", "tg_uid", "123")
    return client
