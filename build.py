"""spots.json -> index.html を生成(データは変更しない)。
URLの再検証込みで spots.json/csv から作り直す場合は build_verify.py を使う。"""
import json,html,datetime,sys
UPDATED=sys.argv[1] if len(sys.argv)>1 else '2026-10-19'
data=json.load(open('spots.json',encoding='utf-8'))
n=len(data); g=len(set(d['genre'] for d in data))
desc=f'東京・関東のデート・おでかけ先候補{n}件を{g}ジャンルで一覧。赤ちゃん連れ向けも。最新の話題スポット、イルミネーション・紅葉の会期、公式サイトとGoogleマップへのリンク付き。'
js=json.dumps(data,ensure_ascii=False).replace('</','<\\/')
out=open('tpl.html',encoding='utf-8').read()
out=out.replace('__DESC__',html.escape(desc)).replace('__UPDATED__',UPDATED).replace('__DATA__',js)
open('index.html','w',encoding='utf-8').write(out)
print('index.html',n,'spots',len(out),'bytes')
