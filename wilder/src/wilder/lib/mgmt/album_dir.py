import os

import click
from wilder.lib.constants import Constants
from wilder.lib.errors import NotInAlbumError
from wilder.lib.resources import get_artwork_path
from wilder.lib.resources import get_default_album_json
from wilder.lib.resources import get_default_track_json
from wilder.lib.user import get_mgmt_json
from wilder.lib.util.sh import copy_files_to_dir
from wilder.lib.util.sh import create_dir_if_not_exists
from wilder.lib.util.sh import file_exists_with_data
from wilder.lib.util.sh import load_json_from_file
from wilder.lib.util.sh import save_json_as


def get_album_json_path(album_path):
    return os.path.join(album_path, "album.json")


def get_album_dir_json(album_path, album_name):
    if not os.path.exists(album_path):
        init_album_dir(album_path, album_name)
    album_json_file_path = get_album_json_path(album_path)

    if not file_exists_with_data(album_json_file_path):
        _init_album_json(album_path, album_name)

    return load_json_from_file(album_json_file_path)


def init_album_dir(album_path, album_name):
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
    album_json_path = get_album_json_path(album_path)
    save_json_as(album_json_path, _json)


def get_track_path(album_path, track_name):
    track_path = os.path.join(album_path, track_name)
    create_dir_if_not_exists(track_path)
    return track_path


def get_track_json_path(track_path):
    return os.path.join(track_path, "track.json")


def get_track_dir_json(track_path, track_name, artist_name, album_name):
    if not os.path.exists(track_path):
        init_track_dir(track_path, track_name, artist_name, album_name)

    track_json_file_path = get_track_json_path(track_path)

    if not file_exists_with_data(track_json_file_path):
        _init_track_json(track_path, track_name, artist_name, album_name)

    return load_json_from_file(track_json_file_path)


def init_track_dir(track_path, track_name, artist_name, album_name):
    create_dir_if_not_exists(track_path)
    _init_track_json(track_path, track_name, artist_name, album_name)


def _init_track_json(track_path, track_name, artist_name, album_name):
    create_dir_if_not_exists(track_path)
    _json = get_default_track_json()
    _json[Constants.NAME] = track_name
    _json[Constants.ARTIST] = artist_name
    _json[Constants.ALBUM] = album_name
    track_json_path = get_track_json_path(track_path)
    save_json_as(track_json_path, _json)


def echo_tracks(tracks):
    for track in tracks:
        click.echo(f"{track.track_number}. {track.name}")


def get_album_json(wilder, artist_arg, album_arg):
    if not album_arg:
        try:
            here = os.getcwd()
            album_json_path = get_album_json_path(here)
            if not os.path.isfile(album_json_path):
                mgmt_json = get_mgmt_json()
                artists = mgmt_json.get(Constants.ARTISTS)
                for artist in artists:
                    albums = artist.get(Constants.DISCOGRAPHY)
                    for album in albums:
                        path = album.get(Constants.PATH)
                        name = album.get(Constants.NAME)
                        if path == here:
                            # Turns out, we are actually in an album dir but someone deleted the JSON
                            init_album_dir(here, name)
                            return load_json_from_file(album_json_path)
                raise NotInAlbumError()
            return load_json_from_file(album_json_path)
        except OSError:
            # Handles case when in a strange directory
            raise NotInAlbumError()
    else:
        album = wilder.get_album(album_arg, artist_name=artist_arg)
        return load_json_from_file(album.dir_json_path)
