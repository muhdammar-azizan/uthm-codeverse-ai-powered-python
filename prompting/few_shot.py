"""Few-shot: show a couple of examples so the model copies the answer style."""

from groq_client import chat, require_client

client = require_client()
messages = [
    {"role": "user", "content": "Terrible battery life."},
    {"role": "assistant", "content": "Negative"},
    {"role": "user", "content": "Works exactly as expected."},
    {"role": "assistant", "content": "Positive"},
    {"role": "user", "content": "Shipping was delayed by a week."},
]
print(chat(client, messages, temperature=0, max_tokens=300))
