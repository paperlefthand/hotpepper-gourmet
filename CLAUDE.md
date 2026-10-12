@AGENTS.md

## Claude Code 固有の運用

プロジェクト共通の規約は上記 `AGENTS.md` が正本です. ここには Claude Code の仕組みに関する導線のみを置きます.

- **作業の進め方**: 複数ファイルにまたがる機能追加・変更は Plan モードでプランを提示し, 承認を得てから実装します. 完了条件とテスト方針をプランに含めてください.
- **自動セルフチェック (Hook)**: `.claude/settings.json` に登録済みです. 手動で同じコマンドを繰り返す必要はありません.
  - Python ファイルの編集時: `ruff format` と `ruff check --fix` を自動実行します.
  - ターン終了時: `src/` か `tests/` に未コミットの変更があれば, `ruff check`, `ty check`, `pytest` を実行し, 失敗した場合は停止せずに修正を求めます.
- **層別ルール (Skill)**: 該当ファイルの作業時に自動で読み込まれます.
  - `src/pygourmet/**/*.py` → `.claude/skills/source-code/SKILL.md`
  - `tests/**/*.py` → `.claude/skills/tests/SKILL.md`
