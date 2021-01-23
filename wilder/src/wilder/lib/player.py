import vlc


def play_album(album, audio_type):
    for track in album.tracks:
        path = track.get_file(audio_type)
        play_track(path)


def play_track(track_path):
    player = vlc.MediaPlayer(track_path)
    player.play()
