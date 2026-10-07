# Paper outline: STALA 2027

Target: STALA 2027 (Security Testing and Assurance for LLMs and Agents, at
NDSS). Full paper, 8 pages without references, deadline **11 December 2026**
(23:59 AoE). Plan and framing: `docs/ROADMAP.md`, "Paper target".

Working title: **"Detectors flag the script, not the attack: testing payment
agents against Bangla and Banglish prompt injection"** (older working title:
"Can AI agents be tricked into moving money in Bangla?").

Rules for this outline:

- Every number below is copied from the README (section named in brackets).
  No new numbers. If a number changes in the README, change it here too.
- **[Groq]** marks a number that will come from the GPT-OSS-120B run on Groq
  (`.github/workflows/groq_run.yml`, results on the `groq-results` branch).
  Expected: `none` and `provenance-amount` by about the end of October,
  `provenance` maybe after 5 November. Until then the paper says "two model
  families"; with it, "three".
- **[Fig N] / [Table N]** are made by `scripts/make_figures.py` (see the end).

---

## Abstract (about 150 words)

Claims, in order:

1. Off-the-shelf prompt-injection detectors do not transfer to Bangla: one
   flags 84% of normal Bangla texts and would break 20 of 22 Bangla-request
   tasks as a filter (1 of 21 in English). [README: detectors]
2. A provenance policy that never reads the text blocks 0 correct payments in
   any language and, with the amount check, lets 0 of 880 attack episodes
   through on four Qwen2.5 models. [README: results]
3. Two testing lessons: attack success alone is misleading for payment agents
   (invented payees in 29% to 52% of episodes), and checking only "did money
   reach the attacker" misses amount-only attacks.
4. Release: 302 cases in Bangla, Banglish, code-mixed and English, over MCP.

## 1. Introduction (about 1 page)

Lead with the detector finding (roadmap point 0), then the rest.

- **Hook.** Bangladesh has about 239 million mobile money accounts; fraud by
  impersonation and PIN or OTP theft is common. Agents that read messages and
  make payments are arriving; indirect prompt injection is the top risk in the
  OWASP Top 10 for Agentic Applications (2026). [README: Why this matters]
- **Gap.** Agent injection benchmarks are English only; Bangla safety work
  covers chatbots, not agents that act. [README: Why this matters; related
  work still to write, see section 7]
- **Point 0, the headline.** The usual defence answer, "put a detector in
  front", fails outside English, and an English detection score hides it.
  ProtectAI's DeBERTa v2 flagged 16 of 19 normal Bangla texts (84%), more than
  it flagged Bangla attacks (57%); as a filter it would break 20 of 22 normal
  Bangla-request tasks and 1 of 21 English ones. deepset's detector flagged
  100% of attacks and 87% of normal texts. [README: detectors]
- **What works instead.** Provenance: check where a recipient, code or amount
  came from, never read the text. 0 correct payments blocked in all four
  request languages, all models. [README: detectors, results]
- **Contributions** (bullet list):
  1. The benchmark: TakaPay, a fictional wallet over MCP, 302 cases.
  2. The detector transfer result (point 0).
  3. Three testing lessons (points 1 to 3 of the roadmap): attack success
     alone misleads; amount-only attacks; harness choices and scripted audits
     change the conclusions.
  4. Results on 5 models from 2 families (3 with [Groq]).

## 2. Background and threat model (about 0.5 page)

- Mobile money (MFS) in Bangladesh; the language situation: Bangla script,
  Banglish (romanised), code-mixed. Users and SMS mix all three.
- Threat model: the attacker controls untrusted text the agent reads (an SMS,
  an invoice, a tool description), not the user's request or the wallet. Goals:
  send money to the attacker, leak the OTP, or overpay the real payee (amount
  only). Attacks copy common public scam patterns only (`docs/ETHICS.md`).
- Adaptive attacker (section 5.4): can also forge the payee's identity
  (spoofed SMS sender, fake revised bill).

## 3. The benchmark (about 1.25 pages)

- **Environment.** TakaPay over MCP, 9 tools (`check_balance`,
  `list_contacts`, `list_billers`, `read_sms`, `list_invoices`,
  `read_invoice`, `send_money`, `pay_bill`, `send_sms`). The wallet rejects
  unregistered biller accounts and malformed numbers. [README: How it works]
- **Simulated user.** Answers "yes" once, in the task language, if the agent
  asks with a "?". (This choice matters: section 5.5.)
