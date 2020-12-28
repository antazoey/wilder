import json
import os
from os import path

_PADDING_SIZE = 3


def get_mgmt_json():
    proj_path = get_project_path()
    mgmt_path = os.path.join(proj_path, "mgmt.json")
    if not os.path.exists(mgmt_path):
        with open(mgmt_path, "w") as mgmt_file:
            json_dict = {"artists": []}
            json_str = json.dumps(json_dict, indent=2)
            mgmt_file.write(json_str)
            return json_dict
    with open(mgmt_path) as mgmt_file:
        return json.load(mgmt_file)


def get_project_path(*subdirs):
    """The path on your user dir to /.wilder/[subdir]."""
    home = path.expanduser("~")
    user_project_path = path.join(home, ".wilder")
    result_path = path.join(user_project_path, *subdirs)
    if not path.exists(result_path):
        os.makedirs(result_path)
    return result_path
