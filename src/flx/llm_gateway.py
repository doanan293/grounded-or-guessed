"""Single entry point for every LLM call in the experiments.

All calls go to the OpenAI-compatible proxy (FLX_LLM_BASE_URL). Each call is
logged as one JSONL record and, unless FLX_LLM_CACHE=0, cached on disk under a
key that includes FLX_RUN_ID, so repeated runs of one configuration (different
run ids) always reach the model while re-running the same run id is free.
"""
import hashlib
import json
import os
import tempfile
import time
from pathlib import Path

import openai

RETRYABLE = (openai.RateLimitError, openai.APIConnectionError, openai.APITimeoutError,
             openai.InternalServerError)


class LLMUnavailable(RuntimeError):
    """The model could not be reached after all retries."""


class LLMEmptyResponse(RuntimeError):
    """The model answered with no content."""


def _client() -> openai.OpenAI:
    return openai.OpenAI(base_url=os.environ.get("FLX_LLM_BASE_URL", "http://localhost:8317/v1"),
                         api_key=os.environ.get("FLX_LLM_API_KEY", ""),
                         timeout=float(os.environ.get("FLX_LLM_TIMEOUT", "600")), max_retries=0)


def _key(model, system, user, temperature, run_id) -> str:
    blob = json.dumps({"model": model, "system": system, "user": user,
                       "temperature": temperature, "run_id": run_id}, sort_keys=True)
    return hashlib.sha256(blob.encode()).hexdigest()


def _atomic_write(path: Path, text: str) -> None:
    path.parent.mkdir(parents=True, exist_ok=True)
    fd, tmp = tempfile.mkstemp(dir=path.parent, suffix=".tmp")
    with os.fdopen(fd, "w") as f:
        f.write(text)
    os.replace(tmp, path)


def _log(record: dict) -> None:
    path = Path(os.environ.get("FLX_LLM_LOG", "runs/llm_log.jsonl"))
    path.parent.mkdir(parents=True, exist_ok=True)
    with open(path, "a") as f:  # one short line per write; appends are atomic enough across workers
        f.write(json.dumps(record) + "\n")


def chat(model: str, system: str, user: str, temperature: float = 0.0,
         max_tokens: int | None = None) -> str:
    run_id = os.environ.get("FLX_RUN_ID", "default")
    use_cache = os.environ.get("FLX_LLM_CACHE", "1") != "0"
    key = _key(model, system, user, temperature, run_id)
    cache_file = Path(os.environ.get("FLX_LLM_CACHE_DIR", "runs/llm_cache")) / f"{key}.json"
    rec = {"ts": time.time(), "run_id": run_id, "model": model, "temperature": temperature,
           "cache_hit": False, "prompt_tokens": None, "completion_tokens": None,
           "latency_s": None, "error": None, "served_model": None, "key": key}

    if use_cache and cache_file.exists():
        cached = json.loads(cache_file.read_text())
        _log({**rec, "cache_hit": True, "prompt_tokens": cached.get("prompt_tokens"),
              "completion_tokens": cached.get("completion_tokens"), "served_model": cached.get("served_model")})
        return cached["content"]

    max_retries = int(os.environ.get("FLX_LLM_MAX_RETRIES", "6"))
    kwargs = {"model": model, "temperature": temperature,
              "messages": [{"role": "system", "content": system}, {"role": "user", "content": user}]}
    if max_tokens is not None:
        kwargs["max_tokens"] = max_tokens
    t0 = time.time()
    for attempt in range(max_retries + 1):
        try:
            resp = _client().chat.completions.create(**kwargs)
            break
        except RETRYABLE as e:
            if attempt == max_retries:
                _log({**rec, "latency_s": time.time() - t0, "error": f"{type(e).__name__}: {e}"[:300]})
                raise LLMUnavailable(f"{model}: {e}") from e
            time.sleep(min(2 * 2 ** attempt, 60))

    content = resp.choices[0].message.content
    usage = getattr(resp, "usage", None)
    rec.update(latency_s=time.time() - t0,
               prompt_tokens=getattr(usage, "prompt_tokens", None),
               completion_tokens=getattr(usage, "completion_tokens", None),
               served_model=getattr(resp, "model", None))  # upstream may substitute the requested model
    if not content or not content.strip():
        _log({**rec, "error": "empty response"})
        raise LLMEmptyResponse(model)
    _log(rec)
    if use_cache:
        _atomic_write(cache_file, json.dumps({"content": content, "prompt_tokens": rec["prompt_tokens"],
                                              "completion_tokens": rec["completion_tokens"],
                                              "served_model": rec["served_model"]}))
    return content
