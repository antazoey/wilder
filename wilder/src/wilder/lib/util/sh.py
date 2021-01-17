import os
import shutil
from pathlib import Path

from wilder.lib.errors import WildNotFoundError

# This module abstracts some OS shell operations.


def wopen(*args, **kwargs):
    return open(*args, **kwargs)


def expand_path(path):
    if path:
        path = os.path.expanduser(path)
        return os.path.abspath(path)


def copy_files_to_dir(source_files, dest_path):
    if not isinstance(source_files, (list, tuple)):
        source_files = [source_files]
    for file in source_files:
        copy_file_to_dir(file, dest_path)


def copy_file_to_dir(source_file, dest_path):
    if not source_file or not os.path.isfile(source_file):
        raise WildNotFoundError(f"File not found: {source_file}.")

    path = Path(dest_path)
    if not os.path.exists(path.parent):
        os.makedirs(path.parent)

    remove_file_if_exists(dest_path)
    shutil.copy(source_file, dest_path)


def remove_file_if_exists(file_path):
    if file_path and os.path.isfile(file_path):
        os.remove(file_path)


def create_dir_if_not_exists(path):
    if path and not os.path.exists(path):
        os.makedirs(path)


def save_as(to, file_text):
    """Overwrites or creates the file at the path with the given text.."""
    remove_file_if_exists(to)
    with wopen(to, "w") as file_to_save:
        file_to_save.write(file_text)
