import os

from models.models import LLMService
from services.gemini_service import get_answer_from_gemini, get_gemini_model
from services.openai_service import get_answer_from_openai, get_gpt_model


def get_available_llm_services() -> list[LLMService]:
    available_services = []
    gemini_available = os.getenv("GEMINI_API_KEY") not in [None, ""]
    openai_available = os.getenv("OPENAI_API_KEY") not in [None, ""]
    if gemini_available:
        available_services.append(
            LLMService(service="gemini", name=f"Gemini ({get_gemini_model()})")
        )
    if openai_available:
        available_services.append(
            LLMService(service="openai", name=f'OpenAI ({get_gpt_model()})')
        )
    return available_services


def get_function_by_llm_service(service):
    funcs = {
        'openai': get_answer_from_openai,
        'gemini': get_answer_from_gemini
    }
    return funcs.get(service) or get_answer_from_openai
