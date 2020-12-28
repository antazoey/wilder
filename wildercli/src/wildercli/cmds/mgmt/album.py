import click
from wilder.mgmt import get_mgmt
from wildercli.options import artist_option


@click.group()
def album():
    """Tools for creating albums."""
    pass


@click.command("list")
@artist_option()
def _list(artist):
    mgmt = get_mgmt()
    return mgmt.get_all_albums_for_artist(artist)


album.add_command(_list)
