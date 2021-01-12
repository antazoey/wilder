from wilder.constants import Constants


class Track:
    # The name of the track.
    name = None

    # The description of the track.
    description = None

    # The track number on the album it appears on.
    track_number = None

    # The .flp file.
    proj_file = None

    # Relational
    album = None

    # The artist of the track.
    artist = None

    # Additional collaborators on the track.
    collaborators = []

    def __init__(self, name, track_num, description=None, collaborators=None):
        self.name = name
        self.track_number = track_num
        self.description = description
        self.collaborators = collaborators

    @classmethod
    def from_json(cls, artist_name, album_name, track_json):
        name = track_json.get(Constants.NAME)
        track_number = track_json.get(Constants.TRACK_NUMBER)
        description = track_json.get(Constants.DESCRIPTION)
        collaborators = track_json.get(Constants.COLLABORATORS)
        track = cls(name, track_number)
        track.artist = artist_name
        track.album = album_name
        track.description = description
        track.collaborators = collaborators
        return track

    def to_json(self):
        return {
            Constants.NAME: self.name,
            Constants.DESCRIPTION: self.description,
            Constants.TRACK_NUMBER: self.track_number,
            Constants.COLLABORATORS: self.collaborators,
        }
