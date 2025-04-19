import os
import sys
from typing import List

def get_source_file_directory(source_file_path: str) -> str:
    """
    Provides the absolute directory path of the source file.

    Paramiters:
        str source_file_path -> The value of the __file__ variable.

    Returns:
        str -> The path to the folder containing the current source file.
    """
    return source_file_path.rsplit(os.sep, 1)[0]

def add_to_path(directory_path: str):
    sys.path.append(os.path.abspath(directory_path))

def relitive_add_to_path(root_directory_path: str, *relitive_path_segments: List[str]):
    """
    Adds to the Python system path, a directory specified relitive to a root directory.

    Paramiters:
        str root_directory_path -> The path onto which to add the relitive path segments.
        List[str] (args) relitive_path_segments -> Relitive path or path segments to append to the root path.
    """
    add_to_path(os.path.join(root_directory_path, *relitive_path_segments))

def source_file_relitive_add_to_path(source_file_path: str, *relitive_path_segments: List[str]):
    """
    Adds to the Python system path, a directory specified relitive to the current source file.

    Paramiters:
        str source_file_path -> The value of the __file__ variable.
    """
    relitive_add_to_path(get_source_file_directory(source_file_path), *relitive_path_segments)
