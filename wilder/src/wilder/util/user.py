import os
import json
from wilder.util.shellutil import create_dir_if_not_exists

CONFIG_FILE_NAME = "config.json"


def get_mgmt_json(mgmt_path=None, as_dict=True):
    mgmt_path = mgmt_path or get_mgmt_json_path()
    with open(mgmt_path) as mgmt_file:
        json_dict = json.load(mgmt_file)
        if as_dict:
            return json_dict
        return json.dumps(json_dict)


def get_mgmt_json_path():
    proj_path = get_project_path()
    mgmt_path = os.path.join(proj_path, "mgmt.json")
    if not os.path.exists(mgmt_path):
        with open(mgmt_path, "w") as mgmt_file:
            json_dict = {Consts.ARTISTS: []}
            json_str = json.dumps(json_dict, indent=2)
            mgmt_file.write(json_str)
    return mgmt_path


def get_config_path(create_if_not_exists=True):
    proj_path = get_project_path()
    config_path = os.path.join(proj_path, CONFIG_FILE_NAME)
    if create_if_not_exists and not os.path.exists(config_path):
        with open(config_path, "w") as config_file:
            config_initial_dict = {
                Consts.CLIENT: {Consts.HOST: None, Consts.PORT: None}
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
