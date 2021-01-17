import json
import os

from wilder.lib.constants import Constants
from wilder.lib.mgmt.release import Release
from wilder.lib.mgmt.track import Track
from wilder.lib.resources import get_artwork_path
from wilder.lib.resources import get_default_album_json
from wilder.lib.util.sh import copy_files_to_dir
from wilder.lib.util.sh import create_dir_if_not_exists
from wilder.lib.util.sh import remove_file_if_exists
from wilder.lib.util.sh import wopen


class Album:
    tracks = []
    releases = []

    def __init__(
        self,
        path,
        name=None,
        description=None,
        album_type=None,
        status=None,
        artist=None,
    ):
        self.path = path
        self.name = name
        self.description = description
        self.album_type = album_type
        self.status = status
        self.artist = artist

    def init_dir(self):
        create_dir_if_not_exists(self.path)
        self._init_artwork()
        self._init_album_json()

    def _init_artwork(self):
        create_dir_if_not_exists(self.path)
        artwork_path = get_artwork_path()
        copy_files_to_dir(artwork_path, self.path)

    def _init_album_json(self):
        create_dir_if_not_exists(self.path)
        _json = get_default_album_json()
        _json[Constants.NAME] = self.name
        album_json_path = self._get_dir_json_path()
        json_text = json.dumps(_json, indent=2)
        with wopen(album_json_path, "w") as album_json_file:
            album_json_file.write(json_text)

    @classmethod
    def from_json(cls, artist_name, album_json):
        path = album_json.get(Constants.PATH)
        album = cls(path)
        album.artist = artist_name
        album.name = album_json.get(Constants.NAME)
        album._set_from_dir_json(artist_name)
        album.save_album_metadata()
        return album

    def _set_from_dir_json(self, artist_name):
        # Requires self.name to already be set.
        album_dir_json = self._get_dir_json()
        self.description = album_dir_json.get(Constants.DESCRIPTION)
        self.artwork = album_dir_json.get(Constants.ARTWORK)
        self.album_type = album_dir_json.get(Constants.ALBUM_TYPE)
        self.status = album_dir_json.get(Constants.STATUS)
        tracks = album_dir_json.get(Constants.TRACKS) or []
        self.tracks = _parse_tracks(artist_name, self.name, tracks)
        releases = album_dir_json.get(Constants.RELEASES)
        self.releases = _parse_releases(artist_name, self.name, releases)

    def _get_dir_json_path(self):
        return os.path.join(self.path, "album.json")

    def _get_dir_json(self):
        if not os.path.exists(self.path):
            self.init_dir()
        album_data_file_path = self._get_dir_json_path()
        if (
            not os.path.isfile(album_data_file_path)
            or not os.path.getsize(album_data_file_path)
        ):
            self.init_dir()

        with wopen(album_data_file_path) as local_json_file:
            return json.load(local_json_file)

    def to_full_json(self):
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
        # Figure out name if path is set
        if not self.name and self.path:
            self.name = os.path.basename(os.path.normpath(self.path))
            self.save_album_metadata()

        return {Constants.ALBUM: self.name, Constants.PATH: self.path}

    def save_album_metadata(self):
        album_path = self._get_dir_json_path()
        remove_file_if_exists(album_path)
        full_json = self.to_full_json()
        album_text = json.dumps(full_json, indent=2)
        with wopen(album_path, "w") as album_file:
            album_file.write(album_text)

    def get_track(self, name):
        for track in self.tracks:
            if track.name == name:
                return track


def _get_track_path(album, track_name):
    track_path = f"{album.path}/{track_name}"
    create_dir_if_not_exists(track_path)
    return track_path


def _parse_tracks(artist_name, album_name, tracks_json):
    return [Track.from_json(artist_name, album_name, t) for t in tracks_json]


def _parse_releases(artist_name, album_name, releases_json):
    return [
        Release.from_json(artist_name, album_name, release_json)
        for release_json in releases_json
    ]
