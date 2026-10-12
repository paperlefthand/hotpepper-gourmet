#!/usr/bin/env bash
# PostToolUse hook: 編集/作成された Python ファイルを ruff で自動整形し,
# 自動修正できない lint 問題があれば Claude にフィードバックする.
set -uo pipefail

input=$(cat)
file=$(printf '%s' "$input" | jq -r '.tool_input.file_path // empty')

# Python ファイル以外は対象外.
case "$file" in
  *.py) ;;
  *) exit 0 ;;
esac
[ -f "$file" ] || exit 0

cd "${CLAUDE_PROJECT_DIR:-.}" || exit 0

# 整形 (構文エラー等で失敗しても, 後段の check で内容を報告する).
uv run ruff format "$file" >/dev/null 2>&1 || true

# 自動修正できるものは修正し, 残った問題は stderr で Claude に返す (exit 2).
if ! out=$(uv run ruff check --fix "$file" 2>&1); then
  {
    echo "ruff check で自動修正できない問題が残っています: $file"
    echo "$out"
  } >&2
  exit 2
fi

exit 0
