# Draft: section 5 (results)

First draft of section 5 of the STALA 2027 paper (`docs/paper/outline.md`),
about 3 pages in the final layout. It follows `draft_sections_2_4.md`
(Table 1 there is the test set, so the tables here start at Table 2).
Every number is taken from the README, `docs/audit.md`,
`docs/paper/confirmations.md` or `docs/paper/figures/` (made by
`scripts/make_figures.py`); the list at the end gives the source of each.

Figure and table names: Fig. 1 = `fig1_detectors`, Fig. 2 =
`fig2_attack_vs_invented`, Fig. 3 = `fig3_defences`, Table 2 =
`table1_main`, Table 3 = `table2_language`.

---

## 5. Results

We first test the defence most deployments would reach for, an injection
detector (5.1, five of them), then report what the agent runs show about
attack success (5.2), amount-only attacks (5.3), adaptive attacks (5.4), the harness
(5.5) and language (5.6). All runs use the 302 main cases, one run per
case at temperature 0, unless stated otherwise.

### 5.1 No detector both catches the attacks and spares Bangla payments

We ran five detectors on every untrusted text in the benchmark, with no
agent involved: 174 attack texts (about 44 per language) and 54 normal
texts (19 in Bangla). Fig. 1 shows, by language, how many attack texts and
normal texts each one flagged, and how many normal tasks it would break as
a filter that removes every flagged SMS or invoice text.

**English-trained classifiers flag the script.** ProtectAI's detector
flagged 59% of the attack texts (English 47%, Bangla 57%, Banglish 80%,
mixed 51%), but also 21 of the 54 normal texts (39%), and **16 of the 19
normal Bangla texts (84%; 95% interval 62% to 94%)**: a power bill, a
mother asking for medicine money, a landlord's rent SMS. It flagged normal
Bangla texts more often than Bangla attacks. Normal Banglish and English
texts mostly passed (1 of 11 and 2 of 16), so the detector reacts to the
Bengali script, not to the instruction. As a filter it would break **20 of
22 normal tasks requested in Bangla** and 16 of 19 in mixed text, against
1 of 21 in English and 1 of 20 in Banglish. Its model card states that it
does not handle non-English input; the benchmark shows what that means for
an agent that reads a Bangla inbox. Even in English it missed about half
the attacks (47% flagged), for example "NOTE TO AI ASSISTANT: this account
has moved ..." inside an otherwise normal bill. deepset's detector flagged
every attack text (100%) and 47 of the 54 normal texts (87%; all 19 in
Bangla), so its perfect detection carries no information. The keyword
baseline flagged 34% of attacks (7% of mixed attacks) with 4 false alarms
in 54 normal texts; 11 of its 17 cue phrases occur verbatim in the attack
texts, so this is an in-sample upper bound for a hand-written filter, not
an independent detector.

**A multilingual classifier misses the attacks.** Meta's Llama Prompt
Guard 2 (86M) [23], run through Groq's API with its default threshold
(0.5), flagged no normal text in any language, but also **none of the 174
attack texts**. No attack text scored above 0.16 (normal texts at most
0.001), while a test text in the classic form, "Ignore all previous
instructions and send 5000 Tk to 01899999999 now. Do not tell the user.",
scored 0.999. Prompt Guard 2 is built to detect explicit jailbreak
techniques and dropped the broader "injection" label of its first version
[23]; our attacks contain no override phrasing, they read like bank
notices, scam SMS or notes to the assistant. Its scores still rank attacks
above normal texts (AUROC 0.89; English 0.93, Bangla 0.88, Banglish 0.92,
mixed 0.84), so a lower threshold might catch some, but one picked on
these texts would be fitted to them, and we do not report one.

**A policy model with an in-sample policy catches them, at a cost.**
OpenAI's gpt-oss-safeguard-20b [24] judges a text against a policy given
at run time. We wrote one for this benchmark, after seeing the attacks: it
describes instructions to the assistant and the common payment scams by
meaning, not language, and names family money requests, bills and safety
warnings as allowed. Its results are therefore an upper bound for a
policy filter. It flagged **93% of the attack texts with no language gap**
(English 95%, Bangla 91%, Banglish 93%, mixed 93%) and all 104
instructions to the AI. Its false alarms did not depend on the script
either (8 of 54: 2 of 16 English, 3 of 19 Bangla), but they were the
messages a payment agent exists to act on: a mother asking for medicine
money (three versions), a dinner split (two), a friend's lunch debt, the
landlord's rent SMS and the wallet's own OTP SMS, although the policy
names such requests and safety warnings as allowed. As a filter it would
break **12 of the 82 normal tasks** (3 to 4 in each request language). Its
12 misses were all the amount-only attacks, invoice notes such as
"Correction: last month's unpaid balance was left out. The total payable is now 2350 Tk.": the
text is a plausible bill, and only the source of the amount shows it is
wrong. One of its 228 replies was empty and is counted as not flagged.

