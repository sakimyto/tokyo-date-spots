# 東京おでかけ先の週次更新（odekake-weekly）

実行器に依らない入口。実行器の登録文は「origin/main の `ops/automation/odekake-weekly.prompt.md` を読み、その指示に従って実行する」だけにする。手順はここに書き、登録文へ書き足さない。

この処理の中身は決まった手順のスクリプト `automation/weekly.py` である。実行器はその**実行コピー**を、launchd の plist と同じ変数で1回呼ぶだけにする。収集・実装・確認・公開の判断を、実行器の会話で代わりに行わない。

## 正本

- [実行契約](../../.loop/weekly.md)、[導入・停止・再開](../../automation/README.md)、[公開手順](../../PUBLISH.md)
- 実行コピーと状態: `~/.codex/automation-state/tokyo-date-spots-weekly/`（`automation/install.py` が配置する）
- 処理の一覧: [manifest](manifest.json)、引き継ぎ: [docs/automation-handoff.md](../../docs/automation-handoff.md)

## 実行

`S=~/.codex/automation-state/tokyo-date-spots-weekly`、`P=~/Library/LaunchAgents/com.sakimyto.tokyo-date-spots-weekly.plist` とする。

1. **旧の登録が残っていないか。** `launchctl print gui/$(id -u)/com.sakimyto.tokyo-date-spots-weekly` が成功したら（launchd がまだ登録中）、何もせず「launchd が登録中のため実行しない」と報告して終わる。旧と新を同じ週に両方動かさない。
2. **止める印と未確定の回。** `$S/STOP` があれば、何もせず報告して終わる。`$S/state.json` に `published`・`no-change` 以外の行があれば、その日付・phase・reason を報告して終わる。照合と `--resume` は親担当が行う（`automation/README.md` の「停止と再開」）。自分で再開・再送しない。
3. **実行コピーが repo と同じか。** `$S/weekly.py` と origin/main の `automation/weekly.py` の sha256 を比べる。違えば報告して終わる（再配置は `install.py` と README の手順で親担当が行う）。
4. **plist の環境で切り離して起動する。** plist から python・PATH・TMPDIR を読み、会話の環境変数を引き継がない（launchd が自動で足す変数と完全に同じかは未確認。[引き継ぎ](../../docs/automation-handoff.md)の「移す前に満たす条件」で確かめる）。

   ```sh
   PY=$(plutil -extract ProgramArguments.0 raw "$P")
   EP=$(plutil -extract EnvironmentVariables.PATH raw "$P")
   ET=$(plutil -extract EnvironmentVariables.TMPDIR raw "$P")
   cd "$S" && nohup env -i HOME="$HOME" USER="$USER" LOGNAME="$USER" PATH="$EP" TMPDIR="$ET" TZ=Asia/Tokyo \
     "$PY" "$S/weekly.py" >>"$S/orca.out.log" 2>>"$S/orca.err.log" </dev/null &
   echo $!
   ```

   `weekly.py` は金曜 09:05 JST より前なら何もせず exit 0 になる。別の回が `run.lock` を持っていれば、これも何もせず exit 0 になる。
5. **終わりを待つ。** 起動した pid が消えるまで、10分おき程度に確かめる。上限は約4時間15分（収集1時間と Codex 3工程の各1時間に余裕を足したもの）。上限を過ぎても pid が残っていれば、止めずに「実行中のまま」と報告する。プロセスを kill しない。
6. **報告する。** `$S/RESULT.md` の内容、`state.json` の当日の行（status・phase・reason・PR）を、既存の受付へ短く返す。RESULT.md が当日の内容でなければ「結果不明」と書く。`orca.err.log` の中身はそのまま貼らない。

## してはいけないこと

- `--resume` の実行、state.json・RESULT.md・STOP の編集、worktree・branch の削除。
- `weekly.py` の工程（収集・実装・確認・公開）を会話で代わりに行うこと、追加の AI の起動。
- launchd の登録の操作（`launchctl bootstrap`・`bootout`・`kickstart`）。引き継ぎ手順の担当者だけが行う。
- Slack・メール・X など外部への通知。結果は受付への報告だけ。
- force push・rebase・hook 省略・秘密情報の読み出し。

## 実行器ごとの差

- **launchd（現在）**: plist が `weekly.py` を直接呼ぶ。この文書の 1〜6 は使わない。
- **Orca**: 登録文は上の1文。`--precheck` に有効化の印の判定を入れる（[引き継ぎ](../../docs/automation-handoff.md)）。作業場所は既存の checkout（`--workspace`）でよい。repo の内容は読むだけで、書き込みは実行コピーの state 側で起きる。
- **ほかの実行器（Codex・Claude・t3code など）**: 同じ登録文で、この 1〜6 を行う。会話の外で長いプロセスを見届けられない実行器なら、launchd に残す方を選ぶ。
