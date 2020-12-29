import click
from wilder.errors import ArtistAlreadySignedError
from wilder.errors import ArtistNotSignedError
from wildercli.args import name_arg
from wildercli.cmds import album
from wildercli.cmds.album import album
from wildercli.cmds.config import config
from wildercli.cmds.player import play
from wildercli.cmds.util import echo_formatted_list
from wildercli.options import format_option
from wildercli.options import mgmt_options


@click.command()
@mgmt_options()
@format_option
def artists(state, format):
    """List all your artists."""
    _artists = state.mgmt.get_artists()
    artists_list = [{"Name": a.name, "Bio": a.bio} for a in _artists]
    if not artists_list:
        click.echo("There are no artists currently being managed.")
    else:
        echo_formatted_list(format, artists_list)


@click.command()
@mgmt_options()
@name_arg
def sign(state, name):
    """Manage a new artist."""
    try:
        state.mgmt.sign_new_artist(name)
    except ArtistAlreadySignedError:
        click.echo(f"{name} is already signed.")


@click.command()
@mgmt_options()
@name_arg
def unsign(state, name):
    """Stop managing an artist."""
    try:
        state.mgmt.unsign_artist(name)
    except ArtistNotSignedError:
        click.echo(f"{name} is not signed.")
