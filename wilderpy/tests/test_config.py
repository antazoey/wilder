import os
import shutil

import pytest
from wilder.config import WildClientConfig
from wilder.config import init_client_config
from wilder.config import delete_config_if_exists
from wilder.errors import ConfigAlreadyExistsError
from wilder.util import get_project_path
from wilder.util import CONFIG_FILE_NAME

TEST_HOST = "example.com"
TEST_PORT = 8888
TEMP_CONFIG_NAME = "temp.config.json"


@pytest.fixture()
def test_config_path():
    # Refers to the config.json in this test's path.
    here = os.path.dirname(os.path.abspath(__file__))
    return os.path.join(here, CONFIG_FILE_NAME)


class ignore_user_config_if_exists:    
    # Makes a copy of the current user config if it exists and then removes the original.
    # When exiting, it will restore the original.
    
    def __init__(self):
        proj_path = get_project_path()
        self.config_path = os.path.join(proj_path, CONFIG_FILE_NAME)
        self.temp_path = os.path.join(proj_path, TEMP_CONFIG_NAME)
    
    def __enter__(self):
        if os.path.exists(self.config_path):
            shutil.copy(self.config_path, self.temp_path)
            os.remove(self.config_path)
    
    def __exit__(self, exc_type, exc_val, exc_tb):
        if os.path.exists(self.temp_path):
            if os.path.exists(self.config_path):
                os.remove(self.config_path)
            shutil.copy(self.temp_path, self.config_path)
            os.remove(self.temp_path)


def test_init_client_config():
    with ignore_user_config_if_exists():
        config = init_client_config(TEST_HOST, TEST_PORT)
        assert config.host == TEST_HOST
        assert config.port == TEST_PORT


def test_init_client_config_when_already_exists_raises_error():
    with ignore_user_config_if_exists():
        init_client_config(TEST_HOST, TEST_PORT)
        with pytest.raises(ConfigAlreadyExistsError):
            init_client_config(TEST_HOST, TEST_PORT)


def test_delete_config_if_exists_deletes_saved_host_and_port():
    with ignore_user_config_if_exists():
        config = init_client_config(TEST_HOST, TEST_PORT)
        assert config.host == TEST_HOST
        assert config.port == TEST_PORT
        delete_config_if_exists()
        config = WildClientConfig()
        assert config.host is None
        assert config.port is None


class TestWildClientConfig:
    def test_init_gets_expected_properties(self, test_config_path):
        config = WildClientConfig(test_config_path)
        assert config.host == TEST_HOST
        assert config.port == TEST_PORT

    def test_init_client_config_when_not_exists_creates(self):
        with ignore_user_config_if_exists():
            config = WildClientConfig()
            assert config.host is None
            assert config.port is None

    def test_is_using_config_returns_false_when_no_host(self):
        with ignore_user_config_if_exists():
            init_client_config(TEST_HOST, TEST_PORT)
            config = WildClientConfig()
            config.host = None
            assert not config.is_using_config()
            
    def test_is_using_config_returns_true_when_has_host(self):
        with ignore_user_config_if_exists():
            init_client_config(TEST_HOST, TEST_PORT)
            config = WildClientConfig()
            assert config.is_using_config()
