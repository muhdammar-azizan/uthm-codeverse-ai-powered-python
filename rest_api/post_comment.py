"""Exercise 3: POST a new comment. JSONPlaceholder pretends to save it."""

import requests

BASE_URL = "https://jsonplaceholder.typicode.com"


def main() -> None:
    comment = {
        "postId": 1,
        "name": "Study Assistant learner",
        "email": "learner@example.com",
        "body": "Practising POST requests after the CodeVerse session.",
    }
    try:
        response = requests.post(f"{BASE_URL}/comments", json=comment, timeout=10)
        response.raise_for_status()
    except requests.RequestException as e:
        raise SystemExit(f"Request failed: {e}")

    # 201 = created. The API echoes the comment back with a new id.
    print(f"Status: {response.status_code}")
    print(response.json())


if __name__ == "__main__":
    main()
