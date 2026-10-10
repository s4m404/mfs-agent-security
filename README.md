# Raw Kaggle results

Raw outputs of the benchmark runs on Kaggle (vLLM, two T4 GPUs, temperature
0, one run per case). Each run folder holds `traces.jsonl` (every step of
every episode), `scores.jsonl` (one score per episode) and `summary.md`.
Folder names follow `<model>__<defence>__<prompt>`. The code is on `main`.

| Folder | Runs | Cases |
|---|---|---|
| `2026-10-03_hermes3_granite/results/` | Hermes-3-Llama-3.1-8B and Granite 3.3 8B: none, provenance, provenance-amount | main 302 |
| `2026-10-05_qwen32b_old_block_message/results/` | Qwen2.5-32B-Instruct-AWQ: none, provenance, provenance-amount (old block message for a wrong biller account) | main 302 |
| `2026-10-06_qwen32b_new_block_message/results/` | Qwen2.5-32B: provenance-amount (new block message), provenance-consistent (first version) | main 302 |
| `2026-10-06_qwen32b_new_block_message/results_adaptive/` | Qwen2.5-32B: none, provenance-amount, provenance-consistent (first version) | adaptive 56 |
| `2026-10-06_qwen32b_consistent_fixed/results/` | Qwen2.5-32B: provenance-consistent (fixed: checks the whole inbox) | main 302 |
| `2026-10-06_qwen32b_consistent_fixed/results_adaptive/` | Qwen2.5-32B: provenance-consistent (fixed) | adaptive 56 |

Granite 3.3 is not in the reported results: its tool calls came out as plain
text in this setup (0.2 tool calls per case).

**Not here yet:** the Qwen2.5 3B, 7B and 14B-AWQ runs on the 302 cases, the
earlier 114-case run with 3 repeats, and the detector flags
(`results_detectors/flags.jsonl`). Add them as new dated folders.

GPT-OSS-120B results are on the `groq-results` branch.

Check everything from the raw traces (on a checkout of `main`, with this
branch unpacked next to it):

```
python scripts/rescore.py <folder>/results                     # main cases
python scripts/rescore.py <folder>/results_adaptive --cases bench/cases_adaptive
python scripts/compare_runs.py <folder>/results
python scripts/conditional_rates.py <folder>/results
python scripts/count_confirmations.py <folder>/results
```

Several folders hold a run with the same name (for example two
provenance-amount runs of Qwen2.5-32B); pass one folder at a time, or pass
them oldest first to `scripts/make_figures.py` (the last one wins).
