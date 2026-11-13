<!-- makeloop-source: d7cce9dbd6e52389884ed72029367583c89781f672d1a56b05aaf323a83328e4; personal-rules: none -->
# 毎週の東京おでかけ更新

方式はopenの週次トリガーと、1週分の収集・実装・独立確認・公開で閉じる実行。金曜09:05 JSTにMacのlaunchdが1回起動する。最初の対象日は2026-11-20で、過去分の再実行はしない。アプリ定期タスク、クラウド実装、CloudAgentは使わない。

正本はこのrepositoryの`automation/`と[PUBLISH.md](../PUBLISH.md)。実行コピー・cursor・lock・停止ファイル・結果は`~/.codex/automation-state/tokyo-date-spots-weekly/`。1週のキーはJSTの日付。`state.json`へ実行前にphaseをpendingとして原子的に保存し、確認した出力とcommitを記録してから進む。成功済みの日付は再実行しない。実行中のlockは同一Macでの二重実行を防ぐ。別環境の旧処理との排他は保証せず、9-05-botの停止は親担当が行う。

観測対象は、当週の公式情報と採用済みJSON。Claude Code `claude-fable-5-2`が読み取り用ツールだけで収集し、構造化出力を返す。実モデル名をCLIのmodelUsageで照合する。parserが成果物を保存し、必須フィールド・URL重複・終了条件・新規30件を機械検査する。追加も除外も0なら結果は「変更なし」の1行だけとし、追加調査・通知をせず終了する。入力欠落やCLI失敗を0件扱いしない。

Codexの実装セッションは元データの採用判断を変えず、両repositoryの作業branchへ実装・検証・commitする。この段階ではpushしない。別のread-only Codexセッションが仕様・commit・実行証拠を検査する。実装担当の自己申告は独立レビューとしない。reviewのHEADが両方一致したときだけ、別のCodexセッションが許可済みの通常push・PR・merge・配備確認を行う。モデル・reasoningはCLIの既存選択を保持する。子CLIは追加AIを起動しない。

完了の証拠はJSON/CSV/HTML同期、再構築の冪等性、全行の採用・除外・維持、画面テストと変種検出、サイト全体の既存品質ゲート、安定ID全列挙、通常hook、CI、Pages built、HTTP 200、両公開JSON/APIとの一致。成功した一部の検査だけで公開へ進まない。差分・入力が変わらない検査を繰り返さず、失敗した箇所の修正と必要な再検査を行う。

STOPがあれば新しい工程を開始しない。認証不足・検査失敗・入力不足・レビューの指摘・timeoutでは結果をRESULT.mdへ残して止まる。各CLIのtimeoutは停止のための実装上限であり、トークン予算ではない。途中中断のpendingは適用結果不明として残す。次回も無条件に送信し直さず、git/PR/CI/本番のreceiptで照合してから親担当が`--resume YYYY-MM-DD`を実行する。認証・新しい権限・課金・force・rebase・hook省略・秘密情報・既存routineの操作へ迂回しない。

結果はRESULT.mdだけに短く記録し、Slack・メール等の経路を作らない。必要な学びは`automation/learnings.md`のUNVERIFIEDへ証拠付きで残し、1回の失敗からglobal ruleを追加しない。導入・停止・復旧・検証方法は`automation/README.md`に置く。
