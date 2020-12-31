from wilder.constants import Constants


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

    @property
    def json(self):
        return {
            Constants.LAST_UPDATED: self.last_updated,
            Constants.ARTISTS: [a.json for a in self.artists],
            Constants.FOCUS_ARTIST: self.focus_artist,
        }
