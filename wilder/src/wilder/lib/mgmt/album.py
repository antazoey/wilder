import json
import os

from wilder.lib.constants import Constants as Consts
from wilder.lib.enum import AlbumStatus
from wilder.lib.mgmt.album_dir import get_album_dir_json, get_track_path
from wilder.lib.mgmt.album_dir import get_album_json_path
from wilder.lib.mgmt.album_dir import init_album_dir
from wilder.lib.mgmt.release import Release
from wilder.lib.mgmt.track import Track
from wilder.lib.util.sh import remove_file_if_exists
from wilder.lib.util.sh import wopen


class Album:
    def __init__(
        self,
        path,
        name,
        artist,
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
        init_album_dir(self.path, self.name)

    @classmethod
    def from_json(cls, album_json, artist_name):
        """Create the Artist object from data from .wilder/mgmt.json."""
        path = album_json[Consts.PATH]
        name = album_json[Consts.NAME]
        album_json = get_album_dir_json(path, name)
        album = cls(
            path,
            name,
            artist=artist_name,
            description=album_json.get(Consts.DESCRIPTION, ""),
            album_type=album_json.get(Consts.ALBUM_TYPE),
            status=album_json.get(Consts.STATUS, AlbumStatus.IN_PROGRESS),
            tracks=_parse_tracks(album_json),
            releases=_parse_releases(artist_name, name, album_json),
        )
        return album.save_album_metadata()

    @property
    def dir_json_path(self):
        return get_album_json_path(self.path)

    def to_json_for_album_dir(self):
        """The JSON blob representing the artifact in the album's directory."""
        return {
            Consts.ARTIST: self.artist,
            Consts.NAME: self.name,
            Consts.PATH: self.path,
            Consts.DESCRIPTION: self.description,
            Consts.ALBUM_TYPE: self.album_type,
            Consts.STATUS: self.status,
            Consts.TRACKS: [t.name for t in self.tracks],
            Consts.RELEASES: [r.to_json() for r in self.releases],
        }

    def to_json_for_mgmt(self):
        # Figure out name if path is set but name for some reason isn't
        if not self.name and self.path:
            self.name = os.path.basename(os.path.normpath(self.path))
            self.save_album_metadata()

        return {Consts.NAME: self.name, Consts.PATH: self.path}

    def update(self, description=None, album_type=None, status=None):
        self.description = description or self.description
        self.album_type = album_type or self.album_type
        self.status = status or self.status
        self.save_album_metadata()

    def start_new_track(
        self, track_name, track_num=None, description=None, collaborators=None
    ):
        """Add a track to an album."""
        track_path = get_track_path(self.path, track_name)
        track = Track(
            track_path,
            track_name,
            track_num,
            self.artist,
            self.name,
            description=description,
            collaborators=collaborators or [],
        )
        track.init_dir()
        self._add_track(track)
        self.save_album_metadata()

    def _add_track(self, track):
        self.tracks.append(track)
        self.save_album_metadata()

    def save_album_metadata(self):
        remove_file_if_exists(self.dir_json_path)
        full_json = self.to_json_for_album_dir()
        album_text = json.dumps(full_json, indent=2)
        with wopen(self.dir_json_path, "w") as album_file:
            album_file.write(album_text)
        return self

    def get_track(self, name):
        for track in self.tracks:
            if track.name == name:
                return track


def _parse_tracks(album_dir_json):
    tracks = album_dir_json.get(Consts.TRACKS, [])
    return [Track.from_json(album_dir_json, t) for t in tracks]


def _parse_releases(artist_name, album_name, album_dir_json):
    releases = album_dir_json.get(Consts.RELEASES)
    return [
        Release.from_json(artist_name, album_name, release_json)
        for release_json in releases
    ]
