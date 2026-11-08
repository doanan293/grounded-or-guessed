"""LLM cost per run id from the gateway log (runs/llm_log.jsonl): fresh successful calls only.

Cache hits cost nothing (a resumed run re-reads them) and failed calls return no tokens; both are
counted separately so a run's cost is what one clean pass would spend.
"""
import json
from collections import defaultdict
from pathlib import Path


def run_costs(log: Path) -> dict[str, dict]:
    out: dict[str, dict] = defaultdict(lambda: {"calls": 0, "prompt_tokens": 0, "completion_tokens": 0,
                                                "latency_s": 0.0, "errors": 0, "cache_hits": 0,
                                                "calls_t0": 0, "tokens_t0": 0})
    for line in Path(log).read_text().splitlines():
        try:
            r = json.loads(line)
        except json.JSONDecodeError:
            continue
        a = out[r.get("run_id")]
        if r.get("error"):
            a["errors"] += 1
        elif r.get("cache_hit"):
            a["cache_hits"] += 1
        else:
            a["calls"] += 1
            a["prompt_tokens"] += r.get("prompt_tokens") or 0
            a["completion_tokens"] += r.get("completion_tokens") or 0
            a["latency_s"] += r.get("latency_s") or 0.0
            if r.get("temperature") == 0.0:  # SemLoc's counterfactual step (constraint inference uses the run T)
                a["calls_t0"] += 1
                a["tokens_t0"] += (r.get("prompt_tokens") or 0) + (r.get("completion_tokens") or 0)
    return dict(out)
