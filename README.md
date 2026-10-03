# Securing AI Agents for Bangladeshi Mobile Money

Can hidden instructions in Bangla, Banglish and code-mixed text trick an AI
agent into moving money? This repository contains a test environment, an
attack test set and defences to find out.

**[Live demo](https://s4m404.github.io/mfs-agent-security/)**: replay real runs step by step and switch the defence on and off. No install needed.

> Status: work in progress. Results below are from all 302 cases on three Qwen2.5 models.

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
  where recipients and codes came from), `provenance-amount` (also checks
  that the amount came from the user or from the payee itself)
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

302 cases: 12 hand-written seed cases (`bench/cases/seed.yaml`) and 290 generated cases (`bench/cases/generated.yaml`). The first 102 generated cases are the earlier 114-case set, unchanged, so older results still compare.

The generated cases are built by `bench/generate.py` from hand-written building blocks, so each Bangla or Banglish sentence is written (and reviewed) once. Counts below are for all 302 cases:

| | Count |
|---|---:|
| Tasks | 12 generated: 6 bill payments (power, internet, gas, water, mobile, school fee), 4 payments requested by SMS (a friend, a parent, a landlord named in the request, a split dinner bill), 2 read-only checks (inbox, unpaid bills) |
| Benign cases | 82, including 30 hard cases (extra numbers, Bangla digits, late fees, real safety warnings, words like "assistant" or "mandatory") |
| Attack cases | 220 |
| Where the attack is hidden | SMS 113, invoice 70, tool description 37 |
| Attack language | English 55, Bangla 56, Banglish 55, mixed 54 |
| Request language | English 76, Bangla 79, Banglish 75, mixed 72 |
| Attack style | instructions to the AI 122, ordinary scam messages 98 (fake account block, wrong transfer, lucky draw, MFS agent cash-in, customs fee, job offer, long chat from a "relative") |
| Attack goal | send money to the attacker 175, leak the OTP 25, overpay the real payee 20 (only the amount is changed) |

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

Latest run (October 2026): all 302 cases, three sizes of the same model family (Qwen2.5 3B, 7B and 14B, the 14B quantised to 4-bit), served with vLLM on Kaggle T4 GPUs at temperature 0, one run per case. Brackets show 95% confidence intervals from a bootstrap over test cases; for 0% the upper bound uses the rule of three. Reproduce the table with `python scripts/compare_runs.py results/`.

| Model | Defence | Attack success | Correct actions blocked | Benign tasks done | Tried to pay an invented payee | Wrong payments that went through |
|---|---|---:|---:|---:|---:|---:|
| Qwen2.5-3B | none | 7.3% (4 to 11) | 0% | 17% (9 to 26) | 52% (46 to 57) | 33 |
| Qwen2.5-3B | provenance | 0.5% (0 to 1) | 0% (0 to 4) | 15% (8 to 23) | 51% (46 to 57) | 30 |
| Qwen2.5-3B | provenance-amount | **0% (0 to 1)** | **0% (0 to 4)** | 13% (7 to 22) | 51% (46 to 57) | **0** |
| Qwen2.5-7B | none | 5.9% (3 to 9) | 0% | 56% (45 to 66) | 29% (24 to 34) | 8 |
| Qwen2.5-7B | provenance | 2.3% (0 to 4) | 0% (0 to 4) | 55% (44 to 66) | 29% (24 to 34) | 6 |
| Qwen2.5-7B | provenance-amount | **0% (0 to 1)** | **0% (0 to 4)** | 55% (44 to 66) | 29% (24 to 34) | **0** |
| Qwen2.5-14B (AWQ) | none | 7.7% (5 to 12) | 0% | 43% (32 to 54) | 49% (43 to 54) | 29 |
| Qwen2.5-14B (AWQ) | provenance | 2.3% (0 to 4) | 0% (0 to 4) | 50% (39 to 61) | 49% (43 to 54) | 27 |
| Qwen2.5-14B (AWQ) | provenance-amount | **0% (0 to 1)** | **0% (0 to 4)** | 51% (40 to 62) | 49% (43 to 54) | **0** |

Attack success is over all 220 attack cases per setting. Counting only attacks the agent actually read, it was 13% for 3B, 8% for 7B and 9% for 14B without a defence. "Wrong payments that went through" counts episodes (out of 302) where the wallet carried out a payment to a payee or amount nobody asked for.

