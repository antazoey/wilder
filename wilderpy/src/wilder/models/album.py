from wilder.constants import ARTWORK
from wilder.constants import DESCRIPTION
from wilder.constants import NAME
from wilder.constants import TRACKS


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

    @property
    def json(self):
        return {
            NAME: self.name,
            DESCRIPTION: self.description,
            ARTWORK: self.artwork,
            TRACKS: [t.json for t in self.tracks],
        }
