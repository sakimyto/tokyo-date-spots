# 東京・関東 デート候補カタログ

東京・関東圏のデート・おでかけ先候補を一覧できる静的ページです。ホテルビュッフェ・スイーツビュッフェ・食べ放題、期間限定のキャラクター・コラボイベント、赤ちゃん連れ(0〜1歳)向けのイベント・スポットも載っています。現在の収録件数は公開ページに表示します。

- 公開ページ: https://sakimyto.github.io/tokyo-date-spots/
- `index.html` … 一覧ページ(1ファイル完結。ジャンルタブ・検索・エリア絞り込み・お気に入り・「今やっている」「これから」「👶赤ちゃんOK」・ランダム。会期が終わったものは自動で非表示)
- `spots.json` / `spots.csv` … 同じデータ(名前、エリア、説明、公式URL、会期、会場、予約・整理券、対象年齢、授乳室・おむつ替え・ベビーカーなど)
- `tpl.html` … ページのテンプレート
- `build.py` … `spots.json` と `tpl.html` から `index.html` を生成(`python3 build.py 2026-10-20` のように最終更新日を渡す)
- `pipeline/` … 採用済みソース、merge、雨の日OKの付与、CSV生成
- `tests/pwtest/` … JSONから期待値を求めるMac用の画面テスト
- [PUBLISH.md](PUBLISH.md) … Macでの再構築・週次公開、作業場所、検査手順
- [automation/README.md](automation/README.md) … 金曜09:05 JSTのMac launchd、停止・復旧、結果の保存

会期・営業状況は変わることがあります。出かける前に各公式サイトで確認してください。
