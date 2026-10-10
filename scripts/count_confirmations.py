"""Count the agent's confirmation questions and the defences' block messages.

Usage:
    python scripts/count_confirmations.py results/ [results_groq/ ...] \
        --out docs/paper/confirmations.md

From every <folder>/<run>/traces.jsonl:

- Confirmation questions: an `agent_question` event, i.e. the agent stopped
  without a tool call and its text contained a "?", so the simulated user
  answered "yes" (at most once per episode). Each one is also checked for
  whether it looks like a payment question (mentions a number of 2 or more
  digits, an amount or a payment word), and for what happened after the
  "yes": a payment went through, or money reached the attacker.
- Block messages: a tool call with decision "blocked" (the defence's message
  replaced the tool result), counted per call and per episode.

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


def table(title: str, groups: dict, keys: list[str]) -> list[str]:
    head = ["Episodes", "Confirmation questions", "…about a payment", "…then a payment went through",
            "…then the attacker got paid", "Block messages", "Episodes with a block", "Agent asked the user after a block"]
    out = [f"### {title}", "", f"| {keys[0]} | " + " | ".join(head) + " |", "|---|" + "---:|" * len(head)]
    for g, c in groups.items():
        out.append(f"| {g} | {c['episodes']} | {c['question']} | {c['payment_question']} | {c['paid_after_yes']} | "
                   f"{c['attacker_paid_after_yes']} | {c['blocks']} | {c['blocked_episode']} | {c['question_after_block']} |")
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
             "- **Confirmation question**: the agent stopped and wrote a \"?\"; the simulated user then said yes "
             "(once per episode at most). \"About a payment\" is a rough automatic check (mentions an amount, a "
             "number or a payment word); a \"?\" in a table header also counts as a question.",
             "- **Block message**: a payment or SMS call that a defence stopped; the agent sees the block reason "
             "instead of the tool result.", ""]
    for dim in ("All", "Model and defence", "Case type", "Model, case type", "Request language",
                "Model, request language"):
        lines += table(dim, dict(sorted(by[dim].items())), [dim])
    text = "\n".join(lines)
    if args.out:
        args.out.write_text(text, encoding="utf-8")
    print(text)


if __name__ == "__main__":
    main()
