# セキュリティポリシー

## サポート対象のバージョン

セキュリティ修正は **最新のリリース** に対してのみ提供します. 古いバージョンをお使いの場合は, 最新版へ更新してください.

| バージョン | サポート |
| --- | --- |
| 最新リリース | ✅ |
| それ以前 | ❌ |

## 脆弱性の報告

脆弱性を見つけた場合は, **公開 Issue には書かず**, GitHub の Private vulnerability reporting で非公開に報告してください.

1. [Security タブの「Report a vulnerability」](https://github.com/paperlefthand/hotpepper-gourmet/security/advisories/new) を開きます.
2. 影響を受けるバージョン, 再現手順, 想定される影響を記入して送信します.

報告はメンテナーだけが閲覧できます. 内容を確認して返信し, 修正版のリリース後に Security Advisory として公開します. 個人で運営しているプロジェクトのため, 返信までに 1 週間程度かかることがあります.

詳しい手順は [GitHub のドキュメント](https://docs.github.com/ja/code-security/security-advisories/guidance-on-reporting-and-writing-information-about-vulnerabilities/privately-reporting-a-security-vulnerability) を参照してください.

## 利用者の方へ: API キーの取り扱い

pygourmet はホットペッパー Web サービスの API キー (`keyid`) をクエリパラメータとして送信します.

- API キーをソースコードに直接書いたりコミットしたりせず, 環境変数や `.env` ファイル (Git 管理外) から読み込んでください.
- Issue やログにリクエスト URL やレスポンスを貼り付ける際は, API キーを必ず伏せてください.
- キーが漏洩した場合は, [リクルート Web サービス](https://webservice.recruit.co.jp/) の案内に従って速やかに対処してください.
