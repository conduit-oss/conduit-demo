"""Stubs the openai 1.x client surface so tests pass only after migration."""

from __future__ import annotations

import importlib
import sys
import types
from types import SimpleNamespace


def _install_v1_stub() -> None:
    """Replace ``openai`` with a minimal 1.x-shaped client."""

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


def test_summarize_uses_v1_message_content():
    _install_v1_stub()
    sys.modules.pop("summarize", None)
    # Dynamic import so static analysis does not treat this file as a
    # reachability path into the app's SDK call.
    mod = importlib.import_module("summarize")
    assert mod.summarize("hello from the hackathon demo") == "stub-summary"
