import click
from PyInquirer import prompt
from wilder.constants import Constants
from wildercli.argv import album_name_arg
from wildercli.argv import album_option
from wildercli.argv import artist_option
from wildercli.argv import format_option
from wildercli.argv import update_album_options
from wildercli.argv import wild_options
from wildercli.argv import yes_option
from wildercli.cmds.util import ArtistArgRequiredIfGivenCommand
from wildercli.cmds.util import echo_formatted_list
from wildercli.output_formats import OutputFormat
from wildercli.util import abridge
from wildercli.util import does_user_agree


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


@click.command(Constants.LIST, cls=ArtistArgRequiredIfGivenCommand)
@wild_options()
@artist_option
@format_option
def _list(state, artist, format):
    """List an artist's discography."""
    artist_obj = state.get_artist(artist)
    albums_json_list = [a.to_full_json() for a in artist_obj.discography]
    if not albums_json_list:
        _handle_no_albums_found(artist_obj.name)
        return

    if format == OutputFormat.TABLE:
        for alb in albums_json_list:
            full_desc = alb.get(Constants.DESCRIPTION)
            if full_desc:
                alb[Constants.DESCRIPTION] = abridge(full_desc)

    click.echo(f"Albums by '{artist_obj.name}':\n")
    echo_formatted_list(format, albums_json_list, header=ALBUM_HEADER)


@click.command(cls=ArtistArgRequiredIfGivenCommand)
@update_album_options()
@album_name_arg
def update(state, artist, album_name, description, album_type, status):
    """Update an album."""
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
@album_option(required=False)
@click.option("--track-num", help="The track number.", required=True)
def add_track(state, artist, path, album, track):
    """Add a track to an album."""
    pass


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


@click.command(cls=ArtistArgRequiredIfGivenCommand)
@wild_options()
@artist_option
@album_name_arg
@yes_option
def delete(state, artist, album_name):
    """Delete an album."""
    album = state.wilder.get_album(album_name, artist_name=artist)
    if does_user_agree(f"Are you sure you wish to delete the album '{album.name}'? "):
        state.wilder.delete_album(album.name, artist_name=artist)


@click.command(cls=ArtistArgRequiredIfGivenCommand)
@wild_options()
@artist_option
@album_name_arg
def list_tracks(state, artist, album_name):
    """List the tracks on an album."""
    album = state.wilder.get_album(album_name, artist_name=artist)
    if album.tracks:
        for track in album.tracks:
            click.echo(f"({track.track_number}.) {track.name}")
    else:
        click.echo(f"No tracks yet on album '{album.name}'.")


def _handle_no_albums_found(name):
    msg = f"{name} does not have any albums."
    click.echo(msg)


album.add_command(init)
album.add_command(_list)
album.add_command(update)
album.add_command(add_track)
album.add_command(delete)
album.add_command(list_tracks)
album.add_command(reorder)
