"""Stubs the anthropic 1.x Messages surface so tests pass only after migration."""

from __future__ import annotations

import sys
import types
from types import SimpleNamespace


def _install_messages_stub() -> None:
    """Replace ``anthropic`` with a minimal Messages-API client (no Completions)."""

    def create(**_kwargs):
        return SimpleNamespace(
            content=[SimpleNamespace(text="stub-complete")],
        )

    class Anthropic:
        def __init__(self, *args, **kwargs):
            self.messages = SimpleNamespace(create=create)

    mod = types.ModuleType("anthropic")
    mod.Anthropic = Anthropic
    sys.modules["anthropic"] = mod


_install_messages_stub()

if "complete" in sys.modules:
    del sys.modules["complete"]

from complete import complete  # noqa: E402


def test_complete_uses_messages_text():
    assert complete("hello from the harder demo", api_key="sk-test") == "stub-complete"
