"""rain_ok等を確定したspots.jsonから、JSONのキー順でCSVを再生成する。"""
import csv
import json
with open('spots.json', encoding='utf-8') as source:
    rows = json.load(source)
with open('spots.csv', 'w', encoding='utf-8-sig', newline='') as target:
    writer = csv.DictWriter(target, fieldnames=list(rows[0]), lineterminator='\n')
    writer.writeheader()
    writer.writerows(rows)
print('spots.csv', len(rows), 'rows')
