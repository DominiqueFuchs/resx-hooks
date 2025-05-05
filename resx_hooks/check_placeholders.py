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
    reference_file_path = next(iter(parsed_files.keys()))

    key_placeholders: Dict[str, Dict[str, Set[str]]] = {}

    for key in parsed_files[reference_file_path].keys():
        key_placeholders[key] = {}
        for file_path, data in parsed_files.items():
            if key in data:
                value = data[key]
                placeholders = find_placeholders(value)
                key_placeholders[key][file_path] = placeholders

    inconsistencies: Dict[str, FileInconsistencies] = {}
    for key, file_placeholders_map in key_placeholders.items():
        reference_placeholders = next(iter(file_placeholders_map.values()))
        for file_path, placeholders in file_placeholders_map.items():
            if placeholders != reference_placeholders:
                if file_path not in inconsistencies:
                    inconsistencies[file_path] = {}

                inconsistencies[file_path][key] = {
                    'expected': list(reference_placeholders),
                    'found': list(placeholders)
                }

    return inconsistencies


def main(argv: Optional[Sequence[str]] = None) -> int:
    args = parse_cli_args(argv)
    parsed_files = parse_resx_files(args)

    if len(parsed_files) <= 1:
        return 0

    if find_missing_keys(parsed_files):
        print(
            "Warning: Files have inconsistent keys. "
            "Placeholder consistency check may not be exhaustive.",
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
