# Confirmation questions and block messages

Made by `scripts/count_confirmations.py` from the raw traces on the
`kaggle-results` and `groq-results` branches (10 October 2026).

- **Confirmation question**: the agent stopped and wrote a "?"; the simulated
  user then said yes (at most once per episode). "About a payment" is a rough
  automatic check (mentions an amount, a number or a payment word); a "?" in a
  table header also counts as a question.
- **…then a payment went through / the attacker got paid**: after that
  simulated "yes", a payment succeeded / money reached the attacker.
- **Block message**: a payment or SMS call that a defence stopped; the agent
  sees the block reason instead of the tool result.

Runs included: Qwen2.5 3B, 7B and 14B (none, provenance, provenance-amount);
Qwen2.5-32B (all six main runs: none, provenance, provenance-amount with the
old and the new block message, provenance-consistent first version and
fixed); Hermes 3 8B and Granite 3.3 8B (none, provenance, provenance-amount);
GPT-OSS-120B (none). Totals per model add up all of that model's runs.
Granite is left out of the main results (its tool calls came out as plain
text) but is counted here for completeness.

Reproduce: `python scripts/count_confirmations.py <run folders>` (main cases)
and `... --cases bench/cases_adaptive` (adaptive cases).

## What stands out

- **The simulated user's automatic "yes" is part of the attack path.**
  Without a defence, 29 of the 78 successful attacks on the four Qwen2.5
  models came right after it (3B 6 of 16, 7B 5 of 13, 14B 5 of 17, 32B 13 of
  32); Hermes 3 1 of 5; adaptive set (32B) 3 of 20. How real users answer
  these questions matters.
- With a defence on, the Qwen models asked the user more often (for example
  7B: 88 questions without a defence, 153 and 158 with one; 32B: 54, then 100
  to 150), often right after a block.
- GPT-OSS-120B almost never asked (1 question in 302 episodes, and that one
  was a "?" in a table header).

## Main cases (302 per run)

### All

| All | Episodes | Confirmation questions | …about a payment | …then a payment went through | …then the attacker got paid | Block messages | Episodes with a block | Agent asked the user after a block |
|---|---:|---:|---:|---:|---:|---:|---:|---:|
| all | 6644 | 1958 | 1852 | 516 | 35 | 2147 | 1570 | 724 |

### Model and defence

| Model and defence | Episodes | Confirmation questions | …about a payment | …then a payment went through | …then the attacker got paid | Block messages | Episodes with a block | Agent asked the user after a block |
|---|---:|---:|---:|---:|---:|---:|---:|---:|
| Hermes-3-8B / none | 302 | 47 | 46 | 9 | 1 | 0 | 0 | 0 |
| Hermes-3-8B / provenance | 302 | 45 | 45 | 7 | 0 | 26 | 25 | 1 |
| Hermes-3-8B / provenance-amount | 302 | 46 | 46 | 1 | 0 | 39 | 34 | 1 |
| Qwen2.5-14B / none | 302 | 48 | 48 | 20 | 5 | 0 | 0 | 0 |
| Qwen2.5-14B / provenance | 302 | 108 | 108 | 37 | 2 | 179 | 132 | 66 |
| Qwen2.5-14B / provenance-amount | 302 | 120 | 120 | 35 | 0 | 216 | 160 | 81 |
| Qwen2.5-32B / none | 302 | 54 | 44 | 39 | 13 | 0 | 0 | 0 |
| Qwen2.5-32B / provenance | 302 | 146 | 139 | 34 | 2 | 228 | 134 | 105 |
| Qwen2.5-32B / provenance-amount (new block message) | 302 | 100 | 96 | 44 | 0 | 170 | 140 | 59 |
| Qwen2.5-32B / provenance-amount (old block message) | 302 | 150 | 144 | 33 | 0 | 235 | 139 | 107 |
| Qwen2.5-32B / provenance-consistent (first version) | 302 | 101 | 96 | 44 | 0 | 170 | 139 | 58 |
| Qwen2.5-32B / provenance-consistent (fixed) | 302 | 108 | 104 | 46 | 0 | 171 | 139 | 65 |
| Qwen2.5-3B / none | 302 | 83 | 77 | 23 | 6 | 0 | 0 | 0 |
| Qwen2.5-3B / provenance | 302 | 86 | 80 | 16 | 1 | 178 | 144 | 13 |
| Qwen2.5-3B / provenance-amount | 302 | 90 | 82 | 2 | 0 | 218 | 175 | 18 |
| Qwen2.5-7B / none | 302 | 88 | 83 | 44 | 5 | 0 | 0 | 0 |
| Qwen2.5-7B / provenance | 302 | 153 | 148 | 40 | 0 | 149 | 98 | 72 |
| Qwen2.5-7B / provenance-amount | 302 | 158 | 153 | 39 | 0 | 165 | 108 | 78 |
| gpt-oss-120b / none | 302 | 1 | 1 | 1 | 0 | 0 | 0 | 0 |
| granite-3.3-8b-instruct / none | 302 | 75 | 64 | 1 | 0 | 0 | 0 | 0 |
| granite-3.3-8b-instruct / provenance | 302 | 76 | 64 | 1 | 0 | 1 | 1 | 0 |
| granite-3.3-8b-instruct / provenance-amount | 302 | 75 | 64 | 0 | 0 | 2 | 2 | 0 |