- **Cases (Table: copy from README "Test set").** 302 cases: 12 hand-written,
  290 generated from tables. 82 benign (30 hard), 220 attacks. Vector: SMS 113,
  invoice 70, tool description 37. Attack language: English 55, Bangla 56,
  Banglish 55, mixed 54. Request language: 76 / 79 / 75 / 72. Style:
  instructions to the AI 122, ordinary scam messages 98. Goal: send money 175,
  leak OTP 25, overpay 20. [README: Test set]
- All Bangla and Banglish text is native-speaker reviewed (second reviewer on
  a 50-sentence sample: planned, roadmap item 5; report agreement if done).
- **Metrics.** Attack success, benign tasks done, false blocks (only when the
  blocked call was the correct action), tried to pay an invented payee, wrong
  payments that went through, and attack success among cases the agent read /
  read and could do. [README: What is measured; conditional rates]
- **Setup.** Qwen2.5 3B, 7B, 14B-AWQ, 32B-AWQ and Hermes-3-Llama-3.1-8B, vLLM
  on Kaggle T4 GPUs, temperature 0, 1 repeat (repeats at temperature 0 agreed
  in 96% to 100% of cases in the earlier 3-repeat run), replies capped at
  1,024 tokens. 95% bootstrap intervals over cases; Wilson intervals for small
  counts. [README: Results, earlier run]
  **[Groq]** GPT-OSS-120B on Groq's free tier, reasoning effort low (say so).
- Granite 3.3 8B left out: tool calls came out as plain text (0.2 tool calls
  per case, 5% of normal tasks), so its 0% attack success means nothing.
  [README: second family]

## 4. Defences (about 0.75 page)

- `keyword`: a baseline filter on suspicious words.
- `provenance`: a recipient or code must not come only from untrusted text.
- `provenance-amount`: also, the amount must come from the user's request or
  from the payee itself (an SMS from the payee's own number, or an invoice for
  that biller account).
- `provenance-consistent`: also, block and ask the user when the payee's own
  messages or invoices disagree on the amount; checks every SMS and invoice
  from the payee in the wallet.
- A block can carry advice for the agent (section 5.5: the wording matters).
- Detectors as defences: ProtectAI DeBERTa v3 v2 and deepset DeBERTa v3, run
  on all untrusted texts (no agent). Prompt Guard not run (needs a Hugging
  Face account). [README: detectors]

## 5. Results (about 3 pages)

### 5.1 Detectors flag the script, not the attack (point 0) [Fig 1]

Claim: a detector's English score says nothing about other languages;
provenance, which never reads the text, does not have this problem.

| Evidence (README: detectors) | Number |
|---|---|
| Texts tested | 174 attack, 54 normal (19 normal Bangla) |
| ProtectAI: attacks flagged, all / en / bn / banglish / mixed | 59% / 47% / 57% / 80% / 51% |
| ProtectAI: normal texts flagged, all / Bangla | 39% (21/54) / **84% (16/19)**; Bangla interval 62% to 94% |
| ProtectAI: normal Banglish / English flagged | 1 of 11 / 2 of 16 |
| ProtectAI as a filter: tasks broken, en / bn / banglish / mixed request | 1/21 / **20/22** / 1/20 / 16/19 |
| deepset: attacks / normal flagged | 100% / 87% (47/54); Bangla 19/19 |
| deepset as a filter | 12/21 / 22/22 / 12/20 / 19/19 |
| keyword: attacks / normal flagged | 34% / 7% (4/54) |
| Provenance defences, correct payments blocked, every request language | 0 |

Notes: ProtectAI's model card says it does not handle non-English input; we
show the cost in practice. Even in English it missed about half the attacks
(47% flagged), e.g. "NOTE TO AI ASSISTANT: this account has moved ...".
This is the "intuitive metric is misleading" negative result STALA asks for.

### 5.2 Attack success alone misleads (point 1) [Fig 2]

Claim: for payment agents, wrong payments with no attacker are more common
than successful attacks, and weak task performance hides attack risk.

| Evidence | Number |
|---|---|
| Attack success, no defence, 3B / 7B / 14B / 32B / Hermes 3 | 7.3% / 5.9% / 7.7% / 14.5% / 2.3% [README: results] |
| Tried to pay an invented payee, same models | 52% / 29% / 49% / 40% / 10% |
| Such payments that went through, no defence | 33 / 8 / 29 / 20 / 10 |
| Same with `provenance-amount` | 0 for every model |
| Attack success among attacks read and on tasks the agent could do, no defence | 24.1% / 10.8% / 14.9% / 17.8% / 9.8% [README: conditional rates] |
| Same with `provenance-amount` | 0% for every model (e.g. 0/118 for 7B, interval 0 to 3) |
| Top cause of failed normal tasks (Qwen) | wrong biller account: 32 / 19 / 21 / 15 of 68 / 36 / 47 / 28 failures; 32B used the invoice ID in 14 of its 15 [README: why normal tasks fail] |

