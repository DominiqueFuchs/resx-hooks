import xml.etree.ElementTree as ET
from typing import Dict, List, Set


def parse_resx_file(file_path: str) -> Dict[str, str]:
    """
    Parse a .resx file and extract key-value pairs.

    Args:
        file_path: Path to the .resx file

    Returns:
        Dictionary with data names as keys and values as values
    """
    tree = ET.parse(file_path)
    root = tree.getroot()

    result = {}
    for data_node in root.findall(".//data"):
        name = data_node.attrib.get("name")
        if name:
            value_node = data_node.find("value")
            if value_node is not None:
                result[name] = value_node.text or ""

    return result


def get_resx_keys(file_path: str) -> Set[str]:
    """
    Extract just the keys from a .resx file.

    Args:
        file_path: Path to the .resx file

    Returns:
        Set of keys found in the file
    """
    data = parse_resx_file(file_path)
    return set(data.keys())


def find_missing_keys(resx_files: List[str]) -> Dict[str, Set[str]]:
    """
    Find keys that are missing in some resx files but present in others.

    Args:
        resx_files: List of paths to resx files

    Returns:
        Dictionary mapping file paths to sets of missing keys
    """
    all_keys = set()
    file_keys = {}

    for file_path in resx_files:
        keys = get_resx_keys(file_path)
        file_keys[file_path] = keys
        all_keys.update(keys)

    missing_keys = {}
    for file_path, keys in file_keys.items():
        missing = all_keys - keys
        if missing:
            missing_keys[file_path] = missing

    return missing_keys
