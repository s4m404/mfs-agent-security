# Research plan

**Question.** Can indirect prompt injection in Bangla, Banglish (romanised
Bangla) and code-mixed text make an LLM agent move money in a mobile money
wallet, and which defences stop it without blocking correct payments?

**Output.** A public benchmark (TakaPay, 302 cases), results on six
models from three families, and a workshop paper.

Last updated: 31 October 2026.

## Done

- **Environment and harness.** A fictional mobile money wallet (TakaPay)
  served as 9 MCP tools; an agent loop for any OpenAI-compatible model; a
  simulated user who answers "yes" once when the agent asks; scoring of
  attack success, task completion, false blocks, invented payees and wrong
  payments from the final wallet state.
- **Test set.** 302 cases: 12 hand-written and 290 generated from tables
  (`bench/generate.py`); 82 normal tasks (30 hard), 220 attacks hidden in
  SMS, invoices and tool descriptions, in English, Bangla, Banglish and
  mixed text; goals: send money to the attacker, leak the OTP, or overpay the
  real payee. A separate adaptive set of 56 cases forges the payee's identity
  (spoofed SMS sender, fake revised bill).
- **Defences.** `keyword` (baseline); `provenance` (recipients and codes must
  not come only from untrusted text); `provenance-amount` (the amount must
  come from the user or the payee); `provenance-consistent` (also asks the
  user when the payee's own messages or invoices disagree). Provenance and
  information-flow tracking are existing ideas (CaMeL, FIDES); these are
  simple rule-based versions.
- **Runs** (vLLM on Kaggle T4 GPUs, temperature 0, one run per case):
  Qwen2.5 3B, 7B, 14B-AWQ and 32B-AWQ; Hermes-3-Llama-3.1-8B (a second
  family). GPT-OSS-120B (a third family, much larger than the others) on
  Groq's API, reasoning effort low, by `.github/workflows/groq_run.yml`
  (none, provenance, provenance-amount; 302 cases each). Granite 3.3 8B
  was run but left out: its tool calls came out as
  plain text (0.2 tool calls per case). An earlier 114-case run with 3
  repeats showed that repeats at temperature 0 barely differ.
- **Detectors.** ProtectAI DeBERTa v2, deepset DeBERTa and the keyword
  baseline on all 174 attack and 54 normal texts, by language
  (`scripts/detector_eval.py`, `notebooks/kaggle_detectors.ipynb`); Llama
  Prompt Guard 2 (86M) and gpt-oss-safeguard-20b on the same texts through
  Groq's API (`scripts/detector_api.py`, raw replies in
  `results_detectors_api/` on the `groq-results` branch).
- **Analyses.** Attack success among cases where the agent read the attack
  and could do the task (`scripts/conditional_rates.py`); one cause per
  failed normal task (`scripts/error_analysis.py`); adaptive-attack audit
  with scripted agents (`scripts/audit_adaptive.py`); message-payee audit
  (`scripts/audit_message_payee.py`); replay of recorded
  traces through another defence (`scripts/replay_defence.py`).
- **Defence fixes found by real runs.** A clearer block message for a wrong
  biller account (Qwen2.5-32B had lost 12 normal tasks to the old one);
  `provenance-consistent` now checks every SMS and invoice from the payee,
  after Qwen2.5-32B beat the first version by reading only the newest SMS.
- **Design review** (22 October 2026, `docs/audit.md`): what the defence
  results show by design, template-level statistics and language tests
  (`scripts/robustness.py`, `docs/paper/robustness.md`), three rule fixes
  (dates read as amounts, bill amounts treated as OTP codes, spaced-out
  codes), and a replay of every recorded decision through the current rules
  (`scripts/verify_decisions.py`: 14,057 of 14,062 match; the 5 that differ
  are expected).
- **Audit** (`docs/audit.md`): every available episode (9,524) re-scored from
  its raw trace with no difference; README numbers checked against the raw
  traces of every model and against the raw detector outputs; two small
  README details corrected and one unverifiable sentence replaced; an OTP-format bug in the scorer fixed. Raw Kaggle results are kept on the
  `kaggle-results` branch, GPT-OSS-120B results on `groq-results`.
