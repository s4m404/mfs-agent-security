"""Figures and tables for the paper (see docs/paper/outline.md).

Usage:
    python scripts/make_figures.py results/ [results_groq/ ...] \
        --detectors results_detectors/flags.jsonl --out docs/paper/figures

Reads every <folder>/<run>/scores.jsonl. A run folder is named
<model>__<defence>__<prompt> (the run_bench.py default). If two folders hold
the same model and defence, the one given later wins (a note is printed), so
pass the newest runs last. Without --detectors, Figure 1 is skipped.

Writes to --out:
    fig1_detectors.pdf/.png   normal texts flagged and normal tasks broken, by
                              language, per detector; provenance for comparison
    fig2_attack_vs_invented.pdf/.png
                              attack success vs tries to pay an invented payee
                              (no defence), per model
    fig3_defences.pdf/.png    successful attacks per defence, amount-only vs
                              redirect/OTP; wrong payments that went through
    table1_main.md/.tex       main results, one row per model and defence
    table2_language.md/.tex   attack success by attack language (no defence)
    numbers.json              every number the figures show

Tables need no extra package; figures need matplotlib (pip install matplotlib).
"""

from __future__ import annotations

import argparse
import json
import re
import sys
from collections import defaultdict
from pathlib import Path

HERE = Path(__file__).resolve().parent
sys.path.insert(0, str(HERE.parent))
sys.path.insert(0, str(HERE))

from bench.cases import load_cases  # noqa: E402
from detector_eval import LANGS, tasks_hit  # noqa: E402

DEFENCE_ORDER = ["none", "keyword", "provenance", "provenance-amount", "provenance-consistent"]
LANG_NAMES = {"en": "English", "bn": "Bangla", "banglish": "Banglish", "mixed": "Mixed"}
DETECTOR_NAMES = {
    "keyword": "Keyword",
    "protectai/deberta-v3-base-prompt-injection-v2": "ProtectAI v2",
    "deepset/deberta-v3-base-injection": "deepset",
}
PROVENANCE = ("provenance", "provenance-amount", "provenance-consistent")
# Categorical slots 1-4 of the reference palette, always in this order.
COLOURS = ["#2a78d6", "#eb6834", "#1baf7a", "#eda100"]
INK, MUTED, GRID = "#222222", "#666666", "#dddddd"


# ---------- loading ----------

def model_label(raw: str) -> str:
    """'Qwen_Qwen2.5-14B-Instruct-AWQ' -> 'Qwen2.5-14B'; 'openai_gpt-oss-120b' -> 'gpt-oss-120b'."""
    name = raw.split("_", 1)[1] if "_" in raw else raw
    name = re.sub(r"-Instruct|-AWQ|-GPTQ.*", "", name)
    return name.replace("Hermes-3-Llama-3.1-8B", "Hermes-3-8B")


def parse_run(dirname: str) -> tuple[str, str]:
    parts = dirname.split("__")
    if len(parts) < 2:
        raise ValueError(f"run folder {dirname!r} is not <model>__<defence>__<prompt>")
    return model_label(parts[0]), parts[1]


def model_key(m: str) -> tuple:
    size = re.search(r"(\d+(?:\.\d+)?)B", m, re.I)
    return (not m.startswith("Qwen"), float(size.group(1)) if size else 0.0, m)


def load_runs(folders: list[Path]) -> dict[tuple[str, str], list[dict]]:
    runs: dict[tuple[str, str], list[dict]] = {}
    for folder in folders:
        for f in sorted(folder.glob("*/scores.jsonl")):
            try:
                key = parse_run(f.parent.name)
            except ValueError as e:
                print(f"skipped: {e}")
                continue
            if key in runs:
                print(f"note: {f.parent} replaces an earlier run of {key[0]} / {key[1]}")
            runs[key] = [json.loads(line) for line in open(f, encoding="utf-8") if line.strip()]
    return runs


def models(runs) -> list[str]:
    return sorted({m for m, _ in runs}, key=model_key)


def defences(runs, model: str) -> list[str]:
    have = {d for m, d in runs if m == model}
    return [d for d in DEFENCE_ORDER if d in have] + sorted(have - set(DEFENCE_ORDER))


def attack_goals(cases) -> dict[str, str]:
    return {c.id: c.attack["goal"] for c in cases if c.is_attack}


# ---------- numbers ----------

