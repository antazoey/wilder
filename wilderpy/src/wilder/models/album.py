from wilder.constants import Constants
from wilder.models.release import Release
from wilder.models.track import Track


class Album:
    # The name of the album
    name = None

    # Some descriptive information about the album.
    description = None

    # The name of the artwork file for the album
    artwork = None

    # The artist name who made the album.
    artist = None

    # The tracks on the album.
    tracks = []

    # Different releases the album has had.
    releases = []

    # The type of the album, such as GREATEST_HIST.
    album_type = None

    # The state of the album, such as RELEASED.
    state = None

    def __init__(self, name=None):
        self.name = name

    @classmethod
    def from_json(cls, artist_name, album_json):
        album = cls()
        album.artist = artist_name
        album.name = album_json.get(Constants.NAME)
        album.description = album_json.get(Constants.DESCRIPTION)
        album.artwork = album_json.get(Constants.ARTWORK)
        album.album_type = album_json.get(Constants.ALBUM_TYPE)
        album.state = album_json.get(Constants.STATE)
        tracks = album_json.get(Constants.TRACKS) or []
        album.tracks = cls.parse_tracks(artist_name, album.name, tracks)
        releases = album_json.get(Constants.RELEASES)
        album.releases = cls.parse_releases(artist_name, album.name, releases)
        return album

    def to_json(self):
        return {
            Constants.NAME: self.name,
            Constants.DESCRIPTION: self.description,
            Constants.ARTWORK: self.artwork,
            Constants.TRACKS: [t.to_json() for t in self.tracks],
        }

    @classmethod
    def parse_tracks(cls, artist_name, album_name, tracks_json):
        return [Track.from_json(artist_name, album_name, t) for t in tracks_json]

    @classmethod
    def parse_releases(cls, artist_name, album_name, releases_json):
        return [
            Release.from_json(artist_name, album_name, release_json)
            for release_json in releases_json
        ]
