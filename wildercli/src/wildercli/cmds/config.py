import click
from wilder.config import create_config_obj
from wilder.config import delete_config_if_exists
from wilder.config import init_client_config
from wilder.errors import ConfigAlreadyExistsError
from wildercli.options import yes_option
from wildercli.util import does_user_agree
from wildercli.util import get_url_parts


@click.group()
def config():
    """Adjust settings."""
    pass


@click.command()
@click.option(
    "--host",
    "-h",
    help="The host address and port for the Wilder server.",
    required=True,
)
def init(host):
    path_parts = get_url_parts(host)
    try:
        init_client_config(path_parts[0], path_parts[1])
    except ConfigAlreadyExistsError:
        click.echo("Unable to create config. One already exists.", err=True)


@click.command()
def show():
    """Show the current client config settings."""
    _config = create_config_obj()
    if _config.is_using_config():
        click.echo(f"Host: {_config.host}, Port: {_config.port}.")
    else:
        click.echo("Not using config.")


@click.command()
@yes_option
def reset():
    """Deletes the config if it exists."""
    _config = create_config_obj()
    _prompt = "Are you sure you wish to delete your config (there is no undo)? "
    if _config.is_using_config() and does_user_agree(_prompt):
        delete_config_if_exists()


config.add_command(init)
config.add_command(show)
config.add_command(reset)
