import sys,re,html,subprocess
KW=sys.argv[2].split(',') if len(sys.argv)>2 else ['0歳','歳','授乳','おむつ','オムツ','ベビーカー','予約','開催期間','会期']
u=sys.argv[1]
r=subprocess.run(['curl','-sL','--compressed','-m','25','-A','Mozilla/5.0 (Windows NT 10.0) Chrome/124','-w','\n__CODE__%{http_code}',u],capture_output=True)
t=r.stdout.decode('utf-8','ignore');code=t.rsplit('__CODE__',1)[-1]
t=re.sub(r'<script.*?</script>|<style.*?</style>','',t,flags=re.S);t=re.sub(r'<[^>]+>',' ',t);t=re.sub(r'\s+',' ',html.unescape(t))
print('==',u,'code',code,'rc',r.returncode,'len',len(t))
seen=0
for k in KW:
  for m in list(re.finditer(re.escape(k),t))[:2]:
    print("  ["+k+"]",t[max(0,m.start()-60):m.end()+80]);seen+=1
  if seen>14:break
