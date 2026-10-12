# メンテナー向け手順書

管理者 (メンテナー) が行う作業の手順です. コントリビューター向けの手順は [CONTRIBUTING.md](CONTRIBUTING.md) を参照してください.

以降のコマンドは, リポジトリのルートで次の変数を設定してある前提です.

```bash
R=paperlefthand/hotpepper-gourmet
```

## 全体像

```text
Issue → ブランチ → PR (タイトル = Conventional Commits)
  → 必須チェック: ci-success (ci.yml) / pr-title (pr-title.yml)
  → Squash マージ (PR タイトルがコミットになり, 種類ラベルが自動で付く)
  → main への push: ci 成功後に TestPyPI へ開発版を公開 (publish-dev.yml)
  → vX.Y.Z タグの push: main 上か検証 → ci → PyPI 公開 → Sigstore 署名
    → GitHub Release (ノート自動生成) → ドキュメント更新 (publish.yml → docs.yml)

定期実行:
  - Dependabot: 依存関係と Actions の更新 PR (毎週)
  - integration.yml: 本番 API への統合テスト (毎週月曜 09:00 JST). 失敗すると api-change Issue を起票する
```

| ワークフロー | 起動条件 | 役割 |
| --- | --- | --- |
| `ci.yml` | main 宛ての PR / main への push / publish.yml からの呼び出し | lint・format・型チェック・3.12〜3.14 のテスト |
| `pr-title.yml` | PR の作成・編集 | PR タイトルの検査と種類ラベルの付与 |
| `publish-dev.yml` | main への push で ci が成功した後 | TestPyPI へ開発版 (`X.Y.Z.devN`) を公開 |
| `publish.yml` | `v*` タグの push | PyPI 公開, 署名, GitHub Release, ドキュメント更新 |
| `docs.yml` | publish.yml からの呼び出し / 手動 | pdoc で生成したドキュメントを GitHub Pages へデプロイ |
| `integration.yml` | 毎週月曜 / 手動 | 本番 API に対する統合テスト |

## PR のレビューとマージ

1. 必須チェックの `ci-success` と `pr-title` が通っていることを確認します.
2. PR タイトルが変更内容を正しく表しているかを確認します. 必要なら, マージ前にメンテナーがタイトルを直接編集します (編集すると `pr-title` が再実行されます).
   - 公開 API (`Api` / `Option` / `Shop` / `SearchError`) の互換性を壊す変更なら, タイトルに `!` が付いているか (`breaking-change` ラベルが付いたか) を確認します.
3. ラベルを確認します. `feat` / `fix` / `docs` / `!` には自動でラベルが付きます. リリースノートでの分類を変えたい場合は手動で付け替えます.
4. **Squash and merge** でマージします. コミットのタイトルは PR タイトル, 本文は PR の説明になります.

外部からの PR でも `ci.yml` は実行されます (fork からの PR は初回のみ, Actions タブで実行の承認が必要な場合があります). 統合テスト用の Secret は fork からの PR には渡りません.

## リリース手順

### 1. バージョンを決める

