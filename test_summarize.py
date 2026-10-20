"""Stubs the openai 1.x client surface so tests pass only after migration."""

from __future__ import annotations

import sys
import types
from types import SimpleNamespace


def _install_v1_stub() -> None:
    """Replace ``openai`` with a minimal 1.x-shaped client (no ChatCompletion)."""

    def create(**_kwargs):
        return SimpleNamespace(
            choices=[SimpleNamespace(message=SimpleNamespace(content="stub-summary"))]
        )

    chat = SimpleNamespace(completions=SimpleNamespace(create=create))

    class OpenAI:
        def __init__(self, *args, **kwargs):
            self.chat = chat

    mod = types.ModuleType("openai")
    mod.OpenAI = OpenAI
    sys.modules["openai"] = mod


_install_v1_stub()

if "summarize" in sys.modules:
    del sys.modules["summarize"]

from summarize import summarize  # noqa: E402


def test_summarize_uses_v1_message_content():
    assert summarize("hello from the hackathon demo") == "stub-summary"
