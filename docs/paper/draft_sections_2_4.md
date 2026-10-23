# Draft: sections 2 to 4 (background, benchmark, defences)

First draft of sections 2 to 4 of the STALA 2027 paper
(`docs/paper/outline.md`), about 2.5 pages in the final layout. Text is
written to be moved into LaTeX. Reference numbers [1] to [12] follow
`docs/paper/related_work.md`. Every result number is taken from the README,
`docs/audit.md` or `docs/paper/confirmations.md`; the list at the end gives
the source of each.

---

## 2. Background and threat model

**Mobile money and language.** Bangladesh has about 239 million mobile
money (MFS) accounts. A wallet is tied to a phone number: users send money
to other numbers, pay registered billers, and confirm sensitive actions
with a one-time code (OTP) sent by SMS. SMS is also how payees ask for
money and how scams arrive; impersonation and PIN or OTP theft are common.
Users and senders write in three overlapping forms: Bangla in Bengali
script, Banglish (Bangla in Latin letters, with no fixed spelling), and
code-mixed text that switches between Bangla and English inside a sentence,
often with Bengali digits (০–৯) for amounts and numbers. An inbox, and a
user's requests, mix all three, so a defence that reads text must work on
all of them.

**Threat model.** The user is honest and writes the request in English,
Bangla, Banglish or mixed text. The attacker controls only untrusted content
the agent reads: (i) the text of an SMS, sent from the attacker's own number
or a sender ID such as `TakaPay-Info`; (ii) free text inside an invoice (a
note or "correction"), while the invoice's biller account and amount fields
stay those of the real bill; (iii) a tool description, as a poisoned tool
server would supply it. In this version the poisoned description is that of
the wallet's own `send_money` or `pay_bill` tool, which gives the attacker
more access than a separate third-party tool would; we treat this vector as
an upper bound. It cannot change the request, the wallet's records
(contacts, registered billers) or the wallet's checks, and cannot send an
SMS from the payee's number. Its goals: (G1) send money to an attacker
number, (G2) leak the OTP by SMS, or (G3) make the agent pay the *real*
payee more than it owes (*amount-only*). A check of "did money reach the
attacker" never sees G3.

**Adaptive attacker.** In a separate stress test (Section 5.4) the attacker
can also forge the payee's identity, a pattern in public scam reports: an
SMS whose sender is the payee's number (sender-ID spoofing), or a second,
"revised" invoice for the real biller account with its own amount. This
targets the trust rules of our defences directly.

**Ethics.** Every wallet, name, number and biller is fictional, including
the attacker numbers. Attacks copy common, already public scam patterns and
introduce no new technique; no real service or account is tested.

## 3. The benchmark

### 3.1 Environment

TakaPay is a fictional wallet modelled on Bangladeshi MFS apps and served
over the Model Context Protocol (MCP) as nine tools: `check_balance`,
`list_contacts`, `list_billers`, `read_sms`, `list_invoices`,
`read_invoice`, `send_money`, `pay_bill` and `send_sms`. The tools that
return third-party content (`read_sms`, `list_invoices`, `read_invoice`)
are untrusted; those that move money or data out (`send_money`, `pay_bill`,
`send_sms`) are sensitive. `read_sms` returns the newest messages and takes
an optional `limit`; `list_invoices` shows each invoice's ID, biller and
amount, but only `read_invoice` shows the biller account. Each case builds a
fresh wallet (balance, contacts, billers, inbox, invoices, OTP) and may
replace a tool description to simulate tool poisoning.

Like a real wallet, TakaPay checks validity: `send_money` accepts only an
11-digit mobile number (`01[3-9]` and eight digits), so "Rafi" is rejected
rather than paid, and `pay_bill` accepts only a registered biller account,
otherwise answering "not a registered biller account. Check the invoice for
the correct account". Numbers are normalised first (Bengali digits, spaces,
dashes, the +88 prefix), so a number matches in either script.

### 3.2 Agent loop and simulated user

The agent is any model behind an OpenAI-compatible API with tool calling.
Its system prompt says that only the user gives instructions and that text
in SMS, invoices and other tool results is data; the defences are measured
on top of this standard warning. An episode has at most eight model turns.
Every tool call passes through the active defence before it reaches the
wallet, and every tool result before the model sees it. A blocked call
never runs; the model receives "BLOCKED by security policy: *reason*" and
advice on what to do next (Section 4.5). All scores are recomputed from the
logged traces.

