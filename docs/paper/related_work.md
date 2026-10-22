# Related work: STALA paper, section 7

Draft of section 7 of `docs/paper/outline.md` (about half a page in the
paper). The first part is text ready to adapt into LaTeX; the second part
is a comparison table and the full references, with a note on how each one
was checked.

Rules for this file:

- Only real papers, with the facts we state about them taken from their
  abstracts or published pages (checked 7 October 2026; see "References").
  If a later version of a paper changes a number, use the later one.
- Our own numbers come from the README, as in the outline. This section
  needs almost none.
- "To our knowledge" claims (nothing else does X) rest on the papers below
  and a search in October 2026, not a full survey. Search again in
  November before submitting.

---

## Draft text

**Agent prompt-injection benchmarks.** Indirect prompt injection, where
instructions hidden in data an LLM reads take over the application, was
named and demonstrated by Greshake et al. [1]. InjecAgent [2] turned it into
a benchmark for tool-using agents: 1,054 cases over 17 user tools and 62
attacker tools, with direct-harm and data-stealing goals; ReAct-prompted
GPT-4 was fooled 24% of the time. Each case is a single turn in which the
attacker text is handed to the model as a tool output. AgentDojo [3] made
the setting dynamic and stateful: 97 tasks and 629 security cases across
four suites (workspace, Slack, travel and an e-banking suite), scored by
checks on the environment state rather than by an LLM judge, and showed
that models fail many tasks even without an attack. Agent Security Bench
[4] widened the range of attacks and defences. Closer to our domain,
FinVault [16] tests financial agents in sandboxed, execution-grounded
scenarios and also scores state changes rather than text, and MCPTox [19]
poisons the tool descriptions of real MCP servers, finding that more capable
models are often more susceptible, as our strongest model was to the one
tool-description template (section 5.2). Our harness follows
AgentDojo's design (a real tool environment, state-based scoring, utility
measured next to attack success), but all of these benchmarks are in
English, and their banking tasks are about Western bank transfers. TakaPay
targets mobile money as used in Bangladesh: phone-number recipients, bill
payment to registered billers, OTPs, and SMS as the main untrusted channel,
with attacks and requests in Bangla, Banglish, code-mixed and English text.

**Defences by design.** CaMeL [5] separates control flow (planned from the
trusted user query) from data flow (untrusted tool outputs), tracks where
every value came from, and enforces capability policies before a tool runs;
it solves 77% of AgentDojo tasks with provable security, against 84% with
no defence. FIDES [12] tracks integrity and confidentiality labels on
data with information-flow control and enforces policies on consequential
actions. Our provenance defences apply the same idea in a much simpler
form: a payment is checked against where its recipient, code and amount
came from (the user's request, the wallet's own records, or the payee),
with no change to the agent and no second model. Because the check never
reads the untrusted text, it does not depend on the language of that text,
which is the property our detector results (section 5.1) show matters.
Deterministic checks before a payment are also the idea behind the Open
Agent Passport [18], evaluated in APort Vault [17] on attacks written in a
public capture-the-flag against a live payment agent: an allowlist-style
authorization layer let no unpermitted transfer through. Those evaluations
are in English and check who may be paid; we test the same class of check
in four language forms and add the amount and consistency checks.
CaMeL's and FIDES's evaluations are in English; we add evidence that this class of
defence carries over to other languages and scripts, and two
payment-specific findings: recipient provenance alone misses attacks that
change only the amount, and a forged message that claims to come from the
payee needs a consistency check across all of the payee's messages
(section 5.4).

