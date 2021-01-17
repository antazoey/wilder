import os

import click
from PyInquirer import prompt
from wilder.cli.argv import album_option
from wilder.cli.argv import wild_options
from wilder.lib.constants import Constants
from wilder.lib.errors import NotInAlbumError
from wilder.lib.util.sh import get_current_dir


@click.group()
def track():
    """Tools for interacting with tracks from a working album directory."""
    pass


def _check_for_album_json():
    here = get_current_dir(__file__)
    album_json_path = os.path.join(here, "album.json")
    if not os.path.isfile(album_json_path):
        click.echo(
            "Error: all 'track' commands require being an album directory. "
            "Do:\n\n\tcd $(wild album path <album-name>)\n\n"
            "to change to the desired album directory.",
            err=True,
        )


class FromAlbumDirectoryCommand(click.Command):
    def invoke(self, ctx):
        _check_for_album_json()
        return super().invoke(ctx)


@click.command(Constants.LIST, cls=FromAlbumDirectoryCommand)
@wild_options()
def _list(state):
    """List the tracks on an album."""
    # _artist = state.wilder.get_artist(artist)
    # _album = state.wilder.get_album(album_name, artist_name=artist)
    # if _album.tracks:
    #     click.echo(f"'{album_name}' by {_artist.name}: \n")
    #     for track in _album.tracks:
    #         click.echo(f"{track.track_number}. {track.name}")
    # else:
    #     click.echo(f"No tracks yet on album '{_album.name}'.")


# @click.command(cls=ArtistArgRequiredIfGivenCommand)
# @wild_options()
# @artist_option
# @album_option(required=True)
# @click.option("--track-num", help="The track number.", required=True)
# def add(state, artist, path, album, track):
#     """Add a track to an album."""
#     pass


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