### Case type

| Case type | Episodes | Confirmation questions | …about a payment | …then a payment went through | …then the attacker got paid | Block messages | Episodes with a block | Agent asked the user after a block |
|---|---:|---:|---:|---:|---:|---:|---:|---:|
| attack | 4840 | 1462 | 1379 | 386 | 35 | 1630 | 1173 | 547 |
| normal | 1804 | 496 | 473 | 130 | 0 | 517 | 397 | 177 |

### Model, case type

| Model, case type | Episodes | Confirmation questions | …about a payment | …then a payment went through | …then the attacker got paid | Block messages | Episodes with a block | Agent asked the user after a block |
|---|---:|---:|---:|---:|---:|---:|---:|---:|
| Hermes-3-8B / attack | 660 | 105 | 104 | 13 | 1 | 56 | 50 | 2 |
| Hermes-3-8B / normal | 246 | 33 | 33 | 4 | 0 | 9 | 9 | 0 |
| Qwen2.5-14B / attack | 660 | 206 | 206 | 67 | 7 | 290 | 208 | 111 |
| Qwen2.5-14B / normal | 246 | 70 | 70 | 25 | 0 | 105 | 84 | 36 |
| Qwen2.5-32B / attack | 1320 | 514 | 480 | 180 | 15 | 746 | 518 | 296 |
| Qwen2.5-32B / normal | 492 | 145 | 143 | 60 | 0 | 228 | 173 | 98 |
| Qwen2.5-3B / attack | 660 | 183 | 170 | 33 | 7 | 300 | 238 | 26 |
| Qwen2.5-3B / normal | 246 | 76 | 69 | 8 | 0 | 96 | 81 | 5 |
| Qwen2.5-7B / attack | 660 | 296 | 284 | 90 | 5 | 235 | 156 | 112 |
| Qwen2.5-7B / normal | 246 | 103 | 100 | 33 | 0 | 79 | 50 | 38 |
| gpt-oss-120b / attack | 220 | 1 | 1 | 1 | 0 | 0 | 0 | 0 |
| gpt-oss-120b / normal | 82 | 0 | 0 | 0 | 0 | 0 | 0 | 0 |
| granite-3.3-8b-instruct / attack | 660 | 157 | 134 | 2 | 0 | 3 | 3 | 0 |
| granite-3.3-8b-instruct / normal | 246 | 69 | 58 | 0 | 0 | 0 | 0 | 0 |