**Filters and firewalls.** The other main defence family inspects text.
Bhagwatkar et al. [6] put two LLM-based firewalls at the agent-tool
boundary, a tool-input minimizer and a tool-output sanitizer, and report
the lowest possible attack success on AgentDojo, Agent Security Bench,
InjecAgent and tau-Bench. They also argue that these benchmarks are too
weak (flawed metrics, implementation bugs, weak attacks) and propose fixes.
We agree that benchmark details change conclusions (section 5.5: one block
message cost Qwen2.5-32B 12 normal tasks), and we add a dimension their
evaluation does not cover: language. Off-the-shelf injection classifiers
are trained on English (ProtectAI's model card [7] says the model does not
handle non-English prompts); we measure what that costs in practice and
find the detector reacts to Bengali script itself (section 5.1). Newer
guards are multilingual or policy-driven: Meta's Prompt Guard 2, part of
LlamaFirewall [23], targets explicit jailbreak techniques and dropped its
predecessor's broader injection label, and gpt-oss-safeguard [24] classifies
text against a policy written at run time. We test both (section 5.1): the
first misses our attacks, which contain no override phrasing; the second,
with a policy we wrote for these attacks, catches most of them in every
language but also flags real family payment requests. This
matches two known problems: guard models over-flag harmless text that
contains trigger words (InjecGuard's NotInject set [20]), and guardrails
lose accuracy on multilingual and code-switched input [21]. For Bangla
specifically, MIPIAD [14] trains a cross-lingual injection detector on
machine-translated BIPIA templates in English and Bangla; it studies
detection only, on translated text without Banglish or code-mixing, and
does not run agents. Whether
an LLM sanitizer such as [6]'s keeps its accuracy on Bangla and Banglish
tool outputs is open; our benchmark can test it (planned, see
"Ideas not yet scheduled" in the roadmap).

**Multilingual jailbreaks.** A line of work shows that LLM safety training
transfers poorly to low-resource languages. Yong et al. [8] translated
harmful English prompts into low-resource languages and got actionable
answers from GPT-4 79% of the time on AdvBench. Deng et al. [9] built
MultiJail with native-speaker translations into nine languages, including
Bengali as one of three low-resource languages, and found about three
times as much unsafe output in low-resource languages. Wang et al. [10]
(XSafety, 10 languages including Bengali) found that every model they
tested gave significantly more unsafe answers to non-English queries than
to English ones. BanglaSafe [13], a Bengali benchmark of 879 prompts over
17 culturally grounded harm categories, found that the register of a
request (for example a formal newspaper framing) changed safety more than
the switch from English to Bengali. Yoo et al. [11] showed that code-switched
queries, which mix languages inside one prompt as real users do, draw out
more unsafe behaviour than English ones. Closest to our language setting, a
case study of indirect prompt injection in English, Tamil and Tanglish
(romanised Tamil) [15] tests one model on eight scenarios and asks whether
visible reasoning helps monitoring. BabelArena [22] shows that agents make
more tool-use errors in lower-resource languages, which we also see as a
utility gap in Bangla (section 5.6). All of these study a user who
attacks a chat model directly (jailbreaks: the harm is the text the model
writes). We study a third party who attacks an agent through the data it
reads (indirect injection: the harm is an action, a payment), with
Banglish written in Latin script and code-mixed text as first-class attack
languages, not translations. Our results also differ in direction: the
jailbreak finding (low-resource language, weaker safety) did not carry
over, and our data suggest why: the models that followed Bangla attacks
least also handled Bangla requests worst, while the model that handled all
four languages followed attacks equally in all four (the "comprehension
gate", section 5.6). Three of our six models fell significantly more often
for English attacks; for the other three no language effect was
distinguishable from chance, and GPT-OSS-120B fell about equally for all
four (Banglish 9, the others 8 of about 55). For none was Bangla script the
most successful attack language (section 5.6).

**What is new here.** We do not claim the provenance idea; it comes from
CaMeL [5] and information-flow control defences such as FIDES [12]. What we
add, as far as we know from the papers above (not a full survey):

1. An agent prompt-injection benchmark in a low-resource language
   (MIPIAD [14] covers Bangla detection on translated text; the Tamil study
   [15] covers one model and eight scenarios),
   with Bangla, Banglish (romanised) and code-mixed attacks and user
   requests, native-speaker reviewed, on tools that move money.
2. A measurement of five injection detectors on non-English tool outputs
   inside an agent task: the English-trained ones flagged the script, not
   the attack; the multilingual Prompt Guard 2 missed every attack; a
   policy model caught most attacks but flagged real payment requests and
   missed amount-only changes (section 5.1).
3. A test of simple provenance rules (the idea behind CaMeL) across
   languages: no correct payment blocked in the normal tasks in any request
   language, on six models from three families.
4. Payment-specific testing lessons: amount-only attacks that pay the real
   payee, wrong payments with no attacker involved, and forged payee
   messages that need a consistency check, which a scripted audit missed
   and a real model found.

---

## Comparison at a glance

Facts about other work from the references below; ours from the README.

| Work | Kind | Attack channel | Languages | Actions | Scoring | Defences studied |
|---|---|---|---|---|---|---|
| Greshake et al. [1] | Attack demos | Web pages, documents, email | English | Various apps | Case studies | None (taxonomy) |
| InjecAgent [2] | Benchmark | One injected tool output | English | 17 user tools, 62 attacker tools | Single turn | Prompting variants |
| AgentDojo [3] | Benchmark | Data inside tool outputs | English | 4 suites incl. e-banking | Environment state | Several, from the literature |
| CaMeL [5] | Defence | (uses AgentDojo) | English | AgentDojo tools | Environment state | Control/data flow + capabilities |
| FIDES [12] | Defence | (uses AgentDojo) | English | AgentDojo tools | Environment state | Information-flow labels + policies |
| Firewalls [6] | Defence + benchmark critique | Tool inputs and outputs | English | 4 benchmarks | The benchmarks' own | LLM minimizer and sanitizer |
| Multilingual jailbreaks [8-11] | Attacks on chat models | User prompt (direct) | Many, incl. Bengali [9, 10] | None (text only) | Harmful text | Mostly safety tuning or prompting |
| MIPIAD [14] | Detector | Translated BIPIA texts | English, Bangla (machine-translated) | None (detection only) | Classification | Fine-tuned Qwen classifier + TF-IDF ensemble |
| LlamaFirewall [23] | Guardrail system | User input, agent reasoning, code | Mainly English; Prompt Guard 2 86M multilingual | AgentDojo (to check) | Detection and attack success | Prompt Guard 2, AlignmentCheck, CodeShield |
| Tamil/Tanglish study [15] | Case study | Injected content | English, Tamil, Tanglish | One model, 8 scenarios | Manual | Visible reasoning as a monitor |
| FinVault [16] | Benchmark | Several, incl. prompt injection | (not checked) | Financial agents, sandboxed | Environment state | Existing defences |
| APort Vault [17] | Benchmark (CTF replay) | User-written attacks on a live payment agent | English | Payment agent | Transfers made | Deterministic authorization layer |
| MCPTox [19] | Benchmark | Poisoned MCP tool descriptions | English | 45+ real MCP servers | Action taken | (Measurement) |
| **This work** | Benchmark + defences | SMS, invoices, tool descriptions | Bangla, Banglish, code-mixed, English | Mobile-money wallet over MCP (9 tools) | Environment state | Keyword, 4 detectors, 3 provenance variants |

---

## References

Checked on 7 October 2026 from arXiv listings, conference pages and
author pages (abstracts were read through search results, not from the
PDFs); venues, author lists and Bengali coverage rechecked on 17 October
2026. BibTeX for all of them, plus OWASP and the Bangladesh Bank figure,
is in `docs/paper/references.bib` (written by hand; compare with each
paper's official BibTeX before submitting).

1. Kai Greshake, Sahar Abdelnabi, Shailesh Mishra, Christoph Endres,
   Thorsten Holz, Mario Fritz. *Not what you've signed up for: Compromising
   Real-World LLM-Integrated Applications with Indirect Prompt Injection.*
   ACM Workshop on Artificial Intelligence and Security (AISec) 2023,
   pp. 79-90. arXiv:2302.12173.
2. Qiusi Zhan, Zhixiang Liang, Zifan Ying, Daniel Kang. *InjecAgent:
   Benchmarking Indirect Prompt Injections in Tool-Integrated Large
   Language Model Agents.* Findings of ACL 2024, pp. 10471-10506.
   arXiv:2403.02691.
3. Edoardo Debenedetti, Jie Zhang, Mislav Balunović, Luca Beurer-Kellner,
   Marc Fischer, Florian Tramèr. *AgentDojo: A Dynamic Environment to
   Evaluate Prompt Injection Attacks and Defenses for LLM Agents.* NeurIPS
   2024 Datasets and Benchmarks Track. arXiv:2406.13352.
4. Hanrong Zhang et al. *Agent Security Bench (ASB): Formalizing and
   Benchmarking Attacks and Defenses in LLM-based Agents.* ICLR 2025.
   arXiv:2410.02644. Authors (ICLR 2025 proceedings page): Hanrong Zhang,
   Jingyuan Huang, Kai Mei, Yifei Yao, Zhenting Wang, Chenlu Zhan,
   Hongwei Wang, Yongfeng Zhang.
5. Edoardo Debenedetti, Ilia Shumailov, Tianqi Fan, Jamie Hayes,
   Nicholas Carlini, Daniel Fabian, Christoph Kern, Chongyang Shi, Andreas
   Terzis, Florian Tramèr. *Defeating Prompt Injections by Design.*
   arXiv:2503.18813 (v2, June 2025). The first author's page lists it at
   IEEE SaTML 2026, but no accepted-papers listing confirmed it (17
   October 2026), so cite the arXiv version. v2 says 77% of AgentDojo
   tasks with provable security (84% undefended); v1 said 67%.
6. Rishika Bhagwatkar, Kevin Kasa, Abhay Puri, Gabriel Huang, Irina Rish,
   Graham W. Taylor, Krishnamurthy Dj Dvijotham, Alexandre Lacoste.
   *Indirect Prompt Injections: Are Firewalls All You Need, or Stronger
   Benchmarks?* arXiv:2510.05244 (v1 October 2025, v2 March 2026). (The
   README and roadmap use the shorter title "Are Firewalls All You
   Need?"; cite the full one.) Venue: poster at the NeurIPS 2025 Lock-LLM
   workshop (NeurIPS virtual site and OpenReview, October 2025).
7. ProtectAI. *deberta-v3-base-prompt-injection-v2* model card, Hugging
   Face (Limitations: "does not ... handle non-English prompts").
   Cite as a footnote or URL.
8. Zheng-Xin Yong, Cristina Menghini, Stephen H. Bach. *Low-Resource
   Languages Jailbreak GPT-4.* NeurIPS 2023 Workshop on Socially
   Responsible Language Modelling Research (SoLaR). arXiv:2310.02446.
9. Yue Deng, Wenxuan Zhang, Sinno Jialin Pan, Lidong Bing. *Multilingual
   Jailbreak Challenges in Large Language Models.* ICLR 2024.
   arXiv:2310.06474.
10. Wenxuan Wang, Zhaopeng Tu, Chang Chen, Youliang Yuan, Jen-tse Huang,
    Wenxiang Jiao, Michael R. Lyu. *All Languages Matter: On the
    Multilingual Safety of Large Language Models.* Findings of ACL 2024
    (ACL Anthology 2024.findings-acl.349). arXiv:2310.00905. Languages:
    English, Chinese, Spanish, French, Bengali, Arabic, Hindi, Russian,
    Japanese, German.
11. Haneul Yoo, Yongjin Yang, Hwaran Lee. *Code-Switching Red-Teaming: LLM
    Evaluation for Safety and Multilingual Understanding.* ACL 2025 (long),
    pp. 13392-13413. arXiv:2406.15481.
12. Manuel Costa, Boris Köpf, Aashish Kolluri, Andrew Paverd, Mark
    Russinovich, Ahmed Salem, Shruti Tople, Lukas Wutschitz, Santiago
    Zanella-Béguelin. *Securing AI Agents with Information-Flow Control.*
    arXiv:2505.23643 (v2, September 2025). (FIDES.)
13. Naymul Islam, Nusrat Jahan Lia, Shubhashis Roy Dipta, Sabik Bin
    Sultan, Abdullah Khan Zehady. *Register Shifts Break LLM Safety: A
    Bengali Benchmark with Culturally Grounded Harms* (BanglaSafe).
    arXiv:2608.22335, August 2026. Found by search on 17 October 2026 from
    its arXiv and Hugging Face listings; read the PDF before citing the
    numbers above.

14. Al Muhit Muhtadi, Mostafa Rifat Tazwar. *MIPIAD: Multilingual
    Indirect Prompt Injection Attack Defense with Qwen-TF-IDF Hybrid and
    Meta-Ensemble Learning.* arXiv:2605.07269, May 2026.
15. Madhusudhanan G. *Visible Reasoning and Indirect Prompt-Injection
    Monitorability Across English, Tamil, and Tanglish.* arXiv:2608.15392,
    August 2026.
16. \* *FinVault: Benchmarking Financial Agent Safety in Execution-Grounded
    Environments.* arXiv:2601.07853, January 2026. (Check the author list.)
17. Uchi Uchibeke. *APort Vault: Benchmarking AI Agent Payment
    Authorization with the Open Agent Passport.* arXiv:2609.22076,
    September 2026. (Single author, affiliated with the vendor.)
18. Uchi Uchibeke. *Before the Tool Call: Deterministic Pre-Action
    Authorization for Autonomous AI Agents.* arXiv:2603.20953, March 2026.
19. \* *MCPTox: A Benchmark for Tool Poisoning on Real-World MCP Servers.*
    AAAI 2026, vol. 40(42), pp. 35811-35819. arXiv:2508.14925. (Check the
    author list.)
20. \* Hao Li, Xiaogeng Liu, Chaowei Xiao. *InjecGuard: Benchmarking and
    Mitigating Over-defense in Prompt Injection Guardrail Models.*
    arXiv:2410.22770. (Check authors and venue.)
21. \* Yahan Yang, Soham Dan, Dan Roth, Insup Lee. *Benchmarking LLM
    Guardrails in Handling Multilingual Toxicity.* arXiv:2410.22153. (Check
    authors and venue.)
22. \* *BabelArena: A Large-Scale Multilingual Benchmark for LLM Agents.*
    arXiv:2609.23490, September 2026. (Check the author list.)
23. \* Sahana Chennabasappa, Cyrus Nikolaidis, Daniel Song, David Molnar,
    et al. (Joshua Saxe, corresponding). *LlamaFirewall: An Open Source
    Guardrail System for Building Secure AI Agents.* arXiv:2505.03574, May
    2025. Introduces Prompt Guard 2 (jailbreak detector, 86M and 22M) and
    AlignmentCheck. Also cite Meta's Llama Prompt Guard 2 model card for
    the dropped "injection" label. (Check the full author list.)
24. \* OpenAI. *Technical Report: Research Preview of gpt-oss-safeguard.*
    October 2025. Open-weight 120B and 20B models that classify content
    against a policy supplied at inference time. Cite as a report or URL.

References 14 to 24 were found on 22 October 2026 through search results
(abstracts and listing pages, not the PDFs); read each before citing its
numbers.

Also cited elsewhere in the paper (introduction): OWASP Top 10 for Agentic
Applications (2026), already in the README.

## Optional additions if space allows

Not checked yet; verify before citing.

- Spotlighting (Hines et al., 2024): marking untrusted text in the prompt,
  a prompting defence that does read the text.
- tau-Bench (Yao et al., 2024): customer-service agents with a simulated
  user, relevant to our simulated-user harness lesson (section 5.5).
- BanglaVeilGuard (arXiv:2608.21880, August 2026): cross-script safety
  benchmark and guardrails for Bangla LLMs, including romanised Bangla.
  Close to our detector finding (a guard across scripts); read it before
  the final version and cite it if it tests Banglish inputs.