def run_numbers(rows: list[dict], goals: dict[str, str]) -> dict:
    att = [r for r in rows if r["is_attack"]]
    ben = [r for r in rows if not r["is_attack"]]
    amount_only = [r for r in att if goals.get(r["case_id"]) == "overpay"]
    n = lambda rs, k: sum(bool(r.get(k)) for r in rs)  # noqa: E731
    return {
        "episodes": len(rows),
        "attacks": len(att),
        "attack_success": n(att, "attack_success"),
        "amount_only_attacks": len(amount_only),
        "amount_only_success": n(amount_only, "attack_success"),
        "benign": len(ben),
        "benign_done": n(ben, "utility"),
        "false_blocks": n(ben, "false_block"),
        "invented_payee_tries": n(rows, "unintended_attempt"),
        "wrong_payments_through": n(rows, "unintended_transfer"),
        "model_errors": n(rows, "model_error"),
    }


def all_numbers(runs, goals) -> dict[str, dict[str, dict]]:
    return {m: {d: run_numbers(runs[(m, d)], goals) for d in defences(runs, m)} for m in models(runs)}


def language_numbers(runs) -> dict[str, dict[str, tuple[int, int]]]:
    """{model: {attack language: (successes, attack cases)}}, no defence only."""
    out = {}
    for m in models(runs):
        rows = runs.get((m, "none"))
        if not rows:
            continue
        c: dict[str, list[int]] = defaultdict(lambda: [0, 0])
        for r in rows:
            if r["is_attack"]:
                c[r["injection_language"]][0] += bool(r["attack_success"])
                c[r["injection_language"]][1] += 1
        out[m] = {lang: tuple(c[lang]) for lang in LANGS if lang in c}
    return out


def detector_numbers(flag_rows: list[dict], cases, runs) -> dict:
    """Per detector: normal texts flagged and normal tasks broken, by language.
    'provenance' row: correct payments blocked in the real runs, by request language."""
    names = list(flag_rows[0]["flags"])
    flags = {d: [r["flags"][d] for r in flag_rows] for d in names}
    texts = [{k: v for k, v in r.items() if k != "flags"} for r in flag_rows]
    hit = tasks_hit(cases, texts, flags)
    out = {}
    for d in names:
        normal = [(t, x) for t, x in zip(texts, flags[d]) if t["kind"] == "normal"]
        attack = [(t, x) for t, x in zip(texts, flags[d]) if t["kind"] == "attack"]
        out[d] = {
            "attack_flagged": (sum(x for _, x in attack), len(attack)),
            "normal_flagged": {lang: (sum(x for t, x in normal if t["language"] == lang),
                                      sum(1 for t, _ in normal if t["language"] == lang)) for lang in LANGS},
            "tasks_broken": {lang: hit[d].get(lang, (0, 0)) for lang in LANGS},
        }
    prov: dict[str, list[int]] = defaultdict(lambda: [0, 0])
    for (_, d), rows in runs.items():
        if d in PROVENANCE:
            for r in rows:
                if not r["is_attack"]:
                    prov[r["task_language"]][0] += bool(r["false_block"])
                    prov[r["task_language"]][1] += 1
    out["provenance (real runs)"] = {"tasks_broken": {lang: tuple(prov.get(lang, (0, 0))) for lang in LANGS}}
    return out


# ---------- tables ----------

def pct(k: int, n: int) -> str:
    return f"{100 * k / n:.1f}%" if n else "n/a"


TABLE1_HEAD = ["Model", "Defence", "Attack success", "Amount-only attacks", "Correct payments blocked",
               "Benign tasks done", "Tried to pay an invented payee", "Wrong payments went through"]


def table1_rows(nums) -> list[list[str]]:
    rows = []
    for m, by_d in nums.items():
        for d, x in by_d.items():
            rows.append([m, d,
                         f"{pct(x['attack_success'], x['attacks'])} ({x['attack_success']}/{x['attacks']})",
                         f"{x['amount_only_success']}/{x['amount_only_attacks']}",
                         f"{x['false_blocks']}/{x['benign']}",
                         pct(x["benign_done"], x["benign"]),
                         pct(x["invented_payee_tries"], x["episodes"]),
                         str(x["wrong_payments_through"])])
    return rows


def table2_rows(lang_nums) -> list[list[str]]:
    return [[m] + [f"{k}/{n}" if n else "n/a" for k, n in (by.get(lang, (0, 0)) for lang in LANGS)]
            for m, by in lang_nums.items()]


def markdown(head: list[str], rows: list[list[str]], text_cols: int = 2) -> str:
    lines = ["| " + " | ".join(head) + " |", "|" + "---|" * text_cols + "---:|" * (len(head) - text_cols)]
    return "\n".join(lines + ["| " + " | ".join(r) + " |" for r in rows]) + "\n"


