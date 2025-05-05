import sys
from typing import Optional, Sequence

from .common import parse_cli_args, parse_resx_files
from .resx_parser import find_empty_values


def main(argv: Optional[Sequence[str]] = None) -> int:
    args = parse_cli_args(argv)
    parsed_files = parse_resx_files(args)

    if not parsed_files:
        return 0

    result = 0
    for file_path, data in parsed_files.items():
        empty_keys = find_empty_values(data)
        if empty_keys:
            result = 1
            print(
                f"File {file_path} has empty values for keys: "
                f"{', '.join(sorted(empty_keys))}")

    return result


if __name__ == '__main__':
    sys.exit(main())
