import os 

from fastapi import FastAPI
from fastapi.middleware.cors import CORSMiddleware
from services.settings_service import get_available_services
from services.settings_service import get_function_by_service
from services.utils import parse_url, get_timestamp, Question, Answer

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
async def ask(q: Question):
    # Default values
    service = "openai"
    domain = "tehisintellekt.ee"

    available_services = get_available_services()
    for available_service in available_services:
        if available_service['service'] == q.service:
            service = q.service
    
    func = get_function_by_service(service)

    domain = parse_url(q.domain) or domain
    prompt = q.question[0:min(120, len(q.question)-1)]
    response, source = await func(prompt, domain)
    answer = Answer(answer=response, domain=domain, source=source, timestamp=get_timestamp())
    return answer.model_dump()

@app.get("/api/settings")
async def get_settings():
    services = get_available_services()
    return {"services": services}
