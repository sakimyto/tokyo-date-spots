#!/usr/bin/env python3
"""共有delegate runnerへ、当該呼び出しのschemaと最終応答先だけを結ぶ。"""
import os
from pathlib import Path
import sys

real = Path(os.environ['TOKYO_WEEKLY_CODEX_REAL']).resolve()
if real == Path(__file__).resolve():
    raise SystemExit('recursive codex entry')
args = sys.argv[1:]
if args[-1:] != ['-']:
    raise SystemExit('unexpected delegate invocation')
args[-1:] = ['--output-schema', os.environ['TOKYO_WEEKLY_SCHEMA'],
             '--output-last-message', os.environ['TOKYO_WEEKLY_RESPONSE'], '-']
os.execv(str(real), [str(real), *args])
