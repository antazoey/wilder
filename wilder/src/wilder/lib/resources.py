import json
import os

# This module is for accessing default Wilder resources for creating albums.


def get_resources_path():
    here = os.path.dirname(os.path.abspath(__file__))
    return os.path.join(here, "resources")


def get_artwork_path():
    resources_path = get_resources_path()
    return os.path.join(resources_path, "artwork.png")


def get_album_json_path():
    resources_path = get_resources_path()
    return os.path.join(resources_path, "album.json")


def get_default_album_json():
    album_path = get_album_json_path()
    from wilder.lib.util.sh import wopen

    with wopen(album_path) as album_file:
        return json.load(album_file) or {}
