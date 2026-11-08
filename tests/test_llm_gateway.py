import json
from types import SimpleNamespace

import openai
import pytest

from flx import llm_gateway


class FakeClient:
    """Stands in for openai.OpenAI; records calls and returns a scripted reply."""

    def __init__(self, content="hello", raise_exc=None, usage=(11, 7)):
        self.calls = 0
        self._content, self._raise, self._usage = content, raise_exc, usage
        self.chat = SimpleNamespace(completions=SimpleNamespace(create=self._create))

    def _create(self, **kwargs):
        self.calls += 1
        if self._raise is not None:
            raise self._raise
        msg = SimpleNamespace(content=self._content)
        usage = SimpleNamespace(prompt_tokens=self._usage[0], completion_tokens=self._usage[1])
        return SimpleNamespace(choices=[SimpleNamespace(message=msg)], usage=usage, model="served-" + kwargs["model"])


def _rate_limit_error():
    # Build the SDK's own exception without touching its HTTP layer (openai 3.x uses httpx2).
    err = openai.RateLimitError.__new__(openai.RateLimitError)
    Exception.__init__(err, "slow down")
    return err


@pytest.fixture
def env(tmp_path, monkeypatch):
    monkeypatch.setenv("FLX_LLM_CACHE_DIR", str(tmp_path / "cache"))
    monkeypatch.setenv("FLX_LLM_LOG", str(tmp_path / "log.jsonl"))
    monkeypatch.setenv("FLX_RUN_ID", "default")
    monkeypatch.delenv("FLX_LLM_CACHE", raising=False)
    monkeypatch.setattr(llm_gateway.time, "sleep", lambda s: None)
    return tmp_path


def _use(monkeypatch, client):
    monkeypatch.setattr(llm_gateway, "_client", lambda: client)
    return client


def _log(env):
    return [json.loads(line) for line in (env / "log.jsonl").read_text().splitlines()]


def test_cache_hit_skips_api(env, monkeypatch):
    c = _use(monkeypatch, FakeClient())
    assert llm_gateway.chat("m", "s", "u", 0.8) == "hello"
    assert llm_gateway.chat("m", "s", "u", 0.8) == "hello"
    assert c.calls == 1
    assert [r["cache_hit"] for r in _log(env)] == [False, True]


def test_run_id_separates_cache(env, monkeypatch):
    c = _use(monkeypatch, FakeClient())
    monkeypatch.setenv("FLX_RUN_ID", "r1")
    llm_gateway.chat("m", "s", "u", 0.8)
    monkeypatch.setenv("FLX_RUN_ID", "r2")
    llm_gateway.chat("m", "s", "u", 0.8)
    assert c.calls == 2


def test_cache_disabled(env, monkeypatch):
    c = _use(monkeypatch, FakeClient())
    monkeypatch.setenv("FLX_LLM_CACHE", "0")
    llm_gateway.chat("m", "s", "u")
    llm_gateway.chat("m", "s", "u")
    assert c.calls == 2


def test_retries_then_raises(env, monkeypatch):
    c = _use(monkeypatch, FakeClient(raise_exc=_rate_limit_error()))
    monkeypatch.setenv("FLX_LLM_MAX_RETRIES", "2")
    with pytest.raises(llm_gateway.LLMUnavailable):
        llm_gateway.chat("m", "s", "u")
    assert c.calls == 3
    assert not list((env / "cache").glob("*.json"))


def test_empty_response_not_cached(env, monkeypatch):
    _use(monkeypatch, FakeClient(content=None))
    with pytest.raises(llm_gateway.LLMEmptyResponse):
        llm_gateway.chat("m", "s", "u")
    assert not list((env / "cache").glob("*.json"))


def test_log_records_tokens(env, monkeypatch):
    _use(monkeypatch, FakeClient(usage=(11, 7)))
    llm_gateway.chat("m", "s", "u", 0.3)
    rec = _log(env)[0]
    assert (rec["prompt_tokens"], rec["completion_tokens"], rec["error"]) == (11, 7, None)
    assert rec["model"] == "m" and rec["temperature"] == 0.3 and rec["run_id"] == "default"


def test_log_records_served_model(env, monkeypatch):
    _use(monkeypatch, FakeClient())
    llm_gateway.chat("m", "s", "u")
    llm_gateway.chat("m", "s", "u")
    assert [r["served_model"] for r in _log(env)] == ["served-m", "served-m"]


def test_client_timeout_from_env(monkeypatch):
    seen = {}
    monkeypatch.setattr(llm_gateway.openai, "OpenAI", lambda **kw: seen.update(kw) or object())
    monkeypatch.delenv("FLX_LLM_TIMEOUT", raising=False)
    llm_gateway._client()
    assert seen["timeout"] == 600
    monkeypatch.setenv("FLX_LLM_TIMEOUT", "900")
    llm_gateway._client()
    assert seen["timeout"] == 900
