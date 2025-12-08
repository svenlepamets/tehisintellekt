import os

from fastapi import FastAPI
from fastapi.middleware.cors import CORSMiddleware

from models.models import Answer, Health, LLMSettings, Question
from services.settings_service import get_available_llm_services, get_function_by_llm_service
from services.utils import get_timestamp, parse_url

app = FastAPI()

is_dev = os.getenv('DEV', None)

if is_dev:
    origins = [
        "http://localhost:3000",  # frontend
        "http://localhost",       # some browsers strip ports in OPTIONS
    ]

    app.add_middleware(
        CORSMiddleware,
        allow_origins=origins,
        allow_credentials=True,
        allow_methods=["*"],
        allow_headers=["*"],
    )


@app.post("/api/ask")
async def ask(q: Question) -> Answer:
    # Default values
    service = "openai"
    domain = "tehisintellekt.ee"

    available_services = get_available_llm_services()
    for available_service in available_services:
        if available_service.service == q.service:
            service = q.service

    func = get_function_by_llm_service(service)

    domain = parse_url(str(q.domain)) or domain
    prompt = q.question[0:min(120, len(q.question)-1)]
    response, source = await func(prompt, domain)
    answer = Answer(answer=response, domain=domain, source=source, timestamp=get_timestamp())
    return answer.model_dump()


@app.get("/api/settings")
async def get_settings() -> LLMSettings:
    services = get_available_llm_services()
    return LLMSettings(services=services)


@app.get("/api/health")
async def get_health() -> Health:
    return Health(status="ok")