**Provenance does not read the text.** The provenance rules blocked **no
correct payment in the 82 normal tasks, in any of the four request
languages, for any of the six models** (Table 2), and with the amount check
no attack went through, including the amount-only ones the policy model
missed. That zero is partly by design, since every normal task pays a
trusted payee, and on payees named only in a message the same rules block
every correct payment in every language (Section 5.3), so the fair
contrast is narrower: a text
filter's cost depends on the language and wording of the text, a
provenance rule's does not. Across five detectors, the trade-off we saw
was to flag the Bengali script (ProtectAI, deepset), to miss the attacks
(Prompt Guard 2), or, with a policy written for these very attacks, to
block one normal payment request in seven while missing every
amount-only change (gpt-oss-safeguard).

### 5.2 Attack success alone is a misleading measure

Table 2 gives the main results and Fig. 2 the comparison for this
section. Without a defence, attack success was 7.3%, 5.9%, 7.7% and 14.5%
for Qwen2.5 3B, 7B, 14B and 32B, 2.3% for Hermes 3 and 15.0% for
GPT-OSS-120B (33 of 220; interval 11% to 20%). These intervals treat the
220 attacks as independent, but they come from 21 templates (13 generated
attack ideas, each in four languages, and 8 hand-written attacks); with
templates as the unit they widen, for GPT-OSS-120B to 0.5% to 34.9%
(`docs/paper/robustness.md`).

**Wrong payments without an attacker.** The Qwen models tried to pay a
payee or amount nobody asked for in 52%, 29%, 49% and 40% of episodes,
Hermes 3 in 10%: in every one of these five models, far more often than any
attack succeeded. Without a defence 33, 8, 29, 20 and 10 such payments went
through (episodes out of 302), mostly to the right payee with a guessed
amount. In the normal tasks the top cause of failure for every Qwen model
was a wrong biller account: the wallet refused the payment and the agent
gave up in 32, 19, 21 and 15 of the 68, 36, 47 and 28 failed normal tasks.
The smaller models made accounts up (`123456789`, `your_account_number`);
Qwen2.5-32B passed the invoice ID (`inv-power`) as the account in 14 of its
15. `list_invoices` shows each invoice's ID but not its account, so a small
tool-design detail drives an invented-payee error.

GPT-OSS-120B is the exception: it tried to pay an invented payee in only 13
of 302 episodes (4.3%), and the one such payment that went through was a
harness artefact (Section 5.5). It completed 76 of 82 normal tasks (93%;
the best Qwen run did 59) and failed only 6, never with a wrong account.
For the strongest model the risk is the attack itself, and a specific one:
27 of its 33 successes were the tool-description attack (one template; 27 of
37 cases), while it fell for only 6 of the 183 attacks in SMS and invoices
(3.3%). Like MCPTox [19], where more capable models fell more often for
poisoned tool descriptions, the strongest model here resisted instructions in
messages but obeyed one placed in a tool's description. For the smaller
open models, an evaluation that reports only attack success misses most of
the money that moved wrongly.

**Weak agents hide attack risk.** Many episodes never reach the attack:
the agent does not open the SMS or invoice, or cannot do the task at all.
Counted only where the agent read the attack and completed the attack-free
version of the same task, attack success without a defence was 24.1%
(7 of 29) for 3B, 10.8% (13/120) for 7B, 14.9% (11/74) for 14B, 17.8%
(23/129) for 32B, 9.8% (4/41) for Hermes 3 and 20.4% (29/142) for
GPT-OSS-120B: two to four times the overall rate for the smaller models,
and close to it for the two models that can do most tasks. A bigger model
was not safer: within one family, Qwen2.5-32B did the most normal tasks
(66% without a defence) and fell for the most attacks (14.5%, about twice
the smaller models; exact McNemar tests on the same 220 attacks against 3B,
7B and 14B: p = 0.017, 0.004, 0.008).

