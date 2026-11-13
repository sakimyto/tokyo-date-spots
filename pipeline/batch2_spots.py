# 第2弾(2026-10-24確認): 映画・謎解き・幅出し(新ジャンル含む)・最近の話題。
# 公式ページを開いて確認できた事実だけを書く。確認できなかったものは入れない。
# R(...)の rain= は「主な体験が屋内で完結し雨でも十分楽しめる」(True)か否か。判断は rain_manual.json に記録される(merge_batch2.py)。
def R(genre,name,area,desc,url,rain,period='',venue='',reservation='',kind='',note='',baby=False,status='ok',unote=''):
    return dict(genre=genre,name=name,area=area,desc=desc,url=url,rain_ok=rain,period=period,venue=venue,
                reservation=reservation,kind=kind,period_note=note,baby_ok=baby,url_status=status,url_note=unote)

FILM='映画館・プラネタリウム'; EXP='体験型'; STAGE='舞台・ミュージカル・ライブ'; MAKE='工場見学・ものづくり'; ANI='動物カフェ・ふれあい'
PLAY='遊び・スポーツ体験'; BOOK='書店・ブックカフェ'; NIGHT='ナイトライフ・バー'; HARV='収穫体験'
SPORT='スポーツ観戦・ライブ'; OUT='アウトドア'; SPA='プール・スパ・温泉'; TRIP='日帰り旅'; SHOP='買い物・街歩き'; CHARA='キャラクター・コラボイベント'

