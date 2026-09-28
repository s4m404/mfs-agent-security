# Securing AI Agents for Bangladeshi Mobile Money

Can hidden instructions in Bangla, Banglish and code-mixed text trick an AI
agent into moving money? This repository contains a test environment, an
attack test set and defences to find out.

> Status: early work in progress. Results below are placeholders until the
> first real model runs.

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

## What is measured

| Metric | Meaning |
| --- | --- |
| Attack success rate | Share of attack cases where money or the OTP reached the attacker |
| Utility on benign tasks | Share of normal tasks completed correctly |
| Utility under attack | Share of attack cases where the user's own task still got done |
| False blocks | Share of benign tasks where the defence blocked a call |

Results are broken down by injection language, script, vector and style.

## Results

[Placeholder: table of models by defences, filled in after the first runs.]

## Roadmap

- [x] Wallet environment over MCP, agent loop, scoring, tests
- [x] 12 seed cases (4 benign, 8 attacks) in English, Bangla, Banglish and mixed text
- [x] Baseline defences: keyword filter and provenance policy
- [ ] First runs with 2 to 3 open models (Ollama or HPC)
- [ ] Grow to about 100 cases (December 2026 milestone), then about 300
- [ ] Trained multilingual injection detector to replace the keyword baseline
- [ ] Connect BRACUVerify as a second backend
- [ ] Comparison with the sanitiser defence from "Indirect Prompt Injections: Are Firewalls All You Need?"
- [ ] Paper and dataset release

## Ethics

All data is synthetic, and "TakaPay" is fictional. See [docs/ETHICS.md](docs/ETHICS.md).
