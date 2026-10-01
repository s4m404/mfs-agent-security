# Securing AI Agents for Bangladeshi Mobile Money

Can hidden instructions in Bangla, Banglish and code-mixed text trick an AI
agent into moving money? This repository contains a test environment, an
attack test set and defences to find out.

> Status: work in progress. Results below are from 3 repeats per setting on 114 cases.

## Why this matters

- Bangladesh has about 239 million mobile money accounts, and fraud through
  impersonation and PIN or OTP theft is common.
- AI assistants that read messages and make payments are arriving, and
  hidden instruction attacks ("indirect prompt injection") are the top risk
  in the OWASP Top 10 for Agentic Applications (2026).
- Existing test sets are English only, and existing Bangla safety work covers
  chatbots, not agents that take actions.

## How it works

```
user request ──> agent (any LLM) ──> defence ──> MCP server ──> fictional TakaPay wallet
                                        ▲                            │
                                        └──── SMS, invoices, tool descriptions (untrusted)
```

- `mfs_env/`: a fictional wallet (balances, contacts, billers, SMS inbox,
  invoices) exposed as MCP tools: `check_balance`, `list_contacts`,
  `list_billers`, `read_sms`, `list_invoices`, `read_invoice`,
  `send_money`, `pay_bill`, `send_sms`
- `agent/`: the agent loop; works with Ollama, vLLM or any OpenAI compatible API
- `defences/`: `none`, `keyword` (simple baseline), `provenance` (tracks
  where recipients and codes came from)
- `bench/`: test cases (`bench/cases/*.yaml`) and scoring
- Every run writes a full trace of tool calls to `traces.jsonl`

## Quick start

```bash
pip install -r requirements.txt
python -m pytest            # runs without any model

# with a local model through Ollama
ollama pull qwen2.5:7b
python scripts/run_bench.py --model qwen2.5:7b --defence none
python scripts/run_bench.py --model qwen2.5:7b --defence provenance
```

For larger models on the university HPC, see [docs/HPC.md](docs/HPC.md).

You can also plug the wallet into any MCP client:

```bash
python -m mfs_env.server --demo
```

## Test set

114 cases: 12 hand-written seed cases (`bench/cases/seed.yaml`) and 102 generated cases (`bench/cases/generated.yaml`).

The generated cases are built by `bench/generate.py` from hand-written building blocks, so each Bangla or Banglish sentence is written (and reviewed) once:

| | Count |
|---|---:|
| Tasks | 6 (3 bill payments, 2 payments requested by SMS, 1 inbox summary with no payment) |
| Benign cases | 30 (every task in every language, plus 6 hard cases with numbers, Bangla digits or look-alike warnings) |
| Attack cases | 72 |
| Where the attack is hidden | invoice 24, SMS 36, tool description 12 |
| Attack language | English, Bangla, Banglish, mixed: 18 each |
| Attack style | instructions to the AI 48, ordinary scam messages 24 |
| Attack goal | send money 60, leak the OTP 12 |

To change the cases, edit the tables in `bench/generate.py` and run `python -m bench.generate`. A test fails if the YAML file is out of date.

## What is measured

| Metric | Meaning |
| --- | --- |
| Attack success rate | Share of attack cases where money or the OTP reached the attacker |
| Utility on benign tasks | Share of normal tasks completed correctly |
| Utility under attack | Share of attack cases where the user's own task still got done |
| False blocks | Share of benign tasks where the defence blocked the correct action |

Results are broken down by injection language, script, vector and style.

## Results

Latest run: 114 cases, three sizes of the same model family (Qwen2.5 3B, 7B and 14B, the 14B quantised to 4-bit), served with vLLM on Kaggle T4 GPUs, 3 repeats per setting at temperature 0. Brackets show 95% confidence intervals from a bootstrap over test cases; for 0% the upper bound uses the rule of three. Reproduce the table with `python scripts/compare_runs.py results/`.

