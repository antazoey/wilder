import json
import os

from wilder.constants import Constants
from wilder.errors import ConfigAlreadyExistsError
from wilder.errors import ConfigFileNotFoundError
from wilder.util import get_config_path


def init_client_config(host, port):
    config_path = get_config_path(create_if_not_exists=False)
    client_config = {Constants.HOST_KEY: host, Constants.PORT_KEY: port}
    config_json = {}
    if os.path.exists(config_path):
        with open(config_path) as config_file:
            config_json = json.load(config_file)
            if config_json.get(Constants.CLIENT_KEY).get(Constants.HOST_KEY):
                raise ConfigAlreadyExistsError()
        os.remove(config_path)

    config_json[Constants.CLIENT_KEY] = client_config
    with open(config_path, "w") as config_file:
        config_file.write(json.dumps(config_json))
    return create_config_obj(config_path)


def create_config_obj(path_to_config=None):
    return WildClientConfig(path_to_config)


def delete_config_if_exists():
    config_path = get_config_path()
    if os.path.exists(config_path):
        os.remove(config_path)


def using_config():
    config = create_config_obj()
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

    def is_using_config(self):
        return self.host is not None
