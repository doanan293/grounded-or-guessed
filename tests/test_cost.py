import json

from flx.cost import run_costs


def test_run_costs_counts_only_fresh_successful_calls(tmp_path):
    log = tmp_path / "log.jsonl"
    recs = [
        {"run_id": "a", "prompt_tokens": 10, "completion_tokens": 5, "latency_s": 2.0, "error": None, "cache_hit": False},
        {"run_id": "a", "prompt_tokens": 10, "completion_tokens": 5, "latency_s": 0.0, "error": None, "cache_hit": True},
        {"run_id": "a", "error": "RateLimitError: 429", "latency_s": 1.0},
        {"run_id": "b", "prompt_tokens": 1, "completion_tokens": 1, "latency_s": 1.0, "error": None, "cache_hit": False},
    ]
    log.write_text("\n".join(json.dumps(r) for r in recs) + "\nnot json\n")
    c = run_costs(log)
    assert c["a"] == {"calls": 1, "prompt_tokens": 10, "completion_tokens": 5, "latency_s": 2.0, "errors": 1, "cache_hits": 1,
                      "calls_t0": 0, "tokens_t0": 0}
    assert c["b"]["calls"] == 1


def test_run_costs_splits_temperature_zero_calls(tmp_path):
    """SemLoc's counterfactual step calls the LLM at T=0, constraint inference at the run temperature."""
    log = tmp_path / "log.jsonl"
    recs = [{"run_id": "s", "temperature": 0.8, "prompt_tokens": 100, "completion_tokens": 50, "latency_s": 1.0},
            {"run_id": "s", "temperature": 0.0, "prompt_tokens": 20, "completion_tokens": 10, "latency_s": 1.0}]
    log.write_text("\n".join(json.dumps(r) for r in recs))
    c = run_costs(log)["s"]
    assert (c["calls"], c["calls_t0"], c["tokens_t0"]) == (2, 1, 30)
