import json
import os
import shutil
from pathlib import Path

from wilder.lib.errors import WildNotFoundError

# This module abstracts some OS shell operations.


def wopen(*args, **kwargs):
    """Open a file."""
    return open(*args, **kwargs)


def expand_path(path):
    """Get the real path from the given one."""
    if path:
        path = os.path.expanduser(path)
        return os.path.abspath(path)


def copy_files_to_dir(source_files, dest_path):
    """Copy the given files to the destination."""
    if not isinstance(source_files, (list, tuple)):
        source_files = [source_files]
    for file in source_files:
        copy_file_to_dir(file, dest_path)


def copy_file_to_dir(source_file, dest_path):
    """Copy a source file to the given destination."""
    if not source_file or not os.path.isfile(source_file):
        raise WildNotFoundError(f"File not found: {source_file}.")

    path = Path(dest_path)
    if not os.path.exists(path.parent):
        os.makedirs(path.parent)

    remove_file_if_exists(dest_path)
    shutil.copy(source_file, dest_path)


def remove_file_if_exists(file_path):
    """Delete a file if it exists."""
    if file_path and os.path.isfile(file_path):
        os.remove(file_path)


def remove_directory(dir_path):
    shutil.rmtree(dir_path)


def create_dir_if_not_exists(path):
    """Build a directory tree."""
    if path and not os.path.exists(path):
        os.makedirs(path)


def save_json_as(to, json_dict):
    """Dump a JSON dict to the file at the given location."""
    json_text = f"{json.dumps(json_dict, indent=2)}\n"
    save_as(to, json_text)


def save_as(to, file_text):
    """Overwrites or creates the file at the path with the given text."""
    remove_file_if_exists(to)
    with wopen(to, "w") as file_to_save:
        file_to_save.write(file_text)


def get_file_dir(file=None):
    """Get the directory name of the given file."""
    return os.path.dirname(os.path.abspath(file or __file__))


def load_json_from_file(file_path):
    """Get a JSON dict loaded from a file."""
    with wopen(file_path) as json_file:
        return json.load(json_file)


def file_exists_with_data(file_path):
    """Check if a file exists and contains bytes."""
    return os.path.isfile(file_path) and os.path.getsize(file_path)
