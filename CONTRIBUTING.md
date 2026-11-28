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

[uv](https://docs.astral.sh/uv/) 0.11 以降を使います (古い場合は `uv self update` で更新してください). 推奨する開発用の Python バージョンは `.python-version` に記載しています (現在は 3.14).

```bash
# 1. リポジトリを fork して clone する
git clone https://github.com/<your-name>/hotpepper-gourmet.git
cd hotpepper-gourmet

# 2. 依存関係をインストールする
uv sync

# 3. (任意) コミット時に ruff / rumdl / tombi を自動実行する Git フックを入れる
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
uv run prek run --all-files   # ruff check / format, rumdl, tombi
uv run ty check               # 型チェック
uv run pytest                 # 単体テスト
```

`Option` や `Shop` を変更した場合は, [API リファレンス](https://webservice.recruit.co.jp/doc/hotpepper/reference.html) と照合してください.

`.github/workflows/` の `uses:` を追加・変更した場合は, [gh-actions-lock](https://github.com/github/gh-actions-lock) で `actions.lock` を更新し, 一緒にコミットしてください. 更新していないと `verify-lockfile` が失敗します.

```bash
gh extension install github/gh-actions-lock --pin v0.4.1   # 初回のみ
gh actions-lock
```

`uv run prek install` を済ませていれば, ワークフローを変更したコミットで更新漏れを検査します (拡張が入っていない場合はスキップされます).

## コーディング規約とテスト方針

コーディング規約 (型注釈, docstring, 後方互換性) とテスト方針は [AGENTS.md](AGENTS.md) にまとめています. AGENTS.md は人間と AI エージェントの共通ガイドで, 層ごとの詳細は [src/AGENTS.md](src/AGENTS.md) と [tests/AGENTS.md](tests/AGENTS.md) にあります. 要点は次のとおりです.

- Ruff の設定に従います. `Any` を使わない厳格な型注釈を書き, 公開 API には日本語の Google Style docstring を書きます.
- 同期 (`search`) と非同期 (`search_async`) の両 API を常に同等の機能で提供します.
- 単体テストは `pytest-httpx` で API レスポンスをモックし, 実ネットワークに接続しません. 変更には必ずテストを付けてください.
- 本番 API に接続するテストには `@pytest.mark.integration` を付けます. 統合テストはメンテナーが CI で毎週実行しているので, 手元での実行は任意です.

## AI ツールの利用について

GitHub Copilot や Claude Code などの AI ツールを使った貢献も歓迎します. ただし, 次の点を守ってください.

- **提出者が内容に責任を持ちます.** 生成されたコードやドキュメントをすべて読んで理解し, 手元でテストを実行して動作を確認してから提出してください. レビューでの質問に自分の言葉で答えられない変更は受け付けられません.
- AI エージェントにはこのリポジトリの [AGENTS.md](AGENTS.md) を読ませてください. AGENTS.md に対応したツールは自動で読み込みます.
- 大量の機械的な変更や, 実際の問題に基づかない「改善」の PR は控えてください.
- API キーなどの機密情報を AI ツールに渡さないでください.

### エージェントの設定について

規約は特定のツールに依存しないよう AGENTS.md に書き, ツール固有の設定は AGENTS.md や CI にある検査を手元で早く回すためのものに限っています. AGENTS.md や CI にないルールを, ツール固有の設定だけに追加しないでください.

Claude Code を使う場合は次の点に注意してください.

- AGENTS.md を直接読むには **v2.1.277 以降**が必要です (Amazon Bedrock 経由やテレメトリを無効にしている場合は v2.1.281 以降). セッション開始時に `/context` を実行し, Memory files に `AGENTS.md` が表示されることを確認してください.
- **`CLAUDE.md` や `CLAUDE.local.md` をリポジトリ内に置かないでください.** どちらかがあると, 既定の設定では AGENTS.md が読まれなくなります. コミットは prek のフックと CI で拒否します. `CLAUDE.local.md` は気づけるようにあえて `.gitignore` に入れていないので, `git status` に表示されたら削除してください.
- 個人の指示は `~/.claude/CLAUDE.md` や `~/.claude/rules/` に置きます. リポジトリ内の CLAUDE.md も使いたい場合は, `/config` の **Project instructions** を AGENTS.md と CLAUDE.md の両方を読む設定 (`claude-md-and-agents-md`) にしてください (ユーザー設定 `~/.claude/settings.json` に保存されます).
- サブディレクトリの AGENTS.md (`src/AGENTS.md`, `tests/AGENTS.md`) は, そのディレクトリのファイルを Read したときに読み込まれます. 新しいファイルを作るだけのときは読まれないことがあるので, ルートの AGENTS.md で「変更前に読む」よう指示しています.
- `.claude/settings.json` に, 次の Hook を登録しています. 実行には `jq` が必要です.
  - Python ファイルの編集時: `ruff format` と `ruff check --fix` を実行します.
  - Markdown / TOML ファイルの編集時: `rumdl` / `tombi` で整形し, 自動修正できない問題が残れば修正を促します.
  - ターン終了時: `src/` か `tests/` に未コミットの変更があれば, CI と同じ `ruff check`, `ruff format --check`, `ty check`, `pytest` を実行し, 失敗したら修正を促します.
- 統合テスト (`--run-integration`) の実行は, 許可済みのコマンドでも毎回確認を求める設定にしています (`.env` の API キーで本番 API に接続するため).
- 個人の権限設定は `.claude/settings.local.json` に置きます (`.gitignore` 済み).

## リリース

リリースはメンテナーが行います. 手順は [MAINTAINING.md](MAINTAINING.md) を参照してください.
`main` にマージされた変更は, 開発版として [TestPyPI](https://test.pypi.org/p/hotpepper-gourmet) に自動公開されます.

## ライセンス

貢献していただいたコードは, このプロジェクトと同じ [MIT License](LICENSE.txt) のもとで公開されます.
