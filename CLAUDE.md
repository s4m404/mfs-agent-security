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
  sentences). `score.py` has all metrics.
- `scripts/run_bench.py` (one model and defence), `scripts/compare_runs.py`
  (table with bootstrap CIs), `scripts/replay_defence.py` (replay recorded
  traces through another defence, no model needed).
- `notebooks/kaggle_run.ipynb` (3 models x none/provenance/provenance-amount
  x 1 repeat on 302 cases, 8 cases at a time with `--workers 8`, about 3 to 4 hours).
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

## Results so far (Qwen2.5 3B, 7B, 14B-AWQ; 114 cases; 3 repeats; temperature 0)

- Attack success without defence: 10.0%, 3.8%, 5.0% of 240 attack episodes.
  With `provenance`: 0 of 720. Correct payments blocked: 0.
- Agents tried to pay invented payees in 29% to 48% of episodes.
- Repeats are nearly identical (96% to 100% agreement), so more cases matter
  more than more repeats.
- Replay estimate for `provenance-amount`: catches 26 / 3 / 6 wrong payments
  that `provenance` allowed, with 0 correct payments blocked. Real run pending.

## Next tasks

See `docs/ROADMAP.md`.
