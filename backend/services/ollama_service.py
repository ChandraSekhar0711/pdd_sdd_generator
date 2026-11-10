"""Ollama integration service for local Ollama and Ollama Cloud."""

import json
import os
import re

import ollama
from dotenv import load_dotenv

load_dotenv()

OLLAMA_MODEL = os.getenv("OLLAMA_MODEL", "llama3.2")
OLLAMA_BASE_URL = os.getenv("OLLAMA_BASE_URL", "http://localhost:11434").rstrip("/")
OLLAMA_API_KEY = os.getenv("OLLAMA_API_KEY")
FRONTEND_URL = os.getenv("FRONTEND_URL", "http://localhost:5173")

# For Ollama Cloud, configure OLLAMA_BASE_URL=https://ollama.com and
# OLLAMA_API_KEY in the Render service environment. For local development,
# leave the base URL at http://localhost:11434 and the API key unset.
client_headers = {}
if OLLAMA_API_KEY:
    client_headers["Authorization"] = f"Bearer {OLLAMA_API_KEY}"

client = ollama.Client(host=OLLAMA_BASE_URL, headers=client_headers)


def _clean_json_response(content: str) -> str:
    """Remove optional Markdown fences around a model's JSON response."""
    content = content.strip()
    content = re.sub(r"^```(?:json)?\s*", "", content, flags=re.IGNORECASE)
    content = re.sub(r"\s*```$", "", content)
    return content.strip()


def generate_structured_response(
    system_prompt: str,
    user_prompt: str,
    output_schema: dict,
) -> str:
    """Generate JSON text using a prompt-embedded schema.

    Ollama Cloud currently does not support the native `format` JSON-schema
    parameter, so the schema is included in the instructions and the returned
    JSON should be validated by the application's existing Pydantic layer.
    """
    schema_instruction = (
        "Return exactly one valid JSON object and nothing else. "
        "Do not use Markdown fences or add explanatory text. "
        "Populate the response according to this JSON Schema. "
        "If source information is missing, use an empty value appropriate "
        "to the schema instead of inventing facts.\n\n"
        "JSON Schema:\n"
        f"{json.dumps(output_schema, ensure_ascii=False, indent=2)}"
    )

    response = client.chat(
        model=OLLAMA_MODEL,
        messages=[
            {
                "role": "system",
                "content": f"{system_prompt}\n\n{schema_instruction}",
            },
            {
                "role": "user",
                "content": user_prompt,
            },
        ],
        options={"temperature": 0.2},
    )

    content = response.message.content
    if not content:
        raise RuntimeError("Ollama returned an empty response.")

    return _clean_json_response(content)


def check_connection() -> bool:
    """Check connectivity and authentication against the configured Ollama host."""
    try:
        # The tags/list call checks the configured endpoint without generating
        # a paid inference request. Cloud API supports listing available models.
        client.list()
        return True
    except Exception as exc:
        print(f"Ollama connection failed: {type(exc).__name__}: {exc}")
        return False
