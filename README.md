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

___

Powered by [ホットペッパー Webサービス](http://webservice.recruit.co.jp/)
