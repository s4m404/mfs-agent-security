"""Model adapters.

Every model returns one assistant turn as a dict:
    {"content": str | None, "tool_calls": [{"id": str, "name": str, "arguments": dict}]}

OpenAICompatModel talks to any OpenAI compatible endpoint, which covers:
- Ollama on a laptop:        base_url=http://localhost:11434/v1
- vLLM on the university HPC: base_url=http://<node>:8000/v1
- Hosted APIs that speak the same protocol.

ScriptedModel replays fixed steps, so the whole pipeline can be tested
without any model at all.
"""

from __future__ import annotations

import json
import os
from typing import Any, Protocol


class ChatModel(Protocol):
    name: str

    def complete(self, messages: list[dict[str, Any]], tools: list[dict[str, Any]]) -> dict[str, Any]: ...


class OpenAICompatModel:
    def __init__(
        self,
        model: str,
        base_url: str,
        api_key_env: str = "OPENAI_API_KEY",
        temperature: float = 0.0,
        max_tokens: int = 1024,
        timeout: float = 300.0,
    ):
        from openai import OpenAI  # imported lazily so tests do not need it

        self.name = model
        self.temperature = temperature
        # Small models sometimes get stuck repeating one word until the context
        # is full. A cap on reply length stops that quickly; a real reply in this
        # benchmark is a few hundred tokens at most.
        self.max_tokens = max_tokens
        self.client = OpenAI(
            base_url=base_url, api_key=os.environ.get(api_key_env, "not-needed"), timeout=timeout, max_retries=1
        )

    def complete(self, messages: list[dict[str, Any]], tools: list[dict[str, Any]]) -> dict[str, Any]:
        resp = self.client.chat.completions.create(
            model=self.name,
            messages=messages,
            tools=tools,
            temperature=self.temperature,
            max_tokens=self.max_tokens,
        )
        msg = resp.choices[0].message
        calls = []
        for tc in msg.tool_calls or []:
            try:
                args = json.loads(tc.function.arguments or "{}")
            except json.JSONDecodeError:
                args = {"_raw": tc.function.arguments}
            calls.append({"id": tc.id, "name": tc.function.name, "arguments": args})
        return {"content": msg.content, "tool_calls": calls}


class ScriptedModel:
    """Replays a list of steps: {"tool": name, "args": {...}} or {"final": text}."""

    def __init__(self, steps: list[dict[str, Any]], name: str = "scripted"):
        self.name = name
        self.steps = list(steps)
        self.i = 0

    def complete(self, messages: list[dict[str, Any]], tools: list[dict[str, Any]]) -> dict[str, Any]:
        if self.i >= len(self.steps):
            return {"content": "Done.", "tool_calls": []}
        step = self.steps[self.i]
        self.i += 1
        if "final" in step:
            return {"content": step["final"], "tool_calls": []}
        return {
            "content": None,
            "tool_calls": [{"id": f"call_{self.i}", "name": step["tool"], "arguments": step.get("args", {})}],
        }
