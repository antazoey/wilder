import click
from wilder.cli.argv import album_name_arg
from wilder.cli.argv import album_option
from wilder.cli.argv import artist_option
from wilder.cli.argv import audio_type_option
from wilder.cli.argv import format_option
from wilder.cli.argv import hard_option
from wilder.cli.argv import new_name_arg
from wilder.cli.argv import track_option
from wilder.cli.argv import update_album_options
from wilder.cli.argv import wild_options
from wilder.cli.argv import yes_option
from wilder.cli.cmds import AlbumDirCommand
from wilder.cli.cmds.util import echo_formatted_list
from wilder.cli.output_formats import OutputFormat
from wilder.cli.player import play_album
from wilder.cli.util import abridge
from wilder.cli.util import does_user_agree
from wilder.lib.constants import Constants
from wilder.lib.mgmt.album_dir import echo_tracks


@click.group()
def album():
    """Tools for creating albums."""
    pass


@album.command(cls=click.Command)
@update_album_options()
@click.option("--path", "-p", help=f"The path where to start an album.", required=True)
@click.option("--name", "-n", help="The name to give the album.", required=True)
def new(state, artist, path, name, description, album_type, status):
    """Start a new album at the given path."""
    state.wilder.create_album(
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


@album.command(Constants.LIST, cls=click.Command)
@wild_options()
@artist_option
@format_option
def _list(state, artist, format):
    """List an artist's discography."""
    artist_obj = state.wilder.get_artist(artist)
    disco = artist_obj.get_discography()
    albums_json_list = [a.to_json_for_album_dir() for a in disco]

    if format == OutputFormat.TABLE:
        _abridge_discography_data(albums_json_list)

    click.echo(f"Albums by '{artist_obj.name}':\n")
    echo_formatted_list(format, albums_json_list, header=ALBUM_HEADER)


def _abridge_discography_data(albums_json_list):
    for alb in albums_json_list:
        full_desc = alb.get(Constants.DESCRIPTION)
        if full_desc:
            alb[Constants.DESCRIPTION] = abridge(full_desc)


@album.command(cls=AlbumDirCommand)
@update_album_options()
@album_option()
def update(state, artist, album, description, album_type, status):
    """Update an album."""
    state.wilder.update_album(
        album,
        artist_name=artist,
        description=description,
        album_type=album_type,
        status=status,
    )


@album.command(cls=AlbumDirCommand)
@wild_options()
@new_name_arg
@artist_option
@album_option()
def rename(state, new_name, artist, album):
    """Rename an album."""
    state.wilder.rename_album(new_name, album, artist_name=artist)


@album.command(cls=click.Command)
@wild_options()
@artist_option
@album_name_arg
@yes_option
@hard_option
def remove(state, artist, album_name, hard):
    """Delete an album."""
    _album = state.wilder.get_album(album_name, artist_name=artist)
    if does_user_agree(f"Are you sure you wish to delete the album '{_album.name}'? "):
        state.wilder.delete_album(_album.name, artist_name=artist, hard=hard)


@album.command(cls=AlbumDirCommand)
@wild_options()
@artist_option
@album_option()
def show(state, artist, album):
    """Show information about an album."""
    _album = state.wilder.get_album(album, artist_name=artist)
    click.echo(f"{_album.name} by {_album.artist}:\n\t")
    click.echo(f"{Constants.DESCRIPTION}: {_album.description}")
    click.echo(f"{Constants.ALBUM_TYPE}: {_album.album_type}")
    click.echo(f"{Constants.STATUS}: {_album.status}")
    tracks = _album.tracks
    if tracks:
        click.echo("\nTracks:\n")
        echo_tracks(tracks)


@album.command(cls=AlbumDirCommand)
@wild_options()
@audio_type_option
@artist_option
@album_option()
@track_option()
def play(state, artist, album, audio_type, track):
    """Play an album."""
    _album = state.wilder.get_album(album, artist_name=artist)
    tracks = _album.get_tracks()
    start_track = _album.get_track(track) if track else tracks[0]
    play_album(state.wilder, _album, start_track, audio_type)
