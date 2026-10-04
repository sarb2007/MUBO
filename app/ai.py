import requests


def ask_local_ai(message: str, max_tokens: int = 250) -> str:
    """Send a message to the local model running in LM Studio."""

    url = "http://127.0.0.1:1234/v1/chat/completions"

    data = {
        "model": "local-model",
        "messages": [
            {
                "role": "system",
                "content": (
                    "You are MUBO, a local AI coding assistant. "
                    "Keep answers short, clear, and practical. "
                    "When reviewing code, identify bugs, risks, and useful improvements."
                ),
            },
            {
                "role": "user",
                "content": message,
            },
        ],
        "temperature": 0.2,
        "max_tokens": max_tokens,
    }

    response = requests.post(url, json=data)

    response.raise_for_status()

    result = response.json()

    return result["choices"][0]["message"]["content"]