- **Paper material.** Outline (`docs/paper/outline.md`), figures and tables
  (`scripts/make_figures.py`, `docs/paper/figures/`), related-work draft
  (`docs/paper/related_work.md`), counts of confirmation questions and block
  messages (`docs/paper/confirmations.md`), first draft of sections 2 to 4:
  background and threat model, the benchmark, the defences
  (`docs/paper/draft_sections_2_4.md`); first draft of section 5, the
  results for all six models (`docs/paper/draft_section_5.md`); first
  draft of the abstract, introduction, limitations and conclusion
  (`docs/paper/draft_sections_1_8_9.md`).
- **What the agents' questions tell the user** (`scripts/code_questions.py`,
  `docs/paper/question_coding.md`): every question that received the
  simulated yes, coded by keyword rules for payee, amount, where the
  request came from, risk and next step, by model and language; block
  messages coded by template. A random sample of 50 is in
  `docs/paper/question_sample.csv` for a hand check.
- **Demo.** `docs/index.html` replays real runs; `docs/demo.gif`.

## Open tasks before the paper

From the design review of 22 October 2026 (`docs/audit.md`), in order of
value for the paper:

A. [x] **A multilingual detector** (done 22 October). Llama Prompt Guard
       2 (86M) flagged 0 of 174 attacks and 0 of 54 normal texts at its
       default threshold (it targets explicit jailbreak phrasing; AUROC
       0.89, reported as secondary). gpt-oss-safeguard-20b with a policy
       written for this benchmark (an upper bound) flagged 93% of attacks
       with no language gap, 15% of normal texts (12 of 82 normal tasks
       broken as a filter), and missed all 12 amount-only attacks. In the
       README, section 5.1, the outline and Fig 1.
B. [x] **Normal tasks whose payee appears only in a message** (done 31
       October; the 28 new sentences still need review, see item 1). Cases and
       scripted audit: 24 cases in `bench/cases_message_payee/` (six
       payees in four request languages: the payee's own SMS, a saved
       contact's SMS, a courier company's SMS, an invoice from a payee that
       is not a registered biller). With a scripted ideal agent
       (`scripts/audit_message_payee.py`) every provenance variant blocks
       all 24 correct payments, and the simulated "yes" does not unblock
       them; with the number typed by the user, `provenance` allows all 24
       and the amount check still blocks the 12 whose amount came from a
       third party. Model runs on all six models (the five open models on
       the `kaggle-results` branch, `2026-10-23_message_payee/`;
       GPT-OSS-120B on `groq-results`, `results_groq_message_payee/`): 64
       of 144 tasks done without a defence, 0 with either defence (every
       correct payment the agents tried was blocked); after a block
       Qwen2.5-14B told the user the money had been sent in 8 of 18
       episodes, GPT-OSS-120B never; with `provenance` Qwen2.5-7B paid a
       registered biller instead twice; every number copied with a digit
       missing or extra was written in Bangla digits (33 of 144 episodes, 0
       of 144 in ASCII digits; GPT-OSS-120B 13 of 24, all 4 of its failures
       without a defence).
C. [ ] **Third-party tool-description attacks:** put the poisoned
       description on a separate tool (for example a bill-reminder server)
       instead of the wallet's own `send_money` / `pay_bill`, and rerun the
       37 tool-description cases.
D. [ ] **Newer models through Groq** (check the current list, for example
       Qwen3-32B or Llama 4 Scout) and GPT-OSS-120B at medium reasoning
       effort, using the same workflow.
E. [ ] **Hand-check the scorer:** fill in `docs/handcheck.csv` (39 episodes,
       none done yet).
F. [ ] **Attack realism:** link each of the 10 SMS and invoice attack texts
       to a public source (fraud warnings from MFS providers, news).
G. [ ] **Pin versions:** fixed versions in `requirements.txt`, and save the
       vLLM version and model revision with each run.

