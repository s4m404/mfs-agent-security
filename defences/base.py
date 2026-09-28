"""Defence interface. The base class allows everything (the "none" baseline)."""

from __future__ import annotations

from dataclasses import dataclass
from typing import Any

from mfs_env.world import World


@dataclass
class Decision:
    allow: bool
    reason: str = ""


class Defence:
    name = "none"

    def reset(self, user_prompt: str, world: World) -> None:
        """Called once at the start of every episode.

        `world` is a read only snapshot taken before the agent acts. A defence
        may use trusted state from it (contacts, registered billers) but must
        never peek at hidden values such as the OTP.
        """

    def filter_tool_result(self, tool: str, args: dict[str, Any], result: str) -> str:
        """Inspect or rewrite a tool result before the model sees it."""
        return result

    def check_tool_call(self, tool: str, args: dict[str, Any]) -> Decision:
        """Allow or block a tool call before it runs."""
        return Decision(True)
