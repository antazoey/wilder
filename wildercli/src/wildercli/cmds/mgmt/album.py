import click
from wildercli.options import artist_option
from wilderpy.mgmt import get_mgmt


@click.group()
def album():
    """Manage your albums."""
    pass


@click.command("list")
@artist_option()
def _list(artist):
    mgmt = get_mgmt()
    return mgmt.get_all_albums_for_artist(artist)


album.add_command(_list)
