"""全行に rain_ok(☔雨の日OK)を付ける。spots.json を更新するだけで冪等。merge_*.py を実行したあとに必ず実行する。
基準: 主な体験が屋内で完結し、雨でも十分楽しめる(屋外メインの体験・景色が主役のものは付けない)。迷ったら False。
優先順位(上が強い):
 1. rain_manual.json … 名前→bool。バッチ(merge_batch2.py)の各行で調べた個別判断。
 2. 話題 の行は同名の元ジャンル行の判断を引き継ぐ(+ 下の WADAI_* で個別に上書き)
 3. OVERRIDE_TRUE / OVERRIDE_FALSE … (ジャンル, 名前に含まれる語) の個別補正リスト
 4. GENRE_DEFAULT … ジャンルの既定値
 5. 上記以外・新ジャンルは、名前・説明のキーワード(KW_*)で判定。どれにも当たらなければ False。
公式の記載で屋内/雨天可が確認できないものには付けない。新ジャンルを足したら GENRE_DEFAULT に追記する。"""
import json,sys
GENRE_DEFAULT={
 '歌舞伎・落語・お笑い・演芸':True,
 '美術館・博物館':True,'映画館・プラネタリウム':True,'ビュッフェ・食べ放題':True,'体験型':True,'カフェ・食べ歩き':True,
 '舞台・ミュージカル・ライブ':True,'工場見学・ものづくり':True,'動物カフェ・ふれあい':True,'遊び・スポーツ体験':True,
 '書店・ブックカフェ':True,'ナイトライフ・バー':True,'赤ちゃん・親子':True,'キャラクター・コラボイベント':True,
 '公園・庭園・花畑':False,'アウトドア':False,'展望台・夜景':False,'日帰り旅':False,'収穫体験':False,'季節イベント':False,
 '水族館・動物園':False,'テーマパーク・遊園地':False,'プール・スパ・温泉':False,'買い物・街歩き':False,'スポーツ観戦・ライブ':False,
}
# (ジャンル, 名前に含まれる語)。語は必ず1行以上に当たること(当たらないと警告)。
OVERRIDE_TRUE=[
 ('季節イベント','デザインフェスタ'),
 ('テーマパーク・遊園地','サンリオピューロランド'),('テーマパーク・遊園地','ワーナー ブラザース スタジオツアー'),('テーマパーク・遊園地','東京ジョイポリス'),
 ('テーマパーク・遊園地','レゴランド'),('テーマパーク・遊園地','スモールワールズ'),
 ('水族館・動物園','すみだ水族館'),('水族館・動物園','マクセル アクアパーク'),('水族館・動物園','サンシャイン水族館'),('水族館・動物園','葛西臨海水族園'),
 ('水族館・動物園','しながわ水族館'),('水族館・動物園','カワスイ'),('水族館・動物園','新江ノ島水族館'),('水族館・動物園','大洗水族館'),
 ('プール・スパ・温泉','天成園'),('プール・スパ・温泉','スパジアム'),('プール・スパ・温泉','竜泉寺の湯'),('プール・スパ・温泉','庭の湯'),('プール・スパ・温泉','ラクーア'),
 ('プール・スパ・温泉','万葉倶楽部'),('プール・スパ・温泉','泉天空の湯'),('プール・スパ・温泉','江戸遊'),('プール・スパ・温泉','平和島'),('プール・スパ・温泉','箱根湯寮'),
 ('プール・スパ・温泉','天山湯治郷'),('プール・スパ・温泉','utatane'),('プール・スパ・温泉','テルマー湯'),('プール・スパ・温泉','SPA:BLIC'),
 ('プール・スパ・温泉','黄金湯'),('プール・スパ・温泉','ゆとろ嵯峨沢'),
 ('買い物・街歩き','GINZA SIX'),('買い物・街歩き','渋谷サクラステージ'),('買い物・街歩き','渋谷ストリーム'),('買い物・街歩き','麻布台ヒルズ'),
 ('買い物・街歩き','東京ミッドタウン日比谷'),('買い物・街歩き','虎ノ門ヒルズ ステーションタワー'),('買い物・街歩き','有明ガーデン'),('買い物・街歩き','ららぽーと豊洲'),
 ('買い物・街歩き','TOFROM YAESU'),('買い物・街歩き','KITTE丸の内'),
 ('スポーツ観戦・ライブ','東京ドーム'),('スポーツ観戦・ライブ','両国国技館'),('スポーツ観戦・ライブ','有明アリーナ'),('スポーツ観戦・ライブ','TOYOTA ARENA'),
 ('スポーツ観戦・ライブ','Kアリーナ'),('スポーツ観戦・ライブ','Billboard'),('スポーツ観戦・ライブ','ブルーノート'),('スポーツ観戦・ライブ','GMOアリーナ'),
 ('スポーツ観戦・ライブ','日本武道館'),('スポーツ観戦・ライブ','LaLa arena'),('スポーツ観戦・ライブ','後楽園ホール'),('スポーツ観戦・ライブ','COTTON CLUB'),
 ('映画館・プラネタリウム','ユナイテッド・シネマ豊洲'),
]
OVERRIDE_FALSE=[
 ('美術館・博物館','彫刻の森'),('美術館・博物館','たてもの園'),('美術館・博物館','ZEN NIGHT'),
 ('体験型','シンフォニー'),('体験型','マリーンルージュ'),
 ('カフェ・食べ歩き','仲見世'),('カフェ・食べ歩き','谷中銀座'),('カフェ・食べ歩き','戸越銀座'),('カフェ・食べ歩き','アメ横'),('カフェ・食べ歩き','ルーフトップ'),
 ('赤ちゃん・親子','こどもの国'),('赤ちゃん・親子','アンデルセン公園'),('赤ちゃん・親子','上野動物園'),('赤ちゃん・親子','多摩動物公園'),('赤ちゃん・親子','ハイハイレース'),
 ('キャラクター・コラボイベント','レジェンドリサーチ'),('キャラクター・コラボイベント','ディズニー・クリスマス'),('キャラクター・コラボイベント','BRIGHT HOLIDAY'),
 ('キャラクター・コラボイベント','TOKYO SNOW DOME'),('キャラクター・コラボイベント','ちいかわクリスマスマーケット'),('キャラクター・コラボイベント','アフロ犬'),
 ('キャラクター・コラボイベント','SAKAMOTO DAYS POP UP STREET'),
]
# 話題(トレンド)の行: 屋内で完結するものだけ True。同名の元行があればその判断を引き継ぎ、ここで上書き。
WADAI_TRUE=['TOFROM YAESU TOWER','自由が丘ミューズスクエア','Yebisu Beer Hall','GUNDAM BASE','MoN Takanawa','TOKYO DREAM PARK','レーヴ・デ・リュミエール',
 '江戸東京博物館','ワンダリア横浜','KAWAII MONSTER LAND','JOYPOLIS SPORTS','うんこミュージアム','横須賀美術館']
