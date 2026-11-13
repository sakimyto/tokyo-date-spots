import copy
import datetime as dt
import importlib.util
import json
from pathlib import Path
import subprocess
import unittest

ROOT = Path(__file__).resolve().parents[1]
spec = importlib.util.spec_from_file_location('collection', ROOT / 'pipeline/check_collection.py')
collection = importlib.util.module_from_spec(spec)
spec.loader.exec_module(collection)


def verify(data, baseline, evidence, *, require_minimum=True):
    key = lambda row: (row['genre'], row['name'])
    old, new = {key(row): row for row in baseline}, {key(row): row for row in data}
    date = dt.date.fromisoformat(evidence['date'])
    assert len(new) == len(data), 'UNIQUE'
    assert not any((period := collection.period_bounds(row['period'], row.get('period_note', ''))) and period[1] < date for row in data), 'NO_EXPIRED'
    assert old.keys() - new.keys() == {key(row) for row in evidence['removals']}, 'KEEP'
    corrections = {key(row): row['fields'] for row in evidence.get('corrections', [])}
    assert all({**old[k], **corrections.get(k, {})} == new[k] for k in old.keys() & new.keys()), 'KEEP_FIELDS'
    additions = new.keys() - old.keys()
    confirmed = [row for row in evidence['accepted'] if collection.confirmed_venue(row)]
    valid_names = {row['name'] for row in confirmed if key(row) in additions}
    if require_minimum:
        assert len(valid_names) >= 30, 'NEW30'
    published = evidence['accepted'] + evidence.get('published_unconfirmed', [])
    assert additions == {key(row) for row in published}, 'ADOPTION'
    for candidate in published:
        row = new[key(candidate)]
        assert all(row[k] == value for k, value in candidate.items() if k in row), 'FACTS'
    return len(valid_names), len(old.keys() - new.keys())


def below_minimum(data, accepted):
    remove_count = len(accepted) - 29
    assert remove_count > 0
    removed = {(row['genre'], row['name']) for row in accepted[:remove_count]}
    return [row for row in data if (row['genre'], row['name']) not in removed]


class WeeklyDataTests(unittest.TestCase):
    def test_all_rows_and_detector_controls(self):
        path = sorted((ROOT / 'pipeline').glob('weekly-evidence-????-??-??.json'))[-1]
        evidence = json.loads(path.read_text())
        baseline = json.loads(subprocess.check_output(['git', 'show', evidence['baseline_ref'] + ':spots.json'], cwd=ROOT))
        rows = json.loads((ROOT / 'spots.json').read_text())
        # Only the explicitly recorded correction can bypass the new-week minimum.
        require_minimum = not bool(evidence.get('review_correction'))
        self.assertEqual(verify(rows, baseline, evidence, require_minimum=require_minimum),
                         (len(evidence['accepted']), len(evidence['removals'])))
        self.assertEqual(evidence.get('valid_additions', len(evidence['accepted'])), len(evidence['accepted']))
        unconfirmed = evidence.get('published_unconfirmed', [])
        report = collection.validate(evidence['accepted'] + unconfirmed,
                                     evidence['removals'], baseline, dt.date.fromisoformat(evidence['date']))
        self.assertEqual(len(report['accepted']), len(evidence['accepted']))
        self.assertEqual(len(report['rejected']), len(unconfirmed))
        self.assertEqual(report['ready'], len(evidence['accepted']) >= 30)
        if len(evidence['accepted']) < 30:
            with self.assertRaisesRegex(AssertionError, '^NEW30$'):
                verify(rows, baseline, evidence)
        else:
            verify(rows, baseline, evidence)
        for row in rows:
            if row['name'] == 'ちいかわクリスマスマーケット':
                self.assertNotRegex(json.dumps(row, ensure_ascii=False), '⚠|10/25|10/30|先行抽選')
        names = {row['name'] for row in evidence['removals']}
        for source in list((ROOT / 'pipeline').glob('batch*.py')) + [ROOT / 'pipeline' / name for name in (
            'collab_events.py', 'baby_spots.py', 'buffet_spots.py', 'miniature_spots.py', 'data2.txt')]:
            self.assertFalse(any(name in source.read_text() for name in names), source.name)
        variants = [('NO_EXPIRED', rows + [next(row for row in baseline if row['name'] in names)]),
                    ('KEEP', rows[1:])]
        changed = copy.deepcopy(rows)
        changed[0]['desc'] += ' broken'
        variants.append(('KEEP_FIELDS', changed))
        for label, broken in variants:
            with self.subTest(label=label), self.assertRaisesRegex(AssertionError, '^' + label + '$'):
                verify(broken, baseline, evidence, require_minimum=False)

    def test_new30_for_variable_adoption_counts(self):
        from test_pipeline import candidate
        baseline = [{**candidate(100), 'name': '既存'}]
        for count in (30, 31, 32, 36):
            accepted = [candidate(index) for index in range(count)]
            evidence = {'date': '2026-11-13', 'accepted': accepted, 'removals': []}
            rows = baseline + accepted
            with self.subTest(count=count):
                self.assertEqual(verify(rows, baseline, evidence), (count, 0))
                broken = below_minimum(rows, accepted)
                self.assertEqual(len(broken) - len(baseline), 29)
                with self.assertRaisesRegex(AssertionError, '^NEW30$'):
                    verify(broken, baseline, evidence)


if __name__ == '__main__':
    unittest.main()
