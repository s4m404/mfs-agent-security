"""Defences that sit between the agent and the wallet tools.

Each defence sees every tool result before the model does, and every tool
call before it runs. Add new defences here and register them in DEFENCES.
"""

from __future__ import annotations

from .base import Decision, Defence
from .keyword import KeywordDetector
from .provenance import ProvenancePolicy

DEFENCES: dict[str, type[Defence]] = {
    "none": Defence,
    "keyword": KeywordDetector,
    "provenance": ProvenancePolicy,
}


def make_defence(name: str) -> Defence:
    try:
        return DEFENCES[name]()
    except KeyError as exc:
        raise ValueError(f"Unknown defence {name!r}. Choose from {sorted(DEFENCES)}") from exc


__all__ = ["Decision", "Defence", "DEFENCES", "make_defence"]
