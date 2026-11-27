# テストの作成規約

ルートの `AGENTS.md` に加え、`tests/` を変更するときは以下に従う。

- 単体テストは `pytest-httpx` で API レスポンスをモックし、実ネットワークに接続しない。
- 新しいコードのカバレッジは 80% 以上を目安とする (`uv run pytest --cov=pygourmet`)。
- API のエラーは HTTP 200 で返るため、エラー系のモックは `status_code` ではなくレスポンス本文の `error` で作る。

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
- `--run-integration` なしではスキップされる。PR の CI では実行されず、`integration.yml` が毎週本番 API に対して実行する (失敗すると `api-change` Issue が起票される)。
- エージェントは統合テストを自分の判断で実行しない。実行は人間の指示があるときのみ。
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
