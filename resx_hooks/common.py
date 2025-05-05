import glob
from pathlib import Path
from typing import List


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
