import time
from urllib.parse import urlparse


def parse_url(unclean_url: str) -> str:
    # Basic parsing for URL coming from the frontend
    try:
        if "." not in unclean_url:  # does not seem like a valid URL
            raise Exception
        parsed_url = urlparse(unclean_url)
    except Exception:
        return ""
    # Depending on how the URL is written, either one could be correct (with priority on netloc)
    # Note that both Gemini and OpenAI API-s expect URL without protocol
    return parsed_url.netloc or parsed_url.path


def get_timestamp():
    return round(time.time(), 4)
