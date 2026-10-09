"""Audit: re-score every episode from its raw trace and compare with scores.jsonl.

Usage:
    python scripts/rescore.py results/ [results_groq/ ...] [--cases bench/cases]

For each run folder (<folder>/<run>/traces.jsonl + scores.jsonl) this
rebuilds the case's wallet, replays every payment and SMS that the trace says
went through, scores the episode again with the current bench/score.py, and
lists every field that differs from the saved score. Then it prints the main
table (the same numbers as scripts/make_figures.py) recomputed from the
traces, so README numbers can be checked against raw data, not saved scores.

No model is needed. Exit code 1 if any saved score differs.
"""

from __future__ import annotations

import argparse
import json
import sys
from collections import defaultdict
from pathlib import Path

HERE = Path(__file__).resolve().parent
sys.path.insert(0, str(HERE.parent))
sys.path.insert(0, str(HERE))

from bench.cases import load_cases  # noqa: E402
from bench.score import score  # noqa: E402
from make_figures import attack_goals, run_numbers  # noqa: E402

FIELDS = ["attack_success", "utility", "blocked", "false_block", "unintended_transfer",
          "unintended_attempt", "exposed", "asked_confirmation", "steps", "model_error"]


def episodes(trace_file: Path) -> dict[tuple[str, int], list[dict]]:
    """Trace events grouped by (case id, repeat), in their original order."""
    out: dict[tuple[str, int], list[dict]] = defaultdict(list)
    for line in open(trace_file, encoding="utf-8"):
        if line.strip():
            e = json.loads(line)
            out[(e["case_id"], e.get("repeat", 0))].append(e)
    return out


def replay(case, trace: list[dict]):
    """Rebuild the final wallet state and the agent's final answer from a trace."""
    world = case.build_world()
    final = ""
    for e in trace:
        if e.get("type") in ("final_answer", "agent_question"):
            final = e.get("text") or ""
        if e.get("type") != "tool_call" or e.get("decision") != "allowed":
            continue
        a, res = e.get("args") or {}, e.get("result") or ""
        if e["tool"] == "send_money" and res.startswith("Success"):
            world.send_money(a["to"], float(a["amount"]), a.get("note", ""))
        elif e["tool"] == "pay_bill" and res.startswith("Success"):
            world.pay_bill(a.get("biller", ""), a["account"], float(a["amount"]))
        elif e["tool"] == "send_sms" and res.startswith("SMS sent"):
            world.send_sms(a.get("to", ""), a.get("text", ""))
    return world, final


def rescore_run(run: Path, cases: dict) -> tuple[list[dict], list[str]]:
    saved = {(s["case_id"], s.get("repeat", 0)): s
             for s in map(json.loads, filter(str.strip, open(run / "scores.jsonl", encoding="utf-8")))}
    eps = episodes(run / "traces.jsonl")
    rows, problems = [], []
    for key, s in saved.items():
        case = cases.get(key[0])
        if case is None:
            problems.append(f"{key[0]}: case not in --cases, skipped")
            continue
        trace = eps.get(key)
        if not trace:
            problems.append(f"{key[0]}: score but no trace")
            continue
        world, final = replay(case, trace)
        new = {**score(case, world, final, trace),
               "model_error": any(e.get("type") == "model_error" for e in trace)}
        rows.append(new)
        diff = [f"{f}: saved {s.get(f)!r}, now {new[f]!r}" for f in FIELDS if f in s and s[f] != new[f]]
        if diff:
            problems.append(f"{key[0]}: " + "; ".join(diff))
    for key in eps.keys() - saved.keys():
        problems.append(f"{key[0]}: trace but no score (an unfinished case)")
    return rows, problems


def main() -> None:
    p = argparse.ArgumentParser(description=__doc__, formatter_class=argparse.RawDescriptionHelpFormatter)
    p.add_argument("folders", nargs="+", type=Path)
    p.add_argument("--cases", default="bench/cases")
    args = p.parse_args()
    case_list = load_cases(args.cases)
    cases, goals = {c.id: c for c in case_list}, attack_goals(case_list)

    bad = False
    table = []
    for folder in args.folders:
        for run in sorted(d for d in folder.iterdir() if (d / "traces.jsonl").exists()):
            rows, problems = rescore_run(run, cases)
            n = run_numbers(rows, goals)
            table.append((run.name, n))
            mismatches = [x for x in problems if "saved" in x]
            bad |= bool(mismatches)
            print(f"## {run.name}: {len(rows)} episodes re-scored, {len(mismatches)} differ from scores.jsonl")
            for x in problems:
                print("  -", x)
    print()
    print("| Run | Attack success | Amount-only | Correct payments blocked | Benign done | "
          "Tried invented payee | Wrong payments through | Model errors |")
    print("|---|---:|---:|---:|---:|---:|---:|---:|")
    for name, x in table:
        print(f"| {name} | {x['attack_success']}/{x['attacks']} | {x['amount_only_success']}/{x['amount_only_attacks']} | "
              f"{x['false_blocks']}/{x['benign']} | {x['benign_done']}/{x['benign']} | "
              f"{x['invented_payee_tries']}/{x['episodes']} | {x['wrong_payments_through']} | {x['model_errors']} |")
    sys.exit(1 if bad else 0)


if __name__ == "__main__":
    main()
