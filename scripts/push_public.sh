#!/usr/bin/env bash
# Push a local branch to the public repo as GitHub user doanan293, whichever gh account is active.
# The token is read from gh at run time and passed as a one-off HTTP header (never stored).
#   scripts/push_public.sh [branch] [target]   (defaults: current branch -> main)
set -euo pipefail
BRANCH="${1:-$(git rev-parse --abbrev-ref HEAD)}"
TARGET="${2:-main}"
TOKEN="$(gh auth token --hostname github.com --user doanan293)"
AUTH="$(printf 'x-access-token:%s' "$TOKEN" | base64 -w0)"
GIT_ASKPASS= git -c credential.helper= -c "http.https://github.com/.extraheader=AUTHORIZATION: basic $AUTH" \
    push origin "$BRANCH:$TARGET"
