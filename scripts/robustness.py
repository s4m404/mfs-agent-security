"""Robustness checks for the no-defence results. No model needed.

Usage:
    python scripts/robustness.py results/ [results_groq/ ...] --skip granite \
        --out docs/paper/robustness.md

Reads the `none` runs (scores.jsonl) of every model and reports:

1. Attack success by where the attack is hidden, and without the
   tool-description attacks (one template in four languages, plus one seed).
2. Confidence intervals that treat each attack template as one unit. The 220
   attacks come from a few templates, each written in four languages and
   reused across tasks, so cases are not independent; a bootstrap over
   templates gives wider, more honest intervals than one over cases.
3. Successful attacks per template.
4. Attack success by attack language, with a permutation test (does the
   language matter more than chance?).
5. Paired comparisons between models on the same 220 attacks (exact McNemar).
6. The comprehension gate: normal tasks done by request language next to
   attack success among attacks the agent read, by attack language.
"""

from __future__ import annotations

import argparse
import json
import math
import random
import sys
from collections import Counter, defaultdict
from pathlib import Path

HERE = Path(__file__).resolve().parent
sys.path.insert(0, str(HERE))

from make_figures import LANG_NAMES, model_key, parse_run  # noqa: E402

LANGS = ["en", "bn", "banglish", "mixed"]
VECTORS = ["sms", "invoice", "tool_description"]


def template(case_id: str) -> str:
    """The attack template behind a case id (its text idea, before language)."""
    p = case_id.split("-")
    if case_id.startswith("gen-atk-amount-"):
        return f"amount-only ({p[3]})"
    if case_id.startswith("gen-atk-tooldesc-"):
        return "tool description"
    if case_id.startswith("gen-atk-"):
        return p[4]
    return f"seed: {case_id}"  # each hand-written seed attack is its own template


def load(folders: list[Path], skip: list[str]) -> dict[str, dict[str, dict]]:
    """model -> case id -> score row, for the `none` runs."""
    out: dict[str, dict[str, dict]] = {}
    for folder in folders:
        for f in sorted(folder.glob("*/scores.jsonl")):
            model, defence = parse_run(f.parent.name)
            if defence != "none" or any(s.lower() in model.lower() for s in skip):
                continue
            out[model] = {r["case_id"]: r for r in map(json.loads, filter(str.strip, open(f, encoding="utf-8")))}
    return dict(sorted(out.items(), key=lambda kv: model_key(kv[0])))


def pct(k: int, n: int) -> str:
    return f"{100 * k / n:.1f}%" if n else "n/a"


def bootstrap(rows: dict[str, dict], ids: list[str], groups: dict[str, list[str]] | None, b: int, seed: int):
    rng = random.Random(seed)
    keys = list(groups) if groups else ids
    vals = []
    for _ in range(b):
        pick = [rng.choice(keys) for _ in keys]
        sel = [i for k in pick for i in (groups[k] if groups else [k])]
        vals.append(sum(rows[i]["attack_success"] for i in sel) / len(sel))
    vals.sort()
    return vals[int(0.025 * b)], vals[min(b - 1, int(0.975 * b))]


def language_stat(rows: list[dict]) -> float:
    k, n = Counter(), Counter()
    for r in rows:
        n[r["injection_language"]] += 1
        k[r["injection_language"]] += r["attack_success"]
    p = sum(k.values()) / max(sum(n.values()), 1)
    return sum((k[l] - n[l] * p) ** 2 / (n[l] * p) for l in n) if p else 0.0


def permutation_p(rows: list[dict], b: int, seed: int) -> float:
    rng = random.Random(seed)
    obs = language_stat(rows)
    succ = [r["attack_success"] for r in rows]
    hits = 0
    for _ in range(b):
        rng.shuffle(succ)
        hits += language_stat([{**r, "attack_success": s} for r, s in zip(rows, succ)]) >= obs - 1e-12
    return hits / b


def mcnemar(a: dict, b: dict, ids: list[str]) -> tuple[int, int, float]:
    only_a = sum(1 for i in ids if a[i]["attack_success"] and not b[i]["attack_success"])
    only_b = sum(1 for i in ids if b[i]["attack_success"] and not a[i]["attack_success"])
    n, k = only_a + only_b, min(only_a, only_b)
    p = min(1.0, 2 * sum(math.comb(n, j) for j in range(k + 1)) / 2 ** n) if n else 1.0
    return only_a, only_b, p


