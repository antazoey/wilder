import json
import os

import click
from wilder.lib.constants import Constants
from wilder.lib.resources import get_artwork_path
from wilder.lib.resources import get_default_album_json
from wilder.lib.util.sh import copy_files_to_dir
from wilder.lib.util.sh import create_dir_if_not_exists
from wilder.lib.util.sh import file_exists_with_data
from wilder.lib.util.sh import load_json_from_file
from wilder.lib.util.sh import wopen


def get_track_path(album, track_name):
    track_path = os.path.join(album.path, track_name)
    create_dir_if_not_exists(track_path)
    return track_path


def get_track_json_path(album, track_name):
    track_path = get_track_path(album, track_name)
    return os.path.join(track_path, "track.json")


def get_album_dir_json_path(album_path):
    return os.path.join(album_path, "album.json")


def get_album_dir_json(album_path, album_name):
    if not os.path.exists(album_path):
        init_dir(album_path, album_name)
    album_data_file_path = get_album_dir_json_path(album_path)

    if not file_exists_with_data(album_data_file_path):
        _init_album_json(album_path, album_name)

    return load_json_from_file(album_data_file_path)


def init_dir(album_path, album_name):
    create_dir_if_not_exists(album_path)
    _init_artwork(album_path)
    _init_album_json(album_path, album_name)


def _init_artwork(album_path):
    create_dir_if_not_exists(album_path)
    artwork_path = get_artwork_path()
    copy_files_to_dir(artwork_path, album_path)


def _init_album_json(album_path, album_name):
    create_dir_if_not_exists(album_path)
    _json = get_default_album_json()
    _json[Constants.NAME] = album_name
    album_json_path = get_album_dir_json_path(album_path)
    json_text = json.dumps(_json, indent=2)
    with wopen(album_json_path, "w") as album_json_file:
        album_json_file.write(json_text)


def echo_tracks(tracks):
    for track in tracks:
        click.echo(f"{track.track_number}. {track.name}")
