"""collab_events.py の「キャラクター・コラボイベント」を spots.json / spots.csv にマージ(何度実行しても同じ結果)。
build_verify.py で spots.json を作り直した後にも実行すること。"""
import json,csv
exec(open('collab_events.py',encoding='utf-8').read())
data=[d for d in json.load(open('spots.json',encoding='utf-8')) if d['genre']!=G]
FIELDS=['genre','name','area','desc','url','period','url_status','url_note','period_note','trending','venue','reservation','age','baby_ok','baby','kind','rain_ok']
for d in data:
    for k in FIELDS: d.setdefault(k,False if k in('baby_ok','trending','rain_ok') else '')
for r in rows:
    for k in FIELDS: r.setdefault(k,False if k in('baby_ok','trending','rain_ok') else '')
data+=rows
json.dump(data,open('spots.json','w',encoding='utf-8'),ensure_ascii=False,indent=1)
w=csv.DictWriter(open('spots.csv','w',encoding='utf-8-sig',newline=''),fieldnames=FIELDS);w.writeheader();w.writerows({k:d.get(k,'') for k in FIELDS} for d in data)
print('spots',len(data),'collab',len(rows))
