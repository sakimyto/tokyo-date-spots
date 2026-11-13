"""Claudeの採用成果物を機械検査する。データ・ソースは変更しない。"""
import argparse
import datetime as dt
import json
from pathlib import Path
import re
from urllib.parse import urlsplit, urlunsplit

ROOT = Path(__file__).resolve().parents[1]
STRINGS = ('genre', 'name', 'area', 'desc', 'url', 'period', 'venue', 'reservation',
           'kind', 'period_note', 'url_status', 'url_note', 'source_checked_at', 'source_evidence', 'venue_status', 'venue_evidence')
NONEMPTY = ('genre', 'name', 'area', 'desc', 'url', 'venue', 'kind', 'source_evidence')


def canonical_url(url):
    parsed = urlsplit(url.strip())
    if parsed.scheme.lower() not in ('https', 'http') or not parsed.hostname or parsed.username or parsed.password:
        raise ValueError('公式URLの形式が不正')
    return urlunsplit((parsed.scheme.lower(), parsed.netloc.lower(), parsed.path.rstrip('/'), '', ''))


def period_intervals(text, note=''):
    intervals = []
    year = None
    for part in text.split('、'):
        first = re.match(r'\s*(?:(\d{4})年)?(\d{1,2})月(\d{1,2})日', part)
        if not first or not (first[1] or year):
            return None
        year = int(first[1] or year)
        try:
            start = dt.date(year, int(first[2]), int(first[3]))
            tail = re.sub(r'^[（(][^）)]*[）)]', '', part[first.end():]).strip()
            last = re.match(r'([〜～~・])\s*(?:(\d{4})年)?(?:(\d{1,2})月)?(\d{1,2})日', tail)
            if last:
                separator, yy, mm, dd = last.groups()
                end = dt.date(int(yy or year), int(mm or first[2]), int(dd))
                if not yy and end < start:
                    end = end.replace(year=year + 1)
                if end < start:
                    return None
                intervals.extend([(start, start), (end, end)] if separator == '・' else [(start, end)])
            elif '1日のみ' in tail + note or tail == 'のみ':
                intervals.append((start, start))
            else:
                return None
        except ValueError:
            return None
    return sorted(intervals) or None


def period_bounds(text, note=''):
    intervals = period_intervals(text, note)
    return (min(s for s, _ in intervals), max(e for _, e in intervals)) if intervals else None


def period_phase(text, date, note=''):
    intervals = period_intervals(text, note)
    if not intervals:
        return None
    if any(start <= date <= end for start, end in intervals):
        return 'now'
    return 'ended' if date > max(end for _, end in intervals) else 'soon'


def confirmed_venue(row):
    # A nonempty instruction to check a venue is not a confirmed physical venue.
    return (row.get('venue_status') == 'confirmed'
            and bool(row.get('venue_evidence', '').strip())
            and bool(row.get('venue', '').strip())
            and not re.search(r'未確認|未定|各劇場|上映館は|で確認|要確認', row['venue']))


