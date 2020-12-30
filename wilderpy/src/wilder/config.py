import json
import os

from wilder.constants import Constants
from wilder.errors import ConfigFileNotFoundError
from wilder.util import get_config_path


def set_client_config_settings(client_config_json):
    config_path = get_config_path()
    full_config = _get_config_json(config_path)
    current_json = full_config.get(Constants.CLIENT_KEY)

    # If setting a host for the first time, enable it.
    if not current_json:
        default_enable = client_config_json.get(Constants.HOST_KEY) is not None
        current_json = {Constants.IS_ENABLED: default_enable} if default_enable else {}

    combined_client_json = _get_new_json(client_config_json, current_json)
    full_config[Constants.CLIENT_KEY] = combined_client_json
    _save_config_change(config_path, full_config)
    return get_config(full_config)


def _get_new_json(new_config, current_config):
    host = _get_new_json_value(new_config, current_config, Constants.HOST_KEY)
    port = _get_new_json_value(new_config, current_config, Constants.PORT_KEY)
    is_enabled = _get_new_json_value(new_config, current_config, Constants.IS_ENABLED)
    return {
        Constants.HOST_KEY: host,
        Constants.PORT_KEY: port,
        Constants.IS_ENABLED: is_enabled,
    }


def _get_new_json_value(new_config, current_config, key):
    return new_config.get(Constants.HOST_KEY) or current_config.get(key)


def _get_config_json(config_path):
    if os.path.exists(config_path):
        with open(config_path) as config_file:
            return json.load(config_file)


def _save_config_change(config_path, config_json):
    if os.path.exists(config_path):
        os.remove(config_path)
    with open(config_path, "w") as config_file:
        config_file.write(json.dumps(config_json))


def get_config(path_to_config=None):
    return WildClientConfig(path_to_config)


def delete_config_if_exists():
    config_path = get_config_path()
    if os.path.exists(config_path):
        os.remove(config_path)


def using_config():
    config = get_config()
    return config.is_using_config()


class WildClientConfig:
    def __init__(self, config_path=None):
        config_path = config_path or get_config_path()
        if not os.path.exists(config_path):
            raise ConfigFileNotFoundError(config_path)
        with open(config_path) as config_file:
            json_obj = json.load(config_file)
            client_settings = json_obj.get(Constants.CLIENT_KEY)
            self.host = client_settings.get(Constants.HOST_KEY)
            self.port = client_settings.get(Constants.PORT_KEY)
            self.is_enabled = client_settings.get(Constants.IS_ENABLED)

    def is_using_config(self):
        return self.host is not None

    @property
    def json(self):
        return {
            Constants.HOST_KEY: self.host,
            Constants.PORT_KEY: self.port,
            Constants.IS_ENABLED: self.is_enabled,
        }
