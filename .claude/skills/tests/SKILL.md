---
name: tests
description: tests/ 配下のテストを作成・変更するときに適用する規約。pytest-httpx によるモックテスト、integration マーカー付き本番 API テスト、非同期テスト、サンプル JSON の置き場所とテスト関数の命名を定義する。tests/**/*.py を編集・作成するときに従う。
paths: "tests/**/*.py"
user-invocable: false
---

# テスト作成ルール

`AGENTS.md` のテスト方針に加え、`tests/` を変更するときは以下に従う。

## ファイルの使い分け

| ファイル | 内容 |
| --- | --- |
| `tests/test_client_dummy.py` | `Api` の検索処理をモックレスポンスで検証する単体テスト |
| `tests/test_serialization.py` | `Option` がクエリパラメータへ正しく変換されるかの検証 |
| `tests/test_client.py` | 本番 API に接続する統合テスト（`integration` マーカー必須） |
| `tests/conftest.py` | `--run-integration` オプションと `client_dummy` フィクスチャ |
| `tests/data/*.json` | API レスポンスのサンプル（実レスポンスから API キー等を除いたもの） |

新しいテストファイルを作る場合も上記の分類に揃える。

## 単体テスト（モック）

- `client_dummy` フィクスチャ（ダミー API キー）と `httpx_mock` を使う。実ネットワークには接続しない。
- 送信内容は `httpx_mock.get_request().url.params` で検証する。
- レスポンスが大きい場合はインラインで書かず、`tests/data/` の JSON を読み込む。

```python
def test_search_dummy_optionあり(client_dummy, httpx_mock):
    with open(
        os.path.join(DATAFILE_PATH, "restaurant_resp_0.json"), encoding="utf-8"
    ) as f:
        mock_response = json.load(f)
    httpx_mock.add_response(json=mock_response)

    shops = client_dummy.search(Option(keyword="ラーメン", lat=35.0, lng=135.0))

    assert shops[0].name == mock_response["results"]["shop"][0]["name"]
```

## 非同期テスト

`search_async` は `@pytest.mark.asyncio` を付けた `async def` テストで `await` して呼ぶ。同期版にテストを追加したら、同じ振る舞いを非同期版でも確認する。

## 統合テスト（本番 API）

- `@pytest.mark.integration` と、`HOTPEPPER_KEYID` 未設定時の `skipif` を必ず両方付ける。
- `--run-integration` なしではスキップされることを前提とし、CI では実行されない。
- API キーはテストコードに書かず、`load_dotenv()` 経由で `.env` から読む。

```python
@pytest.mark.integration
@pytest.mark.skipif(HOTPEPPER_KEYID is None, reason="HOTPEPPER_KEYID is not set")
def test_search_位置指定():
    assert HOTPEPPER_KEYID is not None
    shops = Api(HOTPEPPER_KEYID).search(Option(lat=34.8586318, lng=136.8139928))
    assert len(shops) > 0
```

## 命名

`test_<対象>_<条件や期待>` の形にし、条件部分は日本語で内容が分かるように書いてよい（例: `test_search_dummy_optionなし`, `test_search_位置指定`）。`test_case_1` のような番号だけの名前は使わない。
