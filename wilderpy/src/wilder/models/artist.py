from wilder.constants import Constants
from wilder.models import Album


class Artist:
    name = None
    bio = None

    # Relational
    discography = []

    def __init__(self, name=None, bio=None):
        self.name = name
        self.bio = bio

    @property
    def json(self):
        return {
            Constants.NAME: self.name,
            Constants.BIO: self.bio,
            Constants.DISCOGRAPHY: [a.json for a in self.discography],
        }

    def start_new_album(self, name=None):
        name = name or self._get_default_album_name()
        album = Album(name)
        self.discography.append(album)

    def _get_default_album_name(self):
        album_count = len(self.discography)
        return f"{self.name} {album_count}"