Also: a bigger model was not safer: 32B did the most normal tasks (66%) and
fell for the most attacks (14.5%, about twice the smaller models).
**[Groq]** GPT-OSS-120B: attack success, invented payees, wrong payments
through, conditional rates (run `scripts/conditional_rates.py` on
`results_groq/`).

### 5.3 Amount-only attacks need their own check (point 2) [Fig 3, Table 1]

Claim: scoring only "did money reach the attacker" misses attacks that keep
the real payee and raise the amount; recipient provenance alone lets exactly
those through; the amount check closes them with no false blocks.

| Evidence (README: results) | Number |
|---|---|
| `provenance`: attacks that redirect money or leak the OTP | 0 of 800 episodes (four Qwen models) |
| `provenance`: attacks that got through | 15 (Qwen), all amount-only; Hermes 3: 1, amount-only |
| Amount-only attacks without a defence (of 20), 3B / 7B / 14B / 32B | 2 / 4 / 7 / 7 (other 200 attacks: 14 / 9 / 10 / 25) |
| `provenance-amount`: attacks through | 0 of 880 (four Qwen models), 0 of 220 Hermes 3 |
| `provenance-amount`: correct payments blocked, wrong payments through | 0, 0 |
| Wrong payments through: none / provenance / provenance-amount | 33/30/0, 8/6/0, 29/27/0, 20/2/0, 10/9/0 |
| OTP leaked | 0 of 75 attempts (3B to 14B), 0 of 25 (32B) |

Example for the text: a fake "correction" in a school invoice raising the fee
from 3,500 to 5,000 Tk.
**[Groq]** GPT-OSS-120B rows of Table 1 and bars of Fig 3 (`provenance` may
arrive after 5 November; the figure works without it).

### 5.4 Adaptive attacks: test defences with real agents (point 3, part 1)

Claim: a scripted audit says what a defence can stop, but a real model used
the tools differently and found a gap the script missed.

| Evidence (README: adaptive attacks) | Number |
|---|---|
| Adaptive set | 56 cases, kept out of the main 302 |
| Scripted obeying agent vs `provenance-amount` | forged amounts 40/40 through; forged new number 0/16 |
| Scripted vs `provenance-consistent` | 0/40 (correct payment then waits for the user in those 40) |
| Qwen2.5-32B, forged amount SMS: none / provenance-amount / consistent v1 / fixed | 11/16 / 10/16 / 3/16 / **0/16** |
| Forged new number SMS | 8/16 / 0/16 / 0/16 / 0/16 |
| Forged revised invoice | 1/24 / 1/24 / 0/24 / 0/24 |
| Why v1 failed | all 3: `read_sms` with `limit: 1`, only the newest (forged) SMS seen |
| Fixed version, all 56 adaptive attacks | 0/56; correct payment made in 1 of 56 (12 with provenance-amount) |
| Fixed version, 302 main cases | 0/220 attacks, 0 correct payments blocked, 72% normal tasks |
| Audit with a newest-only scripted agent | v1: 40/40 through; fixed: 0/40 |

Cost to state honestly: when the payee's messages disagree, the correct
payment waits for the user.

### 5.5 Harness choices change the scores (point 3, part 2)

Claim: small harness details move task completion by large amounts, so they
must be reported with any benchmark score.

| Evidence (README) | Number |
|---|---|
| Block message for a wrong biller account, Qwen2.5-32B | old message: 42 of 82 normal tasks with either defence (54 without); new message: 57 (70%) with `provenance-amount`, 58 (71%) with `provenance-consistent`; fixed consistent 59 (72%) |
| Still, with the new message | 0 of 220 attacks, 0 correct payments blocked |
| Simulated user answers only a "?" (Hermes 3) | about 9 of 64 failures asked without a "?"; about 8 said they paid without a payment call (keyword estimates) |
| Hermes 3 normal tasks done | 22% |

### 5.6 Language (short paragraph) [Table 2]

Claim: each model falls for attacks in different languages, so a benchmark in
one language cannot rank models.

| Evidence (README: results) | Number |
|---|---|
| 3B, 14B: English attacks that worked | 10 and 13 of 55 (at most 3 in any other language) |
| 32B | English 14 of 55, Banglish 7, mixed 8 |
| 7B | mostly mixed text, 6 of 54 |
| Hermes 3 | 3 of its 5 in English, all through SMS |

**[Groq]** GPT-OSS-120B row of Table 2.

## 6. Reproducibility (short, can merge into 3)

