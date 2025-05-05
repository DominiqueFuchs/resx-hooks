import sys
import argparse
import re
from typing import Optional, Sequence, List, Dict, Set

from .common import expand_wildcards, get_all_resx_files, filter_resx_files
from .resx_parser import parse_resx_file, find_missing_keys


def find_placeholders(text: str) -> Set[str]:
    """
    Extract placeholders from a string.
    Detects both {0} style and %s style placeholders.

    Args:
        text: String to extract placeholders from

    Returns:
        Set of placeholders found in the string
    """
    braced_placeholders = set(re.findall(r'\{(\d+)(?::[^}]*)?\}', text))
    percent_placeholders = set(re.findall(r'%([sdioxXeEfFgGcrs])', text))

    return braced_placeholders.union(percent_placeholders)


def check_placeholder_consistency(
        resx_files: List[str]) -> Dict[str, Dict[str, Dict[str, List[str]]]]:
    """
    Check if placeholders are consistent across all translations for each key.

    Args:
        resx_files: List of paths to .resx files

    Returns:
        Dictionary mapping file paths to dictionaries mapping keys to
        inconsistent placeholders
    """
    missing_keys_map = find_missing_keys(resx_files)
    if missing_keys_map:
        print(
            "Warning: Files have inconsistent keys. "
            "Placeholder consistency check may not be exhaustive.")

    file_data = {}
    for file_path in resx_files:
        file_data[file_path] = parse_resx_file(file_path)

    key_placeholders = {}
    reference_file = resx_files[0]

    for key in file_data[reference_file].keys():
        key_placeholders[key] = {}
        for file_path in resx_files:
            if key in file_data[file_path]:
                value = file_data[file_path][key]
                placeholders = find_placeholders(value)
                key_placeholders[key][file_path] = placeholders

    inconsistencies = {}
    for key, file_placeholders in key_placeholders.items():
        reference_placeholders = next(iter(file_placeholders.values()))
        for file_path, placeholders in file_placeholders.items():
            if placeholders != reference_placeholders:
                if file_path not in inconsistencies:
                    inconsistencies[file_path] = {}

                inconsistencies[file_path][key] = {
                    'expected': list(reference_placeholders),
                    'found': list(placeholders)
                }

    return inconsistencies


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

    inconsistencies = check_placeholder_consistency(resx_files)
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
