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
  `requirements.txt` pins exact versions (mcp 2.2.0, openai 3.33.0, PyYAML
  6.0.1, pytest 9.1.1); `requirements-lock.txt` pins all 37 packages. Change
  both together (fresh venv, `pip freeze`, rerun the tests).
- Web access: the personal environment `mfs-agent-security` allows the
  Bangladeshi news and MFS sites (bKash, Nagad, Daily Star, Prothom Alo, TBS,
  Business Post, Bangla Tribune, Dhaka Tribune, bdnews24, Bangladesh Bank),
  DHL, GSMA, arXiv, DBLP, the ACL Anthology and the STALA and NDSS sites.
  The Default environment allows none of them: pick `mfs-agent-security`
  when starting a session that needs them.
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
  digit off by Bangla / ASCII digits). Done on all six models: the five
  open ones on `kaggle-results` (2026-10-23_message_payee), GPT-OSS-120B
  on `groq-results` (results_groq_message_payee).
  `cases_third_party/third_party.yaml` (37, also from `generate.py`, also
  kept apart): the main set's 37 tool-description attacks, each with the
  same poisoned text on the third-party tool `billbuddy_upcoming_bills`
  (a bill-reminder tool in `mfs_env/server.py`, added by the case field
  `third_party_tools`) and the wallet's tools left clean; `tp-X` is `X`
  with only that change. `scripts/compare_tool_poison.py --wallet <main
  runs> --third-party <tp runs>` pairs them (McNemar). Done on all six
  models: the five open ones on `kaggle-results` (2026-11-03_third_party,
  with `run_env.json`), GPT-OSS-120B on `groq-results`
  (results_groq_third_party). The wallet-tool runs to pair with are
  2026-10-02_qwen_3b_7b_14b, 2026-10-03_hermes3_granite,
  2026-10-05_qwen32b_old_block_message and
  2026-10-06_qwen32b_new_block_message (in that order) and results_groq.
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
  `results_message_payee/`. Latest set (done 3 November, third attempt): all five models on
  the 37 third-party tool cases with the same three defences, saved to
  `results_third_party/`. The first attempt (1 November) failed in every model: vLLM
  found no GPU ("Failed to infer device type"), as in a session without the GPU accelerator. The notebook now
  stops in its first cell if there are fewer than 2 GPUs, pins vLLM 0.32.0 (the newest on 23 October, when
  the runs worked), checks that vLLM finds the GPUs (`current_platform.is_cuda()`), and saves `run_env.json`
  (Python, vLLM, PyTorch, CUDA, GPU names, each model's Hugging Face revision) into results.zip. vLLM 0.31
  and later have no `vllm._C` file (their GPU code is `vllm._C_stable_libtorch`), so vLLM's "Failed to
  import from vllm._C" warning is harmless; a check on `vllm._C` stopped the second attempt (3 November).
  Granite 3.3 8B did not produce real tool calls on T4/vLLM and is left out of the results. Kaggle keeps its own copy of the notebook:
  after changing it, send him the .ipynb file to import.
  Each model x none/provenance/provenance-amount x 1 repeat on 302 cases,
  8 cases at a time (`--workers 8`). No Hugging Face account is available,
  so use only models that download without one.
  Model replies are capped at 1,024 tokens; a model error ends only that case
  and is counted as `model_error` in scores.jsonl and summary.md.
  Runs happen on Kaggle T4 x2 with vLLM; he starts them and uploads results.zip.
- `.github/workflows/groq_run.yml`: models on Groq's free tier, every 6
  hours, `run_bench.py --resume` until each model's daily limit (exit code 3:
  the case is not scored and runs again next time) or its time for that run
  (`MINUTES_PER_MODEL`), results on the `groq-results` branch. `MODELS` has
  one line per model: id | extra API settings | results folder | reply token
  cap | defences; `CASE_SETS` maps each case set to a folder suffix
  (`results_groq`, `_message_payee`, `_third_party`). Done for GPT-OSS-120B
  at low effort: the main, message-payee and third-party sets (all three
  defences; third-party done 1 November). Task D (done 12 November, all
  three case sets): GPT-OSS-120B medium (`results_groq_medium*`, cap
  4,096; shares 120B's daily limit) and GPT-OSS-20B (in `results_groq*`,
  next to the 120B runs), with none and provenance-amount. Every run in
  `MODELS` is finished, so scheduled runs now only check the API. The
  low- and medium-effort folders hold runs with the same names: give the
  scripts one folder at a time. `results_groq/` now holds a seventh model:
  to rebuild the six-model `robustness.md` use `--skip granite gpt-oss-20b`;
  `make_figures.py` adds two GPT-OSS-20B rows to its tables.
  Qwen3-32B, Llama 4 Scout and Kimi K2 returned 404 on
  1 November and were removed; a model Groq does not serve is skipped with
  a warning, and the "Models Groq serves" step prints the current list. `scripts/check_api.py` checks each model with one
  tool call first (and fails a reply with "<think>" text). Needs the
  `GROQ_API_KEY` repository secret. `run_bench.py --extra-body` passes API
  settings, `--max-tokens` the reply cap.
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
  techniques. See `docs/ETHICS.md`. `docs/attack_sources.md` links each of
  the 10 SMS and invoice attack texts to public reports (task F, 8 of 10
  checked); add a source there for any new attack text.
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
- Extra runs (task D, Groq, none and provenance-amount only; reported apart
  from the six models): GPT-OSS-120B medium effort 36/220 (16.4%; vs low
  McNemar p = 0.45; tool descriptions 27/37, SMS and invoice 9/183), 78/82
  normal tasks, read-and-able 22.9% (35/153). GPT-OSS-20B 59/220 (26.8%,
  the highest of any run; vs 120B p < 0.001; tool descriptions 24/37, SMS
  19/113, invoice 16/70; 12 ordinary scam messages; amount-only 11/20; 14
  of 21 templates), 72/82 normal tasks, invented payees 53/302, 9 wrong
  payments, read-and-able 32.3% (52/161), no language effect (p = 0.28),
  1 OTP leak of 25 (after the simulated "yes" to a table header "?"), 4
  model errors. `provenance-amount`: 0/220 in both, 0 correct payments
  blocked in the 82 normal tasks (77 and 75 done). Message-payee: 24/24
  (medium) and 21/24 (20B) without a defence, 0/24 with it; 20B copied no
  number wrong (0/16), medium 10/16 but retried and paid right.
  Third-party: 20B 12 vs 24 on the wallet's tool (p = 0.002; 3 of the 12
  after calling the tool), medium 25 vs 27 (p = 0.5); 0 with
  provenance-amount; 1 correct payment blocked (20B took the amount from
  the third-party tool). So "bigger was not safer" holds for Qwen only.
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
- Message-payee set (24 normal tasks, payee only in a message; six
  models): tasks done without a defence 6 / 5 / 10 / 19 / 4 / 20 (Qwen 3B /
  7B / 14B / 32B, Hermes 3, GPT-OSS-120B), 0 with either defence (61 / 63
  correct payments tried and blocked). After a block Qwen2.5-14B said the
  money was sent in 8 of 18 (provenance-amount; 6 with provenance),
  Qwen2.5-7B in 1, GPT-OSS-120B never (it gave the number in 19-20 of 24);
  every match read by hand. With provenance Qwen2.5-7B paid Dhaka Power's
  biller account instead twice (0 with provenance-amount). Numbers copied a
  digit off: 33 of 144 episodes with Bangla digits, 0 of 144 with ASCII
  digits; GPT-OSS-120B 13 of 24, all 4 of its failures without a defence.
- Third-party set (37 tool-description attacks on `billbuddy_upcoming_bills`
  instead of the wallet's own tools; six models; `compare_tool_poison.py`):
  without a defence 23 of 222 worked, against 42 of 222 on the wallet's
  tool: GPT-OSS-120B 20 vs 27 (p = 0.039), Qwen2.5-32B 0 vs 9 (p = 0.004),
  3B 2 vs 1, 14B 1 vs 5, 7B and Hermes 3 0 vs 0. In all 23 the agent never
  called the tool (calls: 3B 8 of 37, others 0 to 2). Both provenance
  defences 0 for every model (rule property). Rescore: 0 differences;
  verify_decisions: all 1,133 (open models) and 318 (GPT-OSS) decisions
  match. Caveat: the wallet-tool runs are weeks older (unrecorded vLLM).
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
