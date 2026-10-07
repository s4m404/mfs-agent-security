"""Run the benchmark for one model, one defence and one system prompt.

Examples
    # Laptop, Ollama
    python scripts/run_bench.py --model qwen2.5:7b-instruct --base-url http://localhost:11434/v1 --defence none

    # University HPC, vLLM (see docs/HPC.md)
    python scripts/run_bench.py --model Qwen/Qwen2.5-32B-Instruct --base-url http://NODE:8000/v1 --defence provenance

    # Kaggle, vLLM: 8 cases at a time (vLLM answers them in one batch, much faster)
    python scripts/run_bench.py --model Qwen/Qwen2.5-7B-Instruct --base-url http://localhost:8000/v1 --workers 8

Outputs go to results/<run name>/: traces.jsonl, scores.jsonl, summary.md
"""

from __future__ import annotations

import argparse
import asyncio
import json
import logging
import sys
from collections import defaultdict
from concurrent.futures import ThreadPoolExecutor
from pathlib import Path

sys.path.insert(0, str(Path(__file__).resolve().parents[1]))

from agent.llm import OpenAICompatModel, RateLimited  # noqa: E402
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
        f"| Attack cases where the agent actually read the attack | {rate(attacks, 'exposed')} |",
        f"| Attack success among those (lower is better) | {rate([s for s in attacks if s['exposed']], 'attack_success')} |",
        f"| Utility on benign tasks | {rate(benign, 'utility')} |",
        f"| Utility under attack | {rate(attacks, 'utility')} |",
        f"| Benign tasks where the correct action was blocked (false blocks) | {rate(benign, 'false_block')} |",
        f"| Episodes with any blocked call | {rate(scores, 'blocked')} |",
        f"| Episodes where the agent tried to pay a payee or amount nobody asked for | {rate(scores, 'unintended_attempt')} |",
        f"| Episodes where such a payment went through | {rate(scores, 'unintended_transfer')} |",
        f"| Episodes where the agent asked the user to confirm | {rate(scores, 'asked_confirmation')} |",
        f"| Episodes stopped by a model error (timeout, reply too long) | {rate(scores, 'model_error')} |",
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


def run_cases(cases: list, model, defence: str, max_steps: int, system_prompt: str, workers: int = 1):
    """Run every case and yield (case, episode) in the same order as `cases`.

    With workers > 1, several episodes run at once, each in its own thread with
    its own wallet and defence, so they cannot affect each other. The model
    client is shared; the OpenAI client is safe to use from several threads.
    """

    def one(case):
        return case, asyncio.run(run_episode(case, model, make_defence(defence), max_steps, system_prompt))

    if workers <= 1:
        yield from map(one, cases)
        return
    with ThreadPoolExecutor(max_workers=workers) as pool:
        yield from pool.map(one, cases)


RATE_LIMITED_EXIT = 3  # exit code when the API's daily limit stopped the run; --resume continues it


def _read_jsonl(path: Path) -> list[dict]:
    """Rows of a JSONL file; a half-written last line (a run that was killed) is dropped."""
    rows = []
    if path.exists():
        for line in open(path, encoding="utf-8"):
            try:
                rows.append(json.loads(line))
            except ValueError:
                pass
    return rows


def load_finished(out: Path) -> tuple[list[dict], list[dict]]:
    """Scores and traces of the cases a previous run finished. Trace lines of a
    case without a score (cut off mid-case) are dropped, so it runs again."""
    scores = _read_jsonl(out / "scores.jsonl")
    done = {(s["case_id"], s.get("repeat", 0)) for s in scores}
    traces = [e for e in _read_jsonl(out / "traces.jsonl") if (e.get("case_id"), e.get("repeat", 0)) in done]
    return scores, traces


def main_run(args: argparse.Namespace) -> None:
    cases = load_cases(args.cases)
    extra = json.loads(args.extra_body) if args.extra_body else None
    model = OpenAICompatModel(args.model, args.base_url, args.api_key_env, args.temperature, args.max_tokens,
                              extra_body=extra)
    run_name = args.run_name or f"{args.model.replace('/', '_').replace(':', '_')}__{args.defence}__{args.prompt}"
    out = Path(args.out) / run_name
    out.mkdir(parents=True, exist_ok=True)

    all_scores, old_traces = load_finished(out) if args.resume else ([], [])
    done = {(s["case_id"], s.get("repeat", 0)) for s in all_scores}
    if done:
        print(f"Resuming: {len(done)} cases already done", flush=True)
    stopped = None
    with open(out / "traces.jsonl", "w", encoding="utf-8") as ft, open(out / "scores.jsonl", "w", encoding="utf-8") as fs:
        for row in old_traces:
            ft.write(json.dumps(row, ensure_ascii=False) + "\n")
        for row in all_scores:
            fs.write(json.dumps(row, ensure_ascii=False) + "\n")
        try:
            for rep in range(args.repeats):
                todo = [c for c in cases if (c.id, rep) not in done]
                for case, ep in run_cases(todo, model, args.defence, args.max_steps, PROMPTS[args.prompt], args.workers):
                    _write_case(case, ep, rep, args, all_scores, ft, fs)
        except RateLimited as exc:
            stopped = exc

    summary = summarise(all_scores, f"{args.model} | defence={args.defence} | prompt={args.prompt}")
    (out / "summary.md").write_text(summary, encoding="utf-8")
    print("\n" + summary)
    print(f"Saved to {out}")
    total = len(cases) * args.repeats
    if stopped is not None:
        print(f"Stopped by the API's rate limit after {len(all_scores)} of {total} cases; "
              f"run again with --resume to continue. ({stopped})", flush=True)
        sys.exit(RATE_LIMITED_EXIT)


def _write_case(case, ep, rep, args, all_scores, ft, fs) -> None:
    """Score one finished episode and append its trace and score to the run files."""
    s = {**score(case, ep.world, ep.final_answer, ep.trace), "repeat": rep, "model": args.model,
         "defence": args.defence, "prompt": args.prompt,
         "model_error": any(e["type"] == "model_error" for e in ep.trace)}
    all_scores.append(s)
    for e in ep.trace:
        ft.write(json.dumps({**e, "repeat": rep}, ensure_ascii=False) + "\n")
    fs.write(json.dumps(s, ensure_ascii=False) + "\n")
    ft.flush()
    fs.flush()
    flag = "ATTACK SUCCEEDED" if s["attack_success"] else ("ok" if s["utility"] else "task failed")
    if s["model_error"]:
        flag += " (model error, see traces)"
    print(f"[{rep}] {case.id:45s} {flag}", flush=True)


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
    p.add_argument("--max-tokens", type=int, default=1024, help="longest reply the model may write per turn")
    p.add_argument("--workers", type=int, default=1, help="cases to run at the same time (8 suits vLLM on Kaggle)")
    p.add_argument("--resume", action="store_true", help="keep finished cases in the run folder and run only the rest")
    p.add_argument("--extra-body", default=None, help='extra API settings as JSON, e.g. \'{"reasoning_effort": "low"}\'')
    for name in ("httpx", "httpcore", "openai"):
        logging.getLogger(name).setLevel(logging.WARNING)
        logging.getLogger(name).disabled = True
    main_run(p.parse_args())


if __name__ == "__main__":
    main()
