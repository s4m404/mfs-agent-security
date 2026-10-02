"""Provenance policy (version 0): track where values came from.

Rules
1. send_money: the recipient must be a saved contact or appear in the
   user's own request. Numbers that only appear in untrusted content
   (SMS, invoices, tool descriptions) need explicit human approval.
2. pay_bill: the biller account must be a registered biller.
3. send_sms: the recipient must be trusted, and the text must not contain
   any numeric code that was read from untrusted content (blocks OTP leaks).

The trade off to measure: when a user legitimately asks to pay a number
found in an SMS, this policy blocks it. That is a utility cost, and it
belongs in the results table.
"""

from __future__ import annotations

import json
import re
from typing import Any

from mfs_env.server import UNTRUSTED_TOOLS
from mfs_env.text import extract_numbers, normalise_number, normalise_text
from mfs_env.world import World

from .base import Decision, Defence

_CODE_RE = re.compile(r"\b\d{4,8}\b")


class ProvenancePolicy(Defence):
    name = "provenance"

    def reset(self, user_prompt: str, world: World) -> None:
        self.trusted_numbers = set(world.contacts.values()) | extract_numbers(user_prompt)
        self.biller_accounts = set(world.billers.values())
        self.untrusted_codes: set[str] = set()

    def filter_tool_result(self, tool: str, args: dict[str, Any], result: str) -> str:
        if tool in UNTRUSTED_TOOLS:
            self.untrusted_codes |= set(_CODE_RE.findall(normalise_text(result)))
        return result

    def check_tool_call(self, tool: str, args: dict[str, Any]) -> Decision:
        if tool == "send_money":
            to = normalise_number(args.get("to", ""))
            if to not in self.trusted_numbers:
                return Decision(False, f"recipient {to} is not a saved contact and was not named by the user")
        elif tool == "pay_bill":
            account = normalise_number(args.get("account", ""))
            if account not in self.biller_accounts:
                return Decision(False, f"account {account} is not a registered biller")
        elif tool == "send_sms":
            to = normalise_number(args.get("to", ""))
            if to not in self.trusted_numbers:
                return Decision(False, f"SMS recipient {to} is not trusted")
            codes = set(_CODE_RE.findall(normalise_text(args.get("text", ""))))
            if codes & self.untrusted_codes:
                return Decision(False, "SMS text contains a code read from untrusted content")
        return Decision(True)


_AMOUNT_RE = re.compile(r"\d[\d,]*(?:\.\d+)?")


def _amounts(text: str) -> set[float]:
    out = set()
    for m in _AMOUNT_RE.findall(normalise_text(text)):
        try:
            out.add(round(float(m.replace(",", "")), 2))
        except ValueError:
            pass
    return out


class ProvenanceAmountPolicy(ProvenancePolicy):
    """Provenance for amounts as well as recipients (version 1).

    Extra rule on top of version 0: a payment amount must come from the user
    or from the payee itself.
      - send_money: the amount is in the user's request, or in an SMS sent
        from the recipient's own number ("Rafi asked for 450").
      - pay_bill: the amount is in the user's request, or on an invoice for
        that same registered biller account.
    This catches guessed amounts (paying the right biller 500 instead of 1850)
    and attacks that change only the amount.
    """

    name = "provenance-amount"

    def reset(self, user_prompt: str, world: World) -> None:
        super().reset(user_prompt, world)
        self.user_amounts = _amounts(user_prompt)
        self.biller_by_name = {normalise_text(n): normalise_number(a) for n, a in world.billers.items()}
        self.amounts_from: dict[str, set[float]] = {}

    def _add(self, key: str, value: Any) -> None:
        if key:
            self.amounts_from.setdefault(key, set()).update(_amounts(str(value)))

    def filter_tool_result(self, tool: str, args: dict[str, Any], result: str) -> str:
        result = super().filter_tool_result(tool, args, result)
        try:
            data = json.loads(result)
        except (TypeError, ValueError):
            return result
        items = data if isinstance(data, list) else [data]
        for item in items:
            if not isinstance(item, dict):
                continue
            if tool == "read_sms":
                self._add(normalise_number(str(item.get("from", ""))), item.get("text", ""))
            elif tool in ("list_invoices", "read_invoice"):
                account = normalise_number(str(item.get("account", ""))) or self.biller_by_name.get(
                    normalise_text(str(item.get("biller", ""))), ""
                )
                self._add(account, item.get("amount", ""))
        return result

    def check_tool_call(self, tool: str, args: dict[str, Any]) -> Decision:
        decision = super().check_tool_call(tool, args)
        if not decision.allow or tool not in ("send_money", "pay_bill"):
            return decision
        payee = normalise_number(str(args.get("to") if tool == "send_money" else args.get("account", "")))
        try:
            amount = round(float(args.get("amount", 0)), 2)
        except (TypeError, ValueError):
            return Decision(False, "amount is not a number")
        if amount in self.user_amounts or amount in self.amounts_from.get(payee, set()):
            return Decision(True)
        return Decision(False, f"amount {amount:g} Tk was not given by the user or by the payee {payee}")
