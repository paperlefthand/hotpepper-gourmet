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

このリポジトリは[uv](https://docs.astral.sh/uv/)によるパッケージ管理, [tox-uv](https://github.com/tox-dev/tox-uv)によるタスク統一,
[ruff](https://docs.astral.sh/ruff/)によるLint/フォーマット, [ty](https://docs.astral.sh/ty/)による型チェックを利用しています.

### セットアップ

```bash
# 依存関係をインストール（開発＋テスト＋ドキュメント用）
uv sync --group dev --group test --group doc

# tox / tox-uv が未インストールなら
uv tool install tox --with tox-uv

# pre-commit フックを有効化（推奨）
uv run pre-commit install
```

vscode利用者は`.vscode/settings.example.json`を参考に`.vscode/settings.json`を作成すると後述のlintやformatを自動化できます.

### よく使うコマンド

```bash
# Lint チェック（ruff）
tox -e lint

# 自動整形（ruff --fix + ruff format）
tox -e format

# 型チェック（ty）
tox -e type

# テスト（pytest, Python 3.11/3.12/3.13 対応）
tox -e py311
tox -e py312
tox -e py313
# まとめて実行
tox -e py311,py312,py313

# ドキュメントビルド（Sphinx）
tox -e docs
```

### コード品質（pre-commit）

コミットメッセージは[Conventional Commits](https://www.conventionalcommits.org/ja/v1.0.0/#%e6%a6%82%e8%a6%81)に準拠してください

コミット前に以下が自動実行されます:

- ruff lint & format
- ty (型チェック)
- 簡易的なクリーンチェック（YAML, 改行, 秘密鍵検出など）

初回のみ以下を実行してください:

```bash
uv run pre-commit install
```

全ファイルを対象に走らせる場合:

```bash
uv run pre-commit run --all-files
```

### CI の動作（GitHub Actions）

- Python 3.13
  - Lint / Format / Type / Docs を実行
- Python 3.11 / 3.12 / 3.13
  - pytest を実行（マトリクス）

CI が green = ローカルで tox が通る状態と一致します。

### 開発フロー

#### 開発者（Contributor）

1. `uv sync --group dev --group test --group doc`
1. コーディング → `tox -e format` で自動整形
1. PR 前に `tox -e lint,format,type,py311,py312,py313,docs`
1. PR 作成

#### 承認者（Reviewer）

1. CI が全て green であることを確認
1. 必要に応じてローカルで `tox -e py311,py312,py313` を再現
1. ドキュメント差分を `tox -e docs` で確認

___

Powered by [ホットペッパー Webサービス](http://webservice.recruit.co.jp/)
