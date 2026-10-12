# コントリビューションガイド

pygourmet への貢献に関心を持っていただきありがとうございます.
バグ報告・ドキュメントの修正・機能追加など, どのような貢献も歓迎します.

参加にあたっては [行動規範](CODE_OF_CONDUCT.md) を守ってください.

## 貢献の方法

| やりたいこと | 方法 |
| --- | --- |
| 不具合を報告したい | Issue の「バグ報告」テンプレート |
| 公式 API とモデルの食い違いを報告したい | Issue の「API 仕様との差分の報告」テンプレート |
| 機能を提案したい | Issue の「機能要望」テンプレート |
| 使い方を質問したい | 空の Issue |
| 脆弱性を報告したい | 公開 Issue ではなく [SECURITY.md](SECURITY.md) の手順 |
| コードやドキュメントを直したい | 下記の手順で Pull Request |

typo の修正などの小さな変更は, いきなり PR を出してもらって構いません.
公開 API (`Api` / `Option` / `Shop` / `SearchError`) に関わる変更や大きな機能追加は, 方針のすり合わせのため先に Issue で相談してください.

## 開発環境の構築

[uv](https://docs.astral.sh/uv/) を使います. 推奨する開発用の Python バージョンは `.python-version` に記載しています (現在は 3.14).

```bash
# 1. リポジトリを fork して clone する
git clone https://github.com/<your-name>/hotpepper-gourmet.git
cd hotpepper-gourmet

# 2. 依存関係をインストールする
uv sync

# 3. (任意) コミット時に ruff を自動実行する Git フックを入れる
uv run prek install
```

本番 API に接続する統合テストを手元で動かしたい場合は, [ホットペッパー Web サービス](https://webservice.recruit.co.jp/) で API キーを取得し, `.env` に記載します. `.env` は Git 管理外です. 絶対にコミットしないでください.

```bash
echo 'HOTPEPPER_KEYID=<あなたのキー>' > .env
```

## 開発の流れ

このリポジトリは **GitHub Flow** を採用しています. 開発ブランチは `main` のみです.

1. `main` から作業ブランチを切ります. ブランチ名は自由ですが, `feat/xxx`, `fix/xxx` のように内容が分かる名前を推奨します.
2. 変更を加え, 下記の「PR を出す前の確認」を通します.
3. fork 先へ push し, `main` 宛てに Pull Request を作成します. PR テンプレートの項目を埋めてください.
4. CI (lint / format / 型チェック / Python 3.12–3.14 のテスト) と PR タイトルの検査が通ると, メンテナーがレビューします.
5. 承認されると, メンテナーが **Squash マージ** します.

### PR タイトルの書き方

Squash マージでは **PR タイトルがそのまま `main` のコミットメッセージになり, リリースノートの項目にもなります.**
そのため, PR タイトルは [Conventional Commits](https://www.conventionalcommits.org/ja/v1.0.0/) 形式で書いてください (CI で検査します).
個々のコミットメッセージの形式は問いません.

```text
<type>(<scope>): <変更内容の要約>
```

| type | 用途 | リリースノートでの分類 |
| --- | --- | --- |
| `feat` | 機能追加 | ✨ 新機能 |
| `fix` | バグ修正 | 🐛 バグ修正 |
| `docs` | ドキュメントのみの変更 | 📝 ドキュメント |
| `refactor` / `perf` / `test` / `build` / `ci` / `chore` / `revert` | その他の変更 | 🔧 その他 |

- `scope` は任意です. 例: `client`, `option`, `shop`, `errors`, `deps`.
- 公開 API の互換性を壊す変更には `!` を付けます. 例: `feat(option)!: range の型を Enum に変更する`
- 例: `fix(shop): 営業時間が空のときに検証エラーになる問題を修正する`

### PR を出す前の確認

```bash
uv run prek run --all-files   # ruff check / format
uv run ty check               # 型チェック
uv run pytest                 # 単体テスト
```

`Option` や `Shop` を変更した場合は, [API リファレンス](https://webservice.recruit.co.jp/doc/hotpepper/reference.html) と照合してください.

## コーディング規約とテスト方針

コーディング規約 (型注釈, docstring, 後方互換性) とテスト方針は [AGENTS.md](AGENTS.md) にまとめています. AGENTS.md は人間と AI エージェントの共通ガイドです. 要点は次のとおりです.

- Ruff の設定に従います. `Any` を使わない厳格な型注釈を書き, 公開 API には日本語の Google Style docstring を書きます.
- 同期 (`search`) と非同期 (`search_async`) の両 API を常に同等の機能で提供します.
- 単体テストは `pytest-httpx` で API レスポンスをモックし, 実ネットワークに接続しません. 変更には必ずテストを付けてください.
- 本番 API に接続するテストには `@pytest.mark.integration` を付けます. 統合テストはメンテナーが CI で毎週実行しているので, 手元での実行は任意です.

## AI ツールの利用について

GitHub Copilot や Claude Code などの AI ツールを使った貢献も歓迎します. ただし, 次の点を守ってください.

- **提出者が内容に責任を持ちます.** 生成されたコードやドキュメントをすべて読んで理解し, 手元でテストを実行して動作を確認してから提出してください. レビューでの質問に自分の言葉で答えられない変更は受け付けられません.
- AI エージェントにはこのリポジトリの [AGENTS.md](AGENTS.md) を読ませてください. Claude Code は `CLAUDE.md` 経由で自動的に読み込みます.
- 大量の機械的な変更や, 実際の問題に基づかない「改善」の PR は控えてください.
- API キーなどの機密情報を AI ツールに渡さないでください.

## リリース

リリースはメンテナーが行います. 手順は [MAINTAINING.md](MAINTAINING.md) を参照してください.
`main` にマージされた変更は, 開発版として [TestPyPI](https://test.pypi.org/p/hotpepper-gourmet) に自動公開されます.

## ライセンス

貢献していただいたコードは, このプロジェクトと同じ [MIT License](LICENSE.txt) のもとで公開されます.