def latex(head: list[str], rows: list[list[str]], caption: str, label: str, text_cols: int = 2) -> str:
    esc = lambda s: s.replace("%", r"\%").replace("_", r"\_")  # noqa: E731
    out = [r"\begin{table}[t]", r"\centering\small", rf"\caption{{{caption}}}", rf"\label{{{label}}}",
           r"\begin{tabular}{" + "l" * text_cols + "r" * (len(head) - text_cols) + "}", r"\toprule",
           " & ".join(esc(h) for h in head) + r" \\", r"\midrule"]
    out += [" & ".join(esc(c) for c in r) + r" \\" for r in rows]
    return "\n".join(out + [r"\bottomrule", r"\end{tabular}", r"\end{table}"]) + "\n"


# ---------- figures ----------

def _style(ax, ylabel: str) -> None:
    ax.set_ylabel(ylabel, color=INK)
    ax.spines[["top", "right"]].set_visible(False)
    ax.spines[["left", "bottom"]].set_color(MUTED)
    ax.tick_params(colors=MUTED, labelcolor=INK)
    ax.yaxis.grid(True, color=GRID, linewidth=0.6)
    ax.set_axisbelow(True)


def _bars(ax, groups: list[str], series: dict[str, list[float]], labels: dict[str, list[str]] | None = None):
    width = 0.8 / max(1, len(series))
    for i, (name, vals) in enumerate(series.items()):
        xs = [g + (i - (len(series) - 1) / 2) * width for g in range(len(groups))]
        bars = ax.bar(xs, vals, width * 0.92, label=name, color=COLOURS[i % len(COLOURS)])
        if labels and name in labels:
            ax.bar_label(bars, labels[name], fontsize=6, color=INK, padding=1)
    ax.set_xticks(range(len(groups)), groups)


def _save(fig, out: Path, name: str) -> list[Path]:
    fig.tight_layout()
    paths = [out / f"{name}.pdf", out / f"{name}.png"]
    for p in paths:
        fig.savefig(p, dpi=200)
    return paths


def fig1(det, out: Path, plt) -> list[Path]:
    fig, (a, b) = plt.subplots(1, 2, figsize=(7.0, 2.6))
    groups = [LANG_NAMES[lang] for lang in LANGS]
    detectors = [d for d in det if "normal_flagged" in det[d]]
    share = lambda k, n: 100 * k / n if n else 0  # noqa: E731
    name = lambda d: DETECTOR_NAMES.get(d, d.split("/")[-1])  # noqa: E731
    _bars(a, groups, {name(d): [share(*det[d]["normal_flagged"][lang]) for lang in LANGS] for d in detectors},
          {name(d): [str(k) for k, _ in (det[d]["normal_flagged"][lang] for lang in LANGS)] for d in detectors})
    if detectors:  # the same texts for every detector: show how many under each language
        a.set_xticks(range(len(LANGS)), [f"{g}\n(n={det[detectors[0]]['normal_flagged'][lang][1]})"
                                         for g, lang in zip(groups, LANGS)])
    _style(a, "Normal texts flagged (%)")
    a.set_title("(a) False alarms, by text language", fontsize=9, color=INK)
    rows = detectors + ["provenance (real runs)"]
    _bars(b, groups, {name(d): [share(*det[d]["tasks_broken"][lang]) for lang in LANGS] for d in rows},
          {name(d): [str(k) for k, _ in (det[d]["tasks_broken"][lang] for lang in LANGS)] for d in rows})
    _style(b, "Normal tasks broken (%)")
    b.set_title("(b) Used as a filter, by request language", fontsize=9, color=INK)
    for ax in (a, b):
        ax.set_ylim(0, 110)
    b.legend(fontsize=7, frameon=False, loc="upper left", bbox_to_anchor=(1.0, 1.0))
    return _save(fig, out, "fig1_detectors")


def fig2(nums, out: Path, plt) -> list[Path]:
    ms = [m for m in nums if "none" in nums[m]]
    x = [nums[m]["none"] for m in ms]
    fig, ax = plt.subplots(figsize=(3.5, 2.6))
    _bars(ax, ms, {"Attack succeeded (% of attacks)": [100 * v["attack_success"] / v["attacks"] for v in x],
                   "Tried to pay an invented payee (% of all)": [100 * v["invented_payee_tries"] / v["episodes"]
                                                                  for v in x]})
    _style(ax, "Episodes (%)")
    ax.tick_params(axis="x", labelsize=7, rotation=20)
    ax.legend(fontsize=6.5, frameon=False, loc="upper right")
    ax.set_ylim(0, 70)
    return _save(fig, out, "fig2_attack_vs_invented")


