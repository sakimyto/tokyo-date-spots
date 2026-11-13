import subprocess,re,json,concurrent.futures as cf,html
rows=[];g=None
for l in open('data2.txt'):
    l=l.rstrip('\n')
    if not l.strip(): continue
    if l.startswith('#'): g=l[1:];continue
    p=(l.split('|')+['']*6)[:6]
    if not p[0] or not p[2]: continue
    rows.append(dict(genre=g,name=p[0],area=p[1],desc=p[2],url=p[3].strip(),period=p[4],kw=p[5]))
def chk(r):
    u=r['url']
    if not u: return 'NOURL',0,''
    pr=subprocess.run(['curl','-sL','--compressed','-m','20','-A','Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 Chrome/124 Safari/537.36','-H','Accept-Language: ja','-w','\n@@%{http_code}@@%{url_effective}',u],capture_output=True)
    out=pr.stdout
    m=re.search(rb'\n@@(\d+)@@(.*)$',out)
    code=int(m.group(1)) if m else 0; body=out[:m.start()] if m else b''
    try:
        enc='utf-8'
        mm=re.search(rb'charset=["\']?([\w-]+)',body[:3000],re.I)
        if mm: enc=mm.group(1).decode()
        t=body.decode(enc,'ignore')
    except Exception: t=body.decode('utf-8','ignore')
    tm=re.search(r'<title[^>]*>(.*?)</title>',t,re.S|re.I); title=html.unescape(tm.group(1).strip())[:80] if tm else ''
    kw=r['kw'] or r['name'][:4]
    if code in (403,429,503,0) or (code>=200 and code<300 and len(t)<500 and kw not in t): st='BLOCKED'
    elif code in (404,410) or code>=400: st='BAD'
    elif kw.lower() in t.lower() or kw in html.unescape(t): st='OK'
    else: st='MISMATCH'
    if re.search(r'not found|ページが見つかりません|お探しのページ',title,re.I): st='BAD'
    return st,code,title
with cf.ThreadPoolExecutor(32) as ex: res=list(ex.map(chk,rows))
for r,(s,c,t) in zip(rows,res): r['status']=s;r['code']=c;r['title']=t
json.dump(rows,open('verify.json','w'),ensure_ascii=False,indent=0)
from collections import Counter;print(Counter(r['status'] for r in rows))
for r in rows:
    if r['status'] not in('OK',): print(r['status'],r['code'],r['name'],r['url'],'|',r['title'])
