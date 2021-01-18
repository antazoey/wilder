import click
from PyInquirer import prompt
from wilder.cli.argv import album_option
from wilder.cli.argv import artist_option
from wilder.cli.argv import collaborator_option
from wilder.cli.argv import description_option
from wilder.cli.argv import track_name_arg
from wilder.cli.argv import track_num_option
from wilder.cli.argv import wild_options
from wilder.cli.cmds.util import AlbumDirCommand
from wilder.lib.constants import Constants
from wilder.lib.mgmt.album_dir import echo_tracks


@click.group()
def track():
    """Tools for interacting with tracks from a working album directory."""
    pass


@click.command(Constants.LIST, cls=AlbumDirCommand)
@wild_options()
def _list(state):
    """List the tracks on an album."""
    artist_name = state.album_json.get(Constants.ARTIST)
    album_name = state.album_json.get(Constants.NAME)
    _album = state.wilder.get_album(album_name)

    if _album.tracks:
        click.echo(f"'{album_name}' by {artist_name}: \n")
        echo_tracks(_album.tracks)
    else:
        click.echo(f"No tracks yet on album '{_album.name}'.")


@click.command(cls=AlbumDirCommand)
@wild_options()
@artist_option
@album_option()
@track_name_arg
@track_num_option
@description_option("The description of the track.")
@collaborator_option
def new(state, artist, track_name, track_num):
    """Add a track to an album."""
    album = state.album_json.get(Constants.NAME)
    state.wilder.start_new_track(
        album, track_name, artist_name=artist, track_num=track_num
    )


@click.command()
def reorder():
    """Reorder the tracks on an album."""
    questions = [
        {
            "type": "list",
            "name": "list_name",
            "message": "Add task to which list?",
            "choices": ["test", "foo"],
        },
        {"type": "input", "name": "task_name", "message": "Task description"},
    ]
    answers = prompt(questions)


track.add_command(_list)
# track.add_command(add)
track.add_command(reorder)
