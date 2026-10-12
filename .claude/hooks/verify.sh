#!/usr/bin/env bash
# Stop hook: src/ か tests/ に変更がある場合のみ, ruff/ty/pytest の
# セルフチェックゲートを実行する. 失敗したら停止をブロックして Claude に返す.
set -uo pipefail

input=$(cat)

# stop hook 起因の継続中は再実行しない (無限ループ防止).
active=$(printf '%s' "$input" | jq -r '.stop_hook_active // false')
[ "$active" = "true" ] && exit 0

cd "${CLAUDE_PROJECT_DIR:-.}" || exit 0

# src/ か tests/ に未コミット変更が無ければ何もしない (調査・雑談セッション).
if [ -z "$(git status --porcelain -- src/ tests/ 2>/dev/null)" ]; then
  exit 0
fi

fail=0
report=""

run() {
  local label="$1"; shift
  local out
  if ! out=$("$@" 2>&1); then
    fail=1
    report+="### ${label} 失敗"$'\n'"${out}"$'\n\n'
  fi
}

# CI (tox.ini) と同じ対象に揃える.
run "ruff check" uv run ruff check src/ tests/
run "ruff format" uv run ruff format --check src/ tests/
run "ty check" uv run ty check src/pygourmet
run "pytest" uv run pytest

if [ "$fail" -ne 0 ]; then
  {
    echo "セルフチェック (ruff/ty/pytest) に失敗しました. 修正してください:"
    printf '%s' "$report"
  } >&2
  exit 2
fi

exit 0
