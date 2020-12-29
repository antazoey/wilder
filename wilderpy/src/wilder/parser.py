import json
import os
from datetime import datetime

from wilder.constants import Constants as Consts
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
    return Mgmt(artists, last_updated=mgmt_json.get(Consts.LAST_UPDATED))


def parse_artists(json_data):
    objs = []
    artists = json_data.get(Consts.ARTISTS) or []
    for a in artists:
        artist = Artist()
        artist.name = a.get(Consts.NAME)
        artist.bio = a.get(Consts.BIO)
        discography = a.get(Consts.DISCOGRAPHY) or []
        artist.discography = parse_albums(artist, discography)
        objs.append(artist)
    return objs


def parse_albums(artist, albums):
    objs = []
    for a in albums:
        album = Album()
        album.artist = artist
        album.name = a.get(Consts.NAME)
        album.description = a.get(Consts.DESCRIPTION)
        album.artwork = a.get(Consts.ARTWORK)
        album.album_type = a.get(Consts.ALBUM_TYPE)
        album.state = a.get(Consts.STATE)
        tracks = a.get(Consts.TRACKS) or []
        album.tracks = parse_tracks(artist, album, tracks)
        objs.append(album)
    return objs


def parse_tracks(artist, album, tracks):
    objs = []
    for t in tracks:
        track = Track()
        track.artist = artist
        track.album = album
        track.name = t.get(Consts.NAME)
        track.description = t.get(Consts.DESCRIPTION)
        track.track_number = t.get(Consts.TRACK_NUMBER)
        track.collaborators = t.get(Consts.COLLABORATORS)
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
    mgmt_json_dict[Consts.LAST_UPDATED] = datetime.utcnow().timestamp()
    mgmt_json = json.dumps(mgmt_json_dict)
    mgmt_path = get_mgmt_json_path()
    os.remove(mgmt_path)
    print(mgmt_json)
    with open(mgmt_path, "w") as mgmt_file:
        mgmt_file.write(mgmt_json)
