#!/usr/bin/env python3
"""Mac launchd用。1週につき収集→実装→別セッション確認→通常公開を1回実行する。"""
import argparse
import datetime as dt
import fcntl
import hashlib
import importlib.util
import json
import os
from pathlib import Path
import shutil
import signal
import subprocess
import sys
import unicodedata
import urllib.request
from zoneinfo import ZoneInfo

JST = ZoneInfo('Asia/Tokyo')
FIRST = dt.date(2026, 11, 20)
DEFAULT = Path.home() / '.codex/automation-state/tokyo-date-spots-weekly'
FIELDS = ('genre', 'name', 'area', 'desc', 'url', 'period', 'venue', 'reservation',
          'kind', 'period_note', 'url_status', 'url_note', 'source_checked_at', 'source_evidence')


def object_schema(properties):
    return {'type': 'object', 'properties': properties, 'required': list(properties), 'additionalProperties': False}


STRING = {'type': 'string'}
BOOL = {'type': 'boolean'}
COLLECT_SCHEMA = object_schema({
    'additions': {'type': 'array', 'items': object_schema({**{key: STRING for key in FIELDS}, 'rain_ok': BOOL, 'baby_ok': BOOL})},
    'removals': {'type': 'array', 'items': object_schema({key: STRING for key in ('genre', 'name', 'period', 'url', 'reason')})},
    'notes': STRING,
})
IMPLEMENT_SCHEMA = object_schema({key: STRING for key in ('status', 'summary', 'tokyo_head', 'site_head', 'site_worktree')})
REVIEW_SCHEMA = object_schema({'approved': BOOL, 'findings': {'type': 'array', 'items': STRING}, 'tokyo_head': STRING, 'site_head': STRING})
PUBLISH_SCHEMA = object_schema({**{key: STRING for key in ('status', 'summary', 'tokyo_pr', 'site_pr', 'tokyo_commit', 'site_commit')},
                                'pages_match': BOOL, 'site_match': BOOL})


def save(path, value):
    temporary = path.with_suffix(path.suffix + '.new')
    temporary.write_text(json.dumps(value, ensure_ascii=False, indent=2) + '\n')
    temporary.replace(path)


def command(args, cwd, prompt=None, timeout=120, env=None):
    # その呼び出しが作ったprocess groupだけをtimeout時に閉じる。他作業へ触れない。
    with subprocess.Popen(args, cwd=cwd, stdin=subprocess.PIPE if prompt is not None else subprocess.DEVNULL,
                          stdout=subprocess.PIPE, stderr=subprocess.DEVNULL, text=True, start_new_session=True, env=env) as process:
        try:
            output, _ = process.communicate(prompt, timeout=timeout)
        except subprocess.TimeoutExpired:
            os.killpg(process.pid, signal.SIGTERM)
            try:
                process.communicate(timeout=15)
            except subprocess.TimeoutExpired:
                os.killpg(process.pid, signal.SIGKILL)
                process.communicate()
            raise RuntimeError('CLIがtimeout。適用結果は再照合が必要') from None
        if process.returncode:
            raise RuntimeError(f'CLI exit={process.returncode}。認証・検査・権限の確認が必要')
        if len(output) > 4 * 1024 * 1024:
            raise RuntimeError('CLI出力が上限を超えた')
        return output.strip()


def head(path):
    return command(['git', 'rev-parse', 'HEAD'], path)


def clean(path):
    return not command(['git', 'status', '--porcelain'], path)


