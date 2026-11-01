"""Make study cards for several topics at once and save them as JSON.

Examples (run from the repo root):
    python -m extras.batch_cards --topics "recursion" "REST API" "list vs dictionary"
    python -m extras.batch_cards --topics recursion --post
"""

import argparse
import json
import time
from datetime import datetime
from pathlib import Path

import requests

from groq_client import NO_KEY_HELP, get_client
from study_assistant import safe_study_card

POST_URL = "https://jsonplaceholder.typicode.com/posts"
PAUSE_SECONDS = 2  # small gap between requests to stay inside free-tier limits


def post_to_placeholder(topic: str, card: str) -> int | None:
    """Practice POST: send the card to JSONPlaceholder (it only pretends to save)."""
    try:
        response = requests.post(
            POST_URL, json={"title": topic, "body": card, "userId": 1}, timeout=10
        )
        response.raise_for_status()
        return response.status_code
    except requests.RequestException as e:
        print(f"  POST failed: {e}")
        return None


def main() -> int:
    parser = argparse.ArgumentParser(description="Generate study cards for many topics.")
    parser.add_argument("--topics", nargs="+", required=True, help="one or more topics")
    parser.add_argument("--out", default="cards.json", help="JSON file to write")
    parser.add_argument("--post", action="store_true", help="also POST each card")
    args = parser.parse_args()

    client = get_client()
    if client is None:
        print(NO_KEY_HELP)
        return 1

    cards = []
    for i, topic in enumerate(args.topics):
        if i:
            time.sleep(PAUSE_SECONDS)
        print(f"Making a card for: {topic}")
        card = safe_study_card(client, topic)
        if card is None:
            continue
        entry = {"topic": topic, "card": card}
        if args.post:
            entry["post_status"] = post_to_placeholder(topic, card)
            print(f"  POST status: {entry['post_status']}")
        cards.append(entry)

    if not cards:
        print("No cards were made, so nothing was saved.")
        return 1

    payload = {"created": datetime.now().isoformat(timespec="seconds"), "cards": cards}
    Path(args.out).write_text(json.dumps(payload, indent=2, ensure_ascii=False), encoding="utf-8")
    print(f"Saved {len(cards)} card(s) to {args.out}")
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