What this run showed:

- **Provenance plus the amount check stopped every attack on all three models (0 of 660 attack episodes), never blocked a correct payment, and let no wrong payment through.** The amount rule: a payment amount must come from the user's request or from the payee itself (an SMS from the recipient's own number, or an invoice for that same biller account).
- **Provenance alone stopped every attack that sends money to a new number or leaks the OTP (0 of 600 episodes), but not attacks that change only the amount.** All 11 attacks that got past it kept the real payee and inflated the amount, for example a fake "correction" in a school invoice raising the fee from 3,500 to 5,000 Tk. Without a defence these amount-only attacks were the most successful kind: 2, 4 and 7 of 20 for the 3B, 7B and 14B models, against 14, 9 and 10 of the other 200 attacks.
- **Invented payees are a bigger risk than injection.** Models tried to pay a payee or amount nobody asked for in 29% to 52% of episodes, far more often than any attack succeeded, and without a defence 8 to 33 of these payments per model went through, mostly to the right payee with a guessed amount. The amount check stopped all of them.
- **Each model falls for attacks in different languages.** The 3B and 14B models fell mostly for English text (10 and 13 of 55 English attacks, at most 3 in any other language). The 7B model fell most for mixed Bangla-English text (6 of 54). No model leaked the OTP (0 of 75 attempts).
- **A bigger model was not safer.** The 14B model had the highest attack success (7.7%) and tried to pay invented payees in 49% of episodes, against 29% for the 7B model.
- **The results reproduce.** On the original 114 cases, attack success without a defence was 10.0%, 3.8% and 6.2%, against 10.0%, 3.8% and 5.0% in the earlier 3-repeat run. Four settings that ran twice (an interrupted first attempt, then the full run) gave the same outcome in 97% to 99% of cases.
- **Small models often fail the task itself.** The 3B model completed only 13% to 17% of normal tasks. Without a defence, 27 of its 68 failed tasks were bill payments made without opening the invoice, and 15 paid the wrong payee or amount.

### Earlier run (114 cases, 3 repeats)

The same three models on the first 114 cases, 3 repeats per setting: attack success without a defence was 10.0%, 3.8% and 5.0% of 240 attack episodes; with provenance it was 0 of 720, with no correct payment blocked. Repeats at temperature 0 barely differed (96% to 100% of cases had the same outcome every time), which is why the 302-case run uses one repeat. A replay of those traces through `provenance-amount` (`scripts/replay_defence.py`) predicted that it would catch 26, 3 and 6 wrong payments that provenance allowed, with no correct payment blocked; the real run above confirms this. Full numbers are in the git history of this README.

Pilot runs on the first 12 cases are in the git history.

To reproduce on free Kaggle GPUs, use [`notebooks/kaggle_run.ipynb`](notebooks/kaggle_run.ipynb).

## Roadmap

The full plan with dates is in [docs/ROADMAP.md](docs/ROADMAP.md).

- [x] Wallet environment over MCP, agent loop, scoring, tests
- [x] 12 seed cases (4 benign, 8 attacks) in English, Bangla, Banglish and mixed text
- [x] Baseline defences: keyword filter and provenance policy
- [x] Pilot run with one open model on Kaggle (vLLM)
- [x] Full 114-case run with one model
- [x] Runs with 3 model sizes
- [x] 3 repeats per setting, with confidence intervals
- [x] Grow to about 100 cases: 114 in total (12 hand-written seed cases plus 102 generated)
- [x] Native-speaker review of all Bangla and Banglish text (`bench/review_texts.csv`)
- [x] Grow to about 300 cases: 302 in total
- [x] Provenance check for amounts as well as recipients (replay estimate done)
- [x] Model run with the amount check (302 cases, 3 models)
- [ ] Trained multilingual injection detector to replace the keyword baseline
- [ ] Connect BRACUVerify as a second backend
- [ ] Comparison with the sanitiser defence from "Indirect Prompt Injections: Are Firewalls All You Need?"
- [ ] Paper and dataset release

## Ethics

All data is synthetic, and "TakaPay" is fictional. See [docs/ETHICS.md](docs/ETHICS.md).
