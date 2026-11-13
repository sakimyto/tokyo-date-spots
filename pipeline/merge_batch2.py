"""第2・3弾(batch2_spots.py + batch2b_stage.py + batch3_factory.py)を spots.json / spots.csv にマージ。何度実行しても同じ結果。
- 既存の名前と重複する新規行はスキップしない(同名は置換)。
- TREND の名前は、元ジャンルの行を genre='話題'・trending=True で複製(元の行は trending=False のまま)。
- 各行の rain 判断(R(... rain=...))は rain_manual.json に記録(apply_rain.py が最優先で使う)。
実行後は python3 apply_rain.py を実行すること。"""
import json,csv,os
exec(open('batch2_spots.py',encoding='utf-8').read())
exec(open('batch2b_stage.py',encoding='utf-8').read().replace("exec(open('batch2_spots.py').read().split('ROWS=[')[0])",""))
exec(open('batch3_factory.py',encoding='utf-8').read())
exec(open('batch4_engei.py',encoding='utf-8').read().replace("exec(open('batch2_spots.py',encoding='utf-8').read().split('ROWS=[')[0])",""))
exec(open('batch5_weekly.py',encoding='utf-8').read())
exec(open('batch6_weekly.py',encoding='utf-8').read())
ALL=ROWS+ROWS2+ROWS3+ROWS4+ROWS5+ROWS6
FIELDS=['genre','name','area','desc','url','period','url_status','url_note','period_note','trending','venue','reservation','age','baby_ok','baby','kind','rain_ok']
BOOLS=('baby_ok','trending','rain_ok')
manual=json.load(open('rain_manual.json',encoding='utf-8')) if os.path.exists('rain_manual.json') else {}
names={r['name'] for r in ALL}
MOVE={'アトリエうかい Cafe & Factory HACHIOJI':'工場見学・ものづくり'}  # 既存行のジャンル移動
data=[d for d in json.load(open('spots.json',encoding='utf-8')) if d['name'] not in names and not (d['genre']=='話題' and d['name'] in TREND)]
for d in data:
    for k in FIELDS: d.setdefault(k,False if k in BOOLS else '')
    if d['name'] in MOVE: d['genre']=MOVE[d['name']]
for r in ALL:
    r=dict(r); r.setdefault('url_status','ok'); r.setdefault('url_note','')
    manual[r['name']]=bool(r['rain_ok'])
    for k in FIELDS: r.setdefault(k,False if k in BOOLS else '')
    data.append(r)
src={d['name']:d for d in data if d['genre']!='話題'}
missing=[n for n in TREND if n not in src]
assert not missing,missing
for n,extra in TREND.items():
    d=dict(src[n]); d['genre']='話題'; d['trending']=True
    if extra:
        d['period_note']=(extra+' / '+d['period_note']) if d['period_note'] else extra
    data.append(d)
json.dump(data,open('spots.json','w',encoding='utf-8'),ensure_ascii=False,indent=1)
json.dump(manual,open('rain_manual.json','w',encoding='utf-8'),ensure_ascii=False,indent=1,sort_keys=True)
w=csv.DictWriter(open('spots.csv','w',encoding='utf-8-sig',newline=''),fieldnames=FIELDS);w.writeheader();w.writerows({k:d.get(k,'') for k in FIELDS} for d in data)
print('spots',len(data),'rows',len(ALL),'trend',len(TREND))
