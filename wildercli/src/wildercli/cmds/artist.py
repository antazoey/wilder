import click
from wilder.constants import Constants
from wilder.errors import ArtistAlreadySignedError
from wilder.errors import ArtistNotSignedError
from wildercli.cmds.util import artist_arg_required_if_given
from wildercli.cmds.util import echo_formatted_list
from wildercli.argv import artist_name_option, artist_name_arg
from wildercli.argv import bio_option
from wildercli.argv import format_option
from wildercli.argv import mgmt_options


@click.group()
def artist():
    """Tools for artist management."""
    pass


@click.command(Constants.LIST)
@mgmt_options()
@format_option
def _list(state, format):
    """List all your artists."""
    _artists = state.mgmt.get_artists()
    artists_list = [{Constants.NAME.capitalize(): a.name, Constants.BIO.capitalize(): a.bio} for a in _artists]
    if not artists_list:
        click.echo("There are no artists currently being managed.")
    else:
        echo_formatted_list(format, artists_list)


@click.command()
@mgmt_options()
@artist_name_arg
@bio_option
def sign(state, artist_name, bio):
    """Manage a new artist."""
    try:
        state.mgmt.sign_new_artist(artist_name, bio=bio)
    except ArtistAlreadySignedError:
        click.echo(f"{artist_name} is already signed.")


@click.command()
@mgmt_options()
@artist_name_arg
def unsign(state, artist_name):
    """Stop managing an artist."""
    try:
        state.mgmt.unsign_artist(artist_name)
    except ArtistNotSignedError:
        click.echo(f"{artist_name} is not signed.")


@click.command(cls=artist_arg_required_if_given(Constants.ARTIST))
@mgmt_options()
@artist_name_option(required=False)
@bio_option
def update(state, artist_name, bio):
    """Update artist information."""
    if not bio:
        click.echo("Nothing to do.")
        return
    name = artist_name or state.mgmt.get_focus_artist().name
    state.mgmt.update_artist(name, bio)


@click.command(cls=artist_arg_required_if_given(Constants.NAME))
@mgmt_options()
@artist_name_arg
def focus(state, artist_name):
    """Change the focus artist."""
    state.mgmt.focus_on_artist(artist_name)


artist.add_command(_list)
artist.add_command(sign)
artist.add_command(unsign)
artist.add_command(focus)
artist.add_command(update)