def verify_public(worktree):
    expected = json.loads((worktree / 'spots.json').read_text())
    with urllib.request.urlopen('https://sakimyto.github.io/tokyo-date-spots/', timeout=45) as response:
        if response.status != 200:
            raise RuntimeError('Pages HTMLがHTTP 200ではない')
    with urllib.request.urlopen('https://sakimyto.github.io/tokyo-date-spots/spots.json', timeout=45) as response:
        if json.load(response) != expected:
            raise RuntimeError('公開JSONがローカルと一致しない')
    with urllib.request.urlopen('https://sakimyto.com/lab/odekake', timeout=45) as response:
        if response.status != 200:
            raise RuntimeError('本体ページがHTTP 200ではない')
    actual = []
    page = 1
    while True:
        url = f'https://sakimyto.com/lab/odekake/spots?mode=any&feed=all&ended=1&page={page}'
        with urllib.request.urlopen(url, timeout=45) as response:
            result = json.load(response)
        if result.get('total') != len(expected) or result.get('page') != page or not 1 <= result.get('pageCount', 0) <= len(expected):
            raise RuntimeError('本体APIの件数・ページが不正')
        actual.extend(result['items'])
        if page == result['pageCount']:
            break
        page += 1
    source = {(row['genre'], row['name']): row for row in expected}
    if len(actual) != len(expected) or len({(row['genre'], row['name']) for row in actual}) != len(expected):
        raise RuntimeError('本体APIの行集合が一致しない')
    mapping = {'name': 'name', 'genre': 'genre', 'area': 'area', 'desc': 'desc', 'period': 'period',
               'periodNote': 'period_note', 'venue': 'venue', 'reservation': 'reservation',
               'age': 'age', 'baby': 'baby', 'kind': 'kind', 'rainOk': 'rain_ok', 'trending': 'trending'}
    for row in actual:
        original = source.get((row['genre'], row['name']))
        if not original or any(row.get(api) != original[key] for api, key in mapping.items()):
            raise RuntimeError('本体APIの公開フィールドが一致しない')
        value = 0xcbf29ce484222325
        for byte in unicodedata.normalize('NFC', original['genre']).encode() + b'\0' + unicodedata.normalize('NFC', original['name']).encode():
            value = ((value ^ byte) * 0x100000001b3) & ((1 << 64) - 1)
        if row.get('id') != f'{value:016x}'[:10]:
            raise RuntimeError('本体APIの安定IDが一致しない')
    return len(expected)


def prepare_worktree(config, date):
    repo = Path(config['repo'])
    worktree = Path.home() / '_pjsc/_wt' / ('tokyo-date-spots-weekly-' + date.strftime('%Y%m%d'))
    branch = 'sakimyto/weekly-' + date.strftime('%Y%m%d')
    if worktree.exists():
        actual = command(['git', 'branch', '--show-current'], worktree)
        if actual != branch or not clean(worktree):
            raise RuntimeError('既存worktreeが別用途またはdirty。自動上書きしない')
        return worktree
    entries = command(['git', 'worktree', 'list', '--porcelain'], repo).splitlines()
    if sum(line.startswith('worktree ') for line in entries) - 1 >= 5:
        raise RuntimeError('追加worktree上限5本に到達')
    command(['git', 'fetch', 'origin', 'main'], repo)
    command(['git', 'worktree', 'add', '-b', branch, str(worktree), 'origin/main'], repo)
    return worktree


def prompt(root, phase, values):
    text = (root / 'prompts' / (phase + '.md')).read_text()
    for key, value in values.items():
        text = text.replace('{{' + key + '}}', str(value))
    if '{{' in text:
        raise RuntimeError('promptの入力が不足')
    return text


def collect(config, worktree, scratch, text):
    tools = 'Read,Glob,Grep,WebSearch,WebFetch'
    output = command([config['claude'], '--print', '--model', 'claude-fable-5-2',
                      '--tools', tools, '--allowedTools', tools, '--permission-mode', 'dontAsk',
                      '--strict-mcp-config', '--mcp-config', '{"mcpServers":{}}',
                      '--output-format', 'json', '--json-schema', json.dumps(COLLECT_SCHEMA)],
                     worktree, text, timeout=3600)
    result = json.loads(output)
    models = list(result.get('modelUsage', {}))
    usage = result.get('modelUsage', {}).get('claude-fable-5-2', {})
    if (result.get('is_error') or models != ['claude-fable-5-2']
            or usage.get('canonicalModel') != 'claude-fable-5-2' or not isinstance(usage.get('outputTokens'), int)
            or usage['outputTokens'] <= 0):
        raise RuntimeError('Claudeの実モデルが指定と一致しない、または収集失敗')
    packet = result.get('structured_output')
    if not isinstance(packet, dict) or set(packet) != {'additions', 'removals', 'notes'} or not isinstance(packet['notes'], str):
        raise RuntimeError('収集の構造化出力が不正')
    folder = scratch / 'collect'
    folder.mkdir(exist_ok=True)
    save(folder / 'COLLECTED.json', packet['additions'])
    save(folder / 'REMOVE.json', packet['removals'])
    (folder / 'NOTES.md').write_text(packet['notes'] + '\n')
    (folder / 'MODEL.txt').write_text(models[0] + '\n')
    return packet


