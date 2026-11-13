"""終了確定した名前を、mergeが読むソースから取り除く。"""
import ast
from pathlib import Path


def prune_python(text, names):
    raw = text.encode('utf-8')
    lines = raw.splitlines(keepends=True)
    offsets = [0]
    for line in lines:
        offsets.append(offsets[-1] + len(line))
    def span(node):
        return offsets[node.lineno - 1] + node.col_offset, offsets[node.end_lineno - 1] + node.end_col_offset
    edits = []
    def erase(start, end):
        cursor = end
        while cursor < len(raw) and raw[cursor:cursor+1] in (b' ', b'\t', b'\r', b'\n'):
            cursor += 1
        if raw[cursor:cursor+1] == b',':
            end = cursor + 1
        edits.append((start, end, b''))
    def name_of(node):
        if isinstance(node, ast.Call):
            for keyword in node.keywords:
                if keyword.arg == 'name' and isinstance(keyword.value, ast.Constant):
                    return keyword.value.value
        if isinstance(node, ast.Call) and isinstance(node.func, ast.Name) and node.func.id == 'R' and len(node.args) >= 2:
            return node.args[1].value if isinstance(node.args[1], ast.Constant) else None
        if isinstance(node, ast.Dict):
            for key, value in zip(node.keys, node.values):
                if isinstance(key, ast.Constant) and key.value == 'name' and isinstance(value, ast.Constant):
                    return value.value
        return None
    tree = ast.parse(text)
    for node in ast.walk(tree):
        if isinstance(node, ast.Expr) and isinstance(node.value, ast.Call):
            call = node.value
            if isinstance(call.func, ast.Attribute) and call.func.attr == 'append' and call.args and name_of(call.args[0]) in names:
                start, end = span(node)
                edits.append((start, end, b''))
        if isinstance(node, ast.List):
            for item in node.elts:
                if name_of(item) in names:
                    erase(*span(item))
        if isinstance(node, ast.Dict):
            for key, value in zip(node.keys, node.values):
                if isinstance(key, ast.Constant) and key.value in names:
                    erase(span(key)[0], span(value)[1])
        if isinstance(node, ast.Assign) and any(isinstance(target, ast.Name) and target.id == 'ROWS' for target in node.targets):
            value = node.value
            if isinstance(value, ast.Constant) and isinstance(value.value, str):
                kept = ''.join(line for line in value.value.splitlines(keepends=True)
                               if not names.intersection(line.strip().split('|')))
                if kept != value.value:
                    start, end = span(value)
                    edits.append((start, end, ('r"""' + kept + '"""').encode('utf-8')))
    # 外側の行削除に含まれた内側の編集は重ねない。
    outer = []
    for edit in sorted(set(edits), key=lambda item: (item[0], -item[1])):
        if not any(start <= edit[0] and edit[1] <= end for start, end, _ in outer):
            outer.append(edit)
    for start, end, replacement in reversed(outer):
        raw = raw[:start] + replacement + raw[end:]
    result = raw.decode('utf-8')
    ast.parse(result)
    return result


def prune(folder, names):
    paths = list(folder.glob('batch*.py')) + [folder / name for name in (
        'collab_events.py', 'buffet_spots.py', 'miniature_spots.py', 'baby_spots.py')]
    changed = []
    for path in paths:
        before = path.read_text()
        after = prune_python(before, names)
        if after != before:
            path.write_text(after)
            changed.append(path.name)
    path = folder / 'data2.txt'
    before = path.read_text()
    after = ''.join(line for line in before.splitlines(keepends=True)
                    if not names.intersection(line.strip().split('|')))
    if after != before:
        path.write_text(after)
        changed.append(path.name)
    return changed
