import click
from wilder.cli.argv import album_option
from wilder.cli.argv import all_option
from wilder.cli.argv import artist_option
from wilder.cli.argv import audio_type_option
from wilder.cli.argv import collaborator_option
from wilder.cli.argv import description_option
from wilder.cli.argv import hard_option
from wilder.cli.argv import new_name_option
from wilder.cli.argv import track_name_arg
from wilder.cli.argv import track_num_option
from wilder.cli.argv import track_option
from wilder.cli.argv import wild_options
from wilder.cli.argv import yes_option
from wilder.cli.cmds import AlbumDirCommand
from wilder.cli.select import get_user_selected_item
from wilder.cli.player import play_track
from wilder.cli.util import does_user_agree
from wilder.lib.constants import Constants
from wilder.lib.mgmt.album_dir import echo_tracks


@click.group()
def track():
    """Tools for interacting with tracks from a working album directory."""
    pass


def track_options():
    def decorator(f):
        f = wild_options()(f)
        f = artist_option(f)
        f = album_option()(f)
        return f

    return decorator


def single_track_options():
    def decorator(f):
        f = track_options()(f)
        f = track_name_arg(f)
        return f

    return decorator


def metadata_options():
    def decorator(f):
        f = single_track_options()(f)
        f = track_num_option(f)
        f = description_option("The description of the track.")(f)
        f = collaborator_option(f)
        return f

    return decorator


@track.command("list", cls=AlbumDirCommand)
@track_options()
@all_option(Constants.TRACK)
def _list(state, artist, album, all):
    """List the tracks on an album."""
    if all:
        tracks = []
        artists = state.wilder.get_artists()
    else:
        _album = state.wilder.get_album(album, artist_name=artist)
        tracks = _album.get_tracks()
        click.echo(f"'{_album.name}' by {_album.artist}: \n")
    echo_tracks(tracks)


@track.command(cls=AlbumDirCommand)
@metadata_options()
def new(state, track_name, artist, album, track_number, description, collaborator):
    """Add a track to an album."""
    state.wilder.create_track(
        track_name,
        album,
        artist_name=artist,
        track_number=track_number,
        description=description,
        collaborators=collaborator,
    )


@track.command(cls=AlbumDirCommand)
@single_track_options()
def show(state, track_name, artist, album):
    """Show information about a track."""
    _track = state.wilder.get_track(track_name, album, artist_name=artist)
    click.echo(_track.artist)
    click.echo(f'"{_track.name}"')
    click.echo(_track.album)
    if _track.description:
        click.echo(f'\n"{_track.description}"')


@track.command(cls=AlbumDirCommand)
@metadata_options()
def update(state, track_name, artist, album, track_number, description, collaborator):
    """Update track metadata."""
    state.wilder.update_track(
        track_name,
        album,
        artist_name=artist,
        track_number=track_number,
        description=description,
        collaborators=collaborator,
    )


@track.command(cls=AlbumDirCommand)
@track_options()
@new_name_option(required=True)
@track_option(required=True)
def rename(state, new_name, track, artist, album):
    """Change the name of a track on an album."""
    state.wilder.rename_track(new_name, track, album, artist_name=artist)


@track.command(cls=AlbumDirCommand)
@single_track_options()
@yes_option
@hard_option
def remove(state, track_name, artist, album, hard):
    """Delete a track from an album."""
    _track = state.wilder.get_track(track_name, album, artist_name=artist)
    if does_user_agree(f"Are you sure you wish to delete '{track_name}'? "):
        state.wilder.delete_track(track_name, album, artist_name=artist, hard=hard)


@track.command(cls=AlbumDirCommand)
@track_options()
@click.option(
    "--auto",
    help="Set to skip interactive mode and set track numbers as a sequence.",
    is_flag=True,
)
def reorder(state, artist, album, auto):
    """Reorder the tracks on an album."""
    tracks = state.wilder.get_tracks(album, artist_name=artist)
    track_num_range = tuple(str(i) for i in range(1, len(tracks) + 1))
    track_names = [t.name for t in tracks]
    if not auto:
        answers = _get_track_num_choices(track_names, track_num_range)
        state.wilder.bulk_set_track_numbers(answers, album, artist_name=artist)
    else:
        state.wilder.auto_set_track_numbers(album)


def _get_track_num_choices(track_names, choices, answer_dict=None):
    if not track_names or not choices:
        return answer_dict

    answer_dict = answer_dict or {}
    track_name = track_names.pop()
    message = f"What do you want the track number for '{track_name}' to be?"
    ans = get_user_selected_item(message, choices)
    answer_dict[track_name] = ans
    remaining_choices = tuple(filter(lambda i: i != ans, choices))
    return _get_track_num_choices(track_names, remaining_choices, answer_dict)


@track.command(cls=AlbumDirCommand)
@single_track_options()
@audio_type_option
def play(state, track_name, artist, album, audio_type):
    """Play a track."""
    _track = state.wilder.get_track(track_name, album, artist_name=artist)
    play_track(state.wilder, _track, audio_type=audio_type)
