import datetime as dt
import fcntl
import importlib.util
import io
import json
from pathlib import Path
import shutil
import tempfile
import unittest
from unittest.mock import patch

ROOT = Path(__file__).resolve().parents[1]
SCRATCH = Path.home() / '_pjsc/_work/date-spots-migrate-1113'
spec = importlib.util.spec_from_file_location('weekly', ROOT / 'automation/weekly.py')
weekly = importlib.util.module_from_spec(spec)
spec.loader.exec_module(weekly)
spec = importlib.util.spec_from_file_location('install', ROOT / 'automation/install.py')
install = importlib.util.module_from_spec(spec)
spec.loader.exec_module(install)
DATE = dt.date(2026, 11, 20)


class AutomationTests(unittest.TestCase):
    def setUp(self):
        SCRATCH.mkdir(parents=True, exist_ok=True)
        self.directory = tempfile.TemporaryDirectory(prefix='automation-test-', dir=SCRATCH)
        self.root = Path(self.directory.name)
        self.config = {'scratch_root': str(self.root / 'scratch')}
        shutil.copytree(ROOT / 'automation/prompts', self.root / 'prompts')
        self.prepare = patch.object(weekly, 'prepare_worktree', return_value=ROOT).start()
        self.head = patch.object(weekly, 'head', return_value='test-head').start()
        self.clean = patch.object(weekly, 'clean', return_value=True).start()
        self.addCleanup(patch.stopall)
        self.addCleanup(self.directory.cleanup)

    def valid_packet(self):
        def row(index):
            return dict(genre='test', name=f'candidate-{index}', area='東京', desc='検査',
                url=f'https://example.test/{index}', period='2026年11月20日〜21日', venue='東京',
                reservation='', kind='イベント', period_note='', url_status='ok', url_note='',
                source_checked_at='2026-11-20 JST', source_evidence='会期・会場', rain_ok=True, baby_ok=False)
        return {'additions': [row(index) for index in range(30)], 'removals': [], 'notes': 'test'}

    def test_no_change_and_duplicate_no_model_work(self):
        with (patch.object(weekly, 'collect', return_value={'additions': [], 'removals': [], 'notes': ''}) as collect,
              patch.object(weekly, 'codex') as codex):
            self.assertEqual(weekly.tick(self.root, self.config, DATE), 'no-change')
            self.assertEqual((self.root / 'RESULT.md').read_text(), '変更なし\n')
            self.assertEqual(weekly.tick(self.root, self.config, DATE), 'duplicate')
            self.assertEqual(collect.call_count, 1)
            codex.assert_not_called()

    def test_stop_and_duplicate_lock(self):
        (self.root / 'STOP').touch()
        with patch.object(weekly, 'collect') as collect:
            self.assertEqual(weekly.tick(self.root, self.config, DATE), 'stopped')
            collect.assert_not_called()
        with (self.root / 'run.lock').open('a+') as lock:
            fcntl.flock(lock, fcntl.LOCK_EX | fcntl.LOCK_NB)
            with patch('sys.argv', ['weekly.py', '--state-dir', str(self.root), '--resume', DATE.isoformat()]):
                self.assertEqual(weekly.main(), 0)

    def test_short_input_and_auth_failure_stop_before_implementation(self):
        packet = self.valid_packet()
        packet['additions'].pop()
        with patch.object(weekly, 'collect', return_value=packet), patch.object(weekly, 'codex') as codex:
            with self.assertRaisesRegex(RuntimeError, '有効追加29件'):
                weekly.tick(self.root, self.config, DATE)
            codex.assert_not_called()
        state = json.loads((self.root / 'state.json').read_text())
        self.assertEqual(state['runs'][DATE.isoformat()]['status'], 'needs-reconciliation')
        with patch.object(weekly, 'collect', side_effect=RuntimeError('認証不足')), patch.object(weekly, 'codex') as codex:
            with self.assertRaisesRegex(RuntimeError, '認証不足'):
                weekly.tick(self.root, self.config, DATE, resume=True)
            codex.assert_not_called()

    def test_model_mismatch_is_not_zero_candidates(self):
        output = json.dumps({'modelUsage': {'wrong-model': {}}, 'structured_output': self.valid_packet()})
        with patch.object(weekly, 'command', return_value=output):
            with self.assertRaisesRegex(RuntimeError, '実モデル'):
                weekly.collect({'claude': 'fake'}, ROOT, self.root, 'test')
        self.assertFalse((self.root / 'collect/COLLECTED.json').exists())

    def test_unapproved_review_cannot_publish(self):
        implementation = dict(status='ready', summary='test', tokyo_head='t', site_head='s', site_worktree='test')
        review = dict(approved=False, findings=['failure'], tokyo_head='t', site_head='s')
        with (patch.object(weekly, 'collect', return_value=self.valid_packet()),
              patch.object(weekly, 'validate_heads'),
              patch.object(weekly, 'codex', side_effect=[implementation, review]) as codex):
            with self.assertRaisesRegex(RuntimeError, '独立確認'):
                weekly.tick(self.root, self.config, DATE)
            self.assertEqual(codex.call_count, 2)
        state = json.loads((self.root / 'state.json').read_text())
        self.assertEqual(state['runs'][DATE.isoformat()]['phase'], 'review')

    def test_publish_unknown_is_not_retried_on_resume(self):
        weekly.save(self.root / 'state.json', {'runs': {DATE.isoformat(): {'status': 'pending', 'phase': 'publish', 'attempts': 1}}})
        with patch.object(weekly, 'collect') as collect, patch.object(weekly, 'codex') as codex:
            with self.assertRaisesRegex(RuntimeError, '公開の適用結果不明'):
                weekly.tick(self.root, self.config, DATE, resume=True)
            collect.assert_not_called()
            codex.assert_not_called()
        state = json.loads((self.root / 'state.json').read_text())
        self.assertEqual(state['runs'][DATE.isoformat()]['attempts'], 2)
        self.assertEqual(state['runs'][DATE.isoformat()]['status'], 'needs-reconciliation')

    def test_plist_does_not_run_on_load(self):
        value = install.definition('/verified/python3', self.root)
        self.assertEqual(value['Label'], 'com.sakimyto.tokyo-date-spots-weekly')
        self.assertEqual(value['StartCalendarInterval'], {'Weekday': 5, 'Hour': 9, 'Minute': 5})
        self.assertIs(value['RunAtLoad'], False)
        self.assertEqual(value['EnvironmentVariables']['TZ'], 'Asia/Tokyo')

    def test_publication_uses_real_fields_and_detects_a_wrong_saved_id(self):
        row = {**self.valid_packet()['additions'][0], 'genre': '季節イベント',
               'name': '東京クリスマスマーケット2026', 'age': '', 'baby': '', 'trending': False}
        (self.root / 'spots.json').write_text(json.dumps([row]))
        mapping = {'name': 'name', 'genre': 'genre', 'area': 'area', 'desc': 'desc', 'period': 'period',
                   'periodNote': 'period_note', 'venue': 'venue', 'reservation': 'reservation',
                   'age': 'age', 'baby': 'baby', 'kind': 'kind', 'rainOk': 'rain_ok', 'trending': 'trending'}
        item = {api: row[key] for api, key in mapping.items()}
        item['id'] = 'd4b2c29eb5'
        class Response(io.BytesIO):
            status = 200
        def response(url, timeout):
            value = [row] if url.endswith('/spots.json') else {
                'total': 1, 'page': 1, 'pageCount': 1, 'items': [item]}
            return Response(json.dumps(value).encode())
        with patch.object(weekly.urllib.request, 'urlopen', side_effect=response):
            self.assertEqual(weekly.verify_public(self.root), 1)
            item['id'] = '0000000000'
            with self.assertRaisesRegex(RuntimeError, '安定ID'):
                weekly.verify_public(self.root)


if __name__ == '__main__':
    unittest.main()
