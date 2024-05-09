import distutils.sysconfig as sysconfig
import hashlib
import os
from pathlib import Path
from typing import Union


def check_if_dict_in_list(lst: list) -> Union[dict, None]:
    """Check if a dictionary is in a list.

    Args:
        lst (list): List to check.

    Returns:
        dict: Dictionary if found, None otherwise.
    """
    for i in lst:
        if isinstance(i, dict):
            return i
    return None


def std_modules() -> list:
    """Get the list of standard modules in Python.

    Returns:
        list: List of standard modules.
    """
    ret_list = []
    std_lib = sysconfig.get_python_lib(standard_lib=True)
    for top, dirs, files in os.walk(std_lib):
        for nm in files:
            if nm != "__init__.py" and nm[-3:] == ".py":
                ret_list.append(
                    os.path.join(top, nm)[len(std_lib) + 1 : -3].replace("\\", ".")
                )
    return ret_list


def file_hash(path: str) -> str:
    """Get the hash of a file.

    Args:
        path (str): Path to the file.

    Returns:
        str: Hash of the file.
    """
    data = Path(path).read_bytes()
    return hashlib.sha256(data).hexdigest()
