# 開発ガイドライン（OSSコントリビュータ & Codex 共通）

このリポジトリでは、**OSS コントリビュータ**と **OpenAI Codex（CLI/IDE/クラウド）** を同一の開発者として扱い、
両者が**同一の指針**に従ってコード変更・提案・PR を行うことを前提とします。
以降の記述は「人間・Codex 共通のルール」です。

> Tech stack: **uv(パッケージ管理)** / **tox-uv(タスク統一)** / **ruff(Lint & Format)** / **ty(型チェック)** / **pytest** / **pre-commit**
> Repo: <https://github.com/paperlefthand/hotpepper-gourmet>

## 1. 役割（Roles）

すべての開発者（人間・Codex）は、次のいずれかの役割でタスクを実行してください。
PR 作成時に、どの役割で行った変更かを明示してください。

1. **データ取得ロジックの改善 (Data Retrieval Improvements)**
   - 対象: `src/pygourmet/` 以下の API ラッパー・パラメータ・モデル（例: `client.py`, `option.py`, `shop.py`）
   - 目的: 信頼性・可読性・保守性の向上（リトライ/タイムアウト/エラー処理/型安全性の強化、不要コード削減 など）
   - 成果物: 小さめのコミット単位でのリファクタ、必要に応じたテスト追加

2. **テストの自動生成 (Test Authoring & Maintenance)**
   - 対象: `tests/`（含: `tests/conftest.py`, `tests/data/`）
   - 目的: ユニットテスト/軽量な統合テストの追加・保守、モックやサンプルデータの整備
   - 成果物: 既存挙動を壊さない追加テスト、足りない分岐の補完、回帰テスト

3. **README のサンプル更新 (README Examples & Docs)**
   - 対象: `README.md`（**のみ**）
   - 目的: 導入手順、最小サンプル、よくある落とし穴、サンプルコードの更新・追補
   - 成果物: 初学者が数分で動かせる導線、最新ツールチェーンとの整合

> **非対応**: 上記以外（CI 設定、リリース工程、`docs/` 下の Sphinx 原稿、`pyproject.toml` のビルド設定の大幅変更 等）は対象外です。必要があれば Issue 提案のみ行ってください。

## 2. 作業範囲（Scope Restrictions）

変更可能なのは次の 3 つに限定します：

- `src/`
- `tests/`
- `README.md`

> それ以外（例: `.github/workflows/`, `docs/`, `examples/`, `LICENSE`, `pyproject.toml` の大規模変更）は **変更禁止**。必要なら Issue 提案のみ。

## 3. 方針（Coding & Process Policy）

- **型ヒント必須**（Python）
  - 公開 API・主要関数は**完全注釈**。戻り値の型を明示し、`Any` の漏れを避ける。
- **スタイル/静的解析**は Ruff と Ty に準拠
  - Lint・Format は **Ruff**、型チェックは **Ty** を使用。
- **コミット時は pre-commit を必ず実行**
  - すべてのコミット前に `pre-commit` を走らせ、自動修正できない警告は解消する。
- **Conventional Commits 準拠**
  - 例: `feat: add async client retry`, `fix: correct query param name`, `docs: update README quickstart`
- **最小差分・小さな単位の PR**
  - 1 PR = 1 目的。大規模変更は分割。
- **秘密情報の取り扱い禁止**
  - 実 API キー等の秘匿情報を**生成・貼り付け禁止**。テストはモック/環境変数で。

## 4. 品質ゲート（Quality Gates）

PR を出す前に、**必ず以下のコマンドをローカルで通過**させてください（tox-uv 経由）。

```bash
# 依存セットアップ（開発環境）
uv sync --group dev --group test --group doc

# すべての単体テスト・検査の実行（必須）
tox -e lint,format,type,py311,py312,py313,docs
```

- 失敗した場合は修正して再実行。
- PR は **テスト合格後にのみ** 作成可。

## 5. タスク実行コマンド（統一）

> 人間も Codex も、同じコマンドで開発作業を行うこと。

- 依存セットアップ（開発環境）

  ```bash
  uv sync --group dev --group test --group doc
  ```

- 事前フック（必須）

  ```bash
  pre-commit run --all-files
  ```

- 総合チェック（PR 前の最終確認）

  ```bash
  tox -e lint,format,type,py311,py312,py313,docs
  ```

## 6. Git / PR 運用（Conventions）

- **コミット**: Conventional Commits。先頭行は簡潔に、本文で背景と検証手順（実行コマンド・結果）を記載。
- **PR テンプレ**（必須要素）:
  1) 役割（上記 3 つのどれか）
  2) 変更概要（なぜ・何を）
  3) 動作確認（実行コマンドと成功ログの要約）
  4) 破壊的変更の有無
  5) 関連 Issue（あれば）

- **レビュー**: 人間・Codex どちらが作成した PR でも同一の基準でレビューされます。

## 7. 役割別チェックリスト（DoD）

### 7.1 データ取得ロジックの改善

- [ ] 既存の公開 API 仕様・例外契約を**変更しない**
- [ ] リトライ/タイムアウト/例外メッセージの一貫性
- [ ] 型注釈・Docstring の追加/更新
- [ ] テスト（成功/失敗/例外分岐）追加
- [ ] `tox -e lint,format,type,py311,py312,py313,docs` 合格

### 7.2 テストの自動生成

- [ ] 新規テストは最小限のモック/サンプルで**速く安定**
- [ ] 既存挙動の**回帰防止**を最優先
- [ ] テスト名/説明は**意図が伝わる**命名
- [ ] カバレッジ/分岐の穴を補完
- [ ] 総合チェック合格

### 7.3 README のサンプル更新

- [ ] セットアップ/最小サンプル/落とし穴の**3 点セット**
- [ ] コード片は**実行可能**かつリポジトリ現状と一致
- [ ] コマンドは `uv`/`tox-uv` の運用に整合
- [ ] 過度な機能紹介は避け**最短経路**を示す
- [ ] 総合チェック合格（`docs` ターゲットも通過）

## 8. 禁則事項（Non-Goals / Don’ts）

- `src/`・`tests/`・`README.md`・`pyproject.toml`の依存パッケージ欄 **以外の改変禁止**（Issue 提案は可）
- 秘密情報/API キーの生成・貼付・ログ出力**禁止**
- 破壊的変更の混入、未テストコードの投入、巨大 PR の作成**禁止**
- pre-commit 未実行のコミット**禁止**

## 9. 参考（プロジェクト構造の目安）

- ライブラリ本体: `src/pygourmet/`
- テスト: `tests/`（`conftest.py` / `tests/data/` あり）
- ドキュメント（Sphinx ソース）: `docs/`（**編集範囲外**）
- 型配布: `py.typed` を同梱（完全型サポート）

### 付録: コミットメッセージ例

- `feat: add timeout and retry to async client`
- `fix: correct parameter encoding for keyword search`
- `test: add error-path unit tests for empty results`
- `docs: update README quickstart with uv + tox-uv`
