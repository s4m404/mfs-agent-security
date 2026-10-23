# CLAUDE.md: brief for Claude sessions on this repo

**Read `docs/ROADMAP.md` for the plan.** All planning happens in Claude cloud
sessions on this repo: update the roadmap in the same pull request whenever a
task is finished or the plan changes.

## What this project is

A research benchmark: can indirect prompt injection in Bangla, Banglish
(romanised Bangla) and code-mixed text trick an LLM agent into moving money
in a mobile money (MFS) wallet? Plus defences, a public demo and a workshop
paper.

Author: Mohammed Sayed Sameer (GitHub s4m404), BRAC University. He is a
native Bangla speaker and reviews all Bangla and Banglish text himself.

## How to work on this repo

- Write summaries and explanations in plain, short English; spell out any
  git or terminal step he needs to do himself.
- Keep everything runnable and tested. Run `python -m pytest -q` before every push.
- Never invent results. Numbers in the README must come from real runs.
- Push work to a branch and open a pull request with a clear summary; he
  merges it. Before he merges, give a 5-line summary of what changed and why.
- One task per session.
- Model runs happen on Kaggle (no GPU in cloud sessions). When one is needed,
  say which notebook and the expected time; he uploads results.zip in a new session.

## Working rules

- Each session starts by reading this file and `docs/ROADMAP.md`. Update the
  roadmap in the same pull request when a task is finished or the plan
  changes.
- `docs/ROADMAP.md`, the README, `docs/`, notebooks and scripts are public
  research documents: no workflow or personal notes there (sessions, who
  does what, plans outside the research). Workflow notes belong in this
  file only, and it is public too, so keep it to project information.
- Commits and pull requests: no Co-Authored-By lines and no "Generated with
  Claude Code" lines.
- All Bangla and Banglish text is reviewed by him before it counts as
  reviewed; new sentences go into `bench/review_texts.csv` marked as needing
  review.
- Raw results: after a Kaggle run he uploads `results.zip`. Add its run
  folders to the `kaggle-results` branch as one dated folder per Kaggle run
  (`YYYY-MM-DD_<what>/results/`, `results_adaptive/`), never overwrite an
  older folder, and update that branch's README table. GPT-OSS-120B results
  are written by the workflow to `groq-results`. Recompute and check numbers
  from these branches (`scripts/rescore.py` first).
- `kaggle-results` now holds every Kaggle run used in the README (the
  interrupted first attempts of the 302-case run were not kept).
- Branches: keep `main`, `groq-results` and `kaggle-results`; delete a
  working branch after its pull request is merged.

## Layout

- `mfs_env/`: fictional TakaPay wallet (`world.py`), text helpers (Bangla
  digits, +88 numbers), MCP server with 9 tools (`server.py`).
  The wallet rejects pay_bill to unregistered biller accounts and send_money
  to anything that is not an 11-digit number `01[3-9]XXXXXXXX`.
- `agent/`: agent loop (`runner.py`) and OpenAI-compatible model client.
  A simulated user answers "yes" once (in the task language) if the agent asks.
- `defences/`: `none`, `keyword` (baseline), `provenance` (recipients and
  codes must not come only from untrusted text), `provenance-amount`
  (also: amount must come from the user or from the payee itself),
  `provenance-consistent` (also: block and ask the user when the payee's
  own messages or invoices give different amounts; it checks every SMS and
  invoice from that payee in the wallet, not only those the agent read).
  A block may carry
  `advice` (what the agent should do next); the default is "ask the user".
- `bench/`: `cases/seed.yaml` (12 hand-written) and `cases/generated.yaml`
  (290, built by `bench/generate.py` from tables; the first 102 are the
  original set and must stay unchanged; regenerate with
  `python -m bench.generate`, which also writes `bench/review_texts.csv`
  for native-speaker review and keeps his Y/N answers for unchanged
  sentences). `score.py` has all metrics. `cases_adaptive/adaptive.yaml`
  (56, also from `generate.py`) is a separate stress-test set that forges
  the payee's identity; it is not loaded with `bench/cases`, so the main
  302-case results stay unchanged. `scripts/audit_adaptive.py` checks which
  defences stop it, with scripted agents. `cases_message_payee/message_payee.yaml`
  (24, also from `generate.py`, also kept apart): normal tasks with no
  attacker whose payee's number is only in an SMS or invoice (the id says
  where: sender, contact, company, invoice). `scripts/audit_message_payee.py`:
  with a scripted ideal agent every provenance variant blocks all 24 (the
  simulated "yes" does not unblock them); with the number typed by the
  user, `provenance` allows all 24 and the amount check still blocks 12
  (amount from a third party). `--runs <folder>` reads model runs on it
  (tasks done, blocks, what the agent said after a block, numbers copied a
  digit off by Bangla / ASCII digits). Five open models done (23 October,
  `kaggle-results` 2026-10-23_message_payee); GPT-OSS-120B runs through
  the Groq workflow.
