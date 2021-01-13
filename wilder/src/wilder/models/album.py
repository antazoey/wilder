from wilder.constants import Constants
from wilder.models.release import Release
from wilder.models.track import Track


class Album:
    # The path on the local machine for where the album got initialized.
    path = None

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

    # The status of the album, such as RELEASED.
    status = None

    def __init__(self, path, name=None, description=None, album_type=None, status=None):
        self.path = path
        self.name = name
        self.description = description
        self.album_type = album_type
        self.status = status

    @classmethod
    def from_json(cls, artist_name, album_json):
        path = album_json.get(Constants.PATH)
        album = cls(path)
        album.artist = artist_name
        album.name = album_json.get(Constants.NAME)
        album.description = album_json.get(Constants.DESCRIPTION)
        album.artwork = album_json.get(Constants.ARTWORK)
        album.album_type = album_json.get(Constants.ALBUM_TYPE)
        album.status = album_json.get(Constants.STATUS)
        tracks = album_json.get(Constants.TRACKS) or []
        album.tracks = cls.parse_tracks(artist_name, album.name, tracks)
        releases = album_json.get(Constants.RELEASES)
        album.releases = cls.parse_releases(artist_name, album.name, releases)
        return album

    def to_json(self):
        return {
            Constants.NAME: self.name,
            Constants.PATH: self.path,
            Constants.DESCRIPTION: self.description,
            Constants.ARTWORK: self.artwork,
            Constants.ALBUM_TYPE: self.album_type,
            Constants.STATUS: self.status,
            Constants.TRACKS: [t.to_json() for t in self.tracks],
            Constants.RELEASES: [r.to_json() for r in self.releases],
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

    def get_track(self, name):
        for track in self.tracks:
            if track.name == name:
                return track
