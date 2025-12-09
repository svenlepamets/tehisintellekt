# This is just an example how to test a FastAPI endpoint
from unittest.mock import AsyncMock

import pytest
from fastapi.testclient import TestClient

from models.models import LLMService
from server import app

client = TestClient(app)


def test_health():
    response = client.get("/api/health")

    assert response.status_code == 200
    assert response.json() == {"status": "ok"}


def test_get_settings(monkeypatch):
    # Make the output predictable by ensuring one service is set up and the other one not - to test both scenarios
    monkeypatch.setenv("OPENAI_API_KEY", "mock")
    monkeypatch.delenv("GEMINI_API_KEY", raising=False)
    monkeypatch.delenv("FIRECRAWL_API_KEY", raising=False)
    response = client.get("/api/settings")
    assert response.status_code == 200

    assert response.json()["services"][0]["service"] == "openai"


@pytest.mark.asyncio
async def test_ask_endpoint(monkeypatch):
    MOCK_QUESTION = "Conan! What is best in life?"
    MOCK_ANSWER = "A good meal, a comfy chair, and Wi-Fi that actually works."
    MOCK_MODEL = "openai-model"
    MOCK_TIMESTAMP = 123456

    # Do some mocking, test at the boundaries
    monkeypatch.setattr("server.get_available_llm_services", lambda: [LLMService(service="openai", name="OpenAI")])
    fake_llm = AsyncMock(return_value=(MOCK_ANSWER, MOCK_MODEL))
    monkeypatch.setattr("server.get_function_by_llm_service", lambda service: fake_llm)
    monkeypatch.setattr("server.get_timestamp", lambda: MOCK_TIMESTAMP)

    # Create payload
    payload = {"question": MOCK_QUESTION, "domain": "https://youtube.com", "service": "openai"}

    response = client.post("/api/ask", json=payload)
    data = response.json()

    # Assert the results
    assert response.status_code == 200
    assert "domain" in data
    assert data["answer"] == MOCK_ANSWER
    assert data["source"] == MOCK_MODEL
    assert data["timestamp"] == MOCK_TIMESTAMP
    fake_llm.assert_awaited()
