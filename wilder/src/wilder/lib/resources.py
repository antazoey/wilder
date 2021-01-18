import json
import os

from wilder.lib.util.sh import get_file_dir
from wilder.lib.util.sh import wopen

# This module is for accessing default Wilder resources for creating albums.


def get_resources_path():
    here = get_file_dir(__file__)
    return os.path.join(here, "resources")


def get_artwork_path():
    return _get_resource_path("artwork.png")


def get_album_json_path():
    return _get_resource_path("album.json")


def get_track_json_path():
    return _get_resource_path("track.json")


def _get_resource_path(name):
    resources_path = get_resources_path()
    return os.path.join(resources_path, name)


def get_default_album_json():
    album_path = get_album_json_path()
    return _get_default_json(album_path)


def get_default_track_json():
    track_path = get_track_json_path()
    return _get_default_json(track_path)


def _get_default_json(path):
    with wopen(path) as json_file:
        return json.load(json_file) or {}