def main() -> None:
    ap = argparse.ArgumentParser(description=__doc__, formatter_class=argparse.RawDescriptionHelpFormatter)
    ap.add_argument("folders", nargs="+", type=Path)
    ap.add_argument("--skip", nargs="*", default=[], help="leave out models whose name contains this")
    ap.add_argument("--bootstrap", type=int, default=4000)
    ap.add_argument("--permutations", type=int, default=5000)
    ap.add_argument("--seed", type=int, default=0)
    ap.add_argument("--out", type=Path)
    args = ap.parse_args()

    data = load(args.folders, args.skip)
    if not data:
        sys.exit("no `none` runs found")
    models = list(data)
    ids = sorted(i for i, r in next(iter(data.values())).items() if r["is_attack"])
    groups: dict[str, list[str]] = defaultdict(list)
    for i in ids:
        groups[template(i)].append(i)

    L = ["# Robustness checks (no defence)", "",
         "Made by `scripts/robustness.py` from the `none` runs of: " + ", ".join(models) + ".", "",
         f"{len(ids)} attack cases from {len(groups)} templates (each generated attack idea is one template, "
         "written in four languages and reused across tasks; each hand-written seed attack is its own).", ""]

    L += ["## 1. Where the attack is hidden", "",
          "| Model | All attacks | SMS | Invoice | Tool description | All except tool-description attacks |",
          "|---|---:|---:|---:|---:|---:|"]
    for m in models:
        d = data[m]
        k, n = Counter(), Counter()
        for i in ids:
            n[d[i]["injection_vector"]] += 1
            k[d[i]["injection_vector"]] += d[i]["attack_success"]
        rest = [i for i in ids if d[i]["injection_vector"] != "tool_description"]
        kr = sum(d[i]["attack_success"] for i in rest)
        tot = sum(k.values())
        L.append(f"| {m} | {tot}/{len(ids)} ({pct(tot, len(ids))}) | "
                 + " | ".join(f"{k[v]}/{n[v]}" for v in VECTORS)
                 + f" | {kr}/{len(rest)} ({pct(kr, len(rest))}) |")
    L.append("")

    L += ["## 2. Intervals: cases vs templates as the unit", "",
          f"95% bootstrap intervals, {args.bootstrap} resamples, seed {args.seed}.", "",
          "| Model | Attack success | Over cases | Over templates |", "|---|---:|---:|---:|"]
    for m in models:
        d = data[m]
        k = sum(d[i]["attack_success"] for i in ids)
        lo, hi = bootstrap(d, ids, None, args.bootstrap, args.seed)
        tlo, thi = bootstrap(d, ids, groups, args.bootstrap, args.seed)
        L.append(f"| {m} | {pct(k, len(ids))} | {100 * lo:.1f} to {100 * hi:.1f} | {100 * tlo:.1f} to {100 * thi:.1f} |")
    L.append("")

    L += ["## 3. Successful attacks per template", "",
          "| Template | Cases | " + " | ".join(models) + " |", "|---|---:|" + "---:|" * len(models)]
    order = sorted(groups, key=lambda t: (-sum(data[m][i]["attack_success"] for m in models for i in groups[t]), t))
    for t in order:
        L.append(f"| {t} | {len(groups[t])} | "
                 + " | ".join(str(sum(data[m][i]["attack_success"] for i in groups[t])) for m in models) + " |")
    L.append("")

    L += ["## 4. Attack language", "",
          f"Successful attacks by the language of the attack text. p: permutation test ({args.permutations} "
          "shuffles of the success labels) of whether success differs between languages more than chance.", "",
          "| Model | " + " | ".join(LANG_NAMES[l] for l in LANGS) + " | p |", "|---|" + "---:|" * (len(LANGS) + 1)]
    for m in models:
        rows = [data[m][i] for i in ids]
        k, n = Counter(), Counter()
        for r in rows:
            n[r["injection_language"]] += 1
            k[r["injection_language"]] += r["attack_success"]
        p = permutation_p(rows, args.permutations, args.seed)
        L.append(f"| {m} | " + " | ".join(f"{k[l]}/{n[l]}" for l in LANGS) + f" | {p:.3f} |")
    L.append("")

    L += ["## 5. Paired comparisons", "",
          "Exact McNemar test on the same 220 attacks: attacks only the first model fell for, only the second, "
          "and the two-sided p-value.", "",
          "| First | Second | Only first | Only second | p |", "|---|---|---:|---:|---:|"]
    for i, a in enumerate(models):
        for b in models[i + 1:]:
            oa, ob, p = mcnemar(data[a], data[b], ids)
            L.append(f"| {a} | {b} | {oa} | {ob} | {p:.3f} |")
    L.append("")

    L += ["## 6. Comprehension gate", "",
          "Left: normal tasks done, by the language of the user's request. Right: attack success among attacks "
          "the agent read, by the language of the attack. A model that handles a language badly also follows "
          "attacks in it less often.", "",
          "| Model | " + " | ".join(f"Tasks done: {LANG_NAMES[l]}" for l in LANGS) + " | "
          + " | ".join(f"Attacks (read): {LANG_NAMES[l]}" for l in LANGS) + " |",
          "|---|" + "---:|" * (2 * len(LANGS))]
    for m in models:
        u, un, a, an = Counter(), Counter(), Counter(), Counter()
        for r in data[m].values():
            if not r["is_attack"]:
                un[r["task_language"]] += 1
                u[r["task_language"]] += r["utility"]
            elif r["exposed"]:
                an[r["injection_language"]] += 1
                a[r["injection_language"]] += r["attack_success"]
        L.append(f"| {m} | " + " | ".join(f"{u[l]}/{un[l]}" for l in LANGS) + " | "
                 + " | ".join(f"{a[l]}/{an[l]}" for l in LANGS) + " |")
    L.append("")

    text = "\n".join(L)
    if args.out:
        args.out.write_text(text, encoding="utf-8")
    print(text)


if __name__ == "__main__":
    main()
