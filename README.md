# Raw Kaggle results

Raw outputs of the benchmark runs on Kaggle (vLLM, two T4 GPUs, temperature
0, one run per case). Each run folder holds `traces.jsonl` (every step of
every episode), `scores.jsonl` (one score per episode) and `summary.md`.
Folder names follow `<model>__<defence>__<prompt>`. The code is on `main`.

| Folder | Runs | Cases |
|---|---|---|
| `2026-09-30_qwen_114cases_3repeats/results/` | Qwen2.5 3B, 7B and 14B-AWQ: none and provenance, 3 repeats each (earlier code; cases are the original 114, which are still the first 114 of the main set) | 114 x 3 |
| `2026-10-02_qwen_3b_7b_14b/results/` | Qwen2.5-3B-Instruct, Qwen2.5-7B-Instruct and Qwen2.5-14B-Instruct-AWQ: none, provenance, provenance-amount | main 302 |
| `2026-10-03_hermes3_granite/results/` | Hermes-3-Llama-3.1-8B and Granite 3.3 8B: none, provenance, provenance-amount | main 302 |
| `2026-10-05_qwen32b_old_block_message/results/` | Qwen2.5-32B-Instruct-AWQ: none, provenance, provenance-amount (old block message for a wrong biller account) | main 302 |
| `2026-10-06_qwen32b_new_block_message/results/` | Qwen2.5-32B: provenance-amount (new block message), provenance-consistent (first version) | main 302 |
| `2026-10-06_qwen32b_new_block_message/results_adaptive/` | Qwen2.5-32B: none, provenance-amount, provenance-consistent (first version) | adaptive 56 |
| `2026-10-06_qwen32b_consistent_fixed/results/` | Qwen2.5-32B: provenance-consistent (fixed: checks the whole inbox) | main 302 |
| `2026-10-06_qwen32b_consistent_fixed/results_adaptive/` | Qwen2.5-32B: provenance-consistent (fixed) | adaptive 56 |
| `2026-10-06_detectors/results_detectors/` | Injection detectors (keyword, ProtectAI DeBERTa v2, deepset DeBERTa) on every untrusted text: `flags.jsonl` (one row per text), `summary.md` | 174 attack and 54 normal texts |
| `2026-10-23_message_payee/results_message_payee/` | Qwen2.5 3B, 7B, 14B-AWQ, 32B-AWQ and Hermes-3-Llama-3.1-8B: none, provenance, provenance-amount | message-payee 24 (normal tasks whose payee is only in a message) |
| `2026-11-03_third_party/results_third_party/` | Qwen2.5 3B, 7B, 14B-AWQ, 32B-AWQ and Hermes-3-Llama-3.1-8B: none, provenance, provenance-amount (vLLM 0.32.0; `run_env.json` next to it records the Python, vLLM, PyTorch and CUDA versions, the GPUs and each model's Hugging Face revision) | third-party 37 (the main set's tool-description attacks, with the poisoned text on a third-party tool) |
| `2026-11-23_qwen3_32b/results/`, `results_message_payee/`, `results_third_party/` | Qwen3-32B-AWQ (a newer model family; thinking mode off): none and provenance-amount (vLLM 0.32.0; `run_env.json` next to them) | main 302, message-payee 24, third-party 37 |
| `2026-11-23_wallet_tool_qwen3_8b/results_wallet_tool/` | Wallet-tool rerun: Qwen2.5 3B, 7B, 14B-AWQ, 32B-AWQ and Hermes-3-Llama-3.1-8B, none (vLLM 0.32.0; `run_env.json` next to it) | the main set's 37 tool-description attacks, unchanged, to pair with `2026-11-03_third_party` |
| `2026-11-23_wallet_tool_qwen3_8b/results/`, `results_message_payee/`, `results_third_party/` | Qwen3-8B (thinking mode off): none and provenance-amount. Qwen3-14B-AWQ did not start in this session (download failed, "Read-only file system"; log in `results/vllm_failed_Qwen_Qwen3-14B-AWQ.log`) | main 302, message-payee 24, third-party 37 |

Granite 3.3 is not in the reported results: its tool calls came out as plain
text in this setup (0.2 tool calls per case).

**Not here:** the interrupted first attempts of the 302-case run (only the
finished runs were kept).

GPT-OSS-120B results are on the `groq-results` branch.

Check everything from the raw traces (on a checkout of `main`, with this
branch unpacked next to it):

```
python scripts/rescore.py <folder>/results                     # main cases
python scripts/rescore.py <folder>/results_adaptive --cases bench/cases_adaptive
python scripts/rescore.py <folder>/results_message_payee --cases bench/cases_message_payee
python scripts/audit_message_payee.py --runs <folder>/results_message_payee
python scripts/rescore.py <folder>/results_third_party --cases bench/cases_third_party
python scripts/compare_tool_poison.py --wallet <main-set results folders> --third-party <folder>/results_third_party
python scripts/compare_runs.py <folder>/results
python scripts/conditional_rates.py <folder>/results
python scripts/count_confirmations.py <folder>/results
python scripts/detector_eval.py --from-flags 2026-10-06_detectors/results_detectors/flags.jsonl
```

Several folders hold a run with the same name (for example two
provenance-amount runs of Qwen2.5-32B); pass one folder at a time, or pass
them oldest first to `scripts/make_figures.py` (the last one wins).
