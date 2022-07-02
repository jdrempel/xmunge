# Contains helper functions for comparing the contents of two directories

from difflib import Differ
from filecmp import dircmp
from pathlib import Path
from pprint import pprint


def diff_directories(a: str, b: str):
    d = dircmp(a, b)

    if len(d.left_only):
        print(f'Path {a} contains:')
        pprint(d.left_only)

    if len(d.right_only):
        print(f'Path {b} contains:')
        pprint(d.right_only)

    if len(d.diff_files):
        print(f'The following files differ between {a} and {b}:')
        pprint(d.diff_files)
        for file in d.diff_files:
            a_path, b_path = Path(a), Path(b)
            if file.rsplit('.', 1)[0].lower() in ['lvl']:
                diff_binary_files(a_path / file, b_path / file)
            else:
                diff_text_files(a_path / file, b_path / file)

    return len(d.left_only) + len(d.right_only) + len(d.diff_files) > 0


def _diff_files(a: str, b: str):
    d = Differ()

    with open(a, 'r') as file_a:
        a_lines = file_a.readlines()

    with open(b, 'r') as file_b:
        b_lines = file_b.readlines()

    diff = list(d.compare(a_lines, b_lines))
    result = list(filter(lambda x: x[0] in ['+', '-', '?'], diff))
    return result


def diff_text_files(a: str, b: str):
    result = _diff_files(a, b)
    print(f'File {a} vs {b}:')
    for line in [line.strip('\n') for line in result]:
        print(line)
    return len(result) > 0


def diff_binary_files(a: str, b: str):
    result = _diff_files(a, b)
    print(f'Binary files {a} and {b} differ.')
    return len(result) > 0
