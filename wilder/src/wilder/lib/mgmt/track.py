from wilder.lib.constants import Constants


class Track:
    def __init__(
        self, name, track_num, artist, album, description=None, collaborators=None
    ):
        self.name = name
        self.track_number = track_num
        self.artist = artist
        self.album = album
        self.description = description
        self.collaborators = collaborators

    @classmethod
    def from_json(cls, artist_name, album_name, track_json):
        name = track_json.get(Constants.NAME)
        track_number = track_json.get(Constants.TRACK_NUMBER) or 1
        description = track_json.get(Constants.DESCRIPTION)
        collaborators = track_json.get(Constants.COLLABORATORS)
        return cls(
            name,
            track_number,
            artist_name,
            album_name,
            description=description,
            collaborators=collaborators,
        )

    def to_json(self):
        return {
            Constants.ARTIST: self.artist,
            Constants.NAME: self.name,
            Constants.DESCRIPTION: self.description,
            Constants.TRACK_NUMBER: self.track_number,
            Constants.COLLABORATORS: self.collaborators,
        }
