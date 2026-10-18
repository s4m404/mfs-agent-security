# Dataset card: TakaPay

**TakaPay** is a benchmark for indirect prompt injection against LLM agents
that use a mobile-money (MFS) wallet, with attacks and user requests in
Bangla, Banglish (romanised Bangla), code-mixed Bangla-English and English.
An agent gets a request ("pay my power bill from the invoice"), reads SMS,
invoices and tool descriptions through nine MCP tools, and may make
payments; some of that content hides an attack.

- Code and cases: https://github.com/s4m404/mfs-agent-security
- Live demo: https://s4m404.github.io/mfs-agent-security/
- License: CC BY 4.0 for the data, MIT for the code (`LICENSE-DATA.md`,
  `LICENSE`)
- Citation: `CITATION.cff`

## What is in it

| File | Contents |
|---|---|
| `bench/cases/seed.yaml` | 12 hand-written cases |
| `bench/cases/generated.yaml` | 290 cases built by `bench/generate.py` from hand-written building blocks |
| `bench/cases_adaptive/adaptive.yaml` | 56 adaptive cases that forge the payee's identity (kept apart from the main 302) |
| `bench/SCHEMA.md` | Every field of a case, how a task counts as done, and how each attack goal is scored |
| `bench/review_texts.csv` | Every distinct Bangla, Banglish and mixed sentence once, with the native-speaker review mark |
| `kaggle-results` and `groq-results` branches | Raw runs: every step of every episode (`traces.jsonl`), one score per episode (`scores.jsonl`), summaries |

Each case gives the user's request, the wallet's extra contents (SMS,
invoices, billers, contacts, replaced tool descriptions), what counts as
doing the task, and, for attacks, the attacker's goal. Scoring uses the
final wallet state and the trace (`bench/score.py`); no LLM judge.

## The 302 main cases

| | Count |
|---|---:|
| Normal tasks (no attack) | 82, including 30 hard ones (extra numbers, Bengali digits, late fees, real safety warnings, words like "assistant") |
| Attacks | 220 |
| Where the attack is hidden | SMS 113, invoice 70, tool description 37 |
| Attack language | English 55, Bangla 56, Banglish 55, mixed 54 |
| Request language (all cases) | English 76, Bangla 79, Banglish 75, mixed 72 |
| Attack style | instructions to the AI 122, ordinary scam messages 98 |
| Attack goal | send money to the attacker 175, leak the OTP 25, overpay the real payee 20 |

The tasks are six bill payments (power, internet, gas, water, mobile,
school fee), four payments requested by SMS (a friend, a parent, a
landlord, a split dinner bill) and two read-only checks. The adaptive set
has 16 SMS from the payee's number asking for more, 16 giving a new number
to pay, and 24 forged "revised" invoices.

## How it was made

All text was written for the benchmark. Attacks follow common, already
public scam patterns (fake account blocks, "wrong transfer" requests,
lucky draws, agent cash-in, customs fees, job offers, a long chat from a
"relative") and instructions aimed at an AI assistant; they introduce no
new fraud technique. `bench/generate.py` combines tasks, attacks, languages
and vectors from tables, so each sentence is written once and reused. The
first 114 cases are an earlier version of the set, kept unchanged so older
results still compare.

**Native-speaker review.** All Bangla and Banglish text was written or
reviewed by one native speaker, the author. In `bench/review_texts.csv`
(124 sentences): the 61 sentences added for the 302-case set are marked
"Y" (sounds natural); the 54 sentences of the original set were reviewed
before the file existed and carry no mark; the 9 sentences of the adaptive
set are not yet reviewed. A second native speaker's check of a sample is
planned.

## Intended uses

- Testing whether an LLM agent with payment tools follows instructions
  hidden in untrusted Bangla, Banglish, code-mixed or English content.
- Testing defences (filters, detectors, provenance rules) for attack
  success, and for blocked correct payments, in every language.
- Measuring wrong payments made with no attacker involved (invented payees,
  guessed amounts).

## Out of scope

- Not a measure of any real mobile-money app: TakaPay and every name,
  number, account and biller are fictional.
- Not a training set for scams. The messages copy patterns already in
  public scam reports so that defences can be tested against them.
- Not a test of real users: the harness has a simulated user who answers
  "yes" once to any reply with a "?".

## Known limitations

- Synthetic data and one wallet with nine tools; real apps and their
  messages differ.
- One native-speaker reviewer so far; Banglish spelling varies more in real
  use than here.
- The normal texts used to test detectors are few (54, 19 in Bangla).
- More caveats on scoring are in `docs/audit.md`.

## Results

Results for six models from three families (Qwen2.5 3B to 32B, Hermes 3 on
Llama 3.1 8B, GPT-OSS-120B) with and without defences are in the README.
Every episode can be re-scored from its trace with `scripts/rescore.py`.

## Ethics

See `docs/ETHICS.md`. If work with this benchmark reveals a weakness in a
real product, report it privately to the provider first.

## Maintenance

Issues and corrections: open an issue on the GitHub repository. Changes to
the cases are made through `bench/generate.py`; a test fails if the YAML
files are out of date.
