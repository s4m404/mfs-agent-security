# Running models on the university HPC

The benchmark talks to any OpenAI compatible endpoint. On the HPC, serve an
open model with vLLM, then point `--base-url` at it.

## 1. One time setup

```bash
module load python cuda            # module names differ per cluster; check `module avail`
python -m venv ~/venvs/vllm
source ~/venvs/vllm/bin/activate
pip install vllm
```

Model weights are large. Point the Hugging Face cache at scratch space, not
your home directory:

```bash
export HF_HOME=/path/to/your/scratch/hf_cache
```

## 2. Slurm job that serves a model

Save as `serve.slurm`, fill in the bracketed values from your cluster's
documentation, and submit with `sbatch serve.slurm`.

```bash
#!/bin/bash
#SBATCH --job-name=vllm-serve
#SBATCH --partition=[gpu partition name]
#SBATCH --gres=gpu:1
#SBATCH --cpus-per-task=8
#SBATCH --mem=64G
#SBATCH --time=08:00:00
#SBATCH --output=vllm-%j.log

source ~/venvs/vllm/bin/activate
export HF_HOME=[your scratch path]/hf_cache
echo "Serving on $(hostname)"

# Qwen models use the hermes tool call parser.
vllm serve Qwen/Qwen2.5-7B-Instruct \
  --host 0.0.0.0 --port 8000 \
  --enable-auto-tool-choice --tool-call-parser hermes
```

For Llama 3.1 style models use `--tool-call-parser llama3_json`. Check the
vLLM documentation for the right parser for newer models.

## 3. Run the benchmark against it

Find the node name in the log (`Serving on ...`), then from a login node or
another job:

```bash
python scripts/run_bench.py --model Qwen/Qwen2.5-7B-Instruct \
  --base-url http://[node name]:8000/v1 --defence none
```

## Suggested model set for the paper

Pick three or four open models of different sizes and families, all with
tool calling support, for example one 7B to 8B model, one around 14B and one
around 32B, plus one hosted API model if you have budget. Record exact model
names and versions in the results, because reviewers will ask.
