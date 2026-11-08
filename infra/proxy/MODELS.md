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
(upstream `gemini-3.8-flash-n`, high thinking level via proxy alias)". **vipharmind's proxy config pinned
`gemini-3.8-flash-high*` to `thinkingLevel: low`** and overrides the client's `reasoning_effort`
(measured: 22–70 reasoning tokens on a bug-finding prompt at any requested effort). Since 2026-11-08
the flx proxy mounts its own git-ignored `infra/proxy/config.yaml` (copy of vipharmind's) with that
rule set to **`medium`** (project owner's choice): reasoning tokens on the same prompt rose to 62–195
(mean ≈144 vs ≈42). The dev pilot run `pilot_dev_r1` used **low**; it is re-run as
`pilot_dev_r1_medium`. The gateway logs `served_model` per call. Claude, luna and
gpt-oss report the requested id.

Per-minute limits were not hit. 5-hour / daily caps are unknown; measure from runs/llm_log.jsonl during the Task 8 pilot.
Estimated total for the whole study: ~12,000 calls (~9,000 Gemini, ~750 per other model).

## Reasoning level actually used (measured 2026-11-08, all models at provider default)

Policy (project owner): **no forced reasoning level** — every model runs at its provider default
through the proxy (the vipharmind rules for `gemini-3.8-flash-high*` and `gemini-3.5-flash*` are
removed in `infra/proxy/config.yaml`). Raw measurements: `data/reasoning/`.

| Model (requested id) | Served id | Default behaviour measured | Report as |
|---|---|---|---|
| gemini-3.8-flash-high | gemini-3.8-flash-n | Short prompts: 139 / 539 reasoning tokens, between forced low (42 / 425) and medium (152 / 597), far below high (886 / 1350). SemLoc prompts: median 3,451 output tokens, median 27 s, up to 478 s → **dynamic thinking** | "Gemini 3.8 Flash, provider-default (dynamic) thinking" |
| gemini-3.5-flash-lite | gemini-3.5-flash-lite | 13–14 output tokens, no reasoning tokens; forced high → ~940 | "thinking off by default" |
| claude-sonnet-5-5 / claude-sonnet-4-6 | same | 68–96 output tokens, no thinking reported; `reasoning_effort=high` raises output (Sonnet 4.6: ~250) | "extended thinking not enabled (Anthropic default)" |
| gpt-6-luna | gpt-6-luna | 44 / 30 reasoning tokens vs low 0 / 0, medium 32 / 30, high 59 / 41 | "default reasoning effort (≈ medium)" |
| gpt-oss-120b-medium | gpt-oss-120b-medium | 217–240 output tokens; `reasoning_effort` changes little (low ~177, high ~226); occasional 300 s first-call latency | "gpt-oss-120b, proxy alias `-medium`, default effort" |

Consequence: the LLM timeout is 600 s (`FLX_LLM_TIMEOUT`); at 120 s, 6 of 84 SemLoc calls with
default Gemini thinking timed out.