def validate(additions, removals, baseline, date):
    if not isinstance(additions, list) or not isinstance(removals, list):
        raise ValueError('COLLECTED.jsonとREMOVE.jsonは配列が必要')
    names = {row['name'].strip() for row in baseline}
    urls = {canonical_url(row['url']) for row in baseline if row['url']}
    accepted, rejected, deleted, rejected_removals = [], [], [], []
    for index, row in enumerate(additions):
        try:
            if not isinstance(row, dict):
                raise ValueError('行はobjectが必要')
            missing = [key for key in STRINGS if not isinstance(row.get(key), str)]
            missing += [key for key in NONEMPTY if isinstance(row.get(key), str) and not row[key].strip()]
            missing += [key for key in ('rain_ok', 'baby_ok') if type(row.get(key)) is not bool]
            if missing:
                raise ValueError('必須フィールド欠落・型不正: ' + ', '.join(missing))
            if not confirmed_venue(row):
                raise ValueError('公式会場の確認が完了していない（venue_status / venue_evidence）')
            if row['source_checked_at'] != date.isoformat() + ' JST':
                raise ValueError('公式確認日が対象週と不一致')
            if row['url_status'] != 'ok':
                raise ValueError('公式本文の確認が完了していない')
            if row['kind'] not in ('イベント', '常設'):
                raise ValueError('kindはイベントまたは常設が必要')
            if row['kind'] == 'イベント' and not row['period'].strip():
                raise ValueError('イベントの会期がない')
            period = period_bounds(row['period'], row.get('period_note', ''))
            if period and period[1] < date:
                raise ValueError('追加候補の会期が終了済み')
            name, url = row['name'].strip(), canonical_url(row['url'])
            if name in names:
                raise ValueError('既存または候補間で名前が重複')
            if url in urls:
                raise ValueError('既存または候補間で公式URLが重複（クエリを除く）')
            names.add(name)
            urls.add(url)
            accepted.append(row)
        except (ValueError, TypeError) as error:
            rejected.append({'index': index, 'name': row.get('name', '') if isinstance(row, dict) else '', 'reason': str(error)})
    existing = {(row['genre'], row['name']): row for row in baseline}
    removed_keys = set()
    for index, row in enumerate(removals):
        try:
            if not isinstance(row, dict) or not all(isinstance(row.get(k), str) and row[k].strip()
                    for k in ('genre', 'name', 'period', 'url', 'reason')):
                raise ValueError('除外行の必須フィールドがない')
            key = row['genre'], row['name']
            old = existing.get(key)
            if not old or old['period'] != row['period'] or canonical_url(old['url']) != canonical_url(row['url']):
                raise ValueError('既存行の会期・URLと一致しない')
            bounds = period_bounds(row['period'], old.get('period_note', ''))
            if not bounds or bounds[1] >= date or old.get('kind') == '常設':
                raise ValueError('終了確定の期間イベントではない（常設・開業日・当日以降終了を保持）')
            if key in removed_keys:
                raise ValueError('除外候補内で重複')
            removed_keys.add(key)
            deleted.append(row)
        except (ValueError, TypeError) as error:
            rejected_removals.append({'index': index, 'name': row.get('name', '') if isinstance(row, dict) else '', 'reason': str(error)})
    return {'ready': len(accepted) >= 30 and not rejected_removals,
            'accepted': accepted, 'rejected': rejected, 'removals': deleted,
            'rejected_removals': rejected_removals}


def main():
    parser = argparse.ArgumentParser(description=__doc__)
    parser.add_argument('collection', type=Path)
    parser.add_argument('--date', required=True, type=dt.date.fromisoformat)
    parser.add_argument('--output', type=Path, help='全検査結果の保存先（repository外）')
    args = parser.parse_args()
    required = ('COLLECTED.json', 'REMOVE.json', 'NOTES.md', 'MODEL.txt')
    missing = [name for name in required if not (args.collection / name).is_file()]
    if missing:
        print(json.dumps({'ready': False, 'missing': missing}, ensure_ascii=False))
        return 2
    report = validate(json.loads((args.collection / 'COLLECTED.json').read_text()),
                      json.loads((args.collection / 'REMOVE.json').read_text()),
                      json.loads((ROOT / 'spots.json').read_text()), args.date)
    report['model'] = (args.collection / 'MODEL.txt').read_text().strip()
    if args.output:
        output = args.output.resolve()
        if output == ROOT or ROOT in output.parents:
            raise ValueError('検査結果はrepository外へ保存してください')
        output.write_text(json.dumps(report, ensure_ascii=False, indent=2) + '\n')
    print(json.dumps({'ready': report['ready'], 'accepted': len(report['accepted']),
                      'rejected': report['rejected'], 'removals': len(report['removals']),
                      'rejected_removals': report['rejected_removals'], 'model': report['model']}, ensure_ascii=False))
    return 0 if report['ready'] else 2


if __name__ == '__main__':
    raise SystemExit(main())
