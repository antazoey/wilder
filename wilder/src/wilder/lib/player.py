import time

import vlc
from wilder.lib.errors import WildVLCPlayerLaunchError


def play_track(track_path):
    player = vlc.MediaPlayer()
    media = vlc.Media(track_path)
    player.set_media(media)

    cmd_res = player.play()
    if cmd_res == -1:
        raise WildVLCPlayerLaunchError()

    start = 1
    time.sleep(start)
    track_length = player.get_length() * 0.001

    remaining = track_length - start
    while remaining > 0:
        wait_time = 0.1
        yield remaining
        time.sleep(wait_time)
        remaining -= wait_time
