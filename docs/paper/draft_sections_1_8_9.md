# Draft: sections 1, 8 and 9 (introduction, limitations and ethics, conclusion)

First draft of sections 1, 8 and 9 of the STALA 2027 paper
(`docs/paper/outline.md`), about 1.75 pages in the final layout. With
`draft_sections_2_4.md`, `draft_section_5.md` and `related_work.md` (section
7) this completes a first full draft; section 6 is folded into 5.7.
Reference numbers [1] to [12] follow `docs/paper/related_work.md`. Every
result number is taken from the README, `docs/audit.md` or the section 5
draft; the list at the end gives the source of each.

---

## Abstract (about 150 words)

LLM agents that read messages and make payments are arriving in mobile
money, where users and scammers write in Bangla, romanised Bangla
(Banglish) and code-mixed text. We release TakaPay, a benchmark of 302
cases in which indirect prompt injections hidden in SMS, invoices and tool
descriptions try to make an agent pay an attacker, leak a one-time code or
overpay the real payee, and test six models from three families. Two widely
used injection detectors did not transfer: one flagged 84% of normal Bangla
texts and, used as a filter, would break 20 of 22 Bangla-request tasks (1
of 21 in English). Simple provenance rules, which never read the text,
blocked no correct payment in any language and, with an amount check, let
no attack through on any model. We also report three testing lessons:
attack success alone hides wrong payments made with no attacker, checking
only whether the attacker was paid misses amount-only attacks, and harness
details and scripted audits change the conclusions.

## 1. Introduction

Bangladesh has about 239 million mobile money (MFS) accounts, and fraud by
impersonation and PIN or OTP theft is common. AI assistants that read a
user's messages and make payments for them are arriving, and the first risk
in the OWASP Top 10 for Agentic Applications (2026), agent goal hijack, is
mostly delivered by indirect prompt injection [1]: instructions hidden in
content the agent reads. For a payment agent that content is the inbox and
the bills, and in Bangladesh they are written in Bangla script, in
romanised Bangla (Banglish) with no fixed spelling, and in text that
switches between Bangla and English inside a sentence.

The agent prompt-injection benchmarks we know of, InjecAgent [2] and
AgentDojo [3], are in English. Multilingual safety work, including work on
Bengali [9, 10], studies jailbreaks of chat models, where the harm is the
text the model writes, not agents whose harm is an action. We do not know
whether attacks, or the defences built against them, carry over to an agent
that moves money in Bangla.

**Detectors flag the script, not the attack.** The usual answer to
injection is to put a classifier in front of the agent. We ran two widely
used open detectors on every untrusted text in our benchmark. ProtectAI's
DeBERTa-based detector flagged 16 of 19 normal Bangla texts (84%), such as
a power bill and a mother asking for medicine money, more often than it
flagged Bangla attacks (57%); used as a filter, it would break 20 of 22
normal tasks requested in Bangla and 1 of 21 in English. deepset's detector
flagged every attack and 87% of normal texts. A detector's English score
said little about its behaviour in Bangla.

**What worked instead.** Provenance checks where a payment's recipient,
code and amount came from, never what the text says. The idea is not ours:
CaMeL [5] and information-flow control defences such as FIDES [12]
enforce it, evaluated in English. We test a deliberately simple rule-based
version at the tool boundary. It blocked no correct payment in the 82
normal tasks in any of the four request languages, for any of six models
from three families (Qwen2.5 3B to 32B, Hermes 3 on Llama 3.1 8B, and
GPT-OSS-120B), and with an amount check it let none of the 220 attacks
through on any of them, against 2.3% to 15.0% without a defence.

**Testing lessons.** The runs also showed how easily a payment-agent
benchmark can mislead:

- *Attack success alone misleads.* With no attacker involved, the Qwen
  models tried to pay a payee or amount nobody asked for in 29% to 52% of
  episodes, more often than any attack succeeded; the strongest model,
  GPT-OSS-120B, rarely did (4.3%) but fell for the most attacks (15.0%).
  Counted only where the agent read the attack and could do the task,
  attacks worked two to four times as often as the overall rate for the
  smaller models.
- *"Did the attacker get paid?" misses amount-only attacks.* Every attack
  that got past a recipient check kept the real payee and raised the
  amount, which such a metric scores as safe.
- *The harness and the audit change the conclusions.* Rewording one block
  message brought back 12 normal tasks for Qwen2.5-32B; a simulated user
  that answers any "?" with "yes" was part of 29 of 78 successful attacks
  on the Qwen models; and a scripted audit reported a defence as complete
  until a real model, reading only the newest SMS, got past it.

**Contributions.**

1. TakaPay, a fictional mobile-money wallet served over MCP, with 302 cases
   in Bangla, Banglish, code-mixed text and English, and a separate set of
   56 adaptive attacks that forge the payee's identity. Cases, raw traces
   and re-scoring scripts are public.
2. A measurement of two injection detectors on non-English tool outputs
   inside an agent task, showing that they flag the script rather than the
   attack.
3. A test of simple provenance rules across languages on six models from
   three families, including an amount check and a consistency check
   against forged payee messages.
