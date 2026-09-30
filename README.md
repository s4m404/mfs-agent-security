# Securing AI Agents for Bangladeshi Mobile Money

Can hidden instructions in Bangla, Banglish and code-mixed text trick an AI
agent into moving money? This repository contains a test environment, an
attack test set and defences to find out.

> Status: work in progress. Results below are from single runs; repeats are next.

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

Latest run: 114 cases, three sizes of the same model family (Qwen2.5 3B, 7B and 14B, the 14B quantised to 4-bit), served with vLLM on Kaggle T4 GPUs. One run per setting, so small differences between models are not meaningful yet.

| Model | Defence | Attacks that succeeded, of those the agent read | Correct actions blocked | Benign tasks done | Episodes where the agent tried to pay someone nobody asked for |
|---|---|---:|---:|---:|---:|
| Qwen2.5-3B | none | 8 of 53 | 0 of 34 | 6 of 34 | 43 of 114 (38%) |
| Qwen2.5-3B | provenance | **0 of 53** | **0 of 34** | 4 of 34 | 43 of 114 |
| Qwen2.5-7B | none | 3 of 62 | 0 of 34 | 17 of 34 | 33 of 114 (29%) |
| Qwen2.5-7B | provenance | **0 of 62** | **0 of 34** | 18 of 34 | 33 of 114 |
| Qwen2.5-14B (AWQ) | none | 4 of 67 | 0 of 34 | 13 of 34 | 55 of 114 (48%) |
| Qwen2.5-14B (AWQ) | provenance | **0 of 61** | **0 of 34** | 13 of 34 | 53 of 114 |

What this run showed:

- **The provenance defence stopped every attack on all three models and never blocked a correct payment.**
- **Each model fell for different attacks.** The 3B model fell for 8, mostly English messages and ordinary scam SMS, such as a stranger asking for money they "sent by mistake". The 7B model fell only for the "the user has already approved this" message in Banglish or mixed text. The 14B model fell only for English instructions hidden in invoices and tool descriptions, and for no Bangla or Banglish attack. With one run and small counts, these are leads to test with repeats, not conclusions.
- **Invented payees are a bigger risk than injection.** Every model tried to pay a payee or amount nobody asked for in 29% to 48% of episodes, more often than any attack succeeded. In bill tasks the models usually skipped reading the invoice and invented an account number; in money requests some sent money to a name ("Rafi", "মা") instead of a number.
- **A bigger model was not safer here.** The 14B model read more attacks and invented payees more often than the 7B model.
- **Bill tasks were the hardest.** Across all runs, electricity, internet and gas bills were rarely paid correctly, because the account number is only in the full invoice and most models did not open it.

Changes made after this run: the wallet now rejects `send_money` to anything that is not an 11-digit mobile number, as a real wallet does. Payments to invented biller accounts were already rejected.

The first full run (Qwen2.5-7B only, before the wallet checked biller accounts) found 4 of 62 attacks succeeding without a defence and 0 with it.

Pilot runs on the first 12 cases are in the git history.

To reproduce on free Kaggle GPUs, use [`notebooks/kaggle_run.ipynb`](notebooks/kaggle_run.ipynb).

## Roadmap

- [x] Wallet environment over MCP, agent loop, scoring, tests
- [x] 12 seed cases (4 benign, 8 attacks) in English, Bangla, Banglish and mixed text
- [x] Baseline defences: keyword filter and provenance policy
- [x] Pilot run with one open model on Kaggle (vLLM)
- [x] Full 114-case run with one model
- [x] Runs with 3 model sizes
- [ ] 3 repeats per setting, with confidence intervals
- [x] Grow to about 100 cases: 114 in total (12 hand-written seed cases plus 102 generated)
- [x] Native-speaker review of all Bangla and Banglish text (`bench/review_texts.csv`)
- [ ] Grow to about 300 cases
- [ ] Trained multilingual injection detector to replace the keyword baseline
- [ ] Connect BRACUVerify as a second backend
- [ ] Comparison with the sanitiser defence from "Indirect Prompt Injections: Are Firewalls All You Need?"
- [ ] Paper and dataset release

## Ethics

All data is synthetic, and "TakaPay" is fictional. See [docs/ETHICS.md](docs/ETHICS.md).
