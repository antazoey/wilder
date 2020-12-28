from wilderpy.models import Album
from wilderpy.models import Artist
from wilderpy.models import Mgmt
from wilderpy.models import Track
from wilderpy.util import get_mgmt_json


def parse_mgmt():
    mgmt_json = get_mgmt_json()
    artists = _parse_artists(mgmt_json)
    mgmt = Mgmt(artists)
    return mgmt


def _parse_artists(json_data):
    objs = []
    artists = json_data.get("artists") or []
    for a in artists:
        artist = Artist()
        artist.name = a.get("name")
        artist.bio = a.get("bio")
        albums = a.get("albums") or []
        artist.discography = _parse_albums(artist, albums)
        objs.append(artist)
    return objs


def _parse_albums(artist, albums):
    objs = []
    for a in albums:
        album = Album()
        album.artist = artist
        album.name = a.get("name")
        album.description = a.get("description")
        album.artwork = a.get("artwork")
        tracks = a.get("tracks") or []
        album.tracks = _parse_tracks(artist, album, tracks)
    return objs


def _parse_tracks(artist, album, tracks):
    objs = []
    for t in tracks:
        track = Track()
        track.artist = artist
        tracks.album = album
        track.name = t.get("name")
        track.description = t.get("description")
        track.track_number = t.get("trackNumber")
    return objs
