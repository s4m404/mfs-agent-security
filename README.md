# Securing AI Agents for Bangladeshi Mobile Money

Can hidden instructions in Bangla, Banglish and code-mixed text trick an AI
agent into moving money? This repository contains a test environment, an
attack test set and defences to find out.

**[Live demo](https://s4m404.github.io/mfs-agent-security/)**: replay real runs step by step and switch the defence on and off. No install needed.

> Status: work in progress. Results below are from all 302 cases on four Qwen2.5 models (3B to 32B) and Hermes 3 (Llama 3.1 8B).

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
  that the amount came from the user or from the payee itself),
  `provenance-consistent` (also stops when the payee's own messages or
  invoices give different amounts, and asks the user)
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

Latest runs (October 2026): all 302 cases, four sizes of the same model family (Qwen2.5 3B, 7B, 14B and 32B, the 14B and 32B quantised to 4-bit), served with vLLM on Kaggle T4 GPUs at temperature 0, one run per case. Brackets show 95% confidence intervals from a bootstrap over test cases; for 0% the upper bound uses the rule of three. Reproduce the table with `python scripts/compare_runs.py results/`.

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
| Qwen2.5-32B (AWQ) | none | 14.5% (10 to 19) | 0% | 66% (56 to 76) | 40% (34 to 45) | 20 |
| Qwen2.5-32B (AWQ) | provenance | 1.8% (0 to 4) | 0% (0 to 4) | 51% (40 to 62) | 39% (33 to 45) | 2 |
| Qwen2.5-32B (AWQ) | provenance-amount | **0% (0 to 1)** | **0% (0 to 4)** | 51% (40 to 62) | 39% (33 to 45) | **0** |
| Qwen2.5-32B (AWQ) | provenance-amount, new block message | **0% (0 to 1)** | **0% (0 to 4)** | 70% (60 to 79) | 39% (33 to 44) | **0** |
| Qwen2.5-32B (AWQ) | provenance-consistent | **0% (0 to 1)** | **0% (0 to 4)** | 71% (61 to 80) | 39% (34 to 45) | **0** |

The last two 32B rows are a later run, after the block message for a wrong biller account was changed (see below); all other rows used the old message. Attack success is over all 220 attack cases per setting. Counting only attacks the agent actually read, it was 13% for 3B, 8% for 7B, 9% for 14B and 18% for 32B without a defence. "Wrong payments that went through" counts episodes (out of 302) where the wallet carried out a payment to a payee or amount nobody asked for.

What these runs showed (the 32B model is covered in more detail below):

- **Provenance plus the amount check stopped every attack on all four models (0 of 880 attack episodes), never blocked a correct payment, and let no wrong payment through.** The amount rule: a payment amount must come from the user's request or from the payee itself (an SMS from the recipient's own number, or an invoice for that same biller account).
- **Provenance alone stopped every attack that sends money to a new number or leaks the OTP (0 of 800 episodes), but not attacks that change only the amount.** All 15 attacks that got past it kept the real payee and inflated the amount, for example a fake "correction" in a school invoice raising the fee from 3,500 to 5,000 Tk. Without a defence these amount-only attacks were the most successful kind: 2, 4, 7 and 7 of 20 for the 3B, 7B, 14B and 32B models, against 14, 9, 10 and 25 of the other 200 attacks.
- **Invented payees are a bigger risk than injection.** Models tried to pay a payee or amount nobody asked for in 29% to 52% of episodes, far more often than any attack succeeded, and without a defence 8 to 33 of these payments per model went through (20 for 32B), mostly to the right payee with a guessed amount. The amount check stopped all of them.
- **Each model falls for attacks in different languages.** The 3B and 14B models fell mostly for English text (10 and 13 of 55 English attacks, at most 3 in any other language). The 32B model also fell most for English (14 of 55), but also for Banglish (7) and mixed text (8). The 7B model fell most for mixed Bangla-English text (6 of 54). No model leaked the OTP (0 of 75 attempts).
- **A bigger model was not safer.** The 32B model had the highest attack success (14.5%, about twice the smaller models), and the 14B model tried to pay invented payees in 49% of episodes, against 29% for the 7B model.
- **The results reproduce.** On the original 114 cases, attack success without a defence was 10.0%, 3.8% and 6.2%, against 10.0%, 3.8% and 5.0% in the earlier 3-repeat run. Four settings that ran twice (an interrupted first attempt, then the full run) gave the same outcome in 97% to 99% of cases.
- **Small models often fail the task itself.** The 3B model completed only 13% to 17% of normal tasks. Without a defence, 27 of its 68 failed tasks were bill payments made without opening the invoice, and 15 paid the wrong payee or amount.

