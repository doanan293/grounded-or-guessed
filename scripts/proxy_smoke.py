"""List the models the LLM proxy offers and optionally send one tiny chat to each given id.

    python scripts/proxy_smoke.py                       # list model ids
    python scripts/proxy_smoke.py --try gemini-2.5-pro claude-sonnet-4-6
"""
import argparse
import os
import time

from openai import OpenAI


def main() -> None:
    ap = argparse.ArgumentParser()
    ap.add_argument("--try", dest="models", nargs="*", default=[])
    args = ap.parse_args()
    client = OpenAI(base_url=os.environ.get("FLX_LLM_BASE_URL", "http://localhost:8317/v1"),
                    api_key=os.environ["FLX_LLM_API_KEY"], timeout=120)
    if not args.models:
        for m in sorted(client.models.list().data, key=lambda m: m.id):
            print(m.id)
        return
    for model in args.models:
        t0 = time.time()
        try:
            r = client.chat.completions.create(
                model=model, messages=[{"role": "user", "content": "Reply with the single word OK"}])
            out = (r.choices[0].message.content or "").strip()
        except Exception as e:  # report and continue with the next model
            out = f"ERROR {type(e).__name__}: {e}"[:200]
        print(f"{model:45s} {time.time() - t0:6.1f}s  {out}")


if __name__ == "__main__":
    main()
