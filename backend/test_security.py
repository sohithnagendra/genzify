"""Regression tests for GenZify's Flask API.

Run from the repository root with:
    python -m pytest backend/test_security.py
External AI requests are mocked; these tests do not consume provider credits.
"""
import importlib
import sys
from pathlib import Path
from types import SimpleNamespace
from unittest.mock import patch

import pytest

BACKEND_DIR = Path(__file__).resolve().parent
if str(BACKEND_DIR) not in sys.path:
    sys.path.insert(0, str(BACKEND_DIR))

# Set a dummy key before importing the application module.
import os
os.environ.setdefault("NVIDIA_API_KEY", "test-only-not-a-real-key")
app_module = importlib.import_module("app")


@pytest.fixture
def client():
    app_module.app.config.update(TESTING=True)
    return app_module.app.test_client()


def test_rejects_non_object_json(client):
    response = client.post("/api/convert", json=["not", "an", "object"])
    assert response.status_code == 400


@pytest.mark.parametrize("value", [None, 123, [], {}])
def test_rejects_non_string_text(client, value):
    response = client.post("/api/convert", json={"text": value})
    assert response.status_code == 400


@pytest.mark.parametrize("value", ["", "   ", "\n\t"])
def test_rejects_blank_text(client, value):
    response = client.post("/api/convert", json={"text": value})
    assert response.status_code == 400


def test_rejects_text_over_5000_characters(client):
    response = client.post("/api/convert", json={"text": "A" * 5001})
    assert response.status_code == 413


def test_valid_request_uses_mocked_ai(client):
    fake_response = SimpleNamespace(
        choices=[
            SimpleNamespace(
                message=SimpleNamespace(content="That is so valid fr.")
            )
        ]
    )

    with patch.object(
        app_module.client.chat.completions,
        "create",
        return_value=fake_response,
    ) as mock_create:
        response = client.post(
            "/api/convert",
            json={"text": "That is very good."},
        )

    assert response.status_code == 200
    assert response.get_json() == {"result": "That is so valid fr."}
    mock_create.assert_called_once()


def test_upstream_failure_returns_generic_error(client):
    with patch.object(
        app_module.client.chat.completions,
        "create",
        side_effect=RuntimeError("simulated provider failure"),
    ):
        response = client.post("/api/convert", json={"text": "Hello"})

    assert response.status_code == 502
    assert response.get_json() == {
        "error": "Text conversion failed. Please try again."
    }
    assert "simulated provider failure" not in response.get_data(as_text=True)