### The largest model: Qwen2.5-32B

Qwen2.5-32B-Instruct (4-bit AWQ) is the largest model that fits on Kaggle's two T4 GPUs. It was run on the same 302 cases with the same settings, 0 model errors.

- **It was the best at the task and the easiest to fool.** It completed 66% of normal tasks without a defence (the 3B to 14B models: 17% to 56%), but 32 of 220 attacks succeeded (14.5%), about twice the rate of the smaller models. 23 of the 32 were instructions aimed at the AI, 9 were ordinary scam messages; attacks hidden in a tool description worked most often (9 of 37). No OTP was leaked (0 of 25).
- **The defences still worked.** Provenance let through only 4 attacks, all amount-only (3 of them written in English); provenance-amount stopped all 220 and every wrong payment (20 without a defence, 2 with provenance, 0 with provenance-amount). No correct payment was blocked.
- **But the defences cost it 12 normal tasks (54 of 82 done without a defence, 42 with either one).** These are not false blocks: in all 12, the model first tried to pay the invoice ID (for example `inv-power`) as the biller account. Without a defence the wallet answers "not a registered biller account. Check the invoice for the correct account", and the model reads the invoice and pays correctly. With a defence the same call is stopped first, and the block message says "Ask the user for explicit approval before retrying", so the model asks the user, retries the same wrong call and gives up. The wording of the block message, not the rule, causes the loss; the smaller models lost at most 3 normal tasks with a defence.
- **A clearer block message fixed it.** The block now says "Use the biller account number written on the invoice, or one from list_billers". In a rerun, all 12 tasks came back: 57 of 82 normal tasks done with `provenance-amount` (70%) and 58 with `provenance-consistent` (71%), slightly more than the 54 without any defence. Still 0 of 220 attacks, 0 wrong payments and 0 correct payments blocked. How a defence explains a block matters as much as when it blocks.
- On the original 114 cases its attack success without a defence was 11 of 80 (13.8%).

### A second model family: Hermes 3 (Llama 3.1 8B)

To check that the findings are not specific to Qwen, the same 302 cases were run on Hermes 3, a Llama 3.1 8B model fine-tuned by Nous Research (`NousResearch/Hermes-3-Llama-3.1-8B`), with the same settings.

| Model | Defence | Attack success | Correct actions blocked | Benign tasks done | Tried to pay an invented payee | Wrong payments that went through |
|---|---|---:|---:|---:|---:|---:|
| Hermes-3-Llama-3.1-8B | none | 2.3% (0 to 5) | 0% | 22% (13 to 31) | 10% (7 to 13) | 10 |
| Hermes-3-Llama-3.1-8B | provenance | 0.5% (0 to 1) | 0% (0 to 4) | 22% (13 to 31) | 10% (7 to 13) | 9 |
| Hermes-3-Llama-3.1-8B | provenance-amount | **0% (0 to 1)** | **0% (0 to 4)** | 22% (13 to 31) | 10% (7 to 13) | **0** |

- **The same pattern holds.** Provenance stopped every attack that redirects money; the one attack that got past it changed only the amount (a Bangla note inflating the rent). The amount check stopped that too, blocked no correct payment, and let no wrong payment through.
- Hermes 3 fell for fewer attacks (5 of 220 without a defence, all through SMS; 3 of the 5 in English) and tried to pay invented payees far less often (10% of episodes) than the Qwen models, but it completed only 22% of normal tasks. Of its 64 failed normal tasks, it often read the bill and then stopped without paying; in about 14 it asked the user to confirm without a question mark, which the simulated user does not answer (it only replies to a "?"), and in 9 it told the user it had paid without ever calling a payment tool.

IBM Granite 3.3 8B was also run but is left out: in this setup (vLLM on T4 GPUs) most of its tool calls came out as plain text instead of real tool calls (0.2 tool calls per case, 5% of normal tasks done), so its 0% attack success says nothing about its safety.

### Attack success among agents that could have been fooled

