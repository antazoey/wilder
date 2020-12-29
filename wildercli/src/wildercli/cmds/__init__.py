from wildercli.constants import ALL
from wildercli.cmds.album import album
from wildercli.cmds.config import config
from wildercli.cmds.player import play
import click
from wilder.errors import ArtistAlreadySignedError
from wilder.errors import ArtistNotSignedError
from wildercli.args import artist_arg
from wildercli.args import name_arg
from wildercli.cmds import album
from wildercli.mgmt_factory import get_wilder_mgmt
from wildercli.options import format_option
from wildercli.output_formats import OutputFormatter


@click.command()
@format_option
def artists(format):
    """List all your artists."""
    _mgmt = get_wilder_mgmt()
    _artists = _mgmt.get_artists()
    artists_list = [{"Name": a.name, "Bio": a.bio} for a in _artists]
    if not artists_list:
        click.echo("There are no artists currently being managed.")
    else:
        echo_formatted_list(format, artists_list)


@click.command()
@artist_arg
@format_option
def albums(artist, format):
    """List an artist's discography."""
    _mgmt = get_wilder_mgmt()
    names = _get_artist_names_from_arg(_mgmt, artist)
    _albums = _get_discographies(_mgmt, names)
    if _albums:
        echo_formatted_list(format, _albums)
    else:
        _handle_no_albums_found(names)
    

def _get_artist_names_from_arg(mgmt, arg):
    if arg == ALL:
        all_artists = mgmt.get_artists()
        return [a.name for a in all_artists]
    return [arg]


def _get_discographies(mgmt, artist_names):
    _albums = []
    for name in artist_names:
        _artist = mgmt.get_artist_by_name(name)
        _albums += _artist.discography
    return _albums


def _handle_no_albums_found(names):
    if len(names) == 1:
        msg = f"{names[0]} does not have any albums."
    else:
        names_str = ", ".join(names)
        msg = f"None of the artists '{names_str}' have any albums."
    click.echo(msg)


@click.command()
@name_arg
def sign(name):
    """Manage a new artist."""
    manager = get_wilder_mgmt()
    try:
        manager.sign_new_artist(name)
    except ArtistAlreadySignedError:
        click.echo(f"{name} is already signed.")


@click.command()
@name_arg
def unsign(name):
    """Stop managing an artist."""
    manager = get_wilder_mgmt()
    try:
        manager.unsign_artist(name)
    except ArtistNotSignedError:
        click.echo(f"{name} is not signed.")


def echo_formatted_list(_format, _list):
    formatter = OutputFormatter(_format)
    formatter.echo_formatted_list(_list)