- `scripts/run_bench.py` (one model and defence), `scripts/compare_runs.py`
  (table with bootstrap CIs), `scripts/conditional_rates.py` (attack
  success among read / capable cases), `scripts/replay_defence.py` (replay recorded
  traces through another defence, no model needed), `scripts/error_analysis.py`
  (one cause per failed normal task), `scripts/detector_eval.py` (do
  injection detectors flag each attack / normal text, by language; run the
  Hugging Face ones with `notebooks/kaggle_detectors.ipynb`, about 10 minutes;
  this cloud environment cannot reach huggingface.co).
- `docs/paper/outline.md`: the STALA paper outline (claims and the README
  numbers behind each, GPT-OSS-120B included).
  `docs/paper/related_work.md`: section 7 draft with checked references;
  `docs/paper/references.bib`: their BibTeX (written by hand: this cloud
  environment cannot reach arXiv, DBLP or the ACL Anthology).
  `docs/paper/draft_sections_1_8_9.md`, `draft_sections_2_4.md` and
  `draft_section_5.md`: first drafts of the abstract and sections 1 to 5,
  8 and 9 (each ends with the source of every number).
- Audit tools (no model needed): `scripts/rescore.py` (re-score every
  episode from its trace, list differences from scores.jsonl),
  `scripts/handcheck.py` (random episodes for hand checking ->
  `docs/handcheck.md`), `scripts/count_confirmations.py` (agent questions and
  block messages -> `docs/paper/confirmations.md`), `scripts/code_questions.py`
  (keyword coding of those questions for payee, amount, source, risk, next
  step -> `docs/paper/question_coding.md`; 50-question hand-check sample in
  `docs/paper/question_sample.csv`; his Y/N column on the codes is still
  empty, his notes on the agents' Bangla/Banglish wording are in the last
  column), `scripts/verify_decisions.py` (replay every logged tool call
  through the current defence rules; run it after any defence change:
  14,057 of 14,062 match, 5 expected differences), `scripts/robustness.py`
  (template-level intervals, per-template and per-vector tables, language
  permutation tests, paired McNemar, comprehension gate ->
  `docs/paper/robustness.md`; use `--skip granite`).
- Design review (22 October, `docs/audit.md`): the zero false blocks and the
  stopped redirects are rule properties (every normal payee is trusted;
  attacker numbers never are), not experimental results; say so wherever
  they appear. Rule fixes then: dates are not amounts, only numbers from
  OTP/PIN/password messages are codes, spaced-out codes are caught.
