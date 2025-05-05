import sys
import argparse
from typing import Optional, Sequence, List

from .common import expand_wildcards, get_all_resx_files, filter_resx_files
from .resx_parser import parse_resx_file


def find_empty_values(resx_file: str) -> List[str]:
    """
    Find keys with empty values in a resx file.

    Args:
        resx_file: Path to the resx file to check

    Returns:
        List of keys with empty values
    """
    data = parse_resx_file(resx_file)
    empty_keys = []

    for key, value in data.items():
        if not value or value.isspace():
            empty_keys.append(key)

    return empty_keys


def main(argv: Optional[Sequence[str]] = None) -> int:
    parser = argparse.ArgumentParser()
    parser.add_argument(
        'filenames', nargs='*', help='Filenames or wildcard patterns to check')
    args = parser.parse_args(argv)

    if args.filenames:
        expanded_files = expand_wildcards(args.filenames)
        resx_files = filter_resx_files(expanded_files)
    else:
        resx_files = get_all_resx_files()

    if not resx_files:
        print("No .resx files found to check.")
        return 0

    has_empty_values = False

    for file in resx_files:
        empty_keys = find_empty_values(file)
        if empty_keys:
            has_empty_values = True
            print(
                f"File {file} has empty values for keys: "
                f"{', '.join(sorted(empty_keys))}")

    return 1 if has_empty_values else 0


if __name__ == '__main__':
    sys.exit(main())
