{{date}}の週次更新を実装する。東京のworktreeは{{worktree}}、収集成果物は{{scratch}}/collect。採用判断はClaude成果物を正とし、pipeline/check_collection.pyによる検査結果に従う。PUBLISH.mdと.loop/weekly.mdを読む。

新しい週次batchへ追加し、終了イベントを全ての必要な元ソースと最終JSONから外す。既存順のmerge→rain→build→CSV生成を実行し、残存行の全フィールド、JSON/CSV/HTML同期、再実行一致を検査する。python3 -B -m unittest discover -s tests -p 'test_*.py' と tests/pwtestのpnpm testを通す。検査を緩めない。

sakimyto.comも同じデータで更新する。主checkoutはdirtyで触れない。既存のorigin/mainから{{site_worktree}}を用意し、既存の同用途があれば再利用する。worktree上限5本を守る。固定旧ID表・安定ID関数・保存履歴と残存画像の同一性を保ち、新規行は既存のジャンル別イラストを再利用して生成の表示を付ける。サイト側はCIと同じNode 22をPATHの先頭に置き、TMPDIRは当週のscratch、PlaywrightはAI専用ブラウザ配置を使う。既存全体テスト・Biome・build・同一性と反例の検査を通す。既存理由の失敗でも緩めず止める。

実装・関係文書・機密検査・通常hook付きcommitまで行う。push、PR、merge、公開はこの工程では行わない。別AI・別CLI・subagentを起動しない。force、rebase、--no-verify、主checkoutの編集、台帳の編集、9-05-botの操作、外部通知、秘密の読み書きは禁止。scratchへ短い検証結果を保存し、status（ready/no-change/blocked）、summary、tokyo_head、site_head、site_worktreeをschemaで返す。
