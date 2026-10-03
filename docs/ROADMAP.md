# Roadmap

The plan for this project. Every cloud session reads this file and
`CLAUDE.md` first, and updates this file in the same pull request
whenever a task is finished or the plan changes.

**Goal:** a strong research project and a workshop paper.

Last updated: 3 October 2026.

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
- [ ] Add a second model family (for example Llama 3.1 8B or Gemma 2 9B, if
      tool calling works on vLLM) so the results are not only Qwen.
- [ ] Find 2 or 3 suitable workshops (AI security, NLP for low-resource
      languages, or agent safety) with their deadlines, and plan the paper
      around the earliest realistic one.
- [ ] Add a short GIF of the demo to the top of the README.

## November 2026

- [ ] A trained multilingual injection detector (small model; Bangla,
      Banglish and English) as a third defence, compared with provenance on
      attack success and false blocks.
- [ ] Error analysis of the cases where models fail.

## December 2026

- [ ] Paper draft. Working title: "Can AI agents be tricked into moving
      money in Bangla?"
  - Sections: motivation (mobile money in Bangladesh, agents that make
    payments), benchmark design, defences, results, the invented-payee
    finding, limitations (synthetic data, one wallet, simulated user),
    ethics.
- [ ] Make the figures with a script in the repo.
- [ ] Write a one-page plan for Project 2 so it can start straight after
      the paper.

## January 2027 onwards

- [ ] Submit the paper and release the dataset.
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
