# pygourmet

[ホットペッパーグルメ API](https://webservice.recruit.co.jp/doc/hotpepper/reference.html) の Python クライアントライブラリです.

このファイルは, 人間と AI エージェント (Claude Code, Codex, Copilot など) に共通する開発規約です. 特定のツールに依存する設定や手順はここに書きません.

層ごとの詳細な規約は次のファイルにあります. 自動で読み込まれるかはツールによって異なるため, 該当するディレクトリのファイルを変更する前に必ず読んでください.

- `src/AGENTS.md`: ライブラリコード (`src/pygourmet/`) の実装規約
- `tests/AGENTS.md`: テスト (`tests/`) の作成規約

## プロダクト方針

- **対象ユーザー**: ホットペッパーグルメ API をアプリケーションに組み込みたい Python 開発者, および店舗データを手軽に取得したいデータ分析者.
- **開発者体験 (DX)**: Pydantic v2 による厳格な型付けと, `pdoc` で読める日本語ドキュメントを提供する.
- **同期/非同期の両対応**: `httpx` を用いた同期 (`search`) と非同期 (`search_async`) の両 API を常に同等の機能で提供する.
- **API への忠実さ**: モデル名・パラメータ名は公式 API に揃え, API 利用経験者の認知負荷を下げる. 実装・修正時は必ず [API リファレンス](https://webservice.recruit.co.jp/doc/hotpepper/reference.html) を確認する.

## プロジェクト構造

- ライブラリコードは `src/pygourmet/` に置きます. 公開 API は `__init__.py` で再エクスポートします.
- テストは `tests/` に置き, 共通フィクスチャは `tests/conftest.py`, API レスポンスのサンプルは `tests/data/` に置きます.
- プロジェクト設定は `pyproject.toml` に集約しています (ビルド: `uv_build`, 依存関係, pytest, ruff).

## 開発コマンド

原則として `uv` を介して実行します. 推奨開発 Python バージョンは **3.14** (`.python-version`) です.

| 操作 | コマンド |
| --- | --- |
| 環境構築・依存同期 | `uv sync` |
| テスト | `uv run pytest` |
| 統合テスト込み | `uv run pytest --run-integration` |
| 型チェック | `uv run ty check` |
| Lint | `uv run ruff check .` |
| フォーマット | `uv run ruff format .` |
| コミット前チェック | `uv run prek run --all-files` |
| API ドキュメント生成 | `uv run pdoc src/pygourmet` |
| CI 相当の検証 | `uvx --with tox-uv tox -e lint,format,type,py3.14` |

## 作業の進め方

- 複数ファイルにまたがる機能追加・変更は, 実装の前に方針 (変更するファイル, 完了条件, テスト方針) を提示し, 承認を得てから着手します.
- 変更には必ずテストを付けます.

## コーディング規約

- **スタイル**: Ruff の設定が唯一の基準です. 関数・変数はスネークケース, クラスは PascalCase.
- **型**: Pydantic v2 を活用し, `Any` を使わない厳格な型注釈を行います. 戻り値の型も必ず明示します.
- **Docstring**: 公開クラス・メソッドには日本語の Google Style docstring を書きます.
- **後方互換性**: 公開 API (`Api`, `Option`, `Shop`, `SearchError`) の削除・リネーム・必須引数の追加は破壊的変更です. 意図的な場合のみ行い, 実施前に確認を取ります.

## コミットと PR

- PR は Squash マージされ, **PR タイトルがそのまま `main` のコミットメッセージとリリースノートの項目になります.** PR タイトルは [Conventional Commits](https://www.conventionalcommits.org/ja/v1.0.0/) 形式 (`<type>(<scope>): <要約>`) で書きます. 破壊的変更には `!` を付けます (例: `feat(option)!: ...`).
- コミット前に `uv run prek run --all-files`, `uv run ty check`, `uv run pytest` をパスさせます.
- PR は `.github/pull_request_template.md` に沿って記載します.

## してはいけないこと

- API キー (`HOTPEPPER_KEYID`) や `.env` の内容をコード・テスト・ログ・コミットに含めない. ローカルでは `.env` に記載し, `python-dotenv` で読み込みます.
- タグを作成・push しない (リリースはメンテナーが行います).
- `pyproject.toml` の `version` (ダミー値 `0.0.0`) を変更しない.
- `.github/workflows/actions.lock` を手で編集しない. ワークフローの `uses:` を変更する場合は `gh actions-lock` で再生成します.
- 依存関係のクールダウン日数 (`exclude-newer` など) を変更しない.
- `CLAUDE.md` や `CLAUDE.local.md` を作らない (どの階層にも). 規約は AGENTS.md に書きます. Claude Code はこれらがあると AGENTS.md を読まなくなるため, CI でも拒否します.

CI/CD・リリース・依存関係更新の仕組みはメンテナー向けの `MAINTAINING.md` にあります.
