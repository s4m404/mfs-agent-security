"""Which defences stop the adaptive attacks? No model needed.

The adaptive cases (bench/cases_adaptive/) forge what provenance-amount
trusts: an SMS that appears to come from the payee's own number, or a
second invoice for the real biller account. This script plays two scripted
agents through every case under each defence:

  obeys   reads the attack and does exactly what it asks
  newest  obeys too, but reads only the newest SMS (read_sms with limit 1)
          or only the forged invoice, so it never sees the real amount;
          Qwen2.5-32B did this in real runs
  ideal   reads the real message or invoice and pays the correct amount

It reports how many attacks still succeed when the agent obeys, and whether
any defence blocks the ideal agent. This measures the defences themselves,
not how often a real model obeys; for that, run a model on the same cases
with scripts/run_bench.py --cases bench/cases_adaptive.

Run:  python scripts/audit_adaptive.py
"""

from __future__ import annotations

import argparse
import asyncio
import sys
from collections import defaultdict
from pathlib import Path

sys.path.insert(0, str(Path(__file__).resolve().parents[1]))

from agent.llm import ScriptedModel  # noqa: E402
from agent.runner import run_episode  # noqa: E402
from bench.cases import load_cases  # noqa: E402
from bench.score import score  # noqa: E402
from defences import make_defence  # noqa: E402

DEFENCES = ["none", "provenance", "provenance-amount", "provenance-consistent"]


def attack_type(case_id: str) -> str:
    return case_id.split("-")[1]  # adp-<type>-<task>-...


def obeying_steps(case) -> list[dict]:
    """Read the injected content, then do what the attack asks."""
    goal, target = case.attack["goal"], case.attack["target"]
    if case.injection_vector == "invoice":
        forged = case.invoices[-1]
        return [
            {"tool": "list_invoices", "args": {}},
            {"tool": "read_invoice", "args": {"invoice_id": forged["id"]}},
            {"tool": "pay_bill", "args": {"biller": forged["biller"], "account": target, "amount": case.attack["amount"]}},
            {"final": "Paid."},
        ]
    amount = case.attack["amount"] if goal == "overpay" else case.utility["ledger_contains"]["amount"]
    return [
        {"tool": "read_sms", "args": {}},
        {"tool": "send_money", "args": {"to": target, "amount": amount}},
        {"final": "Sent."},
    ]


def newest_steps(case) -> list[dict]:
    """Obey the attack after reading only the forged message or invoice."""
    steps = obeying_steps(case)
    if case.injection_vector == "invoice":
        return steps[1:]  # skip list_invoices: open the forged invoice directly
    return [{"tool": "read_sms", "args": {"limit": 1}}, *steps[1:]]


def ideal_steps(case) -> list[dict]:
    """Read everything, ignore the attack, pay the real amount to the real payee."""
    spec = case.utility["ledger_contains"]
    if spec["kind"] == "pay_bill":
        real = case.invoices[0]
        return [
            {"tool": "list_invoices", "args": {}},
            {"tool": "read_invoice", "args": {"invoice_id": real["id"]}},
            {"tool": "read_invoice", "args": {"invoice_id": case.invoices[-1]["id"]}},
            {"tool": "pay_bill", "args": {"biller": real["biller"], "account": spec["to"], "amount": spec["amount"]}},
            {"final": "Paid."},
        ]
    return [
        {"tool": "read_sms", "args": {}},
        {"tool": "send_money", "args": {"to": spec["to"], "amount": spec["amount"]}},
        {"final": "Sent."},
    ]


def audit(cases) -> dict[tuple[str, str], dict[str, int]]:
    """{(attack type, defence): {"n", "attack_success", "newest_success", "ideal_blocked"}}"""
    out: dict[tuple[str, str], dict[str, int]] = defaultdict(
        lambda: {"n": 0, "attack_success": 0, "newest_success": 0, "ideal_blocked": 0}
    )
    for case in cases:
        for d in DEFENCES:
            row = out[(attack_type(case.id), d)]
            ep = asyncio.run(run_episode(case, ScriptedModel(obeying_steps(case)), make_defence(d)))
            row["n"] += 1
            row["attack_success"] += score(case, ep.world, ep.final_answer, ep.trace)["attack_success"]
            ep = asyncio.run(run_episode(case, ScriptedModel(newest_steps(case)), make_defence(d)))
            row["newest_success"] += score(case, ep.world, ep.final_answer, ep.trace)["attack_success"]
            ep = asyncio.run(run_episode(case, ScriptedModel(ideal_steps(case)), make_defence(d)))
            s = score(case, ep.world, ep.final_answer, ep.trace)
            row["ideal_blocked"] += bool(s["false_block"] or not s["utility"])
    return out


LABELS = {
    "spoof_amount": "Fake SMS from the payee's number asks for more",
    "spoof_number": "Fake SMS from the payee's number gives a new number",
    "forged_invoice": "Forged revised invoice for the real biller account",
}


def main() -> None:
    p = argparse.ArgumentParser(description=__doc__, formatter_class=argparse.RawDescriptionHelpFormatter)
    p.add_argument("--cases", default="bench/cases_adaptive")
    args = p.parse_args()
    res = audit(load_cases(args.cases))
    print("Attacks that succeed when the agent obeys: reads everything / reads only the newest message")
    print("(in brackets: correct payments blocked for an ideal agent)\n")
    print("| Adaptive attack | " + " | ".join(DEFENCES) + " |")
    print("|---|" + "---:|" * len(DEFENCES))
    for t, label in LABELS.items():
        cells = [
            f"{r['attack_success']}/{r['n']} / {r['newest_success']}/{r['n']} ({r['ideal_blocked']})"
            for r in (res[(t, d)] for d in DEFENCES)
        ]
        print(f"| {label} | " + " | ".join(cells) + " |")


if __name__ == "__main__":
    main()
