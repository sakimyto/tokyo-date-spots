"""miniature_spots.py の ROWS を spots.json / spots.csv にマージ(名前単位・何度実行しても同じ結果)。
rain_ok は apply_rain.py が付けるので、マージ後に python3 apply_rain.py を実行すること。"""
import json,csv
exec(open('miniature_spots.py',encoding='utf-8').read())
FIELDS=['genre','name','area','desc','url','period','url_status','url_note','period_note','trending','venue','reservation','age','baby_ok','baby','kind','rain_ok']
BOOLS=('baby_ok','trending','rain_ok')
names={r['name'] for r in ROWS}
data=[d for d in json.load(open('spots.json',encoding='utf-8')) if d['name'] not in names]
for d in data:
    for k in FIELDS: d.setdefault(k,False if k in BOOLS else '')
for r in ROWS:
    r=dict(r); r.setdefault('url_status','ok'); r.setdefault('url_note','')
    for k in FIELDS: r.setdefault(k,False if k in BOOLS else '')
    data.append(r)
json.dump(data,open('spots.json','w',encoding='utf-8'),ensure_ascii=False,indent=1)
w=csv.DictWriter(open('spots.csv','w',encoding='utf-8-sig',newline=''),fieldnames=FIELDS);w.writeheader();w.writerows({k:d.get(k,'') for k in FIELDS} for d in data)
print('spots',len(data),'miniature',len(ROWS))
