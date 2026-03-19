"""LLM provider abstraction.

Supports OpenAI-compatible APIs out of the box.  To add a new provider,
implement ``LLMProvider`` and pass the instance to ``execute_planning_flow``.
"""

from __future__ import annotations

import importlib
import logging
import os
from typing import Any, Protocol

logger = logging.getLogger("auto-ppt")


class LLMProvider(Protocol):
    """Minimal interface every LLM backend must satisfy."""

    def chat(self, system_prompt: str, user_prompt: str) -> str:
        """Return the raw text completion for the given prompts."""
        ...


class OpenAIProvider:
    """Provider backed by any OpenAI-compatible endpoint.

    Automatically adapts API parameters for reasoning models (o1, o3, o4-mini,
    codex-mini-latest, etc.) which require ``developer`` role instead of
    ``system`` and do not accept ``temperature``.
    """

    # Prefixes that identify reasoning / codex models.
    _REASONING_PREFIXES = ("o1", "o3", "o4", "codex")

    def __init__(
        self,
        api_key: str | None = None,
        base_url: str | None = None,
        model: str | None = None,
    ) -> None:
        OpenAI = importlib.import_module("openai").OpenAI

        resolved_key = api_key or os.getenv("OPENAI_API_KEY")
        if not resolved_key:
            raise RuntimeError(
                "OPENAI_API_KEY is not set. Use mock mode for offline testing or configure the API key."
            )
        self._client: Any = OpenAI(
            api_key=resolved_key,
            base_url=base_url or os.getenv("OPENAI_BASE_URL") or None,
        )
        self._model = model or os.getenv("OPENAI_MODEL") or "gpt-4.1-mini"

    def _is_reasoning_model(self) -> bool:
        return self._model.startswith(self._REASONING_PREFIXES)

    def chat(self, system_prompt: str, user_prompt: str) -> str:
        logger.info("Requesting deck JSON from model=%s", self._model)
        reasoning = self._is_reasoning_model()

        # Reasoning models use "developer" role; standard models use "system".
        instruction_role = "developer" if reasoning else "system"
        messages = [
            {"role": instruction_role, "content": system_prompt},
            {"role": "user", "content": user_prompt},
        ]

        params: dict[str, Any] = {
            "model": self._model,
            "response_format": {"type": "json_object"},
            "messages": messages,
        }

        if reasoning:
            # Reasoning models ignore temperature; optionally set effort.
            effort = os.getenv("OPENAI_REASONING_EFFORT", "medium")
            params["reasoning_effort"] = effort
        else:
            params["temperature"] = 0.3

        response = self._client.chat.completions.create(**params)
        content = response.choices[0].message.content if response.choices else None
        if not content:
            raise RuntimeError("Model returned no content.")
        return str(content)


def get_default_provider() -> LLMProvider:
    """Return the default provider based on environment variables."""
    return OpenAIProvider()
