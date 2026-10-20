"""Legacy Anthropic text completions API (removed in anthropic 1.0)."""

from __future__ import annotations

import anthropic


def complete(prompt: str, api_key: str) -> str:
    client = anthropic.Anthropic(api_key=api_key)
    resp = client.completions.create(
        model="claude-2.1",
        max_tokens_to_sample=64,
        prompt=f"{anthropic.HUMAN_PROMPT} {prompt}{anthropic.AI_PROMPT}",
    )
    return resp.completion


if __name__ == "__main__":
    print(complete("Say hi", api_key="sk-test"))