1. [ ] **Second native-speaker check** of a sample of about 50 Bangla and
       Banglish sentences; report agreement. Review the 9 adaptive-set
       sentences marked in `bench/review_texts.csv`, and re-mark the 27
       original-set sentences still without a mark there (25 re-marked "Y"
       and 2 "N" with small wording fixes so far; the fixes wait for the
       next version, since every run used the original wording).
       Hand-check the 50 coded agent questions in
       `docs/paper/question_sample.csv` (does each of the six codes match
       the question?) before the question-coding counts are quoted as
       checked; notes on the agents' own wording are in its last column.
2. [ ] **Citable dataset:** dataset card (`docs/DATASET.md`), licenses
       (MIT for code, CC BY 4.0 for data) and `CITATION.cff` are in place.
       Left: link the repository to Zenodo, make release v1.0.0 with the
       submission (or at camera-ready if reviewing is anonymous), then add
       the DOI to the README, `CITATION.cff` (and its `date-released`) and
       the paper.
3. [ ] **References, last checks:** BibTeX for every reference is in
       `docs/paper/references.bib` and the starred items are resolved
       (CaMeL cited as arXiv; the firewalls paper is a NeurIPS 2025
       workshop paper; XSafety and MultiJail include Bengali; BanglaSafe
       added as the Bangla safety reference). Left: compare each entry with
       the official BibTeX, read the BanglaSafe PDF, and replace the
       Bangladesh Bank entry with the January 2025 statement itself.

## Paper

