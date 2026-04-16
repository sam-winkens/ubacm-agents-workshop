# llm.py
# The only file that knows about the network.
# call_llm() sends a request to the instructor's n8n webhook (PROXY_URL),
# which forwards it to Claude and returns the response.

import os
import requests
from dotenv import load_dotenv

load_dotenv()

PROXY_URL = os.getenv("PROXY_URL")
MODEL = "claude-haiku-4-5-20251001"


def call_llm(messages: list[dict], tools: list[dict] = None, system: str = None) -> dict:
    """
    Send messages to Claude via the instructor's n8n proxy.
    Returns the raw Anthropic API response as a dict.
    """
    if not PROXY_URL:
        raise EnvironmentError("PROXY_URL is not set. Copy .env.example to .env and fill it in.")

    payload = {
        "model": MODEL,
        "max_tokens": 1024,
        "messages": messages,
    }
    if system:
        payload["system"] = system
    if tools:
        payload["tools"] = tools

    response = requests.post(PROXY_URL, json=payload, timeout=30)
    response.raise_for_status()
    data = response.json()
    # n8n's "Respond to Webhook" node wraps the response in a list so we need to unwrap it.
    if isinstance(data, list):
        data = data[0]
    return data
