import click
from wilder.config import delete_config_if_exists
from wilder.config import get_config
from wilder.config import set_client_config_settings
from wilder.constants import Constants
from wildercli.options import yes_option
from wildercli.util import does_user_agree
from wildercli.util import get_url_parts


@click.group()
def config():
    """Adjust settings."""
    pass


@click.command("set")
@click.option(
    "--host",
    "-h",
    help="The host address and port for the Wilder server.",
    required=True,
)
def _set(host):
    """Create a config file to re-use your Wilder connection parameters."""
    path_parts = get_url_parts(host)
    _json = {Constants.HOST_KEY: path_parts[0], Constants.PORT_KEY: path_parts[1]}
    set_client_config_settings(_json)


@click.command()
def show():
    """Show the current client config settings."""
    _config = get_config()
    if _config.is_using_config():
        click.echo(
            f"Host: {_config.host}, Port: {_config.port}. IsEnabled: {str(_config.is_enabled)}"
        )
    else:
        click.echo("Not using config.")


@click.command()
@yes_option
def reset():
    """Delete the config if it exists."""
    _config = get_config()
    _prompt = "Are you sure you wish to delete your config (there is no undo)? "
    if _config.is_using_config() and does_user_agree(_prompt):
        delete_config_if_exists()


@click.command()
def enable():
    """Enable the config."""
    _enable_or_disable(True)


@click.command()
def disable():
    """Disable the config."""
    _enable_or_disable(False)


def _enable_or_disable(do_enable):
    _config = get_config()
    new_json = dict(_config.json)
    new_json[Constants.IS_ENABLED] = do_enable
    set_client_config_settings(new_json)


config.add_command(_set)
config.add_command(show)
config.add_command(reset)
config.add_command(enable)
config.add_command(disable)
