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


def verify(data, baseline, evidence):
    key = lambda row: (row['genre'], row['name'])
    old, new = {key(row): row for row in baseline}, {key(row): row for row in data}
    date = dt.date.fromisoformat(evidence['date'])
    assert len(new) == len(data), 'UNIQUE'
    assert not any((period := collection.period_bounds(row['period'])) and period[1] < date for row in data), 'NO_EXPIRED'
    assert old.keys() - new.keys() == {key(row) for row in evidence['removals']}, 'KEEP'
    assert all(old[k] == new[k] for k in old.keys() & new.keys()), 'KEEP_FIELDS'
    additions = new.keys() - old.keys()
    assert len({name for genre, name in additions}) >= 30, 'NEW30'
    assert additions == {key(row) for row in evidence['accepted']}, 'ADOPTION'
    for candidate in evidence['accepted']:
        row = new[key(candidate)]
        assert all(row[k] == value for k, value in candidate.items() if k in row), 'FACTS'
    return len(additions), len(old.keys() - new.keys())


class WeeklyDataTests(unittest.TestCase):
    def test_all_rows_and_detector_controls(self):
        path = sorted((ROOT / 'pipeline').glob('weekly-evidence-????-??-??.json'))[-1]
        evidence = json.loads(path.read_text())
        baseline = json.loads(subprocess.check_output(['git', 'show', evidence['baseline_ref'] + ':spots.json'], cwd=ROOT))
        rows = json.loads((ROOT / 'spots.json').read_text())
        self.assertEqual(verify(rows, baseline, evidence), (len(evidence['accepted']), len(evidence['removals'])))
        names = {row['name'] for row in evidence['removals']}
        for source in list((ROOT / 'pipeline').glob('batch*.py')) + [ROOT / 'pipeline' / name for name in (
            'collab_events.py', 'baby_spots.py', 'buffet_spots.py', 'miniature_spots.py', 'data2.txt')]:
            self.assertFalse(any(name in source.read_text() for name in names), source.name)
        variants = [('NO_EXPIRED', rows + [next(row for row in baseline if row['name'] in names)]),
                    ('KEEP', rows[1:])]
        added_names = {row['name'] for row in evidence['accepted'][:2]}
        variants.append(('NEW30', [row for row in rows if row['name'] not in added_names]))
        changed = copy.deepcopy(rows)
        changed[0]['desc'] += ' broken'
        variants.append(('KEEP_FIELDS', changed))
        for label, broken in variants:
            with self.subTest(label=label), self.assertRaisesRegex(AssertionError, '^' + label + '$'):
                verify(broken, baseline, evidence)


if __name__ == '__main__':
    unittest.main()
