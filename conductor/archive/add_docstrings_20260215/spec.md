# Track Specification: Add Japanese Docstrings for pdoc

## Overview
`pygourmet` ライブラリの主要なパブリッククラス、メソッド、およびモジュールに、Googleスタイルの日本語ドキュメント（Docstring）を追加します。これにより、`pdoc` で生成されるAPIドキュメントの品質を向上させ、利用者にとって分かりやすいリファレンスを提供します。

## Functional Requirements
- `src/pygourmet/` 配下の以下の主要なパブリックモジュールを対象とする。
    - `client.py`
    - `shop.py`
    - `option.py`
    - `errors.py`
- すべてのパブリッククラスおよびメソッドに Googleスタイルの Docstring を追加する。
- 既存の Docstring は一旦削除し、新しい基準で一から書き直す。
- 内容には以下の項目を含める：
    - 概要（一行目）
    - 詳細な説明（必要に応じて）
    - 引数（`Args`）: 名前、型、説明、デフォルト値
    - 戻り値（`Returns`）: 型、説明
    - 例外（`Raises`）: 型、発生条件
    - 使用例（`Examples`）: コードスニペット
- Hotpepper Gourmet APIの仕様に基づき、日本語で記述する。

## Non-Functional Requirements
- `pdoc` でのレンダリングが正しく行われること。
- `ruff` の Lint ルール（Googleスタイルに関連するもの）を遵守すること。
- コードの動作自体には影響を与えないこと。

## Acceptance Criteria
- 対象モジュール内のすべてのパブリック要素に Googleスタイルの日本語 Docstring が付与されている。
- `uv run pdoc src/pygourmet` を実行し、ブラウザで閲覧可能な高品質なドキュメントが生成される。
- `uv run ruff check .` を実行し、Docstring 関連の警告（もし有効であれば）が出ていないこと。

## Out of Scope
- `__init__.py` への Docstring 追加。
- プライベートな関数やクラス（`_` で始まるもの）への詳細な Docstring 追加（必要最小限に留める）。
- テストコードへの Docstring 追加。
- APIクライアントのロジック変更。
