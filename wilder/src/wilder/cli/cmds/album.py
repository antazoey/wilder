import click
from wilder.cli.argv import album_name_arg
from wilder.cli.argv import album_option
from wilder.cli.argv import artist_option
from wilder.cli.argv import format_option
from wilder.cli.argv import update_album_options
from wilder.cli.argv import wild_options
from wilder.cli.argv import yes_option
from wilder.cli.cmds.util import AlbumDirCommand
from wilder.cli.cmds.util import ArtistArgRequiredIfGivenCommand
from wilder.cli.cmds.util import echo_formatted_list
from wilder.cli.cmds.util import get_artist_and_album
from wilder.cli.output_formats import OutputFormat
from wilder.cli.util import abridge
from wilder.cli.util import does_user_agree
from wilder.lib.constants import Constants
from wilder.lib.mgmt.album_dir import echo_tracks


@click.group()
def album():
    """Tools for creating albums."""
    pass


@click.command(cls=ArtistArgRequiredIfGivenCommand)
@update_album_options()
@click.option("--path", "-p", help=f"The path where to start an album.", required=True)
@click.option("--name", "-n", help="The name to give the album.", required=True)
def init(state, artist, path, name, description, album_type, status):
    """Start a new album at the given path."""
    state.wilder.start_new_album(
        path,
        album_name=name,
        artist_name=artist,
        description=description,
        album_type=album_type,
        status=status,
    )


ALBUM_HEADER = {
    Constants.NAME: "Name",
    Constants.PATH: "Path",
    Constants.DESCRIPTION: "Description",
    Constants.ALBUM_TYPE: "Album Type",
    Constants.STATUS: "Status",
}


@click.command()
@wild_options()
@artist_option
@album_name_arg
def path(state, album_name, artist):
    """Prints the path to the album."""
    _album = state.wilder.get_album(album_name, artist_name=artist)
    click.echo(_album.path)


@click.command(Constants.LIST, cls=ArtistArgRequiredIfGivenCommand)
@wild_options()
@artist_option
@format_option
def _list(state, artist, format):
    """List an artist's discography."""
    artist_obj = state.wilder.get_artist(artist)
    albums_json_list = [a.to_full_json() for a in artist_obj.discography]
    if not albums_json_list:
        _handle_no_albums_found(artist_obj.name)
        return

    if format == OutputFormat.TABLE:
        _abridge_discography_data(albums_json_list)

    click.echo(f"Albums by '{artist_obj.name}':\n")
    echo_formatted_list(format, albums_json_list, header=ALBUM_HEADER)


def _abridge_discography_data(albums_json_list):
    for alb in albums_json_list:
        full_desc = alb.get(Constants.DESCRIPTION)
        if full_desc:
            alb[Constants.DESCRIPTION] = abridge(full_desc)


@click.command(cls=AlbumDirCommand)
@update_album_options()
@album_option()
def update(state, artist, album, description, album_type, status):
    """Update an album."""
    album_name = album or state.album_json.get(Constants.NAME)
    state.wilder.update_album(
        album_name,
        artist_name=artist,
        description=description,
        album_type=album_type,
        status=status,
    )


@click.command(cls=ArtistArgRequiredIfGivenCommand)
@wild_options()
@artist_option
@album_name_arg
@yes_option
def delete(state, artist, album_name):
    """Delete an album."""
    _album = state.wilder.get_album(album_name, artist_name=artist)
    if does_user_agree(f"Are you sure you wish to delete the album '{_album.name}'? "):
        state.wilder.delete_album(_album.name, artist_name=artist)


@click.command(cls=AlbumDirCommand)
@wild_options()
@artist_option
@album_option()
def show(state, artist, album):
    """Show information about an album."""
    artist_name, album_name = get_artist_and_album(state, artist, album)
    data = state.album_json
    click.echo(f"{album_name} by {artist_name}:\n\t")
    _echo_kv(Constants.DESCRIPTION, data)
    _echo_kv(Constants.ALBUM_TYPE, data)
    _echo_kv(Constants.STATUS, data)
    tracks = data.get(Constants.TRACKS)
    if tracks:
        click.echo("\nTracks:\n")
        echo_tracks(tracks)


def _echo_kv(key, data):
    click.echo(f"{key}: {data.get(key)}")


def _handle_no_albums_found(name):
    msg = f"{name} does not have any albums."
    click.echo(msg)


album.add_command(init)
album.add_command(_list)
album.add_command(path)
album.add_command(update)
album.add_command(delete)
album.add_command(show)
