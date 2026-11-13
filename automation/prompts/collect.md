今日は{{date}}（Asia/Tokyo）。東京・関東のおでかけ先を公式ページの本文で確認して30件以上追加し、終了した期間イベントを除外候補にする。採用済みJSONは{{worktree}}/spots.json。主checkoutを変更しない。実装・git・公開・外部送信・課金・秘密の操作、追加AI起動は禁止。返答は指定schemaのJSONだけにする。

既存の名前、既存と候補間のクエリを除いた公式URLが同じ行は追加しない。映画・舞台・演芸・工場見学・キャラクター・季節イベントなどを広く扱う。公式本文で会期・会場が確認できないものは追加しない。予約要否・残席・料金に記載がなければ未確認とする。雨の日OKは主な体験が屋内で完結すると確認できる場合のみ。子どもの生年月日等の個人情報や、抽選期限を急かす文言は含めない。

additionsは各行genre,name,area,desc,url,rain_ok,period,venue,reservation,kind,period_note,baby_ok,url_status,url_note,source_checked_at,source_evidence。kindはイベントまたは常設、url_statusはok、source_checked_atは「{{date}} JST」。source_evidenceは公式本文の短い根拠。removalsは既存行と完全一致するgenre,name,period,urlにreasonを付ける。終了日は今日より前で、年付き期間または「1日のみ」の行だけを候補にする。常設・開業日・公開日だけの行は終了にしない。話題の複製にも注意する。notesに主な候補、未確認・見送り、工場の予約状況の変更、保証範囲を書く。
