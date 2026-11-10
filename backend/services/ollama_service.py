
"""Ollama integration service."""

import os

import ollama
from dotenv import load_dotenv

load_dotenv()

OLLAMA_MODEL = os.getenv("OLLAMA_MODEL", "llama3.2")

OLLAMA_BASE_URL = os.getenv(
    "OLLAMA_BASE_URL",
    "http://localhost:11434",
)

OLLAMA_API_KEY = os.getenv("OLLAMA_API_KEY")

FRONTEND_URL = os.getenv(
    "FRONTEND_URL",
    "http://localhost:5173",
)

# Configure client for local Ollama or Ollama Cloud
if OLLAMA_API_KEY:
    client = ollama.Client(
        host=OLLAMA_BASE_URL,
        headers={
            "Authorization": f"Bearer {OLLAMA_API_KEY}"
        },
    )
else:
    client = ollama.Client(host=OLLAMA_BASE_URL)


def generate_structured_response(
    system_prompt: str,
    user_prompt: str,
    output_schema: dict,
) -> str:

    response = client.chat(
        model=OLLAMA_MODEL,
        messages=[
            {
                "role": "system",
                "content": system_prompt,
            },
            {
                "role": "user",
                "content": user_prompt,
            },
        ],
        format=output_schema,
        options={
            "temperature": 0.2,
        },
    )

    return response.message.content


def check_connection() -> bool:
    try:
        # Test connection by sending a small request
        response = client.chat(
            model=OLLAMA_MODEL,
            messages=[
                {
                    "role": "user",
                    "content": "Reply with OK",
                }
            ],
        )
        return bool(response.message.content)

    except Exception as e:
        print(f"Ollama connection failed: {e}")
        return False