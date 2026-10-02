"""Benchmark case format and loader. See bench/SCHEMA.md."""

from __future__ import annotations

from dataclasses import dataclass, field
from pathlib import Path
from typing import Any

import yaml

from mfs_env.world import World, default_world

VECTORS = {"none", "sms", "invoice", "tool_description"}
LANGS = {"en", "bn", "banglish", "mixed"}
GOALS = {"send_money", "exfiltrate_otp", "overpay"}


@dataclass
class Case:
    id: str
    user_prompt: str
    task_language: str
    injection_vector: str = "none"
    injection_language: str | None = None
    injection_style: str | None = None  # agent_directive | social_scam
    inbox: list[dict[str, Any]] = field(default_factory=list)
    invoices: list[dict[str, Any]] = field(default_factory=list)
    description_overrides: dict[str, str] = field(default_factory=dict)
    billers: dict[str, str] = field(default_factory=dict)  # extra registered billers: name -> account
    contacts: dict[str, str] = field(default_factory=dict)  # extra saved contacts: name -> number
    utility: dict[str, Any] = field(default_factory=dict)
    attack: dict[str, Any] | None = None

    @property
    def is_attack(self) -> bool:
        return self.attack is not None

    def build_world(self) -> World:
        w = default_world()
        w.inbox.extend(self.inbox)
        w.invoices.extend(self.invoices)
        w.billers.update(self.billers)
        w.contacts.update(self.contacts)
        return w


def _validate(c: Case) -> None:
    if c.injection_vector not in VECTORS:
        raise ValueError(f"{c.id}: unknown injection_vector {c.injection_vector!r}")
    if c.task_language not in LANGS:
        raise ValueError(f"{c.id}: unknown task_language {c.task_language!r}")
    if (c.injection_vector == "none") != (c.attack is None):
        raise ValueError(f"{c.id}: attack must be set exactly when injection_vector is not 'none'")
    if c.attack and c.attack.get("goal") not in GOALS:
        raise ValueError(f"{c.id}: unknown attack goal {c.attack.get('goal')!r}")
    if c.attack and c.attack["goal"] == "overpay" and "amount" not in c.attack:
        raise ValueError(f"{c.id}: an overpay attack needs an amount")


def load_cases(path: str | Path) -> list[Case]:
    paths = sorted(Path(path).glob("*.yaml")) if Path(path).is_dir() else [Path(path)]
    cases: list[Case] = []
    for p in paths:
        for raw in yaml.safe_load(p.read_text(encoding="utf-8")) or []:
            c = Case(**raw)
            _validate(c)
            cases.append(c)
    ids = [c.id for c in cases]
    dupes = {i for i in ids if ids.count(i) > 1}
    if dupes:
        raise ValueError(f"duplicate case ids: {sorted(dupes)}")
    return cases
