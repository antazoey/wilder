import click
from wildercli.util import get_wilder_mgmt


@click.group()
def album():
    """Tools for creating albums."""
    pass


@click.command()
def init():
    """Start a new album."""
    mgmt = get_wilder_mgmt()
    mgmt.start_new_album()


album.add_command(init)
