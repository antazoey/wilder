import os
import shutil

from wilder.util import CONFIG_FILE_NAME
from wilder.util import get_project_path

TEMP_USER_DIR = ".tempwilder"


def ignore_user_project_files(f):
    """Temporarily Removes and then restores app files, for integration test purposes."""

    class ignore_local_user_if_exists:
        # Makes a copy of the current user config if it exists and then removes the original.
        # When exiting, it will restore the original.

        def __init__(self):
            self.proj_path = get_project_path()
            self.temp_path = os.path.join(self.proj_path, TEMP_USER_DIR)

        def __enter__(self):
            if not os.path.exists(self.proj_path):
                return
            shutil.copytree(self.proj_path, self.temp_path)
            shutil.rmtree(self.proj_path)

        def __exit__(self, exc_type, exc_val, exc_tb):
            if not os.path.exists(self.temp_path):
                return
            if os.path.exists(self.proj_path):
                shutil.rmtree(self.proj_path)
            shutil.copytree(self.temp_path, self.proj_path)
            shutil.rmtree(self.temp_path)

    def decorated(*args, **kwargs):
        with ignore_local_user_if_exists():
            f(*args, **kwargs)

    return decorated