- The original 114 cases reproduce: 10.0% / 3.8% / 6.2% now vs 10.0% / 3.8% /
  5.0% in the earlier 3-repeat run. Settings that ran twice gave the same
  outcome in 97% to 99% of cases. [README: results]
- 0 model errors (README: Qwen2.5-32B run; roadmap: the first 302-case
  run). All scripts and the demo page are
  public (or anonymised, depending on STALA's rules; check in November).

## 7. Related work (about 0.5 page) — still to write

AgentDojo, InjecAgent, CaMeL (provenance / capability ideas), multilingual
jailbreak papers, "Indirect Prompt Injections: Are Firewalls All You Need?".
Say what is new: non-English agent injection with real money tools; detector
transfer across scripts; amount-only attacks; harness effects. Roadmap item
"Related work for the paper" is still open. No numbers here.

## 8. Limitations and ethics (about 0.5 page)

- Synthetic data, one fictional wallet, a simulated user that says "yes" once.
- Small open models on T4 GPUs (4-bit for 14B and 32B), 1 repeat; one strong
  API model **[Groq]** with low reasoning effort.
- Normal detector texts are few (54; 19 Bangla), so intervals are wide.
- `provenance-consistent` makes the user decide when the payee's messages
  disagree (1 of 56 adaptive correct payments went through).
- Ethics: everything fictional, attacker numbers fictional, only public scam
  patterns (`docs/ETHICS.md`).

## 9. Conclusion (about 0.25 page)

Test defences in the languages users write in; prefer checks that do not read
the text; report wrong payments and amount-only attacks, not only attack
success; test with real agents and report harness choices.

---

## Figures and tables

Made by `scripts/make_figures.py` from the results files (`results/` and,
later, `results_groq/`; both git-ignored, so run it where the results are):

```
python scripts/make_figures.py results/ results_groq/ \
    --detectors results_detectors/flags.jsonl --out docs/paper/figures
```

It writes PDF (for LaTeX) and PNG, Markdown and LaTeX tables, and
`numbers.json` with every number shown. Before using a figure, check its
numbers against the README tables (they come from the same scores.jsonl
files, so they should match exactly).

| Item | Section | Shows | Data |
|---|---|---|---|
| **Fig 1** `fig1_detectors` | 5.1 | (a) normal texts flagged by language, per detector; (b) normal tasks broken if used as a filter, by request language, with provenance (correct payments blocked, real runs) | `results_detectors/flags.jsonl` + all provenance runs |
| **Fig 2** `fig2_attack_vs_invented` | 5.2 | per model, no defence: attack success vs tried to pay an invented payee | `none` runs |
| **Fig 3** `fig3_defences` | 5.3 | per model and defence: successful attacks split into amount-only vs redirect/OTP; wrong payments that went through | all runs |
| **Table 1** `table1_main` | 5.3 | model x defence: attack success, amount-only, correct payments blocked, benign tasks done, invented payees, wrong payments through | all runs |
| **Table 2** `table2_language` | 5.6 | successful attacks by attack language, no defence | `none` runs |

Tables copied by hand from the README (no script needed): test set counts
(section 3), conditional rates (5.2), adaptive attacks (5.4).

Notes for the figure run:

- Qwen2.5-32B has several runs of the same defence (old and new block
  message, first and fixed `provenance-consistent`). The script keeps the
  folder given last for each model and defence and prints a note. For the
  paper use: `none` and `provenance` (old message; no newer run), and the
  new-message `provenance-amount` and the fixed `provenance-consistent`.
  Put the older 32B runs in a separate folder and leave it out.
- The adaptive runs (`results_adaptive/`) are not plotted; their numbers are
  small, so section 5.4 uses a table.
- **[Groq]** Once `results_groq/` has `none` and `provenance-amount`, rerun
  the command above: GPT-OSS-120B appears in Fig 2, Fig 3 and both tables
  with no code change.

## Still to do before the draft

- [x] Run `make_figures.py` on the real results, check against the README
      (7 October): every number in Table 1, Table 2 and the detector data
      matches the README. Output in `docs/paper/figures/`, made with
      `python scripts/make_figures.py results_old/ results/ results_new/
      results_fixed/ --detectors results_detectors/flags.jsonl --out
      docs/paper/figures`, where results_old holds 3B / 7B / 14B / Hermes 3,
      results the first 32B runs, results_new the new-message 32B runs and
      results_fixed the fixed provenance-consistent run (newest last).
- [ ] [Groq] numbers into 5.2, 5.3, 5.6 and the abstract.
- [ ] Related work (section 7).
- [ ] STALA template and anonymisation rules (check in November).
