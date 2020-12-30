class WildError(Exception):
    """This base-error trips us all up."""


class WildNotFoundError(WildError):
    """A base error for when a resource is not found."""


class ArtistAlreadySignedError(WildError):
    """An error raised when trying to sign an artist that is already signed."""

    def __init__(self, artist):
        msg = f"{artist} already signed."
        super().__init__(self, msg)


class ArtistNotSignedError(WildError):
    """An error raised when trying to unsign an artist that is not signed."""

    def __init__(self, artist):
        msg = f"{artist} is not signed."
        super().__init__(self, msg)


class ArtistNotFoundError(WildNotFoundError):
    """An error raised when an artist is not found in the local mgmt.json file."""

    def __init__(self, artist):
        msg = f"{artist} not found."
        super().__init__(self, msg)


class NoArtistsFoundError(WildNotFoundError):
    """An error raised when there are no artists."""

    def __init__(self):
        super().__init__(self, "No artists found.")


class ConfigFileNotFoundError(WildError):
    """An error raised when the given config file is not found."""

    def __init__(self, config_file):
        msg = f"{config_file} does not exist."
        super().__init__(self, msg)
