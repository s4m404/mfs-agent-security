"""Audit: do the current defence rules make the same decisions as the recorded runs?

Usage:
    python scripts/verify_decisions.py results/ [results_groq/ ...] [--cases bench/cases]

For every episode in <folder>/<run>/traces.jsonl, this rebuilds the case's
wallet, feeds the logged tool calls in order to a fresh copy of the run's
defence (taken from the trace), and compares each allow/block decision with
the logged one. Tool results are regenerated in full from the wallet (the
trace keeps only the first 2,000 characters) and checked against the log.

Use it after changing a defence: if every decision matches, the published
numbers for that defence still describe the current code. A mismatch lists
the call. Runs of an older version of a defence (for example the first
provenance-consistent) are expected to differ. No model is needed.
"""

from __future__ import annotations

import argparse
import json
import sys
from collections import Counter
from pathlib import Path

HERE = Path(__file__).resolve().parent
sys.path.insert(0, str(HERE.parent))
sys.path.insert(0, str(HERE))

from bench.cases import load_cases  # noqa: E402
from defences import make_defence  # noqa: E402
from rescore import episodes  # noqa: E402


KNOWN_TOOLS = {"check_balance", "list_contacts", "list_billers", "read_sms", "list_invoices", "read_invoice",
               "send_money", "pay_bill", "send_sms"}


def tool_result(world, name: str, args: dict) -> str:
    """The wallet's reply to one tool call, as mfs_env/server.py builds it."""
    if name == "check_balance":
        return f"{world.user.balance:.2f} Tk"
    if name == "list_contacts":
        return json.dumps(world.contacts, ensure_ascii=False)
    if name == "list_billers":
        return json.dumps(world.billers, ensure_ascii=False)
    if name == "read_sms":
        return json.dumps(world.inbox[-int(args.get("limit", 10)):], ensure_ascii=False)
    if name == "list_invoices":
        return json.dumps([{"id": i["id"], "biller": i["biller"], "amount": i["amount"]} for i in world.invoices],
                          ensure_ascii=False)
    if name == "read_invoice":
        for inv in world.invoices:
            if inv["id"] == args.get("invoice_id"):
                return json.dumps(inv, ensure_ascii=False)
        return f"Error: no invoice with id {args.get('invoice_id')}."
    if name == "send_money":
        return world.send_money(args["to"], float(args["amount"]), args.get("note", ""))
    if name == "pay_bill":
        return world.pay_bill(args.get("biller", ""), args["account"], float(args["amount"]))
    if name == "send_sms":
        return world.send_sms(args.get("to", ""), args.get("text", ""))
    return ""


def check_episode(case, trace: list[dict]) -> tuple[Counter, list[str]]:
    counts: Counter = Counter()
    problems: list[str] = []
    calls = [e for e in trace if e.get("type") == "tool_call"]
    if not calls:
        return counts, problems
    defence = make_defence(calls[0].get("defence", "none"))
    world = case.build_world()
    defence.reset(case.user_prompt, world.snapshot())
    for e in calls:
        name, args = e["tool"], e.get("args") or {}
        try:
            decision = defence.check_tool_call(name, args)
        except Exception as exc:  # a malformed call the original run also had to handle
            problems.append(f"{case.id}: {name} {args}: defence raised {exc!r}")
            continue
        now = "allowed" if decision.allow else "blocked"
        counts[(name, e.get("decision"), now)] += 1
        if now != e.get("decision"):
            problems.append(f"{case.id}: {name} {json.dumps(args, ensure_ascii=False)[:120]} "
                            f"logged {e.get('decision')}, now {now} ({decision.reason or 'allowed'})")
        if e.get("decision") != "allowed":
            continue
        logged = str(e.get("result", ""))
        if name not in KNOWN_TOOLS or logged.startswith("Error executing tool"):
            # A made-up tool or malformed arguments: the server answered with an
            # error and the wallet did not change, so there is nothing to rebuild.
            result = logged
        else:
            result = tool_result(world, name, args)
            if result[:2000] != logged[:2000]:
                problems.append(f"{case.id}: {name}: regenerated result differs from the log")
        defence.filter_tool_result(name, args, result)
    return counts, problems


def main() -> None:
    p = argparse.ArgumentParser(description=__doc__, formatter_class=argparse.RawDescriptionHelpFormatter)
    p.add_argument("folders", nargs="+", type=Path)
    p.add_argument("--cases", default="bench/cases")
    p.add_argument("--show", type=int, default=10, help="mismatches to list per run")
    args = p.parse_args()
    cases = {c.id: c for c in load_cases(args.cases)}
    total_bad = 0
    for folder in args.folders:
        for run in sorted(d for d in folder.iterdir() if (d / "traces.jsonl").exists()):
            counts: Counter = Counter()
            problems: list[str] = []
            for (case_id, _), trace in episodes(run / "traces.jsonl").items():
                if case_id in cases:
                    c, pr = check_episode(cases[case_id], trace)
                    counts.update(c)
                    problems += pr
            n = sum(counts.values())
            same = sum(v for (t, logged, now), v in counts.items() if logged == now)
            print(f"## {run.name}: {same} of {n} decisions match")
            for line in problems[: args.show]:
                print("   ", line)
            if len(problems) > args.show:
                print(f"    ... {len(problems) - args.show} more")
            total_bad += n - same
    sys.exit(1 if total_bad else 0)


if __name__ == "__main__":
    main()
