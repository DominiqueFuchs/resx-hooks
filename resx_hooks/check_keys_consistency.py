import sys
from typing import Dict, Optional, Sequence

from .common import parse_cli_args, parse_resx_files
from .resx_parser import ResxData, find_missing_keys


def main(
    argv: Optional[Sequence[str]] = None,
    parsed_files: Optional[Dict[str, ResxData]] = None
) -> int:
    """Checks if all resx files have the same keys."""
    if parsed_files is None:
        args = parse_cli_args(argv)
        parsed_files = parse_resx_files(args)

    if not parsed_files or len(parsed_files) <= 1:
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
