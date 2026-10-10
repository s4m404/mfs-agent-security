# Research plan

**Question.** Can indirect prompt injection in Bangla, Banglish (romanised
Bangla) and code-mixed text make an LLM agent move money in a mobile money
wallet, and which defences stop it without blocking correct payments?

**Output.** A public benchmark (TakaPay, 302 cases), results on several
open models, and a workshop paper.

Last updated: 10 October 2026.

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
  family). Granite 3.3 8B was run but left out: its tool calls came out as
  plain text (0.2 tool calls per case). An earlier 114-case run with 3
  repeats showed that repeats at temperature 0 barely differ.
- **Detectors.** ProtectAI DeBERTa v2, deepset DeBERTa and the keyword
  baseline on all 174 attack and 54 normal texts, by language
  (`scripts/detector_eval.py`, `notebooks/kaggle_detectors.ipynb`).
- **Analyses.** Attack success among cases where the agent read the attack
  and could do the task (`scripts/conditional_rates.py`); one cause per
  failed normal task (`scripts/error_analysis.py`); adaptive-attack audit
  with scripted agents (`scripts/audit_adaptive.py`); replay of recorded
  traces through another defence (`scripts/replay_defence.py`).
- **Defence fixes found by real runs.** A clearer block message for a wrong
  biller account (Qwen2.5-32B had lost 12 normal tasks to the old one);
  `provenance-consistent` now checks every SMS and invoice from the payee,
  after Qwen2.5-32B beat the first version by reading only the newest SMS.
- **Audit** (`docs/audit.md`): every available episode (6,930) re-scored from
  its raw trace with no difference; README numbers checked against the raw
  traces of every model and against the raw detector outputs; two small
  README details corrected; an OTP-format bug in the scorer fixed. Raw Kaggle results are kept on the
  `kaggle-results` branch, GPT-OSS-120B results on `groq-results`.
- **Paper material.** Outline (`docs/paper/outline.md`), figures and tables
  (`scripts/make_figures.py`, `docs/paper/figures/`), related-work draft
  (`docs/paper/related_work.md`), counts of confirmation questions and block
  messages (`docs/paper/confirmations.md`).
- **Demo.** `docs/index.html` replays real runs; `docs/demo.gif`.

## Open tasks before the paper

1. [ ] **GPT-OSS-120B on Groq** (a third model family, larger than any open
       model run so far). `.github/workflows/groq_run.yml` runs every 6
       hours and resumes until the free tier's daily token limit (about 85
       cases a day). Order: none (done, 302 cases), provenance-amount (in
       progress), provenance. Expected to finish around 17 October.
       Setting: reasoning effort low (state this in the paper).
2. [ ] **Complete the raw-data archive.** Add the earlier 114-case
       3-repeat run to the `kaggle-results` branch and check the two claims
       that depend on it: its attack success (10.0% / 3.8% / 5.0%) and the
       repeat agreement (96% to 100%). If its output is no longer available,
       report those numbers as from the earlier run, not re-checked.
3. [ ] **Do the agents' questions let a user say no?** The simulated user
       always says yes, and 29 of the 78 successful attacks on the four Qwen
       models (no defence) came right after that "yes". Code each confirmation question and block
       message for what a user would need (payee, amount, where the number
       or amount came from, the risk, what to do), by language. Counts so
       far: `docs/paper/confirmations.md`. A user study would be a separate
       follow-up.
4. [ ] **Second native-speaker check** of a sample of about 50 Bangla and
       Banglish sentences; report agreement. Review the 9 adaptive-set
       sentences marked in `bench/review_texts.csv`.
5. [ ] **Citable dataset:** a GitHub release linked to Zenodo (DOI) with a
       short dataset card.
6. [ ] **References:** export BibTeX and check the starred items in
       `docs/paper/related_work.md`; find a Bangla NLP safety paper for the
       introduction or soften that sentence.

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

0. The two off-the-shelf injection detectors tested do not transfer to
   Bangla: ProtectAI's flags 84% of normal Bangla texts, so an English
   detection score says nothing about other languages; provenance rules,
   which never read the text, blocked no correct payment in any language.
1. Attack success alone is misleading for payment agents: models made wrong
   payments with no attacker involved (invented payees, guessed amounts)
   more often than any attack succeeded.
2. Checking only "did money reach the attacker" misses amount-only attacks,
   which pay the real payee; every attack that got past recipient
   provenance was of this kind, and the amount check stopped them.
3. Harness choices change the scores: the simulated user's "yes" (and that
   it answers only a "?"), the wording of a block message (12 normal tasks
   for Qwen2.5-32B), and scripted audits that miss how real agents use tools
   (reading only the newest SMS).
4. The benchmark: 302 cases in Bangla, Banglish, code-mixed and English,
   over MCP, with raw traces and re-scoring scripts.

**Schedule.** Full draft by 30 November 2026; submit by 11 December 2026;
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
  on the four Qwen2.5 models (0 of 220 for Hermes 3), against 5.9% to 14.5%
  without a defence; no correct payment was blocked in the normal tasks and
  no wrong payment went through.
- Provenance alone stopped every attack that redirects money or leaks the
  OTP (0 of 800 on the Qwen models), but 15 attacks that changed only the
  amount got through. Without a defence, amount-only attacks were the most
  successful kind.
- Qwen models tried to pay a payee or amount nobody asked for in 29% to 52%
  of episodes, more often than any attack succeeded.
- Each model fell for attacks in different languages (3B, 14B and 32B
  mostly English; 7B mostly mixed text).
- A bigger model was not safer: Qwen2.5-32B did the most normal tasks (66%)
  and fell for the most attacks (14.5%).
- Hermes 3 (Llama 3.1 8B) shows the same pattern: 2.3% without a defence,
  one amount-only attack past provenance, 0 with provenance-amount.
- Counted only where the agent read the attack and could do the task,
  attacks worked in 10% to 24% of cases without a defence; provenance-amount
  still stopped all of them.
- Adaptive attacks that forge the payee's identity beat provenance-amount
  when the agent obeys (40 of 40 forged amounts); the recipient check still
  stops a forged new number. With Qwen2.5-32B a forged "correction" from the
  payee worked in 11 of 16 cases without a defence; the fixed
  provenance-consistent stopped all 56 adaptive attacks, at the cost of
  holding most adaptive-case correct payments for the user.
- The two detectors tested failed on Bangla: ProtectAI's flagged 16 of 19
  normal Bangla texts (as a filter it would break 20 of 22 Bangla-request
  tasks, 1 of 21 English) and caught only 47% of English attacks; deepset's
  flagged 87% of all normal texts.
- The simulated user's automatic "yes" is part of the attack path: 29 of the
  78 successful attacks on the four Qwen models (no defence) came right
  after it (13 of 32 for Qwen2.5-32B).
- The original 114 cases reproduce: 10.0% / 3.8% / 6.2% attack success for
  3B / 7B / 14B, against 10.0% / 3.8% / 5.0% in the earlier 3-repeat run.

## Known limitations

Synthetic data and one fictional wallet; a simulated user who always says
yes (and answers any "?"); open models up to 32B (14B and 32B in 4-bit) plus
one API model; Bangla and Banglish text reviewed by one native speaker so
far; a small normal-text set for detectors (54 texts, 19 in Bangla).
Measurement caveats are in `docs/audit.md`.
