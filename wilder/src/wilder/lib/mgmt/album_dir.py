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
from wilder.lib.util.sh import get_parent
from wilder.lib.util.sh import load_json_from_file
from wilder.lib.util.sh import save_json_as


def get_album_json_path(album_path):
    if not album_path:
        return None
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


def get_album_directory(wilder, get_default_handler=None):
    return AlbumDirectory(wilder, get_default_handler=get_default_handler)


class AlbumDirectory:
    def __init__(self, wilder, get_default_handler=None):
        self.wilder = wilder
        self._get_default = get_default_handler

    def get_album_json(self, artist_arg, album_arg):
        """Get the album directory JSON blob. If given an album name, it uses the Wilder SDK.
        Otherwise, it attempts to figure out the artist/album combo based on the currently working
        directory.

        Cases:
            * You provide the album arg: It uses the Wilder SDK to find the path to the album to get the rest of the data.
            * You are in the album directory: It uses the local album.json file.
            * You are in the album directory and the album.json does not exist: It recreates the default JSON and uses that.
            * You are in a track directory of an album. It uses the parent album.json file if it exists.
            * You are in a track directory of an album and the album.json does not exist in the parent directorY: It will
                create the default album JSON in the parent directory and use that.
            * You provide a handler for getting the default Album Directory. An example would be to allow the user to
                select from a list.
        """

        if not album_arg:
            try:
                album_json = _try_get_local_json()
                if not album_json:
                    return self._handle_could_not_find()
                return album_json
            except OSError:
                # Handles case when in a strange directory
                return self._handle_could_not_find()
        else:
            album = self.wilder.get_album(album_arg, artist_name=artist_arg)
            return load_json_from_file(album.dir_json_path)

    def _handle_could_not_find(self):
        if self._get_default:
            return self._get_default()
        return self._handle_could_not_find()


def _get_album_json_from_here(here=None):
    here = here or os.getcwd()
    album_json_path = get_album_json_path(here)
    album_json = _get_album_json_from_path(album_json_path)
    return album_json_path, album_json


def _album_is_supposed_to_exist(here=None):
    mgmt_json = get_mgmt_json()
    artists = mgmt_json.get(Constants.ARTISTS)
    here = here or os.getcwd()
    for artist in artists:
        albums = artist.get(Constants.DISCOGRAPHY)
        for album in albums:
            path = album.get(Constants.PATH)
            name = album.get(Constants.NAME)
            if path == here:
                return name


def _create_album_if_should_exist(album_json_path, here=None):
    here = here or os.getcwd()
    name = _album_is_supposed_to_exist(here=here)
    if name:
        init_album_dir(here, name)
        return load_json_from_file(album_json_path)


def _try_get_local_json():
    album_json_path, album_json = _get_album_json_from_here()
    if album_json:
        return album_json

    local_json = _create_album_if_should_exist(album_json_path)
    if local_json:
        return local_json

    return _try_get_local_json_from_parent_dir()


def _get_album_json_from_path(path):
    if os.path.isfile(path):
        return load_json_from_file(path)


def _try_get_local_json_from_parent_dir(here=None):
    here = here or os.getcwd()
    here = get_parent(here)
    album_json_path, album_json = _get_album_json_from_here(here=here)
    if album_json:
        return album_json
    return _create_album_if_should_exist(album_json_path)
