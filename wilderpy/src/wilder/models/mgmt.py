from wilder.constants import Constants


class Mgmt:
    artists = []

    def __init__(self, artists, last_updated=None):
        self.artists = artists
        self.last_updated = last_updated

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
    def artists_json(self):
        return self.json.get(Constants.ARTISTS) or []

    @property
    def json(self):
        return {Constants.ARTISTS: [a.json for a in self.artists]}