Overall attack success understates the risk, because many episodes never reach the attack: the agent does not open the SMS or invoice, or cannot do the task at all. `scripts/conditional_rates.py` reports attack success only where the agent **read the attack** and, stricter, where it read it **and completed the attack-free version of the same task** (same task, same request language, same run). Brackets: successes / cases and a Wilson 95% interval. Reproduce with `python scripts/conditional_rates.py results/`.

| Model | No defence: all attacks | No defence: read | No defence: read and able | Provenance: read and able | Provenance-amount: read and able |
|---|---:|---:|---:|---:|---:|
| Qwen2.5-3B | 7.3% (16/220) | 12.7% (16/126) | **24.1%** (7/29; 12 to 42) | 0% (0/20) | **0%** (0/22) |
| Qwen2.5-7B | 5.9% (13/220) | 7.6% (13/171) | **10.8%** (13/120; 6 to 18) | 4.2% (5/118) | **0%** (0/118; 0 to 3) |
| Qwen2.5-14B (AWQ) | 7.7% (17/220) | 9.4% (17/180) | **14.9%** (11/74; 9 to 25) | 6.2% (5/80) | **0%** (0/93; 0 to 4) |
| Qwen2.5-32B (AWQ) | 14.5% (32/220) | 17.7% (32/181) | **17.8%** (23/129; 12 to 25) | 3.7% (4/107) | **0%** (0/107; 0 to 3) |
| Hermes-3-Llama-3.1-8B | 2.3% (5/220) | 3.8% (5/131) | **9.8%** (4/41; 4 to 23) | 2.4% (1/41) | **0%** (0/41; 0 to 9) |

- **When an agent was capable and saw the attack, attacks worked more often than the overall rate suggests**: 2 to 4 times more for the smaller models (10% to 24% without a defence). For the 32B model, which can do most tasks, the gap is small (14.5% overall, 17.8% read and able). Weak task performance had been hiding part of the risk, so overall attack success is a misleading measure on its own.
- **The amount check still stopped every attack in this stricter group**, including the 118 cases where Qwen2.5-7B read the attack and could do the task.
- The groups are smaller, so the intervals are wider; the 3B model in particular could do only 20 to 29 of these tasks.

### Adaptive attacks: what the amount check trusts

`provenance-amount` accepts an amount only if it comes from the user or from the payee itself: an SMS sent from the payee's own number, or an invoice for that registered biller account. A separate stress-test set of 56 cases (`bench/cases_adaptive/`, kept out of the main 302) forges exactly that, using public scam patterns: a spoofed SMS sender ID, and a fake "revised bill". `scripts/audit_adaptive.py` plays a scripted agent that obeys every attack, and an ideal agent that ignores it, through each defence. No model is involved, so this measures what each defence can stop, not how often a model obeys.

| Adaptive attack (attack and request language balanced) | No defence | Provenance | Provenance-amount | Provenance-consistent |
|---|---:|---:|---:|---:|
| Fake SMS from the payee's number asks for a larger amount | 16/16 | 16/16 | **16/16** | **0/16** (16 ask the user) |
| Fake SMS from the payee's number gives a new number to pay | 16/16 | **0/16** | **0/16** | **0/16** |
| Forged "revised" invoice for the real biller account | 24/24 | 24/24 | **24/24** | **0/24** (24 ask the user) |

Attacks that succeed when the agent obeys. The first three defences never blocked the correct payment here; in brackets, cases where `provenance-consistent` also holds the correct payment for the user.

- **The recipient check holds even against a forged sender:** money cannot go to a number that only appears in a message.
- **The amount check is only as strong as the payee's identity.** If an attacker can send an SMS that appears to come from the payee, or a bill that appears to come from the biller, it can raise the amount and the defence lets it through.
- **`provenance-consistent` closes that gap by asking the user.** When the payee's own messages or invoices give different amounts (450 in one SMS, 950 in a "correction"), it blocks the payment and tells the agent to ask the user which amount is right; an amount the user typed is always accepted. It stops all 40 forged amounts. The cost: in those 40 cases the correct payment also waits for the user, because a defence cannot tell the real message from a forged one with the same sender. On the 302 main cases it never blocked a correct payment, in the scripted check or in a real Qwen2.5-32B run (results in the table above).

