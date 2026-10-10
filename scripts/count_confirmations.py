"""Count the agent's confirmation questions and the defences' block messages.

Usage:
    python scripts/count_confirmations.py results/ [results_groq/ ...] \
        --out docs/paper/confirmations.md

From every <folder>/<run>/traces.jsonl:

Every column except "Block messages" counts episodes (yes or no per
episode), so it can be divided by "Episodes".

- Question: the episode has an `agent_question` event, i.e. the agent
  stopped without a tool call and its text contained a "?", and the simulated
  user answered "yes" (at most once per episode). The "?" need not be a real
  confirmation request. A rough automatic check marks whether that question
  mentions a payment (a number of 2 or more digits, an amount or a payment
  word).
- Payment later / attacker payment later: at least one successful payment
  (or one counted as the attacker's goal by bench/score.py) appears anywhere
  after that question in the episode, not necessarily as the next step. This
  is an order in time, not evidence that the question caused the payment;
  an earlier payment in the same episode is not excluded.
- Block messages: tool calls with decision "blocked" (the defence's message
  replaced the tool result), counted per call; "episodes with a block"
  counts episodes.
- Question after a block: the episode's question comes after its first
  block. The rate divides by episodes with a block.

Counts are split by model, defence, request language, and attack vs normal
case. No model is needed.
"""

from __future__ import annotations

import argparse
import re
import sys
from collections import Counter, defaultdict
from pathlib import Path

HERE = Path(__file__).resolve().parent
sys.path.insert(0, str(HERE.parent))
sys.path.insert(0, str(HERE))

from bench.cases import load_cases  # noqa: E402
from bench.score import _call_as_transfer, _is_attack_transfer  # noqa: E402
from make_figures import LANG_NAMES, parse_run  # noqa: E402
from mfs_env.text import normalise_text  # noqa: E402
from rescore import episodes  # noqa: E402

PAY_WORDS = re.compile(r"\d{2,}|tk|taka|টাকা|৳|pay|send|পাঠা|পরিশোধ|বিল|bill", re.I)
MONEY_TOOLS = ("send_money", "pay_bill")


def episode_counts(case, trace: list[dict]) -> dict:
    q = next((i for i, e in enumerate(trace) if e.get("type") == "agent_question"), None)
    after = trace[q + 1:] if q is not None else []
    paid_after = [e for e in after if e.get("type") == "tool_call" and e.get("tool") in MONEY_TOOLS
                  and e.get("decision") == "allowed" and str(e.get("result", "")).startswith("Success")]
    blocks = [e for e in trace if e.get("type") == "tool_call" and e.get("decision") == "blocked"]
    return {
        "question": q is not None,
        "payment_question": q is not None and bool(PAY_WORDS.search(normalise_text(trace[q].get("text") or ""))),
        "paid_after_yes": bool(paid_after),
        "attacker_paid_after_yes": any(_is_attack_transfer(case, _call_as_transfer(e)) for e in paid_after),
        "blocks": len(blocks),
        "blocked_episode": bool(blocks),
        "question_after_block": bool(blocks) and q is not None and trace.index(blocks[0]) < q,
    }


def rate(k: int, n: int) -> str:
    return f"{k}/{n} ({100 * k / n:.0f}%)" if n else "n/a"


HEAD = ["Episodes", "Episodes with a question (simulated yes)", "…question mentions a payment (rough check)",
        "…a payment succeeded later in the episode", "…an attacker payment succeeded later in the episode",
        "Block messages (calls)", "Episodes with a block", "Question after a block / episodes with a block"]


def table(title: str, groups: dict, keys: list[str]) -> list[str]:
    out = [f"### {title}", "", f"| {keys[0]} | " + " | ".join(HEAD) + " |", "|---|" + "---:|" * len(HEAD)]
    for g, c in groups.items():
        out.append(f"| {g} | {c['episodes']} | {c['question']} | {c['payment_question']} | {c['paid_after_yes']} | "
                   f"{c['attacker_paid_after_yes']} | {c['blocks']} | {c['blocked_episode']} | "
                   f"{rate(c['question_after_block'], c['blocked_episode'])} |")
    return out + [""]


def main() -> None:
    p = argparse.ArgumentParser(description=__doc__, formatter_class=argparse.RawDescriptionHelpFormatter)
    p.add_argument("folders", nargs="+", type=Path)
    p.add_argument("--cases", default="bench/cases")
    p.add_argument("--out", type=Path, default=None)
    args = p.parse_args()
    cases = {c.id: c for c in load_cases(args.cases)}

    by: dict[str, dict] = defaultdict(lambda: defaultdict(Counter))
    runs = []
    for folder in args.folders:
        for run in sorted(d for d in folder.iterdir() if (d / "traces.jsonl").exists()):
            model, defence = parse_run(run.name)
            runs.append(run.name)
            for (case_id, _), trace in episodes(run / "traces.jsonl").items():
                case = cases.get(case_id)
                if case is None:
                    continue
                c = episode_counts(case, trace)
                c["episodes"] = 1
                kind = "attack" if case.is_attack else "normal"
                for dim, key in (("Model and defence", f"{model} / {defence}"),
                                 ("Request language", LANG_NAMES.get(case.task_language, case.task_language)),
                                 ("Case type", kind),
                                 ("Model, case type", f"{model} / {kind}"),
                                 ("Model, request language",
                                  f"{model} / {LANG_NAMES.get(case.task_language, case.task_language)}"),
                                 ("All", "all")):
                    by[dim][key].update(c)

    lines = ["# Confirmation questions and block messages", "",
             "Made by `scripts/count_confirmations.py` from these runs: " + ", ".join(runs) + ".", "",
             "Column definitions are in the script's docstring. Every column except \"Block messages\" counts "
             "episodes. \"Later in the episode\" means at least one such payment anywhere after the question, "
             "not necessarily the next step, and does not show that the question caused it.", ""]
    for dim in ("All", "Model and defence", "Case type", "Model, case type", "Request language",
                "Model, request language"):
        lines += table(dim, dict(sorted(by[dim].items())), [dim])
    text = "\n".join(lines)
    if args.out:
        args.out.write_text(text, encoding="utf-8")
    print(text)


if __name__ == "__main__":
    main()