def codex(config, root, phase, worktree, scratch, values, schema):
    schema_path = scratch / (phase + '-schema.json')
    response_path = scratch / (phase + '-response.json')
    save(schema_path, schema)
    # 実装委任は導入済みの共有runnerを使う。モデル・reasoning・hookは変更しない。
    task_id = 'tokyo-weekly-' + values['date'] + '-' + phase + '-' + str(values['attempt'])
    out = scratch / task_id
    input_path = scratch / (phase + '-prompt.md')
    input_path.write_text(prompt(root, phase, values))
    args = [config['node'], config['delegate'], '--tool', 'codex', '--worktree', str(worktree),
            '--task-id', task_id, '--prompt-file', str(input_path), '--out-dir', str(out),
            '--sandbox', 'read-only' if phase == 'review' else 'danger-full-access', '--timeout', '3600']
    if phase != 'review':
        args += ['--allow-network', '--exception-reason', '本人指定のMac週次更新・通常公開',
                 '--exception-scope', 'tokyo-date-spotsとsakimytocomの週次データ・既存公開手順',
                 '--exception-expires', dt.datetime.now(JST).date().isoformat(), '--exception-approver', 'owner',
                 '--exception-approved-at', '2026-11-13']
    environment = {**os.environ, 'CURUMI_CODEX_BIN': str(root / 'codex-entry.py'),
                   'TOKYO_WEEKLY_CODEX_REAL': config['codex'], 'TOKYO_WEEKLY_SCHEMA': str(schema_path),
                   'TOKYO_WEEKLY_RESPONSE': str(response_path)}
    try:
        command(args, worktree, timeout=3630, env=environment)
        receipt = json.loads((out / 'result.json').read_text())
        if receipt.get('exit_code') != 0 or not receipt.get('ended_at'):
            raise RuntimeError('共有runnerの正常終了を確認できない')
        result = json.loads(response_path.read_text())
        if set(result) != set(schema['properties']):
            raise RuntimeError('Codexの出力契約が不正')
        for key, prop in schema['properties'].items():
            if prop['type'] == 'string' and not isinstance(result[key], str):
                raise RuntimeError('Codexの文字列フィールドが不正')
            if prop['type'] == 'boolean' and type(result[key]) is not bool:
                raise RuntimeError('Codexの真偽フィールドが不正')
        return result
    finally:
        schema_path.unlink(missing_ok=True)
        response_path.unlink(missing_ok=True)
        input_path.unlink(missing_ok=True)
        for name in ('run.log', 'PROMPT.md', 'STATUS.md'):
            (out / name).unlink(missing_ok=True)


def validate_heads(worktree, result):
    site = Path(result['site_worktree']).resolve()
    allowed = Path.home() / '_pjsc/_wt'
    expected_site = 'sakimytocom-odekake-weekly-' + worktree.name.removeprefix('tokyo-date-spots-weekly-')
    if site.parent != allowed or site.name != expected_site:
        raise RuntimeError('サイトworktreeの境界違反')
    if head(worktree) != result['tokyo_head'] or head(site) != result['site_head'] or not clean(worktree) or not clean(site):
        raise RuntimeError('実装commitが不一致、または未commitの変更がある')


