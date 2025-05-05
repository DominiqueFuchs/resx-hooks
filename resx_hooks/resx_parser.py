import xml.etree.ElementTree as ET
import re
from typing import Dict, Set, TypeAlias, List

ResxData: TypeAlias = Dict[str, str]


def parse_resx_file(file_path: str) -> ResxData:
    """
    Parse a .resx file and extract key-value pairs.

    Args:
        file_path: Path to the .resx file

    Returns:
        Dictionary with data names as keys and values as values (ResxData)
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


def find_missing_keys(
        parsed_files: Dict[str, ResxData]) -> Dict[str, Set[str]]:
    """
    Find keys missing in some resx files compared to the union of all keys.

    Args:
        parsed_files: Dictionary mapping file paths to their parsed data
                      (ResxData).

    Returns:
        Dictionary mapping file paths to sets of missing keys relative to
        the union.
    """
    all_keys: Set[str] = set()
    file_keys: Dict[str, Set[str]] = {}

    for file_path, data in parsed_files.items():
        keys = set(data.keys())
        file_keys[file_path] = keys
        all_keys.update(keys)

    missing_keys: Dict[str, Set[str]] = {}
    for file_path, keys in file_keys.items():
        missing = all_keys - keys
        if missing:
            missing_keys[file_path] = missing

    return missing_keys


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


def find_empty_values(data: ResxData) -> List[str]:
    """
    Find keys with empty or whitespace-only values in parsed resx data.

    Args:
        data: Parsed resx data (Dictionary mapping keys to values)

    Returns:
        List of keys with empty values
    """
    empty_keys = []
    for key, value in data.items():
        if not value or value.isspace():
            empty_keys.append(key)
    return empty_keys
