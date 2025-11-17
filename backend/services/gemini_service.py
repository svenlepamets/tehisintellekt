import os
import asyncio
from google import genai
from google.genai import types


DEFAULT_GEMINI_MODEL = "gemini-2.5-flash"

async def get_answer_from_gemini(prompt: str, domain: str) -> tuple[str, str]:
    """
    Makes an asynchronous API call to Gemini, enabling Google Search 
    to retrieve up-to-date information (uses Google Grounding Tool).
    """

    gemini_model = get_gemini_model()

    # The API key must be set as an environment variable (GEMINI_API_KEY)
    if not os.getenv("GEMINI_API_KEY"):
        return "Error: GEMINI_API_KEY environment variable is not set.", gemini_model

    try:
        # 2. Initialize the asynchronous client
        async with genai.Client().aio as client:

            # 3. Define the Google Search Tool
            grounding_tool = types.Tool(
                google_search=types.GoogleSearch()
            )

            # 4. Create the configuration to include the tool
            config = types.GenerateContentConfig(
                tools=[grounding_tool]
            )

            # 5. Make the asynchronous API call using await
            prompt = f"{prompt +' site:' + domain}"
            response = await client.models.generate_content(
                model=gemini_model, 
                contents=prompt,
                config=config
            )

            # 6. Return the response text
            return response.text, gemini_model

    except Exception as e:
        return f"An error occurred during the API call: {e}", gemini_model

def get_gemini_model() -> str:
    return os.getenv("GEMINI_MODEL", DEFAULT_GEMINI_MODEL)