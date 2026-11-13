"""有限データの移管・同期・収集ゲートの検査。作業コピーは終了時に削除する。"""
import copy
import csv
import datetime as dt
import importlib.util
import json
from pathlib import Path
import re
import shutil
import tempfile
import unittest

ROOT = Path(__file__).resolve().parents[1]
SCRATCH = Path.home() / '_pjsc/_work/date-spots-migrate-1113'


def load_module(name):
    spec = importlib.util.spec_from_file_location(name, ROOT / 'pipeline' / (name + '.py'))
    module = importlib.util.module_from_spec(spec)
    spec.loader.exec_module(module)
    return module


collection = load_module('check_collection')
builder = load_module('rebuild')
pruner = load_module('prune_sources')
DATE = dt.date(2026, 11, 13)
UPDATED = dt.date.fromisoformat(re.search(r'最終更新\s+(\d{4}-\d{2}-\d{2})',
    (ROOT / 'index.html').read_text()).group(1))


def check_sync(folder):
    rows = json.loads((folder / 'spots.json').read_text())
    if len({(r['genre'], r['name']) for r in rows}) != len(rows):
        raise AssertionError('UNIQUE')
    with (folder / 'spots.csv').open(encoding='utf-8-sig', newline='') as file:
        actual_csv = list(csv.DictReader(file))
    expected_csv = [{key: str(value) for key, value in row.items()} for row in rows]
    if actual_csv != expected_csv:
        raise AssertionError('CSV_SYNC')
    html = (folder / 'index.html').read_text()
    embedded = json.loads(html.split('var D=', 1)[1].split(';\nD.forEach', 1)[0].replace('<\\/', '</'))
    if embedded != rows:
        raise AssertionError('HTML_SYNC')
    return rows


def candidate(index=0):
    return dict(genre='美術館・博物館', name=f'テスト候補{index}', area='東京都', desc='検査用',
                url=f'https://example.test/event/{index}/?lang=ja', period='2026年11月13日〜14日',
                venue='検査用会場', reservation='', kind='イベント', period_note='',
                url_status='ok', url_note='', source_checked_at='2026-11-13 JST',
                source_evidence='会期・会場を確認', rain_ok=True, baby_ok=False)


class CollectionTests(unittest.TestCase):
    def test_source_pruning_all_supported_row_shapes(self):
        text = '''ROWS = [R('g', 'ended', 'a'), dict(name='ended'), {'name':'ended'}, {'name':'keep'}]
rows.extend([{'name':'ended'}, {'name':'keep'}])
rows.append(dict(name='ended'))
TREND = {'ended':'old', 'keep':'new'}
MARK.update({'ended':'old', 'keep':'new'})
'''
        cleaned = pruner.prune_python(text, {'ended'})
        self.assertNotIn('ended', cleaned)
        self.assertIn('keep', cleaned)
        self.assertEqual(cleaned, pruner.prune_python(cleaned, {'ended'}))

    def test_minimum_and_required_fields(self):
        rows = [candidate(index) for index in range(30)]
        self.assertTrue(collection.validate(rows, [], [], DATE)['ready'])
        self.assertFalse(collection.validate(rows[:29], [], [], DATE)['ready'])
        for key in (*collection.STRINGS, 'rain_ok', 'baby_ok'):
            with self.subTest(key=key):
                broken = copy.deepcopy(rows)
                del broken[0][key]
                report = collection.validate(broken, [], [], DATE)
                self.assertFalse(report['ready'])
                self.assertEqual(len(report['accepted']), 29)
                self.assertIn(key, report['rejected'][0]['reason'])

    def test_duplicate_and_malformed(self):
        original = candidate()
        for url in ['https://EXAMPLE.test/event/0?other=1#x', 'https://example.test/event/0/']:
            duplicate = candidate(1)
            duplicate['url'] = url
            report = collection.validate([duplicate], [], [original], DATE)
            self.assertIn('公式URLが重複', report['rejected'][0]['reason'])
        self.assertEqual(len(collection.validate([original, original], [], [], DATE)['accepted']), 1)
        for value in [None, [], 'bad']:
            self.assertEqual(len(collection.validate([value], [], [], DATE)['rejected']), 1)
        for key, value in [('rain_ok', 'false'), ('url', 'javascript:alert(1)'),
                           ('source_checked_at', '2026-11-06 JST'), ('url_status', 'blocked'),
                           ('period', '2026年11月12日 1日のみ')]:
            broken = candidate()
            broken[key] = value
            self.assertEqual(len(collection.validate([broken], [], [], DATE)['rejected']), 1)
        with self.assertRaises(ValueError):
            collection.validate({}, [], [], DATE)

    def test_removal_boundaries(self):
        for period, kind, permitted in [
            ('2026年11月12日 1日のみ', 'イベント', True),
            ('2026年11月13日 1日のみ', 'イベント', False),
            ('2026年11月14日 1日のみ', 'イベント', False),
            ('2026年11月1日開業', '常設', False),
            ('2026年11月1日公開', 'イベント', False),
            ('2026年10月1日〜11月12日', '常設', False),
            ('2026年12月31日〜1月1日', 'イベント', False),
        ]:
            with self.subTest(period=period, kind=kind):
                row = {**candidate(), 'period': period, 'kind': kind}
                removal = {key: row[key] for key in ('genre', 'name', 'period', 'url')}
                removal['reason'] = '会期終了'
                report = collection.validate([], [removal], [row], DATE)
                self.assertEqual(len(report['removals']), int(permitted))
                self.assertEqual(len(report['rejected_removals']), int(not permitted))


