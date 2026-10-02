# CLAUDE.md: brief for Claude sessions on this repo

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
  for native-speaker review). `score.py` has all metrics.
- `scripts/run_bench.py` (one model and defence), `scripts/compare_runs.py`
  (table with bootstrap CIs), `scripts/replay_defence.py` (replay recorded
  traces through another defence, no model needed).
- `notebooks/kaggle_run.ipynb` (3 models x none/provenance x 3 repeats) and
  `notebooks/kaggle_run_amount.ipynb` (provenance-amount, 1 repeat).
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

## Next tasks, in order

1. Grow the test set from 114 to about 300 cases in `bench/generate.py`:
   new tasks (e.g. paying a landlord named in the prompt, mobile recharge,
   splitting a bill), new attack styles (fake MFS agent or cash-out notices,
   fake delivery or customs fees, fake job or prize offers, longer chat-style
   messages, attacks that change only the amount), and more hard benign cases
   that look suspicious but are legitimate. Keep languages balanced.
   Output the new sentences in `review_texts.csv` for his review.
2. Update the README test-set table and the notebooks for the bigger set.
3. After new results arrive: update README, the demo page and `compare_runs.py` output.
4. Later: trained multilingual injection detector as a third defence; paper draft.
