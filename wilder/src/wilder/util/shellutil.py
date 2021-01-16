import os
import shutil


def wopen(*args, **kwargs):
    return open(*args, **kwargs)


def expand_path(path):
    if path:
        path = os.path.expanduser(path)
        return os.path.abspath(path)
    
    
def copy_files_to_dir(source_files, dest_path):
    for file in source_files:
        copy_file_to_dir(file, dest_path)


def copy_file_to_dir(source_file, dest_path):
    if not os.path.isfile(source_file):
        raise WilderNotFoundError(f"File not found: {source_file}.")
    remove_file_if_exists(dest_path)
    shutil.copy(source_file, dest_path)


def remove_file_if_exists(file_path):
    if os.path.isfile(file_path):
        os.remove(file_path)


def create_dir_if_not_exists(path):
    if not os.path.exists(path):
        os.makedirs(path)
