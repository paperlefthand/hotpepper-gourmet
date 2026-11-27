# ライブラリコードの実装規約

ルートの `AGENTS.md` に加え, `src/pygourmet/` を変更するときは以下に従います.

## 1. 先に API リファレンスを確認する

パラメータ・フィールドを追加/変更する前に, [ホットペッパーグルメ API リファレンス](https://webservice.recruit.co.jp/doc/hotpepper/reference.html) の該当箇所を確認し, 次を決めます.

- **名前**: API のキー名をそのままフィールド名にする (言い換え・別名は付けない).
- **型**: 下表の対応に従う. 迷ったら既存の類似フィールドに揃える.
- **制約**: 値域や指定可能数があれば `Field(ge=..., le=...)` や docstring に反映する.
- **値の意味**: 0/1 の値は, どちらが「あり」かを API ごとに確認する. すべてが「1 = あり」ではない (例: `ktai_coupon` は 0: あり, 1: なし).

| API 側の値 | `Option` (リクエスト) | `Shop` (レスポンス) |
| --- | --- | --- |
| 0: 絞り込まない / 1: 絞り込む のフラグ | `bool \| None` (0/1 に変換して送る) | API が返す文字列のまま `str \| None` |
| 上記以外の意味を持つ 0/1 | `int \| None` とし, docstring に各値の意味を書く | — |
| 複数指定可 | `str \| list[str] \| None` (カンマ区切りに変換して送る) | — |
| コード値・自由文字列 | `str \| None` | `str \| None` |
| 数値 | `int \| None` / `float \| None` | `int \| None` / `float \| None` |
| 入れ子オブジェクト | — | `frozen=True` の BaseModel を新設 |

## 2. パラメータを追加する (`Option`)

1. `option.py` にフィールドを追加する (既定値は `None`. API 側に既定値がある場合のみ明示).
2. bool 型・リスト型は, 既存の `@field_serializer` の対象に名前を追加する. **追加漏れすると `True`/`False` やリスト表記のまま送られてしまう.**
3. クラス docstring の `Attributes:` に, API リファレンスの日本語名と値の意味を書く.
4. `tests/test_serialization.py` に, クエリパラメータへの変換結果を確認するテストを追加する.

## 3. レスポンスフィールドを追加する (`Shop`)

1. `shop.py` にフィールドを追加する (既定値は `None`). 入れ子なら専用モデルを定義する.
2. 空文字列はモデルのバリデータで `None` に正規化されるので, 個別の変換は書かない.
3. クラス docstring の `Attributes:` に追記する.
4. `tests/data/` のサンプル JSON に該当フィールドが無ければ追加し, パースを確認するテストを書く.

## 4. 同期/非同期の対称性

`Api.search` と `Api.search_async` は, 同じ入力に対して同じ結果・同じ例外を返します. 共通処理はプライベートメソッドに置き, 片方だけを変更しません.

## 5. 例外

API のエラーは HTTP ステータス 200 で返り, 本文の `error.code` (1000: サーバ障害, 2000: 認証エラー, 3000: パラメータ不正) で判定します. 利用者に見せる例外は `errors.py` で定義したものに限ります. 新しい例外クラスの追加は公開 API の変更として扱い, `__init__.py` で再エクスポートします.

## 6. Docstring

公開クラス・メソッドには日本語の Google Style docstring を書きます (`pdoc` で公開されます). プライベート (`_` 始まり) は簡潔でかまいません.

```python
def search(self, option: Option) -> list[Shop]:
    """レストランを同期的に検索します。

    Args:
        option (Option): 検索条件を指定するオプション。

    Returns:
        list[Shop]: 検索条件に合致した店舗データのリスト。

    Raises:
        SearchError: APIリクエストまたはレスポンスの処理中にエラーが発生した場合。
    """
```
