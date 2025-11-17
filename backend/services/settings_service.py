import os
from services.gemini_service import get_gemini_model, get_answer_from_gemini
from services.openai_service import get_gpt_model, get_answer_from_openai

def get_available_services():
    available_services = []
    gemini_available = os.getenv("GEMINI_API_KEY") not in [None, ""]
    openai_available = os.getenv("OPENAI_API_KEY") not in [None, ""]
    if gemini_available:
        available_services.append({'service': 'gemini', 'name': f'Gemini ({get_gemini_model()})'})
    if openai_available:
        available_services.append({'service': 'openai', 'name': f'OpenAI ({get_gpt_model()})'})
    return available_services

def get_function_by_service(service):
    funcs = {
        'openai': get_answer_from_openai,
        'gemini': get_answer_from_gemini
    }
    return funcs.get(service) or get_answer_from_openai