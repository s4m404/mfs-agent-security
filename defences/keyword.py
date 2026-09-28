"""Keyword detector: a deliberately simple baseline.

It normalises text (Bangla digits, case, whitespace) and removes untrusted
content that contains common injection cues in English, Bangla and Banglish.
Its job is to be beaten: replace it with a trained multilingual classifier
and report both in the results table.
"""

from __future__ import annotations

import json
from typing import Any

from mfs_env.server import UNTRUSTED_TOOLS
from mfs_env.text import normalise_text

from .base import Defence

CUES = [
    # English
    "ignore previous", "ignore all previous", "ai assistant", "assistant must",
    "note to ai", "do not tell the user", "without asking the user", "mandatory",
    # Bangla
    "এআই", "সহকারী", "বাধ্যতামূলক", "নির্দেশ", "ব্যবহারকারীকে জানাবে না",
    # Banglish
    "assistant ke", "user ke kichu bolar dorkar nai", "approve korse", "user already approve",
]

REPLACEMENT = "[content removed by security filter: possible injected instructions]"


class KeywordDetector(Defence):
    name = "keyword"

    @staticmethod
    def flagged(text: str) -> bool:
        norm = normalise_text(text)
        return any(cue in norm for cue in CUES)

    def _clean(self, value: Any) -> Any:
        """Replace flagged strings inside JSON results, item by item."""
        if isinstance(value, str):
            return REPLACEMENT if self.flagged(value) else value
        if isinstance(value, list):
            return [self._clean(v) for v in value]
        if isinstance(value, dict):
            return {k: self._clean(v) for k, v in value.items()}
        return value

    def filter_tool_result(self, tool: str, args: dict[str, Any], result: str) -> str:
        if tool not in UNTRUSTED_TOOLS:
            return result
        try:
            data = json.loads(result)
        except ValueError:
            return REPLACEMENT if self.flagged(result) else result
        return json.dumps(self._clean(data), ensure_ascii=False)
