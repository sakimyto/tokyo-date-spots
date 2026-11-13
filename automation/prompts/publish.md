{{date}}の検証済みcommitを通常公開する。東京{{worktree}}のHEADは{{tokyo_head}}、サイト{{site_worktree}}のHEADは{{site_head}}。別セッションのreviewが承認済み。開始前に両HEADとcleanを確認し、一致しなければ公開しない。実装を追加変更しない。PUBLISH.mdと各repositoryの品質・公開手順を守る。

東京のbranchを通常pushしPRを作り、HEADとCIを確認してmainへ通常mergeする。Pages built、公開HTML HTTP 200、公開spots.jsonの全行一致を確認する。サイトは通常hookを省略せずpush・PRを行い、全CI成功後scripts/merge-when-required-checks-pass.sh経由でmergeする。mainのCIと本番/lab/odekake、spots APIを確認する。結果不明の送信は繰り返さず、PR/commit/CI/本番のreceiptで照合する。

force、rebase、--no-verify、hookや品質ゲートの回避、主checkoutの編集、台帳の編集、9-05-botの操作、外部通知、新しいログイン・権限・秘密・課金は禁止。追加AIを起動しない。実装/検査の不一致があればstatus=blocked。status（published/blocked）、summary、tokyo_pr、site_pr、tokyo_commit、site_commit、pages_match、site_matchをschemaで返す。
