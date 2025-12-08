from typing import Literal

from pydantic import BaseModel


class Question(BaseModel):
    question: str
    domain: str
    service: str


class Answer(BaseModel):
    answer: str
    domain: str
    source: str
    timestamp: float


class LLMService(BaseModel):
    service: str
    name: str


class LLMSettings(BaseModel):
    services: list[LLMService]


class Health(BaseModel):
    status: Literal["ok"]
