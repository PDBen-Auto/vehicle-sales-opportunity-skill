# 乗り物販売可視化と機会調査

[简体中文](README.zh-CN.md) | [English](README.en.md) | [日本語](README.ja.md) | [한국어](README.ko.md) | [Deutsch](README.de.md) | [Français](README.fr.md) | [Español](README.es.md) | [Português](README.pt.md)

ユーザーが明示した言語で出力し、指定がなければ依頼文の言語に従います。コマンド、スキル ID、JSON キー、列挙値、単位、引用原文は保持します。翻訳と原文を分け、言語から国・通貨・法域を推定しません。詳細仕様の該当資料を読み、既存の検証と権限確認を適用します。

## 導入と利用

リポジトリを取得し、下記のスキルディレクトリを既存の references、scripts、assets などと一緒にホストのスキル用ディレクトリへコピーします。名前と SKILL.md は変更しません。説明言語を変えるだけなら再導入は不要です。導入用コマンドの掲載は、導入済みや有効化済みを意味しません。

```sh
git clone https://github.com/PDBen-Auto/vehicle-sales-opportunity-skill.git
```

## 乗り物販売可視化と機会調査

`vehicle-sales-opportunity`

自動車、二輪、UTV、ATV、船の既存数量を可視化し、同期間比較と根拠付き機会調査を設計します。

スキルディレクトリ: `skills/vehicle-sales-opportunity`

**実装の根拠と依存関係**

許可済みデータと市場/暦期間/指標/単位、Python 3.10+ 標準ライブラリ、画面検査用ブラウザ。オフライン中核はアカウント/API 不要。調査検証には製品・利用者・適合・原価資料。

**入力**

月次 dataset JSON、対応する基準月範囲、新規出力先は必須。任意の閾値/企画/根拠。欠損、assetType、metricKind を保持。年/四半期を月へ等分しません。

**出力**

dashboard.html、analysis.json、opportunities.json、report.md、qa.json。research-review.md は別途作成。候補と算術 PASS は需要・適合・ROI の証明ではありません。

[実行手順 · 制約と停止条件 · 依頼例](skills/vehicle-sales-opportunity/references/i18n/ja.md)

> 次のスキルを使用してください： `$vehicle-sales-opportunity` — 米加墨の1～6月を前年同月と比較。販売+30%を用品需要+30%の証拠にしません。日本語で回答し、根拠、不明点、操作権限を維持してください。

[Online examples](https://pdben-auto.github.io/vehicle-sales-opportunity-skill/) · [UTV case](https://pdben-auto.github.io/vehicle-sales-opportunity-skill/cases/utv-atv/) · [Original vehicle dashboard](https://north-america-vehicle-dashboard.pages.dev/)

## 言語対応と検証

本書は目的、前提、入出力、手順、例、制約をまとめた日本語運用ガイドです。全参考資料の逐語訳ではありません。詳細技術資料、過去事例、スクリプトのエラー、サンプル画面、画像は原言語のままです。必要に応じて日本語で説明できます。構造・リンク・重要制約を確認していますが、各言語の母語話者による校閲は未実施です。

納品前に入力、根拠、欠損、出力ファイルと元の完了条件を照合します。未実行の工程は未検証とし、終了コードの成功を業務上の検証成功と混同しません。
