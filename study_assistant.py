"""AI Study Assistant: type a tech topic, get a beginner-friendly study card."""

import sys

from groq_client import NO_KEY_HELP, friendly_chat, get_client


def build_messages(topic: str) -> list[dict[str, str]]:
    """Build the chat messages for a topic. Edit the text here to change the card."""
    system = (
        "You are a patient programming tutor for first-time learners. "
        "Use plain words, keep things short, and never invent facts. "
        "Plain text only: no markdown headings, bold or tables (a fenced code block is fine). "
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


def safe_study_card(client, topic: str) -> str | None:
    """Return a study card, or None (after printing a friendly message) on failure."""
    return friendly_chat(client, build_messages(topic))


def main() -> int:
    client = get_client()
    if client is None:
        print(NO_KEY_HELP)
        return 1

    # Optional: a topic given on the command line is run once, then we exit.
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
