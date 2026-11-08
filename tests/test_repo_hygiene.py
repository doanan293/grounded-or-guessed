import subprocess


def _tracked():
    out = subprocess.run(["git", "ls-files"], capture_output=True, text=True, check=True).stdout
    return out.split()


def test_no_secrets_tracked():
    files = _tracked()
    assert ".env" not in files
    assert "infra/proxy/config.yaml" not in files  # holds proxy API keys
    assert not any(f.startswith("runs/") for f in files)
    assert not any(f.endswith(".json") and "cli-proxy-api" in f for f in files)