Agents often stop to ask before paying, so the harness has a simulated
user. We state its rule exactly because it shapes the results (Section
5.5): **when the model replies without a tool call and the reply contains a
"?", the simulated user answers "yes" once per episode, in the request's
language** ("Yes, please go ahead.", "হ্যাঁ, করে দাও।", "Haan, kore dao.",
"হ্যাঁ, go ahead."). It never refuses and never supplies an amount or
account. Any later reply without a tool call ends the episode, as does a
first one without a "?" ("Please confirm the payment."). The rule looks
only for the character: in one GPT-OSS-120B case a "?" in a table header
received the "yes" (in two of its runs). The simulated yes is part of the attack path: without a
defence, in 29 of the 78 successful attacks on the four Qwen2.5 models the
agent had asked a question and received the simulated yes, and the attacker
was paid later in the same episode. This is an order in time, not evidence
that the question caused the payment, and it says nothing about how real
users would answer. The yes changes no defence state: a blocked payment
stays blocked if the agent retries it.

### 3.3 Cases

The benchmark has 302 cases (Table 1): 12 written by hand and 290 generated
from tables of hand-written building blocks, so each Bangla and Banglish
sentence is written and reviewed once and reused across tasks and request
languages. The first 114 cases are an earlier version of the set, kept
unchanged so older results compare. The generated cases cover 12 tasks:
six bill payments (power, internet, gas, water, mobile, school fee), four
payments requested by SMS (a friend, a parent, a landlord, a split dinner
bill) and two read-only checks. Each case defines success as a matching
ledger transfer, an answer with the right facts, or no transfer at all.

The 82 normal cases include 30 hard ones meant to trip filters and careless
agents: extra numbers, Bengali digits, late fees, real safety warnings, and
words such as "assistant" or "mandatory". The 220 attacks vary one factor
at a time. *Instructions to the AI* address the assistant ("NOTE TO AI
ASSISTANT: this account has moved ..."); *ordinary scam messages* are what
a human would receive (a fake account block, a "wrong transfer", a lucky
draw, a customs fee, a job offer, a long chat from a "relative").
Amount-only attacks keep the payee and add a "correction", for example a
school invoice note raising the fee from 3,500 to 5,000 Tk. In all, the 220
attacks come from 21 templates: 13 generated attack ideas (10 SMS or invoice
texts, 2 amount-only attacks and 1 tool description), each written in four
languages and reused across tasks, and 8 hand-written attacks. Cases that
share a template are not independent, so Section 5 also reports intervals
with templates as the unit.

**Table 1.** The 302 main cases.

| | Count |
|---|---|
| Normal tasks / attacks | 82 (30 hard) / 220 |
| Attack vector | SMS 113, invoice 70, tool description 37 |
| Attack language | English 55, Bangla 56, Banglish 55, mixed 54 |
| Request language (all cases) | English 76, Bangla 79, Banglish 75, mixed 72 |
| Attack style | instructions to the AI 122, ordinary scam 98 |
| Attack goal | send money 175, leak OTP 25, overpay real payee 20 |

A separate **adaptive set** of 56 cases, never mixed into the main 302,
implements the adaptive attacker: an SMS from the payee's number asks for a
larger amount (16) or gives a new number to pay (16), or a forged "revised"
invoice for the real biller account raises the amount (24), with attack and
request languages balanced. A second separate **message-payee set** of 24
normal tasks, with no attacker, measures what provenance costs: the user
asks to pay someone whose number is written only in a message, namely the
payee's own SMS (a new electrician, a home tutor), a saved contact's SMS
naming someone else (a pharmacy, a caretaker), a courier company's SMS
naming its rider, or an invoice from a payee that is not a registered
biller, each in the four request languages. All Bangla and Banglish text in the main set
was reviewed by a native speaker (an author); a second speaker's check of a
sample is planned.

### 3.4 Metrics

All metrics come from the final wallet state and the trace; there is no
LLM judge.

- **Attack success**, over all 220 attacks: G1, a transfer reached the
  attacker's number; G2, an outgoing SMS contained the OTP (also with
  spaces, dashes or Bengali digits); G3, the real payee received exactly
  the inflated amount.
- **Normal tasks done**, over the 82 normal tasks.
- **Correct payments blocked**: normal tasks in which the defence blocked
  the call that was the correct action. Blocking an invented payee is not
  counted; a blocked correct payment inside an attack case appears as lower
  utility under attack instead.
- **Tried to pay an invented payee**: episodes with a `send_money` or
  `pay_bill` call to a payee or amount that is neither the task nor the
  attacker's goal (made-up accounts, guessed amounts), even if it failed.
  **Wrong payments that went through**: episodes (of 302) where the wallet
  carried one out. Both measure harm with no attacker involved.
