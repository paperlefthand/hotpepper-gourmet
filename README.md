# hotpepper-gourmet

[![PyPI version](https://badge.fury.io/py/hotpepper-gourmet.svg)](https://badge.fury.io/py/hotpepper-gourmet)
![workflow badge](https://github.com/paperlefthand/hotpepper-gourmet/actions/workflows/ci.yml/badge.svg)
![workflow badge](https://github.com/paperlefthand/hotpepper-gourmet/actions/workflows/publish.yml/badge.svg)

## About

[ホットペッパーグルメAPI](https://webservice.recruit.co.jp/doc/hotpepper/reference.html)のシンプルで型安全なクライアントライブラリです.

- 同期・非同期の両方の検索 API を提供
- リクエストパラメータ・レスポンスを Pydantic v2 のモデルとして扱える
- API ドキュメント: <https://paperlefthand.github.io/hotpepper-gourmet/>

## Install

```bash
pip install hotpepper-gourmet
# または
uv add hotpepper-gourmet
```

Python 3.12, 3.13, 3.14 をサポートしています.

## How To Use

### keyidの取得

[ホットペッパーWebサービス](https://webservice.recruit.co.jp/)に登録し, APIキー(keyid)を取得してください.

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
import asyncio

from pygourmet import Api, Option


async def main() -> None:
    api = Api(keyid=YOUR_KEYID)
    option = Option(keyword="寿司", count=3)
    shops = await api.search_async(option)
    print(len(shops))


asyncio.run(main())
```

エラー時は `pygourmet.SearchError` が送出されます.

## 開発者向けガイド

このリポジトリは [uv](https://docs.astral.sh/uv/) でパッケージを管理しています.

```bash
uv sync                          # 開発環境の構築
uv run pytest                    # テスト
uv run pytest --run-integration  # 統合テスト (.env に HOTPEPPER_KEYID が必要)
uv run ty check                  # 型チェック
uv run prek run --all-files      # Lint / Format (ruff)
uv run pdoc src/pygourmet        # API ドキュメントのプレビュー
```

コーディング規約, テスト方針, ブランチ運用, リリース手順は [AGENTS.md](AGENTS.md) にまとめています (AI エージェントと人間の共通ガイドです).
機能開発は `dev` から `feature/*` ブランチを切り, `dev` へ PR を出してください.

___

Powered by [ホットペッパー Webサービス](http://webservice.recruit.co.jp/)