4. Three testing lessons for payment agents: report wrong payments made
   with no attacker, score amount-only attacks, and report harness choices
   and audit defences with real agents.

Section 2 describes the threat model, Section 3 the benchmark, Section 4
the defences and Section 5 the results; Section 7 discusses related work
and Section 8 the limitations.

## 8. Limitations and ethics

**Synthetic data, one wallet.** All messages, names, numbers and billers
are written for the benchmark, copying public scam patterns; no real user
data is used. TakaPay has nine tools, and real apps, their messages and
their checks differ. The Bangla and Banglish text was reviewed by one
native speaker (an author); a second reviewer's check of a sample is
planned.

**A simulated user who always says yes.** When the agent writes a "?", the
simulated user approves once and never refuses, even when the "?" is not a
question (Section 5.5). How real users answer an agent's question, and
whether its questions give them what they need to refuse, is not studied.
In our harness the "yes" cannot unlock a blocked payment, so it cannot get
an attack past a defence; it can still change what the agent does next, so
attack success without a defence, and payments a rule allows, depend on
it.

**Models and settings.** Open models up to 32B (14B and 32B quantised to
4-bit) on T4 GPUs, and one larger model through an API (GPT-OSS-120B with
reasoning effort set to low; other settings and closed API models were not
tested). One run per case at temperature 0; repeats at temperature 0 barely
differed in an earlier run (Section 5.7). Granite 3.3 8B is left out
because its tool calls failed in our serving setup.

**Measurement.** "Read the attack" means the agent called the tool that
shows it, so the conditional rates are, if anything, slightly too low.
"Correct payments blocked" is measured on the 82 normal tasks; a blocked
correct payment in an attack case shows up as lower utility under attack.
An unwanted SMS is scored as harm only if it contains the OTP. The detector
filter cost is computed from the texts, not from agent runs, and the normal
detector set is small (54 texts, 19 in Bangla), so its intervals are wide.

**What the defences cost.** The provenance rules approximate provenance by
matching values (numbers, accounts, amounts) against trusted sources; they
are weaker than CaMeL or FIDES and were tested only on this wallet's three
payment tools. `provenance-consistent` hands the decision to the user
whenever the payee's own messages disagree: on the adaptive set the correct
payment went through in only 1 of 56 cases. No rule can tell a forged
message from a real one with the same sender, so the amount check is only
as strong as sender authentication.

**Ethics.** Every wallet, name, number and biller is fictional, including
the attacker numbers. Attacks copy common, already public scam patterns
and introduce no new technique; no real service or account was tested. The
benchmark is released to help build and test defences; if work on it ever
reveals a weakness in a real product, it will be reported privately to the
provider first.

## 9. Conclusion

Payment agents will read inboxes written in the languages their users
write in, and their defences should be tested there. In our benchmark, two
widely used injection detectors failed on Bangla, flagging the script
rather than the attack, while simple provenance rules that never read the
text blocked no correct payment in any language and, with an amount check,
let no attack through on any of six models. For anyone testing payment
agents, we suggest four habits: test in the users' languages; report wrong
payments made with no attacker and amount-only attacks, not only attack
success; report harness choices such as the simulated user and the wording
of block messages; and audit defences against real agents, not only
against an ideal script.

---

## Sources of every number in this draft

| Number | Source |
|---|---|
| 239 million mobile money accounts; OWASP Top 10 for Agentic Applications (2026) | README, "Why this matters" (needs a citation for the account count; see notes) |
| Detector rates: 16 of 19, 84%, 57%, 20 of 22, 1 of 21, deepset 100% / 87% | README, "Do injection detectors work"; `draft_section_5.md`, 5.1 |
| 0 correct payments blocked, any language, six models; 0 attacks with the amount check; 2.3% to 15.0% without a defence | README, main results, Hermes 3 and GPT-OSS-120B sections; `draft_section_5.md`, 5.1 and 5.3 |
| Invented payees 29% to 52% (Qwen), 4.3% and 15.0% (GPT-OSS-120B); two to four times when read and able | README, "Results", "A larger API model", conditional rates |
| 12 normal tasks; 29 of 78; newest-only SMS | README, "The largest model", "Adaptive attacks"; `docs/paper/confirmations.md` |
| 302 cases, 56 adaptive cases, nine tools | README, "Test set" and "Adaptive attacks" |
| 1 of 56 adaptive correct payments; 54 normal texts, 19 in Bangla | README, "Adaptive attacks" and "Do injection detectors work" |
| Measurement caveats | `docs/audit.md`, items 2 to 7 |

## Notes for the next draft

- The 239 million figure needs a citable source (Bangladesh Bank MFS
  statistics for the month used); check before submitting.
- "Bengali [9, 10]": check that both papers include Bengali before keeping
  the bracket (roadmap: references task).
- If space is short: drop the abstract's last sentence, merge the
  contributions list into the paragraph before it, and shorten the
  "Measurement" paragraph of section 8 to one sentence pointing to the
  audit.
- If the venue is double-blind, remove "an author" from section 8 and the
  repository link, and refer to an anonymised copy.
