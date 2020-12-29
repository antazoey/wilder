import click
from wilder.errors import ArtistNotFoundError
from wildercli.mgmt_factory import get_wilder_mgmt
from wildercli.options import album_option
from wildercli.options import artist_option


@click.group()
def album():
    """Tools for creating albums."""
    pass


@click.command()
@artist_option()
@album_option()
def new(artist, album):
    """Start a new album."""
    mgmt = get_wilder_mgmt()
    try:
        mgmt.start_new_album(artist, album)
    except ArtistNotFoundError:
        click.echo(f"Artist '{artist}' not found.")


album.add_command(new)
