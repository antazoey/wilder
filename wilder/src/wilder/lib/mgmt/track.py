from wilder.lib.constants import Constants
from wilder.lib.mgmt.album_dir import get_track_json_path
from wilder.lib.util.sh import remove_file_if_exists


class Track:
    def __init__(
        self,
        album_path,
        name,
        track_num,
        artist,
        album,
        description=None,
        collaborators=None,
    ):
        self.album_path = album_path
        self.name = name
        self.track_number = track_num
        self.artist = artist
        self.album = album
        self.description = description
        self.collaborators = collaborators

    @property
    def dir_json_path(self):
        return get_track_json_path(self.album_path, self.name)

    @classmethod
    def from_json(cls, album_path, artist_name, album_name, track_json):
        name = track_json.get(Constants.NAME)
        track_number = track_json.get(Constants.TRACK_NUMBER) or 1
        description = track_json.get(Constants.DESCRIPTION)
        collaborators = track_json.get(Constants.COLLABORATORS)
        return cls(
            album_path,
            name,
            track_number,
            artist_name,
            album_name,
            description=description,
            collaborators=collaborators,
        )

    def to_json_for_track_dir(self):
        return {
            Constants.ARTIST: self.artist,
            Constants.NAME: self.name,
            Constants.DESCRIPTION: self.description,
            Constants.TRACK_NUMBER: self.track_number,
            Constants.COLLABORATORS: self.collaborators,
        }

    def save_track_metadata(self):
        remove_file_if_exists(self.dir_json_path)
