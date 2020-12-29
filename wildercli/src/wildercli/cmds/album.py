import click
from wilder.errors import ArtistNotFoundError
from wildercli.args import artist_arg
from wildercli.cmds.util import echo_formatted_list
from wildercli.constants import ALL
from wildercli.options import album_option
from wildercli.options import artist_option
from wildercli.options import format_option
from wildercli.options import mgmt_options


@click.group()
def album():
    """Tools for creating albums."""
    pass


def requires_existing_artist_if_given(f):
    def decorate(*args, **kwargs):
        artist = kwargs.get("artist")
        try:
            return f(*args, **kwargs)
        except ArtistNotFoundError:
            click.echo(f"Artist '{artist}' not found.")

    decorate.__doc__ = f.__doc__
    return decorate


@click.command("new")
@mgmt_options()
@artist_option()
@album_option()
@requires_existing_artist_if_given
def new(state, artist, album):
    """Start a new album."""
    state.mgmt.start_new_album(artist, album)


@click.command("list")
@mgmt_options()
@artist_option(required=False)
@format_option
@requires_existing_artist_if_given
def _list(state, artist, format):
    """List an artist's discography."""
    names = _get_artist_names_from_arg(state.mgmt, artist)
    _albums = _get_discographies(state.mgmt, names)
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


album.add_command(new)
album.add_command(_list)
