# hotpepper-gourmet

[![PyPI version](https://badge.fury.io/py/hotpepper-gourmet.svg)](https://badge.fury.io/py/hotpepper-gourmet)
![workflow badge](https://github.com/paperlefthand/hotpepper-gourmet/actions/workflows/ci.yml/badge.svg)
![workflow badge](https://github.com/paperlefthand/hotpepper-gourmet/actions/workflows/publish.yml/badge.svg)

## About

[ホットペッパーグルメAPI](https://webservice.recruit.co.jp/doc/hotpepper/reference.html)のシンプルなクライアントライブラリです

## How To Use

### keyidの取得

ホットペッパーグルメAPIに登録し, token(keyid)を取得

### サンプルコード

同期版

```python
>>> from pygourmet import Api, Option
>>> api = Api(keyid=YOUR_KEYID)
>>> option = Option(lat=35.170915, lng=136.8793482, keyword="ラーメン", range=4, count=3)
>>> shops = api.search(option)
>>> len(shops)
3
>>> shops[0].name
'shop name'
```

非同期版

```python
async def call_search_async():
    shops = await api.search_async(option=option)
    print(len(shops))

loop = asyncio.get_event_loop()
loop.run_until_complete(call_search_async())
```

## 開発者向けガイド

このリポジトリは [uv](https://docs.astral.sh/uv/) によるパッケージ管理を採用しています.
Python バージョンは 3.12, 3.13, 3.14 をサポート対象としています.

### セットアップ

```bash
# 依存関係のインストール（開発環境構築）
uv sync
```

### よく使うコマンド

原則として `uv run` を介して実行します.

```bash
# テスト実行
uv run pytest -v

# 統合テスト実行（要 HOTPEPPER_KEYID 環境変数）
# ローカル環境でのみ実行し、APIキーを利用して実際にリクエストを送ります
uv run pytest --run-integration

# 静的型チェック
uv run ty check

# Lint チェック
uv run ruff check .

# コードフォーマット適用
uv run ruff format .

# コミット前チェック（Lint/Format/TypeCheck 等を一括実行）
uv run prek

# API ドキュメント生成
uv run pdoc src/pygourmet

# 特定バージョンの動作確認（tox）
uv run tox -e py314
```

### コーディング規約

- **Style**: Ruff 準拠 (4スペースインデント, ダブルクォート, スネークケース). クラス名は PascalCase.
- **Docstring**: Google Style.
- **Type**: Pydantic v2 を活用し, `Any` を排除した厳格な型注釈を行う.

### テストガイドライン

- **基本**: `pytest` + `pytest-httpx` (モック).
- **統合テスト**: `@pytest.mark.integration` を付与. `uv run pytest --run-integration` でのみ実行される.
- **非同期**: `pytest-asyncio` を使用.

### コミット・PRガイドライン

- コミットメッセージは **Conventional Commits** 形式.
- コミット前に必ず `uv run prek` をパスさせること.
- PR には変更の目的, テスト結果, ドキュメント更新の有無を記載.

### CI/CD

- **CI**: GitHub Actions + `tox-uv` (Python 3.12, 3.13, 3.14).
- **TestPyPI**: `dev` ブランチへの push で自動デプロイ.
- **PyPI / Docs**: `v*` タグ (例: `v1.0.0`) の push で本番リリースおよび GitHub Pages 更新.

### セキュリティ

- API Key (`HOTPEPPER_KEYID`) は絶対コミットしない.
- ローカル開発では `.env` を利用する (`python-dotenv` 対応).

___

Powered by [ホットペッパー Webサービス](http://webservice.recruit.co.jp/)
