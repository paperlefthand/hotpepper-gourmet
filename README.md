# hotpepper-gourmet

## About

[ホットペッパーグルメAPI](https://webservice.recruit.co.jp/doc/hotpepper/reference.html)のシンプルなクライアントライブラリです

## How To Use

### keyidの取得

ホットペッパーグルメAPIに登録し, token(keyid)を取得

### サンプル

``` python
import pygourmet

api = pygourmet.Api(keyid=YOUR_KEYID)
results = api.get_restaurants(lat=35.170915, lng=136.8793482, radius=400)
print(results)
```

### シーケンス図

![sequence](out/diagrams/sequence/sequence.png)

___

Powered by [ホットペッパー Webサービス](http://webservice.recruit.co.jp/)