[SemVer](https://semver.org/lang/ja/) に従います. 1.0.0 までは次の規則とします.

| 前回のリリース以降の変更 | 上げる桁 | 例 |
| --- | --- | --- |
| 破壊的変更 (`breaking-change`) を含む | MINOR | 0.1.3 → 0.2.0 |
| 新機能 (`feat`) を含む | MINOR | 0.1.3 → 0.2.0 |
| バグ修正などのみ | PATCH | 0.1.3 → 0.1.4 |

未リリースの変更は次で確認できます.

```bash
git fetch --tags origin
git log --oneline "$(git describe --tags --abbrev=0 origin/main)"..origin/main
```

### 2. リリースノートをプレビューする

```bash
gh api "repos/$R/releases/generate-notes" -f tag_name=vX.Y.Z -f target_commitish=main --jq .body
```

分類がおかしい場合は, 該当する PR のラベルを付け替えます.

### 3. タグを push する

```bash
git switch main
git pull --ff-only
git tag -a vX.Y.Z -m "vX.Y.Z"
git push origin vX.Y.Z
```

- タグは `vMAJOR.MINOR.PATCH` 形式のみ有効です (`pyproject.toml` の `tag-pattern`). パッケージのバージョンは `hatch-vcs` がタグから決めます.
- main に含まれないコミットにタグを付けると, `publish.yml` の `verify-tag` ジョブで止まります.

### 4. 公開を確認する

```bash
gh run watch "$(gh run list --workflow publish.yml --limit 1 --json databaseId --jq '.[0].databaseId')"
```

完了したら次を確認します.

- [PyPI](https://pypi.org/p/hotpepper-gourmet) に新バージョンが出ていること
- `uvx --from hotpepper-gourmet==X.Y.Z python -c "import pygourmet"` が成功すること
- [GitHub Releases](https://github.com/paperlefthand/hotpepper-gourmet/releases) にリリースノートと署名ファイルが添付されていること
- [ドキュメント](https://paperlefthand.github.io/hotpepper-gourmet/) が更新されていること

### 5. 失敗したとき

- **PyPI への公開前に失敗した場合** (verify-tag, ci, build): main で修正し, タグを付け直します.

  ```bash
  git push --delete origin vX.Y.Z
  git tag -d vX.Y.Z
  # 修正を main にマージした後, 手順 3 をやり直す
  ```

- **PyPI 公開後に失敗した場合** (署名, Release, ドキュメント): PyPI には同じバージョンを再アップロードできません. 該当ジョブを `gh run rerun <run-id> --failed` で再実行します. ドキュメントだけなら `gh workflow run docs.yml` でも再デプロイできます.
- **公開したバージョンに重大な問題があった場合**: PyPI の管理画面 (Manage → Releases → Options → Yank) で yank し, 修正版を PATCH として出します. yank すると, バージョンを固定していない利用者にはインストールされなくなります.

## 週次統合テストが失敗したとき

`integration.yml` が失敗すると, 「週次統合テストが失敗しました」という Issue (`api-change` ラベル) が起票されます. Issue が open のまま再び失敗した場合は, その Issue にコメントが追記されます. 実行ログを開いて原因を切り分けます.

| 症状 | 原因 | 対応 |
| --- | --- | --- |
| タイムアウト, 5xx, 接続エラー | API 側の一時的な障害 | `gh workflow run integration.yml` で再実行し, 成功したら Issue を閉じる |
| `HOTPEPPER_KEYID is not set` / 認証エラー | Secret の未設定またはキーの無効化 | `integration` environment の Secret を更新する (後述) |
| Pydantic の `ValidationError` | レスポンスの仕様変更 (フィールドの追加・削除・型の変化) | 下記の手順で追従する |
| エラーメッセージの不一致 | API のエラーメッセージの変更 | テストの期待値を更新する |

仕様変更に追従する手順は次のとおりです.

1. [API リファレンス](https://webservice.recruit.co.jp/doc/hotpepper/reference.html) で変更点を確認し, Issue に記録します.
2. `src/pygourmet/shop.py` / `option.py` のモデルを修正し, 実レスポンスから API キーを除いたサンプルを `tests/data/` に追加して単体テストを書きます.
3. `fix(shop): ...` のような PR を出してマージし, PATCH リリースします.

## Dependabot の PR

毎週, Python の依存関係 (`uv.lock` / `pyproject.toml`) と GitHub Actions の更新が, それぞれ 1 つの PR にまとめて届きます.

- PR タイトルは `chore(deps): ...` / `ci(deps): ...` 形式なので, そのまま `pr-title` を通過します.
- 公開から 7 日未満のバージョンは提案されません (`cooldown`). `pyproject.toml` の `exclude-newer = "1 week"` と揃えています.
- CI が通れば Squash マージします. メジャーバージョンの更新を含む場合は, 変更履歴を確認してから判断します.
- `ruff` は `pyproject.toml` でバージョンを完全に固定しています. Dependabot がこの固定値を更新した PR では, フォーマット差分で CI が落ちることがあります. その場合はその PR のブランチで `uv run ruff format .` を実行し, コミットします.

## ラベル

| ラベル | 付与 | 用途 |
| --- | --- | --- |
| `breaking-change` | 自動 (タイトルの `!`) / 手動 | リリースノートの「💥 破壊的変更」 |
| `enhancement` | 自動 (`feat`) / Issue テンプレート | 「✨ 新機能」 |
| `bug` | 自動 (`fix`) / Issue テンプレート | 「🐛 バグ修正」 |
| `documentation` | 自動 (`docs`) | 「📝 ドキュメント」 |
| `dependencies` | Dependabot | 「⬆️ 依存関係」 |
| `api-change` | 統合テストの失敗 / Issue テンプレート | 公式 API の仕様変更への追従 |
| `good first issue` / `help wanted` | 手動 | 外部の方に取り組んでほしい Issue |

## リポジトリの初期設定

リポジトリを GitHub Flow に移行したときに行った設定です. 設定を作り直す場合にも使います.

### 1. マージ方式

Squash マージのみを許可し, PR タイトルをコミットタイトルにします.

```bash
gh api -X PATCH "repos/$R" \
  -F allow_squash_merge=true -F allow_merge_commit=false -F allow_rebase_merge=false \
  -f squash_merge_commit_title=PR_TITLE -f squash_merge_commit_message=PR_BODY \
  -F delete_branch_on_merge=true
```

### 2. main ブランチのルールセット

クラシックなブランチ保護を削除し, ルールセットに置き換えます. 内容は次のとおりです.

- PR を必須にする (承認数 0, Squash のみ)
- 必須チェックは `ci-success` と `pr-title`
- force push と削除を禁止する
- 管理者は PR 経由でのみバイパスできる (`actor_id: 5` は Admin ロール)

```bash
gh api -X DELETE "repos/$R/branches/main/protection"
gh api -X POST "repos/$R/rulesets" --input - <<'EOF'
{
  "name": "main",
  "target": "branch",
  "enforcement": "active",
  "conditions": { "ref_name": { "include": ["~DEFAULT_BRANCH"], "exclude": [] } },
  "bypass_actors": [
    { "actor_id": 5, "actor_type": "RepositoryRole", "bypass_mode": "pull_request" }
  ],
  "rules": [
    { "type": "deletion" },
    { "type": "non_fast_forward" },
    {
      "type": "pull_request",
      "parameters": {
        "required_approving_review_count": 0,
        "dismiss_stale_reviews_on_push": false,
        "require_code_owner_review": false,
        "require_last_push_approval": false,
        "required_review_thread_resolution": false,
        "allowed_merge_methods": ["squash"]
      }
    },
    {
      "type": "required_status_checks",
      "parameters": {
        "strict_required_status_checks_policy": false,
        "required_status_checks": [{ "context": "ci-success" }, { "context": "pr-title" }]
      }
    }
  ]
}
EOF
```

### 3. リリースタグのルールセット

`v*` タグの作成・更新・削除を管理者だけに許可します.

```bash
gh api -X POST "repos/$R/rulesets" --input - <<'EOF'
{
  "name": "release-tags",
  "target": "tag",
  "enforcement": "active",
  "conditions": { "ref_name": { "include": ["refs/tags/v*"], "exclude": [] } },
  "bypass_actors": [
    { "actor_id": 5, "actor_type": "RepositoryRole", "bypass_mode": "always" }
  ],
  "rules": [{ "type": "creation" }, { "type": "update" }, { "type": "deletion" }]
}
EOF
```

### 4. 脆弱性の非公開報告

```bash
gh api -X PUT "repos/$R/private-vulnerability-reporting"
```

### 5. ラベル

```bash
gh label create breaking-change --color B60205 --description "公開 API の互換性を壊す変更"
gh label create api-change --color FBCA04 --description "公式 API の仕様変更への追従"
```

### 6. Environment

ワークフローの environment ごとに, デプロイできるブランチやタグを制限します.

```bash
# integration / testpypi: main からのみ
for env in integration testpypi; do
  gh api -X PUT "repos/$R/environments/$env" --input - <<'EOF'
{ "deployment_branch_policy": { "protected_branches": false, "custom_branch_policies": true } }
EOF
  gh api -X POST "repos/$R/environments/$env/deployment-branch-policies" -f name=main -f type=branch
done

# pypi: v* タグからのみ
gh api -X PUT "repos/$R/environments/pypi" --input - <<'EOF'
{ "deployment_branch_policy": { "protected_branches": false, "custom_branch_policies": true } }
EOF
gh api -X POST "repos/$R/environments/pypi/deployment-branch-policies" -f name='v*' -f type=tag

# github-pages: 既存の main に加えて, リリース時のデプロイ用に v* タグを許可する
gh api -X POST "repos/$R/environments/github-pages/deployment-branch-policies" -f name='v*' -f type=tag
```

統合テスト用の API キーは, メンテナー自身が Secret に登録します. 値は対話的に入力します.

```bash
gh secret set HOTPEPPER_KEYID --env integration --repo "$R"
```

### 7. PyPI / TestPyPI の Trusted Publisher

PyPI と TestPyPI の管理画面 (Your projects → Manage → Publishing) で, 次の設定が登録されていることを確認します.

| 公開先 | Workflow | Environment |
| --- | --- | --- |
| PyPI | `publish.yml` | `pypi` |
| TestPyPI | `publish-dev.yml` | `testpypi` |

### 8. その他 (任意)

```bash
gh repo edit "$R" --add-topic hotpepper,api-client,python,pydantic,httpx
```

## GitHub Flow への移行 (初回のみ)

以前は `dev` ブランチを経由していました. 移行は次の順で行いました.

1. 移行用ブランチ (`dev` と `main` の履歴を統合済み) から `main` 宛ての PR を作成し, CI が通ることを確認します.
2. `dev` 由来のコミット履歴を残すため, この PR だけは **Create a merge commit** でマージします. 「リポジトリの初期設定」の 1, 2 はこのマージの後で適用します.
3. 「リポジトリの初期設定」の 1〜6 を適用し, Secret を登録します.
4. `gh workflow run integration.yml` と `gh workflow run docs.yml` を実行し, 成功することを確認します.
5. `dev` ブランチを削除します.

   ```bash
   git push origin --delete dev
   git branch -D dev
   ```
