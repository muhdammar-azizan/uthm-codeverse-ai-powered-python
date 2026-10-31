# AI Study Assistant

A small command-line app that turns a tech topic into a beginner-friendly study card. Type something like `recursion` and it gives you a short explanation, common uses, a commented code example, key points and a few quiz questions. It uses the Groq API with the open-weight `openai/gpt-oss-120b` model.

This is based on the mini project from the UTHM CodeVerse Week 2 workshop (AI-Powered Python) by Rynet Malaysia. The workshop slides and example code are theirs and are not included here; this code is my own implementation.

## Features

- Interactive loop: enter a topic, get a study card, type `quit` to leave
- Or run one topic straight from the command line
- Card sections: Explanation, Common Uses, Example, Key Points, Quiz
- The prompt lives in one function (`build_messages`) so it is easy to change
- Friendly messages instead of tracebacks for a missing key, no internet, a rejected key, and rate limits (HTTP 429)

## Requirements

- Python 3.10 or newer
- A free Groq API key from the [Groq console](https://console.groq.com)

## Setup (Windows PowerShell)

```powershell
python -m venv .venv
.\.venv\Scripts\Activate.ps1
pip install -r requirements.txt
Copy-Item .env.example .env
```

Open `.env` in an editor and put your key after `GROQ_API_KEY=`.

## Run

```powershell
python study_assistant.py
```

Or for a single topic:

```powershell
python study_assistant.py "REST API"
```

If you hit a rate limit, wait a few seconds and try again. Free-tier limits can change, so check the Groq docs if something looks off.

## Security notes

- Never commit `.env`. It is already in `.gitignore`; only `.env.example` (with no key in it) is tracked.
- Keep your key private: don't paste it into chats, screenshots or issues.
- If a key ever leaks, delete it in the Groq console and create a new one.

## License

License: not decided yet.