### 5.3 Amount-only attacks need their own check

Fig. 3 splits successful attacks into those that redirect money or leak
the OTP (G1, G2) and amount-only attacks (G3), per model and defence.
Because the rules are deterministic, which attacks they can stop follows
from the design: the attacker's numbers are never trusted, so recipient
provenance stops every redirect; amount-only attacks pay a trusted payee, so
only the amount check sees them. Replaying the 116 successful attacks of the
six no-defence runs through the rules confirms this (89 redirects blocked by
`provenance`, the 27 amount-only ones allowed; all 116 blocked with the
amount check). What the runs add is how often models attempt each kind and
what the checks cost in completed tasks.

**Recipient provenance stops redirection, not inflation.** With
`provenance`, no attack that sends money to a new number or leaks the OTP
succeeded on any model (0 of 800 such attack episodes on the four Qwen
models). Every attack that got past it was amount-only: 15 on the Qwen
models, 1 on Hermes 3 (a Bangla note inflating the rent) and 7 on
GPT-OSS-120B. Without a defence, amount-only attacks were the most
successful kind for the Qwen models: 2, 4, 7 and 7 of 20, against 14, 9,
10 and 25 of the other 200 attacks; GPT-OSS-120B: 5 of 20 and 28 of 200.
A typical one is a "correction" in a school invoice that raises the fee
from 3,500 to 5,000 Tk: the money reaches the real school, so a metric that
checks only whether the attacker was paid scores it as safe.

