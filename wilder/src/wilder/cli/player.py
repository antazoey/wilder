from datetime import timedelta

import click
from wilder.lib.util.sh import BEGIN_OF_PREVIOUS_LINE
from wilder.lib.util.sh import count_lines


def play_album(wilder, album, start_track, audio_type=None):
    tracks = album.get_tracks()
    start_index = _get_index_of_track(start_track, tracks)

    def play_track_at_index(index):
        track = tracks[index]
        for time_remaining in wilder.play_track(
            track.name, track.album, audio_type=audio_type, artist_name=track.artist
        ):
            text = _get_album_player_text(album, index, time_remaining)
            number_of_lines = count_lines(text)
            print(f" {text}", end=f"{number_of_lines * BEGIN_OF_PREVIOUS_LINE}")
        next_index = (index + 1) % len(tracks)

        play_track_at_index(next_index)

    play_track_at_index(start_index)


def _get_index_of_track(track, tracks):
    for index in range(0, len(tracks)):
        track_to_check = tracks[index]
        if track_to_check.name == track.name:
            return index


def _get_album_player_text(album, now_playing_index, time_remaining):
    tracks = album.get_tracks()
    album_text = f"'{album.name}' by '{album.artist}'\n\n"
    for index in range(0, len(tracks)):
        track = tracks[index]
        track_text = f"{track.track_number}. {track.name}"
        if index == now_playing_index:
            prefix = ">"
            spaces = " " * 9
            time_remaining_text = _format_time_remaining(time_remaining)
            track_text += f"{spaces}{time_remaining_text}"
        else:
            prefix = " "
            trailing_spaces = " " * 16  # Clears previous 'time remaining' text
            track_text += f"{trailing_spaces}"
        album_text += f"{prefix}{track_text}\n"
    return album_text


def play_track(wilder, track, audio_type=None):
    header = f"'{track.name}' by '{track.artist}'"
    click.echo(header)
    for time_remaining in wilder.play_track(
        track.name, track.album, audio_type=audio_type, artist_name=track.artist
    ):
        time_remaining_text = _format_time_remaining(time_remaining)
        print(f" {time_remaining_text}", end="\r")


def _format_time_remaining(time_remaining):
    time_delta = timedelta(seconds=round(time_remaining))
    return f"{str(time_delta)}"
