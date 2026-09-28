"""Run the benchmark for one model, one defence and one system prompt.

Examples
    # Laptop, Ollama
    python scripts/run_bench.py --model qwen2.5:7b-instruct --base-url http://localhost:11434/v1 --defence none

    # University HPC, vLLM (see docs/HPC.md)
    python scripts/run_bench.py --model Qwen/Qwen2.5-32B-Instruct --base-url http://NODE:8000/v1 --defence provenance

Outputs go to results/<run name>/: traces.jsonl, scores.jsonl, summary.md
"""

from __future__ import annotations

import argparse
import asyncio
import json
import logging
import sys
from collections import defaultdict
from pathlib import Path

sys.path.insert(0, str(Path(__file__).resolve().parents[1]))

from agent.llm import OpenAICompatModel  # noqa: E402
from agent.runner import PROMPTS, run_episode  # noqa: E402
from bench.cases import load_cases  # noqa: E402
from bench.score import score  # noqa: E402
from defences import DEFENCES, make_defence  # noqa: E402


def rate(rows: list[dict], key: str) -> str:
    if not rows:
        return "n/a"
    return f"{100 * sum(bool(r[key]) for r in rows) / len(rows):.1f}% (n={len(rows)})"


def summarise(scores: list[dict], title: str) -> str:
    attacks = [s for s in scores if s["is_attack"]]
    benign = [s for s in scores if not s["is_attack"]]
    lines = [
        f"# {title}",
        "",
        "| Metric | Value |",
        "| --- | --- |",
        f"| Attack success rate (lower is better) | {rate(attacks, 'attack_success')} |",
        f"| Utility on benign tasks | {rate(benign, 'utility')} |",
        f"| Utility under attack | {rate(attacks, 'utility')} |",
        f"| Benign tasks with a blocked call (false blocks) | {rate(benign, 'blocked')} |",
        "",
        "## Attack success by injection language",
        "",
        "| Injection language | Attack success |",
        "| --- | --- |",
    ]
    by_lang: dict[str, list[dict]] = defaultdict(list)
    for s in attacks:
        by_lang[s["injection_language"]].append(s)
    lines += [f"| {k} | {rate(v, 'attack_success')} |" for k, v in sorted(by_lang.items())]
    lines += ["", "## Attack success by vector", "", "| Vector | Attack success |", "| --- | --- |"]
    by_vec: dict[str, list[dict]] = defaultdict(list)
    for s in attacks:
        by_vec[s["injection_vector"]].append(s)
    lines += [f"| {k} | {rate(v, 'attack_success')} |" for k, v in sorted(by_vec.items())]
    return "\n".join(lines) + "\n"


async def main_async(args: argparse.Namespace) -> None:
    cases = load_cases(args.cases)
    model = OpenAICompatModel(args.model, args.base_url, args.api_key_env, args.temperature)
    run_name = args.run_name or f"{args.model.replace('/', '_').replace(':', '_')}__{args.defence}__{args.prompt}"
    out = Path(args.out) / run_name
    out.mkdir(parents=True, exist_ok=True)

    all_scores = []
    with open(out / "traces.jsonl", "w", encoding="utf-8") as ft, open(out / "scores.jsonl", "w", encoding="utf-8") as fs:
        for rep in range(args.repeats):
            for case in cases:
                ep = await run_episode(case, model, make_defence(args.defence), args.max_steps, PROMPTS[args.prompt])
                s = {**score(case, ep.world, ep.final_answer, ep.trace), "repeat": rep, "model": args.model,
                     "defence": args.defence, "prompt": args.prompt}
                all_scores.append(s)
                for e in ep.trace:
                    ft.write(json.dumps({**e, "repeat": rep}, ensure_ascii=False) + "\n")
                fs.write(json.dumps(s, ensure_ascii=False) + "\n")
                flag = "ATTACK SUCCEEDED" if s["attack_success"] else ("ok" if s["utility"] else "task failed")
                print(f"[{rep}] {case.id:45s} {flag}")

    summary = summarise(all_scores, f"{args.model} | defence={args.defence} | prompt={args.prompt}")
    (out / "summary.md").write_text(summary, encoding="utf-8")
    print("\n" + summary)
    print(f"Saved to {out}")


def main() -> None:
    p = argparse.ArgumentParser(description=__doc__, formatter_class=argparse.RawDescriptionHelpFormatter)
    p.add_argument("--model", required=True)
    p.add_argument("--base-url", default="http://localhost:11434/v1")
    p.add_argument("--api-key-env", default="OPENAI_API_KEY")
    p.add_argument("--defence", default="none", choices=sorted(DEFENCES))
    p.add_argument("--prompt", default="guarded", choices=sorted(PROMPTS))
    p.add_argument("--cases", default="bench/cases")
    p.add_argument("--out", default="results")
    p.add_argument("--run-name", default=None)
    p.add_argument("--repeats", type=int, default=1)
    p.add_argument("--max-steps", type=int, default=8)
    p.add_argument("--temperature", type=float, default=0.0)
    logging.getLogger("httpx").setLevel(logging.WARNING)
    asyncio.run(main_async(p.parse_args()))


if __name__ == "__main__":
    main()
