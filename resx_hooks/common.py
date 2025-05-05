import argparse
import glob
import sys
from pathlib import Path
from typing import List, Dict, Optional, Sequence

from .resx_parser import ResxData, parse_resx_file


def expand_wildcards(patterns: List[str]) -> List[str]:
    """
    Expand wildcard patterns to actual file paths.

    Args:
        patterns: List of file patterns that may contain wildcards

    Returns:
        List of expanded file paths
    """
    expanded_files = []
    for pattern in patterns:
        if '*' in pattern or '?' in pattern or '[' in pattern:
            matched_files = glob.glob(pattern, recursive=True)
            if matched_files:
                expanded_files.extend(matched_files)
            else:
                print(f"Warning: No files matched pattern '{pattern}'")
        else:
            expanded_files.append(pattern)

    return expanded_files


def get_all_resx_files() -> List[str]:
    """
    Find all .resx files tracked by git in the repository.

    Returns:
        List of paths to .resx files
    """
    import subprocess
    try:
        result = subprocess.run(
            ['git', 'ls-files', '*.resx'],
            capture_output=True,
            text=True,
            check=True
        )
        return result.stdout.splitlines()
    except (subprocess.SubprocessError, FileNotFoundError):
        print(
            "Warning: Couldn't find .resx files using git. "
            "Falling back to filesystem search."
        )
        return [str(file) for file in Path('.').glob('**/*.resx')]


def filter_resx_files(filenames: List[str]) -> List[str]:
    """
    Filter a list of filenames to include only .resx files.

    Args:
        filenames: List of file paths

    Returns:
        List containing only .resx files from the input list
    """
    return [
        f for f in filenames
        if Path(f).suffix.lower() == '.resx'
    ]


def parse_cli_args(argv: Optional[Sequence[str]] = None) -> argparse.Namespace:
    """Parses command-line arguments for resx-hooks."""
    parser = argparse.ArgumentParser()
    parser.add_argument(
        'filenames', nargs='*',
        help='Filenames or wildcard patterns of resx files to check.'
    )
    return parser.parse_args(argv)


def parse_resx_files(args: argparse.Namespace) -> Dict[str, ResxData]:
    """
    Parses all resx files specified in the command line arguments
    or found in the git repository, if no files where specified.

    Args:
        args: The parsed command line arguments (Namespace).

    Returns:
        A dictionary mapping file paths to their parsed ResxData.
        Returns an empty dict if no files are found (considered success).
        Exits with status 1 if any file fails to parse.
    """
    if args.filenames:
        expanded_files = expand_wildcards(args.filenames)
        resx_files = filter_resx_files(expanded_files)
    else:
        resx_files = get_all_resx_files()

    if not resx_files:
        print("No .resx files found to parse.")
        return {}

    parsed_files: Dict[str, ResxData] = {}
    for file_path in resx_files:
        try:
            parsed_files[file_path] = parse_resx_file(file_path)
        except Exception as e:
            print(f"Error parsing file {file_path}: {e}", file=sys.stderr)
            sys.exit(1)

    return parsed_files