class MigrationTests(unittest.TestCase):
    def test_rebuild_oracle_idempotence_and_broken_sync(self):
        SCRATCH.mkdir(parents=True, exist_ok=True)
        with tempfile.TemporaryDirectory(prefix='pipeline-test-', dir=SCRATCH) as directory:
            folder = Path(directory)
            first, second = folder / 'first', folder / 'second'
            builder.rebuild(first, UPDATED)
            self.assertEqual(check_sync(first), check_sync(ROOT))
            for name in ('spots.json', 'spots.csv', 'index.html'):
                self.assertEqual((first / name).read_bytes(), (ROOT / name).read_bytes(), 'BASELINE ' + name)
            builder.rebuild(second, UPDATED, source=first)
            for name in ('spots.json', 'spots.csv', 'index.html', 'rain_manual.json'):
                self.assertEqual((first / name).read_bytes(), (second / name).read_bytes(), 'IDEMPOTENT ' + name)
            # 同期検査器へ実際の不一致ファイルを与える。各違反名で失敗することが条件。
            (second / 'spots.csv').write_text('genre,name\nwrong,row\n')
            with self.assertRaisesRegex(AssertionError, '^CSV_SYNC$'):
                check_sync(second)
            shutil.copyfile(first / 'spots.csv', second / 'spots.csv')
            html = (second / 'index.html').read_text()
            (second / 'index.html').write_text(html.replace('var D=[', 'var D=[{"broken":true},', 1))
            with self.assertRaisesRegex(AssertionError, '^HTML_SYNC$'):
                check_sync(second)

    def test_output_boundary(self):
        SCRATCH.mkdir(parents=True, exist_ok=True)
        for output in (ROOT, ROOT / 'pipeline/output'):
            with self.assertRaisesRegex(ValueError, '出力先'):
                builder.rebuild(output, DATE)
        with tempfile.TemporaryDirectory(prefix='pipeline-guard-', dir=SCRATCH) as directory:
            folder = Path(directory)
            (folder / 'unrelated').write_text('keep')
            with self.assertRaisesRegex(ValueError, '用途不明'):
                builder.rebuild(folder, DATE)
            self.assertEqual((folder / 'unrelated').read_text(), 'keep')


if __name__ == '__main__':
    unittest.main()
