import os

import click
from PyInquirer import prompt
from wilder.cli.argv import wild_options
from wilder.lib.constants import Constants
from wilder.lib.errors import NotInAlbumError
from wilder.lib.util.sh import load_json_from_file


@click.group()
def track():
    """Tools for interacting with tracks from a working album directory."""
    pass


def _get_album_json(wilder):
    here = os.getcwd()
    album_json_path = os.path.join(here, "album.json")
    if not os.path.isfile(album_json_path):

        # Try checking all the managed albums to see if you're in a known path.
        artists = wilder.get_artists()
        for artist in artists:
            album_paths = [a.path for a in artist.discography]
            for path in album_paths:
                if path == here:
                    print("HERE")
                    exit(1)
                    break

        raise NotInAlbumError()
    return load_json_from_file(album_json_path)


class FromAlbumDirectoryCommand(click.Command):
    def invoke(self, ctx):
        ctx.obj.album_json = _get_album_json(ctx.obj.wilder)
        return super().invoke(ctx)


@click.command(Constants.LIST, cls=FromAlbumDirectoryCommand)
@wild_options()
def _list(state):
    """List the tracks on an album."""
    artist_name = state.album_json.get(Constants.ARTIST)
    album_name = state.album_json.get(Constants.NAME)
    _album = state.wilder.get_album(album_name)

    if _album.tracks:
        click.echo(f"'{album_name}' by {artist_name}: \n")
        for tr in _album.tracks:
            click.echo(f"{tr.track_number}. {tr.name}")
    else:
        click.echo(f"No tracks yet on album '{_album.name}'.")


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
