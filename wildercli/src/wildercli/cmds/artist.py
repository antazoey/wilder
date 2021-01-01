import click
from wilder.constants import Constants
from wilder.errors import ArtistAlreadySignedError
from wilder.errors import ArtistNotSignedError
from wildercli.argv import alias_arg
from wildercli.argv import artist_name_arg
from wildercli.argv import artist_name_option
from wildercli.argv import bio_option
from wildercli.argv import format_option
from wildercli.argv import wild_options
from wildercli.cmds.util import artist_arg_required_if_given
from wildercli.cmds.util import echo_formatted_list
from wildercli.util import get_abridged_str


@click.group()
def artist():
    """Tools for artist management."""
    pass


@click.command(cls=artist_arg_required_if_given())
@wild_options()
@artist_name_option(required=False)
def show(state, artist):
    """The artist information."""
    _artist = state.get_artist(artist)
    also_known_as = ", ".join(_artist.also_known_as)
    click.echo(f"{Constants.NAME}: {_artist.name}")
    click.echo(f"{Constants.BIO}: {_artist.bio}")
    if also_known_as:
        click.echo(f"Also known as: '{also_known_as}'")


@click.command(Constants.LIST)
@wild_options()
@format_option
def _list(state, format):
    """List all your artists."""
    _artists = state.wilder.get_artists()
    artists_list = [
        {Constants.NAME.capitalize(): a.name, Constants.BIO.capitalize(): get_abridged_str(a.bio)}
        for a in _artists
    ]
    if not artists_list:
        click.echo("There are no artists currently being managed.")
    else:
        echo_formatted_list(format, artists_list)


@click.command()
@wild_options()
@artist_name_arg
@bio_option
def sign(state, artist_name, bio):
    """Manage a new artist."""
    try:
        state.wilder.sign_new_artist(artist_name, bio=bio)
    except ArtistAlreadySignedError:
        click.echo(f"{artist_name} is already signed.")


@click.command()
@wild_options()
@artist_name_arg
def unsign(state, artist_name):
    """Stop managing an artist."""
    try:
        state.wilder.unsign_artist(artist_name)
    except ArtistNotSignedError:
        click.echo(f"{artist_name} is not signed.")


@click.command(cls=artist_arg_required_if_given())
@wild_options()
@artist_name_option(required=False)
@bio_option
def update(state, artist_name, bio):
    """Update artist information."""
    if not bio:
        click.echo("Nothing to do.")
        return
    name = state.get_artist(artist_name).name
    state.wilder.update_artist(name, bio)


@click.command(cls=artist_arg_required_if_given())
@wild_options()
@artist_name_arg
def focus(state, artist_name):
    """Change the focus artist."""
    state.wilder.focus_on_artist(artist_name)


@click.command(cls=artist_arg_required_if_given())
@wild_options()
@artist_name_option(required=False)
@alias_arg
def add_alias(state, artist, alias):
    """Add an artist alias."""
    _artist = state.get_artist(artist).name
    state.wilder.add_alias(_artist, alias)


@click.command(cls=artist_arg_required_if_given())
@wild_options()
@artist_name_option(required=False)
@alias_arg
def remove_alias(state, artist, alias):
    """Remove an artist alias."""
    _artist = state.get_artist(artist).name
    state.wilder.remove_alias(_artist, alias)


@click.command()
@click.option(
    "--forget-old-name",
    help="To not retain any 'FKA' (formerly known-as) data.",
    default=False,
)
def rename(forget_old_name):
    """Rename an artist."""
    pass


artist.add_command(_list)
artist.add_command(sign)
artist.add_command(unsign)
artist.add_command(focus)
artist.add_command(update)
artist.add_command(show)
artist.add_command(rename)
artist.add_command(add_alias)
artist.add_command(remove_alias)