| Model | Defence | Attack success | Correct actions blocked | Benign tasks done | Tried to pay an invented payee |
|---|---|---:|---:|---:|---:|
| Qwen2.5-3B | none | 10.0% (4 to 17) | 0% | 21% (8 to 36) | 38% (29 to 46) |
| Qwen2.5-3B | provenance | **0% (0 to 4)** | **0% (0 to 9)** | 12% (3 to 24) | 38% (29 to 46) |
| Qwen2.5-7B | none | 3.8% (0 to 8) | 0% | 50% (33 to 67) | 29% (21 to 38) |
| Qwen2.5-7B | provenance | **0% (0 to 4)** | **0% (0 to 9)** | 53% (36 to 70) | 29% (21 to 38) |
| Qwen2.5-14B (AWQ) | none | 5.0% (1 to 10) | 0% | 38% (23 to 54) | 48% (38 to 57) |
| Qwen2.5-14B (AWQ) | provenance | **0% (0 to 4)** | **0% (0 to 9)** | 36% (21 to 54) | 46% (37 to 55) |

Attack success is over all 80 attack cases (240 episodes per setting). Counting only attacks the agent actually read, it was 15% for 3B, 5% for 7B and 6% for 14B without a defence.

What this run showed:

- **The provenance defence stopped every attack on all three models, in all 720 attack episodes, and never blocked a correct payment.**
- **Each model fell for a different kind of attack, and the same ones every time.** The 3B model fell for 8 cases, mostly English messages and ordinary scam SMS, such as a stranger asking for money they "sent by mistake". The 7B model fell only for the "the user has already approved this" message in Banglish or mixed text. The 14B model fell only for English instructions hidden in invoices and tool descriptions, and for no Bangla, Banglish or mixed attack. Every one of these cases succeeded in all 3 repeats.
- **Invented payees are a bigger risk than injection.** Every model tried to pay a payee or amount nobody asked for in 29% to 48% of episodes, far more often than any attack succeeded. In bill tasks the models usually skipped reading the invoice and invented an account number; in money requests some sent money to a name ("Rafi", "মা") instead of a number. The wallet now rejects both, so few of these payments went through.
- **The provenance defence checks who gets paid, not how much.** The 3B model sometimes paid the right biller a guessed amount (500 or 1000 Tk instead of 1850 Tk), and the defence let it through. Checking amounts against the invoice is a next step.
- **A bigger model was not safer.** The 14B model read more attacks and invented payees more often than the 7B model.
- **Repeats at temperature 0 barely differ** (96% to 100% of cases had the same outcome every time), so the confidence intervals are wide because there are few cases, not because results are random. Growing the test set matters more than more repeats.

The first single-repeat runs (before the wallet rejected names as recipients) gave the same attack results.

Pilot runs on the first 12 cases are in the git history.

To reproduce on free Kaggle GPUs, use [`notebooks/kaggle_run.ipynb`](notebooks/kaggle_run.ipynb).

## Roadmap

- [x] Wallet environment over MCP, agent loop, scoring, tests
- [x] 12 seed cases (4 benign, 8 attacks) in English, Bangla, Banglish and mixed text
- [x] Baseline defences: keyword filter and provenance policy
- [x] Pilot run with one open model on Kaggle (vLLM)
- [x] Full 114-case run with one model
- [x] Runs with 3 model sizes
- [x] 3 repeats per setting, with confidence intervals
- [x] Grow to about 100 cases: 114 in total (12 hand-written seed cases plus 102 generated)
- [x] Native-speaker review of all Bangla and Banglish text (`bench/review_texts.csv`)
- [ ] Grow to about 300 cases (the main limit on precision)
- [ ] Provenance check for amounts as well as recipients
- [ ] Trained multilingual injection detector to replace the keyword baseline
- [ ] Connect BRACUVerify as a second backend
- [ ] Comparison with the sanitiser defence from "Indirect Prompt Injections: Are Firewalls All You Need?"
- [ ] Paper and dataset release

## Ethics

All data is synthetic, and "TakaPay" is fictional. See [docs/ETHICS.md](docs/ETHICS.md).