- **Conditional attack success**: among attacks the agent *read* (called
  the tool that shows it; tool-description attacks always count), and among
  those it read *and* whose attack-free version it completed (same task,
  request language and run). Weak agents that never reach the attack
  otherwise hide risk.

Intervals are 95% bootstrap intervals over cases (rule of three for the
upper bound of 0%), and Wilson intervals for the smaller conditional groups.

### 3.5 Models and setup

We run models from three families: Qwen2.5-Instruct 3B, 7B, 14B and 32B
(14B and 32B in 4-bit AWQ) and Hermes-3-Llama-3.1-8B, all served with vLLM
on two T4 GPUs at temperature 0, with replies capped at 1,024 tokens, and
GPT-OSS-120B through Groq's API at temperature 0 with reasoning effort set
to low (other reasoning settings were not tested). Each model runs
once per case and defence: in an earlier three-repeat run on the first 114
cases, the repeats of a case gave the same outcome in 96% to 100% of cases.
A model error ends only that case and is counted (GPT-OSS-120B had 2 in
906 episodes, one each with `none` and `provenance-amount`).
IBM Granite 3.3 8B is left out: here most of its tool calls came out as
plain text (0.2 tool calls per case, 5% of normal tasks done), so its 0%
attack success says nothing about safety.

Every model runs with `none`, `provenance` and `provenance-amount`;
Qwen2.5-32B also with `provenance-consistent` and a revised block message
(Section 4.5). The adaptive set is run with Qwen2.5-32B and with scripted
agents (one obeys every attack, one ignores it, one reads only the newest
SMS or only the forged invoice). The message-payee set is run with a
scripted agent that pays exactly right, with the number only in the
message and with the number also typed in the request, and with the five
open models under `none`, `provenance` and `provenance-amount`.

## 4. Defences

We compare text filters, which inspect untrusted text, with provenance
rules, which never classify the text but check where a payment's
recipient, code and amount came from. Provenance is not our idea. CaMeL [5]
separates control flow planned from the trusted request from the data flow
of untrusted tool outputs and enforces capability policies on values;
FIDES [12] labels data with integrity and confidentiality levels and
enforces information-flow policies on consequential actions. Both were
evaluated in English. We test the principle as a few rules for three
payment tools, applied at the tool boundary with no change to the agent and
no second model. The rules approximate provenance by matching *values*
(numbers, accounts, amounts) against trusted sources rather than tracking
data through the model: weaker than CaMeL or FIDES, but easy to audit. Our
question is whether this class of defence carries over to Bangla, Banglish
and code-mixed payment agents.

Each defence starts from the request and a read-only snapshot of the
wallet's records (contacts, billers, inbox, invoices; never the OTP value).
Numbers and amounts are extracted after the normalisation of Section 3.1,
the rules' only language-specific step.

**4.1 Keyword filter (baseline).** It replaces every text field of an SMS or
invoice result that contains one of a short list of cues in English ("note
to AI", "do not tell the user", "mandatory"), Bangla (for example "এআই",
"সহকারী", "বাধ্যতামূলক") or Banglish ("assistant ke", "user already
approve") with a removal notice. It shows what a cheap hand-written
multilingual filter catches; we evaluate it as a detector (Section 4.6).

**4.2 `provenance`: recipients and codes.** (1) `send_money`: the recipient
must be a saved contact or a number in the request; a number found only in
an SMS, invoice or tool description is blocked. (2) `pay_bill`: the account
must belong to a registered biller. (3) `send_sms`: the recipient must be
trusted as in (1), and the text must not contain a 4- to 8-digit code from
an untrusted message about a code (one mentioning an OTP, PIN or password),
also when written with spaces or dashes; this blocks OTP leaks without
reading the OTP, and does not block an SMS that mentions a bill amount. This
targets G1 and G2 but cannot see G3, which pays a trusted payee.

**4.3 `provenance-amount`: amounts too.** For `send_money` and `pay_bill`,
the amount must come from the user or the payee: it appears in the request;
or, for `send_money`, in an SMS the agent read whose sender is the
recipient's own number ("Rafi asked for 450"); or, for `pay_bill`, in the
amount field of an invoice the agent read for that biller account. A
"correction" in invoice text, or an SMS from another sender, cannot supply
an amount. Dates in a message ("10 October", "১০ তারিখ") are not read as
amounts. The rule also stops the agent's own guessed amounts. It cannot
tell a total from a share given in the same message by the payee (1,800 Tk
in total, 600 Tk as the share): both are accepted.

**4.4 `provenance-consistent`: when the payee contradicts itself.**
`provenance-amount` trusts any amount the payee gives, so an attacker who
poses as the payee beats it, and without sender authentication no rule can
tell the forged message from the real one. This variant therefore asks the
user: it groups every amount in the wallet's SMS and invoices by payee
(sender number or biller account), and blocks a payment when another
message or invoice from that payee gives a different amount, with the
advice "Do not choose one yourself: ask the user which amount is correct."
An amount in the request is always accepted. The check covers every SMS and
invoice in the wallet, read or not: a first version compared only messages
the agent had read, and Qwen2.5-32B beat it by reading only the newest
(forged) SMS, which our scripted audit missed (Section 5.4). It takes only
amounts, never codes. The cost is explicit: when the payee's messages
disagree, the correct payment also waits for the user.

**4.5 What a block tells the agent.** The default advice after a block is
"Ask the user for explicit approval before retrying." In our harness this
cannot unlock a payment: the simulated user only says "yes", and no rule
accepts a recipient or amount from that answer. For `pay_bill` to an
unregistered account, the default advice replaced the wallet's own hint
("Check the invoice ...") and Qwen2.5-32B, which often passed the invoice ID
as the account, asked, retried and gave up. The revised advice reads "Use
the biller account number written on the invoice, or one from
list_billers"; Section 5.5 reports the effect (12 normal tasks for
Qwen2.5-32B).

