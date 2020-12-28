class WildError(Exception):
    """This base-error trips us all up."""


class ArtistAlreadySignedError(Exception):
    """An error raised when trying to sign an artist that is already signed."""


class ArtistNotSignedError(Exception):
    """An error raised when trying to unsign an artist that is not signed."""


class ArtistNotFoundError(Exception):
    """An error raised when an artist is not found in the local mgmt.json file."""


class ConfigFileNotFoundError(Exception):
    """An error raised when the given config file is not found."""

    def __init__(self, config_file):
        msg = f"{config_file} does not exist."
        Exception.__init__(self, msg)


class ConfigAlreadyExistsError(Exception):
    """An error raised when trying to initialize a config when one already exists."""
