#!/usr/bin/env python3
"""公式ページを開いて 状態コード/タイトル/住所/営業時間/料金/指定キーワードの有無 を表示。
usage: peek.py URL[::kw1,kw2] ...   (並列8)"""
import sys,re,subprocess
from concurrent.futures import ThreadPoolExecutor
def get(u):
    r=subprocess.run(['curl','-sL','-m','25','-A','Mozilla/5.0 (X11; Linux x86_64) Chrome/120','-w','\n__CODE__%{http_code} __URL__%{url_effective}',u],capture_output=True)
    b=r.stdout
    m=re.search(rb'\n__CODE__(\d+) __URL__(.*)$',b,re.S)
    code,eu=(m.group(1).decode(),m.group(2).decode()) if m else ('0','')
    b=b[:m.start()] if m else b
    h=None
    mc=re.search(rb'charset=["\']?([\w-]+)',b[:3000],re.I)
    encs=[mc.group(1).decode()] if mc else []
    for e in encs+['utf-8','cp932','euc-jp']:
        try: h=b.decode(e);break
        except Exception: pass
    if h is None: h=b.decode('utf-8','ignore')
    return code,eu,h
def run(arg):
    u,_,kws=arg.partition('::')
    code,eu,h=get(u)
    t=re.search(r'<title[^>]*>(.*?)</title>',h,re.S|re.I)
    h2=re.sub(r'<script.*?</script>|<style.*?</style>|<!--.*?-->','',h,flags=re.S)
    tx=re.sub(r'\s+',' ',re.sub(r'<[^>]+>',' ',h2))
    out=[f'## {u} [{code}] {"-> "+eu if eu!=u else ""}']
    out.append('title: '+re.sub(r'\s+',' ',t.group(1)).strip()[:100] if t else 'title: -')
    for lab,pat,w in [('addr',r'(〒\s?\d{3}-?\d{4}[^。]{0,60})',1),('hours',r'((?:営業時間|開館時間|OPEN|開場時間|営業日時|受付時間)[^。]{0,90})',1),('fee',r'((?:料金|入場料|入館料|観覧料|入園料)[^。]{0,70})',1)]:
        ms=re.findall(pat,tx)
        if ms: out.append(f'{lab}: '+' | '.join(x.strip() for x in ms[:w]))
    if kws:
        out.append('kw: '+', '.join(f'{k}={"Y" if k in tx else "N"}' for k in kws.split(',')))
    return '\n'.join(out)
if __name__=='__main__':
    with ThreadPoolExecutor(8) as ex:
        for o in ex.map(run,sys.argv[1:]): print(o)
