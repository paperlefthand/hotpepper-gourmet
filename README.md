# hotpepper-gourmet

[![PyPI version](https://badge.fury.io/py/hotpepper-gourmet.svg)](https://badge.fury.io/py/hotpepper-gourmet)  
![workflow badge](https://github.com/paperlefthand/hotpepper-gourmet/actions/workflows/build.yml/badge.svg)
![workflow badge](https://github.com/paperlefthand/hotpepper-gourmet/actions/workflows/publish.yml/badge.svg)

## About

[ホットペッパーグルメAPI](https://webservice.recruit.co.jp/doc/hotpepper/reference.html)のシンプルなクライアントライブラリです

## How To Use

### keyidの取得

ホットペッパーグルメAPIに登録し, token(keyid)を取得

### サンプルコード

``` python
>>> from pygourmet import Api, Option
>>> api = Api(keyid=YOUR_KEYID)
>>> option = Option(lat=35.170915, lng=136.8793482, keyword="ラーメン", radius=400, count=3)
>>> results = api.search(option)
>>> len(results)
3
>>> results[0]["name"]
'shop name'
```

___

Powered by [ホットペッパー Webサービス](http://webservice.recruit.co.jp/)
