import json
import os

from wilder.lib.constants import Constants
from wilder.lib.enum import AlbumStatus
from wilder.lib.mgmt.album_dir import get_album_dir_json
from wilder.lib.mgmt.album_dir import get_album_dir_json_path
from wilder.lib.mgmt.album_dir import init_dir
from wilder.lib.mgmt.release import Release
from wilder.lib.mgmt.track import Track
from wilder.lib.util.sh import remove_file_if_exists
from wilder.lib.util.sh import wopen


class Album:
    def __init__(
        self,
        path,
        name,
        artist=None,
        description=None,
        album_type=None,
        status=None,
        tracks=None,
        releases=None,
    ):
        self.path = path
        self.name = name
        self.artist = artist
        self.description = description
        self.album_type = album_type
        self.status = status
        self.tracks = tracks
        self.releases = releases

    def init_dir(self):
        init_dir(self.path, self.name)

    @classmethod
    def from_json(cls, artist_name, album_json):
        """Create the Artist object from data from .wilder/mgmt.json."""
        path = album_json.get(Constants.PATH)
        name = album_json.get(Constants.NAME)
        album_dir_json = get_album_dir_json(path, name)
        description = album_dir_json.get(Constants.DESCRIPTION, "")
        album_type = album_dir_json.get(Constants.ALBUM_TYPE)
        status = album_dir_json.get(Constants.STATUS, AlbumStatus.IN_PROGRESS)
        tracks = album_dir_json.get(Constants.TRACKS, [])
        tracks = _parse_tracks(artist_name, name, tracks)
        releases = album_dir_json.get(Constants.RELEASES)
        releases = _parse_releases(artist_name, name, releases)
        album = cls(
            path,
            name,
            artist=artist_name,
            description=description,
            album_type=album_type,
            status=status,
            tracks=tracks,
            releases=releases,
        )
        album.save_album_metadata()
        return album

    @property
    def dir_json_path(self):
        return get_album_dir_json_path(self.path)

    def to_full_json(self):
        return {
            Constants.ARTIST: self.artist,
            Constants.NAME: self.name,
            Constants.PATH: self.path,
            Constants.DESCRIPTION: self.description,
            Constants.ALBUM_TYPE: self.album_type,
            Constants.STATUS: self.status,
            Constants.TRACKS: [t.to_json() for t in self.tracks],
            Constants.RELEASES: [r.to_json() for r in self.releases],
        }

    def to_json_for_mgmt(self):
        # Figure out name if path is set but name for some reason isn't
        if not self.name and self.path:
            self.name = os.path.basename(os.path.normpath(self.path))
            self.save_album_metadata()

        return {Constants.ALBUM: self.name, Constants.PATH: self.path}

    def save_album_metadata(self):
        remove_file_if_exists(self.dir_json_path)
        full_json = self.to_full_json()
        album_text = json.dumps(full_json, indent=2)
        with wopen(self.dir_json_path, "w") as album_file:
            album_file.write(album_text)

    def get_track(self, name):
        for track in self.tracks:
            if track.name == name:
                return track


def _parse_tracks(artist_name, album_name, tracks_json):
    return [Track.from_json(artist_name, album_name, t) for t in tracks_json]


def _parse_releases(artist_name, album_name, releases_json):
    return [
        Release.from_json(artist_name, album_name, release_json)
        for release_json in releases_json
    ]
