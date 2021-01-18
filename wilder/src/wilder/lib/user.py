import json
import os

from wilder.lib.constants import Constants
from wilder.lib.util.sh import create_dir_if_not_exists
from wilder.lib.util.sh import file_exists_with_data
from wilder.lib.util.sh import load_json_from_file
from wilder.lib.util.sh import wopen

CONFIG_FILE_NAME = "config.json"

# This module exists for accessing the .wilder user directory.


def get_mgmt_json(as_dict=True):
    mgmt_path = get_mgmt_json_path()
    _json = load_json_from_file(mgmt_path)
    if as_dict:
        return _json
    return json.dumps(_json)


def get_mgmt_json_path():
    proj_path = get_project_path()
    mgmt_path = os.path.join(proj_path, "mgmt.json")
    if not os.path.exists(mgmt_path):
        with wopen(mgmt_path, "w") as mgmt_file:
            json_dict = {Constants.ARTISTS: []}
            json_str = json.dumps(json_dict, indent=2)
            mgmt_file.write(json_str)
    return mgmt_path


def get_config_path(create_if_not_exists=True):
    proj_path = get_project_path()
    config_path = os.path.join(proj_path, CONFIG_FILE_NAME)
    if create_if_not_exists and not file_exists_with_data(config_path):
        with wopen(config_path, "w") as config_file:
            config_initial_dict = {
                Constants.CLIENT: {Constants.HOST: None, Constants.PORT: None}
            }
            config_content = f"{json.dumps(config_initial_dict)}\n"
            config_file.write(config_content)
    return config_path


def get_project_path(*subdirs):
    """The path on your user dir to /.wilder/[subdir]."""
    home = os.path.expanduser("~")
    user_project_path = os.path.join(home, ".wilder")
    result_path = os.path.join(user_project_path, *subdirs)
    create_dir_if_not_exists(result_path)
    return result_path
