#!/usr/bin/env python3
"""usage: ctx.py URL::kw1,kw2 ... -> code, title, and ~200 chars around first 2 hits of each kw (parallel)"""
import sys,re
from concurrent.futures import ThreadPoolExecutor

from peek import get
W=int(__import__('os').environ.get('W','110'))
def run(arg):
    u,_,kws=arg.partition('::')
    code,eu,h=get(u)
    t=re.search(r'<title[^>]*>(.*?)</title>',h,re.S|re.I)
    h2=re.sub(r'<script.*?</script>|<style.*?</style>|<!--.*?-->','',h,flags=re.S|re.I)
    tx=re.sub(r'\s+',' ',re.sub(r'<[^>]+>',' ',h2))
    import html as H; tx=H.unescape(tx)
    o=[f'## {u} [{code}] {"-> "+eu if eu.rstrip("/")!=u.rstrip("/") else ""} len={len(tx)}','title: '+(re.sub(r"\s+"," ",t.group(1)).strip()[:100] if t else '-')]
    for k in [k for k in kws.split(',') if k]:
        hits=[m.start() for m in re.finditer(re.escape(k),tx)][:2]
        if not hits: o.append(f'  [{k}] NONE')
        for p in hits: o.append(f'  [{k}] '+tx[max(0,p-W):p+W])
    return '\n'.join(o)
with ThreadPoolExecutor(10) as ex:
    for r in ex.map(run,sys.argv[1:]): print(r)
