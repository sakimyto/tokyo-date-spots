import json,csv,time,subprocess
from collections import Counter
import importlib.util
spec=importlib.util.spec_from_file_location('v','verify.py')
# reuse chk without rerunning main: copy minimal
src=open('verify.py').read().split('with cf.ThreadPoolExecutor')[0]
ns={};exec(src,ns);chk=ns['chk']
rows=json.load(open('verify.json'))
for r in rows:
    if r['status'] not in('OK','NOURL'):
        for _ in range(2):
            s,c,t=chk(r)
            if s=='OK': r['status']='OK';break
            time.sleep(1)
MANUAL_OK={'ARTE TOKYO(東京国際文化芸術祭)','カレッタ汐留','東京ディズニーランド','アサヒビール 茨城工場'}
AGG={'MIDTOWN CHRISTMAS 2026','よみうりランド ジュエルミネーション2026 Growing Light','さがみ湖イルミリオン 2026-2027','東京ドイツ村 ウインターイルミネーション','あしかがフラワーパーク 光の花の庭','東武動物公園 ウインターイルミネーション','東京メガイルミ','ホテル椿山荘東京 森のオーロラと雫の煌めき','恵比寿ガーデンプレイス Baccarat ETERNAL LIGHTS','HIBIYA Magic Time Illumination 2026','東京ドームシティ ウィンターイルミネーション','東京スカイツリータウン ドリームクリスマス2026','表参道イルミネーション2026','ムーミン谷のクリスマス 2026','国営昭和記念公園 黄葉・紅葉まつり&秋の夜散歩'}
out=[]
for r in rows:
    st=r['status']
    if r['name'] in MANUAL_OK: us='ok'
    elif st=='OK': us='ok'
    elif st=='NOURL': us='none'
    else: us='blocked'
    note=''
    if us=='blocked': note='URLは検索で公式と確認済みだが、アクセス制限/JS描画のため中身を直接確認できず'
    if us=='none': note='エリア・街歩き等で単一の公式サイトなし' if r['genre']!='季節イベント' else '公式ページ未確認'
    pn='会期はイベント情報サイト(Walker+/enjoytokyo/のびば/キョウチカ等)掲載値。公式発表との照合は未実施' if r['name'] in AGG else ''
    out.append(dict(genre=r['genre'],name=r['name'],area=r['area'],desc=r['desc'],url=r['url'],period=r['period'],url_status=us,url_note=note,period_note=pn,trending=r['genre']=='話題'))
json.dump(out,open('spots.json','w'),ensure_ascii=False,indent=1)
w=csv.DictWriter(open('spots.csv','w',encoding='utf-8-sig',newline=''),fieldnames=out[0].keys());w.writeheader();w.writerows(out)
open('index.html','w').write(open('tpl.html').read().replace('__DATA__',json.dumps(out,ensure_ascii=False)).replace('__UPDATED__','2026-10-19'))
print(Counter(o['genre'] for o in out));print(Counter(o['url_status'] for o in out))
for o in out:
    if o['url_status']!='ok': print(o['url_status'],o['name'])
