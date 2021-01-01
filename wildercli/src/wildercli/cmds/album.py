import click
from wilder.constants import Constants
from wildercli.argv import album_name_arg, album_options
from wildercli.argv import artist_name_option
from wildercli.argv import format_option
from wildercli.argv import wild_options
from wildercli.cmds.util import artist_arg_required_if_given
from wildercli.cmds.util import echo_formatted_list
from wildercli.util import get_abridged_str


@click.group()
def album():
    """Tools for creating albums."""
    pass


@click.command(cls=artist_arg_required_if_given())
@wild_options()
@artist_name_option(required=False)
@album_name_arg
@album_options()
def new(state, artist, album_name, description):
    """Start a new album."""
    artist = state.get_artist(artist).name
    state.wilder.start_new_album(artist, album_name, description=description)


@click.command(Constants.LIST, cls=artist_arg_required_if_given())
@wild_options()
@artist_name_option(required=False)
@format_option
def _list(state, artist, format):
    """List an artist's discography."""
    artist_obj = state.get_artist(artist)
    albums_json_list = [a.to_json() for a in artist_obj.discography]
    if not albums_json_list:
        _handle_no_albums_found(artist_obj.name)
        return
    
    for alb in albums_json_list:
        full_desc = alb.get(Constants.DESCRIPTION)
        if full_desc:
            alb[Constants.DESCRIPTION] = get_abridged_str(full_desc)

    click.echo(f"Albums by '{artist_obj.name}':\n")
    echo_formatted_list(format, albums_json_list)


def _handle_no_albums_found(name):
    msg = f"{name} does not have any albums."
    click.echo(msg)


album.add_command(new)
album.add_command(_list)
