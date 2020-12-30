from wilder.client import create_client
from wilder.config import get_config
from wilder.mgmt import get_mgmt
from wildercli.errors import WildServerConnectionError


def get_wilder_mgmt():
    config = get_config()
    mgmt = (
        create_client(config)
        if config.is_using_config() and config.is_enabled
        else get_mgmt()
    )
    return _test_connection(mgmt)


def _test_connection(mgmt):
    try:
        mgmt.get_mgmt()
    except Exception as err:
        raise WildServerConnectionError(err)
    return mgmt
