import os

import faiss
import numpy as np
from firecrawl import AsyncFirecrawl
from openai import AsyncOpenAI

from services.openai_service import get_gpt_model
from services.rag_cache import cache_exists, cache_is_fresh, load_cache, save_cache


async def crawl_website(url: str, max_pages=50):
    firecrawl = AsyncFirecrawl(api_key=os.getenv("FIRECRAWL_API_KEY"))
    resp = await firecrawl.v2.crawl(url=url, limit=max_pages, poll_interval=1, timeout=240)
    return resp.data


def chunk(text, size=1000, overlap=100):
    """Cut a webpage content into smaller chunks for better digesting
    """
    chunks = []
    start = 0
    while start < len(text):
        end = start + size
        chunks.append(text[start:end])
        start = end - overlap
    return chunks


async def build_index(pages, client: AsyncOpenAI):
    texts = []
    meta = []

    for page in pages:
        for c in chunk(page.markdown):
            texts.append(c)
            meta.append({"source": page.metadata.source_url})

    emb = await client.embeddings.create(
        model="text-embedding-3-large",
        input=texts
    )

    vecs = np.array([e.embedding for e in emb.data], dtype="float32")

    index = faiss.IndexFlatL2(vecs.shape[1])
    index.add(vecs)

    return index, texts, meta, vecs


async def retrieve_context(query, index, texts, meta, client):
    """Find the most relevant part of the crawled data to use as context
    """
    emb = await client.embeddings.create(
        model="text-embedding-3-large",
        input=[query]
    )
    q = np.array([emb.data[0].embedding], dtype="float32")

    distances, indices = index.search(q, 8)

    return [
        {"text": texts[i], "source": meta[i]["source"]}
        for i in indices[0]
    ]

async def rag_answer(question, retrieved, client: AsyncOpenAI):
    context = "\n\n".join(
        [f"(Source: {r['source']})\n{r['text']}" for r in retrieved]
    )
    prompt = f"""
        Answer the question using ONLY the context below.
        Assume that the source might not be in English.
        If the answer is not present, say "I don't know."

        CONTEXT:
        {context}

        QUESTION: {question}

        Answer:
    """

    res = await client.chat.completions.create(
        model=get_gpt_model(),
        messages=[{"role": "user", "content": prompt}]
    )

    return res.choices[0].message.content


async def run_rag_pipeline(prompt: str, url: str, max_pages: int = 50):
    """This is the entrypoint of the RAG pipeline
    """
    if not os.getenv("OPENAI_API_KEY") or not os.getenv("FIRECRAWL_API_KEY"):
        return "Error: OPENAI_API_KEY environment variable is not set " \
                "or FIRECRAWL_API_KEY environment variable is not set.", get_rag_label()
    client = AsyncOpenAI(api_key=os.getenv("OPENAI_API_KEY"))
    if cache_exists(url) and cache_is_fresh(url, 3600):
        vectors, index, texts, meta = load_cache(url)
    else:
        pages = await crawl_website(url, max_pages)
        index, texts, meta, vectors = await build_index(pages, client)
        save_cache(url, vectors, index, texts, meta)
    retrieved_context = await retrieve_context(prompt, index, texts, meta, client)
    answer = await rag_answer(prompt, retrieved_context, client)
    return answer, get_rag_label()


def get_rag_label():
    return f"rag-{get_gpt_model()}"
