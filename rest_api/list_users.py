"""Exercise 1: GET /users and print each person's name and email."""

import requests

BASE_URL = "https://jsonplaceholder.typicode.com"


def main() -> None:
    try:
        response = requests.get(f"{BASE_URL}/users", timeout=10)
        response.raise_for_status()
    except requests.RequestException as e:
        raise SystemExit(f"Request failed: {e}")

    print(f"Status: {response.status_code}")
    for user in response.json():
        print(f"{user['name']:<28} {user['email']}")


if __name__ == "__main__":
    main()
