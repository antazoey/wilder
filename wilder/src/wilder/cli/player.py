from datetime import timedelta

import click


def play_album(wilder, album, start_track, audio_type=None):
    header = f"'{album.name}' by '{album.artist}'\n\n"
    tracks = album.get_tracks()
    for track in tracks:
        header += f"{track.track_number}. {track.name}"
        if track.name == start_track.name:
            header += " (now playing)"
        header += "\n"
    click.echo(header)
    # TODO: MAKE WORK WITH START AND LOOPING ETC asdfasdfgasd
    # for track in tracks:
    #     play_track(wilder, track, audio_type=audio_type)


def play_track(wilder, track, audio_type=None):
    header = f"'{track.name}' by '{track.artist}'"
    click.echo(header)
    for time_remaining in wilder.play_track(
        track.name, track.album, audio_type=audio_type, artist_name=track.artist
    ):
        time_delta = timedelta(seconds=round(time_remaining))
        print(f" {str(time_delta)}", end="\r")
