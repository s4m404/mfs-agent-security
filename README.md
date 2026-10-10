# Raw Kaggle results

Raw outputs of the benchmark runs on Kaggle (vLLM, two T4 GPUs, temperature
0, one run per case). Each run folder holds `traces.jsonl` (every step of
every episode), `scores.jsonl` (one score per episode) and `summary.md`.
Folder names follow `<model>__<defence>__<prompt>`. The code is on `main`.

| Folder | Runs | Cases |
|---|---|---|
| `2026-10-02_qwen_3b_7b_14b/results/` | Qwen2.5-3B-Instruct, Qwen2.5-7B-Instruct and Qwen2.5-14B-Instruct-AWQ: none, provenance, provenance-amount | main 302 |
| `2026-10-03_hermes3_granite/results/` | Hermes-3-Llama-3.1-8B and Granite 3.3 8B: none, provenance, provenance-amount | main 302 |
| `2026-10-05_qwen32b_old_block_message/results/` | Qwen2.5-32B-Instruct-AWQ: none, provenance, provenance-amount (old block message for a wrong biller account) | main 302 |
| `2026-10-06_qwen32b_new_block_message/results/` | Qwen2.5-32B: provenance-amount (new block message), provenance-consistent (first version) | main 302 |
| `2026-10-06_qwen32b_new_block_message/results_adaptive/` | Qwen2.5-32B: none, provenance-amount, provenance-consistent (first version) | adaptive 56 |
| `2026-10-06_qwen32b_consistent_fixed/results/` | Qwen2.5-32B: provenance-consistent (fixed: checks the whole inbox) | main 302 |
| `2026-10-06_qwen32b_consistent_fixed/results_adaptive/` | Qwen2.5-32B: provenance-consistent (fixed) | adaptive 56 |
| `2026-10-06_detectors/results_detectors/` | Injection detectors (keyword, ProtectAI DeBERTa v2, deepset DeBERTa) on every untrusted text: `flags.jsonl` (one row per text), `summary.md` | 174 attack and 54 normal texts |

Granite 3.3 is not in the reported results: its tool calls came out as plain
text in this setup (0.2 tool calls per case).

**Not here yet:** the earlier 114-case run with 3 repeats (and the
interrupted first attempts of the 302-case run). Add them as new dated
folders.

GPT-OSS-120B results are on the `groq-results` branch.

Check everything from the raw traces (on a checkout of `main`, with this
branch unpacked next to it):

```
python scripts/rescore.py <folder>/results                     # main cases
python scripts/rescore.py <folder>/results_adaptive --cases bench/cases_adaptive
python scripts/compare_runs.py <folder>/results
python scripts/conditional_rates.py <folder>/results
python scripts/count_confirmations.py <folder>/results
python scripts/detector_eval.py --from-flags 2026-10-06_detectors/results_detectors/flags.jsonl
```

Several folders hold a run with the same name (for example two
provenance-amount runs of Qwen2.5-32B); pass one folder at a time, or pass
them oldest first to `scripts/make_figures.py` (the last one wins).
