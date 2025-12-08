from unittest.mock import AsyncMock, MagicMock, patch

import pytest

from services.openai_service import get_answer_from_openai


# Note that this test is not parametrized because the input parameters don't affect anything,
# considering that the API call is mocked
@pytest.mark.asyncio
async def test_get_answer_from_openai(monkeypatch):
    MOCK_OUTPUT = "I do believe it's working. Good."
    MOCK_MODEL = "openai-ultra-nonexistant"

    # Mock OPENAI_API_KEY otherwise the function will just return an error message
    monkeypatch.setenv("OPENAI_API_KEY", "mock")
    monkeypatch.setenv("OPENAI_MODEL", MOCK_MODEL)

    # This is the fake response object
    fake_response = MagicMock()
    fake_response.output_text = MOCK_OUTPUT

    # Create mock for client.models.generate_content
    mock_client = MagicMock()
    mock_client.responses.create = AsyncMock(return_value=fake_response)

    # Create async context manager mock for genai.Client().aio
    class MockAioCtxManager:
        async def __aenter__(self):
            return mock_client

        async def __aexit__(self, exc_type, exc, tb):
            pass

    with patch("services.openai_service.AsyncOpenAI", return_value=MockAioCtxManager()):
        text, model = await get_answer_from_openai("Hello? Is there anybody in there?", "pinkfloyd.com")
    print(text)
    assert text == MOCK_OUTPUT and model == MOCK_MODEL
