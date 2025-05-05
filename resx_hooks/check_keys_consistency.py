import sys
import argparse
from typing import Optional, Sequence

from .common import expand_wildcards, get_all_resx_files, filter_resx_files
from .resx_parser import find_missing_keys


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

    if len(resx_files) <= 1:
        return 0

    missing_keys_map = find_missing_keys(resx_files)

    if missing_keys_map:
        for file_path, missing_keys in missing_keys_map.items():
            print(
                f"File {file_path} is missing keys: "
                f"{', '.join(sorted(missing_keys))}")
        return 1

    return 0


if __name__ == '__main__':
    sys.exit(main())
