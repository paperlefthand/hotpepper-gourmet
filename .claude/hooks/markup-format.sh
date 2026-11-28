#!/usr/bin/env bash
# PostToolUse hook: 編集/作成された Markdown を rumdl で, TOML を tombi で自動整形し,
# 自動修正できない問題があれば Claude にフィードバックする.
set -uo pipefail

input=$(cat)
file=$(printf '%s' "$input" | jq -r '.tool_input.file_path // empty')
[ -n "$file" ] && [ -f "$file" ] || exit 0

project_dir="${CLAUDE_PROJECT_DIR:-$(pwd)}"
cd "$project_dir" || exit 0

# プロジェクト外のファイル (メモリ等) は対象外.
case "$(realpath "$file")" in
  "$(realpath "$project_dir")"/*) ;;
  *) exit 0 ;;
esac

report() {
  {
    echo "$1 で自動修正できない問題が残っています: $file"
    echo "$2"
  } >&2
  exit 2
}

case "$file" in
  *.md)
    uv run rumdl fmt --silent "$file" >/dev/null 2>&1 || true
    out=$(uv run rumdl check --color never "$file" 2>&1) || report "rumdl check" "$out"
    ;;
  *.toml)
    # 構文エラー等で整形に失敗しても, 後段の lint で内容を報告する.
    uv run tombi format --quiet "$file" >/dev/null 2>&1 || true
    out=$(NO_COLOR=1 uv run tombi lint "$file" 2>&1) || report "tombi lint" "$out"
    ;;
esac

exit 0
