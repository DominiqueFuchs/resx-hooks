import sys
from typing import Optional, Sequence

from .common import parse_cli_args, parse_resx_files
from .resx_parser import find_missing_keys


def main(argv: Optional[Sequence[str]] = None) -> int:
    args = parse_cli_args(argv)
    parsed_files = parse_resx_files(args)

    if len(parsed_files) <= 1:
        return 0

    missing_keys_map = find_missing_keys(parsed_files)

    if missing_keys_map:
        for file_path, missing_keys in missing_keys_map.items():
            print(
                f"File {file_path} is missing keys: "
                f"{', '.join(sorted(missing_keys))}")
        return 1

    return 0


if __name__ == '__main__':
    sys.exit(main())
