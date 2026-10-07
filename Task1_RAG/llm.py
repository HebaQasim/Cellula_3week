"""Part 5 (step A): connect to the LLM (Google Gemini), with ChatOpenAI like the mentor's demo."""
import os
from functools import lru_cache
from pathlib import Path

from dotenv import load_dotenv
from langchain_openai import ChatOpenAI

BASE_DIR = Path(__file__).parent
load_dotenv(BASE_DIR / ".env")   # puts the values written in the .env file into os.environ

# Gemini accepts the same request format as OpenAI, so ChatOpenAI works with it (only base_url changes)
LLM_BASE_URL = "https://generativelanguage.googleapis.com/v1beta/openai/"

# Free models are sometimes busy, so we keep a list: if one fails, the next one is tried
LLM_MODELS = [
    "gemini-3.5-flash",       # first choice: answered in about 2 s in our test
    "gemini-3.1-flash-lite",  # second choice: also answered in our test (about 7 s)
    "gemini-3.5-flash-lite",  # last choice
]


def make_chat_model(model_name, api_key):
    """One Gemini model, reached through ChatOpenAI."""
    return ChatOpenAI(
        api_key=api_key,
        base_url=LLM_BASE_URL,
        model=model_name,
        # No temperature here: Google recommends keeping the default (1.0) for Gemini 3 models
        reasoning_effort="low",   # think a little before answering: enough for reading chunks, and faster
        timeout=30,               # stop waiting after 30 seconds (then the next model is tried)
        max_retries=0,            # no retry on the same model: the next model is the retry
    )


@lru_cache(maxsize=1)
def load_llm():
    """Create the chat model the first time; later calls reuse it."""
    api_key = os.getenv("GEMINI_API_KEY")
    if not api_key:
        raise ValueError("GEMINI_API_KEY is missing: write it in the .env file next to the code.")
    models = [make_chat_model(name, api_key) for name in LLM_MODELS]
    # with_fallbacks (from LangChain): if the first model gives an error, try the others in order
    return models[0].with_fallbacks(models[1:])


if __name__ == "__main__":
    llm = load_llm()
    response = llm.invoke("In one sentence, what is Retrieval-Augmented Generation (RAG)?")
    print("Model that answered:", response.response_metadata.get("model_name"))
    print("Answer:", response.content)
