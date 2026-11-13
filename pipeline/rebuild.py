"""採用済みの公開JSONを入力として、専用の出力先で再構築する。"""
import argparse
import datetime as dt
import json
from pathlib import Path
import shutil
import subprocess
import sys

ROOT = Path(__file__).resolve().parents[1]
PIPELINE = ROOT / 'pipeline'
STEPS = ('merge_collab.py', 'merge_buffet.py', 'merge_miniature.py',
         'merge_baby.py', 'merge_batch2.py', 'apply_rain.py')


def rebuild(output, date, source=ROOT):
    output, source = Path(output).resolve(), Path(source).resolve()
    if output == ROOT or ROOT in output.parents or output == source or source in output.parents:
        raise ValueError('出力先はrepositoryと入力元の外にしてください')
    marker = output / '.date-spots-rebuild'
    if output.exists() and any(output.iterdir()) and not marker.is_file():
        raise ValueError('既存の用途不明な出力先を上書きしません')
    output.mkdir(parents=True, exist_ok=True)
    marker.write_text('pipeline/rebuild.py\n', encoding='utf-8')
    # 依存・キャッシュ・ログをコピーせず、再構築に必要な直下のソースだけ置く。
    for path in PIPELINE.iterdir():
        if path.suffix in ('.py', '.json') and path.name != 'rebuild.py':
            shutil.copyfile(path, output / path.name)
    for name in ('spots.json', 'tpl.html', 'build.py'):
        shutil.copyfile(source / name, output / name)
    for name in STEPS:
        subprocess.run([sys.executable, '-B', name], cwd=output, check=True)
    subprocess.run([sys.executable, '-B', 'build.py', date.isoformat()], cwd=output, check=True)
    subprocess.run([sys.executable, '-B', 'sync_csv.py'], cwd=output, check=True)
    rows = json.loads((output / 'spots.json').read_text(encoding='utf-8'))
    print(f'rebuilt: {len(rows)} rows in {output}')


def main():
    parser = argparse.ArgumentParser(description=__doc__)
    parser.add_argument('--output', required=True, type=Path)
    parser.add_argument('--date', required=True, type=dt.date.fromisoformat)
    parser.add_argument('--source', type=Path, default=ROOT)
    args = parser.parse_args()
    rebuild(args.output, args.date, args.source)


if __name__ == '__main__':
    main()
