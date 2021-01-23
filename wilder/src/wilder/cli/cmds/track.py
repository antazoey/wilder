import click
from PyInquirer import prompt
from wilder.cli.argv import album_option
from wilder.cli.argv import artist_option
from wilder.cli.argv import audio_type_option
from wilder.cli.argv import collaborator_option
from wilder.cli.argv import description_option
from wilder.cli.argv import hard_option
from wilder.cli.argv import track_name_arg
from wilder.cli.argv import track_num_option
from wilder.cli.argv import wild_options
from wilder.cli.argv import yes_option
from wilder.cli.cmds import AlbumDirCommand
from wilder.cli.util import does_user_agree
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


@click.command("list", cls=AlbumDirCommand)
@track_options()
def _list(state, artist, album):
    """List the tracks on an album."""
    _album = state.wilder.get_album(album, artist_name=artist)
    if _album.tracks:
        click.echo(f"'{_album.name}' by {_album.artist}: \n")
        echo_tracks(_album.tracks)
    else:
        click.echo(f"No tracks yet on album '{_album.name}'.")


@click.command(cls=AlbumDirCommand)
@metadata_options()
def new(state, track_name, artist, album, track_number, description, collaborator):
    """Add a track to an album."""
    state.wilder.start_new_track(
        track_name,
        album,
        artist_name=artist,
        track_number=track_number,
        description=description,
        collaborators=collaborator,
    )


@click.command(cls=AlbumDirCommand)
@single_track_options()
def show(state, track_name, artist, album):
    """Show information about a track."""
    _track = state.wilder.get_track(track_name, album, artist_name=artist)
    click.echo(_track.artist)
    click.echo(f'"{_track.name}"')
    click.echo(_track.album)
    if _track.description:
        click.echo(f'\n"{_track.description}"')


@click.command(cls=AlbumDirCommand)
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


@click.command(cls=AlbumDirCommand)
@single_track_options()
@yes_option
@hard_option
def delete(state, track_name, artist, album, hard):
    """Delete a track from an album."""
    _track = state.wilder.get_track(track_name, album, artist_name=artist)
    if does_user_agree(f"Are you sure you wish to delete '{track_name}'? "):
        state.wilder.delete_track(track_name, album, artist_name=artist, hard=hard)


@click.command(cls=AlbumDirCommand)
@track_options()
@click.option(
    "--auto", help="Set to skip interactive mode and set track numbers as a sequence."
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
        state.wilder.auto_set_track_numbers()


def _get_track_num_choices(track_names, choices, answer_dict=None):
    if not track_names or not choices:
        return answer_dict

    answer_dict = answer_dict or {}
    track_name = track_names.pop()
    question = {
        "type": "list",
        "name": "choice",
        "message": f"What do you want the track number for '{track_name}' to be?",
        "choices": choices,
    }
    ans = prompt(question)["choice"]
    answer_dict[track_name] = ans
    remaining_choices = tuple(filter(lambda i: i != ans, choices))
    return _get_track_num_choices(track_names, remaining_choices, answer_dict)


@click.command(cls=AlbumDirCommand)
@single_track_options()
@audio_type_option
def play(state, track_name, artist, album, audio_type):
    """Play a track."""
    state.wilder.play_track(
        track_name, album, artist_name=artist, audio_type=audio_type
    )


track.add_command(_list)
track.add_command(new)
track.add_command(show)
track.add_command(update)
track.add_command(delete)
track.add_command(reorder)
track.add_command(play)