def tick(root, config, date, resume=False):
    state_path = root / 'state.json'
    state = json.loads(state_path.read_text()) if state_path.exists() else {'runs': {}, 'last_seen': None, 'last_fired_digest': None}
    key = date.isoformat()
    previous = state['runs'].get(key)
    if previous and previous['status'] in ('published', 'no-change'):
        return 'duplicate'
    if resume and not previous:
        raise RuntimeError('再開対象の週のstateがない。新しい実行として開始しない')
    if (root / 'STOP').exists():
        return 'stopped'
    unsettled = {day: run for day, run in state['runs'].items() if run['status'] not in ('published', 'no-change')}
    if unsettled and (not resume or set(unsettled) != {key}):
        raise RuntimeError('未完了の週がある。receipt照合後に--resumeで再開する')
    scratch = Path(config.get('scratch_root', Path.home() / '_pjsc/_work')) / ('date-spots-weekly-' + date.strftime('%Y%m%d'))
    scratch.mkdir(parents=True, exist_ok=True)
    run = previous or {'status': 'pending', 'phase': 'prepare', 'attempts': 0}
    run['attempts'] += 1
    state['runs'][key] = run
    def phase(name):
        if (root / 'STOP').exists():
            raise RuntimeError('停止ファイルを確認。次の工程へ進まない')
        run.update(status='pending', phase=name, updated_at=dt.datetime.now(JST).isoformat())
        save(state_path, state)
    try:
        if resume and run['phase'] == 'publish':
            raise RuntimeError('公開の適用結果不明。PR/CI/本番のreceiptを親担当が確定するまで再送しない')
        phase('prepare')
        worktree = prepare_worktree(config, date)
        values = {'date': key, 'worktree': worktree, 'scratch': scratch,
                  'attempt': run['attempts'],
                  'site_worktree': Path.home() / '_pjsc/_wt' / ('sakimytocom-odekake-weekly-' + date.strftime('%Y%m%d'))}
        if not previous or 'collection' not in run:
            phase('collect')
            before = head(worktree)
            packet = collect(config, worktree, scratch, prompt(root, 'collect', values))
            if head(worktree) != before or not clean(worktree):
                raise RuntimeError('収集工程でrepositoryが変更された')
            spec = importlib.util.spec_from_file_location('check_collection', worktree / 'pipeline/check_collection.py')
            module = importlib.util.module_from_spec(spec)
            spec.loader.exec_module(module)
            report = module.validate(packet['additions'], packet['removals'], json.loads((worktree / 'spots.json').read_text()), date)
            save(scratch / 'collection-check.json', report)
            if not packet['additions'] and not packet['removals']:
                run.update(status='no-change', phase='done')
                state['last_seen'] = key
                save(state_path, state)
                (root / 'RESULT.md').write_text('変更なし\n')
                return 'no-change'
            if not report['ready']:
                raise RuntimeError(f'入力検査未通過（有効追加{len(report["accepted"])}件）。適用・pushしない')
            run['collection'] = {'accepted': len(report['accepted']), 'removals': len(report['removals'])}
        if 'implementation' not in run:
            phase('implement')
            implementation = codex(config, root, 'implement', worktree, scratch, values, IMPLEMENT_SCHEMA)
            if implementation['status'] != 'ready':
                raise RuntimeError('実装・品質ゲートが未完了。公開しない')
            validate_heads(worktree, implementation)
            run['implementation'] = implementation
        implementation = run['implementation']
        values.update(implementation)
        validate_heads(worktree, implementation)
        if 'review' not in run:
            phase('review')
            review = codex(config, root, 'review', worktree, scratch, values, REVIEW_SCHEMA)
            if review['approved'] is not True or review['findings'] != [] or any(review[k] != implementation[k] for k in ('tokyo_head', 'site_head')):
                raise RuntimeError('独立確認が未承認、または対象HEAD不一致。公開しない')
            run['review'] = review
        validate_heads(worktree, implementation)
        phase('publish')
        result = codex(config, root, 'publish', worktree, scratch, values, PUBLISH_SCHEMA)
        run['receipt'] = result
        save(state_path, state)
        if result['status'] != 'published' or result['pages_match'] is not True or result['site_match'] is not True:
            raise RuntimeError('公開結果を全て確認できなかった。receipt照合が必要')
        run['verified_rows'] = verify_public(worktree)
        run.update(status='published', phase='done', receipt=result)
        state['last_seen'] = key
        state['last_fired_digest'] = hashlib.sha256((implementation['tokyo_head'] + implementation['site_head']).encode()).hexdigest()
        save(state_path, state)
        (root / 'RESULT.md').write_text(f'{key}：{result["summary"]}\n\n東京：{result["tokyo_pr"]}\nサイト：{result["site_pr"]}\n')
        return 'published'
    except Exception as error:
        run.update(status='needs-reconciliation', reason=str(error), updated_at=dt.datetime.now(JST).isoformat())
        save(state_path, state)
        (root / 'RESULT.md').write_text(f'{key}：未完了（{run["phase"]}）\n\n理由：{error}\n作業場所：{scratch}\n適用結果を照合してから再開する。\n')
        raise


def main():
    parser = argparse.ArgumentParser(description=__doc__)
    parser.add_argument('--state-dir', type=Path, default=DEFAULT)
    parser.add_argument('--dry-run', action='store_true')
    parser.add_argument('--resume', type=dt.date.fromisoformat)
    args = parser.parse_args()
    now = dt.datetime.now(JST)
    if args.dry_run:
        print(json.dumps({'label': 'com.sakimyto.tokyo-date-spots-weekly', 'first': '2026-11-20T09:05:00+09:00',
                          'run_at_load': False, 'state': str(args.state_dir)}, ensure_ascii=False))
        return 0
    if not args.resume and (now.date() < FIRST or now.weekday() != 4 or now.time() < dt.time(9, 5)):
        return 0
    root = args.state_dir.resolve()
    root.mkdir(parents=True, exist_ok=True)
    with (root / 'run.lock').open('a+') as lock:
        try:
            fcntl.flock(lock, fcntl.LOCK_EX | fcntl.LOCK_NB)
        except BlockingIOError:
            return 0
        config = json.loads((root / 'config.json').read_text())
        tick(root, config, args.resume or now.date(), bool(args.resume))
    return 0


if __name__ == '__main__':
    try:
        raise SystemExit(main())
    except Exception:
        # 生のCLI出力やpromptをlaunchdログへ流さない。詳細は短いRESULTとstateにある。
        print('weekly: stopped; inspect RESULT.md and state.json', file=sys.stderr)
        raise SystemExit(1)
