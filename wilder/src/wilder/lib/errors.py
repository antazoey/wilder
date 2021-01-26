class WildError(Exception):
    """This base-error trips us all up."""


class WildNotFoundError(WildError):
    """A base error for when a resource is not found."""


class ArtistAlreadyExistsError(WildError):
    """An error raised when trying to add an artist that is already signed."""

    def __init__(self, artist):
        msg = f"{artist} already signed."
        super().__init__(msg)


class ArtistNotFoundError(WildError):
    """An error raised when an artist does not exist."""

    def __init__(self, artist):
        msg = f"Artist '{artist}' is not registered."
        super().__init__(msg)


class NoArtistsFoundError(WildNotFoundError):
    """An error raised when there are no artists."""

    def __init__(self):
        super().__init__("No artists found.")


class AlbumNotFoundError(WildNotFoundError):
    """An error raised when an album is not found."""

    def __init__(self, album_name):
        super().__init__(f"Album '{album_name}' was not found.")


class ArtistHasNoAlbumsError(WildError):
    """An error raised when trying to perform an album-specific operation on an artist when the artist has no albums."""

    def __init__(self, artist_name):
        super().__init__(f"Artist '{artist_name}' does not have any albums.")


class AlbumAlreadyExistsError(WildError):
    """An error raised when trying to create an album that already exists."""

    def __init__(self, album_name):
        super().__init__(f"Album '{album_name}' already exists.")


class NotInAlbumError(WildError):
    """An error raised when trying to do an operation outside an album directory or there is no album.json when
    there needs to be."""

    def __init__(self):
        msg = (
            "Error: album not found. "
            "Try executing the command from an album directory or specifying the album option."
        )
        super().__init__(msg)


class InvalidAudioFileError(WildError):
    """An error raised when receiving a file that has non-audio mime-type when expecting one."""

    def __init__(self, file_path):
        super().__init__(f"File at '{file_path}' is not a supported audio file.")


class TrackNotFoundError(WildNotFoundError):
    """An error raised when the track was not found."""

    def __init__(self, album_name, prop, prop_name="name"):
        super().__init__(
            f"Track with {prop_name} '{prop}' on album '{album_name}' was not found."
        )


class NoTracksFoundErrorWildError(WildError):
    """An error raised when album has no tracks."""

    def __init__(self, album_name):
        super().__init__(f"Album '{album_name}' does not have any tracks.")


class TrackAlreadyExistError(WildError):
    """An error raised when trying to start a new track with the same name as another track on its album."""

    def __init__(self, track_name, album_name):
        msg = f"There is already a track named '{track_name}' on album '{album_name}'."
        super().__init__(msg)


class WildVLCPlayerLaunchError(WildError):
    """An error raised when trying to use VLC media player."""

    def __init__(self):
        super().__init__("VLC Media Player failed to launch.")


class UnsupportedAudioTypeError(WildError):
    """An error raised when receiving an unknown audio type."""

    def __init__(self, audio_type):
        super().__init__(f"Received unsupported audio-type '{audio_type}'.")


class AudioTypeNotFoundError(WildError):
    """An error raised when the audio-type requested was not found."""

    def __init__(self, track_name, audio_type):
        super().__init__(f"Track '{track_name}' has no audio-type '{audio_type}'.")


class NoAudioFoundError(WildError):
    """An error raised when a track has no audio."""

    def __init__(self, track_name):
        super().__init__(f"Track '{track_name}' has no audio.")