ROWS=[
# ---- 映画(新作・期間限定) 公式サイトで公開日を確認 ----
R(FILM,'映画『ゴジラ-0.0』','東京都 都内・関東の劇場','『ゴジラ-0.0』。11月3日(火・祝)公開(公式サイト表記)。上映館は公式サイトのTHEATERで確認','https://godzilla-minuszero.toho-movie.jp/',True,period='2026年11月3日公開',kind='イベント',note='公開日のみで終了日なし'),
R(FILM,'映画『ひつじのショーン かぼちゃ畑の怪物!』','東京都 都内・関東の劇場','2026年10月23日劇場公開(公式サイト表記)。家族向けアニメ','https://movies.shochiku.co.jp/shaun-kabocha/',True,period='2026年10月23日公開',kind='イベント',note='公開日のみで終了日なし'),
R(FILM,'劇場版 前橋ウィッチーズ ～魔女見習いのエモエモリーズ～','東京都 都内・関東の劇場','2026年10月23日(金)公開。応援上映の実施が公式ニュースで告知(日程は公式で確認)','https://www.maebashi-witches.com/',True,period='2026年10月23日公開',kind='イベント',note='公開日のみで終了日なし'),
R(FILM,'映画『負けへんで』','東京都 都内・関東の劇場','11.13 Fri ROADSHOW(公式サイト表記)。内野聖陽・松本若菜・北村一輝出演','https://gaga.ne.jp/makehende/',True,period='2026年11月13日公開',kind='イベント',note='公開日のみで終了日なし'),
R(FILM,'映画『装甲騎兵ボトムズ 灰色の魔女』','東京都 都内・関東の劇場','2026年11月20日劇場公開(公式サイト表記)','https://votoms-gh.com/',True,period='2026年11月20日公開',kind='イベント',note='公開日のみで終了日なし'),
R(FILM,'映画『魔法使いの夜』','東京都 都内・関東の劇場','11.20(fri)劇場公開(公式サイト表記)','https://mahoyo-movie.com/',True,period='2026年11月20日公開',kind='イベント',note='公開日のみで終了日なし'),
R(FILM,'映画『ワンダンス』','東京都 都内・関東の劇場','11.27 Fri 公開(公式サイト表記)。ムビチケ特典あり','https://happinet-phantom.com/wandance/',True,period='2026年11月27日公開',kind='イベント',note='公開日のみで終了日なし'),
R(FILM,'Vシネクスト『仮面ライダーカブト20th 天を継ぐもの』','新宿区 歌舞伎町','新宿バルト9ほかで期間限定上映(公式サイト表記)','https://www.toei-video.co.jp/vcinext-kabuto/',True,period='2026年11月6日より期間限定上映',kind='イベント',note='開始日のみ・終了日は公式で確認'),
R(FILM,'映画『デューン 砂の惑星 PART3』(IMAX/Dolby Cinema/4DX/MX4D)','東京都 都内・関東の劇場','2026年12月18日(金)日米同時公開。IMAX・Dolby Cinema・4DX・MX4Dでの上映が公式ニュースで告知','https://dune-movie-3.jp/',True,period='2026年12月18日公開',kind='イベント',note='公開日は公式サイト由来(検索要約で確認)・上映館は公式で確認'),
R(FILM,'第27回 東京フィルメックス 2026','千代田区 有楽町','アジアの新しい才能を紹介する映画祭。会場は有楽町朝日ホール/丸の内ピカデリー/ヒューマントラストシネマ有楽町','https://filmex.jp/2026/',True,period='2026年11月20日〜2026年11月29日',kind='イベント'),
R(FILM,'新宿武蔵野館','新宿区 新宿','新宿3丁目の映画館(ミニシアター系の上映)。上映作品・時間は公式で確認','https://qualite.musashino-k.jp/',True,kind='常設',venue='新宿区新宿3-27-10 武蔵野ビル3F'),
R(FILM,'キネカ大森','品川区 南大井','大森駅前の映画館(西友大森店内)。上映作品は公式で確認','https://ttcg.jp/cineka_omori/',True,kind='常設',venue='品川区南大井6-27-25 西友大森店 5F'),
R(FILM,'国立映画アーカイブ','中央区 京橋','国立の映画アーカイブ。上映プログラム(特集上映)を公式で公開','https://www.nfaj.go.jp/film-program/',True,kind='常設',venue='中央区京橋3-7-6'),
# ---- 謎解き・脱出ゲーム ----
R(EXP,'リアル脱出ゲーム渋谷店(SCRAP)','渋谷区 渋谷','SCRAPの常設店。『きさらぎ駅からの脱出』ほか屋内の脱出ゲームを随時開催(60〜90分・一般前売3,000円〜の作品あり)','https://realdgame.jp/shop/shibuya/',True,kind='常設',reservation='日時指定の予約制(公式で確認)'),
R(EXP,'ダークエスケープ 新宿歌舞伎町店','新宿区 歌舞伎町','ホラー・暗い演出の脱出ゲーム(公式の店舗一覧は新宿歌舞伎町・横浜中華街・東銀座)。屋内','https://www.darkescape.jp/services/',True,kind='常設',venue='新宿区歌舞伎町2-46-8',reservation='テーマ予約制(公式で確認)'),
R(EXP,'魔王の日曜日 新宿三丁目店(イマーシブ脱出ゲーム)','新宿区 新宿','ゴシックな世界観の没入型謎解き・脱出ゲーム(店舗一覧に新宿三丁目店あり)','https://imgame.jp/stores/',True,kind='常設',reservation='予約制(公式で確認)'),
R(EXP,'謎解きカフェ はてな珈琲店 東京銀座店','中央区 銀座','カフェで謎解きに挑戦(東京は銀座・新宿・池袋に店舗)。公式に料金システムと予約ページあり','https://hatenacoffee.experiful.jp/',True,kind='常設',venue='中央区銀座1-14-14'),
R(EXP,'NoEscape リアル体験脱出ゲーム(新宿・池袋)','豊島区 池袋','池袋・新宿に店舗がある脱出ゲーム専門店(50分の脱出ゲームなど)','https://noescape.co.jp/',True,kind='常設',venue='新宿店・池袋店(詳細は公式)'),
R(EXP,'ナゾトキ街歩きゲーム『東京謎解きトラベル』(都営地下鉄沿線)','東京都 都営地下鉄沿線','都営地下鉄沿線を巡る街歩き謎解き。累計動員2万人突破で2026年11月30日(月)まで期間延長。所要5〜6時間・キット2,500円','https://www.scrapmagazine.com/news/toeinazo260911/',False,period='2026年11月30日まで',kind='イベント',reservation='謎解きキット購入(2,500円)',note='終了が近い(11/30まで)'),
# ---- 舞台・演劇・演芸(新ジャンル) ----
R(STAGE,'ミュージカル『ラ・カージュ・オ・フォール』(日生劇場)','千代田区 有楽町','初のWキャスト(鹿賀丈史/佐藤隆紀、市村正親/石丸幹二ほか)の再演。2026年12月9日〜29日、会場は日生劇場','https://horipro-stage.jp/special/lacage20260317/',True,period='2026年12月9日〜2026年12月29日',kind='イベント',venue='日生劇場',reservation='チケットは今秋一般発売予定(公式の告知)',note='一般発売日は公式で確認'),
R(STAGE,'日生劇場','千代田区 有楽町','日比谷の劇場。公演ラインナップは公式で確認','https://www.nissaytheatre.or.jp/',True,kind='常設'),
R(STAGE,'明治座','中央区 日本橋浜町','劇場。公演ラインナップは公式で確認','https://www.meijiza.co.jp/',True,kind='常設'),
R(STAGE,'新国立劇場','渋谷区 本町','オペラ・バレエ・演劇の劇場。公演は公式で確認','https://www.nntt.jac.go.jp/',True,kind='常設'),
R(STAGE,'東京オペラシティ コンサートホール','新宿区 西新宿','コンサートホール。公演カレンダーは公式で確認','https://www.operacity.jp/',True,kind='常設',venue='新宿区西新宿3-20-2'),
R(STAGE,'すみだトリフォニーホール','墨田区 錦糸','コンサートホール。公演は公式で確認','https://www.triphony.com/',True,kind='常設',venue='墨田区錦糸1-2-3'),
R(STAGE,'ミューザ川崎シンフォニーホール','神奈川県 川崎市','コンサートホール(川崎駅前)。公演は公式で確認','https://www.kawasaki-sym-hall.jp/',True,kind='常設',venue='川崎市幸区大宮町1310'),
R(STAGE,'NHKホール','渋谷区 神南','ホール。公演・番組観覧は公式で確認','https://www.nhk.or.jp/nhkhall/',True,kind='常設'),
# ---- スポーツ観戦・ライブ(追加) ----
R(SPORT,'LIQUIDROOM','渋谷区 東','ライブハウス。公演スケジュールは公式で確認','https://www.liquidroom.net/',True,kind='常設'),
R(SPORT,'アルバルク東京(Bリーグ)','東京都','Bリーグのバスケットボールクラブ。試合日程は公式で確認','https://www.alvark-tokyo.jp/',True,kind='常設',note='会場・日程は公式で確認'),
R(SPORT,'川崎ブレイブサンダース(Bリーグ)','神奈川県 川崎市','Bリーグのバスケットボールクラブ。試合日程は公式で確認','https://www.kawasaki-bravethunders.com/',True,kind='常設'),
R(SPORT,'横浜ビー・コルセアーズ(Bリーグ)','神奈川県 横浜市','Bリーグのバスケットボールクラブ。試合日程は公式で確認','https://b-corsairs.com/',True,kind='常設'),
R(SPORT,'千葉ジェッツ(Bリーグ)','千葉県','Bリーグのバスケットボールクラブ。試合日程は公式で確認','https://chibajets.jp/',True,kind='常設'),
R(SPORT,'FC東京(Jリーグ)','東京都','Jリーグのサッカークラブ。試合日程は公式で確認','https://www.fctokyo.co.jp/',False,kind='常設'),
R(SPORT,'川崎フロンターレ(Jリーグ)','神奈川県 川崎市','Jリーグのサッカークラブ。試合日程は公式で確認','https://www.frontale.co.jp/',False,kind='常設'),
R(SPORT,'横浜F・マリノス(Jリーグ)','神奈川県 横浜市','Jリーグのサッカークラブ。試合日程は公式で確認','https://www.f-marinos.com/',False,kind='常設'),
R(SPORT,'FC町田ゼルビア(Jリーグ)','町田市','Jリーグのサッカークラブ。試合日程は公式で確認','https://www.zelvia.co.jp/',False,kind='常設'),
R(SPORT,'浦和レッズ(Jリーグ)','埼玉県 さいたま市','Jリーグのサッカークラブ。試合日程は公式で確認','https://www.urawa-reds.co.jp/',False,kind='常設'),
R(SPORT,'柏レイソル(Jリーグ)','千葉県 柏市','Jリーグのサッカークラブ。試合日程は公式で確認','https://www.reysol.co.jp/',False,kind='常設'),
R(SPORT,'湘南ベルマーレ(Jリーグ)','神奈川県 平塚市','Jリーグのサッカークラブ。試合日程は公式で確認','https://www.bellmare.co.jp/',False,kind='常設'),
# ---- 遊び・スポーツ体験(新ジャンル) ----
R(PLAY,'シブヤボウリング(EST 渋谷東口会館)','渋谷区 渋谷','渋谷東口のボウリング場。同施設にビリヤードもあり','https://www.shibuyaest.co.jp/bowling/',True,kind='常設'),
R(PLAY,'東京ドームシティ アクティブパスポート(ボウリングほか)','文京区 後楽','東京ドームシティのスポーツ施設のパスポート(ボウリングを含む)。内容・料金は公式で確認','https://www.tokyo-dome.co.jp/passport/active',False,kind='常設',unote=''),
R(PLAY,'東京ドーム ローラースケートアリーナ','文京区 後楽','ローラースケートが楽しめる施設(東京ドームシティ内)。営業日は公式で確認','https://www.tokyo-dome.co.jp/roller/',False,kind='常設'),
R(PLAY,'田中貴金属アイスアリーナ','江東区 辰巳','都内最大級のアイスリンク(公式表記)','https://ia-tatsumi.tokyo/',False,kind='常設',venue='江東区辰巳2-8-10',note='屋内か公式で確認できず(☔は付けていない)'),
R(PLAY,'明治神宮外苑アイススケート場','新宿区 霞ヶ丘町','明治神宮外苑のアイススケート場。営業日は公式で確認','https://meijijingugaien-iceskating.com/',False,kind='常設',venue='新宿区霞ヶ丘町11-1',note='屋内・屋外の別を公式で確認できず(☔は付けていない)'),
R(PLAY,'Fish and Bird(クライミング)','江東区 東陽','クライミングジム','https://www.fish-bird.co.jp/fishandbird/',True,kind='常設',venue='江東区東陽7-4-12'),
R(PLAY,'GiGO秋葉原3号館(ゲームセンター)','千代田区 外神田','秋葉原のゲームセンター(ゲームコーナー案内あり)','https://www.gigo.co.jp/shops/akihabara3/games',True,kind='常設'),
R(PLAY,'ボードゲームカフェ JELLY JELLY CAFE 渋谷','渋谷区 宇田川町','ボードゲームカフェ(渋谷本店)','https://jellyjellycafe.com/shibuya',True,kind='常設',venue='渋谷区宇田川町10-2'),
R(PLAY,'ボードゲームカフェ サイコロブクロ 新宿','新宿区 新宿','新宿のボードゲームカフェ','https://saikorobukuro.com/shinjuku/',True,kind='常設',venue='新宿区新宿5-10-6'),
R(PLAY,'ボードゲームと珈琲豆 新宿店','新宿区 西新宿','ボードゲームカフェ(新宿店)','https://boardgames-coffeebeans.com/',True,kind='常設',venue='新宿区西新宿7-13-5'),
R(PLAY,'ボドゲ東京 新宿店','新宿区 新宿','新宿駅近くのボードゲームカフェ','https://bodoge-tokyo.com/shinjuku',True,kind='常設'),
# ---- ものづくり体験(新ジャンル) ----
R(MAKE,'創吉 切子体験教室(浅草)','台東区 雷門','江戸切子の体験教室','https://www.sokichi-workshop.com/',True,kind='常設',venue='台東区雷門2-1-14'),
R(MAKE,'すみだ江戸切子館 江戸切子体験','墨田区 太平','江戸切子の体験(工房併設)','https://www.edokiriko.net/taiken',True,kind='常設',venue='墨田区太平2-10-9'),
R(MAKE,'アトリエ ガラス工房ZO','墨田区','吹きガラス等の体験教室','https://www.glasszo.com/',True,kind='常設'),
R(MAKE,'東京ガラス工芸研究所 体験教室','大田区 東六郷','吹きガラスの体験教室','https://www.tokyo-glass.jp/experience/',True,kind='常設',venue='大田区東六郷1-26-13'),
R(MAKE,'うづまこ陶芸 1日陶芸体験','港区 芝','1日陶芸体験プラン','https://www.uzumakotougei.com/taiken.html',True,kind='常設',venue='港区芝3-29-11'),
R(MAKE,'陶芸教室Futaba 体験(カップル割あり)','板橋区 中台','陶芸体験。カップル向け割引の案内あり','https://www.fu-ta-ba.jp/trial/date-2/',True,kind='常設',venue='板橋区中台1-29-8 1F'),
R(MAKE,'ふれぐらんす工房「香」(浅草フレグランス作り)','台東区 花川戸','浅草でフレグランスを作る体験','https://fragrance-koubou-kaori.com/',True,kind='常設',venue='台東区花川戸2-7-2'),
R(MAKE,'リングづくり体験 Grace(浅草)','台東区 浅草','ワークショップでリングを作る体験','https://www.grace-ring.com/workshop',True,kind='常設',venue='台東区浅草2-2-2 弐番館'),
R(MAKE,'お菓子教室 スイートリボン(銀座)','中央区 銀座','お菓子づくり教室','https://michiyokumabe.com/',True,kind='常設'),
# ---- 動物カフェ・ふれあい(新ジャンル) ----
R(ANI,'HARRY ハリネズミカフェ 原宿','渋谷区 神宮前','ハリネズミとふれあえるカフェ','https://harinezumi-cafe.com/',True,kind='常設',venue='渋谷区神宮前1-13-21'),
R(ANI,'HARRY ASAKUSA(ハリネズミカフェ 浅草)','台東区 浅草','ハリネズミとふれあえるカフェ(浅草店)','https://harinezumi-cafe.com/store/asakusa/',True,kind='常設',venue='台東区浅草1-1-17 増田ビル5F'),
R(ANI,'もふもふ体験型パーク 浅草 カワウソ・ミーアキャット','台東区 浅草','カワウソ(餌やり付)などとふれあえる屋内施設(公式ページ表記)','https://www.moff-kalahari.com/',True,kind='常設'),
R(ANI,'うさぎcafe もふれる','千代田区 外神田','うさぎとふれあえるカフェ','https://moff-rell.com/ja/yoyaku',True,kind='常設',venue='千代田区外神田5-2-3 アソルティ末広町ビルB1F'),
R(ANI,'ふくろうカフェ 武蔵野カフェ・オウルビレッジ(原宿)','渋谷区 神宮前','ふくろうカフェ','https://www.owlvillage.jp/',True,kind='常設',venue='渋谷区神宮前1-21-15'),
# ---- 書店・ブックカフェ(新ジャンル) ----
R(BOOK,'代官山 蔦屋書店(代官山T-SITE)','渋谷区 猿楽町','蔦屋書店を中核にした代官山T-SITE','https://store.tsite.jp/daikanyama/',True,kind='常設'),
R(BOOK,'銀座 蔦屋書店','中央区 銀座','アートのある書店(GINZA SIX内)','https://store.tsite.jp/ginza/',True,kind='常設'),
R(BOOK,'青山ブックセンター 本店','渋谷区 神宮前','書店','https://www.aoyamabc.jp/',True,kind='常設',venue='渋谷区神宮前5-53-67'),
R(BOOK,'本屋 B&B(下北沢)','世田谷区 北沢','ビールが飲める本屋(下北沢)','https://bookandbeer.com/',True,kind='常設'),
R(BOOK,'国立国会図書館 国際子ども図書館','台東区 上野公園','子どもの本の図書館(上野公園内)','https://www.kodomo.go.jp/',True,kind='常設'),
# ---- ナイトライフ・バー(新ジャンル) ----
R(NIGHT,'TOMIJAZ(麻布十番のジャズバー)','港区 麻布十番','隠れ家的なジャズバー(公式表記)','https://www.tomijaz.jp/',True,kind='常設'),
R(NIGHT,'ライブバー 東京倶楽部','千代田区 神田駿河台','ライブバー(水道橋・御茶ノ水エリア)','https://tokyo-club.com/',True,kind='常設',venue='千代田区神田駿河台2-11-16'),
R(NIGHT,'新宿ゴールデン街','新宿区 歌舞伎町','小さなバーが並ぶ飲み歩きエリア(新宿三光商店街振興組合)','https://goldengai.jp/',True,kind='常設',venue='新宿区歌舞伎町1-1-6'),
R(NIGHT,'WOMB(渋谷クラブ)','渋谷区 円山町','渋谷のクラブ。イベントは公式で確認','https://www.womb.co.jp/',True,kind='常設'),
# ---- 収穫体験(新ジャンル) ----
R(HARV,'町田いちご園 MachidaStrawberryFarm','町田市 相原町','電車で行けるいちご狩り。開園は毎年12月下旬〜5月中旬・完全予約制(公式表記)','https://www.strawberry.tokyo/',False,kind='常設',venue='町田市相原町1279',reservation='完全予約制(24時間ネット予約)',note='いちご狩りは12月下旬開園'),
R(HARV,'ICHIGO HOUSE.みたか','三鷹市 牟礼','三鷹のいちご農園。開園情報は公式で確認','https://mitaka.ichigohouse-wegro.com/',False,kind='常設',venue='三鷹市牟礼1-8'),
R(HARV,'三岳園(みかん狩り)','神奈川県 伊勢原市','早生みかんから楽しめるみかん狩り(公式表記)','https://www.mitake-en.jp/mikan',False,kind='常設',venue='伊勢原市善波468'),
R(HARV,'小田原 みかん狩り(オレンジガーデン)','神奈川県 小田原市','みかん狩り。シーズンの案内あり(10月10日〜の記載)','https://www.orange-garden.net/',False,kind='常設'),
# ---- アウトドア(BBQ/グランピング) ----
R(OUT,'東京スカイツリータウン グランピング&BBQ','墨田区 押上','手ぶらで楽しめるBBQ(スカイツリータウン内・公式サイト)','https://www.skytreetown-glamping-bbq.com/',False,kind='常設'),
R(OUT,'インドアグランピング OUCHI CAMP(浅草・入谷)','台東区 千束','台東区千束のインドアグランピング','https://ouchicamp.com/',True,kind='常設',venue='台東区千束2-30-5'),
R(OUT,'池袋 東武百貨店 手ぶらBBQ','豊島区 西池袋','東武百貨店池袋店の手ぶらBBQ','https://ikebukuro-rakuen-bbq.com/',False,kind='常設',note='屋内外の別を公式で確認できず(☔は付けていない)'),
R(OUT,'渋谷 冷暖房完備BBQ(雨天OK)','渋谷区 道玄坂','冷暖房完備・雨天OKをうたう屋内BBQ(公式ページ表記)','https://www.shibuyagardenspace.com/tonai-bbq-reidanbou/',True,kind='常設',venue='渋谷区道玄坂2-9-10 松本ビル7F'),
# ---- サウナ(プール・スパ・温泉) ----
R(SPA,'Galera Sauna Tachikawa','立川市 曙町','立川のサウナ','https://galera-sauna.tokyo/sauna/',True,kind='常設',venue='立川市曙町2-14-26'),
R(SPA,'Sauna-Tokyo(サウナ東京)赤坂','港区 赤坂','赤坂のサウナ','https://sauna-tokyo.jp/',True,kind='常設',venue='港区赤坂3-13-4'),
# ---- クルーズ・乗り物体験(体験型) ----
R(EXP,'屋形船 晴海屋 乗合屋形船','江東区 東砂','乗合の屋形船(両国発着の案内あり)','https://www.harumiya.co.jp/yakatafune/passenger/',False,kind='常設',venue='受付 江東区東砂6-16-9',note='屋形船は屋根付きだが屋外景観が主体のため☔は付けていない'),
R(EXP,'水上バス・東京湾クルーズ(東京水辺ライン)','東京都 隅田川・東京湾','水上バス・東京湾クルーズ','https://www.suijobus.co.jp/',False,kind='常設'),
R(EXP,'東京湾クルージングレストラン シンフォニー','港区 海岸','東京湾クルージングのレストラン船','https://www.symphony-cruise.co.jp/',True,kind='常設',venue='港区海岸2-7-104',note='屋内ダイニング主体(公式の詳細は要確認)'),
R(EXP,'SEA SHANKS 東京貸切クルーズ','東京都 東京湾','東京の貸切クルーズ','https://www.tokyo-cruising.com/',False,kind='常設'),
R(EXP,'横浜 ロイヤルウイング(クルーズ船)','神奈川県 横浜市','横浜のクルーズ船','https://www.royalwing.co.jp/',True,kind='常設'),
R(EXP,'ヘリコプター・プライベートフライト(ARIAIR東京)','東京都 東京ヘリポート','ヘリコプターで東京上空を遊覧するプラン','https://ariair.arila.co.jp/special/ariair_tokyo_helicopter/',False,kind='常設'),
R(EXP,'人力車のえびす屋(浅草)','台東区 浅草','人力車で観光する体験','https://www.ebisuya.com/',False,kind='常設'),
# ---- 日帰り温泉・日帰りプラン ----
R(TRIP,'箱根湯本 吉池旅館 日帰りプラン','神奈川県 箱根町','日帰り・0泊プランで温泉に入れる(公式)','https://www.yoshiike.org/day_trip/',True,kind='常設',venue='箱根町湯本597'),
R(TRIP,'箱根湯本 かもん 日帰り温泉と食事プラン','神奈川県 箱根町','日帰り温泉と昼食・夕食のプラン(公式)','https://www.hakone-kamon.jp/dayplan/',True,kind='常設',venue='箱根町湯本435'),
R(TRIP,'箱根湯本 ゆの里 日帰りプラン','神奈川県 箱根町','日帰りプラン(公式)','https://www.yunosato-y.jp/plan.html',True,kind='常設',venue='箱根町湯本茶屋191'),
R(TRIP,'富士屋ホテル 日帰りプラン(宮ノ下)','神奈川県 箱根町','日帰りで富士屋ホテルを楽しむプラン(公式ページ)','https://www.fujiyahotel.jp/recommend/recommend22.html',True,kind='常設'),
# ---- 最近の話題・新規(元ジャンル側。話題への複製は TREND で指定) ----
R(CHARA,'東京ディズニーランド「ディズニー・クリスマス」','千葉県 浦安市','パレード「トイズ・ワンダラス・クリスマス!」、エレクトリカルパレード・ドリームライツ(クリスマス版)、花火「スターブライト・クリスマス」、エントランスのデコレーション初登場。ジョリーフード・プラザが初登場','https://www.tokyodisneyresort.jp/treasure/christmas2026/tdl/',False,period='2026年11月11日〜2026年12月25日',reservation='パークチケット(日付指定)が必要。ディズニー・プレミアアクセス(有料)あり',kind='イベント'),
R(CHARA,'Grandberry Christmas「Together this Holiday」(スヌーピーときょうだい)','町田市 鶴間','スヌーピーときょうだいたちのクリスマス装飾をパーク全体で展開。足跡ステッカー、キャラクターパネル。アイススケートリンク「SNOOPY ICE ARENA」は12月5日〜2027年2月28日','https://www.tokyu-tmd.co.jp/news/grandberry-park-20261022/',False,period='2026年11月14日〜2026年12月25日',venue='グランベリーパーク(田園都市線 南町田グランベリーパーク駅直結)',kind='イベント',note='SNOOPY ICE ARENAは2026年12月5日〜2027年2月28日'),
R(CHARA,'ミッフィーほかほかダイニング(東京ソラマチ)','墨田区 押上','ミッフィーのお顔のグラタンパイやほかほかシチュー・スープの冬限定ダイニング。BOX cafe&space 東京ソラマチ店','https://hokahoka-dining.ltr-online.com',True,period='2026年10月31日〜2027年1月24日',venue='BOX cafe&space 東京ソラマチ店',reservation='事前予約 2026年10月23日18:00〜(予約してメニュー注文でマルチケースをプレゼント)',kind='イベント',note='事前予約が10/23 18:00から開始済み'),
R(CHARA,'アクアシティお台場×リラックマ「クリスマスパーティー」','港区 台場','アクアシティお台場がリラックマ一色に。展示・スタンプラリー(3階アクアアリーナほか)、コラボカフェ(11/25〜12/25・5階R.O.STAR Seaside Terrace)','https://www.aquacity.jp/news/detail.php?id=63939',True,period='2026年11月13日〜2026年12月25日',venue='アクアシティお台場',kind='イベント',note='期間はサンエックス公式リリースの記載'),
R(CHARA,'スヌーピータウンミニ東京駅一番街店 クリスマスフェア2026','千代田区 丸の内','東京駅一番街 地下1階 東京キャラクターストリート内。11/7発売「SWEET CANDY CHRISTMAS with Siblings」。税込5,500円以上でマグカップかミニボウル、11,000円以上で両方プレゼント(先着各6,000名)','https://www.tokyoeki-1bangai.co.jp/event/detail/?cd=001267',True,period='2026年11月7日〜2026年12月25日',venue='東京駅一番街 地下1階 東京キャラクターストリート 10:00〜20:30',kind='イベント',note='特典は先着・なくなり次第終了'),
R(CHARA,'サクラ大戦30周年記念展 ～夢はよみがえる～(東京会場)','千代田区 有楽町','サクラ大戦30周年記念展。東京会場は有楽町マルイ8F SPACE1(当日券販売場所)。2,000円(前売・税込)、当日券2,400円','https://sakura-30th-exhibition.com/ticket/',True,period='2026年10月31日〜2026年11月15日',venue='有楽町マルイ 8F イベントスペース SPACE1',reservation='日時指定券10/31・11/1、指定期間中有効券11/2〜11/15。前売はイープラスで10/30 23:59まで、以降は当日券',kind='企画展',note='前売は10/30 23:59まで'),
R(CHARA,'ギルティクラウン×甲鉄城のカバネリ展(東京会場)','中央区 銀座','ギルティクラウン×甲鉄城のカバネリ展。全日日時指定制、11:00〜20:00(最終日17:00閉場・日曜19:30閉場)','https://www.gc-kabaneri-ten.com/',True,period='2026年10月30日〜2026年11月23日',venue='ギンザミライミュージアム',reservation='全日日時指定制',kind='企画展'),
# 新施設
R(SHOP,'PLAZA TOKYO+(新宿マルイ 本館B1F)','新宿区 新宿','60周年のPLAZAが新宿マルイ本館B1Fにオープン。食品・菓子、文具、玩具、キャラクター雑貨、化粧品、衣料品、常設POPUP、カフェなど。11:00〜21:00','https://prtimes.jp/main/html/rd/p/000004216.000003860.html',True,period='2026年11月20日オープン',venue='新宿マルイ 本館B1F',kind='イベント',note='オープン日のみ'),
R(SHOP,'アトレ中野','中野区 中野','アトレ中野 NEW OPEN(公式ページ表記)','https://www.atre.co.jp/campaign/newopen/nakano/',True,period='2026年12月9日オープン',kind='イベント',note='オープン日のみ'),
R(SHOP,'秋葉原UDX 商業ゾーン リニューアル','千代田区 外神田','「秋葉原UDX」商業ゾーン 12/10 リニューアル(NTT都市開発の公式ニュース)','https://www.nttud.co.jp/news/detail/id/n28040.html',True,period='2026年12月10日リニューアル',kind='イベント',note='リニューアル日のみ'),
R(SHOP,'明治安田新宿ビル 商業エリア','新宿区 西新宿','新宿駅直結の1階・地下1階に全21店舗(キル フェボン、Shake Shack、スターバックスなど)が開業(明治安田の公式リリース)','https://www.meijiyasuda.co.jp/profile/news/release/2026/pdf/20261022_02.pdf',True,period='2026年11月28日開業',venue='明治安田新宿ビル 1F・B1F',kind='イベント',note='開業日のみ',unote='公式リリースはPDF。店舗リストは検索要約で確認'),
]

