class WildError(Exception):
    """This base-error trips us all up."""


class WildNotFoundError(WildError):
    """A base error for when a resource is not found."""


class ArtistAlreadySignedError(WildError):
    """An error raised when trying to sign an artist that is already signed."""

    def __init__(self, artist):
        msg = f"{artist} already signed."
        super().__init__(msg)


class ArtistNotSignedError(WildError):
    """An error raised when trying to unsign an artist that is not signed."""

    def __init__(self, artist):
        msg = f"{artist} is not signed."
        super().__init__(msg)


class ArtistNotFoundError(WildNotFoundError):
    """An error raised when an artist is not found in the local mgmt.json file."""

    def __init__(self, artist=None, msg=None):
        if artist:
            msg = f"Artist '{artist}' not found."
        super().__init__(msg)


class NoArtistsFoundError(WildNotFoundError):
    """An error raised when there are no artists."""

    def __init__(self):
        super().__init__("No artists found.")


class AlbumNotFoundError(WildNotFoundError):
    """An error raised when an album is not found."""

    def __init__(self, artist_name, album_name):
        super().__init__(f"Album '{album_name}' by '{artist_name}' was not found.")


class InvalidAudioFileError(WildError):
    """An error raised when receiving a file that has non-audio mime-type when expecting one."""

    def __init__(self, file_path):
        super().__init__(f"File at '{file_path}' is not a supported audio file.")


class TrackNotFoundError(WildNotFoundError):
    """An error raised when the track was not found."""

    def __init__(self, album_name, track_name):
        super().__init__(
            f"Track named '{track_name}' on album '{album_name}' was not found."
        )


class AlbumAlreadyExistsError(WildError):
    """An error raised when trying to create an album that already exists."""
    
    def __init__(self, album_name):
        super().__init__(f"Album '{album_name}' already exists.")