WADAI_FALSE=['mimimi','ARTE TOKYO','TAKANAWA GATEWAY','OIMACHI TRACKS','ポケパーク','OTO-RACTION','モリモリノボル','箱根海賊船','東京クリスマスマーケット','クリスマスマーケット',
 '東京クリスマスアドベント','Skytree Dream Christmas','ムーミン谷','Grandberry','イルミネーション','レジェンドリサーチ','ディズニー・クリスマス','BRIGHT HOLIDAY','SNOW DOME','アフロ犬','SAKAMOTO DAYS POP UP']
# 新ジャンル用(GENRE_DEFAULT に無い場合のみ)。名前・説明にこの語があれば屋内とみなす
KW_INDOOR=['美術館','博物館','ミュージアム','館','シアター','劇場','ホール','カフェ','ビュッフェ','工場見学','体験教室','工房','スタジオ','ホテル']
KW_OUTDOOR=['公園','庭園','花畑','ライトアップ','イルミネーション','花火','屋外','展望','ハイキング','キャンプ','BBQ','バーベキュー','遊覧','クルーズ']

def main():
    data=json.load(open('spots.json',encoding='utf-8'))
    manual=json.load(open('rain_manual.json',encoding='utf-8'))
    orig={}
    for d in data:
        if d['genre']!='話題': orig.setdefault(d['name'],d)
    hit=set()
    def ov(lst,g,n,key):
        for (gg,k) in lst:
            if gg==g and k in n:
                hit.add((key,gg,k)); return True
        return False
    out={}
    for d in data:
        g,n=d['genre'],d['name']
        if n in manual: v=manual[n]
        elif g=='話題':
            if any(k in n for k in WADAI_FALSE): v=False; [hit.add(('wf',k)) for k in WADAI_FALSE if k in n]
            elif any(k in n for k in WADAI_TRUE): v=True; [hit.add(('wt',k)) for k in WADAI_TRUE if k in n]
            elif n in orig: v=bool(orig[n].get('_rain',None)) if False else None
            else: v=False
        elif ov(OVERRIDE_TRUE,g,n,'t'): v=True
        elif ov(OVERRIDE_FALSE,g,n,'f'): v=False
        elif g in GENRE_DEFAULT: v=GENRE_DEFAULT[g]
        else:
            t=n+d.get('desc','')
            v=any(k in t for k in KW_INDOOR) and not any(k in t for k in KW_OUTDOOR)
        out[(g,n)]=v
        d['rain_ok']=v
    # 話題 で同名の元行から引き継ぐもの(v が None)
    for d in data:
        if d['genre']=='話題' and d['rain_ok'] is None:
            src=orig.get(d['name']); d['rain_ok']=bool(src['rain_ok']) if src else False
    json.dump(data,open('spots.json','w',encoding='utf-8'),ensure_ascii=False,indent=1)
    # 警告: どの行にも当たらなかった補正語
    miss=[('t',g,k) for g,k in OVERRIDE_TRUE if ('t',g,k) not in hit]+[('f',g,k) for g,k in OVERRIDE_FALSE if ('f',g,k) not in hit]
    miss+=[('wt',k) for k in WADAI_TRUE if ('wt',k) not in hit]+[('wf',k) for k in WADAI_FALSE if ('wf',k) not in hit]
    if miss: print('WARN 当たらなかった補正語:',miss,file=sys.stderr)
    import collections
    c=collections.Counter(); t=collections.Counter()
    for d in data: t[d['genre']]+=1; c[d['genre']]+=bool(d['rain_ok'])
    print('rain_ok',sum(c.values()),'/',len(data))
    for g in t: print(f'  {g}: {c[g]}/{t[g]}')
if __name__=='__main__': main()