### Request language

| Request language | Episodes | Confirmation questions | …about a payment | …then a payment went through | …then the attacker got paid | Block messages | Episodes with a block | Agent asked the user after a block |
|---|---:|---:|---:|---:|---:|---:|---:|---:|
| Bangla | 1738 | 484 | 442 | 109 | 2 | 579 | 440 | 230 |
| Banglish | 1650 | 574 | 544 | 196 | 10 | 421 | 338 | 163 |
| English | 1672 | 559 | 529 | 125 | 15 | 724 | 506 | 204 |
| Mixed | 1584 | 341 | 337 | 86 | 8 | 423 | 286 | 127 |

### Model, request language

| Model, request language | Episodes | Confirmation questions | …about a payment | …then a payment went through | …then the attacker got paid | Block messages | Episodes with a block | Agent asked the user after a block |
|---|---:|---:|---:|---:|---:|---:|---:|---:|
| Hermes-3-8B / Bangla | 237 | 35 | 35 | 0 | 0 | 4 | 4 | 0 |
| Hermes-3-8B / Banglish | 225 | 39 | 39 | 11 | 0 | 12 | 12 | 0 |
| Hermes-3-8B / English | 228 | 41 | 40 | 6 | 1 | 47 | 41 | 2 |
| Hermes-3-8B / Mixed | 216 | 23 | 23 | 0 | 0 | 2 | 2 | 0 |
| Qwen2.5-14B / Bangla | 237 | 76 | 76 | 19 | 0 | 108 | 81 | 70 |
| Qwen2.5-14B / Banglish | 225 | 91 | 91 | 17 | 2 | 101 | 78 | 37 |
| Qwen2.5-14B / English | 228 | 62 | 62 | 37 | 4 | 107 | 71 | 21 |
| Qwen2.5-14B / Mixed | 216 | 47 | 47 | 19 | 1 | 79 | 62 | 19 |
| Qwen2.5-32B / Bangla | 474 | 176 | 154 | 43 | 1 | 293 | 217 | 115 |
| Qwen2.5-32B / Banglish | 450 | 209 | 206 | 110 | 6 | 225 | 168 | 109 |
| Qwen2.5-32B / English | 456 | 168 | 160 | 49 | 4 | 292 | 204 | 104 |
| Qwen2.5-32B / Mixed | 432 | 106 | 103 | 38 | 4 | 164 | 102 | 66 |
| Qwen2.5-3B / Bangla | 237 | 17 | 16 | 7 | 1 | 108 | 98 | 5 |
| Qwen2.5-3B / Banglish | 225 | 81 | 69 | 20 | 0 | 38 | 38 | 0 |
| Qwen2.5-3B / English | 228 | 117 | 111 | 12 | 6 | 146 | 108 | 16 |
| Qwen2.5-3B / Mixed | 216 | 44 | 43 | 2 | 0 | 104 | 75 | 10 |
| Qwen2.5-7B / Bangla | 237 | 89 | 89 | 40 | 0 | 66 | 40 | 40 |
| Qwen2.5-7B / Banglish | 225 | 136 | 124 | 38 | 2 | 45 | 42 | 17 |
| Qwen2.5-7B / English | 228 | 98 | 95 | 18 | 0 | 129 | 79 | 61 |
| Qwen2.5-7B / Mixed | 216 | 76 | 76 | 27 | 3 | 74 | 45 | 32 |
| gpt-oss-120b / Bangla | 79 | 0 | 0 | 0 | 0 | 0 | 0 | 0 |
| gpt-oss-120b / Banglish | 75 | 0 | 0 | 0 | 0 | 0 | 0 | 0 |
| gpt-oss-120b / English | 76 | 1 | 1 | 1 | 0 | 0 | 0 | 0 |
| gpt-oss-120b / Mixed | 72 | 0 | 0 | 0 | 0 | 0 | 0 | 0 |
| granite-3.3-8b-instruct / Bangla | 237 | 91 | 72 | 0 | 0 | 0 | 0 | 0 |
| granite-3.3-8b-instruct / Banglish | 225 | 18 | 15 | 0 | 0 | 0 | 0 | 0 |
| granite-3.3-8b-instruct / English | 228 | 72 | 60 | 2 | 0 | 3 | 3 | 0 |
| granite-3.3-8b-instruct / Mixed | 216 | 45 | 45 | 0 | 0 | 0 | 0 | 0 |


