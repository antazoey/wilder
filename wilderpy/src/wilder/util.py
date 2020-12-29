import json
import os
from os import path

from wilder.constants import Constants as Consts

_PADDING_SIZE = 3
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
                Consts.CLIENT_KEY: {Consts.HOST_KEY: None, Consts.PORT_KEY: None}
            }
            config_content = f"{json.dumps(config_initial_dict)}\n"
            config_file.write(config_content)
    return config_path


def get_project_path(*subdirs):
    """The path on your user dir to /.wilder/[subdir]."""
    home = path.expanduser("~")
    user_project_path = path.join(home, ".wilder")
    result_path = path.join(user_project_path, *subdirs)
    if not path.exists(result_path):
        os.makedirs(result_path)
    return result_path


def format_dict(dict_, label=None):
    indented_dict = json.dumps(dict_, indent=4)
    if label:
        return "{} {}".format(label, indented_dict)
    return indented_dict
