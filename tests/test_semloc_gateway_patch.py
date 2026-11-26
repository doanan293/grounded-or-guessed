import sys
import types

import pytest

from flx import llm_gateway
from flx._semloc import ensure_on_path

ensure_on_path()
import constraint_inference  # noqa: E402
import counterfactual  # noqa: E402
import llm_direct_fl  # noqa: E402


@pytest.fixture
def calls(monkeypatch):
    rec = []

    def fake_chat(model, system, user, temperature=0.0, max_tokens=None):
        rec.append((model, system, user, temperature))
        return "X"

    monkeypatch.setattr(llm_gateway, "chat", fake_chat)
    monkeypatch.setenv("FLX_USE_GATEWAY", "1")
    return rec


def test_constraint_inference_routes_through_gateway(calls):
    assert constraint_inference._query_gemini("P", "gemini-x", 0.8) == "X"
    assert calls == [("gemini-x", constraint_inference._SYSTEM_PROMPT, "P", 0.8)]


def test_claude_and_openai_branches_route_too(calls):
    constraint_inference._query_claude_vertex("P", "claude-x", 0.3)
    constraint_inference._query_openai("P", "gpt-x", 0.0)
    assert [c[0] for c in calls] == ["claude-x", "gpt-x"]


def test_direct_fl_routes(calls):
    assert llm_direct_fl._query_llm("P", "gemini-x", 0.3) == "X"
    assert calls == [("gemini-x", llm_direct_fl._SYSTEM_PROMPT, "P", 0.3)]


def test_counterfactual_routes_temp_zero(calls):
    assert counterfactual._chat_completion("gemini-x", "S", "U") == "X"
    assert calls == [("gemini-x", "S", "U", 0.0)]


def test_gateway_off_keeps_original(monkeypatch):
    monkeypatch.delenv("FLX_USE_GATEWAY", raising=False)
    monkeypatch.setattr(llm_gateway, "chat", lambda *a, **k: pytest.fail("gateway must not be used"))
    used = []

    class StubClient:
        def __init__(self, api_key=None):
            self.models = types.SimpleNamespace(generate_content=self._gen)

        def _gen(self, **kwargs):
            used.append(kwargs["model"])
            return types.SimpleNamespace(text="orig")

    genai = types.ModuleType("google.genai")
    genai.Client = StubClient
    genai.types = types.SimpleNamespace(GenerateContentConfig=lambda **k: k)
    google = types.ModuleType("google")
    google.genai = genai
    monkeypatch.setitem(sys.modules, "google", google)
    monkeypatch.setitem(sys.modules, "google.genai", genai)
    monkeypatch.setitem(sys.modules, "google.genai.types", genai.types)
    monkeypatch.setenv("GEMINI_API_KEY", "k")
    assert constraint_inference._query_gemini("P", "gemini-x", 0.8) == "orig"
    assert used == ["gemini-x"]
