import click
from wilder.errors import ArtistAlreadySignedError
from wilder.errors import ArtistNotSignedError
from wilder.mgmt import get_mgmt
from wildercli.args import name_arg
from wildercli.cmds.mgmt.album import album
from wildercli.cmds.mgmt.artist import artist
from wildercli.cmds.mgmt.artist import artists


@click.group()
def mgmt():
    """Manage your artists, albums, and tracks."""
    pass


@click.command()
@name_arg
def sign(name):
    """Manage a new artist."""
    manager = get_mgmt()
    try:
        manager.sign_new_artist(name)
    except ArtistAlreadySignedError:
        click.echo(f"{name} is already signed.")


@click.command()
@name_arg
def unsign(name):
    """Stop managing an artist."""
    manager = get_mgmt()
    try:
        manager.unsign_artist(name)
    except ArtistNotSignedError:
        click.echo(f"{name} is not signed.")


mgmt.add_command(album)
mgmt.add_command(artist)
mgmt.add_command(artists)
mgmt.add_command(sign)
mgmt.add_command(unsign)
