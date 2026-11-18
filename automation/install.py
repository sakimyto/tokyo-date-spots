#!/usr/bin/env python3
"""検証済みの実行コピーとlaunchd定義を配置する。loadは--load指定時のみ。"""
import argparse
import fcntl
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


def install_copy():
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
    config_path = TARGET / 'config.json'
    if config_path.exists():
        existing = json.loads(config_path.read_text())
        if not isinstance(existing, dict):
            raise RuntimeError('既存configが不正。上書きしない')
        config.update(existing)
    for key in ('claude', 'codex', 'node', 'delegate'):
        if not Path(config[key]).is_file():
            raise RuntimeError(key + ' CLIが見つからない')
    config_path.write_text(json.dumps(config, indent=2) + '\n')
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


def main():
    TARGET.mkdir(parents=True, exist_ok=True)
    with (TARGET / 'run.lock').open('a+') as lock:
        try:
            fcntl.flock(lock, fcntl.LOCK_EX | fcntl.LOCK_NB)
        except BlockingIOError:
            raise RuntimeError('週次処理が実行中。配置を変更しない') from None
        state_path = TARGET / 'state.json'
        if state_path.exists():
            state = json.loads(state_path.read_text())
            if not isinstance(state.get('runs'), dict) or any(run.get('status') not in ('published', 'no-change') for run in state['runs'].values()):
                raise RuntimeError('未確定の週次処理がある。配置を変更しない')
        if (TARGET / 'weekly.py').exists() and not (TARGET / 'STOP').exists():
            raise RuntimeError('再配置はSTOPと実行中0を確認してから行う')
        install_copy()


if __name__ == '__main__':
    main()
