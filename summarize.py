"""Tiny app stuck on the openai 0.28 ChatCompletion API."""

from __future__ import annotations

import openai


def summarize(text: str) -> str:
    client = openai.OpenAI()
    resp = client.chat.completions.create(
        model="gpt-3.5-turbo",
        messages=[{"role": "user", "content": f"Summarize:\n{text}"}]
    )
    return resp.choices[0].message.content


if __name__ == "__main__":
    print(summarize("Conduit catches SDK breaks and proposes verified fixes."))
