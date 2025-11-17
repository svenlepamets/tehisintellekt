import os
import re
from openai import AsyncOpenAI

DEFAULT_GPT_MODEL = 'gpt-5-nano'

# 1. Define the asynchronous function
async def get_answer_from_openai(prompt: str, domain: str, clean_ouput: bool = True) -> tuple[str, str]:
    """
    Makes an asynchronous API call to OpenAI
    """
    gpt_model = get_gpt_model()
    # The API key must be set as an environment variable (OPENAI_API_KEY)
    if not os.getenv("OPENAI_API_KEY"):
        return "Error: OPENAI_API_KEY environment variable is not set.", gpt_model
    try:
        async with AsyncOpenAI(api_key=os.getenv("OPENAI_API_KEY")) as client:
            response = await client.responses.create(
                model=gpt_model,
                reasoning={"effort": "low"},
                tools=[
                    {
                        "type": "web_search",
                        "filters": {
                            "allowed_domains": [domain]
                        }
                    }
                ],
                tool_choice="auto",
                input=[
                    {
                        "role": "developer",
                        "content": f"Context is {domain}. Answer based on this website."
                    },
                    {
                        "role": "user",
                        "content": prompt
                    }
                ],
                service_tier="flex"  # optimize costs, since it's not a production project
            )
            print(response.__dict__)
            output = clean_output_text(response.output_text) if clean_ouput else response.output_text
            return output, gpt_model
    except Exception as e:
        return f"An error occurred during the API call: {e}", gpt_model

def get_gpt_model():
    return os.getenv("OPENAI_MODEL", DEFAULT_GPT_MODEL)

def clean_output_text(output: str) -> str:
    cleaned_output = re.sub(r"\(\[[^\]]+\]\([^)]+\)\)", "", output)
    return cleaned_output.strip()