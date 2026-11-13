"""buffet_spots.py の「ビュッフェ・食べ放題」を spots.json / spots.csv にマージ(何度実行しても同じ結果)。"""
import json,csv
exec(open('buffet_spots.py',encoding='utf-8').read())
FIELDS=['genre','name','area','desc','url','period','url_status','url_note','period_note','trending','venue','reservation','age','baby_ok','baby','kind','rain_ok']
rows=[]
for ln in ROWS.strip().splitlines():
    kind,name,area,venue,desc,url,period,resv,note,trend,baby=ln.split('|')
    area=area.replace('東京都 ','',1) if area.startswith('東京都 ') else area
    if trend.strip() not in ('','1'): note=(note+'(' if note else '')+trend+(')' if note else '')
    rows.append(dict(genre=G,kind=kind,name=name,area=area,venue=venue,desc=desc,url=url,url_status='ok',url_note='',
        period=period,period_note=note,reservation=resv,trending=bool(trend.strip()),baby_ok=bool(baby.strip()),baby=baby.strip(),age=''))
data=[d for d in json.load(open('spots.json',encoding='utf-8')) if d['genre']!=G]
for d in data:
    for k in FIELDS: d.setdefault(k,False if k in('baby_ok','trending','rain_ok') else '')
for r in rows:
    for k in FIELDS: r.setdefault(k,False if k in('baby_ok','trending','rain_ok') else '')
data+=rows
json.dump(data,open('spots.json','w',encoding='utf-8'),ensure_ascii=False,indent=1)
w=csv.DictWriter(open('spots.csv','w',encoding='utf-8-sig',newline=''),fieldnames=FIELDS);w.writeheader();w.writerows({k:d.get(k,'') for k in FIELDS} for d in data)
print('spots',len(data),'buffet',len(rows),'trending',sum(r['trending'] for r in rows),'baby',sum(r['baby_ok'] for r in rows))
