import click
from wilder.errors import ArtistAlreadySignedError
from wilder.errors import ArtistNotFoundError
from wilder.errors import ArtistNotSignedError
from wildercli.args import artist_arg
from wildercli.args import name_arg
from wildercli.cmds import album
from wildercli.mgmt_factory import get_wilder_mgmt
from wildercli.options import format_option
from wildercli.output_formats import OutputFormatter


@click.group()
def mgmt():
    """Manage your artists, albums, and tracks."""
    pass


@click.command()
@format_option
def artists(format):
    """List all your artists."""
    _mgmt = get_wilder_mgmt()
    _artists = _mgmt.get_artists()
    artists_to_list = [{"Name": a.name, "Bio": a.bio} for a in _artists]
    if not artists_to_list:
        click.echo("There are no artists currently being managed.")
    else:
        formatter = OutputFormatter(format)
        formatter.echo_formatted_list(artists_to_list)


@click.command()
@name_arg
def artist(name):
    """Get artist info by name."""
    _mgmt = get_wilder_mgmt()
    not_found_msg = f"Artist '{name}' not found."
    try:
        _artist = _mgmt.get_artist_by_name(name)
        if _artist is None:
            click.echo(not_found_msg, err=True)
        return _artist
    except ArtistNotFoundError:
        click.echo(not_found_msg, err=True)


@click.command()
@artist_arg
@format_option
def albums(artist, format):
    """List an artist's discography."""
    _mgmt = get_wilder_mgmt()
    _artist = _mgmt.get_artist_by_name(artist)
    _albums = _artist.discography
    if not _albums:
        click.echo(f"{_artist.name} does not have any albums.")
    else:
        formatter = OutputFormatter(format)
        formatter.echo_formatted_list(_albums)
    return _artist.discography


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


mgmt.add_command(artists)
mgmt.add_command(albums)
mgmt.add_command(artist)
mgmt.add_command(sign)
mgmt.add_command(unsign)
mgmt.add_command(album)
