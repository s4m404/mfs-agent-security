# STALA 2027 paper: LaTeX source

`main.tex` is the submission version of the paper (double-blind), on the
NDSS 2027 template: `IEEEtran.cls` is the class file from the NDSS 2027
templates page, and the first-page notice follows its
`bare_conf_NDSS2027.tex` with the workshop's name (the ISBN and DOI are
placeholders until the workshop publishes its own template). Build with
`latexmk -pdf main.tex` (needs TeX Live with `texlive-publishers` for
`IEEEtran.bst`); figures come from `../figures/` and references from
`../references.bib`. `main.pdf` is the last build.

STALA limits: full papers up to 8 pages, excluding references and
appendices; the "Ethics Considerations" section before the references does
not count either (NDSS 2027 call for papers). The main body currently ends
on page 7.

## Where the numbers come from

The text condenses the drafts in `docs/paper/`, which list the source of
every number:

| Paper section | Draft and sources |
|---|---|
| Abstract, I, VI, VII | `draft_sections_1_8_9.md` |
| II, III | `draft_sections_2_4.md` |
| IV, Appendix A, C | `draft_section_5.md` |
| V | `related_work.md` |
| Table II, Fig. 1 to 3 | `../figures/` (`scripts/make_figures.py`) |
| Table III | `../robustness.md` (`scripts/robustness.py`) |
| Appendix B (extra runs) | README, "Two extra runs" and "Extra runs: a newer open model family (Qwen3)"; raw runs on `groq-results` and `kaggle-results` (`2026-11-23_wallet_tool_qwen3_8b/`, `2026-11-23_qwen3_32b/`) |
| Wallet-tool rerun, 184 of 185 (IV-B) | README, "A poisoned tool from another app"; `kaggle-results`, `2026-11-23_wallet_tool_qwen3_8b/results_wallet_tool/` |
| 239 million MFS users | Bangladesh Bank, MFS comparative summary statement of January and February 2025 (`references.bib`, `bangladeshbank2025mfs`) |
| Question counts (35, 14 of 22) | `../question_coding.md` (keyword coding; the hand check of `../question_sample.csv` is still open) |

## Before submitting

- Create the anonymised copy of the repository and put its link in
  `\repourl` (now a placeholder).
- Complete the "Use of Generative AI" statement (tool versions) and check
  that it describes how the paper was written.
- Check the STALA submission site for any template or ISBN change.
