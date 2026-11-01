"""Shared helpers for talking to Groq, used by every script in this repo."""

import os
import sys

from dotenv import load_dotenv
from groq import APIConnectionError, APIStatusError, Groq, RateLimitError

# Windows consoles often use cp1252, which can't print some characters the model
# produces (for example a non-breaking hyphen). Switch output to UTF-8 so printing
# never crashes.
for _stream in (sys.stdout, sys.stderr):
    if hasattr(_stream, "reconfigure"):
        _stream.reconfigure(encoding="utf-8", errors="replace")

MODEL = "openai/gpt-oss-120b"

NO_KEY_HELP = (
    "No API key found.\n"
    "Copy .env.example to .env, then put your key after GROQ_API_KEY=\n"
    "(you can get a free key at https://console.groq.com)."
)


def get_client() -> Groq | None:
    """Return a Groq client, or None if GROQ_API_KEY is not set."""
    load_dotenv()
    api_key = os.environ.get("GROQ_API_KEY", "").strip()
    if not api_key:
        return None
    return Groq(api_key=api_key)


def chat(
    client: Groq,
    messages: list[dict[str, str]],
    temperature: float = 0.4,
    max_tokens: int = 2500,
) -> str:
    """Send messages to the model and return the reply text."""
    response = client.chat.completions.create(
        model=MODEL,
        messages=messages,
        temperature=temperature,
        reasoning_effort="low",  # gpt-oss thinks before answering; keep it quick
        max_completion_tokens=max_tokens,
    )
    text = response.choices[0].message.content
    if not text:
        raise ValueError("The model sent back an empty answer. Try again.")
    return text.strip()


def friendly_chat(client: Groq, messages: list[dict[str, str]], **kwargs) -> str | None:
    """Like chat(), but prints a short message instead of raising for common errors."""
    try:
        return chat(client, messages, **kwargs)
    except RateLimitError:
        print("Rate limit reached (HTTP 429). Wait a few seconds and try again.")
    except APIConnectionError:
        print("Could not reach Groq. Check your internet connection and try again.")
    except APIStatusError as e:
        if e.status_code == 401:
            print("Groq rejected the API key. Check GROQ_API_KEY in your .env file.")
        else:
            print(f"Groq returned an error (HTTP {e.status_code}). Try again later.")
    except ValueError as e:
        print(e)
    return None


def require_client() -> Groq:
    """For small demo scripts: return a client or exit with a friendly message."""
    client = get_client()
    if client is None:
        raise SystemExit(NO_KEY_HELP)
    return client
