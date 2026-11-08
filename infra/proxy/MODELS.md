# Models available through the project proxy

Checked 2026-11-08 against `cli-proxy-api` v8.0.28 (`scripts/proxy_smoke.py`).

## Chosen models

| Role | Model id | Why |
|---|---|---|
| Main (RQ1b, RQ2) | `gemini-3.8-flash-high` | Strongest Gemini the proxy offers; no Gemini Pro id is available (paper used `gemini-2.5-pro`) |
| Light Gemini (RQ3c) | `gemini-3.5-flash-lite` | Small/cheap end of the same family |
| Claude (RQ3c, main Claude) | `claude-sonnet-5-5` | Newest Sonnet; chosen by the project owner |
| Claude reproduction check (RQ1b, small subset only) | `claude-sonnet-4-6` | Same model as the SemLoc paper, to separate model drift from method |
| GPT flagship (RQ3c) | `gpt-6-luna` | Newest luna; 3 free Codex accounts (round-robin). `gpt-5.6-luna` also offered |
| OpenAI open-weight (RQ3c) | `gpt-oss-120b-medium` | OpenAI open-weight model via Antigravity: no Codex login, shares the 3 Antigravity quotas, re-runnable by anyone. Not a flagship GPT: claims stay "an open 120B model" |

## All ids offered (2026-11-08)

claude-3-5-haiku-20241022, claude-3-7-sonnet-20250219, claude-fable-5, claude-fable-5-1,
claude-haiku-4-5-20251001, claude-haiku-5-5, claude-opus-4-1-20250805, claude-opus-4-20250514,
claude-opus-4-5-20251101, claude-opus-4-6, claude-opus-4-6-thinking, claude-opus-4-7, claude-opus-4-8,
claude-opus-5, claude-opus-5-5, claude-sonnet-4-20250514, claude-sonnet-4-5-20250929, claude-sonnet-4-6,
claude-sonnet-5, claude-sonnet-5-5, gemini-3-flash, gemini-3.1-flash-image, gemini-3.1-flash-lite,
gemini-3.5-flash-lite, gemini-3.8-flash-high, gpt-oss-120b-medium

## Quota probe (`scripts/quota_probe.py --n 40`, sequential, no retries)

| Model | OK / 40 | 429 | Median latency | Calls/min (sequential) |
|---|---|---|---|---|
| gemini-3.8-flash-high | 40 | 0 | 2.49 s | 23.8 |
| claude-sonnet-4-6 | 40 | 0 | 1.17 s | 45.7 |
| gpt-6-luna | 40 | 0 | 1.43 s | 35.3 |

Sequential calls hit no rate limit. Parallel throughput (WORKERS) is measured in the Task 8 smoke run.

## Adding Codex (GPT) logins

Run once per free Codex account, by the account owner, with the proxy up:

    docker compose -f infra/proxy/compose.yaml exec cli-proxy-api ./CLIProxyAPI -codex-device-login

then `docker compose -f infra/proxy/compose.yaml restart` and re-run `scripts/proxy_smoke.py`.

## Accounts (2026-11-08, re-checked after adding logins)

- Antigravity (Gemini, gpt-oss): 4 — all 4 auth indexes served calls
- Claude: 1 — works; one transient IPv6 "network is unreachable" 500 to api.anthropic.com, retried OK
- Codex free (luna): 4 — 8/8 calls OK under round-robin

## Upstream model substitution

Antigravity serves `gemini-3.8-flash-high` with upstream model **`gemini-3.8-flash-n`** on every call
(proxy warning `upstream served model ...`). `-high` is a proxy alias: the base Gemini 3.8 Flash model
with a high thinking level injected by the proxy, not a different model. Report it as "Gemini 3.8 Flash
(upstream `gemini-3.8-flash-n`, high thinking level via proxy alias)". Whether the thinking level is
honoured is unverified (no separate thinking-token count). The gateway logs `served_model` per call. Claude, luna and
gpt-oss report the requested id.

Per-minute limits were not hit. 5-hour / daily caps are unknown; measure from runs/llm_log.jsonl during the Task 8 pilot.
Estimated total for the whole study: ~12,000 calls (~9,000 Gemini, ~750 per other model).
