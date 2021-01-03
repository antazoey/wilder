from wildclient import create_client
from wilder import get_wilder_sdk
from wilder.config import create_config_object
from wildercli.errors import WildServerConnectionError


def get_wilder():
    config = create_config_object()
    client = (
        create_client(config)
        if config.is_using_config() and config.is_enabled
        else get_wilder_sdk()
    )
    return _test_connection(client)


def _test_connection(mgmt):
    try:
        if not mgmt:
            raise WildServerConnectionError(Exception("Missing client."))
        mgmt.get_mgmt_json()
    except Exception as err:
        raise WildServerConnectionError(err)
    return mgmt
