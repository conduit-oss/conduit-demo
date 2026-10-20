"""Legacy Anthropic text completions API (removed in anthropic 1.0)."""

from __future__ import annotations

import anthropic


def complete(prompt: str, api_key: str) -> str:
    client = anthropic.Anthropic(api_key=api_key)
    message = client.messages.create(
        model="claude-3-haiku-20240307",
        max_tokens=64,
        messages=[{"role": "user", "content": prompt}]
    )
    return message.content[0].text


if __name__ == "__main__":
    print(complete("Say hi", api_key="sk-test"))
