import sys
from typing import Optional, Sequence, List, Dict, Set, TypedDict

from .common import parse_cli_args, parse_resx_files
from .resx_parser import find_missing_keys, find_placeholders, ResxData


class PlaceholderIssue(TypedDict):
    """Represents the expected vs found placeholders for a single key."""
    expected: List[str]
    found: List[str]


FileInconsistencies = Dict[str, PlaceholderIssue]


def check_placeholder_consistency(
        parsed_files: Dict[str, ResxData]
) -> Dict[str, FileInconsistencies]:
    """
    Check if placeholders are consistent across all translations for each key.

    Args:
        parsed_files: Dictionary mapping file paths to their parsed data.

    Returns:
        Dictionary mapping file paths to dictionaries mapping keys to
        inconsistent placeholders.
    """
    all_keys: Set[str] = set()  # Union of all keys
    for data in parsed_files.values():
        all_keys.update(data.keys())

    inconsistencies: Dict[str, FileInconsistencies] = {}

    for key in all_keys:
        reference_placeholders: Optional[Set[str]] = None
        for file_path, data in parsed_files.items():
            if key in data:
                reference_placeholders = find_placeholders(data[key])
                break

        for file_path, data in parsed_files.items():
            if key in data:
                current_placeholders = find_placeholders(data[key])
                if current_placeholders != reference_placeholders:
                    if file_path not in inconsistencies:
                        inconsistencies[file_path] = {}
                    expected_list = sorted(list(reference_placeholders))
                    found_list = sorted(list(current_placeholders))
                    inconsistencies[file_path][key] = {
                        'expected': expected_list,
                        'found': found_list
                    }

    return inconsistencies


def main(argv: Optional[Sequence[str]] = None) -> int:
    args = parse_cli_args(argv)
    parsed_files = parse_resx_files(args)

    if len(parsed_files) <= 1:
        return 0

    missing_keys = find_missing_keys(parsed_files)
    if missing_keys:
        print(
            "Warning: Files have inconsistent keys. "
            "Placeholder consistency check might report issues "
            "actually related to missing keys.",
            file=sys.stderr
        )

    inconsistencies = check_placeholder_consistency(parsed_files)

    if inconsistencies:
        for file_path, file_issues in inconsistencies.items():
            print(f"Inconsistent placeholders in {file_path}:")
            for key, issue in file_issues.items():
                print(f"  Key '{key}':")
                print(f"    Expected: {issue['expected']}")
                print(f"    Found: {issue['found']}")
        return 1

    return 0


if __name__ == '__main__':
    sys.exit(main())
