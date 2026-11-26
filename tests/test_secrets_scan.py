from flx.secrets_scan import scan


def test_secret_scan_flags_keys_and_emails():
    cases = {
        "openai": "key=sk-proj-" + "a" * 40,
        "anthropic": "sk-ant-api03-" + "b" * 40,
        "google": "AIza" + "c" * 35,
        "github": "ghp_" + "d" * 36,
        "bearer": "Authorization: Bearer " + "e" * 30,
        "email": "contact someone.name@example.org please",
        "jwt": "eyJhbGciOiJIUzI1NiJ9.eyJzdWIiOiIxIn0.abcdefghijklmnop",
    }
    for name, text in cases.items():
        assert name in scan(text), name


def test_secret_scan_passes_ordinary_llm_output():
    assert scan('{"lines": [62, 66, 70]} The fault is `max_norm / (norm + 1)`; use task-start and sk-learn.') == []
