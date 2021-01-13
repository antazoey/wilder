from wilder.constants import Constants
from wilder.models.album import Album


class Artist:
    # The name of the artist.
    name = None

    # The artist's biography.
    bio = None

    # All of the albums of the artist, including unreleased or in-progress.
    discography = []

    # Other names the artist is or has been known as.
    also_known_as = []

    def __init__(self, discography=None, name=None, bio=None, also_known_as=None):
        self.discography = discography or []
        self.name = name
        self.bio = bio
        self.also_known_as = also_known_as or []

    @classmethod
    def from_json(cls, artist_json):
        name = artist_json.get(Constants.NAME)
        bio = artist_json.get(Constants.BIO)
        also_known_as = artist_json.get(Constants.ALSO_KNOWN_AS)
        discography_json = artist_json.get(Constants.DISCOGRAPHY) or []
        discography = cls.parse_discography(name, discography_json)
        return cls(
            discography=discography, name=name, bio=bio, also_known_as=also_known_as
        )

    def to_json(self):
        return {
            Constants.NAME: self.name,
            Constants.BIO: self.bio,
            Constants.DISCOGRAPHY: [a.to_json() for a in self.discography],
            Constants.ALSO_KNOWN_AS: self.also_known_as,
        }

    def start_new_album(
        self, path_location, name=None, description=None, album_type=None, status=None
    ):
        name = name or self._get_default_album_name()
        album = Album(
            path_location,
            name=name,
            description=description,
            album_type=album_type,
            status=status,
        )
        self.discography.append(album)

    def get_album_by_name(self, name):
        for alb in self.discography:
            if alb.name == name:
                return alb
        return None

    def _get_default_album_name(self):
        album_number = len(self.discography) + 1
        return f"{self.name} {album_number}"

    @classmethod
    def parse_discography(cls, artist_name, disco_json):
        return [Album.from_json(artist_name, album_json) for album_json in disco_json]
