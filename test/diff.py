# Contains helper functions for comparing the contents of two directories

from argparse import ArgumentParser
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
            try:
                diff_text_files(a_path / file, b_path / file)
            except UnicodeDecodeError:
                diff_binary_files(a_path / file, b_path / file)

    return len(d.left_only) + len(d.right_only) + len(d.diff_files) > 0


def diff_text_files(a: str, b: str):
    d = Differ()

    with open(a, 'r') as file_a:
        a_lines = file_a.readlines()

    with open(b, 'r') as file_b:
        b_lines = file_b.readlines()

    diff = list(d.compare(a_lines, b_lines))
    result = list(filter(lambda x: x[0] in ['+', '-', '?'], diff))

    print(f'File {a} vs {b}:')
    for line in [line.strip('\n') for line in result]:
        print(line)
    return len(result) > 0


def diff_binary_files(a: str, b: str):

    a_size = Path(a).stat().st_size
    b_size = Path(b).stat().st_size

    if a_size != b_size:
        print(f'Binary files {a} and {b} differ.')
        return True

    with open(a, 'rb') as file_a:
        a_bytes = file_a.read()

    with open(b, 'rb') as file_b:
        b_bytes = file_b.read()

    if a_bytes != b_bytes:
        print(f'Binary files {a} and {b} differ.')
        return True

    return False


if __name__ == "__main__":
    parser = ArgumentParser()
    parser.add_argument('a', type=str)
    parser.add_argument('b', type=str)

    args = parser.parse_args()

    diff_directories(args.a, args.b)
