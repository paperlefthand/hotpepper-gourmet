# hotpepper-gourmet

[![PyPI version](https://img.shields.io/pypi/v/hotpepper-gourmet)](https://pypi.org/p/hotpepper-gourmet)
[![Python versions](https://img.shields.io/pypi/pyversions/hotpepper-gourmet)](https://pypi.org/p/hotpepper-gourmet)
[![CI](https://github.com/paperlefthand/hotpepper-gourmet/actions/workflows/ci.yml/badge.svg?branch=main)](https://github.com/paperlefthand/hotpepper-gourmet/actions/workflows/ci.yml)
[![License: MIT](https://img.shields.io/badge/license-MIT-blue)](https://github.com/paperlefthand/hotpepper-gourmet/blob/main/LICENSE.txt)

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

## コントリビューション

バグ報告・機能要望・Pull Request を歓迎します. 開発環境の構築方法や PR の出し方は [CONTRIBUTING.md](https://github.com/paperlefthand/hotpepper-gourmet/blob/main/CONTRIBUTING.md) を参照してください.

- 変更履歴: [GitHub Releases](https://github.com/paperlefthand/hotpepper-gourmet/releases)
- 行動規範: [CODE_OF_CONDUCT.md](https://github.com/paperlefthand/hotpepper-gourmet/blob/main/CODE_OF_CONDUCT.md)
- 脆弱性の報告: [SECURITY.md](https://github.com/paperlefthand/hotpepper-gourmet/blob/main/SECURITY.md)

## License

[MIT License](https://github.com/paperlefthand/hotpepper-gourmet/blob/main/LICENSE.txt)

___

Powered by [ホットペッパー Webサービス](http://webservice.recruit.co.jp/)
