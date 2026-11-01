"""Exercise 2: GET /todos/5 and say whether the task is done."""

import requests

BASE_URL = "https://jsonplaceholder.typicode.com"


def main() -> None:
    try:
        response = requests.get(f"{BASE_URL}/todos/5", timeout=10)
        response.raise_for_status()
    except requests.RequestException as e:
        raise SystemExit(f"Request failed: {e}")

    todo = response.json()
    state = "completed" if todo["completed"] else "not completed yet"
    print(f"Todo #{todo['id']}: \"{todo['title']}\" is {state}.")


if __name__ == "__main__":
    main()