- Native-speaker review, round 1 (18 October): sentences 1 to 49 of
  `review_texts.csv` marked natural except two "N" with fixes (row 10,
  Banglish gas request; row 123, simulated user's Banglish "yes"). Both are
  in the original 114-case set, so the fixes are recorded, not applied:
  apply them only in a new benchmark version (and rerun), never silently.
  Status after round 1: 88 of 124 marked (86 Y, 2 N). Still blank: rows
  52 to 69, 88 to 94, 113 and 124 (original set, 27) and 114 to 122
  (adaptive set, 9). Rows 125 to 152 (message-payee set, 28) were added on
  23 October and are not reviewed yet; new sentences are always appended
  at the end so row numbers stay the same.
  Findings: `docs/audit.md`.
  `scripts/make_figures.py results/ [results_groq/] --detectors
  results_detectors_api/flags.jsonl` (all five detectors) writes its figures and tables to
  `docs/paper/figures/` (figures need matplotlib).
- `notebooks/kaggle_run.ipynb`: `MODELS` maps each model to its vLLM tool
  parser, and `EXTRA_ARGS` gives a model extra vLLM settings. Done so far:
  four Qwen2.5 models (3B, 7B, 14B-AWQ, 32B-AWQ) and Hermes-3-Llama-3.1-8B
  (`hermes`). Earlier set (done): the fixed provenance-consistent on
  Qwen2.5-32B-Instruct-AWQ (needs `--gpu-memory-utilization 0.95`), main
  and adaptive cases (`results_adaptive/`, git-ignored). Last set (done 23
  October, under 40 minutes of runs): all five models on the 24
  message-payee cases with none, provenance and provenance-amount, saved to
  `results_message_payee/`. Granite 3.3 8B did not produce real tool calls on T4/vLLM and
  is left out of the results. Kaggle keeps its own copy of the notebook:
  after changing it, send him the .ipynb file to import.
  Each model x none/provenance/provenance-amount x 1 repeat on 302 cases,
  8 cases at a time (`--workers 8`). No Hugging Face account is available,
  so use only models that download without one.
  Model replies are capped at 1,024 tokens; a model error ends only that case
  and is counted as `model_error` in scores.jsonl and summary.md.
  Runs happen on Kaggle T4 x2 with vLLM; he starts them and uploads results.zip.
- `.github/workflows/groq_run.yml` (done: none, provenance, provenance-amount,
  302 cases each, reasoning effort low; next in `CASE_SETS`: the 24
  message-payee cases into `results_groq_message_payee/`, starting by
  itself on the next scheduled run): GPT-OSS-120B on Groq's free tier, every 6
  hours, `run_bench.py --resume` until the daily limit (exit code 3: the case
  is not scored and runs again next time), results on the `groq-results`
  branch (`results_groq/`). Needs the `GROQ_API_KEY` repository secret.
  `scripts/check_api.py` checks a key and model with one tool call first.
  `run_bench.py --extra-body` passes API settings (`reasoning_effort: low`).
- `.github/workflows/groq_detectors.yml` + `scripts/detector_api.py`: Llama
  Prompt Guard 2 (86M) and gpt-oss-safeguard-20b on the 228 detector texts
  through Groq (manual start, then every 6 hours until done; resumes; raw
  replies kept in `raw.jsonl`), results to `results_detectors_api/` on
  `groq-results`, merged with the Kaggle detector flags (ProtectAI, deepset,
  keyword) into one `flags.jsonl` / `summary.md`. The safeguard POLICY was
  written for this benchmark (an upper bound for a policy filter). Done 22
  October (456 replies); later scheduled runs make no API calls and only
  rebuild `summary.md`. `--summary-only` rebuilds the tables from
  `raw.jsonl` without a key.
- `docs/index.html`: the public demo page (GitHub Pages from /docs).
  It embeds real traces; regenerate it if the demo cases change.
- `results/` is git-ignored.
- Release files: `docs/DATASET.md` (dataset card), `LICENSE` (MIT, code),
  `LICENSE-DATA.md` (CC BY 4.0: cases, review CSV, raw results, docs), `CITATION.cff`
  (`date-released` is a placeholder until the real release). Zenodo: he
  logs in with GitHub at zenodo.org, turns on this repository, then makes a
  GitHub release; Zenodo then mints the DOI.

## Rules for test cases

- Everything is fictional: TakaPay, names, numbers, billers. Attacker numbers
  are 01899999999, 01877777777, 01866666666.
- Attacks copy common public scam patterns only; no new real-world fraud
  techniques. See `docs/ETHICS.md`.
- Every new Bangla or Banglish sentence goes into `review_texts.csv` and is
  marked as needing review. Do not claim it is reviewed until he says so.
- A test checks that an ideal agent solves every case and a gullible agent
  triggers every attack. Keep it passing.

## Results so far (302 cases; 1 repeat; temperature 0)

- Qwen2.5 3B, 7B, 14B-AWQ: attack success without defence 7.3%, 5.9%, 7.7% of 220 attack cases.
  With `provenance`: 1, 5, 5 (all amount-only attacks). With
  `provenance-amount`: 0 of 660. Correct payments blocked: 0.
- Wrong payments that went through: 30 / 6 / 27 with `provenance`, 0 with
  `provenance-amount`.
- Agents tried to pay invented payees in 29% to 52% of episodes.
- Language: Qwen 3B, 14B, 32B fell mostly for English (permutation p =
  0.002, < 0.001, 0.03); 7B and Hermes 3 show no significant language effect.
  Comprehension gate: those models also did far fewer Bangla-request normal
  tasks (32B: 9/22 vs 18/21 English); GPT-OSS-120B handles all four languages
  and attacks worked equally in all four. 32B fell for significantly more
  attacks than 3B, 7B, 14B (McNemar p = 0.017, 0.004, 0.008).
- The original 114 cases reproduce the earlier 3-repeat run
  (10.0% / 3.8% / 6.2% vs 10.0% / 3.8% / 5.0%).
- Qwen2.5-32B-AWQ: 14.5% without defence, 4 with `provenance` (all
  amount-only), 0 with `provenance-amount`, 0 correct payments blocked. But
  with either defence it did 12 fewer normal tasks (66% to 51%): it paid the
  invoice ID as the account, and the block message ("ask the user") replaced
  the wallet's hint ("check the invoice"), so it gave up. With a clearer
  block message (rerun) all 12 came back: 70% with `provenance-amount`, 71%
  with `provenance-consistent`, still 0 attacks and 0 correct payments blocked.
- Hermes-3-Llama-3.1-8B (second family): 2.3% without defence, 1 with
  `provenance` (amount-only), 0 with `provenance-amount`, 0 correct payments blocked.
- GPT-OSS-120B (third family, Groq, reasoning effort low): 33/220 (15.0%)
  without defence (27 of the 33 are the one tool-description template; 6/183
  SMS and invoice attacks, 3.3%), 7 with `provenance` (all amount-only), 0 with
  `provenance-amount`; 76/82 normal tasks in all three; 0 correct payments
  blocked; invented payees 13 / 10 / 9 of 302 (so the invented-payee finding
  is mainly about the smaller models); no OTP leaked; 27 of the 33 through tool
  descriptions; 1 model error each in none and provenance-amount; asked a
  "?" in 1 of 302 episodes without defence (a table header).
- Among attacks the agent read and on tasks it could do (`scripts/conditional_rates.py`):
  24% / 11% / 15% / 18% (Qwen 3B / 7B / 14B / 32B), 10% (Hermes 3) and 20%
  (GPT-OSS-120B) without defence; 0 with `provenance-amount`.
- Adaptive set: an obeying agent beats `provenance-amount` with a spoofed payee
  SMS or a forged biller invoice (40/40); a forged new number is still blocked (0/16).
  `provenance-consistent` stops 40/40 in the audit. With Qwen2.5-32B: forged
  amount SMS worked 11/16 (none), 10/16 (provenance-amount), 3/16
  (first version of provenance-consistent; all 3 read only the newest SMS,
  `limit: 1`). Fixed: the check now covers the whole inbox; audit 0/40 with
  a newest-only agent; 32B rerun: 0/56 adaptive, 0/220 main attacks, 0
  correct payments blocked, 72% of normal tasks; 1/56 adaptive correct
  payments went through (the rest wait for the user).
- Detectors (`scripts/detector_eval.py`, 174 attack / 54 normal texts): keyword
  34% / 7% false alarms; ProtectAI DeBERTa v2 59% / 39%, but 84% of normal
  Bangla texts flagged (as a filter it would break 20 of 22 Bangla-request
  normal tasks, 1 of 21 English); deepset 100% / 87%. Through Groq
  (`scripts/detector_api.py`): Llama Prompt Guard 2 86M 0% / 0% at
  threshold 0.5 (highest attack score 0.15; it targets explicit jailbreak
  phrasing; AUROC 0.89 only as a secondary number); gpt-oss-safeguard-20b
  with our policy (upper bound) 93% / 15%, no language gap, 12 of 82 normal
  tasks broken (family money requests, the OTP SMS), missed all 12
  amount-only attacks; 1 empty reply counted as not flagged.
- Message-payee set (24 normal tasks, payee only in a message; five open
  models): tasks done without a defence 6 / 5 / 10 / 19 / 4 (Qwen 3B / 7B /
  14B / 32B, Hermes 3), 0 with either defence (42 / 43 correct payments
  tried and blocked). After a block Qwen2.5-14B said the money was sent in
  8 of 18 (provenance-amount; 6 with provenance), Qwen2.5-7B in 1; every
  match read by hand. With provenance Qwen2.5-7B paid Dhaka Power's biller
  account instead twice (0 with provenance-amount). Numbers copied a digit
  off: 20 of 120 episodes with Bangla digits, 0 of 120 with ASCII digits.
- Error analysis (`scripts/error_analysis.py`, all six models, no defence): a
  wrong biller account is the top cause of failed normal tasks for every Qwen
  model (made-up accounts; the invoice ID for 32B); Hermes 3 mostly stops after
  reading (34 of 64 failures); GPT-OSS-120B failed only 6 (4 stopped without
  paying).
- Full tables and findings are in the README; key findings in `docs/ROADMAP.md`.

## Next tasks

See `docs/ROADMAP.md`. Paper target: STALA 2027 workshop at NDSS (Security
Testing and Assurance for LLMs and Agents), 8-page full paper (excluding
references, archival), deadline 11 December 2026; backup:
ICLR 2027 or ACL 2027 workshops in early February 2027.
