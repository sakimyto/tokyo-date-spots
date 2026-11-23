"""定期処理の正本（ops/automation/manifest.json）と引き継ぎ手順の検査。

repo内のファイルだけを読む。launchdやOrcaの実登録には触れない。
"""
import importlib.util
import json
import os
from pathlib import Path
import re
import unittest

ROOT = Path(__file__).resolve().parents[1]
MANIFEST = Path(os.environ.get('AUTOMATION_MANIFEST', str(ROOT / 'ops/automation/manifest.json')))
REQUIRED = ('id', 'purpose', 'kind', 'schedule', 'source', 'canonical', 'entrypoint', 'runner',
            'inputs', 'outputs', 'statePaths', 'dedup', 'stopConditions', 'stopMethod',
            'humanDecisions', 'ledgerIds', 'handoff')
WEEKDAYS = {0: 'SU', 1: 'MO', 2: 'TU', 3: 'WE', 4: 'TH', 5: 'FR', 6: 'SA'}
spec = importlib.util.spec_from_file_location('install', ROOT / 'automation/install.py')
install = importlib.util.module_from_spec(spec)
spec.loader.exec_module(install)


class Manifest(unittest.TestCase):
    def setUp(self):
        self.text = MANIFEST.read_text(encoding='utf-8')
        self.manifest = json.loads(self.text)
        self.jobs = self.manifest['jobs']

    def test_ids_unique_and_fields_present(self):
        ids = [job['id'] for job in self.jobs]
        self.assertTrue(ids)
        self.assertEqual(len(ids), len(set(ids)))
        for job in self.jobs:
            for key in REQUIRED:
                self.assertIn(key, job, f'{job["id"]}: {key}')
            for key in ('current', 'registration', 'desiredStatus', 'observedStatus', 'lastRunEvidence'):
                self.assertIn(key, job['runner'], f'{job["id"]}: runner.{key}')

    def test_repo_paths_exist(self):
        self.assertTrue((ROOT / self.manifest['handover']).is_file())
        for job in self.jobs:
            for rel in [job['source'], job['entrypoint'], *job['canonical']]:
                self.assertTrue((ROOT / rel).is_file(), f'{job["id"]}: {rel}')

    def test_entry_prompt_is_per_job_and_calls_entrypoint(self):
        for job in self.jobs:
            self.assertEqual(job['source'], f'ops/automation/{job["id"]}.prompt.md')
            prompt = (ROOT / job['source']).read_text(encoding='utf-8')
            self.assertIn(Path(job['entrypoint']).name, prompt)
            # 入口は旧launchdの登録が残っていないかを判定する。実行器を替えてもこのlabelは消えない。
            self.assertIn(install.LABEL, prompt)

    def test_schedule_matches_installed_launchd_definition(self):
        # 時刻は処理の属性で、実行器をOrcaへ替えても同じ時刻を保つ。
        job = next(job for job in self.jobs if job['id'] == 'odekake-weekly')
        calendar = install.definition('/python')['StartCalendarInterval']
        self.assertEqual(job['schedule'], {'kind': 'weekly', 'weekday': WEEKDAYS[calendar['Weekday']],
                                           'hour': calendar['Hour'], 'minute': calendar['Minute']})
        self.assertEqual(self.manifest['timezone'], install.definition('/python')['EnvironmentVariables']['TZ'])

    def test_no_secret_or_account_like_values(self):
        for pattern in (r'hooks\.slack\.com/', r'xox[abpr]-', r'Bearer\s+\S', r'sk-[A-Za-z0-9]{8,}',
                        r'user-[A-Za-z0-9]{16,}', r'ghp_[A-Za-z0-9]{20,}'):
            self.assertIsNone(re.search(pattern, self.text), pattern)


# 引き継ぎ手順の模型。旧=launchd、新=Orca（登録の有効と有効化の印の2つの錠）。
# 状態: (旧の登録, 旧の実行中, 新の登録, 印, 新の実行中, 手順の位置)
STEPS = ('bootout_old', 'wait_old_idle', 'enable_new', 'first_run_done')
ROLLBACK = ('disable_new', 'wait_new_idle', 'bootstrap_old', 'rolled_back')


