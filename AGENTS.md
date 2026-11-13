# 東京おでかけ先一覧

公開元はmainのルート。採用済みデータは`spots.json`、テンプレートは`tpl.html`。週次の再構築・公開は[PUBLISH.md](PUBLISH.md)、Macの定期処理は[automation/README.md](automation/README.md)と[実行契約](.loop/weekly.md)を読む。

通常の変更は既存の作業checkoutで行う。週次処理では主checkoutを直接編集せず、`~/_pjsc/_wt`の当週worktreeと`~/_pjsc/_work`のスクラッチを使う。Claudeの採用成果物を機械検査し、有効追加30件未満では週次適用・pushしない。常設や公開日・開業日だけの行は終了として消さない。

```bash
python3 -B -m unittest discover -s tests -p 'test_*.py'
cd tests/pwtest
pnpm install --frozen-lockfile
pnpm test
```

期待件数を毎週手で書き換えず、JSONの行集合を使う。元ソース変更後は全merge、雨の日OKの付与、HTML、CSVの同期と再実行一致を確認する。公開JSONの全行一致まで確認する。force push、rebase、hook省略はしない。作成したブラウザのページ・プロファイル・一時出力は終了時に片付ける。

依頼・定期実行の台帳は受付担当が管理する。2026-11-13の作業ではsakimemoの台帳と9-05-botを変更しない。
