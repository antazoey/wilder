import json

from wilder.constants import Constants
from wilder.models.release import Release
from wilder.models.track import Track
from wilder.util.shellutil import create_dir_if_not_exists
from wilder.util.shellutil import copy_files_to_dir
from wilder.util.shellutil import wopen
from wilder.util.shellutil import remove_file_if_exists
from wilder.util.resources import get_artwork_path
from wilder.util.resources import get_album_json_path


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
    
    def init_dir(self):
        create_dir_if_not_exists(self.path)
        artwork_path = get_artwork_path()
        album_json_path = get_album_json_path()
        copy_files_to_dir([artwork_path, album_json_path], self.path)

    @classmethod
    def from_json(cls, artist_name, album_json):
        path = album_json.get(Constants.PATH)
        album = cls(path)
        album.artist = artist_name
        album.name = album_json.get(Constants.NAME)
        cls._set_from_dir_json(artist_name)
        return album
    
    @classmethod
    def _set_from_dir_json(cls, artist_name):
        album_dir_json = get_album_json()
        cls.description = album_dir_json.get(Constants.DESCRIPTION)      
        cls.artwork = album_dir_json.get(Constants.ARTWORK)
        cls.album_type = album_dir_json.get(Constants.ALBUM_TYPE)
        cls.status = album_dir_json.get(Constants.STATUS)
        tracks = album_dir_json.get(Constants.TRACKS) or []
        cls.tracks = cls.parse_tracks(artist_name, cls.name, tracks)
        releases = album_dir_json.get(Constants.RELEASES)
        cls.releases = cls.parse_releases(artist_name, cls.name, releases)
        return cls

    def to_json_for_album_dir(self):
        return {
            Constants.ARTIST: self.artist,
            Constants.NAME: self.name,
            Constants.PATH: self.path,
            Constants.DESCRIPTION: self.description,
            Constants.ARTWORK: self.artwork,
            Constants.ALBUM_TYPE: self.album_type,
            Constants.STATUS: self.status,
            Constants.TRACKS: [t.to_json() for t in self.tracks],
            Constants.RELEASES: [r.to_json() for r in self.releases],
        }
    
    def to_json_for_mgmt(self):
        return {
            Constants.ARTIST: self.artist,
            Constants.PATH: self.path
        }
    
    def save_album_metadata(self):
        album_path = get_album_json_path()
        remove_file_if_exists(album_path)
        album_json = self.to_json_for_album_dir()
        with wopen(album_path, "w") as album_file:
            album_file.write(album_json)

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


def get_track_path(album, track_name):
    track_path = f"{album.path}/{track_name}"
    create_dir_if_not_exists(track_path)
    return track_path


def get_album_json():
    album_path = get_album_json_path()
    with wopen(album_path) as album_file:
        return json.load(album_file)
    return {}
