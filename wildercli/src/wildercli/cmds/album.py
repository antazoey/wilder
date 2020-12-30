import click
from wilder.constants import Constants
from wildercli.cmds.util import artist_arg_required_if_given
from wildercli.cmds.util import echo_formatted_list
from wildercli.options import album_option
from wildercli.options import artist_option
from wildercli.options import format_option
from wildercli.options import mgmt_options


@click.group()
def album():
    """Tools for creating albums."""
    pass


@click.command(cls=artist_arg_required_if_given(Constants.ARTIST))
@mgmt_options()
@artist_option()
@album_option()
def new(state, artist, album):
    """Start a new album."""
    artist = artist or state.mgmt.get_focus_artist().name
    state.mgmt.start_new_album(artist, album)


@click.command("list", cls=artist_arg_required_if_given(Constants.ARTIST))
@mgmt_options()
@artist_option(required=False)
@format_option
def _list(state, artist, format):
    """List an artist's discography."""
    artist_obj = (
        state.mgmt.get_artist_by_name(artist)
        if artist
        else state.mgmt.get_focus_artist()
    )
    _albums = artist_obj.discography
    echo_formatted_list(format, _albums) if _albums else _handle_no_albums_found(
        artist_obj.name
    )


def _handle_no_albums_found(name):
    msg = f"{name} does not have any albums."
    click.echo(msg)


album.add_command(new)
album.add_command(_list)
