"""System role: set a persona before the user's message."""

from groq_client import chat, require_client

client = require_client()
messages = [
    {
        "role": "system",
        "content": "You are a strict grammar teacher. Point out every mistake, briefly. Plain text only, no markdown.",
    },
    {"role": "user", "content": "She don't like coding."},
]
print(chat(client, messages, max_tokens=500))
