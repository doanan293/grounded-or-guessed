"""Refuse to publish credentials: patterns for API keys, bearer tokens, JWTs and e-mail addresses."""
import re

PATTERNS = {
    "anthropic": r"sk-ant-[A-Za-z0-9_-]{20,}",
    "openai": r"sk-(?!ant-)(?:proj-)?[A-Za-z0-9_-]{32,}",
    "google": r"AIza[0-9A-Za-z_-]{35}",
    "github": r"gh[pousr]_[A-Za-z0-9]{30,}",
    "bearer": r"Bearer\s+[A-Za-z0-9._~+/=-]{20,}",
    "jwt": r"eyJ[A-Za-z0-9_-]{8,}\.eyJ[A-Za-z0-9_-]{8,}\.[A-Za-z0-9_-]{8,}",
    "email": r"[A-Za-z0-9._%+-]+@[A-Za-z0-9.-]+\.[A-Za-z]{2,}",
}
_COMPILED = {k: re.compile(v) for k, v in PATTERNS.items()}


def scan(text: str) -> list[str]:
    return [name for name, rx in _COMPILED.items() if rx.search(text)]