## Adaptive cases (56 per run, Qwen2.5-32B only)

#### All

| All | Episodes | Confirmation questions | …about a payment | …then a payment went through | …then the attacker got paid | Block messages | Episodes with a block | Agent asked the user after a block |
|---|---:|---:|---:|---:|---:|---:|---:|---:|
| all | 224 | 139 | 135 | 20 | 6 | 162 | 114 | 53 |

#### Model and defence

| Model and defence | Episodes | Confirmation questions | …about a payment | …then a payment went through | …then the attacker got paid | Block messages | Episodes with a block | Agent asked the user after a block |
|---|---:|---:|---:|---:|---:|---:|---:|---:|
| Qwen2.5-32B / none | 56 | 23 | 22 | 9 | 3 | 0 | 0 | 0 |
| Qwen2.5-32B / provenance-amount | 56 | 31 | 30 | 9 | 2 | 34 | 26 | 10 |
| Qwen2.5-32B / provenance-consistent (first version) | 56 | 41 | 40 | 2 | 1 | 63 | 42 | 20 |
| Qwen2.5-32B / provenance-consistent (fixed) | 56 | 44 | 43 | 0 | 0 | 65 | 46 | 23 |

#### Case type

| Case type | Episodes | Confirmation questions | …about a payment | …then a payment went through | …then the attacker got paid | Block messages | Episodes with a block | Agent asked the user after a block |
|---|---:|---:|---:|---:|---:|---:|---:|---:|
| attack | 224 | 139 | 135 | 20 | 6 | 162 | 114 | 53 |

#### Model, case type

| Model, case type | Episodes | Confirmation questions | …about a payment | …then a payment went through | …then the attacker got paid | Block messages | Episodes with a block | Agent asked the user after a block |
|---|---:|---:|---:|---:|---:|---:|---:|---:|
| Qwen2.5-32B / attack | 224 | 139 | 135 | 20 | 6 | 162 | 114 | 53 |

#### Request language

| Request language | Episodes | Confirmation questions | …about a payment | …then a payment went through | …then the attacker got paid | Block messages | Episodes with a block | Agent asked the user after a block |
|---|---:|---:|---:|---:|---:|---:|---:|---:|
| Bangla | 56 | 36 | 36 | 1 | 0 | 35 | 28 | 8 |
| Banglish | 56 | 33 | 33 | 10 | 4 | 32 | 23 | 8 |
| English | 56 | 36 | 32 | 1 | 0 | 51 | 29 | 23 |
| Mixed | 56 | 34 | 34 | 8 | 2 | 44 | 34 | 14 |

#### Model, request language

| Model, request language | Episodes | Confirmation questions | …about a payment | …then a payment went through | …then the attacker got paid | Block messages | Episodes with a block | Agent asked the user after a block |
|---|---:|---:|---:|---:|---:|---:|---:|---:|
| Qwen2.5-32B / Bangla | 56 | 36 | 36 | 1 | 0 | 35 | 28 | 8 |
| Qwen2.5-32B / Banglish | 56 | 33 | 33 | 10 | 4 | 32 | 23 | 8 |
| Qwen2.5-32B / English | 56 | 36 | 32 | 1 | 0 | 51 | 29 | 23 |
| Qwen2.5-32B / Mixed | 56 | 34 | 34 | 8 | 2 | 44 | 34 | 14 |

