"""Check that an API key, model and settings work, before a long run.

Sends one short request with one tool and checks that the model calls it.
Exits with 1 (and says why) if the request fails or no tool call comes back,
so a wrong key or setting does not turn every case into a model error.

Run:  python scripts/check_api.py --model openai/gpt-oss-120b \
          --base-url https://api.groq.com/openai/v1 --api-key-env GROQ_API_KEY
"""

from __future__ import annotations

import argparse
import json
import sys
from pathlib import Path

sys.path.insert(0, str(Path(__file__).resolve().parents[1]))

from agent.llm import OpenAICompatModel, RateLimited  # noqa: E402

TOOL = {
    "type": "function",
    "function": {
        "name": "check_balance",
        "description": "Return the wallet balance in Taka.",
        "parameters": {"type": "object", "properties": {}},
    },
}


def main() -> None:
    p = argparse.ArgumentParser(description=__doc__, formatter_class=argparse.RawDescriptionHelpFormatter)
    p.add_argument("--model", required=True)
    p.add_argument("--base-url", required=True)
    p.add_argument("--api-key-env", default="OPENAI_API_KEY")
    p.add_argument("--extra-body", default=None, help="extra API settings as JSON")
    p.add_argument("--max-tokens", type=int, default=1024)
    args = p.parse_args()
    extra = json.loads(args.extra_body) if args.extra_body else None
    model = OpenAICompatModel(args.model, args.base_url, args.api_key_env, max_tokens=args.max_tokens, extra_body=extra)
    messages = [{"role": "system", "content": "You manage a mobile wallet. Use the tools."},
                {"role": "user", "content": "What is my balance?"}]
    try:
        reply = model.complete(messages, [TOOL])
    except RateLimited as exc:
        print(f"API works, but the rate limit is reached for now: {exc}")
        sys.exit(3)
    except Exception as exc:
        print(f"API check failed: {type(exc).__name__}: {str(exc)[:1000]}")
        sys.exit(1)
    if not any(c["name"] == "check_balance" for c in reply["tool_calls"]):
        print(f"API answered, but without a tool call (tool calling may not work for this model): {reply}")
        sys.exit(1)
    print(f"API check passed: {args.model} called check_balance.")


if __name__ == "__main__":
    main()
