# CLAUDE.md: brief for Claude sessions on this repo

**Read `docs/ROADMAP.md` for the plan.** All planning happens in Claude cloud
sessions on this repo: update the roadmap in the same pull request whenever a
task is finished or the plan changes.

## What this project is

A research benchmark: can indirect prompt injection in Bangla, Banglish
(romanised Bangla) and code-mixed text trick an LLM agent into moving money
in a mobile money (MFS) wallet? Plus defences, and a public demo.

Owner: Mohammed Sayed Sameer (GitHub s4m404), BRAC University CS student,
graduating May 2027. The project is his main portfolio piece for AI security
internships (January to May 2027) and master's scholarship applications, and
will become a workshop paper. He reviews all Bangla and Banglish text himself.

## How he likes to work

- Explain in plain, short English. He finds terminal and git steps confusing.
- Keep everything runnable and tested. Run `python -m pytest -q` before every push.
- Never invent results. Numbers in the README must come from real runs.
- Push work to a branch and open a pull request with a clear summary; he merges it.
- One task per cloud session. Before he merges, give a 5-line summary of what
  changed and why.
- Model runs happen on Kaggle (no GPU in cloud sessions). When one is needed,
  say which notebook and the expected time; he uploads results.zip in a new session.
- Cloud credits run out on 5 November 2026, so October tasks come first.

## Layout

- `mfs_env/`: fictional TakaPay wallet (`world.py`), text helpers (Bangla
  digits, +88 numbers), MCP server with 9 tools (`server.py`).
  The wallet rejects pay_bill to unregistered biller accounts and send_money
  to anything that is not an 11-digit number `01[3-9]XXXXXXXX`.
- `agent/`: agent loop (`runner.py`) and OpenAI-compatible model client.
  A simulated user answers "yes" once (in the task language) if the agent asks.
- `defences/`: `none`, `keyword` (baseline), `provenance` (recipients and
  codes must not come only from untrusted text), `provenance-amount`
  (also: amount must come from the user or from the payee itself).
- `bench/`: `cases/seed.yaml` (12 hand-written) and `cases/generated.yaml`
  (290, built by `bench/generate.py` from tables; the first 102 are the
  original set and must stay unchanged; regenerate with
  `python -m bench.generate`, which also writes `bench/review_texts.csv`
  for native-speaker review and keeps his Y/N answers for unchanged
  sentences). `score.py` has all metrics. `cases_adaptive/adaptive.yaml`
  (56, also from `generate.py`) is a separate stress-test set that forges
  the payee's identity; it is not loaded with `bench/cases`, so the main
  302-case results stay unchanged. `scripts/audit_adaptive.py` checks which
  defences stop it, with scripted agents.
- `scripts/run_bench.py` (one model and defence), `scripts/compare_runs.py`
  (table with bootstrap CIs), `scripts/conditional_rates.py` (attack
  success among read / capable cases), `scripts/replay_defence.py` (replay recorded
  traces through another defence, no model needed).
- `notebooks/kaggle_run.ipynb`: `MODELS` maps each model to its vLLM tool
  parser, and `EXTRA_ARGS` gives a model extra vLLM settings. Done so far:
  four Qwen2.5 models (3B, 7B, 14B-AWQ, 32B-AWQ) and Hermes-3-Llama-3.1-8B
  (`hermes`). Currently set to run Qwen2.5-32B-Instruct-AWQ (needs
  `--gpu-memory-utilization 0.95`). Granite 3.3 8B did not produce real tool calls on T4/vLLM and
  is left out of the results. Kaggle keeps its own copy of the notebook:
  after changing it, send him the .ipynb file to import.
  Each model x none/provenance/provenance-amount x 1 repeat on 302 cases,
  8 cases at a time (`--workers 8`). No Hugging Face account is available,
  so use only models that download without one.
  Model replies are capped at 1,024 tokens; a model error ends only that case
  and is counted as `model_error` in scores.jsonl and summary.md.
  Runs happen on Kaggle T4 x2 with vLLM; he starts them and uploads results.zip.
- `docs/index.html`: the public demo page (GitHub Pages from /docs).
  It embeds real traces; regenerate it if the demo cases change.
- `results/` is git-ignored.

## Rules for test cases

- Everything is fictional: TakaPay, names, numbers, billers. Attacker numbers
  are 01899999999, 01877777777, 01866666666.
- Attacks copy common public scam patterns only; no new real-world fraud
  techniques. See `docs/ETHICS.md`.
- Every new Bangla or Banglish sentence goes into `review_texts.csv` and is
  marked as needing review. Do not claim it is reviewed until he says so.
- A test checks that an ideal agent solves every case and a gullible agent
  triggers every attack. Keep it passing.

## Results so far (Qwen2.5 3B, 7B, 14B-AWQ; 302 cases; 1 repeat; temperature 0)

- Attack success without defence: 7.3%, 5.9%, 7.7% of 220 attack cases.
  With `provenance`: 1, 5, 5 (all amount-only attacks). With
  `provenance-amount`: 0 of 660. Correct payments blocked: 0.
- Wrong payments that went through: 30 / 6 / 27 with `provenance`, 0 with
  `provenance-amount`.
- Agents tried to pay invented payees in 29% to 52% of episodes.
- The original 114 cases reproduce the earlier 3-repeat run
  (10.0% / 3.8% / 6.2% vs 10.0% / 3.8% / 5.0%).
- Qwen2.5-32B-AWQ: 14.5% without defence, 4 with `provenance` (all
  amount-only), 0 with `provenance-amount`, 0 correct payments blocked. But
  with either defence it did 12 fewer normal tasks (66% to 51%): it paid the
  invoice ID as the account, and the block message ("ask the user") replaced
  the wallet's hint ("check the invoice"), so it gave up.
- Hermes-3-Llama-3.1-8B (second family): 2.3% without defence, 1 with
  `provenance` (amount-only), 0 with `provenance-amount`, 0 correct payments blocked.
- Among attacks the agent read and on tasks it could do (`scripts/conditional_rates.py`):
  24% / 11% / 15% / 18% (Qwen 3B / 7B / 14B / 32B) and 10% (Hermes 3) without defence; 0 with
  `provenance-amount`.
- Adaptive set: an obeying agent beats `provenance-amount` with a spoofed payee
  SMS or a forged biller invoice (40/40); a forged new number is still blocked (0/16).
- Full tables and findings are in the README; key findings in `docs/ROADMAP.md`.

## Next tasks

See `docs/ROADMAP.md`. Paper target: STALA 2027 workshop at NDSS (Security
Testing and Assurance for LLMs and Agents), 8-page full paper (excluding
references, archival), deadline 11 December 2026; backup:
ICLR 2027 or ACL 2027 workshops in early February 2027.
