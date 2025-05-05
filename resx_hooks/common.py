import argparse
import sys
from typing import Dict, Optional, Sequence

from .resx_parser import ResxData, parse_resx_file


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
    Parses all resx files passed via command line arguments by pre-commit.

    Args:
        args: The parsed command line arguments (Namespace).

    Returns:
        A dictionary mapping file paths to their parsed ResxData.
        Returns an empty dict if no relevant files were passed.
        Exits with status 1 if any file fails to parse.
    """

    if not args.filenames:
        # No files passed by pre-commit, nothing to do.
        return {}

    parsed_files: Dict[str, ResxData] = {}
    for file_path in args.filenames:
        try:
            parsed_files[file_path] = parse_resx_file(file_path)
        except Exception as e:
            print(f"Error parsing file {file_path}: {e}", file=sys.stderr)
            sys.exit(1)

    return parsed_files
