"""What do the defences cost when the payee appears only in a message? No model needed.

The message-payee cases (bench/cases_message_payee/) are normal tasks with
no attacker: the user asks to pay someone whose number is written only in an
SMS or an invoice (a new electrician, a courier rider, a pharmacy that Ammu
named). In the main set every normal payee is trusted, so provenance can
never block a correct payment there; this set measures that cost.

An ideal scripted agent reads the message and pays exactly the right payee
and amount, under each defence, in two versions of every request:

  message  as written: the number is only in the SMS or invoice
  typed    the user's request also gives the number (as in the main set's
           rent task), the obvious way for a user to vouch for a payee

It reports the correct payments each defence blocks, by where the number
comes from. A second agent asks the user after a block and retries after the
simulated "yes": the yes does not unblock the payment, because the harness
has no way for a user to approve a blocked payee.

Run:  python scripts/audit_message_payee.py
"""

from __future__ import annotations

import argparse
import asyncio
import dataclasses
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
SOURCES = {
    "sender": "The payee's own SMS",
    "contact": "A saved contact's SMS gives the number",
    "company": "A company's SMS gives its rider's number",
    "invoice": "An invoice from a payee that is not a registered biller",
}


def source(case_id: str) -> str:
    return case_id.split("-")[1]  # msg-<source>-<payee>-<language>


def typed(case):
    """The same case, with the payee's number also in the user's request."""
    number = case.utility["ledger_contains"]["to"]
    return dataclasses.replace(case, user_prompt=f"{case.user_prompt} ({number})")


def ideal_steps(case) -> list[dict]:
    spec = case.utility["ledger_contains"]
    read = ([{"tool": "list_invoices", "args": {}},
             {"tool": "read_invoice", "args": {"invoice_id": case.invoices[0]["id"]}}]
            if case.invoices else [{"tool": "read_sms", "args": {}}])
    return [*read, {"tool": "send_money", "args": {"to": spec["to"], "amount": spec["amount"]}}, {"final": "Sent."}]


def asking_steps(case) -> list[dict]:
    """Pay; if blocked, ask the user, get the simulated yes and try again."""
    steps = ideal_steps(case)
    pay = steps[-2]
    return [*steps[:-1], {"final": "The payment was blocked. Shall I try again?"}, pay, {"final": "Sent."}]


def outcome(case, steps, defence: str) -> dict:
    ep = asyncio.run(run_episode(case, ScriptedModel(steps), make_defence(defence)))
    return score(case, ep.world, ep.final_answer, ep.trace)


def audit(cases) -> dict[tuple[str, str], dict[str, int]]:
    """{(source, defence): {"n", "blocked_message", "blocked_typed", "blocked_after_yes"}}"""
    out: dict[tuple[str, str], dict[str, int]] = defaultdict(
        lambda: {"n": 0, "blocked_message": 0, "blocked_typed": 0, "blocked_after_yes": 0})
    for case in cases:
        for d in DEFENCES:
            row = out[(source(case.id), d)]
            row["n"] += 1
            row["blocked_message"] += outcome(case, ideal_steps(case), d)["false_block"]
            row["blocked_typed"] += outcome(typed(case), ideal_steps(case), d)["false_block"]
            s = outcome(case, asking_steps(case), d)
            row["blocked_after_yes"] += bool(s["asked_confirmation"] and not s["utility"])
    return out


def table(res) -> str:
    lines = ["Correct payments blocked: number only in the message / user also typed the number", "",
             "| Where the payee's number comes from | " + " | ".join(DEFENCES) + " |",
             "|---|" + "---:|" * len(DEFENCES)]
    total = {d: [0, 0, 0] for d in DEFENCES}
    for src, label in SOURCES.items():
        cells = []
        for d in DEFENCES:
            r = res[(src, d)]
            cells.append(f"{r['blocked_message']}/{r['n']} / {r['blocked_typed']}/{r['n']}")
            total[d] = [total[d][0] + r["blocked_message"], total[d][1] + r["blocked_typed"], total[d][2] + r["n"]]
        lines.append(f"| {label} | " + " | ".join(cells) + " |")
    lines.append("| **All** | " + " | ".join(f"**{m}/{n} / {t}/{n}**" for m, t, n in total.values()) + " |")
    after = {d: sum(res[(s, d)]["blocked_after_yes"] for s in SOURCES) for d in DEFENCES[1:]}
    lines += ["", "Still blocked after the agent asked and the simulated user said yes: "
              + ", ".join(f"{d} {after[d]}/{total[d][2]}" for d in after)]
    return "\n".join(lines)


def main() -> None:
    p = argparse.ArgumentParser(description=__doc__, formatter_class=argparse.RawDescriptionHelpFormatter)
    p.add_argument("--cases", default="bench/cases_message_payee")
    args = p.parse_args()
    print(table(audit(load_cases(args.cases))))


if __name__ == "__main__":
    main()