# 既存/新規の行を「話題」ジャンルに複製して trending=True にする(名前→追加の注意書き)。元の行は trending=False のまま。
TREND={
 'ちいかわクリスマスマーケット':'⚠先行抽選の申込は2026/10/25(日)23:59まで(当落発表10/30)。日時指定チケット制',
 'ちいかわパーク クリスマス':'',
 'Puroland Illumination Christmas(くまのがっこうコラボ)':'',
 'ふわふわんだーシナモロールパーク':'先行抽選(9/17〜9/27)は終了。一般販売は公式で確認',
 'スヌーピーミュージアム 企画展「きょうだいって、いいな」':'',
 '東京ディズニーシー「ディズニー・クリスマス」':'',
 '東京ディズニーランド「ディズニー・クリスマス」':'',
 'MARUNOUCHI BRIGHT HOLIDAY「ハリー・ポッター」丸の内を彩る魔法の雪':'',
 '東京クリスマスアドベント(上野恩賜公園)':'',
 '東京スカイツリータウン ドリームクリスマス2026':'',
 'ムーミン谷のクリスマス 2026':'',
 'Grandberry Christmas「Together this Holiday」(スヌーピーときょうだい)':'',
 'ミッフィーほかほかダイニング(東京ソラマチ)':'事前予約は10/23 18:00から開始済み',
 'アクアシティお台場×リラックマ「クリスマスパーティー」':'',
 'スヌーピータウンミニ東京駅一番街店 クリスマスフェア2026':'',
 'THE WORLD OF BIOHAZARD 30周年展':'',
 '芥見下々『呪術廻戦』完結展':'',
 'ティム・バートンのラビリンス 東京':'',
 'サクラ大戦30周年記念展 ～夢はよみがえる～(東京会場)':'⚠前売(イープラス)は2026/10/30 23:59まで',
 'ギルティクラウン×甲鉄城のカバネリ展(東京会場)':'',
 'テート美術館 ターナー展':'',
 '少女漫画・インフィニティ 萩尾望都×山岸凉子×大和和紀':'',
 'PLAZA TOKYO+(新宿マルイ 本館B1F)':'',
 'アトレ中野':'',
 '秋葉原UDX 商業ゾーン リニューアル':'',
 '明治安田新宿ビル 商業エリア':'',
}

