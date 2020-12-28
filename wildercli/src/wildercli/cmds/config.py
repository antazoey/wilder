import click
from wilder.config import init_client_config
from wilder.errors import ConfigAlreadyExistsError
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


config.add_command(init)
