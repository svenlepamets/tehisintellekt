import time
from urllib.parse import urlparse
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


def parse_url(unclean_url: str) -> str:
    # Basic parsing for URL coming from the frontend
    try:
        parsed_url = urlparse(unclean_url)
    except:
        return ""
    return parsed_url.path

def get_timestamp():
    return round(time.time(), 4)