# ==== 2026-10-30 週次更新(公式ページを開いて確認した事実のみ) ====
SEA='季節イベント'; BABY='赤ちゃん・親子'
ROWS+=[
# ---- キャラクター・コラボ・大型イベント ----
R(CHARA,'東京コミコン2026(幕張メッセ)','千葉県 千葉市美浜区','映画・ドラマ・コミック・ゲームのポップカルチャーの祭典。海外スターの来日企画などは公式で発表。12/11 11:00〜19:00、12/12 10:00〜19:00、12/13 10:00〜18:00(公式の開催概要)','https://tokyocomiccon.jp/whatscc',True,period='2026年12月11日〜2026年12月13日',venue='幕張メッセ 国際展示場 1〜6ホール',reservation='入場チケット制(券種・料金は公式で要確認)',kind='イベント'),
R(CHARA,'ジャンプフェスタ2027(幕張メッセ)','千葉県 千葉市美浜区','マンガ・アニメ・ゲーム・ホビーの「ジャンプ」の祭典。フォトスポット、謎解きラリー、ジャンプキャラクターパレードなど。9:00〜17:00(最終入場16:30)','https://www.jumpfesta.com/',True,period='2026年12月19日〜2026年12月20日',venue='幕張メッセ 国際展示場 展示ホール1〜9・11',reservation='入場方法・応募期間は公式の「入場チケット応募」ページで要確認',kind='イベント'),
R(CHARA,'ゴジラ博 マイナスの世界(大丸東京店)','千代田区 丸の内','ゴジラと特撮の展示イベント。10:00〜19:30(最終日は17:30まで)。一般・大学生1,500円(前売1,300円)、中高生1,000円、小学生700円','https://dmdepart.jp/museum/tokyo/godzilla-tokusatsu2026/',True,period='2026年11月6日〜2026年11月17日',venue='大丸東京店 11F 催事場',reservation='日時によって入場制限あり。小学生以下は保護者同伴(公式表記)',kind='イベント'),
R(CHARA,'ZO&FRIENDS CAFE HOME&DREAM(渋谷PARCO)','渋谷区 宇田川町','渋谷PARCO 6F「THE GUEST CAFE BY PARCO」のコラボカフェ(公式の開催日程)','https://cafe.parco.jp/',True,period='2026年11月7日〜2026年12月15日',venue='渋谷PARCO 6F THE GUEST CAFE BY PARCO',reservation='予約方法は公式の各カフェページで確認',kind='イベント'),

R(CHARA,'祝3000しゅ～ねん!?超たまごっち祭 in シブハラ','渋谷区 神宮前','たまごっち30周年企画。メイン会場の東急プラザ原宿「ハラカド」4F MAZEで特別展示「3000しゅ～ねん!?大発掘プロジェクト展」、出張ショップ、カフェなど。11:00〜20:00(最終入場19:30)','https://www.tamagotchi-factory.jp/news/19',True,period='2026年11月7日〜2026年12月6日',venue='東急プラザ原宿「ハラカド」4F MAZE',reservation='11/7(土)・8(日)は展示・ショップ・カフェの利用に事前抽選の入場整理券が必要',kind='イベント'),
# ---- 季節イベント ----
R(SEA,'新宿の酉の市(花園神社・十二社熊野神社・成子天神社)','新宿区 新宿','一の酉11/7(土)・二の酉11/19(木)。花園神社は各前日に前夜祭(新宿観光振興協会の案内)','https://www.kanko-shinjuku.jp/event/history/article_6631.html',False,period='2026年11月7日・19日',venue='花園神社ほか',kind='イベント',note='花園神社は11/6・11/18が前夜祭'),
R(SEA,'浅草 鷲神社 酉の市(令和8年)','台東区 千束','一の酉11/7(土)・二の酉11/19(木)、各日0:00〜24:00(公式)。熊手の露店が並ぶ','https://otorisama.or.jp/kotoshi.html',False,period='2026年11月7日・19日',venue='鷲神社(台東区千束3-18-7)',reservation='一部の祈祷などは事前予約(公式で確認)',kind='イベント'),
R(SEA,'2026東京スクエアガーデン ウィンターイルミネーション','中央区 京橋','HERALBONYとのコラボツリー(12/25まで)。11/5 17:45から点灯式とコンサート。再生可能エネルギー100%で点灯(公式ニュース)','https://tokyo-sg.com/news/3963',False,period='2026年11月5日〜2027年1月31日',venue='東京スクエアガーデン',kind='イベント'),
R(SEA,'BALLPARK Xmas YOKOHAMA KANNAI 2026','神奈川県 横浜市中区','横浜公園を会場にしたクリスマスイベント。入場無料。BASEGATE横浜関内・日本大通りと連動。コンテンツ詳細は11月上旬に公開予定(公式)','https://ballparkxmas.com/2026/',False,period='2026年11月20日〜2026年12月25日',venue='横浜公園',kind='イベント'),
R(SEA,'第十八回 たかはたもみじ灯路','日野市 高幡','高幡不動尊の参道と高幡不動駅周辺を約3,000灯の灯籠で照らす。五重塔の萬燈会も。17:00〜20:00(日野市観光協会)','https://shinsenhino.com/%e3%83%8b%e3%83%a5%e3%83%bc%e3%82%b9/%e3%80%8c%e7%ac%ac%e5%8d%81%e5%85%ab%e5%9b%9e%e3%81%9f%e3%81%8b%e3%81%af%e3%81%9f%e3%82%82%e3%81%bf%e3%81%98%e7%81%af%e8%b7%af%e3%80%8d%e9%96%8b%e5%82%ac.php',False,period='2026年11月22日〜2026年11月23日',venue='高幡不動尊参道・高幡不動駅周辺',kind='イベント',note='荒天時は中止の場合あり'),
# ---- 赤ちゃん・親子 ----
{**R(BABY,'ムジカべべ 0才からの音楽会 クリスマスコンサート','西東京市・小平市・小金井市','0歳から入れるクリスマスコンサート(約45分)。12/5(土)保谷こもれびホール小ホール 10:40、12/21(月)ルネこだいら、12/24(木)小金井宮地楽器ホール。授乳室・おむつ替え・ベビーカー置き場あり(公式)','https://zerosai-ongakukai.com/concert/12371/',True,period='2026年12月5日〜2026年12月24日',venue='保谷こもれびホールほか',reservation='1人1,000円(0歳から料金が必要)。予約は11/7 9:00から',kind='イベント',baby=True,note='開催日は12/5・12/21・12/24の3日'),'age':'0歳から'},
{**R(BABY,'そらとぶペンギン 5周年記念クリスマス絵本コンサートvol.4','世田谷区 成城','0歳〜高校生と家族向けの絵本コンサート。開場10:15/開演10:45/終演11:30、定員260名(公式)','https://sorapen.jp/20261212-2/',True,period='2026年12月12日(土) 1日のみ',venue='成城ホール(世田谷区成城6-2-1)',reservation='大人1,800円、4歳〜高校生500円、3歳以下無料',kind='イベント',baby=True),'age':'0歳から'},
# ---- 映画 ----
R(FILM,'映画『劇場版 薬屋のひとりごと 亡妃の秘宝』','東京都 都内・関東の劇場','劇場版「薬屋のひとりごと」。2026年12月11日(金)公開(公式ニュース)','https://kusuriyanohitorigoto.jp/news/2520/',True,period='2026年12月11日公開',kind='イベント'),
R(FILM,'映画『人生を変えたコント』','東京都 都内・関東の劇場','霜降り明星・せいやの小説が原作のお笑い青春映画。12.18公開(公式サイト表記)','https://gaga.ne.jp/jinsei_conte/',True,period='2026年12月18日公開',kind='イベント'),
R(FILM,'映画『楽園追放 心のレゾナンス』','東京都 都内・関東の劇場','水島精二×虚淵玄の『楽園追放』続編。2026年11月13日公開(公式サイト表記)','https://rakuen-tsuiho-r.com/',True,period='2026年11月13日公開',kind='イベント'),
R(FILM,'映画『タコピーの原罪 -ありがとう、また明日-』','東京都 都内・関東の劇場','アニメ「タコピーの原罪」の劇場総集編。11月27日(金)公開(公式サイト表記)','https://www.tbs.co.jp/anime/takopi_project/',True,period='2026年11月27日公開',kind='イベント'),
R(FILM,'映画『君の話』','東京都 都内・関東の劇場','三秋縋の小説の実写化。脚本・吉田恵里香。11月27日(金)公開(公式サイト表記)','https://movies.shochiku.co.jp/kimino-hanashi/',True,period='2026年11月27日公開',kind='イベント'),
R(FILM,'映画『SUKIYAKI 上を向いて歩こう』','東京都 都内・関東の劇場','「上を向いて歩こう」誕生の物語。岡田准一・松坂桃李・仲野太賀ほか、監督・瀬々敬久。12.25 Fri.公開(公式サイト表記)','https://sukiyaki.toho-movie.jp/',True,period='2026年12月25日公開',kind='イベント'),
# ---- ナイトライフ・バー(常設) ----
R(NIGHT,'マンダリンバー(マンダリン オリエンタル 東京)','中央区 日本橋室町','東京を見下ろすホテルのバー。シグネチャーカクテルとモクテル。12歳未満は20:00まで利用可、スマートカジュアル(公式)','https://www.mandarinoriental.com/ja/tokyo/nihonbashi/dine/mandarin-bar',True,kind='常設',venue='中央区日本橋室町2-1-1',reservation='テーブル予約は公式から'),
R(NIGHT,'JZ Brat Sound of Tokyo(渋谷セルリアンタワー)','渋谷区 桜丘町','ジャズ中心のライブレストラン。公演スケジュールは公式で確認','https://www.jzbrat.com/',True,kind='常設',venue='渋谷セルリアンタワー 2F',reservation='電話予約 03-5728-0168(平日14:00〜18:00)。予約・入場システムは公式で確認'),
R(NIGHT,'ルーフトップバー(アンダーズ東京 52階)','港区 虎ノ門','虎ノ門ヒルズの屋上バー。日〜木17:00〜24:00、金土17:00〜25:00。3〜12月の20時以降はテラス席に1人2,200円のカバーチャージ(公式)','https://www.andaztokyo.jp/restaurants/jp/rooftop-bar',False,kind='常設',venue='アンダーズ 東京 52階',note='テラス席は喫煙可'),
R(NIGHT,'SOAK(MIYASHITA PARK 18F ルーフトップレストラン&バー)','渋谷区 神宮前','渋谷の街並みと夜景を見渡すルーフトップのレストラン&バー(公式)','https://soaks.tokyo/',False,kind='常設',venue='渋谷区神宮前6-20-10 MIYASHITA PARK North 18F',reservation='公式・LINEから予約可'),
# ---- 書店・ブックカフェ / 動物カフェ(常設) ----
R(BOOK,'森の図書室(渋谷)','渋谷区 宇田川町','渋谷駅すぐの本に囲まれたブックカフェ・バー。本に出てくる食べ物をイメージしたメニュー。準会員制だが会員以外も利用可(公式)','https://morinotosyoshitsu.com/',True,kind='常設',venue='渋谷区宇田川町23-3 渋谷第一勧銀共同ビル8F'),
R(ANI,'カピねこカフェ(capyneko cafe)吉祥寺・原宿','武蔵野市 吉祥寺','カピバラと猫にふれあえるカフェ。40分 吉祥寺2,800円/原宿3,850円、1歳未満無料(公式)','https://capyneko.cafe/',True,kind='常設',venue='吉祥寺 PLATANO 2F/原宿 Bsquare竹下通り 2F',reservation='予約制(公式の予約ページ)'),
# ---- 収穫体験 ----
R(HARV,'イチゴス横浜(いちご狩り 2026-2027シーズン)','神奈川県 横浜市','いちご狩り農園。2026-2027シーズンは料金改定と年齢区分の変更あり。12月の開園はいちごの生育しだい(公式)','https://ichigos.jp/ichigogari-2026-2027/',False,kind='イベント',reservation='2月以降分の予約は11/2(月)20:00から受付(公式)',note='開園日は公式で要確認'),
]
TREND.update({'祝3000しゅ～ねん!?超たまごっち祭 in シブハラ':'','ゴジラ博 マイナスの世界(大丸東京店)':'','東京コミコン2026(幕張メッセ)':''})
