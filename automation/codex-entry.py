#!/usr/bin/env python3
"""Read the phase binding after the shared runner reduces the environment."""
import json
import os
from pathlib import Path
import re
import subprocess
import sys

entry = Path(__file__).resolve()
binding = json.loads(entry.with_suffix('.json').read_text())
expected = {'version', 'codex', 'schema', 'response', 'phase', 'worktree', 'head'}
if not isinstance(binding, dict) or set(binding) != expected or type(binding['version']) is not int or binding['version'] != 1:
    raise SystemExit('invalid binding fields')
phase = binding['phase']
if phase not in ('implement', 'review', 'publish') or entry.name != phase + '-entry.py':
    raise SystemExit('phase binding mismatch')
if not isinstance(binding['head'], str) or not re.fullmatch('[0-9a-f]{40}', binding['head']):
    raise SystemExit('invalid worktree HEAD')
paths = {}
for key in ('codex', 'schema', 'response', 'worktree'):
    if not isinstance(binding[key], str) or not Path(binding[key]).is_absolute():
        raise SystemExit('binding paths must be absolute')
    raw = Path(binding[key])
    if key in ('schema', 'response') and (raw.is_symlink() or raw.parent.resolve() != entry.parent):
        raise SystemExit('schema and response must stay inside the phase directory')
    paths[key] = raw.resolve()
if paths['schema'].name != phase + '-schema.json' or paths['response'].name != phase + '-response.json':
    raise SystemExit('phase output names mismatch')
if paths['codex'] == entry or not paths['codex'].is_file() or not paths['schema'].is_file():
    raise SystemExit('missing or recursive phase executable')
actual = subprocess.check_output(['git', 'rev-parse', 'HEAD'], cwd=paths['worktree'], text=True).strip()
if actual != binding['head']:
    raise SystemExit('worktree HEAD changed before invocation')
args = sys.argv[1:]
if args[-1:] != ['-']:
    raise SystemExit('unexpected delegate invocation')
args[-1:] = ['--output-schema', str(paths['schema']), '--output-last-message', str(paths['response']), '-']
os.execv(str(paths['codex']), [str(paths['codex']), *args])