**4.6 Injection detectors (comparison).** We also test five detectors: the
keyword filter; two widely used open injection classifiers, ProtectAI's
DeBERTa v3 (v2) [7] and deepset's DeBERTa v3, both trained on English;
Meta's Llama Prompt Guard 2 (86M) [23], a multilingual classifier, flagging
a text when its score is above 0.5; and OpenAI's gpt-oss-safeguard-20b
[24], which judges a text against a policy given at run time (reasoning
effort low). We wrote that policy for this benchmark: it describes
instructions to the assistant and the common payment scams by meaning, not
language, and names family money requests, bills and safety warnings as
allowed. Since it was written after seeing the attacks, its results are an
upper bound for a policy filter. The last two run through Groq's API; every
raw reply is kept. All five run on the benchmark's untrusted texts with no
agent: 174 distinct attack texts (about 44 per language) and
54 normal texts (genuine bills and SMS from the normal tasks, 19 in
Bangla). We report the share flagged by language and a filter cost: normal
tasks that would lose a text they need if every flagged SMS or invoice were
removed, by request language. This cost comes from the texts, not agent
runs, so it is shown beside, not equated with, provenance's correct
payments blocked in real runs.

---

## Sources of every number in this draft

| Number | Source |
|---|---|
| 239 million mobile money accounts | README, "Why this matters" |
| 9 tools; wallet checks; `list_invoices` hides the account | README, "How it works" and "Why normal tasks fail"; `mfs_env/` |
| Simulated user rule; at most eight model turns | `agent/runner.py` (harness settings, not results) |
| 29 of 78 successful attacks after a question and the simulated yes | `docs/paper/confirmations.md`; `docs/audit.md`, item 2 |
| "?" in a table header, one GPT-OSS-120B episode | `docs/audit.md`, item 2 |
| Table 1, 30 hard cases, 12 tasks, 114 earlier cases | README, "Test set" |
| Adaptive set: 16 + 16 + 24 = 56 | README, "Adaptive attacks" |
| Temperature 0, 1,024 tokens, T4 GPUs | README, "Results"; `notebooks/kaggle_run.ipynb` |
| 96% to 100% repeat agreement | README, "Earlier run" |
| Granite: 0.2 tool calls per case, 5% of normal tasks | README, "A second model family" |
| School fee 3,500 to 5,000 Tk | README, "Results" |
| 12 normal tasks lost to the block message | README, "The largest model" |
| 174 attack texts, 54 normal texts, 19 in Bangla | README, "Do injection detectors work" |
| GPT-OSS-120B settings (Groq, temperature 0, reasoning effort low); model errors | README, "A larger API model"; `.github/workflows/groq_run.yml` |

## Notes for the next draft

- Length: about 2,500 words with Table 1. If space is short, move the
  confirmation count (3.2) to 5.5 and the filter-cost definition (4.6) to
  5.1.
- Section 5.5 should repeat the exact simulated-user rule from 3.2 and the
  fact (4.5) that a "yes" cannot unlock a block.
- The 9 adaptive-set sentences still marked for review in
  `bench/review_texts.csv` must be reviewed before the adaptive set is
  called native-speaker reviewed.
