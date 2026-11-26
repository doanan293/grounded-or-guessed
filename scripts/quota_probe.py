"""Measure how many sequential calls a proxy model sustains before rate limiting.

    python scripts/quota_probe.py --model gemini-3.8-flash-high --n 40
Writes runs/quota/<model>.json. Prompts are distinct so no cache can answer them.
"""
import argparse
import json
import os
import statistics
import time
from pathlib import Path

import openai
from openai import OpenAI


def main() -> None:
    ap = argparse.ArgumentParser()
    ap.add_argument("--model", required=True)
    ap.add_argument("--n", type=int, default=40)
    args = ap.parse_args()
    client = OpenAI(base_url=os.environ.get("FLX_LLM_BASE_URL", "http://localhost:8317/v1"),
                    api_key=os.environ["FLX_LLM_API_KEY"], timeout=120, max_retries=0)
    ok = rate_limited = other = 0
    latencies, errors = [], []
    t_start = time.time()
    for i in range(args.n):
        t0 = time.time()
        try:
            client.chat.completions.create(
                model=args.model,
                messages=[{"role": "user", "content": f"What is {i} + {i * 7}? Answer with the number only."}])
            ok += 1
            latencies.append(time.time() - t0)
        except openai.RateLimitError as e:
            rate_limited += 1
            errors.append(f"{i}: 429 {str(e)[:120]}")
        except Exception as e:
            other += 1
            errors.append(f"{i}: {type(e).__name__} {str(e)[:120]}")
    wall = time.time() - t_start
    result = {"model": args.model, "n": args.n, "ok": ok, "rate_limited": rate_limited, "other_errors": other,
              "median_latency_s": round(statistics.median(latencies), 2) if latencies else None,
              "calls_per_min": round(ok / wall * 60, 1), "wall_s": round(wall, 1), "errors": errors[:10]}
    out = Path("runs/quota") / f"{args.model}.json"
    out.parent.mkdir(parents=True, exist_ok=True)
    out.write_text(json.dumps(result, indent=2))
    print(json.dumps({k: v for k, v in result.items() if k != "errors"}))


if __name__ == "__main__":
    main()
