# プロジェクト: pygourmet

あなたは Python 開発者として, `pygourmet` ライブラリ ([ホットペッパーグルメ API](https://webservice.recruit.co.jp/doc/hotpepper/reference.html) のクライアント) の開発を支援しています. 目標は, 高品質で型安全かつ最新の Python コードを維持することです.

このファイルは AI エージェント共通の唯一の指示書です. ツール固有の設定 (Claude Code の Hook / Skill など) は各ツールの設定ディレクトリに置き, ここには全エージェントに共通する事実と規約のみを記載します.

## プロダクト方針

- **対象ユーザー**: ホットペッパーグルメ API をアプリケーションに組み込みたい Python 開発者, および店舗データを手軽に取得したいデータ分析者.
- **開発者体験 (DX)**: Pydantic v2 による厳格な型付けと, `pdoc` で読める日本語ドキュメントを提供する.
- **同期/非同期の両対応**: `httpx` を用いた同期 (`search`) と非同期 (`search_async`) の両 API を常に同等の機能で提供する.
- **API への忠実さ**: モデル名・パラメータ名は公式 API に揃え, API 利用経験者の認知負荷を下げる. 実装・修正時は必ず [API リファレンス](https://webservice.recruit.co.jp/doc/hotpepper/reference.html) を確認すること.

## プロジェクト構造

- ライブラリコードは `src/pygourmet/` 配下に配置します. 新規モジュールも必ずここに置いてください.
  - `client.py`: API クライアント (`Api`)
  - `option.py`: リクエストパラメータ (`Option`)
  - `shop.py`: レスポンスモデル (`Shop` と入れ子モデル)
  - `errors.py`: 例外 (`SearchError`)
  - `__init__.py`: 公開 API の再エクスポート
  - `py.typed`: 型情報の同梱マーカー
- テストは `tests/` 配下に配置し, 共通フィクスチャは `tests/conftest.py`, API レスポンスのサンプルは `tests/data/` に置きます.
- プロジェクト設定は `pyproject.toml` に集約しています (ビルド: `hatchling` + `hatch-vcs`, 依存関係, pytest, ruff).

## 開発コマンド

原則として `uv` を介して実行します. 推奨開発 Python バージョンは **3.14** (`.python-version`) です.

| 操作 | コマンド |
| --- | --- |
| 環境構築・依存同期 | `uv sync` |
| テスト | `uv run pytest` |
| 統合テスト込み | `uv run pytest --run-integration` |
| 特定テストのみ | `uv run pytest tests/test_client.py::test_search_位置指定 --run-integration` |
| 型チェック | `uv run ty check` |
| Lint | `uv run ruff check .` |
| フォーマット | `uv run ruff format .` |
| コミット前チェック (ruff check/format) | `uv run prek run --all-files` |
| API ドキュメント生成 | `uv run pdoc src/pygourmet` |
| CI 相当の検証 | `uv run tox -e lint,type,py3.14` |

## コーディング規約

- **スタイル**: Ruff の設定が唯一の基準です (4 スペースインデント, ダブルクォート). 関数・変数はスネークケース, クラスは PascalCase.
- **型**: Pydantic v2 を活用し, `Any` を使わない厳格な型注釈を行います. 戻り値の型も必ず明示します. パラメータやフィールドの型は API リファレンスと照合して決定します.
- **Docstring**: 公開クラス・メソッドには日本語の Google Style docstring を書き, `pdoc` で正しくレンダリングされるようにします.
- **後方互換性**: 公開 API (`Api`, `Option`, `Shop`, `SearchError`) のシグネチャ変更は破壊的変更として扱い, 意図的な場合のみ行います.

## テスト

- テストは `pytest` で記述します. 単体テストでは `pytest-httpx` で API レスポンスをモックし, ダミーの API キー (`client_dummy` フィクスチャ) を使います.
- 本番 API に接続するテストには `@pytest.mark.integration` を付与します. `--run-integration` 指定時のみ実行され, `.env` の `HOTPEPPER_KEYID` が未設定ならスキップされるようにします. CI では `integration.yml` が毎週本番 API に対して実行し, 失敗すると `api-change` Issue を起票します. PR の CI では実行されません.
- 非同期 API のテストは `pytest-asyncio` を使い, `await` で呼び出します.
- 新しいコードのカバレッジは 80% 以上を目安とします (`uv run pytest --cov=pygourmet`).

## ブランチ運用と CI/CD

GitHub Flow を採用しています. 人間向けの詳細は `CONTRIBUTING.md` (コントリビューター) と `MAINTAINING.md` (メンテナー) にあります.

- **機能開発**: `main` から作業ブランチを切り, `main` へ PR を出します. 長期の開発ブランチはありません.
- **CI**: `main` への PR / push で `ci.yml` が実行されます. `tox-uv` で lint・format・型チェックと, Python 3.12 / 3.13 / 3.14 のテストを行います. ブランチ保護の必須チェックは `ci-success` と `pr-title` です.
- **TestPyPI**: `main` への push で CI が成功すると, 開発版が自動デプロイされます.
- **本番リリース**: 管理者が `main` 上のコミットに `vMAJOR.MINOR.PATCH` 形式のタグを push した場合のみ実行されます. CI を通した後, PyPI へのリリース, GitHub Release (ノート自動生成), GitHub Pages へのドキュメント更新が行われます. バージョンは `hatch-vcs` によりタグから決定されます. エージェントはタグを作成・push しないでください.
- **依存関係の更新**: Dependabot が毎週 PR を作成します.

## コミットと PR

- PR は Squash マージされ, **PR タイトルがそのまま `main` のコミットメッセージとリリースノートの項目になります.** PR タイトルは [Conventional Commits](https://www.conventionalcommits.org/ja/v1.0.0/) 形式 (`<type>(<scope>): <要約>`) で書きます. CI (`pr-title.yml`) で検査され, 種類に応じたラベルが付きます.
- 公開 API の互換性を壊す変更は, PR タイトルに `!` を付けます (例: `feat(option)!: ...`).
- 個々のコミットメッセージも Conventional Commits 形式に揃えます.
- コミット前に `uv run prek run --all-files`, `uv run ty check`, `uv run pytest` をパスさせます.
- PR は `.github/pull_request_template.md` に沿って, 変更の目的, テスト結果, ドキュメント更新の有無を記載します.

## セキュリティ

- API キー (`HOTPEPPER_KEYID`) をコードに直接記述したり, コミットしたりしないでください.
- ローカル開発では `.env` に記載し, `python-dotenv` で読み込みます.
