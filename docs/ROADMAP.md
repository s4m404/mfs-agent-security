# Roadmap

The plan for this project. Every cloud session reads this file and
`CLAUDE.md` first, and updates this file in the same pull request
whenever a task is finished or the plan changes.

**Goal:** a strong research project and a workshop paper.

Last updated: 5 October 2026 (STALA call for papers checked).

## Done

- Fictional TakaPay wallet served over MCP, agent loop, scoring and tests.
- Defences: none, keyword (baseline), provenance, provenance-amount.
- Results for 3 model sizes (Qwen2.5 3B, 7B, 14B-AWQ), 3 repeats, on 114 cases.
- Public demo page (`docs/index.html`).
- Test set grown to 302 cases, with new tasks, new attack styles,
  amount-only attacks and more hard benign cases; the 61 new Bangla and
  Banglish sentences are native-speaker reviewed (PR #1).
- `notebooks/kaggle_run.ipynb` set up for 302 cases x 3 models x
  none / provenance / provenance-amount, 1 repeat (PR #1).
- `scripts/run_bench.py --workers` runs several cases at once, so the
  Kaggle run fits well inside the 12-hour limit (PR #2).
- A stuck model reply can no longer crash a run (PR #3).
- Full 302-case run: 3 Qwen2.5 models x none / provenance /
  provenance-amount, 1 repeat, 0 model errors, about 1.5 hours on Kaggle.
  README, demo page and key findings updated (PR #4).

## October 2026

- [x] Merge PR #1, PR #2 and PR #3.
- [x] One Kaggle run on 302 cases (3 models x none / provenance /
      provenance-amount, 1 repeat) with `notebooks/kaggle_run.ipynb`.
      The first attempt crashed on stuck model replies (fixed in PR #3);
      the second finished all 9 runs in about 1.5 hours.
- [x] Update the README, demo page and results from that run (PR #4).
- [x] Add a second model family so the results are not only Qwen.
      Llama 3.1 and Gemma need a Hugging Face account, so we used models
      that do not (PR #5, crash fix in PR #6). Hermes 3 (Llama 3.1 8B,
      fine-tuned by Nous Research) shows the same pattern as Qwen:
      provenance-amount 0 of 220 attacks, 0 correct payments blocked
      (README, PR #7). IBM Granite 3.3 8B is left out: its tool calls came
      out as plain text in this setup (0.2 tool calls per case).
- [x] Find 2 or 3 suitable workshops and plan the paper around the
      earliest realistic one (see "Paper target" below; PR #8).
- [ ] Paper outline and figures script (`scripts/make_figures.py`), so the
      draft can start before cloud credits run out on 5 November.
- [ ] Add a short GIF of the demo to the top of the README.

## Paper target

Checked on 4 October 2026. STALA details below were read from its call for
papers on 5 October 2026; the ICLR and ACL rows still need checking when
their workshop lists come out.

| Workshop | Fit | Paper deadline | Notification | Where and when |
|---|---|---|---|---|
| **STALA 2027**: Security Testing and Assurance for LLMs and Agents, at NDSS ([site](https://stala-workshop.github.io/)) | Best: prompt-injection testing of LLM agents is a listed topic | **11 Dec 2026** | 1 Feb 2027 | Seoul, 22 Mar 2027 |
| ICLR 2027 workshops ([call](https://iclr.cc/Conferences/2027/CallForWorkshops)), e.g. agent safety or security workshops | Good, if an agent-security workshop is accepted (list due 29 Nov 2026) | about 1 Feb 2027 | by 26 Feb 2027 | with ICLR, April 2027 |
| ACL 2027 workshops ([call](https://www.aclweb.org/portal/content/joint-call-workshops-proposals-2027)), e.g. a low-resource or multilingual workshop | Good for the Bangla / Banglish angle; list not out yet | about 5 Feb 2027 | later | with ACL, summer 2027 |

EACL 2027 workshops (papers about 15 Dec 2026, Athens, March 2027) are a
fallback if one on low-resource or multilingual safety is announced.

**STALA call for papers (read 5 October 2026):**

- Full papers: 8 pages; short, position and experience papers (including
  "early methods, benchmark or dataset contributions"): 4 pages. References
  do not count. We aim for an 8-page full paper.
- Deadline 11 December 2026, 23:59 AoE; notification 1 February 2027;
  camera-ready 19 February 2027; workshop 22 March 2027 in Seoul.
- Archival: accepted papers appear in the NDSS 2027 co-located workshop
  proceedings (Internet Society). The same paper cannot then go to another
  archival venue; most ICLR workshops are non-archival.
- Selective: about 7 to 9 papers in a single-track day.
- In person in Seoul (workshop day Monday 22 March 2027, to be confirmed by
  NDSS). Attending needs NDSS workshop registration. Before submitting,
  check whether an author must register and present in person, the cost,
  and whether NDSS offers student travel grants or remote presentation.
- Template and anonymisation rules: not out yet ("submission site opens
  soon"). Check again in November. If reviewing is double-blind, the paper
  must link an anonymised copy of the repo instead of github.com/s4m404.
- Reviewers want general testing insight, not just a new attack: "a new
  attack shown on a small prompt collection is not sufficient on its own
  unless it contributes a general testing insight", and "negative results
  are particularly welcome when they show that an intuitive testing metric,
  benchmark or assurance interpretation is misleading".

**How the paper should be framed for STALA** (every point already backed by
the README numbers):

1. Attack success alone is a misleading metric for payment agents: models
   made wrong payments with no attacker involved (invented payees, guessed
   amounts) more often than any attack succeeded.
2. Checking only "did money reach the attacker" misses amount-only attacks,
   which pay the real payee; all attacks that got past recipient provenance
   were of this kind, and the amount check stopped them with no false blocks.
3. Harness choices change the scores: the simulated user only answers a
   "?", which lowered Hermes 3's task completion.
4. The benchmark itself: 302 cases in Bangla, Banglish, code-mixed and
   English text, over MCP, with reproducible results on two model families.

**Plan:** submit to STALA on 11 December 2026. If it is not accepted
(1 February), improve the paper with the reviews and the injection detector
and submit to an ICLR 2027 or ACL 2027 workshop in early February.

## October 2026 (rest of the month)

- [ ] Paper outline: sections, the 3 or 4 figures and tables, and what each
      claims, using only numbers already in the README.
- [ ] Figures script in the repo (attack success by defence and model,
      by attack language, wrong payments with and without the amount check).
- [ ] Error analysis of the cases where models fail (needed for the paper).
      Start with: the simulated user answers only replies with a "?", so a
      model that asks "Please confirm ..." gets no answer (about 14 of
      Hermes 3's 64 failed normal tasks; 1 to 2 per Qwen model); and
      Hermes 3 sometimes says it paid without calling a payment tool (9 tasks).

## November 2026

- [ ] Full paper draft by 30 November (cloud credits end 5 November, so the
      outline, figures and first sections come first). Working title: "Can AI
      agents be tricked into moving money in Bangla?"
  - Sections: motivation (mobile money in Bangladesh, agents that make
    payments), benchmark design, defences, results, the invented-payee
    finding, limitations (synthetic data, one wallet, simulated user),
    ethics.

## December 2026

- [ ] Final checks and submit to STALA by 11 December.
- [ ] Release the dataset with the submission (or at camera-ready if the
      workshop asks for anonymity).
- [ ] Write a one-page plan for Project 2 so it can start straight after
      the paper.

## January 2027 onwards

- [ ] A trained multilingual injection detector (small model; Bangla,
      Banglish and English) as a third defence, compared with provenance on
      attack success and false blocks. Moved after the first submission;
      it strengthens the February resubmission or a longer version.
- [ ] If needed, resubmit to an ICLR 2027 or ACL 2027 workshop (early
      February).
- [ ] Start Project 2: detecting compromised AI agents in a security
      operations centre (SOC), using this project's traces as attack data.

## Ideas not yet scheduled

From the earlier README roadmap; not part of the plan above unless moved in.

- Connect BRACUVerify as a second backend.
- Compare with the sanitiser defence from "Indirect Prompt Injections: Are
  Firewalls All You Need?".
- Prepaid mobile recharge as a task (needs a new wallet tool).

## Key findings to keep

From the 302-case run (3 Qwen2.5 models, 1 repeat, temperature 0), checked
against the earlier 114-case run with 3 repeats.

- With provenance plus the amount check, 0 of 660 attack episodes
  succeeded, against 5.9% to 7.7% without a defence; no correct payment
  was blocked and no wrong payment went through.
- Provenance alone stopped every attack that redirects money or leaks the
  OTP, but not attacks that change only the amount (11 of 60 got through).
  Without a defence, amount-only attacks were the most successful kind.
- Models tried to pay invented payees in 29% to 52% of episodes, more often
  than any attack succeeded (114-case run: 29% to 48%).
- Each model falls for attacks in different languages (3B and 14B mostly
  English; 7B mostly mixed text).
- A bigger model was not safer (14B: highest attack success, 7.7%).
- The pattern holds for a second model family: Hermes 3 (Llama 3.1 8B)
  2.3% attack success without a defence, 1 amount-only attack past
  provenance, 0 with provenance-amount, no correct payment blocked.
- Results reproduce: the original 114 cases gave 10.0% / 3.8% / 6.2%
  attack success, against 10.0% / 3.8% / 5.0% before. Repeats at
  temperature 0 are nearly identical, so more cases matter more than more
  repeats.

## How we work

- One task per cloud session. Each session starts by reading `CLAUDE.md`
  and this file. Work on a branch, open a pull request, and update this
  roadmap in the same pull request. The owner merges.
- Before a merge, give a 5-line summary of what changed and why, in plain
  English.
- Model runs happen on Kaggle (free T4 GPUs), because cloud sessions have
  no GPU. When a run is needed, say which notebook to use and the expected
  time. The owner starts it with Save Version and uploads `results.zip` in
  a new session for analysis.
- All Bangla and Banglish text is reviewed by a native speaker before it
  counts as reviewed.
- Cloud session time is limited, so October tasks come first.
