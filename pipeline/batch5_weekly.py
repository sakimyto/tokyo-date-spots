"""2026-11-06週次追加。公式本文で会期・会場を確認。空席と記載のない予約要否は未確認。"""
# Rはmerge_batch2.pyの共通ヘルパーを使う。
ENGE='歌舞伎・落語・お笑い・演芸'
SEASON='季節イベント'
MUSEUM='美術館・博物館'
UENO='https://www.kensetsu.metro.tokyo.lg.jp/jimusho/toubuk/ueno/event'
TICKET='公式の電話・インターネットでチケット予約。現在の残席は未確認'
UNCONFIRMED='予約要否・料金の詳細は案内ページに記載なし。未確認のため主催者へ確認'
ROWS5=[
R(FILM,'映画『クレイフェイス』','東京都 都内・関東の劇場','DCスタジオの心理スリラー。公式劇場一覧にTOHOシネマズ日比谷・新宿などを掲載','https://clayface-movie.jp/',True,period='2026年10月30日公開',venue='TOHOシネマズ日比谷・新宿ほか',reservation='各上映館の鑑賞券が必要。販売日・空席は各劇場で確認',kind='イベント',note='公開日のみ。上映終了日は劇場ごとに異なる'),
R(FILM,'映画『ないものねだりの君に光の花束を』','東京都 都内・関東の劇場','原菜乃華・作間龍斗主演。汐見夏衛の小説を実写映画化','https://naihanamovie.jp/',True,period='2026年11月20日公開',venue='東京・関東の上映館は公式THEATERで要確認',reservation='公式サイトにムビチケ案内あり。座席予約・空席は上映館で確認',kind='イベント',note='公開日を配給会社ショウゲートの公式発表でも確認。上映終了日は未定',unote='THEATERはアクセス制限あり。個別上映館と座席販売は未確認'),
R(FILM,'映画『ファーザーマザーシスターブラザー』','千代田区 有楽町ほか','ジム・ジャームッシュ監督作品。公式劇場一覧で都内の11月20日公開を確認','https://gaga.ne.jp/FMSB_NOROSHI/theater/',True,period='2026年11月20日公開',venue='ヒューマントラストシネマ有楽町・渋谷、新宿ピカデリーほか',reservation='ムビチケ前売券の案内あり。座席予約・空席は各劇場で確認',kind='イベント',note='上映期間・時間は劇場へ確認'),
R(FILM,'映画『彼女にあったら、よろしくと』','武蔵野市 吉祥寺','平塚直隆監督・脚本。東京はアップリンク吉祥寺で12月4日公開','https://kanoyoro-movie.com/',True,period='2026年12月4日公開',venue='アップリンク吉祥寺',reservation='ムビチケオンライン販売の告知あり。上映回・座席の販売状況は未確認',kind='イベント',note='東京の公開日を掲載。11月27日は鹿児島先行公開'),
R(STAGE,'日生劇場 オペラ『ドン・ジョヴァンニ』','千代田区 有楽町','モーツァルトのオペラを日生劇場で上演','https://opera.nissaytheatre.or.jp/info/dongiovanni2026/',True,period='2026年11月14日〜2026年11月15日',venue='日生劇場',reservation='一般発売6月26日11時開始。日生劇場Webチケット等で購入。残席未確認',kind='イベント'),
R(STAGE,'日生劇場 オペラ『夕鶴』','千代田区 有楽町','日本オペラ振興会主催、日生劇場共催。新日本フィルハーモニー交響楽団が演奏','https://opera.nissaytheatre.or.jp/info/yuzuru2026/',True,period='2026年11月27日〜2026年11月29日',venue='日生劇場',reservation='一般発売5月15日10時開始。日本オペラ振興会・日生劇場Web等で購入。残席未確認',kind='イベント'),
R(ENGE,'11月国立演芸場寄席(すみだトリフォニーホール小ホール)','墨田区 錦糸','13時開演、16時終演予定。落語・漫才・浪曲・曲芸の寄席','https://www.ntj.jac.go.jp/schedule/engei/2026/1102/',True,period='2026年11月16日〜2026年11月20日',venue='すみだトリフォニーホール小ホール',reservation='全席指定。10月18日10時から電話・Web予約。残席がある場合のみ会場で当日券',kind='イベント',note='国立演芸場本館ではなく錦糸町で開催。一般2,300円'),
R(ENGE,'国立劇場11月舞踊公演 お話と実演－舞と能の身体性－','渋谷区 千駄ヶ谷','19時開演。舞と能の実演とお話を通じて身体表現に触れる','https://www.ntj.jac.go.jp/schedule/kokuritsu_s/2026/0811/',True,period='2026年11月16日 1日のみ',venue='国立能楽堂',reservation=TICKET,kind='イベント'),
R(ENGE,'国立劇場11月舞踊公演 舞の会－京阪の座敷舞－','渋谷区 千駄ヶ谷','15時開演。京阪の座敷舞を紹介する舞踊公演','https://www.ntj.jac.go.jp/schedule/kokuritsu_s/2026/0811/',True,period='2026年11月17日 1日のみ',venue='国立能楽堂',reservation=TICKET,kind='イベント'),

R(ENGE,'国立能楽堂11月企画公演 琵琶と能楽 大楠公・伯養・楠露','渋谷区 千駄ヶ谷','18時30分開演。筑前琵琶『大楠公』、狂言『伯養』、能『楠露』','https://www.ntj.jac.go.jp/schedule/nou/2026/85033/',True,period='2026年11月20日 1日のみ',venue='国立能楽堂',reservation='10月10日10時から電話・Web予約。現在の残席は未確認',kind='イベント'),
R(ENGE,'国立能楽堂11月企画公演 琵琶と能楽 先帝御入水・碇潜','渋谷区 千駄ヶ谷','13時開演。平曲『先帝御入水』と能『碇潜』。日本語・英語字幕あり','https://www.ntj.jac.go.jp/schedule/nou/2026/85034/',True,period='2026年11月21日 1日のみ',venue='国立能楽堂',reservation='10月10日10時から電話・Web予約。現在の残席は未確認',kind='イベント'),

R(ENGE,'浅草演芸ホール 2026年11月中席前半','台東区 浅草','落語芸術協会の中席前半。昼の部11:40〜16:30。落語・講談・曲芸など','https://www.geikyo.com/schedule/jyoseki_detail?id=17616',True,period='2026年11月11日〜2026年11月15日',venue='浅草演芸ホール',reservation='入場方法・料金は浅草演芸ホール公式で確認',kind='イベント',unote='予約要否の詳細は番組ページに記載なし。未確認'),


R(SEASON,'伊ルミネーション -ISETAN Illumination- 2026','新宿区 新宿','本館屋上のイルミネーション。17〜20時、初日は19時開始。ツリー装飾は12月25日まで','https://www.mistore.jp/shopping/event/shinjuku_e/christmas_event_10',False,period='2026年11月11日〜2027年2月7日',venue='伊勢丹新宿店 本館屋上 アイ・ガーデン',reservation='点灯体験イベントは抽選。通常観覧の予約要否は未確認',kind='イベント',note='12月26日〜1月5日はイルミネーション休止',unote='通常観覧の予約要否は公式本文に記載なし。未確認'),
R(SEASON,'TORANOMON HILLS CHRISTMAS 2026','港区 虎ノ門','虎ノ門ヒルズ各所の装飾・イルミネーション。ステーションアトリウムのツリーは11月24日から','https://www.toranomonhills.com/events/2026/11/0295.html',False,period='2026年11月12日〜2026年12月25日',venue='虎ノ門ヒルズ各所',reservation='装飾観覧の予約要否は未確認。飲食企画は店舗別の予約案内を確認',kind='イベント',unote='装飾観覧の予約要否・料金は公式本文に記載なし。未確認'),


R(SEASON,'2026青森人の祭典','台東区 上野','一般社団法人東京青森県人会による催し。公園公式で日程・場所を確認',UENO,False,period='2026年11月14日〜2026年11月15日',venue='上野恩賜公園 竹の台広場(噴水広場)',reservation=UNCONFIRMED,kind='イベント',unote='時間・料金・予約要否は未確認'),
R(SEASON,'伊賀上野NINJAフェスタ2026 in上野恩賜公園','台東区 上野','伊賀上野NINJAフェスタ実行委員会による催し。公園公式で会期・場所を確認',UENO,False,period='2026年11月21日〜2026年11月23日',venue='上野恩賜公園 竹の台広場(噴水広場)',reservation=UNCONFIRMED,kind='イベント',unote='時間・料金・予約要否は未確認'),
R(SEASON,'戦国武将EXPO2026','台東区 上野','SAMURAIフェス実行委員会による催し。公園公式の開催予定を確認',UENO,False,period='2026年11月26日〜2026年11月29日',venue='上野恩賜公園 竹の台広場(噴水広場)',reservation=UNCONFIRMED,kind='イベント',unote='時間・料金・予約要否は未確認'),
R(SEASON,'テラスモール湘南 イルミネーション2026 Our Blue Xmas','神奈川県 藤沢市 辻堂','15周年のイルミネーション。高さ約8mのメインツリーと青い光、音楽に連動する演出','https://shonan.terracemall.com/event/detail/?cd=001259',False,period='2026年11月11日〜2026年12月25日',venue='テラスモール湘南',reservation='通常観覧の予約要否は未確認',kind='イベント',note='点灯17:00〜23:00。ページ上部の日付はオーナメント募集を含むため本文のイルミネーション会期を採用',unote='通常観覧の料金・予約要否は公式本文に記載なし。未確認'),
R(SEASON,'WHITE KITTE 2026 笑顔おどる、クリスマス','千代田区 丸の内','KITTE丸の内のクリスマスイベント。公式予告で会期・会場を確認','https://marunouchi.jp-kitte.jp/event/item_eventnews.jsp?id=825',True,period='2026年11月19日〜2026年12月25日',venue='KITTE丸の内 1Fアトリウム',reservation='詳細は後日発表。予約要否は未確認',kind='イベント',unote='公式予告では詳細は後日発表。時間・料金・予約要否は未確認'),
R('水族館・動物園','すみだ水族館 チンアナゴクリスマスツリー2026','墨田区 押上','1,111個のチンアナゴなどのぬいぐるみを飾った高さ約2mのツリーを展示','https://sumida-aquarium.com/news/20261030/',True,period='2026年11月7日〜2026年12月28日',venue='すみだ水族館 エントランス',reservation='水族館公式にチケット購入案内あり。ツリー単独の予約案内はなし',kind='イベント',unote='ツリー観覧の予約要否の個別記載はなく未確認'),
R(CHARA,'しながわ水族館 エリック・カール COLORFUL CHRISTMAS','品川区 勝島','特別展をクリスマス装飾へ更新。クマノミルーム、トンネル水槽、デンキウナギのツリーなど','https://www.aquarium.gr.jp/news/events/32975',True,period='2026年11月14日〜2026年12月25日',venue='しながわ水族館 地下1Fクマノミルームほか館内',reservation='水族館の入館券が必要。公式にWebチケット案内あり',kind='イベント',unote='特別展単独の予約要否は未確認'),
R(FILM,'コニカミノルタ イルミネーションウェルカムドーム2026','千代田区 有楽町 / 豊島区 池袋 / 墨田区 押上ほか','本編前の約10分間、星と光のクリスマス映像を上映。ウェルカム映像は撮影可能','https://planetarium.konicaminolta.jp/event/illumination/?hall=tenku',True,period='2026年11月12日〜2026年12月25日',venue='プラネタリアTOKYO・YOKOHAMA、満天(池袋)、天空',reservation='対象作品の鑑賞券を購入。ウェルカム映像のみの鑑賞は不可',kind='イベント',note='上映されない作品もあるため対象作品を公式で確認'),
R(MUSEUM,'ヨシロットン展 彼方との交信／BEYOND EARTH','港区 虎ノ門','高層ギャラリーを宇宙船に見立てたアート展。光・映像によるインスタレーション','https://www.tokyonode.jp/sp/yoshirotten/',True,period='2026年10月30日〜2027年1月11日',venue='虎ノ門ヒルズ ステーションタワー45F・49F TOKYO NODE',reservation='公式サイトのチケット案内から購入。現在の残席は未確認',kind='企画展',note='rain_okは屋内ギャラリー鑑賞の判断。屋上展示は天候等により休止あり'),
R(MUSEUM,'野口英世生誕150年記念企画展 感染症への挑戦：過去・現在・未来','台東区 上野','野口英世生誕150年を記念する感染症の企画展','https://www.kahaku.go.jp/tenji-event/nid00003997.html',True,period='2026年10月27日〜2027年2月28日',venue='国立科学博物館',reservation='常設展示入館料で観覧可。一般・大学生630円。企画展単独の予約要否は未確認',kind='企画展',note='日本館1階企画展示室。9:00〜17:00、入館16:30まで',unote='企画展の予約要否は個別記載がなく未確認'),
R(MUSEUM,'東京都美術館開館100周年記念 あなたが世界を読むために','台東区 上野','東京都美術館の開館100周年を記念する展覧会','https://www.tobikan.jp/exhibition/2026_waysofreading.html',True,period='2026年11月19日〜2027年1月11日',venue='東京都美術館',reservation='観覧無料。予約要否は公式本文に記載なし、未確認',kind='企画展',note='ギャラリーA・C。12/7・12/21〜1/3休室',unote='予約要否は未確認'),
R(MUSEUM,'芸術未来研究場展2026','台東区 上野','東京藝術大学の芸術未来研究場による展覧会','https://museum.geidai.ac.jp/exhibit/2026/11/gmk2026.html',True,period='2026年11月20日〜2026年12月2日',venue='東京藝術大学大学美術館',reservation='観覧無料。予約要否は公式本文に記載なし、未確認',kind='企画展',note='本館展示室3・4。10:00〜17:00、11/30休館',unote='予約要否は未確認'),
]
