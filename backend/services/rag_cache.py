# cache.py
import json
import time
from pathlib import Path

import faiss
import numpy as np

CACHE_DIR = Path(".cache")
CACHE_DIR.mkdir(exist_ok=True)

CACHE_TTL = 24*3600  # One day

# ----- Cache file paths -----

def _base(url: str) -> Path:
    """Create a safe filename for this URL."""
    safe = url.replace("://", "_").replace("/", "_")
    return CACHE_DIR / safe


def embeddings_path(url: str) -> Path:
    return _base(url).with_suffix(".emb.npy")


def index_path(url: str) -> Path:
    return _base(url).with_suffix(".faiss")


def texts_path(url: str) -> Path:
    return _base(url).with_suffix(".texts.json")


def meta_path(url: str) -> Path:
    return _base(url).with_suffix(".meta.json")


def timestamp_path(url: str) -> Path:
    return _base(url).with_suffix(".time")


# ----- Cache Check -----

def cache_exists(url: str) -> bool:
    return (
        embeddings_path(url).exists()
        and index_path(url).exists()
        and texts_path(url).exists()
        and meta_path(url).exists()
        and timestamp_path(url).exists()
    )


def cache_is_fresh(url: str, max_age_seconds: int = CACHE_TTL) -> bool:
    """Check whether the cached KB is younger than max_age_seconds."""
    if not cache_exists(url):
        return False

    ts_file = timestamp_path(url)
    age = time.time() - ts_file.stat().st_mtime
    return age < max_age_seconds


def save_cache(url: str, vectors: np.ndarray, faiss_index, texts, meta):
    # Save embeddings
    np.save(embeddings_path(url), vectors)

    # Save FAISS index
    faiss.write_index(faiss_index, str(index_path(url)))

    # Save texts + meta
    texts_path(url).write_text(json.dumps(texts, ensure_ascii=False))
    meta_path(url).write_text(json.dumps(meta, ensure_ascii=False))

    # Update timestamp
    timestamp_path(url).write_text(str(time.time()))


def load_cache(url: str):
    """Returns (vectors, faiss_index, texts, meta)."""
    vectors = np.load(embeddings_path(url))
    faiss_index = faiss.read_index(str(index_path(url)))
    texts = json.loads(texts_path(url).read_text())
    meta = json.loads(meta_path(url).read_text())

    return vectors, faiss_index, texts, meta
