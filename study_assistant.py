"""AI Study Assistant: type a tech topic, get a beginner-friendly study card."""

import os
import sys

from dotenv import load_dotenv
from groq import APIConnectionError, APIStatusError, Groq, RateLimitError

MODEL = "openai/gpt-oss-120b"


def build_messages(topic: str) -> list[dict[str, str]]:
    """Build the chat messages for a topic. Edit the text here to change the card."""
    system = (
        "You are a patient programming tutor for first-time learners. "
        "Use plain words, keep things short, and never invent facts. "
        "Always answer in exactly this plain-text layout, with these headings:\n"
        "\n"
        "EXPLANATION\n"
        "(2-3 simple sentences)\n"
        "\n"
        "COMMON USES\n"
        "(2-3 bullet points starting with '- ')\n"
        "\n"
        "EXAMPLE\n"
        "(a short Python snippet with brief comments, in a fenced code block)\n"
        "\n"
        "KEY POINTS\n"
        "(3-5 bullet points starting with '- ')\n"
        "\n"
        "QUIZ\n"
        "(2-3 numbered questions, no answers)"
    )
    return [
        {"role": "system", "content": system},
        {"role": "user", "content": f"Make a study card for this topic: {topic}"},
    ]


def get_client() -> Groq | None:
    """Return a Groq client, or None if GROQ_API_KEY is not set."""
    load_dotenv()
    api_key = os.environ.get("GROQ_API_KEY", "").strip()
    if not api_key:
        return None
    return Groq(api_key=api_key)


def make_study_card(client: Groq, topic: str) -> str:
    """Ask the model for a study card and return the text."""
    response = client.chat.completions.create(
        model=MODEL,
        messages=build_messages(topic),
        temperature=0.4,  # low = more consistent cards
        reasoning_effort="low",  # gpt-oss thinks first; keep it quick
        max_completion_tokens=2500,
    )
    text = response.choices[0].message.content
    if not text:
        raise ValueError("The model sent back an empty answer. Try again.")
    return text.strip()


def safe_study_card(client: Groq, topic: str) -> str | None:
    """Like make_study_card, but prints a friendly message instead of crashing."""
    try:
        return make_study_card(client, topic)
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


def main() -> int:
    client = get_client()
    if client is None:
        print("No API key found.")
        print("Copy .env.example to .env, then put your key after GROQ_API_KEY=")
        print("(you can get a free key at https://console.groq.com).")
        return 1

    # Optional: topics given on the command line are run once, then we exit.
    if len(sys.argv) > 1:
        card = safe_study_card(client, " ".join(sys.argv[1:]))
        if card:
            print(card)
        return 0 if card else 1

    print("AI Study Assistant - type a topic, or 'quit' to leave.\n")
    while True:
        try:
            topic = input("Topic: ").strip()
        except (EOFError, KeyboardInterrupt):
            print()
            break
        if topic.lower() == "quit":
            break
        if not topic:
            continue
        card = safe_study_card(client, topic)
        if card:
            print(f"\n{card}\n{'-' * 60}")
    return 0


if __name__ == "__main__":
    sys.exit(main())
