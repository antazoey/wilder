import click
from wilder.mgmt import get_mgmt


@click.group()
def album():
    pass


@click.command()
def init():
    """Start a new album."""
    mgmt = get_mgmt()
    mgmt.start_new_album()


album.add_command(init)
