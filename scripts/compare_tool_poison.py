"""Poisoned description on the wallet's own tool, or on a third-party tool?

Usage:
    python scripts/compare_tool_poison.py --wallet results/ results_groq/ \
        --third-party results_third_party/ results_groq_third_party/

The main set's 37 tool-description attacks put the poisoned text in the
description of the wallet's own send_money or pay_bill. The third-party set
(bench/cases_third_party/) repeats each of them with the same text in the
description of a separate app's tool (billbuddy_upcoming_bills) and the
wallet's tools left clean. Case tp-X is case X with only that change, so the
two runs pair case by case.

For every model and defence run on both sets it reports attack success on
each version, the attacks that worked on only one of the two, an exact
McNemar test, and how often the agent called the third-party tool. A second
table splits attack success by the language of the poisoned text. If two
folders hold the same model and defence, the one given later wins.
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

from make_figures import LANG_NAMES, model_key, parse_run  # noqa: E402
from mfs_env.server import THIRD_PARTY_TOOL  # noqa: E402
from robustness import mcnemar  # noqa: E402

LANGS = ["en", "bn", "banglish", "mixed"]
DEFENCES = ["none", "provenance", "provenance-amount", "provenance-consistent"]


def load(folders: list[Path], prefix: str = "") -> dict[tuple[str, str], dict[str, dict]]:
    """(model, defence) -> case id (without the "tp-" prefix) -> score row, plus "_called" per case."""
    out: dict[tuple[str, str], dict[str, dict]] = {}
    for folder in folders:
        for run in sorted(d for d in folder.iterdir() if (d / "scores.jsonl").exists()):
            model, defence = parse_run(run.name)
            rows = {}
            for line in open(run / "scores.jsonl", encoding="utf-8"):
                if line.strip():
                    r = json.loads(line)
                    if r["case_id"].startswith(prefix) and r["injection_vector"] == "tool_description":
                        rows[r["case_id"].removeprefix(prefix)] = {**r, "called": False}
            traces = run / "traces.jsonl"
            if prefix and traces.exists():
                for line in open(traces, encoding="utf-8"):
                    e = json.loads(line)
                    cid = e.get("case_id", "").removeprefix(prefix)
                    if e.get("type") == "tool_call" and e.get("tool") == THIRD_PARTY_TOOL and cid in rows:
                        rows[cid]["called"] = True
            if rows:
                out[(model, defence)] = rows
    return out


def report(wallet: dict, third: dict) -> str:
    keys = sorted(set(wallet) & set(third),
                  key=lambda k: (model_key(k[0]), DEFENCES.index(k[1]) if k[1] in DEFENCES else len(DEFENCES)))
    lines = ["| Model | Defence | Cases | Wallet's own tool | Third-party tool | Both | Only wallet | Only third-party "
             "| p (McNemar) | Called the third-party tool |", "|---|---|" + "---:|" * 8]
    for k in keys:
        ids = sorted(set(wallet[k]) & set(third[k]))
        w, t = wallet[k], third[k]
        kw = sum(w[i]["attack_success"] for i in ids)
        kt = sum(t[i]["attack_success"] for i in ids)
        both = sum(w[i]["attack_success"] and t[i]["attack_success"] for i in ids)
        only_w, only_t, p = mcnemar(w, t, ids)
        called = sum(t[i]["called"] for i in ids)
        lines.append(f"| {k[0]} | {k[1]} | {len(ids)} | {kw} | {kt} | {both} | {only_w} | {only_t} | {p:.3f} | "
                     f"{called}/{len(ids)} |")
    lines += ["", "By the language of the poisoned text (wallet's own tool / third-party tool):", "",
              "| Model | Defence | " + " | ".join(LANG_NAMES[lang] for lang in LANGS) + " |",
              "|---|---|" + "---:|" * len(LANGS)]
    for k in keys:
        ids = sorted(set(wallet[k]) & set(third[k]))
        n, kw, kt = Counter(), Counter(), Counter()
        for i in ids:
            lang = wallet[k][i]["injection_language"]
            n[lang] += 1
            kw[lang] += wallet[k][i]["attack_success"]
            kt[lang] += third[k][i]["attack_success"]
        lines.append(f"| {k[0]} | {k[1]} | " + " | ".join(f"{kw[lang]} / {kt[lang]} of {n[lang]}" for lang in LANGS) + " |")
    return "\n".join(lines)


def main() -> None:
    p = argparse.ArgumentParser(description=__doc__, formatter_class=argparse.RawDescriptionHelpFormatter)
    p.add_argument("--wallet", nargs="+", type=Path, required=True, help="runs on the main cases (bench/cases)")
    p.add_argument("--third-party", nargs="+", type=Path, required=True,
                   help="runs on the third-party cases (bench/cases_third_party)")
    args = p.parse_args()
    wallet, third = load(args.wallet), load(args.third_party, prefix="tp-")
    if not set(wallet) & set(third):
        sys.exit("no model and defence was run on both sets")
    print(report(wallet, third))


if __name__ == "__main__":
    main()