def successors(state, plan, manual_anytime=False):
    old_loaded, old_running, new_enabled, marker, new_running, pc = state
    result = []
    # 環境の動き: 登録中の旧はいつでも起動しうる。実行中の回はいつでも終わりうる。
    if old_loaded and not old_running:
        result.append((old_loaded, True, new_enabled, marker, new_running, pc))
    if old_running:
        result.append((old_loaded, False, new_enabled, marker, new_running, pc))
    if new_enabled and marker and not new_running:
        result.append((old_loaded, old_running, new_enabled, marker, True, pc))
    if new_running:
        result.append((old_loaded, old_running, new_enabled, marker, False, pc))
    # 手動実行（precheckを迂回する）。手順では旧が止まり、新を有効にした後（S3以降）だけ許す。
    if not new_running and (manual_anytime or (not old_loaded and not old_running and new_enabled and marker)):
        result.append((old_loaded, old_running, new_enabled, marker, True, pc))
    if pc >= len(plan):
        return result
    step = plan[pc]
    nxt = pc + 1
    if step == 'bootout_old':
        result.append((False, old_running, new_enabled, marker, new_running, nxt))
    elif step == 'bootstrap_old':
        result.append((True, old_running, new_enabled, marker, new_running, nxt))
    elif step == 'enable_new':
        result.append((old_loaded, old_running, True, True, new_running, nxt))
    elif step == 'disable_new':
        result.append((old_loaded, old_running, False, False, new_running, nxt))
    elif step == 'wait_old_idle' and not old_running:
        result.append((old_loaded, old_running, new_enabled, marker, new_running, nxt))
    elif step == 'wait_new_idle' and not new_running:
        result.append((old_loaded, old_running, new_enabled, marker, new_running, nxt))
    elif step in ('first_run_done', 'rolled_back', 'skip'):
        result.append((old_loaded, old_running, new_enabled, marker, new_running, nxt))
    return result


def explore(plan, start, manual_anytime=False):
    seen, todo = {start}, [start]
    while todo:
        for following in successors(todo.pop(), plan, manual_anytime):
            if following not in seen:
                seen.add(following)
                todo.append(following)
    return seen


def both_running(states):
    return [state for state in states if state[1] and state[4]]


class HandoffStateMachine(unittest.TestCase):
    # 移行: 旧は登録中、新は無効で作成済み（S1）から始める。
    FORWARD_START = (True, False, False, False, False, 0)
    # 戻し: 新が有効、旧は停止済み（S3）から始める。
    ROLLBACK_START = (False, False, True, True, False, 0)

    def test_documented_plans_never_run_old_and_new_together(self):
        forward = explore(STEPS, self.FORWARD_START)
        rollback = explore(ROLLBACK, self.ROLLBACK_START)
        self.assertEqual(both_running(forward), [])
        self.assertEqual(both_running(rollback), [])
        self.assertTrue(any(state[5] == len(STEPS) for state in forward))
        self.assertTrue(any(state[5] == len(ROLLBACK) for state in rollback))
        # 空振りでないこと: 旧の実行中と新の実行中は、それぞれ別の時点で実際に到達する。
        self.assertTrue(any(state[1] for state in forward) and any(state[4] for state in forward))
        self.assertTrue(any(state[4] for state in rollback))

    def test_broken_variants_are_caught(self):
        variants = {
            '旧を止める前に新を有効化': (('enable_new', 'bootout_old', 'wait_old_idle', 'first_run_done'), self.FORWARD_START, False),
            '旧の実行中0件の確認を省略': (('bootout_old', 'skip', 'enable_new', 'first_run_done'), self.FORWARD_START, False),
            '止める前に実行中0件を確認': (('wait_old_idle', 'bootout_old', 'enable_new', 'first_run_done'), self.FORWARD_START, False),
            '旧が動く間の手動実行': (STEPS, self.FORWARD_START, True),
            '戻しで旧を先に再開': (('bootstrap_old', 'disable_new', 'wait_new_idle', 'rolled_back'), self.ROLLBACK_START, False),
            '戻しで新の実行中0件の確認を省略': (('disable_new', 'skip', 'bootstrap_old', 'rolled_back'), self.ROLLBACK_START, False),
        }
        for name, (plan, start, manual) in variants.items():
            with self.subTest(name):
                self.assertTrue(both_running(explore(plan, start, manual)), name)


if __name__ == '__main__':
    unittest.main()