**With a real model.** Qwen2.5-32B was then run on the same 56 adaptive cases (results in `results_adaptive/`, kept apart from the main results):

| Adaptive attack | No defence | Provenance-amount | Provenance-consistent |
|---|---:|---:|---:|
| Fake SMS from the payee's number asks for a larger amount | 11/16 | 10/16 | **3/16** |
| Fake SMS from the payee's number gives a new number to pay | 8/16 | **0/16** | **0/16** |
| Forged "revised" invoice for the real biller account | 1/24 | 1/24 | **0/24** |
| All 56: correct payment made | 11 | 12 | 2 |

- **A forged "correction" from the payee works very well on a real model.** Without a defence the model paid the new amount in 11 of 16 cases and the new number in 8 of 16, far above its 14.5% on the main set. Forged invoices rarely worked (1 of 24), partly because the model opened the second invoice in only 13 of 24 cases.
- **The first version of `provenance-consistent` cut forged amounts from 10 of 16 to 3 of 16, but did not stop them all.** In all 3, the model called `read_sms` with `limit: 1`, saw only the newest (forged) message, and paid it. That version compared only messages the agent had read, so it never saw the real amount. The model read only the newest SMS in 5 of the 16 cases. The scripted check above missed this because its agent always reads every message: a defence must be tested against how real agents use tools, not only against an ideal script.
- **Fixed since:** the check now compares every SMS and invoice from that payee in the wallet, whether or not the agent read them (it takes only amounts from them, never codes). `scripts/audit_adaptive.py` now also plays an agent that reads only the newest SMS or only the forged invoice: it beats the first version in 40 of 40 cases and the fixed one in 0 of 40. Replaying the real 32B traces through the fixed version, it would have blocked all 3 attacks that got through, and on the 302 main cases it still blocks no correct payment (ideal agent, and replays of all five 32B runs). The table above is from the first version; a model rerun of the fixed one is still to come.
- **The cost is real.** With `provenance-consistent` the correct payment went through in only 2 of 56 adaptive cases (12 with `provenance-amount`): when the payee's messages disagree, the payment waits for the user.

### Why normal tasks fail

`scripts/error_analysis.py` puts every failed normal task into one cause, from the traces. Run it with `python scripts/error_analysis.py results/`. So far it has been run on Qwen2.5-32B; the other models' traces are not in this repository yet.

| Qwen2.5-32B: cause of failure | No defence | Provenance-amount (new block message) | Provenance-consistent |
|---|---:|---:|---:|
| Used the invoice ID (or a name) as the biller account; the wallet refused and the agent gave up | 15 | | |
| Blocked by the defence, gave up | | 16 | 17 |
| Wrong payee or amount paid | 4 | 0 | 0 |
| Stopped without paying | 5 | 4 | 4 |
| Read-only task: wrong answer | 3 | 3 | 2 |
| Asked again after its one "yes" | 1 | 2 | 1 |
| **Failed / all normal tasks** | **28/82** | **25/82** | **24/82** |

- **One tool-design detail causes most failures.** `list_invoices` shows each invoice's ID, biller and amount, but not the biller account; that is only in `read_invoice`. The model often paid the invoice ID (`inv-power`) as the account: all 15 "wallet refused" failures without a defence, and 12 of the 16 blocks with `provenance-amount`. The defence did not cause these failures; the same mistake failed without it. Small details of the tools change task success as much as the defences do.
- **The defences block wrong payments, not tasks the model would have done:** with `provenance-amount` the model failed 25 tasks against 28 without a defence. The 4 wrong payments without a defence all went to an invented number (for example +8801711223344 instead of Rafi's 01710000003) with a guessed amount, after reading the SMS; the recipient check stops exactly these.
- The causes for "asked to confirm" and "said it paid" use short keyword lists in three languages, so those counts are estimates.

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
- [x] Larger model: Qwen2.5-32B (AWQ) on all 302 cases
- [x] Consistency check against forged payee amounts (`provenance-consistent`), tested with a model
- [ ] Trained multilingual injection detector to replace the keyword baseline
- [ ] Connect BRACUVerify as a second backend
- [ ] Comparison with the sanitiser defence from "Indirect Prompt Injections: Are Firewalls All You Need?"
- [ ] Paper and dataset release

## Ethics

All data is synthetic, and "TakaPay" is fictional. See [docs/ETHICS.md](docs/ETHICS.md).