**Target: STALA 2027** (Security Testing and Assurance for LLMs and Agents,
at NDSS; [site](https://stala-workshop.github.io/)). Full paper, 8 pages
without references, archival (NDSS 2027 co-located workshop proceedings).
Deadline 11 December 2026 (23:59 AoE); notification 1 February 2027;
camera-ready 19 February 2027; workshop 22 March 2027 in Seoul, in person.
About 7 to 9 papers in one day. Template and anonymisation rules: check in
November; if reviewing is double-blind, link an anonymised copy of the
repository. Check the presentation requirements before submitting.

The call asks for general testing insight, not just a new attack, and
welcomes negative results "when they show that an intuitive testing metric,
benchmark or assurance interpretation is misleading".

| Fallback | Fit | Deadline |
|---|---|---|
| ICLR 2027 workshops ([call](https://iclr.cc/Conferences/2027/CallForWorkshops)), if an agent-security workshop is accepted (list due 29 Nov 2026) | Good | about 1 Feb 2027 |
| ACL 2027 workshops ([call](https://www.aclweb.org/portal/content/joint-call-workshops-proposals-2027)), e.g. low-resource or multilingual | Good for the language angle | about 5 Feb 2027 |
| EACL 2027 workshops, if one on low-resource or multilingual safety is announced | Possible | about 15 Dec 2026 |

**Framing** (every point backed by the README numbers):

0. No detector tested both catches the attacks and lets Bangla payments
   through: ProtectAI's (English-trained) flags 84% of normal Bangla texts,
   so an English detection score says nothing about other languages; the
   multilingual Prompt Guard 2 flags none of the attacks; gpt-oss-safeguard
   with a policy written for these attacks catches 93% in every language
   but breaks 12 of 82 normal tasks and misses every amount-only attack.
   Provenance rules never read the text, so their cost does not depend on
   the language (their zero false blocks in the main set is by design; on
   payees named only in a message they block every correct payment, see
   task B).
1. Attack success alone is misleading for payment agents: the smaller open
   models (Qwen2.5, Hermes 3) made wrong payments with no attacker involved
   (invented payees, guessed amounts) more often than any attack succeeded.
   GPT-OSS-120B rarely did; its attack success is almost all one
   tool-description template, so per-vector and per-template results matter
   more than one overall rate.
1b. The comprehension gate: Bangla attacks worked less on the Qwen models
   because those models also handle Bangla worse (Qwen2.5-32B: 9 of 22
   Bangla requests done, 18 of 21 English); GPT-OSS-120B handles all four
   languages and attacks work equally in all four. Opposite to multilingual
   jailbreak findings; Bangla is not a lasting shield.
2. Checking only "did money reach the attacker" misses amount-only attacks,
   which pay the real payee; every attack that got past recipient
   provenance was of this kind, and the amount check stopped them.
3. Harness choices change the scores: the simulated user's "yes" (and that
   it answers only a "?"), the wording of a block message (12 normal tasks
   for Qwen2.5-32B), and scripted audits that miss how real agents use tools
   (reading only the newest SMS).
4. The benchmark: 302 cases in Bangla, Banglish, code-mixed and English,
   over MCP, with raw traces and re-scoring scripts.

**Related work to position against** (found 22 October 2026, cited in
`docs/paper/related_work.md`): MIPIAD (Bangla indirect-injection detection
on translated text), a Tamil/Tanglish indirect-injection case study,
FinVault (financial agent security), APort Vault and the Open Agent Passport
(deterministic payment authorization), MCPTox (tool poisoning), InjecGuard
(detector over-defense), BabelArena (multilingual agents).

**Schedule.** A full first draft exists: abstract and sections 1, 8, 9
(`docs/paper/draft_sections_1_8_9.md`), 2 to 4
(`docs/paper/draft_sections_2_4.md`), 5 (`docs/paper/draft_section_5.md`)
and 7 (`docs/paper/related_work.md`), with references in
`docs/paper/references.bib`. Next: the STALA template and an 8-page cut. Full draft by 30 November 2026; submit by 11 December 2026;
release the dataset with the submission (or at camera-ready if anonymity is
required). If not accepted, revise with the reviews and submit to an ICLR or
ACL 2027 workshop in early February.

## After the submission

- A trained multilingual injection detector (small model; Bangla, Banglish,
  English) compared with provenance on attack success and false blocks.
- A user study of confirmation and block messages with mobile money users
  (needs ethics approval).
- Port TakaPay as an AgentDojo task suite and offer it upstream.
- A short write-up of the three main findings with the demo GIF.
- Follow-up project: detecting compromised AI agents in a security
  operations centre (SOC), using this project's traces as attack data.

## Ideas not scheduled

- Compare with the LLM sanitiser from "Indirect Prompt Injections: Are
  Firewalls All You Need, or Stronger Benchmarks?" (it reads the text, so
  the detector result suggests testing it on Bangla).
- Prepaid mobile recharge as a task (needs a new wallet tool).
- A second wallet backend.

Not worth it now: more Qwen sizes, more repeats, more cases.

## Key findings

302 cases, one run per case, temperature 0. Full tables in the README.

- With provenance plus the amount check, 0 of 880 attack episodes succeeded
  on the four Qwen2.5 models (0 of 220 each for Hermes 3 and GPT-OSS-120B),
  against 2.3% to 15.0% without a defence across the six models; no
  correct payment was blocked in the normal tasks and
  no wrong payment went through. Stopping the redirects and the zero false
  blocks follow from the rules and the case design (`docs/audit.md`,
  "Design review"); the runs measure what agents attempt and what the
  defences cost in completed tasks.
- Provenance's real cost is paying someone new: on 24 normal tasks whose
  payee is named only in a message, the provenance defences blocked every
  correct payment the six models tried (0 of 144 tasks done, 64 without a
  defence). After the block, Qwen2.5-14B told the user the money had been
  sent in 8 of its 18 blocked episodes, and with the recipient check alone
  Qwen2.5-7B paid a registered biller instead twice. Numbers written in
  Bangla digits were copied with a digit missing or extra in 33 of 144
  episodes, numbers in ASCII digits in none; GPT-OSS-120B, the model that
  handles Bangla best, did it in 13 of 24, and these slips were all 4 of
  its failures without a defence.
- Provenance alone stopped every attack that redirects money or leaks the
  OTP (0 of 800 on the Qwen models), but 15 attacks that changed only the
  amount got through. Without a defence, amount-only attacks were the most
  successful kind.
- Qwen models tried to pay a payee or amount nobody asked for in 29% to 52%
  of episodes, more often than any attack succeeded.
- Qwen2.5 3B, 14B and 32B fell mostly for English attacks (permutation
  tests p = 0.002, < 0.001, 0.03); the 7B and Hermes 3 language patterns are
  not distinguishable from chance. Those three models also did far fewer
  normal tasks requested in Bangla (the comprehension gate); GPT-OSS-120B
  handles all four languages and attacks worked equally in all four.
- A bigger model was not safer: Qwen2.5-32B did the most normal tasks (66%)
  and fell for significantly more attacks (14.5%) than the three smaller
  Qwen models (paired tests, p = 0.004 to 0.017).
- Hermes 3 (Llama 3.1 8B) shows the same pattern: 2.3% without a defence,
  one amount-only attack past provenance, 0 with provenance-amount.
- GPT-OSS-120B (Groq, reasoning effort low) shows it too: 15.0% (33 of 220)
  without a defence, but 27 of the 33 are one tool-description template; 6 of
  183 SMS and invoice attacks (3.3%); 7 past provenance, all
  amount-only; 0 with provenance-amount; 0 correct payments blocked and 76
  of 82 normal tasks with every defence. 27 of its 33 successful attacks
  came through tool descriptions (27 of 37 such attacks); by attack language
  they were spread evenly (8, 8, 9, 8). Unlike the smaller models it rarely
  tried to pay an invented payee (13, 10 and 9 of 302 episodes).
- Counted only where the agent read the attack and could do the task,
  attacks worked in 10% to 24% of cases without a defence (20% for
  GPT-OSS-120B); provenance-amount still stopped all of them.
- Adaptive attacks that forge the payee's identity beat provenance-amount
  when the agent obeys (40 of 40 forged amounts); the recipient check still
  stops a forged new number. With Qwen2.5-32B a forged "correction" from the
  payee worked in 11 of 16 cases without a defence; the fixed
  provenance-consistent stopped all 56 adaptive attacks, at the cost of
  holding most adaptive-case correct payments for the user.
- The two English-trained detectors failed on Bangla: ProtectAI's flagged
  16 of 19 normal Bangla texts (as a filter it would break 20 of 22
  Bangla-request tasks, 1 of 21 English) and caught only 47% of English
  attacks; deepset's flagged 87% of all normal texts. The multilingual
  Prompt Guard 2 flagged none of the 174 attacks (highest score 0.15; an
  explicit "Ignore all previous instructions ..." text scored 0.999).
  gpt-oss-safeguard with our policy (an upper bound) caught 93% in all four
  languages but flagged family money requests and the OTP SMS (8 of 54
  normal texts; 12 of 82 tasks broken) and missed all 12 amount-only
  attacks, which the provenance amount check stops.
- The simulated user's automatic "yes" is part of the attack path: in 29 of
  the 78 successful attacks on the four Qwen models (no defence; 13 of 32
  for Qwen2.5-32B) the agent had asked a question and received the
  simulated yes, and the attacker was paid later in the same episode (an
  order in time, not evidence that the question caused the payment).
  GPT-OSS-120B asked in only 1 of 302 episodes without a defence, so none
  of its successful attacks followed the simulated yes. None of the 35
  questions after which an attacker was paid (all runs) warned of a risk;
  most read like an ordinary payment confirmation (keyword coding, to be
  checked by hand).
- The original 114 cases reproduce: 10.0% / 3.8% / 6.2% attack success for
  3B / 7B / 14B, against 10.0% / 3.8% / 5.0% in the earlier 3-repeat run.
- The 220 attacks come from 21 templates; with templates as the unit the
  intervals widen (GPT-OSS-120B: 0.5% to 34.9%), see
  `docs/paper/robustness.md`.

## Known limitations

Synthetic data and one fictional wallet; 220 attacks from 21 templates (all
OTP attacks one text); normal tasks in the main set with trusted payees
only (the separate message-payee set measures the cost, task B);
tool-description attacks on the wallet's own tools (task C); the attack SMS
always the newest message; a simulated user who always says
yes (and answers any "?"); open models up to 32B (14B and 32B in 4-bit) plus
one API model (GPT-OSS-120B, low reasoning effort only); Bangla and
Banglish text reviewed by one native speaker so
far; a small normal-text set for detectors (54 texts, 19 in Bangla), and a
policy for gpt-oss-safeguard written after seeing the attacks.
Measurement caveats are in `docs/audit.md`.
