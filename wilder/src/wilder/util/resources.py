import os
from pathlib import Path


def get_resources_path():
    here = Path(os.path.dirname(os.path.abspath(__file__)))
    return os.path.join(here.parent, "resources")


def get_artwork_path():
    resources_path = get_resources_path()
    return os.path.join(resources_path, "artwork.png")


def get_album_json_path():
    resources_path = get_resources_path()
    return os.path.join(resources_path, "album.json")
