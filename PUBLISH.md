# Macでの再構築・週次公開

公開先は [GitHub Pages](https://sakimyto.github.io/tokyo-date-spots/)、mainのルート。`index.html`、`spots.json`、`spots.csv`、`build.py`、`tpl.html`、`README.md`をルートに置く。

## 作業場所

主checkout `~/_pjsc/tokyo-date-spots`は直接編集しない。週次の作業は`~/_pjsc/_wt/`、スクラッチは`~/_pjsc/_work/`を使う。2026-11-13の作業場所は`~/_pjsc/_wt/tokyo-date-spots-weekly-20261113`。移管元は11月6日更新済みの838行版。

## 再構築

リポジトリのルートから実行する。出力先はrepository外の専用ディレクトリにする。採用済みの公開JSONを入力とし、ソースを次の順で重ねる。

```bash
weekly_date="$(TZ=Asia/Tokyo date +%F)"
python3 pipeline/rebuild.py --date "$weekly_date" --output "$HOME/_pjsc/_work/date-spots-rebuild-$weekly_date"
```

実行順は`merge_collab.py`、`merge_buffet.py`、`merge_miniature.py`、`merge_baby.py`、`merge_batch2.py`、`apply_rain.py`、ルートの`build.py`、`sync_csv.py`。**build.pyはCSVを再生成しない。必ず最後にsync_csv.pyを実行する。** 再mergeによる終了行の復活を防ぐため、終了したイベントは該当ソースと最終JSONの両方から外す。映画公開日・開業日だけの記述、常設は終了とみなさない。

`data2.txt`、`verify.py`、`build_verify.py`は元データのURL再検証用。通常の週次では呼ばない。オンライン再検証だけでは、過去に採用した全行の情報を再現できないため、出力を直接公開しない。再構築は採用済みJSONから始める。

## 画面とデータの検査

```bash
cd tests/pwtest
pnpm install --frozen-lockfile
pnpm test
pnpm run live
```

Playwrightは固定版を使い、AI専用Chrome for Testingをheadlessで起動する。既定のブラウザ配置は`~/_pjsc/_work/ai-browser/browsers/`。`CHROME_PATH`を使う場合も、この配下の専用バイナリを指定する。通常のChromeや既存セッションに接続しない。作成したページとプロセスは成功・失敗時とも閉じる。検証用プロファイルと一時ファイルも片付ける。スクリーンショットは通常生成しない。

期待件数と行集合はルートの`spots.json`から算出する。`TEST_DATE=YYYY-MM-DD`、`SPOTS_ROOT=/絶対パス`で時計と検査対象を指定できる。標準時計は公開HTMLの最終更新日（JST）。未来の終了非表示も検査する。

## 週次適用と公開

1. Claude Codeの`COLLECTED.json`、`REMOVE.json`、`NOTES.md`、`MODEL.txt`を受け取る。採用判断を作り替えず、必須フィールド・型・既存名・クエリを除いた公式URLの重複を機械検査する。不備行は理由を記録して除外する。有効追加30件未満なら週次適用とpushを止める。
2. 追加を新しい`batchN_weekly.py`へ収録し、mergeの読み込みへ加える。終了確定イベントを各元ソース・最終JSONから外す。親子・話題の複製も確認する。
3. 上記の再構築を当週の日付で実行する。再構築前後の既存行維持、終了行の再混入なし、JSON・CSV・HTML一致、再実行の一致を検査する。公開5ファイルをルートへ反映し、画面テストをもう一度通す。
4. 差分と機密検査を確認し、日本語のcommitを作る。作者は必要に応じて`sakimyto <21049958+sakimyto@users.noreply.github.com>`を使う。force push、rebase、hookの省略は禁止。
5. branchをpushしてPRを作る。HEAD一致と必要なチェックを確認して通常mergeする。Pagesが`built`になるまで待ち、公開HTMLがHTTP 200、公開JSONがローカルと全行一致することを確認する。
6. sakimyto.comの`/lab/odekake`は同じデータを使う。主checkoutを触らず、origin/mainから作業worktreeを用意する。既存の安定IDを保持し、全体検査と同一性の反例検査が通ってからpushする。PRのmergeは対象repositoryの`scripts/merge-when-required-checks-pass.sh`を使い、本番とAPIを確認する。

雨の日OKは主な体験が屋内で完結すると公式情報で確認できる場合のみ付ける。`rain_manual.json`、話題の元ジャンル、`apply_rain.py`の個別補正・ジャンル既定値の順で判断する。mergeの後は必ず全行に付け直す。

移管の仕様・反例検証と保証範囲は[Mac移管の記録](docs/mac-migration.md)を参照する。定期実行は手動の週次公開が一度完了した後に有効化する。


2026-11-13の独立レビュー修正は、本人が指定した公開済みデータの訂正として進める。追加31行の有効件数を28件、上映館未確認を3件へ訂正し、未確認印付きの掲載行は保持する。新規の有効追加30件以上という週次適用条件は満たしておらず、通常の収集検査はready=falseを維持する。埋め草の追加はしない。検証と根拠は[レビュー修正の記録](docs/review-fix-20261113.md)を参照する。
