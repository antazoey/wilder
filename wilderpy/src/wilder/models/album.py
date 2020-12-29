from wilder.constants import Constants


class Album:
    name = None
    description = None
    artwork = None

    # Relational
    artist = None
    tracks = []
    releases = []
    album_type = None
    state = None

    def __init__(self, name=None):
        self.name = name

    @property
    def json(self):
        return {
            Constants.NAME: self.name,
            Constants.DESCRIPTION: self.description,
            Constants.ARTWORK: self.artwork,
            Constants.TRACKS: [t.json for t in self.tracks],
        }
