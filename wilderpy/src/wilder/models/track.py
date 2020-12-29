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

    @property
    def json(self):
        return {
            Constants.NAME: self.name,
            Constants.DESCRIPTION: self.description,
            Constants.TRACK_NUMBER: self.track_number,
            Constants.COLLABORATORS: self.collaborators,
        }
