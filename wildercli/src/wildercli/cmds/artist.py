import click
from wilder.errors import ArtistAlreadySignedError
from wilder.errors import ArtistNotSignedError
from wildercli.args import name_arg
from wildercli.cmds.util import echo_formatted_list
from wildercli.options import bio_option
from wildercli.options import format_option
from wildercli.options import mgmt_options


@click.group()
def artist():
    """Tools for artist management."""
    pass


@click.command("list")
@mgmt_options()
@format_option
def _list(state, format):
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
@bio_option
def sign(state, name, bio):
    """Manage a new artist."""
    try:
        state.mgmt.sign_new_artist(name, bio=bio)
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


artist.add_command(_list)
artist.add_command(sign)
artist.add_command(unsign)
