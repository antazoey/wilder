import vlc


def play_album(album):
    for track in album.tracks:
        play_track(track)


def play_track(track):
    player = _create_player(track)


def _create_player(song_path):
    return vlc.MediaPlayer(song_path)
