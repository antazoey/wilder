import json
import os
from datetime import datetime

from wilder.constants import ALBUM_TYPE
from wilder.constants import ARTISTS
from wilder.constants import ARTWORK
from wilder.constants import BIO
from wilder.constants import COLLABORATORS
from wilder.constants import DESCRIPTION
from wilder.constants import DISCOGRAPHY
from wilder.constants import LAST_UPDATED
from wilder.constants import NAME
from wilder.constants import STATE
from wilder.constants import TRACK_NUMBER
from wilder.constants import TRACKS
from wilder.models import Album
from wilder.models import Artist
from wilder.models import Mgmt
from wilder.models import Release
from wilder.models import Track
from wilder.util import get_mgmt_json
from wilder.util import get_mgmt_json_path


def parse_mgmt(mgmt_json=None):
    # Parses the given mgmt json.
    # Give it a path to a JSON file to parse that file.
    # Give it None (or no arg) to parse the user config file.
    # Give it the raw dict to just use that.

    if mgmt_json is None or isinstance(mgmt_json, str):
        mgmt_json = get_mgmt_json(mgmt_path=mgmt_json)
    artists = parse_artists(mgmt_json)
    return Mgmt(artists, last_updated=mgmt_json.get(LAST_UPDATED))


def parse_artists(json_data):
    objs = []
    artists = json_data.get(ARTISTS) or []
    for a in artists:
        artist = Artist()
        artist.name = a.get(NAME)
        artist.bio = a.get(BIO)
        discography = a.get(DISCOGRAPHY) or []
        artist.discography = parse_albums(artist, discography)
        objs.append(artist)
    return objs


def parse_albums(artist, albums):
    objs = []
    for a in albums:
        album = Album()
        album.artist = artist
        album.name = a.get(NAME)
        album.description = a.get(DESCRIPTION)
        album.artwork = a.get(ARTWORK)
        album.album_type = a.get(ALBUM_TYPE)
        album.state = a.get(STATE)
        tracks = a.get(TRACKS) or []
        album.tracks = parse_tracks(artist, album, tracks)
        objs.append(album)
    return objs


def parse_tracks(artist, album, tracks):
    objs = []
    for t in tracks:
        track = Track()
        track.artist = artist
        track.album = album
        track.name = t.get(NAME)
        track.description = t.get(DESCRIPTION)
        track.track_number = t.get(TRACK_NUMBER)
        track.collaborators = t.get(COLLABORATORS)
        objs.append(track)
    return objs


def parse_releases(artist, album, releases):
    objs = []
    for r in releases:
        release = Release()
        release.date = r.get("date")
        release.release_type = r.get("releaseType")
        release.artist = artist
        release.album = album
        objs.append(release)
    return objs


def save(mgmt_json_dict):
    """Save a MGMT dictionary to the mgmt.json file."""
    mgmt_json_dict[LAST_UPDATED] = datetime.utcnow().timestamp()
    mgmt_json = json.dumps(mgmt_json_dict)
    mgmt_path = get_mgmt_json_path()
    os.remove(mgmt_path)
    print(mgmt_json)
    with open(mgmt_path, "w") as mgmt_file:
        mgmt_file.write(mgmt_json)
