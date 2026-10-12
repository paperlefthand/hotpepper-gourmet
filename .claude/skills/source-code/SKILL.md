---
name: source-code
description: src/pygourmet/ 配下のライブラリコードを実装・変更するときに適用する規約。API リファレンスとの照合手順、Option/Shop へのパラメータ・フィールド追加手順、同期/非同期の対称性、Pydantic と docstring の書き方を定義する。src/pygourmet/**/*.py を編集・作成するときに従う。
paths: "src/pygourmet/**/*.py"
user-invocable: false
---

# ライブラリコード実装ルール

`AGENTS.md` の規約に加え、`src/pygourmet/` を変更するときは以下に従う。

## 1. 先に API リファレンスを確認する

パラメータ・フィールドを追加/変更する前に、[ホットペッパーグルメ API リファレンス](https://webservice.recruit.co.jp/doc/hotpepper/reference.html) の「グルメサーチAPI」の該当箇所を確認し、次を決める。

- 名前: API のキー名をそのままフィールド名にする（言い換え・別名は付けない）。
- 型: 下表の対応に従う。迷ったら既存の類似フィールドに揃える。
- 制約: 値域や指定可能数があれば `Field(ge=..., le=...)` や docstring に反映する。

| API 側の値 | `Option`（リクエスト） | `Shop`（レスポンス） |
| --- | --- | --- |
| 0/1 のフラグ | `bool \| None`（`serialize_bool` で 0/1 に変換） | API が返す文字列のまま `str \| None` |
| カンマ区切りで複数指定可 | `str \| list[str] \| None`（`serialize_list` に登録） | — |
| コード値・自由文字列 | `str \| None` | `str \| None` |
| 数値 | `int \| None` / `float \| None` | `int \| None` / `float \| None` |
| 入れ子オブジェクト | — | `frozen=True` の BaseModel を新設 |

## 2. パラメータ追加の手順（`Option`）

1. `option.py` にフィールドを追加する（既定値は `None`。API 側に既定値がある場合のみ明示）。
2. bool 型なら `serialize_bool`、リスト型なら `serialize_list` の `@field_serializer` 対象に名前を追加する。**追加漏れするとクエリが `True`/`False` やリスト表記で送られてしまう。**
3. クラス docstring の `Attributes:` に API リファレンスの日本語名で追記する。
4. `tests/test_serialization.py` にクエリパラメータへの変換結果を確認するテストを追加する。

`client.py` は `option.model_dump()` の `None` 以外をそのまま送るため、通常は変更不要。

## 3. レスポンスフィールド追加の手順（`Shop`）

1. `shop.py` にフィールドを追加する（既定値は `None`）。入れ子なら専用モデルを定義する。
2. 空文字列は `check_empty_values` で `None` に正規化されるので、個別の変換は書かない。
3. クラス docstring の `Attributes:` に追記する。
4. `tests/data/` のサンプル JSON に該当フィールドが無ければ追加し、パースを確認するテストを書く。

## 4. 同期/非同期の対称性

`Api.search` と `Api.search_async` は同じ入力に対して同じ結果・同じ例外を返す。共通処理はプライベートメソッド（`__create_query_params` / `__create_shop_list`）に置き、片方だけを変更しない。

## 5. 例外

ライブラリ利用者に見せる例外は `SearchError` に統一する。API のエラーコード（1000/2000/3000）は日本語メッセージ付きで `SearchError` に変換する。新たな例外クラスを増やす場合は公開 API の変更として扱い、`__init__.py` で再エクスポートする。

## 6. Docstring

公開クラス・メソッドには日本語の Google Style docstring を書く（`pdoc` で公開される）。プライベート（`_` 始まり）は簡潔でよい。

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

## 7. 公開 API

利用者向けのクラスは `src/pygourmet/__init__.py` で再エクスポートする。既存の公開名（`Api`, `Option`, `Shop`, `SearchError`）の削除・リネーム・必須引数の追加は破壊的変更なので、実施前にユーザーへ確認する。
