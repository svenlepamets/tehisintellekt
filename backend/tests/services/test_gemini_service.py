from unittest.mock import AsyncMock, MagicMock, patch

import pytest

from services.gemini_service import get_answer_from_gemini


# Note that this test is not parametrized because the input parameters don't affect anything,
# considering that the API call is mocked
@pytest.mark.asyncio
async def test_get_answer_from_gemini(monkeypatch):
    MOCK_OUTPUT = "I do believe it's working. Good."
    MOCK_MODEL = "gemini-ultra-nonexistant"

    # Mock GEMINI_API_KEY otherwise the function will just return an error message
    monkeypatch.setenv("GEMINI_API_KEY", "mock")
    monkeypatch.setenv("GEMINI_MODEL", MOCK_MODEL)

    # This is the fake response object
    fake_response = MagicMock()
    fake_response.text = MOCK_OUTPUT

    # Create mock for client.models.generate_content
    mock_client = MagicMock()
    mock_client.models.generate_content = AsyncMock(return_value=fake_response)

    # Create async context manager mock for genai.Client().aio
    class MockAioCtxManager:
        async def __aenter__(self):
            return mock_client

        async def __aexit__(self, exc_type, exc, tb):
            pass

    # Mock genai.Client to return an object with the aio context manager
    mock_client_constructor = MagicMock()
    mock_client_constructor.aio = MockAioCtxManager()

    with patch("services.gemini_service.genai.Client", return_value=mock_client_constructor):
        text, model = await get_answer_from_gemini("Hello? Is there anybody in there?", "pinkfloyd.com")

    assert text == MOCK_OUTPUT and model == MOCK_MODEL
