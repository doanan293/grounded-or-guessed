# Models available through the project proxy

Checked 2026-11-08 against `cli-proxy-api` v8.0.28 (`scripts/proxy_smoke.py`).

## Chosen models

| Role | Model id | Why |
|---|---|---|
| Main (RQ1b, RQ2) | `gemini-3.8-flash-high` | Strongest Gemini the proxy offers; no Gemini Pro id is available (paper used `gemini-2.5-pro`) |
| Light Gemini (RQ3c) | `gemini-3.5-flash-lite` | Small/cheap end of the same family |
| Claude (RQ3c, RQ1b cross-check) | `claude-sonnet-4-6` | Same model as the SemLoc paper |
| GPT (RQ3c, optional) | pending Codex login | `gpt-oss-120b-medium` also answers via Antigravity |

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

Sequential calls hit no rate limit. Parallel throughput (WORKERS) is measured in the Task 8 smoke run.

## Adding the Codex (GPT) login

Run once, by the account owner, with the proxy up:

    docker compose -f infra/proxy/compose.yaml exec cli-proxy-api ./CLIProxyAPI -codex-device-login

then `docker compose -f infra/proxy/compose.yaml restart` and re-run `scripts/proxy_smoke.py`.
