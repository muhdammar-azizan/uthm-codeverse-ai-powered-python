"""Chain-of-thought: ask the model to show its steps on a small maths problem."""

from groq_client import chat, require_client

client = require_client()
messages = [
    {
        "role": "user",
        "content": "A shop had 84 apples and sold 3 boxes of 12. "
        "How many are left? Work it out step by step, then give the final number. Plain text only, no LaTeX or markdown.",
    }
]
print(chat(client, messages, max_tokens=800))
