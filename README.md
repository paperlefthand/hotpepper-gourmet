# hotpepper-gourmet

![workflow badge](https://github.com/paperlefthand/hotpepper-gourmet/actions/workflows/pytest.yml/badge.svg)
![workflow badge](https://github.com/paperlefthand/hotpepper-gourmet/actions/workflows/deploy.yml/badge.svg)

## About

[ホットペッパーグルメAPI](https://webservice.recruit.co.jp/doc/hotpepper/reference.html)のシンプルなクライアントライブラリです

## How To Use

### keyidの取得

ホットペッパーグルメAPIに登録し, token(keyid)を取得

### サンプルコード

``` python
>>> import pygourmet
>>> api = pygourmet.Api(keyid=YOUR_KEYID)
>>> results = api.search(lat=35.170915, lng=136.8793482, radius=400, count=3)
>>> len(reaults)
3
>>> results[0]["name"]
>>> 'shop name'
```

___

Powered by [ホットペッパー Webサービス](http://webservice.recruit.co.jp/)
