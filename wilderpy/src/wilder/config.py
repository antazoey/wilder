import os
import json

from wilder.constants import HOST_KEY, PORT_KEY, CLIENT_KEY
from wilder.errors import ConfigFileNotFoundError, ConfigAlreadyExistsError
from wilder.util import get_config_path


def init_client_config(host, port):
    config_path = get_config_path(create_if_not_exists=False)
    client_config = {HOST_KEY: host, PORT_KEY: port}
    config_json = {}
    if os.path.exists(config_path):
        with open(config_path) as config_file:
            config_json = json.load(config_file)
            if config_json.get(CLIENT_KEY):
                raise ConfigAlreadyExistsError()
        os.remove(config_path)
        
    config_json[CLIENT_KEY] = client_config
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
            client_settings = json_obj.get(CLIENT_KEY)
            self.host = client_settings.get(HOST_KEY)
            self.port = client_settings.get(PORT_KEY)

    def is_using_config(self):
        return self.host is not None
