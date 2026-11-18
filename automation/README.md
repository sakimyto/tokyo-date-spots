# Macの週次実行

`weekly.py`が1週分を直列に実行する。正本はこのディレクトリと[実行契約](../.loop/weekly.md)。Labelは`com.sakimyto.tokyo-date-spots-weekly`、金曜09:05 JST、`RunAtLoad=false`、初回は2026-11-20。Macがスリープ・停止中の起動時刻を厳密には保証しない。JST以外のMacではOSのcalendar解釈を確認してから使う。

実行コピー・config・state・lock・RESULTは`~/.codex/automation-state/tokyo-date-spots-weekly/`、plistは`~/Library/LaunchAgents/`。worktreeは`~/_pjsc/_wt`、収集・検査のスクラッチは`~/_pjsc/_work/date-spots-weekly-YYYYMMDD`。主checkoutはfetchと読み取りにだけ使う。Grokの9-05-botとsakimemo台帳は変更しない。

## 導入と確認

```bash
python3 -B -m unittest discover -s tests -p 'test_*.py'
python3 automation/weekly.py --dry-run
python3 automation/install.py --load
launchctl print "gui/$(id -u)/com.sakimyto.tokyo-date-spots-weekly"
```

ロード時は実行しない。登録内容はWeekday=5、Hour=9、Minute=5、RunAtLoad=falseと実行先を読み戻す。`launchctl print`が次の絶対日時を表示しない場合は、JSTの現在時刻と登録calendarから次の金曜日を算出して記録する。

Claudeは`claude-opus-5-5`を指定し、読み取り・Web取得だけのツールで構造化データを返す。指定した主モデルをmodelUsageの先頭・canonicalModel・正のoutputTokensと照合し、違えば停止する。後続の補助モデルとWeb検索利用は許容する。候補0件・除外0件はRESULT.mdに「変更なし」とだけ書く。新規の有効候補30件未満は適用・pushしない。

Codexの実装・確認・公開は別セッションで順に行い、追加AI起動は禁止する。モデル・reasoningは既存の選択を使う。実装・公開はworktree操作・通常GitHub公開・既存hook・配備確認を要するためCLIの`danger-full-access`を使い、確認は`read-only`にする。`dangerously-bypass-*`やhook回避は使わない。理由は本人が依頼したローカルMacでの週次公開、範囲はこの2repositoryの週次更新、期限は定期処理の停止まで、承認者はsakimyto、承認日は2026-11-13。これは新しいログイン・権限・課金・秘密・外部通知の承認ではない。

## 停止と再開

`~/.codex/automation-state/tokyo-date-spots-weekly/STOP`を作ると次の工程を開始しない。現在のCLIが実行中なら完了を待ち、他のプロセスを止めない。スケジュールだけ外すには、実行中でないことを確認して`launchctl bootout gui/<uid>/com.sakimyto.tokyo-date-spots-weekly`を使う。stateとworktreeは保存し、branchを消さない。

中断・timeout・認証不足・失敗は`needs-reconciliation`で止まる。`state.json`のphase、worktree、commit、PR、CI、本番を親担当が照合する。STOPを解除し、入力・検査等を直した後は`python3 ~/.codex/automation-state/tokyo-date-spots-weekly/weekly.py --resume YYYY-MM-DD`で再開する。公開中の結果不明はこのコマンドでも再送しない。親担当がreceiptを確定してstateを正しい結果へ更新する。実行中のlockや未pushの変更を消さない。

同じ日付の完了は再実行しない。別の日付が未解決のままなら新しい週も止め、二重公開を防ぐ。全Mac・旧routineとの分散排他は持たないため、旧9-05-botの停止は親担当が別途行う。

## 検査と保管

ユニット検査は作業なし、停止中、同じ日付、入力不正、認証相当のCLI失敗、確認不承認、公開中断の再開を扱う。Claude/Codexの実呼び出しは模擬し、schemaと状態のガードを確認する。本物の定期実行は初回予定日まで未実施であり、模擬検査を認証や将来の公開成功の保証としない。

各CLIの上限は1時間。Codexの委任には導入済みの共有`curumi-codex-delegate/scripts/delegate-task.mjs`を使い、同じ実行の結果を待つ。timeoutは結果不明として止まり、状態を失わない。生のCLIログは工程終了時に削除する。結果はローカルのRESULT.mdへ短く残し、Slack・メール・追加の通知ファイルを作らない。収集成果物・検査の短い記録・復旧に必要な未完了データだけを保持し、完了後の画像・動画・大量ログ・比較用コピーは片付ける。公開ソース・履歴・制作画像・未pushの差分は保持する。

## Codex呼び出しの情報受け渡し

共有runnerは環境変数を最小限に減らす。schema・最終応答先・実Codexの場所は、各工程専用のentry.pyと隣接するentry.jsonで渡す。環境変数で渡すのはrunnerが起動するentry.pyの場所だけとし、子に引き継がれない値へ依存しない。工程完了時にentry・binding・一時応答を片付け、結果receiptだけを保持する。schemaと既存Codex profile/権限・独立レビュー・公開条件は変えない。収集の主モデルは現行のOpus 5.5に合わせる。

旧env方式の失敗を検出し、最小環境のwrapper検査と実接続の試運転を分けて記録する。モデルの利用枠不足をmockで解消済みと扱わず、実モデル起動の確認が終わるまで初回readyとしない。

再配置は既存のSTOPを置き、実行中0と未確定の週次stateがないことを確認する。installは同じrun.lockを取得し、実行中・未確定ではコピーを始めない。既存configの接続と追加設定を保持し、実行コピーのhash一致とplistの読戻し後にSTOPを外す。

匿名の公開照合は識別可能なTokyoDateSpotsWeeklyのUser-Agentと、HTML/JSONに対応したAcceptを送る。ログイン・cookie・特別な認証を使わず、403などの取得失敗を0件成功にしない。
