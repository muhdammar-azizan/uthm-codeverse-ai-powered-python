"""Zero-shot: ask directly, with no examples."""

from groq_client import chat, require_client

client = require_client()
messages = [
    {
        "role": "user",
        "content": "Is this review positive or negative? 'The battery life is amazing!' "
        "Answer with one word.",
    }
]
print(chat(client, messages, max_tokens=300))
