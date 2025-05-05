import sys
from typing import Optional, Sequence

from .check_empty_values import main as check_empty_values_main
from .check_keys_consistency import main as check_keys_consistency_main
from .check_placeholders import main as check_placeholders_main
from .common import parse_cli_args, parse_resx_files


def main(argv: Optional[Sequence[str]] = None) -> int:
    """Runs all resx checks sequentially."""
    args = parse_cli_args(argv)
    parsed_files = parse_resx_files(args)

    if not parsed_files:
        return 0

    print("Running all resx checks...")
    return_code = 0

    print("\nChecking keys consistency...")
    if check_keys_consistency_main(parsed_files=parsed_files) != 0:
        print("Keys consistency check failed.")
        return_code = 1

    print("\nChecking for empty values...")
    if check_empty_values_main(parsed_files=parsed_files) != 0:
        print("Empty values check failed.")
        return_code = 1

    print("\nChecking placeholders...")
    if check_placeholders_main(parsed_files=parsed_files) != 0:
        print("Placeholders check failed.")
        return_code = 1

    if return_code == 0:
        print("\nAll checks passed successfully!")

    return return_code


if __name__ == '__main__':
    sys.exit(main())
