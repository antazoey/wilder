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
                Consts.CLIENT: {Consts.HOST: None, Consts.PORT: None}
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


def to_bool(val):
    """Converts some values to booleans.

    Return conditions:
        * val when val is a bool
        * True when val.lower() is in ["t", "true"]
        * True when val is 1
        * False when val.lower() is in ["f", "false"]
        * False when val is 0
        * None for everything else
    """
    if val is None:
        return None

    elif isinstance(val, bool):
        return val

    elif isinstance(val, str):
        val = val.lower()
        if val in ["t", "true"]:
            return True
        elif val in ["f", "false"]:
            return False

    elif isinstance(val, int):
        if val == 0:
            return False
        elif val == 1:
            return True
    return None


def to_int(val):
    """Converts some values to integers.

    Return conditions:
        * val when val is an int
        * int(val) when val is a numeric str
        * None for everything else
    """
    if val is None:
        return None
    elif isinstance(val, int):
        return val
    elif isinstance(val, str):
        if val.isnumeric():
            return int(val)
    return None
