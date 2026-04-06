# プロジェクト: pygourmet

あなたは Python 開発者として, `pygourmet` ライブラリ ([Hotpepper Gourmet API](https://webservice.recruit.co.jp/doc/hotpepper/reference.html) のラッパー) の開発を支援しています. あなたの目標は, 高品質で型安全かつ最新の Python コードを維持することです.

**API 仕様参照先**: 実装・修正時は必ず [ホットペッパーグルメ API リファレンス](https://webservice.recruit.co.jp/doc/hotpepper/reference.html) を確認してください.

## プロジェクト構造とモジュール構成

- ライブラリコードは `src/pygourmet/` 配下に配置されています. `client.py` (API ラッパー), `option.py` (リクエストパラメータ), `shop.py` (レスポンスモデル) などのモジュールで構成されます. 外部への公開インポートは `src/pygourmet/__init__.py` で再エクスポートされます.
- テストは `tests/` 配下に配置し, 再利用可能なフィクスチャは `tests/conftest.py` に, サンプルデータは `tests/data/` に集約してください.
- 型情報を提供するための `py.typed` を同梱しています. 既存のパッケージレイアウトを維持するため, 新規モジュールは必ず `src/pygourmet/` 以下に配置してください.
- プロジェクト全体の設定は `pyproject.toml` で管理しています. ビルドシステム (`hatchling-vcs`), 依存関係, pytest 設定 (`[tool.pytest.ini_options]`), ruff 設定 (`[tool.ruff]`) がここに集約されています.

## ビルド, テスト, 開発コマンド

原則として `uv` を介して実行します. 推奨開発 Python バージョンは **3.14** です.

- `uv sync`: ローカル開発環境の構築と依存関係の同期.
- `uv run pytest -v`: テストスイートの実行.
- `uv run pytest tests/test_client.py::test_search_位置指定 --run-integration`: 特定テストの単体実行（統合テストは `--run-integration` が必要）.
- `uv run pytest --run-integration`: 統合テスト(integration マーカー)を含めることで本番APIと連携するテストスイートを実行します. 通常の pytest 実行時には統合テストはスキップされます.
- `uv run ty check`: 静的型チェックの実行.
- `uv run ruff check .`: Lint の実行.
- `uv run ruff format .`: コードフォーマットの適用.
- `uv run prek`: コミット前の整合性チェック (Lint/Format 含む).
- `uv run pdoc src/pygourmet`: API ドキュメントの生成.
- `uv run tox -e py314`: 特定の Python バージョンでの CI 動作のシミュレーション.

## コーディングスタイルと命名規則

- **Ruff の準拠**: 4 スペースインデント, ダブルクォート, スネークケースを採用します. クラス名は PascalCase を維持してください.
- **Docstring**: Google Style に準拠し, `pdoc` で適切にレンダリングされるように記述してください.
- **型定義**: Pydantic v2 を活用し, `Any` を排除した厳格な型注釈を行ってください. 戻り値の型も明示してください. パラメータの型は必ず [API リファレンス](https://webservice.recruit.co.jp/doc/hotpepper/reference.html) と照合して決定してください.

## テストガイドライン

- **基本方針**: テストは `pytest` で記述します. 通常の単体テストでは `pytest-httpx` を用いて API レスポンスをモック化し, ダミーの API キーを使用してください.
- **本番接続テスト**: 本番 API との接続を確認する必要があるテストケースには `@pytest.mark.integration` マーカーを付与してください.
- **テストの実行制御**: 統合テスト(integration)を実行するには, 明示的に `--run-integration` オプションを付与する必要があります. このテストはローカル環境でのみ実行し, `.env` に記載された `HOTPEPPER_KEYID` を利用します. オプションが指定されていない場合や, 環境変数が設定されていない場合は, 自動的にスキップされるように設計してください.
- **非同期処理**: HTTP クライアントには `httpx` を採用しています. httpxの非同期クライアントを使用するテストでは `pytest-asyncio` を利用し, 非同期クライアントを `await` する形式を推奨します.

## ブランチ運用とリリースフロー

- **機能開発**: `feature/*` ブランチを切って実装し, `dev` ブランチへ PR を出してください.
- **CI**: `dev` への PR および `dev` への push 時に GitHub Actions が自動実行されます. Python 3.12, 3.13, 3.14 の 3 バージョンでテストされます.
- **TestPyPI デプロイ**: `dev` ブランチへの push で TestPyPI へ自動デプロイされます.
- **本番リリース**: 管理者が `vMAJOR.MINOR.PATCH` 形式のタグを push した場合のみ, 本番 PyPI へのリリースと GitHub Pages へのドキュメント更新が実行されます.

## コミットおよびプルリクエストのガイドライン

- コミットメッセージは Conventional Commits 形式に従ってください.
- コミット前に必ず `uv run prek` を実行し, チェックをパスさせること.
- PR には, 変更の目的, テストの実行結果, およびドキュメント更新の有無を記載してください.

## セキュリティと構成

- API キー (`HOTPEPPER_KEYID`) をコードに直接記述したり, コミットしたりしないでください.
- ローカル開発では `.env` ファイルを使用し, `python-dotenv` を介して読み込んでください.

## CI/CD ワークフロー

- CI は GitHub Actions で実行され, `tox-uv` を用いて Python 3.12, 3.13, 3.14 でテストされます.
- `dev` ブランチへの push で TestPyPI へ自動デプロイされます.
- バージョン管理は `hatchling-vcs` を使用し, Git タグ (`vMAJOR.MINOR.PATCH`) から取得します.
- 管理者が `v*` 形式のタグを push した場合のみ, 本番 PyPI へのリリースと GitHub Pages へのドキュメント更新が実行されます.
