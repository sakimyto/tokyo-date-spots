#!/usr/bin/env python3
"""検証済みの実行コピーとlaunchd定義を配置する。loadは--load指定時のみ。"""
import argparse
import json
import os
from pathlib import Path
import plistlib
import shutil
import subprocess
import sys

LABEL = 'com.sakimyto.tokyo-date-spots-weekly'
SOURCE = Path(__file__).resolve().parent
TARGET = Path.home() / '.codex/automation-state/tokyo-date-spots-weekly'


def definition(python, target=TARGET):
    return {'Label': LABEL, 'ProgramArguments': [python, str(target / 'weekly.py')],
            'WorkingDirectory': str(target), 'RunAtLoad': False,
            'StartCalendarInterval': {'Weekday': 5, 'Hour': 9, 'Minute': 5},
            'StandardOutPath': str(target / 'launchd.out.log'),
            'StandardErrorPath': str(target / 'launchd.err.log'),
            'EnvironmentVariables': {'TZ': 'Asia/Tokyo',
                'TMPDIR': str(Path.home() / '_pjsc/_work/date-spots-automation-tmp'),
                'PATH': ':'.join([str(Path.home() / '.bun/bin'), str(Path.home() / '.local/bin'),
                    str(Path.home() / '.nvm/versions/node/v22.22.0/bin'), '/opt/homebrew/bin', '/usr/bin', '/bin'])}}


def main():
    parser = argparse.ArgumentParser(description=__doc__)
    parser.add_argument('--load', action='store_true')
    args = parser.parse_args()
    TARGET.mkdir(parents=True, exist_ok=True)
    (Path.home() / '_pjsc/_work/date-spots-automation-tmp').mkdir(parents=True, exist_ok=True)
    for name in ('weekly.py', 'codex-entry.py', 'learnings.md'):
        shutil.copyfile(SOURCE / name, TARGET / name)
    (TARGET / 'codex-entry.py').chmod(0o700)
    shutil.copytree(SOURCE / 'prompts', TARGET / 'prompts', dirs_exist_ok=True)
    config = {'repo': str(Path.home() / '_pjsc/tokyo-date-spots'),
              'site_repo': str(Path.home() / '_pjsc/sakimytocom'),
              'node': shutil.which('node') or '/opt/homebrew/bin/node',
              'delegate': str(Path.home() / '.codex/skills/curumi-codex-delegate/scripts/delegate-task.mjs'),
              'claude': shutil.which('claude') or str(Path.home() / '.local/bin/claude'),
              'codex': shutil.which('codex') or str(Path.home() / '.bun/bin/codex')}
    for key in ('claude', 'codex', 'node', 'delegate'):
        if not Path(config[key]).is_file():
            raise RuntimeError(key + ' CLIが見つからない')
    (TARGET / 'config.json').write_text(json.dumps(config, indent=2) + '\n')
    plist = Path.home() / 'Library/LaunchAgents' / (LABEL + '.plist')
    plist.parent.mkdir(parents=True, exist_ok=True)
    expected = definition(sys.executable)
    if plist.exists() and plistlib.loads(plist.read_bytes()) != expected:
        raise RuntimeError('既存の異なるlaunchd定義を上書きしない')
    plist.write_bytes(plistlib.dumps(expected))
    subprocess.run(['plutil', '-lint', str(plist)], check=True)
    if args.load:
        domain = 'gui/' + str(os.getuid())
        present = subprocess.run(['launchctl', 'print', domain + '/' + LABEL], capture_output=True)
        if present.returncode:
            subprocess.run(['launchctl', 'bootstrap', domain, str(plist)], check=True)
        subprocess.run(['launchctl', 'print', domain + '/' + LABEL], check=True)
    print('first scheduled occurrence: 2026-11-20 09:05 JST; RunAtLoad=false')


if __name__ == '__main__':
    main()
