"""Replay recorded runs through a different defence, without a model.

Usage:
    python scripts/replay_defence.py results/MODEL__provenance__guarded provenance-amount

Feeds the logged tool calls and results of every episode into the new
defence and reports which money calls it would have blocked that the
original run allowed. This is a quick estimate before a real run: after a
block, a real agent would act differently, so only the first new block in
each episode is exact.
"""

from __future__ import annotations

import argparse
import collections
import json
import sys
from pathlib import Path

sys.path.insert(0, str(Path(__file__).resolve().parents[1]))

from bench.cases import load_cases  # noqa: E402
from bench.score import _call_as_transfer, _ledger_match_one  # noqa: E402
from defences import DEFENCES, make_defence  # noqa: E402


def main() -> None:
    p = argparse.ArgumentParser()
    p.add_argument("run_dir", type=Path)
    p.add_argument("defence", choices=sorted(DEFENCES))
    args = p.parse_args()

    cases = {c.id: c for c in load_cases("bench/cases")}
    episodes = collections.defaultdict(list)
    for line in open(args.run_dir / "traces.jsonl", encoding="utf-8"):
        e = json.loads(line)
        episodes[(e["case_id"], e.get("repeat", 0))].append(e)

    counts = collections.Counter()
    examples = []
    for (case_id, _), events in sorted(episodes.items()):
        case = cases[case_id]
        defence = make_defence(args.defence)
        defence.reset(case.user_prompt, case.build_world())
        expected = case.utility.get("ledger_contains")
        for e in events:
            if e.get("type") != "tool_call" or e.get("decision") == "blocked":
                continue
            if e["tool"] in ("send_money", "pay_bill", "send_sms"):
                decision = defence.check_tool_call(e["tool"], e["args"])
                if not decision.allow:
                    correct = bool(expected) and e["tool"] != "send_sms" and _ledger_match_one(_call_as_transfer(e), expected)
                    went_through = str(e.get("result", "")).startswith(("Success", "SMS sent"))
                    key = "correct action (would be a false block)" if correct else (
                        "wrong action that went through" if went_through else "wrong action the wallet rejected anyway")
                    counts[key] += 1
                    if correct or went_through:
                        examples.append((case_id, e["tool"], e["args"], decision.reason))
            if "result" in e:
                defence.filter_tool_result(e["tool"], e["args"], e["result"])

    print(f"Calls the original run allowed that {args.defence} would block:")
    for k, v in counts.most_common():
        print(f"  {k}: {v}")
    for ex in examples[:10]:
        print("  e.g.", *ex)


if __name__ == "__main__":
    main()
