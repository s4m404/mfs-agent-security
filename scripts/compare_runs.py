"""Compare finished runs, with 95% confidence intervals.

Usage:
    python scripts/compare_runs.py results/

Reads every results/*/scores.jsonl and prints one Markdown table.
Confidence intervals come from a bootstrap over test cases (all repeats of a
case are resampled together), because cases, not repeats, are the main source
of uncertainty: at temperature 0 the repeats of a case are almost identical.
"""

from __future__ import annotations

import argparse
import collections
import json
import random
from pathlib import Path


def load(run_dir: Path) -> list[dict]:
    return [json.loads(line) for line in open(run_dir / "scores.jsonl", encoding="utf-8")]


def rate(rows, num, den=lambda r: True):
    d = [r for r in rows if den(r)]
    return (sum(1 for r in d if num(r)) / len(d)) if d else 0.0


def bootstrap(rows, fn, n=2000, seed=0):
    rng = random.Random(seed)
    by_case = collections.defaultdict(list)
    for r in rows:
        by_case[r["case_id"]].append(r)
    ids = list(by_case)
    vals = sorted(fn([r for i in rng.choices(ids, k=len(ids)) for r in by_case[i]]) for _ in range(n))
    return vals[int(0.025 * n)], vals[int(0.975 * n)]


METRICS = {
    "Attack success": (lambda r: r["attack_success"], lambda r: r["is_attack"]),
    "Benign tasks done": (lambda r: r["utility"], lambda r: not r["is_attack"]),
    "Correct actions blocked": (lambda r: r["false_block"], lambda r: not r["is_attack"]),
    "Tried to pay an invented payee": (lambda r: r["unintended_attempt"], lambda r: True),
}


def repeat_agreement(rows) -> float:
    by_case = collections.defaultdict(set)
    for r in rows:
        by_case[r["case_id"]].add((r["attack_success"], r["utility"], r["unintended_attempt"]))
    return sum(len(v) == 1 for v in by_case.values()) / len(by_case)


def main() -> None:
    p = argparse.ArgumentParser()
    p.add_argument("results", type=Path)
    args = p.parse_args()
    runs = sorted(d for d in args.results.iterdir() if (d / "scores.jsonl").exists())
    print("| Run | Repeats | " + " | ".join(METRICS) + " | Same outcome in every repeat |")
    print("|---|---:|" + "---:|" * len(METRICS) + "---:|")
    for d in runs:
        rows = load(d)
        cells = []
        for num, den in METRICS.values():
            v = rate(rows, num, den)
            lo, hi = bootstrap(rows, lambda s: rate(s, num, den))
            if v == 0:  # the bootstrap gives 0 to 0; use the rule of three instead
                hi = 3 / len({r["case_id"] for r in rows if den(r)})
            cells.append(f"{100 * v:.1f}% ({100 * lo:.0f} to {100 * hi:.0f})")
        reps = len({r.get("repeat", 0) for r in rows})
        print(f"| {d.name} | {reps} | " + " | ".join(cells) + f" | {100 * repeat_agreement(rows):.0f}% |")


if __name__ == "__main__":
    main()
