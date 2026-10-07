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
import re
import time
from typing import Any, Protocol


class RateLimited(Exception):
    """The API's rate limit will not reset soon (for example a daily token limit).

    The runner does not score the case: the run stops, and --resume picks the
    case up again later.
    """


def retry_after_seconds(exc: Exception) -> float | None:
    """How long a 429 reply asks us to wait: the retry-after header, or
    "try again in 1m30.5s" in the message (as Groq writes it)."""
    headers = getattr(getattr(exc, "response", None), "headers", None) or {}
    try:
        return float(headers.get("retry-after"))
    except (TypeError, ValueError):
        pass
    m = re.search(r"try again in (?:(\d+)h)?(?:(\d+)m)?(?:([\d.]+)s)?", str(exc))
    if m and any(m.groups()):
        h, mi, s = (float(x) if x else 0.0 for x in m.groups())
        return h * 3600 + mi * 60 + s
    return None


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
        extra_body: dict[str, Any] | None = None,
        max_wait: float = 120.0,
        max_total_wait: float = 900.0,
    ):
        from openai import OpenAI  # imported lazily so tests do not need it

        self.name = model
        self.temperature = temperature
        # Small models sometimes get stuck repeating one word until the context
        # is full. A cap on reply length stops that quickly; a real reply in this
        # benchmark is a few hundred tokens at most.
        self.max_tokens = max_tokens
        # Provider-specific settings, e.g. {"reasoning_effort": "low"} on Groq.
        self.extra_body = extra_body or None
        # Rate limits. A per-minute limit asks for a short wait, often many times
        # in a row (Groq's free tier: 8,000 tokens a minute), so keep waiting, up
        # to max_total_wait seconds for one reply. A daily limit asks for a long
        # wait (more than max_wait): stop the run by raising RateLimited.
        self.max_wait = max_wait
        self.max_total_wait = max_total_wait
        self.client = OpenAI(
            base_url=base_url, api_key=os.environ.get(api_key_env, "not-needed"), timeout=timeout, max_retries=1
        )

    def _create(self, messages: list[dict[str, Any]], tools: list[dict[str, Any]]) -> Any:
        from openai import RateLimitError

        waited, attempt = 0.0, 0
        while True:
            try:
                return self.client.chat.completions.create(
                    model=self.name,
                    messages=messages,
                    tools=tools,
                    temperature=self.temperature,
                    max_tokens=self.max_tokens,
                    extra_body=self.extra_body,
                )
            except RateLimitError as exc:
                wait = retry_after_seconds(exc)
                wait = min(5.0 * 2**attempt, 60.0) if wait is None else wait + 1.0
                if wait > self.max_wait or waited + wait > self.max_total_wait:
                    raise RateLimited(str(exc)[:500]) from exc
                time.sleep(wait)
                waited += wait
                attempt += 1

    def complete(self, messages: list[dict[str, Any]], tools: list[dict[str, Any]]) -> dict[str, Any]:
        resp = self._create(messages, tools)
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
