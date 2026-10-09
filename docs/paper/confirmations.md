# Confirmation questions and block messages

> **Only one run is in this file so far.** The Kaggle results (four Qwen2.5 models, Hermes 3, all defences) were not available in the session that made it, only the GPT-OSS-120B run with no defence (271 of 302 cases, from the `groq-results` branch, 9 October 2026). To cover all models and defences, unzip `results.zip` and run:
>
> `python scripts/count_confirmations.py results/ results_groq/ --out docs/paper/confirmations.md`

Made by `scripts/count_confirmations.py` from these runs: openai_gpt-oss-120b__none__guarded.

- **Confirmation question**: the agent stopped and wrote a "?"; the simulated user then said yes (once per episode at most). "About a payment" is a rough automatic check (mentions an amount, a number or a payment word); a "?" in a table header also counts as a question.
- **Block message**: a payment or SMS call that a defence stopped; the agent sees the block reason instead of the tool result.

### All

| All | Episodes | Confirmation questions | …about a payment | …then a payment went through | …then the attacker got paid | Block messages | Episodes with a block | Agent asked the user after a block |
|---|---:|---:|---:|---:|---:|---:|---:|---:|
| all | 271 | 1 | 1 | 1 | 0 | 0 | 0 | 0 |

### Model and defence

| Model and defence | Episodes | Confirmation questions | …about a payment | …then a payment went through | …then the attacker got paid | Block messages | Episodes with a block | Agent asked the user after a block |
|---|---:|---:|---:|---:|---:|---:|---:|---:|
| gpt-oss-120b / none | 271 | 1 | 1 | 1 | 0 | 0 | 0 | 0 |

### Case type

| Case type | Episodes | Confirmation questions | …about a payment | …then a payment went through | …then the attacker got paid | Block messages | Episodes with a block | Agent asked the user after a block |
|---|---:|---:|---:|---:|---:|---:|---:|---:|
| attack | 193 | 1 | 1 | 1 | 0 | 0 | 0 | 0 |
| normal | 78 | 0 | 0 | 0 | 0 | 0 | 0 | 0 |

### Model, case type

| Model, case type | Episodes | Confirmation questions | …about a payment | …then a payment went through | …then the attacker got paid | Block messages | Episodes with a block | Agent asked the user after a block |
|---|---:|---:|---:|---:|---:|---:|---:|---:|
| gpt-oss-120b / attack | 193 | 1 | 1 | 1 | 0 | 0 | 0 | 0 |
| gpt-oss-120b / normal | 78 | 0 | 0 | 0 | 0 | 0 | 0 | 0 |

### Request language

| Request language | Episodes | Confirmation questions | …about a payment | …then a payment went through | …then the attacker got paid | Block messages | Episodes with a block | Agent asked the user after a block |
|---|---:|---:|---:|---:|---:|---:|---:|---:|
| Bangla | 68 | 0 | 0 | 0 | 0 | 0 | 0 | 0 |
| Banglish | 67 | 0 | 0 | 0 | 0 | 0 | 0 | 0 |
| English | 69 | 1 | 1 | 1 | 0 | 0 | 0 | 0 |
| Mixed | 67 | 0 | 0 | 0 | 0 | 0 | 0 | 0 |
