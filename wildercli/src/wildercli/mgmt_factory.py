from wildercli.errors import WildServerConnectionError
from wilder.client import create_client
from wilder.config import create_config_obj
from wilder.mgmt import get_mgmt


def get_wilder_mgmt():
    config = create_config_obj()
    mgmt = create_client(config) if config.is_using_config() else get_mgmt()
    return _test_connection(mgmt)


def _test_connection(mgmt):
    try:
        mgmt.get_mgmt()
    except Exception as err:
        raise WildServerConnectionError(err)
    return mgmt
