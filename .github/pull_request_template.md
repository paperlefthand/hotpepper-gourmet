<!--
PR タイトルは Conventional Commits 形式で書いてください (CI で検査されます).
Squash マージされ, タイトルがそのまま main のコミットメッセージとリリースノートの項目になります.

  例) feat(option): 予算コードによる絞り込みに対応する
      fix(shop): 営業時間が空のときに検証エラーになる問題を修正する
      feat!: Api.search の戻り値を変更する   ← 破壊的変更は `!` を付ける

詳しくは CONTRIBUTING.md を参照してください.
-->

## 変更の目的

<!--
このPRで導入される変更の概要を明確かつ簡潔に記述してください.
変更の目的と背景を説明し, 関連するIssueやPRがあればリンクしてください.
-->

- **何をするのか?**
- **なぜこの変更が必要なのか?**
- **関連するIssue** (例: Fixes #123)

## 変更の種類

<!-- 該当するものを選択してください -->

- [ ] バグ修正 (既存の不具合を修正する互換性のある変更)
- [ ] 新機能 (新しい機能を追加する互換性のある変更)
- [ ] 破壊的変更 (`Api` / `Option` / `Shop` / `SearchError` の公開インターフェースが変わる変更. PR タイトルに `!` を付ける)
- [ ] ドキュメント更新
- [ ] リファクタリング
- [ ] CI / 開発環境 / AI エージェント設定の変更
- [ ] その他 (具体的に記述してください):

## テストの実行結果

<!--
変更を確認するために実行したテストについて記述してください.
`uv run pytest` の出力の要約などを添付してください.
-->

- **テスト環境**: (例: Python 3.14, Ubuntu 24.04)
- **実施したテスト**:
  - [ ] `uv run pytest` がパスすることを確認した
  - [ ] (API との通信に関わる変更の場合) 統合テスト `uv run pytest --run-integration` を実行した
  - [ ] (`Option` / `Shop` を変更した場合) [API リファレンス](https://webservice.recruit.co.jp/doc/hotpepper/reference.html) と照合した

## ドキュメント更新の有無

- [ ] `src/pygourmet` 以下の docstring を更新した
- [ ] `README.md` を更新した
- [ ] `CONTRIBUTING.md` / `MAINTAINING.md` を更新した
- [ ] `AGENTS.md` / `CLAUDE.md` / `.claude/` を更新した
- [ ] ドキュメントの更新は不要

## チェックリスト

<!-- レビューを依頼する前に, 以下の項目をすべて確認してください -->

- [ ] **コード品質**
  - [ ] `uv run prek run --all-files` を実行し, エラーがないことを確認した
  - [ ] 型チェック (`uv run ty check`) をパスしている

- [ ] **PR タイトル**
  - [ ] [Conventional Commits](https://www.conventionalcommits.org/ja/v1.0.0/) に従っている

- [ ] **セキュリティ**
  - [ ] APIキー (`HOTPEPPER_KEYID`) などの機密情報や `.env` ファイルが含まれていないことを確認した

- [ ] **AI ツールの利用** (利用した場合のみ)
  - [ ] 生成された内容をすべて理解し, 自分で動作を確認した