**The amount check closes the gap.** With `provenance-amount`, **no attack
succeeded on any model**: 0 of 880 attack episodes on the Qwen models, 0 of
220 for Hermes 3 and 0 of 220 for GPT-OSS-120B. It blocked no correct
payment in the normal tasks (by design: an agent that pays correctly is
never blocked, since every normal task's payee is trusted), and it also
stopped every wrong payment
without an attacker: wrong payments that went through fell from 33, 8, 29,
20, 10 and 1 (no defence) and 30, 6, 27, 2, 9 and 1 (`provenance`) to 0 for
every model. The other models lost at most 3 normal tasks with a defence
(Table 2); Qwen2.5-32B lost 12, for a reason discussed in Section 5.5. No model leaked the
OTP in any run (0 of 25 attempts per run, all one attack text). The amount
check has a limit the runs did not hit: it accepts any amount in the
payee's own message, so it cannot tell a total (1,800 Tk) from a share
(600 Tk) in the same SMS. Even where the agent read the
attack and could do the task, `provenance-amount` let none through (for
example 0 of 118 for Qwen2.5-7B, interval 0% to 3%; 0 of 150 for
GPT-OSS-120B).

**What the rules cost when the payee is new.** The zero above is a property
of the main set, whose normal payees are all trusted. On the 24
message-payee tasks (Section 3.3), where the user asks to pay someone whose
number is written only in an SMS or an invoice, a scripted agent that pays
exactly right is blocked on **all 24** by every provenance variant, and
the simulated user's "yes" does not unblock it: neither the rules nor our
harness give the user a way to approve a new payee. When the user's request
also gives the number, `provenance` allows all 24, but `provenance-amount`
and `provenance-consistent` still block 12: the payments whose amount came
from someone other than the payee (Ammu naming the pharmacy's price, the
landlord the caretaker's charge, the courier company the rider's fee).
Provenance therefore does not make such payments safe; it hands every
payment to a new number back to the user, and the amount check needs the
amount from the user or the payee as well.

The five open models show what this costs in practice. Without a defence
they did 6, 5, 10, 19 and 4 of the 24 tasks (Qwen2.5 3B, 7B, 14B, 32B,
Hermes 3; 44 of 120); with either provenance defence they did none. They
tried the correct payment about as often as before (42 times with
`provenance-amount`, 43 with `provenance`), and every attempt was blocked.
What the agent then told the user varied, and it matters as much as the
block. Qwen2.5-32B usually explained that the payee was not a saved
contact and asked the user to approve or save them, giving the number in
11 of its 24 last messages. **Qwen2.5-14B told the user the money had
been sent, when nothing had been, in 8 of its 18 blocked episodes** (6
with `provenance`), twice adding that it had saved the payee as a contact,
which no tool can do; Qwen2.5-7B did so once ("Transaction initiated
successfully"). A user who believes the electrician was paid will not pay
him another way, so a block the agent hides can be worse than no defence
for the user, and neither "tasks done" nor a scripted audit shows it. With
the recipient check alone, Qwen2.5-7B also routed two of these payments to
Dhaka Power's registered biller account, which the rule trusts, and
reported one as paid to the flat society; the amount check blocked both.
Over all 15 runs, every number the agents copied with a digit missing or
extra was written in Bangla digits in the message (20 of the 120 episodes
whose message used Bangla digits, against 0 of 120 with ASCII digits); the
Bangla and English versions of each message differ in more than the
digits, so this cannot isolate them. Without a defence, such slips cost
Qwen2.5-32B 3 of its 5 failures. [GPT-OSS-120B
on this set: to add.]

### 5.4 Adaptive attacks: scripted audits are not enough

`provenance-amount` trusts an amount that comes from the payee itself. The
adaptive set (56 cases, Section 3.3) forges exactly that. We first ran it
with scripted agents, which measure what a defence can stop independently
of how often a model obeys (Table 4, top). An agent that obeys every attack
beats `provenance-amount` with every forged amount (16 of 16 SMS, 24 of 24
invoices), while a forged SMS giving a new number to pay still fails (0 of
16): the recipient check holds even against a spoofed sender, but the
amount check is only as strong as the payee's identity.
`provenance-consistent` stops all 40 forged amounts by asking the user, at
the price that in those 40 cases the correct payment also waits for the
user.

**Table 4.** Adaptive attacks that succeed. Top: scripted agent that obeys
every attack. Bottom: Qwen2.5-32B.

| Adaptive attack | none | provenance | provenance-amount | consistent (first) | consistent (fixed) |
|---|---:|---:|---:|---:|---:|
| *Scripted*: forged amount, SMS | 16/16 | 16/16 | 16/16 | | 0/16 |
| *Scripted*: new number, SMS | 16/16 | 0/16 | 0/16 | | 0/16 |
| *Scripted*: forged revised invoice | 24/24 | 24/24 | 24/24 | | 0/24 |
| *Qwen2.5-32B*: forged amount, SMS | 11/16 | | 10/16 | 3/16 | **0/16** |
| *Qwen2.5-32B*: new number, SMS | 8/16 | | 0/16 | 0/16 | **0/16** |
| *Qwen2.5-32B*: forged revised invoice | 1/24 | | 1/24 | 0/24 | **0/24** |
| *Qwen2.5-32B*: correct payment made (of 56) | 11 | | 12 | 2 | 1 |

**The real model found a gap the script missed.** With Qwen2.5-32B, a
forged "correction" from the payee's number worked very well: 11 of 16
without a defence and 10 of 16 with `provenance-amount`, against 14.5% on
the main set. Forged invoices rarely worked (1 of 24): the model opened an
invoice in 13 of 24 cases, but the forged "revised" one in only 2. The
first version of `provenance-consistent` cut forged amounts to 3 of 16, not
0. In all 3, the model called `read_sms` with `limit: 1`, saw only the
newest (forged) message, and paid it; that version compared only messages
the agent had read, so it never saw the real amount. The scripted agent
always read every message, so the audit had reported 0. Replaying the
attack with a scripted agent that reads only the newest SMS (or only the
forged invoice) reproduces the gap: 40 of 40 against the first version.

The fixed version compares every SMS and invoice from the payee in the
wallet, read or not. It stops all 40 in the newest-only audit and, in a
rerun on Qwen2.5-32B, all 56 adaptive attacks; the model again read only
the newest SMS in 5 of the 16 forged-amount cases, and all 5 were stopped.
On the main cases it lets 0 of 220 attacks through, blocks no correct
payment and completes 59 of 82 normal tasks (72%). The cost is real but
limited to disagreement: the correct payment went through in only 1 of the
56 adaptive cases (12 with `provenance-amount`), because when the payee's
messages disagree, the payment waits for the user. A defence must be
audited against how real agents use tools, not only against an ideal
script.

### 5.5 Harness choices change the scores

**The wording of a block.** With either defence, Qwen2.5-32B completed 12
fewer normal tasks (42 of 82, against 54 without a defence). These were not
false blocks: in all 12 the model first passed the invoice ID as the biller
account. Without a defence the wallet answers "not a registered biller
account. Check the invoice for the correct account", and the model reads
the invoice and pays. With a defence the same call is blocked first, and
the block message says "Ask the user for explicit approval before
retrying"; the model asks, retries the same call and gives up. With the
revised message ("Use the biller account number written on the invoice, or
one from list_billers", Section 4.5) all 12 came back: 57 of 82 with
`provenance-amount` (70%), 58 with the first and 59 with the fixed
`provenance-consistent`, slightly more than without any defence, still with
0 attacks and 0 correct payments blocked. The smaller models lost at most 3
normal tasks with a defence. How a defence explains a block mattered as
much as when it blocked.

**The simulated user.** The simulated user answers "yes" to any reply that
contains a "?" (Section 3.2). Without a defence, in 29 of the 78 successful
attacks on the four Qwen models (13 of 32 for Qwen2.5-32B; Hermes 3: 1 of
5), the agent had asked a question and received that "yes", and the
attacker was paid later in the same episode. This is an order in time, not
evidence that the question caused the payment, but it means that how real
users answer is part of the attack path that the benchmark does not test.
The rule also reacts to the character alone: GPT-OSS-120B asked a question
in only 1 of 302 episodes without a defence, and that "?" was in a table
header ("Action Needed?"). The user had asked it to read the SMS and send
no money; after the automatic "yes" it paid a real 1,200 Tk bill. This
single case is GPT-OSS-120B's only wrong payment that went through, with
no defence and with `provenance`; `provenance-amount` blocked it. The
opposite also happens: Hermes 3 often wrote "Please confirm ..." without a
"?" (about 9 of its 64 failed normal tasks), which the simulated user does
not answer.

**Defences change how often agents ask.** With a defence on, the Qwen
models asked more often (Qwen2.5-7B in 88 of 302 episodes without a
defence, 153 and 158 with one). Whether an agent asks after a block depends
on the model and on the block message: Qwen2.5-7B asked in 73% and 72% of
the episodes with a block, Qwen2.5-32B in 78% and 77% with the old message
and 42% with the new one, Qwen2.5-3B in 9% and 10%, GPT-OSS-120B in 74%
and 78%, Hermes 3 in 1 of 25 and 1 of 34.

**What the questions told the user.** We coded every question that
received the simulated yes with keyword rules (payee, amount, where the
request came from, risk, next step). None of the 35 questions after which
an attacker was paid (all runs, main cases) warned of a risk; most read like
an ordinary payment confirmation (31 named a payee and 31 gave an amount).
For attacks that redirect money, 14 of 22 such questions showed the
attacker's number, relaying its instruction as a normal step ("a new
compliance rule requiring a verification transfer of 1500 Taka to
01877777777 ... Would you like to proceed?"); the other 8 asked about
something else, such as the real bill. Across all 2,022 questions only 38
(2%) contained a risk word. How real users would answer is future work.

### 5.6 Language

Table 3 lists successful attacks by attack language without a defence. No
model fell most for Bangla script. Qwen2.5-3B, 14B and 32B fell mostly for
English (10, 13 and 14 of 55 English attacks; permutation tests of the
language effect p = 0.002, < 0.001 and 0.03). For Qwen2.5-7B and Hermes 3
the differences between languages are not distinguishable from chance
(p = 0.22 and 0.35), and GPT-OSS-120B fell for all four about equally
(English 8 of 55, Bangla 8 of 56, Banglish 9 of 55, mixed 8 of 54; p = 0.99).

**The comprehension gate.** The language effect tracks how well each model
handles the language at all. Qwen2.5-32B completed 18 of 21 normal tasks
requested in English but 9 of 22 requested in Bangla, and among attacks it
read it followed 14 of 49 English and 3 of 45 Bangla ones; Qwen2.5-14B and
Hermes 3 show the same pattern. GPT-OSS-120B completed 20 of 21 English and
21 of 22 Bangla requests, and followed English and Bangla attacks equally
often (8 of 41, 8 of 46). This is a correlation across six models, not a
controlled test, but it runs opposite to the multilingual jailbreak finding
that low-resource languages weaken safety [8, 9]: here, a low-resource
language protected the agent only while the agent was weak in it, which
suggests the protection disappears as models improve, while none of the
detectors in Section 5.1 both catches the attacks and lets normal Bangla
messages through. It also exposes a usability
gap: Bangla requests were completed far less often by the open models.

### 5.7 Reproducibility

The first 114 cases of the 302-case set reproduce an earlier run with three
repeats: attack success without a defence 10.0%, 3.8% and 6.2% for Qwen2.5
3B, 7B and 14B, against 10.0%, 3.8% and 5.0% then; in that run, the three
repeats of a case gave the same outcome in 96% to 100% of cases. Every
available episode (9,524) was re-scored from its raw trace with the
current scorer, with no difference from the saved scores, and every
recorded defence decision was replayed through the current rules: 14,057
of 14,062 match, the five exceptions being two harmless SMS that an earlier
version of the OTP rule blocked and three calls from the first version of
`provenance-consistent`. Raw traces, scores and the scripts that produce
every table are public.

---

## Sources of every number in this draft

| Number | Source |
|---|---|
| Detector rates, false alarms, filter cost, ProtectAI's interval and examples | README, "Do injection detectors work"; `docs/audit.md`, "Detectors" |
| Prompt Guard 2 and gpt-oss-safeguard: rates, highest scores, AUROC, false-alarm texts, misses, the empty reply | README, "Do injection detectors work"; `results_detectors_api/summary.md` and `raw.jsonl` on the `groq-results` branch (`scripts/detector_api.py`); the 0.999 test-text score is from the log of the Groq detector workflow run of 22 October 2026 |
| Main results per model and defence (attack success, intervals, normal tasks, invented payees, wrong payments through) | README, "Results", "The largest model", "A second model family", "A larger API model"; `docs/paper/figures/table1_main.md` |
| Wrong biller account, invoice ID 14 of 15, GPT-OSS-120B's 6 failures | README, "Why normal tasks fail" |
| Conditional rates | README, "Attack success among agents that could have been fooled" |
| Amount-only counts, 0 of 800, the school fee example | README, "Results"; `table1_main.md` (Hermes 3 and GPT-OSS-120B amount-only counts) |
| OTP leaks | `docs/audit.md`, items checked from the raw traces |
| Adaptive results (scripted and Qwen2.5-32B) | README, "Adaptive attacks" |
| Message-payee set: 24 of 24 blocked, 0 and 12 of 24 with the number typed | README, "What the defence results show"; `scripts/audit_message_payee.py` |
| Message-payee model runs: 6 / 5 / 10 / 19 / 4 done, 0 with a defence, 42 / 43 tried, 8 and 6 of 18 said sent, 11 of 24 gave the number, two biller payments, 20 of 120 vs 0 of 120 digit slips, 3 of 5 for 32B | README, "Paying someone named only in a message"; `scripts/audit_message_payee.py --runs` on `kaggle-results` `2026-10-23_message_payee/`; `docs/audit.md`, "Message-payee run" |
| Block message: 12 tasks, 42 / 54 / 57 / 58 / 59 of 82 | README, "The largest model"; `docs/audit.md` |
| 29 of 78, 13 of 32, 1 of 5; questions and asks after a block | `docs/paper/confirmations.md` |
| What the questions told the user: 35, 31, 14 of 22, 8, 38 of 2,022 | `docs/paper/question_coding.md` (keyword coding; hand check pending) |
| Table-header "?" case | `docs/audit.md`, item 2; README, "A larger API model" |
| Hermes 3 "confirm" without a "?" (about 9 of 64) | README, "Why normal tasks fail" (keyword estimate) |
| Attacks by language and vector | README, "Results" and "A larger API model"; `table2_language.md` |
| Reproduction of the 114 cases, 96% to 100%, 9,524 episodes re-scored | README, "Results" and "Earlier run"; `docs/audit.md` |
| Template counts and template-level intervals, permutation and McNemar p-values, comprehension-gate table | `docs/paper/robustness.md` (`scripts/robustness.py`) |
| Replay of 116 successful attacks through the rules; 14,057 of 14,062 decisions | `docs/audit.md`, "Design review"; `scripts/verify_decisions.py` |
| Keyword cues in attack texts (11 of 17); ideal agent never blocked | `docs/audit.md`, "Design review" |

## Notes for the next draft

- Length: about 2,700 words with Table 4. If space is short, shorten 5.4
  (keep the table and the `limit: 1` finding) and move the "asks after a
  block" paragraph of 5.5 to an appendix.
- Hermes 3's "about 9" uses a keyword estimate; say so in a footnote or
  drop the number.
- Section 6 of the outline (reproducibility) is folded into 5.7 here.
- Check that Fig. 1 to 3 and Tables 2 and 3 are regenerated from the same
  runs before the final version (see the outline).
