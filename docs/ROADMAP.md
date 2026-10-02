# Roadmap

The plan for this project. Every cloud session reads this file and
`CLAUDE.md` first, and updates this file in the same pull request
whenever a task is finished or the plan changes.

**Goal:** a strong research project and a workshop paper.

Last updated: October 2026.

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

## October 2026

- [x] Merge PR #1 and PR #2.
- [ ] One Kaggle run on 302 cases (3 models x none / provenance /
      provenance-amount, 1 repeat) with `notebooks/kaggle_run.ipynb`.
      Expected time: about 3 to 4 hours.
  - First attempt (2 October): all 3 Qwen2.5-7B runs and 3B + provenance
    finished (7B took about 7 minutes per defence). The other 5 runs
    crashed partway: a model got stuck repeating one word, the reply
    timed out or grew too long, and one error stopped the whole run.
    Fixed in PR #3 (reply cap of 1,024 tokens, shorter timeout, an error
    now ends only that case). Rerun the whole notebook so all 9 runs use
    the same settings.
  - First look (7B only, not final): with `provenance`, the only attacks
    that got through were the new amount-only attacks (5 of 220);
    `provenance-amount` stopped all of them.
- [ ] Update the README, demo page and results from that run.
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

Results on 114 cases, 3 models, 3 repeats, temperature 0. Recheck these
against the 302-case run.

- With provenance, 0 of 720 attack episodes succeeded, against 3.8% to 10%
  without it, and no correct payments were blocked.
- Models tried to pay invented payees in 29% to 48% of episodes, more often
  than any attack succeeded.
- Each model falls for attacks in different languages.
- A bigger model was not safer.
- Repeats at temperature 0 are nearly identical, so more cases matter more
  than more repeats.

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