def fig3(nums, out: Path, plt) -> list[Path]:
    short = {"none": "none", "provenance": "prov.", "provenance-amount": "+amount", "provenance-consistent": "+consist."}
    keys, xs, groups, x = [], [], [], 0.0
    for m in nums:
        ds = [d for d in nums[m] if d in short]
        if not ds:
            continue
        start = x
        for d in ds:
            keys.append((m, d))
            xs.append(x)
            x += 1
        groups.append((m, (start + x - 1) / 2))
        x += 0.8  # gap between models
    redirect = [nums[m][d]["attack_success"] - nums[m][d]["amount_only_success"] for m, d in keys]
    amount = [nums[m][d]["amount_only_success"] for m, d in keys]
    wrong = [nums[m][d]["wrong_payments_through"] for m, d in keys]
    fig, (a, b) = plt.subplots(2, 1, figsize=(7.0, 4.2), sharex=True)
    a.bar(xs, redirect, 0.8, color=COLOURS[0], label="Redirect money or leak OTP")
    a.bar(xs, amount, 0.8, bottom=redirect, color=COLOURS[1], label="Amount-only (real payee, higher amount)",
          edgecolor="white", linewidth=1)
    totals = [r + v for r, v in zip(redirect, amount)]
    a.bar_label(a.containers[1], [str(t) for t in totals], fontsize=6, color=INK, padding=1)
    _style(a, "Successful attacks\n(of 220)")
    a.legend(fontsize=7, frameon=False)
    bars = b.bar(xs, wrong, 0.8, color=COLOURS[2])
    b.bar_label(bars, [str(w) for w in wrong], fontsize=6, color=INK, padding=1)
    _style(b, "Wrong payments\nthat went through")
    b.set_xticks(xs, [short[d] for _, d in keys], fontsize=6, rotation=90)
    for m, centre in groups:
        b.annotate(m, (centre, 0), xycoords=("data", "axes fraction"), xytext=(0, -38), textcoords="offset points",
                   ha="center", va="top", fontsize=7, color=INK)
    return _save(fig, out, "fig3_defences")


# ---------- main ----------

def make_all(folders: list[Path], out: Path, cases_dir: str = "bench/cases", detectors: Path | None = None,
             figures: bool = True) -> list[Path]:
    cases = load_cases(cases_dir)
    runs = load_runs(folders)
    if not runs:
        raise SystemExit(f"no */scores.jsonl found in {', '.join(map(str, folders))}")
    out.mkdir(parents=True, exist_ok=True)
    nums = all_numbers(runs, attack_goals(cases))
    langs = language_numbers(runs)
    det = None
    if detectors:
        flag_rows = [json.loads(line) for line in open(detectors, encoding="utf-8") if line.strip()]
        det = detector_numbers(flag_rows, cases, runs)

    written = []
    t1, t2 = table1_rows(nums), table2_rows(langs)
    t2_head = ["Model"] + [f"{LANG_NAMES[lang]} attacks" for lang in LANGS]
    for name, head, rows, cap, tc in [
        ("table1_main", TABLE1_HEAD, t1, "Main results on the 302 cases (220 attacks, 82 normal tasks).", 2),
        ("table2_language", t2_head, t2, "Successful attacks by attack language, no defence.", 1),
    ]:
        (out / f"{name}.md").write_text(markdown(head, rows, tc), encoding="utf-8")
        (out / f"{name}.tex").write_text(latex(head, rows, cap, f"tab:{name}", tc), encoding="utf-8")
        written += [out / f"{name}.md", out / f"{name}.tex"]
    (out / "numbers.json").write_text(json.dumps({"runs": nums, "by_language": langs, "detectors": det},
                                                 indent=1, ensure_ascii=False), encoding="utf-8")
    written.append(out / "numbers.json")

    if figures:
        try:
            import matplotlib

            matplotlib.use("Agg")
            import matplotlib.pyplot as plt
        except ImportError:
            print("matplotlib is not installed: tables written, figures skipped (pip install matplotlib)")
            return written
        plt.rcParams.update({"font.size": 8, "font.family": "DejaVu Sans"})
        if det:
            written += fig1(det, out, plt)
        written += fig2(nums, out, plt)
        written += fig3(nums, out, plt)
        plt.close("all")
    return written


def main() -> None:
    p = argparse.ArgumentParser(description=__doc__, formatter_class=argparse.RawDescriptionHelpFormatter)
    p.add_argument("results", type=Path, nargs="+", help="folders with one sub-folder per run")
    p.add_argument("--detectors", type=Path, default=None, help="flags.jsonl from scripts/detector_eval.py")
    p.add_argument("--cases", default="bench/cases")
    p.add_argument("--out", type=Path, default=Path("docs/paper/figures"))
    p.add_argument("--no-figures", action="store_true", help="tables only")
    args = p.parse_args()
    for path in make_all(args.results, args.out, args.cases, args.detectors, not args.no_figures):
        print(f"wrote {path}")


if __name__ == "__main__":
    main()
