"""baby_spots.py の「赤ちゃん・親子」を spots.json / spots.csv にマージし、既存スポットに👶赤ちゃんOKの印を付ける。
merge_collab.py の後に実行する(何度実行しても同じ結果)。"""
import json,csv
exec(open('baby_spots.py',encoding='utf-8').read())
FIELDS=['genre','name','area','desc','url','period','url_status','url_note','period_note','trending','venue','reservation','age','baby_ok','baby','kind','rain_ok']
data=[d for d in json.load(open('spots.json',encoding='utf-8')) if d['genre']!=G]
hit=set()
for d in data:
    for k in FIELDS: d.setdefault(k,False if k in('baby_ok','trending','rain_ok') else '')
    if d['name'] in MARK:
        d['baby_ok']=True; d['baby']=MARK[d['name']]; hit.add(d['name'])
    else:
        d['baby_ok']=False; d['baby']=''
missing=set(MARK)-hit
assert not missing, missing
data+=rows
json.dump(data,open('spots.json','w',encoding='utf-8'),ensure_ascii=False,indent=1)
w=csv.DictWriter(open('spots.csv','w',encoding='utf-8-sig',newline=''),fieldnames=FIELDS);w.writeheader();w.writerows({k:d.get(k,'') for k in FIELDS} for d in data)
print('spots',len(data),'baby genre',len(rows),'marked existing',len(hit),'baby_ok total',sum(1 for d in data if d['baby_ok']))
