from wilder.constants import Constants
from wilder.models.artist import Artist
from wilder.util.user import get_mgmt_json


class Mgmt:
    artists = []
    last_updated = None
    focus_artist = None

    def __init__(self, artists, last_updated=None, focus_artist=None):
        self.artists = artists
        self.last_updated = last_updated
        self.focus_artist = focus_artist

    def __getitem__(self, item):
        return self.get_artist_by_name(item)

    def __delitem__(self, key):
        artist = self.get_artist_by_name(key)
        if artist:
            self.artists.remove(artist)

    def get_artist_by_name(self, name):
        for artist in self.artists:
            if artist.name == name:
                return artist
        return None

    @classmethod
    def from_json(cls, mgmt_json):
        if mgmt_json is None or isinstance(mgmt_json, str):
            mgmt_json = get_mgmt_json()
        last_updated = mgmt_json.get(Constants.LAST_UPDATED)
        focus_artist = mgmt_json.get(Constants.FOCUS_ARTIST)
        artists = cls.parse_artists(mgmt_json)
        return cls(artists, last_updated=last_updated, focus_artist=focus_artist)

    def to_json(self):
        return {
            Constants.LAST_UPDATED: self.last_updated,
            Constants.ARTISTS: [a.to_json() for a in self.artists],
            Constants.FOCUS_ARTIST: self.focus_artist,
        }

    @classmethod
    def parse_artists(cls, mgmt_json):
        artists = mgmt_json.get(Constants.ARTISTS) or []
        return [Artist.from_json(a) for a in artists]
